"""ONE request path for the AI phases (session 11): the analysis (a ProposalSet), the reading of an image region (a
RegionReadingProposal), the downstream phase (a DownstreamSet) and the selective critic (a batch of reviews) go through
the same safeguards on every route (recorded, anthropic, openrouter, ollama: the provider turn loop; host: a headless
`claude -p` session through hostsession.py; the manual host path: `submit-batch`).

    spec(phase)                     TaskSpec: the task, the system prompt, the answer's JSON SCHEMA (sent natively
                                    through providers/structured.py where the provider supports it; in the packet on
                                    every route), the strict local parser (pydantic), the tools, the modalities
    require(spec, caps, images)     the capability check BEFORE any call: tool use where tools are offered; image input
                                    where images are attached, and ALWAYS for the reading phase (a reading made
                                    without seeing the image is refused, never degraded to text). A capability the
                                    route could not verify is visible: capabilities used under
                                    --allow-unverified-capabilities, and the host's declared ones, carry a route notice
                                    (run log, checkpoint, review packet)
    size(...)                       complete request accounting (batching.request_size): system + tool definitions +
                                    the packet as sent + the images + the later-turn allowance + the expected output,
                                    against the context window and the output cap. A request that does not fit is NEVER
                                    truncated: TooLarge carries the sizes; the workflow splits the batch by provision
                                    or task, and escalates a single provision or task that does not fit alone
    call_provider / call_host       the failure classes (FailurePolicy, config/ai.yaml `failures`):
                                      rate_limit  HTTP 429, a provider's rate-limit error, the host CLI's session/usage
                                                  limit: bounded exponential backoff with jitter (30, 60, 120, 240 s by
                                                  default, `max_tries`), a reset time the host names honoured when it
                                                  is near; then RateLimited -> the workflow DEFERS the batch (not
                                                  failed) and stops cleanly (or continues: `on_deferred`)
                                      provider    5xx, 529, timeouts, connection errors, a host CLI that cannot start or
                                                  ends without a result: bounded retries, then ProviderFailed (failed)
                                      malformed   an answer that does not parse or fails the schema or a reference:
                                                  ONE bounded re-ask carrying the validation errors; an item that still
                                                  fails its SCHEMA after it is set aside ITEM BY ITEM (the batch keeps
                                                  the rest); an item whose only problem is a reference is kept and rated
                                                  by the controller (unknown statement -> insufficient_evidence); an
                                                  answer that is not a set at all is Malformed
    converse(...)                   the provider turn loop for every phase (tools, images, caps, per-turn context bound,
                                    usage and spend, the repair turn); ask_host(...) the same for a host answer session
    check(spec, data, packet)       the local checks of an answer: the envelope, every item against its model, and the
                                    references (an item's `statements` are ids of the set's statements, never free
                                    text; a downstream item answers a task of its packet; a review names a requested
                                    item)
Nothing here assigns a verification status: the controller (analysis), downstream.validate, regionread.validate and
the critic's guard do, exactly as before.

Session 12: compact_shared(packet) sends the shared part of a packet smaller (tool names only, schema titles dropped,
$defs printed once); RateGate is the run's shared rate-limit pause when batches run at once (call_provider and
call_host wait for it before each call and pause it on a 429); in offline mode host_repair refuses before any process
(tenderpack/ai/offline.py).
"""
from __future__ import annotations

import json
import random
import socket
import threading
import time
import urllib.error
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path
from typing import Callable

from . import budget as B
from . import config as C
from .runlog import RunLog, truncate

PHASES = ("analysis", "reading", "downstream", "critic")
FAILURE_CLASSES = ("rate_limit", "provider", "malformed")
PACKET_NOTE = ("The packet is sent ONCE per session: the state identity, the rules, the schema and the shared targets "
               "are not repeated per item.")


def _short(t, n: int = 300) -> str:
    t = " ".join(str(t or "").split())
    return t if len(t) <= n else t[: n - 1] + "…"


# ---------------------------------------------------------------------------------------------- errors

class CapabilityRefused(B.Refused):
    """The route cannot do the phase (no tool use, no image input, no known context window): refused before any call."""


class TooLarge(B.Refused):
    """The request does not fit the context window or the output cap (see `size`); never truncated."""

    def __init__(self, message: str, size=None):
        super().__init__(message)
        self.size = size


class RateLimited(Exception):
    """A rate limit outlasted the bounded backoff: the batch is deferred (resumable), not failed."""

    def __init__(self, message: str, attempts: list | None = None, reset_in_s: float | None = None):
        super().__init__(message)
        self.message, self.attempts, self.reset_in_s = message, list(attempts or []), reset_in_s
        self.outcome = None


class ProviderFailed(Exception):
    def __init__(self, message: str, attempts: list | None = None):
        super().__init__(message)
        self.message, self.attempts = message, list(attempts or [])
        self.outcome = None


class Malformed(Exception):
    """The answer is not a usable set even after the bounded repair."""

    def __init__(self, message: str, errors: list | None = None):
        super().__init__(message)
        self.message, self.errors = message, list(errors or [])
        self.outcome = None


