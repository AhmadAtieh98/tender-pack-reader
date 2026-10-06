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

Where a row comes into force (session 11). By default, from the stage its primary unit (units[0]) is issued in: BASE
for a volume unit, the addendum for an addendum's own unit or a unit an op inserted (reported as DERIVED). A row whose
obligation an addendum creates in a unit that existed before (blind rehearsal 04: a new row citing VOL-V 18.1, issued
in BASE, read at ADD-03 only) states it: `introduced: {stage, by: <op id or provision unit>, evidence: {unit, page,
words}}`. Before that stage the row is NOT IN FORCE (no reading demanded, never STALE, off A3 and A5); at it, NEW
(introduced by <by>); from it, the usual checks. The claim is checked (the op is applied at that stage or the provision
is that addendum's; the words are printed there, new at that stage, in the introducing provision, a unit its op changed
or names, or a unit of the row; no reading made before it); an unsupported claim is a problem (C16) and the row is read
as if it had no field. Putting an addendum's provision first in `units` remains a convention, never the evidence.

Separate statuses, never merged:
  status            what the documents say at that stage (NOT IN FORCE / ACTIVE / AMENDED / REMOVED / DELETED / ...)
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

from .amend import BASE, StageResult, UState, inserted_ref, unit_pin
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


class Quotation(_Strict):
    """Words printed in one unit, on one page: {unit, page, words}."""
    unit: str
    page: int
    words: str


class Introduction(_Strict):
    """Where a row's obligation comes into force (session 11): the `stage`, what introduces it there (`by`: an op of
    that stage, or a provision of that stage's addendum) and the words printed there that say so (`evidence`). Before
    that stage the row is NOT IN FORCE (no reading is demanded, it is never STALE and stays off A3 and A5); from it the
    usual checks apply. The claim is checked (Register._introduction_problems); an unsupported one is a problem (C16) and
    never takes the row out of force: the row is then read as a row without the field."""
    stage: str
    by: str
    evidence: Quotation
    note: str = ""


class Corroboration(_Strict):
    """This row's consequence restates the consequence of another row (session 11, audit A3-6): A3 lists the trigger
    once, on `row`, with this row and the places in `also` as corroborating sources, and says what `adds` adds. `also` and
    `adds_evidence` are printed words ({unit, page, words}); each must be found in its unit's effective text, otherwise
    the row is not folded and is flagged (stage2.a3). Proposed content, like the row."""
    row: str
    also: list[Quotation] = Field(default_factory=list)
    adds: str = ""
    adds_evidence: list[Quotation] = Field(default_factory=list)


class ConditionalOn(_Strict):
    """Session 12 (W3b; blind-05 follow-up 6): the row (or activity) was proposed from an image reading that no person has
    approved. While the reading is pending the row is not in force (status derived.PENDING_STATUS naming the reading:
    shown in A1, off A3 and A5); once the reading is approved it is an ordinary row. `subject_sha256` pins the reading's
    review subject the proposal was made from (written by the validator): a reading changed since is a problem (C16)."""
    reading: str                                 # the reading's region id (curation/readings/<region>.yaml)
    until: Literal["approval"] = "approval"
    subject_sha256: str | None = None


class DerivedConsequence(_Strict):
    """Session 12 (W3b; blind-05 follow-up 9): the row's bid-out consequence is quoted from an EXISTING rule (another
    row's consequence, same unit and class), read with a value or a band the addendum states. `owner: person` when
    whether the rule covers the value is a judgment (HUMAN DECISION PENDING); `deterministic` when the rule's own words
    name the value. Written by the validator; a proposal, like the row."""
    rule: str                                    # the existing row whose consequence is quoted
    unit: str
    owner: Literal["person", "deterministic"]
    basis: str = ""


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
    # session 11: where the obligation comes into force, with evidence. A row without it is in force from the stage its
    # primary unit is issued in (BASE for a volume unit), as before; the register reports that as derived.
    introduced: Introduction | None = None
    corroborates: Corroboration | None = None    # session 11 (A3-6): restates another row's consequence
    conditional_on: ConditionalOn | None = None  # session 12 (W3b): proposed from a reading pending approval
    derived_consequence: DerivedConsequence | None = None   # session 12 (W3b): the consequence of an existing rule
    review: Literal["proposed", "accepted"] = "proposed"
    reviewer: str | None = None

    @model_serializer(mode="wrap")
    def _without_unset_introduction(self, handler):
        # a row without `introduced` dumps exactly as before the field existed, so what a review decision on a row is
        # bound to (review.row_binding) does not change for rows that do not use it
        d = handler(self)
        if self.introduced is None:
            d.pop("introduced", None)
        if self.corroborates is None:                # likewise for `corroborates` (session 11)
            d.pop("corroborates", None)
        for k in ("conditional_on", "derived_consequence"):   # and the session-12 fields
            if getattr(self, k) is None:
                d.pop(k, None)
        return d

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


PIN_FORMAT = 3       # 2: the image reading's review fingerprint is part of the pin (session 05)
#                      3: an annotation whose effect is `confirms` is not (session 12, blind-06 follow-up 9)


