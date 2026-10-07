"""Session 14 (W5), part 2: the controlled handoff of the owner's answers at the workflow's safe checkpoints
(tenderpack/ai/answers.py). The owner: "Notes that the workflow never consumes are not enough. The answers need to
actually flow into the controlled process ... My answers must not silently approve interpretations or overwrite the
validated baseline."

At each safe checkpoint (after readings / before analysis, before downstream, before promotion) the run takes the answers
offered to it that pass (a) the evidence checks (a fact must cite evidence found in the addendum or the pack; a judgment
is the owner's PROPOSED judgment, never an approval), (b) the staleness guard (an answer offered against a run state
that has since changed is not consumed until offered again) and (c) affected-work revalidation (the batches whose packets
it changes are re-asked, and the checkpoint records which). A consumed answer reaches the next packets as a
CONSTRAINT (a fact with verified evidence) or CONTEXT (a judgment) item and is recorded as an intervention by the person.
curation/ and out/ are never touched; an answer touching an approved reading stays pending.

The run folders here are synthetic (a checkpoint, a combined set) except the last test, which drives a RECORDED
workflow (hand-written cassette): no live model call is made and none is implied."""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from pathlib import Path

import pytest
import yaml

from ai_fixture import CASSETTES, ROOT, tree_files

PDF02 = ROOT / "rehearsals/blind-02/input/ADD-03_Addendum_No_3.pdf"          # synthetic rehearsal input (test data)
REAL = [ROOT / "curation", ROOT / "out"]
OWNER = "A. Owner"
Q1_WORDS = "Access to Administrative Building A will be refused to any person who is not so registered."
Q2_WORDS = "‘14:00 hours Riyadh time’ is deleted and ‘11:00 hours Riyadh time’ is substituted."
TEXT = {
    "ADD-03:2.1": "In Volume I Clause 6.1, as amended by Addendum No. 1 Section 2.1, " + Q2_WORDS
                  + " The date of Thursday 26 November 2026 is not changed.",
    "ADD-03:2.4": "The following new Clause 6.8 is inserted in Volume I after Clause 6.7: ‘6.8 Each Bidder shall ... "
                  + Q1_WORDS + " A Proposal that is not received ...’",
    "ADD-03:3.1": "In Volume I Clause 7.1, ‘one hundred and fifty (150) days’ is deleted and ‘one hundred and eighty "
                  "(180) days’ is substituted.",
    "VOL-I:6.6": "A Proposal received after the time stated in Clause 6.1 is a late Proposal and shall be returned "
                 "unopened.",
    "VOL-IV:F4-C/image": "خامساً ... البند ٤-٢",
}
QUESTIONS = [
    {"id": "Q1", "question": "Does a Proposal refused at the door for an unregistered courier count as late?",
     "evidence": [{"page": 1, "quotation": Q1_WORDS, "unit_id": None}], "decision_owner": "Legal"},
    {"id": "Q2", "question": "Is the new time 11:00 for every submission event?",
     "evidence": [{"page": 1, "quotation": Q2_WORDS, "unit_id": None}]},
    {"id": "Q3", "question": "Does Declaration 5 of Form 4-C refer to Volume I 4.3 rather than 4.2?",
     "evidence": [{"page": 6, "quotation": "البند ٤-٢", "unit_id": "VOL-IV:F4-C/image"}]},
]


def _units(u):
    return TEXT.get(u)


def _ans():
    from tenderpack.ai import answers
    return answers


def _qr():
    from tenderpack.ai import quick_review
    return quick_review


def _qr_folder(staging: Path, qid: str = "ADD-03-qr-test") -> Path:
    """A quick review's folder as run() leaves it: the briefing (preserved by its sha256), no answers yet."""
    QR = _qr()
    d = staging / "quick-review" / qid
    d.mkdir(parents=True)
    b = {"label": QR.LABEL, "kind": QR.KIND, "qr_id": qid, "addendum": "ADD-03", "items": [], "questions": QUESTIONS,
         "unverified_calculations": [], "not_read": []}
    (d / "briefing.json").write_text(json.dumps(b, ensure_ascii=False), encoding="utf-8")
    (d / "briefing.md").write_text(f"# {QR.LABEL}\n", encoding="utf-8")
    (d / "briefing.sha256").write_text("".join(f"{hashlib.sha256((d / n).read_bytes()).hexdigest()}  {n}\n"
                                               for n in ("briefing.json", "briefing.md")), encoding="utf-8")
    return d


