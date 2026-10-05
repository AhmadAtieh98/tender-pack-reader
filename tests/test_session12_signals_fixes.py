"""Session 12, fixer F2: the signal and page findings of the session-12 audit (A2-2, A2-3, A3-2, A3-3, A3-4).

A2-2 / A2-3 (one rule for every deliverable, signals.requirement_delta): a row is CONFIRMED (unchanged) at a stage only
when nothing it depends on changed at that stage: its own words, values, dates, parameters, status, consequence, the
units it cites, the units it depends on through the curated relationships (Table 2-4 for the effluent rows), the dates
that flow into it (an anchor date its units print), and no op of the stage adds an obligation to its units. A confirming
op on the row never hides such a change; a printed date that conflicts with the amended anchor is never confirmed.
A3-2 .. A3-4: every unresolved line on the one page carries the reason clause of its issue text; abbreviations are
written out; flags cite the id as listed on the page; a medium confidence points to its reason; the ambiguous window end
shows both readings. Real pack (the committed build) and small synthetic evaluations; nothing is written under the
repository and nothing is approved."""
from __future__ import annotations

import copy
import re
import unicodedata

import pymupdf
import pytest

from tenderpack import live, programme, schedule, signals, stage2
from tenderpack.render import A3OverflowError, write_a3_pdf
from tenderpack.util import ROOT

CONFIRMED = "CONFIRMED (unchanged)"


@pytest.fixture(scope="module")
def real():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


@pytest.fixture(scope="module")
def moved(real):
    return {(m["stage"], m["row"]): m for m in stage2.a2(real)["rows_moved"]}


# ---------------------------------------------------------------------------------------------- the predicate

def _ev(**kw):
    ev = {"status": "ACTIVE", "text": "x shall meet Table 9", "cells": None, "dates": [], "stale": [],
          "interpretation": {"stage": "BASE", "quote": "x shall meet Table 9", "consequence": "none_stated"},
          "depends": {"units": {"T:9/a": {"text": "a | Limit: 5", "cells": {"Limit": "5"}, "status": "active",
                                          "ops": [], "via": ["REL-1 (limit_applies, confirmed)"], "ref": "T 9/a"}},
                      "anchors": {}}}
    ev.update(kw)
    return ev


def test_a_dependency_that_changes_is_a_change_whatever_the_confirming_op():
    a = _ev()
    b = copy.deepcopy(a)
    b["interpretation"].update(stage="ADD-09", note="re-read, same words")
    b["depends"]["units"]["T:9/a"].update(text="a | Limit: 3", cells={"Limit": "3"}, ops=["ADD-09/5.1"])
    q = {"op": "ADD-09/Q1", "type": "annotate", "effect": "confirms", "provision": "ADD-09:Q1", "answer": False,
         "class": "confirms"}
    d = signals.requirement_delta(a, b, [q])
    assert d["changed"] and not d["confirmed"] and "dependency" in d["what"], d
    assert "T 9/a" in d["detail"] and "Limit 5 -> 3" in d["detail"] and "ADD-09/5.1" in d["detail"], d["detail"]
    assert "REL-1" in d["detail"]
    # nothing it depends on changed: the confirmation stands
    c = copy.deepcopy(a)
    c["interpretation"].update(stage="ADD-09", note="re-read, same words")
    assert signals.requirement_delta(a, c, [q])["confirmed"]


