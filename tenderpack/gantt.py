"""A5 Gantt: drawn from the programme data (schedule.plan + programme.extend), never from anything else.

One layout (a list of drawing primitives) is computed from the programme and rendered twice, so the files agree:
  a5/gantt.svg   the chart (each row a <g id="act-..."> whose <title> holds the activity, ALL its A1 requirement
                 ids, its dates and its three statuses)
  a5/gantt.html  the SVG embedded, the legend, the notice, the planning basis and a table of every row with all
                 its requirement ids
  a5/gantt.pdf   one landscape page (A3), drawn directly with PyMuPDF from the same primitives (Base-14 Helvetica,
                 fixed metadata, no /ID): byte-identical across rebuilds
What is drawn: rows grouped by envelope and discipline, ordered by earliest start; the early bar ES..EF (solid =
staff effort; hatched = waiting on an external party, who is named in the row's title); the late window LS..LF as an
outline; float as a line from EF to LF; 0-Working-Day steps as diamonds; negative float (INFEASIBLE) in red with
its shortfall; GATED rows with a diamond at the latest start (the date the decision is needed by); OVERLOAD days of
the row's role as triangles; activities not scheduled (CONDITIONAL with an elapsed window, DEADLINE PASSED, NOT
NEEDED) without an early bar; non-working days shaded; the planning date as a solid line; the pack's dated
milestones (the PDD at the time the pack states, clarification cut-off, Pre-Bid Conference, site visit, ...) as
dashed lines; milestones outside the chart are listed under it. Deterministic: no clock, stable ordering, fixed
number formatting.
Session 11 (audit A5-1, A5-6, A5-8, R-9): a gate whose issue has a drafted clarification question shows both dates
("ask by" = the last day to decide whether to raise it, a hollow diamond; "finalise by" = its latest start, the filled
diamond); the row's flags (REVIEW, BLOCKED, STALE, ...) are tags in the status column and in full in the row's title,
with its predecessors; the status column wraps to a second line instead of truncating; a milestone whose readings
differ prints every reading ("14 Oct (conservative; 15 Oct if ...)"); the HTML table lists predecessors and flags.

Text other than plain ASCII (session 09). A string that is plain ASCII once typographic punctuation is mapped to
ASCII (dashes, quotes, ...) takes exactly the earlier path: Base-14 Helvetica in the PDF, the same characters in the
SVG. Any other string (Arabic, accented Latin, ...) is kept as written: the SVG and HTML carry it XML-escaped, and
the PDF draws it with page.insert_htmlbox (MuPDF's Story engine: it shapes Arabic and orders mixed Arabic/Latin
text by the bidi algorithm, using MuPDF's bundled fallback font, Noto Naskh Arabic, for glyphs Helvetica lacks),
wrapped in /ActualText holding the logical string so text extraction and search return the words as written; its
fonts are subset. Limits: the Arabic glyphs are the fallback font's (no font is chosen here); the SVG has no
direction or bidi markup, so the display of mixed-direction text there is the SVG viewer's job; the width of
non-Latin text is ESTIMATED (a fixed width per character, `_UNI_EM`), so fitting and label staggering are
approximate for it; only the strings this layout draws are covered (the PDF draws ids, statuses, milestone labels
and notes, not the activity names, which are in the SVG row titles and the HTML).
"""
from __future__ import annotations

import html as _html
import re
import unicodedata
from datetime import date, timedelta
from pathlib import Path

import pymupdf

from .dates import Calendar
from .schedule import NO_LEVELLING

PAGE_W, PAGE_H = 1190.0, 842.0                    # A3 landscape, points
MARGIN = 22.0
LABEL_W, STATUS_W = 292.0, 230.0   # session 12 (F5; audit R-d): 200 -> 230 so the full status prints in its two lines
# session 12 (audit A5-10): gantt.html shows the chart at a width at which its smallest text is at least this many CSS
# pixels (it scrolls horizontally inside its frame); the SVG and the PDF are unchanged
HTML_MIN_FONT_PX = 9.0
PDF_DATE = "D:20261001000000Z"
PRODUCER = "tenderpack"

SURFACE, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, NONWORK, BAND = "#e1e0d9", "#c3c2b7", "#ecebe6", "#f2f1ed"
STAFF, WAIT_FILL = "#2a78d6", "#cde2fb"
CRIT, CRIT_FILL, WARN, SERIOUS = "#d03b3b", "#f6d4d4", "#fab219", "#ec835a"

ENVELOPES = (("A", "Envelope A"), ("B", "Envelope B"), ("A+B", "Both envelopes"), ("none", "No envelope (actions)"))
DISC_ORDER = ("Legal", "Technical", "Commercial", "Bid management", "Document control")
_ASCII = {"—": "-", "–": "-", "−": "-", "…": "...", "‘": "'", "’": "'", "“": '"', "”": '"', "×": "x", "≤": "<=",
          "≥": ">=", " ": " "}


_UNI_EM = 0.5     # ESTIMATED advance (em) of a character Helvetica cannot measure (Arabic in the fallback font: ~0.4)


def _t(s) -> str:
    """Text for both renderers, the same in SVG and PDF. A string that is plain ASCII once typographic punctuation is
    mapped (`_ASCII`) is returned so (Base-14 Helvetica); any other string is kept as written (Unicode), control
    characters aside."""
    s = str(s)
    a = "".join(_ASCII.get(c, c) for c in s)
    if a.isascii():
        return "".join(c if 32 <= ord(c) < 127 else "?" for c in a)
    return "".join(c if ord(c) >= 32 and ord(c) != 127 else "?" for c in s)


