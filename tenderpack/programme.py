"""A5 Stage 4: documents, marshalling, resources, disciplines, drivers and scenarios, built on one stage's programme
(schedule.plan), and the A5 files including the Gantt (tenderpack.gantt) and an explanation (a5/README.md).

Everything here is computed from the programme and the configured ASSUMPTIONS (config/assumptions.yaml);
nothing is typed. Every lead time, staff effort, external party waited on, multiplicity and capacity is a
PROVISIONAL assumption with a basis and an owner; none is a fact from the tender pack. Pure functions; only
`write` touches the file system.

  extend(prog, evidence_items, assumptions, cal) -> prog + {documents, marshalling, resources, disciplines, drivers}:
      documents   per evidence item in force: envelope, issuer, per, multiplicity (bidder settings; a template
                  `_per_overrides` entry gives a count the vocabulary cannot express, e.g. per foreign member, VOL-I
                  8.9), physical count = multiplicity x (marked originals + hard copies) for items counted in the
                  VOL-I 6.5 copies, electronic copy yes/no; per-envelope totals (both envelopes always listed)
      marshalling ONE line per evidence item needed by a row in force (none is missing): issuer, envelope, count
                  (per proposal / member / foreign member / signatory ...), the item's own activities, preparation
                  lead time (labelled ASSUMPTION, with its keys), latest start of its first step, needed-by (latest
                  finish of the step that produces it), earliest finish, float, the three statuses, requirement ids
      resources   staff load per role per Working Day (schedule.resource_load: effort spread over the late window
                  clipped at the planning date) vs the role's capacity; every OVERLOAD run with dates and load vs
                  capacity; resource levelling is NOT implemented (overloads are reported, not resolved)
      disciplines per discipline (Legal, Commercial, Technical, Bid management, Document control): activities,
                  staff effort, external waiting, gates, infeasible activities, overloads
      drivers     for each INFEASIBLE or DEADLINE PASSED activity: the chain that sets its earliest start (from the
                  planning date) and the chain that sets its latest finish (to the pack deadline); the lead-time
                  assumptions on them; the shortfall (negative float) in Working Days; and what would make it
                  feasible (the largest value of each lead time that would, a later deadline)
  run_scenarios(make_plan, assumptions, scenarios, evidence_items=None) -> baseline, each scenario's
      programme and its changes against the baseline (dates, float, statuses, documents, overloads)
  stage_planner(r, stage=None) -> make_plan for run_scenarios from a stage2.run result (re-evaluates the
      register's dates when a scenario changes the calendar, e.g. a declared holiday moves the cut-off)
  write(prog_ext, scenarios_result, out_dir) -> a5/{programme,marshalling,documents,resources,overloads,disciplines,
      milestones,drivers,scenario_comparison,requirements_not_carried}.{csv,json}, a5/scenarios/<name>.{csv,json},
      a5/gantt.{svg,html,pdf} and a5/README.md (session 12: the rows not carried with their reason, A5-4; the A1-to-A5
      discipline mapping, A5-8)
  coverage_check(prog) -> C48 (reported): every A1 row in force carried or excepted with a reason (session 12, A5-4)
"""
from __future__ import annotations

import copy
import re
from datetime import date
from pathlib import Path

from .dates import Calendar, calendar_from_config
from .render import write_csv_json
from .schedule import (BLOCKING_FLAGS, DISCIPLINES, LOAD_WINDOW, NO_LEVELLING, PROVISIONAL, date_span, multiplicity,
                       network, plan, resource_load, resource_statuses)
from .util import write_text

NOTICE = ("PROPOSAL, not reviewed. Every lead time, staff effort, external party waited on, multiplicity and resource "
          "capacity is a PROVISIONAL ASSUMPTION (config/assumptions.yaml: value, basis, owner); none is stated in the "
          "tender pack. Earliest dates come from a forward pass from the planning date (the latest addendum's issue "
          "date), latest dates from a backward pass in Working Days (VOL-I 2.4) from the pack's dates; negative float is "
          f"INFEASIBLE, never compressed. Timing, decision readiness and resource feasibility are separate statuses; "
          f"{NO_LEVELLING}. No bidder references, certificates, attendance or financial standing are assumed to exist.")
BAD = ("INFEASIBLE", "DEADLINE PASSED")


def _d(s: str | None) -> date | None:
    return date.fromisoformat(s) if s else None


def _bad(status: str) -> bool:
    return status.startswith(BAD)


# ---------------------------------------------------------------------------------------------- documents

def documents(prog: dict, evidence_items: dict, assumptions: dict) -> dict:
    """Per evidence item in force: what is submitted, how many, where; and totals per envelope."""
    bidder = assumptions.get("bidder") or {}
    basis = assumptions.get("bidder_basis") or {}
    sub = assumptions.get("submission") or {}
    n_orig, n_copy = int(sub.get("marked_originals", 1)), int(sub.get("hard_copies", 3))
    usb = int(sub.get("usb_per_envelope", 1))
    excl = sub.get("exclusive_list") or {}
    overrides = prog.get("per_overrides") or {}
    need = prog.get("evidence_needed")
    if need is None:                                       # a programme from an older plan(): derive from activities
        need = {}
        for a in prog["activities"]:
            for ev in a.get("evidence_items") or [a.get("evidence")]:
                need.setdefault(ev, set()).update(a["req_ids"])
        need = {k: sorted(v) for k, v in need.items()}
    acts_by_ev: dict[str, list[str]] = {}
    for a in prog["activities"]:
        for ev in a.get("evidence_items") or [a.get("evidence")]:
            acts_by_ev.setdefault(ev, []).append(a["id"])
    items = []
    for ev_id in sorted(need):
        it = evidence_items.get(ev_id)
        if it is None:
            items.append({"evidence": ev_id, "name": "", "envelope": "", "kind": "UNKNOWN", "issuer": "", "per": "",
                          "multiplicity": None, "multiplicity_basis": "", "marked_originals": 0, "hard_copies": 0,
                          "physical_count": 0, "electronic_copy": "no", "req_ids": need[ev_id],
                          "activities": sorted(acts_by_ev.get(ev_id, [])), "source": "",
                          "flags": ["not in the evidence vocabulary (curation/evidence_items)"]})
            continue
        flags = []
        ov = overrides.get(ev_id) or {}
        per = ov.get("per") or it.per
        try:
            n, expr = multiplicity(per, bidder)
        except KeyError as e:
            n, expr = 1, ""
            flags.append(f"multiplicity unknown ({e.args[0]}); counted once")
        if expr:
            owners = [f"{k.split('.')[1].split(' ')[0]}: {basis.get(k.split('.')[1].split(' ')[0], {}).get('owner', '?')}"
                      for k in expr.split(" x ")]
            expr = f"{expr} (PROVISIONAL ASSUMPTION; owner {', '.join(owners)})"
        if ov:
            expr = (expr or "one per proposal") + (f"; counted per {per} as {ov.get('source', '')} says ({ov.get('reason', '')}); "
                                                    f"the vocabulary says per {it.per}")
        if n == 0:
            flags.append(f"count 0 under the assumed bidder ({expr.split(' (')[0]}): nothing to submit")
        counted = bool(it.counted) and it.envelope in ("A", "B")
        kind = "document" if counted else ("document (not copied)" if it.envelope in ("A", "B") else "action")
        if it.envelope == excl.get("envelope") and excl.get("source_unit") and excl["source_unit"] not in it.source:
            flags.append(f"OPEN ISSUE: {excl['source_unit']} says Envelope {it.envelope} contains only the documents it "
                         f"lists; this item is required by {it.source}, so where it goes needs a clarification")
        if ev_id not in acts_by_ev:
            reason = (prog.get("exceptions") or {}).get(ev_id)
            flags.append(f"no activity: {reason}" if reason else "no activity and no exception (C44)")
        items.append({"evidence": ev_id, "name": it.name, "envelope": it.envelope, "kind": kind, "issuer": it.issuer,
                      "per": per, "multiplicity": n, "multiplicity_basis": expr or "one per proposal",
                      "marked_originals": n * n_orig if counted else 0, "hard_copies": n * n_copy if counted else 0,
                      "physical_count": n * (n_orig + n_copy) if counted else 0,
                      "electronic_copy": "yes" if counted and n else "no", "req_ids": need[ev_id],
                      "activities": sorted(acts_by_ev.get(ev_id, [])), "source": it.source, "flags": flags})
    totals = []
    for env in ("A", "B"):
        rows = [i for i in items if i["envelope"] == env]
        docs = [i for i in rows if i["kind"] == "document"]
        flags = []
        if not rows:
            flags.append(f"no row in force needs an Envelope {env} item: VOL-I 6.2 requires both envelopes; "
                         "check the register covers them")
        flags += sorted({f for i in rows for f in i["flags"] if f.startswith("OPEN ISSUE")})
        totals.append({"envelope": env, "items": len(rows), "documents": sum(i["multiplicity"] or 0 for i in docs),
                       "marked_originals": sum(i["marked_originals"] for i in docs),
                       "hard_copies": sum(i["hard_copies"] for i in docs),
                       "physical_count": sum(i["physical_count"] for i in docs),
                       "electronic_files": sum(i["multiplicity"] or 0 for i in docs), "usb": usb if rows else 0,
                       "evidence": [i["evidence"] for i in rows], "flags": flags})
    notes = [f"Physical count = multiplicity x ({n_orig} marked original + {n_copy} hard copies), stated in the pack "
             f"({sub.get('source', 'VOL-I 6.5')}); multiplicities come from the bidder settings (PROVISIONAL ASSUMPTIONS).",
             f"Electronic copy: {sub.get('electronic_copy', 'per VOL-I 6.5')}; {usb} encrypted USB per envelope is a "
             "PROVISIONAL reading (VOL-I 6.5 with 6.2: no commercial information in Envelope A), to confirm by clarification."]
    return {"items": items, "totals": totals, "notes": notes}


# ---------------------------------------------------------------------------------------------- marshalling

def _lead_label(a: dict) -> str:
    eff = a.get("effort_total_wd")
    parts = [a["id"]] + ([f"staff effort {eff:g} WD"] if isinstance(eff, (int, float)) else []) \
        + ([f"waits on {a['waiting_on']}"] if a.get("waiting_on") else [])
    return f"{a['duration_assumption']} = {a['duration_wd']} WD elapsed ({'; '.join(parts)})"


def marshalling(prog: dict, docs: dict) -> list[dict]:
    """ONE line per evidence item needed by a row in force (every physical or documentary item, and the actions),
    with its issuer, count, preparation lead time (ASSUMPTION), latest start, needed-by date and requirement ids."""
    by_doc = {i["evidence"]: i for i in docs["items"]}
    totals = docs["totals"]
    acts = prog["activities"]
    out = []
    for ev, req in sorted((prog.get("evidence_needed") or {}).items()):
        d = by_doc.get(ev, {})
        mine = [a for a in acts if ev in (a.get("evidence_items") or [a.get("evidence")])]
        ids = {a["id"] for a in mine}
        flags = list(d.get("flags") or [])
        row = {"evidence": ev, "name": d.get("name", ""), "kind": d.get("kind", ""), "envelope": d.get("envelope", ""),
               "issuer": d.get("issuer", ""), "per": d.get("per", ""), "count": d.get("multiplicity"),
               "count_basis": d.get("multiplicity_basis", ""), "req_ids": list(req)}
        if not mine:
            out.append({**row, "item": d.get("name", ""), "activity": "", "activities": [], "lead_time_wd": None,
                        "clarification_questions": [], "ask_by": None,
                        "lead_time_keys": [], "lead_time_basis": "", "waiting_on": "", "drop_dead_start": None,
                        "needed_by": None, "earliest_finish": None, "float_wd": None, "status": "NO ACTIVITY",
                        "timing_status": "NO ACTIVITY", "decision_status": "", "resource_status": "",
                        "marked_originals": 0, "hard_copies": 0, "physical_count": 0, "electronic_copy": "no",
                        "flags": flags + ["no activity produces this item (see C44 and the exceptions)"]})
            continue
        feeds = {p for a in mine for p in a["predecessors"] if p in ids}
        ends = [a for a in mine if a["id"] not in feeds]
        prod = sorted(ends, key=lambda a: (not a.get("item"), -(_d(a["latest_finish"]) or date.min).toordinal(), a["id"]))[0]
        # longest chain of the item's own activities (elapsed Working Days)
        by = {a["id"]: a for a in mine}
        memo: dict[str, tuple[int, list[str]]] = {}

        def chain(aid: str) -> tuple[int, list[str]]:
            if aid not in memo:
                best = max((chain(p) for p in by[aid]["predecessors"] if p in by), default=(0, []))
                memo[aid] = (best[0] + int(by[aid]["duration_wd"]), best[1] + [aid])
            return memo[aid]
        lt, path = max((chain(a["id"]) for a in mine), key=lambda x: (x[0], x[1]))
        if d.get("kind") == "document":
            counts = {"marked_originals": d["marked_originals"], "hard_copies": d["hard_copies"],
                      "physical_count": d["physical_count"], "electronic_copy": d["electronic_copy"]}
        elif d.get("envelope") == "A+B":                   # copies, sealing, delivery: both envelopes together
            counts = {"marked_originals": sum(t["marked_originals"] for t in totals),
                      "hard_copies": sum(t["hard_copies"] for t in totals),
                      "physical_count": sum(t["physical_count"] for t in totals),
                      "electronic_copy": f"{sum(t['usb'] for t in totals)} USB (PROVISIONAL: one per envelope)"}
        else:
            counts = {"marked_originals": 0, "hard_copies": 0, "physical_count": 0, "electronic_copy": "no"}
        order = sorted(mine, key=lambda a: (a["latest_start"] or "9999", a["id"]))
        flags += [f"{a['id']}: {a['status']}" for a in order if a["id"] != prod["id"] and a["status"] != "OK"]
        # session 11 (audit A5-6): the flags of the item's activities (review, blocked, stale, ...) where it appears
        flags = list(dict.fromkeys(flags + [f"{a['id']}: {f}" for a in order for f in a.get("flags") or []
                                            if not f.startswith(BLOCKING_FLAGS + ("CONDITIONAL (only if",))]))
        gated = [a for a in mine if a.get("gated_by")]
        out.append({**row, **counts, "item": prod.get("item") or d.get("name", ""), "activity": prod["id"],
                    "activities": [a["id"] for a in order], "lead_time_wd": lt, "lead_time_chain": path,
                    "lead_time_keys": list(dict.fromkeys(a["duration_assumption"] for a in order)),
                    "lead_time_basis": f"{PROVISIONAL} (config/assumptions.yaml lead_times): "
                                       + "; ".join(_lead_label(a) for a in order),
                    # session 12 (audit A5-1): the drafted questions on the item's activities and the last day to ask
                    "clarification_questions": sorted({q for a in mine for q in a.get("clarification_questions") or []}),
                    "ask_by": min((a["ask_by"] for a in mine if a.get("ask_by")), default=None),
                    "waiting_on": "; ".join(sorted({a["waiting_on"] for a in mine if a.get("waiting_on")})),
                    "drop_dead_start": min((a["latest_start"] for a in mine if a["latest_start"]), default=None),
                    "needed_by": (f"{prod['latest_finish']} {prod['latest_finish_time']}" if prod.get("latest_finish_time")
                                  else prod["latest_finish"]), "earliest_finish": prod.get("earliest_finish"),
                    "float_wd": prod.get("float_wd"), "status": prod["status"], "timing_status": prod["status"],
                    "decision_status": "; ".join(f"{a['id']}: {a['decision_status']}" for a in gated) or "READY",
                    "resource_status": "; ".join(sorted({f"{a['id']}: {a['resource_status']}" for a in mine
                                                         if a.get("resource_status", "OK").startswith("OVERLOAD")})) or "OK",
                    "owner": prod["owner"], "resource": prod.get("resource", ""), "flags": flags})
    return sorted(out, key=lambda m: (m["drop_dead_start"] or "9999", m["evidence"]))


