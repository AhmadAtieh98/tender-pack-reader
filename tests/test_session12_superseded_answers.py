"""Session 12 (W3a; the owner's part 2): superseded answers are reconsidered.

When an addendum changes a unit that an earlier addendum's clarification answer relied on (the units the answer cites,
the units its annotation targets, or a unit those govern through a curated relationship), that earlier answer is flagged
'to be re-read against the new text' in A2's list of earlier answers, in the diff and the review packet, and the AI
workflow creates a downstream task for it (an escalation for a person). Nothing decides the outcome: the answer stays in
force, is never revoked, and the flag only asks a person to read it again.

Regression material: blind rehearsal 05 (COMPARISON.md S5, IE3; follow-up 8, second half): ADD-03 4.1 makes a membrane
step mandatory in VOL-II 3.1; ADD-01 response 1 ('No. Volume II Clause 3.1 does not mandate a process train') relied on
the old words. A2 listed it mechanically as REVIEW, while the re-made 3.1 reading said the answer 'remains consistent'.
The relationship case uses one test-only relationship entry (labelled REL-S12-TEST, this test's own data, not the pack's)
added to a copy of the run."""
from __future__ import annotations

import copy

import pytest

import s12_blind05
from tenderpack import live, stage2
from tenderpack.ai import downstream as DS
from tenderpack.util import ROOT

REREAD = "to be re-read against the new text"


@pytest.fixture(scope="module")
def r(tmp_path_factory):
    return s12_blind05.run(tmp_path_factory)["r"]


@pytest.fixture(scope="module")
def real():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


def _st(r, name):
    return next(s for s in r["stages"] if s.stage == name)


def test_an_answer_relying_on_a_changed_unit_is_to_be_re_read(r):
    ans = {a["answer"]: a for a in stage2.answers_to_review(r, _st(r, "ADD-03"))}
    q1 = ans["ADD-01:Q1"]
    assert q1["status"] == "REVIEW (not automatically revoked)"         # never revoked, never decided
    assert REREAD in q1["reread"] and "VOL-II:3.1" in q1["reread"] and "ADD-03/4.1" in q1["reread"]
    assert _st(r, "ADD-03").state["ADD-01:Q1"].status == "active"


def test_a2_and_the_diff_say_it(r):
    a2 = stage2.a2(r)
    sec = a2["markdown"].split("## ADD-03")[1].split("### Earlier answers to review")[1].split("###")[0]
    line = next(x for x in sec.splitlines() if x.startswith("- `ADD-01:Q1`"))
    assert REREAD in line and "VOL-II:3.1" in line
    md, data = live.diff(r, "ADD-02", "ADD-03")
    assert any(x["answer"] == "ADD-01:Q1" and REREAD in x["reread"] for x in data["answers_to_reread"])
    assert "ADD-01:Q1" in md.split("## Earlier answers to re-read")[1].split("\n## ")[0]


def test_an_answer_reached_through_its_annotation_targets(real):
    # ADD-01/Q3 annotates VOL-I 6.4; the answer's own words need not cite the clause for it to rely on it
    ans = {(s.stage, a["answer"]): a for s in real["stages"][1:] for a in stage2.answers_to_review(real, s)}
    assert ("ADD-02", "ADD-01:Q2") in ans                              # the session-08 rule still holds
    for a in ans.values():
        assert a["status"] == "REVIEW (not automatically revoked)" and REREAD in a["reread"]


def test_an_answer_reached_through_a_relationship(r):
    r2 = copy.copy(r)
    r2["relationships"] = list(r.get("relationships") or []) + [{
        "id": "REL-S12-TEST", "kind": "depends_on", "status": "proposed", "from": ["VOL-II:3.1"], "to": ["VOL-I:6.4"],
        "note": "test data (session 12): not the pack's"}]
    ans = {a["answer"]: a for a in stage2.answers_to_review(r2, _st(r2, "ADD-03"))}
    assert "ADD-01:Q3" in ans, sorted(ans)                              # ADD-01/Q3 annotates VOL-I 6.4
    assert "REL-S12-TEST" in ans["ADD-01:Q3"]["why"] and REREAD in ans["ADD-01:Q3"]["reread"]
    plain = {a["answer"] for a in stage2.answers_to_review(r, _st(r, "ADD-03"))}
    assert "ADD-01:Q3" not in plain                                     # without the link it is not reached


def test_the_workflow_makes_a_task_for_a_person(r):
    tasks = DS.reread_tasks(r, "ADD-03")
    t = next(x for x in tasks if x["provision"] == "ADD-01:Q1")
    assert t["id"] == "reread:ADD-01:Q1" and t["kind"] == "escalation"
    assert REREAD in t["status"] and "a person decides" in t["status"]
    assert "ADD-01:Q1" in t["scope"]["units"] and "VOL-II:3.1" in t["scope"]["units"]
    assert "VOL-II-3.1-01" in t["scope"]["rows"]
