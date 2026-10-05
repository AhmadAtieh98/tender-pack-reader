"""Change signals and references shared by every deliverable (session 12).

One predicate decides whether a row's requirement changed between two stages, so that A2's change list, A5's replan
deltas (validated and candidate), the diff and the AI review packet agree:

  requirement_delta(a, b, causes)   a, b: the row's evaluations at the earlier and the later stage (register.evaluate);
                                    causes: the ops new at the later stage on the units the row cites, each {op, type,
                                    effect, provision, answer, class} (programme.answers_by_row / causes_between).
      CHANGED     the words (effective text), the values (cells), the dates, the status, the consequence, the quoted
                  words or the parameters of the reading differ, the words or status of another unit the row cites
                  changed (a unit first issued at the later stage is new context, not a change), or the row became
                  STALE because of an op that is not a confirmation. `what` names each: text, cells, dates, status,
                  cited units, consequence, quote, parameters, reading (another field of the reading), stale.
      CONFIRMED (unchanged)
                  nothing of the above differs, and a confirming op landed on the row's units (an annotation whose
                  effect is `confirms` or `interprets`, or a clarification answer summary.classify_answer reads as
                  none/confirms), or the reading was re-made with the same words, values, parameters, dates and
                  consequence (only its note or stage differ). A parameter ADDED to the reading under confirming ops only
                  is recorded with the op that it rests on, not a change (an interpretation of the same words); a value
                  that changes or disappears is always a change. A row made STALE only by confirming ops (a new answer is
                  a new dependency, register.py) is not a change either: it stays STALE in A1 until a person re-reads it,
                  and the detail says so. The detail cites the confirming op and its provision.
      NOT SETTLED nothing differs, but an unresolved provision of the stage cites the row (or it is STALE there and its
                  reading was not re-made): never called CONFIRMED (partial.unresolved_rows gives the reasons). Session
                  12 (F5; audit A2-1, A5 N1): nor is a row that would be CONFIRMED while an issue linked to it is a
                  person's decision not yet recorded (human_owned.pending_reasons: the evaluation's `pending`, put by
                  attach_pending, or a confirming op whose own issue or note names such an issue or carries the HUMAN
                  DECISION PENDING marker: the cause's `pending`): "open: I-CONCESSION, human decision pending".
      neither     no difference and no confirming cause: the row is not listed.
  A confirming label never hides words of change: an answer the deterministic reader classifies as `changes` (words
  such as 'is amended', 'instead of', or a figure the targets do not print) is not a confirmation, whatever its label.
  Labels are proposals: the line says which op and which label it rests on, for a person to check.

Session 12 (F2; audit A2-2, A2-3): CONFIRMED (unchanged) only when NOTHING the row depends on changed at the stage. Besides
its own words, values, dates, status, consequence and the units it cites, a row depends on (a) the units the curated
relationships say it depends on (attach_dependencies: entries of a content kind, DEPENDENCY_KINDS, confirmed or
proposed, followed through calculations: Table 2-4 for the effluent rows), and the unit its consequence is quoted from;
(b) the dates that flow into it: an anchor date one of its units prints ('Proposal Due Date: 12 November 2026'). When
any of them changed, the row is CHANGED with the cause named ('dependency': 'VOL-II T2-4/TN: Limit 5 -> 3 mg/l by
ADD-02/5.1 (through REL-T24-PROCESS-DESIGN ...)'; 'anchor date': 'PDD moved 2026-11-12 -> 2026-11-26 (VOL-I 6.1 as
amended by ADD-01 2.1); VOL-IV F4-A/proposal-due-date prints 2026-11-12: CONFLICT ...'), even when the op touching the
row itself is a confirmation. A printed date that conflicts with its amended anchor is never confirmed: CHANGED at the
stage the anchor moved, NOT SETTLED (with the conflict) at a later stage that changes nothing. `causes` names each cause
({kind, text}: cited unit, dependency, anchor date); for a change `detail` joins them. An annotation that adds an
obligation to the row's units is not by itself a change of the row (blind-05 false signal 2: ADD-03/Q20 on VOL-I 6.2):
it stays listed beside the confirmation for a person to check, as before.

One label (session 12, F5; audit R-f): row_label(a, b, causes, unsettled, acknowledge) gives CHANGED / CONFIRMED
(unchanged) / NOT SETTLED / None for a row between two stages, for A2's rows-moved table and A5's replan deltas alike
(REWORK in A5 is CHANGED here). `acknowledge` (stage, earlier stage) marks a row whose output names the Addenda issued
(the templates' `_addenda_checks`, Form 4-A): CHANGED at every later stage, with the rule's words (acknowledgement).

Issue references (session 12, blind-05 false signal 6): an issue id written in a note, in a row's `issues`, in an
activity's `gated_by` / `linked_issues` or in a clarification's `linked_issues` must exist among the promoted issues
(the curated register's issues and the candidate's new ones). Ids the build generates (I-AUTO-..., I-A5-..., I-OP-...,
I-PARTIAL-...) are not curated and are accepted as generated. `issue_refs` finds the ids in a text, `broken_issue_refs`
lists the ones that do not exist, `issue_ref_findings` checks the curated files (check-register, kind `issue_ref`).

Pure functions; nothing here decides, accepts or applies anything."""
from __future__ import annotations

