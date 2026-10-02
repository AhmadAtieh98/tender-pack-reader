"""Stage 1 accounting and reports.

C01  sources match the manifest (sha256, page count)            -> sources.py raises before anything runs
C02  every page accounted for (content spans, exclusions, regions)
C03  every content span is assigned to exactly one unit
C04  every exclusion matched a declared furniture rule; rules with an expected count matched it on every page
C05  every region has a reading and every reading has a region; readings pass their checks;
     pending review is shown, never hidden (pending is not a failure)
C06  every superscript is classified (unit exponent or footnote marker) and every footnote is paired
C07  unit ids are unique across the pack (text-layer and reading units); nothing was renamed
C08  every content span appears exactly once in exactly one unit's anchors, and every anchored
     span exists on its page
C09  segmentation reported no problems
C10  full evidence. Text-layer units are compared with spans re-extracted from the PDF: every
     anchor's page and bbox are those of its spans (or of the ruled table / region it names), spans
     are in reading order; flow units' printed and matching text equal their spans' text; each table
     cell equals its own spans in order and those spans lie in that cell's column; row, table and
     matching texts are rebuilt from the cells exactly. Units from image readings: every anchor is on
     the region's page and inside it, and every crop cited is the one made for that band/row/cell.

Any failing check is a structural failure: `ingest` exits non-zero and keeps the previous build.
Pending human review is a separate status, not a failure.
"""
from __future__ import annotations

import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import pymupdf

from .extract import extract_page
from .regions import detect_regions
from .segment import Segmenter, _col_edges
from .textnorm import normalize_latin
from .util import write_text


def _chars(text: str) -> str:
    """Characters for evidence comparison: NFKC (a superscript ³ compares as 3), whitespace removed."""
    return "".join(unicodedata.normalize("NFKC", text).split())


def _same_line(a, b) -> bool:
    h = min(a.y1 - a.y0, b.y1 - b.y0)
    return min(a.y1, b.y1) - max(a.y0, b.y0) > 0.3 * h


def _out_of_order(spans) -> str | None:
    """Spans must be in reading order: left to right on a line, lines top to bottom."""
    for a, b in zip(spans, spans[1:]):
        if a.angle != 0 or b.angle != 0:
            continue
        if _same_line(a, b):
            if b.x0 < a.x0 - 0.5:
                return f"{b.span_id} is left of {a.span_id} on the same line"
        elif b.y0 < a.y0:
            return f"{b.span_id} is above {a.span_id}"
    return None


def _union(spans) -> list[float]:
    return [min(s.x0 for s in spans), min(s.y0 for s in spans), max(s.x1 for s in spans), max(s.y1 for s in spans)]


def _close(a, b, tol=0.21) -> bool:
    return len(a) == len(b) and all(abs(x - y) <= tol for x, y in zip(a, b))


_FRESH: dict[tuple, dict] = {}


def _fresh(doc_id: str, path, sha256: str, rules) -> dict:
    """Independent baseline for one source document: spans re-extracted, units re-segmented, ruled tables
    re-detected. Cached by the file's hash and the furniture rules (never by anything the build produced)."""
    key = (doc_id, str(path), sha256, repr([{k: v for k, v in r.items() if not k.startswith("_")} for r in rules.rules]))
    if key not in _FRESH:
        pdf = pymupdf.open(path)
        pages = [extract_page(doc_id, pdf[i], rules) for i in range(pdf.page_count)]
        regs = [g for pt in pages for g in detect_regions(doc_id, pdf[pt.page - 1], pt)]
        seg = Segmenter(doc_id, pdf, pages, regs)
        units = seg.run()
        tables = {}
        for pt in pages:
            tables[pt.page] = [{"bbox": [round(float(v), 1) for v in t.bbox], "edges": _col_edges(t),
                                "rows": [list(r.bbox) for r in t.rows]}
                               for t in pdf[pt.page - 1].find_tables(strategy="lines").tables
                               if t.row_count >= 2 and t.col_count >= 2]
        _FRESH[key] = {"spans": {s.span_id: s for pt in pages for s in pt.content}, "order": list(seg.order),
                       "units": {k: v.to_dict() for k, v in units.items()}, "tables": tables}
    return _FRESH[key]