def _run_folder(staging: Path, rid: str = "ADD-03-run-recorded-s14", done_upto: str = "validation") -> Path:
    """A synthetic run stopped after `done_upto`: three analysis batches done, a combined set, a candidate."""
    from tenderpack.ai.checkpoint import STEPS, Checkpoint
    rd = staging / "runs" / rid
    cp = Checkpoint.new(rd / "checkpoint.json", run_id=rid, addendum="ADD-03", settings={"route": "recorded"},
                        inputs={"pdf": {"path": str(PDF02)}})
    for s in STEPS[:STEPS.index(done_upto) + 1]:
        cp.data["steps"][s].update(status="done", finished="2026-10-07T09:00:00Z")
    plan = {"analysis-001": ["ADD-03:2.1"], "analysis-002": ["ADD-03:2.4"], "analysis-003": ["ADD-03:3.1"]}
    for bid, provs in plan.items():
        cp.data["batches"][bid] = {"phase": "analysis", "provisions": provs, "status": "done", "attempts": 1,
                                   "staged_run": f"{rid}-{bid}", "items": [p.replace(":", "/") for p in provs]}
        for p in provs:
            cp.data["provisions"][p] = {"kind": "paragraph", "pages": [1], "status": "validated", "batch": bid,
                                        "items": [p.replace(":", "/")], "accounted": True}
    cp.save()
    (rd / "ai" / f"{rid}-combined").mkdir(parents=True)
    items = [{"id": "ADD-03/2.1", "provision": "ADD-03:2.1", "target": "VOL-I:6.1", "statement_type": "amendment_op",
              "evidence": [{"unit_id": "ADD-03:2.1", "page": 1, "words": Q2_WORDS}]},
             {"id": "ADD-03/2.4", "provision": "ADD-03:2.4", "target": "VOL-I:6.7", "statement_type": "amendment_op",
              "evidence": [{"unit_id": "ADD-03:2.4", "page": 1, "words": Q1_WORDS}]},
             {"id": "ADD-03/3.1", "provision": "ADD-03:3.1", "target": "VOL-I:7.1", "statement_type": "amendment_op",
              "evidence": [{"unit_id": "ADD-03:3.1", "page": 1, "words": "180"}]}]
    (rd / "ai" / f"{rid}-combined" / "proposals.yaml").write_text(
        yaml.safe_dump({"proposal_set": {"run_id": f"{rid}-combined", "items": items}}, allow_unicode=True),
        encoding="utf-8")
    (rd / "candidate" / "curation").mkdir(parents=True)
    (rd / "candidate" / "curation" / "approvals.yaml").write_text("approvals: []\n", encoding="utf-8")
    return rd


def _cp(rd: Path):
    from tenderpack.ai.checkpoint import Checkpoint
    return Checkpoint.load(rd / "checkpoint.json")


def _approved():
    return _ans().approved_units([ROOT / "curation/approvals.yaml"], ROOT)


@pytest.fixture()
def area(tmp_path):
    staging = tmp_path / "staging" / "ai"
    return {"staging": staging, "qr": _qr_folder(staging), "rd": _run_folder(staging)}


def _offer(area, qid="Q1", answer="Yes: treat it as late.", **kw):
    QR = _qr()
    a = QR.record_answer(area["qr"], qid, answer, OWNER, **kw)
    out = QR.offer_answers(area["qr"], area["rd"])
    assert out["offered"] == [f"{area['qr'].name}/{a['id']}"], out
    return a


def _state(area, aid):
    data = yaml.safe_load((area["qr"] / "answers.yaml").read_text(encoding="utf-8"))
    return next(a for a in data["answers"] if a["id"] == aid)


# ---------------------------------------------------------------------------------------------- (a) evidence checks

