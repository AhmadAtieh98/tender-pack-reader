"""What an addendum implies beyond the units it changes (session 12, W3b; the owner's part 2; blind-05 follow-ups 6-9).

Deterministic and read-only: every function here reads the evaluated stages (stage2.run's `r`, or the Register's own
stages) and returns findings for a person; nothing decides, accepts or applies anything.

Pending readings (follow-up 6). A row or an activity proposed from an image reading that no person has approved carries
`conditional_on: {reading, until: approval, subject_sha256}` (register.ConditionalOn). It is never in force while the
reading is pending: the register gives it the status PENDING_STATUS naming the reading (A1), it stays off A3 and A5, and
the candidate A3/A5 and the review packet list it apart (pending_reading_rows / pending_reading_activities). Once a person
approves the reading (a re-ingest gives its units `reading.status: approved`) it is an ordinary row; a reading whose
review subject differs from the one pinned is a problem (re-read).

Computed deadlines (follow-up 7). computed_deadlines(r, stage) finds every "N <unit> before/after <anchor>" phrase in the
addendum's provisions and the units its ops change, and counts it with calc.deadline (one reading under the registry's
counting rules, else ambiguous and escalated): the inputs, the rule, the result and the fingerprint (`computed_from`).
A deadline of a conditional obligation (the obligation applies only where, if, or to a Bidder whose ...) is conditional.
Session 12 (blind-06 follow-up 5): each deadline also carries the register `date_rule` that plans it (dates.KINDS:
`relative` with its anchor, count, unit and direction; there is no kind "deadline", which is a purpose), and forward
periods ("within N Working Days of receipt ...", "within N Working Days of the date of this Addendum": the anchor
'<stage>-issue') are found too (period_phrases): computed where the counting registry has a rule, otherwise with an
explicit "not computed: no rule ..." note (the readings listed; an event anchor named), never a silent gap. One function
(compute_deadline) gives the fingerprint computed_deadlines records, the one the validator recomputes an activity's
claim with (match_computed_from) and the one the programme gives a relative rule's milestone (rule_computed_from).
working_days_left(r, stage) states the Working Days from the addendum's issue date to the PDD.

Conditions switched on and definitions changed (follow-up 8). switched(r, stage): a clause that applies only "Where /
If / In the event that / Unless / Should <condition>," whose condition words an op of the stage adds to (or removes from)
an obligation ("shall", "must", "is required") of a related unit (same document and section) may now always (or never)
apply; a defined term ("<Term> means ...") whose definition an op changes reaches every row whose units use the term.
The register flags those rows "condition changed by <op>: re-read" / "definition of '<term>' changed by <op>: re-read";
stage2.answers_to_review counts the conditional unit as changed (switched_units), so an earlier answer that relied on
it is re-read through the superseded-answer list. The conditional unit's status never changes.

Derived consequences (follow-up 9). consequence_candidates(r, stage): a band an addendum's words set ("not less than X
and not more than Y", "between X and Y") with the EXISTING bid-out rules (rows whose consequence is a rejection,
disqualification, non-responsiveness or exclusion) that share a defined term with it, and the rows of the forms it
names (read with). The downstream phase may propose a row whose consequence quotes such a rule (PROPOSED; human-owned
unless the rule's own words name the value); when no rule shares a term the finding says NO_CONSEQUENCE.

Session 14 (W3; the owner's part 2). Conditional impacts: conditional_impacts(r, stage) lists, in amend.conditional_impacts'
one shape ({id, stage, provision, conditional_on {kind, ref, state, why}, units, investigate, accepted: False}), every op
that could not be applied, every unresolved disposition or unaccounted provision and every pending image reading of the
stage: each is an investigation CONDITIONAL on that ref (the downstream phase maps its units to rows, activities and
prices), never an accepted fact. Computed amounts: computed_amounts(r, stage) lists each adjust_value op with the value the
engine computed (calc relative_change), its operands and their quoted sources, and its steps: a PROPOSAL with its
derivation, never typed."""
from __future__ import annotations

import re
from datetime import date

PENDING = "PENDING READING"
NO_CONSEQUENCE = "no bid-out consequence stated"
SWITCH_PREFIXES = ("condition changed by ", "definition of '")


def pending_status(reading: str) -> str:
    return f"{PENDING} (conditional on reading {reading} until approval; not in force)"


def label(reading: str) -> str:
    return f"conditional on reading {reading} until approval"


def _short(t, n: int = 200) -> str:
    t = " ".join(str(t or "").split())
    return t if len(t) <= n else t[: n - 1] + "…"


def _stage(r_or_stages, name: str):
    stages = r_or_stages["stages"] if isinstance(r_or_stages, dict) else r_or_stages
    return next(s for s in stages if s.stage == name)


def _prev(stages, name: str):
    order = [s.stage for s in stages]
    i = order.index(name)
    return stages[i - 1] if i else None


# ---------------------------------------------------------------------------------------------- pending readings

def pending_readings(r: dict, stage: str) -> dict[str, dict]:
    """{region: {subject_sha256, doc, pages, units: [unit ids]}} for the image readings still pending a person's approval
    whose units are in force at `stage` and issued by it (the addendum's own images) or changed there."""
    s = _stage(r, stage)
    out: dict[str, dict] = {}
    for u in r["units"]:
        rd = u.get("reading") or {}
        if u.get("origin") != "image_reading" or rd.get("status") != "pending":
            continue
        st = s.state.get(u["unit_id"])
        if st is None or st.status != "active" or (st.issued_by != stage and not any(
                h for h in st.history if any(x.op.id == h for x in s.ops))):
            continue
        e = out.setdefault(rd["region"], {"region": rd["region"], "subject_sha256": rd.get("subject_sha256"),
                                          "doc": u["doc"], "pages": [], "units": []})
        e["units"].append(u["unit_id"])
        e["pages"] = sorted(set(e["pages"]) | set(u.get("pages") or []))
    return out


