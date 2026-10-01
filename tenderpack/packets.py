"""Review packets: evidence crops next to the proposed reading, for a person to approve or correct.

For each region with a reading, writes build/review/<region_id>/:
  packet.md          status, provenance, checks, uncertainties, and every block / row with its crop
  compare-N.png      left: source crop at native resolution; right: the proposed reading as rendered
                     by the program (Arabic shaped and bidi-ordered by the bundled Noto Naskh font)
  bands/, rows/, cells/   native-pixel crops (never downscaled; diacritics vanish when scaled)
  numerals/          for declared numerals: high-dpi crop of the printed glyphs beside renders of the
                     stored token and its alternatives, plus the glyph-shape advisory
For regions without a reading, writes a packet that says so (UNREAD) with crops and bands.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import pymupdf

from . import arabic
from .readings import Block, Reading, check_reading, review_status
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
                "bands": text_bands(gray), "grid": None}
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
    text = _html_escape(line.source)
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
                ok, how = arabic.visual_check(ln.source, n.visual_ltr_expected)
                item["render_check"] = {"ok": ok, "detail": how}
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
    return out


# ------------------------------------------------------------------ packet

def write_packet(pdf: pymupdf.Document, region: Region, reading: Reading | None, approvals: list[dict],
                 ev: dict, out: Path, base: Path, root: Path, reading_path: Path | None) -> dict:
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

    status = review_status(reading, approvals)
    checks = check_reading(reading, region, pdf)
    nums = numeral_evidence(pdf, region, reading, rdir, base)
    summary.update(status=status["status"], status_reason=status.get("reason"), content_sha256=status["content_sha256"],
                   checks=checks, numerals=nums, reading=relpath(reading_path, root) if reading_path else None)

    rows = []
    blocks = reading.all_blocks()
    if reading.table is not None:
        t = reading.table
        for blk in [t.title] + ([t.qualifier] if t.qualifier else []):
            for ln in blk.lines:
                rows.append((f"{blk.key} (band {ln.band})", ev["band_crops"][(ln.band, ln.side)],
                             _block_html(blk, ln), blk.lang, [f"! {u}" for u in blk.uncertain]))
        header = " | ".join(c.heading for c in t.columns)
        rows.append(("header row (grid row 0)", ev["row_crops"][0], _html_escape(header), "en", []))
        for i, r in enumerate(t.rows, 1):
            cells = " | ".join(_html_escape(r.cells.get(c.key, "")) for c in t.columns)
            rows.append((f"row {r.key} (grid row {i})", ev["row_crops"][i], cells, "en", [f"! {u}" for u in r.uncertain]))
        for blk in t.notes:
            for ln in blk.lines:
                rows.append((f"{blk.key} (band {ln.band})", ev["band_crops"][(ln.band, ln.side)],
                             _block_html(blk, ln), blk.lang, [f"! {u}" for u in blk.uncertain]))
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
    compare = _render_rows(rows, rdir / "compare", base)
    summary["compare"] = compare

    ok_all = all(c["ok"] for c in checks)
    lines += [f"# Review packet: {region.region_id} — {reading.title}", "",
              f"**STATUS: {status['status'].upper()}**" + (f" ({status.get('reason')})" if status.get("reason") else "")
              + ". Units derived from this reading carry `reading.status = " + status["status"] + "`.", "",
              "| | |", "|---|---|",
              f"| Source | {region.doc} page {region.page}, bbox {region.bbox} pt (PDF points) |",
              f"| Native image | {region.native['width']}x{region.native['height']} px, sha256 `{region.native['sha256']}` |"
              if region.native else "| Native image | none (rendered crop) |",
              f"| Crop | `{region.crop['path']}` ({region.crop['dpi']} dpi render), page context `{region.context['path']}` |",
              f"| Reading file | `{relpath(reading_path, root) if reading_path else ''}` |",
              f"| Content sha256 | `{status['content_sha256']}` (an approval pins this value) |",
              f"| Prepared by | {reading.prepared_by} |",
              f"| Method | {reading.method} |", "",
              "## Checks run on this reading", "",
              "| Check | Result | Detail |", "|---|---|---|"]
    for c in checks:
        res = "WARNING" if c.get("severity") == "warning" else ("pass" if c["ok"] else "FAIL")
        lines.append(f"| {c['check']} | {res} | {c['detail'].replace('|', '/')} |")
    lines += ["", f"All checks pass: **{'yes' if ok_all else 'NO'}**. Passing checks do not approve the reading; "
                  "they show the reading is complete, positioned and renders as printed. Whether each word and value "
                  "is right is the reviewer's call.", "", "## Uncertainties to resolve", ""]
    unc = list(reading.uncertainties)
    for blk in blocks:
        unc += [f"`{blk.key}`: {u}" for u in blk.uncertain]
        for ln in blk.lines:
            unc += [f"`{blk.key}` band {ln.band}: {u}" for u in ln.uncertain]
            unc += [f"`{blk.key}` numeral `{n.text}`: {n.note}" for n in ln.numerals if n.uncertain]
    if reading.table:
        unc += [f"row `{r.key}`: {u}" for r in reading.table.rows for u in r.uncertain]
    lines += [f"{i}. {u}" for i, u in enumerate(unc, 1)] or ["None recorded."]
    if nums:
        lines += ["", "## Numerals", "",
                  "Stored text is in logical order; the program renders it and compares the glyph order with what the "
                  "crop shows. The glyph-shape comparison is advisory only.", ""]
        for n in nums:
            lines.append(f"- `{n['block']}` band {n['band']}: stored `{n['token']}`, crop shows `{n['visual_ltr_expected']}` "
                         f"(left to right). Render check: **{'pass' if n['render_check']['ok'] else 'FAIL'}** "
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
    lines += ["", "## Line by line", "", "| Segment | Source crop | Proposed source | Translation / notes |", "|---|---|---|---|"]
    if reading.table is not None:
        for i, r in enumerate(reading.table.rows, 1):
            cells = "<br>".join(f"{c.heading}: {r.cells.get(c.key, '')}" for c in reading.table.columns)
            cellc = " ".join(f"![c{c}]({rel(ev['cell_crops'][(i, c)])})" for c in range(len(reading.table.columns)))
            lines.append(f"| row `{r.key}` | ![row]({rel(ev['row_crops'][i])})<br>{cellc} | {cells} | "
                         f"{'; '.join(r.uncertain)} |")
    for blk in blocks:
        for ln in blk.lines:
            lines.append(f"| `{blk.key}` band {ln.band} {ln.side} | ![b]({rel(ev['band_crops'][(ln.band, ln.side)])}) | "
                         f"{ln.source} | {blk.translation or ''} |")
    lines += ["", "## How to approve or correct", "",
              f"1. Correct `{relpath(reading_path, root) if reading_path else ''}` directly if anything is wrong "
              "(the content sha256 will change).",
              f"2. When it is right, record approval: `python -m tenderpack approve {region.region_id} --reviewer \"<name>\"`. "
              "This appends to `curation/approvals.yaml` with today's date and the current content sha256.",
              "3. Re-run `python -m tenderpack ingest`. Any later edit to the reading voids the approval automatically."]
    write_text(rdir / "packet.md", "\n".join(lines) + "\n")
    write_text(rdir / "packet.json", json.dumps(summary, ensure_ascii=False, indent=1, sort_keys=True, default=str) + "\n")
    return summary
