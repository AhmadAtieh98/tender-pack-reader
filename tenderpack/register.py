"""The A1 register: requirement rows evaluated at every stage of the amendment path.

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

An obligation whose words an addendum deletes from a unit that stays in force (ADD-03 4.1 in blind rehearsal 02: the
model audit opinion struck out of VOL-I 10.3) is not DELETED: its unit is still active. The interpretation made at
that stage carries `removed: {by: <op id>, note}`; the row is then REMOVED (<op id>) and out of force from that stage
(A3, A5 and the general gate leave it out; A1 shows it). The removal needs evidence that THIS row's words went
(session 10): the op must exist, be applied at or before that stage and have changed one of the row's units, and the
row's quote must be in that unit immediately before the op and absent from the same unit immediately after it. A
quote that survives the op (the rest of VOL-I 10.3: the Financial Model is still to be submitted) is a problem (C16)
saying that the row's words survive the op, and an unsupported removal never takes a row out of force: the row keeps
its status, consequence and A5 activities until a person re-makes the reading.

Separate statuses, never merged:
  status            what the documents say at that stage (ACTIVE / AMENDED / REMOVED / DELETED / ...)
  transcription     review status of an image reading the row relies on (pending until approved)
  interpretation    review status of the row itself (proposed until a named person accepts it)
  ops               review status of the amendment ops that changed it (proposed / accepted)
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_serializer

from .amend import BASE, StageResult, UState, unit_pin
from .dates import Calendar, DateRule, Interpretation, interpretations, parse_date, planning_value
from .textnorm import normalize_arabic, normalize_latin
from .util import load_yaml, sha256_text

# What each class means (session 09 separated three things the vocabulary had conflated):
#   rejection, disqualification, non_responsive, exclusion   the Proposal is out, as stated (BID_OUT; A3 explicit)
#   score_elimination   below the VOL-I 11.3 technical threshold: Envelope B returned unopened (not a zero on one criterion)
#   document_refusal    a stated refusal of a submitted document ("will not be accepted", "treated as not submitted")
#                       whose effect on the Proposal is NOT stated: the row keeps its place in the VOL-I 11.1(i) pass or
#                       fail gate and is never shown as a disqualification
#   criterion_zero      zero marks under one scoring criterion: a scored consequence, neither a disqualification nor the
#                       score_elimination threshold (any threshold risk is stated in the row, by a person)
#   lesser              any other stated consequence short of those (pages removed, not scored, ...)
#   contractual         a post-award remedy (termination, deduction, ...)
CONSEQUENCE_CLASSES = ("rejection", "disqualification", "non_responsive", "exclusion", "score_elimination",
                       "document_refusal", "criterion_zero", "lesser", "contractual")
BID_OUT = ("rejection", "disqualification", "non_responsive", "exclusion")


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class Consequence(_Strict):
    cls: Literal["rejection", "disqualification", "non_responsive", "exclusion", "score_elimination", "document_refusal",
                 "criterion_zero", "lesser", "contractual"] = Field(alias="class")    # meanings: CONSEQUENCE_CLASSES
    unit: str
    quote: str
    gloss: str | None = None                     # proposed translation of a non-English quote (never checked as evidence)


class Removal(_Strict):
    """The obligation's words were deleted from a unit that stays in force (session 09): `by` is the op that deleted
    them. The row is REMOVED from the stage of the interpretation that carries this, and is no longer in force, but
    only while the removal is supported (Register._removal_problems, session 10); otherwise the row stays in force."""
    by: str
    note: str = ""


class Interp(_Strict):
    stage: str
    quote: str                                   # must be found in the row's effective text at every stage it is used
    parameters: dict = Field(default_factory=dict)
    consequence: Consequence | Literal["none_stated"] = "none_stated"
    note: str | None = None
    removed: Removal | None = None               # the words were deleted; `quote` is then checked before the op instead
    pins: dict[str, str] = Field(default_factory=dict)

    @model_serializer(mode="wrap")
    def _without_unset_removal(self, handler):
        # an interpretation without `removed` dumps exactly as before the field existed, so what a review decision on
        # a row is bound to (review.row_binding) does not change for rows that do not use it
        d = handler(self)
        if self.removed is None:
            d.pop("removed", None)
        return d


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
    note: str = ""                               # kind unresolved: why the program does not compute it


class DateNote(_Strict):
    """A date or period phrase in the row's units that no date rule plans, with the reason (C30)."""
    text: str                                    # the words, as printed
    treatment: Literal["duration", "post_award", "not_a_date", "unresolved"]
    reason: str


