"""Session 12 (W3a; the owner's part 2): confirmations are not changes, 'not reached' counts the citations of
unresolved provisions, issue references are checked, and the candidate A3/A5 stay apart from the validated state.

Regression material (blind rehearsal 05, COMPARISON.md): false signal 2 (Q15, the decoy, and Q16, a confirmation, put
technical-proposal, deviations-review and form-4e on REWORK and marked VOL-IV-F4E-01 CHANGED; the VOL-I-6.2-01 re-reading,
'Words unchanged', put the envelope activities on REWORK; blind-04 follow-up 6), false signal 4 (I-VOL-II-MISSING and
the addendum's own I-ADD03-29.2-NO-OP labelled 'not reached by this addendum's changes'), false signal 6 (row notes cite
I-ADD03-AP-PRICE-BASIS, an issue that was never promoted). The candidate is blind-05's own (tests/fixtures/s12_blind05.py:
its committed pack and curation, ingested afresh into a disposable folder). Real changes must stay changes: VOL-II 3.1
amended by ADD-03 4.1, Q17 (one certificate per JV member), Q20 (the Indexed Proportion in Form 4-F), Q21 (crane plan).
The real pack (the committed build) is used to show what does not change there. Nothing is written under the repository."""
from __future__ import annotations

import copy

import pytest

import s12_blind05
from tenderpack import live, partial, programme, schedule, signals, stage2
from tenderpack.ai import downstream as DS
from tenderpack.ai.contract import DownstreamItem, DownstreamSet, EvidenceRef, RowReadingPayload
from tenderpack.util import ROOT

CONFIRMED = "CONFIRMED (unchanged)"


@pytest.fixture(scope="module")
def b05(tmp_path_factory):
    return s12_blind05.run(tmp_path_factory)


@pytest.fixture(scope="module")
def r(b05):
    return b05["r"]


@pytest.fixture(scope="module")
def real():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


@pytest.fixture(scope="module")
def cand(r):
    return partial.compute(r)


def _deltas(r, frm, to, answers=True):
    progs = {s: programme.stage_planner(r, s)(r["assumptions"]) for s in (frm, to)}
    ea = {e["row"].id: e["stages"][frm] for e in r["evals"]}
    eb = {e["row"].id: e["stages"][to] for e in r["evals"]}
    return schedule.deltas(progs[frm], progs[to], ea, eb, answers=programme.answers_by_row(r, to) if answers else None)


# ---------------------------------------------------------------------------------------------- 1. confirmations

def test_the_predicate_on_its_own():
    a = {"status": "ACTIVE", "text": "x shall y", "cells": None, "dates": [], "stale": [],
         "interpretation": {"stage": "BASE", "quote": "x shall y", "parameters": {"n": 7}, "consequence": "none_stated"}}
    q = {"op": "ADD-03/Q16", "type": "annotate", "effect": "interprets", "provision": "ADD-03:Q16", "answer": True,
         "class": "adds"}
    b = copy.deepcopy(a)
    b["interpretation"].update(stage="ADD-03", note="Words unchanged", parameters={"n": 7, "includes": "assumptions"})
    d = signals.requirement_delta(a, b, [q])
    assert not d["changed"] and d["confirmed"] and "ADD-03/Q16 (interprets; ADD-03:Q16" in d["detail"]
    assert "includes" in d["detail"]                         # the recorded parameter is shown, not hidden
    # the same parameter added under an obligation-adding op is a change
    adds = dict(q, op="ADD-03/Q17", effect="adds_obligation", provision="ADD-03:Q17")
    assert signals.requirement_delta(a, b, [adds])["what"] == ["parameters"]
    # a value that changes is a change whatever the label
    c = copy.deepcopy(b)
    c["interpretation"]["parameters"] = {"n": 10}
    assert "parameters" in signals.requirement_delta(a, c, [q])["what"]
    # words of change in the answer override the label
    assert signals.requirement_delta(a, b, [dict(q, **{"class": "changes"})])["changed"]
    # a re-made reading with only its note different, and no op: confirmed by the reading
    n = copy.deepcopy(a)
    n["interpretation"].update(stage="ADD-03", note="Words unchanged")
    d = signals.requirement_delta(a, n, [])
    assert d["confirmed"] and not d["changed"] and "same words" in d["detail"]
    # STALE only because of the confirming answer (a new dependency): not a change; still said
    s = copy.deepcopy(a)
    s["stale"] = ["new dependency ADD-03:Q16"]
    d = signals.requirement_delta(a, s, [q])
    assert d["confirmed"] and "STALE until a person re-reads it" in d["detail"]
    assert signals.requirement_delta(a, s, [adds])["what"] == ["stale"]