def test_a_fact_answer_without_evidence_is_refused_with_the_reason(area):
    ANS = _ans()
    a = _offer(area, kind="fact")
    before = tree_files(*REAL)
    cp = _cp(area["rd"])
    rec = ANS.handoff(area["rd"], cp, "downstream", unit_text=_units, approved=_approved())
    assert rec["consumed"] == [] and rec["reasked"] == [] and rec["rerun"] == []
    assert [r["id"] for r in rec["refused"]] == [f"{area['qr'].name}/{a['id']}"]
    assert "states a fact but cites no evidence" in rec["refused"][0]["reason"]
    st = _state(area, a["id"])
    assert st["handoff"]["state"] == "refused" and "cites no evidence" in st["handoff"]["reason"]
    assert ANS.items_for(_cp(area["rd"]), "analysis", {"provisions": [{"unit_id": "ADD-03:2.4"}]}) == []
    assert tree_files(*REAL) == before


def test_a_fact_whose_quotation_is_not_in_the_addendum_or_the_pack_is_refused(area):
    ANS = _ans()
    a = _offer(area, kind="fact", evidence=["page 1: the Proposal Due Date is moved to 3 December 2026",
                                            "VOL-I:9.9: anything at all"])
    rec = ANS.handoff(area["rd"], _cp(area["rd"]), "downstream", unit_text=_units, approved=_approved())
    assert rec["consumed"] == [] and len(rec["refused"]) == 1
    why = rec["refused"][0]["reason"]
    assert "NOT FOUND on page 1" in why and "VOL-I:9.9" in why and "not a unit" in why
    assert _state(area, a["id"])["handoff"]["state"] == "refused"


# ---------------------------------------------------------------------------------------------- (b) staleness

def test_a_stale_answer_is_not_consumed_until_it_is_offered_again(area):
    ANS, QR = _ans(), _qr()
    a = _offer(area, kind="fact", evidence=[f"page 1: {Q1_WORDS}"])
    p = area["rd"] / "ai" / f"{area['rd'].name}-combined" / "proposals.yaml"
    p.write_text(p.read_text(encoding="utf-8") + "# the run changed after the offer\n", encoding="utf-8")
    rec = ANS.handoff(area["rd"], _cp(area["rd"]), "downstream", unit_text=_units, approved=_approved())
    nid = f"{area['qr'].name}/{a['id']}"
    assert rec["consumed"] == [] and rec["stale"] == [nid] and rec["reasked"] == []
    assert _state(area, a["id"])["handoff"]["state"] == "stale"
    # still stale at the next checkpoint: never consumed against a state it was not checked against
    rec = ANS.handoff(area["rd"], _cp(area["rd"]), "downstream", unit_text=_units, approved=_approved())
    assert rec["consumed"] == []
    # offered again (re-checked against the current state): consumed
    out = QR.offer_answers(area["qr"], area["rd"])
    assert out["offered"] == [nid]
    rec = ANS.handoff(area["rd"], _cp(area["rd"]), "downstream", unit_text=_units, approved=_approved())
    assert rec["consumed"] == [nid]


# ---------------------------------------------------------------------------------------------- (c) revalidation

