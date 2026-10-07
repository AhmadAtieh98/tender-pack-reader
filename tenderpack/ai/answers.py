"""The controlled handoff of the owner's answers to a run (session 14, W5). The owner: "Notes that the workflow never
consumes are not enough. The answers need to actually flow into the controlled process ... My answers must not silently
approve interpretations or overwrite the validated baseline."

The owner answers a question of a PRELIMINARY AI BRIEFING (quick_review.record_answer: the answer, its kind, the
evidence it cites, the person, the time) and offers it to a run (quick_review.offer_answers: a note in
<run>/owner_answers/<qr id>.yaml with the run's staleness fingerprint; held while a step or batch runs). This module is
where the run TAKES it, at its safe checkpoints only (between steps, never under a running batch):

    CHECKPOINTS   "analysis"   after readings, before analysis
                  "downstream" before downstream
                  "promotion"  before promotion
    (workflow._drive calls at_checkpoint(ctx, step) before running each of these steps)

At a checkpoint, first every answer HELD for this run in a quick review's answers.yaml is offered (the checkpoint is a
safe point), then each offered note goes through:
  (a) evidence checks: an answer of kind `fact` must cite evidence (`page N: words` on the run's addendum, checked
      verbatim against its text layer by quick_review.quote_check; or `UNIT: words`, a unit of the run's workspace whose
      text holds the words); a fact with no evidence or with evidence not found is REFUSED with the reason. An answer of
      kind `judgment` is the owner's PROPOSED judgment with its owner (the person), never an approval.
  (b) staleness: the note's fingerprint (quick_review.fingerprint: the run's combined set, downstream set and candidate
      curation) must equal the run's now; otherwise the note is STALE and is not consumed until it is offered again.
  (c) approved readings: an answer citing a unit of an APPROVED reading (curation/approvals.yaml -> its reading file's
      unit_id, or the region) would change that reading's interpretation: it is recorded PENDING, never applied and never
      given to a batch; the approved reading changes only through the accept/reject workflow.
  (d) consumption and affected-work revalidation: the note's scope is the run's provisions whose text holds a quoted
      words of the question or the answer, or that a cited unit is the target or evidence of (from the run's combined
      set), else the provisions on a cited page. The done batches whose provisions (analysis) or tasks (downstream) are
      in that scope are RE-ASKED: reset to pending (their earlier items kept under `superseded`), the steps from that
      phase up to the checkpoint reset and run again at once (at_checkpoint), the checkpoint records which. A batch
      not asked yet simply receives the answer (`asked_with`).
A consumed answer reaches the next packets of the batches in its scope (with_packet, called by the workflow's packet
builders) under `owner_answers`: a CONSTRAINT item (a fact with verified evidence) or a CONTEXT item (a judgment), each
with the owner's name, times and the evidence checks, labelled PROPOSED and "never an approval". It is recorded as an
intervention by the person (checkpoint `interventions`: kind "owner answer consumed", by, ts) and, in the candidate, in
<run>/candidate/owner_answers.yaml (status PROPOSED or PENDING, decision "none: ... accept/reject"). Nothing here writes
curation/ or out/, approves, accepts or rejects anything, or closes a pending judgment. The state of every answer is
written back beside it (answers.yaml `handoff`: offered | stale | refused | pending | consumed, with the checkpoint and
the reason) for the panel.
"""
from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Callable

import yaml

CHECKPOINTS = {"analysis": "after readings, before analysis", "downstream": "before downstream",
               "promotion": "before promotion"}
KINDS = ("fact", "judgment")
STEP_OF_PHASE = {"analysis": "analysis", "downstream": "downstream"}
NEVER = ("an owner's answer is never an approval: it never approves an interpretation, never overwrites the validated "
         "baseline (curation/ and out/) and never closes a pending judgment; approvals happen only through the "
         "accept/reject workflow")
PACKET_NOTE = ("the owner's answers to questions of a preliminary AI briefing, taken at a safe checkpoint of this run; "
               "each is PROPOSED, never an approval: a `constraint` states a fact the owner backed with evidence the "
               "program found (stay consistent with it and cite that evidence itself, or say why it does not hold); "
               "a `context` item is the owner's proposed judgment (mention it; never resolve an ambiguity, close an "
               "issue or approve an interpretation on it: the item stays human-owned)")