def full_evidence(d, rules) -> dict:
    """C10 for text-layer units: re-extract every page and compare each unit in full with its spans.

    For every unit: every anchored span exists; each anchor's page is the page its spans are on, and its
    bbox is the box of those spans (or, for an anchor with no spans, a ruled table or the region found on
    that page); spans are in reading order. Flow units: printed and matching text equal the spans' text.
    Table rows and form fields: each cell equals its own spans in reading order, those spans sit in that
    cell's column, and the row's printed and matching text are rebuilt from the cells exactly. Tables:
    caption and each header cell likewise, and the table text is rebuilt from them.
    """
    pdf = pymupdf.open(d.doc.path)
    base = _fresh(d.doc.doc_id, d.doc.path, d.doc.sha256, rules)
    fresh = base["spans"]
    page_tables: dict[int, list] = {}
    regions = {g.region_id: g for g in d.regions}
    checked, failures = 0, []

    def fail(u, why):
        failures.append({"unit": u.unit_id, "kind": u.kind, "why": why})

    # (a) every field of every unit equals an independent re-segmentation of the fresh extraction
    if base["order"] != list(d.order):
        failures.append({"unit": d.doc.doc_id, "kind": "document",
                         "why": "unit ids or their order differ from an independent re-segmentation: "
                                f"missing {sorted(set(base['order']) - set(d.order))[:3]}, "
                                f"extra {sorted(set(d.order) - set(base['order']))[:3]}"})
    for uid, u in d.units.items():
        b = base["units"].get(uid)
        if b is None:
            continue
        a = u.to_dict()
        diff = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
        if diff:
            fail(u, f"differs from an independent re-segmentation of the source in: {diff}")

    # (b) geometry independent of the segmenter: tables as ruled on the page, read afresh
    def tables_on(pno):
        return base["tables"].get(pno, [])

    claimed: dict[tuple[int, int], str] = {}
    table_grids: dict[str, dict[int, object]] = {}
    for u in d.units.values():
        if u.kind != "table":
            continue
        for g in (u.table or {}).get("grid", []):
            match = [i for i, t in enumerate(tables_on(g["page"])) if _close(t["bbox"], g["bbox"], 0.6)]
            if len(match) != 1:
                fail(u, f"grid p{g['page']} {g['bbox']} does not match exactly one ruled table on that page")
                continue
            key = (g["page"], match[0])
            if key in claimed:
                fail(u, f"ruled table p{g['page']} #{match[0]} is also claimed by {claimed[key]}")
            claimed[key] = u.unit_id
            table_grids.setdefault(u.unit_id, {})[g["page"]] = tables_on(g["page"])[match[0]]

    def grid_cell(s, table_id):
        """(row index, column index) of a span in its table's fresh grid, by the span's centre."""
        t = table_grids.get(table_id, {}).get(s.page)
        if t is None:
            return None
        ri = next((i for i, r in enumerate(t["rows"]) if r[1] - 0.5 <= s.cy <= r[3] + 0.5), None)
        edges = t["edges"]
        ci = max((i for i, x in enumerate(edges[:-1]) if x <= s.cx + 0.5), default=0)
        return ri, ci

    used_rows: dict[tuple, str] = {}
    for u in d.units.values():
        if u.kind == "region" and (u.text or u.normalized):
            fail(u, "a region placeholder carries text")
        sids = [sid for a in u.anchors for sid in a["spans"] if sid in fresh]
        sp = [fresh[x] for x in sids]
        if sp and (all(s.invisible for s in sp)) != (u.kind == "invisible_text"):
            fail(u, f"kind {u.kind!r} does not match its spans' visibility")
        if u.label_span is not None:
            pg = [x for x in sp if x.page == min(y.page for y in sp)]
            top = min(pg, key=lambda x: x.y0) if pg else None
            line1 = [x for x in pg if _same_line(x, top)] if top else []
            first = min(line1, key=lambda x: x.x0) if line1 else None
            if u.label_span not in fresh or first is None or first.span_id != u.label_span or \
                    fresh[u.label_span].text.strip() != (u.label or ""):
                fail(u, f"label_span {u.label_span} is not the unit's first span printing its label {u.label!r}")
        elif u.kind in ("clause", "footnote"):
            fail(u, "a clause or footnote without the span that prints its label")
        if u.kind not in ("table", "table_row", "form_field") and sp:
            for p_ in sorted({x.page for x in sp}):
                bad = _out_of_order([fresh[x] for x in sids if fresh[x].page == p_])
                if bad:
                    fail(u, f"spans out of reading order across anchors: {bad}")
                    break
        if u.kind in ("table_row", "form_field"):
            parent = d.units.get(u.parent or "")
            if parent is None or parent.kind != "table" or u.unit_id not in parent.children:
                fail(u, "row does not belong to an existing table that lists it")
                continue
            cols = parent.table.get("columns") or [f"col{i + 1}" for i in range(parent.table["ncols"])]
            places = set()
            for k, ss in (u.cell_spans or {}).items():
                for sid in ss:
                    gc = grid_cell(fresh[sid], parent.unit_id) if sid in fresh else None
                    if gc is None or gc[0] is None:
                        fail(u, f"span {sid} is not inside its table's ruled grid")
                        break
                    if k not in cols or cols[gc[1]] != k:
                        fail(u, f"cell {k!r}: span {sid} lies in grid column {cols[gc[1]] if gc[1] < len(cols) else gc[1]!r}")
                        break
                    places.add((fresh[sid].page, gc[0]))
            if len(places) > 1:
                fail(u, f"row spans {len(places)} grid rows")
            for pl in places:
                key = (parent.unit_id,) + pl
                if key in used_rows and used_rows[key] != u.unit_id:
                    fail(u, f"grid row {pl} also belongs to {used_rows[key]}")
                used_rows[key] = u.unit_id
        if u.kind == "table" and (u.table or {}).get("has_header"):
            for k, ss in (u.table.get("header_cell_spans") or {}).items():
                cols = u.table.get("columns") or []
                for sid in ss:
                    gc = grid_cell(fresh[sid], u.unit_id) if sid in fresh else None
                    if gc is None or gc[0] != 0 or k not in cols or cols[gc[1]] != k:
                        fail(u, f"header {k!r}: span {sid} is not in that column of the header row")
                        break

    def anchor_problem(u) -> str | None:
        for a in u.anchors:
            if any(sid not in fresh for sid in a["spans"]):
                return f"anchored spans not found when the PDF is re-extracted: {[x for x in a['spans'] if x not in fresh][:3]}"
            sp = [fresh[sid] for sid in a["spans"]]
            if u.kind == "region":
                g = regions.get(u.region)
                if g is None or a["page"] != g.page or not _close(a["bbox"], g.bbox):
                    return f"anchor p{a['page']} {a['bbox']} is not the detected region"
                continue
            if not sp:
                if u.kind != "table":
                    return "anchor with no spans"
                if a["page"] not in page_tables:
                    page_tables[a["page"]] = [list(t.bbox) for t in pdf[a["page"] - 1].find_tables(strategy="lines").tables]
                if not any(_close(a["bbox"], tb, 0.6) for tb in page_tables[a["page"]]):
                    return f"anchor p{a['page']} {a['bbox']} is not a ruled table on that page"
                continue
            pages = {s.page for s in sp}
            if pages != {a["page"]}:
                return f"anchor says page {a['page']} but its spans are on page(s) {sorted(pages)}"
            if not _close(a["bbox"], _union(sp)):
                return f"anchor bbox {a['bbox']} is not the box of its spans {[round(v, 1) for v in _union(sp)]}"
            if u.kind not in ("table", "table_row", "form_field"):
                bad = _out_of_order(sp)
                if bad:
                    return f"spans out of reading order: {bad}"
        return None

    def cell_problem(key, value, sids, exponents) -> str | None:
        if any(sid not in fresh for sid in sids):
            return f"cell {key!r}: spans not found"
        sp = [fresh[sid] for sid in sids]
        bad = _out_of_order(sp)
        if bad:
            return f"cell {key!r}: spans out of reading order: {bad}"
        if _chars(value) != _chars("".join(s.text for s in sp)):
            return f"cell {key!r}: {value!r} is not the text of its spans in order"
        return None

    def match_text(sids, exponents) -> str:
        return "".join(fresh[sid].text for sid in sids
                       if not (fresh[sid].superscript and fresh[sid].text.strip().isdigit() and sid not in exponents))

    tables = {u.unit_id: u for u in d.units.values() if u.kind == "table"}
    for u in d.units.values():
        checked += 1
        sids = [sid for a in u.anchors for sid in a["spans"]]
        why = anchor_problem(u)
        if why:
            fail(u, why)
            continue
        if u.kind == "region":
            continue
        if not sids:
            if u.text.strip() and u.kind != "table":
                fail(u, "text with no source spans")
            continue
        exps = set(u.unit_exponents)
        if u.kind == "table":
            t = u.table or {}
            cols = t.get("columns") or []
            parts = [("caption", t.get("title") or "", t.get("caption_spans") or [])]
            parts += [(f"header {c!r}", c, t.get("header_cell_spans", {}).get(c, [])) for c in (cols if t.get("has_header") else [])]
            for h in t.get("repeated_headers", []):
                parts += [(f"repeated header {c!r} p{h['page']}", c, h.get("cell_spans", {}).get(c, [])) for c in cols]
            used = [sid for _, _, ss in parts for sid in ss]
            why = next((w for w in (cell_problem(k, v, ss, exps) for k, v, ss in parts) if w), None)
            if why:
                fail(u, why)
            elif sorted(used) != sorted(sids):
                fail(u, "caption and header cells do not account for exactly the table's spans")
            elif u.text != (t["title"] + " — " if t.get("title") else "") + " | ".join(cols):
                fail(u, "table text is not its title and header")
            continue
        if u.kind in ("table_row", "form_field"):
            parent = tables.get(u.parent)
            cs = u.cell_spans or {}
            cols = (parent.table.get("columns") if parent else None) or \
                [f"col{i + 1}" for i in range(parent.table["ncols"] if parent else len(cs))]
            if set(cs) != set(u.cells or {}) or sorted(x for v in cs.values() for x in v) != sorted(sids):
                fail(u, "cells and their spans do not account for exactly the row's spans")
                continue
            why = next((w for w in (cell_problem(k, u.cells[k], cs[k], exps) for k in cs) if w), None)
            if not why and parent:
                for k, ss in cs.items():
                    for sid in ss:
                        s = fresh[sid]
                        grid = next((g for g in parent.table.get("grid", []) if g["page"] == s.page), None)
                        edges = (grid or {}).get("col_edges") or parent.table.get("col_edges")
                        col = max((i for i, x in enumerate(edges[:-1]) if x <= s.cx + 0.5), default=0)
                        if cols[col] != k:
                            why = f"cell {k!r}: span {sid} lies in column {cols[col]!r}"
                            break
                    if why:
                        break
            if why:
                fail(u, why)
                continue
            order = [c for c in cols if c in cs]
            texts = {c: u.cells[c] for c in order}
            mts = {c: match_text(cs[c], exps) for c in order}
            if u.kind == "form_field":
                t0, t1 = texts.get(cols[0], ""), texts.get(cols[1], "") if len(cols) > 1 else ""
                want_text, want_norm = f"{t0}: {t1}" if len(cols) > 1 else t0, \
                    f"{mts.get(cols[0], '')}: {mts.get(cols[1], '')}" if len(cols) > 1 else mts.get(cols[0], "")
            else:
                want_text = " | ".join(f"{c}: {v}" for c, v in texts.items() if v)
                want_norm = " | ".join(f"{c}: {mts[c]}" for c in order if mts[c].strip())
            if _chars(u.text) != _chars(want_text):
                fail(u, "row text is not rebuilt from its cells")
            elif _chars(u.normalized) != _chars(normalize_latin(want_norm)):
                fail(u, "matching text differs from the cells' spans")
            continue
        body = [s for s in (fresh[x] for x in sids) if s.span_id != u.label_span]
        markers = {m["span_id"] for m in u.footnote_markers}
        printed = _chars("".join(s.text for s in body))
        match = _chars(normalize_latin("".join(s.text for s in body if s.span_id not in markers)))
        if _chars(u.text) != printed:
            fail(u, "printed text differs from its spans")
        elif _chars(u.normalized) != match:
            fail(u, "matching text differs from its spans")
    return {"units_checked": checked, "failures": failures}


