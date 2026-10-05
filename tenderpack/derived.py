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
unless the rule's own words name the value); when no rule shares a term the finding says NO_CONSEQUENCE."""
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
    mine = {h for x in s.ops if x.applied for h in [x.op.id]}
    units = [k for k, u in s.state.items() if u.status == "active" and (u.issued_by == stage or set(u.history) & mine)]
    out = []
    for k in units:
        u = s.state[k]
        for p in deadline_phrases(u.text, anchors):
            av = vals.get(p["anchor"])
            unit = "Working Days" if p["unit"].lower().startswith("working") else \
                ("weeks" if p["unit"].lower().startswith("week") else "days")
            res = calc.deadline({"name": "period", "value": p["count"], "unit": unit,
                                 "source": {"unit": k, "page": (u.pages or [None])[0], "words": p["words"]}},
                                {"name": p["anchor"], "date": av.isoformat() if av else None,
                                 "source": anchors[p["anchor"]].get("defined_in")}, p["direction"], cal)
            sent = next((x for x in re.split(r"(?<=[.;])\s+", u.text) if p["words"].split(" before")[0] in x), u.text)
            cond = _CONDITIONAL.search(sent)
            rows = sorted({e["row"].id for e in r["evals"] if k in e["row"].units})
            out.append({"unit": k, "pages": list(u.pages), "words": p["words"], "anchor": p["anchor"],
                        "anchor_date": av.isoformat() if av else None, "result": res,
                        "computed_from": {"method": "deadline", "inputs": res.get("inputs"),
                                          "counting": (res.get("counting") or {}).get("id"),
                                          "result": res.get("value"), "fingerprint": res.get("fingerprint")},
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

def summary(r: dict, stage: str) -> dict:
    rows = pending_reading_rows(r, stage)
    return {"stage": stage, "pending_reading_rows": rows, "pending_reading_activities": pending_reading_activities(r, rows),
            "computed_deadlines": computed_deadlines(r, stage), "working_days_left": working_days_left(r, stage),
            "switched": switched(r, stage), "consequences": consequence_candidates(r, stage)}


def _deadline_line(d: dict) -> str:
    res = d["result"]
    when = res.get("value") or ("AMBIGUOUS: " + "; ".join(f"{x['value']} ({x['key']})" for x in res.get("readings") or [])
                                if res.get("status") == "ambiguous" else f"not computed: {res.get('reason')}")
    return (f"- `{d['unit']}` p{','.join(map(str, d['pages']))}: “{d['words']}” -> **{when}** (computed: calc deadline, "
            f"anchor {d['anchor']} = {d['anchor_date']}, rule {(res.get('counting') or {}).get('id') or 'none'}, "
            f"fingerprint {str(res.get('fingerprint') or '')[:12]}; PROPOSED, not validated)"
            + (f"; CONDITIONAL: “{_short(d['conditional'], 160)}”" if d.get("conditional") else "")
            + ("; ESCALATED: the counting rules do not settle it" if res.get("escalate") else ""))


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
    return L + [""]


def review_lines(sm: dict | None) -> list[str]:
    if not sm:
        return []
    L = ["## Derived effects (session 12: pending readings, computed deadlines, conditions, consequences)", ""]
    L += a5_lines(sm)
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
