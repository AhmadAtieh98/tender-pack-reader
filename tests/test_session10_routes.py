"""Session 10, the AI routes (W4): capability verification without a silent fallback, native structured outputs beside the
local validation, bounded batches, the independent critic, and the host/MCP session.

Every provider exchange here is RECORDED or MOCKED (canned HTTP replies, cassettes, a fake `claude` executable): no live
API call is made and none is implied. Passing these tests shows how the controller and the adapters behave whatever a
model or an endpoint returns; it says nothing about how well any real model proposes or criticises."""
from __future__ import annotations

import copy
import inspect
import json

import pytest
import yaml

from ai_fixture import CASSETTES, workspace
from tenderpack.ai import budget as B
from tenderpack.ai import config as C
from tenderpack.ai import controller
from tenderpack.ai.providers.base import ProviderError
from tenderpack.ai.providers.recorded import HttpCassette

PLACEHOLDER = "placeholder-not-a-real-credential-0000"      # a test value, not a key: nothing is sent anywhere
CAPS = {"max_calls": 4, "max_input_tokens": 10 ** 6, "max_output_tokens": 10 ** 5}


def _workspace(request, d):
    """The blind-02 workspace of the session-09 tests, on the session's disposable build when the fixture exists."""
    if "evidence" in inspect.signature(workspace).parameters:
        try:
            return workspace(d, evidence=request.getfixturevalue("blind02_build"))
        except pytest.FixtureLookupError:
            pass
    return workspace(d)


@pytest.fixture(scope="module")
def ws(request, tmp_path_factory):
    return _workspace(request, tmp_path_factory.mktemp("ai-routes"))


def _staged(ws, ps):
    d = ws.staging / ps.run_id
    data = yaml.safe_load((d / "proposals.yaml").read_text(encoding="utf-8"))
    log = [json.loads(x) for x in (d / "log.jsonl").read_text(encoding="utf-8").splitlines()]
    return data, (d / "review_request.md").read_text(encoding="utf-8"), log


def _status(ps) -> dict:
    return {it.id: it.verification_status for it in ps.items}


class FakeHttp:
    """Stands in for providers.base.http_json: GET/POST replies by (method, path suffix); every request is recorded."""

    def __init__(self, routes: dict):
        self.routes, self.calls = routes, []

    def __call__(self, method, url, headers, body, timeout):
        self.calls.append({"method": method, "url": url, "body": body})
        for (m, suffix), reply in self.routes.items():
            if m == method and url.endswith(suffix):
                reply = reply(body) if callable(reply) else reply
                if isinstance(reply, ProviderError):
                    raise reply
                return 200, {}, reply
        raise ProviderError("network", f"no fake route for {method} {url}", True)

    def posts(self, suffix="/v1/messages"):
        return [c for c in self.calls if c["method"] == "POST" and c["url"].endswith(suffix)]


ANSWER = {"model": "claude-opus-5-5", "stop_reason": "end_turn", "usage": {"input_tokens": 10, "output_tokens": 5},
          "content": [{"type": "text", "text": "{}"}]}


# ---------------------------------------------------------------------------------------------- (1) capabilities

def _anthropic_run(ws, monkeypatch, models_reply, **kw):
    from tenderpack.ai.providers import anthropic as A
    monkeypatch.setenv("ANTHROPIC_API_KEY", PLACEHOLDER)
    fake = FakeHttp({("GET", "/v1/models/claude-opus-5-5"): models_reply, ("POST", "/v1/messages"): ANSWER})
    monkeypatch.setattr(A, "http_json", fake)
    err = None
    try:
        controller.propose(ws, "ADD-03", "anthropic", C.load(), model="claude-opus-5-5", caps=CAPS,
                           sleep=lambda s: None, **kw)
    except B.Refused as e:
        err = str(e)
    return fake, err


