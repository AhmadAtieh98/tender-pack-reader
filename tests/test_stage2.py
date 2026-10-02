"""Stage 2 (session 04): the amendment path, the A1 register slice and the A2/A3/A5 outputs.

Expectations come from tests/golden/stage2_expectations.yaml, an oracle written by an independent
reader of the source PDFs who did not read or run the program. Scenario tests (wrong target, staleness,
partial addendum) change only the curated inputs, in disposable copies, and run the same code path
as a real build: stage2.run -> stage2.write / stage2.build.

Passing these tests does not make any interpretation correct or any reading approved.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pymupdf
import pytest
import yaml

from tenderpack import stage2
from tenderpack.amend import load_opfile
from tenderpack.register import Consequence, printed_date_conflicts
from tenderpack.util import ROOT

GOLD = yaml.safe_load((ROOT / "tests/golden/stage2_expectations.yaml").read_text(encoding="utf-8"))
EVIDENCE = ROOT / "build"
PACK = ROOT / "config/pack.yaml"
STAGES = ("BASE", "ADD-01", "ADD-02")


@pytest.fixture(scope="module")
def real():
    return stage2.run(EVIDENCE, PACK, ROOT)


@pytest.fixture(scope="module")
def written(real, tmp_path_factory):
    out = tmp_path_factory.mktemp("s2") / "out"
    res = stage2.write(real, out)
    return out, res


def st(r, stage):
    return next(s for s in r["stages"] if s.stage == stage)


def ev(r, row_id, stage):
    return next(e for e in r["evals"] if e["row"].id == row_id)["stages"][stage]


def uid(label: str) -> str | None:
    """Oracle unit label ('VOL-II 4.4') -> unit id ('VOL-II:4.4'); None for labels that are not one clause."""
    doc, _, rest = label.partition(" ")
    return f"{doc}:{rest}" if rest and rest.replace(".", "").isdigit() else None


def scenario_pack(tmp: Path, mutate_ops=None, mutate_rows=None) -> Path:
    """A disposable copy of the curated Stage 2 inputs (amendments, rows, pins), changed by the callbacks,
    and a pack.yaml pointing at them. Sources, evidence and every other input are the real ones."""
    amend = tmp / "amendments"
    shutil.copytree(ROOT / "curation/amendments", amend)
    reg = tmp / "register"
    shutil.copytree(ROOT / "curation/register", reg)
    if mutate_ops:
        for f in sorted(amend.glob("ADD-*.yaml")):
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
            mutate_ops(data)
            f.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    if mutate_rows:
        data = yaml.safe_load((reg / "rows.yaml").read_text(encoding="utf-8"))
        mutate_rows(data)
        (reg / "rows.yaml").write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    cfg = yaml.safe_load(PACK.read_text(encoding="utf-8"))
    cfg.update({"amendments_dir": str(amend), "register": str(reg / "rows.yaml"), "issues": str(reg / "issues.yaml")})
    p = tmp / "pack.yaml"
    p.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
    return p


# ============================================================================ the amendment path

def test_existing_addenda_apply_in_order_and_are_validated(real):
    assert [(s.stage, s.status, s.issued) for s in real["stages"]] == [
        ("BASE", "BASE", None), ("ADD-01", "APPLIED", GOLD["meta"]["stages"]["ADD-01"]["issued"]),
        ("ADD-02", "APPLIED", GOLD["meta"]["stages"]["ADD-02"]["issued"])]
    assert real["validated"].stage == "ADD-02" and real["working"] is None
    for s in real["stages"][1:]:
        assert not s.scope_leak and not s.problems
        assert all(x.valid for x in s.ops), [x.op.id for x in s.ops if not x.valid]
        # every op is a proposal: none accepted by a person
        assert {x.op.review for x in s.ops} == {"proposed"}


def _oracle_unit(add: str, item: str) -> list[str]:
    """Oracle provision id -> our unit ids (naming translation only)."""
    if item.startswith("Q") or item[0].isdigit():
        return [f"{add}:{item}"]
    if item == "Appendix A":
        return [f"{add}:AppA/para1"]
    if item == "Appendix B":
        return [f"{add}:AppB/para1", f"{add}:AppB/present"]
    if item.startswith("Appendix B Item "):
        return [f"{add}:AppB/item-{item.rsplit(' ', 1)[1]}-"]                 # prefix
    if item.startswith("T1-1 row "):
        return [f"{add}:T1-1-rev/{item.rsplit(' ', 1)[1].replace('Total', 'total')}"]
    if item.startswith("T1-1 note "):
        return [f"{add}:T1-1-rev/note{item.rsplit(' ', 1)[1]}"]
    if item == "Form 4-G":
        return [f"{add}:F4-G/para1"]
    if item.startswith("Form 4-G item "):
        return [f"{add}:F4-G/T1/{item.rsplit(' ', 1)[1]}"]
    return []                                                                  # 'T1-1 (revised)': the table itself


@pytest.mark.parametrize("add", ["ADD-01", "ADD-02"])
def test_every_oracle_provision_is_accounted_for_and_every_amending_one_has_an_op(real, add):
    cov = {c["provision"]: c for c in st(real, add).coverage}
    assert all(c["disposition"] not in ("UNACCOUNTED", "unresolved") for c in cov.values())
    outside = []
    for item in GOLD["provisions"][add]["items"]:
        ids = _oracle_unit(add, item["id"])
        if not ids:
            continue
        hits = [c for k, c in cov.items() if any(k == i or (i.endswith("-") and k.startswith(i)) for i in ids)]
        assert hits, f"oracle provision {add} {item['id']} has no coverage entry"
        if item.get("amends") and not item["id"].startswith(("T1-1 row", "Form 4-G item")):
            assert all(c["disposition"] in ("op", "outside_slice") for c in hits), (item["id"], [c["disposition"] for c in hits])
            outside += [item["id"] for c in hits if c["disposition"] == "outside_slice"]
    # the only amending provision left outside the slice: the new scoring method (not defined in the pack)
    assert outside == ({"ADD-01": [], "ADD-02": ["T1-1 note (3)"]}[add])


def test_pdd_moves_and_its_dependants_are_recomputed(real):
    for stage in STAGES:
        e = ev(real, "VOL-I-6.1-01", stage)
        assert e["dates"][0]["planning"]["value"] == GOLD["pdd"][stage]["date"]
    assert ev(real, "VOL-I-6.1-01", "ADD-01")["text"] == GOLD["pdd"]["ADD-01"]["expected_clause_text"]
    d = GOLD["dates"]
    cut = {s: ev(real, "VOL-I-5.2-01", s)["dates"][0] for s in ("BASE", "ADD-01")}
    assert cut["BASE"]["planning"]["value"] == d["BASE"]["clarification_cutoff"]["value"]
    assert cut["ADD-01"]["planning"]["value"] == d["ADD-01"]["clarification_cutoff"]["value"]
    for row, key in (("VOL-I-6.3-01", "bid_bond_validity_end"), ("VOL-I-7.1-01", "proposal_validity_end"),
                     ("VOL-I-8.5-01", "reference_plant_lookback_start")):
        for stage in ("BASE", "ADD-01"):
            vals = {i["value"] for i in ev(real, row, stage)["dates"][0]["interpretations"]}
            want = {d[stage][key]["pdd_as_day_0"], d[stage][key]["pdd_as_day_1"]}
            assert vals == want, (row, stage, vals, want)
            assert ev(real, row, stage)["dates"][0]["readings_differ"]
    win = {i["value"] for i in ev(real, "ADD-01-3.1-01", "ADD-01")["dates"][0]["interpretations"]}
    w = d["ADD-01"]["add01_3_1_window_end"]
    assert win == {w["issue_date_not_counted"], w["issue_date_counted"]}
    # ADD-02 does not move the PDD: every derived date equals ADD-01's
    for e in real["evals"]:
        if e["stages"]["ADD-01"]["active"] and e["stages"]["ADD-02"]["active"]:
            assert [x["planning"] for x in e["stages"]["ADD-01"]["dates"]] == [x["planning"] for x in e["stages"]["ADD-02"]["dates"]]


def test_footnote_lookback_is_a_dependency_of_the_pdd(real):
    """Footnote 12 to VOL-I 8.5 (ten years preceding the PDD) is named by ADD-01 2.2; the row reads the
    footnote and depends on the PDD's defining clause."""
    e = ev(real, "VOL-I-8.5-01", "ADD-01")
    assert e["effective_unit"] == "VOL-I:8.5#fn12" or "VOL-I:8.5#fn12" in next(
        x for x in real["evals"] if x["row"].id == "VOL-I-8.5-01")["row"].units
    pins = next(x for x in real["evals"] if x["row"].id == "VOL-I-8.5-01")["row"].interpretations[0].pins
    assert "VOL-I:6.1" in pins


