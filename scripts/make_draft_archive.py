"""Build the DRAFT handover archive, organised around A1-A5, from the committed state.

Usage: python scripts/make_draft_archive.py DEST_DIR [--wheels WHEELHOUSE]

  LAMAR-PPP-R2-DRAFT_<sha>/
    00_README.md                      what is in the archive, its status, pending review, how to verify
    STATUS.md, checks.json            the outputs' own status page and checks (structural, reported, release blockers)
    A1_compliance_register/           a1.xlsx (Excel), a1.csv, a1.json
    A2_addendum_reconciliation/       a2.md and its tables
    A3_disqualification_sheet/        a3.pdf (one page) with a3_detail.html (each id on the page links to it), a3.json
    A4_work_log/                      the work log (worklog/README.md is the A4 index: every session, verbatim prompts,
                                      the subagent briefs, the error index, the model-call logs), the plan, session reports,
                                      repository.bundle (the git repository and its history; worklog/README.md says how to read it), HISTORY.md,
                                      clarification_register/ (draft questions, NOT SENT), review_records/ (the owner's
                                      reading approvals and their snapshots)
    A5_programme/                     programme, marshalling, documents, resources, drivers, scenarios, replan deltas
    REVIEW/                           the review batches (crops beside readings, exact decisions, commands)
    REHEARSALS/blind-0N/              the blind addendum rehearsals: comparison, timeline, frozen key, diff, A3
    OPERATING_GUIDE.md, COST_AND_EFFORT.md, VERIFY_ON_MAC.md
    SHA256SUMS
  and, with --wheels, the offline Python setup for a Mac, one zip per architecture, each also split into 15 MB parts
  with a .sha256 (LAMAR-PPP-R2-DRAFT_<sha>_wheels-macos-<arch>.zip[.partNN]); the parts travel where large files do
  not, and `cat X.zip.part* > X.zip` joins them (docs/VERIFY_ON_MAC.md step 3).

Refuses a dirty working tree, so the archive equals a commit. The zip is deterministic: sorted entries, fixed times.
"""
from __future__ import annotations

import hashlib
import json
import re
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


def rehearsals_to_include(repo: Path) -> list[Path]:
    """Every blind rehearsal folder that has a comparison (session 12: the list was hardcoded to blind-01..03)."""
    return sorted(p for p in (repo / "rehearsals").glob("blind-*") if (p / "COMPARISON.md").exists())


