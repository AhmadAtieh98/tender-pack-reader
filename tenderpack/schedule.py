"""A5: bid programme and marshalling plan, generated from A1 rows (never typed).

For one stage of the amendment path:
  1. every A1 row that is in force at that stage contributes its evidence items (EV-...);
  2. each evidence item expands into activities from curation/activity_templates.yaml; each activity
     carries the ids of the A1 rows that need it, an owner, an issuer, a duration that is a named
     ASSUMPTION from config/assumptions.yaml (value, basis, owner), and its dependencies;
  3. a backward pass in Working Days (tenderpack.dates calendar) from the pack's own dates:
     the Proposal Due Date as amended at that stage, and any pack deadline an activity must meet
     (e.g. the clarification cut-off), using the planning interpretation of each date rule (D4);
     latest finish = min(own deadline, latest start of successors - 1 Working Day);
     latest start = latest finish - (duration - 1) Working Days;
  4. flags: INFEASIBLE by n Working Days when the latest start is before the status date (never
     compressed), DEADLINE PASSED when the activity's own pack deadline is already before the status date
     (a person records whether it was done), plus the requirement flags
     (STALE interpretation, image reading pending) carried from the rows.
Deltas between consecutive stages: NEW, REMOVED, MOVED (latest start changed), REWORK (the
requirement behind an activity changed: work done against the earlier version may need redoing).
"""
from __future__ import annotations

from datetime import date

from .dates import Calendar

IN_FORCE_PREFIXES = ("ACTIVE", "AMENDED", "REINSTATED", "NEW")


def in_force(status: str) -> bool:
    return status.startswith(IN_FORCE_PREFIXES)


def plan(stage: str, evals: list[dict], templates: dict, assumptions: dict, cal: Calendar, status_date: date,
         anchors: dict) -> dict:
    """evals: [{"row": Row, "stages": {stage: evaluation}}] from register.Register.all()."""
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
    acts: dict[str, dict] = {}
    for item in sorted(need):
        for t in templates.get(item, []):
            lt = assumptions["lead_times"][t["duration"]]
            per = t.get("per")
            mult = assumptions["bidder"].get(per) if per else None
            a = acts.setdefault(t["id"], {
                "id": t["id"], "name": t["name"], "evidence": item, "owner": t["owner"], "issuer": t["issuer"],
                "duration_wd": int(lt["value"]), "duration_assumption": t["duration"],
                "duration_basis": f"ASSUMPTION ({lt['owner']}): {lt['basis']}",
                "multiplicity": f"x{mult} ({per}, assumption)" if per else "", "item": t.get("item", ""),
                "predecessors": list(t.get("predecessors", [])), "successors": list(t.get("successors", [])),
                "deadline_rule": (t.get("finish") or {}).get("deadline_of"), "req_ids": []})
            a["req_ids"] = sorted(set(a["req_ids"]) | set(need[item]))
    # links: predecessors declared on the successor, successors declared on the predecessor
    for a in acts.values():
        a["predecessors"] = [p for p in a["predecessors"] if p in acts]
    for a in acts.values():
        for s in a.pop("successors"):
            if s in acts and a["id"] not in acts[s]["predecessors"]:
                acts[s]["predecessors"].append(a["id"])
    succ: dict[str, list[str]] = {k: [] for k in acts}
    for a in acts.values():
        for p in a["predecessors"]:
            succ[p].append(a["id"])
    # backward pass (memoised; the graph is small and acyclic by construction)
    lf: dict[str, date | None] = {}
    ls: dict[str, date | None] = {}

    def finish(aid: str, seen=()) -> date | None:
        if aid in lf:
            return lf[aid]
        if aid in seen:
            raise ValueError(f"dependency cycle at {aid}")
        a = acts[aid]
        cands = []
        if a["deadline_rule"] and a["deadline_rule"] in deadlines:
            cands.append(date.fromisoformat(deadlines[a["deadline_rule"]][0]))
        for s in succ[aid]:
            st = start(s, seen + (aid,))
            if st is not None:
                cands.append(cal.add_working_days(st, -1))
        lf[aid] = min(cands) if cands else None
        return lf[aid]

    def start(aid: str, seen=()) -> date | None:
        if aid in ls:
            return ls[aid]
        f = finish(aid, seen)
        ls[aid] = None if f is None else (cal.add_working_days(f, -(acts[aid]["duration_wd"] - 1))
                                          if acts[aid]["duration_wd"] > 1 else f)
        return ls[aid]

    rows = []
    for aid in sorted(acts, key=lambda k: (start(k) or date.max, k)):
        a = acts[aid]
        s, f = start(aid), finish(aid)
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
        rows.append({**a, "latest_start": s.isoformat() if s else None, "latest_finish": f.isoformat() if f else None,
                     "deadline": (f"{a['deadline_rule']} = {deadlines[a['deadline_rule']][0]} (from {deadlines[a['deadline_rule']][1]})"
                                  if a["deadline_rule"] in deadlines else ""),
                     "flags": flags, "status": "OK" if not any(x.startswith(("INFEASIBLE", "DEADLINE PASSED", "NO DEADLINE"))
                                                               for x in flags) else flags[0].split(" (")[0]})
    marshalling = [{"item": r["item"], "issuer": r["issuer"], "owner": r["owner"], "lead_time_wd": r["duration_wd"],
                    "lead_time_assumption": r["duration_assumption"], "multiplicity": r["multiplicity"],
                    "drop_dead_start": r["latest_start"], "needed_by": r["latest_finish"], "activity": r["id"],
                    "req_ids": r["req_ids"], "flags": r["flags"]} for r in rows if r["item"]]
    return {"stage": stage, "status_date": status_date.isoformat(), "anchors": anchors, "activities": rows,
            "marshalling": marshalling}


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