def reading_units(r: dict, region: str) -> list[dict]:
    """The reading's units as a person checks them: Arabic (or English) as printed, the translation apart, pages, the
    crops and bands (or grid cells) of the build's review packet, numerals and uncertainties."""
    out = []
    for u in r["units"]:
        if (u.get("reading") or {}).get("region") != region:
            continue
        crops = [a.get("crop") for a in u.get("anchors") or [] if a.get("crop")]
        crops += [c for a in u.get("anchors") or [] for c in (a.get("cell_crops") or {}).values() if c]
        d = {"unit": u["unit_id"], "kind": u.get("kind"), "label": u.get("label"), "role": u.get("role"),
             "lang": u.get("lang"), "pages": list(u.get("pages") or []), "text": u.get("text") or "",
             "translation": u.get("translation"), "crops": crops,
             "bands": [a.get("band") for a in u.get("anchors") or [] if a.get("band")]
             + [a.get("grid_row") for a in u.get("anchors") or [] if a.get("grid_row")]}
        for k in ("cells", "numeric", "numerals", "uncertain", "context", "table"):
            if u.get(k):
                d[k] = u[k]
        out.append(d)
    return out


def pending_reading_rows(r: dict, stage: str) -> list[dict]:
    """The rows held out of force at `stage` because they rest on a pending reading (register.ConditionalOn)."""
    reg = r["register"]
    out = []
    for e in r["evals"]:
        row, ev = e["row"], e["stages"].get(stage) or {}
        co = getattr(row, "conditional_on", None)
        if co is None or not str(ev.get("status", "")).startswith(PENDING):
            continue
        it = reg.interp_at(row, stage)
        out.append({"row": row.id, "reading": co.reading, "label": label(co.reading), "status": ev["status"],
                    "requirement": row.requirement, "units": list(row.units), "quote": it.quote if it else "",
                    "parameters": dict(it.parameters) if it else {}, "evidence": list(row.evidence),
                    "problems": list(ev.get("problems") or [])})
    return out


def pending_reading_activities(r: dict, rows: list[dict]) -> list[dict]:
    held = {x["row"]: x["reading"] for x in rows}
    out = []
    for ev, ts in (r.get("templates") or {}).items():
        if str(ev).startswith("_"):
            continue
        for t in ts or []:
            co = t.get("conditional_on") or {}
            need = sorted(x["row"] for x in rows if ev in x["evidence"])
            if co.get("reading") or need:
                out.append({"activity": t["id"], "evidence_item": ev, "reading": co.get("reading") or held[need[0]],
                            "rows": need, "name": t.get("name"), "label": label(co.get("reading") or held[need[0]])})
    return out


# ---------------------------------------------------------------------------------------------- computed deadlines

_NUMW = (r"(?:(?:[a-z]+-)?[a-z]+\s*)?\(\s*(\d+)\s*\)|(\d+)")      # 'twenty-eight (28)', 'three (3)', '30'
_DEADLINE = re.compile(r"(?P<words>(?:" + _NUMW + r")\s+(?P<unit>Working Days?|calendar days?|days?|weeks?)\s+"
                       r"(?P<dir>before|after|prior to|following)\s+(?:the\s+)?(?P<anchor>[A-Z][\w-]*(?:\s+[A-Z][\w-]*){0,4}))")
_CONDITIONAL = re.compile(r"\b(?:Where|If|In the event that|Unless|Should)\b|\bwhose (?:Proposal|bid)\b|\bonly (?:if|where)\b|"
                          r"\bprovides? for any\b|\bexceeding\b", re.I)


# session 12 (blind-06 follow-up 5): a forward period "within N <unit> of <X>" and a count from the addendum's own date
_PERIOD = re.compile(r"(?P<words>(?P<within>within\s+)?(?:" + _NUMW + r")\s+(?P<unit>Working Days?|calendar days?|days?|"
                     r"weeks?)\s+(?P<dir>of|after|from|following)\s+(?P<what>[^.;,()]{3,80}?))"
                     r"(?=[.;,]|\s+(?:and|or|but|which|unless|for|to)\b|$)")
_THIS_ADDENDUM = re.compile(r"^(?:the\s+)?(?:date\s+of\s+(?:issue\s+of\s+)?|issue\s+(?:date\s+)?of\s+)?this\s+Addendum\b",
                            re.I)


def period_phrases(text: str, anchors: dict[str, dict]) -> list[dict]:
    """Session 12 (blind-06 follow-up 5): every forward period 'within N <unit> of <X>' and every count 'N <unit>
    after/from the date of this Addendum'. Each: {words, count, unit, direction 'after', what (the words naming X),
    anchor (a register anchor's key, or None), issue (X is the addendum's own date)}. A count 'N <unit> after <Anchor>'
    of a register anchor is deadline_phrases' (not repeated here)."""
    names = {a.get("name"): k for k, a in anchors.items()} | {k: k for k in anchors}
    out = []
    for m in _PERIOD.finditer(" ".join(str(text or "").split())):
        n = m.group(3) or m.group(4)                      # _NUMW's two groups (after `words` and `within`)
        if n is None:
            continue
        what = m.group("what").strip()
        bare = re.sub(r"^the\s+", "", what, flags=re.I)
        issue = bool(_THIS_ADDENDUM.match(what))
        anchor = next((names[x] for x in sorted(names, key=len, reverse=True) if x and bare.startswith(x)), None)
        if not m.group("within") and not issue:
            continue                                      # 'N days of X' without 'within' is no period of time
        if anchor is not None and not m.group("within") and m.group("dir") in ("after", "following"):
            continue                                      # deadline_phrases has it
        out.append({"words": m.group("words").strip(), "count": int(n), "unit": m.group("unit"), "direction": "after",
                    "what": what, "anchor": anchor, "issue": issue})
    return out


