"""The AI workflow: from a new addendum PDF and the preceding tender state to isolated candidate A1-A5 outputs and a
review packet, every provision accounted for, resumable at any point, and nothing written to the real curation,
configuration or outputs.

    tenderpack ai run ADD-NN --pdf PATH [--route host|recorded|anthropic|openrouter|ollama] [--pack config/pack.yaml]
                     [--evidence build] [--run-id ID] [--batch-size N] ...
    tenderpack ai resume RUN_ID
    tenderpack ai submit-batch RUN_ID FILE --by NAME [--host-model M]       (the manual host path)

Steps (each checkpointed in staging/ai/runs/<run_id>/checkpoint.json; tenderpack/ai/checkpoint.py):
  ingest                 the candidate workspace (candidate.py: copies of the curation and configuration with the PDF
                         added) and `ingest` into candidate/build; a structural failure stops the run with the reason.
                         The pre-addendum outputs (candidate/out-before, the last validated state the review compares
                         with) start building in the background from the previous evidence build.
  readings               only when ingest refused the candidate for addendum image regions with no reading (C05 unread,
                         nothing else): one batch per region proposes a reading over the tools get_region and
                         validate_reading (regionread.py); the controller checks it (readings.check_reading; at most
                         interpretation_pending), writes it into the candidate's readings PENDING HUMAN REVIEW (no
                         approval), and ingest runs again; a region without a usable reading stops the run.
  analysis               bounded batches of provisions (in document order, a section kept together; every provision of
                         the addendum, cover lines, notes, table rows, form rows and image readings included). Each batch
                         is one controller run (controller.propose for the recorded and API routes; for the host route a
                         host session (hostsession.py) when the host CLI is there, else the batch's task packet is
                         written to the run folder and the run waits for `tenderpack ai submit-batch`). A provision is
                         pending -> proposed -> validated (or unaccounted when its batch answered nothing for it); a
                         resumed run skips what is done and never asks twice.
  validation             the items of every batch as ONE set through controller.validate_set (the controller's own
                         statuses and coverage); an op of a change type the engine does not have becomes an
                         escalation carrying its evidence (never forced into a known type).
  downstream             the deterministic impact of the promotable ops (downstream.py) as tasks: rows whose units
                         changed, obligations without rows (C46), clarification entries citing changed units, the A5
                         activities needing the changed rows, escalated provisions with their scope; proposals for them
                         in bounded batches (re-made readings, new rows, issues, draft clarification questions,
                         evidence items, activities, relationships).
  downstream_validation  downstream.validate over the combined downstream set in the candidate.
  promotion              into the CANDIDATE only: its op file (PROPOSED, origin assistant; every other provision
                         `unresolved` with the reason), rows, readings, issues, evidence items, templates, assumptions,
                         clarification entries and relationships (proposed).
  pin, check_register    `pin` and `check-register --update-ids` on the candidate (its own pins and id ledger).
  outputs                the pre-addendum outputs are joined (or built), the candidate is pre-flighted (the structural
                         checks that need no output) and `outputs` builds candidate/out; a refused build keeps
                         out-before as the last validated state. Every candidate output carries the banner
                         "CANDIDATE: proposed by the AI workflow; not reviewed; nothing accepted" and A1 a candidate
                         status column (proposed / unresolved / decided).
  diff                   `diff` from the previous stage to the addendum in the candidate, and out-before vs out.
  review                 staging/ai/runs/<run_id>/review/index.md and index.html: per provision the chain source
                         evidence -> proposed transition -> validation -> downstream impact -> output difference, the
                         unresolved and escalated first, the diff, the links, the timings and every manual step.
Nothing is approved, accepted, sent or published; the real curation/, config/ and out/ are only read.

Session 13. The run's code and policy identity (checkpoint.code_identity: git HEAD when available and whether the tree
is dirty, a content hash over tenderpack/**/*.py, config/*.yaml and pyproject.toml, the time) is recorded at start and
recomputed at every resume (and submit-batch); a different hash is refused (CodeChanged, exit 7) unless
--allow-code-change "<reason>" records the new segment, and run-status, the run log and the review packet then say
"segments ran on different code". An analysis row_new / row_reading item is carried to a downstream task keyed to its
provision (downstream.carry_analysis_rows); its provision is accounted for through that task (carried_answer) and a task
the downstream phase never answers is "unresolved: <reason>"; the packet lists such items under their own heading.

Session 13 (implementer D: speed without weaker checks; docs/AI_ROUTES.md sections 14 and 16):
  * kept answers: a host analysis session that reached submit_proposals is a completed answer (a 429 or a failure after
    it no longer discards it: requests.call_host), its MCP server records the submission at once
    (batches/<batch>.submission.json), and `resume` reuses it after revalidating it against the current evidence and
    state (_reuse_submission; the checkpoint's `submission`, or `reuse_refused` with the reason and the batch asked
    again). A SIGTERM is handled like Ctrl-C (Terminated): the running step and batch keep their elapsed time.
  * analysis batches planned by structure within the token budget (_plan_analysis, batching.plan_structured).
  * answers collected as they arrive (Prefetch: N exchanges running, up to 2N dispatched; one writer takes them in
    plan order) and what concurrency did recorded in the checkpoint's `concurrency`; scripts/bench_workflow.py prints a
    run's timing from its records (--from-run) or simulates the recorded run at 1, 2, 3 sessions at once.

Requests (session 11; tenderpack/ai/requests.py): every model request of every phase (readings, analysis, downstream,
the critic) on every route goes through ONE request layer: the phase's schema (native structured output where the
route supports it; validated locally always), a capability check before any call (the reading phase requires image
input), complete request accounting (a batch that does not fit is split by provision or task; a single one that does
not fit alone is escalated with its size; nothing is truncated), and three failure classes: a rate limit backs off
(bounded, with jitter) and then DEFERS the batch (status `deferred`; the run stops cleanly, exit 5, or continues, per
config failures.rate_limit.on_deferred); a provider failure is retried (bounded) and then fails the batch; a malformed
answer is re-asked once with the validation errors, and what still fails is set aside item by item (`malformed_items`).
Batches that succeeded are never asked again on resume. The selective critic reviews each analysis batch's selected
items after its validation, and each downstream batch's selected items in the `critic` step after the downstream
validation, in one request per batch; its findings are review.critic (analysis items) and downstream/critic.yaml
(downstream items); it changes no status, and agreement is not approval.

Session 12:
  * offline mode (tenderpack/ai/offline.py; `--offline`, config `offline: true`, TENDERPACK_OFFLINE=1): every phase on
    the local ollama route; a hosted route is refused at start (and every host session, hosted adapter and host
    critic refuses in its constructor); the models are checked against the local endpoint first (_ollama_preflight);
    the critic runs on routes.ollama.models.critic or is recorded `skipped` ("independent review did not run: ...",
    in the log, the checkpoint, the review packet and the candidate README); readings with a model that does not
    report vision are escalated to a person (_local_reading_check).
  * models per phase on ollama (config.phase_model): readings `vision`, the text phases `propose`/`text`/--model.
  * bounded concurrency (Prefetch; config concurrency.max_parallel_sessions, host and recorded routes only): the
    exchanges of up to N analysis or downstream batches run in worker threads under ONE run-scoped addendum lock and a
    shared rate-limit gate (requests.RateGate); everything else (packets, validation, checkpoints, the critic) stays in
    the run's thread, in plan order, so the result is the sequential result.
  * the shared part of every packet is sent smaller (requests.compact_shared).
  * consecutive addenda (`run ADD-04 --pdf ... --base-run RUN_ID`, and `resume RUN_ID --base-run RUN_ID`): the
    candidate starts from the BASE RUN's candidate (candidate.base_run / create(base=...)): its curation as promoted
    (op files, rows, readings, issues, clarifications, relationships, pins, triggers), its pack with the base
    addendum's PDF and its evidence build, so the base addendum is the previous stage. The base must have reached
    promotion and must not be running (its run lock); it is read, never written. The state identity carries the base
    run id and the base candidate's fingerprint (a changed base makes this run's sets STALE). out-before, the diff
    and the review compare with the base candidate's state; run-status, the settings, the review packet and the
    candidate README name the base. A run whose addendum skips addenda the state does not hold (ADD-04 on a state
    ending at ADD-02) records them (`missing_addenda`), and a provision citing one of them that is not answered is
    unresolved with the reason "ADD-03 is not in this state; run it first or pass --base-run".
"""
from __future__ import annotations

import datetime as dt
import html
import json
import os
import random
import re
import secrets
import shutil
import signal
import threading
import time
import traceback
import typing
from collections import Counter
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

import yaml

from .. import human_owned as HO
from ..util import ROOT, load_yaml, sha256_file
from . import answers as ANS               # session 14 (W5): the owner's answers, taken at safe checkpoints
from . import budget as B
from . import candidate as CAND
from . import config as C
from . import controller
from . import downstream as DS
from . import offline as OFF
from . import policy
from . import regionread as RR
from . import requests as R
from .checkpoint import STEPS, Checkpoint, RunLock, RunLockError, code_identity, now_iso
from .contract import DOWNSTREAM_TASK, DownstreamSet, ProposalSet
from .runlog import RunLog
from .tools import Workspace

ROUTES = ("recorded", "host", "anthropic", "openrouter", "ollama")
PARALLEL_ROUTES = ("host", "recorded")            # session 12: where batches may ask their sessions at once
MAX_PARALLEL = 4
API_ROUTES = ("anthropic", "openrouter", "ollama")
TARGET_MIN = 30.0
EXIT_CODES = {"complete": 0, "partial": 0, "stopped": 0, "waiting_for_host": 4, "failed": 1, "refused": 2,
              "deferred": 5}
STOP_FOR_PERSON = 6                                # session 12: `stopped` because the run cannot go on by itself
CODE_CHANGED_EXIT = 7                              # session 13: a resume refused because the code changed since
CODE_ROOT = ROOT                                   # session 13: the tree whose identity a run records (tests: a copy)
DIFFERENT_CODE = "segments ran on different code"
RUNNABLE = ("pending", "deferred")                 # batch states a drive asks (a deferred batch: a rate limit)


class WaitingForHost(Exception):
    pass


class CodeChanged(B.Refused):
    """Session 13: a resume (or a submission that continues a run) on code other than the run's last segment's."""
    exit_code = CODE_CHANGED_EXIT


def _short_id(i: dict | None) -> str:
    if not i:
        return "not recorded"
    g = (f"git {i['git_head'][:12]}" + (" (dirty tree)" if i.get("git_dirty") else "")) if i.get("git_head") \
        else "git not available"
    return f"content {i['content_sha256'][:16]}… over {i.get('files')} files; {g}; recorded {i.get('recorded')}"


def record_code_identity(cp: Checkpoint) -> dict:
    """At run start (session 13): the code and policy identity (checkpoint.code_identity of CODE_ROOT) in the
    checkpoint, as the run's first segment."""
    ident = code_identity(CODE_ROOT)
    cp.data["code_identity"] = {"start": ident, "segments": [dict(ident, segment=1, reason="run started")],
                                "differ": False}
    cp.save()
    return ident


def check_code_identity(cp: Checkpoint, allow_code_change: str | None = None) -> dict:
    """At every resume (session 13): recompute the identity and compare its content hash with the last segment's. The
    same code: the segment is recorded. Different code: refused (CodeChanged, exit CODE_CHANGED_EXIT) unless
    `allow_code_change` gives a reason; then the new identity, the reason and the time are recorded as a checkpoint
    event and the run says DIFFERENT_CODE from then on (run-status, the run log, the review packet header). A run
    started before session 13 has no recorded identity: the current one is recorded and the earlier segments' code is
    said to be unknown (never assumed equal)."""
    now = code_identity(CODE_ROOT)
    ci = cp.data.get("code_identity")
    if not ci:
        cp.data["code_identity"] = {"start": None, "segments": [dict(now, segment=1, reason="first recorded on resume: "
                                                                     "the code of the earlier segments is unknown")],
                                    "differ": True, "unknown_before": True}
        cp.event("code_identity_recorded", now=now, note="not recorded when the run started (before session 13)")
        return now
    last = ci["segments"][-1] if ci.get("segments") else ci.get("start") or {}
    reason = (allow_code_change or "").strip()
    if now["content_sha256"] == last.get("content_sha256"):
        ci["segments"].append(dict(now, segment=len(ci["segments"]) + 1, reason="resumed on the same code"))
        cp.save()
        return now
    if not reason:
        raise CodeChanged(
            f"run {cp.data['run_id']}: the code changed since its last segment ({_short_id(last)} -> {_short_id(now)}). "
            "A benchmark is not continued silently on changed code: resume with --allow-code-change \"<reason>\" to "
            "record the change (the run then says that its segments ran on different code), or start a new run")
    ci["segments"].append(dict(now, segment=len(ci["segments"]) + 1, reason=reason))
    ci["differ"] = True
    cp.event("code_changed", before=last, now=now, reason=reason)
    return now


def code_lines(cp: Checkpoint) -> list[str]:
    """The run's code identity for the review packet header and run-status (session 13)."""
    ci = cp.data.get("code_identity") or {}
    if not ci:
        return ["- code: not recorded (a run started before session 13)"]
    segs = ci.get("segments") or []
    L = [f"- code at start: {_short_id(ci.get('start'))}"]
    if ci.get("differ"):
        L.append(f"- **{DIFFERENT_CODE}**: " + "; ".join(f"segment {x.get('segment')}: {_short_id(x)} ({x.get('reason')})"
                                                      for x in segs))
    return L


class Terminated(KeyboardInterrupt):
    """Session 13 (D; blind-05 regression defect 1): SIGTERM, raised in the run's thread like Ctrl-C, so that the
    checkpoint records the running step's and batch's elapsed time and the batches in flight as interrupted (the run
    used to die at once with its analysis step "0.0 s running"). The host sessions in flight are stopped; one that had
    already submitted is reused on resume after revalidation (_reuse_submission), one that had not is asked again."""


def _on_sigterm(signum, frame):
    raise Terminated(f"signal {signum} (SIGTERM): the run was asked to stop")


class StopRun(Exception):
    """`code` (session 12): the exit code of a `stopped` run: 0 only for a stop that was asked for (--stop-after), 2 for
    a structural ingest refusal (as documented), else 6 (STOP_FOR_PERSON: the run cannot go on until a person acts)."""

    def __init__(self, status: str, reason: str, code: int | None = None):
        super().__init__(reason)
        self.status, self.reason, self.code = status, reason, code


class BatchFailed(Exception):
    pass


class Deferred(Exception):
    """A rate limit outlasted the bounded backoff (requests.RateLimited): the batch is deferred, not failed."""

    def __init__(self, message: str, reset_in_s: float | None = None):
        super().__init__(message)
        self.message, self.reset_in_s = message, reset_in_s


def _short(t, n: int = 300) -> str:
    t = " ".join(str(t or "").split())
    return t if len(t) <= n else t[: n - 1] + "…"


def runs_dir(staging) -> Path:
    return Path(staging).absolute() / "runs"


def new_run_id(addendum: str, route: str) -> str:
    return f"{addendum}-run-{route}-{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%SZ}-{secrets.token_hex(2)}"


# ---------------------------------------------------------------------------------------------- recorded cassettes

