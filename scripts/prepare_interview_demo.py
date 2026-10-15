#!/usr/bin/env python3
"""Create an explicit, frozen ADD02 interview copy. Never commit, push or modify source curation.

Run with the source environment: .venv/bin/python scripts/prepare_interview_demo.py [--host claude|codex] /absolute/destination
The returned folder has its own code and launchers; setup.sh installs locked dependencies on first launch.
--host selects the host route's profile (default claude: the signed-in Claude Code CLI; codex: the signed-in Codex CLI).
"""
from pathlib import Path
import argparse
import datetime as dt
import hashlib
import json
import shutil
import subprocess
import sys
import yaml

from make_interview_folder import build, _files, write_zip, verify

ROOT = Path(__file__).resolve().parents[1]
HOSTS = {'claude': {'profile': ROOT / 'config/interview-ai.yaml', 'name': 'Claude Code',
                    'label': 'Claude Code interview demo: frozen ADD02; local changes',
                    'signin': 'Run `claude auth status` first; `claude auth login` signs in, `claude update` updates it.',
                    'viewer': 'If an embedded PDF viewer is blank, use the adjacent HTML detail link or open the panel in Safari.'},
         'codex': {'profile': ROOT / 'config/interview-ai-codex.yaml', 'name': 'Codex',
                   'label': 'Codex interview demo: frozen ADD02; local changes',
                   'signin': 'The Codex CLI must be installed and signed in.',
                   'viewer': 'If Codex’s embedded PDF viewer is blank, use the adjacent HTML detail link or open the panel in Safari.'}}


def parse(argv):
    p = argparse.ArgumentParser(prog='prepare_interview_demo.py')
    p.add_argument('--host', choices=sorted(HOSTS), default='claude')
    p.add_argument('destination')
    a = p.parse_args(argv)
    return Path(a.destination).resolve(), a.host


def guide_text(host):
    h = HOSTS[host]
    return f'''INTERVIEW DEMO — explicitly simulated approvals, not a tender release.

1. Double-click INTERVIEW_START.command to open the local panel.
2. ADD02 results are already built. Open A1–A5 without making an AI call.
   Use Safari for PDF viewing and clickable detail links; use Excel for the register.
   {h['viewer']}
3. Use All demo decisions to inspect approvals, evidence and history, edit a proposal, or change a decision.
   Edits must pass the native validators before updated outputs are published. No model is called for an edit.
   Search assumption:lead_times or assumption:resources for simple duration, effort and capacity controls.
4. Upload the unseen ADD03 PDF from Home. The default host uses signed-in {h['name']}, configured in config/ai.yaml.
   {h['signin']}
   Analysis covers the new addendum and its affected dependencies. Deterministic integrity checks still read baseline files.
5. A run has a configurable 45-minute guard, with checkpoint cleanup afterwards. This is a limit, not a runtime promise.
   A partial/stopped result is not completion.
   Resume from Runs; completed submissions and unchanged reading/downstream answers are reused and revalidated.
6. Each run has its own candidate outputs and All decisions link. The original ADD02 working copy is separate.
7. RESTORE_ADD02.command restores the frozen baseline after verifying its hashes. Previous files and run history remain
   in staging/interview/history and staging/ai/runs. Restoration refuses while a run is active.

A decision edit is currently available after active jobs finish. It creates a new proposed revision; approve separately.
Unresolved evidence and unavailable facts remain unresolved. No approval simulation invents a missing answer.
A new full ADD03 runtime is not promised by this package: timings must be measured on the intended addendum.
'''


def launchers(folder, host='claude'):
    common = '#!/bin/bash\nset -euo pipefail\ncd "$(dirname "$0")"\nif [[ ! -x .venv/bin/python ]]; then bash scripts/mac/setup.sh; fi\n'
    actions = {'INTERVIEW_START.command': 'panel --open',
               'RESTORE_ADD02.command': 'interview restore'}
    for name, command in actions.items():
        p = folder / name
        p.write_text(common + 'exec .venv/bin/python -m tenderpack ' + command + '\n')
        p.chmod(0o755)
    (folder / 'DEMO_GUIDE.txt').write_text(guide_text(host))


