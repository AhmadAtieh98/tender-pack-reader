"""Review packets: evidence crops next to the proposed reading, for a person to approve or correct.

For each region with a reading, writes build/review/<region_id>/:
  packet.md          status, provenance, what the checks prove and what they do not, the points recorded for
                     the reviewer's decision, checks, and every heading / row / cell / line beside its crop
  packet.html        the same, self-contained (crops embedded), for reading in a browser
  compare-N.png      left: source crop at native resolution; right: the proposed reading as rendered
                     by the program (Arabic shaped and bidi-ordered by the bundled Noto Naskh font)
  bands/, rows/, cells/   native-pixel crops (never downscaled; diacritics vanish when scaled)
  numerals/          for declared numerals: high-dpi crop of the printed glyphs beside renders of the
                     stored token and its alternatives, plus the glyph-shape advisory
For regions without a reading, writes a packet that says so (UNREAD) with crops and bands.
"""
from __future__ import annotations

import base64
import html
import json
import os
import re
from pathlib import Path

import numpy as np
import pymupdf

from . import arabic
from .readings import Block, Reading, check_reading, review_status, review_subject
from .regions import Region, detect_grid, image_array, text_bands
from .util import bbox_r, relpath, sha256_file, write_text

PAD = 6


def _native_rgb(pdf: pymupdf.Document, region: Region) -> tuple[np.ndarray, float, float]:
    """Pixels of the region (native image if embedded) and the px->pt scale."""
    if region.xref:
        pix = pymupdf.Pixmap(pdf.extract_image(region.xref)["image"])
    else:
        pix = pdf[region.page - 1].get_pixmap(clip=pymupdf.Rect(region.bbox), dpi=200)
    if pix.n != 3 or pix.alpha:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        if pix.alpha:
            pix = pymupdf.Pixmap(pix, 0)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, 3)
    b = region.bbox
    return a, (b[2] - b[0]) / pix.w, (b[3] - b[1]) / pix.h


