#!/usr/bin/env python3
"""Builder for the blind rehearsal 06 inputs:

  ADD-03_Addendum_No_3.pdf  (stands on the base pack as amended by Addenda Nos. 1 and 2)
  ADD-04_Addendum_No_4.pdf  (stands on the base pack as amended by Addenda Nos. 1, 2 and 3)

Both are drawn in the page furniture and typography of the issued Addenda Nos. 1 and 2:
A4, Base-14 Type1 fonts (Helvetica, Helvetica-Bold, Times-Roman, Times-Bold,
WinAnsiEncoding, not embedded) for every text-layer glyph, the ADD-01/ADD-02 watermark,
header, footer and rules, the ADD-01/ADD-02 clarification grid and table styling, and
ReportLab-style metadata.  There is no Arabic code point in either text layer.

Addendum No. 3 carries one IMAGE-ONLY element (Appendix A, Table 1-3, Arabic), drawn the
way Volume II draws its Table 2-4 reproduction: a partial-page "scanned" raster 1750 px
across, RGB with equal channels, FlateDecode, placed at the frame's left edge over the full
frame width directly below an introductory paragraph.  The raster is produced here from
source strings: the Arabic is shaped by MuPDF's HTML engine (HarfBuzz) in GNU FreeSerif,
the vector master is rotated slightly, rasterised, toned to the pack's paper grey and
speckled with a fixed-seed numpy generator.

The output is byte-for-byte deterministic (fixed dates, fixed /ID, fixed seed, pinned
library versions and font files).

Usage:
  python build_addendum.py <ADD-03 output.pdf> <ADD-04 output.pdf> [--check <candidate_pack_dir>]
"""
import datetime as dt
import hashlib
import io
import re
import sys

import numpy as np
import pymupdf

# --------------------------------------------------------------------------
# Page geometry (points).  "td" = top-down coordinate as reported by PyMuPDF.
# --------------------------------------------------------------------------
PAGE_W, PAGE_H = 595.2756, 841.8898
FRAME_L, FRAME_R = 56.69291, 538.5827
PARA_L, PARA_R = 62.69291, 532.5827
CONTENT_TOP = 68.36218
CONTENT_BOTTOM = 779.2
HANG = 36.85039
QUOTE_FIRST = 36.85039
QUOTE_REST = 62.3622
BREAK_TOL = 1.0

INK = ".101961 .101961 .101961"
HDR_TXT = ".352941 .352941 .352941"
RULE = ".721569 .721569 .721569"
COVER_FILL = ".164706 .164706 .164706"
THEAD_FILL = ".227451 .227451 .227451"

FONTS = [("F1", "Helvetica"), ("F2", "Helvetica-Bold"),
         ("F3", "Times-Roman"), ("F4", "Times-Bold")]
FONTOBJ = {k: pymupdf.Font(v) for k, v in FONTS}
REG, BOLD = "F3", "F4"

FREEFONT = "/usr/share/fonts/truetype/freefont/"
PINNED_FONTS = {
    "FreeSerif.ttf": "c57bf5de095af4e070c2acb5bce634316409ed4203b5098f4fdadb691dc7b3d2",
    "FreeSerifBold.ttf": "f078f2ac5d38addc71e2c123d86584341360b5bf27bc1cf238574ebe4f5a0f4d",
}
PINNED_VERSIONS = {"pymupdf": "1.28.2", "numpy": "2.4.6"}

# Table image: same convention as the Table 2-4 image in Volume II page 3
# (1750 px across, drawn at x = 56.69291 over the full frame width 481.8898 pt).
IMG_PX_W, IMG_PX_H = 1750, 1550
IMG_W = 481.8898
IMG_ZOOM = IMG_PX_W / IMG_W
IMG_H = IMG_PX_H / IMG_ZOOM
IMG_SEED = 20261105
PAPER = 252


def fmt(v):
    s = ("%.6f" % v).rstrip("0").rstrip(".")
    if s.startswith("0.") and len(s) > 2:
        s = s[1:]
    elif s.startswith("-0."):
        s = "-" + s[2:]
    return s if s not in ("", "-") else "0"


def width(text, font, size):
    return FONTOBJ[font].text_length(text, fontsize=size)


def pstr(s):
    out = []
    for ch in s.encode("cp1252"):
        if ch in (0x28, 0x29, 0x5C):
            out.append("\\" + chr(ch))
        elif 32 <= ch < 127:
            out.append(chr(ch))
        else:
            out.append("\\%03o" % ch)
    return "(" + "".join(out) + ")"


def Y(td):
    return PAGE_H - td


# --------------------------------------------------------------------------
# Rich text: markup with <b>..</b> and <sup>..</sup>
# --------------------------------------------------------------------------
def parse_runs(markup, size, reg=REG, bold=BOLD):
    runs, b, sup = [], False, False
    for tok in re.split(r"(</?b>|</?sup>)", markup):
        if tok == "<b>":
            b = True
        elif tok == "</b>":
            b = False
        elif tok == "<sup>":
            sup = True
        elif tok == "</sup>":
            sup = False
        elif tok:
            f = bold if b else reg
            if sup:
                runs.append((tok, f, round(size * 0.8, 4), round(size * 0.5, 4)))
            else:
                runs.append((tok, f, size, 0))
    return runs


def tokenize(runs):
    toks, cur = [], []
    for text, f, sz, rise in runs:
        for part in re.split(r"( )", text):
            if part == "":
                continue
            if part == " ":
                if cur:
                    toks.append(("w", cur))
                    cur = []
                toks.append(("s", (" ", f, sz, rise)))
            else:
                cur.append((part, f, sz, rise))
    if cur:
        toks.append(("w", cur))
    return toks


def pieces_width(pieces):
    return sum(width(t, f, sz) for t, f, sz, _ in pieces)


def break_lines(prefix, runs, avail_first, avail_rest):
    toks = tokenize(runs)
    lines, cur, curw, pend = [], list(prefix), pieces_width(prefix), None
    first = not prefix
    for kind, val in toks:
        if kind == "s":
            if cur:
                pend = val
            continue
        ww = pieces_width(val)
        avail = avail_first if not lines else avail_rest
        add = ww + (width(" ", pend[1], pend[2]) if (pend and not first) else 0)
        if not first and curw + add > avail + BREAK_TOL:
            lines.append(cur)
            cur, curw = list(val), ww
        else:
            if pend and not first:
                cur.append(pend)
            cur.extend(val)
            curw += add
        first = False
        pend = None
    if cur:
        lines.append(cur)
    return lines


def merge(pieces):
    out = []
    for p in pieces:
        if out and out[-1][1:] == p[1:]:
            out[-1] = (out[-1][0] + p[0],) + p[1:]
        else:
            out.append(p)
    return out


def emit_text_block(x_first, x_rest, td_first_baseline, leading, lines, avails,
                    justify, color=INK):
    o = ["BT 1 0 0 1 %s %s Tm %s TL %s rg" % (fmt(x_first), fmt(Y(td_first_baseline)),
                                               fmt(leading), color)]
    cur_font = None
    for i, line in enumerate(lines):
        if i == 1 and x_rest != x_first:
            o.append("%s 0 Td" % fmt(x_rest - x_first))
        last = i == len(lines) - 1
        nsp = sum(t.count(" ") for t, *_ in line)
        lw = pieces_width(line)
        if nsp and lw > avails[i]:
            tw = (avails[i] - lw) / nsp
        elif justify and not last and nsp:
            tw = (avails[i] - lw) / nsp
        else:
            tw = 0.0
        o.append("%s Tw" % fmt(tw))
        for t, f, sz, rise in merge(line):
            key = (f, sz, rise)
            if key != cur_font:
                o.append("/%s %s Tf %s Ts" % (f, fmt(sz), fmt(rise)))
                cur_font = key
            o.append(pstr(t) + " Tj")
        o.append("T*")
    o.append("0 Tw 0 Ts ET")
    return "\n".join(o)


