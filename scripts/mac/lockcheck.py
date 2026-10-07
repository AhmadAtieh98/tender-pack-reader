"""Compare the INSTALLED versions with requirements.lock.txt (session 13; scripts/mac/setup.sh and checks.sh).

Usage: <the venv's python> scripts/mac/lockcheck.py requirements.lock.txt

Standard library only. Each `name==version [; marker]` line whose marker applies to this interpreter (the markers
uv writes: python_full_version / python_version / sys_platform / platform_machine with ==, !=, <, <=, >, >=, joined
by `and` / `or`) must be installed at exactly that version. Prints one line per package and a verdict; exit 0 when
every applicable pin matches, 1 when any is missing or differs (the lines say which), 2 when the file is unreadable.
A marker it cannot read is reported and counted as a mismatch (never silently skipped)."""
from __future__ import annotations

import importlib.metadata as md
import platform
import re
import sys

LINE = re.compile(r"^([A-Za-z0-9._-]+)==([^\s;]+)\s*(?:;\s*(.+))?$")
CLAUSE = re.compile(r"^\s*(python_full_version|python_version|sys_platform|platform_machine)\s*(==|!=|<=|>=|<|>)\s*"
                    r"['\"]([^'\"]*)['\"]\s*$")


def _v(s: str) -> tuple:
    return tuple(int(x) if x.isdigit() else x for x in re.split(r"[.]", s))


def _env() -> dict:
    vi = sys.version_info
    return {"python_full_version": f"{vi.major}.{vi.minor}.{vi.micro}", "python_version": f"{vi.major}.{vi.minor}",
            "sys_platform": sys.platform, "platform_machine": platform.machine()}


def applies(marker: str | None, env: dict | None = None) -> bool:
    """True/False, or raises ValueError for a marker this checker cannot read."""
    if not marker:
        return True
    env = env or _env()
    ors = []
    for alt in re.split(r"\s+or\s+", marker.strip()):
        ok = True
        for clause in re.split(r"\s+and\s+", alt.strip().strip("()")):
            m = CLAUSE.match(clause.strip("() "))
            if not m:
                raise ValueError(f"unreadable marker {marker!r}")
            k, op, val = m.groups()
            a, b = (env[k], val) if k in ("sys_platform", "platform_machine") else (_v(env[k]), _v(val))
            ok &= {"==": a == b, "!=": a != b, "<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b}[op]
        ors.append(ok)
    return any(ors)


def main(path: str) -> int:
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except OSError as e:
        print(f"lockcheck: cannot read {path}: {e}")
        return 2
    bad = good = 0
    for ln in lines:
        m = LINE.match(ln.strip())
        if not m:
            continue
        name, want, marker = m.groups()
        try:
            if not applies(marker):
                continue
        except ValueError as e:
            print(f"MISMATCH {name}: {e}")
            bad += 1
            continue
        try:
            got = md.version(name)
        except md.PackageNotFoundError:
            print(f"MISMATCH {name}: not installed (the lock pins {want})")
            bad += 1
            continue
        if got != want:
            print(f"MISMATCH {name}: {got} installed, the lock pins {want}")
            bad += 1
        else:
            good += 1
    if bad:
        print(f"{bad} package(s) differ from {path} ({good} match): the environment is not the locked set")
        return 1
    print(f"all {good} applicable pins match the lock ({path}; python {platform.python_version()})")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
