from types import SimpleNamespace as NS

from tenderpack import partial
from tenderpack.amend import Disposition


def test_unresolved_candidate_targets_flag_rows_even_without_a_clause_in_the_words(monkeypatch):
    units = {uid: NS(text=text) for uid, text in {
        'ADD-03:6.1': 'The bid security period is extended by thirty days.',
        'VOL-I:6.3': 'Bond period', 'VOL-I:7.2': 'Validity extension',
        'VOL-II:4.4': 'Standby power'}.items()}
    baseline = NS(stage='ADD-02', state=units)
    working = NS(stage='ADD-03', state=units, ops=[],
        coverage=[{'provision': 'ADD-03:6.1', 'disposition': 'unresolved', 'reason': 'Target not established'}],
        dispositions=[Disposition(provision='ADD-03:6.1', disposition='unresolved',
                                   reason='Target not established', candidates=['VOL-I:6.3', 'VOL-I:7.2'])])
    r = {'working': working, 'validated': baseline, 'stages': [baseline, working], 'evals': [
        {'row': NS(id=uid.replace(':', '-') + '-01', units=[uid]),
         'stages': {'ADD-03': {'status': 'ACTIVE', 'stale': []}}}
        for uid in ['VOL-I:6.3', 'VOL-I:7.2', 'VOL-II:4.4']]}
    affected = partial.unresolved_rows(r)
    assert set(affected) == {'VOL-I-6.3-01', 'VOL-I-7.2-01'}
    assert all('POSSIBLE TARGET' in reason for reasons in affected.values() for reason in reasons)
    assert all('value in question' not in units[uid].text for uid in units)
    monkeypatch.setattr(partial, 'missing_documents', lambda *_: [])
    blockers = partial.blockers(r, affected, {'activities': [
        {'id': 'bond-issue', 'name': 'Issue bond', 'req_ids': ['VOL-I-6.3-01']}]}, [], {'stage': 'ADD-03'})
    assert blockers['provisions'][0]['rows'] == sorted(affected)
    assert blockers['provisions'][0]['activities'] == ['bond-issue']


def test_export_includes_audit_regressions(monkeypatch):
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root / 'scripts'))
    from make_interview_folder import focused_tests
    assert 'tests/test_session17_audit.py' in focused_tests(root)


def test_demo_issue_marker_preserves_reason_space_on_a3():
    from tenderpack.stage2 import pending_mark
    label = 'OPEN — REVIEW ASSUMED FOR DEMO (no observed human decision): '
    assert pending_mark(label + 'The permit has not been supplied') == 'DEMO OPEN: The permit has not been supplied'


def test_condensed_a3_moves_gate_id_catalogue_to_detail_before_dropping_reasons():
    from tenderpack.stage2 import condense_a3
    counts = '3 open issues: 1 listed, 0 folded (+n), 0 on a3_detail.html only, I-LONG-1, I-LONG-2 in the gate note.'
    a3 = {'sections': [], 'subtitle': '', 'banner': '', 'issue_counts': counts,
          'groups': {'note': counts + ' Unknown answers stay unknown.',
                     'counts': {'all': 3, 'listed': 1, 'folded': 0, 'detail_only': 0,
                                'gate_note': ['I-LONG-1', 'I-LONG-2']},
                     'groups': [{'questions': [], 'items': [{'id': 'I-X', 'short': 'Missing evidence', 'owner': 'Legal'}]}]}}
    page = condense_a3(a3, 2)
    assert 'I-LONG-1' not in page['groups']['note']
    assert '2 gate-note issues' in page['groups']['note']
    assert page['groups']['groups'][0]['items'][0]['short'] == 'Missing evidence'
    assert 'I-LONG-1' in a3['groups']['note']


def test_candidate_one_page_keeps_unresolved_reason_and_its_own_detail(tmp_path):
    import pymupdf
    import unicodedata
    c = {'stage': 'ADD-03', 'validated_stage': 'ADD-02',
         'a3': {'title': 'A3 CANDIDATE - NOT VALIDATED', 'subtitle': 'ADD-03', 'banner': 'INTERVIEW DEMO',
                'explicit': [], 'score': [], 'none_stated': [], 'issues_detail': [],
                'sections': [{'heading': 'Explicit rejection', 'items': [
                    {'id': 'R-1', 'text': 'Deliver by the deadline', 'confidence': 'high'}]}],
                'unresolved': {'heading': 'Unresolved', 'items': []}, 'footer': 'Full detail: a3_detail.html'},
         'blockers': {'provisions': [{'provision': 'ADD-03:6.1', 'reason': 'The clause and period are not identified.'}]}}
    result = partial.write_candidate_one_page(c, tmp_path)
    assert result['pages'] == 1
    with pymupdf.open(tmp_path / 'a3.pdf') as doc:
        text = unicodedata.normalize('NFKC', doc[0].get_text())
        assert 'NOT VALIDATED' in text and 'clause and period are not identified' in text
        links = doc[0].get_links()
        assert links
        assert all('a3_detail.html' in (link.get('uri') or link.get('file') or '') for link in links)
        assert all('/URI' in doc.xref_object(link['xref']) for link in links)
    assert 'clause and period are not identified' in (tmp_path / 'a3_detail.html').read_text()
