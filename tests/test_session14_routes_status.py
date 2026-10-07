"""Session 14 (W6, part 7, items 3, 4 and 6): the routes described accurately, the same everywhere, and one Mac checklist.

  * config/routes_status.yaml says, for each route, its status, where it ran, what WORKS, what was NEVER RUN and what
    is READY to try (the exact commands): Claude Code tested in the cloud container (sessions 10-13; the sealed
    blind-07 run from a twin of the interview folder), pending on the Mac; Codex the manual MCP path, built,
    unverified; the API key untested, ready with its dry run; OpenRouter blocked here, unverified, ready for a later key
    (its configuration and dry run); Ollama prepared for local use (the roles, the memory check, the pull commands as
    the person's choice; nothing pulled by the tool).
  * `ai routes` (and `--brief`, the launcher's list), the panel's addendum box, docs/AI_ROUTES.md section 1, the
    interview folder's README and docs/MAC_CHECKLIST.md say the same thing; nothing still says "sessions 10-12".
  * docs/MAC_CHECKLIST.md: one page, each step with its command and its expected line, each marked pending on the Mac.
  * Cost figures in the route docs are labelled provisional."""
from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
ROUTES = ("host", "codex", "anthropic", "openrouter", "ollama")


def _status() -> dict:
    return yaml.safe_load((ROOT / "config/routes_status.yaml").read_text(encoding="utf-8"))["routes"]


def _flat(x) -> str:
    return " ".join(str(x).split())


def test_each_route_says_what_works_what_never_ran_and_what_is_ready():
    st = _status()
    for name in ROUTES:
        for k in ("status", "where", "when", "result", "works", "never_run", "ready", "next"):
            assert st[name].get(k), (name, k)
    h, c, a, o, ol = (st[n] for n in ROUTES)
    assert h["status"] == "tested" and "sessions 10-13" in h["where"] and "not yet on the Mac" in h["where"]
    assert "twin of the interview folder" in h["where"] and "blind-07" in _flat(h["result"])
    assert "Mac" in h["never_run"] and "--route host" in _flat(h["ready"])
    assert c["status"] == "built, unverified" and "Codex session" in c["never_run"]
    assert "--host-manual" in _flat(c["ready"]) and "submit-batch" in _flat(c["ready"])
    assert "~/.codex/config.toml" in _flat(c["ready"]) and "serve-mcp" in _flat(c["ready"])
    assert a["status"] == "untested" and "ai capabilities --route anthropic --model claude-opus-5-5" in _flat(a["ready"])
    assert "dry run" in _flat(a["ready"]) and "routes.anthropic.caps" in _flat(a["ready"])
    assert o["status"] == "blocked here, unverified" and "OPENROUTER_API_KEY" in _flat(o["ready"])
    assert "routes.openrouter.caps" in _flat(o["ready"]) and "ai capabilities --route openrouter" in _flat(o["ready"])
    assert ol["status"] == "pending on the Mac" and "prepared for local use" in _flat(ol["works"])
    for word in ("routes.ollama.models", "memory", "three check levels"):
        assert word in _flat(ol["works"]), word
    assert "ollama pull" in _flat(ol["ready"]) and "your choice" in _flat(ol["ready"]) and "never pulls" in _flat(ol["ready"])


def _routes_json() -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith(("TENDERPACK_", "ANTHROPIC", "OPENROUTER"))}
    env["TENDERPACK_OLLAMA_URL"] = "http://127.0.0.1:9"
    r = subprocess.run([PY, "-m", "tenderpack", "ai", "routes", "--json"], cwd=ROOT, capture_output=True, text=True,
                       env=env, timeout=120)
    return json.loads(r.stdout)


