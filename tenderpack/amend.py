"""The amendment path: one code path for the existing addenda and any future one.

    addendum PDF -> Stage 1 units (provisions) -> op file (drafted by draft.py and/or curated; every op
    `proposed` until a named person accepts it) -> validation -> application per stage -> states

Stages are BASE (the volumes as issued) and one per addendum, in addendum-number order with
non-decreasing issue dates (the issue date is parsed from the addendum's own cover line, not typed).

Operation types (a small closed set; PLAN §4.4):
  replace_text   old -> new inside one target unit; `old` must occur exactly once there
  set_value      one cell of a table row (e.g. an image-table cell; the result carries the reading's status)
  append_text    text added at the end of a target unit
  set_status     deleted | reinstated (with the new text quoted from the provision) | revoked (an addendum rule)
  replace_unit   a table or form replaced by one printed in the addendum (rows/fields follow by key)
  insert_unit    a new form (group of addendum units) and, optionally, a new list item after an anchor
  annotate       a clarification answer or rule linked to units: effect none | confirms | interprets |
                 adds_obligation | renumbers (with `renumber: {unit: new number}`, each number printed in the
                 provision; ids keep their issued numbers and outputs cite "10.6 (issued as 10.5)"). Rules may name
                 a `subject`; the units mentioning it are listed
Dispositions for provisions that carry no op: no_effect (reason) or unresolved (blocks validation). Every
provision is treated (an op, op content or a disposition).

Checks per op (an invalid op is listed and changes NOTHING: the state, including history, annotations and
the unit order, is restored to what it was before the op; ops are applied as transactions):
  C21 the op's quoted words (old/new/new_text) occur in its provision; a set_value's new value is the figure
      the provision states (with the row's unit where it has one) and its column is named in the provision;
      an inserted list item's WHOLE text is printed by the provision, the new group or a named unit of the
      same addendum (never a unit of the pack, never a supported quotation with words added around it)
  C22 the target exists and its state allows the operation; the declared target is the one the
      provision (or its section heading) cites (citations.verify_target); claims such as
      "deleted by Addendum No. 1 Section 4" agree with the ledger; replacement and inserted content is
      printed in the same addendum, after the provision, and a replacement's title names its target
  C23 replace_text: `old` occurs exactly once in the target
  C24 post-conditions: `old` count falls by one and `new` is present
  C27 `expect` assertions (e.g. marks moved between criteria, total unchanged)
Per addendum:
  C20 every provision is accounted for (an op, part of an op's replacement content, or a disposition)
  C25 no unit changed other than the declared targets, replaced/inserted content and the addendum's own units
An addendum is APPLIED when every op is valid, every provision accounted for and nothing unresolved;
otherwise PARTIAL. The validated state is the last stage reached through APPLIED addenda only; a
PARTIAL addendum produces a working state that never replaces the validated one.
Op review (proposed / accepted) is a separate question from validity and is carried on every result.
"""
from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .citations import citations, verify_target
from .dates import parse_date
from .textnorm import normalize_latin
from .util import load_yaml, sha256_text

