"""Session 14 (W2): statuses, downstream preservation and records (the blind-07 scorer's defects 7, 8, 9, 13, 16, 19;
rehearsals/blind-07/COMPARISON.md §8; report §9 L26, L29). Each test reproduces a defect first.

  7   a promoted `unresolved` disposition counted as an answer: the packet called the provision answered, A1's candidate
      status said "not changed by this run" for the rows it names (VOL-V 36.2 at SAR 2,500,000 while ADD-03 reduced it),
      and the unresolved change suppressed its possible downstream impacts
  8   analysis issues were never promoted and made no downstream task
  9   downstream tasks came only from valid ops, escalations and readings: when ops failed, the indirect analysis
      disappeared; a new unit has no curated relationships, so nothing followed from it
  13  the closed-clarification-window note was attached to schema errors and tool limitations, and an analysis issue
      could still suggest a clarification after the cut-off
  16  the run's own new rows failed check-register (no evidence item, no activity) because downstream proposed neither,
      and the packet did not tell that gap from a defect
  19  a document a new clause defines ("Revision C of the report of that name issued by the Authority") was never checked
      against the pack

The workspace is blind rehearsal 05's committed candidate (tests/fixtures/s12_blind05.py, ingested into tmp); the items
are this test's data (synthetic, labelled), never the truth about the tender. Quoted reasons and texts marked "frozen"
are blind-07's own words (rehearsals/blind-07/review/index.md, promotion.json)."""
from __future__ import annotations

import json
import re
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

import s12_blind05 as F
import s12_w3b as W3
from tenderpack import clarify
from tenderpack import partial as P
from tenderpack.ai import downstream as DS
from tenderpack.ai import workflow as WF
from tenderpack.ai.contract import ChangeProposal, EvidenceRef, ProposalSet, ValidationRecord

ROOT = Path(__file__).resolve().parents[1]
B07 = ROOT / "rehearsals/blind-07"
TEST = "(session 14 test data)"


@pytest.fixture(scope="module")
def ws(tmp_path_factory):
    return W3.workspace(tmp_path_factory)


def _ps(ws, items):
    st = ws.identity()
    out = []
    for it in items:
        it = dict(it)
        ev = EvidenceRef(doc="ADD-03", unit_id=it["provision"], page=1, kind="span", words="test data")
        val = [ValidationRecord(**v) for v in it.pop("validation", [])]
        out.append(ChangeProposal(state=st, evidence=[ev], validation=val, **it))
    return ProposalSet(run_id="s14", created="2026-10-07T00:00:00Z", route="recorded", provider="test",
                       model_requested="test", task="analysis", addendum="ADD-03", state=st, items=out)


UNRES = {"id": "ADD-03/7.4/disp", "statement_type": "disposition", "provision": "ADD-03:7.4",
         "payload": {"provision": "ADD-03:7.4", "disposition": "unresolved",
                     "reason": f"ambiguous: the provision and the cover state different figures; a person decides {TEST}"},
         "verification_status": "interpretation_pending"}
FAILED_OP = {"id": "ADD-03/7.3", "statement_type": "amendment_op", "provision": "ADD-03:7.3",
             "payload": {"id": "ADD-03/7.3", "type": "annotate", "targets": ["VOL-II:5.5"], "effect": "adds_obligation"},
             "verification_status": "invalid",
             "validation": [{"check": "payload", "ok": False, "detail": f"not a register.Row: consequence {TEST}"}]}
ISSUE = {"id": "ADD-03/7.2/issue", "statement_type": "issue", "provision": "ADD-03:7.2",
         "payload": {"text": f"Readings differ; whether to raise a clarification question with the Authority {TEST}",
                     "owner": "Legal"},
         "verification_status": "interpretation_pending"}
PROVS = ("ADD-03:7.2", "ADD-03:7.3", "ADD-03:7.4")


@pytest.fixture(scope="module")
def handoff(ws, tmp_path_factory):
    ps = _ps(ws, [UNRES, FAILED_OP, ISSUE])
    prom = DS.promoted_ops(ws, ps)
    ctx = SimpleNamespace(cp=SimpleNamespace(data={"provisions": {p: {"status": "validated", "kind": "clause"}
                                                                   for p in PROVS}, "batches": {}}),
                          dir=tmp_path_factory.mktemp("s14ctx"), s={}, ws=ws)
    answers = WF._answers(ctx, ps, prom, tasks=[])
    tasks, _ = DS.tasks(ws, ps, prom, answers)
    return ps, prom, answers, tasks


