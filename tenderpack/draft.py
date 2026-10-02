"""Pattern drafter: proposes ops for an addendum from the wording of its provisions.

It never applies anything and never decides meaning. Every op it writes is `origin: pattern`,
`review: proposed`. Provisions it cannot type become `unresolved` with their text, so nothing is
silently dropped (a person then writes the op or a disposition). The same drafter is used for the
existing addenda (whose op files were then curated) and for any future addendum.

Phrasings recognised (taken from the pack's addenda; extend with new phrasings, never with outcomes):
  "<Volume X Clause N> is amended by deleting '<old>' and substituting '<new>'"          replace_text
  "In <Volume X Clause N>, '<old>' is deleted and '<new>' is substituted"                  replace_text
  "<Volume X Clause N> is amended by adding at the end: '<text>'"                          append_text
  "<Volume X Clause N> (...) is deleted in its entirety"                                   set_status deleted
  "<Volume X Clause N>, deleted by ..., is reinstated in the following amended form: '..'" set_status reinstated
  "Section N.M of Addendum No. K ceases to have effect"                                    set_status revoked
  "In <Volume X Table T>, the <column> for <name> (<ROW>) is amended from the value shown to <value>"  set_value
  "Table T of Volume X is deleted and replaced by the table below"                          replace_unit
  "Form F is reissued below"                                                                replace_unit
  "A new Form F is added to Volume IV and to the list at <Volume X Clause N>, to be inserted after item (x)"  insert_unit
  "The <thing> stated in <Volume X Clause N> is amended to <restated words>"                replace_text, old located
        in the target by the restated words' shape (the addendum does not quote the old words: flagged)
  "The <thing> in <Volume X Clause N> is unchanged at <words>"                              annotate confirms
  the addendum's own cover date line, recitals, and minutes it declares non-binding        no_effect
"""
from __future__ import annotations

import re

