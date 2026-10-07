"""Session 13 (part 2, item 2): an analysis `row_new` / `row_reading` item is never dropped with an empty reason.

The blind-05 regression (rehearsals/blind-05/REGRESSION-S12.md, defect 3; synthetic): the analysis instructions ask for
a row_new on a free-standing provision (controller.INSTRUCTIONS), but downstream.promoted_ops promoted only
amendment_op and disposition items, so a verified row_new landed in neither ops, dispositions nor dropped: the packet
printed "(dropped: )" and the coverage line counted its provision as unaccounted. Now every analysis item that is not
promoted carries an explicit reason; an analysis row item becomes a downstream task keyed to its provision (or rides on
the C46 / row task already asking for that obligation) with the analysis proposal as its UNVERIFIED reference; while the
task is open the provision is accounted for through it, and a task the downstream phase never answers is
"unresolved: <reason>", never a silent gap."""
from __future__ import annotations

import pytest

import s12_w3b as W
from tenderpack.ai import downstream as DS
from tenderpack.ai import workflow as WF
from tenderpack.ai.contract import ChangeProposal, EvidenceRef, ProposalSet

ROW = {"id": "ADD-03-7.4-91", "group": "ADD-03:7.4", "scope": ["submission"], "requirement": "session 13 test data",
       "units": ["ADD-03:7.4"], "discipline": "Technical", "assessment": "procedural", "evidence": [],
       "no_deliverable": "test data", "interpretations": [{"stage": "ADD-03", "quote": "test data"}],
       "confidence": "low", "confidence_reason": "test data"}


@pytest.fixture(scope="module")
def ws(tmp_path_factory):
    return W.workspace(tmp_path_factory)


def _ps(ws, items):
    st = ws.identity()
    ev = EvidenceRef(doc="ADD-03", unit_id="ADD-03:7.4", page=3, kind="span", words="test data")
    return ProposalSet(run_id="s13", created="2026-10-06T00:00:00Z", route="recorded", provider="test",
                       model_requested="test", task="analysis", addendum="ADD-03", state=st,
                       items=[ChangeProposal(state=st, evidence=[ev], **it) for it in items])


ITEMS = [{"id": "ADD-03/7.4/row", "statement_type": "row_new", "provision": "ADD-03:7.4", "payload": {"row": ROW},
          "verification_status": "interpretation_pending"},
         {"id": "ADD-03/7.4/issue", "statement_type": "issue", "provision": "ADD-03:7.4",
          "payload": {"text": "test data", "owner": "Legal", "short": "t", "theme": "t"},
          "verification_status": "interpretation_pending"}]


@pytest.fixture(scope="module")
def handoff(ws):
    ps = _ps(ws, ITEMS)
    prom = DS.promoted_ops(ws, ps)
    tasks, _ = DS.tasks(ws, ps, prom, {})
    return ps, prom, tasks


def test_every_analysis_item_not_promoted_carries_an_explicit_reason(handoff):
    ps, prom, _ = handoff
    for it in ps.items:
        assert it.id not in prom["ops"] and it.id not in prom["dispositions"]
        assert (prom["dropped"].get(it.id) or "").strip(), (it.id, prom["dropped"])


def test_an_analysis_row_becomes_a_downstream_task_with_an_unverified_reference(handoff):
    _, prom, tasks = handoff
    t = next((x for x in tasks if any(a["item"] == "ADD-03/7.4/row" for a in x.get("analysis_items") or [])), None)
    assert t is not None, [x["id"] for x in tasks]
    assert t["kind"] == "row_new" and "ADD-03:7.4" in t["provisions"], t
    ref = next(a for a in t["analysis_items"] if a["item"] == "ADD-03/7.4/row")
    assert "UNVERIFIED" in ref["reference"] and ref["payload"]["row"]["id"] == ROW["id"]
    assert t["id"] in prom["dropped"]["ADD-03/7.4/row"]


def test_while_the_task_is_open_the_provision_is_accounted_through_it(handoff):
    ps, prom, tasks = handoff
    a = WF.carried_answer(["ADD-03/7.4/row"], tasks, None)
    assert a and not a["answered"] and a["carried"] and "open" in a["why"] and a["why"].strip(), a


def test_a_task_downstream_never_answers_is_unresolved_with_the_reason(handoff, ws):
    ps, prom, tasks = handoff
    tid = next(x["id"] for x in tasks if any(a["item"] == "ADD-03/7.4/row" for a in x.get("analysis_items") or []))
    empty = W.dset(ws, [])
    a = WF.carried_answer(["ADD-03/7.4/row"], tasks, empty)
    assert not a["answered"] and a["why"].startswith("unresolved: ") and tid in a["why"] and a["needs_person"], a


def test_the_packet_lists_carried_items_under_their_own_heading(handoff):
    ps, prom, tasks = handoff
    L = WF.carried_lines(ps, prom, tasks, None)
    assert any(x.startswith("## Analysis rows carried to downstream tasks") for x in L), L
    assert any("ADD-03/7.4/row" in x and "ADD-03:7.4" in x for x in L), L


def test_a_c46_task_for_the_same_provision_carries_the_reference_one_task_per_obligation(ws):
    ps = _ps(ws, ITEMS[:1])
    out = [{"id": "c46:ADD-03/7.4", "kind": "row_new", "op": "ADD-03/7.4", "provisions": ["ADD-03:7.4"],
            "outputs": [], "details": [], "rows": []}]
    prom = {"dropped": {}}
    DS.carry_analysis_rows(ps, out, prom, {}, "ADD-02", "ADD-03")
    assert [t["id"] for t in out] == ["c46:ADD-03/7.4"] and out[0]["analysis_items"][0]["item"] == "ADD-03/7.4/row"
    assert "c46:ADD-03/7.4" in prom["dropped"]["ADD-03/7.4/row"]
    assert WF.carried_answer(["ADD-03/7.4/row"], out, None)["carried"] == ["c46:ADD-03/7.4"]


def test_no_change_on_a_carried_row_task_is_refused_like_c46(ws, handoff):
    ps, prom, tasks = handoff
    t = next(x for x in tasks if x["id"].startswith("ana:"))
    ev = EvidenceRef(doc="ADD-03", unit_id="ADD-03:7.4", page=3, kind="span", words="test data")
    ds = W.dset(ws, [{"id": "N1", "statement_type": "no_change", "task": t["id"], "provision": "ADD-03:7.4",
                      "payload": {"why": "nothing"}, "evidence": [ev]}])
    DS.validate(ws, ds, W.promoted(ws), {t["id"]: t["kind"]})
    assert ds.items[0].verification_status == "invalid", [v.detail for v in ds.items[0].validation]