CANDIDATE_FILE = "owner_answers.yaml"


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------------------------- evidence

_PAGE = re.compile(r"^\s*(?:p|page)\s*\.?\s*(\d+)\s*[:\-–]\s*(.+?)\s*$", re.I | re.S)


def parse_cite(c) -> dict:
    """A cite of an answer: a dict {page, quotation, unit_id}, or a line `page N: words` (the addendum) or
    `UNIT_ID: words` (a unit of the pack; the id is the text before the first ': ')."""
    from .quick_review import QuickReviewError
    if isinstance(c, dict):
        q = str(c.get("quotation") or "").strip()
        if not q:
            raise QuickReviewError(f"a cite needs the quoted words: {c!r}")
        return {"page": c.get("page"), "quotation": q, "unit_id": c.get("unit_id") or None}
    s = str(c or "").strip()
    m = _PAGE.match(s)
    if m:
        return {"page": int(m.group(1)), "quotation": m.group(2).strip(), "unit_id": None}
    if ": " in s:
        u, q = s.split(": ", 1)
        if u.strip() and q.strip() and " " not in u.strip():
            return {"page": None, "quotation": q.strip(), "unit_id": u.strip()}
    raise QuickReviewError(f"cite {s!r}: write `page N: the words` (the addendum) or `UNIT_ID: the words` (the pack)")


def check_cite(c: dict, pages: list[dict], unit_text: Callable[[str], str | None]) -> dict:
    """{cite, ok, check}: an addendum cite is checked verbatim on its page of the run's addendum (quote_check); a unit
    cite needs a unit of the run's workspace whose text holds the words."""
    from .quick_review import quote_check
    if c.get("unit_id"):
        t = unit_text(c["unit_id"])
        if t is None:
            return {**c, "ok": False, "check": f"{c['unit_id']} is not a unit of the run's workspace"}
        r = quote_check(c["quotation"], [{"page": 0, "text": t, "image_regions": [], "characters": len(t)}], 0)
        ok = r.startswith("verbatim")
        return {**c, "ok": ok, "check": (f"verbatim in {c['unit_id']}" if ok else
                                         f"the words are NOT in the text of {c['unit_id']}")}
    if not pages:
        return {**c, "ok": False, "check": "not checked: the run's addendum PDF is not readable here"}
    r = quote_check(c["quotation"], pages, c.get("page"))
    return {**c, "ok": r.startswith("verbatim"), "check": r}


def evidence_check(note: dict, pages: list[dict], unit_text) -> tuple[bool, list[dict], str]:
    """(passes, the checks of the answer's own evidence, the reason it is refused)."""
    cites = [parse_cite(c) for c in note.get("answer_evidence") or []]
    checks = [check_cite(c, pages, unit_text) for c in cites]
    if (note.get("answer_kind") or "judgment") != "fact":
        return True, checks, ""
    if not checks:
        return False, checks, ("the answer states a fact but cites no evidence: a fact reaches the run only with "
                               "evidence in the addendum (`page N: words`) or the pack (`UNIT_ID: words`)")
    bad = [c for c in checks if not c["ok"]]
    if bad:
        return False, checks, "the answer states a fact whose evidence was not found: " + "; ".join(
            f"{c.get('unit_id') or 'page ' + str(c.get('page'))}: “{c['quotation'][:80]}” ({c['check']})" for c in bad)
    return True, checks, ""


# ---------------------------------------------------------------------------------------------- approved readings

def approved_units(paths, root: Path) -> dict[str, str]:
    """{unit id or region id: region id} of every APPROVED reading in the approvals files given (a missing file is
    skipped): the region, and the reading file's unit_id (its sub-units are matched by prefix in touches_approved)."""
    out: dict[str, str] = {}
    for p in paths:
        p = Path(p)
        if not p.is_file():
            continue
        for a in (yaml.safe_load(p.read_text(encoding="utf-8")) or {}).get("approvals") or []:
            rid = a.get("region_id")
            if not rid:
                continue
            out[rid] = rid
            rf = (a.get("reading_file") or {}).get("path")
            f = Path(root) / rf if rf else None
            if f is not None and f.is_file():
                uid = (yaml.safe_load(f.read_text(encoding="utf-8")) or {}).get("unit_id")
                if uid:
                    out[str(uid)] = rid
    return out


