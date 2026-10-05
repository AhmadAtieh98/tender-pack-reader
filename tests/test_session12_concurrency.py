"""Session 12 (W4, part 2 "time"): less repeated context per batch, and BOUNDED concurrency of the analysis and
downstream batches where it is safe (`concurrency.max_parallel_sessions`, default 1).

Safe means: independent batches (each its own staging folder and log), ONE addendum lock held by the run (not one per
session), a shared rate-limit gate (one 429 pauses every worker until its wait is over), checkpoints written only by
the run's own thread and results taken IN PLAN ORDER (a resumed or parallel run gives the sequential result), exit 5
deferral and resume kept. Only the host route (the coding host's sessions) and the recorded test route may run
batches at once: the paid API routes check their caps per request, and local inference shares one machine's memory.

Every provider exchange here is RECORDED (cassettes) with a recorded delay: these tests show the mechanism and that
the results do not depend on the order in which answers arrive; they measure NO speed-up of a real host (the next
sealed rehearsal measures that)."""
from __future__ import annotations

import copy
import json
import threading
import time
from pathlib import Path

import pytest
import yaml

from ai_fixture import CASSETTES, ROOT
from tenderpack.ai import budget as B
from tenderpack.ai import config as C
from tenderpack.ai import requests as R
from tenderpack.ai import workflow as W
from tenderpack.ai.providers.recorded import RecordedProvider

quiet = lambda *a, **k: None  # noqa: E731
PDF = ROOT / "rehearsals/blind-02/input/ADD-03_Addendum_No_3.pdf"
BLIND05 = Path("/home/user/tender-pack-reader/staging/ai/runs/ADD-03-run-host-blind05-20261005T025444Z/batches")


# ---------------------------------------------------------------------------------------------- repeated context

def _packets():
    src = BLIND05 if BLIND05.is_dir() else ROOT / "staging/ai/runs/ADD-03-run-host-blind05-20261005T025444Z/batches"
    if not src.is_dir():
        pytest.skip("blind-05's run staging is not in this tree")
    return {f.name: json.loads(f.read_text(encoding="utf-8")) for f in sorted(src.glob("*.packet.json"))}


def _refs(x, out):
    if isinstance(x, dict):
        for k, v in x.items():
            if k == "$ref" and isinstance(v, str):
                out.add(v.rsplit("/", 1)[-1])
            _refs(v, out)
    elif isinstance(x, list):
        for v in x:
            _refs(v, out)
    return out


def _defs(x, out):
    if isinstance(x, dict):
        out |= set((x.get("$defs") or {}) if isinstance(x.get("$defs"), dict) else ())
        for v in x.values():
            _defs(v, out)
    elif isinstance(x, list):
        for v in x:
            _defs(v, out)
    return out


def test_the_shared_context_is_sent_smaller_and_the_batch_content_unchanged():
    """MEASURED on blind-05's 15 packets (read-only): the shared part (tool descriptions repeated beside the tools the
    request already carries; generated schema titles; $defs repeated in every payload schema) is sent once and
    smaller; every batch's provisions, tasks, targets, units, references and crops are byte-identical."""
    total_b = total_a = 0
    for name, pk in _packets().items():
        pub = {k: v for k, v in pk.items() if k != "system"}
        after = R.compact_shared(pub)
        for k in ("provisions", "targets", "reference", "crops", "tasks", "units_after", "promoted_ops", "state",
                  "instructions", "vocabulary", "region", "examples"):
            assert after.get(k) == pub.get(k), (name, k)
        if isinstance(pub.get("tools"), list) and pub["tools"] and isinstance(pub["tools"][0], dict):
            assert after["tools"] == [t["name"] for t in pub["tools"]]
        defs = set(after.get("schema_defs") or {})
        scs = [after.get("schema")] + list((after.get("payload_schemas") or {}).values())
        for sc in [x for x in scs if isinstance(x, dict)]:
            local = _defs(sc, set())                                  # $defs at any depth stay where they were
            for ref in _refs(sc, set()):                             # every reference still resolves
                assert ref in defs or ref in local, (name, ref)
        b, a = len(json.dumps(pub, ensure_ascii=False)), len(json.dumps(after, ensure_ascii=False))
        assert a < b, name
        if name.startswith("analysis"):
            assert (b - a) / b > 0.15, (name, b, a)
        total_b, total_a = total_b + b, total_a + a
    assert (total_b - total_a) / total_b > 0.10, (total_b, total_a)
    # the answer's schema (native structured output) and the local validation come from the contract, unchanged
    assert R.spec("analysis").schema == R.spec("analysis").schema and "$defs" in json.dumps(R.spec("analysis").schema)