# ---------------------------------------------------------------------------------------------- 7: the four states

def test_7_a_promoted_unresolved_disposition_accounts_for_its_provision_but_never_answers_it(handoff):
    ps, prom, answers, _ = handoff
    assert "ADD-03/7.4/disp" in prom["dispositions"]                       # it is promotable (accounted for) ...
    a = answers["ADD-03:7.4"]
    assert a["answered"] is False and a["state"] == "unresolved" and a["accounted"] is True, a     # ... not applied
    assert a["approved"] is False and "ambiguous" in a["why"] and "ADD-03/7.4/disp" in a["why"], a
    assert WF.state_of(a).startswith("UNRESOLVED") and "answered" not in WF.state_of(a)


def test_7_an_unresolved_change_keeps_a_conditional_impact_investigation(handoff):
    _, _, _, tasks = handoff
    cond = [t for t in tasks if t["kind"] == "conditional_impact"]
    items = {x["provision"]: x for t in cond for x in t["items"]}
    assert items.get("ADD-03:7.4", {}).get("basis") == "unresolved", [t["id"] for t in tasks]
    t = next(t for t in cond if "ADD-03:7.4" in t["provisions"])
    assert t["conditional"] is True and t["label"].startswith("CONDITIONAL") and "never an accepted fact" in t["label"]
    assert "scope" in t and "never a row" in t["expect"]


def test_7_a1_flags_the_value_an_unresolved_provision_puts_in_question(ws, tmp_path_factory):
    r = F.run(tmp_path_factory)["r"]                     # blind-05's candidate: its op file holds unresolved provisions
    unres = {k: v for k, v in P.unresolved_rows(r).items() if any(not w.startswith("STALE") for w in v)}
    assert unres, "the candidate names rows through unresolved provisions"
    ctx = SimpleNamespace(addendum="ADD-03", dir=tmp_path_factory.mktemp("s14a1"), ws=ws)
    out, default, _ = WF._row_statuses(ctx, r)
    for rid, why in unres.items():
        st = out.get(rid, default)
        assert st.startswith("UNRESOLVED") and "not changed by this run" not in st, (rid, st)
        if not any(w.startswith("STALE") for w in why):
            prov = next(w for w in why if not w.startswith("STALE")).split(" ")[0]
            assert "value in question" in st and prov in st and "unresolved:" in st, (rid, st)


# ---------------------------------------------------------------------------------------------- 8 and 9

def test_8_an_analysis_issue_gets_a_task_and_is_promoted_as_a_proposed_issue(handoff, ws):
    ps, prom, _, tasks = handoff
    cond = [x for t in tasks if t["kind"] == "conditional_impact" for x in t["items"]]
    rec = next((x for x in cond if x.get("item") == "ADD-03/7.2/issue"), None)
    assert rec and rec["basis"] == "analysis issue" and "UNVERIFIED" in rec["reference"], cond
    iss = DS.analysis_issues(ps, {"closed": True, "date": "2026-11-12"})
    assert len(iss) == 1
    iid, v = next(iter(iss.items()))
    assert re.fullmatch(r"I-[A-Z0-9-]+", iid) and v["owner"] == "Legal" and v["text"].startswith("PROPOSED")
    assert v["clarification_route"] == "bid decision (window closed 2026-11-12)"            # 13: after the cut-off
    assert "PROPOSED issue" in DS.not_promoted_reason(ps.items[2]) and iid in prom["dropped"]["ADD-03/7.2/issue"]


def test_9_a_failed_op_keeps_its_downstream_task_as_conditional_with_the_failure_named(handoff):
    _, _, _, tasks = handoff
    rec = next((x for t in tasks if t["kind"] == "conditional_impact" for x in t["items"]
                if x.get("item") == "ADD-03/7.3"), None)
    assert rec and rec["basis"] == "failed op" and "payload" in rec["why"] and rec["payload"]["type"] == "annotate", rec


