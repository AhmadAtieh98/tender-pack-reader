"""An ACTUAL host session (session 10, routes layer): a headless Claude Code run that works on a task packet ONLY through
the tenderpack MCP tools, reads image crops through them and submits through `submit_proposals`.

    HostSession(ws, cfg).run_batch(packet) -> proposal set dict      (the controller-validated, staged set)

The command (config/ai.yaml `host_session`; docs/AI_ROUTES.md):

    claude -p --mcp-config <run dir>/mcp.json --strict-mcp-config      the tenderpack server only:
              .venv/bin/python -m tenderpack ai serve-mcp --evidence <abs> --pack <abs> --out <staging> --worklog <log>
           --tools ""                                                  no built-in tool: no file, shell or web access
           --allowedTools <exactly the phase's tools>                  session 13: deny-by-default (policy.tools: the
                                                                       read-only tools + submit_proposals for analysis)
           --disallowedTools <every other tenderpack tool>             the packet is given; submit_proposals submits
           --permission-prompts none                                   anything else that would prompt is denied
           --no-session-persistence --output-format stream-json --verbose   every message, tool call and tool result
           --max-turns N --system-prompt <policy.compose(phase, "host")> [--model M]
    the server started with --tools <the same list> and, for analysis, --submit-once (a second submission is refused)
    and --require-crops <the packet's image_targets> (submit_proposals refused until get_crop was called for each)
    and, for a workflow batch, --submission-record <run>/batches/<batch>.submission.json (session 13: the submission
    written at once, so it survives the orchestrator's interruption; workflow._reuse_submission)
    with the task packet on stdin, under a wall-clock timeout. Session 13: the CLI process is started by run_tracked
    (subprocess.run's contract), so terminate_live() stops it when the orchestrator is interrupted.

stream-json is used rather than json because it records every tool call and tool result (the final `result` message
has the same fields as the json output: usage, total_cost_usd, modelUsage, num_turns). The total_cost_usd it reports is
the HOST'S own plan usage, never the application's spend (nothing is added to staging/ai/spend.jsonl).

What is recorded (worklog/model_calls/<run_id>.jsonl and <staging>/<run_id>/, secrets redacted like every run log):
the command, the MCP configuration, the prompt (packet), every tool call with a truncated result and the images the
host received (sha256 and size; the image data itself is not copied into the log), the host's text, the final
result (turns, usage, the model the CLI reports, the host plan's cost figure), the run id of the submission, its
statuses, which crops were read, and the elapsed time. The orchestrator lock on the addendum is held for the session
(route host) and released by the submission, or here when the session ends without one.

The model is the host's: requested with --model when configured, and recorded as the CLI reports it (system init and
modelUsage); the host also declares it in submit_proposals. The controller validates the submitted set exactly as an
API run's (controller.submit); nothing is approved or accepted.

Session 11 (the request layer, tenderpack/ai/requests.py; every phase on the host route goes through it):
  * failure classes: every session's result is classified (`classify`): `setup` (session 13, E159) when the CLI's
    init message says the tenderpack MCP server did not connect or the host offers none of the session's tools (the
    session had no tools; its final text is never an answer; requests.call_host does not retry it); `rate_limit` when the CLI reports
    api_error_status 429 or a rate/session/usage-limit message (blind-04: "You've hit your session limit · resets
    4:30pm (UTC)", is_error true, terminal_reason api_error), with the reset time it names when it names one;
    `provider` when the CLI cannot start, times out, exits without a result, or reports another API error; None when
    the session ended normally (its answer is then parsed and validated; a malformed one is repaired once).
  * declared capabilities (`HostSession.capabilities`): the host's model, context and modalities cannot be verified by
    this tool; config/ai.yaml `host_session.capabilities` states them with their basis, and every use carries a route
    notice saying they are declared, not verified (run log, checkpoint, review packet).
  * AnswerSession: a tool session whose FINAL MESSAGE is the answer (the readings and downstream phases; it submits
    nothing). PlainSession: a session with no tools at all (`--tools ""`, `--output-format json`, optionally
    `--json-schema`): the critic and the bounded repair of a malformed answer.
"""
from __future__ import annotations

import base64
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

from . import budget as B
from . import config as C
from .runlog import RunLog, truncate

TOOL_PREFIX = "mcp__tenderpack__"
# session 13: deny-by-default. A session is allowed exactly its phase's tools (policy.tools: the read-only tools, plus
# submit_proposals for the analysis session); every other tenderpack tool is disallowed by name and its MCP server
# offers only the allowed ones (serve-mcp --tools). DISALLOWED names the writers no session may ever call.
DISALLOWED = ("get_task_packet", "request_review")


def _host_rules() -> str:
    from . import policy
    return "\n" + policy.mechanics("analysis", "host")


HOST_RULES = _host_rules()          # the host-submit mechanics of the runtime policy (80_routes.md), for reference


# session 13: the reply-format rule of a phase's system prompt ("N. When you have finished, reply with ONLY the JSON ..."),
# found by what it says, never by its number
_REPLY_RULE = re.compile(r"^\d+\. When you have finished, reply with ONLY the JSON\b.*$\n?", re.M)


