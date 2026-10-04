"""Output writers for the deliverables: A1 (JSON, CSV, Excel), plain CSV/JSON tables (A2, A5) and
the one-page A3 PDF. Presentation only: every writer takes plain data and adds nothing to it.

Determinism. Writing the same input twice, in any directory, at any time, gives identical bytes.
  JSON  util.dump_json (sorted keys, fixed separators).
  CSV   UTF-8 with BOM (so Excel reads Arabic correctly), "\\r\\n" line ends, every value as text.
  XLSX  openpyxl stamps the save time into docProps/core.xml and into every zip entry. The
        workbook properties are fixed, core.xml is serialised again after saving, and the zip is
        rewritten with fixed entry times, attributes and order, using the same (deflate) compression.
  PDF   fixed metadata and no /ID; fonts come from PyMuPDF's bundled set (never system fonts) and
        are subset by MuPDF, whose subset prefixes depend only on the content.

Arabic in A3. MuPDF 1.28 ignores dir="rtl" on an inline <span> (checked by rendering), so the span
also carries an RLE...PDF embedding. Latin expressions inside Arabic text ("4-C") are embedded left to
right (arabic.display_form), and LRM marks keep the neighbouring quotes and separators in the
left-to-right line. Text whose first strong character is Arabic is laid out right to left as a
whole; English text keeps its order and only its Arabic runs are laid out right to left. The
controls exist only in the HTML handed to MuPDF; stored text is never changed.
"""
from __future__ import annotations

import csv
import html
import io
import re
import unicodedata
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

import pymupdf
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.xml.functions import tostring

from .arabic import display_form
from .util import dump_json, r1

FIXED_TIME = datetime(2026, 10, 1, 0, 0, 0)       # workbook created/modified
PDF_DATE = "D:20261001000000Z"
PRODUCER = "tenderpack"
ZIP_TIME = (1980, 1, 1, 0, 0, 0)                   # earliest time a zip entry can carry
A1_SHEET = "A1 register"
A1_HEADER_ROW = 4                                  # rows 1-2: banner; row 3: blank
A3_SCALE_LOW = 0.9                                 # 8.5 pt body text never drops below 7.6 pt; else: prioritise
A3_MIN_TEXT_PT = 7.5                               # smallest rendered text allowed on A3 (C43)


# ------------------------------------------------------------------ values as text

def cell_text(value: Any) -> str:
    """A value as CSV text: None -> "", bool -> TRUE/FALSE, lists joined with "; "."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (list, tuple)):
        return "; ".join(cell_text(v) for v in value)
    if isinstance(value, (str, int, float)):
        return str(value)
    # anything else (dict, set, ...) has no agreed text form, and a set's order is not stable
    raise TypeError(f"unsupported cell value of type {type(value).__name__}: {value!r}")


def _xlsx_value(value: Any) -> Any:
    """Numbers and booleans stay typed in Excel; lists are joined like in the CSV."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    return cell_text(value)


def _columns(table: dict) -> list[dict]:
    cols = table["columns"]
    keys = [c["key"] for c in cols]
    dup = sorted({k for k in keys if keys.count(k) > 1})
    if dup:
        raise ValueError(f"duplicate column keys: {dup}")
    return cols


# ------------------------------------------------------------------ CSV and JSON

def _csv_bytes(table: dict) -> bytes:
    cols = _columns(table)
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow([c["header"] for c in cols])
    for row in table["rows"]:
        w.writerow([cell_text(row.get(c["key"])) for c in cols])
    return buf.getvalue().encode("utf-8-sig")


def write_csv_json(table: dict, out_dir: Path, stem: str) -> list[Path]:
    """`stem.csv` (declared columns only) and `stem.json` (the whole table) in out_dir."""
    out_dir = Path(out_dir)
    data = _csv_bytes(table)                       # fails before anything is written
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = [out_dir / f"{stem}.csv", out_dir / f"{stem}.json"]
    paths[0].write_bytes(data)
    dump_json(table, paths[1])
    return paths


# ------------------------------------------------------------------ A1: Excel

STATUS_FILLS = (                                   # first match wins
    (lambda v: v.startswith(("DELETED", "REMOVED")), "D9D9D9"),
    (lambda v: "STALE" in v, "FCE4D6"),
    (lambda v: v.startswith(("NEW", "REINSTATED")), "E2EFDA"),
    (lambda v: v.startswith("AMENDED"), "FFF2CC"),
    (lambda v: v.startswith("NOT ISSUED"), "F2F2F2"),
)
WRAP_TOP = Alignment(wrap_text=True, vertical="top")
HEADER_BORDER = Border(bottom=Side(style="thin"))