class ContextExhausted(Exception):
    """The conversation outgrew the context window during the turns (the later-turn allowance was too small)."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.outcome = None


# ---------------------------------------------------------------------------------------------- the task per phase

@dataclass
class TaskSpec:
    phase: str
    task: str
    system: str
    schema: dict
    parse: Callable
    tools: tuple = ()
    needs_images: bool = False
    item_model: type | None = None
    items_field: str | None = "items"
    item_key: str = "provision"
    parse_errors: tuple = (Exception,)


def spec(phase: str, system: str | None = None, parse: Callable | None = None, tools: list | None = None) -> TaskSpec:
    """The task of a phase (see the module docstring). `system`, `parse` and `tools` override the phase's own."""
    from pydantic import ValidationError
    if phase == "analysis":
        from . import controller
        from .contract import ChangeProposal
        from .providers import structured as SO
        s = TaskSpec("analysis", controller.TASK, controller.SYSTEM, SO.proposal_schema(), controller.parse_set,
                     tuple(controller.MODEL_TOOLS), False, ChangeProposal, "items", "provision",
                     (controller.ParseError, ValidationError))
    elif phase == "downstream":
        from . import controller
        from . import downstream as DS
        from .contract import DOWNSTREAM_TASK, DownstreamItem, downstream_fill_schema
        s = TaskSpec("downstream", DOWNSTREAM_TASK, DS.SYSTEM, downstream_fill_schema(), DS.parse,
                     tuple(controller.MODEL_TOOLS), False, DownstreamItem, "items", "task",
                     (DS.DownstreamParseError, controller.ParseError, ValidationError))
    elif phase == "reading":
        from . import controller
        from . import regionread as RR
        from .contract import READING_TASK
        s = TaskSpec("reading", READING_TASK, RR.SYSTEM, RR.answer_schema(), RR.parse, ("get_region", "validate_reading"),
                     True, None, None, "region_id", (RR.RegionError, controller.ParseError, ValidationError))
    elif phase == "critic":
        from . import critic as CR
        s = TaskSpec("critic", CR.CRITIC_TASK, CR.CRITIC_BATCH_SYSTEM, CR.CRITIC_BATCH_SCHEMA, CR.parse_batch, (), False,
                     CR.ReviewEntry, "reviews", "item", (CR.CriticError, ValidationError))
    else:
        raise ValueError(f"no phase {phase!r} ({', '.join(PHASES)})")
    if system is not None:
        s.system = system
    if parse is not None:
        s.parse = parse
    if tools is not None:
        s.tools = tuple(tools)
    return s


def phase_of_task(task: str) -> str:
    from .contract import DOWNSTREAM_TASK, READING_TASK
    return {DOWNSTREAM_TASK: "downstream", READING_TASK: "reading"}.get(task, "analysis")


# ---------------------------------------------------------------------------------------------- the failure policy

@dataclass
class FailurePolicy:
    backoff_s: tuple = (30.0, 60.0, 120.0, 240.0)
    jitter: float = 0.2
    max_tries: int = 4
    honour_reset_up_to_s: float = 300.0
    on_deferred: str = "stop"
    provider_retries: int = 2
    provider_backoff_s: float = 2.0
    host_retries: int = 1
    repairs: int = 1
    after_deferral: bool = False          # a batch was deferred in this drive: one try, then defer (no backoff)
    gate: object = None                   # session 12: the run's shared RateGate when batches run at once

    @classmethod
    def from_cfg(cls, cfg: dict | None, caps: dict | None = None) -> "FailurePolicy":
        f = (cfg or {}).get("failures") or {}
        rl, pv, mf = f.get("rate_limit") or {}, f.get("provider") or {}, f.get("malformed") or {}
        caps = caps or {}
        p = cls()
        if rl.get("backoff_s") is not None:
            p.backoff_s = tuple(float(x) for x in rl["backoff_s"]) or p.backoff_s
        p.jitter = float(rl.get("jitter", p.jitter))
        p.max_tries = int(rl.get("max_tries", len(p.backoff_s)))
        p.honour_reset_up_to_s = float(rl.get("honour_reset_up_to_s", p.honour_reset_up_to_s))
        p.on_deferred = str(rl.get("on_deferred", p.on_deferred))
        if p.on_deferred not in ("stop", "continue"):
            raise C.ConfigError(f"failures.rate_limit.on_deferred must be stop or continue, not {p.on_deferred!r}")
        p.provider_retries = int(pv.get("retries", caps.get("retries", p.provider_retries)))
        p.provider_backoff_s = float(pv.get("backoff_s", caps.get("backoff_s", p.provider_backoff_s)))
        p.host_retries = int(pv.get("host_retries", p.host_retries))
        p.repairs = int(mf.get("repairs", p.repairs))
        if p.repairs > 1:
            raise C.ConfigError("failures.malformed.repairs is bounded at 1 (one re-ask carrying the errors)")
        return p

    def rate_wait(self, attempt: int, rng: random.Random, hint: float | None = None) -> float:
        base = float(self.backoff_s[min(attempt, len(self.backoff_s) - 1)])
        wait = base * (1.0 + rng.uniform(-self.jitter, self.jitter))
        if hint is not None and hint > wait:
            wait = float(hint) + rng.uniform(0, max(1.0, base * self.jitter))
        return round(wait, 1)

    def to_dict(self) -> dict:
        return {f.name: getattr(self, f.name) for f in fields(self) if f.name != "gate"} | (
            {"gate": "shared by the run's workers"} if self.gate is not None else {})


class RateGate:
    """Session 12: ONE rate-limit pause shared by every worker of a run whose batches run at once
    (concurrency.max_parallel_sessions > 1). A rate-limited call pauses the gate for its backoff (or the reset the
    provider names); every worker waits for the gate before its next call, so one 429 pauses all of them until the
    wait is over (more sessions never lift a plan's limit; they reach it sooner). Thread-safe; records its pauses."""

    def __init__(self, clock=time.monotonic):
        self.clock, self.until, self.pauses, self.waits = clock, 0.0, 0, []
        self._lock = threading.Lock()

    def pause(self, seconds: float) -> None:
        with self._lock:
            self.until = max(self.until, self.clock() + max(0.0, float(seconds or 0)))
            self.pauses += 1

    def wait(self, sleep) -> float:
        with self._lock:
            rem = self.until - self.clock()
        if rem > 0:
            self.waits.append(round(rem, 1))
            sleep(rem)
            return rem
        return 0.0

    def record(self) -> dict:
        return {"pauses": self.pauses, "waits": len(self.waits), "longest_wait_s": max(self.waits, default=0.0)}


def _gate_wait(policy: "FailurePolicy", sleep) -> None:
    if getattr(policy, "gate", None) is not None:
        policy.gate.wait(sleep)


def _gate_pause(policy: "FailurePolicy", seconds) -> None:
    if getattr(policy, "gate", None) is not None:
        policy.gate.pause(seconds)


def classify(err) -> str:
    """rate_limit | provider (see the module docstring) for a providers.base.ProviderError."""
    from .hostsession import RATE_LIMIT_RE
    status = getattr(err, "status", None)
    kind = str(getattr(err, "kind", ""))
    msg = str(getattr(err, "message", err))
    if status == 429 or kind in ("http_429", "rate_limited", "rate_limit") or kind.startswith("api_error_429") \
            or (status in (None, 429) and RATE_LIMIT_RE.search(msg) and "schema" not in msg.lower()):
        return "rate_limit"
    return "provider"