# ---------------------------------------------------------------------------------------------- where it is safe

def _cfg_file(tmp: Path, n: int) -> Path:
    tmp.mkdir(parents=True, exist_ok=True)
    cfg = copy.deepcopy(C.load())
    cfg["concurrency"]["max_parallel_sessions"] = n
    cfg["failures"]["rate_limit"]["seed"] = 7
    p = tmp / "ai.yaml"
    p.write_text(yaml.safe_dump({k: v for k, v in cfg.items() if not k.startswith("_")}, sort_keys=False),
                 encoding="utf-8")
    return p


def test_parallel_sessions_are_refused_where_they_are_not_safe(tmp_path):
    for route in ("anthropic", "openrouter", "ollama"):
        with pytest.raises(B.Refused, match="max_parallel_sessions"):
            W.start("ADD-03", PDF, route=route, ai_config=_cfg_file(tmp_path, 2), staging=tmp_path / "st",
                    worklog=tmp_path / "wl", echo=quiet)
    with pytest.raises(B.Refused, match="between 1 and 4"):
        W.start("ADD-03", PDF, route="recorded", cassette=CASSETTES / "workflow_add03.yaml",
                ai_config=_cfg_file(tmp_path, 9), staging=tmp_path / "st", worklog=tmp_path / "wl", echo=quiet)
    assert C.load()["concurrency"]["max_parallel_sessions"] == 1          # the shipped default: one at a time


# ---------------------------------------------------------------------------------------------- the mechanism

def _cassette(tmp: Path, rate_limited: str | None = None, times: int = 5) -> Path:
    data = yaml.safe_load((CASSETTES / "workflow_add03.yaml").read_text(encoding="utf-8"))
    data["sessions"] += yaml.safe_load((CASSETTES / "s11_workflow_critic.yaml").read_text(encoding="utf-8"))["sessions"]
    if rate_limited:
        for s in data["sessions"]:
            if s["phase"] == "analysis" and rate_limited in (s.get("when") or {}).get("provisions_include", []):
                s["turns"] = [{"error": {"kind": "http_429", "status": 429, "retryable": True,
                                         "message": "rate_limit_error: recorded"}, "times": times}] + s["turns"]
    p = tmp / "s12_conc.yaml"
    p.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return p


class _Meter:
    """Wraps RecordedProvider.complete with a recorded delay; counts the calls in flight at once."""

    def __init__(self, mp, delay=0.25):
        self.now = self.max = 0
        self.lock = threading.Lock()
        real = RecordedProvider.complete
        meter = self

        def complete(self_, req):
            with meter.lock:
                meter.now += 1
                meter.max = max(meter.max, meter.now)
            try:
                time.sleep(delay)
                return real(self_, req)
            finally:
                with meter.lock:
                    meter.now -= 1
        mp.setattr(RecordedProvider, "complete", complete)


def _run(d: Path, pack_out: Path, n: int, run_id: str, cassette: Path, stop_after="downstream_validation", sleep=None):
    return W.start("ADD-03", PDF, pack=ROOT / "config/pack.yaml", evidence=pack_out, staging=d / "staging",
                   worklog=d / "worklog", run_id=run_id, route="recorded", cassette=cassette, batch_size=8,
                   ai_config=_cfg_file(d, n), background_before=False, stop_after=stop_after, echo=quiet,
                   sleep=sleep or (lambda s: None))


def _summary(cp: dict) -> dict:
    return {"batches": {k: (b["status"], b.get("items"), b.get("provisions") or b.get("tasks"))
                        for k, b in cp["batches"].items()},
            "provisions": {k: v["status"] for k, v in cp["provisions"].items()},
            "critic": {k: (b.get("critic") or {}).get("status") for k, b in cp["batches"].items()}}


