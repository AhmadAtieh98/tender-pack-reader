"""Session 12, part 6: the labelled working-tree snapshot beside the clean-commit archive.

- scripts/make_snapshot.py packages the tree as it is (tracked + untracked, not ignored), discloses every uncommitted
  path, carries the diff and a manifest, and is named after the base revision (never presented as a release).
- scripts/make_draft_archive.py keeps its safeguard: it refuses a dirty tree.
- The archive's rehearsal list is no longer hardcoded to blind-01..03: every rehearsal with a COMPARISON.md is taken.
"""
from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout


@pytest.fixture
def fixture_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "t")
    (repo / "pyproject.toml").write_text('[project]\nname = "x"\ndependencies = [\n    "pyyaml>=6.0",\n]\n', encoding="utf-8")
    (repo / "kept.txt").write_text("kept\n", encoding="utf-8")
    (repo / "changed.txt").write_text("before\n", encoding="utf-8")
    (repo / "gone.txt").write_text("gone\n", encoding="utf-8")
    (repo / ".gitignore").write_text("ignored/\n", encoding="utf-8")
    (repo / "rehearsals" / "blind-01").mkdir(parents=True)
    (repo / "rehearsals" / "blind-01" / "COMPARISON.md").write_text("one\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")
    # the uncommitted state: a tracked change, a deletion, an untracked file, an ignored file, two more rehearsals
    (repo / "changed.txt").write_text("after\n", encoding="utf-8")
    (repo / "gone.txt").unlink()
    (repo / "new.txt").write_text("new\n", encoding="utf-8")
    (repo / "ignored").mkdir()
    (repo / "ignored" / "cache.bin").write_bytes(b"\x00")
    (repo / "rehearsals" / "blind-05").mkdir()
    (repo / "rehearsals" / "blind-05" / "COMPARISON.md").write_text("five\n", encoding="utf-8")
    (repo / "rehearsals" / "blind-06").mkdir()            # no comparison yet: not included
    return repo


def test_snapshot_packages_the_working_tree_with_disclosure(fixture_repo: Path, tmp_path: Path, capsys):
    snap = _load("make_snapshot")
    when = datetime(2026, 10, 5, 12, 34, tzinfo=timezone.utc)
    assert snap.main(tmp_path / "dest", label="session 12 review", repo=fixture_repo, now=when) == 0
    base = _git(fixture_repo, "rev-parse", "--short", "HEAD").strip()
    name = f"LAMAR-PPP-R2-SNAPSHOT_{base}+wt_20261005T1234Z"
    stage = tmp_path / "dest" / name
    assert stage.is_dir() and (tmp_path / "dest" / f"{name}.zip").exists()
    # the tree: tracked that still exists, the changed content, the untracked file; not the deleted or ignored ones
    assert (stage / "kept.txt").exists() and (stage / "new.txt").exists()
    assert (stage / "changed.txt").read_text(encoding="utf-8") == "after\n"
    assert not (stage / "gone.txt").exists() and not (stage / "ignored").exists()
    md = (stage / "SNAPSHOT.md").read_text(encoding="utf-8")
    assert "WORKING-TREE SNAPSHOT" in md and "not a release archive" in md
    assert f"Base revision: `{base}`" in md and "Label: session 12 review" in md
    assert " M changed.txt" in md and " D gone.txt" in md and "?? new.txt" in md      # the disclosure
    assert "changed.txt" in md.split("## Diff statistics")[1]
    assert '"pyyaml>=6.0"' in md
    patch = (stage / "uncommitted.patch").read_text(encoding="utf-8")
    assert "-before" in patch and "+after" in patch
    # the manifest covers every file and its hashes are right
    manifest = (stage / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
    listed = {l.split("  ", 1)[1] for l in manifest}
    assert listed >= {"kept.txt", "new.txt", "changed.txt", "SNAPSHOT.md", "uncommitted.patch"}
    for line in manifest:
        digest, rel = line.split("  ", 1)
        assert hashlib.sha256((stage / rel).read_bytes()).hexdigest() == digest
    with zipfile.ZipFile(tmp_path / "dest" / f"{name}.zip") as z:
        names = z.namelist()
        assert f"{name}/SNAPSHOT.md" in names and f"{name}/new.txt" in names
        assert all(i.date_time == (2026, 10, 5, 12, 34, 0) for i in z.infolist())
    assert "paths differ from the base" in capsys.readouterr().out


def test_snapshot_of_a_clean_tree_says_so(fixture_repo: Path, tmp_path: Path):
    snap = _load("make_snapshot")
    _git(fixture_repo, "add", "-A")
    _git(fixture_repo, "commit", "-q", "-m", "everything")
    assert snap.main(tmp_path / "dest", repo=fixture_repo, now=datetime(2026, 10, 5, 1, 2, tzinfo=timezone.utc)) == 0
    md = next((tmp_path / "dest").glob("*/SNAPSHOT.md")).read_text(encoding="utf-8")
    assert "(clean: the snapshot equals the base revision)" in md
    assert "Paths that differ from the base revision: 0" in md


def test_archive_keeps_refusing_a_dirty_tree_and_takes_every_rehearsal(fixture_repo: Path, tmp_path: Path,
                                                                        monkeypatch, capsys):
    arc = _load("make_draft_archive")
    monkeypatch.setattr(arc, "REPO", fixture_repo)
    assert arc.main(tmp_path / "dest", None) == 2            # the release safeguard: a dirty tree is refused
    assert "refused: the working tree has uncommitted changes" in capsys.readouterr().out
    assert not (tmp_path / "dest").exists()
    assert [p.name for p in arc.rehearsals_to_include(fixture_repo)] == ["blind-01", "blind-05"]
    src = (ROOT / "scripts" / "make_draft_archive.py").read_text(encoding="utf-8")
    assert '("blind-01", "blind-02", "blind-03")' not in src   # the hardcoded list is gone
    assert 'glob("session-*_report.md")' in src                 # and so is the hardcoded session-report list