def _unit_words(unit: str) -> str:
    u = str(unit or "").lower()
    return "Working Days" if u.startswith("working") else ("weeks" if u.startswith("week") else "days")


def compute_deadline(count, unit: str, words: str, anchor: str, anchor_date, anchor_source, direction: str, cal,
                     source_unit: str | None = None, page=None) -> dict:
    """calc.deadline for one period, with the inputs in one shape (session 12, blind-06 follow-up 5): what
    computed_deadlines records in `computed_from`, what the validator recomputes an activity's claim with, and what
    rule_computed_from gives a register date rule (the programme's milestone), so the three fingerprints agree."""
    from . import calc
    return calc.deadline({"name": "period", "value": count, "unit": _unit_words(unit),
                          "source": {"unit": source_unit or "", "page": page, "words": words}},
                         {"name": anchor, "date": anchor_date.isoformat() if hasattr(anchor_date, "isoformat")
                          else anchor_date, "source": anchor_source}, direction, cal)


def _computed_from(res: dict) -> dict:
    return {"method": "deadline", "inputs": res.get("inputs"), "counting": (res.get("counting") or {}).get("id"),
            "result": res.get("value"), "fingerprint": res.get("fingerprint")}


def _phrase_words(words: str, anchors: dict | None) -> str:
    """The period phrase inside a rule's or a claim's words ('not later than eight (8) Working Days before the Proposal
    Due Date' -> 'eight (8) Working Days before the Proposal Due Date'), as computed_deadlines extracts it."""
    hits = deadline_phrases(words, anchors or {}) + period_phrases(words, anchors or {})
    return hits[0]["words"] if len(hits) == 1 else " ".join(str(words or "").split())


def rule_computed_from(rule, anchor_value, anchor_source, cal, anchors: dict | None = None) -> dict | None:
    """`computed_from` of a register date rule of kind `relative` (a row's DateRule or its dict), computed by
    compute_deadline from the rule's anchor, count, unit, direction and the period phrase in its words: the fingerprint
    the programme gives the rule's milestone, equal to the one computed_deadlines records for the same words. None for
    any other kind or an anchor without a date."""
    g = (lambda k: rule.get(k)) if isinstance(rule, dict) else (lambda k: getattr(rule, k, None))
    if g("kind") != "relative" or anchor_value is None:
        return None
    anchors = anchors if anchors is not None else {g("anchor"): {"name": g("anchor")}}
    res = compute_deadline(g("offset"), g("unit"), _phrase_words(g("text"), anchors), g("anchor"), anchor_value,
                           anchor_source, g("direction"), cal, g("source_unit"))
    return _computed_from(res) if res.get("fingerprint") else None


def match_computed_from(cf: dict, deadlines: list[dict], cal, anchors: dict | None = None) -> dict | None:
    """The computed deadline an activity's `computed_from` claims (session 12, blind-06 follow-up 5): by its
    fingerprint, else by recomputing the fingerprint from the claimed inputs with compute_deadline (a claim that gives
    the method and the inputs only, as blind-06's did, is matched); None when neither matches."""
    fp = (cf or {}).get("fingerprint")
    known = next((d for d in deadlines if fp and d["computed_from"]["fingerprint"] == fp), None)
    i = (cf or {}).get("inputs") or {}
    if known is None and i:
        off, an = i.get("offset") or {}, i.get("anchor") or {}
        try:
            res = compute_deadline(off.get("count"), off.get("unit"), _phrase_words(off.get("words"), anchors),
                                   an.get("name"), an.get("date"), an.get("source"), i.get("direction"), cal)
        except Exception:                                    # noqa: BLE001 (a malformed claim matches nothing)
            return None
        fp2 = res.get("fingerprint")
        known = next((d for d in deadlines if fp2 and d["computed_from"]["fingerprint"] == fp2), None)
    return known


def _not_computed_note(res: dict, p: dict, anchor_date, registry: dict) -> str | None:
    """'not computed: ...' for a period the counting registry does not settle (no rule for its unit and direction, or
    an anchor that is an event with no date): never a silent gap (session 12, blind-06 follow-up 5)."""
    if res.get("status") == "resolved":
        return None
    unit = "working_day" if _unit_words(p["unit"]) == "Working Days" else "day"
    why = []
    if not any(c.get("unit") == unit and c.get("direction") == p["direction"] for c in (registry.get("counting") or {}).values()):
        why.append(f"no rule in the counting registry (config/formulas.yaml `counting`) for "
                   f"{'Working Days' if unit == 'working_day' else 'days'} counted {p['direction']} a date (VOL-I 2.4 "
                   "covers Working Days counted backwards)" + (": every reading is listed and a person decides"
                                                               if res.get("readings") else ""))
    if anchor_date is None:
        why.append(f"its anchor '{p.get('what') or p['anchor']}' is an event, not a date the register holds")
    if not why:
        why.append(str(res.get("reason") or res.get("status")))
    return "not computed: " + "; ".join(why)


