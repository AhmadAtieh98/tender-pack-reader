#!/usr/bin/env python3
"""A RECORDED stand-in for the `claude` CLI (session 11, D2 tests): NOT a model. Its behaviour is set by files in the
folder named by the environment variable FAKE_S11_DIR:

    rate_limit_n         an integer: that many sessions answer with the host plan's rate-limit result, exactly as the
                         real CLI printed it in blind rehearsal 04 (is_error true, api_error_status 429, terminal_reason
                         api_error, "You've hit your session limit · resets 4:30pm (UTC)", exit code 1)
    answer.json          the FINAL MESSAGE of an answer session (a tool session started with --mcp-config whose prompt is
                         not an analysis packet), ${state} replaced with the packet's state
    repair.json          the corrected answer a plain REPAIR session prints (prompt "REPAIR REQUEST ...")
    calls.jsonl          appended: one line per invocation (kind, a few flags, the first characters of the prompt)
    kill_parent_after_submit_n   session 13: an integer: that many analysis sessions send SIGTERM to the process that
                         started them right after their submission (the orchestrator interrupted after a submission)

Without --mcp-config and with --json-schema and a CRITIC REQUEST: the batched critic; it answers every item key of the
request (disagreeing, with a recorded concern). An analysis tool session (a packet with `provisions`) starts the MCP
server named in --mcp-config and submits a one-item set through submit_proposals, as tests/fixtures/ai_cassettes/
fake_claude_host.py does."""
import json
import os
import subprocess
import sys
from pathlib import Path

argv = sys.argv[1:]
D = Path(os.environ.get("FAKE_S11_DIR", "."))


def arg(name):
    return argv[argv.index(name) + 1] if name in argv else None


def out(obj):
    print(json.dumps(obj, ensure_ascii=False), flush=True)


prompt = sys.stdin.read()
kind = ("critic" if "CRITIC REQUEST" in prompt else "repair" if "REPAIR REQUEST" in prompt else
        "tool" if arg("--mcp-config") else "plain")
with open(D / "calls.jsonl", "a", encoding="utf-8") as fh:
    fh.write(json.dumps({"kind": kind, "tools": arg("--tools"), "json_schema": "--json-schema" in argv,
                         "allowed": arg("--allowedTools"), "model": arg("--model"), "prompt": prompt[:200]}) + "\n")
if "-p" not in argv or arg("--tools") != "":
    out({"type": "result", "subtype": "error_during_execution", "is_error": True, "result": "expected -p --tools ''"})
    sys.exit(1)

rl = D / "rate_limit_n"
n = int(rl.read_text().strip() or 0) if rl.exists() else 0
if n > 0:
    rl.write_text(str(n - 1))
    res = {"type": "result", "subtype": "success", "is_error": True, "api_error_status": 429, "terminal_reason": "api_error",
           "num_turns": 1, "duration_ms": 248, "result": "You've hit your session limit · resets 4:30pm (UTC)",
           "usage": {"input_tokens": 0, "output_tokens": 0}, "modelUsage": {}, "total_cost_usd": 0}
    if arg("--output-format") == "stream-json":
        out({"type": "system", "subtype": "init", "model": "fake-host-model", "tools": [], "mcp_servers": []})
    out(res)
    sys.exit(1)


def state_of(text):
    try:
        return json.loads(text[text.index("TASK PACKET\n") + len("TASK PACKET\n"):]).get("state")
    except (ValueError, AttributeError):
        return None


if kind == "critic":
    req = json.loads(prompt[prompt.index("CRITIC REQUEST\n") + len("CRITIC REQUEST\n"):])
    reviews = [{"item": x["key"], "agrees": False, "concerns": [f"fake critic (recorded): {x['key']} checked against "
                                                                  "the evidence shown"], "evidence_checked": ["recorded"]}
               for x in req["items"]]
    out({"type": "result", "subtype": "success", "is_error": False, "num_turns": 1, "result": "{}",
         "structured_output": {"reviews": reviews}, "modelUsage": {"fake-critic-model": {}}, "total_cost_usd": 0.0,
         "usage": {"input_tokens": 10, "output_tokens": 5}})
    sys.exit(0)

