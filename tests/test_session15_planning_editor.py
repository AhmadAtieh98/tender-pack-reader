import copy
from types import SimpleNamespace

import pytest

from tenderpack import interview, programme
from tenderpack.panel import views


def item(group='lead_times'):
    value = {'bond': {'value': 10, 'effort_wd': 1.5, 'basis': 'PROVISIONAL', 'owner': 'Commercial'}}
    if group == 'resources':
        value = {'legal': {'capacity': 2, 'basis': 'PROVISIONAL', 'owner': 'Legal'}}
    return {'id': 'assumption:' + group, 'kind': 'assumption', 'value': value,
            'fingerprint': 'bound', 'label': 'PLANNING ASSUMPTION', 'actions': ['edit'],
            'history': [], 'evidence': {}}


def test_quick_planning_edit_preserves_other_fields_and_records_new_basis():
    before = item()
    original = copy.deepcopy(before)
    result = interview.planning_edit(before, 'bond.value', '7', 'Bank confirmed turnaround')
    assert result['bond']['value'] == 7
    assert result['bond']['effort_wd'] == 1.5
    assert result['bond']['owner'] == 'Commercial'
    assert 'Bank confirmed turnaround' in result['bond']['basis']
    assert 'ASSUMPTION' in result['bond']['basis']
    assert before == original
    assert interview.planning_edit(item('resources'), 'legal.capacity', '2.5', 'Staff allocation')['legal']['capacity'] == 2.5


@pytest.mark.parametrize('group,path,value', [
    ('submission', 'bond.value', '7'), ('lead_times', 'bond.owner', '3'),
    ('lead_times', 'missing.value', '7'), ('lead_times', 'bond.value', '-1'),
    ('lead_times', 'bond.value', '1.5'), ('lead_times', 'bond.value', 'NaN'),
    ('resources', 'legal.capacity', 'Infinity'), ('resources', 'legal.capacity', '0'),
])
def test_quick_planning_edit_rejects_unsafe_or_invalid_fields(group,path,value):
    with pytest.raises(interview.InterviewError):
        interview.planning_edit(item(group), path, value, 'Reason')


def test_planning_form_exposes_numeric_inputs_with_bound_revision_and_no_javascript():
    html = views.interview_page('/t/x/', {'stage': 'ADD-02', 'items': [item()]}, {'run': 'candidate'})
    for expected in ('planning_field', 'bond.value', 'bond.effort_wd', 'planning_value',
                     'Update planning assumption', 'name="fingerprint" value="bound"',
                     'name="run" value="candidate"', 'Advanced structured edit'):
        assert expected in html
    assert '<script' not in html
    busy = views.interview_page('/t/x/', {'stage': 'ADD-02', 'items': [item()]}, {}, busy=True)
    assert 'value="planning" disabled' in busy


def test_base_programme_explains_missing_date_and_names_available_stages():
    r = {'stages': [SimpleNamespace(stage='BASE', issued=None),
                    SimpleNamespace(stage='ADD-02', issued='2026-10-22')]}
    with pytest.raises(ValueError, match='no validated issue date.*ADD-02'):
        programme.stage_planner(r, 'BASE')


def test_interview_guard_allows_a_complete_rehearsal_without_forced_25_minute_stop():
    from pathlib import Path
    import yaml
    cfg = yaml.safe_load((Path(__file__).resolve().parents[1] / 'config/interview-ai.yaml').read_text())
    assert cfg['interview']['time_budget_s'] == 2700
    assert interview.timed_args(['ai', 'resume', 'run'], {})[3] == '2700'
