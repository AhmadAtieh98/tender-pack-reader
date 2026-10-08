"""Session 13 (part 5): the minimal interview folder for the owner's Mac, the zips' executable bits and the locked set.

  * scripts/make_interview_folder.py DEST [--label TEXT] builds LAMAR-PPP-R2-INTERVIEW_<base>+wt_<UTC stamp>/ and its
    zip: the editable code, a focused test subset, the sources, configuration, curation (approvals included), the
    baseline evidence and outputs, the runtime instructions, the exact dependencies, the launcher and scripts, ONE
    labelled smoke test, RECOVERY.md, empty folders for new runs and logs, a manifest and a README. It excludes the
    historical runs, the rehearsals (outputs and keys), the drill/fixture builds, any .venv, worktrees, .git and caches.
  * Every zip writer (the interview folder, the draft archive, the snapshot) keeps the executable bit of *.command and
    *.sh (a zip with 0644 everywhere gives the owner a launcher Finder cannot run).
  * requirements.lock.txt is exported from uv.lock (the pip path of setup.sh installs exactly that set).

Nothing here touches the network, the main tree or git (the builder reads `git rev-parse` only)."""
from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import shutil
import stat
import subprocess
import sys
import tomllib
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 10, 6, 7, 30, tzinfo=timezone.utc)