def test_confirmations_make_no_rework_in_the_programme_deltas(r):
    dl = _deltas(r, "ADD-02", "ADD-03")
    rework = {d["activity"]: d["detail"] for d in dl if d["change"] == "REWORK"}
    for aid in ("deviations-review", "form-4e"):                         # Q16 confirms VOL-I 9.6 / Form 4-E
        assert "VOL-I-9.6-01" not in rework.get(aid, "") and "VOL-IV-F4E-01" not in rework.get(aid, ""), rework.get(aid)
    for aid in ("assemble-envelope-a", "assemble-envelope-b", "copies", "deliver", "seal-and-mark"):
        assert "VOL-I-6.2-01" not in rework.get(aid, ""), (aid, rework.get(aid))
    assert "VOL-II-6.4-0" not in rework.get("technical-proposal", "")     # Q15, the decoy
    conf = {d["activity"]: d["detail"] for d in dl if d["change"] == CONFIRMED}
    assert "VOL-I-9.6-01" in conf["form-4e"] and "ADD-03/Q16" in conf["form-4e"] and "ADD-03:Q16" in conf["form-4e"]
    assert "VOL-II-6.4-01" in conf["technical-proposal"] and "ADD-03/Q15" in conf["technical-proposal"]
    # the real changes stay changes
    assert "VOL-II-3.1-01" in rework["technical-proposal"] and "VOL-I-9.7-01" in rework["technical-proposal"]
    assert "VOL-I-8.3-01" in rework["iso-copy"] and "VOL-IV-F4F-01" in rework["form-4f"]


def test_the_candidate_replan_and_its_readme_agree(cand):
    a5 = cand["a5"]
    s = a5["summary"]
    assert "form-4e" not in s["rework"] and "deviations-review" not in s["rework"], s["rework"]
    assert not {"assemble-envelope-b", "copies", "deliver", "seal-and-mark"} & set(s["rework"]), s["rework"]
    assert {"technical-proposal", "iso-copy", "form-4f"} <= set(s["rework"])
    acts = {a["id"]: a for a in a5["activities"]}
    tp = acts["technical-proposal"]
    assert "VOL-II-3.1-01" in tp["caused_by_rows"] and not {"VOL-II-6.4-01", "VOL-II-6.4-02"} & set(tp["caused_by_rows"])
    readme = programme.candidate_readme(a5, cand["paragraph"])
    sec = readme.split("## Requirement changed")[1].split("\n## ")[0]
    for rid in ("VOL-I-9.6-01", "VOL-IV-F4E-01", "VOL-I-6.2-01", "VOL-II-6.4-01"):
        assert rid not in sec, rid
    conf = readme.split("## Confirmed, unchanged")[1].split("\n## ")[0]
    assert "VOL-I-9.6-01" in conf and "ADD-03/Q16" in conf and "ADD-03:Q16" in conf


def test_the_diff_and_the_review_packet_list_confirmations_apart(r):
    md, data = live.diff(r, "ADD-02", "ADD-03")
    req = data["requirements"]
    assert "VOL-IV-F4E-01" not in req["changed"] and "VOL-IV-F4E-01" in req["confirmed"]
    line = next(x for x in md.splitlines() if x.startswith(f"- {CONFIRMED} VOL-IV-F4E-01"))
    assert "ADD-03/Q16" in line and "ADD-03:Q16" in line
    assert {"VOL-II-3.1-01", "VOL-IV-F4F-01"} <= set(req["changed"])
    for d in data["programme"]:
        if d["change"] == "REWORK":
            assert "VOL-I-9.6-01" not in d["detail"] and "VOL-I-6.2-01" not in d["detail"], d


