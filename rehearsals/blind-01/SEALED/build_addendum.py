#!/usr/bin/env python3
"""Builder for ADD-03_Addendum_No_3.pdf (blind test fixture).

Reproduces the page furniture and typography of ADD-01 / ADD-02 (ReportLab
output, A4, Base-14 Type1 fonts Helvetica / Helvetica-Bold / Times-Roman /
Times-Bold with WinAnsiEncoding, not embedded) by writing the PDF content
streams directly and assembling the file with PyMuPDF.  All geometry below was
measured from ADD-01 / ADD-02 with PyMuPDF (get_text('dict'), get_drawings(),
raw content streams).

Usage:  python build_addendum.py <output.pdf>
"""
import re
import sys

import pymupdf

# --------------------------------------------------------------------------
# Page geometry (points).  "td" = top-down coordinate as reported by PyMuPDF.
# --------------------------------------------------------------------------
PAGE_W, PAGE_H = 595.2756, 841.8898
FRAME_L, FRAME_R = 56.69291, 538.5827          # rules, cover box, full-width tables
PARA_L, PARA_R = 62.69291, 532.5827            # paragraph text box (frame padding 6)
CONTENT_TOP = 68.36218                         # td of first flowable on a page
CONTENT_BOTTOM = 779.2                         # td limit of flowables
HANG = 36.85039                                # provision hanging indent (1.3 cm)
QUOTE_FIRST = 36.85039                         # quoted clause: first line indent
QUOTE_REST = 62.3622                           # quoted clause: continuation indent
BREAK_TOL = 1.0                                # ReportLab-observed overflow tolerance (pt);
                                               # an over-wide line is compressed with negative Tw

INK = ".101961 .101961 .101961"                # #1a1a1a body text
HDR_TXT = ".352941 .352941 .352941"            # #5a5a5a header/footer text
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
    """-> list of tokens; each token is ('w', [pieces]) or ('s', piece)."""
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
    """Greedy line breaking.  prefix = unbreakable leading pieces."""
    toks = tokenize(runs)
    lines, cur, curw, pend_space = [], list(prefix), pieces_width(prefix), None
    first_word_on_line = not prefix
    for kind, val in toks:
        if kind == "s":
            if cur:
                pend_space = val
            continue
        ww = pieces_width(val)
        avail = avail_first if not lines else avail_rest
        add = ww + (width(" ", pend_space[1], pend_space[2]) if (pend_space and not first_word_on_line) else 0)
        if not first_word_on_line and curw + add > avail + BREAK_TOL:
            lines.append(cur)
            cur, curw = list(val), ww
        else:
            if pend_space and not first_word_on_line:
                cur.append(pend_space)
            cur.extend(val)
            curw += add
        first_word_on_line = False
        pend_space = None
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
    """One BT..ET block, ReportLab style (Tm, TL, Tw, Td, T*)."""
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
            tw = (avails[i] - lw) / nsp            # shrink an over-wide line (as ReportLab does)
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
    o.append("0 Tw ET")
    return "\n".join(o)


# --------------------------------------------------------------------------
# Flowables
# --------------------------------------------------------------------------
class Para:
    """kind: body | prov | quote | head | proj | caption"""

    STYLES = {
        "body": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "prov": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "quote": dict(size=9.6, lead=13.4, reg=REG, bold=BOLD, justify=True),
        "head": dict(size=13, lead=16, reg="F2", bold="F2", justify=False),
        "proj": dict(size=10.5, lead=13, reg="F2", bold="F2", justify=False),
        "caption": dict(size=8.5, lead=11, reg="F2", bold="F2", justify=False),
    }

    def __init__(self, kind, markup, num=None):
        self.kind, self.markup, self.num = kind, markup, num
        st = self.STYLES[kind]
        self.size, self.lead, self.justify = st["size"], st["lead"], st["justify"]
        runs = parse_runs(markup, self.size, st["reg"], st["bold"])
        full = PARA_R - PARA_L
        if kind == "prov":
            prefix = [(num, BOLD, self.size, 0), ("   ", REG, self.size, 0)]
            self.x_first, self.x_rest = PARA_L, PARA_L + HANG
        elif kind == "quote":
            prefix = [("‘", REG, self.size, 0), (num, BOLD, self.size, 0),
                      ("  ", REG, self.size, 0)]
            self.x_first, self.x_rest = PARA_L + QUOTE_FIRST, PARA_L + QUOTE_REST
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