import re

CONFIRMING_EFFECTS = ("confirms", "interprets")
CONFIRMED = "CONFIRMED (unchanged)"
# relationship kinds that say the target's content depends on the source (missing_document is a blocker, not content)
DEPENDENCY_KINDS = ("cites", "depends_on", "feeds_calculation", "limit_applies", "member_scope")
DEPENDENCY_STATUSES = ("confirmed",)    # session 12 (the coordinator, 19:10 UTC): only a relationship the documents
# state (status confirmed) makes a row depend on another unit; a `proposed` link (inferred, not confirmed by a person)
# and a `possible` link (a words trigger at most) stay in the diff's review classes and never label a row CHANGED
# (session 10's rule, test_blind03_diff_keeps_the_three_classes_apart_from_the_direct_changes; W3b had included proposed)
_READING_META = ("stage", "note", "pins")
_SUBSTANCE = ("quote", "parameters", "consequence")


def _short(t, n: int = 160) -> str:
    t = " ".join(str(t or "").split())
    return t if len(t) <= n else t[: n - 1] + "…"


# ---------------------------------------------------------------------------------------------- confirmations

def confirming(c: dict) -> bool:
    """Whether one cause (an op new at the stage on the row's units) confirms rather than changes: an annotation labelled
    `confirms` or `interprets`, or a clarification answer that summary.classify_answer reads as none/confirms; never an
    answer read as `changes` (its words of change override the label)."""
    if c.get("answer") and c.get("class") == "changes":
        return False
    eff = c.get("effect")
    if eff is None and not c.get("answer"):
        eff = c.get("class")                      # programme.answers_by_row before session 12: the effect as class
    if (c.get("type") in (None, "annotate")) and eff in CONFIRMING_EFFECTS:
        return True
    return bool(c.get("answer")) and c.get("class") in ("none", "confirms")


def cause_label(c: dict) -> str:
    """'ADD-02/Q8 (confirms; ADD-02:Q8)': the op, its label and the provision it rests on (and how the answer reads)."""
    eff = c.get("effect") or (c.get("class") if not c.get("answer") else "")
    bits = [x for x in (eff, c.get("provision")) if x]
    if c.get("answer") and c.get("class") and c.get("class") != eff:
        bits.append(f"answer reads '{c['class']}' (summary.classify_answer)")
    return f"{c.get('op')}" + (f" ({'; '.join(bits)})" if bits else "")


_NEW_DEP = re.compile(r"^new dependency (\S+)$")
_BY = re.compile(r"\(by ([^)]*)\)\s*$")


def stale_from_confirmations(reasons: list[str], conf: list[dict]) -> bool:
    """Whether every STALE reason comes from the confirming ops: a new dependency that is a confirming op's provision,
    or a dependency changed by confirming ops only. 'never pinned', a dependency gone, a quote lost: not."""
    if not reasons or not conf:
        return False
    ids = {c.get("op") for c in conf}
    provs = {c.get("provision") for c in conf} - {None}
    for x in reasons:
        m = _NEW_DEP.match(x.strip())
        if m:
            if m.group(1) not in provs:
                return False
            continue
        b = _BY.search(x)
        if not b or not {o.strip() for o in b.group(1).split(",")} <= ids:
            return False
    return True


def _dates(ev: dict) -> list:
    return [d.get("planning") for d in ev.get("dates") or []]