def _attempt(cls: str, err, wait: float | None, n: int) -> dict:
    return {"class": cls, "kind": getattr(err, "kind", type(err).__name__), "status": getattr(err, "status", None),
            "message": _short(getattr(err, "message", str(err)), 400), "wait_s": wait, "attempt": n}


def call_provider(prov, req, policy: FailurePolicy, *, sleep=time.sleep, rng: random.Random | None = None,
                  before_attempt=None, record=None):
    """One provider call under the failure policy. Returns the Response; raises RateLimited, ProviderFailed (or the
    budget's BudgetExhausted from `before_attempt`). `record(attempt dict)` sees every failed attempt."""
    from .providers.base import ProviderError
    rng = rng or random.Random()
    attempts: list[dict] = []
    rl = pv = 0
    while True:
        _gate_wait(policy, sleep)                        # session 12: a pause another worker's 429 started
        if before_attempt:
            before_attempt()
        try:
            return prov.complete(req)
        except ProviderError as e:
            err = e
        except (socket.timeout, TimeoutError) as e:
            err = ProviderError("timeout", str(e) or "timed out", True)
        except (ConnectionError, urllib.error.URLError) as e:
            err = ProviderError("network", str(e)[:300], True)
        cls = classify(err)
        n = len(attempts) + 1
        if cls == "rate_limit":
            hint = getattr(err, "retry_after", None)
            if policy.after_deferral or rl >= policy.max_tries or (hint is not None and hint > policy.honour_reset_up_to_s):
                a = _attempt(cls, err, None, n)
                attempts.append(a)
                record and record(a)
                why = ("another batch of this run was deferred for a rate limit: one try, no backoff"
                       if policy.after_deferral else
                       f"the provider names a reset in {hint:g} s, beyond {policy.honour_reset_up_to_s:g} s"
                       if hint is not None and hint > policy.honour_reset_up_to_s else
                       f"still rate limited after {rl} backoff(s) of {sum(x['wait_s'] or 0 for x in attempts):g} s")
                _gate_pause(policy, hint if hint is not None else policy.backoff_s[0])
                raise RateLimited(f"rate limit ({getattr(err, 'kind', '')}: {_short(err.message, 200)}); {why}",
                                  attempts, hint)
            wait = policy.rate_wait(rl, rng, hint)
            a = _attempt(cls, err, wait, n)
            attempts.append(a)
            record and record(a)
            _gate_pause(policy, wait)
            sleep(wait)
            rl += 1
            continue
        if err.retryable and pv < policy.provider_retries:
            wait = min(err.retry_after if err.retry_after is not None else policy.provider_backoff_s * (2 ** pv), 60.0)
            a = _attempt(cls, err, wait, n)
            attempts.append(a)
            record and record(a)
            sleep(wait)
            pv += 1
            continue
        a = _attempt(cls, err, None, n)
        attempts.append(a)
        record and record(a)
        raise ProviderFailed(f"provider failure ({err.kind}: {_short(err.message, 300)}) after {pv} retr"
                             f"{'y' if pv == 1 else 'ies'}", attempts)


def call_host(run: Callable, policy: FailurePolicy, *, sleep=time.sleep, rng: random.Random | None = None,
              record=None):
    """One host session under the failure policy: `run()` starts a session and returns its SessionResult (classified by
    hostsession.classify). Returns the result of a session that ended normally; raises RateLimited / ProviderFailed."""
    rng = rng or random.Random()
    attempts: list[dict] = []
    rl = pv = 0
    while True:
        _gate_wait(policy, sleep)                        # session 12: a pause another worker's 429 started
        res = run()
        cls = getattr(res, "failure_class", None)
        if cls == "refused":                              # session 11 (E135): a local refusal (a lock) is not retried
            raise B.Refused(res.error or "the host session was refused")
        if cls is None:
            return res
        n = len(attempts) + 1
        err = type("E", (), {"kind": f"host_{cls}", "status": getattr(res, "api_error_status", None),
                             "message": f"{res.error or ''} {_short(res.final_text, 200)}".strip()})()
        if cls == "rate_limit":
            hint = getattr(res, "reset_in_s", None)
            if policy.after_deferral or rl >= policy.max_tries or (hint is not None and hint > policy.honour_reset_up_to_s):
                a = _attempt(cls, err, None, n)
                attempts.append(a)
                record and record(a)
                why = ("another batch of this run was deferred for a rate limit: one try, no backoff"
                       if policy.after_deferral else
                       f"the host names a reset in {hint:g} s, beyond {policy.honour_reset_up_to_s:g} s"
                       if hint is not None and hint > policy.honour_reset_up_to_s else
                       f"still rate limited after {rl} backoff(s) of {sum(x['wait_s'] or 0 for x in attempts):g} s")
                _gate_pause(policy, hint if hint is not None else policy.backoff_s[0])
                raise RateLimited(f"host rate limit ({err.message}); {why}", attempts, hint)
            wait = policy.rate_wait(rl, rng, hint)
            a = _attempt(cls, err, wait, n)
            attempts.append(a)
            record and record(a)
            _gate_pause(policy, wait)
            sleep(wait)
            rl += 1
            continue
        if pv < policy.host_retries:
            wait = policy.provider_backoff_s * (2 ** pv)
            a = _attempt(cls, err, wait, n)
            attempts.append(a)
            record and record(a)
            sleep(wait)
            pv += 1
            continue
        a = _attempt(cls, err, None, n)
        attempts.append(a)
        record and record(a)
        raise ProviderFailed(f"host session failure ({err.message}) after {pv} retr{'y' if pv == 1 else 'ies'}",
                             attempts)


# ---------------------------------------------------------------------------------------------- capabilities and size

