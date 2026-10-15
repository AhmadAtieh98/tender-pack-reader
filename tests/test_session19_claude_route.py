"""The interview demo on the Claude Code host route (the Codex route is kept as a second profile).

  * config/interview-ai.yaml selects the `claude` driver with an explicit model for the host sessions and the critic;
    config/interview-ai-codex.yaml keeps the Codex profile with the same interview parameters;
  * the configured reasoning effort reaches the Claude Code CLI (`--effort`), as it reaches Codex;
  * a CLI that rejects its own command line (an older Claude Code: "error: unknown option '--permission-prompts'")
    exits without a result; the cause is named in the session's error and the session is a `setup` failure (asking
    again cannot help), never an empty provider failure.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from tenderpack.ai import hostsession as HS
from tenderpack.ai import policy

ROOT = Path(__file__).resolve().parents[1]


def _profile(name: str) -> dict:
    return yaml.safe_load((ROOT / "config" / name).read_text(encoding="utf-8"))


class _WS:
    def __init__(self, tmp: Path):
        self.root = tmp / "folder"
        self.evidence = self.root / "build"
        self.pack = self.root / "pack.yaml"
        self.staging = tmp / "staging"
        self.worklog = tmp / "worklog"
        self.ai_config = None
        for d in (self.evidence, self.staging, self.worklog):
            d.mkdir(parents=True, exist_ok=True)
        self.pack.write_text("documents: []\n", encoding="utf-8")


def _claude_cfg(**extra) -> dict:
    hs = {"driver": "claude", "claude_bin": sys.executable, "model": "claude-opus-5-5",
          "capabilities": {"context_tokens": 200000, "images": True, "max_output_tokens": 32000}, **extra}
    return {"routes": {"host": {}}, "host_session": hs}


# ---------------------------------------------------------------------------------------------- the profiles

def test_interview_profile_selects_the_claude_code_driver_and_an_explicit_model(tmp_path):
    cfg = _profile("interview-ai.yaml")
    assert HS.settings(cfg)["driver"] == "claude"
    assert cfg["host_session"]["model"] == "claude-opus-5-5"
    assert cfg["critic"]["route"] == "host" and cfg["critic"]["model"] == "claude-opus-5-5"
    host = HS.HostSession(SimpleNamespace(ai_config=None), cfg)
    cmd = host.command(tmp_path / "mcp.json")
    assert cmd[0] == "claude" and "tenderpack.ai.codex" not in cmd
    assert cmd[cmd.index("--model") + 1] == "claude-opus-5-5"
    assert cmd[cmd.index("--tools") + 1] == "" and "--strict-mcp-config" in cmd
    assert cmd[cmd.index("--permission-prompts") + 1] == "none"
    assert host.host_model_label() == "claude-code headless (claude-opus-5-5)"
    plain = HS.PlainSession(cfg, policy.compose("critic", "host"), label="critic")
    assert plain.command()[0] == "claude" and "tenderpack.ai.codex" not in plain.command()


def test_codex_profile_is_kept_with_the_same_interview_parameters():
    claude, codex = _profile("interview-ai.yaml"), _profile("interview-ai-codex.yaml")
    assert codex["host_session"]["driver"] == "codex"
    assert codex["host_session"]["model"] == codex["critic"]["model"]
    for key in ("interview", "concurrency", "batching", "failures", "routes", "defaults"):
        assert claude[key] == codex[key], key
    for key in ("max_turns", "timeout_s", "plain_timeout_s", "output_format", "durable_answers", "reasoning_effort"):
        assert claude["host_session"][key] == codex["host_session"][key], key
    assert claude["critic"]["host"] == codex["critic"]["host"]


def test_prepare_selects_the_profile_for_the_chosen_host():
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import prepare_interview_demo as P
    finally:
        sys.path.remove(str(ROOT / "scripts"))
    assert P.HOSTS["claude"]["profile"] == ROOT / "config/interview-ai.yaml"
    assert P.HOSTS["codex"]["profile"] == ROOT / "config/interview-ai-codex.yaml"
    assert P.parse(["/tmp/x"]) == (Path("/tmp/x").resolve(), "claude")
    assert P.parse(["--host", "codex", "/tmp/x"]) == (Path("/tmp/x").resolve(), "codex")
    with pytest.raises(SystemExit):
        P.parse(["--host", "other", "/tmp/x"])
    guide = P.guide_text("claude")
    assert "Claude Code" in guide and "Codex" not in guide
    assert "Codex" in P.guide_text("codex")


# ---------------------------------------------------------------------------------------------- effort

def test_claude_driver_passes_the_configured_reasoning_effort(tmp_path):
    cfg = _claude_cfg(reasoning_effort="high")
    host = HS.HostSession(SimpleNamespace(ai_config=None), cfg)
    cmd = host.command(tmp_path / "mcp.json")
    assert cmd[cmd.index("--effort") + 1] == "high"
    answer = HS.AnswerSession(SimpleNamespace(ai_config=None), cfg, phase="reading")
    acmd = answer.command(tmp_path / "mcp.json")
    assert acmd[acmd.index("--effort") + 1] == "high"
    plain = HS.PlainSession(cfg, policy.compose("critic", "host"), label="critic")
    assert plain.command()[plain.command().index("--effort") + 1] == "high"


def test_claude_driver_without_a_configured_effort_leaves_the_cli_default(tmp_path):
    cfg = _claude_cfg()
    host = HS.HostSession(SimpleNamespace(ai_config=None), cfg)
    assert "--effort" not in host.command(tmp_path / "mcp.json")
    assert "--effort" not in HS.PlainSession(cfg, policy.compose("critic", "host"), label="critic").command()


def test_codex_settings_still_carry_the_effort_without_a_claude_flag(tmp_path):
    cfg = {"host_session": {"driver": "codex", "codex_bin": "/bin/echo", "model": "configured-test-model",
                            "reasoning_effort": "high", "max_mcp_calls": 120, "timeout_s": 420}}
    cmd = HS.HostSession(SimpleNamespace(ai_config=None), cfg).command(tmp_path / "mcp.json")
    assert json.loads(cmd[cmd.index("--codex-settings") + 1])["reasoning_effort"] == "high"
    assert "--effort" not in cmd


# ---------------------------------------------------------------------------------------------- a rejected command line

USAGE = "error: unknown option '--permission-prompts'\n"


def _rejecting(cmd, input=None, **kw):
    return subprocess.CompletedProcess(cmd, 1, "", USAGE)


def test_a_cli_that_rejects_its_command_line_is_a_named_setup_failure(tmp_path):
    ws = _WS(tmp_path)
    s = HS.AnswerSession(ws, _claude_cfg(), phase="reading", runner=_rejecting)
    s.run_batch({"task": "propose_region_reading", "addendum": "ADD-03", "region_id": "ADD-03-p1-r1",
                 "provisions": []})
    assert s.last.failure_class == "setup"
    assert "unknown option '--permission-prompts'" in s.last.error
    assert "rejected its command line" in s.last.error


def test_a_plain_session_whose_cli_rejects_its_command_line_is_a_setup_failure(tmp_path):
    ps = HS.PlainSession(_claude_cfg(), policy.compose("critic", "host"), label="critic", runner=_rejecting)
    res = ps.run("prompt", tmp_path)
    assert res.failure_class == "setup"
    assert "unknown option '--permission-prompts'" in res.error


def test_an_ordinary_nonzero_exit_without_a_usage_error_stays_a_provider_failure(tmp_path):
    ws = _WS(tmp_path)
    def crashed(cmd, input=None, **kw):
        return subprocess.CompletedProcess(cmd, 1, "", "Segmentation fault\n")
    s = HS.AnswerSession(ws, _claude_cfg(), phase="reading", runner=crashed)
    s.run_batch({"task": "propose_region_reading", "addendum": "ADD-03", "region_id": "ADD-03-p1-r1",
                 "provisions": []})
    assert s.last.failure_class == "provider"
    assert "Segmentation fault" in (s.last.error or "")


# ---------------------------------------------------------------------------------------------- reported models

def _usage(**out):
    return {m.replace("_", "-"): {"inputTokens": 10, "outputTokens": n} for m, n in out.items()}


def test_a_tool_session_reports_the_model_it_ran_on_and_keeps_auxiliary_usage_apart(tmp_path):
    """The timed ADD03 run (11 Oct): every assistant message and the init came from claude-opus-5-5, while the CLI's
    modelUsage also listed claude-haiku-5-5 (553,561 input / 333 output tokens over ten sessions, no message)."""
    usage = _usage(claude_opus_5_5=2000, claude_haiku_5_5=33)
    lines = [{"type": "system", "subtype": "init", "model": "claude-opus-5-5", "tools": [], "mcp_servers": []},
             {"type": "assistant", "message": {"model": "claude-opus-5-5", "content": [{"type": "text", "text": "{}"}]}},
             {"type": "result", "subtype": "success", "is_error": False, "num_turns": 1, "result": "{}",
              "modelUsage": usage}]
    def run(cmd, input=None, **kw):
        return subprocess.CompletedProcess(cmd, 0, "\n".join(json.dumps(x) for x in lines), "")
    s = HS.AnswerSession(_WS(tmp_path), _claude_cfg(), phase="reading", runner=run)
    s.run_batch({"task": "propose_region_reading", "addendum": "ADD-03", "region_id": "ADD-03-p1-r1", "provisions": []})
    assert s.last.model_reported == ["claude-opus-5-5"]
    assert s.last.model_auxiliary == {"claude-haiku-5-5": {"inputTokens": 10, "outputTokens": 33}}


def test_a_plain_session_reports_the_model_with_the_answer_and_keeps_auxiliary_usage_apart(tmp_path):
    out = {"type": "result", "subtype": "success", "is_error": False, "result": "{}", "num_turns": 1,
           "modelUsage": _usage(claude_haiku_5_5=30, claude_opus_5_5=900)}
    def run(cmd, input=None, **kw):
        return subprocess.CompletedProcess(cmd, 0, json.dumps(out), "")
    res = HS.PlainSession(_claude_cfg(), policy.compose("critic", "host"), label="critic", runner=run).run("p", tmp_path)
    assert res.model_reported == ["claude-opus-5-5"]
    assert list(res.model_auxiliary) == ["claude-haiku-5-5"]


def test_usage_without_token_counts_names_every_model_as_reported():
    """The Codex transport's modelUsage carries model names only: nothing is ranked or set aside."""
    assert HS.split_models({"a": {}, "b": {}}, []) == (["a", "b"], {})
    assert HS.split_models({}, ["m"]) == (["m"], {})


