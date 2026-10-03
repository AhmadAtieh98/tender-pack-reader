"""C30 date coverage and C32 counting conventions (session 06).

C30: every date or period phrase printed in a unit in force at the validated stage (volume units, units the
register cites, and content an addendum inserts or reissues) is accounted for, as one of:
  rule          a row's date rule read from that unit, whose words are in the phrase's sentence (planned in A5 or
                computed in A1 Dates; a rule of kind `unresolved` is listed as NOT COMPUTED, with its reason)
  anchor        the unit defines a pack anchor (e.g. VOL-I 6.1 defines the Proposal Due Date)
  printed       a form field prints an anchor's date that differs from the effective one (C31 raises it as an issue)
  duration      the phrase is quoted in an interpretation of a row holding the unit and is not counted from or to an
                event: a duration that is part of the requirement itself (design life, storage hours, retention
                years), not a date to plan
  note          a row holding the unit declares it in `date_notes` (duration / post_award / not_a_date /
                unresolved, with a reason); `unresolved` notes are listed as NOT COMPUTED
  disposition   the unit carries no bidder obligation (definition, authority, informational, context; its reason)
Anything else is UNCOVERED: a C30 finding, a release blocker and an A3 issue. Nothing is guessed: a period the
program cannot compute stays explicitly unresolved.

C32: every relative date rule declares its unit, and where the pack does not state the counting convention every
reading is computed and shown (dates.interpretations); this reports which rules have more than one reading.
"""
from __future__ import annotations

import re

from .dispositions import effective_disposition, sentences
from .textnorm import normalize_latin

MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
DATE_PHRASE = re.compile(
    rf"\b\d{{1,2}} (?:{MONTHS}) \d{{4}}\b"
    r"|\b(?:[a-z]+(?:-[a-z]+)* )?\(\d+\) (?:Working Days?|calendar days?|days?|months?|years?|hours?|weeks?)\b"
    r"|\b\d+(?:[.,]\d+)? (?:Working Days|calendar days|days|months|years|hours|weeks)\b", re.I)
NO_OBLIGATION = ("definition", "authority", "informational", "context", "structural")
# a period counted from or to an event is a date to plan, never just a duration inside the requirement
RELATIVE = re.compile(r"\b(?:before|after|from|following|preceding|prior to|of|within)\b[^.;]{0,70}?\b(?:Date|PDD|Addendum|"
                      r"award|Award|Notice|PCOD|Financial Close|Effective|issue|issued|receipt|detection|request|Commencement|"
                      r"Commercial Operation|termination|expiry|signature|Agreement)\b")


def _n(t: str) -> str:
    return " ".join(normalize_latin(t or "").replace("'", "").lower().split())


def _core(phrase: str) -> str:
    """The '(n) unit' or 'n unit' part of a phrase, or the date itself."""
    m = re.search(r"\(\d+\) [A-Za-z ]+|\d+(?:[.,]\d+)? [A-Za-z ]+|\d{1,2} [A-Za-z]+ \d{4}", phrase)
    return (m.group(0) if m else phrase).strip()


def _parse(phrase: str):
    from .dates import parse_date
    try:
        v = parse_date(phrase)
        return v[0] if isinstance(v, tuple) else v
    except Exception:                                        # noqa: BLE001  (a period, not a calendar date)
        return None


