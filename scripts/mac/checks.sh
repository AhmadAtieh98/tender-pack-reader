#!/usr/bin/env bash
# tenderpack on the owner's Mac: the OFFLINE checks (session 12; session 13: exit codes and blockers examined).
# Turn Wi-Fi off first, then:   bash scripts/mac/checks.sh
#   --plan          print the checks without running them
#   --no-ai         skip the two checks that need Ollama
#   --no-workflow   check 7: skip level 3 (the whole offline run; it can take long with a local model)
#   --only 6,7      run only the listed checks (checks 4 and 5 read check 2's outputs: list 2 with them)
#
# The AI checks have THREE levels (session 14), each printed on its own line; an exit code of 0 is never read as
# "validated" (scripts/mac/levels.py reads the records):
#   level 1  connectivity (check 6): Ollama answers /api/tags, the model is installed, /api/show reports vision, tools
#            and context
#   level 2  valid content (check 7): the one-batch request returned a proposal set that PASSED the controller's
#            validation, read from the run's own record (proposals.yaml: the set status and each item's status)
#   level 3  complete workflow (check 7): a whole `ai run --offline` to the candidate outputs and the review packet,
#            its status and completeness read from the checkpoint; a partial run that exited 0 is PARTIAL, never PASS
# Everything is written to a scratch folder ($TMPDIR/tenderpack-checks-<time>); the folder's build/, out/ and staging/
# are not touched. Nothing here calls a hosted service or downloads anything: TENDERPACK_OFFLINE=1 is set, so any AI
# step can only use the local Ollama (a hosted route is refused before any call).
#
# How a check decides (session 13): the exit code of the command is captured IMMEDIATELY (never after a pipe), the
# blocker lines are read from its log, and the check passes only when the exit code is the expected one AND the
# blockers are exactly the expected human-approval blockers ("RELEASE BLOCKER [approval] ..."). Any other blocker
# (coverage, stale, a register defect) or a structural FAIL line fails the check and is printed.
set -u
cd "$(dirname "$0")/../.." || exit 2
ROOT="$(pwd)"
PY="${TENDERPACK_PY:-$ROOT/.venv/bin/python}"   # TENDERPACK_PY: another interpreter (tests)
export TENDERPACK_OFFLINE=1
PLAN=0; NOAI=0; NOWF=0; ONLY=""
while [ $# -gt 0 ]; do                                     # session 14 (W6): --no-workflow and --only
  case "$1" in
    --plan) PLAN=1 ;;
    --no-ai) NOAI=1 ;;
    --no-workflow) NOWF=1 ;;
    --only) shift; ONLY="${1:-}" ;;
    --only=*) ONLY="${1#--only=}" ;;
  esac
  shift
done
want() { [ -z "$ONLY" ] && return 0; case ",$ONLY," in *",$1,"*) return 0 ;; esac; return 1; }
CHECKS=(
  "0 network off (no default route; checked locally, nothing is contacted)"
  "1 ingest: the evidence build from the PDFs: exit 0 and STRUCTURE OK"
  "2 outputs: A1-A5 build: exit 0, published, no structural FAIL, only the human-approval blockers"
  "3 outputs --strict: exit 3 with only the human-approval blockers (exit 0 once everything is approved)"
  "4 the A1 xlsx opens (openpyxl here; open it in Numbers/Excel yourself)"
  "5 the HTML outputs parse (open them in a browser yourself)"
  "6 level 1, connectivity: ai ollama-models: Ollama answers, the installed models, their capabilities, context and memory, per phase (nothing pulled)"
  "7 level 2, valid content: one-batch offline request, its proposal set read for the validation statuses; level 3, complete workflow: a whole ai run --offline to the candidate outputs and the review packet, read from the checkpoint (--no-workflow skips it)"
  "8 the local panel (tenderpack panel)"
  "9 the installed versions match requirements.lock.txt (the locked set)"
  "10 tenderpack imports from outside the folder (the host route's MCP server starts in the session folder)"
)
if [ $PLAN -eq 1 ]; then printf '%s\n' "${CHECKS[@]}"; exit 0; fi
if [ ! -x "$PY" ]; then
  echo "FAIL     no python at $PY: run   bash \"$ROOT/scripts/mac/setup.sh\"   first"; exit 1
