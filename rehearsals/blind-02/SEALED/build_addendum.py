#!/usr/bin/env python3
"""Builder for ADD-03_Addendum_No_3.pdf (blind rehearsal 02 input).

Draws an "Addendum No. 3" to tender NUPA/ISTP/2026/014 in the page furniture
and typography of the issued Addenda Nos. 1 and 2: A4, Base-14 Type1 fonts
(Helvetica, Helvetica-Bold, Times-Roman, Times-Bold, WinAnsiEncoding, not
embedded), text layer only (no images).  Geometry was measured from ADD-01 and
ADD-02 with PyMuPDF (get_text('dict'), get_drawings() and the raw content
streams).  The content streams are written directly and the file is assembled
with PyMuPDF; the output is byte-for-byte deterministic.

Usage:  python build_addendum.py <output.pdf>
"""
import re
import sys

import pymupdf

# --------------------------------------------------------------------------
# Page geometry (points).  "td" = top-down coordinate as reported by PyMuPDF.
# --------------------------------------------------------------------------
PAGE_W, PAGE_H = 595.2756, 841.8898
FRAME_L, FRAME_R = 56.69291, 538.5827          # rules, cover band, full-width tables
PARA_L, PARA_R = 62.69291, 532.5827            # paragraph box (frame padding 6)
INSET_L, INSET_R = 70.86614, 524.4094          # inset tables (Table 1-1 / 2-2 style)
CONTENT_TOP = 68.36218                         # td of the first flowable on a page
CONTENT_BOTTOM = 779.2                         # td limit of flowables
HANG = 36.85039                                # provision hanging indent
QUOTE_FIRST = 36.85039                         # quoted clause: first-line indent
QUOTE_REST = 62.3622                           # quoted clause: continuation indent
BREAK_TOL = 1.0                                # overflow tolerated before a line break
HR_WIDTH = 147.4016                            # short rule above table notes

INK = ".101961 .101961 .101961"                # #1a1a1a
HDR_TXT = ".352941 .352941 .352941"            # #5a5a5a header / footer text
RULE = ".721569 .721569 .721569"               # #b8b8b8 rules and grid
COVER_FILL = ".164706 .164706 .164706"         # #2a2a2a cover band
THEAD_FILL = ".227451 .227451 .227451"         # #3a3a3a table header band

FONTS = [("F1", "Helvetica"), ("F2", "Helvetica-Bold"),
         ("F3", "Times-Roman"), ("F4", "Times-Bold")]
FONTOBJ = {k: pymupdf.Font(v) for k, v in FONTS}
REG, BOLD = "F3", "F4"


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
    """Greedy line breaking; prefix = unbreakable leading pieces."""
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
    """kind: body | prov | quote | head | proj | caption | note"""

    STYLES = {
        "body": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "prov": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "quote": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "head": dict(size=13, lead=16, reg="F2", bold="F2", justify=False),
        "proj": dict(size=10.5, lead=13, reg="F2", bold="F2", justify=False),
        "caption": dict(size=8.5, lead=11, reg="F2", bold="F2", justify=False),
        "note": dict(size=7.2, lead=9, reg=REG, bold=BOLD, justify=True),
    }

    def __init__(self, kind, markup, num=None):
        self.kind, self.markup, self.num = kind, markup, num
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
        elif kind == "note" and num:
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
    """Ruled table with a dark header band.  Splits across pages with the
    header repeated (as the clarification tables in ADD-01/02 do)."""
    SIZE, LEAD, PAD_T, PAD_B, PAD_X = 8.2, 10.4, 3.5, 3.5, 4.0

    def __init__(self, cols, head, rows, bold_rows=()):
        self.cols, self.head = cols, head
        self.rows = []
        for ri, r in enumerate(rows):
            cells = []
            for ci, txt in enumerate(r):
                avail = cols[ci + 1] - cols[ci] - 2 * self.PAD_X
                f = BOLD if ri in bold_rows else REG
                runs = parse_runs(txt, self.SIZE, f, BOLD)
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
    COLS = [56.69291, 90.70866, 300.4724, 538.5827]

    def __init__(self, rows):
        super().__init__(self.COLS, ["No", "Bidder question", "Authority response"], rows)


class HRule:
    """Short centred rule between a table and its notes."""
    kind = "hr"
    height = 1.0

    def draw(self, top):
        x0 = (PAGE_W - HR_WIDTH) / 2
        return "q 1 J 1 j %s RG .5 w n %s %s m %s %s l S Q" % (
            INK, fmt(x0), fmt(Y(top)), fmt(x0 + HR_WIDTH), fmt(Y(top)))


class PageBreak:
    kind = "break"
    height = 0.0


def kind_of(fl):
    if isinstance(fl, Cover):
        return "cover"
    if isinstance(fl, Grid):
        return "table"
    return fl.kind


