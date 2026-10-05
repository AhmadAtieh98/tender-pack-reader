"""Session 12 (W3b; the owner's part 2): image-table readings feed proposed rows and activities while a person's
approval of the reading is pending (blind-05 follow-up 6; the key's 7.1, S7, DD10).

Blind-05's Appendix A (Table 5-1, Arabic, image only) was read by the readings step and left PENDING (no approval). The
downstream phase left every cell unresolved ("The height values are not taken as parameters here"). Now:
  * a pending reading of the addendum gives a downstream task that carries the reading's units: Arabic as printed,
    translations apart, pages, crops and band ids, uncertainties, and the expectation that every row or activity made
    from it is `conditional_on: {reading: <id>, until: approval}`;
  * a proposed row (or activity) resting on a pending reading is marked `conditional_on` by the validator (the field
    names the reading and pins its review subject), must cite the reading's own units in its evidence, and is never in
    force: A1 shows it as PENDING READING naming the reading, the candidate A3/A5 and the review packet list it apart,
    the validated A3/A5 never carry it;
  * after a person's approval (a re-ingest gives the units `reading.status: approved`) the same row is ordinary; a
    reading that changed since the proposal is a problem, and a changed reading file makes a proposal stale.
Synthetic regression material (blind-05); nothing here approves anything: the 'approved' build copy below stands for
what a re-ingest would give after a person's `tenderpack approve`, in a disposable folder."""
from __future__ import annotations

import copy
import json
import shutil

import pytest

import s12_blind05 as F
import s12_w3b as W
from tenderpack import partial, stage2
from tenderpack.ai import downstream as DS
from tenderpack.ai.contract import EvidenceRef

READING = "ADD-03-p4-r1"
ROW_ID = "ADD-03-T51-A-01"


@pytest.fixture(scope="module")
def ws(tmp_path_factory):
    return W.workspace(tmp_path_factory)


@pytest.fixture(scope="module")
def prom(ws):
    return W.promoted(ws)


def _row(ws, **kw) -> dict:
    a = ws.units_by_id["ADD-03:p4-image/row-a"]["text"]
    row = {"id": ROW_ID, "group": "VOL-II:5.5+ADD-03", "scope": ["technical", "site", "height_limits"],
           "requirement": "Table 5-1 Zone A (within 1,500 m of the eastern boundary of the site): maximum height 25 m "
                          "above natural ground level; warning lighting required",
           "units": ["ADD-03:p4-image/row-a", "ADD-03:p4-image/table-header"], "discipline": "Technical",
           "assessment": "contractual_post_award", "evidence": [],
           "no_deliverable": "a design constraint; shown in the Technical Proposal (test data)",
           "interpretations": [{"stage": "ADD-03", "quote": a[:60],
                                "parameters": {"zone": "A", "max_height_m": 25, "unit": "m",
                                               "datum": "natural ground level (Arabic column heading)",
                                               "distance_from_eastern_boundary_m": 1500, "warning_lighting": "required"}}],
           "confidence": "low", "confidence_reason": "read from an image whose reading is pending (test data)"}
    row.update(kw)
    return row


def _ev(ws, uid="ADD-03:p4-image/row-a", kind="reading"):
    return EvidenceRef(doc="ADD-03", unit_id=uid, page=4, kind=kind, words=ws.units_by_id[uid]["text"][:60])


def _validate(ws, prom, items, kinds=None):
    ds = W.dset(ws, items)
    rep = DS.validate(ws, ds, prom, kinds or {"reading:" + READING: "reading_rows"})
    return ds, rep


# ---------------------------------------------------------------------------------------------- the task

def test_a_pending_reading_gives_a_task_with_its_cells(ws, prom):
    ts, _ = W.tasks(ws, prom)
    t = next((x for x in ts if x["id"] == f"reading:{READING}"), None)
    assert t is not None, sorted({x["kind"] for x in ts})
    assert t["kind"] == "reading_rows" and t["status"] == "pending"
    assert t["conditional_on"] == {"reading": READING, "until": "approval"}
    units = {u["unit"]: u for u in t["units"]}
    for k in ("row-a", "row-b", "note1", "note2", "note3", "table-header"):
        u = units[f"ADD-03:p4-image/{k}"]
        assert u["pages"] == [4] and u["text"] and u["translation"]           # Arabic as printed, translation apart
        assert u["crops"] and all(c.endswith(".png") for c in u["crops"])     # traceable to the crop of its band
        assert u["bands"]
    assert "uncertain" in units["ADD-03:p4-image/row-a"]                      # the separator doubt travels with it
    assert "never in force" in t["expect"] and "conditional_on" in t["expect"]


# ---------------------------------------------------------------------------------------------- validation