def _date_rule(k: str, p: dict, anchor: str | None, note: str | None) -> dict:
    """The register date rule for the phrase (dates.KINDS): `relative` with its anchor, count, unit and direction when
    the anchor is one the register holds; `unresolved` with the words and the note otherwise."""
    if anchor is not None and p["count"] >= 1:
        u = _unit_words(p["unit"])
        return {"kind": "relative", "purpose": "deadline", "anchor": anchor, "offset": p["count"],
                "unit": {"Working Days": "working_day", "weeks": "week"}.get(u, "calendar_day"),
                "direction": p["direction"], "source_unit": k, "text": p["words"]}
    return {"kind": "unresolved", "purpose": "deadline", "source_unit": k, "text": p["words"],
            "note": note or "not computed"}


def deadline_phrases(text: str, anchors: dict[str, dict]) -> list[dict]:
    """Every 'N <unit> before/after <Anchor Name>' phrase whose anchor is a register anchor (by its name or key)."""
    names = {a.get("name"): k for k, a in anchors.items()} | {k: k for k in anchors}
    out = []
    for m in _DEADLINE.finditer(" ".join(str(text or "").split())):
        anchor = next((names[n] for n in sorted(names, key=len, reverse=True)
                       if n and m.group("anchor").startswith(n)), None)
        n = m.group(2) or m.group(3)
        if anchor is None or n is None:
            continue
        words = m.group("words")
        name = next(a.get("name") for k, a in anchors.items() if k == anchor)
        words = words[: words.index(m.group("anchor"))] + name if name and m.group("anchor").startswith(name) else words
        out.append({"words": words.strip(), "count": int(n), "unit": m.group("unit"), "anchor": anchor,
                    "direction": "before" if m.group("dir") in ("before", "prior to") else "after"})
    return out


def computed_deadlines(r: dict, stage: str) -> list[dict]:
    """See the module docstring. Each: {unit, pages, words, anchor, anchor_date, result (calc.deadline), computed_from
    {method, inputs, counting, result, fingerprint}, conditional (the words that make the obligation conditional, or
    None), rows (citing the unit at the stage)}."""
    from . import calc
    from .register import anchor_values
    reg = r["register"]
    s = _stage(r, stage)
    if not s.issued:
        return []
    anchors = reg.rf.anchors
    vals = anchor_values(s.state, anchors, reg.issued)
    cal = reg.cal_by_stage[stage]
    registry = calc.load_registry()
    mine = {h for x in s.ops if x.applied for h in [x.op.id]}
    units = [k for k, u in s.state.items() if u.status == "active" and (u.issued_by == stage or set(u.history) & mine)]
    out = []
    for k in units:
        u = s.state[k]
        found_ = [(p, p["anchor"], vals.get(p["anchor"]), anchors[p["anchor"]].get("defined_in"))
                  for p in deadline_phrases(u.text, anchors)]
        for p in period_phrases(u.text, anchors):          # session 12 (blind-06 follow-up 5): forward periods
            if p["issue"]:
                found_.append((p, f"{stage}-issue", date.fromisoformat(s.issued), getattr(s, "issued_from", None)))
            elif p["anchor"] is not None:
                found_.append((p, p["anchor"], vals.get(p["anchor"]), anchors[p["anchor"]].get("defined_in")))
            else:
                found_.append((p, None, None, None))         # an event ('receipt of a complete application')
        for p, anchor, av, src in found_:
            res = compute_deadline(p["count"], p["unit"], p["words"], anchor or p.get("what"), av, src, p["direction"],
                                   cal, k, (u.pages or [None])[0])
            head = p["words"].split(" before")[0].split(" of ")[0]
            sent = next((x for x in re.split(r"(?<=[.;])\s+", u.text) if head in " ".join(x.split())), u.text)
            cond = _CONDITIONAL.search(sent)
            rows = sorted({e["row"].id for e in r["evals"] if k in e["row"].units})
            note = _not_computed_note(res, p, av, registry)
            out.append({"unit": k, "pages": list(u.pages), "words": p["words"], "anchor": anchor or p.get("what"),
                        "anchor_date": av.isoformat() if av else None, "result": res,
                        "computed_from": _computed_from(res),
                        "date_rule": _date_rule(k, p, anchor, note), **({"note": note} if note else {}),
                        "conditional": _short(sent, 240) if cond else None, "rows": rows})
    # an addendum provision that inserts or replaces the words in a volume unit computes the same date twice: the
    # volume unit's entry is kept (the provision's stays when no volume unit carries it)
    vol = {(d["words"], d["result"].get("value")) for d in out if not s.state[d["unit"]].doc.startswith("ADD-")}
    return [d for d in out if not (s.state[d["unit"]].doc == stage and (d["words"], d["result"].get("value")) in vol)]


def date_derivation(computed: list[dict], d: dict) -> str:
    """' = computed: ...' for a register date (register.evaluate's `dates` entry) whose rule words are a deadline the
    program computed at that stage (same unit, the words within the phrase): the calc result, its counting rule and
    fingerprint; a different value is shown as a disagreement for a person. '' otherwise."""
    words = " ".join(str(d.get("text") or "").split()).lower()
    for c in computed:
        if c["unit"] != d.get("source_unit") or not words or not (c["words"].lower() in words or words in c["words"].lower()):
            continue
        res, val = c["result"], (d.get("planning") or {}).get("value")
        if res.get("status") != "resolved":
            return f" (calc deadline: {res.get('status')}, {res.get('reason')})"
        same = res.get("value") == val
        return (f" {'=' if same else '≠'} computed: calc deadline {res['value']} ({c['words']}; {c['anchor']} "
                f"{c['anchor_date']}; rule {res['counting']['id']}, {res['counting']['source']['unit']}; fingerprint "
                f"{res['fingerprint'][:12]})" + ("" if same else ": the two disagree, a person checks"))
    return ""


