"""Session 09, finding A: clarify.check() accepted (1) an entry with no sources and no decision owner, (2) an
"answered" response status with no evidence of the answer, and (3) a wrong clarification cut-off (never checked).

Reproduced first with in-memory register dicts (these regressions failed before the fix), then on the real register,
blind rehearsal 02 and the blind rehearsal 01 pack. Nothing is sent, answered, accepted or approved: the registers
are only read, and every change below is made to an in-memory copy.
"""
from __future__ import annotations

import copy

import pytest

from tenderpack import clarify, stage2
from tenderpack.cli import ingest
from tenderpack.util import load_yaml, ROOT

UNITS = [  # synthetic units in the pack's style (not tender content)
    {"unit_id": "VOL-I:5.2", "doc": "VOL-I", "pages": [3],
     "text": "Requests for clarification shall be submitted no later than ten (10) Working Days before the Proposal Due Date."},
    {"unit_id": "ADD-09:Q3", "doc": "ADD-09", "pages": [2],
     "text": "No: 3 | Bidder question: May copies be bound? | Authority response: Copies shall be bound in A4 binders."},
]
ENTRY = {"id": "CQ-SYN", "kind": "ambiguity", "volume": "Volume I", "clause": "5.2", "page": 3, "gap": "g",
         "practical_impact": "p", "proposed_question": "Volume I, Clause 5.2, page 3: ...", "interim_handling": "h",
         "decision_owner": "Bid manager", "response_status": "draft, not sent", "theme": "submission",
         "sources": [{"unit": "VOL-I:5.2", "page": 3, "words": "ten (10) Working Days before the Proposal Due Date"}]}
CUT = {"rule": "VOL-I 5.2", "date": "2026-11-12",
       "note": "Ten Working Days before the Proposal Due Date of 26 November 2026, 14:00 Riyadh time."}
EFFECTIVE = {"rule": "VOL-I 5.2", "rule_id": "CLARIFICATION-CUTOFF", "row": "VOL-I-5.2-01", "stage": "ADD-02",
             "date": "2026-11-12", "anchor": "PDD", "conflicts": [],
             "pdd": {"date": "2026-11-26", "time": "14:00", "tz": "Riyadh time", "unit": "VOL-I:6.1"}}


def _reg(cut=CUT, **changes) -> dict:
    entry = {**copy.deepcopy(ENTRY), **changes}
    for k in [k for k, v in changes.items() if v is None]:
        entry.pop(k)
    return {"cut_off": dict(cut), "clarifications": [entry]}


def _check(reg, cutoff=None):
    return clarify.check(reg, UNITS, set(), cutoff=cutoff)


# ---------------------------------------------------------------------------------------------- in memory

def test_a_complete_draft_entry_and_the_right_cut_off_pass():
    assert _check(_reg(), EFFECTIVE) == []


def test_an_entry_without_sources_or_decision_owner_is_a_finding():
    found = _check(_reg(sources=[], decision_owner=None))
    assert any("missing ['decision_owner']" in f for f in found), found
    assert any("no sources" in f for f in found), found
    assert any("no sources" in f for f in _check(_reg(sources=None))), "a missing sources key is a finding too"


@pytest.mark.parametrize("status", ["answered", "sent", "pending", "Draft, not sent", "", None, "answered by Addendum"])
def test_any_response_state_outside_the_three_is_unknown(status):
    found = _check(_reg(response_status=status))
    assert any("unknown response state" in f for f in found), (status, found)


def test_answered_needs_answer_evidence_and_says_how_an_answer_is_evidenced():
    found = _check(_reg(response_status="answered"))
    assert any("unknown response state" in f and "evidence-backed only" in f for f in found), found
    found = _check(_reg(response_status="answered by addendum"))                      # no answer at all
    assert any("without answer evidence" in f and "evidence-backed only" in f for f in found), found
    half = {"unit": "ADD-09:Q3", "page": 2}                                            # no words
    assert any("without answer evidence" in f for f in _check(_reg(response_status="answered by addendum", answer=half)))


