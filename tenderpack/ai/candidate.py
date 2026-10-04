"""The candidate workspace of an AI workflow run (tenderpack/ai/workflow.py): a disposable copy of the preceding tender
state with the new addendum added, under staging/ai/runs/<run_id>/candidate/. Nothing here writes to the real
curation/, config/, build/ or out/: they are read (and hashed) only.

    create()        copies every file the pack configuration names (the curation: op files, register rows and their
                    per-document files, pins, the id ledger, issues, dispositions, proposals, evidence items, activity
                    templates, the clarification register, decisions and the relationships file when they exist; the
                    configuration: assumptions, scenarios, furniture rules, the source manifest; and the owner's reading
                    approvals, readings and reading snapshots, copied UNCHANGED and used read-only), mirrored under
                    candidate/ at the same relative paths; then adds the new PDF as a document (a copy in
                    candidate/input/, a `documents:` entry in candidate/pack.yaml, its sha256 and page count in the
                    candidate's manifest). candidate/pack-before.yaml is the same state WITHOUT the new document, on
                    a second copy (candidate/before/) that promotion never writes: the pre-addendum outputs are built
                    from it and the previous evidence build.
    ingest()        `tenderpack ingest` of the candidate pack into candidate/build/ (a structural failure, exit 2, stops
                    the run with the reason)
    build_before()  the pre-addendum outputs into candidate/out-before/ (the last validated state the review compares
                    with), once per run: in a background process while the AI analysis runs, or copied from a cache
                    keyed by the exact inputs (the previous evidence build, the copied files' contents and the code)
    preflight()     the structural checks an outputs build would fail on, computed cheaply first (E01, C16, C25, C12,
                    C47); a failure refuses the build before it is attempted
    mark()          stamps every candidate output with the BANNER and adds A1's candidate status column (proposed by
                    the AI workflow / unresolved / decided)
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import yaml

from ..util import ROOT, load_yaml, sha256_file

BANNER = "CANDIDATE: proposed by the AI workflow; not reviewed; nothing accepted"

# pack.yaml keys that name curated or configured inputs: (file | dir, default path relative to the repository)
PACK_PATHS = {
    "manifest": ("file", "sources/manifest.json"),
    "furniture": ("file", "config/furniture.yaml"),
    "readings_dir": ("dir", "curation/readings"),
    "approvals": ("file", "curation/approvals.yaml"),
    "decisions": ("file", "curation/reviews/decisions.yaml"),
    "clarifications": ("file", "curation/clarifications/register.yaml"),
    "amendments_dir": ("dir", "curation/amendments"),
    "register": ("file", "curation/register/rows.yaml"),
    "issues": ("file", "curation/register/issues.yaml"),
    "dispositions_dir": ("dir", "curation/register/dispositions"),
    "row_ids": ("file", "curation/register/ids.yaml"),
    "evidence_items_dir": ("dir", "curation/evidence_items"),
    "activity_templates": ("file", "curation/activity_templates.yaml"),
    "assumptions": ("file", "config/assumptions.yaml"),
    "scenarios": ("file", "config/scenarios.yaml"),
    "relationships": ("file", "curation/relationships.yaml"),
}
ADDENDUM = re.compile(r"^ADD-(\d+)$")


class CandidateError(Exception):
    pass


def resolve(p) -> Path:
    p = Path(p)
    return p if p.is_absolute() else ROOT / p


def _real_path(cfg: dict, key: str, default: str) -> Path:
    """Where the pack configuration's `key` points (the relationships file as tenderpack.relationships finds it: the
    `relationships:` key, else beside the register's folder)."""
    if key == "relationships":
        try:
            from ..relationships import default_path
            return Path(default_path(cfg, ROOT))
        except ImportError:
            pass
    return resolve(cfg.get(key, default))


def rel_or_abs(p: Path) -> str:
    p = Path(p).absolute()
    try:
        return p.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return p.resolve().as_posix()


def paths(run_dir: Path) -> dict[str, Path]:
    c = Path(run_dir) / "candidate"
    return {"dir": c, "pack": c / "pack.yaml", "pack_before": c / "pack-before.yaml", "build": c / "build",
            "out": c / "out", "out_before": c / "out-before", "input": c / "input", "logs": Path(run_dir) / "logs",
            "pre_promotion": c / ".pre-promotion", "before": c / "before"}


