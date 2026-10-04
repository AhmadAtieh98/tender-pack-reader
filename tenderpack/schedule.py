"""A5: bid programme and marshalling plan, generated from A1 rows (never typed).

For one stage of the amendment path:
  1. every A1 row that is in force at that stage contributes its evidence items (EV-...);
  2. each evidence item expands into activities from curation/activity_templates.yaml; each activity
     carries the ids of the A1 rows that need it, an owner, a discipline, a resource role, an issuer, a duration
     that is a named ASSUMPTION from config/assumptions.yaml (elapsed value, staff effort `effort_wd`, the external
     party it waits on `waiting_on`, basis, owner), a multiplicity (`per`: member, foreign_member, signatory,
     reference, epc_contractor, om_operator, from the bidder settings) and its dependencies;
  3. planning basis: the planning (status) date is the stage's addendum issue date (the latest addendum of the
     stage). A FORWARD pass in Working Days (tenderpack.dates calendar, VOL-I 2.4) from the first Working Day on
     or after it gives the earliest start and finish of every activity (ES = the Working Day after the latest
     predecessor finish; an activity of 0 Working Days is done at the end of its predecessor's day);
     a BACKWARD pass from the pack's own dates gives the latest ones: the Proposal Due Date as amended at that
     stage, and any pack deadline an activity must meet (e.g. the clarification cut-off), using the planning
     interpretation of each date rule (D4);
     latest finish = min(own deadline, latest start of each successor - 1 Working Day), except that a
     successor of 0 Working Days (done at the end of a day, e.g. sealing) does not take a day of its own:
     its predecessor may finish the same day;
     latest start = latest finish - (duration - 1) Working Days (= latest finish for 0 or 1);
     work happens on Working Days only: when a pack deadline falls on a weekend day or a declared holiday, the
     latest finish is the last Working Day before it. The legal deadline itself is never moved: it is kept on
     the activity (`deadline`) and flagged DEADLINE ON A NON-WORKING DAY (session 08);
     `driven_by` records what set the latest finish (a successor, or the activity's own deadline), `es_driven_by`
     what set the earliest start (a predecessor, or the planning date);
     total float = Working Days from the earliest start to the latest start;
  4. three SEPARATE statuses per activity:
     timing_status (= `status`, read by stage2): from window_flags: INFEASIBLE by n WD when the total float is -n
     (never compressed; the shortfall runs along the whole chain), DEADLINE PASSED when the activity's own pack
     deadline is already before the planning date (a person records whether it was done), CONDITIONAL — window
     elapsed ... when that activity is conditional (`condition` in its template: an elapsed window alone does not
     establish a missed duty), NO WORKING WINDOW when the deadline has not passed but no Working Day is left on or
     before it (an explicit conflict for a person; nothing is moved), NO DEADLINE REACHED, NOT NEEDED (count 0
     under the assumed bidder), or OK; plus the requirement flags (STALE interpretation, image reading pending);
     decision_status: READY, or GATED when the template's `gated_by` names open issues: the finalising step waits
     for a person's decision, which is needed by the activity's latest start; preparation is never gated;
     resource_status: OK, OVERLOAD <role> on <dates> (load vs capacity), or NOT LOADED (why). Load per role per
     Working Day = each activity's staff effort (effort_wd x multiplicity) spread evenly over its LATE window
     (latest start..latest finish, clipped at the planning date). Resource levelling is NOT implemented:
     overloads are reported, not resolved.
Deltas between consecutive stages: NEW, REMOVED, MOVED (latest start changed), REWORK (the
requirement behind an activity changed — its interpretation, dates, wording, cells, or it became STALE:
work done against the earlier version may need redoing).

Both directions are checked (failures are returned in `problems` and are structural in the build):
  C40 every activity cites at least one row in force (an activity needs a requirement)
  C44 every evidence item a row in force needs has activities, or a justified exception in the templates
      file (`_exceptions: {EV-ID: reason}`) (a required deliverable needs an activity)
  C45 every dependency names an activity that some template defines, every duration names a lead-time
      assumption, every activity names a resource role defined in the assumptions, a known multiplicity and (if
      given) a known discipline, and an activity listed under two evidence items is defined identically; a
      dependency on an activity that exists but is not needed at this stage is shown on the activity ("not
      required at this stage"), never silently dropped; a pack fact typed as an assumption
      (`planning.delivery_cutoff_time`) or a time or date typed into an activity's name or item is refused
Pack facts in names and labels are never typed (session 09). The Proposal Due Date's date, time of day, timezone
label and source come from the effective text of the anchor's defining unit at the stage (register.anchor_details,
computed by stage2.evaluate; plan() reads them from the A1 evaluations when a caller passes none). Template strings
take placeholders, filled deterministically at plan time (`fill`):
  activity `name` / `item`   {PDD_TIME} {PDD_TZ} {PDD_DATE} {PDD_SOURCE} (any anchor: {<ANCHOR>_TIME} ...) and
                             {ROW:<row id>:<parameter>}: the named `parameters` value of that row's interpretation
                             at the stage (e.g. {ROW:VOL-I-App3-01:marking}, the Appendix 3 envelope marking)
  `_milestones.labels` of an anchor milestone   {time} {tz} {date} {source} of that anchor (and the above)
An unknown placeholder, or one the stage does not state (no time in the text, a row not in force, a missing
parameter), is a C45 problem and is left as written: "None" is never printed.
Documents, resources, drivers and scenarios are built on this output by tenderpack.programme; the Gantt by
tenderpack.gantt.
"""
from __future__ import annotations

