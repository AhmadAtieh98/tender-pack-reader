"""Candidate consequences and programme impacts for a PARTIAL addendum (session 11).

When an addendum is PARTIAL (some provisions unresolved, an op invalid or withheld), the validated state does not move:
A3 and the main A5 are built from the last stage reached through APPLIED addenda only (stage2), byte for byte as before.
This module adds, beside them and clearly labelled CANDIDATE (NOT VALIDATED), what the working stage would give if
every op that is valid and not withheld there stood (for an AI workflow candidate: the promoted ops, each
evidence_verified or interpretation_pending in the controller):

  out/a3/a3_candidate.{json,md,html,pdf}
      the A3 as it would read at the working stage (every section in full: the candidate may run to more pages than
      the one-page validated A3 and says so on every page), the rows that ENTER, LEAVE or CHANGE against the validated
      A3, each with its source op(s) and their status; a Blockers block (the unresolved provisions with their
      reasons and the rows and activities they reach, invalid or withheld ops, rows whose reading is STALE, the C46
      gaps, the documents not supplied (every one, and whether the addendum's changes reach it), the conflicts and
      the issues the ops raise, the open issues in play); a Conditional scenarios block; and the image-read units the
      addendum touches, with the build's review packets (crops), the Arabic verbatim, the translations apart, the table
      context, the units and the recorded uncertainties.
  out/a5/candidate/
      the programme replanned at the working stage (planning date = its issue date), with the dates that move against
      the validated A5 and the rows and ops that move them, the activities marked REVIEW through relationships, the
      activities BLOCKED because a row they serve is unresolved, and the conditional scenarios as decision milestones
      (programme.candidate_replan / write_candidate); the Gantt is drawn from the same data.

Conditional and effective-dated amendments: first what the engine models (amend.Condition on an op: the stage's
`conditions`, the rows' `conditional` records with the trigger deadline the register computes, the A5 decision
milestone), then an op's `effective_from`, then what the op file says in words only (an op's note or issue, or an
unresolved provision's reason, saying it is conditional or effective-dated), with the dates printed in the words it can
see, labelled as text only. A trigger is never assumed to have occurred.

Nothing here validates, accepts or applies anything: the files are views of the working stage that stage2 already
computes (A1's WORKING column, a5/working/). Pure functions except `write`."""
from __future__ import annotations

import json
import re
from pathlib import Path

from . import programme, relationships
from .citations import citations, resolve
from .dates import _DATE, _MONTH_NO
from .schedule import in_force
from .util import dump_json, write_text

UNRES = ("unresolved", "UNACCOUNTED", "rejected")
BANNER = "CANDIDATE — NOT VALIDATED"
# words that make an op or an unresolved provision a conditional or effective-dated amendment (heuristic: the text only)
_COND = re.compile(r"(?<!not )\bconditional\b|\bonly (?:if|where)\b|\bwhere this section\b[^.]{0,60}\bhas effect\b|"
                   r"\bif the authority (?:gives|issues|notifies)\b|\bin the event that\b|\btrigger", re.I)
_COND_CS = re.compile(r"\bCONDITION\b")                      # 'CONDITION: if ...' as a curator writes it
_EFFECTIVE = re.compile(r"\bwith effect from\b|\beffective (?:from|on|as of)\b|\btakes? effect (?:on|from)\b", re.I)
_DEADLINE_WORD = re.compile(r"\b(?:by|before|not later than|no later than|on or before|until)\b", re.I)
# the words that make it an amendment that may or may not take effect (rather than an obligation that applies only to some
# bidders, 'CONDITION: only a Bidder whose ...')
_AMENDMENT = re.compile(r"\bconditional amendment\b|\bsection\b[^.]{0,60}\bhas effect\b|\bif the authority "
                        r"(?:gives|issues|notifies)\b|\bshall (?:only )?(?:have|take) effect\b|\bnot in effect\b", re.I)
_UNIT_REF = re.compile(r"\b(?:VOL-[IVX]+|ADD-\d+):[\w./()+-]+")
# fields a conditional model on an op may carry (read when present; none is required)
scenario_fields = ("condition", "conditional", "trigger", "trigger_event", "trigger_deadline", "deadline", "states",
                   "alternatives", "if_triggered", "if_not_triggered", "effective_from", "effective_date", "applies_from")


def _short(t, n: int = 220) -> str:
    t = " ".join(str(t or "").split())
    return t if len(t) <= n else t[: n - 1] + "…"


def _iso(m) -> str:
    from datetime import date
    try:
        return date(int(m["y"]), _MONTH_NO[m["m"].lower()], int(m["d"])).isoformat()
    except ValueError:                                         # not a calendar date: shown as printed, never fixed
        return m.group(0)


def printed_dates(text: str) -> list[dict]:
    """Every date printed in `text`, in order: {date (ISO), words, deadline: a deadline word ('by', 'before', 'not later
    than' ...) stands before it in the same sentence, at most 80 characters back ('not later than four (4) Working Days
    before the Proposal Due Date: Thursday 19 November 2026')}."""
    out, text = [], text or ""
    for m in _DATE.finditer(text):
        back = re.split(r"[.;]\s", text[max(0, m.start() - 80):m.start()])[-1]
        out.append({"date": _iso(m), "words": m.group(0), "deadline": bool(_DEADLINE_WORD.search(back))})
    return out


# ---------------------------------------------------------------------------------------------- the stages

def pending(r: dict) -> list:
    """The stages after the validated one (the PARTIAL addendum and any after it); [] when none."""
    order = [s.stage for s in r["stages"]]
    return r["stages"][order.index(r["validated"].stage) + 1:]


def _prev_state(r: dict, s) -> dict:
    order = [x.stage for x in r["stages"]]
    return r["stages"][order.index(s.stage) - 1].state


def conditional_label(r: dict, x) -> str:
    """How a conditional op (amend.Condition; OpResult.pending) reads wherever ops are listed: CONDITIONAL with its state,
    the trigger, the decision date the register computes (else the deadline's words), the recorded fact or that nothing
    assumes one, and both states. Never 'withheld' or 'rejected': a held conditional op is correctly not applied."""
    cd = x.details.get("conditional") or {}
    when = next((c["deadline"]["value"] for e in r.get("evals") or [] for ev in e["stages"].values()
                 for c in ev.get("conditional") or [] if c.get("op") == x.op.id and (c.get("deadline") or {}).get("value")),
                None)
    words = (cd.get("deadline") or {}).get("text")
    fact = cd.get("fact") or {}
    states = "; ".join(f"{u}: “{_short(v.get('before'), 70)}” -> “{_short(v.get('after'), 70)}”"
                       for u, v in (cd.get("if_triggered") or {}).items())
    return (f"CONDITIONAL ({cd.get('state', 'pending')}): not in effect unless {_short(cd.get('trigger'), 140)} "
            f"({cd.get('trigger_unit')})" + (f"; decide by {when}" if when else f"; deadline: {words}" if words else "")
            + (f"; trigger recorded by {fact.get('recorded_by')} ({fact.get('date')}): occurred {fact.get('occurred')}"
               if fact else "; nothing assumes the trigger occurred")
            + (f"; if triggered: {states}" if states else "")
            + f"; if not: {cd.get('if_not_triggered') or 'the units stay as they stand'}")


