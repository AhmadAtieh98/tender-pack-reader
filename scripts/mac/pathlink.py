#!/usr/bin/env python3
"""Link THIS folder into its .venv so `python -m tenderpack` imports the folder's package from ANY working directory
(session 13, E159). The folder's .venv installs only the locked dependencies, never the project: the package is
importable only when the working directory is the folder. The host route's MCP server is started by the host CLI in
the session folder (the CLI ignores the server config's cwd), so a reading session there found "No module named
tenderpack", had no tools, and the model wrote tool-call markup as text. A .pth file in the venv's site-packages adds
the folder to sys.path for every interpreter start; this script writes it, then verifies from OUTSIDE the folder
that `import tenderpack` resolves to this folder's package.

    .venv/bin/python scripts/mac/pathlink.py --root <folder> [--site-dir <site-packages>] [--python <interpreter>]

Exit 0 when the import from outside resolves to <folder>/tenderpack; 1 with the mismatch otherwise. Nothing else is
written. Idempotent: the .pth is rewritten, never appended."""
from __future__ import annotations

import argparse
import subprocess
import sys
import sysconfig
import tempfile
from pathlib import Path

NAME = "tenderpack-folder.pth"


def write_pth(root: Path, site_dir: Path) -> Path:
    site_dir.mkdir(parents=True, exist_ok=True)
    f = site_dir / NAME
    f.write_text(str(root.resolve()) + "\n", encoding="utf-8")
    return f


def verify(python: str, root: Path) -> tuple[bool, str]:
    """Run `python -c 'import tenderpack'` in a neutral working directory; True when the package found is the
    folder's (its __init__.py under root/tenderpack). The interpreter's own environment is used unchanged."""
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([python, "-P", "-c", "import tenderpack, sys; print(tenderpack.__file__)"], cwd=d,
                           capture_output=True, text=True)
    if r.returncode != 0:
        return False, (r.stderr or r.stdout).strip().splitlines()[-1] if (r.stderr or r.stdout).strip() else "no output"
    got = Path(r.stdout.strip()).resolve()
    want = (root.resolve() / "tenderpack" / "__init__.py")
    return got == want, str(got)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True, help="the tenderpack folder (holds tenderpack/, pyproject.toml)")
    ap.add_argument("--site-dir", default=None, help="site-packages to write the .pth into (default: this "
                                                      "interpreter's purelib)")
    ap.add_argument("--python", default=sys.executable, help="the interpreter to verify with (default: this one)")
    ap.add_argument("--verify-only", action="store_true",
                    help="session 14 (W6): write nothing, only verify (checks.sh with TENDERPACK_PY: an interpreter "
                         "that is not this folder's .venv is never changed)")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve()
    if not (root / "tenderpack" / "__init__.py").is_file():
        print(f"FAIL     {root} has no tenderpack/__init__.py: not a tenderpack folder", file=sys.stderr)
        return 1
    site = Path(a.site_dir) if a.site_dir else Path(sysconfig.get_paths()["purelib"])
    f = site / NAME if a.verify_only else write_pth(root, site)
    ok, what = verify(a.python, root)
    if ok:
        print(f"PASS     tenderpack imports from {root} wherever the interpreter starts ({f})")
        return 0
    print(f"FAIL     outside the folder, {a.python} imports tenderpack from {what}, not from {root} ({f} "
          f"{'not written: --verify-only' if a.verify_only else 'written'})",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
