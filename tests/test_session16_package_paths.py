import os
from pathlib import Path
import shlex
import subprocess
import sys
import zipfile

from test_session14_interview_package import _mini


def test_package_verifier_runs_its_interpreter_with_relative_destination(tmp_path):
    archive=_mini(tmp_path,['-c',"print('1 passed in 0.01s')"])
    with zipfile.ZipFile(archive,'a') as z:
        entry=zipfile.ZipInfo('PKG/.venv/bin/python');entry.external_attr=0o100755 << 16
        z.writestr(entry,'#!/bin/bash\nexec '+shlex.quote(sys.executable)+' "$@"\n')
    script=Path(__file__).resolve().parents[1]/'scripts/mac/verify_package.sh'
    result=subprocess.run(['bash',str(script),str(archive),'--into','relative folder','--only','tests,smoke'],
        cwd=tmp_path,capture_output=True,text=True,
        env={k:v for k,v in os.environ.items() if not k.startswith('TENDERPACK_')},timeout=30)
    assert result.returncode==0,result.stdout+result.stderr
    assert 'PASS     tests:' in result.stdout and 'PASS     smoke:' in result.stdout