def test_an_answer_must_quote_an_addendum_unit_verbatim_on_its_page():
    ok = {"unit": "ADD-09:Q3", "page": 2, "words": "Copies shall be bound in A4 binders."}
    assert _check(_reg(response_status="answered by addendum", answer=ok)) == []
    volume = {"unit": "VOL-I:5.2", "page": 3, "words": "ten (10) Working Days"}
    assert any("not a unit of an Addendum" in f and "evidence-backed only" in f
               for f in _check(_reg(response_status="answered by addendum", answer=volume)))
    invented = {**ok, "words": "Copies may be stapled."}
    assert any("not verbatim" in f for f in _check(_reg(response_status="answered by addendum", answer=invented)))
    wrong_page = {**ok, "page": 3}
    assert any("not p3" in f for f in _check(_reg(response_status="answered by addendum", answer=wrong_page)))
    missing = {**ok, "unit": "ADD-09:Q99"}
    assert any("does not exist" in f for f in _check(_reg(response_status="answered by addendum", answer=missing)))


def test_an_answer_recorded_under_an_unanswered_status_is_a_finding():
    ok = {"unit": "ADD-09:Q3", "page": 2, "words": "Copies shall be bound in A4 binders."}
    assert any("an answer is recorded" in f for f in _check(_reg(answer=ok)))
    assert _check(_reg(response_status="withdrawn (not sent)")) == []


def test_a_wrong_cut_off_date_or_time_is_a_finding():
    found = _check(_reg(cut={**CUT, "date": "2026-11-13"}), EFFECTIVE)
    assert any(f.startswith("cut_off: date 2026-11-13 is not the effective cut-off 2026-11-12") for f in found), found
    found = _check(_reg(cut={**CUT, "note": "Ten Working Days before the Proposal Due Date."}), EFFECTIVE)
    assert any("does not state the effective PDD time 14:00" in f for f in found), found
    found = _check(_reg(cut={**CUT, "note": CUT["note"] + " Lodge requests before 11:00."}), EFFECTIVE)
    assert any("states ['11:00'], not the effective PDD time 14:00" in f for f in found), found
    assert any(f.startswith("cut_off: missing") for f in _check({"clarifications": [copy.deepcopy(ENTRY)]}, EFFECTIVE))
    assert any("not computed" in f for f in _check(_reg(), {**EFFECTIVE, "date": None}))
    assert any("no row defines" in f for f in _check(_reg(), {**EFFECTIVE, "row": None}))
    # without the effective cut-off (an older caller) the date is not checked: stage2 always passes it
    assert _check(_reg(cut={**CUT, "date": "2026-11-13"})) == []


# ---------------------------------------------------------------------------------------------- the packs

def _usable(evidence, pack):
    return evidence.exists() and not stage2.load_evidence(evidence, ROOT)[1]


@pytest.fixture(scope="module")
def real():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


def _rehearsal(name, tmp_path_factory):
    """The rehearsal's own build when it is current (it is not committed), else a fresh ingest into a tmp dir."""
    pack, evidence = ROOT / f"rehearsals/{name}/work/pack.yaml", ROOT / f"rehearsals/{name}/build"
    if not _usable(evidence, pack):
        evidence = tmp_path_factory.mktemp(name) / "build"
        assert ingest(pack, evidence, ROOT, quiet=True)["exit_code"] == 0
    return stage2.run(evidence, pack, ROOT)


@pytest.fixture(scope="module")
def blind02(tmp_path_factory):
    return _rehearsal("blind-02", tmp_path_factory)


def _clar(r):
    return [f for f in stage2.register_findings(r) if f["kind"] == "clarification"]