def test_a_printed_anchor_date_that_moved_is_a_change_and_a_conflict_is_never_confirmed():
    pr = lambda v, p: {"PDD": {"name": "Proposal Due Date", "value": v, "source": "VOL-I 6.1", "ops": [],  # noqa: E731
                               "printed": {"F:4-A/pdd": p}}}
    a = _ev(depends={"units": {}, "anchors": pr("2026-11-12", "2026-11-12")})
    b = copy.deepcopy(a)
    b["interpretation"].update(stage="ADD-01", note="reissued form, same words")
    b["depends"]["anchors"] = pr("2026-11-26", "2026-11-12")
    b["depends"]["anchors"]["PDD"].update(source="VOL-I 6.1 as amended by ADD-01 2.1", ops=["ADD-01/2.1"])
    d = signals.requirement_delta(a, b, [])
    assert d["changed"] and "anchor date" in d["what"], d
    assert "PDD moved 2026-11-12 -> 2026-11-26" in d["detail"] and "ADD-01 2.1" in d["detail"], d["detail"]
    assert "prints 2026-11-12" in d["detail"] and "CONFLICT" in d["detail"], d["detail"]
    # the anchor did not move at this stage but the printed date still conflicts: not confirmed, not settled
    c = copy.deepcopy(b)
    c["interpretation"].update(stage="ADD-02")
    d2 = signals.requirement_delta(b, c, [])
    assert not d2["confirmed"] and not d2["changed"] and d2["unsettled"] and "CONFLICT" in d2["detail"], d2


def test_an_added_obligation_alone_is_not_made_a_change():
    # blind-05 false signal 2 stays fixed: an annotation that adds an obligation (ADD-03/Q20 on VOL-I 6.2) does not by
    # itself make a re-read row CHANGED; it is named beside the confirmation for a person
    a = _ev()
    b = copy.deepcopy(a)
    b["interpretation"].update(stage="ADD-09", note="same words")
    adds = {"op": "ADD-09/5.2", "type": "annotate", "effect": "adds_obligation", "provision": "ADD-09:5.2",
            "answer": False, "class": "adds_obligation"}
    d = signals.requirement_delta(a, b, [adds])
    assert not d["changed"] and "ADD-09/5.2" in d["detail"], d


# ---------------------------------------------------------------------------------------------- A2 on the real pack

def test_a2_2_the_tn_rows_are_changed_with_the_cause_named(moved):
    for rid in ("VOL-II-3.1-01", "VOL-V-31.1-02", "VOL-V-29.3-01"):
        m = moved[("ADD-02", rid)]
        why = "; ".join(m["why"])
        assert m["change"] == "CHANGED", (rid, m)
        assert "VOL-II T2-4/TN" in why and "Limit 5 -> 3" in why and "ADD-02/5.1" in why, (rid, why)


def test_a2_3_the_reissued_form_4a_printed_date_is_changed_with_a_conflict(moved):
    m = moved[("ADD-01", "VOL-IV-F4A-01")]
    why = "; ".join(m["why"])
    assert m["change"] == "CHANGED", m
    assert "PDD moved 2026-11-12 -> 2026-11-26" in why and "ADD-01 2.1" in why, why
    assert "prints 2026-11-12" in why and "CONFLICT" in why, why


def test_no_confirmed_row_has_a_dependency_or_an_added_obligation_that_changed(real, moved):
    for (st, rid), m in moved.items():
        if m["change"] != CONFIRMED:
            continue
        e = next(x for x in real["evals"] if x["row"].id == rid)
        prev = real["order"][real["order"].index(st) - 1]
        assert not signals.dependency_changes(e["stages"][prev], e["stages"][st]), (st, rid)
        assert not signals.printed_conflicts(e["stages"][st]), (st, rid)


def test_the_programme_deltas_and_the_diff_use_the_same_rule(real):
    progs = {s: programme.stage_planner(real, s)(real["assumptions"]) for s in ("ADD-01", "ADD-02")}
    ea = {e["row"].id: e["stages"]["ADD-01"] for e in real["evals"]}
    eb = {e["row"].id: e["stages"]["ADD-02"] for e in real["evals"]}
    dl = schedule.deltas(progs["ADD-01"], progs["ADD-02"], ea, eb, answers=programme.answers_by_row(real, "ADD-02"))
    rework = " ".join(d["detail"] for d in dl if d["change"] == "REWORK")
    conf = " ".join(d["detail"] for d in dl if d["change"] == CONFIRMED)
    assert "VOL-II-3.1-01" in rework and "T2-4/TN" in rework, rework
    assert "VOL-II-3.1-01" not in conf
    md, data = live.diff(real, "ADD-01", "ADD-02")
    req = data["requirements"]
    for rid in ("VOL-II-3.1-01", "VOL-V-31.1-02"):
        assert rid in req["changed"] and rid not in req["confirmed"], rid
    md0, data0 = live.diff(real, "BASE", "ADD-01")
    assert "VOL-IV-F4A-01" in data0["requirements"]["changed"]
    assert "VOL-IV-F4A-01" not in data0["requirements"]["confirmed"]


