"""The workflow's checkpoint: staging/ai/runs/<run_id>/checkpoint.json (tenderpack/ai/workflow.py).

One JSON file, rewritten atomically (a temporary sibling, then os.replace) after every state change, so a run stopped
at any point (a crash, a kill, Ctrl-C, a wait for a host submission) continues from it with `tenderpack ai resume`:

    format        "tenderpack-ai-run/1"
    run_id, addendum, created, updated
    status        running | waiting_for_host | stopped | failed | complete | partial | deferred (session 11: a
                  batch was deferred for a rate limit and the run stopped cleanly; `resume` continues it)
                  (complete: the `completeness` record is complete, session 11: every provision answered by a
                   promoted item, every downstream task answered by a promotable item and every downstream batch
                   run, check-register on the candidate clean, the candidate outputs published; partial: the run
                   finished without all of that, the reasons in `status_reason` and `completeness`; stopped:
                   --stop-after or a structural failure, with `status_reason`; failed: a step raised, with the reason)
    execution, completeness, approval
                  (session 11) three separate records, rewritten at the end of every drive (workflow.execution,
                  completeness, approval): what ran; what the run completed and why not; human approval (always
                  "none" from the run, with any decisions a person recorded in the candidate's decisions file)
    settings      what the run was started with (route, model, cassette, pack, evidence, staging, worklog, batch sizes,
                  caps); `resume` reuses them
    inputs        the PDF (path, sha256, pages, the candidate copy), the preceding state (pack id, evidence build id)
                  and the sha256 of every real input file copied into the candidate, as found when the run started
    candidate     the candidate workspace's paths (pack, pack-before, build, out-before, out)
    steps         {step: {status, started, finished, seconds, attempts, detail...}} for STEPS, in order (`readings`:
                  readings proposed for addendum image regions that stopped ingest, then ingest again); `seconds` is
                  the wall-clock time spent in the step, summed over attempts (a wait for a host is not counted)
    batches       {batch id: {phase (reading | analysis | downstream), provisions|tasks|region, status, attempts,
                  staged_run, error, session, seconds}}
                  status pending | running | waiting_for_host | done | failed | skipped | interrupted, and (session 11,
                  the request layer, tenderpack/ai/requests.py):
                    deferred   a rate limit outlasted the bounded backoff: asked again by `resume` (never failed)
                    escalated  a single provision / task / region whose request does not fit even alone: its size is
                               recorded and a person splits it (never truncated)
                    split      a batch whose request did not fit, replaced by its parts (`parts`), in order
                  Per batch, the request layer also records: `failure_class` (rate_limit | provider | malformed) with
                  `attempts` (every failed call: class, kind, status, wait), `deferrals` (each with its time and the
                  reset the provider named), `request` (the complete size, the repair, the malformed items, the usage,
                  the route notices), `malformed_items` (items set aside after the one repair) and `critic` ({status
                  pending | done | deferred | failed | not_needed | skipped, selected, reviewed, agrees, errors, ...}).
    notices       the route notices of the run (capabilities used unverified or declared by the host; a structured-output
                  schema not used or rejected), each with its batch; shown in the review packet
    provisions    {unit id: {kind, pages, batch, status, items, accounted, accounted_by, statuses, reason, history}}
                  status pending -> proposed -> validated, or unaccounted (its batch ran and nothing accounts for it)
    structure     the addendum's units that are not provisions (headings, table containers, image regions), each
                  listed with its kind so the owner sees that nothing was dropped
    downstream    {"tasks": {task id: {...}}, "items": {item id: {type, task, status, verification_status, ...}}}
                  an item's status pending -> proposed -> validated
    out_before    the pre-addendum outputs: status (running | pending | done | refused | not_built), the background
                  process, the cache key and the build's result (exit code, seconds, from_cache)
    interventions every manual step (a submit-batch: who, when, which batch, the file and its sha256, the host model)
                  and every automatic host session (named as such: not a person)
    usage         calls and tokens across the batches (cost as the providers report it; null when not computed)
    host_usage    (session 14) the host's own usage per host session, from the session records next to the run
                  (workflow.host_usage: sessions [{session, batch, kind, usage | null}], known, unknown, totals); a
                  session without usage is unknown, never 0; rewritten at the end of every drive
    concurrency_drives
                  (session 14) every drive's concurrency record ({drive, segment, interrupted, phases}); `concurrency`
                  keeps the last drive's, as before
    interventions (session 14) also the person's stop and resume (kinds "stop (the person's action)", "resume (the
                  person's action)"), the sessions the stop cut and the staged answers reused, each with its time
    events        a short history (started, resumed, stale lock taken over, stopped, code_changed, ...)
    code_identity (session 13) {start, segments [...], differ}: each a code_identity() record (the git HEAD when git
                  is available and whether the tree was dirty, a content hash over CODE_GLOBS computed from the files,
                  the number of files, the time). `start` is taken when the run starts; every resume recomputes it and
                  refuses a different hash unless `--allow-code-change "<reason>"` is given, which appends the new
                  segment (with the reason) and sets `differ`: "segments ran on different code"
"""
from __future__ import annotations

