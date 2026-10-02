"""Stage 1 pipeline: sources -> text + exclusions -> regions + evidence -> units -> readings -> coverage."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

from .extract import FurnitureRules, PageText, check_expected_counts, extract_page
from .regions import Region, detect_regions, save_region_evidence
from .segment import Segmenter, Unit
from .sources import Document, load_documents
from .util import ROOT, load_yaml


@dataclass
class DocResult:
    doc: Document
    pages: list[PageText]
    regions: list[Region]
    units: dict[str, Unit]
    order: list[str]
    span_unit: dict[str, str]
    problems: list[str] = field(default_factory=list)      # segmentation problems: fail C09
    duplicates: list[str] = field(default_factory=list)    # unit ids produced twice: fail C07
    notices: list[str] = field(default_factory=list)       # reported, not failures (e.g. page numbering)


@dataclass
class PackResult:
    root: Path
    out: Path
    docs: list[DocResult]
    furniture_problems: list[str]
    rules: FurnitureRules | None = None
    manifest: str = "sources/manifest.json"     # as named in the pack file (reported by C01)


def process_document(doc: Document, rules: FurnitureRules, out: Path, root: Path,
                     save_evidence: bool = True) -> DocResult:
    pdf = pymupdf.open(doc.path)
    pages = [extract_page(doc.doc_id, pdf[i], rules) for i in range(pdf.page_count)]
    regions: list[Region] = []
    for pt in pages:
        regions.extend(detect_regions(doc.doc_id, pdf[pt.page - 1], pt))
    if save_evidence:
        for g in regions:
            save_region_evidence(pdf, g, out / "regions", out)
    seg = Segmenter(doc.doc_id, pdf, pages, regions)
    units = seg.run()
    notices = [f"{doc.doc_id} p{pt.page}: printed page '{pt.printed_page}' differs from PDF page"
               for pt in pages if pt.printed_page is not None and pt.printed_page != str(pt.page)]
    return DocResult(doc, pages, regions, units, seg.order, seg.span_unit, list(seg.problems),
                     list(seg.duplicates), notices)


def run_pack(pack_path: Path = ROOT / "config/pack.yaml", out: Path = ROOT / "build",
             root: Path = ROOT, save_evidence: bool = True) -> PackResult:
    cfg = load_yaml(pack_path)
    docs = load_documents(cfg, root)
    rules = FurnitureRules.from_file(root / cfg["furniture"])
    results = [process_document(d, rules, out, root, save_evidence) for d in docs]
    furn = check_expected_counts([p for r in results for p in r.pages], rules)
    return PackResult(root, out, results, furn, rules, str(cfg["manifest"]))