def touches_approved(note: dict, approved: dict[str, str]) -> str | None:
    for c in _cites(note):
        u = c.get("unit_id")
        if not u:
            continue
        for k, rid in approved.items():
            if u == k or u.startswith(k + "/"):
                return (f"it cites {u}, a unit of the approved reading {rid}: an answer that would change an approved "
                        "reading's interpretation is recorded PENDING and never applied; the reading changes only "
                        "through the accept/reject workflow (an approved transcription is not an approved "
                        "interpretation either way)")
    return None


# ---------------------------------------------------------------------------------------------- scope

def _cites(note: dict) -> list[dict]:
    out = []
    for c in list(note.get("evidence") or []) + list(note.get("answer_evidence") or []):
        try:
            out.append(parse_cite(c))
        except ValueError:
            continue
    return out


def _n(s: str) -> str:
    from .quick_review import _norm
    return _norm(s).lower()


def _combined_units(rd: Path) -> dict[str, set[str]]:
    """{unit id: provisions whose combined-set items target it or cite it} (empty without a combined set)."""
    from .quick_review import _checkpoint, _combined_path
    try:
        p = _combined_path(rd, _checkpoint(rd))
    except (OSError, ValueError):
        return {}
    if p is None:
        return {}
    out: dict[str, set[str]] = {}
    for it in ((yaml.safe_load(p.read_text(encoding="utf-8")) or {}).get("proposal_set") or {}).get("items") or []:
        prov = it.get("provision")
        if not prov:
            continue
        for u in [it.get("target")] + [e.get("unit_id") for e in it.get("evidence") or [] if isinstance(e, dict)]:
            if u:
                out.setdefault(str(u), set()).add(prov)
    return out


def scope(note: dict, cp, rd: Path, unit_text) -> dict:
    """The run's work the answer concerns: {provisions, units, basis, scoped}."""
    provs = list(cp.data.get("provisions") or {})
    cites = _cites(note)
    hit: dict[str, str] = {}
    by_unit = _combined_units(rd)
    for p in provs:
        t = _n(unit_text(p) or "")
        for c in cites:
            q = _n(c["quotation"])
            if c.get("unit_id") == p:
                hit.setdefault(p, f"cites {p}")
            elif not c.get("unit_id") and t and q and (q in t or (len(t) >= 25 and t in q)):
                hit.setdefault(p, "its quoted words are in the provision")
            elif c.get("unit_id") and p in by_unit.get(c["unit_id"], ()):
                hit.setdefault(p, f"the provision's items target or cite {c['unit_id']}")
    if not hit:
        pages = {c.get("page") for c in cites if not c.get("unit_id") and c.get("page")}
        for p in provs:
            if pages & set((cp.data["provisions"][p] or {}).get("pages") or []):
                hit[p] = "a cited page of the addendum"
    units = sorted({c["unit_id"] for c in cites if c.get("unit_id")})
    return {"provisions": [p for p in provs if p in hit], "units": units,
            "basis": {p: hit[p] for p in provs if p in hit}, "scoped": bool(hit)}


def _task_matches(task, sc: dict) -> bool:
    if not sc.get("scoped"):
        return True
    s = task if isinstance(task, str) else json.dumps(task, ensure_ascii=False, default=str)
    return any(k and k in s for k in list(sc.get("provisions") or []) + list(sc.get("units") or []))


# ---------------------------------------------------------------------------------------------- the items