BASE = "BASE"
OP_TYPES = ("replace_text", "set_value", "append_text", "set_status", "replace_unit", "insert_unit", "annotate")


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Op(_Strict):
    id: str
    provision: str
    type: Literal["replace_text", "set_value", "append_text", "set_status", "replace_unit", "insert_unit", "annotate"]
    target: str | None = None
    targets: list[str] = Field(default_factory=list)          # annotate
    old: str | None = None
    old_resolved: Literal["quoted", "matched_in_target"] = "quoted"
    new: str | None = None
    column: str | None = None                                  # set_value
    status: Literal["deleted", "reinstated", "revoked"] | None = None
    new_text: str | None = None                                # set_status reinstated / insert list item
    new_text_from: str | None = None                           # unit the inserted item's text is taken from
    replacement: str | None = None                             # replace_unit: group in the addendum
    new_group: str | None = None                               # insert_unit: group in the addendum
    anchor: str | None = None                                  # insert_unit list item: insert after this unit
    effect: Literal["none", "confirms", "interprets", "adds_obligation", "renumbers"] | None = None
    renumber: dict[str, str] = Field(default_factory=dict)     # annotate/renumbers: unit id -> its new printed number
    subject: str | None = None                                 # annotate rule: phrase whose mentions are listed
    covers: list[str] = Field(default_factory=list)            # provisions that are content of this op
    claims: list[dict] = Field(default_factory=list)           # [{unit, status, by_provision_prefix}]
    expect: list[dict] = Field(default_factory=list)           # [{row, column, delta}|{row, column, equals}|{contains}]
    issue: str | None = None                                   # something the op leaves open for a person
    note: str | None = None
    origin: Literal["pattern", "assistant", "person"] = "assistant"
    review: Literal["proposed", "accepted", "rejected"] = "proposed"
    reviewer: str | None = None


class Disposition(_Strict):
    provision: str
    disposition: Literal["no_effect", "unresolved"]
    reason: str
    candidates: list[str] = Field(default_factory=list)
    origin: Literal["pattern", "assistant", "person"] = "assistant"


class OpFile(_Strict):
    addendum: str
    issued_from: str                   # unit whose text holds the issue date ("Issued 22 October 2026")
    prepared_by: str
    method: str
    ops: list[Op] = Field(default_factory=list)
    dispositions: list[Disposition] = Field(default_factory=list)


def load_opfile(path: Path) -> OpFile:
    return OpFile.model_validate(load_yaml(path))


# ---------------------------------------------------------------------------------------------- state

@dataclass
class UState:
    unit_id: str
    doc: str
    kind: str
    status: str                       # active | deleted | revoked | superseded | not_issued
    text: str
    cells: dict | None
    pages: list[int]
    origin: str                       # text_layer | image_reading | addendum_op
    reading_status: str | None        # pending | approved (image readings only)
    parent: str | None = None
    reading_subject: str | None = None  # review-subject fingerprint of the image reading (content + uncertainties + evidence)
    label: str | None = None
    number: str | None = None                                    # its printed number after a renumbering op, if any
    history: list[str] = field(default_factory=list)            # op ids that changed this unit
    annotations: list[str] = field(default_factory=list)        # op ids that annotate it
    superseded_by: str | None = None
    issued_by: str | None = None                                 # addendum stage that issued it (addendum units)

    def sha(self) -> str:
        return sha256_text(json.dumps({"status": self.status, "text": self.text, "cells": self.cells},
                                      ensure_ascii=False, sort_keys=True))

    def row_text(self) -> str:
        return " | ".join(f"{k}: {v}" for k, v in (self.cells or {}).items() if v)


def base_state(units: list[dict], addenda: list[str]) -> dict[str, UState]:
    st: dict[str, UState] = {}
    for u in units:
        doc = u["doc"]
        add = doc in addenda
        st[u["unit_id"]] = UState(
            unit_id=u["unit_id"], doc=doc, kind=u["kind"], status="not_issued" if add else "active",
            text=u.get("text", ""), cells=copy.deepcopy(u.get("cells")), pages=list(u.get("pages", [])),
            origin=u.get("origin", "text_layer"), reading_status=(u.get("reading") or {}).get("status"),
            parent=u.get("parent"), label=u.get("label"), issued_by=doc if add else None,
            reading_subject=(u.get("reading") or {}).get("subject_sha256"))
    return st


def group_members(state: dict[str, UState], group: str, exclude: set[str] = frozenset()) -> list[str]:
    """Units of a group id: the unit itself, ids under 'group/', and the group's heading ('DOC:H:X')."""
    doc, _, local = group.partition(":")
    out = [k for k in state if (k == group or k.startswith(group + "/") or k == f"{doc}:H:{local}") and k not in exclude]
    return out


