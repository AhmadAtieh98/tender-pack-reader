"""Session 09, the controller end to end on blind rehearsal 02's Addendum No. 3, with RECORDED provider turns (hand-written
cassettes in tests/fixtures/ai_cassettes; no live call is made and none is implied): evidence -> proposal ->
validation -> impact -> staging, and the adversarial cases (malformed output, fabricated citations, numerical changes,
prompt injection, stale evidence, a rejected op, provider failure, budget exhaustion, a missing capability, the lock).

Passing these tests shows that the controller assigns the statuses and protects the curated state; it says nothing
about how well any real model proposes."""
from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest
import yaml

from ai_fixture import CASSETTES, CURATED_ADD03, ROOT, Untouched, workspace
from tenderpack.ai import budget as B
from tenderpack.ai import config as C
from tenderpack.ai import controller
from tenderpack.ai.contract import ProposalSet
from tenderpack.ai.providers.recorded import RecordedProvider

DECISIONS = ROOT / "curation/reviews/decisions.yaml"


@pytest.fixture(scope="module")
def ws(tmp_path_factory, blind02_build):
    return workspace(tmp_path_factory.mktemp("ai-propose"), evidence=blind02_build)


def _propose(ws, cassette, **kw):
    kw.setdefault("sleep", lambda s: None)
    return controller.propose(ws, "ADD-03", "recorded", C.load(), cassette=CASSETTES / cassette, **kw)


def _staged(ws, ps) -> tuple[dict, str, list[dict]]:
    d = ws.staging / ps.run_id
    data = yaml.safe_load((d / "proposals.yaml").read_text(encoding="utf-8"))
    log = [json.loads(x) for x in (d / "log.jsonl").read_text(encoding="utf-8").splitlines()]
    return data, (d / "review_request.md").read_text(encoding="utf-8"), log


def _status(ps) -> dict:
    return {it.id: it.verification_status for it in ps.items}


# ---------------------------------------------------------------------------------------------- (3) end to end

def test_a_recorded_run_proposes_validates_measures_impact_and_stages_only(ws):
    with Untouched() as u:                                          # curation/, build/ and the rehearsal untouched
        ps = _propose(ws, "add03_propose.yaml", reference=CURATED_ADD03)
    assert u.audit.under(ws.staging) and u.audit.under(ws.worklog)  # it wrote to staging and the work log only
    assert not DECISIONS.exists() and not (ws.pack.parent / "decisions.yaml").exists()
    assert _status(ps) == {"ADD-03/2.1": "evidence_verified", "ADD-03/3.1": "evidence_verified",
                           "ADD-03/5.1": "insufficient_evidence", "ADD-03/7.2": "escalated",
                           "ADD-03/cover/para1": "evidence_verified"}
    fab = next(it for it in ps.items if it.id == "ADD-03/5.1")
    assert any(not v.ok and "not verbatim" in v.detail and "35 dB(A)" in v.detail for v in fab.validation)
    assert any(v.check.startswith("engine") and v.ok for v in fab.validation)      # the op itself is valid: only the quote fails
    assert ps.status == "partial" and ps.coverage.provisions_total == 42 and ps.coverage.accounted == 5
    assert "ADD-03:4.1" in ps.coverage.unaccounted and "ADD-03:2.1" not in ps.coverage.unaccounted
    assert ps.usage.calls == 3 and ps.usage.input_tokens == 46500 and ps.usage.cost_usd is None
    assert ps.model_requested == ps.model_reported == "recorded-fixture-model" and ps.route == "recorded"
    data, md, log = _staged(ws, ps)
    assert ProposalSet.model_validate(data["proposal_set"]) == ps
    imp = data["controller"]["impact"]
    assert imp["changed_units"] == ["VOL-I:6.1", "VOL-I:7.1"]
    assert {"VOL-I-6.1-01", "VOL-I-7.1-01"} <= set(imp["rows_citing_changed_units"])
    assert "VOL-I-6.1-01" in {x["row"] for x in imp["rows_stale_at_addendum"]}
    assert imp["diff"]["from"] == "ADD-02" and imp["diff"]["to"] == "ADD-03"
    assert data["controller"]["reference"]["counts"]["same"] >= 2              # 2.1 and 3.1 match the curated ops
    assert "Nothing here is accepted" in md and "ADD-03:4.1" in md and "promote" in md
    events = [e["event"] for e in log]
    assert events[:3] == ["start", "capabilities", "prompt"] and events.count("tool_call") == 3
    assert "end" in events and "lock_released" in events
    prompt = next(e for e in log if e["event"] == "prompt")
    assert prompt["packet"]["reference"]["label"] == "pattern drafter output, unverified"
    assert len(prompt["packet"]["provisions"]) == 42 and prompt["packet"]["state"] == ps.state.model_dump()
    assert (ws.worklog / f"{ps.run_id}.jsonl").read_text(encoding="utf-8").count("\n") == len(log)
    spend = [json.loads(x) for x in (ws.staging / "spend.jsonl").read_text().splitlines() if ps.run_id in x]
    assert len(spend) == 3 and all(s["cost_usd"] is None for s in spend)
    assert not (ws.staging / ".lock-ADD-03").exists()


