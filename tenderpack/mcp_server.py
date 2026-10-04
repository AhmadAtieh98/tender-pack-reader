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
                              the region's images the same way, in the order it lists them.
Errors: parse error -32700, invalid request -32600, unknown method -32601, unknown tool or bad arguments -32602,
internal error -32603. A tool's own refusal (e.g. no such unit) is a result with isError true, as MCP specifies.

Every tool is read-only except get_task_packet with claim=true (the addendum's lock), request_review and
submit_proposals, which write to staging/ai only (never curation/). Every call is logged to
worklog/model_calls/mcp-<session>.jsonl (arguments and a truncated result; secrets redacted). Anything the tools print
goes to stderr, so stdout carries only protocol messages.
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
INSTRUCTIONS = ("Read-only tools over a confidential tender pack's evidence build, plus staging-only writers. Proposals "
                "are validated by the controller, which assigns every verification status; nothing is accepted or "
                "published here; a named person decides. Claim an addendum with get_task_packet(claim=true) before "
                "working on it, and submit with submit_proposals(proposal_set, host_model).")


def _err(id_, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message}}


class Server:
    def __init__(self, ws, log=None):
        self.ws, self.log = ws, log
        self.initialized = False

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
                "instructions": INSTRUCTIONS}}
        if method == "ping":
            return {"jsonrpc": "2.0", "id": id_, "result": {}}
        if method == "tools/list":
            from .ai.tools import TOOLS
            return {"jsonrpc": "2.0", "id": id_, "result": {"tools": [
                {"name": t.name, "description": t.description + (" (writes to staging only)" if t.writes else " (read-only)"),
                 "inputSchema": t.input_schema} for t in TOOLS.values()]}}
        if method == "tools/call":
            return self._call(id_, params)
        return _err(id_, -32601, f"method not found: {method}")

    def _call(self, id_, params: dict) -> dict:
        from .ai.budget import Refused
        from .ai.tools import TOOLS, ToolError, call_tool, check_args
        name, args = params.get("name"), params.get("arguments") or {}
        if name not in TOOLS:
            return _err(id_, -32602, f"unknown tool: {name}")
        try:
            check_args(TOOLS[name].input_schema, args)
        except ToolError as e:
            return _err(id_, -32602, f"invalid arguments for {name}: {e}")
        try:
            with contextlib.redirect_stdout(sys.stderr):
                res = call_tool(self.ws, name, args, caller="mcp")
            text, is_error = json.dumps(res, ensure_ascii=False, default=str), False
        except (ToolError, Refused) as e:
            text, is_error = json.dumps({"error": str(e)}, ensure_ascii=False), True
        except Exception as e:                                    # noqa: BLE001
            self._log(tool=name, arguments=args, internal_error=f"{type(e).__name__}: {e}")
            return _err(id_, -32603, f"internal error in {name}: {type(e).__name__}: {str(e)[:300]}")
        images, sent = [], []
        if name in ("get_crop", "get_region") and not is_error:
            images, sent = self._crop_images(res, keep_order=(name == "get_region"))
            text = json.dumps({**res, "images_attached": sent}, ensure_ascii=False, default=str)
        self._log(tool=name, arguments=args, is_error=is_error, result=text[:4000],
                  **({"images_sent": sent} if name in ("get_crop", "get_region") else {}))
        return {"jsonrpc": "2.0", "id": id_, "result": {"content": [{"type": "text", "text": text}, *images],
                                                         "isError": is_error}}

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


def serve(ws, stdin=None, stdout=None) -> int:
    from .ai.runlog import RunLog
    stdin = stdin or sys.stdin
    out = stdout or sys.stdout
    session = f"mcp-{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%SZ}-{os.getpid()}"
    log = RunLog(session, [Path(ws.worklog) / f"{session}.jsonl"])
    log.event("mcp_start", evidence=str(ws.evidence), pack=str(ws.pack), staging=str(ws.staging))
    srv = Server(ws, log)
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
