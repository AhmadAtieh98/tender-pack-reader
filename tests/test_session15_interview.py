from pathlib import Path
import copy
import json

import pytest
import yaml


def test_demo_mode_cannot_silently_be_enabled_on_an_ordinary_pack(tmp_path):
    from tenderpack import interview
    p = tmp_path / "pack.yaml"
    p.write_text("pack_id: ordinary\n")
    with pytest.raises(interview.InterviewError, match="demo"):
        interview.require_demo(p)


def test_assumption_candidates_keep_rejections_and_skip_invalid_or_stale_rows():
    from tenderpack import interview
    r = {"reviews": {("row", "R1"): {"status": "proposed"}, ("row", "R2"): {"status": "changed"},
                     ("op", "O1"): {"status": "rejected"}, ("issue", "I-1"): {"status": "proposed"}}}
    decisions = [{"kind": "row", "item": "R2", "decision": "reject", "fingerprint": "old"}]
    assert interview.assumption_candidates(r, decisions) == ["I-1", "R1"]


def test_demo_review_label_never_claims_an_observed_human_approval():
    from tenderpack import review
    d = {"kind": "row", "item": "R", "decision": "accept", "reviewer": "Interview demo assumption",
         "fingerprint": "same", "origin": "interview_demo", "date": "2026-10-08"}
    status = review.status_of([d], "row", "R", "same")
    assert status["status"] == "accepted"
    assert "ASSUMED" in review.label(status)


def test_edit_is_bound_to_the_viewed_content_and_confined_to_the_working_copy(tmp_path):
    from tenderpack import interview
    root = tmp_path / "operating"
    root.mkdir()
    p = root / "pack.yaml"
    p.write_text("interview_demo: true\n")
    outside = tmp_path / "outside.yaml"
    outside.write_text("preserve me")
    with pytest.raises(interview.InterviewError, match="outside"):
        interview.confined(root, outside)
    assert outside.read_text() == "preserve me"


def test_freeze_and_restore_preserves_run_history_and_checks_hashes(tmp_path):
    from tenderpack import interview
    root = tmp_path / "operating"
    for d in ("config", "curation", "sources", "build", "out", "staging/runs"):
        (root / d).mkdir(parents=True)
    (root / "config/pack.yaml").write_text("interview_demo: true\ndocuments:\n  - {doc_id: ADD-02}\n")
    (root / "out/result.txt").write_text("ADD02 baseline")
    interview.freeze(root)
    (root / "out/result.txt").write_text("edited")
    (root / "staging/runs/history.txt").write_text("keep this run")
    interview.restore(root)
    assert (root / "out/result.txt").read_text() == "ADD02 baseline"
    assert (root / "staging/runs/history.txt").read_text() == "keep this run"
    assert interview.verify_frozen(root) == []


def test_demo_page_lists_accepted_items_with_history_and_edit_controls():
    from tenderpack.panel import views
    data = {"stage": "ADD-02", "items": [{"id": "R1", "kind": "row", "fingerprint": "bound",
        "status": "accepted", "label": "ASSUMED APPROVED FOR DEMO", "value": {"id": "R1", "owner": "Legal"},
        "evidence": {"source": "evidence"}, "history": [{"note": "original decision"}]}]}
    html = views.interview_page("/t/token/", data, {})
    for text in ("R1", "ASSUMED", "original decision", "fingerprint", "interview/apply", "Edit"):
        assert text in html


def test_frozen_baseline_tampering_refuses_restore(tmp_path):
    from tenderpack import interview
    (tmp_path / "config").mkdir()
    (tmp_path / "config/pack.yaml").write_text("interview_demo: true\n")
    interview.freeze(tmp_path)
    (tmp_path / "baseline/ADD02/files/config/pack.yaml").write_text("changed")
    with pytest.raises(interview.InterviewError, match="hash"):
        interview.restore(tmp_path)


def test_workflow_demo_assumptions_are_explicit_and_native(monkeypatch, tmp_path):
    from tenderpack import interview, review
    pack = tmp_path / "pack.yaml"
    pack.write_text("interview_demo: true\n")
    r = {"reviews": {("row", "R1"): {"status": "proposed"}}}
    monkeypatch.setattr(interview.stage2, "run", lambda *args: r)
    def decide(state, items, action, reviewer, note, path):
        assert state is r and items == ["R1"]
        review.record(path, [{"kind": "row", "item": "R1", "decision": action, "reviewer": reviewer, "note": note}])
        return 0, []
    monkeypatch.setattr(review, "decide", decide)
    out = interview.assume_reviews(tmp_path, pack, tmp_path / "build")
    assert out["assumed"] == ["R1"]
    entries = review.load_decisions(tmp_path / "curation/reviews/decisions.yaml")
    assert entries[0]["origin"] == "interview_demo"


