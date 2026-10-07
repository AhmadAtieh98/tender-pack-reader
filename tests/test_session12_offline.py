"""Session 12 (W4, part 3): an explicit OFFLINE MODE for the Mac. Every phase (readings, analysis, downstream, the
critic, the bounded repair, the capability checks) on the local Ollama route; no hosted call and no silent fallback;
the critic on a configured local model or recorded SKIPPED with its reason; Ollama capability checks (installed,
vision, tools, context, an estimated memory need) before any request; `tenderpack ai routes`.

There is no Ollama and no network in this container. The Ollama HTTP API is a FAKE server on 127.0.0.1
(tests/fixtures/fake_ollama.py) replaying the hand-written recorded workflow (tests/fixtures/ai_cassettes); a NetGuard
records every socket connection and every process and refuses anything but the fake's loopback port and any host CLI.
Passing these tests shows what tenderpack sends and refuses; it says nothing about how a real local model behaves
(that is PENDING ON THE MAC: docs/MAC_SETUP.md)."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pymupdf
import pytest
import yaml

from ai_fixture import CASSETTES, ROOT, workspace
from fake_ollama import FakeOllama, NetGuard, show
from tenderpack.ai import config as C
from tenderpack.ai import workflow as W
from tenderpack.ai.checkpoint import Checkpoint

quiet = lambda *a, **k: None  # noqa: E731
PDF = ROOT / "rehearsals/blind-02/input/ADD-03_Addendum_No_3.pdf"
TEXT, CRITIC, VISION = "fake-text:8b", "fake-critic:8b", "fake-vl:8b"


def _cfg(url: str, models: dict, offline: bool = False, machine: dict | None = None) -> dict:
    cfg = copy.deepcopy(C.load())
    ol = cfg["routes"]["ollama"]
    ol["base_url"], ol["base_url_env"] = url, "TENDERPACK_TEST_OLLAMA_URL_UNSET"
    ol["models"] = models
    ol["machine"] = machine or {"unified_memory_gb": 48, "usable_fraction": 0.75}
    cfg["failures"]["rate_limit"]["seed"] = 7
    cfg["concurrency"]["max_parallel_sessions"] = 1      # these tests are about offline mode (ollama: one at a time)
    if offline:
        cfg["offline"] = True
    return cfg


def _cfg_file(tmp: Path, cfg: dict) -> Path:
    p = tmp / "ai.yaml"
    p.write_text(yaml.safe_dump({k: v for k, v in cfg.items() if not k.startswith("_")}, sort_keys=False),
                 encoding="utf-8")
    return p


def _ctx(tmp: Path, ws, cfg: dict, route: str = "ollama") -> W.Ctx:
    settings = {"addendum": "ADD-03", "route": route, "worklog": str(tmp / "worklog"), "staging": str(tmp / "staging"),
                "caps": {}, "ai_config": None, "model": None, "batch_size": 8, "downstream_batch_size": 12}
    cp = Checkpoint.new(tmp / "run" / "checkpoint.json", run_id="t12", addendum="ADD-03", settings=settings, inputs={},
                        candidate={})
    ctx = W.Ctx(cp, echo=quiet, sleep=lambda s: None)
    ctx._ws, ctx._cfg = ws, cfg
    return ctx


@pytest.fixture(scope="module")
def ws(request, tmp_path_factory):
    return workspace(tmp_path_factory.mktemp("s12-off"), evidence=request.getfixturevalue("blind02_build"))


@pytest.fixture()
def fake():
    f = FakeOllama({TEXT: show(context=400000), CRITIC: show(caps=("completion",), context=65536)},
                   cassette=None)
    f.start()
    yield f
    f.stop()


# ---------------------------------------------------------------------------------------------- the reproduced bug

def test_regression_an_ollama_run_sends_its_critic_to_the_host_cli(ws, tmp_path, monkeypatch):
    """REGRESSION (owner, session 12): config/ai.yaml selects critic.route host, and workflow._critic_route returned it
    for any run that was not recorded: an Ollama run (the owner's offline Mac) sent its critic to `claude -p`. With
    offline mode asked for (TENDERPACK_OFFLINE=1), the critic must never be routed to the host."""
    monkeypatch.setenv("TENDERPACK_OFFLINE", "1")
    ctx = _ctx(tmp_path, ws, copy.deepcopy(C.load()))
    assert ctx.cfg["critic"]["route"] == "host"
    got = W._critic_route(ctx, ["ADD-03/2.4"])
    assert got[0] != "host", got


# ---------------------------------------------------------------------------------------------- no hosted call

def test_offline_refuses_every_hosted_route_and_host_process_before_any_call(ws, tmp_path, monkeypatch, fake):
    from tenderpack.ai import critic as CR
    from tenderpack.ai import hostsession as HS
    from tenderpack.ai import offline as OFF
    from tenderpack.ai import requests as R
    from tenderpack.ai.providers import make
    guard = NetGuard(monkeypatch, allow_port=int(fake.url.rsplit(":", 1)[1]))
    cfg = OFF.activate(_cfg(fake.url, {"text": {"id": TEXT}}), "--offline")
    for route in ("anthropic", "openrouter", "host"):
        with pytest.raises(C.ConfigError, match="offline mode"):
            make(route, "some-model", cfg)
    with pytest.raises(C.ConfigError, match="offline mode"):
        HS.HostSession(ws, cfg)
    with pytest.raises(C.ConfigError, match="offline mode"):
        HS.AnswerSession(ws, cfg, system="s")
    with pytest.raises(C.ConfigError, match="offline mode: the host critic is not available; configure "
                                            "routes.ollama.models.critic or accept a skipped review"):
        CR.HostCritic(cfg)
    with pytest.raises(C.ConfigError, match="offline mode"):
        R.host_repair(R.spec("critic"), cfg, "{}", ["x"], [], tmp_path, None, R.FailurePolicy())
    with pytest.raises(C.ConfigError, match="offline mode: the host critic is not available"):
        CR.review_batch({"items": []}, route="host", cfg=cfg, log=None, cwd=tmp_path, policy=R.FailurePolicy())
    # the workflow refuses a hosted route BEFORE creating anything
    cfgp = _cfg_file(tmp_path, _cfg(fake.url, {"text": {"id": TEXT}}))
    for route in ("host", "anthropic", "openrouter"):
        with pytest.raises(C.ConfigError, match="offline mode"):
            W.start("ADD-03", PDF, route=route, offline=True, ai_config=cfgp, staging=tmp_path / "st",
                    worklog=tmp_path / "wl", echo=quiet)
    assert not (tmp_path / "st" / "runs").exists() or not any((tmp_path / "st" / "runs").iterdir())
    assert guard.connects == [] and guard.processes == [] and guard.refused == []


def test_offline_ollama_url_must_be_loopback(tmp_path):
    from tenderpack.ai import offline as OFF
    with pytest.raises(C.ConfigError, match="not a loopback address"):
        OFF.activate(_cfg("http://10.1.2.3:11434", {"text": {"id": TEXT}}), "--offline")
    for ok in ("http://127.0.0.1:11434", "http://localhost:11434", "http://[::1]:11434"):
        OFF.activate(_cfg(ok, {"text": {"id": TEXT}}), "--offline")


def test_offline_is_switched_on_by_the_flag_the_config_or_the_environment(monkeypatch):
    from tenderpack.ai import offline as OFF
    monkeypatch.delenv("TENDERPACK_OFFLINE", raising=False)
    assert OFF.requested({}, flag=False) is None
    assert OFF.requested({}, flag=True) == "--offline"
    assert OFF.requested({"offline": True}) == "config/ai.yaml offline: true"
    assert OFF.requested({}, env={"TENDERPACK_OFFLINE": "1"}) == "TENDERPACK_OFFLINE=1"
    assert C.load().get("offline") is False                     # the shipped config: off unless asked


# ---------------------------------------------------------------------------------------------- the critic offline

def test_offline_critic_without_a_local_model_is_skipped_visibly_never_agreement(ws, tmp_path, monkeypatch, fake):
    guard = NetGuard(monkeypatch, allow_port=int(fake.url.rsplit(":", 1)[1]))
    from tenderpack.ai import offline as OFF
    ctx = _ctx(tmp_path / "a", ws, OFF.activate(_cfg(fake.url, {"text": {"id": TEXT}}), "--offline"))
    rec = W._critic_run(ctx, "analysis-001", [], ws)
    assert rec["status"] == "skipped" and rec["route"] == "ollama", rec
    assert rec["reason"].startswith("independent review did not run: ") and "routes.ollama.models.critic" in rec["reason"]
    assert "agrees" not in rec or rec.get("agrees") in (None, 0)
    # a configured critic model that is not installed: skipped with the exact reason and the installed list
    ctx2 = _ctx(tmp_path / "b", ws, OFF.activate(_cfg(fake.url, {"text": {"id": TEXT},
                                                                  "critic": {"id": "qwen3-vl:32b"}}), "--offline"))
    rec2 = W._critic_run(ctx2, "analysis-001", [], ws)
    assert rec2["status"] == "skipped", rec2
    assert "model qwen3-vl:32b is not installed; install it yourself with `ollama pull qwen3-vl:32b` if you want it" \
        in rec2["reason"] and TEXT in rec2["reason"]
    assert all(p != "POST /api/pull" for p in fake.paths())
    assert guard.processes == [] and guard.non_local() == []


# ---------------------------------------------------------------------------------------------- capability checks

def test_ollama_checks_installed_models_capabilities_context_and_memory(fake, monkeypatch):
    from tenderpack.ai.providers.ollama import OllamaProvider, check_models
    from tenderpack.ai.providers.base import ProviderError
    guard = NetGuard(monkeypatch, allow_port=int(fake.url.rsplit(":", 1)[1]))
    fake.models["big:70b"] = show(params="70.6B", quant="Q8_0", context=131072, layers=80, kv_heads=8, head=128)
    cfg = _cfg(fake.url, {"text": {"id": TEXT, "num_ctx": 32768}, "critic": {"id": CRITIC},
                          "vision": {"id": "qwen3-vl:32b"}, "big": {"id": "big:70b", "num_ctx": 131072}})
    rcfg = cfg["routes"]["ollama"]
    rep = check_models(cfg)
    by = {m["role"]: m for m in rep["models"]}
    assert rep["installed"] == sorted([TEXT, CRITIC, "big:70b"])
    assert by["text"]["installed"] and by["text"]["tools"] is True and by["text"]["images"] is False
    assert by["text"]["context_tokens"] == 32768 and by["text"]["memory"]["total_gb"] < 36
    assert by["critic"]["tools"] is False and by["critic"]["images"] is False       # never assumed
    assert by["vision"]["installed"] is False and "ollama pull qwen3-vl:32b" in by["vision"]["problem"]
    assert by["big"]["ok"] is False and "GB" in by["big"]["problem"] and "48 GB" in by["big"]["problem"]
    with pytest.raises(ProviderError, match="is not installed; install it yourself with `ollama pull qwen3-vl:32b`"):
        OllamaProvider("qwen3-vl:32b", rcfg, rcfg["models"]["vision"]).capabilities()
    with pytest.raises(ProviderError, match="estimated memory"):
        OllamaProvider("big:70b", rcfg, rcfg["models"]["big"]).capabilities()
    assert all(p != "POST /api/pull" for p in fake.paths())
    assert guard.non_local() == [] and guard.processes == []


def test_a_run_refuses_at_start_when_its_model_is_not_installed(tmp_path, fake, pack):
    cfgp = _cfg_file(tmp_path, _cfg(fake.url, {"text": {"id": "qwen3:30b-a3b"}}))
    with pytest.raises(C.ConfigError, match=r"model qwen3:30b-a3b is not installed; install it yourself with "
                                            r"`ollama pull qwen3:30b-a3b` if you want it \(installed: "):
        W.start("ADD-03", PDF, route="ollama", offline=True, ai_config=cfgp, evidence=pack["out"],
                staging=tmp_path / "st", worklog=tmp_path / "wl", echo=quiet)
    assert not (tmp_path / "st" / "runs").exists() or not any((tmp_path / "st" / "runs").iterdir())


# ---------------------------------------------------------------------------------------------- the whole run offline

def _critic_cassette(tmp: Path) -> Path:
    data = yaml.safe_load((CASSETTES / "workflow_add03.yaml").read_text(encoding="utf-8"))
    data["sessions"] += yaml.safe_load((CASSETTES / "s11_workflow_critic.yaml").read_text(encoding="utf-8"))["sessions"]
    p = tmp / "s12_offline.yaml"
    p.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return p


@pytest.fixture(scope="module")
def offline_run(tmp_path_factory, pack):
    """A whole workflow run (to the critic) on the ollama route in offline mode against the fake server, with the
    recorded workflow's answers; every connection and process recorded."""
    d = tmp_path_factory.mktemp("s12-offline-run")
    f = FakeOllama({TEXT: show(context=400000), CRITIC: show(caps=("completion",), context=400000)},
                   cassette=_critic_cassette(d))
    f.start()
    mp = pytest.MonkeyPatch()
    guard = NetGuard(mp, allow_port=int(f.url.rsplit(":", 1)[1]))
    try:
        cfgp = _cfg_file(d, _cfg(f.url, {"text": {"id": TEXT, "num_ctx": 400000},
                                         "critic": {"id": CRITIC, "num_ctx": 400000}}))
        res = W.start("ADD-03", PDF, route="ollama", offline=True, ai_config=cfgp, evidence=pack["out"],
                      staging=d / "staging", worklog=d / "worklog", run_id="off1", batch_size=8,
                      background_before=False, stop_after="critic", echo=quiet, sleep=lambda s: None)
        cp = W.load("off1", d / "staging").data
        md = W.review_markdown(W.Ctx(W.load("off1", d / "staging"), quiet))
    finally:
        mp.undo()
        f.stop()
    return {"res": res, "cp": cp, "md": md, "fake": f, "guard": guard, "dir": d}


def test_an_offline_run_uses_only_the_local_endpoint_and_the_local_critic(offline_run):
    r = offline_run
    cp, guard = r["cp"], r["guard"]
    assert r["res"]["status"] == "stopped" and "stopped after critic" in r["res"]["status_reason"], r["res"]
    assert cp["settings"]["route"] == "ollama" and cp["settings"]["offline"] == "--offline"
    assert guard.non_local() == [] and guard.refused == []
    assert not any(Path(p[0]).name in ("claude", "codex") for p in guard.processes)
    chats = [b for m, p, b in r["fake"].requests if p == "/api/chat"]
    assert {b["model"] for b in chats} == {TEXT, CRITIC}
    assert "POST /api/pull" not in r["fake"].paths()
    b = cp["batches"]
    assert b["analysis-001"]["status"] == "done" and b["analysis-002"]["status"] == "done"
    crit = b["analysis-002"]["critic"]
    assert crit["status"] == "done" and crit["route"] == "ollama" and crit["model_requested"] == CRITIC, crit
    assert crit["reviewed"] == 1 and crit["agrees"] == 1
    dcrit = b["downstream-001"]["critic"]
    assert dcrit["status"] == "done" and dcrit["route"] == "ollama" and dcrit["disagrees"] == 1
    assert cp["settings"]["ollama_preflight"]["models"], cp["settings"].get("ollama_preflight")


def test_offline_results_follow_the_same_validation_as_the_recorded_route(offline_run):
    """The same recorded answers through the Ollama adapter and through the recorded route give the same statuses:
    every route goes through the request layer and the controller's validation (session 11), offline included."""
    d = offline_run["dir"]
    comb = yaml.safe_load((d / "staging/runs/off1/ai/off1-combined/proposals.yaml").read_text(encoding="utf-8"))
    st = {x["id"]: x["verification_status"] for x in comb["proposal_set"]["items"]}
    assert st["ADD-03/2.4"] == "evidence_verified"
    it = next(x for x in comb["proposal_set"]["items"] if x["id"] == "ADD-03/2.4")
    assert it["review"]["critic"]["route"] == "ollama" and it["review"]["critic"]["agrees"] is True


def _addendum_with_image(d: Path) -> Path:
    doc = pymupdf.open(PDF)
    src = pymupdf.open()
    pg = src.new_page(width=460, height=80)
    pg.insert_text((12, 30), "Note: Bidders shall also submit one additional USB copy of Envelope B.", fontname="helv",
                   fontsize=11)
    doc[2].insert_image(pymupdf.Rect(66, 240, 526, 320), pixmap=pg.get_pixmap(dpi=200))
    out = Path(d) / "ADD-03_with_image.pdf"
    doc.save(out)
    return out


def test_a_local_model_without_vision_escalates_the_readings_to_a_person(tmp_path, pack, monkeypatch):
    """Readings need image input. A local model that does not report `vision` (/api/show) makes the readings step a
    visible 'cannot run locally with this model', its regions ESCALATED to a person (not skipped, not failed silently);
    ingest refuses the candidate without them (C05), so the text phases cannot start: the run stops with the reason
    and the way on."""
    f = FakeOllama({TEXT: show(context=400000)})
    f.start()
    try:
        guard = NetGuard(monkeypatch, allow_port=int(f.url.rsplit(":", 1)[1]))
        cfgp = _cfg_file(tmp_path, _cfg(f.url, {"text": {"id": TEXT, "num_ctx": 400000}}))
        res = W.start("ADD-03", _addendum_with_image(tmp_path), route="ollama", offline=True, ai_config=cfgp,
                      evidence=pack["out"], staging=tmp_path / "st", worklog=tmp_path / "wl", run_id="novis",
                      background_before=False, echo=quiet, sleep=lambda s: None)
    finally:
        f.stop()
    cp = W.load("novis", tmp_path / "st").data
    rb = [b for k, b in cp["batches"].items() if k.startswith("reading-")]
    assert rb and all(b["status"] == "escalated" for b in rb), rb
    assert "cannot run locally with this model" in rb[0]["error"] and TEXT in rb[0]["error"]
    assert res["status"] == "stopped" and "cannot run locally with this model" in res["status_reason"]
    assert res["exit_code"] == 6                                     # stopped for a person, never 0 (session 12)
    assert "escalated to a person" in res["status_reason"]
    assert any(e["event"] == "readings_escalated_to_person" for e in cp["events"])
    assert not [b for m, p, b in f.requests if p == "/api/chat"]           # nothing was asked of the model
    assert guard.non_local() == [] and not any(Path(p[0]).name == "claude" for p in guard.processes)


# ---------------------------------------------------------------------------------------------- `ai routes`

def test_ai_routes_lists_kinds_checks_ollama_and_marks_what_is_pending(tmp_path, fake, capsys, monkeypatch):
    from tenderpack.cli import main
    guard = NetGuard(monkeypatch, allow_port=int(fake.url.rsplit(":", 1)[1]))
    cfgp = _cfg_file(tmp_path, _cfg(fake.url, {"text": {"id": TEXT, "num_ctx": 32768}, "critic": {"id": CRITIC},
                                               "vision": {"id": "qwen3-vl:32b"}}))
    code = main(["ai", "routes", "--config", str(cfgp), "--json"])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    r = {x["route"]: x for x in out["routes"]}
    assert r["host"]["kind"] == "connected coding host" and r["ollama"]["kind"] == "local inference"
    assert r["anthropic"]["kind"] == r["openrouter"]["kind"] == "hosted API"
    assert r["recorded"]["kind"].startswith("recorded")
    assert "MCP interface tested; automated Codex execution unverified" in r["host"]["verified"]
    assert "not checked by this command" in r["anthropic"]["checked"]
    ol = {m["role"]: m for m in r["ollama"]["models"]}
    assert ol["text"]["tools"] is True and ol["vision"]["installed"] is False
    assert "PENDING ON THE MAC" in r["ollama"]["verified"]
    code = main(["ai", "routes", "--config", str(cfgp), "--offline"])
    text = capsys.readouterr().out
    assert code == 0 and "offline mode" in text and "disabled in offline mode" in text
    assert guard.non_local() == [] and guard.processes == []


# ---------------------------------------------------------------------------------------------- one set of rules

PLACEHOLDER = "placeholder-not-a-real-credential-0000"      # a test value, not a key: nothing is sent anywhere
CAPS = {"max_calls": 6, "max_input_tokens": 10 ** 6, "max_output_tokens": 10 ** 5}


def _ds_item(st, iid, task, statements=(), row="VOL-I-7.1-01"):
    return {"id": iid, "state": st, "statement_type": "row_reading", "task": task, "provision": "ADD-03:3.1",
            "target": row, "statements": list(statements),
            "payload": {"row": row, "interpretation": {"stage": "ADD-03", "quote": "one hundred and eighty (180) days"}},
            "evidence": [{"doc": "VOL-I", "unit_id": "VOL-I:7.1", "page": 4, "kind": "span",
                          "words": "one hundred and eighty (180) days"}]}


def test_every_route_applies_the_same_validation_to_the_same_answer(ws, tmp_path, monkeypatch):
    """The same downstream answer (one good item, one with free text where a statement id belongs, one of an unknown
    type), given twice (the first answer and the one bounded repair), through the Anthropic, OpenRouter and Ollama
    adapters (their real request and response code; HTTP recorded or a fake local server) and a host answer session
    (Claude Code or Codex: the same request layer, a stand-in CLI): every route gives the same items, the same item
    set aside, the same reference problem and the same repair. RECORDED/FAKE: not a live call."""
    import sys
    from tenderpack.ai import requests as R
    from tenderpack.ai.contract import DOWNSTREAM_TASK
    from tenderpack.ai.providers import anthropic as A
    from tenderpack.ai.providers import ollama as O
    from tenderpack.ai.providers import openrouter as OR
    from tenderpack.ai.providers.recorded import HttpCassette
    st = ws.identity().model_dump()
    good = _ds_item(st, "D1", "row:VOL-I-7.1-01", ["S1"])
    bad = _ds_item(st, "D2", "row:VOL-I-6.1-01", ["the clause says the delivery time moved"], row="VOL-I-6.1-01")
    broken = dict(_ds_item(st, "D3", "row:VOL-I-6.1-01", row="VOL-I-6.1-01"), statement_type="row_rewrite")
    stmts = [{"id": "S1", "kind": "interpretation", "text": "180 days now", "evidence": []}]
    answer = json.dumps({"addendum": "ADD-03", "state": st, "statements": stmts, "items": [good, bad, broken]})
    packet = {"task": DOWNSTREAM_TASK, "addendum": "ADD-03", "state": st, "tasks_total": 2,
              "tasks": [{"id": "row:VOL-I-7.1-01", "kind": "row_reading"}, {"id": "row:VOL-I-6.1-01", "kind": "row_reading"}]}
    results = {}

    def outcome(ctx):
        b = ctx.cp.batch("downstream-001")
        return {"repaired": b["request"]["repaired"], "malformed": [m["id"] for m in b.get("malformed_items") or []],
                "reference": [m["id"] for m in b["request"]["reference_problems"]]}

    def batch(ctx):
        ctx.cp.data["batches"]["downstream-001"] = {"phase": "downstream", "tasks": [t["id"] for t in packet["tasks"]],
                                                    "status": "running", "attempts": 1}

    # anthropic
    monkeypatch.setenv("ANTHROPIC_API_KEY", PLACEHOLDER)
    msg = {"response": {"body": {"model": "claude-opus-5-5", "stop_reason": "end_turn",
                                 "usage": {"input_tokens": 5, "output_tokens": 5},
                                 "content": [{"type": "text", "text": answer}]}}}
    cas = HttpCassette({"exchanges": [
        {"request": {"method": "GET", "path": "/v1/models/claude-opus-5-5"},
         "response": {"body": {"id": "claude-opus-5-5", "max_input_tokens": 1000000, "max_tokens": 128000,
                               "capabilities": {"structured_outputs": {"supported": False}}}}},
        {"request": {"method": "POST", "path": "/v1/messages"}, **msg},
        {"request": {"method": "POST", "path": "/v1/messages"}, **msg}]})
    monkeypatch.setattr(A, "http_json", cas)
    ctx = _ctx(tmp_path / "an", ws, copy.deepcopy(C.load()), route="anthropic")
    ctx.s["caps"] = CAPS
    batch(ctx)
    prov = A.AnthropicProvider("claude-opus-5-5", ctx.cfg["routes"]["anthropic"], {})
    ds = W._converse(ctx, prov, packet, "downstream-001")
    results["anthropic"] = ([it.id for it in ds.items], outcome(ctx))
    # openrouter
    listing = {"data": [{"id": "vendor/m", "context_length": 200000, "architecture": {"input_modalities": ["text"]},
                         "supported_parameters": ["tools"], "top_provider": {"max_completion_tokens": 32000}}]}
    ormsg = {"response": {"body": {"model": "vendor/m", "usage": {"prompt_tokens": 5, "completion_tokens": 5},
                                   "choices": [{"finish_reason": "stop", "message": {"content": answer}}]}}}
    cas2 = HttpCassette({"exchanges": [{"request": {"method": "POST", "path": "/chat/completions"}, **ormsg},
                                       {"request": {"method": "POST", "path": "/chat/completions"}, **ormsg}]})
    monkeypatch.setattr(OR, "http_json", cas2)
    ctx = _ctx(tmp_path / "or", ws, copy.deepcopy(C.load()), route="openrouter")
    ctx.s["caps"] = CAPS
    batch(ctx)
    prov = OR.OpenRouterProvider("vendor/m", ctx.cfg["routes"]["openrouter"], env={"OPENROUTER_API_KEY": PLACEHOLDER},
                                 fetch=lambda *a, **k: (200, {}, listing))
    ds = W._converse(ctx, prov, packet, "downstream-001")
    results["openrouter"] = ([it.id for it in ds.items], outcome(ctx))
    # ollama (a fake local server, real HTTP)
    f = FakeOllama({TEXT: show(context=262144)}, chat=lambda body: {
        "model": TEXT, "done": True, "done_reason": "stop", "message": {"role": "assistant", "content": answer},
        "prompt_eval_count": 5, "eval_count": 5})
    f.start()
    try:
        from tenderpack.ai import offline as OFF
        cfg = OFF.activate(_cfg(f.url, {"text": {"id": TEXT, "num_ctx": 262144}}), "--offline")
        ctx = _ctx(tmp_path / "ol", ws, cfg, route="ollama")
        batch(ctx)
        prov = O.OllamaProvider(TEXT, cfg["routes"]["ollama"], cfg["routes"]["ollama"]["models"]["text"])
        ds = W._converse(ctx, prov, packet, "downstream-001")
        results["ollama"] = ([it.id for it in ds.items], outcome(ctx))
    finally:
        f.stop()
        # session 14 (F4; R4-6): offline mode now switches the whole process (offline.switch_process); this test runs
        # four routes in one process, so the offline segment's switch is put back before the host segment (a real
        # process that went offline never starts a host session)
        OFF._PROCESS = None
        monkeypatch.delenv(OFF.ENV, raising=False)
    # host (Claude Code or Codex: a stand-in CLI that answers the same text, then the same repair)
    from tenderpack.ai.hostsession import SessionResult, declared_capabilities

    class Sess:
        model, last = None, None

        def capabilities(self):
            return declared_capabilities(cfg_h)

        def host_model_label(self):
            return "stand-in host"

        def system_prompt(self):
            return "S"

        def prompt(self, pk):
            return "TASK PACKET\n" + json.dumps(pk)

        def run_batch(self, pk):
            self.last = SessionResult(run_id="h1", addendum="ADD-03", provisions=[], started="-", model_requested=None,
                                      run_dir=str(tmp_path))
            self.last.final_text = answer
            return {}
    cli = tmp_path / "standin_cli"                # a stand-in for the host CLI: prints the same answer as JSON
    (tmp_path / "answer.json").write_text(json.dumps({"result": answer, "num_turns": 1,
                                                      "modelUsage": {"stand-in": {}}}), encoding="utf-8")
    cli.write_text(f"#!{sys.executable}\nimport sys\nsys.stdin.read()\n"
                   f"print(open({str(tmp_path / 'answer.json')!r}).read())\n", encoding="utf-8")
    cli.chmod(0o755)
    cfg_h = copy.deepcopy(C.load())
    cfg_h["host_session"] = {**cfg_h["host_session"], "claude_bin": str(cli)}
    ctx = _ctx(tmp_path / "ho", ws, cfg_h, route="host")
    batch(ctx)
    # session 13 (implementer C, deliberate): a system prompt is the runtime policy's composition (requests.spec refuses
    # a hand-written one such as system="S"); the host route's own composition here
    out = W._host_request(ctx, "downstream-001", R.spec("downstream", route="host"), Sess(), packet,
                          {"run_id": "x", "created": "-", "route": "host", "provider": "host-session",
                           "model_requested": "stand-in host", "model_reported": None, "task": DOWNSTREAM_TASK})
    results["host"] = ([it.id for it in out.answer.items], outcome(ctx))
    want = (["D1", "D2"], {"repaired": True, "malformed": ["D3"], "reference": ["D2"]})
    assert all(v == want for v in results.values()), results


def test_a_skipped_review_is_said_in_the_review_packet_and_the_candidate_readme(ws, tmp_path):
    """A batch whose selected items had no second-model review (offline, no local critic) is listed as a review that
    did not run, with its reason, in the review packet and the candidate README; never as agreement."""
    ctx = _ctx(tmp_path, ws, copy.deepcopy(C.load()))
    why = ("independent review did not run: offline mode: no local critic model is configured "
           "(routes.ollama.models.critic; it may name the same model as propose)")
    ctx.cp.data["batches"]["analysis-001"] = {"phase": "analysis", "provisions": [], "status": "done",
                                              "critic": {"status": "skipped", "route": "ollama", "selected": 2,
                                                         "selected_items": {"ADD-03/2.4": ["uncertain_target"],
                                                                            "ADD-03/4.1": ["removal"]},
                                                         "reason": why}}
    md = "\n".join(W.critic_section(ctx, None, None))
    assert "**Reviews that did not run**" in md and "this is not agreement" in md
    assert "ADD-03/2.4, ADD-03/4.1" in md and why in md
    out = tmp_path / "out"
    out.mkdir()
    (out / "README.md").write_text("# Candidate outputs\n", encoding="utf-8")
    W._review_not_run_note(ctx, out)
    text = (out / "README.md").read_text(encoding="utf-8")
    assert "## Independent review (the selective critic)" in text and f"- analysis-001: {why}" in text
    assert W.skipped_reviews(ctx.cp) == [("analysis-001", why)]
