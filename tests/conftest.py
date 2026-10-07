from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests" / "fixtures"))

from tenderpack.cli import ingest  # noqa: E402

import ai_fixture  # noqa: E402

# One module under both import names (`from ai_fixture import ...` and `from tests.fixtures.ai_fixture import ...`), so
# the session's rehearsal builds registered on it below are seen by every caller.
sys.modules.setdefault("tests.fixtures.ai_fixture", ai_fixture)


@pytest.fixture(scope="session")
def golden() -> dict:
    return yaml.safe_load((ROOT / "tests/golden/pack_expectations.yaml").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def pack(tmp_path_factory):
    """Full Stage 1 ingest of the real pack into a temporary build directory."""
    out = tmp_path_factory.mktemp("build")
    res = ingest(ROOT / "config/pack.yaml", out, ROOT, quiet=True)
    res["out"] = out
    res["by_id"] = {u["unit_id"]: u for u in res["units"]}
    return res


@pytest.fixture(scope="session")
def synthetic(tmp_path_factory):
    """The synthetic fixture: built from code, with its own record of what it placed."""
    import make_fixture

    src = tmp_path_factory.mktemp("fixture-src")
    expected = make_fixture.build(src)
    out = tmp_path_factory.mktemp("fixture-build")
    res = ingest(src / "pack.yaml", out, ROOT, quiet=True)
    res["expected"] = expected
    res["src"] = src
    res["out"] = out
    res["by_id"] = {u["unit_id"]: u for u in res["units"]}
    return res


@pytest.fixture(scope="session")
def pending(tmp_path_factory):
    """The real pack built with NO approvals (a disposable, empty approvals file): both image readings pending, as
    they were until the owner confirmed them on 3 Oct 2026 (session 08). Tests of how a PENDING reading flows through
    the outputs use this build; the real build carries the owner's confirmations."""
    d = tmp_path_factory.mktemp("pending")
    cfg = yaml.safe_load((ROOT / "config/pack.yaml").read_text(encoding="utf-8"))
    cfg["approvals"] = str(d / "approvals.yaml")
    (d / "pack.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
    res = ingest(d / "pack.yaml", d / "evidence", ROOT, quiet=True)
    assert res["exit_code"] == 0
    return {"evidence": d / "evidence", "pack": d / "pack.yaml", "dir": d}


# ------------------------------------------------------------------------------------------ rehearsal evidence builds
# The rehearsal packs (rehearsals/<name>/work/pack.yaml and the files it names) are committed; their evidence builds
# (rehearsals/<name>/build) are not (.gitignore): they exist only where a rehearsal was run, and may be stale. Tests
# never read those folders and never write under rehearsals/. Each rehearsal pack a session asks for is ingested
# afresh, once per test session, into a disposable folder under pytest's tmp_path_factory (about 13 s each), and
# stage2.run on that build is computed once per session too. The run is shared: treat it as read-only (deep-copy
# before changing anything), as the module-scoped runs it replaces were.

class RehearsalBuilds:
    """Session-cached, lazily made evidence builds and stage2 runs of the rehearsal packs."""

    def __init__(self, tmp_path_factory):
        self._factory = tmp_path_factory
        self._builds: dict[str, Path] = {}
        self._runs: dict[str, dict] = {}
        self.seconds: dict[str, float] = {}

    @staticmethod
    def pack(name: str) -> Path:
        p = ROOT / "rehearsals" / name / "work" / "pack.yaml"
        if not p.is_file():
            raise FileNotFoundError(f"no rehearsal pack {p.relative_to(ROOT)}")
        return p

    def build(self, name: str) -> Path:
        """The evidence build of rehearsals/<name>/work/pack.yaml, ingested into a disposable folder once per session."""
        if name not in self._builds:
            out = self._factory.mktemp(f"rehearsal-{name}") / "build"
            assert ROOT / "rehearsals" not in out.parents, f"{out}: a test build must not be written under rehearsals/"
            t0 = time.perf_counter()
            res = ingest(self.pack(name), out, ROOT, quiet=True)
            self.seconds[f"{name} ingest"] = time.perf_counter() - t0
            assert res["exit_code"] == 0, f"ingest of {self.pack(name).relative_to(ROOT)} failed: {res['status']}"
            self._builds[name] = out
        return self._builds[name]

    def built(self, name: str) -> Path | None:
        """build(name) if this session has already made it, else None (never builds)."""
        return self._builds.get(name)

    def run(self, name: str) -> dict:
        """stage2.run on build(name) with the rehearsal's pack, computed once per session (read-only; see above)."""
        if name not in self._runs:
            from tenderpack import stage2
            evidence = self.build(name)
            t0 = time.perf_counter()
            self._runs[name] = stage2.run(evidence, self.pack(name), ROOT)
            self.seconds[f"{name} stage2.run"] = time.perf_counter() - t0
        return self._runs[name]


_SESSION_BUILDS: list[RehearsalBuilds] = []


@pytest.fixture(scope="session")
def rehearsal_builds(tmp_path_factory) -> RehearsalBuilds:
    builds = RehearsalBuilds(tmp_path_factory)
    _SESSION_BUILDS.append(builds)
    return builds


@pytest.fixture(scope="session")
def rehearsal_build(rehearsal_builds):
    """`rehearsal_build("blind-02")` -> Path of that rehearsal's disposable evidence build (ingested once per session)."""
    return rehearsal_builds.build


@pytest.fixture(scope="session")
def rehearsal_run(rehearsal_builds):
    """`rehearsal_run("blind-02")` -> stage2.run(rehearsal_build("blind-02"), its work/pack.yaml, ROOT), once per session."""
    return rehearsal_builds.run


def _rehearsal_fixture(name: str, what: str):
    fixture_name = f"{name.replace('-', '')}_{what}"            # blind-02 -> blind02_build, blind02_run

    @pytest.fixture(scope="session", name=fixture_name)
    def f(rehearsal_builds):
        return getattr(rehearsal_builds, what)(name)
    f.__doc__ = f"rehearsal_{what}({name!r}): {'the evidence build (Path)' if what == 'build' else 'the stage2 run (dict)'}."
    return f


blind01_build, blind01_run = _rehearsal_fixture("blind-01", "build"), _rehearsal_fixture("blind-01", "run")
blind02_build, blind02_run = _rehearsal_fixture("blind-02", "build"), _rehearsal_fixture("blind-02", "run")
blind03_build, blind03_run = _rehearsal_fixture("blind-03", "build"), _rehearsal_fixture("blind-03", "run")


@pytest.fixture(scope="session", autouse=True)
def _rehearsal_builds_for_helpers(rehearsal_builds):
    """tests/fixtures/ai_fixture.py is a plain helper module (no fixtures): it reaches the session's blind-02 build
    through this registration. Costs nothing until a build is asked for."""
    ai_fixture.BUILDS = rehearsal_builds
    yield
    ai_fixture.BUILDS = None


# session 14 (F4; R4-6): TENDERPACK_OFFLINE as the test session found it (a run under it stays under it)
_OFFLINE_ENV0 = os.environ.get("TENDERPACK_OFFLINE")


def _offline_as_found() -> None:
    from tenderpack.ai import offline as OFF
    OFF._PROCESS = None
    if _OFFLINE_ENV0 is None:
        os.environ.pop(OFF.ENV, None)
    else:
        os.environ[OFF.ENV] = _OFFLINE_ENV0


@pytest.fixture(autouse=True)
def _offline_switch_is_per_test():
    """Session 14 (F4; R4-6): offline mode switches the whole PROCESS (offline.switch_process: a latch and
    TENDERPACK_OFFLINE=1 for its children) and a process never switches back. In the one pytest process, an offline
    command run in-process by a test or by a module fixture must not leave later tests offline: each test starts and
    ends with the switch as the test session found it."""
    _offline_as_found()
    yield
    _offline_as_found()


def pytest_terminal_summary(terminalreporter):
    spent = {k: v for b in _SESSION_BUILDS for k, v in b.seconds.items()}
    if spent:
        terminalreporter.write_line("rehearsal fixtures (disposable, this session): " + ", ".join(
            f"{k} {v:.1f} s" for k, v in spent.items()) + f"; total {sum(spent.values()):.1f} s")
