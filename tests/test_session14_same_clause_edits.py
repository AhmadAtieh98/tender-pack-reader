"""Session 14 (W1; blind-07 COMPARISON §8 defects 2 and 4, report §9 L22): disjoint edits to the same clause, annotate
with plural targets, and previous values checked against the previous EFFECTIVE target.

blind-07: 3.3 and 3.4 replaced two disjoint spans of VOL-V 42.1 and were held `conflicting` ("change the same unit in
different ways"); the `annotate` answers Q15-Q17 (plural `targets`, no `target`) were refused with "no target to compare
the previous value ... with". The scorer suggested comparing an answer's previous_value with the answer's own text; the
OWNER's rule overrides it: a previous_value is always checked against the previous effective target (the target's text
at the validated stage, after the earlier addenda), never against the new answer's own text. Synthetic items on the
blind-02 rehearsal pack: its ADD-03 5.3 prints two changes to VOL-II 8.4 (a figure and the second sentence)."""
from __future__ import annotations

import pytest

from ai_fixture import workspace
from tenderpack.ai.tools import call_tool

Q53 = {"doc": "ADD-03", "unit_id": "ADD-03:5.3", "page": 2, "kind": "span",
       "words": "‘22% dry solids’ is deleted and ‘25% dry solids’ is substituted, and the second sentence is deleted"}
FIGURE = ("22% dry solids", "25% dry solids")
SENTENCE = ("Disposal to landfill of sludge exceeding 500 tonnes per annum shall require the Authority's prior written "
            "consent.", "No sludge shall be disposed of to landfill without the Authority's prior written consent.")
Q17 = {"doc": "ADD-03", "unit_id": "ADD-03:Q17", "page": 2, "kind": "span",
       "words": "The response to clarification request 10 in Addendum No. 2 is confirmed."}
OWN = "Volume I Clause 8.7 requires a Parent Company Guarantee in respect of the proposed EPC Contractor only"
VOL_I_87 = "The Bidder shall submit an executed Parent Company Guarantee from the ultimate parent company"


@pytest.fixture(scope="module")
def ws(request, tmp_path_factory):
    return workspace(tmp_path_factory.mktemp("s14-edits"), evidence=request.getfixturevalue("blind02_build"))


def _rt(st, iid, old, new, located=False):
    return {"id": iid, "state": st, "statement_type": "amendment_op", "provision": "ADD-03:5.3", "target": "VOL-II:8.4",
            "payload": {"id": iid, "type": "replace_text", "target": "VOL-II:8.4", "old": old, "new": new,
                        **({"old_resolved": "matched_in_target"} if located else {})},
            "evidence": [Q53, {"doc": "VOL-II", "unit_id": "VOL-II:8.4", "page": 5, "kind": "span", "words": old}]}


def _validate(ws, items):
    st = ws.identity().model_dump()
    res = call_tool(ws, "validate_proposal", {"proposal": {"addendum": "ADD-03", "state": st,
                                                           "items": [dict(i, state=st) for i in items]}}, "model")
    return {x["id"]: x for x in res["items"]}


def _failed(x, check):
    return [v["detail"] for v in x["validation"] if v["check"] == check and not v["ok"]]


def test_two_replacements_on_disjoint_spans_of_one_clause_are_both_valid(ws):
    st = ws.identity().model_dump()
    # (b)'s old words are the target's second sentence, located in the target (the provision does not quote them)
    got = _validate(ws, [_rt(st, "ADD-03/5.3(a)", *FIGURE), _rt(st, "ADD-03/5.3(b)", *SENTENCE, located=True)])
    assert got["ADD-03/5.3(a)"]["verification_status"] == "evidence_verified", got["ADD-03/5.3(a)"]["validation"]
    assert got["ADD-03/5.3(b)"]["verification_status"] == "interpretation_pending", got["ADD-03/5.3(b)"]["validation"]
    for k in ("ADD-03/5.3(a)", "ADD-03/5.3(b)"):
        assert not _failed(got[k], "consistency") and not _failed(got[k], "engine (C21-C27)"), got[k]["validation"]


def test_overlapping_spans_stay_rejected(ws):
    st = ws.identity().model_dump()
    got = _validate(ws, [_rt(st, "ADD-03/5.3(a)", *FIGURE),
                         _rt(st, "ADD-03/5.3(x)", "not less than 22% dry solids", "25% dry solids",
                             located=True)])
    # rejected both ways: the consistency check holds (a), and the engine applying them in order finds (x)'s words gone
    assert got["ADD-03/5.3(a)"]["verification_status"] == "conflicting" and _failed(got["ADD-03/5.3(a)"], "consistency")
    assert got["ADD-03/5.3(x)"]["verification_status"] in ("conflicting", "invalid"), got["ADD-03/5.3(x)"]


def test_a_replacement_that_writes_what_the_other_reads_stays_rejected(ws):
    st = ws.identity().model_dump()
    got = _validate(ws, [_rt(st, "ADD-03/5.3(a)", *FIGURE),
                         _rt(st, "ADD-03/5.3(y)", "applicable regulations", "22% dry solids",
                             located=True)])
    # both are valid in the dry run alone (each new text is printed by 5.3); together they depend on their order
    assert all(got[k]["verification_status"] == "conflicting" and _failed(got[k], "consistency")
               for k in ("ADD-03/5.3(a)", "ADD-03/5.3(y)")), got


def _annotate(st, targets, pv, effect="confirms"):
    return {"id": "ADD-03/Q17", "state": st, "statement_type": "amendment_op", "provision": "ADD-03:Q17",
            "payload": {"type": "annotate", "targets": targets, "effect": effect,
                        "note": "Q17 confirms ADD-02 response 10 and VOL-I 8.7"},
            "previous_value": pv, "evidence": [Q17]}


def test_an_annotation_with_plural_targets_checks_the_previous_value_against_each_target(ws):
    st = ws.identity().model_dump()
    got = _validate(ws, [_annotate(st, ["ADD-02:Q10", "VOL-I:8.7"], VOL_I_87)])["ADD-03/Q17"]
    rec = [v for v in got["validation"] if v["check"] == "previous_value"]
    assert rec and rec[0]["ok"] and "VOL-I:8.7" in rec[0]["detail"], got["validation"]
    assert got["verification_status"] != "invalid", got["validation"]


def test_a_previous_value_quoting_the_answers_own_new_text_fails(ws):
    """The owner's rule: never compared with the new answer's own text, even when the answer is among its targets."""
    st = ws.identity().model_dump()
    for targets in (["ADD-02:Q10", "VOL-I:8.7"], ["ADD-03:Q17", "VOL-I:8.7"], ["ADD-03:Q17"]):
        got = _validate(ws, [_annotate(st, targets, OWN)])["ADD-03/Q17"]
        bad = _failed(got, "previous_value")
        assert got["verification_status"] == "invalid" and bad, (targets, got["validation"])
        assert "answer's own text" in bad[0], bad
