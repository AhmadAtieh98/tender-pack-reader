"""Pattern drafter: proposes ops for an addendum from the wording of its provisions.

It never applies anything and never decides meaning. Every op it writes is `origin: pattern`,
`review: proposed`. Provisions it cannot type become `unresolved` with their text, so nothing is
silently dropped (a person then writes the op or a disposition). A provision may hold several changes:
each recognised change becomes its own op, and any remaining text that states something (other than
"... is unchanged" and connecting words) is flagged `unresolved` with that text. The same drafter is used for the
existing addenda (whose op files were then curated) and for any future addendum.

Phrasings recognised (taken from the pack's addenda; extend with new phrasings, never with outcomes):
  "<Volume X Clause N>[, as amended by ...,] is [further] amended by deleting '<old>' and substituting '<new>'"
                                                                                          replace_text
  "In [footnote N to] <Volume X Clause N>[, as reinstated by ...,] '<old>' is deleted and '<new>' is substituted"
                                                                                          replace_text
  "<Volume X Clause N> is amended by adding at the end: '<text>'"                          append_text
  "<Volume X Clause N> (...) is deleted in its entirety"                                   set_status deleted
  "<Volume X Clause N>, deleted by ..., is reinstated in the following amended form: '..'" set_status reinstated
  "Section N.M of Addendum No. K ceases to have effect"                                    set_status revoked
  "In <Volume X Table T>, the <column> for <name> (<ROW>) is amended from the value shown to <value>"  set_value
  "Table T of Volume X is deleted and replaced by the table below"                          replace_unit
  "Form F is reissued below"                                                                replace_unit
  "A new Form F is added to Volume IV and to the list at <Volume X Clause N>, to be inserted after item (x)"  insert_unit
  "The Index of Forms in Volume IV is amended by adding, after the entry for Form F, an entry for Form G with the title
   '<t>', Envelope '<e>' and Status '<s>'"                                                  insert_row (session 09)
  "The <thing> stated in <Volume X Clause N> is amended to <restated words>"                replace_text, old located
        in the target by the restated words' shape (the addendum does not quote the old words: flagged)
  "The <thing> in <Volume X Clause N> is unchanged at <words>"                              annotate confirms
  "Bidders shall acknowledge receipt in Form F"                                            annotate adds_obligation
  "<Volume X Clause N> is deleted and replaced by the following: 'N <text>'"                replace_text (whole clause)
  "The following [new] Clause N is added to / inserted in Volume X after Clause M: 'N <text>'"  insert_unit after Clause M
  the addendum's own cover date line, recitals, and minutes it declares non-binding        no_effect

Cover text (session 07): the addendum's summary of itself ("This Addendum amends ..., deletes ...") is never drafted;
C28 (tenderpack/summary.py) compares it with the provisions and reports differences. From the rest of the cover the
drafter takes only the obligations it states; a change stated in cover text is left unresolved for a person.
"""
from __future__ import annotations

import re

from .amend import PROVISION_KINDS, Disposition, Op, OpFile, UState, base_state, heading_of
from .citations import VOLUMES, citations, is_index_table, row_names
from .summary import SUMMARY_RE
from .textnorm import normalize_latin

Q = r"[‘'\"](.+?)[’'\"]"


def _clean(s: str) -> str:
    return s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')


def _target(text: str, kind: str = "clause") -> str | None:
    c = [x.target for x in citations(text) if x.kind == kind]
    return c[0] if c else None


_NUMBER_WORDS = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                 "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
                 "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "thousand"}


def _shape(new: str) -> re.Pattern:
    """A pattern with the shape of restated words: number words and figures become wildcards, the rest literal."""
    parts = []
    for tok in re.findall(r"\(\d+(?:\.\d+)?%?\)|\d+(?:\.\d+)?%?|[A-Za-z]+(?:-[A-Za-z]+)*|[^\sA-Za-z\d]", new):
        if re.fullmatch(r"\(?\d+(?:\.\d+)?%?\)?", tok):
            parts.append(r"\(\d+(?:\.\d+)?%?\)" if tok.startswith("(") else r"\d+(?:\.\d+)?%?")
        elif all(w.lower() in _NUMBER_WORDS for w in tok.split("-")):
            parts.append(r"[a-z]+(?:-[a-z]+)*")
        else:
            parts.append(re.escape(tok))
    return re.compile(r"\s*".join(parts))