def _w(s: str, size: float, bold: bool = False) -> float:
    s, font = _t(s), "hebo" if bold else "helv"
    if s.isascii():
        return pymupdf.get_text_length(s, fontname=font, fontsize=size)
    w = 0.0                      # Latin-1 measured with Helvetica; any other character ESTIMATED (see _UNI_EM)
    for c in s:
        if ord(c) < 256:
            w += pymupdf.get_text_length(c, fontname=font, fontsize=size)
        elif unicodedata.category(c) not in ("Mn", "Me", "Cf"):             # combining marks, bidi controls: no width
            w += size * (1.0 if unicodedata.east_asian_width(c) in ("W", "F") else _UNI_EM)
    return w


def _fit(s: str, size: float, width: float, bold: bool = False) -> str:
    s = _t(s)
    if _w(s, size, bold) <= width:
        return s
    while s and _w(s + "...", size, bold) > width:
        s = s[:-1]
    return s + "..."


def _ltr(s: str) -> str:
    """s, then a LEFT-TO-RIGHT MARK when s holds right-to-left letters, so that what the chart appends (a date) is not
    pulled into the right-to-left run by the bidi algorithm ('<Arabic> 11:00 26 Nov' would show '26' on the left).
    Plain Latin text is returned unchanged."""
    return s + "\u200e" if any(unicodedata.bidirectional(c) in ("R", "AL") for c in str(s)) else s


def _n(v: float) -> str:
    return f"{v:.2f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)


def _d(s: str | None) -> date | None:
    return date.fromisoformat(s) if s else None


def _cal(prog: dict) -> Calendar:
    c = prog.get("calendar") or {}
    return Calendar(weekend=frozenset(c.get("weekend", (4, 5))),
                    holidays=frozenset(date.fromisoformat(h) for h in c.get("holidays", [])))


# ---------------------------------------------------------------------------------------------- layout

