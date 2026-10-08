"""Downstream tasks and validation for what an addendum implies beyond the units it changes (session 12, W3b).

Called from tenderpack.ai.downstream (tasks(), packet(), validate()); the findings come from tenderpack.derived
(deterministic). Four task kinds:

  reading_rows         reading:<region>   a reading of the addendum still pending a person's approval: its units (Arabic
                                          as printed, translations apart, pages, crops, bands or cells, uncertainties);
                                          rows and activities may be proposed FROM it, each `conditional_on: {reading,
                                          until: approval}`, never in force until a person approves the reading
  computed_date        date:<unit>        a deadline the program computed (calc.deadline: inputs, counting rule, result,
                                          fingerprint) that no row task covers: a milestone proposal (a row's date rule,
                                          or an activity with `computed_from`), conditional where the obligation is;
                                          ambiguous -> escalate. A deadline in a unit a row task (row_new, row_reading)
                                          already covers goes with that task (`computed_dates`), not as a task of its own.
                                          Session 12 (blind-06 follow-up 5): the task carries the register's `date_rule`
                                          (kind 'relative' with anchor, offset, unit, direction; 'unresolved' with the
                                          words and a "not computed: ..." note for a forward period the counting rules
                                          do not settle or an event anchor), and an activity's `computed_from` is matched
                                          by its fingerprint or recomputed from its inputs (derived.match_computed_from)
  condition_changed    cond:<unit> / defn:<unit>   a clause whose condition an op switched, or a definition an op
                                          changed, with the rows that need a re-read (a person decides; nothing applies)
  derived_consequence  cons:<unit>        a band the addendum sets, with the existing bid-out rules that share a term
                                          and the form rows to read with; a consequence row only quotes such a rule
                                          (human-owned unless the rule names the value); none -> an escalation with
                                          "no bid-out consequence stated"

Validation (validate_items, after downstream's pass 1): a row resting on a pending reading is marked `conditional_on`
(the reading named, its review subject pinned) and must cite the reading's own units; `conditional_on` naming any other
reading is invalid, and on an approved reading it is dropped (the row is ordinary); an activity for a conditional row is
conditional too; an activity's `computed_from` is recomputed (a different result is invalid; an ambiguous one is held);
a bid-out consequence must be stated by the words quoted, and a consequence quoted from another unit must be an existing
rule's (`derived_consequence`, human-owned when the rule's words do not name the value). Nothing is decided here."""
from __future__ import annotations

from .. import derived
from ..register import Row, effective

KINDS = ("reading_rows", "computed_date", "condition_changed", "derived_consequence")

_READING_EXPECT = (
    "propose the rows (row_new) the reading's table or form states (zones, heights, datum, scope, notices, units: the "
    "parameters read from these cells, the quote verbatim from the reading's source text, Arabic as printed; the "
    "translation is not evidence), each cites the reading's units and carries `conditional_on: {reading: %s, until: "
    "approval}`, and the activities they need carry the same field. They are never in force while the reading is "
    "pending: A1 shows them as PENDING READING, A3 and A5 leave them out. Where the reading and another rendering differ "
    "(a translation, an English appendix), say so in an issue or an escalation; never choose between them")


