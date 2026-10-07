#!/usr/bin/env bash
# tenderpack launcher for the Mac (session 12; session 13: the connected/offline choice and exact errors). Double-click
# it in Finder (or run it in Terminal). It uses the .venv that scripts/mac/setup.sh built IN THIS FOLDER.
#
# At the start it asks how AI steps run:
#   connected  Claude Code first (the host route, your plan pays); Codex, an API key and Ollama as configured and
#              usable (option 5 shows each route's live state and its tested/unverified status)
#   offline    the local Ollama only: TENDERPACK_OFFLINE=1 is exported, so every phase refuses a hosted route before
#              any process or network call
# Every failure prints two lines: PROBLEM (exactly what is wrong) and NEXT (the one command to run), then waits for
# Return when a person is at the keyboard. Keys are never asked for here: docs/AI_ROUTES.md "Keys" says where they go.
HERE="$(cd "$(dirname "$0")" 2>/dev/null && pwd)"
ROOT="$(cd "$HERE/../.." 2>/dev/null && pwd)"
pause() { if [ -t 0 ]; then read -r -p "Press Return to continue." _; fi; }
problem() { echo; echo "PROBLEM: $1"; echo "NEXT:    $2"; pause; }
stop() { problem "$1" "$2"; exit 1; }

# 1. the folder ---------------------------------------------------------------------------------------------------
if [ -z "$ROOT" ] || [ ! -f "$ROOT/pyproject.toml" ] || [ ! -d "$ROOT/tenderpack" ]; then
  stop "launch.command is not inside a tenderpack folder: $ROOT has no pyproject.toml and tenderpack/ (the launcher must stay at <folder>/scripts/mac/launch.command)" \
       "open the unzipped tenderpack folder in Finder and double-click scripts/mac/launch.command inside it"
fi
cd "$ROOT" || stop "cannot enter $ROOT" "ls -ld \"$ROOT\""
SETUP="bash \"$ROOT/scripts/mac/setup.sh\""
REBUILD="rm -rf \"$ROOT/.venv\" && $SETUP"

# 2. the interpreter: the .venv built here (or TENDERPACK_PY, for tests) --------------------------------------------
if [ -n "${TENDERPACK_PY:-}" ]; then
  PY="$TENDERPACK_PY"
  "$PY" -c 'raise SystemExit(0)' >/dev/null 2>&1 \
    || stop "TENDERPACK_PY=$PY does not run" "unset TENDERPACK_PY   (the launcher then uses $ROOT/.venv/bin/python)"
else
  PY="$ROOT/.venv/bin/python"
  if [ ! -e .venv ]; then
    stop "no .venv in $ROOT: the environment is built in this folder by setup (a copied .venv is not portable)" "$SETUP"
  fi
  if [ ! -x "$PY" ] || ! "$PY" -c 'raise SystemExit(0)' >/dev/null 2>&1; then
    stop "$ROOT/.venv/bin/python does not run (its base interpreter $(sed -n 's/^home = //p' .venv/pyvenv.cfg 2>/dev/null) was moved or removed, or the .venv was copied from another machine)" "$REBUILD"
  fi
  BUILT=""
  [ -f .venv/bin/activate ] && BUILT="$(sed -n "s/^ *VIRTUAL_ENV=[\"']\{0,1\}\([^\"']*\)[\"']\{0,1\} *$/\1/p" .venv/bin/activate | head -1)"
  if [ -n "$BUILT" ] && [ "$BUILT" != "$ROOT/.venv" ]; then
    stop "the .venv was built in another folder ($BUILT); a copied virtual environment is not portable" "$REBUILD"
  fi
fi
"$PY" -c 'raise SystemExit(0 if __import__("sys").version_info >= (3, 11) else 1)' >/dev/null 2>&1 \
  || stop "$PY is $("$PY" -V 2>&1), older than 3.11" "$REBUILD"
ERR="$("$PY" -c 'import pymupdf, openpyxl, pydantic, yaml, numpy' 2>&1)"
if [ $? -ne 0 ]; then
  stop "the .venv runs but tenderpack's dependencies do not import ($(echo "$ERR" | tail -1))" "$SETUP"
fi

# 3. connected or offline -----------------------------------------------------------------------------------------
MODE=""
case "${TENDERPACK_OFFLINE:-}" in 1|true|yes|on) MODE="offline" ;; esac
if [ -z "$MODE" ]; then
  echo
  echo "How should AI steps run?"
  echo "  1  connected: Claude Code first (host route; your plan pays); Codex, an API key and Ollama when usable"
  echo "  2  offline: the local Ollama only; no hosted call in any phase"
  read -r -p "> " M || exit 0
  case "$M" in 2) MODE="offline" ;; *) MODE="connected" ;; esac
fi
set_mode() {
  if [ "$MODE" = "offline" ]; then
    export TENDERPACK_OFFLINE=1
    echo "mode: offline (TENDERPACK_OFFLINE=1: a hosted route is refused before any call; local Ollama only)"
  else
    unset TENDERPACK_OFFLINE
    echo "mode: connected (Claude Code first; option 5 lists what is usable now)"
  fi
}
set_mode
routes() { "$PY" -m tenderpack ai routes --brief; }
echo
routes

