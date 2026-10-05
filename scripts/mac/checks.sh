#!/usr/bin/env bash
# tenderpack on the owner's Mac: the OFFLINE checks (session 12). Turn Wi-Fi off first, then:   bash scripts/mac/checks.sh
#   --plan    print the checks without running them
#   --no-ai   skip the two checks that need Ollama
# Everything is written to a scratch folder ($TMPDIR/tenderpack-checks-<time>); the repository's build/, out/ and
# staging/ are not touched. Nothing here calls a hosted service or downloads anything: TENDERPACK_OFFLINE=1 is set, so
# any AI step can only use the local Ollama (a hosted route is refused before any call).
set -u
cd "$(dirname "$0")/../.." || exit 2
ROOT="$(pwd)"
PY="${TENDERPACK_PY:-$ROOT/.venv/bin/python}"   # TENDERPACK_PY: another interpreter (tests)
export TENDERPACK_OFFLINE=1
PLAN=0; NOAI=0
for a in "$@"; do [ "$a" = "--plan" ] && PLAN=1; [ "$a" = "--no-ai" ] && NOAI=1; done
CHECKS=(
  "0 network off (no default route; checked locally, nothing is contacted)"
  "1 ingest: the evidence build from the PDFs (STRUCTURE OK)"
  "2 outputs: A1-A5 build, exit 0, published, no structural check failed"
  "3 outputs --strict: exit 3 with only the human-approval blockers (exit 0 once everything is approved)"
  "4 the A1 xlsx opens (openpyxl here; open it in Numbers/Excel yourself)"
  "5 the HTML outputs parse (open them in a browser yourself)"
  "6 ai routes --offline: ollama reachable, the configured models' capabilities checked"
  "7 one-batch ai run --offline against the installed model (a synthetic addendum, isolated staging)"
  "8 the local panel (tenderpack panel) when it exists"
)
if [ $PLAN -eq 1 ]; then printf '%s\n' "${CHECKS[@]}"; exit 0; fi
[ -x "$PY" ] || { echo "FAIL     no .venv: run bash scripts/mac/setup.sh first"; exit 1; }
OUT="${TMPDIR:-/tmp}/tenderpack-checks-$(date +%Y%m%dT%H%M%S)"
mkdir -p "$OUT"
NPASS=0; NPEND=0; NFAIL=0
pass() { NPASS=$((NPASS+1)); echo "PASS     $*"; }
pend() { NPEND=$((NPEND+1)); echo "PENDING  $*"; }
fail() { NFAIL=$((NFAIL+1)); echo "FAIL     $*"; }
echo "tenderpack offline checks; logs and outputs in $OUT"

# 0. network off --------------------------------------------------------------------------------------------------
if route -n get default >/dev/null 2>&1 || ip route show default 2>/dev/null | grep -q default; then
  pend "0 a default network route exists: turn Wi-Fi off and run again for a true offline check"
else
  pass "0 no default network route (offline)"
fi

# 1. ingest -------------------------------------------------------------------------------------------------------
if "$PY" -m tenderpack ingest --out "$OUT/build" >"$OUT/ingest.log" 2>&1; then
  pass "1 ingest: exit 0 ($(grep -o '[0-9]* units' "$OUT/ingest.log" | head -1); log $OUT/ingest.log)"
else fail "1 ingest failed (exit $?): see $OUT/ingest.log"; fi

# 2. outputs ------------------------------------------------------------------------------------------------------
if "$PY" -m tenderpack outputs --evidence "$OUT/build" --out "$OUT/out" >"$OUT/outputs.log" 2>&1; then
  if grep -q "OUTPUTS PUBLISHED" "$OUT/outputs.log" && ! grep -qE "^[A-Z][0-9]+ +FAIL" "$OUT/outputs.log"; then
    pass "2 outputs: exit 0, published, no structural check failed ($(grep -c 'RELEASE BLOCKER' "$OUT/outputs.log") release blocker line(s): human approvals)"
  else fail "2 outputs: exit 0 but not published cleanly (see $OUT/outputs.log)"; fi
else fail "2 outputs failed (exit $?): see $OUT/outputs.log"; fi

# 3. outputs --strict ----------------------------------------------------------------------------------------------
"$PY" -m tenderpack outputs --evidence "$OUT/build" --out "$OUT/out-strict" --strict >"$OUT/strict.log" 2>&1
RC=$?
if [ $RC -eq 0 ]; then pass "3 outputs --strict: exit 0 (everything approved)"
elif [ $RC -eq 3 ]; then pass "3 outputs --strict: exit 3, the release blockers listed in $OUT/strict.log (human approvals pending; expected until you approve)"
else fail "3 outputs --strict: exit $RC (see $OUT/strict.log)"; fi

