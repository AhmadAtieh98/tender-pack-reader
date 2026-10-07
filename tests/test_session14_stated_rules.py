"""Session 14 (W1; blind-07 COMPARISON §8 defect 11, report §9 L27): an explicit and unambiguous document rule can SUPPORT
a proposed candidate change, applied and not decided, while a genuine ambiguity stays a person's.

blind-07: analysis items that declined a STATED rule were handed to a person: the addendum's own "The Arabic text
governs" (ten analysis items: "which value applies is for a person"), the operative text over the cover summary under
VOL-I 3.2, and an "as amended by" recital (1.2); the controller's rule application read only issues and escalations.
Now every analysis item (an op, a disposition, a row too) is read the same way, and an item's declared missing
information or conflict that is a point a stated rule settles no longer holds the change back: it is recorded as an
applied rule ("<clause> provides: '<words>' (applied, not decided)"; "a person confirms the application"), the item stays
at most interpretation_pending, and nothing is approved. A genuine ambiguity (two readings of the same words), the
closing of a rule's own exception, and a point the rule does not name stay human-owned: neither a valid quotation of the
rule nor a model's agreement settles an ambiguous point. Synthetic texts (blind-07 style) and the blind-02 pack."""
from __future__ import annotations

import pytest

from ai_fixture import workspace
from tenderpack.ai.controller import APPLIED_RULE, CONFIRM, applied_rule_review
from tenderpack.ai.tools import call_tool

TEXTS = {"ADD-03:3.5": "Table 42-1 is issued in the Arabic language. The Arabic text governs. The English translation "
                       "at Appendix B is provided for convenience only.",
         "ADD-03:T42-1/4": "No: 4 | Asset class: Electrical equipment | Minimum residual life (years): 5",
         "ADD-03:1.2": "A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as "
                       "amended by Addenda Nos. 1 and 2, unless otherwise stated.",
         "ADD-03:2.1": "The amount stated in Volume V Clause 36.2 is reduced by SAR 1,000,000."}
PROVS = ["ADD-03:1.2", "ADD-03:2.1", "ADD-03:3.5", "ADD-03:T42-1/4"]


def test_a_disposition_declining_the_addendums_own_governing_language_rule_is_applied_not_decided():
    d = {"disposition": "unresolved", "reason": "English row 4 shows 5 years; Arabic row 4 shows 7. Translation is for "
                                                "convenience only per clause 3.5; which value applies is for a person "
                                                "(Legal/Technical)."}
    r = applied_rule_review("disposition", d, "ADD-03:T42-1/4", TEXTS, "ADD-03", PROVS)
    assert r["lines"] == ["ADD-03 3.5 provides: 'The Arabic text governs.' (applied, not decided)"], r
    assert r["human"] == [] and r["confirm"] and CONFIRM in r["confirm"][0]


def test_an_as_amended_by_recital_settles_which_version_a_reference_means():
    d = {"disposition": "unresolved", "reason": "Which base the reduction applies to (the amount as issued or the amount "
                                                "as amended by Addendum No. 2) is a person's decision."}
    r = applied_rule_review("disposition", d, "ADD-03:2.1", TEXTS, "ADD-03", PROVS)
    assert len(r["lines"]) == 1 and r["lines"][0].startswith("ADD-03 1.2 provides: 'A reference in this Addendum"), r
    assert "(applied, not decided)" in r["lines"][0]


def test_closing_the_recitals_own_exception_stays_a_persons_judgment():
    d = {"disposition": "unresolved", "reason": "The cover states a different figure, so the exception (unless otherwise "
                                                "stated) may apply; which base applies is a person's decision."}
    r = applied_rule_review("disposition", d, "ADD-03:2.1", TEXTS, "ADD-03", PROVS)
    assert r["lines"] == [], r["lines"]