def test_lcc_deletion_reinstatement_and_revocation_chain(real):
    g = GOLD["lcc"]
    assert ev(real, "VOL-I-8.6-01", "BASE")["status"] == "ACTIVE"
    assert ev(real, "VOL-I-8.6-01", "ADD-01")["status"].startswith("DELETED")
    a2 = ev(real, "VOL-I-8.6-01", "ADD-02")
    assert a2["status"].startswith("REINSTATED") and a2["text"] == g["ADD-02"]["expected_clause_text"]
    assert ev(real, "VOL-I-8.6-01", "BASE")["text"] == g["BASE"]["evidence"]["quote"]
    it = real["register"].interp_at(next(x for x in real["evals"] if x["row"].id == "VOL-I-8.6-01")["row"], "ADD-02")
    assert isinstance(it.consequence, Consequence) and it.consequence.cls == "non_responsive"
    assert it.consequence.quote == g["ADD-02"]["consequence_quote"]
    assert real["register"].interp_at(next(x for x in real["evals"] if x["row"].id == "VOL-I-8.6-01")["row"], "BASE").consequence == "none_stated"
    # ADD-01 4.2 (disregard any LCC reference): not issued, in effect, then ceases to have effect
    assert [st(real, s).state["ADD-01:4.2"].status for s in STAGES] == ["not_issued", "active", "revoked"]
    assert len(a2["chain"]) == 3 and "ADD-01/4.1" in a2["chain"][1] and "ADD-02/9.1" in a2["chain"][2]


