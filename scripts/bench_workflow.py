#!/usr/bin/env python3
"""Timing of the AI workflow from data (session 13, implementer D).

    python scripts/bench_workflow.py --from-run RUN_ID_OR_DIR [--staging staging/ai] [--json]
        a run's per-step, per-batch and per-session timing from its checkpoint, run log, host session records
        (<run>/ai/*/session.json) and MCP server logs: steps' sum, wall clock and segments, sessions started, context
        tokens sent (the request accounting's estimate per batch, and the host's own usage per session), the
        per-session overhead (process start to the MCP server, MCP server to the first tool call, submission to the
        session's end) and what concurrency did. Reads only.

    python scripts/bench_workflow.py --simulate [--parallel 1,2,3] [--scale 0.004] [--seed 7] [--rate-limit]
                                     [--stop-after validation] [--evidence BUILD] [--workdir DIR]
        the SAME recorded run (blind rehearsal 02's ADD-03 cassette, tests/fixtures/ai_cassettes, with --fill generic
        analysis sessions so that every planned batch takes a session's time) at each max_parallel_sessions, with a
        SIMULATED latency per recorded session (from blind-06's measured host sessions: a fixed part and a time per
        provision, scaled by --scale; the order per seed; see _Latency). Reports wall time, per-step time, sessions, context tokens, the workers'
        idle slot time, the arrival order and, with --rate-limit, a recorded 429 (every worker paused; the run defers,
        exit 5, and the resume asks only the deferred batches). It measures the MECHANISM, not a real host: the sealed
        run on the host route is the benchmark.

Nothing here writes outside --workdir (the simulation) or anything at all (--from-run)."""
from __future__ import annotations

import argparse
import contextlib
import copy
import datetime as dt
import json
import random
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).absolute().parents[1]          # not resolved: a copy of the tree benchmarks its own code
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# blind-06's host sessions (seconds; rehearsals/blind-06, the run's ai/*/session.json): analysis and downstream
BLIND06_ANALYSIS_S = [491.5, 207.8, 349.7, 464.3, 181.9, 358.6, 312.2, 381.5, 187.6, 349.1]
BLIND06_DOWNSTREAM_S = [274.0, 397.4, 230.0, 435.5]
BLIND06_CRITIC_S = 47.2 / 14


# ---------------------------------------------------------------------------------------------- --from-run

def _ts(s: str | None):
    try:
        return dt.datetime.strptime(str(s)[:19], "%Y-%m-%dT%H:%M:%S")
    except (TypeError, ValueError):
        return None


def _jsonl(p: Path) -> list[dict]:
    out = []
    try:
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except ValueError:
                    pass
    except OSError:
        pass
    return out


def _run_dir(run: str, staging: str | None) -> Path:
    p = Path(run)
    if (p / "checkpoint.json").is_file():
        return p
    base = Path(staging) if staging else ROOT / "staging/ai"
    q = base / "runs" / run
    if (q / "checkpoint.json").is_file():
        return q
    raise SystemExit(f"no checkpoint for {run} (looked in {p} and {q})")


def _session_dirs(cp: dict, run_dir: Path) -> list[Path]:
    """The host session folders of the run: <run>/ai/*/session.json, or the run's own staging folder named by the
    checkpoint when the folder given is a copy (a rehearsal's frozen records)."""
    cands = [run_dir / "ai"]
    cand = (cp.get("candidate") or {}).get("dir")
    if cand:
        cands.append(Path(cand).parent / "ai")
    for c in cands:
        found = sorted(c.glob("*/session.json")) if c.is_dir() else []
        if found:
            return [f.parent for f in found]
    return []