def test_restoring_is_refused_while_an_ai_run_is_active(tmp_path):
    import os, socket
    from tenderpack import interview
    (tmp_path / "config").mkdir()
    (tmp_path / "config/pack.yaml").write_text("interview_demo: true\n")
    interview.freeze(tmp_path)
    run = tmp_path / "staging/ai/runs/active"
    run.mkdir(parents=True)
    (run / "run.lock").write_text(json.dumps({"pid": os.getpid(), "host": socket.gethostname()}))
    with pytest.raises(interview.InterviewError, match="active"):
        interview.restore(tmp_path)


def test_package_selection_includes_new_runtime_tests():
    import importlib.util
    spec = importlib.util.spec_from_file_location("package", Path(__file__).resolve().parents[1] / "scripts/make_interview_folder.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert "tests/test_session15_interview.py" in module.focused_tests(Path(__file__).resolve().parents[1])


def test_demo_reading_approval_has_demo_provenance(monkeypatch, tmp_path):
    from tenderpack import interview, cli
    p = tmp_path / "pack.yaml"
    p.write_text("interview_demo: true\n")
    def approve(region_id, reviewer, notes, **kw):
        path = tmp_path / "curation/approvals.yaml"
        path.parent.mkdir(parents=True)
        path.write_text(yaml.safe_dump({"approvals": [{"region_id": region_id, "reviewer": reviewer, "notes": notes}]}))
        return 0
    monkeypatch.setattr(cli, "approve", approve)
    interview.assume_reading(tmp_path, p, "ADD-03-p1-r1")
    entries = yaml.safe_load((tmp_path / "curation/approvals.yaml").read_text())["approvals"]
    assert entries[-1]["origin"] == "interview_demo"


def test_catalog_includes_readings_and_planning_assumptions(monkeypatch, tmp_path):
    from tenderpack import interview
    from types import SimpleNamespace
    import tenderpack.readings as readings
    p = tmp_path / "pack.yaml"
    p.write_text("interview_demo: true\n")
    reading = SimpleNamespace(model_dump=lambda **kw: {"region_id": "IMG1", "source": {"doc": "DOC"}})
    monkeypatch.setattr(readings, "load_readings", lambda *a: {"IMG1": (reading, tmp_path / "reading.yaml")})
    monkeypatch.setattr(interview.stage2, "run", lambda *a: {"cfg": {}, "decisions": [], "reviews": {},
        "order": ["ADD-02"], "assumptions": {"submission": {"buffer": 0}}, "units": []})
    monkeypatch.setattr(interview.stage2, "register_findings", lambda *a: [])
    data = interview.catalog(tmp_path, p, tmp_path / "build")
    assert {x["kind"] for x in data["items"]} == {"reading", "assumption"}


def test_every_visible_demo_output_is_labelled(tmp_path):
    from tenderpack import interview
    import pymupdf
    (tmp_path / "result.html").write_text('<html><body><h1>Result</h1></body></html>')
    (tmp_path / "result.json").write_text('{"release":"RELEASABLE"}')
    doc = pymupdf.open(); doc.new_page(); doc.save(tmp_path / 'result.pdf'); doc.close()
    interview.mark_outputs(tmp_path)
    assert "INTERVIEW DEMO" in (tmp_path / "result.html").read_text()
    assert json.loads((tmp_path / "result.json").read_text())["_interview_demo"]
    with pymupdf.open(tmp_path / "result.pdf") as doc:
        assert "INTERVIEW DEMO" in doc[0].get_text()


def test_time_guard_terminates_cleanly_and_records_resumable_stop(tmp_path):
    import sys
    from tenderpack import interview
    child = tmp_path / "child.py"
    child.write_text('import signal,time,sys\nfrom pathlib import Path\ndef stop(*a):\n Path("checkpoint.txt").write_text("saved")\n sys.exit(130)\nsignal.signal(signal.SIGTERM,stop)\ntime.sleep(20)\n')
    result = interview.run_timed([sys.executable, str(child)], tmp_path, 0.3)
    assert result["budget_reached"] and result["exit_code"] == 130
    assert (tmp_path / "checkpoint.txt").read_text() == "saved"


def test_interview_run_profile_sizes_batches_and_guards_resume():
    from tenderpack import interview
    cfg={'interview':{'analysis_batch_size':5,'downstream_batch_size':4,'time_budget_s':1200}}
    args=interview.timed_args(['ai','run','ADD-03','--pdf','new.pdf'],cfg)
    assert args[:5]==['interview','timed','--seconds','1200','--']
    assert args[args.index('--downstream-batch-size')+1]=='4'
    assert '--batch-size' not in interview.timed_args(['ai','resume','existing'],cfg)