def status_fill(value: Any) -> str | None:
    """Fill colour (RRGGBB) of a per-stage status cell, or None."""
    text = cell_text(value).strip()
    return next((rgb for test, rgb in STATUS_FILLS if test(text)), None)


def _is_status_column(col: dict) -> bool:
    # per-stage status columns: header "status:..." as specified; key "status:..." when the header is prose
    return col["header"].startswith("status:") or col["key"].startswith("status:")


def _write_table(ws, cols: list[dict], rows: list[dict], header_row: int, styled: bool) -> None:
    """Header, rows, widths, frozen header and autofilter. `styled`: status fills and pending italics."""
    for c, col in enumerate(cols, 1):
        cell = ws.cell(header_row, c, col["header"])
        cell.font, cell.alignment, cell.border = Font(bold=True), WRAP_TOP, HEADER_BORDER
        ws.column_dimensions[get_column_letter(c)].width = col["width"]
    for r, row in enumerate(rows, header_row + 1):
        for c, col in enumerate(cols, 1):
            value = row.get(col["key"])
            cell = ws.cell(r, c, _xlsx_value(value))
            if isinstance(cell.value, str):
                cell.data_type = "s"               # text such as "=..." or "#N/A" stays text
            cell.alignment = WRAP_TOP
            if not styled:
                continue
            if _is_status_column(col) and (rgb := status_fill(value)):
                cell.fill = PatternFill(fill_type="solid", fgColor=rgb)
            if "status" in col["key"].lower() and "pending" in cell_text(value).lower():
                cell.font = Font(italic=True)
    last = get_column_letter(max(len(cols), 1))
    ws.freeze_panes = ws.cell(header_row + 1, 1).coordinate
    ws.auto_filter.ref = f"A{header_row}:{last}{header_row + len(rows)}"


def _a1_workbook(a1: dict) -> Workbook:
    wb = Workbook()
    p = wb.properties
    p.creator = p.lastModifiedBy = PRODUCER
    p.created = p.modified = FIXED_TIME
    p.title = a1["title"]
    ws = wb.active
    ws.title = A1_SHEET
    ws["A1"] = a1["title"]
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = a1["notice"]
    ws["A2"].font = Font(italic=True)
    _write_table(ws, _columns(a1), a1["rows"], A1_HEADER_ROW, styled=True)
    for name, sheet in a1.get("sheets", {}).items():
        if name == A1_SHEET:
            raise ValueError(f"extra sheet may not be named {A1_SHEET!r}")
        _write_table(wb.create_sheet(name), _columns(sheet), sheet["rows"], 1, styled=False)
    return wb


