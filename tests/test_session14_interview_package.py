"""Session 14 (W6, part 7, item 5): the interview package carries the final editable code and everything to run it,
and scripts/mac/verify_package.sh verifies the PACKAGED COPY itself.

  * the package holds the code, the locked dependencies, the sources, the baseline outputs, the runtime policies
    (tenderpack/ai/policy/), the launchers (and levels.py, verify_package.sh), the recovery instructions, the focused
    tests, the quick-review documentation (docs/QUICK_REVIEW.md) and the Mac checklist (docs/MAC_CHECKLIST.md);
  * EVERY tests/test_session14_*.py is in the focused set (by glob, so a new one cannot be left out); the quick
    command deselects the named slow tests (a deselect list, not a time limit) and every name on that list exists;
    INTERVIEW.json carries the quick command's arguments for the verifier;
  * verify_package.sh unzips the zip into a FRESH place and checks the manifest, the executable bits and the contents
    there; a tampered file or a lost executable bit is a FAIL; the quick tests are timed and a run past three minutes
    is a FAIL that names the slowest.
The real package is built once here (the builder reads git `rev-parse` only and writes under the test's folder)."""
from __future__ import annotations

import ast
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "scripts/mac/verify_package.sh"
NOW = datetime(2026, 10, 7, 9, 0, tzinfo=timezone.utc)


def _mif():
    spec = importlib.util.spec_from_file_location("s14_make_interview_folder", ROOT / "scripts/make_interview_folder.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["s14_make_interview_folder"] = mod
    spec.loader.exec_module(mod)
    return mod


def _verify(*args, env=None, timeout=300) -> subprocess.CompletedProcess:
    e = {k: v for k, v in os.environ.items() if not k.startswith("TENDERPACK_")}
    e.update(env or {})
    return subprocess.run(["bash", str(VERIFY), *map(str, args)], capture_output=True, text=True, env=e,
                          timeout=timeout)


def test_every_session14_test_is_focused_and_the_quick_command_deselects_only_real_slow_tests():
    mif = _mif()
    tests = mif.focused_tests(ROOT)
    s14 = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "tests").glob("test_session14_*.py"))
    assert s14 and set(s14) <= set(tests), set(s14) - set(tests)
    argv = mif.quick_argv(tests)
    assert argv[:2] == ["-m", "pytest"] and all(t in argv for t in tests)
    for s in mif.SLOW:                                       # every deselected id names a test that exists
        f, name = s.split("::", 1)
        assert (ROOT / f).is_file(), s
        fn = name.split("[", 1)[0]
        assert fn in {n.name for n in ast.walk(ast.parse((ROOT / f).read_text(encoding="utf-8")))
                      if isinstance(n, ast.FunctionDef)}, s
        if f in tests:
            assert ["--deselect", s] == argv[argv.index(s) - 1:argv.index(s) + 1]
    assert "--durations=10" in argv                           # the verifier names the slowest from it


def test_the_selection_carries_what_the_mac_needs():
    mif = _mif()
    files = set(mif.select(ROOT))
    for need in ("pyproject.toml", "uv.lock", "requirements.lock.txt", "scripts/mac/launch.command",
                 "scripts/mac/setup.sh", "scripts/mac/checks.sh", "scripts/mac/levels.py",
                 "scripts/mac/verify_package.sh", "scripts/make_interview_folder.py", "docs/QUICK_REVIEW.md",
                 "docs/MAC_CHECKLIST.md", "docs/AI_ROUTES.md", "docs/MAC_SETUP.md", "docs/VERIFY_ON_MAC.md",
                 "config/routes_status.yaml", "config/ai.yaml", "curation/approvals.yaml", "build/units.json",
                 "out/README.md"):
        assert need in files, need
    policy = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "tenderpack/ai/policy").iterdir() if p.is_file())
    assert policy and set(policy) <= files, set(policy) - files
    assert any(f.startswith("sources/") and f.endswith(".pdf") for f in files)
    assert all(t in files for t in mif.focused_tests(ROOT))


@pytest.fixture(scope="module")
def package(tmp_path_factory):
    mif = _mif()
    dest = tmp_path_factory.mktemp("s14-package")
    res = mif.build(dest, label="session 14 test build", repo=ROOT, now=NOW)
    return {"mod": mif, "folder": Path(res["folder"]), "zip": Path(res["zip"]), "dest": dest}


def test_the_package_records_its_focused_tests_and_quick_command(package):
    info = json.loads((package["folder"] / "INTERVIEW.json").read_text(encoding="utf-8"))
    mif = package["mod"]
    assert info["focused_tests"] == mif.focused_tests(ROOT)
    assert info["quick_tests_argv"] == mif.quick_argv(info["focused_tests"])
    readme = (package["folder"] / "README.md").read_text(encoding="utf-8")
    assert "docs/MAC_CHECKLIST.md" in readme and "scripts/mac/verify_package.sh" in readme


