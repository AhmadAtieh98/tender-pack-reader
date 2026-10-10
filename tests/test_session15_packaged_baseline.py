"""Validate the shipped state separately from source tests that require unreviewed curation."""
import json
import pytest
from tenderpack import interview, stage2
from tenderpack.util import ROOT, load_yaml


@pytest.mark.skipif(not (ROOT / 'INTERVIEW.json').exists(), reason='only in a packaged interview copy')
def test_shipped_add02_baseline_is_complete_and_hash_bound():
    cfg = load_yaml(ROOT / 'config/pack.yaml')
    assert cfg.get('interview_demo') is True
    assert len(cfg['documents']) == 6
    assert cfg['documents'][-1]['doc_id'] == 'ADD-02'
    assert interview.verify_frozen(ROOT) == []
    r = stage2.run(ROOT / 'build', ROOT / 'config/pack.yaml', ROOT)
    assert r['order'][-1] == 'ADD-02'
    assert stage2.register_findings(r) == []
    checks = json.loads((ROOT / 'out/checks.json').read_text())
    assert checks['status'] == 'ok'
    assert all(check['ok'] for check in checks['structural'])
    assert 'INTERVIEW DEMO' in checks['release']['status']
    for path in ('a1/a1.xlsx','a2/a2.md','a3/a3.pdf','a5/gantt.pdf'):
        assert (ROOT / 'out' / path).stat().st_size > 0