# ---------------------------------------------------------------------------------------------- resources

def resources(prog: dict, assumptions: dict, cal: Calendar) -> dict:
    """Staff load per role per Working Day vs capacity; overload runs; the statuses of each activity."""
    roles = assumptions.get("resources") or {}
    load = resource_load(prog["activities"], roles, cal, _d(prog["status_date"]))
    rows = []
    for r in sorted(load["daily"]):
        cfg = roles.get(r) or {}
        for day, v in sorted(load["daily"][r].items()):
            y, w, _ = date.fromisoformat(day).isocalendar()
            rows.append({"resource": r, "date": day, "iso_week": f"{y}-W{w:02d}", "load_wd": v["load"],
                         "capacity": v["capacity"],
                         "status": ("NO CAPACITY CONFIGURED" if v["capacity"] is None else "OVERLOAD" if v["over"] else "OK"),
                         "activities": [f"{i} ({s:g})" for i, s in v["activities"]],
                         "capacity_basis": cfg.get("basis", "not configured"), "capacity_owner": cfg.get("owner", "")})
    return {"rows": rows, "overloads": load["overloads"], "window": LOAD_WINDOW,
            "roles": {k: dict(v) for k, v in sorted(roles.items())},
            "statuses": resource_statuses(prog["activities"], load), "notes": load["notes"]}


def disciplines(prog: dict) -> list[dict]:
    out = []
    for disc in DISCIPLINES:
        xs = sorted((a for a in prog["activities"] if a.get("discipline") == disc), key=lambda a: a["id"])
        out.append({"discipline": disc, "activities": len(xs), "activity_ids": [a["id"] for a in xs],
                    "elapsed_wd": sum(int(a["duration_wd"]) for a in xs),
                    "staff_effort_wd": round(sum(float(a.get("effort_total_wd") or 0) for a in xs), 2),
                    "waiting_activities": sum(1 for a in xs if a.get("waiting_on")),
                    "external_parties": sorted({a["waiting_on"] for a in xs if a.get("waiting_on")}),
                    "roles": sorted({a.get("resource", "") for a in xs}),
                    "gated": [a["id"] for a in xs if a.get("gated_by")],
                    "infeasible": [a["id"] for a in xs if a["status"].startswith("INFEASIBLE")],
                    "overloaded": [a["id"] for a in xs if str(a.get("resource_status", "")).startswith("OVERLOAD")]})
    return out


# ---------------------------------------------------------------------------------------------- drivers

def _graph(prog: dict) -> dict[str, dict]:
    return {a["id"]: {"duration_wd": int(a["duration_wd"]), "predecessors": list(a["predecessors"]),
                      "deadline_rule": a.get("deadline_rule"), "deadline_date": _d(a.get("deadline_date")),
                      "buffer_wd": int(a.get("deadline_buffer_wd") or 0),
                      "key": a["duration_assumption"]} for a in prog["activities"]}


def _net_with(g: dict, cal: Calendar, start: date, cache: dict, key: str | None = None, value: int | None = None,
              shift_rule: str | None = None, shift_wd: int = 0) -> dict:
    k = (key, value, shift_rule, shift_wd)
    if k not in cache:
        h = {n: dict(v) for n, v in g.items()}
        for v in h.values():
            if key is not None and v["key"] == key:
                v["duration_wd"] = value
            if shift_rule and v["deadline_rule"] == shift_rule and v["deadline_date"] is not None:
                v["deadline_date"] = cal.add_working_days(v["deadline_date"], shift_wd)
        cache[k] = network(h, cal, start)
    return cache[k]


def _ok(t: dict) -> bool:
    return t["float_wd"] is None or t["float_wd"] >= 0


def drivers(prog: dict, assumptions: dict, cal: Calendar) -> list[dict]:
    lead = assumptions.get("lead_times") or {}
    sd = _d(prog["status_date"])
    g = _graph(prog)
    cache: dict = {}
    net = _net_with(g, cal, sd, cache)
    out = []
    for a in sorted(prog["activities"], key=lambda x: (x["latest_start"] or "9999", x["id"])):
        if not _bad(a["status"]):
            continue
        chain, cur = [a["id"]], a["id"]
        while net[cur]["driven_by"] and not net[cur]["driven_by"].startswith("deadline:"):
            cur = net[cur]["driven_by"]
            chain.append(cur)
        fwd, cur = [], a["id"]
        while net[cur]["es_driven_by"] not in (None, "planning date"):
            cur = net[cur]["es_driven_by"]
            fwd.insert(0, cur)
        rule, dl = g[chain[-1]]["deadline_rule"], g[chain[-1]]["deadline_date"]
        keys = list(dict.fromkeys(g[x]["key"] for x in [a["id"]] + fwd + chain[1:]))
        lts = [f"{k} = {lead.get(k, {}).get('value', '?')} WD ({PROVISIONAL}; owner {lead.get(k, {}).get('owner', '?')})"
               for k in keys]
        options = []
        if a["status"].startswith("DEADLINE PASSED"):
            own = _d(a.get("deadline_date"))
            short = cal.working_days_between(own, sd) if own else None
            options.append(f"none by planning: {a.get('deadline_rule')} = {a.get('deadline_date')} passed {short} WD before "
                           f"the status date {sd}; record whether it was done (owner {a['owner']})")
        else:
            short = -int(net[a["id"]]["float_wd"])
            alone = []
            for k in keys:
                v0 = int(lead.get(k, {}).get("value", g[a["id"]]["duration_wd"]))
                best = next((v for v in range(v0 - 1, -1, -1) if _ok(_net_with(g, cal, sd, cache, k, v)[a["id"]])), None)
                if best is None:
                    alone.append(k)
                else:
                    options.append(f"{k} <= {best} WD (now {v0}; PROVISIONAL ASSUMPTION, owner "
                                   f"{lead.get(k, {}).get('owner', '?')})")
            if alone:
                options.append(f"not enough on its own (even at 0 WD): {', '.join(alone)}")
            if rule and dl:
                n = next((n for n in range(1, short + 60)
                          if _ok(_net_with(g, cal, sd, cache, shift_rule=rule, shift_wd=n)[a["id"]])), None)
                if n is not None:
                    options.append(f"{rule} on or after {cal.add_working_days(dl, n).isoformat()} ({n} WD later; only the "
                                   "Authority can move a pack date, e.g. after a clarification request)")
            # session 12 (audit A5-1): the questions drafted on the rows of the activity and the chain that sets its
            # earliest start, and the last day to decide whether to ask the Authority
            by_id = {x["id"]: x for x in prog["activities"]}
            qs = sorted({q for x in [a["id"]] + fwd for q in by_id[x].get("clarification_questions") or []})
            ask = min((by_id[x]["ask_by"] for x in [a["id"]] + fwd if by_id[x].get("ask_by")), default=None)
            if qs:
                options.append(f"ask the Authority (drafted, not sent: {', '.join(qs)}): decide whether to ask by "
                               + (f"{ask} (the clarification cut-off route; a person decides)" if ask else
                                  "no date (no activity must finish by the clarification cut-off at this stage)"))
            ls = _d(a["latest_start"])
            options.append(f"start by {a['latest_start']}: already passed at the planning date {sd}" if ls and ls < sd else
                           f"the chain before it ({' -> '.join(fwd) or 'none'}) cannot finish before its latest start "
                           f"{a['latest_start']}; earliest start {a.get('earliest_start')}")
        out.append({"activity": a["id"], "name": a["name"], "status": a["status"], "resource": a.get("resource", ""),
                    "shortfall_wd": short, "float_wd": a.get("float_wd"), "earliest_start": a.get("earliest_start"),
                    "latest_start": a["latest_start"], "latest_finish": a["latest_finish"],
                    "status_date": prog["status_date"], "deadline": f"{rule} = {dl.isoformat()}" if rule and dl else "",
                    "forward_chain": fwd, "chain": chain, "lead_times": keys, "lead_time_values": lts,
                    "would_make_feasible": options, "req_ids": a["req_ids"]})
    return out


# ---------------------------------------------------------------------------------------------- extend

def _cal_dict(cal: Calendar) -> dict:
    return {"weekend": sorted(cal.weekend), "holidays": sorted(h.isoformat() for h in cal.holidays)}


def extend(prog: dict, evidence_items: dict, assumptions: dict, cal: Calendar) -> dict:
    """The stage programme with documents, marshalling, resources, disciplines and drivers. Pure."""
    out = copy.deepcopy(prog)
    for a in out["activities"]:
        a.setdefault("evidence_items", [a.get("evidence")])
        if not a.get("envelope"):
            a["envelope"] = getattr(evidence_items.get(a.get("evidence")), "envelope", "")
        a.setdefault("resource", "")
        a.setdefault("deadline_date", (out.get("deadlines") or {}).get(a.get("deadline_rule"), {}).get("date"))
    out["calendar"] = _cal_dict(cal)
    out["documents"] = documents(out, evidence_items, assumptions)
    res = resources(out, assumptions, cal)
    for a in out["activities"]:
        a["resource_status"] = res["statuses"][a["id"]]
    out["resources"] = res
    out["marshalling"] = marshalling(out, out["documents"])
    out["disciplines"] = disciplines(out)
    out["drivers"] = drivers(out, assumptions, cal)
    out["assumptions"] = {k: copy.deepcopy(assumptions.get(k)) for k in
                          ("planning", "calendar", "bidder", "bidder_basis", "resources", "lead_times", "submission")}
    return out


# ---------------------------------------------------------------------------------------------- scenarios

def apply_overrides(assumptions: dict, overrides: dict, name: str = "") -> dict:
    """A deep copy of the assumptions with `overrides` deep-merged in (mappings merge, anything else replaces).
    An override naming a key the assumptions do not have is an error (a typo must not pass silently).
    A lead time whose value changes without a new basis has its basis labelled with the scenario."""
    out = copy.deepcopy(assumptions)

    def merge(dst: dict, src: dict, path: str) -> None:
        for k, v in src.items():
            p = f"{path}.{k}" if path else str(k)
            if k not in dst:
                raise ValueError(f"scenario {name}: override '{p}' names nothing in the assumptions")
            if isinstance(v, dict) and isinstance(dst[k], dict):
                merge(dst[k], v, p)
            else:
                dst[k] = copy.deepcopy(v)

    merge(out, overrides or {}, "")
    for k, lt in (out.get("lead_times") or {}).items():
        b = (assumptions.get("lead_times") or {}).get(k) or {}
        if lt.get("value") != b.get("value") and lt.get("basis") == b.get("basis"):
            lt["basis"] = f"SCENARIO {name}: {b.get('value')} -> {lt['value']} WD (base: {b.get('basis')})"
    return out


def _flat(d, path=""):
    if isinstance(d, dict):
        return [x for k, v in d.items() for x in _flat(v, f"{path}.{k}" if path else str(k))]
    if isinstance(d, (list, tuple)):
        return [f"{path} = [{', '.join(str(x) for x in d)}]"]
    return [f"{path} = {d}"]


def _summary(p: dict) -> dict:
    acts = p["activities"]
    tot = {t["envelope"]: t for t in (p.get("documents") or {}).get("totals", [])}
    return {"infeasible": sorted(a["id"] for a in acts if a["status"].startswith("INFEASIBLE")),
            "deadline_passed": sorted(a["id"] for a in acts if a["status"].startswith("DEADLINE PASSED")),
            "conditional": sorted(a["id"] for a in acts if a["status"].startswith("CONDITIONAL")),
            "gated": sorted(a["id"] for a in acts if a.get("gated_by")),
            "physical_A": tot.get("A", {}).get("physical_count"), "physical_B": tot.get("B", {}).get("physical_count"),
            "overloads": sorted(f"{o['resource']} {o['from']}..{o['to']} ({o['peak_load']:g}/{o['capacity']})"
                                for o in (p.get("resources") or {}).get("overloads", []))}