if kind == "repair":
    text = (D / "repair.json").read_text(encoding="utf-8") if (D / "repair.json").exists() else "not json"
    out({"type": "result", "subtype": "success", "is_error": False, "num_turns": 1, "result": text,
         "modelUsage": {"fake-repair-model": {}}, "total_cost_usd": 0.0, "usage": {"input_tokens": 10, "output_tokens": 5}})
    sys.exit(0)

if kind != "tool":
    out({"type": "result", "subtype": "success", "is_error": False, "num_turns": 1, "result": "", "modelUsage": {}})
    sys.exit(0)

packet = json.loads(prompt[prompt.index("TASK PACKET\n") + len("TASK PACKET\n"):])
out({"type": "system", "subtype": "init", "model": "fake-host-model", "tools": [], "mcp_servers": [{"name": "tenderpack"}]})
if packet.get("provisions") and packet.get("task") == "propose_amendment":
    cfg = json.load(open(arg("--mcp-config")))["mcpServers"]["tenderpack"]
    srv = subprocess.Popen([cfg["command"], *cfg["args"]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
                           cwd=cfg.get("cwd"), stderr=subprocess.DEVNULL)
    k = 0

    def rpc(method, params=None, note=False):
        global k
        msg = {"jsonrpc": "2.0", "method": method, **({"params": params} if params is not None else {})}
        if not note:
            k += 1
            msg["id"] = k
        srv.stdin.write(json.dumps(msg) + "\n")
        srv.stdin.flush()
        return None if note else json.loads(srv.stdout.readline())
    rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "fake", "version": "0"}})
    rpc("notifications/initialized", note=True)
    first = packet["provisions"][0]["unit_id"]
    st = packet["state"]
    pset = {"addendum": packet["addendum"], "state": st, "statements": [], "items": [
        {"id": first.replace(":", "/"), "state": st, "statement_type": "escalation", "provision": first,
         "payload": {"why": "fake host (recorded): not analysed", "what_is_unsupported": "recorded fixture"},
         "evidence": [{"doc": packet["addendum"], "unit_id": first, "page": packet["provisions"][0]["pages"][0],
                       "kind": "span", "words": " ".join(packet["provisions"][0]["text"].split()[:6])}]}]}
    host_model = prompt.split("'", 2)[1] if "'" in prompt.split("\n", 1)[0] else "fake"
    out({"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "t1",
                                                       "name": "mcp__tenderpack__submit_proposals",
                                                       "input": {"proposal_set": pset, "host_model": host_model}}]}})
    r = rpc("tools/call", {"name": "submit_proposals", "arguments": {"proposal_set": pset, "host_model": host_model}})
    res = r.get("result") or {"content": [{"type": "text", "text": json.dumps(r.get("error"))}], "isError": True}
    out({"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "t1", "content": res["content"],
                                                  "is_error": res.get("isError", False)}]}})
    srv.stdin.close()
    srv.wait(timeout=60)
    kp = D / "kill_parent_after_submit_n"           # session 13 (D): the orchestrator stopped right after a submission
    if kp.exists() and int(kp.read_text().strip() or 0) > 0:
        kp.write_text(str(int(kp.read_text().strip()) - 1))
        import signal
        import time
        os.kill(os.getppid(), signal.SIGTERM)
        time.sleep(60)                                # the orchestrator stops this process (or the test times out)
    out({"type": "result", "subtype": "success", "is_error": False, "num_turns": 2, "result": "submitted",
         "usage": {"input_tokens": 100, "output_tokens": 20}, "modelUsage": {"fake-host-model": {}}, "total_cost_usd": 0.0})
    sys.exit(0)

text = (D / "answer.json").read_text(encoding="utf-8") if (D / "answer.json").exists() else ""
st = state_of(prompt)
if st is not None:
    text = text.replace("${state}", json.dumps(st, ensure_ascii=False))
out({"type": "result", "subtype": "success", "is_error": False, "num_turns": 3, "result": text,
     "usage": {"input_tokens": 100, "output_tokens": 20}, "modelUsage": {"fake-host-model": {}}, "total_cost_usd": 0.0})
