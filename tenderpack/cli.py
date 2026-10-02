"""Command line: python -m tenderpack <command>

  ingest   [--pack config/pack.yaml] [--out build] [--require-approved]
           extract, detect regions, segment, check readings, write reports. Exit codes:
             0  structure OK (readings may still be PENDING HUMAN REVIEW, printed visibly)
             2  STRUCTURAL FAILURE (a coverage check failed); the previous build is kept and the
                failed build is written to <out>.failed for inspection
             3  structure OK but readings pending review, and --require-approved was given: the gate
                is applied BEFORE publishing, so the previous build is kept and this candidate is
                written to <out>.rejected (with REJECTED.md saying why)
  show     UNIT_ID [--out build]       print a unit with its source references; write a highlighted crop
  approve  REGION_ID --reviewer NAME [--notes TEXT] [--pack ...] [--approvals PATH]
           record a person's approval of a reading, pinned to its review subject (reading +
           uncertainties + evidence). Refuses placeholder names and readings that fail checks.

Stage 2 (from a published evidence build; see tenderpack/stage2.py):
  outputs  [--evidence build] [--out out] [--pack ...]
           A1 (xlsx/csv/json), A2, A3 (one-page pdf), A5 for every stage of the amendment path.
           Exit 0: published (drafts, with pending reviews listed); 2: structural failure, previous
           outputs kept, candidate in <out>.failed.
  draft    ADD-0N [--evidence build] [--to PATH]
           propose ops and dispositions for an addendum (every op PROPOSED); prints or writes YAML.
           Never writes into curation/ unless --to names a file there explicitly.
  pin      [--evidence build] [--refresh]
           pin each interpretation to its dependencies (curation/register/pins.yaml).

Output safety: the output directory may not be the repository, a parent of it, the home or root
directory, a protected repository folder (sources, config, curation, ...), or anything that
contains or lies inside an input. An existing directory is replaced only if it is empty or a
previous build (it holds `.tenderpack-build` or BUILD_MANIFEST.json). Each build is written to a
temporary sibling directory and swapped in only after it succeeds.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import sys
from pathlib import Path

import pymupdf
import yaml

from .coverage import coverage_report, write_reports
from .extract import FurnitureRules, extract_page
from .packets import build_evidence, write_packet
from .pipeline import run_pack
from .readings import (check_reading, load_approvals, load_readings, reading_units, review_status,
                       review_subject, valid_reviewer)
from .regions import detect_regions
from .sources import load_documents
from .util import ROOT, dump_json, load_yaml, sha256_bytes, sha256_file

MARKER = ".tenderpack-build"
PROTECTED = ("sources", "config", "curation", "tenderpack", "tests", "docs", "worklog", ".git", ".venv")


class UnsafeOutputError(Exception):
    pass


def _failed_dir(out: Path) -> Path:
    return out.with_name(out.name + ".failed")


def _rejected_dir(out: Path) -> Path:
    return out.with_name(out.name + ".rejected")


def _is_previous_build(d: Path) -> bool:
    return d.is_dir() and ((d / MARKER).is_file() or (d / "BUILD_MANIFEST.json").is_file() or not any(d.iterdir()))


def check_output_dir(out: Path, root: Path, inputs: list[Path]) -> None:
    """Refuse output locations that could overwrite the repository, its inputs or unrelated files. The same
    tests apply to the candidate siblings (<out>.failed, <out>.rejected), which a build may replace."""
    out, root = Path(out).absolute(), Path(root).resolve()
    home = Path.home().resolve()
    for d in (out, _failed_dir(out), _rejected_dir(out)):
        if d.is_symlink():
            raise UnsafeOutputError(f"refusing to use {d}: it is a symbolic link")
        r = d.resolve()
        if r == Path(r.anchor) or r == home or home.is_relative_to(r):
            raise UnsafeOutputError(f"refusing to write to {r}: it is the root or home directory or contains it")
        if r == root or root.is_relative_to(r):
            raise UnsafeOutputError(f"refusing to write to {r}: it is the repository or one of its parents")
        for name in PROTECTED:
            prot = root / name
            if r == prot or r.is_relative_to(prot):
                raise UnsafeOutputError(f"refusing to write to {r}: inside the protected folder {prot}")
        for inp in inputs:
            inp = Path(inp).resolve()
            if inp == r or inp.is_relative_to(r) or r.is_relative_to(inp):
                raise UnsafeOutputError(f"refusing to write to {r}: it contains or lies inside the input {inp}")
    for d in (out, _failed_dir(out), _rejected_dir(out)):
        if d.exists() and not _is_previous_build(d):
            raise UnsafeOutputError(f"refusing to replace {d}: it exists and is not a previous tenderpack build "
                                    f"(no {MARKER} or BUILD_MANIFEST.json)")


def _rel(p: Path, root: Path) -> str:
    p = Path(p).resolve()
    return p.relative_to(root.resolve()).as_posix() if p.is_relative_to(root.resolve()) else p.as_posix()


def _inputs(pack_path: Path, cfg: dict, root: Path) -> list[Path]:
    paths = [pack_path, root / cfg["manifest"], root / cfg["furniture"],
             root / cfg.get("readings_dir", "curation/readings"), root / cfg.get("approvals", "curation/approvals.yaml")]
    return paths + [root / d["path"] for d in cfg["documents"]]


def _set_aside(tmp: Path, dest: Path, reason: str | None = None) -> None:
    if dest.exists():
        shutil.rmtree(dest)                           # a previous candidate; checked safe above
    if reason:
        (tmp / "REJECTED.md").write_text(reason, encoding="utf-8")
    tmp.rename(dest)


def ingest(pack_path: Path, out: Path, root: Path = ROOT, quiet: bool = False, require_approved: bool = False) -> dict:
    """Build into a temporary sibling of `out` and publish it (replace `out`) only if every structural check
    passes and, with `require_approved`, no reading is pending. Otherwise the previous build stays untouched
    and the candidate is set aside: <out>.failed (structural failure) or <out>.rejected (approval gate)."""
    pack_path, out, root = Path(pack_path).resolve(), Path(out).absolute(), Path(root).resolve()
    cfg = load_yaml(pack_path)
    check_output_dir(out, root, _inputs(pack_path, cfg, root))   # on the path as given: a symlink is refused
    out = out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.parent / f".{out.name}.building-{os.getpid()}"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()
    try:
        (tmp / MARKER).write_text("tenderpack build directory (safe for tenderpack to replace)\n", encoding="utf-8")
        res = _build(pack_path, cfg, tmp, root)
    except BaseException:
        shutil.rmtree(tmp, ignore_errors=True)
        raise
    cov = res["coverage"]
    gate = require_approved and bool(cov["pending_review"])
    try:
        _publish(res, cov, gate, tmp, out)
    except BaseException:
        shutil.rmtree(tmp, ignore_errors=True)
        raise
    res["pack"].out = res["out"]
    if not quiet:
        _print_summary(res, out, root)
    return res


def _publish(res: dict, cov: dict, gate: bool, tmp: Path, out: Path) -> None:
    if cov["status"] == "ok" and not gate:
        old = None
        if out.exists():
            old = out.parent / f".{out.name}.old-{os.getpid()}"
            out.rename(old)
        tmp.rename(out)
        if old is not None:
            shutil.rmtree(old)
        for stale in (_failed_dir(out), _rejected_dir(out)):
            if stale.exists():
                shutil.rmtree(stale)                  # stale candidates; checked safe above
        res["out"] = out
        res["status"], res["exit_code"] = "ok", 0
    elif cov["status"] != "ok":
        _set_aside(tmp, _failed_dir(out))
        res["out"] = _failed_dir(out)
        res["status"], res["exit_code"] = cov["status"], 2
    else:
        _set_aside(tmp, _rejected_dir(out),
                   "# Rejected by the approval gate (--require-approved)\n\n"
                   f"Structure OK, but these readings are pending human review: {', '.join(cov['pending_review'])}.\n"
                   "This candidate was not published; the previous build (if any) was kept.\n")
        res["out"] = _rejected_dir(out)
        res["status"], res["exit_code"] = "rejected_pending_review", 3


def _print_summary(res: dict, out: Path, root: Path) -> None:
    cov = res["coverage"]
    for c in cov["checks"]:
        print(f"{c['id']} {'pass' if c['ok'] else 'FAIL'}  {c['detail']}")
    for p in cov["problems"]:
        print("PROBLEM:", p)
    for f in cov["evidence"]["failures"][:10]:
        print(f"EVIDENCE MISMATCH: {f['unit']} ({f['kind']}): {f['why']}")
    if cov["pending_review"]:
        print(f"PENDING HUMAN REVIEW: {', '.join(cov['pending_review'])} (not approved; units from these readings "
              "carry reading.status = pending)")
    if res["status"] == "rejected_pending_review":
        print(f"NOT PUBLISHED: --require-approved was given and readings are pending human review. Previous build kept at "
              f"{_rel(out, root)} (if any); this candidate written to {_rel(res['out'], root)}.")
    elif cov["status"] == "ok":
        print(f"STRUCTURE OK. units: {len(res['units'])}  ->  {_rel(out, root)}/units.md, coverage.md, exclusions.md, review/")
    else:
        failed = [c["id"] for c in cov["checks"] if not c["ok"]]
        print(f"STRUCTURAL FAILURE: {', '.join(failed)}. Previous build kept at {_rel(out, root)} "
              f"(if any); this build written to {_rel(res['out'], root)} for inspection.")


def _build(pack_path: Path, cfg: dict, out: Path, root: Path) -> dict:
    pack = run_pack(pack_path, out, root)
    readings_dir = root / cfg.get("readings_dir", "curation/readings")
    readings = load_readings(readings_dir)
    approvals_path = root / cfg.get("approvals", "curation/approvals.yaml")
    approvals = load_approvals(approvals_path)
    packets, r_units, evs, sources = {}, {}, {}, {}
    for d in pack.docs:
        pdf = pymupdf.open(d.doc.path)
        for g in d.regions:
            reading, rpath = readings.get(g.region_id, (None, None))
            ev = evs[g.region_id] = build_evidence(pdf, g, reading, out / "review", out)
            packets[g.region_id] = write_packet(pdf, g, reading, approvals, ev, out / "review", out, root, rpath,
                                                d.doc.sha256, _rel(approvals_path, root))
            if reading is not None:
                st = review_status(reading, approvals, review_subject(reading, g, d.doc.sha256))
                r_units[g.region_id] = reading_units(reading, g, st, ev)
                sources[g.region_id] = (reading, st)
    orphan = sorted(set(readings) - set(packets))
    ordered = []
    for d in pack.docs:
        for uid in d.order:
            u = d.units[uid].to_dict()
            ordered.append(u)
            if u["kind"] == "region" and u.get("region") in r_units:
                ru = r_units[u["region"]]
                u["reading"] = {"unit_id": ru[0]["unit_id"], "status": ru[0]["reading"]["status"]}
                ordered.extend(ru)
    cov = coverage_report(pack, packets, r_units, orphan, evs, sources)
    rules = [{k: v for k, v in r.items() if not k.startswith("_")}
             for r in load_yaml(root / cfg["furniture"])["rules"]]
    title = cfg.get("pack_id", pack_path.stem)
    write_reports(out, cov, ordered, rules, title)
    dump_json({"pack": title, "units": ordered}, out / "units.json")
    dump_json(cov, out / "coverage.json")
    dump_json({"regions": [g.to_dict() for d in pack.docs for g in d.regions]}, out / "regions.json")
    inputs = {_rel(d.doc.path, root): d.doc.sha256 for d in pack.docs}
    for p in [pack_path, root / cfg["furniture"], *sorted(readings_dir.glob("*.yaml"))]:
        inputs[_rel(p, root)] = sha256_file(p)
    ap = root / cfg.get("approvals", "curation/approvals.yaml")
    if ap.exists():
        inputs[_rel(ap, root)] = sha256_file(ap)
    outputs = {}
    for p in sorted(out.rglob("*")):
        if p.is_file() and p.name != "BUILD_MANIFEST.json":
            outputs[p.relative_to(out).as_posix()] = sha256_file(p)   # relative to the build dir
    dump_json({"status": cov["status"], "inputs": inputs, "outputs": outputs,
               "tools": {"python": sys.version.split()[0], "pymupdf": pymupdf.__version__}}, out / "BUILD_MANIFEST.json")
    return {"pack": pack, "coverage": cov, "units": ordered, "packets": packets, "evidence": evs,
            "reading_sources": sources}


def show(unit_id: str, out: Path, root: Path = ROOT) -> int:
    data = json.loads((out / "units.json").read_text(encoding="utf-8"))
    u = next((x for x in data["units"] if x["unit_id"] == unit_id), None)
    if u is None:
        print(f"no unit {unit_id}")
        return 1
    print(f"{u['unit_id']}  [{u['kind']}]  doc {u['doc']}  pages {u.get('pages')}")
    if u.get("origin") == "image_reading":
        print(f"  from image reading of {u['reading']['region']}: status {u['reading']['status'].upper()}")
    for a in u.get("anchors", []):
        print(f"  page {a['page']} bbox {a['bbox']}" + (f" crop {a['crop']}" if a.get("crop") else ""))
    print("  text:", u.get("text"))
    if u.get("translation"):
        print("  translation:", u["translation"])
    cfg_docs = {d["doc_id"]: d["path"] for d in load_yaml(root / "config/pack.yaml")["documents"]}
    if u["doc"] in cfg_docs and u.get("anchors"):
        a = u["anchors"][0]
        pdf = pymupdf.open(root / cfg_docs[u["doc"]])
        page = pdf[a["page"] - 1]
        doc = pymupdf.open()
        pg = doc.new_page(width=page.rect.width, height=page.rect.height)
        pg.show_pdf_page(pg.rect, pdf, a["page"] - 1)
        for an in u["anchors"]:
            if an["page"] == a["page"]:
                pg.draw_rect(pymupdf.Rect(an["bbox"]) + (-2, -2, 2, 2), color=(0.9, 0.1, 0.1), width=1.5)
        dest = out / "show" / (unit_id.replace(":", "_").replace("/", "_").replace("#", "_") + ".png")
        dest.parent.mkdir(parents=True, exist_ok=True)
        clip = pymupdf.Rect(0, max(a["bbox"][1] - 120, 0), page.rect.width, min(a["bbox"][3] + 120, page.rect.height))
        pg.get_pixmap(dpi=110, clip=clip).save(dest)
        print("  highlighted crop:", _rel(dest, root))
    return 0


def approve(region_id: str, reviewer: str, notes: str | None, root: Path = ROOT,
            pack_path: Path | None = None, approvals_path: Path | None = None) -> int:
    """Record a person's approval. Only a person runs this; the program never approves anything itself."""
    if not valid_reviewer(reviewer):
        print(f"refused: --reviewer must name the person approving, not a placeholder ({reviewer!r}). Nothing written.")
        return 2
    pack_path = Path(pack_path or root / "config/pack.yaml").resolve()
    cfg = load_yaml(pack_path)
    readings = load_readings(root / cfg.get("readings_dir", "curation/readings"))
    if region_id not in readings:
        print(f"refused: no reading for {region_id}. Nothing written.")
        return 1
    reading, _ = readings[region_id]
    doc = next((d for d in load_documents(cfg, root) if d.doc_id == reading.source.doc), None)
    if doc is None:
        print(f"refused: document {reading.source.doc} is not in the pack. Nothing written.")
        return 1
    pdf = pymupdf.open(doc.path)
    page = pdf[reading.source.page - 1]
    rules = FurnitureRules.from_file(root / cfg["furniture"])
    region = next((g for g in detect_regions(doc.doc_id, page, extract_page(doc.doc_id, page, rules))
                   if g.region_id == region_id), None)
    if region is None:
        print(f"refused: region {region_id} is not detected on {doc.doc_id} p{reading.source.page}. Nothing written.")
        return 1
    if region.xref:
        region.native = {"sha256": sha256_bytes(pdf.extract_image(region.xref)["image"])}
    failed = [c for c in check_reading(reading, region, pdf) if not c["ok"]]
    if failed:
        print(f"refused: the reading fails {[c['check'] for c in failed]}; fix it first. Nothing written.")
        return 2
    subject = review_subject(reading, region, doc.sha256)
    path = Path(approvals_path).resolve() if approvals_path else root / cfg.get("approvals", "curation/approvals.yaml")
    data = (load_yaml(path) or {}) if path.exists() else {}
    data.setdefault("approvals", []).append({
        "region_id": region_id, "reviewer": reviewer.strip(), "date": dt.date.today().isoformat(),
        "subject_sha256": subject["sha256"], "covers": subject["covers"], "evidence": subject["evidence"],
        "notes": notes})
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# Human approvals of readings, written only by `tenderpack approve` on a person's instruction.\n"
                    "# Each entry pins the review subject: the reading (content, uncertainties, source claims)\n"
                    "# and its evidence (source PDF, region position, native image).\n"
                    + yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"approved {region_id} by {reviewer.strip()}; review subject sha256 {subject['sha256']}")
    return 0