# 4. the xlsx -----------------------------------------------------------------------------------------------------
X="$(ls "$OUT"/out/a1/*.xlsx 2>/dev/null | head -1)"
if [ -n "$X" ] && "$PY" -c "import sys, openpyxl; wb = openpyxl.load_workbook(sys.argv[1]); print(wb.sheetnames)" "$X" >"$OUT/xlsx.log" 2>&1; then
  pass "4 A1 xlsx opens with openpyxl: $X ($(cat "$OUT/xlsx.log"))"
  pend "4 look at it in Numbers or Excel yourself: open \"$X\""
else fail "4 the A1 xlsx is missing or does not open (see $OUT/xlsx.log)"; fi

# 5. the HTML -----------------------------------------------------------------------------------------------------
NH=0; BAD=0
while IFS= read -r h; do
  NH=$((NH+1))
  "$PY" -c "import sys, html.parser; p = html.parser.HTMLParser(); p.feed(open(sys.argv[1], encoding='utf-8').read())" "$h" 2>/dev/null || BAD=$((BAD+1))
done < <(find "$OUT/out" -name '*.html' 2>/dev/null)
if [ $NH -gt 0 ] && [ $BAD -eq 0 ]; then
  pass "5 $NH HTML file(s) parse"
  pend "5 open one in a browser yourself (Arabic, links): open \"$(find "$OUT/out" -name '*.html' | head -1)\""
else fail "5 HTML: $NH found, $BAD did not parse"; fi

# 6 and 7: local AI (Ollama) ---------------------------------------------------------------------------------------
if [ $NOAI -eq 1 ]; then
  pend "6 skipped (--no-ai)"; pend "7 skipped (--no-ai)"
elif ! command -v ollama >/dev/null 2>&1; then
  pend "6 ollama not installed: local AI checks not run"; pend "7 ollama not installed"
else
  "$PY" -m tenderpack ai routes --offline >"$OUT/routes.log" 2>&1
  if grep -q "NOT USABLE\|could not be reached" "$OUT/routes.log"; then
    pend "6 ai routes --offline: some configured local models are not usable (see $OUT/routes.log; nothing was pulled)"
  else
    pass "6 ai routes --offline: every configured local model checked (see $OUT/routes.log)"
  fi
  sed -n '/^ollama:/,/^$/p' "$OUT/routes.log" | sed 's/^/           /'
  PDF="$ROOT/rehearsals/blind-02/input/ADD-03_Addendum_No_3.pdf"
  RUN="macchk-$(date +%Y%m%dT%H%M%S)"
  if "$PY" -m tenderpack ai run ADD-03 --pdf "$PDF" --offline --run-id "$RUN" --out "$OUT/staging" \
       --worklog "$OUT/worklog" --stop-after ingest --no-background >"$OUT/run-ingest.log" 2>&1; then
    CAND="$OUT/staging/runs/$RUN/candidate"
    START=$(date +%s)
    "$PY" -m tenderpack ai propose ADD-03 --route ollama --offline --provisions ADD-03:2.1 \
       --evidence "$CAND/build" --pack "$CAND/pack.yaml" --out "$OUT/staging-propose" --worklog "$OUT/worklog" \
       >"$OUT/propose.log" 2>&1
    RC=$?; SECS=$(( $(date +%s) - START ))
    if [ $RC -eq 0 ]; then pass "7 one-batch offline request answered and validated in ${SECS}s: $(grep '^run ' "$OUT/propose.log" | head -1)"
    elif grep -q "REFUSED" "$OUT/propose.log"; then pend "7 refused before any call (see $OUT/propose.log): $(grep REFUSED "$OUT/propose.log" | head -1)"
    else fail "7 the one-batch offline request ended with exit $RC after ${SECS}s (see $OUT/propose.log)"; fi
  else
    fail "7 the offline run was refused before the model step (see $OUT/run-ingest.log): $(grep -m1 'REFUSED\|FAILED' "$OUT/run-ingest.log")"
  fi
fi

# 8. the panel (built by another agent later: detected, never assumed) ----------------------------------------------
if "$PY" -m tenderpack panel --help >/dev/null 2>&1; then pass "8 tenderpack panel exists (start it from launch.command, option 7)"
else pend "8 tenderpack panel is not in this version yet"; fi

echo
echo "offline checks: ${NPASS} PASS, ${NPEND} PENDING, ${NFAIL} FAIL  (everything in $OUT)"
[ "$NFAIL" -eq 0 ]