def op_info(r: dict, x, op_status: dict | None = None) -> dict:
    """One op as the candidate shows it: validity, whether it stands in the candidate, the review status of the
    register (a person's decision bound to its content, or proposed) and, when the caller passes them, the controller's
    status (evidence_verified, interpretation_pending ...)."""
    o = x.op
    rv = (r.get("reviews") or {}).get(("op", o.id)) or {}
    ctl = (op_status or {}).get(o.id)
    state = ("applied in the candidate" if x.applied else
             conditional_label(r, x) if getattr(x, "conditional_pending", False) else
             "NOT applied: withheld (a person rejected it)" if x.valid else
             "NOT applied: invalid (" + "; ".join(c["id"] for c in x.checks if not c["ok"]) + ")")
    return {"op": o.id, "stage": x.stage, "type": o.type, "provision": o.provision,
            "target": o.target or o.new_group or ", ".join(o.targets), "valid": x.valid, "applied": x.applied,
            "review": rv.get("status", "proposed"), "origin": o.origin, "controller": ctl,
            "label": f"{o.id} ({o.type}; {state}; review {rv.get('status', 'proposed')}; origin {o.origin}"
                     + (f"; controller {ctl}" if ctl else "") + ")"}


def _cited(state: dict, text: str, provision: str | None = None) -> set[str]:
    t = set(resolve(citations(text or ""), set(state)))
    return t | ({provision} if provision else set())


def _rows_citing(r: dict, stage: str, targets: set[str]) -> list[str]:
    out = []
    for e in r["evals"]:
        units = set(e["row"].units) | ({e["stages"][stage].get("effective_unit")} - {None})
        if units & targets or any(u.startswith(t + "/") or u.startswith(t + "(") for t in targets for u in units):
            out.append(e["row"].id)
    return sorted(out)


def unresolved_rows(r: dict) -> dict[str, list[str]]:
    """{row id: [why]} for the rows the candidate cannot settle: rows citing a unit an unresolved provision of a pending
    stage names (or the provision itself), and rows STALE at the working stage (their reading was made against a
    state that no longer holds and was not re-made)."""
    w = r["working"].stage
    out: dict[str, list[str]] = {}
    for s in pending(r):
        for c in s.coverage:
            if c["disposition"] not in UNRES:
                continue
            u = s.state.get(c["provision"])
            for rid in _rows_citing(r, w, _cited(_prev_state(r, s), u.text if u else c.get("text", ""), c["provision"])):
                out.setdefault(rid, []).append(f"{c['provision']} {c['disposition'].upper()}: "
                                               f"{_short(c.get('reason') or 'no op or disposition', 160)}")
    for e in r["evals"]:
        ev = e["stages"][w]
        if ev["stale"] and in_force(ev["status"]):
            out.setdefault(e["row"].id, []).append(f"STALE at {w}: its reading was not re-made "
                                                   f"({_short('; '.join(ev['stale']), 160)})")
    return {k: v for k, v in sorted(out.items())}


def row_sources(r: dict, rid: str) -> dict:
    """What changed a row between the validated and the working stage: the op ids (on its units, on any other unit it
    cites, the ops issuing its units, annotations) and the reasons, from live._secondary and the register."""
    from .live import _secondary
    v, w = r["validated"].stage, r["working"].stage
    e = next(x for x in r["evals"] if x["row"].id == rid)
    a, b = e["stages"][v], e["stages"][w]
    ops = [h for h in b.get("ops") or [] if h not in (a.get("ops") or [])]
    why = []
    sec, sec_ops = _secondary(e["row"], r["validated"].state, r["working"].state)
    why += sec
    ops += [o for o in sec_ops if o not in ops]
    units = set(e["row"].units)
    for s in pending(r):
        for x in s.ops:
            o = x.op
            if not x.applied or o.id in ops:
                continue
            if o.provision in units or {o.target, *o.targets} & units or set(x.changed) & units \
                    or set(o.covers) & units or set(x.details.get("content") or []) & units:
                ops.append(o.id)
    if b.get("interpretation_stage") in {s.stage for s in pending(r)} and a.get("interpretation") != b.get("interpretation"):
        why.append(f"reading re-made at {b['interpretation_stage']} (register)")
    if a["status"] != b["status"]:
        why.append(f"status {a['status']} -> {b['status']}")
    return {"ops": ops, "why": why}


# ---------------------------------------------------------------------------------------------- A3

def a3_index(a3d: dict) -> dict[str, dict]:
    """Row id -> where it stands on an A3 (stage2.a3 output): list, class, consequence, text, flags."""
    idx: dict[str, dict] = {}
    for key, items in (("explicit", a3d.get("explicit") or []), ("score", a3d.get("score") or []),
                       ("refused", a3d.get("refused") or []), ("criterion_zero", a3d.get("criterion_zero") or []),
                       ("gate", a3d.get("none_stated") or [])):
        for x in items:
            idx.setdefault(x["id"], {"list": key, "class": x.get("class", "") if key != "gate" else "pass/fail gate",
                                     "consequence": x.get("consequence", ""), "text": x.get("text", ""),
                                     "flags": list(x.get("flags") or []), "source": x.get("source", "")})
    return idx


def a3_changes(r: dict, a3v: dict, a3c: dict, op_status: dict | None = None,
               unres_rows: dict | None = None) -> list[dict]:
    """The rows that enter, leave or change on A3 between the validated and the candidate state, each with the op(s)
    that move it (op_info), the row's review status and flags, and why it is not settled when it is not (`unres_rows`,
    unresolved_rows: a row re-read against an unresolved provision shows words the candidate does not hold)."""
    unres_rows = unres_rows or {}
    iv, ic = a3_index(a3v), a3_index(a3c)
    ops = {x.op.id: x for s in r["stages"] for x in s.ops}
    out = []
    for rid in sorted(set(iv) | set(ic)):
        a, b = iv.get(rid), ic.get(rid)
        what = []
        if a is None:
            kind = "enters"
            what.append(f"{b['list']} ({b['class']})" + (f": “{_short(b['consequence'], 200)}”" if b["consequence"] else ""))
        elif b is None:
            kind = "leaves"
            what.append(f"was {a['list']} ({a['class']})")
        else:
            if (a["list"], a["class"], a["consequence"]) != (b["list"], b["class"], b["consequence"]):
                what.append(f"consequence: {a['list']} ({a['class']}) “{_short(a['consequence'], 120)}” -> "
                            f"{b['list']} ({b['class']}) “{_short(b['consequence'], 120)}”")
            if a["text"] != b["text"]:
                what.append(f"text: “{_short(a['text'], 120)}” -> “{_short(b['text'], 120)}”")
            for f in ("STALE", "image reading pending"):
                if (f in a["flags"]) != (f in b["flags"]):
                    what.append(f"{'now' if f in b['flags'] else 'no longer'} {f}")
            if not what:
                continue
            kind = "changes"
        src = row_sources(r, rid)
        if kind != "leaves" and not src["ops"] and not src["why"]:
            src["why"].append("no op of the pending stage names it: a register-level difference")
        src["why"] += [f"NOT SETTLED: {y}" for y in unres_rows.get(rid, [])]
        e = next(x for x in r["evals"] if x["row"].id == rid)
        out.append({"row": rid, "change": kind, "what": what, "requirement": e["row"].requirement,
                    "ops": [op_info(r, ops[o], op_status) for o in src["ops"] if o in ops], "why": src["why"],
                    "row_review": ((r.get("reviews") or {}).get(("row", rid)) or {}).get("status", "proposed"),
                    "status_validated": e["stages"][r["validated"].stage]["status"],
                    "status_candidate": e["stages"][r["working"].stage]["status"],
                    "stale": bool(e["stages"][r["working"].stage]["stale"])})
    order = {"enters": 0, "changes": 1, "leaves": 2}
    return sorted(out, key=lambda x: (order[x["change"]], x["row"]))


# ---------------------------------------------------------------------------------------------- blockers

