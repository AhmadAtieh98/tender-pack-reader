#!/usr/bin/env bash
# tenderpack on the owner's Mac: one-time setup (session 12; session 13: the LOCKED set). Run from anywhere:
#   bash scripts/mac/setup.sh             build .venv in THIS folder from the lock
#   bash scripts/mac/setup.sh --dry-run   only the read-only checks; nothing is created or installed
#
# What it does: finds python3 >= 3.11; builds .venv HERE (a virtual environment is not portable: one copied from
# another folder or machine is refused with the command that rebuilds it); installs EXACTLY the locked dependency set
# and never resolves afresh from pyproject.toml:
#   a local wheelhouse (wheels/, or the archive's wheel parts)  ->  pip/uv pip --no-index -r requirements.lock.txt
#   uv on PATH                                                  ->  uv sync --frozen --extra dev --no-install-project
#   neither                                                     ->  python3 -m venv + pip install -r requirements.lock.txt
# (requirements.lock.txt is exported from uv.lock; tests check they agree). The project itself is not installed: it
# runs from this folder (python -m tenderpack), which a .pth file links into .venv so the import works from any working
# directory (scripts/mac/pathlink.py; session 13, E159). It then compares every installed version with the lock
# (scripts/mac/lockcheck.py), checks the imports and lists the Ollama models ALREADY installed. It never downloads a
# model, never starts a hosted AI call and sends nothing anywhere; the only network use is the package download when
# there is no wheelhouse and the uv cache does not hold the wheels. It ends with a PASS / PENDING / FAIL checklist.
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
  echo "setup checklist: ${NPASS} PASS, ${NPEND} PENDING, ${NFAIL} FAIL  (folder: ${ROOT})"
  if [ "$NFAIL" -eq 0 ]; then
    echo "next: bash \"$ROOT/scripts/mac/checks.sh\"   (the offline checks; turn Wi-Fi off first)"
    echo "      or double-click scripts/mac/launch.command"
  fi
}
REBUILD="rm -rf \"$ROOT/.venv\" && bash \"$ROOT/scripts/mac/setup.sh\""

echo "tenderpack setup ($( [ $DRY -eq 1 ] && echo 'dry run: nothing is created or installed' || echo 'installing the locked set' ))"

# 1. python >= 3.11 ------------------------------------------------------------------------------------------------
PY=""
# TENDERPACK_SETUP_PYTHON: the interpreter(s) to try instead (e.g. python3.12, or a full path), in this order
for c in ${TENDERPACK_SETUP_PYTHON:-python3.13 python3.12 python3.11 python3}; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
    PY="$(command -v "$c")"; break
  fi
done
if [ -n "$PY" ]; then pass "python >= 3.11: $PY ($("$PY" -V 2>&1))"
else fail "python >= 3.11 not found: install it (python.org, or Homebrew: brew install python@3.12) and run again"; summary; exit 1
fi

# 2. the pins and the lock -----------------------------------------------------------------------------------------
PIN="$(sed -n 's/.*"pymupdf==\([0-9][0-9.]*\)".*/\1/p' pyproject.toml | head -1)"
if [ -n "$PIN" ]; then pass "pyproject.toml pins pymupdf==$PIN"; else fail "pyproject.toml has no pymupdf pin"; fi
LOCK="requirements.lock.txt"
if [ -f uv.lock ] && [ -f "$LOCK" ]; then
  LPIN="$(sed -n 's/^pymupdf==\([0-9][0-9.]*\).*/\1/p' "$LOCK" | head -1)"
  if [ "$LPIN" = "$PIN" ]; then pass "uv.lock and $LOCK present ($LOCK pins pymupdf==$LPIN)"
  else fail "$LOCK pins pymupdf==$LPIN but pyproject.toml pins $PIN: the lock is out of date (uv lock; uv export ...)"; fi
else
  fail "uv.lock or $LOCK is missing in $ROOT: this folder is incomplete (unzip it again)"; summary; exit 1
fi

# 3. an existing .venv must have been built HERE -------------------------------------------------------------------
venv_problem() {   # prints why the existing .venv cannot be used, or nothing
  [ -e .venv ] || return 0
  if [ ! -x .venv/bin/python ] || ! .venv/bin/python -c 'import sys' >/dev/null 2>&1; then
    echo ".venv/bin/python does not run (its base interpreter $(sed -n 's/^home = //p' .venv/pyvenv.cfg 2>/dev/null) was moved or removed, or the .venv was copied from another machine)"; return 0
  fi
  local built=""
  [ -f .venv/bin/activate ] && built="$(sed -n "s/^ *VIRTUAL_ENV=[\"']\{0,1\}\([^\"']*\)[\"']\{0,1\} *$/\1/p" .venv/bin/activate | head -1)"
  if [ -n "$built" ] && [ "$built" != "$ROOT/.venv" ]; then
    echo ".venv was built in another folder ($built); a copied virtual environment is not portable"; return 0
  fi
  .venv/bin/python -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null \
    || echo ".venv runs $(.venv/bin/python -V 2>&1), older than 3.11"
}
VP="$(venv_problem)"
if [ -n "$VP" ]; then
  fail "$VP"
  echo "         next: $REBUILD"
  summary; exit 1
fi

