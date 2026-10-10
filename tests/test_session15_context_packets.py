from pathlib import Path
from ai_fixture import workspace
from tenderpack.ai import controller, downstream
from tenderpack.ai.contract import ProposalSet
from tenderpack.util import load_yaml


def test_interview_packet_carries_full_effective_target_text(tmp_path, blind02_build):
    ws = workspace(tmp_path, evidence=blind02_build)
    cfg=tmp_path/'ai.yaml';cfg.write_text('routes: {host: {paid: false}}\ninterview: {complete_target_context: true}\n')
    ws.ai_config=cfg
    packet=controller.task_packet(ws,'ADD-03',['ADD-03:5.3'])
    before=ws.stage(ws.prev_stage('ADD-03')).state
    targets=[c for p in packet['provisions'] for c in p['candidate_targets'] if 'text' in c]
    assert targets and any(len(before[c['target']].text)>240 for c in targets)
    assert all(c['text']==before[c['target']].text for c in targets)


def test_real_downstream_context_rejects_changed_state_and_matches_native_basis(tmp_path, blind02_build):
    import pytest
    from tenderpack.ai.tools import ToolError
    ws=workspace(tmp_path,evidence=blind02_build)
    ps=ProposalSet(run_id='context-test',created='2026-10-08T00:00:00Z',provider='host-session',route='host',model_requested='fixture',
                   task=controller.TASK,addendum='ADD-03',state=ws.identity(),items=[])
    ws.downstream_context={'analysis':ps.model_dump(mode='json'),'tasks':[{'id':'task','kind':'escalation'}]}
    promoted,kinds=downstream.validation_basis(ws)
    assert promoted['r2']['order'][-1]=='ADD-03' and kinds=={'task':'escalation'}
    ws.downstream_context['analysis']['state']['evidence_build_id']='different'
    with pytest.raises(ToolError,match='stale'):
        downstream.validation_basis(ws)
