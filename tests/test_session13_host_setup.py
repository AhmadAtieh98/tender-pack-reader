"""Session 13, E159 (the sealed blind-07 run from the interview folder): the reading host session's MCP server did not
start ("No module named tenderpack": the host CLI ignores the server config's `cwd` and starts the server in the
session folder, where a folder-only package is not importable), the host had no tools, the model wrote tool-call
markup as text, and the empty "reading" was validated and refused as an invalid reading instead of being named a
setup failure. Three fixes, each with its regression here:

  * hostsession.mcp_config puts the workspace root on the server's PYTHONPATH (the host CLI merges `env` into its own
    environment; verified on claude 2.1.291), so the server imports the package from the folder wherever it starts;
  * a session whose MCP server did not connect, or whose host offered none of the session's tools, is classified
    `setup` with the cause, never parsed as an answer, and requests.call_host raises at once (not retried: the
    environment must be fixed);
  * the Mac setup links the folder into .venv (scripts/mac/pathlink.py: a .pth file) and verifies the import from
    outside the folder; checks.sh checks it too.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tenderpack.ai import hostsession as HS
from tenderpack.ai import requests as R

ROOT = Path(__file__).resolve().parents[1]
MAC = ROOT / "scripts/mac"


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


def _cfg():
    return {"routes": {"host": {}}, "host_session": {"claude_bin": sys.executable,       # never run: a fake runner
                                                     "capabilities": {"context_tokens": 200000, "images": True,
                                                                      "max_output_tokens": 32000}}}


# what the real session recorded (staging/ai/runs/ADD-03-run-host-20261006T183015Z-9ae8/ai/...-044c)
MARKUP = ('I\'ll start by viewing the region image.\n\n\n<invoke name="get_region">\n'
          '<parameter name="region_id">ADD-03-p3-r1</parameter>\n</invoke>')
FAILED_INIT = {"type": "system", "subtype": "init", "model": "claude-sonnet-5-5", "permissionMode": "default",
               "tools": [], "mcp_servers": [{"name": "tenderpack", "status": "failed", "source": "dynamic"}]}
CONNECTED_INIT = {"type": "system", "subtype": "init", "model": "claude-sonnet-5-5", "permissionMode": "default",
                  "tools": ["mcp__tenderpack__get_region", "mcp__tenderpack__validate_reading"],
                  "mcp_servers": [{"name": "tenderpack", "status": "connected", "source": "dynamic"}]}


def _stream(init: dict, text: str) -> str:
    lines = [init,
             {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": text}]}},
             {"type": "result", "subtype": "success", "is_error": False, "num_turns": 1, "result": text,
              "usage": {"input_tokens": 2, "output_tokens": 187}, "modelUsage": {"claude-sonnet-5-5": {}},
              "total_cost_usd": 0.071438}]
    return "\n".join(json.dumps(x) for x in lines)


def _runner(stdout: str, calls: list):
    def run(cmd, input=None, **kw):
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, stdout, "")
    return run


PACKET = {"task": "propose_region_reading", "addendum": "ADD-03", "region_id": "ADD-03-p3-r1", "provisions": []}


# ---------------------------------------------------------------------------------------------- the server's environment

def test_the_mcp_server_is_started_with_the_folder_on_its_pythonpath(tmp_path, monkeypatch):
    ws = _WS(tmp_path)
    monkeypatch.delenv("PYTHONPATH", raising=False)
    for sess in (HS.HostSession(ws, _cfg()), HS.AnswerSession(ws, _cfg(), phase="reading")):
        srv = sess.mcp_config()["mcpServers"]["tenderpack"]
        assert srv["env"]["PYTHONPATH"] == str(Path(ws.root).resolve())
        assert srv["cwd"] == str(ws.root)                 # kept for clients that honour it; the host CLI does not
        assert srv["args"][:3] == ["-m", "tenderpack", "ai"]
    monkeypatch.setenv("PYTHONPATH", "/somewhere/else")
    srv = HS.HostSession(ws, _cfg()).mcp_config()["mcpServers"]["tenderpack"]
    assert srv["env"]["PYTHONPATH"] == str(Path(ws.root).resolve()) + os.pathsep + "/somewhere/else"


def test_the_server_command_imports_the_package_from_the_folder_when_started_elsewhere(tmp_path, monkeypatch):
    """The real failure, in miniature: a folder that holds the package, an interpreter that has it nowhere else
    (python -S -P: no site-packages, no working directory on sys.path), started in another folder exactly as the host
    CLI starts the server: with the config's env merged in and its cwd ignored."""
    ws = _WS(tmp_path)
    (ws.root / "tenderpack").mkdir()
    (ws.root / "tenderpack" / "__init__.py").write_text("MARK = 'from the folder'\n", encoding="utf-8")
    monkeypatch.delenv("PYTHONPATH", raising=False)
    srv = HS.HostSession(ws, _cfg()).mcp_config()["mcpServers"]["tenderpack"]
    elsewhere = tmp_path / "session-folder"
    elsewhere.mkdir()
    probe = [sys.executable, "-S", "-P", "-c", "import tenderpack; print(tenderpack.MARK)"]
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    without = subprocess.run(probe, cwd=elsewhere, env=env, capture_output=True, text=True)
    assert without.returncode != 0 and "No module named 'tenderpack'" in without.stderr   # as in E159
    with_env = subprocess.run(probe, cwd=elsewhere, env={**env, **srv["env"]}, capture_output=True, text=True)
    assert with_env.returncode == 0 and with_env.stdout.strip() == "from the folder", with_env.stderr
    normal = subprocess.run([sys.executable, "-P", "-c", "import tenderpack; print(tenderpack.__file__)"],
                            cwd=elsewhere, env={**env, **srv["env"]}, capture_output=True, text=True)
    assert normal.returncode == 0 and normal.stdout.strip().startswith(str(ws.root.resolve())), normal.stderr