def working_days_left(r: dict, stage: str) -> dict:
    """The Working Days from the stage's issue date (not counted) to the PDD (counted), on the stage's calendar."""
    from .register import anchor_values
    reg = r["register"]
    s = _stage(r, stage)
    pdd = anchor_values(s.state, reg.rf.anchors, reg.issued).get("PDD")
    if not s.issued or pdd is None:
        return {"issued": s.issued, "pdd": pdd.isoformat() if pdd else None, "working_days": None, "calendar": "",
                "convention": "not computed: the issue date or the PDD is not known"}
    cal = reg.cal_by_stage[stage]
    iss = date.fromisoformat(s.issued)
    return {"issued": s.issued, "pdd": pdd.isoformat(), "working_days": cal.working_days_between(iss, pdd),
            "calendar": f"Working Days per VOL-I 2.4 (weekend {sorted(cal.weekend)} as date.weekday numbers; holidays "
                        f"{sorted(h.isoformat() for h in cal.holidays) or 'none declared'})",
            "convention": "the issue date not counted, the PDD counted"}


def working_days_line(w: dict) -> str:
    if not w or w.get("working_days") is None:
        return f"Working Days left to the PDD: {(w or {}).get('convention', 'not computed')}"
    return (f"Working Days left from the issue date ({w['issued']}) to the PDD ({w['pdd']}): {w['working_days']} "
            f"({w['convention']}; {w['calendar']})")


# ---------------------------------------------------------------------------------------------- conditions, definitions

_COND = re.compile(r"^\s*(?P<lead>Where|If|In the event that|Unless|Should)\s+(?P<cond>[^,;:]{3,160}?),\s")
_DEF = re.compile(r"^\s*[“\"']?(?P<term>[A-Z][\w-]*(?:\s+(?:[A-Z][\w-]*|of|and)){0,5}?)[”\"']?\s+means\b")
_OBLIG = re.compile(r"\b(?:shall|must|is required|are required|mandatory)\b", re.I)
_STOP = {"where", "which", "that", "this", "these", "those", "there", "their", "with", "from", "into", "under", "upon",
         "proposed", "provided", "used", "required", "applicable", "applies", "apply", "being", "been", "have", "has",
         "project", "company", "bidder", "authority", "proposal", "shall", "will", "would", "made", "given", "such",
         "other", "than", "more", "less", "after", "before", "within", "achieved", "submitted", "stated"}


def condition_clause(text: str) -> dict | None:
    """'Where a membrane process is proposed, ...' -> {condition, terms: ['membrane']}; None when the text does not
    open with a condition."""
    m = _COND.match(text or "")
    if not m:
        return None
    terms = [w for w in re.findall(r"[A-Za-z][A-Za-z-]{3,}", m.group("cond")) if w.lower() not in _STOP]
    return {"condition": f"{m.group('lead')} {m.group('cond')}", "terms": terms} if terms else None


def defined_term(text: str) -> str | None:
    m = _DEF.match(text or "")
    return m.group("term").strip() if m else None


def _section(uid: str) -> str:
    doc, _, local = uid.partition(":")
    return f"{doc}:{re.split(r'[./]', local)[0]}"


def _sentences(text: str) -> list[str]:
    return [x for x in re.split(r"(?<=[.;])\s+", text or "") if x.strip()]


def switched_in(stages: list, stage: str) -> list[dict]:
    """See the module docstring; `stages` are the evaluated StageResults in order."""
    s = _stage(stages, stage)
    p = _prev(stages, stage)
    if p is None:
        return []
    out = []
    changed = [(x, k) for x in s.ops if x.applied for k in x.changed
               if k in s.state and k in p.state and s.state[k].status == "active"
               and (s.state[k].text or "") != (p.state[k].text or "")]
    # conditions
    for uid, u in s.state.items():
        if u.status != "active":
            continue
        c = condition_clause(u.text)
        if c is None:
            continue
        for x, k in changed:
            if k == uid or _section(k) != _section(uid):
                continue
            before, after = p.state[k].text or "", s.state[k].text or ""
            low_b, low_a = before.lower(), after.lower()
            added = [t for t in c["terms"] if t.lower() in low_a and t.lower() not in low_b]
            removed = [t for t in c["terms"] if t.lower() in low_b and t.lower() not in low_a]
            if not (added and all(t.lower() in low_a for t in c["terms"])) and not removed:
                continue
            words = next((sn for sn in _sentences(after if added else before)
                          if any(t.lower() in sn.lower() for t in (added or removed)) and _OBLIG.search(sn)), None)
            if words is None:
                continue
            way = "adds" if added else "removes"
            out.append({"kind": "condition", "unit": uid, "condition": c["condition"], "terms": c["terms"],
                        "op": x.op.id, "provision": x.op.provision, "changed_unit": k, "words": _short(words, 260),
                        "flag": (f"condition changed by {x.op.id}: re-read ({uid} applies '{c['condition']}'; "
                                 f"{x.op.id} {way} '{', '.join(added or removed)}' in an obligation of {k}: the condition "
                                 f"may now always{'' if added else ' never'} hold; a person decides)")})
    # definitions
    for x, k in changed:
        tb, ta = defined_term(p.state[k].text), defined_term(s.state[k].text)
        if ta and tb == ta:
            out.append({"kind": "definition", "unit": k, "term": ta, "op": x.op.id, "provision": x.op.provision,
                        "changed_unit": k, "words": _short(s.state[k].text, 260),
                        "flag": f"definition of '{ta}' changed by {x.op.id}: re-read ({k} as amended: "
                                f"'{_short(s.state[k].text, 120)}')"})
    seen, uniq = set(), []
    for o in out:
        key = (o["kind"], o["unit"], o["op"])
        if key not in seen:
            seen.add(key)
            uniq.append(o)
    return uniq