def compose_host_system(system: str, rules: str, *, submits: bool) -> str:
    """The system prompt of a host session, composed in ONE place for every host phase (session 13).

    `submits`: the session answers through a tool (the analysis phase: submit_proposals), so the phase's reply-format
    rule is replaced by the host rules and EVERY other rule stands (the no_effect safeguard, rule 9 of controller.SYSTEM,
    included); a system without exactly one reply-format rule is refused (ValueError), never guessed. Otherwise (an
    answer session: readings, downstream; the final message is the answer) every rule stands and the host rules are
    appended. The critic's plain session has no host rules: its system is its own."""
    if submits:
        hits = list(_REPLY_RULE.finditer(system))
        if len(hits) != 1:
            raise ValueError(f"the system prompt has {len(hits)} reply-format rule(s) ('N. When you have finished, reply "
                             "with ONLY the JSON ...'): exactly one is replaced by the host rules")
        system = (system[:hits[0].start()] + system[hits[0].end():]).rstrip("\n")
    return system + ("\n" + rules if rules else "")


@dataclass
class SessionResult:
    run_id: str
    addendum: str
    provisions: list[str]
    started: str
    elapsed_s: float = 0.0
    exit_code: int | None = None
    timed_out: bool = False
    error: str | None = None
    model_requested: str | None = None
    model_reported: list[str] = field(default_factory=list)
    tool_calls: list[dict] = field(default_factory=list)
    crops_read: list[str] = field(default_factory=list)
    images_received: list[dict] = field(default_factory=list)
    submission: dict | None = None
    statuses: dict = field(default_factory=dict)
    num_turns: int | None = None
    usage: dict | None = None
    host_plan_cost_usd: float | None = None
    final_text: str = ""
    run_dir: str = ""
    api_error_status: int | None = None         # the CLI's result message (e.g. 429 on a plan's session limit)
    terminal_reason: str | None = None
    failure_class: str | None = None            # refused | setup | rate_limit | provider | None (see classify)
    mcp_servers: list = field(default_factory=list)   # session 13 (E159): the CLI's init message, server by status
    reset_in_s: float | None = None             # seconds until the reset time a rate-limit message names, if any
    structured_output: object = None            # PlainSession with --json-schema: the CLI's structured_output

    def to_dict(self) -> dict:
        return asdict(self)


RATE_LIMIT_RE = re.compile(r"\b429\b|rate[ _-]?limit|too many requests|session limit|usage limit|hit your (?:\w+ )?limit",
                           re.I)
_RESET_RE = re.compile(r"resets?\s+(?:at\s+)?(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\s*\(?(UTC|GMT)\)?", re.I)
_RETRY_IN_RE = re.compile(r"(?:try again|retry)\s+(?:in|after)\s+(\d+(?:\.\d+)?)\s*(s|sec|seconds?|m|min|minutes?)\b",
                          re.I)


def reset_seconds(text: str, now: dt.datetime | None = None) -> float | None:
    """Seconds until the reset a rate-limit message names ('resets 4:30pm (UTC)', 'try again in 20 s'); None when it
    names none (or names a time zone other than UTC, which this tool does not guess)."""
    now = now or _now()
    m = _RETRY_IN_RE.search(text or "")
    if m:
        v = float(m.group(1))
        return v * 60 if m.group(2).lower().startswith("m") else v
    m = _RESET_RE.search(text or "")
    if not m:
        return None
    h, mi, ap = int(m.group(1)), int(m.group(2) or 0), (m.group(3) or "").lower()
    if ap == "pm" and h < 12:
        h += 12
    elif ap == "am" and h == 12:
        h = 0
    if h > 23 or mi > 59:
        return None
    t = now.replace(hour=h, minute=mi, second=0, microsecond=0)
    if t <= now:
        t += dt.timedelta(days=1)
    return round((t - now).total_seconds(), 1)


SETUP_ERROR = "the tenderpack MCP server "      # the prefix every setup failure's error starts with (classify)


def _mcp_cli_stderr(run_dir: Path) -> str:
    """What the host CLI logged from the MCP server's stderr for a session started in `run_dir` (best effort: the
    CLI keeps ~/.cache/claude-cli-nodejs/<cwd>/mcp-logs-<server>/*.jsonl, each line with the cwd); "" when none."""
    try:
        base = Path.home() / ".cache" / "claude-cli-nodejs"
        if not base.is_dir():
            return ""
        want = str(run_dir)
        found: list[str] = []
        for f in sorted(base.glob("*/mcp-logs-tenderpack/*.jsonl"), key=lambda x: x.stat().st_mtime, reverse=True)[:40]:
            try:
                lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            if not any(want in ln for ln in lines[:3]):
                continue
            for ln in lines:
                try:
                    d = json.loads(ln)
                except ValueError:
                    continue
                if d.get("cwd") != want:
                    continue
                msg = str(d.get("error") or d.get("debug") or "")
                if "stderr" in msg.lower():
                    found.append(msg.split(":", 1)[1].strip() if msg.lower().startswith("server stderr:") else msg)
            if found:
                break
        return " | ".join(dict.fromkeys(x.strip() for x in found if x.strip()))[:600]
    except Exception:                                    # a diagnostic only; never a second failure
        return ""