class QATable:
    COLS = [56.69291, 90.70866, 300.4724, 538.5827]
    HEAD = ["No", "Bidder question", "Authority response"]
    SIZE, LEAD, PAD_T, PAD_B, PAD_X = 8.2, 10.4, 3.5, 3.5, 4.0

    def __init__(self, rows):
        self.rows = []
        for r in rows:
            cells = []
            for ci, txt in enumerate(r):
                avail = self.COLS[ci + 1] - self.COLS[ci] - 2 * self.PAD_X
                runs = parse_runs(txt, self.SIZE)
                cells.append(break_lines([], runs, avail, avail))
            n = max(len(c) for c in cells)
            self.rows.append((cells, self.PAD_T + n * self.LEAD + self.PAD_B))
        self.head_h = self.PAD_T + self.LEAD + self.PAD_B

    def chunk(self, start, room):
        """How many rows from start fit (with repeated header) into room."""
        h, n = self.head_h, 0
        for cells, rh in self.rows[start:]:
            if h + rh > room + 1e-6:
                break
            h += rh
            n += 1
        return n, h

    def draw_rows(self, top, start, n):
        o = []
        x0, x1 = self.COLS[0], self.COLS[-1]
        o.append("q %s rg n %s %s %s %s re f* Q" % (THEAD_FILL, fmt(x0), fmt(Y(top)),
                                                   fmt(x1 - x0), fmt(-self.head_h)))
        for ci, h in enumerate(self.HEAD):
            o.append("BT 1 0 0 1 %s %s Tm /F2 8.2 Tf 10.4 TL 1 1 1 rg %s Tj T* ET"
                     % (fmt(self.COLS[ci] + self.PAD_X), fmt(Y(top + self.PAD_T + self.SIZE)), pstr(h)))
        y = top + self.head_h
        bounds = [top, y]
        for cells, rh in self.rows[start:start + n]:
            for ci, lines in enumerate(cells):
                x = self.COLS[ci] + self.PAD_X
                avail = self.COLS[ci + 1] - self.COLS[ci] - 2 * self.PAD_X
                o.append(emit_text_block(x, x, y + self.PAD_T + self.SIZE, self.LEAD, lines,
                                         [avail] * len(lines), False))
            y += rh
            bounds.append(y)
        # grid (ReportLab order: box top, bottom, left, right, inner rows, inner cols)
        g = ["q 1 J 1 j %s RG .4 w" % RULE]
        line = lambda a, b, c, d: g.append("n %s %s m %s %s l S" % (fmt(a), fmt(Y(b)), fmt(c), fmt(Y(d))))
        line(x0, top, x1, top)
        line(x0, y, x1, y)
        line(x0, y, x0, top)
        line(x1, y, x1, top)
        for b in bounds[1:-1]:
            line(x0, b, x1, b)
        for cx in self.COLS[1:-1]:
            line(cx, y, cx, top)
        g.append("Q")
        o.append("\n".join(g))
        return "\n".join(o), y - top


# Vertical gaps (bottom of previous flowable -> top of next), measured on ADD-01/02.
def gap(prev, nxt):
    if prev is None:
        return 0.0
    if prev == "cover":
        return 18.0                       # 8 pt spacer + 10 pt before project name
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
    return 5.0


def kind_of(fl):
    if isinstance(fl, Cover):
        return "cover"
    if isinstance(fl, QATable):
        return "table"
    return fl.kind