def context_item(note: dict, step: str, checks: list[dict], sc: dict, now: str) -> dict:
    fact = (note.get("answer_kind") or "judgment") == "fact"
    return {"id": note["id"], "role": "constraint" if fact else "context", "kind": "fact" if fact else "judgment",
            "status": "PROPOSED by the owner (not an approval)", "question": note.get("question"),
            "question_evidence": note.get("evidence"), "answer": note.get("answer"), "by": note.get("by"),
            "decision_owner": note.get("by"), "recorded": note.get("recorded"), "offered": note.get("offered"),
            "consumed": now, "checkpoint": CHECKPOINTS[step], "evidence_checks": checks,
            "applies_to": {"provisions": sc["provisions"], "units": sc["units"], "scoped": sc["scoped"]},
            "how_to_use": (
                "a fact the owner states with evidence the program found: stay consistent with it and cite that "
                "evidence itself, or say why it does not hold; it is never an approval of an interpretation"
                if fact else
                "the owner's PROPOSED judgment (owner: " + str(note.get("by")) + "): mention it where it bears; never "
                "resolve an ambiguity, close an issue or treat an interpretation as decided on it; it is never an "
                "approval and the item stays human-owned")}


def items_for(cp, phase: str, packet: dict) -> list[dict]:
    """The consumed answers a packet of `phase` carries: those whose scope holds one of its provisions (analysis) or
    tasks (downstream); an answer whose scope was not established reaches every next packet."""
    consumed = list(((cp.data.get("owner_answers") or {}).get("consumed") or {}).values())
    if not consumed:
        return []
    if phase == "analysis":
        keys = {p.get("unit_id") for p in packet.get("provisions") or [] if isinstance(p, dict)}
        return [i for i in consumed if not i["applies_to"]["scoped"] or keys & set(i["applies_to"]["provisions"])]
    tasks = packet.get("tasks") or []
    return [i for i in consumed if any(_task_matches(t, i["applies_to"]) for t in tasks)]


def with_packet(cp, packet: dict, phase: str, bid: str | None = None) -> dict:
    """The packet with its owner's answers (`owner_answers`); the packet itself when it has none (a run without
    consumed answers is left byte for byte as it was)."""
    items = items_for(cp, phase, packet)
    if not items:
        return packet
    if bid and bid in (cp.data.get("batches") or {}):
        cp.batch(bid)["owner_answers"] = [i["id"] for i in items]
    return {**packet, "owner_answers": {"note": PACKET_NOTE + "; " + NEVER, "items": items}}


def with_answers(ctx, packet: dict, phase: str, bid: str | None = None) -> dict:
    """The workflow's packet builders: with_packet on the run's checkpoint."""
    return with_packet(ctx.cp, packet, phase, bid)


# ---------------------------------------------------------------------------------------------- notes and answers

def _note_files(rd: Path) -> list[Path]:
    d = Path(rd) / "owner_answers"
    return sorted(d.glob("*.yaml")) if d.is_dir() else []


def _write_yaml(p: Path, data) -> None:
    from .quick_review import _write
    _write(p, yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=110))


def _qr_dir(rd: Path, qr_id: str) -> Path:
    return Path(rd).parent.parent / "quick-review" / qr_id


def _mark_answer(rd: Path, note: dict, state: dict) -> None:
    """The answer's state written back beside it (the quick review's answers.yaml), for the panel."""
    from .quick_review import _answers, _save_answers
    d = _qr_dir(rd, note["id"].split("/", 1)[0])
    if not (d / "answers.yaml").is_file():
        return
    data = _answers(d)
    for a in data.get("answers") or []:
        if a.get("id") == note.get("answer_id"):
            a["handoff"] = state
    _save_answers(d, data)


def _held_for(rd: Path, run_id: str) -> list[Path]:
    """The quick reviews with an answer held for this run and not offered since."""
    from .quick_review import _answers
    base = Path(rd).parent.parent / "quick-review"
    out = []
    for d in sorted(base.iterdir()) if base.is_dir() else []:
        if not (d / "answers.yaml").is_file():
            continue
        nf = Path(rd) / "owner_answers" / f"{d.name}.yaml"
        have = {n.get("answer_id") for n in ((yaml.safe_load(nf.read_text(encoding="utf-8")) or {}).get("notes") or [])
                } if nf.is_file() else set()
        for a in _answers(d).get("answers") or []:
            offers = [o for o in a.get("offers") or [] if o.get("run") == run_id]
            if offers and offers[-1].get("result") == "held" and a.get("id") not in have:
                out.append(d)
                break
    return out