def pin_value(state: dict[str, UState], uid: str, confirming=frozenset()) -> str:
    """What an interpretation is pinned to for one dependency: the unit's status, text and cells, the
    annotations on it, and, for a unit read from an image, the reading's review-subject fingerprint
    (content, uncertainties and evidence). A changed reading therefore keeps dependent interpretations
    STALE even after its new transcription is approved; the approval status itself is not pinned.
    `confirming` (Register.confirming: the ids of the annotate ops whose effect is `confirms`) are left out: a
    confirmation changes nothing, so it never makes a reading STALE nor appears among the ops that changed a
    dependency (session 12, pin format 3). The confirming provision itself stays a dependency (dependencies())."""
    return unit_pin(state, uid, ignore=confirming)


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
        # session 12 (blind-06 follow-up 9): the annotations that confirm a unit unchanged are not part of its pin
        self.confirming = frozenset(r.op.id for s in stages for r in s.ops
                                    if r.op.type == "annotate" and r.op.effect == "confirms")
        self.issued = {s.stage: s.issued for s in stages}
        # session 11 audit (A1-2): every list item an applied insert_unit op put into a volume unit: a row whose primary
        # unit is the list the item is inserted into is AMENDED by that op at its stage
        self.insertions = []
        for s in stages:
            for x in s.ops:
                nid = f"{x.op.anchor}+{s.stage}" if x.op.type == "insert_unit" and x.op.anchor else None
                if x.applied and nid in s.state:
                    self.insertions.append({"op": x.op.id, "stage": s.stage, "unit": nid, "anchor": x.op.anchor,
                                            "parent": s.state[nid].parent})

    def inserted_into(self, row: Row, stage: str) -> list[dict]:
        """The insertions (op, stage, unit, anchor, parent) made at or before `stage` into the row's primary unit: an
        item inserted in the list the row's first unit is (ADD-02 7.1: Form 4-G after VOL-I 9.1(e) amends the Envelope A
        list VOL-I-9.1-01). Inserting after an item does not amend that item's own row."""
        i = self.order.index(stage)
        return [x for x in self.insertions if x["parent"] and x["parent"] == row.units[0]
                and self.order.index(x["stage"]) <= i]

    def unchanged_by(self, row: Row, op_id: str) -> str | None:
        """Session 11 audit (A1-8): how an op that changed one of the row's units left the row's OWN words, or None when
        it changed them. 'reissued': every unit the row cites reads exactly the same (text and cells) after the op's stage
        as before it (a reissued table whose row is printed again unchanged: Table 1-1 A, C, E, F). 'elsewhere': a text op
        changed other words of the unit, and the row's reading was RE-MADE at the op's stage with the same quote and
        consequence (a person read the row against the amended unit); the quote is in the unit before and after and no
        word the op wrote or struck is in the sentence that holds it; its date rules are unaffected (VOL-II 4.4: 72 -> 96
        hours; the N+1 sentence untouched). A row not re-read there is not 'unchanged': words elsewhere in a clause can
        change what its quote means ('All other utilities ...' once the grid connection is struck), so it stays AMENDED
        (and STALE until a person re-reads it). Insertions, deletions, reinstatements and figure changes in the row's
        words are changes (None)."""
        x = self.op_result.get(op_id)
        if x is None or not x.applied or x.op.type not in ("replace_unit", "replace_text", "append_text", "set_value"):
            return None
        i = self.order.index(self.op_stage[op_id])
        if i == 0:
            return None
        prev, cur = self.stages[i - 1], self.stages[i]

        def reads(st, uid):
            u = effective(st, uid, row.follows_replacement)
            return None if u is None else (u.status, u.text, u.cells)
        if all(reads(prev.state, k) == reads(cur.state, k) for k in row.units):
            return "reissued"
        if x.op.type == "replace_unit":
            return None
        a, b = self.interp_at(row, prev.stage), self.interp_at(row, cur.stage)
        if a is None or b is None or b.stage != cur.stage or a.quote != b.quote or a.consequence != b.consequence \
                or a.removed or b.removed:
            return None                               # (only a reading re-made at the op's stage can say so)
        texts = lambda st: [u.text for k in row.units if (u := effective(st, k, row.follows_replacement)) is not None  # noqa: E731
                            and u.status == "active"]
        if not any(found(b.quote, t) for t in texts(prev.state)) or not any(found(b.quote, t) for t in texts(cur.state)):
            return None
        new, old = (x.op.new or "").strip(), (x.op.old or "").strip() if x.op.type == "replace_text" else ""
        if not new and not old:
            return None
        for st, words in ((cur.state, new), (prev.state, old)):   # the words written after, the words struck before
            for t in (texts(st) if words else []):
                for sent in re.split(r"(?<=[.;])\s+", t):
                    if found(b.quote, sent) and (found(words, sent) or found(sent, words)):
                        return None
        for rd in row.date_rules:
            src = effective(cur.state, rd.source_unit, True)
            if src is not None and src.status == "active" and not found(rd.text, src.text) and \
                    rd.kind == "relative" and re.search(r"\(\d+\)", rd.text):
                return None
        return "elsewhere"

    def _unchanged_words(self, ops: list[str], row: Row) -> str:
        re_, el = [h for h in ops if self.unchanged_by(row, h) == "reissued"], [h for h in ops
                                                                                if self.unchanged_by(row, h) != "reissued"]
        return "; ".join(([f"reissued by {', '.join(re_)}, unchanged"] if re_ else [])
                         + ([f"unit amended by {', '.join(el)}; the row's words unchanged"] if el else []))

    def interp_at(self, row: Row, stage: str) -> Interp | None:
        idx = self.order.index(stage)
        cands = [i for i in row.interpretations if i.stage in self.order and self.order.index(i.stage) <= idx]
        return cands[-1] if cands else None

    def _legacy_pin_holds(self, it: Interp, d: str, now: str) -> bool:
        """Session 12 (pin format 3): a pin written under format 2 (every annotation hashed, confirming ones included)
        still holds when it is the format-2 value of the dependency at the interpretation's own stage and the format-3
        value there equals the value now: nothing but a confirmation lies between. A pack whose pins.yaml predates
        format 3 (a rehearsal, a candidate) is therefore read right without re-pinning; anything else stays STALE."""
        xs = next((s for s in self.stages if s.stage == it.stage), None)
        return xs is not None and it.pins.get(d) == unit_pin(xs.state, d) and \
            pin_value(xs.state, d, self.confirming) == now

    def pins_for(self, row: Row, interp: Interp, stage: StageResult) -> dict[str, str]:
        deps = dependencies(row, interp, stage.state, self.rf.anchors, self.op_provision)
        return {d: pin_value(stage.state, d, self.confirming) for d in deps}

    # ------------------------------------------------------------------ introduction (session 11)
    def introduction(self, row: Row) -> dict:
        """Where the row comes into force and on what basis: {stage, by, explicit, basis, problems, claimed}.
        `explicit` when the row carries `introduced` and the claim is supported (problems empty): the row is NOT IN FORCE
        before that stage. Otherwise the stage is DERIVED, as it always was, from the row's primary unit: the first stage
        at which it exists and is issued (BASE for a volume unit, the addendum for an addendum's own unit or a unit an op
        inserted). `problems` are those of an `introduced` claim (reported as C16 at the claimed stage); `claimed` is the
        claimed stage (None without the field)."""
        uid = row.units[0]
        first = next((s for s in self.stages if (u := s.state.get(uid)) is not None and u.status != "not_issued"), None)
        if first is None:
            derived = {"stage": None, "by": None, "basis": f"derived from the primary unit {uid}, which no stage issues"}
        else:
            u = first.state[uid]
            by = (u.history[0] if u.origin == "addendum_op" and u.history else u.issued_by or (BASE if first.stage == BASE
                                                                                                else None))
            how = ("issued in BASE" if first.stage == BASE else f"inserted by {by}" if u.origin == "addendum_op"
                   else f"issued by {first.stage}")
            derived = {"stage": first.stage, "by": by, "basis": f"derived from the primary unit {uid} ({how})"}
        ii = row.introduced
        if ii is None:
            return {**derived, "explicit": False, "problems": [], "claimed": None}
        problems = self._introduction_problems(row, ii)
        if problems:
            return {**derived, "explicit": False, "problems": problems, "claimed": ii.stage,
                    "basis": derived["basis"] + f"; the `introduced` claim ({ii.stage} by {ii.by}) is not supported"}
        return {"stage": ii.stage, "by": ii.by, "explicit": True, "problems": [], "claimed": ii.stage,
                "basis": f"introduced at {ii.stage} by {ii.by}: '{ii.evidence.words[:80]}' ({ii.evidence.unit} "
                         f"p{ii.evidence.page})"}

    def _introduction_problems(self, row: Row, ii: Introduction) -> list[str]:
        """C16 for `introduced: {stage, by, evidence}`: the stage is a stage of the pack; `by` is an op applied at that
        stage, or a provision of that stage's addendum in force there (a unit of a volume for BASE); the evidence words
        are printed, at that stage, in the unit and on the page given, are new there (not in the same unit at the stage
        before), and come from the introducing provision, a unit its op changed or names, or a unit of the row; and no
        interpretation of the row is made before that stage."""
        if ii.stage not in self.order:
            return [f"introduced at {ii.stage}, which is not a stage of this pack ({', '.join(self.order)})"]
        i = self.order.index(ii.stage)
        s = self.stages[i]
        st = s.state
        out: list[str] = []
        related = set(row.units) | {e.unit_id for u in row.units if (e := effective(st, u, row.follows_replacement))}
        x = self.op_result.get(ii.by)
        if x is not None:
            if self.op_stage[ii.by] != ii.stage:
                out.append(f"introduced by {ii.by}: the op applies at {self.op_stage[ii.by]}, not {ii.stage}")
            elif getattr(x, "conditional_pending", False):
                out.append(f"introduced by {ii.by}: the op is a conditional amendment held at {ii.stage} (no person has "
                           "recorded that its trigger occurred): the row is not in force from it until a trigger fact is "
                           "recorded")
            elif not x.applied:
                out.append(f"introduced by {ii.by}: the op is not applied at {ii.stage} ("
                           + ("withheld after a person's rejection)" if x.valid else "invalid)"))
            related |= {x.op.provision, *x.changed, *x.op.targets, *(x.details.get("content") or [])} | \
                {k for k in (x.op.target, x.op.anchor, x.op.replacement, x.op.new_group, x.op.new_text_from) if k}
        elif ii.by in st:
            u = st[ii.by]
            own = (u.issued_by is None and not u.doc.startswith("ADD-")) if ii.stage == BASE else u.doc == ii.stage
            if not own or u.status != "active":
                out.append(f"introduced by {ii.by}: not a provision of {ii.stage} in force there" if ii.stage != BASE
                           else f"introduced by {ii.by}: not a unit of the documents as issued")
            related.add(ii.by)
        else:
            out.append(f"introduced by {ii.by}: no op of the amendment path and no unit of the pack has that id")
        ev = ii.evidence
        u = effective(st, ev.unit, True)
        if u is None or u.status != "active":
            out.append(f"introduction evidence: {ev.unit} is not in force at {ii.stage}")
        else:
            if ev.page not in (u.pages or []):
                out.append(f"introduction evidence: {ev.unit} is on page(s) {u.pages}, not page {ev.page}")
            if not (ev.words or "").strip() or not found(ev.words, u.text):
                out.append(f"introduction evidence: the words are not in {ev.unit} at {ii.stage}: '{ev.words[:60]}'")
            elif i > 0:
                p = effective(self.stages[i - 1].state, ev.unit, True)
                if p is not None and p.status == "active" and found(ev.words, p.text):
                    out.append(f"introduction evidence: '{ev.words[:60]}' is already in {ev.unit} at "
                               f"{self.order[i - 1]}: it does not show what {ii.stage} introduces")
            if ev.unit not in related and u.unit_id not in related:
                out.append(f"introduction evidence: {ev.unit} is neither the introducing provision, a unit its op "
                           "changed or names, nor a unit of the row")
        early = [it.stage for it in row.interpretations if it.stage in self.order and self.order.index(it.stage) < i]
        if early:
            out.append(f"interpretation(s) made at {', '.join(early)}, before the row's introduction at {ii.stage}")
        return out

    def evaluate(self, row: Row, s: StageResult) -> dict:
        st = s.state
        prim = st.get(row.units[0])
        eff = effective(st, row.units[0], row.follows_replacement)
        out = {"stage": s.stage, "stage_status": s.status}
        intro = self.introduction(row)               # session 11: explicit (`introduced`, supported) or derived
        pre = intro["explicit"] and self.order.index(s.stage) < self.order.index(intro["stage"])
        out["introduction"] = {k: intro[k] for k in ("stage", "by", "explicit", "basis")}
        it = None if pre else self.interp_at(row, s.stage)    # its `removed` decides the status (session 09)
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
        inserted = [] if pre else self.inserted_into(row, s.stage)     # session 11 audit (A1-2)
        hist += [x["op"] for x in inserted if x["op"] not in hist]
        here = [h for h in hist if self.op_stage.get(h) == s.stage]
        earlier = [h for h in hist if h not in here and self.order.index(self.op_stage.get(h, BASE)) < self.order.index(s.stage)]
        introduced_here = intro["explicit"] and intro["stage"] == s.stage
        if pre:                                      # session 11: the obligation is not yet in force (`introduced`)
            status = f"NOT IN FORCE (introduced at {intro['stage']} by {intro['by']})"
        elif prim is None or prim.status == "not_issued":
            status = "NOT ISSUED"
        elif eff.status == "deleted":
            status = f"DELETED ({', '.join(here or earlier)})" if here else f"DELETED (by {', '.join(earlier)})"
        elif eff.status == "revoked":
            status = f"REVOKED ({', '.join(here or earlier)})"
        elif eff.status == "superseded":
            status = f"REPLACED (by {eff.superseded_by})"
        elif removal is not None:                    # the obligation's words were deleted; the unit stays in force
            status = f"REMOVED ({removal.by})"
        elif introduced_here:
            status = f"NEW (introduced by {intro['by']})"
        elif prim.issued_by == s.stage or (eff.origin == "addendum_op" and here and eff.issued_by in (None, s.stage)):
            # (session 11: a unit an op inserted is NEW at the stage that inserted it; a later addendum amends it)
            status = "NEW"
        elif here and all(self.unchanged_by(row, h) for h in here):
            # session 11 audit (A1-8): reissued or amended elsewhere in the unit; the row's own words are unchanged
            changed_before = [h for h in earlier if not self.unchanged_by(row, h)]
            status = "ACTIVE (" + (f"as amended by {', '.join(changed_before)}; " if changed_before else "") + \
                self._unchanged_words(here, row) + ")"
        elif here:
            reinstated = any(self._op_type(h) == ("set_status", "reinstated") for h in here)
            status = ("REINSTATED-AMENDED" if reinstated else "AMENDED") + f" ({', '.join(here)})"
        elif earlier:
            changed_before = [h for h in earlier if not self.unchanged_by(row, h)]
            same = [h for h in earlier if h not in changed_before]
            status = "ACTIVE (" + "; ".join(([f"as amended by {', '.join(changed_before)}"] if changed_before else [])
                                            + ([self._unchanged_words(same, row)] if same else [])) + ")"
        else:
            status = "ACTIVE"
        out["status"] = status
        unit_active = prim is not None and eff is not None and eff.status == "active" and prim.status != "not_issued"
        active = unit_active and removal is None and not pre
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
                    conf = sorted(h for u in (st.values() if d in self.op_provision.values() else [])
                                  for h in u.annotations if h in self.confirming and self.op_provision.get(h) == d
                                  and self.order.index(self.op_stage.get(h, BASE)) > self.order.index(it.stage))
                    stale.append(f"new dependency {d}" + (f" (the provision of {', '.join(conf)}, which confirms a "
                                                          "unit of the row unchanged)" if conf else ""))
                elif it.pins[d] != v and not self._legacy_pin_holds(it, d, v):
                    by = [h for h in (st[d].history + st[d].annotations if d in st else [])
                          if self.order.index(self.op_stage.get(h, BASE)) > self.order.index(it.stage)
                          and h not in self.confirming]           # session 12: a confirmation changes nothing
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
        if intro["problems"] and (intro["claimed"] == s.stage or (intro["claimed"] not in self.order
                                                                  and s.stage == self.order[0])):
            problems += intro["problems"]            # session 11: an unsupported `introduced` claim (C16)
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
        flags += self._precedence_flags(rel, s)              # session 12: two renderings issued together
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
                            "original_text": self.as_issued_text(uid),
                            "issued_by": b.issued_by if b is not None else None,
                            "effective_unit": e_u.unit_id if e_u is not None else None,
                            "effective_ref": self._ref(e_u.unit_id, st) if e_u is not None else "",
                            "text": e_u.text if e_u is not None and e_u.status not in ("not_issued",) else "",
                            "status": e_u.status if e_u is not None else "absent",
                            "ops": [h for h in (e_u.history if e_u is not None else []) if self.op_stage.get(h)]})
        for x in inserted:                            # session 11 audit (A1-2): each inserted item in its position
            u = st.get(x["unit"])
            if u is None:
                continue
            d = {"unit": x["unit"], "ref": self._ref(x["unit"], st), "original_text": self.as_issued_text(x["unit"]),
                 "issued_by": u.issued_by,
                 "effective_unit": x["unit"], "effective_ref": self._ref(x["unit"], st),
                 "text": u.text if u.status != "not_issued" else "", "status": u.status,
                 "ops": [h for h in u.history if self.op_stage.get(h)]}
            at = [j for j, dd in enumerate(details) if dd["unit"] == x["anchor"]]
            details.insert(at[0] + 1 if at else len(details), d)
        out["units_detail"] = details
        self._conditional_and_effective(row, s, out, anchors)     # session 11 (D3): conditional / effective-dated state
        self._derived_state(row, s, out, rel)                      # session 12 (W3b): pending reading; switched conditions
        return out

    def _derived_state(self, row: Row, s: StageResult, out: dict, rel: list) -> None:
        """Session 12 (W3b; tenderpack.derived). A row `conditional_on` a reading still pending (or changed since the
        proposal) is not in force: its status names the reading and `active` is False (A3 and A5 leave it out); after a
        person's approval it is ordinary. A row whose unit's condition, or a defined term its units use, an op of this
        stage changed is flagged for a re-read (nothing decided; the status is unchanged)."""
        from . import derived
        from .schedule import in_force
        co = row.conditional_on
        if co is not None:
            mine = [u for u in rel if u is not None and u.origin == "image_reading" and u.reading_region == co.reading]
            if not mine:
                out["problems"].append(f"conditional_on: the row cites no unit of reading {co.reading} at {s.stage}")
            else:
                pend = [u.unit_id for u in mine if u.reading_status != "approved"]
                if co.subject_sha256 and all(u.reading_subject != co.subject_sha256 for u in mine):
                    out["problems"].append(f"conditional_on: reading {co.reading} changed since the row was proposed from "
                                           f"it (review subject {co.subject_sha256[:12]}… now {str(mine[0].reading_subject)[:12]}…): "
                                           "re-read the row against the reading")
                    pend = pend or [mine[0].unit_id]
                if pend:
                    if in_force(out["status"]):
                        out["status"], out["active"] = derived.pending_status(co.reading), False
                    out["flags"].append(f"{derived.label(co.reading)} (pending): proposed from the reading, not in force")
                else:
                    out["flags"].append(f"conditional_on reading {co.reading}: approved, the condition is met (an "
                                        "ordinary row now)")
        cache = self.__dict__.setdefault("_switched", {})
        if s.stage not in cache:
            cache[s.stage] = derived.switched_in(self.stages, s.stage) if s.stage in self.order else []
        if cache[s.stage] and out.get("active"):
            out["flags"] += [f for f in derived.row_flags(cache[s.stage], row, s.state) if f not in out["flags"]]

    def _precedence_flags(self, rel: list, s: StageResult) -> list[str]:
        """Session 12: a row that relies on one of two renderings issued together (an annotate op's `precedence`, at this
        stage or before): flagged for a person when the addendum does not say which governs, and when the row relies on
        the rendering the addendum's words say does not govern. Nothing is decided here."""
        upto = self.order[: self.order.index(s.stage) + 1] if s.stage in self.order else [s.stage]
        out = []
        for x in (x for st_ in self.stages if st_.stage in upto for x in st_.ops):
            pr = x.details.get("precedence") if x.applied else None
            if not pr:
                continue

            def under(uid: str, t: str) -> bool:
                return uid == t or uid.startswith(t + "/")
            uids = [u.unit_id for u in rel if u is not None]
            if pr["governs"] == "unstated":
                hit = [u for u in uids if any(under(u, t) for t in pr["over"])]
                if hit:
                    out.append(f"relies on {', '.join(hit)}, one of renderings issued together ({', '.join(pr['over'])}); "
                               f"{x.op.provision} does not say which governs (precedence unstated, {x.op.id}): a person "
                               "decides")
            else:
                hit = [u for u in uids if any(under(u, t) for t in pr["over"])]
                if hit:
                    out.append(f"relies on {', '.join(hit)}, a rendering that does not govern: '{pr['words']}' "
                               f"({pr['stated_by']}, {x.op.id}); {pr['governs']} governs")
        return out

    # ------------------------------------------------------------------ conditional and effective-dated state (s11)
    def _conditional_and_effective(self, row: Row, s: StageResult, out: dict, anchors: dict) -> None:
        """Session 11. A conditional amendment (amend.Condition) that is pending at this stage and would change one of
        the row's units (or names the row or a unit in `affects`): the row is CONDITIONAL, never AMENDED: `status`
        becomes 'CONDITIONAL (<op>: not in effect unless <trigger>; in force: <status as computed>)' while the row is
        in force, and `conditional` lists both states ({op, condition, trigger, trigger_unit, applicability, state,
        stated_at, deadline {rule_id, text, value, readings}, state_if_not_triggered, state_if_triggered, fact}); the
        trigger's deadline is added to `dates` as a deadline rule (`conditional: {condition, op}`, so A5 plans a
        decision milestone). A condition a person recorded as not triggered, or as triggered (the op then applies as
        any other), is a flag. An op with an effective date is listed in `effective` ({op, effective_from, effective:
        retroactive | deferred | on issue}) and flagged; a change that flowed through an earlier addendum's amending
        text says so in `chain`. Nothing here assumes a trigger occurred."""
        mine = set(row.units) | {e.unit_id for u in row.units if (e := effective(s.state, u, row.follows_replacement))}
        conds = []
        for c in getattr(s, "conditions", None) or []:
            if not c.get("valid", True) or c.get("state") == "invalid":
                continue
            hit = sorted(mine & set(c.get("targets") or []))
            named = sorted((mine | {row.id}) & set(c.get("affects") or []))
            if not hit and not named:
                continue
            conds.append((c, hit, named))
        lines = []
        for c, hit, named in conds:
            dl = c.get("deadline")
            dentry = None
            if dl:
                rid = "TRIGGER-" + re.sub(r"[^A-Za-z0-9]+", "-", str(c["condition"])).strip("-").upper()
                rule = DateRule(rule_id=rid, kind=dl.get("kind", "relative"), purpose="deadline", anchor=dl.get("anchor"),
                                offset=int(dl.get("offset") or 0), unit=dl.get("unit", "calendar_day"),
                                direction=dl.get("direction", "after"),
                                fixed=date.fromisoformat(dl["fixed"]) if dl.get("fixed") else None,
                                source_unit=c.get("trigger_unit") or "", text=dl.get("text") or "")
                ins = interpretations(rule, anchors, self.cal_by_stage[s.stage])
                plan = planning_value(rule, ins, self.policy)
                dentry = {"rule_id": rid, "text": rule.text, "source_unit": rule.source_unit, "purpose": "deadline",
                          "reread": None, "anchor": rule.anchor,
                          "anchor_value": anchors.get(rule.anchor).isoformat() if anchors.get(rule.anchor) else None,
                          "interpretations": [{"key": i.key, "label": i.label, "value": i.value.isoformat() if i.value
                                               else None, "basis": i.basis} for i in ins],
                          "planning": {"key": plan.key, "value": plan.value.isoformat() if plan.value else None,
                                       "policy": self.policy},
                          "readings_differ": len({i.value for i in ins}) > 1,
                          "conditional": {"condition": c["condition"], "op": c["op"], "trigger": c.get("trigger"),
                                          "trigger_unit": c.get("trigger_unit"), "state": c.get("state")}}
            u0 = hit[0] if hit else None
            states = c.get("if_triggered") or {}
            rec = {"op": c["op"], "condition": c["condition"], "stated_at": c.get("stated_at"),
                   "trigger": c.get("trigger"), "trigger_unit": c.get("trigger_unit"),
                   "applicability": c.get("applicability"), "if_not_triggered": c.get("if_not_triggered"),
                   "state": c.get("state"), "fact": c.get("fact"), "units": hit, "named_in_affects": named,
                   "deadline": ({"rule_id": dentry["rule_id"], "text": dentry["text"],
                                 "value": dentry["planning"]["value"], "readings": dentry["interpretations"]}
                                if dentry else None),
                   "state_if_not_triggered": {u: (s.state[u].text if u in s.state else None) for u in hit},
                   "state_if_triggered": {u: (states.get(u) or {}).get("after") for u in hit}}
            out.setdefault("conditional", []).append(rec)
            short = " ".join(str(c.get("trigger") or "").split())[:140]
            if c.get("state") == "pending":
                if dentry and out.get("active"):
                    out["dates"].append(dentry)
                lines.append(f"{c['op']}: not in effect unless {short}"
                             + (f"; decide by {dentry['planning']['value']} ({dentry['rule_id']})"
                                if dentry and dentry["planning"]["value"] else ""))
                out["flags"].append(f"CONDITIONAL: {c['op']} ({c['condition']}, {c.get('trigger_unit')}) would change "
                                    f"{', '.join(hit) or ', '.join(named)} only if {short}; both states are kept, "
                                    "nothing assumes the trigger occurred"
                                    + (f"; the trigger's deadline is {dentry['planning']['value']}" if dentry and
                                       dentry["planning"]["value"] else ""))
            elif c.get("state") == "not_triggered":
                f = c.get("fact") or {}
                out["flags"].append(f"conditional {c['op']} ({c['condition']}) not triggered: recorded by "
                                    f"{f.get('recorded_by')} on {f.get('date')}; the unit stands as it is")
        if lines and out.get("active") and not str(out["status"]).startswith(("NOT ", "DELETED", "REVOKED", "REPLACED",
                                                                                "REMOVED")):
            out["status"] = f"CONDITIONAL ({'; '.join(lines)}; in force: {out['status']})"
        # effective dates and changes that flowed through an earlier addendum's amending text
        eff, flowed = [], {}
        for h in out.get("ops") or []:
            x = self.op_result.get(h)
            if x is None or not x.applied:
                continue
            if x.details.get("effective_from"):
                eff.append({"op": h, "effective_from": x.details["effective_from"],
                            "effective": x.details.get("effective") or ("on the trigger" if x.details.get("conditional")
                                                                        else "")})
            for fl in x.details.get("flowed") or []:
                if fl["unit"] in mine:
                    flowed[h] = fl
            cd = x.details.get("conditional") or {}
            if cd.get("state") == "triggered":
                f = cd.get("fact") or {}
                out["flags"].append(f"{h} applies on its trigger ({cd.get('condition')}): recorded by "
                                    f"{f.get('recorded_by')} as occurred on {f.get('date')}")
        if eff:
            out["effective"] = eff
            out["flags"] += [f"{e['op']}: effective from {e['effective_from']}"
                             + (f" ({e['effective']}" + (f" to before its issue on {self.issued.get(self.op_stage[e['op']])})"
                                                          if e["effective"] == "retroactive" else ")") if e["effective"]
                                else "") for e in eff]
        if flowed:
            chain = []
            for ln in out["chain"]:
                h = ln.split(" ", 1)[0]
                fl = flowed.get(h)
                chain.append(ln + (f" (amends {self.op_result[h].op.target}, whose op {fl['via']} had written the words "
                                   f"into {fl['unit']}: the change flows to {fl['unit']})" if fl else ""))
            out["chain"] = chain

    # ------------------------------------------------------------------ provenance (latest reference)
    def _ref(self, uid: str, st: dict[str, UState], pages: bool = True) -> str:
        u = st.get(uid) or self.stages[0].state.get(uid)
        ins = inserted_ref(st, u, pages) if u is not None else None
        if ins:                                       # session 11 audit (A1-5): printed in the addendum, inserted at a place
            return ins
        doc, _, local = uid.partition(":")
        pg = u.pages if u is not None else []
        shown = f"{u.number} (issued as {local})" if u is not None and u.number else local
        return f"{doc} {shown}" + (f" p{','.join(map(str, pg))}" if pages and pg else "")

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

    def as_issued_text(self, uid: str) -> str:
        """A unit's text as issued (never assembled): the volume's text, or, for a unit first issued by an addendum, the
        addendum's own text at the stage that issued it (session 12, F1; audit A1-5: one rule for every row first issued
        by an addendum, so 'Text as issued' never shows a placeholder for some and the text for others)."""
        b = self.stages[0].state.get(uid)
        if b is not None and b.status != "not_issued":
            return b.text
        for s in self.stages[1:]:
            u = s.state.get(uid)
            if u is not None and u.status != "not_issued":
                return u.text or ""
        return ""

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
            unpaged = self._ref(uid, self.stages[0].state if uid in self.stages[0].state else st, pages=False)
            latest = f"{prov} ({verb} {unpaged})"
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

        def unit_line(uid: str, u0: UState) -> str:
            if u0.printed_in:                         # session 11 audit (A1-5): printed in the addendum, inserted at a place
                where = inserted_ref(st, u0) or ""
                after = where[where.index(" (inserted after ") + 2:-1] if " (inserted after " in where else ""
                return (f"{uid} ({u0.printed_in} p{','.join(map(str, u0.pages))}; {u0.origin.replace('_', ' ')}"
                        + (f"; issued by {u0.issued_by}" if u0.issued_by else "") + (f"; {after}" if after else "") + ")")
            return (f"{uid} ({u0.doc} p{','.join(map(str, u0.pages))}; {u0.origin.replace('_', ' ')}"
                    + (f"; issued by {u0.issued_by}" if u0.issued_by else "") + ")")
        for uid in row.units:
            u0 = base.get(uid) or st.get(uid)
            if u0 is not None:
                out.append(unit_line(uid, u0))
            eff = effective(st, uid, row.follows_replacement)
            for k in [uid] + ([eff.unit_id] if eff is not None and eff.unit_id != uid else []):
                hist += [h for h in (st[k].history if k in st else []) if h not in hist]
        for x in self.inserted_into(row, s.stage):  # session 11 audit (A1-2): the items inserted into the row's list
            if x["unit"] in st and x["unit"] not in row.units:
                out.append(unit_line(x["unit"], st[x["unit"]]))
                hist += [h for h in st[x["unit"]].history if h not in hist]
        why = {h: "" for h in hist}
        for h, w in self._chain_annotations(row, s).items():   # session 11 audit (A1-1, A2-7): annotations, anchors
            why.setdefault(h, w)
        hist += [h for h in why if h not in hist]
        hist.sort(key=lambda h: self.order.index(self.op_stage.get(h, BASE)))   # in addendum order (stable within one)
        for h in hist:
            prov = self.op_provision.get(h)
            pu = st.get(prov)
            out.append(f"{h} [{self.op_stage.get(h)}; {self.op_review.get(h)}{why.get(h) or ''}] <- {prov} "
                       f"({pu.doc} p{','.join(map(str, pu.pages))})" if pu else h)
        return out

    def _chain_annotations(self, row: Row, s: StageResult) -> dict[str, str]:
        """Session 11 audit (A1-1, A2-7): the ops that re-make a row or move its dates without changing its units, for the
        evidence chain, up to stage `s`: at each addendum stage where the row's reading is re-made or its dates move, every
        annotation on the row's dependency units (its units, their replacements and annotated parents: the answer or rule
        the reading follows, e.g. ADD-01/2.2 on VOL-I 5.2, ADD-02/Q7 on VOL-I 12.1); where its dates move, also the op that
        changed the date anchor's defining unit (ADD-01/2.1 on VOL-I 6.1 for VOL-I 8.3). {op id: '; why'}."""
        out: dict[str, str] = {}
        upto = self.order.index(s.stage)
        made = {it.stage for it in row.interpretations}
        for i in range(1, upto + 1):
            cur, prev = self.stages[i], self.stages[i - 1]
            moved = []
            for rd in row.date_rules:
                a = self.rf.anchors.get(rd.anchor or "")
                if not a:
                    continue
                va = anchor_values(prev.state, {rd.anchor: a}, {}).get(rd.anchor)
                vb = anchor_values(cur.state, {rd.anchor: a}, {}).get(rd.anchor)
                d = cur.state.get(a["defined_in"])
                if va != vb and d is not None:
                    moved += [(h, f"; moves the date anchor {rd.anchor} ({a['defined_in']})") for h in d.history
                              if self.op_stage.get(h) == cur.stage]
            if cur.stage not in made and not moved:
                continue
            deps = set()
            for uid in row.units:
                deps.add(uid)
                e = effective(cur.state, uid, row.follows_replacement)
                if e is not None:
                    deps.add(e.unit_id)
            for it in row.interpretations:          # session 11 recheck (A1-1): the consequence's unit is a dependency too
                cu = getattr(getattr(it, "consequence", None), "unit", None)
                if cu:
                    deps.add(cu)
            deps |= {cur.state[k].parent for k in list(deps) if k in cur.state and cur.state[k].parent}
            for k in sorted(deps):
                for h in (cur.state[k].annotations if k in cur.state else []):
                    if self.op_stage.get(h) == cur.stage and h not in out:
                        x = self.op_result.get(h)
                        out[h] = f"; annotates {k}" + (f" ({x.op.effect})" if x is not None and x.op.effect else "")
            for h, w in moved:
                out.setdefault(h, w)
            # session 12 (F5; audit A1 recheck A1-1 remainder): a reading made at this stage that cites an answer of the
            # stage by its printed reference ('ADD-02 Q7') rests on it: the answer's op is in the chain
            for it in row.interpretations:
                if it.stage != cur.stage:
                    continue
                for doc, q in re.findall(r"\b(ADD-\d+)[ /](Q\d+)\b", str(it.note or "")):
                    h = f"{doc}/{q}"
                    if self.op_stage.get(h) == cur.stage and h not in out:
                        x = self.op_result.get(h)
                        out[h] = f"; cited by the reading made at {cur.stage}" + (
                            f" ({x.op.effect})" if x is not None and x.op.effect else "")
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


