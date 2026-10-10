from types import SimpleNamespace

import pytest

from tenderpack.ai import downstream as DS, tools
from tenderpack.ai.contract import DownstreamItem, DownstreamSet
from test_session15_batch_references import STATE, item, proposal


def test_downstream_dry_run_uses_the_promoted_state_and_task_kinds(monkeypatch):
    context = {"analysis": {"marker": "frozen"}, "tasks": [{"id": "task", "kind": "escalation"}]}
    ws = SimpleNamespace(downstream_context=context, identity=lambda: STATE)
    seen = []
    monkeypatch.setattr(DS, "validation_basis", lambda workspace: ({"r2": "post-amendment"}, {"task": "escalation"}))
    def validate(workspace, ds, promoted, kinds, **kw):
        seen.append((promoted, kinds))
        ds.items[0].verification_status = "escalated"
        return {"held_back": {}}
    monkeypatch.setattr(DS, "validate", validate)
    ds = proposal(DownstreamSet, [item(DownstreamItem)])
    result = tools.validate_proposal(ws, ds.model_dump())
    assert result["parsed"], result
    assert result["items"][0]["verification_status"] == "escalated"
    assert seen == [({"r2": "post-amendment"}, {"task": "escalation"})]


def test_downstream_draft_never_falls_back_to_analysis_without_a_controller_context():
    ds = proposal(DownstreamSet, [item(DownstreamItem)])
    with pytest.raises(tools.ToolError, match="downstream.*context"):
        tools.validate_proposal(SimpleNamespace(), ds.model_dump())