def _candidate_record(rd: Path, rec: dict) -> None:
    cand = Path(rd) / "candidate"
    p = (cand if cand.is_dir() else Path(rd) / "owner_answers") / CANDIDATE_FILE
    p.parent.mkdir(parents=True, exist_ok=True)
    data = (yaml.safe_load(p.read_text(encoding="utf-8")) or {}) if p.is_file() else {}
    data.setdefault("label", "the owner's answers taken by this run: PROPOSED or PENDING, never an approval; nothing "
                             "here changes curation/ or out/")
    rows = [r for r in data.get("answers") or [] if r.get("id") != rec["id"]]
    data["answers"] = rows + [rec]
    _write_yaml(p, data)


# ---------------------------------------------------------------------------------------------- the checkpoint

def _reask_analysis(cp, rd: Path, bid: str, ids: list[str], now: str) -> None:
    b = cp.batch(bid)
    old = {k: b.pop(k) for k in ("items", "staged_run", "ignored_items", "shown", "submission", "malformed_items",
                                 "critic", "set_status", "owner_answers") if k in b}
    b.setdefault("superseded", []).append({"ts": now, "why": f"re-asked for the owner's answer(s) {ids}", **old})
    b.update(status="pending", reasked_for=ids, reasked_at=now)
    for p in b.get("provisions") or []:
        v = (cp.data.get("provisions") or {}).get(p)
        if v is None or (v.get("batch") not in (bid, None) and v.get("answered_in") != bid):
            continue
        cp.set_provision(p, "pending")
        for k in ("items", "accounted", "accounted_by", "answered_in", "statuses", "reason", "final"):
            v.pop(k, None)
    sub = Path(rd) / "batches" / f"{bid}.submission.json"          # a kept submission is the OLD answer: never reused
    if sub.is_file():
        sub.rename(sub.with_name(f"{bid}.submission.superseded-{now.replace(':', '')}.json"))


def _reask_downstream(cp, bid: str, ids: list[str], now: str) -> None:
    b = cp.batch(bid)
    items = {k: v for k, v in (cp.data["downstream"].get("items") or {}).items() if (v or {}).get("batch") == bid}
    for k in items:
        del cp.data["downstream"]["items"][k]
    cp.data["downstream"].setdefault("superseded", []).append({"ts": now, "batches": {bid: dict(b)}, "items": items,
                                                               "why": f"re-asked for the owner's answer(s) {ids}"})
    for k in ("items", "critic", "owner_answers"):
        b.pop(k, None)
    b.update(status="pending", reasked_for=ids, reasked_at=now)


