"""The A1 register slice: requirement rows evaluated at every stage of the amendment path.

Rows (curation/register/rows.yaml) are independently testable obligations (D3), grouped by the
clause they come from (`group`) and tagged by scope. Each row carries one or more
*interpretations*, each made at a stage and PINNED to the evidence it was made against:

  pins = {unit: hash} over the row's dependency set at that stage:
         the row's units (and their replacements), the unit stating the consequence, the unit
         defining each date anchor (e.g. the Proposal Due Date in VOL-I 6.1), and every clarification
         or rule that annotates those units (a new answer is a new dependency).

At a stage, a row uses its latest interpretation made at or before that stage. If any pinned
dependency has changed since (or a new one has appeared), the row is STALE: its dates are still
recomputed from the effective text, but its reading needs a person again. Pins are written by
`tenderpack pin` when an interpretation is drafted or re-reviewed, never during a build.

Separate statuses, never merged:
  status            what the documents say at that stage (ACTIVE / AMENDED / DELETED / ...)
  transcription     review status of an image reading the row relies on (pending until approved)
  interpretation    review status of the row itself (proposed until a named person accepts it)
  ops               review status of the amendment ops that changed it (proposed / accepted)
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .amend import BASE, StageResult, UState
from .dates import Calendar, DateRule, interpretations, parse_date, planning_value
from .textnorm import normalize_arabic, normalize_latin
from .util import load_yaml, sha256_text

CONSEQUENCE_CLASSES = ("rejection", "disqualification", "non_responsive", "exclusion", "score_elimination", "lesser")
BID_OUT = ("rejection", "disqualification", "non_responsive", "exclusion")


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class Consequence(_Strict):
    cls: Literal["rejection", "disqualification", "non_responsive", "exclusion", "score_elimination", "lesser"] = \
        Field(alias="class")
    unit: str
    quote: str
    gloss: str | None = None                     # proposed translation of a non-English quote (never checked as evidence)


class Interp(_Strict):
    stage: str
    quote: str                                   # must be found in the row's effective text at every stage it is used
    parameters: dict = Field(default_factory=dict)
    consequence: Consequence | Literal["none_stated"] = "none_stated"
    note: str | None = None
    pins: dict[str, str] = Field(default_factory=dict)


class RuleDef(_Strict):
    rule_id: str
    kind: str
    purpose: str
    anchor: str | None = None
    offset: int = 0
    unit: str = "calendar_day"
    direction: str = "after"
    fixed: str | None = None
    source_unit: str
    text: str


class Row(_Strict):
    id: str
    group: str
    scope: list[str]
    requirement: str
    units: list[str]                             # primary unit first
    discipline: str
    assessment: Literal["pass_fail", "scored", "contractual_post_award", "procedural", "informational"]
    evidence: list[str] = Field(default_factory=list)
    interpretations: list[Interp]
    date_rules: list[RuleDef] = Field(default_factory=list)
    confidence: Literal["high", "medium", "low"]
    confidence_reason: str
    issues: list[str] = Field(default_factory=list)
    follows_replacement: bool = False            # a replaced table row / form field continues in its replacement
    review: Literal["proposed", "accepted"] = "proposed"
    reviewer: str | None = None


class RowFile(_Strict):
    prepared_by: str
    method: str
    anchors: dict[str, dict]                     # {"PDD": {"name": "Proposal Due Date", "defined_in": "VOL-I:6.1"}}
    rows: list[Row]


def pins_path(rows_path: Path) -> Path:
    return Path(rows_path).with_name("pins.yaml")


def load_rows(path: Path) -> RowFile:
    """Rows are hand-curated; their pins are machine-written by `tenderpack pin` into pins.yaml beside them
    ({row id: {interpretation stage: {unit: hash}}}), so re-pinning never rewrites the curated file."""
    rf = RowFile.model_validate(load_yaml(path))
    pp = pins_path(path)
    pins = (load_yaml(pp) or {}).get("pins", {}) if pp.exists() else {}
    for row in rf.rows:
        for it in row.interpretations:
            if not it.pins and it.stage in pins.get(row.id, {}):
                it.pins = dict(pins[row.id][it.stage])
    return rf


def write_pins(rowfile: RowFile, path: Path, header: str) -> None:
    data = {"pins": {r.id: {it.stage: dict(sorted(it.pins.items())) for it in r.interpretations if it.pins}
                     for r in rowfile.rows if any(it.pins for it in r.interpretations)}}
    import yaml
    Path(path).write_text(header + yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")


# ---------------------------------------------------------------------------------------------- helpers

def _norm(t: str) -> str:
    return " ".join(normalize_arabic(t).split()) if any("؀" <= c <= "ۿ" for c in t) else \
        " ".join(normalize_latin(t).replace("'", "").split())


def found(quote: str, text: str) -> bool:
    return _norm(quote) in _norm(text)


def stage_order(stages: list[StageResult]) -> list[str]:
    return [s.stage for s in stages]


def effective(state: dict[str, UState], uid: str, follow: bool) -> UState | None:
    u = state.get(uid)
    while follow and u is not None and u.status == "superseded" and u.superseded_by in state:
        u = state[u.superseded_by]
    return u


def anchor_values(state: dict[str, UState], anchors: dict, stages_issued: dict[str, str | None]) -> dict:
    vals = {}
    for name, a in anchors.items():
        u = state.get(a["defined_in"])
        p = parse_date(u.text) if u and u.status == "active" else None
        vals[name] = p[0] if p else None
    for st, iss in stages_issued.items():
        if iss:
            vals[f"{st}-issue"] = date.fromisoformat(iss)
    return vals


def dependencies(row: Row, interp: Interp, state: dict[str, UState], anchors: dict, op_provision: dict) -> list[str]:
    deps = []
    for uid in row.units:
        deps.append(uid)
        e = effective(state, uid, row.follows_replacement)
        if e is not None and e.unit_id != uid:
            deps.append(e.unit_id)
    if isinstance(interp.consequence, Consequence):
        deps.append(interp.consequence.unit)
    for r in row.date_rules:
        if r.anchor in anchors:
            deps.append(anchors[r.anchor]["defined_in"])
    for uid in list(deps):
        for op_id in (state[uid].annotations if uid in state else []):
            if op_provision.get(op_id):
                deps.append(op_provision[op_id])
    return sorted(set(deps))


def pin_value(state: dict[str, UState], uid: str) -> str:
    u = state.get(uid)
    if u is None:
        return "absent"
    return sha256_text(u.sha() + "|" + ",".join(sorted(u.annotations)))[:16]


# ---------------------------------------------------------------------------------------------- evaluation

class Register:
    def __init__(self, rowfile: RowFile, stages: list[StageResult], cal: Calendar, policy: str = "conservative"):
        self.rf, self.stages, self.cal, self.policy = rowfile, stages, cal, policy
        self.order = stage_order(stages)
        self.op_provision = {r.op.id: r.op.provision for s in stages for r in s.ops}
        self.op_stage = {r.op.id: s.stage for s in stages for r in s.ops}
        self.op_review = {r.op.id: r.op.review for s in stages for r in s.ops}
        self.issued = {s.stage: s.issued for s in stages}

    def interp_at(self, row: Row, stage: str) -> Interp | None:
        idx = self.order.index(stage)
        cands = [i for i in row.interpretations if i.stage in self.order and self.order.index(i.stage) <= idx]
        return cands[-1] if cands else None

    def pins_for(self, row: Row, interp: Interp, stage: StageResult) -> dict[str, str]:
        deps = dependencies(row, interp, stage.state, self.rf.anchors, self.op_provision)
        return {d: pin_value(stage.state, d) for d in deps}

    def evaluate(self, row: Row, s: StageResult) -> dict:
        st = s.state
        prim = st.get(row.units[0])
        eff = effective(st, row.units[0], row.follows_replacement)
        out = {"stage": s.stage, "stage_status": s.status}
        # --- status
        hist = (prim.history if prim else []) + ([h for h in eff.history if h not in prim.history]
                                                  if eff is not None and prim is not None and eff is not prim else [])
        here = [h for h in hist if self.op_stage.get(h) == s.stage]
        earlier = [h for h in hist if h not in here and self.order.index(self.op_stage.get(h, BASE)) < self.order.index(s.stage)]
        if prim is None or prim.status == "not_issued":
            status = "NOT ISSUED"
        elif eff.status == "deleted":
            status = f"DELETED ({', '.join(here or earlier)})" if here else f"DELETED (by {', '.join(earlier)})"
        elif eff.status == "revoked":
            status = f"REVOKED ({', '.join(here or earlier)})"
        elif eff.status == "superseded":
            status = f"REPLACED (by {eff.superseded_by})"
        elif prim.issued_by == s.stage or (eff.origin == "addendum_op" and here):
            status = "NEW"
        elif here:
            reinstated = any(self._op_type(h) == ("set_status", "reinstated") for h in here)
            status = ("REINSTATED-AMENDED" if reinstated else "AMENDED") + f" ({', '.join(here)})"
        elif earlier:
            status = f"ACTIVE (as amended by {', '.join(earlier)})"
        else:
            status = "ACTIVE"
        out["status"] = status
        active = prim is not None and eff is not None and eff.status == "active" and prim.status != "not_issued"
        out["active"] = active
        out["text"] = eff.text if eff is not None and eff.status != "not_issued" else ""
        out["cells"] = eff.cells if eff is not None else None
        out["effective_unit"] = eff.unit_id if eff is not None else None
        out["pages"] = eff.pages if eff is not None else []
        out["ops"] = hist
        out["ops_review"] = sorted({self.op_review.get(h, "?") for h in hist})
        # --- interpretation, quote, consequence
        it = self.interp_at(row, s.stage)
        out["interpretation_stage"] = it.stage if it else None
        problems, flags = [], []
        if it is None:
            if active:
                problems.append(f"no interpretation made at or before {s.stage}")
        elif active:
            if not found(it.quote, eff.text):
                problems.append(f"quote not found in the effective text at {s.stage}: '{it.quote[:60]}'")
            if isinstance(it.consequence, Consequence):
                cu = effective(st, it.consequence.unit, True)
                if cu is None or cu.status != "active" or not found(it.consequence.quote, cu.text):
                    problems.append(f"consequence quote not found in {it.consequence.unit} at {s.stage}")
        out["interpretation"] = it.model_dump(by_alias=True, exclude={"pins"}) if it else None
        # --- staleness
        stale = []
        if it is not None and active:
            now = self.pins_for(row, it, s)
            if not it.pins:
                stale.append("never pinned")
            for d, v in now.items():
                if d not in it.pins:
                    stale.append(f"new dependency {d}")
                elif it.pins[d] != v:
                    by = [h for h in (st[d].history + st[d].annotations if d in st else [])
                          if self.order.index(self.op_stage.get(h, BASE)) > self.order.index(it.stage)]
                    stale.append(f"{d} changed since {it.stage}" + (f" (by {', '.join(by)})" if by else ""))
            for d in it.pins:
                if d not in now:
                    stale.append(f"dependency {d} no longer applies")
        if problems and any(x != "never pinned" for x in stale):
            # The text the interpretation quoted has changed since it was made: that is what STALE means
            # (a person re-reads the row). A quote missing from a row that is NOT stale stays a problem (C16).
            stale += [f"{p} (expected: the interpretation predates the change)" for p in problems]
            problems = []
        out["stale"] = stale
        # --- transcription status of image readings the row relies on
        rel = [effective(st, u, True) for u in row.units] + \
              ([effective(st, it.consequence.unit, True)] if it and isinstance(it.consequence, Consequence) else [])
        reading = sorted({u.reading_status for u in rel if u is not None and u.origin == "image_reading"})
        out["transcription"] = "pending" if "pending" in reading else ("approved" if reading else "n/a (text layer)")
        if out["transcription"] == "pending":
            flags.append("image reading pending")
        val_old = [r for r in s.ops if r.op.type == "set_value" and r.op.target in row.units and r.details.get("reading_status") == "pending"]
        if val_old:
            flags.append("amended value replaces a value read from an image still pending review")
        # --- dates
        anchors = anchor_values(st, self.rf.anchors, self.issued)
        dates = []
        for rd in row.date_rules:
            rule = DateRule(rule_id=rd.rule_id, kind=rd.kind, purpose=rd.purpose, anchor=rd.anchor, offset=rd.offset,
                            unit=rd.unit, direction=rd.direction,
                            fixed=date.fromisoformat(rd.fixed) if rd.fixed else None, source_unit=rd.source_unit,
                            text=rd.text)
            ins = interpretations(rule, anchors, self.cal)
            plan = planning_value(rule, ins, self.policy)
            dates.append({"rule_id": rd.rule_id, "text": rd.text, "source_unit": rd.source_unit, "purpose": rd.purpose,
                          "anchor": rd.anchor, "anchor_value": anchors.get(rd.anchor).isoformat() if anchors.get(rd.anchor) else None,
                          "interpretations": [{"key": i.key, "label": i.label, "value": i.value.isoformat() if i.value else None,
                                               "basis": i.basis} for i in ins],
                          "planning": {"key": plan.key, "value": plan.value.isoformat() if plan.value else None,
                                       "policy": self.policy},
                          "readings_differ": len({i.value for i in ins}) > 1})
        out["dates"] = dates
        out["problems"], out["flags"] = problems, flags
        out["chain"] = self.chain(row, s)
        return out

    def _op_type(self, op_id: str):
        for s in self.stages:
            for r in s.ops:
                if r.op.id == op_id:
                    return (r.op.type, r.op.status)
        return (None, None)

    def chain(self, row: Row, s: StageResult) -> list[str]:
        """Evidence chain: the original unit and page, then each op with its provision and page."""
        st = s.state
        base = self.stages[0].state
        out = []
        u0 = base.get(row.units[0]) or st.get(row.units[0])
        if u0 is not None:
            out.append(f"{row.units[0]} ({u0.doc} p{','.join(map(str, u0.pages))}; {u0.origin.replace('_', ' ')})")
        eff = effective(st, row.units[0], row.follows_replacement)
        hist = []
        for uid in [row.units[0]] + ([eff.unit_id] if eff is not None and eff.unit_id != row.units[0] else []):
            hist += [h for h in (st[uid].history if uid in st else []) if h not in hist]
        for h in hist:
            prov = self.op_provision.get(h)
            pu = st.get(prov)
            out.append(f"{h} [{self.op_review.get(h)}] <- {prov} ({pu.doc} p{','.join(map(str, pu.pages))})" if pu else h)
        return out

    def all(self) -> list[dict]:
        return [{"row": r, "stages": {s.stage: self.evaluate(r, s) for s in self.stages}} for r in self.rf.rows]


def compute_pins(rowfile: RowFile, stages: list[StageResult], refresh: bool = False) -> int:
    """Fill the pins of interpretations that have none (or all, with refresh). Returns how many were written."""
    reg = Register(rowfile, stages, Calendar())
    by_stage = {s.stage: s for s in stages}
    n = 0
    for row in rowfile.rows:
        for it in row.interpretations:
            if (refresh or not it.pins) and it.stage in by_stage:
                it.pins = reg.pins_for(row, it, by_stage[it.stage])
                n += 1
    return n


def printed_date_conflicts(stage: StageResult, anchors: dict) -> list[dict]:
    """Form fields that print an anchor's date ("Proposal Due Date: 12 November 2026") but disagree with the
    anchor's effective value at this stage. Never corrected: raised as an issue for a person."""
    st = stage.state
    vals = anchor_values(st, anchors, {})
    out = []
    for uid, u in st.items():
        if u.status != "active" or u.kind != "form_field":
            continue
        for name, a in anchors.items():
            if normalize_latin(u.text).lower().startswith(a["name"].lower() + ":"):
                p = parse_date(u.text)
                v = vals.get(name)
                if p and v and p[0] != v:
                    out.append({"unit": uid, "printed": p[0].isoformat(), "anchor": name, "effective": v.isoformat(),
                                "defined_in": a["defined_in"], "page": u.pages, "doc": u.doc})
    return out


def dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str)
