"""Session 13, part 4: the optional parallel AI QUICK REVIEW (tenderpack/ai/quick_review.py, `tenderpack ai quick-review`,
the panel's "Start AI quick review" and "Quick review" page).

The owner: "while the main AI-plus-code pipeline runs, let me start a separate, bounded AI reading from the panel ...
label everything as a preliminary AI briefing. it must not edit authoritative data, approve items or mark pipeline work
complete ... preserve its initial findings, then compare them with the pipeline results ... model agreement is not
proof. record my answers against the exact questions/evidence and incorporate them at safe checkpoints with
revalidation. keep this pass short and lower priority ... measure time to the first useful briefing separately from
time to updated A1-A5."

Every provider exchange here is RECORDED (a hand-written cassette) or a FAKE host CLI: no live call is made and none is
implied. The briefings these tests produce show the plumbing (one bounded session, the policy, the read-only tools on the
published workspace, the files, the comparison, the answers, the safe checkpoints), never how well a model reads an
addendum."""
from __future__ import annotations

import html
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import pytest
import yaml

from ai_fixture import ROOT, workspace

PDF02 = ROOT / "rehearsals/blind-02/input/ADD-03_Addendum_No_3.pdf"          # synthetic rehearsal inputs
PDF06 = ROOT / "rehearsals/blind-06/input/ADD-03_Addendum_No_3.pdf"          # page 4 carries an image region
RUN06 = ROOT / "rehearsals/blind-06"                                          # a recorded run (read only)
TOOLS5 = ("search_evidence", "get_unit", "get_group", "get_crop", "compare_state")
LABEL = ("PRELIMINARY AI BRIEFING — unverified: not a decision, not a validation; calculations and interpretations "
         "unchecked")
NOT_PROOF = "model agreement is not proof: every item is verified only by the validators and a person"


def _qr():
    from tenderpack.ai import quick_review
    return quick_review


BRIEFING = {
    "addendum": "ADD-03",
    "items": [
        {"id": "P1", "provision": "2.1", "page": 1,
         "quotation": "‘14:00 hours Riyadh time’ is deleted and ‘11:00 hours Riyadh time’ is substituted.",
         "target_unit_guess": "VOL-I:6.1", "kind": "replace", "deliverables": ["A1", "A2", "A5"], "rows": [],
         "confidence": "high", "uncertainty_class": "none", "uncertainty": None,
         "propagation": ["the submission milestone of A5"]},
        {"id": "P2", "provision": "2.4", "page": 1,
         "quotation": "The following new Clause 6.8 is inserted in Volume I after Clause 6.7:",
         "target_unit_guess": "VOL-I:6.7", "kind": "insert", "deliverables": ["A1", "A3"], "rows": [],
         "confidence": "medium", "uncertainty_class": "genuine ambiguity",
         "uncertainty": "ambiguous: whether the refusal of access is a rejection consequence for A3"},
    ],
    "questions": [
        {"id": "Q1", "question": "Does a Proposal refused at the door for an unregistered courier count as late?",
         "evidence": [{"page": 1, "quotation": "Access to Administrative Building A will be refused to any person "
                                               "who is not so registered.", "unit_id": None}],
         "decision_owner": "Legal", "why": "A3 consequence"},
    ],
    "unverified_calculations": [
        {"id": "C1", "what": "the registration deadline (five Working Days before the Proposal Due Date)",
         "inputs": [{"page": 1, "quotation": "not later than five (5) Working Days before the Proposal Due Date",
                     "unit_id": None}],
         "model_result_unverified": "19 November 2026", "why_unverified": "no calculation tool in the quick review"},
    ],
    "not_read": [],
    "model_rationale": "read pages 1-4; looked up VOL-I:6.1 at ADD-02",
}


def tree_files(*dirs: Path) -> dict[str, str]:
    import hashlib
    return {p.as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for base in dirs if Path(base).exists()
            for p in sorted(Path(base).rglob("*")) if p.is_file()}


def _cassette(briefing: dict | None = None, tool=("get_unit", {"unit_id": "VOL-I:6.1", "stage": "ADD-02"})) -> dict:
    turns = []
    if tool:
        turns.append({"response": {"text": "", "tool_calls": [{"id": "t1", "name": tool[0], "arguments": tool[1]}],
                                   "usage": {"input_tokens": 900, "output_tokens": 40}}})
    turns.append({"response": {"text": json.dumps(briefing or BRIEFING, ensure_ascii=False),
                               "usage": {"input_tokens": 1200, "output_tokens": 600}}})
    return {"name": "quick-review (hand-written; not a model's output)", "model": "recorded-fixture-model",
            "capabilities": {"images": True, "tools": True, "structured_output": False, "context_tokens": 400000,
                             "source": "cassette (recorded fixture)"}, "turns": turns}


