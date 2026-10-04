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
"""
from __future__ import annotations

import datetime as dt
import html
import json
import os
import re
import secrets
import shutil
import time
import traceback
import typing
from collections import Counter
from pathlib import Path

import yaml

from ..util import ROOT, load_yaml, sha256_file
from . import budget as B
from . import candidate as CAND
from . import config as C
from . import controller
from . import downstream as DS
from . import regionread as RR
from .checkpoint import STEPS, Checkpoint, RunLock, RunLockError, now_iso
from .contract import DOWNSTREAM_TASK, DownstreamSet, ProposalSet
from .runlog import RunLog
from .tools import Workspace

ROUTES = ("recorded", "host", "anthropic", "openrouter", "ollama")
API_ROUTES = ("anthropic", "openrouter", "ollama")
TARGET_MIN = 30.0
EXIT_CODES = {"complete": 0, "partial": 0, "stopped": 0, "waiting_for_host": 4, "failed": 1, "refused": 2}


class WaitingForHost(Exception):
    pass


class StopRun(Exception):
    def __init__(self, status: str, reason: str):
        super().__init__(reason)
        self.status, self.reason = status, reason


class BatchFailed(Exception):
    pass


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
          - phase: reading | analysis | downstream
            when: {regions_include: [region id]} | {provisions_include: [unit ids]} | {tasks_include: [task ids]}
            turns: [...]                              the RecordedProvider turns of that batch
    A batch takes the first unused session of its phase whose `when` holds; a batch no session covers fails with
    "no recorded session" and its provisions stay pending (a resumed run asks again)."""

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
                    + list(w.get("regions_include") or []))
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
        return {b["session"] for b in self.cp.data["batches"].values() if b.get("session") is not None
                and b["status"] in ("done", "running")}

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
          cache: bool = True, echo=print, sleep=time.sleep) -> dict:
    """Start a run (see the module docstring). Refuses (budget.Refused / candidate.CandidateError) before creating
    anything when the inputs cannot work."""
    if route not in ROUTES:
        raise B.Refused(f"unknown route {route!r} ({', '.join(ROUTES)})")
    if stop_after and stop_after not in STEPS:
        raise B.Refused(f"--stop-after must be one of {', '.join(STEPS)}")
    if route == "recorded" and not cassette:
        raise B.Refused("the recorded route needs --cassette (a recorded workflow; not a live integration)")
    if int(batch_size) < 1 or int(downstream_batch_size) < 1:
        raise B.Refused("batch sizes must be at least 1")
    pack = Path(pack or ROOT / "config/pack.yaml").absolute()
    evidence = Path(evidence or ROOT / "build").absolute()
    staging = Path(staging or ROOT / "staging/ai").absolute()
    worklog = Path(worklog or ROOT / "worklog/model_calls").absolute()
    CAND.check(pack, addendum, Path(pdf))
    rd = B.safe_staging(runs_dir(staging), ROOT, evidence)
    run_id = B.check_run_id(run_id or new_run_id(addendum, route))
    if (rd / run_id).exists():
        raise B.Refused(f"run {run_id} exists ({rd / run_id}): resume it with `tenderpack ai resume {run_id}`")
    if route not in ("recorded", "host"):
        cfg = C.load(Path(ai_config) if ai_config else None)
        rcfg = C.route(cfg, route)
        mdl = model or C.default_model(rcfg)
        B.check_startable(route, rcfg, C.caps(cfg, route, caps), B.price_for(cfg, mdl or ""))
    settings = {"addendum": addendum, "pdf": str(Path(pdf).absolute()), "route": route, "pack": str(pack),
                "evidence": str(evidence), "staging": str(staging), "worklog": str(worklog),
                "ai_config": str(Path(ai_config).absolute()) if ai_config else None, "batch_size": int(batch_size),
                "downstream_batch_size": int(downstream_batch_size), "model": model,
                "cassette": str(Path(cassette).absolute()) if cassette else None,
                "caps": {k: v for k, v in (caps or {}).items() if v is not None}, "host_model": host_model,
                "host_mode": host_mode, "host_session_model": host_session_model,
                "allow_unverified_capabilities": bool(allow_unverified_capabilities),
                "background_before": bool(background_before), "cache": bool(cache)}
    cp = Checkpoint.new(rd / run_id / "checkpoint.json", run_id=run_id, addendum=addendum, settings=settings,
                        inputs={"pack": str(pack), "evidence": str(evidence)}, candidate={})
    cp.event("started", by_pid=os.getpid())
    return _drive(cp, stop_after, echo, sleep)


def load(run_id: str, staging=None) -> Checkpoint:
    staging = Path(staging or ROOT / "staging/ai").absolute()
    p = runs_dir(staging) / B.check_run_id(run_id) / "checkpoint.json"
    if not p.exists():
        raise B.Refused(f"no run {run_id} under {runs_dir(staging)}")
    return Checkpoint.load(p)


def resume(run_id: str, staging=None, stop_after: str | None = None, retry_failed: bool = True, echo=print,
           sleep=time.sleep) -> dict:
    """Continue a stopped, interrupted, failed or waiting run from its checkpoint. Done steps and batches are skipped;
    a batch that failed is asked again (`retry_failed`), and the steps after it are recomputed from the candidate as it
    was before any promotion."""
    if stop_after and stop_after not in STEPS:
        raise B.Refused(f"--stop-after must be one of {', '.join(STEPS)}")
    cp = load(run_id, staging)
    cp.event("resumed", by_pid=os.getpid(), status_before=cp.data["status"])
    if retry_failed:
        for phase, step in (("reading", "readings"), ("analysis", "analysis"), ("downstream", "downstream")):
            failed = [k for k in cp.batches(phase) if cp.batch(k)["status"] in ("failed", "interrupted", "running")]
            if failed:
                for k in failed:
                    cp.batch(k)["status"] = "pending"
                _reset_from(cp, step)
                break
    return _drive(cp, stop_after, echo, sleep)


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
    cp.set_status("running")
    step = None
    try:
        for step in STEPS:
            if cp.done(step):
                continue
            ctx.say(f"[{ctx.run_id}] {step} ...")
            with cp.timed(step) as st:
                STEP_FUNCS[step](ctx, st)
            if stop_after == step and step != STEPS[-1]:
                raise StopRun("stopped", f"stopped after {step} (--stop-after); resume with `tenderpack ai resume "
                                         f"{ctx.run_id}`")
        cp.set_status(*_final_status(cp))
    except WaitingForHost as w:
        cp.set_status("waiting_for_host", str(w))
        ctx.say(str(w))
    except StopRun as s:
        cp.set_status(s.status, s.reason)
        ctx.say(f"{s.status.upper()}: {s.reason}")
    except KeyboardInterrupt:
        _interrupted(cp)
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
        lock.release()
    out = summary(cp)
    for line in timing_lines(cp):
        ctx.echo(line)
    ctx.echo(f"run {ctx.run_id}: {out['status']}" + (f" ({out['status_reason']})" if out.get("status_reason") else ""))
    if (ctx.dir / "review" / "index.md").exists():
        ctx.echo(f"review packet: {ctx.dir / 'review' / 'index.md'}")
    return out


