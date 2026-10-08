"""Session 14 (coordinator; the full suite on the frozen code, test_session12_signals): F2's named-deliverable reach
(programme.named_deliverable_reach) attached an issue raised only at a LATER stage (ADD-03, its words naming the
Financial Model) to the Financial Model activity of the validated ADD-02 programme. An issue bears on a stage's
programme only from the stage it bears from (stage2.issue_stages, the rule the row reach already follows)."""
from __future__ import annotations

from tenderpack import programme


def test_only_the_issues_in_force_at_the_planned_stage_reach_by_their_words():
    r = {"order": ["BASE", "ADD-01", "ADD-02", "ADD-03"],
         "issue_stages": {"I-OLD": "ADD-01", "I-NOW": "ADD-02", "I-LATER": "ADD-03"}}
    assert programme.issues_in_force(r, "ADD-02") == {"I-OLD", "I-NOW"}
    assert programme.issues_in_force(r, "ADD-03") == {"I-OLD", "I-NOW", "I-LATER"}
    assert programme.issues_in_force(r, "BASE") == set()


def test_an_issue_without_a_known_start_stage_is_kept_and_an_unknown_stage_filters_nothing():
    r = {"order": ["BASE", "ADD-01"], "issue_stages": {"I-A": "ADD-01"}}
    assert programme.issues_in_force(r, "ADD-01", ["I-A", "I-NO-STAGE"]) == {"I-A", "I-NO-STAGE"}
    assert programme.issues_in_force(r, "ADD-09", ["I-A"]) == {"I-A"}


def test_the_named_reach_skips_an_issue_not_yet_in_force():
    acts = [{"id": "fin-model-build", "evidence_items": ["EV-FM"], "predecessors": [], "envelope": "B"}]
    words = {"I-LATER": "the Financial Model term start", "I-NOW": "the Financial Model term start"}
    pend = {"I-LATER": {}, "I-NOW": {}}
    r = {"order": ["ADD-02", "ADD-03"], "issue_stages": {"I-LATER": "ADD-03", "I-NOW": "ADD-02"}}
    keep = programme.issues_in_force(r, "ADD-02", pend)
    got = programme.named_deliverable_reach(acts, pend, {"EV-FM": "Financial Model"},
                                            {i: w for i, w in words.items() if i in keep})
    assert set(got) == {"I-NOW"}


def test_an_issue_with_no_established_start_does_not_reach_by_its_words():
    """An issue that states no `since` and cites no unit (a candidate's promoted issue) has no known start stage; the
    word-based reach (a PROPOSED reading of the issue's words) does not carry it into any stage's programme. The row
    rule still carries it wherever its rows are."""
    order = ["BASE", "ADD-01", "ADD-02", "ADD-03"]
    cur = {"I-STATED": {"since": "ADD-01"}, "I-UNITS": {"units": ["VOL-I:12.1"]}, "I-ROWS": {"rows": ["VOL-I-12.1-01"]},
           "I-NONE": {"rows": []}}
    assert programme.issues_with_known_start(cur, order) == {"I-STATED", "I-UNITS", "I-ROWS"}


def test_the_real_pack_keeps_the_concession_reach_and_a_candidate_issue_without_a_start_stays_out():
    """I-CONCESSION states no start itself but rows in force cite it, so its words still reach the Financial Model chain
    (F2's R3-14-3); the integration case of the other side is test_session12_signals (an ADD-03 candidate's promoted
    issues never reach the validated ADD-02 programme)."""
    from tenderpack import stage2
    from tenderpack.util import ROOT
    r = stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)
    prog = programme.stage_planner(r, r["validated"].stage)(r["assumptions"])
    fm = next(a for a in prog["activities"] if a["id"] == "fin-model-build")
    assert "I-CONCESSION" in (fm.get("open_decisions") or [])


def test_only_rows_in_force_at_the_planned_stage_anchor_an_issue():
    """An issue cited only by a row introduced at a later stage (blind-05's ADD-03-3.2-01, NOT IN FORCE at ADD-02) has
    no row in force at the planned stage, so that row does not establish its start for the word-based reach."""
    class Row:
        def __init__(self, i): self.id = i
    r = {"evals": [{"row": Row("ROW-NOW"), "stages": {"ADD-02": {"active": True}, "ADD-03": {"active": True}}},
                   {"row": Row("ROW-LATER"), "stages": {"ADD-02": {"active": False}, "ADD-03": {"active": True}}}]}
    by_row = {"ROW-NOW": ["I-NOW"], "ROW-LATER": ["I-LATER"]}
    assert programme.issues_cited_in_force(r, by_row, "ADD-02") == {"I-NOW"}
    assert programme.issues_cited_in_force(r, by_row, "ADD-03") == {"I-NOW", "I-LATER"}
    assert programme.issues_cited_in_force(r, by_row, "ADD-09") == {"I-NOW", "I-LATER"}