def blockers(r: dict, unres_rows: dict, prog_c: dict | None, issues_c: list[dict]) -> dict:
    """Everything that stops the candidate from becoming the validated state, or that it cannot establish."""
    w = r["working"].stage
    acts = (prog_c or {}).get("activities") or []
    provs, invalid, held, conflicts, op_issues = [], [], [], [], []
    for s in pending(r):
        for c in s.coverage:
            if c["disposition"] not in UNRES:
                continue
            u = s.state.get(c["provision"])
            rows = _rows_citing(r, w, _cited(_prev_state(r, s), u.text if u else c.get("text", ""), c["provision"]))
            reason = c.get("reason") or ("no op or disposition accounts for it" if c["disposition"] == "UNACCOUNTED" else "")
            low = reason.lower()
            kind = ("escalated" if "escalat" in low else "conflicting" if "conflict" in low else
                    "insufficient evidence" if "insufficient" in low or "missing" in low else
                    "not analysed" if "not analysed" in low else "invalid op" if "invalid" in low else
                    "rejected by a person" if c["disposition"] == "rejected" else
                    "unaccounted" if c["disposition"] == "UNACCOUNTED" else "unresolved")
            provs.append({"stage": s.stage, "provision": c["provision"], "page": c.get("page"), "kind": kind,
                          "disposition": c["disposition"], "reason": reason, "text": _short(u.text if u else c.get("text"), 300),
                          "rows": rows, "activities": sorted({a["id"] for a in acts if set(a["req_ids"]) & set(rows)})})
            if "conflict" in low:
                conflicts.append({"stage": s.stage, "what": f"{c['provision']}: {_short(reason, 260)}",
                                  "source": "unresolved provision"})
        for x in s.ops:
            if not x.valid:
                invalid.append({"stage": s.stage, "op": x.op.id, "provision": x.op.provision,
                                "failed": "; ".join(f"{c['id']}: {_short(c['detail'], 160)}" for c in x.checks if not c["ok"])})
            elif x.withdrawn:
                held.append({"stage": s.stage, "op": x.op.id, "provision": x.op.provision})
            if x.op.issue:
                op_issues.append({"stage": s.stage, "op": x.op.id, "issue": _short(x.op.issue, 300), "applied": x.applied})
    stages = {s.stage for s in pending(r)}
    for sc in r.get("summary_check") or []:
        if sc["stage"] in stages:
            conflicts += [{"stage": sc["stage"], "what": _short(f["detail"], 260), "source": f"cover summary vs provisions (C28 {f['kind']})"}
                          for f in sc["findings"] if f["kind"] == "contradicted"]
    for i in issues_c:
        if i["id"].startswith("I-AUTO-PRINTED"):
            conflicts.append({"stage": w, "what": _short(i["text"], 260), "source": f"printed date vs effective date ({i['id']}, C31)"})
    stale = [{"row": e["row"].id, "why": _short("; ".join(e["stages"][w]["stale"]), 260)}
             for e in r["evals"] if e["stages"][w]["stale"] and in_force(e["stages"][w]["status"])]
    gaps = [{"stage": t["stage"], "op": t["op"], "output": t["output"], "detail": _short(t["detail"], 260)}
            for t in r.get("trace") or [] if t["stage"] in stages]
    entries = r.get("relationships") or []
    chains = [{"target": x["target"], "path": list(x.get("path") or []), "kind": x.get("kind"), "status": x.get("status"),
               "completeness": x.get("completeness", "complete"), "truncated_by": x.get("truncated_by") or "",
               "unfollowed": list(x.get("unfollowed") or []), "cycle": list(x.get("cycle") or []),
               "blockers": [{k: b.get(k) for k in ("entry_id", "document_id", "document", "blocks", "node", "status", "text")}
                            for b in x.get("blockers") or []],
               "label": relationships.label(x, entries)}
              for x in ((r.get("relationship_impact") or {}).get(w) or {}).get("records") or []
              if x.get("kind") != "missing_document" and (x.get("completeness", "complete") != "complete" or x.get("blockers"))]
    blocked = [{"activity": a["id"], "name": a["name"], "rows": sorted(set(a["req_ids"]) & set(unres_rows)),
                "why": sorted({y for rid in set(a["req_ids"]) & set(unres_rows) for y in unres_rows[rid]})}
               for a in acts if set(a["req_ids"]) & set(unres_rows)]
    return {"provisions": provs, "invalid_ops": invalid, "withheld_ops": held, "stale_rows": stale, "c46": gaps,
            "missing_documents": missing_documents(r, issues_c), "conflicts": conflicts, "op_issues": op_issues,
            "blocked_activities": blocked, "unresolved_rows": [{"row": k, "why": v} for k, v in unres_rows.items()],
            "chains": chains}


def missing_documents(r: dict, issues: list[dict]) -> list[dict]:
    """Every document the pack refers to but does not supply: the relationships file's missing_document entries (with
    the conclusions they block, and whether what the pending stages changed reaches them) and the open issues that say
    so (e.g. I-PERMIT). Kept visible whatever the addendum does."""
    from .stage2 import MISSING_DOC_WORDS, issue_theme
    w = r["working"].stage
    recs = ((r.get("relationship_impact") or {}).get(w) or {}).get("records") or []
    reached = {}
    for rec in relationships.gaps(recs):
        reached.setdefault(rec["entry_id"], []).append(rec["target"])
    for rec in recs:                                    # a chain the document blocks (trace records' blockers)
        for b in rec.get("blockers") or []:
            reached.setdefault(b.get("entry_id"), []).append(rec["target"])
    out = []
    for did, d in relationships.missing_documents(r.get("relationships") or []).items():
        ents = [e["id"] for e in d["entries"]]
        out.append({"id": f"I-AUTO-NOT-SUPPLIED-{did}", "document": d["document"],
                    "issues": sorted({i for e in d["entries"] for i in e.get("issues") or []}),
                    "blocks": "; ".join(_short(e.get("blocks"), 220) for e in d["entries"]),
                    "targets": d["targets"], "referenced_in": d["sources"],
                    "reached_by_this_addendum": sorted({t for x in ents for t in reached.get(x, [])})})
    named = {i for m in out for i in m["issues"]}
    for i in issues:
        if i["id"].startswith("I-AUTO-NOT-SUPPLIED-"):
            continue
        if issue_theme(i) == "missing" or any(x in i["text"].lower() for x in MISSING_DOC_WORDS):
            out.append({"id": i["id"], "document": "", "issues": [i["id"]], "blocks": _short(i.get("a3") or i["text"], 300),
                        "targets": i.get("rows") or [], "referenced_in": [], "reached_by_this_addendum": [],
                        "linked": i["id"] in named})
    return out


def open_issues_in_play(r: dict, rows: set[str], issues: list[dict]) -> list[dict]:
    """The open issues the rows in play (entering, leaving, changing, blocked or reached at the working stage) name, and
    the issues on the relationship entries that reach them: kept open, never resolved here."""
    by_id = {i["id"]: i for i in issues}
    w = r["working"].stage
    hit: dict[str, set[str]] = {}
    for e in r["evals"]:
        if e["row"].id in rows:
            for i in e["row"].issues:
                hit.setdefault(i, set()).add(e["row"].id)
    ents = {x.get("id"): x for x in r.get("relationships") or [] if isinstance(x, dict)}
    for rec in ((r.get("relationship_impact") or {}).get(w) or {}).get("records") or []:
        for eid in rec["path"]:
            for i in (ents.get(eid) or {}).get("issues") or []:
                hit.setdefault(i, set()).add(rec["target"])
    return [{"id": i, "text": _short((by_id.get(i) or {}).get("text", "(not in the open-issue register)"), 400),
             "owner": (by_id.get(i) or {}).get("owner", ""), "via": sorted(v)} for i, v in sorted(hit.items())]