# --------------------------------------------------------------------------
# Page furniture
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
def layout(flowables):
    pages, cur, top, prev = [], [], CONTENT_TOP, None
    first_top = CONTENT_TOP + 6.0          # 6 pt spacer above the cover band
    i = 0
    started = False
    while i < len(flowables):
        fl = flowables[i]
        k = kind_of(fl)
        g = gap(prev, k) if prev is not None else 0.0
        t = top + g
        if not started:
            t = first_top
            started = True
        if isinstance(fl, QATable):
            start = getattr(fl, "_next", 0)
            n, h = fl.chunk(start, CONTENT_BOTTOM - t)
            if n == 0:
                pages.append(cur); cur, top, prev = [], CONTENT_TOP, None
                continue
            s, h = fl.draw_rows(t, start, n)
            cur.append(s)
            fl._next = start + n
            if fl._next < len(fl.rows):
                pages.append(cur); cur, top, prev = [], CONTENT_TOP, None
                continue
            top, prev = t + h, k
            i += 1
            continue
        h = fl.height
        need = h
        if k in ("head", "caption") and i + 1 < len(flowables):   # keep with next
            nx = flowables[i + 1]
            if isinstance(nx, QATable):
                need = h + gap(k, "table") + nx.head_h + nx.rows[0][1]
            else:
                need = h + gap(k, kind_of(nx)) + nx.height
        if prev is not None and t + need > CONTENT_BOTTOM:
            pages.append(cur); cur, top, prev = [], CONTENT_TOP, None
            continue
        cur.append(fl.draw(t))
        top, prev = t + h, k
        i += 1
    if cur:
        pages.append(cur)
    return pages