class _L:
    """Drawing primitives, in order. Each is a tuple: ("rect", x, y, w, h, fill, stroke, width, dash),
    ("line", x1, y1, x2, y2, stroke, width, dash), ("poly", points, fill, stroke, width),
    ("text", x, y, text, size, colour, bold), ("open", id, title), ("close",)."""

    def __init__(self):
        self.items: list[tuple] = []

    def rect(self, x, y, w, h, fill=None, stroke=None, width=0.0, dash=None):
        self.items.append(("rect", x, y, max(w, 0.0), max(h, 0.0), fill, stroke, width, dash))

    def line(self, x1, y1, x2, y2, stroke=INK, width=0.5, dash=None):
        self.items.append(("line", x1, y1, x2, y2, stroke, width, dash))

    def poly(self, pts, fill=None, stroke=None, width=0.0):
        self.items.append(("poly", tuple(pts), fill, stroke, width))

    def text(self, x, y, s, size=6.0, colour=INK, bold=False):
        self.items.append(("text", x, y, _t(s), size, colour, bold))

    def hatch(self, x, y, w, h, stroke, step=2.6, width=0.45):
        k = x - h
        while k < x + w:
            x0, y0, x1, y1 = k, y + h, k + h, y
            if x0 < x:
                y0, x0 = y0 - (x - x0), x
            if x1 > x + w:
                y1, x1 = y1 + (x1 - (x + w)), x + w
            if x0 < x1:
                self.line(x0, y0, x1, y1, stroke, width)
            k += step

    def diamond(self, cx, cy, r, fill, stroke=None):
        self.poly([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill, stroke, 0.4 if stroke else 0.0)

    def triangle(self, cx, cy, r, fill):
        self.poly([(cx, cy - r), (cx + r, cy + r * 0.8), (cx - r, cy + r * 0.8)], fill, None, 0.0)


def _groups(prog: dict) -> list[tuple[str, list[dict]]]:
    env_rank = {k: i for i, (k, _) in enumerate(ENVELOPES)}
    env_name = dict(ENVELOPES)
    keyed: dict[tuple, list[dict]] = {}
    for a in prog["activities"]:
        env = a.get("envelope") or "none"
        disc = a.get("discipline") or "Bid management"
        k = (env_rank.get(env, 9), DISC_ORDER.index(disc) if disc in DISC_ORDER else 9, env, disc)
        keyed.setdefault(k, []).append(a)
    out = []
    for k in sorted(keyed):
        rows = sorted(keyed[k], key=lambda a: (a.get("earliest_start") or "9999", a.get("latest_start") or "9999", a["id"]))
        out.append((f"{env_name.get(k[2], k[2])} - {k[3]}", rows))
    return out


def _range(prog: dict) -> tuple[date, date, list[dict], list[dict]]:
    pd = _d(prog["planning_date"] if prog.get("planning_date") else prog["status_date"])
    dates = [pd]
    for a in prog["activities"]:
        dates += [_d(a.get(k)) for k in ("earliest_start", "earliest_finish", "latest_start", "latest_finish") if a.get(k)]
    lo_cut, hi_cut = pd - timedelta(days=30), max(dates) + timedelta(days=21)
    inside, outside = [], []
    for m in prog.get("milestones", []):
        md = _d(m.get("date"))
        if md is None:
            continue
        (inside if lo_cut <= md <= hi_cut else outside).append(m)
    dates += [_d(m["date"]) for m in inside]
    lo, hi = min(dates), max(dates)
    d0 = lo - timedelta(days=(lo.weekday() + 1) % 7)            # the Sunday on or before
    d1 = hi + timedelta(days=(5 - hi.weekday()) % 7)            # the Saturday on or after
    return d0, d1, inside, outside


def _tags(a: dict) -> list[tuple[str, str, str]]:
    """(text, colour, marker) for the status column: timing, decision, resource; never colour alone."""
    out = []
    st = a.get("status", "OK")
    if st.startswith("INFEASIBLE"):
        out.append((st, CRIT, "square"))
    elif st.startswith("CONDITIONAL"):
        out.append(("CONDITIONAL: window elapsed, not known if needed", MUTED, "circle"))
    elif st != "OK":
        out.append((st, CRIT if st.startswith(("DEADLINE", "NO WORKING")) else MUTED, "square"))
    if a.get("gated_by"):
        ask, fin = _d(a.get("ask_by")), _d(a.get("finalise_by") or a.get("decision_needed_by"))
        day = lambda d: f"{d.day} {d:%b}" if d else "-"                    # noqa: E731
        out.append((f"GATED {', '.join(a['gated_by'])}; " + (f"ask by {day(ask)}; finalise by {day(fin)}" if ask
                                                             else f"decide by {day(fin)}"), WARN, "diamond"))
    elif _route_shown(a):                                   # session 12 (audit A5-1): the route on a late chain
        ask = _d(a["ask_by"])
        out.append((f"question drafted: ask by {ask.day} {ask:%b}", WARN, "diamond"))
    rs = str(a.get("resource_status", ""))
    if rs.startswith("OVERLOAD"):
        out.append((f"OVERLOAD {a.get('resource', '')}", SERIOUS, "triangle"))
    for f in a.get("flags") or []:                          # session 11 (audit A5-6): review and blocking flags
        if f.startswith("REVIEW ("):
            out.append((f.split(":")[0], WARN, "square"))
            out += [(f"BLOCKED: {b.split(' (')[0]}", CRIT, "square") for b in re.findall(r"; BLOCKED: ([^;]+)", f)]
        elif f.startswith(("BLOCKED", "REQUIREMENT STALE", "IMAGE READING PENDING", "GATE ISSUE NOT IN THE REGISTER")):
            out.append((f.split(" (")[0], CRIT if f.startswith(("BLOCKED", "REQUIREMENT STALE")) else MUTED, "square"))
    # session 12 (F5; audit R-d): the BLOCKED tags as one ('BLOCKED, not supplied: A; B'), each document once, so the
    # status prints in full in its two lines (the cell cut 'BLOCKED...' when each document repeated the words)
    blocked = [t for t in out if t[0].startswith("BLOCKED")]
    if len(blocked) > 1:
        docs = list(dict.fromkeys(re.sub(r"\s+not supplied$", "", re.sub(r"^BLOCKED:\s*(?:cannot be established:\s*)?",
                                                                          "", t[0])).strip() for t in blocked))
        i = out.index(blocked[0])
        out = [t for t in out if t not in blocked]
        out.insert(i, ("BLOCKED, not supplied: " + "; ".join(docs), CRIT, "square"))
    return out


def _route_shown(a: dict) -> bool:
    """Whether the chart shows the clarification route of an activity that is not gated (session 12, audit A5-1): a
    question is drafted on its rows (`ask_by`) and its timing is not OK (asking the Authority is one way to move the
    pack date that makes it late); every other activity has it in its title, gantt.html and programme.csv."""
    st = str(a.get("status") or "OK")
    return bool(a.get("ask_by")) and not a.get("gated_by") and st != "OK" and not st.startswith(("CONDITIONAL", "NOT NEEDED"))


def _status_layout(tags: list[tuple[str, str, str]], x0: float, x1: float, size: float, lines: int,
                   force: bool) -> list[tuple] | None:
    """[(line, x, text, colour, marker or None)] placing the status tags (a marker, then the text) on up to `lines`
    lines between x0 and x1. A tag that does not fit in the rest of a line is split at a space and continues on the
    next line. None when not `force` and the tags do not fit on the lines; with `force`, only what does not fit on the
    last line is cut (with '...'): the full text is in the row's title, gantt.html and programme.csv."""
    out, ln, x = [], 0, x0
    for text, colour, marker in tags:
        rest, mk = text, marker
        while rest:
            room = x1 - x - 6
            if _w(rest, size) <= room:
                out.append((ln, x, rest, colour, mk))
                x += 6 + _w(rest, size) + 6
                break
            if not force:
                return None
            words, head = rest.split(" "), ""
            while words and _w((head + " " + words[0]).strip(), size) <= room:
                head = (head + " " + words.pop(0)).strip()
            if ln + 1 < lines:
                if head:
                    out.append((ln, x, head, colour, mk))
                    rest, mk = " ".join(words), None
                ln, x = ln + 1, x0
                continue
            s = _fit(rest, size, max(room, 1.0))
            out.append((ln, x, s, colour, mk))
            x += 6 + _w(s, size) + 6
            break
    return out


def _title(a: dict) -> str:
    return (f"{a['id']}: {a['name']} | A1 requirement ids: {', '.join(a['req_ids'])} | {a.get('discipline')}; "
            f"{a.get('resource')}; x{a.get('count')} | elapsed {a['duration_wd']} WD ({a['duration_assumption']}), staff "
            f"effort {_n(float(a.get('effort_total_wd') or 0))} WD, waits on: {a.get('waiting_on') or 'nobody external'} | "
            f"ES {a.get('earliest_start')} EF {a.get('earliest_finish')} LS {a.get('latest_start')} LF "
            f"{a.get('latest_finish')} float {a.get('float_wd')} WD | timing: {a['status']} | decision: "
            f"{a.get('decision_status')} | resource: {a.get('resource_status')} | after: "
            f"{', '.join(a.get('predecessors') or []) or 'none (starts from the planning date)'} | flags: "
            f"{' | '.join(a.get('flags') or []) or 'none'}")


def _alt(ms: list[dict]) -> str:
    """' (conservative; 15 Oct if the ADD-01 issue day is excluded)' for milestones whose readings differ, else ''."""
    alts = [(m.get("reading_policy") or "planning", x) for m in ms for x in m.get("alternatives") or []]
    if not alts:
        return ""
    return (f" ({alts[0][0]}; " + "; ".join(f"{_d(x['value']).day} {_d(x['value']):%b} {x['words']}" for _, x in alts)
            + ")")


def layout(prog: dict) -> list[tuple]:
    L = _L()
    cal = _cal(prog)
    pd = _d(prog.get("planning_date") or prog["status_date"])
    d0, d1, inside, outside = _range(prog)
    groups = _groups(prog)
    n_rows = sum(len(r) for _, r in groups)
    L.rect(0, 0, PAGE_W, PAGE_H, SURFACE)
    # ---- title and basis
    L.text(MARGIN, 34, f"A5 bid programme - Gantt - {prog['stage']} - planning date {pd.isoformat()} "
                       f"(PROPOSAL, not reviewed)", 13, INK, True)
    L.text(MARGIN, 47, _fit(f"Earliest dates: forward pass from {prog.get('start_date', pd.isoformat())} (first Working Day "
                            f"on or after the planning date, the {prog['stage']} issue date). Latest dates: backward pass "
                            "from the pack deadlines. Working Days Sun-Thu (VOL-I 2.4). Every duration, effort, waiting "
                            "party and capacity is a PROVISIONAL ASSUMPTION (config/assumptions.yaml).",
                            6.6, PAGE_W - 2 * MARGIN), 6.6, INK2)
    # ---- geometry
    cx0 = MARGIN + LABEL_W + STATUS_W
    cx1 = PAGE_W - MARGIN
    ndays = (d1 - d0).days + 1
    dw = (cx1 - cx0) / ndays
    x = lambda d: cx0 + (d - d0).days * dw                            # noqa: E731  (start of day d)
    band_top, axis_y = 56.0, 112.0
    rows_top = 128.0
    legend_h = 96.0
    rows_bot_max = PAGE_H - MARGIN - legend_h
    gh = 10.0
    rh = min(13.0, (rows_bot_max - rows_top - gh * len(groups)) / max(n_rows, 1))
    fs = max(5.2, min(6.8, rh * 0.56))
    rows_bot = rows_top + gh * len(groups) + rh * n_rows
    # ---- non-working days, week lines, axis
    d = d0
    while d <= d1:
        if not cal.is_working_day(d):
            L.rect(x(d), rows_top, dw, rows_bot - rows_top, NONWORK)
        d += timedelta(days=1)
    d, months = d0, []
    while d <= d1:
        if d.weekday() == 6:                                         # Sunday: start of the working week
            L.line(x(d), axis_y - 6, x(d), rows_bot, GRID, 0.5)
            L.text(x(d) + 1.5, axis_y + 8, f"{d.day} {d.strftime('%b')}", 5.8, INK2)
        if d == d0 or d.day == 1:
            months.append(d)
        d += timedelta(days=1)
    for i, m in enumerate(months):                                   # a month label only where it fits
        label = m.strftime("%B %Y")
        nxt = x(months[i + 1]) if i + 1 < len(months) else cx1
        if x(m) + 1.5 + _w(label, 6.2, True) + 3 <= nxt:
            L.text(x(m) + 1.5, axis_y - 1, label, 6.2, INK, True)
    L.line(cx0, rows_top, cx1, rows_top, AXIS, 0.6)
    L.text(MARGIN, rows_top - 4, "Activity  (count)   A1 requirement ids", 6.2, INK, True)
    L.text(MARGIN + LABEL_W + 4, rows_top - 4, "Timing / decision / resource status", 6.2, INK, True)
    # ---- milestones and the planning date: labels staggered in the band above the axis
    by_day: dict[date, list[dict]] = {}
    for m in inside:
        by_day.setdefault(_d(m["date"]), []).append(m)
    labels = [(x(pd), f"Planning date {pd.isoformat()} ({prog['stage']} issued)", True)]
    for md, ms in sorted(by_day.items()):                            # one line per day; a timed milestone sets it
        ms = sorted(ms, key=lambda m: (not m.get("time"), m["id"] != "PDD", m["id"]))
        m = ms[0]
        if m.get("time"):
            hh, mm = (int(v) for v in m["time"].split(":"))
            mx = x(md) + dw * (hh + mm / 60) / 24
        elif m.get("purpose") == "deadline":
            mx = x(md) + dw                                          # by the end of that day
        else:
            mx = x(md) + dw / 2
        labels.append((mx, " / ".join(_ltr(k["short"]) + (" (conditional)" if k.get("conditional") and "conditional" not in
                                                          k["short"] else "") for k in ms)
                       + f" {md.day} {md.strftime('%b')}" + _alt(ms), False))
    levels: list[float] = []
    for mx, s, bold in sorted(labels, key=lambda t: t[0]):
        size = 6.0
        w = _w(s, size, bold)
        lx = min(mx + 2, cx1 - w)
        lvl = next((i for i, end in enumerate(levels) if lx > end + 4), None)
        if lvl is None:
            lvl = len(levels)
            levels.append(0.0)
        levels[lvl] = lx + w
        ly = band_top + 9 + (lvl % 5) * 9
        L.line(mx, ly + 2, mx, rows_bot, INK if bold else INK2, 1.1 if bold else 0.6, None if bold else "2 2")
        if not bold:
            L.diamond(mx, rows_top - 1.5, 2.2, INK2)
        L.text(lx, ly, s, size, INK if bold else INK2, bold)
    # ---- rows
    y = rows_top
    overload_days: dict[str, set[str]] = {}
    for o in (prog.get("resources") or {}).get("overloads", []):
        for aid in o["activities"]:
            overload_days.setdefault(aid, set()).update(o["dates"])
    for gname, acts in groups:
        L.rect(MARGIN, y, cx1 - MARGIN, gh, BAND)
        L.text(MARGIN + 2, y + gh - 2.6, f"{gname} ({len(acts)})", 6.4, INK, True)
        y += gh
        for a in acts:
            L.items.append(("open", f"act-{a['id']}", _title(a)))
            st = a.get("status", "OK")
            mid = y + rh / 2
            # label: id (count) and the A1 requirement ids that fit; all of them are in the title and the HTML table
            head = a["id"] + (f" x{a['count']}" if a.get("count", 1) != 1 else "")
            L.text(MARGIN + 2, y + rh * 0.68, head, fs, INK, True)
            hx = MARGIN + 2 + _w(head, fs, True) + 4
            avail = MARGIN + LABEL_W - 4 - hx
            ids = list(a["req_ids"])
            shown = ""
            for i in range(len(ids), 0, -1):
                more = f" +{len(ids) - i}" if i < len(ids) else ""
                cand = ", ".join(ids[:i]) + more
                if _w(cand, fs - 0.8) <= avail:
                    shown = cand
                    break
            if not shown and ids:
                shown = _fit(f"{ids[0]} +{len(ids) - 1}" if len(ids) > 1 else ids[0], fs - 0.8, avail)
            L.text(hx, y + rh * 0.68, shown, fs - 0.8, INK2)
            # status column: one line when everything fits, else two (R-9); markers centred on their line
            sx0, sx1 = MARGIN + LABEL_W + 4, MARGIN + LABEL_W + STATUS_W - 6
            tags = _tags(a)
            placed = _status_layout(tags, sx0, sx1, fs - 0.6, 1, False)
            if placed is not None:
                ssize, base = fs - 0.6, (y + rh * 0.68,)
            else:
                ssize = fs - 1.0
                placed, base = _status_layout(tags, sx0, sx1, ssize, 2, True), (y + rh * 0.46, y + rh * 0.93)
            for ln, sx, text, colour, marker in placed:
                cy = base[ln] - ssize * 0.34
                if marker is None:
                    pass
                elif marker == "square":
                    L.rect(sx, cy - 2.2, 4.4, 4.4, colour)
                elif marker == "diamond":
                    L.diamond(sx + 2.2, cy, 2.6, colour, INK2)
                elif marker == "triangle":
                    L.triangle(sx + 2.2, cy, 2.5, colour)
                else:
                    L.poly([(sx + 2.2 + 2.2 * c, cy + 2.2 * s) for c, s in ((1, 0), (0.7, 0.7), (0, 1), (-0.7, 0.7),
                                                                           (-1, 0), (-0.7, -0.7), (0, -1), (0.7, -0.7))],
                           None, colour, 0.8)
                L.text(sx + 6, base[ln], text, ssize, INK)
            # bars
            es, ef, ls, lf = (_d(a.get(k)) for k in ("earliest_start", "earliest_finish", "latest_start", "latest_finish"))
            scheduled = not st.startswith(("CONDITIONAL", "DEADLINE PASSED", "NOT NEEDED"))
            bad = st.startswith(("INFEASIBLE", "NO WORKING WINDOW"))
            colour, light = (CRIT, CRIT_FILL) if bad else (STAFF, WAIT_FILL)
            if ls and lf:
                L.rect(x(ls), y + rh * 0.62, x(lf) + dw - x(ls), rh * 0.26, None, INK2 if scheduled else MUTED, 0.6,
                       None if scheduled else "1.5 1.5")
            if scheduled and es and ef:
                bt, bh = y + rh * 0.14, rh * 0.42
                if int(a["duration_wd"]) == 0:
                    L.diamond(x(ef) + dw, bt + bh / 2, min(3.2, rh * 0.3), colour)
                elif a.get("waiting_on"):
                    L.rect(x(es), bt, x(ef) + dw - x(es), bh, light)
                    L.hatch(x(es), bt, x(ef) + dw - x(es), bh, colour)
                    L.rect(x(es), bt, x(ef) + dw - x(es), bh, None, colour, 0.6)
                else:
                    L.rect(x(es), bt, x(ef) + dw - x(es), bh, colour)
                fl = a.get("float_wd")
                if fl is not None and fl > 0 and lf and lf > ef:
                    L.line(x(ef) + dw, bt + bh / 2, x(lf) + dw, bt + bh / 2, MUTED, 0.6)
                    L.line(x(lf) + dw, bt + bh * 0.15, x(lf) + dw, bt + bh * 0.85, MUTED, 0.6)
                    if _w(f"+{fl}", fs - 1.4) + 3 < x(lf) - x(ef):
                        L.text(x(ef) + dw + 2, bt + bh / 2 - 1, f"+{fl}", fs - 1.4, MUTED)
                elif fl is not None and fl < 0:
                    L.text(x(ef) + dw + 2, bt + bh * 0.9, f"{fl} WD", fs - 0.6, CRIT, True)
            if a.get("gated_by") and ls:
                L.diamond(x(ls), y + rh * 0.75, min(3.4, rh * 0.32), WARN, INK2)
            ask = _d(a.get("ask_by"))
            if (a.get("gated_by") or _route_shown(a)) and ask:   # session 11: the last day to decide whether to ask
                r_ = min(3.4, rh * 0.32)
                L.poly([(x(ask), y + rh * 0.75 - r_), (x(ask) + r_, y + rh * 0.75), (x(ask), y + rh * 0.75 + r_),
                        (x(ask) - r_, y + rh * 0.75)], SURFACE, WARN, 0.9)
            for day in sorted(overload_days.get(a["id"], ())):
                dd = _d(day)
                if ls and lf and max(ls, pd) <= dd <= lf:
                    L.triangle(x(dd) + dw / 2, y + rh - 2.2, min(2.2, rh * 0.18), SERIOUS)
            L.line(MARGIN, y + rh, cx1, y + rh, GRID, 0.3)
            L.items.append(("close",))
            y += rh
    # ---- legend
    ly = rows_bot + 12
    L.text(MARGIN, ly, "Legend", 6.8, INK, True)
    items = [("staff", "staff effort (early bar ES..EF)"), ("wait", "external waiting + staff effort (hatched, ES..EF)"),
             ("late", "late window LS..LF"), ("float", "float (EF to LF)"), ("zero", "0-WD step"),
             ("crit", "INFEASIBLE: negative float, shortfall in WD (never compressed)"),
             ("gate", "GATED: finalise by (latest start)"),
             ("ask", "ask by: last day to decide whether to raise a clarification request"),
             ("over", "OVERLOAD: role over capacity that day"),
             ("cond", "CONDITIONAL / not scheduled (late window only)"), ("nonwork", "non-working day"),
             ("today", "planning date"), ("mile", "pack milestone")]
    lx, row = MARGIN + 40, 0
    for kind, label in items:
        w = 22 + _w(label, 6.2) + 14
        if lx + w > PAGE_W - MARGIN:
            lx, row = MARGIN + 40, row + 1
        yy = ly - 6 + row * 11
        if kind == "staff":
            L.rect(lx, yy, 16, 5, STAFF)
        elif kind == "wait":
            L.rect(lx, yy, 16, 5, WAIT_FILL)
            L.hatch(lx, yy, 16, 5, STAFF)
            L.rect(lx, yy, 16, 5, None, STAFF, 0.6)
        elif kind == "late":
            L.rect(lx, yy + 1, 16, 3.5, None, INK2, 0.6)
        elif kind == "float":
            L.line(lx, yy + 2.5, lx + 16, yy + 2.5, MUTED, 0.6)
            L.line(lx + 16, yy, lx + 16, yy + 5, MUTED, 0.6)
        elif kind == "zero":
            L.diamond(lx + 8, yy + 2.5, 3, STAFF)
        elif kind == "crit":
            L.rect(lx, yy, 16, 5, CRIT)
        elif kind == "gate":
            L.diamond(lx + 8, yy + 2.5, 3.2, WARN, INK2)
        elif kind == "ask":
            L.poly([(lx + 8, yy - 0.7), (lx + 11.2, yy + 2.5), (lx + 8, yy + 5.7), (lx + 4.8, yy + 2.5)], SURFACE, WARN, 0.9)
        elif kind == "over":
            L.triangle(lx + 8, yy + 2.5, 2.8, SERIOUS)
        elif kind == "cond":
            L.rect(lx, yy + 1, 16, 3.5, None, MUTED, 0.6, "1.5 1.5")
        elif kind == "nonwork":
            L.rect(lx, yy - 1, 16, 7, NONWORK)
        elif kind == "today":
            L.line(lx + 8, yy - 2, lx + 8, yy + 7, INK, 1.1)
        else:
            L.line(lx + 8, yy - 2, lx + 8, yy + 7, INK2, 0.6, "2 2")
        L.text(lx + 20, yy + 4.6, label, 6.2, INK2)
        lx += w
    ny = ly + 11 * (row + 1) + 4
    out_txt = "; ".join(f"{_ltr(m['short'])} {m['date']}" + (f" ({m.get('reading_policy') or 'planning'}; "
                                                             f"{m['other_readings']})" if m.get("other_readings") else "")
                        for m in outside)
    notes = [f"PROPOSAL, not reviewed. Timing, decision readiness and resource feasibility are separate statuses; "
             f"{NO_LEVELLING}. No bidder references, certificates, attendance or financial standing are assumed to exist.",
             "Each row: activity id, count, then the A1 requirement ids that fit (+n more); ALL ids are in the row's hover "
             "title, gantt.html and programme.csv. Load window: late (LS..LF, clipped at the planning date).",
             f"Milestones outside the chart: {out_txt or 'none'}."]
    if any(str(f).startswith("REVIEW (") for a in prog.get("activities") or [] for f in a.get("flags") or []):
        from .relationships import STATUS_LEGEND        # session 12 (F5; audit R-e): what 'REVIEW (confirmed ...)' means
        notes.append(f"REVIEW (<status> ...) tags: {STATUS_LEGEND}")
    for s in notes:                                   # wrapped, never cut (session 11)
        line = ""
        for wd in s.split(" "):
            if line and _w(line + " " + wd, 6.2) > PAGE_W - 2 * MARGIN:
                L.text(MARGIN, ny, line, 6.2, INK2)
                ny, line = ny + 8.6, wd
            else:
                line = (line + " " + wd).strip()
        L.text(MARGIN, ny, line, 6.2, INK2)
        ny += 8.6
    return L.items


# ---------------------------------------------------------------------------------------------- renderers

def svg(prog: dict) -> str:
    esc = lambda s: _html.escape(s, quote=True)                      # noqa: E731
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{_n(PAGE_W)}" height="{_n(PAGE_H)}" '
           f'viewBox="0 0 {_n(PAGE_W)} {_n(PAGE_H)}" font-family="Helvetica, Arial, sans-serif" role="img" '
           f'aria-label="A5 bid programme Gantt chart, {esc(prog["stage"])}">']
    for it in layout(prog):
        k = it[0]
        if k == "rect":
            _, x, y, w, h, fill, stroke, sw, dash = it
            out.append(f'<rect x="{_n(x)}" y="{_n(y)}" width="{_n(w)}" height="{_n(h)}" fill="{fill or "none"}"'
                       + (f' stroke="{stroke}" stroke-width="{_n(sw)}"' if stroke else "")
                       + (f' stroke-dasharray="{dash.replace(" ", ",")}"' if dash else "") + "/>")
        elif k == "line":
            _, x1, y1, x2, y2, stroke, sw, dash = it
            out.append(f'<line x1="{_n(x1)}" y1="{_n(y1)}" x2="{_n(x2)}" y2="{_n(y2)}" stroke="{stroke}" '
                       f'stroke-width="{_n(sw)}"' + (f' stroke-dasharray="{dash.replace(" ", ",")}"' if dash else "") + "/>")
        elif k == "poly":
            _, pts, fill, stroke, sw = it
            out.append(f'<polygon points="{" ".join(f"{_n(px)},{_n(py)}" for px, py in pts)}" fill="{fill or "none"}"'
                       + (f' stroke="{stroke}" stroke-width="{_n(sw)}"' if stroke else "") + "/>")
        elif k == "text":
            _, x, y, s, size, colour, bold = it
            out.append(f'<text x="{_n(x)}" y="{_n(y)}" font-size="{_n(size)}" fill="{colour}"'
                       + (' font-weight="bold"' if bold else "") + f">{esc(s)}</text>")
        elif k == "open":
            out.append(f'<g id="{esc(it[1])}"><title>{esc(it[2])}</title>')
        elif k == "close":
            out.append("</g>")
    out.append("</svg>")
    return "\n".join(out) + "\n"