def _save(arr: np.ndarray, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    arr = np.ascontiguousarray(arr)
    pymupdf.Pixmap(pymupdf.csRGB, arr.shape[1], arr.shape[0], arr.tobytes(), False).save(path)


def _px_to_pt(region: Region, sx: float, sy: float, box) -> list[float]:
    x0, y0, x1, y1 = box
    b = region.bbox
    return bbox_r([b[0] + x0 * sx, b[1] + y0 * sy, b[0] + x1 * sx, b[1] + y1 * sy])


def build_evidence(pdf: pymupdf.Document, region: Region, reading: Reading | None, out: Path, base: Path) -> dict:
    rdir = out / region.region_id
    arr, sx, sy = _native_rgb(pdf, region)
    gray = arr.mean(axis=2)
    H, W = gray.shape
    ev: dict = {"band_crops": {}, "band_bbox_pt": {}, "row_crops": {}, "row_bbox_pt": {}, "cell_crops": {},
                "cell_bbox_pt": {}, "bands": text_bands(gray), "grid": None}
    for b in ev["bands"]:
        sides = [("full", b["x0"], b["x1"])]
        if b["split_x"] is not None:
            sides += [("left", b["x0"], b["split_x"]), ("right", b["split_x"], b["x1"])]
        for side, x0, x1 in sides:
            box = (max(x0 - PAD, 0), max(b["y0"] - PAD, 0), min(x1 + PAD, W), min(b["y1"] + PAD, H))
            p = rdir / "bands" / f"b{b['index']:02d}-{side}.png"
            _save(arr[box[1]:box[3], box[0]:box[2]], p)
            ev["band_crops"][(b["index"], side)] = relpath(p, base)
            ev["band_bbox_pt"][(b["index"], side)] = _px_to_pt(region, sx, sy, box)
    if reading is not None and reading.table is not None:
        g = detect_grid(gray)
        ev["grid"] = {"skew_deg": g.skew_deg, "h_lines": g.h_lines, "v_lines": g.v_lines, "rows": g.rows, "cols": g.cols}
        for r in range(g.rows):
            boxes = [g.cell_box(r, c) for c in range(g.cols)]
            rb = (min(x[0] for x in boxes), min(x[1] for x in boxes), max(x[2] for x in boxes), max(x[3] for x in boxes))
            p = rdir / "rows" / f"r{r:02d}.png"
            _save(arr[rb[1]:rb[3], rb[0]:rb[2]], p)
            ev["row_crops"][r] = relpath(p, base)
            ev["row_bbox_pt"][r] = _px_to_pt(region, sx, sy, rb)
            for c, cb in enumerate(boxes):
                pc = rdir / "cells" / f"r{r:02d}c{c}.png"
                _save(arr[cb[1]:cb[3], cb[0]:cb[2]], pc)
                ev["cell_crops"][(r, c)] = relpath(pc, base)
                ev["cell_bbox_pt"][(r, c)] = _px_to_pt(region, sx, sy, cb)
    return ev


# ------------------------------------------------------------------ comparison sheets

def _html_escape(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _render_rows(rows: list[tuple[str, str, str, str, list[str]]], out_prefix: Path, base: Path) -> list[str]:
    """rows: (label, crop_path, proposed_html, lang, notes).

    Each segment is stacked: the source crop at native size (1 image px = 1 output px, never
    downscaled, because diacritics and decimal points disappear when scaled), and directly below
    it the proposed reading rendered by the program at a matching size, aligned the same way
    (right-aligned for Arabic). Several sheets are written if needed.
    """
    pixes = [pymupdf.Pixmap(str(base / r[1])) for r in rows]
    page_w = max(p.w for p in pixes) * 0.75 + 24          # sheet rendered at 96 dpi: 1 px = 0.75 pt
    files: list[str] = []
    state = {"doc": None, "page": None, "y": 0.0, "n": 0}

    def flush():
        if state["doc"] is not None:
            state["n"] += 1
            p = Path(f"{out_prefix}-{state['n']}.png")
            state["page"].get_pixmap(dpi=96, clip=pymupdf.Rect(0, 0, page_w, state["y"] + 8)).save(p)
            files.append(relpath(p, base))

    def new_page():
        flush()
        state["doc"] = pymupdf.open()
        state["page"] = state["doc"].new_page(width=page_w, height=3000)
        state["page"].insert_text((10, 14), "Each segment: source crop at native resolution, then (shaded) the proposed "
                                            "reading as rendered by the program. Red = marked uncertain.",
                                  fontsize=8, color=(0.3, 0.3, 0.3))
        state["y"] = 22.0

    new_page()
    for (label, crop, html, lang, notes), pix in zip(rows, pixes):
        w, h = pix.w * 0.75, pix.h * 0.75
        prop_h = max(h * 1.1, 22)
        need = 12 + h + 4 + prop_h + 11 * len(notes) + 10
        if state["y"] + need > 2990:
            new_page()
        page, y = state["page"], state["y"]
        page.insert_text((10, y + 9), label, fontsize=8, color=(0.1, 0.1, 0.6))
        page.insert_image(pymupdf.Rect(12, y + 12, 12 + w, y + 12 + h), pixmap=pix)
        py = y + 12 + h + 4
        box = pymupdf.Rect(12, py, 12 + w, py + prop_h)
        page.draw_rect(box, color=None, fill=(0.93, 0.95, 1.0))
        direction = "rtl" if lang in ("ar", "mixed") else "ltr"
        size = max(min(h * 0.55, 30), 9)
        page.insert_htmlbox(box, f'<div dir="{direction}" style="font-size:{size:.1f}px">{html}</div>')
        ny = py + prop_h + 10
        for note in notes:
            colour = "#bf1a1a" if note.startswith("!") else "#4d4d4d"
            page.insert_htmlbox(pymupdf.Rect(14, ny - 8, page_w - 14, ny + 6),
                                f'<div style="font-size:7.5px; color:{colour}">{_html_escape(note[:220])}</div>')
            ny += 11
        page.draw_line((10, ny), (page_w - 10, ny), color=(0.8, 0.8, 0.8), width=0.5)
        state["y"] = ny + 6
    flush()
    return files


def _block_html(blk: Block, line) -> str:
    text = _html_escape(arabic.display_form(line.source) if blk.lang in ("ar", "mixed") else line.source)
    for n in line.numerals:
        if n.uncertain:
            text = text.replace(_html_escape(n.text), f'<span style="color:#c00000">{_html_escape(n.text)}</span>')
    return text


def numeral_evidence(pdf: pymupdf.Document, region: Region, reading: Reading, rdir: Path, base: Path) -> list[dict]:
    out = []
    page = pdf[region.page - 1]
    for blk in reading.all_blocks():
        for li, ln in enumerate(blk.lines):
            for ni, n in enumerate(ln.numerals):
                item = {"block": blk.key, "band": ln.band, "token": n.text, "visual_ltr_expected": n.visual_ltr_expected,
                        "meaning": n.meaning, "uncertain": n.uncertain, "alternatives": n.alternatives, "note": n.note}
                res, how = arabic.visual_check(ln.source, n.visual_ltr_expected)
                item["render_check"] = {"ok": res == "pass", "result": res, "detail": how}
                if n.crop_bbox_pt:
                    adv = arabic.digit_advisory(page, n.crop_bbox_pt)
                    item["glyph_advisory"] = adv
                    doc = pymupdf.open()
                    cands = [("stored (as rendered)", n.text)] + [(f"alternative {i + 1} (as rendered)", a.split(",")[0].split(" ")[0])
                                                                  for i, a in enumerate(n.alternatives)]
                    pg = doc.new_page(width=200 + 150 * len(cands), height=160)
                    pg.insert_htmlbox(pymupdf.Rect(10, 4, 190, 30),
                                      f'<div style="font-size:8px">printed, {region.doc} p{region.page}<br>crop {n.crop_bbox_pt} pt</div>')
                    pg.insert_image(pymupdf.Rect(10, 34, 150, 154),
                                    pixmap=page.get_pixmap(clip=pymupdf.Rect(n.crop_bbox_pt), dpi=600))
                    for ci, (lab, tok) in enumerate(cands):
                        x = 200 + ci * 150
                        ascii_tok = tok.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))
                        pg.insert_htmlbox(pymupdf.Rect(x, 4, x + 145, 30),
                                          f'<div style="font-size:8px">{lab}<br>logical {_html_escape(ascii_tok)}</div>')
                        pg.insert_htmlbox(pymupdf.Rect(x, 50, x + 130, 150),
                                          f'<p dir="rtl" style="font-size:44px">{_html_escape(tok)}</p>')
                    p = rdir / "numerals" / f"{blk.key}-{li}-{ni}.png"
                    p.parent.mkdir(parents=True, exist_ok=True)
                    pg.get_pixmap(dpi=150).save(p)
                    item["image"] = relpath(p, base)
                out.append(item)
    if reading.table is not None:
        for r in reading.table.rows:
            for n in r.numerals:
                text = r.cells.get(n.column or "", "")
                res, how = arabic.visual_check(text, n.visual_ltr_expected)
                out.append({"block": f"row {r.key}", "column": n.column, "band": None, "token": n.text,
                            "visual_ltr_expected": n.visual_ltr_expected, "meaning": n.meaning,
                            "uncertain": n.uncertain, "alternatives": n.alternatives, "note": n.note,
                            "render_check": {"ok": res == "pass", "result": res,
                                             "detail": f"cell rendered right to left: {how}"}})
    return out


