"""Session 11: `tenderpack ai resume RUN_ID --from STEP` reruns a step and the later ones on a run whose batches are
done (after a code change, e.g. the blind-04 run whose outputs build was refused), without asking any batch again.
Reuses the session-10 recorded workflow fixtures (no live call)."""
from __future__ import annotations

from test_session10_workflow import area, full, prev_build, quiet  # noqa: F401  (fixtures reused by name)
from tenderpack.ai import workflow as W


def test_resume_from_promotion_reruns_the_later_steps_and_asks_no_batch_again(full, area, monkeypatch):
    cp0 = W.load("full", area["staging"])
    assert all(cp0.done(s) for s in ("analysis", "downstream", "promotion", "outputs", "review"))
    attempts_before = {s: cp0.step(s)["attempts"] for s in W.STEPS}
    calls: list[tuple] = []
    real = W.WorkflowCassette.provider

    def spy(self, phase, keys, used):
        calls.append((phase, list(keys)))
        return real(self, phase, keys, used)
    monkeypatch.setattr(W.WorkflowCassette, "provider", spy)
    # retry_failed=False: a batch the recorded run left failed or escalated is not the subject here; done batches are
    # what must never be asked again
    res = W.resume("full", area["staging"], from_step="promotion", retry_failed=False, echo=quiet,
                   sleep=lambda s: None)
    assert calls == []                                                  # no batch of any phase asked again
    cp = W.load("full", area["staging"])
    for s in W.STEPS[W.STEPS.index("promotion"):]:
        assert cp.step(s)["attempts"] == attempts_before[s] + 1, s     # promotion and every later step rerun once
    for s in W.STEPS[:W.STEPS.index("promotion")]:
        assert cp.step(s)["attempts"] == attempts_before[s], s         # the earlier steps untouched
    ev = [e for e in cp.data["events"] if e["event"] == "resumed"]
    assert ev[-1].get("from_step") == "promotion"
    assert res["status"] == cp0.data["status"]                         # the same end state, recomputed


def test_resume_from_an_unknown_step_is_refused(full, area):
    import pytest
    from tenderpack.ai import budget as B
    with pytest.raises(B.Refused):
        W.resume("full", area["staging"], from_step="nowhere", echo=quiet, sleep=lambda s: None)
