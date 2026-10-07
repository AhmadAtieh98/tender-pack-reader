#!/usr/bin/env python3
"""Builder for the blind rehearsal 07 input:

  ADD-03_Addendum_No_3.pdf  (stands on the base pack as amended by Addenda Nos. 1 and 2 only)

Drawn in the page furniture and typography of the issued Addenda Nos. 1 and 2: A4, Base-14
Type1 fonts (Helvetica, Helvetica-Bold, Times-Roman, Times-Bold, WinAnsiEncoding, not
embedded) for every text-layer glyph, the ADD-01/ADD-02 watermark, header, footer and rules,
the ADD-01/ADD-02 clarification grid and table styling, and ReportLab-style metadata.  There
is no Arabic code point in the text layer.

Appendix A carries one IMAGE-ONLY element (Table 42-1, Arabic), drawn the way Volume II draws
its Table 2-4 reproduction: a partial-page "scanned" raster 1750 px across, RGB with equal
channels, FlateDecode, placed at the frame's left edge over the full frame width directly
below an introductory paragraph.  The Arabic is shaped by MuPDF's HTML engine (HarfBuzz) in
GNU FreeSerif; the vector master is rotated slightly, rasterised, toned to the pack's paper
grey and speckled with a fixed-seed numpy generator.

The layout engine, furniture, Arabic line shaper and raster pipeline are adapted from the
blind-06 builder (technique example).  The content is new.

Output is byte-for-byte deterministic (fixed dates, fixed /ID, fixed seed, pinned library
versions and font files).

Usage:
  python build_addendum.py <ADD-03 output.pdf> [--check <candidate_pack_dir>]
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
IMG_PX_W, IMG_PX_H = 1750, 1700
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
        j, kk, cf = i, k, fl                  # keep-with-next, chained (heading -> intro -> quote)
        while (kk in ("head", "ttitle", "notehdr") or getattr(cf, "keep_next", False)) \
                and j + 1 < len(flowables):
            nx = flowables[j + 1]
            need += gap(kk, kind_of(nx)) + first_height(nx)
            if isinstance(nx, Grid) or kind_of(nx) == "break":
                break
            j, kk, cf = j + 1, kind_of(nx), nx
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
# The "scanned" Arabic Table 42-1 (Addendum No. 3, Appendix A): shaping helpers
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
LETTER = dt.date(2026, 11, 15)                  # Asset Transfer Committee letter No. 417/2026 (Table 42-1)
ISSUE = dt.date(2026, 11, 17)                   # Addendum No. 3 issue date (after the 5.2 cut-off)


def is_wd(d):
    # Volume I Clause 2.4: Sunday..Thursday, other than a public holiday in the Kingdom.
    # Assumption (not stated by the pack): no public holiday in the Kingdom falls in Oct-Dec 2026.
    return d.weekday() in (6, 0, 1, 2, 3)


def wd_before(d, n):
    """Volume I Clause 2.4: counting backwards, the stated date itself is not counted."""
    c = 0
    while c < n:
        d -= dt.timedelta(days=1)
        if is_wd(d):
            c += 1
    return d


def wd_after_excl(d, n):
    """Counting forwards, start day NOT counted (mirror of Clause 2.4; the pack states no forward rule)."""
    c = 0
    while c < n:
        d += dt.timedelta(days=1)
        if is_wd(d):
            c += 1
    return d


def wd_after_incl(d, n):
    """Counting forwards, start day counted as day 1 if it is a Working Day (the other reading)."""
    c = 1 if is_wd(d) else 0
    while c < n:
        d += dt.timedelta(days=1)
        if is_wd(d):
            c += 1
    return d


def wd_between(a, b):
    """Working Days from a (inclusive) to b (exclusive)."""
    n, x = 0, a
    while x < b:
        if is_wd(x):
            n += 1
        x += dt.timedelta(days=1)
    return n


def long_date(d):
    return "%s %d %s %d" % (d.strftime("%A"), d.day, d.strftime("%B"), d.year)


DATES = {
    "add03_issue": ISSUE,
    "table_42_1_letter": LETTER,
    "clarification_cutoff_vol1_5_2": wd_before(PDD, 10),
    "core_appointment_latest_s4_3_3wd_before_pdd": wd_before(PDD, 3),
    "core_request_deadline_s4_3_excl_reading": wd_after_excl(ISSUE, 3),
    "core_request_deadline_s4_3_incl_reading": wd_after_incl(ISSUE, 3),
    "proposal_due_date": PDD,
}
assert ADD02 < LETTER < ISSUE < PDD
assert all(is_wd(d) for d in (LETTER, ISSUE, PDD))
assert DATES["clarification_cutoff_vol1_5_2"] == dt.date(2026, 11, 12)
assert DATES["clarification_cutoff_vol1_5_2"] < ISSUE              # issued AFTER the cut-off (deliberate)
assert DATES["core_appointment_latest_s4_3_3wd_before_pdd"] == dt.date(2026, 11, 23)
assert DATES["core_request_deadline_s4_3_excl_reading"] == dt.date(2026, 11, 22)
assert DATES["core_request_deadline_s4_3_incl_reading"] == dt.date(2026, 11, 19)
assert DATES["core_request_deadline_s4_3_excl_reading"] < DATES["core_appointment_latest_s4_3_3wd_before_pdd"]
assert wd_between(ISSUE, PDD) == 7

# Figures derived from the text (asserted; printed by --check)
CIL_BASE, CIL_ADD02, CIL_DELTA = 5_000_000, 2_500_000, 1_000_000
CIL_NOW = CIL_ADD02 - CIL_DELTA
CIL_COVER_WRONG = CIL_BASE - CIL_DELTA                 # cover error E1 (stale base)
assert (CIL_NOW, CIL_COVER_WRONG) == (1_500_000, 4_000_000)


# --------------------------------------------------------------------------
# Arabic source strings of Table 42-1 (the governing text).  Keys are referenced by the
# answer key.  Discrepancies against the English convenience translation (Appendix B) are
# deliberate: AR1 (row 4, electrical/I&C: 7 years in Arabic, 5 in English), AR2 (row 5,
# membranes: 24 MONTHS in Arabic, "24" under a years heading in English) and AR3 (English
# note (4) has no Arabic counterpart).
# --------------------------------------------------------------------------
AR = {
    "issuer": "الهيئة الشمالية للمشتريات المرفقية",
    "committee": "لجنة نقل الأصول",
    "ref": "الرقم: ٤١٧/٢٠٢٦",
    "date": "التاريخ: ١٥ نوفمبر ٢٠٢٦م",
    "subject": "الموضوع: متطلبات حالة الأصول عند نقل محطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان",
    "tender": "مناقصة رقم: NUPA/ISTP/2026/014",
    "title": "جدول ٤٢-١: الحد الأدنى للعمر المتبقي للأصول عند النقل",
    "intro": "يجب ألا يقل العمر المتبقي لكل فئة من فئات الأصول في تاريخ نقل المرفق إلى الهيئة عمّا هو مبيَّن أدناه:",
    "h_no": "م",
    "h_cls": "فئة الأصول",
    "h_life": "الحد الأدنى للعمر المتبقي (سنة)",
    "h_grade": "أقصى درجة للحالة",
    "no1": "١", "no2": "٢", "no3": "٣", "no4": "٤", "no5": "٥",
    "c1": "المنشآت المدنية والخرسانية",
    "c2": "خط نقل المياه المعالجة",
    "c3": "المعدات الميكانيكية",
    "c4": "المعدات الكهربائية وأجهزة القياس والتحكم",
    "c5": "الأغشية (إن وُجدت)",
    "l1": "٢٠", "l2": "٢٠", "l3": "٥", "l4": "٧", "l5": "٢٤ شهراً",
    "g1": "٢", "g2": "٢", "g3": "٣", "g4": "٣", "g5": "٣",
    "notes": "ملاحظات:",
    "n1": "١. تُقيَّم درجة الحالة وفق مقياس الهيئة لتصنيف حالة الأصول المكوَّن من خمس درجات، وتعني الدرجة ١ أن الأصل بحالة جديدة.",
    "n2": "٢. يحدِّد المهندس المستقل العمر المتبقي لكل أصل في مسح الحالة الذي يُجرى قبل النقل.",
    "n3": "٣. يُستبدَل على نفقة شركة المشروع قبل تاريخ النقل كلُّ أصل لا يستوفي متطلبات هذا الجدول.",
    "sign": "رئيس لجنة نقل الأصول",
}
AR_LINES = {
    "h_life": ["الحد الأدنى للعمر", "المتبقي (سنة)"],
    "h_grade": ["أقصى درجة", "للحالة"],
}
for _k, _lines in AR_LINES.items():
    assert " ".join(_lines) == AR[_k], _k


def table_42_1_master():
    """Vector master of the reproduced table (points; 1750 px across when rasterised)."""
    W, H = IMG_W, IMG_H
    doc = pymupdf.open()
    pg = doc.new_page(width=W, height=H)
    L, R = 16.0, W - 16.0
    RX = R - 2.0

    def line(text, x_right, baseline, size, bold=False):
        w = ar_line(pg, text, x_right, baseline, size, bold)
        if x_right - w < L:
            raise SystemExit("Arabic line wider than the sheet: %s" % text)
        return w

    line(AR["issuer"], RX, 24, 13, bold=True)
    line(AR["committee"], RX, 40, 10.5, bold=True)
    pg.insert_text((L + 2, 22), "Northern Utilities Procurement Authority - Asset Transfer Committee",
                   fontname="tiro", fontsize=8, color=(0.3, 0.3, 0.3))
    line(AR["ref"], RX, 56, 9.5)
    line(AR["date"], RX - 140, 56, 9.5)
    sh = pg.new_shape()
    sh.draw_line((L, 64), (R, 64))
    sh.finish(color=(0, 0, 0), width=0.9)
    sh.commit()
    line(AR["subject"], RX, 81, 9.6)
    line(AR["tender"], RX, 96, 9.6)
    line(AR["title"], RX, 120, 12.5, bold=True)
    line(AR["intro"], RX, 139, 9.8)
    # table, columns from right to left: no | asset class | minimum residual life | maximum grade
    cols = [R, R - 40, R - 250, R - 360, L]
    top = 150.0
    hh, rh = 38.0, 25.0
    bottom = top + hh + 5 * rh
    sh = pg.new_shape()
    sh.draw_rect(pymupdf.Rect(L, top, R, top + hh))
    sh.finish(color=None, fill=(0.88, 0.88, 0.88), width=0)
    sh.draw_rect(pymupdf.Rect(L, top, R, bottom))
    for r in range(5):
        sh.draw_line((L, top + hh + r * rh), (R, top + hh + r * rh))
    for cx in cols[1:-1]:
        sh.draw_line((cx, top), (cx, bottom))
    sh.finish(color=(0, 0, 0), width=0.8)
    sh.commit()
    pad = 5.0

    def cell(text, ci, baseline, size, bold=False, inset=0.0):
        xr = cols[ci] - pad - inset
        w = ar_line(pg, text, xr, baseline, size, bold)
        if xr - w < cols[ci + 1] + 3.0:
            raise SystemExit("Arabic cell text does not fit: %s" % text)

    heads = ["h_no", "h_cls", "h_life", "h_grade"]
    for ci, key in enumerate(heads):
        if key in AR_LINES:
            cell(AR_LINES[key][0], ci, top + 16, 9.6, True)
            cell(AR_LINES[key][1], ci, top + 31, 9.6, True)
        else:
            cell(AR[key], ci, top + 23, 9.6, True, inset=(10 if ci == 0 else 0))
    for r in range(5):
        s = str(r + 1)
        y0 = top + hh + r * rh
        cell(AR["no" + s], 0, y0 + 17, 10, inset=12)
        cell(AR["c" + s], 1, y0 + 17, 9.8)
        cell(AR["l" + s], 2, y0 + 17, 10.5, inset=(30 if s != "5" else 18))
        cell(AR["g" + s], 3, y0 + 17, 10.5, inset=36)
    y = bottom + 22
    line(AR["notes"], RX, y, 10, bold=True)
    for key in ("n1", "n2", "n3"):
        y += 17
        line(AR[key], RX - 4, y, 9.4)
    y += 36
    line(AR["sign"], L + 150, y, 10.5, bold=True)
    sh = pg.new_shape()
    sh.draw_bezier((L + 20, y + 18), (L + 44, y - 2), (L + 62, y + 26), (L + 92, y + 6))
    sh.finish(color=(0.15, 0.15, 0.15), width=0.9)
    sh.draw_oval(pymupdf.Rect(L + 168, y - 20, L + 230, y + 22))
    sh.finish(color=(0.45, 0.45, 0.45), width=0.8)
    sh.commit()
    pg.insert_text((L + 2, H - 9), "FICTIONAL DOCUMENT - Lamar Holding internal assessment pack - "
                   "not a real tender.", fontname="tiro", fontsize=6.5, color=(0.45, 0.45, 0.45))
    if y + 30 > H - 14:
        raise SystemExit("table master overflows")
    return doc


def table_42_1_image():
    """Rotate slightly, rasterise at 1750 px across, tone to paper grey, speckle."""
    master = table_42_1_master()
    scan = pymupdf.open()
    sp = scan.new_page(width=IMG_W, height=IMG_H)
    sp.show_pdf_page(sp.rect, master, 0, rotate=-0.3)
    pix = sp.get_pixmap(matrix=pymupdf.Matrix(IMG_ZOOM, IMG_ZOOM), alpha=False,
                        colorspace=pymupdf.csRGB)
    if (pix.width, pix.height) != (IMG_PX_W, IMG_PX_H):
        raise SystemExit("unexpected raster size %dx%d" % (pix.width, pix.height))
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3).astype(np.int32)
    gray = (a.sum(axis=2) + 1) // 3
    gray = (gray * PAPER + 127) // 255
    rng = np.random.default_rng(IMG_SEED)
    speck = rng.random((pix.height, pix.width)) < 0.0085
    tone = rng.integers(141, 217, size=(pix.height, pix.width), dtype=np.int32)
    gray = np.where(speck, np.minimum(gray, tone), gray)
    g8 = np.clip(gray, 0, 255).astype(np.uint8)
    return np.repeat(g8[:, :, None], 3, axis=2).tobytes()


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

COVER = (
    "This Addendum reduces the threshold in Volume V Clause 36.2 for compensation for a General Change in Law "
    "to SAR 4,000,000, relocates the handback condition survey from Volume II to Volume V, replaces the "
    "remaining design life required at handback with minimum residual service lives for four asset classes set "
    "out in Table 42-1 (issued in Arabic), invites Bidders to describe in their Technical Proposals how their "
    "lifecycle plans address Table 42-1, inserts a new Volume V Clause 12.5 on adverse ground conditions and "
    "requires Bidders to state the ground conditions assumed for the design of foundations, provides for the "
    "inspection of borehole cores and laboratory records with a limited exception to Volume I Clause 4.2, and "
    "responds to clarification requests 15 to 19.")

R1_1 = ("This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in "
        "accordance with Volume I Clause 3.2.")
R1_2 = ("A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by "
        "Addenda Nos. 1 and 2, unless otherwise stated.")
R1_3 = "Clarification requests 15 to 19 were received before the time stated in Volume I Clause 5.2."

S2_1 = "The amount stated in Volume V Clause 36.2 is reduced by SAR 1,000,000."
S2_2 = "Bidders shall take Section 2.1 into account in the Availability Payment quoted in Form 4-F."

OLD_8_5 = ("A handback condition survey shall be carried out in the final two (2) years of the concession, and any "
           "remedial works identified shall be completed before transfer.")
S3_1 = ("Volume II Clause 8.5 is relocated to Volume V, in which it becomes Clause 42.3. Its text is unchanged "
        "and reads as follows:")
S3_1B = "The number 8.5 is not reused in Volume II, and the Clauses of Volume II are not renumbered."
OLD_42_1_REF = "Volume II Clause 8.5"
NEW_42_1_REF = "Clause 42.3"
OLD_42_1_LIFE = "with a remaining design life of not less than five (5) years for all major assets"
NEW_42_1_LIFE = "with a residual service life, for each asset class, of not less than that stated in Table 42-1"
S3_2 = "In Volume V Clause 42.1, %s is deleted and %s is substituted." % (q(OLD_42_1_REF), q(NEW_42_1_REF, True))
S3_3 = ("In Volume V Clause 42.1, %s is deleted and %s is substituted. Table 42-1 is reproduced at Appendix A to "
        "this Addendum and forms part of Volume V." % (q(OLD_42_1_LIFE), q(NEW_42_1_LIFE, True)))
S3_4 = ("Table 42-1 is issued in the Arabic language. The Arabic text governs. The English translation at "
        "Appendix B is provided for convenience only.")
S3_5 = ("The Bidder shall demonstrate in the Technical Proposal how its lifecycle plan achieves the residual "
        "service lives in Table 42-1.")

S4_1 = "The following new Clause 12.5 is inserted in Volume V after Clause 12.4:"
NEW_12_5 = ("If the Project Company encounters at the site ground conditions that are materially more adverse "
            "than those described in the Geotechnical Baseline Report, it shall be entitled to an extension of "
            "the Scheduled PCOD and to payment of its reasonable additional costs, provided that it notifies the "
            "Authority within five (5) Working Days of encountering them. In this Clause, the Geotechnical "
            "Baseline Report means Revision C of the report of that name issued by the Authority.")
S4_2 = ("Each Bidder shall state in the Technical Proposal the ground conditions assumed for the design of "
        "foundations, by reference to the Geotechnical Baseline Report.")
S4_3_REQ = "within three (3) Working Days of the date of this Addendum"
S4_3_APPT = "not later than three (3) Working Days before the Proposal Due Date"
S4_3 = ("A Bidder that wishes to inspect the borehole cores and laboratory records on which the Geotechnical "
        "Baseline Report is based shall request an appointment through the Portal %s. Appointments will be "
        "held at the Authority's core store in Sakaka %s." % (S4_3_REQ, S4_3_APPT))
S4_4 = ("Volume I Clause 4.2 does not apply to communications with the Authority's geotechnical consultant during "
        "an appointment under Section 4.3, to the extent that they concern the identification and handling of "
        "cores and records.")

QA = [
    ["15",
     "Will the minutes of the Pre-Bid Conference at Appendix B to Addendum No. 1 be issued in Arabic?",
     "No. The minutes are issued in English only. Section 3.2 of Addendum No. 1 continues to apply to them."],
    ["16",
     "At what stage must the grievance mechanism referred to in Volume II Clause 9.3 be in place?",
     "The grievance mechanism shall be established before construction, shall be accessible to the affected "
     "community and shall be maintained for the concession period. Volume II Clause 9.3 applies."],
    ["17",
     "Volume I Clause 10.1 states that no document other than Form 4-F and the Financial Model shall be placed in "
     "Envelope B, but Volume I Clause 10.6 requires a schedule of financing assumptions to be submitted with "
     "Form 4-F. Where is the schedule to be placed?",
     "The schedule required by Volume I Clause 10.6 forms part of Form 4-F and shall be attached to it in "
     "Envelope B. The schedule shall also state the minimum annual debt service cover ratio assumed. A schedule "
     "placed in Envelope A will be treated in accordance with Volume I Clause 6.2."],
    ["18",
     "Volume V Clause 39.5 refers to a Direct Agreement with the Senior Lenders. If the Direct Agreement provides "
     "for compensation on termination for Project Company default that differs from Volume V Clause 40.2, which "
     "prevails?",
     "The Authority notes the question. The order of precedence at Volume I Clause 3.2 applies. The Direct "
     "Agreement will be negotiated with the Senior Lenders after the Preferred Bidder Notification."],
    ["19",
     "May Bidders inspect the borehole cores and laboratory records from the site investigation?",
     "Yes, by appointment. Section 4.3 of this Addendum applies. Requests made after the period stated in that "
     "Section will not be accommodated."],
]

EN_TABLE = [
    ["1", "Civil and concrete structures", "20", "2"],
    ["2", "Treated effluent transmission main", "20", "2"],
    ["3", "Mechanical equipment", "5", "3"],
    ["4", "Electrical, instrumentation and control equipment", "5", "3"],
    ["5", "Membranes (where provided)", "24", "3"],
]
EN_NOTES = [
    ("(1)", "Condition grade is assessed on the Authority's five-point asset condition grading scale, grade 1 "
            "meaning as new."),
    ("(2)", "The Independent Engineer determines the residual service life of each asset in the condition survey "
            "carried out before transfer."),
    ("(3)", "Any asset that does not meet this Table shall be replaced at the Project Company's cost before the "
            "date of transfer."),
    ("(4)", "The design life of electrical equipment stated in Volume II Clause 2.2 is increased to twenty-five "
            "(25) years."),
]


class ResidualLifeTable(Grid):
    # ADD-02 Table 1-1 outer edges (70.86614 .. 524.4094), four columns
    COLS = [70.86614, 100.86614, 330.86614, 440.86614, 524.4094]

    def __init__(self, rows):
        super().__init__(self.COLS, ["No", "Asset class", "Minimum residual life (years)",
                                     "Maximum condition grade"], rows)


def addendum3(image_name):
    F = []
    F.append(Cover("3", issued(ISSUE), "Tender NUPA/ISTP/2026/014"))
    F.append(Para("proj", "Wadi Sirhan Independent Sewage Treatment Plant"))
    F.append(Para("body", COVER))
    F.append(Para("body", PRECEDENCE))

    F.append(Para("head", "1. RECITALS"))
    F.append(Para("prov", R1_1, "1.1"))
    F.append(Para("prov", R1_2, "1.2"))
    F.append(Para("prov", R1_3, "1.3"))

    F.append(Para("head", "2. CHANGE IN LAW"))
    F.append(Para("prov", S2_1, "2.1"))
    F.append(Para("prov", S2_2, "2.2"))

    F.append(Para("head", "3. HANDBACK"))
    F.append(Para("prov", S3_1, "3.1", keep_next=True))
    F.append(Para("quote", OLD_8_5 + RQ, "42.3"))
    F.append(Para("prov", S3_1B, "3.2"))
    F.append(Para("prov", S3_2, "3.3"))
    F.append(Para("prov", S3_3, "3.4"))
    F.append(Para("prov", S3_4, "3.5"))
    F.append(Para("prov", S3_5, "3.6"))

    F.append(Para("head", "4. GROUND CONDITIONS"))
    F.append(Para("prov", S4_1, "4.1", keep_next=True))
    F.append(Para("quote", NEW_12_5 + RQ, "12.5"))
    F.append(Para("prov", S4_2, "4.2"))
    F.append(Para("prov", S4_3, "4.3"))
    F.append(Para("prov", S4_4, "4.4"))

    F.append(Para("head", "5. RESPONSES TO CLARIFICATION REQUESTS 15 TO 19"))
    F.append(QATable(QA))

    F.append(PageBreak())
    F.append(Para("head", "APPENDIX A — TABLE 42-1 (ARABIC)"))
    F.append(Para("body", "The following table is reproduced as issued by the Authority's Asset Transfer Committee "
                          "under cover of its letter No. 417/2026 dated %d %s %d. The Arabic text governs in "
                          "accordance with Section 3.5 of this Addendum."
                  % (LETTER.day, LETTER.strftime("%B"), LETTER.year), keep_next=True))
    F.append(ImageBlock(image_name))
    F.append(Para("body", "End of reproduction."))

    F.append(PageBreak())
    F.append(Para("head", "APPENDIX B — ENGLISH TRANSLATION OF TABLE 42-1"))
    F.append(Para("body", "This translation is provided for convenience only. The Arabic text of Table 42-1 at "
                          "Appendix A governs. Asset Transfer Committee letter No. 417/2026 dated %d %s %d. "
                          "Subject: asset condition requirements on transfer of the Wadi Sirhan Independent "
                          "Sewage Treatment Plant. Tender No. NUPA/ISTP/2026/014."
                  % (LETTER.day, LETTER.strftime("%B"), LETTER.year)))
    F.append(Para("ttitle", "Table 42-1 — Minimum residual service life of assets at transfer"))
    F.append(Para("body", "The residual service life of each asset class at the date of transfer of the Facility "
                          "to the Authority shall be not less than stated below."))
    F.append(ResidualLifeTable(EN_TABLE))
    F.append(NoteRule())
    F.append(Para("notehdr", "Notes to Table 42-1:"))
    for num, txt in EN_NOTES:
        F.append(Para("note", txt, num))
    F.append(Para("body", "Signed: Chairman, Asset Transfer Committee, Northern Utilities Procurement Authority "
                          "(signature and stamp)."))
    return F


META = {"title": "(anonymous)", "author": "(anonymous)", "subject": "(unspecified)",
        "creator": "(unspecified)", "keywords": "", "producer": "ReportLab PDF Library - (opensource)",
        "creationDate": "D:20261117102501+00'00'", "modDate": "D:20261117102501+00'00'"}
DOC_ID = hashlib.md5(b"NUPA/ISTP/2026/014 Addendum No. 3 issued 17 November 2026 (blind-07)").hexdigest().upper()


# --------------------------------------------------------------------------
# Consistency check against the issued pack (old quotations and state_before verbatim)
# --------------------------------------------------------------------------
V1, V2, V4, V5 = ("VOL-I_Instructions_to_Bidders.pdf", "VOL-II_Technical_Requirements.pdf",
                  "VOL-IV_Form_Sheets.pdf", "VOL-V_Draft_Project_Agreement.pdf")
A1, A2 = "ADD-01_Addendum_No_1.pdf", "ADD-02_Addendum_No_2.pdf"

# "old" texts quoted or reproduced by Addendum No. 3; each must occur exactly once in its volume
OLD_ONCE = [
    (V2, OLD_8_5),
    (V5, OLD_42_1_REF),
    (V5, OLD_42_1_LIFE),
]

# state_before quotations used by the answer key (id, file, text)
STATE_BEFORE = [
    ("SB01", V5, "A General Change in Law entitles the Project Company to compensation only in respect of capital "
                 "expenditure required by that change and only to the extent that such expenditure exceeds SAR "
                 "5,000,000 in aggregate over the term."),
    ("SB02", A2, "In Volume V Clause 36.2, ‘SAR 5,000,000’ is deleted and ‘SAR 2,500,000’ is "
                 "substituted."),
    ("SB03", V2, OLD_8_5),
    ("SB04", V5, "The Project Company shall transfer the Facility to the Authority on expiry in the condition "
                 "required by Volume II Clause 8.5, free of encumbrance and with a remaining design life of not "
                 "less than five (5) years for all major assets."),
    ("SB05", V5, "A handback reserve shall be funded from the start of year twenty (20) of the term in an amount "
                 "certified by the Independent Engineer."),
    ("SB06", V2, "The design life of mechanical and electrical equipment shall be not less than twenty (20) years "
                 "or the manufacturer's rated life, whichever is the shorter, with lifecycle replacement provided "
                 "for in the Project Company's lifecycle plan."),
    ("SB07", V2, "Where a membrane process is proposed, the Project Company shall demonstrate membrane replacement "
                 "provisions in the lifecycle plan and shall warrant a membrane life of not less than seven (7) "
                 "years."),
    ("SB08", V2, "shall transfer the Facility to the Authority at the end of the concession period in the "
                 "condition required by Volume V."),
    ("SB09", V5, "This extract contains the clauses of the draft Project Agreement on which the Authority invites "
                 "comment through Form 4-E. Clause numbering follows the full draft; omitted clauses are not "
                 "reproduced. A deviation not listed in Form 4-E will be taken as accepted."),
    ("SB10", V1, "Form 4-E shall list every deviation, qualification or reservation to Volume V."),
    ("SB11", V4, "List every deviation, qualification or reservation to Volume V."),
    ("SB12", V1, "(a) the Addenda, a later Addendum prevailing over an earlier one; (b) Volume I (Instructions to "
                 "Bidders); (c) Volume V (Draft Project Agreement); (d) Volume II (Technical Requirements);"),
    ("SB13", V1, "The RFP Documents comprise: Volume I (Instructions to Bidders); Volume II (Technical "
                 "Requirements); Volume III (Drawings); Volume IV (Form Sheets); Volume V (Draft Project "
                 "Agreement); and every Addendum issued."),
    ("SB14", V5, "The Project Company shall achieve PCOD within thirty-six (36) months of the Notice to Proceed "
                 "(the Scheduled PCOD)."),
    ("SB15", V5, "The Project Company shall submit monthly progress reports and shall permit the Authority access "
                 "to the site at all reasonable times."),
    ("SB16", V5, "If PCOD is not achieved by the Scheduled PCOD, the Project Company shall pay to the Authority "
                 "delay liquidated damages at the rate of SAR 180,000 for each day of delay."),
    ("SB17", V5, "If PCOD has not been achieved within three hundred and sixty-five (365) days after the Scheduled "
                 "PCOD, the Authority may terminate under Clause 39.2."),
    ("SB18", V5, "The Project Company shall have no right to an extension of the term save as expressly provided "
                 "in Clause 34 (Relief Events) and Clause 36 (Change in Law)."),
    ("SB19", V5, "A Relief Event entitles the Project Company to an extension of time but not to compensation."),
    ("SB20", A1, "Can the Authority confirm the ground conditions at the wadi crossing?"),
    ("SB21", A1, "The geotechnical report in the data room is provided for information. Bidders shall satisfy "
                 "themselves as to ground conditions."),
    ("SB22", V1, "Attendance at the site visit is optional and does not relieve a Bidder of its obligation to "
                 "satisfy itself as to site conditions."),
    ("SB23", V1, "From the date of issue of this Volume until the issue of the Preferred Bidder Notification, no "
                 "Bidder, and no person acting for a Bidder, shall contact any board member, officer, employee, "
                 "consultant or advisor of the Authority in relation to the Project other than through the Portal. "
                 "Breach of this Clause shall result in the disqualification of the Bidder."),
    ("SB24", V1, "All communications between a Bidder and the Authority shall be made exclusively through the "
                 "Portal and shall be in the English language, save where this Volume expressly requires Arabic."),
    ("SB25", V1, "Envelope B shall contain only (a) Form 4-F (Financial Proposal Schedule) and (b) the Financial "
                 "Model. No other document shall be placed in Envelope B."),
    ("SB26", V1, "The Bidder shall submit with Form 4-F a schedule of the principal financing assumptions "
                 "underlying the Availability Payment, including the assumed debt tenor, margin and gearing."),
    ("SB27", V1, "The appearance of any price, rate, or other commercial information within Envelope A shall "
                 "render the Proposal non-responsive."),
    ("SB28", V4, "Envelope B only. This Form and the Financial Model are the only documents to be placed in "
                 "Envelope B."),
    ("SB29", V5, "The Senior Lenders shall have step-in rights in accordance with the Direct Agreement, and the "
                 "Authority shall not terminate under Clause 39.1 without first giving the Senior Lenders the "
                 "notice and cure period stated in the Direct Agreement."),
    ("SB30", V5, "On termination for Project Company default, compensation shall be the lesser of (a) the market "
                 "value of the Agreement determined by a re-tender and (b) outstanding senior debt, in each case "
                 "less the Authority's costs of re-tender and rectification."),
    ("SB31", V2, "A grievance mechanism accessible to the affected community shall be established before "
                 "construction and maintained for the concession period."),
    ("SB32", A1, "Statements recorded in the minutes at Appendix B are a record of what was said and do not bind "
                 "the Authority unless the substance is confirmed in the body of an Addendum."),
    ("SB33", V1, "Requests for clarification shall be submitted no later than ten (10) Working Days before the "
                 "Proposal Due Date. Requests received after that time will not be answered."),
    ("SB34", V1, "Where a period expressed in Working Days is to be counted backwards from a stated date, the "
                 "stated date itself shall not be counted."),
    ("SB35", V1, "A Bidder that identifies a conflict, ambiguity or discrepancy shall raise it as a request for "
                 "clarification under Section 5. A Bidder that resolves such a conflict unilaterally does so at its "
                 "own risk, and the Authority shall not be bound by the Bidder's interpretation."),
    ("SB36", A2, "Operations and maintenance philosophy and lifecycle strategy"),
    ("SB37", V1, "Proposals shall be received by the Authority not later than 14:00 hours Riyadh time on Thursday "
                 "12 November 2026"),
    ("SB38", A1, "Volume I Clause 6.1 is amended by deleting ‘Thursday 12 November 2026’ and substituting "
                 "‘Thursday 26 November 2026’. The time of 14:00 Riyadh time is unchanged."),
    ("SB39", V5, "Deductions shall not apply during a Relief Event or a Force Majeure Event to the extent that the "
                 "Unavailability Event is caused by that event."),
    ("SB40", V1, "The Technical Proposal shall address, as a minimum, the process design, the construction "
                 "methodology and programme, the operations and maintenance philosophy,"),
    ("SB41", V2, "The Works comprise: the inlet works and screening; primary, secondary and tertiary treatment;"),
    ("SB42", V5, "The Authority shall appoint an Independent Engineer whose reasonable costs shall be borne equally "
                 "by the parties."),
    ("SB43", V1, "The Authority may seek written clarification of any Proposal."),
]

# Strings that the answer key quotes from Addendum No. 3; each must appear in its text layer.
def key_strings():
    s = [COVER, PRECEDENCE, R1_1, R1_2, R1_3, S2_1, S2_2, S3_1, OLD_8_5, S3_1B,
         S3_2.replace("<b>", "").replace("</b>", ""), S3_3.replace("<b>", "").replace("</b>", ""),
         S3_4, S3_5, S4_1, NEW_12_5, S4_2, S4_3, S4_4, issued(ISSUE),
         "Table 42-1 — Minimum residual service life of assets at transfer"]
    for row in QA:
        s += row[1:]
    for row in EN_TABLE:
        s.append(" ".join(row))
    for num, txt in EN_NOTES:
        s.append(num + " " + txt)
    return s


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def doc_text(path):
    d = pymupdf.open(path)
    out = []
    for p in d:
        lines = []
        for b in p.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                if abs(ln["dir"][1]) > 0.1:          # drop the rotated watermark
                    continue
                lines.append("".join(sp["text"] for sp in ln["spans"]))
        out.append(norm(" ".join(lines)))
    return out


def check(pack_dir):
    texts = {}
    for fn in sorted({fn for _, fn, _ in STATE_BEFORE} | {fn for fn, _ in OLD_ONCE}):
        texts[fn] = doc_text(pack_dir.rstrip("/") + "/" + fn)
    for fn, s in OLD_ONCE:
        n = norm(" ".join(texts[fn])).count(norm(s))
        if n != 1:
            raise SystemExit("OLD text not exactly once in %s (%d): %s" % (fn, n, s))
    for sid, fn, s in STATE_BEFORE:
        whole = norm(" ".join(texts[fn]))
        if norm(s) not in whole:
            raise SystemExit("NOT VERBATIM %s in %s: %s" % (sid, fn, s))
        pages = [i + 1 for i, t in enumerate(texts[fn]) if norm(s) in t]
        print("verbatim %s %-36s p.%-6s %s" % (sid, fn, ",".join(map(str, pages)) or "span", s[:60]))
    print("verbatim: %d old + %d state_before quotations OK" % (len(OLD_ONCE), len(STATE_BEFORE)))
    for k, v in DATES.items():
        print("date %-46s %s" % (k, long_date(v)))
    print("Working Days from the issue date (incl.) to the PDD (excl.): %d" % wd_between(ISSUE, PDD))
    print("Volume V 36.2 amount: base %d -> ADD-02 %d -> ADD-03 %d (cover says %d)"
          % (CIL_BASE, CIL_ADD02, CIL_NOW, CIL_COVER_WRONG))


def self_check(out_path):
    t = norm(" ".join(doc_text(out_path)))
    for s in key_strings():
        if norm(s) not in t:
            raise SystemExit("key string not in the built text layer: %s" % s)
    if re.search("[؀-ۿ]", t):
        raise SystemExit("Arabic code point in the text layer")
    for s, n in ((S4_3_REQ, 1), (S4_3_APPT, 1), ("SAR 4,000,000", 1), ("SAR 1,000,000", 1)):
        assert t.count(norm(s)) == n, (s, t.count(norm(s)))
    print("self-check: %d key strings found in the text layer; no Arabic code point" % len(key_strings()))


def main():
    for name, want in PINNED_FONTS.items():
        got = hashlib.sha256(open(FREEFONT + name, "rb").read()).hexdigest()
        if got != want:
            raise SystemExit("unexpected %s; output would not be reproducible" % name)
    if pymupdf.VersionBind != PINNED_VERSIONS["pymupdf"] or np.__version__ != PINNED_VERSIONS["numpy"]:
        raise SystemExit("pinned versions: %r" % PINNED_VERSIONS)
    args = list(sys.argv[1:])
    pack = None
    if "--check" in args:
        i = args.index("--check")
        pack = args[i + 1]
        del args[i:i + 2]
    out = args[0] if args else "ADD-03_Addendum_No_3.pdf"
    if pack:
        check(pack)
    image_raw = table_42_1_image()
    image_name = "FormXob." + hashlib.md5(image_raw).hexdigest()
    n = build_pdf(addendum3(image_name), "Addendum No. 3", out, META, image_raw, image_name, DOC_ID)
    self_check(out)
    print("pages: %d" % n)


if __name__ == "__main__":
    main()