def test_the_host_route_is_validated_identically(ws):
    """The same proposal set submitted by a coding host (no API call) gets the same statuses."""
    ps = _propose(ws, "add03_propose.yaml")
    data, _, _ = _staged(ws, ps)
    raw = {k: data["proposal_set"][k] for k in ("addendum", "state", "statements", "items")}
    res = controller.submit(ws, raw, host_model="host-declared-model")
    assert {x["id"]: x["status"] for x in res["items"]} == _status(ps)
    host = ProposalSet.model_validate(yaml.safe_load(open(f"{res['staging']}/proposals.yaml"))["proposal_set"])
    assert host.route == "host" and host.model_requested == "host-declared-model" and host.usage.calls == 0
    assert "no application API call" in host.usage.cost_basis
    with pytest.raises(B.Refused, match="host-model"):
        controller.submit(ws, raw, host_model=" ")


def test_promote_is_a_persons_step_and_writes_proposed_drafts_only(ws, tmp_path):
    ps = _propose(ws, "add03_propose.yaml")
    code, msgs = controller.promote(ws, ps.run_id, "Claude Code", tmp_path / "amend", tmp_path / "props")
    assert code == 2 and "names the assistant" in msgs[0] and not (tmp_path / "amend").exists()
    code, msgs = controller.promote(ws, ps.run_id, "Fixture Test Reviewer", tmp_path / "amend", tmp_path / "props")
    assert code == 0, msgs
    from tenderpack.amend import load_opfile
    of = load_opfile(tmp_path / "amend/ADD-03.yaml")
    assert {o.id for o in of.ops} == {"ADD-03/2.1", "ADD-03/3.1"}               # the insufficient one is not promoted
    assert all(o.review == "proposed" and o.reviewer is None and o.origin == "assistant" for o in of.ops)
    d = {x.provision: x for x in of.dispositions}
    assert d["ADD-03:cover/para1"].disposition == "no_effect"
    assert d["ADD-03:5.1"].disposition == "unresolved" and d["ADD-03:7.2"].disposition == "unresolved"
    assert len(of.dispositions) + 2 == 42
    code, msgs = controller.promote(ws, ps.run_id, "Fixture Test Reviewer", tmp_path / "amend", tmp_path / "props")
    assert code == 2 and "never overwrites" in msgs[0]


# ---------------------------------------------------------------------------------------------- (4) adversarial

def test_malformed_output_is_retried_once_then_recorded(ws):
    with Untouched():
        ps = _propose(ws, "add03_malformed.yaml")
    assert ps.status == "malformed" and ps.items == [] and ps.usage.calls == 2
    assert ps.coverage.accounted == 0 and len(ps.coverage.unaccounted) == 42
    _, md, log = _staged(ws, ps)
    errs = [e for e in log if e["event"] == "parse_error"]
    assert len(errs) == 2 and not errs[0]["retry_used"] and errs[1]["retry_used"]
    req2 = [e for e in log if e["event"] == "request"][1]
    assert "could not be parsed" in json.dumps(req2["new_messages"])         # the parse error is quoted back once