def _rgb(h: str | None):
    if not h:
        return None
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


def _pdf_unicode_text(doc, page, x: float, y: float, s: str, size: float, colour: str, bold: bool) -> None:
    """Draw a string that is not plain ASCII with MuPDF's Story engine (shaping, bidi, fallback fonts), its first
    baseline at y and its text starting at x (the engine sets the baseline 1 pt + 0.9 em below the box top and the
    text 1 pt inside it), wrapped in /ActualText holding the logical string (extraction and search read the words as
    written, not the shaped glyphs)."""
    top = y - 1.0 - 0.9 * size
    rect = pymupdf.Rect(x - 1.0, top, max(PAGE_W, x + 2 * _w(s, size, bold) + 10), top + 3 * size)
    css = (f"*{{margin:0;padding:0;font-family:sans-serif;font-size:{_n(size)}px;color:{colour};white-space:nowrap;"
           f"text-align:left;font-weight:{'bold' if bold else 'normal'}}}")
    before = set(page.get_contents())
    spare, _ = page.insert_htmlbox(rect, f"<div>{_html.escape(s, quote=False)}</div>", css=css, scale_low=1)
    if spare < 0:
        raise ValueError(f"Gantt PDF: text does not fit its box: {s!r}")
    actual = f"/Span <</ActualText <FEFF{s.encode('utf-16-be').hex().upper()}>>> BDC\n".encode()
    for xref in page.get_contents():
        if xref not in before:
            doc.update_stream(xref, actual + doc.xref_stream(xref) + b"\nEMC\n")


