"""Verify a draft archive in a fresh location: extraction, checksums, links, the repository bundle, and an offline rebuild.

Usage: python scripts/verify_archive.py ARCHIVE_ZIP WORK_DIR [--wheels WHEEL_DIR] [--python PYTHON] [--no-tests]

  1. unzip into WORK_DIR (must not exist) and check every file against SHA256SUMS;
  2. links: every link in A3 (a3.pdf) resolves to a3_detail.html and an element with that id; every relative
     src/href in the review pages and a3_detail.html resolves to a file (and anchor) inside the archive;
  3. clone A4_work_log/repository.bundle; HEAD must equal the commit in the archive's name, the tree clean;
  4. with --wheels, and only where `unshare -n` gives a namespace with no network: create a virtualenv, install
     from the wheel directory with --no-index, then inside the clone regenerate everything that is committed
     (make evidence, outputs, drill, rehearsal; the blind rehearsal's out-after-fixes) and require the clone to
     stay clean (every regenerated file byte-identical to the committed one); compare the rebuilt outputs with
     the archive's A1/A2/A3/A5/REVIEW (scripts/compare_outputs.py); run the test suite.

Prints one line per step and exits 1 on the first failure. Linux only for step 4 (`unshare`); on a Mac use
docs/VERIFY_ON_MAC.md.
"""
from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import sys
import time
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


def say(ok: bool, msg: str) -> None:
    print(f"{'PASS' if ok else 'FAIL'}  {msg}", flush=True)
    if not ok:
        sys.exit(1)


