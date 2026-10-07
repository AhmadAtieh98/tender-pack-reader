"""Session 13 (implementer D, part 3 of the owner's message): speed without weaker checks.

    1. completed, validated responses survive interruptions: a host session that reached submit_proposals (its set
       staged and validated) is kept through a 429 or a SIGTERM after the submission and REUSED on resume after
       revalidation against the current evidence and state; a session killed before its submission is asked again;
       a reused set whose evidence changed is revalidated and, when it no longer holds, asked again with the reason;
       the step timer keeps a running step's elapsed time across a SIGTERM;
    2. no session for a batch whose provisions are all accounted for;
    3. batches planned by structure (an image region with its elements, a table with its rows and notes, a clause with
       its lettered items, the answers under one heading, provisions a reference links) within the token budget;
    4. answers collected as they arrive by the workers, taken by ONE writer in plan order: the result does not depend
       on the arrival order, and a worker does not idle while an earlier batch's answer is awaited;
    6. scripts/bench_workflow.py --from-run prints a run's per-step and per-session timing from its records.

Every model exchange here is RECORDED (cassettes, or tests/fixtures/ai_cassettes/fake_claude_s11.py standing in for
the host CLI: not a model). They show the mechanisms; they measure no speed-up of a real host."""
from __future__ import annotations

import copy
import json
import os
import random
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest
import yaml

from ai_fixture import CASSETTES, ROOT
from tenderpack.ai import batching
from tenderpack.ai import config as C
from tenderpack.ai import requests as R
from tenderpack.ai import workflow as W

quiet = lambda *a, **k: None  # noqa: E731
PDF = ROOT / "rehearsals/blind-02/input/ADD-03_Addendum_No_3.pdf"
FAKE = CASSETTES / "fake_claude_s11.py"
BENCH = ROOT / "scripts/bench_workflow.py"