def test_the_clis_synthetic_messages_are_not_a_model_the_session_ran_on(tmp_path):
    lines = [{"type": "assistant", "message": {"model": "<synthetic>", "content": [{"type": "text", "text": "x"}]}},
             {"type": "result", "subtype": "success", "is_error": True, "num_turns": 1, "result": "x",
              "modelUsage": {}}]
    def run(cmd, input=None, **kw):
        return subprocess.CompletedProcess(cmd, 1, "\n".join(json.dumps(x) for x in lines), "")
    s = HS.AnswerSession(_WS(tmp_path), _claude_cfg(), phase="reading", runner=run)
    s.run_batch({"task": "propose_region_reading", "addendum": "ADD-03", "region_id": "ADD-03-p1-r1", "provisions": []})
    assert s.last.model_reported == []


def test_the_review_packet_names_auxiliary_models_apart_from_the_session_models():
    from tenderpack.ai import workflow as W
    d = {"batches": {"analysis-001": {"host_session": {"model_reported": ["claude-opus-5-5"],
                                                       "model_auxiliary": ["claude-haiku-5-5"]}},
                     "downstream-001": {"host_session": {"model_reported": ["claude-opus-5-5"]}}}}
    assert W._auxiliary_models(d) == "; also in the host CLI's usage, with no answer turn: claude-haiku-5-5"
    assert W._auxiliary_models({"batches": {"a": {"host_session": {"model_reported": ["m"]}}}}) == ""
