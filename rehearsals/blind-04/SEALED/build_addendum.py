#!/usr/bin/env python3
"""Builder for ADD-03_Addendum_No_3.pdf (blind rehearsal 04 input).

Draws an "Addendum No. 3" to tender NUPA/ISTP/2026/014 in the page furniture and
typography of the issued Addenda Nos. 1 and 2: A4, Base-14 Type1 fonts (Helvetica,
Helvetica-Bold, Times-Roman, Times-Bold, WinAnsiEncoding, not embedded) for every
text-layer glyph.  There is no Arabic in the text layer.  The Arabic Form 4-H is an
IMAGE-ONLY page (a "scanned" 1654 x 2339 RGB raster, FlateDecode, drawn exactly as the
Form 4-C image is drawn in Volume IV), produced here from source strings:
  * the Arabic is shaped by MuPDF's HTML engine (HarfBuzz) in GNU FreeSerif,
  * the form page is rotated slightly, rasterised at 200 dpi and speckled with a
    fixed-seed numpy generator, then deflated by MuPDF.

Layout engine: adapted from the blind-03 builder (technique only).  Geometry of the
Table 1-1 grid, notes rule and notes was measured from ADD-02 (raw content stream).
The output is byte-for-byte deterministic (fixed dates, fixed /ID, fixed seed).

Usage:  python build_addendum.py <output.pdf> [--check <candidate_pack_dir>]
"""
import datetime as dt
import hashlib
import io
import math
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

