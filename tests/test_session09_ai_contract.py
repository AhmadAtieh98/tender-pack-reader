"""Session 09, the AI layer's shared contract, configuration, redaction, budget and locks (offline; no provider call).

Passing these tests does not make any proposal correct or any route a working live integration."""
from __future__ import annotations

import json
import os

import pytest
from pydantic import ValidationError

from tenderpack.ai import budget as B
from tenderpack.ai import config as C
from tenderpack.ai.contract import (CONTROLLER_ITEM_FIELDS, CONTROLLER_SET_FIELDS, ChangeProposal, EvidenceRef,
                                    ProposalSet, StateIdentity, Statement, model_fill_schema, payload_schemas)
from tenderpack.ai.runlog import REDACTED, RunLog, redact

STATE = StateIdentity(pack_id="P", evidence_build_id="a" * 64, validated_stage="ADD-02", working_stage="ADD-03")


def _set(**kw) -> ProposalSet:
    item = ChangeProposal(id="ADD-03/2.1", state=STATE, statement_type="amendment_op", provision="ADD-03:2.1",
                          target="VOL-I:6.1", payload={"type": "replace_text", "old": "14:00", "new": "11:00"},
                          previous_value="14:00", proposed_value=11,
                          evidence=[EvidenceRef(doc="ADD-03", unit_id="ADD-03:2.1", page=1, kind="span", words="x y z w")],
                          statements=["S1"])
    return ProposalSet(run_id="r1", created="2026-10-04T00:00:00Z", route="recorded", provider="recorded",
                       model_requested="m", task="propose_amendment", addendum="ADD-03", state=STATE,
                       statements=[Statement(id="S1", kind="interpretation", text="t")], items=[item], **kw)


# ---------------------------------------------------------------------------------------------- (1) contract

def test_the_contract_round_trips_through_json_and_rejects_unknown_fields():
    ps = _set()
    back = ProposalSet.model_validate(json.loads(ps.model_dump_json()))
    assert back == ps and back.items[0].verification_status == "unverified" and back.status == "partial"
    assert back.usage.cost_usd is None and back.usage.cost_basis == "no price configured"
    with pytest.raises(ValidationError):
        ProposalSet.model_validate({**json.loads(ps.model_dump_json()), "approved": True})
    with pytest.raises(ValidationError):                      # facts, assumptions, interpretations: no fourth kind
        Statement(id="S", kind="opinion", text="t")
    with pytest.raises(ValidationError):
        EvidenceRef(doc="D", unit_id="U", page=1, kind="summary", words="w")


def test_the_model_schema_is_trimmed_to_what_the_proposer_fills():
    s = model_fill_schema()
    assert set(s["properties"]) == {"addendum", "state", "statements", "items"}
    assert not set(CONTROLLER_SET_FIELDS) & set(s["properties"])
    item = s["$defs"]["ChangeProposal"]["properties"]
    assert not set(CONTROLLER_ITEM_FIELDS) & set(item) and {"evidence", "payload", "statements"} <= set(item)
    assert "Usage" not in s["$defs"] and "ValidationRecord" not in s["$defs"]
    full = ProposalSet.model_json_schema()                     # the full model still carries them (for parsing)
    assert "verification_status" in full["$defs"]["ChangeProposal"]["properties"]
    ps = payload_schemas()
    assert {"amendment_op", "disposition", "escalation", "row_reading", "row_new", "issue", "clarification"} == set(ps)
    assert "replace_text" in json.dumps(ps["amendment_op"])


# ---------------------------------------------------------------------------------------------- configuration

def test_the_configuration_keeps_model_choices_as_values_and_paid_routes_uncapped():
    cfg = C.load()
    assert set(cfg["routes"]) >= {"recorded", "host", "anthropic", "openrouter", "ollama"}
    assert C.default_model(cfg["routes"]["anthropic"], "propose") == "claude-opus-5-5"
    assert C.default_model(cfg["routes"]["anthropic"], "check") == "claude-haiku-4-5-20251001"
    oll = cfg["routes"]["ollama"]["models"]
    assert oll["vision"]["id"] == "qwen3-vl:32b" and oll["vision"]["num_ctx"] == 32768
    assert all("candidate, unmeasured" in m["status"] for m in oll.values())
    assert all("unverified" in m["status"] for m in cfg["routes"]["openrouter"]["models"].values())
    assert cfg["prices"]["claude-opus-5-5"] == {"input_per_mtok": 4.0, "output_per_mtok": 20.0}   # list prices, to confirm
    assert "qwen3-vl:32b" not in cfg["prices"]                                                  # local: no price
    for r in ("anthropic", "openrouter"):                      # the owner sets the spending limits
        caps = C.caps(cfg, r)
        assert caps["max_calls"] is None and caps["max_input_tokens"] is None and caps["max_output_tokens"] is None
        with pytest.raises(B.Refused, match="set max_calls"):
            B.check_startable(r, cfg["routes"][r], caps, None)
        B.check_startable(r, cfg["routes"][r], C.caps(cfg, r, {"max_calls": 5, "max_input_tokens": 10 ** 5,
                                                               "max_output_tokens": 10 ** 4}), None)
    B.check_startable("ollama", cfg["routes"]["ollama"], C.caps(cfg, "ollama"), None)      # local: not paid


