"""Readings: human-verifiable transcriptions of regions that have no usable text layer.

A reading is a curated YAML file (curation/readings/<region_id>.yaml). It records:
  * where it came from: doc, page, bbox and the sha256 of the native image it was read from;
  * the content: for tables, title, columns (heading + key), rows of cells, notes; for text and
    forms, lines with `source` (as printed; Arabic in logical Unicode order) and, separately,
    `translation`. Matching text (`normalized`) is computed here and never typed by hand;
  * declared numerals with the glyph order seen in the crop (`visual_ltr_expected`);
  * uncertainties, and who prepared it and how (AI-assisted preparation is stated as such).

Approval is never written into the reading itself. `curation/approvals.yaml` holds approvals,
each pinned to the sha256 of the reading content it approved. If the content changes after
approval, the approval no longer matches and the reading is pending again.

Checks (each yields a finding; nothing is silently corrected):
  RD1  the region exists and doc/page/bbox agree with detection (0.5 pt tolerance)
  RD2  the native image sha256 matches the evidence the reading was made from
  RD3  table readings: grid detected from pixels has header+rows x columns that match the reading
  RD4  text readings: the declared bands exist in the detected text-band list
  RD5  Arabic stored as logical letters (no presentation forms, no undeclared bidi controls);
       every Arabic line has a translation, kept separate
  RD6  every numeral in an Arabic line is declared, and rendering the stored text reproduces the
       declared left-to-right glyph order seen in the crop
  RD7  approval status: approved only if an approval entry matches the current content sha256
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Literal

import pymupdf
from pydantic import BaseModel, Field

from . import arabic
from .regions import Region, detect_grid, image_array, text_bands
from .textnorm import has_arabic, normalize_arabic, normalize_latin, numerals
from .util import load_yaml, sha256_text


class Numeral(BaseModel):
    """A token containing digits whose rendered order must match the crop.

    text                 as stored in `source` (logical order)
    visual_ltr_expected  glyph order seen in the crop, left to right (e.g. "٢-٤" for logical "٤-٢")
    """
    text: str
    visual_ltr_expected: str
    meaning: str
    crop_bbox_pt: list[float] | None = None
    uncertain: bool = False
    alternatives: list[str] = Field(default_factory=list)
    note: str | None = None


class BlockLine(BaseModel):
    band: int
    side: Literal["full", "left", "right"] = "full"
    source: str
    numerals: list[Numeral] = Field(default_factory=list)
    uncertain: list[str] = Field(default_factory=list)


class Block(BaseModel):
    """One logical piece of text (a heading, a declaration, a field label) over one or more lines."""
    key: str
    lang: Literal["ar", "en", "mixed"]
    role: str | None = None
    translation: str | None = None
    lines: list[BlockLine]
    uncertain: list[str] = Field(default_factory=list)

    @property
    def source(self) -> str:
        return " ".join(ln.source for ln in self.lines)


class Column(BaseModel):
    key: str
    heading: str


class Row(BaseModel):
    key: str
    cells: dict[str, str]
    uncertain: list[str] = Field(default_factory=list)


class TableReading(BaseModel):
    title: Block
    qualifier: Block | None = None
    columns: list[Column]
    rows: list[Row]
    notes: list[Block] = Field(default_factory=list)


class SourceRef(BaseModel):
    doc: str
    page: int
    bbox_pt: list[float]
    native_sha256: str | None = None


class Reading(BaseModel):
    region_id: str
    unit_id: str
    title: str
    source: SourceRef
    content_type: Literal["table", "text", "form"]
    languages: list[str]
    prepared_by: str
    method: str
    table: TableReading | None = None
    blocks: list[Block] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)

    def content_sha256(self) -> str:
        body = {"unit_id": self.unit_id, "table": self.table.model_dump() if self.table else None,
                "blocks": [b.model_dump() for b in self.blocks]}
        return sha256_text(json.dumps(body, ensure_ascii=False, sort_keys=True))

    def all_blocks(self) -> list[Block]:
        if self.table is None:
            return list(self.blocks)
        return [self.table.title] + ([self.table.qualifier] if self.table.qualifier else []) + list(self.table.notes)


def load_readings(directory: Path) -> dict[str, tuple[Reading, Path]]:
    out = {}
    if not directory.exists():
        return out
    for p in sorted(directory.glob("*.yaml")):
        r = Reading.model_validate(load_yaml(p))
        out[r.region_id] = (r, p)
    return out


def load_approvals(path: Path) -> list[dict]:
    if not path.exists():
        return []
    data = load_yaml(path) or {}
    return data.get("approvals", [])


def review_status(reading: Reading, approvals: list[dict]) -> dict:
    sha = reading.content_sha256()
    mine = [a for a in approvals if a.get("region_id") == reading.region_id]
    match = [a for a in mine if a.get("content_sha256") == sha]
    if match:
        a = match[-1]
        return {"status": "approved", "reviewer": a.get("reviewer"), "date": a.get("date"),
                "content_sha256": sha}
    if mine:
        return {"status": "pending", "reason": "content changed after the last approval", "content_sha256": sha}
    return {"status": "pending", "reason": "not yet reviewed by a person", "content_sha256": sha}


# ------------------------------------------------------------------ parsing table values

_RANGE = re.compile(r"^\s*([0-9]+(?:\.[0-9]+)?)\s*[-–]\s*([0-9]+(?:\.[0-9]+)?)\s*$")
_NUM = re.compile(r"^\s*([0-9]+(?:\.[0-9]+)?)\s*$")


def parse_limit(text: str) -> dict | None:
    """'10' -> {max: 10}; '0.5 - 1.0' -> {min: 0.5, max: 1.0}. The header says values are maxima."""
    m = _RANGE.match(text)
    if m:
        return {"min": float(m.group(1)), "max": float(m.group(2)), "rule": "range a - b"}
    m = _NUM.match(text)
    if m:
        return {"max": float(m.group(1)), "rule": "single value read as a maximum (table header: 'all values are maxima')"}
    return None


# ------------------------------------------------------------------ checks

def _grid_y_range(grid) -> tuple[float, float]:
    return (grid.h_lines[0], grid.h_lines[-1]) if grid and grid.h_lines else (0.0, -1.0)


def check_reading(reading: Reading, region: Region | None, pdf: pymupdf.Document | None) -> list[dict]:
    f: list[dict] = []

    def add(check, ok, detail, severity="error"):
        f.append({"check": check, "ok": bool(ok), "detail": detail, "severity": "info" if ok else severity})

    if region is None:
        add("RD1", False, f"region {reading.region_id} was not detected in this build")
        return f
    same = (region.doc == reading.source.doc and region.page == reading.source.page and
            all(abs(a - b) <= 0.5 for a, b in zip(region.bbox, reading.source.bbox_pt)))
    add("RD1", same, f"region {region.doc} p{region.page} {region.bbox}; reading says "
                     f"{reading.source.doc} p{reading.source.page} {reading.source.bbox_pt}")
    if region.native:
        add("RD2", region.native["sha256"] == reading.source.native_sha256,
            f"native image sha256 {region.native['sha256'][:16]}…; reading made from {str(reading.source.native_sha256)[:16]}…")
    if pdf is None:
        return f
    gray = image_array(pdf, region)
    grid = None
    if reading.table is not None:
        grid = detect_grid(gray)
        want_rows, want_cols = len(reading.table.rows) + 1, len(reading.table.columns)
        add("RD3", grid.rows == want_rows and grid.cols == want_cols,
            f"grid from pixels: {len(grid.h_lines)} horizontal x {len(grid.v_lines)} vertical rules = "
            f"{grid.rows} rows x {grid.cols} cols (skew {grid.skew_deg} deg); reading: header + "
            f"{len(reading.table.rows)} rows x {want_cols} columns")

    # RD4: every text band (each side of a split band) is read; nothing refers to a missing or rule band
    bands = text_bands(gray)
    gy0, gy1 = _grid_y_range(grid)
    need = set()
    for b in bands:
        if b["kind"] != "text":
            continue
        cy = (b["y0"] + b["y1"]) / 2
        if gy0 - 15 <= cy <= gy1 + 15:
            continue                                    # inside the table grid: covered by cells
        if b["split_x"] is not None:
            need |= {(b["index"], "left"), (b["index"], "right")}
        else:
            need.add((b["index"], "full"))
    used, bad = set(), []
    for blk in reading.all_blocks():
        for ln in blk.lines:
            used.add((ln.band, ln.side))
            if ln.band >= len(bands) or bands[ln.band]["kind"] != "text":
                bad.append(f"{blk.key}: band {ln.band} is not a text band")
            elif ln.side != "full" and bands[ln.band]["split_x"] is None:
                bad.append(f"{blk.key}: band {ln.band} has no left/right split")
    # RD7 (warning): text touching the image edge suggests the image was cropped from something larger
    H, W = gray.shape
    edge = [b["index"] for b in bands if b["kind"] == "text" and
            (b["y0"] <= 3 or b["y1"] >= H - 3 or b["x0"] <= 3 or b["x1"] >= W - 3)]
    f.append({"check": "RD7", "ok": True, "severity": "warning" if edge else "info",
              "detail": (f"text bands {edge} touch the image edge ({W}x{H} px): content may continue beyond the image; "
                         "cannot be established from the pack") if edge else "no text touches the image edge"})
    unread = sorted(need - used)
    add("RD4", not unread and not bad,
        f"{sum(1 for b in bands if b['kind'] == 'text')} text bands and {sum(1 for b in bands if b['kind'] == 'rule')} "
        f"rule bands detected; outside-grid text segments needing a reading: {len(need)}; "
        f"unread: {unread or 'none'}" + (f"; problems: {bad}" if bad else ""))

    for blk in reading.all_blocks():
        if blk.lang in ("ar", "mixed"):
            add("RD5", bool(blk.translation),
                f"{blk.key}: translation {'present' if blk.translation else 'MISSING'} (stored separately from source)")
        for ln in blk.lines:
            if blk.lang in ("ar", "mixed"):
                probs = arabic.storage_problems(ln.source)
                add("RD5", not probs and has_arabic(ln.source),
                    f"{blk.key} band {ln.band}: " + ("; ".join(probs) or "stored as logical Unicode Arabic letters"))
                found = [n["text"] for n in numerals(ln.source)]
                declared_digits = [n["text"] for d in ln.numerals for n in numerals(d.text)]
                undeclared = [x for x in found if x not in declared_digits]
                add("RD6", not undeclared,
                    f"{blk.key} band {ln.band}: numerals in source {found or 'none'}; undeclared {undeclared or 'none'}")
                for n in ln.numerals:
                    ok, how = arabic.visual_check(ln.source, n.visual_ltr_expected)
                    add("RD6", ok, f"{blk.key} band {ln.band}: stored '{n.text}' -> rendered {how}; "
                                   f"crop shows '{n.visual_ltr_expected}' (left to right)")
    return f


# ------------------------------------------------------------------ units from readings

def reading_units(reading: Reading, region: Region, status: dict, evidence: dict) -> list[dict]:
    """Units derived from a reading. They carry origin=image_reading and the review status."""
    reading_ref = {"region": region.region_id, "status": status["status"],
                   "status_reason": status.get("reason"), "content_sha256": status["content_sha256"],
                   "prepared_by": reading.prepared_by}
    base = {"doc": reading.source.doc, "origin": "image_reading", "pages": [reading.source.page],
            "region": region.region_id, "reading": reading_ref}
    page = reading.source.page

    def line_anchor(ln: BlockLine) -> dict:
        key = (ln.band, ln.side)
        return {"page": page, "bbox": evidence.get("band_bbox_pt", {}).get(key, region.bbox), "spans": [],
                "crop": evidence.get("band_crops", {}).get(key)}

    def block_unit(blk: Block, uid: str, parent: str) -> dict:
        u = dict(base, unit_id=uid, kind="reading_block", parent=parent, label=blk.key, lang=blk.lang,
                 role=blk.role, text=blk.source, anchors=[line_anchor(ln) for ln in blk.lines])
        u["normalized"] = normalize_latin(blk.source) if blk.lang == "en" else normalize_arabic(blk.source)
        if blk.translation:
            u["translation"] = blk.translation
        unc = list(blk.uncertain) + [x for ln in blk.lines for x in ln.uncertain]
        unc += [f"numeral '{n.text}': {n.note or 'uncertain'}" for ln in blk.lines for n in ln.numerals if n.uncertain]
        if unc:
            u["uncertain"] = unc
        return u

    units = []
    if reading.table is not None:
        t = reading.table
        cols = [c.heading for c in t.columns]
        top = dict(base, unit_id=reading.unit_id, kind="table", label=t.title.source,
                   text=t.title.source + (f" {t.qualifier.source}" if t.qualifier else ""),
                   table={"columns": cols, "title": t.title.source,
                          "qualifier": t.qualifier.source if t.qualifier else None},
                   anchors=[{"page": page, "bbox": region.bbox, "spans": []}])
        units.append(top)
        for i, row in enumerate(t.rows):
            cells = {c.heading: row.cells.get(c.key, "") for c in t.columns}
            u = dict(base, unit_id=f"{reading.unit_id}/{row.key}", kind="table_row", parent=reading.unit_id,
                     label=row.key, cells=cells, text=" | ".join(f"{k}: {v}" for k, v in cells.items() if v),
                     anchors=[{"page": page, "bbox": evidence.get("row_bbox_pt", {}).get(i + 1, region.bbox),
                               "spans": [], "crop": evidence.get("row_crops", {}).get(i + 1),
                               "cell_crops": {cols[c]: evidence.get("cell_crops", {}).get((i + 1, c))
                                              for c in range(len(cols))}}])
            if "limit" in row.cells:
                u["parsed"] = {"limit": parse_limit(row.cells["limit"]), "unit": row.cells.get("unit"),
                               "basis": row.cells.get("basis")}
            if row.uncertain:
                u["uncertain"] = row.uncertain
            units.append(u)
        for blk in t.notes:
            units.append(block_unit(blk, f"{reading.unit_id}/{blk.key}", reading.unit_id))
    else:
        units.append(dict(base, unit_id=reading.unit_id, kind="image_text", label=reading.title, text=reading.title,
                          anchors=[{"page": page, "bbox": region.bbox, "spans": []}]))
        for blk in reading.blocks:
            units.append(block_unit(blk, f"{reading.unit_id}/{blk.key}", reading.unit_id))
    for u in units:
        u.setdefault("normalized", normalize_latin(u["text"]))
    return units
