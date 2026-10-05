#!/usr/bin/env bash
# tenderpack on the owner's Mac: one-time setup (session 12). Run from anywhere:   bash scripts/mac/setup.sh
#   --dry-run   only the read-only checks; nothing is created or installed
#
# What it does: finds python3 >= 3.11; creates .venv (uv when installed, else python3 -m venv); installs this project
# from pyproject.toml, from the local wheelhouse wheels/ when it holds wheels (no network), else from PyPI (the only
# network use, once); checks that pymupdf (pinned in pyproject.toml), openpyxl, pydantic, yaml and numpy import; checks
# that `ollama` is on PATH and lists the models ALREADY installed. It never downloads a model, never starts a hosted
# AI call and sends nothing anywhere. It ends with a PASS / PENDING / FAIL checklist.
set -u
cd "$(dirname "$0")/../.." || exit 2
ROOT="$(pwd)"
DRY=0
[ "${1:-}" = "--dry-run" ] && DRY=1
NPASS=0; NPEND=0; NFAIL=0
pass() { NPASS=$((NPASS+1)); echo "PASS     $*"; }
pend() { NPEND=$((NPEND+1)); echo "PENDING  $*"; }
fail() { NFAIL=$((NFAIL+1)); echo "FAIL     $*"; }
summary() {
  echo
  echo "setup checklist: ${NPASS} PASS, ${NPEND} PENDING, ${NFAIL} FAIL  (repository: ${ROOT})"
  if [ "$NFAIL" -eq 0 ]; then
    echo "next: bash scripts/mac/checks.sh   (the offline checks; turn Wi-Fi off first)"
    echo "      or double-click scripts/mac/launch.command"
  fi
}

echo "tenderpack setup ($( [ $DRY -eq 1 ] && echo 'dry run: nothing is created or installed' || echo 'installing' ))"

# 1. python >= 3.11 ------------------------------------------------------------------------------------------------
PY=""
for c in python3.13 python3.12 python3.11 python3; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
    PY="$(command -v "$c")"; break
  fi
done
if [ -n "$PY" ]; then pass "python >= 3.11: $PY ($("$PY" -V 2>&1))"
else fail "python >= 3.11 not found: install it (python.org, or Homebrew: brew install python@3.12) and run again"; summary; exit 1
fi

# 2. the pins in pyproject.toml ------------------------------------------------------------------------------------
PIN="$(sed -n 's/.*"pymupdf==\([0-9][0-9.]*\)".*/\1/p' pyproject.toml | head -1)"
if [ -n "$PIN" ]; then pass "pyproject.toml pins pymupdf==$PIN"; else fail "pyproject.toml has no pymupdf pin"; fi

