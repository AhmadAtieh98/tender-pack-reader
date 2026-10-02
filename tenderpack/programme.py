"""A5 Stage 4: documents, resources, drivers and scenarios, built on one stage's programme (schedule.plan).

Everything here is computed from the programme and the configured ASSUMPTIONS (config/assumptions.yaml);
nothing is typed. Every lead time, multiplicity and capacity is a PROVISIONAL assumption with a basis and an
owner; none is a fact from the tender pack. Pure functions; only `write` touches the file system.

  extend(prog, evidence_items, assumptions, cal) -> prog + {documents, resources, drivers} and an extended
      marshalling plan:
      documents  per evidence item in force: envelope, issuer, per, multiplicity (bidder settings), physical
                 count = multiplicity x (marked originals + hard copies) for items counted in the VOL-I 6.5
                 copies, electronic copy yes/no; per-envelope totals (both envelopes always listed)
      resources  per role per ISO week: the peak number of the role's activities running on one Working Day
                 between latest start and latest finish (as late as possible; clipped at the status date) vs
                 the role's capacity; OVERLOAD (provisional) when above it
      drivers    for each INFEASIBLE or DEADLINE PASSED activity: the chain that sets its latest finish, up to
                 the pack deadline; the lead-time assumptions on it; the shortfall in Working Days; and what
                 would make it feasible (the largest value of each lead time that would, a later deadline)
  run_scenarios(make_plan, assumptions, scenarios, evidence_items=None) -> baseline, each scenario's
      programme and its changes against the baseline (latest dates, statuses, documents, overloads)
  stage_planner(r, stage=None) -> make_plan for run_scenarios from a stage2.run result (re-evaluates the
      register's dates when a scenario changes the calendar, e.g. a declared holiday moves the cut-off)
  write(prog_ext, scenarios_result, out_dir) -> a5/{programme,marshalling,documents,resources,drivers,
      scenario_comparison}.{csv,json} and a5/scenarios/<name>.{csv,json}
"""
from __future__ import annotations

import copy
from datetime import date, timedelta
from pathlib import Path

from .dates import Calendar, calendar_from_config
from .render import write_csv_json
from .schedule import backward_pass, multiplicity, plan