def _pin_value_v2(state: dict[str, UState], uid: str) -> str:
    return unit_pin(state, uid)                 # format 2: every annotation hashed, confirming ones included


def migrate_pins(rowfile: RowFile, stages: list[StageResult]) -> tuple[int, list[str]]:
    """Format 1 or 2 -> PIN_FORMAT: upgrade a pin only where every dependency still has the value it was pinned to
    under format 1 or under format 2 (nothing changed since pinning); anything else is left as it is and stays STALE
    for a person. The fingerprint added in format 2 is taken from the current reading, so run this only when the
    readings have not changed since the pins were made (recorded in the work log). Format 3 (session 12) differs from
    format 2 only for a unit that carries a `confirms` annotation."""
    by_stage = {s.stage: s for s in stages}
    reg = Register(rowfile, stages, Calendar())
    n, kept = 0, []
    for row in rowfile.rows:
        for it in row.interpretations:
            if not it.pins or it.stage not in by_stage:
                continue
            st = by_stage[it.stage].state
            now = reg.pins_for(row, it, by_stage[it.stage])
            if set(now) == set(it.pins) and any(all(f(st, d) == v for d, v in it.pins.items())
                                                for f in (_pin_value_v1, _pin_value_v2)):
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


# ---------------------------------------------------------------------------------------------- glosses (session 11)