import contextlib
import datetime as dt
import json
import os
import socket
import time
from pathlib import Path

FORMAT = "tenderpack-ai-run/1"
STEPS = ("ingest", "readings", "analysis", "validation", "downstream", "downstream_validation", "critic", "promotion",
         "pin", "check_register", "outputs", "diff", "review")
BATCH_STATES = ("pending", "running", "waiting_for_host", "done", "failed", "skipped", "interrupted", "deferred",
                "escalated", "split")
PROVISION_STATES = ("pending", "proposed", "validated", "unaccounted")
ITEM_STATES = ("pending", "proposed", "validated")


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# session 13: what a run's behaviour depends on besides its inputs: the code, the configuration and the runtime policy
# (tenderpack/ai/policy/*.md, composed by tenderpack.ai.policy into every prompt of every route and phase)
CODE_GLOBS = ("tenderpack/**/*.py", "tenderpack/ai/policy/*.md", "config/*.yaml", "pyproject.toml")
POLICY_DIR = "tenderpack/ai/policy"


def code_identity(root: Path) -> dict:
    """The code and policy identity of the tree at `root` (session 13): {content_sha256 (over the relative path and
    the bytes of every file CODE_GLOBS match, sorted; computed from the files, never from git), files, git_head,
    git_dirty (None when git is not available), policy (session 13: the runtime policy's identity, policy.identity of
    the tree's tenderpack/ai/policy/; None without it), recorded}. A changed policy file changes content_sha256 too, so
    a resume over a changed policy is refused like any code change."""
    import hashlib
    import subprocess
    root = Path(root)
    files = sorted({f for g in CODE_GLOBS for f in root.glob(g) if f.is_file() and "__pycache__" not in f.parts})
    h = hashlib.sha256()
    for f in files:
        h.update(f.relative_to(root).as_posix().encode() + b"\0" + f.read_bytes() + b"\0")
    head = dirty = None
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=root, capture_output=True, text=True, timeout=10)
        own_checkout = top.returncode == 0 and Path(top.stdout.strip()).resolve() == root.resolve()
        r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, timeout=10) if own_checkout else None
        if r is not None and r.returncode == 0:
            head = r.stdout.strip()
            st = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=root, capture_output=True,
                                text=True, timeout=20)
            dirty = bool(st.stdout.strip()) if st.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        pass
    try:
        package_base = json.loads((root / "INTERVIEW.json").read_text()).get("base")
    except (OSError, ValueError):
        package_base = None
    from .policy import identity as policy_identity
    pol = policy_identity(root / POLICY_DIR) if (root / POLICY_DIR).is_dir() else None
    return {"content_sha256": h.hexdigest(), "files": len(files), "git_head": head, "git_dirty": dirty,
            "policy": pol, "recorded": now_iso(), "package_base": package_base}


