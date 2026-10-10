"""Real backend jobs for the panel (session 12, part 5).

Every action of the panel is the existing command line run in a subprocess: `<this interpreter> -m tenderpack ...`
with the repository as the working directory, never a function call made to look like one and never a demo. Each job
has its own folder <panel_dir>/jobs/<job-id>/ with
  job.json     the exact argv, the working directory, the command line to repeat it in a terminal, started, finished,
               the exit code and its meaning, the pid, and what the panel recorded beside it (an upload's sanitised
               original name and sha256, the run id); never the environment, never a key;
  output.log   stdout and stderr of the command as it ran.
One job runs at a time per group (ingest/outputs/strict/check-register share the evidence build and out/; the AI run
and resume share the staging folder; a diff; a decision; session 13: the AI quick review, started under `nice -n 10`,
and its notes). A job the panel did not see end (the panel was closed) is
shown `interrupted` once its process is gone; the AI workflow's own checkpoint says where to resume.

Stopping a job sends SIGINT to its process group (the workflow records the interruption in its checkpoint), then
SIGTERM and SIGKILL if it does not end."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import secrets
import shlex
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

GROUPS = {"ingest": "build", "outputs": "build", "strict": "build", "check-register": "build",
          "interview-decision": "build",
          "ai-run": "ai", "ai-resume": "ai", "diff": "diff", "decision": "decision",
          # session 13, part 4: the AI quick review has its own group (one at a time, beside the run, never blocking it)
          # and its notes (compare, an owner's answer, offering answers to a run) another
          "ai-quick-review": "quick-review", "qr-compare": "quick-review-notes", "qr-answer": "quick-review-notes",
          "qr-offer": "quick-review-notes"}
NICE = {"ai-quick-review": 10}     # session 13: started under `nice -n 10` (lower priority than the main run)

AI_EXIT = {0: "finished (complete or partial), or stopped where asked",
           1: "a step failed, or the candidate outputs build was refused (the last validated state is kept)",
           2: "refused before anything ran (or ingest failed structurally)",
           4: "waiting for a host submission (`tenderpack ai submit-batch`)",
           5: "deferred: a batch hit a rate limit; resume after the reset time the run names",
           6: "stopped until a person acts (the reason says what to do); then resume"}
EXIT_MEANING = {
    "interview-decision": {0: "decision applied and validated outputs rebuilt; history retained",
                           2: "decision refused or rolled back; see the validation details below"},
    "ingest": {0: "structure OK; the evidence build was written",
               2: "structural failure: the previous build is kept; the candidate is in <build>.failed",
               3: "readings still pending human review (--require-approved)"},
    "outputs": {0: "published: a WORKING DRAFT that lists its release blockers",
                2: "structural failure: nothing published; the previous outputs are kept (candidate in <out>.failed)"},
    "strict": {0: "released",
               2: "structural failure: nothing published; the previous outputs are kept (candidate in <out>.failed)",
               3: "release refused while a blocker remains (e.g. human approvals pending); the previous outputs are "
                  "kept (candidate in <out>.rejected)"},
    "check-register": {0: "no findings", 1: "findings listed in the output"},
    "ai-run": AI_EXIT, "ai-resume": AI_EXIT,
    "diff": {0: "the report is the output below"},
    "ai-quick-review": {0: "the PRELIMINARY AI BRIEFING was written (unverified)", 1: "the session failed: no briefing "
                        "(the reason is in the output)", 2: "refused before any call (the output says why)",
                        5: "deferred: a rate limit; the quick review is lower priority, start it again later"},
    "qr-compare": {0: "the comparison was written (model agreement is not proof)", 2: "refused (the output says why)"},
    "qr-answer": {0: "the answer was recorded against the question (curation/ is not changed)",
                  2: "refused (the output says why); nothing recorded"},
    "qr-offer": {0: "the answers were offered or held (the output lists which, and why)",
                 2: "refused (the output says why)"},
    "decision": {0: "the engine recorded the decision (its output below)",
                 1: "the engine refused (its output below says why); nothing recorded",
                 2: "the engine refused (its output below says why); nothing recorded"},
}
JOB_ID = re.compile(r"^[0-9]{8}T[0-9]{6}Z-[a-z-]+-[0-9a-f]{6}$")
FULL_LOG = ("diff", "decision", "check-register")         # shown whole (capped), not only the tail


class JobError(Exception):
    pass


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def meaning(kind: str, code) -> str:
    if code is None:
        return ""
    if isinstance(code, int) and code < 0:
        return f"ended by signal {-code}"
    return EXIT_MEANING.get(kind, {}).get(code, "see the output")


def _alive(pid) -> bool:
    try:
        os.kill(int(pid), 0)
    except (OSError, ValueError, TypeError):
        return False
    return True


class Jobs:
    def __init__(self, root: Path, jobs_dir: Path, python: str | None = None):
        self.root = Path(root)
        self.dir = Path(jobs_dir)
        self.python = python or sys.executable
        self.dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._procs: dict[str, subprocess.Popen] = {}
        for rec in self.list():                                   # a job an earlier panel did not see end
            if rec["status"] == "interrupted" and rec.get("finished") is None and "note" in rec:
                self._save(rec)

    # ------------------------------------------------------------------ records
    def _path(self, jid: str) -> Path:
        return self.dir / jid / "job.json"

    def _save(self, rec: dict) -> None:
        p = self._path(rec["id"])
        tmp = p.with_name(f".job.json.{os.getpid()}.{threading.get_ident()}.tmp")
        tmp.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(tmp, p)

    def get(self, jid: str) -> dict | None:
        if not JOB_ID.match(jid or ""):
            return None
        try:
            rec = json.loads(self._path(jid).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        if rec.get("status") == "running" and jid not in self._procs and not _alive(rec.get("pid")):
            rec.update(status="interrupted",           # started by an earlier panel; its process is gone
                       note="the panel did not see this job's process end; its exit code is unknown")
        return rec

    def list(self) -> list[dict]:
        out = []
        for p in sorted(self.dir.iterdir(), reverse=True) if self.dir.is_dir() else []:
            rec = self.get(p.name)
            if rec:
                out.append(rec)
        return out

    def running(self, group: str) -> dict | None:
        for rec in self.list():
            if rec.get("group") == group and rec["status"] == "running" and (rec["id"] in self._procs
                                                                              or _alive(rec.get("pid"))):
                return rec
        return None

    def log_text(self, rec: dict, max_bytes: int = 2_000_000, tail_lines: int = 200) -> tuple[str, bool]:
        """The job's output (the whole of it for a diff, a decision or check-register, capped; else the tail)."""
        p = self.dir / rec["id"] / "output.log"
        try:
            size = p.stat().st_size
            with p.open("rb") as f:
                if size > max_bytes:
                    f.seek(size - max_bytes)
                data = f.read()
        except OSError:
            return "", False
        text = data.decode("utf-8", "replace")
        if rec.get("kind") in FULL_LOG:
            return text, size > max_bytes
        lines = text.splitlines()
        return "\n".join(lines[-tail_lines:]), len(lines) > tail_lines or size > max_bytes

    # ------------------------------------------------------------------ start and stop
    def start(self, kind: str, args: list[str], meta: dict | None = None) -> dict:
        if kind not in GROUPS:
            raise JobError(f"unknown job kind {kind!r}")
        if any(not isinstance(a, str) for a in args):
            raise JobError("every argument must be text")
        group = GROUPS[kind]
        with self._lock:
            busy = self.running(group)
            if busy:
                raise JobError(f"a {busy['kind']} job is running ({busy['id']}); one at a time for this kind of work. "
                               "Wait for it, or stop it on its page.")
            jid = f"{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%SZ}-{kind}-{secrets.token_hex(3)}"
            d = self.dir / jid
            d.mkdir(parents=True)
            argv = [self.python, "-m", "tenderpack", *args]
            if kind in NICE:                                      # session 13: a lower-priority job
                argv = ["nice", "-n", str(NICE[kind]), *argv]
            rec = {"id": jid, "kind": kind, "group": group, "argv": argv, "cwd": str(self.root),
                   "command": f"cd {shlex.quote(str(self.root))} && {shlex.join(argv)}",
                   "started": now_iso(), "finished": None, "status": "running", "exit_code": None, "pid": None,
                   "meta": meta or {}}
            env = dict(os.environ)
            env["PYTHONUNBUFFERED"] = "1"                         # the log shows progress as it happens
            with (d / "output.log").open("wb") as logf:
                proc = subprocess.Popen(argv, cwd=str(self.root), stdout=logf, stderr=subprocess.STDOUT,
                                        stdin=subprocess.DEVNULL, start_new_session=True, env=env)
            rec["pid"] = proc.pid
            self._procs[jid] = proc
            self._save(rec)
        threading.Thread(target=self._wait, args=(jid, proc), daemon=True, name=f"job-{jid}").start()
        return rec

    def _wait(self, jid: str, proc) -> None:
        code = proc.wait()
        with self._lock:
            rec = self.get(jid) or {}
            rec.update(finished=now_iso(), exit_code=code)
            if rec.get("stop_requested"):
                rec["status"] = "stopped"
            else:
                rec["status"] = "finished" if code == 0 else "failed"
            rec["meaning"] = meaning(rec.get("kind", ""), code)
            self._save(rec)
            self._procs.pop(jid, None)

    def stop(self, jid: str) -> dict:
        rec = self.get(jid)
        if not rec or rec["status"] != "running":
            raise JobError("that job is not running")
        rec["stop_requested"] = now_iso()
        self._save(rec)
        pid = rec.get("pid")

        def escalate():
            for sig, wait in ((signal.SIGINT, 20), (signal.SIGTERM, 10), (signal.SIGKILL, 0)):
                try:
                    os.killpg(int(pid), sig)
                except (OSError, ValueError, TypeError):
                    return
                t0 = time.time()
                while time.time() - t0 < wait:
                    if not _alive(pid) or (self.get(jid) or {}).get("status") != "running":
                        return
                    time.sleep(0.2)
        threading.Thread(target=escalate, daemon=True).start()
        return rec