GLOSS_NOT_REVIEWED = "proposed translation, not reviewed"
_AR_RUN = re.compile("[\u0600-\u06ff]+(?:\\s+[\u0600-\u06ff]+)*")


def gloss_label(gloss: str | None, unit: dict | None, approval: dict | None, issues: dict[str, str] | None = None,
                quote: str = "") -> str:
    """How the English gloss of a non-English consequence is labelled, derived from the approval state at build time
    (session 11, audit A3-4/R-1). The gloss is 'confirmed' only when the unit comes from an image reading that is
    approved now (its `reading.status`, from curation/approvals.yaml at ingest) and the gloss is part of the reading's
    own displayed translation, which is what the approval confirms; otherwise it is the assistant's proposal. Open
    issues (`issues`: id -> text) that quote the consequence's own words keep what the words mean open, and are named.
    One wording for every output (A1, A3, a3_detail, the review batches)."""
    rd = (unit or {}).get("reading") or {}
    tr = (unit or {}).get("translation") or ""
    if not (gloss and approval and rd.get("status") == "approved" and approval.get("date")
            and normalize_latin(gloss).lower() in normalize_latin(tr).lower()):
        return GLOSS_NOT_REVIEWED
    words = [w for w in _AR_RUN.findall(normalize_arabic(quote or "")) if len(w.split()) >= 2] or \
        ([normalize_arabic(quote)] if quote else [])
    open_ = sorted(i for i, t in (issues or {}).items()
                   if any(w and w in normalize_arabic(t or "") for w in words))
    return (f"translation confirmed by the owner {approval['date']} ({rd.get('region')})"
            + (f"; category mapping open ({', '.join(open_)})" if open_ else ""))


