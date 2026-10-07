#!/usr/bin/env bash
# SMOKE TEST: synthetic, not tender content. Copied into <folder>/smoke-test/ by scripts/make_interview_folder.py.
#   bash smoke-test/run_smoke.sh
# The synthetic Addendum No. 3 (tests/fixtures/make_drill.py: invented for a drill, laid out like the real addenda)
# goes through the workflow's first, deterministic step: `tenderpack ai run ADD-03 ... --stop-after ingest` builds an
# isolated candidate workspace (in a scratch folder under $TMPDIR, never under staging/ or out/) and stops before any
# model step. NO MODEL IS CALLED and nothing leaves the machine: the run names the host route in manual mode
# (--host-manual never starts a process) only because a run needs a route; for that reason this one command runs
# without TENDERPACK_OFFLINE (offline mode refuses to name a hosted route at all), and check_smoke.py then proves from
# the run's own log that no model, host session or network call happened. It compares the result with
# smoke-test/expected.yaml (the drill builder's record of what it printed, not the program's output):
# exit 0, status stopped after ingest, the 12 provisions of ADD-03 all pending, approval none.
set -u
cd "$(dirname "$0")/.." || exit 2
ROOT="$(pwd)"
PY="${TENDERPACK_PY:-$ROOT/.venv/bin/python}"
if [ ! -x "$PY" ]; then
  echo "PROBLEM: no .venv in $ROOT"; echo "NEXT:    bash \"$ROOT/scripts/mac/setup.sh\""; exit 1
fi
cat smoke-test/LABEL.txt
OUT="${TMPDIR:-/tmp}"; OUT="${OUT%/}/tenderpack-smoke-$(date +%Y%m%dT%H%M%S)"
RUN="smoke-$(date +%Y%m%dT%H%M%S)"
mkdir -p "$OUT"
echo "running the synthetic ADD-03 to the end of ingest (no model call) into $OUT ..."
env -u TENDERPACK_OFFLINE "$PY" -m tenderpack ai run ADD-03 --pdf smoke-test/ADD-03_Addendum_No_3.pdf \
  --route host --host-manual --stop-after ingest --no-background --run-id "$RUN" \
  --out "$OUT/staging" --worklog "$OUT/worklog" --evidence build --pack config/pack.yaml >"$OUT/run.log" 2>&1
RC=$?
"$PY" smoke-test/check_smoke.py "$OUT/staging/runs/$RUN" smoke-test/expected.yaml "$RC" "$OUT/run.log"
