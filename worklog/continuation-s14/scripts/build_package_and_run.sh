#!/bin/bash
# Session 14, part 6: build the interview package from the main tree, unzip it, build its .venv, PIN the host model
# and the concurrency for the timed run, then run the given addendum PDF through the package's panel with the
# session-14 driver (a submission just before the interruption, then a resume). Every step prints a clock.
# Usage: build_package_and_run.sh TAG PDF REHEARSAL_DIR MODEL PARALLEL LABEL
set -u
TAG="$1"; MODEL="$4"; PAR="$5"; LABEL="$6"
cd /home/user/tender-pack-reader
PDF=$(readlink -f "$2"); mkdir -p "$3"; R=$(readlink -f "$3")   # absolute: the driver cd's into the package folder
S=/tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s14
PY=.venv/bin/python
c() { echo "== $1 $(date -u +%H:%M:%SZ) =="; }
mkdir -p $S/pkg/$TAG/zip $S/pkg/$TAG/unzipped $S/pkg/$TAG/mac $S/pkg/$TAG/run
c "build"
$PY scripts/make_interview_folder.py $S/pkg/$TAG/zip --label "$LABEL" 2>&1 | tail -4
ZIP=$(ls $S/pkg/$TAG/zip/*.zip | head -1); NAME=$(basename "$ZIP" .zip); echo "zip: $ZIP"
c "unzip + manifest"
(cd $S/pkg/$TAG/unzipped && unzip -q "$ZIP") || { echo "unzip failed"; exit 2; }
F=$S/pkg/$TAG/unzipped/$NAME
(cd "$F" && sha256sum -c MANIFEST.sha256 2>&1 | grep -vc ': OK$' | sed 's/^/not-OK lines: /')
c "setup.sh"
(cd "$F" && bash scripts/mac/setup.sh 2>&1 | grep -E "^PASS|^FAIL|^PENDING|checklist" | tail -12); echo "setup exit ${PIPESTATUS[0]}"
c "pin the runtime model and the concurrency (the package copy only)"
$PY - "$F/config/ai.yaml" "$MODEL" <<'PY'
import sys, re
from pathlib import Path
p = Path(sys.argv[1]); lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
out = []; block = None
for ln in lines:
    if re.match(r"^[A-Za-z_]+:", ln): block = ln.split(":")[0]
    if block in ("host_session", "critic") and re.match(r"^  model: null", ln):
        ln = f"  model: {sys.argv[2]}   # session 14: pinned for the timed run (recorded in FROZEN.md)\n"
    out.append(ln)
p.write_text("".join(out), encoding="utf-8")
PY
sed -i "s/^  max_parallel_sessions: 1$/  max_parallel_sessions: $PAR/" "$F/config/ai.yaml"
grep -n "^  model:\|^  max_parallel_sessions" "$F/config/ai.yaml"
c "smoke test"
(cd "$F" && bash smoke-test/run_smoke.sh 2>&1 | tail -2)
echo "FOLDER=$F"
echo "code identity: $($PY - "$F" <<'PY'
import sys; from pathlib import Path
sys.path.insert(0, sys.argv[1])
from tenderpack.ai import checkpoint as C
print(C.code_identity(Path(sys.argv[1]))["content_sha256"][:16])
PY
)"
c "run"
echo "$TAG start $(date -u '+%Y-%m-%d %H:%M:%S UTC') (model $MODEL, max_parallel_sessions $PAR)" >> $R/clock.txt
bash $S/run_blind_panel.sh "$F" "$PDF" "$R" $S/pkg/$TAG/run
echo "driver exit $?"
c "end"