def test_a_consumed_answer_re_asks_exactly_the_affected_batch(area):
    ANS = _ans()
    before = tree_files(*REAL)
    a = _offer(area, kind="fact", evidence=[f"page 1: {Q1_WORDS}", "VOL-I:6.6: is a late Proposal"])
    cp = _cp(area["rd"])
    rec = ANS.handoff(area["rd"], cp, "downstream", unit_text=_units, approved=_approved(), now="2026-10-07T10:00:00Z")
    nid = f"{area['qr'].name}/{a['id']}"
    assert rec["consumed"] == [nid]
    assert rec["reasked"] == ["analysis-002"]                           # exactly the batch whose packet it changes
    assert rec["rerun"] == ["analysis", "validation"]
    cp = _cp(area["rd"])
    assert cp.batch("analysis-002")["status"] == "pending" and cp.provision("ADD-03:2.4")["status"] == "pending"
    assert cp.batch("analysis-002")["reasked_for"] == [nid]
    for bid, p in (("analysis-001", "ADD-03:2.1"), ("analysis-003", "ADD-03:3.1")):
        assert cp.batch(bid)["status"] == "done" and cp.provision(p)["status"] == "validated"
    assert cp.step("analysis")["status"] == "pending" and cp.step("validation")["status"] == "pending"
    # the checkpoint records which work it revalidated; the person's intervention is named and timed
    ck = cp.data["owner_answers"]["checkpoints"][-1]
    assert ck["step"] == "downstream" and ck["checkpoint"] == "before downstream" and ck["reasked"] == ["analysis-002"]
    iv = [i for i in cp.data["interventions"] if i.get("kind") == "owner answer consumed"]
    assert len(iv) == 1 and iv[0]["by"] == OWNER and iv[0]["ts"] == "2026-10-07T10:00:00Z"
    assert iv[0]["answer_recorded"] == a["recorded"] and iv[0]["batches_reasked"] == ["analysis-002"]
    # the answer reaches the re-asked batch's packet as a CONSTRAINT item, and no other batch's
    it = ANS.items_for(cp, "analysis", {"provisions": [{"unit_id": "ADD-03:2.4"}]})
    assert len(it) == 1 and it[0]["role"] == "constraint" and it[0]["by"] == OWNER
    assert it[0]["status"].startswith("PROPOSED") and "approval" in it[0]["status"]
    assert it[0]["evidence_checks"] and all(c["ok"] for c in it[0]["evidence_checks"])
    assert ANS.items_for(cp, "analysis", {"provisions": [{"unit_id": "ADD-03:2.1"}]}) == []
    st = _state(area, a["id"])
    assert st["handoff"]["state"] == "consumed" and st["handoff"]["checkpoint"] == "before downstream"
    # consumed once: the next checkpoint does not consume or re-ask it again
    rec = ANS.handoff(area["rd"], cp, "promotion", unit_text=_units, approved=_approved())
    assert rec["consumed"] == [] and rec["reasked"] == []
    assert tree_files(*REAL) == before                                 # curation/ and out/ untouched


def test_before_analysis_the_answer_rides_with_the_batches_it_concerns_and_nothing_is_re_asked(tmp_path):
    ANS = _ans()
    staging = tmp_path / "st" / "ai"
    area = {"staging": staging, "qr": _qr_folder(staging), "rd": _run_folder(staging, done_upto="readings")}
    cp = _cp(area["rd"])
    for bid in list(cp.data["batches"]):                    # not planned yet: the analysis step plans its batches
        del cp.data["batches"][bid]
    for p in cp.data["provisions"].values():
        p.update(status="pending", items=[])
    cp.save()
    a = _offer(area, qid="Q2", kind="fact", evidence=[f"page 1: {Q2_WORDS}"])
    rec = ANS.handoff(area["rd"], _cp(area["rd"]), "analysis", unit_text=_units, approved=_approved())
    assert rec["consumed"] == [f"{area['qr'].name}/{a['id']}"] and rec["reasked"] == [] and rec["rerun"] == []
    ck = _cp(area["rd"]).data["owner_answers"]["checkpoints"][-1]
    assert ck["checkpoint"] == "after readings, before analysis" and ck["asked_with"] == ["ADD-03:2.1"]
    pk = ANS.with_packet(_cp(area["rd"]), {"provisions": [{"unit_id": "ADD-03:2.1"}]}, "analysis")
    assert pk["owner_answers"]["items"][0]["answer"] == "Yes: treat it as late."
    assert "never an approval" in pk["owner_answers"]["note"]
    assert "owner_answers" not in ANS.with_packet(_cp(area["rd"]), {"provisions": [{"unit_id": "ADD-03:3.1"}]},
                                                  "analysis")