# ---------------------------------------------------------------------------------------------- a setup failure

def test_a_session_whose_mcp_server_failed_is_a_setup_failure_not_an_answer(tmp_path):
    ws = _WS(tmp_path)
    calls: list = []
    sess = HS.AnswerSession(ws, _cfg(), phase="reading", runner=_runner(_stream(FAILED_INIT, MARKUP), calls))
    sess.run_batch(PACKET)
    res = sess.last
    assert len(calls) == 1
    assert res.failure_class == "setup", (res.failure_class, res.error)
    assert res.error and "MCP server" in res.error and "did not connect" in res.error and "failed" in res.error
    assert res.mcp_servers == FAILED_INIT["mcp_servers"]
    assert res.final_text == MARKUP                 # kept for the record, never taken as the reading
    rec = json.loads((Path(res.run_dir) / "session.json").read_text(encoding="utf-8"))
    assert rec["failure_class"] == "setup" and rec["mcp_servers"] == FAILED_INIT["mcp_servers"]
    log = [json.loads(x) for x in (Path(res.run_dir) / "log.jsonl").read_text(encoding="utf-8").splitlines()]
    ev = next(e for e in log if e.get("event") == "failure_class")
    assert ev["failure_class"] == "setup" and "did not connect" in ev["error"]


def test_the_servers_stderr_is_named_when_the_host_cli_logged_it(tmp_path, monkeypatch):
    ws = _WS(tmp_path)
    home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home))
    calls: list = []
    sess = HS.AnswerSession(ws, _cfg(), phase="reading", runner=_runner(_stream(FAILED_INIT, MARKUP), calls))

    def run(cmd, input=None, **kw):                 # the CLI writes its MCP log while the session runs
        run_dir = Path(kw["cwd"])
        d = home / ".cache/claude-cli-nodejs" / run_dir.name / "mcp-logs-tenderpack"
        d.mkdir(parents=True)
        (d / "2026-10-06T18-30-34-000Z.jsonl").write_text(
            json.dumps({"debug": "Starting connection with timeout of 30000ms", "cwd": str(run_dir)}) + "\n"
            + json.dumps({"error": "Server stderr: /x/.venv/bin/python: No module named tenderpack\n",
                          "cwd": str(run_dir)}) + "\n"
            + json.dumps({"error": "Connection failed (CONNECTION_CLOSED): Connection closed", "cwd": str(run_dir)})
            + "\n", encoding="utf-8")
        return subprocess.CompletedProcess(cmd, 0, _stream(FAILED_INIT, MARKUP), "")
    sess.runner = run
    sess.run_batch(PACKET)
    assert "No module named tenderpack" in (sess.last.error or "")


def test_a_connected_server_that_offers_none_of_the_sessions_tools_is_a_setup_failure(tmp_path):
    ws = _WS(tmp_path)
    init = dict(CONNECTED_INIT, tools=["mcp__tenderpack__get_unit"])      # connected, but not this session's tools
    sess = HS.AnswerSession(ws, _cfg(), phase="reading", runner=_runner(_stream(init, MARKUP), []))
    sess.run_batch(PACKET)
    assert sess.last.failure_class == "setup" and "offered none of" in (sess.last.error or "")


