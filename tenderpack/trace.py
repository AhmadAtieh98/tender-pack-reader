"""C46 obligation trace: an amendment op being accounted for (C20) does not prove that what it requires reached
the register. For every valid op that creates or amends an obligation, at the stage it applies:

  A1  a register row in force at that stage holds the units the op created or changed (or its provision);
  A3  consequence words the op brings in (new text, inserted or replacement content, an obligation it adds;
      English and Arabic lexicons of dispositions.py) are carried by such a row's consequence, quoted from those
      units, or explained by a unit disposition's `consequence_note`;
  A5  each such row at bid stage names a deliverable (an evidence item that has activity templates or a justified
      exception), or states why it needs none (`no_deliverable`).

Which ops carry obligations: annotate with effect adds_obligation; insert_unit; replace_unit; set_status
reinstated; replace_text / append_text / set_value when the changed unit is a requirement (its disposition) or
its new words contain obligation language. Deletions and revocations remove obligations (their rows go out of
force) and confirmations change nothing; neither is traced.

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
    return not status.startswith(("NOT ISSUED", "DELETED", "REVOKED", "REPLACED"))


def _consequence_words(text: str) -> set[str]:
    return {m.group(0).lower() for rx in (CONSEQUENCE_EN, CONSEQUENCE_AR) for m in rx.finditer(text or "")}


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
            if not x.valid or (op.type == "annotate" and op.effect != "adds_obligation"):
                continue
            if op.type == "set_status" and op.status != "reinstated":
                continue
            prov = st[op.provision]
            if op.type == "annotate":
                carriers = [op.provision] + [k for t in op.targets for k in ([t] if t in st else group_members(st, t))]
            else:
                carriers = [k for k in x.changed if k in st and st[k].status != "superseded"]
            keys = set(carriers) | {op.provision} | set(x.changed)
            keys |= {k for k in (op.target, op.replacement, op.new_group, op.anchor) if k}
            keys |= set(op.targets or [])
            # obligation-bearing? and which consequence words the op brings in
            bearing, brought = op.type in ("annotate", "insert_unit", "replace_unit") or op.status == "reinstated", set()
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
            if not rows:
                out.append({**base, "output": "A1", "detail": f"{op.id} ({op.type}) creates or amends an obligation that no "
                            f"A1 row in force at {s.stage} holds: {words}"})
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