def _interrupted(cp: Checkpoint) -> None:
    for b in cp.data["batches"].values():
        if b["status"] == "running":
            b["status"] = "interrupted"
    cp.save()


def _final_status(cp: Checkpoint) -> tuple[str, str | None]:
    outs = cp.step("outputs")
    unres = (cp.step("promotion").get("unresolved") or [])
    if outs.get("refused"):
        return "partial", f"the candidate outputs build was refused ({outs.get('reason')}); out-before stays the last " \
                          "validated state"
    if unres:
        return "partial", f"{len(unres)} provision(s) unresolved in the candidate (listed first in the review packet)"
    return "complete", None


def summary(cp: Checkpoint) -> dict:
    d = cp.data
    prov = Counter(v["status"] for v in d["provisions"].values())
    return {"run_id": d["run_id"], "addendum": d["addendum"], "status": d["status"], "status_reason": d["status_reason"],
            "exit_code": 1 if d["status"] in ("complete", "partial") and cp.step("outputs").get("refused")
            else EXIT_CODES.get(d["status"], 1),
            "run_dir": str(cp.path.parent), "provisions": dict(prov), "timings": cp.timings(),
            "total_seconds": round(sum(cp.timings().values()), 1),
            "review": str(cp.path.parent / "review" / "index.md"),
            "waiting": [k for k, b in d["batches"].items() if b["status"] == "waiting_for_host"]}


def timing_lines(cp: Checkpoint) -> list[str]:
    return ["timings (wall clock per step):"] + cp.timing_lines(TARGET_MIN)


# ---------------------------------------------------------------------------------------------- step: ingest

def step_ingest(ctx: Ctx, st: dict) -> None:
    cp, s = ctx.cp, ctx.s
    if not ctx.P["pack"].exists():
        if ctx.P["dir"].exists():
            shutil.rmtree(ctx.P["dir"])                         # an interrupted creation: made again from the copies
        info = CAND.create(ctx.dir, Path(s["pack"]), ctx.addendum, Path(s["pdf"]), ctx.run_id)
        cp.data["candidate"] = {k: info[k] for k in ("dir", "pack", "pack_before", "build", "out", "out_before", "pdf_copy")}
        cp.data["inputs"].update(pdf=info["pdf"], copied=info["copied"], real_hashes=info["real_hashes"],
                                 preceding_pack_id=info["preceding_pack_id"])
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
        raise StopRun("stopped", f"ingest refused the candidate (exit {res['exit_code']}): {st['reason']}")
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
    st["batches"] = {k: cp.batch(k)["status"] for k in cp.batches("reading")}
    st["readings"] = {cp.batch(k)["region"]: {"status": cp.batch(k).get("verification_status"),
                                              "file": cp.batch(k).get("reading_file")} for k in cp.batches("reading")}
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
                                 f"{res['exit_code']}): {res.get('reason') or res['status']}")
    ctx.say(f"  ingest with the proposed readings: ok ({res.get('units')} units; readings PENDING HUMAN REVIEW: "
            f"{res.get('pending_review')})")
    _after_ingest(ctx, st)


def _reading_batch(ctx: Ctx, st: dict, bid: str, rid: str) -> None:
    cp, s = ctx.cp, ctx.s
    b = cp.batch(bid)
    b.update(status="running", pid=os.getpid(), attempts=b.get("attempts", 0) + 1, started=now_iso())
    b.pop("error", None)
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
            packet["system"] = RR.SYSTEM
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
                prov = make(s["route"], s.get("model") or C.default_model(rcfg), ctx.cfg, None)
            prop = _converse(ctx, prov, packet, bid, system=RR.SYSTEM, parse=RR.parse, task=RR.READING_TASK,
                             tool_names=["get_region", "validate_reading"], ws=rws)
            who = f"{s['route']} route, model {prov.model}"
        _take_reading(ctx, bid, rid, prop, who)
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