def test_a_judgment_is_the_owners_proposed_judgment_never_an_approval(area):
    ANS = _ans()
    before = tree_files(*REAL)
    a = _offer(area, answer="I would treat it as late, but Legal decides.")       # kind defaults to judgment
    rec = ANS.handoff(area["rd"], _cp(area["rd"]), "downstream", unit_text=_units, approved=_approved())
    nid = f"{area['qr'].name}/{a['id']}"
    assert rec["consumed"] == [nid] and rec["reasked"] == ["analysis-002"]
    it = ANS.items_for(_cp(area["rd"]), "analysis", {"provisions": [{"unit_id": "ADD-03:2.4"}]})[0]
    assert it["role"] == "context" and it["kind"] == "judgment" and it["decision_owner"] == OWNER
    assert "never" in it["how_to_use"] and "approval" in it["how_to_use"]
    cand = yaml.safe_load((area["rd"] / "candidate" / "owner_answers.yaml").read_text(encoding="utf-8"))
    rec0 = cand["answers"][0]
    assert rec0["status"] == "PROPOSED" and rec0["by"] == OWNER and "accept/reject" in rec0["decision"]
    text = json.dumps(cand, ensure_ascii=False).lower() + json.dumps(it, ensure_ascii=False).lower()
    assert '"approved"' not in text and '"accepted"' not in text
    assert (area["rd"] / "candidate" / "curation" / "approvals.yaml").read_text(encoding="utf-8") == "approvals: []\n"
    assert tree_files(*REAL) == before


def test_an_answer_that_would_change_an_approved_readings_interpretation_stays_pending(area):
    ANS = _ans()
    before = tree_files(ROOT / "curation")
    a = _offer(area, qid="Q3", answer="It refers to 4.3.", kind="fact",
               evidence=["VOL-IV:F4-C/image: البند ٤-٢"])
    rec = ANS.handoff(area["rd"], _cp(area["rd"]), "downstream", unit_text=_units, approved=_approved())
    nid = f"{area['qr'].name}/{a['id']}"
    assert rec["consumed"] == [] and rec["reasked"] == [] and [p["id"] for p in rec["pending"]] == [nid]
    assert "approved reading VOL-IV-p6-r1" in rec["pending"][0]["reason"]
    st = _state(area, a["id"])
    assert st["handoff"]["state"] == "pending" and "never applied" in st["handoff"]["reason"]
    cp = _cp(area["rd"])
    assert all(b["status"] == "done" for b in cp.data["batches"].values())
    assert not any(ANS.items_for(cp, "analysis", {"provisions": [{"unit_id": p}]}) for p in cp.data["provisions"])
    cand = yaml.safe_load((area["rd"] / "candidate" / "owner_answers.yaml").read_text(encoding="utf-8"))
    assert cand["answers"][0]["status"] == "PENDING" and "accept/reject" in cand["answers"][0]["decision"]
    assert tree_files(ROOT / "curation") == before


def test_an_answer_held_while_a_step_ran_is_offered_and_consumed_at_the_next_safe_checkpoint(area):
    ANS, QR = _ans(), _qr()
    cp = _cp(area["rd"])
    cp.data["steps"]["validation"]["status"] = "running"
    cp.save()
    a = QR.record_answer(area["qr"], "Q1", "Yes.", OWNER, kind="fact", evidence=[f"page 1: {Q1_WORDS}"])
    assert QR.offer_answers(area["qr"], area["rd"])["held"]
    cp = _cp(area["rd"])
    cp.data["steps"]["validation"]["status"] = "done"
    cp.save()
    rec = ANS.handoff(area["rd"], cp, "downstream", unit_text=_units, approved=_approved())
    assert rec["offered"] == [f"{area['qr'].name}/{a['id']}"] and rec["consumed"] == rec["offered"]


def test_with_packet_leaves_a_run_without_answers_byte_for_byte_alone(area):
    ANS = _ans()
    pk = {"provisions": [{"unit_id": "ADD-03:2.4"}], "x": 1}
    assert ANS.with_packet(_cp(area["rd"]), pk, "analysis") is pk


# ---------------------------------------------------------------------------------------------- the real workflow

@pytest.fixture(scope="module")
def prev_build(tmp_path_factory):
    from tenderpack.cli import ingest
    out = tmp_path_factory.mktemp("w14-prev") / "build"
    assert ingest(ROOT / "config/pack.yaml", out, ROOT, quiet=True)["exit_code"] == 0
    return out