def reading_evidence(reading_units: dict[str, list[dict]], regions: dict, evidence: dict,
                     sources: dict | None = None) -> dict:
    """C10 for units derived from image readings.

    (a) The units equal a fresh derivation from their reading (`sources`: {region: (reading, status)}).
    (b) Independently of that derivation, every unit has at least one anchor, every anchor is on the
        region's page, inside it, and cites a crop: the whole-region crop for the reading's top unit,
        the crop of exactly the band and side a block line was read from, or for a table row the crop of
        its grid row (row n of the reading is grid row n) and, for every column heading, the cell crop
        and cell box of that column in that row (right-to-left tables: the first column is rightmost).
    """
    from .readings import reading_units as derive
    checked, failures = 0, []
    for rid, units in reading_units.items():
        g, ev = regions.get(rid), evidence.get(rid) or {}
        if sources is not None and rid in sources:
            reading, status = sources[rid]
            want = derive(reading, g, status, ev)
            if [u["unit_id"] for u in want] != [u["unit_id"] for u in units]:
                failures.append({"unit": rid, "kind": "reading", "why": "units or their order differ from the reading"})
            for a, b in zip(units, want):
                diff = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
                if diff:
                    failures.append({"unit": a["unit_id"], "kind": a.get("kind"), "why": f"differs from its reading in: {diff}"})
        top = units[0] if units else {}
        cols = (top.get("table") or {}).get("columns") or []
        rtl = (top.get("table") or {}).get("direction") == "rtl"
        expect_row = 1
        for u in units:
            checked += 1
            why = None if u.get("anchors") else "no anchor"
            for a in u.get("anchors", []):
                if g is None or a["page"] != g.page:
                    why = f"anchor page {a['page']} is not the region's page"
                    break
                b, rb = a["bbox"], g.bbox
                if not (b[0] >= rb[0] - 0.6 and b[1] >= rb[1] - 0.6 and b[2] <= rb[2] + 0.6 and b[3] <= rb[3] + 0.6):
                    why = f"anchor bbox {b} lies outside the region {rb}"
                    break
                crop = a.get("crop")
                if not crop:
                    why = "anchor cites no crop"
                    break
                if u["kind"] == "table_row":
                    gr = a.get("grid_row")
                    if gr != expect_row:
                        why = f"row unit at reading position {expect_row} cites grid row {gr}"
                        break
                    expect_row += 1
                    if crop != ev.get("row_crops", {}).get(gr) or not _close(b, ev.get("row_bbox_pt", {}).get(gr) or []):
                        why = f"row crop/bbox is not grid row {gr}"
                        break
                    cc, cb = a.get("cell_crops") or {}, a.get("cell_bbox_pt") or {}
                    for i, h in enumerate(cols):
                        gc = len(cols) - 1 - i if rtl else i
                        if cc.get(h) is None or cc.get(h) != ev.get("cell_crops", {}).get((gr, gc)) or \
                                not _close(cb.get(h) or [], ev.get("cell_bbox_pt", {}).get((gr, gc)) or []):
                            why = f"cell crop/bbox for column {h!r} is not grid cell ({gr}, {gc})"
                            break
                    if why:
                        break
                elif u["kind"] == "reading_block":
                    key = tuple(a.get("band") or ())
                    if len(key) != 2 or crop != ev.get("band_crops", {}).get(key) or \
                            not _close(b, ev.get("band_bbox_pt", {}).get(key) or []):
                        why = f"block anchor is not the crop and box of band {list(key) or '?'}"
                        break
                elif crop != (g.crop or {}).get("path") or not _close(b, g.bbox):
                    why = f"anchor of {u['kind']} is not the whole-region crop"
                    break
            if why:
                failures.append({"unit": u["unit_id"], "kind": u["kind"], "why": why})
    return {"units_checked": checked, "failures": failures}


