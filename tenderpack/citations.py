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
    for m in re.finditer(_VOL + r" Table (\d+-\d+)", t):
        add(m, f"{VOLUMES[m.group(1)]}:T{m.group(2)}", "table")
    for m in re.finditer(r"Table (\d+-\d+) of " + _VOL, t):
        add(m, f"{VOLUMES[m.group(2)]}:T{m.group(1)}", "table")
    for m in re.finditer(_VOL + r" Section (\d+)\b", t):
        add(m, f"{VOLUMES[m.group(1)]}:S{m.group(2)}", "section")
    for m in re.finditer(r"Section (\d+\.\d+) of Addendum No\.? ?(\d+)", t, re.I):
        add(m, f"{_addendum(m.group(2))}:{m.group(1)}", "addendum_section")
    for m in re.finditer(r"Addendum No\.? ?(\d+),? Section (\d+)\b(?!\.\d)", t, re.I):
        add(m, f"{_addendum(m.group(1))}:S{m.group(2)}", "addendum_section")
    for m in re.finditer(r"\bForm (\d-[A-Z])\b", t):
        add(m, f"VOL-IV:F{m.group(1)}", "form")
    for m in re.finditer(_VOL + r" Appendix (\d+|[A-Z])\b", t):
        add(m, f"{VOLUMES[m.group(1)]}:App{m.group(2)}", "appendix")
    for m in re.finditer(r"\bAppendix ([A-Z])\b,? (?:to|of) Addendum No\.? ?(\d+)", t, re.I):
        add(m, f"{_addendum(m.group(2))}:App{m.group(1).upper()}", "appendix")
    for m in re.finditer(r"\bclarification requests? (\d+) (?:in|of|to) Addendum No\.? ?(\d+)", t, re.I):
        add(m, f"{_addendum(m.group(2))}:Q{m.group(1)}", "answer")
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
    return names


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
    return out


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