# --------------------------------------------------------------------------
# Flowables
# --------------------------------------------------------------------------
class Para:
    STYLES = {
        "body": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "prov": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "quote": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "head": dict(size=13, lead=16, reg="F2", bold="F2", justify=False),
        "proj": dict(size=10.5, lead=13, reg="F2", bold="F2", justify=False),
        "ttitle": dict(size=8.5, lead=11, reg="F2", bold="F2", justify=False),
        "notehdr": dict(size=7.2, lead=9, reg=REG, bold=BOLD, justify=False),
        "note": dict(size=7.2, lead=9, reg=REG, bold=BOLD, justify=True),
    }

    def __init__(self, kind, markup, num=None, keep_next=False):
        self.kind, self.markup, self.num, self.keep_next = kind, markup, num, keep_next
        st = self.STYLES[kind]
        self.size, self.lead, self.justify = st["size"], st["lead"], st["justify"]
        runs = parse_runs(markup, self.size, st["reg"], st["bold"])
        if kind == "prov":
            prefix = [(num, BOLD, self.size, 0), ("   ", REG, self.size, 0)]
            self.x_first, self.x_rest = PARA_L, PARA_L + HANG
        elif kind == "quote":
            prefix = [("‘", REG, self.size, 0), (num, BOLD, self.size, 0),
                      ("  ", REG, self.size, 0)]
            self.x_first, self.x_rest = PARA_L + QUOTE_FIRST, PARA_L + QUOTE_REST
        elif kind == "note":
            prefix = [(num, REG, self.size, 0), ("  ", REG, self.size, 0)]
            self.x_first = self.x_rest = PARA_L
        else:
            prefix = []
            self.x_first = self.x_rest = PARA_L
        self.af = PARA_R - self.x_first
        self.ar = PARA_R - self.x_rest
        self.lines = break_lines(prefix, runs, self.af, self.ar)
        self.height = len(self.lines) * self.lead

    def draw(self, top):
        avails = [self.af] + [self.ar] * (len(self.lines) - 1)
        return emit_text_block(self.x_first, self.x_rest, top + self.size, self.lead,
                               self.lines, avails, self.justify)


class Cover:
    height = 40.0
    kind = "cover"

    def __init__(self, number, issued, tender):
        self.number, self.issued, self.tender = number, issued, tender

    def draw(self, top):
        o = ["q %s rg n %s %s %s %s re f* Q" % (COVER_FILL, fmt(FRAME_L), fmt(Y(top)),
                                               fmt(FRAME_R - FRAME_L), fmt(-self.height))]
        o.append("BT 1 0 0 1 %s %s Tm /F2 15 Tf 18 TL 1 1 1 rg %s Tj T* ET"
                 % (fmt(FRAME_L + 10), fmt(Y(top + 26)), pstr("ADDENDUM NO. %s" % self.number)))
        right = FRAME_R - 10
        w1 = width(self.issued, "F2", 8.5)
        w2 = width(self.tender, "F1", 8.5)
        o.append("BT 1 0 0 1 %s %s Tm 11 TL /F2 8.5 Tf 1 1 1 rg %s Tj ET"
                 % (fmt(right - w1), fmt(Y(top + 17.5)), pstr(self.issued)))
        o.append("BT 1 0 0 1 %s %s Tm 11 TL /F1 8.5 Tf 1 1 1 rg %s Tj ET"
                 % (fmt(right - w2), fmt(Y(top + 28.5)), pstr(self.tender)))
        return "\n".join(o)


class Grid:
    """Ruled table with a dark header band (header cells may wrap); splits with the
    header repeated."""
    SIZE, LEAD, PAD_T, PAD_B, PAD_X = 8.2, 10.4, 3.5, 3.5, 4.0
    kind = "table"

    def __init__(self, cols, head, rows):
        self.cols = cols
        self.head = []
        for ci, h in enumerate(head):
            avail = cols[ci + 1] - cols[ci] - 2 * self.PAD_X
            self.head.append(break_lines([], parse_runs(h, self.SIZE, "F2", "F2"), avail, avail))
        nh = max(len(h) for h in self.head)
        self.head_h = self.PAD_T + nh * self.LEAD + self.PAD_B
        self.rows = []
        for r in rows:
            cells = []
            for ci, txt in enumerate(r):
                avail = cols[ci + 1] - cols[ci] - 2 * self.PAD_X
                runs = parse_runs(txt, self.SIZE, REG, BOLD)
                cells.append(break_lines([], runs, avail, avail) if txt else [])
            n = max(1, max(len(c) for c in cells))
            self.rows.append((cells, self.PAD_T + n * self.LEAD + self.PAD_B))

    def chunk(self, start, room):
        h, n = self.head_h, 0
        for cells, rh in self.rows[start:]:
            if h + rh > room + 1e-6:
                break
            h += rh
            n += 1
        return n, h

    def draw_rows(self, top, start, n):
        o = []
        x0, x1 = self.cols[0], self.cols[-1]
        o.append("q %s rg n %s %s %s %s re f* Q" % (THEAD_FILL, fmt(x0), fmt(Y(top)),
                                                   fmt(x1 - x0), fmt(-self.head_h)))
        for ci, lines in enumerate(self.head):
            x = self.cols[ci] + self.PAD_X
            avail = self.cols[ci + 1] - self.cols[ci] - 2 * self.PAD_X
            o.append(emit_text_block(x, x, top + self.PAD_T + self.SIZE, self.LEAD, lines,
                                     [avail] * len(lines), False, color="1 1 1"))
        y = top + self.head_h
        bounds = [top, y]
        for cells, rh in self.rows[start:start + n]:
            for ci, lines in enumerate(cells):
                if not lines:
                    continue
                x = self.cols[ci] + self.PAD_X
                avail = self.cols[ci + 1] - self.cols[ci] - 2 * self.PAD_X
                o.append(emit_text_block(x, x, y + self.PAD_T + self.SIZE, self.LEAD, lines,
                                         [avail] * len(lines), False))
            y += rh
            bounds.append(y)
        g = ["q 1 J 1 j %s RG .4 w" % RULE]
        line = lambda a, b, c, d: g.append("n %s %s m %s %s l S" % (fmt(a), fmt(Y(b)), fmt(c), fmt(Y(d))))
        line(x0, top, x1, top)
        line(x0, y, x1, y)
        line(x0, y, x0, top)
        line(x1, y, x1, top)
        for b in bounds[1:-1]:
            line(x0, b, x1, b)
        for cx in self.cols[1:-1]:
            line(cx, y, cx, top)
        g.append("Q")
        o.append("\n".join(g))
        return "\n".join(o), y - top


class QATable(Grid):
    COLS = [56.69291, 90.70866, 300.4724, 538.5827]       # ADD-01 / ADD-02 clarification grid

    def __init__(self, rows):
        super().__init__(self.COLS, ["No", "Bidder question", "Authority response"], rows)


class TieInTable(Grid):
    # ADD-02 Table 1-1 outer edges (70.86614 .. 524.4094), six columns
    COLS = [70.86614, 114.86614, 234.86614, 296.86614, 371.86614, 441.86614, 524.4094]

    def __init__(self, rows):
        super().__init__(self.COLS, ["Tie-in point", "Location", "Existing sewer diameter (mm)",
                                     "Permitted shutdown window", "Maximum shutdown duration (hours)",
                                     "Advance notice"], rows)


class NoteRule:
    """Short centred rule between a table and its notes (ADD-02 page 1)."""
    kind = "noterule"
    height = 4.0

    def draw(self, top):
        x0 = 223.937
        return ("q 1 J 1 j %s RG .5 w n %s %s m %s %s l S Q"
                % (INK, fmt(x0), fmt(Y(top + 3)), fmt(x0 + 147.4016), fmt(Y(top + 3))))


class PageBreak:
    kind = "break"
    height = 0.0


class ImageBlock:
    """A reproduced table image drawn as Volume II draws Table 2-4: a 9 pt spacer, then
    the image at the frame's left edge over the full frame width."""
    kind = "image"
    SPACER = 9.0

    def __init__(self, name):
        self.name = name
        self.height = self.SPACER + IMG_H

    def draw(self, top):
        y0 = Y(top + self.SPACER + IMG_H)
        return ("q\n1 0 0 1 %s %s cm\nq\n%s 0 0 %s 0 0 cm\n/%s Do\nQ\nQ"
                % (fmt(FRAME_L), fmt(y0), fmt(IMG_W), fmt(IMG_H), self.name))


def kind_of(fl):
    return fl.kind


def gap(prev, nxt):
    if prev is None:
        return 0.0
    if prev == "cover":
        return 18.0
    if prev == "proj":
        return 4.0
    if nxt == "head":
        return 14.0
    if prev == "head":
        return 7.0
    if nxt == "image":
        return 0.0
    if prev == "image":
        return 4.0
    if nxt == "ttitle":
        return 17.0
    if prev == "ttitle":
        return 3.0
    if nxt in ("noterule", "notehdr", "note") and prev in ("table", "noterule", "notehdr", "note"):
        return 0.0
    if prev == "note":
        return 8.0
    return 5.0