@pytest.mark.parametrize("models_reply", [
    ProviderError("network", "the models endpoint cannot be reached (test)", True),
    ProviderError("http_404", "model not found (test)", False, 404),
    {"id": "claude-opus-5-5"},                                  # listed, but without context or output limits
], ids=["unreachable", "not-listed", "no-limits"])
def test_anthropic_refuses_live_use_when_the_models_endpoint_does_not_verify_the_model(ws, monkeypatch, models_reply):
    """REGRESSION (session 10): with a credential set, an unreachable or silent GET /v1/models/{id} used to fall back to
    the configured `capabilities:` block and the paid run went ahead. Live use is now refused with the reason."""
    fake, err = _anthropic_run(ws, monkeypatch, models_reply)
    assert fake.posts() == [], "a paid call was made on capabilities nobody verified"
    assert err and "capabilit" in err and "unverified" in err
    assert "--allow-unverified-capabilities" in err


def test_openrouter_and_ollama_refuse_when_the_endpoint_omits_the_context(monkeypatch):
    """REGRESSION (session 10): a listing entry (OpenRouter) or /api/show reply (Ollama) without a context length used
    to pass with context None (OpenRouter: the controller's fit check was skipped) or the configured num_ctx (Ollama)."""
    from tenderpack.ai.providers.ollama import OllamaProvider
    from tenderpack.ai.providers.openrouter import OpenRouterProvider
    cfg = C.load()
    listing = {"data": [{"id": "vendor/m", "architecture": {"input_modalities": ["text"]},
                         "supported_parameters": ["tools"]}]}
    orp = OpenRouterProvider("vendor/m", cfg["routes"]["openrouter"], env={}, fetch=lambda *a, **k: (200, {}, listing))
    with pytest.raises(ProviderError, match="context"):
        orp.capabilities()
    olp = OllamaProvider("qwen3-vl:32b", cfg["routes"]["ollama"], cfg["routes"]["ollama"]["models"]["vision"], env={},
                         fetch=lambda *a, **k: (200, {}, {"capabilities": ["completion", "tools", "vision"]}))
    with pytest.raises(ProviderError, match="context"):
        olp.capabilities()


def test_allow_unverified_capabilities_is_explicit_logged_and_shown(ws, monkeypatch):
    """With --allow-unverified-capabilities (propose(allow_unverified_capabilities=True)) the configured block is used,
    marked UNVERIFIED in the run log's capabilities event, recorded as a route notice and shown in the review request."""
    from tenderpack.ai.providers import anthropic as A
    monkeypatch.setenv("ANTHROPIC_API_KEY", PLACEHOLDER)
    cas = HttpCassette({"exchanges": [
        {"request": {"method": "GET", "path": "/v1/models/claude-opus-5-5"},
         "error": {"kind": "network", "message": "blocked (recorded)", "retryable": True}},
        {"request": {"method": "POST", "path": "/v1/messages", "body_has": ["tools"]},
         "response": {"body": {"model": "claude-opus-5-5", "stop_reason": "end_turn", "usage": {"input_tokens": 9,
                                                                                               "output_tokens": 9},
                               "content": [{"type": "text", "text": '{"addendum": "ADD-03", "state": ${state}, '
                                                                    '"statements": [], "items": []}'}]}}}]})
    monkeypatch.setattr(A, "http_json", cas)
    ps = controller.propose(ws, "ADD-03", "anthropic", C.load(), model="claude-opus-5-5", caps=CAPS,
                            sleep=lambda s: None, allow_unverified_capabilities=True)
    assert ps.status == "partial" and ps.items == []
    data, md, log = _staged(ws, ps)
    cap = next(e for e in log if e["event"] == "capabilities")
    assert "UNVERIFIED" in cap["source"] and cap["details"]["unverified"] is True
    assert "--allow-unverified-capabilities" in cap["source"]
    notes = next(e for e in log if e["event"] == "route_notices")["notices"]
    assert [n["kind"] for n in notes][0] == "capabilities_unverified"
    assert "capabilities unverified" in md and md.index("Route notices") < md.index("## Items")
    assert data["controller"]["route_notices"][0]["kind"] == "capabilities_unverified"
    with pytest.raises(B.Refused, match="capabilities unverified"):           # without the flag: refused, nothing sent
        cas2 = HttpCassette({"exchanges": [{"request": {"method": "GET"}, "error": {"kind": "network", "message": "x"}}]})
        monkeypatch.setattr(A, "http_json", cas2)
        controller.propose(ws, "ADD-03", "anthropic", C.load(), model="claude-opus-5-5", caps=CAPS, sleep=lambda s: None)
    assert [r["method"] for r in cas2.requests] == ["GET"]