def _matches(t: str, p: str, st: dict[str, UState], order: list[str], provs: list[str], addendum: str) -> list[tuple]:
    """Every recognised change in the provision text: [(start, end, op fields, covered provisions)].
    A paragraph may hold several changes; each becomes its own op."""
    out = []
    I = re.I

    def add(m, covered=(), **kw):
        out.append((m.start(), m.end(), kw, list(covered)))

    # session 06 live fix (blind rehearsal): a citation may carry a qualifier ("as amended by Addendum No. 1 Section
    # 2.1", "as reinstated by ...") and a change may be "further" amended; a footnote may be the target
    qual = r"(?:, as (?:further )?(?:amended|reinstated|corrected) by [^,‘'\"]+?)?"
    for m in re.finditer(r"(Volume \S+ Clause [\d.]+)" + qual + r",? is (?:further )?amended by deleting " + Q + " and substituting " + Q, t):
        add(m, type="replace_text", target=_target(m.group(1)), old=m.group(2), new=m.group(3))
    for m in re.finditer(r"\bIn ((?:footnote \d+ to )?Volume \S+ (?:Clause|Table) [\d.-]+)" + qual + ", " + Q
                         + " is deleted and " + Q + " is substituted", t, I):
        tgt = (_target(m.group(1), "footnote") if m.group(1).lower().startswith("footnote") else None) \
            or _target(m.group(1)) or _target(m.group(1), "table")
        add(m, type="replace_text", target=tgt, old=m.group(2), new=m.group(3))
    for m in re.finditer(r"(Volume \S+ Clause [\d.]+) is amended by adding at the end: " + Q + r"\s*$", t):
        add(m, type="append_text", target=_target(m.group(1)), new=m.group(2))
    for m in re.finditer(r"(Volume \S+ Clause [\d.]+)(?: \([^)]*\))? is deleted in its entirety", t):
        add(m, type="set_status", target=_target(m.group(1)), status="deleted")
    for m in re.finditer(r"(Volume \S+ Clause ([\d.]+)), deleted by (Addendum No\. ?\d+ Section \d+), is reinstated in the "
                         r"following amended form: " + Q + r"\s*$", t):
        new_text = re.sub(r"^" + re.escape(m.group(2)) + r"\s+", "", m.group(4)).strip()
        add(m, type="set_status", target=_target(m.group(1)), status="reinstated", new_text=new_text,
            claims=[{"unit": _target(m.group(1)), "status": "deleted",
                     "by_provision_prefix": _target(m.group(3), "addendum_section").replace(":S", ":")}])
    for m in re.finditer(r"(?:^|(?<=\. ))Section (\d+\.\d+) of Addendum No\. ?(\d+) ceases to have effect", t):
        add(m, type="set_status", target=f"ADD-{int(m.group(2)):02d}:{m.group(1)}", status="revoked")
    for m in re.finditer(r"\bIn (Volume \S+ Table [\d-]+), the (\w+) for (.+?) is amended from the value shown to (.+?), "
                         r"assessed on the same basis", t, I):
        table = _target(m.group(1), "table")
        names = row_names(m.group(3))
        rows = [k for k in st if k.startswith(table + "/") and st[k].label in names]
        col = next((c for c in (st[rows[0]].cells or {}) if c.lower() == m.group(2).lower()), m.group(2).title()) if rows else m.group(2)
        add(m, type="set_value", target=rows[0] if rows else f"{table}/?", column=col, new=_value(m.group(4)),
            note=f"'assessed on the same basis': the other cells of the row are unchanged; new value read from '{m.group(4)}'")
    for m in re.finditer(r"(Table [\d-]+ of Volume \S+) is deleted and replaced by the table below", t):
        repl = _next_table(st, order, p, addendum)
        covers = [k for k in provs if repl and k.startswith(repl + "/") and st[k].kind == "table_row"]
        add(m, covers, type="replace_unit", target=_target(m.group(1), "table"), replacement=repl, covers=covers)
    for m in re.finditer(r"(?:^|(?<=\. ))Form (\d-[A-Z]) is reissued below", t):
        group = p.rsplit("/", 1)[0]
        content = [k for k in provs if k.startswith(group + "/") and k != p]
        add(m, content, type="replace_unit", target=f"VOL-IV:F{m.group(1)}", replacement=group, covers=content,
            issue="the reissued form may differ from the original in more than its stated purpose; compare")
    for m in re.finditer(r"A new Form (\d-[A-Z]) is added to Volume IV and to the list at (Volume \S+ Clause [\d.]+), to be "
                         r"inserted after item \((\w+)\)", t):
        clause = _target(m.group(2))
        group = f"{addendum}:F{m.group(1)}"
        content = [k for k in provs if k.startswith(group + "/")]
        add(m, content, type="insert_unit", new_group=group, anchor=f"{clause}({m.group(3)})",
            new_text_from=f"{addendum}:H:F{m.group(1)}", covers=content,
            issue=f"re-lettering of the items after ({m.group(3)}) is not stated")
    # session 09: an index entry described in prose (the engine checks each cell against these words, C21)
    for m in re.finditer(r"(?:^|(?<=\. ))The Index of Forms in Volume (\S+) is amended by adding,? (?:after the entry for "
                         r"Form (\d+-[A-Z]+),? )?an entry for Form (\d+-[A-Z]+) with (.+?)\.?$", t):
        doc = VOLUMES.get(m.group(1), "")
        head = lambda k: [c.strip() for c in (st[k].text or "").split("|") if c.strip()]  # noqa: E731
        tables = [k for k in order if k in st and st[k].doc == doc and st[k].kind == "table" and is_index_table(head(k))]
        if len(tables) != 1:
            continue                                  # no index table, or more than one: left to a person
        cols = head(tables[0])
        cells = {cols[0]: m.group(3)}
        for c in re.finditer(r"(?:^|,\s*|\s+and\s+)(?:the\s+)?([A-Za-z][A-Za-z ]*?)\s+'([^']+)'", m.group(4)):
            col = next((x for x in cols if x.lower() == c.group(1).strip().lower()), None)
            if col is None:
                cells = {}
                break
            cells[col] = c.group(2)
        after = next((k for k in order if k in st and st[k].parent == tables[0] and st[k].label == m.group(2)), None)
        if cells and (after or not m.group(2)):
            add(m, type="insert_row", target=tables[0], after=after, cells=cells)
    for m in re.finditer(r"(?:^|(?<=\. ))(The [^.]*?) stated in (Volume \S+ Clause [\d.]+) is amended to (.+?)\.?$", t):
        target = _target(m.group(2))
        if target in st:
            new_words = m.group(3).strip()
            found = list(_shape(new_words).finditer(normalize_latin(st[target].text)))
            if len(found) == 1:
                add(m, type="replace_text", target=target, old=found[0].group(0), new=new_words,
                    old_resolved="matched_in_target",
                    issue="the addendum restates the value without quoting the old words; the old words were "
                          "located in the target by shape and need a person's check")
    for m in re.finditer(r"(?:^|(?<=\. ))(The [^.]*?) in (Volume \S+ Clause [\d.]+) is unchanged at (.+?)\.?$", t):
        add(m, type="annotate", targets=[_target(m.group(2))], effect="confirms",
            expect=[{"unit": _target(m.group(2)), "contains": m.group(3).strip()}])
    # whole clause deleted and replaced (session 05 rehearsal: a change type not seen in ADD-01/ADD-02)
    for m in re.finditer(r"(Volume \S+ Clause ([\d.]+)) is deleted and replaced by the following: " + Q + r"\s*$", t):
        target = _target(m.group(1))
        new_text = re.sub(r"^" + re.escape(m.group(2)) + r"\s+", "", m.group(3)).strip()
        if target in st and st[target].status == "active":
            add(m, type="replace_text", target=target, old=st[target].text, old_resolved="matched_in_target", new=new_text,
                issue="the whole clause is replaced; compare the old and new text for anything dropped")
    # a new clause inserted after an existing one (session 05 rehearsal: unseen change type)
    for m in re.finditer(r"The following (?:new )?Clause ([\d.]+) is (?:added to|inserted in) (Volume \S+) after Clause ([\d.]+): "
                         + Q + r"\s*$", t):
        anchor = _target(f"{m.group(2)} Clause {m.group(3)}")
        new_text = re.sub(r"^" + re.escape(m.group(1)) + r"\s+", "", m.group(4)).strip()
        add(m, type="insert_unit", anchor=anchor, new_text=new_text,
            note=f"new Clause {m.group(1)} inserted after Clause {m.group(3)} (the engine names it {anchor}+{addendum})")
    for m in re.finditer(r"Bidders shall acknowledge receipt (?:of this Addendum )?in Form (\d-[A-Z])\.?", t):
        add(m, type="annotate", targets=[p], effect="adds_obligation",
            note=f"the addendum must be acknowledged in Form {m.group(1)}")
    # keep the earliest of overlapping matches
    out.sort(key=lambda x: (x[0], -x[1]))
    kept, last = [], -1
    for x in out:
        if x[0] >= last:
            kept.append(x)
            last = x[1]
    return kept