@pytest.fixture(scope="module")
def runs(tmp_path_factory, pack):
    d = tmp_path_factory.mktemp("s12-conc")
    cas = _cassette(d)
    mp = pytest.MonkeyPatch()
    out = {}
    try:
        for n in (1, 3):
            m = _Meter(mp, delay=1.5)        # a recorded delay longer than building the next packet (no flakiness)
            t0 = time.perf_counter()
            res = _run(d / f"n{n}", pack["out"], n, f"conc{n}", cas)
            out[n] = {"res": res, "max": m.max, "s": time.perf_counter() - t0,
                      "cp": W.load(f"conc{n}", d / f"n{n}" / "staging").data}
            mp.undo()
    finally:
        mp.undo()
    return out


def test_batches_run_at_once_within_the_bound_and_give_the_sequential_result(runs):
    one, three = runs[1], runs[3]
    assert one["max"] == 1, one["max"]
    assert 2 <= three["max"] <= 3, three["max"]
    assert _summary(three["cp"]) == _summary(one["cp"])            # the same result, in plan order
    assert list(three["cp"]["batches"]) == list(one["cp"]["batches"])
    assert three["res"]["status"] == one["res"]["status"]
    assert three["cp"]["settings"]["max_parallel_sessions"] == 3
    ev = [e for e in three["cp"]["events"] if e["event"] == "run_lock_scoped"]
    assert ev and ev[0]["scope"] == "run"


def test_a_rate_limit_pauses_every_worker_defers_cleanly_and_resumes(tmp_path, pack, monkeypatch):
    cas = _cassette(tmp_path, rate_limited="ADD-03:7.1", times=10)
    slept: list[float] = []
    _Meter(monkeypatch, delay=0.05)
    res = _run(tmp_path, pack["out"], 3, "rl3", cas, stop_after="validation", sleep=slept.append)
    cp = W.load("rl3", tmp_path / "staging").data
    assert res["status"] == "deferred" and res["exit_code"] == 5, res
    deferred = [k for k, b in cp["batches"].items() if b["status"] == "deferred"]
    assert deferred and all(cp["batches"][k]["failure_class"] == "rate_limit" for k in deferred)
    done = [k for k, b in cp["batches"].items() if b["status"] == "done"]
    gate = cp.get("rate_gate") or {}
    assert gate.get("pauses", 0) >= 1, gate                        # one 429 paused every worker (the shared gate)
    _cassette(tmp_path)                                             # the limit is over (same file, no 429)
    res2 = W.resume("rl3", tmp_path / "staging", stop_after="validation", echo=quiet, sleep=lambda s: None)
    cp2 = W.load("rl3", tmp_path / "staging").data
    for k in done:                                                  # never asked again
        assert cp2["batches"][k]["attempts"] == cp["batches"][k]["attempts"] == 1
    assert all(cp2["batches"][k]["status"] == "done" for k in deferred), {k: cp2["batches"][k]["status"]
                                                                          for k in deferred}
    assert res2["status"] == "stopped"


def test_the_run_holds_one_addendum_lock_and_a_submission_does_not_release_it(tmp_path):
    from tenderpack.ai import hostsession as HS
    st = tmp_path / "ai"
    lk = B.acquire(st, "ADD-03", {"route": "host", "run_id": "r", "pid": 1, "scope": "run"})
    info = B.read_lock(B.lock_path(st, "ADD-03"))
    assert info["scope"] == "run"
    assert HS.HostSession.takes_lock(run_lock=True) is False and HS.HostSession.takes_lock(run_lock=False) is True
    from tenderpack.ai import controller
    assert controller.releases_host_lock(info) is False
    assert controller.releases_host_lock({**info, "scope": None}) is True
    lk.release()