def _mirror(cand: Path, real: Path, key: str) -> Path:
    real = real.absolute()
    try:
        return cand / real.resolve().relative_to(ROOT.resolve())
    except ValueError:
        return cand / "ext" / key / real.name


def _copy(src: Path, dst: Path) -> None:
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True)
    elif src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)


def _hash_tree(p: Path) -> dict[str, str]:
    if p.is_file():
        return {rel_or_abs(p): sha256_file(p)}
    return {rel_or_abs(f): sha256_file(f) for f in sorted(p.rglob("*")) if f.is_file()} if p.is_dir() else {}


def real_sources(pack: Path) -> list[Path]:
    """Every real file or folder the candidate copies from (for the isolation fingerprint)."""
    cfg = load_yaml(pack) or {}
    out = [Path(pack).resolve()]
    for key, (_, default) in PACK_PATHS.items():
        p = _real_path(cfg, key, default)
        out.append(p)
        if key == "register":
            out.append(p.parent)
        if key == "issues":
            out.append(p.parent / "issues")
        if key == "approvals":
            out.append(p.parent / "reading-snapshots")
    return list(dict.fromkeys(out))


def fingerprint(pack: Path) -> dict[str, str]:
    """sha256 of every real input file the candidate copies (read only; compared after a run)."""
    out: dict[str, str] = {}
    for p in real_sources(pack):
        out.update(_hash_tree(p))
    return dict(sorted(out.items()))


# ---------------------------------------------------------------------------------------------- create

def check(pack: Path, addendum: str, pdf: Path) -> tuple[int, dict]:
    """Refuse (CandidateError) inputs the workflow cannot use: an addendum id that is not ADD-NN or does not follow the
    pack's last addendum, a document the pack already has, a missing or unreadable PDF. Returns (pages, metadata)."""
    import pymupdf
    m = ADDENDUM.match(addendum or "")
    if not m:
        raise CandidateError(f"the addendum id must look like ADD-03, got {addendum!r}")
    pdf = Path(pdf).resolve()
    if not pdf.is_file():
        raise CandidateError(f"no PDF at {pdf}")
    try:
        doc = pymupdf.open(pdf)
        pages, meta = doc.page_count, doc.metadata or {}
    except Exception as e:                                       # noqa: BLE001
        raise CandidateError(f"{pdf} is not a readable PDF: {e}") from None
    pack = Path(pack).resolve()
    if not pack.is_file():
        raise CandidateError(f"no pack configuration at {pack}")
    docs = (load_yaml(pack) or {}).get("documents") or []
    if any(d.get("doc_id") == addendum for d in docs):
        raise CandidateError(f"{addendum} is already a document of {rel_or_abs(pack)}: the workflow adds a NEW addendum to "
                             "the preceding state")
    nums = [int(ADDENDUM.match(d["doc_id"]).group(1)) for d in docs if ADDENDUM.match(str(d.get("doc_id")))]
    if nums and int(m.group(1)) <= max(nums):
        raise CandidateError(f"{addendum} does not follow the pack's last addendum (ADD-{max(nums):02d})")
    return pages, meta


