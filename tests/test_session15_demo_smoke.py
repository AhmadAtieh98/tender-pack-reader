import hashlib
import importlib.util
from pathlib import Path


def test_demo_smoke_allows_only_unchanged_baseline_decisions(tmp_path):
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location('smoke_check', root / 'scripts/smoke_test/check_smoke.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cand = tmp_path / 'candidate'
    (cand / 'config').mkdir(parents=True)
    pack = cand / 'config/pack.yaml'
    pack.write_text('interview_demo: true\n')
    rel = 'curation/reviews/decisions.yaml'
    decisions = cand / rel
    decisions.parent.mkdir(parents=True)
    original = b'decisions: [{kind: row, item: R1, decision: accept, origin: interview_demo}]\n'
    decisions.write_bytes(original)
    cp = {'candidate': {'dir': str(cand), 'pack': str(pack)},
          'inputs': {'copied': {'decisions': rel}, 'real_hashes': {rel: hashlib.sha256(original).hexdigest()}}}
    assert mod.demo_baseline_unchanged(cp, tmp_path)
    decisions.write_bytes(original + b'# changed\n')
    assert not mod.demo_baseline_unchanged(cp, tmp_path)
    decisions.write_bytes(original)
    pack.write_text('interview_demo: false\n')
    assert not mod.demo_baseline_unchanged(cp, tmp_path)