def require(sp: TaskSpec, caps, images: int = 0, route: str = "", model: str = "") -> list[dict]:
    """The capability check before any call. Raises CapabilityRefused; returns the route notices it adds (capabilities
    used unverified, or declared by the host) so they stay visible."""
    from .providers.base import notice
    who = f"{route} {model}".strip() or "the route"
    problems = []
    if sp.tools and caps.tools is not True:
        problems.append(f"the {sp.phase} phase offers tools and {who} does not report tool use (tools={caps.tools}; "
                        f"source: {caps.source})")
    need_img = sp.needs_images or images > 0
    if need_img and caps.images is not True:
        what = ("the reading phase reads an image and REQUIRES image input" if sp.needs_images else
                f"the request attaches {images} image(s), which needs image input")
        problems.append(f"{what}; {who} does not report image input (images={caps.images}; source: {caps.source}): "
                        "refused, not degraded to text")
    if problems:
        raise CapabilityRefused("; ".join(problems))
    notes = []
    det = getattr(caps, "details", None) or {}
    if det.get("declared"):
        notes.append(notice("capabilities_declared", f"capabilities declared, not verified: {who} ({caps.source}); "
                                                     f"the {sp.phase} request was checked against them",
                            route=route, model=model, phase=sp.phase))
    elif det.get("unverified"):
        notes.append(notice("capabilities_unverified", f"capabilities unverified: {who} ran the {sp.phase} phase on "
                                                       f"configured values ({caps.source})", route=route, model=model,
                            phase=sp.phase))
    return notes


def size(sp: TaskSpec, caps, text: str, *, system: str | None = None, tools_spec: list | None = None, images: int = 0,
         units: int = 0, max_output_tokens: int | None = None, settings: dict | None = None):
    from . import batching
    return batching.request_size(sp.phase, caps, system=system if system is not None else sp.system,
                                 tools=tools_spec, packet_text=text, images=images, prior_turns=bool(sp.tools),
                                 units=units, max_output_tokens=max_output_tokens, settings=settings)


def settings_for(cfg: dict | None, route: str | None) -> dict:
    """config/ai.yaml `batching`, with the route's own `batching` over it (e.g. Ollama's smaller later-turn allowance)."""
    cfg = cfg or {}
    rb = (((cfg.get("routes") or {}).get(route) or {}).get("batching") or {}) if route else {}
    return {**(cfg.get("batching") or {}), **rb}


def context_fits(sz) -> bool:
    """The hard part of a size: input + output within the usable context, the output counted at most at the output cap
    (a call never writes more); the output estimate against the cap is the planner's (converse(enforce_output_estimate))."""
    out = min(sz.output_tokens, sz.output_cap) if sz.output_cap else sz.output_tokens
    return sz.usable_tokens is not None and sz.input_tokens + out <= sz.usable_tokens


def _loggable(msgs: list[dict]) -> list[dict]:
    out = []
    for m in msgs:
        m = {k: v for k, v in m.items() if k != "provider_raw"}
        if m.get("role") == "tool":
            m = {"role": "tool", "results": [{**x, "content": truncate(x["content"], 4000)} for x in m["results"]]}
        out.append(m)
    return out


def check_size(sp: TaskSpec, sz) -> None:
    if not sz.fits:
        raise TooLarge(f"the {sp.phase} request does not fit: {sz.why} ({sz.line()}); never truncated: split it by "
                       f"{'provision' if sp.phase == 'analysis' else 'task' if sp.phase == 'downstream' else 'item'}, "
                       "or a person splits a single one", sz)


def units_of(sp: TaskSpec, packet: dict) -> int:
    if sp.phase == "analysis":
        return len(packet.get("provisions") or [])
    if sp.phase == "downstream":
        return len(packet.get("tasks") or [])
    if sp.phase == "critic":
        return len(packet.get("items") or [])
    return 1


def packet_images(packet: dict) -> int:
    """Images the request carries or the session is asked to read: attached crops and listed image targets."""
    return len(packet.get("crops") or []) + len(packet.get("image_targets") or [])


# ---------------------------------------------------------------------------------------------- the packet, once

def compact_analysis(packet: dict) -> dict:
    """Shared context once per session: the candidate targets' texts move to one `targets` map (a target cited by
    several provisions is sent once), and the pattern drafter's reference keeps only this batch's provisions. Nothing
    of the batch's own provisions is shortened."""
    pk = dict(packet)
    provs = {p.get("unit_id") for p in pk.get("provisions") or []}
    targets: dict = {}
    plist = []
    for p in pk.get("provisions") or []:
        ids = []
        for c in p.get("candidate_targets") or []:
            t = c.get("target")
            if t is None:
                continue
            targets.setdefault(t, {k: v for k, v in c.items() if k != "target"})
            ids.append(t)
        plist.append({**p, "candidate_targets": ids})
    pk["provisions"] = plist
    pk["targets"] = targets
    ref = dict(pk.get("reference") or {})
    if ref:
        ref["ops"] = [o for o in ref.get("ops") or [] if o.get("provision") in provs]
        ref["dispositions"] = [d for d in ref.get("dispositions") or [] if d.get("provision") in provs]
        ref["note"] = "the pattern drafter's output for THIS batch's provisions only"
        pk["reference"] = ref
    pk["packet_note"] = PACKET_NOTE + " `candidate_targets` name entries of `targets`."
    return compact_shared(pk)


SHARED_NOTE = ("`tools` names the tools offered with the request (their definitions come with the request itself); "
               "`#/$defs/NAME` in `schema` and `payload_schemas` is `schema_defs.NAME`, each definition printed once.")


def _untitled(x):
    """A JSON schema without its generated `title` strings (pydantic's 'Row Key' for row_key): nothing a model or the
    local validation uses. A PROPERTY named title (a dict under `properties`) is kept."""
    if isinstance(x, dict):
        return {k: _untitled(v) for k, v in x.items() if not (k == "title" and isinstance(v, str))}
    if isinstance(x, list):
        return [_untitled(v) for v in x]
    return x