def readme(sha: str, date: str, checks: dict, items: dict, sessions: str) -> str:
    blockers = checks["release"]["blockers"]
    pend: dict[str, int] = {}
    for x in items["items"]:
        k = f"{x['kind']}:{x['status']}"
        pend[k] = pend.get(k, 0) + 1
    lines = [
        f"# LAMAR PPP AI Partner, Round 2: DRAFT handover ({sha}, {date})", "",
        "**Status: WORKING DRAFT, not a submission.** Everything in it is the assistant's proposal: the register rows, "
        "amendment ops, dispositions, lead times, capacities and the draft clarification questions (none sent). "
        "Recorded decisions are only the owner's own (see `REVIEW/items.csv` below); the program never approves or "
        "accepts anything. A strict release (`outputs --strict`) refuses these outputs until every row and op is decided.", "",
        "## Deliverables", "",
        "| | Folder | Open first |", "|---|---|---|",
        "| A1 | `A1_compliance_register/` | `a1.xlsx` (Excel; also CSV, JSON) |",
        "| A2 | `A2_addendum_reconciliation/` | `a2.md` |",
        "| A3 | `A3_disqualification_sheet/` | `a3.pdf` (one page); each id links to `a3_detail.html` |",
        f"| A4 | `A4_work_log/` | `worklog/` (sessions {sessions}), `repository.bundle` (`git clone A4_work_log/repository.bundle`), "
        "`clarification_register/clarification_register.md` (draft questions, not sent) |",
        "| A5 | `A5_programme/` | `gantt.pdf` / `gantt.html`, `programme.csv`, `marshalling.csv`, `resources.csv`, `README.md` |",
        "", "## What blocks a release now", ""]
    lines += [f"- **{b['kind']}**: {b['detail']}" for b in blockers]
    lines += ["", "## Your review", "",
              "Start at `REVIEW/index.html`: image readings, then disqualifiers, then amendment ops, then the STALE-row "
              "proposals, then the remaining rows. The full packets of the two image readings (Table 2-4 cells; the "
              "Arabic Form 4-C bands and numerals, native crops beside every reading) are in `REVIEW/packets/`. "
              "Each addendum's cover summary is compared with its provisions in A2 (C28: omissions and contradictions, "
              "report only; the summary is never applied). The status of every item is in `REVIEW/items.csv`:", ""]
    lines += [f"- {k}: {v}" for k, v in sorted(pend.items())]
    lines += ["", "## Also here", "",
              "- `REHEARSALS/blind-0N/COMPARISON.md`: independently written Addenda No. 3, each processed blind through "
              "the normal pipeline and scored against a key frozen before the start.",
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
    # session 12: every session report is copied (no hardcoded list), plus the named guides that exist
    docs_named = ["PLAN.md", "session-03_before-after.md", "AI_ROUTES.md", "COST_AND_EFFORT.md", "OPERATING_GUIDE.md",
                  "MAC_SETUP.md", "VERIFY_ON_MAC.md"]
    docs_reports = sorted(p.name for p in (REPO / "docs").glob("session-*_report.md"))
    for f in docs_named + docs_reports:
        if (REPO / "docs" / f).exists():
            shutil.copy(REPO / "docs" / f, a4 / "docs" / f)
    subprocess.run(["git", "bundle", "create", str(a4 / "repository.bundle"), "--all"], cwd=REPO, check=True, capture_output=True)
    (a4 / "HISTORY.md").write_text("# Repository history (git log)\n\n```\n" + git("log", "--format=%h %ad %s", "--date=iso-strict")
                                   + "\n```\n", encoding="utf-8")
    if (out / "a4").is_dir():
        copytree(out / "a4", a4 / "clarification_register")
    rr = a4 / "review_records"
    rr.mkdir()
    if (REPO / "curation/approvals.yaml").exists():
        shutil.copy(REPO / "curation/approvals.yaml", rr / "approvals.yaml")
        copytree(REPO / "curation/reading-snapshots", rr / "reading-snapshots")
    copytree(REPO / "curation/register/proposals", rr / "proposals")
    # session 12: every blind rehearsal with a comparison is included (the list was hardcoded to blind-01..03 before),
    # with its frozen-output records, post-key regression notes, clocks, diffs and candidate A3/A5 where they exist
    for src in rehearsals_to_include(REPO):
        rb = stage / "REHEARSALS" / src.name
        rb.mkdir(parents=True)
        files = ["README.md", "FROZEN.md", "FROZEN-OUTPUTS.md", "FROZEN-OUTPUTS.sha256", "COMPARISON.md", "run.id"]
        files += sorted(p.name for pat in ("REGRESSION*.md", "clock*.txt", "diff-*.md") for p in src.glob(pat))
        for f in files:
            if (src / f).exists():
                shutil.copy(src / f, rb / f)
        for d_ in ("SEALED", "input", "review"):
            if (src / d_).is_dir():
                copytree(src / d_, rb / d_)
        for sub, name_ in (("out-curated/a3", "out-curated-a3"), ("out-candidate/a3", "out-candidate-a3"),
                           ("out-candidate/a5", "out-candidate-a5")):
            if (src / sub).is_dir():
                copytree(src / sub, rb / name_)
        if (src / "out-candidate/README.md").exists():
            shutil.copy(src / "out-candidate/README.md", rb / "out-candidate-README.md")
    for f in ("OPERATING_GUIDE.md", "COST_AND_EFFORT.md", "VERIFY_ON_MAC.md"):
        shutil.copy(REPO / "docs" / f, stage / f)
    checks = json.loads((out / "checks.json").read_text(encoding="utf-8"))
    items = json.loads((out / "review/items.json").read_text(encoding="utf-8"))
    nums = sorted({m.group(1) for f in (REPO / "worklog").glob("*session-*") if (m := re.search(r"session-(\d+)", f.name))})
    (stage / "00_README.md").write_text(readme(sha, date, checks, items, f"{nums[0]}-{nums[-1]}"), encoding="utf-8")
    sums = [f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.relative_to(stage).as_posix()}"
            for f in sorted(p for p in stage.rglob("*") if p.is_file())]
    (stage / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
    zpath = dest / f"{name}.zip"
    write_zip(stage, zpath, stamp)
    print(f"archive: {zpath} ({zpath.stat().st_size / 1e6:.1f} MB, {len(sums)} files)")
    if wheels:
        req = Path(wheels) / "requirements.txt"
        for arch, tag in (("arm64", "macosx_11_0_arm64"), ("x86_64", "macosx_14_0_x86_64")):
            wstage = dest / f"{name}_wheels-macos-{arch}"
            if wstage.exists():
                shutil.rmtree(wstage)
            d = wstage / f"macos-{arch}"
            d.mkdir(parents=True)
            for f in sorted(Path(wheels).glob(f"{tag}-py*/*.whl")):
                shutil.copy(f, d / f.name)
            shutil.copy(req, wstage / "requirements.txt")
            (wstage / "INSTALL.txt").write_text(
                f"Offline Python setup for the tender-pack-reader repository on a Mac ({arch}); see VERIFY_ON_MAC.md step 3.\n"
                "python3 -m venv .venv\n"
                f".venv/bin/python -m pip install --no-index --find-links <this folder>/macos-{arch} -r <this folder>/requirements.txt\n"
                "Wheels for CPython 3.11, 3.12 and 3.13, from PyPI, pinned by uv.lock. "
                + ("Apple silicon: macOS 11 or later.\n" if arch == "arm64" else
                   "Intel: macOS 14 or later (on an older Intel Mac, set up with network once: uv sync --extra dev).\n"),
                encoding="utf-8")
            wz = dest / f"{wstage.name}.zip"
            write_zip(wstage, wz, stamp)
            for old in dest.glob(f"{wz.name}.part*"):
                old.unlink()
            data, size = wz.read_bytes(), 15 * 1024 * 1024
            parts = [data[i:i + size] for i in range(0, len(data), size)]
            for i, part in enumerate(parts, 1):
                (dest / f"{wz.name}.part{i:02d}").write_bytes(part)
            (dest / f"{wz.name}.sha256").write_text(f"{hashlib.sha256(data).hexdigest()}  {wz.name}\n", encoding="utf-8")
            print(f"wheelhouse {arch}: {wz} ({len(data) / 1e6:.1f} MB; {len(parts)} parts of at most 15 MiB + .sha256)")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    w = Path(args[args.index("--wheels") + 1]) if "--wheels" in args else None
    sys.exit(main(Path(args[0]), w))
