"""Session 09, the stdio MCP server (JSON-RPC 2.0, no dependency), spoken to by a subprocess as a coding host would:
initialize -> notifications/initialized -> tools/list -> tools/call, plus the error objects. Disposable directories."""
from __future__ import annotations

import json
import subprocess
import sys

import pytest

from ai_fixture import EVIDENCE, ROOT, fresh_pack


@pytest.fixture(scope="module")
def session(tmp_path_factory):
    d = tmp_path_factory.mktemp("ai-mcp")
    pack = fresh_pack(d / "pack")
    msgs = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize",
         "params": {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "test-host", "version": "0"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_unit", "arguments": {"unit_id": "VOL-I:6.1",
                                                                                                         "stage": "ADD-03"}}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "get_unit", "arguments": {"unit_id": "NOPE:1"}}},
        {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "write_file", "arguments": {"path": "x"}}},
        {"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "get_unit", "arguments": {"bad": 1}}},
        {"jsonrpc": "2.0", "id": 7, "method": "resources/list"},
        {"jsonrpc": "2.0", "id": 8, "method": "ping"},
        {"jsonrpc": "2.0", "id": 9, "method": "initialize", "params": {"protocolVersion": "1999-01-01"}},
        {"jsonrpc": "2.0", "id": 10, "method": "tools/call", "params": {"name": "get_state", "arguments": {}}},
    ]
    text = "\n".join(json.dumps(m) for m in msgs) + "\n{not json\n"
    p = subprocess.run([sys.executable, "-m", "tenderpack", "ai", "serve-mcp", "--evidence", str(EVIDENCE), "--pack", str(pack),
                        "--out", str(d / "staging"), "--worklog", str(d / "worklog")],
                       input=text, capture_output=True, text=True, cwd=ROOT, timeout=300)
    assert p.returncode == 0, p.stderr
    lines = [json.loads(x) for x in p.stdout.splitlines() if x.strip()]
    return {"by_id": {r.get("id"): r for r in lines}, "lines": lines, "dir": d}


def test_initialize_echoes_a_supported_version_and_notifications_get_no_reply(session):
    r = session["by_id"][1]["result"]
    assert r["protocolVersion"] == "2025-03-26" and r["serverInfo"]["name"] == "tenderpack" and "tools" in r["capabilities"]
    assert session["by_id"][9]["result"]["protocolVersion"] == "2025-03-26"     # unsupported -> the latest supported
    assert len(session["lines"]) == 11                                         # 10 requests + 1 parse error; no notification reply
    assert session["by_id"][8]["result"] == {}


def test_tools_list_and_a_tool_call(session):
    tools = {t["name"]: t for t in session["by_id"][2]["result"]["tools"]}
    assert {"search_evidence", "get_unit", "get_group", "get_crop", "compare_state", "calculate", "simulate_amendment",
            "simulate_programme", "validate_proposal", "request_review", "submit_proposals", "get_task_packet"} <= set(tools)
    assert tools["get_unit"]["inputSchema"]["required"] == ["unit_id"]
    assert "(read-only)" in tools["get_unit"]["description"] and "staging only" in tools["submit_proposals"]["description"]
    res = session["by_id"][3]["result"]
    assert res["isError"] is False and res["content"][0]["type"] == "text"
    unit = json.loads(res["content"][0]["text"])
    assert "11:00 hours Riyadh time" in unit["effective_text"] and unit["stage"] == "ADD-03"
    st = json.loads(session["by_id"][10]["result"]["content"][0]["text"])
    assert st["state"]["validated_stage"] == "ADD-02"


def test_errors_are_proper_json_rpc_objects(session):
    nf = session["by_id"][4]["result"]
    assert nf["isError"] is True and "no unit" in json.loads(nf["content"][0]["text"])["error"]
    assert session["by_id"][5]["error"]["code"] == -32602 and "unknown tool" in session["by_id"][5]["error"]["message"]
    assert session["by_id"][6]["error"]["code"] == -32602
    assert session["by_id"][7]["error"]["code"] == -32601
    assert session["by_id"][None]["error"]["code"] == -32700
    logs = list((session["dir"] / "worklog").glob("mcp-*.jsonl"))
    assert len(logs) == 1 and '"tool": "get_unit"' in logs[0].read_text()
    assert not (session["dir"] / "staging").exists() or not any((session["dir"] / "staging").iterdir())   # read-only