def switched(r: dict, stage: str) -> list[dict]:
    return switched_in(r["stages"], stage)


def row_flags(sw: list[dict], row, state: dict) -> list[str]:
    """The flags a row gets at a stage from switched_in(...) of that stage."""
    from .register import effective
    out = []
    eff = {u: effective(state, u, row.follows_replacement) for u in row.units}
    texts = " ".join(e.text for e in eff.values() if e is not None and e.status == "active")
    for x in sw:
        if x["kind"] == "condition" and (x["unit"] in row.units or any(e is not None and e.unit_id == x["unit"]
                                                                     for e in eff.values())):
            out.append(x["flag"])
        elif x["kind"] == "definition" and x["unit"] not in row.units and re.search(
                r"(?<![\w-])" + re.escape(x["term"]) + r"(?![\w-])", texts):
            out.append(x["flag"])
    return list(dict.fromkeys(out))


def switched_units(r: dict, s) -> dict:
    """{conditional unit: the OpResult that switched its condition} at stage `s` (stage2.answers_to_review counts these
    as changed, so an answer that relied on the old condition is re-read; definitions are not included: a defined term's
    unit is itself changed)."""
    ops = {x.op.id: x for x in s.ops}
    return {x["unit"]: ops[x["op"]] for x in switched(r, s.stage) if x["kind"] == "condition" and x["op"] in ops}


def is_switch_flag(f: str) -> bool:
    return str(f).startswith(SWITCH_PREFIXES)


# ---------------------------------------------------------------------------------------------- consequences

# words that state a consequence at all (a class's own word, or a consequence by reference: 'shall be treated as a late
# Proposal under Clause 6.6'); a bid-out class quoted from words with none of them is not stated by the pack
CONSEQUENCE_WORDS = (r"reject|disqualif|non-?\s?responsive|not responsive|exclu|treated as|deemed|render|returned|"
                     r"forfeit|invalid|will not be (?:accepted|considered|opened|evaluated|scored)|shall not be "
                     r"(?:accepted|considered|opened|evaluated|scored)")
_BANDS = (re.compile(r"not less than (?P<lo>.{1,60}?) and not more than (?P<hi>.{1,60}?)(?=[;,.]\s|;|$|\s+and\b)", re.I),
          re.compile(r"\bbetween (?P<lo>[^;.]{1,40}?) and (?P<hi>[^;.]{1,40}?)(?=[;,.]\s|;|$|\s+and\b)", re.I))
_TERM = re.compile(r"\b(?:[A-Z][a-z]+|Form|Volume|Schedule)(?:\s+(?:[A-Z][\w-]*|\d[\w-]*))+")
_GENERIC = {"Proposal Due Date", "Project Company", "The Bidder", "The Authority", "The Proposal", "This Addendum"}


def bands(text: str) -> list[dict]:
    from .calc import parse_quantity
    out = []
    for rx in _BANDS:
        for m in rx.finditer(" ".join(str(text or "").split())):
            lo, hi = parse_quantity(m.group("lo")), parse_quantity(m.group("hi"))
            if lo and hi:
                out.append({"words": m.group(0), "low": int(lo[0][0]) if lo[0][0] == int(lo[0][0]) else float(lo[0][0]),
                            "high": int(hi[0][0]) if hi[0][0] == int(hi[0][0]) else float(hi[0][0]),
                            "unit": lo[0][1] or hi[0][1]})
    return out


def terms(text: str) -> set[str]:
    """The capitalised multi-word terms of a text ('Availability Payment', 'Volume V', 'Form 4-F'), a leading article
    dropped and a reference cut before 'Clause', 'Section', 'Table' or 'Paragraph' ('Volume V Clause 29' -> 'Volume V')."""
    out = set()
    for m in _TERM.finditer(text or ""):
        t = re.sub(r"^(?:The|A|An|Any|This|Each|Every|Such)\s+", "", m.group(0).strip())
        t = re.split(r"\s+(?:Clause|Section|Table|Paragraph|Article)\b", t)[0].strip()
        if " " in t and t not in _GENERIC:
            out.add(t)
    return out


def bid_out_rules(r: dict, stage: str) -> list[dict]:
    """The rows in force at `stage` whose own consequence is a bid-out class, with the rule's words (the consequence
    unit's text) and the quote."""
    from .register import BID_OUT, Consequence
    reg = r["register"]
    s = _stage(r, stage)
    out = []
    for e in r["evals"]:
        ev = e["stages"].get(stage) or {}
        it = reg.interp_at(e["row"], stage)
        if not ev.get("active") or it is None or not isinstance(it.consequence, Consequence) or \
                it.consequence.cls not in BID_OUT:
            continue
        u = s.state.get(it.consequence.unit)
        out.append({"row": e["row"].id, "class": it.consequence.cls, "unit": it.consequence.unit,
                    "quote": it.consequence.quote, "page": (u.pages or [None])[0] if u else None,
                    "text": u.text if u else ""})
    return out