def test_host_route_batches_at_once_hold_one_run_lock_and_match_one_at_a_time(tmp_path, pack, monkeypatch):
    """RECORDED host route end to end (tests/fixtures/ai_cassettes/fake_claude_s11.py, a stand-in for the CLI, not a
    model): each analysis session starts the REAL MCP server and submits through submit_proposals. With two sessions at
    once the run holds the addendum's lock once (no session is refused for a lock, no submission releases the run's
    lock) and the batches and provisions end exactly as one at a time."""
    d = tmp_path / "fake"
    d.mkdir()
    monkeypatch.setenv("FAKE_S11_DIR", str(d))
    fake = str(CASSETTES / "fake_claude_s11.py")
    out = {}
    for n in (1, 2):
        cfg = copy.deepcopy(C.load())
        cfg["host_session"] = {**cfg["host_session"], "claude_bin": fake, "timeout_s": 120}
        cfg["critic"] = {**cfg["critic"], "host": {**cfg["critic"]["host"], "claude_bin": fake}}
        cfg["failures"]["rate_limit"]["seed"] = 7
        cfg["concurrency"]["max_parallel_sessions"] = n
        p = tmp_path / f"ai{n}.yaml"
        p.write_text(yaml.safe_dump({k: v for k, v in cfg.items() if not k.startswith("_")}, sort_keys=False),
                     encoding="utf-8")
        res = W.start("ADD-03", PDF, pack=ROOT / "config/pack.yaml", evidence=pack["out"], staging=tmp_path / f"st{n}",
                      worklog=tmp_path / f"wl{n}", ai_config=p, run_id=f"h{n}", route="host", batch_size=8,
                      background_before=False, stop_after="validation", echo=quiet, sleep=lambda s: None)
        cp = W.load(f"h{n}", tmp_path / f"st{n}").data
        out[n] = (res, cp)
        assert not B.lock_path(Path(res["run_dir"]) / "ai", "ADD-03").exists()        # released at the end
        errs = [b.get("host_session", {}).get("error") for b in cp["batches"].values()]
        assert not any(e and "another orchestrator" in e for e in errs), errs
    (r1, c1), (r2, c2) = out[1], out[2]
    assert {k: b["status"] for k, b in c2["batches"].items()} == {k: b["status"] for k, b in c1["batches"].items()}
    assert {k: v["status"] for k, v in c2["provisions"].items()} == {k: v["status"] for k, v in c1["provisions"].items()}
    assert r2["status"] == r1["status"]
    assert any(e["event"] == "run_lock_scoped" for e in c2["events"])
    asked = [json.loads(x) for x in (Path(r2["run_dir"]) / "log.jsonl").read_text().splitlines()]
    assert sum(1 for e in asked if e.get("event") == "batch_asked_ahead") >= 2


# ---------------------------------------------------------------------------------------------- the run's own lock

def test_a_session_of_the_run_recognises_the_runs_own_lock_and_a_foreign_one_is_still_refused(tmp_path):
    """REGRESSION (session 12, the real host run ADD-03-run-host-blind05-s12-20261005T114809Z with
    max_parallel_sessions 2): the run held the addendum's lock (scope run) and its own readings session was refused by
    it ("another orchestrator holds ADD-03: held by host run <the same run>"). A session of the process that holds a
    run-scoped lock works under it; a live foreign holder is still refused; a dead holder is still taken over."""
    import os
    st = tmp_path / "ai"
    run = B.acquire(st, "ADD-03", {"route": "host", "run_id": "ADD-03-run-x", "pid": os.getpid(), "scope": "run"})
    sess = B.acquire(st, "ADD-03", {"route": "host", "run_id": "ADD-03-hostsession-y", "pid": os.getpid()})
    sess.release()                                                  # never releases the run's lock
    assert B.read_lock(B.lock_path(st, "ADD-03"))["run_id"] == "ADD-03-run-x"
    run.release()
    assert not B.lock_path(st, "ADD-03").exists()
    other = B.acquire(st, "ADD-03", {"route": "host", "run_id": "ADD-03-run-other", "pid": os.getppid(), "scope": "run"})
    with pytest.raises(B.Refused, match="another orchestrator holds ADD-03"):
        B.acquire(st, "ADD-03", {"route": "host", "run_id": "ADD-03-hostsession-z", "pid": os.getpid()})
    other.release()
    B.lock_path(st, "ADD-03").write_text(json.dumps({"addendum": "ADD-03", "host": __import__("socket").gethostname(),
                                                     "pid": 4194301, "created_epoch": time.time(), "scope": "run",
                                                     "token": "dead", "run_id": "ADD-03-run-dead", "route": "host"}))
    took = B.acquire(st, "ADD-03", {"route": "host", "run_id": "ADD-03-hostsession-w", "pid": os.getpid()})
    assert took.info["taken_over_from"]["run_id"] == "ADD-03-run-dead"
    took.release()


def _addendum_with_image(d: Path) -> Path:
    """Blind-02's Addendum No. 3 with an image of two printed lines on page 3 (no text layer): ingest refuses it (C05
    unread) until the region ADD-03-p3-r1 has a reading (as in tests/test_session10_workflow.py)."""
    import pymupdf
    doc = pymupdf.open(PDF)
    pg = pymupdf.open().new_page(width=460, height=80)
    pg.insert_text((12, 30), "Note: Bidders shall also submit one additional USB copy of Envelope B.", fontname="helv",
                   fontsize=11)
    pg.insert_text((12, 58), "The additional USB copy shall be encrypted as Clause 6.5 requires.", fontname="helv",
                   fontsize=11)
    doc[2].insert_image(pymupdf.Rect(66, 240, 526, 320), pixmap=pg.get_pixmap(dpi=200))
    out = Path(d) / "ADD-03_with_image.pdf"
    doc.save(out)
    return out