def pdf_bytes(prog: dict) -> bytes:
    doc = pymupdf.open()
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    shape = page.new_shape()
    unicode_text = False
    for it in layout(prog):
        k = it[0]
        if k == "rect":
            _, x, y, w, h, fill, stroke, sw, dash = it
            shape.draw_rect(pymupdf.Rect(x, y, x + w, y + h))
            shape.finish(color=_rgb(stroke), fill=_rgb(fill), width=sw if stroke else 0,
                         dashes=f"[{dash}] 0" if dash else None)
        elif k == "line":
            _, x1, y1, x2, y2, stroke, sw, dash = it
            shape.draw_line(pymupdf.Point(x1, y1), pymupdf.Point(x2, y2))
            shape.finish(color=_rgb(stroke), width=sw, dashes=f"[{dash}] 0" if dash else None)
        elif k == "poly":
            _, pts, fill, stroke, sw = it
            shape.draw_polyline([pymupdf.Point(px, py) for px, py in pts])
            shape.finish(color=_rgb(stroke), fill=_rgb(fill), width=sw if stroke else 0, closePath=True)
        elif k == "text":
            _, x, y, s, size, colour, bold = it
            if s.isascii():
                shape.insert_text(pymupdf.Point(x, y), s, fontname="hebo" if bold else "helv", fontsize=size,
                                  color=_rgb(colour))
            else:                                   # Unicode: drawn in order (the shape so far is committed first)
                shape.commit()
                _pdf_unicode_text(doc, page, x, y, s, size, colour, bold)
                shape = page.new_shape()
                unicode_text = True
    shape.commit()
    if unicode_text:
        doc.subset_fonts()
    doc.set_metadata({"title": f"A5 bid programme Gantt {prog['stage']}", "author": "", "subject": "", "keywords": "",
                      "creator": PRODUCER, "producer": PRODUCER, "creationDate": PDF_DATE, "modDate": PDF_DATE})
    data = doc.tobytes(garbage=3, deflate=True, no_new_id=True)
    doc.close()
    return data