@pytest.mark.parametrize("entry", [e["id"] for e in GOLD["repeated_wording"]])
def test_repeated_wording_changes_only_the_cited_occurrence(real, entry):
    g = next(e for e in GOLD["repeated_wording"] if e["id"] == entry)
    target = uid(g["changes"]["unit"])
    if target and g["changes"].get("ADD-02_value"):
        base, after = st(real, "BASE").state[target].text, st(real, "ADD-02").state[target].text
        assert base != after
        if g["changes"].get("ADD-02_expected_sentence"):
            assert g["changes"]["ADD-02_expected_sentence"] in after
    for m in g.get("must_not_change", []):
        u = uid(m["unit"])
        if u and u in st(real, "BASE").state:
            assert st(real, "BASE").state[u].text == st(real, "ADD-02").state[u].text, m["unit"]
            assert not st(real, "ADD-02").state[u].history, m["unit"]


def test_vol_v_31_3_is_recorded_as_same_words_not_targeted(real):
    x = next(x for x in st(real, "ADD-02").ops if x.op.id == "ADD-02/4.1")
    assert x.details.get("also_in") == ["VOL-V:31.3"]
    assert ev(real, "VOL-V-31.3-01", "ADD-02")["status"] == "ACTIVE"


def test_weighting_change_and_table_1_1(real):
    g = GOLD["weighting"]
    assert "sixty per cent (60%) technical and forty per cent (40%)" in st(real, "ADD-01").state["VOL-I:11.2"].text
    assert "sixty-five per cent (65%) technical and thirty-five per cent (35%) commercial" in st(real, "ADD-02").state["VOL-I:11.2"].text
    assert st(real, "ADD-02").state["VOL-V:29.2"].text == st(real, "BASE").state["VOL-V:29.2"].text
    for stage in STAGES:
        state = st(real, stage).state
        t = state["VOL-I:T1-1"]
        table = t.superseded_by if t.status == "superseded" else "VOL-I:T1-1"
        marks = {k.rsplit("/", 1)[1]: int(u.cells["Marks"]) for k, u in state.items()
                 if k.startswith(table + "/") and u.kind == "table_row" and u.status == "active" and u.label in "ABCDEF"}
        assert marks == g["table_1_1"][stage]["marks"], stage
    assert ev(real, "VOL-I-T1-1-B", "ADD-02")["cells"]["Marks"] == "15"
    assert ev(real, "VOL-I-T1-1-D", "ADD-02")["cells"]["Marks"] == "20"