def classify(res: SessionResult, stderr: str = "") -> str | None:
    """The failure class of a finished session (see the module docstring); sets res.failure_class and res.reset_in_s."""
    text = " ".join(x for x in (res.final_text, res.error or "", stderr[-2000:]) if x)
    cls = None
    if (res.error or "").startswith("refused:"):
        cls = "refused"                                   # session 11 (E135): a local refusal (a lock), never an answer
    elif (res.error or "").startswith(SETUP_ERROR):
        cls = "setup"                                     # session 13 (E159): the session had no tools; never an answer
    elif res.api_error_status == 429 or (res.error and RATE_LIMIT_RE.search(text)):
        cls = "rate_limit"
    elif res.timed_out or res.exit_code is None and res.error or (res.error or "").startswith("the host CLI could not"):
        cls = "provider"
    elif res.api_error_status is not None or res.terminal_reason == "api_error":
        cls = "provider"
    elif res.exit_code not in (0, None) and not res.final_text and not res.submission:
        cls = "provider"
    res.failure_class = cls
    res.reset_in_s = reset_seconds(text) if cls == "rate_limit" else None
    return cls


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def settings(cfg: dict) -> dict:
    s = dict(cfg.get("host_session") or {})
    s.setdefault("claude_bin", "claude")
    s.setdefault("max_turns", 40)
    s.setdefault("timeout_s", 900)
    s.setdefault("model", None)
    s.setdefault("output_format", "stream-json")
    return s


_LIVE: set = set()                     # session 13 (D): the host CLI processes running now (run_tracked)
_LIVE_LOCK = threading.Lock()
STOP = threading.Event()               # session 13 (E161): set by terminate_live(): the run is stopping; no new host
                                       # session is started and no failed one is asked again (the workers' retries
                                       # restarted the sessions a SIGTERM had just killed, and the run could not end)
STOPPING = "refused: the run is stopping (interrupted); no new host session is started"


def stopping() -> bool:
    return STOP.is_set()


def reset_stop() -> None:
    """A new run in this process (the workflow installs its signal handler; tests)."""
    STOP.clear()


def run_tracked(cmd, *, input=None, capture_output=True, text=True, timeout=None, cwd=None):
    """subprocess.run's contract (a CompletedProcess; TimeoutExpired after the child is killed), with the child
    registered while it runs so that terminate_live() can stop it when the orchestrator is interrupted (session 13: a
    SIGTERM stops the run promptly; a session that already submitted is reused on resume, one that had not is asked
    again). The process is the same guarded host CLI command; nothing else is started here."""
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE if capture_output else None,
                         stderr=subprocess.PIPE if capture_output else None, text=text, cwd=cwd)
    with _LIVE_LOCK:
        _LIVE.add(p)
    try:
        try:
            out, err = p.communicate(input, timeout=timeout)
        except subprocess.TimeoutExpired:
            p.kill()
            out, err = p.communicate()
            raise subprocess.TimeoutExpired(cmd, timeout, output=out, stderr=err) from None
        except BaseException:
            p.kill()
            p.wait()
            raise
        return subprocess.CompletedProcess(cmd, p.returncode, out, err)
    finally:
        with _LIVE_LOCK:
            _LIVE.discard(p)


def terminate_live(grace_s: float = 5.0) -> int:
    """Stop every host CLI process started by run_tracked that is still running (the orchestrator was interrupted).
    Returns how many were stopped. Sets STOP first (E161): a worker whose session this kills sees a provider failure
    and would ask again; with STOP set, call_host raises instead and run_batch refuses to start."""
    STOP.set()
    with _LIVE_LOCK:
        procs = [p for p in _LIVE if p.poll() is None]
    for p in procs:
        try:
            p.terminate()
        except OSError:
            pass
    t0 = time.monotonic()
    for p in procs:
        try:
            p.wait(timeout=max(0.1, grace_s - (time.monotonic() - t0)))
        except subprocess.TimeoutExpired:
            p.kill()
        except OSError:
            pass
    return len(procs)