# Placement of the form image: identical to the Form 4-C image in Volume IV page 6.
IMG_X, IMG_Y, IMG_W, IMG_H = 66.61417, 120.1246, 462.0472, 653.403
IMG_PX_W, IMG_PX_H = 1654, 2339
IMG_SEED = 20261109


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
# Rich text: markup with <b>..</b>
# --------------------------------------------------------------------------
def parse_runs(markup, size, reg=REG, bold=BOLD):
    runs, b = [], False
    for tok in re.split(r"(</?b>)", markup):
        if tok == "<b>":
            b = True
        elif tok == "</b>":
            b = False
        elif tok:
            runs.append((tok, bold if b else reg, size, 0))
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
    """kind: body | prov | cont | quote | quote2 | head | proj | formtitle |
    ttitle | notehdr | note"""

    STYLES = {
        "body": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "prov": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "cont": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "quote": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "quote2": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "head": dict(size=13, lead=16, reg="F2", bold="F2", justify=False),
        "proj": dict(size=10.5, lead=13, reg="F2", bold="F2", justify=False),
        "formtitle": dict(size=10.5, lead=13, reg="F2", bold="F2", justify=False),
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
        elif kind == "cont":
            prefix = []
            self.x_first = self.x_rest = PARA_L + HANG
        elif kind == "quote":
            prefix = [("‘", REG, self.size, 0), (num, BOLD, self.size, 0),
                      ("  ", REG, self.size, 0)]
            self.x_first, self.x_rest = PARA_L + QUOTE_FIRST, PARA_L + QUOTE_REST
        elif kind == "quote2":
            prefix = []
            self.x_first = self.x_rest = PARA_L + QUOTE_FIRST
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
    """Ruled table with a dark header band; splits with the header repeated."""
    SIZE, LEAD, PAD_T, PAD_B, PAD_X = 8.2, 10.4, 3.5, 3.5, 4.0
    kind = "table"

    def __init__(self, cols, head, rows):
        self.cols, self.head = cols, head
        self.rows = []
        for r in rows:
            cells = []
            for ci, txt in enumerate(r):
                avail = cols[ci + 1] - cols[ci] - 2 * self.PAD_X
                runs = parse_runs(txt, self.SIZE, REG, BOLD)
                cells.append(break_lines([], runs, avail, avail) if txt else [])
            n = max(1, max(len(c) for c in cells))
            self.rows.append((cells, self.PAD_T + n * self.LEAD + self.PAD_B))
        self.head_h = self.PAD_T + self.LEAD + self.PAD_B

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
        for ci, h in enumerate(self.head):
            o.append("BT 1 0 0 1 %s %s Tm /F2 8.2 Tf 10.4 TL 1 1 1 rg %s Tj T* ET"
                     % (fmt(self.cols[ci] + self.PAD_X), fmt(Y(top + self.PAD_T + self.SIZE)), pstr(h)))
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


class EvalTable(Grid):
    COLS = [70.86614, 116.2205, 467.7165, 524.4094]        # ADD-02 Table 1-1 (revised) grid

    def __init__(self, rows):
        super().__init__(self.COLS, ["Ref", "Criterion", "Marks"], rows)


class OwnerTable(Grid):
    COLS = [56.69291, 90.70866, 270.0, 350.0, 460.0, 538.5827]

    def __init__(self, rows):
        super().__init__(self.COLS, ["No", "Name of beneficial owner", "Nationality",
                                     "Ownership (%)", "Direct / indirect"], rows)


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


class ImagePage:
    """A page carrying only the furniture and one full-page image."""
    kind = "image"
    height = 0.0

    def __init__(self, name):
        self.name = name

    def draw(self, top):
        return ("q\n1 0 0 1 %s %s cm\nq\n%s 0 0 %s 0 0 cm\n/%s Do\nQ\nQ"
                % (fmt(IMG_X), fmt(IMG_Y), fmt(IMG_W), fmt(IMG_H), self.name))


def kind_of(fl):
    return fl.kind


def gap(prev, nxt):
    if prev is None:
        return 0.0
    if prev == "cover":
        return 18.0
    if prev in ("proj", "formtitle"):
        return 4.0
    if nxt == "head":
        return 14.0
    if prev == "head":
        return 7.0
    if nxt == "formtitle":
        return 19.0
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
        return fl.lead * min(2, len(fl.lines))
    return fl.height


def layout(flowables):
    """Returns a list of pages; each page is (list of content chunks, has_image)."""
    pages, cur, top, prev, img = [], [], CONTENT_TOP, None, None
    i = 0
    started = False

    def flush():
        pages.append((cur, img))

    while i < len(flowables):
        fl = flowables[i]
        k = kind_of(fl)
        if k == "break":
            flush()
            cur, top, prev, img = [], CONTENT_TOP, None, None
            i += 1
            continue
        if k == "image":
            if cur:
                flush()
            cur, img = [fl.draw(0)], fl.name
            flush()
            cur, top, prev, img = [], CONTENT_TOP, None, None
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
                cur, top, prev, img = [], CONTENT_TOP, None, None
                continue
            s, h = fl.draw_rows(t, start, n)
            cur.append(s)
            fl._next = start + n
            if fl._next < len(fl.rows):
                flush()
                cur, top, prev, img = [], CONTENT_TOP, None, None
                continue
            top, prev = t + h, k
            i += 1
            continue
        need = fl.height
        keep = k in ("head", "formtitle", "ttitle", "notehdr") or getattr(fl, "keep_next", False)
        if keep and i + 1 < len(flowables):
            nx = flowables[i + 1]
            need = fl.height + gap(k, kind_of(nx)) + first_height(nx)
        if prev is not None and t + need > CONTENT_BOTTOM:
            flush()
            cur, top, prev, img = [], CONTENT_TOP, None, None
            continue
        cur.append(fl.draw(t))
        top, prev = t + fl.height, k
        i += 1
    if cur:
        flush()
    return pages


# --------------------------------------------------------------------------
# The "scanned" Arabic form (Appendix A)
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
    more, _ = story.place(pymupdf.Rect(50, 2 * size, 1450, 6 * size))  # room around for marks
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
    "authority": "الهيئة الشمالية للمشتريات المرفقية",
    "tender": "مناقصة رقم: NUPA/ISTP/2026/014",
    "form_no": "النموذج ٤-ح",
    "title": "إقرار المستفيد الحقيقي",
    "intro_1": "نحن الموقعون أدناه، بصفتنا ممثلين مفوضين عن العضو المذكور أدناه في ائتلاف مقدم العرض،",
    "intro_2": "نقر ونتعهد بما يلي:",
    "first": ("أولاً: أن الأشخاص الطبيعيين المبينين في الجدول أدناه هم جميع المستفيدين الحقيقيين من العضو، "
              "والمستفيد الحقيقي هو كل شخص طبيعي يملك، بصورة مباشرة أو غير مباشرة، ما نسبته عشرة في "
              "المائة (١٠٪) أو أكثر من رأس مال العضو أو من حقوق التصويت فيه، أو يسيطر على العضو بأي "
              "وسيلة أخرى."),
    "second": ("ثانياً: أنه لا يملك أيٌّ من المستفيدين الحقيقيين، بصورة مباشرة أو غير مباشرة، أي حصة في "
               "عضو في ائتلاف آخر يقدم عرضاً لهذه المناقصة."),
    "third": ("ثالثاً: أننا أرفقنا بهذا الإقرار نسخة مصدقة من سجل الشركاء أو المساهمين في العضو، صادرة "
              "خلال الثلاثين (٣٠) يوماً السابقة لتاريخ تقديم العروض."),
    "col_no": "م",
    "col_name": "اسم المستفيد الحقيقي",
    "col_nat": "الجنسية",
    "col_pct": "نسبة الملكية (٪)",
    "col_dir": "مباشرة / غير مباشرة",
    "rows": ["١", "٢", "٣", "٤"],
    "f_member": "اسم العضو في الائتلاف :",
    "f_cr": "رقم السجل التجاري :",
    "f_signatory": "اسم المفوض بالتوقيع :",
    "f_capacity": "الصفة :",
    "f_date": "التاريخ :",
    "f_sign": "التوقيع والختم :",
    "note_1": "ملاحظة: يجب تقديم هذا النموذج باللغة العربية عن كل عضو من أعضاء الائتلاف، والنص العربي هو المعتمد.",
    "note_2": "عدم تقديمه كاملاً يجعل العرض غير مستجيب.",
}