fi
OUT="${TMPDIR:-/tmp}"; OUT="${OUT%/}/tenderpack-checks-$(date +%Y%m%dT%H%M%S)"
mkdir -p "$OUT"
NPASS=0; NPEND=0; NFAIL=0; NPART=0
pass() { NPASS=$((NPASS+1)); echo "PASS     $*"; }
partial() { NPART=$((NPART+1)); echo "PARTIAL  $*"; }   # session 14: part of a level reached; never counted as a PASS
pend() { NPEND=$((NPEND+1)); echo "PENDING  $*"; }
fail() { NFAIL=$((NFAIL+1)); echo "FAIL     $*"; }
indent() { sed 's/^/           /'; }
blockers() { grep -E '^RELEASE BLOCKER \[' "$1" 2>/dev/null; }                      # every blocker line
defects() { grep -E '^RELEASE BLOCKER \[' "$1" 2>/dev/null | grep -vE '^RELEASE BLOCKER \[approval\] '; }
structural() { grep -E '^[A-Za-z0-9_.-]+ FAIL  ' "$1" 2>/dev/null; }                  # a structural check that failed
count() { if [ -z "$1" ]; then echo 0; else printf '%s\n' "$1" | wc -l | tr -d ' '; fi; }
echo "tenderpack offline checks; logs and outputs in $OUT"

# 0. network off --------------------------------------------------------------------------------------------------
if want 0; then
if route -n get default >/dev/null 2>&1 || ip route show default 2>/dev/null | grep -q default; then
  pend "0 a default network route exists: turn Wi-Fi off and run again for a true offline check"
else
  pass "0 no default network route (offline)"
fi
fi

# 1. ingest -------------------------------------------------------------------------------------------------------
if want 1; then
"$PY" -m tenderpack ingest --out "$OUT/build" >"$OUT/ingest.log" 2>&1
RC=$?
if [ $RC -eq 0 ] && grep -q "^STRUCTURE OK" "$OUT/ingest.log"; then
  pass "1 ingest: exit 0, STRUCTURE OK ($(grep -o 'units: [0-9]*' "$OUT/ingest.log" | head -1); log $OUT/ingest.log)"
else
  fail "1 ingest: exit $RC (expected 0 with STRUCTURE OK); see $OUT/ingest.log"
  grep -E "STRUCTURAL FAILURE|Error|error" "$OUT/ingest.log" | head -5 | indent
fi
fi

# 2 and 3. outputs: the exit code AND the blockers ------------------------------------------------------------------
judge_outputs() {   # $1 check number, $2 log, $3 exit code, $4 expected exit ("0" or "3"), $5 what
  local n="$1" log="$2" rc="$3" want="$4" what="$5" all def sf na
  all="$(blockers "$log")"; def="$(defects "$log")"; sf="$(structural "$log")"
  na=$(( $(count "$all") - $(count "$def") ))
  if [ -n "$def" ] || [ -n "$sf" ]; then
    fail "$n $what: exit $rc with $(count "$def") defect blocker(s) and $(count "$sf") structural FAIL line(s) (see $log):"
    { printf '%s\n' "$sf"; printf '%s\n' "$def"; } | grep -v '^$' | indent
    return
  fi
  if [ "$want" = "3" ] && [ "$rc" -eq 0 ] && [ "$na" -eq 0 ]; then
    pass "$n $what: exit 0 and no blocker (everything approved)"; return
  fi
  if [ "$rc" -ne "$want" ]; then
    fail "$n $what: exit $rc, expected $want (see $log)"; tail -3 "$log" | indent; return
  fi
  if [ "$want" = "3" ] && [ "$na" -eq 0 ]; then
    fail "$n $what: exit 3 but no blocker line in the log (a refusal must name its blockers; see $log)"; return
  fi
  if [ "$want" = "0" ] && ! grep -q "^OUTPUTS PUBLISHED" "$log"; then
    fail "$n $what: exit 0 but not published (no OUTPUTS PUBLISHED line; see $log)"; return
  fi
  pass "$n $what: exit $rc, $na approval blocker(s) only (human approvals pending; expected until you approve):"
  printf '%s\n' "$all" | grep -v '^$' | indent
}
if want 2 || want 4 || want 5; then
"$PY" -m tenderpack outputs --evidence "$OUT/build" --out "$OUT/out" >"$OUT/outputs.log" 2>&1
RC=$?
judge_outputs 2 "$OUT/outputs.log" "$RC" 0 "outputs"
fi
if want 3; then
"$PY" -m tenderpack outputs --evidence "$OUT/build" --out "$OUT/out-strict" --strict >"$OUT/strict.log" 2>&1
RC=$?
judge_outputs 3 "$OUT/strict.log" "$RC" 3 "outputs --strict"
fi