def compact_shared(packet: dict) -> dict:
    """Session 12: the shared part of a packet (repeated in every batch's session) sent smaller, its meaning kept:
      * `tools`: the names only; the definitions reach the model with the request (the MCP tool list on the host
        route, the request's `tools` on the API routes), so the packet no longer repeats their descriptions;
      * `schema` and `payload_schemas`: without the generated `title` strings, and every `$defs` entry printed ONCE
        in `schema_defs` (a definition whose name clashes with a different one stays where it is).
    Nothing of the batch's own provisions, tasks, targets or evidence is touched, and the answer's schema sent
    NATIVELY (structured output) and the local validation are unchanged (they come from the contract, not the packet).
    Measured on blind-05's packets: see tests/test_session12_concurrency.py and the session-12 report."""
    pk = dict(packet)
    if isinstance(pk.get("tools"), list) and pk["tools"] and isinstance(pk["tools"][0], dict):
        pk["tools"] = [t.get("name") for t in pk["tools"]]
    if not isinstance(pk.get("schema"), dict) and not isinstance(pk.get("payload_schemas"), dict):
        return pk
    defs: dict = {}

    def lift(sc):
        sc = _untitled(sc)
        if isinstance(sc, dict) and isinstance(sc.get("$defs"), dict):
            own = {}
            for k, v in sc["$defs"].items():
                if k in defs and defs[k] != v:
                    own[k] = v
                else:
                    defs[k] = v
            sc = {k: v for k, v in sc.items() if k != "$defs"}
            if own:
                sc["$defs"] = own
        return sc
    if isinstance(pk.get("schema"), dict):
        pk["schema"] = lift(pk["schema"])
    if isinstance(pk.get("payload_schemas"), dict):
        pk["payload_schemas"] = {k: lift(v) for k, v in pk["payload_schemas"].items()}
    if defs:
        pk["schema_defs"] = defs
    pk["shared_note"] = SHARED_NOTE
    return pk


# ---------------------------------------------------------------------------------------------- checks and repair

def _extract(text):
    from .controller import ParseError, _extract_json
    try:
        return _extract_json(text), None
    except ParseError as e:
        return None, str(e)


def check(sp: TaskSpec, answer, packet: dict | None = None, fields: dict | None = None):
    """(data, envelope errors, item problems) of an answer (text or an object); see the module docstring."""
    from .providers import structured as SO
    data, err = (_extract(answer) if isinstance(answer, str) else (answer, None))
    if err:
        return None, [err], []
    data = SO.decode_free_form(data, sp.schema)
    if isinstance(data, dict) and sp.phase == "downstream" and "downstream_set" in data:
        data = data["downstream_set"]
    if not isinstance(data, dict):
        return None, ["the answer must be a JSON object"], []
    fields = fields or _dummy_fields(sp)
    env: list[str] = []
    problems: list[dict] = []
    if sp.items_field is None:
        try:
            sp.parse(data, dict(fields), [])
        except sp.parse_errors as e:
            env.append(_short(str(e), 1500))
        return data, env, []
    items = data.get(sp.items_field, [])
    if not isinstance(items, list):
        return data, [f"`{sp.items_field}` must be a list"], []
    try:
        sp.parse({**data, sp.items_field: []}, dict(fields), [])
    except sp.parse_errors as e:
        env.append(_short(str(e), 1500))
    declared = {s.get("id") for s in data.get("statements") or [] if isinstance(s, dict)}
    tasks = {t.get("id") for t in (packet or {}).get("tasks") or [] if isinstance(t, dict)}
    asked = {x.get("key") for x in (packet or {}).get("items") or [] if isinstance(x, dict)}
    for i, it in enumerate(items):
        errs, refs = [], []                                  # schema errors (unusable) / reference errors (rated later)
        if not isinstance(it, dict):
            errs.append("an item must be a JSON object")
        else:
            if sp.item_model is not None:
                try:
                    sp.item_model.model_validate(_for_item_check(sp, it))
                except Exception as e:                       # noqa: BLE001 (pydantic: reported to the model)
                    errs.append(_short(str(e), 900))
            if sp.phase in ("analysis", "downstream"):
                sts = it.get("statements") or []
                bad = [s for s in sts if not isinstance(s, str) or s not in declared] if isinstance(sts, list) else [sts]
                if bad:
                    refs.append(f"`statements` must list ids of entries of the set's `statements` (ids only, never free "
                                f"text); not ids: {[_short(x, 80) for x in bad][:5]} (declared: {sorted(declared)[:20]})")
            if sp.phase == "downstream" and tasks and it.get("task") not in tasks:
                refs.append(f"`task` {it.get('task')!r} is not a task of this packet ({sorted(tasks)[:12]})")
            if sp.phase == "critic" and asked and it.get("item") not in asked:
                errs.append(f"`item` {it.get('item')!r} is not an item of this request ({sorted(asked)[:12]})")
        if errs or refs:
            problems.append({"index": i, "id": it.get("id") or it.get("item") if isinstance(it, dict) else None,
                             sp.item_key: it.get(sp.item_key) if isinstance(it, dict) else None, "errors": errs + refs,
                             "kind": "schema" if errs else "reference"})
    return data, env, problems


def _for_item_check(sp: TaskSpec, it: dict) -> dict:
    if sp.phase == "analysis":
        from .providers import structured as SO
        it = SO.decode_payloads({"items": [it]})["items"][0]
        return {k: v for k, v in it.items() if k != "review"}
    return it


def _dummy_fields(sp: TaskSpec) -> dict:
    base = {"run_id": "check", "created": "-", "route": "check", "provider": "check", "model_requested": "-",
            "model_reported": None, "task": sp.task}
    if sp.phase == "analysis":
        from .contract import CONTROLLER_VERSION
        base["controller_version"] = CONTROLLER_VERSION
    return base


def repair_message(sp: TaskSpec, env: list[str], problems: list[dict]) -> str:
    lines = ["REPAIR REQUEST: your answer could not be parsed or used as it stands. The controller's local checks "
             "found:"]
    lines += [f"- the answer: {e}" for e in env]
    for p in problems[:40]:
        lines.append(f"- {sp.items_field[:-1] if sp.items_field else 'item'} {p['index']} (id {p.get('id')!r}, "
                     f"{sp.item_key} {p.get(sp.item_key)!r}): " + " | ".join(p["errors"]))
    if len(problems) > 40:
        lines.append(f"- … {len(problems) - 40} more item(s) with problems")
    lines.append("Reply again with ONLY the corrected JSON object described by `schema` in the packet: the whole object, "
                 "every item, fixing what is listed (this is the one re-ask: an item that still fails its schema is set "
                 "aside as malformed; a reference that still fails is rated by the controller). An item's `statements` "
                 "lists only ids of entries of the set's `statements`.")
    return "\n".join(lines)