def test_a_quotation_alone_never_settles_an_ambiguous_point():
    from tenderpack.ai.controller import settled_handoff
    two = ("The Arabic words for row 4 can be read as the electrical equipment only or as the instrumentation too; "
           "which rendering governs")
    assert settled_handoff(two, "ADD-03:T42-1/4", TEXTS, "ADD-03", PROVS) is None
    assert settled_handoff("Which rendering of Table 42-1 row 4 governs", "ADD-03:T42-1/4", TEXTS, "ADD-03",
                           PROVS).startswith("ADD-03 3.5 provides: 'The Arabic text governs.'")
    # a point on another table is never applied by a clause about Table 42-1
    assert settled_handoff("Which rendering of Table 5-1 governs", "ADD-03:2.1", TEXTS, "ADD-03", PROVS) is None


# ---------------------------------------------------------------------------------------------- through the controller

Q21 = {"doc": "ADD-03", "unit_id": "ADD-03:2.1", "page": 1, "kind": "span",
       "words": "‘14:00 hours Riyadh time’ is deleted and ‘11:00 hours Riyadh time’ is substituted"}
V32 = {"doc": "VOL-I", "unit_id": "VOL-I:3.2", "page": 2, "kind": "span",
       "words": "the following order of precedence shall apply, the first named prevailing"}


@pytest.fixture(scope="module")
def ws(request, tmp_path_factory):
    return workspace(tmp_path_factory.mktemp("s14-rules"), evidence=request.getfixturevalue("blind02_build"))


def _op(st, missing, evidence=(Q21,)):
    return {"id": "ADD-03/2.1", "state": st, "statement_type": "amendment_op", "provision": "ADD-03:2.1",
            "target": "VOL-I:6.1", "payload": {"type": "replace_text", "target": "VOL-I:6.1",
                                               "old": "14:00 hours Riyadh time", "new": "11:00 hours Riyadh time"},
            "evidence": list(evidence), "missing_information": [missing]}


def _one(ws, item):
    st = ws.identity().model_dump()
    res = call_tool(ws, "validate_proposal", {"proposal": {"addendum": "ADD-03", "state": st,
                                                           "items": [dict(item, state=st)]}}, "model")
    return res["items"][0]


def test_a_stated_rule_supports_the_change_the_item_held_back(ws):
    st = ws.identity().model_dump()
    x = _one(ws, _op(st, "The cover summary describes this change differently from Section 2.1; which text governs"))
    assert x["verification_status"] == "interpretation_pending", x["validation"]       # promotable, never approved
    rec = [v for v in x["validation"] if v["check"] == APPLIED_RULE]
    assert rec and rec[0]["ok"] and "VOL-I 3.2 provides" in rec[0]["detail"], x["validation"]
    assert "(applied, not decided)" in rec[0]["detail"] and CONFIRM in rec[0]["detail"]
    assert not [v for v in x["validation"] if v["check"] == "missing_information" and not v["ok"]]


def test_a_valid_quotation_of_the_rule_does_not_settle_two_readings(ws):
    st = ws.identity().model_dump()
    x = _one(ws, _op(st, "The cover can be read as moving the time to 10:00 or to 11:00; which text governs",
                     evidence=(Q21, V32)))
    assert all(v["ok"] for v in x["validation"] if v["check"] == "evidence"), x["validation"]   # the quote is valid
    assert x["verification_status"] == "insufficient_evidence", x["validation"]
    assert not [v for v in x["validation"] if v["check"] == APPLIED_RULE]


def test_a_disposition_handing_over_a_settled_point_is_recorded_as_an_applied_rule(ws):
    st = ws.identity().model_dump()
    d = {"id": "ADD-03/2.1/disp", "state": st, "statement_type": "disposition", "provision": "ADD-03:2.1",
         "payload": {"disposition": "unresolved",
                     "reason": "The cover summary says otherwise than Section 2.1; which text governs is a person's "
                               "decision."}, "evidence": [Q21]}
    x = _one(ws, d)
    rec = [v for v in x["validation"] if v["check"] == APPLIED_RULE]
    assert rec and "(applied, not decided)" in rec[0]["detail"] and CONFIRM in rec[0]["detail"], x["validation"]
    assert x["verification_status"] == "interpretation_pending"          # an unresolved answer stays pending