class PostAwardEvidence(_Strict):
    """What would evidence a post-award obligation (session 08). Never a claim that the bidder holds anything:
    `proposed` is a requirement to produce in future, `not_applicable` says why none applies, `unresolved` names what
    the pack does not specify. Every `basis` quote must be in the unit's text (check-register)."""
    kind: Literal["proposed", "not_applicable", "unresolved"]
    text: str
    basis: list[dict] = Field(default_factory=list)          # [{unit, page, words}]
    when: str | None = None
    reason: str | None = None
    missing: str | None = None
    bid_stage_note: str | None = None


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
    date_notes: list[DateNote] = Field(default_factory=list)
    confidence: Literal["high", "medium", "low"]
    confidence_reason: str
    issues: list[str] = Field(default_factory=list)
    follows_replacement: bool = False            # a replaced table row / form field continues in its replacement
    owner: str | None = None                     # role accountable for the row (defaults to the discipline)
    no_deliverable: str | None = None            # why a bid-stage row needs no deliverable (A5 two-way check)
    post_award_evidence: PostAwardEvidence | None = None   # post-award rows: proposed evidence / not applicable / unresolved
    review: Literal["proposed", "accepted"] = "proposed"
    reviewer: str | None = None

    @property
    def owner_role(self) -> str:
        return self.owner or self.discipline


class RowFile(_Strict):
    prepared_by: str
    method: str
    anchors: dict[str, dict]                     # {"PDD": {"name": "Proposal Due Date", "defined_in": "VOL-I:6.1"}}
    include: list[str] = Field(default_factory=list)   # further row files (globs relative to this file)
    rows: list[Row]
    files: dict[str, str] = Field(default_factory=dict)  # row id -> included file it came from (filled on load)


class RowPart(_Strict):
    doc: str
    prepared_by: str
    method: str | None = None
    rows: list[Row]


def pins_path(rows_path: Path) -> Path:
    return Path(rows_path).with_name("pins.yaml")


def load_rows(path: Path, lenient: list | None = None) -> RowFile:
    """Rows are hand-curated; their pins are machine-written by `tenderpack pin` into pins.yaml beside them
    ({row id: {interpretation stage: {unit: hash}}}), so re-pinning never rewrites the curated file.
    With `lenient` (a list), an included file that does not load is skipped and its error appended to it
    (used by check-register while several files are being drafted); otherwise any error raises."""
    rf = RowFile.model_validate(load_yaml(path))
    seen = {r.id for r in rf.rows}
    for pattern in rf.include:
        for f in sorted(Path(path).parent.glob(pattern)):
            try:
                part = RowPart.model_validate(load_yaml(f) or {})
                dup = [r.id for r in part.rows if r.id in seen]
                if dup:
                    raise ValueError(f"row ids defined twice: {dup}")
            except Exception as e:                       # noqa: BLE001
                if lenient is None:
                    raise ValueError(f"{f}: {e}") from e
                lenient.append(f"{f.name}: skipped, does not load: {str(e)[:400]}")
                continue
            for r in part.rows:
                seen.add(r.id)
                rf.files[r.id] = f.name
                rf.rows.append(r)
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


_NUMBER_WORDS = ("zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|"
                 "sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|"
                 "thousand|and")


def _rule_shape(text: str):
    """A rule's words with the period wildcarded: number words and '(n)' match any other number."""
    parts = []
    for tok in re.findall(r"\(\d+\)|\d+|[A-Za-z]+(?:-[A-Za-z]+)*|[^\sA-Za-z\d]", normalize_latin(text)):
        if re.fullmatch(r"\(\d+\)", tok):
            parts.append(r"\(\d+\)")
        elif re.fullmatch(r"\d+", tok):
            parts.append(r"\d+")
        elif all(w.lower() in _NUMBER_WORDS.split("|") for w in tok.split("-")):
            parts.append(r"(?:[a-z]+(?:[- ][a-z]+)*)")
        else:
            parts.append(re.escape(tok))
    return re.compile(r"\s*".join(parts), re.I)


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