# --------------------------------------------------------------------------
# Page furniture (identical to ADD-01 / ADD-02 apart from the header text)
# --------------------------------------------------------------------------
def furniture(header_left, page_no):
    o = ["1 0 0 1 0 0 cm  BT /F1 12 Tf 14.4 TL ET",
         "q",
         "BT /F2 34 Tf 40.8 TL ET",
         ".86 .86 .86 rg",
         ".615661 .788011 -0.788011 .615661 297.6378 420.9449 cm",
         "BT 1 0 0 1 -287.13 0 Tm (FICTIONAL \\227 ASSESSMENT PACK) Tj T* ET",
         "Q",
         "q",
         "%s RG" % RULE,
         ".4 w",
         "n 56.69291 796.5354 m 538.5827 796.5354 l S",
         "BT /F1 6.8 Tf 8.16 TL ET",
         "%s rg" % HDR_TXT,
         "BT 1 0 0 1 56.69291 802.2047 Tm %s Tj T* ET" % pstr(header_left),
         "BT 1 0 0 1 472.4391 802.2047 Tm (NUPA/ISTP/2026/014) Tj T* ET",
         "n 56.69291 42.51969 m 538.5827 42.51969 l S",
         "BT /F1 6.4 Tf 7.68 TL ET",
         "BT 1 0 0 1 56.69291 32.59843 Tm (FICTIONAL DOCUMENT \\227 prepared solely for a Lamar "
         "Holding internal capability assessment. Not a real tender.) Tj T* ET"]
    pg = "Page %d" % page_no
    o.append("BT 1 0 0 1 %s 32.59843 Tm %s Tj T* ET" % (fmt(FRAME_R - width(pg, "F1", 6.4)), pstr(pg)))
    o.append("Q")
    return "\n".join(o)


# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------
def first_height(fl):
    if isinstance(fl, Grid):
        return fl.head_h + fl.rows[0][1]
    return fl.height                          # paragraphs are never split


def layout(flowables):
    """Returns a list of pages; each page is (list of content chunks, list of image names)."""
    pages, cur, top, prev, imgs = [], [], CONTENT_TOP, None, []
    i = 0
    started = False

    def flush():
        pages.append((cur, imgs))

    while i < len(flowables):
        fl = flowables[i]
        k = kind_of(fl)
        if k == "break":
            flush()
            cur, top, prev, imgs = [], CONTENT_TOP, None, []
            i += 1
            continue
        t = top + (gap(prev, k) if prev is not None else 0.0)
        if not started:
            t = CONTENT_TOP + 6.0
            started = True
        if isinstance(fl, Grid):
            start = getattr(fl, "_next", 0)
            n, h = fl.chunk(start, CONTENT_BOTTOM - t)
            if n == 0:
                flush()
                cur, top, prev, imgs = [], CONTENT_TOP, None, []
                continue
            s, h = fl.draw_rows(t, start, n)
            cur.append(s)
            fl._next = start + n
            if fl._next < len(fl.rows):
                flush()
                cur, top, prev, imgs = [], CONTENT_TOP, None, []
                continue
            top, prev = t + h, k
            i += 1
            continue
        need = fl.height
        keep = k in ("head", "ttitle", "notehdr") or getattr(fl, "keep_next", False)
        if keep and i + 1 < len(flowables):
            nx = flowables[i + 1]
            need = fl.height + gap(k, kind_of(nx)) + first_height(nx)
        if prev is not None and t + need > CONTENT_BOTTOM:
            flush()
            cur, top, prev, imgs = [], CONTENT_TOP, None, []
            continue
        cur.append(fl.draw(t))
        if k == "image":
            imgs = imgs + [fl.name]
        top, prev = t + fl.height, k
        i += 1
    if cur:
        flush()
    return pages


# --------------------------------------------------------------------------
# The "scanned" Arabic Table 1-3 (Addendum No. 3, Appendix A)
# --------------------------------------------------------------------------
AR_CSS = """
@font-face {font-family: ar; src: url(FreeSerif.ttf);}
@font-face {font-family: ar; src: url(FreeSerifBold.ttf); font-weight: bold;}
body {font-family: ar; margin: 0; padding: 0;}
p {margin: 0; padding: 0; white-space: nowrap;}
"""


def html_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ar_line(page, text, x_right, baseline, size, bold=False):
    """Shape one RTL line with MuPDF/HarfBuzz and place it right-aligned at x_right."""
    arch = pymupdf.Archive(FREEFONT)
    html = '<p dir="rtl" style="font-size:%spt;%s">%s</p>' % (
        fmt(size), "font-weight:bold;" if bold else "", html_escape(text))
    story = pymupdf.Story(html=html, user_css=AR_CSS, archive=arch)
    buf = io.BytesIO()
    w = pymupdf.DocumentWriter(buf)
    box = pymupdf.Rect(0, 0, 1500, 6 * size)
    dev = w.begin_page(box)
    more, _ = story.place(pymupdf.Rect(50, 2 * size, 1450, 6 * size))
    if more:
        raise SystemExit("Arabic line does not fit: %s" % text)
    story.draw(dev)
    w.end_page()
    w.close()
    tmp = pymupdf.open("pdf", buf.getvalue())
    tp = tmp[0]
    xs, base = [], None
    for blk in tp.get_text("rawdict")["blocks"]:
        for ln in blk.get("lines", []):
            for sp in ln["spans"]:
                for ch in sp["chars"]:
                    xs += [ch["bbox"][0], ch["bbox"][2]]
                if base is None:
                    base = sp["origin"][1]
    for kind, r in tp.get_bboxlog():
        if "text" in kind:
            xs += [r[0], r[2]]
    x0, x1 = min(xs), max(xs)
    up, down = 1.7 * size, 0.9 * size
    clip = pymupdf.Rect(x0 - 1, base - up, x1 + 1, base + down)
    if not (clip in tp.rect):
        raise SystemExit("Arabic clip outside the source page")
    tgt = pymupdf.Rect(x_right - (x1 - x0) - 1, baseline - up, x_right + 1, baseline + down)
    page.show_pdf_page(tgt, tmp, 0, clip=clip, keep_proportion=False)
    return x1 - x0


# Arabic source strings of Table 1-3 (the governing text).  Keys are referenced by the
# answer key.  Discrepancies against the English convenience translation (Appendix B) are
# deliberate: AR1 (TP-2 maximum shutdown duration 4 h in Arabic, 6 h in English) and AR2
# (note 1: the Arabic also excludes the Eid al-Fitr and Eid al-Adha holidays).
AR = {
    "issuer": "شركة خدمات المياه بالمنطقة الشمالية",
    "ref": "الرقم: ٣١٢/٢٠٢٦",
    "date": "التاريخ: ٥ نوفمبر ٢٠٢٦م",
    "subject": "الموضوع: نقاط الربط بشبكة التجميع القائمة لمحطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان",
    "tender": "مناقصة رقم: NUPA/ISTP/2026/014",
    "title": "جدول ١-٣: نقاط الربط وشروط إيقاف التدفق",
    "intro": "تُحدَّد نقاط الربط بشبكة التجميع القائمة وشروط إيقاف التدفق فيها على النحو الآتي:",
    "h_tp": "نقطة الربط",
    "h_loc": "الموقع",
    "h_dia": "قطر الخط القائم (مم)",
    "h_win": "فترة الإيقاف المسموح بها",
    "h_max": "أقصى مدّة للإيقاف (ساعة)",
    "h_ntc": "مهلة الإشعار المسبق",
    "tp1": "TP-1",
    "loc1": "غرفة التفتيش MH-41 على خط الطرد الشمالي",
    "dia1": "١٠٠٠",
    "win1": "من ٢٣:٠٠ إلى ٠٥:٠٠",
    "max1": "٦",
    "ntc1": "١٠ أيام عمل",
    "tp2": "TP-2",
    "loc2": "غرفة التفتيش MH-07 على خط الانحدار الجنوبي",
    "dia2": "٨٠٠",
    "win2": "من ٠١:٠٠ إلى ٠٥:٠٠",
    "max2": "٤",
    "ntc2": "١٠ أيام عمل",
    "notes": "ملاحظات:",
    "n1": "١. لا يُسمح بأي إيقاف خلال شهر رمضان المبارك أو خلال إجازتَي عيد الفطر وعيد الأضحى.",
    "n2": "٢. يُسمح بإيقافٍ واحدٍ فقط لكل نقطة ربط طوال مدّة الإنشاء.",
    "n3": "٣. تُقدَّم طلبات الإيقاف عبر البوابة الإلكترونية للشركة، مرفقاً بها برنامج الإيقاف المقترح وخطة الطوارئ.",
    "n4": "٤. جميع الأوقات المذكورة بتوقيت الرياض.",
    "sign": "مدير إدارة تشغيل الشبكات",
}

