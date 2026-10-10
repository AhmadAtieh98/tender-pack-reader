"""Codex runtime transport for tenderpack's host sessions.

Uses the signed-in CLI with only the phase-scoped MCP server. Native events are kept
separately from the normalised host events; configured identity is never reported identity.
"""
import argparse
import base64
import binascii
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import queue
import shutil
import re
import signal
import subprocess
import sys
import threading
import time
import uuid

PREFIX = "mcp__tenderpack__"
DISABLED = ("shell_tool", "unified_exec", "multi_agent", "apps", "plugins", "remote_plugin",
            "browser_use", "browser_use_external", "browser_use_full_cdp_access", "computer_use",
            "in_app_browser", "image_generation", "view_image", "skill_search", "workspace_dependencies",
            "hooks", "memories", "shell_snapshot")


def j(obj):
    return json.dumps(obj, ensure_ascii=False)


def toml(value):
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return "[" + ",".join(toml(x) for x in value) + "]"
    if isinstance(value, dict):
        return "{" + ",".join(toml(str(k)) + "=" + toml(v) for k, v in value.items()) + "}"
    raise ValueError("Unsupported TOML value type: " + type(value).__name__)


def compatible_schema(schema):
    """Use native strict output only where the supplied schema already fits it; do not rewrite it."""
    if isinstance(schema, list):
        return all(compatible_schema(x) for x in schema)
    if not isinstance(schema, dict):
        return True
    if schema.get("type") == "object" or "properties" in schema:
        if schema.get("additionalProperties") is not False:
            return False
        if set(schema.get("properties", {})) != set(schema.get("required", [])):
            return False
    return all(compatible_schema(v) for v in schema.values())


def normalize_mcp_result(result):
    """Codex may put an MCP result envelope in its sole text block; unwrap only that exact shape.

    Real image/tool-return probes observed this, while the minimal echo probe had
    ordinary direct content. Raw JSONL remains unchanged for audit.
    """
    result = dict(result) if isinstance(result, dict) else {}
    for _ in range(4):
        content = result.get("content") or []
        if not isinstance(content, list) or len(content) != 1 or not isinstance(content[0], dict) or content[0].get("type") != "text":
            break
        try:
            inner = json.loads(content[0].get("text", ""))
        except (ValueError, TypeError):
            break
        if not isinstance(inner, dict) or not isinstance(inner.get("content"), list):
            break
        if not set(inner) <= {"content", "isError", "structuredContent", "_meta"}:
            break
        if not all(isinstance(block, dict) and block.get("type") in
                   ("text", "image", "audio", "resource", "resource_link") for block in inner["content"]):
            break
        result = {**inner, "isError": bool(result.get("isError") or inner.get("isError"))}
    diagnostics = []
    content = []
    for block in result.get("content") or []:
        if not isinstance(block, dict):
            continue
        if block.get("type") != "image":
            content.append(block)
            continue
        data = block.get("data") or (block.get("source") or {}).get("data") or ""
        try:
            if not isinstance(data, str) or not data:
                raise ValueError("image payload is empty or not a string")
            base64.b64decode(data, validate=True)
        except (ValueError, binascii.Error, UnicodeError) as exc:
            raw = data if isinstance(data, str) else j(data)
            diagnostics.append({"kind": "invalid_image_transport", "action": "omitted invalid image; no reconstruction or fetch",
                                "sha256_of_raw_payload_text": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
                                "raw_payload_char_count": len(raw), "error": str(exc)[:160],
                                "mime_type": block.get("mimeType") or (block.get("source") or {}).get("media_type")})
        else:
            content.append(block)
    if diagnostics:
        # Keep one JSON text block where possible, so the existing parser can still
        # read images_attached/run_id. Diagnostics are TEXT, never invented pixels.
        attached = False
        for index, block in enumerate(content):
            if block.get("type") != "text":
                continue
            try:
                data = json.loads(block.get("text", ""))
            except (ValueError, TypeError):
                continue
            if isinstance(data, dict):
                data["codex_image_transport_diagnostics"] = diagnostics
                content[index] = {**block, "text": j(data)}
                attached = True
                break
        if not attached:
            content.append({"type": "text", "text": j({"codex_image_transport_diagnostics": diagnostics})})
        result["_codex_image_transport_diagnostics"] = diagnostics
    result["content"] = content
    return result


