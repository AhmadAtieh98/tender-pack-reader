"""Named review decisions on register rows and amendment ops (session 06).

Only a person makes a decision, by running
    tenderpack accept ITEM [ITEM ...] --reviewer "Name" [--note TEXT]
    tenderpack reject ITEM [ITEM ...] --reviewer "Name" --note "what is wrong"
where ITEM is an A1 row id (VOL-I-8.6-01) or an op id (ADD-02/9.1). The program never decides anything itself.
Session 12: ITEM may also be a clarification entry (CQ-...) or an issue (I-...): accepting one records that a person
decided the entry as it now reads, including a closing response status ("answered by addendum", "withdrawn (not
sent)") or an issue's status/resolution; until then every output shows it as HUMAN DECISION PENDING
(tenderpack.human_owned). The decision is bound to the entry's fingerprint (human_owned.entry_fingerprint: every
field), so any later edit voids it. The AI workflow never calls this; only a person running `accept`/`reject` does.

Each decision is bound to a FINGERPRINT of what was reviewed:
  row  the row as written (requirement, units, scope, assessment, owner, evidence, date rules and every
       interpretation with its quote, parameters, consequence, note and pins), the definitions of its evidence
       items, where each of its units is printed (page, box, spans, image-reading subject), and the state of each of its dependencies (status, text, cells, annotations, image review
       fingerprint) wherever the row applies. Stages that leave all of this unchanged do not change the
       fingerprint, so an addendum that does not touch the row keeps its decision; one that does, voids it.
  op   the op as written and its SUBJECT, captured by the engine immediately before the op runs, whether or not it
       then applies (amend.Engine.subject): its provision's text, pages and evidence anchors, the section heading,
       and the pin of every unit it reads or changes, including every member row of a replaced table or form and
       of its replacement. Withholding a rejected op therefore never changes what the rejection is bound to.
Source binding (session 09): every unit pin in a binding (a row's dependencies, an op's subject) covers the unit's
SOURCE as well as its content: its document (id and the sha256 the build manifest records for it), pages, each
anchor's page, box (0.1 pt) and spans, and an image reading's region and review subject (amend.unit_pin with
evidence). A unit printed elsewhere with the same words, or a re-issued document, therefore voids the decision. The
interpretation pins that decide STALE (register.pin_value) stay content-only: a moved source needs a person's
decision again, not a new reading of unchanged words.
A rejection withholds the op for as long as it is the latest decision on it, even when its subject has changed
since (shown as CHANGED: review again; the op stays withheld until a person decides again). Pending review
(proposed), rejection (withheld) and structural failure (invalid op) stay distinct.
A decision counts only while its fingerprint is the item's current one. Any change makes it CHANGED: the record
is kept and shown ("accepted by X; changed since: review again") but no longer counts. The `review:` and
`reviewer:` fields in the curated YAML are drafting flags and are never counted as acceptance.

Decisions are appended to the pack's decisions file (`decisions:` in config/pack.yaml, default
curation/reviews/decisions.yaml); the latest decision on an item is the one that applies.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import yaml

from .amend import unit_evidence, unit_pin
from .readings import is_assistant, valid_reviewer
from .util import load_yaml, sha256_file, sha256_text

DEFAULT_PATH = "curation/reviews/decisions.yaml"
HEADER = ("# Review decisions on register rows and amendment ops. Written only by `tenderpack accept` / `tenderpack\n"
          "# reject` on a person's instruction; never by the program on its own. Each decision is bound to the\n"
          "# fingerprint of what was reviewed (the item, its evidence and its dependencies). A later change to any\n"
          "# of them voids the decision: the item needs review again. The latest decision on an item applies.\n")


def decisions_path(cfg: dict, root: Path) -> Path:
    p = Path(cfg.get("decisions", DEFAULT_PATH))
    return p if p.is_absolute() else root / p


def load_decisions(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return list((load_yaml(path) or {}).get("decisions") or [])


def _canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str)


def _in_force(status: str) -> bool:
    return not status.startswith(("NOT ISSUED", "NOT IN FORCE", "DELETED", "REVOKED", "REPLACED", "REMOVED"))


def documents(r: dict) -> dict[str, str | None]:
    """{doc id: sha256 of the source document}, as the evidence build's BUILD_MANIFEST.json recorded its input (E01
    has checked that the file still has it), else hashed from the file; None when neither is available."""
    root = Path(r.get("root") or ".")
    absolute = lambda p: str((Path(p) if Path(p).is_absolute() else root / p).resolve())  # noqa: E731
    man = Path(r["evidence_dir"]) / "BUILD_MANIFEST.json" if r.get("evidence_dir") else None
    inputs = json.loads(man.read_text(encoding="utf-8")).get("inputs", {}) if man is not None and man.exists() else {}
    by_path = {absolute(p): sha for p, sha in inputs.items()}
    out = {}
    for d in (r.get("cfg") or {}).get("documents") or []:
        p = absolute(d["path"])
        out[d["doc_id"]] = by_path.get(p) or (sha256_file(Path(p)) if Path(p).is_file() else None)
    return out


def _evidence(r: dict) -> dict:
    """{unit id: amend.unit_evidence with its document's sha256}, cached in r (stage2.evaluate drops the cache)."""
    if "_unit_evidence" not in r:
        docs = documents(r)
        r["_unit_evidence"] = {u["unit_id"]: unit_evidence(u, docs.get(u["doc"])) for u in r["units"]}
    return r["_unit_evidence"]


def row_binding(r: dict, e: dict) -> dict:
    """What a decision on a row is bound to."""
    row, reg = e["row"], r["register"]
    ev = _evidence(r)
    by_stage = {s.stage: s for s in r["stages"]}
    states, last = [], None
    for st in r["order"]:
        it = reg.interp_at(row, st)
        force = _in_force(e["stages"][st]["status"])
        # the row's dependencies (register.pins_for), each pinned with its content AND its source (session 09)
        deps = ({d: unit_pin(by_stage[st].state, d, ev) for d in reg.pins_for(row, it, by_stage[st])}
                if (it and force) else {})
        cur = {"in_force": force, "dependencies": deps}
        if cur != last:                                    # stages that change nothing for the row add nothing
            states.append(cur)
            last = cur
    return {"row": row.model_dump(mode="json", exclude={"review", "reviewer"}),
            "evidence": {k: (r["evidence_items"][k].model_dump(mode="json") if k in r["evidence_items"] else None)
                         for k in row.evidence},
            "source": {u: ev.get(u) for u in row.units},          # where each of its units is printed
            "states": states}


def op_binding(r: dict, stage_index: int, x) -> dict:
    """What a decision on an op is bound to: the op as written and its subject (the state immediately before it),
    with the identity (sha256) of every document whose units the subject pins (session 09)."""
    ev = _evidence(r)
    docs = {v["doc"]: v["doc_sha256"] for v in ev.values()}
    involved = set()
    for k in [x.subject.get("provision", {}).get("unit"), *x.subject.get("before", {})]:
        if k:
            involved.add((ev.get(k) or {}).get("doc") or k.partition(":")[0])
            if "+" in k:                                   # a unit an op inserted: '<anchor>+<addendum>'
                involved.add(k.rpartition("+")[2])
    return {"op": x.op.model_dump(mode="json", exclude={"review", "reviewer"}, exclude_none=True), **x.subject,
            "documents": {d: docs.get(d) for d in sorted(involved)}}


def withdrawn_ops(decisions: list[dict]) -> dict[str, dict]:
    """Ops whose latest named decision is a rejection, whatever their fingerprint: {op id: {reviewer, date, note}}.
    A rejection keeps the op withheld until a person decides again; it never lapses into applying."""
    out = {}
    for item in {d.get("item") for d in decisions if d.get("kind") == "op"}:
        d = _latest(decisions, "op", item)
        if d and d["decision"] == "reject":
            out[item] = {"reviewer": d["reviewer"], "date": d.get("date"), "note": d.get("note")}
    return out


def fingerprint(binding: dict) -> str:
    return sha256_text(_canon(binding))


def _latest(decisions: list[dict], kind: str, item: str) -> dict | None:
    named = [d for d in decisions if d.get("kind") == kind and d.get("item") == item and valid_reviewer(d.get("reviewer"))
             and d.get("decision") in ("accept", "reject")]
    return named[-1] if named else None


def status_of(decisions: list[dict], kind: str, item: str, fp: str, flag: str | None = None) -> dict:
    """{'status': accepted | rejected | changed | proposed, ...}. A file flag alone is reported, never counted."""
    d = _latest(decisions, kind, item)
    if d is None:
        out = {"status": "proposed"}
        if flag == "accepted":
            out["flag_only"] = True
        return out
    base = {"reviewer": d["reviewer"], "date": d.get("date"), "note": d.get("note"), "decision": d["decision"]}
    if d.get("origin") == "interview_demo":
        base["origin"] = "interview_demo"
    if d.get("fingerprint") != fp:
        return {"status": "changed", **base}
    return {"status": "accepted" if d["decision"] == "accept" else "rejected", **base}


def label(st: dict) -> str:
    s = st["status"]
    note = f" — note: {st['note']}" if st.get("note") else ""
    if s == "accepted":
        if st.get("origin") == "interview_demo":
            return f"ASSUMED APPROVED FOR DEMO ({st.get('date')}); no observed human review{note}"
        return f"accepted by {st['reviewer']} ({st.get('date')}){note}"
    if s == "rejected":
        return f"REJECTED by {st['reviewer']} ({st.get('date')}){note}"
    if s == "changed":
        if st["decision"] == "reject":
            return (f"rejected by {st['reviewer']} ({st.get('date')}) but CHANGED since: review again; the op is still "
                    "withheld until a person decides again")
        return f"accepted by {st['reviewer']} ({st.get('date')}) but CHANGED since: review again"
    return "proposed (not reviewed)" + (" — file flag 'accepted' has no bound decision: not counted" if st.get("flag_only") else "")


def compute(r: dict, decisions: list[dict]) -> dict:
    """{('row', id) | ('op', id): {'status', 'fingerprint', 'binding', ...}} for every row and op."""
    out = {}
    for e in r["evals"]:
        b = row_binding(r, e)
        fp = fingerprint(b)
        out[("row", e["row"].id)] = {**status_of(decisions, "row", e["row"].id, fp, e["row"].review), "fingerprint": fp,
                                     "binding": b}
    for i, s in enumerate(r["stages"][1:], start=1):
        for x in s.ops:
            b = op_binding(r, i, x)
            fp = fingerprint(b)
            out[("op", x.op.id)] = {**status_of(decisions, "op", x.op.id, fp, x.op.review), "fingerprint": fp,
                                    "binding": b, "stage": s.stage, "valid": x.valid}
    # session 12: clarification entries and issues (tenderpack.human_owned), bound to the entry as it reads
    from .human_owned import entry_binding, entry_fingerprint
    for c in (r.get("clarifications") or {}).get("clarifications") or []:
        cid = str(c.get("id"))
        fp = entry_fingerprint("clarification", c)
        out[("clarification", cid)] = {**status_of(decisions, "clarification", cid, fp), "fingerprint": fp,
                                       "binding": entry_binding("clarification", c)}
    for iid, it in (r.get("curated_issues") or {}).items():
        fp = entry_fingerprint("issue", it)
        out[("issue", iid)] = {**status_of(decisions, "issue", iid, fp), "fingerprint": fp,
                               "binding": entry_binding("issue", it)}
    return out


def item_kind(item: str) -> str:
    """The kind of an ITEM named on the command line: a clarification entry (CQ-...), an issue (I-...), an op (it has
    a '/'), else a row."""
    return ("clarification" if item.startswith("CQ-") else "issue" if item.startswith("I-") else
            "op" if "/" in item else "row")


def record(path: Path, entries: list[dict]) -> None:
    data = load_decisions(path)
    data += entries
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(HEADER + yaml.safe_dump({"decisions": data}, allow_unicode=True, sort_keys=False, width=110),
                    encoding="utf-8")


def decide(r: dict, items: list[str], decision: str, reviewer: str, note: str | None, path: Path,
           today: str | None = None) -> tuple[int, list[str]]:
    """Validate and record decisions. Returns (exit code, messages). Writes nothing unless every item passes."""
    msgs: list[str] = []
    if not valid_reviewer(reviewer):
        return 2, [f"refused: --reviewer must name the person deciding, not a placeholder ({reviewer!r}). Nothing written."]
    if is_assistant(reviewer):
        return 2, [f"refused: a decision is a person's; {reviewer!r} names the assistant or the program. Nothing written."]
    if decision == "reject" and not (note or "").strip():
        return 2, ["refused: a rejection needs --note saying what is wrong. Nothing written."]
    if r["problems"]:
        return 2, [f"refused: the evidence build is not usable ({'; '.join(r['problems'])[:200]}). Nothing written."]
    reviews = r.get("reviews") or compute(r, load_decisions(path))
    rows = {e["row"].id: e for e in r["evals"]}
    last = r["order"][-1]
    entries = []
    for item in items:
        kind = item_kind(item)
        cur = reviews.get((kind, item))
        if cur is None:
            msgs.append(f"refused: no {kind} {item}")
            continue
        if decision == "accept" and kind == "row":
            ev = rows[item]["stages"][last]
            if ev["stale"]:
                msgs.append(f"refused: {item} is STALE at {last} (its interpretation predates a change to its dependencies); "
                            "re-make it (e.g. apply a prepared proposal) before accepting")
                continue
            bad = [p for st in r["order"] for p in rows[item]["stages"][st]["problems"]]
            if bad:
                msgs.append(f"refused: {item} has quote problems: {bad[:2]}")
                continue
        if decision == "accept" and kind == "op" and not cur["valid"]:
            msgs.append(f"refused: op {item} is invalid at {cur['stage']}; an invalid op cannot be accepted (reject it instead)")
            continue
        if decision == "accept" and kind == "clarification":     # session 12: an answer it closes with is checked
            from .clarify import check as clarify_check
            bad = clarify_check({"clarifications": [cur["binding"]["entry"]]}, r.get("units") or [],
                                set(r.get("curated_issues") or {}),
                                state=(r["stages"][-1].state if r.get("stages") else None))   # session 12
            if bad:
                msgs.append(f"refused: {item} does not pass the register's checks: {bad[:2]}")
                continue
        b = cur["binding"]
        summary = ({"evidence": sorted(b["evidence"]), "dependencies": sorted({d for s in b["states"] for d in s["dependencies"]})}
                   if kind == "row" else {"entry": item, "response_status": b["entry"].get("response_status"),
                                          "answer": b["entry"].get("answer"), "status": b["entry"].get("status")}
                   if kind in ("clarification", "issue") else
                   {"provision": b["provision"]["unit"], "units_before_op": sorted(b["before"])})
        summary = {k: v for k, v in summary.items() if v is not None}
        entries.append({"kind": kind, "item": item, "decision": decision, "reviewer": reviewer.strip(),
                        "date": today or dt.date.today().isoformat(), "note": (note or "").strip() or None,
                        "fingerprint": cur["fingerprint"], "bound_to": summary})
    if len(entries) != len(items):
        return 1, msgs + ["Nothing written (every item must pass)."]
    record(path, entries)
    msgs += [f"{decision}ed {e['kind']} {e['item']} by {e['reviewer']}; bound to fingerprint {e['fingerprint'][:16]}"
             for e in entries] + [f"written to {path}"]
    return 0, msgs


def ai_guard_decisions(cfg: dict, decisions: list[dict]) -> list[dict]:
    """Protect actual operator choices; a simulated acceptance is not a human override.

    This filtered view is only for AI conflict guards, never the decision ledger or
    release checks. Explicit demo mode and controller provenance are both required.
    Rejections and all operator decisions keep their existing protection.
    """
    if cfg.get("interview_demo") is not True:
        return decisions
    return [d for d in decisions if not (d.get("origin") == "interview_demo" and d.get("decision") == "accept")]
