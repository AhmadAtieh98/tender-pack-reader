"""Build a labelled WORKING-TREE SNAPSHOT for review: the tree as it is, uncommitted changes included and disclosed.

Usage: python scripts/make_snapshot.py DEST_DIR [--label TEXT] [--exclude PREFIX ...]

This is NOT the release archive. `scripts/make_draft_archive.py` refuses a dirty tree so that an archive equals a
commit; that safeguard stays. A snapshot is for reviewing work that is deliberately uncommitted (the owner decides
what is committed): it is named after the base revision plus a timestamp, carries the disclosure of every uncommitted
and untracked path, the diff statistics, and a manifest of every file it holds.

  LAMAR-PPP-R2-SNAPSHOT_<base-sha>+wt_<UTC stamp>/
    SNAPSHOT.md                       base revision, branch, label, the uncommitted-change disclosure (git status),
                                      diff statistics, counts, the dependency pins of the packaged pyproject
    uncommitted.patch                 `git diff HEAD` (tracked files only; untracked files are in the tree itself)
    MANIFEST.sha256                   sha256 of every file in the snapshot (`shasum -a 256 -c MANIFEST.sha256`)
    <the working tree>                every tracked file that still exists and every untracked file that is not
                                      ignored (what `git add -A` would capture), minus `--exclude` prefixes

Runnable: unzip, `make setup` (or `scripts/mac/setup.sh`), then the commands of docs/OPERATING_GUIDE.md.
Deterministic for a given tree and stamp: sorted entries, fixed times.
"""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_EXCLUDES = ("staging/ai/runs/_cache/",)


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout


def tree_files(repo: Path, excludes: tuple[str, ...]) -> list[str]:
    """Every path a commit of the tree would hold: tracked files that still exist plus untracked, not-ignored files."""
    tracked = git(repo, "ls-files", "-z").split("\0")
    untracked = git(repo, "ls-files", "-z", "--others", "--exclude-standard").split("\0")
    deleted = set(git(repo, "ls-files", "-z", "--deleted").split("\0"))
    paths = {p for p in tracked + untracked if p and p not in deleted}
    return sorted(p for p in paths if not any(p.startswith(x) for x in excludes))


def zip_mode(name: str, src: Path | None = None) -> int:
    """The entry's external_attr: a regular file, 0755 for a launcher or a shell script (*.command, *.sh) or a file
    executable on disk, else 0644. Session 13: every entry was written 0644, so the unzipped launch.command and setup.sh
    lost their executable bit and Finder would not run the launcher."""
    exe = name.endswith((".command", ".sh")) or bool(src is not None and src.stat().st_mode & 0o100)
    return (0o100000 | (0o755 if exe else 0o644)) << 16


def write_zip(folder: Path, dest: Path, stamp: tuple) -> None:
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for f in sorted(p for p in folder.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(f"{folder.name}/{f.relative_to(folder).as_posix()}", date_time=stamp)
            info.compress_type, info.external_attr = zipfile.ZIP_DEFLATED, zip_mode(f.name, f)
            info.create_system = 3                     # Unix: unzip and Finder apply the mode bits
            z.writestr(info, f.read_bytes())


def snapshot_md(repo: Path, name: str, base: str, branch: str, label: str, status: str, diffstat: str,
                files: list[str], when: str) -> str:
    changed = [l for l in status.splitlines() if l.strip()]
    untracked = [l for l in changed if l.startswith("??")]
    pyproject = (repo / "pyproject.toml").read_text(encoding="utf-8") if (repo / "pyproject.toml").exists() else ""
    deps = [l.strip() for l in pyproject.splitlines() if l.strip().startswith('"') and "==" in l or ">=" in l]
    lines = [f"# {name}", "",
             "**WORKING-TREE SNAPSHOT for review: not a release archive, not a commit, not a submission.** Everything "
             "in it is the assistant's proposal unless a recorded decision of the owner says otherwise; nothing is "
             "accepted, approved or sent. The release archive (`scripts/make_draft_archive.py`) is built only from a "
             "clean commit; this snapshot exists because the owner asked that work stay uncommitted until authorised.", "",
             f"- Base revision: `{base}` on branch `{branch}`",
             f"- Taken: {when} (UTC)",
             f"- Label: {label or '(none)'}",
             f"- Files in the snapshot: {len(files)}",
             f"- Paths that differ from the base revision: {len(changed)} ({len(untracked)} untracked)", "",
             "## Uncommitted-change disclosure (`git status --short` against the base revision)", "", "```",
             status.rstrip() or "(clean: the snapshot equals the base revision)", "```", "",
             "## Diff statistics against the base revision (tracked files; `uncommitted.patch` holds the diff)", "",
             "```", diffstat.rstrip() or "(no tracked file differs)", "```", "",
             "## Dependency pins of the packaged `pyproject.toml`", "", "```"] + (deps or ["(none found)"]) + ["```", "",
             "## How to run it", "",
             "1. Unzip; `cd` into the folder.",
             "2. `make setup` (needs network once) or `scripts/mac/setup.sh` when present (offline with a wheelhouse).",
             "3. `.venv/bin/python -m tenderpack ingest`, then `… outputs --evidence build --out out` and the checks in "
             "`docs/OPERATING_GUIDE.md`. The outputs in `out/` are the ones the snapshot was taken with; a rebuild must "
             "reproduce them (`diff -r`) except for timestamps the guide names.",
             "4. `shasum -a 256 -c MANIFEST.sha256` verifies every file.", ""]
    return "\n".join(lines)


def main(dest: Path, label: str = "", excludes: tuple[str, ...] = DEFAULT_EXCLUDES, repo: Path = REPO,
         now: datetime | None = None) -> int:
    now = now or datetime.now(timezone.utc)
    base = git(repo, "rev-parse", "--short", "HEAD").strip()
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
    status = git(repo, "status", "--short")
    diffstat = git(repo, "diff", "--stat", "HEAD")
    patch = git(repo, "diff", "HEAD")
    files = tree_files(repo, excludes)
    stamp_s = now.strftime("%Y%m%dT%H%MZ")
    name = f"LAMAR-PPP-R2-SNAPSHOT_{base}+wt_{stamp_s}"
    dest = Path(dest).resolve()
    stage = dest / name
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    for rel in files:
        src = repo / rel
        if not src.is_file():
            continue
        dst = stage / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    (stage / "uncommitted.patch").write_text(patch, encoding="utf-8")
    (stage / "SNAPSHOT.md").write_text(
        snapshot_md(repo, name, base, branch, label, status, diffstat, files, now.strftime("%Y-%m-%d %H:%M")),
        encoding="utf-8")
    sums = [f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.relative_to(stage).as_posix()}"
            for f in sorted(p for p in stage.rglob("*") if p.is_file())]
    (stage / "MANIFEST.sha256").write_text("\n".join(sums) + "\n", encoding="utf-8")
    zpath = dest / f"{name}.zip"
    write_zip(stage, zpath, (now.year, now.month, now.day, now.hour, now.minute, 0))
    print(f"snapshot: {zpath} ({zpath.stat().st_size / 1e6:.1f} MB, {len(sums)} files; base {base}; "
          f"{len([l for l in status.splitlines() if l.strip()])} paths differ from the base)")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    label_ = args[args.index("--label") + 1] if "--label" in args else ""
    ex = list(DEFAULT_EXCLUDES)
    i = 0
    while "--exclude" in args[i:]:
        j = args.index("--exclude", i)
        ex.append(args[j + 1])
        i = j + 2
    sys.exit(main(Path(args[0]), label_, tuple(ex)))