def _reading_host_session(ctx: Ctx, hs, rws: Workspace, bid: str, packet: dict):
    """A reading in a headless host session over the MCP tools (get_region shows the images; validate_reading checks the
    draft); the session's final message is the proposal. It writes nothing and submits nothing."""
    from .providers.recorded import PACKET_MARK

    class ReadingSession(hs.HostSession):
        def system_prompt(self):
            return RR.SYSTEM + ("\nHost session rules: you work ONLY through the tenderpack MCP tools get_region and "
                                "validate_reading; the packet is below; do not call any other tool. Your final message "
                                "is ONLY the JSON object {region_id, reading, model_rationale}.")

        def command(self, mcp_path):
            cmd = super().command(mcp_path)
            if "--allowedTools" in cmd:
                cmd[cmd.index("--allowedTools") + 1] = ",".join(hs.TOOL_PREFIX + x for x in ("get_region",
                                                                                            "validate_reading"))
            if "--disallowedTools" in cmd:
                i = cmd.index("--disallowedTools")
                cmd[i + 1] += "," + hs.TOOL_PREFIX + "submit_proposals"
            return cmd

        def prompt(self, pk):
            return PACKET_MARK + json.dumps({k: v for k, v in pk.items() if k != "system"}, ensure_ascii=False, default=str)

        def _finish(self, log, pk, res, stdout):               # no proposal set: the final message is the answer
            log.event("end", **{k: v for k, v in res.to_dict().items() if k != "final_text"},
                      note="a reading session submits nothing: its final message is the proposed reading")
            return {}

    sess = ReadingSession(rws, ctx.cfg, model=ctx.s.get("host_session_model"))
    pk = dict(packet, addendum=ctx.addendum, provisions=[])
    sess.run_batch(pk)
    last = sess.last
    ctx.cp.batch(bid)["host_session"] = {"run_id": last.run_id, "elapsed_s": last.elapsed_s, "error": last.error,
                                         "model_reported": last.model_reported, "tool_calls": len(last.tool_calls),
                                         "note": "the session's final message is the proposed reading"}
    ctx.cp.intervention(kind="host session (automatic)", batch=bid, by="tenderpack.ai.hostsession",
                        host_model=sess.host_model_label(), note="a headless host session reading an image; not a person")
    fields = {"run_id": f"{ctx.run_id}-{bid}", "created": now_iso(), "route": "host", "provider": "host-session",
              "model_requested": sess.host_model_label(), "model_reported": ", ".join(last.model_reported or []) or None,
              "task": RR.READING_TASK}
    try:
        prop = RR.parse(controller._extract_json(getattr(last, "final_text", "") or ""), fields, [])
    except (controller.ParseError, RR.RegionError) as e:
        raise BatchFailed(f"the host session's final message is not a reading proposal: {e}"
                          + (f" (session: {last.error})" if last.error else "")) from None
    who = (f"headless host session {last.run_id} ({sess.host_model_label()}; the CLI reported "
           f"{', '.join(last.model_reported or []) or 'no model'})")
    return prop, who


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


def _fit_to_context(ctx: Ctx, batches: list[list[str]]) -> tuple[list[list[str]], list[str]]:
    """For an API route, split a batch the provider's verified context or output cap cannot take (batching.py)."""
    if ctx.s["route"] not in API_ROUTES:
        return batches, []
    try:
        from . import batching
        from .providers import make
        rcfg = C.route(ctx.cfg, ctx.s["route"])
        prov = make(ctx.s["route"], ctx.s.get("model") or C.default_model(rcfg), ctx.cfg, None)
        capsr = prov.capabilities()
        packet = controller.task_packet(ctx.ws, ctx.addendum)
        caps_ = C.caps(ctx.cfg, ctx.s["route"], ctx.remaining_caps())
        ov = batching.overhead_for(packet, controller.SYSTEM, [controller.TOOLS[n].spec() for n in controller.MODEL_TOOLS],
                                   max_output_tokens=caps_.get("max_tokens_per_call"), settings=ctx.cfg.get("batching"))
        entries = {p["unit_id"]: p for p in batching.packet_provisions(packet)}
        out, notes = [], []
        for b in batches:
            for x in batching.plan_batches([entries[p] for p in b if p in entries], capsr, ov):
                out.append(list(x.provisions))
                if not x.fits:
                    notes.append(f"{x.provisions}: {x.note}")
        return out, notes
    except Exception as e:                                       # noqa: BLE001 (the count plan stands; reported)
        return batches, [f"context fit not checked: {type(e).__name__}: {_short(str(e), 300)}"]


def step_analysis(ctx: Ctx, st: dict) -> None:
    cp = ctx.cp
    if not cp.batches("analysis"):
        plan = plan_batches(list(cp.data["provisions"]), int(ctx.s["batch_size"]))
        plan, notes = _fit_to_context(ctx, plan)
        for n, provs in enumerate(plan, 1):
            bid = f"analysis-{n:03d}"
            cp.data["batches"][bid] = {"phase": "analysis", "provisions": provs, "status": "pending", "attempts": 0,
                                       "seconds": 0.0}
            for p in provs:
                cp.provision(p)["batch"] = bid
        st["plan_notes"] = notes
        cp.save()
        ctx.say(f"  {len(cp.data['provisions'])} provisions in {len(plan)} batch(es) of at most {ctx.s['batch_size']}")
    for bid in cp.batches("analysis"):
        b = cp.batch(bid)
        if b["status"] in ("done", "skipped"):
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
        _analysis_batch(ctx, st, bid, todo)
    st["batches"] = {k: cp.batch(k)["status"] for k in cp.batches("analysis")}
    st["provisions"] = dict(Counter(v["status"] for v in cp.data["provisions"].values()))


def _shown(ctx: Ctx, todo: list[str]) -> list[str]:
    """The provisions a batch's task packet shows (controller.task_packet selects by id or prefix)."""
    return [p for p in ctx.cp.data["provisions"] if any(p == x or p.startswith(x) for x in todo)]