def compare(base: dict, scen: dict, cal: Calendar) -> dict:
    """Changes from the baseline programme to a scenario programme (both extended)."""
    b = {a["id"]: a for a in base["activities"]}
    s = {a["id"]: a for a in scen["activities"]}
    acts = []
    for k in sorted(set(b) | set(s), key=lambda k: ((s.get(k) or b[k])["latest_start"] or "9999", k)):
        x, y = b.get(k), s.get(k)
        change = []
        if x is None:
            change.append("NEW")
        elif y is None:
            change.append("REMOVED")
        else:
            if (x["latest_start"], x["latest_finish"]) != (y["latest_start"], y["latest_finish"]):
                change.append("MOVED")
            if x.get("earliest_start") != y.get("earliest_start"):
                change.append("EARLY DATES")
            if x["status"] != y["status"]:
                change.append("STATUS")
            if x["duration_wd"] != y["duration_wd"]:
                change.append("DURATION")
            if x.get("count") != y.get("count"):
                change.append("COUNT")
        shift = (cal.working_days_between(_d(x["latest_start"]), _d(y["latest_start"]))
                 if x and y and x["latest_start"] and y["latest_start"] else None)
        acts.append({"id": k, "name": (y or x)["name"], "resource": (y or x).get("resource", ""),
                     "duration_assumption": (y or x)["duration_assumption"],
                     "duration_wd_base": x["duration_wd"] if x else None, "duration_wd": y["duration_wd"] if y else None,
                     "count_base": x.get("count") if x else None, "count": y.get("count") if y else None,
                     "earliest_start_base": x.get("earliest_start") if x else None,
                     "earliest_start": y.get("earliest_start") if y else None,
                     "latest_start_base": x["latest_start"] if x else None, "latest_start": y["latest_start"] if y else None,
                     "latest_finish_base": x["latest_finish"] if x else None, "latest_finish": y["latest_finish"] if y else None,
                     "float_wd_base": x.get("float_wd") if x else None, "float_wd": y.get("float_wd") if y else None,
                     "shift_wd": shift, "status_base": x["status"] if x else None, "status": y["status"] if y else None,
                     "change": change})
    status = [f"{a['id']}: {a['status_base']} -> {a['status']}" for a in acts if "STATUS" in a["change"]]
    bd = {i["evidence"]: i for i in base["documents"]["items"]}
    sdoc = {i["evidence"]: i for i in scen["documents"]["items"]}
    docs = [f"{k}: x{bd[k]['multiplicity']} -> x{sdoc[k]['multiplicity']} (physical {bd[k]['physical_count']} -> "
            f"{sdoc[k]['physical_count']})" for k in sorted(set(bd) & set(sdoc))
            if (bd[k]["multiplicity"], bd[k]["physical_count"]) != (sdoc[k]["multiplicity"], sdoc[k]["physical_count"])]
    docs += [f"{k}: {'added' if k in sdoc else 'removed'}" for k in sorted(set(bd) ^ set(sdoc))]
    bt = {t["envelope"]: t for t in base["documents"]["totals"]}
    st = {t["envelope"]: t for t in scen["documents"]["totals"]}
    totals = [f"Envelope {e}: physical {bt[e]['physical_count']} -> {st[e]['physical_count']}, documents "
              f"{bt[e]['documents']} -> {st[e]['documents']}" for e in sorted(bt) if e in st and
              (bt[e]["physical_count"], bt[e]["documents"]) != (st[e]["physical_count"], st[e]["documents"])]
    sb, ss = _summary(base), _summary(scen)
    key = lambda o: o.rsplit(" (", 1)[0]                      # noqa: E731
    ob, os_ = {key(o): o for o in sb["overloads"]}, {key(o): o for o in ss["overloads"]}
    res = ([f"new OVERLOAD: {os_[k]}" for k in sorted(set(os_) - set(ob))] +
           [f"OVERLOAD cleared: {ob[k]}" for k in sorted(set(ob) - set(os_))] +
           [f"OVERLOAD changed: {ob[k]} -> {os_[k]}" for k in sorted(set(ob) & set(os_)) if ob[k] != os_[k]])
    return {"activities": acts, "status_changes": status, "document_changes": docs, "envelope_totals": totals,
            "resource_changes": res, "baseline": sb, "scenario": ss}


def run_scenarios(make_plan, assumptions: dict, scenarios: dict, evidence_items: dict | None = None) -> dict:
    """make_plan(assumptions) -> a stage programme (schedule.plan output, extended or not). Each scenario's
    overrides are deep-merged into a copy of the assumptions and the programme is rebuilt and compared with
    the baseline. `scenarios`: the loaded config/scenarios.yaml ({scenarios: {name: {purpose, overrides,
    hypothetical?}}}) or its inner mapping. A plain plan() output is extended with `evidence_items`."""
    specs = scenarios.get("scenarios", scenarios) if isinstance(scenarios, dict) else scenarios

    def build(a: dict) -> dict:
        p = make_plan(a)
        if "documents" not in p:
            p = extend(p, evidence_items or {}, a, calendar_from_config(a.get("calendar")))
        return p

    base = build(assumptions)
    out, rows = {}, []
    for name, spec in specs.items():
        spec = spec or {}
        merged = apply_overrides(assumptions, spec.get("overrides") or {}, name)
        prog = build(merged)
        cmp_ = compare(base, prog, calendar_from_config(merged.get("calendar")))
        moved = [a for a in cmp_["activities"] if "MOVED" in a["change"]]
        shifts = [a["shift_wd"] for a in moved if a["shift_wd"] is not None]
        out[name] = {"name": name, "purpose": spec.get("purpose", ""), "hypothetical": bool(spec.get("hypothetical")),
                     "overrides": _flat(spec.get("overrides") or {}), "programme": prog, "changes": cmp_}
        sb, ss = cmp_["baseline"], cmp_["scenario"]
        rows.append({"scenario": name, "purpose": spec.get("purpose", ""), "hypothetical": bool(spec.get("hypothetical")),
                     "overrides": out[name]["overrides"], "activities_moved": len(moved),
                     "latest_start_shift_wd": (f"{min(shifts)}..{max(shifts)}" if shifts else ""),
                     "status_changes": cmp_["status_changes"],
                     "infeasible_base": len(sb["infeasible"]), "infeasible": len(ss["infeasible"]),
                     "deadline_passed_base": len(sb["deadline_passed"]), "deadline_passed": len(ss["deadline_passed"]),
                     "physical_A_base": sb["physical_A"], "physical_A": ss["physical_A"],
                     "physical_B_base": sb["physical_B"], "physical_B": ss["physical_B"],
                     "document_changes": cmp_["document_changes"],
                     "overloads_base": len(sb["overloads"]), "overloads": len(ss["overloads"]),
                     "resource_changes": cmp_["resource_changes"],
                     "drivers": [f"{d['activity']}: {d['status']} ({'; '.join(o for o in d['would_make_feasible'][:1])})"
                                 for d in prog["drivers"]]})
    return {"baseline": base, "scenarios": out, "comparison": rows}


def stage_planner(r: dict, stage: str | None = None, extended: bool = True):
    """make_plan(assumptions) for run_scenarios from a stage2.run result `r`: plans `stage` (default: the validated
    stage) the way stage2.a5_all does (planning date = the stage's issue date; anchor = its PDD, whose time, timezone
    and source come from r["anchor_details"][stage], the effective text of its defining unit). When the
    assumptions give another calendar or counting policy, the register's dates are re-evaluated with it, so a
    declared holiday also moves pack dates counted in Working Days (e.g. the clarification cut-off). A gate that
    names an issue missing from the open-issue register is flagged on its activity (decided and removed, or a typo):
    the gate stays until a person removes it from the templates. Activities a curated relationship reaches at the
    stage are marked REVIEW (<class>) with their dates unchanged (r["relationship_impact"], session 10)."""
    from .register import Register
    stage = stage or r["validated"].stage
    s = next(x for x in r["stages"] if x.stage == stage)
    status_date = date.fromisoformat(s.issued)
    cache: dict = {}
    open_issues = set(r.get("curated_issues") or {})

    def make_plan(a: dict) -> dict:
        notified = (r.get("non_working_days") or {}).get(stage) or []
        cal = calendar_from_config(a.get("calendar")).with_days(notified)
        policy = (a.get("planning") or {}).get("counting_policy", "conservative")
        if cal == r["register"].cal_by_stage[stage] and policy == r["policy"]:
            evals = r["evals"]
        else:
            if (cal, policy) not in cache:
                cache[(cal, policy)] = Register(r["rowfile"], r["stages"], cal, policy).all()
            evals = cache[(cal, policy)]
        pdd = next((d["anchor_value"] for e in evals for d in e["stages"][stage]["dates"] if d["anchor"] == "PDD"), None)
        prog = plan(stage, evals, r["templates"], a, cal, status_date, {"PDD": pdd}, evidence_items=r["evidence_items"],
                    anchor_details=(r.get("anchor_details") or {}).get(stage), notified_days=notified,
                    reached=((r.get("relationship_impact") or {}).get(stage) or {}).get("records"),
                    questions=gate_questions(r), question_units=question_units(r))
        # session 12 (blind-06 follow-up 5): a milestone planned from a relative date rule carries the `computed_from`
        # of the same calc.deadline inputs derived.computed_deadlines records (one function: derived.compute_deadline)
        from . import derived
        anchors = r["register"].rf.anchors
        issued_from = {f"{x.stage}-issue": getattr(x, "issued_from", None) for x in r["stages"]}
        rules_by_id = {rd.rule_id: rd for row in r["rowfile"].rows for rd in row.date_rules if rd.kind == "relative"}
        for m in prog.get("milestones") or []:
            rd = rules_by_id.get(m["id"])
            if rd is None or not m.get("date"):
                continue
            av = next((d["anchor_value"] for e in evals for d in (e["stages"].get(stage) or {}).get("dates") or []
                       if d["rule_id"] == m["id"] and d.get("anchor_value")), None)
            src = (anchors.get(rd.anchor) or {}).get("defined_in") or issued_from.get(rd.anchor)
            cf = derived.rule_computed_from(rd, av, src, cal, anchors) if av else None
            if cf:
                m["computed_from"] = cf
        for act in prog["activities"]:
            for i in act.get("gated_by") or []:
                if i not in open_issues:
                    act["flags"].append(f"GATE ISSUE NOT IN THE REGISTER ({i}: decided and removed, or a typo; the gate "
                                        "stays until a person removes it from curation/activity_templates.yaml)")
        attach_open_decisions(prog, r, a)          # session 13 (F2; audit R2-2, R3-1)
        return extend(prog, r["evidence_items"], a, cal) if extended else prog

    return make_plan


# ---------------------------------------------------------------------------------------------- open decisions (s13)
# Session 13 (F2; audit R2-2 A5 part, R3-1): an activity shows the open human-owned issues of the rows it carries (a
# row's own issues and those of the curated relationships that reach it, as the register renders them; an issue counts
# when human_owned.pending_reasons says it is a person's decision not yet recorded: r["pending_issues"]), as a readable
# note (`open_decisions`, a flag 'OPEN DECISION ...', the README and the Gantt). Whether such an issue holds the
# activity's finalisation is a judgment for the owner, so it is ONE named rule, off unless the assumptions turn it on:
OPEN_DECISION_RULE = "planning.gate_on_open_decisions"
OPEN_DECISION_FLAG = "OPEN DECISION, HUMAN DECISION PENDING (an issue of the rows it carries; no decision recorded)"


def gate_on_open_decisions(assumptions: dict | None) -> bool:
    """OPEN_DECISION_RULE: true makes an activity with an open decision 'REVIEW (open decision)' instead of READY.
    Default false: A5 keeps READY (preparation and finalisation are not held) and shows the note."""
    return bool(((assumptions or {}).get("planning") or {}).get("gate_on_open_decisions", False))


def row_open_issues(r: dict) -> dict[str, list[str]]:
    """Row id -> the issues it carries: its own `issues`, those of every curated relationship whose `to` names it
    (relationships.yaml `issues:`) and those of a reissued form's dropped field. Session 13 (F4; audit R1-7): the ONE
    set A1's Issues cell and A2's pending list read (stage2.row_issues). Ordered, without repeats."""
    from .stage2 import row_issues
    return row_issues(r)


_LABEL_RX = re.compile(r"^" + re.escape("HUMAN DECISION PENDING") + r"(?: \([^()]*\))?: ")


def open_decision_index(r: dict) -> dict[str, dict]:
    """Issue id -> {short, owner} for the issues that are a person's decision not yet recorded (r["pending_issues"]):
    the curated `a3` wording, else `short`, else the text's first sentence."""
    cur = r.get("curated_issues") or {}
    out = {}
    for iid in r.get("pending_issues") or {}:
        it = cur.get(iid) or {}
        t = str(it.get("a3") or it.get("short") or str(it.get("text") or "").split(". ")[0])
        out[iid] = {"short": _LABEL_RX.sub("", t), "owner": str(it.get("decision_owner") or it.get("owner") or ""),
                    # session 13 (F4; audit R3 recheck R3-1): the curated `short` words, for the Gantt's notes line
                    "brief": _LABEL_RX.sub("", str(it.get("short") or t))}
    return out


NO_QUESTION_BASIS = "by the activity's start (no question drafted)"
ASK_BY_BASIS = ("the clarification cut-off route's ask-by: whether to ask the Authority is settled before the cut-off "
                "(VOL-I 5.2, moved by ADD-01 2.2)")


def open_decision_date(a: dict, ids: list[str], questions: dict | None, route_ask_by: str | None) -> tuple:
    """Session 13 (F4; audit R2 recheck note, R3 recheck N-2): (date, basis) by which a person must decide the open
    decisions of an activity that no gate holds: the earlier of the clarification route's ask-by (the activity's
    `ask_by`, else `route_ask_by`: whether to ask the Authority must be settled before the cut-off; after it only an
    internal decision remains) and the activity's own latest start. The basis names the questions drafted on those
    issues (`questions`: issue -> question ids, gate_questions), or says none is ('by the activity's start (no question
    drafted)'). (None, None) without a date."""
    if not ids:
        return None, None
    ask, ls = a.get("ask_by") or route_ask_by, a.get("latest_start")
    qs = list(dict.fromkeys(q for i in ids for q in (questions or {}).get(i) or []))
    drafted = f"questions drafted: {', '.join(qs)}" if qs else "no question drafted"
    if ask and (not ls or str(ask) <= str(ls)):
        return str(ask), f"{ASK_BY_BASIS} ({drafted})"
    if ls:
        return str(ls), (NO_QUESTION_BASIS if not qs else
                         f"by the activity's start ({drafted}; their ask-by {ask} is later)" if ask else
                         f"by the activity's start ({drafted})")
    return None, None


