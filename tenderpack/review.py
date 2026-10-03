"""Named review decisions on register rows and amendment ops (session 06).

Only a person makes a decision, by running
    tenderpack accept ITEM [ITEM ...] --reviewer "Name" [--note TEXT]
    tenderpack reject ITEM [ITEM ...] --reviewer "Name" --note "what is wrong"
where ITEM is an A1 row id (VOL-I-8.6-01) or an op id (ADD-02/9.1). The program never decides anything itself.

Each decision is bound to a FINGERPRINT of what was reviewed:
  row  the row as written (requirement, units, scope, assessment, owner, evidence, date rules and every
       interpretation with its quote, parameters, consequence, note and pins), the definitions of its evidence
       items, and the state of each of its dependencies (status, text, cells, annotations, image review
       fingerprint) wherever the row applies. Stages that leave all of this unchanged do not change the
       fingerprint, so an addendum that does not touch the row keeps its decision; one that does, voids it.
  op   the op as written, its provision's text and pages, the state before the op of every unit it targets or
       anchors on, and the text of the content it brings in.
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

from .readings import valid_reviewer
from .register import pin_value
from .util import load_yaml, sha256_text

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
    return not status.startswith(("NOT ISSUED", "DELETED", "REVOKED", "REPLACED"))


def row_binding(r: dict, e: dict) -> dict:
    """What a decision on a row is bound to."""
    row, reg = e["row"], r["register"]
    by_stage = {s.stage: s for s in r["stages"]}
    states, last = [], None
    for st in r["order"]:
        it = reg.interp_at(row, st)
        force = _in_force(e["stages"][st]["status"])
        deps = reg.pins_for(row, it, by_stage[st]) if (it and force) else {}
        cur = {"in_force": force, "dependencies": deps}
        if cur != last:                                    # stages that change nothing for the row add nothing
            states.append(cur)
            last = cur
    return {"row": row.model_dump(mode="json", exclude={"review", "reviewer"}),
            "evidence": {k: (r["evidence_items"][k].model_dump(mode="json") if k in r["evidence_items"] else None)
                         for k in row.evidence},
            "states": states}


def op_binding(r: dict, stage_index: int, x) -> dict:
    """What a decision on an op is bound to."""
    op = x.op
    prev, cur = r["stages"][stage_index - 1].state, r["stages"][stage_index].state
    prov = cur.get(op.provision)
    before = {k: pin_value(prev, k) for k in sorted({op.target, op.anchor, op.new_text_from, *(op.targets or [])} - {None})}
    content = {k: cur[k].text for k in sorted(x.details.get("content") or []) if k in cur}
    return {"op": op.model_dump(mode="json", exclude={"review", "reviewer"}, exclude_none=True),
            "provision": {"text": prov.text if prov else None, "pages": list(prov.pages) if prov else None},
            "before": before, "content": content}


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
    if d.get("fingerprint") != fp:
        return {"status": "changed", **base}
    return {"status": "accepted" if d["decision"] == "accept" else "rejected", **base}


def label(st: dict) -> str:
    s = st["status"]
    note = f" — note: {st['note']}" if st.get("note") else ""
    if s == "accepted":
        return f"accepted by {st['reviewer']} ({st.get('date')}){note}"
    if s == "rejected":
        return f"REJECTED by {st['reviewer']} ({st.get('date')}){note}"
    if s == "changed":
        verb = "accepted" if st["decision"] == "accept" else "rejected"
        return f"{verb} by {st['reviewer']} ({st.get('date')}) but CHANGED since: review again"
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
    return out


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
    if decision == "reject" and not (note or "").strip():
        return 2, ["refused: a rejection needs --note saying what is wrong. Nothing written."]
    if r["problems"]:
        return 2, [f"refused: the evidence build is not usable ({'; '.join(r['problems'])[:200]}). Nothing written."]
    reviews = r.get("reviews") or compute(r, load_decisions(path))
    rows = {e["row"].id: e for e in r["evals"]}
    last = r["order"][-1]
    entries = []
    for item in items:
        kind = "op" if "/" in item else "row"
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
        b = cur["binding"]
        summary = ({"evidence": sorted(b["evidence"]), "dependencies": sorted({d for s in b["states"] for d in s["dependencies"]})}
                   if kind == "row" else {"provision": item.split("/")[0] + ":" + item.split("/", 1)[1].split("(")[0],
                                          "before": sorted(b["before"]), "content": sorted(b["content"])})
        entries.append({"kind": kind, "item": item, "decision": decision, "reviewer": reviewer.strip(),
                        "date": today or dt.date.today().isoformat(), "note": (note or "").strip() or None,
                        "fingerprint": cur["fingerprint"], "bound_to": summary})
    if len(entries) != len(items):
        return 1, msgs + ["Nothing written (every item must pass)."]
    record(path, entries)
    msgs += [f"{decision}ed {e['kind']} {e['item']} by {e['reviewer']}; bound to fingerprint {e['fingerprint'][:16]}"
             for e in entries] + [f"written to {path}"]
    return 0, msgs
