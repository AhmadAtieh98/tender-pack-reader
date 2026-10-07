"""Session 12 (W3a; the owner's part 2): a closed clarification route is said everywhere.

VOL-I 5.2: requests for clarification are submitted no later than ten Working Days before the Proposal Due Date. The pack
computes that cut-off (the date rule CLARIFICATION-CUTOFF; clarify.effective_cutoff). When an addendum issues after it,
no question about that addendum can be submitted as a clarification: every escalation, every proposed clarification
entry, the candidate A3's unresolved list, A5's clarification activity and the review packet say so in one wording
(clarify.CLOSED_WINDOW), and a proposed clarification entry is still written as a DRAFT with that note. When the
addendum issues before the cut-off nothing changes.

Regression material: blind rehearsal 05 (COMPARISON.md 1.3 and IE6, follow-up 12): ADD-03 issued Sunday 15 November 2026,
after the cut-off of Thursday 12 November; the closed route was recorded only for D1, and three items still suggested a
clarification without saying the route had closed. The dates below are the pack's computed values for that synthetic
addendum (the test reads them from the run and checks them against the wording, never types them into code). The real
pack's ADD-01 and ADD-02 issued before the cut-off."""
from __future__ import annotations

import pytest

import s12_blind05
from tenderpack import clarify, live, partial, programme, stage2
from tenderpack.ai import downstream as DS
from tenderpack.schedule import CLARIFICATION_RULE
from tenderpack.util import ROOT


@pytest.fixture(scope="module")
def r(tmp_path_factory):
    return s12_blind05.run(tmp_path_factory)["r"]


@pytest.fixture(scope="module")
def real():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


@pytest.fixture(scope="module")
def cand(r):
    return partial.compute(r)


@pytest.fixture(scope="module")
def win(r):
    return clarify.window(r, "ADD-03")


def test_the_window_is_computed_from_the_pack(r, win):
    eff = clarify.effective_cutoff(r, "ADD-03")
    assert win["closed"] and win["date"] == eff["date"] and win["rule"] == "VOL-I 5.2"
    assert win["issued"] == next(s.issued for s in r["stages"] if s.stage == "ADD-03")
    assert win["date"] < win["issued"]
    assert win["note"] == clarify.CLOSED_WINDOW.format(date=win["date"], rule="VOL-I 5.2")
    assert "cannot be submitted as a clarification" in win["note"] and "bid-decision for a person" in win["note"]
    assert not clarify.window(r, "ADD-02")["closed"]


def test_nothing_changes_when_the_addendum_issues_before_the_cut_off(real):
    for s in ("ADD-01", "ADD-02"):
        w = clarify.window(real, s)
        assert w is not None and not w["closed"] and w["note"] == "", w
    prog = programme.stage_planner(real, "ADD-02")(real["assumptions"])
    for a in prog["activities"]:
        assert not any("clarification window closed" in str(f) for f in a.get("flags") or []), a["id"]


def test_the_candidate_a3_unresolved_list_says_it(cand, win):
    assert cand["clarification_window"]["closed"] and cand["clarification_window"]["note"] == win["note"]
    provs = cand["blockers"]["provisions"]
    # session 14 (W2): this assertion encoded the blind-07 scorer's defect 13 (the note on EVERY unresolved provision,
    # schema errors and tool limitations included); the note now goes on every one except a processing failure
    assert provs and all(p["route"] == (win["note"] if partial.route_class(p["reason"]) != "software" else "")
                         for p in provs)
    assert any(p["route"] == win["note"] for p in provs)
    md = partial.markdown(cand)
    sec = md.split("### Unresolved provisions")[1].split("\n### ")[0]
    assert win["note"] in sec
    assert win["note"] in cand["paragraph"]


def test_the_candidate_a5_clarification_activity_says_it(cand, win):
    acts = [a for a in cand["a5"]["activities"] if a.get("deadline_rule") == CLARIFICATION_RULE]
    assert acts, "the clarification route activity"
    for a in acts:
        assert any(win["note"] in f for f in a["flags"]), a["flags"]
    readme = programme.candidate_readme(cand["a5"], cand["paragraph"])
    assert win["note"] in readme


def test_the_diff_and_the_review_packet_carry_it(r, win):
    md, data = live.diff(r, "ADD-02", "ADD-03")
    assert data["clarification_window"]["closed"] and data["clarification_window"]["note"] == win["note"]
    assert win["note"] in md
    lines = clarify.route_lines(data["clarification_window"])
    assert lines and win["note"] in lines[0]
    assert clarify.route_lines({"closed": False, "note": ""}) == []


def test_a_proposed_clarification_entry_stays_a_draft_with_the_note(win):
    e = {"id": "CQ-X", "response_status": "draft, not sent", "proposed_question": "Which basis governs?"}
    out = clarify.with_window(e, win)
    assert out["response_status"] == "draft, not sent" and out["clarification_window"] == win["note"]
    assert e.get("clarification_window") is None                       # the proposal itself is not edited
    assert clarify.with_window(e, {"closed": False, "note": ""}) == e
    # the published register shows it beside the question
    md = clarify.markdown({"clarifications": [out]})
    assert win["note"] in md


def test_the_downstream_tasks_carry_the_window(r, win):
    t = DS.window_fields(r, "ADD-03")
    assert t == {"clarification_window": win["note"]}
    assert DS.window_fields(r, "ADD-02") == {}