def test_the_recorded_route_still_uses_its_cassette_capabilities(ws):
    ps = controller.propose(ws, "ADD-03", "recorded", C.load(), cassette=CASSETTES / "add03_propose.yaml",
                            sleep=lambda s: None)
    _, md, log = _staged(ws, ps)
    assert next(e for e in log if e["event"] == "capabilities")["source"] == "cassette (recorded fixture)"
    assert "Route notices" not in md and not any(e["event"] == "route_notices" for e in log)


# ---------------------------------------------------------------------------------------------- (2) structured outputs

def _walk(node, path=""):
    if isinstance(node, dict):
        yield path, node
        for k, v in node.items():
            yield from _walk(v, f"{path}/{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _walk(v, f"{path}/{i}")


def test_the_structured_schema_is_derived_from_the_contract_and_fitted_to_the_limits():
    from tenderpack.ai.contract import ProposalSet, model_fill_schema
    from tenderpack.ai.providers import structured as SO
    base = SO.proposal_schema()
    assert base == model_fill_schema() and set(base["properties"]) == {"addendum", "state", "statements", "items"}
    assert set(base["$defs"]["ChangeProposal"]["properties"]) < set(ProposalSet.model_json_schema()["$defs"]
                                                                    ["ChangeProposal"]["properties"])
    s = SO.for_provider(base, "anthropic")
    banned = {"title", "default", "minimum", "maximum", "minLength", "maxLength", "pattern"}
    for path, node in _walk(s):
        if path.endswith("/properties") or path.endswith("/$defs"):
            continue                                                  # field names, not keywords
        assert not banned & set(node), (path, banned & set(node))
        if node.get("type") == "object" or "properties" in node:
            assert node.get("additionalProperties") is False and node.get("properties"), path
    pl = s["$defs"]["ChangeProposal"]["properties"]["payload"]
    assert pl["type"] == "string" and "JSON-ENCODED STRING" in pl["description"]
    assert s["$defs"]["ChangeProposal"]["required"] == base["$defs"]["ChangeProposal"]["required"]   # optional stays optional
    oll = SO.for_provider(base, "ollama")
    assert oll["$defs"]["ChangeProposal"]["properties"]["payload"]["type"] == "object"         # free-form allowed there
    rec = {"$defs": {"A": {"type": "object", "properties": {"b": {"$ref": "#/$defs/B"}}},
                     "B": {"type": "object", "properties": {"a": {"$ref": "#/$defs/A"}}}}, "$ref": "#/$defs/A"}
    with pytest.raises(SO.SchemaUnsupported, match="recursive"):
        SO.for_provider(rec)
    d = {"items": [{"id": "x", "payload": '{"provision": "P", "disposition": "no_effect", "reason": "r"}'},
                   {"id": "y", "payload": "not json"}, {"id": "z", "payload": {"k": 1}}]}
    out = SO.decode_payloads(d)
    assert out["items"][0]["payload"]["disposition"] == "no_effect" and out["items"][1]["payload"] == "not json"
    assert out["items"][2]["payload"] == {"k": 1} and d["items"][0]["payload"].startswith("{")      # input untouched
    assert SO.is_schema_rejection(ProviderError("http_400", "output_config.format.schema: unsupported", False, 400))
    assert not SO.is_schema_rejection(ProviderError("http_400", "messages.0: bad image", False, 400))
    assert not SO.is_schema_rejection(ProviderError("http_429", "schema rate limited", True, 429))


def _anthropic(ws, monkeypatch, cassette, **kw):
    from tenderpack.ai.providers import anthropic as A
    monkeypatch.setenv("ANTHROPIC_API_KEY", PLACEHOLDER)
    cas = HttpCassette(CASSETTES / cassette)
    monkeypatch.setattr(A, "http_json", cas)
    ps = controller.propose(ws, "ADD-03", "anthropic", C.load(), model="claude-opus-5-5", caps=CAPS,
                            sleep=lambda s: None, **kw)
    return ps, cas


def test_anthropic_native_structured_output_beside_local_validation(ws, monkeypatch):
    """RECORDED (s10_anthropic_structured.yaml): output_config.format json_schema merged with the configured effort,
    sent with the tools on every turn; the payload-as-string is decoded and the set validated locally as before."""
    ps, cas = _anthropic(ws, monkeypatch, "s10_anthropic_structured.yaml")
    assert cas.pos == len(cas.exchanges)                                     # every recorded exchange matched
    assert _status(ps) == {"ADD-03/2.1": "evidence_verified", "ADD-03/cover/para1": "evidence_verified"}
    posts = [r["body"] for r in cas.requests if r["method"] == "POST"]
    assert len(posts) == 2 and all(b["output_config"]["effort"] == "high" for b in posts)
    fmt = posts[0]["output_config"]["format"]
    assert fmt["type"] == "json_schema" and fmt["schema"]["additionalProperties"] is False
    assert posts[0]["tools"] and "thinking" not in posts[0]
    data, md, log = _staged(ws, ps)
    item = next(i for i in data["proposal_set"]["items"] if i["id"] == "ADD-03/2.1")
    assert item["payload"]["type"] == "replace_text"                         # decoded, then validated as an amend.Op
    assert any(v["check"].startswith("engine") and v["ok"] for v in item["validation"])
    assert "Route notices" not in md and ps.usage.calls == 2
    cap = next(e for e in log if e["event"] == "capabilities")
    assert cap["structured_output"] is True and cap["context_tokens"] == 1000000 and "GET /v1/models" in cap["source"]


def test_a_rejected_schema_falls_back_to_the_tool_use_path_visibly(ws, monkeypatch):
    """RECORDED (s10_anthropic_schema_rejected.yaml): a 400 naming the schema switches the run to the plain path; the
    retry (counted) is sent without output_config.format; a route notice reaches the log and the review request."""
    ps, cas = _anthropic(ws, monkeypatch, "s10_anthropic_schema_rejected.yaml")
    assert cas.pos == len(cas.exchanges)
    assert _status(ps) == {"ADD-03/2.1": "evidence_verified"} and ps.usage.calls == 2
    data, md, log = _staged(ws, ps)
    errs = [e for e in log if e["event"] == "provider_error"]
    assert [e["kind"] for e in errs] == ["structured_output_rejected"]
    kinds = [n["kind"] for n in next(e for e in log if e["event"] == "route_notices")["notices"]]
    assert kinds == ["structured_output_rejected"]
    assert "structured_output_rejected" in md and "plain tool-use path" in md
    assert data["controller"]["route_notices"][0]["kind"] == "structured_output_rejected"


def test_openrouter_and_ollama_structured_request_shapes(ws):
    """RECORDED: OpenRouter response_format json_schema (only when the listing names structured_outputs); Ollama
    `format` (here with with_tools true, as a person would set it after checking on the Mac). Both validated locally."""
    from tenderpack.ai.providers.ollama import OllamaProvider
    from tenderpack.ai.providers import openrouter as R
    from tenderpack.ai.providers import ollama as O
    cfg = C.load()
    cas = HttpCassette(CASSETTES / "s10_openrouter_structured.yaml")
    prov = R.OpenRouterProvider("vendor/model-a", cfg["routes"]["openrouter"], env={"OPENROUTER_API_KEY": PLACEHOLDER},
                                fetch=cas)
    mp = pytest.MonkeyPatch()
    try:
        mp.setattr(R, "http_json", cas)
        ps = controller.propose(ws, "ADD-03", "openrouter", cfg, provider=prov, caps=CAPS, sleep=lambda s: None)
        assert cas.pos == len(cas.exchanges) and _status(ps) == {"ADD-03/cover/para1": "evidence_verified"}
        rf = cas.requests[1]["body"]["response_format"]
        assert rf["type"] == "json_schema" and rf["json_schema"]["strict"] is True
        rcfg = copy.deepcopy(cfg["routes"]["ollama"])
        rcfg["structured_output"] = {"mode": "native", "with_tools": True}
        cas2 = HttpCassette(CASSETTES / "s10_ollama_format.yaml")
        olp = OllamaProvider("qwen3-vl:32b", rcfg, rcfg["models"]["vision"], env={}, fetch=cas2)
        mp.setattr(O, "http_json", cas2)
        # session 11: one provision. The whole addendum (with the system prompt, the tools, the later-turn allowance and
        # 16,000 output tokens) does not fit the 32,768-token bound, which the complete accounting now refuses
        ps2 = controller.propose(ws, "ADD-03", "ollama", cfg, provider=olp, sleep=lambda s: None,
                                 provisions=["ADD-03:cover/para1"])
        assert cas2.pos == len(cas2.exchanges) and _status(ps2) == {"ADD-03/cover/para1": "evidence_verified"}
        assert cas2.requests[1]["body"]["format"]["properties"]["items"]
    finally:
        mp.undo()
    listing = {"data": [{"id": "v/m", "context_length": 1000, "architecture": {}, "supported_parameters":
                         ["tools", "response_format"]}]}
    p3 = R.OpenRouterProvider("v/m", cfg["routes"]["openrouter"], env={}, fetch=lambda *a, **k: (200, {}, listing))
    from tenderpack.ai.providers.base import Request, collect_notices
    with collect_notices() as notes:
        p3.capabilities()
        body = p3.body(Request(system="S", messages=[], tools=[], response_schema={"type": "object"}))
    assert "response_format" not in body and "names response_format but not structured_outputs" in notes[0]["message"]


# ---------------------------------------------------------------------------------------------- (3) batches

def test_batches_fit_the_verified_limits_and_never_drop_a_provision(ws):
    from tenderpack.ai import batching as BT
    from tenderpack.ai.providers.base import Capabilities
    from tenderpack.ai.tools import MODEL_TOOLS, TOOLS
    pk = controller.task_packet(ws, "ADD-03")
    ov = BT.overhead_for(pk, controller.SYSTEM, [TOOLS[n].spec() for n in MODEL_TOOLS], max_output_tokens=16000,
                         settings={"prior_turns_tokens": 8000})
    assert ov.packet_fixed_tokens > 1000 and ov.system_tokens > 100 and ov.tools_tokens > 100
    caps = Capabilities(images=True, tools=True, structured_output=True, context_tokens=40000, retention="r",
                        source="cassette (recorded fixture)", max_output_tokens=16000)
    provs = BT.packet_provisions(pk)
    batches = BT.plan_batches(provs, caps, ov)
    ids = [p["unit_id"] for p in provs]
    assert [u for b in batches for u in b.provisions] == ids and len(ids) == 42      # every provision once, in order
    assert len(batches) > 1 and all(b.fits for b in batches)
    for b in batches:
        assert b.input_tokens + b.output_tokens <= int(40000 * 0.9) and b.output_tokens <= 16000
        assert b.input_tokens == ov.input_fixed() + sum(b.sizes.values())
    assert BT.assignment(batches)["ADD-03:2.1"] == 1
    # one provision that cannot fit even alone: its own batch, flagged with its size; nothing dropped
    huge = provs[:3] + [{"unit_id": "ADD-03:HUGE", "tokens": 60000}] + provs[3:6]
    b2 = BT.plan_batches(huge, caps, ov)
    bad = [b for b in b2 if not b.fits]
    assert [b.provisions for b in bad] == [["ADD-03:HUGE"]] and BT.TOO_LARGE in bad[0].note
    assert "60000" not in bad[0].note or bad[0].sizes["ADD-03:HUGE"] == 60000
    assert [u for b in b2 for u in b.provisions] == [p["unit_id"] for p in huge]
    assert BT.summary(b2)["too_large"][0]["provision"] == "ADD-03:HUGE"
    # the output cap binds too: 1,500 + 700 per provision must stay under it
    small_out = Capabilities(images=True, tools=True, structured_output=True, context_tokens=10 ** 6, retention="r",
                             source="s", max_output_tokens=5000)
    assert max(len(b.provisions) for b in BT.plan_batches(provs, small_out, ov)) == 5
    with pytest.raises(BT.BatchPlanError, match="capabilities unverified"):
        BT.plan_batches(provs, {"context_tokens": None, "source": "config"}, ov)


def test_token_counts_calibrate_the_sizes_recorded(ws, monkeypatch):
    """RECORDED: the Messages API token-count endpoint (POST /v1/messages/count_tokens) measures this packet."""
    from tenderpack.ai import batching as BT
    from tenderpack.ai.providers import anthropic as A
    monkeypatch.setenv("ANTHROPIC_API_KEY", PLACEHOLDER)
    cas = HttpCassette({"exchanges": [
        {"request": {"method": "POST", "path": "/v1/messages/count_tokens", "body_has": ["model", "messages", "system"],
                     "body_lacks": ["max_tokens", "output_config"]},
         "response": {"body": {"input_tokens": 20000}}}]})
    monkeypatch.setattr(A, "http_json", cas)
    prov = A.AnthropicProvider("claude-opus-5-5", C.load()["routes"]["anthropic"])
    pk = controller.task_packet(ws, "ADD-03")
    text = controller._packet_text(pk)
    ratio, source = BT.calibrate(prov, text, controller.SYSTEM, [])
    assert ratio == pytest.approx((len(text) + len(controller.SYSTEM) + 2) / 20000)
    assert "token-count endpoint" in source and "20000 tokens" in source
    ov = BT.overhead_for(pk, controller.SYSTEM, [], chars_per_token=ratio, size_source=source)
    assert ov.size_source == source and ov.chars_per_token == ratio


# ---------------------------------------------------------------------------------------------- (5) MCP images

def test_get_crop_over_mcp_returns_the_image_itself(ws, tmp_path):
    """The MCP server's get_crop result carries image content blocks (base64 PNG with mimeType) after the JSON."""
    import base64
    import hashlib
    from tenderpack.mcp_server import MAX_IMAGES, Server
    srv = Server(ws)
    r = srv.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                    "params": {"name": "get_crop", "arguments": {"unit_id": "VOL-II:T2-4/BOD5"}}})["result"]
    assert r["isError"] is False and r["content"][0]["type"] == "text"
    meta = json.loads(r["content"][0]["text"])
    imgs = r["content"][1:]
    assert 1 <= len(imgs) <= MAX_IMAGES and all(i["type"] == "image" and i["mimeType"] == "image/png" for i in imgs)
    attached = [x for x in meta["images_attached"] if x["attached"]]
    assert [x["sha256"] for x in attached] == [hashlib.sha256(base64.b64decode(i["data"])).hexdigest() for i in imgs]
    assert attached[0]["kind"] == "unit"                                      # the unit's own crop first
    # REGRESSION (the real host session, 4 Oct 2026): a table whose unit crop IS its region crop sent the image twice
    tb = srv.handle({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                     "params": {"name": "get_crop", "arguments": {"unit_id": "VOL-II:T2-4"}}})["result"]
    sent = [x for x in json.loads(tb["content"][0]["text"])["images_attached"] if x["attached"]]
    assert len({x["sha256"] for x in sent}) == len(sent) == len(tb["content"]) - 1
    t = srv.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                    "params": {"name": "get_unit", "arguments": {"unit_id": "ADD-03:2.1"}}})["result"]
    assert [c["type"] for c in t["content"]] == ["text"]                     # other tools: text only


