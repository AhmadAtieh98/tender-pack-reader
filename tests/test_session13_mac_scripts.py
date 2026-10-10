"""Session 13 (part 5): the Mac scripts' operating reliability, the routes' honest status and offline mode.

  * launch.command: every failure says exactly what is wrong and the ONE command to run next (no .venv, the wrong
    folder, a python that does not run, a copied .venv, a busy panel port, a run that is already live), checked with a
    bash harness that builds each condition in a temporary folder (TENDERPACK_PY for the interpreter).
  * checks.sh: a check passes only when the command's exit code is the expected one AND the blocker lines in its log
    are exactly the expected approval blockers; a defect blocker fails the check and is printed. A fake `tenderpack`
    (TENDERPACK_PY) makes each case. The installed versions are compared with requirements.lock.txt (lockcheck.py).
  * checks 6/7 (Ollama): `tenderpack ai ollama-models` discovers the INSTALLED models (/api/tags), reads each one's
    capabilities and context (/api/show), compares its estimated memory with the machine's, and says which can serve
    each phase; it never pulls (a fake Ollama server here; /api/pull answers 403 and is never called).
  * config/routes_status.yaml: where and when each route (Claude Code host, Codex, the API key, OpenRouter, Ollama)
    was last exercised and with what result; `tenderpack ai routes` prints it beside the live availability, the
    launcher's menu and the panel's addendum box show the usable routes and explain the others.
  * Keys: the environment or a chmod-600 file OUTSIDE the folder (tenderpack/ai/keys.py); never written to a log.
  * Offline: every provider / host-session construction site in tenderpack/ is enumerated; a new one without the
    offline guard fails the test."""
from __future__ import annotations

import ast
import json
import os
import re
import shutil
import socket
import stat
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
MAC = ROOT / "scripts/mac"
PY = sys.executable


def _bash(script: Path, *args, env=None, stdin: str = "", cwd=None, timeout=120):
    e = {k: v for k, v in os.environ.items() if not k.startswith("TENDERPACK_")}
    e.update(env or {})
    return subprocess.run(["bash", str(script), *args], input=stdin, capture_output=True, text=True, env=e,
                          cwd=cwd, timeout=timeout)


# ---------------------------------------------------------------------------------------------- the launcher