def _contains(text: str, phrase: str) -> int:
    return normalize_latin(text).count(normalize_latin(phrase))


def _quoted_in(provision_text: str, phrase: str) -> bool:
    return normalize_latin(phrase).replace("'", "") in normalize_latin(provision_text).replace("'", "")


def _evidence_form(t: str) -> str:
    return " ".join(normalize_latin(t or "").replace("'", "").split()).lower()


def unevidenced_additions(prev: dict[str, "UState"], cur: dict[str, "UState"], addendum: str) -> list[str]:
    """C47, independent of the op types: every word a unit of the pack gains between two consecutive stages
    (a new unit, words inserted or substituted in its text, a new cell value) must be printed somewhere in that
    stage's addendum. Returns 'unit: added words' for each run of added words the addendum does not print."""
    import difflib
    evidence = " \n ".join(_evidence_form(u.text) for u in cur.values() if u.doc == addendum)
    out = []
    for k, u in cur.items():
        if u.doc == addendum:
            continue
        p = prev.get(k)
        runs: list[str] = []
        if p is None:
            runs = [u.text or ""]
        else:
            if (u.text or "") != (p.text or ""):
                a, b = (p.text or "").split(), (u.text or "").split()
                for tag, _, _, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
                    if tag in ("insert", "replace"):
                        runs.append(" ".join(b[j1:j2]))
            if u.cells and p.cells:
                runs += [v for c, v in u.cells.items() if v and v != p.cells.get(c)]
        for run in runs:
            w = _evidence_form(run).strip(" ,;:.")
            if w and w not in evidence:
                out.append(f"{k}: '{run[:160]}'")
    return out


# ---------------------------------------------------------------------------------------------- results

@dataclass
class OpResult:
    op: Op
    stage: str
    valid: bool
    checks: list[dict]
    changed: list[str] = field(default_factory=list)
    details: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"op": self.op.model_dump(exclude_none=True), "stage": self.stage, "valid": self.valid,
                "checks": self.checks, "changed": self.changed, "details": self.details}


@dataclass
class StageResult:
    stage: str
    addendum: str | None
    issued: str | None
    status: str                         # BASE | APPLIED | PARTIAL
    state: dict[str, UState]
    ops: list[OpResult] = field(default_factory=list)
    coverage: list[dict] = field(default_factory=list)   # one per provision: {provision, accounted_by, disposition}
    problems: list[str] = field(default_factory=list)
    scope_leak: list[str] = field(default_factory=list)
    opfile: str | None = None
    prepared_by: str | None = None


# ---------------------------------------------------------------------------------------------- engine

PROVISION_KINDS = {"clause", "paragraph", "list_item", "numbered_paragraph", "lead_in_paragraph", "note", "note_intro",
                   "table_row", "form_field", "footnote", "reading_block"}


def provisions(state: dict[str, UState], addendum: str) -> list[str]:
    return [k for k, u in state.items() if u.doc == addendum and u.kind in PROVISION_KINDS]


def heading_of(units_order: list[str], state: dict[str, UState], unit_id: str) -> str:
    """Text of the nearest heading before a unit in the same document (section headings carry citations)."""
    doc = state[unit_id].doc
    i = units_order.index(unit_id)
    for k in reversed(units_order[:i]):
        if state[k].doc != doc:
            break
        if state[k].kind == "heading":
            return state[k].text
    return ""