def anchor_details(state: dict[str, UState], anchors: dict, stages_issued: dict[str, str | None],
                   op_stage: dict[str, str] | None = None, op_provision: dict[str, str] | None = None) -> dict:
    """What the effective text of each anchor's defining unit (rows.yaml `anchors: {PDD: {defined_in: VOL-I:6.1}}`)
    states at this state: {name: {"date": date | None, "time": "HH:MM" | None, "tz": "Riyadh time" | None,
    "unit": defined_in, "as_amended_by": [op ids in the unit's history, in order], "source": "VOL-I 6.1 as amended by
    ADD-01 2.1, ADD-03 2.1" ("VOL-I 6.1" when unamended)}}.

    The date and time are read with dates.parse_date (the date is the value anchor_values gives); the timezone label
    is the 'Xxx time' words printed right after the time, else anywhere in the text. Anything the text does not
    state is None, never a default. `source` is written with the references of the A1 source column (Register._ref:
    '<doc> <clause>', a renumbered unit '<number> (issued as <clause>)') without page numbers, then ' as amended by '
    and the provision of each op in the unit's history. With `op_stage` (op id -> stage), history entries that are
    not ops of the amendment path are left out, as A1's units detail does; `op_provision` maps op ids to their
    provisions (default: the op id with its first '/' read as ':' and any '(...)' suffix dropped). `stages_issued`
    is accepted for symmetry with anchor_values: issue dates have no defining unit and are not returned here."""
    near = re.compile(r"(?<![\d:.])(?:[01]\d|2[0-3]):[0-5]\d(?![\d:])(?:\s+hours?)?,?\s+\(?([A-Z][a-z]+ time)\b")
    anywhere = re.compile(r"\b([A-Z][a-z]+ time)\b")
    not_a_zone = {"The", "Any", "This", "That", "Each", "Every", "Such", "Same", "No", "At", "Its", "Their", "Which"}

    def ref(uid: str) -> str:
        u = state.get(uid)
        doc, _, local = uid.partition(":")
        return f"{doc} {u.number} (issued as {local})" if u is not None and u.number else f"{doc} {local}"

    def provision(op_id: str) -> str:
        return (op_provision or {}).get(op_id) or re.sub(r"\(.*\)$", "", op_id).replace("/", ":", 1)

    out = {}
    for name, a in anchors.items():
        uid = a["defined_in"]
        u = state.get(uid)
        text = u.text if u is not None and u.status == "active" else ""
        p = parse_date(text) if text else None
        m = near.search(text) or next((x for x in anywhere.finditer(text) if x.group(1).split()[0] not in not_a_zone), None)
        ops = [h for h in (u.history if u is not None else []) if op_stage is None or op_stage.get(h)]
        out[name] = {"date": p[0] if p else None, "time": p[1] if p else None, "tz": m.group(1) if m else None,
                     "unit": uid, "as_amended_by": ops,
                     "source": ref(uid) + (f" as amended by {', '.join(ref(provision(h)) for h in ops)}" if ops else "")}
    return out


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
    for uid in list(deps):                       # a clarification on a table or form reaches its rows and fields
        par = state[uid].parent if uid in state else None
        if par in state and state[par].annotations:
            deps.append(par)
    for uid in list(deps):
        for op_id in (state[uid].annotations if uid in state else []):
            if op_provision.get(op_id):
                deps.append(op_provision[op_id])
    return sorted(set(deps))


PIN_FORMAT = 2       # 2: the image reading's review fingerprint is part of the pin (session 05)


def pin_value(state: dict[str, UState], uid: str) -> str:
    """What an interpretation is pinned to for one dependency: the unit's status, text and cells, the
    annotations on it, and, for a unit read from an image, the reading's review-subject fingerprint
    (content, uncertainties and evidence). A changed reading therefore keeps dependent interpretations
    STALE even after its new transcription is approved; the approval status itself is not pinned."""
    return unit_pin(state, uid)


# ---------------------------------------------------------------------------------------------- evaluation

