"""Session 13 (the blind-07 scorer's defect 15): the run's interruption bookkeeping named batches as "not taken"
that had been answered through their staged submissions (reuse never calls take(), so their prefetch records stayed),
and every reused submission was called "made before the interruption" even when it was made after the resume."""
from __future__ import annotations

from concurrent.futures import Future
from types import SimpleNamespace

from tenderpack.ai import workflow as W


def _ctx(batches: dict):
    events = []
    cp = SimpleNamespace(data={"batches": batches, "settings": {}},
                         event=lambda name, **kw: events.append({"event": name, **kw}))
    return SimpleNamespace(cp=cp, log=SimpleNamespace(event=lambda *a, **k: None)), events


def _done_future():
    f = Future()
    f.set_result(("ok", None))
    return f


def test_close_names_only_the_batches_still_pending():
    ctx, events = _ctx({"analysis-002": {"status": "done", "phase": "analysis"},
                        "analysis-004": {"status": "done", "phase": "analysis"},
                        "analysis-003": {"status": "interrupted", "phase": "analysis"}})
    pf = W.Prefetch(ctx, 2)
    for bid in ("analysis-002", "analysis-004", "analysis-003"):   # answered by reuse (never taken) and one pending
        pf.recs[bid] = {"future": _done_future(), "phase": "analysis", "key": "k", "t_dispatch": 0.0}
    pf.close(interrupted=True)
    not_taken = [e for e in events if e["event"] == "prefetch_not_taken"]
    assert len(not_taken) == 1 and not_taken[0]["batches"] == ["analysis-003"], events
    assert pf.recs == {}


def test_close_says_nothing_when_every_dispatched_batch_is_done():
    ctx, events = _ctx({"analysis-002": {"status": "done", "phase": "analysis"}})
    pf = W.Prefetch(ctx, 1)
    pf.recs["analysis-002"] = {"future": _done_future(), "phase": "analysis", "key": "k", "t_dispatch": 0.0}
    pf.close(interrupted=False)
    assert not [e for e in events if e["event"] == "prefetch_not_taken"]


def test_the_reuse_message_names_the_submission_time_not_the_interruption():
    import inspect
    src = inspect.getsource(W._reuse_submission) if hasattr(W, "_reuse_submission") else open(W.__file__).read()
    assert "made before the interruption" not in src
    assert "submitted {rec.get('ts')" in src