# Manual line breaks inside table cells (logical order, joined by one space).
AR_LINES = {
    "h_dia": ["قطر الخط القائم", "(مم)"],
    "h_win": ["فترة الإيقاف", "المسموح بها"],
    "h_max": ["أقصى مدّة للإيقاف", "(ساعة)"],
    "h_ntc": ["مهلة الإشعار", "المسبق"],
    "loc1": ["غرفة التفتيش MH-41", "على خط الطرد الشمالي"],
    "loc2": ["غرفة التفتيش MH-07", "على خط الانحدار الجنوبي"],
}
for _k, _lines in AR_LINES.items():
    assert " ".join(_lines) == AR[_k], _k


def table_1_3_master():
    """Vector master of the reproduced table (points; 1750 px across when rasterised)."""
    W, H = IMG_W, IMG_H
    doc = pymupdf.open()
    pg = doc.new_page(width=W, height=H)
    L, R = 16.0, W - 16.0
    RX = R - 2.0
    ar_line(pg, AR["issuer"], RX, 24, 13, bold=True)
    pg.insert_text((L + 2, 22), "Northern Region Water Services Company", fontname="tiro",
                   fontsize=8, color=(0.3, 0.3, 0.3))
    ar_line(pg, AR["ref"], RX, 41, 9.5)
    ar_line(pg, AR["date"], RX - 140, 41, 9.5)
    sh = pg.new_shape()
    sh.draw_line((L, 49), (R, 49))
    sh.finish(color=(0, 0, 0), width=0.9)
    sh.commit()
    ar_line(pg, AR["subject"], RX, 66, 9.6)
    ar_line(pg, AR["tender"], RX, 81, 9.6)
    ar_line(pg, AR["title"], RX, 106, 12.5, bold=True)
    ar_line(pg, AR["intro"], RX, 125, 9.8)
    # table, columns from right to left: point | location | diameter | window | maximum | notice
    cols = [R, R - 52, R - 152, R - 222, R - 312, R - 388, L]
    top = 136.0
    hh, rh = 38.0, 36.0
    bottom = top + hh + 2 * rh
    sh = pg.new_shape()
    sh.draw_rect(pymupdf.Rect(L, top, R, top + hh))
    sh.finish(color=None, fill=(0.88, 0.88, 0.88), width=0)
    sh.draw_rect(pymupdf.Rect(L, top, R, bottom))
    sh.draw_line((L, top + hh), (R, top + hh))
    sh.draw_line((L, top + hh + rh), (R, top + hh + rh))
    for cx in cols[1:-1]:
        sh.draw_line((cx, top), (cx, bottom))
    sh.finish(color=(0, 0, 0), width=0.8)
    sh.commit()
    pad = 5.0

    def cell(text, ci, baseline, size, bold=False, inset=0.0):
        """Right-aligned Arabic text in column ci; asserts that it fits inside the cell."""
        xr = cols[ci] - pad - inset
        w = ar_line(pg, text, xr, baseline, size, bold)
        if xr - w < cols[ci + 1] + 3.0:
            raise SystemExit("Arabic cell text does not fit: %s" % text)

    heads = ["h_tp", "h_loc", "h_dia", "h_win", "h_max", "h_ntc"]
    for ci, key in enumerate(heads):
        if key in AR_LINES:
            cell(AR_LINES[key][0], ci, top + 16, 9.6, True)
            cell(AR_LINES[key][1], ci, top + 31, 9.6, True)
        else:
            cell(AR[key], ci, top + 23, 9.6, True)
    for r, sfx in enumerate(("1", "2")):
        y0 = top + hh + r * rh
        cell(AR["tp" + sfx], 0, y0 + 22, 10, inset=10)
        cell(AR_LINES["loc" + sfx][0], 1, y0 + 15, 9.6)
        cell(AR_LINES["loc" + sfx][1], 1, y0 + 30, 9.6)
        cell(AR["dia" + sfx], 2, y0 + 22, 10.5, inset=20)
        cell(AR["win" + sfx], 3, y0 + 22, 9.8, inset=3)
        cell(AR["max" + sfx], 4, y0 + 22, 11, inset=30)
        cell(AR["ntc" + sfx], 5, y0 + 22, 9.8, inset=4)
    y = bottom + 22
    ar_line(pg, AR["notes"], RX, y, 10, bold=True)
    for key in ("n1", "n2", "n3", "n4"):
        y += 17
        ar_line(pg, AR[key], RX - 4, y, 9.4)
    y += 36
    ar_line(pg, AR["sign"], L + 150, y, 10.5, bold=True)
    sh = pg.new_shape()
    sh.draw_bezier((L + 24, y + 20), (L + 46, y + 2), (L + 66, y + 28), (L + 96, y + 10))
    sh.finish(color=(0.15, 0.15, 0.15), width=0.9)
    sh.draw_oval(pymupdf.Rect(L + 168, y - 20, L + 226, y + 22))
    sh.finish(color=(0.45, 0.45, 0.45), width=0.8)
    sh.commit()
    pg.insert_text((L + 2, H - 9), "FICTIONAL DOCUMENT - Lamar Holding internal assessment pack - "
                   "not a real tender.", fontname="tiro", fontsize=6.5, color=(0.45, 0.45, 0.45))
    if y + 30 > H - 14:
        raise SystemExit("table master overflows")
    return doc


def table_1_3_image():
    """Rotate slightly, rasterise at 1750 px across, tone to paper grey, speckle."""
    master = table_1_3_master()
    scan = pymupdf.open()
    sp = scan.new_page(width=IMG_W, height=IMG_H)
    sp.show_pdf_page(sp.rect, master, 0, rotate=0.35)
    pix = sp.get_pixmap(matrix=pymupdf.Matrix(IMG_ZOOM, IMG_ZOOM), alpha=False,
                        colorspace=pymupdf.csRGB)
    if (pix.width, pix.height) != (IMG_PX_W, IMG_PX_H):
        raise SystemExit("unexpected raster size %dx%d" % (pix.width, pix.height))
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3).astype(np.int32)
    gray = (a.sum(axis=2) + 1) // 3
    gray = (gray * PAPER + 127) // 255                     # white paper -> 252, as in the pack scans
    rng = np.random.default_rng(IMG_SEED)
    speck = rng.random((pix.height, pix.width)) < 0.0085
    tone = rng.integers(141, 217, size=(pix.height, pix.width), dtype=np.int32)
    gray = np.where(speck, np.minimum(gray, tone), gray)
    g8 = np.clip(gray, 0, 255).astype(np.uint8)
    return np.repeat(g8[:, :, None], 3, axis=2).tobytes()


# --------------------------------------------------------------------------
# PDF assembly
# --------------------------------------------------------------------------
def build_pdf(flowables, header_left, out_path, metadata, image_raw, image_name, doc_id):
    pages = layout(flowables)
    doc = pymupdf.open()
    font_xrefs = {}
    for name, base in FONTS:
        x = doc.get_new_xref()
        doc.update_object(x, "<</BaseFont/%s/Encoding/WinAnsiEncoding/Name/%s/Subtype/Type1/Type/Font>>"
                          % (base, name))
        font_xrefs[name] = x
    fd = doc.get_new_xref()
    doc.update_object(fd, "<<" + "".join("/%s %d 0 R" % (n, x) for n, x in font_xrefs.items()) + ">>")
    ix = None
    if image_raw is not None:
        ix = doc.get_new_xref()
        doc.update_object(ix, "<</BitsPerComponent 8/ColorSpace/DeviceRGB/Height %d"
                              "/Subtype/Image/Type/XObject/Width %d>>" % (IMG_PX_H, IMG_PX_W))
        doc.update_stream(ix, image_raw, compress=True)     # MuPDF deflate -> /FlateDecode
    for pno, (chunks, imgs) in enumerate(pages, start=1):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        stream = furniture(header_left, pno) + "\n" + "\n".join(chunks) + "\n"
        cx = doc.get_new_xref()
        doc.update_object(cx, "<<>>")
        doc.update_stream(cx, stream.encode("latin-1"))
        doc.xref_set_key(page.xref, "Contents", "%d 0 R" % cx)
        res = "<</Font %d 0 R/ProcSet[/PDF/Text/ImageB/ImageC/ImageI]" % fd
        if imgs:
            res += "/XObject<<" + "".join("/%s %d 0 R" % (nm, ix) for nm in imgs) + ">>"
        doc.xref_set_key(page.xref, "Resources", res + ">>")
        doc.xref_set_key(page.xref, "Rotate", "0")
        doc.xref_set_key(page.xref, "Trans", "<<>>")
    doc.xref_set_key(doc.pdf_catalog(), "PageMode", "/UseNone")
    doc.set_metadata(metadata)
    doc.xref_set_key(-1, "ID", "[<%s><%s>]" % (doc_id, doc_id))
    data = doc.tobytes(garbage=3, deflate=True, no_new_id=True)
    if not data.startswith(b"%PDF-1.7\n"):
        raise SystemExit("unexpected header")
    data = b"%PDF-1.4\n" + data[len(b"%PDF-1.7\n"):]           # same length: offsets unchanged
    with open(out_path, "wb") as f:
        f.write(data)
    return len(pages)