def coverage_report(pack, packets: dict[str, dict], reading_units: dict[str, list[dict]],
                    orphan_readings: list[str] | None = None, evidence_index: dict | None = None,
                    reading_sources: dict | None = None) -> dict:
    checks = []
    pages = []
    exclusions = []
    superscripts = []
    footnotes = []
    split_tables = []
    small_print = []
    rotated_content = []
    problems = []
    notices = []
    anchor_twice, anchor_none, anchor_unknown, duplicates = [], [], [], []
    evidence = {"units_checked": 0, "failures": []}
    for d in pack.docs:
        doc_id = d.doc.doc_id
        assigned = Counter(d.span_unit.values())
        unit_pages = defaultdict(set)
        for u in d.units.values():
            for pg in u.pages:
                unit_pages[pg].add(u.unit_id)
        for p in d.pages:
            excl = Counter(e.rule for e in p.exclusions)
            content_ids = [s.span_id for s in p.content]
            unassigned = [sid for sid in content_ids if sid not in d.span_unit]
            regs = [g for g in d.regions if g.page == p.page]
            pages.append({
                "doc": doc_id, "page": p.page, "printed_page": p.printed_page,
                "content_spans": len(content_ids), "assigned": len(content_ids) - len(unassigned),
                "unassigned": unassigned, "excluded": dict(sorted(excl.items())), "blank_spans": p.blank_spans,
                "invisible_spans": p.invisible_spans, "units": len(unit_pages[p.page]),
                "regions": [{"id": g.region_id, "kind": g.kind,
                             "reading": packets.get(g.region_id, {}).get("status", "unread")} for g in regs],
            })
            for e in p.exclusions:
                exclusions.append(e.__dict__)
            for s in p.content:
                if s.angle != 0 and not s.invisible:
                    rotated_content.append({"span": s.span_id, "text": s.text, "angle": s.angle,
                                            "unit": d.span_unit.get(s.span_id)})
                if s.superscript:
                    u = d.units.get(d.span_unit.get(s.span_id, ""))
                    kind = ("unit exponent" if u and s.span_id in u.unit_exponents else
                            "footnote marker" if u and any(m["span_id"] == s.span_id for m in u.footnote_markers) else
                            "unclassified")
                    paired = None
                    if u and kind == "footnote marker":
                        paired = next((m.get("footnote") for m in u.footnote_markers if m["span_id"] == s.span_id), None)
                    superscripts.append({"span": s.span_id, "text": s.text, "size": s.size, "unit": d.span_unit.get(s.span_id),
                                         "class": kind, "footnote": paired})
        for u in d.units.values():
            if u.kind == "footnote":
                footnotes.append({"unit": u.unit_id, "label": u.label, "host": u.parent, "page": u.pages,
                                  "text": u.text})
            if u.kind == "table" and len(u.pages) > 1:
                split_tables.append({"unit": u.unit_id, "pages": u.pages, "title": u.table.get("title"),
                                     "rows": len(u.children),
                                     "repeated_headers": u.table.get("repeated_headers", []),
                                     "row_pages": {c: d.units[c].pages for c in u.children}})
            if u.style.get("small_print"):
                small_print.append({"unit": u.unit_id, "kind": u.kind, "max_size": u.style.get("max_size"),
                                    "text": u.text[:160]})
        problems += [f"{doc_id}: {x}" for x in d.problems]
        notices += [f"{doc_id}: {x}" for x in getattr(d, "notices", [])]
        anchored = Counter(sid for u in d.units.values() for a in u.anchors for sid in a["spans"])
        content = {s.span_id for p in d.pages for s in p.content}
        anchor_twice += [sid for sid, n in anchored.items() if n > 1]
        anchor_none += [sid for sid in content if sid not in anchored]
        anchor_unknown += [sid for sid in anchored if sid not in content]
        duplicates += list(getattr(d, "duplicates", []))
        ev = full_evidence(d, pack.rules)
        evidence["units_checked"] += ev["units_checked"]
        evidence["failures"] += ev["failures"]

    total_content = sum(p["content_spans"] for p in pages)
    total_assigned = sum(p["assigned"] for p in pages)
    checks.append({"id": "C01", "ok": True, "detail": f"{len(pack.docs)} documents match sources/manifest.json (sha256, pages)"})
    checks.append({"id": "C02", "ok": len(pages) == sum(d.doc.pages for d in pack.docs),
                   "detail": f"{len(pages)} pages accounted for out of {sum(d.doc.pages for d in pack.docs)}"})
    checks.append({"id": "C03", "ok": total_content == total_assigned and not any("assigned twice" in x for x in problems),
                   "detail": f"{total_assigned} of {total_content} content spans assigned to exactly one unit"})
    excl_counts = Counter(e["rule"] for e in exclusions)
    checks.append({"id": "C04", "ok": not pack.furniture_problems,
                   "detail": f"{len(exclusions)} spans excluded, all by declared rules: {dict(sorted(excl_counts.items()))}; "
                             f"expected-count problems: {pack.furniture_problems or 'none'}"})
    regions = [g for d in pack.docs for g in d.regions]
    unread = [g.region_id for g in regions if g.region_id not in packets or packets[g.region_id]["status"] == "unread"]
    failing = [rid for rid, pk in packets.items() if any(not c["ok"] for c in pk.get("checks", []))]
    pending = [rid for rid, pk in packets.items() if pk.get("status") == "pending"]
    partial = sorted({rid for rid, pk in packets.items() if any(c.get("result") == "partial" for c in pk.get("checks", []))})
    orphan = sorted(orphan_readings or [])
    checks.append({"id": "C05", "ok": not unread and not failing and not orphan,
                   "detail": f"{len(regions)} regions; unread {unread or 'none'}; readings failing checks {failing or 'none'}; "
                             f"readings with no detected region {orphan or 'none'}; "
                             f"readings with PARTIAL render checks {partial or 'none'}; "
                             f"PENDING HUMAN REVIEW: {pending or 'none'}"})
    unclassified = [s for s in superscripts if s["class"] == "unclassified"]
    unpaired = [s for s in superscripts if s["class"] == "footnote marker" and not s["footnote"]]
    checks.append({"id": "C06", "ok": not unclassified and not unpaired and not any("footnote" in x for x in problems),
                   "detail": f"{len(superscripts)} superscripts: "
                             f"{sum(1 for s in superscripts if s['class'] == 'unit exponent')} unit exponents, "
                             f"{sum(1 for s in superscripts if s['class'] == 'footnote marker')} footnote markers "
                             f"(all paired: {not unpaired}); unclassified {len(unclassified)}"})
    rev = reading_evidence(reading_units, {g.region_id: g for d in pack.docs for g in d.regions}, evidence_index or {},
                           reading_sources)
    evidence["units_checked"] += rev["units_checked"]
    evidence["failures"] += rev["failures"]
    ids = [u.unit_id for d in pack.docs for u in d.units.values()] + \
          [u["unit_id"] for us in reading_units.values() for u in us]
    id_dups = sorted({i for i, n in Counter(ids).items() if n > 1} | set(duplicates))
    checks.append({"id": "C07", "ok": not id_dups,
                   "detail": f"{len(ids)} unit ids; produced more than once: {id_dups or 'none'}"})
    checks.append({"id": "C08", "ok": not (anchor_twice or anchor_none or anchor_unknown),
                   "detail": f"{total_content} content spans; in more than one anchor: {sorted(anchor_twice)[:5] or 'none'}; "
                             f"in no anchor: {sorted(anchor_none)[:5] or 'none'}; anchored but not on the page: "
                             f"{sorted(anchor_unknown)[:5] or 'none'}"})
    checks.append({"id": "C09", "ok": not problems,
                   "detail": f"segmentation problems: {len(problems)}" + (f" (see Problems): {problems[:3]}" if problems else "")})
    checks.append({"id": "C10", "ok": not evidence["failures"],
                   "detail": f"{evidence['units_checked']} units checked in full: text-layer units against spans re-extracted "
                             f"from the PDF (text, cells in order and column, matching text, anchor page and geometry); "
                             f"image-reading units against their region and crops; "
                             f"mismatches: {[f['unit'] for f in evidence['failures']][:5] or 'none'}"})
    status = "ok" if all(c["ok"] for c in checks) else "structural_failure"
    return {"status": status, "checks": checks, "evidence": evidence, "notices": notices, "pages": pages, "exclusions": exclusions, "superscripts": superscripts,
            "footnotes": footnotes, "split_tables": split_tables, "small_print": small_print,
            "rotated_content": rotated_content, "problems": problems,
            "regions": [{"id": g.region_id, "doc": g.doc, "page": g.page, "kind": g.kind, "bbox": g.bbox,
                         "detection": g.detection, "notes": g.notes,
                         "reading_status": packets.get(g.region_id, {}).get("status", "unread"),
                         "reading_units": len(reading_units.get(g.region_id, []))} for g in regions],
            "pending_review": pending}


