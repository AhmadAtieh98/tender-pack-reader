#!/bin/bash
# Session 14 rebuild chain on the merged tree (the session-13 closing chain, unchanged in order): ingest, fixture, outputs
# into out/, drill into out-drill/, strict into scratch, check-register, the output diff against a918d5e, Mac checks.
set -u
cd /home/user/tender-pack-reader
S=/tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s14/rebuild
PY=.venv/bin/python
echo "== rebuild start $(date -u +%H:%M:%SZ) =="
$PY -m tenderpack ingest 2>&1 | tail -2
$PY tests/fixtures/make_fixture.py build/fixture-src 2>&1 | tail -1
$PY -m tenderpack ingest --pack build/fixture-src/pack.yaml --out build/fixture 2>&1 | tail -1
$PY -m tenderpack outputs --evidence build --out out 2>&1 | grep -E "C13|C43|C11|C48|BLOCKER|PUBLISHED|FAIL" ; echo "outputs exit ${PIPESTATUS[0]} $(date -u +%H:%M:%SZ)"
$PY tests/fixtures/make_drill.py build/drill-src 2>&1 | tail -1
$PY -m tenderpack ingest --pack build/drill-src/pack.yaml --out build/drill 2>&1 | tail -1
$PY -m tenderpack outputs --evidence build/drill --pack build/drill-src/pack.yaml --out out-drill 2>&1 | grep -E "BLOCKER|PUBLISHED|FAIL" | head -5; echo "drill exit ${PIPESTATUS[0]} $(date -u +%H:%M:%SZ)"
echo "== strict =="
rm -rf $S/out-strict
$PY -m tenderpack outputs --evidence build --out $S/out-strict --strict 2>&1 | grep -E "BLOCKER|REFUSED|PUBLISHED" ; echo "strict exit ${PIPESTATUS[0]} $(date -u +%H:%M:%SZ)"
echo "== check-register =="
$PY -m tenderpack check-register 2>&1 | grep -E "findings|C14"; echo "check-register exit ${PIPESTATUS[0]}"
echo "== output files changed against a918d5e =="
git diff --stat a918d5e -- out/ | tail -1
git diff --name-only a918d5e -- out/ | sed 's#out/##' | cut -d/ -f1 | sort | uniq -c
git diff --name-only a918d5e -- out/ > $S/changed_files.txt
echo "untracked new output files: $(git status --short out/ | grep '^??' | wc -l)"
git status --short out/ | grep '^??' >> $S/changed_files.txt
echo "== mac checks =="
TMPDIR=$S/mac bash scripts/mac/checks.sh --no-ai 2>&1 | tail -16; echo "checks exit ${PIPESTATUS[0]} $(date -u +%H:%M:%SZ)"
echo "== rebuild end $(date -u +%H:%M:%SZ) =="