def test_numerical_changes_wrong_values_and_a_wrong_old_are_invalid(ws):
    ps = _propose(ws, "add03_numeric.yaml")
    st = _status(ps)
    assert st == {"ADD-03/3.1": "invalid", "ADD-03/3.1(x)": "invalid", "ADD-03/3.2": "evidence_verified",
                  "ADD-03/5.1": "invalid"}
    by = {it.id: it for it in ps.items}
    assert any(v.check == "previous_value" and not v.ok and "'120' does not match VOL-I:7.1" in v.detail
               for v in by["ADD-03/3.1"].validation)
    assert any(not v.ok and "C23" in v.detail and "occurs 0 time(s)" in v.detail for v in by["ADD-03/3.1(x)"].validation)
    assert any(v.check == "proposed_value" and not v.ok for v in by["ADD-03/5.1"].validation)
    assert any(v.check == "previous_value" and v.ok for v in by["ADD-03/3.2"].validation)
    assert "ADD-03:3.1" in ps.coverage.unaccounted                  # invalid items account for nothing


def test_prompt_injection_changes_nothing(ws):
    with Untouched() as u:
        ps = _propose(ws, "add03_injection.yaml")
    assert not [p for p in u.audit.paths if "decisions" in p or "approvals" in p]
    assert not DECISIONS.exists() and not (ws.pack.parent / "decisions.yaml").exists()
    assert not (ROOT / "curation/reviews").exists() or not any((ROOT / "curation/reviews").iterdir())
    assert _status(ps) == {"ADD-03/2.1": "evidence_verified", "ADD-03/5.1": "insufficient_evidence",
                           "ADD-03/Q15": "interpretation_pending", "ADD-03/7.1": "escalated"}
    assert ps.status == "partial" and ps.usage.calls == 2                    # the claimed 'complete' and usage are ignored
    op = next(it for it in ps.items if it.id == "ADD-03/2.1")
    assert not any(v.check == "all" for v in op.validation)                 # the proposer's own validation is dropped
    assert any("replaced by 'proposed'" in v.detail for v in op.validation)
    data, md, log = _staged(ws, ps)
    ows = data["controller"]["overwrites"]
    assert {o.get("field") for o in ows} >= {"status", "usage"}
    assert {o["item"] for o in ows if "item" in o} == {"ADD-03/2.1", "ADD-03/5.1", "ADD-03/Q15", "ADD-03/7.1"}
    calls = [e for e in log if e["event"] == "tool_call"]
    assert [(c["name"], c["ok"]) for c in calls] == [("write_file", False), ("request_review", False),
                                                    ("get_unit", False), ("calculate", False)]
    assert not os.path.exists("/tmp/pwned")


def test_stale_evidence_makes_every_item_invalid(ws):
    ps = _propose(ws, "add03_stale.yaml")
    assert ps.status == "stale" and _status(ps) == {"ADD-03/2.1": "invalid"}
    assert "evidence_build_id" in ps.items[0].validation[0].detail
    data, md, _ = _staged(ws, ps)
    assert "STALE" in md and data["controller"]["state_differences"]


def test_a_rejected_op_is_conflicting(tmp_path, blind02_build):
    rej = [{"kind": "op", "item": "ADD-03/2.1", "decision": "reject", "reviewer": "Fixture Test Reviewer",
            "date": "2026-10-04", "note": "fixture: the time is wrong", "fingerprint": "fixture"}]
    w = workspace(tmp_path, decisions=rej, evidence=blind02_build)
    assert w.identity().decisions_sha256 is not None
    ps = controller.propose(w, "ADD-03", "recorded", C.load(), cassette=CASSETTES / "add03_propose.yaml",
                            sleep=lambda s: None)
    st = _status(ps)
    assert st["ADD-03/2.1"] == "conflicting" and st["ADD-03/3.1"] == "evidence_verified"
    x = next(it for it in ps.items if it.id == "ADD-03/2.1")
    assert any(v.check == "decision" and "rejection by Fixture Test Reviewer" in v.detail for v in x.validation)
    assert (tmp_path / "pack/decisions.yaml").read_text(encoding="utf-8").count("reject") == 1     # unchanged