@pytest.fixture(scope="module")
def ws(tmp_path_factory, blind02_build):
    """The PUBLISHED ADD-02 workspace of the tests: blind-02's pack at ADD-02 and its evidence build (disposable)."""
    return workspace(tmp_path_factory.mktemp("qr-ws"), evidence=blind02_build)


def _run(ws, tmp_path, cassette=None, **kw):
    QRm = _qr()
    staging = kw.pop("staging", tmp_path / "staging" / "ai")
    cas = tmp_path / "cassette.yaml"
    cas.write_text(yaml.safe_dump(cassette or _cassette(), allow_unicode=True, sort_keys=False), encoding="utf-8")
    return QRm.run("ADD-03", kw.pop("pdf", PDF02), route=kw.pop("route", "recorded"), evidence=ws.evidence,
                   pack=ws.pack, staging=staging, worklog=tmp_path / "worklog", ai_config=ROOT / "config/ai.yaml",
                   cassette=cas, **kw)


# ---------------------------------------------------------------------------------------------- (1) the policy phase

@pytest.mark.parametrize("route", ["recorded", "anthropic", "openrouter", "ollama", "host"])
def test_the_quick_review_phase_is_composed_by_the_policy_with_only_the_retrieval_tools(route):
    from tenderpack.ai import policy as P
    from tenderpack.ai import requests as R
    text = P.compose("quick_review", route)
    assert text.splitlines()[0].startswith(f"POLICY {P.identity()['sha256']} phase=quick_review")
    assert "# Phase: quick review" in text
    assert "You PROPOSE; you decide nothing." in text                     # the shared sections come first
    assert "PRELIMINARY AI BRIEFING" in text and "never decide" in text.lower()
    # session 14 (W5): this asserted the defect "host route without page images" (report s13 §6); the host route now
    # also has the ONE read-only tool scoped to the new addendum's own pages (tests/test_session14_quick_review_pages.py)
    assert P.tools("quick_review", route) == TOOLS5 + (("get_addendum_page",) if route == "host" else ())
    assert not {"simulate_amendment", "calculate", "validate_proposal"} & set(P.tools("quick_review", route))
    assert "submit_proposals" not in P.tools("quick_review", route)
    if route == "host":
        assert "reply with ONLY the JSON" in text and "read-only" in text  # host-answer mechanics
    sp = R.spec("quick_review", route=route if route != "host" else "api")
    assert sp.tools == TOOLS5 and sp.system == P.compose("quick_review", "api")
    with pytest.raises(P.PolicyError):
        R.spec("quick_review", system="You are a helpful reviewer.")       # a hand-written prompt is refused
    with pytest.raises(P.PolicyError):
        R.spec("quick_review", tools=["simulate_amendment"])               # deny-by-default


def test_the_runtime_instructions_doc_lists_the_quick_review_phase():
    from tenderpack.ai import policy as P
    assert (ROOT / "tenderpack/ai/policy/70_quick_review.md").is_file()
    assert (ROOT / "docs/RUNTIME_INSTRUCTIONS.md").read_text(encoding="utf-8") == P.render_doc()
    assert "quick_review: search_evidence, get_unit, get_group, get_crop, compare_state" in P.render_doc()


# ---------------------------------------------------------------------------------------------- (2) one bounded session

