#!/bin/bash
# Session 14: the full suite as the coordinator ran it (about 73 min in the cloud container; 1,575 passed, 1 skipped).
# Usage: bash worklog/continuation-s14/scripts/run_suite.sh > suite.log 2>&1   (temporary files under $SCRATCH)
set -u
cd "$(dirname "$0")/../../.."
S="${SCRATCH:-/tmp/tenderpack-s14}/suite"; mkdir -p "$S"
echo "suite start $(date -u +%H:%M:%SZ) on $(git rev-parse --short HEAD)"
time .venv/bin/python -m pytest -q -p no:cacheprovider --basetemp="$S/pt" --durations=15 tests/
echo "suite end $(date -u +%H:%M:%SZ)"