# Line breaks of the Arabic paragraphs on the form (logical order, joined by one space).
AR_LINES = {
    "first": ["أولاً: أن الأشخاص الطبيعيين المبينين في الجدول أدناه هم جميع المستفيدين الحقيقيين من العضو،",
              "والمستفيد الحقيقي هو كل شخص طبيعي يملك، بصورة مباشرة أو غير مباشرة، ما نسبته عشرة في",
              "المائة (١٠٪) أو أكثر من رأس مال العضو أو من حقوق التصويت فيه، أو يسيطر على العضو بأي",
              "وسيلة أخرى."],
    "second": ["ثانياً: أنه لا يملك أيٌّ من المستفيدين الحقيقيين، بصورة مباشرة أو غير مباشرة، أي حصة في",
               "عضو في ائتلاف آخر يقدم عرضاً لهذه المناقصة."],
    "third": ["ثالثاً: أننا أرفقنا بهذا الإقرار نسخة مصدقة من سجل الشركاء أو المساهمين في العضو، صادرة",
              "خلال الثلاثين (٣٠) يوماً السابقة لتاريخ تقديم العروض."],
}
for _k, _lines in AR_LINES.items():
    assert " ".join(_lines) == AR[_k], _k


def form_4h_page():
    """Vector master of the form, on an A4 page (points)."""
    W, H = PAGE_W, PAGE_H
    doc = pymupdf.open()
    pg = doc.new_page(width=W, height=H)
    L, R = 37.0, 566.0          # content box, as on the Form 4-C master
    RX = R - 9.0                # right edge of Arabic text
    sh = pg.new_shape()
    sh.draw_rect(pymupdf.Rect(L - 6, 25, R + 6, 82))
    sh.finish(color=(0, 0, 0), width=1.1)
    sh.commit()
    pg.insert_text((L + 5, 46), "NORTHERN UTILITIES PROCUREMENT AUTHORITY", fontname="tibo", fontsize=11.5)
    pg.insert_text((L + 5, 70), "Tender Ref: NUPA/ISTP/2026/014", fontname="tiro", fontsize=11,
                   color=(0.25, 0.25, 0.25))
    ar_line(pg, AR["authority"], RX, 49, 16, bold=True)
    ar_line(pg, AR["tender"], RX, 71, 11)
    pg.insert_text((L + 5, 108), "FORM 4-H", fontname="tibo", fontsize=12)
    ar_line(pg, AR["form_no"], RX, 111, 16, bold=True)
    ar_line(pg, AR["title"], RX, 138, 18, bold=True)
    y = 167.0
    ar_line(pg, AR["intro_1"], RX, y, 14)
    y += 20
    ar_line(pg, AR["intro_2"], RX, y, 14)
    y += 28
    for key in ("first", "second", "third"):
        for ln in AR_LINES[key]:
            ar_line(pg, ln, RX, y, 14)
            y += 20.5
        y += 12
    # beneficial owners table (right to left)
    y -= 2
    cols = [R, R - 40, R - 230, R - 318, R - 426, L]        # right edges, first column at right
    top, hh, rh = y, 24.0, 21.0
    bottom = top + hh + 4 * rh
    sh = pg.new_shape()
    sh.draw_rect(pymupdf.Rect(L, top, R, top + hh))
    sh.finish(color=None, fill=(0.88, 0.88, 0.88), width=0)
    sh.draw_rect(pymupdf.Rect(L, top, R, bottom))
    for k in range(4):
        yy = top + hh + k * rh
        sh.draw_line((L, yy), (R, yy))
    for cx in cols[1:-1]:
        sh.draw_line((cx, top), (cx, bottom))
    sh.finish(color=(0, 0, 0), width=0.8)
    sh.commit()
    heads = [AR["col_no"], AR["col_name"], AR["col_nat"], AR["col_pct"], AR["col_dir"]]
    for c, h in enumerate(heads):
        ar_line(pg, h, cols[c] - 7, top + 16.5, 12, bold=True)
    for r, num in enumerate(AR["rows"]):
        ar_line(pg, num, cols[0] - 16, top + hh + r * rh + 15, 12)
    y = bottom + 30
    # signature fields, Arabic label at right and English label at left (as on Form 4-C)
    sh = pg.new_shape()
    sh.draw_line((L + 2, y - 8), (R - 8, y - 7))
    fields = [("f_member", "Name of consortium member"), ("f_cr", "Commercial registration number"),
              ("f_signatory", "Name of authorised signatory"), ("f_capacity", "Capacity"),
              ("f_date", "Date"), ("f_sign", "Signature and company seal")]
    for key, en in fields:
        pg.insert_text((L + 2, y + 9), en, fontname="tiro", fontsize=11, color=(0.2, 0.2, 0.2))
        ar_line(pg, AR[key], RX, y + 14, 13)
        sh.draw_line((L + 2, y + 22), (R - 8, y + 23))
        y += 30
    sh.finish(color=(0.15, 0.15, 0.15), width=0.7)
    sh.commit()
    y += 20
    ar_line(pg, AR["note_1"], RX - 4, y, 12)
    ar_line(pg, AR["note_2"], RX - 4, y + 18, 12)
    pg.insert_text((L - 2, y + 46), "FICTIONAL DOCUMENT - Lamar Holding internal assessment pack - not a real tender.",
                   fontname="tiro", fontsize=8.5, color=(0.45, 0.45, 0.45))
    if y + 50 > H - 30:
        raise SystemExit("form overflows")
    return doc