def parse_args(argv):
    p = argparse.ArgumentParser()
    p.add_argument("-p", action="store_true")
    p.add_argument("--codex-settings", required=True)
    for name in ("mcp-config", "tools", "allowedTools", "disallowedTools", "permission-prompts",
                 "output-format", "system-prompt", "model", "json-schema"):
        p.add_argument("--" + name)
    for name in ("strict-mcp-config", "no-session-persistence", "verbose"):
        p.add_argument("--" + name, action="store_true")
    p.add_argument("--max-turns", type=int, default=40)
    return p.parse_args(argv)


def kill_group(pid, sig=signal.SIGTERM):
    try:
        os.killpg(pid, sig)
    except ProcessLookupError:
        pass


def watchdog(bridge_pid, child_pid, timeout):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        try:
            os.kill(child_pid, 0)
        except ProcessLookupError:
            return
        try:
            os.kill(bridge_pid, 0)
        except ProcessLookupError:
            break
        time.sleep(0.5)
    kill_group(child_pid)
    time.sleep(1)
    kill_group(child_pid, signal.SIGKILL)


def event_adapter(events, final_text, allowed, model):
    converted = []
    reported_models = set()
    seen = set()
    usage = {}
    turns = 0
    errors = []
    for e in events:
        if not isinstance(e, dict):
            continue
        typ = e.get("type")
        if e.get("model"):
            reported_models.add(str(e["model"]))
        item = e.get("item") if isinstance(e.get("item"), dict) else {}
        if item.get("model"):
            reported_models.add(str(item["model"]))
        if typ == "turn.completed":
            turns += 1
            for k, v in (e.get("usage") or {}).items():
                if isinstance(v, (int, float)):
                    usage[k] = usage.get(k, 0) + v
        if typ in ("turn.failed", "error") or item.get("type") == "error":
            err = e.get("error")
            errors.append(e.get("message") or (err.get("message") if isinstance(err, dict) else str(err or "")) or item.get("message") or j(e))
        if item.get("type") == "mcp_tool_call" and typ == "item.completed":
            ident = item.get("id")
            if ident in seen:
                continue
            seen.add(ident)
            name = item.get("tool", "")
            server = item.get("server", "")
            if server != "tenderpack" or name not in allowed:
                errors.append("MCP call outside configured phase: " + server + "." + name)
                continue
            converted.append({"type": "assistant", "message": {"content": [{"type": "tool_use", "id": ident,
                              "name": PREFIX + name, "input": item.get("arguments") or {}}]}})
            res = normalize_mcp_result(item.get("result"))
            err = item.get("error")
            if err and "requires approval" in j(err).lower():
                errors.append("MCP approval configuration prevented " + server + "." + name + ": " + j(err))
            content = res.get("content") or []
            if not content and err:
                content = [{"type": "text", "text": j(err)}]
            converted.append({"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": ident,
                              "content": content, "is_error": bool(err or res.get("isError") or item.get("status") != "completed"),
                              "codex_image_transport_diagnostics": res.get("_codex_image_transport_diagnostics", [])} ]}})
        elif item.get("type") == "agent_message" and typ == "item.completed":
            final_text = item.get("text", final_text)
    # A model configuration is recorded separately; it is never represented as runtime-reported telemetry.
    return converted, final_text, usage, turns, sorted(reported_models), errors


def transport_diagnostics(converted):
    return [d for e in converted for b in (e.get("message") or {}).get("content", [])
            for d in b.get("codex_image_transport_diagnostics", [])]



def discover(configured=None):
    candidate = configured or shutil.which("codex")
    if not candidate:
        candidate = "/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex"
    if not (shutil.which(candidate) or Path(candidate).is_file()):
        raise FileNotFoundError("Codex CLI not found; set host_session.codex_bin")
    return str(candidate)


def wrap_command(command, cfg, model, timeout):
    settings = dict(cfg.get("host_session") or {})
    settings = {k: settings[k] for k in ("codex_bin", "reasoning_effort", "max_mcp_calls") if k in settings}
    from .offline import active
    settings.update(model=model, timeout_s=max(1, float(timeout) - 5), offline=bool(active(cfg)))
    return [sys.executable, "-m", "tenderpack.ai.codex", "--codex-settings", j(settings), *command[1:]]