def test_a_connected_server_with_the_sessions_tools_is_not_a_setup_failure(tmp_path):
    ws = _WS(tmp_path)
    text = json.dumps({"reading": {"doc": "ADD-03", "page": 3}})
    sess = HS.AnswerSession(ws, _cfg(), phase="reading", runner=_runner(_stream(CONNECTED_INIT, text), []))
    sess.run_batch(PACKET)
    assert sess.last.failure_class is None and sess.last.error is None and sess.last.final_text == text
    # an init without the servers' statuses (an older CLI, a fake) is not judged: no servers listed, a server entry
    # without a status (tests/fixtures/ai_cassettes/fake_claude_s11.py), or no MCP tool listed at all
    for init in ({"type": "system", "subtype": "init", "model": "fake-host-model", "tools": []},
                 {"type": "system", "subtype": "init", "model": "fake-host-model", "tools": [],
                  "mcp_servers": [{"name": "tenderpack"}]},
                 dict(CONNECTED_INIT, tools=[])):
        sess = HS.AnswerSession(ws, _cfg(), phase="reading", runner=_runner(_stream(init, text), []))
        sess.run_batch(PACKET)
        assert sess.last.failure_class is None and sess.last.error is None, init


def test_call_host_does_not_retry_a_setup_failure():
    slept: list = []
    attempts: list = []
    n = {"runs": 0}

    def run():
        n["runs"] += 1
        res = HS.SessionResult(run_id="r", addendum="ADD-03", provisions=[], started="now")
        res.error = "the tenderpack MCP server did not connect (status failed): No module named tenderpack"
        res.final_text = MARKUP
        HS.classify(res)
        assert res.failure_class == "setup"
        return res
    pol = R.FailurePolicy()
    with pytest.raises(R.ProviderFailed) as ei:
        R.call_host(run, pol, sleep=slept.append, record=attempts.append)
    assert n["runs"] == 1 and slept == []                     # asked once; nothing waited for
    assert "did not connect" in ei.value.message and "not retried" in ei.value.message
    assert len(attempts) == 1 and attempts[0]["kind"] == "host_setup"


def test_classify_orders_setup_after_a_refusal_and_before_the_rest():
    res = HS.SessionResult(run_id="r", addendum="A", provisions=[], started="now")
    res.error = "refused: the lock is held"
    assert HS.classify(res) == "refused"
    res = HS.SessionResult(run_id="r", addendum="A", provisions=[], started="now")
    res.error = "the tenderpack MCP server did not connect (status failed)"
    res.api_error_status = 429                                 # even with a limit message: the setup failed first
    assert HS.classify(res) == "setup"


# ---------------------------------------------------------------------------------------------- the Mac folder

def test_pathlink_writes_the_folder_into_the_venv_and_verifies_the_import_from_outside(tmp_path):
    site = tmp_path / "site-packages"
    site.mkdir()
    folder = tmp_path / "LAMAR"
    (folder / "tenderpack").mkdir(parents=True)
    (folder / "tenderpack" / "__init__.py").write_text("", encoding="utf-8")
    r = subprocess.run([sys.executable, str(MAC / "pathlink.py"), "--root", str(folder), "--site-dir", str(site),
                        "--python", sys.executable], capture_output=True, text=True)
    pth = site / "tenderpack-folder.pth"
    assert pth.exists() and pth.read_text(encoding="utf-8") == str(folder.resolve()) + "\n"
    # the verification runs the interpreter OUTSIDE the folder: this test session's python imports the repository's
    # package, not the fake folder's, so the verification reports the mismatch and the script fails
    assert r.returncode != 0 and str(ROOT) in (r.stdout + r.stderr), r.stdout + r.stderr
    r2 = subprocess.run([sys.executable, str(MAC / "pathlink.py"), "--root", str(ROOT), "--site-dir", str(site),
                         "--python", sys.executable], capture_output=True, text=True)
    assert r2.returncode == 0 and "imports from" in r2.stdout, r2.stdout + r2.stderr
    assert pth.read_text(encoding="utf-8") == str(ROOT) + "\n"           # rewritten, never appended


def test_setup_and_checks_link_and_verify_the_folder():
    setup = (MAC / "setup.sh").read_text(encoding="utf-8")
    assert "pathlink.py" in setup and "--root" in setup
    checks = (MAC / "checks.sh").read_text(encoding="utf-8")
    assert "pathlink.py" in checks
    r = subprocess.run(["bash", str(MAC / "checks.sh"), "--plan"], capture_output=True, text=True)
    assert any("outside the folder" in x for x in r.stdout.splitlines()), r.stdout