NOTICE = ("PROPOSAL, not reviewed. Every lead time, multiplicity and resource capacity is a PROVISIONAL ASSUMPTION "
          "(config/assumptions.yaml: value, basis, owner); none is stated in the tender pack. Latest dates come from "
          "a backward pass in Working Days (VOL-I 2.4) from the pack's dates; INFEASIBLE is reported, never compressed.")
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
        try:
            n, expr = multiplicity(it.per, bidder)
        except KeyError as e:
            n, expr = 1, ""
            flags.append(f"multiplicity unknown ({e.args[0]}); counted once")
        if expr:
            owners = [f"{k.split('.')[1].split(' ')[0]}: {basis.get(k.split('.')[1].split(' ')[0], {}).get('owner', '?')}"
                      for k in expr.split(" x ")]
            expr = f"{expr} (PROVISIONAL ASSUMPTION; owner {', '.join(owners)})"
        counted = bool(it.counted) and it.envelope in ("A", "B")
        kind = "document" if counted else ("document (not copied)" if it.envelope in ("A", "B") else "action")
        if it.envelope == excl.get("envelope") and excl.get("source_unit") and excl["source_unit"] not in it.source:
            flags.append(f"OPEN ISSUE: {excl['source_unit']} says Envelope {it.envelope} contains only the documents it "
                         f"lists; this item is required by {it.source}, so where it goes needs a clarification")
        if ev_id not in acts_by_ev:
            reason = (prog.get("exceptions") or {}).get(ev_id)
            flags.append(f"no activity: {reason}" if reason else "no activity and no exception (C44)")
        items.append({"evidence": ev_id, "name": it.name, "envelope": it.envelope, "kind": kind, "issuer": it.issuer,
                      "per": it.per, "multiplicity": n, "multiplicity_basis": expr or "one per proposal",
                      "marked_originals": n * n_orig if counted else 0, "hard_copies": n * n_copy if counted else 0,
                      "physical_count": n * (n_orig + n_copy) if counted else 0,
                      "electronic_copy": "yes" if counted else "no", "req_ids": need[ev_id],
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

def marshalling(prog: dict, docs: dict) -> list[dict]:
    """The last-stretch list: every activity that produces a physical or documentary item, with counts."""
    by_ev = {i["evidence"]: i for i in docs["items"]}
    both = [t for t in docs["totals"]]
    out = []
    for a in prog["activities"]:
        if not a.get("item"):
            continue
        d = by_ev.get(a.get("evidence"), {})
        if d.get("kind") == "document":
            counts = {"marked_originals": d["marked_originals"], "hard_copies": d["hard_copies"],
                      "physical_count": d["physical_count"], "electronic_copy": d["electronic_copy"]}
        elif a.get("envelope") == "A+B":                   # copies, sealing, delivery: both envelopes together
            counts = {"marked_originals": sum(t["marked_originals"] for t in both),
                      "hard_copies": sum(t["hard_copies"] for t in both),
                      "physical_count": sum(t["physical_count"] for t in both),
                      "electronic_copy": f"{sum(t['usb'] for t in both)} USB (PROVISIONAL: one per envelope)"}
        else:
            counts = {"marked_originals": 0, "hard_copies": 0, "physical_count": 0, "electronic_copy": "no"}
        out.append({"item": a["item"], "envelope": a.get("envelope", ""), "evidence": a.get("evidence", ""),
                    "issuer": a["issuer"], "owner": a["owner"], "resource": a.get("resource", ""),
                    "count": a.get("count", 1), "multiplicity": a.get("multiplicity", ""), **counts,
                    "lead_time_wd": a["duration_wd"], "lead_time_assumption": a["duration_assumption"],
                    "lead_time_basis": a["duration_basis"], "drop_dead_start": a["latest_start"],
                    "needed_by": a["latest_finish"], "status": a["status"], "activity": a["id"],
                    "req_ids": a["req_ids"], "flags": a["flags"]})
    return sorted(out, key=lambda m: (m["drop_dead_start"] or "9999", m["activity"]))


# ---------------------------------------------------------------------------------------------- resources

def resources(prog: dict, assumptions: dict, cal: Calendar) -> dict:
    roles = assumptions.get("resources") or {}
    sd = _d(prog["status_date"])
    load: dict[str, dict[date, list[str]]] = {}
    notes = []
    for a in prog["activities"]:
        r = a.get("resource")
        ls, lf = _d(a["latest_start"]), _d(a["latest_finish"])
        if not r:
            notes.append(f"{a['id']}: no resource role (not loaded)")
            continue
        if ls is None or lf is None:
            notes.append(f"{a['id']}: no latest dates (not linked to a pack date; not loaded)")
            continue
        if a["status"].startswith("DEADLINE PASSED"):
            notes.append(f"{a['id']}: deadline passed before the status date (not loaded)")
            continue
        if lf < sd:
            notes.append(f"{a['id']}: latest finish {lf} is before the status date (INFEASIBLE; not loaded, see drivers)")
            continue
        start = max(ls, sd)
        if ls < sd:
            notes.append(f"{a['id']}: window {ls}..{lf} clipped at the status date {sd} (INFEASIBLE; see drivers)")
        days = [start + timedelta(days=i) for i in range((lf - start).days + 1)]
        days = [x for x in days if cal.is_working_day(x)] or [lf]
        for x in days:
            load.setdefault(r, {}).setdefault(x, []).append(a["id"])
    rows = []
    for r in sorted(load):
        cfg = roles.get(r) or {}
        cap = cfg.get("capacity")
        weeks: dict[tuple[int, int], dict[date, list[str]]] = {}
        for x, ids in load[r].items():
            weeks.setdefault(tuple(x.isocalendar())[:2], {})[x] = ids
        for (y, w), days in sorted(weeks.items()):
            peak = max(len(v) for v in days.values())
            monday = date.fromisocalendar(y, w, 1)
            over = sorted(x.isoformat() for x, v in days.items() if cap is not None and len(v) > cap)
            rows.append({"resource": r, "iso_week": f"{y}-W{w:02d}", "week_start": monday.isoformat(),
                         "week_end": (monday + timedelta(days=6)).isoformat(), "days_loaded": len(days),
                         "peak_concurrent": peak, "capacity": cap,
                         "status": ("NO CAPACITY CONFIGURED" if cap is None else
                                    "OVERLOAD (provisional)" if peak > cap else "OK"),
                         "overloaded_days": over,
                         "activities": sorted({i for v in days.values() for i in v}),
                         "capacity_basis": cfg.get("basis", "not configured"), "capacity_owner": cfg.get("owner", "")})
    notes.insert(0, "Load at the latest dates (as late as possible): each activity counts once per Working Day "
                    "between its latest start and latest finish, whatever its multiplicity; an activity waiting on an "
                    "external issuer counts for the role that chases it. Starting earlier spreads the load. "
                    "Capacities are PROVISIONAL ASSUMPTIONS (config/assumptions.yaml resources:).")
    return {"rows": rows, "roles": {k: dict(v) for k, v in sorted(roles.items())}, "notes": notes}


# ---------------------------------------------------------------------------------------------- drivers

def _graph(prog: dict) -> dict[str, dict]:
    return {a["id"]: {"duration_wd": int(a["duration_wd"]), "predecessors": list(a["predecessors"]),
                      "deadline_rule": a.get("deadline_rule"), "deadline_date": _d(a.get("deadline_date")),
                      "key": a["duration_assumption"]} for a in prog["activities"]}


def _ls_with(g: dict, cal: Calendar, aid: str, key: str | None = None, value: int | None = None,
             shift_rule: str | None = None, shift_wd: int = 0) -> date | None:
    h = {k: dict(v) for k, v in g.items()}
    for v in h.values():
        if key is not None and v["key"] == key:
            v["duration_wd"] = value
        if shift_rule and v["deadline_rule"] == shift_rule and v["deadline_date"] is not None:
            v["deadline_date"] = cal.add_working_days(v["deadline_date"], shift_wd)
    return backward_pass(h, cal)[aid]["ls"]


def drivers(prog: dict, assumptions: dict, cal: Calendar) -> list[dict]:
    lead = assumptions.get("lead_times") or {}
    sd = _d(prog["status_date"])
    g = _graph(prog)
    bp = backward_pass(g, cal)
    out = []
    for a in sorted(prog["activities"], key=lambda x: (x["latest_start"] or "9999", x["id"])):
        if not _bad(a["status"]):
            continue
        chain, cur = [a["id"]], a["id"]
        while bp[cur]["driven_by"] and not bp[cur]["driven_by"].startswith("deadline:"):
            cur = bp[cur]["driven_by"]
            chain.append(cur)
        rule = g[cur]["deadline_rule"]
        dl = g[cur]["deadline_date"]
        keys = list(dict.fromkeys(g[x]["key"] for x in chain))
        lts = [f"{k} = {lead.get(k, {}).get('value', '?')} WD (PROVISIONAL ASSUMPTION; owner {lead.get(k, {}).get('owner', '?')})"
               for k in keys]
        options = []
        if a["status"].startswith("DEADLINE PASSED"):
            own = _d(a.get("deadline_date"))
            short = cal.working_days_between(own, sd) if own else None
            options.append(f"none by planning: {a.get('deadline_rule')} = {a.get('deadline_date')} passed {short} WD before "
                           f"the status date {sd}; record whether it was done (owner {a['owner']})")
        else:
            ls = _d(a["latest_start"])
            short = cal.working_days_between(ls, sd)
            alone = []
            for k in keys:
                v0 = int(lead.get(k, {}).get("value", g[a["id"]]["duration_wd"]))
                best = next((v for v in range(v0 - 1, -1, -1) if (_ls_with(g, cal, a["id"], k, v) or date.min) >= sd), None)
                if best is None:
                    alone.append(k)
                else:
                    options.append(f"{k} <= {best} WD (now {v0}; PROVISIONAL ASSUMPTION, owner "
                                   f"{lead.get(k, {}).get('owner', '?')})")
            if alone:
                options.append(f"not enough on its own (even at 0 WD): {', '.join(alone)}")
            if rule and dl:
                n = next((n for n in range(1, short + 60) if (_ls_with(g, cal, a["id"], shift_rule=rule, shift_wd=n)
                                                              or date.min) >= sd), None)
                if n is not None:
                    options.append(f"{rule} on or after {cal.add_working_days(dl, n).isoformat()} ({n} WD later; only the "
                                   "Authority can move a pack date, e.g. after a clarification request)")
            options.append(f"start by {a['latest_start']}: already passed at the status date {sd}")
        out.append({"activity": a["id"], "name": a["name"], "status": a["status"], "resource": a.get("resource", ""),
                    "shortfall_wd": short, "latest_start": a["latest_start"], "latest_finish": a["latest_finish"],
                    "status_date": prog["status_date"], "deadline": f"{rule} = {dl.isoformat()}" if rule and dl else "",
                    "chain": chain, "lead_times": keys, "lead_time_values": lts, "would_make_feasible": options,
                    "req_ids": a["req_ids"]})
    return out


# ---------------------------------------------------------------------------------------------- extend

def extend(prog: dict, evidence_items: dict, assumptions: dict, cal: Calendar) -> dict:
    """The stage programme with documents, resources, drivers and an extended marshalling plan. Pure."""
    out = copy.deepcopy(prog)
    for a in out["activities"]:
        a.setdefault("evidence_items", [a.get("evidence")])
        if not a.get("envelope"):
            a["envelope"] = getattr(evidence_items.get(a.get("evidence")), "envelope", "")
        a.setdefault("resource", "")
        a.setdefault("deadline_date", (out.get("deadlines") or {}).get(a.get("deadline_rule"), {}).get("date"))
    out["documents"] = documents(out, evidence_items, assumptions)
    out["marshalling"] = marshalling(out, out["documents"])
    out["resources"] = resources(out, assumptions, cal)
    out["drivers"] = drivers(out, assumptions, cal)
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
            "physical_A": tot.get("A", {}).get("physical_count"), "physical_B": tot.get("B", {}).get("physical_count"),
            "overloads": sorted(f"{r['resource']} {r['iso_week']} ({r['peak_concurrent']}/{r['capacity']})"
                                for r in (p.get("resources") or {}).get("rows", []) if r["status"].startswith("OVERLOAD"))}


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
                     "latest_start_base": x["latest_start"] if x else None, "latest_start": y["latest_start"] if y else None,
                     "latest_finish_base": x["latest_finish"] if x else None, "latest_finish": y["latest_finish"] if y else None,
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
    stage) the way stage2.a5_all does (status date = the stage's issue date; anchor = its PDD). When the
    assumptions give another calendar or counting policy, the register's dates are re-evaluated with it, so a
    declared holiday also moves pack dates counted in Working Days (e.g. the clarification cut-off)."""
    from .register import Register
    stage = stage or r["validated"].stage
    s = next(x for x in r["stages"] if x.stage == stage)
    status_date = date.fromisoformat(s.issued)
    cache: dict = {}

    def make_plan(a: dict) -> dict:
        cal = calendar_from_config(a.get("calendar"))
        policy = (a.get("planning") or {}).get("counting_policy", "conservative")
        if cal == r["cal"] and policy == r["policy"]:
            evals = r["evals"]
        else:
            if (cal, policy) not in cache:
                cache[(cal, policy)] = Register(r["rowfile"], r["stages"], cal, policy).all()
            evals = cache[(cal, policy)]
        pdd = next((d["anchor_value"] for e in evals for d in e["stages"][stage]["dates"] if d["anchor"] == "PDD"), None)
        prog = plan(stage, evals, r["templates"], a, cal, status_date, {"PDD": pdd}, evidence_items=r["evidence_items"])
        return extend(prog, r["evidence_items"], a, cal) if extended else prog

    return make_plan


# ---------------------------------------------------------------------------------------------- write

PROGRAMME_COLS = ("id", "name", "evidence", "envelope", "req_ids", "owner", "resource", "issuer", "duration_wd",
                  "duration_assumption", "duration_basis", "multiplicity", "count", "predecessors", "driven_by",
                  "latest_start", "latest_finish", "deadline", "status", "flags")
MARSHALLING_COLS = ("item", "envelope", "evidence", "issuer", "owner", "resource", "count", "multiplicity",
                    "marked_originals", "hard_copies", "physical_count", "electronic_copy", "lead_time_wd",
                    "lead_time_assumption", "drop_dead_start", "needed_by", "status", "activity", "req_ids", "flags")
DOCUMENT_COLS = ("evidence", "name", "envelope", "kind", "issuer", "per", "multiplicity", "multiplicity_basis",
                 "marked_originals", "hard_copies", "physical_count", "electronic_copy", "usb", "req_ids",
                 "activities", "source", "flags")
RESOURCE_COLS = ("resource", "iso_week", "week_start", "week_end", "days_loaded", "peak_concurrent", "capacity", "status",
                 "overloaded_days", "activities", "capacity_basis", "capacity_owner")
DRIVER_COLS = ("activity", "status", "shortfall_wd", "latest_start", "latest_finish", "status_date", "deadline", "chain",
               "lead_time_values", "would_make_feasible", "resource", "req_ids")
SCENARIO_COLS = ("id", "name", "resource", "duration_assumption", "duration_wd_base", "duration_wd", "count_base", "count",
                 "latest_start_base", "latest_start", "latest_finish_base", "latest_finish", "shift_wd", "status_base",
                 "status", "change")
COMPARISON_COLS = ("scenario", "purpose", "hypothetical", "overrides", "activities_moved", "latest_start_shift_wd",
                   "status_changes", "infeasible_base", "infeasible", "deadline_passed_base", "deadline_passed",
                   "physical_A_base", "physical_A", "physical_B_base", "physical_B", "document_changes",
                   "overloads_base", "overloads", "resource_changes", "drivers")


def _table(cols, rows, **extra) -> dict:
    return {"columns": [{"key": k, "header": k, "width": 20} for k in cols],
            "rows": [{k: r.get(k) for k in cols} for r in rows], "notice": NOTICE, **extra}


def write(prog_ext: dict, scenarios_result: dict | None, out_dir: Path) -> list[Path]:
    """Deterministic A5 tables (no timestamps) under out_dir/a5/."""
    a5 = Path(out_dir) / "a5"
    meta = {"stage": prog_ext["stage"], "status_date": prog_ext["status_date"], "anchors": prog_ext["anchors"]}
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
    paths += write_csv_json(_table(RESOURCE_COLS, res["rows"], **meta, roles=res["roles"], notes=res["notes"]),
                            a5, "resources")
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
    return paths
