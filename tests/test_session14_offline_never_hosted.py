"""Session 14 (W6, part 7, item 2): offline mode never falls back to a hosted model.

Proved at every constructor and at the run level, with both switches (`TENDERPACK_OFFLINE=1` and `--offline`):

  * every hosted adapter refuses to be BUILT in offline mode, also when built directly (not through providers.make):
    AnthropicProvider, OpenRouterProvider, HostProvider (before session 14 only providers.make checked, so an adapter
    built directly in an offline process could still reach a hosted endpoint);
  * the HTTP layer every adapter shares (providers.base.http_json) refuses a non-loopback address in an offline
    process BEFORE any connection (the last line: whatever builds a request, nothing hosted is reached);
  * the Ollama adapter refuses a non-loopback base URL in an offline process (it would otherwise be a hosted model
    behind the "local" route);
  * the run (`ai run`), the one-batch request (`ai propose`), the capability check, the batch planner, the critic
    (`ai critic`) and the quick review (`ai quick-review`) refuse a hosted route before any process or connection;
    a hosted route CONFIGURED for the critic (config `critic.route`) is never used offline; with
    TENDERPACK_OFFLINE=1 and no --route, the run and the quick review default to the local route, never the host.

A NetGuard (tests/fixtures/fake_ollama.py) records every socket connection and every process: nothing hosted may be
reached and no `claude` / `codex` process may start. Tested in the cloud container; the same on the Mac is PENDING."""
from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from ai_fixture import CASSETTES, ROOT, workspace
from fake_ollama import NetGuard

PDF = ROOT / "rehearsals/blind-02/input/ADD-03_Addendum_No_3.pdf"
HOSTED = ("host", "anthropic", "openrouter")


def _guard(monkeypatch) -> NetGuard:
    return NetGuard(monkeypatch, allow_port=1)            # nothing at all may be reached


def _no_hosted(guard: NetGuard) -> None:
    assert guard.non_local() == [], guard.connects                # a loopback attempt (the local Ollama) is allowed
    assert not any(Path(p[0]).name in ("claude", "codex") for p in guard.processes), guard.processes


# ---------------------------------------------------------------------------------------------- constructors

def test_every_hosted_adapter_refuses_to_be_built_in_an_offline_process(monkeypatch):
    from tenderpack.ai import config as C
    from tenderpack.ai.offline import OfflineError
    from tenderpack.ai.providers.anthropic import AnthropicProvider
    from tenderpack.ai.providers.host import HostProvider
    from tenderpack.ai.providers.openrouter import OpenRouterProvider
    guard = _guard(monkeypatch)
    monkeypatch.setenv("TENDERPACK_OFFLINE", "1")
    cfg = C.load()
    with pytest.raises(OfflineError, match="offline mode"):
        AnthropicProvider("claude-opus-5-5", cfg["routes"]["anthropic"], {})
    with pytest.raises(OfflineError, match="offline mode"):
        OpenRouterProvider("vendor/m", cfg["routes"]["openrouter"], {})
    with pytest.raises(OfflineError, match="offline mode"):
        HostProvider("declared-model")
    _no_hosted(guard)
    monkeypatch.delenv("TENDERPACK_OFFLINE")                  # connected: the adapters are built as before
    AnthropicProvider("claude-opus-5-5", cfg["routes"]["anthropic"], {})
    HostProvider("declared-model")


def test_the_http_layer_refuses_a_hosted_address_in_an_offline_process(monkeypatch):
    from tenderpack.ai.offline import OfflineError
    from tenderpack.ai.providers import base
    guard = _guard(monkeypatch)
    monkeypatch.setenv("TENDERPACK_OFFLINE", "1")
    for url in ("https://api.anthropic.com/v1/models/claude-opus-5-5", "https://openrouter.ai/api/v1/models",
                "http://10.0.0.5:11434/api/show"):
        with pytest.raises(OfflineError, match="not a loopback address"):
            base.http_json("GET", url, {}, None, 5)
    _no_hosted(guard)


def test_the_ollama_adapter_refuses_a_remote_base_url_in_an_offline_process(monkeypatch):
    from tenderpack.ai import config as C
    from tenderpack.ai.offline import OfflineError
    from tenderpack.ai.providers.ollama import OllamaProvider
    guard = _guard(monkeypatch)
    monkeypatch.setenv("TENDERPACK_OFFLINE", "1")
    rc = copy.deepcopy(C.load()["routes"]["ollama"])
    with pytest.raises(OfflineError, match="not a loopback address"):
        OllamaProvider("m", rc, {}, env={"TENDERPACK_OLLAMA_URL": "https://ollama.example.net"})
    OllamaProvider("m", rc, {}, env={"TENDERPACK_OLLAMA_URL": "http://127.0.0.1:11434"})     # local: built
    _no_hosted(guard)


# ---------------------------------------------------------------------------------------------- the run level

@pytest.fixture(scope="module")
def ws(request, tmp_path_factory):
    return workspace(tmp_path_factory.mktemp("s14-offline"), evidence=request.getfixturevalue("blind02_build"))


def _main(args, capsys) -> tuple[int, str]:
    from tenderpack.cli import main
    code = main(args)
    return code, capsys.readouterr().out


_STAGED: dict = {}


def staged_run(ws):
    """One staged proposal run (the recorded route) for the critic to be asked about."""
    if "run" not in _STAGED:
        from tenderpack.ai import controller
        _STAGED["run"] = controller.propose(ws, "ADD-03", "recorded", None, cassette=CASSETTES / "add03_propose.yaml")
    return _STAGED["run"]


