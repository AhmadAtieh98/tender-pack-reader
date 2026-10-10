"""Session 11, D1: the downstream workflow finished properly (the owner's section 1), each finding reproduced first.

A  Requirement introduction is explicit and evidenced. Blind rehearsal 04's post-key build was refused at pre-flight:
   the AI's new row cited only a BASE unit with a reading at ADD-03, so the register held it in force from BASE with no
   reading there (C16). Rebuilt here on the real pack with blind-02's Addendum No. 3: a new row citing VOL-I 6.3 only
   is refused at validation with the reason unless it carries `introduced: {stage, by, evidence}`; with it, the row is
   NOT IN FORCE before ADD-03, NEW at ADD-03, and the candidate passes pre-flight.
B  Rows are found and updated by id through the YAML structure: a row the downstream serializer wrote (its own file,
   `rows:` items at column 0) is updated by a later reading; a curated file keeps its comments; ids never duplicate.
C  Completion: a run whose downstream batch failed, whose tasks are unanswered and whose candidate check-register has
   C46 findings is `partial` with those reasons, not `complete`; execution, completeness and approval are kept apart.
D  The state identity covers the register, relationships and other curated inputs; a change between validation and
   promotion makes the combined set stale and promotion refuses.
F  A recorded end-to-end run whose downstream items carry new rows (with introduction evidence), re-made readings, an
   issue, an evidence item, an activity, a re-read clarification entry and `no_change` answers reaches a candidate whose
   check-register is clean and whose outputs publish the new rows on A1 and the activity on A5.

The addendum is the first page of blind-02's Addendum No. 3 (cover and Sections 1-3; the rest cut away here, into a
disposable folder) added to the real pack. The cassettes are hand-written recorded fixtures (no live call is made and
none is implied). Nothing is written under the repository; the preceding evidence build is ingested into tmp."""
from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path

import pymupdf
import pytest
import yaml

from ai_fixture import CASSETTES, ROOT
from tenderpack.ai import downstream as DS
from tenderpack.ai import workflow as W
from tenderpack.ai.contract import DownstreamItem, DownstreamSet, EvidenceRef

PDF = ROOT / "rehearsals/blind-02/input/ADD-03_Addendum_No_3.pdf"
CASSETTE = CASSETTES / "s11_downstream_add03.yaml"
quiet = lambda *a, **k: None  # noqa: E731


def short_addendum(out: Path) -> Path:
    """Page 1 of blind-02's Addendum No. 3 up to the end of Section 3 (Section 4 onwards and pages 2-4 removed): 12
    provisions."""
    doc = pymupdf.open(PDF)
    pg = doc[0]
    pg.add_redact_annot(pymupdf.Rect(0, 668, pg.rect.width, 796))
    pg.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)
    doc.delete_pages(1, doc.page_count - 1)
    doc.save(out)
    return out


NO_EFFECT_22 = ('{"id": "ADD-03/2.2", "state": ${state}, "statement_type": "disposition", "provision": "ADD-03:2.2", '
                '"payload": {"provision": "ADD-03:2.2", "disposition": "no_effect", "reason": "\u2018The time of 14:00 Riyadh '
                'time is unchanged.\u2019 ceases to have effect: that sentence of ADD-01 2.1 only stated that the time was '
                'unchanged; ADD-03 2.1 itself changes the time, so no text in force changes"}, '
                '"evidence": [{"doc": "ADD-03", "unit_id": "ADD-03:2.2", "page": 1, "kind": "span", '
                '"words": "(\u2018The time of 14:00 Riyadh time is unchanged.\u2019) ceases to have effect"}]},\n              ')


@pytest.fixture(scope="module")
def prev_build(tmp_path_factory):
    """The preceding state's evidence build (the real pack as received), ingested into a disposable folder."""
    from tenderpack.cli import ingest
    out = tmp_path_factory.mktemp("s11d-prev") / "build"
    assert ingest(ROOT / "config/pack.yaml", out, ROOT, quiet=True)["exit_code"] == 0
    return out