def _folder(tmp: Path, venv: bool = True) -> Path:
    """A minimal tenderpack folder: the launcher in scripts/mac, pyproject.toml, a tenderpack/ that imports."""
    f = tmp / "tp"
    (f / "scripts/mac").mkdir(parents=True)
    shutil.copy(MAC / "launch.command", f / "scripts/mac/launch.command")
    (f / "pyproject.toml").write_text('[project]\nname = "tenderpack"\n', encoding="utf-8")
    shutil.copytree(ROOT / "tenderpack", f / "tenderpack", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(ROOT / "config", f / "config")
    if venv:                                  # a stand-in .venv whose python is this test session's interpreter
        (f / ".venv/bin").mkdir(parents=True)
        (f / ".venv/bin/python").write_text(f'#!/usr/bin/env bash\nexec "{PY}" "$@"\n', encoding="utf-8")
        (f / ".venv/bin/python").chmod(0o755)
        (f / ".venv/pyvenv.cfg").write_text(f"home = {Path(PY).parent}\n", encoding="utf-8")
    return f


def _problem_and_next(out: str) -> tuple[str, str]:
    p = re.search(r"^PROBLEM: (.+)$", out, re.M)
    n = re.search(r"^NEXT:    (.+)$", out, re.M)
    assert p and n, out
    return p.group(1), n.group(1)


def test_launcher_without_a_venv_names_the_setup_command(tmp_path):
    f = _folder(tmp_path, venv=False)
    r = _bash(f / "scripts/mac/launch.command")
    assert r.returncode == 1
    problem, nxt = _problem_and_next(r.stdout)
    assert "no .venv" in problem and str(f) in problem
    assert nxt == f'bash "{f}/scripts/mac/setup.sh"'


def test_launcher_outside_the_folder_says_so(tmp_path):
    f = tmp_path / "loose/scripts/mac"
    f.mkdir(parents=True)
    shutil.copy(MAC / "launch.command", f / "launch.command")
    r = _bash(f / "launch.command")
    assert r.returncode == 1
    problem, nxt = _problem_and_next(r.stdout)
    assert "not inside a tenderpack folder" in problem and "pyproject.toml" in problem
    assert "scripts/mac/launch.command" in nxt


def test_launcher_with_a_python_that_does_not_run(tmp_path):
    f = _folder(tmp_path)
    (f / ".venv/bin/python").unlink()
    os.symlink(tmp_path / "gone/python3.12", f / ".venv/bin/python")          # the base interpreter was removed
    r = _bash(f / "scripts/mac/launch.command")
    assert r.returncode == 1
    problem, nxt = _problem_and_next(r.stdout)
    assert ".venv/bin/python does not run" in problem
    assert nxt == f'rm -rf "{f}/.venv" && bash "{f}/scripts/mac/setup.sh"'
    # TENDERPACK_PY naming a missing interpreter is reported as itself, not as a missing .venv
    r = _bash(f / "scripts/mac/launch.command", env={"TENDERPACK_PY": str(tmp_path / "nope/python")})
    problem, nxt = _problem_and_next(r.stdout)
    assert "TENDERPACK_PY" in problem and "does not run" in problem and "unset TENDERPACK_PY" in nxt


def test_launcher_refuses_a_venv_built_in_another_folder(tmp_path):
    f = _folder(tmp_path)
    (f / ".venv/bin/activate").write_text('VIRTUAL_ENV="/Users/someone/elsewhere/.venv"\nexport VIRTUAL_ENV\n',
                                          encoding="utf-8")
    r = _bash(f / "scripts/mac/launch.command")
    assert r.returncode == 1
    problem, nxt = _problem_and_next(r.stdout)
    assert "built in another folder" in problem and "/Users/someone/elsewhere/.venv" in problem
    assert nxt == f'rm -rf "{f}/.venv" && bash "{f}/scripts/mac/setup.sh"'


def test_launcher_with_dependencies_that_do_not_import(tmp_path):
    f = _folder(tmp_path)
    fake = tmp_path / "py-noimport"
    fake.write_text(f'#!/usr/bin/env bash\nif [ "$1" = "-c" ] && [[ "$2" == *pymupdf* ]]; then echo "ModuleNotFoundError: '
                    f"No module named 'pymupdf'\" >&2; exit 1; fi\nexec \"{PY}\" \"$@\"\n", encoding="utf-8")
    fake.chmod(0o755)
    r = _bash(f / "scripts/mac/launch.command", env={"TENDERPACK_PY": str(fake)})
    problem, nxt = _problem_and_next(r.stdout)
    assert "do not import" in problem and "pymupdf" in problem
    assert nxt == f'bash "{f}/scripts/mac/setup.sh"'


def test_launcher_menu_offers_connected_and_offline_and_lists_the_routes(tmp_path):
    f = _folder(tmp_path)
    r = _bash(f / "scripts/mac/launch.command", stdin="2\nq\n")
    assert r.returncode == 0, r.stdout + r.stderr
    out = r.stdout
    assert "connected" in out and "offline" in out
    assert "mode: offline" in out                                     # the choice was taken
    for route in ("host", "codex", "anthropic", "openrouter", "ollama"):
        assert re.search(rf"^\s+{route}\b", out, re.M), (route, out)
    assert "not usable now" in out                                      # the unavailable ones are explained


def test_launcher_reports_a_busy_panel_port(tmp_path):
    f = _folder(tmp_path)
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    s.listen(1)
    port = s.getsockname()[1]
    try:
        r = _bash(f / "scripts/mac/launch.command", env={"TENDERPACK_PANEL_PORT": str(port)}, stdin="2\n7\nq\n")
    finally:
        s.close()
    problem, nxt = _problem_and_next(r.stdout)
    assert f"127.0.0.1:{port} is already in use" in problem
    assert "TENDERPACK_PANEL_PORT" in nxt


def test_launcher_reports_a_run_that_is_already_live(tmp_path):
    f = _folder(tmp_path)
    (f / "staging/ai").mkdir(parents=True)
    pdf = tmp_path / "a.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")
    lock = {"addendum": "ADD-03", "host": socket.gethostname(), "pid": os.getpid(), "run_id": "ADD-03-live-1",
            "route": "ollama", "created_epoch": __import__("time").time(), "token": "x", "scope": "run"}
    (f / "staging/ai/.lock-ADD-03").write_text(json.dumps(lock), encoding="utf-8")
    r = _bash(f / "scripts/mac/launch.command", stdin=f"2\n6\nADD-03\n{pdf}\nq\n")
    problem, nxt = _problem_and_next(r.stdout)
    assert "ADD-03 is already live" in problem and "ADD-03-live-1" in problem
    assert "ai run-status ADD-03-live-1" in nxt