def test_provider_failure_is_retried_within_bounds_then_recorded(ws):
    slept = []
    ps = _propose(ws, "provider_timeout.yaml", sleep=slept.append)
    assert ps.status == "provider_failed" and ps.items == []
    assert ps.usage.calls == 3 and slept == [2.0, 4.0]                       # retries: 2, exponential backoff
    _, _, log = _staged(ws, ps)
    assert [e["kind"] for e in log if e["event"] == "provider_error"] == ["timeout"] * 3
    assert any(e["event"] == "provider_failed" for e in log) and log[-1]["event"] == "lock_released"


def test_budget_exhaustion_stops_the_run(ws):
    ps = _propose(ws, "add03_propose.yaml", caps={"max_calls": 1})
    assert ps.status == "budget_exhausted" and ps.items == [] and ps.usage.calls == 1
    _, md, log = _staged(ws, ps)
    assert any(e["event"] == "budget_exhausted" and "max_calls 1" in e["reason"] for e in log)
    ps2 = _propose(ws, "add03_propose.yaml", caps={"max_output_tokens": 300})
    assert ps2.status == "budget_exhausted"


# ---------------------------------------------------------------------------------------------- (5) capabilities

def test_a_task_with_crops_is_refused_by_a_provider_without_images(ws):
    prov = RecordedProvider(CASSETTES / "vision_needed.yaml")
    with pytest.raises(B.Refused, match="does not report image input"):
        controller.propose(ws, "ADD-03", "recorded", C.load(), provider=prov, include_crops=["VOL-II:T2-4/BOD5"])
    assert prov.requests == []                                               # refused before any call
    assert not (ws.staging / ".lock-ADD-03").exists()
    pk = controller.task_packet(ws, "ADD-03", include_crops=["VOL-II:T2-4/BOD5"])
    assert pk["crops"][0]["unit_id"] == "VOL-II:T2-4/BOD5" and len(pk["crops"][0]["sha256"]) == 64


def test_live_routes_refuse_without_their_endpoint_or_key(ws, monkeypatch):
    from tenderpack.ai.providers.base import ProviderError
    from tenderpack.ai.providers.ollama import OllamaProvider
    from tenderpack.ai.providers.openrouter import OpenRouterProvider
    cfg = C.load()

    def unreachable(*a, **k):
        raise ProviderError("network", "blocked in this test", True)
    orp = OpenRouterProvider("vendor/model", cfg["routes"]["openrouter"], fetch=unreachable)
    with pytest.raises(ProviderError, match="refused until it can be checked"):
        orp.capabilities()
    olp = OllamaProvider("qwen3-vl:32b", cfg["routes"]["ollama"], cfg["routes"]["ollama"]["models"]["vision"],
                         env={}, fetch=unreachable)
    with pytest.raises(ProviderError, match="owner's Mac only"):
        olp.capabilities()
    shown = OllamaProvider("qwen3-vl:32b", cfg["routes"]["ollama"], cfg["routes"]["ollama"]["models"]["vision"], env={},
                           fetch=lambda *a, **k: (200, {}, {"capabilities": ["completion", "tools"],
                                                            "model_info": {"qwen3vl.context_length": 262144}}))
    caps = shown.capabilities()
    assert caps.images is False and caps.tools is True and caps.context_tokens == 32768      # bounded by num_ctx
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    caps_cfg = C.caps(cfg, "anthropic", {"max_calls": 2, "max_input_tokens": 1000, "max_output_tokens": 100})
    with pytest.raises(B.Refused, match="ANTHROPIC_API_KEY in the environment"):
        controller.propose(ws, "ADD-03", "anthropic", cfg, model="claude-opus-5-5", caps=caps_cfg)