def reading_approval(r: dict, region: str | None) -> dict | None:
    """The approval recorded for an image reading in this build (the evidence build's review packet, written at ingest
    from curation/approvals.yaml and valid only for the reading as approved), or None. Cached on `r`."""
    cache = r.setdefault("_reading_approvals", {})
    if region not in cache:
        p = Path(r.get("evidence_dir") or ".") / "review" / str(region) / "packet.json"
        try:
            cache[region] = json.loads(p.read_text(encoding="utf-8")).get("approval") if region and p.exists() else None
        except (OSError, ValueError):
            cache[region] = None
    return cache[region]


def consequence_gloss(r: dict, row: Row, cons) -> str:
    """gloss_label for a row's consequence in a stage2 run `r`: the consequence unit (as ingested), its reading's
    approval and the row's open issues. '' when the consequence has no gloss."""
    if not isinstance(cons, Consequence) or not cons.gloss:
        return ""
    units = r.setdefault("_units_by_id", {u["unit_id"]: u for u in r.get("units") or []})
    unit = units.get(cons.unit)
    region = ((unit or {}).get("reading") or {}).get("region")
    cur = r.get("curated_issues") or {}
    issues = {i: (cur.get(i) or {}).get("text", "") for i in row.issues if i in cur}
    return gloss_label(cons.gloss, unit, reading_approval(r, region), issues, cons.quote)


def dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str)