class Engine:
    def __init__(self, units: list[dict], opfiles: list[OpFile]):
        self.units = units
        self.order = [u["unit_id"] for u in units]
        self.opfiles = sorted(opfiles, key=lambda f: int(f.addendum.split("-")[1]))
        self.addenda = [f.addendum for f in self.opfiles]

    # ------------------------------------------------------------------ run
    def run(self) -> list[StageResult]:
        state = base_state(self.units, self.addenda + [d for d in {u["doc"] for u in self.units}
                                                      if d.startswith("ADD-") and d not in self.addenda])
        stages = [StageResult(BASE, None, None, "BASE", copy.deepcopy(state))]
        prev_issued = None
        for f in self.opfiles:
            st = copy.deepcopy(stages[-1].state)
            res = StageResult(f.addendum, f.addendum, None, "APPLIED", st, opfile=f.addendum, prepared_by=f.prepared_by)
            issued = parse_date(st[f.issued_from].text) if f.issued_from in st else None
            res.issued = issued[0].isoformat() if issued else None
            if res.issued is None:
                res.problems.append(f"issue date not found in {f.issued_from}")
            elif prev_issued and res.issued < prev_issued:
                res.problems.append(f"issued {res.issued} before the previous addendum ({prev_issued})")
            prev_issued = res.issued or prev_issued
            for k, u in st.items():                                   # the addendum's own units are issued
                if u.doc == f.addendum and u.status == "not_issued":
                    u.status = "active"
            before = {k: u.sha() for k, u in st.items()}
            for op in self._ordered(f):
                snap, order = copy.deepcopy(st), list(self.order)
                r = self._apply(op, st, f.addendum)
                if not r.valid:                       # a failed op changes nothing: restore state and unit order
                    st.clear()
                    st.update(snap)
                    self.order[:] = order
                    r.changed = []
                    r.details.pop("content", None)
                res.ops.append(r)
            self._coverage(res, f)
            self._scope(res, before, f.addendum)
            if res.problems or res.scope_leak or any(not r.valid for r in res.ops) or \
                    any(c["disposition"] == "unresolved" or not c["accounted_by"] for c in res.coverage):
                res.status = "PARTIAL"
            stages.append(res)
        return stages

    def _ordered(self, f: OpFile) -> list[Op]:
        pos = {k: i for i, k in enumerate(self.order)}
        return sorted(f.ops, key=lambda o: (pos.get(o.provision, 10 ** 9), f.ops.index(o)))

    # ------------------------------------------------------------------ coverage and scope
    def _coverage(self, res: StageResult, f: OpFile) -> None:
        st = res.state
        disp = {d.provision: d for d in f.dispositions}
        by_op: dict[str, list[str]] = {}
        valid_for: dict[str, bool] = {}
        for r in res.ops:
            for p in [r.op.provision] + r.op.covers + r.details.get("content", []):
                if r.op.id not in by_op.setdefault(p, []):
                    by_op[p].append(r.op.id)
                valid_for[p] = valid_for.get(p, False) or r.valid
        for p in provisions(st, f.addendum):
            d = disp.get(p)
            if d:
                kind, reason = d.disposition, d.reason
            elif p in by_op:
                # a provision whose only ops are invalid is not accounted for: it counts as unresolved (C20)
                kind, reason = ("op", "") if valid_for[p] else ("unresolved", "every op for this provision is invalid")
            else:
                kind, reason = "UNACCOUNTED", ""
            res.coverage.append({"provision": p, "page": st[p].pages[0] if st[p].pages else None,
                                 "text": st[p].text[:160], "accounted_by": by_op.get(p, []) or ([d.disposition] if d else []),
                                 "disposition": kind, "reason": reason})
        unknown = [d.provision for d in f.dispositions if d.provision not in st]
        if unknown:
            res.problems.append(f"dispositions for provisions that do not exist: {unknown}")

    def _scope(self, res: StageResult, before: dict[str, str], addendum: str) -> None:
        allowed = set()
        for r in res.ops:
            allowed |= set(r.changed)
        for k, u in res.state.items():
            if k not in before:
                if k not in allowed:
                    res.scope_leak.append(f"{k} appeared without an op")
            elif u.sha() != before[k] and k not in allowed and u.doc != addendum:
                res.scope_leak.append(f"{k} changed without an op targeting it")

    # ------------------------------------------------------------------ one op
    def _apply(self, op: Op, st: dict[str, UState], addendum: str) -> OpResult:
        stage = addendum
        checks: list[dict] = []
        r = OpResult(op, stage, False, checks)

        def check(cid, ok, detail):
            checks.append({"id": cid, "ok": bool(ok), "detail": detail})
            return bool(ok)

        if op.review == "rejected":
            check("REVIEW", False, f"rejected by {op.reviewer or 'a reviewer'}")
            return r
        prov = st.get(op.provision)
        if not check("C21", prov is not None and prov.doc == addendum, f"provision {op.provision} belongs to {addendum}"):
            return r
        ptext = prov.text
        cite_text = ptext + " " + heading_of(self.order, st, op.provision)
        quoted = [x for x in (op.old if op.old_resolved == "quoted" else None, op.new, op.new_text) if x]
        if op.type in ("replace_text", "append_text", "set_status") and quoted:
            bad = [q for q in quoted if not _quoted_in(ptext, q)]
            if not check("C21", not bad, f"quoted words found in {op.provision}" if not bad else f"not in the provision: {bad}"):
                return r
        ids = set(st)
        label = lambda uid: st[uid].label if uid in st else None  # noqa: E731

        if op.type == "annotate":
            missing = [t for t in op.targets if t not in st and not group_members(st, t)]
            if not check("C22", op.targets and not missing, f"targets exist: {op.targets}" + (f"; missing {missing}" if missing else "")):
                return r
            if op.effect in ("confirms", "interprets", "adds_obligation"):
                cited_ok = [verify_target(t, cite_text, ids, label)[0] or t.startswith(addendum) for t in op.targets]
                if not check("C22", all(cited_ok), "every annotated target is cited by the provision"
                             if all(cited_ok) else f"not cited: {[t for t, ok in zip(op.targets, cited_ok) if not ok]}"):
                    return r
            if op.effect == "renumbers":
                bad = [k for k in op.renumber if k not in op.targets or k not in st]
                unstated = [v for v in op.renumber.values() if not re.search(r"(?<![\d.])" + re.escape(v) + r"(?![\d])", ptext)]
                if not check("C21", op.renumber and not bad and not unstated,
                             f"renumbering {op.renumber} stated in {op.provision}" if op.renumber and not bad and not unstated
                             else f"renumbering not supported by the provision: targets {bad}, numbers not printed {unstated}"):
                    return r
                for k, v in op.renumber.items():
                    st[k].number = v
                r.details["renumbered"] = dict(op.renumber)
            for t in op.targets:
                for k in ([t] if t in st else group_members(st, t)):
                    st[k].annotations.append(op.id)
            if op.subject:
                r.details["mentions"] = [k for k, u in st.items() if u.status == "active" and k != op.provision
                                         and u.doc != addendum and _contains(u.text, op.subject)]
            for e in op.expect:
                if "contains" in e:
                    t = st.get(e.get("unit", op.targets[0]))
                    if not check("C27", t is not None and _contains(t.text, e["contains"]) >= 1,
                                 f"{e.get('unit', op.targets[0])} still says '{e['contains']}'"):
                        return r
            r.valid = True
            return r

        # every other op has one declared target that must be the cited one
        target = op.target
        if op.type == "insert_unit":
            target = op.anchor or op.new_group
        ok, why, cited = verify_target(target, cite_text, ids, label) if target else (False, "no target", [])
        if op.type == "insert_unit" and op.new_group and not op.anchor:
            ok, why = True, "new group from this addendum"
        r.details["cited"] = cited
        if not check("C22", ok, why):
            return r
        for c in op.claims:
            u = st.get(c["unit"])
            hist_ok = u is not None and u.status == c.get("status", u.status if u else None) and \
                any(h.split("/")[0] == c["by_provision_prefix"].split(":")[0] and
                    self._op_provision(h).startswith(c["by_provision_prefix"]) for h in u.history)
            if not check("C22", hist_ok, f"claim: {c['unit']} is {c.get('status')} by {c['by_provision_prefix']}"):
                return r

        if op.type in ("replace_text", "append_text", "set_status", "set_value"):
            t = st.get(op.target)
            if not check("C22", t is not None, f"target {op.target} exists"):
                return r
            r.details["reading_status"] = t.reading_status
            if op.type == "replace_text":
                if not check("C22", t.status == "active", f"target is {t.status}"):
                    return r
                n = _contains(t.text, op.old)
                if not check("C23", n == 1, f"'{op.old}' occurs {n} time(s) in {op.target}"):
                    r.details["also_in"] = _also_in(st, op.target, op.old)
                    return r
                r.details["also_in"] = _also_in(st, op.target, op.old)
                new_text = _replace_once(t.text, op.old, op.new)
                if not check("C24", _contains(new_text, op.old) == n - 1 + _contains(op.new, op.old)
                             and _contains(new_text, op.new) >= 1, "post-condition: old removed once, new present"):
                    return r
                r.details["before"], t.text = t.text, new_text
                if t.cells:                  # a table row: the cell that holds the words changes with the text
                    hit = [c for c, v in t.cells.items() if v and _contains(v, op.old) == 1]
                    if len(hit) == 1:
                        r.details["cell"] = hit[0]
                        t.cells[hit[0]] = _replace_once(t.cells[hit[0]], op.old, op.new)
            elif op.type == "append_text":
                if not check("C22", t.status == "active", f"target is {t.status}"):
                    return r
                if not check("C24", _contains(t.text, op.new) == 0, "appended text not already present"):
                    return r
                r.details["before"], t.text = t.text, (t.text.rstrip() + " " + op.new).strip()
            elif op.type == "set_value":
                if not check("C22", t.status == "active" and t.cells is not None and op.column in t.cells,
                             f"target is an active table row with column '{op.column}'"):
                    return r
                if not check("C21", _names_column(ptext, op.column),
                             f"the provision names the column '{op.column}'" if _names_column(ptext, op.column)
                             else f"the provision does not name the column '{op.column}'"):
                    return r
                unit = next((v for c, v in t.cells.items() if c.lower() == "unit" and v and v != "-"), None)
                if not re.fullmatch(r"[<>≤≥]?\s*-?\d[\d,]*(?:\.\d+)?(?:\s*[-–]\s*\d[\d,]*(?:\.\d+)?)?", (op.new or "").strip()):
                    unit = None              # a text cell (e.g. a basis of assessment) is quoted as it stands, with no unit
                ok_value = _states_value(ptext, op.new or "", unit) if unit else _quoted_in(ptext, op.new or "")
                if not check("C21", ok_value, f"the provision states the new value '{op.new}'" + (f" {unit}" if unit else "")
                             if ok_value else f"the provision does not state the new value '{op.new}'" + (f" {unit}" if unit else "")):
                    return r
                old_value = r.details["old_value"] = t.cells[op.column]
                t.cells[op.column] = op.new
                cell_before, cell_after = f"{op.column}: {old_value}", f"{op.column}: {op.new}"
                r.details["before"] = t.text
                t.text = t.text.replace(cell_before, cell_after, 1) if t.text.count(cell_before) == 1 else t.row_text()
            else:                                                       # set_status
                need = {"deleted": "active", "reinstated": "deleted", "revoked": "active"}[op.status]
                if not check("C22", t.status == need, f"{op.status} needs the target {need}; it is {t.status}"):
                    return r
                if op.status == "reinstated":
                    if not check("C22", bool(op.new_text), "reinstatement quotes the new text"):
                        return r
                    r.details["before"], t.text = t.text, op.new_text
                    t.status = "active"
                else:
                    t.status = op.status
            t.history.append(op.id)
            r.changed = [op.target]
        elif op.type == "replace_unit":
            old = group_members(st, op.target)
            new = [k for k in group_members(st, op.replacement, exclude={op.provision}) if st[k].kind != "note"
                   and not k.split("/")[-1].startswith(("note", "notes"))]
            if not check("C22", old and new and all(st[k].status == "active" for k in old),
                         f"{op.target} ({len(old)} units) replaced by {op.replacement} ({len(new)} units)"):
                return r
            if not check("C22", all(st[k].doc == addendum for k in new),
                         f"the replacement {op.replacement} is printed in {addendum}" if all(st[k].doc == addendum for k in new)
                         else f"the replacement {op.replacement} is not content of {addendum}"):
                return r
            pos = {k: i for i, k in enumerate(self.order)}
            after = all(pos.get(k, -1) > pos.get(op.provision, 10 ** 9) for k in new if st[k].kind != "heading")
            if not check("C22", after, "the replacement is printed after the provision" if after
                         else "the replacement is not printed after the provision"):
                return r
            title = _group_title(st, op.replacement)
            if not check("C22", _names_target(title, op.target), f"the replacement's title names {op.target}: '{title[:60]}'"
                         if _names_target(title, op.target) else f"the replacement's title does not name {op.target}: '{title[:60]}'"):
                return r
            by_label = {st[k].label: k for k in new if st[k].label}
            for k in old:
                st[k].status, st[k].superseded_by = "superseded", by_label.get(st[k].label) or op.replacement
                st[k].history.append(op.id)
            for k in new:
                st[k].history.append(op.id)
            r.changed, r.details["content"] = old + new, new
            for e in op.expect:
                ok, why = _expect_rows(st, e, old, new)
                if not check("C27", ok, why):
                    for k in old:                                       # undo: an invalid op is not applied
                        st[k].status, st[k].superseded_by = "active", None
                        st[k].history.remove(op.id)
                    for k in new:
                        st[k].history.remove(op.id)
                    r.changed = []
                    return r
        elif op.type == "insert_unit":
            content = []
            if op.new_group:
                content = [k for k in group_members(st, op.new_group) if st[k].doc == addendum]
                if not check("C22", bool(content), f"new group {op.new_group} has {len(content)} units"):
                    return r
                for k in content:
                    st[k].history.append(op.id)
            if op.anchor:
                a = st.get(op.anchor)
                if not check("C22", a is not None and a.status == "active", f"anchor {op.anchor} exists and is active"):
                    return r
                if op.new_text_from and not check(
                        "C21", op.new_text_from in st and st[op.new_text_from].doc == addendum,
                        f"the inserted text is taken from {op.new_text_from}, a unit of {addendum}"
                        if op.new_text_from in st and st[op.new_text_from].doc == addendum
                        else f"{op.new_text_from} is not a unit of {addendum}: not evidence of what {addendum} inserts"):
                    return r
                text = op.new_text or (st[op.new_text_from].text if op.new_text_from in st else "")
                if not check("C22", bool(text), "the inserted item has text (quoted or taken from a named unit)"):
                    return r
                # evidence for the WHOLE inserted text: printed in full by the provision, the new group or the named unit
                evid = [op.provision] + content + ([op.new_text_from] if op.new_text_from else [])
                where = next((k for k in evid if k in st and st[k].doc == addendum and _quoted_in(st[k].text, text)), None)
                if not check("C21", where is not None, f"the whole inserted text is printed in {where}" if where
                             else f"the inserted text is not printed in full by {addendum}: '{text[:120]}'"):
                    return r
                r.details["evidence"] = where
                new_id = f"{op.anchor}+{addendum}"
                if not check("C22", new_id not in st, f"{new_id} is a new id"):
                    return r
                st[new_id] = UState(new_id, a.doc, a.kind, "active", text, None, list(prov.pages), "addendum_op",
                                    None, parent=a.parent, label=f"after {a.label}", history=[op.id], issued_by=addendum)
                content.append(new_id)
                self.order.insert(self.order.index(op.anchor) + 1, new_id)
            r.changed, r.details["content"] = content, content
        r.valid = True
        return r

    def _op_provision(self, op_id: str) -> str:
        for f in self.opfiles:
            for o in f.ops:
                if o.id == op_id:
                    return o.provision
        return ""