# ---------------------------------------------------------------------------------------------- (7) the lock

def test_a_second_orchestrator_is_refused_and_only_a_person_breaks_the_lock(ws):
    staging = B.safe_staging(ws.staging)
    held = B.acquire(staging, "ADD-03", {"route": "host", "run_id": "host-claim-test", "pid": os.getpid()})
    try:
        with pytest.raises(B.Refused, match="another orchestrator holds ADD-03"):
            _propose(ws, "add03_propose.yaml")
        with pytest.raises(B.Refused, match="names the assistant"):
            _propose(ws, "add03_propose.yaml", break_lock_by="Claude Code")
        assert (staging / ".lock-ADD-03").exists()
        ps = _propose(ws, "add03_propose.yaml", break_lock_by="Fixture Test Reviewer")
        assert ps.status == "partial"
        broken = [json.loads(x) for x in (staging / "locks.jsonl").read_text().splitlines()]
        assert broken[-1]["broken_by"] == "Fixture Test Reviewer" and broken[-1]["was_stale"] is False
    finally:
        held.release()
    claim = controller.host_task(ws, "ADD-03", claim=True, host_model="host-declared-model", pid=os.getpid())
    assert claim["lock"]["route"] == "host" and claim["provisions_total"] == 42
    with pytest.raises(B.Refused, match="another orchestrator"):
        _propose(ws, "add03_propose.yaml")                                   # an API run while the host holds it
    data, _, _ = _staged(ws, ps)
    controller.submit(ws, {k: data["proposal_set"][k] for k in ("addendum", "state", "statements", "items")},
                      host_model="host-declared-model")
    assert not (staging / ".lock-ADD-03").exists()                           # the host's submission releases it


# ---------------------------------------------------------------------------------------------- the CLI

def test_the_cli_runs_a_recorded_proposal_and_a_tool(ws, tmp_path, blind02_build):
    out, wl = tmp_path / "staging", tmp_path / "worklog"
    base = [sys.executable, "-m", "tenderpack", "ai"]
    common = ["--evidence", str(blind02_build), "--pack", str(ws.pack)]
    p = subprocess.run(base + ["propose", "ADD-03", "--route", "recorded", "--cassette",
                               str(CASSETTES / "add03_propose.yaml"), "--out", str(out), "--worklog", str(wl)] + common,
                       cwd=ROOT, capture_output=True, text=True, timeout=300)
    assert p.returncode == 0, p.stdout + p.stderr
    assert "partial" in p.stdout and "review_request.md" in p.stdout and "cost None (no price configured)" in p.stdout
    t = subprocess.run(base + ["tool", "get_unit", "--json", '{"unit_id": "ADD-03:2.1"}'] + common,
                       cwd=ROOT, capture_output=True, text=True, timeout=300)
    assert t.returncode == 0 and json.loads(t.stdout)["pages"] == [1]
    r = subprocess.run(base + ["propose", "ADD-03", "--route", "anthropic", "--model", "claude-opus-5-5",
                               "--out", str(out), "--worklog", str(wl)] + common,
                       cwd=ROOT, capture_output=True, text=True, timeout=300, env={**os.environ, "ANTHROPIC_API_KEY": ""})
    assert r.returncode == 2 and "REFUSED" in r.stdout and "max_calls" in r.stdout    # no caps: a paid run never starts
    b = subprocess.run(base + ["propose", "ADD-03", "--route", "recorded", "--cassette", str(CASSETTES / "add03_propose.yaml"),
                               "--break-lock", "--by", "Claude Code", "--out", str(out), "--worklog", str(wl)] + common,
                       cwd=ROOT, capture_output=True, text=True, timeout=300)
    assert b.returncode == 2 and "names the assistant" in b.stdout