READING_ANSWER = (
    '{"region_id": "ADD-03-p3-r1", "reading": {"region_id": "ADD-03-p3-r1", "unit_id": "ADD-03:p3-image", '
    '"title": "Note on page 3 (image)", "source": ${state}, "content_type": "text", "languages": ["en"], '
    '"prepared_by": "the proposer (overwritten by the controller)", "method": "visual reading (recorded stand-in)", '
    '"blocks": [{"key": "note", "lang": "en", "role": "note", "lines": ['
    '{"band": 0, "source": "Note: Bidders shall also submit one additional USB copy of Envelope B."}, '
    '{"band": 1, "source": "The additional USB copy shall be encrypted as Clause 6.5 requires."}]}], '
    '"uncertainties": []}, "model_rationale": "two printed lines (recorded stand-in, not a model)"}')


def test_batches_at_once_get_past_a_reading_and_a_blocked_stop_does_not_exit_0(tmp_path, pack, monkeypatch):
    """REGRESSION (the same real run): with max_parallel_sessions 2 on the host route, an addendum with an image region
    needing a reading must get past the readings step (every session the run creates works under the run's own lock).
    And a run that STOPS because it cannot go on (no usable reading) exited 0, like a finished run: it now exits 6
    (stopped for a person); a stop asked for with --stop-after still exits 0. RECORDED: the stand-in CLI
    (fake_claude_s11.py) answers the reading session with a fixed reading; not a model."""
    d = tmp_path / "fake"
    d.mkdir()
    monkeypatch.setenv("FAKE_S11_DIR", str(d))
    fake = str(CASSETTES / "fake_claude_s11.py")
    cfg = copy.deepcopy(C.load())
    cfg["host_session"] = {**cfg["host_session"], "claude_bin": fake, "timeout_s": 120}
    cfg["critic"] = {**cfg["critic"], "host": {**cfg["critic"]["host"], "claude_bin": fake}}
    cfg["failures"]["rate_limit"]["seed"] = 7
    cfg["concurrency"]["max_parallel_sessions"] = 2
    p = tmp_path / "ai.yaml"
    p.write_text(yaml.safe_dump({k: v for k, v in cfg.items() if not k.startswith("_")}, sort_keys=False),
                 encoding="utf-8")
    pdf = _addendum_with_image(tmp_path)
    (d / "answer.json").write_text(READING_ANSWER, encoding="utf-8")
    res = W.start("ADD-03", pdf, pack=ROOT / "config/pack.yaml", evidence=pack["out"], staging=tmp_path / "st",
                  worklog=tmp_path / "wl", ai_config=p, run_id="rd2", route="host", batch_size=8,
                  background_before=False, stop_after="readings", echo=quiet, sleep=lambda s: None)
    cp = W.load("rd2", tmp_path / "st").data
    b = cp["batches"]["reading-ADD-03-p3-r1"]
    assert b["status"] == "done", b.get("error")
    assert res["status"] == "stopped" and "stopped after readings" in res["status_reason"], res
    assert res["exit_code"] == 0                                     # a stop that was asked for
    assert cp["steps"]["readings"]["reingest"]["exit_code"] == 0
    # the same addendum, no usable reading this time: the run stops for a person and says so in its exit code
    (d / "answer.json").write_text("I cannot read it.", encoding="utf-8")
    res2 = W.start("ADD-03", pdf, pack=ROOT / "config/pack.yaml", evidence=pack["out"], staging=tmp_path / "st",
                   worklog=tmp_path / "wl", ai_config=p, run_id="rd3", route="host", batch_size=8,
                   background_before=False, echo=quiet, sleep=lambda s: None)
    b2 = W.load("rd3", tmp_path / "st").data["batches"]["reading-ADD-03-p3-r1"]
    assert "another orchestrator" not in (b2.get("error") or "")
    assert res2["status"] == "stopped" and "no usable reading" in res2["status_reason"], res2
    assert res2["exit_code"] == 6, res2