def coverage_markdown(cov: dict, title: str) -> str:
    L = [f"# Coverage report — {title}", "",
         "Generated by `python -m tenderpack ingest`. Deterministic: no timestamps. "
         "Accounting is not correctness: a span assigned to a unit says the text was captured, "
         "not that its meaning has been interpreted.", ""]
    if cov["status"] != "ok":
        L += [f"> **STRUCTURAL FAILURE:** checks {', '.join(c['id'] for c in cov['checks'] if not c['ok'])} failed. "
              "This build is not usable; the previous build (if any) was kept.", ""]
    if cov["pending_review"]:
        L += [f"> **PENDING HUMAN REVIEW:** {', '.join(cov['pending_review'])}. Units derived from these readings are "
              "marked `reading.status = pending`.", ""]
    L += ["## Checks", "", "| Check | Result | Detail |", "|---|---|---|"]
    for c in cov["checks"]:
        L.append(f"| {c['id']} | {'pass' if c['ok'] else 'FAIL'} | {c['detail']} |")
    L += ["", "## Pages", "", "| Doc | PDF p | Printed | Content spans | Assigned | Excluded (rule: n) | Units | Regions (reading) |",
          "|---|---|---|---|---|---|---|---|"]
    for p in cov["pages"]:
        ex = ", ".join(f"{k}: {v}" for k, v in p["excluded"].items())
        rg = ", ".join(f"{r['id']} {r['kind']} ({r['reading']})" for r in p["regions"]) or "—"
        L.append(f"| {p['doc']} | {p['page']} | {p['printed_page']} | {p['content_spans']} | {p['assigned']} | {ex} | "
                 f"{p['units']} | {rg} |")
    L += ["", "## Regions (content outside the text layer)", "", "| Region | Kind | BBox (pt) | Detection | Reading | Units from reading |",
          "|---|---|---|---|---|---|"]
    for r in cov["regions"]:
        L.append(f"| {r['id']} | {r['kind']} | {r['bbox']} | {r['detection']} | **{r['reading_status']}** | {r['reading_units']} |")
    L += ["", "## Superscripts", "", "| Span | Text | Size | Class | Unit | Footnote |", "|---|---|---|---|---|---|"]
    for s in cov["superscripts"]:
        L.append(f"| {s['span']} | {s['text']} | {s['size']} | {s['class']} | {s['unit']} | {s['footnote'] or ''} |")
    L += ["", "## Footnotes", ""]
    for f in cov["footnotes"]:
        L.append(f"- `{f['unit']}` (label {f['label']}, host `{f['host']}`, p{f['page']}): {f['text']}")
    L += ["", "## Tables split across pages", ""]
    for t in cov["split_tables"]:
        L.append(f"- `{t['unit']}` pages {t['pages']}, {t['rows']} rows; title: {t['title'] or '—'}; "
                 f"repeated header rows recognised and kept with the table: "
                 f"{[(h['page'], len(h['spans'])) for h in t['repeated_headers']]}; row pages: "
                 + ", ".join(f"{k.split('/')[-1] if '/' in k else k}: {v}" for k, v in t["row_pages"].items()))
    L += ["", "## Small print (largest font < 85% of the document's body size)", ""]
    for s in cov["small_print"]:
        L.append(f"- `{s['unit']}` ({s['kind']}, {s['max_size']} pt): {s['text']}")
    L += ["", "## Rotated text kept as content", ""]
    L += [f"- `{r['span']}` angle {r['angle']}: {r['text']} -> `{r['unit']}`" for r in cov["rotated_content"]] or \
         ["None in this pack: every rotated span matched the WATERMARK rule (see exclusions)."]
    L += ["", "## Full evidence check (C10) mismatches", ""] + (
        [f"- `{f['unit']}` ({f['kind']}): {f['why']}" for f in cov["evidence"]["failures"]] or
        [f"None: {cov['evidence']['units_checked']} units compared in full."])
    L += ["", "## Problems", ""] + ([f"- {p}" for p in cov["problems"]] or ["None."])
    L += ["", "## Notices (reported, not failures)", ""] + ([f"- {p}" for p in cov["notices"]] or ["None."])
    return "\n".join(L) + "\n"


