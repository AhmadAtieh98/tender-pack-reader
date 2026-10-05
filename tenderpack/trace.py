"""C46 obligation trace: an amendment op being accounted for (C20) does not prove that what it requires reached
the register. For every valid op that creates or amends an obligation, at the stage it applies:

  A1  a register row in force at that stage holds the units the op created or changed (or its provision). For an
      insertion, each inserted part needs its own row: the new list item (or the provision that inserts it), and
      the new group's content. The insertion anchor is never evidence of coverage: its rows predate the insertion
      and say nothing about what was inserted after it (session 08);
  A3  consequence words the op brings in (new text, inserted or replacement content, an obligation it adds;
      English and Arabic lexicons of dispositions.py) are carried by such a row's consequence, quoted from those
      units, or explained by a unit disposition's `consequence_note`;
  A5  each such row at bid stage names a deliverable (an evidence item that has activity templates or a justified
      exception), or states why it needs none (`no_deliverable`).

Which ops carry obligations: annotate with effect adds_obligation; insert_unit; insert_row; replace_unit; set_status
reinstated; replace_text / append_text / set_value when the changed unit is a requirement (its disposition) or
its new words contain obligation language. Deletions and revocations remove obligations (their rows go out of
force) and confirmations change nothing; neither is traced.

Session 09: a row inserted in a table (insert_row) needs a row of its own: the rows of the table's other entries do
not count. A REMOVED row (its words deleted from a unit that stays in force) is out of force like a DELETED one.
Two consequences the dispositions lexicon does not list are consequence words here: a refused document ("will be
treated as not submitted", "will not be accepted") and zero marks ("will be awarded no marks"). Like any other, they
are carried by a row whose consequence is quoted from the op's units, whatever its class (a document refusal is
`document_refusal`, zero marks under one criterion `criterion_zero`: register.CONSEQUENCE_CLASSES).

Each finding names the op, the stage, the output it fails to reach and the provision's own words, so it can be
shown on A3 and in A2. Findings block a release (coverage) and fail check-register; a working draft is still
published with them listed.
"""
from __future__ import annotations

import re

from .amend import group_members
from .dispositions import CONSEQUENCE_AR, CONSEQUENCE_EN, OBLIGATION, effective_disposition

BID_STAGE = ("pass_fail", "scored", "procedural")
OBLIGATION_DISPOSITIONS = ("requirement", "consequence", "duplicate")


def _in_force(status: str) -> bool:
    return not status.startswith(("NOT ISSUED", "NOT IN FORCE", "DELETED", "REVOKED", "REPLACED", "REMOVED"))


# a refused document and zero marks under a criterion (session 09; not in the dispositions lexicon)
REFUSAL = re.compile(r"\b(?:treated as not (?:having been )?submitted|(?:will|shall) not be accepted|"
                     r"(?:will|shall) be refused)\b", re.I)
ZERO_MARKS = re.compile(r"\b(?:awarded|given|receive|score)\s+(?:no|zero|nil)\s+(?:marks?|points?)\b|"
                        r"\b(?:no|zero) marks\b", re.I)


def _consequence_words(text: str) -> set[str]:
    return {m.group(0).lower() for rx in (CONSEQUENCE_EN, CONSEQUENCE_AR, REFUSAL, ZERO_MARKS)
            for m in rx.finditer(text or "")}


def _cites(row_units: list[str], keys: set[str]) -> bool:
    return any(u in keys or any(u.startswith(k + "/") or k.startswith(u + "/") for k in keys) for u in row_units)