# 3. the virtual environment ---------------------------------------------------------------------------------------
HAVE_UV=0; command -v uv >/dev/null 2>&1 && HAVE_UV=1
# a local wheelhouse: wheels/*.whl, or the draft archive's layout (docs/VERIFY_ON_MAC.md section 3: the joined and
# unzipped wheel parts, <dir>/macos-<arch>/ beside a requirements.txt), in the repository or next to it
WHEELS=0; WDIR=""; WREQ=""
ARCH="$(uname -m)"
for d in wheels wheels/*/macos-"$ARCH" ../wheels/*/macos-"$ARCH"; do
  if ls "$d"/*.whl >/dev/null 2>&1; then WHEELS=1; WDIR="$d"; break; fi
done
if [ $WHEELS -eq 1 ]; then
  for r in "$WDIR/requirements.txt" "$WDIR/../requirements.txt"; do [ -f "$r" ] && { WREQ="$r"; break; }; done
fi
deps_from_pyproject() {   # the [project] dependencies and the dev extra, exactly as pyproject.toml pins them
  "$PY" - <<'PYEOF'
import re, pathlib
t = pathlib.Path("pyproject.toml").read_text()
deps = re.search(r"dependencies = \[(.*?)\]", t, re.S).group(1)
dev = re.search(r"dev = \[(.*?)\]", t, re.S)
print("\n".join(re.findall(r'"([^"]+)"', deps + (dev.group(1) if dev else ""))))
PYEOF
}
if [ $DRY -eq 1 ]; then
  [ $HAVE_UV -eq 1 ] && pass "uv found ($(command -v uv)): the venv would be made with uv" \
                     || pass "uv not found: the venv would be made with $PY -m venv"
  [ $WHEELS -eq 1 ] && pass "local wheelhouse $WDIR: the install would use it only (no network)" \
                    || pend "no local wheelhouse (wheels/, or the archive's wheel parts): the install would use PyPI once (network)"
else
  if [ -x .venv/bin/python ] && .venv/bin/python -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
    pass "existing .venv kept ($(.venv/bin/python -V 2>&1))"
  elif [ $HAVE_UV -eq 1 ]; then
    uv venv --python "$PY" .venv >/dev/null && pass "venv created with uv" || { fail "uv venv failed"; summary; exit 1; }
  else
    "$PY" -m venv .venv && pass "venv created with $PY -m venv" || { fail "python -m venv failed"; summary; exit 1; }
  fi
  # 4. the project and its dependencies
  if [ $WHEELS -eq 1 ]; then
    # the dependencies only, from the wheelhouse; the project itself runs from the repository (python -m tenderpack)
    SRC="the local wheelhouse $WDIR (no network)"
    REQ="${WREQ:-$(mktemp)}"; [ -n "$WREQ" ] || deps_from_pyproject > "$REQ"
    if [ $HAVE_UV -eq 1 ]; then uv pip install --python .venv/bin/python --no-index --find-links "$WDIR" -r "$REQ"
    else .venv/bin/python -m pip install --no-index --find-links "$WDIR" -r "$REQ"; fi
  else
    SRC="PyPI (network, once)"
    if [ $HAVE_UV -eq 1 ]; then uv pip install --python .venv/bin/python -e ".[dev]"
    else .venv/bin/python -m pip install -e ".[dev]"; fi
  fi
  [ $? -eq 0 ] && pass "project installed from $SRC" || fail "the install from $SRC failed (see the messages above)"
fi

# 5. the imports and the pinned version ----------------------------------------------------------------------------
VPY=".venv/bin/python"; [ -x "$VPY" ] || VPY="$PY"
if [ $DRY -eq 1 ] && [ ! -x .venv/bin/python ]; then
  pend "imports (pymupdf, openpyxl, pydantic, yaml, numpy): checked after the install"
else
  if "$VPY" -c 'import pymupdf, openpyxl, pydantic, yaml, numpy' 2>/dev/null; then
    pass "pymupdf, openpyxl, pydantic, yaml, numpy import ($VPY)"
  else
    fail "an import failed: $VPY -c 'import pymupdf, openpyxl, pydantic, yaml, numpy'"
  fi
  GOT="$("$VPY" -c 'import importlib.metadata as m; print(m.version("pymupdf"))' 2>/dev/null)"
  if [ -n "$PIN" ] && [ "$GOT" = "$PIN" ]; then pass "pymupdf $GOT matches the pin"
  elif [ -n "$GOT" ]; then fail "pymupdf $GOT installed, pyproject.toml pins $PIN"
  else pend "pymupdf version not readable yet"; fi
fi

# 6. local AI: ollama (optional; the deterministic build and exports do not need it) -------------------------------
if command -v ollama >/dev/null 2>&1; then
  pass "ollama on PATH: $(command -v ollama)"
  if MODELS="$(ollama list 2>/dev/null)"; then
    pass "ollama answers locally; installed models (nothing is downloaded by this script):"
    echo "$MODELS" | sed 's/^/           /'
  else
    pend "ollama is installed but not running: start the Ollama app (or 'ollama serve'), then run checks.sh"
  fi
else
  pend "ollama not on PATH: local AI is unavailable (the build, the exports and the checks still work without it)"
fi
echo "         models are never pulled here; config/ai.yaml routes.ollama.models names the ones tenderpack will use"
echo "         (tenderpack ai routes --offline shows each one's checked capabilities and memory estimate)"

summary
[ "$NFAIL" -eq 0 ]