# ---------------------------------------------------------------------------------------------- conditional scenarios

def _context_texts(r: dict, state: dict, *texts: str) -> str:
    """The texts plus the text of every unit id they name (a reason naming 'ADD-03:7.1' brings 7.1's words)."""
    out = [t or "" for t in texts]
    for t in texts:
        for uid in dict.fromkeys(_UNIT_REF.findall(t or "")):
            u = state.get(uid.rstrip(".,;)"))
            if u is not None:
                out.append(u.text or "")
    return "\n".join(out)


def _changes_a_date(before: str | None, after: str | None) -> bool:
    """Whether the words of a state change a date or a number (a period in days, a deadline): then the programme of
    that state would differ and is not computed here."""
    b, a = before or "", after or ""
    return [d["date"] for d in printed_dates(b)] != [d["date"] for d in printed_dates(a)] or \
        re.findall(r"\d+", b) != re.findall(r"\d+", a)


def modelled_conditions(r: dict, prog_c: dict | None = None) -> list[dict]:
    """The conditional amendments the engine models (amend.Condition on an op; StageResult.conditions at the working
    stage, including those stated earlier and still pending), each with the rows whose evaluation lists it (their
    `conditional` records), the trigger deadline's planning value (the row's deadline rule, else the A5 decision
    milestone of the condition) and both states. Never assumes the trigger occurred."""
    w = r["working"]
    ew = {e["row"].id: e["stages"][w.stage] for e in r["evals"]}
    ms = {(m.get("decision") or {}).get("condition"): m for m in (prog_c or {}).get("milestones") or [] if m.get("decision")}
    out = []
    for c in getattr(w, "conditions", None) or []:
        recs = {rid: x for rid, ev in ew.items() for x in ev.get("conditional") or [] if x.get("op") == c.get("op")}
        dl = next((x.get("deadline") for x in recs.values() if x.get("deadline")), None) or {}
        m = ms.get(c.get("condition"))
        deadline = dl.get("value") or (m or {}).get("date") or None
        states = c.get("if_triggered") or {}
        rows = sorted(recs) or _rows_citing(r, w.stage, set(c.get("targets") or []) | set(c.get("affects") or []))
        out.append({
            "id": f"SCENARIO-{c.get('condition')}-{c.get('op')}", "kind": "conditional", "what": "amendment",
            "stage": c.get("stated_at") or w.stage,
            "provision": c.get("provision"), "op": c.get("op"), "condition": c.get("condition"),
            "applied": c.get("state") == "triggered", "state": c.get("state"), "fact": c.get("fact"),
            "source": "conditional model (amend.Condition on the op)", "fields": {},
            "why": _short(c.get("applicability"), 300),
            "trigger": _short(f"{c.get('trigger')} ({c.get('trigger_unit')})", 300),
            "trigger_deadline": deadline, "deadline_words": (c.get("deadline") or {}).get("text") or dl.get("text"),
            "effective_from": None, "dates_printed": [d["date"] for d in printed_dates(str(c.get("trigger") or ""))],
            "if_triggered": "; ".join(f"{u}: “{_short(v.get('before'), 90)}” -> “{_short(v.get('after'), 90)}”"
                                      for u, v in states.items()) or "the op's change (see A2)",
            "if_not_triggered": c.get("if_not_triggered") or "the units stay as they stand (the op is not applied)",
            "changes_a_date": any(_changes_a_date(v.get("before"), v.get("after")) for v in states.values()),
            "rows": rows, "milestone": (m or {}).get("id"),
            "model": f"conditional model; state {c.get('state')}"
                     + (" (no person has recorded the trigger: nothing assumed)" if c.get("state") == "pending" else "")})
    return out


def conditional_scenarios(r: dict, prog_c: dict | None = None) -> list[dict]:
    """Conditional and effective-dated amendments of the pending stages: first those the engine models
    (modelled_conditions), then ops with `effective_from`, then what the op file says in words only: an op whose fields
    (scenario_fields) or note/issue say it is conditional or effective-dated, or an unresolved provision whose reason
    does. Each with the trigger words, the dates printed (the trigger deadline: the first date after 'by', 'before', 'not
    later than' ...), the two states and the rows they reach. A trigger is never assumed to have occurred."""
    out = modelled_conditions(r, prog_c)
    seen = {x["op"] for x in out}
    for s in pending(r):
        prev = _prev_state(r, s)
        for x in s.ops:
            o = x.op
            if o.id in seen or getattr(o, "condition", None) is not None:
                continue
            dumped = o.model_dump(exclude_none=True)
            fields = {k: dumped.get(k, x.details.get(k)) for k in scenario_fields if dumped.get(k) or x.details.get(k)}
            text = " ".join(filter(None, [o.note, o.issue]))
            kind = ("conditional" if fields.get("condition") or fields.get("trigger") or fields.get("conditional")
                    or _COND.search(text) or _COND_CS.search(text) else
                    "effective-dated" if fields.get("effective_from") or fields.get("effective_date") or _EFFECTIVE.search(text)
                    else None)
            if not kind:
                continue
            prov = s.state.get(o.provision)
            ctx = _context_texts(r, s.state, prov.text if prov else "", text)
            out.append(_scenario(r, s, kind, o.provision, ctx, text, fields, op=o.id, applied=x.applied,
                                 targets={o.target, *o.targets, *x.changed} - {None}))
        for c in s.coverage:
            if c["disposition"] not in UNRES:
                continue
            reason = c.get("reason") or ""
            u = s.state.get(c["provision"])
            words = u.text if u else c.get("text", "")
            kind = ("conditional" if _COND.search(reason) or _COND.search(words) else
                    "effective-dated" if _EFFECTIVE.search(reason) or _EFFECTIVE.search(words) else None)
            if not kind:
                continue
            ctx = _context_texts(r, s.state, words, reason)
            out.append(_scenario(r, s, kind, c["provision"], ctx, reason, {}, op=None, applied=False,
                                 targets=_cited(prev, words)))
    # a conditional provision with no date of its own takes the trigger deadline of a conditional provision of the same
    # section ('Where this Section 7 has effect' and 7.1's 'by 12 November 2026'); said so, never silently
    sec = lambda p: (p or "").rsplit(".", 1)[0] if "." in (p or "").split(":", 1)[-1] else None  # noqa: E731
    for x in out:
        if x["kind"] != "conditional" or x["trigger_deadline"]:
            continue
        doc = (x["provision"] or "").split(":", 1)[0]
        named = {f"{doc}:{n}" for n in re.findall(r"\bSection (\d+)\b", x["why"] + " " + x["trigger"])}
        mine = ({sec(x["provision"])} - {None}) | named          # its own section, and a Section N its words name
        if mine:
            y = next((y for y in out if y is not x and y["kind"] == "conditional" and y["trigger_deadline"]
                      and sec(y["provision"]) in mine), None)
            if y is not None:
                x["trigger_deadline"] = y["trigger_deadline"]
                how = "the same section" if sec(y["provision"]) == sec(x["provision"]) else "the Section its words name"
                x["why"] = _short(f"trigger deadline taken from {y['provision']} ({how}). " + x["why"], 400)
    return out