def obligation_trace(r: dict) -> list[dict]:
    units = {u["unit_id"]: u for u in r["units"]}
    disp = r.get("dispositions") or {}
    templates = r.get("templates") or {}
    exceptions = templates.get("_exceptions") or {}
    reg = r["register"]
    out: list[dict] = []
    for i, s in enumerate(r["stages"][1:], start=1):
        st, prev = s.state, r["stages"][i - 1].state
        for x in s.ops:
            op = x.op
            if not x.applied or (op.type == "annotate" and op.effect != "adds_obligation"):
                continue
            if op.type == "set_status" and op.status != "reinstated":
                continue
            prov = st[op.provision]
            if op.type == "annotate":
                # (session 12: a target named by the number an earlier op inserted it as is that inserted unit)
                tg = [(x.details.get("resolved_targets") or {}).get(t, t) for t in op.targets]
                carriers = [op.provision] + [k for t in tg for k in ([t] if t in st else group_members(st, t))]
            else:
                carriers = [k for k in x.changed if k in st and st[k].status != "superseded"]
            needs: list[tuple[str, set[str]]] = []               # (what, the units any one of which a row must hold)
            if op.type == "insert_unit":
                item = f"{op.anchor}+{s.stage}" if op.anchor else None
                if item:
                    needs.append((f"the item inserted after {op.anchor}", {item, op.provision}))
                if op.new_group:
                    needs.append((f"the new {op.new_group}", {k for k in x.changed if k != item} | {op.new_group}))
                keys = set().union(*(n for _, n in needs)) if needs else {op.provision}
            elif op.type == "insert_row":                  # the new row, never the table's other rows
                keys = {x.details.get("inserted"), op.provision} - {None}
                needs = [(f"the row inserted in {op.target}", keys)]
            else:
                keys = set(carriers) | {op.provision} | set(x.changed)
                keys |= {k for k in (op.target, op.replacement, op.new_group) if k}
                keys |= set(op.targets or [])
                needs = [("it", keys)]
            # obligation-bearing? and which consequence words the op brings in
            bearing, brought = op.type in ("annotate", "insert_unit", "insert_row", "replace_unit") or op.status == "reinstated", set()
            for k in carriers:
                new = st[k].text or ""
                old = prev[k].text if k in prev and prev[k].status == "active" and op.type != "annotate" else ""
                d = effective_disposition(units[k], disp) if k in units and not units[k]["doc"].startswith("ADD-") else None
                if (d and d.disposition in OBLIGATION_DISPOSITIONS) or OBLIGATION.search(new) and not OBLIGATION.search(old or ""):
                    bearing = True
                brought |= _consequence_words(new) - _consequence_words(old)
            if op.type in ("annotate", "insert_unit"):
                brought |= _consequence_words(prov.text)
            if not bearing:
                continue
            noted = any((disp.get(k) and (disp[k].consequence_note or "").strip()) for k in carriers)
            rows = [e for e in r["evals"] if _in_force(e["stages"][s.stage]["status"]) and _cites(e["row"].units, keys)]
            words = f"'{(prov.text or '')[:200]}'"
            base = {"stage": s.stage, "op": op.id, "provision": op.provision, "units": sorted(carriers)[:8],
                    "rows": [e["row"].id for e in rows]}
            for what, need in needs:
                if not [e for e in rows if _cites(e["row"].units, need)]:
                    out.append({**base, "output": "A1", "detail": f"{op.id} ({op.type}) creates or amends an obligation that no "
                                f"A1 row in force at {s.stage} holds" + (f" ({what}; a row of the anchor {op.anchor} does "
                                                                         "not count)" if op.type == "insert_unit" else
                                                                         f" ({what}; the table's other rows do not count)"
                                                                         if op.type == "insert_row" else "")
                                + f": {words}"})
            if brought and not noted:
                carried = []
                for e in rows:
                    it = reg.interp_at(e["row"], s.stage)
                    cu = getattr(getattr(it, "consequence", None), "unit", None)
                    if cu and _cites([cu], keys):
                        carried.append(e["row"].id)
                if not carried:
                    out.append({**base, "output": "A3", "detail": f"{op.id} brings in consequence words "
                                f"{sorted(brought)} that no row's consequence carries at {s.stage}: {words}"})
            for e in rows:
                row = e["row"]
                if row.assessment not in BID_STAGE:
                    continue
                if not row.evidence and not (row.no_deliverable or "").strip():
                    out.append({**base, "rows": [row.id], "output": "A5", "detail": f"{op.id}: row {row.id} names no "
                                f"deliverable and no reason it needs none, so no activity plans it"})
                for ev in row.evidence:
                    if not templates.get(ev) and not (exceptions.get(ev) or "").strip():
                        out.append({**base, "rows": [row.id], "output": "A5", "detail": f"{op.id}: deliverable {ev} of "
                                    f"{row.id} has no activity template and no justified exception"})
    return out