def test_a_row_from_the_pending_reading_is_marked_conditional_and_not_in_force(ws, prom):
    ds, rep = _validate(ws, prom, [{"id": "R1", "statement_type": "row_new", "task": f"reading:{READING}",
                                     "provision": "ADD-03:7.1", "payload": {"row": _row(ws)}, "evidence": [_ev(ws)]}])
    it = ds.items[0]
    co = it.payload["row"].get("conditional_on")
    assert co and co["reading"] == READING and co["until"] == "approval", it.payload["row"]
    assert co["subject_sha256"] == ws.units_by_id["ADD-03:p4-image/row-a"]["reading"]["subject_sha256"]
    assert it.verification_status == "interpretation_pending", [(v.check, v.detail) for v in it.validation]
    rec = next(v for v in it.validation if v.check == "conditional_on")
    assert rec.ok and READING in rec.detail and "pending" in rec.detail
    assert rep["stages"][ROW_ID]["ADD-03"].startswith("PENDING READING"), rep["stages"][ROW_ID]


def test_the_row_must_cite_the_readings_own_units(ws, prom):
    ev = EvidenceRef(doc="ADD-03", unit_id="ADD-03:7.1", page=2, kind="span",
                     words="The Project Company shall comply with the height limits in Table 5-1")
    ds, _ = _validate(ws, prom, [{"id": "R2", "statement_type": "row_new", "task": f"reading:{READING}",
                                  "provision": "ADD-03:7.1", "payload": {"row": _row(ws)}, "evidence": [ev]}])
    it = ds.items[0]
    assert it.verification_status == "insufficient_evidence", it.verification_status
    assert any(v.check == "conditional_on" and not v.ok and "cells" in v.detail for v in it.validation)


def test_conditional_on_must_name_the_reading_the_row_rests_on(ws, prom):
    row = _row(ws, conditional_on={"reading": "VOL-II-p3-r1", "until": "approval"})
    ds, _ = _validate(ws, prom, [{"id": "R3", "statement_type": "row_new", "task": f"reading:{READING}",
                                  "provision": "ADD-03:7.1", "payload": {"row": row}, "evidence": [_ev(ws)]}])
    assert ds.items[0].verification_status == "invalid"
    assert any(v.check == "conditional_on" and "VOL-II-p3-r1" in v.detail for v in ds.items[0].validation)


def test_an_activity_for_a_conditional_row_is_conditional_too(ws, prom):
    row = _row(ws, evidence=["EV-TECH-PROPOSAL"], no_deliverable=None)
    row.pop("no_deliverable")
    act = copy.deepcopy(next(t for t in ws.r["templates"]["EV-TECH-PROPOSAL"] if t["id"] == "technical-proposal"))
    ds, _ = _validate(ws, prom, [
        {"id": "R4", "statement_type": "row_new", "task": f"reading:{READING}", "provision": "ADD-03:7.1",
         "payload": {"row": row}, "evidence": [_ev(ws)]},
        {"id": "A4", "statement_type": "activity", "task": f"reading:{READING}", "provision": "ADD-03:7.1",
         "payload": {"evidence_item": "EV-TECH-PROPOSAL", "activity": act, "rows": [ROW_ID]}, "evidence": [_ev(ws)]}])
    a = ds.items[1]
    assert a.payload["activity"].get("conditional_on", {}).get("reading") == READING, \
        (a.payload["activity"], [(v.check, v.detail) for v in a.validation])


# ---------------------------------------------------------------------------------------------- outputs