def main(argv):
    args = parse_args(argv)
    original_prompt = sys.stdin.read()
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:10]
    settings = json.loads(args.codex_settings)
    from .offline import check_host_session
    check_host_session(settings, "Codex runtime transport")
    binary = discover(settings.get("codex_bin"))
    logdir = Path.cwd() / "codex" / stamp
    logdir.mkdir(parents=True)
    allowed = [x.removeprefix(PREFIX) for x in (args.allowedTools or "").split(",") if x]
    model = args.model or settings.get("model")
    effort = settings.get("reasoning_effort", "high")
    if not model:
        raise ValueError("Configure host_session.model for the Codex runtime")
    label = "codex exec (configured " + model + "; runtime model identity reported separately)"
    prompt, replacements = re.subn(r"^host_model value for submit_proposals:.*$",
                                  "host_model value for submit_proposals: " + repr(label), original_prompt, count=1, flags=re.M)
    system = args.system_prompt or ""
    phase_match = re.search(r"\bphase=([a-z_]+)", system)
    phase = phase_match.group(1) if phase_match else "plain"
    is_plain = not args.mcp_config
    mcp_call_limit = int(settings.get("max_mcp_calls", 120))
    timeout = float(settings["timeout_s"])
    if mcp_call_limit < 1 or timeout <= 0:
        raise ValueError("Codex call and time budgets must be positive")
    command = [binary, "--no-daemon", "-a", "never", "exec", "--ignore-user-config", "--ephemeral", "--json",
               "--sandbox", "read-only", "--skip-git-repo-check", "--color", "never", "-C", str(Path.cwd()),
               "--model", model, "-c", "model_reasoning_effort=" + toml(effort),
               "-c", "web_search=\"disabled\"", "-c", "project_doc_max_bytes=0"]
    for feature in DISABLED:
        command.extend(["-c", "features." + feature + "=false"])
    # Code Mode is the installed CLI's tool dispatcher. It must stay enabled for MCP to function.
    command.extend(["-c", "features.code_mode_host=true"])
    system += ("\n\nTENDERPACK RUNTIME: You run through Codex exec. Use only the explicitly listed tenderpack MCP tools "
               "for this phase. Do not use native file, shell, network, browser, planning, or other tools. Do not edit "
               "files directly. The legacy host protocol is only a transport adapter. Its model label is replaced "
               "by the Codex label in this prompt. Do not claim a human decision, approval or bidder fact. ")
    if is_plain:
        system += "This phase has no tools. Return only the JSON response required by its policy."
    command.extend(["-c", "developer_instructions=" + toml(system)])
    mcp = {}
    if args.mcp_config:
        mcp = json.loads(Path(args.mcp_config).read_text())
        if set(mcp.get("mcpServers", {})) != {"tenderpack"}:
            raise ValueError("Expected only the tenderpack MCP server")
        original = mcp["mcpServers"]["tenderpack"]
        server = {k: original[k] for k in ("command", "args", "cwd", "env") if k in original}
        server.update(required=True, enabled=True, enabled_tools=allowed, startup_timeout_sec=90, tool_timeout_sec=180)
        # The user authorized this workflow. Approval applies only to this phase's
        # existing allowlist; the server retains its own independent phase limits.
        # Do not change the process sandbox or the approval policy for other tools.
        server["tools"] = {name: {"approval_mode": "approve"} for name in allowed}
        command.extend(["-c", "mcp_servers=" + toml({"tenderpack": server})])
    schema_mode = "none"
    if args.json_schema:
        schema = json.loads(args.json_schema)
        schema_path = logdir / "output-schema.json"
        schema_path.write_text(j(schema))
        if compatible_schema(schema):
            schema_mode = "native_output_schema"
            command.extend(["--output-schema", str(schema_path)])
        else:
            schema_mode = "prompt_only_original_schema_not_strict_compatible"
            prompt += "\n\nReturn JSON conforming to this original schema (the application validates it):\n" + j(schema)
    last = logdir / "final.txt"
    command.extend(["--output-last-message", str(last), "-"])
    metadata = {"runtime": "Codex CLI", "binary": binary, "event_protocol": "Codex events normalised for tenderpack HostSession",
                "configured_model": model, "configured_effort": effort, "model_configuration_source": "host_session configuration and phase override",
                "model_reported": [], "cost_usd": None, "command": command, "cwd": str(Path.cwd()), "phase": phase,
                "allowed_mcp_tools": allowed, "original_mcp": mcp, "schema_mode": schema_mode, "host_model_label_replacements": replacements,
                "mcp_approval_scope": "Per-tool approval_mode=approve only for allowed tenderpack phase tools; workflow authorised by user",
                "original_prompt_sha256": hashlib.sha256(original_prompt.encode()).hexdigest(),
                "effective_prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(), "timeout_s": timeout,
                "max_turns_requested": args.max_turns, "max_turns_note": "Completed turns, MCP calls and elapsed time have separate bounds; a tool call is not a model turn", "max_mcp_calls": mcp_call_limit,
                "sandbox": "read-only", "disabled_features": list(DISABLED), "code_mode_host_required": True,
                "native_tools_note": "No shell/apps/plugins/browser; native mutation is blocked by read-only sandbox. Unexpected native action events fail the run.",
                "started_utc": dt.datetime.now(dt.timezone.utc).isoformat()}
    (logdir / "metadata.json").write_text(j(metadata))
    (logdir / "prompt.txt").write_text(prompt)
    (logdir / "policy.txt").write_text(system)
    print("Codex run runtime logs: " + str(logdir), file=sys.stderr, flush=True)
    stopped = threading.Event()
    completed_turns = 0
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda *_: stopped.set())
    events = []
    failures = []
    seen_calls = set()
    t0 = time.monotonic()
    with (logdir / "stderr.txt").open("w") as errfile, (logdir / "raw.jsonl").open("w") as rawfile:
        child = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errfile,
                                 text=True, start_new_session=True)
        guard = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "--watchdog", str(os.getpid()), str(child.pid), str(timeout+2)],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        q = queue.Queue()
        def reader():
            for line in child.stdout:
                q.put(line)
            q.put(None)
        threading.Thread(target=reader, daemon=True).start()
        child.stdin.write(prompt)
        child.stdin.close()
        while True:
            if stopped.is_set() or time.monotonic() - t0 > timeout:
                failures.append("Codex runtime interrupted" if stopped.is_set() else "Codex runtime timeout")
                kill_group(child.pid)
                break
            try:
                line = q.get(timeout=0.2)
            except queue.Empty:
                continue
            if line is None:
                break
            rawfile.write(line)
            rawfile.flush()
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if not isinstance(event, dict):
                continue
            events.append(event)
            if event.get("type") == "turn.completed":
                completed_turns += 1
                if completed_turns > args.max_turns:
                    failures.append("Completed model turn cap exceeded")
                    kill_group(child.pid)
                    break
            item = event.get("item") if isinstance(event.get("item"), dict) else {}
            if item.get("type") == "mcp_tool_call" and event.get("type") in ("item.started", "item.completed"):
                seen_calls.add(item.get("id"))
                if len(seen_calls) > mcp_call_limit or item.get("server") != "tenderpack" or item.get("tool") not in allowed:
                    failures.append("MCP call cap or phase allowlist violated")
                    kill_group(child.pid)
                    break
            if item.get("type") in ("command_execution", "file_change", "web_search"):
                failures.append("Unexpected native action: " + item["type"])
                kill_group(child.pid)
                break
        try:
            code = child.wait(timeout=3)
        except subprocess.TimeoutExpired:
            kill_group(child.pid, signal.SIGKILL)
            code = child.wait()
        guard.terminate()
        guard.wait(timeout=3)
    final = last.read_text() if last.exists() else ""
    converted, final, usage, turns, models, errors = event_adapter(events, final, allowed, model)
    failures.extend(errors)
    if code:
        failures.append("Codex exit code " + str(code))
    if not any(e.get("type") == "turn.completed" for e in events):
        failures.append("Codex emitted no completed turn")
    failed = bool(failures)
    result = {"type": "result", "subtype": "error_during_execution" if failed else "success", "is_error": failed,
              "result": final if not failed else "\n".join(failures) + ("\n" + final if final else ""),
              "usage": usage, "num_turns": turns, "modelUsage": {m: {} for m in models}, "total_cost_usd": None,
              "terminal_reason": "api_error" if failed else "completed", "codex_bridge_metadata": str(logdir / "metadata.json")}
    if args.json_schema and not failed:
        try:
            result["structured_output"] = json.loads(final)
        except ValueError:
            pass
    metadata.update(elapsed_s=round(time.monotonic()-t0, 3), exit_code=code, failures=failures,
                    model_reported=models, usage=usage, mcp_calls=len(seen_calls), final_sha256=hashlib.sha256(final.encode()).hexdigest(),
                    image_transport_diagnostics=transport_diagnostics(converted))
    (logdir / "metadata.json").write_text(j(metadata))
    (logdir / "translated.jsonl").write_text("\n".join(j(x) for x in converted+[result]) + "\n")
    if args.output_format == "stream-json":
        # No fabricated init or discovery; completed actual MCP call results are the evidence.
        for e in converted:
            print(j(e), flush=True)
    print(j(result), flush=True)
    if failed:
        stderr = (logdir / "stderr.txt").read_text()
        print(stderr[-5000:], file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--watchdog":
        watchdog(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]))
    else:
        try:
            raise SystemExit(main(sys.argv[1:]))
        except Exception as exc:
            print(j({"type": "result", "is_error": True, "subtype": "bridge_setup_error", "result": str(exc), "terminal_reason": "api_error"}), flush=True)
            raise