def requirement_delta(a: dict, b: dict, causes: list[dict] | None = None, unsettled: list[str] | None = None) -> dict:
    """See the module docstring. {changed, confirmed, unsettled, what: [...], detail} for one row between two stage
    evaluations. `unsettled` (partial.unresolved_rows for the row: an unresolved provision of the stage cites it, or it is
    STALE there): a row the stage does not settle is never called CONFIRMED; when nothing else changed it is `unsettled`
    with the reasons, so no reader takes it as final."""
    from .schedule import status_changed
    causes = list(causes or [])
    conf = [c for c in causes if confirming(c)]
    other = [c for c in causes if not confirming(c)]
    what: list[str] = []
    for k, x, y in (("text", a.get("text"), b.get("text")), ("cells", a.get("cells"), b.get("cells")),
                    ("dates", _dates(a), _dates(b))):
        if x != y:
            what.append(k)
    if status_changed(a, b):
        what.append("status")
    # the other units the row cites: words or status that change are a change (an amended table row, a deleted item);
    # a unit issued only at the later stage is new context, which the re-made reading reads (or the row is STALE)
    ua = {d.get("unit"): (d.get("text"), d.get("status")) for d in (a.get("units_detail") or [])[1:]}
    ub = {d.get("unit"): (d.get("text"), d.get("status")) for d in (b.get("units_detail") or [])[1:]}
    named: list[dict] = []
    cited = [u for u, v in ub.items() if u in ua and ua[u][1] not in ("absent", "not_issued") and ua[u] != v]
    if cited:
        what.append("cited units")
        da = {d.get("unit"): d for d in (a.get("units_detail") or [])[1:]}
        db = {d.get("unit"): d for d in (b.get("units_detail") or [])[1:]}
        for u in _no_parents(cited):
            x, y = da[u], db[u]
            named.append({"kind": "cited unit", "text": f"cited unit {_ref(u, y)}: {_how(x, y)}"
                          + _by([o for o in y.get("ops") or [] if o not in (x.get("ops") or [])])})
    dep = dependency_changes(a, b)                       # session 12 (F2): what it depends on, and the dates into it
    for k in ("dependency", "anchor date"):
        if any(x["kind"] == k for x in dep):
            what.append(k)
    named += dep
    ia, ib = a.get("interpretation") or {}, b.get("interpretation") or {}
    recorded: list[str] = []
    reread = (a.get("interpretation") or None) != (b.get("interpretation") or None)
    if reread:
        if ia.get("consequence") != ib.get("consequence"):
            what.append("consequence")
        if ia.get("quote") != ib.get("quote"):
            what.append("quote")
        pa, pb = ia.get("parameters") or {}, ib.get("parameters") or {}
        if any(k not in pb or pb[k] != v for k, v in pa.items()):
            what.append("parameters")                    # a value changed or went: always a change
        elif set(pb) - set(pa):
            added = sorted(set(pb) - set(pa))
            if conf and not other:
                recorded.append("parameter(s) recorded from the confirming op(s): "
                                + "; ".join(f"{k} = {_short(pb[k], 120)}" for k in added))
            else:
                what.append("parameters")
        rest = lambda i: {k: v for k, v in i.items() if k not in _READING_META + _SUBSTANCE}  # noqa: E731
        if rest(ia) != rest(ib):
            what.append("reading")
    if bool(a.get("stale")) != bool(b.get("stale")):
        if b.get("stale") and stale_from_confirmations(list(b["stale"]), conf) and not other:
            recorded.append("STALE until a person re-reads it (A1): " + _short("; ".join(b["stale"]), 200))
        else:
            what.append("stale")
    if what:
        return {"changed": True, "confirmed": False, "unsettled": False, "what": what, "causes": named,
                "detail": "; ".join(x["text"] for x in named)}
    conflicts = printed_conflicts(b)                     # a printed date that disagrees with its anchor: never confirmed
    if unsettled or conflicts:
        return {"changed": False, "confirmed": False, "unsettled": True, "what": [], "causes": [],
                "detail": "NOT SETTLED: " + _short("; ".join(list(unsettled or []) + conflicts), 300)}
    if not (conf or reread or recorded):
        return {"changed": False, "confirmed": False, "unsettled": False, "what": [], "causes": [], "detail": ""}
    # session 12 (F5; audit A2-1, A5 N1): a row under an issue a person has not decided is never confirmed
    pend = list(dict.fromkeys(list(b.get("pending") or []) + [p for c in conf for p in c.get("pending") or []]))
    if pend:
        return {"changed": False, "confirmed": False, "unsettled": True, "what": [], "causes": [], "pending": pend,
                "detail": "NOT SETTLED: " + _short("; ".join(pend), 300) + (
                    f" (the confirming op(s) {', '.join(cause_label(c) for c in conf)} do not settle it)" if conf else "")}
    parts = []
    if conf:
        parts.append("confirmed by " + "; ".join(cause_label(c) for c in conf))
    if reread:
        note = _short(ib.get("note"), 160)
        parts.append(f"reading re-made at {ib.get('stage')} with the same words, values, parameters, dates and "
                     "consequence" + (f" (note: '{note}')" if note else ""))
    parts += recorded
    if other:
        parts.append("other ops on its units (the re-made reading records no change from them; a person checks): "
                     + "; ".join(cause_label(c) for c in other))
    return {"changed": False, "confirmed": True, "unsettled": False, "what": [], "causes": [], "detail": "; ".join(parts)}