def _names_column(provision_text: str, column: str) -> bool:
    return bool(column) and normalize_latin(column).lower() in normalize_latin(provision_text).lower()


def _states_value(provision_text: str, value: str, unit: str | None) -> bool:
    """The provision states the figure (followed by the row's unit where the row has one)."""
    if not value.strip():
        return False
    t = normalize_latin(provision_text)
    rx = r"(?<![\d.,])" + re.escape(value.strip()) + r"(?![\d,]|\.\d)"
    if unit:
        rx += r"\s*" + re.escape(normalize_latin(unit))
    return re.search(rx, t, re.I) is not None


def _group_title(st: dict[str, UState], group: str) -> str:
    doc, _, local = group.partition(":")
    for k in (group, f"{doc}:H:{local}"):
        if k in st and st[k].text:
            return st[k].text
    return ""


def _names_target(title: str, target: str) -> bool:
    """'Table 1-1 (revised) ...' names VOL-I:T1-1; 'APPENDIX A — REVISED FORM 4-A' names VOL-IV:F4-A."""
    local = target.partition(":")[2]
    if re.fullmatch(r"T\d+-\d+", local):
        phrase = "Table " + local[1:]
    elif re.fullmatch(r"F\d-[A-Z]", local):
        phrase = "Form " + local[1:]
    else:
        phrase = local
    return re.search(r"(?<![\w-])" + re.escape(phrase) + r"(?![\w-])", normalize_latin(title), re.I) is not None


