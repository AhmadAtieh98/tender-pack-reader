"""A Model Context Protocol server over stdio (JSON-RPC 2.0, one JSON message per line), with no dependency beyond the
standard library: `python -m tenderpack ai serve-mcp [--evidence build --pack config/pack.yaml --out staging/ai]`.

It lets a coding host (Claude Code, Codex) use ITS OWN model with the same tools the application routes use:
  initialize                  echoes a supported protocolVersion ("2025-03-26" or "2024-11-05"; otherwise the latest)
  notifications/initialized   no response (a notification)
  ping                        {}
  tools/list                  every tool of tenderpack.ai.tools with its JSON input schema
  tools/call                  {name, arguments} -> {content: [{type: "text", text: <JSON>}], isError}
                              get_crop (session 10) also returns the images themselves, so a host model SEES the crop:
                              after the text block (the JSON with path, sha256 and `images_attached`), up to
                              MAX_IMAGES image content blocks {type: "image", data: <base64 PNG>, mimeType: "image/png"}
                              (the MCP ImageContent shape), the unit's own crops first, then cell crops, the region crop
                              and the native image; a file over MAX_IMAGE_BYTES is listed but not attached. Each image
                              sent is logged (sha256, bytes). get_region (the workflow's readings step) returns
                              the region's images the same way, in the order it lists them; so does
                              get_addendum_page (session 14: a quick review's NEW addendum pages and image regions,
                              served only by a server started with --addendum-scope)
Errors: parse error -32700, invalid request -32600, unknown method -32601, unknown tool or bad arguments -32602,
internal error -32603. A tool's own refusal (e.g. no such unit) is a result with isError true, as MCP specifies.

Every tool is read-only except get_task_packet with claim=true (the addendum's lock), request_review and
submit_proposals, which write to staging/ai only (never curation/). Session 13: a session the program starts runs the
server with `--tools` (only that session's tools are listed and run; deny-by-default), `--submit-once` (a second
submission is refused, the first stands) and `--require-crops` (submit_proposals is refused until get_crop was called
for each image target); `initialize` returns the runtime policy's short host entry (policy.host_entry). A workflow
batch's session also passes `--submission-record FILE`: a successful submit_proposals writes its run id, status and
staging folder there at once (it points at the staged set and decides nothing). Every call is logged to
worklog/model_calls/mcp-<session>.jsonl (arguments and a truncated result; secrets redacted). Anything the tools print
goes to stderr, so stdout carries only protocol messages.

Session 14 (W1): the submission gate's bounded repair. A submit_proposals whose inner payloads fail their full schema
(contract.submission_problems: a row_new that is not a register.Row, ...; a fact with no evidence) is staged as it is
and answered with `repair` (the exact errors and the full schemas); ONE re-submission of the named items only is then
accepted (even with --submit-once) and merged into the first (contract.merge_repair: every other item stands as first
submitted). It is staged as a new run that supersedes the first (`superseded.json` in the first's folder; the
submission record points at it). An item still failing after it is invalid with its errors.
"""
from __future__ import annotations

import contextlib
import datetime as dt
import json
import os
import sys
from pathlib import Path

SUPPORTED = ("2025-03-26", "2024-11-05")
SERVER_INFO = {"name": "tenderpack", "version": "s10-ai-1"}
MAX_IMAGES = 3
MAX_IMAGE_BYTES = 3_750_000
_CROP_ORDER = {"unit": 0, "cell": 1, "region_crop": 2, "native": 3}
# session 13: the coding hosts' entry text is the runtime policy's short host entry (tenderpack/ai/policy/
# 90_host_entry.md): it points to the runtime prompt the program supplies explicitly (the task packet's `system`, a
# session's --system-prompt) and is never a second copy of the rules
def _entry() -> str:
    from .ai.policy import host_entry
    return host_entry()


def _err(id_, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message}}


