"""Budgets, spend and locks for model runs.

Caps (config/ai.yaml `defaults.caps` < route `caps` < command line): max_calls, max_input_tokens, max_output_tokens,
max_usd, timeout_s (wall clock for the whole run), max_turns, concurrency (orchestrator runs at once), and per call
max_tokens_per_call, call_timeout_s, retries, backoff_s.
  * Before every provider call (each retry attempt counts as a call) the budget is checked; after every call the
    usage is added. Exceeding any cap raises BudgetExhausted: the run stops with status `budget_exhausted` and
    nothing is published (the partial log and an empty proposal record stay in staging).
  * Cost: `prices: {model: {input_per_mtok, output_per_mtok}}` (USD per million tokens). With no price for the model,
    cost_usd stays null with cost_basis "no price configured", and a PAID route refuses to start unless max_calls and
    both token caps are set (with a price, max_calls and either the token caps or max_usd).
  * Every call is appended to the persistent spend meter staging/ai/spend.jsonl.

Locks: staging/ai/.lock-<ADDENDUM> stops two orchestrators (e.g. a coding host and an API route) working on the same
addendum. A lock is STALE when its process is dead (same host) or it is older than `lock_stale_after_min`; a stale
lock is reported, never silently taken over. `--break-lock --by NAME` removes a lock only for a person's name
(readings.valid_reviewer and not readings.is_assistant); every break is recorded in staging/ai/locks.jsonl.

Staging safety: the staging directory may not be, or lie inside, curation/, config/, build/, out/, sources/,
tenderpack/, tests/, docs/, .git or the evidence build; run ids are restricted to [A-Za-z0-9._-].
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import socket
import time
from pathlib import Path

from ..readings import is_assistant, valid_reviewer
from ..util import ROOT

PAID_ROUTES_DEFAULT = ("anthropic", "openrouter")
NO_STAGING_UNDER = ("curation", "config", "build", "out", "sources", "tenderpack", "tests", "docs", ".git", ".venv")
RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,120}$")


class BudgetExhausted(Exception):
    pass


class Refused(Exception):
    """A run (or a step of it) that the controller refuses to start; nothing is sent to a provider."""


# ---------------------------------------------------------------------------------------------- staging safety

def safe_staging(staging: Path, root: Path = ROOT, evidence: Path | None = None) -> Path:
    s = Path(staging).absolute().resolve()
    root = Path(root).resolve()
    for name in NO_STAGING_UNDER:
        prot = root / name
        if s == prot or s.is_relative_to(prot):
            raise Refused(f"refusing staging directory {s}: it is inside the protected folder {prot}")
    if s == root or root.is_relative_to(s):
        raise Refused(f"refusing staging directory {s}: it is the repository or a parent of it")
    if evidence is not None:
        e = Path(evidence).resolve()
        if s == e or s.is_relative_to(e) or e.is_relative_to(s):
            raise Refused(f"refusing staging directory {s}: it overlaps the evidence build {e}")
    return s


def check_run_id(run_id: str) -> str:
    if not RUN_ID.match(run_id or "") or ".." in run_id:
        raise Refused(f"invalid run id {run_id!r}")
    return run_id


# ---------------------------------------------------------------------------------------------- prices and budget

def price_for(cfg: dict, model: str) -> dict | None:
    return (cfg.get("prices") or {}).get(model)


def cost(price: dict | None, input_tokens: int, output_tokens: int) -> tuple[float | None, str]:
    if not price:
        return None, "no price configured"
    c = input_tokens / 1e6 * price["input_per_mtok"] + output_tokens / 1e6 * price["output_per_mtok"]
    return round(c, 6), (f"config/ai.yaml prices: {price['input_per_mtok']} USD/Mtok in, {price['output_per_mtok']} "
                         "USD/Mtok out (as configured; not checked against an invoice)")


def check_startable(route_name: str, rcfg: dict, caps: dict, price: dict | None) -> None:
    """A paid route never starts without explicit limits (see the module docstring)."""
    paid = rcfg.get("paid", route_name in PAID_ROUTES_DEFAULT)
    if not paid:
        return
    missing = [k for k in ("max_calls",) if caps.get(k) is None]
    tokens = [k for k in ("max_input_tokens", "max_output_tokens") if caps.get(k) is None]
    if price is None:
        missing += tokens
        if missing:
            raise Refused(f"route {route_name} makes paid calls and no price is configured for the model, so cost "
                          f"cannot be computed: set {', '.join(missing)} (config/ai.yaml routes.{route_name}.caps or "
                          f"--{missing[0].replace('_', '-')}) before a live run")
    elif missing or (tokens and caps.get("max_usd") is None):
        raise Refused(f"route {route_name} makes paid calls: set max_calls and either both token caps or max_usd "
                      "before a live run")


class Budget:
    def __init__(self, caps: dict, price: dict | None, clock=time.monotonic):
        self.caps, self.price, self.clock = dict(caps), price, clock
        self.start = clock()
        self.calls = self.input_tokens = self.output_tokens = 0
        self.turns = 0

    # what the next call may use
    def elapsed(self) -> float:
        return self.clock() - self.start

    def call_timeout(self) -> float:
        per = self.caps.get("call_timeout_s") or 120
        total = self.caps.get("timeout_s")
        return max(1.0, min(per, total - self.elapsed())) if total else per

    def max_tokens(self) -> int:
        per = int(self.caps.get("max_tokens_per_call") or 8000)
        cap = self.caps.get("max_output_tokens")
        return max(0, min(per, int(cap) - self.output_tokens)) if cap is not None else per

    def cost_usd(self) -> tuple[float | None, str]:
        return cost(self.price, self.input_tokens, self.output_tokens)

    def before_call(self) -> None:
        c = self.caps
        if c.get("max_calls") is not None and self.calls >= c["max_calls"]:
            raise BudgetExhausted(f"max_calls {c['max_calls']} reached")
        if c.get("max_input_tokens") is not None and self.input_tokens >= c["max_input_tokens"]:
            raise BudgetExhausted(f"max_input_tokens {c['max_input_tokens']} reached ({self.input_tokens})")
        if c.get("max_output_tokens") is not None and self.max_tokens() <= 0:
            raise BudgetExhausted(f"max_output_tokens {c['max_output_tokens']} reached ({self.output_tokens})")
        usd, _ = self.cost_usd()
        if c.get("max_usd") is not None and usd is not None and usd >= c["max_usd"]:
            raise BudgetExhausted(f"max_usd {c['max_usd']} reached ({usd})")
        if c.get("timeout_s") is not None and self.elapsed() >= c["timeout_s"]:
            raise BudgetExhausted(f"timeout_s {c['timeout_s']} reached ({self.elapsed():.1f} s)")
        self.calls += 1

    def after_call(self, input_tokens: int, output_tokens: int) -> None:
        self.input_tokens += int(input_tokens or 0)
        self.output_tokens += int(output_tokens or 0)
        c = self.caps
        over = []
        if c.get("max_input_tokens") is not None and self.input_tokens > c["max_input_tokens"]:
            over.append(f"max_input_tokens {c['max_input_tokens']} exceeded ({self.input_tokens})")
        if c.get("max_output_tokens") is not None and self.output_tokens > c["max_output_tokens"]:
            over.append(f"max_output_tokens {c['max_output_tokens']} exceeded ({self.output_tokens})")
        usd, _ = self.cost_usd()
        if c.get("max_usd") is not None and usd is not None and usd > c["max_usd"]:
            over.append(f"max_usd {c['max_usd']} exceeded ({usd})")
        if over:
            raise BudgetExhausted("; ".join(over))

    def next_turn(self) -> None:
        if self.caps.get("max_turns") is not None and self.turns >= self.caps["max_turns"]:
            raise BudgetExhausted(f"max_turns {self.caps['max_turns']} reached without a final answer")
        self.turns += 1


def record_spend(staging: Path, entry: dict) -> None:
    p = Path(staging) / "spend.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, sort_keys=True) + "\n")


# ---------------------------------------------------------------------------------------------- locks

def lock_path(staging: Path, addendum: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9_-]+", addendum or ""):
        raise Refused(f"invalid addendum id {addendum!r}")
    return Path(staging) / f".lock-{addendum}"


def read_lock(path: Path) -> dict | None:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except (OSError, ValueError):
        return {"unreadable": True}


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def lock_state(info: dict, stale_after_min: float, now: float | None = None) -> tuple[bool, str]:
    """(stale, why)."""
    now = time.time() if now is None else now
    if info.get("unreadable"):
        return True, "the lock file is unreadable"
    age_min = (now - float(info.get("created_epoch", now))) / 60
    pid = info.get("pid")
    if pid and info.get("host") == socket.gethostname() and not _pid_alive(int(pid)):
        return True, f"its process {pid} is no longer running"
    if age_min > stale_after_min:
        return True, f"it is {age_min:.0f} min old (stale after {stale_after_min:g} min)"
    return False, f"held by {info.get('route')} run {info.get('run_id')} (pid {pid or '-'}, {age_min:.1f} min old)"


def live_locks(staging: Path, stale_after_min: float) -> list[dict]:
    out = []
    for p in sorted(Path(staging).glob(".lock-*")) if Path(staging).is_dir() else []:
        info = read_lock(p) or {}
        if not lock_state(info, stale_after_min)[0]:
            out.append({**info, "path": str(p)})
    return out


class Lock:
    def __init__(self, path: Path, info: dict):
        self.path, self.info = path, info

    def release(self) -> None:
        cur = read_lock(self.path)
        if cur and cur.get("token") == self.info.get("token"):
            self.path.unlink(missing_ok=True)


def acquire(staging: Path, addendum: str, holder: dict, stale_after_min: float = 120, concurrency: int | None = None) -> Lock:
    staging = Path(staging)
    staging.mkdir(parents=True, exist_ok=True)
    path = lock_path(staging, addendum)
    if concurrency:
        live = [x for x in live_locks(staging, stale_after_min) if x.get("addendum") != addendum]
        if len(live) >= concurrency:
            raise Refused(f"{len(live)} orchestrator run(s) already in progress ({', '.join(x.get('addendum', '?') for x in live)}); "
                          f"the configured concurrency is {concurrency}")
    info = {"addendum": addendum, "host": socket.gethostname(), "created": dt.datetime.now(dt.timezone.utc).isoformat(),
            "created_epoch": time.time(), "token": os.urandom(8).hex(), **holder}
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError:
        cur = read_lock(path) or {}
        stale, why = lock_state(cur, stale_after_min)
        if stale and why.startswith("its process") and cur.get("host") == socket.gethostname():
            # session 11 (E135): the holder died on this host (a crash, a container restart): nobody holds the
            # addendum, so the lock is taken over, as the run lock is, and the takeover is recorded in the new lock
            info["taken_over_from"] = {k: cur.get(k) for k in ("pid", "run_id", "route", "created", "token")}
            try:
                os.unlink(path)
            except FileNotFoundError:
                pass
            try:
                fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            except FileExistsError:
                raise Refused(f"another orchestrator holds {addendum}: the lock was taken by another process while a "
                              f"dead holder's lock was being taken over") from None
        else:
            raise Refused(f"another orchestrator holds {addendum}: " + (f"STALE lock ({why}); a person may remove it with "
                          f"--break-lock --by \"Your Name\"" if stale else f"{why}; wait for it to finish, or a person "
                          f"removes it with --break-lock --by \"Your Name\"")) from None
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(info, fh, sort_keys=True)
    return Lock(path, info)


def break_lock(staging: Path, addendum: str, by: str, stale_after_min: float = 120) -> tuple[bool, str]:
    if not valid_reviewer(by):
        return False, f"refused: --by must name the person breaking the lock, not a placeholder ({by!r})"
    if is_assistant(by):
        return False, f"refused: breaking a lock is a person's decision; {by!r} names the assistant or the program"
    path = lock_path(staging, addendum)
    info = read_lock(path)
    if info is None:
        return True, f"no lock on {addendum}"
    stale, why = lock_state(info, stale_after_min)
    path.unlink(missing_ok=True)
    rec = {"ts": dt.datetime.now(dt.timezone.utc).isoformat(), "addendum": addendum, "broken_by": by.strip(),
           "was_stale": stale, "state": why, "lock": {k: v for k, v in info.items() if k != "token"}}
    with open(Path(staging) / "locks.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, sort_keys=True) + "\n")
    return True, f"lock on {addendum} removed by {by.strip()} ({'stale: ' if stale else 'WAS LIVE: '}{why})"