def test_9_a_blocked_item_named_by_its_readiness_keeps_a_conditional_task(ws):
    # W1's controller-written readiness (`ready`, `blocked_by` on each ChangeProposal; session 14): read as attributes
    blocked = SimpleNamespace(id="ADD-03/7.1x", statement_type="amendment_op", provision="ADD-03:7.1",
                              verification_status="interpretation_pending", payload={"type": "insert_unit"},
                              validation=[], blocked_by=["blocked by failed statement S2: not verbatim"], ready=False)
    prom = W3.promoted(ws)
    tasks = DS.conditional_tasks(ws, SimpleNamespace(items=[blocked]), prom, {}, prom["r2"], "ADD-03")
    rec = next(x for t in tasks for x in t["items"] if x.get("item") == "ADD-03/7.1x")
    assert rec["basis"] == "blocked" and rec["ready"] is False and "failed statement S2" in rec["why"], rec
    assert rec["conditional_on"] == {"kind": "op", "ref": "ADD-03/7.1x", "state": "held", "why": rec["why"]}


def test_9_promotion_waits_for_an_item_that_is_not_ready(ws):
    # an op W1 marks not ready is not promoted by the workflow's combined promotion; its blocker is the reason
    ok = SimpleNamespace(id="ADD-03/3.1", statement_type="amendment_op", provision="ADD-03:3.1",
                         verification_status="evidence_verified", payload=W3.promoted(ws)["ops"]["ADD-03/3.1"]
                         .model_dump(exclude_none=True), validation=[], blocked_by=["depends on ADD-03/3.0/esc "
                                                                                    "(escalation, escalated)"],
                         ready=False, evidence=[], statements=[])
    prom = DS.promoted_ops(ws, SimpleNamespace(addendum="ADD-03", items=[ok], statements=[]))
    assert "ADD-03/3.1" not in prom["ops"] and "not ready" in prom["dropped"]["ADD-03/3.1"]
    assert "ADD-03/3.0/esc" in prom["dropped"]["ADD-03/3.1"]


def test_9_the_engine_s_conditional_impacts_join_the_tasks_in_their_shape(ws, monkeypatch):
    from tenderpack import derived
    prom = W3.promoted(ws)
    unit = next(iter(prom["r2"]["evals"]))["row"].units[0]
    imp = {"id": "impact:ADD-03/9.9", "stage": "ADD-03", "provision": "ADD-03:7.2",            # W3's shape (test data)
           "conditional_on": {"kind": "op", "ref": "ADD-03/9.9", "state": "invalid", "why": f"C47 failed {TEST}"},
           "units": [unit], "investigate": "conditional on op ADD-03/9.9 (invalid)", "accepted": False}
    monkeypatch.setattr(derived, "conditional_impacts", lambda r, stage: [imp], raising=False)
    tasks = DS.conditional_tasks(ws, SimpleNamespace(items=[]), prom, {}, prom["r2"], "ADD-03")
    t = next(t for t in tasks if any(x.get("item") == "impact:ADD-03/9.9" for x in t["items"]))
    assert t["conditional"] is True and t["accepted"] is False and imp["conditional_on"]["ref"] in str(t["conditional_on"])
    assert unit in t["scope"]["units"] and any(unit in r.units for e in prom["r2"]["evals"] for r in [e["row"]]
                                               if r.id in t["scope"]["rows"]) and "prices" in t["scope"]


def test_9_an_op_that_adds_a_unit_gets_an_obligation_task_with_what_shares_its_terms(ws):
    prom = W3.promoted(ws)
    tasks, _ = DS.tasks(ws, SimpleNamespace(addendum="ADD-03", items=[]), prom, {})
    # session 14 (F3, N2): an obligation task of an op that also has a row task is merged into that task (`obligation`)
    ob = [t for t in tasks if t["kind"] == "obligation_impact"] + [t["obligation"] for t in tasks if t.get("obligation")]
    adds = [o.id for o in prom["ops"].values() if o.type in ("insert_unit", "insert_row", "append_text", "replace_unit")
            or o.effect == "adds_obligation"]
    assert adds and {t["op"] for t in ob} == set(adds), ([t.get("id") or t["op"] for t in ob], adds)
    assert all("related" in t and "terms" in t and "hint" in t["expect"] for t in ob)