def test_secrets_are_redacted_from_logs(tmp_path, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test-0123456789abcdef")
    rec = redact({"headers": {"x-api-key": "anything", "Authorization": "Bearer abc.def.ghi.jkl"},
                  "usage": {"input_tokens": 12, "output_tokens": 3},
                  "text": "the key is sk-ant-test-0123456789abcdef and Bearer abcdefghijkl"})
    assert rec["headers"] == {"x-api-key": REDACTED, "Authorization": REDACTED}
    assert rec["usage"] == {"input_tokens": 12, "output_tokens": 3}
    assert "sk-ant" not in rec["text"] and "abcdefghijkl" not in rec["text"]
    log = RunLog("r", [tmp_path / "a.jsonl"])
    log.event("x", note=os.environ["ANTHROPIC_API_KEY"])
    assert "sk-ant-test" not in (tmp_path / "a.jsonl").read_text()


# ---------------------------------------------------------------------------------------------- budget and locks

def test_the_budget_stops_at_every_cap():
    b = B.Budget({"max_calls": 2, "max_output_tokens": 100, "max_tokens_per_call": 80}, None)
    b.before_call()
    b.after_call(10, 60)
    assert b.max_tokens() == 40
    b.before_call()
    with pytest.raises(B.BudgetExhausted, match="max_output_tokens"):
        b.after_call(10, 50)
    with pytest.raises(B.BudgetExhausted, match="max_calls"):
        B.Budget({"max_calls": 0}, None).before_call()
    priced = B.Budget({"max_usd": 0.01}, {"input_per_mtok": 1.0, "output_per_mtok": 5.0})
    priced.before_call()
    with pytest.raises(B.BudgetExhausted, match="max_usd"):
        priced.after_call(10_000, 1_000)
    assert priced.cost_usd()[0] == pytest.approx(0.015)
    t = B.Budget({"max_turns": 1}, None)
    t.next_turn()
    with pytest.raises(B.BudgetExhausted, match="max_turns"):
        t.next_turn()


def test_staging_never_lands_in_protected_folders(tmp_path):
    from tenderpack.util import ROOT
    for bad in (ROOT / "curation", ROOT / "curation/x", ROOT / "build", ROOT / "config", ROOT):
        with pytest.raises(B.Refused):
            B.safe_staging(bad, ROOT)
    assert B.safe_staging(tmp_path / "s", ROOT) == (tmp_path / "s").resolve()
    for bad in ("../x", "a/b", "", ".hidden"):
        with pytest.raises(B.Refused):
            B.check_run_id(bad)


def test_a_lock_is_released_and_a_dead_process_lock_is_stale(tmp_path):
    lk = B.acquire(tmp_path, "ADD-03", {"route": "anthropic", "run_id": "r1", "pid": os.getpid()})
    with pytest.raises(B.Refused, match="another orchestrator holds ADD-03"):
        B.acquire(tmp_path, "ADD-03", {"route": "host", "run_id": "r2"})
    lk.release()
    assert not (tmp_path / ".lock-ADD-03").exists()
    (tmp_path / ".lock-ADD-04").write_text(json.dumps({"addendum": "ADD-04", "route": "host", "pid": 2 ** 22 + 7,
                                                       "host": __import__("socket").gethostname(), "created_epoch": 0}))
    stale, why = B.lock_state(B.read_lock(tmp_path / ".lock-ADD-04"), 120)
    assert stale and ("no longer running" in why or "min old" in why)
    with pytest.raises(B.Refused, match="STALE lock"):
        B.acquire(tmp_path, "ADD-04", {"route": "anthropic", "run_id": "r3"})


# ---------------------------------------------------------------------------------------------- adapters (MOCKED HTTP)

def _conversation(png):
    return [{"role": "user", "content": [{"type": "text", "text": "TASK PACKET\n{}"},
                                         {"type": "image", "path": str(png), "sha256": "x", "media_type": "image/png"}]},
            {"role": "assistant", "content": [{"type": "text", "text": "reading"}],
             "tool_calls": [{"id": "c1", "name": "get_unit", "arguments": {"unit_id": "VOL-I:6.1"}}], "provider_raw": None},
            {"role": "tool", "results": [{"tool_call_id": "c1", "name": "get_unit", "content": "{\"ok\": 1}", "is_error": False,
                                          "images": [{"type": "image", "path": str(png), "sha256": "x"}]}]}]


def test_the_adapters_translate_the_neutral_conversation_and_parse_responses(tmp_path, monkeypatch):
    """MOCKED: no network. Each adapter's request body and response parsing, with canned HTTP replies."""
    from tenderpack.ai.providers import anthropic as A
    from tenderpack.ai.providers import ollama as O
    from tenderpack.ai.providers import openrouter as R
    from tenderpack.ai.providers.base import ProviderError, Request
    png = tmp_path / "x.png"
    png.write_bytes(b"\x89PNG\r\n\x1a\n" + b"0" * 16)
    cfg = C.load()
    tools = [{"name": "get_unit", "description": "d", "input_schema": {"type": "object", "properties": {}}}]
    req = Request(system="S", messages=_conversation(png), tools=tools, max_tokens=100, timeout_s=5)

    a = A.AnthropicProvider("claude-opus-5-5", cfg["routes"]["anthropic"], C.model_entry(cfg["routes"]["anthropic"],
                                                                                          "claude-opus-5-5"), env={"ANTHROPIC_API_KEY": "k" * 20})
    body = a.body(req)
    assert body["system"] == "S" and body["tools"][0]["input_schema"] and body["output_config"] == {"effort": "high"}
    assert body["messages"][0]["content"][1]["source"]["type"] == "base64"
    assert body["messages"][1]["content"][-1] == {"type": "tool_use", "id": "c1", "name": "get_unit",
                                                  "input": {"unit_id": "VOL-I:6.1"}}
    tr = body["messages"][2]
    assert tr["role"] == "user" and tr["content"][0]["type"] == "tool_result" and tr["content"][0]["tool_use_id"] == "c1"
    seen = {}

    def fake(method, url, headers, data, timeout):
        seen.update(url=url, headers=headers)
        return 200, {}, {"model": "claude-opus-5-5", "stop_reason": "tool_use",
                         "content": [{"type": "thinking", "thinking": ""}, {"type": "text", "text": "t"},
                                     {"type": "tool_use", "id": "u1", "name": "get_unit", "input": {"unit_id": "X"}}],
                         "usage": {"input_tokens": 10, "output_tokens": 5, "cache_read_input_tokens": 3}}
    monkeypatch.setattr(A, "http_json", fake)
    r = a.complete(req)
    assert seen["url"].endswith("/v1/messages") and seen["headers"]["anthropic-version"] == "2023-06-01"
    assert r.tool_calls[0].name == "get_unit" and r.usage["input_tokens"] == 13 and r.provider_raw[0]["type"] == "thinking"
    monkeypatch.setattr(A, "http_json", lambda *x, **k: (200, {}, {"stop_reason": "refusal", "content": []}))
    with pytest.raises(ProviderError, match="refusal"):
        a.complete(req)
    with pytest.raises(ProviderError, match="ANTHROPIC_API_KEY"):
        A.AnthropicProvider("m", cfg["routes"]["anthropic"], env={}).check_ready()

    o = R.OpenRouterProvider("vendor/m", cfg["routes"]["openrouter"], env={"OPENROUTER_API_KEY": "k" * 20})
    ob = o.body(req)
    assert ob["messages"][0] == {"role": "system", "content": "S"} and ob["tools"][0]["type"] == "function"
    assert json.loads(ob["messages"][2]["tool_calls"][0]["function"]["arguments"]) == {"unit_id": "VOL-I:6.1"}
    assert ob["messages"][3]["role"] == "tool" and ob["messages"][4]["content"][1]["type"] == "image_url"
    monkeypatch.setattr(R, "http_json", lambda *x, **k: (200, {}, {"model": "vendor/m", "choices": [{"message": {
        "content": None, "tool_calls": [{"id": "z", "function": {"name": "get_unit", "arguments": "{\"unit_id\": \"Y\"}"}}]},
        "finish_reason": "tool_calls"}], "usage": {"prompt_tokens": 7, "completion_tokens": 2}}))
    rr = o.complete(req)
    assert rr.tool_calls[0].arguments == {"unit_id": "Y"} and rr.usage["input_tokens"] == 7
    listing = {"data": [{"id": "vendor/m", "context_length": 128000, "architecture": {"input_modalities": ["text"]},
                         "supported_parameters": ["tools"]}]}
    o2 = R.OpenRouterProvider("vendor/m", cfg["routes"]["openrouter"], env={}, fetch=lambda *x, **k: (200, {}, listing))
    caps = o2.capabilities()
    assert caps.images is False and caps.tools is True and caps.context_tokens == 128000 and "fetched" in caps.source

    ol = O.OllamaProvider("qwen3-vl:32b", cfg["routes"]["ollama"], cfg["routes"]["ollama"]["models"]["vision"], env={})
    lb = ol.body(req)
    assert lb["options"]["num_ctx"] == 32768 and lb["messages"][1]["images"] and lb["stream"] is False
    assert lb["messages"][3] == {"role": "tool", "content": "{\"ok\": 1}", "tool_name": "get_unit"}
    monkeypatch.setattr(O, "http_json", lambda *x, **k: (200, {}, {"model": "qwen3-vl:32b", "message": {
        "content": "", "tool_calls": [{"function": {"name": "get_unit", "arguments": {"unit_id": "Z"}}}]},
        "prompt_eval_count": 50, "eval_count": 9, "eval_duration": 1000}))
    lr = ol.complete(req)
    assert lr.tool_calls[0].arguments == {"unit_id": "Z"} and lr.usage["output_tokens"] == 9
    assert O.OllamaProvider("m", {"base_url": "http://127.0.0.1:11434"}, env={"TENDERPACK_OLLAMA_URL": "http://mac:1"}).base_url \
        == "http://mac:1"
