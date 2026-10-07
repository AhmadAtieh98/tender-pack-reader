"""Session 13 (part 2, item 3): the code and policy identity of a run, recorded at start and checked at every resume.

The blind-05 regression (rehearsals/blind-05/REGRESSION-S12.md, defect 10; synthetic): "The code changed between the
run's segments. A resumed run picks up whatever tree is current, and nothing in the checkpoint records the code version
per segment." Now the checkpoint records, at start, the git HEAD when available (and whether the tree is dirty), a
content hash over tenderpack/**/*.py, config/*.yaml and pyproject.toml (the prompts and policy texts live in those
files), computed from the files, and the time; every resume recomputes it and refuses a mismatch (exit 7) unless
--allow-code-change "<reason>" is given, which records the new identity, the reason and the time, and run-status, the
run log and the review packet header then say "segments ran on different code"."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tenderpack.ai import checkpoint as CPM
from tenderpack.ai import workflow as W


def _tree(root: Path) -> Path:
    (root / "tenderpack" / "ai").mkdir(parents=True)
    (root / "config").mkdir()
    (root / "tenderpack" / "__init__.py").write_text("")
    (root / "tenderpack" / "ai" / "controller.py").write_text('SYSTEM = "rule 9: no_effect safeguard"\n')
    (root / "config" / "ai.yaml").write_text("routes: {}\n")
    (root / "pyproject.toml").write_text("[project]\nname='x'\n")
    (root / "README.md").write_text("not code\n")
    return root


def test_the_identity_is_a_content_hash_of_the_code_config_and_policy_files(tmp_path):
    root = _tree(tmp_path / "t")
    a = CPM.code_identity(root)
    assert a["content_sha256"] and a["files"] == 4 and a["recorded"], a
    (root / "README.md").write_text("changed, not code\n")
    (root / "tenderpack" / "__pycache__").mkdir()
    (root / "tenderpack" / "__pycache__" / "x.pyc").write_bytes(b"\0")
    assert CPM.code_identity(root)["content_sha256"] == a["content_sha256"]
    (root / "tenderpack" / "ai" / "controller.py").write_text('SYSTEM = "rule 9 replaced"\n')
    assert CPM.code_identity(root)["content_sha256"] != a["content_sha256"]


def _run(tmp_path, monkeypatch):
    root = _tree(tmp_path / "code")
    monkeypatch.setattr(W, "CODE_ROOT", root)
    staging = tmp_path / "staging"
    cp = CPM.Checkpoint.new(staging / "runs" / "ADD-03-run-t" / "checkpoint.json", run_id="ADD-03-run-t",
                            addendum="ADD-03", settings={"route": "recorded", "ai_config": None, "offline": None,
                                                         "base_run": None, "worklog": str(tmp_path / "wl")},
                            inputs={}, candidate={})
    W.record_code_identity(cp)
    return root, staging, cp


def test_start_records_it_and_a_resume_on_changed_code_is_refused(tmp_path, monkeypatch):
    root, staging, cp = _run(tmp_path, monkeypatch)
    assert CPM.Checkpoint.load(cp.path).data["code_identity"]["start"]["content_sha256"]
    (root / "tenderpack" / "ai" / "controller.py").write_text('SYSTEM = "changed between segments"\n')
    with pytest.raises(W.CodeChanged) as e:
        W.resume("ADD-03-run-t", staging)
    assert e.value.exit_code == W.CODE_CHANGED_EXIT and "--allow-code-change" in str(e.value)
    events = [x["event"] for x in CPM.Checkpoint.load(cp.path).data["events"]]
    assert "resumed" not in events                                       # refused before anything ran


def test_the_cli_refuses_with_a_distinct_exit_code(tmp_path, monkeypatch, capsys):
    from tenderpack.cli import main
    root, staging, cp = _run(tmp_path, monkeypatch)
    (root / "config" / "ai.yaml").write_text("routes: {changed: true}\n")
    assert main(["ai", "resume", "ADD-03-run-t", "--out", str(staging)]) == W.CODE_CHANGED_EXIT == 7
    assert "code changed" in capsys.readouterr().out.lower()


def test_allow_code_change_records_the_new_identity_and_every_view_says_so(tmp_path, monkeypatch):
    root, staging, cp = _run(tmp_path, monkeypatch)
    (root / "tenderpack" / "ai" / "controller.py").write_text('SYSTEM = "fixed between segments"\n')
    cp = CPM.Checkpoint.load(cp.path)
    W.check_code_identity(cp, "the HOST_RULES fix (test)")
    data = CPM.Checkpoint.load(cp.path).data
    ev = [x for x in data["events"] if x["event"] == "code_changed"]
    assert ev and ev[0]["reason"] == "the HOST_RULES fix (test)" and ev[0]["ts"] and \
        ev[0]["now"]["content_sha256"] != ev[0]["before"]["content_sha256"]
    assert len(data["code_identity"]["segments"]) == 2 and data["code_identity"]["differ"]
    assert "segments ran on different code" in json.dumps(W.summary(cp))
    assert any("segments ran on different code" in x for x in W.code_lines(cp))
    W.check_code_identity(cp, None)                                      # the same code again: no refusal now


def test_a_resume_on_the_same_code_records_the_segment_without_refusing(tmp_path, monkeypatch):
    root, staging, cp = _run(tmp_path, monkeypatch)
    W.check_code_identity(cp, None)
    data = CPM.Checkpoint.load(cp.path).data
    assert not data["code_identity"].get("differ") and "segments ran on different code" not in json.dumps(W.summary(cp))
