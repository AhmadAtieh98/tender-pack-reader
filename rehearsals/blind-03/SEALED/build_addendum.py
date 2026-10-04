#!/usr/bin/env python3
"""Builder for ADD-03_Addendum_No_3.pdf (blind rehearsal 03 input).

Draws an "Addendum No. 3" to tender NUPA/ISTP/2026/014 in the page furniture
and typography of the issued Addenda Nos. 1 and 2: A4, Base-14 Type1 fonts
(Helvetica, Helvetica-Bold, Times-Roman, Times-Bold, WinAnsiEncoding, not
embedded) for all Latin text.  The Arabic text of the Form 4-C amendment is set
in an embedded subset of GNU FreeSerif (Type0 / Identity-H) because no Base-14
font carries Arabic; it is shaped here (presentation forms, lam-alef ligatures),
drawn right-to-left in logical order, and given a ToUnicode CMap that maps every
glyph back to the base Arabic letters, so text extraction returns ordinary
logical-order Arabic.  No images.

Geometry was measured from ADD-01 and ADD-02 with PyMuPDF (raw content streams);
the layout engine follows the technique of the blind-02 builder.  The output is
byte-for-byte deterministic (fixed dates, no random IDs).

Usage:  python build_addendum.py <output.pdf>
"""
import hashlib
import re
import sys

import pymupdf

# --------------------------------------------------------------------------
# Page geometry (points).  "td" = top-down coordinate as reported by PyMuPDF.
# --------------------------------------------------------------------------
PAGE_W, PAGE_H = 595.2756, 841.8898
FRAME_L, FRAME_R = 56.69291, 538.5827          # rules, cover band, full-width tables
PARA_L, PARA_R = 62.69291, 532.5827            # paragraph box (frame padding 6)
CONTENT_TOP = 68.36218                         # td of the first flowable on a page
CONTENT_BOTTOM = 779.2                         # td limit of flowables
HANG = 36.85039                                # provision hanging indent
QUOTE_FIRST = 36.85039                         # quoted clause: first-line indent
QUOTE_REST = 62.3622                           # quoted clause: continuation indent
BREAK_TOL = 1.0

INK = ".101961 .101961 .101961"                # #1a1a1a
HDR_TXT = ".352941 .352941 .352941"            # #5a5a5a header / footer text
RULE = ".721569 .721569 .721569"               # #b8b8b8 rules and grid
COVER_FILL = ".164706 .164706 .164706"         # #2a2a2a cover band
THEAD_FILL = ".227451 .227451 .227451"         # #3a3a3a table header band

FONTS = [("F1", "Helvetica"), ("F2", "Helvetica-Bold"),
         ("F3", "Times-Roman"), ("F4", "Times-Bold")]
FONTOBJ = {k: pymupdf.Font(v) for k, v in FONTS}
REG, BOLD = "F3", "F4"