def draft_cmd(addendum: str, evidence: Path, to: str | None) -> int:
    from .draft import draft
    units = json.loads((Path(evidence) / "units.json").read_text(encoding="utf-8"))["units"]
    if not any(u["doc"] == addendum for u in units):
        print(f"no units for {addendum} in {evidence}")
        return 1
    text = ("# DRAFTED by tenderpack.draft; every op PROPOSED. Review, correct and save as curation/amendments/"
            f"{addendum}.yaml to curate it.\n"
            + yaml.safe_dump(draft(units, addendum).model_dump(exclude_none=True), allow_unicode=True, sort_keys=False, width=110))
    if to is None:
        print(text, end="")
        return 0
    dest = Path(to)
    if dest.exists():
        print(f"refused: {dest} exists; drafts never overwrite a file")
        return 2
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    print(f"wrote {dest}")
    return 0


def pin_cmd(evidence: Path, pack_path: Path, refresh: bool) -> int:
    from .amend import Engine, load_opfile
    from .register import compute_pins, load_rows, pins_path, write_pins
    cfg = load_yaml(pack_path)
    units = json.loads((Path(evidence) / "units.json").read_text(encoding="utf-8"))["units"]
    amend_dir = ROOT / cfg.get("amendments_dir", "curation/amendments")
    addenda = sorted({u["doc"] for u in units if u["doc"].startswith("ADD-")}, key=lambda x: int(x.split("-")[1]))
    missing = [a for a in addenda if not (amend_dir / f"{a}.yaml").exists()]
    if missing:
        print(f"refused: no curated op file for {missing}; pins are taken only against curated amendments")
        return 2
    stages = Engine(units, [load_opfile(amend_dir / f"{a}.yaml") for a in addenda]).run()
    rows_path = ROOT / cfg.get("register", "curation/register/rows.yaml")
    rf = load_rows(rows_path)
    n = compute_pins(rf, stages, refresh)
    write_pins(rf, pins_path(rows_path),
               "# Written by `python -m tenderpack pin` (machine-generated; do not edit by hand).\n"
               "# For each row and interpretation stage: the hash of every dependency when the interpretation\n"
               "# was drafted. A later change to any of them makes the row STALE until a person re-reviews it.\n")
    print(f"pinned {n} interpretation(s); wrote {pins_path(rows_path)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tenderpack")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("ingest")
    a.add_argument("--pack", default=str(ROOT / "config/pack.yaml"))
    a.add_argument("--out", default=str(ROOT / "build"))
    a.add_argument("--require-approved", action="store_true",
                   help="exit 3 if any reading is still pending human review")
    b = sub.add_parser("show")
    b.add_argument("unit_id")
    b.add_argument("--out", default=str(ROOT / "build"))
    c = sub.add_parser("approve")
    c.add_argument("region_id")
    c.add_argument("--reviewer", required=True)
    c.add_argument("--notes")
    c.add_argument("--pack", default=str(ROOT / "config/pack.yaml"))
    c.add_argument("--approvals", help="approvals file (default: the pack's `approvals` path)")
    d = sub.add_parser("outputs")
    d.add_argument("--evidence", default=str(ROOT / "build"))
    d.add_argument("--out", default=str(ROOT / "out"))
    d.add_argument("--pack", default=str(ROOT / "config/pack.yaml"))
    e = sub.add_parser("draft")
    e.add_argument("addendum")
    e.add_argument("--evidence", default=str(ROOT / "build"))
    e.add_argument("--to")
    f = sub.add_parser("pin")
    f.add_argument("--evidence", default=str(ROOT / "build"))
    f.add_argument("--pack", default=str(ROOT / "config/pack.yaml"))
    f.add_argument("--refresh", action="store_true", help="re-pin every interpretation, not only unpinned ones")
    args = ap.parse_args(argv)
    if args.cmd == "outputs":
        from .stage2 import build
        try:
            return build(Path(args.evidence), Path(args.out), Path(args.pack), ROOT)["exit_code"]
        except UnsafeOutputError as err:
            print(f"REFUSED: {err}")
            return 2
    if args.cmd == "draft":
        return draft_cmd(args.addendum, Path(args.evidence), args.to)
    if args.cmd == "pin":
        return pin_cmd(Path(args.evidence), Path(args.pack), args.refresh)
    if args.cmd == "ingest":
        try:
            res = ingest(Path(args.pack), Path(args.out), require_approved=args.require_approved)
        except UnsafeOutputError as e:
            print(f"REFUSED: {e}")
            return 2
        return res["exit_code"]
    if args.cmd == "show":
        return show(args.unit_id, Path(args.out))
    return approve(args.region_id, args.reviewer, args.notes, ROOT, Path(args.pack), args.approvals)


if __name__ == "__main__":
    sys.exit(main())
