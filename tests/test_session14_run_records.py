"""Session 14 (W2; the blind-07 scorer's defects 15 and 18, rehearsals/blind-07/COMPARISON.md §6 and §8; report §9 L29).

Reproduced on the frozen run's own checkpoint (rehearsals/blind-07/checkpoint.json, copied into tmp; never changed):
  18  the review packet's usage line said "0 call(s), 0 input / 0 output tokens" although 10 host sessions and 6 critic
      requests ran: the host's own usage per session (what scripts/bench_workflow.py reads from the session records)
      was not carried into the run record. Unknown usage is not zero.
  15  the `concurrency` record covered only the last drive; `interventions` omitted the sessions the person's stop
      killed, the sessions whose answers were reused, and the person's stop and resume, so the packet's "Manual
      interventions" section listed none.
The session records below are this test's data (synthetic: two host sessions, one with usage and one killed without)."""
from __future__ import annotations

import json
import shutil
from concurrent.futures import Future
from pathlib import Path
from types import SimpleNamespace

import pytest

from tenderpack.ai import workflow as W
from tenderpack.ai.checkpoint import STEPS, Checkpoint

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "rehearsals/blind-07/checkpoint.json"


@pytest.fixture()
def frozen(tmp_path):
    run = tmp_path / "staging/ai/runs" / "b07"
    run.mkdir(parents=True)
    shutil.copy(FROZEN, run / "checkpoint.json")
    cp = Checkpoint.load(run / "checkpoint.json")
    cp.data["candidate"] = {"dir": str(run / "candidate")}          # the frozen copy's own folder (no sessions)
    return cp


def _session(run: Path, sid: str, usage, provisions=("ADD-03:2.1",), error=None):
    d = run / "ai" / sid
    d.mkdir(parents=True)
    (d / "session.json").write_text(json.dumps({"run_id": sid, "provisions": list(provisions), "elapsed_s": 12.0,
                                                "usage": usage, "error": error}), encoding="utf-8")


def test_the_frozen_runs_usage_line_never_says_zero_for_sessions_that_ran(frozen):
    text = "\n".join(W.usage_lines(frozen))
    assert "0 call(s), 0 input / 0 output tokens" not in text, text
    assert "unknown" in text and "host session" in text, text


def test_the_hosts_own_usage_per_session_is_carried_and_an_unknown_one_said_so(frozen):
    run = frozen.path.parent
    _session(run, "ADD-03-hostsession-20261006T202104Z-b683", {"input_tokens": 120, "cache_creation_input_tokens": 4000,
                                                               "cache_read_input_tokens": 90000, "output_tokens": 5100})
    _session(run, "ADD-03-hostsession-20261006T201953Z-ad30", None, error="killed by the stop")
    hu = W.host_usage(run, frozen.data)
    assert hu["known"] == 1 and hu["unknown"] == 1 and hu["totals"]["output_tokens"] == 5100, hu
    by = {x["session"]: x for x in hu["sessions"]}
    assert by["ADD-03-hostsession-20261006T202104Z-b683"]["batch"] == "analysis-003"      # from the batch record
    frozen.data["host_usage"] = hu
    text = "\n".join(W.usage_lines(frozen))
    assert "output 5100 tokens" in text and "**unknown** for 1 session(s)" in text and "201953Z-ad30" in text, text


def test_the_person_s_stop_and_resume_and_the_reused_answers_are_listed(frozen):
    text = "\n".join(W.intervention_lines(frozen))
    person = text.split("### ")[0]
    assert "stop (the person's action)" in person and "20:20:32" in person and "SIGTERM" in person, text
    assert "resume (the person's action)" in person and "20:20:41" in person, text
    assert text.count("submission reused") == 3, text
    assert "Manual interventions" in text and "\n- none" not in person, text


def test_a_reused_answer_says_whether_it_was_made_before_the_stop_or_after_the_resume(frozen):
    assert W._made_when(frozen.data, "2026-10-06T20:19:48Z").startswith("made before the interruption")
    assert W._made_when(frozen.data, "2026-10-06T20:24:15Z") == "made after the resume at 2026-10-06T20:20:41Z"


def _fake_ctx(batches):
    cp = SimpleNamespace(data={"batches": batches, "settings": {}}, event=lambda *a, **k: None)
    return SimpleNamespace(cp=cp, log=SimpleNamespace(event=lambda *a, **k: None))


def _done():
    f = Future()
    f.set_result(("ok", None))
    return f


def test_every_drive_s_concurrency_is_kept():
    ctx = _fake_ctx({"analysis-001": {"status": "done", "phase": "analysis"}})
    for n in (1, 2):
        pf = W.Prefetch(ctx, 2)
        pf.meter["analysis"] = dict(pf._m("analysis"), dispatched=n + 2, taken=n)
        pf.close(interrupted=(n == 1))
    drives = ctx.cp.data.get("concurrency_drives") or []
    assert [d["segment"] for d in drives] == [1, 2] and drives[0]["interrupted"] and not drives[1]["interrupted"]
    assert [d["phases"]["analysis"]["dispatched"] for d in drives] == [3, 4]
    assert ctx.cp.data["concurrency"]["analysis"]["dispatched"] == 4          # the last drive, as before


def test_a_stop_records_the_person_s_action_and_the_sessions_it_cut(tmp_path, monkeypatch):
    staging = tmp_path / "staging"
    run = staging / "runs" / "r-stop"
    cp = Checkpoint.new(run / "checkpoint.json", run_id="r-stop", addendum="ADD-03",
                        settings={"route": "recorded", "worklog": str(tmp_path / "wl"), "max_parallel_sessions": 1})
    for s in STEPS[1:]:
        cp.step(s)["status"] = "done"
    cp.data["batches"]["analysis-001"] = {"phase": "analysis", "status": "pending"}

    def stop(ctx, st):
        ctx.cp.batch("analysis-001")["status"] = "running"
        raise W.Terminated()
    monkeypatch.setitem(W.STEP_FUNCS, "ingest", stop)
    with pytest.raises(KeyboardInterrupt):
        W._drive(cp, None, lambda *a, **k: None, lambda s: None)
    kinds = [(x["kind"], x.get("batch")) for x in cp.data["interventions"]]
    assert ("stop (the person's action)", None) in kinds, kinds
    assert ("host session stopped by the person's stop", "analysis-001") in kinds, kinds
    stop_rec = next(x for x in cp.data["interventions"] if x["kind"].startswith("stop"))
    assert "SIGTERM" in stop_rec["note"] and stop_rec["ts"]
    monkeypatch.setitem(W.STEP_FUNCS, "ingest", lambda ctx, st: None)
    W.resume("r-stop", staging, echo=lambda *a, **k: None, sleep=lambda s: None)
    cp2 = W.load("r-stop", staging)
    assert any(x["kind"] == "resume (the person's action)" for x in cp2.data["interventions"]), cp2.data["interventions"]
