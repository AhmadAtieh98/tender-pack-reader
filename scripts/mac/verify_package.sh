#!/usr/bin/env bash
# Verify the PACKAGED COPY of the interview folder itself (session 14, W6): unzip the zip into a fresh place and check
# what is in it, then set it up and run it there, never in the folder it was built from.
#
#   bash scripts/mac/verify_package.sh LAMAR-PPP-R2-INTERVIEW_<...>.zip [--into DIR] [--only STEPS] [--no-ai]
#
# Steps, in order (each prints PASS / PENDING / FAIL; --only unzip,manifest,bits,contents,... runs a subset; unzip is
# always run):
#   unzip     into a fresh folder (DIR must not exist or be empty; default $TMPDIR/tenderpack-verify-<time>)
#   manifest  every file matches MANIFEST.sha256, and no file is missing from it
#   bits      every *.command and *.sh is executable after the unzip (the zip keeps the bits)
#   contents  the parts the package must carry: the code, the runtime policies (tenderpack/ai/policy/), the locked
#             dependencies, the sources, the baseline build/ and out/, the launchers, RECOVERY.md, the quick-review
#             documentation, the Mac checklist, the smoke test, every focused test listed in INTERVIEW.json; no .venv
#   setup     scripts/mac/setup.sh in the unzipped folder (the locked set; needs the network or a uv cache once)
#   tests     the focused QUICK tests (INTERVIEW.json quick_tests_argv) with the folder's interpreter; FAIL past three
#             minutes, with the slowest tests named (add them to SLOW in scripts/make_interview_folder.py)
#   checks    scripts/mac/checks.sh --no-ai (without --no-ai when Ollama is installed and --no-ai is not given)
#   smoke     smoke-test/run_smoke.sh
# TENDERPACK_PY names an interpreter to use instead of the unzipped folder's .venv (with --only and no setup step).
# Nothing here calls a hosted AI service or downloads a model; setup may download the locked packages once.
set -u
ZIP=""; INTO=""; ONLY=""; NOAI=0
while [ $# -gt 0 ]; do
  case "$1" in
    --into) shift; INTO="${1:-}" ;;
    --only) shift; ONLY="${1:-}" ;;
    --no-ai) NOAI=1 ;;
    -h|--help) sed -n '2,23p' "$0"; exit 2 ;;
    *) ZIP="$1" ;;
  esac
  shift
done
want() { [ -z "$ONLY" ] && return 0; case ",$ONLY," in *",$1,"*) return 0 ;; esac; return 1; }
NPASS=0; NPEND=0; NFAIL=0
pass() { NPASS=$((NPASS+1)); echo "PASS     $*"; }
pend() { NPEND=$((NPEND+1)); echo "PENDING  $*"; }
fail() { NFAIL=$((NFAIL+1)); echo "FAIL     $*"; }
indent() { sed 's/^/           /'; }
finish() {
  echo
  echo "package verification: ${NPASS} PASS, ${NPEND} PENDING, ${NFAIL} FAIL  (unzipped copy: ${F:-none})"
  [ "$NFAIL" -eq 0 ]
  exit $?
}
sha_check() { if command -v shasum >/dev/null 2>&1; then shasum -a 256 -c "$1"; else sha256sum -c "$1"; fi; }

if [ -z "$ZIP" ] || [ ! -f "$ZIP" ]; then echo "FAIL     no zip given or not a file: '$ZIP' (usage: bash $0 PACKAGE.zip)"; exit 2; fi
ZIP="$(cd "$(dirname "$ZIP")" && pwd)/$(basename "$ZIP")"
T="${TMPDIR:-/tmp}"; INTO="${INTO:-${T%/}/tenderpack-verify-$(date +%Y%m%dT%H%M%S)}"
if [ -e "$INTO" ] && [ -n "$(ls -A "$INTO" 2>/dev/null)" ]; then
  echo "FAIL     $INTO is not empty: the packaged copy is verified in a FRESH place (give another --into)"; exit 2
fi
mkdir -p "$INTO"
INTO="$(cd "$INTO" && pwd)"
echo "verifying the packaged copy $ZIP in $INTO"

