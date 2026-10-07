#!/usr/bin/env bash
# tenderpack on the owner's Mac: the OFFLINE checks (session 12; session 13: exit codes and blockers examined).
# Turn Wi-Fi off first, then:   bash scripts/mac/checks.sh
#   --plan    print the checks without running them
#   --no-ai   skip the two checks that need Ollama
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
PLAN=0; NOAI=0
for a in "$@"; do [ "$a" = "--plan" ] && PLAN=1; [ "$a" = "--no-ai" ] && NOAI=1; done
CHECKS=(
  "0 network off (no default route; checked locally, nothing is contacted)"
  "1 ingest: the evidence build from the PDFs: exit 0 and STRUCTURE OK"
  "2 outputs: A1-A5 build: exit 0, published, no structural FAIL, only the human-approval blockers"
  "3 outputs --strict: exit 3 with only the human-approval blockers (exit 0 once everything is approved)"
  "4 the A1 xlsx opens (openpyxl here; open it in Numbers/Excel yourself)"
  "5 the HTML outputs parse (open them in a browser yourself)"
  "6 ai ollama-models: the installed local models, their capabilities, context and memory, per phase (nothing pulled)"
  "7 one-batch ai run --offline against an installed model (the smoke-test addendum, isolated staging)"
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
NPASS=0; NPEND=0; NFAIL=0
pass() { NPASS=$((NPASS+1)); echo "PASS     $*"; }
pend() { NPEND=$((NPEND+1)); echo "PENDING  $*"; }
fail() { NFAIL=$((NFAIL+1)); echo "FAIL     $*"; }
indent() { sed 's/^/           /'; }
blockers() { grep -E '^RELEASE BLOCKER \[' "$1" 2>/dev/null; }                      # every blocker line
defects() { grep -E '^RELEASE BLOCKER \[' "$1" 2>/dev/null | grep -vE '^RELEASE BLOCKER \[approval\] '; }
structural() { grep -E '^[A-Za-z0-9_.-]+ FAIL  ' "$1" 2>/dev/null; }                  # a structural check that failed
count() { if [ -z "$1" ]; then echo 0; else printf '%s\n' "$1" | wc -l | tr -d ' '; fi; }
echo "tenderpack offline checks; logs and outputs in $OUT"

# 0. network off --------------------------------------------------------------------------------------------------
if route -n get default >/dev/null 2>&1 || ip route show default 2>/dev/null | grep -q default; then
  pend "0 a default network route exists: turn Wi-Fi off and run again for a true offline check"
else
  pass "0 no default network route (offline)"
fi

# 1. ingest -------------------------------------------------------------------------------------------------------
"$PY" -m tenderpack ingest --out "$OUT/build" >"$OUT/ingest.log" 2>&1
RC=$?
if [ $RC -eq 0 ] && grep -q "^STRUCTURE OK" "$OUT/ingest.log"; then
  pass "1 ingest: exit 0, STRUCTURE OK ($(grep -o 'units: [0-9]*' "$OUT/ingest.log" | head -1); log $OUT/ingest.log)"
else
  fail "1 ingest: exit $RC (expected 0 with STRUCTURE OK); see $OUT/ingest.log"
  grep -E "STRUCTURAL FAILURE|Error|error" "$OUT/ingest.log" | head -5 | indent
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
"$PY" -m tenderpack outputs --evidence "$OUT/build" --out "$OUT/out" >"$OUT/outputs.log" 2>&1
RC=$?
judge_outputs 2 "$OUT/outputs.log" "$RC" 0 "outputs"
"$PY" -m tenderpack outputs --evidence "$OUT/build" --out "$OUT/out-strict" --strict >"$OUT/strict.log" 2>&1
RC=$?
judge_outputs 3 "$OUT/strict.log" "$RC" 3 "outputs --strict"

# 4. the xlsx -----------------------------------------------------------------------------------------------------
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

# 5. the HTML -----------------------------------------------------------------------------------------------------
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

# 6 and 7: local AI (Ollama) ---------------------------------------------------------------------------------------
if [ $NOAI -eq 1 ]; then
  pend "6 skipped (--no-ai)"; pend "7 skipped (--no-ai)"
elif ! command -v ollama >/dev/null 2>&1; then
  pend "6 ollama not installed: local AI checks not run (install the Ollama app yourself if you want the offline route)"
  pend "7 ollama not installed"
else
  # discovery: /api/tags (installed), /api/show per model (capabilities, context), memory vs this machine; no pull
  "$PY" -m tenderpack ai ollama-models --offline >"$OUT/ollama-models.log" 2>&1
  RC=$?
  case $RC in
    0) pass "6 ai ollama-models: every phase has an installed model that can serve it (see $OUT/ollama-models.log)" ;;
    1) pend "6 ai ollama-models: Ollama answers, but some phase has no installed model that can serve it (nothing was pulled; the listing says what is missing)" ;;
    3) pend "6 ai ollama-models: Ollama is installed but does not answer on its local address: start the Ollama app (or 'ollama serve') and run again" ;;
    *) fail "6 ai ollama-models ended with exit $RC (see $OUT/ollama-models.log)" ;;
  esac
  indent <"$OUT/ollama-models.log" | head -40
  PDF="$ROOT/smoke-test/ADD-03_Addendum_No_3.pdf"           # the labelled synthetic smoke-test addendum
  if [ ! -f "$PDF" ]; then
    "$PY" tests/fixtures/make_drill.py "$OUT/drill" >/dev/null 2>&1
    PDF="$OUT/drill/ADD-03_Addendum_No_3.pdf"
  fi
  if [ $RC -ne 0 ]; then
    pend "7 not run: check 6 found no installed model for every phase (see above)"
  else
    RUN="macchk-$(date +%Y%m%dT%H%M%S)"
    "$PY" -m tenderpack ai run ADD-03 --pdf "$PDF" --offline --run-id "$RUN" --out "$OUT/staging" \
       --worklog "$OUT/worklog" --stop-after ingest --no-background >"$OUT/run-ingest.log" 2>&1
    RC=$?
    if [ $RC -ne 0 ]; then
      fail "7 the offline run was refused before the model step (exit $RC; see $OUT/run-ingest.log): $(grep -m1 'REFUSED\|FAILED' "$OUT/run-ingest.log")"
    else
      CAND="$OUT/staging/runs/$RUN/candidate"
      START=$(date +%s)
      "$PY" -m tenderpack ai propose ADD-03 --route ollama --offline --provisions ADD-03:2.1 \
         --evidence "$CAND/build" --pack "$CAND/pack.yaml" --out "$OUT/staging-propose" --worklog "$OUT/worklog" \
         >"$OUT/propose.log" 2>&1
      RC=$?
      SECS=$(( $(date +%s) - START ))
      if [ $RC -eq 0 ]; then pass "7 one-batch offline request answered and validated in ${SECS}s: $(grep '^run ' "$OUT/propose.log" | head -1)"
      elif [ $RC -eq 2 ] && grep -q "REFUSED" "$OUT/propose.log"; then
        pend "7 refused before any call (exit 2; see $OUT/propose.log): $(grep -m1 REFUSED "$OUT/propose.log")"
      else fail "7 the one-batch offline request ended with exit $RC after ${SECS}s (see $OUT/propose.log)"; fi
    fi
  fi