# ---------------------------------------------------------------------------------------------- (5) host session

FAKE_CLAUDE = CASSETTES / "fake_claude_host.py"


def test_a_host_session_works_only_through_mcp_reads_a_crop_and_submits(ws):
    """RECORDED host (tests/fixtures/ai_cassettes/fake_claude_host.py stands in for the CLI; it is not a model): the
    real MCP server is started from the session's mcp.json; get_crop images reach the host; submit_proposals stages the
    set; the lock is released; every tool call is in the run log."""
    from tenderpack.ai.hostsession import HostSession, host_packet
    pk = host_packet(ws, "ADD-03", ["ADD-03:cover/para1", "ADD-03:2.1"])
    pk["image_targets"] = ["VOL-II:T2-4/BOD5"]
    hs = HostSession(ws, C.load(), claude_bin=str(FAKE_CLAUDE), timeout_s=240)
    cmd = hs.command(ws.staging / "mcp.json")
    assert cmd[cmd.index("--tools") + 1] == "" and cmd[cmd.index("--allowedTools") + 1] == "mcp__tenderpack__*"
    assert "--strict-mcp-config" in cmd and cmd[cmd.index("--max-turns") + 1] == "40"
    assert "mcp__tenderpack__get_task_packet" in cmd[cmd.index("--disallowedTools") + 1]
    ps = hs.run_batch(pk)
    r = hs.last
    assert r.error is None and r.exit_code == 0, (r.error, r.run_dir)
    assert [c["name"] for c in r.tool_calls] == ["get_crop", "submit_proposals"]
    assert r.crops_read == ["VOL-II:T2-4/BOD5"] and r.images_received[0]["received"]
    assert [x["sha256"] for x in r.images_received[0]["sent"]] == [x["sha256"] for x in r.images_received[0]["received"]]
    assert r.model_reported == ["fake-host-model"] and r.submission["run_id"].startswith("ADD-03-host-")
    assert ps["route"] == "host" and r.statuses == {"ADD-03/cover/para1": "evidence_verified"}
    assert ps["items"][0]["verification_status"] == "evidence_verified"
    assert not (ws.staging / ".lock-ADD-03").exists()
    log = [json.loads(x) for x in (ws.staging / r.run_id / "log.jsonl").read_text().splitlines()]
    ev = [e["event"] for e in log]
    assert ev[:2] == ["start", "prompt"] and ev.count("tool_call") == 2 and ev[-1] == "end"
    crop = next(e for e in log if e["event"] == "tool_call" and e["name"] == "get_crop")
    assert crop["images"] and "data" not in json.dumps(crop["images"])           # sizes and hashes, not the image data
    tr = (ws.staging / r.run_id / "transcript.jsonl").read_text()
    assert "[image data not copied]" in tr and "iVBOR" not in tr
    assert json.loads((ws.staging / r.run_id / "mcp.json").read_text())["mcpServers"]["tenderpack"]["args"][:4] == \
        ["-m", "tenderpack", "ai", "serve-mcp"]