def acknowledgement_detail(ev: dict, stage: str, prev_stage: str) -> str:
    """'Addenda to acknowledge: ADD-02 issued since ADD-01; ADD-02:cover/para3: '<the rule's words>'' for a row whose
    output names the Addenda issued (the templates' `_addenda_checks`): the addendum's own units the row cites and the
    quoted rule."""
    it = (ev or {}).get("interpretation") or {}
    units = [u.get("unit") for u in (ev or {}).get("units_detail") or [] if str(u.get("unit") or "").startswith(f"{stage}:")]
    return (f"Addenda to acknowledge: {stage} issued since {prev_stage}" + (f"; {', '.join(units)}" if units else "")
            + (f": '{it['quote']}'" if it.get("quote") else ""))


LABELS = ("CHANGED", CONFIRMED, "NOT SETTLED")


def row_label(a: dict, b: dict, causes: list[dict] | None = None, unsettled: list[str] | None = None,
              acknowledge: tuple[str, str] | None = None) -> dict:
    """The ONE label of a row between two stages (session 12, F5; audit R-f), for A2's rows-moved table and A5's
    replan deltas: requirement_delta's result plus `label`: CHANGED, CONFIRMED (unchanged), NOT SETTLED or None (not
    listed). `acknowledge` = (stage, earlier stage) for a row whose output names the Addenda issued: CHANGED, with
    acknowledgement_detail as its cause."""
    if acknowledge:
        t = acknowledgement_detail(b, *acknowledge)
        return {"changed": True, "confirmed": False, "unsettled": False, "what": ["addenda to acknowledge"],
                "causes": [{"kind": "addenda to acknowledge", "text": t}], "detail": t, "label": "CHANGED"}
    d = requirement_delta(a, b, causes, unsettled)
    return dict(d, label="CHANGED" if d["changed"] else "NOT SETTLED" if d["unsettled"] else
                CONFIRMED if d["confirmed"] else None)


def acknowledgement_rows(templates: dict | None) -> set[str]:
    """The rows the templates' `_addenda_checks` name (a row whose output names the Addenda issued)."""
    return {k for spec in ((templates or {}).get("_addenda_checks") or {}).values() if isinstance(spec, dict)
            for k in spec.get("rows") or []}


def pending_issues(r: dict) -> dict[str, list[str]]:
    """Issue id -> why it is a person's decision not yet recorded (human_owned.pending_reasons), for every issue of the
    run (the curated register's and a candidate's promoted ones), with the clarification register's pending links."""
    from . import human_owned as HO
    links = HO.pending_links(r.get("clarifications"))
    out = {}
    for iid, it in (r.get("curated_issues") or {}).items():
        why = HO.pending_reasons(iid, it, r.get("decisions"), links.get(iid))
        if why:
            out[iid] = why
    return out


def pending_note(iid: str) -> str:
    return f"open: {iid}, human decision pending"


def attach_pending(r: dict) -> None:
    """Session 12 (F5; audit A2-1, A5 N1): put on every row evaluation at every stage a `pending` list ("open: <issue>,
    human decision pending") for each issue linked to the row (its `issues`) that is a person's decision not yet
    recorded (pending_issues). requirement_delta never calls such a row CONFIRMED. Pure data."""
    pend = pending_issues(r)
    r["pending_issues"] = pend
    for e in r.get("evals") or []:
        mine = [pending_note(i) for i in dict.fromkeys(e["row"].issues) if i in pend]
        for ev in e["stages"].values():
            if isinstance(ev, dict):
                ev["pending"] = list(mine)


