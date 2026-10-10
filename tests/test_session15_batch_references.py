"""References must keep their meaning across batch namespaces and interruption boundaries."""
import json
from types import SimpleNamespace

import pytest

from tenderpack.ai import workflow as W
from tenderpack.ai.contract import ChangeProposal, DownstreamItem, DownstreamSet, ProposalSet, StateIdentity, Statement


STATE = StateIdentity(pack_id="demo", evidence_build_id="fixture", validated_stage="ADD-02", working_stage="ADD-03")


def item(cls, id="item", **kw):
    return cls(id=id, state=STATE, statement_type="escalation",
               payload={"why": "needs a choice", "what_is_unsupported": "fixture"},
               **({"task": "task"} if cls is DownstreamItem else {"provision": "ADD-03:1"}), **kw)


def proposal(cls, items):
    return cls(run_id="fixture", created="-", route="host", provider="host", model_requested="fixture",
               task="propose_downstream" if cls is DownstreamSet else W.controller.TASK,
               addendum="ADD-03", state=STATE, items=items,
               statements=[Statement(id="basis", kind="interpretation", text="proposed basis")])


def context(tmp_path, batches):
    cp = SimpleNamespace(batches=lambda phase: list(batches), batch=batches.__getitem__)
    ws = SimpleNamespace(identity=lambda: STATE, refresh=lambda: None, staging=tmp_path / "staging",
                         root=tmp_path, evidence=tmp_path / "evidence")
    return SimpleNamespace(cp=cp, ws=ws, s={"route": "host"}, run_id="demo", addendum="ADD-03")


def test_analysis_combination_remaps_statement_dependencies_without_changing_unit_ids(tmp_path, monkeypatch):
    ps = proposal(ProposalSet, [item(ChangeProposal, statements=["basis"], dependencies=["basis", "VOL-I:1"])])
    ctx = context(tmp_path, {"analysis-001": {"status": "done", "staged_run": "fixture", "items": ["item"]}})
    monkeypatch.setattr(W, "_load_staged", lambda *a: (ps, {}))
    captured = []
    class Captured(Exception):
        pass
    def validate(ws, merged, *args, **kwargs):
        captured.append(merged)
        raise Captured
    monkeypatch.setattr(W.controller, "validate_set", validate)
    with pytest.raises(Captured):
        W.step_validation(ctx, {})
    assert captured[0].items[0].dependencies == ["analysis-001/basis", "VOL-I:1"]
    assert captured[0].items[0].statements == ["analysis-001/basis"]
    assert ps.items[0].dependencies == ["basis", "VOL-I:1"]


def downstream(tmp_path, sets):
    batches = {}
    for bid, ds in sets.items():
        path = tmp_path / f"{bid}.json"
        path.write_text(ds.model_dump_json())
        batches[bid] = {"status": "done", "result": str(path)}
    return W._combined_downstream(context(tmp_path, batches))


def test_downstream_statement_dependencies_follow_their_batch(tmp_path):
    ds = proposal(DownstreamSet, [item(DownstreamItem, dependencies=["basis", "VOL-I:1"], statements=["basis"])])
    combined = downstream(tmp_path, {"downstream-001": ds})
    assert combined.items[0].dependencies == ["downstream-001/basis", "VOL-I:1"]


def test_downstream_dependencies_follow_renamed_duplicate_item_in_same_batch(tmp_path):
    first = proposal(DownstreamSet, [item(DownstreamItem)])
    second = proposal(DownstreamSet, [item(DownstreamItem), item(DownstreamItem, "child", dependencies=["item"])])
    combined = downstream(tmp_path, {"downstream-001": first, "downstream-002": second})
    assert combined.items[-1].dependencies == ["downstream-002/item"]
    assert combined.items[-2].id == "downstream-002/item"
    assert second.items[-1].dependencies == ["item"]


def test_duplicate_ids_inside_one_batch_are_not_silently_bound_to_an_arbitrary_item(tmp_path):
    ds = proposal(DownstreamSet, [item(DownstreamItem), item(DownstreamItem)])
    with pytest.raises(ValueError, match="duplicate.*item"):
        downstream(tmp_path, {"downstream-001": ds})
