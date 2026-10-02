"""A5: bid programme and marshalling plan, generated from A1 rows (never typed).

For one stage of the amendment path:
  1. every A1 row that is in force at that stage contributes its evidence items (EV-...);
  2. each evidence item expands into activities from curation/activity_templates.yaml; each activity
     carries the ids of the A1 rows that need it, an owner, a resource role, an issuer, a duration that is a
     named ASSUMPTION from config/assumptions.yaml (value, basis, owner), a multiplicity (`per`: member,
     signatory, reference, epc_contractor, om_operator, from the bidder settings) and its dependencies;
  3. a backward pass in Working Days (tenderpack.dates calendar) from the pack's own dates:
     the Proposal Due Date as amended at that stage, and any pack deadline an activity must meet
     (e.g. the clarification cut-off), using the planning interpretation of each date rule (D4);
     latest finish = min(own deadline, latest start of each successor - 1 Working Day), except that a
     successor of 0 Working Days (done at the end of a day, e.g. sealing) does not take a day of its own:
     its predecessor may finish the same day;
     latest start = latest finish - (duration - 1) Working Days (= latest finish for 0 or 1);
     `driven_by` records what set the latest finish (a successor, or the activity's own deadline);
  4. flags: INFEASIBLE by n Working Days when the latest start is before the status date (never
     compressed), DEADLINE PASSED when the activity's own pack deadline is already before the status date
     (a person records whether it was done), plus the requirement flags
     (STALE interpretation, image reading pending) carried from the rows.
Deltas between consecutive stages: NEW, REMOVED, MOVED (latest start changed), REWORK (the
requirement behind an activity changed: work done against the earlier version may need redoing).

Both directions are checked (failures are returned in `problems` and are structural in the build):
  C40 every activity cites at least one row in force (an activity needs a requirement)
  C44 every evidence item a row in force needs has activities, or a justified exception in the templates
      file (`_exceptions: {EV-ID: reason}`) (a required deliverable needs an activity)
  C45 every dependency names an activity that some template defines, every duration names a lead-time
      assumption, every activity names a resource role defined in the assumptions and a known multiplicity,
      and an activity listed under two evidence items is defined identically; a dependency on an activity
      that exists but is not needed at this stage is shown on the activity ("not required at this stage"),
      never silently dropped
Documents, resources, drivers and scenarios are built on this output by tenderpack.programme.
"""
from __future__ import annotations

from datetime import date

from .dates import Calendar

IN_FORCE_PREFIXES = ("ACTIVE", "AMENDED", "REINSTATED", "NEW")

# evidence-vocabulary `per` -> the bidder settings (config/assumptions.yaml bidder:) whose product it is
PER = {
    "proposal": (), "lead_member": (),
    "member": ("members",),
    "signatory": ("members", "signatories_per_member"),
    "reference": ("reference_plants_offered",),
    "epc_contractor": ("epc_contractors",),
    "om_operator": ("om_operators",),
}


def in_force(status: str) -> bool:
    return status.startswith(IN_FORCE_PREFIXES)


def multiplicity(per: str | None, bidder: dict) -> tuple[int, str]:
    """How many `per` means, from the bidder settings (ASSUMPTIONS), and how it was computed:
    (1, "") for one per proposal; (3, "bidder.members = 3") for 'member'. A `per` that is itself a bidder
    setting (older templates: 'members') is accepted. KeyError for an unknown `per` or a missing setting."""
    if not per:
        return 1, ""
    keys = PER.get(per)
    if keys is None:
        if per in bidder and not isinstance(bidder[per], str):
            keys = (per,)
        else:
            raise KeyError(f"unknown multiplicity per '{per}' (known: {', '.join(PER)})")
    n = 1
    for k in keys:
        if k not in bidder:
            raise KeyError(f"bidder setting '{k}' (needed for per '{per}') is not in the assumptions")
        n *= int(bidder[k])
    return n, " x ".join(f"bidder.{k} = {bidder[k]}" for k in keys)