def handoff(rd: Path, cp, step: str, *, unit_text: Callable[[str], str | None], approved: dict[str, str],
            now: str | None = None) -> dict:
    """The handoff at the checkpoint before `step` (see the module docstring). Returns the checkpoint's record
    {step, checkpoint, at, offered, consumed, stale, refused, pending, reasked, asked_with, rerun}; `rerun` lists the
    steps reset here that the caller runs again before `step`."""
    from .checkpoint import STEPS
    from .quick_review import _checkpoint, fingerprint, offer_answers, read_pdf
    rd, now = Path(rd), now or _now()
    rec = {"step": step, "checkpoint": CHECKPOINTS[step], "at": now, "offered": [], "consumed": [], "stale": [],
           "refused": [], "pending": [], "reasked": [], "asked_with": [], "rerun": []}
    cp.save()                                     # offer_answers and the fingerprint read the checkpoint from disk
    for d in _held_for(rd, cp.data.get("run_id")):
        rec["offered"] += offer_answers(d, rd)["offered"]
    files = _note_files(rd)
    if not files:
        return rec
    fp = fingerprint(rd)
    c = _checkpoint(rd)
    pdf = ((c.get("inputs") or {}).get("pdf") or {}).get("path") or (c.get("candidate") or {}).get("pdf_copy")
    pages = read_pdf(Path(pdf))["pages"] if pdf and Path(pdf).is_file() else []
    oa = cp.data.setdefault("owner_answers", {"consumed": {}, "checkpoints": []})
    new: list[tuple[dict, dict]] = []
    for nf in files:
        data = yaml.safe_load(nf.read_text(encoding="utf-8")) or {}
        changed = False
        for n in data.get("notes") or []:
            h = n.get("handoff") or {}
            if h.get("state") not in (None, "offered"):
                continue                          # consumed, refused, pending: done; stale: until offered again
            changed = True
            base = {"run": cp.data.get("run_id"), "checkpoint": CHECKPOINTS[step], "at": now}
            if (n.get("revalidation") or {}).get("fingerprint") != fp:
                n["handoff"] = {**base, "state": "stale",
                                "reason": "the run's proposals or candidate changed after the answer was offered: it is "
                                          "not consumed until it is offered again (and checked against the new state)"}
                n.setdefault("revalidation", {})["state"] = f"STALE since {now}"
                rec["stale"].append(n["id"])
            else:
                ok, checks, why = evidence_check(n, pages, unit_text)
                pend = touches_approved(n, approved) if ok else None
                if not ok:
                    n["handoff"] = {**base, "state": "refused", "reason": why, "evidence_checks": checks}
                    rec["refused"].append({"id": n["id"], "reason": why})
                elif pend:
                    n["handoff"] = {**base, "state": "pending", "reason": pend, "evidence_checks": checks}
                    rec["pending"].append({"id": n["id"], "reason": pend})
                    _candidate_record(rd, {"id": n["id"], "status": "PENDING", "kind": n.get("answer_kind") or "judgment",
                                           "question": n.get("question"), "answer": n.get("answer"), "by": n.get("by"),
                                           "recorded": n.get("recorded"), "checkpoint": CHECKPOINTS[step], "at": now,
                                           "reason": pend, "decision": "none: pending a person (accept/reject)"})
                else:
                    sc = scope(n, cp, rd, unit_text)
                    item = context_item(n, step, checks, sc, now)
                    oa["consumed"][n["id"]] = item
                    n["handoff"] = {**base, "state": "consumed", "role": item["role"], "applies_to": item["applies_to"]}
                    rec["consumed"].append(n["id"])
                    new.append((n, item))
            _mark_answer(rd, n, n["handoff"])
        if changed:
            _write_yaml(nf, data)
    # affected-work revalidation: the done batches whose packets the consumed answers change are asked again
    first = None
    for n, item in new:
        sc = item["applies_to"]
        hit_a = [b for b in cp.batches("analysis") if sc["scoped"]
                 and set(cp.batch(b).get("provisions") or []) & set(sc["provisions"])]
        hit_d = [b for b in cp.batches("downstream") if sc["scoped"] and (
            any(_task_matches(t, sc) for t in cp.batch(b).get("tasks") or [])
            or any((v or {}).get("batch") == b and (v or {}).get("provision") in sc["provisions"]
                   for v in (cp.data["downstream"].get("items") or {}).values()))]
        # a done batch in scope is asked again at every checkpoint from its phase on (before analysis too: a resumed
        # run re-enters the analysis step when a failed batch is retried, and its done batches are then re-asked)
        re_a = [b for b in hit_a if cp.batch(b).get("status") == "done" and STEPS.index(step) >= STEPS.index("analysis")]
        re_d = [b for b in hit_d if cp.batch(b).get("status") == "done" and STEPS.index(step) >= STEPS.index("downstream")]
        for b in re_a:
            _reask_analysis(cp, rd, b, [n["id"]], now)
        for b in re_d:
            _reask_downstream(cp, b, [n["id"]], now)
        if re_a:
            first = "analysis"
        elif re_d and first is None:
            first = "downstream"
        later = [b for b in hit_a + hit_d if b not in re_a + re_d]
        rec["reasked"] += [b for b in re_a + re_d if b not in rec["reasked"]]
        rec["asked_with"] += [b for b in later if b not in rec["asked_with"]] or (
            [p for p in sc["provisions"] if p not in rec["asked_with"]] if not (hit_a or hit_d) else [])
        item["revalidation"] = {"reasked": re_a + re_d, "asked_with": later or sc["provisions"]}
        cp.intervention(kind="owner answer consumed", by=n.get("by"), ts=now, answer=n["id"],
                        answer_recorded=n.get("recorded"), question=n.get("question"), role=item["role"],
                        checkpoint=CHECKPOINTS[step], batches_reasked=re_a + re_d,
                        note="the owner's answer taken at a safe checkpoint as a PROPOSED " + item["kind"] + "; "
                             "not an approval")
        _candidate_record(rd, {"id": n["id"], "status": "PROPOSED", "kind": item["kind"], "role": item["role"],
                               "question": n.get("question"), "answer": n.get("answer"), "by": n.get("by"),
                               "recorded": n.get("recorded"), "checkpoint": CHECKPOINTS[step], "at": now,
                               "evidence_checks": item["evidence_checks"], "applies_to": item["applies_to"],
                               "batches_reasked": re_a + re_d,
                               "decision": "none: a PROPOSED answer; a person decides every item (accept/reject)"})
    if first is not None:
        for s in STEPS[STEPS.index(first):STEPS.index(step)]:
            if cp.step(s)["status"] != "pending":
                cp.step(s)["status"] = "pending"
                rec["rerun"].append(s)
    oa["checkpoints"].append(rec)
    cp.save()
    return rec