def op_pending(op, pend: dict) -> list[str]:
    """For a confirming op's cause: the pending issues its own issue or note names, and the op itself when its words
    carry the HUMAN DECISION PENDING marker."""
    from .human_owned import HUMAN_DECISION_PENDING
    text = f"{getattr(op, 'issue', '') or ''} {getattr(op, 'note', '') or ''}"
    out = [pending_note(i) for i in issue_refs(text) if i in (pend or {})]
    if HUMAN_DECISION_PENDING in text:
        out.append(pending_note(getattr(op, "id", "?")))
    return out


# ---------------------------------------------------------------------------------------------- dependencies (F2)

def _ref(uid: str, d: dict | None = None) -> str:
    ref = (d or {}).get("ref") or (lambda doc, _, loc: f"{doc} {loc}")(*str(uid).partition(":"))
    return re.sub(r" p[\d,]+$", "", ref)


def _no_parents(uids: list[str]) -> list[str]:
    """The units without a changed member listed beside them (a table and its changed row: the row names the change)."""
    return [u for u in uids if not any(v != u and v.startswith(u + "/") for v in uids)]


def _by(ops: list[str]) -> str:
    return f" by {', '.join(ops)}" if ops else ""


def _pairs(text) -> dict | None:
    """A table row's text as its cells ('Parameter: TN | Unit: mg/l | Limit: 5' -> {Parameter: TN, ...}), else None."""
    segs = [x.split(": ", 1) for x in str(text or "").split(" | ")]
    return {k.strip(): v.strip() for k, v in segs} if len(segs) > 1 and all(len(x) == 2 for x in segs) else None


def _how(x: dict, y: dict) -> str:
    """What changed in one unit between two snapshots: its changed cells ('Limit 5 -> 3 mg/l'), its status, or its words."""
    cx, cy = x.get("cells") or _pairs(x.get("text")), y.get("cells") or _pairs(y.get("text"))
    if isinstance(cx, dict) and isinstance(cy, dict) and cx != cy:
        unit = next((v for k, v in cy.items() if str(k).lower() == "unit" and cx.get(k) == v), "")
        return "; ".join(f"{k} {cx.get(k, '(none)')} -> {cy.get(k, '(none)')}" for k in list(cy) + [k for k in cx if k not in cy]
                         if cx.get(k) != cy.get(k)) + (f" {unit}" if unit else "")
    if x.get("status") != y.get("status"):
        return f"{x.get('status')} -> {y.get('status')}"
    # session 12 (F5; audit A2-8): the words replaced, as the A2 change table prints them (two cuts of a long text can
    # read the same: 'SAR 5,000,000' -> 'SAR 2,500,000' was hidden behind the clause's first words)
    return word_diff(x.get("text"), y.get("text")) or f"'{_short(x.get('text'), 70)}' -> '{_short(y.get('text'), 70)}'"


def word_diff(old: str, new: str) -> str:
    """The words that differ between two texts: 'a' -> 'b'; + 'added'; - 'removed' (stage2's A2 change table too)."""
    import difflib
    a, b = (old or "").split(), (new or "").split()
    groups: list[list[int]] = []                  # [i1, i2, j1, j2]: changes up to two equal words apart are one phrase
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        if groups and i1 - groups[-1][1] <= 2 and j1 - groups[-1][3] <= 2:
            groups[-1][1], groups[-1][3] = i2, j2
        else:
            groups.append([i1, i2, j1, j2])
    out = []
    for i1, i2, j1, j2 in groups:
        o, n = " ".join(a[i1:i2]), " ".join(b[j1:j2])
        out.append(f"'{o}' -> '{n}'" if o and n else f"+ '{n}'" if n else f"- '{o}'")
    return "; ".join(out)