def test_image_based_tn_amended_from_a_pending_reading(real):
    g = GOLD["tn"]
    for stage in STAGES:
        u = st(real, stage).state["VOL-II:T2-4/TN"]
        assert u.cells["Limit"] == g[stage]["limit"] and u.cells["Unit"] == g[stage]["unit"]
        assert u.cells["Basis of assessment"] == g[stage]["basis"]
        assert u.reading_status == "pending"
    for key, row in g["other_rows_unchanged_at_all_stages"].items():
        assert st(real, "ADD-02").state[f"VOL-II:T2-4/{key}"].cells["Limit"] == row["limit"]
    x = next(x for x in st(real, "ADD-02").ops if x.op.id == "ADD-02/5.1")
    assert x.details["old_value"] == "5" and x.details["reading_status"] == "pending"
    e = ev(real, "VOL-II-T2-4-TN", "ADD-02")
    assert e["transcription"] == "pending"
    assert "amended value replaces a value read from an image still pending review" in e["flags"]


def test_form_4g_inserted_after_item_e_with_its_consequence(real):
    g = GOLD["form_4g"]
    for stage in STAGES:
        exists = st(real, stage).state["ADD-02:F4-G/T1/1"].status == "active"
        assert exists == g["exists"][stage]
    x = next(x for x in st(real, "ADD-02").ops if x.op.id == "ADD-02/7.1")
    assert x.op.anchor == "VOL-I:9.1(e)" and x.valid
    assert "re-lettering" in (x.op.issue or "")
    row = next(x for x in real["evals"] if x["row"].id == "ADD-02-7.2-01")["row"]
    it = real["register"].interp_at(row, "ADD-02")
    assert it.consequence.cls == "non_responsive" and it.consequence.quote == g["consequence"]["quote"]
    assert ev(real, "ADD-02-7.2-01", "ADD-01")["status"] == "NOT ISSUED"


def test_arabic_form_4c_consequences_are_kept_in_arabic_and_pending(real, written):
    g = GOLD["form_4c"]
    rows = {x["row"].id: x for x in real["evals"]}
    c4 = real["register"].interp_at(rows["VOL-IV-F4C-04"]["row"], "ADD-02").consequence
    assert c4.cls == "exclusion" and c4.quote == g["declaration_4"]["consequence_arabic"] and c4.gloss
    cn = real["register"].interp_at(rows["VOL-IV-F4C-N1"]["row"], "ADD-02").consequence
    assert cn.cls == "non_responsive" and cn.quote in g["arabic_note"]["arabic"]
    for rid in ("VOL-IV-F4C-04", "VOL-IV-F4C-N1", "VOL-I-9.4-01"):
        for stage in STAGES:
            assert rows[rid]["stages"][stage]["transcription"] == "pending"
    a3 = json.loads((written[0] / "a3/a3.json").read_text(encoding="utf-8"))
    item = next(i for s in a3["sections"] for i in s["items"] if i["id"] == "VOL-IV-F4C-04")
    assert item["consequence"] == g["declaration_4"]["consequence_arabic"] and "image reading pending" in item["flags"]
    assert "I-READING-F4C" in {i["id"] for i in a3["unresolved"]["items"]} or \
        any("pending" in i["text"] and "VOL-IV-F4C-04" in i["text"] for i in a3["unresolved"]["items"])