def _analysis_batch(ctx: Ctx, st: dict, bid: str, todo: list[str]) -> None:
    cp, s, ws = ctx.cp, ctx.s, ctx.ws
    b = cp.batch(bid)
    b.update(status="running", pid=os.getpid(), attempts=b.get("attempts", 0) + 1, started=now_iso())
    b.pop("error", None)
    cp.save()
    t0 = time.perf_counter()
    try:
        if s["route"] == "host":
            ps = _host_analysis(ctx, st, bid, todo)
        else:
            kw = {}
            if s["route"] == "recorded":
                prov, sess = ctx.cassette.provider("analysis", todo, ctx.used_sessions())
                if prov is None:
                    raise BatchFailed("no recorded session covers this batch (the cassette does not record it)")
                b["session"] = sess
                kw["provider"] = prov
            else:
                kw["model"] = s.get("model")
            ps = controller.propose(ws, ctx.addendum, s["route"], ctx.cfg, caps=ctx.remaining_caps(), provisions=todo,
                                    sleep=ctx.sleep, allow_unverified_capabilities=bool(s.get("allow_unverified_capabilities")),
                                    **kw)
        _take_analysis(ctx, bid, ps, todo)
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
    cp, ws = ctx.cp, ctx.ws
    b = cp.batch(bid)
    hs = _host_auto(ctx)
    packet = (hs.host_packet(ws, ctx.addendum, todo) if hs and hasattr(hs, "host_packet")
              else controller.host_task(ws, ctx.addendum, claim=False, provisions=todo))
    packet["workflow"] = {"run_id": ctx.run_id, "batch": bid, "phase": "analysis", "answer_only": todo,
                          "note": "answer the provisions in answer_only; any other provision in the packet belongs to "
                                  "another batch",
                          "submit_with": f"tenderpack ai submit-batch {ctx.run_id} FILE --by NAME --host-model MODEL"}
    path = ctx.dir / "batches" / f"{bid}.packet.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({k: v for k, v in packet.items() if k != "crops"} | {
        "crops": [{k: v for k, v in c.items() if not k.startswith("_")} for c in packet.get("crops") or []]},
        ensure_ascii=False, indent=1), encoding="utf-8")
    b["packet"] = str(path)
    if hs is not None:
        sess = hs.HostSession(ws, ctx.cfg, model=ctx.s.get("host_session_model"))
        data = sess.run_batch(packet)
        last = getattr(sess, "last", None)
        b["host_session"] = {"run_id": getattr(last, "run_id", None), "elapsed_s": getattr(last, "elapsed_s", None),
                             "error": getattr(last, "error", None), "crops_read": getattr(last, "crops_read", None),
                             "model_reported": getattr(last, "model_reported", None)}
        cp.intervention(kind="host session (automatic)", batch=bid, by="tenderpack.ai.hostsession",
                        host_model=sess.host_model_label() if hasattr(sess, "host_model_label") else None,
                        note="a headless host session over the MCP tools; not a person")
        ps = ProposalSet.model_validate(data)
        if ps.status == "provider_failed":
            raise BatchFailed(f"the host session submitted nothing ({getattr(last, 'error', '')})")
        return ps
    b.update(status="waiting_for_host", waiting_since=now_iso(), waiting_epoch=time.time())
    cp.save()
    st["status"] = "waiting_for_host"
    raise WaitingForHost(_wait_message(ctx, bid))


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

def _answers(ctx: Ctx, cps: ProposalSet, promoted: dict) -> dict[str, dict]:
    """Per provision: whether a promoted op or disposition answers it, and why not."""
    content = {c for o in promoted["sim"]["ops"] if o["valid"] for c in o.get("content") or []}
    ok = ({o.provision for o in promoted["ops"].values()} | {c for o in promoted["ops"].values() for c in o.covers}
          | {d.provision for d in promoted["dispositions"].values()} | content)
    out = {}
    for p, v in ctx.cp.data["provisions"].items():
        mine = [it for it in cps.items if it.provision == p]
        if p in ok:
            out[p] = {"answered": True}
            continue
        esc = [it for it in mine if it.statement_type == "escalation"]
        if esc:
            why = "escalated: " + "; ".join(_short(it.payload.get("why"), 200) for it in esc)
        elif mine:
            why = "; ".join(f"{it.id} {it.verification_status}" + (
                f" ({next((x.check + ': ' + _short(x.detail, 160) for x in it.validation if not x.ok), '')})"
                if it.verification_status not in DS.PROMOTABLE else f" (dropped: {promoted['dropped'].get(it.id, '')})")
                for it in mine)
            why = "not promotable: " + why
        elif v["status"] == "pending":
            b = ctx.cp.data["batches"].get(v.get("batch") or "", {})
            why = f"not analysed: batch {v.get('batch')} {b.get('status')}" + (f" ({b.get('error')})" if b.get("error") else "")
        else:
            why = "no item proposed for it" + (f" ({v.get('reason')})" if v.get("reason") else "")
        out[p] = {"answered": False, "why": why,
                  "needs_person": bool(esc) or any(it.verification_status in ("conflicting", "insufficient_evidence")
                                                   for it in mine)}
    return out


def step_downstream(ctx: Ctx, st: dict) -> None:
    cp, ws = ctx.cp, ctx.ws
    cps, _ = ctx.combined()
    promoted = ctx.promoted()
    answers = _answers(ctx, cps, promoted)
    tasks, imp = DS.tasks(ws, cps, promoted, answers)
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
        n = int(ctx.s["downstream_batch_size"])
        for k in range(0, len(tasks), n):
            bid = f"downstream-{k // n + 1:03d}"
            cp.data["batches"][bid] = {"phase": "downstream", "tasks": [t["id"] for t in tasks[k:k + n]],
                                       "status": "pending", "attempts": 0, "seconds": 0.0}
        cp.data["downstream"]["tasks"] = {t["id"]: {"kind": t["kind"], "batch": next(
            b for b in cp.batches("downstream") if t["id"] in cp.batch(b)["tasks"])} for t in tasks}
        cp.save()
    by_id = {t["id"]: t for t in tasks}
    for bid in cp.batches("downstream"):
        b = cp.batch(bid)
        if b["status"] in ("done", "skipped"):
            continue
        if b["status"] == "waiting_for_host":
            st["status"] = "waiting_for_host"
            raise WaitingForHost(_wait_message(ctx, bid))
        if ctx.stop_batches:
            b.update(status="failed", error=f"not run: {ctx.stop_batches}")
            continue
        _downstream_batch(ctx, st, bid, [by_id[t] for t in b["tasks"] if t in by_id], promoted, len(tasks))
    st.update(tasks=len(tasks), by_kind=dict(Counter(t["kind"] for t in tasks)),
              batches={k: cp.batch(k)["status"] for k in cp.batches("downstream")})
    ctx.say(f"  downstream: {len(tasks)} task(s) {dict(Counter(t['kind'] for t in tasks))}")


