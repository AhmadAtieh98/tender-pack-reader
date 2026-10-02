"""Drill B (session 05): a second synthetic Addendum No. 3 through the same path, as in the live session.

It holds two changes in one paragraph (2.1), a new obligation with a consequence (3.1), an image-table change
(4.1, Table 2-4 TSS, a reading), two change types not seen in ADD-01/ADD-02 (5.1 a whole clause deleted and
replaced; 6.1 a new clause inserted) and two answers (Q15 quotes a replaced figure; Q16 cites an unchanged
clause). The rehearsal (tests/fixtures/drill_b/rehearse.py) builds and ingests it, publishes the drafted working
draft, applies the curation in a copy of the register, and publishes again. In this disposable copy only,
"Fixture Test Reviewer" approves the Table 2-4 reading and accepts two rows first, to show what happens to an
earlier approved state. Nothing is approved in the repository.
"""
from __future__ import annotations

import json
import sys

import pytest

from tenderpack.util import ROOT

sys.path.insert(0, str(ROOT / "tests/fixtures/drill_b"))
import rehearse  # noqa: E402


@pytest.fixture(scope="module")
def drill(tmp_path_factory):
    root = tmp_path_factory.mktemp("drillb")
    res = rehearse.rehearse(root, fixture_review=True)
    load = lambda p: json.loads((root / p).read_text(encoding="utf-8"))  # noqa: E731
    return {"root": root, "res": res, "load": load}


def st(r, stage):
    return next(s for s in r["stages"] if s.stage == stage)


def test_drafted_run_is_a_labelled_working_draft_that_keeps_the_validated_state(drill):
    d = drill["res"]["drafted"]
    assert d["exit_code"] == 0 and d["release"].startswith("WORKING DRAFT")
    r = d["run"]
    assert st(r, "ADD-03").status == "PARTIAL" and r["validated"].stage == "ADD-02"
    ops = {x.op.id: x for x in st(r, "ADD-03").ops}
    assert ops["ADD-03/2.1(a)"].valid and ops["ADD-03/2.1(b)"].valid               # two changes, one paragraph
    assert ops["ADD-03/4.1"].valid and ops["ADD-03/4.1"].details["old_value"] == "10"
    unresolved = {c["provision"] for c in st(r, "ADD-03").coverage if c["disposition"] == "unresolved"}
    assert {"ADD-03:3.1", "ADD-03:Q15", "ADD-03:Q16"} <= unresolved                  # a person decides
    a3 = drill["load"]("out-drafted/a3/a3.json")
    assert "Proposal Due Date 2026-11-26" in a3["subtitle"] and "ADD-03 is PARTIAL" in a3["subtitle"]


def test_curated_run_applies_and_shows_new_rows(drill):
    c = drill["res"]["curated"]
    assert c["exit_code"] == 0 and c["status"] == "ok"
    r = c["run"]
    assert st(r, "ADD-03").status == "APPLIED" and r["validated"].stage == "ADD-03"
    a1 = {x["id"]: x for x in drill["load"]("out-curated/a1/a1.json")["rows"]}
    assert a1["ADD-03-3.1-01"]["status:ADD-03"] == "NEW" and a1["ADD-03-3.1-01"]["status:ADD-02"] == "NOT ISSUED"
    assert a1["VOL-I-4.4-01"]["status:ADD-03"] == "NEW"
    s = st(r, "ADD-03").state
    assert "seven (7) Working Days" in s["VOL-I:5.2"].text and "one hundred and eighty (180) days" in s["VOL-I:7.1"].text
    assert s["VOL-I:6.7"].text.startswith("A Bidder may withdraw its Proposal")
    assert s["VOL-II:T2-4/TSS"].cells["Limit"] == "5"
    a3 = drill["load"]("out-curated/a3/a3.json")
    new = next(x for x in a3["explicit"] if x["id"] == "ADD-03-3.1-01")
    assert new["class"] == "non-responsive" and new["source"].startswith("ADD-03 3.1 p")


def test_affected_activities_are_shown(drill):
    d = [x for x in drill["load"]("out-curated/a5/replan_deltas.json")["rows"] if x["to_stage"] == "ADD-03"]
    got = {(x["activity"], x["change"]) for x in d}
    assert {("good-standing", "NEW"), ("clarifications", "MOVED"), ("clarifications", "REWORK"), ("form-4a", "REWORK"),
            ("technical-proposal", "REWORK"), ("spoc", "REWORK")} <= got
    prog = {a["id"]: a for a in drill["load"]("out-curated/a5/programme.json")["rows"]}
    assert "ADD-03-3.1-01" in prog["good-standing"]["req_ids"]
    a1 = {x["id"]: x for x in drill["load"]("out-curated/a1/a1.json")["rows"]}
    assert a1["VOL-I-5.2-01"]["dates"] == ["CLARIFICATION-CUTOFF: 2026-11-17 (stated_date_excluded)"]   # 7 WD re-read


def test_stale_dependencies_and_preserved_approved_state(drill):
    r = drill["res"]["curated"]["run"]
    ev = {e["row"].id: e["stages"]["ADD-03"] for e in r["evals"]}
    for rid in ("VOL-I-5.2-01", "VOL-I-7.1-01", "VOL-II-T2-4-TSS", "VOL-I-6.4-01"):
        assert ev[rid]["stale"], rid
    assert any("period re-read" in f for f in ev["VOL-I-5.2-01"]["flags"])
    a1 = {x["id"]: x for x in drill["load"]("out-curated/a1/a1.json")["rows"]}
    # the fixture approval of the Table 2-4 transcription is preserved; the interpretation of the changed row is STALE
    assert a1["VOL-II-T2-4-TSS"]["transcription"] == "approved" and "STALE" in a1["VOL-II-T2-4-TSS"]["status:ADD-03"]
    # an accepted row ADD-03 changed keeps its acceptance but is STALE (a release blocker); one it did not change is not
    assert a1["VOL-I-5.2-01"]["interpretation"] == "accepted by Fixture Test Reviewer" and ev["VOL-I-5.2-01"]["stale"]
    assert a1["VOL-I-9.3-01"]["interpretation"] == "accepted by Fixture Test Reviewer" and not ev["VOL-I-9.3-01"]["stale"]
    blockers = " ".join(b["detail"] for b in drill["res"]["curated"]["blockers"])
    assert "VOL-I-5.2-01" in blockers and "VOL-IV-p6-r1" in blockers and "VOL-II-p3-r1" not in blockers
    assert not (ROOT / "curation/approvals.yaml").exists()


def test_question_quoting_a_replaced_period_is_listed_for_review(drill):
    md = (drill["root"] / "out-curated/a2/a2.md").read_text(encoding="utf-8")
    line = next(l for l in md.splitlines() if "`ADD-03:Q15`" in l)
    assert "REVIEW (not automatically revoked)" in line and "ADD-03/2.1(a)" in line
    assert "`ADD-03:Q16`" not in md.split("### Earlier answers to review")[-1].split("###")[0]