def dependency_changes(a: dict, b: dict) -> list[dict]:
    """[{kind, text}] for what a row depends on (its evaluation's `depends`, attach_dependencies) that changed between two
    stage evaluations: a unit reached through a relationship or its consequence unit ('dependency'), and an anchor date
    one of its units prints ('anchor date', with the conflict when the printed date is no longer the anchor's). A unit
    first present at the later stage is new context, not a change (as for the units the row cites)."""
    da, db = a.get("depends") or {}, b.get("depends") or {}
    ua, ub = da.get("units") or {}, db.get("units") or {}
    key = lambda x: (x.get("text"), x.get("cells"), x.get("status"))  # noqa: E731
    changed = [u for u, y in ub.items() if u in ua and ua[u].get("status") not in ("absent", "not_issued")
               and key(ua[u]) != key(y)]
    changed += [u for u, x in ua.items() if u not in ub and x.get("status") == "active"]
    out = []
    for u in _no_parents(changed):
        x, y = ua[u], ub.get(u) or {"status": "absent", "text": "", "cells": None, "ops": []}
        out.append({"kind": "dependency", "unit": u,
                    "text": f"{_ref(u, y if u in ub else x)}: {_how(x, y)}"
                            + _by([o for o in y.get("ops") or [] if o not in (x.get("ops") or [])])
                            + f" (depends on it: {'; '.join((y if u in ub else x).get('via') or [])})"})
    aa, ab = da.get("anchors") or {}, db.get("anchors") or {}
    for n, y in ab.items():
        x = aa.get(n) or {}
        if x.get("value") and y.get("value") and x["value"] != y["value"]:
            t = f"{n} moved {x['value']} -> {y['value']} ({y.get('source') or n})"
            conf = _conflicts(n, y)
            out.append({"kind": "anchor date", "anchor": n,
                        "text": t + (f"; {'; '.join(conf)}: CONFLICT with the amended {n}, not corrected (a person "
                                     "decides)" if conf else "")})
    return out


def _conflicts(name: str, y: dict) -> list[str]:
    out = []
    for u, p in (y.get("printed") or {}).items():
        d = p if isinstance(p, str) else (p or {}).get("date")
        if d and y.get("value") and d != y["value"]:
            out.append(f"{_ref(u, p if isinstance(p, dict) else None)} prints {d}")
    return out


def printed_conflicts(b: dict) -> list[str]:
    """'CONFLICT: <unit> prints <date>; the PDD is <date> (<source>) ...' for each anchor date a unit of the row prints
    that is not the anchor's effective value at this stage (a reissued form printing the old due date)."""
    out = []
    for n, y in ((b.get("depends") or {}).get("anchors") or {}).items():
        c = _conflicts(n, y)
        if c:
            out.append(f"CONFLICT: {'; '.join(c)}; the {n} is {y['value']} ({y.get('source') or n}): not corrected "
                       "(a person decides)")
    return out


def relationship_sources(entries, rows: dict) -> dict[str, list[tuple[str, str]]]:
    """Row id -> [(source id, 'REL-ID (kind, status)[ < ...]')]: the units (a table or form id stands for its members)
    and the rows whose content the curated relationships say the row depends on (DEPENDENCY_KINDS, DEPENDENCY_STATUSES),
    followed back through calculations (`calc:` nodes) and source rows (their units); `words:` triggers are lexical, not
    dependencies. Cycle-safe."""
    from .relationships import ends
    into: dict[str, list[tuple[str, dict]]] = {}
    for e in entries or []:
        if isinstance(e, dict) and e.get("id") and e.get("kind") in DEPENDENCY_KINDS \
                and e.get("status") in DEPENDENCY_STATUSES:
            for t in ends(e, "to"):
                into.setdefault(t, []).extend((s, e) for s in ends(e, "from") if not s.startswith("words:"))
    out: dict[str, list[tuple[str, str]]] = {}
    for rid in rows:
        seen, stack, got = {rid}, [(rid, [])], []
        while stack:
            node, path = stack.pop()
            for s, e in into.get(node, []):
                if s in seen:
                    continue
                seen.add(s)
                p = path + [f"{e['id']} ({e['kind']}, {e['status']})"]
                if s.startswith("calc:"):
                    stack.append((s, p))
                elif s in rows:
                    got += [(u, " < ".join(p) + f" (row {s})") for u in rows[s].units]
                else:
                    got.append((s, " < ".join(p)))
        if got:
            out[rid] = got
    return out


_PRINTED_LEAD = re.compile(r"\s*(?::|,|is|shall be)?\s*(?:[A-Z][a-z]+day,?\s+)?\d{1,2}\s+[A-Z][a-z]+\s+\d{4}")


def printed_anchors(text: str, anchors: dict) -> dict[str, str]:
    """{anchor key: ISO date} for each anchor whose name the text prints followed by a date ('Proposal Due Date: 12
    November 2026'): a date that flows into the row from the anchor. A name alone ('... on the Proposal Due Date') is not."""
    from .dates import parse_date
    out = {}
    for k, a in (anchors or {}).items():
        for m in re.finditer(re.escape(str(a.get("name") or k)), text or "", re.I):
            rest = (text or "")[m.end(): m.end() + 60]
            if _PRINTED_LEAD.match(rest):
                try:
                    p = parse_date(rest)
                except ValueError:
                    p = None
                if p:
                    out[k] = p[0].isoformat()
                    break
    return out


