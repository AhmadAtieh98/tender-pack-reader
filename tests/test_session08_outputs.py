"""Session 08, items 2-6 of the owner's message: interpretations backed by evidence, A1-A3 completeness, the
clarification register, and the scope of the owner's confirmations. Real pack, disposable outputs only.

Passing these tests does not make any interpretation correct, any row accepted or any question worth sending.
"""
from __future__ import annotations

import csv
import json
import re

import pymupdf
import pytest
import yaml

from tenderpack import clarify, stage2
from tenderpack.register import found
from tenderpack.util import ROOT, load_yaml

EVIDENCE, PACK = ROOT / "build", ROOT / "config/pack.yaml"
PROPS = ROOT / "curation/register/proposals"


@pytest.fixture(scope="module")
def real():
    return stage2.run(EVIDENCE, PACK, ROOT)


@pytest.fixture(scope="module")
def written(real, tmp_path_factory):
    out = tmp_path_factory.mktemp("s08") / "out"
    return out, stage2.write(real, out)


def _row(r, rid):
    return next(e for e in r["evals"] if e["row"].id == rid)


# ---------------------------------------------------------------------------------------------- §3 interpretations

def test_owner_directed_interpretations_rest_on_verbatim_evidence(real):
    units = {u["unit_id"]: u for u in real["units"]}
    new = yaml.safe_load((PROPS / "2026-10-03_session-08_owner-directed.yaml").read_text(encoding="utf-8"))["proposals"]
    old = {p["id"]: p for p in yaml.safe_load((PROPS / "2026-10-03_stale-rows.yaml").read_text(encoding="utf-8"))["proposals"]}
    assert {p["row"] for p in new} == {"VOL-I-8.3-01", "VOL-I-3.4-01", "VOL-I-6.7-01"}
    for p in new:
        for e in p["evidence"]:
            if e["unit"] in units:                                  # quoted evidence: verbatim, on its page
                assert found(e["words"], units[e["unit"]]["text"]) and e["page"] in units[e["unit"]]["pages"], e
        o = old[p["supersedes"]]                                    # the original is kept, with the exact conflict
        assert o["status"] == "superseded" and o["superseded_by"] == p["id"] and o["superseded_because"]
        assert o["add_interpretation"]["note"]                      # unchanged text of the original
    # the evidence statements that are not quotations, checked mechanically
    add02 = next(s for s in real["stages"] if s.stage == "ADD-02")
    assert not [x for x in add02.ops if {x.op.target, *x.op.targets} & {"VOL-I:6.1", "VOL-I:6.7", "VOL-I:8.3"}]
    cure = re.compile(r"\bcur(e|ed|able)\b|rectif|remed|\bwaive", re.I)
    assert not [u for u in real["units"] if u["doc"] in ("VOL-I", "ADD-01", "ADD-02") and cure.search(u.get("text") or "")]


def test_the_three_rows_carry_the_direction_and_stay_proposed(real):
    for rid in ("VOL-I-8.3-01", "VOL-I-3.4-01", "VOL-I-6.7-01"):
        e = _row(real, rid)
        it = real["register"].interp_at(e["row"], "ADD-02")
        assert it.stage == "ADD-01" and "As directed by the owner on 3 Oct 2026" in it.note
        assert "[Applied from proposal P-S08-" in it.note
        assert not e["stages"]["ADD-01"]["stale"] and not e["stages"]["ADD-02"]["stale"]
        assert real["reviews"][("row", rid)]["status"] == "proposed"                 # the owner still decides
        assert e["stages"]["ADD-02"]["dates"][0]["planning"]["value"] == "2026-11-26"
    iso = real["register"].interp_at(_row(real, "VOL-I-8.3-01")["row"], "ADD-02")
    assert "11.1(i)" in iso.note and "accredited certification body" in iso.note and "Envelope A" in iso.note
    assert iso.consequence == "none_stated" and "14:00" in iso.note                  # no invented ISO label
    assert "can be cured" in iso.note and "neither is implied" in iso.note
    om = real["register"].interp_at(_row(real, "VOL-I-3.4-01")["row"], "ADD-02")
    assert "14:00" in om.note and "separate cut-off" in om.note and "5.2" in om.note
    wd = _row(real, "VOL-I-6.7-01")["row"]
    assert "only before" not in wd.requirement and "no modification will be accepted thereafter" in wd.requirement
    assert "modifications only" in real["register"].interp_at(wd, "ADD-02").note