def form_4h_image():
    """Rotate slightly, rasterise at 200 dpi, add scan speckle; returns raw RGB bytes."""
    master = form_4h_page()
    scan = pymupdf.open()
    sp = scan.new_page(width=PAGE_W, height=PAGE_H)
    sp.show_pdf_page(sp.rect, master, 0, rotate=-0.35)
    z = 200.0 / 72.0
    pix = sp.get_pixmap(matrix=pymupdf.Matrix(z, z), alpha=False, colorspace=pymupdf.csRGB)
    if (pix.width, pix.height) != (IMG_PX_W, IMG_PX_H):
        raise SystemExit("unexpected raster size %dx%d" % (pix.width, pix.height))
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3).astype(np.int16)
    gray = a.mean(axis=2, keepdims=True)
    a = np.repeat(gray, 3, axis=2)
    rng = np.random.default_rng(IMG_SEED)
    # sparse grey speckle on white paper, matching the Volume II / IV scans (about 0.5% of
    # the blank area, grey levels 141-235)
    speck = rng.random((pix.height, pix.width)) < 0.0055
    tone = rng.integers(141, 236, size=(pix.height, pix.width), dtype=np.int16)
    a[speck] = np.minimum(a[speck], tone[speck][:, None])
    a = np.clip(a, 0, 255).astype(np.uint8)
    return a.tobytes()


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
    for pno, (chunks, img) in enumerate(pages, start=1):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        stream = furniture(header_left, pno) + "\n" + "\n".join(chunks) + "\n"
        cx = doc.get_new_xref()
        doc.update_object(cx, "<<>>")
        doc.update_stream(cx, stream.encode("latin-1"))
        doc.xref_set_key(page.xref, "Contents", "%d 0 R" % cx)
        res = "<</Font %d 0 R/ProcSet[/PDF/Text/ImageB/ImageC/ImageI]" % fd
        if img:
            res += "/XObject<</%s %d 0 R>>" % (img, ix)
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
ISSUE = dt.date(2026, 11, 9)
ADD02 = dt.date(2026, 10, 22)
PDD = dt.date(2026, 11, 26)


def is_wd(d):
    return d.weekday() in (6, 0, 1, 2, 3)      # Sunday..Thursday; no public holiday Oct-Dec 2026


def wd_before(d, n):
    c = 0
    while c < n:
        d -= dt.timedelta(days=1)
        if is_wd(d):
            c += 1
    return d


def wd_after(d, n):
    c = 0
    while c < n:
        d += dt.timedelta(days=1)
        if is_wd(d):
            c += 1
    return d


def long_date(d):
    return "%s %d %s %d" % (d.strftime("%A"), d.day, d.strftime("%B"), d.year)


DATES = {
    "issue": ISSUE,
    "clarification_cutoff": wd_before(PDD, 10),
    "grid_notice_deadline": wd_before(PDD, 10),
    "form_4h_foreign_deadline": wd_after(PDD, 5),
    "register_window_start": PDD - dt.timedelta(days=30),
}
assert ADD02 < ISSUE < DATES["grid_notice_deadline"] < PDD
assert DATES["grid_notice_deadline"] == dt.date(2026, 11, 12)
assert DATES["form_4h_foreign_deadline"] == dt.date(2026, 12, 3)
assert DATES["register_window_start"] == dt.date(2026, 10, 27)
assert is_wd(ISSUE) and is_wd(PDD)