@pytest.fixture(scope="module")
def area(tmp_path_factory):
    d = tmp_path_factory.mktemp("s11d")
    data = yaml.safe_load(CASSETTE.read_text(encoding="utf-8"))
    # for C: the same analysis with no downstream session, and 2.2 answered by a no_effect disposition (promotable,
    # interpretation_pending: the sentence it ends only said the time was unchanged), so every provision is answered
    analysis_only = dict(data, sessions=[s for s in data["sessions"] if s["phase"] == "analysis"])
    for s in analysis_only["sessions"]:
        turn = s["turns"][-1]["response"]
        turn["text"] = re.sub(r'\{"id": "ADD-03/2\.2".*?(?=\{"id": "ADD-03/2\.3")', NO_EFFECT_22, turn["text"], flags=re.S)
    (d / "analysis-only.yaml").write_text(yaml.safe_dump(analysis_only, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return {"staging": d / "staging", "worklog": d / "worklog", "pdf": short_addendum(d / "ADD-03_page1.pdf"),
            "analysis_only": d / "analysis-only.yaml"}


def _start(prev_build, area, run_id, cassette=CASSETTE, **kw):
    kw.setdefault("background_before", False)
    # one downstream batch (the cassette answers the whole downstream phase in one session): the batch size and the
    # output cap the request layer sizes a batch against are set for it
    kw.setdefault("caps", {"max_tokens_per_call": 120000})
    return W.start("ADD-03", area["pdf"], pack=ROOT / "config/pack.yaml", evidence=prev_build, staging=area["staging"],
                   worklog=area["worklog"], run_id=run_id, batch_size=8, downstream_batch_size=60, route="recorded",
                   cassette=cassette, echo=quiet, sleep=lambda s: None, **kw)


def _stopped(prev_build, area, run_id, stop="validation", cassette=CASSETTE) -> W.Ctx:
    res = _start(prev_build, area, run_id, cassette=cassette, stop_after=stop)
    assert res["status"] == "stopped" and f"stopped after {stop}" in res["status_reason"], res
    return W.Ctx(W.load(run_id, area["staging"]), quiet)


def _yaml(p: Path):
    return yaml.safe_load(Path(p).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------------------------- A: introduction

BOND_ROW = {"id": "ADD-03-3.2-01", "group": "ADD-03:3.2", "scope": ["envelope_A", "bid_security", "validity", "new_in_addendum"],
            "requirement": "Bid Bond valid for 210 days from the Proposal Due Date", "units": ["VOL-I:6.3"],
            "discipline": "Commercial", "owner": "Commercial lead", "assessment": "pass_fail", "evidence": ["EV-BID-BOND"],
            "interpretations": [{"stage": "ADD-03", "parameters": {"validity_days": 210},
                                 "quote": "remain valid for two hundred and ten (210) days from the Proposal Due Date"}],
            "confidence": "medium", "confidence_reason": "verbatim as amended by ADD-03 3.2", "issues": ["I-NO-CONSEQUENCE"]}
BOND_INTRO = {"stage": "ADD-03", "by": "ADD-03/3.2",
              "evidence": {"unit": "ADD-03:3.2", "page": 1, "words": "‘two hundred and ten (210) days’ is substituted"}}
BOND_EV = EvidenceRef(doc="ADD-03", unit_id="ADD-03:3.2", page=1, kind="span",
                      words="‘two hundred and ten (210) days’ is substituted")


def _one_row_set(ws, row) -> DownstreamSet:
    st = ws.identity()
    it = DownstreamItem(id="D1", state=st, statement_type="row_new", task="t:bond", provision="ADD-03:3.2",
                        payload={"row": row}, evidence=[BOND_EV])
    return DownstreamSet(run_id="s11-a", created="2026-10-04T00:00:00Z", route="recorded", provider="test",
                         model_requested="test", addendum="ADD-03", state=st, items=[it])


def test_a_a_new_row_citing_a_base_unit_needs_its_introduction_evidence(prev_build, area):
    from tenderpack import stage2
    from tenderpack.ai import candidate as CAND
    ctx = _stopped(prev_build, area, "a-intro")
    ws = ctx.ws
    cps, _ = ctx.combined()
    promoted = ctx.promoted(fresh=True)
    # the blind-04 shape: a row an addendum creates, citing only a unit issued in BASE, read at the addendum only
    ds = _one_row_set(ws, BOND_ROW)
    DS.validate(ws, ds, promoted, {"t:bond": "row_new"})
    it = ds.items[0]
    assert it.verification_status not in DS.PROMOTABLE, (it.verification_status, [v.detail for v in it.validation])
    why = " | ".join(v.detail for v in it.validation if not v.ok)
    assert "would be in force from BASE" in why and "introduced" in why, why
    assert "BASE: no interpretation made at or before BASE" in why          # checked at every stage, not only ADD-03
    # with the introduction evidence the same row is promotable, NOT IN FORCE before ADD-03 and NEW at it
    ds = _one_row_set(ws, dict(BOND_ROW, introduced=BOND_INTRO))
    rep = DS.validate(ws, ds, promoted, {"t:bond": "row_new"})
    it = ds.items[0]
    assert it.verification_status == "interpretation_pending", [v.detail for v in it.validation if not v.ok]
    assert rep["stages"]["ADD-03-3.2-01"] == {
        "BASE": "NOT IN FORCE (introduced at ADD-03 by ADD-03/3.2)", "ADD-01": "NOT IN FORCE (introduced at ADD-03 by ADD-03/3.2)",
        "ADD-02": "NOT IN FORCE (introduced at ADD-03 by ADD-03/3.2)", "ADD-03": "NEW (introduced by ADD-03/3.2)"}
    assert rep["introduction"]["ADD-03-3.2-01"]["explicit"]
    # an introduction the pack does not support is refused with the reason (and the row is then read without it)
    for bad, words in ((dict(BOND_INTRO, by="ADD-03/9.9"), "no op of the amendment path"),
                       (dict(BOND_INTRO, evidence={"unit": "VOL-I:6.3", "page": 3, "words": "shall be extended on demand"}),
                        "already in VOL-I:6.3 at ADD-02")):
        ds = _one_row_set(ws, dict(BOND_ROW, introduced=bad))
        DS.validate(ws, ds, promoted, {"t:bond": "row_new"})
        assert ds.items[0].verification_status not in DS.PROMOTABLE
        assert any(words in v.detail for v in ds.items[0].validation if not v.ok), words
    # promoted into the candidate, the evidenced row passes pre-flight ...
    cand = ctx.cp.data["candidate"]
    forced = _one_row_set(ws, BOND_ROW)                            # (made now: promotion changes the candidate's inputs)
    forced.items[0].verification_status = "interpretation_pending"
    ds = _one_row_set(ws, dict(BOND_ROW, introduced=BOND_INTRO))
    DS.validate(ws, ds, promoted, {"t:bond": "row_new"})
    DS.promote(ws, cand, "a-intro", cps, promoted, ds, "test", {})
    r = stage2.run(Path(cand["build"]), Path(cand["pack"]), ROOT)
    assert CAND.preflight(r) == [], CAND.preflight(r)
    ev = next(e for e in r["evals"] if e["row"].id == "ADD-03-3.2-01")["stages"]
    assert ev["BASE"]["status"].startswith("NOT IN FORCE") and not ev["BASE"]["active"] and ev["BASE"]["problems"] == []
    assert ev["ADD-03"]["status"] == "NEW (introduced by ADD-03/3.2)" and ev["ADD-03"]["problems"] == []
    # ... and the row without it, forced through, is what blind-04 hit: refused at pre-flight (C16 at BASE)
    DS.promote(ws, cand, "a-intro", cps, promoted, forced, "test", {})
    pf = CAND.preflight(stage2.run(Path(cand["build"]), Path(cand["pack"]), ROOT))
    assert [x["id"] for x in pf] == ["C16"] and "ADD-03-3.2-01@BASE: no interpretation made at or before BASE" in pf[0]["detail"]


# ---------------------------------------------------------------------------------------------- B: rows by id

def test_b_a_row_the_downstream_serializer_wrote_is_updated_by_id(prev_build, area):
    from tenderpack.register import load_rows
    ctx = _stopped(prev_build, area, "b-rows")
    ws = ctx.ws
    cps, _ = ctx.combined()
    promoted = ctx.promoted(fresh=True)
    cand = ctx.cp.data["candidate"]
    rows_path = Path(_yaml(cand["pack"])["register"])
    row68 = next(i["payload"]["row"] for i in json.loads(CASSETTE_DOWNSTREAM())["items"]
                 if i["statement_type"] == "row_new" and i["payload"]["row"]["id"] == "ADD-03-6.8-01")
    st = ws.identity()

    def one(kind, payload, task="t:x"):
        it = DownstreamItem(id="D1", state=st, statement_type=kind, task=task, payload=payload,
                            evidence=[BOND_EV], verification_status="interpretation_pending")
        return DownstreamSet(run_id="s11-b", created="x", route="recorded", provider="test", model_requested="test",
                             addendum="ADD-03", state=st, items=[it])
    # 1. the downstream serializer writes a new row in a row file of its own
    s1 = DS.promote(ws, cand, "b-rows", cps, promoted, one("row_new", {"row": row68}), "test", {})
    ai_file = rows_path.parent / "rows/ADD-03-ai.yaml"
    assert s1["rows_new"] == ["ADD-03-6.8-01"] and ai_file.is_file()
    assert "\n- id: ADD-03-6.8-01\n" in ai_file.read_text(encoding="utf-8")      # PyYAML's layout, not the curated one
    shutil.rmtree(Path(cand["dir"]) / ".pre-promotion")         # that file is now part of the state a later run starts from
    # 2. a later addendum's reading of that row (stage ADD-04 here: promote writes what validation passed)
    later = {"stage": "ADD-04", "quote": "register through the Portal the names and identity document numbers",
             "note": "re-read at a later addendum"}
    s2 = DS.promote(ws, cand, "b-rows", cps, promoted, one("row_reading", {
        "row": "ADD-03-6.8-01", "interpretation": later,
        "replace_requirement": {"old": row68["requirement"], "new": "Register up to two delivery representatives"}}),
        "test", {})
    assert s2["readings"] == ["ADD-03-6.8-01"], s2["notes"]
    data = _yaml(ai_file)
    row = next(x for x in data["rows"] if x["id"] == "ADD-03-6.8-01")
    assert [i["stage"] for i in row["interpretations"]] == ["ADD-03", "ADD-04"]
    assert row["requirement"] == "Register up to two delivery representatives"
    assert ai_file.read_text(encoding="utf-8").startswith("# CANDIDATE rows written by AI workflow run b-rows")
    rf = load_rows(rows_path)                                   # the register loads, and the id is there once
    assert [x.id for x in rf.rows].count("ADD-03-6.8-01") == 1


def test_b_a_curated_row_file_keeps_its_comments_and_no_row_id_is_duplicated(prev_build, area):
    from tenderpack.register import load_rows
    ctx = _stopped(prev_build, area, "b-curated")
    ws = ctx.ws
    cps, _ = ctx.combined()
    promoted = ctx.promoted(fresh=True)
    cand = ctx.cp.data["candidate"]
    rows_path = Path(_yaml(cand["pack"])["register"])
    before = rows_path.read_text(encoding="utf-8")
    st = ws.identity()
    reading = DownstreamItem(id="R1", state=st, statement_type="row_reading", task="t:r", verification_status="interpretation_pending",
                             payload={"row": "VOL-I-7.1-01", "interpretation": {
                                 "stage": "ADD-03", "quote": "one hundred and eighty (180) days from the Proposal Due Date"},
                                 "replace_requirement": {"old": "Proposal open for acceptance for 150 days from the Proposal Due Date",
                                                         "new": "Proposal open for acceptance for 180 days from the Proposal Due Date"}},
                             evidence=[BOND_EV])
    dup = DownstreamItem(id="R2", state=st, statement_type="row_new", task="t:r", verification_status="interpretation_pending",
                         payload={"row": dict(BOND_ROW, id="VOL-I-6.3-01", introduced=BOND_INTRO)}, evidence=[BOND_EV])
    ds = DownstreamSet(run_id="s11-b2", created="x", route="recorded", provider="test", model_requested="test",
                       addendum="ADD-03", state=st, items=[reading, dup])
    summ = DS.promote(ws, cand, "b-curated", cps, promoted, ds, "test", {})
    after = rows_path.read_text(encoding="utf-8")
    comments = lambda t: [x for x in t.splitlines() if x.lstrip().startswith("#")]  # noqa: E731
    assert comments(after) == comments(before)                  # every comment of the curated file kept
    changed = [x for x in after.splitlines() if x not in before.splitlines()]
    assert any("180 days" in x for x in changed) and any("stage: ADD-03" in x for x in changed)
    assert summ["readings"] == ["VOL-I-7.1-01"] and summ["rows_new"] == []
    assert any("VOL-I-6.3-01 not written: the id is already in rows.yaml" in n for n in summ["notes"]), summ["notes"]
    ids = [x.id for x in load_rows(rows_path).rows]
    assert ids.count("VOL-I-6.3-01") == 1 and len(ids) == len(set(ids))


# ---------------------------------------------------------------------------------------------- C: completeness

def test_c_a_run_with_a_failed_downstream_batch_is_partial_with_its_reasons(prev_build, area):
    """Every provision is answered and the candidate outputs build, but the downstream batch has no recorded answer
    (it fails), its tasks are unanswered and check-register on the candidate finds the C46 gaps: partial."""
    res = _start(prev_build, area, "c-partial", cassette=area["analysis_only"])
    cp = W.load("c-partial", area["staging"]).data
    assert cp["steps"]["promotion"]["unresolved"] == [] and cp["steps"]["outputs"]["exit_code"] == 0
    assert res["status"] == "partial", (res["status"], res["status_reason"])
    comp = cp["completeness"]
    assert comp["status"] == "partial"
    reasons = " | ".join(comp["reasons"])
    assert "downstream batch downstream-001 failed (no recorded session covers this batch" in reasons
    n = len(json.loads((Path(res["run_dir"]) / "downstream/tasks.json").read_text(encoding="utf-8")))
    assert n > 20 and f"{n} of {n} downstream task(s) unanswered" in reasons
    assert "check-register on the candidate: exit 1" in reasons and "C46" in reasons
    assert comp["check_register"]["c46"] and comp["outputs"]["published"]
    assert {x["task"] for x in comp["downstream"]["unanswered"]} >= {"c46:ADD-03/2.4", "row:VOL-I-6.3-01", "act:deliver"}
    # three records kept apart: what ran, what is complete, what a person approved
    assert cp["execution"]["steps"]["outputs"] == "done" and cp["execution"]["batches"]["downstream"] == {"failed": 1}
    assert cp["approval"]["status"] == "none" and cp["approval"]["decisions"] == []
    md = (Path(res["run_dir"]) / "review/index.md").read_text(encoding="utf-8")
    sec = md[md.index("## Execution, completeness and approval"):md.index("## What is candidate and what is real")]
    assert "**Completeness** (what the run completed): **partial**" in sec and "**Human approval**: **none**" in sec
    assert res["completeness"]["status"] == "partial" and res["approval"] == "none"


@pytest.mark.parametrize("name, expect", [
    ("checkpoint.json", ["24 provision(s) unresolved", "downstream batch downstream-001 failed", "55 of 55 downstream task(s) unanswered",
                         "8 finding(s) {'C46': 8}"]),
    ("review-after-resume/checkpoint-after-resume.json", ["downstream batch downstream-003 failed", "12 of 56 downstream task(s) unanswered",
                                                          "13 downstream task(s) answered only by items that cannot be promoted",
                                                          "the candidate outputs were not published (pre-flight: C16 ADD-03-4.1-01@BASE"]),
])
def test_c_the_blind04_checkpoints_read_as_partial_with_their_reasons(tmp_path, name, expect):
    """The real blind-04 checkpoints, loaded as data (copied into tmp): the record lists what was not completed."""
    from tenderpack.ai.checkpoint import Checkpoint
    (tmp_path / "run").mkdir()
    shutil.copy(ROOT / "rehearsals/blind-04" / name, tmp_path / "run/checkpoint.json")
    cp = Checkpoint.load(tmp_path / "run/checkpoint.json")
    comp = W.completeness(cp)
    assert comp["status"] == "partial"
    reasons = " | ".join(comp["reasons"])
    for x in expect:
        assert x in reasons, (x, reasons)
    assert W._final_status(cp)[0] == "partial" and W.approval(cp)["status"] == "none"


# ---------------------------------------------------------------------------------------------- D: state identity

def _edit_yaml(path: Path, fn) -> None:
    d = _yaml(path)
    fn(d)
    path.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False), encoding="utf-8")


def _first_row_note(d):
    d["rows"][0]["interpretations"][0]["note"] = "edited after the proposals were made"


def _first_value(section: str, field: str):
    def fn(d):
        first = next(iter(d[section]))
        d[section][first] = {**d[section][first], field: "edited after the proposals were made"}
    return fn


EDITS = {   # (pack key, file under it (None: the key names the file), the edit)
    "register": ("register", "rows/VOL-II.yaml", _first_row_note),            # a row's interpretation, in an included file
    "relationships": ("relationships", None, lambda d: d["relationships"][0].update(note="edited")),
    "issues": ("issues", None, _first_value("issues", "text")),
    "clarifications": ("clarifications", None, lambda d: d["clarifications"][0].update(gap="edited")),
    "evidence_items": ("evidence_items_dir", "core.yaml", _first_value("items", "name")),
    "dispositions": ("dispositions_dir", "VOL-I.yaml", _first_value("units", "reason")),
}


@pytest.fixture(scope="module")
def d_cand(prev_build, area):
    """One candidate (stopped after ingest) whose copied inputs the identity tests edit, one value each."""
    return _stopped(prev_build, area, "d-ident", stop="ingest")


@pytest.mark.parametrize("what", list(EDITS))
def test_d_the_state_identity_covers_the_curated_inputs(d_cand, what):
    ctx = d_cand
    ws = ctx.ws
    ws.refresh()
    before = ws.identity()
    key, sub, fn = EDITS[what]
    p = Path(_yaml(ctx.P["pack"])[key])
    p = (p.parent if key == "register" else p) / sub if sub else p
    assert p.is_file(), p
    _edit_yaml(p, fn)                                              # one value changed, in the candidate's copy
    ws.refresh()                                                   # reload: the new inputs are read
    after = ws.identity()
    assert after.fingerprint() != before.fingerprint(), f"{what}: the proposal fingerprint did not change"
    assert [k for k in type(after).model_fields if getattr(after, k) != getattr(before, k)], what


def test_d_an_edit_that_keeps_the_modification_time_is_noticed_before_promotion(prev_build, area):
    from tenderpack.ai.tools import ToolError
    ctx = _stopped(prev_build, area, "d-mtime", stop="ingest")
    ws = ctx.ws
    ws.refresh()
    rows = Path(_yaml(ctx.P["pack"])["register"]).parent / "rows" / "VOL-II.yaml"
    st = os.stat(rows)
    text = rows.read_text(encoding="utf-8")
    rows.write_text(text.replace("The applicable regulations are not identified.",
                                 "The applicable regulations are not identified!"), encoding="utf-8")
    assert rows.stat().st_size == st.st_size
    os.utime(rows, ns=(st.st_atime_ns, st.st_mtime_ns))
    ws.check_fresh()                                               # the quick check (size, inode, mtime) cannot see it
    with pytest.raises(ToolError, match="register_sha256"):
        ws.check_fresh(deep=True)


def test_d_an_input_changed_after_validation_makes_the_set_stale_and_promotion_refuses(prev_build, area):
    ctx = _stopped(prev_build, area, "d-stale", stop="downstream_validation")
    rows = Path(_yaml(ctx.P["pack"])["register"]).parent / "rows" / "VOL-II.yaml"
    _edit_yaml(rows, _first_row_note)                              # a person edits the candidate's register meanwhile
    res = W.resume("d-stale", area["staging"], stop_after="promotion", echo=quiet, sleep=lambda s: None)
    cp = W.load("d-stale", area["staging"]).data
    assert res["status"] == "stopped" and "promotion refused" in res["status_reason"], res["status_reason"]
    assert "STALE" in res["status_reason"] and "register_sha256" in res["status_reason"]
    assert cp["steps"]["promotion"]["status"] == "stopped" and cp["steps"]["promotion"]["refused"]
    assert not (Path(res["run_dir"]) / "promotion.json").exists()
    assert not (ctx.P["dir"] / "curation/amendments/ADD-03.yaml").exists()


# ---------------------------------------------------------------------------------------------- F: the downstream lands

def CASSETTE_DOWNSTREAM() -> str:
    """The downstream answer of the cassette (the JSON text, with a placeholder state)."""
    s = next(x for x in _yaml(CASSETTE)["sessions"] if x["phase"] == "downstream")
    return s["turns"][0]["response"]["text"].replace("${state}", "{}")


@pytest.fixture(scope="module")
def full(prev_build, area):
    res = _start(prev_build, area, "f-full")
    cp = W.load("f-full", area["staging"]).data
    return {"res": res, "cp": cp, "dir": Path(res["run_dir"])}


def test_f_the_downstream_items_reach_a_clean_candidate(full):
    """Every downstream item is promotable and lands; check-register on the candidate is clean; the outputs publish.
    The run is still `partial`, for exactly one reason: provision 2.2 (it ends a statement of ADD-01 2.1) is escalated
    for a person (the engine does not re-target an earlier amendment), and its downstream task is answered by an issue."""
    res, cp, d = full["res"], full["cp"], full["dir"]
    items = _yaml(d / "downstream/proposals.yaml")["downstream_set"]["items"]
    st = {i["id"]: (i["statement_type"], i["verification_status"]) for i in items}
    bad = {k: v for k, v in st.items() if v[1] not in DS.PROMOTABLE}
    assert not bad, {k: (v, [x["detail"] for x in next(i for i in items if i["id"] == k)["validation"] if not x["ok"]])
                     for k, v in bad.items()}
    kinds = {v[0] for v in st.values()}
    assert {"row_new", "row_reading", "issue", "evidence_item", "activity", "clarification_item", "no_change"} <= kinds
    prom = cp["steps"]["promotion"]
    assert set(prom["rows_new"]) == {"ADD-03-6.8-01", "ADD-03-cover-01"} and len(prom["readings"]) == 11
    assert set(prom["issues"]) == {"I-ADD03-DELIVERY-REG", "I-ADD03-2.2-ADD01-SENTENCE"}
    assert prom["evidence_items"] == ["EV-DELIVERY-REGISTRATION"] and prom["activities"] == ["register-delivery-reps"]
    assert prom["clarifications"] == ["CQ-BOND-FC-COVERAGE"] and prom["unresolved"] == ["ADD-03:2.2"]
    cr = cp["steps"]["check_register"]
    assert cr["exit_code"] == 0 and cr["findings"] == 0, cr.get("first")
    o = cp["steps"]["outputs"]
    assert o["exit_code"] == 0 and not o["refused"]
    comp = cp["completeness"]
    assert comp["downstream"]["answered"] == comp["downstream"]["tasks"] > 20, comp["downstream"]
    assert not comp["downstream"]["batches_not_done"] and comp["outputs"]["published"]
    assert res["status"] == "partial" and comp["reasons"] == [
        "1 provision(s) unresolved in the candidate (listed first in the review packet)"], comp["reasons"]
    assert cp["approval"]["status"] == "none" and cp["interventions"] == []     # recorded route: no person, no host


def test_f_the_new_rows_are_on_a1_with_their_introduction_and_the_activity_on_a5(full):
    d = full["dir"]
    out = d / "candidate/out"
    a1 = json.loads((out / "a1/a1.json").read_text(encoding="utf-8"))
    rows = {r["id"]: r for r in a1["rows"]}
    for rid, by in (("ADD-03-6.8-01", "ADD-03/2.4"), ("ADD-03-cover-01", "ADD-03/cover/para3")):
        r = rows[rid]
        assert r["status:ADD-03"] == f"NEW (introduced by {by})", r["status:ADD-03"]
        assert r["status:BASE"] == f"NOT IN FORCE (introduced at ADD-03 by {by})" and r["source:BASE"] == ""
        assert r["candidate_status"].startswith("PROPOSED BY THE AI WORKFLOW: new row")
    assert rows["VOL-I-6.3-01"]["requirement"] == "Bid Bond valid for 210 days from the Proposal Due Date (extendable on demand)"
    assert rows["VOL-I-6.3-01"]["candidate_status"].startswith("PROPOSED BY THE AI WORKFLOW: reading re-made")
    # ADD-03 is PARTIAL in the candidate (2.2 for a person): A5's working programme for ADD-03 carries the activity
    prog = json.loads((out / "a5/working/ADD-03.json").read_text(encoding="utf-8"))
    acts = prog.get("activities") if isinstance(prog, dict) else prog
    reg = next(a for a in acts if a.get("id") == "register-delivery-reps")
    assert "ADD-03-6.8-01" in reg["req_ids"]
    cmp_ = json.loads((d / "review/outputs-before-after.json").read_text(encoding="utf-8"))
    assert {"ADD-03-6.8-01", "ADD-03-cover-01"} <= set(cmp_["a1"]["new"]) and "register-delivery-reps" in cmp_["a5"]["new"]
    # the rows were written by id through the YAML structure: the AI rows file loads, each id once
    from tenderpack.register import load_rows
    rf = load_rows(Path(_yaml(d / "candidate/pack.yaml")["register"]))
    ids = [x.id for x in rf.rows]
    assert len(ids) == len(set(ids)) and {"ADD-03-6.8-01", "ADD-03-cover-01"} <= set(ids)
    md = (d / "review/index.md").read_text(encoding="utf-8")
    assert "**Completeness** (what the run completed): **partial**: 1 provision(s) unresolved" in md


def test_c_complete_only_when_every_part_is_done(tmp_path):
    """The completeness rule itself, on a checkpoint written for it: complete when every provision is answered, every
    downstream task answered by a promotable item, check-register clean and the outputs published; each missing part
    is a reason (and approval stays a separate record)."""
    from tenderpack.ai.checkpoint import Checkpoint
    run = tmp_path / "run"
    (run / "downstream").mkdir(parents=True)
    (run / "downstream/tasks.json").write_text(json.dumps([{"id": "row:R1", "kind": "row_reading"},
                                                           {"id": "act:a1", "kind": "activity"}]), encoding="utf-8")
    items = [{"id": "D1", "task": "row:R1", "statement_type": "row_reading", "verification_status": "interpretation_pending"},
             {"id": "D2", "task": "act:a1", "statement_type": "no_change", "verification_status": "interpretation_pending"}]
    (run / "downstream/proposals.yaml").write_text(yaml.safe_dump({"downstream_set": {"items": items},
                                                                   "controller": {"held_back": {}}}), encoding="utf-8")
    cp = Checkpoint.new(run / "checkpoint.json", run_id="r", addendum="ADD-03", settings={}, inputs={}, candidate={})
    cp.data["provisions"] = {"ADD-03:1.1": {"status": "validated"}}
    cp.data["batches"] = {"downstream-001": {"phase": "downstream", "status": "done", "tasks": ["row:R1", "act:a1"]}}
    for s, extra in (("promotion", {"unresolved": []}), ("downstream", {}), ("check_register", {"exit_code": 0, "findings": 0}),
                     ("outputs", {"exit_code": 0, "refused": False})):
        cp.step(s).update(status="done", **extra)
    assert W.completeness(cp)["status"] == "complete" and W._final_status(cp) == ("complete", None)
    assert W.completeness(cp)["downstream"]["no_change"] == ["act:a1"]
    items[1]["verification_status"] = "escalated"
    (run / "downstream/proposals.yaml").write_text(yaml.safe_dump({"downstream_set": {"items": items}}), encoding="utf-8")
    cp.step("check_register").update(exit_code=1, findings=1, by_kind={"C46": 1}, first=["[C46] X: [A1] gap"])
    comp = W.completeness(cp)
    assert comp["status"] == "partial" and comp["downstream"]["unresolved"][0]["task"] == "act:a1"
    assert any("check-register on the candidate: exit 1" in x and "C46" in x for x in comp["reasons"])
    assert W.approval(cp)["status"] == "none"


# ---------------------------------------------------------------------------------------------- follow-ups (D2, D3)

def test_c_a_split_batch_is_followed_through_its_parts(tmp_path):
    """A batch the request layer split (status `split`, `parts`) is not a failure: its parts are the batches."""
    from tenderpack.ai.checkpoint import Checkpoint
    run = tmp_path / "run"
    (run / "downstream").mkdir(parents=True)
    (run / "downstream/tasks.json").write_text(json.dumps([{"id": "act:a1", "kind": "activity"},
                                                           {"id": "act:a2", "kind": "activity"}]), encoding="utf-8")
    items = [{"id": f"D{i}", "task": f"act:a{i}", "statement_type": "no_change", "verification_status": "interpretation_pending"}
             for i in (1, 2)]
    (run / "downstream/proposals.yaml").write_text(yaml.safe_dump({"downstream_set": {"items": items}}), encoding="utf-8")
    cp = Checkpoint.new(run / "checkpoint.json", run_id="r", addendum="ADD-03", settings={}, inputs={}, candidate={})
    cp.data["batches"] = {
        "downstream-001": {"phase": "downstream", "status": "split", "parts": ["downstream-001.1", "downstream-001.2"],
                           "tasks": ["act:a1", "act:a2"]},
        "downstream-001.1": {"phase": "downstream", "status": "done", "tasks": ["act:a1"], "split_from": "downstream-001"},
        "downstream-001.2": {"phase": "downstream", "status": "done", "tasks": ["act:a2"], "split_from": "downstream-001"}}
    for s, extra in (("promotion", {"unresolved": []}), ("downstream", {}), ("check_register", {"exit_code": 0, "findings": 0}),
                     ("outputs", {"exit_code": 0, "refused": False})):
        cp.step(s).update(status="done", **extra)
    assert W.completeness(cp)["status"] == "complete", W.completeness(cp)["reasons"]
    cp.data["batches"]["downstream-001.2"]["status"] = "escalated"          # a part that did not run is still a reason
    assert any("downstream-001.2 escalated" in x for x in W.completeness(cp)["reasons"])


def test_the_downstream_packet_carries_every_unit_in_full():
    """Nothing is shortened at the source: a unit longer than 4,000 characters is in `units_after` in full (a packet
    that does not fit is split or escalated by the request layer, never squeezed)."""
    from types import SimpleNamespace
    from tenderpack.amend import StageResult, UState
    long = " ".join(f"word{i}" for i in range(1500))
    assert len(long) > 4000
    st = {"ADD-03:9.9": UState("ADD-03:9.9", "ADD-03", "clause", "active", long, None, [1], "text_layer", None)}
    ws = SimpleNamespace(prev_stage=lambda a: "ADD-02", r={"templates": {}, "rowfile": SimpleNamespace(anchors={}),
                                                         "evidence_items": {}, "curated_issues": {}, "assumptions": {}})
    promoted = {"r2": {"stages": [StageResult("ADD-03", "ADD-03", None, "APPLIED", st)], "evals": []}, "ops": {}}
    pk = DS.packet(ws, "ADD-03", [{"id": "esc:ADD-03:9.9", "kind": "escalation", "provision": "ADD-03:9.9",
                                   "scope": {"units": []}}], promoted, 1, {})
    assert pk["units_after"]["ADD-03:9.9"]["text"] == long


def test_d_the_identity_covers_the_trigger_facts_and_the_formula_registry(tmp_path):
    from tenderpack.ai.tools import Workspace
    ws = Workspace(tmp_path / "build", tmp_path / "pack.yaml", tmp_path)
    cfg = {"triggers": str(tmp_path / "curation/triggers.yaml")}
    before = ws._curation_shas(cfg)
    (tmp_path / "curation").mkdir()
    (tmp_path / "curation/triggers.yaml").write_text("triggers:\n  - {condition: ADD-03/S7, occurred: true}\n", encoding="utf-8")
    after_trigger = ws._curation_shas(cfg)
    assert after_trigger["curation_sha256"] != before["curation_sha256"]
    (tmp_path / "config").mkdir()
    (tmp_path / "config/formulas.yaml").write_text("formulas: {}\n", encoding="utf-8")
    assert ws._curation_shas(cfg)["curation_sha256"] != after_trigger["curation_sha256"]