@pytest.mark.skipif(not shutil.which("unzip"), reason="needs unzip")
def test_verify_package_checks_the_packaged_copy_in_a_fresh_place(package, tmp_path):
    into = tmp_path / "fresh"
    r = _verify(package["zip"], "--into", into, "--only", "manifest,bits,contents")
    assert r.returncode == 0, r.stdout + r.stderr
    for step in ("unzip: one folder", "manifest: ", "bits: all ", "contents: the code, "):
        assert any(ln.startswith("PASS     " + step) for ln in r.stdout.splitlines()), (step, r.stdout)
    assert "0 FAIL" in r.stdout and str(into) in r.stdout
    assert (into / package["folder"].name / "scripts/mac/launch.command").stat().st_mode & 0o111
    # the same folder again is refused: the copy is always verified in a fresh place
    again = _verify(package["zip"], "--into", into, "--only", "manifest")
    assert again.returncode != 0 and "not empty" in again.stdout


@pytest.mark.skipif(not shutil.which("unzip"), reason="needs unzip")
def test_verify_package_fails_a_tampered_file_and_a_lost_executable_bit(package, tmp_path):
    bad = tmp_path / "bad.zip"
    name = package["folder"].name
    with zipfile.ZipFile(package["zip"]) as src, zipfile.ZipFile(bad, "w", zipfile.ZIP_DEFLATED) as dst:
        for i in src.infolist():
            data = src.read(i)
            if i.filename == f"{name}/docs/MAC_CHECKLIST.md":
                data += b"\nedited after the manifest\n"
            if i.filename == f"{name}/scripts/mac/checks.sh":
                i.external_attr = (0o100644 << 16)
            dst.writestr(i, data)
    r = _verify(bad, "--into", tmp_path / "v", "--only", "manifest,bits")
    assert r.returncode != 0, r.stdout
    assert any(ln.startswith("FAIL     manifest:") for ln in r.stdout.splitlines()), r.stdout
    assert "docs/MAC_CHECKLIST.md" in r.stdout
    assert any(ln.startswith("FAIL     bits:") and "scripts/mac/checks.sh" in ln for ln in r.stdout.splitlines())


def _mini(tmp: Path, argv: list[str]) -> Path:
    f = tmp / "PKG"
    (f / "smoke-test").mkdir(parents=True)
    (f / "INTERVIEW.json").write_text(json.dumps({"quick_tests_argv": argv}, indent=1), encoding="utf-8")
    (f / "smoke-test/run_smoke.sh").write_text("#!/usr/bin/env bash\necho 'smoke test: PASS (stand-in)'\n",
                                               encoding="utf-8")
    z = tmp / "pkg.zip"
    with zipfile.ZipFile(z, "w") as zf:
        for p in sorted(f.rglob("*")):
            if p.is_file():
                info = zipfile.ZipInfo(f"PKG/{p.relative_to(f).as_posix()}")
                info.external_attr = (0o100755 if p.suffix == ".sh" else 0o100644) << 16
                zf.writestr(info, p.read_bytes())
    return z


@pytest.mark.skipif(not shutil.which("unzip"), reason="needs unzip")
def test_verify_package_runs_the_quick_tests_times_them_and_runs_the_smoke_test(tmp_path):
    z = _mini(tmp_path, ["-c", "print('3 passed in 0.10s')"])
    r = _verify(z, "--into", tmp_path / "a", "--only", "tests,smoke", env={"TENDERPACK_PY": sys.executable})
    assert r.returncode == 0, r.stdout
    assert "PASS     tests: the focused quick tests: 3 passed in 0.10s in " in r.stdout
    assert "PASS     smoke: smoke test: PASS (stand-in)" in r.stdout
    slow = _mini(tmp_path / "s", ["-c", "import time; time.sleep(1.2); print('2 passed in 1.20s')"])
    r = _verify(slow, "--into", tmp_path / "b", "--only", "tests",
                env={"TENDERPACK_PY": sys.executable, "TENDERPACK_VERIFY_QUICK_LIMIT_S": "0"})
    assert r.returncode != 0 and "over 0s (three minutes)" in r.stdout and "SLOW in scripts/make_interview_folder.py" \
        in r.stdout, r.stdout
    failing = _mini(tmp_path / "f", ["-c", "import sys; print('1 failed'); sys.exit(1)"])
    r = _verify(failing, "--into", tmp_path / "c", "--only", "tests", env={"TENDERPACK_PY": sys.executable})
    assert r.returncode != 0 and "FAIL     tests: the focused quick tests ended with exit 1" in r.stdout, r.stdout
