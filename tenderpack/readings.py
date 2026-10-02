"""Readings: human-verifiable transcriptions of regions that have no usable text layer.

A reading is a curated YAML file (curation/readings/<region_id>.yaml). It records:
  * where it came from: doc, page, bbox and the sha256 of the native image it was read from;
  * the content: for tables, direction (ltr/rtl), optional title/qualifier, columns (key,
    heading, lang), rows of cells with explicitly declared blanks, notes; for text and forms,
    lines with `source` (as printed; Arabic in logical Unicode order) and, separately,
    `translation`; for drawings (`graphic`), a description. Matching text (`normalized`) is
    computed here and never typed by hand;
  * declared numerals with the glyph order seen in the crop (`visual_ltr_expected`);
  * uncertainties, and who prepared it and how (AI-assisted preparation is stated as such).
Unknown fields are rejected (a misspelt field must not silently vanish).

Approval is never written into the reading itself, and the program never approves anything.
An approvals file (`curation/approvals.yaml`, written only by `tenderpack approve` on a
person's instruction) holds entries pinned to a *review subject* sha256 that covers:
  the whole reading (content, every uncertainty, source claims, who prepared it and how), and
  the evidence it was read from (source PDF sha256, region page, bbox and kind, native image sha256).
An entry counts only if it names an identified reviewer. Any change to the reading, its
uncertainties or the evidence (even with the transcription unchanged) makes it pending again.

Checks (each yields a finding; nothing is silently corrected):
  RD1  the region exists and doc/page/bbox agree with detection (0.5 pt tolerance)
  RD2  the native image sha256 matches the evidence the reading was made from
  RD3  table readings: grid detected from pixels has header+rows x columns that match the reading
  RD4  text readings: every text band is read and the declared bands exist (not for graphics)
  RD5  Arabic stored as logical letters (no presentation forms, no undeclared bidi controls);
       every Arabic line has a translation, kept separate
  RD6  every numeral in an Arabic line or Arabic/mixed table cell is declared, and rendering the
       stored text right to left (Latin expressions as left-to-right islands) reproduces the declared
       left-to-right glyph order of the crop. Result pass / PARTIAL (only digits, Latin and punctuation
       could be verified because the token holds Arabic letters) / fail
  RD7  (warning) text touching the image edge: the image may be cropped
  RD8  table structure: unique column and row keys; every row has exactly one cell per column;
       an empty cell only where the row declares it in `blank` (and a declared blank is empty)
  RD9  graphic readings carry a description
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Literal

import pymupdf
from pydantic import BaseModel, ConfigDict, Field

from . import arabic
from .regions import Region, detect_grid, image_array, text_bands
from .textnorm import _DIGITS, has_arabic, normalize_arabic, normalize_latin, numerals
from .util import load_yaml, sha256_text


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Numeral(_Strict):
    """A token containing digits whose rendered order must match the crop.

    text                 as stored in `source` or the cell (logical order)
    visual_ltr_expected  glyph order seen in the crop, left to right (e.g. "٢-٤" for logical "٤-٢")
    column               table rows only: the column key of the cell holding the token
    """
    column: str | None = None
    text: str
    visual_ltr_expected: str
    meaning: str
    crop_bbox_pt: list[float] | None = None
    uncertain: bool = False
    alternatives: list[str] = Field(default_factory=list)
    note: str | None = None


class BlockLine(_Strict):
    band: int
    side: Literal["full", "left", "right"] = "full"
    source: str
    numerals: list[Numeral] = Field(default_factory=list)
    uncertain: list[str] = Field(default_factory=list)


class Block(_Strict):
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


class Column(_Strict):
    key: str
    heading: str
    lang: Literal["ar", "en", "mixed"] = "en"


class Row(_Strict):
    key: str
    cells: dict[str, str]
    blank: list[str] = Field(default_factory=list)       # column keys whose cell is empty on the page
    numerals: list[Numeral] = Field(default_factory=list)
    uncertain: list[str] = Field(default_factory=list)


class TableReading(_Strict):
    direction: Literal["ltr", "rtl"] = "ltr"               # rtl: first column is the rightmost on the page
    title: Block | None = None
    qualifier: Block | None = None
    columns: list[Column]
    rows: list[Row]
    notes: list[Block] = Field(default_factory=list)


class SourceRef(_Strict):
    doc: str
    page: int
    bbox_pt: list[float]
    native_sha256: str | None = None


class Reading(_Strict):
    region_id: str
    unit_id: str
    title: str
    source: SourceRef
    content_type: Literal["table", "text", "form", "graphic"]
    languages: list[str]
    prepared_by: str
    method: str
    table: TableReading | None = None
    blocks: list[Block] = Field(default_factory=list)
    description: str | None = None                        # graphic readings: what the drawing shows
    uncertainties: list[str] = Field(default_factory=list)

    def all_blocks(self) -> list[Block]:
        if self.table is None:
            return list(self.blocks)
        t = self.table
        return [b for b in (t.title, t.qualifier) if b is not None] + list(t.notes)

    def column_of(self, key: str) -> Column | None:
        return next((c for c in self.table.columns if c.key == key), None) if self.table else None


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


_PLACEHOLDER = re.compile(r"^\s*(<[^>]*>|name|reviewer|your name|tbd|todo|n/?a|none|-+|\?+)\s*$", re.I)


def valid_reviewer(name) -> bool:
    """An approval must identify a person: a non-empty name that is not a template placeholder."""
    return isinstance(name, str) and bool(name.strip()) and not _PLACEHOLDER.match(name)


def review_subject(reading: Reading, region: Region, doc_sha256: str) -> dict:
    """What an approval covers: the whole reading plus the evidence it was read from."""
    evidence = {"doc": region.doc, "doc_sha256": doc_sha256, "page": region.page, "bbox": region.bbox,
                "kind": region.kind, "native_sha256": (region.native or {}).get("sha256")}
    body = {"reading": reading.model_dump(mode="json"), "evidence": evidence}
    return {"sha256": sha256_text(json.dumps(body, ensure_ascii=False, sort_keys=True)),
            "covers": "reading (content, uncertainties, source claims, preparer, method) + evidence "
                      "(source PDF sha256, region page/bbox/kind, native image sha256)",
            "evidence": evidence}


def review_status(reading: Reading, approvals: list[dict], subject: dict) -> dict:
    sha = subject["sha256"]
    mine = [a for a in approvals if a.get("region_id") == reading.region_id]
    match = [a for a in mine if a.get("subject_sha256") == sha]
    named = [a for a in match if valid_reviewer(a.get("reviewer"))]
    if named:
        a = named[-1]
        return {"status": "approved", "reviewer": a["reviewer"].strip(), "date": a.get("date"), "subject_sha256": sha}
    if match:
        return {"status": "pending", "reason": "approval entry does not identify a reviewer", "subject_sha256": sha}
    if mine:
        return {"status": "pending", "subject_sha256": sha,
                "reason": "the reading, its uncertainties or its evidence changed after the last approval"}
    return {"status": "pending", "reason": "not yet reviewed by a person", "subject_sha256": sha}


# ------------------------------------------------------------------ numbers in cells (no meaning attached)

_RANGE = re.compile(r"^\s*([0-9]+(?:\.[0-9]+)?)\s*[-–]\s*([0-9]+(?:\.[0-9]+)?)\s*$")
_NUM = re.compile(r"^\s*([0-9]+(?:\.[0-9]+)?)\s*$")


def numeric_reading(text: str) -> dict | None:
    """The numbers a cell shows, in logical order, and nothing more.

    '10' -> {form: single, values: [10.0]}; '0.5 - 1.0' -> {form: range, values: [0.5, 1.0]}.
    Arabic-Indic digits and the Arabic decimal separator are read as digits and '.'. Whether a
    value is a maximum, a minimum or a target is NOT decided here: the table's headings,
    qualifier and notes are carried beside it (`context`) for a person to interpret.
    """
    t = text.translate(_DIGITS).replace("٫", ".")
    m = _RANGE.match(t)
    if m:
        return {"form": "range", "values": [float(m.group(1)), float(m.group(2))], "text": text}
    m = _NUM.match(t)
    if m:
        return {"form": "single", "values": [float(m.group(1))], "text": text}
    return None


# ------------------------------------------------------------------ checks

def _grid_y_range(grid) -> tuple[float, float]:
    return (grid.h_lines[0], grid.h_lines[-1]) if grid and grid.h_lines else (0.0, -1.0)


def check_reading(reading: Reading, region: Region | None, pdf: pymupdf.Document | None) -> list[dict]:
    f: list[dict] = []

    def add(check, ok, detail, severity="error", result=None):
        result = result or ("pass" if ok else "fail")
        f.append({"check": check, "ok": bool(ok), "detail": detail, "result": result,
                  "severity": "partial" if result == "partial" else ("info" if ok else severity)})

    if region is None:
        add("RD1", False, f"region {reading.region_id} was not detected in this build")
        return f
    same = (region.doc == reading.source.doc and region.page == reading.source.page and
            len(reading.source.bbox_pt) == 4 and
            all(abs(a - b) <= 0.5 for a, b in zip(region.bbox, reading.source.bbox_pt)))
    add("RD1", same, f"region {region.doc} p{region.page} {region.bbox}; reading says "
                     f"{reading.source.doc} p{reading.source.page} {reading.source.bbox_pt}")
    if region.native:
        add("RD2", region.native["sha256"] == reading.source.native_sha256,
            f"native image sha256 {region.native['sha256'][:16]}…; reading made from {str(reading.source.native_sha256)[:16]}…")
    if reading.table is not None:
        _table_structure(reading, add)
    elif reading.content_type == "table":
        add("RD8", False, "content_type is table but the reading has no `table`")
    if reading.content_type == "graphic":
        add("RD9", bool(reading.description and reading.description.strip()) and not reading.blocks and reading.table is None,
            f"graphic reading: description {'present' if reading.description else 'MISSING'}; it records what the "
            "drawing shows and declares no text (a drawing with text needs a text or form reading)")
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

    if reading.content_type == "graphic":
        _table_numerals(reading, add)
        return f
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
                    res, how = arabic.visual_check(ln.source, n.visual_ltr_expected)
                    add("RD6", res != "fail", f"{blk.key} band {ln.band}: stored '{n.text}' -> rendered {how}; "
                                              f"crop shows '{n.visual_ltr_expected}' (left to right)", result=res)
    _table_numerals(reading, add)
    return f


def _table_structure(reading: Reading, add) -> None:
    """RD8: the rows and cells say exactly what the grid holds; blanks are recorded, not implied."""
    t = reading.table
    keys = [c.key for c in t.columns]
    problems = []
    for what, seq in (("column key", keys), ("column heading", [c.heading for c in t.columns]),
                      ("row key", [r.key for r in t.rows])):
        dup = sorted({k for k in seq if seq.count(k) > 1})
        if dup:
            problems.append(f"duplicate {what}(s) {dup}")
    for r in t.rows:
        missing = [k for k in keys if k not in r.cells]
        unknown = sorted(set(r.cells) - set(keys))
        empty = [k for k in keys if k in r.cells and not r.cells[k].strip()]
        if missing:
            problems.append(f"row {r.key}: missing cells {missing} (write every cell; an empty one as \"\" "
                            "and list it in `blank`)")
        if unknown:
            problems.append(f"row {r.key}: unknown cell keys {unknown}")
        undeclared = [k for k in empty if k not in r.blank]
        if undeclared:
            problems.append(f"row {r.key}: cells {undeclared} are blank but not declared in `blank`")
        not_empty = [k for k in r.blank if k in r.cells and r.cells[k].strip()]
        if not_empty:
            problems.append(f"row {r.key}: `blank` lists {not_empty} but those cells have text")
        bad = [k for k in r.blank if k not in keys] + [n.column for n in r.numerals if n.column not in keys]
        if bad:
            problems.append(f"row {r.key}: `blank`/numerals refer to unknown columns {bad}")
    add("RD8", not problems, f"{len(t.columns)} columns x {len(t.rows)} rows; "
                             f"{sum(len(r.blank) for r in t.rows)} declared blank cells; "
                             + ("; ".join(problems) if problems else "every row has exactly one cell per column"))


def _table_numerals(reading: Reading, add) -> None:
    """RD6 for table cells in Arabic or mixed columns: each cell is rendered right to left as printed."""
    if reading.table is None:
        return
    for r in reading.table.rows:
        for key, text in r.cells.items():
            col = reading.column_of(key)
            if col is None or (col.lang == "en" and not has_arabic(text)):
                continue
            found = [n["text"] for n in numerals(text)]
            decl = [n for n in r.numerals if n.column == key]
            declared = [x["text"] for d in decl for x in numerals(d.text)]
            undeclared = [x for x in found if x not in declared]
            add("RD6", not undeclared,
                f"row {r.key} cell {key}: numerals {found or 'none'}; undeclared {undeclared or 'none'}")
            for n in decl:
                res, how = arabic.visual_check(text, n.visual_ltr_expected)
                add("RD6", res != "fail", f"row {r.key} cell {key}: stored '{n.text}' -> rendered {how}; "
                                          f"crop shows '{n.visual_ltr_expected}' (left to right)", result=res)


# ------------------------------------------------------------------ units from readings

def reading_units(reading: Reading, region: Region, status: dict, evidence: dict) -> list[dict]:
    """Units derived from a reading. They carry origin=image_reading and the review status."""
    reading_ref = {"region": region.region_id, "status": status["status"],
                   "status_reason": status.get("reason"), "subject_sha256": status["subject_sha256"],
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
        title = t.title.source if t.title else None
        context = {"table_title": title, "column_headings": cols,
                   "qualifier": t.qualifier.source if t.qualifier else None,
                   "notes": [b.source for b in t.notes], "interpretation": None,
                   "interpretation_note": "not decided by the program: whether a number is a maximum, minimum, "
                                          "range or target is read from these headings and notes by a person"}
        top = dict(base, unit_id=reading.unit_id, kind="table", label=title or reading.title,
                   text=(title or reading.title) + (f" {t.qualifier.source}" if t.qualifier else ""),
                   table={"columns": cols, "title": title, "direction": t.direction,
                          "column_lang": {c.heading: c.lang for c in t.columns},
                          "qualifier": t.qualifier.source if t.qualifier else None},
                   anchors=[{"page": page, "bbox": region.bbox, "spans": []}])
        units.append(top)
        ncols = len(cols)
        # grid column on the page for logical column c: right to left tables start at the right
        grid_col = (lambda c: ncols - 1 - c) if t.direction == "rtl" else (lambda c: c)
        for i, row in enumerate(t.rows):
            cells = {c.heading: row.cells.get(c.key, "") for c in t.columns}
            u = dict(base, unit_id=f"{reading.unit_id}/{row.key}", kind="table_row", parent=reading.unit_id,
                     label=row.key, cells=cells,
                     text=" | ".join(f"{k}: {v}" for k, v in cells.items() if v),
                     anchors=[{"page": page, "bbox": evidence.get("row_bbox_pt", {}).get(i + 1, region.bbox),
                               "spans": [], "crop": evidence.get("row_crops", {}).get(i + 1), "grid_row": i + 1,
                               "cell_crops": {cols[c]: evidence.get("cell_crops", {}).get((i + 1, grid_col(c)))
                                              for c in range(ncols)},
                               "cell_bbox_pt": {cols[c]: evidence.get("cell_bbox_pt", {}).get((i + 1, grid_col(c)))
                                                for c in range(ncols)}}])
            if row.blank:
                u["blank"] = [reading.column_of(k).heading for k in row.blank if reading.column_of(k)]
            numeric = {c.heading: numeric_reading(row.cells.get(c.key, "")) for c in t.columns}
            numeric = {k: v for k, v in numeric.items() if v is not None}
            if numeric:
                u["numeric"] = numeric
            u["context"] = context
            if row.numerals:
                u["numerals"] = [n.model_dump(exclude_none=True) for n in row.numerals]
            if row.uncertain:
                u["uncertain"] = row.uncertain
            units.append(u)
        for blk in t.notes:
            units.append(block_unit(blk, f"{reading.unit_id}/{blk.key}", reading.unit_id))
    elif reading.content_type == "graphic":
        units.append(dict(base, unit_id=reading.unit_id, kind="graphic", label=reading.title,
                          text=reading.description or "", description=reading.description,
                          anchors=[{"page": page, "bbox": region.bbox, "spans": [],
                                    "crop": region.crop["path"] if region.crop else None}]))
    else:
        units.append(dict(base, unit_id=reading.unit_id, kind="image_text", label=reading.title, text=reading.title,
                          anchors=[{"page": page, "bbox": region.bbox, "spans": []}]))
        for blk in reading.blocks:
            units.append(block_unit(blk, f"{reading.unit_id}/{blk.key}", reading.unit_id))
    for u in units:
        u.setdefault("normalized", normalize_latin(u["text"]))
    return units