def test_the_workflow_consumes_an_offered_answer_at_its_checkpoint_and_re_asks_the_batch(prev_build, tmp_path,
                                                                                          monkeypatch):
    from tenderpack.ai import workflow as W
    quiet = lambda *a, **k: None  # noqa: E731
    cas = yaml.safe_load((CASSETTES / "workflow_add03.yaml").read_text(encoding="utf-8"))
    s1 = next(s for s in cas["sessions"] if "ADD-03:2.1" in (s.get("when") or {}).get("provisions_include", []))
    cas["sessions"].insert(cas["sessions"].index(s1) + 1, json.loads(json.dumps(s1)))   # the re-ask's recording
    cpath = tmp_path / "cassette.yaml"
    cpath.write_text(yaml.safe_dump(cas, allow_unicode=True, sort_keys=False), encoding="utf-8")
    staging = tmp_path / "staging"
    before = tree_files(*REAL)
    res = W.start("ADD-03", PDF02, pack=ROOT / "config/pack.yaml", evidence=prev_build, staging=staging,
                  worklog=tmp_path / "wl", run_id="ans", batch_size=8, route="recorded", cassette=cpath,
                  background_before=False, stop_after="validation", echo=quiet, sleep=lambda s: None)
    assert res["status"] == "stopped", res
    rd = staging / "runs" / "ans"
    cp0 = json.loads((rd / "checkpoint.json").read_text(encoding="utf-8"))
    bid = cp0["provisions"]["ADD-03:2.1"]["batch"]
    attempts = {k: v.get("attempts") for k, v in cp0["batches"].items()}
    d = _qr_folder(staging)
    QR = _qr()
    a = QR.record_answer(d, "Q2", "Yes, 11:00 throughout.", OWNER, kind="fact", evidence=[f"page 1: {Q2_WORDS}"])
    assert QR.offer_answers(d, rd)["offered"]
    packets = []
    real = W._request

    def spy(ctx, sp, prov, packet, bid_, **kw):
        packets.append((bid_, packet))
        return real(ctx, sp, prov, packet, bid_, **kw)
    monkeypatch.setattr(W, "_request", spy)
    # the run stopped after validation: nothing was consumed yet (the checkpoint before downstream is not reached)
    assert "owner_answers" not in json.loads((rd / "checkpoint.json").read_text(encoding="utf-8"))
    res = W.resume("ans", staging, stop_after="downstream", echo=quiet, sleep=lambda s: None)
    cp = json.loads((rd / "checkpoint.json").read_text(encoding="utf-8"))
    nid = f"{d.name}/{a['id']}"
    # taken at the FIRST safe checkpoint the resumed run reaches: the resume retries the batch that failed (the
    # cassette records no session for it), so the run re-enters the analysis step: "after readings, before analysis"
    cks = [c for c in cp["owner_answers"]["checkpoints"] if c["consumed"]]
    assert len(cks) == 1 and cks[0]["consumed"] == [nid], json.dumps(cp["owner_answers"], ensure_ascii=False)[:3000]
    assert cks[0]["checkpoint"] == "after readings, before analysis"
    assert cks[0]["reasked"] == [bid]                                       # exactly the batch the answer concerns
    assert cp["batches"][bid]["attempts"] == attempts[bid] + 1 and cp["batches"][bid]["status"] == "done"
    done_before = [k for k, v in cp0["batches"].items() if v["status"] == "done" and k != bid]
    assert done_before and {k: cp["batches"][k]["attempts"] for k in done_before} == \
        {k: attempts[k] for k in done_before}                                # not asked again
    sent = [p for b, p in packets if b == bid]
    assert sent and sent[0]["owner_answers"]["items"][0]["role"] == "constraint"
    assert sent[0]["owner_answers"]["items"][0]["by"] == OWNER
    assert [b for b, p in packets if b != bid and b.startswith("analysis") and "owner_answers" in p] == []
    ds = [p["owner_answers"]["items"][0]["id"] for b, p in packets if b.startswith("downstream") and "owner_answers" in p]
    assert set(ds) <= {nid}                     # a downstream packet carries it only for tasks of its scope
    assert cp["batches"][bid]["owner_answers"] == [nid]
    assert any(i.get("kind") == "owner answer consumed" and i.get("by") == OWNER for i in cp["interventions"])
    assert cp["steps"]["downstream"]["status"] == "done"
    assert (rd / "candidate" / "owner_answers.yaml").is_file()
    assert tree_files(*REAL) == before


# ---------------------------------------------------------------------------------------------- the panel