# unzip -------------------------------------------------------------------------------------------------------------
unzip -q "$ZIP" -d "$INTO" >"$INTO.unzip.log" 2>&1
RC=$?
TOPS="$(ls -A "$INTO")"
if [ $RC -ne 0 ] || [ "$(printf '%s\n' "$TOPS" | grep -c .)" -ne 1 ]; then
  fail "unzip: exit $RC; expected one top folder, found: $(printf '%s ' $TOPS)"; finish
fi
F="$INTO/$TOPS"
pass "unzip: one folder, $(find "$F" -type f | wc -l | tr -d ' ') files ($F)"

# manifest ----------------------------------------------------------------------------------------------------------
if want manifest; then
  if [ ! -f "$F/MANIFEST.sha256" ]; then fail "manifest: no MANIFEST.sha256 in the package"
  else
    (cd "$F" && sha_check MANIFEST.sha256) >"$INTO.manifest.log" 2>&1
    RC=$?
    BAD="$(grep -v ': OK$' "$INTO.manifest.log")"
    NLISTED=$(grep -c . "$F/MANIFEST.sha256")
    NFILES=$(( $(find "$F" -type f | wc -l) - 1 ))
    if [ $RC -eq 0 ] && [ -z "$BAD" ] && [ "$NLISTED" -eq "$NFILES" ]; then
      pass "manifest: $NLISTED file(s) match MANIFEST.sha256; no file outside it"
    else
      fail "manifest: exit $RC; $NLISTED listed, $NFILES in the folder; mismatches:"
      printf '%s\n' "$BAD" | head -10 | indent
    fi
  fi
fi

# executable bits ---------------------------------------------------------------------------------------------------
if want bits; then
  NOX=""
  while IFS= read -r x; do [ -x "$x" ] || NOX="$NOX ${x#$F/}"; done < <(find "$F" -type f \( -name '*.command' -o -name '*.sh' \))
  NX=$(find "$F" -type f \( -name '*.command' -o -name '*.sh' \) | wc -l | tr -d ' ')
  if [ -z "$NOX" ] && [ "$NX" -gt 0 ]; then pass "bits: all $NX *.command / *.sh are executable after the unzip"
  else fail "bits: not executable after the unzip:$NOX (of $NX)"; fi
fi