# --------------------------------------------------------------------------
# Content of Addendum No. 3
# --------------------------------------------------------------------------
LQ, RQ = "‘", "’"


def q(s, bold=False):
    return LQ + ("<b>%s</b>" % s if bold else s) + RQ


COVER_SUMMARY = (
    "This Addendum amends the definition of Estimated Project Cost, the financial capacity requirement in "
    "Volume I Clause 8.4 and the delay liquidated damages in Volume V Clause 18.1, relaxes the velocity limit "
    "for the treated effluent transmission main, amends Section 5.1 of Addendum No. 1, reissues the technical "
    "evaluation table to add a criterion for energy efficiency, divides Volume I Clause 11.3 into two Clauses, "
    "makes a conditional amendment to Volume II Clause 1.4, adds a Declaration of Beneficial Ownership (Form "
    "4-H) which all Bidders may submit through the Portal within five Working Days after the Proposal Due "
    "Date, and responds to clarification requests 15 to 20.")

TR_FIRST = ("First: that the natural persons listed in the table below are all of the beneficial owners of the "
            "member, a beneficial owner being each natural person who owns, directly or indirectly, twenty-five "
            "per cent (25%) or more of the capital of the member or of the voting rights in it, or who controls "
            "the member by any other means.")


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

    # 2 -------------------------------------------------------------------
    F.append(Para("head", "2. DEFINITION OF ESTIMATED PROJECT COST"))
    F.append(Para("prov", "In Volume V Clause 1.3, %s is deleted and %s is substituted."
                  % (q("as set out in the agreed Financial Model at Financial Close"),
                     q("as stated by the Bidder in Form 4-F, excluding financing costs, interest during "
                       "construction and development fees", True)), "2.1"))
    F.append(Para("prov", "The definition in Volume V Clause 1.3, as amended by Section 2.1, applies wherever the "
                          "expression Estimated Project Cost is used in the RFP Documents.", "2.2"))

    # 3 -------------------------------------------------------------------
    F.append(Para("head", "3. AMENDMENT TO VOLUME I CLAUSE 8.4"))
    F.append(Para("prov", "In Volume I Clause 8.4, %s is deleted and %s is substituted. Limb (b) of Clause 8.4 "
                          "is unchanged."
                  % (q("SAR 800,000,000"), q("twenty-five per cent (25%) of the Estimated Project Cost", True)),
                  "3.1"))

    # 4 -------------------------------------------------------------------
    F.append(Para("head", "4. AMENDMENT TO VOLUME V CLAUSE 18.1"))
    F.append(Para("prov", "In Volume V Clause 18.1, %s is deleted and %s is substituted. Volume V Clause 18.4 is "
                          "unchanged."
                  % (q("SAR 180,000 for each day of delay"),
                     q("one-twentieth of one per cent (0.05%) of the Estimated Project Cost for each day of "
                       "delay", True)), "4.1"))

    # 5 -------------------------------------------------------------------
    F.append(Para("head", "5. TREATED EFFLUENT TRANSMISSION MAIN"))
    F.append(Para("prov", "In Volume II Clause 5.2, %s is deleted and %s is substituted. The minimum residual "
                          "head of 15 m at the delivery point is unchanged."
                  % (q("2.0 m/s"), q("1.5 m/s", True)), "5.1"))
    F.append(Para("prov", "With effect from 8 October 2026, Section 5.1 of Addendum No. 1 is amended by deleting "
                          "%s and substituting %s."
                  % (q("for the buried sections of the transmission main"),
                     q("for the buried sections of the transmission main other than the trenchless crossings "
                       "required by Volume II Clause 5.4, at which ductile iron only shall be used", True)),
                  "5.2"))

    # 6 -------------------------------------------------------------------
    F.append(Para("head", "6. TECHNICAL EVALUATION"))
    F.append(Para("prov", "Table 1-1 (revised) and the Notes to it, issued by Section 3 of Addendum No. 2, are "
                          "deleted and replaced by the table and Notes below, which add criterion G (energy "
                          "efficiency). The marks for criteria A to F are unchanged.", "6.1"))
    F.append(Para("ttitle", "Table 1-1 (second revision) — Technical evaluation criteria"))
    F.append(EvalTable([
        ["A", "Process design, treatment performance and compliance with Volume II", "25"],
        ["B", "Construction methodology, programme and interface management", "15"],
        ["C", "Operations and maintenance philosophy and lifecycle strategy", "20"],
        ["D", "Environmental and social management", "20"],
        ["E", "Organisation, key personnel and consortium governance", "10"],
        ["F", "Health, safety and security of supply", "10"],
        ["G", "Energy efficiency and specific energy consumption", "20"],
        ["", "<b>Total</b>", "<b>120</b>"],
    ]))
    F.append(NoteRule())
    F.append(Para("notehdr", "Notes to Table 1-1 (second revision):"))
    F.append(Para("note", "The technical score threshold in Volume I Clause 11.3 is unchanged at seventy per cent "
                          "(70%).", "(1)"))
    F.append(Para("note", "The combined score weighting stated in Volume I Clause 11.2 is amended to seventy per "
                          "cent (70%) technical and thirty per cent (30%) commercial.", "(2)"))
    F.append(Para("note", "Marks are awarded on the Authority's standard five-point scale and multiplied by the "
                          "weight shown.", "(3)"))
    F.append(Para("note", "Criterion G is assessed on the Energy Performance Statement, which shall be included in "
                          "the Technical Proposal in the format at Appendix C to this Addendum.", "(4)"))
    F.append(Para("prov", "Volume I Clause 11.3 is deleted and replaced by the following two Clauses:", "6.2",
                  keep_next=True))
    F.append(Para("quote", "A Proposal whose technical score is less than seventy per cent (70%) of the total marks "
                           "available in Table 1-1 shall not proceed to commercial evaluation." + RQ, "11.3"))
    F.append(Para("quote", "The Envelope B of a Proposal that does not proceed to commercial evaluation shall be "
                           "retained unopened by the Authority and returned to the Bidder after the Preferred "
                           "Bidder Notification." + RQ, "11.3A"))

    # 7 -------------------------------------------------------------------
    F.append(Para("head", "7. CONDITIONAL AMENDMENT TO VOLUME II CLAUSE 1.4"))
    F.append(Para("prov", "This Section 7 has effect only if the Authority notifies Bidders through the Portal, "
                          "not later than ten (10) Working Days before the Proposal Due Date, that the grid "
                          "connection point referred to in Volume II Clause 1.4 will not be energised at least "
                          "twelve (12) months before the Scheduled PCOD. If no such notice is given by that time, "
                          "this Section 7 lapses.", "7.1"))
    F.append(Para("prov", "Where this Section 7 has effect: (a) in Volume II Clause 1.4, the words %s, and the "
                          "comma before them, are deleted; (b) the grid connection is a utility to be procured by "
                          "the Project Company under the second sentence of Volume II Clause 1.4; and (c) the cost "
                          "of the grid connection works forms part of the Estimated Project Cost."
                  % q("together with a grid connection point at the site boundary"), "7.2"))

    # 8 -------------------------------------------------------------------
    F.append(Para("head", "8. NEW FORM 4-H — DECLARATION OF BENEFICIAL OWNERSHIP"))
    F.append(Para("prov", "A new Form 4-H (Declaration of Beneficial Ownership) is added to Volume IV and to the "
                          "list at Volume I Clause 9.1, to be inserted after Form 4-G. Form 4-H is reproduced at "
                          "Appendix A to this Addendum.", "8.1"))
    F.append(Para("prov", "Form 4-H shall be completed in the Arabic language, signed and stamped by an authorised "
                          "signatory of each member of the Bidder. The Arabic text governs. The English translation "
                          "at Appendix B is provided for convenience only.", "8.2"))
    F.append(Para("prov", "Form 4-H shall be submitted with Envelope A. A member of the Bidder that is incorporated "
                          "outside the Kingdom may instead submit its Form 4-H through the Portal not later than "
                          "five (5) Working Days after the Proposal Due Date.", "8.3"))
    F.append(Para("prov", "Failure to submit a complete and properly executed Form 4-H for each member of the "
                          "Bidder by the time required by Section 8.3 shall render the Proposal non-responsive.",
                  "8.4"))

    # 9 -------------------------------------------------------------------
    F.append(Para("head", "9. RESPONSES TO CLARIFICATION REQUESTS 15 TO 20"))
    F.append(QATable([
        ["15",
         "Volume I Clause 8.7 requires a Parent Company Guarantee that is unconditional as to the EPC "
         "Contractor's obligations during the construction period. Will the Authority accept a guarantee "
         "limited to a fixed amount?",
         "No. The Parent Company Guarantee shall be unlimited as to the guaranteed obligations and shall not be "
         "conditional on any demand first being made of the EPC Contractor. Volume I Clause 8.7 and Form 4-D "
         "apply."],
        ["16",
         "Does the Estimated Project Cost to be stated in Form 4-F include the cost of the grid connection works?",
         "Only if Section 7 of this Addendum has effect. Otherwise the grid connection point is provided by the "
         "Authority in accordance with Volume II Clause 1.4."],
        ["17",
         "Will the Authority publish the reference specific energy consumption against which criterion G of "
         "Table 1-1 will be assessed?",
         "The reference specific energy consumption, in kWh per cubic metre of treated effluent, is stated in "
         "Appendix C to this Addendum together with the format of the Energy Performance Statement."],
        ["18",
         "Does the maximum velocity in Volume II Clause 5.2 apply to the trenchless crossings?",
         "Yes. Volume II Clause 5.2, as amended by Section 5.1 of this Addendum, applies to the whole length of "
         "the transmission main, including the crossings required by Volume II Clause 5.4."],
        ["19",
         "How is compliance with Volume I Clause 8.4(a), as amended, to be demonstrated in Envelope A, given "
         "that the Estimated Project Cost is stated only in Form 4-F?",
         "The Authority notes the question. Volume I Clauses 6.2 and 11.1 apply. The Authority does not consider "
         "further amendment necessary at this stage."],
        ["20",
         "Must the certified copy of the register of shareholders attached to Form 4-H be legalised where the "
         "member is incorporated outside the Kingdom?",
         "No. Legalisation is not required for the purposes of Form 4-H."],
    ]))

    # Appendix A ----------------------------------------------------------
    F.append(Para("head", "APPENDIX A — FORM 4-H (ARABIC)"))
    F.append(Para("body", "Form 4-H is reproduced on the following page as issued. It shall be completed in the "
                          "Arabic language in accordance with Section 8 of this Addendum."))
    F.append(ImagePage(IMAGE_NAME))

    # Appendix B ----------------------------------------------------------
    F.append(Para("head", "APPENDIX B — ENGLISH TRANSLATION OF FORM 4-H"))
    F.append(Para("body", "This translation is provided for convenience only. The Arabic text of Form 4-H at "
                          "Appendix A governs."))
    F.append(Para("formtitle", "FORM 4-H — DECLARATION OF BENEFICIAL OWNERSHIP"))
    F.append(Para("body", "We, the undersigned, as the authorised representatives of the member of the Bidder's "
                          "consortium named below, declare and undertake as follows:"))
    F.append(Para("body", TR_FIRST))
    F.append(Para("body", "Second: that none of the beneficial owners owns, directly or indirectly, any interest "
                          "in a member of another consortium submitting a Proposal for this tender."))
    F.append(Para("body", "Third: that we have attached to this declaration a certified copy of the register of "
                          "partners or shareholders of the member, issued within the thirty (30) days preceding "
                          "the date for submission of Proposals."))
    F.append(OwnerTable([["1", "", "", "", ""], ["2", "", "", "", ""], ["3", "", "", "", ""],
                         ["4", "", "", "", ""]]))
    F.append(Para("body", "Name of consortium member: _______________________ Commercial registration number: "
                          "_______________ Name of authorised signatory: _______________________ Capacity: "
                          "_______________ Date: ____________ Signature and company seal: _______________"))
    F.append(Para("body", "Note: This Form shall be submitted in the Arabic language for each member of the "
                          "consortium, and the Arabic text governs. Failure to submit it complete renders the "
                          "Proposal non-responsive."))
    return F