class Server:
    """`tools` (session 13): the only tools this server offers and runs (deny-by-default; None: every tool, for a
    person's own MCP client). `submit_once`: after one successful submit_proposals or request_review, a later one is
    refused and the first stands. `require_crops`: submit_proposals is refused until get_crop was called for each of
    these units (a program-run host session's image targets)."""

    def __init__(self, ws, log=None, *, tools=None, submit_once: bool = False, require_crops=(),
                 submission_record=None):
        self.ws, self.log = ws, log
        self.initialized = False
        self.tools = None if tools is None else list(tools)
        self.submit_once, self.require_crops = bool(submit_once), [str(u) for u in require_crops or ()]
        self.submitted: str | None = None
        # session 13: where a successful submit_proposals is recorded at once (atomically), so that a workflow batch
        # whose orchestrator is killed after the submission finds its staged set on resume (workflow._reuse_submission)
        self.submission_record = Path(submission_record) if submission_record else None
        self.crops_called: set[str] = set()
        # session 14 (W1, blind-07 defect 1): the submission gate's bounded repair. A submission whose inner payloads
        # fail their full schema (or that states a fact with no evidence) is STAGED as it is (never lost) and answered
        # with a repair request naming the failing items, their exact errors and their full schemas; ONE re-submission
        # of those items only is then accepted (despite --submit-once) and merged into the first: every other item stands
        # exactly as first submitted. The bound is the failure policy's (config/ai.yaml failures.malformed.repairs, <= 1).
        self.repairs_left: int | None = None
        self._repair: dict | None = None

    def _offered(self, name: str) -> bool:
        return self.tools is None or name in self.tools

    def _guard(self, name: str, args: dict) -> str | None:
        """Why this call is refused by the session's permissions (session 13), or None."""
        if name in ("submit_proposals", "request_review"):
            if self.submit_once and self.submitted and not (name == "submit_proposals" and self._repair is not None):
                return (f"refused: this session already submitted ({self.submitted}); a session submits ONCE and the "
                        "first submission stands")
            missing = [u for u in self.require_crops if u not in self.crops_called]
            if name == "submit_proposals" and missing:
                return ("refused: look at the image targets first: call get_crop for " + ", ".join(missing)
                        + " and say in model_rationale what the image shows, then submit")
        return None

    def _log(self, **kw) -> None:
        if self.log:
            self.log.event("mcp", **kw)

    def handle(self, msg) -> dict | list | None:
        if isinstance(msg, list):                                 # a JSON-RPC batch
            if not msg:
                return _err(None, -32600, "empty batch")
            out = [r for r in (self.handle(m) for m in msg) if r is not None]
            return out or None
        if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0" or not isinstance(msg.get("method"), str):
            return _err(msg.get("id") if isinstance(msg, dict) else None, -32600, "invalid request")
        id_, method, params = msg.get("id"), msg["method"], msg.get("params") or {}
        is_note = "id" not in msg
        if method == "notifications/initialized" or (is_note and method.startswith("notifications/")):
            self.initialized = True if method == "notifications/initialized" else self.initialized
            return None
        if is_note:
            return None
        if method == "initialize":
            v = params.get("protocolVersion")
            return {"jsonrpc": "2.0", "id": id_, "result": {
                "protocolVersion": v if v in SUPPORTED else SUPPORTED[0],
                "capabilities": {"tools": {"listChanged": False}}, "serverInfo": SERVER_INFO,
                "instructions": _entry()}}
        if method == "ping":
            return {"jsonrpc": "2.0", "id": id_, "result": {}}
        if method == "tools/list":
            from .ai.tools import TOOLS
            return {"jsonrpc": "2.0", "id": id_, "result": {"tools": [
                {"name": t.name, "description": t.description + (" (writes to staging only)" if t.writes else " (read-only)"),
                 "inputSchema": t.input_schema} for t in TOOLS.values() if self._offered(t.name)]}}
        if method == "tools/call":
            return self._call(id_, params)
        return _err(id_, -32601, f"method not found: {method}")

    def _call(self, id_, params: dict) -> dict:
        from .ai.budget import Refused
        from .ai.tools import TOOLS, ToolError, check_args
        from .ai import tools as T
        name, args = params.get("name"), params.get("arguments") or {}
        if name not in TOOLS or not self._offered(name):
            self._log(tool=name, refused="not offered to this session")
            return _err(id_, -32602, f"unknown tool: {name}" + ("" if name not in TOOLS else
                                                                " (not offered to this session)"))
        try:
            check_args(TOOLS[name].input_schema, args)
        except ToolError as e:
            return _err(id_, -32602, f"invalid arguments for {name}: {e}")
        why = self._guard(name, args)
        if why:
            self._log(tool=name, arguments=args, is_error=True, refused=why)
            return {"jsonrpc": "2.0", "id": id_, "result": {"content": [{"type": "text", "text": json.dumps(
                {"error": why}, ensure_ascii=False)}], "isError": True}}
        if name == "get_crop":
            self.crops_called.add(str(args.get("unit_id")))
        gate = None
        try:
            if name == "submit_proposals":
                args, gate = self._submission_gate(args)                     # session 14 (W1)
            with contextlib.redirect_stdout(sys.stderr):
                res = T.call_tool(self.ws, name, args, caller="mcp")
            if gate is not None and isinstance(res, dict) and res.get("run_id"):
                res = self._after_submission(res, gate)
            text, is_error = json.dumps(res, ensure_ascii=False, default=str), False
            if name in ("submit_proposals", "request_review") and isinstance(res, dict) and res.get("run_id"):
                self.submitted = str(res["run_id"])
                if name == "submit_proposals" and self.submission_record is not None:
                    self._record_submission(res)
        except (ToolError, Refused) as e:
            text, is_error = json.dumps({"error": str(e)}, ensure_ascii=False), True
        except Exception as e:                                    # noqa: BLE001
            self._log(tool=name, arguments=args, internal_error=f"{type(e).__name__}: {e}")
            return _err(id_, -32603, f"internal error in {name}: {type(e).__name__}: {str(e)[:300]}")
        images, sent = [], []
        imaging = ("get_crop", "get_region", "get_addendum_page")     # session 14 (W5): the addendum's own pages too
        if name in imaging and not is_error:
            images, sent = self._crop_images(res, keep_order=(name != "get_crop"))
            text = json.dumps({**res, "images_attached": sent}, ensure_ascii=False, default=str)
        self._log(tool=name, arguments=args, is_error=is_error, result=text[:4000],
                  **({"images_sent": sent} if name in imaging else {}))
        return {"jsonrpc": "2.0", "id": id_, "result": {"content": [{"type": "text", "text": text}, *images],
                                                         "isError": is_error}}

    # ------------------------------------------------------------------ session 14 (W1): the submission gate's repair
    def _repairs(self) -> int:
        if self.repairs_left is None:
            try:
                from .ai import config as C
                from .ai.requests import FailurePolicy
                self.repairs_left = FailurePolicy.from_cfg(C.load(self.ws.ai_config)).repairs
            except Exception:                                     # noqa: BLE001 (the default bound)
                self.repairs_left = 1
        return self.repairs_left

    def _submission_gate(self, args: dict) -> tuple[dict, dict]:
        """(the arguments to submit, the gate's record). The re-submission that answers a repair request is merged
        into the first submission (contract.merge_repair): only the named items and statements are taken from it."""
        from .ai.contract import merge_repair, submission_problems
        from .ai.controller import _load_set_data
        raw = _load_set_data(args.get("proposal_set"))
        if self._repair is not None:
            rep = self._repair
            merged, notes = merge_repair(rep["raw"], raw if isinstance(raw, dict) else {}, rep["ids"], rep["indices"])
            self._log(tool="submission_repair", repair_of=rep["run_id"], merge=notes)
            return {**args, "proposal_set": merged}, {"repair_of": rep, "merge": notes, "raw": merged}
        return args, {"repair_of": None, "raw": raw,
                      "problems": submission_problems(raw) if isinstance(raw, dict) else []}

    def _after_submission(self, res: dict, gate: dict) -> dict:
        from .ai.contract import repair_schemas, submission_problems
        if gate["repair_of"] is not None:                         # the one repair: the merged set is staged
            first = gate["repair_of"]
            self._repair = None
            left = submission_problems(gate["raw"])
            self._mark_superseded(first, res)
            return {**res, "repair_of": first["run_id"], "repair_merge": gate["merge"],
                    "still_failing": left,
                    "note": ("the repair is merged into the first submission (the other items stand as first "
                             "submitted) and staged as this run; it supersedes " + first["run_id"]
                             + (". An item still failing its schema is invalid with its errors: no further repair"
                                if left else ""))}
        probs = gate["problems"]
        if not probs:
            return res
        if self._repairs() <= 0:
            return {**res, "still_failing": probs,
                    "note": "items whose payload fails its schema are invalid with their errors (no repair left)"}
        self.repairs_left -= 1
        ids = {str(p["id"]) for p in probs if p.get("id") is not None}
        idx = {p["index"] for p in probs if p.get("index") is not None and p.get("id") is None}
        self._repair = {"run_id": res.get("run_id"), "staging": res.get("staging"), "raw": gate["raw"], "ids": ids,
                        "indices": idx}
        self._log(tool="submission_repair_asked", run_id=res.get("run_id"), problems=probs)
        return {**res, "repair": {
            "tries_left": 1, "problems": probs, "schemas": repair_schemas(probs),
            "how": ("Your submission is staged as it is (" + str(res.get("run_id")) + "); the items and statements "
                    "listed fail their FULL schema (given here). Correct ONLY those and call submit_proposals ONCE "
                    "more with proposal_set {addendum, state, statements: the corrected statements only, items: the "
                    "corrected items only, with the same ids}. Every other item stands exactly as first submitted (a "
                    "resent sibling is ignored). This is the one repair: an item still failing after it stays invalid "
                    "with its errors.")}}

    def _mark_superseded(self, first: dict, res: dict) -> None:
        try:
            d = Path(first.get("staging") or "")
            if d.is_dir():
                (d / "superseded.json").write_text(json.dumps(
                    {"superseded_by": res.get("run_id"), "staging": res.get("staging"),
                     "why": "the submission gate's one repair of the items whose payload failed its schema; the other "
                            "items are carried over unchanged"}, ensure_ascii=False, indent=1), encoding="utf-8")
        except OSError as e:
            self._log(tool="submission_repair", superseded_marker_error=str(e))

    def _record_submission(self, res: dict) -> None:
        """Session 13: the submission's run id, status and staging folder written to `submission_record` (a temporary
        sibling, then os.replace). The record only points at the set the controller staged; it decides nothing."""
        rec = {"run_id": res.get("run_id"), "status": res.get("status"), "staging": res.get("staging"),
               "ts": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "pid": os.getpid()}
        try:
            p = self.submission_record
            p.parent.mkdir(parents=True, exist_ok=True)
            tmp = p.with_name(p.name + f".tmp{os.getpid()}")
            tmp.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
            os.replace(tmp, p)
            self._log(tool="submission_record", record=str(p), submission=rec)
        except OSError as e:                                     # the session's answer stands; only the record failed
            self._log(tool="submission_record", record=str(self.submission_record), error=str(e))

    @staticmethod
    def _crop_images(res: dict, keep_order: bool = False) -> tuple[list[dict], list[dict]]:
        """The crops of a get_crop result as MCP image content blocks (see the module docstring); get_region's in the
        order the tool lists them (the native image first, or the bands asked for)."""
        import base64
        blocks, sent, seen = [], [], set()
        crops = list(res.get("crops") or [])
        for c in (crops if keep_order else sorted(crops, key=lambda c: _CROP_ORDER.get(c.get("kind"), 9))):
            p = Path(c["path"])
            size = p.stat().st_size if p.is_file() else None
            rec = {"sha256": c["sha256"], "path_in_build": c["path_in_build"], "kind": c["kind"], "bytes": size}
            if c["sha256"] in seen:                               # the same file listed twice (e.g. a table's unit crop
                rec["attached"], rec["why_not"] = False, "the same image is already attached"   # is its region crop)
            elif len(blocks) >= MAX_IMAGES or size is None or size > MAX_IMAGE_BYTES:
                rec["attached"] = False
                rec["why_not"] = ("limit of images per call" if len(blocks) >= MAX_IMAGES else
                                  "missing" if size is None else f"over {MAX_IMAGE_BYTES} bytes")
            else:
                blocks.append({"type": "image", "data": base64.standard_b64encode(p.read_bytes()).decode("ascii"),
                               "mimeType": c.get("media_type") or "image/png"})
                rec["attached"] = True
                seen.add(c["sha256"])
            sent.append(rec)
        return blocks, sent


