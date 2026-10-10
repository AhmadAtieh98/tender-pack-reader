"""Session 11 (owner's item 4): a PARTIAL addendum keeps the validated A3 and A5 exactly as they are and adds clearly
labelled CANDIDATE consequences and programme impacts from the working stage (tenderpack/partial.py): a3/a3_candidate.*
and a5/candidate/, the blockers, the conditional scenarios, the image-read units with their review packets, and a
paragraph in the diff and the AI review packet on what may be changing.

The packs are rehearsal packs built into disposable folders by the conftest fixtures (never rehearsals/*/build). The
partial op files are copies of the curated ADD-03 op files of blind rehearsals 02 and 03 with two provisions left
unresolved; the unresolved reasons are this test's own words (one of them deliberately says 'conditional amendment ...
by Thursday 12 November 2026' to exercise how the candidate renders conditional information an op file carries; the
addendum itself says nothing of the kind). Nothing is written under rehearsals/, curation/, config/ or out/.

The validated A3 PDF writer is replaced by a stand-in in the full writes below (it spends minutes rewriting links; its
output is a pure function of the page data it is handed, which the stand-in writes instead, so two writes still compare
what A3 would draw). The candidate PDF is rendered for real."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import pymupdf
import pytest
import yaml

from tenderpack import live, partial, programme, stage2
from tenderpack.render import write_candidate_a3_pdf

ROOT = Path(__file__).resolve().parents[1]
UNRESOLVED_02 = {
    "ADD-03:3.2": "insufficient evidence (test fixture): left for a person; the bid bond validity is not settled here",
    "ADD-03:5.3": "escalated (test fixture wording, not the addendum's): treated as a conditional amendment that takes "
                  "effect only if the Authority gives notice by Thursday 12 November 2026",
}
UNRESOLVED_03 = {"ADD-03:6.1": "unresolved (test fixture): left for a person",
                 "ADD-03:Q17": "unresolved (test fixture): left for a person"}


def _fast_a3_pdf(page: dict, path) -> dict:
    """Stands in for render.write_a3_pdf: writes the page data the writer would draw (see the module docstring)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json.dumps(page, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8"))
    return {"pages": 1, "scale": 1.0, "spare_pt": 0.0, "min_text_pt": 8.5}


def _partial_pack(d: Path, rehearsal: str, unresolved: dict[str, str]) -> Path:
    """A copy of the rehearsal's pack config whose ADD-03 op file leaves `unresolved` for a person (their ops removed,
    a disposition `unresolved` with the reason); every other input is the rehearsal's own, read-only."""
    work = ROOT / "rehearsals" / rehearsal / "work"
    am = d / "amendments"
    am.mkdir(parents=True)
    for f in ("ADD-01.yaml", "ADD-02.yaml"):
        shutil.copyfile(work / "amendments" / f, am / f)
    of = yaml.safe_load((work / "amendments" / "ADD-03.yaml").read_text(encoding="utf-8"))
    assert all(any(o["provision"] == p for o in of["ops"]) for p in unresolved), "the provisions must have curated ops"
    of["ops"] = [o for o in of["ops"] if o["provision"] not in unresolved]
    of["dispositions"] += [{"provision": p, "disposition": "unresolved", "reason": why} for p, why in unresolved.items()]
    (am / "ADD-03.yaml").write_text(yaml.safe_dump(of, allow_unicode=True, sort_keys=False), encoding="utf-8")
    cfg = yaml.safe_load((work / "pack.yaml").read_text(encoding="utf-8"))
    cfg["amendments_dir"] = str(am)
    (d / "pack.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
    return d / "pack.yaml"


def _files(d: Path) -> dict[str, bytes]:
    return {p.relative_to(d).as_posix(): p.read_bytes() for p in sorted(d.rglob("*")) if p.is_file()}


def _rows(p: Path) -> dict[str, dict]:
    return {x.get("id") or x.get("activity"): x for x in json.loads(p.read_text(encoding="utf-8"))["rows"]}


@pytest.fixture(scope="module")
def p02(blind02_build, tmp_path_factory):
    """Blind-02's pack with ADD-03 partial; written twice (candidate step off, as before session 11, and on), each from
    its own stage2.run."""
    d = tmp_path_factory.mktemp("s11-partial02")
    pack = _partial_pack(d / "pack", "blind-02", UNRESOLVED_02)
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(stage2, "write_a3_pdf", _fast_a3_pdf)
        off = stage2.write(stage2.run(blind02_build, pack, ROOT), d / "off", candidate=False)
        r = stage2.run(blind02_build, pack, ROOT)
        on = stage2.write(r, d / "on")
    return {"r": r, "pack": pack, "off": d / "off", "on": d / "on", "res_off": off, "res_on": on, "dir": d,
            "cand": json.loads((d / "on" / "a3" / "a3_candidate.json").read_text(encoding="utf-8"))}


@pytest.fixture(scope="module")
def p03(blind03_build, tmp_path_factory):
    """Blind-03's pack with ADD-03 partial: its ops change an image-read Table 2-4 value and an Arabic Form 4-C
    declaration, and its op notes carry 'CONDITION: ...' wording."""
    d = tmp_path_factory.mktemp("s11-partial03")
    pack = _partial_pack(d / "pack", "blind-03", UNRESOLVED_03)
    r = stage2.run(blind03_build, pack, ROOT)
    paths = partial.write(r, d / "out", None, None, op_status={"ADD-03/5.1": "evidence_verified"})
    return {"r": r, "out": d / "out", "paths": paths, "build": blind03_build,
            "cand": json.loads((d / "out" / "a3" / "a3_candidate.json").read_text(encoding="utf-8"))}


# ---------------------------------------------------------------------------------------------- the validated state stays

def test_the_validated_outputs_are_the_same_bytes_with_or_without_the_candidate(p02):
    r = p02["r"]
    assert r["validated"].stage == "ADD-02" and r["working"].stage == "ADD-03" and r["working"].status == "PARTIAL"
    off, on = _files(p02["off"]), _files(p02["on"])
    extra = sorted(set(on) - set(off))
    briefing = ['a3/candidate/a3.json', 'a3/candidate/a3_detail.html']
    if json.loads(on['a3/a3_candidate.json']).get('one_page', {}).get('pages') == 1:
        briefing.append('a3/candidate/a3.pdf')
    assert extra == sorted(["a3/a3_candidate.html", "a3/a3_candidate.json", "a3/a3_candidate.md", "a3/a3_candidate.pdf"]
                           + briefing
                           + [f"a5/candidate/{f}" for f in (
                               "README.md", "blockers.csv", "blockers.json", "changes.csv", "changes.json", "gantt.html",
                               "gantt.pdf", "gantt.svg", "marshalling.csv", "marshalling.json", "milestones.csv",
                               "milestones.json", "programme.csv", "programme.json", "scenarios.csv", "scenarios.json")])
    assert set(off) <= set(on)
    differ = sorted(k for k in off if off[k] != on[k])
    assert differ == ["README.md"], differ                       # A1-A5, checks, stages, review: byte-identical
    a, b = off["README.md"].decode().splitlines(), on["README.md"].decode().splitlines()
    assert [x for x in b if x not in a] == [next(x for x in b if "a3/a3_candidate.pdf" in x)]
    assert p02["res_on"]["candidate"] and not p02["res_off"]["candidate"]
    assert p02["res_on"]["status"] == "ok"


def test_a_failing_candidate_never_blocks_the_validated_outputs(p02, blind02_build, tmp_path):
    def boom(*a, **k):
        raise RuntimeError("boom")
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(stage2, "write_a3_pdf", _fast_a3_pdf)
        mp.setattr(partial, "write", boom)
        res = stage2.write(stage2.run(blind02_build, p02["pack"], ROOT), tmp_path / "out")
    assert res["status"] == "ok" and res["candidate"] == [] and res["candidate_error"] == "RuntimeError: boom"
    files, off = _files(tmp_path / "out"), _files(p02["off"])
    assert all(files[k] == off[k] for k in off if k != "README.md")
    assert "NOT PRODUCED (RuntimeError: boom)" in files["README.md"].decode()
    assert files["a3/a3_candidate_FAILED.md"].decode().endswith("RuntimeError: boom\n")


def test_the_validated_a3_and_a5_are_the_add02_state(p02, blind02_run):
    on = p02["on"]
    a3 = json.loads((on / "a3" / "a3.json").read_text(encoding="utf-8"))
    # session 12 (F2, audit A3-3): 'Validated state' reads 'State after' on the page (plain words)
    assert a3["subtitle"].startswith("State after ADD-02") and "Working state ADD-03 is PARTIAL and NOT used" in a3["subtitle"]
    assert "ADD-03-6.8-01" not in a3["explicit_ids"] and "ADD-03-Q20-01" not in a3["explicit_ids"]
    prog = json.loads((on / "a5" / "programme.json").read_text(encoding="utf-8"))
    assert prog["stage"] == "ADD-02" and prog["status_date"] == "2026-10-22"
    # the same ADD-02 stage from the curated blind-02 pack (every addendum up to ADD-02 validated there too): the same
    # A5 activities and the same A3 rows
    ref = blind02_run
    want = programme.stage_planner(ref, "ADD-02")(ref["assumptions"])
    cols = programme.PROGRAMME_COLS
    assert prog["rows"] == [{k: a.get(k) for k in cols} for a in want["activities"]]
    st = next(s for s in ref["stages"] if s.stage == "ADD-02")
    view = dict(ref, validated=st, working=None)
    ref_a3 = stage2.a3(view, stage2.collect_issues(view, want), want)
    for k in ("explicit_ids", "none_stated_ids"):
        assert a3[k] == ref_a3[k], k
    assert [(x["id"], x["cls"], x["consequence"]) for x in a3["explicit"]] == \
        [(x["id"], x["cls"], x["consequence"]) for x in ref_a3["explicit"]]


def test_the_real_pack_has_no_partial_addendum_and_no_candidate_files(pack, tmp_path):
    r = stage2.run(pack["out"], ROOT / "config/pack.yaml", ROOT)
    assert r["working"] is None and partial.compute(r) is None
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(stage2, "write_a3_pdf", _fast_a3_pdf)
        res = stage2.write(r, tmp_path / "out")
    files = _files(tmp_path / "out")
    assert res["candidate"] == [] and not [f for f in files if "candidate" in f]
    assert b"CANDIDATE" not in files["README.md"]


# ---------------------------------------------------------------------------------------------- the candidate A3

def test_the_candidate_a3_lists_the_rows_the_valid_ops_bring_in_with_their_ops(p02):
    c = p02["cand"]
    assert c["banner"] == "CANDIDATE — NOT VALIDATED" and c["validated_stage"] == "ADD-02" and c["stage"] == "ADD-03"
    ch = {x["row"]: x for x in c["changes"]}
    for rid, op in (("ADD-03-6.8-01", "ADD-03/2.4"), ("ADD-03-Q20-01", "ADD-03/Q20")):
        assert ch[rid]["change"] == "enters", rid
        o = next(o for o in ch[rid]["ops"] if o["op"] == op)
        assert o["applied"] and o["valid"] and o["review"] == "proposed" and "applied in the candidate" in o["label"]
    assert ch["ADD-03-6.8-01"]["what"][0].startswith("explicit (rejection)")
    assert ch["VOL-I-10.3-02"]["change"] == "leaves" and [o["op"] for o in ch["VOL-I-10.3-02"]["ops"]] == ["ADD-03/4.1"]
    # a row re-read against an unresolved provision is shown, but as not settled
    assert any(y.startswith("NOT SETTLED: ADD-03:3.2 UNRESOLVED") for y in ch["VOL-I-6.3-01"]["why"])
    # the ops of the unresolved provisions are nowhere in the candidate
    ops = {o["op"] for o in c["ops"]}
    assert "ADD-03/2.4" in ops and not {o for o in ops if o.startswith(("ADD-03/3.2", "ADD-03/5.3"))}
    a3c = c["a3"]
    assert a3c["subtitle"].startswith("Candidate state ADD-03 (NOT validated: the validated state is ADD-02)")
    assert {"ADD-03-6.8-01", "ADD-03-Q20-01"} <= set(a3c["explicit_ids"])


def test_the_candidate_a3_blockers(p02):
    b = p02["cand"]["blockers"]
    prov = {x["provision"]: x for x in b["provisions"]}
    assert prov["ADD-03:3.2"]["reason"] == UNRESOLVED_02["ADD-03:3.2"] and prov["ADD-03:3.2"]["rows"] == ["VOL-I-6.3-01"]
    assert prov["ADD-03:3.2"]["activities"] == ["bond-approval", "bond-issue"]
    assert prov["ADD-03:5.3"]["kind"] == "escalated" and prov["ADD-03:5.3"]["rows"] == ["VOL-II-8.4-01", "VOL-II-8.4-02"]
    assert {x["row"] for x in b["unresolved_rows"]} >= {"VOL-I-6.3-01", "VOL-II-8.4-01", "VOL-II-8.4-02"}
    # the missing Environmental Permit stays visible, as the relationships file records it and as the open issue
    md = {x["id"]: x for x in b["missing_documents"]}
    assert "I-PERMIT" in md and md["I-AUTO-NOT-SUPPLIED-ENVIRONMENTAL-PERMIT"]["document"] == \
        "the Environmental Permit issued for the site"
    assert any("C28" in x["source"] for x in b["conflicts"])
    text = (p02["on"] / "a3" / "a3_candidate.md").read_text(encoding="utf-8")
    for w in ("**ADD-03:3.2**", "**ADD-03:5.3**", "I-PERMIT", "I-VOL-II-T24-TENSIONS", "the Environmental Permit issued "
              "for the site", "NOT VALIDATED", "## What may be changing"):
        assert w in text, w
    assert "I-VOL-II-T24-TENSIONS" in {i["id"] for g in p02["cand"]["a3"]["groups"]["groups"] for i in g["items"]}


def test_the_candidate_a3_pdf_says_how_many_pages_and_is_deterministic(p02, tmp_path):
    pdf = pymupdf.open(p02["on"] / "a3" / "a3_candidate.pdf")
    n = pdf.page_count
    assert n > 1 and p02["cand"]["pages"] == n
    first, last = pdf[0].get_text(), pdf[-1].get_text()
    assert "NOT VALIDATED" in first and f"runs to {n} pages" in " ".join(first.split())
    assert f"page {n} of {n}" in last and "the validated A3 is a3.pdf" in last
    assert "C43 applies to the validated A3 only" in " ".join(first.split())
    c = partial.compute(p02["r"])
    write_candidate_a3_pdf(c, tmp_path / "a.pdf")
    write_candidate_a3_pdf(c, tmp_path / "b.pdf")
    assert (tmp_path / "a.pdf").read_bytes() == (tmp_path / "b.pdf").read_bytes()


def test_controller_statuses_are_shown_beside_the_ops(p02):
    c = partial.compute(p02["r"], op_status={"ADD-03/2.4": "evidence_verified"})
    o = next(o for x in c["changes"] if x["row"] == "ADD-03-6.8-01" for o in x["ops"] if o["op"] == "ADD-03/2.4")
    assert o["controller"] == "evidence_verified" and "controller evidence_verified" in o["label"]


# ---------------------------------------------------------------------------------------------- the candidate A5

def test_the_candidate_a5_moves_the_dates_the_ops_move_and_flags_the_blocked(p02):
    on = p02["on"]
    cp = _rows(on / "a5" / "candidate" / "programme.json")
    rr = cp["register-reps"]
    assert (rr["latest_start_validated"], rr["latest_start"]) == ("2026-11-25", "2026-11-19")
    assert rr["candidate_status"] == "MOVED" and rr["caused_by_rows"] == ["ADD-03-6.8-01"] and rr["caused_by_ops"] == ["ADD-03/2.4"]
    for a, row in (("bond-issue", "VOL-I-6.3-01"), ("bond-approval", "VOL-I-6.3-01"),
                   ("technical-proposal", "VOL-II-8.4-01")):
        assert cp[a]["candidate_status"] == "BLOCKED", a
        assert any(x.startswith(f"{row}: ADD-03:") for x in cp[a]["blocked"]), cp[a]["blocked"]
    meta = json.loads((on / "a5" / "candidate" / "programme.json").read_text(encoding="utf-8"))
    assert meta["status_date"] == "2026-11-03" and meta["validated_status_date"] == "2026-10-22"
    assert meta["notice"].startswith("CANDIDATE — NOT VALIDATED")
    assert {x["activity"] for x in json.loads((on / "a5" / "candidate" / "blockers.json").read_text())["rows"]} >= \
        {"bond-issue", "bond-approval", "technical-proposal", "simulation-report"}
    assert "REVIEW" in {a["candidate_status"] for a in cp.values()}             # reached through relationships
    readme = (on / "a5" / "candidate" / "README.md").read_text(encoding="utf-8")
    assert "| register-reps | 2026-11-25 -> 2026-11-19 |" in readme and "ADD-03/2.4" in readme
    assert "CANDIDATE — NOT VALIDATED" in (on / "a5" / "candidate" / "gantt.html").read_text(encoding="utf-8")
    # the validated A5 is untouched
    assert _rows(on / "a5" / "programme.json")["register-reps"]["latest_start"] == "2026-11-25"


def test_conditional_information_in_the_op_file_becomes_a_decision_milestone(p02):
    sc = {x["provision"]: x for x in p02["cand"]["scenarios"]}
    x = sc["ADD-03:5.3"]
    assert (x["kind"], x["what"], x["trigger_deadline"], x["applied"]) == ("conditional", "amendment", "2026-11-12", False)
    assert x["rows"] == ["VOL-II-8.4-01", "VOL-II-8.4-02"] and "text only" in x["model"]
    ms = _rows(p02["on"] / "a5" / "candidate" / "milestones.json")
    m = ms["DECISION-ADD-03:5.3"]
    assert m["date"] == "2026-11-12" and m["conditional"] and "technical-proposal" in m["activities"]
    assert "DECISION-ADD-03:5.3" not in _rows(p02["on"] / "a5" / "milestones.json")      # never in the validated A5
    assert "decision by 2026-11-12" in p02["cand"]["paragraph"]


def test_a_modelled_conditional_amendment_is_a_scenario_with_its_decision_date(pack):
    """The engine's conditional model (amend.Condition; tests/test_session11_conditional.py builds blind-04's Section 7
    from the addendum's words over the real pack): with one more provision left unresolved the stage is PARTIAL, and the
    candidate's scenario carries the condition, its state (pending: nothing assumed), the trigger deadline the register
    computes (Thu 12 Nov 2026), both states and the rows it reaches."""
    T = pytest.importorskip("test_session11_conditional")
    from tenderpack.amend import Disposition, Engine, OpFile, load_opfile, validated_stage
    from tenderpack.dates import Calendar
    from tenderpack.register import Register, load_rows
    units = pack["units"] + [T.add03_unit("ADD-03:cover/para1", "Issued 9 November 2026", kind="paragraph"),
                             T.add03_unit("ADD-03:7.1", T.SEVEN_ONE, page=2, label="7.1"),
                             T.add03_unit("ADD-03:7.2", T.SEVEN_TWO, page=2, label="7.2"),
                             T.add03_unit("ADD-03:8.1", "Form 4-H is added to Volume IV (test unit).", page=2, label="8.1")]
    earlier = [load_opfile(ROOT / "curation/amendments" / f"{a}.yaml") for a in ("ADD-01", "ADD-02")]
    f = OpFile(addendum="ADD-03", issued_from="ADD-03:cover/para1", prepared_by="test", method="test", ops=[T.seven()],
               dispositions=[T.COVER, Disposition(provision="ADD-03:8.1", disposition="unresolved", reason="test")])
    stages = Engine(units, earlier + [f]).run()
    assert stages[-1].status == "PARTIAL" and validated_stage(stages).stage == "ADD-02"
    reg = Register(load_rows(ROOT / "curation/register/rows.yaml"), stages, Calendar())
    r = {"stages": stages, "validated": validated_stage(stages), "working": stages[-1], "evals": reg.all()}
    (s,) = partial.modelled_conditions(r)
    assert (s["kind"], s["what"], s["op"], s["condition"], s["state"], s["applied"]) == \
        ("conditional", "amendment", "ADD-03/7.2(a)", "ADD-03/S7", "pending", False)
    assert s["trigger_deadline"] == "2026-11-12" and "VOL-II-1.4-01" in s["rows"]
    assert s["if_triggered"].startswith("VOL-II:1.4: “") and "nothing assumed" in s["model"]
    assert s["if_not_triggered"] == "If no such notice is given by that time, this Section 7 lapses."


def _replay04(run: Path, edit=None):
    """Blind-04's frozen candidate (rehearsals/blind-04/candidate-curation/, read only) replayed in a disposable candidate
    workspace under `run`; `edit(opfile_dict)` may change the copied op file first. Returns (paths, stage2 run)."""
    from tenderpack.ai import candidate as CAND
    from tenderpack.cli import ingest
    b4 = ROOT / "rehearsals" / "blind-04"
    CAND.create(run, ROOT / "config/pack.yaml", "ADD-03", b4 / "input/ADD-03_Addendum_No_3.pdf", "s11-blind04-replay")
    P = CAND.paths(run)
    cfg = yaml.safe_load(P["pack"].read_text(encoding="utf-8"))
    where = lambda k: Path(cfg[k]) if Path(cfg[k]).is_absolute() else ROOT / cfg[k]  # noqa: E731
    of = yaml.safe_load((b4 / "candidate-curation/amendments/ADD-03.yaml").read_text(encoding="utf-8"))
    if edit:
        edit(of)
    (where("amendments_dir") / "ADD-03.yaml").write_text(yaml.safe_dump(of, allow_unicode=True, sort_keys=False),
                                                         encoding="utf-8")
    shutil.copyfile(b4 / "candidate-curation/readings/ADD-03-p4-r1.yaml", where("readings_dir") / "ADD-03-p4-r1.yaml")
    shutil.copyfile(b4 / "candidate-curation/activity_templates.yaml", where("activity_templates"))
    shutil.copyfile(b4 / "candidate-curation/clarifications/register.yaml", where("clarifications"))
    shutil.copyfile(b4 / "candidate-curation/relationships.yaml", where("register").parent.parent / "relationships.yaml")
    assert ROOT / "rehearsals" not in P["build"].parents
    assert ingest(P["pack"], P["build"], ROOT, quiet=True)["exit_code"] == 0
    return P, stage2.run(P["build"], P["pack"], ROOT)


def test_blind04_frozen_partial_candidate_now_says_what_may_be_changing(tmp_path_factory):
    """Blind rehearsal 04 as post-key regression material, read only: its frozen, scored candidate (the op file with 24
    provisions unresolved, the pending Form 4-H reading, the relationships, templates and clarification register under
    rehearsals/blind-04/candidate-curation/) replayed in a disposable candidate workspace over the real pack. The frozen
    review packet could only say 'A3 and the A5 programme show the validated state (ADD-02)'; the candidate now lists
    the blockers, the Section 7 decision by Thu 12 Nov 2026 and the 8 Oct 2026 effective date (answer key IE5, A6), and
    keeps the Form 4-H reading beside its packet."""
    b4 = ROOT / "rehearsals" / "blind-04"
    P, r = _replay04(tmp_path_factory.mktemp("s11-blind04") / "run")
    assert (r["validated"].stage, r["working"].stage, r["working"].status) == ("ADD-02", "ADD-03", "PARTIAL")
    c = partial.compute(r)
    frozen = (b4 / "review" / "index.md").read_text(encoding="utf-8")
    unres = [a or b for a, b in re.findall(r"^- \*\*UNRESOLVED (\S+)\*\*|^- \*\*ESCALATED \S+\*\* \((\S+)\)", frozen, re.M)]
    assert len(unres) == 24 and sorted(unres) == sorted(x["provision"] for x in c["blockers"]["provisions"])
    sc = {x["provision"]: x for x in c["scenarios"]}
    assert (sc["ADD-03:7.1"]["kind"], sc["ADD-03:7.1"]["what"], sc["ADD-03:7.1"]["trigger_deadline"]) == \
        ("conditional", "amendment", "2026-11-12")
    assert sc["ADD-03:7.2"]["trigger_deadline"] == "2026-11-12" and not sc["ADD-03:7.2"]["applied"]
    assert (sc["ADD-03:5.2"]["kind"], sc["ADD-03:5.2"]["effective_from"]) == ("effective-dated", "2026-10-08")
    ms = {m["id"]: m for m in c["a5"]["milestones"]}
    assert ms["DECISION-ADD-03:7.1"]["date"] == "2026-11-12" and ms["EFFECTIVE-ADD-03:5.2"]["date"] == "2026-10-08"
    img = {g["region"]: g for g in c["images"]}["ADD-03-p4-r1"]
    assert img["touched"] and img["status"] == "pending" and (P["build"] / img["packet"]).is_file()
    ar = [u for u in img["units"] if re.search("[؀-ۿ]", u["text"])]
    assert ar and all(not re.search("[؀-ۿ]", u["translation"]) for u in ar if u["translation"])
    assert c["blockers"]["c46"] and c["blockers"]["blocked_activities"]
    assert "I-PERMIT" in {x["id"] for x in c["blockers"]["missing_documents"]}
    assert "decision by 2026-11-12" in c["paragraph"] and "stay validated at ADD-02" in c["paragraph"]


def test_a_held_conditional_op_is_labelled_conditional_never_rejected(tmp_path_factory):
    """Blind-04's Section 7 written as the engine's conditional op (tests/test_session11_conditional.py: amend.Condition)
    in place of the frozen file's two unresolved dispositions: the op is held, not rejected, and every label (A2's op
    table, the diff, the candidate) says CONDITIONAL with the decision date and both states."""
    T = pytest.importorskip("test_session11_conditional")

    def edit(of):
        of["dispositions"] = [d for d in of["dispositions"] if d["provision"] not in ("ADD-03:7.1", "ADD-03:7.2")]
        of["ops"].append(T.seven().model_dump(mode="json", exclude_none=True))
    P, r = _replay04(tmp_path_factory.mktemp("s11-blind04-cond") / "run", edit)
    x = next(x for s in r["stages"] for x in s.ops if x.op.id == "ADD-03/7.2(a)")
    assert x.valid and x.conditional_pending and not x.applied and not x.withdrawn
    lab = partial.op_info(r, x)["label"]
    assert "CONDITIONAL (pending): not in effect unless" in lab and "decide by 2026-11-12" in lab, lab
    assert "WITHHELD" not in lab and "VOL-II:1.4: “" in lab
    row = next(ln for ln in stage2.a2(r)["markdown"].splitlines() if ln.startswith("| ADD-03/7.2(a) |"))
    assert "CONDITIONAL (pending)" in row and "decide by 2026-11-12" in row and "WITHHELD" not in row
    md, _ = live.diff(r, "ADD-02", "ADD-03")
    assert "- CONDITIONAL ADD-03/7.2(a):" in md and "WITHHELD ADD-03/7.2(a)" not in md
    s = next(s for s in partial.compute(r)["scenarios"] if s["op"] == "ADD-03/7.2(a)")
    assert (s["state"], s["trigger_deadline"], s["applied"]) == ("pending", "2026-11-12", False)


def test_relationship_chains_that_are_blocked_or_incomplete_are_candidate_blockers(p03):
    """The trace records carry completeness and blockers: a chain reached through Table 2-4 that the missing
    Environmental Permit blocks is named as blocked, with the document, in the candidate's Blockers."""
    ch = p03["cand"]["blockers"]["chains"]
    hit = [x for x in ch if any(b["document"] == "the Environmental Permit issued for the site" for b in x["blockers"])]
    assert hit and all(x["completeness"] in ("complete", "truncated", "cyclic") for x in ch)
    md = (p03["out"] / "a3" / "a3_candidate.md").read_text(encoding="utf-8")
    assert "### Relationship chains blocked or incomplete" in md
    assert f"BLOCKED: the Environmental Permit issued for the site" in md
    permit = next(m for m in p03["cand"]["blockers"]["missing_documents"] if m["id"] == "I-AUTO-NOT-SUPPLIED-ENVIRONMENTAL-PERMIT")
    assert set(x["target"] for x in hit) <= set(permit["reached_by_this_addendum"])


# ---------------------------------------------------------------------------------------------- the diff and the packet

def test_the_diff_points_to_both_and_says_what_may_be_changing(p02):
    md, data = live.diff(p02["r"], "ADD-02", "ADD-03")
    assert "### Validated vs candidate (partial should not mean useless)" in md
    assert "`<outputs>/a3/a3_candidate.pdf`" in md and "`<outputs>/a3/a3.pdf` (one page)" in md
    para = md.split("**What may be changing.** ", 1)[1].split("\n", 1)[0]
    assert para == p02["cand"]["paragraph"]
    assert "ADD-03-6.8-01 (ADD-03/2.4)" in para and "register-reps" in para and "stay validated at ADD-02" in para
    assert {"ADD-03-6.8-01", "ADD-03-Q20-01"} <= set(data["candidate"]["a3"]["enters"])
    assert "bond-issue" in data["candidate"]["blocked_activities"]
    md_v, data_v = live.diff(p02["r"], "ADD-01", "ADD-02")                      # a validated stage: no paragraph
    assert "Validated vs candidate" not in md_v and "candidate" not in data_v


def test_image_read_units_touched_keep_crops_arabic_translations_tables_units_and_notes(p03):
    c = p03["cand"]
    g = {x["region"]: x for x in c["images"]}
    t24 = {u["unit"]: u for u in g["VOL-II-p3-r1"]["units"]}
    tp = t24["VOL-II:T2-4/TP"]
    assert tp["cells"]["Limit"] == "1" and tp["candidate"]["cells"]["Limit"] == "0.5"     # read value kept apart
    assert tp["measure"] == "mg/l" and "changed by ADD-03/5.1" in tp["touched"]
    assert "all values are maxima" in tp["table"]["qualifier"] and tp["table"]["column_headings"]
    assert {"I-PERMIT", "I-READING-T24"} <= set(tp["issues"])
    assert g["VOL-II-p3-r1"]["uncertainties"] and g["VOL-II-p3-r1"]["packet"] == "review/VOL-II-p3-r1/packet.html"
    assert (p03["build"] / g["VOL-II-p3-r1"]["packet"]).is_file()
    f4c = {u["unit"]: u for u in g["VOL-IV-p6-r1"]["units"]}
    d4 = f4c["VOL-IV:F4-C/image/decl4"]
    assert re.search("[؀-ۿ]", d4["text"]) and not re.search("[؀-ۿ]", d4["translation"])
    assert d4["candidate"]["status"] == "deleted" and d4["crops"]
    # the maxima/range ambiguity stays open and visible; the Permit stays visible
    assert "I-VOL-II-T24-TENSIONS" in {x["id"] for x in c["open_issues_in_play"]}
    assert "I-PERMIT" in {x["id"] for x in c["blockers"]["missing_documents"]}
    # a conditional obligation in an op note ('CONDITION: ...') with the earliest deadline printed
    s = next(x for x in c["scenarios"] if x["op"] == "ADD-03/3.2")
    assert (s["what"], s["trigger_deadline"], s["applied"]) == ("obligation", "2026-11-19", True)
    # the AI review packet's section: validated vs candidate, the paragraph, the packets beside the units
    lines = "\n".join(partial.review_lines(p03["out"], p03["build"], lambda p: Path(p).as_posix(),
                                           {"ADD-03/5.1": "evidence_verified"}))
    assert "**Validated** (unchanged; ADD-02)" in lines and "**Candidate** (CANDIDATE — NOT VALIDATED; ADD-03" in lines
    assert f"[packet]({(p03['build'] / 'review/VOL-IV-p6-r1/packet.html').as_posix()})" in lines
    assert d4["text"][:40] in lines and "translation (apart)" in lines and "unit mg/l" in lines
    assert "**What may be changing.** " + c["paragraph"] in lines