# 4. the xlsx -----------------------------------------------------------------------------------------------------
if want 4; then
X="$(ls "$OUT"/out/a1/*.xlsx 2>/dev/null | head -1)"
if [ -z "$X" ]; then fail "4 no A1 xlsx in $OUT/out/a1 (check 2 did not publish)"
else
  "$PY" -c "import sys, openpyxl; wb = openpyxl.load_workbook(sys.argv[1]); print(wb.sheetnames)" "$X" >"$OUT/xlsx.log" 2>&1
  RC=$?
  if [ $RC -eq 0 ]; then
    pass "4 A1 xlsx opens with openpyxl: $X ($(cat "$OUT/xlsx.log"))"
    pend "4 look at it in Numbers or Excel yourself: open \"$X\""
  else fail "4 the A1 xlsx does not open (exit $RC; see $OUT/xlsx.log)"; fi
fi
fi

# 5. the HTML -----------------------------------------------------------------------------------------------------
if want 5; then
NH=0; BAD=0
while IFS= read -r h; do
  NH=$((NH+1))
  "$PY" -c "import sys, html.parser; p = html.parser.HTMLParser(); p.feed(open(sys.argv[1], encoding='utf-8').read())" "$h" 2>/dev/null
  [ $? -eq 0 ] || BAD=$((BAD+1))
done < <(find "$OUT/out" -name '*.html' 2>/dev/null)
if [ $NH -gt 0 ] && [ $BAD -eq 0 ]; then
  pass "5 $NH HTML file(s) parse"
  pend "5 open one in a browser yourself (Arabic, links): open \"$(find "$OUT/out" -name '*.html' | head -1)\""
else fail "5 HTML: $NH found, $BAD did not parse"; fi
fi

# 6 and 7: local AI (Ollama), three levels (session 14, W6) ------------------------------------------------------
# Before session 14, check 7 printed "answered and validated" for ANY exit 0 of `ai propose` (which exits 0 for a
# partial set whose items all failed the validation). Now each level is read from its record by scripts/mac/levels.py.
if want 6 || want 7; then
if [ $NOAI -eq 1 ]; then
  pend "6 skipped (--no-ai)"; pend "7 skipped (--no-ai)"
elif ! command -v ollama >/dev/null 2>&1; then
  pend "6 ollama not installed: local AI checks not run (install the Ollama app yourself if you want the offline route)"
  pend "7 ollama not installed"
else
  # level 1: /api/tags (installed), /api/show per model (capabilities, context), memory vs this machine; no pull
  "$PY" -m tenderpack ai ollama-models --offline --json >"$OUT/ollama-models.json" 2>"$OUT/ollama-models.err"
  RC=$?
  "$PY" -m tenderpack ai ollama-models --offline >"$OUT/ollama-models.log" 2>&1
  "$PY" scripts/mac/levels.py connectivity "$OUT/ollama-models.json" >"$OUT/level1.txt" 2>&1
  L1=$?
  MSG="$(head -1 "$OUT/level1.txt")"
  if [ $RC -ne 0 ] && [ $RC -ne 1 ] && [ $RC -ne 3 ]; then
    fail "6 ai ollama-models ended with exit $RC (see $OUT/ollama-models.err)"; L1=1
  else
    case $L1 in
      0) pass "6 $MSG" ;;
      3) pend "6 $MSG" ;;
      *) fail "6 $MSG" ;;
    esac
  fi
  tail -n +2 "$OUT/level1.txt" | indent
  MODEL="$("$PY" scripts/mac/levels.py pick-model "$OUT/ollama-models.json" 2>/dev/null)"
  PDF="$ROOT/smoke-test/ADD-03_Addendum_No_3.pdf"           # the labelled synthetic smoke-test addendum
  if [ ! -f "$PDF" ]; then
    "$PY" tests/fixtures/make_drill.py "$OUT/drill" >/dev/null 2>&1
    PDF="$OUT/drill/ADD-03_Addendum_No_3.pdf"
  fi
  # level 2: one batch, its proposal set read for the controller's validation statuses
  L2=9
  if [ -z "$MODEL" ]; then
    pend "7 level 2 (valid content) not run: no installed model can serve the analysis (level 1 above)"
  else
    RUN="macchk-$(date +%Y%m%dT%H%M%S)"
    "$PY" -m tenderpack ai run ADD-03 --pdf "$PDF" --offline --run-id "$RUN" --out "$OUT/staging" \
       --worklog "$OUT/worklog" --stop-after ingest --no-background >"$OUT/run-ingest.log" 2>&1
    RC=$?
    if [ $RC -ne 0 ]; then
      fail "7 level 2 (valid content): the offline run was refused before the model step (exit $RC; see $OUT/run-ingest.log): $(grep -m1 'REFUSED\|FAILED' "$OUT/run-ingest.log")"
    else
      CAND="$OUT/staging/runs/$RUN/candidate"
      START=$(date +%s)
      "$PY" -m tenderpack ai propose ADD-03 --route ollama --offline --model "$MODEL" --provisions ADD-03:2.1 \
         --evidence "$CAND/build" --pack "$CAND/pack.yaml" --out "$OUT/staging-propose" --worklog "$OUT/worklog" \
         >"$OUT/propose.log" 2>&1
      RC=$?
      SECS=$(( $(date +%s) - START ))
      if [ $RC -eq 2 ] && grep -q "REFUSED" "$OUT/propose.log"; then
        pend "7 level 2 (valid content): refused before any call (exit 2; see $OUT/propose.log): $(grep -m1 REFUSED "$OUT/propose.log")"
      else
        "$PY" scripts/mac/levels.py content "$OUT/staging-propose" ADD-03:2.1 >"$OUT/level2.txt" 2>&1
        L2=$?
        MSG="$(head -1 "$OUT/level2.txt") [$MODEL; the request's exit $RC after ${SECS}s]"
        case $L2 in
          0) pass "7 $MSG" ;;
          4) partial "7 $MSG" ;;
          *) fail "7 $MSG" ;;
        esac
        tail -n +2 "$OUT/level2.txt" | indent
      fi
    fi
  fi
  # level 3: a whole offline run to the candidate outputs and the review packet, read from the checkpoint
  if [ $NOWF -eq 1 ]; then
    pend "7 level 3 (complete workflow) skipped (--no-workflow)"
  elif [ $L1 -ne 0 ] || [ $L2 -ne 0 ]; then
    pend "7 level 3 (complete workflow) not run: level 1 and level 2 must PASS first"
  else
    RUN3="macchk-full-$(date +%Y%m%dT%H%M%S)"
    echo "         level 3: a whole offline run of the smoke-test addendum (it can take long with a local model) ..."
    START=$(date +%s)
    "$PY" -m tenderpack ai run ADD-03 --pdf "$PDF" --offline --run-id "$RUN3" --out "$OUT/staging-full" \
       --worklog "$OUT/worklog" --no-background >"$OUT/run-full.log" 2>&1
    RC=$?
    SECS=$(( $(date +%s) - START ))
    "$PY" scripts/mac/levels.py workflow "$OUT/staging-full/runs/$RUN3" "$RC" >"$OUT/level3.txt" 2>&1
    L3=$?
    MSG="$(head -1 "$OUT/level3.txt") [${SECS}s; log $OUT/run-full.log]"
    case $L3 in
      0) pass "7 $MSG" ;;
      4) partial "7 $MSG" ;;
      5) pend "7 $MSG" ;;
      *) fail "7 $MSG" ;;
    esac
    tail -n +2 "$OUT/level3.txt" | indent
  fi
