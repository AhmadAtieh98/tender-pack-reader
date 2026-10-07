"""Session 14 (W5), part 1: the quick review's scoped, read-only access to the NEW addendum's pages and image regions
on the host route (report s13 §6: "the host route without page images").

ONE new tool, get_addendum_page, offered only to the quick-review phase on the host route (policy.tools), serving only
the pages and image regions of the addendum the quick review was started on (rendered at a bounded size when the
quick review starts, each file's sha256 recorded and re-checked on every call), never another volume and never a write.
The first briefing stays separate and is labelled "preliminary; model output; not a tool result" in every rendering.

Every exchange is a FAKE host CLI or the real MCP server over stdio on a scope file: no live model call is made."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from ai_fixture import ROOT, workspace

PDF02 = ROOT / "rehearsals/blind-02/input/ADD-03_Addendum_No_3.pdf"          # synthetic rehearsal inputs (test data)
PDF06 = ROOT / "rehearsals/blind-06/input/ADD-03_Addendum_No_3.pdf"          # page 4 carries an image region
TOOLS5 = ("search_evidence", "get_unit", "get_group", "get_crop", "compare_state")
KIND = "preliminary; model output; not a tool result"

BRIEFING = {
    "addendum": "ADD-03",
    "items": [{"id": "P1", "provision": "2.1", "page": 1, "quotation": "Proposal Due Date", "target_unit_guess": None,
               "kind": "unclear", "deliverables": ["A5"], "rows": [], "confidence": "low",
               "uncertainty_class": "genuine ambiguity", "uncertainty": "test briefing", "propagation": []}],
    "questions": [], "unverified_calculations": [], "not_read": [], "model_rationale": "a test briefing"}


@pytest.fixture(scope="module")
def ws(tmp_path_factory, blind02_build):
    return workspace(tmp_path_factory.mktemp("qr14-ws"), evidence=blind02_build)


def _scope(tmp_path, pdf=PDF06, qid="ADD-03-qr-test"):
    from tenderpack.ai import quick_review as QR
    d = tmp_path / "staging" / "ai" / "quick-review" / qid
    d.mkdir(parents=True)
    sc = QR.prepare_scope(pdf, d, "ADD-03", qid)
    return d, sc


def test_the_page_tool_is_offered_only_to_the_quick_review_on_the_host_route():
    from tenderpack.ai import policy as P
    from tenderpack.ai.tools import MODEL_TOOLS, TOOLS
    assert "get_addendum_page" in TOOLS and not TOOLS["get_addendum_page"].writes
    assert "get_addendum_page" not in MODEL_TOOLS                      # never offered to the API routes' models
    assert P.tools("quick_review", "host") == TOOLS5 + ("get_addendum_page",)
    for route in ("recorded", "anthropic", "openrouter", "ollama"):
        assert P.tools("quick_review", route) == TOOLS5
    for phase in ("analysis", "downstream", "reading", "critic"):
        assert "get_addendum_page" not in P.tools(phase, "host")


def test_the_scope_renders_every_page_and_region_at_a_bounded_size(tmp_path):
    import pymupdf
    from tenderpack.ai import quick_review as QR
    d, sc = _scope(tmp_path)
    assert sc["label"].startswith("a tool result") and sc["pdf"]["sha256"]
    assert [p["page"] for p in sc["pages"]] == [1, 2, 3, 4, 5]
    assert [len(p["regions"]) for p in sc["pages"]] == [0, 0, 0, 1, 0]
    for p in sc["pages"]:
        pix = pymupdf.Pixmap(str(d / QR.SCOPE_DIR / p["image"]["file"]))
        assert max(pix.width, pix.height) <= QR.PAGE_MAX_PX
    r = sc["pages"][3]["regions"][0]
    pix = pymupdf.Pixmap(str(d / QR.SCOPE_DIR / r["crop"]["file"]))
    assert max(pix.width, pix.height) <= QR.CROP_MAX_PX and r["bbox"]


def test_the_page_tool_serves_the_addendums_page_and_region_images_over_mcp_and_nothing_else(tmp_path, ws):
    from tenderpack.ai import quick_review as QR
    from tenderpack.mcp_server import Server
    d, sc = _scope(tmp_path)
    ws.addendum_scope = str(d / QR.SCOPE_FILE)
    ws.addendum_scope_sha256 = sc["file_sha256"]          # session 14 (F4; R4-5): the scope file's recorded sha256
    try:
        srv = Server(ws, tools=list(TOOLS5) + ["get_addendum_page"])
        listed = srv.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})["result"]["tools"]
        assert "get_addendum_page" in [t["name"] for t in listed]
        r = srv.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                        "params": {"name": "get_addendum_page", "arguments": {"page": 4}}})["result"]
        assert r["isError"] is False
        body = json.loads(r["content"][0]["text"])
        assert body["page"] == 4 and body["addendum"] == "ADD-03" and body["label"].startswith("a tool result")
        assert body["image_regions"] and body["image_regions"][0]["region"] == 1
        imgs = [c for c in r["content"] if c["type"] == "image"]
        assert len(imgs) == 1 and imgs[0]["mimeType"] == "image/png"          # the page image itself
        r = srv.handle({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                        "params": {"name": "get_addendum_page", "arguments": {"page": 4, "region": 1}}})["result"]
        body = json.loads(r["content"][0]["text"])
        kinds = [c["kind"] for c in body["crops"]]
        assert kinds[0] == "region_crop" and r["isError"] is False
        assert 1 <= len([c for c in r["content"] if c["type"] == "image"]) <= 2   # the crop (and the native image)
        # a page or region the addendum does not have is refused; nothing else of the pack is served
        for args in ({"page": 9}, {"page": 4, "region": 2}, {"page": 1, "region": 1}):
            r = srv.handle({"jsonrpc": "2.0", "id": 4, "method": "tools/call",
                            "params": {"name": "get_addendum_page", "arguments": args}})["result"]
            assert r["isError"] is True, args
        # an image changed after the scope was written is an integrity failure, never served
        f = d / QR.SCOPE_DIR / sc["pages"][0]["image"]["file"]
        f.write_bytes(f.read_bytes() + b"\0")
        r = srv.handle({"jsonrpc": "2.0", "id": 5, "method": "tools/call",
                        "params": {"name": "get_addendum_page", "arguments": {"page": 1}}})["result"]
        assert r["isError"] is True and "integrity" in r["content"][0]["text"]
    finally:
        ws.addendum_scope = ws.addendum_scope_sha256 = None
    # with no addendum in scope (any other session) the tool serves nothing
    srv = Server(ws, tools=None)
    r = srv.handle({"jsonrpc": "2.0", "id": 6, "method": "tools/call",
                    "params": {"name": "get_addendum_page", "arguments": {"page": 1}}})["result"]
    assert r["isError"] is True and "no new addendum is in scope" in r["content"][0]["text"]


def test_a_scope_file_outside_a_quick_review_folder_is_refused(tmp_path, ws):
    from tenderpack.ai import quick_review as QR
    from tenderpack.ai.tools import ToolError, call_tool
    d, sc = _scope(tmp_path)
    other = tmp_path / "elsewhere"
    other.mkdir()
    (other / QR.SCOPE_FILE).write_text((d / QR.SCOPE_FILE).read_text(encoding="utf-8"), encoding="utf-8")
    ws.addendum_scope = str(other / QR.SCOPE_FILE)
    try:
        with pytest.raises(ToolError, match="quick review"):
            call_tool(ws, "get_addendum_page", {"page": 1}, caller="mcp")
    finally:
        ws.addendum_scope = None


def test_serve_mcp_takes_the_addendum_scope_and_serves_the_page_over_stdio(tmp_path, ws):
    from tenderpack.ai import quick_review as QR
    d, sc = _scope(tmp_path, pdf=PDF02)
    msgs = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-03-26"}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
             "params": {"name": "get_addendum_page", "arguments": {"page": 2}}}]
    env = dict(os.environ, PYTHONPATH=str(ROOT))
    r = subprocess.run([sys.executable, "-m", "tenderpack", "ai", "serve-mcp", "--evidence", str(ws.evidence),
                        "--pack", str(ws.pack), "--out", str(tmp_path / "st"), "--worklog", str(tmp_path / "wl"),
                        "--tools", ",".join(TOOLS5) + ",get_addendum_page", "--addendum-scope",
                        str(d / QR.SCOPE_FILE), "--addendum-scope-sha256", sc["file_sha256"]], input="\n".join(json.dumps(m) for m in msgs) + "\n",
                       capture_output=True, text=True, cwd=ROOT, env=env, timeout=120)
    assert r.returncode == 0, r.stderr[-2000:]
    out = [json.loads(x) for x in r.stdout.splitlines() if x.strip()]
    res = next(o for o in out if o.get("id") == 2)["result"]
    assert res["isError"] is False and json.loads(res["content"][0]["text"])["page"] == 2
    assert any(c["type"] == "image" for c in res["content"])


def test_the_host_quick_review_offers_the_page_tool_and_records_the_pages_it_read(ws, tmp_path):
    from tenderpack.ai import policy as P
    from tenderpack.ai import quick_review as QR
    staging = tmp_path / "staging" / "ai"
    seen = []

    def runner(cmd, input=None, **kw):
        seen.append({"cmd": cmd, "input": input})
        lines = [{"type": "system", "subtype": "init", "model": "fake-host-model", "tools": []},
                 {"type": "assistant", "message": {"content": [
                     {"type": "tool_use", "id": "t1", "name": "mcp__tenderpack__get_addendum_page",
                      "input": {"page": 4, "region": 1}}]}},
                 {"type": "result", "subtype": "success", "is_error": False, "num_turns": 2,
                  "result": json.dumps(BRIEFING), "usage": {"input_tokens": 10, "output_tokens": 5},
                  "modelUsage": {"fake-host-model": {}}}]
        return subprocess.CompletedProcess(cmd, 0, "\n".join(json.dumps(x) for x in lines), "")
    res = QR.run("ADD-03", PDF06, route="host", evidence=ws.evidence, pack=ws.pack, staging=staging,
                 worklog=tmp_path / "wl", ai_config=ROOT / "config/ai.yaml", runner=runner, claude_bin=sys.executable)
    assert res["exit_code"] == 0, res
    cmd = seen[0]["cmd"]
    allowed = cmd[cmd.index("--allowedTools") + 1].split(",")
    assert allowed == ["mcp__tenderpack__" + t for t in TOOLS5 + ("get_addendum_page",)]
    assert cmd[cmd.index("--system-prompt") + 1] == P.compose("quick_review", "host")
    mcp = json.loads(Path(cmd[cmd.index("--mcp-config") + 1]).read_text(encoding="utf-8"))
    args = mcp["mcpServers"]["tenderpack"]["args"]
    d = Path(res["dir"])
    assert args[args.index("--addendum-scope") + 1] == str((d / QR.SCOPE_FILE).resolve())
    # session 14 (F4; R4-5): the scope file's sha256 as written, handed to the server and recorded in the request
    sha = args[args.index("--addendum-scope-sha256") + 1]
    assert sha == QR.hashlib.sha256((d / QR.SCOPE_FILE).read_bytes()).hexdigest()
    assert "--submit-once" not in args
    from tenderpack.ai.providers.recorded import PACKET_MARK
    packet = json.loads(seen[0]["input"].split(PACKET_MARK, 1)[1])
    assert packet["page_images"]["tool"] == "get_addendum_page" and packet["page_images"]["image_pages"] == [4]
    req = json.loads((d / "request.json").read_text(encoding="utf-8"))
    assert req["images_not_attached"] == [] and req["addendum_scope"]["pages"] == 5
    assert req["addendum_scope"]["sha256"] == sha
    assert req["main_run_inputs_read"] == [] and req["kind"] == KIND
    b = json.loads((d / "briefing.json").read_text(encoding="utf-8"))
    assert b["kind"] == KIND
    assert b["page_images_read_through_tool"] == [{"page": 4, "region": 1}]
    assert not [n for n in b["not_read"] if n.get("page") == 4]            # page 4 was read through the tool
    md = (d / "briefing.md").read_text(encoding="utf-8")
    assert KIND in md.splitlines()[2] or KIND in md[:400]


def test_the_host_quick_review_lists_an_offered_image_page_it_did_not_read(ws, tmp_path):
    from tenderpack.ai import quick_review as QR

    def runner(cmd, input=None, **kw):
        lines = [{"type": "system", "subtype": "init", "model": "fake-host-model", "tools": []},
                 {"type": "result", "subtype": "success", "is_error": False, "num_turns": 1,
                  "result": json.dumps(BRIEFING), "usage": {"input_tokens": 10, "output_tokens": 5}}]
        return subprocess.CompletedProcess(cmd, 0, "\n".join(json.dumps(x) for x in lines), "")
    res = QR.run("ADD-03", PDF06, route="host", evidence=ws.evidence, pack=ws.pack, staging=tmp_path / "st" / "ai",
                 worklog=tmp_path / "wl", ai_config=ROOT / "config/ai.yaml", runner=runner, claude_bin=sys.executable)
    b = json.loads((Path(res["dir"]) / "briefing.json").read_text(encoding="utf-8"))
    nr = [n for n in b["not_read"] if n.get("page") == 4]
    assert len(nr) == 1 and "get_addendum_page" in nr[0]["reason"] and "did not request" in nr[0]["reason"]
    assert b["page_images_read_through_tool"] == []