# ------------------------------------------------------------------ packet

def _grid_col(reading: Reading, c: int) -> int:
    """Grid column (left to right on the page) of logical column c."""
    n = len(reading.table.columns)
    return n - 1 - c if reading.table.direction == "rtl" else c


def write_packet(pdf: pymupdf.Document, region: Region, reading: Reading | None, approvals: list[dict],
                 ev: dict, out: Path, base: Path, root: Path, reading_path: Path | None,
                 doc_sha256: str = "", approvals_path: str = "curation/approvals.yaml") -> dict:
    """Evidence paths are relative to `base` (the build directory); the reading path to `root` (the repo)."""
    rdir = out / region.region_id
    rdir.mkdir(parents=True, exist_ok=True)
    rel = lambda p: Path(os.path.relpath(base / p, rdir)).as_posix() if p else ""  # noqa: E731
    lines = []
    summary = {"region_id": region.region_id, "doc": region.doc, "page": region.page, "kind": region.kind,
               "bbox": region.bbox}
    if reading is None:
        summary.update(status="unread", checks=[])
        lines += [f"# Review packet: {region.region_id} — NO READING", "",
                  "**STATUS: UNREAD.** This region has content outside the text layer and no reading exists. "
                  "Nothing from it is in the units; coverage reports it as unread.", "",
                  f"- Source: {region.doc} page {region.page}, bbox {region.bbox} pt; detected as `{region.kind}` "
                  f"({region.detection})",
                  f"- Crop: `{region.crop['path'] if region.crop else ''}`", "",
                  f"![crop]({rel(region.crop['path']) if region.crop else ''})", "",
                  f"Text bands detected in the region: {sum(1 for b in ev['bands'] if b['kind'] == 'text')} "
                  f"(rule bands: {sum(1 for b in ev['bands'] if b['kind'] == 'rule')})."]
        write_text(rdir / "packet.md", "\n".join(lines) + "\n")
        return summary

    subject = review_subject(reading, region, doc_sha256)
    status = review_status(reading, approvals, subject)
    checks = check_reading(reading, region, pdf)
    nums = numeral_evidence(pdf, region, reading, rdir, base)
    summary.update(status=status["status"], status_reason=status.get("reason"), subject_sha256=subject["sha256"],
                   subject_covers=subject["covers"], subject_evidence=subject["evidence"],
                   checks=checks, numerals=nums, reading=relpath(reading_path, root) if reading_path else None)

    rows = []
    blocks = reading.all_blocks()
    if reading.table is not None:
        t = reading.table
        table_lang = "ar" if t.direction == "rtl" else "en"
        for blk in [b for b in (t.title, t.qualifier) if b is not None]:
            for ln in blk.lines:
                rows.append((f"{blk.key} (band {ln.band})", ev["band_crops"][(ln.band, ln.side)],
                             _block_html(blk, ln), blk.lang, [f"! {u}" for u in blk.uncertain]))
        # cells joined in logical order; a right-to-left table is rendered right to left, like the image
        header = " | ".join(_html_escape(c.heading) for c in t.columns)
        if ev["row_crops"]:
            rows.append(("header row (grid row 0)", ev["row_crops"][0], header, table_lang, []))
        for i, r in enumerate(t.rows, 1):
            if i not in ev["row_crops"]:
                continue                                   # grid mismatch: reported by RD3
            cells = " | ".join(_html_escape(arabic.display_form(r.cells.get(c.key, "")) if t.direction == "rtl"
                                            else r.cells.get(c.key, "")) or "<i>(blank)</i>" for c in t.columns)
            rows.append((f"row {r.key} (grid row {i})", ev["row_crops"][i], cells, table_lang,
                         [f"! {u}" for u in r.uncertain]))
        for blk in t.notes:
            for ln in blk.lines:
                rows.append((f"{blk.key} (band {ln.band})", ev["band_crops"][(ln.band, ln.side)],
                             _block_html(blk, ln), blk.lang, [f"! {u}" for u in blk.uncertain]))
    elif reading.content_type == "graphic":
        rows.append(("drawing (rendered crop)", region.crop["path"], _html_escape(reading.description or ""), "en",
                     [f"! {u}" for u in reading.uncertainties]))
    else:
        for blk in blocks:
            for li, ln in enumerate(blk.lines):
                notes = []
                if li == len(blk.lines) - 1 and blk.translation:
                    notes.append(f"translation: {blk.translation}")
                notes += [f"! {u}" for u in (ln.uncertain + (blk.uncertain if li == len(blk.lines) - 1 else []))]
                notes += [f"! numeral {n.text}: uncertain — see numerals/" for n in ln.numerals if n.uncertain]
                rows.append((f"{blk.key} (band {ln.band}, {ln.side})", ev["band_crops"][(ln.band, ln.side)],
                             _block_html(blk, ln), blk.lang, notes))
    compare = _render_rows(rows, rdir / "compare", base) if rows else []
    summary["compare"] = compare

    ok_all = all(c["ok"] for c in checks)
    unc = list(reading.uncertainties)
    for blk in blocks:
        unc += [f"`{blk.key}`: {u}" for u in blk.uncertain]
        for ln in blk.lines:
            unc += [f"`{blk.key}` band {ln.band}: {u}" for u in ln.uncertain]
            unc += [f"`{blk.key}` numeral `{n.text}`: {n.note}" for n in ln.numerals if n.uncertain]
    if reading.table:
        unc += [f"row `{r.key}`: {u}" for r in reading.table.rows for u in r.uncertain]
        unc += [f"row `{r.key}` numeral `{n.text}`: {n.note}" for r in reading.table.rows for n in r.numerals
                if n.uncertain]
    warnings = [c for c in checks if c.get("severity") == "warning"]
    summary["decisions"] = unc
    lines += [f"# Review packet: {region.region_id} — {reading.title}", "",
              f"**STATUS: {status['status'].upper()}**" + (f" ({status.get('reason')})" if status.get("reason") else "")
              + ". Units derived from this reading carry `reading.status = " + status["status"] + "`.", "",
              "| | |", "|---|---|",
              f"| Source | {region.doc} page {region.page}, bbox {region.bbox} pt (PDF points) |",
              f"| Native image | {region.native['width']}x{region.native['height']} px, sha256 `{region.native['sha256']}` |"
              if region.native else "| Native image | none (rendered crop) |",
              f"| Crop | `{region.crop['path']}` ({region.crop['dpi']} dpi render), page context `{region.context['path']}` |",
              f"| Reading file | `{relpath(reading_path, root) if reading_path else ''}` |",
              f"| Review subject sha256 | `{subject['sha256']}` — an approval pins this value. It covers the "
              f"{subject['covers']}. |",
              f"| Prepared by | {reading.prepared_by} |",
              f"| Method | {reading.method} |", "",
              "## Checks run on this reading", "",
              "| Check | Result | Detail |", "|---|---|---|"]
    for c in checks:
        res = "WARNING" if c.get("severity") == "warning" else \
            ("PARTIAL" if c.get("result") == "partial" else ("pass" if c["ok"] else "FAIL"))
        lines.append(f"| {c['check']} | {res} | {c['detail'].replace('|', '/')} |")
    lines += ["", f"All checks pass: **{'yes' if ok_all else 'NO'}**.", "",
              "## What the checks prove, and what they do not", "",
              "They prove: the reading points at the detected region (RD1) and at the same image bytes (RD2); "
              "a table reading has the row and column count the pixels show (RD3) and exactly one cell per column, "
              "with blanks declared (RD8); every text band outside a table grid is covered by a reading line (RD4); "
              "Arabic is stored as logical letters with a separate translation (RD5); every numeral in Arabic text or "
              "Arabic/mixed cells is declared and the stored text, rendered right to left, puts its glyphs in the "
              "order the crop shows (RD6).", "",
              "They do NOT prove: that any word, letter, mark, digit or value is the one printed; that a translation "
              "is right; what a value means (maximum, minimum, range, target); that nothing was cut off at the image "
              "edge" + (" (RD7 warns that it may have been)" if warnings else "") + ". Those are your decisions. "
              "Passing checks never approve a reading.", "",
              "## Points recorded for your decision", "",
              "From the reading's recorded uncertainties; each is a question for you, not something the program decided.", ""]
    lines += [f"{i}. {u}" for i, u in enumerate(unc, 1)]
    lines += [f"{len(unc) + 1}. Read every segment below against its crop and either approve the reading as a whole "
              "or correct the reading file (see the end of this packet)."]
    if nums:
        lines += ["", "## Numerals", "",
                  "Stored text is in logical order; the program renders it and compares the glyph order with what the "
                  "crop shows. The glyph-shape comparison is advisory only.", ""]
        for n in nums:
            where = f"cell `{n['column']}`" if n.get("column") else f"band {n['band']}"
            lines.append(f"- `{n['block']}` {where}: stored `{n['token']}`, crop shows `{n['visual_ltr_expected']}` "
                         f"(left to right). Render check: **{n['render_check'].get('result', 'pass').upper()}** "
                         f"({n['render_check']['detail']}). Meaning: {n['meaning']}."
                         + (f" **Uncertain.** Alternatives: {'; '.join(n['alternatives'])}" if n['uncertain'] else ""))
            if "glyph_advisory" in n:
                g = n["glyph_advisory"]
                det = ", ".join(f"{x['glyph']}" + (f" (best {x['best'][0]} {x['best'][1]}, next {x['second'][0]} "
                                                    f"{x['second'][1]}, margin {x['margin']}"
                                                    + (", LOW" if x.get('low_confidence') else "") + ")"
                                                    if x['kind'] == 'digit' else "") for x in g["glyphs"])
                lines.append(f"  - glyph-shape advisory, left to right: {det}")
            if "image" in n:
                lines.append(f"  - ![numeral]({rel(n['image'])})")
    lines += ["", "## Side-by-side", ""] + [f"![compare]({rel(c)})" for c in compare]
    segs = _segments(reading, region, ev)
    lines += ["", "## Line by line (each crop beside its reading)", "",
              "| Segment | Source crop | Proposed reading | Translation / notes |", "|---|---|---|---|"]
    for label, crop, text, _lang, note in segs:
        cell = lambda t: t.replace("|", "\\|")  # noqa: E731
        lines.append(f"| {label} | " + (f"![crop]({rel(crop)})" if crop else "—") + f" | {cell(text)} | {cell(note)} |")
    lines += ["", "## How to approve or correct", "",
              f"1. Correct `{relpath(reading_path, root) if reading_path else ''}` directly if anything is wrong, "
              "including adding or removing uncertainties.",
              f"2. When it is right, record your approval yourself: `python -m tenderpack approve {region.region_id} "
              f"--reviewer \"Your Name\"`. It refuses placeholder names, re-detects the region from the source PDF, "
              f"re-runs the checks, and appends to `{approvals_path}` your name, today's date and the review subject "
              "sha256 above. The program never writes an approval by itself.",
              "3. Re-run `python -m tenderpack ingest`. Any later change to the reading, its uncertainties, the source "
              "PDF, the region's position or the image makes the reading pending again."]
    write_text(rdir / "packet.md", "\n".join(lines) + "\n")
    write_text(rdir / "packet.html", _packet_html(region, reading, status, subject, checks, nums, unc, segs, compare,
                                                  base, relpath(reading_path, root) if reading_path else "", approvals_path))
    summary["html"] = relpath(rdir / "packet.html", base)
    write_text(rdir / "packet.json", json.dumps(summary, ensure_ascii=False, indent=1, sort_keys=True, default=str) + "\n")
    return summary


