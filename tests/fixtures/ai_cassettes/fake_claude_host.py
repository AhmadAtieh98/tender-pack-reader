#!/usr/bin/env python3
"""A RECORDED stand-in for the `claude` CLI (session 10, W4 tests): NOT a model. It checks the flags tenderpack passes,
then either (a) with --json-schema answers as a critic, or (b) as a host session starts the MCP server named in
--mcp-config, calls get_crop and submit_proposals over JSON-RPC exactly as a host would, and prints stream-json lines
shaped like Claude Code's (system init, assistant tool_use, user tool_result with image blocks, result)."""
import json
import os
import subprocess
import sys

argv = sys.argv[1:]


def arg(name):
    return argv[argv.index(name) + 1] if name in argv else None


def fail(msg):
    print(json.dumps({"type": "result", "subtype": "error_during_execution", "is_error": True, "result": msg}))
    sys.exit(1)


if "-p" not in argv or arg("--tools") != "":
    fail("expected -p and --tools '' (no built-in tools)")
prompt = sys.stdin.read()
if "--json-schema" in argv:                                   # (a) the critic
    if arg("--output-format") != "json" or "CRITIC REQUEST" not in prompt:
        fail("critic: expected --output-format json and a CRITIC REQUEST")
    print(json.dumps({"type": "result", "subtype": "success", "is_error": False, "num_turns": 2,
                      "structured_output": {"agrees": False, "concerns": ["fake host critic: a recorded concern"],
                                            "evidence_checked": ["recorded"]},
                      "result": "{}", "modelUsage": {"fake-critic-model": {}}, "total_cost_usd": 0.0,
                      "usage": {"input_tokens": 10, "output_tokens": 5}}))
    sys.exit(0)

# (b) the host session
# session 13: deny-by-default, an explicit allow list (never the wildcard) naming the tools this stand-in calls
allowed = (arg("--allowedTools") or "").split(",")
if "mcp__tenderpack__*" in allowed or not {"mcp__tenderpack__get_crop", "mcp__tenderpack__submit_proposals"} <= \
        set(allowed) or "--strict-mcp-config" not in argv or arg("--output-format") != "stream-json":
    fail("host session: expected an explicit --allowedTools list with get_crop and submit_proposals, "
         "--strict-mcp-config, --output-format stream-json")
cfg = json.load(open(arg("--mcp-config")))["mcpServers"]["tenderpack"]
srv = subprocess.Popen([cfg["command"], *cfg["args"]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
                       cwd=cfg.get("cwd"), stderr=subprocess.DEVNULL)
n = 0


def rpc(method, params=None, note=False):
    global n
    msg = {"jsonrpc": "2.0", "method": method, **({"params": params} if params is not None else {})}
    if not note:
        n += 1
        msg["id"] = n
    srv.stdin.write(json.dumps(msg) + "\n")
    srv.stdin.flush()
    return None if note else json.loads(srv.stdout.readline())


def out(obj):
    print(json.dumps(obj, ensure_ascii=False), flush=True)


rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "fake", "version": "0"}})
rpc("notifications/initialized", note=True)
tools = [t["name"] for t in rpc("tools/list")["result"]["tools"]]
out({"type": "system", "subtype": "init", "model": "fake-host-model", "tools": ["mcp__tenderpack__" + t for t in tools],
     "mcp_servers": [{"name": "tenderpack", "status": "connected"}], "permissionMode": "default"})
packet = json.loads(prompt[prompt.index("TASK PACKET\n") + len("TASK PACKET\n"):])
host_model = prompt.split("'", 2)[1] if "'" in prompt.split("\n", 1)[0] else "fake"


def call(i, name, args):
    out({"type": "assistant", "message": {"model": "fake-host-model", "content": [
        {"type": "tool_use", "id": f"t{i}", "name": "mcp__tenderpack__" + name, "input": args}]}})
    r = rpc("tools/call", {"name": name, "arguments": args})
    res = r.get("result") or {"content": [{"type": "text", "text": json.dumps(r.get("error"))}], "isError": True}
    blocks = []
    for c in res["content"]:
        if c["type"] == "image":                              # Claude Code passes MCP images on as image blocks
            blocks.append({"type": "image", "source": {"type": "base64", "media_type": c["mimeType"], "data": c["data"]}})
        else:
            blocks.append(c)
    out({"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": f"t{i}", "content": blocks, "is_error": res.get("isError", False)}]}})
    return res


targets = packet.get("image_targets") or []
if targets:
    call(1, "get_crop", {"unit_id": targets[0]})
state = packet["state"]
pset = {"addendum": packet["addendum"], "state": state, "statements": [], "items": [
    {"id": "ADD-03/cover/para1", "state": state, "statement_type": "disposition", "provision": "ADD-03:cover/para1",
     "payload": {"provision": "ADD-03:cover/para1", "disposition": "no_effect", "reason": "the addendum's issue date line"},
     "evidence": [{"doc": "ADD-03", "unit_id": "ADD-03:cover/para1", "page": 1, "kind": "span",
                   "words": "Issued 3 November 2026"}],
     "model_rationale": "fake host: the crop shows a table (recorded)"}]}
sub = call(2, "submit_proposals", {"proposal_set": pset, "host_model": host_model})
srv.stdin.close()
srv.wait(timeout=60)
text = json.loads(sub["content"][0]["text"])
out({"type": "assistant", "message": {"model": "fake-host-model", "content": [
    {"type": "text", "text": f"submitted {text.get('run_id')} ({text.get('status')}); crops read: {targets[:1]}"}]}})
out({"type": "result", "subtype": "success", "is_error": False, "num_turns": 3, "result": "submitted",
     "usage": {"input_tokens": 100, "output_tokens": 20}, "modelUsage": {"fake-host-model": {}}, "total_cost_usd": 0.0})