# ---------------------------------------------------------------------------------------------- checks.sh

FAKE = r'''#!/usr/bin/env bash
# a fake `tenderpack` for checks.sh (session 13 tests): -m tenderpack <cmd> answers per FAKE_CASE; anything else runs
# on the real interpreter (openpyxl, html.parser, lockcheck.py)
REAL="__REAL__"
if [ "$1" = "-m" ] && [ "$2" = "tenderpack" ]; then
  shift 2
  case "$1" in
    ingest)
      if [ "$FAKE_CASE" = "ingest_fails_but_prints_ok" ]; then echo "STRUCTURE OK. units: 10"; exit 2; fi
      echo "STRUCTURE OK. units: 1234  ->  build/units.md"; exit 0 ;;
    outputs)
      strict=0; for a in "$@"; do [ "$a" = "--strict" ] && strict=1; done
      echo "C1 pass  ok"
      echo "RELEASE BLOCKER [approval] 205 of 205 register rows not accepted by a person"
      echo "RELEASE BLOCKER [approval] 37 of 37 amendment op(s) not accepted by a person"
      if [ "$FAKE_CASE" = "defect" ]; then echo "RELEASE BLOCKER [coverage] ADD-02 is PARTIAL; unresolved provisions: ['ADD-02:9.9']"; fi
      if [ $strict -eq 1 ]; then echo "RELEASE REFUSED (--strict); previous outputs kept; candidate in: x"; exit 3; fi
      echo "OUTPUTS PUBLISHED (WORKING DRAFT): out"
      if [ "$FAKE_CASE" = "outputs_exit1" ]; then exit 1; fi
      exit 0 ;;
    panel) exit 0 ;;
    *) echo "fake: $*"; exit 0 ;;
  esac
fi
exec "$REAL" "$@"
'''


def _fake_py(tmp: Path) -> Path:
    p = tmp / "fakepy"
    p.write_text(FAKE.replace("__REAL__", PY), encoding="utf-8")
    p.chmod(0o755)
    return p


def _checks(tmp: Path, case: str):
    env = {"TENDERPACK_PY": str(_fake_py(tmp)), "FAKE_CASE": case, "TMPDIR": str(tmp)}
    return _bash(MAC / "checks.sh", "--no-ai", env=env, timeout=300)


def _line(out: str, n: int) -> list[str]:
    return [ln for ln in out.splitlines() if re.match(rf"^(PASS|FAIL|PENDING) +{n} ", ln)]


def test_checks_pass_only_on_the_expected_exit_and_the_approval_blockers(tmp_path):
    r = _checks(tmp_path, "ok")
    for n in (1, 2, 3):
        assert _line(r.stdout, n) and all(x.startswith("PASS") for x in _line(r.stdout, n)), (n, r.stdout)
    assert "2 approval blocker(s)" in "\n".join(_line(r.stdout, 3))


def test_a_defect_blocker_fails_the_check_and_is_printed(tmp_path):
    r = _checks(tmp_path, "defect")
    for n in (2, 3):
        lines = _line(r.stdout, n)
        assert lines and lines[0].startswith("FAIL"), (n, r.stdout)
    assert "RELEASE BLOCKER [coverage] ADD-02 is PARTIAL" in r.stdout
    assert r.returncode != 0


def test_a_non_zero_exit_fails_the_check_whatever_the_log_says(tmp_path):
    r = _checks(tmp_path, "outputs_exit1")
    assert _line(r.stdout, 2)[0].startswith("FAIL") and "exit 1" in _line(r.stdout, 2)[0], r.stdout
    r = _checks(tmp_path, "ingest_fails_but_prints_ok")
    assert _line(r.stdout, 1)[0].startswith("FAIL") and "exit 2" in _line(r.stdout, 1)[0], r.stdout