def _segments(reading: Reading, region: Region, ev: dict) -> list[tuple[str, str | None, str, str, str]]:
    """(label, crop path relative to the build dir, proposed reading, lang, note) for every piece read."""
    segs = []
    if reading.table is not None:
        t = reading.table
        lang = "ar" if t.direction == "rtl" else "en"
        if 0 in ev["row_crops"]:
            segs.append(("header row", ev["row_crops"][0], " | ".join(c.heading for c in t.columns), lang,
                         f"table direction {t.direction}" + (": the first column is the rightmost on the page"
                                                             if t.direction == "rtl" else "")))
            for ci, c in enumerate(t.columns):
                segs.append((f"&nbsp;&nbsp;heading `{c.key}`", ev["cell_crops"].get((0, _grid_col(reading, ci))),
                             c.heading, c.lang, f"column language {c.lang}"))
        for i, r in enumerate(t.rows, 1):
            if i not in ev["row_crops"]:
                continue                                       # grid mismatch: reported by RD3
            segs.append((f"row `{r.key}`", ev["row_crops"][i], "", lang, "; ".join(r.uncertain)))
            for ci, c in enumerate(t.columns):
                val = r.cells.get(c.key, "")
                shown = val if val else ("*(blank, declared)*" if c.key in r.blank else "*(empty, NOT declared)*")
                note = "; ".join(f"numeral `{n.text}` shows `{n.visual_ltr_expected}` left to right"
                                 for n in r.numerals if n.column == c.key)
                segs.append((f"&nbsp;&nbsp;`{r.key}`.`{c.key}`", ev["cell_crops"].get((i, _grid_col(reading, ci))),
                             shown, c.lang, note))
    if reading.content_type == "graphic":
        segs.append(("drawing", region.crop["path"] if region.crop else None, reading.description or "", "en", ""))
    for blk in reading.all_blocks():
        for ln in blk.lines:
            segs.append((f"`{blk.key}` band {ln.band} {ln.side}", ev["band_crops"].get((ln.band, ln.side)), ln.source,
                         blk.lang, blk.translation or ""))
    return segs