class WorkflowCassette:
    """A recorded workflow (hand-written; NOT a live model's output): `sessions`, each the turns of one batch.

        name, model, capabilities                    as a provider cassette (providers/recorded.py)
        sessions:
          - phase: reading | analysis | downstream | critic
            when: {regions_include: [region id]} | {provisions_include: [unit ids]} | {tasks_include: [task ids]}
                  | {items_include: [item ids]}       (critic: the ids of the items selected for one batch's review)
            turns: [...]                              the RecordedProvider turns of that batch
    A batch takes the first unused session of its phase whose `when` holds; a batch no session covers fails with
    "no recorded session" and its provisions stay pending (a resumed run asks again). A batch's critic with no recorded
    session is `skipped` with that reason (visible), never failed."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.data = load_yaml(self.path) or {}
        self.sessions = list(self.data.get("sessions") or [])

    def provider(self, phase: str, keys: list[str], used: set[int]):
        from .providers.recorded import RecordedProvider
        for i, s in enumerate(self.sessions):
            if i in used or s.get("phase") != phase:
                continue
            w = s.get("when") or {}
            need = (list(w.get("provisions_include") or []) + list(w.get("tasks_include") or [])
                    + list(w.get("regions_include") or []) + list(w.get("items_include") or []))
            if all(k in keys for k in need):
                p = RecordedProvider({"name": f"{self.data.get('name')}#{i}", "model": s.get("model") or self.data.get("model"),
                                      "capabilities": self.data.get("capabilities"), "turns": s.get("turns") or []})
                p.cassette_path = f"{self.path}#session{i}"
                return p, i
        return None, None


# ---------------------------------------------------------------------------------------------- the run context

class Ctx:
    def __init__(self, cp: Checkpoint, echo=print, sleep=time.sleep):
        self.cp, self.echo, self.sleep = cp, echo, sleep
        self.s = cp.data["settings"]
        self.dir = cp.path.parent
        self.P = CAND.paths(self.dir)
        self.addendum = cp.data["addendum"]
        self.run_id = cp.data["run_id"]
        self.log = RunLog(self.run_id, [self.dir / "log.jsonl", Path(self.s["worklog"]) / f"{self.run_id}.jsonl"])
        self._ws = self._cfg = self._cassette = self._promoted = None
        self.before_proc = None
        self.stop_batches: str | None = None
        self.prefetch: "Prefetch | None" = None          # session 12: batches at once (max_parallel_sessions > 1)
        self.gate: "R.RateGate | None" = None
        self.run_lock = None
        self.stop_pending: "StopRun | None" = None

    @property
    def ws(self) -> Workspace:
        if self._ws is None:
            self._ws = Workspace(self.P["build"], self.P["pack"], ROOT, self.dir / "ai", Path(self.s["worklog"]),
                                 Path(self.s["ai_config"]) if self.s.get("ai_config") else None)
        return self._ws

    @property
    def cfg(self) -> dict:
        if self._cfg is None:
            self._cfg = C.load(Path(self.s["ai_config"]) if self.s.get("ai_config") else None)
            src = self.s.get("offline") or OFF.requested(self._cfg)        # session 12: offline mode, kept on resume
            if src:
                OFF.activate(self._cfg, src)
            if self.s.get("allow_unverified_capabilities"):
                from .providers.base import ALLOW_UNVERIFIED_KEY
                self._cfg[ALLOW_UNVERIFIED_KEY] = True
        return self._cfg

    @property
    def cassette(self) -> WorkflowCassette:
        if self._cassette is None:
            if not self.s.get("cassette"):
                raise B.Refused("the recorded route needs --cassette (a recorded workflow; not a live integration)")
            self._cassette = WorkflowCassette(Path(self.s["cassette"]))
        return self._cassette

    def say(self, msg: str, **data) -> None:
        self.echo(msg)
        self.log.event("say", message=msg, **data)

    def used_sessions(self) -> set[int]:
        used = {b["session"] for b in self.cp.data["batches"].values() if b.get("session") is not None
                and b["status"] in ("done", "running")}
        used |= {(b.get("critic") or {}).get("session") for b in self.cp.data["batches"].values()
                 if (b.get("critic") or {}).get("status") == "done"} - {None}
        used |= {c.get("session") for c in (self.cp.data["downstream"].get("critic") or {}).values()
                 if c.get("status") == "done"} - {None}
        if self.prefetch is not None:                     # sessions reserved by batches asked ahead (session 12)
            used |= {r.get("session") for r in self.prefetch.recs.values()} - {None}
        return used

    def remaining_caps(self) -> dict:
        """The run's caps (config, then the command line) less what the batches used so far: the caps bound the whole
        workflow run, not each batch."""
        route = self.s["route"]
        if route == "host":
            return {}
        caps = C.caps(self.cfg, route, self.s.get("caps") or {})
        used = self.cp.data["usage"]
        out = {k: v for k, v in (self.s.get("caps") or {}).items() if v is not None}
        for k, u in (("max_calls", used["calls"]), ("max_input_tokens", used["input_tokens"]),
                     ("max_output_tokens", used["output_tokens"])):
            if caps.get(k) is not None:
                out[k] = max(0, int(caps[k]) - int(u))
        if caps.get("max_usd") is not None and used.get("cost_usd") is not None:
            out["max_usd"] = max(0.0, float(caps["max_usd"]) - float(used["cost_usd"]))
        return out

    def combined(self) -> tuple[ProposalSet, dict]:
        return _load_staged(self.ws, f"{self.run_id}-combined")

    def promoted(self, fresh: bool = False) -> dict:
        if self._promoted is None or fresh:
            self.ws.refresh()
            self._promoted = DS.promoted_ops(self.ws, self.combined()[0])
        return self._promoted

    # ------------------------------------------------------------------ requests (session 11)
    @property
    def policy(self) -> R.FailurePolicy:
        """The failure policy (config failures, then the run's caps for provider retries); after a deferral in this
        drive a rate-limited request is tried once and deferred without backoff (more sessions do not lift a limit)."""
        route = self.s["route"]
        caps = C.caps(self.cfg, route, self.s.get("caps") or {}) if route != "host" else {}
        p = R.FailurePolicy.from_cfg(self.cfg, caps)
        p.after_deferral = bool(getattr(self, "deferred_in_drive", None))
        p.gate = self.gate
        return p

    @property
    def rng(self) -> random.Random:
        if getattr(self, "_rng", None) is None:
            seed = (self.cfg.get("failures") or {}).get("rate_limit", {}).get("seed")
            self._rng = random.Random(seed)
        return self._rng

    def notices(self, bid: str, notes: list[dict]) -> None:
        """Route notices of a batch: on the batch and in the run's list (checkpoint; the review packet shows them)."""
        if not notes:
            return
        b = self.cp.batch(bid)
        b["notices"] = [n for n in notes]
        allx = self.cp.data.setdefault("notices", [])
        for n in notes:
            rec = {"batch": bid, **{k: v for k, v in n.items() if k != "capabilities"}}
            if rec not in allx:
                allx.append(rec)
                self.log.event("route_notice", **rec)


class Prefetch:
    """Session 12: bounded concurrency of a run's analysis and downstream batches (concurrency.max_parallel_sessions).

    The run's own thread plans, dispatches and TAKES every batch in plan order, exactly as one at a time; only the
    exchange with the model (a host session, or a provider conversation) runs in a worker thread, at most `n` at once.
    A worker touches no checkpoint, no candidate input and no other batch's files (its own staging folder and log).
    When the batch's turn comes, its packet is built again; the worker's answer is used only when that packet is the
    one the worker sent (otherwise it is discarded, recorded, and the batch is asked as usual), so the result is the
    sequential result. A deferral stops new dispatches; the batches already asked are taken, then the run stops.

    Session 13 (D): answers are COLLECTED as they arrive and wait (at most `lookahead` dispatched batches in all)
    without holding a worker: `n` bounds the exchanges RUNNING at once, so a worker whose answer came back early takes
    the next batch while the run's thread still waits for an earlier one (take() dispatches more while it waits). The
    run's thread stays the ONE writer: it validates and applies the answers in plan order (deterministic whatever the
    arrival order). `meter` records, per phase, what concurrency did (running at most, busy and held seconds,
    batches dispatched before the first answer was taken, discards) into the checkpoint's `concurrency`."""

    def __init__(self, ctx: "Ctx", n: int):
        self.ctx, self.n = ctx, int(n)
        self.lookahead = 2 * self.n
        self.pool = ThreadPoolExecutor(max_workers=self.n, thread_name_prefix="tenderpack-batch")
        self.recs: dict[str, dict] = {}
        self.tried: set[str] = set()
        self.discarded: list[str] = []
        self.refill = None
        self.meter: dict[str, dict] = {}
        self._lock = threading.Lock()

    @staticmethod
    def key(packet: dict) -> str:
        import hashlib
        return hashlib.sha256(json.dumps(packet, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()

    def running(self) -> int:
        return sum(1 for r in self.recs.values() if not r["future"].done())

    def full(self) -> bool:
        return self.running() >= self.n or len(self.recs) >= self.lookahead

    def _m(self, phase: str) -> dict:
        return self.meter.setdefault(phase, {"dispatched": 0, "taken": 0, "discarded": 0, "max_running": 0,
                                             "busy_s": 0.0, "held_s": 0.0,
                                             "dispatched_before_first_take": None, "first_dispatch": None,
                                             "last_done": None})

    def submit(self, bid: str, rec: dict) -> None:
        work = rec.pop("work")
        phase = self.ctx.cp.data["batches"].get(bid, {}).get("phase", "analysis")
        rec["phase"] = phase

        def run():
            rec["t_start"] = time.monotonic()
            try:
                return ("ok", work())
            except BaseException as e:                      # noqa: BLE001 (handed to the run's thread as is)
                return ("exc", e)
            finally:
                rec["t_done"] = time.monotonic()
                with self._lock:
                    m = self._m(phase)
                    m["busy_s"] += rec["t_done"] - rec.get("t_start", rec["t_done"])
                    m["last_done"] = rec["t_done"]
        rec["t_dispatch"] = time.monotonic()
        rec["future"] = self.pool.submit(run)
        self.recs[bid] = rec
        with self._lock:
            m = self._m(phase)
            m["dispatched"] += 1
            m["first_dispatch"] = m["first_dispatch"] or rec["t_dispatch"]
            m["max_running"] = max(m["max_running"], self.running())
        self.ctx.log.event("batch_asked_ahead", batch=bid, in_flight=len(self.recs), running=self.running())

    def peek(self, bid: str) -> dict | None:
        return self.recs.get(bid)

    def take(self, bid: str, key: str) -> dict | None:
        rec = self.recs.get(bid)
        if rec is None:
            return None
        fut = rec["future"]
        while not fut.done():                    # session 13: the other workers are kept busy meanwhile
            # refill BEFORE waiting too: an answer that came back while this thread built the batch's packet has
            # already freed its worker (otherwise that worker idles until this batch is taken)
            if self.refill is not None and not self.full():
                try:
                    self.refill()
                except Exception as e:                           # noqa: BLE001 (the batches are asked in their turn)
                    self.ctx.log.event("prefetch_refill_failed", error=f"{type(e).__name__}: {_short(str(e), 300)}")
            if fut.done():
                break
            others = [r["future"] for k, r in self.recs.items() if k != bid and not r["future"].done()]
            wait([fut, *others], return_when=FIRST_COMPLETED)
            with self._lock:
                self._m(rec["phase"])["max_running"] = max(self._m(rec["phase"])["max_running"], self.running())
        self.recs.pop(bid, None)
        kind, val = fut.result()
        now = time.monotonic()
        with self._lock:
            m = self._m(rec["phase"])
            m["taken"] += 1
            if m["dispatched_before_first_take"] is None:
                m["dispatched_before_first_take"] = m["dispatched"]
            m["held_s"] += max(0.0, now - rec.get("t_done", now))
        b = self.ctx.cp.data["batches"].get(bid)
        if b is not None and rec.get("t_start") is not None:
            b["session_seconds"] = round(rec.get("t_done", now) - rec["t_start"], 3)     # the exchange in its worker
        if rec["key"] != key:
            self.discarded.append(bid)
            with self._lock:
                self._m(rec["phase"])["discarded"] += 1
            self.ctx.cp.event("prefetch_discarded", batch=bid, reason="the batch's packet changed before its turn "
                                                                      "(an earlier batch answered part of it); asked "
                                                                      "again as usual")
            return None
        rec["kind"], rec["value"] = kind, val
        return rec

    @staticmethod
    def result(rec: dict):
        if rec["kind"] == "exc":
            raise rec["value"]
        return rec["value"]

    def record(self) -> dict:
        """What concurrency did in this drive, per phase (the checkpoint's `concurrency`; scripts/bench_workflow.py)."""
        out = {}
        with self._lock:
            for phase, m in self.meter.items():
                window = ((m["last_done"] or 0) - (m["first_dispatch"] or 0)) if m["first_dispatch"] else 0.0
                out[phase] = {"max_parallel_sessions": self.n, "lookahead": self.lookahead,
                              "dispatched": m["dispatched"], "taken": m["taken"], "discarded": m["discarded"],
                              "max_running": m["max_running"], "busy_s": round(m["busy_s"], 3),
                              "held_s": round(m["held_s"], 3), "window_s": round(max(window, 0.0), 3),
                              "idle_slots_s": round(max(0.0, self.n * max(window, 0.0) - m["busy_s"]), 3),
                              "dispatched_before_first_take": m["dispatched_before_first_take"]}
        return out

    def close(self, interrupted: bool = False) -> None:
        # session 13 (D): an interrupted run does not wait for the exchanges in flight (their host sessions were
        # stopped; a submission already made is reused on resume); otherwise the workers finish first
        self.pool.shutdown(wait=not interrupted, cancel_futures=True)
        conc = self.ctx.cp.data.setdefault("concurrency", {})
        recs = self.record()
        for phase, rec in recs.items():
            conc[phase] = {**rec, "drive": now_iso()}
        # session 14 (W2; blind-07 defect 15): `concurrency` keeps the last drive (as before); every drive (segment) is
        # kept in `concurrency_drives`, so a resumed run's first segment is not lost
        if recs:
            drives = self.ctx.cp.data.setdefault("concurrency_drives", [])
            seg = segment_number(self.ctx.cp.data)          # session 14 (N6): the segment's own number (its event)
            if drives and int(drives[-1].get("segment") or 0) >= seg:
                seg = int(drives[-1]["segment"]) + 1         # a second drive in one segment (no event): the next one
            drives.append({"drive": now_iso(), "segment": seg, "interrupted": bool(interrupted), "phases": recs})
        # session 13 (blind-07 scorer, defect 15): a batch answered through its staged submission (_reuse_submission)
        # is never take()n, so its record stays here although the batch is done; only the batches still pending are
        # "not taken"
        batches = self.ctx.cp.data.get("batches") or {}
        left = sorted(b for b in self.recs if (batches.get(b) or {}).get("status") not in ("done", "skipped"))
        if left:
            self.ctx.cp.event("prefetch_not_taken", batches=left,
                              reason="the run stopped before their answers were taken; they stay pending and are asked "
                                     "again on resume")
        self.recs.clear()


def _fill(ctx: "Ctx", phase: str, start: str, **kw) -> None:
    """Dispatch the batches of `phase` from `start` on (plan order) while fewer than `n` exchanges run and fewer than
    `lookahead` answers are dispatched and not yet taken (session 12; session 13: answers waiting to be taken no longer
    hold a worker). While the run's thread waits for a batch's answer, Prefetch.take calls this again (`refill`)."""
    pf = ctx.prefetch
    if pf is None or ctx.stop_batches or ctx.stop_pending is not None:
        return
    pf.refill = lambda: _fill(ctx, phase, start, **kw)
    keys = ctx.cp.batches(phase)
    for k in keys[keys.index(start):] if start in keys else []:
        if pf.full():
            break
        if k in pf.recs or k in pf.tried or ctx.cp.batch(k)["status"] not in ("pending", "deferred"):
            continue
        pf.tried.add(k)
        try:
            rec = (_prep_analysis(ctx, k) if phase == "analysis" else _prep_downstream(ctx, k, **kw))
        except Exception as e:                                   # noqa: BLE001 (the batch then runs in its turn)
            ctx.log.event("prefetch_skipped", batch=k, error=f"{type(e).__name__}: {_short(str(e), 300)}")
            rec = None
        if rec is not None:
            pf.submit(k, rec)


def _load_staged(ws: Workspace, run_id: str) -> tuple[ProposalSet, dict]:
    f = B.safe_staging(ws.staging, ws.root, ws.evidence) / run_id / "proposals.yaml"
    d = load_yaml(f) or {}
    return ProposalSet.model_validate(d["proposal_set"]), d.get("controller") or {}


def _hostsession():
    try:
        from . import hostsession
    except ImportError:
        return None
    return hostsession if hasattr(hostsession, "HostSession") else None


# ---------------------------------------------------------------------------------------------- start / resume

def start(addendum: str, pdf, route: str = "recorded", pack=None, evidence=None, staging=None, worklog=None,
          ai_config=None, run_id: str | None = None, batch_size: int = 8, downstream_batch_size: int = 12,
          model: str | None = None, cassette=None, caps: dict | None = None, host_model: str | None = None,
          host_mode: str = "auto", host_session_model: str | None = None,
          allow_unverified_capabilities: bool = False, stop_after: str | None = None, background_before: bool = True,
          cache: bool = True, echo=print, sleep=time.sleep, offline: bool = False, base_run: str | None = None) -> dict:
    """Start a run (see the module docstring). Refuses (budget.Refused / candidate.CandidateError) before creating
    anything when the inputs cannot work.

    Session 12: `base_run` (consecutive addenda) starts the candidate from that run's candidate: the pack and the
    evidence build are the base run's (so `pack` and `evidence` must not be given too); the base must have reached
    promotion and must not be running (candidate.base_run refuses with the reason).

    Session 12: `offline` (or config `offline: true`, or TENDERPACK_OFFLINE=1) is offline mode (tenderpack/ai/offline.py):
    the route must be ollama (a hosted route raises OfflineError, a ConfigError, before anything is created), and on the
    ollama route the models are checked against the local endpoint first (`_ollama_preflight`: installed, tool use,
    context, estimated memory; a missing model is named with the `ollama pull` command a person may run)."""
    cfg_off = C.load(Path(ai_config) if ai_config else None)
    off_src = OFF.requested(cfg_off, offline)
    if off_src:
        OFF.activate(cfg_off, off_src)
        OFF.check_run_route(cfg_off, route)
    if route not in ROUTES:
        raise B.Refused(f"unknown route {route!r} ({', '.join(ROUTES)})")
    if stop_after and stop_after not in STEPS:
        raise B.Refused(f"--stop-after must be one of {', '.join(STEPS)}")
    if route == "recorded" and not cassette:
        raise B.Refused("the recorded route needs --cassette (a recorded workflow; not a live integration)")
    if int(batch_size) < 1 or int(downstream_batch_size) < 1:
        raise B.Refused("batch sizes must be at least 1")
    cfg0 = C.load(Path(ai_config) if ai_config else None)
    if int((cfg0.get("concurrency") or {}).get("batches") or 1) != 1:
        raise B.Refused("config/ai.yaml concurrency.batches must be 1: the workflow runs its batches one at a time "
                        "(concurrent sessions do not lift a plan's rate limit; they reach it sooner)")
    try:
        R.FailurePolicy.from_cfg(cfg0)
    except C.ConfigError as e:
        raise B.Refused(f"config/ai.yaml failures: {e}") from None
    n_par = parallel_sessions(cfg0, route)
    staging = Path(staging or ROOT / "staging/ai").absolute()
    worklog = Path(worklog or ROOT / "worklog/model_calls").absolute()
    base = None
    if base_run:                                   # session 12: consecutive addenda
        if pack is not None or evidence is not None:
            raise B.Refused("--base-run takes the preceding state (the pack and the evidence build) from the base run's "
                            "candidate: do not pass --pack or --evidence with it")
        base = CAND.base_run(runs_dir(staging), B.check_run_id(base_run))
        pack, evidence = Path(base["pack"]), Path(base["build"])
    pack = Path(pack or ROOT / "config/pack.yaml").absolute()
    evidence = Path(evidence or ROOT / "build").absolute()
    CAND.check(pack, addendum, Path(pdf))
    missing = missing_addenda(pack, addendum)
    # with a base run the evidence build is the base candidate's, inside the runs folder: THIS run's folder must not
    # overlap it (it is read, never written)
    rd = B.safe_staging(runs_dir(staging), ROOT, None if base else evidence)
    run_id = B.check_run_id(run_id or new_run_id(addendum, route))
    if base:
        B.safe_staging(rd / run_id, ROOT, evidence)
    if (rd / run_id).exists():
        raise B.Refused(f"run {run_id} exists ({rd / run_id}): resume it with `tenderpack ai resume {run_id}`")
    preflight = None
    if route not in ("recorded", "host"):
        cfg = C.load(Path(ai_config) if ai_config else None)
        rcfg = C.route(cfg, route)
        mdl = C.phase_model(rcfg, route, "analysis", model)
        B.check_startable(route, rcfg, C.caps(cfg, route, caps), B.price_for(cfg, mdl or ""))
        if route == "ollama":
            preflight = _ollama_preflight(cfg_off, model)
    settings = {"addendum": addendum, "pdf": str(Path(pdf).absolute()), "route": route, "pack": str(pack),
                "evidence": str(evidence), "staging": str(staging), "worklog": str(worklog),
                "ai_config": str(Path(ai_config).absolute()) if ai_config else None, "batch_size": int(batch_size),
                "downstream_batch_size": int(downstream_batch_size), "model": model,
                "cassette": str(Path(cassette).absolute()) if cassette else None,
                "caps": {k: v for k, v in (caps or {}).items() if v is not None}, "host_model": host_model,
                "host_mode": host_mode, "host_session_model": host_session_model,
                "allow_unverified_capabilities": bool(allow_unverified_capabilities),
                "background_before": bool(background_before), "cache": bool(cache), "offline": off_src,
                "ollama_preflight": preflight, "max_parallel_sessions": n_par,
                "base_run": base, "missing_addenda": missing}
    cp = Checkpoint.new(rd / run_id / "checkpoint.json", run_id=run_id, addendum=addendum, settings=settings,
                        inputs={"pack": str(pack), "evidence": str(evidence)}, candidate={})
    record_code_identity(cp)                       # session 13: the code and policy identity of the run's first segment
    cp.event("started", by_pid=os.getpid(), **({"offline": off_src} if off_src else {}),
             **({"base_run": base["run_id"], "base_fingerprint": base["fingerprint"]} if base else {}))
    if base:
        echo(f"[{run_id}] base run {base['run_id']}: the candidate starts from its candidate "
             f"({' -> '.join(base['chain'])}); {addendum} follows {base['addendum']}")
    if missing:
        echo(f"[{run_id}] WARNING: {missing_reason(missing)} ({addendum} follows "
             f"{_last_addendum(pack) or 'BASE'} in this state)")
    return _drive(cp, stop_after, echo, sleep)


def _last_addendum(pack: Path) -> str | None:
    nums = [int(CAND.ADDENDUM.match(str(d.get("doc_id"))).group(1)) for d in (load_yaml(pack) or {}).get("documents") or []
            if CAND.ADDENDUM.match(str(d.get("doc_id")))]
    return f"ADD-{max(nums):02d}" if nums else None


def missing_addenda(pack: Path, addendum: str) -> list[str]:
    """Session 12: the addenda between the state's last addendum and `addendum` that the state does not hold (ADD-04
    on a state ending at ADD-02: ["ADD-03"])."""
    m = CAND.ADDENDUM.match(addendum or "")
    last = _last_addendum(pack)
    if not m:
        return []
    lo = int(last.split("-")[1]) if last else 0
    return [f"ADD-{k:02d}" for k in range(lo + 1, int(m.group(1)))]


def missing_reason(missing: list[str]) -> str:
    return "; ".join(f"{a} is not in this state; run it first or pass --base-run" for a in missing)


_ADD_NO = re.compile(r"\bAddendum No\.? ?(\d+)\b", re.I)


def cites_missing(ctx: "Ctx", p: str, items: list) -> list[str]:
    """Session 12: the missing addenda (settings missing_addenda) a provision cites: by its own words ("Addendum No. 3")
    or by a unit id one of its items names (a target, an anchor, an evidence unit: "VOL-I:6.7+ADD-03", "ADD-03:2.1")."""
    missing = list(ctx.s.get("missing_addenda") or [])
    if not missing:
        return []
    text = ((ctx.ws.units_by_id.get(p) or {}).get("text") or "")
    named = {f"ADD-{int(n):02d}" for n in _ADD_NO.findall(text)}
    for it in items:
        blob = json.dumps({"target": getattr(it, "target", None), "payload": it.payload,
                           "evidence": [e.unit_id for e in it.evidence]}, ensure_ascii=False, default=str)
        named |= {a for a in missing if re.search(rf"(?:\+|\b){a}(?::|\b)", blob)}
    return [a for a in missing if a in named]


def parallel_sessions(cfg: dict, route: str) -> int:
    """config concurrency.max_parallel_sessions (session 12): 1..4; above 1 only on the host and recorded routes (see
    config/ai.yaml). Raises budget.Refused with the reason."""
    n = (cfg.get("concurrency") or {}).get("max_parallel_sessions", 1)
    if not isinstance(n, int) or isinstance(n, bool) or not 1 <= n <= MAX_PARALLEL:
        raise B.Refused(f"config/ai.yaml concurrency.max_parallel_sessions must be between 1 and {MAX_PARALLEL}, "
                        f"not {n!r}")
    if n > 1 and route not in PARALLEL_ROUTES:
        why = ("the paid API routes check the run's caps per request, so requests at once could overrun them"
               if route in ("anthropic", "openrouter") else
               "local inference shares one machine: requests at once multiply the KV cache in the same memory")
        raise B.Refused(f"config/ai.yaml concurrency.max_parallel_sessions is {n}: batches at once run only on the "
                        f"host route (and the recorded test route); not on {route}: {why}. Set it to 1")
    return n


def _ollama_preflight(cfg: dict, model: str | None) -> dict:
    """Session 12: the ollama route's models checked against the LOCAL endpoint before a run starts (never pulled):
    the analysis model must be installed (/api/tags), report tool use, and hold its context bound in the configured
    machine's memory (an estimate); the other roles (vision for the readings, critic) are checked and recorded, and a
    missing one is handled where it is needed (readings escalated to a person; the review recorded as skipped).
    Raises ConfigError with the exact reason."""
    from .providers import make
    from .providers.base import ProviderError
    from .providers.ollama import check_models, not_installed_message
    rcfg = C.route(cfg, "ollama")
    need = C.phase_model(rcfg, "ollama", "analysis", model)
    if not need:
        raise C.ConfigError("the ollama route needs a model: --model, or routes.ollama.models.propose (or text) in "
                            "config/ai.yaml")
    rep = check_models(cfg)
    if not rep["reachable"]:
        raise C.ConfigError(f"{rep.get('error')}: is Ollama running on this machine (`ollama serve`)? The ollama "
                            "route runs on the owner's Mac only")
    if need not in (rep["installed"] or []):
        raise C.ConfigError(not_installed_message(need, rep["installed"]))
    try:
        caps = make("ollama", need, cfg).capabilities()
    except ProviderError as e:
        raise C.ConfigError(f"the analysis model {need}: {e.message}") from None
    if caps.tools is not True:
        raise C.ConfigError(f"the analysis model {need} does not report tool use (/api/show capabilities "
                            f"{caps.details.get('reported_capabilities')}); the analysis phase offers tools: refused, "
                            "never assumed")
    return {"checked": now_iso(), "base_url": rep["base_url"], "installed": rep["installed"], "analysis_model": need,
            "analysis_capabilities": {"images": caps.images, "tools": caps.tools, "context_tokens": caps.context_tokens,
                                      "memory": caps.details.get("memory")},
            "models": rep["models"], "note": "checked against the local endpoint at start; nothing was pulled"}


def load(run_id: str, staging=None) -> Checkpoint:
    staging = Path(staging or ROOT / "staging/ai").absolute()
    p = runs_dir(staging) / B.check_run_id(run_id) / "checkpoint.json"
    if not p.exists():
        raise B.Refused(f"no run {run_id} under {runs_dir(staging)}")
    return Checkpoint.load(p)


def resume(run_id: str, staging=None, stop_after: str | None = None, retry_failed: bool = True, echo=print,
           sleep=time.sleep, from_step: str | None = None, offline: bool = False, base_run: str | None = None,
           allow_code_change: str | None = None, by_person: bool = True) -> dict:
    """Continue a stopped, interrupted, failed or waiting run from its checkpoint. Done steps and batches are skipped;
    a batch that failed is asked again (`retry_failed`), and the steps after it are recomputed from the candidate as it
    was before any promotion.

    `from_step` (session 11): rerun that step and every later one even when they are done, e.g. after a code change
    (the blind-04 run whose outputs build was refused). Batches that succeeded are NEVER asked again: a batch step named
    here only recomputes from its done batches (its failed, interrupted or deferred ones are asked again as usual).

    `base_run` (session 12): the run's base run, as recorded when it started (the base of a run is fixed then; another
    one is refused). A run with a base is resumed only while the base is still promoted and not being driven; a base
    changed since the start is recorded, and the run's sets are then STALE (the state identity carries it)."""
    if stop_after and stop_after not in STEPS:
        raise B.Refused(f"--stop-after must be one of {', '.join(STEPS)}")
    if from_step and from_step not in STEPS:
        raise B.Refused(f"--from must be one of {', '.join(STEPS)}")
    cp = load(run_id, staging)
    s_ = cp.data["settings"]
    _check_base_on_resume(cp, base_run, echo)
    cfg_off = C.load(Path(s_["ai_config"]) if s_.get("ai_config") else None)
    off_src = s_.get("offline") or OFF.requested(cfg_off, offline)
    if off_src:                                                 # session 12: before anything is asked
        OFF.activate(cfg_off, off_src)
        OFF.check_run_route(cfg_off, s_["route"])
        if s_.get("offline") != off_src:
            s_["offline"] = off_src
            cp.event("offline_mode", source=off_src)
    check_code_identity(cp, allow_code_change)                  # session 13: refused on changed code unless allowed
    killed = record_killed_segment(cp)                          # session 14 (N6): a segment a kill ended
    if killed is not None:
        echo(f"[{cp.data['run_id']}] note: segment {killed['segment']} {killed['note']}")
    cp.event("resumed", by_pid=os.getpid(), status_before=cp.data["status"],
             **({"from_step": from_step} if from_step else {}))
    if by_person:                                # session 14 (W2): defect 15 (a submit-batch continues on its own record)
        cp.intervention(kind="resume (the person's action)", by="a person (tenderpack ai resume, or the panel's Resume)",
                        note=f"process {os.getpid()}; status before: {cp.data['status']}"
                             + (f"; from step {from_step}" if from_step else ""))
    if from_step:
        _reset_from(cp, from_step)
    bad = reclassify_errored_batches(cp.data["batches"])
    if bad:                                                 # session 11 (E135): never a done batch without an answer
        cp.event("batches_reclassified_failed", batches=bad,
                 reason="recorded done although the host session ended with an error and no answer")
        cp.save()
    # a deferred batch (a rate limit) is always asked again; a failed one when retry_failed. Done batches never are.
    again = ("failed", "interrupted", "running", "deferred") if retry_failed else ("deferred",)
    for phase, step in (("reading", "readings"), ("analysis", "analysis"), ("downstream", "downstream")):
        redo = [k for k in cp.batches(phase) if cp.batch(k)["status"] in again]
        if redo:
            for k in redo:
                cp.batch(k)["status"] = "pending"
            _reset_from(cp, step)
            break
    if any((b.get("critic") or {}).get("status") in ("deferred", "failed") for b in cp.data["batches"].values()) \
            and cp.step("critic")["status"] == "done":
        cp.step("critic")["status"] = "pending"                 # the critic of a done batch is asked again, alone
        for s in STEPS[STEPS.index("critic") + 1:]:
            cp.step(s)["status"] = "pending"
        cp.save()
    return _drive(cp, stop_after, echo, sleep)


def _check_base_on_resume(cp: Checkpoint, base_run: str | None, echo) -> None:
    """Session 12: `resume --base-run` names the run's recorded base or is refused; a run with a base needs it still
    promoted and not running (candidate.base_run); a base whose fingerprint changed since the start is recorded."""
    rec = cp.data["settings"].get("base_run") or None
    if base_run and (not rec or rec.get("run_id") != base_run):
        raise B.Refused(f"run {cp.data['run_id']} was started " + (f"on base run {rec['run_id']}" if rec else
                                                                   "without a base run")
                        + f", not on {base_run}: the base of a run is fixed when it starts (start a new run with "
                          f"--base-run {base_run})")
    if not rec:
        return
    try:
        now = CAND.base_run(Path(rec["dir"]).parent, rec["run_id"])
    except CAND.CandidateError as e:
        raise B.Refused(f"run {cp.data['run_id']}: {e}") from None
    changed = now["fingerprint"] != rec.get("fingerprint")
    cp.event("base_checked", base_run=rec["run_id"], fingerprint=now["fingerprint"], changed_since_start=changed)
    if changed:
        echo(f"[{cp.data['run_id']}] note: base run {rec['run_id']}'s candidate changed since this run started: sets "
             "made against it are STALE (validated again before promotion, which then refuses)")


def reclassify_errored_batches(batches: dict) -> list[str]:
    """Session 11 (E135): a batch recorded `done` although its host session ended with an error (a refusal, a CLI that
    could not start) and gave no items was never answered; it becomes `failed` so that a resume asks it again. Returns
    the batch ids changed. A done batch with items, or whose session recorded no error, is left alone."""
    changed = []
    for bid, b in batches.items():
        hs = b.get("host_session") or {}
        if b.get("status") == "done" and hs.get("error") and not b.get("items"):
            b.update(status="failed", error=f"the host session ended without an answer: {hs['error']}")
            changed.append(bid)
    return changed


def _reset_from(cp: Checkpoint, step: str) -> None:
    """Mark `step` and every later step pending again, and put the candidate back as it was before promotion."""
    i = STEPS.index(step)
    for s in STEPS[i:]:
        if cp.step(s)["status"] != "pending":
            cp.step(s)["status"] = "pending"
    if i <= STEPS.index("downstream"):
        for k in cp.batches("downstream"):
            if cp.batch(k)["status"] in ("failed", "interrupted", "running"):
                cp.batch(k)["status"] = "pending"
    snap = CAND.paths(cp.path.parent)["pre_promotion"]
    if snap.exists() and i <= STEPS.index("promotion"):
        DS._snapshot(snap.parent, snap)                         # restores the pre-promotion copies
    cp.save()


def _drive(cp: Checkpoint, stop_after: str | None, echo, sleep) -> dict:
    lock = RunLock(cp.path.parent)
    try:
        lock.acquire()
    except RunLockError as e:
        raise B.Refused(str(e)) from None
    ctx = Ctx(cp, echo, sleep)
    if lock.taken_over:
        cp.event("stale_run_lock_taken_over", previous=lock.taken_over)
        ctx.say(f"note: the run lock of process {lock.taken_over.get('pid')} (no longer running) was taken over")
    if (cp.data.get("code_identity") or {}).get("differ"):   # session 13: in the run log of every later segment
        ctx.say(f"note: {DIFFERENT_CODE}: " + "; ".join(code_lines(cp))[:600])
    cp.data.pop("stop_code", None)                     # session 12: set again only by this drive's own stop
    cp.set_status("running")
    step = None
    prev_term, interrupted = None, False
    hs_mod = _hostsession()
    if hs_mod is not None and hasattr(hs_mod, "reset_stop"):
        hs_mod.reset_stop()                                       # session 13 (E161): a new run in this process
    if threading.current_thread() is threading.main_thread():     # session 13 (D): SIGTERM recorded like Ctrl-C
        try:
            prev_term = signal.signal(signal.SIGTERM, _on_sigterm)
        except (ValueError, OSError):
            prev_term = None
    n_par = int(cp.data["settings"].get("max_parallel_sessions") or 1)
    if n_par > 1:                                  # session 12: batches at once, under one run-scoped lock
        ctx.gate = R.RateGate()
        ctx.prefetch = Prefetch(ctx, n_par)
        try:
            ctx.run_lock = B.acquire(ctx.dir / "ai", ctx.addendum, {"route": cp.data["settings"]["route"],
                                                                    "run_id": ctx.run_id, "pid": os.getpid(),
                                                                    "scope": "run"})
            cp.event("run_lock_scoped", scope="run", lock=str(B.lock_path(ctx.dir / "ai", ctx.addendum)),
                     max_parallel_sessions=n_par)
        except B.Refused as e:
            lock.release()
            raise B.Refused(f"batches at once need the addendum's lock for the run: {e}") from None
    try:
        for step in STEPS:
            if cp.done(step):
                continue
            ANS.at_checkpoint(ctx, step)     # session 14 (W5): a safe checkpoint (before analysis, downstream, promotion)
            ctx.say(f"[{ctx.run_id}] {step} ...")
            with cp.timed(step) as st:
                STEP_FUNCS[step](ctx, st)
            if stop_after == step and step != STEPS[-1]:
                raise StopRun("stopped", f"stopped after {step} (--stop-after); resume with `tenderpack ai resume "
                                         f"{ctx.run_id}`", code=0)
        cp.set_status(*_final_status(cp))
    except WaitingForHost as w:
        cp.set_status("waiting_for_host", str(w))
        ctx.say(str(w))
    except StopRun as s:
        if s.status == "stopped":
            cp.data["stop_code"] = STOP_FOR_PERSON if s.code is None else s.code
        cp.set_status(s.status, s.reason)
        ctx.say(f"{s.status.upper()}: {s.reason}")
    except KeyboardInterrupt as e:
        interrupted = True
        # session 14 (W2; blind-07 defect 15): the batches whose exchanges the stop cuts (this thread's and the workers')
        in_flight = sorted({k for k, b in cp.data["batches"].items() if b.get("status") == "running"}
                           | ({k for k, r_ in ctx.prefetch.recs.items() if not r_["future"].done()}
                              if ctx.prefetch is not None else set()))
        stopped = _stop_live_sessions()
        _interrupted(cp)
        sig = "SIGTERM" if isinstance(e, Terminated) else "SIGINT"
        cp.event("interrupted", step=step, signal=sig, host_sessions_stopped=stopped)
        cp.data["interventions"].append({"ts": now_iso(), "kind": "stop (the person's action)",
                                         "by": "a person (a signal from outside the run: the panel's Stop, Ctrl-C or a "
                                               "kill)", "note": f"{sig} during step {step}; {stopped} host session "
                                                                f"process(es) stopped"})
        for k in in_flight:
            cp.data["interventions"].append({"ts": now_iso(), "kind": "host session stopped by the person's stop",
                                             "batch": k, "by": "tenderpack.ai.workflow (automatic)",
                                             "note": "its exchange was cut before its answer was taken; on resume its "
                                                     "staged submission is reused if it made one, else it is asked again"})
        cp.save()
        cp.set_status("stopped", f"interrupted during {step}; resume with `tenderpack ai resume {ctx.run_id}`")
        raise
    except Exception as e:                                       # noqa: BLE001 (recorded with its traceback; resumable)
        tb = traceback.format_exc()
        (ctx.dir / "logs").mkdir(parents=True, exist_ok=True)
        with open(ctx.dir / "logs" / "error.log", "a", encoding="utf-8") as fh:
            fh.write(f"{now_iso()} {step}\n{tb}\n")
        ctx.log.event("error", step=step, error=f"{type(e).__name__}: {e}", traceback=tb[-4000:])
        cp.set_status("failed", f"{step}: {type(e).__name__}: {_short(str(e), 500)} (traceback in logs/error.log)")
        ctx.say(f"FAILED in {step}: {type(e).__name__}: {_short(str(e), 300)}")
    finally:
        if ctx.prefetch is not None:
            ctx.prefetch.close(interrupted=interrupted)
        if prev_term is not None:
            try:
                signal.signal(signal.SIGTERM, prev_term)
            except (ValueError, OSError):
                pass
        if ctx.gate is not None:
            cp.data["rate_gate"] = ctx.gate.record()
        if ctx.run_lock is not None:
            ctx.run_lock.release()
        cp.event(SEGMENT_END, segment=segment_number(cp.data), status=cp.data.get("status"))   # session 14 (N6)
        _record_outcome(cp)                         # session 11: execution, completeness, approval (kept apart)
        lock.release()
    out = summary(cp)
    for line in timing_lines(cp):
        ctx.echo(line)
    ctx.echo(f"run {ctx.run_id}: {out['status']}" + (f" ({out['status_reason']})" if out.get("status_reason") else ""))
    if (ctx.dir / "review" / "index.md").exists():
        ctx.echo(f"review packet: {ctx.dir / 'review' / 'index.md'}")
    return out


def _stop_live_sessions() -> int:
    """Session 13 (D): stop the host CLI processes of this process still running (hostsession.run_tracked)."""
    hs = _hostsession()
    if hs is None or not hasattr(hs, "terminate_live"):
        return 0
    try:
        return hs.terminate_live()
    except Exception:                                            # noqa: BLE001 (the interruption proceeds)
        return 0


def _interrupted(cp: Checkpoint) -> None:
    for b in cp.data["batches"].values():
        if b["status"] == "running":
            b["status"] = "interrupted"
    cp.save()


def _final_status(cp: Checkpoint) -> tuple[str, str | None]:
    """complete only when the run's completeness record is complete (session 11, completeness()): every provision
    answered by a promoted item, every downstream task answered by a promotable item and no downstream batch failed or
    left unrun, the candidate's check-register clean, the candidate outputs published; otherwise partial, with the
    reasons."""
    outs = cp.step("outputs")
    comp = completeness(cp)
    if outs.get("refused"):
        return "partial", f"the candidate outputs build was refused ({outs.get('reason')}); out-before stays the last " \
                          "validated state" + (f"; also: {'; '.join(comp['reasons'][1:3])}" if len(comp["reasons"]) > 1
                                                else "")
    if comp["status"] != "complete":
        return "partial", "; ".join(comp["reasons"][:4]) + (f" (+{len(comp['reasons']) - 4} more in the review packet)"
                                                            if len(comp["reasons"]) > 4 else "")
    return "complete", None


def _js(p: Path):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def completeness(cp: Checkpoint) -> dict:
    """Session 11 (D1): what the run COMPLETED, kept apart from execution (execution()) and from human approval
    (approval()). complete only when (1) every provision of the addendum is answered by a promoted op or disposition
    (none `unresolved` in the candidate op file), (2) every downstream task is answered by a promotable item (a task with
    no item is `unanswered`; one whose items are all escalated, insufficient, invalid, conflicting or held back is
    `unresolved`) and every downstream batch ran (`done`), (3) the candidate's check-register is clean (exit 0, no
    finding; the C46 findings are listed) and (4) the candidate outputs were published (built, exit 0, not refused).
    Otherwise partial, with every reason. Reads the checkpoint and the run's files only."""
    d, run = cp.data, cp.path.parent
    reasons: list[str] = []
    prom = cp.step("promotion")
    unres = list(prom.get("unresolved") or [])
    prov = {"total": len(d["provisions"]), "unresolved": unres,
            "answered": len(d["provisions"]) - len(unres) if prom.get("status") == "done" else 0}
    if prom.get("status") != "done":
        reasons.append(f"promotion into the candidate did not run (step {prom.get('status')})")
    elif unres:
        reasons.append(f"{len(unres)} provision(s) unresolved in the candidate (listed first in the review packet)")
    tasks = _js(run / "downstream" / "tasks.json")
    kinds = ({t["id"]: t.get("kind") for t in tasks} if tasks is not None else
             {k: (v or {}).get("kind") for k, v in (d.get("downstream") or {}).get("tasks", {}).items()})
    batches = {k: b for k, b in d["batches"].items() if b.get("phase") == "downstream"}
    bad = [{"batch": k, "status": b.get("status"), "error": _short(b.get("error"), 300), "tasks": list(b.get("tasks") or [])}
           for k, b in batches.items() if b.get("status") != "done"
           and not (b.get("status") == "split" and b.get("parts"))]     # a split batch: its parts are the batches
    if cp.step("downstream").get("status") != "done":
        reasons.append(f"the downstream step did not run (step {cp.step('downstream').get('status')})")
    for x in bad:
        reasons.append(f"downstream batch {x['batch']} {x['status']}" + (f" ({x['error']})" if x["error"] else "")
                       + f": {len(x['tasks'])} task(s) not asked")
    ds_file = run / "downstream" / "proposals.yaml"
    if ds_file.exists():
        staged = load_yaml(ds_file) or {}
        items = (staged.get("downstream_set") or {}).get("items") or []
        held = (staged.get("controller") or {}).get("held_back") or {}
    else:                                          # the checkpoint's own record of the items (a copied checkpoint)
        items = [{"id": v.get("id_in_set") or k, "task": v.get("task"), "statement_type": v.get("type"),
                  "verification_status": v.get("verification_status")}
                 for k, v in ((d.get("downstream") or {}).get("items") or {}).items()]
        held = {i["id"]: True for i, v in zip(items, ((d.get("downstream") or {}).get("items") or {}).values())
                if v.get("held_back")}
    alias = DS.task_aliases(tasks or [])          # session 14 (N2): an answer by a merged origin's id answers its task
    by_task: dict[str, list[dict]] = {}
    for it in items:
        by_task.setdefault(alias.get(it.get("task"), it.get("task")), []).append(it)
    unanswered = [{"task": t, "kind": kinds[t]} for t in kinds if t not in by_task]
    unresolved_tasks = [{"task": t, "kind": kinds[t], "items": {i["id"]: i.get("verification_status") for i in by_task[t]}}
                        for t in kinds if t in by_task and not any(
                            i.get("verification_status") in DS.PROMOTABLE and i["id"] not in held for i in by_task[t])]
    if unanswered:
        reasons.append(f"{len(unanswered)} of {len(kinds)} downstream task(s) unanswered: "
                       + ", ".join(x["task"] for x in unanswered[:8]) + (" …" if len(unanswered) > 8 else ""))
    if unresolved_tasks:
        reasons.append(f"{len(unresolved_tasks)} downstream task(s) answered only by items that cannot be promoted: "
                       + ", ".join(x["task"] for x in unresolved_tasks[:8]) + (" …" if len(unresolved_tasks) > 8 else ""))
    cr = cp.step("check_register")
    c46 = [x for x in cr.get("first") or [] if x.startswith("[C46]")]
    if cr.get("status") != "done":
        reasons.append(f"check-register did not run on the candidate (step {cr.get('status')})")
    elif cr.get("exit_code") != 0 or cr.get("findings"):
        cl = cr.get("classified") or {}
        reasons.append(f"check-register on the candidate: exit {cr.get('exit_code')}, {cr.get('findings')} finding(s) "
                       f"{cr.get('by_kind')}" + (f" ({len(cl.get('not_proposed') or [])} missing because the downstream "
                                                 f"phase did not propose them, {len(cl.get('defects') or [])} defect(s))"
                                                 if cl else "")
                       + (f"; C46: {'; '.join(_short(x, 160) for x in c46[:3])}" if c46 else ""))
    outs = cp.step("outputs")
    published = outs.get("status") == "done" and not outs.get("refused") and outs.get("exit_code") == 0
    if outs.get("status") != "done":
        reasons.append(f"the candidate outputs were not built (step {outs.get('status')})")
    elif not published:
        reasons.append(f"the candidate outputs were not published ({_short(outs.get('reason'), 300)})")
    return {"status": "partial" if reasons else "complete", "reasons": reasons, "provisions": prov,
            "downstream": {"tasks": len(kinds), "answered": len(kinds) - len(unanswered) - len(unresolved_tasks),
                           "unanswered": unanswered, "unresolved": unresolved_tasks, "batches_not_done": bad,
                           "no_change": sorted({i.get("task") for i in items if i.get("statement_type") == "no_change"
                                                and i.get("verification_status") in DS.PROMOTABLE})},
            "check_register": {"exit_code": cr.get("exit_code"), "findings": cr.get("findings"),
                               "by_kind": cr.get("by_kind"), "c46": c46},
            "outputs": {"published": published, "refused": bool(outs.get("refused")), "reason": outs.get("reason"),
                        "exit_code": outs.get("exit_code")}}


def execution(cp: Checkpoint) -> dict:
    """Session 11 (D1): what RAN, apart from completeness and approval: each step's status (done / stopped / failed /
    waiting / pending ...) and the batches of each phase by status."""
    by_phase: dict[str, Counter] = {}
    for b in cp.data["batches"].values():
        by_phase.setdefault(b.get("phase") or "?", Counter())[b.get("status") or "?"] += 1
    return {"run_status": cp.data.get("status"), "steps": {s: cp.step(s).get("status") for s in STEPS},
            "batches": {k: dict(v) for k, v in by_phase.items()}}


def approval(cp: Checkpoint) -> dict:
    """Session 11 (D1): human approval, apart from execution and completeness. The workflow approves, accepts and sends
    nothing: always "none" from the run. The decisions a named person has recorded in the candidate's (copied)
    decisions file, if any, are listed by name."""
    out = {"status": "none", "by_the_workflow": "nothing approved, accepted, rejected or sent", "decisions": []}
    pack = (cp.data.get("candidate") or {}).get("pack")
    try:
        cfg = load_yaml(Path(pack)) or {} if pack and Path(pack).exists() else {}
        from .. import review
        dec = review.load_decisions(review.decisions_path(cfg, ROOT)) if cfg else []
    except Exception as e:                                       # noqa: BLE001 (a report; never blocks the run)
        out["note"] = f"the candidate's decisions file could not be read: {type(e).__name__}: {_short(str(e), 200)}"
        dec = []
    out["decisions"] = [f"{x.get('decision')} {x.get('kind')} {x.get('id')} by {x.get('reviewer')} ({x.get('date')})"
                        for x in dec if isinstance(x, dict)]
    return out


# session 14 (N6, defect 15): a segment ended by a kill (the process gone, no `segment_ended`) leaves no end and no
# drive record, and its lost work was invisible (the bench showed segment 2 ending at its last event although the
# process worked on). On resume the end is recorded ("ended by a stop at <the last event>; sessions without a result:
# <ids> (killed)"), its `concurrency_drives` entry is kept (phases not recorded: the process was killed), and the
# destroyed work (the host sessions of that segment that never wrote a result) is counted in `destroyed_work` (and in
# scripts/bench_workflow.py's "destroyed" line).
SEGMENT_END = "segment_ended"
SEGMENT_END_RECORDED = "segment_end_recorded"


def segment_number(data: dict) -> int:
    """The current segment's number: one per `started` / `resumed` event."""
    return max(1, sum(1 for e in data.get("events") or [] if e.get("event") in ("started", "resumed")))


def _killed_sessions(data: dict, run_dir: Path, since: str) -> list[dict]:
    """The host session folders started at or after `since` that hold a prompt and no result (session.json)."""
    roots = [Path(run_dir) / "ai"]
    cand = (data.get("candidate") or {}).get("dir")
    if cand:
        roots.append(Path(cand).parent / "ai")
    known = {x.get("session") for d in data.get("destroyed_work") or [] for x in d.get("sessions") or []}
    t0 = dt.datetime.strptime(since[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc).timestamp()
    out, seen = [], set()
    for root in roots:
        for f in sorted(root.glob("*/prompt.txt")) if root.is_dir() else []:
            d = f.parent
            if d.name in seen or d.name in known or (d / "session.json").exists() or f.stat().st_mtime < t0:
                continue
            seen.add(d.name)
            last = max(x.stat().st_mtime for x in d.iterdir())
            iso = lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")  # noqa: E731
            out.append({"session": d.name, "started": iso(f.stat().st_mtime), "last_activity": iso(last),
                        "seconds": round(last - f.stat().st_mtime, 1)})
    return out


def record_killed_segment(cp) -> dict | None:
    """The end record of the last segment when it has none (see above); None when it ended (or there is none)."""
    evs = cp.data.get("events") or []
    starts = [i for i, e in enumerate(evs) if e.get("event") in ("started", "resumed")]
    if not starts or any(e.get("event") in (SEGMENT_END, SEGMENT_END_RECORDED) for e in evs[starts[-1] + 1:]):
        return None
    start = evs[starts[-1]]["ts"]
    at = max([str(e.get("ts")) for e in evs[starts[-1]:]] + [str(cp.data.get("updated") or "")])
    seg = segment_number(cp.data)
    killed = _killed_sessions(cp.data, Path(cp.path).parent, start)
    note = (f"ended by a stop at {at}; sessions without a result: "
            + (", ".join(x["session"] for x in killed) + " (killed)" if killed else "none"))
    rec = {"segment": seg, "start": start, "at": at, "note": note, "sessions": killed,
           "session_seconds_lost": round(sum(x["seconds"] or 0 for x in killed), 1)}
    cp.event(SEGMENT_END_RECORDED, segment=seg, at=at, note=note, sessions_without_result=[x["session"] for x in killed])
    cp.data.setdefault("concurrency_drives", []).append(
        {"drive": at, "segment": seg, "interrupted": True, "ended_by": "a stop (the process was killed; recorded on "
                                                                      "resume)", "phases": {}})
    cp.data.setdefault("destroyed_work", []).append(rec)
    cp.data.setdefault("interventions", []).append(
        {"ts": at, "kind": "stop (no end recorded)", "by": "unknown (the process was killed: a kill, the panel's Stop "
                                                          "or a closed terminal)", "note": note})
    return rec


def promotion_lines(prom: dict, pops: dict) -> list[str]:
    """The review packet's promotion section (session 14, N12: the output-time issues; N2/N3/N11: the merges)."""
    L = ["## Promoted into the candidate (PROPOSED; nothing accepted)", ""]
    for k in ("ops", "dispositions", "accounted_unresolved", "rows_new", "readings", "issues", "analysis_issues",
              "output_time_issues", "evidence_items", "activities", "lead_times", "clarifications", "relationships",
              "referenced_documents", "no_change"):
        if prom.get(k):
            L.append(f"- {k.replace('_', ' ')}: {', '.join(map(str, prom[k][:40]))}" + (f" (+{len(prom[k]) - 40})" if len(prom[k]) > 40 else ""))
    if prom.get("output_time_issues"):
        L.append("  - raised at output time (the class-scope rule): HUMAN DECISION PENDING, written into the candidate "
                 "register as PROPOSED")
    if prom.get("issues_merged"):
        L.append("- the same question promoted once (analysis issue -> the issue it was merged into): " + "; ".join(
            f"{k} -> {v}" for k, v in prom["issues_merged"].items()))
    if prom.get("applied_by_rows"):
        L.append("- applied through a new row (the provision's obligation is the row; PROPOSED): " + "; ".join(
            f"{k} -> {', '.join(v)}" for k, v in prom["applied_by_rows"].items()))
    L += [f"- unresolved provisions: {len(prom.get('unresolved') or [])}"] + [f"- note: {x}" for x in prom.get("notes") or []] + [""]
    dropped = (pops or {}).get("dropped") or {}
    if dropped:
        L += ["- left out of the promoted ops: " + "; ".join(f"{k}: {_short(v, 160)}" for k, v in dropped.items()), ""]
    return L


def _record_outcome(cp: Checkpoint) -> None:
    """The three records, kept apart in the checkpoint (and the review packet): execution, completeness, approval.
    Session 14 (W2): and the host's own usage per session (host_usage), rewritten at the end of every drive."""
    try:
        cp.data["host_usage"] = host_usage(cp.path.parent, cp.data)
    except Exception as e:                                       # noqa: BLE001 (a record; never breaks a run)
        cp.data["host_usage"] = {"sessions": [], "error": f"{type(e).__name__}: {_short(str(e), 200)}"}
    try:
        cp.data["execution"], cp.data["completeness"], cp.data["approval"] = execution(cp), completeness(cp), approval(cp)
        cp.save()
    except Exception as e:                                       # noqa: BLE001 (the records never break a run)
        cp.data["completeness"] = {"status": "unknown", "reasons": [f"not computed: {type(e).__name__}: {e}"]}
        cp.save()


# ---------------------------------------------------------------------------------------------- session 14 (W2): records
# The blind-07 scorer's defects 15 and 18 (rehearsals/blind-07/COMPARISON.md §6, §8): the packet's usage line said
# "0 call(s), 0 input / 0 output tokens" although 10 host sessions and 6 critic requests ran (the host's own usage was
# only in the session records scripts/bench_workflow.py reads); the `concurrency` record kept the last drive only; and
# `interventions` named neither the sessions the person's stop killed, nor the answers reused, nor the stop and resume.
# Unknown usage is never printed as 0.
_TOKEN_KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")


def _session_batch_index(data: dict) -> dict[str, str]:
    """{host session run id: batch (or '<batch> critic')} from the checkpoint's batch and critic records."""
    out: dict[str, str] = {}
    for k, b in (data.get("batches") or {}).items():
        hs = b.get("host_session") or {}
        if hs.get("run_id"):
            out[hs["run_id"]] = k
        for x in ((b.get("request") or {}).get("host_sessions") or []):
            if isinstance(x, dict) and x.get("run_id"):
                out.setdefault(x["run_id"], k)
        cr = b.get("critic") or {}
        for x in (((cr.get("request") or {}) if isinstance(cr.get("request"), dict) else {}).get("host_sessions") or []):
            if isinstance(x, dict) and x.get("run_id"):
                out.setdefault(x["run_id"], f"{k} critic")
        if cr.get("critic_run"):
            out.setdefault(cr["critic_run"], f"{k} critic")
    return out


def _known_usage(u) -> dict | None:
    if not isinstance(u, dict) or not any(isinstance(u.get(k), (int, float)) for k in _TOKEN_KEYS):
        return None
    return {k: int(u.get(k) or 0) for k in _TOKEN_KEYS}


def host_usage(run_dir: Path, data: dict) -> dict:
    """The host's own usage per session, from the session records next to the run (what scripts/bench_workflow.py reads):
    every <run>/ai/*/session.json (a host session: reading, analysis, downstream answer) and every `plain_session` event
    of <run>/ai/*/log.jsonl (a plain host session: the critic, a repair). A session without usage (killed, failed before
    its result) is `unknown`, never 0. {sessions: [{session, batch, kind, elapsed_s, error, usage | None}], known,
    unknown, totals (over the known ones), source}."""
    run_dir = Path(run_dir)
    roots = [run_dir / "ai"]
    cand = (data.get("candidate") or {}).get("dir")
    if cand:
        roots.append(Path(cand).parent / "ai")
    idx = _session_batch_index(data)
    sessions: list[dict] = []
    seen: set = set()
    for root in roots:
        if not root.is_dir():
            continue
        for f in sorted(root.glob("*/session.json")):
            try:
                sj = json.loads(f.read_text(encoding="utf-8")) or {}
            except (OSError, ValueError):
                sj = {}
            sid = sj.get("run_id") or f.parent.name
            if sid in seen:
                continue
            seen.add(sid)
            batch = idx.get(sid) or next((k for k, b in (data.get("batches") or {}).items() if sj.get("provisions")
                                          and list(b.get("provisions") or []) == list(sj["provisions"])), None)
            kind = ("analysis" if sj.get("provisions") else str(batch).split("-")[0] if batch else "host session")
            sessions.append({"session": sid, "batch": batch, "kind": kind, "elapsed_s": sj.get("elapsed_s"),
                             "error": _short(sj.get("error"), 160) if sj.get("error") else None,
                             "usage": _known_usage(sj.get("usage"))})
        for f in sorted(root.glob("*/log.jsonl")):
            try:
                lines = f.read_text(encoding="utf-8").splitlines()
            except OSError:
                continue
            for n, line in enumerate(lines):
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                if e.get("event") != "plain_session":
                    continue
                sid = f"{f.parent.name}#{n}"
                if sid in seen:
                    continue
                seen.add(sid)
                b = idx.get(f.parent.name) or next((v for k, v in idx.items() if f.parent.name.startswith(str(k))), None)
                sessions.append({"session": sid, "batch": b or f.parent.name.replace(str(data.get("run_id") or ""), "")
                                 .strip("-") or None, "kind": e.get("label") or "plain session",
                                 "elapsed_s": e.get("elapsed_s"), "error": _short(e.get("error"), 160) if e.get("error")
                                 else None, "usage": _known_usage(e.get("usage"))})
    known = [x for x in sessions if x["usage"] is not None]
    totals = {k: sum(x["usage"][k] for x in known) for k in _TOKEN_KEYS}
    return {"sessions": sessions, "known": len(known), "unknown": len(sessions) - len(known), "totals": totals,
            "source": "the host's own session records under the run's ai/ folder (session.json, plain_session events)"}


def usage_lines(cp: Checkpoint) -> list[str]:
    """The review packet's usage lines (session 14): the application routes' calls and tokens, and the host's own usage
    per session; a usage nobody reported is 'unknown', never 0."""
    d = cp.data
    u = d.get("usage") or {}
    route = (d.get("settings") or {}).get("route")
    hu = d.get("host_usage") or host_usage(cp.path.parent, d)
    host_batches = [k for k, b in (d.get("batches") or {}).items() if b.get("host_session")
                    or ((b.get("request") or {}).get("host_sessions"))]
    critic_runs = [k for k, b in (d.get("batches") or {}).items() if (b.get("critic") or {}).get("critic_run")]
    L = []
    if u.get("calls") or route not in ("host",):
        L.append(f"- usage (application routes): {u.get('calls', 0)} call(s), {u.get('input_tokens', 0)} input / "
                 f"{u.get('output_tokens', 0)} output tokens; cost "
                 f"{u['cost_usd'] if u.get('cost_usd') is not None else 'not computed'}")
    else:
        L.append("- usage (application routes): none: the run's route is host, every exchange ran in a host session "
                 "(below)")
    ss = hu.get("sessions") or []
    if ss:
        t = hu.get("totals") or {}
        L.append(f"- host sessions: {len(ss)} (their own records); usage of the {hu.get('known', 0)} that reported it: "
                 f"input {t.get('input_tokens', 0)}, cache write {t.get('cache_creation_input_tokens', 0)}, cache read "
                 f"{t.get('cache_read_input_tokens', 0)} / output {t.get('output_tokens', 0)} tokens"
                 + (f"; usage **unknown** for {hu.get('unknown')} session(s): "
                    + ", ".join(f"{x['session']} ({x.get('batch') or 'batch not recorded'})"
                                for x in ss if x["usage"] is None)[:600] if hu.get("unknown") else ""))
    elif host_batches or critic_runs or route == "host":
        L.append(f"- host sessions: {len(host_batches)} batch(es) and {len(critic_runs)} critic request(s) recorded a "
                 "host session; their usage: **unknown** (no session record was found next to this run)")
    return L


def _events(data: dict, name: str) -> list[dict]:
    return [e for e in data.get("events") or [] if (e.get("event") or e.get("name")) == name]


PERSON_KINDS = ("stop (the person's action)", "resume (the person's action)", "submit-batch")


def intervention_lines(cp: Checkpoint) -> list[str]:
    """The packet's interventions (session 14): the person's own actions (stop, resume, a submitted batch) first, then
    what the run did with them (sessions the stop killed, answers reused), then the automatic host sessions. A run
    recorded before session 14 has its stop and resume in its events only: they are listed from there, so said."""
    d = cp.data
    xs = list(d.get("interventions") or [])

    def line(x: dict) -> str:
        return (f"- {x.get('ts')}: {x.get('kind')}" + (f" — batch {x.get('batch')}" if x.get("batch") else "")
                + (f" by {x.get('by')}" if x.get("by") else "")
                + (f"; host model {x.get('host_model')}" if x.get("host_model") else "")
                + (f"; file {x.get('file')} (sha256 {str(x.get('sha256'))[:16]}…)" if x.get("file") else "")
                + (f"; {x.get('note')}" if x.get("note") else ""))
    person = [x for x in xs if str(x.get("kind") or "").startswith(PERSON_KINDS)]
    if not any(str(x.get("kind")).startswith(("stop (", "resume (")) for x in person):
        for e in _events(d, "interrupted"):
            person.append({"ts": e.get("ts"), "kind": "stop (the person's action)",
                           "note": f"{e.get('signal')} during step {e.get('step')}; host sessions stopped "
                                   f"{e.get('host_sessions_stopped', 'unknown')} (from the run's events)"})
        for e in _events(d, "resumed"):
            person.append({"ts": e.get("ts"), "kind": "resume (the person's action)",
                           "note": f"process {e.get('by_pid')}; status before: {e.get('status_before')} "
                                   "(from the run's events)"})
        if not any(str(x.get("kind")).startswith("submission reused") for x in xs):
            xs += [{"ts": e.get("ts"), "kind": "submission reused (automatic)", "batch": e.get("batch"),
                    "note": f"staged set {e.get('run_id')}, submitted {e.get('submitted') or 'earlier'} "
                            "(from the run's events)"} for e in _events(d, "submission_reused")]
    person.sort(key=lambda x: str(x.get("ts")))
    rest = [x for x in xs if x not in person and not str(x.get("kind") or "").startswith(PERSON_KINDS)]
    L = ["## Manual interventions (the person's actions)", ""]
    L += [line(x) for x in person] or ["- none"]
    L += ["", "### What the run did with them, and its automatic host sessions (not a person)", ""]
    L += [line(x) for x in sorted(rest, key=lambda x: str(x.get("ts")))] or ["- none"]
    return L + [""]


def _made_when(data: dict, ts) -> str:
    """Whether a submission at `ts` was made before an interruption or after a resume (from the run's events)."""
    if not ts:
        return "made earlier (time not recorded)"
    stops = [e.get("ts") for e in _events(data, "interrupted") if str(e.get("ts")) > str(ts)]
    if stops:
        return f"made before the interruption at {min(stops)}"
    res = [e.get("ts") for e in _events(data, "resumed") if str(e.get("ts")) < str(ts)]
    return f"made after the resume at {max(res)}" if res else "made in this drive"


def summary(cp: Checkpoint) -> dict:
    d = cp.data
    prov = Counter(v["status"] for v in d["provisions"].values())
    return {"run_id": d["run_id"], "addendum": d["addendum"], "status": d["status"], "status_reason": d["status_reason"],
            "exit_code": 1 if d["status"] in ("complete", "partial") and cp.step("outputs").get("refused")
            else d.get("stop_code", 0) if d["status"] == "stopped" else EXIT_CODES.get(d["status"], 1),
            "run_dir": str(cp.path.parent), "provisions": dict(prov), "timings": cp.timings(),
            "total_seconds": round(sum(cp.timings().values()), 1),
            "review": str(cp.path.parent / "review" / "index.md"),
            "waiting": [k for k, b in d["batches"].items() if b["status"] == "waiting_for_host"],
            # session 11: execution, completeness and approval are three separate records
            "completeness": {k: (d.get("completeness") or {}).get(k) for k in ("status", "reasons")},
            "approval": (d.get("approval") or {}).get("status", "none"),
            # session 13: the code and policy identity of the run's segments
            "code": {"start": (d.get("code_identity") or {}).get("start"),
                     "segments": len((d.get("code_identity") or {}).get("segments") or []),
                     **({"note": DIFFERENT_CODE, "lines": code_lines(cp)} if (d.get("code_identity") or {}).get("differ")
                        else {})},
            # session 12: consecutive addenda (the run this one starts from, the addenda the state lacks)
            **({"base_run": {k: (d["settings"]["base_run"] or {}).get(k) for k in ("run_id", "addendum", "chain", "dir")}}
               if (d.get("settings") or {}).get("base_run") else {}),
            **({"missing_addenda": d["settings"]["missing_addenda"]}
               if (d.get("settings") or {}).get("missing_addenda") else {})}


def timing_lines(cp: Checkpoint) -> list[str]:
    return ["timings (wall clock per step):"] + cp.timing_lines(TARGET_MIN)


# ---------------------------------------------------------------------------------------------- step: ingest

def step_ingest(ctx: Ctx, st: dict) -> None:
    cp, s = ctx.cp, ctx.s
    if not ctx.P["pack"].exists():
        if ctx.P["dir"].exists():
            shutil.rmtree(ctx.P["dir"])                         # an interrupted creation: made again from the copies
        info = CAND.create(ctx.dir, Path(s["pack"]), ctx.addendum, Path(s["pdf"]), ctx.run_id, base=s.get("base_run"))
        cp.data["candidate"] = {k: info[k] for k in ("dir", "pack", "pack_before", "build", "out", "out_before", "pdf_copy")}
        cp.data["inputs"].update(pdf=info["pdf"], copied=info["copied"], real_hashes=info["real_hashes"],
                                 preceding_pack_id=info["preceding_pack_id"],
                                 **({"base_run": info["base_run"]} if info.get("base_run") else {}))
        cp.save()
    res = CAND.ingest(ctx.dir)
    st.update(exit_code=res["exit_code"], units=res.get("units"), pending_review=res.get("pending_review"),
              failed_checks=res.get("failed"))
    if res["exit_code"] != 0:
        from . import regionread as RR
        unread = RR.unread_only_failure(ctx.P["build"].with_name(ctx.P["build"].name + ".failed"))
        if unread:
            # refused ONLY because image regions have no reading: the readings step proposes them, then ingests again
            st.update(refused_for_readings=True, unread_regions=unread, reason=res.get("reason"))
            ctx.say(f"  ingest refused the candidate only for image regions with no reading {unread}: the readings step "
                    "proposes readings (PENDING HUMAN REVIEW) and ingests again")
            _start_before(ctx)
            return
        st["status"], st["reason"] = "stopped", res.get("reason") or res["status"]
        raise StopRun("stopped", f"ingest refused the candidate (exit {res['exit_code']}): {st['reason']}", code=2)
    _after_ingest(ctx, st)
    _start_before(ctx)


def _after_ingest(ctx: Ctx, st: dict) -> None:
    """The provisions and structural units of the addendum from the candidate build (checkpointed)."""
    cp = ctx.cp
    ctx._ws = None
    ws = ctx.ws
    ws.refresh()
    ws.require_ok()
    provs = controller._provisions(ws, ctx.addendum)
    by_id = ws.units_by_id
    for p in provs:
        u = by_id.get(p) or {}
        cp.data["provisions"].setdefault(p, {"kind": u.get("kind"), "pages": u.get("pages"), "origin": u.get("origin"),
                                             "status": "pending", "batch": None, "items": [], "accounted": False,
                                             "history": [{"ts": now_iso(), "status": "pending"}]})
    cp.data["structure"] = [{"unit_id": u["unit_id"], "kind": u["kind"], "pages": u.get("pages"),
                             "text": _short(u.get("text"), 120),
                             "note": "structure, not a provision (headings, table and form containers, image regions are "
                                     "read through their members and readings)"}
                            for u in ws.r["units"] if u["doc"] == ctx.addendum and u["unit_id"] not in set(provs)]
    cp.data["inputs"]["candidate_state"] = ws.identity().model_dump()
    st.update(provisions=len(provs), structure_units=len(cp.data["structure"]))
    cp.save()
    ctx.say(f"  candidate built: {len(provs)} provisions of {ctx.addendum} "
            f"(+{len(cp.data['structure'])} structural units listed)")


def _start_before(ctx: Ctx) -> None:
    cp, s = ctx.cp, ctx.s
    ob = cp.data.setdefault("out_before", {})
    ev = Path(s["evidence"])
    reason = None
    if not (ev / "BUILD_MANIFEST.json").is_file():
        reason = f"no previous evidence build at {ev}"
    else:
        from .. import stage2
        units, problems = stage2.load_evidence(ev, ROOT)
        docs = {u["doc"] for u in units}
        want = {d["doc_id"] for d in (load_yaml(ctx.P["pack_before"]) or {}).get("documents") or []}
        if problems:
            reason = "the previous evidence build is not usable (E01): " + "; ".join(problems)[:400]
        elif docs != want:
            reason = f"the evidence build {ev} holds {sorted(docs)}, the preceding pack {sorted(want)}"
    if reason:
        ob.update(status="not_built", reason=reason + "; the last validated state is the real out/ (not verified here)")
        cp.save()
        ctx.say(f"  out-before not built: {reason}")
        return
    key = CAND.before_key(ctx.dir, ev) if s.get("cache") else None
    if not s.get("background_before"):
        ob.update(status="pending", key=key, evidence=str(ev), note="built at the outputs step (--no-background)")
        cp.save()
        return
    res = CAND.start_before(ctx.dir, ev, Path(s["staging"]), key, background=True)
    if res.get("background"):
        ob.update(status="running", pid=res["pid"], key=key, started=now_iso(), evidence=str(ev))
        ctx.before_proc = res["_proc"]
    else:
        ob.update(status="done" if res.get("exit_code") == 0 else "refused", result=res, key=key, evidence=str(ev))
    cp.save()


def _join_before(ctx: Ctx) -> dict:
    cp, s = ctx.cp, ctx.s
    ob = cp.data.setdefault("out_before", {})
    if ob.get("status") in ("done", "refused", "not_built"):
        return ob
    if ob.get("status") == "running":
        res = CAND.wait_before(ctx.dir, Path(s["staging"]), ob.get("key"), ob.get("pid"), ctx.before_proc)
        if res is not None:
            ob.update(status="done" if res.get("exit_code") == 0 else "refused", result=res)
            cp.save()
            return ob
        ob.update(status="pending", note="the background build ended without a result; built again here")
    if not ob.get("status") or ob.get("status") == "pending":
        ev = Path(ob.get("evidence") or s["evidence"])
        if not (ev / "BUILD_MANIFEST.json").is_file():
            ob.update(status="not_built", reason=f"no previous evidence build at {ev}")
        else:
            res = CAND.start_before(ctx.dir, ev, Path(s["staging"]), ob.get("key"), background=False)
            ob.update(status="done" if res.get("exit_code") == 0 else "refused", result=res)
    cp.save()
    return ob


# ---------------------------------------------------------------------------------------------- step: readings

def _failed_build(ctx: Ctx) -> Path:
    return ctx.P["build"].with_name(ctx.P["build"].name + ".failed")


def _readings_dir(ctx: Ctx) -> Path:
    cfg = load_yaml(ctx.P["pack"]) or {}
    return CAND.resolve(cfg.get("readings_dir", "curation/readings"))


def step_readings(ctx: Ctx, st: dict) -> None:
    """Readings for the addendum's image regions that stopped ingest (C05 unread), proposed one region per batch,
    validated (regionread.validate: at most interpretation_pending), written into the candidate's readings PENDING
    HUMAN REVIEW; then ingest again. A region without a usable reading stops the run with the reason."""
    cp = ctx.cp
    ing = cp.step("ingest")
    if not ing.get("refused_for_readings"):
        st["note"] = "no addendum image region without a reading"
        return
    regions = ing.get("unread_regions") or []
    if not cp.batches("reading"):
        for rid in regions:
            cp.data["batches"][f"reading-{rid}"] = {"phase": "reading", "region": rid, "status": "pending",
                                                    "attempts": 0, "seconds": 0.0}
        cp.save()
    _local_reading_check(ctx, st)                                 # session 12: a local model without vision
    for bid in cp.batches("reading"):
        b = cp.batch(bid)
        if b["status"] in ("done", "skipped"):
            continue
        if b["status"] == "waiting_for_host":
            st["status"] = "waiting_for_host"
            raise WaitingForHost(_wait_message(ctx, bid))
        if ctx.stop_batches:
            b.update(status="failed", error=f"not run: {ctx.stop_batches}")
            continue
        _reading_batch(ctx, st, bid, b["region"])
        _stop_if_deferred(ctx, st, bid)
    st["batches"] = {k: cp.batch(k)["status"] for k in cp.batches("reading")}
    st["readings"] = {cp.batch(k)["region"]: {"status": cp.batch(k).get("verification_status"),
                                              "file": cp.batch(k).get("reading_file")} for k in cp.batches("reading")}
    deferred = [cp.batch(k)["region"] for k in cp.batches("reading") if cp.batch(k)["status"] == "deferred"]
    if deferred:
        st["status"] = "stopped"
        raise StopRun("deferred", f"rate limit: the reading of {deferred} is deferred (bounded backoff exhausted); "
                                  f"ingest needs it. Resume later: `tenderpack ai resume {ctx.run_id}`")
    missing = [cp.batch(k)["region"] for k in cp.batches("reading") if cp.batch(k)["status"] != "done"]
    if missing:
        st["status"] = "stopped"
        why = "; ".join(f"{cp.batch(k)['region']}: {_short(cp.batch(k).get('error'), 300)}"
                        for k in cp.batches("reading") if cp.batch(k)["status"] != "done")
        raise StopRun("stopped", f"no usable reading for the image region(s) {missing} ({why}); ingest cannot read the "
                                 f"addendum without them. Resume to ask again: `tenderpack ai resume {ctx.run_id}`")
    res = CAND.ingest(ctx.dir)
    st["reingest"] = {"exit_code": res["exit_code"], "units": res.get("units"), "pending_review": res.get("pending_review"),
                      "failed_checks": res.get("failed")}
    if res["exit_code"] != 0:
        st["status"] = "stopped"
        raise StopRun("stopped", f"ingest refused the candidate again after the proposed readings (exit "
                                 f"{res['exit_code']}): {res.get('reason') or res['status']}", code=2)
    ctx.say(f"  ingest with the proposed readings: ok ({res.get('units')} units; readings PENDING HUMAN REVIEW: "
            f"{res.get('pending_review')})")
    _after_ingest(ctx, st)


def _local_reading_check(ctx: Ctx, st: dict) -> None:
    """Session 12: on the ollama route the readings phase needs a local model that REPORTS image input (/api/show
    `vision`; never assumed). When the reading model (routes.ollama.models.vision, else the run's model) is missing,
    cannot be checked or does not report vision, the step is a visible "cannot run locally with this model": every
    reading still to do is ESCALATED to a person (status `escalated`, the reason on the batch, an event in the
    checkpoint and the run log), nothing is asked of the model, and the run stops with the reason and the way on
    (ingest refuses the candidate without the readings, C05, so the text phases cannot start)."""
    cp, s = ctx.cp, ctx.s
    if s["route"] != "ollama":
        return
    todo = [k for k in cp.batches("reading") if cp.batch(k)["status"] not in ("done", "skipped")]
    if not todo:
        return
    from .providers import make
    from .providers.base import ProviderError
    rcfg = C.route(ctx.cfg, "ollama")
    model = C.phase_model(rcfg, "ollama", "reading", s.get("model"))
    why = None
    try:
        caps = make("ollama", model, ctx.cfg, None).capabilities()
        if caps.images is not True:
            why = (f"{model} does not report image input (/api/show capabilities "
                   f"{caps.details.get('reported_capabilities')})")
    except (ProviderError, C.ConfigError) as e:
        why = f"{model}: {getattr(e, 'message', None) or e}"
    if why is None:
        for k in todo:                                           # a vision model is there now: asked as usual
            if cp.batch(k)["status"] == "escalated" and cp.batch(k).get("failure_class") == "capability":
                cp.batch(k).update(status="pending")
        cp.save()
        return
    reason = f"cannot run locally with this model: {why}"
    rdir = _readings_dir(ctx)
    regions = [cp.batch(k)["region"] for k in todo]
    for k in todo:
        cp.batch(k).update(status="escalated", failure_class="capability",
                           error=f"{reason}; escalated to a person (read the image region and record the reading)")
    cp.event("readings_escalated_to_person", regions=regions, reason=reason, model=model)
    ctx.log.event("readings_escalated_to_person", regions=regions, reason=reason, model=model)
    st.update(status="stopped", escalated=regions, reason=reason)
    raise StopRun("stopped", f"the readings step {reason}. The image region(s) {regions} are escalated to a person: "
                             "ingest refuses the candidate without their readings (C05), so the text phases cannot "
                             f"start. A person records each reading (PENDING HUMAN REVIEW) in {rdir} and resumes with "
                             f"`tenderpack ai resume {ctx.run_id} --from ingest`, or configures a local model that "
                             "reports vision (routes.ollama.models.vision) and resumes")


def _reading_batch(ctx: Ctx, st: dict, bid: str, rid: str) -> None:
    cp, s = ctx.cp, ctx.s
    b = cp.batch(bid)
    b.update(status="running", pid=os.getpid(), attempts=b.get("attempts", 0) + 1, started=now_iso())
    for k in ("error", "failure_class", "session"):          # a retry may take its recorded session again
        b.pop(k, None)
    cp.save()
    t0 = time.perf_counter()
    build = _failed_build(ctx)
    rws = Workspace(build, ctx.P["pack"], ROOT, ctx.dir / "ai", Path(s["worklog"]),
                    Path(s["ai_config"]) if s.get("ai_config") else None)
    try:
        packet = RR.packet(build, ctx.P["pack"], rid, _readings_dir(ctx), ctx.run_id, bid)
        path = ctx.dir / "batches" / f"{bid}.packet.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        if s["route"] == "host":
            packet["system"] = policy.compose("reading", "mcp", cfg=ctx.cfg)   # session 13: a person's coding host
            packet["workflow"] = {"run_id": ctx.run_id, "batch": bid, "phase": "reading",
                                  "submit_with": f"tenderpack ai submit-batch {ctx.run_id} FILE --by NAME --host-model MODEL",
                                  "tools": "the MCP tools get_region and validate_reading (serve-mcp --evidence "
                                           f"{build} --pack {ctx.P['pack']})"}
            path.write_text(json.dumps(packet, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
            b["packet"] = str(path)
            hs = _host_auto(ctx)
            if hs is None:
                b.update(status="waiting_for_host", waiting_since=now_iso(), waiting_epoch=time.time())
                cp.save()
                st["status"] = "waiting_for_host"
                raise WaitingForHost(_wait_message(ctx, bid))
            prop, who = _reading_host_session(ctx, hs, rws, bid, packet)
        else:
            path.write_text(json.dumps(packet, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
            b["packet"] = str(path)
            if s["route"] == "recorded":
                prov, sess = ctx.cassette.provider("reading", [rid], ctx.used_sessions())
                if prov is None:
                    raise BatchFailed("no recorded session covers this region (the cassette does not record it)")
                b["session"] = sess
            else:
                from .providers import make
                rcfg = C.route(ctx.cfg, s["route"])
                prov = make(s["route"], C.phase_model(rcfg, s["route"], "reading", s.get("model")), ctx.cfg, None)
            prop = _converse(ctx, prov, packet, bid, parse=RR.parse, task=RR.READING_TASK, ws=rws)
            who = f"{s['route']} route, model {prov.model}"
        _take_reading(ctx, bid, rid, prop, who)
    except Deferred as e:
        _defer(ctx, bid, e)
    except R.TooLarge as e:                                      # one region cannot be split: escalated with its size
        b.update(status="escalated", failure_class="too_large", size=getattr(e.size, "to_dict", lambda: None)(),
                 error=f"escalated: {e} (a person reads or splits this region)")
    except BatchFailed as e:
        b.update(status="failed", error=str(e))
    except (B.Refused, RR.RegionError) as e:
        b.update(status="failed", error=f"refused: {e}")
    finally:
        b["seconds"] = round(b.get("seconds", 0.0) + time.perf_counter() - t0, 3)
        if b["status"] == "running":
            b["status"] = "interrupted"
        cp.save()
    ctx.say(f"  {bid}: {b['status']}" + (f" ({_short(b.get('error'), 300)})" if b.get("error") else
                                         f" ({b.get('verification_status')}; {b.get('reading_file')})"))


def _take_reading(ctx: Ctx, bid: str, rid: str, prop, who: str) -> None:
    """Validate a proposed reading; write it into the candidate's readings when it can be used (PENDING HUMAN REVIEW)."""
    cp = ctx.cp
    b = cp.batch(bid)
    build = _failed_build(ctx)
    try:
        known = {u["unit_id"] for u in json.loads((build / "units.json").read_text(encoding="utf-8"))["units"]}
    except (OSError, ValueError, KeyError):
        known = set()
    prepared_by = (f"AI-assisted: {who}, in AI workflow run {ctx.run_id} ({bid}), {now_iso()}; proposed for a person's "
                   "review, not approved")
    report = RR.validate(build, ctx.P["pack"], prop, rid, prepared_by, known)
    res_path = ctx.dir / "batches" / f"{bid}.result.json"
    res_path.write_text(json.dumps({"proposal": prop.model_dump(mode="json"), "controller": report}, ensure_ascii=False,
                                   indent=1, default=str), encoding="utf-8")
    b.update(result=str(res_path), verification_status=prop.verification_status, model_requested=prop.model_requested,
             model_reported=prop.model_reported)
    if prop.verification_status not in DS.PROMOTABLE:
        bad = [v.detail for v in prop.validation if not v.ok]
        b.update(status="failed", error=f"the proposed reading is {prop.verification_status}: " + "; ".join(bad)[:900])
        return
    f = RR.write(_readings_dir(ctx), prop, ctx.run_id)
    b.update(status="done", reading_file=str(f), unit_id=prop.reading.get("unit_id"))
    cp.event("reading_written", region=rid, file=str(f), status=prop.verification_status)


# session 13: the host-answer mechanics of the runtime policy (tenderpack/ai/policy/80_routes.md), for reference;
# AnswerSession(phase=...) composes them itself (policy.compose)
READING_HOST_RULES = policy.mechanics("reading", "host")
DOWNSTREAM_HOST_RULES = policy.mechanics("downstream", "host")


def _reading_host_session(ctx: Ctx, hs, rws: Workspace, bid: str, packet: dict):
    """A reading in a headless host session over the MCP tools (get_region shows the images; validate_reading checks the
    draft); the session's final message is the proposal. It writes nothing and submits nothing. Through the request
    layer: the host's declared image input checked (the reading phase requires it), the size, the failure classes and
    one bounded repair of a malformed answer."""
    sess = hs.AnswerSession(rws, ctx.cfg, phase="reading", model=ctx.s.get("host_session_model"),
                            run_lock=ctx.run_lock is not None)
    pk = dict(packet, addendum=ctx.addendum, provisions=[])
    fields = {"run_id": f"{ctx.run_id}-{bid}", "created": now_iso(), "route": "host", "provider": "host-session",
              "model_requested": sess.host_model_label(), "model_reported": None, "task": RR.READING_TASK}
    try:
        out = _host_request(ctx, bid, R.spec("reading", system=sess.system_prompt()), sess, pk, fields, rws)
    finally:
        last = sess.last
        if last is not None:
            ctx.cp.batch(bid)["host_session"] = {"run_id": last.run_id, "elapsed_s": last.elapsed_s,
                                                 "error": last.error, "model_reported": last.model_reported,
                                                 "tool_calls": len(last.tool_calls),
                                                 "failure_class": last.failure_class,
                                                 "note": "the session's final message is the proposed reading"}
            ctx.cp.intervention(kind="host session (automatic)", batch=bid, by="tenderpack.ai.hostsession",
                                host_model=sess.host_model_label(),
                                note="a headless host session reading an image; not a person")
    who = (f"headless host session {last.run_id} ({sess.host_model_label()}; the CLI reported "
           f"{', '.join(last.model_reported or []) or 'no model'})")
    return out.answer, who


# ---------------------------------------------------------------------------------------------- step: analysis

def _section(pid: str) -> str:
    local = pid.split(":", 1)[1] if ":" in pid else pid
    if "/" in local:
        return local.split("/")[0]
    m = re.match(r"^(\d+)[.(]", local)
    if m:
        return m.group(1)
    m = re.match(r"^([A-Za-z]+)\d+$", local)
    return m.group(1) if m else local


def plan_batches(provisions: list[str], size: int) -> list[list[str]]:
    """Provisions in document order, a section kept in one batch where it fits, at most `size` per batch; every
    provision in exactly one batch."""
    groups: list[list[str]] = []
    for p in provisions:
        if groups and _section(groups[-1][-1]) == _section(p):
            groups[-1].append(p)
        else:
            groups.append([p])
    out: list[list[str]] = []
    for g in groups:
        for i in range(0, len(g), size):
            part = g[i:i + size]
            if out and len(out[-1]) + len(part) <= size and i == 0:
                out[-1] += part
            else:
                out.append(list(part))
    assert [p for b in out for p in b] == list(provisions), "a batch plan lost or reordered a provision"
    return out


def _route_caps(ctx: Ctx):
    """The capabilities the run's requests are held to, for planning: the cassette's (recorded), the host's DECLARED
    ones (host), the endpoint's verified ones (API routes; raises when the endpoint does not verify them)."""
    route = ctx.s["route"]
    if route == "host":
        from .hostsession import declared_capabilities
        return declared_capabilities(ctx.cfg)
    if route == "recorded":
        from .providers.recorded import RecordedProvider
        return RecordedProvider({"capabilities": ctx.cassette.data.get("capabilities"), "turns": []}).capabilities()
    return _make_provider(ctx).capabilities()


def _make_provider(ctx: Ctx):
    from .providers import make
    rcfg = C.route(ctx.cfg, ctx.s["route"])
    return make(ctx.s["route"], C.phase_model(rcfg, ctx.s["route"], "analysis", ctx.s.get("model")), ctx.cfg, None)


def _max_out(ctx: Ctx) -> int | None:
    if ctx.s["route"] == "host":
        return None
    return C.caps(ctx.cfg, ctx.s["route"], ctx.remaining_caps()).get("max_tokens_per_call")


def _context_budget(ctx: Ctx):
    """(fits(ids) -> bool, units {id: packet entry}, source) for planning the analysis batches: the request layer's
    complete accounting (system, tool definitions, the packet as sent, images, later turns, the expected output) with
    estimates per provision. Raises when the route's capabilities or the packet cannot be had (the caller reports it)."""
    from . import batching
    from .providers.recorded import PACKET_MARK
    caps = _route_caps(ctx)
    packet = R.compact_analysis(controller.task_packet(ctx.ws, ctx.addendum))
    sp = R.spec("analysis", route=ctx.s["route"], cfg=ctx.cfg)      # session 13: the route's policy composition
    st = R.settings_for(ctx.cfg, ctx.s["route"])
    cpt = float(st.get("chars_per_token", 3.5))

    def tok(x) -> int:
        return int(len(json.dumps(x, ensure_ascii=False, default=str)) / cpt) + 1
    ref = packet.get("reference") or {}
    fixed = tok({k: v for k, v in packet.items() if k not in ("provisions", "crops", "targets", "reference")}) \
        + tok({k: v for k, v in ref.items() if k not in ("ops", "dispositions")}) + tok(PACKET_MARK)
    crops = Counter(c.get("unit_id") for c in packet.get("crops") or [])
    per: dict[str, tuple[int, int]] = {}
    for p in packet.get("provisions") or []:
        u = p["unit_id"]
        mine = [x for x in (ref.get("ops") or []) + (ref.get("dispositions") or []) if x.get("provision") == u]
        per[u] = (tok(p) + sum(tok(packet["targets"].get(t)) for t in p.get("candidate_targets") or []) + tok(mine),
                  crops.get(u, 0))
    tools_spec = [controller.TOOLS[n].spec() for n in sp.tools]
    maxout = _max_out(ctx)

    def fits(ids: list[str]) -> bool:
        sz = batching.request_size("analysis", caps, system=sp.system, tools=tools_spec,
                                   packet_tokens=fixed + sum(per.get(i, (0, 0))[0] for i in ids),
                                   images=sum(per.get(i, (0, 0))[1] for i in ids), units=len(ids),
                                   max_output_tokens=maxout, settings=st)
        return sz.fits
    units = {p["unit_id"]: p for p in packet.get("provisions") or []}
    return fits, units, caps.source


def _fit_to_context(ctx: Ctx, batches: list[list[str]], budget=None) -> tuple[list[list[str]], list[str]]:
    """Every route (session 11): split a planned batch whose request would not fit the route's context window or output
    cap, with the request layer's complete accounting (system, tool definitions, the packet as sent, images, later
    turns, the expected output). The sizes here are estimates per provision; the request layer checks the exact
    request again before it is sent and the batch is split further, or a single provision escalated, if needed."""
    from . import batching
    try:
        fits_ids, _, source = budget or _context_budget(ctx)
    except Exception as e:                                       # noqa: BLE001 (the count plan stands; reported)
        return batches, [f"context fit not checked at planning: {type(e).__name__}: {_short(str(e), 300)} (each "
                         "request is still checked before it is sent)"]

    def fits(group: list[dict]) -> bool:
        return fits_ids([g["unit_id"] for g in group])
    out, notes = [], []
    for b in batches:
        for g in batching.plan_units([{"unit_id": p} for p in b], fits):
            ids = [x["unit_id"] for x in g]
            out.append(ids)
            if len(ids) == 1 and not fits(g):
                notes.append(f"{ids}: does not fit even alone (estimate); it is escalated with its size at its request")
    if len(out) != len(batches):
        notes.append(f"{len(batches)} planned batch(es) split into {len(out)} to fit the context window and the "
                     f"output cap ({source})")
    return out, notes


def _plan_analysis(ctx: Ctx, provisions: list[str], size: int) -> tuple[list[list[str]], list[str]]:
    """Session 13 (D): the analysis batches planned by STRUCTURE within the token budget (batching.plan_structured:
    an image region with its elements, a table with its rows and notes, a clause with its lettered items, the answers
    under one heading, provisions a table reference links), then checked against the context as before. Without a
    budget (the route's capabilities or the packet unavailable at planning) the count plan stands, as before."""
    from . import batching
    try:
        budget = _context_budget(ctx)
    except Exception as e:                                       # noqa: BLE001 (reported; requests still checked)
        return plan_batches(provisions, size), [
            f"context fit not checked at planning: {type(e).__name__}: {_short(str(e), 300)} (each request is still "
            "checked before it is sent); batches planned by count"]
    fits_ids, units, _ = budget
    plan = batching.plan_structured(provisions, size, units=units, fits=fits_ids)
    plan, notes = _fit_to_context(ctx, plan, budget)
    groups = [b for b in plan if len(b) > size]
    if groups:
        notes.append(f"{len(groups)} batch(es) of one structure kept whole beyond {size} provisions within the token "
                     f"budget: " + ", ".join(f"{b[0]}..{b[-1]} ({len(b)})" for b in groups))
    return plan, notes


def _defer(ctx: Ctx, bid: str, e: "Deferred") -> None:
    b = ctx.cp.batch(bid)
    b.update(status="deferred", failure_class="rate_limit", error=f"deferred: {e.message}")
    b.setdefault("deferrals", []).append({"ts": now_iso(), "message": _short(e.message, 400),
                                          "reset_in_s": e.reset_in_s})
    ctx.deferred_in_drive = True
    ctx.cp.event("batch_deferred", batch=bid, reason=_short(e.message, 300), reset_in_s=e.reset_in_s)


def _stop_if_deferred(ctx: Ctx, st: dict, bid: str) -> None:
    """After a batch (or its critic) was deferred for a rate limit: stop the run cleanly (failures.rate_limit.on_deferred
    stop, the default; everything done so far is checkpointed) or go on (continue: later requests in this drive get one
    try each, no backoff)."""
    b = ctx.cp.batch(bid)
    crit = (b.get("critic") or {}).get("status") == "deferred"
    if b["status"] != "deferred" and not crit:
        return
    ctx.deferred_in_drive = True
    if ctx.policy.on_deferred != "stop":
        return
    last = (b.get("deferrals") or [{}])[-1] if b["status"] == "deferred" else (b.get("critic") or {})
    reset = last.get("reset_in_s")
    stop = StopRun("deferred", f"rate limit: {bid}{' (its critic)' if b['status'] != 'deferred' else ''} was deferred "
                              f"after the bounded backoff ({_short(last.get('message') or last.get('error'), 200)}); "
                              "everything done so far is checkpointed"
                              + (f"; the provider names a reset in about {reset / 60:.0f} min" if reset else "")
                              + f". Resume later: `tenderpack ai resume {ctx.run_id}` (done batches are not asked again)")
    if ctx.prefetch is not None and ctx.prefetch.recs:
        if ctx.stop_pending is None:      # session 12: no new dispatch; the batches already asked are taken first
            ctx.stop_pending = stop
        return
    st["status"] = "stopped"
    raise ctx.stop_pending or stop


def _split(ctx: Ctx, bid: str, key: str, units: list, e) -> None:
    """A batch whose request does not fit: split in two (in order, each part asked in turn); a single unit that does not
    fit alone is escalated with its size. Never truncated."""
    cp = ctx.cp
    b = cp.batch(bid)
    sz = getattr(getattr(e, "size", None), "to_dict", lambda: None)()
    if len(units) <= 1:
        b.update(status="escalated", failure_class="too_large", size=sz,
                 error=f"escalated: a single {key[:-1]} whose request does not fit even alone ({e}); a person splits it")
        for u in units:
            if key == "provisions" and u in cp.data["provisions"] and cp.provision(u)["status"] == "pending":
                cp.set_provision(u, "unaccounted", reason=f"{bid}: too large for one request even alone "
                                                          f"({_short(str(e), 300)}); escalated for a person to split")
        cp.event("batch_escalated_too_large", batch=bid, size=sz)
        return
    half = (len(units) + 1) // 2
    parts = [units[:half], units[half:]]
    items = list(cp.data["batches"].items())
    i = next(n for n, (k, _) in enumerate(items) if k == bid)
    new = []
    for j, part in enumerate(parts, 1):
        nb = {"phase": b["phase"], key: part, "status": "pending", "attempts": 0, "seconds": 0.0, "split_from": bid}
        new.append((f"{bid}.{j}", nb))
    b.update(status="split", parts=[k for k, _ in new], size=sz, failure_class="too_large",
             error=f"split in {len(parts)}: the request does not fit ({_short(str(e), 300)})")
    cp.data["batches"] = dict(items[:i + 1] + new + items[i + 1:])
    for k, nb in new:
        for u in nb[key]:
            if key == "provisions" and u in cp.data["provisions"]:
                cp.provision(u)["batch"] = k
            elif key == "tasks" and u in cp.data["downstream"]["tasks"]:
                cp.data["downstream"]["tasks"][u]["batch"] = k
    cp.event("batch_split", batch=bid, parts=[k for k, _ in new], size=sz)
    cp.save()


def _next_batch(ctx: Ctx, phase: str, seen: set) -> str | None:
    bid = next((k for k in ctx.cp.batches(phase) if k not in seen), None)
    if bid is not None:
        seen.add(bid)
    return bid


def step_analysis(ctx: Ctx, st: dict) -> None:
    cp = ctx.cp
    if not cp.batches("analysis"):
        plan, notes = _plan_analysis(ctx, list(cp.data["provisions"]), int(ctx.s["batch_size"]))
        for n, provs in enumerate(plan, 1):
            bid = f"analysis-{n:03d}"
            cp.data["batches"][bid] = {"phase": "analysis", "provisions": provs, "status": "pending", "attempts": 0,
                                       "seconds": 0.0}
            for p in provs:
                cp.provision(p)["batch"] = bid
        st["plan_notes"] = notes
        cp.save()
        ctx.say(f"  {len(cp.data['provisions'])} provisions in {len(plan)} batch(es), planned by structure (up to "
                f"{ctx.s['batch_size']} per batch; one structure kept whole when it fits the token budget)")
    seen: set = set()
    while (bid := _next_batch(ctx, "analysis", seen)) is not None:
        b = cp.batch(bid)
        if b["status"] in ("skipped", "split", "escalated"):
            continue
        if ctx.stop_pending is not None and b["status"] != "done" and not (ctx.prefetch and bid in ctx.prefetch.recs):
            st["status"] = "stopped"
            raise ctx.stop_pending                    # session 12: the batches asked ahead were taken; now stop
        if b["status"] == "done":
            if (b.get("critic") or {}).get("status") in ("pending", "deferred") and b.get("staged_run"):
                _critic_analysis(ctx, bid)                   # a critic deferred (or never run) before: asked alone
                _stop_if_deferred(ctx, st, bid)
            continue
        if b["status"] == "waiting_for_host":
            st["status"] = "waiting_for_host"
            raise WaitingForHost(_wait_message(ctx, bid))
        todo = [p for p in b["provisions"] if cp.provision(p)["status"] == "pending"]
        if not todo:
            b.update(status="skipped", reason="every provision of the batch was accounted for by an earlier batch")
            cp.save()
            continue
        if ctx.stop_batches:
            b.update(status="failed", error=f"not run: {ctx.stop_batches}")
            cp.save()
            continue
        _fill(ctx, "analysis", bid)                   # session 12: batches at once (max_parallel_sessions > 1)
        _analysis_batch(ctx, st, bid, todo)
        if cp.batch(bid)["status"] == "done":
            # session 12 (blind-06 follow-up 14): the next batches are asked BEFORE this batch's critic, so no slot sits
            # idle while the critic runs; their answers are still taken in plan order (Prefetch.take checks the packet)
            _fill(ctx, "analysis", bid)
            _critic_analysis(ctx, bid)
        _stop_if_deferred(ctx, st, bid)
        if ctx.gate is not None:
            cp.data["rate_gate"] = ctx.gate.record()
    if ctx.stop_pending is not None:
        st["status"] = "stopped"
        raise ctx.stop_pending
    st["batches"] = {k: cp.batch(k)["status"] for k in cp.batches("analysis")}
    st["provisions"] = dict(Counter(v["status"] for v in cp.data["provisions"].values()))
    deferred = [k for k in cp.batches("analysis") if cp.batch(k)["status"] == "deferred"]
    if deferred:
        st["deferred"] = deferred


def _shown(ctx: Ctx, todo: list[str]) -> list[str]:
    """The provisions a batch's task packet shows (controller.task_packet selects by id or prefix)."""
    return [p for p in ctx.cp.data["provisions"] if any(p == x or p.startswith(x) for x in todo)]


# ---------------------------------------------------------------------------------------------- session 13: kept answers

def _submission_file(ctx: Ctx, bid: str) -> Path:
    """Where the MCP server of a batch's host session records its submission at once (serve-mcp --submission-record)."""
    return ctx.dir / "batches" / f"{bid}.submission.json"


def _submission_entry(ctx: Ctx, ps: ProposalSet, *, reused: bool, **extra) -> dict:
    """What the checkpoint keeps of a batch's submitted set: where it is staged and its validation result."""
    staging = B.safe_staging(ctx.ws.staging, ctx.ws.root, ctx.ws.evidence)
    return {"run_id": ps.run_id, "staging": str(staging / ps.run_id), "set_status": ps.status,
            "statuses": {it.id: it.verification_status for it in ps.items}, "validated": now_iso(), "reused": reused,
            **extra}


def _reuse_submission(ctx: Ctx, bid: str, todo: list[str]) -> ProposalSet | None:
    """Session 13 (D; blind-05 regression defect 2): a batch whose host session reached submit_proposals before the
    run was interrupted (a SIGTERM, a crash) or before a failure ended the session: its staged set is REUSED instead of
    asking the batch again, after revalidation against the CURRENT evidence and state (controller.validate_set and the
    freshness re-check, exactly as a new submission). It is not reused, and the batch is asked again with the reason
    recorded (`reuse_refused`, event submission_reuse_refused), when the record or the set does not load, the set is not
    usable (stale, malformed, provider_failed, budget_exhausted), the state identity changed since the submission, or an
    item is invalid now that was not at the submission. A session killed before its submission left no record."""
    f = _submission_file(ctx, bid)
    if not f.is_file():
        return None
    cp, ws = ctx.cp, ctx.ws
    b = cp.batch(bid)
    rec: dict = {}

    def refuse(reason: str) -> None:
        n = len(b.get("reuse_refused") or []) + 1
        b.setdefault("reuse_refused", []).append({"ts": now_iso(), "run_id": rec.get("run_id"), "reason": reason})
        cp.event("submission_reuse_refused", batch=bid, run_id=rec.get("run_id"), reason=_short(reason, 400))
        try:
            f.rename(f.with_name(f"{bid}.submission.refused-{n}.json"))       # kept for the record, never reused
        except OSError:
            pass
        cp.save()
        ctx.say(f"  {bid}: the submission {rec.get('run_id')} is not reused ({_short(reason, 200)}); asked again")
        return None
    try:
        rec = json.loads(f.read_text(encoding="utf-8")) or {}
        rid = B.check_run_id(str(rec.get("run_id") or ""))
    except (OSError, ValueError, B.Refused) as e:
        return refuse(f"the submission record does not read: {_short(str(e), 300)}")
    try:
        ps, _ = _load_staged(ws, rid)
    except Exception as e:                                       # noqa: BLE001 (asked again, with the reason)
        return refuse(f"the staged set {rid} does not load: {type(e).__name__}: {_short(str(e), 300)}")
    if ps.addendum != ctx.addendum:
        return refuse(f"the staged set {rid} is for {ps.addendum}, not {ctx.addendum}")
    if ps.status in ("malformed", "provider_failed", "budget_exhausted", "stale"):
        return refuse(f"the staged set {rid} is {ps.status}")
    before = {it.id: it.verification_status for it in ps.items}
    set_before = ps.status
    staging = B.safe_staging(ws.staging, ws.root, ws.evidence)
    log = RunLog(rid, [staging / rid / "log.jsonl"])
    report = controller.validate_set(ws, ps, log, expected_addendum=ctx.addendum,
                                     reference=controller._reference_path(ws, ctx.addendum))
    fresh = controller.recheck_fresh(ws, ps, report)
    if report.get("state_differences") or not fresh or ps.status == "stale":
        return refuse("the evidence or state changed since the submission: "
                      + "; ".join(report.get("state_differences") or ["the inputs changed while it was validated"]))
    after = {it.id: it.verification_status for it in ps.items}
    worse = [i for i, s_ in after.items() if s_ == "invalid" and before.get(i) != "invalid"]
    if worse:
        return refuse(f"revalidated against the current evidence and state, {len(worse)} item(s) are invalid now that "
                      f"were not at the submission: {', '.join(worse[:8])}")
    report["reused"] = {"workflow_run": ctx.run_id, "batch": bid, "statuses_at_submission": before,
                        "set_status_at_submission": set_before}
    controller.write_staging(ws, ps, report)             # the staged set now carries the current validation
    log.event("revalidated_for_reuse", workflow_run=ctx.run_id, batch=bid, set_status=ps.status, statuses=after,
              statuses_at_submission=before)
    b["submission"] = _submission_entry(ctx, ps, reused=True, revalidated=now_iso(), submitted=rec.get("ts"),
                                        statuses_at_submission=before)
    cp.event("submission_reused", batch=bid, run_id=rid, set_status=ps.status, submitted=rec.get("ts"))
    # session 14 (W2; blind-07 defect 15): the reused answer is an intervention record too, with when it was made
    cp.data["interventions"].append({"ts": now_iso(), "kind": "submission reused (automatic)", "batch": bid,
                                     "by": "tenderpack.ai.workflow", "run_id": rid, "submitted": rec.get("ts"),
                                     "note": f"the host session's staged set {rid} ({_made_when(cp.data, rec.get('ts'))})"
                                             " was revalidated and taken instead of asking the batch again"})
    cp.save()
    ctx.say(f"  {bid}: the submission {rid} (submitted {rec.get('ts') or 'earlier'}) is reused after revalidation "
            f"({ps.status})")                   # session 13 (blind-07 scorer): it may have been made after a resume
    return ps


def _analysis_batch(ctx: Ctx, st: dict, bid: str, todo: list[str]) -> None:
    """One analysis batch through the request layer (recorded, API and host routes alike; see the module docstring)."""
    cp, s = ctx.cp, ctx.s
    b = cp.batch(bid)
    b.update(status="running", pid=os.getpid(), attempts=b.get("attempts", 0) + 1, started=now_iso())
    for k in ("error", "failure_class", "session"):          # a retry may take its recorded session again
        b.pop(k, None)
    cp.save()
    t0 = time.perf_counter()
    try:
        if s["route"] == "host":
            ps = _reuse_submission(ctx, bid, todo)       # session 13 (D): a submission made before an interruption
            if ps is None:
                ps = _host_analysis(ctx, st, bid, todo)
                if ps.status not in ("provider_failed", "malformed", "budget_exhausted"):
                    b["submission"] = _submission_entry(ctx, ps, reused=False)
        else:
            if s["route"] == "recorded":
                pre = ctx.prefetch.peek(bid) if ctx.prefetch else None
                prov, sess = ((pre["prov"], pre["session"]) if pre else
                              ctx.cassette.provider("analysis", todo, ctx.used_sessions()))
                if prov is None:
                    raise BatchFailed("no recorded session covers this batch (the cassette does not record it)")
                b["session"] = sess
            else:
                prov = _make_provider(ctx)
            ps = _analysis_request(ctx, bid, todo, prov)
        _take_analysis(ctx, bid, ps, todo)
        for m in b.get("malformed_items") or []:                 # items set aside after the one repair
            p = m.get("provision")
            if p in cp.data["provisions"] and cp.provision(p)["status"] == "unaccounted":
                cp.provision(p)["reason"] = (f"{bid}: its item {m.get('id')!r} was malformed after the bounded repair: "
                                             + _short("; ".join(m.get("errors") or []), 300))
    except Deferred as e:
        _defer(ctx, bid, e)
    except R.TooLarge as e:
        _split(ctx, bid, "provisions", todo, e)
    except BatchFailed as e:
        b.update(status="failed", error=str(e))
    except B.Refused as e:
        b.update(status="failed", error=f"refused: {e}")
        ctx.stop_batches = f"the route refused {bid}: {_short(str(e), 300)}"
    finally:
        b["seconds"] = round(b.get("seconds", 0.0) + time.perf_counter() - t0, 3)
        if b["status"] == "running":
            b["status"] = "interrupted"
        cp.save()
    ctx.say(f"  {bid}: {b['status']}" + (f" ({b.get('error')})" if b.get("error") else
                                         f" ({len(b.get('items') or [])} item(s); run {b.get('staged_run')})"))


def _take_analysis(ctx: Ctx, bid: str, ps: ProposalSet, todo: list[str]) -> None:
    cp, ws = ctx.cp, ctx.ws
    b = cp.batch(bid)
    b.update(staged_run=ps.run_id, set_status=ps.status, model_requested=ps.model_requested,
             model_reported=ps.model_reported)
    cp.add_usage(ps.usage.calls, ps.usage.input_tokens, ps.usage.output_tokens, ps.usage.cost_usd)
    _mirror_spend(ctx)
    if ps.status in ("malformed", "provider_failed", "budget_exhausted", "stale"):
        b.update(status="failed", error=f"the proposal set is {ps.status}")
        if ps.status == "budget_exhausted":
            ctx.stop_batches = "the run's budget is exhausted"
        return
    _, report = _load_staged(ws, ps.run_id)
    shown = _shown(ctx, todo)
    pend = [p for p in shown if cp.provision(p)["status"] == "pending"]
    take = [it for it in ps.items if it.provision in pend]
    b.update(items=[it.id for it in take], ignored_items=[it.id for it in ps.items if it.provision not in pend],
             shown=shown)
    sim_ops = {o["id"]: o for o in (report.get("simulation") or {}).get("ops", [])}
    covered: dict[str, list[str]] = {}
    for it in take:
        if it.statement_type == "amendment_op" and it.verification_status != "invalid":
            oid = it.payload.get("id", it.id)
            so = sim_ops.get(oid) or {}
            for c in list(it.payload.get("covers") or []) + (list(so.get("content") or []) if so.get("valid") else []):
                covered.setdefault(c, []).append(it.id)
    unacc = set(ps.coverage.unaccounted)
    for p in cp.data["provisions"]:
        if cp.provision(p)["status"] != "pending":
            continue
        mine = [it for it in take if it.provision == p]
        if mine:
            cp.set_provision(p, "proposed", batch=bid, items=[it.id for it in mine])
            cp.set_provision(p, "validated", accounted=p not in unacc,
                             statuses={it.id: it.verification_status for it in mine})
        elif covered.get(p) and p not in unacc:
            cp.set_provision(p, "proposed", accounted_by=covered[p], answered_in=bid)
            cp.set_provision(p, "validated", accounted=True, statuses={})
        elif p in todo:
            cp.set_provision(p, "unaccounted", reason=f"{bid} gave no item that accounts for it")
    b["status"] = "done"


def _mirror_spend(ctx: Ctx) -> None:
    """The batches' spend entries (run folder) copied to the persistent meter staging/ai/spend.jsonl once each."""
    src = ctx.dir / "ai" / "spend.jsonl"
    if not src.exists():
        return
    lines = src.read_text(encoding="utf-8").splitlines()
    done = int(ctx.cp.data.get("spend_mirrored", 0))
    new = lines[done:]
    if new:
        with open(Path(ctx.s["staging"]) / "spend.jsonl", "a", encoding="utf-8") as fh:
            fh.write("\n".join(new) + "\n")
        ctx.cp.data["spend_mirrored"] = len(lines)


def _wait_message(ctx: Ctx, bid: str) -> str:
    b = ctx.cp.batch(bid)
    return (f"WAITING FOR THE HOST: batch {bid} ({b['phase']}). The task packet is {b.get('packet')}. Submit the set with:\n"
            f"  tenderpack ai submit-batch {ctx.run_id} FILE --by \"Your Name or session\" --host-model \"MODEL\""
            + (f" --out {ctx.s['staging']}" if Path(ctx.s["staging"]) != ROOT / "staging/ai" else "")
            + "\nThe run then continues by itself (or with `tenderpack ai resume`).")


def _host_auto(ctx: Ctx):
    hs = _hostsession() if ctx.s.get("host_mode", "auto") != "manual" else None
    if hs is None:
        return None
    s = hs.settings(ctx.cfg) if hasattr(hs, "settings") else {}
    binary = s.get("claude_bin", "claude")
    return hs if (shutil.which(binary) or Path(binary).exists()) else None


def _host_analysis(ctx: Ctx, st: dict, bid: str, todo: list[str]) -> ProposalSet:
    """An analysis batch on the host route: a headless host session (or the manual path: the packet is written and the
    run waits for `submit-batch`). Through the request layer: the host's declared capabilities (image input when the
    packet names image targets) and the complete size are checked before the session starts; a rate limit backs off and
    then defers the batch; a CLI failure is retried once and then fails it; a session that ends without a usable
    submission gets ONE bounded repair (a plain session given its answer and the errors), whose result is submitted to
    the controller like any submission."""
    cp, ws = ctx.cp, ctx.ws
    b = cp.batch(bid)
    hs = _host_auto(ctx)
    packet = _host_analysis_packet(ctx, hs, bid, todo)
    b["packet"] = str(ctx.dir / "batches" / f"{bid}.packet.json")
    if hs is None:
        b.update(status="waiting_for_host", waiting_since=now_iso(), waiting_epoch=time.time())
        cp.save()
        st["status"] = "waiting_for_host"
        raise WaitingForHost(_wait_message(ctx, bid))
    from .providers.base import collect_notices
    pre = ctx.prefetch.take(bid, Prefetch.key(packet)) if ctx.prefetch else None
    sess = pre["sess"] if pre else hs.HostSession(ws, ctx.cfg, model=ctx.s.get("host_session_model"),
                                                  run_lock=ctx.run_lock is not None)
    sess.submission_record = _submission_file(ctx, bid)        # session 13 (D): kept through an interruption
    sp = R.spec("analysis", system=sess.system_prompt())
    run_id, log, staging = _batch_log(ctx, bid, ws)
    out = R.Outcome("analysis", run_id=run_id)
    box: dict = {}
    n_img = R.packet_images(packet)
    with collect_notices() as notes:
        try:
            caps = sess.capabilities()
            R.require(sp, caps, n_img, "host", sess.host_model_label())
            sz = R.size(sp, caps, sess.prompt(packet), system=sess.system_prompt(),
                        tools_spec=[controller.TOOLS[n].spec() for n in sp.tools], images=n_img,
                        units=len(packet.get("provisions") or []), settings=R.settings_for(ctx.cfg, "host"))
            out.size = sz.to_dict()
            log.event("start", route="host", phase="analysis", batch=bid, provisions=todo, size=sz.to_dict(),
                      policy=ctx.policy.to_dict(), capabilities=caps.to_dict())
            R.check_size(sp, sz)

            def run():
                box["data"] = sess.run_batch(packet)
                last = sess.last
                out.host_sessions.append({"run_id": last.run_id, "elapsed_s": last.elapsed_s, "error": last.error,
                                          "failure_class": last.failure_class, "crops_read": last.crops_read,
                                          "model_reported": last.model_reported, "reset_in_s": last.reset_in_s})
                return last

            def rec(a):
                out.attempts.append(a)
                log.event("host_failure", **a)
            if pre is not None:                          # session 12: the session already ran in a worker
                for a in pre["attempts"]:
                    rec(a)
                out.host_sessions += pre["sessions"]
                got = Prefetch.result(pre)
                res, box["data"] = got["res"], got["data"]
            else:
                res = R.call_host(run, ctx.policy, sleep=ctx.sleep, rng=ctx.rng, record=rec)
            ps = ProposalSet.model_validate(box["data"])
            if ps.status in ("provider_failed", "malformed"):
                ps = _host_analysis_repair(ctx, bid, sp, sess, packet, ps, res, out, log, staging, rec)
        except R.RateLimited as e:
            out.notices = list(notes)
            _record_request(ctx, bid, out, "rate_limit")
            raise Deferred(e.message, e.reset_in_s) from None
        except R.ProviderFailed as e:
            out.notices = list(notes)
            _record_request(ctx, bid, out, "provider")
            raise BatchFailed(f"provider failure: {e.message}") from None
        except R.TooLarge:
            out.notices = list(notes)
            _record_request(ctx, bid, out, "too_large")
            raise
        finally:
            last = sess.last
            if last is not None:
                b["host_session"] = {"run_id": last.run_id, "elapsed_s": last.elapsed_s, "error": last.error,
                                     "crops_read": last.crops_read, "model_reported": last.model_reported,
                                     "failure_class": last.failure_class, "sessions": len(out.host_sessions)}
                cp.intervention(kind="host session (automatic)", batch=bid, by="tenderpack.ai.hostsession",
                                host_model=sess.host_model_label(), sessions=len(out.host_sessions),
                                note="a headless host session over the MCP tools; not a person")
        out.notices = list(notes)
    log.event("end", phase="analysis", batch=bid, staged_run=ps.run_id, set_status=ps.status,
              statuses={it.id: it.verification_status for it in ps.items}, repaired=out.repaired,
              malformed_items=out.malformed_items, host_sessions=out.host_sessions, notices=out.notices)
    _record_request(ctx, bid, out)
    return ps


def _host_analysis_packet(ctx: Ctx, hs, bid: str, todo: list[str]) -> dict:
    """The task packet of a host analysis batch (written to batches/<bid>.packet.json, private crop paths left out)."""
    ws = ctx.ws
    packet = (hs.host_packet(ws, ctx.addendum, todo) if hs and hasattr(hs, "host_packet")
              else controller.host_task(ws, ctx.addendum, claim=False, provisions=todo))
    packet = ANS.with_answers(ctx, R.compact_analysis(packet), "analysis", bid)     # session 14 (W5): owner's answers
    packet["workflow"] = {"run_id": ctx.run_id, "batch": bid, "phase": "analysis", "answer_only": todo,
                          "note": "answer the provisions in answer_only; any other provision in the packet belongs to "
                                  "another batch",
                          "submit_with": f"tenderpack ai submit-batch {ctx.run_id} FILE --by NAME --host-model MODEL"}
    path = ctx.dir / "batches" / f"{bid}.packet.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({k: v for k, v in packet.items() if k != "crops"} | {
        "crops": [{k: v for k, v in c.items() if not k.startswith("_")} for c in packet.get("crops") or []]},
        ensure_ascii=False, indent=1), encoding="utf-8")
    return packet


def _prep_analysis(ctx: Ctx, bid: str) -> dict | None:
    """Session 12 (Prefetch): an analysis batch asked ahead: the packet built here (the run's thread), the exchange
    with the model in a worker. None when the batch is not one to ask ahead (it is then asked in its turn)."""
    cp, s = ctx.cp, ctx.s
    b = cp.batch(bid)
    todo = [p for p in b["provisions"] if cp.provision(p)["status"] == "pending"]
    if not todo:
        return None
    n = int(b.get("attempts", 0)) + 1
    if s["route"] == "host":
        hs = _host_auto(ctx)
        if hs is None or _submission_file(ctx, bid).is_file():     # session 13: a kept submission is checked in turn
            return None
        packet = _host_analysis_packet(ctx, hs, bid, todo)
        sess = hs.HostSession(ctx.ws, ctx.cfg, model=s.get("host_session_model"), run_lock=ctx.run_lock is not None)
        sess.submission_record = _submission_file(ctx, bid)
        sp = R.spec("analysis", system=sess.system_prompt())
        caps = sess.capabilities()
        n_img = R.packet_images(packet)
        R.require(sp, caps, n_img, "host", sess.host_model_label())
        sz = R.size(sp, caps, sess.prompt(packet), system=sess.system_prompt(),
                    tools_spec=[controller.TOOLS[t].spec() for t in sp.tools], images=n_img,
                    units=len(packet.get("provisions") or []), settings=R.settings_for(ctx.cfg, "host"))
        if not sz.fits:
            return None
        pol, attempts, sessions = ctx.policy, [], []

        def work():
            box: dict = {}

            def run():
                box["data"] = sess.run_batch(packet)
                last = sess.last
                sessions.append({"run_id": last.run_id, "elapsed_s": last.elapsed_s, "error": last.error,
                                 "failure_class": last.failure_class, "crops_read": last.crops_read,
                                 "model_reported": last.model_reported, "reset_in_s": last.reset_in_s})
                return last
            res = R.call_host(run, pol, sleep=ctx.sleep, rng=ctx.rng, record=attempts.append)
            return {"res": res, "data": box.get("data")}
        return {"key": Prefetch.key(packet), "sess": sess, "attempts": attempts, "sessions": sessions, "work": work}
    if s["route"] != "recorded":
        return None
    ws = ctx.ws
    ws.refresh()
    ws.require_ok()
    raw = controller.task_packet(ws, ctx.addendum, todo)
    images = [{"type": "image", "path": c["_path"], "sha256": c["sha256"], "media_type": c["media_type"]}
              for c in raw["crops"]]
    packet = ANS.with_answers(ctx, R.compact_analysis(dict(raw, crops=[{k: v for k, v in c.items() if not k.startswith("_")}
                                                                      for c in raw["crops"]])), "analysis", bid)   # s14 (W5)
    prov, sess = ctx.cassette.provider("analysis", todo, ctx.used_sessions())
    if prov is None:
        return None
    return _prep_converse(ctx, bid, R.spec("analysis", route=ctx.s["route"], cfg=ctx.cfg), prov, sess, packet, n,
                          images=images)


def _prep_converse(ctx: Ctx, bid: str, sp, prov, sess, packet: dict, n: int, images=None) -> dict:
    """A provider conversation asked ahead (Prefetch): its own workspace for the tools, log and staging folder."""
    a = _request_args(ctx, sp, prov, bid, n=n)
    pol = ctx.policy
    route = ctx.s["route"]
    a["log"].event("start", route=route, provider=prov.name, model_requested=prov.model, task=sp.task, phase=sp.phase,
                   batch=bid, caps=a["caps_"], cassette=getattr(prov, "cassette_path", None), policy=pol.to_dict(),
                   asked_ahead=True)
    s = ctx.s
    wsn = Workspace(ctx.P["build"], ctx.P["pack"], ROOT, ctx.dir / "ai", Path(s["worklog"]),
                    Path(s["ai_config"]) if s.get("ai_config") else None)

    def work():
        return R.converse(sp, prov, packet, ws=wsn, route=route, caps_=a["caps_"], price=a["price"], policy=pol,
                          log=a["log"], staging=a["staging"], run_id=a["run_id"], fields=a["fields"],
                          sleep=ctx.sleep, rng=ctx.rng, images=images, settings=R.settings_for(ctx.cfg, route))
    return {"key": Prefetch.key(packet), "prov": prov, "session": sess, "work": work}


def _prep_downstream(ctx: Ctx, bid: str, by_id: dict | None = None, promoted: dict | None = None,
                     total: int = 0) -> dict | None:
    """Session 12 (Prefetch): a downstream batch asked ahead (see _prep_analysis)."""
    cp, s = ctx.cp, ctx.s
    b = cp.batch(bid)
    batch = [by_id[t] for t in b["tasks"] if t in (by_id or {})]
    if not batch:
        return None
    n = int(b.get("attempts", 0)) + 1
    packet = _downstream_packet(ctx, batch, promoted, total)
    if s["route"] == "host":
        hs = _host_auto(ctx)
        if hs is None:
            return None
        packet = _host_downstream_packet(ctx, bid, packet)
        sess = hs.AnswerSession(ctx.ws, ctx.cfg, phase="downstream",
                                model=s.get("host_session_model"), run_lock=ctx.run_lock is not None)
        sp = R.spec("downstream", system=sess.system_prompt())
        run_id, log, staging = _batch_log(ctx, bid, n=n)
        fields = {"run_id": run_id, "created": now_iso(), "route": "host", "provider": "host-session",
                  "model_requested": sess.host_model_label(), "model_reported": None, "task": DOWNSTREAM_TASK}
        log.event("start", route="host", phase=sp.phase, batch=bid, model_requested=sess.host_model_label(),
                  policy=ctx.policy.to_dict(), asked_ahead=True)
        pol = ctx.policy

        def work():
            return R.ask_host(sp, sess, packet, cfg=ctx.cfg, policy=pol, log=log, fields=fields,
                              cwd=staging / run_id, sleep=ctx.sleep, rng=ctx.rng,
                              settings=R.settings_for(ctx.cfg, "host"))
        return {"key": Prefetch.key(packet), "sess": sess, "work": work}
    if s["route"] != "recorded":
        return None
    prov, sess = ctx.cassette.provider("downstream", [t["id"] for t in batch], ctx.used_sessions())
    if prov is None:
        return None
    return _prep_converse(ctx, bid, R.spec("downstream", route=ctx.s["route"], cfg=ctx.cfg), prov, sess, packet, n)


def _host_analysis_repair(ctx: Ctx, bid: str, sp, sess, packet: dict, ps: ProposalSet, res, out, log, staging, rec):
    """The one bounded repair of a host analysis batch without a usable submission (see _host_analysis)."""
    ws = ctx.ws
    fields = R._dummy_fields(sp)
    previous, env = None, []
    if ps.status == "malformed":                                 # submitted, but the controller could not parse it
        try:
            ev = [json.loads(x) for x in (staging / ps.run_id / "log.jsonl").read_text(encoding="utf-8").splitlines()]
            raw = next((e.get("proposal") for e in ev if e.get("event") == "submitted"), None)
            env = [e.get("error") for e in ev if e.get("event") == "parse_error"] or ["the submitted set does not parse"]
            previous = json.dumps(raw, ensure_ascii=False) if raw is not None else None
        except (OSError, ValueError):
            previous = None
    else:                                                        # ended without a submission
        text = res.final_text or ""
        data, e1, p1 = R.check(sp, text, packet, fields)
        if data is not None and not e1 and not p1:               # it replied with the set instead of submitting it
            sub = controller.submit(ws, data, sess.host_model_label(), via=f"workflow {ctx.run_id} {bid} (final message)")
            log.event("submitted_from_final_message", run_id=sub["run_id"], status=sub["status"])
            return _load_staged(ws, sub["run_id"])[0]
        previous = text if data is not None or "{" in text else None
        env = [res.error or "the session ended without submitting through submit_proposals"] + e1
    if previous is None:
        raise BatchFailed(f"malformed: the host session ended without an answer to repair ({res.error or 'no submission'}"
                          "); a resume asks the batch again")
    out.problems_before_repair = [{"answer": e} for e in env]
    text2, meta = R.host_repair(sp, ctx.cfg, previous, env, [], staging / out.run_id, log, ctx.policy,
                                model=sess.model, sleep=ctx.sleep, rng=ctx.rng, record=rec)
    out.host_sessions.append({"repair": True, **meta})
    out.repaired = True
    data2, env2, probs2 = R.check(sp, text2, packet, fields)
    if data2 is None or env2:
        raise BatchFailed("malformed after the bounded repair: " + _short("; ".join(env2), 600))
    bad = {p["index"] for p in probs2 if p.get("kind") == "schema"}       # references: the controller rates them
    clean = {**data2, "items": [it for i, it in enumerate(data2.get("items") or []) if i not in bad]}
    sub = controller.submit(ws, clean, sess.host_model_label(), via=f"workflow {ctx.run_id} {bid} (bounded repair)")
    out.malformed_items = [p for p in probs2 if p.get("kind") == "schema"]
    out.reference_problems = [p for p in probs2 if p.get("kind") != "schema"]
    probs2 = out.malformed_items
    log.event("repaired_submission", run_id=sub["run_id"], status=sub["status"], malformed_items=probs2)
    return _load_staged(ws, sub["run_id"])[0]


def _batch_log(ctx: Ctx, bid: str, ws=None, n: int | None = None):
    """The run id, log and staging folder of one request of a batch (`<run>-<batch>`, `-aN` from the second attempt)."""
    ws = ws or ctx.ws
    n = n or ctx.cp.data["batches"].get(bid, {}).get("attempts", 1) or 1
    run_id = B.check_run_id(f"{ctx.run_id}-{bid}" + (f"-a{n}" if n > 1 else ""))
    staging = B.safe_staging(ws.staging, ws.root, ws.evidence)
    log = RunLog(run_id, [staging / run_id / "log.jsonl", Path(ctx.s["worklog"]) / f"{run_id}.jsonl"])
    return run_id, log, staging


def _record_request(ctx: Ctx, bid: str, out, failure_class: str | None = None) -> None:
    """What the request layer did for a batch, on the batch (checkpoint): the size, repairs, malformed items, failed
    calls with their class and waits, usage and route notices."""
    if out is None or bid not in ctx.cp.data["batches"]:
        return
    b = ctx.cp.batch(bid)
    rec = out.record()
    b["request"] = rec
    if out.malformed_items:
        b["malformed_items"] = out.malformed_items
    if out.attempts:
        b.setdefault("failures", []).extend(out.attempts)
    if failure_class:
        b["failure_class"] = failure_class
    ctx.notices(bid, out.notices)


def _add_usage(ctx: Ctx, out) -> None:
    if out is None:
        return
    u = out.usage
    ctx.cp.add_usage(u.get("calls", 0), u.get("input_tokens", 0), u.get("output_tokens", 0), u.get("cost_usd"))
    _mirror_spend(ctx)


def _request_args(ctx: Ctx, sp, prov, bid: str, ws=None, n: int | None = None) -> dict:
    """What one request of a batch is sent with (caps, price, its run id, log and staging folder, the fields)."""
    route = ctx.s["route"]
    caps_ = C.caps(ctx.cfg, route, ctx.remaining_caps())
    price = B.price_for(ctx.cfg, prov.model) if route != "recorded" else None
    B.check_startable(route, C.route(ctx.cfg, route), caps_, price)
    run_id, log, staging = _batch_log(ctx, bid, ws, n)
    fields = {"run_id": run_id, "created": now_iso(), "route": route, "provider": prov.name,
              "model_requested": prov.model, "model_reported": None, "task": sp.task}
    if sp.phase == "analysis":
        from .contract import CONTROLLER_VERSION
        fields["controller_version"] = CONTROLLER_VERSION
    return {"caps_": caps_, "price": price, "run_id": run_id, "log": log, "staging": staging, "fields": fields}


def _request(ctx: Ctx, sp, prov, packet: dict, bid: str, *, images: list | None = None, ws=None,
             account_usage: bool = True, prompt_text: str | None = None, pre: dict | None = None):
    """One request of a workflow batch with a provider (recorded or an API route) through the request layer
    (requests.converse). Returns the Outcome; maps its failures to the workflow's: a rate limit -> Deferred, a
    provider failure, a malformed answer or a conversation that outgrew the context -> BatchFailed (with the class on
    the batch); TooLarge and a capability refusal propagate (the caller splits or stops)."""
    s, ws = ctx.s, (ws or ctx.ws)
    route = s["route"]
    pol = ctx.policy
    if pre is None:
        a = _request_args(ctx, sp, prov, bid, ws)
        a["log"].event("start", route=route, provider=prov.name, model_requested=prov.model, task=sp.task,
                       phase=sp.phase, batch=bid, caps=a["caps_"], cassette=getattr(prov, "cassette_path", None),
                       policy=pol.to_dict())
    try:
        if pre is not None:                             # session 12: the exchange already ran in a worker
            out = Prefetch.result(pre)
        else:
            out = R.converse(sp, prov, packet, ws=ws, route=route, caps_=a["caps_"], price=a["price"], policy=pol,
                             log=a["log"], staging=a["staging"], run_id=a["run_id"], fields=a["fields"],
                             sleep=ctx.sleep, rng=ctx.rng, images=images, settings=R.settings_for(ctx.cfg, route),
                             prompt_text=prompt_text)
    except R.RateLimited as e:
        _add_usage(ctx, e.outcome)
        _record_request(ctx, bid, e.outcome, "rate_limit")
        raise Deferred(e.message, e.reset_in_s) from None
    except (R.ProviderFailed, R.Malformed, R.ContextExhausted) as e:
        cls = {R.ProviderFailed: "provider", R.Malformed: "malformed", R.ContextExhausted: "too_large"}[type(e)]
        _add_usage(ctx, e.outcome)
        _record_request(ctx, bid, e.outcome, cls)
        raise BatchFailed(f"{ {'provider': 'provider failure', 'malformed': 'malformed', 'too_large': 'context'}[cls] }: "
                          f"{e.message}") from None
    except B.BudgetExhausted as e:
        _add_usage(ctx, getattr(e, "outcome", None))
        ctx.stop_batches = "the run's budget is exhausted"
        raise BatchFailed(f"the {sp.phase} request is budget_exhausted: {e}") from None
    except R.TooLarge as e:
        _record_request(ctx, bid, e.outcome, "too_large")
        raise
    if account_usage:
        _add_usage(ctx, out)
    _record_request(ctx, bid, out)
    return out


def _host_request(ctx: Ctx, bid: str, sp, sess, packet: dict, fields: dict, ws=None, pre: dict | None = None):
    """One request of a workflow batch in a host answer session (requests.ask_host); failures mapped as _request.
    `pre` (session 12): the same request already asked by a worker (Prefetch)."""
    if pre is None:
        run_id, log, staging = _batch_log(ctx, bid, ws)
        fields = {**fields, "run_id": run_id}
        log.event("start", route="host", phase=sp.phase, batch=bid, model_requested=sess.host_model_label(),
                  policy=ctx.policy.to_dict())
    try:
        if pre is not None:
            out = Prefetch.result(pre)
        else:
            out = R.ask_host(sp, sess, packet, cfg=ctx.cfg, policy=ctx.policy, log=log, fields=fields,
                             cwd=staging / run_id, sleep=ctx.sleep, rng=ctx.rng,
                             settings=R.settings_for(ctx.cfg, "host"))
    except R.RateLimited as e:
        _record_request(ctx, bid, e.outcome, "rate_limit")
        raise Deferred(e.message, e.reset_in_s) from None
    except (R.ProviderFailed, R.Malformed) as e:
        cls = "provider" if isinstance(e, R.ProviderFailed) else "malformed"
        _record_request(ctx, bid, e.outcome, cls)
        raise BatchFailed(f"{'provider failure' if cls == 'provider' else 'malformed'}: {e.message}") from None
    except R.TooLarge as e:
        _record_request(ctx, bid, e.outcome, "too_large")
        raise
    _record_request(ctx, bid, out)
    return out


def _analysis_request(ctx: Ctx, bid: str, todo: list[str], prov) -> ProposalSet:
    """An analysis batch with a provider (recorded or an API route): the task packet (shared context once: see
    requests.compact_analysis), one request through the request layer, then the controller's validation and staging
    exactly as controller.propose does (validate_set, the freshness re-check, write_staging with the route notices)."""
    from .contract import Usage
    ws, s = ctx.ws, ctx.s
    ws.refresh()
    ws.require_ok()
    raw = controller.task_packet(ws, ctx.addendum, todo)
    images = [{"type": "image", "path": c["_path"], "sha256": c["sha256"], "media_type": c["media_type"]}
              for c in raw["crops"]]
    packet = ANS.with_answers(ctx, R.compact_analysis(dict(raw, crops=[{k: v for k, v in c.items() if not k.startswith("_")}
                                                                      for c in raw["crops"]])), "analysis", bid)   # s14 (W5)
    staging = B.safe_staging(ws.staging, ws.root, ws.evidence)
    pre = ctx.prefetch.take(bid, Prefetch.key(packet)) if ctx.prefetch else None
    if pre is None and ctx.prefetch is not None and bid in ctx.prefetch.discarded and s["route"] == "recorded":
        prov, sess = ctx.cassette.provider("analysis", todo, ctx.used_sessions())   # its reserved session, afresh
        if prov is None:
            raise BatchFailed("no recorded session covers this batch (the cassette does not record it)")
        ctx.cp.batch(bid)["session"] = sess
    lock = None if ctx.run_lock is not None else B.acquire(
        staging, ctx.addendum, {"route": s["route"], "run_id": f"{ctx.run_id}-{bid}", "pid": os.getpid(),
                                "model": prov.model}, ctx.cfg.get("lock_stale_after_min", 120))
    try:
        out = _request(ctx, R.spec("analysis", route=ctx.s["route"], cfg=ctx.cfg), prov, packet, bid, images=images,
                       account_usage=False, pre=pre)
    finally:
        if lock is not None:
            lock.release()
    ps = out.answer
    log = RunLog(out.run_id, [staging / out.run_id / "log.jsonl", Path(s["worklog"]) / f"{out.run_id}.jsonl"])
    report = controller.validate_set(ws, ps, log, expected_addendum=ctx.addendum,
                                     reference=controller._reference_path(ws, ctx.addendum), overwrites=out.overwrites)
    if not controller.recheck_fresh(ws, ps, report):
        log.event("stale", differences=report["state_differences"])
    if out.notices:
        report["route_notices"] = out.notices
    if out.malformed_items:
        report["malformed_items"] = out.malformed_items
    report["request"] = {k: v for k, v in out.record().items() if k != "notices"}
    u = out.usage
    ps.usage = Usage(calls=u["calls"], input_tokens=u["input_tokens"], output_tokens=u["output_tokens"],
                     cost_usd=u["cost_usd"], cost_basis=u["cost_basis"])
    d = controller.write_staging(ws, ps, report)
    log.event("staged", status=ps.status, staging=str(d), statuses={it.id: it.verification_status for it in ps.items},
              coverage=ps.coverage.model_dump())
    return ps


# ---------------------------------------------------------------------------------------------- step: validation

def _op_types() -> set[str]:
    from ..amend import Op
    return set(typing.get_args(Op.model_fields["type"].annotation))


def step_validation(ctx: Ctx, st: dict) -> None:
    cp, ws, s = ctx.cp, ctx.ws, ctx.s
    ws.refresh()
    items, statements, meta, converted = [], [], None, []
    types = _op_types()
    for bid in cp.batches("analysis"):
        b = cp.batch(bid)
        if b["status"] != "done":
            continue
        ps, _ = _load_staged(ws, b["staged_run"])
        meta = meta or ps
        keep = set(b.get("items") or [])
        smap = {x.id: f"{bid}/{x.id}" for x in ps.statements}
        statements += [x.model_copy(update={"id": smap[x.id]}) for x in ps.statements]
        for it in ps.items:
            if it.id not in keep:
                continue
            it2 = it.model_copy(deep=True)
            it2.statements = [smap.get(x, x) for x in it2.statements]
            t = it2.payload.get("type") if it2.statement_type == "amendment_op" else None
            if it2.statement_type == "amendment_op" and t not in types:
                converted.append({"item": it2.id, "batch": bid, "type": t})
                it2 = it2.model_copy(update={"statement_type": "escalation", "payload": {
                    "why": f"the proposer named the change type {t!r}, which the amendment engine does not have: escalated "
                           "with its evidence and affected scope, never forced into a known type",
                    "what_is_unsupported": f"change type {t!r}: {_short(json.dumps(it2.payload, ensure_ascii=False), 400)}"},
                    "previous_value": None, "proposed_value": None})
            items.append(it2)
    rid = f"{ctx.run_id}-combined"
    cps = ProposalSet(run_id=rid, created=now_iso(), route=s["route"], provider=meta.provider if meta else s["route"],
                      model_requested=(meta.model_requested if meta else s.get("model") or s.get("host_model") or "-"),
                      model_reported=meta.model_reported if meta else None, task=controller.TASK,
                      addendum=ctx.addendum, state=ws.identity(), statements=statements, items=items)
    staging = B.safe_staging(ws.staging, ws.root, ws.evidence)
    log = RunLog(rid, [staging / rid / "log.jsonl"])
    log.event("start", note="the items of every analysis batch validated together", batches=cp.batches("analysis"),
              converted_unknown_types=converted)
    report = controller.validate_set(ws, cps, log, expected_addendum=ctx.addendum)
    report["converted_unknown_types"] = converted
    controller.write_staging(ws, cps, report)
    for p, v in cp.data["provisions"].items():
        mine = [it for it in cps.items if it.provision == p]
        v["final"] = {"items": {it.id: it.verification_status for it in mine}, "accounted": p not in cps.coverage.unaccounted}
    cp.save()
    st.update(staged=str(staging / rid), set_status=cps.status, coverage=cps.coverage.model_dump(),
              statuses=dict(Counter(it.verification_status for it in cps.items)), converted=converted)
    if getattr(cps, "resolution", None) is not None:
        st["resolution"] = cps.resolution.model_dump()
    ctx._promoted = None
    ctx.say(f"  combined set: {len(items)} item(s); {cps.coverage.accounted}/{cps.coverage.provisions_total} provisions "
            f"accounted for; {dict(Counter(it.verification_status for it in cps.items))}")


# ---------------------------------------------------------------------------------------------- step: downstream


def answer_state(promoted_ids: list[str], escalations: list[str]) -> dict:
    """Session 12 (blind-06 follow-up 1): a provision with a promoted op or disposition is ANSWERED only while none of
    its sibling items is an escalation. With one, it is "partly answered": the promoted item stands, but the provision
    stays on the unresolved list, in the packet's first section and in A4, so the escalation never drops out of sight."""
    if not escalations:
        return {"answered": True}
    return {"answered": False, "partly": True,
            "why": "partly answered" + (f" by {', '.join(promoted_ids)}" if promoted_ids else "")
                   + "; escalated: " + "; ".join(escalations)}


def carried_answer(item_ids: list[str], tasks, ds, held: dict | None = None) -> dict | None:
    """Session 13 (blind-05 regression, defect 3): the state of a provision whose analysis row items were carried to
    downstream tasks (downstream.carry_analysis_rows), or None when none was. Never `answered` (no op or disposition
    answers the provision; the op file keeps it `unresolved` with this reason), but never a silent gap: while the
    downstream phase has not run the provision is accounted for through the open task; afterwards it names the rows
    proposed for it, or says "unresolved: <reason>" (the task unanswered, or answered only by items that cannot be
    promoted) and needs a person."""
    tasks = list(tasks.values()) if isinstance(tasks, dict) else list(tasks or [])
    tids = [t["id"] for t in tasks if any(a.get("item") in item_ids for a in t.get("analysis_items") or [])]
    if not tids:
        return None
    what = f"analysis {', '.join(item_ids)}, an UNVERIFIED reference"
    if ds is None:
        return {"answered": False, "carried": tids, "needs_person": False,
                "why": f"carried to downstream task(s) {', '.join(tids)} ({what}): open until the downstream phase "
                       "answers it"}
    held = held or {}
    rows, bad, row_ids = [], [], []
    for tid in tids:
        its = [it for it in ds.items if it.task == tid]
        ok = [it for it in its if it.verification_status in DS.PROMOTABLE and it.id not in held]
        row_ids += [str((it.payload.get("row") or {}).get("id")) for it in ok if it.statement_type == "row_new"]
        if ok:
            rows += [f"{(it.payload.get('row') or {}).get('id') if it.statement_type == 'row_new' else it.payload.get('row')}"
                     f" ({it.statement_type}, {it.verification_status})" for it in ok
                     if it.statement_type in ("row_new", "row_reading")]
            rows += [f"{it.id} ({it.statement_type}, {it.verification_status})" for it in ok
                     if it.statement_type not in ("row_new", "row_reading")]
        elif its:
            bad.append(f"downstream task {tid} answered only by items that cannot be promoted: " + "; ".join(
                f"{it.id} {it.verification_status}" + (f" ({held[it.id]})" if it.id in held else (
                    f" ({next((x.check + ': ' + _short(x.detail, 120) for x in it.validation if not x.ok), '')})"))
                for it in its))
        else:
            bad.append(f"downstream task {tid} was not answered")
    if bad:
        return {"answered": False, "carried": tids, "needs_person": True,
                "why": "unresolved: " + "; ".join(bad) + (f"; proposed downstream: {', '.join(rows)}" if rows else "")}
    if row_ids:
        # session 14 (N3): the provision's obligation IS the promoted row: the provision is applied through it (the
        # row PROPOSED, a person confirms it), never "UNRESOLVED (accounted for, not applied)", so the activities
        # carrying the row are not blocked by the provision the row answers
        return {"answered": True, "carried": tids, "needs_person": False, "applied_by_rows": row_ids,
                "why": f"applied as the new row(s) {', '.join(row_ids)} (proposed downstream: {', '.join(rows)}; task(s) "
                       f"{', '.join(tids)}; PROPOSED, not approved): the provision's obligation is that row; a person "
                       "confirms it"}
    return {"answered": False, "carried": tids, "needs_person": False,
            "why": f"its obligation is proposed downstream as {', '.join(rows)} (task(s) {', '.join(tids)}; PROPOSED): "
                   "no op or disposition answers the provision; a person confirms the row and the provision's "
                   "disposition"}


def carried_lines(cps, pops: dict, tasks, ds, held: dict | None = None, win: dict | None = None) -> list[str]:
    """Session 13: the review packet's own heading for the analysis items not promoted from the analysis set (rows
    carried to downstream tasks, and every other item with its reason): never "(dropped: )"."""
    dropped = (pops or {}).get("dropped") or {}
    items = [it for it in (cps.items if cps else []) if it.verification_status in DS.PROMOTABLE
             and it.statement_type not in ("amendment_op", "disposition")]
    if not items:
        return []
    L = ["## Analysis rows carried to downstream tasks (and other analysis items not promoted)", ""]
    for it in items:
        a = carried_answer([it.id], tasks, ds, held) if it.statement_type in DS.CARRIED else None
        route = DS.window_route(HO.prose(dict(it.payload or {})), win)   # session 14 (W2; blind-07 defect 13)
        L.append(f"- `{it.id}` {it.statement_type} ({it.provision}, {it.verification_status}): "
                 + _short(dropped.get(it.id) or DS.not_promoted_reason(it), 300)
                 + (f" — {_short(a['why'], 300)}" if a else "")
                 + (f" — clarification route: {route} (its suggestion of a clarification is a bid decision now)"
                    if route else ""))
    return L + [""]


def _answers(ctx: Ctx, cps: ProposalSet, promoted: dict, tasks=None, ds=None) -> dict[str, dict]:
    """Per provision: whether a promoted op or disposition answers it, and why not. Session 13: a provision whose
    analysis rows were carried to downstream tasks says so (carried_answer), with `tasks` (else the run's tasks.json)
    and, once the downstream phase ran, its set `ds`."""
    if tasks is None:
        tasks = _js(ctx.dir / "downstream" / "tasks.json") or []
    held = {}
    if ds is not None:
        staged = load_yaml(ctx.dir / "downstream" / "proposals.yaml") if (ctx.dir / "downstream" / "proposals.yaml"
                                                                          ).exists() else {}
        held = ((staged or {}).get("controller") or {}).get("held_back") or {}
    content = {c for o in promoted["sim"]["ops"] if o["valid"] for c in o.get("content") or []}
    applied = {o.provision for o in promoted["ops"].values()} | {c for o in promoted["ops"].values() for c in o.covers} \
        | content
    no_eff = {d.provision for d in promoted["dispositions"].values() if d.disposition == "no_effect"}
    # session 14 (W2; blind-07 defect 7): a promoted `unresolved` disposition ACCOUNTS FOR its provision but applies
    # nothing: the provision is unresolved (never "answered"), with the disposition's reason
    unres_disp = {d.provision: (k, d) for k, d in promoted["dispositions"].items() if d.disposition == "unresolved"}
    ok = applied | no_eff
    out = {}
    for p, v in ctx.cp.data["provisions"].items():
        mine = [it for it in cps.items if it.provision == p]
        esc = [it for it in mine if it.statement_type == "escalation"]
        if p in ok:
            state = answer_state([it.id for it in mine if it.id in promoted["ops"] or it.id in promoted["dispositions"]],
                                 [_short(it.payload.get("why"), 200) for it in esc])
            out[p] = state if state["answered"] else {**state, "needs_person": True}
            out[p].update(state=("applied" if p in applied else "no_effect") if state["answered"] else "partly applied",
                          accounted=True, approved=False)
            continue
        if p in unres_disp:
            k, d = unres_disp[p]
            out[p] = {"answered": False, "state": "unresolved", "accounted": True, "approved": False,
                      "needs_person": True, "accounted_by": k,
                      "why": f"unresolved (accounted for by the promoted `unresolved` disposition {k}; nothing applied): "
                             + _short(d.reason, 400)
                             + ("; escalated: " + "; ".join(_short(it.payload.get("why"), 200) for it in esc) if esc else "")}
            continue
        carried = carried_answer([it.id for it in mine if it.statement_type in DS.CARRIED
                                  and it.verification_status in DS.PROMOTABLE], tasks, ds, held) if not esc else None
        if carried is not None and not any(it.verification_status not in DS.PROMOTABLE for it in mine):
            out[p] = {**carried, "state": "applied" if carried.get("applied_by_rows") else "unresolved",
                      "accounted": True, "approved": False}               # session 14 (N3)
            continue
        if esc:
            why = "escalated: " + "; ".join(_short(it.payload.get("why"), 200) for it in esc)
        elif mine:
            why = "; ".join(f"{it.id} {it.verification_status}" + (
                f" ({next((x.check + ': ' + _short(x.detail, 160) for x in it.validation if not x.ok), '')})"
                if it.verification_status not in DS.PROMOTABLE else
                f" (dropped: {promoted['dropped'].get(it.id) or DS.not_promoted_reason(it)})")
                for it in mine)
            why = "not promotable: " + why
        elif v["status"] == "pending":
            b = ctx.cp.data["batches"].get(v.get("batch") or "", {})
            why = f"not analysed: batch {v.get('batch')} {b.get('status')}" + (f" ({b.get('error')})" if b.get("error") else "")
        else:
            why = "no item proposed for it" + (f" ({v.get('reason')})" if v.get("reason") else "")
        gap = cites_missing(ctx, p, mine)               # session 12: it cites an addendum this state does not hold
        if gap:
            why = f"{missing_reason(gap)} (the provision cites {', '.join(gap)}); {why}"
        out[p] = {"answered": False, "why": why, "approved": False,
                  "state": "unresolved" if any(it.verification_status in DS.PROMOTABLE for it in mine) or esc
                  else "unaccounted",
                  "accounted": any(it.verification_status in DS.PROMOTABLE for it in mine),
                  "needs_person": bool(esc) or bool(gap) or any(it.verification_status in ("conflicting",
                                                                                          "insufficient_evidence")
                                                                for it in mine)}
    return out


# session 14 (W2; blind-07 defect 7): the four states, kept distinct in every output
#   accounted for  the provision has a promotable item (an op, a disposition, a carried row, an escalation)
#   applied        a promoted op applied to the candidate (or a promoted `no_effect`: nothing to apply)
#   unresolved     named but not applied, with the reason (a promoted `unresolved` disposition, a failed or escalated item)
#   approved       a person's recorded decision only (never the workflow's; `approval` in the checkpoint)
STATE_LABEL = {"applied": "applied (PROPOSED; not approved)", "no_effect": "no effect (PROPOSED; not approved)",
               "partly applied": "PARTLY APPLIED (an escalated sibling stays unresolved)",
               "unresolved": "UNRESOLVED (accounted for, not applied)", "unaccounted": "UNRESOLVED (unaccounted)"}


def state_of(a: dict | None) -> str:
    """The state label of a provision's answer record (answers.json / promotion.json), for the review packet."""
    a = a or {}
    st = a.get("state") or ("applied" if a.get("answered") else "unresolved" if a.get("accounted") else "unaccounted")
    return STATE_LABEL.get(st, st)


def step_downstream(ctx: Ctx, st: dict) -> None:
    cp, ws = ctx.cp, ctx.ws
    cps, _ = ctx.combined()
    promoted = ctx.promoted()
    answers = _answers(ctx, cps, promoted, tasks=[])
    tasks, imp = DS.tasks(ws, cps, promoted, answers)
    answers = _answers(ctx, cps, promoted, tasks=tasks)        # session 13: the analysis rows carried to their tasks
    ddir = ctx.dir / "downstream"
    ddir.mkdir(parents=True, exist_ok=True)
    (ddir / "tasks.json").write_text(json.dumps(tasks, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    (ddir / "impact.json").write_text(json.dumps({k: v for k, v in imp.items() if k != "diff_markdown"},
                                                 ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    (ddir / "answers.json").write_text(json.dumps(answers, ensure_ascii=False, indent=1), encoding="utf-8")
    (ddir / "promoted_ops.json").write_text(json.dumps(
        {"ops": {k: o.model_dump(exclude_none=True) for k, o in promoted["ops"].items()},
         "dispositions": {k: d.model_dump() for k, d in promoted["dispositions"].items()},
         "dropped": promoted["dropped"], "changed_units": promoted["sim"]["changed_units"],
         "ops_changed": {o["id"]: o["changed"] for o in promoted["sim"]["ops"]}}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    import hashlib
    sha = hashlib.sha256(json.dumps(tasks, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()
    if cp.batches("downstream") and cp.data["downstream"].get("tasks_sha") != sha:
        # the analysis changed since these batches were planned (a resumed run asked failed batches again): their
        # tasks are not this run's any more; they are kept in the record, never merged
        old = {k: cp.data["batches"].pop(k) for k in cp.batches("downstream")}
        cp.data["downstream"].setdefault("superseded", []).append({"ts": now_iso(), "batches": old,
                                                                     "items": cp.data["downstream"]["items"]})
        cp.data["downstream"]["items"] = {}
        cp.event("downstream_replanned", why="the downstream tasks changed since the batches were planned")
    if not cp.batches("downstream"):
        cp.data["downstream"]["tasks_sha"] = sha
        groups, notes = _plan_downstream(ctx, tasks, promoted)
        for k, g in enumerate(groups, 1):
            bid = f"downstream-{k:03d}"
            cp.data["batches"][bid] = {"phase": "downstream", "tasks": [t["id"] for t in g],
                                       "status": "pending", "attempts": 0, "seconds": 0.0}
        cp.data["downstream"]["tasks"] = {t["id"]: {"kind": t["kind"], "batch": next(
            b for b in cp.batches("downstream") if t["id"] in cp.batch(b)["tasks"])} for t in tasks}
        st["plan_notes"] = notes
        cp.save()
    by_id = {t["id"]: t for t in tasks}
    seen: set = set()
    while (bid := _next_batch(ctx, "downstream", seen)) is not None:
        b = cp.batch(bid)
        if b["status"] in ("done", "skipped", "split", "escalated"):
            continue
        if ctx.stop_pending is not None and not (ctx.prefetch and bid in ctx.prefetch.recs):
            st["status"] = "stopped"
            raise ctx.stop_pending
        if b["status"] == "waiting_for_host":
            st["status"] = "waiting_for_host"
            raise WaitingForHost(_wait_message(ctx, bid))
        if ctx.stop_batches:
            b.update(status="failed", error=f"not run: {ctx.stop_batches}")
            continue
        _fill(ctx, "downstream", bid, by_id=by_id, promoted=promoted, total=len(tasks))
        _downstream_batch(ctx, st, bid, [by_id[t] for t in b["tasks"] if t in by_id], promoted, len(tasks))
        _stop_if_deferred(ctx, st, bid)
        if ctx.gate is not None:
            cp.data["rate_gate"] = ctx.gate.record()
    if ctx.stop_pending is not None:
        st["status"] = "stopped"
        raise ctx.stop_pending
    st.update(tasks=len(tasks), by_kind=dict(Counter(t["kind"] for t in tasks)),
              batches={k: cp.batch(k)["status"] for k in cp.batches("downstream")})
    deferred = [k for k in cp.batches("downstream") if cp.batch(k)["status"] == "deferred"]
    if deferred:
        st["deferred"] = deferred
    ctx.say(f"  downstream: {len(tasks)} task(s) {dict(Counter(t['kind'] for t in tasks))}")


def _downstream_packet(ctx: Ctx, batch: list[dict], promoted: dict, total: int, state: dict | None = None) -> dict:
    """downstream.packet with every unit of `units_after` in FULL (session 11: the packet never carries a shortened unit
    text; a packet that does not fit is split by task instead). The restored units are listed in the packet."""
    ws = ctx.ws
    pk = DS.packet(ws, ctx.addendum, batch, promoted, total, state or ws.identity().model_dump())
    pk = ANS.with_answers(ctx, pk, "downstream")                  # session 14 (W5): the owner's answers it concerns
    try:
        st2 = DS._stage(promoted["r2"], ctx.addendum).state
    except (KeyError, StopIteration):
        return R.compact_shared(pk)
    restored = []
    for uid, v in (pk.get("units_after") or {}).items():
        u = st2.get(uid)
        full = " ".join(str(getattr(u, "text", "") or "").split()) if u is not None else None
        if full is not None and v.get("text") != full:
            v["text"] = full
            restored.append(uid)
    if restored:
        pk["units_after_note"] = f"full text restored for {restored} (never shortened in a request)"
    return R.compact_shared(pk)                        # session 12: the shared part smaller, its meaning kept


def _plan_downstream(ctx: Ctx, tasks: list[dict], promoted: dict) -> tuple[list[list[dict]], list[str]]:
    """Downstream batches: at most --downstream-batch-size tasks each, in order, and each request within the route's
    context window and output cap with the complete accounting (the real packet of the group is sized); a task that
    does not fit alone is its own batch (escalated with its size at its request)."""
    from . import batching
    from .providers.recorded import PACKET_MARK
    n = int(ctx.s["downstream_batch_size"])
    notes: list[str] = []
    try:
        caps = _route_caps(ctx)
    except Exception as e:                                       # noqa: BLE001 (each request is still checked)
        caps = None
        notes.append(f"context fit not checked at planning: {type(e).__name__}: {_short(str(e), 300)}")
    sp = R.spec("downstream", route=ctx.s["route"], cfg=ctx.cfg)    # session 13: the route's policy composition
    tools_spec = [controller.TOOLS[t].spec() for t in sp.tools]
    state, maxout, st = ctx.ws.identity().model_dump(), _max_out(ctx), R.settings_for(ctx.cfg, ctx.s["route"])
    cache: dict = {}

    def fits(group: list[dict]) -> bool:
        if len(group) > n:
            return False
        if caps is None:
            return True
        key = tuple(t["id"] for t in group)
        if key not in cache:
            pk = _downstream_packet(ctx, group, promoted, len(tasks), state)
            text = PACKET_MARK + json.dumps(pk, ensure_ascii=False, default=str)
            cache[key] = R.size(sp, caps, text, tools_spec=tools_spec, units=len(group), max_output_tokens=maxout,
                                settings=st).fits
        return cache[key]
    groups = batching.plan_units(tasks, fits) if tasks else []
    for g in groups:
        if len(g) == 1 and caps is not None and not fits(g):
            notes.append(f"{g[0]['id']}: does not fit even alone; escalated with its size at its request")
    if caps is not None and len(groups) > -(-len(tasks) // n):
        notes.append(f"{len(groups)} batch(es) for {len(tasks)} task(s) to fit the context window and the output cap "
                     f"({caps.source})")
    return groups, notes


def _downstream_batch(ctx: Ctx, st: dict, bid: str, batch: list[dict], promoted: dict, total: int) -> None:
    cp, s = ctx.cp, ctx.s
    b = cp.batch(bid)
    b.update(status="running", pid=os.getpid(), attempts=b.get("attempts", 0) + 1, started=now_iso())
    for k in ("error", "failure_class", "session"):          # a retry may take its recorded session again
        b.pop(k, None)
    cp.save()
    t0 = time.perf_counter()
    try:
        res_path = ctx.dir / "batches" / f"{bid}.result.json"
        packet = _downstream_packet(ctx, batch, promoted, total)
        if s["route"] == "host":
            packet = _host_downstream_packet(ctx, bid, packet)
            b["packet"] = str(ctx.dir / "batches" / f"{bid}.packet.json")
            hs = _host_auto(ctx)
            if hs is None:
                b.update(status="waiting_for_host", waiting_since=now_iso(), waiting_epoch=time.time())
                cp.save()
                st["status"] = "waiting_for_host"
                raise WaitingForHost(_wait_message(ctx, bid))
            ds = _downstream_host_session(ctx, hs, bid, packet)
        else:
            pre = ctx.prefetch.take(bid, Prefetch.key(packet)) if ctx.prefetch else None
            if s["route"] == "recorded":
                prov, sess = ((pre["prov"], pre["session"]) if pre else
                              ctx.cassette.provider("downstream", [t["id"] for t in batch], ctx.used_sessions()))
                if prov is None:
                    raise BatchFailed("no recorded session covers this batch (the cassette does not record it)")
                b["session"] = sess
            else:
                prov = _make_provider(ctx)
            ds = _converse(ctx, prov, packet, bid, pre=pre)
        _take_downstream(ctx, bid, ds, res_path)
    except Deferred as e:
        _defer(ctx, bid, e)
    except R.TooLarge as e:
        _split(ctx, bid, "tasks", [t["id"] for t in batch], e)
    except BatchFailed as e:
        b.update(status="failed", error=str(e))
    except B.Refused as e:
        b.update(status="failed", error=f"refused: {e}")
        ctx.stop_batches = f"the route refused {bid}: {_short(str(e), 300)}"
    finally:
        b["seconds"] = round(b.get("seconds", 0.0) + time.perf_counter() - t0, 3)
        if b["status"] == "running":
            b["status"] = "interrupted"
        cp.save()
    ctx.say(f"  {bid}: {b['status']}" + (f" ({b.get('error')})" if b.get("error") else
                                         f" ({len(b.get('items') or [])} item(s))"))


def _take_downstream(ctx: Ctx, bid: str, ds: DownstreamSet, res_path: Path) -> None:
    cp = ctx.cp
    b = cp.batch(bid)
    res_path.parent.mkdir(parents=True, exist_ok=True)
    res_path.write_text(json.dumps(ds.model_dump(mode="json", by_alias=True), ensure_ascii=False, indent=1),
                        encoding="utf-8")
    b.update(result=str(res_path), items=[it.id for it in ds.items], model_requested=ds.model_requested,
             model_reported=ds.model_reported, status="done")
    for it in ds.items:
        cp.set_item(f"{bid}/{it.id}", "proposed", type=it.statement_type, task=it.task, batch=bid,
                    provision=it.provision)


def _host_downstream_packet(ctx: Ctx, bid: str, packet: dict) -> dict:
    packet = dict(packet)
    packet["system"] = policy.compose("downstream", "mcp", cfg=getattr(ctx, "cfg", None))   # session 13: a person's host
    packet["workflow"] = {"run_id": ctx.run_id, "batch": bid, "phase": "downstream",
                          "submit_with": f"tenderpack ai submit-batch {ctx.run_id} FILE --by NAME --host-model MODEL"}
    path = ctx.dir / "batches" / f"{bid}.packet.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(packet, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return packet


def _converse(ctx: Ctx, prov, packet: dict, bid: str, system: str | None = None, parse=None, task: str = DOWNSTREAM_TASK,
              tool_names: list[str] | None = None, ws=None, pre: dict | None = None):
    """One request of a downstream (or reading) batch with a provider (recorded or an API route), through the request
    layer (session 11; requests.converse): the phase's schema on every request, the capability check before any call
    (the reading phase requires image input), the complete size (a request that does not fit raises
    requests.TooLarge: the caller splits by task or escalates), the failure classes (a rate limit -> Deferred) and one
    bounded repair. `parse` and `system` override the phase's own; `tool_names` the tools offered; `ws` the workspace
    the tools read (default: the candidate's). Returns the parsed answer (DownstreamSet / RegionReadingProposal)."""
    sp = R.spec(R.phase_of_task(task), system=system, parse=parse, tools=tool_names, route=ctx.s["route"], cfg=ctx.cfg)
    return _request(ctx, sp, prov, packet, bid, ws=ws, pre=pre).answer


_run_tool = R.run_tool                                          # kept for callers of the session-10 name


def _downstream_host_session(ctx: Ctx, hs, bid: str, packet: dict) -> DownstreamSet:
    """A downstream batch in a headless host session (hostsession.AnswerSession with the downstream rules): the host
    reads with the MCP tools and replies with the DownstreamSet as its final message (it submits nothing). Through the
    request layer (requests.ask_host): the declared capabilities and the size checked, the failure classes, and ONE
    bounded repair of a malformed answer (a plain session given the answer and the errors: an item's `statements` are
    ids, never free text); what still fails is set aside item by item."""
    pre = ctx.prefetch.take(bid, Prefetch.key(packet)) if ctx.prefetch else None
    sess = pre["sess"] if pre else hs.AnswerSession(ctx.ws, ctx.cfg, phase="downstream",
                                                    model=ctx.s.get("host_session_model"),
                                                    run_lock=ctx.run_lock is not None)
    fields = {"run_id": f"{ctx.run_id}-{bid}", "created": now_iso(), "route": "host", "provider": "host-session",
              "model_requested": sess.host_model_label(), "model_reported": None, "task": DOWNSTREAM_TASK}
    try:
        out = _host_request(ctx, bid, R.spec("downstream", system=sess.system_prompt()), sess, packet, fields,
                            pre=pre)
    finally:
        last = sess.last
        if last is not None:
            ctx.cp.batch(bid)["host_session"] = {"run_id": last.run_id, "elapsed_s": last.elapsed_s,
                                                 "error": last.error, "model_reported": last.model_reported,
                                                 "failure_class": last.failure_class,
                                                 "note": "a downstream session submits nothing: its final message is "
                                                         "the set"}
            ctx.cp.intervention(kind="host session (automatic)", batch=bid, by="tenderpack.ai.hostsession",
                                host_model=sess.host_model_label(), note="a headless host session; not a person")
    return out.answer


# ---------------------------------------------------------------------------------------------- downstream validation

def _combined_downstream(ctx: Ctx) -> DownstreamSet:
    cp, ws = ctx.cp, ctx.ws
    items, statements, meta = [], [], None
    seen: set[str] = set()
    for bid in cp.batches("downstream"):
        b = cp.batch(bid)
        if b["status"] != "done":
            continue
        d = DownstreamSet.model_validate(json.loads(Path(b["result"]).read_text(encoding="utf-8")))
        meta = meta or d
        smap = {x.id: f"{bid}/{x.id}" for x in d.statements}
        statements += [x.model_copy(update={"id": smap[x.id]}) for x in d.statements]
        for it in d.items:
            it2 = it.model_copy(deep=True)
            it2.statements = [smap.get(x, x) for x in it2.statements]
            if it2.id in seen:
                it2.id = f"{bid}/{it2.id}"
            seen.add(it2.id)
            it2.model_rationale = it2.model_rationale
            items.append((bid, it.id, it2))
    ds = DownstreamSet(run_id=f"{ctx.run_id}-downstream", created=now_iso(), route=ctx.s["route"],
                       provider=meta.provider if meta else ctx.s["route"],
                       model_requested=meta.model_requested if meta else "-", model_reported=meta.model_reported if meta else None,
                       addendum=ctx.addendum, state=ws.identity(), statements=statements, items=[x[2] for x in items])
    ctx._ds_keys = {x[2].id: f"{x[0]}/{x[1]}" for x in items}
    return ds


def step_downstream_validation(ctx: Ctx, st: dict) -> None:
    cp = ctx.cp
    ds = _combined_downstream(ctx)
    promoted = ctx.promoted()
    tasks = json.loads((ctx.dir / "downstream" / "tasks.json").read_text(encoding="utf-8"))
    report = DS.validate(ctx.ws, ds, promoted, DS.task_kinds(tasks))   # kinds: where no_change may answer (N2: origins)
    out = ctx.dir / "downstream" / "proposals.yaml"
    out.write_text("# Downstream proposals of the AI workflow, validated by tenderpack.ai.downstream in the candidate. "
                   "STAGING ONLY: nothing here is accepted.\n"
                   + yaml.safe_dump({"downstream_set": ds.model_dump(mode="json", by_alias=True),
                                     "controller": json.loads(json.dumps(report, default=str))},
                                    allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
    for it in ds.items:
        key = getattr(ctx, "_ds_keys", {}).get(it.id, it.id)
        cp.set_item(key, "validated", verification_status=it.verification_status, id_in_set=it.id,
                    held_back=report["held_back"].get(it.id))
    cp.save()
    st.update(items=len(ds.items), statuses=dict(Counter(it.verification_status for it in ds.items)),
              held_back=report["held_back"], schedule_problems=report["schedule_problems"][:20],
              interactions=report["interactions"][:20], staged=str(out))
    ctx.say(f"  downstream items: {dict(Counter(it.verification_status for it in ds.items))}"
            + (f"; held back {len(report['held_back'])}" if report["held_back"] else ""))


def _load_downstream(ctx: Ctx) -> tuple[DownstreamSet | None, dict]:
    p = ctx.dir / "downstream" / "proposals.yaml"
    if not p.exists():
        return None, {}
    d = load_yaml(p) or {}
    return DownstreamSet.model_validate(d["downstream_set"]), d.get("controller") or {}


# ---------------------------------------------------------------------------------------------- the critic (session 11)

def _critic_route(ctx: Ctx, keys: list[str]):
    """(route, (recorded provider, session index) or None, why it cannot run, model) for one batch's critic.

    Session 12: in offline mode the critic is LOCAL: the ollama route with `routes.ollama.models.critic` (it may be the
    same model as propose); without one the review is skipped with the reason. config `critic.route` (host by default)
    is never consulted offline, and nothing falls back to another route."""
    from . import critic as CR
    cs = CR.settings(ctx.cfg)
    if cs.get("workflow") is False:
        return None, None, "critic.workflow is false in config/ai.yaml", None
    if ctx.s["route"] == "recorded":
        prov, sess = ctx.cassette.provider("critic", keys, ctx.used_sessions())
        if prov is None:
            return (None, None, "the recorded workflow has no critic session for these items (not run; nothing implied)",
                    None)
        return "recorded", (prov, sess), None, None
    if OFF.active(ctx.cfg):
        rcfg = C.route(ctx.cfg, "ollama")
        model = C.critic_model(rcfg, "ollama", cs.get("model") if cs.get("route") == "ollama" else None)
        if not model:
            return ("ollama", None, "independent review did not run: offline mode: no local critic model is configured "
                    "(routes.ollama.models.critic; it may name the same model as propose)", None)
        return "ollama", None, None, model
    route = cs.get("route") or "host"
    if route == "host":
        binary = (cs.get("host") or {}).get("claude_bin") or (ctx.cfg.get("host_session") or {}).get("claude_bin") \
            or "claude"
        if not (shutil.which(binary) or Path(binary).exists()):
            return None, None, f"the host CLI ({binary}) is not installed here: the host critic cannot run", None
    return route, None, None, cs.get("model")


def _critic_run(ctx: Ctx, label: str, entries: list, ws) -> dict:
    """ONE critic request for the selected items of a batch (critic.review_batch through the request layer)."""
    from . import critic as CR
    keys = [k for k, _, _, _ in entries]
    route, rec_prov, why, model = _critic_route(ctx, keys)
    base = {"selected": len(entries), "selected_items": {k: w for k, _, w, _ in entries}}
    if route is None or why:
        ctx.log.event("critic_skipped", batch=label, route=route, reason=why, items=keys)
        return {**base, "status": "skipped", "reason": why, **({"route": route} if route else {})}
    offline = OFF.active(ctx.cfg)
    local_prov = None
    if offline:                                       # session 12: the local critic model checked before the packet
        from .providers import make
        from .providers.base import ProviderError
        try:
            local_prov = make("ollama", model, ctx.cfg, None)
            local_prov.capabilities()
        except (ProviderError, C.ConfigError) as e:
            why = f"independent review did not run: the local critic model {model}: {getattr(e, 'message', None) or e}"
            ctx.log.event("critic_skipped", batch=label, route="ollama", reason=why, items=keys)
            return {**base, "status": "skipped", "route": "ollama", "model_requested": model, "reason": why}
    elif ctx.s["route"] == "ollama" and route in OFF.HOSTED_ROUTES:
        ctx.log.event("critic_route_notice", batch=label, route=route,
                      note=f"the critic of this ollama run uses the {route} route (config critic.route; "
                           f"{OFF.KINDS[route]}), not local inference; --offline keeps every phase local")
    run_id, log, staging = _batch_log(ctx, f"{label}-critic", ws)
    packet = CR.batch_packet(ws, ctx.addendum, entries)
    cs = CR.settings(ctx.cfg)
    log.event("critic_start", route=route, items=keys, note=CR.NOT_APPROVAL)
    (staging / run_id).mkdir(parents=True, exist_ok=True)
    try:
        res = CR.review_batch(packet, route=route, cfg=ctx.cfg, log=log, cwd=(staging / run_id), policy=ctx.policy,
                              model=model, provider=rec_prov[0] if rec_prov else local_prov, sleep=ctx.sleep,
                              staging=staging, run_id=run_id)
    except R.RateLimited as e:
        ctx.deferred_in_drive = True
        return {**base, "status": "deferred", "critic_run": run_id, "route": route, "error": _short(e.message, 400),
                "message": _short(e.message, 400), "reset_in_s": e.reset_in_s, "attempts": e.attempts}
    except (R.CapabilityRefused, R.TooLarge, C.ConfigError) as e:
        if not offline:
            return {**base, "status": "failed", "critic_run": run_id, "route": route,
                    "error": f"{type(e).__name__}: {_short(getattr(e, 'message', None) or str(e), 400)}"}
        why = f"independent review did not run: the local critic model {model}: {_short(str(e), 400)}"
        ctx.log.event("critic_skipped", batch=label, route=route, reason=why, items=keys)
        return {**base, "status": "skipped", "route": route, "model_requested": model, "reason": why}
    except (R.ProviderFailed, R.Malformed, R.ContextExhausted, B.Refused, CR.CriticError) as e:
        return {**base, "status": "failed", "critic_run": run_id, "route": route,
                "error": f"{type(e).__name__}: {_short(getattr(e, 'message', None) or str(e), 400)}"}
    items = {}
    for k, it, why, _ in entries:
        a = res["answers"].get(k)
        if a is not None:
            items[k] = {"agrees": a.agrees, "concerns": a.concerns, "evidence_checked": a.evidence_checked,
                        "selected_because": why}
    out = {**base, "status": "done", "critic_run": run_id, "route": route, "reviewed": len(items),
           "agrees": sum(1 for v in items.values() if v["agrees"]),
           "disagrees": sum(1 for v in items.values() if not v["agrees"]), "missing": res["missing"],
           "model_requested": res["model_requested"], "model_reported": res["model_reported"], "items": items,
           "request": res["outcome"], "note": CR.NOT_APPROVAL}
    if rec_prov:
        out["session"] = rec_prov[1]
    log.event("critic_end", reviewed=len(items), missing=res["missing"], statuses_unchanged=True)
    return out


def _critic_analysis(ctx: Ctx, bid: str) -> None:
    """The selective critic over one validated analysis batch: the batch's items of the selected classes (critic.select:
    removals, conflicts and contradicting evidence, consequential interpretations, uncertain targets) in ONE request;
    the answers are written to each item's review.critic in the batch's staged set and its review request. No status
    changes (checked); agreement is not approval."""
    from . import critic as CR
    cp, ws = ctx.cp, ctx.ws
    b = cp.batch(bid)
    if (b.get("critic") or {}).get("status") in ("done", "not_needed", "skipped"):
        return
    cs = CR.settings(ctx.cfg)
    ps, _ = _load_staged(ws, b["staged_run"])
    keep = set(b.get("items") or [])
    chosen = [(it, why) for it, why in CR.select(ps, ws, cs.get("select")) if it.id in keep]
    if not chosen:
        b["critic"] = {"status": "not_needed", "selected": 0, "note": "no item of the selected classes"}
        cp.save()
        return
    limit = int(cs.get("max_items") or 25)
    over = [it.id for it, _ in chosen[limit:]]
    chosen = chosen[:limit]
    statements = {s.id: s for s in ps.statements}
    b["critic"] = {"status": "pending", "selected": len(chosen)}
    cp.save()
    rec = _critic_run(ctx, bid, [(it.id, it, why, statements) for it, why in chosen], ws)
    rec["not_reviewed_over_limit"] = over
    b["critic"] = rec
    if rec["status"] == "done":
        _write_critic_analysis(ctx, b["staged_run"], rec)
    cp.save()
    ctx.say(f"  {bid} critic: {rec['status']}" + (f" ({rec.get('reviewed')} reviewed, {rec.get('disagrees')} disagree)"
                                                  if rec["status"] == "done" else
                                                  f" ({_short(rec.get('error') or rec.get('reason'), 200)})"))


def _write_critic_analysis(ctx: Ctx, run_id: str, rec: dict) -> None:
    """review.critic on the items of a staged analysis set (proposals.yaml and review_request.md); statuses unchanged."""
    from . import critic as CR
    from .contract import CriticReview, ItemReview
    ws = ctx.ws
    d = B.safe_staging(ws.staging, ws.root, ws.evidence) / run_id
    f = d / "proposals.yaml"
    raw = load_yaml(f) or {}
    ps = ProposalSet.model_validate(raw["proposal_set"])
    before = {it.id: it.verification_status for it in ps.items}
    results = []
    for it in ps.items:
        a = (rec.get("items") or {}).get(it.id)
        if a is None:
            continue
        it.review = ItemReview(critic=CriticReview(
            agrees=a["agrees"], concerns=a["concerns"], evidence_checked=a["evidence_checked"],
            selected_because=a["selected_because"], route=rec["route"],
            model_requested=rec.get("model_requested") or "the CLI's default", model_reported=rec.get("model_reported"),
            critic_run=rec["critic_run"], created=now_iso()))
        results.append({"item": it.id, "agrees": a["agrees"], "concerns": len(a["concerns"])})
    if {it.id: it.verification_status for it in ps.items} != before:
        raise CR.CriticError("a status changed during the critic step; nothing written")
    raw["proposal_set"] = ps.model_dump(mode="json")
    ctl = dict(raw.get("controller") or {})
    ctl.setdefault("critic_runs", []).append({"critic_run": rec["critic_run"], "route": rec["route"], "items": results,
                                              "errors": [{"item": k, "error": "no review in the critic's answer"}
                                                         for k in rec.get("missing") or []],
                                              "not_reviewed_over_limit": rec.get("not_reviewed_over_limit") or [],
                                              "note": CR.NOT_APPROVAL})
    raw["controller"] = ctl
    f.write_text(controller.HEADER + yaml.safe_dump(raw, allow_unicode=True, sort_keys=False, width=110),
                 encoding="utf-8")
    rr = d / "review_request.md"
    md = rr.read_text(encoding="utf-8") if rr.exists() else f"# Review request: run {run_id}\n"
    rr.write_text(CR._with_section(md, CR.critic_markdown(
        ps, rec["critic_run"], rec["route"], results, [{"item": k, "error": "no review in the critic's answer"}
                                                        for k in rec.get("missing") or []],
        rec.get("not_reviewed_over_limit") or [], [])), encoding="utf-8")


def _merge_reviews_into_combined(ctx: Ctx) -> None:
    """When an analysis batch's critic ran after the combined set was made (on_deferred: continue, or a resume), its
    reviews are copied into the combined set (statuses unchanged)."""
    ws = ctx.ws
    d = B.safe_staging(ws.staging, ws.root, ws.evidence) / f"{ctx.run_id}-combined"
    f = d / "proposals.yaml"
    if not f.exists():
        return
    raw = load_yaml(f) or {}
    cps = ProposalSet.model_validate(raw["proposal_set"])
    reviews = {}
    for bid in ctx.cp.batches("analysis"):
        b = ctx.cp.batch(bid)
        if b["status"] == "done" and (b.get("critic") or {}).get("status") == "done":
            for it in _load_staged(ws, b["staged_run"])[0].items:
                if it.review is not None:
                    reviews[it.id] = it.review
    before = {it.id: it.verification_status for it in cps.items}
    changed = False
    for it in cps.items:
        if it.id in reviews and it.review != reviews[it.id]:
            it.review, changed = reviews[it.id], True
    if changed and {it.id: it.verification_status for it in cps.items} == before:
        raw["proposal_set"] = cps.model_dump(mode="json")
        f.write_text(controller.HEADER + yaml.safe_dump(raw, allow_unicode=True, sort_keys=False, width=110),
                     encoding="utf-8")


def step_critic(ctx: Ctx, st: dict) -> None:
    """The selective critic over the validated downstream items, ONE request per downstream batch for its selected
    items (critic.select_downstream), and any analysis batch whose critic is still pending or was deferred. Findings:
    downstream/critic.yaml (per item, `review.critic`) and the checkpoint; the review packet shows them. No status
    changes; agreement is not approval."""
    from . import critic as CR
    cp = ctx.cp
    if cp.step("promotion").get("status") == "done" and not any(b.get("critic") for b in cp.data["batches"].values()):
        st["note"] = ("this run predates the critic step (its later steps are done): not run here; a resume from the "
                      "downstream step includes it")
        return
    redo = [k for k in cp.batches("analysis") if cp.batch(k)["status"] == "done" and cp.batch(k).get("staged_run")
            and (cp.batch(k).get("critic") or {}).get("status") in ("pending", "deferred")]
    for bid in redo:
        _critic_analysis(ctx, bid)
        _stop_if_deferred(ctx, st, bid)
    if redo:
        _merge_reviews_into_combined(ctx)
    ds, _ = _load_downstream(ctx)
    cs = CR.settings(ctx.cfg)
    tasks = {t["id"]: t for t in (json.loads((ctx.dir / "downstream" / "tasks.json").read_text(encoding="utf-8"))
                                  if (ctx.dir / "downstream" / "tasks.json").exists() else [])}
    by_batch: dict[str, list[str]] = {}
    for v in cp.data["downstream"].get("items", {}).values():
        if v.get("id_in_set") and v.get("batch"):
            by_batch.setdefault(v["batch"], []).append(v["id_in_set"])
    items_by_id = {it.id: it for it in (ds.items if ds else [])}
    statements = {s.id: s for s in (ds.statements if ds else [])}
    for bid in cp.batches("downstream"):
        b = cp.batch(bid)
        if b["status"] != "done" or (b.get("critic") or {}).get("status") in ("done", "not_needed", "skipped"):
            continue
        mine = [items_by_id[i] for i in by_batch.get(bid, []) if i in items_by_id]
        chosen = CR.select_downstream(ds.model_copy(update={"items": mine}), tasks, cs.get("select")) if ds else []
        if not chosen:
            b["critic"] = {"status": "not_needed", "selected": 0, "note": "no item of the selected classes"}
            continue
        limit = int(cs.get("max_items") or 25)
        over = [it.id for it, _ in chosen[limit:]]
        chosen = chosen[:limit]
        b["critic"] = {"status": "pending", "selected": len(chosen)}
        cp.save()
        rec = _critic_run(ctx, bid, [(it.id, it, why, statements) for it, why in chosen], ctx.ws)
        rec["not_reviewed_over_limit"] = over
        b["critic"] = rec
        cp.save()
        ctx.say(f"  {bid} critic: {rec['status']}" + (f" ({rec.get('reviewed')} reviewed, {rec.get('disagrees')} "
                                                      "disagree)" if rec["status"] == "done" else
                                                      f" ({_short(rec.get('error') or rec.get('reason'), 200)})"))
        _stop_if_deferred(ctx, st, bid)
    # the findings, per downstream item (DownstreamItem has no review field: the sidecar holds review.critic)
    side = {"note": CR.NOT_APPROVAL + "; the downstream items' review.critic, by item id in downstream/proposals.yaml",
            "batches": {}, "items": {}}
    for bid in cp.batches("downstream"):
        rec = cp.batch(bid).get("critic") or {}
        side["batches"][bid] = {k: v for k, v in rec.items() if k not in ("items", "request")}
        for k, v in (rec.get("items") or {}).items():
            side["items"][k] = {"batch": bid, "review": {"critic": {**v, "route": rec.get("route"),
                                                                   "critic_run": rec.get("critic_run"),
                                                                   "model_reported": rec.get("model_reported")}}}
    for key, v in cp.data["downstream"].get("items", {}).items():
        if v.get("id_in_set") in side["items"]:
            v["critic"] = side["items"][v["id_in_set"]]["review"]["critic"]
    (ctx.dir / "downstream").mkdir(parents=True, exist_ok=True)
    (ctx.dir / "downstream" / "critic.yaml").write_text(
        "# The selective critic's findings on the downstream items (a second model). Agreement is not approval; no "
        "status was changed.\n" + yaml.safe_dump(side, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
    allb = [cp.batch(k).get("critic") or {} for k in cp.batches("analysis") + cp.batches("downstream")]
    st.update(batches={k: (cp.batch(k).get("critic") or {}).get("status") for k in cp.batches("analysis")
                       + cp.batches("downstream")},
              reviewed=sum(c.get("reviewed") or 0 for c in allb),
              disagrees=sum(c.get("disagrees") or 0 for c in allb),
              sessions=sum(1 for c in allb if c.get("status") in ("done", "deferred", "failed")),
              note=CR.NOT_APPROVAL)


# ---------------------------------------------------------------------------------------------- step: promotion

def _revalidate(ctx: Ctx, st: dict) -> tuple[ProposalSet, dict, DownstreamSet | None]:
    """Session 11 (D1): the COMBINED proposal set (the ops and dispositions, and the downstream items) validated again
    immediately before promotion, against the candidate's inputs as they are now (reloaded, their bytes compared with
    the state identity: tools.Workspace.check_fresh(deep=True)). A set made against another state is STALE and nothing
    is promoted (StopRun); otherwise the statuses promoted are the ones computed here (a change from the recorded ones
    is listed and the staged files are rewritten)."""
    ctx._ws, ctx._promoted = None, None
    ws = ctx.ws
    ws.refresh()
    ws.check_fresh(deep=True)
    cps, _ = ctx.combined()
    before = {it.id: it.verification_status for it in cps.items}
    rep = controller.validate_set(ws, cps, None, expected_addendum=ctx.addendum)
    stale = list(rep.get("state_differences") or []) if cps.status == "stale" else []
    promoted = DS.promoted_ops(ws, cps)
    ds, _ = _load_downstream(ctx)
    dbefore, drep = {}, {}
    if ds is not None and not stale:
        dbefore = {it.id: it.verification_status for it in ds.items}
        tasks = _js(ctx.dir / "downstream" / "tasks.json") or []
        drep = DS.validate(ws, ds, promoted, DS.task_kinds(tasks))      # session 14 (N2): merged origins included
        if ds.status == "stale":
            stale = list(drep.get("state_differences") or [])
    if stale:
        st.update(status="stopped", refused=True, stale=stale[:10])
        raise StopRun("stopped", "promotion refused: the candidate's inputs changed after the proposals were validated "
                                 "(the set is STALE: " + "; ".join(_short(x, 200) for x in stale[:3]) + "); nothing was "
                                 "promoted. Restore the candidate or start a new run")
    changed = [f"{k}: {v} -> {it.verification_status}" for it in cps.items for k, v in [(it.id, before.get(it.id))]
               if v != it.verification_status]
    changed += [f"{it.id}: {dbefore.get(it.id)} -> {it.verification_status}" for it in (ds.items if ds else [])
                if dbefore.get(it.id) != it.verification_status]
    st["revalidated"] = {"identity": ws.identity().fingerprint(), "set_status": cps.status,
                         "downstream_status": ds.status if ds else None, "status_changes": changed[:40]}
    if changed:                                    # what is promoted is what was validated now, and the files say so
        controller.write_staging(ws, cps, rep)
        out = ctx.dir / "downstream" / "proposals.yaml"
        if ds is not None:
            out.write_text("# Downstream proposals of the AI workflow, validated by tenderpack.ai.downstream in the "
                           "candidate (validated again before promotion). STAGING ONLY: nothing here is accepted.\n"
                           + yaml.safe_dump({"downstream_set": ds.model_dump(mode="json", by_alias=True),
                                             "controller": json.loads(json.dumps(drep, default=str))},
                                            allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
        ctx.say(f"  validated again before promotion: {len(changed)} status change(s): {'; '.join(changed[:5])}")
    ctx._promoted = promoted
    return cps, promoted, ds


def step_promotion(ctx: Ctx, st: dict) -> None:
    snap = ctx.P["pre_promotion"]
    if snap.exists():
        DS._snapshot(snap.parent, snap)                          # back to the candidate as it was before promotion
    cps, promoted, ds = _revalidate(ctx, st)                     # session 11: the combined set, validated again now
    tasks = _js(ctx.dir / "downstream" / "tasks.json") or []    # session 13: the analysis rows' downstream tasks
    answers = _answers(ctx, cps, promoted, tasks=tasks, ds=ds)
    origin = (f"AI workflow run {ctx.run_id} (route {ctx.s['route']}, model {cps.model_requested}"
              + (f", reported {cps.model_reported}" if cps.model_reported else "") + "); PROPOSED; not reviewed")
    summ = DS.promote(ctx.ws, ctx.cp.data["candidate"], ctx.run_id, cps, promoted, ds, origin,
                      {p: a["why"] for p, a in answers.items() if not a["answered"]},
                      applied_by_rows={p: a["applied_by_rows"] for p, a in answers.items()
                                       if a.get("applied_by_rows")})          # session 14 (N3)
    summ["answers"] = answers                                    # session 13: after the downstream phase (packet)
    (ctx.dir / "promotion.json").write_text(json.dumps(summ, ensure_ascii=False, indent=1), encoding="utf-8")
    st.update({k: v for k, v in summ.items() if k not in ("written", "answers")})
    st["files_written"] = len(summ["written"])
    ctx._ws = None                                               # the candidate's inputs changed
    ctx.say(f"  promoted into the candidate: {len(summ['ops'])} op(s), {len(summ['dispositions'])} disposition(s), "
            f"{len(summ['unresolved'])} unresolved, {len(summ['rows_new'])} new row(s), {len(summ['readings'])} "
            f"reading(s), {len(summ['issues'])} issue(s), {len(summ['activities'])} activit(y/ies), "
            f"{len(summ['clarifications'])} clarification(s), {len(summ['relationships'])} relationship(s)")


# ---------------------------------------------------------------------------------------------- candidate commands

def step_pin(ctx: Ctx, st: dict) -> None:
    from ..cli import pin_cmd
    with CAND.captured(ctx.P["logs"] / "pin.log") as buf:
        code = pin_cmd(ctx.P["build"], ctx.P["pack"], refresh=False)
    st.update(exit_code=code, output=_short(buf.getvalue(), 400))


def step_check_register(ctx: Ctx, st: dict) -> None:
    from .. import stage2
    with CAND.captured(ctx.P["logs"] / "check-register.log") as buf:
        code = stage2.check_register(ctx.P["build"], ctx.P["pack"], ROOT, None, update=True)
    found = [m.groups() for m in re.finditer(r"(?m)^  \[([^\]]+)\] ([^:]*): (.*)$", buf.getvalue())]
    st.update(exit_code=code, findings=len(found), by_kind=dict(Counter(k for k, _, _ in found)),
              first=[f"[{k}] {w}: {_short(d, 200)}" for k, w, d in found[:40]])
    prom = _js(ctx.dir / "promotion.json") or {}
    st["classified"] = classify_register_findings(found, set(prom.get("rows_new") or []))   # session 14 (W2)
    ctx.say(f"  check-register: exit {code}, {len(found)} finding(s) {dict(Counter(k for k, _, _ in found))}")


# session 14 (W2; blind-07 defect 16): which check-register findings are the downstream phase's gap (the run's own new
# rows without the evidence item, activity or reason it should have proposed) and which are real defects
_DELIVERABLE_GAP = ("deliverable",)


def classify_register_findings(found: list, new_rows: set) -> dict:
    """{not_proposed: ["[kind] where: detail" ...], defects: [...]} for check-register's findings `found` ([(kind,
    where, detail)]): a `deliverable` finding on a row this run proposed (`new_rows`) is "missing because downstream
    did not propose" its evidence item, activity or no_deliverable reason; every other finding is a defect."""
    out = {"not_proposed": [], "defects": []}
    for k, w, d in found:
        line = f"[{k}] {w}: {_short(d, 200)}"
        if k in _DELIVERABLE_GAP and w.strip() in new_rows:
            out["not_proposed"].append(line + " (missing because the downstream phase did not propose the row's "
                                              "evidence item, activity or reason)")
        else:
            out["defects"].append(line)
    return out


def step_outputs(ctx: Ctx, st: dict) -> None:
    from .. import stage2
    t0 = time.perf_counter()
    ob = _join_before(ctx)
    st["before"] = {k: v for k, v in ob.items() if k != "pid"}
    st["before_wait_s"] = round(time.perf_counter() - t0, 1)
    out = ctx.P["out"]
    for d in (out, out.with_name(out.name + ".failed"), out.with_name(out.name + ".rejected")):
        if d.exists():
            shutil.rmtree(d)                                    # a previous attempt of this run (never validated)
    r = stage2.run(ctx.P["build"], ctx.P["pack"], ROOT)
    pf = CAND.preflight(r)
    if pf:
        st.update(exit_code=2, refused=True, preflight=pf,
                  reason="pre-flight: " + "; ".join(f"{x['id']} {_short(x['detail'], 200)}" for x in pf))
        ctx.say(f"  outputs REFUSED before the build: {st['reason']}")
        return
    with CAND.captured(ctx.P["logs"] / "outputs.log"):
        res = stage2.build(ctx.P["build"], out, ctx.P["pack"], ROOT, quiet=False)
    st.update(exit_code=res["exit_code"], release=res.get("release"), blockers=len(res.get("blockers") or []),
              out=str(res["out"]))
    if res["exit_code"] != 0:
        failed = [f"{c['id']}: {_short(c['detail'], 200)}" for c in res.get("checks") or [] if not c["ok"]]
        st.update(refused=True, reason=f"exit {res['exit_code']} ({res['status']}): " + "; ".join(failed)
                  + f"; the candidate is in {res['out']} for inspection")
        ctx.say(f"  outputs REFUSED: {st['reason']}")
        return
    statuses, default, legend = _row_statuses(ctx, res["run"])
    marked = CAND.mark(out, statuses, default, legend)
    st.update(refused=False, marked=len(marked), unmarked=[m for m in marked if m.startswith("NOT MARKED")],
              row_statuses=dict(Counter(statuses.get(e["row"].id, default).split(":")[0]
                                        for e in res["run"]["evals"])))
    _review_not_run_note(ctx, out)
    _base_note(ctx, out)
    ctx.say(f"  candidate outputs published to {out} (exit 0; {len(marked)} file(s) carry the banner)")


def base_lines(ctx: "Ctx") -> list[str]:
    """Session 12: what the run starts from, for the candidate README and the review packet."""
    b = ctx.s.get("base_run") or None
    gap = ctx.s.get("missing_addenda") or []
    out = []
    if b:
        out.append(f"- **Base run** `{b['run_id']}`: this candidate starts from that run's candidate "
                   f"(`{b.get('candidate')}`; the chain {' -> '.join(list(b.get('chain') or []) + [ctx.addendum])}); "
                   f"{b['addendum']} is the previous stage of {ctx.addendum}. Its proposals are PROPOSED, not accepted: "
                   "this run is built on unreviewed proposals. The base run was read, never written (fingerprint at "
                   f"start {str(b.get('fingerprint'))[:16]}…).")
    if gap:
        out.append(f"- **Missing addenda**: {missing_reason(gap)}.")
    return out


def _base_note(ctx: "Ctx", out: Path) -> None:
    """The candidate README (and CANDIDATE.md) name the base run (session 12)."""
    lines = base_lines(ctx)
    if not lines:
        return
    for name in ("README.md", "CANDIDATE.md"):
        f = Path(out) / name
        if f.exists():
            f.write_text(f.read_text(encoding="utf-8").rstrip("\n") + "\n\n## Preceding state of this candidate\n\n"
                         + "\n".join(lines) + "\n", encoding="utf-8")


def skipped_reviews(cp: Checkpoint) -> list[tuple[str, str]]:
    """(batch, reason) of every critic recorded `skipped` (session 12: offline without a local critic, a missing
    model, a model that cannot hold the request): an independent review that did not run, never an agreement."""
    return [(k, (cp.batch(k).get("critic") or {}).get("reason") or "no reason recorded")
            for k in cp.batches("analysis") + cp.batches("downstream")
            if (cp.batch(k).get("critic") or {}).get("status") == "skipped"]


def _review_not_run_note(ctx: Ctx, out: Path) -> None:
    """The candidate README says which independent reviews did not run, and why (session 12)."""
    sk = skipped_reviews(ctx.cp)
    readme = Path(out) / "README.md"
    if not sk or not readme.exists():
        return
    lines = ["", "## Independent review (the selective critic)", "",
             "Some selected items had NO second-model review; nothing here implies agreement:", ""]
    lines += [f"- {k}: {_short(r if r.startswith('independent review did not run') else 'independent review did not run: ' + r, 400)}"
              for k, r in sk]
    readme.write_text(readme.read_text(encoding="utf-8").rstrip("\n") + "\n" + "\n".join(lines) + "\n",
                      encoding="utf-8")


def _row_statuses(ctx: Ctx, r: dict) -> tuple[dict, str, list]:
    add = ctx.addendum
    prom = json.loads((ctx.dir / "promotion.json").read_text(encoding="utf-8")) if (ctx.dir / "promotion.json").exists() else {}
    ds, _ = _load_downstream(ctx)
    # session 14 (N2): the promoted item's status, never a later duplicate's "(invalid)"
    vstat = DS.row_item_status(ds.items if ds else [])
    new, readings = set(prom.get("rows_new") or []), set(prom.get("readings") or [])
    answers = json.loads((ctx.dir / "downstream" / "answers.json").read_text(encoding="utf-8")) \
        if (ctx.dir / "downstream" / "answers.json").exists() else {}
    scope_rows: dict[str, list[str]] = {}
    ws = ctx.ws
    if r.get("working") is not None:
        # session 14 (W2; blind-07 defect 7): the candidate A3's own list (partial.unresolved_rows: the op file's
        # unresolved provisions, promoted `unresolved` dispositions included, and the rows they name), so A1, A3 and
        # the packet agree and a superseded value is never shown as "not changed by this run"
        from ..partial import unresolved_rows
        scope_rows = {k: [w for w in v if not w.startswith("STALE")] for k, v in unresolved_rows(r).items()}
    for p, a in answers.items():
        if not a.get("answered"):
            u = ws.units_by_id.get(p) or {}
            pst = ws.stage(ws.prev_stage(add)).state
            from ..citations import citations, resolve
            t = set(resolve(citations(u.get("text") or ""), set(pst)))
            for e in r["evals"]:
                if any(x in t or any(x.startswith(y + "/") for y in t) for x in e["row"].units):
                    lst = scope_rows.setdefault(e["row"].id, [])
                    if not any(w.startswith(p + " ") for w in lst):
                        lst.append(f"{p} UNRESOLVED: {_short(a.get('why'), 160)}")
    out = {}
    for e in r["evals"]:
        rid = e["row"].id
        rv = (r.get("reviews") or {}).get(("row", rid)) or {}
        ev = e["stages"].get(add) or {}
        if rv.get("status") in ("accepted", "rejected"):
            out[rid] = f"DECIDED: {rv['status']} by {rv.get('reviewer')} ({rv.get('date')})"
        elif rid in new:
            out[rid] = f"PROPOSED BY THE AI WORKFLOW: new row at {add} ({vstat.get(rid, 'interpretation_pending')})"
        elif rid in readings:
            out[rid] = f"PROPOSED BY THE AI WORKFLOW: reading re-made at {add} ({vstat.get(rid, 'interpretation_pending')})"
        elif ev.get("stale"):
            out[rid] = f"UNRESOLVED: STALE at {add} (its reading was not re-made: " + _short("; ".join(ev["stale"]), 120) + ")"
        elif scope_rows.get(rid):
            out[rid] = ("UNRESOLVED (value in question): " + "; ".join(
                w.replace(" UNRESOLVED: ", " unresolved: ", 1) for w in scope_rows[rid][:3]))[:400]
        elif rv.get("status") == "changed":
            out[rid] = "DECIDED BEFORE, CHANGED SINCE: review again"
    default = "proposed (existing row; not changed by this run; not reviewed)"
    cnt = Counter(out.get(e["row"].id, default).split(":")[0].split(" (")[0] for e in r["evals"])
    legend = [{"status": "PROPOSED BY THE AI WORKFLOW", "rows": cnt.get("PROPOSED BY THE AI WORKFLOW", 0),
               "meaning": f"a new row or a reading re-made at {add} by this run, validated by the controller; a person "
                          "decides it (accept / reject)"},
              {"status": "UNRESOLVED", "rows": cnt.get("UNRESOLVED", 0),
               "meaning": f"STALE at {add} with no re-made reading, or (value in question) citing a unit an unresolved "
                          f"provision of {add} names: the value shown may be superseded by that provision, which is "
                          "named with its reason (never 'not changed by this run')"},
              {"status": "DECIDED", "rows": cnt.get("DECIDED", 0),
               "meaning": "a named person's decision in the copied decisions file (none means nobody has decided yet)"},
              {"status": "proposed (existing row)", "rows": cnt.get("proposed", 0),
               "meaning": "an existing row this run did not change; not reviewed"}]
    return out, default, legend


def step_diff(ctx: Ctx, st: dict) -> None:
    from .. import live, stage2
    r = stage2.run(ctx.P["build"], ctx.P["pack"], ROOT)
    prev = r["order"][r["order"].index(ctx.addendum) - 1]
    md, data = live.diff(r, prev, ctx.addendum)
    data["stage_status"] = next(s.status for s in r["stages"] if s.stage == ctx.addendum)
    from .. import derived                              # session 12 (W3b): pending readings, computed deadlines, the
    data["derived"] = derived.summary(r, ctx.addendum)  # Working Days left, switched conditions, bands and their rules
    rd = ctx.dir / "review"
    rd.mkdir(parents=True, exist_ok=True)
    (rd / "diff.md").write_text(f"> **{CAND.BANNER}**\n\n" + md, encoding="utf-8")
    (rd / "diff.json").write_text(json.dumps(data, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    cmp_ = _compare_outputs(ctx.P["out_before"], ctx.P["out"], ctx.addendum)
    (rd / "outputs-before-after.json").write_text(json.dumps(cmp_, ensure_ascii=False, indent=1), encoding="utf-8")
    req = data.get("requirements") or {}
    if ctx.s.get("base_run"):                      # session 12: out-before is the base run's candidate state
        st["base_run"] = ctx.s["base_run"]["run_id"]
        st["chain"] = list(ctx.s["base_run"].get("chain") or []) + [ctx.addendum]
    st.update(stage=f"{prev} -> {ctx.addendum}", new=len(req.get("new") or []), out=len(req.get("out") or []),
              changed=len(req.get("changed") or []), stale=len(data.get("stale") or []),
              a3=data.get("a3"), programme=len(data.get("programme") or []), outputs=cmp_.get("summary"))


def _compare_outputs(before: Path, after: Path, addendum: str | None = None) -> dict:
    def j(p):
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
    out: dict = {"before": str(before), "after": str(after)}
    a1b, a1a = j(before / "a1" / "a1.json"), j(after / "a1" / "a1.json")
    a3b, a3a = j(before / "a3" / "a3.json"), j(after / "a3" / "a3.json")
    pb = j(before / "a5" / "programme.json")
    pa = (j(after / "a5" / "working" / f"{addendum}.json") if addendum and (after / "a5" / "working" / f"{addendum}.json").exists()
          else j(after / "a5" / "programme.json"))
    if a1b and a1a:
        ib, ia = {x["id"] for x in a1b["rows"]}, {x["id"] for x in a1a["rows"]}
        out["a1"] = {"rows_before": len(ib), "rows_after": len(ia), "new": sorted(ia - ib), "gone": sorted(ib - ia)}
    if a3b and a3a:
        eb, ea = set(a3b.get("explicit_ids") or []), set(a3a.get("explicit_ids") or [])
        out["a3"] = {"before": len(eb), "after": len(ea), "enters": sorted(ea - eb), "leaves": sorted(eb - ea)}

    def acts(p):
        if isinstance(p, dict):
            p = p.get("activities") or p.get("rows") or []
        return {a.get("id") or a.get("activity") for a in p or [] if isinstance(a, dict)} - {None}
    if pb is not None and pa is not None:
        xb, xa = acts(pb), acts(pa)
        out["a5"] = {"activities_before": len(xb), "activities_after": len(xa), "new": sorted(xa - xb),
                     "gone": sorted(xb - xa)}
    out["summary"] = {k: {kk: (len(vv) if isinstance(vv, list) else vv) for kk, vv in v.items()}
                      for k, v in out.items() if isinstance(v, dict)}
    return out


# ---------------------------------------------------------------------------------------------- step: review

def step_review(ctx: Ctx, st: dict) -> None:
    md = review_markdown(ctx)
    rd = ctx.dir / "review"
    rd.mkdir(parents=True, exist_ok=True)
    (rd / "index.md").write_text(md, encoding="utf-8")
    (rd / "index.html").write_text(md_to_html(md, f"Review: {ctx.addendum}, run {ctx.run_id}"), encoding="utf-8")
    st.update(path=str(rd / "index.md"), html=str(rd / "index.html"), lines=md.count("\n"))


def _rel(p, base: Path) -> str:
    try:
        return Path(os.path.relpath(Path(p).resolve(), Path(base).resolve())).as_posix()
    except (ValueError, OSError):
        return str(p)


def review_markdown(ctx: Ctx) -> str:
    cp, d = ctx.cp, ctx.cp.data
    rd = ctx.dir / "review"
    try:
        cps = ctx.combined()[0]
    except (OSError, KeyError, FileNotFoundError):
        cps = None
    ds, dreport = _load_downstream(ctx)
    def js(p):
        try:
            return json.loads(Path(p).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}
    prom = js(ctx.dir / "promotion.json")
    answers = prom.get("answers") or js(ctx.dir / "downstream" / "answers.json")   # session 13: after downstream
    tasks = {t["id"]: t for t in (js(ctx.dir / "downstream" / "tasks.json") or [])}
    pops = js(ctx.dir / "downstream" / "promoted_ops.json")
    diff = js(rd / "diff.json")
    cmp_ = js(rd / "outputs-before-after.json")
    outs = cp.step("outputs")
    ob = d.get("out_before") or {}
    add = ctx.addendum
    L = [f"# Review packet: {add}, AI workflow run {ctx.run_id}", "",
         f"> **{CAND.BANNER}.** Statuses are the controller's; a person decides every item. The real `curation/`, "
         "`config/` and `out/` were only read: everything below lives in this run's folder.", "",
         f"- PDF: `{(d['inputs'].get('pdf') or {}).get('path')}` (sha256 {(d['inputs'].get('pdf') or {}).get('sha256', '')[:16]}…, "
         f"{(d['inputs'].get('pdf') or {}).get('pages')} pages); preceding state: pack `{d['inputs'].get('pack')}` "
         f"({d['inputs'].get('preceding_pack_id')}), previous evidence build `{d['inputs'].get('evidence')}`",
         f"- route **{ctx.s['route']}**; model requested `{cps.model_requested if cps else ctx.s.get('model')}`, reported "
         f"`{cps.model_reported if cps else None}`" + (" (a recorded fixture: NOT a live model)" if ctx.s["route"] == "recorded" else "")
         + (("; host sessions report: " + ", ".join(sorted({m for b in d["batches"].values()
                                                            for m in (b.get("host_session") or {}).get("model_reported") or []})))
            if any((b.get("host_session") or {}).get("model_reported") for b in d["batches"].values()) else ""),
         "- status **{}**".format(*(_final_status(cp)[:1])) + (": " + _final_status(cp)[1] if _final_status(cp)[1] else "")]
    L += usage_lines(cp)                            # session 14 (W2): the host's own usage; unknown is never 0
    L += code_lines(cp)                             # session 13: the code identity; DIFFERENT_CODE when it changed
    L += base_lines(ctx) + [""]                     # session 12: the base run, the missing addenda
    # ---- session 11: three separate records (checkpoint keys execution, completeness, approval)
    ex, comp, ap = execution(cp), completeness(cp), approval(cp)
    L += ["## Execution, completeness and approval (three separate things)", "",
          "- **Execution** (what ran): " + ", ".join(f"{s} {v}" for s, v in ex["steps"].items())
          + "; batches " + "; ".join(f"{ph}: {dict(c)}" for ph, c in ex["batches"].items()),
          f"- **Completeness** (what the run completed): **{comp['status']}**"
          + (": " + "; ".join(comp["reasons"]) if comp["reasons"] else
             ": every provision answered, every downstream task answered, check-register clean, outputs published"),
          f"  - downstream tasks: {comp['downstream']['tasks']}; answered {comp['downstream']['answered']}; unanswered "
          f"{len(comp['downstream']['unanswered'])}; answered only by items that cannot be promoted "
          f"{len(comp['downstream']['unresolved'])}; answered 'no change' {len(comp['downstream']['no_change'])}",
          f"- **Human approval**: **{ap['status']}** ({ap['by_the_workflow']})"
          + (f"; decisions a person recorded in the candidate's decisions file: {'; '.join(ap['decisions'][:10])}"
             if ap["decisions"] else "; no decision is recorded in the candidate's decisions file"), ""]
    # ---- what is candidate and what is real
    L += ["## What is candidate and what is real", "",
          f"- **Candidate** (proposed by this run, nothing accepted): `{_rel(ctx.P['dir'], rd)}/` — a copy of the curation and "
          f"configuration with {add} added, its evidence build, its op file, rows, issues, templates and outputs.",
          "- **Last validated state**: " + (f"`{_rel(ctx.P['out_before'], rd)}/` (the pre-addendum outputs built from the "
                                             + (f"base run {ctx.s['base_run']['run_id']}'s candidate state "
                                                f"({ctx.s['base_run']['addendum']}, PROPOSED, not accepted): its copied "
                                                "curation and its evidence build; " if ctx.s.get("base_run") else
                                                "copied curation and the previous evidence build; ")
                                             + f"{ob.get('status')}"
                                             + (", from the cache" if (ob.get('result') or {}).get('from_cache') else "")
                                             + ")" if ob.get("status") == "done" else
                                             f"the real `out/` ({ob.get('reason') or ob.get('status')})"),
          "- **Real** (untouched): `curation/`, `config/`, `out/`; the owner's approvals and readings were copied unchanged "
          "and used read-only.", ""]
    real_now = CAND.fingerprint(Path(d["inputs"]["pack"])) if d["inputs"].get("pack") else {}
    changed = sorted(k for k in set(real_now) | set(d["inputs"].get("real_hashes") or {})
                     if real_now.get(k) != (d["inputs"].get("real_hashes") or {}).get(k))
    L += [f"- real inputs changed since the run started: {', '.join(changed[:20]) if changed else 'none'}"
          + (" (by someone else: this run wrote nothing there; the candidate used the copies made at the start)" if changed else ""), ""]
    # ---- outputs
    L += ["## Candidate outputs", ""]
    if outs.get("refused"):
        L += [f"**The candidate outputs build was REFUSED** (exit {outs.get('exit_code')}): {outs.get('reason')}", "",
              "The last validated state stays " + (f"`{_rel(ctx.P['out_before'], rd)}/`." if ob.get("status") == "done"
                                                    else "the real `out/`."), ""]
    elif outs.get("status") == "done":
        o = _rel(ctx.P["out"], rd)
        L += [f"Exit {outs.get('exit_code')} ({outs.get('release')}); every file carries the banner "
              f"(`{o}/CANDIDATE.md`); A1 has a candidate status column {outs.get('row_statuses')}.", "",
              f"| Output | Candidate | Before ({add} not applied) |", "|---|---|---|"]
        b = _rel(ctx.P["out_before"], rd)
        for name, path in (("A1 register", "a1/a1.xlsx"), ("A2 changes", "a2/a2.md"), ("A3 consequences", "a3/a3.pdf"),
                           ("A4 clarification register", "a4/clarification_register.md"), ("A5 programme", "a5/README.md"),
                           ("A5 Gantt", "a5/gantt.html"), ("A5 marshalling", "a5/marshalling.csv"), ("Checks", "checks.json")):
            L.append(f"| {name} | [{o}/{path}]({o}/{path}) | " + (f"[{b}/{path}]({b}/{path})" if ob.get("status") == "done" else "-") + " |")
        L.append("")
    else:
        L += [f"- not built yet (step outputs: {outs.get('status')})", ""]
    if cmp_.get("summary"):
        L += [f"- before → after: {json.dumps(cmp_['summary'], ensure_ascii=False)}", ""]
    stg = (diff.get("stage_status") or "")
    if stg and stg != "APPLIED":
        L += [f"- {add} is **{stg}** in the candidate (provisions unresolved): A3 and the A5 programme show the validated "
              f"state ({diff.get('from')}); {add} as proposed is in A1's `Status after {add}` column, in A2, in the "
              f"candidate A3 and A5 below, in `a5/working/{add}.json` and in the diff below.", ""]
        from ..partial import review_lines              # session 11 (D4): validated vs candidate A3/A5, with the statuses
        L += review_lines(ctx.P["out"], ctx.P["build"], lambda p: _rel(p, rd),
                          {it.payload.get("id", it.id): it.verification_status for it in (cps.items if cps else [])
                           if it.statement_type == "amendment_op"})
    # ---- timings
    L += ["## Timings (wall clock per step)", "", "| Step | Seconds | Status |", "|---|---|---|"]
    t = cp.timings()
    L += [f"| {s} | {t[s]:.1f} | {cp.step(s)['status']} |" for s in STEPS]
    total = sum(t.values())
    L += [f"| **total** | **{total:.1f}** ({total / 60:.1f} min) | target {TARGET_MIN:g} min from the PDF to candidate "
          "outputs and this packet, human review excluded |", ""]
    waits = [(k, b.get("waited_s")) for k, b in d["batches"].items() if b.get("waited_s")]
    if waits:
        L += [f"- waiting for host submissions (not counted): {', '.join(f'{k} {v:.0f} s' for k, v in waits)}", ""]
    if outs.get("before_wait_s"):
        L += [f"- the pre-addendum outputs: waited {outs['before_wait_s']} s at the outputs step "
              f"(built in the background: {(ob.get('result') or {}).get('seconds')} s)", ""]
    # ---- readings of image regions
    rb = cp.batches("reading")
    if rb:
        L += ["## Readings of the addendum's image regions (AI-proposed, PENDING HUMAN REVIEW)", "",
              f"Ingest first refused the candidate because these image regions had no reading (C05): "
              f"{', '.join(cp.batch(k)['region'] for k in rb)}. Each reading below was proposed by the route of this run, "
              "checked by readings.check_reading and written into the candidate's readings; it is an interpretation "
              "of an image, never approved, and every unit made from it carries `reading.status: pending`.", ""]
        for k in rb:
            b = cp.batch(k)
            res = js(b["result"]) if b.get("result") else {}
            prop = res.get("proposal") or {}
            rid = b["region"]
            pk = ctx.P["build"] / "review" / rid / "packet.html"
            L.append(f"- **{rid}** — {b['status']}; controller status **{b.get('verification_status') or '-'}**"
                     + (f"; unit `{b.get('unit_id')}`" if b.get("unit_id") else "")
                     + (f"; file `{_rel(b['reading_file'], rd)}`" if b.get("reading_file") else "")
                     + (f"; error: {_short(b.get('error'), 300)}" if b.get("error") else ""))
            if pk.exists():
                L.append(f"  - the reading beside its crops (the build's review packet): [{_rel(pk, rd)}]({_rel(pk, rd)})")
            r_ = prop.get("reading") or {}
            if r_:
                L.append(f"  - {r_.get('content_type')} reading, languages {r_.get('languages')}; prepared by: "
                         f"{_short(r_.get('prepared_by'), 300)}")
                L += [f"  - uncertainty: {_short(u, 240)}" for u in (r_.get("uncertainties") or [])[:6]]
            L += [f"  - check {v['check']}: {'ok' if v['ok'] else 'FAILED'} — {_short(v['detail'], 240)}"
                  for v in prop.get("validation") or [] if not v["ok"] or "partial" in v["check"] or "warning" in v["check"]]
        L.append("")
    # ---- needs a person first
    unres = [p for p, a in answers.items() if not a.get("answered")]
    esc = [it for it in (cps.items if cps else []) if it.statement_type == "escalation"]
    st_n = Counter((answers.get(p) or {}).get("state") or ("applied" if (answers.get(p) or {}).get("answered")
                                                             else "unresolved") for p in answers)
    L += ["## First: unresolved provisions and escalations", "",
          f"{len(unres)} of {len(d['provisions'])} provisions are not applied or settled by a promoted item (each is "
          f"`unresolved` in the candidate op file with the reason); {len(esc)} escalation(s).",
          f"- states (session 14: kept distinct): applied {st_n.get('applied', 0)}, no effect {st_n.get('no_effect', 0)}, "
          f"partly applied {st_n.get('partly applied', 0)}, unresolved but accounted for {st_n.get('unresolved', 0)}, "
          f"unaccounted {st_n.get('unaccounted', 0)}; approved by a person: none (only a person's recorded decision "
          "approves; see Human approval above)", ""]
    from ..clarify import route_lines                   # session 12 (W3a): the closed clarification route, one wording
    win = diff.get("clarification_window") or {}
    L += route_lines(win) + ([""] if win.get("closed") else [])
    for it in esc:
        sc = ((tasks.get(f"esc:{it.provision}") or {}).get("scope")) or _scope(ctx, it.provision)
        L += [f"- **ESCALATED {it.id}** ({it.provision}): {_short(it.payload.get('why'), 300)}"]
        # session 14 (W2; blind-07 defect 13): the closed-window note only where a clarification would have been the
        # route, never on a software limitation or a schema failure
        L += [f"  - clarification route: {win['note']}"] if win.get("closed") and DS.route_class(
            f"{it.payload.get('why')} {it.payload.get('what_is_unsupported')}") != "software" else []
        L += [
              f"  - unsupported: {_short(it.payload.get('what_is_unsupported'), 300)}",
              "  - evidence: " + ("; ".join(f"{x.unit_id} p{x.page}: “{_short(x.words, 160)}”" for x in it.evidence) or "none"),
              f"  - affected scope: units {', '.join(sc.get('units', [])[:12]) or 'none'}; rows {', '.join(sc.get('rows', [])[:12]) or 'none'}; "
              f"activities {', '.join(sc.get('activities', [])[:12]) or 'none'}; clarifications "
              f"{', '.join(map(str, sc.get('clarifications', [])[:8])) or 'none'}"]
    for p in unres:
        if any(it.provision == p for it in esc):
            continue
        v = d["provisions"].get(p, {})
        L.append(f"- **UNRESOLVED {p}** ({v.get('kind')}, p{','.join(map(str, v.get('pages') or []))}): {answers[p].get('why')}"
                 + (f" — {win['note']}" if win.get("closed") and DS.route_class(answers[p].get("why")) !=
                    "software" else ""))
    L.append("")
    rr = diff.get("answers_to_reread") or []            # session 12 (W3a): superseded answers, for a person
    if rr:
        L += ["## Earlier answers to re-read against the new text (never revoked; a person decides)", ""]
        L += [f"- `{x['answer']}` ({x['issued_by']}): {_short(x['why'], 300)}; {x['reread']}"
              + (f" (downstream task `reread:{x['answer']}`)" if f"reread:{x['answer']}" in tasks else "") for x in rr]
        L.append("")
    from ..derived import review_lines as derived_lines  # session 12 (W3b): derived effects, each for a person
    L += derived_lines(diff.get("derived"))
    # ---- per provision chain
    L += ["## Per provision: source evidence → proposed transition → validation → downstream impact → output difference", ""]
    units = ctx.ws.units_by_id if ctx.P["build"].exists() else {}
    ops_changed = pops.get("ops_changed") or {}
    req = diff.get("requirements") or {}
    prog = diff.get("programme") or []
    for p, v in d["provisions"].items():
        mine = [it for it in (cps.items if cps else []) if it.provision == p]
        u = units.get(p) or {}
        L.append(f"### {p} ({v.get('kind')}, p{','.join(map(str, v.get('pages') or []))}) — "
                 + state_of(answers.get(p)))                # session 14 (W2): the four states, never "answered" alone
        L.append(f"- source: “{_short(u.get('text'), 360)}”")
        if not mine:
            via = v.get("accounted_by")
            L.append("- transition: " + (f"content of {', '.join(via)}" if via else
                                         f"none ({(answers.get(p) or {}).get('why', v.get('status'))})"))
        changed_units, rows_hit = [], set()
        for it in mine:
            bad = next((x for x in it.validation if not x.ok), None)
            L.append(f"- transition: `{it.id}` {it.statement_type} {_transition(it)}")
            L.append(f"  - validation: **{_shown_status(it)}**" + (f" — {bad.check}: {_short(bad.detail, 220)}" if bad else ""))
            L += _critic_item_lines(getattr(getattr(it, "review", None), "critic", None))
            oid = it.payload.get("id", it.id) if it.statement_type == "amendment_op" else None
            if oid and oid in ops_changed:
                changed_units += ops_changed[oid]
        if changed_units:
            rows_hit = {x for t_ in tasks.values() if t_["kind"] == "row_reading"
                        for x in [t_["row"]] if set(c["unit"] for c in t_["changed_units"]) & set(changed_units)
                        or any(c.get("effective_unit") in changed_units for c in t_["changed_units"])}
            L.append(f"  - downstream: units changed {', '.join(sorted(set(changed_units)))}; rows citing them "
                     f"{', '.join(sorted(rows_hit)) or 'none'}")
        dits = [it for it in (ds.items if ds else []) if it.provision == p
                or any(t_ == it.task for t_, tk in tasks.items() if p in (tk.get("provisions") or []))]
        for it in dits:
            L.append(f"  - downstream proposal `{it.id}` {it.statement_type} ({it.task}): **{_shown_status(it)}**"
                     + (f" — held back: {dreport.get('held_back', {}).get(it.id)}" if dreport.get("held_back", {}).get(it.id) else ""))
            L += _critic_item_lines(next((v.get("critic") for v in d["downstream"].get("items", {}).values()
                                          if v.get("id_in_set") == it.id and v.get("critic")), None), "    ")
        rows_all = rows_hit | {(it.payload.get("row") or {}).get("id") if it.statement_type == "row_new" else it.payload.get("row")
                               for it in dits if it.statement_type in ("row_new", "row_reading")} - {None}
        od = [f"NEW {x}" for x in req.get("new") or [] if x in rows_all] + \
             [f"OUT {x}" for x in req.get("out") or [] if x in rows_all] + \
             [f"CHANGED {x}" for x in req.get("changed") or [] if x in rows_all] + \
             [f"CONFIRMED (unchanged) {x}" for x in req.get("confirmed") or [] if x in rows_all] + \
             [f"A3 enters {x}" for x in (diff.get("a3") or {}).get("enters") or [] if x in rows_all] + \
             [f"A5 {g['change']} {g['activity']}" for g in prog if any(x in g.get("detail", "") for x in rows_all)]
        if od:
            L.append(f"  - output difference: {'; '.join(od[:20])}")
        L.append("")
    # ---- downstream items
    if ds:
        L += ["## Downstream proposals (validated in the candidate)", "",
              "| Item | Type | Task | Status | First failed check, or what a person confirms |", "|---|---|---|---|---|"]
        for it in ds.items:
            bad = next((x for x in it.validation if not x.ok), None)
            note = next((x.detail for x in it.validation if x.ok and x.check == HO.CHECK), "") or \
                next((x.detail for x in it.validation if x.ok and x.check in ("interpretation", "duration", "relationship")), "")
            if win.get("closed") and (it.statement_type == "clarification_item" or (
                    it.statement_type == "escalation" and DS.route_class(" ".join(
                        str(v) for v in (it.payload or {}).values())) != "software")):
                note = (note + "; " if note else "") + win["note"]          # session 12: never suggested as sendable
            L.append(f"| {it.id} | {it.statement_type} | {it.task} | {_shown_status(it)} | "
                     f"{_short((bad.check + ': ' + bad.detail) if bad else note, 200).replace('|', '/')} |")
        L.append("")
        if dreport.get("schedule_problems") or dreport.get("interactions"):
            L += ["- interactions: " + "; ".join(_short(x, 200) for x in (dreport.get("interactions") or [])[:10])
                  if dreport.get("interactions") else "- interactions: none",
                  "- A5 problems the proposals would add: " + ("; ".join(_short(x, 200) for x in dreport.get("schedule_problems")[:10])
                                                              if dreport.get("schedule_problems") else "none"), ""]
        if dreport.get("deliverable_gaps"):         # session 14 (W2; blind-07 defect 16)
            L += ["- new rows without the deliverables the downstream phase should have proposed (check-register "
                  "reports them as a downstream gap): " + "; ".join(f"{k}: {v}" for k, v in
                                                                    dreport["deliverable_gaps"].items())[:1500], ""]
    elif tasks:
        L += ["## Downstream proposals", "", f"- {len(tasks)} task(s); no downstream set was produced "
              "(batches: " + ", ".join(k + " " + cp.batch(k)["status"] for k in cp.batches("downstream")) + ")", ""]
    # ---- promotion
    if prom:
        L += promotion_lines(prom, pops)
    # ---- checks
    cr = cp.step("check_register")
    if cr.get("status") == "done":
        L += ["## check-register on the candidate", "", f"- exit {cr.get('exit_code')}; {cr.get('findings')} finding(s) "
              f"{cr.get('by_kind')}"]
        cl = cr.get("classified")
        if cl:                                   # session 14 (W2): a downstream gap is not a register defect
            L += [f"- missing because the downstream phase did not propose them (the run's own new rows): "
                  f"{len(cl['not_proposed'])}"] + [f"  - {x}" for x in cl["not_proposed"][:20]]
            L += [f"- defects: {len(cl['defects'])}"] + [f"  - {x}" for x in cl["defects"][:25]] + [""]
        else:
            L += [f"  - {x}" for x in (cr.get("first") or [])[:25]] + [""]
    # ---- session 13: the analysis items not promoted from the analysis set, under their own heading
    L += carried_lines(cps, pops, tasks, ds, dreport.get("held_back") or {}, win)
    # ---- coverage
    cov = (cps.coverage.model_dump() if cps else {})
    L += ["## Coverage", "", f"- provisions: {len(d['provisions'])}; accounted for by the combined set: {cov.get('accounted')}; "
          f"states {dict(Counter(v['status'] for v in d['provisions'].values()))}"]
    via = {p: a["carried"] for p, a in answers.items() if a.get("carried")}
    if via:                                              # session 13: accounted for through a downstream task
        L.append(f"- accounted for through downstream tasks (analysis rows carried; never a silent gap): {len(via)} "
                 + "; ".join(f"{p} → {', '.join(t)}" + (" (unresolved)" if answers[p]["why"].startswith("unresolved")
                                                       else "") for p, t in via.items()))
    res = cp.step("validation").get("resolution")
    if res:
        L.append(f"- the analysis ITEMS' resolution by the controller (items, not provisions; session 14): resolved "
                 f"{res.get('resolved')}, pending {res.get('pending')}, invalid {res.get('invalid')}, unaccounted "
                 f"{res.get('unaccounted')}; approved {res.get('approved')}")
    L.append(f"- structural units of {add} that are not provisions (listed so nothing is dropped): "
             + ", ".join(f"{x['unit_id']} ({x['kind']})" for x in d.get("structure") or []))
    L += ["- batches: " + ", ".join(f"{k} {b['status']}" + (f" ({_short(b.get('error'), 80)})" if b.get("error") else "")
                                     for k, b in d["batches"].items()), ""]
    # ---- session 11: the critic, and what the request layer did (failure classes, deferrals, repairs, notices)
    L += critic_section(ctx, cps, ds) + requests_section(cp)
    # ---- interventions
    L += intervention_lines(cp)                     # session 14 (W2): the person's stop and resume, killed and reused
    # ---- diff
    dm = rd / "diff.md"
    if dm.exists():
        text = dm.read_text(encoding="utf-8").split("\n", 2)[-1]
        lines = text.splitlines()
        L += [f"## The diff ({diff.get('from')} → {diff.get('to')}; [diff.md](diff.md))", ""]
        L += [("#" + x) if x.startswith("#") else x for x in lines[:250]]
        if len(lines) > 250:
            L.append(f"… {len(lines) - 250} more lines in [diff.md](diff.md)")
        L.append("")
    L += ["## Next (a person)", "",
          "- read the unresolved and escalated provisions first, then each item against its evidence "
          f"(`{_rel(ctx.dir / 'ai' / (ctx.run_id + '-combined'), rd)}/proposals.yaml`, "
          f"`{_rel(ctx.dir / 'downstream' / 'proposals.yaml', rd)}`)",
          "- nothing here is applied to the real curation: to take an item over, add the PDF to the pack (OPERATING_GUIDE "
          "§3 steps 1-2) and copy the reviewed files listed in `promotion.json`; then `pin`, `check-register`, `outputs` "
          "and decide with `accept` / `reject` as usual", ""]
    return "\n".join(L)


def _critic_item_lines(c, indent: str = "  ") -> list[str]:
    """One item's critic finding for the review packet (a CriticReview or its dict)."""
    if c is None:
        return []
    g = (lambda k: c.get(k)) if isinstance(c, dict) else (lambda k: getattr(c, k, None))
    out = [f"{indent}- critic (a second model; agreement is not approval): {'agrees' if g('agrees') else 'DOES NOT agree'}"
           f" — selected because {', '.join(g('selected_because') or [])}"
           + (f"; model {g('model_reported') or g('model_requested')}" if (g('model_reported') or g('model_requested'))
              else "")]
    out += [f"{indent}  - concern: {_short(x, 300)}" for x in g("concerns") or []]
    return out


def _shown_status(it) -> str:
    """An item's status as the review packet shows it (session 12): a human-owned item (tenderpack.human_owned) carries
    HUMAN DECISION PENDING beside its controller status; nothing it concludes is presented as settled."""
    ap = next((v for v in getattr(it, "validation", None) or [] if v.check == "applied rule"), None)
    return it.verification_status + (f" — {HO.HUMAN_DECISION_PENDING}" if HO.is_human_owned(it) else "") + (
        f" — applied rule: {_short(ap.detail, 240).replace('|', '/')}" if ap else "")   # session 12 (follow-up 12)


def critic_section(ctx: Ctx, cps, ds) -> list[str]:
    """The review packet's Critic section (session 11): per batch, what was selected and reviewed, and every finding."""
    cp = ctx.cp
    rows = [(k, cp.batch(k).get("critic")) for k in cp.batches("analysis") + cp.batches("downstream")
            if cp.batch(k).get("critic")]
    if not rows:
        return []
    L = ["## Critic (a second model over the selected items; it changed no status)", "",
         "**Agreement between the critic and the proposer is not approval**: every item still needs a person's decision, "
         "and a disagreement is a concern for that person, not a rejection. The critic reviews only the selected classes "
         "(consequential interpretations, uncertain targets, removals, conflicting evidence), in one request per batch.",
         "", "| Batch | Critic | Selected | Reviewed | Agrees | Does not agree | Note |", "|---|---|---|---|---|---|---|"]
    for k, c in rows:
        note = c.get("reason") or c.get("error") or (f"no review for {c.get('missing')}" if c.get("missing") else "") \
            or (f"over the limit: {c.get('not_reviewed_over_limit')}" if c.get("not_reviewed_over_limit") else "")
        L.append(f"| {k} | {c.get('status')} | {c.get('selected', 0)} | {c.get('reviewed', '-')} | {c.get('agrees', '-')} | "
                 f"{c.get('disagrees', '-')} | {_short(note, 200).replace('|', '/')} |")
    L.append("")
    sk = [(k, c) for k, c in rows if c.get("status") == "skipped" and c.get("selected")]
    if sk:                                                       # session 12: a review that did not run, said plainly
        L += ["**Reviews that did not run** (the selected items below had NO second-model review; this is not "
              "agreement):", ""]
        L += [f"- **{k}** ({c.get('selected')} selected item(s): {', '.join(c.get('selected_items') or {})}): "
              f"{_short(c.get('reason'), 400)}" for k, c in sk]
        L.append("")
    by = {it.id: it for it in (cps.items if cps else [])}
    dsby = {it.id: it for it in (ds.items if ds else [])}
    for k, c in rows:
        for key, v in (c.get("items") or {}).items():
            it = by.get(key) if k.startswith("analysis") else dsby.get(key)
            st = getattr(it, "verification_status", "?")
            L.append(f"- **{key}** ({k}; controller status **{st}**, unchanged)")
            L += _critic_item_lines({**v, "model_reported": c.get("model_reported")})
    L.append("")
    return L


def requests_section(cp: Checkpoint) -> list[str]:
    """The review packet's section on the request layer (session 11): failure classes and their attempts, deferrals,
    splits and escalations by size, repairs and malformed items, and every route notice (capabilities used unverified
    or declared by the host; structured output not used or rejected)."""
    d = cp.data
    L = ["## Requests: failures, deferrals, repairs and route notices", ""]
    any_ = False
    for k, b in d["batches"].items():
        bits = []
        if b.get("failure_class"):
            bits.append(f"failure class **{b['failure_class']}**")
        f = b.get("failures") or []
        if f:
            waits = [x.get("wait_s") for x in f if x.get("wait_s")]
            bits.append(f"{len(f)} failed call(s) ({', '.join(sorted({x['class'] for x in f}))})"
                        + (f", waited {', '.join(f'{w:g}' for w in waits)} s" if waits else ""))
        for x in b.get("deferrals") or []:
            bits.append(f"DEFERRED {x.get('ts')}: {_short(x.get('message'), 200)}"
                        + (f" (reset named in about {x['reset_in_s'] / 60:.0f} min)" if x.get("reset_in_s") else ""))
        if b.get("status") in ("split", "escalated"):
            bits.append(f"{b['status'].upper()}: {_short(b.get('error'), 300)}" + (f"; parts {b.get('parts')}"
                                                                                    if b.get("parts") else ""))
        rq = b.get("request") or {}
        if rq.get("repaired"):
            bits.append(f"repaired once ({len(rq.get('problems_before_repair') or [])} problem(s) before the re-ask)")
        for m in rq.get("reference_problems") or []:
            bits.append(f"item {m.get('id')!r} kept with a reference problem after the re-ask (the controller rates it): "
                        + _short("; ".join(m.get("errors") or []), 160))
        for m in b.get("malformed_items") or []:
            bits.append(f"malformed item {m.get('id')!r} ({m.get('provision') or m.get('task') or ''}): "
                        + _short("; ".join(m.get("errors") or []), 200))
        if bits:
            any_ = True
            L.append(f"- **{k}** ({b.get('status')}): " + "; ".join(bits))
    if not any_:
        L.append("- every request was answered at the first call, parsed, and fitted its context")
    notes = d.get("notices") or []
    L += ["", "Route notices (how the requests were served; they change no status):"]
    L += [f"- **{'capabilities unverified' if n.get('kind') == 'capabilities_unverified' else n.get('kind')}** "
          f"({n.get('batch')}): {_short(n.get('message'), 400)}" for n in notes] or ["- none"]
    L.append("")
    return L


def _scope(ctx: Ctx, pid: str) -> dict:
    try:
        return DS.scope_of(ctx.ws, ctx.ws.r, ctx.addendum, pid)
    except Exception:                                            # noqa: BLE001 (a report; never blocks the packet)
        return {}


def _transition(it) -> str:
    p = it.payload
    if it.statement_type == "amendment_op":
        bits = [p.get("type"), p.get("target") or p.get("anchor") or p.get("new_group") or ", ".join(p.get("targets") or [])]
        if p.get("old") or p.get("new"):
            bits.append(f"“{_short(p.get('old'), 80)}” → “{_short(p.get('new') or p.get('new_text'), 80)}”")
        elif p.get("new_text"):
            bits.append(f"“{_short(p.get('new_text'), 120)}”")
        if p.get("effect"):
            bits.append(f"effect {p['effect']}")
        return " ".join(str(b) for b in bits if b)
    if it.statement_type == "disposition":
        return f"{p.get('disposition')}: {_short(p.get('reason'), 160)}"
    if it.statement_type == "escalation":
        return f"why: {_short(p.get('why'), 200)}"
    return _short(json.dumps(p, ensure_ascii=False), 200)


def md_to_html(md: str, title: str) -> str:
    """A small Markdown subset (headings, lists, tables, links, bold, code, quotes) as one HTML page."""
    def inline(t: str) -> str:
        t = html.escape(t, quote=False)
        t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        return t
    out, in_list, in_table = [], False, False
    for line in md.splitlines():
        if in_table and not line.startswith("|"):
            out.append("</table>")
            in_table = False
        if in_list and not re.match(r"^\s*- ", line):
            out.append("</ul>")
            in_list = False
        if m := re.match(r"^(#{1,4}) (.*)", line):
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
        elif line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r"-+", c) for c in cells):
                continue
            if not in_table:
                out.append("<table>")
                in_table = True
                out.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in cells) + "</tr>")
            else:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
        elif m := re.match(r"^(\s*)- (.*)", line):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li{' class=sub' if m.group(1) else ''}>{inline(m.group(2))}</li>")
        elif line.startswith("> "):
            out.append(f"<blockquote>{inline(line[2:])}</blockquote>")
        elif line.strip():
            out.append(f"<p>{inline(line)}</p>")
    if in_list:
        out.append("</ul>")
    if in_table:
        out.append("</table>")
    css = ("body{font:14px/1.45 sans-serif;max-width:1200px;margin:16px auto;padding:0 16px;color:#111}"
           "table{border-collapse:collapse;margin:8px 0}td,th{border:1px solid #bbb;padding:3px 6px;vertical-align:top;"
           "font-size:13px}th{background:#eee}code{background:#f3f3f3;padding:0 3px}li.sub{margin-left:24px;"
           "list-style:circle}blockquote{background:#fde2e2;border:2px solid #b00000;color:#7a0000;padding:6px 10px;"
           "margin:8px 0;font-weight:bold}")
    return (f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(title)}</title><style>{css}</style>"
            f"</head><body>{CAND.HTML_BANNER}" + "\n".join(out) + "</body></html>\n")


STEP_FUNCS = {"ingest": step_ingest, "readings": step_readings, "analysis": step_analysis, "validation": step_validation,
              "downstream": step_downstream, "downstream_validation": step_downstream_validation,
              "critic": step_critic, "promotion": step_promotion, "pin": step_pin, "check_register": step_check_register,
              "outputs": step_outputs, "diff": step_diff, "review": step_review}


# ---------------------------------------------------------------------------------------------- submit-batch

def submit_batch(run_id: str, file, by: str, host_model: str | None = None, batch: str | None = None, staging=None,
                 cont: bool = True, echo=print, sleep=time.sleep, allow_code_change: str | None = None) -> dict:
    """The manual host path: a host (a coding assistant without MCP, or a person) answered a batch's task packet with
    a proposal set (analysis) or a downstream set (downstream). The set is validated exactly as an API run's, the
    submission is recorded (who, when, the file and its sha256, the declared host model), and the run continues."""
    if not (by or "").strip():
        raise B.Refused("--by must name who submits the batch (a person, or the host session); it is recorded")
    cp = load(run_id, staging)
    check_code_identity(cp, allow_code_change)       # session 13: a submission is validated by the code of this segment
    waiting = [k for k, b in cp.data["batches"].items() if b["status"] == "waiting_for_host"]
    bid = batch or (waiting[0] if len(waiting) == 1 else None)
    if bid is None:
        raise B.Refused(f"name the batch with --batch (waiting: {waiting or 'none'})")
    if bid not in cp.data["batches"] or cp.batch(bid)["status"] != "waiting_for_host":
        raise B.Refused(f"batch {bid} is not waiting for a host submission ({cp.data['batches'].get(bid, {}).get('status')})")
    lock = RunLock(cp.path.parent)
    try:
        lock.acquire()
    except RunLockError as e:
        raise B.Refused(str(e)) from None
    ctx = Ctx(cp, echo, sleep)
    try:
        b = cp.batch(bid)
        path = Path(file).absolute()
        sha = sha256_file(path)
        data = controller._load_set_data(path)
        # session 11: the request layer's checks of an answer (the envelope, every item, the references); on the manual
        # path the re-ask is the submitter's: a submission with problems is not taken and the batch keeps waiting
        sp = R.spec(b["phase"], route="mcp")             # the manual path: the checks of the phase's answer
        pk = json.loads(Path(b["packet"]).read_text(encoding="utf-8")) if b.get("packet") and Path(b["packet"]).exists() \
            else None
        if sp.phase == "downstream" and isinstance(data, dict) and "downstream_set" in data:
            data = data["downstream_set"]
        _, env, probs = R.check(sp, data, pk)
        if env or probs:
            err = "; ".join(env + [f"item {p['index']} ({p.get('id')}): {' | '.join(p['errors'])}" for p in probs])
            b.update(last_submission_error=_short(err, 2000))
            cp.intervention(kind="submit-batch (not taken)", batch=bid, phase=b["phase"], by=by.strip(),
                            host_model=host_model, file=str(path), sha256=sha, note=_short(err, 600))
            raise B.Refused(f"the submission does not pass the checks of a {sp.phase} answer ({_short(err, 1500)}); "
                            "nothing was taken and the batch still waits for a submission")
        if b["phase"] == "reading":
            hm = (host_model or ctx.s.get("host_model") or "undeclared").strip()
            fields = {"run_id": f"{ctx.run_id}-{bid}", "created": now_iso(), "route": "host", "provider": "host",
                      "model_requested": hm, "model_reported": None, "task": RR.READING_TASK}
            try:
                prop = RR.parse(data, fields, [])
            except RR.RegionError as e:
                raise B.Refused(f"the file is not a reading proposal: {e}") from None
            _take_reading(ctx, bid, b["region"], prop, f"a host (submitted by {by.strip()}; declared model {hm})")
            n_items = 1
            if b["status"] != "done":
                err = b.get("error")
                b.update(status="waiting_for_host", error=None, last_submission_error=err)
                cp.intervention(kind="submit-batch (not taken)", batch=bid, phase=b["phase"], by=by.strip(),
                                host_model=host_model, file=str(path), sha256=sha, note=err)
                raise B.Refused(f"the submitted reading was not taken ({err}); the batch still waits for a submission")
        elif b["phase"] == "analysis":
            hm = (host_model or ctx.s.get("host_model") or "").strip()
            if not hm:
                raise B.Refused("--host-model must name the model the host used (recorded as declared, not verified)")
            res = controller.submit(ctx.ws, data, hm, via=f"workflow submit-batch {ctx.run_id} {bid}")
            ps, _ = _load_staged(ctx.ws, res["run_id"])
            todo = [p for p in b["provisions"] if cp.provision(p)["status"] == "pending"]
            _take_analysis(ctx, bid, ps, todo)
            n_items = len(b.get("items") or [])
            if b["status"] != "done":
                err = b.get("error")
                b.update(status="waiting_for_host", error=None, last_submission_error=err)
                cp.intervention(kind="submit-batch (not taken)", batch=bid, phase=b["phase"], by=by.strip(),
                                host_model=host_model, file=str(path), sha256=sha, note=err)
                raise B.Refused(f"the submitted set was not taken ({err}); the batch still waits for a submission")
        else:
            fields = {"run_id": f"{ctx.run_id}-{bid}", "created": now_iso(), "route": "host", "provider": "host",
                      "model_requested": (host_model or ctx.s.get("host_model") or "undeclared").strip(),
                      "model_reported": None, "task": DOWNSTREAM_TASK}
            try:
                ds = DS.parse(data, fields, [])
            except DS.DownstreamParseError as e:
                raise B.Refused(f"the file is not a DownstreamSet: {e}") from None
            _take_downstream(ctx, bid, ds, ctx.dir / "batches" / f"{bid}.result.json")
            n_items = len(ds.items)
        if b.get("waiting_epoch"):
            b["waited_s"] = round(b.get("waited_s", 0.0) + time.time() - b["waiting_epoch"], 1)
        cp.intervention(kind="submit-batch", batch=bid, phase=b["phase"], by=by.strip(), host_model=host_model,
                        file=str(path), sha256=sha, items=n_items, status=b["status"])
        ctx.say(f"{bid}: {b['status']} ({n_items} item(s)) submitted by {by.strip()}")
    finally:
        lock.release()
    if cont:
        return resume(run_id, staging, retry_failed=False, echo=echo, sleep=sleep, by_person=False)
    return summary(cp)