def test_no_exit_code_is_read_after_a_pipe():
    text = (MAC / "checks.sh").read_text(encoding="utf-8")
    lines = text.splitlines()
    n = 0
    for i, ln in enumerate(lines):
        if "$?" not in ln or ln.lstrip().startswith("#"):
            continue
        n += 1
        before = ln.split("$?")[0]
        cmd = before if re.search(r"\S", re.sub(r"^\s*(RC=|\[|if)\s*", "", before)) and ";" in before else lines[i - 1]
        assert "|" not in re.sub(r"\|\|", "", cmd.split("#")[0]), (i + 1, ln, cmd)
    assert n >= 8                                                      # every check captures its own exit code


def test_lockcheck_compares_installed_versions_with_the_lock(tmp_path):
    good = subprocess.run([PY, str(MAC / "lockcheck.py"), str(ROOT / "requirements.lock.txt")], capture_output=True,
                          text=True)
    req = tmp_path / "req.txt"
    req.write_text("pyyaml==0.0.1\n    # via tenderpack\ncolorama==0.4.6 ; sys_platform == 'win32'\n", encoding="utf-8")
    bad = subprocess.run([PY, str(MAC / "lockcheck.py"), str(req)], capture_output=True, text=True)
    assert bad.returncode == 1 and "pyyaml" in bad.stdout and "0.0.1" in bad.stdout, bad.stdout
    assert "colorama" not in bad.stdout                                 # a marker that does not apply is skipped
    assert good.returncode in (0, 1) and ("match the lock" in good.stdout or "MISMATCH" in good.stdout)


def test_checks_has_the_lock_check_in_its_plan():
    r = _bash(MAC / "checks.sh", "--plan")
    plan = [x for x in r.stdout.splitlines() if x.strip()]
    assert any("requirements.lock.txt" in x for x in plan), plan


@pytest.mark.skipif(os.environ.get("TENDERPACK_TEST_UV_SYNC") != "1" or not shutil.which("uv"),
                    reason="opt-in (TENDERPACK_TEST_UV_SYNC=1): runs setup.sh with uv offline from the local uv cache")
def test_setup_builds_the_locked_environment_offline_from_the_cache(tmp_path):
    f = tmp_path / "tp"
    (f / "scripts/mac").mkdir(parents=True)
    for n in ("setup.sh", "lockcheck.py"):
        shutil.copy(MAC / n, f / "scripts/mac" / n)
    for n in ("pyproject.toml", "uv.lock", "requirements.lock.txt"):
        shutil.copy(ROOT / n, f / n)
    shutil.copytree(ROOT / "tenderpack", f / "tenderpack", ignore=shutil.ignore_patterns("__pycache__"))
    env = {"UV_OFFLINE": "1", "HOME": os.environ.get("HOME", "")}
    if os.environ.get("TENDERPACK_SETUP_PYTHON"):                     # the interpreter the uv cache was built for
        env["TENDERPACK_SETUP_PYTHON"] = os.environ["TENDERPACK_SETUP_PYTHON"]
    r = _bash(f / "scripts/mac/setup.sh", env=env, timeout=600)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "PASS     installed versions match requirements.lock.txt" in r.stdout
    assert "uv sync --frozen" in r.stdout


# ---------------------------------------------------------------------------------------------- Ollama discovery