def _downstream_batch(ctx: Ctx, st: dict, bid: str, batch: list[dict], promoted: dict, total: int) -> None:
    cp, s, ws = ctx.cp, ctx.s, ctx.ws
    b = cp.batch(bid)
    b.update(status="running", pid=os.getpid(), attempts=b.get("attempts", 0) + 1, started=now_iso())
    b.pop("error", None)
    cp.save()
    t0 = time.perf_counter()
    try:
        res_path = ctx.dir / "batches" / f"{bid}.result.json"
        packet = DS.packet(ws, ctx.addendum, batch, promoted, total, ws.identity().model_dump())
        if s["route"] == "host":
            packet["system"] = DS.SYSTEM
            packet["workflow"] = {"run_id": ctx.run_id, "batch": bid, "phase": "downstream",
                                  "submit_with": f"tenderpack ai submit-batch {ctx.run_id} FILE --by NAME --host-model MODEL"}
            path = ctx.dir / "batches" / f"{bid}.packet.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(packet, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
            b["packet"] = str(path)
            hs = _host_auto(ctx)
            if hs is None:
                b.update(status="waiting_for_host", waiting_since=now_iso(), waiting_epoch=time.time())
                cp.save()
                st["status"] = "waiting_for_host"
                raise WaitingForHost(_wait_message(ctx, bid))
            ds = _downstream_host_session(ctx, hs, bid, packet)
        else:
            if s["route"] == "recorded":
                prov, sess = ctx.cassette.provider("downstream", [t["id"] for t in batch], ctx.used_sessions())
                if prov is None:
                    raise BatchFailed("no recorded session covers this batch (the cassette does not record it)")
                b["session"] = sess
            else:
                from .providers import make
                rcfg = C.route(ctx.cfg, s["route"])
                prov = make(s["route"], s.get("model") or C.default_model(rcfg), ctx.cfg, None)
            ds = _converse(ctx, prov, packet, bid)
        _take_downstream(ctx, bid, ds, res_path)
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


def _converse(ctx: Ctx, prov, packet: dict, bid: str, system: str | None = None, parse=None, task: str = DOWNSTREAM_TASK,
              tool_names: list[str] | None = None, ws=None):
    """One downstream (or reading) batch with a provider (recorded or an API route): the controller's turn loop with
    the tools, the caps of the run, bounded retries and one retry of a malformed answer; logged like a controller run.
    `parse(data, fields, overwrites)` makes the answer (default: a DownstreamSet); `tool_names` the tools offered
    (default: the proposer's MODEL_TOOLS); `ws` the workspace the tools read (default: the candidate's)."""
    system = system or DS.SYSTEM
    parse = parse or DS.parse
    tool_names = tool_names or list(controller.MODEL_TOOLS)
    from .providers.base import ProviderError, Request
    from .providers.base import complete_with_retries as _retry
    from .providers.recorded import PACKET_MARK
    s, ws = ctx.s, (ws or ctx.ws)
    route = s["route"]
    caps_ = C.caps(ctx.cfg, route, ctx.remaining_caps())
    price = B.price_for(ctx.cfg, prov.model) if route != "recorded" else None
    B.check_startable(route, C.route(ctx.cfg, route), caps_, price)
    run_id = B.check_run_id(f"{ctx.run_id}-{bid}")
    staging = B.safe_staging(ws.staging, ws.root, ws.evidence)
    log = RunLog(run_id, [staging / run_id / "log.jsonl", Path(s["worklog"]) / f"{run_id}.jsonl"])
    log.event("start", route=route, provider=prov.name, model_requested=prov.model, task=task, batch=bid,
              caps=caps_, cassette=getattr(prov, "cassette_path", None))
    try:
        capsr = prov.capabilities()
    except ProviderError as e:
        log.event("refused", reason=e.message)
        raise BatchFailed(f"capability check failed: {e.message}") from None
    text = PACKET_MARK + json.dumps(packet, ensure_ascii=False, default=str)
    est = int(len(text) / 3.5)
    budget = B.Budget(caps_, price)
    problems = []
    if capsr.tools is not True:
        problems.append(f"the task needs tool use and {prov.name} {prov.model} does not report it ({capsr.source})")
    if capsr.context_tokens and est + budget.max_tokens() > capsr.context_tokens:
        problems.append(f"the packet is about {est} tokens; with {budget.max_tokens()} output tokens it does not fit "
                        f"the context bound of {capsr.context_tokens} (use a smaller --downstream-batch-size)")
    if problems:
        log.event("refused", reason="; ".join(problems))
        raise BatchFailed("; ".join(problems))
    log.event("prompt", system=system, packet=packet, packet_tokens_estimate=est)
    messages = [{"role": "user", "content": [{"type": "text", "text": text}]}]
    tools_spec = [controller.TOOLS[n].spec() for n in tool_names]
    maxchars = int(caps_.get("max_tool_result_chars") or 20000)
    ds, status, retry_used, model_reported = None, None, False, None
    created = now_iso()

    def on_error(attempt, err):
        log.event("provider_error", attempt=attempt, kind=err.kind, retryable=err.retryable, message=_short(err.message, 400))
    try:
        while True:
            budget.next_turn()
            req = Request(system=system, messages=messages, tools=tools_spec, max_tokens=budget.max_tokens(),
                          timeout_s=budget.call_timeout())
            resp = _retry(prov, req, retries=int(caps_.get("retries") or 0), backoff_s=float(caps_.get("backoff_s") or 0),
                          sleep=ctx.sleep, before_attempt=budget.before_call, on_error=on_error)
            model_reported = resp.model_reported or model_reported
            usd0 = budget.cost_usd()[0]
            log.event("response", turn=budget.turns, text=resp.text, stop_reason=resp.stop_reason, usage=resp.usage,
                      tool_calls=[{"id": c.id, "name": c.name, "arguments": c.arguments} for c in resp.tool_calls])
            try:
                budget.after_call(resp.usage.get("input_tokens", 0), resp.usage.get("output_tokens", 0))
            finally:
                usd1, basis = budget.cost_usd()
                B.record_spend(staging, {"ts": now_iso(), "run_id": run_id, "route": route, "provider": prov.name,
                                         "model_requested": prov.model, "model_reported": resp.model_reported,
                                         "input_tokens": resp.usage.get("input_tokens", 0),
                                         "output_tokens": resp.usage.get("output_tokens", 0),
                                         "cost_usd": None if usd1 is None else round(usd1 - (usd0 or 0), 6),
                                         "cost_basis": basis})
            messages.append({"role": "assistant", "content": [{"type": "text", "text": resp.text}] if resp.text else [],
                             "tool_calls": [{"id": c.id, "name": c.name, "arguments": c.arguments} for c in resp.tool_calls],
                             "provider_raw": resp.provider_raw})
            if resp.tool_calls:
                messages.append({"role": "tool", "results": [_run_tool(ws, c, log, capsr.images is True, maxchars, tool_names)
                                                             for c in resp.tool_calls]})
                continue
            fields = {"run_id": run_id, "created": created, "route": route, "provider": prov.name,
                      "model_requested": prov.model, "model_reported": model_reported, "task": task}
            ow: list = []
            try:
                ds = parse(controller._extract_json(resp.text), fields, ow)
                if ow:
                    log.event("overwrites", overwrites=ow)
                break
            except (controller.ParseError, DS.DownstreamParseError, RR.RegionError) as e:
                log.event("parse_error", error=str(e), retry_used=retry_used)
                if retry_used:
                    status = "malformed"
                    break
                retry_used = True
                messages.append({"role": "user", "content": [{"type": "text", "text":
                                 f"Your answer could not be parsed: {e}\nReply again with ONLY the JSON object described "
                                 "by `schema` in the packet."}]})
    except B.BudgetExhausted as e:
        status = "budget_exhausted"
        log.event("budget_exhausted", reason=str(e))
    except ProviderError as e:
        status = "provider_failed"
        log.event("provider_failed", kind=e.kind, message=_short(e.message, 400))
    usd, _ = budget.cost_usd()
    ctx.cp.add_usage(budget.calls, budget.input_tokens, budget.output_tokens, usd)
    _mirror_spend(ctx)
    log.event("end", status=status or "parsed", items=len(getattr(ds, "items", [None])) if ds else 0, calls=budget.calls)
    if ds is None:
        if status == "budget_exhausted":
            ctx.stop_batches = "the run's budget is exhausted"
        raise BatchFailed(f"the {'downstream set' if task == DOWNSTREAM_TASK else 'answer'} is {status}")
    return ds