def build_pdf(flowables, header_left, out_path, metadata=None):
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
    if metadata:
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
    F.append(Cover("3", "Issued 5 November 2026", "Tender NUPA/ISTP/2026/014"))
    F.append(Para("proj", "Wadi Sirhan Independent Sewage Treatment Plant"))
    F.append(Para("body",
        "This Addendum amends the Proposal Due Date, the clarification period, the Bid Bond amount and the "
        "number of copies to be submitted, amends footnote 12 to Volume I Clause 8.5 and Volume I Clauses 8.6 "
        "and 12.2, inserts a new Volume I Clause 10.5, amends Volume II Tables 2-4 and 2-6 and Form 4-C, and "
        "responds to clarification requests 15 to 20."))
    F.append(Para("body",
        "This Addendum forms part of the RFP Documents and takes precedence in accordance with Volume I Clause "
        "3.2. Bidders shall acknowledge receipt in Form 4-A. All other terms of the RFP Documents remain unchanged."))

    F.append(Para("head", "1. RECITALS"))
    F.append(Para("prov", "This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda "
                          "Nos. 1 and 2 in accordance with Volume I Clause 3.2.", "1.1"))
    F.append(Para("prov", "A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or "
                          "Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.", "1.2"))

    F.append(Para("head", "2. AMENDMENT TO THE PROPOSAL DUE DATE"))
    F.append(Para("prov", "Volume I Clause 6.1, as amended by Addendum No. 1 Section 2.1, is further amended by "
                          "deleting %s and substituting %s. The time of 14:00 Riyadh time is unchanged."
                  % (q("Thursday 26 November 2026"), q("Thursday 10 December 2026", True)), "2.1"))
    F.append(Para("prov", "Section 2.2 of Addendum No. 1 applies mutatis mutandis to the amendment made by "
                          "Section 2.1 of this Addendum.", "2.2"))
    F.append(Para("prov", "In the revised Form 4-A at Appendix A to Addendum No. 1, the entry against %s, which "
                          "was not updated by that Addendum, is corrected to read %s."
                  % (q("Proposal Due Date"), q("10 December 2026, 14:00 Riyadh time", True)), "2.3"))

    F.append(Para("head", "3. AMENDMENT TO VOLUME I CLAUSE 5.2"))
    F.append(Para("prov", "In Volume I Clause 5.2, %s is deleted and %s is substituted. This amendment applies "
                          "to Clause 5.2 only. The periods of ten (10) Working Days in Volume I Clause 12.3 and "
                          "Volume V Clause 29.4 are unchanged."
                  % (q("ten (10) Working Days"), q("fifteen (15) Working Days", True)), "3.1"))
    F.append(Para("prov", "In Volume I Clause 5.2, %s is deleted and %s is substituted."
                  % (q("Requests received after that time will not be answered."),
                     q("Requests received after 14:00 Riyadh time on the last day for submission will not "
                       "be answered.", True)), "3.2"))

    F.append(Para("head", "4. AMENDMENT TO VOLUME I CLAUSE 6.4"))
    F.append(Para("prov", "In Volume I Clause 6.4, %s is deleted and %s is substituted. The other requirements "
                          "of Clause 6.4 are unchanged."
                  % (q("SAR 4,500,000 (four million five hundred thousand Saudi Riyals)"),
                     q("SAR 6,000,000 (six million Saudi Riyals)", True)), "4.1"))

    F.append(Para("head", "5. AMENDMENT TO VOLUME I CLAUSE 6.5"))
    F.append(Para("prov", "In Volume I Clause 6.5, the first sentence is deleted and replaced by: %s The "
                          "requirement to submit three (3) hard copies is <b>deleted</b>. The second and third "
                          "sentences of Clause 6.5 are unchanged."
                  % q("Each Proposal shall be submitted as one (1) marked original and one (1) searchable "
                      "electronic copy on encrypted USB media.", True), "5.1"))

    F.append(Para("head", "6. AMENDMENT TO FOOTNOTE 12 TO VOLUME I CLAUSE 8.5"))
    F.append(Para("prov", "In footnote 12 to Volume I Clause 8.5, %s is deleted and %s is substituted. The "
                          "remainder of footnote 12, including the number of reference plants, the look-back "
                          "period and the consequence of rejection, is unchanged."
                  % (q("80,000 m<sup>3</sup>/day"), q("60,000 m<sup>3</sup>/day", True)), "6.1"))

    F.append(Para("head", "7. AMENDMENT TO VOLUME I CLAUSE 8.6"))
    F.append(Para("prov", "In Volume I Clause 8.6, as reinstated by Addendum No. 2 Section 9.1, %s is deleted "
                          "and %s is substituted. The second sentence of Clause 8.6 as reinstated is unchanged."
                  % (q("thirty-five per cent (35%)"), q("thirty per cent (30%)", True)), "7.1"))

    F.append(Para("head", "8. NEW VOLUME I CLAUSE 10.5 AND RENUMBERING"))
    F.append(Para("prov", "The following new Clause 10.5 is <b>inserted</b> in Volume I after Clause 10.4:", "8.1"))
    F.append(Para("quote", "The Availability Payment quoted in Form 4-F shall not exceed <b>SAR 210,000,000 per "
                           "annum</b> (year 1 of operations, exclusive of value added tax). A Proposal that "
                           "quotes an Availability Payment exceeding this amount shall be rejected." + RQ,
                  "10.5"))
    F.append(Para("prov", "Existing Volume I Clauses 10.5 and 10.6 are renumbered <b>10.6</b> and <b>10.7</b> "
                          "respectively. A reference to Clause 10.5 or Clause 10.6 in Volumes I to V or in "
                          "Addenda Nos. 1 and 2, including in the response to clarification request 14 in "
                          "Addendum No. 2, shall be read as a reference to Clause 10.6 or Clause 10.7 "
                          "respectively.", "8.2"))

    F.append(Para("head", "9. AMENDMENT TO VOLUME I CLAUSE 12.2"))
    F.append(Para("prov", "In Volume I Clause 12.2, %s is deleted and %s is substituted. The period for "
                          "Commercial Close is unchanged."
                  % (q("two hundred and seventy (270) days"), q("three hundred (300) days", True)), "9.1"))
    F.append(Para("prov", "The response to clarification request 13 in Addendum No. 2 is <b>superseded</b>.",
                  "9.2"))

    F.append(Para("head", "10. AMENDMENT TO VOLUME II TABLE 2-4"))
    F.append(Para("prov", "In Volume II Table 2-4, in the row for <b>Total Suspended Solids (TSS)</b>, the limit "
                          "is amended from the value shown to <b>15 mg/l</b> and the basis of assessment is "
                          "amended to %s. All other entries in Table 2-4, including the Total Nitrogen limit as "
                          "amended by Addendum No. 2, are unchanged."
                  % q("Maximum, any single sample", True), "10.1"))

    F.append(Para("head", "11. AMENDMENT TO VOLUME II TABLE 2-6"))
    F.append(Para("prov", "In Volume II Table 2-6, in row 2-6.2 (Peak hourly flow (design)), %s is deleted and "
                          "%s is substituted. The unit is unchanged. No other row of Table 2-6 is amended."
                  % (q("7,500"), q("9,000", True)), "11.1"))
    F.append(Para("prov", "Bidders shall reflect the amended flow in the hydraulic design submitted under "
                          "Volume II Section 4.", "11.2"))

    F.append(Para("head", "12. AMENDMENT TO FORM 4-C"))
    F.append(Para("prov", "Form 4-C is amended by adding, after the fifth numbered declaration, the following "
                          "sixth declaration: %s"
                  % q("Sixth: that neither the member nor any of its directors has, within the preceding five "
                      "(5) years, been convicted in the Kingdom of an offence involving fraud, bribery or "
                      "corruption."), "12.1"))
    F.append(Para("prov", "Each member of the Bidder shall give the sixth declaration in its Form 4-C. Volume I "
                          "Clause 9.4 applies.", "12.2"))

    F.append(Para("head", "13. RESPONSES TO CLARIFICATION REQUESTS 15 TO 20"))
    F.append(QATable([
        ["15",
         "Must the Local Content Certificate required by Volume I Clause 8.6, as reinstated by Addendum "
         "No. 2, be submitted with the Proposal or may it follow at Financial Close?",
         "It shall be submitted with the Proposal, in Envelope A, as part of the evidence required under "
         "Section 8 (Volume I Clause 9.1). The required ratio is amended by Section 7 of this Addendum."],
        ["16",
         "Volume II Clause 6.1 requires unattended operation of the whole Facility and a permanently manned "
         "central control room. Must the control room be manned 24 hours a day?",
         "No. In Volume II Clause 6.1, " + q("a permanently manned central control room") + " is deleted and "
         + q("a central control room manned between 06:00 and 22:00 daily") + " is substituted. Volume II "
         "Clause 8.3 is unchanged."],
        ["17",
         "May a consortium member rely on a reference project delivered by its parent company or another "
         "affiliate for the purposes of Volume I Clause 8.5?",
         "No. Only a reference project for which the consortium member itself was responsible for design, "
         "construction or operation will be considered. A reference project of an affiliate will be "
         "disregarded."],
        ["18",
         "Does the Total Nitrogen limit introduced by Addendum No. 2 apply during the reliability run under "
         "Volume II Clause 7.2?",
         "Yes. Volume II Clause 7.2 requires every parameter in Table 2-4, as amended, to be met during the "
         "reliability run."],
        ["19",
         "Will a further site visit be offered?",
         "No further site visit will be held. Volume I Clause 5.5 applies."],
        ["20",
         "Are the appendices permitted by Volume II counted within the 150-page limit introduced by "
         "Addendum No. 2?",
         "No. Volume I Clause 9.2, as amended by Addendum No. 2, excludes the Form Sheets and the appendices "
         "expressly permitted by Volume II."],
    ]))
    return F


META = {"title": "(anonymous)", "author": "(anonymous)", "subject": "(unspecified)",
        "creator": "(unspecified)", "keywords": "", "producer": "",
        "creationDate": "D:20261003000000+00'00'", "modDate": "D:20261003000000+00'00'"}

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "ADD-03_Addendum_No_3.pdf"
    n = build_pdf(addendum3(), "Addendum No. 3", out, META)
    print("pages:", n)