def test_ollama_discovery_reports_each_installed_model_per_phase_and_never_pulls():
    sys.path.insert(0, str(ROOT / "tests/fixtures"))
    from fake_ollama import FakeOllama, show
    from tenderpack.ai import config as C
    from tenderpack.ai.providers import ollama as O
    fake = FakeOllama({"qwen3-vl:32b": show(caps=("completion", "vision", "tools"), params="33B", context=262144),
                       "tiny:1b": show(caps=("completion",), params="1B", context=8192),
                       "huge:235b": show(caps=("completion", "tools"), params="235B", quant="Q4_K_M")})
    url = fake.start()
    try:
        cfg = C.load(ROOT / "config/ai.yaml")
        rep = O.discover(cfg, env={"TENDERPACK_OLLAMA_URL": url}, memory_bytes=48 * 1024 ** 3)
    finally:
        fake.stop()
    assert rep["reachable"] and sorted(m["id"] for m in rep["models"]) == ["huge:235b", "qwen3-vl:32b", "tiny:1b"]
    by = {m["id"]: m for m in rep["models"]}
    assert by["qwen3-vl:32b"]["phases"]["reading"]["ok"] and by["qwen3-vl:32b"]["phases"]["analysis"]["ok"]
    assert not by["tiny:1b"]["phases"]["reading"]["ok"] and "vision" in by["tiny:1b"]["phases"]["reading"]["why"]
    assert not by["tiny:1b"]["phases"]["analysis"]["ok"] and "tools" in by["tiny:1b"]["phases"]["analysis"]["why"]
    assert "context" in by["tiny:1b"]["phases"]["critic"]["why"]          # 8192 < the configured bound
    assert by["huge:235b"]["memory"]["fits"] is False and not by["huge:235b"]["phases"]["analysis"]["ok"]
    assert rep["phases"]["reading"] == ["qwen3-vl:32b"] and rep["phases"]["analysis"] == ["qwen3-vl:32b"]
    assert rep["machine"]["memory_gb"] == 48.0 and "detected" in rep["machine"]["source"]
    assert not any(p == "/api/pull" for p in fake.paths())


def test_ollama_discovery_unreachable_is_reported_not_raised():
    from tenderpack.ai import config as C
    from tenderpack.ai.providers import ollama as O
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    rep = O.discover(C.load(ROOT / "config/ai.yaml"), env={"TENDERPACK_OLLAMA_URL": f"http://127.0.0.1:{port}"})
    assert rep["reachable"] is False and "could not be reached" in rep["error"] and rep["models"] == []


def test_the_ollama_checks_use_the_discovery_and_capture_its_exit_code():
    text = (MAC / "checks.sh").read_text(encoding="utf-8")
    assert "ai ollama-models" in text
    assert "ollama pull" not in re.sub(r"(echo|pend|pass|fail|#)[^\n]*", "", text)
    assert "rehearsals/" not in text                                    # the folder has no rehearsals: the smoke PDF


# ---------------------------------------------------------------------------------------------- route status

def test_routes_status_file_covers_every_route_honestly():
    st = yaml.safe_load((ROOT / "config/routes_status.yaml").read_text(encoding="utf-8"))
    routes = st["routes"]
    assert set(routes) >= {"host", "codex", "anthropic", "openrouter", "ollama"}
    assert routes["host"]["status"] == "tested" and "sessions 10" in routes["host"]["where"]
    assert routes["codex"]["status"] == "built, unverified"
    assert routes["anthropic"]["status"] == "untested"
    assert routes["openrouter"]["status"].startswith("blocked")
    assert routes["ollama"]["status"].startswith("pending")
    for name, r in routes.items():
        for k in ("status", "where", "when", "result", "next"):
            assert r.get(k), (name, k)
    assert "connected" in st["order"][0] or st["first"] == "host"


def test_ai_routes_prints_the_status_beside_the_live_availability(tmp_path):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("TENDERPACK_", "ANTHROPIC", "OPENROUTER"))}
    env["TENDERPACK_OLLAMA_URL"] = "http://127.0.0.1:9"
    r = subprocess.run([PY, "-m", "tenderpack", "ai", "routes", "--json"], cwd=ROOT, capture_output=True, text=True,
                       env=env, timeout=120)
    data = json.loads(r.stdout)
    rows = {x["route"]: x for x in data["routes"]}
    assert set(rows) >= {"host", "codex", "anthropic", "openrouter", "ollama"}
    for name in ("host", "codex", "anthropic", "openrouter", "ollama"):
        assert rows[name]["status"]["status"] and "available" in rows[name] and "why" in rows[name], name
    assert rows["anthropic"]["available"] is False and "ANTHROPIC_API_KEY" in rows["anthropic"]["why"]
    assert rows["ollama"]["available"] is False
    text = subprocess.run([PY, "-m", "tenderpack", "ai", "routes"], cwd=ROOT, capture_output=True, text=True,
                          env=env, timeout=120).stdout
    assert "last exercised:" in text and "usable now:" in text and "codex" in text