def attach_dependencies(r: dict) -> None:
    """Session 12 (F2): put on every row evaluation at every stage (r["evals"]) a `depends` snapshot that
    requirement_delta compares: {"units": {uid: {text, cells, status, ops, via, ref}}, "anchors": {key: {name, value,
    source, ops, printed: {uid: {date, ref}}}}}. Units: the relationship sources (relationship_sources) and the unit the
    reading's consequence is quoted from, each as its effective unit (a replaced unit is followed), minus the units the
    row cites (compared already). Anchors: those a unit of the row prints a date for (printed_anchors), with the
    anchor's effective value and source at the stage (r["anchor_details"]); never the anchor's own defining unit (its
    words are the row's text). Pure data; nothing is decided."""
    from .register import effective
    reg = r.get("register")
    rows = {e["row"].id: e["row"] for e in r.get("evals") or []}
    srcs = relationship_sources(r.get("relationships"), rows)
    anchors = getattr(r.get("rowfile"), "anchors", None) or {}
    defining = {a.get("defined_in") for a in anchors.values()}
    by = {s.stage: s for s in r.get("stages") or []}
    members: dict[tuple[str, str], list[str]] = {}

    def expand(stage: str, state: dict, src: str) -> list[str]:
        if (stage, src) not in members:
            members[(stage, src)] = ([src] if src in state else []) + sorted(k for k in state if k.startswith(src + "/"))
        return members[(stage, src)]

    def snap(state: dict, uid: str, via: str) -> dict:
        u = effective(state, uid, True)
        return {"text": u.text if u is not None and u.status != "not_issued" else "",
                "cells": u.cells if u is not None else None, "status": u.status if u is not None else "absent",
                "ops": list(u.history) if u is not None else [], "via": [via],
                "ref": reg._ref(uid, state, pages=False) if reg is not None else _ref(uid)}

    for e in r.get("evals") or []:
        row, own = e["row"], set(e["row"].units)
        for st, ev in e["stages"].items():
            s = by.get(st)
            if s is None:
                continue
            state, units = s.state, {}
            for src, via in srcs.get(row.id, []):
                for uid in expand(st, state, src):
                    if uid in own:
                        continue
                    if uid in units:
                        units[uid]["via"] = list(dict.fromkeys(units[uid]["via"] + [via]))
                    else:
                        units[uid] = snap(state, uid, via)
            cons = (ev.get("interpretation") or {}).get("consequence")
            cu = cons.get("unit") if isinstance(cons, dict) else None
            if cu and cu not in own and cu not in units:
                units[cu] = snap(state, cu, "the unit its consequence is quoted from")
            anc = {}
            det = (r.get("anchor_details") or {}).get(st) or {}
            for d in ev.get("units_detail") or []:
                if d.get("unit") in defining or d.get("effective_unit") in defining:
                    continue
                for k, p in printed_anchors(d.get("text") or "", anchors).items():
                    ad = det.get(k) or {}
                    x = anc.setdefault(k, {"name": anchors[k].get("name"),
                                           "value": ad["date"].isoformat() if ad.get("date") else None,
                                           "source": ad.get("source") or "", "ops": list(ad.get("as_amended_by") or []),
                                           "printed": {}})
                    x["printed"][d["unit"]] = {"date": p, "ref": reg._ref(d.get("effective_unit") or d["unit"], state, pages=False)
                                               if reg is not None else _ref(d["unit"])}
            ev["depends"] = {"units": units, "anchors": anc}


def causes_between(r: dict, frm: str, to: str) -> dict[str, list[dict]]:
    """Row -> the ops new on its units at each stage after `frm` up to `to` (programme.answers_by_row per stage)."""
    from .programme import answers_by_row
    order = list(r["order"])
    out: dict[str, list[dict]] = {}
    if frm not in order or to not in order:
        return out
    for st in order[order.index(frm) + 1: order.index(to) + 1]:
        for rid, recs in answers_by_row(r, st).items():
            have = out.setdefault(rid, [])
            have += [x for x in recs if not any(y["op"] == x["op"] for y in have)]
    return out


