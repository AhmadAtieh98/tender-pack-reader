"""Session 14 (W4), part 4: unchanged table values are kept apart from unresolved interpretation and approval status.

A Table 2-4 value can be unchanged at ADD-02 while its interpretation is pending (I-PERMIT, the compliance point, the
maxima/ranges) and no person has approved the row, the op that re-reads it or anything but the transcription of the
image. The three are shown apart (stage2.row_states: value / interpretation / approval) in A1's columns and on the
review cards, and nothing is called CONFIRMED on the value alone:
  * a confirming op that no person accepted is named as such in a CONFIRMED line ('proposed op ... (awaiting a
    person's acceptance)'), as the NOT SETTLED lines already did;
  * the owner's approval of an image reading's transcription is never shown as an approval of the interpretation."""
from __future__ import annotations

import pytest

from tenderpack import batches, signals, stage2
from tenderpack.util import ROOT


@pytest.fixture(scope="module")
def real():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


@pytest.fixture(scope="module")
def states(real):
    return stage2.row_states(real)


@pytest.fixture(scope="module")
def a1(real):
    return {x["id"]: x for x in stage2.a1_table(real, stage2.collect_issues(real, None))["rows"]}


def test_confirmed_line_names_an_unaccepted_confirming_op_synthetic():
    a = {"text": "x", "cells": None, "dates": [], "status": "ACTIVE", "active": True, "interpretation": None,
         "stale": [], "pending": []}
    c = {"op": "ADD-9/Q1", "type": "annotate", "effect": "confirms", "provision": "ADD-9:Q1", "accepted": False}
    d = signals.requirement_delta(a, dict(a), [c])
    assert d["confirmed"] and ("confirmed by ADD-9/Q1 (confirms; ADD-9:Q1) (proposed op, awaiting a person's "
                               "acceptance)") in d["detail"], d
    d = signals.requirement_delta(a, dict(a), [dict(c, accepted=True)])
    assert d["confirmed"] and "confirmed by ADD-9/Q1 (confirms; ADD-9:Q1)" in d["detail"], d
    assert "awaiting" not in d["detail"], d


def test_three_states_for_an_unchanged_table_2_4_value(states):
    s = states["VOL-II-T2-4-BOD5"]
    assert s["value"].startswith("unchanged since BASE"), s["value"]
    assert "Limit: 10" in s["value"] and "CONFIRMED" not in s["value"]
    assert "ADD-02/5.1/unchanged" in s["value"]                       # the re-reading op is named with the value
    assert "HUMAN DECISION PENDING" in s["interpretation"]
    for i in ("I-PERMIT", "I-VOL-II-COMPLIANCE-POINT"):
        assert i in s["interpretation"], s["interpretation"]
    ap = s["approval"]
    assert "transcription approved" in ap and "not an approval of the interpretation" in ap, ap
    assert "row: proposed (not reviewed)" in ap and "ADD-02/5.1/unchanged: proposed (not reviewed)" in ap, ap


def test_range_row_carries_the_maxima_issue_and_tn_shows_its_change(states):
    assert "I-VOL-II-T24-TENSIONS" in states["VOL-II-T2-4-ResidualChlorine"]["interpretation"]
    tn = states["VOL-II-T2-4-TN"]
    assert tn["value"].startswith("changed at ADD-02 by ADD-02/5.1"), tn["value"]
    assert "ADD-02/5.1: proposed (not reviewed)" in tn["approval"]


def test_a_text_layer_row_has_no_transcription_approval(states):
    ap = states["VOL-I-6.4-01"]["approval"]
    assert "transcription" not in ap and ap.startswith("row: proposed (not reviewed)"), ap


def test_a1_shows_the_three_columns(real, a1):
    cols = [c["key"] for c in stage2.a1_table(real, stage2.collect_issues(real, None))["columns"]]
    for k in ("value_state", "interpretation_state", "approval_state"):
        assert k in cols
    row = a1["VOL-II-T2-4-BOD5"]
    assert row["value_state"].startswith("unchanged since BASE")
    assert "HUMAN DECISION PENDING" in row["interpretation_state"]
    assert "not an approval of the interpretation" in row["approval_state"]


def test_card_block_shows_the_three_apart(states):
    h = batches.states_block_html(states["VOL-II-T2-4-BOD5"])
    for w in ("Value", "Interpretation", "Approval", "unchanged since BASE", "HUMAN DECISION PENDING",
              "not an approval of the interpretation"):
        assert w in h, w
    assert batches.states_block_html(None) == ""