def test_a_recorded_quick_review_writes_the_labelled_briefing_timing_and_hash(ws, tmp_path):
    res = _run(ws, tmp_path)
    assert res["exit_code"] == 0, res
    d = Path(res["dir"])
    assert d.parent == tmp_path / "staging" / "ai" / "quick-review" and d.name == res["qr_id"]
    b = json.loads((d / "briefing.json").read_text(encoding="utf-8"))
    md = (d / "briefing.md").read_text(encoding="utf-8")
    assert md.splitlines()[0] == f"# {LABEL}" and b["label"] == LABEL
    assert [i["id"] for i in b["items"]] == ["P1", "P2"] and b["questions"][0]["id"] == "Q1"
    it = b["items"][0]
    for k in ("provision", "page", "quotation", "target_unit_guess", "kind", "deliverables", "confidence",
              "uncertainty_class"):
        assert k in it
    assert b["unverified_calculations"][0]["model_result_unverified"] == "19 November 2026"
    assert "unverified" in md.lower() and "19 November 2026" in md
    # the program's checks are labelled as checks, never as validation
    assert b["items"][0]["checks"]["quotation"].startswith("verbatim")
    assert b["items"][0]["checks"]["target"].startswith("a unit of the ADD-02 workspace")
    assert b["workspace"]["stage"] == "ADD-02" and b["session"] == {"sessions": 1, "batches": 0, "critic": False}
    t = json.loads((d / "timing.json").read_text(encoding="utf-8"))
    for k in ("start", "first_useful_briefing", "end", "seconds_to_first_briefing", "tokens"):
        assert t.get(k) is not None, k
    assert t["tokens"]["input_tokens"] == 2100 and t["tokens"]["output_tokens"] == 640 and t["tokens"]["calls"] == 2
    sha = (d / "briefing.sha256").read_text(encoding="utf-8")
    import hashlib
    for f in ("briefing.json", "briefing.md"):
        assert f"{hashlib.sha256((d / f).read_bytes()).hexdigest()}  {f}" in sha
    assert _qr().preserved(d)["ok"] is True
    log = [json.loads(x) for x in (d / "log.jsonl").read_text(encoding="utf-8").splitlines()]
    calls = [e for e in log if e.get("event") == "tool_call"]
    assert [c["name"] for c in calls] == ["get_unit"] and calls[0]["ok"] is True
    prompt = next(e for e in log if e.get("event") == "prompt")
    assert prompt["tools"] == list(TOOLS5)
    assert prompt["system"].startswith("POLICY ") and "phase=quick_review" in prompt["system"].splitlines()[0]


def test_a_quick_review_attaches_the_page_images_of_image_regions(ws, tmp_path):
    res = _run(ws, tmp_path, pdf=PDF06)
    assert res["exit_code"] == 0, res
    d = Path(res["dir"])
    log = [json.loads(x) for x in (d / "log.jsonl").read_text(encoding="utf-8").splitlines()]
    prompt = next(e for e in log if e.get("event") == "prompt")
    req = json.loads((d / "request.json").read_text(encoding="utf-8"))
    assert [i["page"] for i in req["images"]] == [4]                       # the page with the image region
    assert len(prompt["images"]) == 1 and prompt["images"][0]["sha256"] == req["images"][0]["sha256"]
    assert (d / "pages" / "page-4.png").is_file()


def test_the_quick_review_gets_the_published_workspace_never_a_runs_staging(ws, tmp_path):
    """The tool list and the workspace are the published ADD-02 ones; the main run's proposals, candidate and packet
    are never read (a run's folder sits beside it in the same staging)."""
    QRm = _qr()
    staging = tmp_path / "staging" / "ai"
    run = staging / "runs" / "ADD-03-run-recorded-x"
    (run / "candidate" / "build").mkdir(parents=True)
    (run / "ai" / "ADD-03-run-recorded-x-combined").mkdir(parents=True)
    (run / "ai" / "ADD-03-run-recorded-x-combined" / "proposals.yaml").write_text("SECRET-RUN-PROPOSAL\n")
    (run / "checkpoint.json").write_text(json.dumps({"run_id": "ADD-03-run-recorded-x", "steps": {}}))
    res = _run(ws, tmp_path, staging=staging)
    assert res["exit_code"] == 0
    d = Path(res["dir"])
    req = json.loads((d / "request.json").read_text(encoding="utf-8"))
    assert req["workspace"]["evidence"] == str(Path(ws.evidence).resolve())
    assert req["workspace"]["pack"] == str(Path(ws.pack).resolve())
    assert req["tools"] == list(TOOLS5) and req["main_run_inputs_read"] == []
    blob = (d / "log.jsonl").read_text(encoding="utf-8") + (d / "request.json").read_text(encoding="utf-8")
    assert "SECRET-RUN-PROPOSAL" not in blob and "/runs/" not in blob
    # a workspace inside a run's staging is refused before any call
    with pytest.raises(QRm.QuickReviewError, match="published"):
        QRm.run("ADD-03", PDF02, route="recorded", evidence=run / "candidate" / "build", pack=ws.pack,
                staging=staging, worklog=tmp_path / "wl", ai_config=ROOT / "config/ai.yaml",
                cassette=tmp_path / "cassette.yaml")


def test_a_quick_review_tool_call_outside_the_retrieval_tools_is_refused(ws, tmp_path):
    res = _run(ws, tmp_path, cassette=_cassette(tool=("simulate_amendment", {"addendum": "ADD-03", "ops": []})))
    assert res["exit_code"] == 0
    log = [json.loads(x) for x in (Path(res["dir"]) / "log.jsonl").read_text(encoding="utf-8").splitlines()]
    call = next(e for e in log if e.get("event") == "tool_call")
    assert call["ok"] is False and "no tool 'simulate_amendment' is available here" in call["result"]