# 4. the locked install --------------------------------------------------------------------------------------------
HAVE_UV=0; command -v uv >/dev/null 2>&1 && HAVE_UV=1
# a local wheelhouse: wheels/*.whl, or the draft archive's layout (docs/VERIFY_ON_MAC.md section 3: the joined and
# unzipped wheel parts, <dir>/macos-<arch>/), in the folder or next to it
WHEELS=0; WDIR=""
ARCH="$(uname -m)"
for d in wheels wheels/*/macos-"$ARCH" ../wheels/*/macos-"$ARCH"; do
  if ls "$d"/*.whl >/dev/null 2>&1; then WHEELS=1; WDIR="$d"; break; fi
done
if [ $DRY -eq 1 ]; then
  if [ $WHEELS -eq 1 ]; then pass "local wheelhouse $WDIR: the install would use it only (no network): -r $LOCK --no-index"
  elif [ $HAVE_UV -eq 1 ]; then pass "uv found ($(command -v uv)): the install would be uv sync --frozen --extra dev --no-install-project (uv.lock)"
  else pass "uv not found: the install would be $PY -m venv .venv, then pip install -r $LOCK"; fi
  [ $WHEELS -eq 1 ] || pend "no local wheelhouse: the install downloads the locked wheels once (network) unless uv's cache holds them"
else
  if [ $WHEELS -eq 1 ]; then
    SRC="the local wheelhouse $WDIR (no network)"
    if [ ! -x .venv/bin/python ]; then
      if [ $HAVE_UV -eq 1 ]; then uv venv --python "$PY" .venv >/dev/null || { fail "uv venv failed"; summary; exit 1; }
      else "$PY" -m venv .venv || { fail "$PY -m venv failed"; summary; exit 1; }; fi
    fi
    if [ $HAVE_UV -eq 1 ]; then
      echo "         uv pip install --python .venv/bin/python --no-index --find-links $WDIR -r $LOCK"
      uv pip install --python .venv/bin/python --no-index --find-links "$WDIR" -r "$LOCK"; RC=$?
    else
      echo "         .venv/bin/python -m pip install --no-index --find-links $WDIR -r $LOCK"
      .venv/bin/python -m pip install --no-index --find-links "$WDIR" -r "$LOCK"; RC=$?
    fi
  elif [ $HAVE_UV -eq 1 ]; then
    SRC="uv.lock (uv sync --frozen; the uv cache, else PyPI once)"
    echo "         uv sync --frozen --extra dev --no-install-project --python $PY"
    uv sync --frozen --extra dev --no-install-project --python "$PY"; RC=$?
    if [ $RC -ne 0 ] && [ -x .venv/bin/python ]; then
      # the same locked set by another door: uv's cache may hold the wheels under the index rather than the lock's
      # file URLs (e.g. offline, after earlier `uv pip` installs); exact pins, so nothing is resolved afresh
      echo "         uv sync --frozen ended with exit $RC; the same locked set with: uv pip install -r $LOCK"
      SRC="$LOCK (uv pip install; the uv cache, else PyPI once)"
      uv pip install --python .venv/bin/python -r "$LOCK"; RC=$?
    fi
  else
    SRC="$LOCK (pip; PyPI once)"
    if [ ! -x .venv/bin/python ]; then "$PY" -m venv .venv || { fail "$PY -m venv failed"; summary; exit 1; }; fi
    echo "         .venv/bin/python -m pip install -r $LOCK"
    .venv/bin/python -m pip install -r "$LOCK"; RC=$?
  fi
  if [ $RC -eq 0 ]; then pass "locked set installed from $SRC"
  else fail "the install from $SRC ended with exit $RC (see the messages above); nothing was resolved from pyproject.toml"; fi
fi

# 5. the installed versions against the lock, the imports and the pinned version ------------------------------------
if [ $DRY -eq 1 ] && [ ! -x .venv/bin/python ]; then
  pend "installed versions and imports: checked after the install"
else
  VPY=".venv/bin/python"
  if [ ! -x "$VPY" ]; then fail "no .venv/bin/python after the install"; summary; exit 1; fi
  LC="$("$VPY" scripts/mac/lockcheck.py "$LOCK" 2>&1)"; RC=$?
  if [ $RC -eq 0 ]; then pass "installed versions match $LOCK ($(echo "$LC" | tail -1))"
  else
    fail "installed versions differ from $LOCK (lockcheck exit $RC):"
    echo "$LC" | sed 's/^/           /'
    echo "         next: $REBUILD"
  fi
  if "$VPY" -c 'import pymupdf, openpyxl, pydantic, yaml, numpy' 2>/dev/null; then
    pass "pymupdf, openpyxl, pydantic, yaml, numpy import ($VPY)"
  else
    fail "an import failed: $VPY -c 'import pymupdf, openpyxl, pydantic, yaml, numpy'"
  fi
  GOT="$("$VPY" -c 'import importlib.metadata as m; print(m.version("pymupdf"))' 2>/dev/null)"
  if [ -n "$PIN" ] && [ "$GOT" = "$PIN" ]; then pass "pymupdf $GOT matches the pin"
  elif [ -n "$GOT" ]; then fail "pymupdf $GOT installed, pyproject.toml pins $PIN"
  else pend "pymupdf version not readable yet"; fi
  # 5b. (session 13, E159) link THIS folder into .venv (a .pth file) so `python -m tenderpack` imports the folder's
  # package from any working directory: the host route's MCP server is started in the session folder, not here
  if [ $DRY -eq 1 ]; then
    pend "the folder link into .venv (scripts/mac/pathlink.py) is written after the install"
  elif LK="$("$VPY" scripts/mac/pathlink.py --root "$ROOT" 2>&1)"; then pass "${LK#PASS     }"
  else fail "${LK#FAIL     }"; echo "         next: $REBUILD"; fi
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
echo "         models are never pulled here; .venv/bin/python -m tenderpack ai ollama-models shows which installed"
echo "         model can serve each phase (capabilities, context, memory; nothing downloaded)"

summary
[ "$NFAIL" -eq 0 ]