def _img(base: Path, path: str | None, max_w: int | None = None) -> str:
    if not path:
        return "—"
    data = base64.b64encode((base / path).read_bytes()).decode("ascii")
    style = f' style="max-width:{max_w}px"' if max_w else ""
    return f'<img src="data:image/png;base64,{data}"{style}>'


def _md_inline(t: str) -> str:
    """The few markdown marks used in segment labels and values, as HTML."""
    t = html.escape(t).replace("&amp;nbsp;", "&nbsp;")
    t = re.sub(r"`([^`]*)`", r"<code>\1</code>", t)
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", t)


def _packet_html(region, reading, status, subject, checks, nums, unc, segs, compare, base, reading_file,
                 approvals_path) -> str:
    """Self-contained review page: every crop embedded beside the reading it supports."""
    e = html.escape
    rows = []
    for label, crop, text, lang, note in segs:
        d = "rtl" if lang in ("ar", "mixed") else "ltr"
        rows.append(f"<tr><td>{_md_inline(label)}</td><td>{_img(base, crop, 900)}</td>"
                    f'<td dir="{d}" class="v">{_md_inline(text)}</td><td>{_md_inline(note)}</td></tr>')
    label = lambda c: ("WARNING" if c.get("severity") == "warning" else "PARTIAL" if c.get("result") == "partial"  # noqa: E731
                       else "pass" if c["ok"] else "FAIL")
    chk = "".join(f"<tr><td>{c['check']}</td><td class=\"{'ok' if label(c) == 'pass' else 'w' if label(c) in ('WARNING', 'PARTIAL') else 'bad'}\">"
                  f"{label(c)}</td>"
                  f"<td>{e(c['detail'])}</td></tr>" for c in checks)
    num = "".join(f"<li><code>{e(n['block'])}</code> {e(str(n.get('column') or 'band ' + str(n['band'])))}: stored "
                  f"<b dir=\"rtl\">{e(n['token'])}</b>, crop shows <b>{e(n['visual_ltr_expected'])}</b> left to right; "
                  f"render check <b>{e(n['render_check'].get('result', 'pass').upper())}</b>"
                  + (f"; <b class=\"bad\">uncertain</b>, alternatives: {e('; '.join(n['alternatives']))}" if n["uncertain"] else "")
                  + (f"<br>{_img(base, n['image'], 900)}" if n.get("image") else "") + "</li>" for n in nums)
    dec = "".join(f"<li>{_md_inline(u)}</li>" for u in unc)
    failing = ", ".join(sorted({c["check"] for c in checks if not c["ok"]}))
    warns = "; ".join(e(c["detail"]) for c in checks if c.get("severity") in ("warning", "partial"))
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Review {e(region.region_id)}</title>
<style>body{{font:14px/1.45 system-ui,sans-serif;margin:16px;max-width:1500px}}table{{border-collapse:collapse}}
td,th{{border:1px solid #ccc;padding:4px 6px;vertical-align:top}}td.v{{min-width:340px;font-size:18px;font-family:'Noto Naskh Arabic',serif}}
.ok{{color:#176117}}.bad{{color:#b00020;font-weight:bold}}.w{{color:#9a5b00;font-weight:bold}}
.status{{padding:8px 12px;background:#fff3cd;border:1px solid #e0c060;font-weight:bold}}img{{max-width:100%}}</style></head><body>
<h1>Review packet {e(region.region_id)}: {e(reading.title)}</h1>
<p class="status">STATUS: {e(status['status'].upper())}{(' (' + e(status['reason']) + ')') if status.get('reason') else ''}.
Nothing here is approved until you approve it.</p>
<p>Source {e(region.doc)} page {region.page}, bbox {region.bbox} pt. Reading file <code>{e(reading_file)}</code>.
Prepared by: {e(reading.prepared_by)}. Review subject sha256 <code>{subject['sha256']}</code> (covers {e(subject['covers'])}).</p>
<h2>What the checks prove, and what they do not</h2>
<p>They prove: the reading points at the detected region and image bytes (RD1, RD2); tables have the row and column
count the pixels show and one cell per column with blanks declared (RD3, RD8); every text band outside a table grid is
read (RD4); Arabic is stored as logical letters with a separate translation (RD5); declared numerals render right to left
in the order the crop shows (RD6).</p>
<p><b>They do not prove</b> that any word, letter, mark, digit or value is the one printed, that a translation is right,
what a value means, or that nothing was cut off at the image edge. Those are your decisions.</p>
<h2>Points recorded for your decision</h2><ol>{dec}<li>Read every segment below against its crop; approve the reading as
a whole or correct the reading file.</li></ol>
<h2>Each crop beside its reading</h2><table><tr><th>Segment</th><th>Source crop (native pixels)</th>
<th>Proposed reading</th><th>Translation / notes</th></tr>{''.join(rows)}</table>
{'<h2>Numerals</h2><ul>' + num + '</ul>' if nums else ''}
<h2>Checks</h2><p>{sum(c['ok'] for c in checks)} of {len(checks)} pass; failing: {failing or 'none'}; warnings: {warns or 'none'}.</p>
<details{' open' if failing or warns else ''}><summary>All check results</summary><table><tr><th>Check</th><th>Result</th>
<th>Detail</th></tr>{chk}</table></details>
<h2>The reading as rendered by the program</h2>{''.join(_img(base, c) for c in compare)}
<h2>How to approve or correct</h2><ol><li>Correct <code>{e(reading_file)}</code> if anything is wrong, including its uncertainties.</li>
<li>When it is right, run yourself: <code>python -m tenderpack approve {e(region.region_id)} --reviewer "Your Name"</code>
(written to <code>{e(approvals_path)}</code>; placeholders are refused).</li>
<li>Re-run <code>python -m tenderpack ingest</code>. Any later change to the reading, its uncertainties or its evidence makes it pending again.</li></ol>
</body></html>
"""