fi

# 8. the panel ----------------------------------------------------------------------------------------------------
"$PY" -m tenderpack panel --help >"$OUT/panel-help.log" 2>&1
RC=$?
if [ $RC -eq 0 ]; then pass "8 tenderpack panel answers --help (start it from launch.command, option 7)"
  pend "8 open the panel in Safari yourself (docs/VERIFY_ON_MAC.md, the panel check)"
else fail "8 tenderpack panel --help ended with exit $RC (see $OUT/panel-help.log)"; fi

# 9. the locked set -----------------------------------------------------------------------------------------------
"$PY" scripts/mac/lockcheck.py requirements.lock.txt >"$OUT/lockcheck.log" 2>&1
RC=$?
if [ $RC -eq 0 ]; then pass "9 installed versions match requirements.lock.txt ($(tail -1 "$OUT/lockcheck.log"))"
else
  fail "9 installed versions differ from requirements.lock.txt (lockcheck exit $RC):"
  indent <"$OUT/lockcheck.log"
  echo "           next: rm -rf \"$ROOT/.venv\" && bash \"$ROOT/scripts/mac/setup.sh\""
fi

# 10. the folder link (session 13, E159) ---------------------------------------------------------------------------
LK="$("$PY" scripts/mac/pathlink.py --root "$ROOT" 2>&1)"
RC=$?
if [ $RC -eq 0 ]; then pass "10 ${LK#PASS     }"
else
  fail "10 ${LK#FAIL     }"
  echo "           next: rm -rf \"$ROOT/.venv\" && bash \"$ROOT/scripts/mac/setup.sh\""
fi

echo
echo "offline checks: ${NPASS} PASS, ${NPEND} PENDING, ${NFAIL} FAIL  (everything in $OUT)"
[ "$NFAIL" -eq 0 ]