@pytest.fixture(scope="module")
def runs(ws, tmp_path_factory):
    """stage2 over a copy of the candidate with the conditional row (pending), the same with an approved-reading build
    (what a re-ingest gives after a person's approval), and the same with the reading changed since the proposal."""
    sub = ws.units_by_id["ADD-03:p4-image/row-a"]["reading"]["subject_sha256"]
    co = {"reading": READING, "until": "approval", "subject_sha256": sub}
    tmp = tmp_path_factory.mktemp("s12w3b-img")
    build = F.build(tmp_path_factory)
    act = {"id": "table-5-1-height-schedule", "name": "Height schedule against Table 5-1 (test data)", "owner": "Technical",
           "discipline": "Technical", "resource": "proposal_writers", "issuer": "Bidder", "duration": "technical_proposal",
           "predecessors": [], "successors": [], "conditional_on": {"reading": READING, "until": "approval"}}
    row = _row(ws, conditional_on=co, evidence=["EV-TECH-PROPOSAL"])
    row.pop("no_deliverable")
    pack = W.copy_candidate(tmp / "pending", rows=[row], templates={"EV-TECH-PROPOSAL": [act]})
    pending = stage2.run(build, pack, F.ROOT)
    appr = tmp / "approved-build"
    shutil.copytree(build, appr)
    data = json.loads((appr / "units.json").read_text(encoding="utf-8"))
    for u in (data["units"] if isinstance(data, dict) else data):
        if (u.get("reading") or {}).get("region") == READING:
            u["reading"]["status"] = "approved"
    (appr / "units.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    approved = stage2.run(appr, pack, F.ROOT)
    pack2 = W.copy_candidate(tmp / "changed", rows=[_row(ws, conditional_on=dict(co, subject_sha256="0" * 64))])
    changed = stage2.run(build, pack2, F.ROOT)
    return {"pending": pending, "approved": approved, "changed": changed}


def _ev_at(r, rid, stage):
    return next(e for e in r["evals"] if e["row"].id == rid)["stages"][stage]


def test_the_register_keeps_it_out_of_force_and_names_the_reading(runs):
    ev = _ev_at(runs["pending"], ROW_ID, "ADD-03")
    assert ev["status"].startswith("PENDING READING") and READING in ev["status"] and not ev["active"]
    a1 = stage2.a1_table(runs["pending"], [])
    rec = next(x for x in a1["rows"] if x["id"] == ROW_ID)
    assert rec["status:ADD-03"].startswith("PENDING READING") and READING in rec["status:ADD-03"]


def test_after_approval_the_row_is_ordinary(runs):
    ev = _ev_at(runs["approved"], ROW_ID, "ADD-03")
    assert ev["status"].startswith("NEW") and ev["active"], ev["status"]
    assert any(READING in f and "approved" in f for f in ev["flags"]), ev["flags"]
    r = runs["approved"]
    rc = dict(r, validated=r["working"], working=None)
    from tenderpack import programme as P
    acts = {a["id"]: a for a in P.stage_planner(rc, "ADD-03")(rc["assumptions"])["activities"]}
    assert "table-5-1-height-schedule" in acts and ROW_ID in acts["table-5-1-height-schedule"]["req_ids"]


def test_a_reading_changed_since_the_proposal_is_a_problem(runs):
    ev = _ev_at(runs["changed"], ROW_ID, "ADD-03")
    assert not ev["active"] and any("changed since" in p and READING in p for p in ev["problems"]), ev["problems"]


def test_a_changed_reading_file_makes_the_proposal_stale(ws, prom, tmp_path_factory):
    from tenderpack.ai.tools import Workspace
    tmp = tmp_path_factory.mktemp("s12w3b-stale")
    pack = W.copy_candidate(tmp)
    ws1 = Workspace(evidence=F.build(tmp_path_factory), pack=pack, root=F.ROOT)
    ds = W.dset(ws1, [{"id": "R5", "statement_type": "row_new", "task": f"reading:{READING}", "provision": "ADD-03:7.1",
                       "payload": {"row": _row(ws1)}, "evidence": [_ev(ws1)]}])
    p = tmp / "curation/readings" / f"{READING}.yaml"
    p.write_text(p.read_text(encoding="utf-8") + "# a person corrected a cell (test data)\n", encoding="utf-8")
    ws2 = Workspace(evidence=F.build(tmp_path_factory), pack=pack, root=F.ROOT)
    assert ws2.identity().readings_sha256 != ds.state.readings_sha256
    DS.validate(ws2, ds, W.promoted(ws2), {"reading:" + READING: "reading_rows"})
    assert ds.status == "stale" and ds.items[0].verification_status == "invalid"
    assert "readings_sha256" in ds.items[0].validation[0].detail


def test_validated_outputs_never_show_it_in_force_and_the_candidate_lists_it_apart(runs):
    r = runs["pending"]
    rc = dict(r, validated=r["working"], working=None)          # even with ADD-03 seen as the validated state
    a3 = stage2.a3(rc, stage2.collect_issues(rc, None), None)

    def ids(o):
        if isinstance(o, dict):
            return ({o["id"]} if isinstance(o.get("id"), str) else set()) | {i for v in o.values() for i in ids(v)}
        return {i for v in o for i in ids(v)} if isinstance(o, (list, tuple)) else set()
    assert ROW_ID not in ids(a3)                               # no A3 entry (an automatic issue may name it as text)
    from tenderpack import programme as P
    prog = P.stage_planner(rc, "ADD-03")(rc["assumptions"])
    assert not any(ROW_ID in (a.get("req_ids") or []) for a in prog["activities"])
    assert "table-5-1-height-schedule" not in {a["id"] for a in prog["activities"]}    # its activity is not planned
    cand = partial.compute(r)
    assert ROW_ID not in {c["row"] for c in cand["changes"]}
    cond = cand["derived"]["pending_reading_rows"]
    assert [x["row"] for x in cond] == [ROW_ID] and cond[0]["reading"] == READING
    assert "max_height_m" in json.dumps(cond[0]["parameters"])
    md = partial.markdown(cand)
    assert f"conditional on reading {READING}" in md and ROW_ID in md
    from tenderpack import programme
    readme = programme.candidate_readme(cand["a5"], cand["paragraph"])
    assert ROW_ID in readme and f"conditional on reading {READING}" in readme
    assert "table-5-1-height-schedule" in readme
    assert "table-5-1-height-schedule" not in {a["id"] for a in cand["a5"]["activities"]}
