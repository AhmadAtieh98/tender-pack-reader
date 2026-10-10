import copy
import unicodedata

import pymupdf

from test_session16_downstream_context import basis
from tenderpack import partial
from tenderpack.ai import downstream


def test_shared_packaging_context_uses_programme_requirements_and_direct_inputs(tmp_path, blind02_build):
    ws, promoted = basis(tmp_path, blind02_build)
    ts = ws.r['templates']['EV-DELIVERY']
    batch = [{'id': 'act:' + t['id'], 'kind': 'activity', 'evidence_item': 'EV-DELIVERY',
              'activity': t, 'rows': ['VOL-I-6.1-01']}
             for t in ts if t['id'] in {'copies', 'assemble-envelope-b'}]
    before = copy.deepcopy(batch)
    packet = downstream.packet(ws, 'ADD-03', batch, promoted, len(batch), ws.identity().model_dump())
    assert {'VOL-I:6.5', 'VOL-I:App2/para1', 'VOL-I:10.1', 'VOL-I:10.3', 'VOL-I:10.6'} <= set(packet['units_after'])
    rec = packet['current_records']
    assert set(rec['activities']['copies']['evidence_items']) == {'EV-COPIES', 'EV-DELIVERY'}
    assert rec['issues']['I-VOL-I-ENV-B'] == promoted['r2']['curated_issues']['I-VOL-I-ENV-B']
    assert len(rec['rows']) < len(promoted['r2']['evals'])
    assert batch == before


def crowded_candidate():
    # Synthetic lengths exercise long generated identifiers without shipping recorded AI answers.
    issues = [{'id': f'I-ADD-03-DEMONSTRATION-HANDLING-{i:02}',
               'short': 'Missing instruction for handling the conditional document; obtain a recorded interpretation before finalising this item.',
               'text': 'Missing instruction for handling the conditional document.',
               'owner': 'Legal', 'rows': [], 'theme': 'Handling'} for i in range(30)]
    return {'stage': 'ADD-03', 'validated_stage': 'ADD-02', 'blockers': {'provisions': [
        {'provision': 'ADD-03:6.1', 'reason': 'The clause and period have not been identified.'},
        {'provision': 'ADD-03:7.1', 'reason': 'The replacement refers to wording superseded by an earlier addendum.'}]},
        'a3': {'title': 'A3 candidate', 'subtitle': 'Due date 2026-12-10. All rows remain candidate.',
               'banner': 'INTERVIEW DEMO', 'explicit': [], 'score': [], 'none_stated': [],
               'sections': [{'heading': 'Explicit consequences', 'items': [
                   {'id': f'REQ-{i:02}', 'text': 'Deliver the completed proposal and required supporting documentation by the stated deadline. Late submission will be rejected unopened. Supply executed originals, all supporting certificates and the required attachments, with the authority and validity evidence required by the current submission instructions.',
                    'confidence': 'high', 'source': 'VOL-I 6.6',
                    'flags': ['CANDIDATE interpretation; associated handling issue remains open'],
                    'consequence': 'will be rejected unopened and returned to the Bidder'} for i in range(17)]}],
               'groups': {'heading': 'Open issues', 'note': 'Unknown answers remain open.',
                          'groups': [{'title': f'Handling group {i}', 'items': issues[i*5:i*5+5], 'questions': []}
                                     for i in range(6)]},
               'issues_detail': issues, 'unresolved': {'heading': 'Unresolved', 'items': []},
               'footer': 'Full reasons and evidence: a3_detail.html'}}


def test_candidate_crowded_issues_fit_without_losing_identifiers_or_reasons(tmp_path):
    c = crowded_candidate()
    for item in c['a3']['sections'][0]['items']:
        item['text'] = 'Deliver the completed proposal and supporting documentation before the stated deadline; late submission will be rejected unopened.'
    before = copy.deepcopy(c)
    fit = partial.write_candidate_one_page(c, tmp_path)
    assert fit['pages'] == 1, fit
    assert fit['condensed'] <= 2
    with pymupdf.open(tmp_path / 'a3.pdf') as pdf:
        text = unicodedata.normalize('NFKC', pdf[0].get_text())
        assert all(f'REQ-{i:02}' in text for i in range(17))
        assert all(f'I-ADD-03-DEMONSTRATION-HANDLING-{i:02}' in text for i in range(30))
        assert text.count('Missing instruction') == 30
        assert 'ADD-03:6.1' in text and 'ADD-03:7.1' in text
        assert min(s['size'] for b in pdf[0].get_text('dict')['blocks'] if 'lines' in b
                   for line in b['lines'] for s in line['spans']) >= 7.5
    assert c == before