fi
fi

# 8. the panel ----------------------------------------------------------------------------------------------------
if want 8; then
"$PY" -m tenderpack panel --help >"$OUT/panel-help.log" 2>&1
RC=$?
if [ $RC -eq 0 ]; then pass "8 tenderpack panel answers --help (start it from launch.command, option 7)"
  pend "8 open the panel in Safari yourself (docs/VERIFY_ON_MAC.md, the panel check)"
else fail "8 tenderpack panel --help ended with exit $RC (see $OUT/panel-help.log)"; fi
fi

# 9. the locked set -----------------------------------------------------------------------------------------------
if want 9; then
"$PY" scripts/mac/lockcheck.py requirements.lock.txt >"$OUT/lockcheck.log" 2>&1
RC=$?
if [ $RC -eq 0 ]; then pass "9 installed versions match requirements.lock.txt ($(tail -1 "$OUT/lockcheck.log"))"
else
  fail "9 installed versions differ from requirements.lock.txt (lockcheck exit $RC):"
  indent <"$OUT/lockcheck.log"
  echo "           next: rm -rf \"$ROOT/.venv\" && bash \"$ROOT/scripts/mac/setup.sh\""
fi
fi

# 10. the folder link (session 13, E159) ---------------------------------------------------------------------------
if want 10; then
VO=""; [ -n "${TENDERPACK_PY:-}" ] && VO="--verify-only"   # session 14 (W6): another interpreter is never changed
LK="$("$PY" scripts/mac/pathlink.py --root "$ROOT" $VO 2>&1)"
RC=$?
if [ $RC -eq 0 ]; then pass "10 ${LK#PASS     }"
else
  fail "10 ${LK#FAIL     }"
  echo "           next: rm -rf \"$ROOT/.venv\" && bash \"$ROOT/scripts/mac/setup.sh\""
fi
fi

echo
echo "offline checks: ${NPASS} PASS, ${NPART} PARTIAL, ${NPEND} PENDING, ${NFAIL} FAIL  (everything in $OUT)"
[ "$NFAIL" -eq 0 ]