def test_panel_route_choices_show_every_route_with_its_status_and_why():
    from tenderpack.panel import views as V
    routes = {"offline": None, "routes": [
        {"route": "host", "available": True, "why": "", "status": {"status": "tested"}},
        {"route": "codex", "available": False, "why": "the workflow starts Claude Code only", "status": {"status": "built, unverified"}},
        {"route": "anthropic", "available": False, "why": "no key: set ANTHROPIC_API_KEY", "status": {"status": "untested"}},
        {"route": "openrouter", "available": False, "why": "no key", "status": {"status": "blocked here, unverified"}},
        {"route": "ollama", "available": False, "why": "", "status": {"status": "pending on the Mac"},
         "error": "Ollama could not be reached", "models": []}]}
    choices, default, _ = V.route_choices(routes, True, False)
    by = {c["value"]: c for c in choices}
    assert set(by) >= {"host", "codex", "anthropic", "openrouter", "ollama"}
    assert by["host"]["available"] and default == "host" and "tested" in by["host"]["label"]
    assert not by["anthropic"]["available"] and "ANTHROPIC_API_KEY" in by["anthropic"]["why"]
    assert "untested" in by["anthropic"]["label"] and "built, unverified" in by["codex"]["label"]
    assert not by["ollama"]["available"] and "could not be reached" in by["ollama"]["why"]
    html = V.addendum_box("/t/x/", routes, None, "ADD-03", True, False, 50)
    assert 'value="codex"' in html and 'value="anthropic"' in html and "disabled" in html


# ---------------------------------------------------------------------------------------------- keys

SENTINEL = "KEYVALUE-s13-Zq81Lm4Hn0Pt7Rw2"                              # matches no generic key pattern on purpose


def test_a_key_comes_from_the_environment_or_a_private_file_outside_the_folder(tmp_path, monkeypatch):
    from tenderpack.ai import keys
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    kf = tmp_path / "home/.config/tenderpack/keys.env"
    kf.parent.mkdir(parents=True)
    kf.write_text(f"ANTHROPIC_API_KEY={SENTINEL}\n", encoding="utf-8")
    kf.chmod(0o644)
    with pytest.raises(keys.KeyFileError, match="chmod 600"):
        keys.get("ANTHROPIC_API_KEY", env={}, path=kf)
    kf.chmod(0o600)
    assert keys.get("ANTHROPIC_API_KEY", env={}, path=kf) == SENTINEL
    assert keys.get("ANTHROPIC_API_KEY", env={"ANTHROPIC_API_KEY": "from-env-12345"}, path=kf) == "from-env-12345"
    inside = ROOT / "config" / "keys.env"                               # inside the folder: refused, never read
    with pytest.raises(keys.KeyFileError, match="outside"):
        keys.check_location(inside)
    assert keys.source("ANTHROPIC_API_KEY", env={}, path=kf) == f"file {kf}"


def test_no_key_value_is_written_to_a_log(tmp_path, monkeypatch):
    from tenderpack.ai import keys
    from tenderpack.ai.providers.anthropic import AnthropicProvider
    from tenderpack.ai.providers.base import ProviderError
    from tenderpack.ai.runlog import RunLog
    kf = tmp_path / "keys.env"
    kf.write_text(f"ANTHROPIC_API_KEY={SENTINEL}\n", encoding="utf-8")
    kf.chmod(0o600)
    monkeypatch.setenv("TENDERPACK_KEYS_FILE", str(kf))
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    seen = {}

    def fetch(method, url, headers, body, timeout):
        seen["headers"] = dict(headers)
        raise ProviderError("http_401", f"unauthorized: {json.dumps(headers)}", False, 401)
    prov = AnthropicProvider("claude-x", {"api_key_env": "ANTHROPIC_API_KEY"}, {}, env={"TENDERPACK_KEYS_FILE": str(kf)},
                             fetch=fetch)
    assert seen == {} and prov.key_source() == f"file {kf}"
    caps = None
    try:
        caps = prov.capabilities()
    except ProviderError as e:
        caps = e
    assert seen["headers"]["x-api-key"] == SENTINEL                      # the key reaches the request header only
    log = RunLog("r1", [tmp_path / "log.jsonl"])
    log.event("capabilities", error=str(caps), headers=seen["headers"], note=f"key was {SENTINEL}",
              nested=[{"text": f"Authorization: {SENTINEL}"}])
    written = (tmp_path / "log.jsonl").read_text(encoding="utf-8")
    assert SENTINEL not in written and "[REDACTED]" in written
    # and statically: no provider puts its key attribute anywhere but a request header
    for f in (ROOT / "tenderpack/ai/providers").glob("*.py"):
        for i, ln in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if "self._key" in ln and "self._key =" not in ln and "self._key_source" not in ln:
                assert re.search(r"(if not self\._key|\"x-api-key\": self\._key|authorization\": f\"Bearer "
                                 r"\{self\._key\})", ln, re.I), (f.name, i, ln)