def test_a2_shows_confirmations_as_confirmed_not_moved(r):
    a2 = stage2.a2(r)
    moved = {(m["stage"], m["row"]): m for m in a2["rows_moved"] if m["stage"] == "ADD-03"}
    for rid in ("VOL-I-9.6-01", "VOL-IV-F4E-01", "VOL-II-6.4-01", "VOL-II-6.4-02", "VOL-I-6.2-01"):
        assert moved[("ADD-03", rid)]["change"] == CONFIRMED, (rid, moved[("ADD-03", rid)])
    assert "ADD-03/Q16" in "; ".join(moved[("ADD-03", "VOL-I-9.6-01")]["why"])
    for rid in ("VOL-I-8.3-01", "VOL-II-3.1-01", "VOL-IV-F4F-01"):
        assert moved[("ADD-03", rid)]["change"] == "CHANGED", rid
    sec = a2["markdown"].split("## ADD-03")[1]
    table = sec.split("### Register rows that move")[1].split("###")[0]
    assert "| VOL-I-9.6-01 |" not in table and "| VOL-I-8.3-01 |" in table
    conf = sec.split(f"### Rows confirmed or re-read, unchanged ({CONFIRMED})")[1].split("###")[0]
    assert "| VOL-I-9.6-01 |" in conf and "ADD-03/Q16" in conf


def test_real_pack_confirmations_are_confirmed_and_changes_stay(real):
    dl = _deltas(real, "ADD-01", "ADD-02")
    conf = {d["activity"]: d["detail"] for d in dl if d["change"] == CONFIRMED}
    assert "ADD-02/Q8 (confirms; ADD-02:Q8" in conf["bond-approval"]
    rework = {d["activity"]: d["detail"] for d in dl if d["change"] == "REWORK"}
    assert "VOL-I-9.1-01" in rework["assemble-envelope-a"]            # Form 4-G inserted: a real change


# ---------------------------------------------------------------------------------------------- 2. not reached

def test_not_reached_counts_the_citations_of_unresolved_provisions(cand):
    md = {m["id"]: m for m in cand["blockers"]["missing_documents"]}
    assert md["I-VOL-II-MISSING"]["reached_by_this_addendum"], md["I-VOL-II-MISSING"]
    assert md["I-ADD03-29.2-NO-OP"]["reached_by_this_addendum"], md["I-ADD03-29.2-NO-OP"]
    sec = partial.markdown(cand).split("### Documents referenced but not supplied")[1].split("\n### ")[0]
    for i in ("I-VOL-II-MISSING", "I-ADD03-29.2-NO-OP"):
        line = next(x for x in sec.splitlines() if x.startswith(f"- **{i}**"))
        assert "not reached by this addendum's changes" not in line and "reached by this addendum: " in line, line


def test_not_settled_rows_are_the_same_in_a3_and_a5(cand):
    rows = {x["row"] for x in cand["blockers"]["unresolved_rows"]}
    blocked = {r for x in cand["a5"]["blocked"] for r in x["rows"]}
    assert blocked <= rows


# ---------------------------------------------------------------------------------------------- 3. issue references

def test_issue_ids_are_read_from_text_and_row_ids_are_not():
    t = ("see I-ADD03-AP-PRICE-BASIS. Rows VOL-I-6.2-01 and VOL-I-10.3-01; VOL-II-MISSING; I-A5-fin-model-build and "
         "(I-CONCESSION).")
    assert signals.issue_refs(t) == ["I-ADD03-AP-PRICE-BASIS", "I-A5-fin-model-build", "I-CONCESSION"]
    assert signals.broken_issue_refs(signals.issue_refs(t), {"I-CONCESSION"}) == ["I-ADD03-AP-PRICE-BASIS"]


def test_check_register_reports_a_broken_issue_reference(r):
    f = [x for x in stage2.register_findings(r) if x["kind"] == "issue_ref"]
    hit = [x for x in f if "I-ADD03-AP-PRICE-BASIS" in x["detail"]]
    assert {x["where"] for x in hit} >= {"VOL-I-10.3-01"}, f
    assert all(signals.BROKEN in x["detail"] for x in hit)
    assert not any("I-ADD03-PRICE-BASIS " in x["detail"] or x["detail"].endswith("I-ADD03-PRICE-BASIS") for x in f)


def test_the_real_pack_has_no_broken_issue_reference(real):
    assert [x for x in stage2.register_findings(real) if x["kind"] == "issue_ref"] == []


def test_the_candidate_a3_names_a_broken_reference_instead_of_linking_it(cand):
    oi = {x["id"]: x for x in cand["open_issues_in_play"]}
    assert "I-ADD03-AP-PRICE-BASIS" in oi, sorted(oi)
    assert oi["I-ADD03-AP-PRICE-BASIS"]["text"].startswith(signals.BROKEN)
    assert "I-ADD03-PRICE-BASIS" in oi and not oi["I-ADD03-PRICE-BASIS"]["text"].startswith(signals.BROKEN)
    assert signals.BROKEN in partial.markdown(cand)


