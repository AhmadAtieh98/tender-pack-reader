"""Session 14 (W1; blind-07 COMPARISON §8 defects 3 and 5, report §9 L23): typed dependencies, cycles and readiness,
and the blast radius of a failed shared statement.

blind-07: a dependency could name only op ids, so 3.3 (on the escalation 3.1(a)), 2.2's row (on the disposition
2.1/disp) and 3.1(b) failed as "unknown ids"; one summary "fact" with `evidence: []` (analysis-003/S2) failed its check
and sank every item citing it without the blast radius being reported. Now a dependency may name any id of the set's
typed id space (units, rows, recorded ops, the set's own items and statements), the kind is checked (a change never
rests on an issue or a question), a cycle is refused with the cycle named, readiness is computed (an item is ready when
every item it relies on is promotable and ready), and a failed fact still blocks every item citing it (a failed fact
supports nothing) while the review packet, the validation report and an unresolved provision's reason name it:
"blocked by failed statement <id>: <why>". A fact with empty evidence is refused. Synthetic items, blind-02 pack."""
from __future__ import annotations

import pytest
import yaml

from ai_fixture import workspace
from tenderpack.ai import controller
from tenderpack.ai.tools import call_tool

Q31 = {"doc": "ADD-03", "unit_id": "ADD-03:3.1", "page": 1, "kind": "span",
       "words": "‘one hundred and fifty (150) days’ is deleted and ‘one hundred and eighty (180) days’ is substituted"}
Q32 = {"doc": "ADD-03", "unit_id": "ADD-03:3.2", "page": 1, "kind": "span",
       "words": "‘one hundred and eighty (180) days’ is deleted and ‘two hundred and ten (210) days’ is substituted"}
Q33 = {"doc": "ADD-03", "unit_id": "ADD-03:3.3", "page": 1, "kind": "span",
       "words": "Paragraph 2 of Form 4-A shall be read accordingly."}
Q12 = {"doc": "ADD-03", "unit_id": "ADD-03:1.2", "page": 1, "kind": "span",
       "words": "Clarification request 18 was withdrawn by the Bidder that submitted it and is not answered."}


@pytest.fixture(scope="module")
def ws(request, tmp_path_factory):
    return workspace(tmp_path_factory.mktemp("s14-deps"), evidence=request.getfixturevalue("blind02_build"))


def op31(**kw):
    return {"id": "ADD-03/3.1", "statement_type": "amendment_op", "provision": "ADD-03:3.1", "target": "VOL-I:7.1",
            "payload": {"type": "replace_text", "target": "VOL-I:7.1", "old": "one hundred and fifty (150) days",
                        "new": "one hundred and eighty (180) days"}, "evidence": [Q31], **kw}


def op32(**kw):
    return {"id": "ADD-03/3.2", "statement_type": "amendment_op", "provision": "ADD-03:3.2", "target": "VOL-I:6.3",
            "payload": {"type": "replace_text", "target": "VOL-I:6.3", "old": "one hundred and eighty (180) days",
                        "new": "two hundred and ten (210) days"}, "evidence": [Q32], **kw}


def esc33(**kw):
    return {"id": "ADD-03/3.3/esc", "statement_type": "escalation", "provision": "ADD-03:3.3",
            "payload": {"why": "the reissued Form 4-A has no numbered paragraphs", "what_is_unsupported": "a reading"},
            "evidence": [Q33], **kw}


def disp12(iid="ADD-03/1.2/disp", **kw):
    return {"id": iid, "statement_type": "disposition", "provision": "ADD-03:1.2",
            "payload": {"disposition": "no_effect", "reason": "a withdrawn request; nothing is answered"},
            "evidence": [Q12], **kw}


def issue33(**kw):
    return {"id": "ADD-03/3.3/issue", "statement_type": "issue", "provision": "ADD-03:3.3",
            "payload": {"text": "Form 4-A as reissued has no paragraph 2", "owner": "Legal"}, "evidence": [Q33], **kw}


def _set(ws, items, statements=()):
    st = ws.identity().model_dump()
    return {"addendum": "ADD-03", "state": st, "statements": list(statements), "items": [dict(i, state=st) for i in items]}


def _validate(ws, items, statements=()):
    res = call_tool(ws, "validate_proposal", {"proposal": _set(ws, items, statements)}, "model")
    return {x["id"]: x for x in res["items"]}, res


def _details(x, check):
    return [v["detail"] for v in x["validation"] if v["check"] == check and not v["ok"]]


def test_a_dependency_may_name_an_escalation_a_disposition_or_a_statement_of_the_set(ws):
    interp = {"id": "S-int", "kind": "interpretation", "text": "the withdrawn request needs no answer"}
    got, _ = _validate(ws, [op31(dependencies=["ADD-03/3.3/esc"]), esc33(), disp12(dependencies=["S-int"]),
                            op32(dependencies=["ADD-03/1.2/disp", "VOL-I:6.3"])], [interp])
    for k in ("ADD-03/3.1", "ADD-03/1.2/disp", "ADD-03/3.2"):
        assert not any("unknown" in d for d in _details(got[k], "dependencies")), got[k]["validation"]
    assert got["ADD-03/3.1"]["verification_status"] == "evidence_verified"
    assert got["ADD-03/1.2/disp"]["verification_status"] == "interpretation_pending"   # rests on an interpretation
    # readiness: 3.1 waits on an escalation (not promotable); its status is unchanged
    assert got["ADD-03/3.1"]["ready"] is False
    assert got["ADD-03/3.1"]["blocked_by"] == ["depends on ADD-03/3.3/esc (escalation, escalated)"]
    assert got["ADD-03/3.2"]["ready"] is True and got["ADD-03/1.2/disp"]["ready"] is True