def test_the_host_route_runs_one_answer_session_with_exactly_the_retrieval_tools_and_no_lock(ws, tmp_path):
    from tenderpack.ai import budget as B
    from tenderpack.ai import policy as P
    staging = tmp_path / "staging" / "ai"
    staging.mkdir(parents=True)
    held = B.acquire(B.safe_staging(staging, ws.root, ws.evidence), "ADD-03",
                     {"route": "host", "run_id": "the-main-run", "pid": os.getpid()}, 120)   # the main run's lock
    seen = []

    def runner(cmd, input=None, **kw):
        seen.append({"cmd": cmd, "input": input, "kw": kw})
        lines = [{"type": "system", "subtype": "init", "model": "fake-host-model", "tools": []},
                 {"type": "result", "subtype": "success", "is_error": False, "num_turns": 3,
                  "result": json.dumps(BRIEFING, ensure_ascii=False), "usage": {"input_tokens": 10, "output_tokens": 5},
                  "modelUsage": {"fake-host-model": {}}}]
        return subprocess.CompletedProcess(cmd, 0, "\n".join(json.dumps(x) for x in lines), "")
    try:
        res = _qr().run("ADD-03", PDF02, route="host", evidence=ws.evidence, pack=ws.pack, staging=staging,
                        worklog=tmp_path / "wl", ai_config=ROOT / "config/ai.yaml", runner=runner,
                        claude_bin=sys.executable)
    finally:
        held.release()
    assert res["exit_code"] == 0, res
    assert len(seen) == 1                                                  # ONE session, no repair needed
    cmd = seen[0]["cmd"]
    allowed = cmd[cmd.index("--allowedTools") + 1].split(",")
    # session 14 (W5): + get_addendum_page (the defect "host route without page images", report s13 §6)
    assert allowed == ["mcp__tenderpack__" + t for t in TOOLS5 + ("get_addendum_page",)]
    assert cmd[cmd.index("--system-prompt") + 1] == P.compose("quick_review", "host")
    mcp = json.loads(Path(cmd[cmd.index("--mcp-config") + 1]).read_text(encoding="utf-8"))
    args = mcp["mcpServers"]["tenderpack"]["args"]
    assert args[args.index("--tools") + 1] == ",".join(TOOLS5 + ("get_addendum_page",)) and "--submit-once" not in args
    assert args[args.index("--evidence") + 1] == str(Path(ws.evidence).resolve())
    assert args[args.index("--pack") + 1] == str(Path(ws.pack).resolve())
    b = json.loads((Path(res["dir"]) / "briefing.json").read_text(encoding="utf-8"))
    assert b["route"] == "host" and len(b["items"]) == 2


@pytest.mark.parametrize("route", ["host", "anthropic", "openrouter"])
def test_offline_mode_refuses_a_hosted_quick_review_before_any_call(ws, tmp_path, monkeypatch, route):
    monkeypatch.setenv("TENDERPACK_OFFLINE", "1")
    started = []
    from tenderpack.ai.offline import OfflineError
    with pytest.raises(OfflineError):
        _qr().run("ADD-03", PDF02, route=route, evidence=ws.evidence, pack=ws.pack, staging=tmp_path / "s",
                  worklog=tmp_path / "wl", ai_config=ROOT / "config/ai.yaml", model="m",
                  runner=lambda *a, **k: started.append(a))
    assert started == [] and not (tmp_path / "s" / "quick-review").exists()


