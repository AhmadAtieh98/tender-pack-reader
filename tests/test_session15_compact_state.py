import copy
import pytest

from tenderpack.ai import contract, controller, downstream
from test_session15_batch_references import item, proposal
from tenderpack.ai import requests


CASES = [(contract.ProposalSet, contract.ChangeProposal, controller.parse_set, contract.model_fill_schema),
         (contract.DownstreamSet, contract.DownstreamItem, downstream.parse, contract.downstream_fill_schema)]


@pytest.mark.parametrize('set_cls,item_cls,parse,schema', CASES)
def test_compact_items_inherit_exactly_the_declared_set_state(set_cls,item_cls,parse,schema):
    original = proposal(set_cls, [item(item_cls), item(item_cls, 'second')])
    data = original.model_dump(mode='json', by_alias=True)
    fields = {k: data[k] for k in contract.CONTROLLER_SET_FIELDS if k in data}
    for entry in data['items']:
        entry.pop('state')
    before = copy.deepcopy(data)
    got = parse(data, fields, [])
    assert got.model_dump() == original.model_dump()
    assert data == before
    assert 'state' not in schema()['$defs'][item_cls.__name__]['properties']


@pytest.mark.parametrize('set_cls,item_cls,parse,schema', CASES)
def test_explicit_foreign_item_state_is_never_rebound_to_current_state(set_cls,item_cls,parse,schema):
    data = proposal(set_cls,[item(item_cls)]).model_dump(mode='json',by_alias=True)
    fields = {k:data[k] for k in contract.CONTROLLER_SET_FIELDS if k in data}
    data['items'][0]['state']['evidence_build_id'] = 'foreign-build'
    got = parse(data,fields,[])
    assert got.items[0].state.evidence_build_id == 'foreign-build'
    assert got.items[0].state != got.state
    data['items'][0].pop('state')
    data.pop('state')
    with pytest.raises((controller.ParseError, downstream.DownstreamParseError), match='state'):
        parse(data,fields,[])


@pytest.mark.parametrize('phase,set_cls,item_cls', [
    ('analysis',contract.ProposalSet,contract.ChangeProposal),
    ('downstream',contract.DownstreamSet,contract.DownstreamItem)])
def test_shared_request_checks_accept_compact_replies_without_a_repair(phase,set_cls,item_cls):
    data = proposal(set_cls,[item(item_cls)]).model_dump(mode='json',by_alias=True)
    data['items'][0].pop('state')
    checked, errors, problems = requests.check(requests.spec(phase), data)
    assert not errors
    assert not [p for p in problems if p['kind'] == 'schema'], problems
    assert checked['items'][0]['state'] == data['state']


def test_compact_repair_cannot_rebind_untouched_siblings_to_a_new_state():
    data = proposal(contract.ProposalSet,[item(contract.ChangeProposal),item(contract.ChangeProposal,'second')]).model_dump(mode='json')
    for i in data['items']:
        i.pop('state')
    repaired = copy.deepcopy(data)
    repaired['state']['evidence_build_id'] = 'foreign-build'
    merged, _ = contract.merge_repair(data,repaired,{'second'})
    assert merged['items'][0]['state'] == data['state']
    assert merged['items'][1]['state'] == repaired['state']