def test_readiness_is_transitive(ws):
    got, _ = _validate(ws, [op31(dependencies=["ADD-03/3.3/esc"]), esc33(), op32(dependencies=["ADD-03/3.1"])])
    assert got["ADD-03/3.2"]["ready"] is False
    assert got["ADD-03/3.2"]["blocked_by"] == ["depends on ADD-03/3.1, which is not ready"], got["ADD-03/3.2"]


def test_a_change_may_not_rest_on_an_issue(ws):
    got, _ = _validate(ws, [op31(dependencies=["ADD-03/3.3/issue"]), issue33()])
    d = _details(got["ADD-03/3.1"], "dependencies")
    assert d and "may not depend on ADD-03/3.3/issue (item:issue)" in d[0], got["ADD-03/3.1"]["validation"]
    assert got["ADD-03/3.1"]["verification_status"] == "insufficient_evidence"
    ok, _ = _validate(ws, [esc33(dependencies=["ADD-03/3.3/issue"]), issue33()])      # an escalation may
    assert not _details(ok["ADD-03/3.3/esc"], "dependencies")


def test_a_cycle_is_refused_with_the_cycle_named(ws):
    got, res = _validate(ws, [disp12("D1", dependencies=["D2"]), disp12("D2", dependencies=["D1"]),
                              op31(dependencies=["ADD-03/3.1"])])
    for k in ("D1", "D2"):
        assert got[k]["verification_status"] == "invalid", got[k]["validation"]
        assert any(d.startswith("dependency cycle refused: D1 -> D2 -> D1") for d in _details(got[k], "dependencies"))
    assert got["ADD-03/3.1"]["verification_status"] == "invalid"                     # a self-dependency
    assert "dependency cycle refused: ADD-03/3.1 -> ADD-03/3.1" in _details(got["ADD-03/3.1"], "dependencies")


FACT = {"id": "S2", "kind": "fact", "text": "the Arabic and English renderings differ (a paraphrase)", "evidence": []}


def test_a_failed_fact_blocks_every_item_citing_it_and_the_blast_radius_is_reported(ws, tmp_path):
    items = [op32(statements=["S2"]), disp12(statements=["S2"]), issue33(statements=["S2"]), op31()]
    got, res = _validate(ws, items, [FACT])
    for k in ("ADD-03/3.2", "ADD-03/1.2/disp", "ADD-03/3.3/issue"):        # kept in the set, blocked, reason named
        assert got[k]["verification_status"] == "insufficient_evidence"
        assert got[k]["ready"] is False and got[k]["blocked_by"][0].startswith("blocked by failed statement S2: no "
                                                                               "evidence: refused"), got[k]
    assert got["ADD-03/3.1"]["ready"] is True and got["ADD-03/3.1"]["verification_status"] == "evidence_verified"
    br = res["blast_radius"]
    assert br[0]["statement"] == "S2" and br[0]["refused"] is True
    assert sorted(br[0]["blocks"]) == ["ADD-03/1.2/disp", "ADD-03/3.2", "ADD-03/3.3/issue"]
    # the host route: staged, the review packet names the blast radius, and promotion names the blocker
    sub = controller.submit(ws, _set(ws, items, [FACT]), host_model="test-host")
    assert sub["blast_radius"][0]["statement"] == "S2"
    from pathlib import Path
    md = (Path(sub["staging"]) / "review_request.md").read_text(encoding="utf-8")
    assert "## Blocked by a failed shared statement" in md and "**S2**" in md and "blocks 3 item(s)" in md, md
    code, msgs = controller.promote(ws, sub["run_id"], "Fixture Test Reviewer", tmp_path / "amend", tmp_path / "props")
    assert code == 0, msgs
    of = yaml.safe_load((tmp_path / "amend" / "ADD-03.yaml").read_text(encoding="utf-8"))
    d = {x["provision"]: x for x in of["dispositions"]}
    assert d["ADD-03:3.2"]["disposition"] == "unresolved"
    assert "blocked by failed statement S2: no evidence: refused" in d["ADD-03:3.2"]["reason"], d["ADD-03:3.2"]


def test_an_item_waiting_on_an_escalation_is_not_promoted_and_says_why(ws, tmp_path):
    sub = controller.submit(ws, _set(ws, [op31(dependencies=["ADD-03/3.3/esc"]), esc33(), op32()]),
                            host_model="test-host")
    code, msgs = controller.promote(ws, sub["run_id"], "Fixture Test Reviewer", tmp_path / "amend", tmp_path / "props")
    assert code == 0, msgs
    of = yaml.safe_load((tmp_path / "amend" / "ADD-03.yaml").read_text(encoding="utf-8"))
    assert [o["id"] for o in of["ops"]] == ["ADD-03/3.2"]
    d = {x["provision"]: x for x in of["dispositions"]}
    assert "depends on ADD-03/3.3/esc (escalation, escalated)" in d["ADD-03:3.1"]["reason"], d["ADD-03:3.1"]