@pytest.fixture()
def panel(tmp_path, blind02_build):
    from tenderpack.panel.server import Panel, PanelConfig
    cfg = PanelConfig(root=ROOT, pack=ROOT / "config/pack.yaml", evidence=blind02_build, out=tmp_path / "out",
                      staging=tmp_path / "staging" / "ai", worklog=tmp_path / "worklog", panel_dir=tmp_path / "panel",
                      cassette=tmp_path / "c.yaml")
    p = Panel(cfg, 0, log=open(os.devnull, "w"))
    p._routes = (time.time() + 3600, {"offline": None, "routes": [
        {"route": "host", "status": {"status": "tested"}, "available": True}]}, None)
    p.host_found = lambda: True
    p.start()
    yield p
    p.stop()


def _get(p, path):
    import html
    import urllib.request
    with urllib.request.urlopen(p.url + path, timeout=60) as r:
        return html.unescape(r.read().decode("utf-8", "replace"))


def test_the_panel_shows_the_briefing_as_preliminary_and_each_answers_state_with_no_approve_button(panel):
    ANS, QR = _ans(), _qr()
    staging = panel.cfg.staging
    area = {"staging": staging, "qr": _qr_folder(staging), "rd": _run_folder(staging)}
    a1 = _offer(area, kind="fact")                                                  # refused: no evidence
    QR.record_answer(area["qr"], "Q1", "Late, in my view.", OWNER)                  # a judgment, offered
    QR.offer_answers(area["qr"], area["rd"])
    ANS.handoff(area["rd"], _cp(area["rd"]), "downstream", unit_text=_units, approved=_approved())
    QR.record_answer(area["qr"], "Q2", "Not yet offered.", OWNER)
    page = _get(panel, f"quickreview/{area['qr'].name}")
    assert QR.KIND in page and QR.LABEL in page
    assert "refused: the answer states a fact but cites no evidence" in page
    assert "consumed at before downstream" in page and "recorded (not offered yet)" in page
    buttons = re.findall(r"<button[^>]*>(.*?)</button>", page, flags=re.S)
    actions = re.findall(r'(?:action|formaction)="([^"]*)"', page)
    assert buttons and actions
    for x in buttons + actions:                                       # never a button or a form that approves
        assert not re.search(r"approv|accept|reject", x, flags=re.I), x
    assert 'name="kind"' in page and 'name="evidence"' in page
    run_page = _get(panel, f"runs/{area['rd'].name}")
    assert "consumed at before downstream" in run_page and "refused" in run_page
    assert a1["id"] in run_page


def test_the_panel_records_an_answers_kind_and_evidence(panel):
    import urllib.parse
    import urllib.request
    staging = panel.cfg.staging
    d = _qr_folder(staging)
    form = urllib.parse.urlencode({"question": "Q2", "answer": "Yes, 11:00.", "name": OWNER, "kind": "fact",
                                   "evidence": f"page 1: {Q2_WORDS}\nVOL-I:6.6: is a late Proposal\n"}).encode()

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    import urllib.error
    try:
        urllib.request.build_opener(NoRedirect).open(urllib.request.Request(
            panel.url + f"quickreview/{d.name}/answer", data=form,
            headers={"Content-Type": "application/x-www-form-urlencoded"}), timeout=60)
        loc = None
    except urllib.error.HTTPError as e:
        assert e.code == 303
        loc = e.headers["Location"]
    jid = re.search(r"/jobs/([^/]+)$", loc).group(1)
    t0 = time.time()
    while panel.jobs.get(jid)["status"] == "running" and time.time() - t0 < 120:
        time.sleep(0.3)
    j = panel.jobs.get(jid)
    assert j["exit_code"] == 0, panel.jobs.log_text(j)
    assert j["argv"].count("--cite") == 2 and j["argv"][j["argv"].index("--kind") + 1] == "fact"
    a = yaml.safe_load((d / "answers.yaml").read_text(encoding="utf-8"))["answers"][0]
    assert a["kind"] == "fact" and [c.get("unit_id") for c in a["answer_evidence"]] == [None, "VOL-I:6.6"]
    assert a["answer_evidence"][0]["page"] == 1 and a["answer_evidence"][0]["quotation"] == Q2_WORDS