IMAGE_RAW = None
IMAGE_NAME = None
META = {"title": "(anonymous)", "author": "(anonymous)", "subject": "(unspecified)",
        "creator": "(unspecified)", "keywords": "", "producer": "ReportLab PDF Library - (opensource)",
        "creationDate": "D:20261109102501+00'00'", "modDate": "D:20261109102501+00'00'"}
DOC_ID = hashlib.md5(b"NUPA/ISTP/2026/014 Addendum No. 3 issued 9 November 2026").hexdigest().upper()


# --------------------------------------------------------------------------
# Optional consistency check against the issued pack (old quotations verbatim)
# --------------------------------------------------------------------------
OLD_QUOTES = [
    ("VOL-V_Draft_Project_Agreement.pdf", "Estimated Project Cost means the aggregate capital cost of the Facility "
     "as set out in the agreed Financial Model at Financial Close."),
    ("VOL-I_Instructions_to_Bidders.pdf", "(a) a consolidated tangible net worth of not less than SAR 800,000,000 "
     "as at the most recent audited financial statements"),
    ("VOL-V_Draft_Project_Agreement.pdf", "delay liquidated damages at the rate of SAR 180,000 for each day of delay."),
    ("VOL-V_Draft_Project_Agreement.pdf", "The aggregate liability of the Project Company for delay liquidated "
     "damages under this Clause 18 shall not exceed ten per cent (10%) of the Estimated Project Cost."),
    ("VOL-II_Technical_Requirements.pdf", "The main shall be sized for the peak hourly flow in Table 2-6 with a "
     "maximum velocity of 2.0 m/s and a minimum residual head of 15 m at the delivery point."),
    ("VOL-II_Technical_Requirements.pdf", "with a minimum nominal diameter of DN1200"),
    ("ADD-01_Addendum_No_1.pdf", "‘Glass reinforced plastic pipe of an equivalent pressure class is acceptable for "
     "the buried sections of the transmission main, subject to the whole-life cost comparison required by this "
     "Clause.’"),
    ("ADD-01_Addendum_No_1.pdf", "Issued 8 October 2026"),
    ("VOL-I_Instructions_to_Bidders.pdf", "A Proposal scoring less than seventy (70) marks out of one hundred (100) "
     "at the technical evaluation shall not proceed to commercial evaluation and its Envelope B shall be returned "
     "unopened."),
    ("ADD-02_Addendum_No_2.pdf", "The technical score threshold in Volume I Clause 11.3 is unchanged at seventy "
     "(70) marks."),
    ("ADD-02_Addendum_No_2.pdf", "The combined score weighting stated in Volume I Clause 11.2 is amended to "
     "sixty-five per cent (65%) technical and thirty-five per cent (35%) commercial."),
    ("ADD-02_Addendum_No_2.pdf", "Marks are awarded on the Authority's standard five-point scale and multiplied by "
     "the weight shown."),
    ("VOL-II_Technical_Requirements.pdf", "The Authority will provide the site free of encumbrance, together with a "
     "grid connection point at the site boundary. All other utilities shall be procured by the Project Company."),
    ("VOL-I_Instructions_to_Bidders.pdf", "The appearance of any price, rate, or other commercial information "
     "within Envelope A shall render the Proposal non-responsive."),
    ("VOL-IV_Form_Sheets.pdf", "Estimated Project Cost (SAR)"),
    ("VOL-IV_Form_Sheets.pdf", "Unlimited as to the guaranteed obligations"),
    ("VOL-IV_Form_Sheets.pdf", "This guarantee is not conditional on any demand first being made of the EPC "
     "Contractor."),
    ("ADD-02_Addendum_No_2.pdf", "A new Form 4-G is added to Volume IV and to the list at Volume I Clause 9.1, to be "
     "inserted after item (e)."),
    ("ADD-01_Addendum_No_1.pdf", "‘the weighting is expected to remain at the customary seventy / thirty split used "
     "on comparable projects’"),
    ("VOL-V_Draft_Project_Agreement.pdf", "The Project Company shall achieve PCOD within thirty-six (36) months of "
     "the Notice to Proceed (the Scheduled PCOD)."),
    ("VOL-II_Technical_Requirements.pdf", "Three (3) road crossings and one (1) wadi crossing shall be executed by "
     "trenchless methods."),
    ("VOL-I_Instructions_to_Bidders.pdf", "No firm, and no affiliate of a firm, shall participate in more than one "
     "Proposal."),
]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def check(pack_dir):
    texts = {}
    for fn, quote in OLD_QUOTES:
        if fn not in texts:
            d = pymupdf.open(pack_dir.rstrip("/") + "/" + fn)
            texts[fn] = norm(" ".join(p.get_text() for p in d))
        if norm(quote) not in texts[fn]:
            raise SystemExit("NOT VERBATIM in %s: %s" % (fn, quote))
    print("verbatim: %d quotations OK" % len(OLD_QUOTES))
    for k, v in DATES.items():
        print("date %-26s %s" % (k, long_date(v)))
    q_peak = 7500 / 3600.0
    for v in (2.0, 1.5):
        print("velocity %.1f m/s -> minimum bore %.3f m" % (v, math.sqrt(4 * q_peak / (math.pi * v))))
    print("DN1200 velocity at peak: %.3f m/s" % (q_peak / (math.pi * 0.6 ** 2)))
    print("LD cap reached after %d days" % round(0.10 / 0.0005))
    print("threshold %.1f marks of 120" % (0.70 * 120))


def main():
    global IMAGE_RAW, IMAGE_NAME
    for name, want in PINNED_FONTS.items():
        got = hashlib.sha256(open(FREEFONT + name, "rb").read()).hexdigest()
        if got != want:
            raise SystemExit("unexpected %s; output would not be reproducible" % name)
    if pymupdf.VersionBind != PINNED_VERSIONS["pymupdf"] or np.__version__ != PINNED_VERSIONS["numpy"]:
        raise SystemExit("pinned versions: %r" % PINNED_VERSIONS)
    out = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "ADD-03_Addendum_No_3.pdf"
    if "--check" in sys.argv:
        check(sys.argv[sys.argv.index("--check") + 1])
    IMAGE_RAW = form_4h_image()
    IMAGE_NAME = "FormXob." + hashlib.md5(IMAGE_RAW).hexdigest()
    n = build_pdf(addendum3(), "Addendum No. 3", out, META, IMAGE_RAW, IMAGE_NAME, DOC_ID)
    print("pages:", n)


if __name__ == "__main__":
    main()