def confirming_ops(r: dict) -> set[str]:
    """The ids of every annotate op labelled confirms/interprets, at every stage (for the diff's secondary units)."""
    return {x.op.id for s in r["stages"] for x in s.ops
            if x.op.type == "annotate" and (x.op.effect or "") in CONFIRMING_EFFECTS}


# ---------------------------------------------------------------------------------------------- issue references

ISSUE_REF = re.compile(r"(?<![\w./-])I-[A-Z][A-Za-z0-9]*(?:[-./][A-Za-z0-9]+)*")
GENERATED_ISSUE_PREFIXES = ("I-AUTO-", "I-A5-", "I-OP-", "I-PARTIAL-")
BROKEN = "BROKEN ISSUE REFERENCE"


def issue_refs(text) -> list[str]:
    """The issue ids written in a text, in order, once each ('I-ADD03-PRICE-BASIS'; never the 'I-6.2' of a row id)."""
    return list(dict.fromkeys(m.rstrip(".") for m in ISSUE_REF.findall(str(text or ""))))


def generated_issue(i: str) -> bool:
    return str(i).startswith(GENERATED_ISSUE_PREFIXES)


def broken_issue_refs(ids, known) -> list[str]:
    """The ids that are neither a known (promoted) issue nor generated by the build."""
    known = set(known or ())
    return [i for i in dict.fromkeys(ids or []) if i not in known and not generated_issue(i)]


def row_issue_refs(row) -> list[tuple[str, str]]:
    """[(where, id)] for every issue id a row carries: its `issues` and the notes of its readings."""
    out = [("issues", i) for i in row.issues]
    for it in row.interpretations:
        out += [(f"note of the reading at {it.stage}", i) for i in issue_refs(it.note)]
    return out


def activity_issue_refs(t: dict) -> list[tuple[str, str]]:
    """[(where, id)] for an activity template entry: gated_by, linked_issues, and ids in its note, name or item."""
    out = []
    for k in ("gated_by", "linked_issues"):
        v = t.get(k) or []
        out += [(k, i) for i in ([v] if isinstance(v, str) else v)]
    for k in ("note", "notes", "name", "item", "condition"):
        out += [(k, i) for i in issue_refs(t.get(k))]
    return out


def clarification_issue_refs(c: dict) -> list[tuple[str, str]]:
    """[(where, id)] for a clarification entry: linked_issues, and ids in its free-text fields."""
    out = [("linked_issues", i) for i in c.get("linked_issues") or []]
    for k in ("gap", "already_settled", "practical_impact", "interim_handling", "proposed_question", "note"):
        out += [(k, i) for i in issue_refs(c.get(k))]
    return out


def issue_ref_findings(rows, templates: dict, clarifications: dict, known, opfiles=()) -> list[dict]:
    """check-register (kind issue_ref): every broken issue reference in the curated rows, activity templates,
    clarification entries and amendment ops (their note and issue), on the item that carries it."""
    known = set(known or ())
    out = []
    for f in opfiles or ():
        for o in getattr(f, "ops", None) or []:
            for where in ("note", "issue"):
                for i in broken_issue_refs(issue_refs(getattr(o, where, None)), known):
                    out.append({"kind": "issue_ref", "where": o.id,
                                "detail": f"{BROKEN}: op {o.id} {where} names {i}, which is not an issue of the register"})
    for row in rows or []:
        for where, i in row_issue_refs(row):
            if broken_issue_refs([i], known):
                out.append({"kind": "issue_ref", "where": row.id,
                            "detail": f"{BROKEN}: {where} names {i}, which is not an issue of the register"})
    for ev, ts in (templates or {}).items():
        if str(ev).startswith("_"):
            continue
        for t in ts or []:
            for where, i in activity_issue_refs(t):
                if broken_issue_refs([i], known):
                    out.append({"kind": "issue_ref", "where": str(t.get("id")),
                                "detail": f"{BROKEN}: activity {t.get('id')} ({ev}) {where} names {i}, which is not an "
                                          "issue of the register"})
    for c in (clarifications or {}).get("clarifications") or []:
        for where, i in clarification_issue_refs(c):
            if where != "linked_issues" and broken_issue_refs([i], known):   # linked_issues: clarify.check reports it
                out.append({"kind": "issue_ref", "where": str(c.get("id")),
                            "detail": f"{BROKEN}: {where} names {i}, which is not an issue of the register"})
    return out