class HostSession:
    def __init__(self, ws, cfg: dict | None = None, *, model: str | None = None, max_turns: int | None = None,
                 timeout_s: float | None = None, claude_bin: str | None = None, runner=None,
                 python: str | None = None, run_lock: bool = False):
        self.ws = ws
        self.run_lock = bool(run_lock)          # session 12: the workflow run holds the addendum's lock for the run
        self.cfg = cfg or C.load(ws.ai_config)
        from .offline import check_host_session
        check_host_session(self.cfg, f"a host session ({type(self).__name__})")   # session 12: before any process
        s = settings(self.cfg)
        self.model = model if model is not None else s["model"]
        self.max_turns = int(max_turns or s["max_turns"])
        self.timeout_s = float(timeout_s or s["timeout_s"])
        self.claude_bin = claude_bin or s["claude_bin"]
        self.output_format = s["output_format"]
        self.runner = runner or run_tracked           # session 13 (D): stoppable when the orchestrator is interrupted
        self.python = python or sys.executable
        self.last: SessionResult | None = None
        self.require_crops: list[str] = []      # session 13: set from the packet's image_targets by run_batch
        self.submission_record: Path | None = None    # session 13 (D): the workflow batch's submission record file

    @staticmethod
    def takes_lock(run_lock: bool) -> bool:
        """Session 12: a session takes the addendum's lock itself unless the run holds it (batches at once: ONE lock
        per run, never one per session; a submission does not release a run's lock, controller.releases_host_lock)."""
        return not run_lock

    # ------------------------------------------------------------------ pieces
    PHASE = "analysis"
    SUBMIT_ONCE = True              # session 13: a second submission in the session is refused (HOST_RULES D)

    def allowed_tools(self) -> list[str]:
        """Exactly the tools of this session's phase (policy.tools; deny-by-default)."""
        from . import policy
        return list(policy.tools(self.PHASE, "host"))

    def mcp_config(self) -> dict:
        ws = self.ws
        args = ["-m", "tenderpack", "ai", "serve-mcp", "--evidence", str(Path(ws.evidence).resolve()),
                "--pack", str(Path(ws.pack).resolve()), "--out", str(Path(ws.staging).resolve()),
                "--worklog", str(Path(ws.worklog).resolve())]
        if ws.ai_config:
            args += ["--config", str(Path(ws.ai_config).resolve())]
        # session 13: the server offers only this session's tools, accepts one submission, and refuses the submission
        # until every image target's crop was fetched (HOST_RULES B and D in code, not only in the prompt)
        args += ["--tools", ",".join(self.allowed_tools())]
        if self.SUBMIT_ONCE and "submit_proposals" in self.allowed_tools():
            args.append("--submit-once")
        if getattr(self, "require_crops", None) and "submit_proposals" in self.allowed_tools():
            args += ["--require-crops", ",".join(self.require_crops)]
        if getattr(self, "submission_record", None) and "submit_proposals" in self.allowed_tools():
            args += ["--submission-record", str(Path(self.submission_record).resolve())]     # session 13 (D)
        # session 13 (E159): the host CLI merges `env` into the server's environment and IGNORES `cwd` (it starts the
        # server in the session folder); the folder on PYTHONPATH makes `-m tenderpack` import from the folder wherever
        # the server starts (the interview folder's .venv does not install the package). `cwd` is kept for clients
        # that honour it.
        root = str(Path(ws.root).resolve())
        had = os.environ.get("PYTHONPATH")
        env = {"PYTHONPATH": root + (os.pathsep + had if had else "")}
        return {"mcpServers": {"tenderpack": {"command": self.python, "args": args, "cwd": str(ws.root), "env": env}}}

    def system_prompt(self) -> str:
        """The runtime policy for the analysis phase on the host route (policy.compose: hostsession.compose_host_system
        replaces the reply-format rule with the host-submit rules; rules 1-9 stand)."""
        from . import policy
        return policy.compose("analysis", "host", cfg=getattr(self, "cfg", None))

    def command(self, mcp_path: Path) -> list[str]:
        from .tools import TOOLS
        allowed = self.allowed_tools()
        cmd = [self.claude_bin, "-p", "--mcp-config", str(mcp_path), "--strict-mcp-config", "--tools", "",
               "--allowedTools", ",".join(TOOL_PREFIX + t for t in allowed),
               "--disallowedTools", ",".join(TOOL_PREFIX + t for t in TOOLS if t not in allowed),
               "--permission-prompts", "none", "--no-session-persistence",
               "--output-format", self.output_format, "--max-turns", str(self.max_turns),
               "--system-prompt", self.system_prompt()]
        if self.output_format == "stream-json":
            cmd.append("--verbose")
        if self.model:
            cmd += ["--model", str(self.model)]
        return cmd

    def host_model_label(self) -> str:
        return (f"claude-code headless ({self.model})" if self.model else
                "claude-code headless (the CLI's default model; recorded from the CLI output)")

    def capabilities(self):
        """The host's capabilities as DECLARED in config/ai.yaml host_session.capabilities (this tool cannot verify a
        host's model): image input and tool use as observed in real host sessions, the context window and output cap
        the request accounting is held to. The source says so; the request layer adds a route notice."""
        return declared_capabilities(self.cfg)

    def prompt(self, packet: dict) -> str:
        from .providers.recorded import PACKET_MARK
        pub = dict(packet)
        pub["crops"] = [{k: v for k, v in c.items() if not k.startswith("_")} for c in packet.get("crops") or []]
        pub.pop("system", None)
        return (f"host_model value for submit_proposals: {self.host_model_label()!r}\n\n"
                + PACKET_MARK + json.dumps(pub, ensure_ascii=False))

    # ------------------------------------------------------------------ the run
    def run_batch(self, packet: dict) -> dict:
        """Run one headless session on `packet` (controller.task_packet, optionally with `image_targets`); return the
        proposal set the controller validated and staged (or, when nothing was submitted, an empty set with status
        provider_failed). Details of the session are on `self.last`."""
        from .controller import make_run_id
        ws, addendum = self.ws, packet["addendum"]
        staging = B.safe_staging(ws.staging, ws.root, ws.evidence)
        run_id = B.check_run_id(make_run_id(addendum, "hostsession"))
        run_dir = staging / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        provs = [p["unit_id"] for p in packet.get("provisions") or []]
        res = SessionResult(run_id=run_id, addendum=addendum, provisions=provs, started=_now().isoformat(),
                            model_requested=self.model, run_dir=str(run_dir))
        self.last = res
        self.require_crops = [str(u) for u in packet.get("image_targets") or []]
        log = RunLog(run_id, [Path(ws.worklog) / f"{run_id}.jsonl", run_dir / "log.jsonl"])
        mcp_path = run_dir / "mcp.json"
        mcp_path.write_text(json.dumps(self.mcp_config(), indent=1), encoding="utf-8")
        cmd = self.command(mcp_path)
        prompt = self.prompt(packet)
        (run_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
        log.event("start", route="host", provider="host-session", via="claude -p (headless) over MCP",
                  model_requested=self.model or "the CLI's default", addendum=addendum, provisions=provs,
                  command=[c if len(c) < 400 else c[:200] + f"... [{len(c)} characters]" for c in cmd],
                  mcp_config=self.mcp_config(), max_turns=self.max_turns, timeout_s=self.timeout_s,
                  note="the host's own plan pays; nothing is added to the application's spend meter")
        log.event("prompt", system=self.system_prompt(), prompt=prompt)
        lock = None
        if STOP.is_set():                                   # session 13 (E161): the run is stopping
            res.error = STOPPING
            classify(res)
            log.event("refused", reason=STOPPING, failure_class=res.failure_class)
            return self._finish(log, packet, res, None)
        try:
            if self.takes_lock(self.run_lock):
                lock = B.acquire(staging, addendum, {"route": "host", "run_id": run_id, "pid": os.getpid(),
                                                     "model": self.host_model_label()},
                                 self.cfg.get("lock_stale_after_min", 120))
        except B.Refused as e:
            res.error = f"refused: {e}"
            classify(res)                                 # session 11 (E135): failure_class "refused", never an answer
            log.event("refused", reason=str(e), failure_class=res.failure_class)
            return self._finish(log, packet, res, None)
        mcp_logs_before = set(Path(ws.worklog).glob("mcp-*.jsonl")) if Path(ws.worklog).is_dir() else set()
        t0 = time.monotonic()
        stdout = ""
        try:
            if not shutil.which(self.claude_bin) and not Path(self.claude_bin).exists():
                raise FileNotFoundError(f"{self.claude_bin} not found")
            p = self.runner(cmd, input=prompt, capture_output=True, text=True, timeout=self.timeout_s, cwd=str(run_dir))
            res.exit_code, stdout = p.returncode, p.stdout or ""
            if p.stderr:
                (run_dir / "stderr.txt").write_text(p.stderr[-20000:], encoding="utf-8")
        except subprocess.TimeoutExpired as e:
            res.timed_out, res.error = True, f"timed out after {self.timeout_s:g} s"
            stdout = (e.stdout.decode() if isinstance(e.stdout, bytes) else e.stdout) or ""
        except (OSError, FileNotFoundError) as e:
            res.error = f"the host CLI could not be started: {e}"
        finally:
            res.elapsed_s = round(time.monotonic() - t0, 1)
            if lock is not None:
                lock.release()          # no-op when the submission already released it (route host)
        self._parse(stdout, res, log, run_dir)
        err_path = run_dir / "stderr.txt"
        classify(res, err_path.read_text(encoding="utf-8") if err_path.exists() else "")
        if res.failure_class:
            log.event("failure_class", failure_class=res.failure_class, api_error_status=res.api_error_status,
                      terminal_reason=res.terminal_reason, reset_in_s=res.reset_in_s, error=res.error,
                      result=truncate(res.final_text, 500))
        new_logs = sorted(set(Path(ws.worklog).glob("mcp-*.jsonl")) - mcp_logs_before) if Path(ws.worklog).is_dir() else []
        if new_logs:
            log.event("mcp_server_log", files=[str(x) for x in new_logs])
        return self._finish(log, packet, res, stdout)

    # ------------------------------------------------------------------ transcript
    def _parse(self, stdout: str, res: SessionResult, log: RunLog, run_dir: Path) -> None:
        msgs = []
        for line in stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                msgs.append(json.loads(line))
            except ValueError:
                continue
        pending: dict[str, dict] = {}
        kept = []
        for m in msgs:
            t = m.get("type")
            if t == "system" and m.get("subtype") == "init":
                if m.get("model"):
                    res.model_reported.append(str(m["model"]))
                log.event("host_init", model=m.get("model"), tools=m.get("tools"), mcp_servers=m.get("mcp_servers"),
                          permission_mode=m.get("permissionMode"))
                self._judge_init(m, res, run_dir)
            elif t in ("assistant", "user"):
                for b in (m.get("message") or {}).get("content") or []:
                    if not isinstance(b, dict):
                        continue
                    if b.get("type") == "tool_use":
                        call = {"id": b.get("id"), "name": str(b.get("name", "")).removeprefix(TOOL_PREFIX),
                                "arguments": b.get("input")}
                        pending[b.get("id")] = call
                        res.tool_calls.append(call)
                    elif b.get("type") == "tool_result":
                        self._tool_result(b, pending.get(b.get("tool_use_id")) or {}, res, log)
                    elif b.get("type") == "text" and t == "assistant":
                        log.event("host_text", text=b.get("text"))
            elif t == "result":
                res.num_turns = m.get("num_turns")
                res.usage = m.get("usage")
                res.host_plan_cost_usd = m.get("total_cost_usd")
                res.final_text = str(m.get("result") or "")
                res.api_error_status = m.get("api_error_status") if isinstance(m.get("api_error_status"), int) else None
                res.terminal_reason = m.get("terminal_reason")
                if m.get("structured_output") is not None:
                    res.structured_output = m.get("structured_output")
                for k in (m.get("modelUsage") or {}):
                    if k not in res.model_reported:
                        res.model_reported.append(k)
                if m.get("is_error") and not res.error:
                    res.error = f"the host ended with an error ({m.get('subtype')}: {m.get('api_error_status')})"
                log.event("host_result", subtype=m.get("subtype"), is_error=m.get("is_error"), num_turns=res.num_turns,
                          usage=res.usage, model_usage=m.get("modelUsage"), result=res.final_text,
                          host_plan_cost_usd=res.host_plan_cost_usd, permission_denials=m.get("permission_denials"),
                          note="total_cost_usd is the host's own plan usage, not the application's spend")
            kept.append(_strip_images(m))
        (run_dir / "transcript.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in kept) + "\n",
                                                  encoding="utf-8")

    def _judge_init(self, m: dict, res: SessionResult, run_dir: Path) -> None:
        """Session 13 (E159): a session whose MCP server did not connect, or whose host offers none of this session's
        tools, cannot do its task; its final message is then a tool-less model's text (blind-07: tool-call markup
        written as text), never an answer. The error names the cause (the server's stderr when the CLI logged it) and
        classify() makes it a `setup` failure. An init message without the servers' statuses is not judged."""
        servers = m.get("mcp_servers")
        if not isinstance(servers, list) or not servers:
            return
        res.mcp_servers = [dict(x) for x in servers if isinstance(x, dict)]
        mine = next((x for x in res.mcp_servers if x.get("name") == "tenderpack"), None)
        if mine is None:
            res.error = res.error or f"{SETUP_ERROR}is not among the host's servers ({res.mcp_servers})"
            return
        if mine.get("status") is None:
            return                                           # no status reported (a stand-in): not judged
        if mine.get("status") != "connected":
            why = _mcp_cli_stderr(run_dir)
            res.error = res.error or (f"{SETUP_ERROR}did not connect (status {mine.get('status')}): "
                                      f"{why or 'the host CLI logged no server stderr'}")
            return
        offered = m.get("tools")
        # the CLI lists the MCP tools it offers (mcp__<server>__<tool>); judged only when it lists some MCP tool at
        # all (a CLI or stand-in that lists none is not judged on this: the server's status decided above)
        if isinstance(offered, list) and any(str(t).startswith("mcp__") for t in offered):
            wanted = [TOOL_PREFIX + t for t in self.allowed_tools()]
            if wanted and not any(t in offered for t in wanted):
                res.error = res.error or (f"{SETUP_ERROR}connected but the host offered none of this session's tools "
                                          f"({', '.join(wanted)}); offered: {', '.join(map(str, offered)) or 'none'}")

    def _tool_result(self, b: dict, call: dict, res: SessionResult, log: RunLog) -> None:
        content = b.get("content")
        parts = content if isinstance(content, list) else [{"type": "text", "text": str(content or "")}]
        text = "\n".join(p.get("text", "") for p in parts if isinstance(p, dict) and p.get("type") == "text")
        images = []
        for p in parts:
            if isinstance(p, dict) and p.get("type") == "image":
                src = p.get("source") or {}
                data = src.get("data") or p.get("data") or ""
                raw = base64.b64decode(data) if data else b""
                images.append({"media_type": src.get("media_type") or p.get("mimeType"), "bytes": len(raw),
                               "sha256": hashlib.sha256(raw).hexdigest()})
        name = call.get("name", "")
        if name == "get_crop" and not b.get("is_error"):
            uid = (call.get("arguments") or {}).get("unit_id")
            if uid and uid not in res.crops_read:
                res.crops_read.append(uid)
            try:
                sent = [x for x in json.loads(text).get("images_attached") or [] if x.get("attached")]
            except (ValueError, AttributeError):
                sent = []
            # what the server sent (crop files, by sha256) and what reached the host's model (the host CLI may
            # re-encode a large image, so a received sha256 can differ from the file's)
            res.images_received.append({"unit_id": uid, "sent": sent, "received": images})
        if name == "submit_proposals" and not b.get("is_error"):
            try:
                sub = json.loads(text)
                if isinstance(sub, dict) and sub.get("run_id"):
                    res.submission = sub
            except ValueError:
                pass
        call["ok"] = not b.get("is_error")
        call["images"] = len(images)
        log.event("tool_call", id=call.get("id"), name=name, arguments=call.get("arguments"), ok=call["ok"],
                  result=truncate(text, 4000), images=images)

    # ------------------------------------------------------------------ the set
    def _finish(self, log: RunLog, packet: dict, res: SessionResult, stdout) -> dict:
        from .contract import ProposalSet
        ps_dict = None
        if res.submission and res.submission.get("staging"):
            f = Path(res.submission["staging"]) / "proposals.yaml"
            if f.exists():
                ps_dict = (yaml.safe_load(f.read_text(encoding="utf-8")) or {}).get("proposal_set")
        if ps_dict is not None:
            res.statuses = {it["id"]: it.get("verification_status") for it in ps_dict.get("items") or []}
        else:
            if not res.error:
                res.error = "the host did not submit a proposal set through submit_proposals"
            from .contract import Coverage
            from .controller import _provisions
            ws = self.ws
            provs = _provisions(ws, res.addendum)
            ps = ProposalSet(run_id=res.run_id, created=res.started[:19] + "Z", route="host", provider="host-session",
                             model_requested=self.host_model_label(),
                             model_reported=", ".join(res.model_reported) or None, task="propose_amendment",
                             addendum=res.addendum, state=ws.identity(), status="provider_failed",
                             coverage=Coverage(provisions_total=len(provs), accounted=0, unaccounted=provs))
            ps_dict = ps.model_dump(mode="json")
        if packet.get("image_targets") and not res.crops_read:
            log.event("warning", message="the packet names image targets but the host read no crop through get_crop",
                      image_targets=packet.get("image_targets"))
        summary = {k: v for k, v in res.to_dict().items() if k != "final_text"}
        log.event("end", **summary)
        (Path(res.run_dir) / "session.json").write_text(json.dumps(res.to_dict(), indent=1, ensure_ascii=False,
                                                                   default=str), encoding="utf-8")
        return ps_dict


def _strip_images(m):
    """A transcript message with image data replaced by its sha256 and size (the crops stay in the evidence build)."""
    if isinstance(m, dict):
        if m.get("type") == "image":
            src = m.get("source") or {}
            data = src.get("data") or m.get("data")
            if isinstance(data, str):
                raw = base64.b64decode(data)
                return {"type": "image", "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                        "data": "[image data not copied]"}
        return {k: _strip_images(v) for k, v in m.items()}
    if isinstance(m, list):
        return [_strip_images(x) for x in m]
    return m


def image_targets(ws, packet: dict) -> list[str]:
    """Candidate targets of the packet's provisions that are read from an image (their crops are worth reading)."""
    out = []
    for p in packet.get("provisions") or []:
        for c in p.get("candidate_targets") or []:
            t = c.get("target")
            u = ws.units_by_id.get(t) if t else None
            if u and (u.get("origin") == "image_reading" or u.get("region")) and t not in out:
                out.append(t)
    return out


def host_packet(ws, addendum: str, provisions: list[str] | None = None) -> dict:
    """The task packet for a host session: controller.task_packet plus the image targets to read with get_crop."""
    from .controller import task_packet
    ws.refresh()
    pk = task_packet(ws, addendum, provisions)
    pk["image_targets"] = image_targets(ws, pk)
    return pk


# ---------------------------------------------------------------------------------------------- session 11

DECLARED_SOURCE = ("config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model "
                   "cannot be queried; image input and tool use as observed in real host sessions)")


def declared_capabilities(cfg: dict):
    """The host route's capabilities as declared in config/ai.yaml `host_session.capabilities` (see HostSession)."""
    from .providers.base import Capabilities
    d = dict((cfg.get("host_session") or {}).get("capabilities") or {})
    return Capabilities(images=d.get("images"), tools=d.get("tools", True), structured_output=False,
                        context_tokens=d.get("context_tokens"), max_output_tokens=d.get("max_output_tokens"),
                        retention="the coding host's own policy; not verified by this tool",
                        source=DECLARED_SOURCE + (f"; basis: {d['basis']}" if d.get("basis") else ""),
                        details={"declared": True, "unverified": True})


class AnswerSession(HostSession):
    """A tool session whose FINAL MESSAGE is the answer (readings, downstream): it submits nothing. Session 13: built
    for a `phase` (reading | downstream), its system prompt is the runtime policy's composition for that phase on the
    host route (policy.compose: every rule stands, the host-answer mechanics appended) and its tools are the phase's
    (policy.tools; `tools` may narrow them, never add one). A `system` given instead must itself be a policy
    composition (policy.require_composed); there is no `rules` override any more."""
    PHASE = "downstream"

    def __init__(self, ws, cfg: dict | None = None, *, phase: str | None = None, system: str | None = None,
                 tools: list[str] | None = None, **kw):
        super().__init__(ws, cfg, **kw)                      # the offline check comes first (session 12)
        from . import policy
        if phase is None and system is None:
            raise ValueError("an answer session needs its phase (reading | downstream)")
        self.PHASE = phase or "downstream"
        self._phase = phase
        self._system = policy.compose(phase, "host", cfg=self.cfg) if system is None else \
            policy.require_composed(system, "an answer session's system prompt")
        self._rules = ""
        self._tools = list(policy.check_tools(self.PHASE, tools, "host")) if tools is not None else None

    def allowed_tools(self) -> list[str]:
        return list(self._tools) if self._tools is not None else super().allowed_tools()

    def system_prompt(self) -> str:
        return compose_host_system(self._system, self._rules, submits=False)   # session 13: one composition

    def prompt(self, packet: dict) -> str:
        from .providers.recorded import PACKET_MARK
        pub = {k: v for k, v in packet.items() if k != "system"}
        if "crops" in pub:
            pub["crops"] = [{k: v for k, v in c.items() if not k.startswith("_")} for c in pub.get("crops") or []]
        return PACKET_MARK + json.dumps(pub, ensure_ascii=False, default=str)

    def _finish(self, log, packet, res, stdout):               # no proposal set: the final message is the answer
        log.event("end", **{k: v for k, v in res.to_dict().items() if k != "final_text"},
                  note="an answer session submits nothing: its final message is the answer")
        (Path(res.run_dir) / "session.json").write_text(json.dumps(res.to_dict(), indent=1, ensure_ascii=False,
                                                                   default=str), encoding="utf-8")
        return {}


class PlainSession:
    """A headless call with NO tools (`claude -p --tools "" --strict-mcp-config --output-format json`), optionally
    constrained by `--json-schema`: the critic and the bounded repair of a malformed answer. Classified like a tool
    session (rate_limit / provider / None). Logged to `log` when given."""

    def __init__(self, cfg: dict, system: str, *, schema: dict | None = None, model: str | None = None,
                 timeout_s: float | None = None, max_turns: int | None = None, claude_bin: str | None = None,
                 runner=subprocess.run, label: str = "plain"):
        from .offline import check_host_session
        check_host_session(cfg, "critic" if label == "critic" else f"a plain host session ({label})")   # session 12
        from . import policy
        s = settings(cfg)
        self.cfg, self.schema = cfg, schema
        self.system = policy.require_composed(system, f"a plain host session's system prompt ({label})")   # session 13
        self.model = model if model is not None else s["model"]
        self.timeout_s = float(timeout_s or s.get("plain_timeout_s") or 300)
        self.max_turns = int(max_turns or 3)
        self.claude_bin = claude_bin or s["claude_bin"]
        self.runner, self.label = runner, label
        self.last: SessionResult | None = None

    def command(self) -> list[str]:
        cmd = [self.claude_bin, "-p", "--tools", "", "--strict-mcp-config", "--no-session-persistence",
               "--permission-prompts", "none", "--output-format", "json", "--max-turns", str(self.max_turns),
               "--system-prompt", self.system]
        if self.schema is not None:
            cmd += ["--json-schema", json.dumps(self.schema)]
        if self.model:
            cmd += ["--model", str(self.model)]
        return cmd

    def host_model_label(self) -> str:
        return (f"claude-code headless ({self.model})" if self.model else
                "claude-code headless (the CLI's default model; recorded from the CLI output)")

    def run(self, prompt: str, cwd: Path, log=None) -> SessionResult:
        res = SessionResult(run_id=f"{self.label}-{_now():%Y%m%dT%H%M%SZ}", addendum="", provisions=[],
                            started=_now().isoformat(), model_requested=self.model, run_dir=str(cwd))
        self.last = res
        t0 = time.monotonic()
        stdout = stderr = ""
        try:
            if STOP.is_set():                               # session 13 (E161): the run is stopping
                raise OSError(STOPPING)
            if not shutil.which(self.claude_bin) and not Path(self.claude_bin).exists():
                raise FileNotFoundError(f"{self.claude_bin} not found")
            p = self.runner(self.command(), input=prompt, capture_output=True, text=True, timeout=self.timeout_s,
                            cwd=str(cwd))
            res.exit_code, stdout, stderr = p.returncode, p.stdout or "", p.stderr or ""
        except subprocess.TimeoutExpired:
            res.timed_out, res.error = True, f"timed out after {self.timeout_s:g} s"
        except (OSError, FileNotFoundError) as e:
            res.error = f"the host CLI could not be started: {e}"
        res.elapsed_s = round(time.monotonic() - t0, 1)
        out = None
        for line in (stdout or "").splitlines()[::-1]:
            try:
                out = json.loads(line)
                break
            except ValueError:
                continue
        if isinstance(out, dict):
            res.final_text = str(out.get("result") or "")
            res.structured_output = out.get("structured_output")
            res.num_turns, res.usage = out.get("num_turns"), out.get("usage")
            res.host_plan_cost_usd = out.get("total_cost_usd")
            res.model_reported = list(out.get("modelUsage") or {})
            res.api_error_status = out.get("api_error_status") if isinstance(out.get("api_error_status"), int) else None
            res.terminal_reason = out.get("terminal_reason")
            if out.get("is_error") and not res.error:
                res.error = f"the host ended with an error ({out.get('subtype')}: {out.get('api_error_status')})"
        elif not res.error:
            res.error = f"the host CLI printed no JSON (exit {res.exit_code}): {(stdout or stderr)[:300]}"
        classify(res, stderr)
        if log is not None:
            log.event("plain_session", label=self.label, elapsed_s=res.elapsed_s, exit_code=res.exit_code,
                      error=res.error, failure_class=res.failure_class, api_error_status=res.api_error_status,
                      reset_in_s=res.reset_in_s, model_reported=res.model_reported, usage=res.usage,
                      host_plan_cost_usd=res.host_plan_cost_usd, result=truncate(res.final_text, 4000),
                      note="the host plan's figures; never the application's spend")
        return res
