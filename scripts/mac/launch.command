#!/usr/bin/env bash
# tenderpack launcher for the Mac (session 12): double-click it in Finder (or run it in Terminal). It uses the .venv
# made by scripts/mac/setup.sh, works without internet or an API key, and calls no hosted service: AI steps run in
# offline mode (local Ollama only).
cd "$(dirname "$0")/../.." || exit 1
ROOT="$(pwd)"
if [ ! -x .venv/bin/python ]; then
  echo "No .venv yet: run   bash scripts/mac/setup.sh   first."; read -r -p "Press Return to close." _; exit 1
fi
# shellcheck disable=SC1091
source .venv/bin/activate
export TENDERPACK_OFFLINE=1
PY="$ROOT/.venv/bin/python"
has_panel() { "$PY" -m tenderpack panel --help >/dev/null 2>&1; }
while true; do
  echo
  echo "tenderpack ($ROOT) - offline"
  echo "  1  rebuild the evidence (ingest the PDFs into build/)"
  echo "  2  build the outputs A1-A5 into out/"
  echo "  3  strict check (the release check; exit 3 while approvals are pending)"
  echo "  4  check the register (check-register)"
  echo "  5  AI routes and local model capabilities (Ollama; nothing downloaded)"
  echo "  6  run an addendum offline (local Ollama; a candidate under staging/ai/runs/, nothing accepted)"
  if has_panel; then echo "  7  start the local panel"; else echo "  7  local panel (not in this version yet)"; fi
  echo "  8  run the offline checks (scripts/mac/checks.sh)"
  echo "  q  quit"
  read -r -p "> " CH
  case "$CH" in
    1) "$PY" -m tenderpack ingest ;;
    2) "$PY" -m tenderpack outputs --evidence build --out out ;;
    3) "$PY" -m tenderpack outputs --evidence build --out out --strict; echo "(exit $?: 3 means human approvals pending)" ;;
    4) "$PY" -m tenderpack check-register ;;
    5) "$PY" -m tenderpack ai routes --offline ;;
    6) read -r -p "addendum id (e.g. ADD-03): " ADD
       read -r -p "path to its PDF: " PDFP
       [ -f "$PDFP" ] && "$PY" -m tenderpack ai run "$ADD" --pdf "$PDFP" --offline || echo "no such file: $PDFP" ;;
    7) if has_panel; then "$PY" -m tenderpack panel; else echo "tenderpack panel is not in this version yet."; fi ;;
    8) bash scripts/mac/checks.sh ;;
    q|Q) exit 0 ;;
    *) echo "choose 1-8 or q" ;;
  esac
done