# ---------------------------------------------------------------------------------------------- §4 A1-A3

def test_every_form_4g_undertaking_is_its_own_row(real):
    quotes = {}
    for e in real["evals"]:
        for u in e["row"].units:
            m = re.fullmatch(r"ADD-02:F4-G/T1/(\d)", u)
            if m:
                quotes.setdefault(int(m.group(1)), []).append(real["register"].interp_at(e["row"], "ADD-02").quote)
    assert sorted(quotes) == [1, 2, 3, 4, 5, 6] and all(len(v) == 1 for v in quotes.values())
    assert "twenty-four (24) hours" in quotes[4][0] and "penetration test" in quotes[5][0]
    assert "multi-factor authentication" in quotes[6][0] and "logged" in quotes[6][0]


def test_multi_unit_rows_keep_every_value_and_citation_in_a1(written):
    rows = {r["Requirement ID"]: r for r in csv.DictReader(open(written[0] / "a1/a1.csv", encoding="utf-8-sig"))}
    r = rows["VOL-II-2.1-01"]
    issued = r["Text as issued (original document; never assembled)"]
    for v in ("Peak (design): 480", "Average: 640", "Peak (design): 34 (max) / 14 (min)"):
        assert v in issued
    units = r["Every unit the row cites (reference at the validated state; amending ops)"]
    assert units.count("VOL-II T2-2/") == 6 and "VOL-II 2.1 p2" in units
    tn = rows["VOL-II-T2-4-TN"]
    assert tn["Status after ADD-02"].startswith("AMENDED (ADD-02/5.1)")
    assert "VOL-II T2-4/TN p3 as amended by ADD-02 5.1" in tn["Source after ADD-02 (latest reference for the quoted words)"]
    assert tn["Source after BASE (latest reference for the quoted words)"] == "VOL-II T2-4/TN p3"


def test_no_post_award_row_has_a_blank_evidence_field_or_claims_evidence(real, written):
    a1 = {r["id"]: r for r in json.loads((written[0] / "a1/a1.json").read_text(encoding="utf-8"))["rows"]}
    post = [e["row"] for e in real["evals"] if e["row"].assessment == "contractual_post_award"]
    assert post
    for row in post:
        assert a1[row.id]["evidence"], row.id
        pa = row.post_award_evidence
        if pa is not None:
            assert pa.text.startswith(("Post-award (proposed requirement): ", "Not applicable: ", "Unresolved: "))
            assert not re.search(r"\b(the Bidder|we) (has|have|holds?|hold)\b", pa.text)
    assert stage2.register_findings(real) == []


def test_a3_separates_explicit_gate_and_grouped_unresolved_on_one_page(written, real):
    out = written[0]
    a3 = json.loads((out / "a3/a3.json").read_text(encoding="utf-8"))
    heads = [s["heading"] for s in a3["sections"]]
    assert all(h.startswith(("Explicit — ", "General gate")) for h in heads)
    gate = next(s for s in a3["sections"] if s["heading"].startswith("General gate"))
    assert "VOL-I-8.3-01" in gate["ids"] and "11.1(i)" in gate["heading"]
    assert "VOL-IV-F4A-02" in gate["ids"] and "VOL-IV-F4A-02" not in a3["explicit_ids"]   # blank field != rejection
    late = next(x for x in a3["explicit"] if x["id"] == "VOL-I-6.1-01")
    assert "VOL-I 6.6" in late["source"] and "ADD-01 2.1" in late["source"]              # amendment beside consequence
    groups = a3["groups"]["groups"]
    listed = {i["id"] for g in groups for i in g["items"]} | {f for g in groups for i in g["items"] for f in i["folds"]}
    issue_ids = {i["id"] for i in a3["issues_detail"]}
    assert issue_ids - listed <= {"I-NO-CONSEQUENCE"}                                     # complete (gate note cites it)
    qs = {q for g in groups for q in g["questions"]}
    assert qs == {c["id"] for c in real["clarifications"]["clarifications"]}
    doc = pymupdf.open(out / "a3/a3.pdf")
    assert len(doc) == 1
    detail = (out / "a3/a3_detail.html").read_text(encoding="utf-8")
    assert all(f'id="{i}"' in detail for i in issue_ids | qs)