def serve(ws, stdin=None, stdout=None, *, tools=None, submit_once: bool = False, require_crops=(),
          submission_record=None, addendum_scope=None) -> int:
    from .ai.runlog import RunLog
    stdin = stdin or sys.stdin
    out = stdout or sys.stdout
    # session 14 (W5): a quick review's server serves its NEW addendum's pages (get_addendum_page) from this scope file
    ws.addendum_scope = str(addendum_scope) if addendum_scope else None
    session = f"mcp-{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%SZ}-{os.getpid()}"
    log = RunLog(session, [Path(ws.worklog) / f"{session}.jsonl"])
    log.event("mcp_start", evidence=str(ws.evidence), pack=str(ws.pack), staging=str(ws.staging),
              tools=tools if tools is not None else "all", submit_once=submit_once, require_crops=list(require_crops),
              addendum_scope=ws.addendum_scope)
    srv = Server(ws, log, tools=tools, submit_once=submit_once, require_crops=require_crops,
                 submission_record=submission_record)
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError as e:
            resp = _err(None, -32700, f"parse error: {e}")
        else:
            try:
                resp = srv.handle(msg)
            except Exception as e:                                # noqa: BLE001 (never kill the session on a bug)
                resp = _err(msg.get("id") if isinstance(msg, dict) else None, -32603, f"internal error: {e}")
        if resp is not None:
            out.write(json.dumps(resp, ensure_ascii=False) + "\n")
            out.flush()
    log.event("mcp_end")
    return 0