def multiplicity_label(per: str | None, bidder: dict) -> str:
    n, expr = multiplicity(per, bidder)
    return f"x{n} (per {per}: {expr}; PROVISIONAL ASSUMPTION)" if expr else ""


def duration_basis(lt: dict) -> str:
    """'ASSUMPTION (PROVISIONAL; owner Commercial): <basis>' for a lead-time entry."""
    b = str(lt.get("basis", "")).strip()
    for p in ("PROVISIONAL ASSUMPTION:", "ASSUMPTION:"):
        if b.startswith(p):
            b = b[len(p):].strip()
    return f"ASSUMPTION (PROVISIONAL; owner {lt.get('owner', '?')}): {b}"


def backward_pass(acts: dict[str, dict], cal: Calendar) -> dict[str, dict]:
    """acts: id -> {"duration_wd": int, "predecessors": [ids in acts], "deadline_date": date | None,
    "deadline_rule": str | None}. Returns id -> {"ls", "lf" (date | None), "driven_by" (successor id,
    'deadline:<rule>' or None)}. Pure; raises ValueError on a dependency cycle."""
    succ: dict[str, list[str]] = {k: [] for k in acts}
    for k, a in acts.items():
        for p in a["predecessors"]:
            succ[p].append(k)
    res: dict[str, dict] = {}
    visiting: set[str] = set()

    def visit(aid: str) -> dict:
        if aid in res:
            return res[aid]
        if aid in visiting:
            raise ValueError(f"dependency cycle at {aid}")
        visiting.add(aid)
        a = acts[aid]
        cands = []
        if a.get("deadline_date") is not None:
            cands.append((a["deadline_date"], 0, f"deadline:{a.get('deadline_rule')}"))
        for s in sorted(succ[aid]):
            st = visit(s)["ls"]
            if st is not None:
                cands.append((st if acts[s]["duration_wd"] == 0 else cal.add_working_days(st, -1), 1, s))
        lf, _, drv = min(cands) if cands else (None, 0, None)
        d = int(a["duration_wd"])
        ls = None if lf is None else (cal.add_working_days(lf, -(d - 1)) if d > 1 else lf)
        visiting.discard(aid)
        res[aid] = {"ls": ls, "lf": lf, "driven_by": drv}
        return res[aid]

    for k in sorted(acts):
        visit(k)
    return res


def check_templates(templates: dict, assumptions: dict) -> list[str]:
    """C45 problems of the templates file against the assumptions (independent of any stage)."""
    problems: list[str] = []
    lead = assumptions.get("lead_times") or {}
    roles = assumptions.get("resources")
    bidder = assumptions.get("bidder") or {}
    defined = {t["id"] for item, ts in templates.items() if not item.startswith("_") for t in (ts or [])}
    seen: dict[str, tuple[str, dict]] = {}
    for item, ts in templates.items():
        if item.startswith("_"):
            continue
        for t in ts or []:
            for dep in list(t.get("predecessors", [])) + list(t.get("successors", [])):
                if dep not in defined:
                    problems.append(f"C45: activity {t['id']} ({item}) depends on unknown activity '{dep}'")
            if t.get("duration") not in lead:
                problems.append(f"C45: activity {t['id']} ({item}) uses an unknown lead-time assumption '{t.get('duration')}'")
            if not t.get("resource"):
                problems.append(f"C45: activity {t['id']} ({item}) names no resource role")
            elif roles is not None and t["resource"] not in roles:
                problems.append(f"C45: activity {t['id']} ({item}) names resource '{t['resource']}', which is not a role "
                                f"in the assumptions (resources:)")
            try:
                multiplicity(t.get("per"), bidder)
            except KeyError as e:
                problems.append(f"C45: activity {t['id']} ({item}): {e.args[0]}")
            if t["id"] in seen and seen[t["id"]][1] != t:
                problems.append(f"C45: activity {t['id']} is defined differently under {seen[t['id']][0]} and {item}")
            seen.setdefault(t["id"], (item, t))
    for k, v in lead.items():
        try:
            if int(v["value"]) < 0 or int(v["value"]) != v["value"]:
                raise ValueError
        except (KeyError, TypeError, ValueError):
            problems.append(f"C45: lead-time assumption '{k}' has no whole, non-negative number of Working Days")
    return problems