# A sentence is harmless only if it is, as a WHOLE, a statement that nothing changes or that the addendum is part
# of the RFP Documents (or, in cover text only, the addendum's summary of itself). Any exception, qualifier or
# obligation in it ("... unchanged except that each bidder shall ...") makes it substantive: it is left unresolved.
_BENIGN_WHOLE = [
    re.compile(r"[\w\s,()'’\-:/.]*?\b(?:is|are|remains?|shall remain) unchanged(?: at [^;]+?)?\.?", re.I),
    re.compile(r"this addendum (?:forms part of|is issued (?:under|pursuant to|in accordance with)|takes precedence)[^;]*?\.?",
               re.I),
]
_COVER_SUMMARY = re.compile(r"this addendum (?:amends|adds|deletes|reissues|publishes|responds|corrects|clarifies|withdraws|"
                            r"replaces|confirms)\b[^;]*?\.?", re.I)
_QUALIFIER = re.compile(r"\b(?:except|save|provided|unless|subject to|other than|but|however|notwithstanding|apart from|"
                        r"exception|instead|in addition|additionally|shall|must|required|mandatory|non-responsive|"
                        r"reject\w*|disqualif\w*|deemed)\b", re.I)
_FILLER = {"and", "or", "also", "further", "then", "in", "addition", "the", "following"}