AR_FONT_FILE = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
AR_FONT_SHA256 = "c57bf5de095af4e070c2acb5bce634316409ed4203b5098f4fdadb691dc7b3d2"
AR_RES = "F5"


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
# Rich text: markup with <b>..</b>, <sup>..</sup> and <sub>..</sub>
# --------------------------------------------------------------------------
def parse_runs(markup, size, reg=REG, bold=BOLD):
    runs, b, pos = [], False, 0
    for tok in re.split(r"(</?b>|</?sup>|</?sub>)", markup):
        if tok == "<b>":
            b = True
        elif tok == "</b>":
            b = False
        elif tok == "<sup>":
            pos = 1
        elif tok == "<sub>":
            pos = -1
        elif tok in ("</sup>", "</sub>"):
            pos = 0
        elif tok:
            f = bold if b else reg
            if pos:
                runs.append((tok, f, round(size * 0.8, 4), round(pos * size * 0.5, 4)))
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
# Arabic: shaping to presentation forms + right-to-left placement
# --------------------------------------------------------------------------
AR_FORMS = {  # base: (isolated, final[, initial, medial])
    0x0621: (0xFE80,), 0x0622: (0xFE81, 0xFE82), 0x0623: (0xFE83, 0xFE84),
    0x0624: (0xFE85, 0xFE86), 0x0625: (0xFE87, 0xFE88),
    0x0626: (0xFE89, 0xFE8A, 0xFE8B, 0xFE8C), 0x0627: (0xFE8D, 0xFE8E),
    0x0628: (0xFE8F, 0xFE90, 0xFE91, 0xFE92), 0x0629: (0xFE93, 0xFE94),
    0x062A: (0xFE95, 0xFE96, 0xFE97, 0xFE98), 0x062B: (0xFE99, 0xFE9A, 0xFE9B, 0xFE9C),
    0x062C: (0xFE9D, 0xFE9E, 0xFE9F, 0xFEA0), 0x062D: (0xFEA1, 0xFEA2, 0xFEA3, 0xFEA4),
    0x062E: (0xFEA5, 0xFEA6, 0xFEA7, 0xFEA8), 0x062F: (0xFEA9, 0xFEAA),
    0x0630: (0xFEAB, 0xFEAC), 0x0631: (0xFEAD, 0xFEAE), 0x0632: (0xFEAF, 0xFEB0),
    0x0633: (0xFEB1, 0xFEB2, 0xFEB3, 0xFEB4), 0x0634: (0xFEB5, 0xFEB6, 0xFEB7, 0xFEB8),
    0x0635: (0xFEB9, 0xFEBA, 0xFEBB, 0xFEBC), 0x0636: (0xFEBD, 0xFEBE, 0xFEBF, 0xFEC0),
    0x0637: (0xFEC1, 0xFEC2, 0xFEC3, 0xFEC4), 0x0638: (0xFEC5, 0xFEC6, 0xFEC7, 0xFEC8),
    0x0639: (0xFEC9, 0xFECA, 0xFECB, 0xFECC), 0x063A: (0xFECD, 0xFECE, 0xFECF, 0xFED0),
    0x0641: (0xFED1, 0xFED2, 0xFED3, 0xFED4), 0x0642: (0xFED5, 0xFED6, 0xFED7, 0xFED8),
    0x0643: (0xFED9, 0xFEDA, 0xFEDB, 0xFEDC), 0x0644: (0xFEDD, 0xFEDE, 0xFEDF, 0xFEE0),
    0x0645: (0xFEE1, 0xFEE2, 0xFEE3, 0xFEE4), 0x0646: (0xFEE5, 0xFEE6, 0xFEE7, 0xFEE8),
    0x0647: (0xFEE9, 0xFEEA, 0xFEEB, 0xFEEC), 0x0648: (0xFEED, 0xFEEE),
    0x0649: (0xFEEF, 0xFEF0), 0x064A: (0xFEF1, 0xFEF2, 0xFEF3, 0xFEF4),
}
AR_LAMALEF = {0x0622: (0xFEF5, 0xFEF6), 0x0623: (0xFEF7, 0xFEF8),
              0x0625: (0xFEF9, 0xFEFA), 0x0627: (0xFEFB, 0xFEFC)}
AR_MARKS = set(range(0x064B, 0x0653))
AR_ALLOWED_OTHER = set(map(ord, " :.،"))


def ar_jtype(cp):
    if cp in AR_MARKS:
        return "T"
    f = AR_FORMS.get(cp)
    if f is None:
        return "U"
    return {4: "D", 2: "R"}.get(len(f), "U")