def test_conflicting_form_4a_printed_date_is_raised_not_corrected(real):
    g = GOLD["form_4a"]
    assert printed_date_conflicts(st(real, "BASE"), real["rowfile"].anchors) == []
    for stage in ("ADD-01", "ADD-02"):
        c = printed_date_conflicts(st(real, stage), real["rowfile"].anchors)
        assert [(x["unit"], x["printed"], x["effective"]) for x in c] == [
            ("ADD-01:AppA/proposal-due-date", g["reissued"]["printed_pdd"]["date"],
             g["printed_pdd_matches_stage_pdd"][stage]["stage_pdd"])]
        assert "12 November 2026" in st(real, stage).state["ADD-01:AppA/proposal-due-date"].text   # not rewritten
    s1 = st(real, "ADD-01").state
    assert s1["VOL-IV:F4-A/proposal-due-date"].superseded_by == "ADD-01:AppA/proposal-due-date"
    # fields the reissue drops have no counterpart: they point at the reissued form as a whole
    omitted = [k for k, u in s1.items() if k.startswith("VOL-IV:F4-A/") and u.superseded_by == "ADD-01:AppA"]
    assert {"VOL-IV:F4-A/commercial-registration-number", "VOL-IV:F4-A/registered-address"} <= set(omitted)
    assert ev(real, "VOL-IV-F4A-01", "ADD-01")["effective_unit"] == "ADD-01:AppA/proposal-due-date"


def test_answers_quoting_old_values_are_listed_for_review_never_revoked(real):
    listed = {(s.stage, a["answer"]) for s in real["stages"][1:] for a in stage2.answers_to_review(real, s)}
    assert ("ADD-02", "ADD-01:Q2") in listed
    assert all(a["status"] == "REVIEW (not automatically revoked)" for s in real["stages"][1:]
               for a in stage2.answers_to_review(real, s))
    # the answer itself stays in force
    assert st(real, "ADD-02").state["ADD-01:Q2"].status == "active"
    for neg in GOLD["answers_quoting_unchanged_values"]:
        u = neg["unit"].replace(" ", ":")
        assert not any(a == u for _, a in listed), f"{u} quotes or cites only unchanged values"


def test_non_binding_minutes_are_context_not_answers(real):
    cov = {c["provision"]: c for c in st(real, "ADD-01").coverage}
    minutes = [k for k in cov if k.startswith("ADD-01:AppB/")]
    assert len(minutes) == 9
    assert all(cov[k]["disposition"] == "no_effect" and "non-binding" in cov[k]["reason"] for k in minutes)
    # the 'seventy / thirty' remark does not change the weighting at ADD-01
    assert "sixty per cent (60%)" in st(real, "ADD-01").state["VOL-I:11.2"].text


# ============================================================================ outputs

def test_outputs_are_complete_and_structurally_ok(written):
    out, res = written
    assert res["status"] == "ok", res["checks"]
    for f in ("a1/a1.xlsx", "a1/a1.csv", "a1/a1.json", "a2/a2.md", "a2/a2_changes.csv", "a2/a2_provisions.csv",
              "a2/a2_rows_moved.csv", "a2/a2_answers_to_review.csv", "a3/a3.pdf", "a3/a3.json",
              "a5/programme.csv", "a5/marshalling.csv", "a5/replan_deltas.csv", "a5/stages/ADD-02.json",
              "checks.json", "stages.json", "README.md"):
        assert (out / f).is_file(), f
    assert len(pymupdf.open(out / "a3/a3.pdf")) == 1


def test_a1_carries_status_at_each_stage_and_separate_review_statuses(written):
    a1 = json.loads((written[0] / "a1/a1.json").read_text(encoding="utf-8"))
    assert a1["stages"] == list(STAGES)
    rows = {r["id"]: r for r in a1["rows"]}
    assert [rows["VOL-I-8.6-01"][f"status:{s}"].split(" ")[0] for s in STAGES] == ["ACTIVE", "DELETED", "REINSTATED-AMENDED"]
    assert rows["VOL-II-T2-4-TN"]["transcription"] == "pending"
    assert all(r["interpretation"] == "proposed (not reviewed)" for r in a1["rows"])
    assert rows["VOL-I-6.1-01"]["transcription"] == "n/a (text layer)"
    assert {"Dates", "Issues", "Stages", "Assumptions"} <= set(a1["sheets"])