def plan(stage: str, evals: list[dict], templates: dict, assumptions: dict, cal: Calendar, status_date: date,
         anchors: dict, evidence_items: dict | None = None) -> dict:
    """evals: [{"row": Row, "stages": {stage: evaluation}}] from register.Register.all().
    evidence_items (optional): the evidence vocabulary (evidence.load_evidence_items), for each activity's envelope."""
    need: dict[str, list[str]] = {}
    row_flags: dict[str, list[str]] = {}
    deadlines: dict[str, tuple[str, str]] = {}            # rule_id -> (date, row id)
    for e in evals:
        row, ev = e["row"], e["stages"][stage]
        if not in_force(ev["status"]):
            continue
        for item in row.evidence:
            need.setdefault(item, []).append(row.id)
        fl = []
        if ev["stale"]:
            fl.append("REQUIREMENT STALE")
        if ev["transcription"] == "pending":
            fl.append("IMAGE READING PENDING")
        row_flags[row.id] = fl
        for d in ev["dates"]:
            if d["planning"]["value"]:
                deadlines[d["rule_id"]] = (d["planning"]["value"], row.id)
    exceptions = templates.get("_exceptions") or {}
    defined = {t["id"] for item, ts in templates.items() if not item.startswith("_") for t in (ts or [])}
    problems = check_templates(templates, assumptions)
    missing = [i for i in sorted(need) if not templates.get(i) and not (exceptions.get(i) or "").strip()]
    for item in missing:
        problems.append(f"C44: {item} is needed by {', '.join(need[item])} (in force at {stage}) but has no "
                        f"activities and no justified exception")
    lead = assumptions.get("lead_times") or {}
    bidder = assumptions.get("bidder") or {}
    acts: dict[str, dict] = {}
    for item in sorted(need):
        for t in templates.get(item) or []:
            if t.get("duration") not in lead:
                continue
            try:
                count, _ = multiplicity(t.get("per"), bidder)
            except KeyError:
                continue                                     # reported by check_templates (C45)
            lt = lead[t["duration"]]
            env = getattr((evidence_items or {}).get(item), "envelope", "") if evidence_items else ""
            a = acts.setdefault(t["id"], {
                "id": t["id"], "name": t["name"], "evidence": item, "evidence_items": [], "envelope": env,
                "owner": t["owner"], "resource": t.get("resource", ""), "issuer": t["issuer"],
                "duration_wd": int(lt["value"]), "duration_assumption": t["duration"],
                "duration_basis": duration_basis(lt), "per": t.get("per") or "proposal", "count": count,
                "multiplicity": multiplicity_label(t.get("per"), bidder), "item": t.get("item", ""),
                "predecessors": list(t.get("predecessors", [])), "successors": list(t.get("successors", [])),
                "deadline_rule": (t.get("finish") or {}).get("deadline_of"), "req_ids": []})
            a["req_ids"] = sorted(set(a["req_ids"]) | set(need[item]))
            a["evidence_items"] = sorted(set(a["evidence_items"]) | {item})
    # links: predecessors declared on the successor, successors declared on the predecessor
    for a in acts.values():
        a["not_required_here"] = sorted({p for p in a["predecessors"] + a["successors"] if p not in acts and p in defined})
        a["predecessors"] = [p for p in a["predecessors"] if p in acts]
    for a in acts.values():
        for s in a.pop("successors"):
            if s in acts and a["id"] not in acts[s]["predecessors"]:
                acts[s]["predecessors"].append(a["id"])
    for a in acts.values():
        a["predecessors"] = sorted(a["predecessors"])
        rule = a["deadline_rule"]
        a["deadline_date"] = deadlines[rule][0] if rule in deadlines else None
    bp = backward_pass({k: {"duration_wd": a["duration_wd"], "predecessors": a["predecessors"],
                            "deadline_rule": a["deadline_rule"],
                            "deadline_date": date.fromisoformat(a["deadline_date"]) if a["deadline_date"] else None}
                        for k, a in acts.items()}, cal)
    rows = []
    for aid in sorted(acts, key=lambda k: (bp[k]["ls"] or date.max, k)):
        a = acts[aid]
        s, f = bp[aid]["ls"], bp[aid]["lf"]
        flags = []
        own = deadlines.get(a["deadline_rule"]) if a["deadline_rule"] else None
        if f is None:
            flags.append("NO DEADLINE REACHED (not linked to a pack date)")
        elif own is not None and date.fromisoformat(own[0]) < status_date:
            flags.append(f"DEADLINE PASSED ({a['deadline_rule']} = {own[0]} is before the status date "
                         f"{status_date.isoformat()}; record whether it was done)")
        elif s is not None and s < status_date:
            short = cal.working_days_between(s, status_date)
            flags.append(f"INFEASIBLE by {short} WD (latest start {s.isoformat()} is before the status date "
                         f"{status_date.isoformat()}; not compressed)")
        for r in a["req_ids"]:
            flags += [f"{x} ({r})" for x in row_flags.get(r, [])]
        flags += [f"dependency '{d}' not required at this stage" for d in a.pop("not_required_here")]
        rows.append({**a, "latest_start": s.isoformat() if s else None, "latest_finish": f.isoformat() if f else None,
                     "driven_by": bp[aid]["driven_by"],
                     "deadline": (f"{a['deadline_rule']} = {deadlines[a['deadline_rule']][0]} (from {deadlines[a['deadline_rule']][1]})"
                                  if a["deadline_rule"] in deadlines else ""),
                     "flags": flags, "status": "OK" if not any(x.startswith(("INFEASIBLE", "DEADLINE PASSED", "NO DEADLINE"))
                                                               for x in flags) else flags[0].split(" (")[0]})
    marshalling = [{"item": r["item"], "envelope": r["envelope"], "evidence": r["evidence"], "issuer": r["issuer"],
                    "owner": r["owner"], "resource": r["resource"], "lead_time_wd": r["duration_wd"],
                    "lead_time_assumption": r["duration_assumption"], "multiplicity": r["multiplicity"],
                    "count": r["count"], "drop_dead_start": r["latest_start"], "needed_by": r["latest_finish"],
                    "activity": r["id"], "status": r["status"], "req_ids": r["req_ids"], "flags": r["flags"]}
                   for r in rows if r["item"]]
    return {"stage": stage, "status_date": status_date.isoformat(), "anchors": anchors, "activities": rows,
            "marshalling": marshalling, "problems": problems,
            "exceptions": {k: v for k, v in exceptions.items() if k in need},
            "evidence_needed": {k: sorted(v) for k, v in sorted(need.items())},
            "deadlines": {k: {"date": v[0], "row": v[1]} for k, v in sorted(deadlines.items())}}