has_panel() { "$PY" -m tenderpack panel --help >/dev/null 2>&1; }
said() {   # $1 exit code, $2 what exit 3 / 5 mean for this command
  case "$1" in
    0) echo "(exit 0: done)" ;;
    3) echo "(exit 3: $2)" ;;
    4) echo "(exit 4: waiting for a host submission: the manual path, $PY -m tenderpack ai submit-batch RUN_ID FILE --by \"Your Name\")" ;;
    5) echo "(exit 5: deferred by a rate limit; everything done is checkpointed: after the reset, $PY -m tenderpack ai resume RUN_ID)" ;;
    6) echo "(exit 6: stopped for a person: $PY -m tenderpack ai run-status RUN_ID says what it needs)" ;;
    *) echo "(exit $1: see the messages above; RECOVERY.md says what to do)" ;;
  esac
}
live_run() {   # prints "run_id|route|pid|state" for a live lock on the addendum, or nothing
  "$PY" -c '
import sys, time
from pathlib import Path
from tenderpack.ai import budget as B
p = B.lock_path(Path(sys.argv[1]), sys.argv[2])
info = B.read_lock(p)
if info:
    stale, why = B.lock_state(info, 120)
    print("|".join(str(x) for x in (info.get("run_id"), info.get("route"), info.get("pid"),
                                    "stale" if stale else "live", why)))
' "$ROOT/staging/ai" "$1" 2>/dev/null
}

while true; do
  echo
  echo "tenderpack ($ROOT) - $MODE"
  echo "  1  rebuild the evidence (ingest the PDFs into build/)"
  echo "  2  build the outputs A1-A5 into out/"
  echo "  3  strict check (the release check; exit 3 while approvals are pending)"
  echo "  4  check the register (check-register)"
  echo "  5  AI routes: what is usable now, its tested/unverified status, and why the others are not"
  if [ "$MODE" = "offline" ]; then
    echo "  6  run an addendum offline (local Ollama; a candidate under staging/ai/runs/, nothing accepted)"
  else
    echo "  6  run an addendum connected (Claude Code first; a candidate under staging/ai/runs/, nothing accepted)"
  fi
  if has_panel; then echo "  7  start the local panel"; else echo "  7  local panel (not in this version)"; fi
  echo "  8  run the offline checks (scripts/mac/checks.sh)"
  echo "  9  the smoke test (smoke-test/run_smoke.sh; synthetic, no model call)"
  echo "  m  switch connected / offline"
  echo "  q  quit"
  read -r -p "> " CH || exit 0
  case "$CH" in
    1) "$PY" -m tenderpack ingest; said $? "" ;;
    2) "$PY" -m tenderpack outputs --evidence build --out out; said $? "" ;;
    3) "$PY" -m tenderpack outputs --evidence build --out out --strict; said $? "human approvals pending (expected until a person approves)" ;;
    4) "$PY" -m tenderpack check-register; said $? "" ;;
    5) "$PY" -m tenderpack ai routes; said $? "" ;;
    6) read -r -p "addendum id (e.g. ADD-03): " ADD || exit 0
       read -r -p "path to its PDF: " PDFP || exit 0
       if [ ! -f "$PDFP" ]; then problem "no such file: $PDFP" "drag the addendum PDF from Finder into this window at the prompt (option 6 again)"; continue; fi
       if ! [[ "$ADD" =~ ^ADD-[0-9]{2}$ ]]; then problem "the addendum id must look like ADD-03 (got '$ADD')" "choose option 6 again"; continue; fi
       LR="$(live_run "$ADD")"
       if [ -n "$LR" ]; then
         IFS='|' read -r LRUN LROUTE LPID LSTATE LWHY <<<"$LR"
         if [ "$LSTATE" = "live" ]; then
           problem "a run on $ADD is already live: $LRUN ($LROUTE route, pid $LPID; $LWHY)" \
                   "$PY -m tenderpack ai run-status $LRUN   (follow it; start another only when it has finished)"
           continue
         fi
         echo "note: an earlier run on $ADD ($LRUN) left a stale lock ($LWHY); a new run takes it over if its process is gone, else see RECOVERY.md"
       fi
       if [ "$MODE" = "offline" ]; then
         "$PY" -m tenderpack ai run "$ADD" --pdf "$PDFP" --offline; said $? "refused"
       else
         read -r -p "route [host]: " RT || exit 0
         "$PY" -m tenderpack ai run "$ADD" --pdf "$PDFP" --route "${RT:-host}"; said $? "refused"
       fi ;;
    7) if ! has_panel; then echo "tenderpack panel is not in this version."; continue; fi
       PORT="${TENDERPACK_PANEL_PORT:-0}"
       if [ "$PORT" != "0" ] && ! "$PY" -c 'import socket, sys; s = socket.socket(); s.bind(("127.0.0.1", int(sys.argv[1])))' "$PORT" >/dev/null 2>&1; then
         problem "127.0.0.1:$PORT is already in use (probably a panel started earlier: its Terminal window shows its address)" \
                 "use that panel, or stop it with Ctrl-C in its window, or: TENDERPACK_PANEL_PORT=$((PORT+1)) bash \"$ROOT/scripts/mac/launch.command\""
         continue
       fi
       echo "the panel prints its address (127.0.0.1, a new token each start); Ctrl-C stops it"
       "$PY" -m tenderpack panel --open --port "$PORT"; RC=$?
       [ $RC -eq 0 ] || problem "the panel ended with exit $RC (see its message above)" "TENDERPACK_PANEL_PORT=0 bash \"$ROOT/scripts/mac/launch.command\"   (a free port)" ;;
    8) bash scripts/mac/checks.sh; said $? "" ;;
    9) if [ -x smoke-test/run_smoke.sh ] || [ -f smoke-test/run_smoke.sh ]; then bash smoke-test/run_smoke.sh; said $? ""
       else echo "no smoke-test/ in this folder (it is part of the interview folder)"; fi ;;
    m|M) if [ "$MODE" = "offline" ]; then MODE="connected"; else MODE="offline"; fi; set_mode; routes ;;
    q|Q) exit 0 ;;
    *) echo "choose 1-9, m or q" ;;
  esac
done
