"""Builds a synthetic future addendum, "Addendum No. 3" (ADD-03), and a 7-document drill pack around it.

NOT tender content: ADD-03 is invented for a drill. It lets the same path that handled ADD-01 and ADD-02
(ingest -> units -> `draft` -> op file -> amendment engine) run on an addendum nobody has seen yet.
The six real documents are used as received (same repository-relative paths, same manifest entries);
only ADD-03 is new.

Layout copies the received addenda (measured on ADD-02 with get_text("dict") and get_drawings()):
  A4 595.2756 x 841.8898; base-14 Type1 fonts with WinAnsiEncoding, as ReportLab wrote them
  furniture  watermark 'FICTIONAL — ASSESSMENT PACK' Helvetica-Bold 34 #dbdbdb, 52 deg, centred on the page;
             header 'Addendum No. 3' / 'NUPA/ISTP/2026/014' Helvetica 6.8 #5a5a5a (baseline 39.69, rule 45.35);
             footer disclaimer / 'Page N' Helvetica 6.4 #5a5a5a (baseline 809.29, rule 799.37)
  cover      dark band (#2a2a2a) with 'ADDENDUM NO. 3' Helvetica-Bold 15, 'Issued …' Helvetica-Bold 8.5 and
             'Tender …' Helvetica 8.5 in white; project title Helvetica-Bold 10.5; front matter Times-Roman 9.6
  body       headings Helvetica-Bold 13 at x 62.69; clause number Times-Bold 9.6 at x 62.69, text Times-Roman
             9.6 from x 74.69 (printed with three leading spaces), wrapped lines at x 99.54, leading 13.4;
             substituted words in Times-Bold, as in ADD-01/ADD-02
  Q&A table  ruled grid at x 56.69 / 90.71 / 300.47 / 538.58, header row 17.4 pt on #3a3a3a with white
             Helvetica-Bold 8.2 headings, body Times-Roman 8.2 (cell padding 4, leading 10.4), rules #b8b8b8 0.4 pt

The em dash and typographic quotes: PyMuPDF's insert_text writes characters below 256 as single bytes, and its
base-14 fonts are declared /WinAnsiEncoding, so the WinAnsi codes 0x97 (em dash), 0x91 / 0x92 (single quotes)
are written for '—', '‘', '’' — exactly the bytes in the received PDFs (ADD-02 page 1: '(FICTIONAL \\227
ASSESSMENT PACK) Tj'). Extraction gives back '—', '‘', '’', and span fonts are 'Helvetica', 'Helvetica-Bold',
'Times-Roman', 'Times-Bold'. The drill therefore uses config/furniture.yaml unchanged (copied byte for byte).
(Passing '—' itself to insert_text writes a middle dot, see make_fixture.py; TextWriter keeps '—' but embeds
the font, which extraction then names 'NimbusSans-Regular' etc.)

`expected.yaml` is written from the builder's own inputs (what it printed and the outcome each provision is
meant to drill), never from the program's output. Unit ids follow the segmenter's documented naming.

Usage:  python tests/fixtures/make_drill.py OUT_DIR
        python -m tenderpack ingest --pack OUT_DIR/pack.yaml --out SOME_BUILD_DIR
        python -m tenderpack draft ADD-03 --evidence SOME_BUILD_DIR
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

import pymupdf
import yaml

ROOT = Path(__file__).resolve().parents[2]
PDF_NAME = "ADD-03_Addendum_No_3.pdf"
PACK_ID = "NUPA-ISTP-2026-014-DRILL"

# ---------------------------------------------------------------------------------------------- page geometry
W, H = 595.2756, 841.8898                        # A4, as in the received addenda
L, R = 56.69, 538.58                             # header/footer rules, cover band, Q&A table outer edges
TEXT_X, TEXT_R = 62.69, 532.58                   # text column
CLAUSE_TEXT_X, CLAUSE_WRAP_X = 74.69, 99.54      # clause text after the number; wrapped clause lines
HEADER_Y, HEADER_RULE_Y = 39.69, 45.35
FOOTER_Y, FOOTER_RULE_Y = 809.29, 799.37
BAND = (L, 74.36, R, 114.36)
QA_COLS = [56.69, 90.71, 300.47, 538.58]

BODY, LEAD = 9.6, 13.4                           # body size and leading
AFTER_PARA = 18.4                                # last baseline of a paragraph/clause -> next one's first baseline
BEFORE_HEAD = 30.8                               # last baseline -> section heading baseline
AFTER_HEAD = 19.6                                # section heading baseline -> first clause baseline
HEAD_TO_TABLE = 10.0                             # section heading baseline -> top rule of the table
CELL, CELL_LEAD, CELL_ROW, CELL_BASE, CELL_PAD = 8.2, 10.4, 17.4, 11.7, 4.0

INK = (26 / 255,) * 3                            # #1a1a1a
GREY = (90 / 255,) * 3                           # #5a5a5a
WM = (219 / 255,) * 3                            # #dbdbdb
RULE = (184 / 255,) * 3                          # #b8b8b8
BAND_FILL = (42 / 255,) * 3                      # #2a2a2a
HEAD_FILL = (58 / 255,) * 3                      # #3a3a3a
WHITE = (1.0, 1.0, 1.0)

WATERMARK = "FICTIONAL — ASSESSMENT PACK"
DISCLAIMER = "FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender."
HEADER_TITLE, HEADER_REF = "Addendum No. 3", "NUPA/ISTP/2026/014"

FONTS = {name: pymupdf.Font(name) for name in ("helv", "hebo", "tiro", "tibo")}
FONT_NAMES = {"helv": "Helvetica", "hebo": "Helvetica-Bold", "tiro": "Times-Roman", "tibo": "Times-Bold"}
# Unicode -> WinAnsiEncoding byte (written as the character with that code; insert_text emits it as one byte)
WINANSI = str.maketrans({"—": "\x97", "–": "\x96", "‘": "\x91", "’": "\x92", "“": "\x93", "”": "\x94"})

# ---------------------------------------------------------------------------------------------- content
ISSUED = "Issued 5 November 2026"
FRONT = [
    "This Addendum amends the Proposal Due Date, Volume V Clause 31.3, Volume II Table 2-4 and Volume II Clause 4.4, "
    "deletes Volume I Clause 8.6, and responds to clarification requests 15 and 16.",
    "This Addendum forms part of the RFP Documents and takes precedence in accordance with Volume I Clause 3.2. "
    "Bidders shall acknowledge receipt in Form 4-A. All other terms of the RFP Documents remain unchanged.",
]
R_, B_ = "tiro", "tibo"
# (heading, [(clause number, [(text, font), ...]), ...], intended outcome per clause)
SECTIONS = [
    ("1. RECITALS", [
        ("1.1", [("This Addendum is issued under Volume I Clause 5.3 and takes precedence in accordance with "
                  "Volume I Clause 3.2.", R_)])]),
    ("2. AMENDMENT TO VOLUME I CLAUSE 6.1", [
        ("2.1", [("In Volume I Clause 6.1, ‘Thursday 26 November 2026’ is deleted and ‘", R_),
                 ("Thursday 10 December 2026", B_), ("’ is substituted.", R_)])]),
    ("3. AMENDMENT TO VOLUME V CLAUSE 31.3", [
        ("3.1", [("In Volume V Clause 31.3, ‘seventy-two (72) hours’ is deleted and ‘", R_),
                 ("forty-eight (48) hours", B_), ("’ is substituted.", R_)])]),
    ("4. DELETION OF VOLUME I CLAUSE 8.6", [
        ("4.1", [("Volume I Clause 8.6 (Local Content Certificate) is ", R_), ("deleted in its entirety", B_),
                 (".", R_)])]),
    ("5. AMENDMENT TO VOLUME II TABLE 2-4", [
        ("5.1", [("In Volume II Table 2-4, the limit for ", R_), ("Total Phosphorus (TP)", B_),
                 (" is amended from the value shown to ", R_), ("0.5 mg/l", B_),
                 (", assessed on the same basis. All other parameters in Table 2-4 are unchanged.", R_)])]),
    ("6. BID SECURITY", [
        ("6.1", [("The bid security period is extended by thirty days.", R_)])]),
    ("7. AMENDMENT TO VOLUME II CLAUSE 4.4", [
        ("7.1", [("In Volume II Clause 4.4, ‘seventy-two (72) hours’ is deleted and ‘", R_),
                 ("sixty (60) hours", B_), ("’ is substituted.", R_)])]),
]
QA_HEADING = "8. RESPONSES TO CLARIFICATION REQUESTS 15 TO 16"
QA_HEADER = ["No", "Bidder question", "Authority response"]
QA_ROWS = [
    ["15", "Does the 150-page limit in Volume I Clause 9.2 include the Form Sheets?",
     "No. The response to request 2 in Addendum No. 1 continues to apply."],
    ["16", "Addendum No. 1 moved the Proposal Due Date to 26 November 2026. Is that date firm?",
     "See Section 2 of this Addendum."],
]

# What each provision is meant to drill. Written here, from the wording above; never read back from the program.
INTENDED = {
    "ADD-03:cover/para1": {"draft": "no_effect", "why": "the addendum's issue date line (issued_from; stage date "
                                                        "2026-11-05, after ADD-02's 2026-10-22)"},
    "ADD-03:cover/para2": {"draft": "no_effect", "why": "cover text"},
    "ADD-03:cover/para3": {"draft": "annotate", "effect": "adds_obligation",
                           "why": "front matter: 'Bidders shall acknowledge receipt in Form 4-A' is an obligation; the rest "
                                  "summarises the addendum"},
    "ADD-03:1.1": {"draft": "no_effect", "why": "recital (section 1. RECITALS)"},
    "ADD-03:2.1": {"draft": "replace_text", "target": "VOL-I:6.1", "old": "Thursday 26 November 2026",
                   "new": "Thursday 10 December 2026", "engine": "valid",
                   "effect": "the Proposal Due Date moves from 26 November 2026 (ADD-01) to 10 December 2026; dates "
                             "computed from it are recomputed and interpretations pinned to it become STALE"},
    "ADD-03:3.1": {"draft": "replace_text", "target": "VOL-V:31.3", "old": "seventy-two (72) hours",
                   "new": "forty-eight (48) hours", "engine": "valid",
                   "effect": "only VOL-V:31.3 changes; VOL-II:4.4, which also said 'seventy-two (72) hours' until "
                             "ADD-02, is untouched"},
    "ADD-03:4.1": {"draft": "set_status", "target": "VOL-I:8.6", "status": "deleted", "engine": "valid",
                   "effect": "Local Content Certificate chain: deleted (ADD-01 4.1) -> reinstated (ADD-02 9.1) -> "
                             "deleted (ADD-03 4.1)"},
    "ADD-03:5.1": {"draft": "set_value", "target": "VOL-II:T2-4/TP", "column": "Limit", "new": "0.5",
                   "engine": "valid",
                   "effect": "a cell of an image-reading table whose reading (VOL-II-p3-r1) is still pending; the "
                             "result carries reading status pending"},
    "ADD-03:6.1": {"draft": "unresolved", "engine": "unresolved (addendum PARTIAL until a person writes the op or a "
                                                    "disposition)",
                   "why": "no recognised phrasing and no cited target: 'bid security period' could be the Bid Bond "
                          "validity or another period"},
    "ADD-03:7.1": {"draft": "replace_text", "target": "VOL-II:4.4", "old": "seventy-two (72) hours",
                   "new": "sixty (60) hours", "engine": "INVALID (C23)",
                   "effect": "ADD-02 4.1 already changed VOL-II:4.4 to 'ninety-six (96) hours', so the quoted old "
                             "words are not in the target; the op is listed and not applied, and the engine must not "
                             "retarget it to VOL-V:31.3 (which ADD-03 3.1 changes anyway)"},
    "ADD-03:Q15": {"draft": "unresolved", "cites": ["VOL-I:9.2"],
                   "effect": "negative control: cites a unit ADD-03 does not change (VOL-I:9.2, last changed by "
                             "ADD-02 2.1); nothing about it should be flagged by ADD-03"},
    "ADD-03:Q16": {"draft": "unresolved",
                   "effect": "quotes '26 November 2026', the value ADD-03 2.1 replaces: must be listed for review, "
                             "never revoked or changed automatically"},
}


# ---------------------------------------------------------------------------------------------- drawing helpers
def _width(s: str, font: str, size: float) -> float:
    return FONTS[font].text_length(s, fontsize=size)


def _text(page: pymupdf.Page, x: float, y: float, s: str, font: str, size: float, color=INK, morph=None) -> float:
    """Print `s` with its baseline origin at (x, y); returns the x where it ends."""
    enc = s.translate(WINANSI)
    bad = sorted({c for c in enc if ord(c) > 255})
    assert not bad, f"not encodable in WinAnsiEncoding: {bad!r} in {s!r}"
    page.insert_text((x, y), enc, fontname=font, fontsize=size, color=color, morph=morph)
    return x + _width(s, font, size)


def _rule(page: pymupdf.Page, p, q) -> None:
    page.draw_line(p, q, color=RULE, width=0.4)


def _wrap(runs: list[tuple[str, str]], first: float, rest: float, size: float, lead_in: str = ""):
    """Greedy word wrap of styled runs into lines of styled spans.

    `first` / `rest`: room on the first / following lines; `lead_in` (spaces, regular face) starts the first
    line. Words break only at spaces, so a quote and the bold words it opens stay on one line.
    Returns [[(text, font), ...] per line]."""
    words, gaps, cur = [], [], []
    for txt, font in runs:
        for ch in txt:
            if ch == " ":
                assert cur, f"double or leading space in {runs!r}"
                words.append(cur)
                gaps.append(font)
                cur = []
            else:
                cur.append((ch, font))
    assert cur, f"trailing space in {runs!r}"
    words.append(cur)

    def wlen(seq):
        return sum(_width("".join(c for c, _ in grp), grp[0][1], size) for grp in _groups(seq))

    lines, line, used = [], list(words[0]), wlen(words[0]) + _width(lead_in, R_, size)
    room = first
    for gap, word in zip(gaps, words[1:]):
        add = _width(" ", gap, size) + wlen(word)
        if used + add <= room + 1e-6:
            line += [(" ", gap)] + word
            used += add
        else:
            lines.append(line)
            line, used, room = list(word), wlen(word), rest
    lines.append(line)
    out = []
    for i, ln in enumerate(lines):
        if i == 0 and lead_in:
            ln = [(c, R_) for c in lead_in] + ln
        out.append([("".join(c for c, _ in grp), grp[0][1]) for grp in _groups(ln)])
    return out


def _groups(seq):
    """Consecutive (char, font) pairs with the same font."""
    out = []
    for c, f in seq:
        if out and out[-1][0][1] == f:
            out[-1].append((c, f))
        else:
            out.append([(c, f)])
    return out


def _flow(page, y: float, runs, x_first: float, x_rest: float, size: float = BODY, lead: float = LEAD,
          right: float = TEXT_R, lead_in: str = "") -> tuple[float, list[str]]:
    """Print wrapped styled text; returns (baseline of the last line, printed lines as plain text)."""
    lines = _wrap(runs, right - x_first, right - x_rest, size, lead_in)
    printed = []
    for i, spans in enumerate(lines):
        x = x_first if i == 0 else x_rest
        for txt, font in spans:
            x = _text(page, x, y + i * lead, txt, font, size)
        printed.append("".join(t for t, _ in spans))
    return y + (len(lines) - 1) * lead, printed


def _furniture(page: pymupdf.Page, n: int) -> None:
    """Watermark, running header and footer, in the order the received addenda draw them."""
    w = _width(WATERMARK, "hebo", 34)
    a = math.radians(52)
    o = pymupdf.Point(W / 2 - math.cos(a) * w / 2, H / 2 + math.sin(a) * w / 2)   # centred on the page
    _text(page, o.x, o.y, WATERMARK, "hebo", 34, WM, morph=(o, pymupdf.Matrix(52)))
    _rule(page, (L, HEADER_RULE_Y), (R, HEADER_RULE_Y))
    _text(page, L, HEADER_Y, HEADER_TITLE, "helv", 6.8, GREY)
    _text(page, R - _width(HEADER_REF, "helv", 6.8), HEADER_Y, HEADER_REF, "helv", 6.8, GREY)
    _rule(page, (L, FOOTER_RULE_Y), (R, FOOTER_RULE_Y))
    _text(page, L, FOOTER_Y, DISCLAIMER, "helv", 6.4, GREY)
    pg = f"Page {n}"
    _text(page, R - _width(pg, "helv", 6.4), FOOTER_Y, pg, "helv", 6.4, GREY)


def _qa_table(page: pymupdf.Page, top: float) -> dict:
    """The clarification table, ruled like ADD-02 page 2. Returns what was printed in each cell."""
    cols = QA_COLS
    cells = [[_wrap([(c, R_)], cols[i + 1] - cols[i] - 2 * CELL_PAD, cols[i + 1] - cols[i] - 2 * CELL_PAD, CELL)
              for i, c in enumerate(row)] for row in QA_ROWS]
    heights = [CELL_ROW] + [CELL_ROW + CELL_LEAD * (max(len(c) for c in row) - 1) for row in cells]
    bottom = top + sum(heights)
    page.draw_rect(pymupdf.Rect(cols[0], top, cols[-1], top + CELL_ROW), color=None, fill=HEAD_FILL)
    _rule(page, (cols[0], top), (cols[-1], top))
    _rule(page, (cols[0], bottom), (cols[-1], bottom))
    _rule(page, (cols[0], bottom), (cols[0], top))
    _rule(page, (cols[-1], bottom), (cols[-1], top))
    y = top
    for h in heights[:-1]:
        y += h
        _rule(page, (cols[0], y), (cols[-1], y))
    for x in cols[1:-1]:
        _rule(page, (x, bottom), (x, top))
    for i, head in enumerate(QA_HEADER):
        _text(page, cols[i] + CELL_PAD, top + CELL_BASE, head, "hebo", CELL, WHITE)
    printed = {}
    y = top + CELL_ROW
    for row, wrapped, h in zip(QA_ROWS, cells, heights[1:]):
        printed[row[0]] = {}
        for i, lines in enumerate(wrapped):
            for k, spans in enumerate(lines):
                _text(page, cols[i] + CELL_PAD, y + CELL_BASE + k * CELL_LEAD, spans[0][0], R_, CELL)
            printed[row[0]][QA_HEADER[i]] = [spans[0][0] for spans in lines]
        y += h
    return {"top": round(top, 2), "bottom": round(bottom, 2), "col_edges": cols, "row_heights": heights,
            "printed_lines": printed}


# ---------------------------------------------------------------------------------------------- the addendum
def _make_pdf(path: Path) -> dict:
    doc = pymupdf.open()
    layout: dict = {"pages": {}}

    # ---- page 1: cover band, front matter, sections 1-7
    p = doc.new_page(width=W, height=H)
    _furniture(p, 1)
    p.draw_rect(pymupdf.Rect(*BAND), color=None, fill=BAND_FILL)
    _text(p, 66.69, 100.36, "ADDENDUM NO. 3", "hebo", 15, WHITE)
    _text(p, 528.58 - _width(ISSUED, "hebo", 8.5), 91.86, ISSUED, "hebo", 8.5, WHITE)
    tender = "Tender NUPA/ISTP/2026/014"
    _text(p, 528.58 - _width(tender, "helv", 8.5), 102.86, tender, "helv", 8.5, WHITE)
    _text(p, TEXT_X, 142.86, "Wadi Sirhan Independent Sewage Treatment Plant", "hebo", 10.5)
    y, lines1 = _flow(p, 158.96, [(FRONT[0], R_)], TEXT_X, TEXT_X)
    y, lines2 = _flow(p, y + AFTER_PARA, [(FRONT[1], R_)], TEXT_X, TEXT_X)
    p1 = {"front_matter_lines": lines1 + lines2, "sections": {}}
    for heading, clauses in SECTIONS:
        y += BEFORE_HEAD
        _text(p, TEXT_X, y, heading, "hebo", 13)
        sec = p1["sections"][heading] = {"heading_baseline": round(y, 2), "clauses": {}}
        for i, (num, runs) in enumerate(clauses):
            y += AFTER_HEAD if i == 0 else AFTER_PARA
            first = y
            _text(p, TEXT_X, y, num, "tibo", BODY)
            y, printed = _flow(p, y, runs, CLAUSE_TEXT_X, CLAUSE_WRAP_X, lead_in="   ")
            sec["clauses"][num] = {"first_baseline": round(first, 2), "lines": printed}
    assert y < FOOTER_RULE_Y - 20, f"sections 1-7 overflow page 1 (last baseline {y:.1f})"
    layout["pages"][1] = p1

    # ---- page 2: section 8, the clarification table
    p = doc.new_page(width=W, height=H)
    _furniture(p, 2)
    y = 81.36
    _text(p, TEXT_X, y, QA_HEADING, "hebo", 13)
    layout["pages"][2] = {"heading_baseline": y, "table": _qa_table(p, y + HEAD_TO_TABLE)}

    doc.set_metadata({"title": "Addendum No. 3 (synthetic drill, not tender content)",
                      "author": "tests/fixtures/make_drill.py", "creator": "tests/fixtures/make_drill.py",
                      "producer": "PyMuPDF via tests/fixtures/make_drill.py",
                      "creationDate": "D:20261105090000+00'00'", "modDate": "D:20261105090000+00'00'"})
    doc.save(path, garbage=3, deflate=True, no_new_id=True)
    doc.close()
    return layout


def _clause_text(runs) -> str:
    return "".join(t for t, _ in runs)


def _expected(layout: dict) -> dict:
    units = [
        {"id": "ADD-03:cover/para1", "kind": "paragraph", "page": 1, "text": ISSUED},
        {"id": "ADD-03:H:cover", "kind": "heading", "page": 1, "text": "ADDENDUM NO. 3"},
        {"id": "ADD-03:cover/para2", "kind": "paragraph", "page": 1, "text": "Tender NUPA/ISTP/2026/014"},
        {"id": "ADD-03:H:cover-2", "kind": "heading", "page": 1, "text": "Wadi Sirhan Independent Sewage Treatment Plant"},
        # two printed paragraphs with ADD-02's spacing; ADD-02 prints its front matter the same way (ADD-02:cover/para3)
        {"id": "ADD-03:cover/para3", "kind": "paragraph", "page": 1, "text": " ".join(FRONT),
         "printed_paragraphs": list(FRONT)},
    ]
    for heading, clauses in SECTIONS:
        units.append({"id": f"ADD-03:H:S{heading.split('.')[0]}", "kind": "heading", "page": 1, "text": heading})
        for num, runs in clauses:
            units.append({"id": f"ADD-03:{num}", "kind": "clause", "page": 1, "label": num, "text": _clause_text(runs),
                          "bold_runs": [t for t, f in runs if f == B_]})
    units.append({"id": "ADD-03:H:S8", "kind": "heading", "page": 2, "text": QA_HEADING})
    units.append({"id": "ADD-03:S8/QA", "kind": "table", "page": 2, "text": " | ".join(QA_HEADER),
                  "columns": list(QA_HEADER)})
    for row in QA_ROWS:
        cells = dict(zip(QA_HEADER, row))
        units.append({"id": f"ADD-03:Q{row[0]}", "kind": "table_row", "page": 2, "parent": "ADD-03:S8/QA",
                      "cells": cells, "text": " | ".join(f"{k}: {v}" for k, v in cells.items())})
    for u in units:
        if u["id"] in INTENDED:
            u["intended"] = INTENDED[u["id"]]
    return {
        "pack_id": PACK_ID,
        "note": "synthetic drill addendum (NOT tender content); written from the builder's inputs, not from program output",
        "doc_id": "ADD-03", "kind": "addendum", "number": 3, "pdf": PDF_NAME, "pages": 2,
        "issued": {"unit": "ADD-03:cover/para1", "text": ISSUED, "date": "2026-11-05", "previous": "ADD-02 2026-10-22"},
        "furniture_per_page": {"WATERMARK": 1, "HEADER-TITLE": 1, "HEADER-REF": 1, "FOOTER-DISCLAIMER": 1,
                               "FOOTER-PAGE": 1},
        "printed_pages": ["1", "2"],
        "fonts": sorted(FONT_NAMES.values()),
        "regions": [],
        "provisions": [u["id"] for u in units if u["kind"] in ("paragraph", "clause", "table_row")],
        "units": units,
        "engine_outcome": {
            "status": "PARTIAL",
            "why": "ADD-03:7.1 is invalid (C23) and ADD-03:6.1, Q15, Q16 are unresolved until a person decides them",
            "valid_ops": ["ADD-03/cover/para3", "ADD-03/2.1", "ADD-03/3.1", "ADD-03/4.1", "ADD-03/5.1"],
            "invalid_ops": ["ADD-03/7.1"],
            "unresolved": ["ADD-03:6.1", "ADD-03:Q15", "ADD-03:Q16"],
            "no_effect": ["ADD-03:cover/para1", "ADD-03:cover/para2", "ADD-03:1.1"],
        },
        "layout": layout,
    }


# ---------------------------------------------------------------------------------------------- the drill pack
def _rel(p: Path) -> str:
    """Repository-relative when inside the repository (committed outputs carry no machine paths), else absolute.
    Either form resolves as root / path in tenderpack."""
    p = Path(p).resolve()
    return p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix()


def build(out_dir: Path) -> dict:
    out = Path(out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    pdf_path = out / PDF_NAME
    layout = _make_pdf(pdf_path)
    data = pdf_path.read_bytes()
    pages = pymupdf.open(pdf_path).page_count

    real = yaml.safe_load((ROOT / "config/pack.yaml").read_text(encoding="utf-8"))
    documents = [dict(d) for d in real["documents"]]
    assert [d["doc_id"] for d in documents] == ["VOL-I", "VOL-II", "VOL-IV", "VOL-V", "ADD-01", "ADD-02"], documents
    documents.append({"doc_id": "ADD-03", "kind": "addendum", "number": 3, "path": _rel(pdf_path)})

    received = {f["path"]: f for f in json.loads((ROOT / "sources/manifest.json").read_text(encoding="utf-8"))["files"]}
    files = [received[d["path"]] for d in documents[:-1]]
    files.append({"path": documents[-1]["path"], "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                  "pages": pages, "producer": "PyMuPDF via tests/fixtures/make_drill.py",
                  "creation_date": "D:20261105090000+00'00'",
                  "note": "synthetic drill addendum built by tests/fixtures/make_drill.py (not tender content)"})
    (out / "manifest.json").write_text(json.dumps({"files": files}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    (out / "furniture.yaml").write_bytes((ROOT / "config/furniture.yaml").read_bytes())   # unchanged: '—' is encoded

    pack = {"pack_id": PACK_ID,
            "manifest": _rel(out / "manifest.json"),
            "furniture": _rel(out / "furniture.yaml"),
            "readings_dir": "curation/readings",               # the real image readings (still pending review)
            "approvals": _rel(out / "approvals.yaml"),         # never created: no reading is approved in a drill
            "amendments_dir": "curation/amendments",
            "register": "curation/register/rows.yaml",
            "documents": documents}
    (out / "pack.yaml").write_text(
        "# Drill pack: the six received documents as in config/pack.yaml, plus a SYNTHETIC Addendum No. 3\n"
        "# (tests/fixtures/make_drill.py; not tender content). Paths are repository-relative, or absolute when the\n"
        "# drill was built outside the repository; tenderpack resolves either as root / path.\n"
        + yaml.safe_dump(pack, sort_keys=False, allow_unicode=True, width=200), encoding="utf-8")

    expected = _expected(layout)
    expected["sha256"] = hashlib.sha256(data).hexdigest()
    (out / "expected.yaml").write_text(yaml.safe_dump(expected, allow_unicode=True, sort_keys=False, width=110),
                                       encoding="utf-8")
    return expected


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python tests/fixtures/make_drill.py OUT_DIR")
    build(Path(sys.argv[1]))
