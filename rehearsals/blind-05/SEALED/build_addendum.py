#!/usr/bin/env python3
"""Builder for ADD-03_Addendum_No_3.pdf (blind rehearsal 05 input).

Draws an "Addendum No. 3" to tender NUPA/ISTP/2026/014 in the page furniture and
typography of the issued Addenda Nos. 1 and 2: A4, Base-14 Type1 fonts (Helvetica,
Helvetica-Bold, Times-Roman, Times-Bold, WinAnsiEncoding, not embedded) for every
text-layer glyph.  There is no Arabic in the text layer.

The Arabic Table 5-1 is an IMAGE-ONLY element reproduced the way Volume II reproduces
Table 2-4: a partial-page "scanned" raster, 1750 px wide, RGB with equal channels,
FlateDecode, drawn at the full frame width (481.8898 pt) directly below an introductory
paragraph.  The raster is produced here from source strings:
  * the Arabic is shaped by MuPDF's HTML engine (HarfBuzz) in GNU FreeSerif,
  * the master is rotated slightly, rasterised at 1750 px across, toned to the pack's
    paper grey (252) and speckled with a fixed-seed numpy generator.

Layout engine: adapted from the blind-04 builder (technique only).  The furniture
(watermark, header, footer) is the ADD-01 / ADD-02 content-stream text.
The output is byte-for-byte deterministic (fixed dates, fixed /ID, fixed seed).

Usage:  python build_addendum.py <output.pdf> [--check <candidate_pack_dir>]
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
IMG_PX_W, IMG_PX_H = 1750, 1500
IMG_W = 481.8898
IMG_ZOOM = IMG_PX_W / IMG_W
IMG_H = IMG_PX_H / IMG_ZOOM
IMG_SEED = 20261115
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
# (superscript as in ADD-02: 0.8 x size, rise 0.5 x size)
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


class HeightTable(Grid):
    COLS = [70.86614, 116.2205, 330.0, 444.0, 524.4094]    # ADD-02 Table 1-1 outer edges

    def __init__(self, rows):
        super().__init__(self.COLS, ["Zone", "Description",
                                     "Maximum height (m above finished ground level)",
                                     "Obstacle lighting"], rows)


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
    if isinstance(fl, Para):
        return fl.height                      # paragraphs are never split
    return fl.height


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
# The "scanned" Arabic Table 5-1 (Appendix A)
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


AR = {
    "office": "مكتب حماية المجال الجوي بالمنطقة الشمالية",
    "ref": "الرقم: ٤٧١/٢٠٢٦",
    "date": "التاريخ: ١٠ نوفمبر ٢٠٢٦م",
    "subject": "الموضوع: اشتراطات الارتفاعات لموقع محطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان",
    "tender": "مناقصة رقم: NUPA/ISTP/2026/014",
    "title": "جدول ٥-١: الحدّ الأقصى لارتفاع المنشآت والمعدّات في الموقع",
    "intro": "يُحدَّد الحدّ الأقصى المسموح به للارتفاع في كل منطقة من مناطق الموقع على النحو الآتي:",
    "h_zone": "المنطقة",
    "h_desc": "الوصف",
    "h_max": "الحدّ الأقصى للارتفاع (متر فوق منسوب الأرض الطبيعية)",
    "h_light": "الإنارة التحذيرية",
    "z_a": "أ",
    "d_a": "الجزء من الموقع الواقع ضمن مسافة ١٬٥٠٠ متر من الحدّ الشرقي للموقع",
    "m_a": "٢٥",
    "l_a": "مطلوبة",
    "z_b": "ب",
    "d_b": "باقي مساحة الموقع",
    "m_b": "٤٠",
    "l_b": "مطلوبة لأي جزء يزيد ارتفاعه على ٣٠ متراً",
    "notes": "ملاحظات:",
    "n1": "١. تسري هذه الحدود على جميع المنشآت الدائمة والمؤقتة، بما في ذلك المداخن والرافعات ومعدّات الإنشاء.",
    "n2": "٢. يُقاس الارتفاع من منسوب الأرض الطبيعية قبل أعمال التسوية والردم.",
    "n3": "٣. يجب إخطار المكتب قبل ثلاثين (٣٠) يوماً على الأقل من تركيب أي رافعة في الموقع.",
    "sign": "مدير المكتب",
}

# Manual line breaks inside table cells (logical order, joined by one space).
AR_LINES = {
    "h_max": ["الحدّ الأقصى للارتفاع", "(متر فوق منسوب الأرض الطبيعية)"],
    "d_a": ["الجزء من الموقع الواقع ضمن مسافة", "١٬٥٠٠ متر من الحدّ الشرقي للموقع"],
    "l_b": ["مطلوبة لأي جزء يزيد", "ارتفاعه على ٣٠ متراً"],
}
for _k, _lines in AR_LINES.items():
    assert " ".join(_lines) == AR[_k], _k


def table_5_1_master():
    """Vector master of the reproduced table (points; 1750 px across when rasterised)."""
    W, H = IMG_W, IMG_H
    doc = pymupdf.open()
    pg = doc.new_page(width=W, height=H)
    L, R = 16.0, W - 16.0
    RX = R - 2.0
    ar_line(pg, AR["office"], RX, 24, 13, bold=True)
    pg.insert_text((L + 2, 22), "Northern Region Airspace Safeguarding Office", fontname="tiro",
                   fontsize=8, color=(0.3, 0.3, 0.3))
    ar_line(pg, AR["ref"], RX, 41, 9.5)
    ar_line(pg, AR["date"], RX - 150, 41, 9.5)
    sh = pg.new_shape()
    sh.draw_line((L, 49), (R, 49))
    sh.finish(color=(0, 0, 0), width=0.9)
    sh.commit()
    ar_line(pg, AR["subject"], RX, 66, 10)
    ar_line(pg, AR["tender"], RX, 81, 10)
    ar_line(pg, AR["title"], RX, 106, 12.5, bold=True)
    ar_line(pg, AR["intro"], RX, 125, 10)
    # table, columns from right to left: zone | description | maximum height | lighting
    cols = [R, R - 46, R - 214, R - 352, L]
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
    pad = 6.0

    def cell(text, ci, baseline, size, bold=False, inset=0.0):
        """Right-aligned Arabic text in column ci; asserts that it fits inside the cell."""
        xr = cols[ci] - pad - inset
        w = ar_line(pg, text, xr, baseline, size, bold)
        if xr - w < cols[ci + 1] + 3.0:
            raise SystemExit("Arabic cell text does not fit: %s" % text)

    cell(AR["h_zone"], 0, top + 23, 10.5, True)
    cell(AR["h_desc"], 1, top + 23, 10.5, True)
    cell(AR_LINES["h_max"][0], 2, top + 16, 10.5, True)
    cell(AR_LINES["h_max"][1], 2, top + 31, 9.5, True)
    cell(AR["h_light"], 3, top + 23, 10.5, True)
    for r, (z, d, m, li) in enumerate([("z_a", "d_a", "m_a", "l_a"), ("z_b", "d_b", "m_b", "l_b")]):
        y0 = top + hh + r * rh
        cell(AR[z], 0, y0 + 22, 11, inset=12)
        if d in AR_LINES:
            cell(AR_LINES[d][0], 1, y0 + 15, 10)
            cell(AR_LINES[d][1], 1, y0 + 30, 10)
        else:
            cell(AR[d], 1, y0 + 22, 10)
        cell(AR[m], 2, y0 + 22, 11, inset=56)
        if li in AR_LINES:
            cell(AR_LINES[li][0], 3, y0 + 15, 10)
            cell(AR_LINES[li][1], 3, y0 + 30, 10)
        else:
            cell(AR[li], 3, y0 + 22, 10)
    y = bottom + 22
    ar_line(pg, AR["notes"], RX, y, 10, bold=True)
    for key in ("n1", "n2", "n3"):
        y += 17
        ar_line(pg, AR[key], RX - 4, y, 9.5)
    y += 34
    ar_line(pg, AR["sign"], L + 120, y, 10.5, bold=True)
    sh = pg.new_shape()
    sh.draw_bezier((L + 30, y + 22), (L + 52, y + 4), (L + 70, y + 30), (L + 98, y + 12))
    sh.finish(color=(0.15, 0.15, 0.15), width=0.9)
    sh.draw_oval(pymupdf.Rect(L + 140, y - 18, L + 196, y + 24))
    sh.finish(color=(0.45, 0.45, 0.45), width=0.8)
    sh.commit()
    if y + 30 > H:
        raise SystemExit("table master overflows")
    return doc


def table_5_1_image():
    """Rotate slightly, rasterise at 1750 px across, tone to paper grey, speckle."""
    master = table_5_1_master()
    scan = pymupdf.open()
    sp = scan.new_page(width=IMG_W, height=IMG_H)
    sp.show_pdf_page(sp.rect, master, 0, rotate=-0.3)
    pix = sp.get_pixmap(matrix=pymupdf.Matrix(IMG_ZOOM, IMG_ZOOM), alpha=False,
                        colorspace=pymupdf.csRGB)
    if (pix.width, pix.height) != (IMG_PX_W, IMG_PX_H):
        raise SystemExit("unexpected raster size %dx%d" % (pix.width, pix.height))
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3).astype(np.int32)
    gray = (a.sum(axis=2) + 1) // 3
    gray = (gray * PAPER + 127) // 255                     # white paper -> 252, as in the pack scans
    rng = np.random.default_rng(IMG_SEED)
    # sparse grey speckle as on the Volume II Table 2-4 scan (about 0.85% of the blank
    # area below 250, roughly four in five of those below 200; grey levels 141-216)
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
    ix = doc.get_new_xref()
    doc.update_object(ix, "<</BitsPerComponent 8/ColorSpace/DeviceRGB/Height %d"
                          "/Subtype/Image/Type/XObject/Width %d>>" % (IMG_PX_H, IMG_PX_W))
    doc.update_stream(ix, image_raw, compress=True)         # MuPDF deflate -> /FlateDecode
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
ISSUE = dt.date(2026, 11, 15)
ADD02 = dt.date(2026, 10, 22)
PDD = dt.date(2026, 11, 26)                     # ADD-01 Section 2.1; 14:00 Riyadh time
LETTER = dt.date(2026, 11, 10)                  # date on the reproduced Table 5-1 letter


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
    "issue": ISSUE,
    "clarification_cutoff_vol1_5_2": wd_before(PDD, 10),
    "base_date_vol5_1_1A": PDD - dt.timedelta(days=28),
    "modification_deadline_vol1_6_6": wd_before(PDD, 2),
    "tall_structure_notice_add03_7_3": wd_before(PDD, 3),
    "table_5_1_letter": LETTER,
    "proposal_due_date": PDD,
}
assert ADD02 < LETTER < ISSUE < PDD
assert is_wd(ISSUE) and is_wd(PDD)
assert DATES["clarification_cutoff_vol1_5_2"] == dt.date(2026, 11, 12)
assert DATES["clarification_cutoff_vol1_5_2"] < ISSUE          # issued after the cut-off
assert DATES["base_date_vol5_1_1A"] == dt.date(2026, 10, 29)
assert DATES["modification_deadline_vol1_6_6"] == dt.date(2026, 11, 24)
assert DATES["tall_structure_notice_add03_7_3"] == dt.date(2026, 11, 23)
assert wd_between(ISSUE, PDD) == 9


# --------------------------------------------------------------------------
# Content of Addendum No. 3
# --------------------------------------------------------------------------
LQ, RQ = "‘", "’"


def q(s, bold=False):
    return LQ + ("<b>%s</b>" % s if bold else s) + RQ


COVER_SUMMARY = (
    "This Addendum consolidates Volume I Clauses 6.6 and 6.7 without change of substance, amends the definition "
    "of Availability Payment and the indexation of the Availability Payment under Volume V Clause 29.2, adds a "
    "membrane filtration requirement to Volume II Clause 3.1, replaces the odour criterion in Volume II Clause "
    "3.5 by reference to the Environmental and Social Impact Assessment, inserts a new Volume II Clause 5.6 "
    "limiting the height of permanent structures at the site in accordance with Table 5-1, and responds to "
    "clarification requests 15 to 21.")

OLD_3_1 = "The Authority does not mandate a particular process train."
NEW_3_1 = ("The treatment process shall include a membrane filtration step, either in the tertiary treatment "
           "stage or as part of a membrane bioreactor, with a nominal pore size not exceeding 0.1 µm. Subject to "
           "the preceding sentence, the Authority does not mandate a particular process train.")

NEW_6_6 = ("A Bidder may withdraw its Proposal at any time before the Proposal Due Date, and may modify its "
           "Proposal not later than two (2) Working Days before the Proposal Due Date, in each case by written "
           "notice through the Portal. A Proposal received after the time stated in Clause 6.1, and a "
           "modification received after the time stated in this Clause, will be rejected unopened and returned "
           "to the Bidder.")

NEW_1_1A = "Base Date means the date falling twenty-eight (28) days before the Proposal Due Date."

NEW_29_2 = ("The Availability Payment shall be indexed annually from the Base Date in accordance with Schedule 9. "
            "The proportion of the payment indexed to the published consumer price index (the Indexed "
            "Proportion) shall be: (a) until the end of the tenth (10th) year of operations, the percentage "
            "stated by the Bidder in Form 4-F, which shall be not less than fifty per cent (50%) and not more "
            "than seventy per cent (70%); and (b) from the start of the eleventh (11th) year of operations, "
            "seventy-five per cent (75%). The balance of the payment shall remain fixed.")

NEW_5_6 = ("The Project Company shall comply with the height limits in Table 5-1, which is reproduced at "
           "Appendix A to this Addendum as issued by the Northern Region Airspace Safeguarding Office and is "
           "incorporated into this Volume by reference.")

QA = [
    ["15",
     "Volume II Clause 6.4 requires process data to be retained for not less than seven (7) years. Would a "
     "retention period of ten (10) years be acceptable?",
     "Volume II Clause 6.4 states a minimum period. A Bidder may propose a longer period but is not required to "
     "do so."],
    ["16",
     "May a Bidder state ‘no deviations’ in Form 4-E and set out its assumptions on Volume V in the Technical "
     "Proposal?",
     "A Bidder that states ‘no deviations’ in Form 4-E shall not include any qualification of Volume V elsewhere "
     "in its Proposal. An assumption that limits or qualifies an obligation in Volume V is a qualification and "
     "shall be listed in Form 4-E. Volume I Clause 9.6 applies."],
    ["17",
     "Where the proposed EPC Contractor is an unincorporated joint venture, which entity must hold the ISO "
     "9001:2015 certificate required by Volume I Clause 8.3?",
     "Each member of the joint venture shall hold a certificate that meets Volume I Clause 8.3, and a copy of "
     "each certificate shall be submitted with Envelope A."],
    ["18",
     "Will the Authority provide dispersion modelling inputs for the design of the odour control system?",
     "The nearest sensitive receptor, and the odour concentration applicable at it for the purposes of Volume "
     "II Clause 3.4 as amended by Section 5 of this Addendum, are shown in Figure 7-2 of the Environmental and "
     "Social Impact Assessment, which is available to Bidders in the data room. No other modelling inputs will "
     "be provided."],
    ["19",
     "Form 4-F requests the Availability Payment for year 1 of operations. Is that figure to be stated in the "
     "prices of year 1 of operations?",
     "Yes. The Availability Payment stated in Form 4-F is the amount payable for year 1 of operations, in the "
     "prices of that year. Indexation under Volume V Clause 29.2 applies from the first anniversary of PCOD."],
    ["20",
     "Form 4-F states ‘Per Volume V Clause 29.2’ against ‘Indexation basis assumed’. Is any figure to be "
     "stated in that row?",
     "Yes. The Bidder shall complete that row by stating, after the words ‘Per Volume V Clause 29.2’, the "
     "Indexed Proportion as a percentage. The Indexed Proportion shall not be stated anywhere in Envelope A. "
     "Volume I Clause 6.2 applies."],
    ["21",
     "Does the Technical Proposal need to address construction plant in addition to the matters listed in "
     "Volume I Clause 9.7?",
     "Yes. The construction methodology in the Technical Proposal shall include a crane and lifting plan that "
     "demonstrates compliance with Table 5-1 (Volume II Clause 5.6, inserted by Section 7 of this Addendum)."],
]

EN_TABLE = [
    ["A", "The part of the site within 1,500 m of the eastern site boundary", "25", "Required"],
    ["B", "The remainder of the site", "40", "Required for any part exceeding 30 m"],
]
EN_NOTES = [
    ("(1)", "These limits apply to all permanent structures, including stacks."),
    ("(2)", "Height is measured from finished ground level after grading and filling."),
    ("(3)", "The Office shall be notified at least thirty (30) days before any crane is erected at the site."),
]


def addendum3():
    F = []
    F.append(Cover("3", "Issued %d %s %d" % (ISSUE.day, ISSUE.strftime("%B"), ISSUE.year),
                   "Tender NUPA/ISTP/2026/014"))
    F.append(Para("proj", "Wadi Sirhan Independent Sewage Treatment Plant"))
    F.append(Para("body", COVER_SUMMARY))
    F.append(Para("body",
        "This Addendum forms part of the RFP Documents and takes precedence in accordance with Volume I Clause "
        "3.2. Bidders shall acknowledge receipt in Form 4-A. All other terms of the RFP Documents remain unchanged."))

    # 1 -------------------------------------------------------------------
    F.append(Para("head", "1. RECITALS"))
    F.append(Para("prov", "This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda "
                          "Nos. 1 and 2 in accordance with Volume I Clause 3.2.", "1.1"))
    F.append(Para("prov", "A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or "
                          "Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.", "1.2"))
    F.append(Para("prov", "Requests for clarification received after the time stated in Volume I Clause 5.2 have "
                          "not been answered.", "1.3"))

    # 2 -------------------------------------------------------------------
    F.append(Para("head", "2. CONSOLIDATION OF VOLUME I CLAUSES 6.6 AND 6.7"))
    F.append(Para("prov", "Volume I Clauses 6.6 and 6.7 are deleted and replaced by the following single Clause "
                          "6.6:", "2.1", keep_next=True))
    F.append(Para("quote", NEW_6_6 + RQ, "6.6"))
    F.append(Para("prov", "The number 6.7 is not reused. The Clauses of Volume I are not renumbered.", "2.2"))

    # 3 -------------------------------------------------------------------
    F.append(Para("head", "3. AVAILABILITY PAYMENT AND INDEXATION"))
    F.append(Para("prov", "In Volume V Clause 1.1, %s is deleted and %s is substituted."
                  % (q("the annual payment calculated under Clause 29"),
                     q("the annual payment, expressed at Base Date prices, calculated under Clause 29", True)),
                  "3.1"))
    F.append(Para("prov", "The following new Clause 1.1A is inserted in Volume V after Clause 1.1:", "3.2",
                  keep_next=True))
    F.append(Para("quote", NEW_1_1A + RQ, "1.1A"))
    F.append(Para("prov", "Volume V Clause 29.2 is deleted and replaced by the following:", "3.3", keep_next=True))
    F.append(Para("quote", NEW_29_2 + RQ, "29.2"))
    F.append(Para("prov", "Bidders shall reflect this Section 3 in the Financial Model submitted under Volume I "
                          "Clause 10.3.", "3.4"))

    # 4 -------------------------------------------------------------------
    F.append(Para("head", "4. MEMBRANE FILTRATION"))
    F.append(Para("prov", "In Volume II Clause 3.1, %s is deleted and %s is substituted."
                  % (q(OLD_3_1), q(NEW_3_1, True)), "4.1"))
    F.append(Para("prov", "Bidders shall reflect this Section 4 in the process design submitted under Volume II "
                          "Section 3.", "4.2"))

    # 5 -------------------------------------------------------------------
    F.append(Para("head", "5. ODOUR CONTROL"))
    F.append(Para("prov", "In Volume II Clause 3.4, %s is deleted and %s is substituted. The basis of assessment "
                          "(98th percentile hourly value) is unchanged."
                  % (q("not more than 5 OU/m<sup>3</sup> at the site boundary"),
                     q("not more than the odour concentration shown for the nearest sensitive receptor in Figure "
                       "7-2 of the Environmental and Social Impact Assessment referred to in Volume II Clause 9.1, "
                       "at that receptor", True)), "5.1"))
    F.append(Para("prov", "Bidders shall demonstrate compliance with Volume II Clause 3.4, as amended, in the "
                          "Technical Proposal.", "5.2"))

    # 6 -------------------------------------------------------------------
    F.append(Para("head", "6. RESPONSES TO CLARIFICATION REQUESTS 15 TO 21"))
    F.append(QATable(QA))

    # 7 -------------------------------------------------------------------
    F.append(Para("head", "7. HEIGHT OF STRUCTURES"))
    F.append(Para("prov", "The following new Clause 5.6 is inserted in Volume II after Clause 5.5:", "7.1",
                  keep_next=True))
    F.append(Para("quote", NEW_5_6 + RQ, "5.6"))
    F.append(Para("prov", "Table 5-1 is issued in the Arabic language. The Arabic text governs. The English "
                          "translation at Appendix B is provided for convenience only.", "7.2"))
    F.append(Para("prov", "A Bidder whose Proposal provides for any structure, plant or equipment at the site "
                          "exceeding thirty (30) metres in height shall notify the Authority through the Portal, not "
                          "later than three (3) Working Days before the Proposal Due Date, of the zone of Table 5-1 "
                          "in which it is to be located and its proposed height.", "7.3"))
    F.append(Para("prov", "Bidders shall reflect Table 5-1 in the Technical Proposal.", "7.4"))

    # Appendix A ----------------------------------------------------------
    F.append(PageBreak())
    F.append(Para("head", "APPENDIX A — TABLE 5-1 (ARABIC)"))
    F.append(Para("body", "Table 5-1 is reproduced below as issued by the Northern Region Airspace Safeguarding "
                          "Office. The Arabic text governs in accordance with Section 7 of this Addendum.",
                  keep_next=True))
    F.append(ImageBlock(IMAGE_NAME))
    F.append(Para("body", "End of reproduction."))

    # Appendix B ----------------------------------------------------------
    F.append(PageBreak())
    F.append(Para("head", "APPENDIX B — ENGLISH TRANSLATION OF TABLE 5-1"))
    F.append(Para("body", "This translation is provided for convenience only. The Arabic text of Table 5-1 at "
                          "Appendix A governs."))
    F.append(Para("ttitle", "Table 5-1 — Maximum height of structures and equipment at the site"))
    F.append(HeightTable(EN_TABLE))
    F.append(NoteRule())
    F.append(Para("notehdr", "Notes to Table 5-1:"))
    for num, txt in EN_NOTES:
        F.append(Para("note", txt, num))
    return F


IMAGE_NAME = None
META = {"title": "(anonymous)", "author": "(anonymous)", "subject": "(unspecified)",
        "creator": "(unspecified)", "keywords": "", "producer": "ReportLab PDF Library - (opensource)",
        "creationDate": "D:20261115102501+00'00'", "modDate": "D:20261115102501+00'00'"}
DOC_ID = hashlib.md5(b"NUPA/ISTP/2026/014 Addendum No. 3 issued 15 November 2026").hexdigest().upper()


# --------------------------------------------------------------------------
# Consistency check against the issued pack (old quotations verbatim)
# --------------------------------------------------------------------------
OLD_QUOTES = [
    ("VOL-I_Instructions_to_Bidders.pdf", "A Proposal received after the time stated in Clause 6.1 will be rejected "
     "unopened and returned to the Bidder."),
    ("VOL-I_Instructions_to_Bidders.pdf", "A Bidder may withdraw or modify its Proposal at any time before the "
     "Proposal Due Date by written notice through the Portal. No modification will be accepted thereafter."),
    ("VOL-I_Instructions_to_Bidders.pdf", "Working Day means any day from Sunday to Thursday inclusive, other than a "
     "day declared a public holiday in the Kingdom. Where a period expressed in Working Days is to be counted "
     "backwards from a stated date, the stated date itself shall not be counted."),
    ("VOL-I_Instructions_to_Bidders.pdf", "Requests for clarification shall be submitted no later than ten (10) "
     "Working Days before the Proposal Due Date. Requests received after that time will not be answered."),
    ("VOL-I_Instructions_to_Bidders.pdf", "(a) the Addenda, a later Addendum prevailing over an earlier one;"),
    ("VOL-I_Instructions_to_Bidders.pdf", "A Bidder that identifies a conflict, ambiguity or discrepancy shall raise "
     "it as a request for clarification under Section 5. A Bidder that resolves such a conflict unilaterally does "
     "so at its own risk, and the Authority shall not be bound by the Bidder's interpretation."),
    ("VOL-I_Instructions_to_Bidders.pdf", "The appearance of any price, rate, or other commercial information within "
     "Envelope A shall render the Proposal non-responsive."),
    ("VOL-I_Instructions_to_Bidders.pdf", "The proposed EPC Contractor shall hold a valid ISO 9001:2015 quality "
     "management certificate, current as at the Proposal Due Date, issued by an accredited certification body. A "
     "copy of the certificate shall be submitted with Envelope A."),
    ("VOL-I_Instructions_to_Bidders.pdf", "Form 4-E shall list every deviation, qualification or reservation to Volume "
     "V. A Proposal that states ‘no deviations’ in Form 4-E while containing a qualification elsewhere in the "
     "Proposal shall be treated as non-responsive."),
    ("VOL-I_Instructions_to_Bidders.pdf", "The Technical Proposal shall address, as a minimum, the process design, "
     "the construction methodology and programme, the operations and maintenance philosophy, the health and safety "
     "plan, the environmental and social management approach, and the organisation and key personnel."),
    ("VOL-I_Instructions_to_Bidders.pdf", "Envelope B shall contain only (a) Form 4-F (Financial Proposal Schedule) "
     "and (b) the Financial Model. No other document shall be placed in Envelope B."),
    ("VOL-I_Instructions_to_Bidders.pdf", "The Bidder shall quote a single Availability Payment expressed in Saudi "
     "Riyals per annum, calculated in accordance with the payment mechanism at Volume V Clause 29."),
    ("VOL-I_Instructions_to_Bidders.pdf", "Any conditional price, price subject to adjustment other than as provided "
     "in Volume V, or alternative price shall render the Proposal non-responsive."),
    ("VOL-I_Instructions_to_Bidders.pdf", "A response to a clarification shall not change the Availability Payment "
     "quoted; any response that does so shall render the Proposal non-responsive."),
    ("VOL-I_Instructions_to_Bidders.pdf", "Proposal Due Date means the date and time stated in Clause 6.1, as the "
     "same may be amended by Addendum."),
    ("VOL-I_Instructions_to_Bidders.pdf", "Construction methodology, programme and interface management"),
    ("VOL-I_Instructions_to_Bidders.pdf", "The concession period shall be twenty-five (25) years commencing on the "
     "Project Commercial Operation Date"),
    ("VOL-II_Technical_Requirements.pdf", "The Authority does not mandate a particular process train."),
    ("VOL-II_Technical_Requirements.pdf", "Where a membrane process is proposed, the Project Company shall "
     "demonstrate membrane replacement provisions in the lifecycle plan and shall warrant a membrane life of not "
     "less than seven (7) years."),
    ("VOL-II_Technical_Requirements.pdf", "Each treatment stage shall be arranged in not fewer than four (4) parallel "
     "streams, such that the Facility can meet Table 2-4 with any one stream out of service."),
    ("VOL-II_Technical_Requirements.pdf", "with lifecycle replacement provided for in the Project Company's "
     "lifecycle plan"),
    ("VOL-II_Technical_Requirements.pdf", "Odour control shall achieve not more than 5 OU/m3 at the site boundary, "
     "assessed as a 98th percentile hourly value."),
    ("VOL-II_Technical_Requirements.pdf", "not more than 5 OU/m3 at the site boundary"),
    ("VOL-II_Technical_Requirements.pdf", "Noise at the nearest sensitive receptor shall not exceed 55 dB(A) by day "
     "and 45 dB(A) by night."),
    ("VOL-II_Technical_Requirements.pdf", "All process data shall be retained for not less than seven (7) years and "
     "shall be made available to the Authority on demand in a non-proprietary format."),
    ("VOL-II_Technical_Requirements.pdf", "The Project Company shall comply with the Environmental and Social Impact "
     "Assessment prepared for the site and available in the data room"),
    ("VOL-II_Technical_Requirements.pdf", "All permanent civil structures shall be designed for a seismic event with "
     "a return period of 475 years and for a flood with a return period of 100 years."),
    ("VOL-II_Technical_Requirements.pdf", "The treated effluent shall at all times comply with the parameters set out "
     "in Table 2-4."),
    ("VOL-IV_Form_Sheets.pdf", "Availability Payment (SAR per annum, year 1 of operations)"),
    ("VOL-IV_Form_Sheets.pdf", "Indexation basis assumed Per Volume V Clause 29.2"),
    ("VOL-IV_Form_Sheets.pdf", "We confirm that the Availability Payment stated above is unconditional, is not subject "
     "to any qualification, and has been derived from the Financial Model submitted with this Form."),
    ("VOL-IV_Form_Sheets.pdf", "Forms shall be reproduced without alteration to their wording."),
    ("VOL-IV_Form_Sheets.pdf", "Envelope B only. This Form and the Financial Model are the only documents to be "
     "placed in Envelope B."),
    ("VOL-V_Draft_Project_Agreement.pdf", "Availability Payment means the annual payment calculated under Clause 29 "
     "and adjusted under Clause 31."),
    ("VOL-V_Draft_Project_Agreement.pdf", "the annual payment calculated under Clause 29"),
    ("VOL-V_Draft_Project_Agreement.pdf", "The Availability Payment shall be indexed annually in accordance with "
     "Schedule 9, with sixty per cent (60%) of the payment indexed to the published consumer price index and forty "
     "per cent (40%) remaining fixed."),
    ("VOL-V_Draft_Project_Agreement.pdf", "From PCOD the Authority shall pay the Project Company the Availability "
     "Payment in equal monthly instalments in arrears, subject to the deductions in Clause 31."),
    ("VOL-V_Draft_Project_Agreement.pdf", "An Unavailability Event occurs where (a) the Facility is unable to treat "
     "the flow delivered to it, (b) the treated effluent fails any parameter in Volume II Table 2-4, or (c) the "
     "Facility fails to deliver treated effluent to the delivery point at the required residual head."),
    ("VOL-V_Draft_Project_Agreement.pdf", "The Project Company shall achieve PCOD within thirty-six (36) months of "
     "the Notice to Proceed (the Scheduled PCOD)."),
    ("ADD-01_Addendum_No_1.pdf", "Volume I Clause 6.1 is amended by deleting ‘Thursday 12 November 2026’ and "
     "substituting ‘Thursday 26 November 2026’. The time of 14:00 Riyadh time is unchanged."),
    ("ADD-01_Addendum_No_1.pdf", "Capitalised terms have the meanings given in Volume I."),
    ("ADD-01_Addendum_No_1.pdf", "Is a membrane bioreactor process mandatory? No. Volume II Clause 3.1 does not "
     "mandate a process train. Any process capable of meeting Table 2-4 under the Table 2-2 influent conditions is "
     "acceptable."),
    ("VOL-V_Draft_Project_Agreement.pdf", "The Project Company shall transfer the Facility to the Authority on expiry "
     "in the condition required by Volume II Clause 8.5, free of encumbrance and with a remaining design life of "
     "not less than five (5) years for all major assets."),
    ("VOL-V_Draft_Project_Agreement.pdf", "This Agreement shall come into force on the Effective Date and shall "
     "continue for a period of twenty-five (25) years from the Effective Date"),
    ("ADD-02_Addendum_No_2.pdf", "The Authority does not consider further amendment necessary at this stage."),
    ("ADD-02_Addendum_No_2.pdf", "Issued 22 October 2026"),
    ("ADD-02_Addendum_No_2.pdf", "This Addendum is issued under Volume I Clause 5.3 and takes precedence over "
     "Addendum No. 1 in accordance with Volume I Clause 3.2."),
]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def pack_texts(pack_dir):
    texts = {}
    for fn in sorted({fn for fn, _ in OLD_QUOTES}):
        d = pymupdf.open(pack_dir.rstrip("/") + "/" + fn)
        texts[fn] = [norm(p.get_text()) for p in d]
    return texts


def check(pack_dir):
    texts = pack_texts(pack_dir)
    for fn, quote in OLD_QUOTES:
        whole = norm(" ".join(texts[fn]))
        if norm(quote) not in whole:
            raise SystemExit("NOT VERBATIM in %s: %s" % (fn, quote))
        pages = [i + 1 for i, t in enumerate(texts[fn]) if norm(quote) in t]
        print("verbatim  %-36s p.%-6s %s" % (fn, ",".join(map(str, pages)) or "span", quote[:70]))
    print("verbatim: %d quotations OK" % len(OLD_QUOTES))
    for k, v in DATES.items():
        print("date %-34s %s" % (k, long_date(v)))
    print("Working Days from issue (incl.) to the PDD (excl.): %d" % wd_between(ISSUE, PDD))
    print("Indexed Proportion band 50%-70% -> fixed balance 50%-30% (years 1-10); year 11+: 75% / 25%")
    # membrane replacement over a 25-year term (VOL-I 12.1) with the 7-year minimum life (VOL-II 3.2),
    # with and without the 5-year remaining-life handback condition (VOL-V 42.1)
    term, life, handback = 25, 7, 5
    plain = [y for y in range(life, term, life)]
    last_install_for_handback = term + handback - life
    print("membrane replacements at a %d-year life over %d years: %s (%d)" % (life, term, plain, len(plain)))
    print("for >= %d years remaining at year %d, the last set must be installed in or after year %d"
          % (handback, term, last_install_for_handback))


def main():
    global IMAGE_NAME
    for name, want in PINNED_FONTS.items():
        got = hashlib.sha256(open(FREEFONT + name, "rb").read()).hexdigest()
        if got != want:
            raise SystemExit("unexpected %s; output would not be reproducible" % name)
    if pymupdf.VersionBind != PINNED_VERSIONS["pymupdf"] or np.__version__ != PINNED_VERSIONS["numpy"]:
        raise SystemExit("pinned versions: %r" % PINNED_VERSIONS)
    out = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "ADD-03_Addendum_No_3.pdf"
    if "--check" in sys.argv:
        check(sys.argv[sys.argv.index("--check") + 1])
    image_raw = table_5_1_image()
    IMAGE_NAME = "FormXob." + hashlib.md5(image_raw).hexdigest()
    n = build_pdf(addendum3(), "Addendum No. 3", out, META, image_raw, IMAGE_NAME, DOC_ID)
    print("pages:", n)


if __name__ == "__main__":
    main()