# ---------------------------------------------------------------------------------------------- offline call sites

GUARDED_CONSTRUCTORS = {
    # constructor -> where its offline guard is (checked below to be the first thing it does)
    "HostSession": "hostsession.HostSession.__init__ -> offline.check_host_session",
    "AnswerSession": "a HostSession subclass (the same __init__)",
    "PlainSession": "hostsession.PlainSession.__init__ -> offline.check_host_session",
    "make": "providers.make -> offline.check_route",
}
# Direct adapter construction bypasses providers.make: allowed only where it is local or a test replay.
DIRECT_OK = {
    ("tenderpack/ai/providers/__init__.py", "AnthropicProvider"), ("tenderpack/ai/providers/__init__.py", "OpenRouterProvider"),
    ("tenderpack/ai/providers/__init__.py", "OllamaProvider"), ("tenderpack/ai/providers/__init__.py", "HostProvider"),
    ("tenderpack/ai/providers/__init__.py", "RecordedProvider"),
    ("tenderpack/ai/providers/ollama.py", "OllamaProvider"),          # check_models / discover: loopback /api/show only
    ("tenderpack/ai/workflow.py", "RecordedProvider"),                # the recorded test replay (no network)
}
KNOWN_SITES = {
    ("tenderpack/ai/cli.py", "make"), ("tenderpack/ai/cli_routes.py", "make"), ("tenderpack/ai/cli_routes.py", "HostSession"),
    ("tenderpack/ai/critic.py", "make"), ("tenderpack/ai/critic.py", "PlainSession"),
    ("tenderpack/ai/requests.py", "PlainSession"),
    ("tenderpack/ai/workflow.py", "make"), ("tenderpack/ai/workflow.py", "HostSession"),
    ("tenderpack/ai/workflow.py", "AnswerSession"),
    # session 13, part 4 (implementer E): the AI quick review builds its provider through providers.make (the offline
    # check inside make, and offline.check_route before it) and its ONE host session as an AnswerSession (whose
    # HostSession constructor runs check_host_session first)
    ("tenderpack/ai/quick_review.py", "make"), ("tenderpack/ai/quick_review.py", "_session_class"),
}
PROCESS_SITES = {
    "tenderpack/ai/codex.py": "guarded by check_host_session in the transport and parent session; watchdog is local",
    "tenderpack/interview.py": "AI CLI delegates to its offline guards; caffeinate is local",   # subprocess users in tenderpack/: none of them may start the host CLI except the guarded sessions
    "tenderpack/cli.py": "git log (read only)",
    "tenderpack/ai/candidate.py": "python -m tenderpack.ai.candidate build-before (deterministic, no model)",
    # session 13 (implementer A, merged after this test was written): the run's code identity reads `git rev-parse HEAD`
    # and `git status --porcelain` (local, read only; no hosted process)
    "tenderpack/ai/checkpoint.py": "git rev-parse / git status (read only, local: the run's code identity)",
    "tenderpack/ai/critic.py": "runner of the host critic, constructed after check_host_session",
    "tenderpack/ai/hostsession.py": "the guarded host sessions themselves",
    "tenderpack/panel/jobs.py": "python -m tenderpack ... (the CLI's own guards; --offline passed by the panel)",
    "tenderpack/panel/server.py": "python -m tenderpack ai routes --json / ai run --help (read only)",
}


def _calls(path: Path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Call) and isinstance(fn.func, ast.Name):   # session 14: a factory call, f(...)(...)
                fn = fn.func
            name = fn.attr if isinstance(fn, ast.Attribute) else fn.id if isinstance(fn, ast.Name) else None
            if name:
                yield name, node.lineno