def test_a3_lists_explicit_consequences_only_with_quotes(written, real):
    a3 = json.loads((written[0] / "a3/a3.json").read_text(encoding="utf-8"))
    explicit = a3["sections"][0]["items"]
    for item in explicit:
        row = next(x for x in real["evals"] if x["row"].id == item["id"])["row"]
        c = real["register"].interp_at(row, "ADD-02").consequence
        assert isinstance(c, Consequence) and item["consequence"] == c.quote
    ids = {i["id"] for i in explicit}
    assert {"VOL-I-8.6-01", "ADD-02-7.2-01", "VOL-IV-F4C-04"} <= ids
    assert "VOL-I-6.3-01" not in ids              # no consequence stated: listed separately
    assert "VOL-I-6.3-01" in {i["id"] for i in a3["sections"][2]["items"]}


def test_a5_is_generated_from_rows_in_force_with_labelled_assumptions(written, real):
    prog = json.loads((written[0] / "a5/stages/ADD-02.json").read_text(encoding="utf-8"))
    force = {e["row"].id for e in real["evals"] if e["stages"]["ADD-02"]["status"].startswith(("ACTIVE", "AMENDED", "REINSTATED", "NEW"))}
    for a in prog["activities"]:
        assert set(a["req_ids"]) <= force and a["req_ids"]
        assert a["duration_basis"].startswith("ASSUMPTION")
    acts = {a["id"]: a for a in prog["activities"]}
    assert acts["lcc-certificate"]["status"] == "INFEASIBLE by 7 WD"
    assert acts["attendance-notice"]["status"] == "DEADLINE PASSED"
    assert acts["deliver"]["latest_finish"] == "2026-11-26"
    a1prog = json.loads((written[0] / "a5/stages/ADD-01.json").read_text(encoding="utf-8"))
    assert "lcc-certificate" not in {a["id"] for a in a1prog["activities"]}     # deleted at ADD-01
    assert next(a for a in a1prog["activities"] if a["id"] == "attendance-notice")["status"] == "OK"
    deltas = json.loads((written[0] / "a5/replan_deltas.json").read_text(encoding="utf-8"))["rows"]
    assert {"activity": "lcc-certificate", "change": "NEW"} in [{k: d[k] for k in ("activity", "change")} for d in deltas]


def test_pending_image_status_carries_through_a1_a3_a5(written):
    out = written[0]
    a1 = {r["id"]: r for r in json.loads((out / "a1/a1.json").read_text(encoding="utf-8"))["rows"]}
    a3 = json.loads((out / "a3/a3.json").read_text(encoding="utf-8"))
    a5 = json.loads((out / "a5/stages/ADD-02.json").read_text(encoding="utf-8"))
    for rid in ("VOL-II-T2-4-TN", "VOL-IV-F4C-04", "VOL-IV-F4C-N1"):
        assert a1[rid]["transcription"] == "pending"
        item = next(i for s in a3["sections"] for i in s["items"] if i["id"] == rid)
        assert "image reading pending" in item["flags"]
        acts = [a for a in a5["activities"] if rid in a["req_ids"]]
        assert acts and all(f"IMAGE READING PENDING ({rid})" in a["flags"] for a in acts)
    assert not (ROOT / "curation/approvals.yaml").exists()


def test_two_builds_are_byte_identical(real, tmp_path):
    hashes = []
    for name in ("a", "b"):
        stage2.write(stage2.run(EVIDENCE, PACK, ROOT), tmp_path / name)
        hashes.append({p.relative_to(tmp_path / name).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in sorted((tmp_path / name).rglob("*")) if p.is_file()})
    assert hashes[0] == hashes[1]


# ============================================================================ scenarios (disposable copies)

