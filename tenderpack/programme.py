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
      milestones,drivers,scenario_comparison}.{csv,json}, a5/scenarios/<name>.{csv,json}, a5/gantt.{svg,html,pdf}
      and a5/README.md
"""
from __future__ import annotations

import copy
from datetime import date
from pathlib import Path

from .dates import Calendar, calendar_from_config
from .render import write_csv_json
from .schedule import (DISCIPLINES, LOAD_WINDOW, NO_LEVELLING, date_span, multiplicity, network, plan, resource_load,
                       resource_statuses)
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
        gated = [a for a in mine if a.get("gated_by")]
        out.append({**row, **counts, "item": prod.get("item") or d.get("name", ""), "activity": prod["id"],
                    "activities": [a["id"] for a in order], "lead_time_wd": lt, "lead_time_chain": path,
                    "lead_time_keys": list(dict.fromkeys(a["duration_assumption"] for a in order)),
                    "lead_time_basis": "ASSUMPTION (PROVISIONAL, config/assumptions.yaml lead_times): "
                                       + "; ".join(_lead_label(a) for a in order),
                    "waiting_on": "; ".join(sorted({a["waiting_on"] for a in mine if a.get("waiting_on")})),
                    "drop_dead_start": min((a["latest_start"] for a in mine if a["latest_start"]), default=None),
                    "needed_by": prod["latest_finish"], "earliest_finish": prod.get("earliest_finish"),
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
        lts = [f"{k} = {lead.get(k, {}).get('value', '?')} WD (PROVISIONAL ASSUMPTION; owner {lead.get(k, {}).get('owner', '?')})"
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
                          ("planning", "calendar", "bidder", "bidder_basis", "resources", "lead_times")}
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
                    reached=((r.get("relationship_impact") or {}).get(stage) or {}).get("records"))
        for act in prog["activities"]:
            for i in act.get("gated_by") or []:
                if i not in open_issues:
                    act["flags"].append(f"GATE ISSUE NOT IN THE REGISTER ({i}: decided and removed, or a typo; the gate "
                                        "stays until a person removes it from curation/activity_templates.yaml)")
        return extend(prog, r["evidence_items"], a, cal) if extended else prog

    return make_plan


# ---------------------------------------------------------------------------------------------- write

PROGRAMME_COLS = ("id", "name", "discipline", "evidence", "envelope", "req_ids", "owner", "resource", "issuer", "count",
                  "multiplicity", "duration_wd", "duration_assumption", "duration_basis", "effort_wd", "effort_total_wd",
                  "effort_basis", "waiting_on", "work_type", "predecessors", "earliest_start", "earliest_finish",
                  "es_driven_by", "latest_start", "latest_finish", "driven_by", "float_wd", "deadline", "timing_status",
                  "decision_status", "gated_by", "decision_needed_by", "condition", "resource_status", "status", "flags")
MARSHALLING_COLS = ("evidence", "item", "name", "kind", "envelope", "issuer", "per", "count", "count_basis",
                    "marked_originals", "hard_copies", "physical_count", "electronic_copy", "activity", "activities",
                    "lead_time_wd", "lead_time_chain", "lead_time_keys", "lead_time_basis", "waiting_on",
                    "drop_dead_start", "needed_by", "earliest_finish", "float_wd", "timing_status", "decision_status",
                    "resource_status", "status", "owner", "resource", "req_ids", "flags")
DOCUMENT_COLS = ("evidence", "name", "envelope", "kind", "issuer", "per", "multiplicity", "multiplicity_basis",
                 "marked_originals", "hard_copies", "physical_count", "electronic_copy", "usb", "req_ids",
                 "activities", "source", "flags")
RESOURCE_COLS = ("resource", "date", "iso_week", "load_wd", "capacity", "status", "activities", "capacity_basis",
                 "capacity_owner")
OVERLOAD_COLS = ("resource", "from", "to", "days", "dates", "peak_load", "capacity", "activities")
DISCIPLINE_COLS = ("discipline", "activities", "staff_effort_wd", "elapsed_wd", "waiting_activities", "external_parties",
                   "roles", "gated", "infeasible", "overloaded", "activity_ids")
MILESTONE_COLS = ("id", "date", "time", "short", "label", "kind", "purpose", "conditional", "derived", "reading",
                  "readings_differ", "source", "words", "rows", "activities")
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
    L += [f"- **{m['date']}{(' ' + m['time']) if m['time'] else ''}** {_md(m['label'])} "
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
          "- `decision_status`: READY, or GATED: finalisation waits on an open issue; the decision is needed by the gated "
          "activity's latest start. Preparation is never gated.",
          "- `resource_status`: OK / OVERLOAD role on dates (peak load vs capacity) / NOT LOADED (why).", "",
          "A gated activity can be on time, and an infeasible one can be decision-ready: the three are read separately.",
          "", "## Decision gates (finalisation only; preparation continues)", ""]
    gated = [a for a in acts if a.get("gated_by")]
    by_id = {a["id"]: a for a in acts}
    for a in gated:
        preps = [x for x in a["predecessors"] if not by_id.get(x, {}).get("gated_by")]
        L.append(f"- `{a['id']}` — {a['decision_status']} (timing: {a['status']}; preparation continuing: "
                 f"{', '.join(preps) or 'none'})")
    if not gated:
        L.append("- none")
    L += ["", "## Conditional obligations", ""]
    cond = [a for a in acts if a.get("condition")]
    for a in cond:
        L.append(f"- `{a['id']}`: needed only if {a['condition']}. Timing: **{a['status']}**. An elapsed window alone "
                 "does not establish a missed duty; a person records whether the condition arose.")
    if not cond:
        L.append("- none")
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