from .amend import PROVISION_KINDS, Disposition, Op, OpFile, UState, base_state, heading_of
from .citations import citations, row_names
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
        head = heading_of(order, st, p)
        oid = f"{addendum}/{p.split(':', 1)[1]}"
        mk = lambda **kw: Op(id=oid, provision=p, origin="pattern", review="proposed", **kw)  # noqa: E731
        m = (re.search(r"(Volume \S+ Clause [\d.]+) is amended by deleting " + Q + " and substituting " + Q, t) or
             re.search(r"In (Volume \S+ (?:Clause|Table) [\d.-]+), " + Q + " is deleted and " + Q + " is substituted", t))
        if m:
            ops.append(mk(type="replace_text", target=_target(m.group(1)) or _target(m.group(1), "table"),
                          old=m.group(2), new=m.group(3)))
            continue
        m = re.search(r"(Volume \S+ Clause [\d.]+) is amended by adding at the end: " + Q + r"\s*$", t)
        if m:
            ops.append(mk(type="append_text", target=_target(m.group(1)), new=m.group(2)))
            continue
        m = re.search(r"(Volume \S+ Clause [\d.]+)(?: \([^)]*\))? is deleted in its entirety", t)
        if m:
            ops.append(mk(type="set_status", target=_target(m.group(1)), status="deleted"))
            continue
        m = re.search(r"(Volume \S+ Clause ([\d.]+)), deleted by (Addendum No\. ?\d+ Section \d+), is reinstated in the "
                      r"following amended form: " + Q + r"\s*$", t)
        if m:
            new_text = re.sub(r"^" + re.escape(m.group(2)) + r"\s+", "", m.group(4)).strip()
            ops.append(mk(type="set_status", target=_target(m.group(1)), status="reinstated", new_text=new_text,
                          claims=[{"unit": _target(m.group(1)), "status": "deleted",
                                   "by_provision_prefix": _target(m.group(3), "addendum_section").replace(":S", ":")}]))
            continue
        m = re.search(r"^Section (\d+\.\d+) of Addendum No\. ?(\d+) ceases to have effect", t)
        if m:
            ops.append(mk(type="set_status", target=f"ADD-{int(m.group(2)):02d}:{m.group(1)}", status="revoked"))
            continue
        m = re.search(r"In (Volume \S+ Table [\d-]+), the (\w+) for (.+?) is amended from the value shown to (.+?), "
                      r"assessed on the same basis", t)
        if m:
            table = _target(m.group(1), "table")
            names = row_names(m.group(3))
            rows = [k for k in st if k.startswith(table + "/") and st[k].label in names]
            col = next((c for c in (st[rows[0]].cells or {}) if c.lower() == m.group(2).lower()), m.group(2).title()) if rows else m.group(2)
            ops.append(mk(type="set_value", target=rows[0] if rows else f"{table}/?", column=col, new=_value(m.group(4)),
                          note=f"'assessed on the same basis': the other cells of the row are unchanged; new value read "
                               f"from '{m.group(4)}'"))
            continue
        m = re.search(r"(Table [\d-]+ of Volume \S+) is deleted and replaced by the table below", t)
        if m:
            target = _target(m.group(1), "table")
            repl = _next_table(st, order, p, addendum)
            ops.append(mk(type="replace_unit", target=target, replacement=repl,
                          covers=[k for k in provs if repl and k.startswith(repl + "/") and st[k].kind == "table_row"]))
            covered.update(ops[-1].covers)
            continue
        m = re.search(r"^Form (\d-[A-Z]) is reissued below", t)
        if m:
            group = p.rsplit("/", 1)[0]
            content = [k for k in provs if k.startswith(group + "/") and k != p]
            ops.append(mk(type="replace_unit", target=f"VOL-IV:F{m.group(1)}", replacement=group, covers=content,
                          issue="the reissued form may differ from the original in more than its stated purpose; compare"))
            covered.update(content)
            continue
        m = re.search(r"A new Form (\d-[A-Z]) is added to Volume IV and to the list at (Volume \S+ Clause [\d.]+), to be "
                      r"inserted after item \((\w+)\)", t)
        if m:
            clause = _target(m.group(2))
            group = f"{addendum}:F{m.group(1)}"
            content = [k for k in provs if k.startswith(group + "/")]
            ops.append(mk(type="insert_unit", new_group=group, anchor=f"{clause}({m.group(3)})",
                          new_text_from=f"{addendum}:H:F{m.group(1)}", covers=content,
                          issue=f"re-lettering of the items after ({m.group(3)}) is not stated"))
            covered.update(content)
            continue
        m = re.search(r"stated in (Volume \S+ Clause [\d.]+) is amended to (.+?)\.?$", t)
        if m and _target(m.group(1)) in st:
            target = _target(m.group(1))
            new = m.group(2).strip()
            found = list(_shape(new).finditer(normalize_latin(st[target].text)))
            if len(found) == 1:
                ops.append(mk(type="replace_text", target=target, old=found[0].group(0), new=new,
                              old_resolved="matched_in_target",
                              issue="the addendum restates the value without quoting the old words; the old words were "
                                    "located in the target by shape and need a person's check"))
                continue
        m = re.search(r"in (Volume \S+ Clause [\d.]+) is unchanged at (.+?)\.?$", t)
        if m:
            ops.append(mk(type="annotate", targets=[_target(m.group(1))], effect="confirms",
                          expect=[{"unit": _target(m.group(1)), "contains": m.group(2).strip()}]))
            continue
        # dispositions the drafter can justify from the addendum's own words
        if p == cover_line:
            disp.append(Disposition(provision=p, disposition="no_effect", origin="pattern",
                                    reason="the addendum's issue date line (used as the stage date)"))
        elif re.search(r"RECITALS", head) or p.startswith(f"{addendum}:cover/"):
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
                  method="tenderpack.draft patterns; every op proposed, none applied by the drafter", ops=ops,
                  dispositions=disp)


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