def test_wrong_target_is_rejected_and_the_validated_state_is_kept(tmp_path):
    def retarget(data):
        for o in data.get("ops", []):
            if o["id"] == "ADD-02/4.1":
                o["target"] = "VOL-V:31.3"           # same words, but not the clause the provision cites
    r = stage2.run(EVIDENCE, scenario_pack(tmp_path, mutate_ops=retarget), ROOT)
    s = st(r, "ADD-02")
    x = next(x for x in s.ops if x.op.id == "ADD-02/4.1")
    assert not x.valid and any(c["id"] == "C22" and not c["ok"] for c in x.checks)
    assert s.status == "PARTIAL" and r["validated"].stage == "ADD-01" and r["working"].stage == "ADD-02"
    assert "seventy-two (72) hours" in s.state["VOL-V:31.3"].text        # not applied to the wrong clause
    assert "seventy-two (72) hours" in s.state["VOL-II:4.4"].text        # nor to the right one
    cov = next(c for c in s.coverage if c["provision"] == "ADD-02:4.1")
    assert cov["disposition"] == "unresolved"


def test_partial_addendum_preserves_the_last_validated_state_in_outputs(tmp_path):
    def drop(data):
        if data["addendum"] == "ADD-02":
            data["dispositions"] = [d for d in data["dispositions"] if d["provision"] != "ADD-02:Q12"]
    r = stage2.run(EVIDENCE, scenario_pack(tmp_path, mutate_ops=drop), ROOT)
    assert st(r, "ADD-02").status == "PARTIAL" and r["validated"].stage == "ADD-01"
    res = stage2.write(r, tmp_path / "out")
    assert res["status"] == "ok"                 # partial is reported, not a structural failure
    a1 = json.loads((tmp_path / "out/a1/a1.json").read_text(encoding="utf-8"))
    assert a1["validated_stage"] == "ADD-01" and a1["working_stage"] == "ADD-02"
    assert "WORKING, not validated" in next(c["header"] for c in a1["columns"] if c["key"] == "status:ADD-02")
    a3 = json.loads((tmp_path / "out/a3/a3.json").read_text(encoding="utf-8"))
    assert a3["subtitle"].startswith("Validated state ADD-01") and "NOT used here" in a3["subtitle"]
    assert "I-PARTIAL-ADD-02" in {i["id"] for i in a3["unresolved"]["items"]}
    main = json.loads((tmp_path / "out/a5/programme.json").read_text(encoding="utf-8"))["rows"]
    assert "lcc-certificate" not in {a["id"] for a in main}     # A5 from ADD-01 (LCC deleted), not ADD-02
    assert (tmp_path / "out/a5/working/ADD-02.json").is_file()


def test_an_op_on_a_clause_its_provision_does_not_cite_is_rejected(tmp_path):
    """ADD-02 Q8 answers about VOL-I 6.4; an op claiming it changes VOL-I 6.3 fails C22 and is not applied."""
    def misattach(data):
        if data["addendum"] == "ADD-02":
            data["ops"].append({"id": "ADD-02/Q8-test", "provision": "ADD-02:Q8", "type": "annotate",
                                "targets": ["VOL-I:6.3"], "effect": "interprets", "origin": "assistant",
                                "review": "proposed", "note": "synthetic test op"})
    r = stage2.run(EVIDENCE, scenario_pack(tmp_path, mutate_ops=misattach), ROOT)
    x = next(x for x in st(r, "ADD-02").ops if x.op.id == "ADD-02/Q8-test")
    assert not x.valid and [c["id"] for c in x.checks if not c["ok"]] == ["C22"]
    assert "ADD-02/Q8-test" not in st(r, "ADD-02").state["VOL-I:6.3"].annotations
    assert st(r, "ADD-02").status == "PARTIAL" and r["validated"].stage == "ADD-01"