# contents ----------------------------------------------------------------------------------------------------------
if want contents; then
  MISSING=""
  for p in tenderpack/__init__.py tenderpack/ai/policy pyproject.toml uv.lock requirements.lock.txt sources config \
           curation build out scripts/mac/launch.command scripts/mac/setup.sh scripts/mac/checks.sh \
           scripts/mac/levels.py scripts/mac/verify_package.sh scripts/make_interview_folder.py RECOVERY.md README.md \
           INTERVIEW.json docs/QUICK_REVIEW.md docs/MAC_CHECKLIST.md docs/MAC_SETUP.md docs/VERIFY_ON_MAC.md \
           docs/AI_ROUTES.md config/routes_status.yaml smoke-test/run_smoke.sh; do
    [ -e "$F/$p" ] || MISSING="$MISSING $p"
  done
  NPOL=$(find "$F/tenderpack/ai/policy" -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
  [ "$NPOL" -gt 0 ] || MISSING="$MISSING tenderpack/ai/policy/*.md"
  while IFS= read -r t; do
    [ -n "$t" ] && { [ -f "$F/$t" ] || MISSING="$MISSING $t"; }
  done < <(sed -n 's/^ *"\(tests\/test_[A-Za-z0-9_]*\.py\)",\{0,1\}$/\1/p' "$F/INTERVIEW.json" 2>/dev/null)
  VENV="$(find "$F" -name pyvenv.cfg -o -type d -name .venv 2>/dev/null | head -3)"
  if [ -z "$MISSING" ] && [ -z "$VENV" ]; then
    pass "contents: the code, $NPOL runtime policy file(s), the lock, the sources, build/ and out/, the launchers, RECOVERY.md, QUICK_REVIEW.md, MAC_CHECKLIST.md, the smoke test and the focused tests are there; no .venv"
  else
    fail "contents: missing:${MISSING:- none}${VENV:+; a virtual environment was packaged: $VENV}"
  fi
fi

# the interpreter ---------------------------------------------------------------------------------------------------
PY="${TENDERPACK_PY:-$F/.venv/bin/python}"
if want setup && [ -z "${TENDERPACK_PY:-}" ]; then
  bash "$F/scripts/mac/setup.sh" >"$INTO.setup.log" 2>&1
  RC=$?
  if [ $RC -eq 0 ]; then pass "setup: $(grep '^setup checklist:' "$INTO.setup.log")"
  else fail "setup: exit $RC (see $INTO.setup.log):"; grep '^FAIL' "$INTO.setup.log" | head -5 | indent; fi
fi
if ! "$PY" -c 'raise SystemExit(0)' >/dev/null 2>&1; then
  if want tests || want checks || want smoke; then fail "no interpreter at $PY (the setup step did not build it)"; fi
  finish
fi

# the focused quick tests -------------------------------------------------------------------------------------------
if want tests; then
  ARGS=()
  while IFS= read -r a; do ARGS+=("$a"); done < <("$PY" -c 'import json, sys
for a in json.load(open(sys.argv[1], encoding="utf-8")).get("quick_tests_argv") or []: print(a)' "$F/INTERVIEW.json")
  LIMIT="${TENDERPACK_VERIFY_QUICK_LIMIT_S:-180}"
  if [ ${#ARGS[@]} -eq 0 ]; then fail "tests: INTERVIEW.json names no quick_tests_argv"
  else
    START=$(date +%s)
    (cd "$F" && "$PY" "${ARGS[@]}") >"$INTO.tests.log" 2>&1
    RC=$?
    SECS=$(( $(date +%s) - START ))
    LAST="$(grep -E '(passed|failed|error)' "$INTO.tests.log" | tail -1)"
    if [ $RC -ne 0 ]; then fail "tests: the focused quick tests ended with exit $RC after ${SECS}s: $LAST (see $INTO.tests.log)"
      grep -E '^(FAILED|ERROR)' "$INTO.tests.log" | head -10 | indent
    elif [ "$SECS" -gt "$LIMIT" ]; then
      fail "tests: the focused quick tests passed but took ${SECS}s, over ${LIMIT}s (three minutes): deselect the slowest (SLOW in scripts/make_interview_folder.py): $LAST"
      grep -E '^[0-9.]+s (call|setup|teardown)' "$INTO.tests.log" | head -10 | indent
    else pass "tests: the focused quick tests: $LAST in ${SECS}s (under ${LIMIT}s)"; fi
  fi
fi

# the checks --------------------------------------------------------------------------------------------------------
if want checks; then
  CA="--no-ai"; if [ $NOAI -eq 0 ] && command -v ollama >/dev/null 2>&1; then CA=""; fi
  TENDERPACK_PY="$PY" bash "$F/scripts/mac/checks.sh" $CA >"$INTO.checks.log" 2>&1
  RC=$?
  SUM="$(grep '^offline checks:' "$INTO.checks.log")"
  if [ $RC -eq 0 ]; then pass "checks ${CA:-(with the Ollama levels)}: $SUM"
  else fail "checks: exit $RC: $SUM (see $INTO.checks.log)"; grep -E '^FAIL' "$INTO.checks.log" | head -8 | indent; fi
  grep -E '^PENDING' "$INTO.checks.log" | head -8 | indent
fi

# the smoke test ----------------------------------------------------------------------------------------------------
if want smoke; then
  TENDERPACK_PY="$PY" bash "$F/smoke-test/run_smoke.sh" >"$INTO.smoke.log" 2>&1
  RC=$?
  if [ $RC -eq 0 ]; then pass "smoke: $(grep -m1 '^smoke test:' "$INTO.smoke.log")"
  else fail "smoke: exit $RC (see $INTO.smoke.log)"; grep -E '^FAIL' "$INTO.smoke.log" | head -5 | indent; fi
fi
finish