def finish(sp: TaskSpec, data: dict, env: list[str], problems: list[dict], fields: dict, overwrites: list):
    """The answer after the checks: Malformed when the envelope fails; otherwise the strict parse of the set without
    the items that still fail their SCHEMA (the malformed items). An item whose only problem is a reference (a statement
    id the set does not declare, a task not in the packet) is kept: the controller's own checks rate it (unknown
    statement -> insufficient_evidence), with the reason, so nothing a person could read is dropped."""
    if data is None or env:
        raise Malformed(f"the {sp.phase} answer is malformed after the bounded repair: " + "; ".join(env)[:1500], env)
    clean = data
    if sp.items_field is not None and problems:
        bad = {p["index"] for p in problems if p.get("kind", "schema") == "schema"}
        clean = {**data, sp.items_field: [it for i, it in enumerate(data.get(sp.items_field) or []) if i not in bad]}
    try:
        return sp.parse(clean, dict(fields), overwrites)
    except sp.parse_errors as e:
        raise Malformed(f"the {sp.phase} answer is malformed: {_short(str(e), 1500)}", [str(e)]) from None


# ---------------------------------------------------------------------------------------------- the outcome

@dataclass
class Outcome:
    phase: str
    answer: object = None
    malformed_items: list = field(default_factory=list)
    problems_before_repair: list = field(default_factory=list)
    repaired: bool = False
    attempts: list = field(default_factory=list)
    size: dict | None = None
    usage: dict = field(default_factory=lambda: {"calls": 0, "input_tokens": 0, "output_tokens": 0, "cost_usd": None,
                                                 "cost_basis": "no price configured"})
    model_reported: str | None = None
    notices: list = field(default_factory=list)
    turns: int = 0
    overwrites: list = field(default_factory=list)
    run_id: str | None = None
    host_sessions: list = field(default_factory=list)
    reference_problems: list = field(default_factory=list)   # kept after the repair; the controller rates them

    def record(self) -> dict:
        """What the checkpoint keeps for a batch (no answer body)."""
        return {"phase": self.phase, "malformed_items": self.malformed_items, "repaired": self.repaired,
                "reference_problems": self.reference_problems,
                "problems_before_repair": self.problems_before_repair[:40], "attempts": self.attempts,
                "size": self.size, "usage": self.usage, "notices": self.notices, "turns": self.turns,
                "host_sessions": self.host_sessions}


# ---------------------------------------------------------------------------------------------- tools

def run_tool(ws, call, log: RunLog, images_ok: bool, maxchars: int, allowed: list[str]) -> dict:
    """A tool call of a request: only the tools offered; arguments are data; get_crop and get_region attach their images
    when the provider takes images (the phase's capability check already refused a route without them where images
    are needed)."""
    from .tools import ToolError, call_tool
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
    if len(content) > maxchars:
        log.event("tool_result_truncated", name=call.name, characters=len(content), limit=maxchars,
                  note="the model is told the result was truncated (caps.max_tool_result_chars); it can ask for less")
    return {"tool_call_id": call.id, "name": call.name, "content": truncate(content, maxchars), "is_error": err,
            "images": images}


def _images_in(messages: list[dict]) -> int:
    n = 0
    for m in messages:
        n += sum(1 for p in m.get("content") or [] if isinstance(p, dict) and p.get("type") == "image")
        n += sum(len(r.get("images") or []) for r in m.get("results") or [])
    return n


def conversation_tokens(messages: list[dict], cpt: float = 3.5) -> int:
    return int(sum(len(json.dumps({k: v for k, v in m.items() if k != "provider_raw"}, ensure_ascii=False, default=str))
                   for m in messages) / cpt)


# ---------------------------------------------------------------------------------------------- provider routes