def _scenario(r: dict, s, kind: str, provision: str, ctx: str, why: str, fields: dict, op: str | None, applied: bool,
              targets: set[str]) -> dict:
    w = r["working"].stage
    dates = printed_dates(ctx)
    worded = sorted({d["date"] for d in dates if d["deadline"] and len(d["date"]) == 10})
    if fields.get("trigger_deadline") or fields.get("deadline"):
        deadline = str(fields.get("trigger_deadline") or fields.get("deadline"))
    elif kind == "effective-dated":
        deadline = None
    else:                                    # the earliest date printed after a deadline word (conservative planning)
        deadline = worded[0] if worded else None
    effective = (str(fields.get("effective_from") or fields.get("effective_date") or fields.get("applies_from") or "")
                 or (next((d["date"] for d in dates if not d["deadline"]), None) if kind == "effective-dated" else None))
    m = _COND.search(ctx) or _COND_CS.search(ctx) or _EFFECTIVE.search(ctx)
    trig = _short(ctx[max(0, m.start() - 60): m.end() + 200], 300) if m else ""
    rows = _rows_citing(r, w, targets) if targets else []
    what = "amendment" if kind == "effective-dated" or _AMENDMENT.search(ctx) else "obligation"
    if what == "obligation":                 # 'CONDITION: only a Bidder whose ...': it applies only if a fact holds
        yes = f"the obligation applies (as the candidate shows it{f': {op} applied' if applied else ''})"
        no = "it does not apply to this Bidder; a person records the fact (a bidder fact or an event), nothing is assumed"
    elif applied:
        yes = f"as the candidate shows it ({op} applied)"
        no = f"as validated at {r['validated'].stage} for what {op} changes ({op} would not stand)"
    else:
        yes = f"the provision's words would apply ({provision} is not applied in the candidate: a person writes the op)"
        no = f"the candidate stands for what {provision} names (nothing applied for it)"
    if len(worded) > 1:
        why = (f"several deadline dates printed ({', '.join(worded)}): the earliest is planned; a person reads which "
               f"governs. " + why)
    return {"id": f"SCENARIO-{provision}" + (f"-{op}" if op else ""), "kind": kind, "what": what, "stage": s.stage,
            "provision": provision,
            "op": op, "condition": None, "applied": applied, "state": "applied" if applied else "not applied",
            "fact": None, "source": ("op fields " + ", ".join(sorted(fields))) if fields else
            ("op note/issue" if op else "unresolved provision's reason"),
            "fields": {k: (v if isinstance(v, (str, int, float, bool)) else json.loads(json.dumps(v, default=str)))
                       for k, v in fields.items()},
            "why": _short(why, 400), "trigger": trig, "trigger_deadline": deadline, "deadline_words": None,
            "effective_from": effective, "dates_printed": [d["date"] for d in dates], "if_triggered": yes,
            "if_not_triggered": no, "changes_a_date": None, "rows": rows, "milestone": None,
            "model": "op fields" if fields else
                     "text only: the op file carries no conditional model for it; dates as printed, not computed"}


# ---------------------------------------------------------------------------------------------- image-read units