def _reading_set(note: str) -> tuple[DownstreamSet, list]:
    st = {"pack_id": "test", "evidence_build_id": "test", "validated_stage": "ADD-02", "working_stage": "ADD-03"}
    ev = EvidenceRef(doc="VOL-I", unit_id="VOL-I:10.3", page=1, kind="span", words="Financial Model")
    it = DownstreamItem(id="D1", state=st, statement_type="row_reading", task="row:VOL-I-10.3-01", provision="ADD-03:3.4",
                        payload={"row": "VOL-I-10.3-01", "interpretation": {"stage": "ADD-03", "quote": "q", "note": note}},
                        evidence=[ev], verification_status="interpretation_pending")
    ds = DownstreamSet(run_id="s12", created="2026-10-05T00:00:00Z", route="recorded", provider="test",
                       model_requested="test", addendum="ADD-03", state=st, items=[it])
    return ds, [{"pl": RowReadingPayload.model_validate(it.payload), "recs": [], "invalid": [], "insufficient": [],
                 "conflict": [], "interp": []}]


def test_downstream_holds_back_a_reading_whose_note_names_an_issue_not_promoted():
    ds, F = _reading_set("The price basis conflicts with Q19: see I-ADD03-AP-PRICE-BASIS.")
    held = DS._closure(ds, F, {}, {}, {"I-CONCESSION"}, {}, {})
    assert "D1" in held and "I-ADD03-AP-PRICE-BASIS" in held["D1"], held
    assert ds.items[0].verification_status == "insufficient_evidence"
    ds, F = _reading_set("see I-CONCESSION and I-A5-FEASIBILITY")
    assert DS._closure(ds, F, {}, {}, {"I-CONCESSION"}, {}, {}) == {}


# ---------------------------------------------------------------------------------------------- 6. candidate vs validated

def test_the_new_signals_stay_in_the_candidate_and_approval_is_shown_apart(r, cand):
    assert r["validated"].stage == "ADD-02" and cand["validated_stage"] == "ADD-02" and cand["stage"] == "ADD-03"
    readme = programme.candidate_readme(cand["a5"], cand["paragraph"])
    assert "CANDIDATE — NOT VALIDATED" in readme and CONFIRMED in readme
    md = partial.markdown(cand)
    assert md.startswith("# A3 CANDIDATE") and "NOT VALIDATED" in md.splitlines()[0]
    assert "review proposed" in cand["paragraph"]                      # approval status, apart from the ops' validity
    # the validated A5 (ADD-02) carries no ADD-03 signal: its deltas stop at the validated stage
    prog_v = programme.stage_planner(r, "ADD-02")(r["assumptions"])
    assert prog_v["stage"] == "ADD-02" and not any("ADD-03" in str(a.get("flags")) for a in prog_v["activities"])
    assert not any("CLARIFICATION ROUTE CLOSED" in str(a.get("flags")) for a in prog_v["activities"])
    assert any("CLARIFICATION ROUTE CLOSED (candidate)" in str(a.get("flags")) for a in cand["a5"]["activities"])
    # A2 is the reconciliation of every stage: the ADD-03 confirmations sit under ADD-03, the ADD-02 section is as before
    a2 = stage2.a2(r)["markdown"]
    assert "ADD-03/Q16" not in a2.split("## ADD-03")[0]


def test_a_row_the_stage_does_not_settle_is_never_called_confirmed(r):
    # VOL-V-29.2-01: STALE only through Q19 (labelled interprets), but ADD-03 3.3, which replaces VOL-V 29.2, is unresolved
    md, data = live.diff(r, "ADD-02", "ADD-03")
    assert "VOL-V-29.2-01" not in data["requirements"]["confirmed"]
    assert "VOL-V-29.2-01" in data["requirements"]["not_settled"]
    assert any(x.startswith("- NOT SETTLED VOL-V-29.2-01:") and "ADD-03:3.3" in x for x in md.splitlines())
    m = next(x for x in stage2.a2(r)["rows_moved"] if x["stage"] == "ADD-03" and x["row"] == "VOL-V-29.2-01")
    assert m["change"] == "CHANGED" and any(w.startswith("NOT SETTLED") for w in m["why"]), m
