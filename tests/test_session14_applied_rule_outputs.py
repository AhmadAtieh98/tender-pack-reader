"""Session 14 (W4), part 3 (a) and (d): human ownership accurate on the register/output side (report section 9 L27;
blind-07 COMPARISON.md section 5 "Over-escalated").

(a) An issue whose point an explicit and unambiguous document rule settles is re-presented by the controller
    (controller.re_present_issue, W1's side) with `applied_rule` (the clause's words, "applied, not decided") and
    `confirm` ("applied rule: <clause words>; a person confirms the application"). The outputs used to label it
    HUMAN DECISION PENDING (proposed by the AI workflow) like any open judgment. Now it reads
    "PROPOSED BASIS (applied rule; a person confirms the application)" with its owner kept, and the rows it is linked
    to stay NOT SETTLED with 'applied rule awaiting a person's confirmation' (never CONFIRMED) until a person accepts it.
    Genuine judgments keep HUMAN DECISION PENDING: a proposed status or resolution, a pending decision of the
    clarification register naming it, or its own remaining words asserting a judgment.
(d) Nothing the owner has not decided becomes decided: the curated pending issues (the 'at all times' reading, the
    maxima/ranges, the Permit, the concession term, the compliance point) stay HUMAN DECISION PENDING in the real
    pack; the owner's transcription approvals are not interpretation approvals (no curated issue or row reads as
    decided because an image reading is approved)."""
from __future__ import annotations

import pytest

from tenderpack import human_owned as H
from tenderpack import signals, stage2
from tenderpack.util import ROOT

APPLIED = {"text": "applied rule: ADD-09 3.5 'The Arabic text governs.'; a person confirms the application ADD-09 3.5 "
                   "provides: 'The Arabic text governs.' (applied, not decided) Rows 4 and 5 follow the Arabic.",
           "owner": "Legal", H.MARKER: True,
           "applied_rule": ["ADD-09 3.5 provides: 'The Arabic text governs.' (applied, not decided)"],
           "confirm": ["applied rule: ADD-09 3.5 'The Arabic text governs.'; a person confirms the application"]}


def test_an_applied_rule_issue_shows_the_proposed_basis_not_human_decision_pending():
    lab = H.issue_label("I-X", APPLIED, [])
    assert lab.startswith(H.PROPOSED_BASIS) and H.HUMAN_DECISION_PENDING not in lab, lab
    assert H.pending_reasons("I-X", APPLIED, []) == []
    assert H.awaiting_confirmation("I-X", APPLIED, []) == APPLIED["confirm"]
    # the owner is kept
    assert APPLIED["owner"] == "Legal"


def test_a_genuine_judgment_beside_the_rule_stays_pending():
    for extra in ({"resolution": "the Arabic governs"},                         # a proposed resolution
                  {"text": APPLIED["text"] + " Which class an asset in both classes takes is to be read as mechanical."}):
        it = dict(APPLIED, **extra)
        assert H.issue_label("I-X", it, []).startswith(H.HUMAN_DECISION_PENDING), it
        assert H.pending_reasons("I-X", it, [])
    # a pending decision of the clarification register names it
    assert H.issue_label("I-X", APPLIED, [], ["which rendering governs"]).startswith(H.HUMAN_DECISION_PENDING)
    # without `confirm` (no applied rule) a model's issue stays HUMAN DECISION PENDING as before
    plain = {k: v for k, v in APPLIED.items() if k not in ("applied_rule", "confirm")}
    assert H.issue_label("I-X", plain, []).startswith(H.HUMAN_DECISION_PENDING)


def test_rows_under_an_applied_rule_are_not_settled_with_the_confirmation_named():
    r = {"curated_issues": {"I-X": APPLIED}, "decisions": [], "clarifications": {}, "order": ["BASE", "ADD-09"],
         "evals": []}
    assert signals.pending_issues(r) == {}
    aw = signals.awaiting_issues(r)
    assert list(aw) == ["I-X"]
    a = {"text": "x", "cells": None, "dates": [], "status": "ACTIVE", "active": True, "interpretation": None,
         "stale": [], "pending": [signals.awaiting_note("I-X")]}
    c = {"op": "ADD-09/3.5", "type": "annotate", "effect": "confirms", "provision": "ADD-09:3.5", "accepted": False}
    d = signals.requirement_delta(dict(a, pending=[]), a, [c])
    assert d["unsettled"] and "applied rule awaiting a person's confirmation" in d["detail"], d


def test_attach_pending_puts_the_awaiting_note_on_linked_rows():
    class Row:
        id, issues = "R-1", ["I-X"]
    ev = {"BASE": {}, "ADD-09": {}}
    r = {"curated_issues": {"I-X": APPLIED}, "decisions": [], "clarifications": {}, "order": ["BASE", "ADD-09"],
         "evals": [{"row": Row(), "stages": ev}]}
    signals.attach_pending(r)
    assert ev["ADD-09"]["pending"] == ["open: I-X, applied rule awaiting a person's confirmation"]


@pytest.fixture(scope="module")
def real():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


def test_the_owners_open_decisions_stay_pending_in_the_real_pack(real):
    pend = real["pending_issues"]
    for i in ("I-VOL-II-AT-ALL-TIMES", "I-VOL-II-T24-TENSIONS", "I-PERMIT", "I-CONCESSION",
              "I-VOL-II-COMPLIANCE-POINT"):
        assert i in pend, i
    labels = {x["id"]: x.get("human_decision") for x in stage2.collect_issues(real, None)}
    for i in ("I-VOL-II-AT-ALL-TIMES", "I-VOL-II-T24-TENSIONS", "I-PERMIT", "I-CONCESSION"):
        assert labels.get(i) == H.HUMAN_DECISION_PENDING, (i, labels.get(i))
    # no curated issue is re-presented as an applied rule in the real pack (nothing of the owner's is settled here)
    assert not any(it.get("applied_rule") for it in real["curated_issues"].values())


def test_an_approved_transcription_is_never_an_interpretation_approval(real):
    states = stage2.row_states(real)
    for e in real["evals"]:
        v = e["stages"][real["validated"].stage]
        if v.get("transcription") == "approved":
            ap = states[e["row"].id]["approval"]
            assert "not an approval of the interpretation" in ap, (e["row"].id, ap)
            assert "accepted by" not in ap.split("row:")[1].split(";")[0], (e["row"].id, ap)   # no row decision exists
    # the review label of every row stays 'proposed (not reviewed)': no decisions file exists (an approval of a reading
    # is recorded in approvals.yaml and is never read as a row or issue decision)
    assert not any(st["status"] == "accepted" for (k, _), st in real["reviews"].items() if k in ("row", "issue"))