# --------------------------------------------------------------------------
# Dates (computed, then asserted against the printed text)
# --------------------------------------------------------------------------
ADD02 = dt.date(2026, 10, 22)
PDD = dt.date(2026, 11, 26)                     # ADD-01 Section 2.1; 14:00 Riyadh time
LETTER = dt.date(2026, 11, 5)                   # date of the Network Operator's letter (Table 1-3)
ISSUE3 = dt.date(2026, 11, 10)
ISSUE4 = dt.date(2026, 11, 16)
Q21_RECEIVED = dt.date(2026, 11, 11)


def is_wd(d):
    # Volume I Clause 2.4: Sunday..Thursday, other than a public holiday in the Kingdom.
    # No public holiday in the Kingdom falls between October and December 2026.
    return d.weekday() in (6, 0, 1, 2, 3)


def wd_before(d, n):
    """Volume I Clause 2.4: counting backwards, the stated date itself is not counted."""
    c = 0
    while c < n:
        d -= dt.timedelta(days=1)
        if is_wd(d):
            c += 1
    return d


def wd_after(d, n):
    """Counting forwards (not defined by Clause 2.4; mirrored: the start date is not counted)."""
    c = 0
    while c < n:
        d += dt.timedelta(days=1)
        if is_wd(d):
            c += 1
    return d


def wd_between(a, b):
    """Working Days from a (inclusive) to b (exclusive)."""
    n, d = 0, a
    while d < b:
        if is_wd(d):
            n += 1
        d += dt.timedelta(days=1)
    return n


def long_date(d):
    return "%s %d %s %d" % (d.strftime("%A"), d.day, d.strftime("%B"), d.year)


DATES = {
    "add03_issue": ISSUE3,
    "add04_issue": ISSUE4,
    "network_operator_letter": LETTER,
    "clarification_cutoff_vol1_5_2": wd_before(PDD, 10),
    "sal_application_add03_2_5": wd_before(PDD, 8),
    "sal_response_latest_add03_2_5": wd_after(wd_before(PDD, 8), 5),
    "cover_e2_wrong_anchor_8wd_after_issue": wd_after(ISSUE3, 8),
    "sal_application_add04_2_1": wd_before(PDD, 5),
    "sal_response_latest_add04_2_2": wd_after(wd_before(PDD, 5), 3),
    "q21_received": Q21_RECEIVED,
    "proposal_due_date": PDD,
}
assert ADD02 < LETTER < ISSUE3 < ISSUE4 < PDD
assert all(is_wd(d) for d in (LETTER, ISSUE3, ISSUE4, PDD, Q21_RECEIVED))
assert DATES["clarification_cutoff_vol1_5_2"] == dt.date(2026, 11, 12)
assert ISSUE3 < DATES["clarification_cutoff_vol1_5_2"] < ISSUE4   # No. 3 before, No. 4 after the cut-off
assert Q21_RECEIVED <= DATES["clarification_cutoff_vol1_5_2"]
assert DATES["sal_application_add03_2_5"] == dt.date(2026, 11, 16) == ISSUE4
assert DATES["sal_response_latest_add03_2_5"] == dt.date(2026, 11, 23)
assert DATES["cover_e2_wrong_anchor_8wd_after_issue"] == dt.date(2026, 11, 22)
assert DATES["sal_application_add04_2_1"] == dt.date(2026, 11, 19)
assert DATES["sal_response_latest_add04_2_2"] == dt.date(2026, 11, 24)
assert wd_between(ISSUE3, PDD) == 12
assert wd_between(ISSUE4, PDD) == 8