def test_9_an_answer_to_a_conditional_task_is_never_a_row_and_never_above_interpretation_pending(handoff, ws):
    ps, prom, _, tasks = handoff
    tid = next(t["id"] for t in tasks if t["kind"] == "conditional_impact")
    ev = {"doc": "ADD-03", "unit_id": "ADD-03:7.4", "page": 1, "kind": "span", "words": "test data"}
    ds = W3.dset(ws, [{"id": "C1", "statement_type": "issue", "task": tid, "provision": "ADD-03:7.4",
                       "payload": {"id": "I-S14-COND", "text": f"possible effect on pricing {TEST}", "owner": "Commercial",
                                   "theme": "pricing"}, "evidence": [ev]},
                      {"id": "C2", "statement_type": "evidence_item", "task": tid, "provision": "ADD-03:7.4",
                       "payload": {"id": "EV-S14-COND", "item": {"name": "test", "envelope": "A"}}, "evidence": [ev]}])
    DS.validate(ws, ds, prom, {t["id"]: t["kind"] for t in tasks})
    c1, c2 = ds.items
    assert c2.verification_status == "invalid" and any(v.check == "conditional" and not v.ok for v in c2.validation)
    assert c1.verification_status != "evidence_verified" and any(v.check == "conditional" and v.ok for v in c1.validation)


# ---------------------------------------------------------------------------------------------- 13: window by class

FROZEN_REASONS = {   # blind-07's own unresolved reasons (review/index.md L120-140), shortened
    "not promotable: ADD-03/2.2/row invalid (payload: not a register.Row: 2 validation errors for Row)": "software",
    "not promotable: ADD-03/Q15 invalid (previous_value: no target to compare the previous value)": "software",
    "not promotable: ADD-03/3.3 conflicting (dependencies: unknown ids ['ADD-03/3.1(a)'])": "software",
    "not promotable: ADD-03/T42-1/2/disp insufficient_evidence (statements: fact analysis-003/S2 is not supported "
    "verbatim)": "software",
    "escalated: software limitation: no op type inserts a table into a volume": "software",
    "ambiguous: 2.1 prints a change ('is reduced by SAR 1,000,000') to VOL-V:36.2, but the cover states SAR 4,000,000":
        "clarification",
}


def test_13_the_closed_window_note_never_goes_on_a_software_limitation_or_a_schema_failure(ws):
    for why, cls in FROZEN_REASONS.items():
        assert DS.route_class(why) == cls, why
    prom = W3.promoted(ws)
    st = {"ADD-03:7.3": {"needs_person": True, "why": next(iter(FROZEN_REASONS))},
          "ADD-03:7.4": {"needs_person": True, "why": list(FROZEN_REASONS)[-1]}}
    tasks, _ = DS.tasks(ws, SimpleNamespace(addendum="ADD-03", items=[]), prom, st)
    esc = {t["provision"]: t for t in tasks if t["id"].startswith("esc:")}
    assert "clarification_window" not in esc["ADD-03:7.3"], esc["ADD-03:7.3"]
    assert "clarification_window" in esc["ADD-03:7.4"]                     # blind-05's ADD-03 issued after the cut-off


def test_13_the_candidate_a3_route_follows_the_class(tmp_path_factory):
    r = F.run(tmp_path_factory)["r"]
    win = clarify.window(r, "ADD-03")
    assert win and win["closed"]
    b = P.blockers(r, P.unresolved_rows(r), None, [], win)
    assert b["provisions"]
    for p in b["provisions"]:
        assert (p["route"] == "") == (P.route_class(p["reason"]) == "software"), p


# ---------------------------------------------------------------------------------------------- 16: deliverables

def test_16_row_tasks_ask_for_the_new_rows_evidence_and_activity(ws):
    prom = W3.promoted(ws)
    tasks, _ = DS.tasks(ws, SimpleNamespace(addendum="ADD-03", items=[]), prom, {})
    rows = [t for t in tasks if t["kind"] in DS.ROW_MAKING]
    assert rows and all("evidence_item" in t["needs"] and "activity" in t["needs"] and "no_deliverable" in t["needs"]
                        for t in rows)


def test_16_check_register_tells_a_downstream_gap_from_a_defect():
    pkt = (B07 / "review/index.md").read_text(encoding="utf-8")
    found = re.findall(r"(?m)^  - \[([^\]]+)\] ([^:]*): (.*)$", pkt.split("## check-register on the candidate")[1]
                       .split("\n## ")[0])
    assert len(found) == 8                                                   # the frozen run's eight findings
    new = set(json.loads((B07 / "promotion.json").read_text(encoding="utf-8"))["rows_new"])
    cl = WF.classify_register_findings(found + [("quote", "VOL-I-6.3-01", "a quote not found")], new)
    assert len(cl["not_proposed"]) == 8 and all("did not propose" in x for x in cl["not_proposed"])
    assert cl["defects"] == ["[quote] VOL-I-6.3-01: a quote not found"]