def bands_with_rules(units: dict[str, str], rules: list[dict], read_with: list[dict] | None = None) -> list[dict]:
    out = []
    for uid, text in units.items():
        for b in bands(text):
            mine = terms(text)
            hit = [dict(x, shared=sorted(mine & terms(x["text"]))) for x in rules if mine & terms(x["text"])]
            rw = [dict(x, shared=sorted(mine & terms(x["text"]))) for x in (read_with or []) if mine & terms(x["text"])
                  and x["row"] not in {h["row"] for h in hit}]
            out.append({"unit": uid, "band": b, "rules": [{k: v for k, v in h.items() if k != "text"} for h in hit],
                        "read_with": [{k: v for k, v in h.items() if k != "text"} for h in rw],
                        "silent": not hit, "note": NO_CONSEQUENCE if not hit else
                        "existing bid-out rule(s) share a term with the band: whether a value outside it falls under "
                        "them is for a person (HUMAN DECISION PENDING) unless the rule's own words name the value"})
    return out


def consequence_candidates(r: dict, stage: str) -> list[dict]:
    """See the module docstring: the bands the addendum's provisions and changed units state, each with the existing
    bid-out rules sharing a defined term and the form rows to read with."""
    s = _stage(r, stage)
    prev = _prev(r["stages"], stage)
    if prev is None:
        return []
    mine = {x.op.id for x in s.ops if x.applied}
    units = {k: u.text for k, u in s.state.items() if u.status == "active" and u.kind != "table_row"
             and (u.issued_by == stage or set(u.history) & mine)}
    rules = bid_out_rules(r, prev.stage)
    reg = r["register"]
    forms = []
    for e in r["evals"]:
        ev = e["stages"].get(prev.stage) or {}
        if ev.get("active") and e["row"].units and e["row"].units[0].startswith("VOL-IV:") \
                and e["row"].id not in {x["row"] for x in rules}:
            it = reg.interp_at(e["row"], prev.stage)
            forms.append({"row": e["row"].id, "unit": e["row"].units[0], "quote": it.quote if it else "",
                          "text": " ".join((prev.state[u].text if u in prev.state else "") for u in e["row"].units)})
    return bands_with_rules(units, rules, forms)


def consequence_check(row, rules: list[dict], st_text: dict[str, str], addendum_units: set[str]) -> dict:
    """For a proposed row with a bid-out consequence: {ok, derived, rule, owner, why}. The quoted words must state the
    class; a consequence quoted from a unit that is not the row's own nor the addendum's must be an EXISTING rule's
    (same unit and class). A derived consequence is the person's ('owner: person') unless the rule's own words name the
    row's figures ('deterministic')."""
    from .register import BID_OUT, Consequence
    out = {"ok": True, "derived": False, "rule": None, "owner": None, "why": ""}
    it = row.interpretations[-1] if row.interpretations else None
    c = it.consequence if it is not None else None
    if not isinstance(c, Consequence) or c.cls not in BID_OUT:
        return out
    latin = not re.search(r"[؀-ۿ]", c.quote)
    if latin and not re.search(CONSEQUENCE_WORDS, c.quote, re.I):
        return dict(out, ok=False, why=(f"the quoted words do not state a {c.cls} consequence ('{_short(c.quote, 120)}'): "
                                        f"the pack does not state it; a consequence is quoted from the rule that states it, "
                                        f"or the item is an escalation with '{NO_CONSEQUENCE}'"))
    if c.unit in row.units or c.unit in addendum_units:
        return out
    rule = next((x for x in rules if x["unit"] == c.unit and x["class"] == c.cls), None)
    if rule is None:
        return dict(out, ok=False, derived=True, why=(
            f"{c.unit} is neither one of the row's units nor the addendum's, and no existing row states a {c.cls} "
            f"consequence there: the pack does not state this consequence for it (escalate with '{NO_CONSEQUENCE}')"))
    figs = [str(v) for v in (it.parameters or {}).values() if isinstance(v, (int, float))]
    named = bool(figs) and all(re.search(r"(?<!\d)" + re.escape(f) + r"(?!\d)", st_text.get(c.unit, "")) for f in figs)
    return dict(out, derived=True, rule=rule["row"], owner="deterministic" if named else "person",
                why=(f"derived from the existing rule {rule['row']} ({c.unit}, {c.cls}): "
                     + ("its words name the value" if named else
                        "whether it covers this value is a person's judgment (HUMAN DECISION PENDING)")))


# ---------------------------------------------------------------------------------------------- summary and lines

# ---------------------------------------------------------------------------------------------- session 14 (W3)

def computed_amounts(r: dict, stage: str) -> list[dict]:
    """Each adjust_value op of the stage: the value the engine computed from the previous effective one, with its
    derivation (PROPOSED: a person accepts or rejects the op; the figure is never typed)."""
    out = []
    for x in _stage(r, stage).ops:
        c = x.details.get("computed")
        if x.op.type != "adjust_value" or not c:
            continue
        out.append({"op": x.op.id, "provision": x.op.provision, "target": x.op.target, "change": x.op.change,
                    "valid": x.valid, "applied": x.applied, "previous_value": x.details.get("previous_value"),
                    "new_value": x.details.get("new_value"), "derivation": x.details.get("derivation"),
                    "status": c.get("status"), "reason": c.get("reason"), "steps": list(c.get("steps") or []),
                    "operands": list(c.get("operands") or [])})
    return out


def conditional_impacts(r: dict, stage: str) -> list[dict]:
    """The stage's conditional investigations (amend.conditional_impacts), with every pending reading of the stage that
    the engine's list does not already name (pending_readings: units changed there as well as the addendum's own)."""
    from .amend import _impact
    s = _stage(r, stage)
    out = [dict(x) for x in (getattr(s, "impacts", None) or [])]
    seen = {x["id"] for x in out}
    for region, e in pending_readings(r, stage).items():
        if f"impact:{region}" not in seen:
            out.append(_impact(stage, e["units"][0], "reading", region, "pending_reading",
                               f"the reading {region} is pending a person's approval: its values are not in force",
                               list(e["units"])))
    return out