def converse(sp: TaskSpec, prov, packet: dict, *, ws, route: str, caps_: dict, price, policy: FailurePolicy,
             log: RunLog, staging: Path, run_id: str, fields: dict, sleep=time.sleep, rng: random.Random | None = None,
             images: list[dict] | None = None, prompt_text: str | None = None, settings: dict | None = None,
             tool_ws=None, enforce_output_estimate: bool = True) -> Outcome:
    """One request of `sp` with a provider (recorded or an API route): the capability check, the complete size, the
    turn loop with the phase's tools, the failure policy on every call, the per-turn context bound, the one repair
    turn and the item-level malformed separation. Returns an Outcome; raises CapabilityRefused, TooLarge, RateLimited,
    ProviderFailed, Malformed, ContextExhausted or BudgetExhausted (each carrying `.outcome` with the usage so far).
    `enforce_output_estimate` False (a single standalone run, which cannot split: `ai propose`): an expected output over
    the per-call cap is recorded (the prompt event's `size_note`, the staged `request.size`), not refused; the context bound is always
    enforced."""
    from .providers.base import ProviderError, Request, collect_notices
    from .providers.recorded import PACKET_MARK
    from .tools import TOOLS
    rng = rng or random.Random()
    out = Outcome(sp.phase, run_id=run_id)
    st = settings or {}
    with collect_notices() as notes:
        try:
            if hasattr(prov, "check_ready"):
                prov.check_ready()
            capsr = prov.capabilities()
        except ProviderError as e:
            log.event("refused", reason=e.message, stage="capabilities")
            raise CapabilityRefused(f"capability check failed: {e.message}") from None
        log.event("capabilities", phase=sp.phase, **capsr.to_dict())
        images = list(images or [])
        try:
            require(sp, capsr, len(images), route, getattr(prov, "model", ""))
        except CapabilityRefused as e:
            log.event("refused", reason=str(e), stage="capabilities", phase=sp.phase)
            raise
        tools_spec = [TOOLS[n].spec() for n in sp.tools]
        text = prompt_text if prompt_text is not None else PACKET_MARK + json.dumps(packet, ensure_ascii=False,
                                                                                      default=str)
        budget = B.Budget(caps_, price)
        per_call = int(caps_.get("max_tokens_per_call") or 8000)          # the run's remaining budget: Budget's
        sz = size(sp, capsr, text, tools_spec=tools_spec, images=len(images), units=units_of(sp, packet),
                  max_output_tokens=per_call, settings=st)
        out.size = sz.to_dict()
        size_note = None
        if not sz.fits and not enforce_output_estimate and context_fits(sz):
            size_note = (f"the expected output ({sz.output_tokens} tokens, an estimate) exceeds the output cap "
                         f"({sz.output_cap}); the answer may be cut (then malformed): send part of the task "
                         "(--provisions). Recorded, not refused: this single run cannot split")
        elif not sz.fits:
            log.event("refused", reason=sz.why, stage="size", size=sz.to_dict())
            e = TooLarge(f"the {sp.phase} request does not fit: {sz.why} ({sz.line()}); never truncated", sz)
            e.outcome = out
            raise e
        log.event("prompt", phase=sp.phase, system=sp.system, packet=packet if prompt_text is None else None,
                  prompt=prompt_text, size=sz.to_dict(), tools=[t["name"] for t in tools_spec],
                  images=[{"sha256": i.get("sha256")} for i in images], schema_sent=True, size_note=size_note)
        messages = [{"role": "user", "content": [{"type": "text", "text": text}] + images}]
        maxchars = int(caps_.get("max_tool_result_chars") or 20000)
        usable = sz.usable_tokens
        cpt = float(st.get("chars_per_token", 3.5))
        image_tokens = int(st.get("image_tokens", 4800))
        overhead = sz.system_tokens + sz.tools_tokens
        repaired, final = False, None
        first = None
        logged = 1

        def rec(a):
            out.attempts.append(a)
            log.event("provider_error", **a)
            B.record_spend(staging, {"ts": _now(), "run_id": run_id, "route": route, "provider": prov.name,
                                     "model_requested": prov.model, "input_tokens": 0, "output_tokens": 0,
                                     "cost_usd": None, "cost_basis": "failed attempt: no usage reported",
                                     "error": a["kind"], "failure_class": a["class"]})
        try:
            while True:
                budget.next_turn()
                req = Request(system=sp.system, messages=messages, tools=tools_spec, response_schema=sp.schema,
                              max_tokens=budget.max_tokens(), timeout_s=budget.call_timeout())
                used = overhead + conversation_tokens(messages, cpt) + _images_in(messages) * image_tokens
                if usable and used + req.max_tokens > usable:
                    raise ContextExhausted(f"context bound at turn {budget.turns}: about {used} tokens of conversation "
                                           f"(system, tools, turns, images) plus {req.max_tokens} output tokens exceed "
                                           f"the usable context of {usable}; the batch needs to be smaller")
                log.event("request", turn=budget.turns, max_tokens=req.max_tokens, timeout_s=round(req.timeout_s, 1),
                          new_messages=_loggable(messages[logged:]) if budget.turns > 1 else "(the prompt above)")
                logged = len(messages)
                resp = call_provider(prov, req, policy, sleep=sleep, rng=rng, before_attempt=budget.before_call,
                                     record=rec)
                out.model_reported = resp.model_reported or out.model_reported
                usd0 = budget.cost_usd()[0]
                log.event("response", turn=budget.turns, text=resp.text, stop_reason=resp.stop_reason, usage=resp.usage,
                          tool_calls=[{"id": c.id, "name": c.name, "arguments": c.arguments} for c in resp.tool_calls])
                try:
                    budget.after_call(resp.usage.get("input_tokens", 0), resp.usage.get("output_tokens", 0))
                finally:
                    usd1, basis = budget.cost_usd()
                    B.record_spend(staging, {"ts": _now(), "run_id": run_id, "route": route, "provider": prov.name,
                                             "model_requested": prov.model, "model_reported": resp.model_reported,
                                             "input_tokens": resp.usage.get("input_tokens", 0),
                                             "output_tokens": resp.usage.get("output_tokens", 0),
                                             "cost_usd": None if usd1 is None else round(usd1 - (usd0 or 0), 6),
                                             "cost_basis": basis})
                messages.append({"role": "assistant",
                                 "content": [{"type": "text", "text": resp.text}] if resp.text else [],
                                 "tool_calls": [{"id": c.id, "name": c.name, "arguments": c.arguments}
                                                for c in resp.tool_calls], "provider_raw": resp.provider_raw})
                if resp.tool_calls:
                    messages.append({"role": "tool", "results": [
                        run_tool(tool_ws or ws, c, log, capsr.images is True, maxchars, list(sp.tools))
                        for c in resp.tool_calls]})
                    continue
                data, env, probs = check(sp, resp.text, packet, fields)
                if env or probs:
                    log.event("parse_error", error="; ".join(env) or f"{len(probs)} item(s) with problems",
                              problems=probs[:20], retry_used=repaired)
                if first is None:
                    first = (data, env, probs)
                if (env or probs) and not repaired and policy.repairs > 0:
                    out.problems_before_repair = [{"answer": e} for e in env] + probs
                    log.event("repair_ask", errors=env, problems=probs[:40])
                    repaired = True
                    messages.append({"role": "user", "content": [{"type": "text",
                                                                  "text": repair_message(sp, env, probs)}]})
                    continue
                final = (data, env, probs)
                break
        except B.BudgetExhausted as e:
            _usage(out, budget)
            out.notices = list(notes)
            log.event("budget_exhausted", reason=str(e))
            e.outcome = out
            raise
        except (RateLimited, ProviderFailed, ContextExhausted) as e:
            _usage(out, budget)
            out.notices = list(notes)
            log.event({RateLimited: "rate_limited", ProviderFailed: "provider_failed",
                       ContextExhausted: "context_exhausted"}[type(e)], message=e.message, attempts=out.attempts)
            e.outcome = out
            raise
        _usage(out, budget)
        out.turns, out.repaired = budget.turns, repaired
        data, env, probs = final
        if env and first is not None and not first[1]:          # the repair broke the envelope: keep the first answer
            data, env, probs = first
        fields = {**fields, "model_reported": out.model_reported or fields.get("model_reported")}
        try:
            out.answer = finish(sp, data, env, probs, fields, out.overwrites)
        except Malformed as e:
            out.notices = list(notes)
            log.event("malformed", errors=e.errors, repaired=repaired)
            e.outcome = out
            raise
        out.malformed_items = [x for x in probs if x.get("kind") == "schema"]
        out.reference_problems = [x for x in probs if x.get("kind") == "reference"]
        if probs:
            log.event("malformed_items", items=out.malformed_items, left_to_the_controller=out.reference_problems)
        if out.overwrites:
            log.event("overwrites", overwrites=out.overwrites)
        out.notices = list(notes)
    log.event("end", phase=sp.phase, status="parsed", repaired=repaired, malformed_items=len(out.malformed_items),
              calls=out.usage["calls"], notices=out.notices)
    return out