def open_decision_reach(acts: list[dict], by_row: dict[str, list[str]], pending: dict, route: str | None = None) -> dict:
    """Session 13 (F4; audit R3 recheck N-1): issue id -> the activities whose own work the open decision bears on, by
    session 12's rule for questions (schedule.question_reach): the issue's rows that an activity carries; the
    deliverables (evidence items) shared by the activities carrying each of those rows (the intersection over the rows;
    the union when they share none), so a generic row (Volume IV's cover note on every form, VOL-I 9.3 on the Power of
    Attorney too) does not spread it; an activity is reached when it carries one of the rows and produces one of those
    deliverables. The clarification route activity (`route`) is left out of the computation: it lists every open
    decision once (inherit_open_decisions)."""
    carriers: dict[str, set[str]] = {}
    ev: dict[str, set[str]] = {}
    for a in acts:
        if a["id"] == route:
            continue
        ev[a["id"]] = set(a.get("evidence_items") or [a.get("evidence")]) - {None, ""}
        for rid in a.get("req_ids") or []:
            carriers.setdefault(rid, set()).add(a["id"])
    out: dict[str, set[str]] = {}
    for i in pending or {}:
        rows = [k for k, ids in (by_row or {}).items() if i in ids and k in carriers]
        sets = [set().union(*(ev[x] for x in carriers[k])) for k in rows]
        deliv = set.intersection(*sets) if sets else set()
        deliv = deliv or (set().union(*sets) if sets else set())
        out[i] = {aid for k in rows for aid in carriers[k] if ev[aid] & deliv}
    return out


def inherit_open_decisions(acts: list[dict], by_row: dict[str, list[str]], pending: dict[str, dict],
                           gate: bool = False, questions: dict | None = None, route_ask_by: str | None = None,
                           reach: dict | None = None, route: str | None = None) -> None:
    """Put on every activity the open decisions of the rows it carries (`open_decisions`: issue ids; one flag
    OPEN_DECISION_FLAG naming each with its wording, owner and rows). With `gate` (OPEN_DECISION_RULE on), a READY
    activity becomes 'REVIEW (open decision): ...'; a GATED one keeps its gate. In place."""
    carried = {rid for x in acts for rid in x.get("req_ids") or []}
    for a in acts:
        rows: dict[str, list[str]] = {}
        # session 13 (F4; audit R3 recheck N-1): with `reach` (open_decision_reach), an activity inherits an issue only
        # where the issue bears on its own work; the clarification route activity (`route`) lists every open decision
        # of the rows in force once
        mine = sorted(carried) if a["id"] == route else a.get("req_ids") or []
        for rid in mine:
            for i in by_row.get(rid) or []:
                if i in pending and (reach is None or a["id"] == route or a["id"] in (reach.get(i) or ())):
                    rows.setdefault(i, []).append(rid)
        a["open_decisions"] = list(rows)
        a["open_decision_words"] = {i: f"{pending[i].get('short') or i} ({pending[i].get('owner') or 'owner not named'})"
                                    for i in rows}
        a["flags"] = [f for f in a.get("flags") or [] if not f.startswith(OPEN_DECISION_FLAG)]
        if not a.get("gated_by"):                # a gate's own date stays (schedule.plan); else the open decisions'
            a["decision_needed_by"], a["decision_needed_by_basis"] = open_decision_date(a, list(rows), questions,
                                                                                       route_ask_by)
        if not rows:
            continue
        a["flags"].append(OPEN_DECISION_FLAG + ": " + "; ".join(
            f"{i}: {pending[i].get('short') or i} ({pending[i].get('owner') or 'owner not named'}; rows "
            + ", ".join(rs[:3]) + (f" +{len(rs) - 3} more" if len(rs) > 3 else "") + ")" for i, rs in rows.items()))
        if gate and str(a.get("decision_status") or "READY") == "READY":
            a["decision_status"] = (f"REVIEW (open decision): finalisation waits on a person's decision on "
                                    f"{', '.join(rows)} ({OPEN_DECISION_RULE} is on)")


def attach_open_decisions(prog: dict, r: dict, assumptions: dict | None = None) -> dict:
    """inherit_open_decisions over a planned programme from a stage2.run result (the one rule A5, its stages and the
    scenarios use)."""
    acts, by_row, pending = prog.get("activities") or [], row_open_issues(r), open_decision_index(r)
    route = (prog.get("gate_route") or {}).get("activity")
    prog["open_decision_index"] = pending              # session 13 (F4): the words the Gantt's notes print
    gate = gate_on_open_decisions(assumptions if assumptions is not None else r.get("assumptions"))
    inherit_open_decisions(acts, by_row, pending, gate,
                           gate_questions(r), (prog.get("gate_route") or {}).get("ask_by"),
                           open_decision_reach(acts, by_row, pending, route), route)
    attach_readiness(prog, gate)                       # session 14 (W4): preparation apart from finalisation
    try:                                               # session 14 (W4): Form 4-E against the whole Proposal
        prog["form_4e_checks"] = form_4e_checks_for(r, prog)
    except (KeyError, ValueError, TypeError) as exc:   # a pack without the Form 4-E step or the envelope chain
        prog["form_4e_checks"] = {"activity": None, "checks": [], "what_if": {}, "findings": [],
                                  "error": f"not computed: {exc}"}
    return prog


# ---------------------------------------------------------------------------------------------- readiness (session 14)
# Session 14 (W4; part 4, report section 9 G7): an activity can be PREPARED (its inputs are known: its predecessors and
# its earliest start; its work can start) while its FINALISATION needs a person's decision that is not recorded. The two
# are stated apart on every activity (`preparation`, `finalisation`: programme.csv/json, gantt.html, the Gantt's amber
# tick, the review cards of the rows it carries). Nothing is approved here; whether an open decision holds the
# finalisation stays the owner's pending choice (OPEN_DECISION_RULE, off by default); durations are not touched.
NOT_SCHEDULED_TIMING = ("CONDITIONAL", "DEADLINE PASSED", "NOT NEEDED")


def readiness(a: dict, gate: bool = False) -> tuple[str, str]:
    """(preparation, finalisation) of one planned activity (see above)."""
    st = str(a.get("status") or a.get("timing_status") or "OK")
    preds = list(a.get("predecessors") or [])
    if st.startswith(NOT_SCHEDULED_TIMING):
        prep = f"NOT SCHEDULED ({st})"
    else:
        prep = (f"PREPARATION READY: can start {a.get('earliest_start')} "
                + (f"(after {', '.join(preds)})" if preds else "(inputs known; no predecessor)")
                + (f"; timing {st}" if st != "OK" else ""))
    by = a.get("decision_needed_by") or a.get("finalise_by") or a.get("latest_start")
    if a.get("gated_by"):
        fin = (f"FINALISATION GATED: needs a person's decision on {', '.join(a['gated_by'])} by {by}; no decision "
               "recorded (preparation continues)")
    elif a.get("open_decisions"):
        words = a.get("open_decision_words") or {}
        fin = ("FINALISATION NEEDS A DECISION: " + "; ".join(f"{i}: {words.get(i, i)}" for i in a["open_decisions"])
               + f" by {by} (HUMAN DECISION PENDING; no decision recorded; "
               + (f"{OPEN_DECISION_RULE} is on: held" if gate else
                  f"not a gate while {OPEN_DECISION_RULE} is off, the owner's pending choice") + ")")
    else:
        fin = "FINALISATION: no pending decision on the rows it carries"
    return prep, fin


def attach_readiness(prog: dict, gate: bool = False) -> None:
    """readiness() on every activity, in place."""
    for a in prog.get("activities") or []:
        a["preparation"], a["finalisation"] = readiness(a, gate)


def readiness_by_row(prog: dict | None) -> dict[str, list[str]]:
    """Row id -> '<activity>: <preparation>; <finalisation>' for every activity that carries the row (the review cards)."""
    out: dict[str, list[str]] = {}
    for a in (prog or {}).get("activities") or []:
        if not a.get("preparation"):
            continue
        for rid in a.get("req_ids") or []:
            out.setdefault(rid, []).append(f"{a['id']}: {a['preparation']}; {a['finalisation']}")
    return out


# ---------------------------------------------------------------------------------------------- Form 4-E (session 14)
# Session 14 (W4; the owner's part 4): VOL-I 9.6 "A Proposal that states 'no deviations' in Form 4-E while containing
# a qualification elsewhere in the Proposal shall be treated as non-responsive." Form 4-E is checked against EVERY
# document of the Proposal, not against Volume V and the Technical Proposal only: the documents placed in Envelope A or
# B (the direct inputs of the envelope assembly steps, ENVELOPE_ASSEMBLY), each with the clause that places it in the
# Proposal. A document final only after Form 4-E starts cannot be cross-checked; the what-if that makes Form 4-E wait for
# every document is computed on the same network, durations unchanged, and its feasibility is reported for a person.
FORM_4E_ACTIVITY = "form-4e"
ENVELOPE_ASSEMBLY = ("assemble-envelope-a", "assemble-envelope-b")
RULE_9_6 = "VOL-I 9.6"


def _ancestors(acts: dict, aid: str) -> set[str]:
    out, todo = set(), list((acts.get(aid) or {}).get("predecessors") or [])
    while todo:
        p = todo.pop()
        if p not in out and p in acts:
            out.add(p)
            todo += list(acts[p].get("predecessors") or [])
    return out


def form_4e_checks(prog: dict, cal: Calendar, clause_of, issues_of, activity: str = FORM_4E_ACTIVITY,
                   rule_words: str = "") -> dict:
    """{activity, rule, checks, what_if, findings} (see above). `clause_of(activity) -> str` names the clause that
    places the activity's document in the Proposal; `issues_of(activity) -> [issue ids]` the open issues of the rows it
    carries. Pure; nothing is planned differently and nothing is decided."""
    acts = {a["id"]: a for a in prog.get("activities") or []}
    f = acts.get(activity)
    if f is None:
        return {"activity": None, "rule": RULE_9_6, "checks": [], "what_if": {}, "findings": []}
    before = _ancestors(acts, activity)
    docs = []
    for asm in ENVELOPE_ASSEMBLY:
        for p in (acts.get(asm) or {}).get("predecessors") or []:
            if p != activity and p not in docs and str((acts.get(p) or {}).get("envelope") or "") in ("A", "B"):
                docs.append(p)
    rule = f"{RULE_9_6}" + (f" ('{rule_words}')" if rule_words else "")
    checks = []
    for d in docs:
        a = acts[d]
        ef, es = a.get("earliest_finish"), f.get("earliest_start")
        if d in before:
            st = "checked (finalised before Form 4-E)"
        elif ef and es and str(ef) < str(es):
            st = (f"final on {ef}, before Form 4-E starts on {es}, but not linked: a later change to it would not "
                  "reach Form 4-E")
        else:
            st = f"NOT CHECKABLE: final on {ef}, after Form 4-E starts on {es}"
        checks.append({"document_activity": d, "document": a.get("item") or a.get("name"), "envelope": a.get("envelope"),
                       "finish": ef, "status": st, "clause": f"{rule}; {clause_of(a)}",
                       "open_issues": list(issues_of(a) or [])})
    missing = [c["document_activity"] for c in checks if not c["status"].startswith("checked")]
    what_if: dict = {"added_predecessors": missing}
    if missing:
        g = _graph(prog)
        h = {k: dict(v, predecessors=list(v["predecessors"])) for k, v in g.items()}
        h[activity]["predecessors"] = list(dict.fromkeys(h[activity]["predecessors"] + missing))
        start = _d(prog.get("planning_date") or prog.get("status_date"))
        try:
            base, alt = network(g, cal, start), network(h, cal, start)
        except ValueError as exc:
            what_if.update(error=f"the links would make a cycle ({exc})", feasible=None)
        else:
            t = alt[activity]
            worse = sorted(k for k in alt if alt[k]["float_wd"] is not None and alt[k]["float_wd"] < 0
                           and (base[k]["float_wd"] is None or alt[k]["float_wd"] < base[k]["float_wd"]))
            what_if.update(form_4e_earliest_start=t["es"].isoformat(), form_4e_earliest_finish=t["ef"].isoformat(),
                           form_4e_latest_finish=t["lf"].isoformat() if t["lf"] else None,
                           float_wd=t["float_wd"], made_worse=worse, feasible=not worse,
                           shortfall_wd=max([0] + [-alt[k]["float_wd"] for k in worse]))
    findings = []
    late = [c for c in checks if c["status"].startswith("NOT CHECKABLE")]
    if late:
        wi = what_if
        how = ("the links would make a cycle" if wi.get("error") else
               f"it would finish on {wi.get('form_4e_earliest_finish')} against its latest finish "
               f"{wi.get('form_4e_latest_finish')}: " + ("feasible on the assumed durations" if wi.get("feasible") else
                                                         f"INFEASIBLE by {wi.get('shortfall_wd')} WD on the assumed "
                                                         f"durations ({', '.join(wi.get('made_worse') or [])} made late)"))
        findings.append(f"Form 4-E ({activity}) is finalised before {len(late)} Proposal document(s) are final ("
                        + ", ".join(c["document_activity"] for c in late) + f"), so a qualification in them cannot be "
                        f"checked against its declaration ({rule}). If Form 4-E waited for all of them, {how}. How "
                        "the cross-check is done (a later final read of every document, a different order, or a "
                        "change of a lead time) is for a person (Legal, Bid manager); no duration, setting or "
                        "dependency was changed.")
    return {"activity": activity, "rule": rule, "checks": checks, "what_if": what_if, "findings": findings}


_STOP = {"the", "of", "and", "for", "each", "per", "or", "a", "an", "in", "to", "on", "by", "with", "form", "its",
         "one", "shall", "be", "vol-i", "sar"}