def _benign(sentence: str, cover: bool = False) -> bool:
    s = sentence.strip(" ,;")
    if not s or _QUALIFIER.search(re.sub(r"\bshall remain unchanged\b", "", s, flags=re.I)):
        return False
    pats = _BENIGN_WHOLE + ([_COVER_SUMMARY] if cover else [])
    return any(p.fullmatch(s) for p in pats)


def _remainder(t: str, spans: list[tuple[int, int]], cover: bool = False) -> str:
    """Provision text no op accounts for, minus whole sentences that state nothing changes and connecting words."""
    keep, pos = [], 0
    for a, b in spans:
        keep.append(t[pos:a])
        keep.append(" | ")
        pos = b
    keep.append(t[pos:])
    rest = []
    for chunk in "".join(keep).split("|"):
        for sent in re.split(r"(?<=[.;])\s+", chunk):
            words = re.findall(r"[A-Za-z0-9']+", sent)
            if not words or all(w.lower() in _FILLER for w in words) or _benign(sent, cover):
                continue
            rest.append(sent.strip(" ,;"))
    return " ".join(rest).strip()


def draft(units: list[dict], addendum: str, prepared_by: str = "pattern drafter (tenderpack.draft)") -> OpFile:
    st = base_state(units, [addendum])
    order = [u["unit_id"] for u in units]
    for u in st.values():
        if u.doc == addendum:
            u.status = "active"
    provs = [k for k in order if st[k].doc == addendum and st[k].kind in PROVISION_KINDS]
    ops: list[Op] = []
    disp: list[Disposition] = []
    covered: set[str] = set()
    cover_line = next((k for k in provs if re.match(r"^Issued \d", st[k].text)), provs[0] if provs else "")
    nonbinding = _nonbinding_groups(st, provs)

    for p in provs:
        if p in covered:
            continue
        u = st[p]
        t = _clean(normalize_latin(u.text))
        cover = p.startswith(f"{addendum}:cover/")
        if cover:
            # the addendum's summary of itself is never drafted: C28 compares it with the provisions (session 07)
            t = SUMMARY_RE.sub(" ", t).strip()
        head = heading_of(order, st, p)
        oid = f"{addendum}/{p.split(':', 1)[1]}"
        found = _matches(t, p, st, order, provs, addendum)
        if cover:
            # cover text never drafts a change, only the obligations it states ("Bidders shall acknowledge receipt
            # in Form 4-A"); a change stated in the cover stays unresolved for a person (session 07)
            found = [f for f in found if f[2].get("type") == "annotate" and f[2].get("effect") == "adds_obligation"]
        if found:
            for i, (a, b, kw, cov) in enumerate(found):
                ops.append(Op(id=oid if len(found) == 1 else f"{oid}({chr(97 + i)})", provision=p, origin="pattern",
                              review="proposed", **kw))
                covered.update(cov)
            rest = _remainder(t, [(a, b) for a, b, _, _ in found], cover=cover)
            if rest:
                disp.append(Disposition(provision=p, disposition="unresolved", origin="pattern",
                                        reason=("cover text the drafter never applies (a person decides): " if cover
                                                else "text not covered by any op: ") + f"'{rest[:240]}'",
                                        candidates=[c.target for c in citations(rest)]))
            continue
        # dispositions the drafter can justify from the addendum's own words
        if p == cover_line:
            disp.append(Disposition(provision=p, disposition="no_effect", origin="pattern",
                                    reason="the addendum's issue date line (used as the stage date)"))
        elif re.search(r"RECITALS", head) or p.startswith(f"{addendum}:cover/"):
            rest = _remainder(t, [], cover=True)
            if rest and (_QUALIFIER.search(rest) or re.search(r"\b(?:amended|deleted|substituted|replaced|added|inserted|"
                                                              r"extended|reduced|increased)\b", rest, re.I)):
                disp.append(Disposition(provision=p, disposition="unresolved", origin="pattern",
                                        reason=f"cover or recital text that states an obligation, exception or change: "
                                               f"'{rest[:240]}'", candidates=[c.target for c in citations(rest)]))
            else:
                disp.append(Disposition(provision=p, disposition="no_effect", origin="pattern",
                                        reason="recital or cover text; changes nothing by itself"))
        elif any(p.startswith(g) for g in nonbinding):
            src = next(v for g, v in nonbinding.items() if p.startswith(g))
            disp.append(Disposition(provision=p, disposition="no_effect", origin="pattern",
                                    reason=f"minutes declared non-binding by {src}; recorded as context only"))
        else:
            disp.append(Disposition(provision=p, disposition="unresolved", origin="pattern",
                                    reason="no recognised phrasing; a person must write the op or a disposition",
                                    candidates=[c.target for c in citations(u.text)]))
    return OpFile(addendum=addendum, issued_from=cover_line, prepared_by=prepared_by,
                  method="tenderpack.draft patterns; every op proposed, none applied by the drafter; a paragraph with "
                         "several recognised changes gives one op per change, and any remaining text is unresolved",
                  ops=ops, dispositions=disp)


def _value(s: str) -> str:
    m = re.match(r"\s*(-?\d+(?:\.\d+)?)", s)
    return m.group(1) if m else s.strip()


def _next_table(st: dict[str, UState], order: list[str], p: str, addendum: str) -> str | None:
    i = order.index(p)
    return next((k for k in order[i + 1:] if st[k].doc == addendum and st[k].kind == "table"), None)


def _nonbinding_groups(st: dict[str, UState], provs: list[str]) -> dict[str, str]:
    """'Statements recorded in the minutes at Appendix B ... do not bind the Authority' -> {group prefix: provision}."""
    out = {}
    for p in provs:
        m = re.search(r"minutes at Appendix (\w+).{0,120}do not bind", normalize_latin(st[p].text))
        if m:
            doc = st[p].doc
            out[f"{doc}:App{m.group(1)}/"] = p
    return out
