from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests" / "fixtures"))

from tenderpack.cli import ingest  # noqa: E402


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
