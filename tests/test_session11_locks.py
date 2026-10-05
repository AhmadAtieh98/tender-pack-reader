"""Session 11, E135 (found by the interrupted-run demonstration on blind-04): after a container restart, `resume` took
over the run lock of the dead process but every host session was refused by the addendum's AI staging lock still held
by that dead process, and the workflow recorded each refused session as a DONE batch with 0 items.

Two rules: (1) a staging lock whose process on this host is no longer running is taken over (as the run lock is), never
refused; (2) a session that was refused, or ended with an error and no answer, is never an empty answer: the request
layer raises, and the batch fails (asked again on resume)."""
from __future__ import annotations

import json
import os
import socket
import time

import pytest

from tenderpack.ai import budget as B
from tenderpack.ai import hostsession as HS
from tenderpack.ai import requests as R


def _dead_pid() -> int:
    pid = 2 ** 22 + 4321
    while B._pid_alive(pid):
        pid += 1
    return pid


def _write_lock(staging, addendum, pid, age_s=5.0):
    p = B.lock_path(staging, addendum)
    p.write_text(json.dumps({"addendum": addendum, "host": socket.gethostname(), "pid": pid, "route": "host",
                             "run_id": "old-run", "created": "x", "created_epoch": time.time() - age_s, "token": "t0"}))
    return p


def test_a_staging_lock_of_a_dead_process_is_taken_over(tmp_path):
    staging = tmp_path / "staging"
    staging.mkdir()
    _write_lock(staging, "ADD-03", _dead_pid())
    lock = B.acquire(staging, "ADD-03", {"route": "host", "run_id": "new-run", "pid": os.getpid()})
    assert lock.info.get("taken_over_from", {}).get("pid") == _dead_pid() or lock.info.get("taken_over_from")
    assert json.loads(B.lock_path(staging, "ADD-03").read_text())["run_id"] == "new-run"
    lock.release()


def test_a_staging_lock_of_a_live_process_is_still_refused(tmp_path):
    staging = tmp_path / "staging"
    staging.mkdir()
    _write_lock(staging, "ADD-03", os.getpid())                 # this test's own process: alive
    with pytest.raises(B.Refused, match="another orchestrator holds ADD-03"):
        B.acquire(staging, "ADD-03", {"route": "host", "run_id": "new-run", "pid": os.getpid()})


def test_an_old_lock_without_a_dead_process_is_still_refused_as_stale(tmp_path):
    staging = tmp_path / "staging"
    staging.mkdir()
    _write_lock(staging, "ADD-03", os.getpid(), age_s=200 * 60)     # live pid but older than stale_after_min
    with pytest.raises(B.Refused, match="STALE lock"):
        B.acquire(staging, "ADD-03", {"route": "host", "run_id": "new-run", "pid": os.getpid()}, stale_after_min=120)


def _res(**kw) -> HS.SessionResult:
    r = HS.SessionResult(run_id="r", addendum="ADD-03", provisions=[], started="2026-10-04T23:00:00")
    for k, v in kw.items():
        setattr(r, k, v)
    return r


def test_a_refused_session_is_classified_refused():
    r = _res(error="refused: another orchestrator holds ADD-03: STALE lock (its process 5474 is no longer running)")
    assert HS.classify(r) == "refused"


def test_call_host_raises_on_a_refused_session_instead_of_returning_it():
    r = _res(error="refused: another orchestrator holds ADD-03: STALE lock (its process 5474 is no longer running)")
    HS.classify(r)
    with pytest.raises(B.Refused):
        R.call_host(lambda: r, R.FailurePolicy(), sleep=lambda s: None)


def test_call_host_never_returns_an_errored_session_without_an_answer():
    r = _res(error="the host ended without a final message", final_text="")
    HS.classify(r)
    with pytest.raises((R.ProviderFailed, B.Refused)):
        R.call_host(lambda: r, R.FailurePolicy(host_retries=0), sleep=lambda s: None)


# --- resume: a batch recorded `done` although its host session ended with an error is asked again (E135's checkpoint)

def test_resume_reclassifies_a_done_batch_whose_session_was_refused():
    from tenderpack.ai import workflow as W
    batches = {
        "downstream-001": {"status": "done", "items": ["a", "b"], "host_session": {"error": None}},
        "downstream-003": {"status": "done", "items": [], "host_session": {"error": "refused: another orchestrator holds ADD-03"}},
        "downstream-004": {"status": "done", "items": [], "host_session": {"error": "the host CLI could not be started"}},
        "analysis-002": {"status": "skipped", "reason": "accounted for"},
    }
    changed = W.reclassify_errored_batches(batches)
    assert sorted(changed) == ["downstream-003", "downstream-004"]
    assert batches["downstream-003"]["status"] == "failed" and "refused" in batches["downstream-003"]["error"]
    assert batches["downstream-001"]["status"] == "done" and batches["analysis-002"]["status"] == "skipped"