def html(prog: dict, svg_text: str | None = None) -> str:
    esc = lambda s: _html.escape(str(s if s is not None else ""), quote=False)  # noqa: E731
    from .programme import NOTICE
    svg_text = svg_text if svg_text is not None else svg(prog)
    smallest = min((it[4] for it in layout(prog) if it[0] == "text"), default=HTML_MIN_FONT_PX)
    width = int(-(-PAGE_W * HTML_MIN_FONT_PX // smallest)) if smallest < HTML_MIN_FONT_PX else int(PAGE_W)
    rows = []
    for gname, acts in _groups(prog):
        rows.append(f'<tr class="g"><td colspan="16">{esc(gname)} ({len(acts)})</td></tr>')
        for a in acts:
            rows.append("<tr>" + "".join(f"<td>{v}</td>" for v in (
                f"<b>{esc(a['id'])}</b>" + (f" x{a['count']}" if a.get("count", 1) != 1 else ""),
                esc(", ".join(a["req_ids"])), esc(", ".join(a.get("predecessors") or []) or "-"),
                esc(a.get("earliest_start")), esc(a.get("earliest_finish")),
                esc(a.get("latest_start")), esc(a.get("latest_finish")), esc(a.get("float_wd")), esc(a["status"]),
                esc(a.get("decision_status")),
                esc((", ".join(a.get("clarification_questions") or []) + (f" (ask by {a['ask_by']})" if a.get("ask_by")
                                                                         else "")) or "-"),
                esc(a.get("resource_status")),
                esc(f"{a['duration_wd']} WD elapsed; staff {_n(float(a.get('effort_total_wd') or 0))} WD"),
                esc(a.get("waiting_on") or "-"), esc(a.get("resource")), esc(" | ".join(a.get("flags") or []) or "-"))) + "</tr>")
    ms = [f"<tr><td>{esc(m['date'] or 'no date')} {esc(m.get('time') or '')}"
          + (f" ({esc(m.get('reading_policy') or 'planning')}; {esc(m['other_readings'])})" if m.get("other_readings") else "")
          + f"</td><td>{esc(m['label'])}</td>"
          f"<td>{esc(m['source'])}</td><td>{esc(m['kind'])}</td></tr>" for m in prog.get("milestones", [])]
    ov = [f"<li>{esc(o['resource'])}: {esc(o['from'])}..{esc(o['to'])} ({o['days']} WD), peak {_n(float(o['peak_load']))} "
          f"vs capacity {esc(o['capacity'])} staff: {esc(', '.join(o['activities']))}</li>"
          for o in (prog.get("resources") or {}).get("overloads", [])]
    legend = ["Solid bar: staff effort, earliest start to earliest finish (ES..EF).",
              "Hatched bar: the elapsed time waits on an external party (bank, notary, authority, auditor, member, "
              "client...); the staff effort inside it is in the row's title and the table.",
              "Outline below the bar: late window, latest start to latest finish (LS..LF).",
              "Grey line from the bar to the end of the late window: positive float (Working Days).",
              "Red bar and '-n WD': negative float, INFEASIBLE by n Working Days; nothing is compressed.",
              "Amber diamond on the late window: GATED; finalise by the latest start. Hollow amber diamond: the last day "
              "to decide whether to raise the gate's drafted clarification question (the latest start of the activity "
              "that must finish by the clarification cut-off); on a late activity that is not gated, 'question drafted: "
              "ask by' and the hollow diamond show the same date for a question drafted on its rows (the Clarification "
              "questions column lists every activity's).",
              "Status tags REVIEW / BLOCKED / STALE: the row's flags (in full in the Flags column and the row's title).",
              "REVIEW (<status> ...): " + __import__("tenderpack.relationships", fromlist=["STATUS_LEGEND"]).STATUS_LEGEND,
              "Orange triangles: OVERLOAD days of the row's role (load above capacity). Not levelled.",
              "Dotted outline only: CONDITIONAL (window elapsed; whether the condition arose is not known), DEADLINE "
              "PASSED or NOT NEEDED: no work scheduled.",
              "Shaded columns: non-working days (Friday, Saturday, declared holidays). Solid vertical line: the planning "
              "date. Dashed vertical lines: the pack's dated milestones."]
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" "
            "content=\"width=device-width, initial-scale=1\"><title>A5 Gantt</title><style>"
            "body{font-family:system-ui,-apple-system,'Segoe UI',sans-serif;margin:16px;color:#0b0b0b;background:#fcfcfb}"
            ".chart{overflow-x:auto;border:1px solid #e1e0d9}"
            f".chart svg{{display:block;width:{width}px;max-width:none;height:auto}}"
            "table{border-collapse:collapse;width:100%;margin:8px 0 18px}td,th{border:1px solid #e1e0d9;padding:3px 5px;"
            "font-size:12px;text-align:left;vertical-align:top}th{background:#f2f1ed}tr.g td{background:#f2f1ed;"
            "font-weight:bold}.notice{color:#52514e}</style></head><body>"
            f"<h1>A5 bid programme — Gantt ({esc(prog['stage'])})</h1>"
            f"<p class=\"notice\">{esc(NOTICE)}</p>"
            f"<p><b>Planning basis.</b> {esc(prog.get('planning_basis', ''))}</p>"
            f"<p><b>{esc(NO_LEVELLING[0].upper() + NO_LEVELLING[1:])}.</b></p>"
            f"<p class=\"notice\">The chart is shown {width} px wide so that its smallest text is at least "
            f"{_n(HTML_MIN_FONT_PX)} px; scroll it sideways. gantt.pdf (one A3 page) and gantt.svg are the same drawing.</p>"
            f"<div class=\"chart\">{svg_text}</div>"
            "<h2>Legend</h2><ul>" + "".join(f"<li>{esc(x)}</li>" for x in legend) + "</ul>"
            "<h2>Rows (every A1 requirement id)</h2><table><tr><th>Activity</th><th>A1 requirement ids</th>"
            "<th>Predecessors</th><th>ES</th>"
            "<th>EF</th><th>LS</th><th>LF</th><th>Float (WD)</th><th>Timing</th><th>Decision</th>"
            "<th>Clarification questions (drafted, not sent)</th><th>Resource</th>"
            "<th>Duration / effort</th><th>Waits on</th><th>Role</th><th>Flags</th></tr>" + "".join(rows) + "</table>"
            "<h2>Milestones</h2><table><tr><th>Date</th><th>Milestone</th><th>Source</th><th>Kind</th></tr>"
            + "".join(ms) + "</table>"
            f"<h2>Overloads ({len(ov)}; reported, not resolved)</h2><ul>" + ("".join(ov) or "<li>none</li>") + "</ul>"
            "</body></html>\n")


def write(prog: dict, a5_dir: Path) -> list[Path]:
    a5_dir = Path(a5_dir)
    a5_dir.mkdir(parents=True, exist_ok=True)
    s = svg(prog)
    paths = [a5_dir / "gantt.svg", a5_dir / "gantt.html", a5_dir / "gantt.pdf"]
    paths[0].write_text(s, encoding="utf-8")
    paths[1].write_text(html(prog, s), encoding="utf-8")
    paths[2].write_bytes(pdf_bytes(prog))
    return paths