def image_units(r: dict, rows_in_play: set[str]) -> list[dict]:
    """The image-read units the pending stages touch (their own image readings, units an op changes or names, units an
    unresolved provision names, units cited by the rows in play or reached through relationships), grouped by region,
    each with its words verbatim, its translation kept apart (a proposal, not evidence), its table context (column,
    headings, notes, qualifier), its units of measure, its uncertainties and its crops; with the build's review packet of
    the region (crops beside the reading). Regions not touched are listed with their packet so they stay available."""
    w = r["working"].stage
    img = {u["unit_id"]: u for u in r["units"] if u.get("origin") == "image_reading"}
    touched: dict[str, list[str]] = {}

    def hit(uid, why):
        if uid in img and why not in touched.setdefault(uid, []):
            touched[uid].append(why)
    for s in pending(r):
        for uid, u in img.items():
            if u["doc"] == s.addendum:
                hit(uid, f"read from {s.stage}'s own image (a new reading)")
        for x in s.ops:
            for k in {x.op.target, x.op.anchor, *x.op.targets, *x.changed} - {None}:
                hit(k, f"{'changed' if x.applied and k in x.changed else 'named'} by {x.op.id}"
                       + ("" if x.applied else " (not applied)"))
        for c in s.coverage:
            if c["disposition"] in UNRES:
                u = s.state.get(c["provision"])
                for k in _cited(_prev_state(r, s), u.text if u else ""):
                    hit(k, f"named by the unresolved provision {c['provision']}")
    rows = {e["row"].id: e["row"] for e in r["evals"]}
    for rid in sorted(rows_in_play):
        for uid in rows[rid].units if rid in rows else []:
            hit(uid, f"cited by {rid} (in play at {w})")
    for rec in ((r.get("relationship_impact") or {}).get(w) or {}).get("records") or []:
        hit(rec["target"], f"reached via {' > '.join(rec['path'])}")
        for uid in rows[rec["target"]].units if rec["target"] in rows else []:
            hit(uid, f"cited by {rec['target']}, reached via {' > '.join(rec['path'])}")
    st = r["working"].state
    by_region: dict[str, list[str]] = {}
    for uid, u in img.items():
        by_region.setdefault(u.get("region") or (u.get("reading") or {}).get("region") or "?", []).append(uid)
    issues_of = {}
    for e in r["evals"]:
        for uid in e["row"].units:
            issues_of.setdefault(uid, set()).update(e["row"].issues)
    out = []
    for region in sorted(by_region):
        pk = Path(r["evidence_dir"]) / "review" / region / "packet.json"
        try:
            packet = json.loads(pk.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            packet = {}
        units = []
        for uid in by_region[region]:
            if uid not in touched:
                continue
            u, now = img[uid], st.get(uid)
            ctx = u.get("context") or {}
            cells = u.get("cells") or {}
            units.append({
                "unit": uid, "kind": u.get("kind"), "label": u.get("label"), "lang": u.get("lang"),
                "text": u.get("text", ""), "cells": cells, "translation": u.get("translation") or "",
                "table": {k: ctx.get(k) for k in ("table_title", "column_headings", "qualifier", "notes",
                                                  "interpretation_note") if ctx.get(k)},
                "parent": u.get("parent"), "measure": cells.get("Unit") or "",
                "uncertain": list(u.get("uncertain") or []),
                "reading_status": (u.get("reading") or {}).get("status"),
                "candidate": ({"status": now.status, "text": now.text, "cells": now.cells, "changed_by": list(now.history)}
                              if now is not None and (now.status != "active" or now.text != u.get("text", "")
                                                      or (now.cells or {}) != cells) else None),
                "crops": [a.get("crop") for a in u.get("anchors") or [] if a.get("crop")]
                         + sorted({c for a in u.get("anchors") or [] for c in (a.get("cell_crops") or {}).values()}),
                "issues": sorted(issues_of.get(uid, set())), "touched": touched[uid]})
        out.append({"region": region, "doc": packet.get("doc") or (img[by_region[region][0]]["doc"]),
                    "page": packet.get("page"), "status": packet.get("status") or "",
                    "packet": f"review/{region}/packet.html", "packet_md": f"review/{region}/packet.md",
                    "uncertainties": [_short(x, 400) for x in packet.get("decisions") or []],
                    "touched": bool(units), "units": units})
    return out


# ---------------------------------------------------------------------------------------------- everything

def compute(r: dict, a3v: dict | None = None, prog_v: dict | None = None, prog_c: dict | None = None,
            op_status: dict | None = None) -> dict | None:
    """The candidate (see the module docstring) for a stage2 run, or None when there is no working stage. `a3v` and
    `prog_v` are the validated A3 data and programme (computed here when not given); `prog_c` the extended programme of
    the working stage; `op_status` op id -> the controller's status, shown beside each op."""
    from . import stage2
    if not r.get("working"):
        return None
    v, w = r["validated"].stage, r["working"].stage
    stages_by = {s.stage: s for s in r["stages"]}
    if prog_v is None and stages_by[v].issued:
        prog_v = programme.stage_planner(r, v)(r["assumptions"])
    if prog_c is None and r["working"].issued:
        prog_c = programme.stage_planner(r, w)(r["assumptions"])
    if a3v is None:
        a3v = stage2.a3(r, stage2.collect_issues(r, prog_v), prog_v)
    rc = dict(r, validated=r["working"], working=None)          # the working stage seen as if it were validated
    pend = pending(r)
    issues_c = [i for i in stage2.collect_issues(rc, prog_c) if i["id"] not in {f"I-PARTIAL-{s.stage}" for s in pend}]
    a3c = stage2.a3(rc, issues_c, prog_c)
    a3c["title"] = f"A3 CANDIDATE — {w} as proposed ({BANNER})"
    a3c["subtitle"] = a3c["subtitle"].replace(f"Validated state {w}", f"Candidate state {w} (NOT validated: the "
                                              f"validated state is {v})", 1)
    a3c["banner"] = f"{BANNER}. " + a3c["banner"]
    unres = unresolved_rows(r)
    changes = a3_changes(r, a3v, a3c, op_status, unres)
    blk = blockers(r, unres, prog_c, issues_c)
    scen = conditional_scenarios(r, prog_c)
    imp = (r.get("relationship_impact") or {}).get(w) or {}
    in_play = ({c["row"] for c in changes} | set(unres) | set(imp.get("direct_rows") or [])
               | {rec["target"] for rec in imp.get("records") or []})
    in_play &= {e["row"].id for e in r["evals"]}
    applied = [op_info(r, x, op_status) for s in pend for x in s.ops if x.applied]
    cand = {"banner": BANNER, "validated_stage": v, "stage": w, "issued": r["working"].issued,
            "pending": [{"stage": s.stage, "status": s.status, "issued": s.issued, "provisions": len(s.coverage),
                         "unresolved": sum(1 for c in s.coverage if c["disposition"] in UNRES),
                         "ops": len(s.ops), "applied": sum(1 for x in s.ops if x.applied)} for s in pend],
            "ops": applied, "a3": a3c, "changes": changes, "blockers": blk, "scenarios": scen,
            "open_issues_in_play": open_issues_in_play(r, in_play, issues_c),
            "images": image_units(r, in_play), "issues": issues_c}
    cal = r["register"].cal_by_stage[w]
    if prog_c is not None:
        ev = {e["row"].id: e["stages"][v] for e in r["evals"]}
        ew = {e["row"].id: e["stages"][w] for e in r["evals"]}
        moved_rows, date_rows = {}, set()
        for e in r["evals"]:
            a, b = ev[e["row"].id], ew[e["row"].id]
            dates_moved = [d["planning"] for d in (a["dates"] if in_force(a["status"]) else [])] != \
                [d["planning"] for d in b["dates"]]
            if in_force(b["status"]) and (not in_force(a["status"]) or dates_moved or a.get("ops") != b.get("ops")
                                          or a.get("interpretation") != b.get("interpretation")):
                moved_rows[e["row"].id] = row_sources(r, e["row"].id)["ops"]
                if dates_moved:
                    date_rows.add(e["row"].id)
        cand["a5"] = programme.candidate_replan(prog_v, prog_c, ev, ew, cal, blocked=unres, row_ops=moved_rows,
                                                date_rows=date_rows, scenarios=scen, label=f"{w} [{BANNER}]")
    else:
        cand["a5"] = None
    cand["paragraph"] = paragraph(cand)
    return cand


def _ids(xs, n: int = 6) -> str:
    xs = list(xs)
    return ", ".join(xs[:n]) + (f" and {len(xs) - n} more" if len(xs) > n else "") if xs else "none"


def paragraph(c: dict) -> str:
    """One paragraph: what may be changing although the addendum is partial."""
    v, w = c["validated_stage"], c["stage"]
    p = c["pending"]
    unres = sum(x["unresolved"] for x in p)
    provs = sum(x["provisions"] for x in p)
    ch = c["changes"]
    by = lambda k: [f"{x['row']} ({', '.join(o['op'] for o in x['ops']) or 'register'})" for x in ch if x["change"] == k]  # noqa: E731
    rv = {}
    for o in c["ops"]:
        k = o["controller"] or f"review {o['review']}"
        rv[k] = rv.get(k, 0) + 1
    t = (f"{', '.join(x['stage'] for x in p)} {'is' if len(p) == 1 else 'are'} PARTIAL: {unres} of {provs} provisions "
         f"unresolved, so A3 and A5 stay validated at {v}. If the {len(c['ops'])} op(s) that are valid there stood (each "
         f"still a proposal: {', '.join(f'{k} {n}' for k, n in sorted(rv.items())) or 'none'}), A3 would gain "
         f"{len(by('enters'))} row(s) ({_ids(by('enters'), 4)}), lose {len(by('leaves'))} ({_ids(by('leaves'), 4)}) and "
         f"change {len(by('changes'))} ({_ids(by('changes'), 4)})")
    a5 = c.get("a5")
    if a5:
        s = a5["summary"]
        t += (f"; A5, replanned at {w}'s issue date ({a5['status_date']}), would move the latest dates of "
              f"{len(s['moved'])} activit{'y' if len(s['moved']) == 1 else 'ies'} ({_ids(s['moved'], 4)}), add "
              f"{len(s['new'])} ({_ids(s['new'], 4)}) and remove {len(s['removed'])} ({_ids(s['removed'], 4)}), and marks "
              f"{len(s['review'])} REVIEW through relationships")
    b = c["blockers"]
    t += (f". Not settled: {len(b['blocked_activities'])} activit{'y' if len(b['blocked_activities']) == 1 else 'ies'} "
          f"blocked by an unresolved row ({_ids([x['activity'] for x in b['blocked_activities']], 4)}), "
          f"{len(b['stale_rows'])} STALE row(s), {len(b['c46'])} obligation(s) reaching no output (C46), "
          f"{len(b.get('chains') or [])} relationship chain(s) blocked or incomplete, "
          f"{len(b['conflicts'])} conflict(s); documents not supplied: "
          f"{_ids([m['document'] or m['id'] for m in b['missing_documents']], 4)}")
    if c["scenarios"]:
        t += ("; conditional or effective-dated: " + "; ".join(
            f"{x['provision']} ({x['kind']} {x.get('what', '')}" + (f", decision by {x['trigger_deadline']}" if x["trigger_deadline"] else "")
            + (f", effective {x['effective_from']}" if x["effective_from"] else "") + ")" for x in c["scenarios"][:4]))
    return t + ". Nothing here is validated, accepted or applied to the real state."


# ---------------------------------------------------------------------------------------------- markdown

def _md(t) -> str:
    return str(t if t is not None else "").replace("|", "/").replace("\n", " ")


def markdown(c: dict) -> str:
    a3c = c["a3"]
    L = [f"# A3 CANDIDATE — {c['stage']} as proposed, NOT VALIDATED", "",
         f"> **{BANNER}.** The validated A3 (`a3.pdf`, one page) stays at **{c['validated_stage']}**. This candidate applies "
         f"the ops of {', '.join(x['stage'] for x in c['pending'])} that are valid and not withheld; it is a view for review, "
         "not a deliverable. It is not held to the one-page rule (C43 applies to the validated A3 only)"
         + (f": the PDF runs to {c['pages']} page(s)." if c.get("pages") else "."), "",
         "## What may be changing", "", c["paragraph"], "",
         f"## Changes against the validated A3 ({len(c['changes'])})", ""]
    for x in c["changes"]:
        L.append(f"- **{x['change'].upper()} {x['row']}** — {_md('; '.join(x['what']))} (row {x['status_validated']} -> "
                 f"{x['status_candidate']}; review {x['row_review']}" + ("; STALE" if x["stale"] else "") + ")")
        L += [f"  - source op {_md(o['label'])}" for o in x["ops"]] + [f"  - {_md(y)}" for y in x["why"]]
    if not c["changes"]:
        L.append("- none: no row enters, leaves or changes")
    L += ["", "## The candidate A3 (every section in full)", "", f"_{_md(a3c['subtitle'])}_", ""]
    marks = {x["row"]: x["change"].upper() for x in c["changes"]}
    for sec in a3c["sections"]:
        L += [f"### {sec['heading']}", ""] + ([f"_{sec['note']}_", ""] if sec.get("note") else [])
        for it in sec["items"]:
            L.append(f"- {'[' + marks[it['id']] + '] ' if it['id'] in marks else ''}**{it['id']}** {_md(it['text'])}"
                     + (f" — {it.get('class', '')}: “{_md(it['consequence'])}”" if it.get("consequence") else "")
                     + (f" [{_md(it.get('source'))}]" if it.get("source") else "")
                     + (f" — flags: {_md('; '.join(it['flags']))}" if it.get("flags") else ""))
        if sec.get("ids"):
            L.append(", ".join(f"{'[' + marks[i] + '] ' if i in marks else ''}{i}" for i in sec["ids"]))
        L.append("")
    b = c["blockers"]
    L += ["## Blockers (what stops the candidate becoming the validated state, or what it cannot establish)", "",
          f"### Unresolved provisions ({len(b['provisions'])})", ""]
    L += [f"- **{x['provision']}** ({x['stage']}, p{x['page']}; {x['kind']}): {_md(x['reason'])} — words: “{_md(x['text'])}”; "
          f"rows: {_ids(x['rows'], 12)}; activities: {_ids(x['activities'], 12)}" for x in b["provisions"]] or ["- none"]
    L += ["", f"### Invalid or withheld ops ({len(b['invalid_ops']) + len(b['withheld_ops'])})", ""]
    L += [f"- INVALID {x['op']} ({x['provision']}): {_md(x['failed'])}" for x in b["invalid_ops"]]
    L += [f"- WITHHELD {x['op']} ({x['provision']}): rejected by a person" for x in b["withheld_ops"]]
    if not b["invalid_ops"] and not b["withheld_ops"]:
        L.append("- none")
    L += ["", f"### Rows not settled in the candidate ({len(b['unresolved_rows'])})", ""]
    L += [f"- {x['row']}: {_md('; '.join(x['why']))}" for x in b["unresolved_rows"]] or ["- none"]
    L += ["", f"### Activities blocked by an unresolved row ({len(b['blocked_activities'])})", ""]
    L += [f"- {x['activity']} ({_md(x['name'])}): rows {', '.join(x['rows'])}" for x in b["blocked_activities"]] or ["- none"]
    L += ["", f"### Obligations reaching no output (C46) ({len(b['c46'])})", ""]
    L += [f"- {x['op']} [{x['output']}]: {_md(x['detail'])}" for x in b["c46"]] or ["- none"]
    ch = b.get("chains") or []
    L += ["", f"### Relationship chains blocked or incomplete ({len(ch)})", ""]
    L += [f"- {x['target']} via {' > '.join(x['path'])}: "
          + "; ".join([f"BLOCKED: {y['document']} not supplied ({y['entry_id']}): cannot be established: "
                       f"{_md(_short(y['blocks'], 200))}" for y in x["blockers"]]
                      + ([f"CHAIN INCOMPLETE ({x['truncated_by'] or 'bound'}); not followed: {', '.join(x['unfollowed'])}"]
                         if x["completeness"] == "truncated" else [])
                      + ([f"CYCLIC: {' > '.join(x['cycle'])}"] if x["completeness"] == "cyclic" else []))
          for x in ch] or ["- none"]
    L += ["", f"### Documents referenced but not supplied ({len(b['missing_documents'])})", ""]
    L += [f"- **{x['id']}**" + (f" {x['document']}" if x["document"] else "") + f": {_md(x['blocks'])}"
          + (f" — reached by this addendum: {_ids(x['reached_by_this_addendum'], 8)}" if x["reached_by_this_addendum"] else
             " — not reached by this addendum's changes; still open")
          + (f" (issues {', '.join(x['issues'])})" if x["issues"] else "") for x in b["missing_documents"]] or ["- none"]
    L += ["", f"### Conflicts ({len(b['conflicts'])})", ""]
    L += [f"- {_md(x['what'])} ({x['source']})" for x in b["conflicts"]] or ["- none"]
    L += ["", f"### Issues the ops raise ({len(b['op_issues'])})", ""]
    L += [f"- {x['op']}{'' if x['applied'] else ' (not applied)'}: {_md(x['issue'])}" for x in b["op_issues"]] or ["- none"]
    L += ["", f"### Open issues in play (kept open; never resolved here) ({len(c['open_issues_in_play'])})", ""]
    L += [f"- **{x['id']}** ({x['owner']}): {_md(x['text'])} — via {_ids(x['via'], 6)}" for x in c["open_issues_in_play"]] or ["- none"]
    L += ["", f"## Conditional scenarios ({len(c['scenarios'])})", ""]
    for x in c["scenarios"]:
        L += [f"- **{x['provision']}** ({x['kind']} {x.get('what', '')}; {x['source']}; {'applied' if x['applied'] else 'not applied'} in the candidate)"
              + (f": decision by **{x['trigger_deadline']}**" if x["trigger_deadline"] else "")
              + (f"; effective from {x['effective_from']}" if x["effective_from"] else ""),
              f"  - trigger words: “{_md(x['trigger'])}”" if x["trigger"] else "  - trigger words: none found",
              f"  - if triggered: {_md(x['if_triggered'])}; if not: {_md(x['if_not_triggered'])}",
              f"  - rows: {_ids(x['rows'], 10)}; dates printed: {', '.join(x['dates_printed']) or 'none'}; {x['model']}"]
    if not c["scenarios"]:
        L.append("- none found in the op file (no op or unresolved provision says it is conditional or effective-dated)")
    L += ["", "## Image-read units (crops, Arabic verbatim, translations apart, table context, units, uncertainties)", "",
          "Each region's review packet in the evidence build shows every crop beside its reading; translations are "
          "proposals, never evidence; what a value means (maximum, range, target) is decided by a person.", ""]
    for g in c["images"]:
        L.append(f"- **{g['region']}** ({g['doc']} p{g['page']}; reading {g['status']}): packet `<evidence build>/{g['packet']}`"
                 + ("" if g["touched"] else f" — not touched by {c['stage']}; kept available"))
        L += [f"  - uncertainty: {_md(u)}" for u in g["uncertainties"][:8]]
        for u in g["units"]:
            words = u["text"] or "; ".join(f"{k}: {v}" for k, v in u["cells"].items())
            L.append(f"  - `{u['unit']}` ({u['kind']}; {u['lang'] or 'table'}): “{_md(words)}”"
                     + (f" — translation (proposal, not evidence): ‘{_md(u['translation'])}’" if u["translation"] else "")
                     + (f" — unit {u['measure']}" if u["measure"] else "")
                     + (f" — table: {_md(json.dumps(u['table'], ensure_ascii=False))}" if u["table"] else "")
                     + (f" — at {c['stage']}: {_md(u['candidate']['status'])} “{_md(u['candidate']['text'] or u['candidate']['cells'])}”"
                        f" (by {', '.join(u['candidate']['changed_by'])})" if u["candidate"] else "")
                     + (f" — uncertain: {_md('; '.join(u['uncertain']))}" if u["uncertain"] else "")
                     + (f" — issues {', '.join(u['issues'])}" if u["issues"] else "")
                     + f" — touched: {_md('; '.join(u['touched']))}")
    g = a3c.get("groups") or {}
    L += ["", f"## {g.get('heading', 'Open issues')}", ""]
    for grp in g.get("groups") or []:
        L.append(f"- **{grp['title']}** ({len(grp['items'])}): " + "; ".join(f"{i['id']} {i['short']}" for i in grp["items"])
                 + (f" — questions drafted: {', '.join(grp['questions'])}" if grp.get("questions") else ""))
    L += ["", f"Ops standing in the candidate ({len(c['ops'])}): " + "; ".join(o["label"] for o in c["ops"]), ""]
    return "\n".join(L)


# ---------------------------------------------------------------------------------------------- files

def write(r: dict, out: Path, a3v: dict | None, prog_v: dict | None, prog_c: dict | None = None,
          op_status: dict | None = None) -> list[Path]:
    """out/a3/a3_candidate.{json,md,html,pdf} and out/a5/candidate/ (see the module docstring); [] without a working
    stage. Nothing else under `out` is written or changed."""
    from .render import candidate_a3_html, write_candidate_a3_pdf
    c = compute(r, a3v, prog_v, prog_c, op_status)
    if c is None:
        return []
    out = Path(out)
    paths = []
    fit = write_candidate_a3_pdf(c, out / "a3" / "a3_candidate.pdf")
    c["pages"] = fit["pages"]
    paths.append(out / "a3" / "a3_candidate.pdf")
    write_text(out / "a3" / "a3_candidate.html", candidate_a3_html(c, standalone=True))
    write_text(out / "a3" / "a3_candidate.md", markdown(c) + "\n")
    dump_json({k: v for k, v in c.items() if k != "a5"} | {"a5": _a5_summary(c)}, out / "a3" / "a3_candidate.json")
    paths += [out / "a3" / "a3_candidate.html", out / "a3" / "a3_candidate.md", out / "a3" / "a3_candidate.json"]
    if c.get("a5"):
        paths += programme.write_candidate(c["a5"], out / "a5" / "candidate", c["paragraph"])
    return paths


def _a5_summary(c: dict) -> dict | None:
    a5 = c.get("a5")
    if not a5:
        return None
    return {"files": "a5/candidate/", "status_date": a5["status_date"], "summary": a5["summary"],
            "moved": [x for x in a5["changes"] if "MOVED" in x["change"]]}


def review_lines(out: Path, build: Path | None, rel, op_status: dict | None = None) -> list[str]:
    """Markdown lines for an AI workflow review packet: the validated and the candidate A3/A5 side by side, the paragraph,
    the rows that move on A3 with their ops (and the controller's statuses when given), the blockers and the image-read
    units with their review packets. `rel(path)` makes a link relative to the packet; [] when there is no candidate."""
    out = Path(out)
    f = out / "a3" / "a3_candidate.json"
    try:
        c = json.loads(f.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    link = lambda p, t=None: f"[{t or p}]({rel(out / p)})"  # noqa: E731
    L = ["### Validated and candidate A3 / A5 (partial should not mean useless)", "",
         f"- **Validated** (unchanged; {c['validated_stage']}): {link('a3/a3.pdf')} (one page), {link('a5/README.md')}, "
         f"{link('a5/gantt.html')}",
         f"- **Candidate** ({BANNER}; {c['stage']} as proposed): {link('a3/a3_candidate.pdf')} "
         f"({c.get('pages')} page(s)), {link('a3/a3_candidate.md')}, {link('a5/candidate/README.md')}, "
         f"{link('a5/candidate/gantt.html')}", "", f"**What may be changing.** {c['paragraph']}", ""]
    st = op_status or {}
    for x in c.get("changes") or []:
        L.append(f"- {x['change'].upper()} {x['row']}: {_md('; '.join(x['what']))}; ops "
                 + (", ".join(o["op"] + (f" ({st.get(o['op']) or o.get('controller') or 'review ' + o['review']})")
                              for o in x["ops"]) or "none (" + _md("; ".join(x["why"])) + ")"))
    b = c.get("blockers") or {}
    L += ["", f"- blockers: {len(b.get('provisions') or [])} unresolved provision(s), {len(b.get('blocked_activities') or [])} "
          f"blocked activit(y/ies), {len(b.get('stale_rows') or [])} STALE row(s), {len(b.get('c46') or [])} C46 gap(s), "
          f"{len(b.get('chains') or [])} relationship chain(s) blocked or incomplete, "
          f"{len(b.get('conflicts') or [])} conflict(s); documents not supplied: "
          + (", ".join(m.get("document") or m["id"] for m in b.get("missing_documents") or []) or "none"),
          f"- conditional scenarios: {len(c.get('scenarios') or [])}"
          + "".join(f"; {x['provision']} ({x['kind']} {x.get('what', '')}" + (f", decision by {x['trigger_deadline']}" if x["trigger_deadline"] else "")
                    + ")" for x in c.get("scenarios") or []), ""]
    imgs = c.get("images") or []
    if imgs:
        L += ["**Image-read units** (the review packet of each region shows every crop beside its reading; translations "
              "are proposals, not evidence):", ""]
        for g in imgs:
            pk = (Path(build) / g["packet"]) if build else None
            L.append(f"- {g['region']} ({g['doc']} p{g['page']}; reading {g['status']}): "
                     + (f"[packet]({rel(pk)})" if pk is not None and pk.exists() else f"`{g['packet']}` in the evidence build")
                     + (f"; {len(g['units'])} unit(s) touched" if g["touched"] else "; not touched by this addendum"))
            for u in g["units"][:12]:
                words = u["text"] or "; ".join(f"{k}: {v}" for k, v in (u.get("cells") or {}).items())
                L.append(f"  - `{u['unit']}`: “{_md(_short(words, 200))}”"
                         + (f"; translation (apart): ‘{_md(_short(u['translation'], 160))}’" if u.get("translation") else "")
                         + (f"; unit {u['measure']}" if u.get("measure") else "")
                         + (f"; uncertain: {_md(_short('; '.join(u['uncertain']), 200))}" if u.get("uncertain") else "")
                         + (f"; issues {', '.join(u['issues'])}" if u.get("issues") else ""))
            if len(g["units"]) > 12:
                L.append(f"  - … {len(g['units']) - 12} more in `a3/a3_candidate.md`")
        L.append("")
    return L


def diff_lines(r: dict, to: str) -> tuple[list[str], dict]:
    """For `tenderpack diff` when `to` is past the validated stage: where the validated and the candidate outputs are,
    and the paragraph. ([], {}) otherwise."""
    order = r["order"]
    if not r.get("working") or order.index(to) <= order.index(r["validated"].stage):
        return [], {}
    c = compute(r)
    lines = ["### Validated vs candidate (partial should not mean useless)", "",
             f"- validated (unchanged, {c['validated_stage']}): `<outputs>/a3/a3.pdf` (one page), `<outputs>/a5/`",
             f"- candidate ({BANNER}, {c['stage']} as proposed): `<outputs>/a3/a3_candidate.pdf` / `.md`, "
             "`<outputs>/a5/candidate/`", "", f"**What may be changing.** {c['paragraph']}", ""]
    data = {"validated_stage": c["validated_stage"], "stage": c["stage"], "paragraph": c["paragraph"],
            "a3": {k: [x["row"] for x in c["changes"] if x["change"] == k] for k in ("enters", "leaves", "changes")},
            "blocked_activities": [x["activity"] for x in c["blockers"]["blocked_activities"]],
            "scenarios": [x["id"] for x in c["scenarios"]]}
    return lines, data