class Refs(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.refs: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("name"):
            self.ids.add(a["name"])
        for k in ("src", "href"):
            if a.get(k):
                self.refs.append(a[k])


def parse(p: Path) -> Refs:
    r = Refs()
    r.feed(p.read_text(encoding="utf-8"))
    return r


def check_ref(page: Path, ref: str, root: Path, cache: dict) -> str | None:
    u = urlparse(ref)
    if u.scheme == "data":
        return None
    if u.scheme or ref.startswith("//"):
        return f"external link {ref} (the archive must work offline)"
    target = page.resolve() if not u.path else (page.parent / unquote(u.path)).resolve()
    if root.resolve() not in target.parents and target != root.resolve():
        return f"{ref} leaves the archive"
    if not target.exists():
        return f"{ref} -> missing {target.relative_to(root.resolve())}"
    if u.fragment and target.suffix == ".html":
        ids = cache.setdefault(target, parse(target).ids)
        if unquote(u.fragment) not in ids:
            return f"{ref} -> no element with id '{u.fragment}'"
    return None


def run(cmd: list[str], cwd: Path, log: Path, offline: bool = False) -> int:
    full = (["unshare", "-n"] if offline else []) + cmd
    with log.open("a", encoding="utf-8") as f:
        f.write(f"\n$ {' '.join(full)}\n")
        f.flush()
        return subprocess.run(full, cwd=cwd, stdout=f, stderr=subprocess.STDOUT).returncode


def main(zpath: Path, work: Path, wheels: Path | None, python: str, tests: bool) -> int:
    t0 = time.time()
    if work.exists():
        say(False, f"{work} exists; give a fresh location")
    work.mkdir(parents=True)
    with zipfile.ZipFile(zpath) as z:
        z.extractall(work)
        n_zip = len(z.namelist())
    roots = [p for p in work.iterdir() if p.is_dir()]
    say(len(roots) == 1, f"extracted {n_zip} entries into one folder: {roots[0].name if roots else '-'}")
    root = roots[0]
    sha = root.name.rsplit("_", 1)[-1]

    # 1. checksums
    bad, n = [], 0
    for line in (root / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, rel = line.split("  ", 1)
        n += 1
        f = root / rel
        if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest() != digest:
            bad.append(rel)
    listed = {l.split("  ", 1)[1] for l in (root / "SHA256SUMS").read_text(encoding="utf-8").splitlines()}
    unlisted = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()
                and p.name != "SHA256SUMS" and p.relative_to(root).as_posix() not in listed]
    say(not bad and not unlisted, f"SHA256SUMS: {n} files match; unlisted files: {len(unlisted)}; mismatches: {bad[:5]}")

    # 2. links
    import pymupdf  # noqa: PLC0415 (only needed here)
    a3 = root / "A3_disqualification_sheet"
    doc = pymupdf.open(a3 / "a3.pdf")
    say(doc.page_count == 1, f"A3 is one page ({doc.page_count})")
    # Read each link's own PDF object: PyMuPDF reports a relative /URI action as a "file" link, so check that the
    # action really is /URI (not /Launch, which viewers block) and that its target exists.
    links = []
    for ln in doc[0].get_links():
        obj = doc.xref_object(ln["xref"])
        m = re.search(r"/S /URI\s+/URI \((.*?)\)", obj)
        links.append(m.group(1) if m else f"not a /URI action: {obj[:80]}")
    detail_ids = parse(a3 / "a3_detail.html").ids
    broken = [u for u in links if not (u.startswith("a3_detail.html#") and unquote(u.split("#", 1)[1]) in detail_ids)]
    say(bool(links) and not broken, f"A3: {len(links)} /URI links ({len(set(links))} targets), each to an id in "
        f"a3_detail.html; broken: {broken[:5]}")
    pages = sorted((root / "REVIEW").rglob("*.html")) + [a3 / "a3_detail.html"]
    cache: dict = {}
    problems, nref = [], 0
    for p in pages:
        for ref in parse(p).refs:
            nref += 1
            e = check_ref(p, ref, root, cache)
            if e:
                problems.append(f"{p.relative_to(root)}: {e}")
    say(not problems, f"review pages and A3 detail: {len(pages)} pages, {nref} src/href, unresolved: {len(problems)} {problems[:5]}")

    # 3. repository bundle
    clone = work / "repo"
    r = subprocess.run(["git", "clone", "-q", str(root / "A4_work_log" / "repository.bundle"), str(clone)],
                       capture_output=True, text=True)
    say(r.returncode == 0, f"git clone from the bundle {r.stderr.strip()[:200]}")
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=clone, capture_output=True, text=True).stdout.strip()
    ncommits = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=clone, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=clone, capture_output=True, text=True).stdout.strip()
    say(head == sha and not dirty, f"clone HEAD {head} equals the archive's commit {sha}; {ncommits} commits; tree clean")

    if not wheels:
        print(f"done (no --wheels: offline rebuild skipped) in {time.time() - t0:.0f} s")
        return 0

    # 4. offline install, rebuild, compare, tests
    probe = subprocess.run(["unshare", "-n", python, "-c",
                            "import socket\nfor h in (('pypi.org',443),('1.1.1.1',443)):\n"
                            "    try:\n        socket.create_connection(h, timeout=3); print('REACHED', h)\n"
                            "    except OSError as e:\n        print('blocked', h, type(e).__name__)"],
                           capture_output=True, text=True)
    say(probe.returncode == 0 and "REACHED" not in probe.stdout,
        f"no network inside `unshare -n`: {' | '.join(probe.stdout.split(chr(10))[:2])}")
    log = work / "offline.log"
    venv = work / "venv"
    req = Path(wheels) / "requirements.txt" if (Path(wheels) / "requirements.txt").exists() else Path(wheels).parent / "requirements.txt"
    t = time.time()
    rc = run([python, "-m", "venv", str(venv)], work, log, offline=True)
    rc = rc or run([str(venv / "bin/python"), "-m", "pip", "install", "-q", "--no-index", "--find-links", str(wheels),
                    "-r", str(req)], work, log, offline=True)
    say(rc == 0, f"offline: virtualenv and --no-index install from {Path(wheels).name} ({time.time() - t:.0f} s); log {log}")
    py = str(venv / "bin/python")
    for target in ("evidence", "outputs", "drill", "rehearsal"):
        t = time.time()
        rc = run(["make", target, f"PY={py}"], clone, log, offline=True)
        say(rc == 0, f"offline: make {target} in the clone ({time.time() - t:.0f} s)")
    for b, target in (("rehearsals/blind-01", "out-after-fixes"), ("rehearsals/blind-02", "out-curated")):
        if not (clone / b / "work/pack.yaml").exists():
            continue
        t = time.time()
        rc = run([py, "-m", "tenderpack", "ingest", "--pack", f"{b}/work/pack.yaml", "--out", f"{b}/build"], clone, log, offline=True)
        rc = rc or run([py, "-m", "tenderpack", "outputs", "--evidence", f"{b}/build", "--pack", f"{b}/work/pack.yaml",
                        "--out", f"{b}/{target}"], clone, log, offline=True)
        say(rc == 0, f"offline: {b} pack re-ingested and {target} rebuilt ({time.time() - t:.0f} s)")
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=clone, capture_output=True, text=True).stdout.strip()
    say(not dirty, "every regenerated file equals the committed one (build/, out/, out-drill/, out-drill-b/, "
        f"blind-01 out-after-fixes, blind-02 out-curated; git status clean){': ' + dirty[:400] if dirty else ''}")
    r = subprocess.run([py, "scripts/compare_outputs.py", "out", str(root)], cwd=clone, capture_output=True, text=True)
    say(r.returncode == 0, f"rebuilt outputs vs the archive: {r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-300:]}")
    if tests:
        t = time.time()
        rc = run([py, "-m", "pytest", "-q", "-p", "no:cacheprovider"], clone, log, offline=True)
        tail = [l for l in log.read_text(encoding="utf-8").splitlines() if re.search(r"\d+ (passed|failed)", l)]
        say(rc == 0, f"offline: test suite: {tail[-1] if tail else '?'} ({time.time() - t:.0f} s)")
    print(f"done in {time.time() - t0:.0f} s")
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d  # noqa: E731
    sys.exit(main(Path(a[0]), Path(a[1]), Path(opt("--wheels")) if opt("--wheels") else None,
                  opt("--python", sys.executable), "--no-tests" not in a))
