"""Session 13, E161 (the sealed blind-07 run, attempt 3): the planned SIGTERM killed the two host sessions in flight
(exit 143, no result); their worker threads saw a provider failure and ASKED AGAIN 3 s later, so two new sessions
ran under a run already recorded as stopped, the run's process could not end while they ran, the panel's job stayed
"running" and the panel refused the resume (409). The fix: terminate_live() sets a stop flag; while it is set no host
session starts (HostSession.run_batch and PlainSession.run refuse) and requests.call_host raises instead of retrying."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tenderpack.ai import hostsession as HS
from tenderpack.ai import requests as R


@pytest.fixture(autouse=True)
def _fresh():
    HS.reset_stop()
    yield
    HS.reset_stop()


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
    return {"routes": {"host": {}}, "host_session": {"claude_bin": sys.executable,
                                                     "capabilities": {"context_tokens": 200000, "images": True,
                                                                      "max_output_tokens": 32000}}}


PACKET = {"task": "propose_downstream", "addendum": "ADD-03", "provisions": []}


def test_terminate_live_sets_the_stop_flag_and_no_session_starts_after_it(tmp_path):
    calls: list = []

    def runner(cmd, input=None, **kw):
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, "", "")
    assert not HS.stopping()
    assert HS.terminate_live() == 0                      # nothing was running; the flag is set all the same
    assert HS.stopping()
    sess = HS.AnswerSession(_WS(tmp_path), _cfg(), phase="downstream", runner=runner)
    sess.run_batch(PACKET)
    assert calls == []                                   # the host CLI was never started
    assert sess.last.failure_class == "refused" and "stopping" in (sess.last.error or "")
    log = [json.loads(x) for x in (Path(sess.last.run_dir) / "log.jsonl").read_text(encoding="utf-8").splitlines()]
    assert any(e.get("event") == "refused" and "stopping" in (e.get("reason") or "") for e in log)
    HS.reset_stop()
    assert not HS.stopping()


def test_a_session_killed_by_the_interruption_is_not_asked_again(tmp_path):
    """The live sequence in miniature: the interruption arrives while the session runs (terminate_live is called
    from the signal handler), the CLI dies with exit 143 and no result, the worker's call_host sees a provider
    failure: before the fix it slept the backoff and started a second session."""
    n = {"runs": 0}
    slept: list = []

    def runner(cmd, input=None, **kw):
        n["runs"] += 1
        HS.terminate_live()                              # the SIGTERM handler, while this session is in flight
        return subprocess.CompletedProcess(cmd, 143, "", "")
    sess = HS.AnswerSession(_WS(tmp_path), _cfg(), phase="downstream", runner=runner)

    def run():
        sess.run_batch(PACKET)
        return sess.last
    with pytest.raises(R.ProviderFailed) as ei:
        R.call_host(run, R.FailurePolicy(), sleep=slept.append)
    assert n["runs"] == 1 and slept == []                # one session, nothing waited for, nothing asked again
    assert "stopping" in ei.value.message and ei.value.attempts and ei.value.attempts[0]["kind"] == "host_provider"


def test_a_rate_limited_session_is_not_waited_for_while_stopping():
    slept: list = []

    def run():
        res = HS.SessionResult(run_id="r", addendum="ADD-03", provisions=[], started="now")
        res.api_error_status = 429
        res.error = "the host ended with an error (api_error: 429)"
        HS.classify(res)
        assert res.failure_class == "rate_limit"
        return res
    HS.terminate_live()
    with pytest.raises(R.ProviderFailed):
        R.call_host(run, R.FailurePolicy(), sleep=slept.append)
    assert slept == []


def test_a_plain_session_refuses_to_start_while_stopping(tmp_path):
    from tenderpack.ai import policy as P
    calls: list = []

    def runner(cmd, input=None, **kw):
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, json.dumps({"result": "x"}), "")
    HS.terminate_live()
    ps = HS.PlainSession(_cfg(), P.compose("critic", "host"), runner=runner, label="critic")
    res = ps.run("prompt", tmp_path)
    assert calls == [] and res.failure_class == "provider" and "stopping" in (res.error or "")


def test_the_workflow_resets_the_flag_for_a_new_run(monkeypatch):
    """The flag is per process: a new run (the workflow installs its SIGTERM handler) starts clean."""
    from tenderpack.ai import workflow as W
    HS.terminate_live()
    assert HS.stopping()
    src = Path(W.__file__).read_text(encoding="utf-8")
    i = src.index("prev_term = signal.signal(signal.SIGTERM, _on_sigterm)")
    assert "reset_stop()" in src[i - 400:i]              # right before the handler is installed
    HS.reset_stop()
    assert not HS.stopping()


def test_a_worker_asleep_in_a_backoff_wakes_at_the_stop_and_is_not_asked_again():
    """K.20 of the session-13 report: a worker asleep in a long backoff delayed the exit by up to 240 s. With the
    stop-aware wait it wakes at once and raises instead of asking again."""
    import threading
    import time as _t
    n = {"runs": 0}

    def run():
        n["runs"] += 1
        res = HS.SessionResult(run_id="r", addendum="ADD-03", provisions=[], started="now")
        res.exit_code, res.error = 1, "the host ended with an error (api_error: 500)"
        HS.classify(res)
        assert res.failure_class == "provider"
        return res
    pol = R.FailurePolicy(provider_backoff_s=60.0, host_retries=2)
    threading.Timer(0.3, HS.terminate_live).start()
    t0 = _t.monotonic()
    with pytest.raises(R.ProviderFailed) as ei:
        R.call_host(run, pol)                          # the real time.sleep path: the wait is STOP.wait
    assert _t.monotonic() - t0 < 5.0                     # woke at the stop, not after 60 s
    assert n["runs"] == 1 and "stopping" in ei.value.message


def test_the_folder_builder_never_ships_patch_backups():
    import importlib.util
    spec = importlib.util.spec_from_file_location("mif", Path(__file__).resolve().parents[1] / "scripts/make_interview_folder.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for name in ("requests.py.orig", "cli.py.rej", "views.py~", "a.swp", "x.bak"):
        assert mod.is_backup(name), name
    assert not mod.is_backup("requests.py") and not mod.is_backup("original.md")
    src = (Path(__file__).resolve().parents[1] / "scripts/make_interview_folder.py").read_text(encoding="utf-8")
    assert "is_backup(f)" in src                          # the walk uses it