def _tokens(t: str) -> set[str]:
    return {w.lower() for w in re.findall(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*", str(t or "")) if w.lower() not in _STOP
            and len(w) > 1}


def proposal_clause(name: str, envelope: str, state: dict) -> str:
    """The clause that places a document in the Proposal: for Envelope A the item of VOL-I 9.1 (as amended: an item an
    addendum inserted counts) sharing most words with the document's name (two words at least, or a form number),
    else 9.1(i) (certificates and evidence); for Envelope B the clause of VOL-I 10 chosen the same way, else 10.1.
    '<unit> ('<words>')'."""
    pre, fallback = ("VOL-I:9.1(", "VOL-I:9.1(i)") if envelope == "A" else ("VOL-I:10.", "VOL-I:10.1")
    cands = [(k, getattr(u, "text", "") or "") for k, u in state.items()
             if k.startswith(pre) and getattr(u, "status", "active") == "active"]
    mine = _tokens(name)
    best = max(cands, key=lambda kv: (len(mine & _tokens(kv[1])), -cands.index(kv)), default=None)
    shared = (mine & _tokens(best[1])) if best else set()
    # two shared words, or a form number ('4-g'), name the item; one ordinary word is not enough
    if best is None or not (len(shared) >= 2 or any(re.fullmatch(r"\d+-[a-z]", w) for w in shared)):
        best = (fallback, getattr(state.get(fallback), "text", "") or "")
    k, t = best
    return f"{k.replace(':', ' ', 1)} ('{' '.join(t.split())[:140]}')"


def form_4e_checks_for(r: dict, prog: dict) -> dict:
    """form_4e_checks on a stage's programme from a stage2.run result: the clauses from the stage's effective units,
    the open issues of the rows each activity carries (row_open_issues; those not decided), and, from the same
    effective units, the commercial-qualification tension (VOL-I 9.6 with 6.2 and 10.5) as a finding for a person."""
    st = next((s.state for s in r["stages"] if s.stage == prog.get("stage")), r["validated"].state)
    ev = r.get("evidence_items") or {}
    by_row = row_open_issues(r)
    from .human_owned import decision
    decided = {i for i, it in (r.get("curated_issues") or {}).items() if decision(r.get("decisions"), "issue", i, it)}
    name = lambda a: getattr(ev.get(a.get("evidence")), "name", None) or a.get("item") or a.get("name")  # noqa: E731
    issues_of = lambda a: [i for i in dict.fromkeys(i for rid in a.get("req_ids") or []  # noqa: E731
                                                     for i in by_row.get(rid) or []) if i not in decided]
    words = lambda uid, rx: next((x.strip() for x in re.split(r"(?<=\.)\s+", " ".join(  # noqa: E731
        (getattr(st.get(uid), "text", "") or "").split())) if re.search(rx, x, re.I)), "")
    w96 = words("VOL-I:9.6", r"elsewhere in the Proposal")
    cal = (r["register"].cal_by_stage.get(prog.get("stage"))
           or calendar_from_config((r.get("assumptions") or {}).get("calendar")))
    res = form_4e_checks(prog, cal, lambda a: proposal_clause(name(a), str(a.get("envelope") or ""), st), issues_of,
                         rule_words=w96)
    w62, w105 = words("VOL-I:6.2", r"commercial information"), words("VOL-I:10.5", r"conditional price")
    if w96 and w62 and w105 and any(c["envelope"] == "B" for c in res["checks"]):
        res["findings"].append(
            "A qualification of a commercial term of Volume V would have to be listed in Form 4-E (VOL-I 9.6: "
            f"'{w96}'), which is placed in Envelope A (VOL-I 9.1(e)), where commercial information renders the Proposal "
            f"non-responsive (VOL-I 6.2: '{w62}'); stated in Envelope B instead, it would be a conditional price "
            f"(VOL-I 10.5: '{w105}'). Whether such a qualification can be made at all, and how Form 4-E words a "
            "deviation from a commercial term without commercial information, is for a person (Legal and "
            "Commercial); nothing is decided here.")
    return res


def question_units(r: dict) -> dict[str, list[str]]:
    """Question id -> its own units (the clarification register's `units`, else the units its sources quote), for the
    open questions (session 12, F5; audit A5 N2: schedule.question_reach)."""
    from .human_owned import clarification_closed
    return {str(c.get("id")): list(c.get("units") or [x.get("unit") for x in c.get("sources") or [] if x.get("unit")])
            for c in (r.get("clarifications") or {}).get("clarifications") or []
            if not clarification_closed(c, r.get("decisions"))}


def gate_questions(r: dict) -> dict[str, list[str]]:
    """Open issue -> the ids of the clarification questions drafted on it (the clarification register's
    `linked_issues`; a question answered or withdrawn no longer counts). Session 11, audit A5-1. Session 12: it no
    longer counts only when a person's decision is bound to that status (human_owned.clarification_closed); a status a
    proposal or a hand edit set, or an answer the workflow recorded, keeps the question open."""
    from .human_owned import clarification_closed
    out: dict[str, list[str]] = {}
    for c in (r.get("clarifications") or {}).get("clarifications") or []:
        if clarification_closed(c, r.get("decisions")):
            continue
        for i in c.get("linked_issues") or []:
            out.setdefault(i, []).append(str(c.get("id")))
    return {k: sorted(set(v)) for k, v in sorted(out.items())}


def answers_by_row(r: dict, stage: str) -> dict[str, list[dict]]:
    """Row -> the annotations applied at `stage` (not at the stage before) to the units it cites, each {op, type, effect,
    provision, answer, class, why}: a clarification answer (an 'Authority response:' or a Q-numbered provision) is read by
    summary.classify_answer against the words of the units it annotates at the stage before; any other op is listed
    with answer False (its effect as class). For schedule.deltas(answers=...): a confirming answer never makes a
    requirement change (session 11, audit A5-4)."""
    import re
    from .summary import answer_targets, classify_answer
    order = list(r["order"])
    if stage not in order or order.index(stage) == 0:
        return {}
    by = {s.stage: s for s in r["stages"]}
    st, prev = by[stage].state, by[order[order.index(stage) - 1]].state
    texts = {u["unit_id"]: u.get("text") or "" for u in r.get("units") or []}
    cache: dict[str, dict] = {}
    out: dict[str, list[dict]] = {}
    for e in r["evals"]:
        ev = e["stages"].get(stage) or {}
        uids = list(dict.fromkeys(list(e["row"].units) + [u.get("effective_unit") for u in ev.get("units_detail") or []
                                                          if u.get("effective_unit")]))
        recs = []
        for uid in uids:
            old = set(prev[uid].annotations) if uid in prev else set()
            for oid in (st[uid].annotations if uid in st else []):
                if oid in old or any(x["op"] == oid for x in recs):
                    continue
                if oid not in cache:
                    x = r["register"]._op_by_id(oid)
                    op = x.op if x is not None else None
                    text = (st[op.provision].text if op is not None and op.provision in st else
                            texts.get(getattr(op, "provision", ""), ""))
                    # session 12: every record says what the op is (type, effect, provision) for signals.confirming
                    kind = {"type": getattr(op, "type", None), "effect": getattr(op, "effect", None),
                            "provision": getattr(op, "provision", None),
                            # session 13 (F4; audit R1-7, R1-8): an issue the op's note names is context for the
                            # op (the rows an issue bears on are its own links: signals.attach_pending); the op is
                            # named as awaiting a person's acceptance until one is bound to it (signals.chain_label)
                            "accepted": ((r.get("reviews") or {}).get(("op", oid)) or {}).get("status") == "accepted"}
                    if op is not None and (re.search(r":Q\d+$", op.provision) or "Authority response:" in text):
                        c = classify_answer(text, answer_targets(prev, [t for t in op.targets if t != op.provision]))
                        cache[oid] = {"op": oid, "answer": True, "class": c["class"], "why": c["why"], **kind}
                    else:
                        cache[oid] = {"op": oid, "answer": False, "class": str(getattr(op, "effect", "") or ""), "why": "",
                                      **kind}
                recs.append(cache[oid])
        if recs:
            out[e["row"].id] = recs
    return out


# ---------------------------------------------------------------------------------------------- write

PROGRAMME_COLS = ("id", "name", "discipline", "evidence", "envelope", "req_ids", "owner", "resource", "issuer", "count",
                  "multiplicity", "duration_wd", "duration_assumption", "duration_basis", "effort_wd", "effort_total_wd",
                  "effort_basis", "waiting_on", "work_type", "predecessors", "earliest_start", "earliest_finish",
                  "es_driven_by", "latest_start", "latest_finish", "driven_by", "float_wd", "deadline", "timing_status",
                  "decision_status",
                  "preparation", "finalisation",     # session 14 (W4): preparation readiness apart from finalisation
                  "gated_by", "decision_needed_by", "decision_needed_by_basis", "clarification_questions",
                  "ask_by", "finalise_by",
                  "condition", "resource_status", "status", "flags")
MARSHALLING_COLS = ("evidence", "item", "name", "kind", "envelope", "issuer", "per", "count", "count_basis",
                    "marked_originals", "hard_copies", "physical_count", "electronic_copy", "activity", "activities",
                    "lead_time_wd", "lead_time_chain", "lead_time_keys", "lead_time_basis", "waiting_on",
                    "drop_dead_start", "needed_by", "earliest_finish", "float_wd", "timing_status", "decision_status",
                    "clarification_questions", "ask_by", "resource_status", "status", "owner", "resource", "req_ids",
                    "flags")
# session 12 (audit A5-4): every A1 row in force that no activity carries, with the reason A1 (or the templates) holds
NOT_CARRIED_COLS = ("row", "status", "assessment", "discipline", "a3", "reason", "source")
FORM_4E_COLS = ("document_activity", "document", "envelope", "finish", "status", "clause", "open_issues")  # session 14
DOCUMENT_COLS = ("evidence", "name", "envelope", "kind", "issuer", "per", "multiplicity", "multiplicity_basis",
                 "marked_originals", "hard_copies", "physical_count", "electronic_copy", "usb", "req_ids",
                 "activities", "source", "flags")
RESOURCE_COLS = ("resource", "date", "iso_week", "load_wd", "capacity", "status", "activities", "capacity_basis",
                 "capacity_owner")
OVERLOAD_COLS = ("resource", "from", "to", "days", "dates", "peak_load", "capacity", "activities")
DISCIPLINE_COLS = ("discipline", "activities", "staff_effort_wd", "elapsed_wd", "waiting_activities", "external_parties",
                   "roles", "gated", "infeasible", "overloaded", "activity_ids")
MILESTONE_COLS = ("id", "date", "time", "short", "label", "kind", "purpose", "conditional", "derived", "reading",
                  "readings_differ", "other_readings", "source", "words", "rows", "activities")
DRIVER_COLS = ("activity", "status", "shortfall_wd", "float_wd", "earliest_start", "latest_start", "latest_finish",
               "status_date", "deadline", "forward_chain", "chain", "lead_time_values", "would_make_feasible", "resource",
               "req_ids")
SCENARIO_COLS = ("id", "name", "resource", "duration_assumption", "duration_wd_base", "duration_wd", "count_base", "count",
                 "earliest_start_base", "earliest_start", "latest_start_base", "latest_start", "latest_finish_base",
                 "latest_finish", "float_wd_base", "float_wd", "shift_wd", "status_base", "status", "change")
COMPARISON_COLS = ("scenario", "purpose", "hypothetical", "overrides", "activities_moved", "latest_start_shift_wd",
                   "status_changes", "infeasible_base", "infeasible", "deadline_passed_base", "deadline_passed",
                   "physical_A_base", "physical_A", "physical_B_base", "physical_B", "document_changes",
                   "overloads_base", "overloads", "resource_changes", "drivers")


def discipline_map(templates: dict) -> dict[str, list[str]]:
    """A5 discipline -> the A1 disciplines whose rows it plans (the templates' `_discipline_map`, session 12, audit A5-8);
    an A5 discipline that is also an A1 discipline maps to itself and is not listed."""
    return {k: list(v) for k, v in (templates.get("_discipline_map") or {}).items()}


def carried_words(cov: dict) -> str:
    """'160 discharged by an activity, 30 reviewed for deviations (the VOL-V volume check)' (session 12, F5; audit A5
    N3: 'carried' mixed rows discharged with rows only reviewed under a volume check); the older form without the
    split."""
    if "discharged" not in cov:
        return f"{len(cov.get('carried') or {})} carried by the A5 programme"
    vols = ", ".join(cov.get("volumes") or [])
    how = f"(the {vols} volume check)" if vols else "(no volume check applies at this stage)"   # session 12: never "the a volume check"
    return (f"{len(cov.get('discharged') or {})} discharged by an activity, {len(cov.get('reviewed') or {})} reviewed "
            f"for deviations {how}")


COVERAGE_COLS = ("row", "carried_how", "activities", "reason")


def coverage_rows(p: dict) -> list[dict]:
    """One line per A1 row in force (requirements_coverage.csv): how it is carried: discharged, reviewed for deviations
    (a volume check only), excepted (with the reason) or NOT CARRIED."""
    cov = p.get("row_coverage") or {}
    out = []
    for k in cov.get("rows") or []:
        if k in (cov.get("discharged") or {}):
            out.append({"row": k, "carried_how": "discharged", "activities": cov["discharged"][k], "reason": ""})
        elif k in (cov.get("reviewed") or {}):
            out.append({"row": k, "carried_how": "reviewed for deviations", "activities": cov["reviewed"][k],
                        "reason": f"only checked under the {', '.join(cov.get('volumes') or [])} volume check"})
        elif k in (cov.get("excepted") or {}):
            out.append({"row": k, "carried_how": "excepted", "activities": [], "reason": cov["excepted"][k]["reason"]})
        else:
            out.append({"row": k, "carried_how": "NOT CARRIED", "activities": [], "reason": "no reason given (C48)"})
    return out


def not_carried(p: dict) -> list[dict]:
    """The rows of `row_coverage` that no activity carries: excepted (with the reason) or NOT CARRIED (no reason)."""
    cov = p.get("row_coverage") or {}
    out = [{"row": k, **{c: v.get(c) for c in NOT_CARRIED_COLS if c != "row"}} for k, v in (cov.get("excepted") or {}).items()]
    out += [{"row": k, "reason": "NOT CARRIED and no reason given (C48)", "source": ""} for k in cov.get("uncarried") or []]
    return sorted(out, key=lambda x: x["row"])


def coverage_check(p: dict) -> dict:
    """C48 (reported): every A1 row in force at the programme's stage is carried by an activity or excepted with a reason
    (session 12, audit A5-4; session 11 counted the A3 rows only, still shown)."""
    cov, a3 = p.get("row_coverage") or {}, p.get("a3_coverage") or {}
    unc = list(cov.get("uncarried") or []) + [k for k in a3.get("uncarried") or [] if k not in (cov.get("uncarried") or [])]
    # session 13 (F2, after F3; audit R3-5/R2-9): the A3 rows by id (schedule.a3_rows: the page's own set), so the
    # count in a5/requirements_*.json and checks.json is checkable against the page's lines
    return {"id": "C48", "ok": not unc,
            "detail": f"{len(cov.get('rows') or [])} A1 rows in force at {p.get('stage')}: {carried_words(cov)}, "
                      f"{len(cov.get('excepted') or {})} excepted with a reason (listed in "
                      f"a5/requirements_not_carried.csv); not carried: {', '.join(unc) or 'none'}. Of these, "
                      f"{len(a3.get('rows') or [])} A3 (bid-out) rows: {len(a3.get('carried') or {})} carried, "
                      f"{len(a3.get('excepted') or {})} excepted with a reason" + a3_members_note(a3)}


A3_BASIS = "the rows the A3 page lists: explicit plus the score row"


def a3_members_note(cov: dict) -> str:
    """The members of A5's A3 rows where C48 counts them (session 13, F3; audit R3-5; moved here by F2 so the C48 text of
    checks.json and of a5/requirements_*.json say the same): ' (the rows the A3 page lists: explicit plus the score
    row: <ids>)' (schedule.a3_rows, the page's own set); '' when none."""
    ids = list(cov.get("rows") or [])
    return f" ({A3_BASIS}: {', '.join(ids)})" if ids else ""


def _table(cols, rows, **extra) -> dict:
    return {"columns": [{"key": k, "header": k, "width": 20} for k in cols],
            "rows": [{k: r.get(k) for k in cols} for r in rows], "notice": NOTICE, **extra}


def _md(t) -> str:
    return str(t if t is not None else "").replace("|", "/").replace("\n", " ")


def readme(p: dict, scenarios_result: dict | None = None) -> str:
    """a5/README.md: what A5 is, how it is computed, and what is assumed (generated; nothing typed)."""
    asm = p.get("assumptions") or {}
    acts = p["activities"]
    L = [f"# A5 bid programme — {p['stage']} (PROPOSAL, not reviewed)", "",
         "Generated by `tenderpack outputs` from the A1 rows in force, curation/activity_templates.yaml and "
         "config/assumptions.yaml. Nothing here is typed by hand; edit the assumptions and rebuild.", "",
         "## Planning basis", "", p["planning_basis"], "",
         f"Pack milestones are kept at their legal dates (a deadline on a non-working day keeps its date; the work "
         f"finishes on the last Working Day before it):", ""]
    L += [f"- **{m['date']}{(' ' + m['time']) if m['time'] else ''}**"
          + (f" ({m.get('reading_policy') or 'planning'} reading; {_md(m['other_readings'])})" if m.get("other_readings") else "")
          + f" {_md(m['label'])} "
          f"({m['kind']}; {m['source'] or 'derived'}" + ("; CONDITIONAL" if m["conditional"] else "") + ")"
          for m in p.get("milestones", []) if m["date"]]
    undated = [m for m in p.get("milestones", []) if not m["date"]]
    if undated:
        L.append("- Event-dependent (no date until the event occurs; not planned; every reading in A1 Dates): "
                 + "; ".join(f"{m['id']} ({m['source']}: '{_md(m['words'])}')" for m in undated))
    L += ["", "## Method", "",
          "- Activities are derived from A1: every evidence item needed by a row in force expands into the activities of "
          "its template; each activity carries the A1 requirement ids it supports (`req_ids`, also on every marshalling "
          "line and every Gantt row). Dependencies come from the templates (shared by A5 and the Gantt).",
          "- **forward pass** (earliest start ES / earliest finish EF) from the first Working Day on or after the planning "
          "date; **backward pass** (latest start LS / latest finish LF) from the pack deadlines; Working Days are Sunday "
          "to Thursday less declared holidays (VOL-I 2.4).",
          "- **total float** = Working Days from ES to LS. Negative float = `INFEASIBLE by n WD`: never compressed; the "
          "same shortfall runs along the whole chain to the deadline (drivers.csv lists what would make it feasible).",
          f"- Resource load: {LOAD_WINDOW}. Capacity is staff per Working Day per role.",
          f"- **{NO_LEVELLING[0].upper() + NO_LEVELLING[1:]}.** No activity is moved to remove an overload.",
          "- Elapsed duration (`duration_wd`) is the scheduling value; `effort_wd` is the staff effort inside it per unit "
          "of the activity's multiplicity, and `waiting_on` names the external party whose time fills the rest. The Gantt "
          "draws external waiting (hatched) differently from staff effort (solid).", "",
          "## Three separate statuses", "",
          "- `timing_status` (= `status`): OK / INFEASIBLE by n WD / DEADLINE PASSED / NO WORKING WINDOW / NO DEADLINE "
          "REACHED / CONDITIONAL — window elapsed ... / NOT NEEDED (count 0).",
          "- `decision_status`: READY, or GATED: finalisation waits on an open issue; the decision is needed by `ask_by` "
          "(the clarifications activity's latest start) when a clarification question is drafted on the issue, else by "
          "the gated activity's latest start (`finalise_by`). Preparation is never gated.",
          "- `resource_status`: OK / OVERLOAD role on dates (peak load vs capacity) / NOT LOADED (why).", "",
          "A gated activity can be on time, and an infeasible one can be decision-ready: the three are read separately.",
          "", "## Decision gates (finalisation only; preparation continues)", ""]
    gated = [a for a in acts if a.get("gated_by")]
    by_id = {a["id"]: a for a in acts}
    for a in gated:
        preps = [x for x in a["predecessors"] if not by_id.get(x, {}).get("gated_by")]
        if a.get("ask_by"):                 # session 11 (audit A5-1): a drafted question gives the gate two dates
            L.append(f"- `{a['id']}` — finalisation waits on {', '.join(a['gated_by'])}; clarification question drafted: "
                     f"{', '.join(a.get('clarification_questions') or [])}. **Decide whether to ask the Authority by "
                     f"{a['ask_by']}**; **finalise by {a.get('finalise_by')}**. (timing: {a['status']}; preparation "
                     f"continuing: {', '.join(preps) or 'none'})")
        else:
            L.append(f"- `{a['id']}` — {a['decision_status']} (timing: {a['status']}; preparation continuing: "
                     f"{', '.join(preps) or 'none'})")
    if not gated:
        L.append("- none")
    gr = p.get("gate_route")
    if gr and any(a.get("ask_by") for a in gated):
        why = "; ".join(f"{_md(str(b['unit']).replace(':', ' '))}: '{_md(b['quote'])}' and '{_md(b['consequence'])}'"
                        for b in gr.get("basis") or [])
        L += ["", f"Why two dates: the route the pack gives for a conflict, ambiguity or discrepancy is a clarification "
                  f"request ({why or 'see the clarification rows'}). Requests close at the {gr['rule']} "
                  f"({_md(str(gr['source']).replace(':', ' '))}: '{_md(gr['words'])}') = {gr['cutoff']}; `{gr['activity']}` "
                  f"must finish by then, so its latest start, {gr['ask_by']}, is the last day to decide whether to ask. "
                  "The finalisation date is the gated activity's own latest start. A gate whose issue has no drafted "
                  "question keeps one date (its latest start)."]
    cov = p.get("a3_coverage")
    if cov is not None:                     # session 11 (audit A5-2)
        L += ["", f"## A3 rows carried by the programme ({len(cov['rows'])} A3 (bid-out) rows in force; "
                  f"{len(cov['carried'])} carried, {len(cov['excepted'])} excepted with a reason, "
                  f"{len(cov['uncarried'])} not carried)", "",
              f"Basis: {A3_BASIS} (schedule.a3_rows, one set for A3, A5 and the live diff).", ""]
        L += [f"- `{k}`: carried by {', '.join(v)}" + (" (through `_row_checks`: a check, not a deliverable)"
                                                        if k in cov.get("row_checks", {}) else "")
              for k, v in cov["carried"].items()]
        L += [f"- `{k}`: no step carries it: {_md(v)}" for k, v in cov["excepted"].items()]
        L += [f"- `{k}`: NOT CARRIED and no reason given (C48: add the step that checks it under `_row_checks`, or the "
              "reason under `_row_exceptions`, in curation/activity_templates.yaml)" for k in cov["uncarried"]]
    rc = p.get("row_coverage")
    if rc is not None:                      # session 12 (audit A5-4): every A1 row in force, not only A3's
        nc = not_carried(p)
        L += ["", "## Requirements not carried by an activity (with the reason)", "",
              f"{len(rc['rows'])} A1 rows in force at {p['stage']}: {carried_words(rc)}, "
              f"{len(rc['excepted'])} excepted with a reason, {len(rc['uncarried'])} not carried (no reason: C48). The "
              "reason is the one A1 holds (the row's no_deliverable, or its post-award assessment) or the templates' "
              "`_row_exceptions`. Also in requirements_not_carried.csv; how every row in force is carried "
              "(discharged, reviewed for deviations, excepted) is in requirements_coverage.csv.", "",
              "| Row | Status | Pass/fail or scored | Discipline (A1) | A3 | Reason | Where stated |", "|---|---|---|---|---|---|---|"]
        L += [f"| `{x['row']}` | {_md(x.get('status'))} | {_md(x.get('assessment'))} | {_md(x.get('discipline'))} | "
              f"{'yes' if x.get('a3') else ''} | {_md(x['reason'])} | {_md(x.get('source'))} |" for x in nc] or ["| none | | | | | | |"]
    dm = p.get("discipline_map")
    if dm is not None:                      # session 12 (audit A5-8)
        a1 = {}
        for a in acts:
            for d in a.get("a1_disciplines") or []:
                a1.setdefault(a.get("discipline"), set()).add(d)
        L += ["", "## Disciplines: A1 to A5", "",
              "A1's disciplines are the register's. A5 groups the work by the discipline that does it; where an A5 "
              "discipline is not an A1 one, it plans the rows of these A1 disciplines (curation/activity_templates.yaml "
              "`_discipline_map`, PROPOSED):", "", "| A5 discipline | A1 disciplines it plans | A1 disciplines of the rows "
              "its activities carry |", "|---|---|---|"]
        L += [f"| {d} | {', '.join(dm.get(d) or ([d] if d not in dm else [])) or '-'} | "
              f"{', '.join(sorted(a1.get(d) or [])) or '-'} |" for d in DISCIPLINES]
    fl = [(a, [f for f in a.get("flags") or [] if not f.startswith(BLOCKING_FLAGS + ("CONDITIONAL (only if",))])
          for a in acts]
    fl = [(a, f) for a, f in fl if f]
    L += ["", f"## Flags on activities ({len(fl)}; review, blocked, stale, clarification questions drafted; the dates are "
              "unchanged)", ""]
    if any(str(x).startswith("REVIEW (") for _, f in fl for x in f):     # session 12 (F5; audit R-e)
        from .relationships import STATUS_LEGEND
        L += [f"REVIEW (<status> ...): {STATUS_LEGEND}", ""]
    L += [f"- `{a['id']}`: " + " | ".join(_md(x) for x in f) for a, f in fl] or ["- none"]
    L += ["", "## Conditional obligations", ""]
    cond = [a for a in acts if a.get("condition")]
    for a in cond:
        L.append(f"- `{a['id']}`: needed only if {a['condition']}. Timing: **{a['status']}**. An elapsed window alone "
                 "does not establish a missed duty; a person records whether the condition arose.")
    if not cond:
        L.append("- none")
    # session 13 (F2; audit R2-2, R3-1): the open human-owned issues of the rows each activity carries, readable
    opened: dict[str, list[str]] = {}
    for a in acts:
        for i in a.get("open_decisions") or []:
            opened.setdefault(i, []).append(a["id"])
    if opened:
        words = {i: w for a in acts for i, w in (a.get("open_decision_words") or {}).items()}
        L += ["", "## Open decisions on the rows carried (HUMAN DECISION PENDING; no decision recorded)", "",
              "Shown on each activity (flag OPEN DECISION) and in the Gantt. Whether an open decision holds an activity is "
              f"a judgment for the owner: rule `{OPEN_DECISION_RULE}` in config/assumptions.yaml (now "
              f"{'on' if any(str(a.get('decision_status', '')).startswith('REVIEW (open decision)') for a in acts) else 'off'}"
              "; off: the activity stays READY; on: a READY activity reads REVIEW (open decision)).", ""]
        L += [f"- `{i}` {words.get(i, '')}: {', '.join(f'`{x}`' for x in xs)}" for i, xs in opened.items()]
    # session 14 (W4; report section 9 G7): preparation readiness apart from a finalisation that needs a decision
    if any(a.get("preparation") for a in acts):
        prep_fin = [a for a in acts if str(a.get("finalisation", "")).startswith(("FINALISATION GATED",
                                                                                  "FINALISATION NEEDS A DECISION"))]
        L += ["", "## Preparation readiness and finalisation (two states; nothing approved)", "",
              "Every activity says apart whether its preparation can start (its inputs: predecessors and earliest start) "
              "and what its finalisation needs (columns `preparation` and `finalisation` in programme.csv/json and "
              "gantt.html; an amber tick on the Gantt row marks the date the decision is needed by). "
              f"{len(prep_fin)} activities can be prepared now or on their earliest start while their finalisation needs "
              "a person's decision that is not recorded:", ""]
        L += [f"- `{a['id']}`: {_md(a['preparation'])}; {_md(a['finalisation'])}" for a in prep_fin]
    f4 = p.get("form_4e_checks") or {}
    if f4.get("checks"):                         # session 14 (W4): Form 4-E against the whole Proposal (VOL-I 9.6)
        L += ["", f"## Form 4-E against the whole Proposal ({len(f4['checks'])} documents; {f4.get('rule')})", "",
              "Every document placed in Envelope A or B is checked against Form 4-E's finalisation (form_4e_checks.csv/"
              "json: the clause that places it in the Proposal, its status, the open issues of the rows it carries).", ""]
        L += [f"- `{c['document_activity']}` ({c['envelope']}): {_md(c['status'])}" for c in f4["checks"]]
        L += ["", "Findings for a person (nothing resolved; no duration, setting or dependency changed):", ""]
        L += [f"- {_md(x)}" for x in f4.get("findings") or []] or ["- none"]
    res = p.get("resources") or {}
    L += ["", f"## Overloads ({len(res.get('overloads', []))}; reported, not resolved)", ""]
    L += [f"- {o['resource']}: {date_span(o['from'], o['to'])} ({o['days']} WD), peak {o['peak_load']:g} vs capacity "
          f"{o['capacity']} staff; activities {', '.join(o['activities'])}" for o in res.get("overloads", [])] or ["- none"]
    L += ["", "## Timing at the planning date", ""]
    bad = [a for a in acts if a["status"] != "OK"]
    drv = {d["activity"]: d for d in p.get("drivers", [])}
    L += [f"- `{a['id']}`: {a['status']} ("
          + (f"float {a['float_wd']} WD" if a["float_wd"] is not None else "no float: no latest start") + "; "
          + f"{', '.join(a['req_ids'][:6])}"
          + (f" +{len(a['req_ids']) - 6} more" if len(a["req_ids"]) > 6 else "") + ")"
          + (f"; would be feasible with: {drv[a['id']]['would_make_feasible'][0]}" if a["id"] in drv else "")
          + (f"; clarification question drafted, not sent: {', '.join(a['clarification_questions'])}"
             + (f", decide whether to ask the Authority by {a['ask_by']}" if a.get("ask_by") else "")
             if a.get("clarification_questions") and not a.get("gated_by") else "")
          for a in bad] or ["- all OK"]
    L += ["", "## Per discipline", "", "| Discipline | Activities | Staff effort (WD) | Waiting on external parties | "
          "Gated | Infeasible | Overloaded |", "|---|---|---|---|---|---|---|"]
    L += [f"| {d['discipline']} | {d['activities']} | {d['staff_effort_wd']:g} | {d['waiting_activities']} | "
          f"{len(d['gated'])} | {len(d['infeasible'])} | {len(d['overloaded'])} |" for d in p.get("disciplines", [])]
    L += ["", "## What is assumed (every value PROVISIONAL, editable in config/assumptions.yaml)", "",
          "No bidder references, certificates, attendance or financial standing are assumed to exist: the programme "
          "plans the work to obtain or confirm them; whether the Bidder attended the Pre-Bid Conference, holds qualifying "
          "references, certificates or the VOL-I 8.4 financial standing is not known.", "",
          "### Bidder (assumed scenario)", "", "| Setting | Value | Basis | Owner |", "|---|---|---|---|"]
    bb = asm.get("bidder_basis") or {}
    L += [f"| bidder.{k} | {_md(v)} | {_md((bb.get(k) or {}).get('basis', 'configurable assumption'))} | "
          f"{_md((bb.get(k) or {}).get('owner', 'Bid manager'))} |" for k, v in (asm.get("bidder") or {}).items()]
    sub = asm.get("submission") or {}
    if "delivery_buffer_wd" in sub:         # session 11 (audit A5-7): the delivery buffer is a visible choice
        db = sub.get("delivery_buffer_basis") or {}
        L += ["", "### Submission", "", "| Setting | Value | Basis | Owner |", "|---|---|---|---|",
              f"| submission.delivery_buffer_wd | {sub['delivery_buffer_wd']} | {_md(db.get('basis', ''))} | "
              f"{_md(db.get('owner', ''))} |"]
    L += ["", "### Resource capacities", "", "| Role | Capacity (staff per WD) | Basis | Owner |", "|---|---|---|---|"]
    L += [f"| {k} | {v.get('capacity')} | {_md(v.get('basis'))} | {_md(v.get('owner'))} |"
          for k, v in (asm.get("resources") or {}).items()]
    L += ["", "### Lead times (elapsed WD), staff effort and external waiting", "",
          "| Key | Elapsed WD | Effort WD (per unit) | Waits on | Basis | Effort basis | Owner |", "|---|---|---|---|---|---|---|"]
    L += [f"| {k} | {v.get('value')} | {v.get('effort_wd', '= elapsed (default)')} | {_md(v.get('waiting_on') or '-')} | "
          f"{_md(v.get('basis'))} | {_md(v.get('effort_basis', ''))} | {_md(v.get('owner'))} |"
          for k, v in (asm.get("lead_times") or {}).items()]
    if scenarios_result:
        L += ["", "## Scenarios (config/scenarios.yaml)", ""]
        L += [f"- **{row['scenario']}**{' (HYPOTHETICAL)' if row['hypothetical'] else ''}: {_md(row['purpose'])} — "
              f"infeasible {row['infeasible_base']} -> {row['infeasible']}, overloads {row['overloads_base']} -> "
              f"{row['overloads']}" + (f"; documents: {'; '.join(row['document_changes'])}" if row["document_changes"] else "")
              for row in scenarios_result["comparison"]]
    L += ["", "## Files", "",
          "| File | Content |", "|---|---|",
          "| programme.csv/json | every activity: dates (ES, EF, LS, LF), float, the three statuses, effort and waiting, req_ids |",
          "| marshalling.csv/json | one line per required item: issuer, count, lead time (ASSUMPTION), latest start, needed by, req_ids |",
          "| documents.csv/json | document counts per item and per envelope |",
          "| resources.csv/json, overloads.csv/json | staff load per role per Working Day; overload runs |",
          "| disciplines.csv/json | totals per discipline |", "| milestones.csv/json | dated pack milestones |",
          "| drivers.csv/json | what drives each infeasible activity and what would make it feasible |",
          "| form_4e_checks.csv/json | every Proposal document against Form 4-E's finalisation (VOL-I 9.6), the what-if "
          "and the findings for a person |",
          "| requirements_not_carried.csv/json | every A1 row in force no activity carries, with the reason |",
          "| requirements_coverage.csv/json | every A1 row in force and how it is carried (`carried_how`: discharged, "
          "reviewed for deviations under a volume check, excepted) |",
          "| scenario_comparison.csv/json, scenarios/ | the scenarios against the baseline |",
          "| gantt.svg, gantt.html, gantt.pdf | the Gantt, drawn from the same programme data |", "",
          NOTICE, ""]
    return "\n".join(L)


def write(prog_ext: dict, scenarios_result: dict | None, out_dir: Path) -> list[Path]:
    """Deterministic A5 files (no timestamps) under out_dir/a5/, including the Gantt and the README."""
    from . import gantt
    a5 = Path(out_dir) / "a5"
    meta = {"stage": prog_ext["stage"], "status_date": prog_ext["status_date"], "anchors": prog_ext["anchors"],
            "planning_date": prog_ext.get("planning_date", prog_ext["status_date"]),
            "planning_basis": prog_ext.get("planning_basis", "")}
    paths = []
    paths += write_csv_json(_table(PROGRAMME_COLS, prog_ext["activities"], **meta, problems=prog_ext.get("problems", []),
                                   exceptions=prog_ext.get("exceptions", {})), a5, "programme")
    paths += write_csv_json(_table(MARSHALLING_COLS, prog_ext["marshalling"], **meta), a5, "marshalling")
    docs = prog_ext["documents"]
    total_rows = [{**t, "evidence": f"TOTAL Envelope {t['envelope']}", "kind": "TOTAL", "multiplicity": t["documents"],
                   "activities": t["evidence"]} for t in docs["totals"]]
    paths += write_csv_json(_table(DOCUMENT_COLS, docs["items"] + total_rows, **meta, totals=docs["totals"],
                                   notes=docs["notes"]), a5, "documents")
    res = prog_ext["resources"]
    paths += write_csv_json(_table(RESOURCE_COLS, res["rows"], **meta, window=res["window"], roles=res["roles"],
                                   notes=res["notes"], levelling=NO_LEVELLING), a5, "resources")
    paths += write_csv_json(_table(OVERLOAD_COLS, res["overloads"], **meta, window=res["window"], levelling=NO_LEVELLING),
                            a5, "overloads")
    paths += write_csv_json(_table(DISCIPLINE_COLS, prog_ext["disciplines"], **meta), a5, "disciplines")
    paths += write_csv_json(_table(MILESTONE_COLS, prog_ext.get("milestones", []), **meta), a5, "milestones")
    paths += write_csv_json(_table(DRIVER_COLS, prog_ext["drivers"], **meta), a5, "drivers")
    f4 = prog_ext.get("form_4e_checks") or {}
    if f4.get("checks"):                         # session 14 (W4): Form 4-E against the whole Proposal (VOL-I 9.6)
        paths += write_csv_json(_table(FORM_4E_COLS, f4["checks"], **meta, rule=f4.get("rule"), what_if=f4.get("what_if"),
                                       findings=f4.get("findings")), a5, "form_4e_checks")
    if prog_ext.get("row_coverage") is not None:     # session 12 (audit A5-4)
        paths += write_csv_json(_table(NOT_CARRIED_COLS, not_carried(prog_ext), **meta,
                                       check=coverage_check(prog_ext)["detail"]), a5, "requirements_not_carried")
        if "discharged" in (prog_ext.get("row_coverage") or {}):       # session 12 (F5; audit A5 N3)
            paths += write_csv_json(_table(COVERAGE_COLS, coverage_rows(prog_ext), **meta,
                                           check=coverage_check(prog_ext)["detail"]), a5, "requirements_coverage")
    if scenarios_result:
        for name, s in scenarios_result["scenarios"].items():
            c = s["changes"]
            paths += write_csv_json(_table(SCENARIO_COLS, c["activities"], **meta, scenario=name, purpose=s["purpose"],
                                           hypothetical=s["hypothetical"], overrides=s["overrides"],
                                           status_changes=c["status_changes"], document_changes=c["document_changes"],
                                           envelope_totals=c["envelope_totals"], resource_changes=c["resource_changes"],
                                           drivers=s["programme"]["drivers"]), a5 / "scenarios", name)
        paths += write_csv_json(_table(COMPARISON_COLS, scenarios_result["comparison"], **meta), a5, "scenario_comparison")
    paths += gantt.write(prog_ext, a5)
    write_text(a5 / "README.md", readme(prog_ext, scenarios_result))
    paths.append(a5 / "README.md")
    return paths


# ---------------------------------------------------------------------------------------------- candidate (session 11)
# A PARTIAL addendum: the programme replanned at the working stage beside the validated A5, which is never touched
# (tenderpack.partial builds the inputs; stage2.write calls it).

CANDIDATE_NOTICE = ("CANDIDATE — NOT VALIDATED. The programme replanned at the working stage of a PARTIAL addendum: every "
                    "op valid there stands as a proposal, none is accepted, and the validated A5 (the a5/ folder above "
                    "this one) is unchanged. " + NOTICE)
CANDIDATE_PROGRAMME_COLS = ("id", "name", "candidate_status", "candidate_change", "blocked", "earliest_start_validated",
                            "earliest_start", "latest_start_validated", "latest_start", "latest_finish_validated",
                            "latest_finish", "shift_wd", "status_validated", "status", "caused_by_rows", "caused_by_ops",
                            "decision_milestones")
CANDIDATE_PROGRAMME_COLS += tuple(c for c in PROGRAMME_COLS if c not in CANDIDATE_PROGRAMME_COLS)
CANDIDATE_CHANGE_COLS = ("id", "name", "change", "earliest_start_validated", "earliest_start", "latest_start_validated",
                         "latest_start", "latest_finish_validated", "latest_finish", "shift_wd", "status_validated",
                         "status", "caused_by_rows", "caused_by_ops", "blocked", "review")
CANDIDATE_BLOCKED_COLS = ("activity", "name", "rows", "why", "latest_start", "latest_finish", "status")
CANDIDATE_SCENARIO_COLS = ("id", "kind", "stage", "provision", "op", "applied", "trigger_deadline", "effective_from",
                           "trigger", "if_triggered", "if_not_triggered", "rows", "activities", "dates_printed", "model",
                           "source")


def candidate_replan(prog_v: dict | None, prog_c: dict, ev: dict, ew: dict, cal: Calendar, *, blocked: dict[str, list[str]],
                     row_ops: dict[str, list[str]], scenarios: list[dict], label: str,
                     date_rows: set[str] | None = None, answers: dict[str, list[dict]] | None = None,
                     window: dict | None = None) -> dict:
    """The candidate A5 of a PARTIAL addendum (session 11): `prog_c` (the extended programme of the working stage, its
    planning date the working stage's issue date) compared with `prog_v` (the validated one) by `compare` and
    schedule.deltas: per activity what moves (NEW / REMOVED / MOVED / EARLY DATES / STATUS / REWORK / REVIEW), the rows
    that moved it (`date_rows`, rows whose planning dates changed or that came into force with dates, for MOVED; else
    `row_ops`: rows whose status, reading or ops changed, with their ops), whether it is BLOCKED (a row it serves is
    unresolved: `blocked`, row -> why; its candidate dates are not reliable) and the decision milestones of the
    conditional scenarios that reach it: the engine's own decision milestone when the conditional model gives one
    (schedule.milestones, `decision`), else one at the trigger deadline as printed; an effective-dated amendment at
    its effective date. Session 12: `answers` (signals.causes_between from the validated to the working stage) lets the
    shared predicate tell a confirmation from a change (CONFIRMED (unchanged), never REWORK; a REWORK names only the rows
    that changed); `window` (clarify.window at the working stage) puts the closed clarification route on the activity that
    must finish by the cut-off and on every activity whose decision date asks the Authority. Pure; prog_v and prog_c are
    not changed."""
    from .schedule import CLARIFICATION_RULE, CONFIRMED, deltas
    date_rows = set(date_rows or ())
    cmp_ = compare(prog_v, prog_c, cal) if prog_v else {"activities": []}
    by = {a["id"]: a for a in cmp_["activities"]}
    extra: dict[str, list[str]] = {}
    rework_rows: dict[str, list[str]] = {}
    confirmed: dict[str, dict] = {}
    for d in (deltas(prog_v, prog_c, ev, ew, answers=answers) if prog_v else []):
        if d["change"] not in ("MOVED", "NEW", "REMOVED", "STATUS") and d["change"] not in extra.setdefault(d["activity"], []):
            extra[d["activity"]].append(d["change"])
        if d["change"] == "REWORK":
            rework_rows[d["activity"]] = list(d.get("rows") or [])
        elif d["change"] == CONFIRMED:
            confirmed[d["activity"]] = {"rows": list(d.get("rows") or []), "detail": d["detail"]}
    closed = (window or {}).get("closed") and (window or {}).get("note")
    vacts = {a["id"]: a for a in (prog_v or {}).get("activities", [])}
    have = {m["id"]: m for m in prog_c.get("milestones") or []}
    decisions, scen = [], []
    for sc in scenarios:
        hit = sorted(a["id"] for a in prog_c["activities"] if set(a["req_ids"]) & set(sc.get("rows") or []))
        scen.append({**sc, "activities": hit})
        if sc.get("milestone") in have:                     # the engine planned it (conditional model): referenced
            decisions.append({**have[sc["milestone"]], "activities": sorted(set(have[sc["milestone"]].get("activities")
                                                                                   or []) | set(hit)), "existing": True})
            continue
        when = sc.get("trigger_deadline") if sc["kind"] == "conditional" else sc.get("effective_from")
        dated = bool(when and len(str(when)) == 10 and str(when)[4] == "-")
        decisions.append({
            "id": f"{'DECISION' if sc['kind'] == 'conditional' else 'EFFECTIVE'}-{sc['provision']}",
            "date": str(when) if dated else "", "time": "",
            "short": f"{'decision' if sc['kind'] == 'conditional' else 'takes effect'}: {sc['provision']}",
            "label": (f"CANDIDATE decision: does {sc['provision']} take effect? (conditional; the trigger is never assumed)"
                      if sc["kind"] == "conditional" else f"CANDIDATE: {sc['provision']} takes effect (effective-dated)"),
            "kind": ("decision (conditional amendment; trigger deadline as printed, not computed)" if dated else
                     "decision (conditional amendment; event-dependent, no date)") if sc["kind"] == "conditional" else
                    "effective date (as printed)",
            "purpose": "decision", "conditional": True, "derived": False, "reading": "as printed in the addendum",
            "readings_differ": False, "source": sc["provision"], "words": sc.get("trigger") or "",
            "rows": list(sc.get("rows") or []), "activities": hit})
    acts = []
    for a in prog_c["activities"]:
        x, v = by.get(a["id"]), vacts.get(a["id"])
        change = list(x["change"]) if x else ["NEW"]
        change += [c for c in extra.get(a["id"], []) if c not in change]
        moved = bool({"MOVED", "NEW", "REWORK"} & set(change))
        rows = sorted(r for r in a["req_ids"] if r in row_ops) if moved else []
        if "MOVED" in change and set(rows) & date_rows:            # the rows whose dates moved, when there are some
            rows = sorted(set(rows) & date_rows)
        elif "REWORK" in change and "NEW" not in change and a["id"] in rework_rows:
            rows = sorted(set(rework_rows[a["id"]]) & set(a["req_ids"]))   # session 12: only the rows that changed
        blk = sorted({f"{r}: {why}" for r in a["req_ids"] for why in blocked.get(r, [])})
        dec = [m["id"] for m in decisions if a["id"] in m["activities"]]
        status = ("BLOCKED" if blk else "MOVED" if "MOVED" in change else "NEW" if "NEW" in change else
                  "REVIEW" if a.get("relationship_review") else "REWORK" if "REWORK" in change else "unchanged")
        route = []
        if closed and (a.get("deadline_rule") == CLARIFICATION_RULE or a.get("ask_by")
                       or a.get("clarification_questions")):
            route = [f"CLARIFICATION ROUTE CLOSED (candidate): {window['note']}"]
        acts.append({**a, "candidate_status": status, "candidate_change": change, "blocked": blk,
                     "confirmed": confirmed.get(a["id"]),
                     "earliest_start_validated": (v or {}).get("earliest_start"),
                     "latest_start_validated": (v or {}).get("latest_start"),
                     "latest_finish_validated": (v or {}).get("latest_finish"),
                     "status_validated": (v or {}).get("status"), "shift_wd": x["shift_wd"] if x else None,
                     "caused_by_rows": rows, "caused_by_ops": sorted({o for r in rows for o in row_ops.get(r, [])}),
                     "decision_milestones": dec,
                     "flags": list(a.get("flags") or []) + ([f"BLOCKED (candidate): {'; '.join(blk)}"] if blk else [])
                     + route})
    removed = [{"id": x["id"], "name": x["name"], "change": x["change"], "latest_start_validated": x["latest_start_base"],
                "latest_finish_validated": x["latest_finish_base"], "status_validated": x["status_base"]}
               for x in cmp_["activities"] if "REMOVED" in x["change"]]
    by_act = {a["id"]: a for a in acts}
    changes = []
    for a in acts:
        if a["candidate_change"] or a["blocked"]:
            changes.append({k: a.get(k) for k in ("id", "name", "earliest_start_validated", "earliest_start",
                                                  "latest_start_validated", "latest_start", "latest_finish_validated",
                                                  "latest_finish", "shift_wd", "status_validated", "status",
                                                  "caused_by_rows", "caused_by_ops", "blocked")}
                           | {"change": a["candidate_change"],
                              "review": [f"{rv['class']}: {', '.join(rv['targets'])}" for rv in a.get("relationship_review") or []]})
    changes += [dict(x, earliest_start=None, latest_start=None, latest_finish=None, status=None, caused_by_rows=[],
                     caused_by_ops=[], blocked=[], review=[]) for x in removed]
    blocked_rows = [{"activity": a["id"], "name": a["name"], "rows": sorted(set(a["req_ids"]) & set(blocked)),
                     "why": sorted({w for r in a["req_ids"] for w in blocked.get(r, [])}),
                     "latest_start": a["latest_start"], "latest_finish": a["latest_finish"], "status": a["status"]}
                    for a in acts if a["blocked"]]
    marsh = [dict(m, blocked=sorted({x for act in m.get("activities") or [] for x in (by_act.get(act) or {}).get("blocked", [])}))
             for m in prog_c.get("marshalling") or []]
    ms = sorted(list(prog_c.get("milestones") or []) + [m for m in decisions if not m.get("existing")],
                key=lambda m: (m["date"] or "9999", m["id"]))
    summary = {"moved": sorted(a["id"] for a in acts if "MOVED" in a["candidate_change"]),
               "new": sorted(a["id"] for a in acts if "NEW" in a["candidate_change"]),
               "removed": sorted(x["id"] for x in removed),
               "rework": sorted(a["id"] for a in acts if "REWORK" in a["candidate_change"]),
               "confirmed": sorted(a["id"] for a in acts if a.get("confirmed")),
               "review": sorted(a["id"] for a in acts if a.get("relationship_review")),
               "blocked": sorted(a["id"] for a in acts if a["blocked"]),
               "status_changed": sorted(a["id"] for a in acts if "STATUS" in a["candidate_change"]),
               "decisions": [m["id"] for m in decisions]}
    return {"stage": label, "status_date": prog_c["status_date"], "clarification_window": window,
            "planning_date": prog_c.get("planning_date", prog_c["status_date"]),
            "validated_status_date": (prog_v or {}).get("status_date"), "validated_stage": (prog_v or {}).get("stage"),
            "planning_basis": prog_c.get("planning_basis", ""), "anchors": prog_c.get("anchors", {}),
            "activities": acts, "removed": removed, "changes": changes, "blocked": blocked_rows, "scenarios": scen,
            "decisions": decisions, "milestones": ms, "marshalling": marsh, "summary": summary,
            "programme": {**prog_c, "stage": label, "activities": acts, "milestones": ms}}


def _ctable(cols, rows, **extra) -> dict:
    return {"columns": [{"key": k, "header": k, "width": 20} for k in cols],
            "rows": [{k: r.get(k) for k in cols} for r in rows], "notice": CANDIDATE_NOTICE, **extra}


def write_candidate(cand: dict, a5_dir: Path, paragraph: str = "") -> list[Path]:
    """The candidate A5 (candidate_replan) under `a5_dir` (out/a5/candidate/): programme, changes, marshalling,
    milestones (with the decision milestones), blockers, scenarios, the Gantt drawn from the same data and a README.
    Deterministic; nothing outside `a5_dir` is written."""
    import html as _html
    from . import gantt
    a5 = Path(a5_dir)
    meta = {"stage": cand["stage"], "status_date": cand["status_date"], "planning_date": cand["planning_date"],
            "validated_stage": cand["validated_stage"], "validated_status_date": cand["validated_status_date"],
            "planning_basis": cand["planning_basis"], "anchors": cand["anchors"]}
    paths = []
    paths += write_csv_json(_ctable(CANDIDATE_PROGRAMME_COLS, cand["activities"], **meta, summary=cand["summary"]),
                            a5, "programme")
    paths += write_csv_json(_ctable(CANDIDATE_CHANGE_COLS, cand["changes"], **meta), a5, "changes")
    paths += write_csv_json(_ctable(MARSHALLING_COLS + ("blocked",), cand["marshalling"], **meta), a5, "marshalling")
    paths += write_csv_json(_ctable(MILESTONE_COLS, cand["milestones"], **meta), a5, "milestones")
    paths += write_csv_json(_ctable(CANDIDATE_BLOCKED_COLS, cand["blocked"], **meta), a5, "blockers")
    paths += write_csv_json(_ctable(CANDIDATE_SCENARIO_COLS, cand["scenarios"], **meta), a5, "scenarios")
    paths += gantt.write(cand["programme"], a5)
    g = a5 / "gantt.html"
    t = g.read_text(encoding="utf-8")
    i = t.find("<body>") + len("<body>")
    g.write_text(t[:i] + '<p style="background:#fde2e2;border:2px solid #b00000;color:#7a0000;font-weight:bold;'
                 f'padding:6px 10px">{_html.escape(CANDIDATE_NOTICE.split(". ")[0])}: {_html.escape(paragraph)}</p>' + t[i:],
                 encoding="utf-8")
    write_text(a5 / "README.md", candidate_readme(cand, paragraph))
    paths.append(a5 / "README.md")
    return paths


def candidate_readme(cand: dict, paragraph: str = "") -> str:
    s = cand["summary"]
    acts = {a["id"]: a for a in cand["activities"]}
    L = [f"# A5 CANDIDATE — {cand['stage']}", "",
         f"> **CANDIDATE — NOT VALIDATED.** The validated A5 is `../README.md` ({cand['validated_stage']}, planning date "
         f"{cand['validated_status_date']}); nothing there is changed. This folder replans the programme at the working "
         f"stage (planning date {cand['status_date']}, its issue date) with every op that is valid there standing as a "
         "proposal. Earliest dates move with the planning date for every activity (EARLY DATES); the latest dates move "
         "only where a pack date or a requirement changes.", ""]
    if paragraph:
        L += ["## What may be changing", "", paragraph, ""]
    from .derived import a5_lines                  # session 12 (W3b): computed deadlines, Working Days left, pending readings
    L += a5_lines(cand.get("derived"))
    win = cand.get("clarification_window") or {}
    if win.get("closed"):                          # session 12: the closed clarification route, in one wording
        route = [a["id"] for a in cand["activities"] if any(str(f).startswith("CLARIFICATION ROUTE CLOSED")
                                                            for f in a.get("flags") or [])]
        L += ["## Clarification route", "", f"{win['note'][0].upper() + win['note'][1:]}. Activities that relied on it: "
              + (", ".join(f"`{a}`" for a in route) or "none") + ".", ""]
    L += [f"## Dates that move ({len(s['moved'])} activities; latest start / finish, validated -> candidate)", "",
          "| Activity | Latest start | Latest finish | Shift (WD) | Timing | Rows that move it | Ops |", "|---|---|---|---|---|---|---|"]
    L += [f"| {a} | {acts[a]['latest_start_validated']} -> {acts[a]['latest_start']} | {acts[a]['latest_finish_validated']} -> "
          f"{acts[a]['latest_finish']} | {acts[a]['shift_wd']} | {acts[a]['status_validated']} -> {acts[a]['status']} | "
          f"{', '.join(acts[a]['caused_by_rows']) or 'through the network (a linked activity or a pack date)'} | "
          f"{', '.join(acts[a]['caused_by_ops']) or '-'} |" for a in s["moved"]] or ["| none | | | | | | |"]
    L += ["", f"## New and removed activities ({len(s['new'])} new, {len(s['removed'])} removed)", ""]
    L += [f"- NEW `{a}`: needed by {', '.join(acts[a]['req_ids'])}; latest start {acts[a]['latest_start']}"
          + (f" (ops {', '.join(acts[a]['caused_by_ops'])})" if acts[a]["caused_by_ops"] else "") for a in s["new"]]
    L += [f"- REMOVED `{x['id']}` (was latest start {x['latest_start_validated']})" for x in cand["removed"]]
    if not s["new"] and not s["removed"]:
        L.append("- none")
    L += ["", f"## Requirement changed: work may need redoing (REWORK, {len(s['rework'])})", ""]
    L += [f"- `{a}`: rows {', '.join(acts[a]['caused_by_rows']) or 'see changes.csv'}" for a in s["rework"]] or ["- none"]
    conf = s.get("confirmed") or []                # session 12: confirmations are not changes (signals.requirement_delta)
    L += ["", f"## Confirmed, unchanged: work done stands (CONFIRMED, {len(conf)})", ""]
    L += [f"- `{a}`: {acts[a]['confirmed']['detail']}" for a in conf] or ["- none"]
    L += ["", f"## Marked REVIEW through relationships ({len(s['review'])}; dates unchanged)", ""]
    L += [f"- `{a}`: " + "; ".join(f"{rv['class']}: {', '.join(rv['targets'])} via {', '.join(rv['entries'])}"
                                   for rv in acts[a].get("relationship_review") or []) for a in s["review"]] or ["- none"]
    L += ["", f"## Blocked: the row is unresolved, the candidate dates are not reliable ({len(cand['blocked'])})", ""]
    L += [f"- `{b['activity']}` (rows {', '.join(b['rows'])}): {'; '.join(b['why'])}" for b in cand["blocked"]] or ["- none"]
    L += ["", f"## Conditional scenarios and decision milestones ({len(cand['scenarios'])})", ""]
    for sc, m in zip(cand["scenarios"], cand["decisions"]):
        L += [f"- **{m['id']}** {m['date'] or '(no date: event-dependent)'}: {sc['provision']} ({sc['kind']} "
              f"{sc.get('what') or ''}; "
              f"{'applied' if sc['applied'] else 'not applied'} in the candidate). If triggered: {sc['if_triggered']}. "
              f"If not: {sc['if_not_triggered']}. Activities reached: {', '.join(sc['activities']) or 'none'}"
              + (" — their dates in both states: " + "; ".join(
                  f"{a} LS {acts[a]['latest_start_validated']} (without) / {acts[a]['latest_start']} (with)"
                  for a in sc["activities"]) if sc["activities"] else "") + f". {sc['model']}."]
    if not cand["scenarios"]:
        L.append("- none in the op file")
    L += ["", "## Files", "", "| File | Content |", "|---|---|",
          "| programme.csv/json | every activity at the working stage with its validated dates beside it, candidate status "
          "(BLOCKED / MOVED / NEW / REVIEW / REWORK / unchanged; a confirmation is CONFIRMED (unchanged) in its changes), "
          "the rows and ops that move it |",
          "| changes.csv/json | every activity that changes (and the removed ones) |",
          "| marshalling.csv/json | the marshalling plan at the working stage, with blocked items |",
          "| milestones.csv/json | the pack milestones and the candidate decision milestones |",
          "| blockers.csv/json | activities whose row is unresolved |", "| scenarios.csv/json | conditional scenarios |",
          "| gantt.svg, gantt.html, gantt.pdf | the Gantt drawn from the same data |", "", CANDIDATE_NOTICE, ""]
    return "\n".join(L)
