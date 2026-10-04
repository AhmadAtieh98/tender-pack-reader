"""An ACTUAL host session (session 10, routes layer): a headless Claude Code run that works on a task packet ONLY through
the tenderpack MCP tools, reads image crops through them and submits through `submit_proposals`.

    HostSession(ws, cfg).run_batch(packet) -> proposal set dict      (the controller-validated, staged set)

The command (config/ai.yaml `host_session`; docs/AI_ROUTES.md):

    claude -p --mcp-config <run dir>/mcp.json --strict-mcp-config      the tenderpack server only:
              .venv/bin/python -m tenderpack ai serve-mcp --evidence <abs> --pack <abs> --out <staging> --worklog <log>
           --tools ""                                                  no built-in tool: no file, shell or web access
           --allowedTools "mcp__tenderpack__*"                         the MCP tools need no permission prompt
           --disallowedTools <get_task_packet, request_review>         the packet is given; submit_proposals submits
           --permission-prompts none                                   anything else that would prompt is denied
           --no-session-persistence --output-format stream-json --verbose   every message, tool call and tool result
           --max-turns N --system-prompt <the controller's rules + the host rules> [--model M]
    with the task packet on stdin, under a wall-clock timeout.

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
"""
from __future__ import annotations

import base64
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

from . import budget as B
from . import config as C
from .runlog import RunLog, truncate

TOOL_PREFIX = "mcp__tenderpack__"
DISALLOWED = ("get_task_packet", "request_review")
HOST_RULES = """
Host session rules (they replace rule 9 above):
A. You work ONLY through the tenderpack MCP tools. The task packet is below: do not call get_task_packet.
B. Where a provision changes, or relies on, a unit read from an image (the packet's `crops` and `image_targets`), call
   get_crop for that unit and LOOK at the image before you propose; say in the item's model_rationale what the image
   shows that you relied on (for example the row, the cell or the declaration and its script).
C. Check ops with simulate_amendment (and the whole set with validate_proposal) before submitting.
D. When the set is ready, submit it ONCE with submit_proposals(proposal_set=<the JSON object described by `schema`>,
   host_model=<the host_model value given below>). Do not reply with the JSON itself.
E. Then reply with one short line: the run_id and status the tool returned, and which crops you read."""


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

    def to_dict(self) -> dict:
        return asdict(self)


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


class HostSession:
    def __init__(self, ws, cfg: dict | None = None, *, model: str | None = None, max_turns: int | None = None,
                 timeout_s: float | None = None, claude_bin: str | None = None, runner=subprocess.run,
                 python: str | None = None):
        self.ws = ws
        self.cfg = cfg or C.load(ws.ai_config)
        s = settings(self.cfg)
        self.model = model if model is not None else s["model"]
        self.max_turns = int(max_turns or s["max_turns"])
        self.timeout_s = float(timeout_s or s["timeout_s"])
        self.claude_bin = claude_bin or s["claude_bin"]
        self.output_format = s["output_format"]
        self.runner = runner
        self.python = python or sys.executable
        self.last: SessionResult | None = None

    # ------------------------------------------------------------------ pieces
    def mcp_config(self) -> dict:
        ws = self.ws
        args = ["-m", "tenderpack", "ai", "serve-mcp", "--evidence", str(Path(ws.evidence).resolve()),
                "--pack", str(Path(ws.pack).resolve()), "--out", str(Path(ws.staging).resolve()),
                "--worklog", str(Path(ws.worklog).resolve())]
        if ws.ai_config:
            args += ["--config", str(Path(ws.ai_config).resolve())]
        return {"mcpServers": {"tenderpack": {"command": self.python, "args": args, "cwd": str(ws.root)}}}

    def system_prompt(self) -> str:
        from .controller import SYSTEM
        return SYSTEM + "\n" + HOST_RULES

    def command(self, mcp_path: Path) -> list[str]:
        cmd = [self.claude_bin, "-p", "--mcp-config", str(mcp_path), "--strict-mcp-config", "--tools", "",
               "--allowedTools", f"{TOOL_PREFIX}*",
               "--disallowedTools", ",".join(TOOL_PREFIX + t for t in DISALLOWED),
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
        try:
            lock = B.acquire(staging, addendum, {"route": "host", "run_id": run_id, "pid": os.getpid(),
                                                 "model": self.host_model_label()},
                             self.cfg.get("lock_stale_after_min", 120))
        except B.Refused as e:
            res.error = f"refused: {e}"
            log.event("refused", reason=str(e))
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