def _also_in(st: dict[str, UState], target: str, words: str) -> list[str]:
    """Other active volume units with the same words (addenda quoting them are not targets)."""
    return [k for k, u in st.items() if u.status == "active" and k != target and not u.doc.startswith("ADD-")
            and _contains(u.text, words)]


def _replace_once(text: str, old: str, new: str) -> str:
    if old in text:
        return text.replace(old, new, 1)
    # tolerate typographic quotes/dashes: locate via the normalised form, character by character
    norm = normalize_latin(text)
    i = norm.find(normalize_latin(old))
    if i < 0 or len(norm) != len(text):
        return text
    return text[:i] + new + text[i + len(old):]


def _num(s: str | None) -> float | None:
    m = re.search(r"-?\d+(?:\.\d+)?", s or "")
    return float(m.group(0)) if m else None


def _expect_rows(st, e: dict, old: list[str], new: list[str]) -> tuple[bool, str]:
    col = e["column"]
    find = lambda ids, key: next((st[k] for k in ids if st[k].label == key or (st[k].cells or {}).get("Criterion") == key), None)  # noqa: E731
    n = find(new, e["row"])
    if n is None:
        return False, f"row {e['row']} not in the replacement"
    if "equals" in e:
        return _num(n.cells.get(col)) == float(e["equals"]), f"{e['row']} {col} = {n.cells.get(col)} (expected {e['equals']})"
    o = find(old, e["row"])
    if o is None:
        return False, f"row {e['row']} not in the replaced table"
    d = _num(n.cells.get(col)) - _num(o.cells.get(col))
    return d == float(e["delta"]), f"{e['row']} {col}: {o.cells.get(col)} -> {n.cells.get(col)} (change {d:+g}, expected {e['delta']:+g})"


def validated_stage(stages: list[StageResult]) -> StageResult:
    """The last stage reached through APPLIED addenda only."""
    last = stages[0]
    for s in stages[1:]:
        if s.status != "APPLIED":
            break
        last = s
    return last


def provision_citations(state: dict[str, UState], unit_id: str) -> list[str]:
    return [c.target for c in citations(state[unit_id].text)]
