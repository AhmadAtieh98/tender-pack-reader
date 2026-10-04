"""The ADD-03 drill: a synthetic future addendum through the same path as ADD-01 and ADD-02.

tests/fixtures/make_drill.py writes a synthetic "Addendum No. 3" (laid out like the real addenda) and a
seven-document pack around it, in a disposable directory. It has no curated op file, so `run` drafts its
ops with tenderpack.draft, exactly as for any unseen addendum. Nothing about ADD-03 is written into the
program: the expectations below come from the fixture's own record (expected.yaml) of what it placed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from tenderpack import stage2
from tenderpack.cli import ingest
from tenderpack.util import ROOT

sys.path.insert(0, str(ROOT / "tests/fixtures"))
import make_drill  # noqa: E402


@pytest.fixture(scope="module")
def drill(tmp_path_factory):
    base = tmp_path_factory.mktemp("drill")
    expected = make_drill.build(base / "src")
    res = ingest(base / "src/pack.yaml", base / "evidence", ROOT, quiet=True)
    assert res["exit_code"] == 0
    r = stage2.run(base / "evidence", base / "src/pack.yaml", ROOT)
    out = stage2.write(r, base / "out")
    return {"base": base, "expected": expected, "r": r, "out": out}


def st(r, stage):
    return next(s for s in r["stages"] if s.stage == stage)


def ev(r, row_id, stage):
    return next(e for e in r["evals"] if e["row"].id == row_id)["stages"][stage]


def op(r, oid):
    return next(x for x in st(r, "ADD-03").ops if x.op.id == oid)


def test_drill_is_drafted_through_the_same_path_and_stays_partial(drill):
    r = drill["r"]
    assert "ADD-03" in r["drafted"] and not (ROOT / "curation/amendments/ADD-03.yaml").exists()
    assert [s.stage for s in r["stages"]] == ["BASE", "ADD-01", "ADD-02", "ADD-03"]
    assert st(r, "ADD-03").issued == "2026-11-05"
    assert st(r, "ADD-03").status == "PARTIAL"
    assert r["validated"].stage == "ADD-02" and r["working"].stage == "ADD-03"
    assert {x.op.review for x in st(r, "ADD-03").ops} == {"proposed"}
    assert {x.op.origin for x in st(r, "ADD-03").ops} == {"pattern"}


def test_drafted_ops_apply_where_the_wording_is_recognised(drill):
    r = drill["r"]
    s = st(r, "ADD-03").state
    assert op(r, "ADD-03/2.1").valid and "Thursday 10 December 2026" in s["VOL-I:6.1"].text
    assert op(r, "ADD-03/3.1").valid and "forty-eight (48) hours" in s["VOL-V:31.3"].text
    assert op(r, "ADD-03/4.1").valid and s["VOL-I:8.6"].status == "deleted"
    tp = op(r, "ADD-03/5.1")
    assert tp.valid and tp.op.target == "VOL-II:T2-4/TP" and s["VOL-II:T2-4/TP"].cells["Limit"] == "0.5"
    assert tp.details["old_value"] == "1" and tp.details["reading_status"] == "pending"


def test_stale_old_words_are_rejected_not_retargeted(drill):
    """ADD-03 7.1 quotes 'seventy-two (72) hours' for VOL-II 4.4, which ADD-02 already changed to 96 hours.
    The op is invalid; VOL-II 4.4 keeps 96 hours; VOL-V 31.3 (which had the same words) is changed only by
    its own provision 3.1."""
    r = drill["r"]
    x = op(r, "ADD-03/7.1")
    assert not x.valid and any(c["id"] == "C23" and not c["ok"] for c in x.checks)
    s = st(r, "ADD-03").state
    assert "ninety-six (96) hours" in s["VOL-II:4.4"].text and "sixty (60)" not in s["VOL-II:4.4"].text
    assert s["VOL-V:31.3"].history == ["ADD-03/3.1"]


def test_unrecognised_and_question_provisions_are_unresolved_and_listed(drill):
    cov = {c["provision"]: c for c in st(drill["r"], "ADD-03").coverage}
    for p in ("ADD-03:6.1", "ADD-03:7.1", "ADD-03:Q15", "ADD-03:Q16"):
        assert cov[p]["disposition"] == "unresolved", (p, cov[p])
    assert all(cov[p]["disposition"] == "op" for p in ("ADD-03:2.1", "ADD-03:3.1", "ADD-03:4.1", "ADD-03:5.1"))
    assert not [p for p, c in cov.items() if c["disposition"] == "UNACCOUNTED"]


def test_working_state_moves_dates_and_marks_dependants_stale(drill):
    r = drill["r"]
    assert ev(r, "VOL-I-6.1-01", "ADD-03")["dates"][0]["planning"]["value"] == "2026-12-10"
    assert ev(r, "VOL-I-5.2-01", "ADD-03")["dates"][0]["planning"]["value"] == "2026-11-26"
    for rid in ("VOL-I-5.2-01", "VOL-I-6.3-01", "VOL-I-7.1-01", "VOL-I-8.5-01", "VOL-I-8.3-01", "VOL-I-6.1-01"):
        assert any("VOL-I:6.1 changed since" in x for x in ev(r, rid, "ADD-03")["stale"]), rid
    # the validated columns are those of the real pack
    assert ev(r, "VOL-I-6.1-01", "ADD-02")["dates"][0]["planning"]["value"] == "2026-11-26"
    assert ev(r, "VOL-I-5.2-01", "ADD-02")["stale"] == []


def test_lcc_chain_continues_in_the_working_state_only(drill):
    r = drill["r"]
    assert [ev(r, "VOL-I-8.6-01", s)["status"].split(" ")[0] for s in ("BASE", "ADD-01", "ADD-02", "ADD-03")] == \
        ["ACTIVE", "DELETED", "REINSTATED-AMENDED", "DELETED"]
    ops = [c.split(" ")[0] for c in ev(r, "VOL-I-8.6-01", "ADD-03")["chain"] if " <- " in c]   # every unit, then ops
    assert ops == ["ADD-01/4.1", "ADD-02/9.1", "ADD-02/9.2", "ADD-03/4.1"]               # in addendum order


def test_question_quoting_a_replaced_value_is_listed_for_review(drill):
    r = drill["r"]
    ans = {a["answer"]: a for a in stage2.answers_to_review(r, st(r, "ADD-03"))}
    assert "ADD-03:Q16" in ans and "26 November" in ans["ADD-03:Q16"]["why"]
    assert ans["ADD-03:Q16"]["status"] == "REVIEW (not automatically revoked)"
    assert "ADD-03:Q15" not in ans                      # cites VOL-I 9.2, which ADD-03 does not change


def test_outputs_keep_the_validated_state_and_label_the_working_one(drill):
    out = drill["base"] / "out"
    assert drill["out"]["status"] == "ok"
    a1 = json.loads((out / "a1/a1.json").read_text(encoding="utf-8"))
    assert a1["validated_stage"] == "ADD-02" and a1["working_stage"] == "ADD-03"
    a3 = json.loads((out / "a3/a3.json").read_text(encoding="utf-8"))
    assert "Proposal Due Date 2026-11-26" in a3["subtitle"] and "ADD-03 is PARTIAL" in a3["subtitle"]
    assert "I-PARTIAL-ADD-03" in {i["id"] for i in a3["unresolved"]["items"]}
    main = json.loads((out / "a5/programme.json").read_text(encoding="utf-8"))["rows"]
    assert next(a for a in main if a["id"] == "deliver")["latest_finish"] == "2026-11-26"
    work = json.loads((out / "a5/working/ADD-03.json").read_text(encoding="utf-8"))
    acts = {a["id"]: a for a in work["activities"]}
    assert acts["deliver"]["latest_finish"] == "2026-12-10" and "lcc-certificate" not in acts
    assert work["status_date"] == "2026-11-05"
    md = (out / "a2/a2.md").read_text(encoding="utf-8")
    assert "## ADD-03 (issued 2026-11-05) — PARTIAL" in md and "drafted by tenderpack.draft" in md
    assert (out / "drafted/ADD-03.yaml").is_file()


def test_the_drill_changes_nothing_for_the_real_pack(drill):
    real = stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)
    for e in real["evals"]:
        d = next(x for x in drill["r"]["evals"] if x["row"].id == e["row"].id)
        for stage in ("BASE", "ADD-01", "ADD-02"):
            assert d["stages"][stage]["status"] == e["stages"][stage]["status"]
            assert d["stages"][stage]["text"] == e["stages"][stage]["text"]
            assert d["stages"][stage]["dates"] == e["stages"][stage]["dates"]


def test_engine_outcome_matches_the_fixture_record(drill):
    """expected.yaml is written by the fixture from what it printed, not from the program."""
    want = drill["expected"]["engine_outcome"]
    s = st(drill["r"], "ADD-03")
    assert s.status == want["status"]
    assert sorted(x.op.id for x in s.ops if x.valid) == sorted(want["valid_ops"])
    assert sorted(x.op.id for x in s.ops if not x.valid) == sorted(want["invalid_ops"])
    cov = {c["provision"]: c["disposition"] for c in s.coverage}
    assert all(cov[p] == "unresolved" for p in want["unresolved"])
    assert all(cov[p] == "no_effect" for p in want["no_effect"])
    assert sorted(cov) == sorted(drill["expected"]["provisions"])