class Register:
    def __init__(self, rowfile: RowFile, stages: list[StageResult], cal: Calendar | None = None,
                 policy: str = "conservative"):
        cal = cal if cal is not None else Calendar()      # a caller that needs no dates (pins, labels) may omit it
        self.rf, self.stages, self.cal, self.policy = rowfile, stages, cal, policy
        # the calendar at each stage: the configured one plus the days notified by the addenda applied so far
        self.cal_by_stage = {s.stage: cal.with_days(getattr(s, "non_working_days", [])) for s in stages}
        self.order = stage_order(stages)
        self.op_provision = {r.op.id: r.op.provision for s in stages for r in s.ops}
        self.op_stage = {r.op.id: s.stage for s in stages for r in s.ops}
        self.op_review = {r.op.id: r.op.review for s in stages for r in s.ops}
        self.op_result = {r.op.id: r for s in stages for r in s.ops}
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
        it = self.interp_at(row, s.stage)            # its `removed` decides the status (session 09)
        removal = it.removed if it is not None else None
        removal_problems: list[str] = []
        if removal is not None and prim is not None and eff is not None and eff.status == "active" \
                and prim.status != "not_issued":
            # nothing left to quote: the removal itself is checked (session 10: an unsupported removal, e.g. of words
            # that survive the op, is a problem and leaves the row in force with its status, consequence and A5 work)
            removal_problems = self._removal_problems(row, it, s)
            if removal_problems:
                removal = None
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
        elif removal is not None:                    # the obligation's words were deleted; the unit stays in force
            status = f"REMOVED ({removal.by})"
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
        unit_active = prim is not None and eff is not None and eff.status == "active" and prim.status != "not_issued"
        active = unit_active and removal is None
        out["active"] = active
        out["text"] = eff.text if eff is not None and eff.status != "not_issued" else ""
        out["cells"] = eff.cells if eff is not None else None
        out["effective_unit"] = eff.unit_id if eff is not None else None
        out["pages"] = eff.pages if eff is not None else []
        out["ops"] = hist
        out["ops_review"] = sorted({self.op_review.get(h, "?") for h in hist})
        # --- interpretation, quote, consequence
        out["interpretation_stage"] = it.stage if it else None
        problems, flags = [], []
        if it is None:
            if active:
                problems.append(f"no interpretation made at or before {s.stage}")
        elif removal is not None and unit_active:     # a supported removal: nothing left to quote (checked above)
            pass
        elif active:
            if not found(it.quote, eff.text):
                problems.append(f"quote not found in the effective text at {s.stage}: '{it.quote[:60]}'")
            if isinstance(it.consequence, Consequence):
                cu = effective(st, it.consequence.unit, True)
                if cu is None or cu.status != "active" or not found(it.consequence.quote, cu.text):
                    problems.append(f"consequence quote not found in {it.consequence.unit} at {s.stage}")
        out["interpretation"] = it.model_dump(by_alias=True, exclude={"pins"}) if it else None
        base_u = self.stages[0].state.get(row.units[0])
        out["original_text"] = base_u.text if base_u is not None else ""          # as issued (never assembled)
        out["source"] = self.source_of(row.units[0], it.quote if it else None, s, row.follows_replacement)
        out["consequence_source"] = (self.source_of(it.consequence.unit, it.consequence.quote, s)
                                     if it is not None and isinstance(it.consequence, Consequence) else None)
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
        problems += removal_problems                  # a claim the curation makes now: never explained away as STALE
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
            offset, reread = rd.offset, None
            src = effective(st, rd.source_unit, True)
            if (rd.kind == "relative" and re.search(r"\(\d+\)", rd.text) and src is not None and src.status == "active"
                    and not found(rd.text, src.text)):
                # the rule's own words are no longer in the effective text (an addendum changed the period): re-read
                # the period from the amended words of the same shape; the row is STALE and needs a person
                hits = list(_rule_shape(rd.text).finditer(normalize_latin(src.text)))
                num = re.search(r"\((\d+)\)", hits[0].group(0)) if len(hits) == 1 else None
                if num:
                    offset = int(num.group(1))
                    reread = (f"period re-read from the effective text of {rd.source_unit}: {offset} (the rule says "
                              f"{rd.offset}); needs a person")
                else:
                    reread = f"the rule's words are not in the effective text of {rd.source_unit}; no date planned"
            rule = DateRule(rule_id=rd.rule_id, kind=rd.kind, purpose=rd.purpose, anchor=rd.anchor, offset=offset,
                            unit=rd.unit, direction=rd.direction,
                            fixed=date.fromisoformat(rd.fixed) if rd.fixed else None, source_unit=rd.source_unit,
                            text=rd.text, note=rd.note)
            ins = interpretations(rule, anchors, self.cal_by_stage[s.stage])
            plan = planning_value(rule, ins, self.policy)
            if reread:
                flags.append(f"{rd.rule_id}: {reread}")
                if offset == rd.offset and reread.endswith("no date planned"):
                    plan = Interpretation(plan.key, "rule words not found", None, plan.basis)
            dates.append({"rule_id": rd.rule_id, "text": rd.text, "source_unit": rd.source_unit, "purpose": rd.purpose,
                          "reread": reread,
                          "anchor": rd.anchor, "anchor_value": anchors.get(rd.anchor).isoformat() if anchors.get(rd.anchor) else None,
                          "interpretations": [{"key": i.key, "label": i.label, "value": i.value.isoformat() if i.value else None,
                                               "basis": i.basis} for i in ins],
                          "planning": {"key": plan.key, "value": plan.value.isoformat() if plan.value else None,
                                       "policy": self.policy},
                          "readings_differ": len({i.value for i in ins}) > 1})
        out["dates"] = dates
        out["problems"], out["flags"] = problems, flags
        out["chain"] = self.chain(row, s)
        # every unit the row cites, not only the first: its text as issued, its effective text and its reference at
        # this stage (a multi-unit row, e.g. a clause with the Table 2-2 rows it relies on, keeps every value and citation)
        details = []
        for uid in row.units:
            b = self.stages[0].state.get(uid)
            e_u = effective(st, uid, row.follows_replacement)
            details.append({"unit": uid, "ref": self._ref(uid, self.stages[0].state if uid in self.stages[0].state else st),
                            "original_text": b.text if b is not None and b.status != "not_issued" else "",
                            "issued_by": b.issued_by if b is not None else None,
                            "effective_unit": e_u.unit_id if e_u is not None else None,
                            "effective_ref": self._ref(e_u.unit_id, st) if e_u is not None else "",
                            "text": e_u.text if e_u is not None and e_u.status not in ("not_issued",) else "",
                            "status": e_u.status if e_u is not None else "absent",
                            "ops": [h for h in (e_u.history if e_u is not None else []) if self.op_stage.get(h)]})
        out["units_detail"] = details
        return out

    # ------------------------------------------------------------------ provenance (latest reference)
    def _ref(self, uid: str, st: dict[str, UState]) -> str:
        u = st.get(uid) or self.stages[0].state.get(uid)
        doc, _, local = uid.partition(":")
        pages = u.pages if u is not None else []
        shown = f"{u.number} (issued as {local})" if u is not None and u.number else local
        return f"{doc} {shown}" + (f" p{','.join(map(str, pages))}" if pages else "")

    def _op_by_id(self, op_id: str):
        for s in self.stages:
            for r in s.ops:
                if r.op.id == op_id:
                    return r
        return None

    def _removal_problems(self, row: Row, it: Interp, s: StageResult) -> list[str]:
        """C16 for an interpretation that says the obligation was removed (`removed: {by: op}`): the op exists, is applied
        at or before this stage and changed one of the row's units, and the row's quote is in one of those units
        immediately before the op and absent from the same unit immediately after it (session 10). A quote still there
        after the op is not removed by it ("the row's words survive the op"): the op deleted other words of the clause."""
        by = it.removed.by
        x = self.op_result.get(by)
        if x is None:
            return [f"removed by {by}: no op of the amendment path has that id"]
        if not x.applied:
            return [f"removed by {by}: the op is not applied at {self.op_stage[by]} ("
                    + ("withheld after a person's rejection)" if x.valid else "invalid)")]
        if self.order.index(self.op_stage[by]) > self.order.index(s.stage):
            return [f"removed by {by}: the op applies at {self.op_stage[by]}, after {s.stage}"]
        mine = set(row.units) | {e.unit_id for u in row.units if (e := effective(s.state, u, row.follows_replacement))}
        hit = [u for u in x.changed if u in mine]
        if not hit:
            return [f"removed by {by}: the op changed none of the row's units ({', '.join(row.units)})"]
        around = {u: self._text_around(by, u, row.follows_replacement) for u in hit}
        had = [u for u in hit if found(it.quote, around[u][0] or "")]
        if not had:                                      # the unit's text immediately before the op
            return [f"removed by {by}: quote not found in {', '.join(hit)} as it stood before the op: '{it.quote[:60]}'"]
        if all(found(it.quote, around[u][1] or "") for u in had):
            return [f"removed by {by}: the row's words survive the op: '{it.quote[:80]}' is still in "
                    f"{', '.join(had)} immediately after it ({by} changed other words of the unit). The row stays in "
                    "force with its status, consequence and A5 activities; re-make the reading without `removed`, or "
                    "quote the words the op deleted if those were the obligation"]
        return []

    def _text_around(self, op_id: str, uid: str, follow: bool) -> tuple[str | None, str | None]:
        """The text of unit `uid` immediately before and immediately after the op `op_id` (None where the unit did not
        exist or was not in force). Before: the text the op recorded for its target, else the unit at the end of the
        previous stage. After: the text the next op on the same unit at the same stage recorded as its 'before', else
        the unit at the end of the op's stage; a unit replaced by the op is read through its replacement when the row
        follows replacements (a replacement that drops the words removes them)."""
        x = self.op_result[op_id]
        i = self.order.index(self.op_stage[op_id])
        prev, cur = self.stages[i - 1].state, self.stages[i].state
        if x.op.target == uid and x.details.get("before") is not None:
            before = x.details["before"]
        else:
            p = prev.get(uid)
            before = p.text if p is not None and p.status == "active" else None
        hist = cur[uid].history if uid in cur else []
        later = [h for h in hist[hist.index(op_id) + 1:] if self.op_stage.get(h) == self.op_stage[op_id]] \
            if op_id in hist else []
        nxt = self.op_result.get(later[0]) if later else None
        if nxt is not None and nxt.op.target == uid and nxt.details.get("before") is not None:
            return before, nxt.details["before"]
        u = effective(cur, uid, follow)
        return before, (u.text if u is not None and u.status == "active" else None)

    def source_of(self, uid: str, quote: str | None, s: StageResult, follow: bool = True) -> dict:
        out = self._source_of(uid, quote, s, follow)
        num = s.state[uid].number if uid in s.state else None
        if num:                                       # renumbered: cite the number in force, with the issued one
            doc, _, local = uid.partition(":")
            out["latest"] = out["latest"].replace(f"{doc} {local}", f"{doc} {num} (issued as {local})", 1)
        return out

    def _source_of(self, uid: str, quote: str | None, s: StageResult, follow: bool = True) -> dict:
        """Where the words of `quote` in a unit's effective text come from at stage `s`: the unit as issued,
        or the addendum provision (with its page) that supplied them. `latest` is the reference to cite for
        the point; `refs` lists every document involved, oldest first."""
        st = s.state
        eff = effective(st, uid, follow)
        if eff is None:
            return {"latest": self._ref(uid, st), "refs": [self._ref(uid, st)], "from_amendment": False}
        base = self.stages[0].state.get(eff.unit_id)
        refs = [self._ref(uid, self.stages[0].state if uid in self.stages[0].state else st)]
        if eff.unit_id != uid:                                   # replaced: the replacement is the source
            by = next((h for h in eff.history if self.op_stage.get(h)), None)
            latest = f"{self._ref(eff.unit_id, st)} (replacing {refs[0]}" + (f", {by}" if by else "") + ")"
            return {"latest": latest, "refs": refs + [self._ref(eff.unit_id, st)], "from_amendment": True}
        hist = [self._op_by_id(h) for h in eff.history]
        hist = [h for h in hist if h is not None]
        in_original = base is not None and base.status != "not_issued" and quote is not None and found(quote, base.text)
        supplied = []
        for h in hist:
            words = " ".join(x for x in (h.op.new, h.op.new_text) if x)
            if quote and words and (found(words, quote) or found(quote, words)):
                supplied.append(h)
        if not supplied and not in_original and hist:
            supplied = [hist[-1]]
        if base is not None and base.status == "not_issued" and not hist:   # an addendum's own unit
            return {"latest": self._ref(uid, st), "refs": refs, "from_amendment": False}
        if supplied:
            h = supplied[-1]
            prov = self._ref(h.op.provision, st)
            words = " ".join(x for x in (h.op.new, h.op.new_text) if x)
            if quote and words and not found(quote, words):      # original words with amended words inside them
                latest = f"{refs[0]} as amended by {', '.join(self._ref(x.op.provision, st) for x in supplied)}"
                return {"latest": latest, "refs": refs + [self._ref(x.op.provision, st) for x in supplied],
                        "from_amendment": True, "ops": [x.op.id for x in supplied]}
            verb = {"set_status": "reinstating" if h.op.status == "reinstated" else "changing"}.get(h.op.type, "amending")
            latest = f"{prov} ({verb} {refs[0].rsplit(' p', 1)[0]})"
            return {"latest": latest, "refs": refs + [self._ref(x.op.provision, st) for x in supplied],
                    "from_amendment": True, "ops": [x.op.id for x in supplied]}
        latest = refs[0] + (f" as amended by {', '.join(self._ref(h.op.provision, st) for h in hist)}" if hist else "")
        return {"latest": latest, "refs": refs + [self._ref(h.op.provision, st) for h in hist], "from_amendment": False}

    def _op_type(self, op_id: str):
        for s in self.stages:
            for r in s.ops:
                if r.op.id == op_id:
                    return (r.op.type, r.op.status)
        return (None, None)

    def chain(self, row: Row, s: StageResult) -> list[str]:
        """Evidence chain: every unit the row cites, as issued (document, page, origin), then each op that changed any of
        them (or its replacement) up to this stage, with the stage, its provision and page."""
        st = s.state
        base = self.stages[0].state
        out, hist = [], []
        for uid in row.units:
            u0 = base.get(uid) or st.get(uid)
            if u0 is not None:
                out.append(f"{uid} ({u0.doc} p{','.join(map(str, u0.pages))}; {u0.origin.replace('_', ' ')}"
                           + (f"; issued by {u0.issued_by}" if u0.issued_by else "") + ")")
            eff = effective(st, uid, row.follows_replacement)
            for k in [uid] + ([eff.unit_id] if eff is not None and eff.unit_id != uid else []):
                hist += [h for h in (st[k].history if k in st else []) if h not in hist]
        hist.sort(key=lambda h: self.order.index(self.op_stage.get(h, BASE)))   # in addendum order (stable within one)
        for h in hist:
            prov = self.op_provision.get(h)
            pu = st.get(prov)
            out.append(f"{h} [{self.op_stage.get(h)}; {self.op_review.get(h)}] <- {prov} ({pu.doc} p{','.join(map(str, pu.pages))})"
                       if pu else h)
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


def _pin_value_v1(state: dict[str, UState], uid: str) -> str:
    u = state.get(uid)
    return "absent" if u is None else sha256_text(u.sha() + "|" + ",".join(sorted(u.annotations)))[:16]


def migrate_pins(rowfile: RowFile, stages: list[StageResult]) -> tuple[int, list[str]]:
    """Format 1 -> 2: upgrade a pin only where every dependency still has the value it was pinned to under
    format 1 (nothing changed since pinning); anything else is left as it is and stays STALE for a person.
    The fingerprint added in format 2 is taken from the current reading, so run this only when the
    readings have not changed since the pins were made (recorded in the work log)."""
    by_stage = {s.stage: s for s in stages}
    reg = Register(rowfile, stages, Calendar())
    n, kept = 0, []
    for row in rowfile.rows:
        for it in row.interpretations:
            if not it.pins or it.stage not in by_stage:
                continue
            st = by_stage[it.stage].state
            now = reg.pins_for(row, it, by_stage[it.stage])
            if set(now) == set(it.pins) and all(_pin_value_v1(st, d) == v for d, v in it.pins.items()):
                if now != it.pins:
                    it.pins = now
                    n += 1
            else:
                kept.append(f"{row.id}@{it.stage}")
    return n, kept


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
