"""Content spans -> source units with stable IDs.

Every content span is assigned to exactly one unit (checked by coverage.py). Recognisers,
in order of precedence, each based on style and pattern rather than page coordinates:

  heading      bold Helvetica >= 10 pt (consecutive heading lines merge)
  caption      bold Helvetica line beginning "Table N-N" -> titles the next table (also across a page break)
  table        ruled grid (PyMuPDF find_tables, strategy=lines); cell text comes from our own content
               spans, so excluded furniture (the watermark) never leaks into cells. A table continues
               the previous one across a page break only if nothing came between them (no text,
               heading, caption, region or rotated text after the earlier part), it is the first item
               on the next page, its column edges match, and its header row (if any) repeats the
               earlier header. Matching columns alone never join two tables.
  footnote     small text at the page foot starting with a number that matches a superscript marker
  clause       line opening with a bold number such as 8.5 / 2.1
  list item    "(a)" / "(iv)" opening a line, inside a clause or list whose text so far ends ":", ";",
               ",", "and" or "or" (a list item may also end "." when it closes a sentence)
  note         "Notes to Table ..." block; "(1)" items inside it
  numbered     "1. Having examined ..." paragraphs (not bold), e.g. form paragraphs. A number at the
               start of a line opens a numbered paragraph only if it is in sequence (1, or one more
               than the previous numbered paragraph in this section) and the line does not continue
               an unfinished sentence: open text not ending . : ; ? !, the line close enough to
               continue it, and the previous line wrapped (the new line's first word would not have
               fitted in the room left at the end of the previous line, measured against the
               page's text column). "...under Section / 5. A Bidder..." therefore stays one clause,
               while "To: The Authority / 1. Having examined..." starts item 1.
  lead-in      a line opening with a bold run, e.g. "Item 3 — Evaluation."
  paragraph    anything else; following lines continue it while the style and spacing match
  rotated      rotated content text (not the watermark), kept with its angle
  region       placeholder for image / graphic / unexplained-ink regions (filled by readings)

Superscripts: a digit superscript directly after a unit token (m, km, cm, mm, ".../m") is a
unit exponent (display m³, matching text m3). Any other digit superscript is a footnote marker;
it must pair with a footnote on the same page.
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field

import pymupdf

from .extract import PageText, Span
from .regions import Region
from .textnorm import SUPERSCRIPT, normalize_latin, slug
from .util import bbox_r

LINE_GAP_SPLIT = 30.0          # pt: a horizontal gap this large splits a visual line into fragments
TERMINAL = (".", ":", ";", "?", "!")
TABLE_EDGE_TOL = 2.0           # pt: column edges of two table parts must agree within this to continue
UNIT_TOKEN = re.compile(r"(?:^|[\s(/0-9])(?:m|km|cm|mm)$|/m$")
CLAUSE_NO = re.compile(r"^\d+(?:\.\d+)+$")
LIST_ITEM = re.compile(r"^\(([a-z]{1,3}|[0-9]{1,2})\)\s")
NUMBERED = re.compile(r"^(\d{1,2})\.\s+\S")
NOTE_INTRO = re.compile(r"^Notes? to (Table [0-9]+-[0-9]+(?: \(revised\))?)\s*:", re.I)
CAPTION = re.compile(r"^Table\s+([0-9]+-[0-9]+)(\s*\(revised\))?", re.I)
FORM_HEAD = re.compile(r"^FORM\s+([0-9]+-[A-Z])\b")


@dataclass
class Unit:
    unit_id: str
    doc: str
    kind: str
    parent: str | None = None
    label: str | None = None
    label_span: str | None = None    # the span printing the label (clause / footnote number), not in `text`
    text: str = ""
    normalized: str = ""
    pages: list[int] = field(default_factory=list)
    anchors: list[dict] = field(default_factory=list)          # [{page, bbox, spans}]
    origin: str = "text_layer"
    style: dict = field(default_factory=dict)
    footnote_markers: list[dict] = field(default_factory=list)  # [{number, span_id, footnote}]
    unit_exponents: list[str] = field(default_factory=list)     # span ids
    children: list[str] = field(default_factory=list)
    table: dict | None = None        # tables: {columns, header_spans, repeated_headers, title}
    cells: dict | None = None        # table rows: {column: text}
    angle: float | None = None
    region: str | None = None        # region units: region id
    reading: dict | None = None      # filled by readings.py
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = asdict(self)
        return {k: v for k, v in d.items() if v not in (None, [], {}, "")}


@dataclass
class Fragment:
    """A run of spans on one visual line, split from neighbours by a large horizontal gap."""
    spans: list[Span]

    @property
    def bbox(self):
        return [min(s.x0 for s in self.spans), min(s.y0 for s in self.spans),
                max(s.x1 for s in self.spans), max(s.y1 for s in self.spans)]

    @property
    def body_bbox(self):
        body = [s for s in self.spans if not s.superscript] or self.spans
        return [min(s.x0 for s in body), min(s.y0 for s in body),
                max(s.x1 for s in body), max(s.y1 for s in body)]

    @property
    def page(self):
        return self.spans[0].page

    @property
    def size(self):
        c = Counter()
        for s in self.spans:
            if not s.superscript:
                c[s.size] += len(s.text.strip())
        return c.most_common(1)[0][0] if c else self.spans[0].size

    @property
    def raw(self) -> str:
        return "".join(s.text for s in self.spans)


def _col_edges(t) -> list[float]:
    """x positions of the column boundaries of a found table, from its fullest row."""
    row = max(t.rows, key=lambda r: sum(c is not None for c in r.cells))
    cells = [c for c in row.cells if c is not None]
    return [round(float(c[0]), 1) for c in cells] + [round(float(max(c[2] for c in cells)), 1)]


def _same_edges(a: list[float], b: list[float]) -> bool:
    return len(a) == len(b) and all(abs(x - y) <= TABLE_EDGE_TOL for x, y in zip(a, b))


class Segmenter:
    def __init__(self, doc_id: str, pdf: pymupdf.Document, pages: list[PageText], regions: list[Region]):
        self.doc_id = doc_id
        self.pdf = pdf
        self.pages = pages
        self.regions = regions
        self.units: dict[str, Unit] = {}
        self.order: list[str] = []
        self.problems: list[str] = []
        self.duplicates: list[str] = []                # unit ids that were produced twice (structural failure)
        self.span_unit: dict[str, str] = {}
        self.markers: list[dict] = []                 # superscript footnote markers found
        # table pre-pass: tables per page, and body size measured on flow text only
        self.page_tables = {}
        sizes = Counter()
        for p in pages:
            horiz = [s for s in p.content if s.angle == 0 and not s.invisible]
            self.page_tables[p.page] = self._tables(p.page, horiz)
            in_table = self.page_tables[p.page][1]
            for s in horiz:
                if s.span_id not in in_table and not s.superscript:
                    sizes[s.size] += len(s.text.strip())
        self.body_size = sizes.most_common(1)[0][0] if sizes else 9.6
        self.context = "cover"
        self.counters: Counter = Counter()
        self.open: Unit | None = None
        self.open_last: Fragment | None = None
        self.open_kind_group: str | None = None
        self.pending_caption: tuple[str, list[Span]] | None = None
        self.notes_for: str | None = None
        self.last_table: Unit | None = None
        self.after_table = False                       # content has followed the last table
        self.page_right: dict[int, float] = {}         # right edge of the text column per page
        self.last_numbered: dict[str, int] = {}        # context -> last numbered paragraph number

    # ------------------------------------------------------------------ helpers
    def _new_unit(self, uid: str, kind: str, **kw) -> Unit:
        base, n = uid, 1
        while uid in self.units:
            n += 1
            uid = f"{base}~{n}"
        if n > 1:
            self.duplicates.append(base)
            self.problems.append(f"duplicate unit id {base}; renamed {uid}")
        u = Unit(unit_id=uid, doc=self.doc_id, kind=kind, **kw)
        self.units[uid] = u
        self.order.append(uid)
        if u.parent and u.parent in self.units:
            self.units[u.parent].children.append(uid)
        return u

    def _assign(self, unit: Unit, spans: list[Span]) -> None:
        for s in spans:
            if s.span_id in self.span_unit:
                self.problems.append(f"span {s.span_id} assigned twice ({self.span_unit[s.span_id]}, {unit.unit_id})")
            self.span_unit[s.span_id] = unit.unit_id
        by_page = defaultdict(list)
        for s in spans:
            by_page[s.page].append(s)
        for pg, ss in sorted(by_page.items()):
            box = [min(s.x0 for s in ss), min(s.y0 for s in ss), max(s.x1 for s in ss), max(s.y1 for s in ss)]
            existing = [a for a in unit.anchors if a["page"] == pg]
            if existing:
                a = existing[0]
                a["bbox"] = bbox_r([min(a["bbox"][0], box[0]), min(a["bbox"][1], box[1]),
                                    max(a["bbox"][2], box[2]), max(a["bbox"][3], box[3])])
                a["spans"].extend(s.span_id for s in ss)
            else:
                unit.anchors.append({"page": pg, "bbox": bbox_r(box), "spans": [s.span_id for s in ss]})
            if pg not in unit.pages:
                unit.pages.append(pg)
        sizes = [s.size for s in spans if not s.superscript] or [s.size for s in spans]
        lo = min(sizes + ([unit.style["min_size"]] if "min_size" in unit.style else []))
        hi = max(sizes + ([unit.style["max_size"]] if "max_size" in unit.style else []))
        unit.style.update({"min_size": lo, "max_size": hi, "small_print": hi < 0.85 * self.body_size})

    def _join2(self, spans: list[Span], unit: Unit | None) -> tuple[str, str]:
        """(display, match) text for spans on one line; classifies superscripts.

        display: as printed, superscripts as Unicode superscript digits (m³, Form 4-B.¹²)
        match:   unit exponents as plain digits (m3); footnote markers dropped, so a marker
                 can never fuse with the preceding text (\"Form 4-B.12\")
        """
        out, match = "", ""
        prev: Span | None = None
        for s in spans:
            t = s.text
            if s.superscript and t.strip().isdigit():
                if UNIT_TOKEN.search(out.rstrip()) and not out.endswith(" "):
                    out += t.strip().translate(SUPERSCRIPT)
                    match += t.strip()
                    if unit is not None:
                        unit.unit_exponents.append(s.span_id)
                else:
                    out += t.strip().translate(SUPERSCRIPT)
                    if unit is not None:
                        self.markers.append({"number": t.strip(), "span_id": s.span_id, "page": s.page,
                                             "unit": unit.unit_id})
                        unit.footnote_markers.append({"number": t.strip(), "span_id": s.span_id})
                prev = s
                continue
            if prev is not None and out and not out.endswith(" ") and not t.startswith(" "):
                gap = s.x0 - prev.x1
                if gap > 0.2 * min(s.size, prev.size):
                    out += " "
                    match += " "
            out += t
            match += t
            prev = s
        return out, match

    def _join(self, spans: list[Span], unit: Unit | None) -> str:
        return self._join2(spans, unit)[0]

    def _append_text(self, unit: Unit, frag_spans: list[Span]) -> None:
        line, match = self._join2(frag_spans, unit)
        line, match = line.strip(), match.strip()
        if not line:
            return
        unit.text = (unit.text + " " + line).strip() if unit.text else line
        unit.normalized = normalize_latin((unit.normalized + " " + match) if unit.normalized else match)

    def _close(self):
        self.open = None
        self.open_last = None
        self.open_kind_group = None

    def _counter_id(self, kind: str) -> str:
        self.counters[(self.context, kind)] += 1
        return f"{self.doc_id}:{self.context}/{kind}{self.counters[(self.context, kind)]}"

    # ------------------------------------------------------------------ visual lines
    def _fragments(self, spans: list[Span]) -> list[Fragment]:
        """Group spans into visual lines by baseline; attach satellites; split on large gaps.

        Satellites are flagged superscripts and small digit runs that abut a larger span
        (footnote labels, subscripts such as the 5 in BOD5). They join the line of the span
        they touch, never a neighbouring line that merely overlaps them vertically.
        """
        def abutting(s, others):
            return [o for o in others if o is not s and (abs(s.x0 - o.x1) <= 1.5 or abs(o.x0 - s.x1) <= 1.5)
                    and min(o.y1, s.y1) - max(o.y0, s.y0) > 0]

        satellites, body = [], []
        for s in spans:
            t = s.text.strip()
            small_digit = (t.isdigit() and len(t) <= 3 and
                           any(o.size * 0.85 >= s.size for o in abutting(s, spans)))
            (satellites if (s.superscript or small_digit) else body).append(s)
        body.sort(key=lambda s: (s.origin[1], s.x0))
        lines: list[list[Span]] = []
        for s in body:
            for ln in reversed(lines[-3:]):
                seed = ln[0]
                if abs(seed.origin[1] - s.origin[1]) <= 0.45 * min(seed.size, s.size):
                    ln.append(s)
                    break
            else:
                lines.append([s])
        for s in satellites:
            best, best_score = None, None
            for ln in lines:
                y0, y1 = min(x.y0 for x in ln), max(x.y1 for x in ln)
                ov = min(y1, s.y1) - max(y0, s.y0)
                if ov <= 0:
                    continue
                touch = bool(abutting(s, ln))
                score = (not touch, -ov)
                if best_score is None or score < best_score:
                    best, best_score = ln, score
            if best is None:
                lines.append([s])
            else:
                best.append(s)
        frags: list[Fragment] = []
        for ln in lines:
            ln.sort(key=lambda s: s.x0)
            cur = [ln[0]]
            for s in ln[1:]:
                if s.x0 - cur[-1].x1 > LINE_GAP_SPLIT:
                    frags.append(Fragment(cur))
                    cur = [s]
                else:
                    cur.append(s)
            frags.append(Fragment(cur))
        frags.sort(key=lambda f: (round(f.bbox[1], 0), f.bbox[0]))
        return frags

    # ------------------------------------------------------------------ tables
    def _tables(self, pno: int, content: list[Span]):
        page = self.pdf[pno - 1]
        found = []
        for t in page.find_tables(strategy="lines").tables:
            if t.row_count < 2 or t.col_count < 2:
                continue
            found.append(t)
        cell_of: dict[str, tuple[int, int, int]] = {}
        for ti, t in enumerate(found):
            for s in content:
                if s.angle != 0 or s.span_id in cell_of:
                    continue
                cx, cy = s.cx, s.cy
                tb = t.bbox
                if not (tb[0] <= cx <= tb[2] and tb[1] <= cy <= tb[3]):
                    continue
                for ri, row in enumerate(t.rows):
                    rb = row.bbox
                    if not (rb[1] <= cy <= rb[3]):
                        continue
                    col = None
                    for ci, cb in enumerate(row.cells):
                        if cb is not None and cb[0] <= cx <= cb[2]:
                            col = ci
                            break
                    if col is None:  # merged cell: nearest real cell to the left
                        cands = [ci for ci, cb in enumerate(row.cells) if cb is not None and cb[0] <= cx]
                        col = cands[-1] if cands else 0
                    cell_of[s.span_id] = (ti, ri, col)
                    break
        return found, cell_of

    def _build_table(self, t, ti: int, cell_of, content_by_id, pno: int, first_item_on_page: bool):
        grid: dict[tuple[int, int], list[Span]] = defaultdict(list)
        for sid, (tj, ri, ci) in cell_of.items():
            if tj == ti:
                grid[(ri, ci)].append(content_by_id[sid])
        nrows, ncols = t.row_count, t.col_count

        def cell_text(ri, ci, unit=None, match=False):
            spans = grid.get((ri, ci), [])
            if not spans:
                return ""
            k = 1 if match else 0
            return " ".join(self._join2(f.spans, unit if not match else None)[k].strip()
                            for f in self._fragments(spans)).strip()

        row0_spans = [s for ci in range(ncols) for s in grid.get((0, ci), [])]
        has_header = bool(row0_spans) and all(s.color == "#ffffff" for s in row0_spans)
        header = [cell_text(0, ci) for ci in range(ncols)] if has_header else None

        # continuation of a table split across a page break: nothing in between, first on the next
        # page, same column geometry, and a header row (if printed) that repeats the earlier one
        lt = self.last_table
        edges = _col_edges(t)
        if (first_item_on_page and lt is not None and not self.after_table
                and lt.table["pages_last"] == pno - 1 and self.pending_caption is None
                and lt.table["ncols"] == ncols and _same_edges(lt.table["col_edges"], edges)
                and (header is None or header == lt.table["columns"])):
            table = lt
            if has_header:
                table.table["repeated_headers"].append({"page": pno, "spans": [s.span_id for s in row0_spans]})
                self._assign(table, row0_spans)
            start = 1 if has_header else 0
        else:
            title, cap_spans = (None, [])
            if self.pending_caption:
                title, cap_spans = self.pending_caption
                self.pending_caption = None
            m = CAPTION.match(title or "")
            if m:
                tid = f"{self.doc_id}:T{m.group(1)}" + ("-rev" if m.group(2) else "")
            elif header and "Bidder question" in header:
                tid = f"{self.doc_id}:{self.context}/QA"
            else:
                self.counters[(self.context, "T")] += 1
                tid = f"{self.doc_id}:{self.context}/T{self.counters[(self.context, 'T')]}"
            table = self._new_unit(tid, "table", label=title)
            table.table = {"columns": header, "ncols": ncols, "has_header": has_header, "col_edges": edges,
                           "repeated_headers": [], "title": title, "pages_last": pno,
                           "form_like": (not has_header and ncols == 2)}
            if cap_spans:
                self._assign(table, cap_spans)
            if has_header:
                self._assign(table, row0_spans)
            start = 1 if has_header else 0
            table.text = (title + " — " if title else "") + (" | ".join(header) if header else "")
        table.table["pages_last"] = pno
        tb = bbox_r(t.bbox)
        if not any(a["page"] == pno for a in table.anchors):
            table.anchors.append({"page": pno, "bbox": tb, "spans": []})
            if pno not in table.pages:
                table.pages.append(pno)
        table.table.setdefault("grid", []).append({"page": pno, "bbox": tb, "rows": t.row_count,
                                                   "cols": t.col_count})

        cols = table.table["columns"] or [f"col{i + 1}" for i in range(ncols)]
        existing_keys = {self.units[c].label for c in table.children}
        for ri in range(start, nrows):
            spans = [s for ci in range(ncols) for s in grid.get((ri, ci), [])]
            if not spans:
                continue
            texts = [cell_text(ri, ci) for ci in range(ncols)]
            if table.table["form_like"]:
                key = slug(texts[0]) if texts[0] else f"row{ri}"
            elif cols[0] in ("No", "Ref", "Form", "Item") and texts[0]:
                key = texts[0]
            elif texts[0]:
                key = slug(texts[0])
            elif len(texts) > 1 and texts[1]:
                key = slug(texts[1])
            else:
                key = f"row{ri}"
            if key in existing_keys:
                key = f"{key}~{ri}"
            existing_keys.add(key)
            if "Bidder question" in (table.table["columns"] or []):
                rid = f"{self.doc_id}:Q{key}"
            elif table.table["form_like"]:
                rid = f"{self.doc_id}:{self.context}/{key}"      # form fields belong to the form
            else:
                rid = f"{table.unit_id}/{key}"
            row = self._new_unit(rid, "table_row", parent=table.unit_id, label=key)
            row.cells = {}
            for ci in range(ncols):
                cs = grid.get((ri, ci), [])
                if cs:
                    row.cells[cols[ci]] = cell_text(ri, ci, row)
            mtexts = [cell_text(ri, ci, match=True) for ci in range(ncols)]
            if table.table["form_like"]:
                row.kind = "form_field"
                row.text = f"{texts[0]}: {texts[1]}".strip() if len(texts) > 1 else texts[0]
                row.normalized = normalize_latin(f"{mtexts[0]}: {mtexts[1]}" if len(mtexts) > 1 else mtexts[0])
            else:
                row.text = " | ".join(f"{cols[ci]}: {texts[ci]}" for ci in range(ncols) if texts[ci])
                row.normalized = normalize_latin(" | ".join(f"{cols[ci]}: {mtexts[ci]}" for ci in range(ncols) if mtexts[ci]))
            self._assign(row, spans)
        self.last_table = table
        self.after_table = False
        self._close()
        return table

    # ------------------------------------------------------------------ main
    def run(self) -> dict[str, Unit]:
        for pt in self.pages:
            self._page(pt)
        self._pair_footnotes()
        for u in self.units.values():
            if not u.normalized:
                u.normalized = normalize_latin(u.text)
            u.pages.sort()
        return self.units

    def _page(self, pt: PageText) -> None:
        pno = pt.page
        self.page_h = pt.height
        visible = [s for s in pt.content if not s.invisible]
        invisible = [s for s in pt.content if s.invisible]
        horiz = [s for s in visible if s.angle == 0]
        rotated = [s for s in visible if s.angle != 0]
        content_by_id = {s.span_id: s for s in visible}
        tables, cell_of = self.page_tables[pno]
        flow = [s for s in horiz if s.span_id not in cell_of]
        items: list[tuple[float, float, str, object]] = []
        frags = self._fragments(flow)
        if frags:
            self.page_right[pno] = max(f.bbox[2] for f in frags)
        for f in frags:
            items.append((f.bbox[1], f.bbox[0], "frag", f))
        for ti, t in enumerate(tables):
            items.append((t.bbox[1], t.bbox[0], "table", ti))
        for g in self.regions:
            if g.page == pno:
                items.append((g.bbox[1], g.bbox[0], "region", g))
        for grp in self._rotated_groups(rotated):
            items.append((min(s.y0 for s in grp), min(s.x0 for s in grp), "rotated", grp))
        items.sort(key=lambda it: (round(it[0], 0), it[1]))
        for n, (_, _, kind, obj) in enumerate(items):
            first = n == 0
            if kind == "table":
                self._build_table(tables[obj], obj, cell_of, content_by_id, pno, first)
                continue
            self.after_table = True            # anything after a table ends its chance to continue
            if kind == "frag":
                self._fragment(obj, first)
            elif kind == "region":
                self._region(obj)
            else:
                self._rotated(obj)
        if invisible:
            u = self._new_unit(f"{self.doc_id}:invisible:p{pno}", "invisible_text")
            u.notes.append("invisible text (render mode 3 or zero opacity); recorded, not used as content")
            self._append_text(u, invisible)
            self._assign(u, invisible)

    def _rotated_groups(self, spans: list[Span]) -> list[list[Span]]:
        groups: list[list[Span]] = []
        for s in sorted(spans, key=lambda s: (s.angle, s.y0, s.x0)):
            for g in groups:
                if g[0].angle == s.angle and pymupdf.Rect(g[-1].bbox).intersects(
                        pymupdf.Rect(s.bbox) + (-6, -6, 6, 6)):
                    g.append(s)
                    break
            else:
                groups.append([s])
        return groups

    def _rotated(self, spans: list[Span]) -> None:
        self.counters[("rot", spans[0].page)] += 1
        u = self._new_unit(f"{self.doc_id}:rotated:p{spans[0].page}-{self.counters[('rot', spans[0].page)]}",
                           "rotated_text", angle=spans[0].angle)
        u.text = " ".join(s.text.strip() for s in spans)
        u.normalized = normalize_latin(u.text)
        self._assign(u, spans)

    def _region(self, g: Region) -> None:
        u = self._new_unit(f"{self.doc_id}:region:{g.region_id}", "region", region=g.region_id)
        u.pages = [g.page]
        u.anchors = [{"page": g.page, "bbox": g.bbox, "spans": []}]
        u.notes.append(f"{g.kind}: content not in the text layer; requires a reading")
        self._close()

    def _fragment(self, f: Fragment, first_on_page: bool) -> None:
        spans = f.spans
        lead = next((s for s in spans if s.text.strip()), spans[0])
        text = self._join(spans, None).strip()
        bold_helv = all(("Helvetica" in s.font and s.bold) for s in spans if s.text.strip())
        size = f.size
        small = size < 0.85 * self.body_size

        # caption
        if bold_helv and size < 10 and CAPTION.match(text):
            self._close()
            self.pending_caption = (text, spans)
            return
        # heading
        if bold_helv and size >= 10:
            if self.open is not None and self.open.kind == "heading" and self.open_last is not None \
                    and f.bbox[1] - self.open_last.bbox[3] < 0.8 * size and self.open_last.size == size:
                self._append_text(self.open, spans)
                self._assign(self.open, spans)
                self.open_last = f
                self._set_context(self.open.text)
                return
            self._close()
            self._set_context(text)
            u = self._new_unit(self._heading_id(), "heading")
            self._append_text(u, spans)
            self._assign(u, spans)
            self.open, self.open_last = u, f
            self.notes_for = None
            return
        # form heading in smaller type (e.g. Form 4-G inside an addendum)
        if bold_helv and FORM_HEAD.match(text):
            self._close()
            self._set_context(text)
            u = self._new_unit(self._heading_id(), "heading")
            self._append_text(u, spans)
            self._assign(u, spans)
            self.open, self.open_last = u, f
            return
        # footnote body
        if (small and lead.text.strip().isdigit() and len(spans) > 1 and lead.size < size - 0.5
                and f.bbox[1] > 0.4 * self.page_h):
            num = lead.text.strip()
            self._close()
            u = self._new_unit(f"{self.doc_id}:fn{num}@p{f.page}", "footnote", label=num, label_span=lead.span_id)
            self._append_text(u, spans[1:])
            self._assign(u, spans)
            self.open, self.open_last, self.open_kind_group = u, f, "footnote"
            return
        # notes block
        m = NOTE_INTRO.match(text)
        if m:
            self._close()
            target = self.last_table.unit_id if self.last_table else f"{self.doc_id}:{self.context}"
            self.notes_for = target
            u = self._new_unit(f"{target}/notes", "note_intro", parent=target)
            self._append_text(u, spans)
            self._assign(u, spans)
            return
        lm = LIST_ITEM.match(text)
        if lm and self.notes_for and small:
            self._close()
            u = self._new_unit(f"{self.notes_for}/note({lm.group(1)})", "note", parent=self.notes_for,
                               label=f"({lm.group(1)})")
            self._append_text(u, spans)
            self._assign(u, spans)
            self.open, self.open_last, self.open_kind_group = u, f, "small" if small else "body"
            return
        # clause
        if lead.bold and CLAUSE_NO.match(lead.text.strip()):
            self._close()
            num = lead.text.strip()
            u = self._new_unit(f"{self.doc_id}:{num}", "clause", label=num, label_span=lead.span_id)
            self._append_text(u, [s for s in spans if s is not lead])
            self._assign(u, spans)
            self.open, self.open_last, self.open_kind_group = u, f, "small" if small else "body"
            self.notes_for = None
            return
        # list item inside an open clause or list
        open_text = self.open.text.rstrip() if self.open is not None else ""
        if lm and self.open is not None and self.open.kind in ("clause", "list_item") \
                and (open_text.endswith((":", ";", ",", " and", " or"))
                     or (self.open.kind == "list_item" and open_text.endswith("."))):
            parent = self.open if self.open.kind == "clause" else self.units[self.open.parent]
            u = self._new_unit(f"{parent.unit_id}({lm.group(1)})", "list_item", parent=parent.unit_id,
                               label=f"({lm.group(1)})")
            self._append_text(u, spans)
            self._assign(u, spans)
            self.open, self.open_last, self.open_kind_group = u, f, "small" if small else "body"
            return
        # numbered paragraph (not bold)
        nm = NUMBERED.match(text)
        if nm and not lead.bold and self._starts_numbered(int(nm.group(1)), f, small, size, first_on_page):
            self.last_numbered[self.context] = int(nm.group(1))
            self._close()
            u = self._new_unit(f"{self.doc_id}:{self.context}/item{nm.group(1)}", "numbered_paragraph",
                               label=nm.group(1))
            self._append_text(u, spans)
            self._assign(u, spans)
            self.open, self.open_last, self.open_kind_group = u, f, "small" if small else "body"
            return
        # a bold lead-in ("Item 3 — Evaluation.", "Present:") starts a new paragraph unit, but only
        # after paragraphs: inside clauses a wrapped line may begin with bold emphasis (ADD-01 §2.1)
        lead_text = lead.text.strip()
        is_lead_in = (lead.bold and len(spans) > 1 and not all(s.bold for s in spans)
                      and re.search(r"[.:]$", lead_text) is not None)
        if is_lead_in and (self.open is None or self.open.kind in ("paragraph", "lead_in_paragraph", "heading")):
            self._close()
            u = self._new_unit(f"{self.doc_id}:{self.context}/{slug(lead_text.rstrip('.:'))}", "lead_in_paragraph")
            self._append_text(u, spans)
            self._assign(u, spans)
            self.open, self.open_last, self.open_kind_group = u, f, "small" if small else "body"
            return
        # continuation of the open unit
        if self._continues(f, small, size, first_on_page):
            self._append_text(self.open, spans)
            self._assign(self.open, spans)
            self.open_last = f
            return
        # lead-in paragraph (bold run then text) or plain paragraph
        self._close()
        kind = "lead_in_paragraph" if lead.bold and len(spans) > 1 and not all(s.bold for s in spans) else "paragraph"
        if kind == "lead_in_paragraph":
            key = slug(lead.text.strip().rstrip(".:"))
            uid = f"{self.doc_id}:{self.context}/{key}"
        else:
            uid = self._counter_id("para")
        u = self._new_unit(uid, kind)
        self._append_text(u, spans)
        self._assign(u, spans)
        self.open, self.open_last, self.open_kind_group = u, f, "small" if small else "body"

    def _continues(self, f: Fragment, small: bool, size: float, first_on_page: bool) -> bool:
        """Would this line continue the open unit (same type size group, normal line spacing)?"""
        if self.open is None or self.open.kind == "heading" or self.open_last is None:
            return False
        same_group = self.open_kind_group == ("small" if small else "body")
        if self.open.kind == "footnote":
            same_group = small
        gap = f.body_bbox[1] - self.open_last.body_bbox[3]
        cross_page = f.page != self.open_last.page and first_on_page
        return same_group and (cross_page or (f.page == self.open_last.page and -2 < gap < 1.2 * size))

    def _starts_numbered(self, n: int, f: Fragment, small: bool, size: float, first_on_page: bool) -> bool:
        """A line beginning "N. " starts a numbered paragraph only if N is in sequence and the line
        does not carry on an unfinished sentence ("... under Section" / "5. A Bidder ...")."""
        in_sequence = n == 1 or self.last_numbered.get(self.context) == n - 1
        if not in_sequence:
            return False
        if self.open is None or self.open.kind == "heading":
            return True
        unfinished = not self.open.text.rstrip().endswith(TERMINAL)
        return not (unfinished and self._continues(f, small, size, first_on_page) and self._wrapped(f, size))

    def _wrapped(self, f: Fragment, size: float) -> bool:
        """Did the open unit's last line run out of room? True if the first word of `f` (plus a
        space) would not have fitted between the end of that line and the text column's right edge."""
        prev = self.open_last
        right = self.page_right.get(prev.page, prev.bbox[2])
        lead = next((s for s in f.spans if s.text.strip()), f.spans[0])
        word = lead.text.strip().split()[0] if lead.text.strip() else ""
        word_w = (lead.x1 - lead.x0) * len(word) / max(len(lead.text), 1)
        return right - prev.bbox[2] < word_w + 0.3 * size

    def _heading_id(self) -> str:
        base = f"{self.doc_id}:H:{self.context}"
        if base not in self.units:
            return base
        n = 2
        while f"{base}-{n}" in self.units:
            n += 1
        return f"{base}-{n}"

    def _set_context(self, heading_text: str) -> None:
        t = normalize_latin(heading_text)
        patterns = [
            (r"^SECTION\s+(\d+)\b", "S{}"), (r"^CLAUSE\s+(\d+)\b", "C{}"),
            (r"^APPENDIX\s+([0-9A-Z]+)\b", "App{}"), (r"^FORM\s+([0-9]+-[A-Z])\b", "F{}"),
            (r"^TABLE\s+([0-9]+-[0-9]+)\b", "T{}-heading"), (r"^(\d+)\.\s+[A-Z]", "S{}"),
        ]
        for pat, fmt in patterns:
            m = re.match(pat, t, re.I)
            if m:
                self.context = fmt.format(m.group(1))
                return
        if self.context == "cover" or not self.order:
            self.context = "cover"
            return
        self.context = slug(t)[:40]

    def _pair_footnotes(self) -> None:
        notes = {(u.label, u.pages[0]): u for u in self.units.values() if u.kind == "footnote"}
        paired = set()
        for m in self.markers:
            key = (m["number"], m["page"])
            fn = notes.get(key)
            if fn is None:
                self.problems.append(f"footnote marker {m['number']} ({m['span_id']}) has no footnote on p{m['page']}")
                continue
            host = self.units[m["unit"]]
            new_id = f"{host.unit_id}#fn{m['number']}"
            # re-key the footnote under its host unit
            self.units.pop(fn.unit_id)
            idx = self.order.index(fn.unit_id)
            for a in fn.anchors:
                for sid in a["spans"]:
                    self.span_unit[sid] = new_id
            fn.unit_id = new_id
            fn.parent = host.unit_id
            self.units[new_id] = fn
            self.order[idx] = new_id
            host.children.append(new_id)
            for fm in host.footnote_markers:
                if fm["number"] == m["number"]:
                    fm["footnote"] = new_id
            paired.add(key)
        for key, fn in notes.items():
            if key not in paired:
                self.problems.append(f"footnote {fn.unit_id} has no marker on its page")