def _run_tool(ws, call, log: RunLog, images_ok: bool, maxchars: int, allowed: list[str]) -> dict:
    """A tool call of a workflow batch: only the tools offered; arguments are data; get_crop and get_region attach their
    images when the provider takes images (as controller._model_tool does for get_crop)."""
    from .tools import ToolError, call_tool
    from .runlog import truncate
    images: list[dict] = []
    try:
        if call.name not in allowed:
            raise ToolError(f"no tool {call.name!r} is available here; tools: {allowed}")
        res = call_tool(ws, call.name, call.arguments, caller="controller")
        content, err = json.dumps(res, ensure_ascii=False, default=str), False
        if call.name in ("get_crop", "get_region"):
            if images_ok:
                images = [{"type": "image", "path": c["path"], "sha256": c["sha256"], "media_type": c["media_type"]}
                          for c in (res.get("crops") or [])[:3]]
            else:
                content = json.dumps({**res, "note": "images not attached: the model does not report image input"},
                                     ensure_ascii=False, default=str)
    except (ToolError, B.Refused) as e:
        content, err = json.dumps({"error": str(e)}, ensure_ascii=False), True
    except Exception as e:                                       # noqa: BLE001 (a tool bug goes to the log and the model)
        content, err = json.dumps({"error": f"{type(e).__name__}: {_short(str(e), 300)}"}), True
    log.event("tool_call", id=call.id, name=call.name, arguments=call.arguments, ok=not err,
              result=truncate(content, 4000), images=[i["sha256"] for i in images])
    return {"tool_call_id": call.id, "name": call.name, "content": truncate(content, maxchars), "is_error": err,
            "images": images}


def _downstream_host_session(ctx: Ctx, hs, bid: str, packet: dict) -> DownstreamSet:
    """A downstream batch in a headless host session (hostsession.HostSession with the downstream rules): the host
    reads with the MCP tools and replies with the DownstreamSet as its final message (it submits nothing)."""
    from .providers.recorded import PACKET_MARK

    class DownstreamSession(hs.HostSession):
        def system_prompt(self):
            return DS.SYSTEM + ("\nHost session rules: you work ONLY through the tenderpack MCP tools (read-only use); the "
                                "packet is below; do not call get_task_packet, request_review or submit_proposals. Your "
                                "final message is ONLY the JSON object described by `schema`.")

        def command(self, mcp_path):
            cmd = super().command(mcp_path)
            if "--disallowedTools" in cmd:
                i = cmd.index("--disallowedTools")
                cmd[i + 1] += "," + hs.TOOL_PREFIX + "submit_proposals"
            return cmd

        def prompt(self, pk):
            return PACKET_MARK + json.dumps({k: v for k, v in pk.items() if k != "system"}, ensure_ascii=False, default=str)

    sess = DownstreamSession(ctx.ws, ctx.cfg, model=ctx.s.get("host_session_model"))
    sess.run_batch(packet)
    last = sess.last
    ctx.cp.batch(bid)["host_session"] = {"run_id": last.run_id, "elapsed_s": last.elapsed_s, "error": last.error,
                                         "model_reported": last.model_reported,
                                         "note": "a downstream session submits nothing: its final message is the set"}
    ctx.cp.intervention(kind="host session (automatic)", batch=bid, by="tenderpack.ai.hostsession",
                        host_model=sess.host_model_label(), note="a headless host session; not a person")
    fields = {"run_id": f"{ctx.run_id}-{bid}", "created": now_iso(), "route": "host", "provider": "host-session",
              "model_requested": sess.host_model_label(), "model_reported": ", ".join(last.model_reported or []) or None,
              "task": DOWNSTREAM_TASK}
    try:
        return DS.parse(controller._extract_json(getattr(last, "final_text", "") or ""), fields, [])
    except (controller.ParseError, DS.DownstreamParseError) as e:
        raise BatchFailed(f"the host session's final message is not a DownstreamSet: {e}") from None


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
    report = DS.validate(ctx.ws, ds, promoted, {t["id"] for t in tasks})
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


# ---------------------------------------------------------------------------------------------- step: promotion

def step_promotion(ctx: Ctx, st: dict) -> None:
    snap = ctx.P["pre_promotion"]
    if snap.exists():
        DS._snapshot(snap.parent, snap)                          # back to the candidate as it was before promotion
    cps, _ = ctx.combined()
    promoted = ctx.promoted(fresh=True)
    ds, _ = _load_downstream(ctx)
    answers = _answers(ctx, cps, promoted)
    origin = (f"AI workflow run {ctx.run_id} (route {ctx.s['route']}, model {cps.model_requested}"
              + (f", reported {cps.model_reported}" if cps.model_reported else "") + "); PROPOSED; not reviewed")
    summ = DS.promote(ctx.ws, ctx.cp.data["candidate"], ctx.run_id, cps, promoted, ds, origin,
                      {p: a["why"] for p, a in answers.items() if not a["answered"]})
    (ctx.dir / "promotion.json").write_text(json.dumps(summ, ensure_ascii=False, indent=1), encoding="utf-8")
    st.update({k: v for k, v in summ.items() if k != "written"})
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
    ctx.say(f"  check-register: exit {code}, {len(found)} finding(s) {dict(Counter(k for k, _, _ in found))}")


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
    ctx.say(f"  candidate outputs published to {out} (exit 0; {len(marked)} file(s) carry the banner)")


