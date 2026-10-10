import copy

from ai_fixture import workspace
from tenderpack.ai import controller, downstream
from tenderpack.ai.contract import ProposalSet


def basis(tmp_path, build):
    ws = workspace(tmp_path, evidence=build)
    ps = ProposalSet(run_id='context', created='2026-10-10', provider='host', route='host',
                     model_requested='fixture', task=controller.TASK, addendum='ADD-03',
                     state=ws.identity(), items=[])
    ws.downstream_context = {'analysis': ps.model_dump(mode='json'), 'tasks': []}
    promoted, _ = downstream.validation_basis(ws)
    return ws, promoted


def test_activity_only_packet_contains_its_effective_requirement_text(tmp_path, blind02_build):
    ws, promoted = basis(tmp_path, blind02_build)
    ev, template = next((ev, t) for ev, ts in ws.r['templates'].items() if not ev.startswith('_')
                        for t in ts if t['id'] == 'assemble-envelope-a')
    task = {'id': 'act:assemble-envelope-a', 'kind': 'activity', 'evidence_item': ev,
            'activity': template, 'rows': ['VOL-I-6.1-01']}
    before = copy.deepcopy(task)
    packet = downstream.packet(ws, 'ADD-03', [task], promoted, 1, ws.identity().model_dump())
    assert 'VOL-I:6.1' in packet['units_after']
    assert 'VOL-I:9.1' in packet['units_after']
    current = packet['current_records']
    assert current['rows']['VOL-I-6.1-01']['definition']['units'] == ['VOL-I:6.1']
    assert current['activities']['assemble-envelope-a']['template'] == template
    effective = downstream._stage(promoted['r2'], 'ADD-03').state
    assert packet['units_after']['VOL-I:6.1']['text'] == ' '.join(effective['VOL-I:6.1'].text.split())
    assert task == before


def test_conditional_packet_supplies_named_records_without_unrelated_register_dump(tmp_path, blind02_build):
    ws, promoted = basis(tmp_path, blind02_build)
    entry = ws.r['clarifications']['clarifications'][0]
    task = {'id': 'impact:fixture', 'kind': 'conditional_impact', 'provisions': [],
            'scope': {'rows': ['VOL-I-6.1-01'], 'units': [], 'activities': ['assemble-envelope-a'],
                      'clarifications': [entry['id']]}}
    packet = downstream.packet(ws, 'ADD-03', [task], promoted, 1, ws.identity().model_dump())
    context = packet['current_records']
    assert context['clarifications'][entry['id']] == entry
    assert set(context['rows']) == {'VOL-I-6.1-01'}
    assert set(context['activities']) == {'assemble-envelope-a'}
    assert 'VOL-I:6.1' in packet['units_after']
    assert not packet['tasks'][0].get('accepted')


def test_critic_receives_full_cited_consequence_not_only_its_fragment(tmp_path, blind02_build):
    from tenderpack.ai import critic
    from tenderpack.ai.contract import DownstreamItem
    ws, _ = basis(tmp_path, blind02_build)
    item = DownstreamItem(id='deadline-reading', state=ws.identity(), statement_type='row_reading',
        task='row:VOL-I-6.1-01', provision='ADD-03:2.1', target='VOL-I-6.1-01',
        payload={'row':'VOL-I-6.1-01','interpretation':{'stage':'ADD-03','quote':'deadline',
                 'consequence':{'unit':'VOL-I:6.6','quote':'will be rejected unopened and returned to the Bidder'}}},
        evidence=[{'doc':'VOL-I','unit_id':'VOL-I:6.6','page':3,'kind':'span',
                   'words':'will be rejected unopened and returned to the Bidder'}])
    packet=critic.batch_packet(ws,'ADD-03',[('reading',item,['consequential_interpretation'],{})])
    assert packet['units']['VOL-I:6.6']['text_before_addendum'] == ws.stage('ADD-02').state['VOL-I:6.6'].text


def test_named_form_context_includes_issue_and_bound_demo_review(tmp_path, blind02_build):
    ws, promoted = basis(tmp_path, blind02_build)
    r = promoted['r2']
    review = {'status': 'changed', 'decision': 'accept', 'origin': 'interview_demo',
              'note': 'Assumed approval only; no handling instruction.', 'fingerprint': 'old'}
    r['reviews'][('issue', 'I-F4A-FIELDS')] = review
    task = {'id': 'impact:form', 'kind': 'conditional_impact', 'provisions': [],
            'scope': {'rows': ['VOL-I-6.1-01'], 'units': []},
            'items': [{'payload': {'text': 'Review ADD-01:AppA/proposal-due-date and ADD-01:AppA/para1.'}}]}
    packet = downstream.packet(ws, 'ADD-03', [task], promoted, 1, ws.identity().model_dump())
    records = packet['current_records']
    assert records['issues']['I-F4A-FIELDS'] == r['curated_issues']['I-F4A-FIELDS']
    assert records['reviews']['issue:I-F4A-FIELDS'] == review
    assert 'ADD-01:AppA/proposal-due-date' in packet['units_after']
    assert 'ADD-01-AppA-01' in records['rows']
    assert len(records['rows']) < len(r['evals'])
    assert 'not a resolution' in records['review_note']
    records['reviews']['issue:I-F4A-FIELDS']['status'] = 'accepted'
    assert r['reviews'][('issue', 'I-F4A-FIELDS')]['status'] == 'changed'


def test_critic_sees_existing_form_issue_without_inventing_a_resolution(tmp_path, blind02_build):
    from tenderpack.ai import critic
    from tenderpack.ai.contract import DownstreamItem
    ws, _ = basis(tmp_path, blind02_build)
    item = DownstreamItem(id='form-review', state=ws.identity(), statement_type='issue',
        task='impact:form', payload={'text': 'Carry I-F4A-FIELDS forward; ADD-01:AppA/para1 still applies.'},
        evidence=[])
    packet = critic.batch_packet(ws, 'ADD-03', [('form', item, ['consequential_interpretation'], {})])
    assert packet['current_records']['issues']['I-F4A-FIELDS'] == ws.r['curated_issues']['I-F4A-FIELDS']
    assert 'ADD-01:AppA/para1' in packet['units']
    assert packet['current_records']['basis'].startswith('Current curated')