import re
from datetime import date, timedelta
from types import SimpleNamespace

from .dates import _DATE, _TIME, Calendar, parse_date

IN_FORCE_PREFIXES = ("ACTIVE", "AMENDED", "REINSTATED", "NEW")
# flags that set the timing status (the first one found, up to " (", is `status`)
BLOCKING_FLAGS = ("INFEASIBLE", "DEADLINE PASSED", "NO DEADLINE", "NO WORKING WINDOW", "CONDITIONAL —", "NOT NEEDED")
NOT_SCHEDULED = ("DEADLINE PASSED", "CONDITIONAL", "NOT NEEDED")      # timing statuses whose work is not loaded
DISCIPLINES = ("Legal", "Commercial", "Technical", "Bid management", "Document control")
NO_LEVELLING = "resource levelling is NOT implemented; overloads are reported, not resolved"
LOAD_WINDOW = ("late: each activity's staff effort (effort_wd x multiplicity) is spread evenly over the Working Days of "
               "its late window, latest start..latest finish, clipped at the planning date (as late as possible)")

# evidence-vocabulary `per` -> the bidder settings (config/assumptions.yaml bidder:) whose product it is
PER = {
    "proposal": (), "lead_member": (),
    "member": ("members",),
    "foreign_member": ("foreign_members",),
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


def _strip(b: str) -> str:
    b = str(b or "").strip()
    for p in ("PROVISIONAL ASSUMPTION:", "ASSUMPTION:"):
        if b.startswith(p):
            b = b[len(p):].strip()
    return b


def duration_basis(lt: dict) -> str:
    """'ASSUMPTION (PROVISIONAL; owner Commercial): <basis>' for a lead-time entry."""
    return f"ASSUMPTION (PROVISIONAL; owner {lt.get('owner', '?')}): {_strip(lt.get('basis', ''))}"


def effort_of(lt: dict) -> tuple[float, str, str]:
    """(staff effort per unit in Working Days, external party waited on or "", labelled basis) of a lead-time entry.
    Without `effort_wd` the whole elapsed duration counts as staff effort (the conservative default)."""
    waiting = str(lt.get("waiting_on") or "").strip()
    if "effort_wd" in lt and lt["effort_wd"] is not None:
        eff = float(lt["effort_wd"])
        eff = int(eff) if eff == int(eff) else eff
        b = _strip(lt.get("effort_basis", "")) or "no basis given"
    else:
        eff = int(lt.get("value", 0))
        b = "no effort_wd configured: the whole elapsed duration is counted as staff effort (conservative default)"
    return eff, waiting, (f"ASSUMPTION (PROVISIONAL; owner {lt.get('owner', '?')}): {b}; "
                          f"waits on: {waiting or 'no external party'}")


def last_working_day(cal: Calendar, d: date) -> date:
    """d itself when it is a Working Day, otherwise the last Working Day before it."""
    while not cal.is_working_day(d):
        d -= timedelta(days=1)
    return d


def first_working_day(cal: Calendar, d: date) -> date:
    """d itself when it is a Working Day, otherwise the first Working Day after it."""
    while not cal.is_working_day(d):
        d += timedelta(days=1)
    return d


def _working_days(cal: Calendar, a: date, b: date) -> list[date]:
    return [a + timedelta(days=i) for i in range((b - a).days + 1) if cal.is_working_day(a + timedelta(days=i))]


def backward_pass(acts: dict[str, dict], cal: Calendar) -> dict[str, dict]:
    """acts: id -> {"duration_wd": int, "predecessors": [ids in acts], "deadline_date": date | None,
    "deadline_rule": str | None}. Returns id -> {"ls", "lf" (Working Days or None), "driven_by" (successor id,
    'deadline:<rule>' or None), "deadline" (the legal deadline, unchanged), "deadline_nonworking"}.
    Pure; raises ValueError on a dependency cycle."""
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
        legal = a.get("deadline_date")
        if legal is not None:
            cands.append((last_working_day(cal, legal), 0, f"deadline:{a.get('deadline_rule')}"))
        for s in sorted(succ[aid]):
            st = visit(s)["ls"]
            if st is not None:
                cands.append((st if acts[s]["duration_wd"] == 0 else cal.add_working_days(st, -1), 1, s))
        lf, _, drv = min(cands) if cands else (None, 0, None)
        d = int(a["duration_wd"])
        ls = None if lf is None else (cal.add_working_days(lf, -(d - 1)) if d > 1 else lf)
        visiting.discard(aid)
        res[aid] = {"ls": ls, "lf": lf, "driven_by": drv, "deadline": legal,
                    "deadline_nonworking": legal is not None and not cal.is_working_day(legal)}
        return res[aid]

    for k in sorted(acts):
        visit(k)
    return res


def forward_pass(acts: dict[str, dict], cal: Calendar, start: date) -> dict[str, dict]:
    """acts as for backward_pass. Earliest dates from the first Working Day on or after `start` (the planning date):
    ES = max(that day, the Working Day after each predecessor's earliest finish; for an activity of 0 Working Days,
    the predecessor's finish day itself); EF = ES + (duration - 1) Working Days (= ES for 0 or 1).
    Returns id -> {"es", "ef", "es_driven_by" (predecessor id or 'planning date')}. Pure; ValueError on a cycle."""
    day0 = first_working_day(cal, start)
    res: dict[str, dict] = {}
    visiting: set[str] = set()

    def visit(aid: str) -> dict:
        if aid in res:
            return res[aid]
        if aid in visiting:
            raise ValueError(f"dependency cycle at {aid}")
        visiting.add(aid)
        d = int(acts[aid]["duration_wd"])
        cands = [(day0, 0, "planning date")]
        for p in sorted(acts[aid]["predecessors"]):
            pf = visit(p)["ef"]
            cands.append((pf if d == 0 else cal.add_working_days(pf, 1), 1, p))
        es, _, drv = max(cands)
        visiting.discard(aid)
        res[aid] = {"es": es, "ef": cal.add_working_days(es, d - 1) if d > 1 else es, "es_driven_by": drv}
        return res[aid]

    for k in sorted(acts):
        visit(k)
    return res


def network(acts: dict[str, dict], cal: Calendar, start: date) -> dict[str, dict]:
    """Forward and backward pass together: id -> {es, ef, es_driven_by, ls, lf, driven_by, deadline,
    deadline_nonworking, float_wd} where float_wd = Working Days from ES to LS (None without a latest start)."""
    fw, bw = forward_pass(acts, cal, start), backward_pass(acts, cal)
    out = {}
    for k in sorted(acts):
        b, f = bw[k], fw[k]
        out[k] = {**b, **f, "float_wd": None if b["ls"] is None else cal.working_days_between(f["es"], b["ls"])}
    return out


def window_flags(t: dict, status_date: date, cal: Calendar) -> list[str]:
    """Timing flags of one activity from its pass results. The legal deadline is quoted, never moved. With a
    forward pass (`float_wd`), INFEASIBLE means negative total float; without one, a latest start before the
    status date. A `condition` turns an elapsed window into CONDITIONAL, never a missed duty."""
    s, f, legal = t["ls"], t["lf"], t.get("deadline")
    cond = str(t.get("condition") or "").strip()
    flags = []
    if f is None:
        return ["NO DEADLINE REACHED (not linked to a pack date)"]
    if t.get("deadline_nonworking"):
        flags.append(f"DEADLINE ON A NON-WORKING DAY (legal deadline {legal.isoformat()} ({legal.strftime('%a')}) "
                     f"kept; the work must finish by {f.isoformat()}, the last Working Day before it)")
    fl = t.get("float_wd")
    if legal is not None and legal < status_date and cond:
        flags.insert(0, f"CONDITIONAL — window elapsed {legal.isoformat()}; whether the condition arose is not known "
                        f"({t.get('rule') or 'own deadline'} = {legal.isoformat()} is before the planning date "
                        f"{status_date.isoformat()}; needed only if {cond}; an elapsed window alone does not establish "
                        "a missed duty: a person records whether the condition arose and, if it did, what was done)")
        return flags
    if legal is not None and legal < status_date:
        flags.insert(0, f"DEADLINE PASSED ({t.get('rule') or 'own deadline'} = {legal.isoformat()} is before the status "
                        f"date {status_date.isoformat()}; record whether it was done)")
    elif legal is not None and str(t.get("driven_by") or "").startswith("deadline:") and f < status_date:
        flags.insert(0, f"NO WORKING WINDOW (the deadline {legal.isoformat()} has not passed, but the last Working Day "
                        f"on or before it, {f.isoformat()}, is before the status date {status_date.isoformat()}; the "
                        "legal deadline is unchanged; a person decides how to resolve the conflict)")
    elif fl is not None and fl < 0:
        why = (f"latest start {s.isoformat()} is before the planning date {status_date.isoformat()}" if s < status_date
               else f"earliest start {t['es'].isoformat()} (after {t.get('es_driven_by')}) is after the latest start "
                    f"{s.isoformat()}")
        flags.insert(0, f"INFEASIBLE by {-fl} WD (total float {fl} WD: {why}; not compressed)")
    elif fl is None and s is not None and s < status_date:
        short = cal.working_days_between(s, status_date)
        flags.insert(0, f"INFEASIBLE by {short} WD (latest start {s.isoformat()} is before the status date "
                        f"{status_date.isoformat()}; not compressed)")
    if cond:
        flags.append(f"CONDITIONAL (only if {cond})")
    return flags


def timing_status(flags: list[str]) -> str:
    return next((x for x in flags if x.startswith(BLOCKING_FLAGS)), "OK").split(" (")[0]


# ---------------------------------------------------------------------------------------------- resources

def resource_load(rows: list[dict], roles: dict, cal: Calendar, status_date: date) -> dict:
    """Staff load per role per Working Day. rows: activities with id, resource, effort_total_wd, latest_start,
    latest_finish (ISO), status. Each activity's effort is spread evenly over the Working Days of its late window
    clipped at the planning date. Not loaded: no role, no effort, no latest dates, a window wholly before the
    planning date, or a timing status that schedules no work (DEADLINE PASSED, CONDITIONAL, NOT NEEDED).
    Returns {"daily": {role: {iso: {load, capacity, over, activities: [[id, share]]}}}, "overloads": [runs of
    consecutive overloaded Working Days], "loaded": {id: {...}}, "notes", "window"}. Nothing is levelled."""
    day0 = first_working_day(cal, status_date)
    daily: dict[str, dict[date, list[tuple[str, float]]]] = {}
    loaded: dict[str, dict] = {}
    notes: list[str] = []
    for a in sorted(rows, key=lambda x: x["id"]):
        r, eff, st = a.get("resource"), float(a.get("effort_total_wd") or 0), str(a.get("status") or "OK")
        ls = date.fromisoformat(a["latest_start"]) if a.get("latest_start") else None
        lf = date.fromisoformat(a["latest_finish"]) if a.get("latest_finish") else None
        reason = None
        if not r:
            reason = "no resource role"
        elif st.startswith(NOT_SCHEDULED):
            reason = f"timing status {st.split(' —')[0]}: no work is scheduled"
        elif eff <= 0:
            reason = "no staff effort (effort 0 or count 0)"
        elif ls is None or lf is None:
            reason = "no latest dates (not linked to a pack date)"
        elif lf < day0:
            reason = f"late window {ls.isoformat()}..{lf.isoformat()} ends before the planning date (INFEASIBLE; see drivers)"
        if reason:
            loaded[a["id"]] = {"loaded": False, "reason": reason}
            notes.append(f"{a['id']}: not loaded ({reason})")
            continue
        days = _working_days(cal, max(ls, day0), lf) or [lf]
        share = eff / len(days)
        if ls < day0:
            notes.append(f"{a['id']}: late window {ls.isoformat()}..{lf.isoformat()} clipped at the planning date "
                         f"{day0.isoformat()}: {eff:g} staff WD in {len(days)} WD")
        for d in days:
            daily.setdefault(r, {}).setdefault(d, []).append((a["id"], share))
        loaded[a["id"]] = {"loaded": True, "resource": r, "days": [d.isoformat() for d in days],
                           "per_day": round(share, 3)}
    out_daily: dict[str, dict[str, dict]] = {}
    overloads: list[dict] = []
    for r in sorted(daily):
        cap = (roles.get(r) or {}).get("capacity")
        out_daily[r] = {}
        over: list[date] = []
        for d in sorted(daily[r]):
            load = round(sum(s for _, s in daily[r][d]), 3)
            is_over = cap is not None and load > cap
            out_daily[r][d.isoformat()] = {"load": load, "capacity": cap, "over": is_over,
                                           "activities": [[i, round(s, 3)] for i, s in daily[r][d]]}
            if is_over:
                over.append(d)
        runs: list[list[date]] = []
        for d in over:
            if runs and cal.add_working_days(runs[-1][-1], 1) == d:
                runs[-1].append(d)
            else:
                runs.append([d])
        for run in runs:
            ds = [d.isoformat() for d in run]
            overloads.append({"resource": r, "from": ds[0], "to": ds[-1], "dates": ds, "days": len(ds),
                              "peak_load": max(out_daily[r][x]["load"] for x in ds), "capacity": cap,
                              "activities": sorted({i for x in ds for i, _ in out_daily[r][x]["activities"]})})
    return {"daily": out_daily, "overloads": overloads, "loaded": loaded, "window": LOAD_WINDOW,
            "notes": [f"Load window: {LOAD_WINDOW}. Capacities are staff per Working Day (PROVISIONAL ASSUMPTIONS); "
                      f"{NO_LEVELLING}."] + notes}


def date_span(a: str, b: str) -> str:
    return a if a == b else f"{a}..{b}"


def resource_statuses(rows: list[dict], load: dict) -> dict[str, str]:
    """id -> OK / OVERLOAD <role> on <dates> (peak <load> vs capacity <c> staff) / NOT LOADED (<why>)."""
    out = {}
    for a in rows:
        x = load["loaded"].get(a["id"]) or {"loaded": False, "reason": "not assessed"}
        if not x["loaded"]:
            out[a["id"]] = f"NOT LOADED ({x['reason']})"
            continue
        days = set(x["days"])
        hits = [o for o in load["overloads"] if o["resource"] == x["resource"] and days & set(o["dates"])]
        cap = (load["daily"].get(x["resource"]) or {}).get(x["days"][0], {}).get("capacity")
        if cap is None:
            out[a["id"]] = f"NO CAPACITY CONFIGURED for {x['resource']}"
        elif hits:
            out[a["id"]] = "; ".join(f"OVERLOAD {o['resource']} on {date_span(o['from'], o['to'])} (peak {o['peak_load']:g} "
                                     f"vs capacity {o['capacity']} staff)" for o in hits)
        else:
            out[a["id"]] = "OK"
    return out


# ---------------------------------------------------------------------------------------------- checks

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
            if t.get("discipline") and t["discipline"] not in DISCIPLINES:
                problems.append(f"C45: activity {t['id']} ({item}) names discipline '{t['discipline']}' (known: "
                                f"{', '.join(DISCIPLINES)})")
            g = t.get("gated_by")
            if g is not None and (not isinstance(g, list) or not all(isinstance(i, str) and i.startswith("I-") for i in g)):
                problems.append(f"C45: activity {t['id']} ({item}): gated_by must list issue ids (I-...)")
            try:
                multiplicity(t.get("per"), bidder)
            except KeyError as e:
                problems.append(f"C45: activity {t['id']} ({item}): {e.args[0]}")
            if t["id"] in seen and seen[t["id"]][1] != t:
                problems.append(f"C45: activity {t['id']} is defined differently under {seen[t['id']][0]} and {item}")
            for k in ("name", "item"):
                typed = [m.group(0) for rx in (_TIME, _DATE) for m in rx.finditer(PLACEHOLDER.sub("", str(t.get(k) or "")))]
                if typed:
                    problems.append(f"C45: activity {t['id']} ({item}): its {k} types {', '.join(repr(x) for x in typed)}; a "
                                    "time or date the pack states is filled from the stage ({PDD_TIME}, {PDD_DATE}, "
                                    "{ROW:<row id>:<parameter>}), never typed")
            seen.setdefault(t["id"], (item, t))
    for ev, o in (templates.get("_per_overrides") or {}).items():
        try:
            multiplicity((o or {}).get("per"), bidder)
        except KeyError as e:
            problems.append(f"C45: _per_overrides {ev}: {e.args[0]}")
    for k, v in lead.items():
        try:
            if int(v["value"]) < 0 or int(v["value"]) != v["value"]:
                raise ValueError
        except (KeyError, TypeError, ValueError):
            problems.append(f"C45: lead-time assumption '{k}' has no whole, non-negative number of Working Days")
        if "effort_wd" in v and not (isinstance(v["effort_wd"], (int, float)) and v["effort_wd"] >= 0):
            problems.append(f"C45: lead-time assumption '{k}' has an effort_wd that is not a non-negative number")
    if "foreign_members" in bidder and "members" in bidder and int(bidder["foreign_members"]) > int(bidder["members"]):
        problems.append(f"C45: bidder.foreign_members ({bidder['foreign_members']}) is more than bidder.members "
                        f"({bidder['members']})")
    if "delivery_cutoff_time" in (assumptions.get("planning") or {}):
        problems.append("C45: planning.delivery_cutoff_time is refused: the Proposal Due Date's time is stated in the pack, "
                        "and pack-stated facts are derived (from the effective text of the anchor's defining unit at each "
                        "stage), not assumed. Remove the key from the assumptions")
    return problems


# ---------------------------------------------------------------------------------------------- placeholders

PLACEHOLDER = re.compile(r"\{([^{}\s]+)\}")


def anchor_fields(details: dict | None) -> dict[str, str | None]:
    """The placeholder values of every anchor: {PDD_TIME, PDD_TZ, PDD_DATE, PDD_SOURCE} (None where the effective
    text does not state it). `details`: register.anchor_details at one stage."""
    out: dict[str, str | None] = {}
    for name, d in (details or {}).items():
        key = re.sub(r"[^A-Za-z0-9]+", "_", name).upper()
        out.update({f"{key}_TIME": d.get("time"), f"{key}_TZ": d.get("tz"),
                    f"{key}_DATE": d["date"].isoformat() if d.get("date") else None, f"{key}_SOURCE": d.get("source")})
    return out


def fill(text: str, values: dict, where: str, problems: list[str], row_value=None) -> str:
    """`text` with its placeholders filled: {NAME} from `values`; {ROW:<row id>:<parameter>} from
    row_value(row id, parameter) -> (value, why not). An unknown placeholder, or a value that is None or empty, is
    a C45 problem appended to `problems` and the placeholder is kept as written ("None" is never printed). Pure."""
    def sub(m: re.Match) -> str:
        key, why = m.group(1), "not stated in the effective text at this stage"
        if key.startswith("ROW:") and row_value is not None and key.count(":") >= 2:
            rid, param = key[4:].rsplit(":", 1)
            v, why = row_value(rid, param)
        elif key in values:
            v = values[key]
        else:
            problems.append(f"C45: {where}: unknown placeholder {m.group(0)} (known: "
                            f"{', '.join('{' + k + '}' for k in sorted(values))}"
                            + (", {ROW:<row id>:<parameter>}" if row_value is not None else "") + ")")
            return m.group(0)
        if v is None or isinstance(v, (dict, list)) or str(v).strip() == "":
            problems.append(f"C45: {where}: {m.group(0)} cannot be filled ({why})")
            return m.group(0)
        return str(v)
    return PLACEHOLDER.sub(sub, str(text))


def stated_time(text: str) -> tuple[str | None, str | None] | None:
    """The time of day ('HH:MM') and the timezone words ('Riyadh time') that a date rule's own quoted words state
    (e.g. 'Wednesday 30 September 2026 at 10:00 Riyadh time'), read the way register.anchor_details reads an anchor's
    defining unit; None when the words print no date, (None, tz) when they print no time."""
    try:
        p = parse_date(text or "")
    except ValueError:
        return None
    if p is None:
        return None
    m = re.search(r"\b([A-Z][a-z]+ time)\b", text)
    return p[1], (m.group(1) if m else None)


def details_from_evals(evals: list[dict], stage: str, anchors: dict) -> dict:
    """Anchor details for a caller of plan() that passes none: each anchor's defining unit is the source unit of the
    date rule named after it, and that unit's effective text and amending ops are those the A1 evaluations show at
    the stage (units_detail); they are read by register.anchor_details, as stage2.evaluate reads the state."""
    from .register import anchor_details
    state: dict[str, SimpleNamespace] = {}
    defined: dict[str, str] = {}
    for e in evals:
        ev = e["stages"].get(stage) or {}
        for d in ev.get("dates") or []:
            if d.get("anchor") in anchors and d.get("rule_id") == d.get("anchor") and d.get("source_unit"):
                defined.setdefault(d["anchor"], d["source_unit"])
        for u in ev.get("units_detail") or []:
            if u.get("effective_unit") == u.get("unit"):
                state.setdefault(u["unit"], SimpleNamespace(text=u.get("text") or "", status=u.get("status"),
                                                            history=list(u.get("ops") or []), number=None))
    return anchor_details(state, {k: {"defined_in": v} for k, v in sorted(defined.items())}, {})


# ---------------------------------------------------------------------------------------------- milestones

def milestones(rules: dict[str, dict], templates: dict, assumptions: dict, act_rules: dict[str, list[str]],
               linked_rows: set[str], anchor_details: dict | None = None, problems: list[str] | None = None) -> list[dict]:
    """Dated pack milestones of the stage: every date rule of a row in force with a planning value (fixed dates,
    the PDD, the clarification cut-off, validity ends...), named by the templates' `_milestones.labels`; the
    `_milestones.derived` ones (e.g. the site visit, 'the day following the Pre-Bid Conference'); and the
    event-dependent rules (no date) of rows the programme's activities serve. The milestone of an anchor (the PDD)
    takes its time from `anchor_details` (register.anchor_details at the stage), never from the templates or the
    assumptions; its labels fill {time} {tz} {date} {source} (`fill`; C45 problems go to `problems`)."""
    cfg = templates.get("_milestones") or {}
    labels = cfg.get("labels") or {}
    details = anchor_details or {}
    problems = problems if problems is not None else []
    glob = anchor_fields(details)
    out = []
    for rid in sorted(rules):
        d = rules[rid]
        value = d["planning"]["value"]
        if not value and not (set(d["rows"]) & linked_rows):
            continue
        lab = labels.get(rid) or {}
        anc = details.get(rid)
        stated = None if anc is not None else stated_time(d.get("text") or "")   # a fixed rule's own quoted words
        if anc is not None and "time" in lab:
            problems.append(f"C45: _milestones.labels.{rid} types a time ({lab['time']!r}); the time of an anchor is read "
                            f"from its defining unit ({anc.get('unit')}), never typed")
        elif stated and stated[0] and "time" in lab:
            problems.append(f"C45: _milestones.labels.{rid} types a time ({lab['time']!r}); the rule's own words state "
                            f"it ({d.get('text')!r}), so the label fills {{time}} {{tz}} from them, never typed")
        if anc is not None:
            vals = dict(glob, time=anc.get("time"), tz=anc.get("tz"), source=anc.get("source"),
                        date=anc["date"].isoformat() if anc.get("date") else None)
            time = str(anc.get("time") or "")
        elif stated and stated[0]:
            vals = dict(glob, time=stated[0], tz=stated[1])
            time = stated[0]
        else:
            vals, time = glob, str(lab.get("time", ""))
        out.append({"id": rid, "date": value, "time": time,
                    "short": fill(lab.get("short", rid), vals, f"_milestones.labels.{rid}.short", problems),
                    "label": (fill(lab["label"], vals, f"_milestones.labels.{rid}.label", problems) if lab.get("label")
                              else d.get("text", rid)),
                    "purpose": d.get("purpose", ""), "words": d.get("text", ""), "source": d.get("source_unit", ""),
                    "reading": d["planning"].get("key", ""), "readings_differ": bool(d.get("readings_differ")),
                    "rows": sorted(d["rows"]), "conditional": bool(lab.get("conditional")), "derived": False,
                    "activities": sorted(act_rules.get(rid, [])),
                    "kind": ("dated" if value else "event-dependent (no date: " + str(d["planning"].get("key")) + ")")})
    by_id = {m["id"]: m for m in out}
    for did, spec in sorted((cfg.get("derived") or {}).items()):
        src = by_id.get(spec.get("from"))
        if not src or not src["date"]:
            continue
        v = date.fromisoformat(src["date"]) + timedelta(days=int(spec.get("calendar_days_after", 0)))
        out.append({"id": did, "date": v.isoformat(), "time": str(spec.get("time", "")),
                    "short": fill(spec.get("short", did), glob, f"_milestones.derived.{did}.short", problems),
                    "label": fill(spec.get("label", did), glob, f"_milestones.derived.{did}.label", problems),
                    "purpose": "event", "words": spec.get("label", ""),
                    "source": spec.get("source", ""), "reading": f"derived from {src['id']}", "readings_differ": False,
                    "rows": [], "conditional": bool(spec.get("conditional")), "derived": True, "activities": [],
                    "kind": "dated (derived)"})
    return sorted(out, key=lambda m: (m["date"] or "9999", m["id"]))


# ---------------------------------------------------------------------------------------------- plan

def plan(stage: str, evals: list[dict], templates: dict, assumptions: dict, cal: Calendar, status_date: date,
         anchors: dict, evidence_items: dict | None = None, anchor_details: dict | None = None, notified_days: list[str] | None = None) -> dict:
    """evals: [{"row": Row, "stages": {stage: evaluation}}] from register.Register.all().
    evidence_items (optional): the evidence vocabulary (evidence.load_evidence_items), for each activity's envelope.
    status_date: the planning date (the stage's addendum issue date).
    anchor_details (optional): register.anchor_details at this stage (stage2.evaluate's r["anchor_details"][stage]);
    without it, the same is read from the evaluations (details_from_evals). It fills the placeholders of activity
    names and items and the PDD milestone, and gives the PDD time in the planning basis."""
    if anchor_details is None:
        anchor_details = details_from_evals(evals, stage, anchors)
    need: dict[str, list[str]] = {}
    row_flags: dict[str, list[str]] = {}
    deadlines: dict[str, tuple[str, str]] = {}            # rule_id -> (date, row id)
    rules: dict[str, dict] = {}                           # rule_id -> date entry + rows (for milestones)
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
            x = rules.setdefault(d["rule_id"], {**{k: v for k, v in d.items() if k != "interpretations"}, "rows": set()})
            x["rows"].add(row.id)
    exceptions = templates.get("_exceptions") or {}
    defined = {t["id"] for item, ts in templates.items() if not item.startswith("_") for t in (ts or [])}
    problems = check_templates(templates, assumptions)
    missing = [i for i in sorted(need) if not templates.get(i) and not (exceptions.get(i) or "").strip()]
    for item in missing:
        problems.append(f"C44: {item} is needed by {', '.join(need[item])} (in force at {stage}) but has no "
                        f"activities and no justified exception")
    lead = assumptions.get("lead_times") or {}
    bidder = assumptions.get("bidder") or {}
    fields = anchor_fields(anchor_details)
    by_row = {e["row"].id: e["stages"].get(stage) or {} for e in evals}
    named_rows: dict[str, set[str]] = {}                  # activity -> rows its name or item quotes ({ROW:...})

    def row_value(rid: str, param: str):
        ev = by_row.get(rid)
        if not ev:
            return None, f"no row {rid} in the register"
        if not in_force(str(ev.get("status") or "")):
            return None, f"row {rid} is not in force at {stage} ({ev.get('status')})"
        it = ev.get("interpretation") or {}
        if param not in (it.get("parameters") or {}):
            return None, f"the interpretation of row {rid} used at {stage} ({it.get('stage') or 'none'}) has no parameter '{param}'"
        return it["parameters"][param], ""
    acts: dict[str, dict] = {}
    for item in sorted(need):
        for t in templates.get(item) or []:
            if t.get("duration") not in lead:
                continue
            try:
                count, expr = multiplicity(t.get("per"), bidder)
            except KeyError:
                continue                                     # reported by check_templates (C45)
            lt = lead[t["duration"]]
            eff, waiting, eff_basis = effort_of(lt)
            env = getattr((evidence_items or {}).get(item), "envelope", "") if evidence_items else ""
            if t["id"] not in acts:
                named_rows[t["id"]] = {k[4:].rsplit(":", 1)[0] for s in (t["name"], t.get("item", ""))
                                       for k in PLACEHOLDER.findall(str(s)) if k.startswith("ROW:") and k.count(":") >= 2}
                name = fill(t["name"], fields, f"activity {t['id']} ({item}) name at {stage}", problems, row_value)
                item_text = fill(t.get("item", ""), fields, f"activity {t['id']} ({item}) item at {stage}", problems, row_value)
            a = acts.setdefault(t["id"], {
                "id": t["id"], "name": name, "evidence": item, "evidence_items": [], "envelope": env,
                "owner": t["owner"],
                "discipline": t.get("discipline") or (t["owner"] if t["owner"] in DISCIPLINES else "Bid management"),
                "resource": t.get("resource", ""), "issuer": t["issuer"],
                "duration_wd": int(lt["value"]), "duration_assumption": t["duration"],
                "duration_basis": duration_basis(lt), "per": t.get("per") or "proposal", "count": count,
                "multiplicity": multiplicity_label(t.get("per"), bidder), "count_expr": expr,
                "effort_wd": eff, "effort_total_wd": round(eff * count, 3), "effort_basis": eff_basis,
                "waiting_on": waiting, "work_type": "external waiting + staff effort" if waiting else "staff effort",
                "item": item_text, "gated_by": list(t.get("gated_by") or []),
                "condition": str(t.get("condition") or ""),
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
    net = network({k: {"duration_wd": a["duration_wd"], "predecessors": a["predecessors"],
                       "deadline_rule": a["deadline_rule"],
                       "deadline_date": date.fromisoformat(a["deadline_date"]) if a["deadline_date"] else None}
                   for k, a in acts.items()}, cal, status_date)
    iso = lambda d: d.isoformat() if d else None                                    # noqa: E731
    rows = []
    for aid in sorted(acts, key=lambda k: (net[k]["ls"] or date.max, k)):
        a = acts[aid]
        t = net[aid]
        flags = window_flags({**t, "rule": a["deadline_rule"], "condition": a["condition"]}, status_date, cal)
        if a["count"] == 0:
            flags.insert(0, f"NOT NEEDED (count 0 under the assumed bidder: {a['count_expr']}; nothing to produce; kept "
                            "in the network unchanged so scenarios compare like for like)")
        for r in a["req_ids"]:
            flags += [f"{x} ({r})" for x in row_flags.get(r, [])]
        for r in sorted(named_rows.get(aid, set()) - set(a["req_ids"])):
            flags += [f"{x} ({r}, quoted in the activity's text)" for x in row_flags.get(r, [])]
        flags += [f"dependency '{d}' not required at this stage" for d in a.pop("not_required_here")]
        status = timing_status(flags)
        g = a["gated_by"]
        ls = t["ls"]
        decision = "READY" if not g else (
            f"GATED: finalisation waits on {', '.join(g)}; decision needed by "
            + (ls.isoformat() + (" (already before the planning date; see timing)" if ls < status_date else "")
               if ls else "no latest start (not linked to a pack date)"))
        rows.append({**a, "earliest_start": iso(t["es"]), "earliest_finish": iso(t["ef"]), "es_driven_by": t["es_driven_by"],
                     "latest_start": iso(ls), "latest_finish": iso(t["lf"]), "float_wd": t["float_wd"],
                     "driven_by": t["driven_by"],
                     "deadline": (f"{a['deadline_rule']} = {deadlines[a['deadline_rule']][0]} (from {deadlines[a['deadline_rule']][1]})"
                                  if a["deadline_rule"] in deadlines else ""),
                     "flags": flags, "status": status, "timing_status": status, "decision_status": decision,
                     "decision_needed_by": iso(ls) if g else None})
    load = resource_load(rows, assumptions.get("resources") or {}, cal, status_date)
    rst = resource_statuses(rows, load)
    for row in rows:
        row["resource_status"] = rst[row["id"]]
    marshalling = [{"item": r["item"], "envelope": r["envelope"], "evidence": r["evidence"], "issuer": r["issuer"],
                    "owner": r["owner"], "resource": r["resource"], "lead_time_wd": r["duration_wd"],
                    "lead_time_assumption": r["duration_assumption"], "multiplicity": r["multiplicity"],
                    "count": r["count"], "drop_dead_start": r["latest_start"], "needed_by": r["latest_finish"],
                    "activity": r["id"], "status": r["status"], "decision_status": r["decision_status"],
                    "req_ids": r["req_ids"], "flags": r["flags"]}
                   for r in rows if r["item"]]
    day0 = first_working_day(cal, status_date)
    act_rules: dict[str, list[str]] = {}
    for r in rows:
        if r["deadline_rule"]:
            act_rules.setdefault(r["deadline_rule"], []).append(r["id"])
    used = sorted({r["deadline_rule"] for r in rows if r["deadline_rule"] in deadlines})
    pdd = deadlines.get("PDD", (anchors.get("PDD"), ""))[0]
    basis = (f"Planning date {status_date.isoformat()} = the issue date of {stage}, the latest addendum at this stage "
             f"(owner's instruction: the latest addendum date is the planning date). Earliest dates: a forward pass in "
             f"Working Days (VOL-I 2.4: Sunday to Thursday, declared holidays excluded; holidays configured: "
             f"{', '.join(sorted(h.isoformat() for h in cal.holidays)) or 'none'}"
             + (f"; of these, notified by an addendum under VOL-I 2.4: {', '.join(sorted(notified_days))}" if notified_days else "")
             + ") from the first Working Day on or "
             f"after the planning date ({day0.isoformat()}). Latest dates: a backward pass from the pack deadlines in "
             f"force at {stage} ("
             + "; ".join(f"{k} {deadlines[k][0]}" + (f" {anchor_details[k]['time']}"
                                                     if (anchor_details.get(k) or {}).get("time") else "") for k in used)
             + f"). Total float = Working Days from earliest start to latest start; negative float = INFEASIBLE by that "
               f"many Working Days (never compressed). Proposal Due Date at this stage: {pdd}.")
    linked = {x for r in rows for x in r["req_ids"]}
    ms = milestones(rules, templates, assumptions, act_rules, linked, anchor_details, problems)
    return {"stage": stage, "status_date": status_date.isoformat(), "planning_date": status_date.isoformat(),
            "start_date": day0.isoformat(), "planning_basis": basis, "anchors": anchors, "activities": rows,
            "marshalling": marshalling, "problems": problems,
            "exceptions": {k: v for k, v in exceptions.items() if k in need},
            "evidence_needed": {k: sorted(v) for k, v in sorted(need.items())},
            "deadlines": {k: {"date": v[0], "row": v[1]} for k, v in sorted(deadlines.items())},
            "milestones": ms,
            "per_overrides": {k: dict(v) for k, v in sorted((templates.get("_per_overrides") or {}).items()) if k in need},
            "calendar": {"weekend": sorted(cal.weekend), "holidays": sorted(h.isoformat() for h in cal.holidays)},
            "load": {"window": load["window"], "overloads": load["overloads"], "notes": load["notes"]}}


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
                         [d["planning"] for d in prev_evals[r]["dates"]] != [d["planning"] for d in cur_evals[r]["dates"]] or
                         prev_evals[r].get("text") != cur_evals[r].get("text") or
                         prev_evals[r].get("cells") != cur_evals[r].get("cells") or
                         bool(prev_evals[r].get("stale")) != bool(cur_evals[r].get("stale")))]
        if changed_rows:
            out.append({"activity": k, "change": "REWORK", "detail": f"requirement changed: {', '.join(changed_rows)}"})
        if p[k]["latest_start"] != c[k]["latest_start"]:
            out.append({"activity": k, "change": "MOVED", "detail": f"latest start {p[k]['latest_start']} -> {c[k]['latest_start']}"})
    return out