def ar_shape(text):
    """Logical-order list of (glyph codepoint, source text, is_mark)."""
    cps = [ord(c) for c in text]
    for cp in cps:
        if not (cp in AR_FORMS or cp in AR_MARKS or cp in AR_ALLOWED_OTHER):
            raise ValueError("unsupported character U+%04X" % cp)
    n = len(cps)

    def neighbour(i, step):
        j = i + step
        while 0 <= j < n and ar_jtype(cps[j]) == "T":
            j += step
        return (j, ar_jtype(cps[j])) if 0 <= j < n else (j, "U")

    out, i, lig_tail = [], 0, set()
    while i < n:
        cp = cps[i]
        t = ar_jtype(cp)
        if t in ("T", "U"):
            out.append((cp, chr(cp), t == "T"))
            i += 1
            continue
        pj, pt = neighbour(i, -1)
        joins_prev = pt == "D" and pj not in lig_tail
        if cp == 0x0644 and i + 1 < n and cps[i + 1] in AR_LAMALEF:
            lig = AR_LAMALEF[cps[i + 1]]
            out.append((lig[1] if joins_prev else lig[0], text[i:i + 2], False))
            lig_tail.add(i + 1)
            i += 2
            continue
        nj, nt = neighbour(i, +1)
        joins_next = t == "D" and nt in ("D", "R")
        f = AR_FORMS[cp]
        g = f[3] if (joins_prev and joins_next) else f[1] if joins_prev else \
            f[2] if joins_next else f[0]
        out.append((g, chr(cp), False))
        i += 1
    return out


AR_FONT = None
AR_TOUNICODE = {}      # gid -> source text (base letters), filled while laying out


def ar_font():
    global AR_FONT
    if AR_FONT is None:
        data = open(AR_FONT_FILE, "rb").read()
        if hashlib.sha256(data).hexdigest() != AR_FONT_SHA256:
            raise SystemExit("unexpected FreeSerif.ttf; output would not be reproducible")
        AR_FONT = pymupdf.Font(fontfile=AR_FONT_FILE)
    return AR_FONT


class Arabic:
    """A right-to-left Arabic block, indented 36.85 pt on both sides."""
    kind = "arabic"
    SIZE, LEAD = 10.5, 15.0

    def __init__(self, text):
        F = ar_font()
        self.x_right = PARA_R - QUOTE_FIRST
        avail = self.x_right - (PARA_L + QUOTE_FIRST)
        words, cur = [], []
        for g in ar_shape(text):
            if g[0] == 0x20:
                words.append(cur)
                cur = []
            else:
                cur.append(g)
        words.append(cur)
        adv = lambda g: 0.0 if g[2] else F.glyph_advance(g[0]) * self.SIZE
        sp = (0x20, " ", False)
        lines, line, lw = [], [], 0.0
        for w in words:
            ww = sum(adv(g) for g in w)
            add = ww + (adv(sp) if line else 0)
            if line and lw + add > avail:
                lines.append(line)
                line, lw = list(w), ww
            else:
                line += ([sp] if line else []) + w
                lw += add
        lines.append(line)
        self.lines, self.adv = lines, adv
        self.height = len(lines) * self.LEAD

    def draw(self, top):
        F = ar_font()
        o = []
        for li, line in enumerate(self.lines):
            base = Y(top + self.SIZE * 1.1 + li * self.LEAD)
            o.append("BT /%s %s Tf %s rg" % (AR_RES, fmt(self.SIZE), INK))
            x = self.x_right
            xbase = x
            for cp, src, mark in line:
                gid = F.has_glyph(cp)
                if not gid:
                    raise SystemExit("missing glyph U+%04X" % cp)
                prev = AR_TOUNICODE.setdefault(gid, src)
                if prev != src:
                    raise SystemExit("glyph %d maps to two texts" % gid)
                if mark:
                    o.append("1 0 0 1 %s %s Tm <%04X> Tj" % (fmt(xbase), fmt(base), gid))
                    continue
                x -= self.adv((cp, src, mark))
                xbase = x
                o.append("1 0 0 1 %s %s Tm <%04X> Tj" % (fmt(x), fmt(base), gid))
            o.append("ET")
        return "\n".join(o)


def tounicode_cmap(mapping):
    entries = sorted(mapping.items())
    o = ["/CIDInit /ProcSet findresource begin", "12 dict begin", "begincmap",
         "/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def",
         "/CMapName /Adobe-Identity-UCS def", "/CMapType 2 def",
         "1 begincodespacerange", "<0000> <FFFF>", "endcodespacerange"]
    for k in range(0, len(entries), 100):
        chunk = entries[k:k + 100]
        o.append("%d beginbfchar" % len(chunk))
        for gid, txt in chunk:
            o.append("<%04X> <%s>" % (gid, txt.encode("utf-16-be").hex().upper()))
        o.append("endbfchar")
    o += ["endcmap", "CMapName currentdict /CMap defineresource pop", "end", "end"]
    return "\n".join(o).encode("ascii")