def tasks(ws, r2: dict, addendum: str, existing: list[dict]) -> list[dict]:
    """The tasks of the four kinds (see the module docstring), not duplicating an id already in `existing`."""
    from .downstream import window_fields
    have = {t["id"] for t in existing}
    out: list[dict] = []
    evals = {e["row"].id: e for e in r2["evals"]}
    for region, e in derived.pending_readings(r2, addendum).items():
        out.append({"id": f"reading:{region}", "kind": "reading_rows", "reading": region, "status": "pending",
                    "subject_sha256": e["subject_sha256"], "pages": e["pages"],
                    "conditional_on": {"reading": region, "until": "approval"},
                    "units": derived.reading_units(r2, region), "expect": _READING_EXPECT % region})
    covered: dict[str, dict] = {}                 # a unit a row task already covers: the date goes with that task
    for t in existing:
        us = (list(t.get("units_changed") or []) + list(t.get("attaches_to") or [])) if t["kind"] == "row_new" else \
            (list(t["row_def"]["units"]) + [c["effective_unit"] for c in t["changed_units"] if c.get("effective_unit")]
             if t["kind"] == "row_reading" else [])
        for u in us:
            covered.setdefault(u, t)
    for d in derived.computed_deadlines(r2, addendum):
        res = d["result"]
        if d["unit"] in covered:
            covered[d["unit"]].setdefault("computed_dates", []).append({
                "unit": d["unit"], "words": d["words"], "computed_from": d["computed_from"], "status": res.get("status"),
                "date_rule": d["date_rule"], **({"note": d["note"]} if d.get("note") else {}),
                "conditional": d["conditional"],
                "expect": "the row's date rule for these words plans this date (the program computed it; A1 shows the "
                          "derivation and any disagreement)"})
            continue
        tid = f"date:{d['unit']}" + ("" if not any(t["id"] == f"date:{d['unit']}" for t in out) else f":{d['words']}")
        rule_txt = ("`date_rule` (kind 'relative': its anchor, offset, unit and direction; dates.KINDS has no kind "
                    "'deadline', which is a purpose) copied unchanged into the row's `date_rules` with a rule_id of its "
                    "own" if d["date_rule"]["kind"] == "relative" else
                    "`date_rule` (kind 'unresolved': the words and the note) copied unchanged into the row's "
                    "`date_rules`, or the words as a date note")
        out.append({"id": tid, "kind": "computed_date", "unit": d["unit"], "pages": d["pages"],
                    "words": d["words"], "anchor": d["anchor"], "anchor_date": d["anchor_date"],
                    "computed_from": d["computed_from"], "date_rule": d["date_rule"], "status": res.get("status"),
                    "readings": res.get("readings"), **({"note": d["note"]} if d.get("note") else {}),
                    "conditional": d["conditional"], "rows": d["rows"],
                    "expect": (("a milestone proposal: an activity (milestone) whose `computed_from` is this object "
                                "unchanged, or a row whose date rule is this task's " + rule_txt + " (the program "
                                "recomputes either; nothing typed)") if res.get("status") == "resolved" else
                               (f"{d.get('note') or 'not computed'}: a row carries the words as this task's "
                                + rule_txt + "; never a typed date"))
                    + ("; the obligation is conditional, so the milestone is conditional (say on what)"
                       if d["conditional"] else "")
                    # session 14 (N1): an ambiguous count is still carried as the relative rule (planned at the
                    # earlier reading, the later kept); the escalation asks the counting question
                    + ("; AMBIGUOUS under the counting rules: carry the relative `date_rule` unchanged all the same "
                       "(the program plans at the earlier reading and keeps the later; never kind 'unresolved'), and "
                       "escalate the counting question; never choose a reading"
                       if res.get("escalate") else "")})
    for x in derived.switched(r2, addendum):
        rows = sorted(rid for rid, e in evals.items() if x["flag"] in (e["stages"].get(addendum) or {}).get("flags", []))
        out.append({"id": f"{'cond' if x['kind'] == 'condition' else 'defn'}:{x['unit']}", "kind": "condition_changed",
                    "unit": x["unit"], "op": x["op"], "changed_unit": x["changed_unit"], "words": x["words"],
                    "flag": x["flag"], **({"condition": x["condition"]} if x["kind"] == "condition" else {"term": x["term"]}),
                    "scope": {"units": [x["unit"], x["changed_unit"]], "rows": rows, "activities": [], "clarifications": []},
                    "expect": ("re-read each row against the changed condition or definition (row_reading at the "
                               "addendum, or an escalation): whether the clause now always, or never, applies is a "
                               "person's reading; an earlier answer that relied on it is listed under reread:")})
    for c in derived.consequence_candidates(r2, addendum):
        out.append({"id": f"cons:{c['unit']}", "kind": "derived_consequence", "unit": c["unit"], "band": c["band"],
                    "rules": c["rules"], "read_with": c["read_with"], "silent": c["silent"],
                    "expect": ("never invent a consequence the pack does not state. If an existing rule's words cover a "
                               "value outside the band, a row (row_new) whose consequence quotes that rule (its unit, "
                               "class and words): PROPOSED, a person decides whether the rule covers the value. If no "
                               f"rule covers it: an escalation saying '{derived.NO_CONSEQUENCE}'. Read the rule with "
                               "the forms that state the value (read_with)")})
    # an escalation (an unresolved or escalated provision, an answer to re-read) gets the existing bid-out rules that
    # share a defined term with its provision (a price-basis conflict read with VOL-I 11.5, 10.5 and the form that
    # confirms the price): what a person reads it with; a consequence is quoted from one of them or none is stated
    st2 = next(s for s in r2["stages"] if s.stage == addendum).state
    order = [s.stage for s in r2["stages"]]
    rules = derived.bid_out_rules(r2, order[order.index(addendum) - 1])
    for t in existing:
        if t["kind"] != "escalation" or t.get("bid_out_rules") is not None:
            continue
        u = st2.get(t.get("provision") or "")
        mine = derived.terms(u.text) if u is not None else set()
        hit = [{k: v for k, v in x.items() if k != "text"} | {"shared": sorted(mine & derived.terms(x["text"]))}
               for x in rules if mine & derived.terms(x["text"])]
        t["bid_out_rules"] = hit
        t["consequence_note"] = (("read with these existing rules; a consequence is quoted from one of them (PROPOSED, "
                                  "a person decides whether it applies), never invented") if hit else derived.NO_CONSEQUENCE)
    win = window_fields(r2, addendum)
    for t in out:
        if win and t["kind"] in ("condition_changed", "derived_consequence"):
            t.update(win)
    return [t for t in out if t["id"] not in have]