@pytest.mark.parametrize("switch", ["flag", "env"])
def test_every_command_refuses_a_hosted_route_offline_before_any_call(ws, tmp_path, monkeypatch, capsys, switch):
    """`--offline` or TENDERPACK_OFFLINE=1: each command that takes a route refuses host, anthropic and openrouter
    with exit 2 and an 'offline mode' reason, and nothing is connected to and no host process starts."""
    staged = staged_run(ws)
    guard = _guard(monkeypatch)
    off = ["--offline"] if switch == "flag" else []
    if switch == "env":
        monkeypatch.setenv("TENDERPACK_OFFLINE", "1")
    common = ["--evidence", str(ws.evidence), "--pack", str(ws.pack), "--out", str(ws.staging),
              "--worklog", str(ws.worklog)]
    for route in HOSTED:
        runs = tmp_path / route / "staging"
        cases = {
            "run": ["ai", "run", "ADD-03", "--pdf", str(PDF), "--route", route, "--out", str(runs),
                    "--worklog", str(tmp_path / "wl"), *off],
            "quick-review": ["ai", "quick-review", "ADD-03", "--pdf", str(PDF), "--route", route,
                             "--out", str(tmp_path / route / "qr"), "--worklog", str(tmp_path / "wl"), *off],
            "critic": ["ai", "critic", staged.run_id, "--route", route, *common, *off]}
        heavy = switch == "flag" or route == "anthropic"     # the commands that read the workspace first: every
        if not heavy:                                          # route with the flag, one with the environment
            cases.pop("critic")
        if route != "host" and heavy:
            cases["propose"] = ["ai", "propose", "ADD-03", "--route", route, "--model", "m", *common, *off]
            cases["plan-batches"] = ["ai", "plan-batches", "ADD-03", "--route", route, "--model", "m", *common, *off]
        cases["capabilities"] = ["ai", "capabilities", "--route", route, "--model", "m", *off]
        for name, args in cases.items():
            code, out = _main(args, capsys)
            assert code == 2 and "offline mode" in out, (switch, route, name, code, out[-600:])
        assert not (runs / "runs").exists() or not any((runs / "runs").iterdir())       # nothing was created
    _no_hosted(guard)


def test_offline_defaults_are_local_and_a_configured_hosted_critic_is_never_used(ws, tmp_path, monkeypatch, capsys):
    """With TENDERPACK_OFFLINE=1 and no --route, the run and the quick review choose the local route (and say so when
    no local model answers), never the host; a hosted route CONFIGURED for the critic (critic.route: anthropic or
    host) is not consulted offline: the critic is local or recorded as skipped."""
    from tenderpack.ai import config as C
    from tenderpack.ai import workflow as W
    from tenderpack.ai.checkpoint import Checkpoint
    guard = _guard(monkeypatch)
    monkeypatch.setenv("TENDERPACK_OFFLINE", "1")
    monkeypatch.setenv("TENDERPACK_OLLAMA_URL", "http://127.0.0.1:9")             # nothing answers there
    code, out = _main(["ai", "run", "ADD-03", "--pdf", str(PDF), "--out", str(tmp_path / "st"),
                       "--worklog", str(tmp_path / "wl")], capsys)
    assert code == 2 and "REFUSED: Ollama at http://127.0.0.1:9 could not be reached" in out, out[-400:]
    code, out = _main(["ai", "quick-review", "ADD-03", "--pdf", str(PDF), "--out", str(tmp_path / "qr"),
                       "--worklog", str(tmp_path / "wl")], capsys)
    assert "quick review ADD-03-qr-ollama-" in out and "on the ollama route" in out, out[-400:]
    assert "refused (capability check failed: Ollama at http://127.0.0.1:9" in out, out[-400:]
    assert not any(Path(p[0]).name == "claude" for p in guard.processes)
    for configured in ("anthropic", "openrouter", "host"):
        cfg = copy.deepcopy(C.load())
        cfg["critic"] = {**cfg["critic"], "route": configured, "model": "a-hosted-model"}
        settings = {"addendum": "ADD-03", "route": "ollama", "worklog": str(tmp_path / "wl"),
                    "staging": str(tmp_path / "s"), "caps": {}, "ai_config": None, "model": None, "batch_size": 8,
                    "downstream_batch_size": 12}
        cp = Checkpoint.new(tmp_path / configured / "checkpoint.json", run_id="t14", addendum="ADD-03",
                            settings=settings, inputs={}, candidate={})
        ctx = W.Ctx(cp, echo=lambda *a, **k: None, sleep=lambda s: None)
        ctx._ws, ctx._cfg = ws, cfg
        route, _, why, model = W._critic_route(ctx, ["ADD-03/2.1"])
        assert route == "ollama" and model != "a-hosted-model", (configured, route, why, model)
    _no_hosted(guard)


def test_the_launcher_and_the_checks_switch_offline_for_every_child_process():
    """The Mac scripts export TENDERPACK_OFFLINE=1 (so every child `tenderpack` process, the panel's jobs included,
    builds no hosted adapter), and nothing in scripts/mac names a hosted endpoint."""
    for name in ("checks.sh", "launch.command"):
        text = (ROOT / "scripts/mac" / name).read_text(encoding="utf-8")
        assert "export TENDERPACK_OFFLINE=1" in text, name
        assert "api.anthropic.com" not in text and "openrouter.ai" not in text, name
    levels = (ROOT / "scripts/mac/levels.py").read_text(encoding="utf-8")
    assert "http" not in levels.replace("https?", "")             # the levels read files only
    assert yaml.safe_load((ROOT / "config/ai.yaml").read_text(encoding="utf-8"))["offline"] is False