# ---------------------------------------------------------------------------------------------- 19: documents

NEW_12_5 = ("The following new Clause 12.5 is inserted in Volume V after Clause 12.4: ‘12.5 If the Project Company "
            "encounters at the site ground conditions that are materially more adverse than those described in the "
            "Geotechnical Baseline Report, it shall be entitled to an extension of the Scheduled PCOD and to payment of "
            "its reasonable additional costs, provided that it notifies the Authority within five (5) Working Days of "
            "encountering them. In this Clause, the Geotechnical Baseline Report means Revision C of the report of that "
            "name issued by the Authority.’")                                # blind-07's ADD-03 4.1 (frozen words)


def _r_with(units, rels=()):
    cfg = yaml.safe_load((ROOT / "config/pack.yaml").read_text(encoding="utf-8"))
    return {"cfg": cfg, "units": units, "relationships": list(rels), "stages": [], "evals": []}


def test_19_a_document_a_new_clause_defines_is_checked_against_the_pack_and_proposed_missing():
    r = _r_with([{"unit_id": "ADD-03:4.1", "doc": "ADD-03", "kind": "clause", "text": NEW_12_5, "pages": [2]}])
    got = P.referenced_documents(r, ["ADD-03"])
    assert [d["document"] for d in got] == ["Geotechnical Baseline Report (Revision C)"], got
    d = got[0]
    assert d["kind"] == "missing_document" and d["status"] == "proposed" and d["from"] == ["ADD-03:4.1"]
    assert d["evidence"][0]["words"] in NEW_12_5 and "Revision C" in d["evidence"][0]["words"]
    assert "not among the pack's documents" in d["basis"]


def test_19_a_supplied_or_curated_document_is_not_proposed_again():
    unit = {"unit_id": "ADD-03:4.1", "doc": "ADD-03", "kind": "clause", "text": NEW_12_5, "pages": [2]}
    curated = _r_with([unit], [{"id": "REL-X", "kind": "missing_document", "document": "Geotechnical Baseline Report",
                                "document_id": "GBR"}])
    assert P.referenced_documents(curated, ["ADD-03"]) == []
    supplied = _r_with([unit])
    supplied["cfg"]["documents"].append({"doc_id": "VOL-VI", "kind": "volume",           # this test's data
                                         "path": "sources/x/VOL-VI_Geotechnical_Baseline_Report_Rev_C.pdf"})
    assert P.referenced_documents(supplied, ["ADD-03"]) == []


# ---------------------------------------------------------------------------------------------- promotion (7, 8, 19)

def test_promotion_counts_the_unresolved_disposition_writes_the_issue_and_proposes_the_missing_document(tmp_path,
                                                                                                    tmp_path_factory):
    from tenderpack.ai.tools import Workspace
    pack = W3.copy_candidate(tmp_path)
    ws2 = Workspace(evidence=F.build(tmp_path_factory), pack=pack, root=F.ROOT)
    ps = _ps(ws2, [UNRES, FAILED_OP, ISSUE])
    prom = DS.promoted_ops(ws2, ps)
    summ = DS.promote(ws2, {"dir": str(tmp_path), "pack": str(pack)}, "s14-test", ps, prom, None, "test origin", {})
    assert "ADD-03:7.4" in summ["unresolved"] and "ADD-03:7.4" in summ["accounted_unresolved"], summ["unresolved"]
    iid = DS.analysis_issue_id(ps.items[2])
    assert summ["analysis_issues"] == [iid]
    iss = yaml.safe_load((tmp_path / "curation/register/issues/ADD-03-ai.yaml").read_text(encoding="utf-8"))["issues"]
    assert iss[iid]["owner"] == "Legal" and iss[iid]["human_decision"] == "pending", iss[iid]
    assert iss[iid]["text"].startswith("PROPOSED by the analysis phase")
    of = yaml.safe_load((tmp_path / "curation/amendments/ADD-03.yaml").read_text(encoding="utf-8"))
    d = [x for x in of["dispositions"] if x["provision"] == "ADD-03:7.4"]
    assert len(d) == 1 and d[0]["disposition"] == "unresolved"                # accounted for once, still unresolved