# Figures derived from the text (asserted; printed by --check)
NOMINAL = 120000                                   # Volume II Clause 2.1, m3/day
BAND = (NOMINAL * 85 // 100, NOMINAL * 110 // 100)
assert BAND == (102000, 132000)
OLD_MIN = NOMINAL * 90 // 100
assert OLD_MIN == 108000


# --------------------------------------------------------------------------
# Content
# --------------------------------------------------------------------------
LQ, RQ = "‘", "’"


def q(s, bold=False):
    return LQ + ("<b>%s</b>" % s if bold else s) + RQ


def issued(d):
    return "Issued %d %s %d" % (d.day, d.strftime("%B"), d.year)


PRECEDENCE = ("This Addendum forms part of the RFP Documents and takes precedence in accordance with Volume I "
              "Clause 3.2. Bidders shall acknowledge receipt in Form 4-A. All other terms of the RFP Documents "
              "remain unchanged.")

COVER3 = (
    "This Addendum incorporates the Network Operator's Table 1-3 describing the two tie-in points referred to in "
    "Volume II Clause 1.3, requires a Bidder that elects to interrupt flows at a tie-in point to obtain the "
    "Authority's acceptance of its shutdown programme, applications for which shall be made within eight (8) "
    "Working Days of the date of this Addendum, introduces a flow range for the reliability run in Volume II "
    "Clause 7.2, replaces Volume II Clauses 8.1 to 8.3, adds to Volume V Clause 31.1 a new Unavailability Event "
    "for loss of treated effluent volume, with no cure period and with no deduction during the Ramp-Up Period, "
    "and responds to clarification requests 15 to 20.")

OLD_1_3_END = "including any temporary works required to maintain flows during construction."
NEW_1_3_ADD = ("The two designated tie-in points are TP-1 and TP-2, described in Table 1-3, which is reproduced at "
               "Appendix A to this Addendum as issued by the Northern Region Water Services Company (the Network "
               "Operator) and is incorporated into this Volume by reference.")

S2_3 = ("The Bidder shall elect, for each tie-in point, one of the following methods of maintaining flows during "
        "the connection works, and shall state its election in the construction methodology section of the "
        "Technical Proposal: (a) temporary over-pumping, without interruption of flow in the existing collection "
        "network; or (b) interruption of flow within the permitted shutdown window stated for that tie-in point "
        "in Table 1-3.")
S2_4 = ("The temporary works for method (a) shall be capable of passing, at each tie-in point, the maximum "
        "transfer flow stated for that tie-in point in Table 1-3.")
S2_5_APPLY = "not later than eight (8) Working Days before the Proposal Due Date"
S2_5_RESP = "within five (5) Working Days of receipt of a complete application"
S2_5 = ("Where the Bidder elects method (b) for a tie-in point, it shall submit with Envelope A a letter from the "
        "Network Operator accepting the Bidder's proposed shutdown programme for that tie-in point (a Shutdown "
        "Acceptance Letter). Applications for a Shutdown Acceptance Letter shall be made to the Network Operator "
        "%s. The Network Operator has undertaken to respond %s." % (S2_5_APPLY, S2_5_RESP))
S2_6 = ("A Bidder that elects method (b) for a tie-in point but does not submit a Shutdown Acceptance Letter for "
        "that tie-in point with Envelope A shall be deemed to have elected method (a) for that tie-in point.")
S2_7 = ("A Proposal that provides for an interruption of flow at a tie-in point for longer than the maximum "
        "shutdown duration stated for that tie-in point in Table 1-3 shall be rejected.")

OLD_7_2 = "at not less than 90% of nominal capacity"
NEW_7_2 = ("at a daily average flow, measured at the inlet works, of not less than 85% and not more than 110% of "
           "nominal capacity")
S3_2 = ("A day on which the daily average flow is outside that range shall not count towards the thirty (30) days. "
        "Volume II Clause 7.3 is unchanged.")

NEW_8_1 = ("The Project Company shall hold a spare parts inventory sufficient for eighteen (18) months of normal "
           "operation for all items with a lead time exceeding twelve (12) weeks, and shall record that inventory "
           "in the asset register required by Clause 7.4.")
NEW_8_3 = ("The Project Company shall employ a plant manager holding a degree in chemical, civil, environmental or "
           "mechanical engineering and having not less than ten (10) years' experience in the operation of "
           "wastewater treatment facilities, and shall maintain a minimum of two (2) certified operators on shift "
           "at all times. The plant manager proposed for the first two (2) years of operation shall be named in the "
           "Technical Proposal, and his or her curriculum vitae shall be included as an appendix to it.")

OLD_31_1 = ("(b) the treated effluent fails any parameter in Volume II Table 2-4, or (c) the Facility fails to "
            "deliver treated effluent to the delivery point at the required residual head.")
NEW_31_1 = ("(b) the treated effluent fails any parameter in Volume II Table 2-4, (c) the Facility fails to deliver "
            "treated effluent to the delivery point at the required residual head, or (d) the volume of treated "
            "effluent delivered to the delivery point on any day is less than ninety per cent (90%) of the volume "
            "of sewage received at the inlet works on that day.")
OLD_31_3 = "No cure period applies to an event under Clause 31.1(b)."
NEW_31_3 = "No cure period applies to an event under Clause 31.1(b) or Clause 31.1(d)."

QA3 = [
    ["15",
     "Is the Network Operator owned or controlled by the Authority?",
     "No. The Network Operator is a separate company. Its ownership has no bearing on any requirement of the RFP "
     "Documents."],
    ["16",
     "May ozonation be used as the disinfection process?",
     "Ozonation shall not be used as the sole means of disinfection. Disinfection shall be by chlorination with "
     "provision for dechlorination, or by ultraviolet irradiation with a validated dose, or by a combination. "
     "Volume II Clause 3.3 applies."],
    ["17",
     "Volume V Clause 12.3 provides that the reasonable costs of the Independent Engineer are borne equally by the "
     "parties. Does this apply to the Independent Engineer's attendance at a repeated reliability run?",
     "No. The reasonable costs of the Independent Engineer attributable to any reliability run after the first "
     "shall be borne by the Project Company. Volume V Clause 12.3 is amended accordingly."],
    ["18",
     "If the flow delivered to the Facility by the existing collection network during the reliability run under "
     "Volume II Clause 7.2 is lower than the flow required by that Clause, for reasons outside the Project "
     "Company's control, will the Project Company be entitled to relief?",
     "The Authority notes the question. Volume V Clause 34 applies. The Authority does not consider further "
     "amendment necessary at this stage."],
    ["19",
     "Volume II Clause 7.4 requires an asset register in the Authority's standard format. Will the format be "
     "issued before the Proposal Due Date?",
     "No. The format will be issued to the Preferred Bidder. The asset register shall be maintained in the "
     "computerised maintenance management system required by Volume II Clause 8.2 and shall be submitted to the "
     "Authority before the start of the reliability run under Volume II Clause 7.2."],
    ["20",
     "What design flow should be used for the temporary works needed to maintain flows at the tie-in points "
     "referred to in Volume II Clause 1.3?",
     "The temporary works shall be capable of passing the maximum transfer flow stated for each tie-in point in "
     "Table 1-3 at Appendix A to this Addendum. Section 2.4 of this Addendum applies."],
]

EN_TABLE_1_3 = [
    ["TP-1", "Manhole MH-41 on the northern rising main", "1,000", "23:00 to 05:00", "6", "10 Working Days"],
    ["TP-2", "Manhole MH-07 on the southern gravity sewer", "800", "01:00 to 05:00", "6", "10 Working Days"],
]
EN_NOTES_1_3 = [
    ("(1)", "No shutdown is permitted during the holy month of Ramadan."),
    ("(2)", "Only one shutdown is permitted at each tie-in point during the construction period."),
    ("(3)", "Shutdown requests shall be submitted through the Network Operator's electronic portal, accompanied by "
            "the proposed shutdown programme and a contingency plan."),
    ("(4)", "All times are Riyadh time."),
]


def addendum3(image_name):
    F = []
    F.append(Cover("3", issued(ISSUE3), "Tender NUPA/ISTP/2026/014"))
    F.append(Para("proj", "Wadi Sirhan Independent Sewage Treatment Plant"))
    F.append(Para("body", COVER3))
    F.append(Para("body", PRECEDENCE))

    F.append(Para("head", "1. RECITALS"))
    F.append(Para("prov", "This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda "
                          "Nos. 1 and 2 in accordance with Volume I Clause 3.2.", "1.1"))
    F.append(Para("prov", "A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or "
                          "Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.", "1.2"))

    F.append(Para("head", "2. TIE-IN POINTS AND MAINTENANCE OF FLOWS"))
    F.append(Para("prov", "Volume II Clause 1.3 is amended by adding at the end: %s" % q(NEW_1_3_ADD, True), "2.1"))
    F.append(Para("prov", "Table 1-3 is issued in the Arabic language. The Arabic text governs. The English "
                          "translation at Appendix B is provided for convenience only.", "2.2"))
    F.append(Para("prov", S2_3, "2.3"))
    F.append(Para("prov", S2_4, "2.4"))
    F.append(Para("prov", S2_5, "2.5"))
    F.append(Para("prov", S2_6, "2.6"))
    F.append(Para("prov", S2_7, "2.7"))

    F.append(Para("head", "3. RELIABILITY RUN"))
    F.append(Para("prov", "In Volume II Clause 7.2, %s is deleted and %s is substituted."
                  % (q(OLD_7_2), q(NEW_7_2, True)), "3.1"))
    F.append(Para("prov", S3_2, "3.2"))

    F.append(Para("head", "4. OPERATION, MAINTENANCE AND SPARES"))
    F.append(Para("prov", "Volume II Clauses 8.1 to 8.3 are deleted and replaced by the following:", "4.1",
                  keep_next=True))
    F.append(Para("quote", NEW_8_1 + RQ, "8.1"))
    F.append(Para("quote", NEW_8_3 + RQ, "8.3"))
    F.append(Para("prov", "The Clauses of Volume II are not renumbered. Volume II Clauses 8.4 and 8.5 are "
                          "unchanged.", "4.2"))

    F.append(Para("head", "5. UNAVAILABILITY EVENTS"))
    F.append(Para("prov", "In Volume V Clause 31.1, %s is deleted and %s is substituted."
                  % (q(OLD_31_1), q(NEW_31_1, True)), "5.1"))
    F.append(Para("prov", "In Volume V Clause 31.3, %s is deleted and %s is substituted."
                  % (q(OLD_31_3), q(NEW_31_3, True)), "5.2"))

    F.append(Para("head", "6. RESPONSES TO CLARIFICATION REQUESTS 15 TO 20"))
    F.append(QATable(QA3))

    F.append(PageBreak())
    F.append(Para("head", "APPENDIX A — TABLE 1-3 (ARABIC)"))
    F.append(Para("body", "The following table is reproduced as issued by the Network Operator under cover of its "
                          "letter No. 312/2026 dated %d %s %d. The Arabic text governs in accordance with Section "
                          "2.2 of this Addendum." % (LETTER.day, LETTER.strftime("%B"), LETTER.year),
                  keep_next=True))
    F.append(ImageBlock(image_name))
    F.append(Para("body", "End of reproduction."))

    F.append(PageBreak())
    F.append(Para("head", "APPENDIX B — ENGLISH TRANSLATION OF TABLE 1-3"))
    F.append(Para("body", "This translation is provided for convenience only. The Arabic text of Table 1-3 at "
                          "Appendix A governs. Network Operator's letter No. 312/2026 dated %d %s %d. Subject: "
                          "tie-in points with the existing collection network for the Wadi Sirhan Independent "
                          "Sewage Treatment Plant. Tender No. NUPA/ISTP/2026/014."
                  % (LETTER.day, LETTER.strftime("%B"), LETTER.year)))
    F.append(Para("ttitle", "Table 1-3 — Tie-in points and conditions for interruption of flow"))
    F.append(TieInTable(EN_TABLE_1_3))
    F.append(NoteRule())
    F.append(Para("notehdr", "Notes to Table 1-3:"))
    for num, txt in EN_NOTES_1_3:
        F.append(Para("note", txt, num))
    F.append(Para("body", "Signed: Director, Network Operations, Northern Region Water Services Company "
                          "(signature and company stamp)."))
    return F


# ---------------------------- Addendum No. 4 --------------------------------
COVER4 = ("This Addendum amends Section 2.5 of Addendum No. 3, reinstates Volume II Clause 8.2 in amended form, "
          "amends the electronic file naming convention at Volume I Appendix 2, and responds to clarification "
          "request 21.")

A4_NEW_APPLY = "not later than five (5) Working Days before the Proposal Due Date"
A4_NEW_RESP = "within three (3) Working Days of receipt of a complete application"
NEW_8_2 = ("A computerised maintenance management system shall be implemented before the start of the reliability "
           "run under Clause 7.2 and shall remain in use for the concession period.")
OLD_8_2 = ("A computerised maintenance management system shall be implemented before PCOD and shall remain in use "
           "for the concession period.")
OLD_APP2 = "File names shall not exceed 120 characters."
NEW_APP2 = "File names shall not exceed eighty (80) characters, including the extension."

QA4 = [
    ["21",
     "Section 4.1 of Addendum No. 3 replaces Volume II Clauses 8.1 to 8.3 by new Clauses 8.1 and 8.3 only, but the "
     "response to clarification request 19 in that Addendum refers to the computerised maintenance management "
     "system required by Volume II Clause 8.2. Is a computerised maintenance management system required?",
     "Yes. See Section 3 of this Addendum."],
]

S2_5_AS_AMENDED = S2_5.replace(S2_5_APPLY, A4_NEW_APPLY).replace(S2_5_RESP, A4_NEW_RESP)
assert S2_5_AS_AMENDED.count(A4_NEW_APPLY) == 1 and S2_5_AS_AMENDED.count(A4_NEW_RESP) == 1


def addendum4():
    F = []
    F.append(Cover("4", issued(ISSUE4), "Tender NUPA/ISTP/2026/014"))
    F.append(Para("proj", "Wadi Sirhan Independent Sewage Treatment Plant"))
    F.append(Para("body", COVER4))
    F.append(Para("body", PRECEDENCE))

    F.append(Para("head", "1. RECITALS"))
    F.append(Para("prov", "This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda "
                          "Nos. 1, 2 and 3 in accordance with Volume I Clause 3.2.", "1.1"))
    F.append(Para("prov", "A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or "
                          "Form as amended by Addenda Nos. 1, 2 and 3, unless otherwise stated.", "1.2"))
    F.append(Para("prov", "Clarification request 21 was received on %d %s %d, before the time stated in Volume I "
                          "Clause 5.2. Requests received after that time have not been answered."
                  % (Q21_RECEIVED.day, Q21_RECEIVED.strftime("%B"), Q21_RECEIVED.year), "1.3"))

    F.append(Para("head", "2. AMENDMENT TO SECTION 2.5 OF ADDENDUM NO. 3"))
    F.append(Para("prov", "In Section 2.5 of Addendum No. 3, %s is deleted and %s is substituted."
                  % (q(S2_5_APPLY), q(A4_NEW_APPLY, True)), "2.1"))
    F.append(Para("prov", "In Section 2.5 of Addendum No. 3, %s is deleted and %s is substituted."
                  % (q(S2_5_RESP), q(A4_NEW_RESP, True)), "2.2"))
    F.append(Para("prov", "A Shutdown Acceptance Letter issued in response to an application made before the date "
                          "of this Addendum remains valid.", "2.3"))

    F.append(Para("head", "3. REINSTATEMENT OF VOLUME II CLAUSE 8.2"))
    F.append(Para("prov", "Volume II Clause 8.2, deleted by Section 4.1 of Addendum No. 3, is reinstated in the "
                          "following amended form:", "3.1", keep_next=True))
    F.append(Para("quote", NEW_8_2 + RQ, "8.2"))
    F.append(Para("prov", "The response to clarification request 19 in Addendum No. 3 shall be read with Section "
                          "3.1 of this Addendum.", "3.2"))

    F.append(Para("head", "4. AMENDMENT TO VOLUME I APPENDIX 2"))
    F.append(Para("prov", "In Volume I Appendix 2, %s is deleted and %s is substituted. The remainder of "
                          "Appendix 2 is unchanged." % (q(OLD_APP2), q(NEW_APP2, True)), "4.1"))

    F.append(Para("head", "5. RESPONSE TO CLARIFICATION REQUEST 21"))
    F.append(QATable(QA4))

    F.append(PageBreak())
    F.append(Para("head", "APPENDIX A — CONSOLIDATED TEXT FOR CONVENIENCE"))
    F.append(Para("body", "The following consolidated text is provided for convenience only. In the event of any "
                          "discrepancy, the operative provisions of Addenda Nos. 3 and 4 prevail."))
    F.append(Para("prov", "<b>Section 2.5 of Addendum No. 3, as amended by Section 2 of this Addendum</b>", "A.1",
                  keep_next=True))
    F.append(Para("quote", S2_5_AS_AMENDED + RQ, "2.5"))
    F.append(Para("prov", "<b>Volume II Clauses 8.1 to 8.3, as amended by Addenda Nos. 3 and 4</b>", "A.2",
                  keep_next=True))
    F.append(Para("quote", NEW_8_1 + RQ, "8.1"))
    F.append(Para("quote", OLD_8_2 + RQ, "8.2"))          # deliberate: stale consolidated 8.2 (A4 trap)
    F.append(Para("quote", NEW_8_3 + RQ, "8.3"))
    return F


META3 = {"title": "(anonymous)", "author": "(anonymous)", "subject": "(unspecified)",
         "creator": "(unspecified)", "keywords": "", "producer": "ReportLab PDF Library - (opensource)",
         "creationDate": "D:20261110102501+00'00'", "modDate": "D:20261110102501+00'00'"}
META4 = dict(META3, creationDate="D:20261116102501+00'00'", modDate="D:20261116102501+00'00'")
DOC_ID3 = hashlib.md5(b"NUPA/ISTP/2026/014 Addendum No. 3 issued 10 November 2026").hexdigest().upper()
DOC_ID4 = hashlib.md5(b"NUPA/ISTP/2026/014 Addendum No. 4 issued 16 November 2026").hexdigest().upper()


# --------------------------------------------------------------------------
# Consistency check against the issued pack (old quotations verbatim)
# --------------------------------------------------------------------------
V1, V2, V4, V5 = ("VOL-I_Instructions_to_Bidders.pdf", "VOL-II_Technical_Requirements.pdf",
                  "VOL-IV_Form_Sheets.pdf", "VOL-V_Draft_Project_Agreement.pdf")
A1, A2 = "ADD-01_Addendum_No_1.pdf", "ADD-02_Addendum_No_2.pdf"
OLD_QUOTES = [
    # quoted as "old" in Addendum No. 3
    (V2, OLD_1_3_END),
    (V2, OLD_7_2),
    (V5, OLD_31_1),
    (V5, OLD_31_3),
    # quoted as "old" in Addendum No. 4 (base pack)
    (V2, OLD_8_2),
    (V1, OLD_APP2),
    # state_before quotations used by the answer key
    (V2, "The Project Company shall be responsible for all interfaces with the existing collection network at "
         "the two designated tie-in points, including any temporary works required to maintain flows during "
         "construction."),
    (V2, "PCOD shall not be certified until the Facility has completed a continuous reliability run of thirty (30) "
         "days at not less than 90% of nominal capacity, during which every parameter in Table 2-4 has been met."),
    (V2, "A failure of any Table 2-4 parameter during the reliability run shall restart the run in full."),
    (V2, "The Project Company shall provide as-built documentation, operation and maintenance manuals, and an asset "
         "register in the Authority's standard format not later than sixty (60) days after PCOD."),
    (V2, "The Project Company shall hold a spare parts inventory sufficient for two (2) years of normal operation "
         "for all items with a lead time exceeding twelve (12) weeks."),
    (V2, OLD_8_2),
    (V2, "The Project Company shall employ a suitably qualified plant manager and shall maintain a minimum of two "
         "(2) certified operators on shift at all times."),
    (V2, "Sludge shall be dewatered to not less than 22% dry solids"),
    (V2, "A handback condition survey shall be carried out in the final two (2) years of the concession"),
    (V2, "Disinfection shall be by chlorination with provision for dechlorination, or by ultraviolet irradiation "
         "with a validated dose, or by a combination. Ozonation alone is not acceptable."),
    (V2, "The Facility shall be designed for a nominal treatment capacity of 120,000 m3/day average daily flow, "
         "measured at the inlet works"),
    (V2, "The hydraulic profile shall accommodate the flows in Table 2-6 without surcharge of any structure and "
         "without reliance on pumped bypass."),
    (V2, "Each treatment stage shall be arranged in not fewer than four (4) parallel streams, such that the "
         "Facility can meet Table 2-4 with any one stream out of service."),
    (V2, "The Project Company shall carry out factory acceptance testing, site acceptance testing, and integrated "
         "process commissioning in accordance with a commissioning plan approved by the Authority."),
    (V5, "An Unavailability Event occurs where (a) the Facility is unable to treat the flow delivered to it, (b) "
         "the treated effluent fails any parameter in Volume II Table 2-4, or (c) the Facility fails to deliver "
         "treated effluent to the delivery point at the required residual head."),
    (V5, "A cure period of twenty-four (24) hours applies to an Unavailability Event under Clause 31.1(a) and of "
         "seventy-two (72) hours to an event under Clause 31.1(c). No cure period applies to an event under "
         "Clause 31.1(b)."),
    (V5, "Unavailability Event has the meaning given in Clause 31.1."),
    (V5, "PCOD means the date on which the Independent Engineer certifies that the Facility has satisfied the "
         "requirements of Volume II Clause 7.2."),
    (V5, "The Authority shall appoint an Independent Engineer whose reasonable costs shall be borne equally by the "
         "parties."),
    (V5, "The Project Company shall achieve PCOD within thirty-six (36) months of the Notice to Proceed (the "
         "Scheduled PCOD)."),
    (V5, "If PCOD is not achieved by the Scheduled PCOD, the Project Company shall pay to the Authority delay "
         "liquidated damages at the rate of SAR 180,000 for each day of delay."),
    (V5, "From PCOD the Authority shall pay the Project Company the Availability Payment in equal monthly "
         "instalments in arrears, subject to the deductions in Clause 31."),
    (V5, "During the first twelve (12) months after PCOD (the Ramp-Up Period) the Availability Payment shall be "
         "paid at ninety per cent (90%) of the full rate, and no availability deduction shall apply to a parameter "
         "listed in Table 2-4 as assessed on a rolling average basis."),
    (V5, "The Project Company shall not make a distribution to its shareholders unless the conditions to "
         "distribution in the Financing Documents are satisfied and no Unavailability Event is continuing."),
    (V5, "Persistent breach, being three (3) or more Unavailability Events in any rolling ninety (90) day period, "
         "entitles the Authority to require a remediation plan and, on a second occurrence, to terminate under "
         "Clause 39.3."),
    (V5, "On the occurrence of an Unavailability Event the Authority shall deduct from the Availability Payment the "
         "amounts calculated under Schedule 7."),
    (V5, "A Relief Event entitles the Project Company to an extension of time but not to compensation."),
    (V5, "Relief Events comprise: fire, explosion, flood or other physical damage not caused by the Project "
         "Company; failure of a utility not caused by the Project Company; blockade or embargo; and official "
         "strike other than one confined to the Project Company or its subcontractors."),
    (V5, "The Project Company shall notify a Relief Event within five (5) Working Days of becoming aware of it, "
         "failing which no relief shall be granted."),
    (V5, "Availability Payment means the annual payment calculated under Clause 29 and adjusted under Clause 31."),
    (V1, "Working Day means any day from Sunday to Thursday inclusive, other than a day declared a public holiday "
         "in the Kingdom. Where a period expressed in Working Days is to be counted backwards from a stated date, "
         "the stated date itself shall not be counted."),
    (V1, "Requests for clarification shall be submitted no later than ten (10) Working Days before the Proposal Due "
         "Date. Requests received after that time will not be answered."),
    (V1, "(a) the Addenda, a later Addendum prevailing over an earlier one;"),
    (V1, "A Bidder that identifies a conflict, ambiguity or discrepancy shall raise it as a request for "
         "clarification under Section 5."),
    (V1, "The Authority will publish its responses to clarification requests in the form of Addenda issued to all "
         "Bidders."),
    (V1, "Envelope A shall contain, in the following order and separated by numbered dividers:"),
    (V1, "(i) the certificates and evidence required under Section 8."),
    (V1, "excluding the Form Sheets and the appendices expressly permitted by Volume II."),
    (V1, "The Technical Proposal shall address, as a minimum, the process design, the construction methodology and "
         "programme, the operations and maintenance philosophy, the health and safety plan, the environmental and "
         "social management approach, and the organisation and key personnel."),
    (V1, "Each Proposal shall be submitted as one (1) marked original, three (3) hard copies, and one (1) searchable "
         "electronic copy on encrypted USB media. Electronic files shall be named strictly in accordance with the "
         "convention at Appendix 2."),
    (V1, "Files shall be named: ISTP2026-014_[BIDDER]_[ENV]_[VOL]_[NN]_[YYYYMMDD].pdf"),
    (V1, "Non-conforming file names will be corrected by the Authority at the Bidder's risk."),
    (V1, "The concession period shall be twenty-five (25) years commencing on the Project Commercial Operation Date"),
    (V1, "Construction methodology, programme and interface management"),
    (V1, "Operations and maintenance philosophy and lifecycle strategy"),
    (V1, "Organisation, key personnel and consortium governance"),
    (V1, "The appearance of any price, rate, or other commercial information within Envelope A shall render the "
         "Proposal non-responsive."),
    (V4, "Addenda numbered ______ to ______"),
    (A1, "No. The payment mechanism at Volume V Clause 29 is availability based and does not depend on volume "
         "delivered."),
    (A1, "No. The limit applies to the Technical Proposal narrative only. Form Sheets and the appendices permitted "
         "by Volume II are excluded."),
    (A1, "The geotechnical report in the data room is provided for information. Bidders shall satisfy themselves "
         "as to ground conditions."),
    (A2, "In Volume I Clause 9.2, ‘one hundred and twenty (120) pages’ is deleted and ‘one hundred and fifty (150) "
         "pages’ is substituted."),
    (A2, "The Authority refers Bidders to the wording of Clause 31.2."),
    (A2, "Bidders shall design to the figures stated in Volume II. Volume II Clause 4.2 applies."),
    (A2, "The marks available for criterion D are increased and those for criterion B reduced correspondingly."),
    (A2, "Issued 22 October 2026"),
]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def doc_text(path):
    d = pymupdf.open(path)
    return [norm(p.get_text()) for p in d]


def check(pack_dir):
    texts = {}
    for fn in sorted({fn for fn, _ in OLD_QUOTES}):
        texts[fn] = doc_text(pack_dir.rstrip("/") + "/" + fn)
    for fn, quote in OLD_QUOTES:
        whole = norm(" ".join(texts[fn]))
        if norm(quote) not in whole:
            raise SystemExit("NOT VERBATIM in %s: %s" % (fn, quote))
        pages = [i + 1 for i, t in enumerate(texts[fn]) if norm(quote) in t]
        print("verbatim  %-36s p.%-6s %s" % (fn, ",".join(map(str, pages)) or "span", quote[:72]))
    print("verbatim: %d quotations OK" % len(OLD_QUOTES))
    # 7.2 and 31.1 old words occur exactly once in their volume (no ambiguity of target)
    for fn, s in ((V2, OLD_7_2), (V5, OLD_31_1), (V5, OLD_31_3), (V2, OLD_8_2), (V1, OLD_APP2)):
        n = norm(" ".join(texts[fn])).count(norm(s))
        assert n == 1, (fn, s, n)
    for k, v in DATES.items():
        print("date %-40s %s" % (k, long_date(v)))
    print("Working Days from ADD-03 issue (incl.) to the PDD (excl.): %d" % wd_between(ISSUE3, PDD))
    print("Working Days from ADD-04 issue (incl.) to the PDD (excl.): %d" % wd_between(ISSUE4, PDD))
    print("reliability-run band: %d - %d m3/day (was >= %d m3/day)" % (BAND[0], BAND[1], OLD_MIN))
    print("31.1(d) at nominal inflow: >= %d m3/day delivered (loss <= %d m3/day)"
          % (NOMINAL * 9 // 10, NOMINAL // 10))


def check_add04_against_add03(add03_path):
    t3 = norm(" ".join(doc_text(add03_path)))
    for s in (S2_5_APPLY, S2_5_RESP, norm(S2_5)):
        if norm(s) not in t3:
            raise SystemExit("ADD-04 quotation not verbatim in ADD-03: %s" % s)
        assert t3.count(norm(s)) == 1
    print("ADD-04 quotations of ADD-03 Section 2.5: verbatim OK")


def main():
    for name, want in PINNED_FONTS.items():
        got = hashlib.sha256(open(FREEFONT + name, "rb").read()).hexdigest()
        if got != want:
            raise SystemExit("unexpected %s; output would not be reproducible" % name)
    if pymupdf.VersionBind != PINNED_VERSIONS["pymupdf"] or np.__version__ != PINNED_VERSIONS["numpy"]:
        raise SystemExit("pinned versions: %r" % PINNED_VERSIONS)
    args = [a for a in sys.argv[1:]]
    pack = None
    if "--check" in args:
        i = args.index("--check")
        pack = args[i + 1]
        del args[i:i + 2]
    out3 = args[0] if len(args) > 0 else "ADD-03_Addendum_No_3.pdf"
    out4 = args[1] if len(args) > 1 else "ADD-04_Addendum_No_4.pdf"
    if pack:
        check(pack)
    image_raw = table_1_3_image()
    image_name = "FormXob." + hashlib.md5(image_raw).hexdigest()
    n3 = build_pdf(addendum3(image_name), "Addendum No. 3", out3, META3, image_raw, image_name, DOC_ID3)
    n4 = build_pdf(addendum4(), "Addendum No. 4", out4, META4, None, None, DOC_ID4)
    check_add04_against_add03(out3)
    print("pages: ADD-03 %d, ADD-04 %d" % (n3, n4))


if __name__ == "__main__":
    main()