def test_dependency_staleness_from_a_new_clarification(tmp_path):
    """A further answer about a clause is a new dependency: rows reading that clause become STALE (their
    interpretation needs a person again) and the flag reaches A5 and the issues list."""
    def add_answer(data):
        if data["addendum"] == "ADD-02":
            data["ops"].append({"id": "ADD-02/Q8-test", "provision": "ADD-02:Q8", "type": "annotate",
                                "targets": ["VOL-I:6.4"], "effect": "interprets", "origin": "assistant",
                                "review": "proposed", "note": "synthetic test op"})
    r = stage2.run(EVIDENCE, scenario_pack(tmp_path, mutate_ops=add_answer), ROOT)
    assert st(r, "ADD-02").status == "APPLIED"
    for rid in ("VOL-I-6.4-01", "VOL-I-6.4-02"):
        assert ev(r, rid, "ADD-02")["stale"] == ["VOL-I:6.4 changed since ADD-02"]
        assert ev(r, rid, "ADD-01")["stale"] == []
    res = stage2.write(r, tmp_path / "out")
    a5 = json.loads((tmp_path / "out/a5/stages/ADD-02.json").read_text(encoding="utf-8"))
    assert any("REQUIREMENT STALE (VOL-I-6.4-01)" in a["flags"] for a in a5["activities"])
    assert {"VOL-I-6.4-01", "VOL-I-6.4-02"} <= set(next(i for i in res["issues"] if i["id"] == "I-AUTO-STALE")["rows"])


def test_pdd_change_leaves_unreinterpreted_dependants_stale(real):
    """VOL-I 8.3 (ISO current at the PDD) has no re-interpretation after ADD-01 moved the PDD."""
    assert ev(real, "VOL-I-8.3-01", "BASE")["stale"] == []
    stale = ev(real, "VOL-I-8.3-01", "ADD-01")["stale"]
    assert stale == ["VOL-I:6.1 changed since BASE (by ADD-01/2.1)"]
    assert ev(real, "VOL-I-8.3-01", "ADD-01")["dates"][0]["planning"]["value"] == "2026-11-26"   # still recomputed


def test_a_quote_missing_from_the_effective_text_is_a_structural_failure_and_keeps_previous_outputs(tmp_path):
    out = tmp_path / "out"
    first = stage2.build(EVIDENCE, out, PACK, ROOT, quiet=True)
    assert first["exit_code"] == 0
    before = (out / "a1/a1.json").read_bytes()

    def bad_quote(data):
        for row in data["rows"]:
            if row["id"] == "VOL-II-4.4-01":
                row["interpretations"][-1]["quote"] = "for not less than sixty (60) hours"
    res = stage2.build(EVIDENCE, out, scenario_pack(tmp_path, mutate_rows=bad_quote), ROOT, quiet=True)
    assert res["exit_code"] == 2 and not next(c for c in res["checks"] if c["id"] == "C16")["ok"]
    assert (out / "a1/a1.json").read_bytes() == before
    assert (tmp_path / "out.failed/checks.json").is_file()


def test_outputs_refuse_to_write_into_the_repository(tmp_path):
    from tenderpack.cli import UnsafeOutputError
    for bad in (ROOT, ROOT / "curation", ROOT / "build"):
        with pytest.raises(UnsafeOutputError):
            stage2.build(EVIDENCE, bad, PACK, ROOT, quiet=True)


def test_transcription_approval_stays_separate_from_interpretation(tmp_path):
    """In a disposable copy, a FIXTURE reviewer approves the Table 2-4 reading: TN's transcription becomes
    approved; its interpretation stays proposed, and every other reading stays pending. The real
    curation/approvals.yaml is never created."""
    from tenderpack.cli import approve, ingest
    approvals = tmp_path / "approvals.yaml"
    cfg = yaml.safe_load(PACK.read_text(encoding="utf-8"))
    cfg["approvals"] = str(approvals)
    pack = tmp_path / "pack.yaml"
    pack.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
    assert approve("VOL-II-p3-r1", "Fixture Test Reviewer", "disposable test", ROOT, pack, approvals) == 0
    res = ingest(pack, tmp_path / "evidence", ROOT, quiet=True)
    assert res["exit_code"] == 0
    r = stage2.run(tmp_path / "evidence", pack, ROOT)
    e = ev(r, "VOL-II-T2-4-TN", "ADD-02")
    assert e["transcription"] == "approved"
    assert next(x for x in r["evals"] if x["row"].id == "VOL-II-T2-4-TN")["row"].review == "proposed"
    assert ev(r, "VOL-IV-F4C-04", "ADD-02")["transcription"] == "pending"
    assert not (ROOT / "curation/approvals.yaml").exists()