def test_ai_routes_the_launcher_list_and_the_panel_say_what_the_record_says():
    st = _status()
    data = _routes_json()
    rows = {r["route"]: r for r in data["routes"]}
    for name in ROUTES:
        for k in ("works", "never_run", "ready"):
            assert rows[name][k] == _flat(st[name][k]), (name, k)
        assert rows[name]["status"]["status"] == st[name]["status"]
    assert "sessions 10-13" in rows["host"]["verified"] and "PENDING ON THE MAC" in rows["host"]["verified"]
    assert rows["anthropic"]["verified"].startswith("untested")
    assert rows["openrouter"]["verified"].startswith("blocked here, unverified")
    assert rows["ollama"]["verified"].startswith("prepared for local use")
    env = {k: v for k, v in os.environ.items() if not k.startswith(("TENDERPACK_", "ANTHROPIC", "OPENROUTER"))}
    env["TENDERPACK_OLLAMA_URL"] = "http://127.0.0.1:9"
    brief = subprocess.run([PY, "-m", "tenderpack", "ai", "routes", "--brief"], cwd=ROOT, capture_output=True,
                           text=True, env=env, timeout=120).stdout
    full = subprocess.run([PY, "-m", "tenderpack", "ai", "routes"], cwd=ROOT, capture_output=True, text=True, env=env,
                          timeout=120).stdout
    for name in ROUTES:
        assert f"[{st[name]['status']}; last exercised: {_flat(st[name]['where'])}" in brief, name
        assert f"  ready:    {_flat(st[name]['ready'])}" in full, name
    from tenderpack.panel import views as V
    choices, _, _ = V.route_choices(data, True, False)
    by = {c["value"]: c for c in choices}
    for name in ROUTES:
        assert st[name]["status"] in by[name]["label"], (name, by[name]["label"])


def test_the_docs_and_the_readme_quote_the_same_record():
    st = _status()
    doc = (ROOT / "docs/AI_ROUTES.md").read_text(encoding="utf-8")
    sec = doc[doc.index("## 1. Two kinds of route"):doc.index("## 7. Recorded route")]
    table = sec[sec.index("| Route | Status (config/routes_status.yaml)"):]
    for name in ROUTES:
        row = next(ln for ln in table.splitlines() if ln.startswith(f"| `{name}`"))
        assert row.split("|")[2].strip().startswith(st[name]["status"]), (name, row)
    assert "sessions 10–13" in table and "blind-07" in table
    for f in ("docs/AI_ROUTES.md", "docs/MAC_SETUP.md", "docs/VERIFY_ON_MAC.md", "docs/MAC_CHECKLIST.md",
              "tenderpack/ai/cli_routes.py", "scripts/make_interview_folder.py", "config/routes_status.yaml"):
        text = (ROOT / f).read_text(encoding="utf-8")
        assert not re.search(r"sessions 10[-–]1[12]\b|cloud container of sessions 10-12", text), f
    spec = importlib.util.spec_from_file_location("s14_mif", ROOT / "scripts/make_interview_folder.py")
    mif = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mif)
    readme = mif.readme("X", "abc1234", "", ["tests/test_session14_routes_status.py"], [], 10, {"provisions": 12})
    for name in ROUTES:
        for k in ("status", "works", "never_run", "ready"):
            assert _flat(st[name][k]) in readme, (name, k)
    # cost: provisional wherever the route sections speak of prices
    assert "provisional" in sec[sec.index("## 4."):sec.index("## 5.")]


def test_the_mac_checklist_is_one_page_with_commands_expected_lines_and_pending_marks():
    text = (ROOT / "docs/MAC_CHECKLIST.md").read_text(encoding="utf-8")
    assert len(text.splitlines()) <= 40 and len(text) <= 9000                  # one page
    rows = [ln for ln in text.splitlines() if re.match(r"^\| \d+ \|", ln)]
    assert len(rows) >= 10
    for ln in rows:
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", ln.strip().strip("|"))]
        assert len(cells) == 5, ln
        assert "`" in cells[2] or "launch.command" in cells[2] or "launcher" in cells[2], ln     # a command
        assert cells[3], ln                                                                  # the expected line
        assert "PENDING ON THE MAC" in cells[4], ln                                          # never claimed done
    for word in ("setup.sh", "checks.sh --no-ai", "run_smoke.sh", "launch.command", "level 1 (connectivity)",
                 "level 2 (valid content)", "level 3 (complete workflow)", "host", "codex", "submit-batch",
                 "ai capabilities --route anthropic", "provisional", "cloud-tested"):
        assert word in text, word