def _xlsx_bytes(wb: Workbook) -> bytes:
    """Save, then rewrite the zip so that nothing depends on when or where it was written."""
    raw = io.BytesIO()
    wb.save(raw)                                   # stamps properties.modified with the time now
    wb.properties.modified = FIXED_TIME
    core = tostring(wb.properties.to_tree())       # serialised exactly as openpyxl's writer does
    out = io.BytesIO()
    with zipfile.ZipFile(raw) as src, zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as dst:
        names = sorted(src.namelist(), key=lambda n: (n != "[Content_Types].xml", n))
        for name in names:
            info = zipfile.ZipInfo(name, date_time=ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 0                 # not the writing platform's
            info.external_attr = 0
            dst.writestr(info, core if name == "docProps/core.xml" else src.read(name))
    return out.getvalue()


def write_a1(a1: dict, out_dir: Path) -> list[Path]:
    """`a1.json`, `a1.csv` (main rows) and `a1.xlsx` (register plus extra sheets) in out_dir."""
    out_dir = Path(out_dir)
    csv_data = _csv_bytes(a1)                      # build everything before writing anything
    xlsx_data = _xlsx_bytes(_a1_workbook(a1))
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = [out_dir / "a1.json", out_dir / "a1.csv", out_dir / "a1.xlsx"]
    dump_json(a1, paths[0])
    paths[1].write_bytes(csv_data)
    paths[2].write_bytes(xlsx_data)
    return paths


# ------------------------------------------------------------------ A3: one-page PDF

class A3OverflowError(ValueError):
    """A3 does not fit on one A4 page at scale >= A3_SCALE_LOW. Nothing is written: the content
    has to be prioritised by a person, never dropped or moved to a second page."""


LRM, RLE, POP = "\u200e", "\u202b", "\u202c"
SEP = " \u00b7 "                                  # between source, confidence and flags
_ARABIC = re.compile("[\u0600-\u06ff]")
_ARABIC_RUN = re.compile("[\u0600-\u06ff](?:[^A-Za-z]*[\u0600-\u06ff])?")   # no Latin letter inside

A3_PAGE = pymupdf.paper_rect("a4")
A3_MARGIN_X, A3_MARGIN_Y, A3_FOOTER_H = 26, 20, 26
A3_CSS = """
body {font-family: sans-serif; font-size: 8.5px; line-height: 1.16; color: #000}
.title {font-size: 13px; font-weight: bold; margin: 0 0 1px 0}
.sub {color: #333; margin: 0 0 4px 0}
.banner {background-color: #e3e3e3; border: 0.5px solid #8c8c8c; padding: 2px 5px; font-weight: bold;
         margin: 0 0 5px 0}
h2 {font-size: 9.5px; font-weight: bold; border-bottom: 0.5px solid #8c8c8c; margin: 6px 0 2px 0;
    padding: 0 0 1px 0}
p {margin: 0 0 1.5px 0}
.note {font-style: italic; color: #444}
.it {padding-left: 9px; text-indent: -9px}
.meta {color: #444}
.flag {color: #b00000; font-size: 8.5px}
.ids {font-size: 8.5px; color: #222}
a {color: #000; text-decoration: none}
.none {color: #444; font-style: italic}
"""
A3_FOOTER_CSS = """
body {font-family: sans-serif; font-size: 8.5px; line-height: 1.2; color: #444}
.foot {border-top: 0.5px solid #8c8c8c; padding-top: 2px}
"""


def _esc(text: str) -> str:
    return html.escape(text, quote=False)


def _first_strong_rtl(text: str) -> bool:
    for ch in text:
        b = unicodedata.bidirectional(ch)
        if b in ("R", "AL"):
            return True
        if b == "L":
            return False
    return False


def _rtl(text: str) -> str:
    """One right-to-left run inside the left-to-right page (see module docstring)."""
    return f'{LRM}<span dir="rtl">{RLE}{_esc(display_form(text))}{POP}</span>{LRM}'


def _rich(text: str) -> str:
    """Escaped HTML for one field, with any Arabic laid out right to left."""
    text = text or ""
    if not _ARABIC.search(text):
        return _esc(text)
    if _first_strong_rtl(text):
        return _rtl(text)
    out, pos = [], 0
    for m in _ARABIC_RUN.finditer(text):
        out += [_esc(text[pos:m.start()]), _rtl(m.group(0))]
        pos = m.end()
    return "".join(out) + _esc(text[pos:])


def _a3_item(it: dict) -> str:
    """Bold id (linked to a3_detail.html), text, class: "consequence" (proposed translation), source, confidence,
    flags in red. A compact item leaves the quotation to the detail page."""
    parts = [f'<b><a href="a3_detail.html#{_esc(it["id"])}">{_esc(it["id"])}</a></b> {_rich(it["text"])}']
    if it.get("consequence") and not it.get("compact"):
        cls = f"<i>{_esc(it['class'])}</i>: " if it.get("class") else ""
        parts.append(f"\u2014 {cls}\u201c{_rich(it['consequence'])}\u201d")
        if it.get("gloss"):
            parts.append(f"(proposed translation, not reviewed: \u2018{_esc(it['gloss'])}\u2019)")
    meta = [_rich(it["source"])] if it.get("source") else []
    if it.get("confidence"):
        meta.append(f"confidence {_rich(it['confidence'])}")
    if it.get("owner"):
        meta.append(f"owner: {_rich(it['owner'])}")
    if meta:
        parts.append(f'<span class="meta">[{SEP.join(meta)}]</span>')
    if it.get("flags"):
        parts.append(f'<span class="flag">{SEP.join(_rich(f) for f in it["flags"])}</span>')
    return f'<p class="it">{" ".join(parts)}</p>'


def _a3_html(a3: dict) -> str:
    out = [f'<div class="title">{_rich(a3["title"])}</div>']
    if a3.get("subtitle"):
        out.append(f'<div class="sub">{_rich(a3["subtitle"])}</div>')
    if a3.get("banner"):
        out.append(f'<div class="banner">{_rich(a3["banner"])}</div>')
    tail = [] if a3.get("groups") else [*([a3["missing"]] if a3.get("missing") else []), a3["unresolved"]]
    for sec in [*a3["sections"], *tail]:
        out.append(f"<h2>{_rich(sec['heading'])}</h2>")
        if sec.get("note"):
            out.append(f'<p class="note">{_rich(sec["note"])}</p>')
        if sec.get("ids"):
            own = sec.get("owners") or {}
            out.append('<p class="ids">' + ", ".join(f'<a href="a3_detail.html#{_esc(i)}">{_esc(i)}</a>'
                                                     + (f' <span class="meta">({_esc(own[i])})</span>' if own.get(i) else "")
                                                     for i in sec["ids"]) + "</p>")
            continue
        if "ids" in sec and not sec.get("items"):
            continue
        out += [_a3_item(it) for it in sec["items"]] or ['<p class="none">None.</p>']
    if a3.get("groups"):
        g = a3["groups"]
        out.append(f"<h2>{_rich(g['heading'])}</h2>")
        if g.get("note"):
            out.append(f'<p class="note">{_rich(g["note"])}</p>')
        link = lambda i: f'<a href="a3_detail.html#{_esc(i)}"><b>{_esc(i)}</b></a>'  # noqa: E731
        for grp in g["groups"]:
            items = [link(i["id"]) + (f" {_rich(i['short'])}" if i.get("short") else "")
                     for i in grp["items"]]
            qs = (f' <span class="meta">questions drafted: {", ".join(link(q) for q in grp["questions"])}</span>'
                  if grp.get("questions") else "")
            if "count" in grp:                     # condensed to a count (stage2.condense_a3 level 3): ids on a3_detail.html
                qs = f' <span class="meta">questions drafted: {grp["n_questions"]}</span>' if grp.get("n_questions") else ""
                out.append(f'<p class="it"><b>{_rich(grp["title"])}</b> ({grp["count"]})' + qs + "</p>")
                continue
            out.append(f'<p class="it"><b>{_rich(grp["title"])}</b> ({len(grp["items"])}): ' + "; ".join(items) + qs + "</p>")
    return "\n".join(out)


def write_a3_pdf(a3: dict, path: Path) -> dict:
    """Render A3 on exactly one A4 portrait page, scaled down to at most A3_SCALE_LOW if needed.

    Returns {"pages": 1, "scale": s, "spare_pt": h}: s = 1.0 means no scaling; h is the unused height
    below the content. Raises A3OverflowError, and writes nothing, if it does not fit.
    """
    w, h = A3_PAGE.width, A3_PAGE.height
    doc = pymupdf.open()
    page = doc.new_page(width=w, height=h)
    body = pymupdf.Rect(A3_MARGIN_X, A3_MARGIN_Y, w - A3_MARGIN_X, h - A3_MARGIN_Y - A3_FOOTER_H - 4)
    # insert_htmlbox places everything or nothing: (-1, scale) when even scale_low does not fit
    spare, scale = page.insert_htmlbox(body, _a3_html(a3), css=A3_CSS, scale_low=A3_SCALE_LOW)
    if spare < 0 or scale < A3_SCALE_LOW or round(8.5 * scale, 2) < A3_MIN_TEXT_PT:
        raise A3OverflowError(f"A3 content does not fit on one A4 page at scale >= {A3_SCALE_LOW} "
                              f"({sum(len(s['items']) for s in a3['sections'])} items, "
                              f"{len((a3.get('unresolved') or {}).get('items') or [])} unresolved); shorten or prioritise it")
    foot = pymupdf.Rect(A3_MARGIN_X, h - A3_MARGIN_Y - A3_FOOTER_H, w - A3_MARGIN_X, h - A3_MARGIN_Y)
    fspare, _ = page.insert_htmlbox(foot, f'<div class="foot">{_rich(a3.get("footer", ""))}</div>',
                                    css=A3_FOOTER_CSS, scale_low=A3_SCALE_LOW)
    if fspare < 0:
        raise A3OverflowError(f"A3 footer does not fit in {A3_FOOTER_H} pt at scale >= {A3_SCALE_LOW}")
    assert doc.page_count == 1
    doc.subset_fonts()
    doc.set_metadata({"title": a3["title"], "creator": PRODUCER, "producer": PRODUCER,
                      "creationDate": PDF_DATE, "modDate": PDF_DATE})
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = doc.tobytes(garbage=3, deflate=True, no_new_id=True)
    doc.close()
    # Relative hrefs come out as /Launch actions, which many viewers block. The links only become visible after
    # a save, so reopen and rewrite them as /URI actions (resolved relative to the PDF), then write once.
    doc = pymupdf.open("pdf", data)
    page = doc[0]

    def launch_links():
        return [ln for ln in page.get_links() if ln.get("kind") in (pymupdf.LINK_LAUNCH, pymupdf.LINK_GOTOR)
                and "/Launch" in doc.xref_object(ln["xref"])]
    todo = [(ln["from"], (ln.get("file") or "").replace("%23", "#")) for ln in launch_links()]
    while launch_links():                                  # one at a time: deleting invalidates the list
        page.delete_link(launch_links()[0])
    for rect, target in todo:
        page.insert_link({"kind": pymupdf.LINK_URI, "from": rect, "uri": target})
    path.write_bytes(doc.tobytes(garbage=3, deflate=True, no_new_id=True))
    doc.close()
    return {"pages": 1, "scale": round(scale, 3), "spare_pt": r1(spare), "min_text_pt": round(8.5 * scale, 2)}