def packet_units(t: dict) -> list[str]:
    k = t["kind"]
    if k == "reading_rows":
        return [u["unit"] for u in t["units"]]
    if k == "computed_date":
        return [t["unit"]]
    if k == "condition_changed":
        return list(t["scope"]["units"])
    if k == "derived_consequence":
        return [t["unit"]] + [x["unit"] for x in t["rules"]] + [x["unit"] for x in t["read_with"]]
    return []


def _pending_regions(r2: dict, st2: dict, units: list[str], addendum: str) -> dict[str, str]:
    """{region: subject} of the addendum's own readings, still pending, that the given units are read from (effective at
    the addendum). A volume's reading pending since an earlier stage keeps the register's 'image reading pending' flag."""
    out = {}
    for uid in units:
        u = effective(st2, uid, True)
        if u is not None and u.origin == "image_reading" and u.reading_region and u.reading_status != "approved" \
                and u.doc == addendum:
            out.setdefault(u.reading_region, u.reading_subject)
    return out


def validate_items(ws, ds, F: list, r2: dict, addendum: str, rec, rows_existing: dict, provisions: set) -> None:
    """The session-12 (W3b) checks after downstream.validate's pass 1 (see the module docstring). `F` and `rec` are
    validate's per-item findings and its recorder; payloads are updated in place (the pydantic payload and the item)."""
    from ..register import Consequence
    st2 = next(s for s in r2["stages"] if s.stage == addendum).state
    order = [s.stage for s in r2["stages"]]
    prev = order[order.index(addendum) - 1]
    rules = derived.bid_out_rules(r2, prev)
    mine = {x.op.id for s in r2["stages"] if s.stage == addendum for x in s.ops if x.applied}
    add_units = set(provisions) | {k for k, u in st2.items() if set(u.history) & mine}
    deadlines = None
    conditional_rows: dict[str, str] = {}
    for i, it in enumerate(ds.items):
        pl = F[i]["pl"]
        if pl is None or F[i]["invalid"] or it.statement_type != "row_new":
            continue
        try:
            row = Row.model_validate(pl.row)
        except Exception:                                        # noqa: BLE001 (reported by pass 1)
            continue
        cons_units = [ip.consequence.unit for ip in row.interpretations if isinstance(ip.consequence, Consequence)]
        relied = _pending_regions(r2, st2, list(row.units) + cons_units, addendum)
        co = dict(pl.row.get("conditional_on") or {})
        if co and co.get("reading") not in relied:
            named = _pending_regions(r2, st2, list(row.units), addendum) or {}
            cited = {effective(st2, u, True).reading_region for u in row.units
                     if effective(st2, u, True) is not None and effective(st2, u, True).reading_region}
            if co.get("reading") in cited:                       # cited, and approved: the row is ordinary
                pl.row.pop("conditional_on", None)
                it.payload["row"].pop("conditional_on", None)
                rec(i, "conditional_on", True, f"reading {co.get('reading')} is approved: the row is ordinary "
                                               "(conditional_on dropped)")
            else:
                rec(i, "conditional_on", False, f"conditional_on names reading {co.get('reading')!r}, which the row does "
                                                f"not rest on (pending readings it cites: {sorted(named) or 'none'})",
                    "invalid")
                continue
        if not relied:
            continue
        if len(relied) > 1:
            rec(i, "conditional_on", False, f"the row rests on more than one pending reading ({sorted(relied)}): one "
                                            "row per reading", "insufficient")
            continue
        region, subject = next(iter(relied.items()))
        val = {"reading": region, "until": "approval", "subject_sha256": subject}
        pl.row["conditional_on"] = val
        it.payload["row"]["conditional_on"] = dict(val)
        conditional_rows[row.id] = region
        r_units = {u["unit_id"] for u in r2["units"] if (u.get("reading") or {}).get("region") == region}
        if not any(x.unit_id in r_units for x in it.evidence):
            rec(i, "conditional_on", False, f"the row rests on reading {region} (pending): cite the reading's cells "
                                            "(its unit ids and page) in the evidence", "insufficient")
        else:
            rec(i, "conditional_on", True, f"{derived.label(region)}: the reading is pending (no person has approved "
                                           "it); the row is proposed from it and is not in force until a person "
                                           "approves the reading (A1: PENDING READING; off A3 and A5)")
        F[i]["interp"].append("conditional on a pending reading")
    for i, it in enumerate(ds.items):                            # derived consequences (row_new)
        pl = F[i]["pl"]
        if pl is None or F[i]["invalid"] or it.statement_type != "row_new":
            continue
        try:
            row = Row.model_validate(pl.row)
        except Exception:                                        # noqa: BLE001
            continue
        texts = {x["unit"]: x["text"] for x in rules}
        res = derived.consequence_check(row, rules, texts, add_units)
        if not res["ok"]:
            rec(i, "derived consequence", False, res["why"], "invalid")
        elif res["derived"]:
            rule = next(x for x in rules if x["row"] == res["rule"])
            val = {"rule": res["rule"], "unit": rule["unit"], "owner": res["owner"], "basis": res["why"][:400]}
            pl.row["derived_consequence"] = val
            it.payload["row"]["derived_consequence"] = dict(val)
            rec(i, "derived consequence", True, res["why"][:400])
            if res["owner"] == "person":
                F[i]["human"].append(f"a derived consequence: {res['why']}"[:300])
    for i, it in enumerate(ds.items):                            # activities
        pl = F[i]["pl"]
        if pl is None or F[i]["invalid"] or it.statement_type != "activity":
            continue
        a = pl.activity
        def reading_of(x: str):
            co = getattr(rows_existing.get(x), "conditional_on", None)
            return conditional_rows.get(x) or (co.reading if co is not None else None)
        cond = {x: reading_of(x) for x in pl.rows}
        held = sorted({v for v in cond.values() if v})
        if held and not all(cond.values()):                      # it serves rows in force too: planned for them
            rec(i, "conditional_on", True, f"serves rows {derived.label(held[0])} and rows in force: planned for the "
                                           "rows in force; the conditional rows are not in force")
        elif held:
            val = {"reading": held[0], "until": "approval"}
            a["conditional_on"] = val
            it.payload["activity"]["conditional_on"] = dict(val)
            rec(i, "conditional_on", True, f"the activity serves rows {derived.label(held[0])}: conditional too, not "
                                           "planned while the reading is pending")
        cf = a.get("computed_from")
        if cf:
            if deadlines is None:
                deadlines = derived.computed_deadlines(r2, addendum)
            # session 12 (blind-06 follow-up 5): matched by its fingerprint or, failing that, recomputed from the
            # claimed inputs by the function the program used (derived.compute_deadline)
            known = derived.match_computed_from(cf, deadlines, r2["register"].cal_by_stage[addendum],
                                                r2["register"].rf.anchors)
            if known is None:
                rec(i, "computed_from", False, "computed_from matches no deadline the program computed for "
                                               f"{addendum} (its fingerprint; computed: "
                                               + "; ".join(f"{d['unit']} {d['computed_from']['result']}"
                                                           for d in deadlines)[:300] + ")", "invalid")
            elif known["result"].get("status") != "resolved":
                rec(i, "computed_from", False, f"{known['unit']}: '{known['words']}' is {known['result'].get('status')} "
                                               f"under the counting rules ({known['result'].get('reason')}): escalated, "
                                               "never chosen", "insufficient")
            elif cf.get("result") not in (None, known["computed_from"]["result"]):     # inputs only: the result is ours
                rec(i, "computed_from", False, f"the claimed result {cf.get('result')} is not the computed "
                                               f"{known['computed_from']['result']} ({known['unit']}: '{known['words']}')",
                    "invalid")
            else:
                val = dict(known["computed_from"], **({"conditional": known["conditional"]} if known["conditional"]
                                                      else {}))
                a["computed_from"] = val
                it.payload["activity"]["computed_from"] = dict(val)
                rec(i, "computed_from", True, f"recomputed: {known['unit']} '{known['words']}' -> "
                                              f"{known['computed_from']['result']} (rule {known['computed_from']['counting']}"
                                              f", fingerprint {known['computed_from']['fingerprint'][:12]})"
                                              + ("; CONDITIONAL" if known["conditional"] else ""))
