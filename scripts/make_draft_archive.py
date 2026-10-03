"""Build the DRAFT handover archive, organised around A1-A5, from the committed state.

Usage: python scripts/make_draft_archive.py DEST_DIR [--wheels WHEELHOUSE]

  LAMAR-PPP-R2-DRAFT_<sha>/
    00_README.md                      what is in the archive, its status, pending review, how to verify
    STATUS.md, checks.json            the outputs' own status page and checks (structural, reported, release blockers)
    A1_compliance_register/           a1.xlsx (Excel), a1.csv, a1.json
    A2_addendum_reconciliation/       a2.md and its tables
    A3_disqualification_sheet/        a3.pdf (one page) with a3_detail.html (each id on the page links to it), a3.json
    A4_work_log/                      the work log (every session, verbatim exchanges, errors), the plan, session reports,
                                      repository.bundle (the git repository with its real history), HISTORY.md
    A5_programme/                     programme, marshalling, documents, resources, drivers, scenarios, replan deltas
    REVIEW/                           the review batches (crops beside readings, exact decisions, commands)
    REHEARSALS/blind-01/              the blind addendum rehearsal: comparison, timeline, frozen key, diff, A3
    OPERATING_GUIDE.md, COST_AND_EFFORT.md, VERIFY_ON_MAC.md
    SHA256SUMS
  and, with --wheels, LAMAR-PPP-R2-DRAFT_<sha>_wheels-macos.zip (offline Python setup for Apple silicon and Intel).

Refuses a dirty working tree, so the archive equals a commit. The zip is deterministic: sorted entries, fixed times.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO, check=True, capture_output=True, text=True).stdout.strip()


def copytree(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", ".tenderpack-build"))


def write_zip(folder: Path, dest: Path, stamp: tuple) -> None:
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted(p for p in folder.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(f"{folder.name}/{f.relative_to(folder).as_posix()}", date_time=stamp)
            info.compress_type, info.external_attr = zipfile.ZIP_DEFLATED, 0o644 << 16
            z.writestr(info, f.read_bytes())


def readme(sha: str, date: str, checks: dict, items: dict) -> str:
    blockers = checks["release"]["blockers"]
    pend: dict[str, int] = {}
    for x in items["items"]:
        k = f"{x['kind']}:{x['status']}"
        pend[k] = pend.get(k, 0) + 1
    lines = [
        f"# LAMAR PPP AI Partner, Round 2: DRAFT handover ({sha}, {date})", "",
        "**Status: WORKING DRAFT, not a submission.** Everything in it is the assistant's proposal: the register rows, "
        "amendment ops, dispositions, lead times and capacities. **Pending your review:** the two image readings, and "
        "every row and op. The program never approves or accepts anything. A strict release (`outputs --strict`) "
        "refuses these outputs until you have decided.", "",
        "## Deliverables", "",
        "| | Folder | Open first |", "|---|---|---|",
        "| A1 | `A1_compliance_register/` | `a1.xlsx` (Excel; also CSV, JSON) |",
        "| A2 | `A2_addendum_reconciliation/` | `a2.md` |",
        "| A3 | `A3_disqualification_sheet/` | `a3.pdf` (one page); each id links to `a3_detail.html` |",
        "| A4 | `A4_work_log/` | `worklog/` (sessions 01-06), `repository.bundle` (`git clone A4_work_log/repository.bundle`) |",
        "| A5 | `A5_programme/` | `programme.csv`, `marshalling.csv`, `drivers.csv`, `scenario_comparison.csv` |",
        "", "## What blocks a release now", ""]
    lines += [f"- **{b['kind']}**: {b['detail']}" for b in blockers]
    lines += ["", "## Your review", "",
              "Start at `REVIEW/index.html`: image readings, then disqualifiers, then amendment ops, then the STALE-row "
              "proposals, then the remaining rows. The status of every item is in `REVIEW/items.csv`:", ""]
    lines += [f"- {k}: {v}" for k, v in sorted(pend.items())]
    lines += ["", "## Also here", "",
              "- `REHEARSALS/blind-01/COMPARISON.md`: an independently written Addendum No. 3, processed blind and scored "
              "against a key frozen before the start.",
              "- `OPERATING_GUIDE.md`: setup, the live-addendum procedure, review commands, what each check means.",
              "- `COST_AND_EFFORT.md`: time, agents, what is not known.",
              "- `VERIFY_ON_MAC.md`: exact commands to check the archive and rebuild offline on a Mac.",
              "- `SHA256SUMS`: every file (`shasum -a 256 -c SHA256SUMS`).", ""]
    return "\n".join(lines)


def main(dest: Path, wheels: Path | None) -> int:
    if git("status", "--porcelain"):
        print("refused: the working tree has uncommitted changes; commit first so the archive equals a commit")
        return 2
    sha, date = git("rev-parse", "--short", "HEAD"), git("log", "-1", "--format=%cd", "--date=format:%Y-%m-%d")
    y, m, d = map(int, date.split("-"))
    stamp = (y, m, d, 0, 0, 0)
    name = f"LAMAR-PPP-R2-DRAFT_{sha}"
    dest = Path(dest).resolve()
    stage = dest / name
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    out = REPO / "out"
    copytree(out / "a1", stage / "A1_compliance_register")
    copytree(out / "a2", stage / "A2_addendum_reconciliation")
    copytree(out / "a3", stage / "A3_disqualification_sheet")
    copytree(out / "a5", stage / "A5_programme")
    copytree(out / "review", stage / "REVIEW")
    shutil.copy(out / "README.md", stage / "STATUS.md")
    shutil.copy(out / "checks.json", stage / "checks.json")
    a4 = stage / "A4_work_log"
    copytree(REPO / "worklog", a4 / "worklog")
    (a4 / "docs").mkdir()
    for f in ("PLAN.md", "session-03_before-after.md", "session-04_report.md", "session-05_report.md", "session-06_report.md"):
        if (REPO / "docs" / f).exists():
            shutil.copy(REPO / "docs" / f, a4 / "docs" / f)
    subprocess.run(["git", "bundle", "create", str(a4 / "repository.bundle"), "--all"], cwd=REPO, check=True, capture_output=True)
    (a4 / "HISTORY.md").write_text("# Repository history (git log)\n\n```\n" + git("log", "--format=%h %ad %s", "--date=iso-strict")
                                   + "\n```\n", encoding="utf-8")
    rb = stage / "REHEARSALS" / "blind-01"
    rb.mkdir(parents=True)
    for f in ("README.md", "FROZEN.md", "COMPARISON.md", "clock.txt", "diff-ADD-02-to-ADD-03.md"):
        shutil.copy(REPO / "rehearsals/blind-01" / f, rb / f)
    copytree(REPO / "rehearsals/blind-01/SEALED", rb / "SEALED")
    copytree(REPO / "rehearsals/blind-01/input", rb / "input")
    copytree(REPO / "rehearsals/blind-01/out-curated/a3", rb / "out-curated-a3")
    for f in ("OPERATING_GUIDE.md", "COST_AND_EFFORT.md", "VERIFY_ON_MAC.md"):
        shutil.copy(REPO / "docs" / f, stage / f)
    checks = json.loads((out / "checks.json").read_text(encoding="utf-8"))
    items = json.loads((out / "review/items.json").read_text(encoding="utf-8"))
    (stage / "00_README.md").write_text(readme(sha, date, checks, items), encoding="utf-8")
    sums = [f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.relative_to(stage).as_posix()}"
            for f in sorted(p for p in stage.rglob("*") if p.is_file())]
    (stage / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
    zpath = dest / f"{name}.zip"
    write_zip(stage, zpath, stamp)
    print(f"archive: {zpath} ({zpath.stat().st_size / 1e6:.1f} MB, {len(sums)} files)")
    if wheels:
        wstage = dest / f"{name}_wheels-macos"
        if wstage.exists():
            shutil.rmtree(wstage)
        for arch, tag in (("arm64", "macosx_11_0_arm64"), ("x86_64", "macosx_14_0_x86_64")):
            d = wstage / f"macos-{arch}"
            d.mkdir(parents=True)
            for f in sorted(Path(wheels).glob(f"{tag}-py*/*.whl")):
                shutil.copy(f, d / f.name)
        shutil.copy(Path(wheels) / "requirements.txt", wstage / "requirements.txt")
        (wstage / "INSTALL.txt").write_text(
            "Offline Python setup for the tender-pack-reader repository (see VERIFY_ON_MAC.md section 3, option B).\n"
            "python3 -m venv .venv\n"
            ".venv/bin/python -m pip install --no-index --find-links <this folder>/macos-$(uname -m) -r <this folder>/requirements.txt\n"
            "Wheels for CPython 3.11, 3.12 and 3.13, from PyPI, pinned by uv.lock. Apple silicon: macOS 11 or later;\n"
            "Intel: macOS 14 or later (on an older Intel Mac, set up with network once: uv sync --extra dev).\n", encoding="utf-8")
        wz = dest / f"{wstage.name}.zip"
        write_zip(wstage, wz, stamp)
        print(f"wheelhouse: {wz} ({wz.stat().st_size / 1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    w = Path(args[args.index("--wheels") + 1]) if "--wheels" in args else None
    sys.exit(main(Path(args[0]), w))