SESSION_CLASSES = ("HostSession", "AnswerSession", "PlainSession")


def _session_names(path: Path) -> set[str]:
    """Session 14: the names under which a guarded session is constructed in `path`: the session classes themselves, a
    subclass of one of them (its constructor is the parent's, which runs the guard first), and a factory function that
    defines such a subclass and returns it (W5's `_session_class(HS)(...)` in quick_review.py)."""
    names = set(SESSION_CLASSES)
    tree = ast.parse(path.read_text(encoding="utf-8"))

    def is_session_base(b) -> bool:
        return (isinstance(b, ast.Name) and b.id in SESSION_CLASSES) or \
               (isinstance(b, ast.Attribute) and b.attr in SESSION_CLASSES)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and any(is_session_base(b) for b in node.bases):
            names.add(node.name)
        if isinstance(node, ast.FunctionDef) and any(isinstance(c, ast.ClassDef) and any(is_session_base(b) for b in c.bases)
                                                     for c in ast.walk(node)):
            names.add(node.name)
    return names


def test_every_provider_and_host_session_construction_goes_through_the_offline_guard():
    adapters = {"AnthropicProvider", "OpenRouterProvider", "OllamaProvider", "HostProvider", "RecordedProvider"}
    sites, direct, procs = set(), set(), set()
    for f in sorted((ROOT / "tenderpack").rglob("*.py")):
        rel = f.relative_to(ROOT).as_posix()
        text = f.read_text(encoding="utf-8")
        session_names = _session_names(f)            # session 14: subclasses and factories count under their own names
        for name, line in _calls(f):
            if name in session_names:
                sites.add((rel, name))
            elif name == "make" and re.search(r"from \.?\.?(providers|\.providers) import [^\n]*\bmake\b|"
                                               r"from \.providers import make|from \. import make", text) \
                    and "schedule.py" not in rel:
                sites.add((rel, "make"))
            elif name in adapters:
                direct.add((rel, name))
        if re.search(r"subprocess\.(run|Popen|call|check_output)|runner=subprocess", text):
            procs.add(rel)
    assert sites == KNOWN_SITES, ("a provider or host-session construction site appeared or moved: check it passes "
                                  "the offline guard, then add it here", sites ^ KNOWN_SITES)
    assert direct <= DIRECT_OK, ("an adapter is constructed directly (bypassing providers.make and its offline "
                                 "check)", direct - DIRECT_OK)
    assert procs == set(PROCESS_SITES), ("a new subprocess user: it must not start a hosted process in offline mode",
                                         procs ^ set(PROCESS_SITES))
    # the guards themselves: the constructors and make check offline mode before anything else
    hs = (ROOT / "tenderpack/ai/hostsession.py").read_text(encoding="utf-8")
    for cls in ("class HostSession", "class PlainSession"):
        body = hs[hs.index(cls):]
        init = body[body.index("def __init__"):]
        first = init[:init.index("\n\n")] if "\n\n" in init else init
        assert "check_host_session(" in first, cls
    pv = (ROOT / "tenderpack/ai/providers/__init__.py").read_text(encoding="utf-8")
    mk = pv[pv.index("def make("):]
    assert mk.index("check_route(") < mk.index("route(cfg, route_name)")
    cr = (ROOT / "tenderpack/ai/critic.py").read_text(encoding="utf-8")
    assert cr.count("check_host_session(cfg, \"critic\")") >= 2


def test_offline_mode_refuses_every_hosted_construction_before_any_call(monkeypatch):
    from tenderpack.ai import config as C
    from tenderpack.ai import hostsession as HS
    from tenderpack.ai.offline import OfflineError
    from tenderpack.ai.providers import make
    cfg = C.load(ROOT / "config/ai.yaml")
    cfg["_offline"] = "--offline"
    started = []
    runner = lambda *a, **k: started.append(a)                          # noqa: E731
    for route in ("host", "anthropic", "openrouter"):
        with pytest.raises(OfflineError):
            make(route, "m", cfg)
    with pytest.raises(OfflineError):
        HS.PlainSession(cfg, "system", runner=runner, label="repair-analysis")
    with pytest.raises(OfflineError):
        HS.PlainSession(cfg, "system", runner=runner, label="critic")
    assert started == []