# ---------------------------------------------------------------------------------------------- A3 page

@pytest.fixture(scope="module")
def page(real, tmp_path_factory):
    v = real["validated"].stage
    main = stage2.a5_all(real)[v]
    issues = stage2.collect_issues(real, main)
    a3 = stage2.a3(real, issues, main)
    out = tmp_path_factory.mktemp("s12f2")
    fit = level = None
    for level in range(stage2.A3_LEVELS + 1):
        try:
            cond = stage2.condense_a3(a3, level)
            fit = write_a3_pdf(cond, out / "a3.pdf")
            break
        except A3OverflowError:
            continue
    pg = pymupdf.open(out / "a3.pdf")[0]
    text = unicodedata.normalize("NFKC", pg.get_text())
    return {"a3": a3, "cond": cond, "fit": fit, "level": level, "text": " ".join(text.split()), "issues": issues}


def _listed(a3):
    return {i["id"]: i for g in a3["groups"]["groups"] for i in g["items"]}


def test_a3_2_every_unresolved_line_carries_its_reason(page):
    listed = _listed(page["cond"])
    expect = {"I-READING-T24": ["cut off"], "I-VOL-II-T24-TENSIONS": ["UV", "VOL-II 3.3"],
              "I-AUTO-COUNTING": ["ATTENDANCE-NOTICE", "conservative"],
              "I-A5-attendance-notice": ["incorrectly recorded", "ADD-01 3.1"],
              "I-VOL-I-FILE-NAMES": [".pdf"]}
    for iid, words in expect.items():
        s = listed[iid]["short"]
        for w in words:
            assert w in s, (iid, w, s)
            assert w in page["text"], (iid, w)
    for iid, i in listed.items():                     # never an id alone
        assert i["short"].strip() and i["short"].strip() != iid, iid


def test_a3_2_the_page_stays_one_page_at_no_smaller_font(page):
    fit = page["fit"]
    assert fit and fit["pages"] == 1
    assert fit["min_text_pt"] >= 7.72, fit                 # the reviewer measured 7.72 pt; never smaller


def test_a3_3_abbreviations_are_written_out_and_no_pipeline_terms(page):
    t = page["text"]
    for k, v in (("WD", "Working Day"), ("PDD", "Proposal Due Date"), ("PBN", "Preferred Bidder Notification"),
                 ("LCC", "Local Content Certificate")):
        assert f"{k} = {v}" in t, k
    assert "Validated state" not in t and "level 2" not in t and "(level" not in t
    assert "State after ADD-02" in t


def test_a3_3_flags_cite_the_id_listed_on_the_page(page):
    a3 = page["a3"]
    listed = set(_listed(a3))
    for s in a3["sections"]:
        for it in s["items"]:
            for f in it.get("flags") or []:
                for i in signals.issue_refs(f):
                    assert i in listed, (it["id"], i, f)
    six = next(i for s in a3["sections"] for i in s["items"] if i["id"] == "VOL-I-6.1-01")
    assert any("I-LCC-ISSUER" in f for f in six["flags"]), six["flags"]


def test_a3_4_the_window_end_shows_both_readings_and_medium_confidence_points_to_its_reason(page):
    s = _listed(page["cond"])["I-A5-attendance-notice"]["short"]
    assert "2026-10-14" in s and "2026-10-15" in s, s
    item = next(i for sec in page["a3"]["sections"] for i in sec["items"] if i["id"] == "VOL-I-6.2-02")
    assert "I-VOL-I-ENV-A-PRICES" in item["confidence"], item["confidence"]
    assert re.search(r"confidence medium \(see I-VOL-I-ENV-A-PRICES\)", page["text"]), page["text"][:300]
