"""Session 14: the interview package's smoke check (scripts/smoke_test/check_smoke.py) judges a session by its RECORDS
under <run>/ai/, not by the folder's existence: the run-scoped lock of a run allowed two sessions at once (session 12,
max_parallel_sessions > 1) creates <run>/ai/ and removes the lock when the run stops, leaving the folder empty. The
regression build of the package (max_parallel_sessions pinned to 2 for the timed run) failed its smoke test on that
empty folder although no session ran."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _load():
    spec = importlib.util.spec_from_file_location("check_smoke", ROOT / "scripts/smoke_test/check_smoke.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run_folder(tmp_path: Path) -> tuple[Path, Path, Path]:
    rd = tmp_path / "run"
    rd.mkdir()
    cp = {"status": "stopped", "steps": {"ingest": {"status": "done"}, "analysis": {"status": "pending"}},
          "provisions": {"ADD-03:1.1": {"status": "pending"}, "ADD-03:2.1": {"status": "pending"}},
          "approval": {"status": "none", "decisions": []}, "candidate": {"dir": str(rd / "candidate")}}
    (rd / "checkpoint.json").write_text(json.dumps(cp), encoding="utf-8")
    (rd / "log.jsonl").write_text(json.dumps({"event": "say", "message": "ingest"}) + "\n", encoding="utf-8")
    exp = tmp_path / "expected.yaml"
    exp.write_text(yaml.safe_dump({"doc_id": "ADD-03", "provisions": ["ADD-03:1.1", "ADD-03:2.1"]}), encoding="utf-8")
    log = tmp_path / "run.log"
    log.write_text("ok\n", encoding="utf-8")
    return rd, exp, log


def test_an_empty_ai_folder_left_by_the_run_lock_is_not_a_session(tmp_path, capsys):
    mod = _load()
    rd, exp, log = _run_folder(tmp_path)
    (rd / "ai").mkdir()                                   # what the run-scoped lock leaves behind
    assert mod.main(str(rd), str(exp), "0", str(log)) == 0
    out = capsys.readouterr().out
    assert "smoke test: PASS (9 of 9 checks" in out and "session records under ai/: none" in out


def test_a_session_record_under_ai_fails_the_smoke_check(tmp_path, capsys):
    mod = _load()
    rd, exp, log = _run_folder(tmp_path)
    (rd / "ai" / "ADD-03-analysis-001").mkdir(parents=True)
    (rd / "ai" / "ADD-03-analysis-001" / "session.json").write_text("{}", encoding="utf-8")
    assert mod.main(str(rd), str(exp), "0", str(log)) == 1
    out = capsys.readouterr().out
    assert "FAIL  no model, host-session or network event" in out and "ADD-03-analysis-001/session.json" in out