def _bench():
    import importlib.util
    spec = importlib.util.spec_from_file_location("bench_workflow", BENCH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _host_cfg(tmp: Path, n: int = 1, name: str = "ai.yaml") -> Path:
    cfg = copy.deepcopy(C.load())
    cfg["host_session"] = {**cfg["host_session"], "claude_bin": str(FAKE), "timeout_s": 120}
    cfg["critic"] = {**cfg["critic"], "host": {**cfg["critic"]["host"], "claude_bin": str(FAKE)}}
    cfg["failures"]["rate_limit"]["seed"] = 7
    cfg["concurrency"]["max_parallel_sessions"] = n
    p = tmp / name
    p.write_text(yaml.safe_dump({k: v for k, v in cfg.items() if not k.startswith("_")}, sort_keys=False),
                 encoding="utf-8")
    return p


def _analysis_sessions(fake_dir: Path) -> list[dict]:
    f = fake_dir / "calls.jsonl"
    rows = [json.loads(x) for x in f.read_text().splitlines()] if f.exists() else []
    return [r for r in rows if r["kind"] == "tool" and "submit_proposals" in (r.get("allowed") or "")]


def _start_host(tmp: Path, evidence: Path, run_id: str, cfg: Path, stop_after="analysis"):
    return W.start("ADD-03", PDF, pack=ROOT / "config/pack.yaml", evidence=evidence, staging=tmp / "st",
                   worklog=tmp / "wl", ai_config=cfg, run_id=run_id, route="host", batch_size=8,
                   background_before=False, stop_after=stop_after, echo=quiet, sleep=lambda s: None)


@pytest.fixture
def fake(tmp_path, monkeypatch):
    d = tmp_path / "fake"
    d.mkdir()
    monkeypatch.setenv("FAKE_S11_DIR", str(d))
    return d


# ---------------------------------------------------------------------------------------------- 1. preserved answers

def test_a_session_that_submitted_and_then_hit_a_rate_limit_is_kept():
    """REGRESSION (blind-05 regression defect 2): two host sessions staged four proposal sets and then ended with a 429;
    the run discarded them (about 12 min) and asked the batches again after the reset. A session that reached
    submit_proposals is a completed answer whatever ended it afterwards: kept, the failure recorded, the shared gate
    still paused for the other workers."""
    from tenderpack.ai.hostsession import SessionResult
    res = SessionResult(run_id="r", addendum="ADD-03", provisions=["ADD-03:1.1"], started="t")
    res.failure_class, res.error, res.api_error_status = "rate_limit", "the host ended with an error (429)", 429
    res.submission = {"run_id": "ADD-03-host-x", "status": "partial", "staging": "/nowhere"}
    pol = R.FailurePolicy.from_cfg(C.load(), {})
    gate = R.RateGate()
    pol.gate = gate
    seen = []
    got = R.call_host(lambda: res, pol, sleep=lambda s: None, rng=random.Random(1), record=seen.append)
    assert got is res
    assert seen and seen[0]["class"] == "rate_limit" and "after the submission" in seen[0]["note"]
    assert gate.record()["pauses"] == 1


def _kill_after_submission(monkeypatch, which: int = 1, before: bool = False):
    """The orchestrator interrupted (as a SIGTERM does: KeyboardInterrupt in the run's thread) right after analysis
    session number `which` submitted (or, `before`, just before it started)."""
    from tenderpack.ai import hostsession as HS
    real = HS.HostSession.run_batch
    seen = {"n": 0}

    def run_batch(self, packet):
        if type(self) is HS.HostSession:
            seen["n"] += 1
            if seen["n"] == which:
                if before:
                    raise KeyboardInterrupt("SIGTERM before the session (simulated)")
                real(self, packet)
                raise KeyboardInterrupt("SIGTERM after the submission (simulated)")
        return real(self, packet)
    monkeypatch.setattr(HS.HostSession, "run_batch", run_batch)


def test_kill_after_submission_resume_reuses_the_staged_set(tmp_path, pack, fake, monkeypatch):
    cfg = _host_cfg(tmp_path)
    _kill_after_submission(monkeypatch)
    with pytest.raises(KeyboardInterrupt):
        _start_host(tmp_path, pack["out"], "k1", cfg)
    monkeypatch.undo()
    monkeypatch.setenv("FAKE_S11_DIR", str(fake))
    cp0 = W.load("k1", tmp_path / "st").data
    assert cp0["batches"]["analysis-001"]["status"] == "interrupted"
    asked_before = len(_analysis_sessions(fake))
    W.resume("k1", tmp_path / "st", stop_after="analysis", echo=quiet, sleep=lambda s: None)
    cp = W.load("k1", tmp_path / "st").data
    b = cp["batches"]["analysis-001"]
    assert b["status"] == "done", b
    sub = b.get("submission") or {}
    assert sub.get("reused") is True, b
    assert sub.get("staging") and (Path(sub["staging"]) / "proposals.yaml").is_file()
    assert sub.get("revalidated") and sub.get("set_status") and sub.get("statuses")       # the validation result
    n_batches = len(cp["batches"])
    assert len(_analysis_sessions(fake)) == n_batches, "the submitted batch was asked again"
    assert asked_before == 1
    assert any(e["event"] == "submission_reused" for e in cp["events"])


def test_kill_before_submission_is_asked_again(tmp_path, pack, fake, monkeypatch):
    cfg = _host_cfg(tmp_path)
    _kill_after_submission(monkeypatch, before=True)
    with pytest.raises(KeyboardInterrupt):
        _start_host(tmp_path, pack["out"], "k2", cfg)
    monkeypatch.undo()
    monkeypatch.setenv("FAKE_S11_DIR", str(fake))
    W.resume("k2", tmp_path / "st", stop_after="analysis", echo=quiet, sleep=lambda s: None)
    cp = W.load("k2", tmp_path / "st").data
    b = cp["batches"]["analysis-001"]
    assert b["status"] == "done" and not (b.get("submission") or {}).get("reused")
    assert len(_analysis_sessions(fake)) == len(cp["batches"])            # asked once, in the resumed segment


def test_a_reused_set_whose_evidence_changed_is_revalidated_and_asked_again_with_the_reason(tmp_path, pack, fake,
                                                                                             monkeypatch):
    cfg = _host_cfg(tmp_path)
    _kill_after_submission(monkeypatch)
    with pytest.raises(KeyboardInterrupt):
        _start_host(tmp_path, pack["out"], "k3", cfg)
    monkeypatch.undo()
    monkeypatch.setenv("FAKE_S11_DIR", str(fake))
    run_dir = tmp_path / "st" / "runs" / "k3"
    found = [p for p in sorted((run_dir / "candidate").rglob("assumptions.yaml")) if "before" not in p.parts]
    assert found, "the candidate's assumptions file (not the pre-addendum copy under candidate/before)"
    with open(found[0], "a", encoding="utf-8") as fh:              # the candidate's evidence changed between segments
        fh.write("\n# changed between the segments (test)\n")
    W.resume("k3", tmp_path / "st", stop_after="analysis", echo=quiet, sleep=lambda s: None)
    cp = W.load("k3", tmp_path / "st").data
    b = cp["batches"]["analysis-001"]
    assert b["status"] == "done"
    refused = b.get("reuse_refused") or []
    assert refused and "assumptions_sha256" in refused[-1]["reason"], b
    assert not (b.get("submission") or {}).get("reused")
    assert len(_analysis_sessions(fake)) == len(cp["batches"]) + 1        # asked again, with the reason recorded
    assert any(e["event"] == "submission_reuse_refused" for e in cp["events"])


DRIVER = """
import sys
from pathlib import Path
from tenderpack.ai import workflow as W
a = sys.argv[1:]
W.start("ADD-03", Path(a[0]), pack=Path(a[1]), evidence=Path(a[2]), staging=Path(a[3]), worklog=Path(a[4]),
        ai_config=Path(a[5]), run_id="sig", route="host", batch_size=8, background_before=False,
        stop_after="analysis", echo=lambda *x, **k: None)
"""


def test_sigterm_after_a_submission_keeps_the_step_time_and_the_answer(tmp_path, pack, fake):
    """REGRESSION (blind-05 regression defect 1): a SIGTERM during the analysis step left it "0.0 s running" (its
    elapsed time lost) and the submitted work of the session in flight was asked again. The stand-in CLI sends SIGTERM
    to the orchestrator right after its submission: the step is recorded `interrupted` with its seconds, the batch
    with its seconds, and the resume reuses the submission."""
    cfg = _host_cfg(tmp_path)
    (fake / "kill_parent_after_submit_n").write_text("1")
    p = subprocess.run([sys.executable, "-c", DRIVER, str(PDF), str(ROOT / "config/pack.yaml"), str(pack["out"]),
                        str(tmp_path / "st"), str(tmp_path / "wl"), str(cfg)], cwd=str(ROOT), capture_output=True,
                       text=True, timeout=600, env={**os.environ, "FAKE_S11_DIR": str(fake)})
    assert p.returncode != 0, p.stdout[-2000:] + p.stderr[-2000:]
    cp0 = W.load("sig", tmp_path / "st").data
    st = cp0["steps"]["analysis"]
    assert st["status"] == "interrupted" and st["seconds"] > 0, st
    assert cp0["batches"]["analysis-001"]["status"] == "interrupted"
    assert cp0["batches"]["analysis-001"]["seconds"] > 0
    W.resume("sig", tmp_path / "st", stop_after="analysis", echo=quiet, sleep=lambda s: None)
    cp = W.load("sig", tmp_path / "st").data
    assert (cp["batches"]["analysis-001"].get("submission") or {}).get("reused") is True
    assert cp["steps"]["analysis"]["seconds"] >= st["seconds"]
    assert len(_analysis_sessions(fake)) == len(cp["batches"])


# ---------------------------------------------------------------------------------------------- 2. no needless session

def test_no_session_starts_for_a_batch_whose_provisions_are_all_accounted_for(tmp_path, pack, fake, monkeypatch):
    """Provisions accounted for by an earlier batch (an op's `covers`, a reused set) never start a session, also with
    two sessions at once (nothing is asked ahead for such a batch)."""
    cfg = _host_cfg(tmp_path, n=2)
    real = W._take_analysis

    def take(ctx, bid, ps, todo):
        real(ctx, bid, ps, todo)
        if bid == "analysis-001":                                 # as if its ops covered every provision of 003
            for p in ctx.cp.batch("analysis-003")["provisions"]:
                if ctx.cp.provision(p)["status"] == "pending":
                    ctx.cp.set_provision(p, "proposed", accounted_by=["test"], answered_in=bid)
                    ctx.cp.set_provision(p, "validated", accounted=True, statuses={})
    monkeypatch.setattr(W, "_take_analysis", take)
    monkeypatch.setattr(W, "_prep_analysis_delay", 0.0, raising=False)
    _start_host(tmp_path, pack["out"], "acc", cfg)
    cp = W.load("acc", tmp_path / "st").data
    assert cp["batches"]["analysis-003"]["status"] == "skipped"
    assert len(_analysis_sessions(fake)) == len(cp["batches"]) - 1


# ---------------------------------------------------------------------------------------------- 3. grouping

def _synthetic():
    """A synthetic addendum: two cover lines, clause 2 with lettered items, an image region of 12 elements under its
    appendix heading, the English translation of its table (a table with rows and notes), the answers under one
    heading."""
    units = {}
    order = []

    def add(pid, heading, kind="clause", origin=None, text=""):
        order.append(pid)
        units[pid] = {"unit_id": pid, "heading": heading, "kind": kind, "origin": origin, "text": text}
    add("ADD-09:cover/para1", "", "paragraph")
    add("ADD-09:cover/para2", "ADDENDUM NO. 9", "paragraph")
    for x in ("2.1", "2.2", "2.2(a)", "2.2(b)", "2.3"):
        add(f"ADD-09:{x}", "2. WORKS")
    add("ADD-09:AppA/para1", "APPENDIX A - TABLE 4-2 (ARABIC)", "paragraph")
    for i in range(12):
        add(f"ADD-09:p3-image/el{i:02d}", "APPENDIX A - TABLE 4-2 (ARABIC)", "reading_block", "image_reading")
    add("ADD-09:AppB/para1", "APPENDIX B - ENGLISH TRANSLATION OF TABLE 4-2", "paragraph",
        text="The English translation of Table 4-2 follows.")
    for x in ("r-1", "r-2", "notes", "note(1)", "note(2)"):
        add(f"ADD-09:T4-2/{x}", "APPENDIX B - ENGLISH TRANSLATION OF TABLE 4-2", "table_row")
    for q in range(30, 34):
        add(f"ADD-09:Q{q}", "6. RESPONSES TO CLARIFICATION REQUESTS 30 TO 33", "table_row")
    return order, units


def test_the_image_region_of_a_synthetic_addendum_lands_in_one_batch_when_it_fits():
    """REGRESSION (blind-06: the 29 elements of one image region were spread over four batches of 8, each session
    reading the region's crops again). The count planner splits this synthetic addendum's 12-element region in two;
    planned by structure, the region is one batch when the token budget allows, beyond the batch size."""
    order, units = _synthetic()
    region = [p for p in order if ":p3-image/" in p]
    plan = batching.plan_structured(order, 8, units=units, fits=lambda ids: len(ids) <= 40)
    assert sorted(p for b in plan for p in b) == sorted(order) and len({p for b in plan for p in b}) == len(order)
    holding = [i for i, b in enumerate(plan) if set(region) & set(b)]
    assert len(holding) == 1 and set(region) <= set(plan[holding[0]]), plan      # 12 > size 8, kept whole
    clause = [p for p in order if p.startswith("ADD-09:2.")]
    assert sum(1 for b in plan if set(clause) & set(b)) == 1         # a clause with its lettered items
    table = [p for p in order if ":T4-2/" in p]
    tb = [i for i, b in enumerate(plan) if set(table) & set(b)]
    assert len(tb) == 1                                              # a table with its rows and notes
    assert "ADD-09:AppB/para1" in plan[tb[0]]                        # the translation that names it, beside it
    assert sum(1 for b in plan if {p for p in order if ":Q" in p} & set(b)) == 1    # the answers under one heading
    appa = next(i for i, b in enumerate(plan) if "ADD-09:AppA/para1" in b)
    assert appa <= holding[0] <= tb[0] <= appa + 2                   # linked structures next to each other
    assert all(len(b) <= 8 for i, b in enumerate(plan) if i != holding[0])   # links never make a batch larger
    assert plan == batching.plan_structured(list(order), 8, units=units, fits=lambda ids: len(ids) <= 40)
    # the count planner (before) split the region over two batches
    assert sum(1 for b in W.plan_batches(order, 8) if set(region) & set(b)) == 2


def test_a_group_that_does_not_fit_is_split_in_order_and_the_cover_links_nothing():
    order, units = _synthetic()
    plan = batching.plan_structured(order, 8, units=units, fits=lambda ids: len(ids) <= 10)
    flat = [p for b in plan for p in b]
    assert sorted(flat) == sorted(order) and len(flat) == len(order)
    assert all(len(b) <= 10 for b in plan)
    region = [p for p in flat if ":p3-image/" in p]
    assert region == [p for p in order if ":p3-image/" in p]          # split in document order
    assert sum(1 for b in plan if set(region) & set(b)) == 2
    table = [p for p in order if ":T4-2/" in p]
    assert sum(1 for b in plan if set(table) & set(b)) == 1          # the smaller structure still whole
    # no budget given: the count bounds a batch, as before
    plan2 = batching.plan_structured(order, 8, units=units)
    assert all(len(b) <= 8 for b in plan2) and sorted(p for b in plan2 for p in b) == sorted(order)
    # the cover's words (its summary of the addendum) link it to nothing
    u2 = {**units, "ADD-09:cover/para2": {**units["ADD-09:cover/para2"], "text": "This Addendum amends Table 4-2."}}
    assert not [x for x in batching.structure_links(order, u2) if "cover" in x[:2]]


# ---------------------------------------------------------------------------------------------- 4. one writer

@pytest.fixture(scope="module")
def arrivals(tmp_path_factory, pack):
    """The same recorded run (scripts/bench_workflow.py simulate: blind-02's ADD-03 cassette, simulated latency) one at
    a time, two at a time with the FIRST batch held until two later batches have answered (later answers arrive
    first, deterministically: a hold, not a race against the machine's speed; a run that never asks the third batch
    while the first is awaited is released by the hold's timeout and fails the assertions), and three at a time with
    another seeded order."""
    bench = _bench()
    d = tmp_path_factory.mktemp("s13-arrivals")
    out = {}
    for key, n, seed, hold in (("one", 1, None, 0), ("two", 2, 11, 2), ("three", 3, 29, 0)):
        out[key] = bench.simulate(n, evidence=pack["out"], workdir=d / key, seed=seed, scale=0.008,
                                  stop_after="validation", hold_first=hold)
    return out


def test_the_result_does_not_depend_on_the_arrival_order(arrivals):
    one = arrivals["one"]
    for k in ("two", "three"):
        assert arrivals[k]["summary"] == one["summary"], k
        assert arrivals[k]["status"] == one["status"]
    order = arrivals["two"]["arrival_order"]
    assert order and order[-1] == "analysis-001" and len(order) == 3, order    # the first batch answered last


def test_no_worker_idles_while_an_earlier_answer_is_awaited(arrivals):
    """The first batch is held until two later batches have answered. The second batch's worker takes the third batch
    while the run's thread still waits for the first (a bounded look-ahead), instead of holding a finished answer until
    the first is taken; also when the second answer came back while the run's thread was still building the first
    batch's packet (Prefetch.take refills before it waits)."""
    c = arrivals["two"]["concurrency"]["analysis"]
    assert c["dispatched_before_first_take"] == 3, c                   # every recorded batch asked before the first take
    assert c["max_running"] <= 2
    assert c["busy_s"] > 0 and c["taken"] <= c["dispatched"]


# ---------------------------------------------------------------------------------------------- 6. timing from data

def test_bench_from_run_prints_the_steps_and_batches_of_a_recorded_run():
    run = ROOT / "rehearsals/blind-06"
    p = subprocess.run([sys.executable, str(BENCH), "--from-run", str(run)], cwd=str(ROOT), capture_output=True,
                       text=True, timeout=120)
    assert p.returncode == 0, p.stderr[-2000:]
    out = p.stdout
    assert "analysis" in out and "2170.6" in out and "downstream" in out
    assert "analysis-001" in out and "steps' sum" in out
