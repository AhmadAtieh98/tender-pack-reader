"""Command line: python -m tenderpack <command>

  ingest   [--pack config/pack.yaml] [--out build]   extract, detect regions, segment, check readings, write reports
  show     UNIT_ID [--out build]                     print a unit with its source references; write a highlighted crop
  approve  REGION_ID --reviewer NAME [--notes TEXT]  record a person's approval of a reading (pinned to its content hash)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import sys
from pathlib import Path

import pymupdf
import yaml

from .coverage import coverage_report, write_reports
from .packets import build_evidence, write_packet
from .pipeline import run_pack
from .readings import load_approvals, load_readings, reading_units, review_status
from .util import ROOT, dump_json, load_yaml, sha256_file


def _rel(p: Path, root: Path) -> str:
    p = Path(p).resolve()
    return p.relative_to(root.resolve()).as_posix() if p.is_relative_to(root.resolve()) else p.as_posix()


def ingest(pack_path: Path, out: Path, root: Path = ROOT, quiet: bool = False) -> dict:
    pack_path, out, root = Path(pack_path).resolve(), Path(out).resolve(), Path(root).resolve()
    cfg = load_yaml(pack_path)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    pack = run_pack(pack_path, out, root)
    readings_dir = root / cfg.get("readings_dir", "curation/readings")
    readings = load_readings(readings_dir)
    approvals = load_approvals(root / cfg.get("approvals", "curation/approvals.yaml"))
    packets, r_units = {}, {}
    for d in pack.docs:
        pdf = pymupdf.open(d.doc.path)
        for g in d.regions:
            reading, rpath = readings.get(g.region_id, (None, None))
            ev = build_evidence(pdf, g, reading, out / "review", out)
            packets[g.region_id] = write_packet(pdf, g, reading, approvals, ev, out / "review", out, root, rpath)
            if reading is not None:
                st = review_status(reading, approvals)
                r_units[g.region_id] = reading_units(reading, g, st, ev)
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
    cov = coverage_report(pack, packets, r_units)
    if orphan:
        cov["problems"].append(f"readings with no detected region: {orphan}")
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
    import pymupdf as _m
    dump_json({"inputs": inputs, "outputs": outputs,
               "tools": {"python": sys.version.split()[0], "pymupdf": _m.__version__}}, out / "BUILD_MANIFEST.json")
    if not quiet:
        for c in cov["checks"]:
            print(f"{c['id']} {'pass' if c['ok'] else 'FAIL'}  {c['detail']}")
        if cov["pending_review"]:
            print(f"PENDING HUMAN REVIEW: {', '.join(cov['pending_review'])}")
        for p in cov["problems"]:
            print("PROBLEM:", p)
        print(f"units: {len(ordered)}  ->  {_rel(out, root)}/units.md, coverage.md, exclusions.md, review/")
    return {"pack": pack, "coverage": cov, "units": ordered, "packets": packets}


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


def approve(region_id: str, reviewer: str, notes: str | None, root: Path = ROOT) -> int:
    cfg = load_yaml(root / "config/pack.yaml")
    readings = load_readings(root / cfg.get("readings_dir", "curation/readings"))
    if region_id not in readings:
        print(f"no reading for {region_id}")
        return 1
    reading, _ = readings[region_id]
    path = root / cfg.get("approvals", "curation/approvals.yaml")
    data = (load_yaml(path) or {}) if path.exists() else {}
    data.setdefault("approvals", []).append({
        "region_id": region_id, "reviewer": reviewer, "date": dt.date.today().isoformat(),
        "content_sha256": reading.content_sha256(), "notes": notes})
    path.write_text("# Human approvals of readings. Each entry pins the exact content approved.\n"
                    + yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"approved {region_id} by {reviewer}; content sha256 {reading.content_sha256()}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tenderpack")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("ingest")
    a.add_argument("--pack", default=str(ROOT / "config/pack.yaml"))
    a.add_argument("--out", default=str(ROOT / "build"))
    b = sub.add_parser("show")
    b.add_argument("unit_id")
    b.add_argument("--out", default=str(ROOT / "build"))
    c = sub.add_parser("approve")
    c.add_argument("region_id")
    c.add_argument("--reviewer", required=True)
    c.add_argument("--notes")
    args = ap.parse_args(argv)
    if args.cmd == "ingest":
        res = ingest(Path(args.pack), Path(args.out))
        return 0 if all(c["ok"] for c in res["coverage"]["checks"]) else 2
    if args.cmd == "show":
        return show(args.unit_id, Path(args.out))
    return approve(args.region_id, args.reviewer, args.notes)


if __name__ == "__main__":
    sys.exit(main())
