from types import SimpleNamespace

import pytest

from tenderpack.ai import downstream as DS
from tenderpack.ai.contract import DependencyPayload, DownstreamItem, DownstreamSet
from test_session15_batch_references import item, proposal


@pytest.mark.parametrize('issue_status,existing,held', [
    ('conflicting', False, True),
    ('insufficient_evidence', False, True),
    ('interpretation_pending', False, False),
    ('conflicting', True, False),
])
def test_relationship_cannot_outlive_its_linked_issue(issue_status, existing, held):
    payload = DependencyPayload.model_validate({'from': 'VOL-I:6.3', 'to': 'bond-approval',
                  'kind': 'feeds_calculation', 'basis': 'The bond affects approval planning.',
                  'issues': ['I-SECURITY-IMPACT'], 'status': 'possible'})
    dependency = item(DownstreamItem, 'relationship').model_copy(update={
        'statement_type': 'dependency', 'payload': payload.model_dump(by_alias=True),
        'verification_status': 'interpretation_pending'})
    issue = item(DownstreamItem, 'issue').model_copy(update={
        'statement_type': 'issue', 'payload': {'id': 'I-SECURITY-IMPACT'},
        'verification_status': issue_status})
    ds = proposal(DownstreamSet, [dependency, issue])
    report = DS._closure(ds, [{'pl': payload}, {'pl': SimpleNamespace(id='I-SECURITY-IMPACT')}],
                         {}, {}, {'I-SECURITY-IMPACT'} if existing else set(), {}, {})
    assert ('relationship' in report) == held
    assert dependency.verification_status == ('insufficient_evidence' if held else 'interpretation_pending')
    if held:
        assert 'I-SECURITY-IMPACT' in report['relationship']