def _row_statuses(ctx: Ctx, r: dict) -> tuple[dict, str, list]:
    add = ctx.addendum
    prom = json.loads((ctx.dir / "promotion.json").read_text(encoding="utf-8")) if (ctx.dir / "promotion.json").exists() else {}
    ds, _ = _load_downstream(ctx)
    vstat = {}
    for it in (ds.items if ds else []):
        if it.statement_type == "row_new":
            vstat[(it.payload.get("row") or {}).get("id")] = it.verification_status
        elif it.statement_type == "row_reading":
            vstat[it.payload.get("row")] = it.verification_status
    new, readings = set(prom.get("rows_new") or []), set(prom.get("readings") or [])
    answers = json.loads((ctx.dir / "downstream" / "answers.json").read_text(encoding="utf-8")) \
        if (ctx.dir / "downstream" / "answers.json").exists() else {}
    scope_rows = set()
    ws = ctx.ws
    for p, a in answers.items():
        if not a.get("answered"):
            u = ws.units_by_id.get(p) or {}
            pst = ws.stage(ws.prev_stage(add)).state
            from ..citations import citations, resolve
            t = set(resolve(citations(u.get("text") or ""), set(pst)))
            scope_rows |= {e["row"].id for e in r["evals"] if any(x in t or any(x.startswith(y + "/") for y in t)
                                                                   for x in e["row"].units)}
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
        elif rid in scope_rows:
            out[rid] = f"UNRESOLVED: cites a unit an unresolved provision of {add} names"
        elif rv.get("status") == "changed":
            out[rid] = "DECIDED BEFORE, CHANGED SINCE: review again"
    default = "proposed (existing row; not changed by this run; not reviewed)"
    cnt = Counter(out.get(e["row"].id, default).split(":")[0].split(" (")[0] for e in r["evals"])
    legend = [{"status": "PROPOSED BY THE AI WORKFLOW", "rows": cnt.get("PROPOSED BY THE AI WORKFLOW", 0),
               "meaning": f"a new row or a reading re-made at {add} by this run, validated by the controller; a person "
                          "decides it (accept / reject)"},
              {"status": "UNRESOLVED", "rows": cnt.get("UNRESOLVED", 0),
               "meaning": f"STALE at {add} with no re-made reading, or citing a unit an unresolved provision names"},
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
    rd = ctx.dir / "review"
    rd.mkdir(parents=True, exist_ok=True)
    (rd / "diff.md").write_text(f"> **{CAND.BANNER}**\n\n" + md, encoding="utf-8")
    (rd / "diff.json").write_text(json.dumps(data, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    cmp_ = _compare_outputs(ctx.P["out_before"], ctx.P["out"], ctx.addendum)
    (rd / "outputs-before-after.json").write_text(json.dumps(cmp_, ensure_ascii=False, indent=1), encoding="utf-8")
    req = data.get("requirements") or {}
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
    answers = js(ctx.dir / "downstream" / "answers.json")
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
         "- status **{}**".format(*(_final_status(cp)[:1])) + (": " + _final_status(cp)[1] if _final_status(cp)[1] else ""),
         f"- usage: {d['usage']['calls']} call(s), {d['usage']['input_tokens']} input / {d['usage']['output_tokens']} output "
         f"tokens; cost {d['usage']['cost_usd'] if d['usage']['cost_usd'] is not None else 'not computed'}", ""]
    # ---- what is candidate and what is real
    L += ["## What is candidate and what is real", "",
          f"- **Candidate** (proposed by this run, nothing accepted): `{_rel(ctx.P['dir'], rd)}/` — a copy of the curation and "
          f"configuration with {add} added, its evidence build, its op file, rows, issues, templates and outputs.",
          "- **Last validated state**: " + (f"`{_rel(ctx.P['out_before'], rd)}/` (the pre-addendum outputs built from the "
                                             f"copied curation and the previous evidence build; {ob.get('status')}"
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
              f"state ({diff.get('from')}); {add} as proposed is in A1's `Status after {add}` column, in A2, in "
              f"`a5/working/{add}.json` and in the diff below.", ""]
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
    L += ["## First: unresolved provisions and escalations", "",
          f"{len(unres)} of {len(d['provisions'])} provisions are not answered by a promoted item (each is `unresolved` in "
          f"the candidate op file with the reason); {len(esc)} escalation(s).", ""]
    for it in esc:
        sc = ((tasks.get(f"esc:{it.provision}") or {}).get("scope")) or _scope(ctx, it.provision)
        L += [f"- **ESCALATED {it.id}** ({it.provision}): {_short(it.payload.get('why'), 300)}",
              f"  - unsupported: {_short(it.payload.get('what_is_unsupported'), 300)}",
              "  - evidence: " + ("; ".join(f"{x.unit_id} p{x.page}: “{_short(x.words, 160)}”" for x in it.evidence) or "none"),
              f"  - affected scope: units {', '.join(sc.get('units', [])[:12]) or 'none'}; rows {', '.join(sc.get('rows', [])[:12]) or 'none'}; "
              f"activities {', '.join(sc.get('activities', [])[:12]) or 'none'}; clarifications "
              f"{', '.join(map(str, sc.get('clarifications', [])[:8])) or 'none'}"]
    for p in unres:
        if any(it.provision == p for it in esc):
            continue
        v = d["provisions"].get(p, {})
        L.append(f"- **UNRESOLVED {p}** ({v.get('kind')}, p{','.join(map(str, v.get('pages') or []))}): {answers[p].get('why')}")
    L.append("")
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
                 + ("answered" if (answers.get(p) or {}).get("answered") else "UNRESOLVED"))
        L.append(f"- source: “{_short(u.get('text'), 360)}”")
        if not mine:
            via = v.get("accounted_by")
            L.append("- transition: " + (f"content of {', '.join(via)}" if via else
                                         f"none ({(answers.get(p) or {}).get('why', v.get('status'))})"))
        changed_units, rows_hit = [], set()
        for it in mine:
            bad = next((x for x in it.validation if not x.ok), None)
            L.append(f"- transition: `{it.id}` {it.statement_type} {_transition(it)}")
            L.append(f"  - validation: **{it.verification_status}**" + (f" — {bad.check}: {_short(bad.detail, 220)}" if bad else ""))
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
            L.append(f"  - downstream proposal `{it.id}` {it.statement_type} ({it.task}): **{it.verification_status}**"
                     + (f" — held back: {dreport.get('held_back', {}).get(it.id)}" if dreport.get("held_back", {}).get(it.id) else ""))
        rows_all = rows_hit | {(it.payload.get("row") or {}).get("id") if it.statement_type == "row_new" else it.payload.get("row")
                               for it in dits if it.statement_type in ("row_new", "row_reading")} - {None}
        od = [f"NEW {x}" for x in req.get("new") or [] if x in rows_all] + \
             [f"OUT {x}" for x in req.get("out") or [] if x in rows_all] + \
             [f"CHANGED {x}" for x in req.get("changed") or [] if x in rows_all] + \
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
            note = next((x.detail for x in it.validation if x.ok and x.check in ("interpretation", "duration", "relationship")), "")
            L.append(f"| {it.id} | {it.statement_type} | {it.task} | {it.verification_status} | "
                     f"{_short((bad.check + ': ' + bad.detail) if bad else note, 200).replace('|', '/')} |")
        L.append("")
        if dreport.get("schedule_problems") or dreport.get("interactions"):
            L += ["- interactions: " + "; ".join(_short(x, 200) for x in (dreport.get("interactions") or [])[:10])
                  if dreport.get("interactions") else "- interactions: none",
                  "- A5 problems the proposals would add: " + ("; ".join(_short(x, 200) for x in dreport.get("schedule_problems")[:10])
                                                              if dreport.get("schedule_problems") else "none"), ""]
    elif tasks:
        L += ["## Downstream proposals", "", f"- {len(tasks)} task(s); no downstream set was produced "
              "(batches: " + ", ".join(k + " " + cp.batch(k)["status"] for k in cp.batches("downstream")) + ")", ""]
    # ---- promotion
    if prom:
        L += ["## Promoted into the candidate (PROPOSED; nothing accepted)", ""]
        for k in ("ops", "dispositions", "rows_new", "readings", "issues", "evidence_items", "activities", "lead_times",
                  "clarifications", "relationships"):
            if prom.get(k):
                L.append(f"- {k.replace('_', ' ')}: {', '.join(map(str, prom[k][:40]))}" + (f" (+{len(prom[k]) - 40})" if len(prom[k]) > 40 else ""))
        L += [f"- unresolved provisions: {len(prom.get('unresolved') or [])}"] + [f"- note: {x}" for x in prom.get("notes") or []] + [""]
        dropped = pops.get("dropped") or {}
        if dropped:
            L += ["- left out of the promoted ops: " + "; ".join(f"{k}: {_short(v, 160)}" for k, v in dropped.items()), ""]
    # ---- checks
    cr = cp.step("check_register")
    if cr.get("status") == "done":
        L += ["## check-register on the candidate", "", f"- exit {cr.get('exit_code')}; {cr.get('findings')} finding(s) "
              f"{cr.get('by_kind')}"] + [f"  - {x}" for x in (cr.get("first") or [])[:25]] + [""]
    # ---- coverage
    cov = (cps.coverage.model_dump() if cps else {})
    L += ["## Coverage", "", f"- provisions: {len(d['provisions'])}; accounted for by the combined set: {cov.get('accounted')}; "
          f"states {dict(Counter(v['status'] for v in d['provisions'].values()))}"]
    res = cp.step("validation").get("resolution")
    if res:
        L.append(f"- resolution (controller): resolved {res.get('resolved')}, pending {res.get('pending')}, invalid "
                 f"{res.get('invalid')}, unaccounted {res.get('unaccounted')}; approved {res.get('approved')}")
    L.append(f"- structural units of {add} that are not provisions (listed so nothing is dropped): "
             + ", ".join(f"{x['unit_id']} ({x['kind']})" for x in d.get("structure") or []))
    L += ["- batches: " + ", ".join(f"{k} {b['status']}" + (f" ({_short(b.get('error'), 80)})" if b.get("error") else "")
                                     for k, b in d["batches"].items()), ""]
    # ---- interventions
    L += ["## Manual interventions (and automatic host sessions, named as such: not a person)", ""]
    L += [f"- {x['ts']}: {x.get('kind')} — batch {x.get('batch')} by {x.get('by')}"
          + (f"; host model {x.get('host_model')}" if x.get("host_model") else "")
          + (f"; file {x.get('file')} (sha256 {str(x.get('sha256'))[:16]}…)" if x.get("file") else "")
          + (f"; {x.get('note')}" if x.get("note") else "") for x in d.get("interventions") or []] or ["- none"]
    L.append("")
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
              "promotion": step_promotion, "pin": step_pin, "check_register": step_check_register,
              "outputs": step_outputs, "diff": step_diff, "review": step_review}


# ---------------------------------------------------------------------------------------------- submit-batch

def submit_batch(run_id: str, file, by: str, host_model: str | None = None, batch: str | None = None, staging=None,
                 cont: bool = True, echo=print, sleep=time.sleep) -> dict:
    """The manual host path: a host (a coding assistant without MCP, or a person) answered a batch's task packet with
    a proposal set (analysis) or a downstream set (downstream). The set is validated exactly as an API run's, the
    submission is recorded (who, when, the file and its sha256, the declared host model), and the run continues."""
    if not (by or "").strip():
        raise B.Refused("--by must name who submits the batch (a person, or the host session); it is recorded")
    cp = load(run_id, staging)
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
        return resume(run_id, staging, retry_failed=False, echo=echo, sleep=sleep)
    return summary(cp)