# Vertical gaps (bottom of previous flowable -> top of next), measured on ADD-01/02.
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
    if nxt == "caption":
        return 17.0
    if prev == "caption":
        return 3.0
    if nxt == "hr":
        return 3.0
    if prev == "hr" or (prev == "note" and nxt == "note"):
        return 0.0
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
        if k in ("head", "caption") and i + 1 < len(flowables):      # keep with next
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
    fd = doc.get_new_xref()
    doc.update_object(fd, "<<" + "".join("/%s %d 0 R" % (n, x) for n, x in font_xrefs.items()) + ">>")
    for pno, chunks in enumerate(pages, start=1):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        stream = furniture(header_left, pno) + "\n" + "\n".join(chunks) + "\n"
        cx = doc.get_new_xref()
        doc.update_object(cx, "<<>>")
        doc.update_stream(cx, stream.encode("latin-1"))
        doc.xref_set_key(page.xref, "Contents", "%d 0 R" % cx)
        doc.xref_set_key(page.xref, "Resources",
                         "<</Font %d 0 R/ProcSet[/PDF/Text/ImageB/ImageC/ImageI]>>" % fd)
    doc.set_metadata(metadata)
    doc.save(out_path, garbage=3, deflate=True, no_new_id=True)
    return len(pages)


# --------------------------------------------------------------------------
# Content of Addendum No. 3
# --------------------------------------------------------------------------
LQ, RQ = "‘", "’"


def q(s, bold=False):
    return LQ + ("<b>%s</b>" % s if bold else s) + RQ