def _load(name: str):
    spec = importlib.util.spec_from_file_location(f"s13_{name}", ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[f"s13_{name}"] = mod
    spec.loader.exec_module(mod)
    return mod


def _tree_with_scripts(base: Path) -> Path:
    f = base / "pkg"
    (f / "scripts/mac").mkdir(parents=True)
    for n in ("launch.command", "setup.sh", "checks.sh"):
        (f / "scripts/mac" / n).write_text("#!/usr/bin/env bash\necho hi\n", encoding="utf-8")
        (f / "scripts/mac" / n).chmod(0o755)
    (f / "README.md").write_text("readme\n", encoding="utf-8")
    return f


def _modes_in_zip(z: Path) -> dict[str, int]:
    with zipfile.ZipFile(z) as zf:
        return {i.filename: (i.external_attr >> 16) & 0o777 for i in zf.infolist()}


def _modes_after_unzip(z: Path, into: Path) -> dict[str, int]:
    into.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["unzip", "-q", "-o", str(z), "-d", str(into)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return {p.relative_to(into).as_posix(): stat.S_IMODE(p.stat().st_mode) for p in into.rglob("*") if p.is_file()}


@pytest.mark.parametrize("script", ["make_draft_archive", "make_snapshot"])
def test_the_existing_zip_writers_keep_the_executable_bit(tmp_path, script):
    if not (ROOT / "scripts" / f"{script}.py").is_file():
        pytest.skip(f"scripts/{script}.py is not part of this copy (the interview folder carries only its own builder)")
    mod = _load(script)
    folder = _tree_with_scripts(tmp_path)
    z = tmp_path / "x.zip"
    mod.write_zip(folder, z, (2026, 10, 6, 0, 0, 0))
    modes = _modes_in_zip(z)
    assert modes["pkg/scripts/mac/launch.command"] == 0o755, modes
    assert modes["pkg/scripts/mac/setup.sh"] == 0o755 and modes["pkg/scripts/mac/checks.sh"] == 0o755, modes
    assert modes["pkg/README.md"] == 0o644, modes
    if shutil.which("unzip"):
        got = _modes_after_unzip(z, tmp_path / "u")
        assert got["pkg/scripts/mac/launch.command"] & 0o111 and got["pkg/scripts/mac/setup.sh"] & 0o111, got
        assert not got["pkg/README.md"] & 0o111, got


# ---------------------------------------------------------------------------------------------- the interview folder

@pytest.fixture(scope="module")
def built(tmp_path_factory):
    mif = _load("make_interview_folder")
    dest = tmp_path_factory.mktemp("interview")
    res = mif.build(dest, label="test build", repo=ROOT, now=NOW)
    return {"mod": mif, "folder": Path(res["folder"]), "zip": Path(res["zip"]), "res": res}


def _files(folder: Path) -> list[str]:
    return sorted(p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file())


def test_the_folder_is_named_after_the_base_revision_and_a_utc_stamp(built):
    name = built["folder"].name
    assert re.fullmatch(r"LAMAR-PPP-R2-INTERVIEW_[0-9a-f]{7,12}\+wt_20261006T0730Z", name), name
    assert built["zip"].name == name + ".zip"


def test_it_holds_what_the_owner_listed(built):
    f = built["folder"]
    files = set(_files(f))
    must = ["tenderpack/cli.py", "tenderpack/ai/offline.py", "tenderpack/panel/server.py",
            "config/ai.yaml", "config/pack.yaml", "curation/approvals.yaml", "pyproject.toml", "uv.lock",
            "requirements.lock.txt", "scripts/mac/setup.sh", "scripts/mac/checks.sh", "scripts/mac/launch.command",
            "scripts/make_interview_folder.py", "docs/OPERATING_GUIDE.md", "docs/AI_ROUTES.md", "docs/PANEL.md",
            "docs/MAC_SETUP.md", "docs/VERIFY_ON_MAC.md", "out/README.md", "out/checks.json", "build/units.json",
            "tests/conftest.py", "tests/test_session12_panel.py", "tests/test_session12_mac_checks.py",
            "tests/test_session12_computed_dates.py", "tests/test_session12_human_owned.py",
            "tests/test_session12_closed_window.py", "tests/test_session12_concurrency.py",
            "tests/test_session13_interview_folder.py", "tests/fixtures/ai_fixture.py", "tests/fixtures/make_drill.py",
            "RECOVERY.md", "README.md", "MANIFEST.sha256", "staging/ai/runs/.keep", "worklog/model_calls/.keep",
            "logs/.keep", "smoke-test/LABEL.txt", "smoke-test/ADD-03_Addendum_No_3.pdf", "smoke-test/EXPECTED.md",
            "smoke-test/expected.yaml", "smoke-test/run_smoke.sh"]
    missing = [m for m in must if m not in files]
    assert not missing, missing
    assert any(p.startswith("sources/") and p.endswith(".pdf") for p in files)
    if (ROOT / "docs/RUNTIME_INSTRUCTIONS.md").is_file():
        assert "docs/RUNTIME_INSTRUCTIONS.md" in files
    assert (f / "smoke-test/LABEL.txt").read_text(encoding="utf-8") == "SMOKE TEST: synthetic, not tender content\n"
    assert (f / "smoke-test/ADD-03_Addendum_No_3.pdf").read_bytes().startswith(b"%PDF-")


def test_it_excludes_the_history_the_rehearsals_and_any_environment(built):
    files = _files(built["folder"])
    # session 14: plus the run records a few focused tests read (TEST_RECORDS; still no key, comparison or output)
    allowed_material = tuple(built["mod"].TEST_MATERIAL) + tuple(getattr(built["mod"], "TEST_RECORDS", ()))
    for p in files:
        assert not p.startswith((".git/", ".venv/", "wt-", "out-drill", "build/drill", "build/fixture")), p
        assert "/.venv/" not in p and "__pycache__" not in p and not p.endswith(".pyc"), p
        if p.startswith("staging/"):
            assert p == "staging/ai/runs/.keep" or p.startswith(allowed_material), p
        if p.startswith("rehearsals/"):
            assert p.startswith(allowed_material), p
            assert "/SEALED/" not in p and "COMPARISON" not in p and "/out-" not in p, p
        if p.startswith("worklog/"):
            assert p in ("worklog/model_calls/.keep", "worklog/README.md", "worklog/ERROR_INDEX.md"), p
        if p.startswith("docs/"):
            assert p.split("/", 1)[1] in built["mod"].DOCS + built["mod"].OPTIONAL_DOCS, p
    # the material the focused tests read is synthetic regression input, never an answer key or a run's outputs
    for m in built["mod"].TEST_MATERIAL:
        assert "SEALED" not in m and "out" not in Path(m).parts and "batches" not in m, m


def test_it_refuses_a_virtual_environment_anywhere_in_what_it_copies(tmp_path):
    mif = _load("make_interview_folder")
    fake = tmp_path / "repo"
    for d in ("tenderpack", "sources", "config", "curation", "build", "out", "scripts/mac", "tests/fixtures", "docs"):
        (fake / d).mkdir(parents=True)
    (fake / "tenderpack/__init__.py").write_text("", encoding="utf-8")
    (fake / "tenderpack/.venv/bin").mkdir(parents=True)
    (fake / "tenderpack/.venv/pyvenv.cfg").write_text("home = /usr/bin\n", encoding="utf-8")
    with pytest.raises(mif.Refused, match=r"\.venv"):
        mif.select(fake)


def test_the_readme_lists_the_focused_tests_and_the_command(built):
    f = built["folder"]
    readme = (f / "README.md").read_text(encoding="utf-8")
    tests = sorted(p.name for p in (f / "tests").glob("test_*.py"))
    run = built["mod"].focused_tests(ROOT)
    for t in run:
        assert Path(t).name in readme, t
    assert set(Path(t).name for t in run) <= set(tests)
    assert ".venv/bin/python -m pytest -q -p no:cacheprovider " + " ".join(run) in readme
    quick, full = built["mod"].commands(run)
    kept = [s for s in built["mod"].SLOW if s.split("::")[0] in run and s.split("::")[0] not in built["mod"].QUICK_SKIP_FILES]
    assert quick in readme and quick.count("--deselect") == len(kept) and full in readme
    for word in ("bash scripts/mac/setup.sh", "launch.command", "connected", "offline", "smoke-test/run_smoke.sh",
                 "PENDING", "RECOVERY.md", "SMOKE TEST: synthetic, not tender content", "excluded"):
        assert word in readme, word


def test_recovery_says_how_to_resume_and_what_never_to_delete(built):
    rec = (built["folder"] / "RECOVERY.md").read_text(encoding="utf-8")
    for word in ("ai run-status", "ai resume", "lock", "exit 5", "--from", "Resume", "logs/", "worklog/model_calls/",
                 "staging/ai/runs/", "checkpoint.json", "never delete", "curation/approvals.yaml"):
        assert word in rec, word


def test_the_manifest_covers_every_file_and_the_zip_equals_the_folder(built):
    f, z = built["folder"], built["zip"]
    lines = (f / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
    listed = {}
    for ln in lines:
        h, p = ln.split("  ", 1)
        listed[p] = h
    files = [p for p in _files(f) if p != "MANIFEST.sha256"]
    assert sorted(listed) == files
    for p in files:
        assert hashlib.sha256((f / p).read_bytes()).hexdigest() == listed[p], p
    with zipfile.ZipFile(z) as zf:
        names = {i.filename for i in zf.infolist() if not i.is_dir()}
        assert names == {f"{f.name}/{p}" for p in _files(f)}
        for p in ("README.md", "MANIFEST.sha256", "scripts/mac/launch.command"):
            assert zf.read(f"{f.name}/{p}") == (f / p).read_bytes()
    assert built["mod"].verify(f, z) == []


def test_the_zip_keeps_the_launcher_and_scripts_executable(built, tmp_path):
    z, name = built["zip"], built["folder"].name
    modes = _modes_in_zip(z)
    execs = [n for n in modes if n.endswith((".command", ".sh"))]
    assert f"{name}/scripts/mac/launch.command" in execs and f"{name}/smoke-test/run_smoke.sh" in execs
    assert all(modes[n] == 0o755 for n in execs), {n: oct(modes[n]) for n in execs}
    # anything else is 0644, except a file executable at its source (the tests' fake CLIs keep their bit)
    src_exec = {f"{name}/{p}" for p in _files(built["folder"]) if (ROOT / p).is_file() and (ROOT / p).stat().st_mode & 0o100}
    assert all(modes[n] == (0o755 if n in src_exec else 0o644) for n in modes if n not in execs), \
        {n: oct(modes[n]) for n in modes if n not in execs and modes[n] != 0o644}
    if shutil.which("unzip"):
        got = _modes_after_unzip(z, tmp_path / "u")
        assert got[f"{name}/scripts/mac/launch.command"] & 0o111
        assert got[f"{name}/scripts/mac/setup.sh"] & 0o111 and got[f"{name}/smoke-test/run_smoke.sh"] & 0o111
    # and on disk in the folder itself
    assert (built["folder"] / "scripts/mac/launch.command").stat().st_mode & 0o111


# ---------------------------------------------------------------------------------------------- the locked set

def _lock_versions() -> dict[str, list[str]]:
    data = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    out: dict[str, list[str]] = {}
    for p in data["package"]:
        if p.get("source", {}).get("editable") or p.get("source", {}).get("virtual"):
            continue
        out.setdefault(p["name"], []).append(p["version"])
    return out


def _req_versions() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for ln in (ROOT / "requirements.lock.txt").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([A-Za-z0-9._-]+)==([^\s;]+)", ln)
        if m:
            out.setdefault(m.group(1).lower(), []).append(m.group(2))
    return out


def test_requirements_lock_is_the_export_of_uv_lock():
    assert (ROOT / "requirements.lock.txt").is_file(), "requirements.lock.txt (exported from uv.lock) is missing"
    lock, req = _lock_versions(), _req_versions()
    py = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    direct = [re.split(r"[<>=!~\[ ]", d, maxsplit=1)[0].lower()
              for d in py["dependencies"] + py["optional-dependencies"]["dev"]]
    for name in direct:
        assert name in req, f"{name}: a direct dependency is not pinned in requirements.lock.txt"
        assert sorted(req[name]) == sorted(lock[name]), (name, req[name], lock[name])
    for name, versions in req.items():                                   # nothing beyond the lock, no other version
        assert name in lock and set(versions) <= set(lock[name]), (name, versions, lock.get(name))
    assert set(lock) - {"tenderpack"} == set(req), set(lock) ^ set(req)
    text = (ROOT / "requirements.lock.txt").read_text(encoding="utf-8")
    assert "-e ." not in text and "file://" not in text


def test_setup_installs_the_locked_set_and_never_resolves_from_pyproject():
    setup = (ROOT / "scripts/mac/setup.sh").read_text(encoding="utf-8")
    assert "uv sync --frozen" in setup and "requirements.lock.txt" in setup
    assert '-e ".[dev]"' not in setup and "deps_from_pyproject" not in setup
    assert not re.search(r"pip install[^\n]*-e ", setup)
    assert "lockcheck.py" in setup                                     # the installed versions are compared after
    assert "lockcheck.py" in (ROOT / "scripts/mac/checks.sh").read_text(encoding="utf-8")


def test_the_smoke_test_passes_from_inside_the_folder(built, tmp_path):
    """run_smoke.sh in the built folder (this session's interpreter stands in for the folder's .venv): the synthetic
    addendum to the end of ingest, compared with the drill's own record; no model call."""
    f = built["folder"]
    before = sorted(x.name for x in (f / "staging/ai/runs").iterdir())
    env = {k: v for k, v in os.environ.items() if not k.startswith("TENDERPACK_")}
    env.update(TENDERPACK_PY=sys.executable, TMPDIR=str(tmp_path), TENDERPACK_OFFLINE="1")
    r = subprocess.run(["bash", str(f / "smoke-test/run_smoke.sh")], cwd=f, capture_output=True, text=True, env=env,
                       timeout=600)
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.startswith("SMOKE TEST: synthetic, not tender content")
    assert "smoke test: PASS (9 of 9 checks" in r.stdout and "FAIL" not in r.stdout
    assert sorted(x.name for x in (f / "staging/ai/runs").iterdir()) == before       # nothing written in the folder
    assert not [x for x in before if x != ".keep" and (f / "staging/ai/runs" / x / "checkpoint.json").exists()]