def at_checkpoint(ctx, step: str) -> dict | None:
    """The workflow's call before running `step` (workflow._drive): the handoff at that safe checkpoint, then the steps
    it reset run again at once (their batches re-asked with the answer). A failure of the handoff's own bookkeeping is
    recorded and the run continues without consuming anything (the answers stay offered); a stop, wait or interruption
    of a re-run step propagates like any step's."""
    if step not in CHECKPOINTS:
        return None
    rd = Path(ctx.dir)
    try:
        if not _note_files(rd) and not _held_for(rd, ctx.cp.data.get("run_id")):
            return None                                    # nothing offered or held for this run: nothing to do
        from ..util import ROOT
        box: dict = {}

        def unit_text(u):                                  # the run's workspace, loaded only when a cite needs it
            if "by_id" not in box:
                try:
                    box["by_id"] = ctx.ws.units_by_id
                except Exception:                          # noqa: BLE001 (no usable workspace: no unit evidence)
                    box["by_id"] = {}
            x = box["by_id"].get(u)
            return None if x is None else str(x.get("text") or "")
        cand = Path((ctx.cp.data.get("candidate") or {}).get("dir") or rd / "candidate")
        approved = approved_units([ROOT / "curation/approvals.yaml", cand / "curation/approvals.yaml"], ROOT)
        rec = handoff(rd, ctx.cp, step, unit_text=unit_text, approved=approved)
    except Exception as e:                                 # noqa: BLE001
        ctx.cp.event("owner_answers_handoff_failed", step=step, error=f"{type(e).__name__}: {str(e)[:400]}")
        ctx.say(f"  owner's answers: the handoff before {step} failed ({type(e).__name__}: {str(e)[:200]}); nothing "
                "was consumed")
        return None
    if any(rec[k] for k in ("offered", "consumed", "stale", "refused", "pending")):
        ctx.say(f"  owner's answers at the checkpoint {rec['checkpoint']}: consumed {len(rec['consumed'])}, stale "
                f"{len(rec['stale'])}, refused {len(rec['refused'])}, pending {len(rec['pending'])}; re-asked "
                f"{rec['reasked'] or 'none'}")
    if rec["rerun"]:
        from .workflow import STEP_FUNCS
        for s in rec["rerun"]:
            ctx.say(f"[{ctx.run_id}] {s} (again: re-asked for the owner's answers) ...")
            with ctx.cp.timed(s) as st:
                STEP_FUNCS[s](ctx, st)
    return rec


def state_line(a: dict) -> str:
    """One answer's state for the panel: recorded | held | offered | consumed at <checkpoint> | stale | refused | pending."""
    h = a.get("handoff") or {}
    st = h.get("state")
    run = f" (run {h['run']})" if h.get("run") else ""
    if st == "consumed":
        return f"consumed at {h.get('checkpoint')}{run} as a PROPOSED {h.get('role') or 'item'}; not an approval"
    if st in ("stale", "refused", "pending"):
        return f"{st}: {h.get('reason')}{run}"
    offers = a.get("offers") or []
    if offers:
        o = offers[-1]
        if o.get("result") == "held":
            return f"held for run {o.get('run')} (a step was running): offered at its next safe checkpoint"
        return f"offered to run {o.get('run')} (taken at its next safe checkpoint)"
    return "recorded (not offered yet)"