def deltas(prev: dict, cur: dict, prev_evals: dict, cur_evals: dict) -> list[dict]:
    """NEW / REMOVED / MOVED / REWORK between the programme of two stages."""
    p = {a["id"]: a for a in prev["activities"]}
    c = {a["id"]: a for a in cur["activities"]}
    out = []
    for k in sorted(set(p) | set(c)):
        if k not in p:
            out.append({"activity": k, "change": "NEW", "detail": f"needed by {', '.join(c[k]['req_ids'])}"})
            continue
        if k not in c:
            out.append({"activity": k, "change": "REMOVED", "detail": f"no longer needed by any row in force"})
            continue
        changed_rows = [r for r in c[k]["req_ids"] if r in prev_evals and r in cur_evals and
                        (prev_evals[r]["interpretation"] != cur_evals[r]["interpretation"] or
                         [d["planning"] for d in prev_evals[r]["dates"]] != [d["planning"] for d in cur_evals[r]["dates"]])]
        if changed_rows:
            out.append({"activity": k, "change": "REWORK", "detail": f"requirement changed: {', '.join(changed_rows)}"})
        if p[k]["latest_start"] != c[k]["latest_start"]:
            out.append({"activity": k, "change": "MOVED", "detail": f"latest start {p[k]['latest_start']} -> {c[k]['latest_start']}"})
    return out