# --------------------------------------------------------------------------
# Flowables
# --------------------------------------------------------------------------
class Para:
    """kind: body | prov | quote | quote2 | head | proj | formtitle"""

    STYLES = {
        "body": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "prov": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "cont": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "quote": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "quote2": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "head": dict(size=13, lead=16, reg="F2", bold="F2", justify=False),
        "proj": dict(size=10.5, lead=13, reg="F2", bold="F2", justify=False),
        "formtitle": dict(size=10.5, lead=13, reg="F2", bold="F2", justify=False),
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


class FormGTable(Grid):
    COLS = [56.69291, 96.37795, 459.2126, 538.5827]       # ADD-02 Form 4-G grid

    def __init__(self, rows):
        super().__init__(self.COLS, ["Item", "Undertaking", "Confirmed"], rows)


class PageBreak:
    kind = "break"
    height = 0.0


def kind_of(fl):
    return fl.kind


# Vertical gaps (bottom of previous flowable -> top of next), measured on ADD-01/02.
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
    if isinstance(fl, Arabic):
        return fl.height                      # Arabic blocks are never split
    if isinstance(fl, Para):
        return fl.lead * min(2, len(fl.lines))
    return fl.height


def layout(flowables):
    pages, cur, top, prev = [], [], CONTENT_TOP, None
    i = 0
    started = False
    while i < len(flowables):
        fl = flowables[i]
        k = kind_of(fl)
        if k == "break":
            pages.append(cur)
            cur, top, prev = [], CONTENT_TOP, None
            i += 1
            continue
        t = top + (gap(prev, k) if prev is not None else 0.0)
        if not started:
            t = CONTENT_TOP + 6.0              # 6 pt spacer above the cover band
            started = True
        if isinstance(fl, Grid):
            start = getattr(fl, "_next", 0)
            n, h = fl.chunk(start, CONTENT_BOTTOM - t)
            if n == 0:
                pages.append(cur)
                cur, top, prev = [], CONTENT_TOP, None
                continue
            s, h = fl.draw_rows(t, start, n)
            cur.append(s)
            fl._next = start + n
            if fl._next < len(fl.rows):
                pages.append(cur)
                cur, top, prev = [], CONTENT_TOP, None
                continue
            top, prev = t + h, k
            i += 1
            continue
        need = fl.height
        keep = k in ("head", "formtitle") or getattr(fl, "keep_next", False)
        if keep and i + 1 < len(flowables):
            nx = flowables[i + 1]
            need = fl.height + gap(k, kind_of(nx)) + first_height(nx)
        if prev is not None and t + need > CONTENT_BOTTOM:
            pages.append(cur)
            cur, top, prev = [], CONTENT_TOP, None
            continue
        cur.append(fl.draw(t))
        top, prev = t + fl.height, k
        i += 1
    if cur:
        pages.append(cur)
    return pages


def build_pdf(flowables, header_left, out_path, metadata):
    pages = layout(flowables)
    doc = pymupdf.open()
    font_xrefs = {}
    for name, base in FONTS:
        x = doc.get_new_xref()
        doc.update_object(x, "<</BaseFont/%s/Encoding/WinAnsiEncoding/Name/%s/Subtype/Type1/Type/Font>>"
                          % (base, name))
        font_xrefs[name] = x
    page_objs = []
    for pno, chunks in enumerate(pages, start=1):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        stream = furniture(header_left, pno) + "\n" + "\n".join(chunks) + "\n"
        cx = doc.get_new_xref()
        doc.update_object(cx, "<<>>")
        doc.update_stream(cx, stream.encode("latin-1"))
        doc.xref_set_key(page.xref, "Contents", "%d 0 R" % cx)
        page_objs.append(page.xref)
    # Embedded Arabic font (Type0, Identity-H), created through page 1.
    ar_xref = doc[0].insert_font(fontname=AR_RES, fontfile=AR_FONT_FILE)
    font_xrefs[AR_RES] = ar_xref
    fd = doc.get_new_xref()
    doc.update_object(fd, "<<" + "".join("/%s %d 0 R" % (n, x) for n, x in font_xrefs.items()) + ">>")
    for px in page_objs:
        doc.xref_set_key(px, "Resources", "<</Font %d 0 R/ProcSet[/PDF/Text/ImageB/ImageC/ImageI]>>" % fd)
    doc.subset_fonts()
    tu = doc.xref_get_key(ar_xref, "ToUnicode")
    if tu[0] != "xref":
        raise SystemExit("no ToUnicode on the Arabic font")
    doc.update_stream(int(tu[1].split()[0]), tounicode_cmap(AR_TOUNICODE))
    doc.set_metadata(metadata)
    doc.save(out_path, garbage=3, deflate=True, no_new_id=True)
    return len(pages)


# --------------------------------------------------------------------------
# Content of Addendum No. 3
# --------------------------------------------------------------------------
LQ, RQ = "‘", "’"


def q(s, bold=False):
    return LQ + ("<b>%s</b>" % s if bold else s) + RQ


AR_OLD_4 = ("رابعاً: أن جميع المعلومات المقدمة في هذا العرض صحيحة وكاملة، وندرك أن أي بيان غير "
            "صحيح يؤدي إلى استبعاد العرض.")
AR_NEW_4 = ("رابعاً: أن جميع المعلومات المقدمة في هذا العرض صحيحة وكاملة، ونتعهد بإخطار الهيئة "
            "عبر البوابة خلال ثلاثة أيام عمل من تاريخ علمنا بأي تغيير يطرأ على أي من تلك المعلومات "
            "قبل صدور إشعار مقدم العرض المفضل، وندرك أن أي بيان غير صحيح أو أي إخلال بهذا التعهد "
            "يؤدي إلى استبعاد العرض.")

SIG_BIDDER = ("Signed for and on behalf of the Bidder: _______________________ Name: "
              "_______________________ Date: ____________")
SIG_OM = ("Countersigned for and on behalf of the proposed O&M Operator: _______________________ "
          "Name: _______________________ Date: ____________")


def addendum3():
    F = []
    F.append(Cover("3", "Issued 1 November 2026", "Tender NUPA/ISTP/2026/014"))
    F.append(Para("proj", "Wadi Sirhan Independent Sewage Treatment Plant"))
    F.append(Para("body",
        "This Addendum amends the definition of Working Day and notifies a closure of the Authority's "
        "offices, requires the proposed O&M Operator to be a member of the Bidder, replaces the fourth "
        "declaration in Form 4-C, amends Volume II Table 2-4, deletes Volume V Clause 31.4, reissues "
        "Form 4-G, and responds to clarification requests 15 to 19. The closure of the Authority's "
        "offices does not affect any deadline under the RFP Documents."))
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
    F.append(Para("head", "2. WORKING DAYS AND CLOSURE OF THE AUTHORITY'S OFFICES"))
    F.append(Para("prov", "In Volume I Clause 2.4, %s is deleted and %s is substituted. The second sentence of "
                          "Clause 2.4 is unchanged."
                  % (q("other than a day declared a public holiday in the Kingdom"),
                     q("other than a day declared a public holiday in the Kingdom or a day notified by the "
                       "Authority in an Addendum as a day on which its offices are closed", True)), "2.1"))
    F.append(Para("prov", "The Authority's offices will be closed on <b>Sunday 22 November 2026</b>. That day is "
                          "notified for the purposes of Volume I Clause 2.4 as amended by Section 2.1. The Portal "
                          "will remain available on that day.", "2.2"))

    # 3 -------------------------------------------------------------------
    F.append(Para("head", "3. MEMBERSHIP OF THE O&M OPERATOR"))
    F.append(Para("prov", "Volume I Clause 8.8 is amended by adding at the end: %s"
                  % q("The proposed O&M Operator shall be a member of the Bidder and shall hold, from Financial "
                      "Close until the second anniversary of PCOD, not less than ten per cent (10%) of the "
                      "shares in the Project Company.", True), "3.1"))
    F.append(Para("prov", "A Bidder whose proposed O&M Operator is not a member of the Bidder shall apply through "
                          "the Portal for the Authority's consent under Volume I Clause 8.1 to the admission of "
                          "the O&M Operator as a member, not later than <b>four (4) Working Days before the "
                          "Proposal Due Date</b>.", "3.2"))
    F.append(Para("prov", "A Bidder that intends to apply under Section 3.2 shall notify the Authority of that "
                          "intention through the Portal within <b>five (5) Working Days of the date of this "
                          "Addendum</b>.", "3.3"))
    F.append(Para("prov", "If, at any time before the Preferred Bidder Notification, the proposed O&M Operator "
                          "ceases to be a member of the Bidder, the Bidder shall notify the Authority through the "
                          "Portal within two (2) Working Days of that event. Volume I Clause 8.1 applies.", "3.4"))

    # 4 -------------------------------------------------------------------
    F.append(Para("head", "4. AMENDMENT TO FORM 4-C"))
    F.append(Para("prov", "In Form 4-C, the fourth numbered declaration, which as issued reads as follows, is "
                          "deleted:", "4.1", keep_next=True))
    F.append(Arabic(AR_OLD_4))
    F.append(Para("prov", "The following fourth declaration is substituted:", "4.2", keep_next=True))
    F.append(Arabic(AR_NEW_4))
    F.append(Para("prov", "An English translation of the substituted declaration is given below for convenience "
                          "only. The Arabic text governs, in accordance with Volume I Clause 9.4.", "4.3",
                  keep_next=True))
    F.append(Para("quote2",
        LQ + "Fourth: that all the information provided in this Proposal is correct and complete; that we "
        "undertake to notify the Authority through the Portal within three (3) days of the date on which we "
        "become aware of any change to any of that information before the issue of the Preferred Bidder "
        "Notification; and that we understand that any incorrect statement, or any breach of this undertaking, "
        "will lead to the exclusion of the Proposal." + RQ))
    F.append(Para("prov", "Each member of the Bidder shall give the fourth declaration as substituted. A Form 4-C "
                          "that contains the fourth declaration as issued is not a properly executed Form 4-C for "
                          "the purposes of Volume I Clause 9.4.", "4.4"))

    # 5 -------------------------------------------------------------------
    F.append(Para("head", "5. AMENDMENT TO VOLUME II TABLE 2-4"))
    F.append(Para("prov", "In Volume II Table 2-4, in the row for Total Phosphorus (TP), the limit is amended from "
                          "1 mg/l to <b>0.5 mg/l</b>. The unit and the basis of assessment (30-day rolling average) "
                          "are unchanged. All other entries in Table 2-4, including the Total Nitrogen limit as "
                          "amended by Addendum No. 2, are unchanged.", "5.1"))
    F.append(Para("prov", "Bidders shall reflect the amended limit in the process design submitted under Volume II "
                          "Section 3.", "5.2"))

    # 6 -------------------------------------------------------------------
    F.append(Para("head", "6. AMENDMENTS TO VOLUME V"))
    F.append(Para("prov", "In Volume V Clause 29.3, %s is deleted and %s is substituted. The duration of the "
                          "Ramp-Up Period is unchanged."
                  % (q("ninety per cent (90%)"), q("eighty-five per cent (85%)", True)), "6.1"))
    F.append(Para("prov", "Volume V Clause 31.4 is <b>deleted</b> in its entirety. Volume V Clause 39.3, which "
                          "provides for termination for persistent breach in the circumstances described in Clause "
                          "31.4, is also deleted. The remaining Clauses of Volume V are not renumbered.", "6.2"))

    # 7 -------------------------------------------------------------------
    F.append(Para("head", "7. REISSUED FORM 4-G"))
    F.append(Para("prov", "Form 4-G, added to Volume IV by Section 7 of Addendum No. 2, is deleted and replaced by "
                          "the reissued Form 4-G at Appendix A to this Addendum, which provides for its "
                          "countersignature by the proposed O&M Operator. Bidders shall use the reissued Form.",
                  "7.1"))
    F.append(Para("prov", "Section 7.2 of Addendum No. 2 applies to the reissued Form 4-G. <b>A Form 4-G that is "
                          "not countersigned by the proposed O&M Operator shall be treated as not submitted.</b>",
                  "7.2"))

    # 8 -------------------------------------------------------------------
    F.append(Para("head", "8. RESPONSES TO CLARIFICATION REQUESTS 15 TO 19"))
    F.append(QATable([
        ["15",
         "Response 9 in Addendum No. 2 states that an English translation of Form 4-C may be attached for "
         "convenience. Must a translation be attached where the member is incorporated outside the Kingdom?",
         "Yes. The response to clarification request 9 in Addendum No. 2 is amended by adding at the end: "
         "‘A member incorporated outside the Kingdom shall attach an English translation to its Form 4-C.’ "
         "The Arabic text of Form 4-C governs in accordance with Volume I Clause 9.4."],
        ["16",
         "May construction water be abstracted from the local aquifer if it is treated on site before use?",
         "No. Volume II Clause 9.4 applies. Construction water shall be sourced from tankered supply or "
         "treated effluent and shall not be abstracted from the local aquifer, whether or not it is treated "
         "before use."],
        ["17",
         "Volume I Clause 8.1 requires the Authority's prior written consent to any change in the composition "
         "of a prequalified consortium. By when must a Bidder apply for consent to admit an additional member?",
         "Bidders are referred to Section 3 of this Addendum. An application for consent to the admission of "
         "the proposed O&M Operator as a member of a Bidder shall be submitted through the Portal not later "
         "than Sunday 22 November 2026."],
        ["18",
         "Under Volume V Clause 31.4, does the rolling ninety (90) day period restart once the Authority has "
         "approved a remediation plan?",
         "Volume V Clause 31.4 is deleted by Section 6.2 of this Addendum. The question does not arise."],
        ["19",
         "May the lead member give the declarations in Form 4-C on behalf of all members of the Bidder?",
         "No. Volume I Clause 9.4 requires a complete and properly executed Form 4-C for each member of the "
         "Bidder, signed and stamped by an authorised signatory of that member."],
    ]))

    # Appendix A ----------------------------------------------------------
    F.append(PageBreak())
    F.append(Para("head", "APPENDIX A — REISSUED FORM 4-G"))
    F.append(Para("body", "Form 4-G is reissued below in accordance with Section 7 of this Addendum. Bidders "
                          "shall use this version."))
    F.append(Para("formtitle", "FORM 4-G — CYBERSECURITY COMPLIANCE UNDERTAKING"))
    F.append(FormGTable([
        ["1", "The operational technology environment will be segregated from any business network in "
              "accordance with Volume II Clause 6.2.", "Yes / No"],
        ["2", "An information security management system covering the operational technology environment will "
              "be implemented before commissioning.", "Yes / No"],
        ["3", "A named accountable security officer will be appointed for the concession period.", "Yes / No"],
        ["4", "Security incidents affecting the Facility will be notified to the Authority within twenty-four "
              "(24) hours of detection.", "Yes / No"],
        ["5", "An independent penetration test of the operational technology environment will be carried out "
              "annually and the report provided to the Authority.", "Yes / No"],
        ["6", "Remote access to the control system will require multi-factor authentication and will be "
              "logged.", "Yes / No"],
        ["7", "Personnel with privileged or remote access to the control system will be subject to security "
              "screening approved by the Authority before access is granted.", "Yes / No"],
    ]))
    F.append(Para("body", SIG_BIDDER))
    F.append(Para("body", SIG_OM))
    return F


META = {"title": "(anonymous)", "author": "(anonymous)", "subject": "(unspecified)",
        "creator": "(unspecified)", "keywords": "", "producer": "",
        "creationDate": "D:20261101070000+00'00'", "modDate": "D:20261101070000+00'00'"}

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "ADD-03_Addendum_No_3.pdf"
    n = build_pdf(addendum3(), "Addendum No. 3", out, META)
    print("pages:", n)