def export(folder, archive):
    """Export through a clean directory so the local venv/cache/run history never enters the zip."""
    scratch = archive.parent / ('.export-' + folder.name)
    if scratch.exists():
        raise RuntimeError(f'export scratch already exists: {scratch}')
    scratch.mkdir()
    clean = scratch / folder.name
    shutil.copytree(folder, clean, ignore=shutil.ignore_patterns('.venv','__pycache__','.pytest_cache','.DS_Store'))
    # Operating/test run data is local. Frozen baseline and source test fixtures are retained.
    for rel in ('staging/panel','staging/interview','staging/codex-runtime-smoke','worklog/model_calls','codex'):
        shutil.rmtree(clean / rel, ignore_errors=True)
    for run in (clean / 'staging/ai/runs').glob('*'):
        if run.is_dir() and (run / 'checkpoint.json').exists():
            shutil.rmtree(run)
    (clean / 'MANIFEST.sha256').unlink(missing_ok=True)
    meta_path = clean / "INTERVIEW.json"
    meta = json.loads(meta_path.read_text())
    meta.update(files=len(_files(clean)) + 1, interview_demo=True)
    demo_tests = sorted(p.relative_to(clean).as_posix() for pattern in ('test_session15_*.py', 'test_session16_*.py', 'test_session17_*.py', 'test_session18_*.py')
                        for p in (clean / 'tests').glob(pattern))
    if demo_tests:
        meta.setdefault('source_quick_tests_argv', meta.get('quick_tests_argv', []))
        meta['quick_tests_argv'] = ['-m', 'pytest', '-q', '--durations=10', *demo_tests]
        meta['verification_scope'] = ('Demo runtime regressions and shipped ADD02 baseline checks. '
                                      'Run the full regression suite in the source checkout; older source tests '
                                      'expect unreviewed curation rather than simulated approvals.')
    meta_path.write_text(json.dumps(meta, indent=1) + "\n")
    sums = [f'{hashlib.sha256((clean / p).read_bytes()).hexdigest()}  {p}' for p in _files(clean)]
    (clean / 'MANIFEST.sha256').write_text('\n'.join(sums)+'\n')
    now = dt.datetime.now(dt.timezone.utc)
    write_zip(clean, archive, (now.year,now.month,now.day,now.hour,now.minute,0))
    problems = verify(clean,archive)
    if problems:
        raise RuntimeError(problems)
    shutil.copyfile(clean / 'MANIFEST.sha256',folder / 'MANIFEST.sha256')
    shutil.copyfile(meta_path, folder / "INTERVIEW.json")
    shutil.rmtree(scratch)
    return {'zip':str(archive),'files':len(sums)+1,'zip_bytes':archive.stat().st_size,'verified':True}


def prepare(destination, host='claude'):
    result=build(destination, label=HOSTS[host]['label'],repo=ROOT)
    folder=Path(result['folder'])
    pack=folder/'config/pack.yaml'; cfg=yaml.safe_load(pack.read_text()); cfg['interview_demo']=True
    pack.write_text('# Explicit interview demo simulation.\n'+yaml.safe_dump(cfg,sort_keys=False))
    shutil.copyfile(HOSTS[host]['profile'],folder/'config/ai.yaml')
    launchers(folder, host)
    for args in (['ingest'],['interview','assume'],['outputs','--strict'],['interview','freeze']):
        # python -m starts with this copied package's cwd; dependencies come from the invoking locked environment.
        name='-'.join(args).replace('--','')
        with (folder/'logs'/f'prepare-{name}.log').open('w') as log:
            subprocess.run([sys.executable,'-m','tenderpack',*args],cwd=folder,stdout=log,stderr=subprocess.STDOUT,check=True)
    result.update(export(folder,Path(result['zip'])))
    return result


if __name__=='__main__':
    destination, host = parse(sys.argv[1:])
    result = prepare(destination, host)
    result['host'] = host
    print(json.dumps(result,indent=2))