def _usage(out: Outcome, budget) -> None:
    usd, basis = budget.cost_usd()
    out.usage = {"calls": budget.calls, "input_tokens": budget.input_tokens, "output_tokens": budget.output_tokens,
                 "cost_usd": usd, "cost_basis": basis}


def _now() -> str:
    import datetime as dt
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------------------------- host route

REPAIR_RULES = ("\nRepair rules: you have NO tools now. The evidence you read before is not repeated: correct ONLY what "
                "the listed problems name, keep every quotation as it was, and reply with ONLY the corrected JSON "
                "object (no prose, no code fence).")


def host_repair(sp: TaskSpec, cfg: dict, previous: str, env: list[str], problems: list[dict], cwd: Path, log: RunLog,
                policy: FailurePolicy, *, model: str | None = None, sleep=time.sleep, rng=None, record=None,
                runner=None) -> tuple[str, dict]:
    """The bounded repair on the host route: ONE plain session (no tools) given the previous answer, the schema and the
    errors; returns (its final text, the session's record). The failure policy applies to it too."""
    from . import hostsession as HS
    kw = {"runner": runner} if runner is not None else {}
    ps = HS.PlainSession(cfg, sp.system + REPAIR_RULES, model=model, label=f"repair-{sp.phase}", **kw)
    prompt = (repair_message(sp, env, problems) + "\n\nSCHEMA\n" + json.dumps(sp.schema, ensure_ascii=False)
              + "\n\nYOUR PREVIOUS ANSWER\n" + (previous or "(none: the session ended without an answer)"))
    res = call_host(lambda: ps.run(prompt, cwd, log), policy, sleep=sleep, rng=rng, record=record)
    text = json.dumps(res.structured_output, ensure_ascii=False) if res.structured_output is not None else res.final_text
    return text, {"label": ps.label, "elapsed_s": res.elapsed_s, "model_reported": res.model_reported,
                  "error": res.error, "host_plan_cost_usd": res.host_plan_cost_usd}


def ask_host(sp: TaskSpec, session, packet: dict, *, cfg: dict, policy: FailurePolicy, log: RunLog, fields: dict,
             cwd: Path, sleep=time.sleep, rng: random.Random | None = None, settings: dict | None = None,
             runner=None) -> Outcome:
    """One request of `sp` in a host ANSWER session (hostsession.AnswerSession, or a PlainSession wrapped by the
    caller): the declared capabilities checked (image input for the reading phase), the complete size of the prompt,
    the failure policy, then the final message checked and repaired once (a plain no-tool session). Raises like
    converse."""
    from .providers.base import collect_notices
    rng = rng or random.Random()
    out = Outcome(sp.phase, run_id=fields.get("run_id"))
    with collect_notices() as notes:
        caps = session.capabilities()
        n_img = packet_images(packet) + (1 if sp.needs_images else 0)
        require(sp, caps, n_img, "host", session.host_model_label())
        prompt = session.prompt(packet)
        from .tools import TOOLS
        tools_spec = [TOOLS[n].spec() for n in sp.tools if n in TOOLS]
        sz = size(sp, caps, prompt, system=session.system_prompt(), tools_spec=tools_spec, images=n_img,
                  units=units_of(sp, packet), settings=settings)
        out.size = sz.to_dict()
        if not sz.fits:
            log.event("refused", reason=sz.why, stage="size", size=sz.to_dict())
            e = TooLarge(f"the {sp.phase} request does not fit: {sz.why} ({sz.line()}); never truncated", sz)
            e.outcome = out
            raise e

        def rec(a):
            out.attempts.append(a)
            log.event("host_failure", **a)

        def run():
            session.run_batch(packet)
            last = session.last
            out.host_sessions.append({"run_id": last.run_id, "elapsed_s": last.elapsed_s, "error": last.error,
                                      "failure_class": last.failure_class, "model_reported": last.model_reported,
                                      "tool_calls": len(last.tool_calls), "crops_read": last.crops_read})
            return last
        try:
            res = call_host(run, policy, sleep=sleep, rng=rng, record=rec)
            out.model_reported = ", ".join(res.model_reported or []) or None
            text = res.final_text
            data, env, probs = check(sp, text, packet, fields)
            first = (data, env, probs)
            if (env or probs) and policy.repairs > 0:
                out.problems_before_repair = [{"answer": e} for e in env] + probs
                log.event("repair_ask", errors=env, problems=probs[:40])
                text2, meta = host_repair(sp, cfg, text, env, probs, cwd, log, policy, model=getattr(session, "model", None),
                                          sleep=sleep, rng=rng, record=rec, runner=runner)
                out.host_sessions.append({"repair": True, **meta})
                out.repaired = True
                data, env, probs = check(sp, text2, packet, fields)
                if env and not first[1]:
                    data, env, probs = first
        except (RateLimited, ProviderFailed) as e:
            out.notices = list(notes)
            e.outcome = out
            raise
        fields = {**fields, "model_reported": out.model_reported or fields.get("model_reported")}
        try:
            out.answer = finish(sp, data, env, probs, fields, out.overwrites)
        except Malformed as e:
            out.notices = list(notes)
            log.event("malformed", errors=e.errors, repaired=out.repaired)
            e.outcome = out
            raise
        out.malformed_items = [x for x in probs if x.get("kind") == "schema"]
        out.reference_problems = [x for x in probs if x.get("kind") == "reference"]
        if probs:
            log.event("malformed_items", items=out.malformed_items, left_to_the_controller=out.reference_problems)
        out.notices = list(notes)
    log.event("end", phase=sp.phase, status="parsed", repaired=out.repaired, malformed_items=len(out.malformed_items),
              host_sessions=out.host_sessions, notices=out.notices)
    return out
