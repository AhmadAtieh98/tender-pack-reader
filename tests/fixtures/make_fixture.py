"""Builds a synthetic test pack (NOT tender content) and records what it placed.

The expectations are written by the builder from what it drew, not from the program's
output, so tests compare the segmenter against an independent oracle.

Pages:
  1  clause with a unit exponent (m³), clause with a footnote marker, footnote body at the foot;
     a legitimate rotated margin note (90 deg, dark) that must stay content; the watermark
  2  clause, table caption, ruled table with a white-on-dark header and 2 rows near the foot
  3  the same table continues: repeated header + 3 rows; then a clause; and a decoy identical to
     the watermark except for its dark colour (must stay content)
  4  mixed page: paragraph, raster image holding a small ruled table in English and Arabic,
     paragraph, and a vector-drawn curve with no text (signature-like)
  5  a raster image of a sentence with an invisible text layer on top (as an OCR'd scan has)
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pymupdf
import yaml

W, H = 595.0, 842.0
GREY = (0x5A / 255, 0x5A / 255, 0x5A / 255)
INK = (0x1A / 255, 0x1A / 255, 0x1A / 255)
WM = (0xDB / 255, 0xDB / 255, 0xDB / 255)
# Base-14 Helvetica cannot encode an em dash (it renders as a middle dot), so the fixture uses ASCII
# and its own WATERMARK rule text; every other attribute of the real rule is kept.
WATERMARK = "FICTIONAL - ASSESSMENT PACK"


def furniture(page: pymupdf.Page, n: int) -> None:
    page.insert_text((62.7, 38), "Synthetic Test Volume", fontname="helv", fontsize=6.8, color=GREY)
    page.insert_text((62.7, 806), f"Page {n}", fontname="helv", fontsize=6.4, color=GREY)
    p = pymupdf.Point(150, 640)
    page.insert_text(p, WATERMARK, fontname="hebo", fontsize=34, color=WM, morph=(p, pymupdf.Matrix(52)))


def clause(page, y, number, text, size=9.6):
    page.insert_text((62.7, y), number, fontname="tibo", fontsize=size, color=INK)
    page.insert_text((88.0, y), text, fontname="tiro", fontsize=size, color=INK)


def ruled_table(page, x0, y0, widths, rows, header=None, row_h=17.0):
    """rows: list of lists of strings. Returns bottom y."""
    x1 = x0 + sum(widths)
    y = y0
    allrows = ([header] if header else []) + rows
    for ri, r in enumerate(allrows):
        if header and ri == 0:
            page.draw_rect(pymupdf.Rect(x0, y, x1, y + row_h), color=None, fill=(0.23, 0.23, 0.23))
        cx = x0
        for ci, cell in enumerate(r):
            colour = (1, 1, 1) if (header and ri == 0) else INK
            page.insert_text((cx + 4, y + 12), cell, fontname="hebo" if (header and ri == 0) else "tiro",
                             fontsize=8.2, color=colour)
            cx += widths[ci]
        y += row_h
    # rules
    yy = y0
    for _ in range(len(allrows) + 1):
        page.draw_line((x0, yy), (x1, yy), color=(0.72, 0.72, 0.72), width=0.6)
        yy += row_h
    cx = x0
    for w in widths + [0]:
        page.draw_line((cx, y0), (cx, y), color=(0.72, 0.72, 0.72), width=0.6)
        cx += w
    return y


def raster_table_image() -> pymupdf.Pixmap:
    """A small bilingual ruled table, rendered to a raster (as a scanned insert would be)."""
    doc = pymupdf.open()
    pg = doc.new_page(width=360, height=110)
    html = ('<table style="border-collapse:collapse; font-size:11px; width:340px">'
            '<tr><td style="border:1px solid #000; padding:3px">Item</td>'
            '<td style="border:1px solid #000; padding:3px">Limit</td>'
            '<td style="border:1px solid #000; padding:3px" dir="rtl">البند</td></tr>'
            '<tr><td style="border:1px solid #000; padding:3px">Noise at night</td>'
            '<td style="border:1px solid #000; padding:3px">45 dB(A)</td>'
            '<td style="border:1px solid #000; padding:3px" dir="rtl">الضوضاء ليلاً ٤٥</td></tr>'
            '<tr><td style="border:1px solid #000; padding:3px">Odour</td>'
            '<td style="border:1px solid #000; padding:3px">5 OU</td>'
            '<td style="border:1px solid #000; padding:3px" dir="rtl">الرائحة ٥</td></tr></table>')
    pg.insert_htmlbox(pymupdf.Rect(8, 8, 352, 102), html)
    return pg.get_pixmap(dpi=150)


def sentence_image(text: str) -> pymupdf.Pixmap:
    doc = pymupdf.open()
    pg = doc.new_page(width=420, height=40)
    pg.insert_text((10, 26), text, fontname="tiro", fontsize=13, color=(0, 0, 0))
    return pg.get_pixmap(dpi=150)


def build(out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open()
    exp: dict = {"pages": 5, "watermark_per_page": 1}

    # ---- page 1
    p = doc.new_page(width=W, height=H)
    furniture(p, 1)
    p.insert_text((62.7, 90), "SECTION 1 - TEST CLAUSES", fontname="hebo", fontsize=13, color=INK)
    clause(p, 120, "1.1", "The plant shall treat not less than 50,000 m")
    p.insert_text((88.0 + pymupdf.get_text_length("The plant shall treat not less than 50,000 m", "tiro", 9.6), 116.5),
                  "3", fontname="tiro", fontsize=6.6, color=INK)
    x_after = 88.0 + pymupdf.get_text_length("The plant shall treat not less than 50,000 m", "tiro", 9.6) + 3.7
    p.insert_text((x_after, 120), "/day.", fontname="tiro", fontsize=9.6, color=INK)
    clause(p, 140, "1.2", "The Bidder shall submit three copies of Form 9-A.")
    x_fn = 88.0 + pymupdf.get_text_length("The Bidder shall submit three copies of Form 9-A.", "tiro", 9.6)
    p.insert_text((x_fn, 136.5), "7", fontname="tiro", fontsize=6.6, color=INK)
    p.draw_line((62.7, 742), (200, 742), color=(0.1, 0.1, 0.1), width=0.5)
    p.insert_text((62.7, 752), "7", fontname="tiro", fontsize=5.8, color=INK)
    p.insert_text((67.5, 754), "A Bidder that submits fewer copies shall be disqualified.", fontname="tiro",
                  fontsize=7.2, color=INK)
    m = pymupdf.Point(560, 400)
    p.insert_text(m, "Amended by Addendum No. 9, see Clause 1.2", fontname="helv", fontsize=8, color=INK,
                  morph=(m, pymupdf.Matrix(90)))
    exp["p1"] = {"clauses": ["1.1", "1.2"], "unit_exponent_in": "1.1", "footnote": {"number": "7", "host": "1.2",
                 "text_contains": "shall be disqualified"},
                 "rotated_content": "Amended by Addendum No. 9, see Clause 1.2"}

    # ---- page 2
    p = doc.new_page(width=W, height=H)
    furniture(p, 2)
    clause(p, 90, "2.1", "The parameters in Table 9-1 apply.")
    p.insert_text((71, 680), "Table 9-1 - Test parameters", fontname="hebo", fontsize=8.6, color=INK)
    ruled_table(p, 71, 690, [80, 220, 80], [["9-1.1", "Average flow", "100"], ["9-1.2", "Peak flow", "150"]],
                header=["Ref", "Criterion", "Value"])

    exp["p2_p3_table"] = {"unit": "T9-1", "pages": [2, 3], "rows": ["9-1.1", "9-1.2", "9-1.3", "9-1.4", "9-1.5"],
                          "row_pages": [2, 2, 3, 3, 3], "repeated_header_page": 3}
    exp["decoy_rotated_dark_watermark_words_on_page"] = 3

    # ---- page 3
    p = doc.new_page(width=W, height=H)
    furniture(p, 3)
    ruled_table(p, 71, 68, [80, 220, 80],
                [["9-1.3", "Minimum flow", "40"], ["9-1.4", "Storm flow", "300"], ["9-1.5", "Velocity", "1.2"]],
                header=["Ref", "Criterion", "Value"])
    clause(p, 180, "3.1", "Flows shall be measured at the inlet works.")
    # decoy: identical to the watermark in text, font, size and angle; differs ONLY in colour (dark ink).
    # A rule that ignored colour would wrongly exclude it.
    d = pymupdf.Point(240, 800)
    p.insert_text(d, WATERMARK, fontname="hebo", fontsize=34, color=INK, morph=(d, pymupdf.Matrix(52)))

    # ---- page 4: mixed text / image / graphic
    p = doc.new_page(width=W, height=H)
    furniture(p, 4)
    clause(p, 90, "4.1", "The limits in the inserted table below apply at the site boundary.")
    img = raster_table_image()
    rect = pymupdf.Rect(80, 110, 80 + img.w * 0.48, 110 + img.h * 0.48)
    p.insert_image(rect, pixmap=img)
    clause(p, rect.y1 + 24, "4.2", "Readings shall be taken quarterly.")
    sig = p.new_shape()
    sig.draw_bezier((90, 420), (120, 380), (150, 460), (180, 410))
    sig.draw_bezier((180, 410), (210, 370), (230, 450), (260, 400))
    sig.finish(color=(0, 0, 0.4), width=1.2)
    sig.commit()
    exp["p4"] = {"clauses": ["4.1", "4.2"], "image_rect": [round(v, 1) for v in rect], "vector_graphic": True,
                 "image_text_rows": 3, "image_text_cols": 3}

    # ---- page 5: image with invisible text layer
    p = doc.new_page(width=W, height=H)
    furniture(p, 5)
    sentence = "Scanned sentence: deliveries before 10:00 only."
    simg = sentence_image(sentence)
    r5 = pymupdf.Rect(80, 100, 80 + simg.w * 0.48, 100 + simg.h * 0.48)
    p.insert_image(r5, pixmap=simg)
    p.insert_text((r5.x0 + 4.8, r5.y0 + 12.5), sentence, fontname="tiro", fontsize=6.2, render_mode=3)
    exp["p5"] = {"invisible_text": sentence}

    doc.set_metadata({"producer": "tests/fixtures/make_fixture.py", "creationDate": "D:20261001000000Z",
                      "modDate": "D:20261001000000Z"})
    pdf_path = out / "SYN-01_Synthetic_Test_Volume.pdf"
    doc.save(pdf_path, garbage=3, deflate=True, no_new_id=True)
    data = pdf_path.read_bytes()
    root = Path(__file__).resolve().parents[2]
    def rel(q):
        q = Path(q).resolve()
        return q.relative_to(root).as_posix() if q.is_relative_to(root) else q.as_posix()
    manifest = {"files": [{"path": rel(pdf_path), "sha256": hashlib.sha256(data).hexdigest(), "pages": 5}]}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    furn = yaml.safe_load((root / "config/furniture.yaml").read_text(encoding="utf-8"))
    furn["rules"] = [r for r in furn["rules"] if r["id"] in ("WATERMARK", "FOOTER-PAGE")]
    for r in furn["rules"]:
        if r["id"] == "WATERMARK":
            r["text"] = WATERMARK
    furn["rules"] += [
        {"id": "HEADER-SYN", "reason": "synthetic running header", "max_y1": 45.0, "color": "#5a5a5a",
         "size": [6.0, 7.5], "pattern": "^Synthetic Test Volume$"}]
    (out / "furniture.yaml").write_text(yaml.safe_dump(furn, allow_unicode=True, sort_keys=False), encoding="utf-8")
    pack = {"pack_id": "SYNTHETIC-FIXTURE (not tender content)", "manifest": rel(out / "manifest.json"),
            "furniture": rel(out / "furniture.yaml"), "readings_dir": rel(out / "readings"),
            "approvals": rel(out / "approvals.yaml"),
            "documents": [{"doc_id": "SYN-01", "kind": "volume", "path": rel(pdf_path)}]}
    (out / "pack.yaml").write_text(yaml.safe_dump(pack, sort_keys=False), encoding="utf-8")
    (out / "expected.yaml").write_text(yaml.safe_dump(exp, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return exp


if __name__ == "__main__":
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "out")