def create(run_dir: Path, pack: Path, addendum: str, pdf: Path, run_id: str) -> dict:
    """Build the candidate workspace (see the module docstring). Returns what the checkpoint records."""
    pages, meta = check(pack, addendum, pdf)
    m = ADDENDUM.match(addendum)
    pdf = Path(pdf).resolve()
    pack = Path(pack).resolve()
    cfg = load_yaml(pack) or {}
    docs = cfg.get("documents") or []
    P = paths(run_dir)
    cand = P["dir"]
    if cand.exists():
        raise CandidateError(f"{cand} exists: a run's candidate is created once (resume the run instead)")
    cand.mkdir(parents=True)
    real_hashes = fingerprint(pack)
    copied: dict[str, str] = {}
    before = dict(cfg, documents=list(docs))
    orig = dict(cfg)
    for key, (kind, default) in PACK_PATHS.items():
        real = _real_path(orig, key, default)
        # two copies: the candidate (promotion writes into it) and the pre-addendum state (out-before is built from
        # it, so it never sees a promoted item)
        for base, conf in ((cand, cfg), (P["before"], before)):
            dest = _mirror(base, real, key)
            if real.exists():
                _copy(real, dest)
                copied[key] = rel_or_abs(real)
            conf[key] = rel_or_abs(dest)             # even when absent: the candidate never reads the real path
            if key == "register" and real.parent.is_dir():
                _copy(real.parent, dest.parent)      # rows/, issues/, pins.yaml, ids.yaml, proposals/, ...
            if key == "issues" and (real.parent / "issues").is_dir():
                _copy(real.parent / "issues", dest.parent / "issues")
            if key == "approvals" and (real.parent / "reading-snapshots").is_dir():
                _copy(real.parent / "reading-snapshots", dest.parent / "reading-snapshots")
    P["input"].mkdir(parents=True, exist_ok=True)
    pdf_copy = P["input"] / pdf.name
    shutil.copyfile(pdf, pdf_copy)
    new_doc = {"doc_id": addendum, "kind": "addendum", "number": int(m.group(1)), "path": rel_or_abs(pdf_copy)}
    cfg["documents"] = list(docs) + [new_doc]
    man_path = resolve(cfg["manifest"])
    man = json.loads(man_path.read_text(encoding="utf-8")) if man_path.exists() else {"files": []}
    entry = {"path": new_doc["path"], "bytes": pdf_copy.stat().st_size, "sha256": sha256_file(pdf_copy), "pages": pages,
             "producer": meta.get("producer"), "creation_date": meta.get("creationDate"),
             "added_by": f"AI workflow run {run_id} (candidate only)"}
    man["files"] = [f for f in man.get("files", []) if f.get("path") != entry["path"]] + [entry]
    man_path.parent.mkdir(parents=True, exist_ok=True)
    man_path.write_text(json.dumps(man, indent=1, ensure_ascii=False), encoding="utf-8")
    orig_id = str(cfg.get("pack_id") or pack.stem)
    cfg["pack_id"] = f"{orig_id}+{addendum}-CANDIDATE"
    head = (f"# CANDIDATE pack of AI workflow run {run_id}: the preceding state ({rel_or_abs(pack)}) with {addendum} added.\n"
            "# Disposable: every curated file named here is a COPY under this run's folder; nothing is accepted.\n")
    P["pack"].write_text(head + yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False), encoding="utf-8")
    P["pack_before"].write_text(
        head.replace("with", "WITHOUT (the pre-addendum state;", 1).replace("added.", "added.)", 1)
        + yaml.safe_dump(before, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return {"dir": str(cand), "pack": str(P["pack"]), "pack_before": str(P["pack_before"]), "build": str(P["build"]),
            "out": str(P["out"]), "out_before": str(P["out_before"]), "pdf_copy": str(pdf_copy),
            "pdf": {"path": str(pdf), "sha256": entry["sha256"], "pages": pages, "bytes": entry["bytes"]},
            "copied": copied, "real_hashes": real_hashes, "preceding_pack_id": orig_id}


@contextlib.contextmanager
def captured(log: Path):
    """Send stdout (and stderr) of in-process commands to a log file."""
    log.parent.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        try:
            yield buf
        finally:
            with open(log, "a", encoding="utf-8") as fh:
                fh.write(buf.getvalue())


def ingest(run_dir: Path) -> dict:
    from ..cli import UnsafeOutputError
    from ..cli import ingest as _ingest
    from ..sources import SourceIntegrityError
    P = paths(run_dir)
    try:
        with captured(P["logs"] / "ingest.log"):
            res = _ingest(P["pack"], P["build"], ROOT, quiet=False)
    except (UnsafeOutputError, SourceIntegrityError) as e:
        return {"exit_code": 2, "status": "refused", "failed": [], "reason": str(e)}
    cov = res["coverage"]
    failed = [f"{c['id']}: {c['detail']}" for c in cov["checks"] if not c["ok"]]
    return {"exit_code": res["exit_code"], "status": res["status"], "failed": failed,
            "problems": list(cov.get("problems") or [])[:20], "pending_review": list(cov.get("pending_review") or []),
            "units": len(res["units"]), "build": str(res["out"]),
            "reason": ("STRUCTURAL FAILURE: " + "; ".join(failed + list(cov.get("problems") or []))[:1500])
            if res["exit_code"] == 2 else None}


# ---------------------------------------------------------------------------------------------- out-before

def code_hash() -> str:
    h = hashlib.sha256()
    pkg = ROOT / "tenderpack"
    for f in sorted(pkg.rglob("*.py")):
        h.update(f.relative_to(pkg).as_posix().encode())
        h.update(f.read_bytes())
    return h.hexdigest()


def before_key(run_dir: Path, evidence: Path) -> str:
    """The cache key of the pre-addendum outputs: the previous evidence build, the content of every file of the
    pre-addendum copy (candidate/before/, by its relative path), the documents and the code."""
    P = paths(run_dir)
    cand = P["before"]
    cfg = load_yaml(P["pack_before"]) or {}
    h = hashlib.sha256()
    h.update(sha256_file(Path(evidence) / "BUILD_MANIFEST.json").encode())
    h.update(json.dumps(cfg.get("documents"), sort_keys=True).encode())
    h.update(str(cfg.get("pack_id")).encode())
    for f in sorted(p for p in cand.rglob("*") if p.is_file()):
        rel = f.relative_to(cand).as_posix()
        h.update(rel.encode())
        h.update(sha256_file(f).encode())
    h.update(code_hash().encode())
    return h.hexdigest()


def _build_before(evidence: Path, pack_before: Path, out: Path, result: Path, log: Path, cache: Path | None,
                  key: str | None) -> dict:
    from .. import stage2
    t0 = time.perf_counter()
    res: dict = {"key": key}
    try:
        if cache is not None and (cache / ".complete").is_file():
            if out.exists():
                shutil.rmtree(out)
            shutil.copytree(cache / "out", out)
            meta = json.loads((cache / ".complete").read_text(encoding="utf-8"))
            res.update(exit_code=0, status="ok", from_cache=str(cache), built_by=meta.get("built_by"))
        else:
            with captured(log):
                b = stage2.build(Path(evidence), out, Path(pack_before), ROOT, quiet=False)
            res.update(exit_code=b["exit_code"], status=b["status"], release=b.get("release"),
                       blockers=len(b.get("blockers") or []), out=str(b["out"]))
            if b["exit_code"] == 0 and cache is not None:
                tmp = cache.with_name(cache.name + f".tmp-{os.getpid()}")
                if tmp.exists():
                    shutil.rmtree(tmp)
                tmp.mkdir(parents=True)
                shutil.copytree(out, tmp / "out")
                (tmp / ".complete").write_text(json.dumps({"key": key, "built_by": str(result.parent.parent)}),
                                               encoding="utf-8")
                if not cache.exists():
                    os.replace(tmp, cache)
                else:
                    shutil.rmtree(tmp, ignore_errors=True)
    except Exception as e:                                       # noqa: BLE001 (recorded; the run reports it)
        res.update(exit_code=2, status="error", reason=f"{type(e).__name__}: {str(e)[:600]}")
    res["seconds"] = round(time.perf_counter() - t0, 3)
    result.parent.mkdir(parents=True, exist_ok=True)
    result.write_text(json.dumps(res, indent=1), encoding="utf-8")
    return res


def before_paths(run_dir: Path, staging: Path, key: str | None) -> dict:
    P = paths(run_dir)
    return {"out": P["out_before"], "result": P["logs"] / "out-before.result.json", "log": P["logs"] / "out-before.log",
            "cache": (Path(staging) / "runs" / "_cache" / f"out-before-{key[:20]}") if key else None}


def start_before(run_dir: Path, evidence: Path, staging: Path, key: str | None, background: bool = True) -> dict:
    """Build candidate/out-before (or copy it from the cache). In the background (a separate process that writes
    out-before.result.json when it ends) or here and now. Returns {pid} or the result."""
    bp = before_paths(run_dir, staging, key)
    P = paths(run_dir)
    if bp["result"].exists():
        bp["result"].unlink()
    if bp["out"].exists():
        shutil.rmtree(bp["out"])
    if not background:
        return _build_before(Path(evidence), P["pack_before"], bp["out"], bp["result"], bp["log"], bp["cache"], key)
    args = {"evidence": str(evidence), "pack_before": str(P["pack_before"]), "out": str(bp["out"]),
            "result": str(bp["result"]), "log": str(bp["log"]), "cache": str(bp["cache"]) if bp["cache"] else None,
            "key": key}
    bp["log"].parent.mkdir(parents=True, exist_ok=True)
    with open(bp["log"], "a", encoding="utf-8") as fh:
        proc = subprocess.Popen([sys.executable, "-m", "tenderpack.ai.candidate", "build-before", json.dumps(args)],
                                cwd=str(ROOT), stdout=fh, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    return {"pid": proc.pid, "background": True, "_proc": proc}


def wait_before(run_dir: Path, staging: Path, key: str | None, pid: int | None, proc=None, poll_s: float = 0.5,
                timeout_s: float = 3600) -> dict | None:
    """The background build's result once it has ended; None when its process is gone without a result."""
    from .checkpoint import _pid_alive
    bp = before_paths(run_dir, staging, key)
    t0 = time.monotonic()
    while True:
        if bp["result"].exists():
            if proc is not None:
                proc.wait()
            return json.loads(bp["result"].read_text(encoding="utf-8"))
        alive = proc.poll() is None if proc is not None else (bool(pid) and _pid_alive(int(pid)))
        if not alive:
            time.sleep(poll_s)
            return json.loads(bp["result"].read_text(encoding="utf-8")) if bp["result"].exists() else None
        if time.monotonic() - t0 > timeout_s:
            return {"exit_code": 2, "status": "error", "reason": f"the background build did not end in {timeout_s} s"}
        time.sleep(poll_s)


# ---------------------------------------------------------------------------------------------- preflight and marking

def preflight(r: dict) -> list[dict]:
    """The structural checks of an outputs build that need no output to be written (stage2.structural_checks):
    E01, C16, C25, C12 and C47. Any failure means the build would be refused."""
    from ..amend import unevidenced_additions
    out = []
    if r["problems"]:
        out.append({"id": "E01", "detail": "; ".join(r["problems"])[:600]})
    bad = [f"{e['row'].id}@{st}: {p}" for e in r["evals"] for st, ev in e["stages"].items() for p in ev["problems"]]
    if bad:
        out.append({"id": "C16", "detail": "; ".join(bad[:6])})
    leaks = [f"{s.stage}: {x}" for s in r["stages"] for x in s.scope_leak]
    if leaks:
        out.append({"id": "C25", "detail": "; ".join(leaks[:4])})
    ids = r["ids"]
    if ids["missing"] or ids["duplicates"] or ids["back"]:
        out.append({"id": "C12", "detail": f"missing {ids['missing']}; duplicated {ids['duplicates']}; withdrawn ids "
                                           f"reused {ids['back']}"})
    added = [f"{b.stage}: {x}" for a, b in zip(r["stages"], r["stages"][1:]) for x in unevidenced_additions(a.state, b.state, b.stage)]
    if added:
        out.append({"id": "C47", "detail": "; ".join(added[:4])})
    return out


HTML_BANNER = ('<div class="tp-candidate-banner" style="background:#fde2e2;border:2px solid #b00000;color:#7a0000;'
               f'font:bold 14px sans-serif;padding:6px 10px;margin:0 0 8px 0">{BANNER}</div>')


def mark(out: Path, row_status: dict[str, str], default_status: str, legend: list[dict]) -> list[str]:
    """Stamp every candidate output with BANNER; rewrite A1 with the candidate status column first after the id."""
    import pymupdf
    from ..render import write_a1
    out = Path(out)
    marked = []
    a1p = out / "a1" / "a1.json"
    if a1p.is_file():
        a1 = json.loads(a1p.read_text(encoding="utf-8"))
        cols = [c for c in a1["columns"] if c["key"] != "candidate_status"]
        cols.insert(1, {"key": "candidate_status", "header": "Candidate status (this AI workflow run: proposed / "
                                                             "unresolved / decided)", "width": 36})
        a1["columns"] = cols
        for rec in a1["rows"]:
            rec["candidate_status"] = row_status.get(rec["id"], default_status)
        a1["title"] = "CANDIDATE — " + a1["title"].replace("CANDIDATE — ", "")
        a1["notice"] = BANNER + ". " + a1["notice"]
        a1.setdefault("sheets", {})["Candidate statuses"] = {
            "columns": [{"key": "status", "header": "Candidate status", "width": 40},
                        {"key": "rows", "header": "Rows", "width": 8},
                        {"key": "meaning", "header": "Meaning", "width": 100}],
            "rows": legend}
        write_a1(a1, out / "a1")
    for f in sorted(p for p in out.rglob("*") if p.is_file()):
        if "/img/" in f.as_posix() or f.name.startswith("."):
            continue
        sfx = f.suffix.lower()
        try:
            if sfx == ".md":
                f.write_text(f"> **{BANNER}**\n\n" + f.read_text(encoding="utf-8"), encoding="utf-8")
            elif sfx == ".html":
                t = f.read_text(encoding="utf-8")
                m = re.search(r"<body[^>]*>", t, re.I)
                t = (t[:m.end()] + HTML_BANNER + t[m.end():]) if m else HTML_BANNER + t
                f.write_text(t, encoding="utf-8")
            elif sfx == ".svg":
                t = f.read_text(encoding="utf-8")
                m = re.search(r"<svg[^>]*>", t, re.I)
                if m:
                    f.write_text(t[:m.end()] + f'<title>{BANNER}</title><text x="4" y="10" font-size="9" fill="#b00000" '
                                 f'font-family="sans-serif">{BANNER}</text>' + t[m.end():], encoding="utf-8")
            elif sfx == ".csv":
                f.write_bytes(f"# {BANNER}\n".encode("utf-8") + f.read_bytes())
            elif sfx == ".json":
                d = json.loads(f.read_text(encoding="utf-8"))
                if not isinstance(d, dict):
                    continue
                f.write_text(json.dumps({"_candidate": BANNER, **{k: v for k, v in d.items() if k != "_candidate"}},
                                        ensure_ascii=False, indent=1), encoding="utf-8")
            elif sfx == ".pdf":
                doc = pymupdf.open(f)
                for page in doc:
                    page.insert_text((24, 11), BANNER, fontsize=7, color=(0.69, 0, 0))
                tmp = f.with_name(f".{f.name}.marked")
                doc.save(tmp)
                doc.close()
                os.replace(tmp, f)
            elif sfx == ".xlsx" and f.name != "a1.xlsx":
                continue
            else:
                continue
            marked.append(f.relative_to(out).as_posix())
        except (ValueError, OSError, RuntimeError) as e:          # recorded: an unmarked file is listed, never hidden
            marked.append(f"NOT MARKED {f.relative_to(out).as_posix()}: {e}")
    if a1p.is_file():
        marked.append("a1/a1.xlsx")
    (out / "CANDIDATE.md").write_text(
        f"# {BANNER}\n\nEvery file in this folder was produced by the AI workflow in a disposable candidate workspace. "
        "Nothing here is reviewed, accepted or published; the real curation/, config/ and out/ were not changed.\n\n"
        "A1's first column after the id gives each row's candidate status:\n\n"
        + "\n".join(f"- **{x['status']}** ({x['rows']} rows): {x['meaning']}" for x in legend) + "\n\n"
        "Data files that cannot carry a banner (JSON lists) are covered by this file.\n", encoding="utf-8")
    return marked


# ---------------------------------------------------------------------------------------------- background entry point

if __name__ == "__main__":                                       # python -m tenderpack.ai.candidate build-before JSON
    if len(sys.argv) == 3 and sys.argv[1] == "build-before":
        a = json.loads(sys.argv[2])
        r = _build_before(Path(a["evidence"]), Path(a["pack_before"]), Path(a["out"]), Path(a["result"]), Path(a["log"]),
                          Path(a["cache"]) if a.get("cache") else None, a.get("key"))
        sys.exit(0 if r.get("exit_code") == 0 else 1)
    sys.exit("usage: python -m tenderpack.ai.candidate build-before '<json>'")