def session_rows(cp: dict, run_dir: Path) -> list[dict]:
    rows = []
    for d in _session_dirs(cp, run_dir):
        try:
            s = json.loads((d / "session.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        ev = _jsonl(d / "log.jsonl")
        start = next((e for e in ev if e.get("event") == "start"), {})
        end = next((e for e in ev if e.get("event") == "end"), {})
        files = next((e.get("files") for e in ev if e.get("event") == "mcp_server_log"), None) or []
        sub_id = (s.get("submission") or {}).get("run_id")
        mlog, best = None, None
        for f in files:                                   # sessions at once: the log whose submission is this one's
            m = _jsonl(Path(f))
            if sub_id and any(sub_id in str(e.get("result") or "") for e in m if e.get("tool") == "submit_proposals"):
                mlog = m
                break
            st0 = _ts((m[0] if m else {}).get("ts"))
            gap = abs((st0 - _ts(start.get("ts"))).total_seconds()) if st0 and _ts(start.get("ts")) else 1e9
            if best is None or gap < best[0]:
                best = (gap, m)
        if mlog is None and best is not None and (len(files) == 1 or sub_id is None):
            mlog = best[1]
        u = s.get("usage") or {}
        row = {"session": d.name, "kind": "analysis" if s.get("provisions") else "answer",
               "provisions": len(s.get("provisions") or []), "elapsed_s": s.get("elapsed_s"),
               "turns": s.get("num_turns"), "tool_calls": len(s.get("tool_calls") or []),
               "input_tokens": u.get("input_tokens"), "cache_creation": u.get("cache_creation_input_tokens"),
               "cache_read": u.get("cache_read_input_tokens"), "output_tokens": u.get("output_tokens"),
               "failure_class": s.get("failure_class"), "submitted": bool(sub_id),
               "prompt_chars": (d / "prompt.txt").stat().st_size if (d / "prompt.txt").exists() else None}
        if mlog:
            t_start, t_end = _ts(start.get("ts")), _ts(end.get("ts"))
            m0 = _ts(mlog[0].get("ts"))
            tools = [e for e in mlog if e.get("event") == "mcp" and e.get("tool") not in (None, "submission_record")]
            if t_start and m0:
                row["to_mcp_s"] = (m0 - t_start).total_seconds()
            if tools and m0:
                row["first_tool_s"] = (_ts(tools[0]["ts"]) - m0).total_seconds()
            subs = [e for e in tools if e.get("tool") == "submit_proposals"]
            if subs and t_end:
                row["after_submit_s"] = (t_end - _ts(subs[-1]["ts"])).total_seconds()
            elif tools and t_end:
                row["after_last_tool_s"] = (t_end - _ts(tools[-1]["ts"])).total_seconds()
        rows.append(row)
    return rows


def from_run(run: str, staging: str | None = None) -> dict:
    run_dir = _run_dir(run, staging)
    cp = json.loads((run_dir / "checkpoint.json").read_text(encoding="utf-8"))
    steps = {k: {"status": v.get("status"), "seconds": v.get("seconds", 0.0), "attempts": v.get("attempts")}
             for k, v in (cp.get("steps") or {}).items()}
    batches = []
    for bid, b in (cp.get("batches") or {}).items():
        req = b.get("request") if isinstance(b.get("request"), dict) else {}
        size = (req or {}).get("size") or {}
        batches.append({"batch": bid, "phase": b.get("phase"), "status": b.get("status"),
                        "units": len(b.get("provisions") or b.get("tasks") or ([b["region"]] if b.get("region") else [])),
                        "attempts": b.get("attempts"), "seconds": b.get("seconds"),
                        "session_seconds": b.get("session_seconds"),
                        "host_session_s": (b.get("host_session") or {}).get("elapsed_s"),
                        "input_tokens_est": size.get("input_tokens"),
                        "reused": (b.get("submission") or {}).get("reused", False)})
    ev = cp.get("events") or []
    segs, cur = [], None
    for e in ev:
        if e.get("event") in ("started", "resumed"):
            cur = {"start": e["ts"], "end": e["ts"]}
            segs.append(cur)
        elif cur is not None:
            cur["end"] = e["ts"]
    if segs:
        segs[-1]["end"] = max(segs[-1]["end"], cp.get("updated") or segs[-1]["end"])
    seg_s = [((_ts(s["end"]) - _ts(s["start"])).total_seconds() if _ts(s["end"]) and _ts(s["start"]) else None)
             for s in segs]
    wall = ((_ts(cp.get("updated")) - _ts(cp.get("created"))).total_seconds()
            if _ts(cp.get("updated")) and _ts(cp.get("created")) else None)
    sessions = session_rows(cp, run_dir)
    return {"run_id": cp.get("run_id"), "run_dir": str(run_dir), "route": (cp.get("settings") or {}).get("route"),
            "max_parallel_sessions": (cp.get("settings") or {}).get("max_parallel_sessions"),
            "status": cp.get("status"), "steps": steps,
            "steps_sum_s": round(sum(float(v["seconds"] or 0) for v in steps.values()), 1), "wall_s": wall,
            "segments": [{"start": s["start"], "end": s["end"], "seconds": x} for s, x in zip(segs, seg_s)],
            "batches": batches, "sessions": sessions, "concurrency": cp.get("concurrency"),
            "rate_gate": cp.get("rate_gate")}


def _fmt(v, w=9):
    if v is None:
        return "-".rjust(w)
    if isinstance(v, float):
        return f"{v:.1f}".rjust(w)
    return str(v).rjust(w)


def print_run(r: dict) -> None:
    print(f"run {r['run_id']} ({r['route']}, max_parallel_sessions {r['max_parallel_sessions']}): {r['status']}")
    print(f"  folder: {r['run_dir']}")
    print("\nsteps (checkpoint; seconds summed over attempts, a wait for a host not counted)")
    for k, v in r["steps"].items():
        print(f"  {k:<22}{_fmt(v['seconds'])} s  {v['status']}  attempts {v['attempts']}")
    label = "steps' sum"
    print(f"  {label:<22}{_fmt(r['steps_sum_s'])} s")
    print(f"  wall clock (created -> updated): {_fmt(r['wall_s'], 0)} s; segments: "
          + "; ".join(f"{s['start']} -> {s['end']} ({_fmt(s['seconds'], 0)} s)" for s in r["segments"]))
    print("\nbatches (seconds: in the run's thread; session: the exchange in a worker; host: the host session's own)")
    print(f"  {'batch':<26}{'phase':>11}{'status':>12}{'units':>6}{'tries':>6}{'seconds':>9}{'session':>9}"
          f"{'host':>9}{'tokens~':>9} reused")
    for b in r["batches"]:
        print(f"  {b['batch']:<26}{_fmt(b['phase'], 11)}{_fmt(b['status'], 12)}{_fmt(b['units'], 6)}"
              f"{_fmt(b['attempts'], 6)}{_fmt(b['seconds'])}{_fmt(b['session_seconds'])}{_fmt(b['host_session_s'])}"
              f"{_fmt(b['input_tokens_est'])} {'yes' if b['reused'] else ''}")
    ss = r["sessions"]
    print(f"\nhost sessions started: {len(ss)}" + ("" if ss else " (no session records found next to this checkpoint)"))
    if ss:
        print(f"  {'session':<44}{'kind':>9}{'provs':>6}{'elapsed':>9}{'turns':>6}{'tools':>6}{'cache_wr':>10}"
              f"{'cache_rd':>10}{'out':>8}{'to_mcp':>7}{'1st_tool':>9}{'tail':>7}")
        for s in ss:
            print(f"  {s['session']:<44}{_fmt(s['kind'], 9)}{_fmt(s['provisions'], 6)}{_fmt(s['elapsed_s'])}"
                  f"{_fmt(s['turns'], 6)}{_fmt(s['tool_calls'], 6)}{_fmt(s['cache_creation'], 10)}"
                  f"{_fmt(s['cache_read'], 10)}{_fmt(s['output_tokens'], 8)}{_fmt(s.get('to_mcp_s'), 7)}"
                  f"{_fmt(s.get('first_tool_s'))}{_fmt(s.get('after_submit_s', s.get('after_last_tool_s')), 7)}")
        an = [s for s in ss if s["kind"] == "analysis" and s.get("to_mcp_s") is not None]
        if an:
            ov = [s["to_mcp_s"] + s.get("first_tool_s", 0) + s.get("after_submit_s", 0) for s in an]
            el = sum(s["elapsed_s"] or 0 for s in an)
            print(f"  analysis sessions: {len(an)}, {el:.0f} s in all; fixed overhead per session (start -> MCP server "
                  f"-> first tool call, submission -> end) {min(ov):.0f}-{max(ov):.0f} s, {sum(ov):.0f} s in all "
                  f"({100 * sum(ov) / el:.1f}% of the session time)")
    if r.get("concurrency"):
        print("\nconcurrency (this drive):")
        for ph, c in r["concurrency"].items():
            print(f"  {ph}: " + ", ".join(f"{k} {v}" for k, v in c.items()))
    if r.get("rate_gate"):
        print(f"rate gate: {r['rate_gate']}")


# ---------------------------------------------------------------------------------------------- --simulate

GENERIC_ANALYSIS = {"phase": "analysis", "when": {}, "turns": [{"match": {"last_role": "user", "contains": ["TASK PACKET"]},
                    "response": {"usage": {"input_tokens": 19000, "output_tokens": 900},
                                 "text": '{"addendum": "ADD-03", "state": ${state}, "statements": [], "items": []}'}}]}


def _cassette(workdir: Path, rate_limited: str | None = None, times: int = 10, fill: int = 0) -> Path:
    """Blind-02's ADD-03 workflow cassette with the critic's sessions; `fill` generic analysis sessions appended (an
    empty answer, so a batch the cassette does not record still takes a session's time in the simulation; its
    provisions end unaccounted, as a model that answered nothing)."""
    import yaml
    cas = ROOT / "tests/fixtures/ai_cassettes"
    data = yaml.safe_load((cas / "workflow_add03.yaml").read_text(encoding="utf-8"))
    data["sessions"] += yaml.safe_load((cas / "s11_workflow_critic.yaml").read_text(encoding="utf-8"))["sessions"]
    data["sessions"] += [copy.deepcopy(GENERIC_ANALYSIS) for _ in range(fill)]
    if rate_limited:
        for s in data["sessions"]:
            if s["phase"] == "analysis" and rate_limited in (s.get("when") or {}).get("provisions_include", []):
                s["turns"] = [{"error": {"kind": "http_429", "status": 429, "retryable": True,
                                         "message": "rate_limit_error: recorded"}, "times": times}] + s["turns"]
    workdir.mkdir(parents=True, exist_ok=True)
    p = workdir / "bench_cassette.yaml"
    p.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return p


def _cfg(workdir: Path, n: int) -> Path:
    import yaml
    from tenderpack.ai import config as C
    cfg = copy.deepcopy(C.load())
    cfg["concurrency"]["max_parallel_sessions"] = n
    cfg["failures"]["rate_limit"]["seed"] = 7
    p = workdir / f"ai-{n}.yaml"
    p.write_text(yaml.safe_dump({k: v for k, v in cfg.items() if not k.startswith("_")}, sort_keys=False),
                 encoding="utf-8")
    return p


class _Latency:
    """RecordedProvider.complete with a simulated latency per recorded session, and a record of every call (session,
    phase, thread, start, end). An analysis session takes (fixed + per provision x the provisions its packet carries)
    x scale, spread over its turns: fixed 12 s (blind-06's measured start, MCP server, first call and tail per session)
    and each provision's own time, drawn (per seed, by its id) from blind-06's sessions ((elapsed - 12) / provisions:
    27-74 s), so the total work is the same whatever the plan and only the scheduling differs. A
    downstream session takes one of blind-06's downstream session times x scale; a critic request 3.4 s x scale."""

    FIXED_S = 12.0

    def __init__(self, cassette: dict, scale: float, seed: int | None, slow_first: float = 0.0, hold_first: int = 0,
                 hold_timeout_s: float = 60.0):
        self.cassette, self.scale, self.slow_first = cassette, scale, slow_first
        # hold_first N: the FIRST analysis session does not answer until N other analysis sessions have answered
        # (or hold_timeout_s passes): a deterministic "later answers arrive first", whatever the machine's speed
        self.hold_first, self.hold_timeout_s = int(hold_first), float(hold_timeout_s)
        self.done_sessions: set[int] = set()
        self.cond = threading.Condition()
        provs = [5, 7, 6, 7, 8, 8, 8, 8, 5, 8]                     # blind-06's analysis sessions, in order
        per = [(e - self.FIXED_S) / n for e, n in zip(BLIND06_ANALYSIS_S, provs)]
        ds = list(BLIND06_DOWNSTREAM_S)
        if seed is not None:
            random.Random(seed).shuffle(per)
            random.Random(seed + 1).shuffle(ds)
        self.per, self.ds = per, ds
        self.seed = seed
        self.calls: list[dict] = []
        self.provisions: dict[int, float] = {}
        self.lock = threading.Lock()

    def _provision_ids(self, req) -> list[str]:
        """The provisions of the batch's packet (the first user message: TASK PACKET + JSON)."""
        from tenderpack.ai.providers.recorded import PACKET_MARK
        for m in getattr(req, "messages", None) or []:
            c = m.get("content")
            texts = [c] if isinstance(c, str) else [b.get("text", "") for b in c or [] if isinstance(b, dict)]
            for t in texts:
                if t and PACKET_MARK in t:
                    try:
                        pk = json.loads(t[t.index(PACKET_MARK) + len(PACKET_MARK):])
                        return [str(x.get("unit_id")) for x in pk.get("provisions") or []]
                    except (ValueError, AttributeError):
                        return []
        return []

    def rate(self, pid: str) -> float:
        """A provision's own time (s, before scaling): the same whatever batch it is planned in."""
        import hashlib
        h = int(hashlib.sha256(f"{self.seed}:{pid}".encode()).hexdigest()[:8], 16)
        return self.per[h % len(self.per)]

    def seconds(self, i: int, req=None) -> float:
        s = self.cassette["sessions"][i]
        turns = max(1, len([t for t in s.get("turns") or [] if "error" not in t]))
        phase = s.get("phase")
        k = sum(1 for x in self.cassette["sessions"][:i] if x.get("phase") == phase)
        if phase == "analysis":
            if i not in self.provisions:
                ids = self._provision_ids(req)
                self.provisions[i] = sum(self.rate(p) for p in ids) if ids else 8 * self.per[0]
            base = self.FIXED_S + self.provisions[i]
        elif phase == "downstream":
            base = self.ds[k % len(self.ds)]
        else:
            base = BLIND06_CRITIC_S
        extra = self.slow_first if (phase == "analysis" and k == 0) else 0.0
        return (base * self.scale + extra) / turns

    @contextlib.contextmanager
    def installed(self):
        from tenderpack.ai.providers.recorded import RecordedProvider
        real = RecordedProvider.complete
        meter = self

        def complete(self_, req):
            try:                                     # the workflow cassette's session: "<cassette>#session<i>"
                i = int(str(getattr(self_, "cassette_path", "") or "").rsplit("#session", 1)[1])
            except (IndexError, ValueError):
                i = -1
            t0 = time.monotonic()
            phase = meter.cassette["sessions"][i].get("phase") if i >= 0 else None
            first = i >= 0 and phase == "analysis" and not any(
                x.get("phase") == "analysis" for x in meter.cassette["sessions"][:i])
            if first and meter.hold_first:
                with meter.cond:
                    meter.cond.wait_for(lambda: len(meter.done_sessions) >= meter.hold_first,
                                        timeout=meter.hold_timeout_s)
            if i >= 0:
                time.sleep(meter.seconds(i, req))
            try:
                return real(self_, req)
            finally:
                if i >= 0 and phase == "analysis" and not first:
                    with meter.lock:
                        n = sum(1 for c in meter.calls if c["session"] == i) + 1
                    turns = len([t for t in meter.cassette["sessions"][i].get("turns") or [] if "error" not in t])
                    if n >= max(1, turns):
                        with meter.cond:
                            meter.done_sessions.add(i)
                            meter.cond.notify_all()
                with meter.lock:
                    meter.calls.append({"session": i, "phase": (meter.cassette["sessions"][i].get("phase")
                                                                if i >= 0 else None),
                                        "start": t0, "end": time.monotonic(),
                                        "thread": threading.current_thread().name})
        RecordedProvider.complete = complete
        try:
            yield self
        finally:
            RecordedProvider.complete = real


def _summary(cp: dict) -> dict:
    return {"batches": {k: (b["status"], b.get("items"), b.get("provisions") or b.get("tasks"))
                        for k, b in cp["batches"].items()},
            "provisions": {k: v["status"] for k, v in cp["provisions"].items()},
            "critic": {k: (b.get("critic") or {}).get("status") for k, b in cp["batches"].items()}}


def _evidence(workdir: Path) -> Path:
    from tenderpack.cli import ingest
    out = workdir / "evidence"
    if not (out / "BUILD_MANIFEST.json").is_file():
        res = ingest(ROOT / "config/pack.yaml", out, ROOT, quiet=True)
        if res.get("exit_code") != 0:
            raise SystemExit(f"ingest of the pack failed: {res.get('status')}")
    return out


def simulate(n: int, *, evidence: Path | None = None, workdir: Path, seed: int | None = 7, scale: float = 0.004,
             stop_after: str | None = "validation", slow_first: float = 0.0, rate_limit: bool = False,
             resume_after_deferral: bool = True, fill: int = 0, hold_first: int = 0) -> dict:
    """One recorded run at max_parallel_sessions `n` with simulated latency (see the module docstring)."""
    import yaml
    from tenderpack.ai import workflow as W
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    evidence = Path(evidence) if evidence else _evidence(workdir)
    cas = _cassette(workdir, rate_limited="ADD-03:7.1" if rate_limit else None, fill=fill)
    cdata = yaml.safe_load(cas.read_text(encoding="utf-8"))
    lat = _Latency(cdata, scale, seed, slow_first, hold_first=hold_first)
    run_id = f"bench-n{n}" + (f"-s{seed}" if seed is not None else "") + ("-rl" if rate_limit else "")
    slept: list[float] = []
    t0 = time.perf_counter()
    with lat.installed():
        res = W.start("ADD-03", ROOT / "rehearsals/blind-02/input/ADD-03_Addendum_No_3.pdf",
                      pack=ROOT / "config/pack.yaml", evidence=evidence, staging=workdir / "staging",
                      worklog=workdir / "worklog", run_id=run_id, route="recorded", cassette=cas, batch_size=8,
                      ai_config=_cfg(workdir, n), background_before=False, stop_after=stop_after,
                      echo=lambda *a, **k: None, sleep=slept.append)
    wall = time.perf_counter() - t0
    cp = W.load(run_id, workdir / "staging").data
    out = {"n": n, "seed": seed, "status": res.get("status"), "exit_code": res.get("exit_code"),
           "wall_s": round(wall, 3), "steps": {k: v.get("seconds") for k, v in cp["steps"].items()}}
    by_sess = {}
    for c in lat.calls:
        by_sess.setdefault(c["session"], []).append(c)
    sess_batch = {b.get("session"): k for k, b in cp["batches"].items() if b.get("session") is not None}
    arrivals = sorted(((max(c["end"] for c in cs), sess_batch.get(i)) for i, cs in by_sess.items()
                       if cdata["sessions"][i].get("phase") == "analysis"), key=lambda x: x[0])
    out["arrival_order"] = [b for _, b in arrivals if b]
    out["sessions_started"] = len(by_sess)
    out["calls"] = len(lat.calls)
    phases = {}
    for ph in ("analysis", "downstream", "critic"):
        cs = [c for c in lat.calls if c["phase"] == ph]
        if not cs:
            continue
        window = max(c["end"] for c in cs) - min(c["start"] for c in cs)
        busy = sum(c["end"] - c["start"] for c in cs)
        phases[ph] = {"window_s": round(window, 3), "busy_s": round(busy, 3),
                      "idle_slots_s": round(max(0.0, n * window - busy), 3),
                      "max_threads": len({c["thread"] for c in cs})}
    out["phases"] = phases
    out["context_tokens_est"] = sum(int(((b.get("request") or {}).get("size") or {}).get("input_tokens") or 0)
                                    for b in cp["batches"].values() if isinstance(b.get("request"), dict))
    out["concurrency"] = cp.get("concurrency") or {}
    out["rate_gate"] = cp.get("rate_gate")
    out["backoff_sleeps_s"] = [round(x, 1) for x in slept]
    out["summary"] = _summary(cp)
    if rate_limit and resume_after_deferral and res.get("exit_code") == 5:
        done = {k for k, b in cp["batches"].items() if b["status"] == "done"}
        _cassette(workdir, fill=fill)                            # the limit is over
        with lat.installed():
            res2 = W.resume(run_id, workdir / "staging", stop_after=stop_after, echo=lambda *a, **k: None,
                            sleep=lambda s: None)
        cp2 = W.load(run_id, workdir / "staging").data
        out["after_resume"] = {"status": res2.get("status"), "exit_code": res2.get("exit_code"),
                               "asked_again": sorted(k for k, b in cp2["batches"].items()
                                                     if k in done and b.get("attempts") != cp["batches"][k].get("attempts")),
                               "deferred_then_done": sorted(k for k, b in cp["batches"].items()
                                                            if b["status"] == "deferred"
                                                            and cp2["batches"][k]["status"] == "done")}
    return out


def print_sim(rows: list[dict]) -> None:
    print("simulated recorded run (blind-02 ADD-03 cassette; latency: blind-06's host session times x scale)")
    print(f"  {'n':>2}{'status':>10}{'exit':>5}{'wall s':>8}{'analysis':>9}{'downstr':>8}{'critic':>7}{'sessions':>9}"
          f"{'tokens~':>9}{'idle(an)':>9}{'idle(ds)':>9}  arrival order (analysis)")
    for r in rows:
        st = r["steps"]
        print(f"  {r['n']:>2}{r['status']:>10}{r['exit_code']:>5}{r['wall_s']:>8.2f}{(st.get('analysis') or 0):>9.2f}"
              f"{(st.get('downstream') or 0):>8.2f}{(st.get('critic') or 0):>7.2f}{r['sessions_started']:>9}"
              f"{r['context_tokens_est']:>9}{(r['phases'].get('analysis') or {}).get('idle_slots_s', 0):>9.2f}"
              f"{(r['phases'].get('downstream') or {}).get('idle_slots_s', 0):>9.2f}  {' '.join(r['arrival_order'])}")
        if r.get("rate_gate") or r.get("after_resume"):
            print(f"     rate gate {r.get('rate_gate')}; backoff sleeps {r.get('backoff_sleeps_s')}; "
                  f"resume: {r.get('after_resume')}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--from-run", help="a run id (with --staging) or a run folder holding checkpoint.json")
    ap.add_argument("--staging", help="the staging folder (default staging/ai)")
    ap.add_argument("--simulate", action="store_true")
    ap.add_argument("--parallel", default="1,2,3")
    ap.add_argument("--scale", type=float, default=0.004)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--rate-limit", action="store_true")
    ap.add_argument("--stop-after", default="validation")
    ap.add_argument("--fill", type=int, default=8, help="generic analysis sessions added to the cassette (default 8: "
                                                       "every planned batch takes a session's time)")
    ap.add_argument("--evidence")
    ap.add_argument("--workdir")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.from_run:
        r = from_run(a.from_run, a.staging)
        print(json.dumps(r, indent=1, default=str) if a.json else "", end="")
        if not a.json:
            print_run(r)
        return 0
    if a.simulate:
        import tempfile
        wd = Path(a.workdir) if a.workdir else Path(tempfile.mkdtemp(prefix="bench-workflow-"))
        rows = []
        stop = None if a.stop_after in ("", "none", "None") else a.stop_after
        for n in [int(x) for x in a.parallel.split(",") if x]:
            rows.append(simulate(n, evidence=Path(a.evidence) if a.evidence else None, workdir=wd / f"n{n}",
                                 seed=a.seed, scale=a.scale, stop_after=stop, fill=a.fill))
        if a.rate_limit:
            n = max(int(x) for x in a.parallel.split(",") if x)
            rows.append(simulate(n, evidence=Path(a.evidence) if a.evidence else None, workdir=wd / f"rl{n}",
                                 seed=a.seed, scale=a.scale, stop_after=stop, rate_limit=True, fill=a.fill))
        if a.json:
            print(json.dumps(rows, indent=1, default=str))
        else:
            print_sim(rows)
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