def test_a_paid_route_needs_the_owners_caps_before_the_quick_reviews_own(ws, tmp_path, monkeypatch):
    """The quick review tightens the caps (its budget and token cap) but never stands in for the owner's: a paid route
    whose caps the owner has not set in config/ai.yaml is refused before any call."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    res = _qr().run("ADD-03", PDF02, route="anthropic", model="claude-opus-5-5", evidence=ws.evidence, pack=ws.pack,
                    staging=tmp_path / "s", worklog=tmp_path / "wl", ai_config=ROOT / "config/ai.yaml")
    assert res["exit_code"] == 2 and "makes paid calls" in res["error"]
    assert not (Path(res["dir"]) / "briefing.json").exists() and not (tmp_path / "s" / "spend.jsonl").exists()


def test_a_second_quick_review_is_refused_while_one_runs(ws, tmp_path):
    QRm = _qr()
    staging = tmp_path / "staging" / "ai"
    lock = QRm.SessionLock(staging).acquire()
    try:
        with pytest.raises(QRm.QuickReviewError, match="one quick review at a time"):
            _run(ws, tmp_path, staging=staging)
    finally:
        lock.release()


# ---------------------------------------------------------------------------------------------- (3) compare

def _synthetic_run(staging: Path, rid: str = "ADD-03-run-recorded-syn", analysis: str = "done") -> Path:
    """A synthetic run folder: a checkpoint and a combined set whose items mirror the briefing in part."""
    rd = staging / "runs" / rid
    (rd / "ai" / f"{rid}-combined").mkdir(parents=True)
    steps = {s: {"status": "done", "seconds": 1.0, "started": "2026-10-06T10:00:00Z", "finished": "2026-10-06T10:00:01Z"}
             for s in ("ingest", "readings", "analysis", "validation", "downstream", "downstream_validation",
                       "critic", "promotion", "pin", "check_register", "outputs", "diff", "review")}
    steps["outputs"]["finished"] = "2026-10-06T10:12:00Z"
    steps["analysis"]["status"] = analysis
    cp = {"format": "tenderpack-ai-run/1", "run_id": rid, "addendum": "ADD-03", "created": "2026-10-06T10:00:00Z",
          "updated": "2026-10-06T10:13:00Z", "status": "partial", "steps": steps, "batches": {},
          "settings": {"route": "recorded"}, "inputs": {"pdf": {"path": str(PDF02)}}}
    (rd / "checkpoint.json").write_text(json.dumps(cp), encoding="utf-8")

    def item(i, prov, target, typ, words, status="evidence_verified", st="amendment_op"):
        payload = {"type": typ} if st == "amendment_op" else ({"disposition": typ} if st == "disposition" else {})
        return {"id": i, "statement_type": st, "provision": prov, "target": target, "payload": payload,
                "evidence": [{"doc": "ADD-03", "unit_id": prov, "page": 1, "words": words}],
                "verification_status": status}
    items = [item("ADD-03/2.1", "ADD-03:2.1", "VOL-I:6.1", "replace_text",
                  "‘14:00 hours Riyadh time’ is deleted and ‘11:00 hours Riyadh time’ is substituted."),
             item("ADD-03/2.4", "ADD-03:2.4", "VOL-I:6.7", "no_effect",
                  "The following new Clause 6.8 is inserted in Volume I after Clause 6.7:", st="disposition"),
             item("ADD-03/2.2", "ADD-03:2.2", "ADD-01:2.1", "set_status",
                  "ceases to have effect", status="interpretation_pending")]
    (rd / "ai" / f"{rid}-combined" / "proposals.yaml").write_text(
        yaml.safe_dump({"proposal_set": {"run_id": f"{rid}-combined", "items": items}}, allow_unicode=True),
        encoding="utf-8")
    return rd


def test_compare_lists_agreements_disagreements_and_one_sided_items_and_never_edits(ws, tmp_path):
    QRm = _qr()
    res = _run(ws, tmp_path)
    staging = tmp_path / "staging" / "ai"
    rd = _synthetic_run(staging)
    before = tree_files(rd, ROOT / "curation")
    sha_before = (Path(res["dir"]) / "briefing.sha256").read_text(encoding="utf-8")
    cmp = QRm.compare(res["qr_id"], rd.name, staging=staging)
    assert cmp["header"] == NOT_PROOF
    assert [a["briefing"]["id"] for a in cmp["agreements"]] == ["P1"]
    assert [x["briefing"]["id"] for x in cmp["disagreements"]] == ["P2"]
    dis = cmp["disagreements"][0]
    assert any("kind" in r for r in dis["differences"]) and dis["for_a_person"] is True
    assert dis["run"]["evidence"] and dis["briefing"]["quotation"]               # the evidence of each side
    assert [x["id"] for x in cmp["run_only"]] == ["ADD-03/2.2"] and cmp["briefing_only"] == []
    d = Path(res["dir"])
    md = (d / "comparison.md").read_text(encoding="utf-8")
    assert md.splitlines()[0] == f"# {NOT_PROOF}"
    assert json.loads((d / "comparison.json").read_text(encoding="utf-8"))["header"] == NOT_PROOF
    assert tree_files(rd, ROOT / "curation") == before                           # a list for a person, never an edit
    assert (d / "briefing.sha256").read_text(encoding="utf-8") == sha_before and QRm.preserved(d)["ok"]
    assert cmp["timings"]["run_updated_a1_a5_s"] == 720.0
    assert cmp["timings"]["quick_review_first_briefing_s"] is not None


def test_compare_reads_a_recorded_rehearsal_run_folder(ws, tmp_path):
    res = _run(ws, tmp_path, pdf=PDF06)
    cmp = _qr().compare(res["qr_id"], str(RUN06), staging=tmp_path / "staging" / "ai")
    assert cmp["run"]["run_id"] == "ADD-03-run-host-blind06-20261005T173226Z"
    assert cmp["counts"]["run_items"] == 83
    assert cmp["header"] == NOT_PROOF


# ---------------------------------------------------------------------------------------------- (4) answers

def test_answers_are_recorded_against_the_exact_question_and_evidence_and_never_touch_curation(ws, tmp_path):
    QRm = _qr()
    res = _run(ws, tmp_path)
    d = Path(res["dir"])
    before = tree_files(ROOT / "curation")
    e = QRm.record_answer(d, "Q1", "Yes: treat it as late; I checked Clause 6.1.", "A. Owner")
    a = yaml.safe_load((d / "answers.yaml").read_text(encoding="utf-8"))["answers"]
    assert a[0]["question"] == BRIEFING["questions"][0]["question"]
    assert a[0]["evidence"] == BRIEFING["questions"][0]["evidence"]
    assert a[0]["by"] == "A. Owner" and a[0]["recorded"] and a[0]["status"] == "recorded (not incorporated)"
    assert e["briefing_sha256"] and QRm.preserved(d)["ok"]
    for bad in ((d, "Q1", "x", ""), (d, "Q1", "", "A. Owner"), (d, "Q9", "x", "A. Owner")):
        with pytest.raises(QRm.QuickReviewError):
            QRm.record_answer(*bad)
    assert tree_files(ROOT / "curation") == before


def test_an_answer_recorded_during_the_analysis_step_is_held_until_the_step_ends(ws, tmp_path):
    QRm = _qr()
    res = _run(ws, tmp_path)
    d = Path(res["dir"])
    staging = tmp_path / "staging" / "ai"
    rd = _synthetic_run(staging, analysis="running")
    cp = json.loads((rd / "checkpoint.json").read_text(encoding="utf-8"))
    for s in ("validation", "downstream", "downstream_validation", "critic", "promotion", "pin", "check_register",
              "outputs", "diff", "review"):
        cp["steps"][s]["status"] = "pending"
    cp["batches"] = {"analysis-001": {"phase": "analysis", "status": "running"}}
    (rd / "checkpoint.json").write_text(json.dumps(cp), encoding="utf-8")
    QRm.record_answer(d, "Q1", "Treat it as late.", "A. Owner")
    out = QRm.offer_answers(d, rd)
    assert out["offered"] == [] and len(out["held"]) == 1
    assert "analysis" in out["held"][0]["reason"] and "between phases" in out["held"][0]["reason"]
    assert not (rd / "owner_answers").exists()
    # the step ends (the batch done, the next step not started): a safe checkpoint
    cp["steps"]["analysis"]["status"] = "done"
    cp["batches"]["analysis-001"]["status"] = "done"
    (rd / "checkpoint.json").write_text(json.dumps(cp), encoding="utf-8")
    out = QRm.offer_answers(d, rd)
    assert len(out["offered"]) == 1 and out["held"] == []
    notes = yaml.safe_load(next((rd / "owner_answers").glob("*.yaml")).read_text(encoding="utf-8"))["notes"]
    n = notes[0]
    assert n["status"] == "PROPOSED" and n["review"] == "pending a person" and n["offered_after"] == "analysis"
    assert n["question"] == BRIEFING["questions"][0]["question"] and n["answer"] == "Treat it as late."
    assert n["revalidation"]["state"] == "current"
    assert not any(v in json.dumps(n).lower() for v in ("accepted", "approved"))
    # offering again does not duplicate; a later change to the run's proposals makes the note stale (revalidation)
    assert QRm.offer_answers(d, rd)["offered"] == []
    p = rd / "ai" / f"{rd.name}-combined" / "proposals.yaml"
    p.write_text(p.read_text(encoding="utf-8") + "# changed\n", encoding="utf-8")
    rv = QRm.revalidate_offers(rd)
    assert rv["stale"] == [n["id"]]
    n2 = yaml.safe_load(next((rd / "owner_answers").glob("*.yaml")).read_text(encoding="utf-8"))["notes"][0]
    assert n2["revalidation"]["state"].startswith("STALE")


def test_the_preserved_briefing_detects_a_later_edit(ws, tmp_path):
    QRm = _qr()
    res = _run(ws, tmp_path)
    d = Path(res["dir"])
    f = d / "briefing.json"
    os.chmod(f, 0o644)
    f.write_text(f.read_text(encoding="utf-8").replace("P1", "PX"), encoding="utf-8")
    assert QRm.preserved(d)["ok"] is False
    with pytest.raises(QRm.QuickReviewError, match="changed after"):
        QRm.compare(res["qr_id"], str(RUN06), staging=tmp_path / "staging" / "ai")


# ---------------------------------------------------------------------------------------------- (5) the CLI and routes

def test_the_cli_runs_a_recorded_quick_review_and_compare(ws, tmp_path):
    cas = tmp_path / "c.yaml"
    cas.write_text(yaml.safe_dump(_cassette(), allow_unicode=True), encoding="utf-8")
    staging = tmp_path / "staging" / "ai"
    base = [sys.executable, "-m", "tenderpack", "ai", "quick-review"]
    common = ["--evidence", str(ws.evidence), "--pack", str(ws.pack), "--out", str(staging), "--worklog",
              str(tmp_path / "wl")]
    r = subprocess.run(base + ["ADD-03", "--pdf", str(PDF02), "--route", "recorded", "--cassette", str(cas),
                               "--budget-minutes", "3", "--max-tokens", "20000", "--qr-id", "ADD-03-qr-cli"] + common,
                       cwd=ROOT, capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, r.stdout + r.stderr
    assert LABEL in r.stdout and "first useful briefing" in r.stdout
    req = json.loads((staging / "quick-review" / "ADD-03-qr-cli" / "request.json").read_text(encoding="utf-8"))
    assert req["budget"]["minutes"] == 3 and req["budget"]["max_tokens"] == 20000
    rd = _synthetic_run(staging)
    r = subprocess.run(base + ["compare", "ADD-03-qr-cli", rd.name] + common, cwd=ROOT, capture_output=True, text=True,
                       timeout=600)
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.splitlines()[0] == NOT_PROOF


def test_ai_routes_states_the_quick_review_status_of_every_route():
    r = subprocess.run([sys.executable, "-m", "tenderpack", "ai", "routes", "--json"], cwd=ROOT, capture_output=True,
                       text=True, timeout=300)
    rows = {x["route"]: x for x in json.loads(r.stdout)["routes"]}
    for name in ("host", "anthropic", "openrouter", "ollama", "recorded"):
        assert rows[name]["quick_review"], name
    assert rows["recorded"]["quick_review"].startswith("tested")
    assert "untested" in rows["host"]["quick_review"] and "untested" in rows["anthropic"]["quick_review"]


def test_the_offline_guard_test_knows_the_quick_review_construction_sites():
    src = (ROOT / "tests/test_session13_mac_scripts.py").read_text(encoding="utf-8")
    assert '("tenderpack/ai/quick_review.py", "make")' in src
    # session 14: W5 builds the quick review's AnswerSession through a factory that subclasses it; the guard test
    # counts that site under the factory's name (its constructor is still AnswerSession's, which runs the guard)
    assert '("tenderpack/ai/quick_review.py", "_session_class")' in src


# ---------------------------------------------------------------------------------------------- (6) the panel

@pytest.fixture()
def panel(tmp_path, blind02_build):
    from tenderpack.panel.server import Panel, PanelConfig
    cfg = PanelConfig(root=ROOT, pack=ROOT / "config/pack.yaml", evidence=blind02_build, out=tmp_path / "out",
                      staging=tmp_path / "staging" / "ai", worklog=tmp_path / "worklog", panel_dir=tmp_path / "panel",
                      cassette=tmp_path / "c.yaml")
    (tmp_path / "c.yaml").write_text(yaml.safe_dump(_cassette(), allow_unicode=True), encoding="utf-8")
    p = Panel(cfg, 0, log=open(os.devnull, "w"))
    p._routes = (time.time() + 3600, {"offline": None, "routes": [
        {"route": "host", "status": {"status": "tested"}, "available": True},
        {"route": "ollama", "models": [], "error": "not here"}]}, None)
    p.host_found = lambda: True
    p.start()
    yield p
    p.stop()


def _http(p, path, data=None, ctype=None):
    import urllib.error
    import urllib.request

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    r = urllib.request.Request(p.url + path, data=data, headers={"Content-Type": ctype} if ctype else {})
    try:
        with urllib.request.build_opener(NoRedirect).open(r, timeout=60) as resp:
            return resp.status, dict(resp.headers), html.unescape(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), html.unescape(e.read().decode("utf-8", "replace"))


def _mp(fields: dict, pdf: bytes) -> tuple[bytes, str]:
    b = "----qrboundary"
    out = b""
    for k, v in fields.items():
        out += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    out += (f"--{b}\r\nContent-Disposition: form-data; name=\"pdf\"; filename=\"a.pdf\"\r\nContent-Type: "
            "application/pdf\r\n\r\n").encode() + pdf + b"\r\n" + f"--{b}--\r\n".encode()
    return out, f"multipart/form-data; boundary={b}"


def _wait_job(p, jid, timeout=300):
    t0 = time.time()
    while time.time() - t0 < timeout:
        j = p.jobs.get(jid)
        if j and j["status"] != "running":
            return j
        time.sleep(0.3)
    raise AssertionError("job still running")


def test_the_panel_starts_a_quick_review_from_the_new_addendum_box_at_lower_priority(panel):
    st, _, home = _http(panel, "")
    assert "Start AI quick review" in home and 'formaction="' in home
    body, ctype = _mp({"addendum": "ADD-03", "route": "recorded"}, PDF02.read_bytes())
    st, h, _ = _http(panel, "quickreview/start", body, ctype)
    assert st == 303, _
    jid = re.search(r"/jobs/([^/]+)$", h["Location"]).group(1)
    j = panel.jobs.get(jid)
    assert j["kind"] == "ai-quick-review" and j["argv"][:3] == ["nice", "-n", "10"]
    assert j["argv"][j["argv"].index("--budget-minutes") + 1] and "--max-tokens" in j["argv"]
    j = _wait_job(panel, jid)
    assert j["exit_code"] == 0, panel.jobs.log_text(j)
    qid = j["meta"]["qr_id"]
    st, _, page = _http(panel, f"quickreview/{qid}")
    assert st == 200 and LABEL in page and "Q1" in page and 'name="answer"' in page
    assert "Time to the first briefing" in page and "Time to the run's updated A1-A5 candidate" in page
    # offline forbids a hosted route: refused before any job
    body, ctype = _mp({"addendum": "ADD-03", "route": "host", "offline": "yes"}, PDF02.read_bytes())
    st, _, txt = _http(panel, "quickreview/start", body, ctype)
    assert st == 400 and "offline" in txt


def test_the_panel_quick_review_page_records_an_answer_and_starts_one_from_a_run(panel):
    staging = panel.cfg.staging
    rd = _synthetic_run(staging)
    st, _, page = _http(panel, f"runs/{rd.name}")
    assert st == 200 and "Start AI quick review" in page
    st, h, _ = _http(panel, f"runs/{rd.name}/quickreview", b"", "application/x-www-form-urlencoded")
    assert st == 303
    jid = re.search(r"/jobs/([^/]+)$", h["Location"]).group(1)
    j = _wait_job(panel, jid)
    assert j["exit_code"] == 0, panel.jobs.log_text(j)
    assert j["argv"][j["argv"].index("--pdf") + 1] == str(PDF02) and j["meta"]["for_run"] == rd.name
    assert panel.running_for(rd.name) is None                         # never mistaken for the run's own job
    qid = j["meta"]["qr_id"]
    import urllib.parse
    form = urllib.parse.urlencode({"question": "Q1", "answer": "Treat it as late.", "name": ""}).encode()
    st, _, txt = _http(panel, f"quickreview/{qid}/answer", form, "application/x-www-form-urlencoded")
    assert st == 400 and "name" in txt
    form = urllib.parse.urlencode({"question": "Q1", "answer": "Treat it as late.", "name": "A. Owner"}).encode()
    st, h, _ = _http(panel, f"quickreview/{qid}/answer", form, "application/x-www-form-urlencoded")
    assert st == 303
    j = _wait_job(panel, re.search(r"/jobs/([^/]+)$", h["Location"]).group(1))
    assert j["kind"] == "qr-answer" and j["exit_code"] == 0, panel.jobs.log_text(j)
    a = yaml.safe_load((staging / "quick-review" / qid / "answers.yaml").read_text(encoding="utf-8"))["answers"]
    assert a[0]["by"] == "A. Owner" and a[0]["question"] == BRIEFING["questions"][0]["question"]
    form = urllib.parse.urlencode({"run": rd.name}).encode()
    st, h, _ = _http(panel, f"quickreview/{qid}/compare", form, "application/x-www-form-urlencoded")
    assert st == 303
    j = _wait_job(panel, re.search(r"/jobs/([^/]+)$", h["Location"]).group(1))
    assert j["exit_code"] == 0, panel.jobs.log_text(j)
    st, _, page = _http(panel, f"quickreview/{qid}")
    assert NOT_PROOF in page and "Treat it as late." in page and "12.0 min" in page
    # offering the answers to the run (every step done: a safe checkpoint): a PROPOSED note shown on the run's page
    st, h, _ = _http(panel, f"quickreview/{qid}/offer", form, "application/x-www-form-urlencoded")
    j = _wait_job(panel, re.search(r"/jobs/([^/]+)$", h["Location"]).group(1))
    assert j["kind"] == "qr-offer" and j["exit_code"] == 0, panel.jobs.log_text(j)
    st, _, page = _http(panel, f"runs/{rd.name}")
    assert "Your answers offered to this run (PROPOSED notes; never a decision)" in page and "Treat it as late." in page