def addendum3():
    F = []
    F.append(Cover("3", "Issued 3 November 2026", "Tender NUPA/ISTP/2026/014"))
    F.append(Para("proj", "Wadi Sirhan Independent Sewage Treatment Plant"))
    F.append(Para("body",
        "This Addendum amends the time for receipt of Proposals and the submission address, introduces "
        "registration of the persons delivering Proposals, extends the Proposal validity period, removes the "
        "model audit opinion from the Proposal, re-letters Volume I Clause 9.1, amends Volume II Clauses 3.5, "
        "4.4 and 8.4, reissues Volume II Table 2-2, and responds to clarification requests 15 to 21. The "
        "Proposal Due Date is unchanged."))
    F.append(Para("body",
        "This Addendum forms part of the RFP Documents and takes precedence in accordance with Volume I Clause "
        "3.2. Bidders shall acknowledge receipt in Form 4-A. All other terms of the RFP Documents remain unchanged."))

    # 1 -------------------------------------------------------------------
    F.append(Para("head", "1. RECITALS"))
    F.append(Para("prov", "This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda "
                          "Nos. 1 and 2 in accordance with Volume I Clause 3.2.", "1.1"))
    F.append(Para("prov", "Clarification request 18 was withdrawn by the Bidder that submitted it and is not "
                          "answered.", "1.2"))

    # 2 -------------------------------------------------------------------
    F.append(Para("head", "2. TIME AND PLACE FOR RECEIPT OF PROPOSALS"))
    F.append(Para("prov", "In Volume I Clause 6.1, as amended by Addendum No. 1 Section 2.1, %s is deleted and "
                          "%s is substituted. The date of Thursday 26 November 2026 is not changed."
                  % (q("14:00 hours Riyadh time"), q("11:00 hours Riyadh time", True)), "2.1"))
    F.append(Para("prov", "The second sentence of Section 2.1 of Addendum No. 1 (%s) ceases to have effect."
                  % q("The time of 14:00 Riyadh time is unchanged."), "2.2"))
    F.append(Para("prov", "Volume I Appendix 3 is deleted and replaced by the following: %s"
                  % q("Tender Box 2, First Floor, Northern Utilities Procurement Authority, <b>Administrative "
                      "Building A</b>, Sakaka. Marked: “NUPA/ISTP/2026/014 — NOT TO BE OPENED BEFORE 11:00 ON "
                      "THE PROPOSAL DUE DATE”."), "2.3"))
    F.append(Para("prov", "The following new Clause 6.8 is <b>inserted</b> in Volume I after Clause 6.7:", "2.4"))
    F.append(Para("quote", "Each Bidder shall, not later than <b>five (5) Working Days before the Proposal Due "
                           "Date</b>, register through the Portal the names and identity document numbers of not "
                           "more than two (2) representatives who will deliver its Proposal. Access to "
                           "Administrative Building A will be refused to any person who is not so registered. A "
                           "Proposal that is not received by the time stated in Clause 6.1 for that reason shall "
                           "be treated as a late Proposal under Clause 6.6." + RQ, "6.8"))

    # 3 -------------------------------------------------------------------
    F.append(Para("head", "3. PROPOSAL VALIDITY"))
    F.append(Para("prov", "In Volume I Clause 7.1, %s is deleted and %s is substituted."
                  % (q("one hundred and fifty (150) days"), q("one hundred and eighty (180) days", True)), "3.1"))
    F.append(Para("prov", "In Volume I Clause 6.3, %s is deleted and %s is substituted."
                  % (q("one hundred and eighty (180) days"), q("two hundred and ten (210) days", True)), "3.2"))
    F.append(Para("prov", "Paragraph 2 of Form 4-A shall be read accordingly.", "3.3"))

    # 4 -------------------------------------------------------------------
    F.append(Para("head", "4. FINANCIAL MODEL AUDIT OPINION"))
    F.append(Para("prov", "In Volume I Clause 10.3, the words %s are <b>deleted</b>. No model audit opinion is "
                          "required with the Proposal."
                  % q(", and shall be accompanied by an opinion from an independent model auditor addressed "
                      "to the Authority"), "4.1"))
    F.append(Para("prov", "The following new Clause 12.5 is <b>inserted</b> in Volume I after Clause 12.4:", "4.2"))
    F.append(Para("quote", "The Preferred Bidder shall deliver to the Authority, not later than <b>forty-five "
                           "(45) days after the Preferred Bidder Notification</b>, an opinion from an independent "
                           "model auditor on the Financial Model, addressed to the Authority." + RQ, "12.5"))
    F.append(Para("prov", "In Form 4-F, the rows %s and %s are deleted."
                  % (q("Model auditor"), q("Date of model audit opinion")), "4.3"))

    # 5 -------------------------------------------------------------------
    F.append(Para("head", "5. AMENDMENTS TO VOLUME II CLAUSES 3.5, 4.4 AND 8.4"))
    F.append(Para("prov", "In Volume II Clause 3.5, %s is deleted and %s is substituted. The daytime limit is "
                          "unchanged." % (q("45 dB(A) by night"), q("40 dB(A) by night", True)), "5.1"))
    F.append(Para("prov", "Section 4.1 of Addendum No. 2 is <b>revoked</b>. The period in Volume II Clause 4.4 is "
                          "seventy-two (72) hours, as originally issued.", "5.2"))
    F.append(Para("prov", "In Volume II Clause 8.4, %s is deleted and %s is substituted, and the second sentence "
                          "is deleted and replaced by: %s"
                  % (q("22% dry solids"), q("25% dry solids", True),
                     q("No sludge shall be disposed of to landfill without the Authority's prior written "
                       "consent.", True)), "5.3"))

    # 6 -------------------------------------------------------------------
    F.append(Para("head", "6. REISSUED VOLUME II TABLE 2-2"))
    F.append(Para("prov", "Table 2-2 of Volume II is deleted and replaced by Table 2-2 (revised) at Appendix A to "
                          "this Addendum, including the Notes to that Table. The principal changes are an increase "
                          "in the influent nitrogen concentrations, the addition of ammonia nitrogen and a "
                          "reduction in the minimum design temperature.", "6.1"))
    F.append(Para("prov", "Bidders shall reflect Table 2-2 (revised) in the process design submitted under Volume "
                          "II Section 3.", "6.2"))

    # 7 -------------------------------------------------------------------
    F.append(Para("head", "7. RE-LETTERING OF VOLUME I CLAUSE 9.1"))
    F.append(Para("prov", "Following the insertion of Form 4-G by Section 7.1 of Addendum No. 2, the items of "
                          "Volume I Clause 9.1 are re-lettered: Form 4-G is item <b>(f)</b>, and former items (f) "
                          "to (i) become items <b>(g) to (j)</b> respectively. The numbered dividers in Envelope A "
                          "shall follow the re-lettered list.", "7.1"))
    F.append(Para("prov", "The Index of Forms in Volume IV is amended by adding, after the entry for Form 4-F, an "
                          "entry for Form 4-G with the title %s, Envelope %s and Status %s."
                  % (q("Cybersecurity Compliance Undertaking"), q("A"), q("Mandatory")), "7.2"))

    # 8 -------------------------------------------------------------------
    F.append(Para("head", "8. RESPONSES TO CLARIFICATION REQUESTS 15 TO 21"))
    F.append(QATable([
        ["15",
         "Addendum No. 1 response 3 permits a Bid Bond issued by a licensed branch of a foreign bank. Must "
         "such a Bid Bond also be confirmed by a bank incorporated in the Kingdom?",
         "The response to clarification request 3 in Addendum No. 1 is withdrawn. The Bid Bond shall be "
         "issued by a bank incorporated in the Kingdom that meets the rating requirement in Volume I Clause "
         "6.4. A Bid Bond issued by a branch of a foreign bank, whether or not confirmed, will not be "
         "accepted."],
        ["16",
         "Must the notarised Powers of Attorney required by Volume I Clause 9.1 be legalised where they are "
         "executed outside the Kingdom?",
         "Yes. A Power of Attorney executed outside the Kingdom shall, in addition to notarisation, be "
         "legalised by an embassy or consulate of the Kingdom in the country of execution, or apostilled "
         "where that country is a party to the Apostille Convention. The Powers of Attorney are item (i) of "
         "Volume I Clause 9.1 as re-lettered by Section 7 of this Addendum. A Power of Attorney that does not "
         "comply will be treated as not submitted."],
        ["17",
         "Following response 10 in Addendum No. 2, is any guarantee or other security required in respect "
         "of the proposed O&M Operator?",
         "No. The response to clarification request 10 in Addendum No. 2 is confirmed. Volume I Clause 8.7 "
         "requires a Parent Company Guarantee in respect of the proposed EPC Contractor only."],
        ["18",
         "Withdrawn.",
         "Not answered. See Section 1.2 of this Addendum."],
        ["19",
         "Further to response 7 in Addendum No. 2, will Volume V Clause 3.1 be conformed to Volume I Clause "
         "12.1 so that the twenty-five (25) year term runs from PCOD?",
         "The Authority intends to address the commencement of the term in the execution version of the "
         "Project Agreement. No amendment is made to Volume I or Volume V by this Addendum. A Bidder that "
         "wishes to propose wording may do so in Form 4-E."],
        ["20",
         "Volume I Clause 6.5 requires one electronic copy of the Proposal, but Volume I Clause 10.1 requires "
         "the Financial Model to be placed in Envelope B. How is the Financial Model to be submitted?",
         "The Financial Model shall be submitted on a second, separate encrypted USB media placed in Envelope "
         "B. The electronic copy required by Volume I Clause 6.5 shall contain Envelope A only. The password "
         "for each USB media shall be submitted through the Portal within one (1) hour after the Proposal Due "
         "Date. Commercial information on the Envelope A media will be treated in accordance with Volume I "
         "Clause 6.2."],
        ["21",
         "In view of the changes made by Addenda Nos. 1 and 2, will the Authority extend the Proposal Due "
         "Date?",
         "No. The date for receipt of Proposals is not extended. Bidders' attention is drawn to Section 2 of "
         "this Addendum."],
    ]))

    # Appendix A ----------------------------------------------------------
    F.append(PageBreak())
    F.append(Para("head", "APPENDIX A — REVISED TABLE 2-2"))
    F.append(Para("body", "Table 2-2 of Volume II is reissued below in accordance with Section 6 of this "
                          "Addendum. Bidders shall use this version."))
    F.append(Para("caption", "Table 2-2 (revised) — Design influent characteristics"))
    F.append(Grid([INSET_L, 235.2756, 308.9764, 405.3543, INSET_R],
                  ["Parameter", "Unit", "Average", "Peak (design)"],
                  [["BOD<sub>5</sub>", "mg/l", "320", "480"],
                   ["COD", "mg/l", "640", "950"],
                   ["Total Suspended Solids", "mg/l", "350", "520"],
                   ["Total Nitrogen", "mg/l", "60", "85"],
                   ["Ammonia nitrogen (NH<sub>4</sub>-N)", "mg/l", "42", "62"],
                   ["Total Phosphorus", "mg/l", "9", "16"],
                   ["Temperature", "°C", "24", "34 (max) / 12 (min)"]]))
    F.append(HRule())
    F.append(Para("note", "Notes to Table 2-2 (revised):"))
    F.append(Para("note", "Concentrations are flow-weighted 24-hour composite values measured at the inlet "
                          "works. Peak (design) values are 95th percentile values.", "(1)"))
    F.append(Para("note", "The minimum temperature of 12 °C shall be used for the design of the nitrification "
                          "stage.", "(2)"))
    F.append(Para("note", "Bidders shall submit, as an appendix to the Technical Proposal, a process simulation "
                          "report demonstrating that the effluent quality in Table 2-4, as amended, is achieved "
                          "under the Peak (design) values in this Table at the minimum design temperature. The "
                          "report shall not exceed twenty-five (25) pages and is excluded from the page limit in "
                          "Volume I Clause 9.2. <b>A Technical Proposal that does not include the report will be "
                          "awarded no marks under criterion A of Table 1-1 (revised).</b>", "(3)"))
    F.append(Para("note", "In Volume II Clause 2.3, %s is deleted and %s is substituted."
                  % (q("50% of nominal capacity"), q("25% of nominal capacity", True)), "(4)"))
    return F


META = {"title": "(anonymous)", "author": "(anonymous)", "subject": "(unspecified)",
        "creator": "(unspecified)", "keywords": "", "producer": "",
        "creationDate": "D:20261103070000+00'00'", "modDate": "D:20261103070000+00'00'"}

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "ADD-03_Addendum_No_3.pdf"
    n = build_pdf(addendum3(), "Addendum No. 3", out, META)
    print("pages:", n)