def date_coverage(r: dict) -> list[dict]:
    st = r["validated"].state
    units = {u["unit_id"]: u for u in r["units"]}
    rows_by_unit: dict[str, list] = {}
    for e in r["evals"]:
        for u in e["row"].units:
            rows_by_unit.setdefault(u, []).append(e)
    cited = set(rows_by_unit)
    anchors = {a["defined_in"]: k for k, a in r["rowfile"].anchors.items() if a.get("defined_in")}
    content_ops = {x.op.id for s in r["stages"] for x in s.ops if x.op.type in ("insert_unit", "replace_unit")}
    from .dates import parse_date
    from .register import anchor_values, printed_date_conflicts
    printed = {c["unit"]: c for c in printed_date_conflicts(r["validated"], r["rowfile"].anchors)}
    anchor_now = {v: k for k, v in anchor_values(st, r["rowfile"].anchors, {}).items() if v}
    out = []
    for k, u in st.items():
        if u.status != "active":
            continue
        is_addendum = u.doc.startswith("ADD-")
        if is_addendum and k not in cited and not (set(u.history) & content_ops) and u.origin != "addendum_op":
            continue
        for sent in sentences(u.text or ""):
            for m in DATE_PHRASE.finditer(sent):
                phrase, core, ns = m.group(0), _core(m.group(0)), _n(sent)
                rec = {"unit": k, "phrase": phrase, "sentence": sent[:220]}
                rows = rows_by_unit.get(k, [])
                rule = next(((e["row"].id, dr) for e in rows for dr in e["row"].date_rules
                             if (dr.source_unit == k or k in e["row"].units)       # the rule's words, in a unit the row holds
                             and (_n(dr.text) in ns or _n(core) in _n(dr.text))), None)
                if rule is None:                     # a rule whose period an addendum changed is re-read (flagged)
                    rule = next(((e["row"].id, dr) for e in rows for dr in e["row"].date_rules if dr.source_unit == k
                                 and any(d["rule_id"] == dr.rule_id and (d.get("reread") or "").startswith("period re-read")
                                         for d in e["stages"][r["validated"].stage]["dates"])), None)
                note = next(((e["row"].id, dn) for e in rows for dn in e["row"].date_notes
                             if _n(core) in _n(dn.text) or _n(dn.text) in ns), None)
                quoted = next((e["row"].id for e in rows for it in e["row"].interpretations if _n(core) in _n(it.quote)), None)
                d = effective_disposition(units[k], r["dispositions"]) if k in units and not is_addendum else None
                if rule:
                    rid, dr = rule
                    rec.update(treatment="rule" if dr.kind != "unresolved" else "NOT COMPUTED",
                               by=f"{rid} {dr.rule_id}" + (f": {dr.note}" if dr.kind == "unresolved" else ""))
                elif k in printed:
                    rec.update(treatment="printed", by=f"prints the {printed[k]['anchor']} as {printed[k]['printed']}; the "
                               f"effective date is {printed[k]['effective']} (raised as an issue, C31; not corrected)")
                elif u.kind == "form_field" and _parse(phrase) in anchor_now:
                    rec.update(treatment="anchor", by=f"a form field printing the {anchor_now[_parse(phrase)]} as in force")
                elif k in anchors:
                    rec.update(treatment="anchor", by=f"defines {anchors[k]}")
                elif note:
                    rid, dn = note
                    rec.update(treatment="NOT COMPUTED" if dn.treatment == "unresolved" else dn.treatment,
                               by=f"{rid}: {dn.reason}")
                elif quoted and not RELATIVE.search(sent[m.start():]):
                    rec.update(treatment="duration", by=f"{quoted} quotes it as part of the requirement")
                elif d is not None and d.disposition in NO_OBLIGATION:
                    rec.update(treatment="disposition", by=f"{d.disposition}: {d.reason or ''}"[:160])
                else:
                    rec.update(treatment="UNCOVERED", by="no rule, anchor, quote, note or disposition accounts for it")
                out.append(rec)
    return out


def counting_conventions(r: dict) -> list[dict]:
    """C32: relative rules whose readings differ at the validated stage (the convention is not stated)."""
    v = r["validated"].stage
    return [{"row": e["row"].id, "rule": d["rule_id"], "readings": [f"{i['key']}: {i['value']}" for i in d["interpretations"]],
             "planning": d["planning"]["key"]}
            for e in r["evals"] for d in e["stages"][v]["dates"] if d["readings_differ"]]