def test_two_column_layout_retains_every_group_and_issue():
    from tenderpack.render import _a3_html
    data = crowded_candidate()['a3']
    data['issue_columns'] = 2
    html = _a3_html(data)
    assert '<table class="issue-columns">' in html
    assert html.count('<td>') == 2
    for group in data['groups']['groups']:
        assert group['title'] in html
        for item in group['items']:
            assert item['id'] in html and item['short'] in html


def test_excessive_candidate_stays_explicitly_unfitted(tmp_path):
    c = crowded_candidate()
    for i in c['a3']['sections'][0]['items']:
        i['text'] *= 3
    fit = partial.write_candidate_one_page(c, tmp_path)
    assert fit['pages'] == 0 and fit['error']
    assert not (tmp_path / 'a3.pdf').exists()
    assert (tmp_path / 'a3_detail.html').exists()


def test_shared_activity_update_is_valid_under_either_existing_association(tmp_path, blind02_build):
    from tenderpack.ai.contract import DownstreamSet, DownstreamItem
    ws, promoted = basis(tmp_path, blind02_build)
    for ev, row in [('EV-COPIES', 'VOL-I-6.5-01'), ('EV-DELIVERY', 'VOL-I-6.1-01')]:
        template = copy.deepcopy(next(t for t in ws.r['templates'][ev] if t['id'] == 'copies'))
        template['name'] += ' (proposed wording revision)'
        unit = ws.units_by_id['VOL-I:6.5']
        item = DownstreamItem(id='shared-copy', state=ws.identity(), statement_type='activity', task='act:copies',
            payload={'evidence_item': ev, 'activity': template, 'rows': [row]},
            evidence=[{'doc': 'VOL-I', 'unit_id': 'VOL-I:6.5', 'page': unit['pages'][0],
                       'kind': 'span', 'words': unit['text']}])
        ds = DownstreamSet(run_id='shared-copy-test', created='2026-10-10', route='recorded', provider='test',
                           model_requested='fixture', addendum='ADD-03', state=ws.identity(), items=[item])
        result = downstream.validate(ws, ds, promoted, {'act:copies': 'activity'})
        assert not result['schedule_problems']
        assert not any(v.check == 'id' and not v.ok for v in item.validation)
        assert item.verification_status != 'invalid'


def test_shared_replacement_preserves_associations_and_unrelated_templates():
    import pytest
    templates = {'EV-A': [{'id': 'shared', 'name': 'old'}, {'id': 'other', 'name': 'untouched'}],
                 'EV-B': [{'id': 'shared', 'name': 'old'}], '_row_checks': {'ROW': {'activities': ['shared']}}}
    new = {'id': 'shared', 'name': 'revised'}
    assert downstream.replace_activity(templates, 'EV-A', new) == ['EV-A', 'EV-B']
    assert templates['EV-A'][1] == templates['EV-B'][0] == new
    assert templates['EV-A'][0] == {'id': 'other', 'name': 'untouched'}
    assert templates['_row_checks'] == {'ROW': {'activities': ['shared']}}
    before = copy.deepcopy(templates)
    with pytest.raises(ValueError):
        downstream.replace_activity(templates, 'EV-NEW', new)
    assert templates == before


def test_assembly_context_does_not_expand_into_whole_technical_design(tmp_path, blind02_build):
    ws, promoted = basis(tmp_path, blind02_build)
    template = next(t for t in ws.r['templates']['EV-DELIVERY'] if t['id'] == 'assemble-envelope-a')
    task = {'id': 'act:assemble-envelope-a', 'kind': 'activity', 'evidence_item': 'EV-DELIVERY',
            'activity': template, 'rows': ['VOL-I-6.1-01']}
    packet = downstream.packet(ws, 'ADD-03', [task], promoted, 1, ws.identity().model_dump())
    assert 'VOL-I:9.7' in packet['units_after']
    assert 'VOL-II:1.2' not in packet['units_after']