def test_the_real_register_is_clean_against_the_effective_cut_off(real):
    eff = clarify.effective_cutoff(real)
    assert (eff["stage"], eff["row"], eff["rule"], eff["date"]) == ("ADD-02", "VOL-I-5.2-01", "VOL-I 5.2", "2026-11-12")
    assert (eff["pdd"]["date"], eff["pdd"]["time"], eff["pdd"]["tz"]) == ("2026-11-26", "14:00", "Riyadh time")
    reg = real["clarifications"]
    assert reg["cut_off"]["date"] == eff["date"] and "14:00" in reg["cut_off"]["note"]
    assert clarify.check(reg, real["units"], set(real["curated_issues"]), cutoff=eff) == []
    assert _clar(real) == []                                              # check-register and the gate: 0 findings
    assert all(c["response_status"] == "draft, not sent" and c["decision_owner"] and c["sources"]
               for c in reg["clarifications"])                            # unknown answers stay unknown


def test_the_cut_off_is_derived_the_same_way_without_stage2s_anchor_details(real):
    r = copy.copy(real)
    r.pop("anchor_details", None)
    eff = clarify.effective_cutoff(r)
    assert (eff["date"], eff["pdd"]["date"], eff["pdd"]["time"], eff["pdd"]["tz"]) == \
        ("2026-11-12", "2026-11-26", "14:00", "Riyadh time")


def test_check_register_and_the_release_gate_use_the_effective_cut_off(real):
    r = copy.copy(real)
    r["clarifications"] = copy.deepcopy(real["clarifications"])
    r["clarifications"]["cut_off"]["date"] = "2026-11-13"
    found = _clar(r)
    assert [f["where"] for f in found] == ["cut_off"] and "2026-11-12" in found[0]["detail"]
    assert any(b["kind"] == "coverage" and "cut_off" in b["detail"] for b in stage2.release_blockers(r))
    r["clarifications"]["cut_off"] = {**real["clarifications"]["cut_off"],
                                      "note": real["clarifications"]["cut_off"]["note"].replace("14:00", "11:00")}
    assert any("11:00" in f["detail"] and "14:00" in f["detail"] for f in _clar(r))


def test_blind_02_register_follows_its_amended_proposal_due_date_time(blind02):
    eff = clarify.effective_cutoff(blind02)
    assert (eff["stage"], eff["date"], eff["pdd"]["date"], eff["pdd"]["time"]) == ("ADD-03", "2026-11-12", "2026-11-26", "11:00")
    assert "ADD-03 2.1" in (eff["pdd"].get("source") or "ADD-03 2.1")
    assert _clar(blind02) == []
    stale = copy.deepcopy(blind02["clarifications"])                      # the time before ADD-03 moved it
    stale["cut_off"]["note"] = stale["cut_off"]["note"].replace("11:00", "14:00")
    found = clarify.check(stale, blind02["units"], set(blind02["curated_issues"]), cutoff=eff)
    assert any("does not state the effective PDD time 11:00" in f for f in found), found


def test_blind_01_cut_off_is_computed_from_its_moved_due_date_not_assumed(tmp_path_factory):
    """Blind 01's ADD-03 moved the Proposal Due Date to 10 December 2026 and the 5.2 period to fifteen Working Days,
    so its cut-off is 19 November 2026, computed from the effective text. The pack has its own register copy
    (session 09) carrying that date; the real register's 12 November, read against this pack, is reported."""
    r = _rehearsal("blind-01", tmp_path_factory)
    eff = clarify.effective_cutoff(r)
    assert (eff["stage"], eff["pdd"]["date"], eff["pdd"]["time"], eff["date"]) == ("ADD-03", "2026-12-10", "14:00", "2026-11-19")
    assert r["clarifications"]["cut_off"]["date"] == "2026-11-19" and "19 November 2026" in r["clarifications"]["cut_off"]["note"]
    assert not [f for f in _clar(r) if f["where"] == "cut_off"]
    real = load_yaml(ROOT / "curation/clarifications/register.yaml")
    wrong = clarify.check(real, r["units"], set(r["curated_issues"]), cutoff=eff)
    assert any("2026-11-12" in f and "2026-11-19" in f for f in wrong)