def test_a_host_session_without_a_submission_is_reported_not_hidden(ws, tmp_path):
    from tenderpack.ai.hostsession import HostSession, host_packet
    pk = host_packet(ws, "ADD-03", ["ADD-03:cover/para1"])
    hs = HostSession(ws, C.load(), claude_bin=str(tmp_path / "no-such-claude"))
    ps = hs.run_batch(pk)
    assert ps["status"] == "provider_failed" and ps["items"] == [] and "could not be started" in hs.last.error
    assert not (ws.staging / ".lock-ADD-03").exists()


# ---------------------------------------------------------------------------------------------- (4) the critic

def test_the_critic_reviews_only_the_selected_items_and_changes_no_status(ws):
    """RECORDED (s10_critic_source.yaml, s10_critic_review.yaml): removal, conflict, consequential interpretation and
    uncertain target are selected; the critic's answers land in review.critic and the review request; no status
    changes; the critic's own system prompt is used and every call is logged."""
    from tenderpack.ai import critic
    from tenderpack.ai.contract import ProposalSet
    ps = controller.propose(ws, "ADD-03", "recorded", C.load(), cassette=CASSETTES / "s10_critic_source.yaml",
                            sleep=lambda s: None)
    before = _status(ps)
    assert before["ADD-03/2.1"] == "conflicting" and before["ADD-03/3.3"] == "interpretation_pending"
    sel = {it.id: why for it, why in critic.select(ps, ws)}
    assert set(sel) == {"ADD-03/2.1", "ADD-03/3.3", "ADD-03/4.3(a)"}
    assert sel["ADD-03/2.1"] == ["conflicting"] and sel["ADD-03/4.3(a)"] == ["removal"]
    assert {"consequential_interpretation", "uncertain_target"} <= set(sel["ADD-03/3.3"])
    assert "uncertain_target: target is a group" in sel["ADD-03/3.3"]
    res = critic.run(ws, ps.run_id, route="recorded", cassette=CASSETTES / "s10_critic_review.yaml", cfg=C.load())
    assert res["reviewed"] == 3 and res["agrees"] == 2 and res["disagrees"] == 1 and not res["errors"]
    data, md, log = _staged(ws, ps)
    after = ProposalSet.model_validate(data["proposal_set"])
    assert _status(after) == before                                          # agreement is not approval
    by = {it.id: it for it in after.items}
    c = by["ADD-03/3.3"].review.critic
    assert c.agrees is False and "paragraph 2" in c.concerns[0] and c.route == "recorded"
    assert c.model_reported == "recorded-critic-model" and "consequential_interpretation" in c.selected_because
    assert by["ADD-03/cover/para1"].review is None
    assert "## Independent critic" in md and "DOES NOT agree" in md and "no status was changed" in md
    assert md.index("## Independent critic") < md.index("## Next")
    req = next(e for e in log if e["event"] == "critic_request")
    assert req["system"] == critic.CRITIC_SYSTEM and req["system"] != controller.SYSTEM and "CRITIC REQUEST" in req["prompt"]
    assert [e["item"] for e in log if e["event"] == "critic_answer"] == ["ADD-03/2.1", "ADD-03/3.3", "ADD-03/4.3(a)"]
    assert data["controller"]["critic_runs"][0]["note"].startswith("agreement between models is not approval")
    # a review supplied by a proposer is dropped at parse time and recorded as an overwrite
    raw = {k: data["proposal_set"][k] for k in ("addendum", "state", "statements", "items")}
    sub = controller.submit(ws, raw, host_model="host-declared-model")
    staged = yaml.safe_load(open(f"{sub['staging']}/proposals.yaml"))
    assert all(i["review"] is None for i in staged["proposal_set"]["items"])
    assert {o["item"] for o in staged["controller"]["overwrites"] if o.get("field") == "review"} == set(sel)
    # the host critic: a headless CLI call with no tools and a JSON schema (RECORDED stand-in for the CLI)
    cfg = C.load()
    cfg["critic"] = {**cfg["critic"], "host": {"claude_bin": str(FAKE_CLAUDE), "timeout_s": 120, "max_turns": 3}}
    hb = critic.HostCritic(cfg)
    cmd = hb.command()
    assert cmd[cmd.index("--tools") + 1] == "" and "--json-schema" in cmd and "--system-prompt" in cmd
    res2 = critic.run(ws, ps.run_id, route="host", cfg=cfg, max_items=1)
    assert res2["reviewed"] == 1 and res2["not_reviewed_over_limit"] == ["ADD-03/3.3", "ADD-03/4.3(a)"]
    data2, md2, _ = _staged(ws, ps)
    c2 = ProposalSet.model_validate(data2["proposal_set"]).items[0].review.critic
    assert c2.route == "host" and c2.model_reported == "fake-critic-model" and md2.count("## Independent critic") == 1