def impact_lines(sm: dict | None) -> list[str]:
    """The conditional investigations and computed amounts, for a person (review packet, candidate A3)."""
    if not sm:
        return []
    L = []
    imps = sm.get("conditional_impacts") or []
    if imps:
        L += ["## Conditional impact investigations (CONDITIONAL; never accepted facts)", ""]
        L += [f"- `{x['id']}` {x['investigate']}" for x in imps] + [""]
    amts = sm.get("computed_amounts") or []
    if amts:
        L += ["## Computed amounts (PROPOSED; computed by the engine from the previous effective value, never typed)", ""]
        for a in amts:
            L.append(f"- `{a['op']}` ({a['provision']}, '{a['change']}') on `{a['target']}`: "
                     + (f"{a['previous_value']} -> **{a['new_value']}** — {a['derivation']}" if a["status"] == "resolved"
                        else f"not computed: {a['reason']}")
                     + ("" if a["applied"] else " (op not applied: CONDITIONAL)"))
        L.append("")
    return L


def summary(r: dict, stage: str) -> dict:
    rows = pending_reading_rows(r, stage)
    return {"stage": stage, "pending_reading_rows": rows, "pending_reading_activities": pending_reading_activities(r, rows),
            "computed_deadlines": computed_deadlines(r, stage), "working_days_left": working_days_left(r, stage),
            "switched": switched(r, stage), "consequences": consequence_candidates(r, stage),
            # session 14 (W3): conditional investigations and computed amounts
            "conditional_impacts": conditional_impacts(r, stage), "computed_amounts": computed_amounts(r, stage)}


def _deadline_line(d: dict) -> str:
    res = d["result"]
    when = res.get("value") or ("AMBIGUOUS: " + "; ".join(f"{x['value']} ({x['key']})" for x in res.get("readings") or [])
                                if res.get("status") == "ambiguous" else d.get("note") or f"not computed: {res.get('reason')}")
    return (f"- `{d['unit']}` p{','.join(map(str, d['pages']))}: “{d['words']}” -> **{when}** (computed: calc deadline, "
            f"anchor {d['anchor']} = {d['anchor_date']}, rule {(res.get('counting') or {}).get('id') or 'none'}, "
            f"fingerprint {str(res.get('fingerprint') or '')[:12]}; PROPOSED, not validated)"
            + (f"; CONDITIONAL: “{_short(d['conditional'], 160)}”" if d.get("conditional") else "")
            + ("; ESCALATED: the counting rules do not settle it" if res.get("escalate") else "")
            + (f"; {d['note']}" if d.get("note") and res.get("status") == "ambiguous" else ""))


def a5_lines(sm: dict | None) -> list[str]:
    if not sm:
        return []
    L = ["## Computed deadlines and the Working Days left (PROPOSED; nothing typed)", "",
         "- " + working_days_line(sm.get("working_days_left") or {})]
    L += [_deadline_line(d) for d in sm.get("computed_deadlines") or []] or ["- no 'N days before/after' deadline in the "
                                                                              "addendum's provisions"]
    rows, acts = sm.get("pending_reading_rows") or [], sm.get("pending_reading_activities") or []
    if rows or acts:
        L += ["", "## Proposed from a pending reading (not in force; not planned)", ""]
        L += [f"- `{x['row']}` {x['label']}: {_short(x['requirement'], 160)}" for x in rows]
        L += [f"- activity `{x['activity']}` {x['label']} (rows {', '.join(x['rows']) or 'none'})" for x in acts]
    return L + [""]


def a3_lines(sm: dict | None) -> list[str]:
    if not sm:
        return []
    L = ["## Derived, not in force (CANDIDATE; a person decides)", "", "- " + working_days_line(sm.get("working_days_left") or {})]
    for x in sm.get("pending_reading_rows") or []:
        L.append(f"- `{x['row']}` {x['label']} — {_short(x['requirement'], 160)}; parameters "
                 + ", ".join(f"{k}: {v}" for k, v in x["parameters"].items()) + " (never shown as in force)")
    for x in sm.get("switched") or []:
        L.append(f"- {x['flag']}")
    return L + [""] + impact_lines(sm)                         # session 14 (W3)


def review_lines(sm: dict | None) -> list[str]:
    if not sm:
        return []
    L = ["## Derived effects (session 12: pending readings, computed deadlines, conditions, consequences)", ""]
    L += a5_lines(sm)
    L += impact_lines(sm)                                      # session 14 (W3)
    sw = sm.get("switched") or []
    if sw:
        L += ["## Conditions switched and definitions changed (rows flagged: re-read; nothing decided)", ""]
        L += [f"- {x['flag']}" for x in sw] + [""]
    cs = sm.get("consequences") or []
    if cs:
        L += ["## Bands and the existing bid-out rules (derived consequences are PROPOSED; HUMAN DECISION PENDING)", ""]
        for c in cs:
            L.append(f"- `{c['unit']}`: “{_short(c['band']['words'], 140)}” — "
                     + ("; ".join(f"{x['row']} ({x['class']}, {x['unit']}: “{_short(x['quote'], 100)}”)" for x in c["rules"])
                        or c["note"])
                     + (f"; read with {', '.join(x['row'] for x in c['read_with'])}" if c["read_with"] else ""))
        L.append("")
    return L
