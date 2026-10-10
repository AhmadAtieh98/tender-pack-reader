from types import SimpleNamespace

from tenderpack.ai import workflow as W


def test_prefetch_does_not_dispatch_a_batch_with_a_saved_submission(tmp_path, monkeypatch):
    record = tmp_path / "saved.json"
    record.write_text('{"run_id": "submitted-before-stop"}')
    dispatched = []
    pf = SimpleNamespace(recs={}, tried=set(), full=lambda: False, submit=lambda key, rec: dispatched.append(key))
    cp = SimpleNamespace(batches=lambda phase: ["analysis-001", "analysis-002"], batch=lambda key: {"status": "pending"})
    ctx = SimpleNamespace(prefetch=pf, cp=cp, stop_batches=False, stop_pending=None, s={"route": "host"})
    monkeypatch.setattr(W, "_submission_file", lambda ctx, key: record if key == "analysis-001" else tmp_path / "absent")
    monkeypatch.setattr(W, "_prep_analysis", lambda *a: {"work": "fixture"})
    W._fill(ctx, "analysis", "analysis-001")
    assert dispatched == ["analysis-002"]
    assert "analysis-001" not in pf.tried  # The ordered consumer must still revalidate it, or retry if stale.
