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
  insert_row     a new row of a table that the provision describes in prose rather than prints as a table (session
                 09, blind rehearsal 02: "The Index of Forms in Volume IV is amended by adding, after the entry for
                 Form 4-F, an entry for Form 4-G with the title 'Cybersecurity Compliance Undertaking', Envelope 'A'
                 and Status 'Mandatory'"): `target` the table, `after` the row it follows (default: the last row),
                 `cells` {column: value}. The new unit is `<table>/<key>+<addendum>` (key as Stage 1 keys the table's
                 rows), a table_row of the table with those cells and the siblings' text form ("Form: 4-G | Title:
                 ... | Envelope: A | Status: Mandatory"), placed after `after` in the unit order
  annotate      a clarification answer or rule linked to units: effect none | confirms | interprets |
                 non_working_day (with `date`: a day the addendum notifies under VOL-I 2.4; from that stage the date
                 rules and the programme count it as non-working; C21: the provision prints the date) |
                 adds_obligation | renumbers (with `renumber: {unit: new number}`, each number printed in the
                 provision; ids keep their issued numbers and outputs cite "10.6 (issued as 10.5)"). Rules may name
                 a `subject`; the units mentioning it are listed
Dispositions for provisions that carry no op: no_effect (reason) or unresolved (blocks validation). Every
provision is treated (an op, op content or a disposition).

Session 12 (blind rehearsal 05, follow-ups 2 and 5): one quotation, one op.
  run-on quotations  ingest splits a provision into the clause and its list items (ADD-03:3.3, ADD-03:3.3(b)); an op's
                  quoted words may run on from its provision into the provision's own list items, in order (C21 reads
                  the provision and its items joined); the items the words reach are content of the op (C20) and
                  `details.quoted_across` lists them
  span replace_text   the volume splits a clause the same way (VOL-I:9.1, VOL-I:9.1(a) ...): when `old` is not in the
                  target alone, it is matched once across the clause and its active list items in order (normalised
                  as everywhere), replaced, and the result is re-split at its item letters into the clause body and
                  the items it now has (fewer or more). A unit whose words are unchanged keeps its id (re-lettered:
                  its text and `number` carry the new letter); a changed item keeps the id of the item with its letter;
                  a new item gets a new id (`<clause>(<letter>)`, or `...+<addendum>` if that id was ever used), printed
                  in the addendum; an item the result no longer has is deleted. Every unit whose text or status changes
                  carries the op in its history (rows citing it are re-read by today's rules); `details.span` records
                  before and after. A quotation that does not match as one contiguous span says where it breaks
                  (the unit it matched from, the unit and words where it stopped matching), never just "not found"
  inserted targets   a unit an earlier op of the same addendum (or an earlier addendum) inserted exists for later
                  ops; an op may name it by the number it was inserted as ('VOL-II:5.6' for VOL-II:5.5+ADD-03,
                  `details.resolved_targets`); an annotation of a unit printed in this addendum is cited as the
                  addendum's own units are
  precedence      on an annotate op over two renderings issued together (an Arabic table and its English
                  translation): {governs, over, words}, where `words` is printed in the provision (C21) and governs/over
                  are the op's targets (C22); or `unstated` when the addendum does not say, refused if the provision
                  prints a precedence word (governs, prevails, takes precedence). The engine never decides which
                  rendering governs; `unstated` is carried to the rows as a flag for a person (register)

Session 11 (blind rehearsal 04), three attributes of an op rather than new types:
  effective_from  'With effect from 8 October 2026': the ISO date the provision prints (C21). The op applies at its
                  addendum's stage as any other; its result says `effective` retroactive | deferred | on issue, and the
                  register shows the date. The states of earlier stages are copies and are never rewritten.
  an amendment of an earlier addendum's amending text: a replace_text whose target is an earlier addendum's unit (ADD-01:5.1)
                  that wrote words into other units (ADD-01/5.1 appended a sentence to VOL-II:5.3) changes those words
                  where they were written as well (`details.flowed`; VOL-II 5.3 <- ADD-01 5.1 <- ADD-03 5.2). Words the
                  earlier op never wrote change only that addendum's unit, as before; words it wrote that are no longer
                  there as written make the op invalid (nothing is half applied).
  condition       a conditional amendment ('This Section 7 has effect only if ...'): {id, trigger, trigger_unit,
                  applicability, deadline (a date rule), if_not_triggered, affects}, every quoted field printed in the
                  trigger unit or the provision (C21/C22). The op is checked as if triggered and both states are kept
                  (`details.conditional`: if_triggered {unit: {before, after}}), but it applies only when a person has
                  recorded the trigger as a dated fact with evidence (load_triggers: curation/triggers.yaml), and then
                  from that date; otherwise it is `pending` (OpResult.pending; applied False), its provision and trigger
                  unit are accounted `conditional`, and a held conditional op does not make the addendum PARTIAL. Nothing
                  assumes a trigger occurred. StageResult.conditions lists the conditions in play (conditions_of).

Checks per op (an invalid op is listed and changes NOTHING: the state, including history, annotations and
the unit order, is restored to what it was before the op; ops are applied as transactions):
  C21 the op's quoted words (old/new/new_text) occur in its provision; a set_value's new value is the figure
      the provision states (with the row's unit where it has one) and its column is named in the provision;
      an inserted list item's WHOLE text is printed by the provision, the new group or a named unit of the
      same addendum (never a unit of the pack, never a supported quotation with words added around it); every
      cell of an inserted row is printed by the provision after its column's name, quoted ("Envelope 'A'") or,
      for the key, as "<column> <value>" ("Form 4-G")
  C22 the target exists and its state allows the operation; the declared target is the one the
      provision (or its section heading) cites (citations.verify_target; for insert_row also "the Index of Forms in
      Volume IV", the volume's one table whose first column is "Form" and which has a "Title" column); an
      inserted row's `after` is a row of that table the provision names ("after the entry for Form 4-F"), every
      column is in the table's header and no row of the table has the new row's key yet; claims such as
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
Review, validity and application are three separate things on every result (session 08):
  valid      the op passes its structural checks (C21-C27) against the state immediately before it
  withdrawn  a person's latest named decision on the op is a rejection (passed in by the caller from the
             decisions file; a `review: rejected` flag in the op file also withholds it). A withdrawn op is still
             checked (on a copy) so its structural validity is reported, but it changes nothing
  applied    valid and not withdrawn
A provision whose only ops are withdrawn is `rejected` in the coverage (not `unresolved`, which means its ops
are invalid); either makes the addendum PARTIAL.
Each result also carries `subject`: what a review decision on it is bound to, captured immediately BEFORE the
op runs, whether or not it then applies: the provision's text, pages and evidence anchors, its section heading,
and the pin of every unit it reads or changes (targets, anchors, every member of a replaced table or form and
of its replacement, inserted groups, annotated groups, covered provisions, claims). Applying or withholding the
op therefore never changes its own subject, and a change to any member row voids a decision on it.
"""
from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_serializer

from .citations import after_row, citations, is_index_table, verify_target
from .dates import MONTHS, parse_date
from .textnorm import has_arabic, normalize_arabic, normalize_latin, slug
from .util import load_yaml, sha256_text

BASE = "BASE"
OP_TYPES = ("replace_text", "set_value", "append_text", "set_status", "replace_unit", "insert_unit", "insert_row",
            "annotate")


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class DeadlineRule(_Strict):
    """The trigger's deadline as a date rule (dates.DateRule fields; session 11), so A5 can plan a decision milestone:
    e.g. {kind: relative, anchor: PDD, offset: 10, unit: working_day, direction: before, text: 'not later than ten (10)
    Working Days before the Proposal Due Date'}. `text` is printed in the trigger unit."""
    kind: Literal["relative", "fixed", "anchor"] = "relative"
    anchor: str | None = None
    offset: int = 0
    unit: Literal["calendar_day", "working_day", "week", "month", "year"] = "calendar_day"
    direction: Literal["after", "before"] = "after"
    fixed: str | None = None
    text: str


class Condition(_Strict):
    """A conditional amendment (session 11): the op applies only if a stated event occurs. Every quoted field is printed
    in the trigger unit (or, for the applicability and the lapse, in the op's provision); a person records whether the
    event occurred (a trigger fact, `triggers`), and only then does the engine apply the op. Ops sharing an `id` are
    the alternative state 'if triggered'; the state if not is the unit as it stands."""
    id: str                                                    # shared by every op of the condition (e.g. ADD-03/S7)
    trigger: str                                               # the event, verbatim
    trigger_unit: str                                          # the unit that states it (ADD-03:7.1)
    applicability: str                                         # 'has effect only if' (not in effect unless ...)
    deadline: DeadlineRule | None = None                       # when the trigger must occur by
    if_not_triggered: str | None = None                        # the words saying what happens otherwise ('... lapses')
    affects: list[str] = Field(default_factory=list)           # further obligations the curator names (rows, units)


class Precedence(_Strict):
    """Which of two renderings issued together governs, in the addendum's own words (session 12)."""
    governs: str                                               # the governing rendering (a target of the op)
    over: list[str] = Field(default_factory=list)              # the renderings it prevails over (targets of the op)
    words: str                                                 # the words of the provision that say so (C21)


class Op(_Strict):
    id: str
    provision: str
    type: Literal["replace_text", "set_value", "append_text", "set_status", "replace_unit", "insert_unit", "insert_row",
                  "annotate"]
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
    after: str | None = None                                   # insert_row: the row the new one follows (default: last)
    cells: dict[str, str] | None = None                        # insert_row: the new row, {column: value}
    effect: Literal["none", "confirms", "interprets", "adds_obligation", "renumbers", "non_working_day"] | None = None
    date: str | None = None                                    # annotate/non_working_day: the notified day (ISO), as printed
    renumber: dict[str, str] = Field(default_factory=dict)     # annotate/renumbers: unit id -> its new printed number
    subject: str | None = None                                 # annotate rule: phrase whose mentions are listed
    covers: list[str] = Field(default_factory=list)            # provisions that are content of this op
    claims: list[dict] = Field(default_factory=list)           # [{unit, status, by_provision_prefix}]
    expect: list[dict] = Field(default_factory=list)           # [{row, column, delta}|{row, column, equals}|{contains}]
    issue: str | None = None                                   # something the op leaves open for a person
    note: str | None = None
    # session 11 audit (A2-6): annotate on a clarification answer: units of the documents the answer RESTATES without
    # citing them (ADD-01 Q4 restates VOL-I 5.5). Checked: each is in force before the op and the answer, read against
    # it (summary.classify_answer), has a sentence that confirms it; never an annotation of that unit
    restates: list[str] = Field(default_factory=list)
    effective_from: str | None = None                          # session 11: ISO date the provision prints ('With effect from ...')
    condition: Condition | None = None                         # session 11: applies only if a person records the trigger
    precedence: Literal["unstated"] | Precedence | None = None # session 12: annotate over two renderings issued together
    origin: Literal["pattern", "assistant", "person"] = "assistant"
    review: Literal["proposed", "accepted", "rejected"] = "proposed"
    reviewer: str | None = None

    @model_serializer(mode="wrap")
    def _without_unset_session11(self, handler):
        # an op without the session 11 fields dumps exactly as before they existed, so what a review decision on it is
        # bound to does not change for ops that do not use them
        d = handler(self)
        for k in ("effective_from", "condition", "precedence"):
            if getattr(self, k) is None:
                d.pop(k, None)
        if not self.restates:                     # session 11 audit: absent unless used (bindings unchanged)
            d.pop("restates", None)
        return d


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
    # session 11 audit (A1-5): a unit an op inserted is PRINTED in the addendum (its pages are the provision's), at a
    # place in a volume: `printed_in` is that addendum, `inserted_after` the unit it follows (inserted_ref labels it)
    printed_in: str | None = None
    inserted_after: str | None = None
    reading_region: str | None = None   # session 12 (W3b): the image reading (region id) the unit was read from

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
            reading_subject=(u.get("reading") or {}).get("subject_sha256"),
            reading_region=(u.get("reading") or {}).get("region"))
    return st


def group_members(state: dict[str, UState], group: str, exclude: set[str] = frozenset()) -> list[str]:
    """Units of a group id: the unit itself, ids under 'group/', and the group's heading ('DOC:H:X')."""
    doc, _, local = group.partition(":")
    out = [k for k in state if (k == group or k.startswith(group + "/") or k == f"{doc}:H:{local}") and k not in exclude]
    return out


def _contains(text: str, phrase: str) -> int:
    if has_arabic(phrase):                       # Arabic words: compared without diacritics, with alef forms unified
        return normalize_arabic(text).count(normalize_arabic(phrase))
    return normalize_latin(text).count(normalize_latin(phrase))


def _quoted_in(provision_text: str, phrase: str) -> bool:
    if has_arabic(phrase):
        return normalize_arabic(phrase) in normalize_arabic(provision_text)
    return normalize_latin(phrase).replace("'", "") in normalize_latin(provision_text).replace("'", "")


def _evidence_form(t: str) -> str:
    return " ".join(normalize_latin(t or "").replace("'", "").split()).lower()


def unevidenced_additions(prev: dict[str, "UState"], cur: dict[str, "UState"], addendum: str) -> list[str]:
    """C47, independent of the op types: every word a unit of the pack gains between two consecutive stages
    (a new unit, words inserted or substituted in its text, a new cell value) must be printed somewhere in that
    stage's addendum. Returns 'unit: added words' for each run of added words the addendum does not print."""
    import difflib
    evidence = " \n ".join(_evidence_form(u.text) for u in cur.values() if u.doc == addendum)
    # session 12: one quotation that ingest split into a provision and its list items is printed as one text
    kids: dict[str, list[str]] = {}
    for u in cur.values():
        if u.doc == addendum and u.kind == "list_item" and u.parent in cur:
            kids.setdefault(u.parent, []).append(u.text or "")
    evidence += "".join(" \n " + _evidence_form(" ".join([cur[p].text or ""] + t)) for p, t in kids.items())
    out = []
    for k, u in cur.items():
        if u.doc == addendum:
            continue
        p = prev.get(k)
        runs: list[str] = []
        if p is None:
            par = cur.get(u.parent) if u.parent else None
            header = [c.strip() for c in (par.text or "").split("|")] if par is not None and par.kind == "table" else []
            if u.cells and header and set(u.cells) <= set(header):
                # a new row of a table (insert_row, session 09): its column names are the table's own header, so the
                # added words are its cell values ('Form: 4-G | Title: ...' is not printed as such; '4-G' and the title are)
                runs = [v for v in u.cells.values() if v]
            else:
                runs = [u.text or ""]
        else:
            if (u.text or "") != (p.text or ""):
                # words compared without the punctuation around them: a deletion moves a full stop or comma onto the
                # word before it ('cells, and ... Authority.' -> 'cells.'), which gains no word (session 08 blind rehearsal)
                # (the words are aligned without it; the added words are then checked as printed, punctuation included)
                bw = (u.text or "").split()
                a, b = [w.strip(",;:.") for w in (p.text or "").split()], [w.strip(",;:.") for w in bw]
                for tag, _, _, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
                    if tag in ("insert", "replace"):
                        runs.append(" ".join(bw[j1:j2]))
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
    valid: bool                              # structural checks pass (never set by a review decision)
    checks: list[dict]
    changed: list[str] = field(default_factory=list)
    details: dict = field(default_factory=dict)
    withdrawn: bool = False                  # a person rejected it: checked, but not applied
    subject: dict = field(default_factory=dict)   # what a decision is bound to (state immediately before the op)
    pending: bool = False                    # session 11: a conditional op whose trigger no person has recorded as having
                                             # occurred (or recorded as not occurred): checked on a copy, never applied

    @property
    def applied(self) -> bool:
        return self.valid and not self.withdrawn and not self.pending

    @property
    def conditional_pending(self) -> bool:
        """Valid, not withdrawn, and held only because its condition is not (or not yet) met: correctly not applied."""
        return self.valid and not self.withdrawn and self.pending

    def to_dict(self) -> dict:
        return {"op": self.op.model_dump(exclude_none=True), "stage": self.stage, "valid": self.valid,
                "withdrawn": self.withdrawn, "applied": self.applied,
                **({"pending": True} if self.pending else {}),
                "checks": self.checks, "changed": self.changed, "details": self.details}


def unit_evidence(u: dict, doc_sha256: str | None = None) -> dict:
    """Where a unit of the evidence build is printed, for binding decisions (session 09): its source document (id and,
    when the caller knows it, the document's sha256 from the build manifest), its pages, each anchor's page, box
    (rounded to 0.1 pt, written as text so the value is stable across rebuilds) and spans, and for an image reading
    its region and the reading's review subject (which covers the native image sha256, page and box)."""
    return {"doc": u.get("doc"), "doc_sha256": doc_sha256, "pages": sorted(u.get("pages") or []),
            "anchors": [{"page": a.get("page"), "bbox": [f"{float(v):.1f}" for v in a.get("bbox") or []],
                         "spans": list(a.get("spans") or [])} for a in u.get("anchors") or []],
            "region": u.get("region") or (u.get("reading") or {}).get("region"),
            "reading": (u.get("reading") or {}).get("subject_sha256")}


def inserted_ref(state: dict[str, "UState"], u: "UState", pages: bool = True) -> str | None:
    """The reference of a unit an addendum op inserted (session 11 audit, A1-5): the document and page it is PRINTED on
    (the addendum, the provision's page), then its insertion point with that unit's own page: 'ADD-02 p3 (inserted after
    VOL-I 9.1(e), p4)'. None for any other unit. Never the volume's name with the addendum's page."""
    if u is None or not u.printed_in:
        return None
    head = u.printed_in + (f" p{','.join(map(str, u.pages))}" if pages and u.pages else "")
    if not u.inserted_after:
        return head
    a = state.get(u.inserted_after)
    doc, _, local = u.inserted_after.partition(":")
    where = f"{doc} {a.number} (issued as {local})" if a is not None and a.number else f"{doc} {local}"
    if a is not None and a.printed_in:                       # inserted after a unit that was itself inserted
        where = inserted_ref(state, a, pages=False) or where
    return head + f" (inserted after {where}" + (f", p{','.join(map(str, a.pages))}" if pages and a is not None
                                                 and a.pages and not a.printed_in else "") + ")"


def unit_pin(state: dict[str, "UState"], uid: str, evidence: dict | None = None) -> str:
    """A unit as it stands: status, text and cells, the annotations on it and, for an image reading, the
    reading's review-subject fingerprint. 'absent' when the unit does not exist.
    With `evidence` ({unit id: unit_evidence(...)}), the pin also binds the unit's SOURCE: its document identity,
    pages, anchor boxes and spans, and its image region (decision bindings: Engine.subject, review.row_binding). A
    unit created by an op has no printed place of its own; its document, pages and creating op stand in for it.
    Without `evidence` the pin is the content-only value interpretations are pinned to (register.pin_value)."""
    u = state.get(uid)
    if u is None:
        return "absent"
    content = u.sha() + "|" + ",".join(sorted(u.annotations)) + "|" + (u.reading_subject or "")
    if evidence is None:
        return sha256_text(content)[:16]
    # a unit an op inserted is printed in the addendum, on the provision's pages, at its insertion point (A1-5)
    src = evidence.get(uid) or {"doc": u.printed_in or u.doc, "pages": list(u.pages), "created_by": u.history[:1],
                                **({"inserted_after": u.inserted_after} if u.inserted_after else {})}
    return sha256_text(content + "|" + json.dumps(src, ensure_ascii=False, sort_keys=True))[:16]


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
    non_working_days: list[str] = field(default_factory=list)   # days notified under VOL-I 2.4 at or before this stage
    conditions: list[dict] = field(default_factory=list)        # session 11: conditional ops stated at or before this
                                                                 # stage, with their state (conditions_of)


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
    def __init__(self, units: list[dict], opfiles: list[OpFile], withdrawn: dict[str, dict] | None = None,
                 triggers: dict[str, dict] | None = None):
        """withdrawn: op id -> the person's rejection ({reviewer, date, note}); those ops are checked, never applied.
        triggers (session 11): condition id -> the fact a person recorded (load_triggers); without one a conditional
        op is pending and never applied."""
        self.units = units
        self.order = [u["unit_id"] for u in units]
        self.opfiles = sorted(opfiles, key=lambda f: int(f.addendum.split("-")[1]))
        self.addenda = [f.addendum for f in self.opfiles]
        self.withdrawn = dict(withdrawn or {})
        self.triggers = dict(triggers or {})
        self.evidence = {u["unit_id"]: unit_evidence(u) for u in units}    # where each unit is printed (unit_pin)
        self._issued_now: str | None = None                       # the issue date of the stage being applied
        # session 11 (D1): a clause an addendum inserted ('new Clause 9.3 ... after Clause 9.2' -> VOL-I:9.2+ADD-01) is
        # cited by later addenda by the number it was inserted as: {inserted unit id: 'VOL-I:9.3'}
        self.inserted_as: dict[str, str] = {}
        self._applied_before: list[OpResult] = []                 # ops applied at earlier stages (flows, session 11)

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
            self._issued_now = res.issued
            for k, u in st.items():                                   # the addendum's own units are issued
                if u.doc == f.addendum and u.status == "not_issued":
                    u.status = "active"
            before = {k: u.sha() for k, u in st.items()}
            for op in self._ordered(f):
                subject = self.subject(op, st)                       # bound before the op, applied or not
                snap, order = copy.deepcopy(st), list(self.order)
                r = self._apply(op, st, f.addendum)
                rej = self.withdrawn.get(op.id) or ({"reviewer": op.reviewer, "flag": "review: rejected in the op file"}
                                                    if op.review == "rejected" else None)
                if op.condition is not None:          # session 11: checked as if triggered; applied only on a fact
                    r.pending = self._condition(op, r, snap, st, f.addendum, res)
                if not r.valid or rej or r.pending:   # a failed, withdrawn or pending op changes nothing: restore
                    st.clear()
                    st.update(snap)
                    self.order[:] = order
                    r.changed = []
                    r.details.pop("content", None)
                if rej:
                    r.withdrawn, r.details["withdrawn_by"] = True, rej
                r.subject = subject
                res.ops.append(r)
            self._coverage(res, f)
            self._scope(res, before, f.addendum)
            res.non_working_days = sorted(set(stages[-1].non_working_days)
                                          | {x.details["non_working_day"] for x in res.ops if x.applied and x.details.get("non_working_day")})
            res.conditions = conditions_of(stages[-1], res)
            # a conditional op that is valid and held only by its condition is correctly not applied: it does not make
            # the addendum PARTIAL (session 11); an invalid or withdrawn one does
            if res.problems or res.scope_leak or any(not r.applied and not r.conditional_pending for r in res.ops) or \
                    any(c["disposition"] in ("unresolved", "rejected") or not c["accounted_by"] for c in res.coverage):
                res.status = "PARTIAL"
            stages.append(res)
            self._applied_before += [x for x in res.ops if x.applied]
        return stages

    # ------------------------------------------------------------------ conditions (session 11)
    def _condition(self, op: Op, r: OpResult, snap: dict[str, UState], st: dict[str, UState], addendum: str,
                   res: StageResult) -> bool:
        """Check a conditional op's condition against the state before it (every quoted field printed in the trigger
        unit, a unit of this addendum, or in the provision), record both states (`details.conditional`) and decide from
        the trigger facts whether it applies. Returns True when the op is pending (held: no fact that the trigger
        occurred). A failed check makes the op invalid."""
        c = op.condition
        tu = snap.get(c.trigger_unit)
        prov = snap.get(op.provision)
        ttext = tu.text if tu is not None else ""
        both = ttext + " \n " + (prov.text if prov is not None else "")

        def check(cid, ok, detail):
            r.checks.append({"id": cid, "ok": bool(ok), "detail": detail})
            if not ok:
                r.valid = False
        check("C22", tu is not None and tu.doc == addendum, f"the trigger unit {c.trigger_unit} is a unit of {addendum}"
              if tu is not None and tu.doc == addendum else f"the trigger unit {c.trigger_unit} is not a unit of {addendum}")
        check("C21", bool(ttext) and _quoted_in(ttext, c.trigger), f"the trigger is printed in {c.trigger_unit}"
              if ttext and _quoted_in(ttext, c.trigger) else f"the trigger is not in {c.trigger_unit}: '{c.trigger[:80]}'")
        check("C21", _quoted_in(both, c.applicability), "the applicability words are printed in the trigger unit or the "
              "provision" if _quoted_in(both, c.applicability) else f"the applicability words are not in "
                                                                     f"{c.trigger_unit} or {op.provision}: '{c.applicability[:80]}'")
        if c.if_not_triggered:
            check("C21", _quoted_in(both, c.if_not_triggered), "the words for the state if not triggered are printed"
                  if _quoted_in(both, c.if_not_triggered) else f"the words for the state if not triggered are not in "
                                                                f"{c.trigger_unit} or {op.provision}")
        if c.deadline is not None:
            d = c.deadline
            ok = _quoted_in(ttext, d.text) and (d.kind != "relative" or (bool(d.anchor) and d.offset >= 1)) and \
                (d.kind != "fixed" or bool(d.fixed))
            check("C21", ok, f"the trigger's deadline is printed in {c.trigger_unit} ('{d.text[:60]}')" if ok else
                  f"the trigger's deadline is not a usable date rule printed in {c.trigger_unit}: '{d.text[:60]}'")
        r.details["conditional"] = cd = {
            "condition": c.id, "trigger": c.trigger, "trigger_unit": c.trigger_unit, "applicability": c.applicability,
            "deadline": c.deadline.model_dump() if c.deadline else None, "if_not_triggered": c.if_not_triggered,
            "affects": list(c.affects), "state": "pending", "fact": None,
            "if_triggered": {k: {"before": snap[k].text if k in snap else None, "after": st[k].text if k in st else None}
                             for k in r.changed} if r.valid else {},
            "targets": list(r.changed) if r.valid else []}
        if not r.valid:
            cd["state"] = "invalid"
            return False
        fact, problems = self._trigger_fact(c.id)
        if problems:
            res.problems += [f"trigger record for {c.id}: {p}" for p in problems]
            cd["trigger_problems"] = problems
            return True
        if fact is None:
            return True                                           # nothing assumes the trigger occurred
        cd["fact"] = fact
        if not fact["occurred"]:
            cd["state"] = "not_triggered"
            return True
        cd["state"] = "triggered"
        r.details.setdefault("effective_from", fact["date"])
        return False

    def _trigger_fact(self, cid: str) -> tuple[dict | None, list[str]]:
        """The fact a person recorded for a condition: {condition, occurred, date, recorded_by, evidence, note}. A
        record that is not a person's, has no ISO date or no evidence is a problem, and the op stays pending."""
        f = self.triggers.get(cid)
        if f is None:
            return None, []
        from .readings import is_assistant, valid_reviewer
        out = []
        if not isinstance(f.get("occurred"), bool):
            out.append("`occurred` must be true or false")
        try:
            date.fromisoformat(str(f.get("date")))
        except ValueError:
            out.append(f"`date` must be the ISO date the event occurred (or was established not to), got {f.get('date')!r}")
        who = f.get("recorded_by")
        if not valid_reviewer(who) or is_assistant(who):
            out.append("`recorded_by` must name the person who recorded the fact (never the program or a model)")
        ev = f.get("evidence")
        if not isinstance(ev, list) or not ev or not all(isinstance(q, dict) and str(q.get("words") or "").strip()
                                                          and (q.get("source") or q.get("unit")) for q in ev):
            out.append("`evidence` must list [{source or unit, words}] (the notice that shows it)")
        return (None if out else {k: f.get(k) for k in ("condition", "occurred", "date", "recorded_by", "evidence",
                                                         "note")}), out

    def subject(self, op: Op, st: dict[str, UState]) -> dict:
        """What a decision on `op` is bound to, from the state immediately before it (see the module docstring). Each
        unit's pin covers its content and its source (document, pages, anchor boxes and spans, image region: unit_pin
        with self.evidence), so a member row printed elsewhere with the same words changes the subject (session 09);
        review.op_binding adds the sha256 of each document involved."""
        scope = {op.target, op.anchor, op.new_text_from, getattr(op, "after", None), *op.targets, *op.covers,
                 *(c.get("unit") for c in op.claims)}
        groups = [g for g in (op.replacement, op.new_group) if g]
        if op.type in ("replace_unit", "insert_row") and op.target:   # insert_row reads the table's header and rows
            groups.append(op.target)
        if op.type == "annotate":
            groups += [t for t in op.targets if t not in st]
        for g in groups:
            scope |= set(group_members(st, g)) | {g}
        scope.discard(None)
        prov = st.get(op.provision)
        return {"provision": {"unit": op.provision, "text": prov.text if prov else None,
                              "pages": list(prov.pages) if prov else None, "evidence": self.evidence.get(op.provision)},
                "heading": heading_of(self.order, st, op.provision) if prov else None,
                "before": {k: unit_pin(st, k, self.evidence) for k in sorted(scope)}}   # content AND source of each

    def _ordered(self, f: OpFile) -> list[Op]:
        pos = {k: i for i, k in enumerate(self.order)}
        return sorted(f.ops, key=lambda o: (pos.get(o.provision, 10 ** 9), f.ops.index(o)))

    # ------------------------------------------------------------------ coverage and scope
    def _coverage(self, res: StageResult, f: OpFile) -> None:
        st = res.state
        disp = {d.provision: d for d in f.dispositions}
        by_op: dict[str, list[str]] = {}
        applied_for: dict[str, bool] = {}
        withdrawn_for: dict[str, bool] = {}
        held_for: dict[str, str] = {}                 # session 11: provision -> why its conditional op is held
        for r in res.ops:
            cond = r.op.condition.trigger_unit if r.op.condition is not None else None
            for p in [r.op.provision] + r.op.covers + r.details.get("content", []) + ([cond] if cond else []):
                if r.op.id not in by_op.setdefault(p, []):
                    by_op[p].append(r.op.id)
                applied_for[p] = applied_for.get(p, False) or r.applied
                withdrawn_for[p] = withdrawn_for.get(p, False) or r.withdrawn
                if r.conditional_pending and p not in held_for:
                    cd = r.details.get("conditional") or {}
                    held_for[p] = (f"conditional ({cd.get('condition')}): "
                                   + ("not triggered, as a person recorded" if cd.get("state") == "not_triggered" else
                                      f"not in effect unless the trigger occurs ('{_short_words(cd.get('trigger'), 120)}');"
                                      " no person has recorded that it did")
                                   + "; both states are kept")
        for p in provisions(st, f.addendum):
            d = disp.get(p)
            if d:
                kind, reason = d.disposition, d.reason
            elif p in by_op:
                # a provision none of whose ops applies is not accounted for (C20): `rejected` when a person withdrew
                # an op for it, `unresolved` when its ops are invalid. Both keep the addendum PARTIAL. A conditional op
                # held by its condition accounts for its provision and its trigger unit (`conditional`, session 11)
                if applied_for[p]:
                    kind, reason = "op", ""
                elif p in held_for and not withdrawn_for[p]:
                    kind, reason = "conditional", held_for[p]
                elif withdrawn_for[p]:
                    kind, reason = "rejected", ("every op for this provision was rejected by a person and is withheld; "
                                                "a corrected op or a disposition is needed")
                else:
                    kind, reason = "unresolved", "every op for this provision is invalid"
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

        prov = st.get(op.provision)
        if not check("C21", prov is not None and prov.doc == addendum, f"provision {op.provision} belongs to {addendum}"):
            return r
        ptext = prov.text
        if op.effective_from is not None:            # session 11: an effective date is the one the provision prints
            printed = _printed_dates(ptext)
            if not check("C21", op.effective_from in printed,
                         f"the provision prints the effective date {op.effective_from}" if op.effective_from in printed
                         else f"the effective date must be a date the provision prints ({printed or 'none'}); the op "
                              f"says {op.effective_from!r}"):
                return r
            r.details["effective_from"] = op.effective_from
            if self._issued_now:
                r.details["effective"] = ("retroactive" if op.effective_from < self._issued_now else
                                          "deferred" if op.effective_from > self._issued_now else "on issue")
        cite_text = ptext + " " + heading_of(self.order, st, op.provision)
        quoted = [x for x in (op.old if op.old_resolved == "quoted" else None, op.new, op.new_text) if x]
        # session 12: the quotation may run on into the provision's own list items (one quotation that ingest split)
        kids = [k for k in self.order if k in st and st[k].parent == op.provision and st[k].doc == addendum
                and st[k].kind == "list_item"]
        run_on: list[str] = []
        if op.type in ("replace_text", "append_text", "set_status") and quoted:
            bad = [q for q in quoted if not _quoted_in(ptext, q)]
            if bad and kids:
                run_on = _items_reached([ptext] + [st[k].text for k in kids], [op.provision] + kids, bad)
                bad = [q for q in bad if not run_on or not _quoted_in(" ".join([ptext] + [st[k].text for k in kids]), q)]
            if not check("C21", not bad, (f"quoted words found in {op.provision}" + (
                    f" and its list items {', '.join(k for k in run_on if k != op.provision)} (one quotation)"
                    if run_on else "")) if not bad else f"not in the provision: {bad}"):
                return r
            if run_on:
                r.details["quoted_across"] = run_on
        ids = set(st)
        label = lambda uid: st[uid].label if uid in st else None  # noqa: E731

        if op.type == "annotate":
            targets, resolved = self._inserted_targets(op.targets, st)          # session 12
            if resolved:
                r.details["resolved_targets"] = resolved
            missing = [t for t in targets if t not in st and not group_members(st, t)]
            if not check("C22", targets and not missing, f"targets exist: {op.targets}" + (f"; missing {missing}" if missing else "")):
                return r
            if op.effect in ("confirms", "interprets", "adds_obligation"):
                # a unit printed in this addendum (inserted by an earlier op of it) is cited as the addendum's own are
                cited_ok = [verify_target(t, cite_text, ids, label)[0] or t.startswith(addendum)
                            or (t in st and st[t].printed_in == addendum) for t in targets]
                if not check("C22", all(cited_ok), "every annotated target is cited by the provision"
                             if all(cited_ok) else f"not cited: {[t for t, ok in zip(targets, cited_ok) if not ok]}"):
                    return r
            if op.precedence is not None and not self._precedence(op, targets, ptext, st, r, check):
                return r
            if op.effect == "renumbers":
                bad = [k for k in op.renumber if k not in op.targets or k not in st]
                stated = ptext + " " + _letter_ranges(ptext)       # "(g) to (j)" states (g), (h), (i) and (j)
                unstated = [v for v in op.renumber.values() if not re.search(r"(?<![\d.])" + re.escape(v) + r"(?![\d])", stated)]
                if not check("C21", op.renumber and not bad and not unstated,
                             f"renumbering {op.renumber} stated in {op.provision}" if op.renumber and not bad and not unstated
                             else f"renumbering not supported by the provision: targets {bad}, numbers not printed {unstated}"):
                    return r
                for k, v in op.renumber.items():
                    st[k].number = v
                r.details["renumbered"] = dict(op.renumber)
            if op.effect == "non_working_day":       # a day notified under VOL-I 2.4: the date the provision prints
                try:
                    p = parse_date(ptext)
                except ValueError:
                    p = None
                printed = p[0].isoformat() if p else None
                if not check("C21", bool(op.date) and printed == op.date,
                             f"the provision prints the notified day {op.date}" if op.date and printed == op.date
                             else f"the notified day must be the date the provision prints ({printed}); the op says {op.date!r}"):
                    return r
                r.details["non_working_day"] = op.date
            if op.restates:
                # session 11 audit (A2-6): a clarification answer that restates a unit it does not cite, read against
                # it and its annotated targets; one that only confirms or interprets is not a new obligation (C28 reads
                # `answer_class`). Only on a curated `restates` claim: no answer is reclassified without one
                from .summary import answer_targets, classify_answer
                bad = [k for k in op.restates if k not in st or st[k].status != "active" or st[k].doc == addendum]
                if not check("C22", not bad, f"restated units in force: {op.restates}" if not bad
                             else f"restated units not in force before {op.id} (or units of {addendum}): {bad}"):
                    return r
                question = re.split(r"Authority response:", ptext)[0]
                tg = answer_targets(st, [t for t in op.targets if t != op.provision] + list(op.restates))
                c = classify_answer(ptext, tg, [question])
                r.details["answer_class"] = {"class": c["class"], "restates": list(op.restates), "why": c["why"],
                                             "sentences": [{"text": x["text"], "kind": x["kind"]} for x in c["sentences"]]}
                if op.restates and not check(
                        "C22", any(x["kind"] == "confirms" for x in c["sentences"]),
                        f"the answer restates {', '.join(op.restates)} (a sentence confirms it)"
                        if any(x["kind"] == "confirms" for x in c["sentences"]) else
                        f"no sentence of the answer confirms {', '.join(op.restates)}: not a restatement"):
                    return r
            for t in targets:
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

        if op.type == "insert_row":
            return self._insert_row(op, st, addendum, prov, cite_text, r, check)

        # every other op has one declared target that must be the cited one
        target = op.target
        if target and target not in st:                                  # session 12: named by its inserted number
            (target,), resolved = self._inserted_targets([target], st)
            if resolved:
                r.details["resolved_targets"] = resolved
        tgt = target
        if op.type == "insert_unit":
            target = op.anchor or op.new_group
        ok, why, cited = verify_target(target, cite_text, ids, label) if target else (False, "no target", [])
        alias = self.inserted_as.get(target) if target else None
        if not ok and alias and alias not in ids and verify_target(alias, cite_text, ids | {alias}, label)[0]:
            # session 11 (D1): the provision cites the clause an earlier addendum inserted by its inserted number
            ok, why, cited = True, f"declared target {target} is {alias} as inserted by {st[target].issued_by}", [target]
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
            t = st.get(tgt)
            if not check("C22", t is not None, f"target {op.target} exists"):
                return r
            r.details["reading_status"] = t.reading_status
            if op.type == "replace_text":
                if not check("C22", t.status == "active", f"target is {t.status}"):
                    return r
                n = _contains(t.text, op.old)
                items = [k for k in self.order if k in st and st[k].parent == tgt and st[k].kind == "list_item"
                         and st[k].status == "active"]
                if n == 0 and items:                 # session 12: the old words span the clause and its list items
                    if not self._replace_span(op, tgt, items, st, addendum, prov, r, check):
                        return r
                    return self._finish(op, r, run_on)
                if not check("C23", n == 1, f"'{op.old}' occurs {n} time(s) in {op.target}"):
                    r.details["also_in"] = _also_in(st, tgt, op.old)
                    return r
                r.details["also_in"] = _also_in(st, tgt, op.old)
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
            r.changed = [tgt]
            if op.type == "replace_text" and t.doc.startswith("ADD-") and t.doc != addendum:
                # session 11: an earlier addendum's amending text is amended: the change flows to the units that
                # addendum's op wrote those words into (VOL-II 5.3 <- ADD-01 5.1 <- ADD-03 5.2, blind rehearsal 04)
                ok, why, flowed = self._flow(op, st)
                if not check("C22", ok, why):
                    return r
                if flowed:                            # (nothing flowed: the op is exactly what it was before s11)
                    r.details["flow"] = why
                    r.changed += [x["unit"] for x in flowed if x["unit"] not in r.changed]
                    r.details["flowed"] = flowed
                    r.details["also_in"] = [k for k in r.details.get("also_in", []) if k not in r.changed]
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
                                    None, parent=a.parent, label=f"after {a.label}", history=[op.id], issued_by=addendum,
                                    printed_in=addendum, inserted_after=op.anchor)
                num = re.search(r"\bnew (?:Clause|clause|Section|section|Paragraph|paragraph) (\d+(?:\.\d+)*[A-Z]?)\b"
                                r"[^.]{0,80}?\binserted\b", ptext)
                if num:                                  # session 11: the number later addenda cite it by
                    self.inserted_as[new_id] = f"{a.doc}:{num.group(1)}"
                    r.details["inserted_as"] = num.group(1)
                content.append(new_id)
                self.order.insert(self.order.index(op.anchor) + 1, new_id)
            r.changed, r.details["content"] = content, content
        return self._finish(op, r, run_on)

    # ------------------------------------------------------------------ session 12 helpers
    def _finish(self, op: Op, r: OpResult, run_on: list[str]) -> OpResult:
        """A valid op: the list items its quotation ran on into are content of it (C20)."""
        extra = [k for k in run_on if k != op.provision and k not in (r.details.get("content") or [])]
        if extra:
            r.details["content"] = list(r.details.get("content") or []) + extra
        r.valid = True
        return r

    def _inserted_targets(self, targets: list[str], st: dict[str, UState]) -> tuple[list[str], dict[str, str]]:
        """Targets named by the number an earlier op inserted them as ('VOL-II:5.6' -> 'VOL-II:5.5+ADD-03')."""
        by_number = {v: k for k, v in self.inserted_as.items() if k in st}
        out, resolved = [], {}
        for t in targets:
            if t not in st and not group_members(st, t) and t in by_number:
                resolved[t] = by_number[t]
                out.append(by_number[t])
            else:
                out.append(t)
        return out, resolved

    def _precedence(self, op: Op, targets: list[str], ptext: str, st: dict[str, UState], r: OpResult, check) -> bool:
        """Which of two renderings governs, as the provision says it; never decided here (session 12)."""
        p = op.precedence
        if p == "unstated":
            said = re.search(r"\b(?:govern(?:s|ing)?|prevail(?:s|ing)?|takes? precedence|is authoritative)\b", ptext, re.I)
            if not check("C21", said is None, "the provision states no precedence between the renderings" if said is None
                         else f"the provision states a precedence ('{_short_words(ptext[max(0, said.start() - 60):said.end() + 40], 160)}'):"
                              " quote its words instead of 'unstated'"):
                return False
            r.details["precedence"] = {"governs": "unstated", "over": list(targets), "stated_by": None,
                                       "flag": "the addendum does not say which rendering governs: a person decides "
                                               "(nothing is assumed)"}
            return True
        ok = p.governs in targets and bool(p.over) and all(o in targets and o != p.governs for o in p.over)
        if not check("C22", ok, f"{p.governs} governs {p.over}: both are targets of the op" if ok
                     else f"governs/over must be distinct targets of the op ({targets}); got {p.governs} over {p.over}"):
            return False
        if not check("C21", _quoted_in(ptext, p.words), f"the provision prints '{p.words}'" if _quoted_in(ptext, p.words)
                     else f"the provision does not print '{p.words}': the precedence must be the addendum's own words"):
            return False
        # the words name a language: the rendering they make govern must be in it (checked on the units' own letters)
        lang = "Arabic" if re.search(r"\bArabic\b", p.words, re.I) else "English" if re.search(r"\bEnglish\b", p.words, re.I) else None
        def arabic(g: str) -> bool:
            return any(has_arabic(st[k].text or "") for k in ([g] if g in st else []) + group_members(st, g) if k in st)
        if lang is not None:
            ok = arabic(p.governs) and not any(arabic(o) for o in p.over) if lang == "Arabic" else \
                not arabic(p.governs) and any(arabic(o) for o in p.over)
            if not check("C22", ok, f"'{p.words}' names the {lang} text: {p.governs} is in {lang}" if ok
                         else f"'{p.words}' names the {lang} text, but {p.governs} is not the {lang} rendering of {targets}"):
                return False
        r.details["precedence"] = {"governs": p.governs, "over": list(p.over), "words": p.words, "stated_by": op.provision}
        return True

    def _replace_span(self, op: Op, target: str, items: list[str], st: dict[str, UState], addendum: str,
                      prov: UState, r: OpResult, check) -> bool:
        """replace_text whose old words span a clause and its list items (module docstring, session 12)."""
        fam = [target] + items
        texts = [st[k].text for k in fam]
        joined = " ".join(texts)
        n = _contains(joined, op.old)
        if n != 1:
            check("C23", False, f"'{op.old}' occurs 0 time(s) in {target}; " + _span_break(fam, texts, op.old)
                  if n == 0 else f"'{op.old}' occurs {n} time(s) across {target} and its list items {items}")
            return False
        if len(_split_items(joined)) != len(fam):
            check("C22", False, f"{target} and its list items {items} cannot be re-split at their item letters; the "
                                "replacement is not applied (a person writes it)")
            return False
        new_joined = _replace_once(joined, op.old, op.new)
        if new_joined == joined:                       # typographic forms differ in length: work on the normalised text
            new_joined = _replace_once(normalize_latin(joined), normalize_latin(op.old), op.new)
        if not check("C24", _contains(new_joined, op.old) == _contains(op.new, op.old) and _contains(new_joined, op.new) >= 1,
                     "post-condition: old removed once, new present (across the clause and its list items)"):
            return False
        pieces = _split_items(new_joined)
        body, new_items = pieces[0], pieces[1:]

        def words(x: str) -> str:
            return normalize_latin(re.sub(r"^\(([a-z]{1,3})\)\s*", "", x)).lower()

        def letter(x: str) -> str | None:
            m = re.match(r"^\(([a-z]{1,3})\)", x.strip())
            return m.group(1) if m else None
        free, assigned = list(items), {}
        for i, x in enumerate(new_items):                       # 1. words unchanged: the same id (re-lettered)
            k = next((k for k in free if words(st[k].text) == words(x)), None)
            if k:
                assigned[i] = k
                free.remove(k)
        for i, x in enumerate(new_items):                       # 2. the item with the same letter, changed in place
            if i not in assigned:
                k = next((k for k in free if letter(st[k].text) == letter(x)), None)
                if k:
                    assigned[i] = k
                    free.remove(k)
        changed, after, prev_id = [], {}, target
        before = {k: st[k].text for k in fam}
        if st[target].text != body:
            st[target].text = body
            changed.append(target)
        for i, x in enumerate(new_items):
            k = assigned.get(i)
            if k is None:                                      # 3. a new item, printed in this addendum
                k = f"{target}({letter(x) or i + 1})"
                if k in st:
                    k = f"{k}+{addendum}"
                st[k] = UState(k, st[target].doc, "list_item", "active", x, None, list(prov.pages), "addendum_op", None,
                               parent=target, label=f"({letter(x)})" if letter(x) else None, issued_by=addendum,
                               printed_in=addendum, inserted_after=prev_id)
                self.order.insert(self.order.index(prev_id) + 1 if prev_id in self.order else len(self.order), k)
                changed.append(k)
            elif st[k].text != x:
                st[k].text = x
                changed.append(k)
            if letter(x) and letter(st[k].text) != letter(before.get(k, x)) and k in before:
                st[k].number = f"({letter(x)})"
            after[k] = x
            prev_id = k
        for k in free:                                         # an item the result no longer has
            st[k].status = "deleted"
            changed.append(k)
        for k in changed:
            st[k].history.append(op.id)
        if target not in changed:                              # the clause as a whole was amended
            st[target].history.append(op.id)
        r.changed = [target] + [k for k in changed if k != target]
        r.details["before"] = joined
        r.details["span"] = {"units_before": fam, "before": before, "after": {target: body, **after},
                             "deleted": list(free)}
        letters = [letter(x) for x in new_items]
        twice = sorted({x for x in letters if x and letters.count(x) > 1})
        if twice:                                             # said, never corrected: the addendum printed the letters
            r.details["lettering"] = (f"after {op.id} the list of {target} has more than one item lettered "
                                      f"{', '.join(f'({x})' for x in twice)}: the addendum does not re-letter it; a person "
                                      "checks the lettering")
        return True

    def _insert_row(self, op: Op, st: dict[str, UState], addendum: str, prov: UState, cite_text: str, r: OpResult,
                    check) -> OpResult:
        """insert_row (session 09): a row of a table that the provision describes in prose (module docstring)."""
        ptext = prov.text
        t = st.get(op.target or "")
        if not check("C22", t is not None and t.kind == "table" and t.status == "active",
                     f"target {op.target} is an active table" if t is not None and t.kind == "table" and t.status == "active"
                     else f"target {op.target} is not an active table"):
            return r
        header = lambda u: [c.strip() for c in (u.text or "").split("|") if c.strip()]  # noqa: E731
        cols = header(t)
        ok, why, cited = verify_target(op.target, cite_text, set(st), lambda uid: st[uid].label if uid in st else None)
        if not ok:                                   # "the Index of Forms in Volume IV": the volume's one index table
            index = [c for c in citations(cite_text) if c.kind == "index" and c.target == f"{t.doc}:index"]
            tables = [k for k, u in st.items() if u.doc == t.doc and u.kind == "table" and u.status == "active"
                      and is_index_table(header(u))]
            if index:
                ok = tables == [op.target]
                why = (f"the provision cites '{index[0].text}': {op.target} is the {t.doc} table whose first column is "
                       "'Form' and which has a 'Title' column" if ok else
                       f"the provision cites '{index[0].text}', but the index tables of {t.doc} are {tables}")
        r.details["cited"] = cited
        if not check("C22", ok, why):
            return r
        cells = {k: str(v) for k, v in (op.cells or {}).items()}
        unknown = [c for c in cells if c not in cols]
        ok = bool(cells) and not unknown and bool(cols) and cols[0] in cells
        if not check("C22", ok, f"every column is in the header of {op.target} ({' | '.join(cols)}) and the key column "
                     f"'{cols[0]}' is given" if ok else f"the new row's columns {sorted(cells)} are not those of {op.target} "
                     f"({' | '.join(cols)}): unknown {unknown}; the key column '{cols[0] if cols else '?'}' must be given"):
            return r
        members = [k for k in self.order if k in st and st[k].parent == op.target and st[k].kind == "table_row"]
        if op.after is not None:
            named, a = after_row(ptext), st.get(op.after)
            ok = a is not None and op.after in members and a.status == "active" and named is not None and \
                slug(named) in {slug(a.label or ""), slug(op.after.rsplit("/", 1)[-1])}
            if not check("C22", ok, f"{op.after} is the row the provision inserts after ('{named}')" if ok else
                         f"{op.after} is not a row of {op.target} that the provision names as the one to follow "
                         f"(the provision names {named!r})"):
                return r
        key = cells[cols[0]] if cols[0] in ("No", "Ref", "Form", "Item") else slug(cells[cols[0]])  # as Stage 1 keys rows
        new_id = f"{op.target}/{key}+{addendum}"
        taken = [k for k in members if st[k].status == "active" and slug(st[k].label or "") == slug(key)]
        if not check("C22", not taken and new_id not in st, f"{op.target} has no row keyed '{key}' yet" if not taken
                     and new_id not in st else f"{op.target} already has a row keyed '{key}': {taken or [new_id]}"):
            return r
        unstated = [f"{c}: {v}" for c, v in cells.items() if v and not _states_cell(ptext, c, v)]
        if not check("C21", not unstated, "every cell is printed in the provision after its column's name" if not unstated
                     else f"cells not printed in the provision after their column's name: {unstated}"):
            return r
        row = {c: cells[c] for c in cols if c in cells}                    # in the header's order, as the siblings
        after = op.after or (members[-1] if members else op.target)
        st[new_id] = UState(new_id, t.doc, "table_row", "active", " | ".join(f"{c}: {v}" for c, v in row.items() if v),
                            row, list(prov.pages), "addendum_op", None, parent=op.target, label=key, history=[op.id],
                            issued_by=addendum, printed_in=addendum, inserted_after=after)
        self.order.insert(self.order.index(after) + 1, new_id)
        r.changed = [new_id]
        r.details.update({"inserted": new_id, "after": after, "cells": row})
        r.valid = True
        return r

    def _op_provision(self, op_id: str) -> str:
        for f in self.opfiles:
            for o in f.ops:
                if o.id == op_id:
                    return o.provision
        return ""

    def _flow(self, op: Op, st: dict[str, UState]) -> tuple[bool, str, list[dict]]:
        """A replace_text on an earlier addendum's unit (session 11). When that unit is the provision of ops applied at
        earlier stages that wrote words into other units (append_text / replace_text `new`, a reinstatement's or an
        inserted item's `new_text`), and `old` is inside those words exactly once, the same change is made inside them
        in every unit those ops wrote into (each such unit must still hold the words exactly once). Returns (ok, why,
        [{unit, via, via_provision, before, after, inserted_before, inserted_after}]). The earlier stages' states are
        copies and are never touched: the historical state is not rewritten."""
        wrote = []
        for x in self._applied_before:
            if x.op.provision != op.target:
                continue
            words = x.op.new if x.op.type in ("append_text", "replace_text") else (
                x.op.new_text if x.op.type in ("set_status", "insert_unit") else None)
            if words:
                wrote.append((x, words))
        if not wrote:
            return True, f"{op.target} wrote nothing into another unit: only its own words change", []
        flowed, why_not = [], []
        for x, words in wrote:
            if _contains(words, op.old) != 1:
                why_not.append(f"'{op.old[:60]}' is not once in the words {x.op.id} wrote")
                continue
            new_words = _replace_once(words, op.old, op.new)
            for k in x.changed:
                if k == op.target:
                    continue
                u = st.get(k)
                n = u.text.count(words) if u is not None else 0
                if u is None or u.status != "active" or n != 1:
                    return False, (f"the words {x.op.id} wrote into {k} are no longer there once as written ({n} "
                                   f"occurrence(s){'' if u is None else '; ' + u.status}): the change to {op.target} "
                                   "cannot flow to it; a person decides"), []
                before_old = _contains(u.text, op.old)
                after = u.text.replace(words, new_words, 1)
                if _contains(after, op.old) != before_old - 1 + _contains(op.new, op.old) or _contains(after, op.new) < 1:
                    return False, f"post-condition failed in {k} for the flowed change", []
                flowed.append({"unit": k, "via": x.op.id, "via_provision": x.op.provision, "before": u.text,
                               "after": after, "inserted_before": words, "inserted_after": new_words})
                u.text = after
                u.history.append(op.id)
        if not flowed:
            # words of the earlier addendum that its ops did not write anywhere (blind rehearsal 02: ADD-03 2.2 strikes
            # ADD-01 2.1's 'The time of 14:00 Riyadh time is unchanged.'): only that addendum's own unit changes
            return True, (f"only {op.target} changes: the amended words are not among those "
                          f"{', '.join(x.op.id for x, _ in wrote)} wrote into other units ({'; '.join(why_not)}), so "
                          "nothing flows (a re-targeting of the earlier amendment would need its own op)"), []
        return True, ("the change flows to " + ", ".join(f"{x['unit']} (written by {x['via']})" for x in flowed)
                      + f"; {op.target} itself is amended too"), flowed


def _names_column(provision_text: str, column: str) -> bool:
    return bool(column) and normalize_latin(column).lower() in normalize_latin(provision_text).lower()


def _states_cell(provision_text: str, column: str, value: str) -> bool:
    """A new row's cell printed in the provision right after its column's name: quoted ("Envelope 'A'", "the title
    'Cybersecurity Compliance Undertaking'") or, unquoted, as "<column> <value>" ("Form 4-G" for the Form cell 4-G)."""
    t = normalize_latin(provision_text)
    c, v = re.escape(normalize_latin(column)), re.escape(normalize_latin(value))
    return bool(re.search(r"\b" + c + r"\s+['\"]" + v + r"['\"]", t, re.I)
                or re.search(r"\b" + c + r"\s+" + v + r"(?![\w-])", t, re.I))


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
    if re.fullmatch(r"T\d+-\d+(?:-[A-Za-z0-9]+)?", local):
        # an addendum's issue of a table carries a suffix (ADD-02:T1-1-rev); its title still names "Table 1-1"
        phrase = "Table " + re.match(r"T(\d+-\d+)", local).group(1)
    elif re.fullmatch(r"F\d-[A-Z]", local):
        phrase = "Form " + local[1:]
    else:
        phrase = local
    return re.search(r"(?<![\w-])" + re.escape(phrase) + r"(?![\w-])", normalize_latin(title), re.I) is not None


def _also_in(st: dict[str, UState], target: str, words: str) -> list[str]:
    """Other active volume units with the same words (addenda quoting them are not targets)."""
    return [k for k, u in st.items() if u.status == "active" and k != target and not u.doc.startswith("ADD-")
            and _contains(u.text, words)]


def _letter_ranges(text: str) -> str:
    """Every item letter inside a printed range: 'items (g) to (j)' -> '(g) (h) (i) (j)' (session 08 blind rehearsal:
    a re-lettering is usually stated as a range, and each new letter is then stated without being printed)."""
    out = []
    for m in re.finditer(r"\(([a-z])\) to \(([a-z])\)", text):
        a, b = ord(m.group(1)), ord(m.group(2))
        if a < b <= a + 12:
            out += [f"({chr(c)})" for c in range(a, b + 1)]
    return " ".join(out)


def _arabic_span(text: str, old: str) -> tuple[int, int] | None:
    """(start, end) of the first run of `text` whose Arabic-normalised form equals that of `old`: a printed addendum
    and an image reading may differ in diacritics, tatweel or alef forms while saying the same words (session 09)."""
    target = normalize_arabic(old)
    if not target:
        return None
    pieces, idx = [], []
    for i, ch in enumerate(text):
        n = " " if ch.isspace() else normalize_arabic(ch)
        if not n or (n == " " and pieces and pieces[-1] == " "):
            continue
        for c in n:
            pieces.append(c)
            idx.append(i)
    k = "".join(pieces).find(target)
    return None if k < 0 else (idx[k], idx[k + len(target) - 1] + 1)


_ITEM_START = re.compile(r"(?:(?<=:)|(?<=;)|(?<=; and)|(?<=; or)|(?<=, and)|(?<=\.))\s+(?=\(([a-z]{1,3})\)\s)")


def _split_items(text: str) -> list[str]:
    """A clause's text split into its body and list items at item letters that follow a ':', ';', '; and', '; or' or
    '.', in sequence from (a) (an '(a)' inside a sentence that no '(b)' follows in sequence is not a list) (session 12)."""
    cuts, want, last = [], "a", None
    for m in _ITEM_START.finditer(text):
        if m.group(1) in (want, last):            # a repeated letter (an insertion the addendum did not re-letter) is kept
            cuts.append(m)
            last = m.group(1)
            want = chr(ord(last) + 1) if len(last) == 1 else last
    out, at = [], 0
    for m in cuts:
        out.append(text[at:m.start()].strip())
        at = m.end()
    out.append(text[at:].strip())
    return [x for x in out if x] if cuts else [text.strip()]


def _items_reached(texts: list[str], ids: list[str], quotes: list[str]) -> list[str]:
    """The units (a provision and its list items, in order) that the quotations reach when the units are read as one
    text; [] when a quotation is not in that text (session 12)."""
    norm = [normalize_latin(t).replace("'", "") for t in texts]
    joined = " ".join(norm)
    reached: set[int] = set()
    for q in quotes:
        i = joined.find(normalize_latin(q).replace("'", ""))
        if i < 0:
            return []
        j, off = i + len(normalize_latin(q).replace("'", "")), 0
        for n, t in enumerate(norm):
            if off < j and i < off + len(t):
                reached.add(n)
            off += len(t) + 1
    return [ids[n] for n in sorted(reached | {0})]


def _span_break(ids: list[str], texts: list[str], old: str) -> str:
    """Where a quotation stops matching a clause and its list items read as one text (session 12)."""
    norm = [normalize_latin(t) for t in texts]
    joined = " ".join(norm)
    w = normalize_latin(old).split()
    lo, hi = 0, len(w)
    while lo < hi:                                       # the longest leading run of the quotation's words found
        mid = (lo + hi + 1) // 2
        if " ".join(w[:mid]) in joined:
            lo = mid
        else:
            hi = mid - 1
    k = lo
    if k == 0:
        return f"read across {ids[0]} and its list items {ids[1:]}, no part of the quotation's start is found"

    def unit_at(pos: int) -> str:
        off = 0
        for uid, t in zip(ids, norm):
            if pos < off + len(t) + 1:
                return uid
            off += len(t) + 1
        return ids[-1]
    start = joined.find(" ".join(w[:k]))
    end = start + len(" ".join(w[:k]))
    return (f"read across {ids[0]} and its list items {ids[1:]}, the quotation matches from {unit_at(start)} as far "
            f"as '...{' '.join(w[max(0, k - 6):k])}' and breaks in {unit_at(min(end + 1, len(joined) - 1))} at "
            f"'{' '.join(w[k:k + 8])}' (the text there reads '{joined[end:end + 60].strip()}')")


def _replace_once(text: str, old: str, new: str) -> str:
    if old in text:
        return text.replace(old, new, 1)
    if has_arabic(old):
        span = _arabic_span(text, old)
        return text if span is None else text[:span[0]] + new + text[span[1]:]
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


_PRINTED_DATE = re.compile(r"\b(\d{1,2})\s+(" + "|".join(MONTHS) + r"),?\s+(\d{4})\b")


def _printed_dates(text: str) -> list[str]:
    """Every calendar date printed like '8 October 2026' in the text, as ISO strings (an impossible date is skipped)."""
    out = []
    for m in _PRINTED_DATE.finditer(normalize_latin(text or "")):
        try:
            out.append(date(int(m.group(3)), MONTHS.index(m.group(2)) + 1, int(m.group(1))).isoformat())
        except ValueError:
            continue
    return out


def _short_words(t, n: int) -> str:
    t = " ".join(str(t or "").split())
    return t if len(t) <= n else t[: n - 1] + "…"


def conditions_of(prev: StageResult | None, res: StageResult) -> list[dict]:
    """The conditional amendments in play at a stage (session 11): those stated by this stage's ops, then those stated
    earlier and still pending (carried with `stated_at`; their `if_triggered` texts are as computed then). Each:
    {op, condition, stated_at, provision, state (pending | triggered | not_triggered | invalid), trigger, trigger_unit,
    applicability, deadline (a DeadlineRule dict), if_not_triggered, affects, targets, if_triggered {unit: {before,
    after}}, fact}."""
    out = []
    for x in res.ops:
        if x.op.condition is None or x.withdrawn:
            continue
        cd = dict(x.details.get("conditional") or {})
        out.append({"op": x.op.id, "stated_at": res.stage, "provision": x.op.provision, "valid": x.valid, **cd})
    mine = {c["op"] for c in out}
    for c in (prev.conditions if prev is not None else []):
        if c["op"] not in mine and c.get("state") == "pending":
            out.append(dict(c))
    return out


def triggers_path(cfg: dict, root: Path) -> Path:
    """`triggers:` in the pack config, else curation/triggers.yaml (a pack without one has no recorded triggers)."""
    p = Path(cfg.get("triggers") or "curation/triggers.yaml")
    return p if p.is_absolute() else Path(root) / p


def load_triggers(path) -> dict[str, dict]:
    """The trigger facts a person recorded (session 11), {condition id: fact}; {} when the file does not exist.

        triggers:
          - condition: ADD-03/S7            the Condition.id of the conditional op(s)
            occurred: true | false          a person's finding; nothing is ever assumed
            date: 2026-11-10                when it occurred (or was established not to have occurred by the deadline)
            recorded_by: <a person>         never the program or a model
            evidence: [{source or unit, words}]   the notice that shows it
            note: ...
    The engine checks each record when it uses it (Engine._trigger_fact); a condition recorded twice raises."""
    p = Path(path)
    if not p.exists():
        return {}
    data = load_yaml(p) or {}
    out: dict[str, dict] = {}
    for f in data.get("triggers") or []:
        if not isinstance(f, dict) or not f.get("condition"):
            raise ValueError(f"{p}: every trigger record names its `condition`")
        if f["condition"] in out:
            raise ValueError(f"{p}: condition {f['condition']} recorded twice")
        f = dict(f)
        if hasattr(f.get("date"), "isoformat"):
            f["date"] = f["date"].isoformat()
        out[f["condition"]] = f
    return out


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