class Checkpoint:
    def __init__(self, path: Path, data: dict):
        self.path, self.data = Path(path), data

    # ------------------------------------------------------------------ files
    @classmethod
    def new(cls, path: Path, **fields) -> "Checkpoint":
        data = {"format": FORMAT, **fields, "created": now_iso(), "updated": now_iso(), "status": "running",
                "status_reason": None, "steps": {s: {"status": "pending", "seconds": 0.0, "attempts": 0} for s in STEPS},
                "batches": {}, "provisions": {}, "structure": [], "downstream": {"tasks": {}, "items": {}},
                "interventions": [], "usage": {"calls": 0, "input_tokens": 0, "output_tokens": 0, "cost_usd": None},
                "events": []}
        cp = cls(path, data)
        cp.save()
        return cp

    @classmethod
    def load(cls, path: Path) -> "Checkpoint":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if data.get("format") != FORMAT:
            raise ValueError(f"{path}: not a {FORMAT} checkpoint (format {data.get('format')!r})")
        return cls(path, data)

    def save(self) -> None:
        self.data["updated"] = now_iso()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_name(f".{self.path.name}.{os.getpid()}.tmp")
        tmp.write_text(json.dumps(self.data, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
        os.replace(tmp, self.path)

    # ------------------------------------------------------------------ run status and events
    def event(self, name: str, **detail) -> None:
        self.data["events"].append({"ts": now_iso(), "event": name, **detail})
        self.save()

    def set_status(self, status: str, reason: str | None = None) -> None:
        self.data["status"], self.data["status_reason"] = status, reason
        self.save()

    # ------------------------------------------------------------------ steps
    def step(self, name: str) -> dict:
        # a checkpoint written before a step existed (e.g. `readings`) gains it as pending
        return self.data["steps"].setdefault(name, {"status": "pending", "seconds": 0.0, "attempts": 0})

    def done(self, name: str) -> bool:
        return self.step(name)["status"] == "done"

    @contextlib.contextmanager
    def timed(self, name: str):
        """Run a step: status running, then done (with the seconds added) or failed (with the reason)."""
        st = self.step(name)
        st.update(status="running", started=st.get("started") or now_iso(), attempts=st.get("attempts", 0) + 1)
        st.pop("error", None)
        self.save()
        t0 = time.perf_counter()
        try:
            yield st
        except BaseException as e:
            st["seconds"] = round(st.get("seconds", 0.0) + time.perf_counter() - t0, 3)
            st["status"] = "interrupted" if isinstance(e, KeyboardInterrupt) else (
                st["status"] if st["status"] in ("waiting_for_host", "stopped") else "failed")
            if st["status"] in ("failed", "interrupted"):
                st["error"] = f"{type(e).__name__}: {str(e)[:600]}"
            self.save()
            raise
        st["seconds"] = round(st.get("seconds", 0.0) + time.perf_counter() - t0, 3)
        if st["status"] == "running":
            st["status"] = "done"
        st["finished"] = now_iso()
        self.save()

    def reset_step(self, name: str) -> None:
        st = self.step(name)
        st["status"] = "pending"
        self.save()

    # ------------------------------------------------------------------ provisions, batches, items
    def provision(self, pid: str) -> dict:
        return self.data["provisions"][pid]

    def set_provision(self, pid: str, status: str | None = None, **kw) -> None:
        p = self.data["provisions"][pid]
        if status and status != p.get("status"):
            if status not in PROVISION_STATES:
                raise ValueError(f"unknown provision state {status!r}")
            p.setdefault("history", []).append({"ts": now_iso(), "status": status})
            p["status"] = status
        p.update(kw)

    def batch(self, bid: str) -> dict:
        return self.data["batches"][bid]

    def batches(self, phase: str) -> list[str]:
        return [k for k, v in self.data["batches"].items() if v["phase"] == phase]

    def item(self, iid: str) -> dict:
        return self.data["downstream"]["items"][iid]

    def set_item(self, iid: str, status: str | None = None, **kw) -> None:
        it = self.data["downstream"]["items"].setdefault(iid, {"status": "pending", "history": []})
        if status and status != it.get("status"):
            if status not in ITEM_STATES:
                raise ValueError(f"unknown item state {status!r}")
            it["history"].append({"ts": now_iso(), "status": status})
            it["status"] = status
        it.update(kw)

    def intervention(self, **kw) -> None:
        self.data["interventions"].append({"ts": now_iso(), **kw})
        self.save()

    def add_usage(self, calls: int = 0, input_tokens: int = 0, output_tokens: int = 0, cost_usd=None) -> None:
        u = self.data["usage"]
        u["calls"] += int(calls or 0)
        u["input_tokens"] += int(input_tokens or 0)
        u["output_tokens"] += int(output_tokens or 0)
        if cost_usd is not None:
            u["cost_usd"] = round((u["cost_usd"] or 0.0) + float(cost_usd), 6)

    # ------------------------------------------------------------------ timings
    def timings(self) -> dict[str, float]:
        return {s: round(self.step(s).get("seconds", 0.0), 1) for s in STEPS}

    def timing_lines(self, target_min: float = 30.0) -> list[str]:
        t = self.timings()
        total = sum(t.values())
        lines = [f"  {s:<22} {t[s]:>8.1f} s  {self.step(s)['status']}" for s in STEPS]
        lines.append(f"  {'total (steps)':<22} {total:>8.1f} s  ({total / 60:.1f} min; target {target_min:g} min from the "
                     "PDF to candidate outputs and review packet, human review excluded)")
        waits = [b for b in self.data["batches"].values() if b.get("waited_s")]
        if waits:
            lines.append(f"  waiting for host submissions (not counted above): "
                         f"{sum(b['waited_s'] for b in waits):.0f} s")
        return lines


# ---------------------------------------------------------------------------------------------- the run lock

class RunLockError(Exception):
    pass


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


class RunLock:
    """`run.lock` in the run folder: one process drives a run at a time. A lock whose process is dead (same host) is
    taken over by a resume and the takeover is recorded in the checkpoint's events (never silently)."""

    def __init__(self, run_dir: Path):
        self.path = Path(run_dir) / "run.lock"
        self.token = os.urandom(8).hex()
        self.taken_over: dict | None = None

    def acquire(self) -> "RunLock":
        info = {"pid": os.getpid(), "host": socket.gethostname(), "created": now_iso(), "token": self.token}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            try:
                cur = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                cur = {"unreadable": True}
            same_host = cur.get("host") == socket.gethostname()
            if cur.get("unreadable") or (same_host and cur.get("pid") and not _pid_alive(int(cur["pid"]))):
                self.taken_over = cur
                self.path.unlink(missing_ok=True)
                return self.acquire()
            raise RunLockError(f"the run is being driven by process {cur.get('pid')} on {cur.get('host')} (since "
                               f"{cur.get('created')}); wait for it, or stop that process first") from None
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(info, fh)
        return self

    def release(self) -> None:
        try:
            cur = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        if cur.get("token") == self.token:
            self.path.unlink(missing_ok=True)
