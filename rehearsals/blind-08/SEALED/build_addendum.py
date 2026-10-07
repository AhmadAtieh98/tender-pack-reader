#!/usr/bin/env python3
"""Builder for the blind rehearsal 08 input (SYNTHETIC: not tender content):

  ADD-03_Addendum_No_3.pdf  (stands on the base pack as amended by Addenda Nos. 1 and 2 only)

Drawn in the page furniture and typography of the issued Addenda Nos. 1 and 2: A4, Base-14
Type1 fonts (Helvetica, Helvetica-Bold, Times-Roman, Times-Bold, WinAnsiEncoding, not
embedded) for every text-layer glyph, the ADD-01/ADD-02 watermark, header, footer and rules,
the ADD-01/ADD-02 clarification grid and table styling.  The cover carries the line
"SYNTHETIC: not tender content", and so do the Subject, Keywords and Producer metadata.
There is no Arabic code point in the text layer.

Appendix A carries one IMAGE-ONLY element (the Office letter with Table 8-1, Arabic), drawn the
way Volume II draws its Table 2-4 reproduction: a partial-page "scanned" raster 1750 px across,
RGB with equal channels, FlateDecode, placed at the frame's left edge over the full frame width
directly below an introductory paragraph.  The Arabic is shaped by MuPDF's HTML engine
(HarfBuzz) in GNU FreeSerif from the AR dictionary below (no OCR layer); the vector master is
rotated slightly, rasterised, toned to the pack's paper grey and speckled with a fixed-seed
numpy generator.

The layout engine, furniture, Arabic line shaper and raster pipeline are adapted from the
blind-07 builder (technique example).  The content is new.

Output is byte-for-byte deterministic (fixed dates, fixed /ID, fixed seed, pinned library
versions and font files).

Usage:
  python -I build_addendum.py <ADD-03 output.pdf> [--check <candidate_pack_dir>]
                                                  [--verify-key expected_findings.yaml]
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
IMG_PX_W, IMG_PX_H = 1750, 1750
IMG_W = 481.8898
IMG_ZOOM = IMG_PX_W / IMG_W
IMG_H = IMG_PX_H / IMG_ZOOM
IMG_SEED = 20261116
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
        "synth": dict(size=8.5, lead=11, reg="F2", bold="F2", justify=False),
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
LETTER = dt.date(2026, 11, 16)                  # Investment Services Office letter No. 228/2026 (Table 8-1)
ISSUE = dt.date(2026, 11, 18)                   # Addendum No. 3 issue date (after the 5.2 cut-off)
Q16_LODGE = dt.date(2026, 11, 22)               # response 16: reduced period for applications lodged by this day


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
    """Table 8-1 Note 1 (Arabic, governing): counted from the Working Day following the day of receipt."""
    c = 0
    while c < n:
        d += dt.timedelta(days=1)
        if is_wd(d):
            c += 1
    return d


def latest_lodging(n, must_issue_by):
    """Latest lodging day d (a Working Day) such that wd_after_excl(d, n) <= must_issue_by."""
    d = must_issue_by
    while True:
        if is_wd(d) and wd_after_excl(d, n) <= must_issue_by:
            return d
        d -= dt.timedelta(days=1)


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


# Issue periods of Table 8-1: the ARABIC text governs (Section 2.2).  The English translation
# (Appendix B) shows 3 for row 2 (deliberate discrepancy AR1).
PERIOD_AR = {1: 3, 2: 5, 3: 8}
PERIOD_EN = {1: 3, 2: 3, 3: 8}
Q16_REDUCTION = 2
PERIOD_ROW2_Q16 = PERIOD_AR[2] - Q16_REDUCTION                 # 3 (correct)
PERIOD_ROW2_Q16_WRONG = PERIOD_EN[2] - Q16_REDUCTION           # 1 (stale English base)
assert (PERIOD_ROW2_Q16, PERIOD_ROW2_Q16_WRONG) == (3, 1)

HAND_BY = PDD - dt.timedelta(days=1)            # certificate in hand by close of the Working Day before the PDD
assert HAND_BY == dt.date(2026, 11, 25) and is_wd(HAND_BY)

DATES = {
    "add02_issue": ADD02,
    "clarification_cutoff_vol1_5_2": wd_before(PDD, 10),
    "table_8_1_letter": LETTER,
    "add03_issue": ISSUE,
    "q16_lodging_limit": Q16_LODGE,
    "s2_5_portal_notification_3wd_before_pdd": wd_before(PDD, 3),
    "row1_latest_lodging_for_issue_by_25_nov": latest_lodging(PERIOD_AR[1], HAND_BY),
    "row2_latest_lodging_with_q16_reduction": Q16_LODGE,
    "row2_issue_if_lodged_22_nov_reduced": wd_after_excl(Q16_LODGE, PERIOD_ROW2_Q16),
    "row2_issue_if_lodged_23_nov_unreduced": wd_after_excl(dt.date(2026, 11, 23), PERIOD_AR[2]),
    "row2_issue_if_lodged_on_add03_issue_unreduced": wd_after_excl(ISSUE, PERIOD_AR[2]),
    "row3_latest_lodging_for_issue_by_25_nov": latest_lodging(PERIOD_AR[3], HAND_BY),
    "row3_issue_if_lodged_on_add03_issue": wd_after_excl(ISSUE, PERIOD_AR[3]),
    "proposal_due_date": PDD,
}
assert ADD02 < DATES["clarification_cutoff_vol1_5_2"] < LETTER < ISSUE < Q16_LODGE < PDD
assert all(is_wd(d) for d in (LETTER, ISSUE, Q16_LODGE, PDD))
assert DATES["clarification_cutoff_vol1_5_2"] == dt.date(2026, 11, 12)
assert DATES["s2_5_portal_notification_3wd_before_pdd"] == dt.date(2026, 11, 23)
assert DATES["row1_latest_lodging_for_issue_by_25_nov"] == dt.date(2026, 11, 22)
assert DATES["row2_issue_if_lodged_22_nov_reduced"] == dt.date(2026, 11, 25)
assert DATES["row2_issue_if_lodged_23_nov_unreduced"] == dt.date(2026, 11, 30)
assert DATES["row2_issue_if_lodged_on_add03_issue_unreduced"] == dt.date(2026, 11, 25)
assert DATES["row3_latest_lodging_for_issue_by_25_nov"] == dt.date(2026, 11, 15)
assert DATES["row3_latest_lodging_for_issue_by_25_nov"] < ISSUE          # row 3 cannot be met by a new application
assert DATES["row3_issue_if_lodged_on_add03_issue"] == dt.date(2026, 11, 30)
assert wd_between(ISSUE, PDD) == 6

# Figures derived from the text (asserted; printed by --check)
AEOD_BASE, AEOD_CUT_PCT = 20_000_000, 40
AEOD_NOW = AEOD_BASE * (100 - AEOD_CUT_PCT) // 100            # 12,000,000
AEOD_COVER_WRONG = AEOD_BASE * AEOD_CUT_PCT // 100             # 8,000,000 (cover error E1)
assert (AEOD_NOW, AEOD_COVER_WRONG) == (12_000_000, 8_000_000)
PCOD_BASE_M, PCOD_ADD_M = 36, 6
PCOD_NOW_M = PCOD_BASE_M + PCOD_ADD_M
assert PCOD_NOW_M == 42
ADF_M3_DAY, PEAK_M3_H, HOURS = 120_000, 7_500, 6
RES_READING_AVG = ADF_M3_DAY // 24 * HOURS                     # 30,000 m3
RES_READING_PEAK = PEAK_M3_H * HOURS                           # 45,000 m3
assert (RES_READING_AVG, RES_READING_PEAK) == (30_000, 45_000)


# --------------------------------------------------------------------------
# Arabic source strings of Table 8-1 (the governing text).  Keys are referenced by the
# answer key.  The discrepancy against the English convenience translation (Appendix B) is
# deliberate: AR1 (row 2 issue period: 5 Working Days in Arabic, 3 in English).
# --------------------------------------------------------------------------
AR = {
    "issuer": "مكتب خدمات الاستثمار بالمنطقة الشمالية",
    "ref": "الرقم: ٢٢٨/٢٠٢٦",
    "date": "التاريخ: ١٦ نوفمبر ٢٠٢٦م",
    "to": "إلى: الهيئة الشمالية للمشتريات المرفقية",
    "subject": "الموضوع: تسجيل استثمار أعضاء الائتلافات المؤسسين خارج المملكة",
    "tender": "مناقصة رقم: NUPA/ISTP/2026/014 (محطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان)",
    "title": "جدول ٨-١: مدد إصدار شهادة تسجيل الاستثمار",
    "intro": "يُصدر المكتب شهادة تسجيل الاستثمار للعضو المؤسس خارج المملكة خلال المدة المبيَّنة أدناه لفئته:",
    "h_no": "م",
    "h_cls": "فئة العضو",
    "h_docs": "المستندات المطلوبة مع الطلب",
    "h_period": "مدة الإصدار (أيام عمل)",
    "no1": "١", "no2": "٢", "no3": "٣",
    "c1": "شركة مؤسسة في إحدى دول مجلس التعاون الخليجي",
    "c2": "شركة مؤسسة خارج دول مجلس التعاون الخليجي",
    "c3": "فرع مسجل في المملكة لشركة أجنبية",
    "d1": "السجل التجاري مصدقاً",
    "d2": "السجل التجاري والقوائم المالية المدققة لآخر سنة مالية، مصدقة",
    "d3": "شهادة تسجيل الفرع وقرار مجلس إدارة الشركة الأم بتفويض الفرع",
    "p1": "٣", "p2": "٥", "p3": "٨",
    "notes": "ملاحظات:",
    "n1": "١. تُحسب مدة الإصدار بأيام العمل اعتباراً من يوم العمل التالي ليوم استلام الطلب المكتمل.",
    "n2": "٢. تكون الشهادة سارية لمدة تسعين (٩٠) يوماً من تاريخ إصدارها.",
    "n3": "٣. تُقدَّم الطلبات إلكترونياً عبر بوابة المكتب فقط، ولا يُعدّ الطلب مكتملاً إلا بإرفاق جميع المستندات المبيَّنة أعلاه.",
    "sign": "مدير مكتب خدمات الاستثمار بالمنطقة الشمالية",
}
AR_LINES = {
    "h_docs": ["المستندات المطلوبة", "مع الطلب"],
    "h_period": ["مدة الإصدار", "(أيام عمل)"],
    "c1": ["شركة مؤسسة في إحدى دول", "مجلس التعاون الخليجي"],
    "c2": ["شركة مؤسسة خارج دول", "مجلس التعاون الخليجي"],
    "c3": ["فرع مسجل في المملكة", "لشركة أجنبية"],
    "d2": ["السجل التجاري والقوائم المالية المدققة", "لآخر سنة مالية، مصدقة"],
    "d3": ["شهادة تسجيل الفرع وقرار مجلس إدارة", "الشركة الأم بتفويض الفرع"],
    "n3": ["٣. تُقدَّم الطلبات إلكترونياً عبر بوابة المكتب فقط، ولا يُعدّ الطلب مكتملاً",
           "إلا بإرفاق جميع المستندات المبيَّنة أعلاه."],
}
for _k, _lines in AR_LINES.items():
    assert " ".join(_lines) == AR[_k], _k
assert AR["p2"] == "٥" and AR["p1"] == "٣" and AR["p3"] == "٨"


def table_8_1_master():
    """Vector master of the reproduced letter and table (points; 1750 px across when rasterised)."""
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

    line(AR["issuer"], RX, 26, 13, bold=True)
    pg.insert_text((L + 2, 22), "Northern Region Investment Services Office",
                   fontname="tiro", fontsize=8, color=(0.3, 0.3, 0.3))
    line(AR["ref"], RX, 46, 9.5)
    line(AR["date"], RX - 150, 46, 9.5)
    sh = pg.new_shape()
    sh.draw_line((L, 55), (R, 55))
    sh.finish(color=(0, 0, 0), width=0.9)
    sh.commit()
    line(AR["to"], RX, 72, 9.8, bold=True)
    line(AR["subject"], RX, 88, 9.6)
    line(AR["tender"], RX, 103, 9.6)
    line(AR["title"], RX, 127, 12.5, bold=True)
    line(AR["intro"], RX, 146, 9.8)
    # table, columns from right to left: no | class of member | documents | issue period
    cols = [R, R - 32, R - 186, R - 376, L]
    top = 158.0
    hh, rh = 38.0, 36.0
    nrows = 3
    bottom = top + hh + nrows * rh
    sh = pg.new_shape()
    sh.draw_rect(pymupdf.Rect(L, top, R, top + hh))
    sh.finish(color=None, fill=(0.88, 0.88, 0.88), width=0)
    sh.draw_rect(pymupdf.Rect(L, top, R, bottom))
    for r in range(nrows):
        sh.draw_line((L, top + hh + r * rh), (R, top + hh + r * rh))
    for cx in cols[1:-1]:
        sh.draw_line((cx, top), (cx, bottom))
    sh.finish(color=(0, 0, 0), width=0.8)
    sh.commit()
    pad = 5.0

    def cell(key, ci, y0, height, size, bold=False, inset=0.0):
        texts = AR_LINES.get(key, [AR[key]])
        xr = cols[ci] - pad - inset
        if len(texts) == 1:
            bases = [y0 + height / 2 + size * 0.35]
        else:
            bases = [y0 + height / 2 - 2.5, y0 + height / 2 + 11.5]
        for t, b in zip(texts, bases):
            w = ar_line(pg, t, xr, b, size, bold)
            if xr - w < cols[ci + 1] + 3.0:
                raise SystemExit("Arabic cell text does not fit: %s" % t)

    for ci, key in enumerate(["h_no", "h_cls", "h_docs", "h_period"]):
        cell(key, ci, top, hh, 9.6, True, inset=(6 if ci == 0 else 0))
    for r in range(nrows):
        s = str(r + 1)
        y0 = top + hh + r * rh
        cell("no" + s, 0, y0, rh, 10, inset=9)
        cell("c" + s, 1, y0, rh, 9.8)
        cell("d" + s, 2, y0, rh, 9.6)
        cell("p" + s, 3, y0, rh, 11, inset=30)
    y = bottom + 22
    line(AR["notes"], RX, y, 10, bold=True)
    y += 17
    line(AR["n1"], RX - 4, y, 9.4)
    y += 17
    line(AR["n2"], RX - 4, y, 9.4)
    y += 17
    line(AR_LINES["n3"][0], RX - 4, y, 9.4)
    y += 14
    line(AR_LINES["n3"][1], RX - 14, y, 9.4)
    y += 36
    line(AR["sign"], RX, y, 10.5, bold=True)
    sh = pg.new_shape()
    sh.draw_bezier((R - 190, y + 24), (R - 160, y + 4), (R - 140, y + 34), (R - 100, y + 12))
    sh.finish(color=(0.15, 0.15, 0.15), width=0.9)
    sh.draw_oval(pymupdf.Rect(L + 60, y - 18, L + 128, y + 26))
    sh.finish(color=(0.45, 0.45, 0.45), width=0.8)
    sh.commit()
    pg.insert_text((L + 2, H - 9), "FICTIONAL DOCUMENT - Lamar Holding internal assessment pack - "
                   "not a real tender. SYNTHETIC: not tender content.", fontname="tiro", fontsize=6.5,
                   color=(0.45, 0.45, 0.45))
    if y + 30 > H - 14:
        raise SystemExit("table master overflows")
    return doc


def table_8_1_image():
    """Rotate slightly, rasterise at 1750 px across, tone to paper grey, speckle."""
    master = table_8_1_master()
    scan = pymupdf.open()
    sp = scan.new_page(width=IMG_W, height=IMG_H)
    sp.show_pdf_page(sp.rect, master, 0, rotate=0.25)
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


SYNTH = "SYNTHETIC: not tender content. Test material for blind rehearsal 08; not issued by any authority."

PRECEDENCE = ("This Addendum forms part of the RFP Documents and takes precedence in accordance with Volume I "
              "Clause 3.2. Bidders shall acknowledge receipt in Form 4-A. All other terms of the RFP Documents "
              "remain unchanged.")

# Planted cover errors: E1 'SAR 8,000,000' (operative result SAR 12,000,000); E2 'clarification
# requests 15 to 20' (five requests, 15 to 19, are answered); E3 'failing which the Proposal will be
# rejected' (Section 2.5 states no consequence).
COVER = (
    "This Addendum replaces Volume I Clause 8.9 so that a member of a Bidder incorporated outside the Kingdom "
    "must submit either its investment licence or a Certificate of Investment Registration issued within the "
    "periods in Table 8-1 (issued in Arabic), subject to a limited exception, requires a Bidder relying on a "
    "Certificate to notify the Authority of its applications, failing which the Proposal will be rejected, "
    "inserts a new Volume II Clause 4.6 on the treated effluent storage reservoir, extends the Scheduled PCOD "
    "in Volume V Clause 12.1 to forty-two (42) months, reduces the unpaid sum that constitutes an Authority "
    "Event of Default under Volume V Clause 39.4 to SAR 8,000,000, and responds to clarification requests 15 "
    "to 20.")
COVER_E1 = "to SAR 8,000,000"
COVER_E2 = "responds to clarification requests 15 to 20"
COVER_E3 = "failing which the Proposal will be rejected"

R1_1 = ("This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in "
        "accordance with Volume I Clause 3.2.")
R1_2 = ("A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by "
        "Addenda Nos. 1 and 2, unless otherwise stated.")
R1_3 = "Clarification requests 15 to 19 were received before the time stated in Volume I Clause 5.2."

OLD_8_9 = ("The Bidder shall submit either evidence of a current investment licence for each foreign consortium "
           "member, or a signed undertaking to obtain such licence prior to Financial Close.")
S2_1 = "Volume I Clause 8.9 is deleted and replaced by the following:"
NEW_8_9 = ("Each member of the Bidder that is incorporated outside the Kingdom shall submit with Envelope A "
           "either (a) a copy of its current investment licence or (b) a Certificate of Investment Registration "
           "issued by the Northern Region Investment Services Office (the Office) in accordance with Table 8-1. "
           "A Proposal that does not include the evidence required by this Clause for each such member shall be "
           "rejected.")
S2_2 = ("Table 8-1 is reproduced at Appendix A to this Addendum as issued by the Office and forms part of Volume "
        "I. Table 8-1 is issued in the Arabic language. The Arabic text governs. The English translation at "
        "Appendix B is provided for convenience only.")
S2_3 = ("Applications for a Certificate of Investment Registration shall be made by the member to the Office. "
        "The Office has undertaken to the Authority to issue a Certificate within the issue period stated in "
        "Table 8-1 for the class of the member, counted in accordance with the Notes to Table 8-1.")
S2_4 = ("Section 2.1 does not apply to a member of the Bidder that is to hold not more than ten per cent (10%) "
        "of the shares in the Project Company and that has no role in the design, construction or operation of "
        "the Facility. Such a member shall instead submit with Envelope A the signed undertaking described in "
        "Volume I Clause 8.9 as issued.")
S2_5_WHEN = "not later than three (3) Working Days before the Proposal Due Date"
S2_5 = ("A Bidder that relies on paragraph (b) of Volume I Clause 8.9 for any member shall notify the Authority "
        "through the Portal, %s, of the name of that member and the reference number of its application to "
        "the Office." % S2_5_WHEN)
S2_6 = "The periods in Volume I Clause 12.2 for Commercial Close and Financial Close are unchanged."

S3_1 = "The following new Clause 4.6 is inserted in Volume II after Clause 4.5:"
NEW_4_6 = ("The treated effluent storage reservoir referred to in Clause 1.2 shall provide a working volume of "
           "not less than six (6) hours of the design flow and shall be divided into not fewer than two (2) "
           "compartments, each capable of being isolated for cleaning while the other remains in service.")
S3_2 = "The insertion of Clause 4.6 does not renumber any other Clause of Volume II."
S3_3 = "In Volume V Clause 12.1, the period of thirty-six (36) months is increased by six (6) months."
S3_4 = ("Bidders shall reflect Sections 3.1 and 3.3 in the process design and the construction programme "
        "submitted in the Technical Proposal and in the Financial Model.")

S4_1 = "The amount stated in Volume V Clause 39.4 is reduced by forty per cent (40%)."
S4_2 = "The period of sixty (60) days in Volume V Clause 39.4 is unchanged."

QA = [
    ["15",
     "May the undertaking required by Volume I Clause 8.9 be given by the lead member on behalf of a foreign "
     "consortium member?",
     "No. Volume I Clause 8.9 is replaced by Section 2.1 of this Addendum and an undertaking is no longer "
     "accepted, save from a member described in Section 2.4, which shall give its own undertaking."],
    ["16",
     "Will the Authority assist foreign consortium members that have not obtained an investment licence "
     "before the Proposal Due Date?",
     "Section 2 of this Addendum applies. The Office has confirmed to the Authority that, for an application "
     "lodged not later than Sunday 22 November 2026, the issue period in row 2 of Table 8-1 is reduced by two "
     "(2) Working Days. The other issue periods in Table 8-1 are unchanged."],
    ["17",
     "Will the arbitration under Volume V Clause 44.2 be conducted in English?",
     "Yes. Volume V Clause 44.2 applies."],
    ["18",
     "Volume II Clause 1.2 includes a treated effluent storage reservoir, but no capacity is stated. What "
     "capacity is required?",
     "See new Volume II Clause 4.6, inserted by Section 3.1 of this Addendum."],
    ["19",
     "Will the Authority reconsider the threshold for an Authority Event of Default in Volume V Clause 39.4?",
     "Yes. See Section 4 of this Addendum."],
]

EN_TABLE = [
    ["1", "Company incorporated in a GCC state", "Certified commercial registration", "3"],
    ["2", "Company incorporated outside the GCC states",
     "Commercial registration and audited financial statements for the last financial year, certified", "3"],
    ["3", "Branch registered in the Kingdom of a foreign company",
     "Branch registration certificate and parent company board resolution authorising the branch", "8"],
]
EN_NOTES = [
    ("(1)", "The issue period is counted in Working Days from the Working Day following the day of receipt of a "
            "complete application."),
    ("(2)", "A Certificate is valid for ninety (90) days from its date of issue."),
    ("(3)", "Applications are made electronically through the Office's portal only. An application is complete "
            "only when all the documents listed above are attached."),
]


class IssuePeriodTable(Grid):
    # ADD-02 Table 1-1 outer edges (70.86614 .. 524.4094), four columns
    COLS = [70.86614, 100.86614, 250.86614, 440.86614, 524.4094]

    def __init__(self, rows):
        super().__init__(self.COLS, ["No", "Class of member", "Documents required with the application",
                                     "Issue period (Working Days)"], rows)


def addendum3(image_name):
    F = []
    F.append(Cover("3", issued(ISSUE), "Tender NUPA/ISTP/2026/014"))
    F.append(Para("proj", "Wadi Sirhan Independent Sewage Treatment Plant"))
    F.append(Para("synth", SYNTH))
    F.append(Para("body", COVER))
    F.append(Para("body", PRECEDENCE))

    F.append(Para("head", "1. RECITALS"))
    F.append(Para("prov", R1_1, "1.1"))
    F.append(Para("prov", R1_2, "1.2"))
    F.append(Para("prov", R1_3, "1.3"))

    F.append(Para("head", "2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS"))
    F.append(Para("prov", S2_1, "2.1", keep_next=True))
    F.append(Para("quote", NEW_8_9 + RQ, "8.9"))
    F.append(Para("prov", S2_2, "2.2"))
    F.append(Para("prov", S2_3, "2.3"))
    F.append(Para("prov", S2_4, "2.4"))
    F.append(Para("prov", S2_5, "2.5"))
    F.append(Para("prov", S2_6, "2.6"))

    F.append(Para("head", "3. TREATED EFFLUENT STORAGE AND SCHEDULED PCOD"))
    F.append(Para("prov", S3_1, "3.1", keep_next=True))
    F.append(Para("quote", NEW_4_6 + RQ, "4.6"))
    F.append(Para("prov", S3_2, "3.2"))
    F.append(Para("prov", S3_3, "3.3"))
    F.append(Para("prov", S3_4, "3.4"))

    F.append(Para("head", "4. AUTHORITY EVENT OF DEFAULT"))
    F.append(Para("prov", S4_1, "4.1"))
    F.append(Para("prov", S4_2, "4.2"))

    F.append(Para("head", "5. RESPONSES TO CLARIFICATION REQUESTS 15 TO 19"))
    F.append(QATable(QA))

    F.append(PageBreak())
    F.append(Para("head", "APPENDIX A — TABLE 8-1 (ARABIC)"))
    F.append(Para("body", "The following letter and table are reproduced as issued by the Northern Region "
                          "Investment Services Office under its reference No. 228/2026 dated %d %s %d. The "
                          "Arabic text governs in accordance with Section 2.2 of this Addendum."
                  % (LETTER.day, LETTER.strftime("%B"), LETTER.year), keep_next=True))
    F.append(ImageBlock(image_name))
    F.append(Para("body", "End of reproduction."))

    F.append(Para("head", "APPENDIX B — ENGLISH TRANSLATION OF TABLE 8-1"))
    F.append(Para("body", "This translation is provided for convenience only. The Arabic text of Table 8-1 at "
                          "Appendix A governs. Northern Region Investment Services Office, reference No. 228/2026 "
                          "dated %d %s %d, to the Northern Utilities Procurement Authority. Subject: investment "
                          "registration of consortium members incorporated outside the Kingdom. Tender No. "
                          "NUPA/ISTP/2026/014 (Wadi Sirhan Independent Sewage Treatment Plant)."
                  % (LETTER.day, LETTER.strftime("%B"), LETTER.year)))
    F.append(Para("ttitle", "Table 8-1 — Issue periods for Certificates of Investment Registration"))
    F.append(Para("body", "The Office issues a Certificate of Investment Registration to a member incorporated "
                          "outside the Kingdom within the period stated below for its class."))
    F.append(IssuePeriodTable(EN_TABLE))
    F.append(NoteRule())
    F.append(Para("notehdr", "Notes to Table 8-1:"))
    for num, txt in EN_NOTES:
        F.append(Para("note", txt, num))
    F.append(Para("body", "Signed: Director, Northern Region Investment Services Office (signature and stamp)."))
    return F


META = {"title": "(anonymous)", "author": "(anonymous)",
        "subject": "SYNTHETIC: not tender content",
        "creator": "(unspecified)", "keywords": "SYNTHETIC: not tender content; blind rehearsal 08",
        "producer": "blind-08 build_addendum.py (PyMuPDF 1.28.2) - SYNTHETIC: not tender content",
        "creationDate": "D:20261118102501+00'00'", "modDate": "D:20261118102501+00'00'"}
DOC_ID = hashlib.md5(b"NUPA/ISTP/2026/014 Addendum No. 3 issued 18 November 2026 (blind-08)").hexdigest().upper()


# --------------------------------------------------------------------------
# Consistency check against the issued pack (old quotations and state_before verbatim)
# --------------------------------------------------------------------------
V1, V2, V4, V5 = ("VOL-I_Instructions_to_Bidders.pdf", "VOL-II_Technical_Requirements.pdf",
                  "VOL-IV_Form_Sheets.pdf", "VOL-V_Draft_Project_Agreement.pdf")
A1, A2 = "ADD-01_Addendum_No_1.pdf", "ADD-02_Addendum_No_2.pdf"

# "old" texts the Addendum relies on; each must occur exactly once in its volume
OLD_ONCE = [
    (V1, OLD_8_9),
    (V5, "within thirty-six (36) months of the Notice to Proceed"),
    (V5, "an undisputed sum exceeding SAR 20,000,000 that continues for sixty (60) days after notice"),
    (V2, "the treated effluent storage reservoir"),
]

# Pack text that must NOT contain the ambiguous expression (GA1 is not settled anywhere)
ABSENT = [(fn, "design flow") for fn in (V1, V2, V4, V5, A1, A2)]

# state_before quotations used by the answer key (id, file, text)
STATE_BEFORE = [
    ("SB01", V1, OLD_8_9),
    ("SB02", V1, "(i) the certificates and evidence required under Section 8."),
    ("SB03", V1, "Envelope B shall contain only (a) Form 4-F (Financial Proposal Schedule) and (b) the Financial "
                 "Model. No other document shall be placed in Envelope B."),
    ("SB04", V1, "The Preferred Bidder shall achieve Commercial Close within one hundred and twenty (120) days, and "
                 "Financial Close within two hundred and seventy (270) days, of the date of the Preferred Bidder "
                 "Notification."),
    ("SB05", V1, "Working Day means any day from Sunday to Thursday inclusive, other than a day declared a public "
                 "holiday in the Kingdom. Where a period expressed in Working Days is to be counted backwards from "
                 "a stated date, the stated date itself shall not be counted."),
    ("SB06", V1, "Requests for clarification shall be submitted no later than ten (10) Working Days before the "
                 "Proposal Due Date. Requests received after that time will not be answered."),
    ("SB07", A1, "Volume I Clause 6.1 is amended by deleting ‘Thursday 12 November 2026’ and substituting "
                 "‘Thursday 26 November 2026’. The time of 14:00 Riyadh time is unchanged."),
    ("SB08", A1, "including without limitation the period in Volume I Clause 5.2 (clarification cut-off)"),
    ("SB09", V1, "(a) the Addenda, a later Addendum prevailing over an earlier one; (b) Volume I (Instructions to "
                 "Bidders); (c) Volume V (Draft Project Agreement); (d) Volume II (Technical Requirements);"),
    ("SB10", V1, "A Bidder that identifies a conflict, ambiguity or discrepancy shall raise it as a request for "
                 "clarification under Section 5. A Bidder that resolves such a conflict unilaterally does so at its "
                 "own risk, and the Authority shall not be bound by the Bidder's interpretation."),
    ("SB11", V2, "The Works comprise: the inlet works and screening; primary, secondary and tertiary treatment; "
                 "disinfection; sludge thickening, digestion and dewatering; odour control; the treated effluent "
                 "transmission main; the treated effluent storage reservoir; and all associated electrical, control "
                 "and civil works."),
    ("SB12", V2, "The Facility shall be designed for a nominal treatment capacity of 120,000 m3/day average daily "
                 "flow, measured at the inlet works, at the design year influent characteristics stated in Table "
                 "2-2."),
    ("SB13", V2, "2-6.1 Average daily flow 120,000 m3/day 2-6.2 Peak hourly flow (design) 7,500 m3/h"),
    ("SB14", V2, "The main shall be sized for the peak hourly flow in Table 2-6 with a maximum velocity of 2.0 m/s"),
    ("SB15", V2, "The Project Company shall satisfy itself as to the consistency of the flow figures stated in this "
                 "Volume and shall raise any inconsistency as a clarification under Volume I Clause 5.1."),
    ("SB16", A2, "Bidders shall design to the figures stated in Volume II. Volume II Clause 4.2 applies."),
    ("SB17", V2, "The transmission main shall be provided with surge protection designed for the full range of "
                 "operating scenarios including simultaneous pump trip."),
    ("SB18", V5, "The Project Company shall achieve PCOD within thirty-six (36) months of the Notice to Proceed "
                 "(the Scheduled PCOD)."),
    ("SB19", V5, "If PCOD is not achieved by the Scheduled PCOD, the Project Company shall pay to the Authority "
                 "delay liquidated damages at the rate of SAR 180,000 for each day of delay."),
    ("SB20", V5, "If PCOD has not been achieved within three hundred and sixty-five (365) days after the Scheduled "
                 "PCOD, the Authority may terminate under Clause 39.2."),
    ("SB21", V5, "The Authority may terminate where PCOD is not achieved within the period stated in Clause 18.3."),
    ("SB22", V4, "All obligations of the EPC Contractor under the EPC Contract during the construction period, "
                 "including the payment of liquidated damages."),
    ("SB23", V4, "Forms shall be reproduced without alteration to their wording."),
    ("SB24", V1, "The Bidder shall submit an executed Parent Company Guarantee from the ultimate parent company of "
                 "the proposed EPC Contractor, substantially in the form set out in Form 4-D, unconditional as to "
                 "the EPC Contractor's obligations during the construction period."),
    ("SB25", V1, "The Technical Proposal shall address, as a minimum, the process design, the construction "
                 "methodology and programme,"),
    ("SB26", A2, "B Construction methodology, programme and interface management 15"),
    ("SB27", V4, "We confirm that the Availability Payment stated above is unconditional, is not subject to any "
                 "qualification, and has been derived from the Financial Model submitted with this Form."),
    ("SB28", V5, "The Project Company may terminate for an Authority Event of Default, being a failure to pay an "
                 "undisputed sum exceeding SAR 20,000,000 that continues for sixty (60) days after notice."),
    ("SB29", V5, "On termination for Authority default or for prolonged force majeure, compensation shall equal "
                 "outstanding senior debt, breakage costs, and equity subscribed together with the equity return "
                 "to the date of termination, calculated under Schedule 12."),
    ("SB30", V5, "This extract contains the clauses of the draft Project Agreement on which the Authority invites "
                 "comment through Form 4-E. Clause numbering follows the full draft; omitted clauses are not "
                 "reproduced. A deviation not listed in Form 4-E will be taken as accepted."),
    ("SB31", V5, "The parties shall first refer a dispute to senior representatives, then to an expert where the "
                 "dispute is technical, and failing resolution to arbitration seated in Riyadh conducted in the "
                 "English language before three arbitrators"),
    ("SB32", V1, "The concession period shall be twenty-five (25) years commencing on the Project Commercial "
                 "Operation Date"),
    ("SB33", V5, "This Agreement shall come into force on the Effective Date and shall continue for a period of "
                 "twenty-five (25) years from the Effective Date, unless terminated earlier in accordance with its "
                 "terms."),
    ("SB34", A2, "The Authority notes the question. The order of precedence at Volume I Clause 3.2 applies. The "
                 "Authority does not consider further amendment necessary at this stage."),
    ("SB35", V1, "Proposals will be evaluated in three stages: (i) a responsiveness and mandatory compliance check "
                 "on a pass or fail basis;"),
    ("SB36", V1, "All communications between a Bidder and the Authority shall be made exclusively through the "
                 "Portal and shall be in the English language, save where this Volume expressly requires Arabic."),
    ("SB37", V1, "A Bidder shall be either a single entity or a consortium, in each case prequalified under the "
                 "RFQ. No change to the composition, shareholding or lead member of a prequalified consortium "
                 "shall be effective without the prior written consent of the Authority."),
    ("SB38", V1, "Proposals shall be received by the Authority not later than 14:00 hours Riyadh time on Thursday "
                 "12 November 2026"),
    ("SB39", V1, "The Authority will publish its responses to clarification requests in the form of Addenda issued "
                 "to all Bidders."),
    ("SB40", V5, "The Project Company shall have no right to an extension of the term save as expressly provided "
                 "in Clause 34 (Relief Events) and Clause 36 (Change in Law)."),
    ("SB41", V5, "A handback reserve shall be funded from the start of year twenty (20) of the term in an amount "
                 "certified by the Independent Engineer."),
    ("SB42", V5, "The aggregate liability of the Project Company for delay liquidated damages under this Clause 18 "
                 "shall not exceed ten per cent (10%) of the Estimated Project Cost."),
    ("SB43", V2, "All permanent civil structures shall be designed for a seismic event with a return period of 475 "
                 "years and for a flood with a return period of 100 years."),
]


def plain(s):
    return s.replace("<b>", "").replace("</b>", "")


# Strings that the answer key quotes from Addendum No. 3; each must appear in its text layer.
def key_strings():
    s = [SYNTH, COVER, PRECEDENCE, R1_1, R1_2, R1_3, S2_1, NEW_8_9, S2_2, S2_3, S2_4, S2_5, S2_6,
         S3_1, NEW_4_6, S3_2, S3_3, S3_4, S4_1, S4_2, issued(ISSUE),
         "Table 8-1 — Issue periods for Certificates of Investment Registration"]
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
    files = {fn for _, fn, _ in STATE_BEFORE} | {fn for fn, _ in OLD_ONCE} | {fn for fn, _ in ABSENT}
    for fn in sorted(files):
        texts[fn] = doc_text(pack_dir.rstrip("/") + "/" + fn)
    for fn, s in OLD_ONCE:
        n = norm(" ".join(texts[fn])).count(norm(s))
        if n != 1:
            raise SystemExit("OLD text not exactly once in %s (%d): %s" % (fn, n, s))
    for fn, s in ABSENT:
        if norm(s).lower() in norm(" ".join(texts[fn])).lower():
            raise SystemExit("expression unexpectedly present in %s: %s" % (fn, s))
    for sid, fn, s in STATE_BEFORE:
        whole = norm(" ".join(texts[fn]))
        if norm(s) not in whole:
            raise SystemExit("NOT VERBATIM %s in %s: %s" % (sid, fn, s))
        pages = [i + 1 for i, t in enumerate(texts[fn]) if norm(s) in t]
        print("verbatim %s %-36s p.%-6s %s" % (sid, fn, ",".join(map(str, pages)) or "span", s[:60]))
    print("verbatim: %d old + %d state_before quotations OK; %d absence checks OK"
          % (len(OLD_ONCE), len(STATE_BEFORE), len(ABSENT)))
    for k, v in DATES.items():
        print("date %-50s %s" % (k, long_date(v)))
    print("Working Days from the issue date (incl.) to the PDD (excl.): %d" % wd_between(ISSUE, PDD))
    print("Volume V 39.4 amount: base %d -> ADD-03 %d (cover says %d)" % (AEOD_BASE, AEOD_NOW, AEOD_COVER_WRONG))
    print("Volume V 12.1 period: %d -> %d months" % (PCOD_BASE_M, PCOD_NOW_M))
    print("Table 8-1 row 2 period: Arabic %d (English %d); after response 16: %d (stale English base: %d)"
          % (PERIOD_AR[2], PERIOD_EN[2], PERIOD_ROW2_Q16, PERIOD_ROW2_Q16_WRONG))
    print("Reservoir readings: %d m3 (average daily flow) or %d m3 (peak hourly flow (design))"
          % (RES_READING_AVG, RES_READING_PEAK))


def self_check(out_path):
    pages = doc_text(out_path)
    t = norm(" ".join(pages))
    for s in key_strings():
        if norm(plain(s)) not in t:
            raise SystemExit("key string not in the built text layer: %s" % s)
    if re.search("[؀-ۿ]", t):
        raise SystemExit("Arabic code point in the text layer")
    for s, n in ((S2_5_WHEN, 1), ("SAR 8,000,000", 1), ("15 to 20", 1), ("design flow", 1),
                 (COVER_E3, 1), ("SYNTHETIC: not tender content", 1)):
        assert t.count(norm(s)) == n, (s, t.count(norm(s)))
    for s in (COVER_E1, COVER_E2, COVER_E3):
        assert norm(s) in norm(COVER), s
    print("self-check: %d key strings found in the text layer; no Arabic code point" % len(key_strings()))
    return pages


def verify_key(key_path, pdf_pages, pack_dir):
    """Every addendum quote in the key must be on the page it names; every pack quote verbatim."""
    import yaml
    key = yaml.safe_load(open(key_path, encoding="utf-8"))
    pack = {}
    n_add, n_pack, n_ar = 0, 0, 0

    def walk(o):
        nonlocal n_add, n_pack, n_ar
        if isinstance(o, dict):
            if "quote" in o and "page" in o and o.get("doc", "ADD-03") == "ADD-03":
                pg = o["page"]
                if norm(o["quote"]) not in pdf_pages[pg - 1]:
                    raise SystemExit("key quote not on ADD-03 p.%s: %s" % (pg, o["quote"]))
                n_add += 1
            elif "quote" in o and "doc" in o and o["doc"] != "ADD-03-image":
                fn = o["doc"]
                if fn not in pack:
                    pack[fn] = doc_text(pack_dir.rstrip("/") + "/" + fn)
                pg = o.get("page")
                hay = pack[fn][pg - 1] if pg else norm(" ".join(pack[fn]))
                if norm(o["quote"]) not in hay:
                    raise SystemExit("pack quote not verbatim in %s p.%s: %s" % (fn, pg, o["quote"]))
                n_pack += 1
            for k, v in o.items():
                if k.endswith("_ar"):
                    if v not in AR.values() and v not in sum(AR_LINES.values(), []):
                        raise SystemExit("Arabic quote not in the source dictionary: %s" % v)
                    n_ar += 1
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(key)
    print("key verified: %d ADD-03 quotes on their pages, %d pack quotes verbatim, %d Arabic strings "
          "match the image source" % (n_add, n_pack, n_ar))


def main():
    for name, want in PINNED_FONTS.items():
        got = hashlib.sha256(open(FREEFONT + name, "rb").read()).hexdigest()
        if got != want:
            raise SystemExit("unexpected %s; output would not be reproducible" % name)
    if pymupdf.VersionBind != PINNED_VERSIONS["pymupdf"] or np.__version__ != PINNED_VERSIONS["numpy"]:
        raise SystemExit("pinned versions: %r" % PINNED_VERSIONS)
    args = list(sys.argv[1:])
    pack, key = None, None
    if "--check" in args:
        i = args.index("--check")
        pack = args[i + 1]
        del args[i:i + 2]
    if "--verify-key" in args:
        i = args.index("--verify-key")
        key = args[i + 1]
        del args[i:i + 2]
    out = args[0] if args else "ADD-03_Addendum_No_3.pdf"
    if pack:
        check(pack)
    image_raw = table_8_1_image()
    image_name = "FormXob." + hashlib.md5(image_raw).hexdigest()
    n = build_pdf(addendum3(image_name), "Addendum No. 3", out, META, image_raw, image_name, DOC_ID)
    pages = self_check(out)
    if key:
        if not pack:
            raise SystemExit("--verify-key needs --check <pack_dir>")
        verify_key(key, pages, pack)
    print("pages: %d" % n)


if __name__ == "__main__":
    main()
