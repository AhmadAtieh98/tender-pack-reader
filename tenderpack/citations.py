"""Citations written in addendum text, resolved to unit ids.

Used to verify that an operation's declared target is the clause the addendum itself names
(PLAN §4.4.1): a matching quotation and a change confined to the target prove only that an
operation is internally consistent; the citation is independent evidence of intent.

Recognised forms (as written in the pack; extend the patterns, not the outcomes):
  Volume I Clause 6.1 · Volume II Table 2-4 · Table 1-1 of Volume I · Footnote 12 to Volume I Clause 8.5
  Clause 8.5 footnote 12 · footnote 12 to Clause 8.5 (volume from the same sentence)
  Volume II Section 3 · Section 4.2 of Addendum No. 1 · Addendum No. 1 Section 4 · Form 4-A
  "the list at Volume I Clause 9.1 ... after item (e)" -> the list item VOL-I:9.1(e)
  a parenthesised abbreviation such as "(TN)" names a row of a cited table whose key matches
  (session 06 blind rehearsal) Appendix A to Addendum No. 1 · clarification request 13 in Addendum No. 2 ·
  "in row 2-6.2" · "the entry against 'Proposal Due Date'" · "the fifth numbered declaration" (-> decl5)
  (session 08 blind rehearsal) Volume I Appendix 3 · "the rows 'Model auditor' and 'Date of model audit opinion'"
  (session 09) "the Index of Forms in Volume IV" -> "VOL-IV:index" (kind index): the volume's index table, which
  only the unit metadata can name (is_index_table: its first column is "Form" and it has a "Title" column; the
  amendment engine resolves it); "the entry for Form 4-F" names the index row keyed "4-F"; after_row() reads the
  row an insertion follows ("after the entry for Form 4-F" -> "4-F")
A bare "Clause 4.2" takes its volume from the nearest preceding volume citation in the same text.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from .textnorm import normalize_latin

VOLUMES = {"I": "VOL-I", "II": "VOL-II", "III": "VOL-III", "IV": "VOL-IV", "V": "VOL-V"}
_VOL = r"Volume (I{1,3}|IV|V)\b"


@dataclass(frozen=True)
class Citation:
    text: str
    target: str          # unit id or group id (e.g. "VOL-IV:F4-A", "ADD-01:S4", "VOL-II:S3")
    kind: str            # clause | table | footnote | section | form | addendum_section | list_item | row


def _addendum(n: str) -> str:
    return f"ADD-{int(n):02d}"


def citations(text: str) -> list[Citation]:
    t = normalize_latin(text)
    out: list[Citation] = []
    seen: set[tuple[int, str]] = set()

    def add(m, target, kind, start=None):
        key = (m.start() if start is None else start, target)
        if key not in seen:
            seen.add(key)
            out.append((m.start(), Citation(m.group(0), target, kind)))

    for m in re.finditer(r"Footnote (\d+) to " + _VOL + r" Clause (\d+(?:\.\d+)*)", t, re.I):
        add(m, f"{VOLUMES[m.group(2)]}:{m.group(3)}#fn{m.group(1)}", "footnote")
    for m in re.finditer(_VOL + r" Clause (\d+(?:\.\d+)*)", t):
        add(m, f"{VOLUMES[m.group(1)]}:{m.group(2)}", "clause")
    # session 11 (blind-05, post-key): the plural list "Volume I Clauses 6.6 and 6.7", "Clauses 3.1, 3.2 and 3.4",
    # "Clauses 29.1 to 29.3" cites every clause listed (a range cites its two ends; the clauses between are not
    # inferred: an op that means them names them)
    for m in re.finditer(_VOL + r" Clauses ((?:\d+(?:\.\d+)*)(?:(?:,\s*|\s+and\s+|\s+to\s+)\d+(?:\.\d+)*)*)", t):
        for n in re.findall(r"\d+(?:\.\d+)*", m.group(2)):
            add(m, f"{VOLUMES[m.group(1)]}:{n}", "clause")
    for m in re.finditer(_VOL + r" Table (\d+-\d+)", t):
        add(m, f"{VOLUMES[m.group(1)]}:T{m.group(2)}", "table")
    for m in re.finditer(r"Table (\d+-\d+) of " + _VOL, t):
        add(m, f"{VOLUMES[m.group(2)]}:T{m.group(1)}", "table")
    # a table an addendum issued: "Table 1-1 (revised) and the Notes to it, issued by Section 3 of Addendum No. 2"
    # names the issue of Table 1-1 that lives under that addendum (ADD-02:T1-1-rev), resolved by resolve() (session 10)
    for m in re.finditer(r"Table (\d+-\d+)(?: \((?:revised|second revision|third revision|as revised)\))?[^.;]{0,80}?"
                         r"\b(?:issued|published|set out|reissued|introduced) (?:by|in|under|at) (?:Section \d+(?:\.\d+)? of )?"
                         r"Addendum No\.? ?(\d+)", t, re.I):
        add(m, f"{_addendum(m.group(2))}:T{m.group(1)}", "table")
    for m in re.finditer(_VOL + r" Section (\d+)\b", t):
        add(m, f"{VOLUMES[m.group(1)]}:S{m.group(2)}", "section")
    for m in re.finditer(r"Section (\d+\.\d+) of Addendum No\.? ?(\d+)", t, re.I):
        add(m, f"{_addendum(m.group(2))}:{m.group(1)}", "addendum_section")
    for m in re.finditer(r"Addendum No\.? ?(\d+),? Section (\d+)\b(?!\.\d)", t, re.I):
        add(m, f"{_addendum(m.group(1))}:S{m.group(2)}", "addendum_section")
    for m in re.finditer(r"\bForm (\d-[A-Z])\b", t, re.I):             # a heading prints "FORM 4-C" (session 09)
        add(m, f"VOL-IV:F{m.group(1).upper()}", "form")
    for m in re.finditer(_VOL + r" Appendix (\d+|[A-Z])\b", t):
        add(m, f"{VOLUMES[m.group(1)]}:App{m.group(2)}", "appendix")
    for m in re.finditer(r"\bAppendix ([A-Z])\b,? (?:to|of) Addendum No\.? ?(\d+)", t, re.I):
        add(m, f"{_addendum(m.group(2))}:App{m.group(1).upper()}", "appendix")
    for m in re.finditer(r"\bclarification requests? (\d+) (?:in|of|to) Addendum No\.? ?(\d+)", t, re.I):
        add(m, f"{_addendum(m.group(2))}:Q{m.group(1)}", "answer")
    for m in re.finditer(r"\bIndex of Forms (?:in|of|to) " + _VOL, t):                 # session 09
        add(m, f"{VOLUMES[m.group(1)]}:index", "index")
    # bare "Clause N" after a volume citation in the same text
    last_vol = None
    for m in re.finditer(_VOL + r"|\bClause (\d+(?:\.\d+)*)", t):
        if m.group(1):
            last_vol = VOLUMES[m.group(1)]
        elif last_vol and not re.search(r"(Volume (?:I{1,3}|IV|V)|Footnote \d+ to Volume (?:I{1,3}|IV|V))\s*$", t[:m.start()]):
            add(m, f"{last_vol}:{m.group(2)}", "clause")
            fn = re.search(r"footnote (\d+) to\s*$", t[:m.start()], re.I)
            if fn:                                                    # "footnote 12 to Clause 8.5"
                add(m, f"{last_vol}:{m.group(2)}#fn{fn.group(1)}", "footnote", start=m.start() + 1)
    # "Clause 8.5 footnote 12": a footnote named after its clause
    for m in re.finditer(r"Clause (\d+(?:\.\d+)*),? footnote (\d+)", t, re.I):
        clause = next((c.target for p, c in sorted(out, key=lambda x: x[0]) if p <= m.start() and c.kind == "clause"
                       and c.target.endswith(":" + m.group(1))), None)
        if clause:
            add(m, f"{clause}#fn{m.group(2)}", "footnote")
    # list item: "... Clause 9.1 ... after item (e)"
    for m in re.finditer(r"(?:after|before) item \(([a-z]{1,3})\)", t):
        clauses = [c for _, c in out if c.kind == "clause"]
        if clauses:
            add(m, f"{clauses[-1].target}({m.group(1)})", "list_item")
    out.sort(key=lambda x: x[0])
    return [c for _, c in out]


def row_names(text: str) -> list[str]:
    """Names a provision gives a table row: a parenthesised abbreviation ('Total Nitrogen (TN)' -> 'TN') or the row's
    reference after the word 'row' ('in row 2-6.2' -> '2-6.2'; session 06)."""
    t = normalize_latin(text)
    names = re.findall(r"\(([A-Z][A-Za-z0-9]{0,7})\)", t) + re.findall(r"\brow (\d[\w-]*(?:\.\d+)*)", t)
    names += re.findall(r"\b(?:entry|field|line) (?:against|for) ['\"]([^'\"]+)['\"]", t)
    for m in re.finditer(r"\b(?:rows?|fields?|entries|entry) ((?:['\"][^'\"]+['\"](?:,? and |, )?)+)", t):   # the rows 'A' and 'B'
        names += re.findall(r"['\"]([^'\"]+)['\"]", m.group(1))
    names += [f"decl{_ORDINALS.index(m.group(1).lower()) + 1}"
              for m in re.finditer(r"\b(" + "|".join(_ORDINALS) + r") (?:numbered )?declaration\b", t, re.I)]
    names += re.findall(r"\b(?:entry|row|line) for Form (\d+-[A-Z]+)\b", t)     # an index row (session 09)
    return names


def after_row(text: str) -> str | None:
    """The row an insertion follows, by the name the provision gives it: 'after the entry for Form 4-F' -> '4-F';
    "after the row 'TN'" -> 'TN'. None when the provision names no row to follow (session 09)."""
    t = normalize_latin(text)
    m = re.search(r"\bafter (?:the )?((?:entry|row|line|field) (?:for|against) (?:Form \d+-[A-Z]+\b|['\"][^'\"]+['\"])"
                  r"|(?:entry|row|line|field) ['\"][^'\"]+['\"])", t)
    names = row_names(m.group(1)) if m else []
    return names[0] if names else None


def is_index_table(columns: list[str]) -> bool:
    """An index of forms: a table whose first column is 'Form' and which has a 'Title' column (the VOL-IV cover table
    'Form | Title | Envelope | Status')."""
    cols = [normalize_latin(c).strip().lower() for c in columns or []]
    return bool(cols) and cols[0] == "form" and "title" in cols


_ORDINALS = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]


def _slug(s) -> str:
    return re.sub(r"[^a-z0-9]+", "-", normalize_latin(str(s or "")).lower()).strip("-")


def resolve(cites: list[Citation], unit_ids: set[str]) -> list[str]:
    """Targets that exist, as unit ids or as group prefixes of existing units."""
    out = []
    for c in cites:
        t = c.target
        if t in unit_ids or any(u.startswith(t + "/") or u.startswith(t + "(") for u in unit_ids):
            out.append(t)
        elif c.kind == "clause" and t not in unit_ids and any(u.startswith(t + ".") for u in unit_ids):
            # a whole clause cited ("Volume V Clause 29") that the volume prints only as sub-clauses 29.1, 29.2 ...
            out += sorted((u for u in unit_ids if u.startswith(t + ".") and u[len(t) + 1:].split("/")[0].isdigit()),
                          key=lambda u: int(u[len(t) + 1:].split("/")[0]))
        elif c.kind in ("section", "addendum_section"):
            doc, sec = t.split(":")
            if f"{doc}:H:{sec}" in unit_ids:
                out.append(t)
        elif c.kind == "form":
            # a form that an addendum inserted lives under the addendum's id (ADD-02:F4-G), not under Volume IV; every
            # issue of it is a candidate (the op names which one it targets or replaces) (session 09)
            local = t.split(":", 1)[1]
            out += sorted({u.split(":", 1)[0] + ":" + local for u in unit_ids if u.split(":", 1)[1].startswith(local + "/")})
        elif c.kind == "table" and ":" in t:
            # a table an addendum issued carries a suffix in that addendum (ADD-02:T1-1-rev): the citation names the
            # addendum and the table number, the group id is whatever that addendum printed (session 10)
            doc, local = t.split(":", 1)
            pat = re.compile(r"^" + re.escape(local) + r"(?:-[A-Za-z0-9]+)?$")
            out += sorted({f"{doc}:{u.split(':', 1)[1].split('/')[0]}" for u in unit_ids
                           if u.split(":", 1)[0] == doc and "/" in u.split(":", 1)[1] and pat.match(u.split(":", 1)[1].split("/")[0])})
    return list(dict.fromkeys(out))                 # a target named twice (body and heading) is listed once


def verify_target(target: str, text: str, unit_ids: set[str], row_label_of=None) -> tuple[bool, str, list[str]]:
    """Is `target` the unit the provision text cites? Returns (ok, reason, cited targets).

    A row of a cited table is accepted only if the provision also names the row (e.g. '(TN)').
    `row_label_of(unit_id)` returns the row's key/label (for matching names)."""
    cites = citations(text)
    cited = resolve(cites, unit_ids)
    if not cited:
        return False, "the provision cites no clause, table, form or section that exists in the pack", cited
    if target in cited:
        return True, f"declared target {target} is cited", cited
    names = row_names(text)
    for c in cited:
        if target.startswith(c + "/"):
            label = row_label_of(target) if row_label_of else target.rsplit("/", 1)[-1]
            keys = {_slug(label), _slug(target.rsplit("/", 1)[-1])} - {""}
            if label in names or keys & {_slug(n) for n in names}:
                return True, f"declared target {target} is row '{label}' of cited {c}", cited
            if [u for u in unit_ids if u.startswith(c + "/")] == [target]:     # session 08: 'Volume I Appendix 3' = its one paragraph
                return True, f"declared target {target} is the only unit of cited {c}", cited
            return False, f"declared target {target} is a row of cited {c}, but the provision does not name it", cited
    return False, f"declared target {target} is not cited; the provision cites {cited}", cited
