"""Session 12 (W4, part 3): the Mac setup, launcher and offline checks (scripts/mac/, docs/MAC_SETUP.md).

What is tested HERE (a Linux cloud container with no Ollama and no Mac): the scripts' syntax, that they phone nowhere
and never pull a model, that the pins agree with pyproject.toml, the dry-run setup checklist, the list of offline
checks and that the guide marks every check that needs the Mac PENDING ON THE MAC. `checks.sh --no-ai` was run once
by hand in the container (its output is in the session-12 report); a run on the Mac is PENDING."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAC = ROOT / "scripts/mac"
SCRIPTS = [MAC / "setup.sh", MAC / "checks.sh", MAC / "launch.command"]


def test_the_scripts_exist_are_executable_and_parse():
    for f in SCRIPTS:
        assert f.is_file() and f.stat().st_mode & 0o111, f
        r = subprocess.run(["bash", "-n", str(f)], capture_output=True, text=True)
        assert r.returncode == 0, (f, r.stderr)


def test_nothing_phones_home_or_pulls_a_model():
    for f in SCRIPTS:
        text = f.read_text(encoding="utf-8")
        assert not re.search(r"\b(curl|wget|nc|ssh|scp)\b", text), f
        assert not re.search(r"https?://", text), f
        assert "pip download" not in text and "ANTHROPIC_API_KEY" not in text and "OPENROUTER_API_KEY" not in text
        for line in text.splitlines():
            if "ollama pull" in line or "ollama run" in line:
                assert re.match(r"\s*(#|echo|printf|pend|pass|fail)", line), (f, line)
    assert "export TENDERPACK_OFFLINE=1" in (MAC / "checks.sh").read_text()
    assert "export TENDERPACK_OFFLINE=1" in (MAC / "launch.command").read_text()


def test_the_pins_come_from_pyproject():
    pin = re.search(r'"pymupdf==([\d.]+)"', (ROOT / "pyproject.toml").read_text()).group(1)
    assert pin == "1.28.2"
    setup = (MAC / "setup.sh").read_text()
    assert "pyproject.toml" in setup and "1.28.2" not in setup          # read from pyproject, never a second copy
    r = subprocess.run(["bash", str(MAC / "setup.sh"), "--dry-run"], capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stdout + r.stderr
    assert f"PASS     pyproject.toml pins pymupdf=={pin}" in r.stdout
    assert re.search(r"PASS     python >= 3\.11", r.stdout)
    assert "setup checklist:" in r.stdout and "FAIL     " not in r.stdout
    assert not (ROOT / ".venv").exists() or (ROOT / ".venv").is_dir()     # a dry run creates nothing new


def test_the_offline_checks_and_the_launcher_menu():
    r = subprocess.run(["bash", str(MAC / "checks.sh"), "--plan"], capture_output=True, text=True, timeout=60)
    plan = [x for x in r.stdout.splitlines() if x.strip()]
    # session 13: check 9 added (the installed versions against requirements.lock.txt, the locked set)
    assert r.returncode == 0 and [x.split()[0] for x in plan] == [str(i) for i in range(11)], plan    # session 13 (E159): check 10, the folder link
    menu = (MAC / "launch.command").read_text()
    for item in ("rebuild the evidence", "build the outputs", "strict check", "check-register", "AI routes",
                 "run an addendum offline", "local panel"):
        assert item in menu, item
    assert "tenderpack panel --help" in menu                             # detected, never assumed


def test_the_guide_lists_every_check_and_marks_what_needs_the_mac():
    doc = (ROOT / "docs/MAC_SETUP.md").read_text(encoding="utf-8")
    assert "bash scripts/mac/setup.sh" in doc and "bash scripts/mac/checks.sh" in doc and "launch.command" in doc
    assert doc.count("PENDING ON THE MAC") >= 5
    for word in ("ingest", "outputs --strict", "xlsx", "HTML", "ai routes --offline", "--offline", "ollama pull"):
        assert word in doc, word
    assert "never" in doc and "48 GB" in doc