def exclusions_markdown(cov: dict, rules: list[dict], title: str) -> str:
    L = [f"# Excluded text — {title}", "",
         "Every span below was excluded from content because it matched a declared rule in "
         "`config/furniture.yaml` on all of the rule's attributes. Nothing else is excluded; in particular, "
         "rotated text that does not match the WATERMARK rule stays content.", "", "## Rules", ""]
    for r in rules:
        attrs = {k: v for k, v in r.items() if not k.startswith("_") and k not in ("id", "reason")}
        L.append(f"- **{r['id']}**: {r['reason']}. Attributes: `{attrs}`")
    L += ["", f"## All exclusions ({len(cov['exclusions'])} spans)", "",
          "| Span | Rule | Text | Angle | Colour | Size | BBox |", "|---|---|---|---|---|---|---|"]
    for e in cov["exclusions"]:
        L.append(f"| {e['span_id']} | {e['rule']} | {e['text']} | {e['angle']} | {e['color']} | {e['size']} | {e['bbox']} |")
    return "\n".join(L) + "\n"


def units_markdown(ordered_units: list[dict], title: str) -> str:
    L = [f"# Source units — {title}", "",
         "One line per unit, in reading order. `text` is as printed (superscripts shown as ¹²/³); "
         "matching text is in units.json (`normalized`). Units from image readings show their review status.", ""]
    doc = None
    for u in ordered_units:
        if u["doc"] != doc:
            doc = u["doc"]
            L += ["", f"## {doc}", "", "| Unit | Kind | Pages | Flags | Text |", "|---|---|---|---|---|"]
        flags = []
        st = u.get("style", {})
        if st.get("small_print"):
            flags.append(f"small print {st.get('max_size')}pt")
        if u.get("origin") == "image_reading":
            flags.append(f"image reading: **{u['reading']['status'].upper()}**")
        if u.get("angle"):
            flags.append(f"rotated {u['angle']}°")
        if u.get("footnote_markers"):
            flags.append("footnote " + ",".join(m["number"] for m in u["footnote_markers"]))
        if u.get("unit_exponents"):
            flags.append(f"{len(u['unit_exponents'])} unit exponent(s)")
        if u.get("uncertain"):
            flags.append(f"{len(u['uncertain'])} uncertainty(ies)")
        if u.get("table", {}) and u["table"].get("repeated_headers"):
            flags.append(f"split table, repeated headers on p{[h['page'] for h in u['table']['repeated_headers']]}")
        text = u.get("text", "").replace("|", "/")
        if u.get("translation"):
            text += f" — *translation:* {u['translation']}"
        L.append(f"| `{u['unit_id']}` | {u['kind']} | {','.join(map(str, u.get('pages', [])))} | {'; '.join(flags)} | {text} |")
    return "\n".join(L) + "\n"


def write_reports(out: Path, cov: dict, ordered_units: list[dict], rules: list[dict], title: str) -> None:
    write_text(out / "coverage.md", coverage_markdown(cov, title))
    write_text(out / "exclusions.md", exclusions_markdown(cov, rules, title))
    write_text(out / "units.md", units_markdown(ordered_units, title))