# ---------------------------------------------------------------------------------------------- §6 clarifications

def test_clarification_register_is_verified_unsent_and_keeps_settled_answers(real, written):
    reg = real["clarifications"]
    assert clarify.check(reg, real["units"], set(real["curated_issues"])) == []
    qs = {c["id"]: c for c in reg["clarifications"]}
    assert all(c["response_status"] == "draft, not sent" for c in qs.values())
    assert all(re.match(r"(Volume|Addendum)", c["proposed_question"]) for c in qs.values())   # VOL-I 5.1: cite the place
    assert "Q7" in qs["CQ-CONCESSION-TERM"]["already_settled"] and "precedence" in qs["CQ-CONCESSION-TERM"]["already_settled"]
    assert "Q11" in qs["CQ-DWF-STORM-FLOW"]["already_settled"] and "Q13" in qs["CQ-BOND-FC-COVERAGE"]["already_settled"]
    assert "Which applies" not in qs["CQ-CONCESSION-TERM"]["proposed_question"]              # not re-asked
    closed = " ".join(c["topic"] + " " + c["finding"] for c in reg["checked_no_question"])
    for settled in ("copy quantities", "Excel", "Form 4-G", "not contradictory"):
        assert settled in closed, settled
    for k in ("Form 4-A", "Envelope B", "Form 4-B"):                                         # the owner's interim approaches
        assert any(k in c["gap"] or k in c["proposed_question"] for c in qs.values()), k
    assert not [c for c in qs.values() if re.search(r"software|defect in the tool|assessment administration", c["gap"], re.I)]
    md = (written[0] / "a4/clarification_register.md").read_text(encoding="utf-8")
    assert "NOT SENT" in md and all(f"### {i} " in md for i in qs)


# ---------------------------------------------------------------------------------------------- §2 confirmations

def test_confirmation_scope_is_recorded_and_the_permit_is_not_claimed(real):
    appr = {a["region_id"]: a for a in load_yaml(ROOT / "curation/approvals.yaml")["approvals"]}
    t24 = appr["VOL-II-p3-r1"]
    assert "location of the precedence language" in t24["permit"]["confirmed"]
    assert any("contents" in x for x in t24["permit"]["not_confirmed"])
    assert any("compliance" in x for x in t24["permit"]["not_confirmed"])
    assert any("chlorine" in x.lower() for x in t24["keeps_open"]) and any("29.3" in x for x in t24["keeps_open"])
    f4c = appr["VOL-IV-p6-r1"]
    assert any("diacritic" in x for x in f4c["keeps_open"]) and any("exclusion" in x for x in f4c["keeps_open"])
    issues = {**load_yaml(ROOT / "curation/register/issues.yaml")["issues"]}
    assert "not claimed" in issues["I-PERMIT"]["text"] and "contents" in issues["I-PERMIT"]["text"]
    tn = _row(real, "VOL-II-T2-4-TN")
    assert tn["stages"]["BASE"]["cells"]["Limit"] == "5" and tn["stages"]["ADD-02"]["cells"]["Limit"] == "3"
    assert real["register"].interp_at(_row(real, "VOL-IV-F4C-04")["row"], "ADD-02").consequence.cls == "exclusion"
    ramp = _row(real, "VOL-V-29.3-01")["row"]
    assert "not an exemption from technical compliance or commissioning" in ramp.requirement
