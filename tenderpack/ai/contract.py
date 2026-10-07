"""The shared, typed contract for claims and change proposals (every route uses it: application adapters, a coding
host through MCP or the CLI, and offline recordings).

    StateIdentity   which tender state a proposal was made against: pack id, the evidence build's identity (the
                    sha256 of its BUILD_MANIFEST.json, which records every file the build wrote, crops included), the
                    validated and working stages, the sha256 of the decisions file and (session 10) of the other
                    inputs a proposal or a calculation depends on: the assumptions (calendar, holidays, counting
                    policy), the activity templates, the readings and approvals, the amendment files before the
                    working stage, and any crop the manifest does not record. A proposal made against another state
                    is STALE: every item is invalid. `fingerprint()` is what a calculation states it was computed
                    under.
    EvidenceRef     one exact supporting quotation: document, unit, page, kind (span | cell | crop | reading), the
                    words verbatim, the cell for a table cell, the crop's sha256 for a crop.
    Statement       a fact, an assumption or an interpretation, each with its own evidence; the three kinds are kept
                    apart and never merged. An item that depends on an interpretation (or an assumption) is at best
                    `interpretation_pending`: a verbatim quotation or a well-formed JSON never verifies one.
    ChangeProposal  one proposed change: its statement type, the addendum provision it answers, the target, the
                    payload (an amend.Op for amendment_op, an amend.Disposition for disposition, a row reading, a new
                    row, an issue, a clarification, or an escalation {why, what_is_unsupported}), previous and
                    proposed values, evidence, dependencies, conflicts and missing information.
                    `validation` and `verification_status` are CONTROLLER-WRITTEN: a value supplied by a model is
                    overwritten and the overwrite is logged. `model_rationale` is never read by code.
    ProposalSet     one run: route, provider, the model requested and the model the endpoint reported, the task,
                    the addendum, the state, statements, items, provision coverage, resolution (session 10: per
                    provision resolved / pending / invalid / unaccounted, apart from coverage; approval is never
                    assigned), usage (cost null when no price is configured), status and the controller version.

Session 14 (W1): `payload_schemas()` gives the FULL payload shapes (register.Row / register.Interp inlined); an item's
`ready` / `blocked_by` are controller-written (controller.readiness); payload_errors / submission_problems /
merge_repair serve the bounded repair of invalid inner payloads (see the section at the end).

`model_fill_schema()` is the JSON schema given to the model: ProposalSet.model_json_schema() trimmed to the fields
the model fills (controller-written fields removed). Parsing (controller.parse_model_output) accepts the full item
model so that a model-supplied status is caught and overwritten rather than silently dropped.
"""
from __future__ import annotations

import copy
import hashlib
import json
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

CONTROLLER_VERSION = "s10-ai-1"     # s10: inputs bound to the state identity; semantic resolution apart from coverage

STATEMENT_TYPES = ("amendment_op", "disposition", "row_reading", "row_new", "issue", "clarification", "escalation")
VERIFICATION = ("unverified", "evidence_verified", "insufficient_evidence", "invalid", "conflicting", "escalated",
                "interpretation_pending")
SET_STATUS = ("complete", "partial", "malformed", "provider_failed", "budget_exhausted", "stale",
              "deferred")                   # s11: a rate limit outlasted the bounded backoff (requests.py)

# fields of a ProposalSet / ChangeProposal that only the controller writes
CONTROLLER_SET_FIELDS = ("run_id", "created", "route", "provider", "model_requested", "model_reported", "task",
                         "coverage", "resolution", "usage", "status", "controller_version")
CONTROLLER_ITEM_FIELDS = ("validation", "verification_status",
                          "ready", "blocked_by")        # session 14 (W1): readiness, controller-written


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class StateIdentity(_Strict):
    pack_id: str
    evidence_build_id: str = Field(description="sha256 of the evidence build's BUILD_MANIFEST.json")
    validated_stage: str
    working_stage: str | None = None
    decisions_sha256: str | None = Field(None, description="sha256 of the decisions file; null when there is none")
    # session 10: the other inputs a proposal or a calculation depends on (null in a state written before session 10,
    # which therefore never matches a current one)
    assumptions_sha256: str | None = Field(None, description="sha256 of the assumptions file (calendar, holidays, "
                                                             "counting policy, durations)")
    activity_templates_sha256: str | None = Field(None, description="sha256 of the activity templates file")
    readings_sha256: str | None = Field(None, description="one sha256 over the approvals file and the reading files")
    amendments_sha256: str | None = Field(None, description="one sha256 over the amendment files of the addenda before "
                                                            "the working stage (all of them when there is none)")
    unrecorded_crops_sha256: str | None = Field(None, description="one sha256 over the image crops the units name that "
                                                                  "BUILD_MANIFEST.json does not record; null when it "
                                                                  "records every one")
    # session 11 (D1): the curated inputs the register reads; a proposal made before any of them changed is STALE
    register_sha256: str | None = Field(None, description="one sha256 over the register: rows.yaml, every row file its "
                                                          "`include` names and the machine-written pins.yaml")
    relationships_sha256: str | None = Field(None, description="sha256 of the relationships file the pack reads; null "
                                                               "when there is none")
    curation_sha256: str | None = Field(None, description="one sha256 over the other curated inputs the pack names: "
                                                          "the issues (and per-document issue files), the dispositions, "
                                                          "the evidence items, the clarification register, the row-id "
                                                          "ledger, the scenarios, the recorded trigger facts and the "
                                                          "approved-formula registry")
    # session 12 (consecutive addenda): a run started on another run's candidate (`--base-run`) depends on that
    # candidate too; a change there makes the run's sets STALE as any other input would (null without a base run)
    base_run: str | None = Field(None, description="the run whose candidate this state starts from (`--base-run`); "
                                                   "null when it starts from the real curation")
    base_candidate_sha256: str | None = Field(None, description="one sha256 over the base run's candidate as it is now "
                                                                "(its pack, every curated file it names and its "
                                                                "evidence build's BUILD_MANIFEST.json); null without a "
                                                                "base run")

    def fingerprint(self) -> str:
        """sha256 of the whole identity: what a calculation or a simulation states it was computed under."""
        return hashlib.sha256(json.dumps(self.model_dump(), sort_keys=True).encode("utf-8")).hexdigest()


class CellRef(_Strict):
    row_key: str
    column: str


class EvidenceRef(_Strict):
    doc: str
    unit_id: str
    page: int
    kind: Literal["span", "cell", "crop", "reading"]
    words: str = Field(description="the exact words, verbatim, as printed in the unit (or the cell) at the stated "
                                   "state; for an image reading, the SOURCE text (Arabic as printed), never the "
                                   "translation")
    cell: CellRef | None = None
    crop_sha256: str | None = None


class Statement(_Strict):
    id: str
    kind: Literal["fact", "assumption", "interpretation"]
    text: str
    evidence: list[EvidenceRef] = Field(default_factory=list)
    note: str | None = None


class ValidationRecord(_Strict):
    check: str
    ok: bool
    detail: str
    aspect: Literal["structure", "state", "evidence", "engine", "semantic", "decision"] | None = Field(
        None, description="what the check is about, kept apart: evidence (quotations verbatim at the stated place), "
                          "semantic (the item is consistent with what the provision's own words do), engine (C21-C27, "
                          "C47, values), decision (named decisions and approvals), structure, state")


class EscalationPayload(_Strict):
    why: str
    what_is_unsupported: str


class IssuePayload(_Strict):
    text: str
    owner: str | None = None
    short: str | None = None
    theme: str | None = None


class ClarificationPayload(_Strict):
    gap: str
    proposed_question: str
    practical_impact: str | None = None
    interim_handling: str | None = None
    decision_owner: str | None = None


class ReplaceRequirement(_Strict):
    """Session 12 (blind-06 follow-up 3): the shape of a requirement correction, stated in the packet schema."""
    old: str = Field(description="the row's CURRENT requirement text, verbatim (the validator compares it)")
    new: str = Field(description="the corrected requirement text (non-empty)")


class RowReadingPayload(_Strict):
    row: str = Field(description="an existing A1 row id")
    interpretation: dict = Field(description="register.Interp fields: stage, quote, parameters, consequence, note "
                                             "(no pins: pins are machine-written)")
    replace_requirement: ReplaceRequirement | None = Field(
        None, description="only when the row's requirement text itself must change: {old: its current text verbatim, "
                          "new: the corrected text}; omit it when the reading re-states the same requirement")


class RowNewPayload(_Strict):
    row: dict = Field(description="register.Row fields (id, group, scope, requirement, units, discipline, "
                                  "assessment, evidence, interpretations, confidence, confidence_reason, ...)")


class ChangeProposal(_Strict):
    id: str
    state: StateIdentity
    statement_type: Literal["amendment_op", "disposition", "row_reading", "row_new", "issue", "clarification",
                            "escalation"]
    provision: str = Field(description="unit id of the addendum provision this item answers")
    target: str | None = Field(None, description="unit id (or group id) the item changes or concerns")
    payload: dict = Field(description="amendment_op: an amend.Op; disposition: an amend.Disposition; row_reading: "
                                      "{row, interpretation}; row_new: {row}; issue: {text, owner, short, theme}; "
                                      "clarification: {gap, proposed_question, practical_impact, interim_handling, "
                                      "decision_owner}; escalation: {why, what_is_unsupported}")
    previous_value: str | int | float | None = Field(None, description="the value as it stands in the current state")
    proposed_value: str | int | float | None = None
    evidence: list[EvidenceRef] = Field(default_factory=list)
    # session 14 (W1): the typed id space of the set (blind-07 defect 3): units and groups, A1 rows, recorded ops, and
    # the ids of this set's own items (ops, dispositions, escalations, rows, issues, questions) and statements
    dependencies: list[str] = Field(default_factory=list, description=(
        "ids this item relies on: units or groups, existing A1 rows or ops, or the ids of this set's own items (an op, a "
        "disposition, an escalation, a row, an issue, a question) or statements. A change (op or disposition) may not "
        "rely on an issue or a question; a cycle is refused"))
    conflicts: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    statements: list[str] = Field(default_factory=list, description="ids of the statements this item depends on")
    validation: list[ValidationRecord] = Field(default_factory=list, description="controller-written")
    verification_status: Literal["unverified", "evidence_verified", "insufficient_evidence", "invalid", "conflicting",
                                 "escalated", "interpretation_pending"] = Field("unverified",
                                                                               description="controller-written")
    model_rationale: str | None = Field(None, description="free text; never read by code")
    # session 14 (W1): controller-written readiness. `ready` is true when every item of the set this one relies on
    # (its dependencies and statements) is promotable and ready itself; `blocked_by` names each blocker with the reason
    # ("blocked by failed statement S2: ...", "depends on X (escalated)"). Null/empty before validation.
    ready: bool | None = Field(None, description="controller-written")
    blocked_by: list[str] = Field(default_factory=list, description="controller-written")


class Coverage(_Strict):
    provisions_total: int = 0
    accounted: int = 0
    unaccounted: list[str] = Field(default_factory=list)


class Resolution(_Strict):
    """Semantic resolution per provision of the addendum, kept apart from coverage (accounted for), evidence verification
    (verbatim quotations) and approval. Each provision is exactly one of: resolved (every answer to it is
    evidence_verified, consistent with what its own words do, and decides it), pending (answered, but a person must
    still decide: interpretation_pending, insufficient_evidence, conflicting, escalated, or an `unresolved`
    disposition), invalid (an answer to it is invalid, e.g. a no_effect that contradicts a substitution it prints; an
    invalid answer accounts for nothing) or unaccounted (no answer)."""
    provisions_total: int = 0
    accounted: int = 0
    resolved: int = 0
    pending: int = 0
    invalid: int = 0
    unaccounted: int = 0
    pending_provisions: list[str] = Field(default_factory=list)
    invalid_provisions: list[str] = Field(default_factory=list)
    no_change_on_amendment_language: list[str] = Field(
        default_factory=list, description="provisions answered 'no change' (a no_effect disposition, or an annotation "
                                          "that changes nothing) whose own words amend, oblige or except")
    approved: int = Field(0, description="always 0: approval is a named person's decision, recorded in curation; the "
                                         "controller never assigns it")


class Usage(_Strict):
    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float | None = None
    cost_basis: str = "no price configured"


class ProposalSet(_Strict):
    run_id: str
    created: str
    route: str
    provider: str
    model_requested: str
    model_reported: str | None = None
    task: str
    addendum: str
    state: StateIdentity
    statements: list[Statement] = Field(default_factory=list)
    items: list[ChangeProposal] = Field(default_factory=list)
    coverage: Coverage = Field(default_factory=Coverage)
    resolution: Resolution = Field(default_factory=Resolution)
    usage: Usage = Field(default_factory=Usage)
    status: Literal["complete", "partial", "malformed", "provider_failed", "budget_exhausted", "stale",
                    "deferred"] = "partial"
    controller_version: str = CONTROLLER_VERSION


def _strip_props(schema: dict, name: str, fields) -> None:
    node = schema if name is None else schema.get("$defs", {}).get(name)
    if not node:
        return
    for f in fields:
        node.get("properties", {}).pop(f, None)
        if f in node.get("required", []):
            node["required"].remove(f)


def model_fill_schema() -> dict:
    """ProposalSet.model_json_schema() trimmed to what the model fills: the controller-written set fields
    (run id, route, usage, coverage, status, ...) and item fields (validation, verification_status) are removed."""
    s = copy.deepcopy(ProposalSet.model_json_schema())
    _strip_props(s, None, CONTROLLER_SET_FIELDS)
    _strip_props(s, "ChangeProposal", CONTROLLER_ITEM_FIELDS)
    s.get("$defs", {}).pop("Coverage", None)
    s.get("$defs", {}).pop("Resolution", None)
    s.get("$defs", {}).pop("Usage", None)
    s.get("$defs", {}).pop("ValidationRecord", None)
    s["title"] = "ProposalSet (fields the proposer fills)"
    s["description"] = ("Return exactly one JSON object of this shape. verification_status and validation are written "
                        "by the controller; any value you supply is overwritten.")
    return s


def payload_schemas() -> dict:
    """The payload shapes per statement type (amend.Op and amend.Disposition come from the amendment engine). Session 14
    (W1, blind-07 defect 1): the FULL shapes, so that a model never guesses: row_new's `row` is the register.Row schema
    and row_reading's `interpretation` the register.Interp schema, their nested models (Consequence, RuleDef, ...) in
    `$defs` (one self-contained schema per type: compact_shared lifts the `$defs` once)."""
    return {t: payload_schema(t) for t in STATEMENT_TYPES}


def _inline_model(base: dict, prop: str, model) -> dict:
    """`base` (a pydantic JSON schema) with property `prop` replaced by a reference to `model`'s full schema."""
    s = copy.deepcopy(base)
    m = copy.deepcopy(model.model_json_schema())
    defs = {**s.pop("$defs", {}), **m.pop("$defs", {}), model.__name__: m}
    desc = (s.get("properties", {}).get(prop) or {}).get("description")
    s.setdefault("properties", {})[prop] = {"$ref": f"#/$defs/{model.__name__}",
                                            **({"description": desc} if desc else {})}
    s["$defs"] = defs
    return s


def payload_schema(statement_type: str) -> dict:
    """Session 14 (W1): the full JSON schema of one statement type's payload (what payload_errors checks)."""
    from ..amend import Disposition, Op
    from ..register import Interp, Row
    if statement_type not in STATEMENT_TYPES:
        raise ValueError(f"no statement type {statement_type!r} ({', '.join(STATEMENT_TYPES)})")
    return {"amendment_op": lambda: Op.model_json_schema(), "disposition": lambda: Disposition.model_json_schema(),
            "row_reading": lambda: _inline_model(RowReadingPayload.model_json_schema(), "interpretation", Interp),
            "row_new": lambda: _inline_model(RowNewPayload.model_json_schema(), "row", Row),
            "issue": lambda: IssuePayload.model_json_schema(),
            "clarification": lambda: ClarificationPayload.model_json_schema(),
            "escalation": lambda: EscalationPayload.model_json_schema()}[statement_type]()


# ---------------------------------------------------------------------------------------------- critic review (s10, W4)
# Appended by the routes layer (session 10). An item's `review.critic` is written ONLY by tenderpack.ai.critic: a
# second, independent model pass over selected items (removals, conflicts, interpretations with a consequence, uncertain
# targets). It never changes a verification status: agreement between models is not approval. It is a
# controller-written field: it is not in the schema a proposer sees, and a value a proposer supplies is dropped when the
# set is parsed and recorded as an overwrite (controller.parse_set).

class CriticReview(_Strict):
    agrees: bool
    concerns: list[str] = Field(default_factory=list)
    evidence_checked: list[str] = Field(default_factory=list, description="unit ids (or quotations) the critic checked")
    selected_because: list[str] = Field(default_factory=list, description="why the item was sent to the critic")
    route: str
    model_requested: str | None = None
    model_reported: str | None = None
    critic_run: str | None = None
    created: str | None = None
    note: str = "a second model's opinion: agreement between models is not approval, and it changes no status"


class ItemReview(_Strict):
    critic: CriticReview | None = None


if "review" not in CONTROLLER_ITEM_FIELDS:
    CONTROLLER_ITEM_FIELDS = (*CONTROLLER_ITEM_FIELDS, "review")

if "review" not in ChangeProposal.model_fields:      # a no-op once the field is declared in the class body above
    from pydantic.fields import FieldInfo as _FieldInfo
    ChangeProposal.__annotations__["review"] = "ItemReview | None"
    ChangeProposal.model_fields["review"] = _FieldInfo.from_annotated_attribute(
        ItemReview | None, Field(None, description="controller-written: the independent critic's review"))
    ChangeProposal.model_rebuild(force=True, _types_namespace={"ItemReview": ItemReview})
    ProposalSet.model_rebuild(force=True)

_model_fill_schema_without_review = model_fill_schema


def model_fill_schema() -> dict:  # noqa: F811 (the review is controller-written: not in the proposer's schema)
    s = _model_fill_schema_without_review()
    _strip_props(s, "ChangeProposal", ("review",))
    for k in ("CriticReview", "ItemReview"):
        s.get("$defs", {}).pop(k, None)
    return s


# ---------------------------------------------------------------------------------------------- downstream (s10, W3)
# Appended by the workflow (session 10; tenderpack/ai/workflow.py, validated by tenderpack/ai/downstream.py). After the
# amendment ops of an addendum are validated, a second analysis phase proposes the downstream work a curator otherwise
# writes by hand: re-made row readings, new register rows, issues, draft clarification questions (never sent), evidence
# items, A5 activities (their durations are PROVISIONAL ASSUMPTIONS) and relationships between rows, activities and
# calculations (they land only as `proposed`). A DownstreamItem answers one downstream TASK of the packet (a row whose
# cited units changed, an obligation without a row (C46), a clarification entry citing a changed unit, an A5 activity
# needing a changed row, an escalated provision). Statuses use the controller's vocabulary and are written by
# downstream.py only; a row, a reading, an activity or a relationship is never above `interpretation_pending`.

DOWNSTREAM_TASK = "propose_downstream"
DOWNSTREAM_TYPES = ("row_reading", "row_new", "issue", "clarification_item", "evidence_item", "activity", "dependency",
                    "escalation", "no_change")


class NoChangePayload(_Strict):
    """Session 11 (D1): the answer to a downstream task that needs nothing (an activity or a clarification entry the
    change does not affect), with its verbatim evidence. Never for a row task (a STALE row's reading is re-made) or an
    obligation without a row (C46). At most `interpretation_pending`: a person confirms that nothing changes."""
    why: str


class IssueItemPayload(_Strict):
    """Session 12: an issue is a matter kept open for people; a proposal never changes an existing issue (a new id only,
    no status or resolution field) and is at most `interpretation_pending`, shown HUMAN DECISION PENDING."""
    id: str = Field(description="a NEW issue id, I-... (an existing issue is never changed, closed or resolved by a "
                                "proposal; there is no status or resolution field)")
    text: str
    owner: str
    theme: str
    short: str | None = None
    a3: str | None = Field(None, description="the A3 wording, when the issue belongs on the one-page sheet")
    show_in_a3: bool = False


class ClarificationItemPayload(_Strict):
    """Session 12: a proposal never changes a question's response status (new or existing id): the controller keeps the
    register's status (a new entry is 'draft, not sent'); whether a question is answered or withdrawn is a person's
    decision. An addendum unit that responds to the question may be quoted as `answer: {unit, page, words}`: it is kept
    as `recorded_answer` ("answer recorded; whether it resolves the question is a human decision"), never applied."""
    entry: dict = Field(description="one entry of the clarification register in its own shape: id (CQ-...), kind, "
                                    "volume, clause, page, units, sources [{unit, page, words}], gap, already_settled, "
                                    "practical_impact, proposed_question, interim_handling, decision_owner, "
                                    "response_status ('draft, not sent'), linked_issues, theme. A DRAFT: never sent. "
                                    "You may NOT set response_status to 'answered by addendum' or 'withdrawn (not "
                                    "sent)', for a new or an existing id: the register's status is kept. You MAY quote "
                                    "the addendum words that respond to an existing question as answer: {unit, page, "
                                    "words}; it is recorded, not applied: a person decides whether it resolves it")


class EvidenceItemPayload(_Strict):
    id: str = Field(description="a new evidence item id, EV-...")
    item: dict = Field(description="tenderpack.evidence.EvidenceItem fields: name, envelope (A | B | A+B | none), "
                                   "issuer, per, source (the units requiring it), counted, note")


class LeadTimeAssumption(_Strict):
    key: str
    value: int = Field(description="Working Days (a PROVISIONAL ASSUMPTION; the pack states no such duration)")
    basis: str = Field(description="starts with 'PROVISIONAL ASSUMPTION:'")
    owner: str
    effort_wd: float | None = None
    waiting_on: str | None = None
    effort_basis: str | None = None


class ActivityPayload(_Strict):
    evidence_item: str = Field(description="the evidence item (EV-...) the activity is listed under in the templates")
    activity: dict = Field(description="an activity template entry: id, name, owner, discipline, resource, issuer, "
                                       "duration (a lead-time assumption key), per, predecessors, successors, item, "
                                       "condition, finish, gated_by. An existing id replaces that entry")
    rows: list[str] = Field(description="the A1 rows (existing or proposed in this set) that need it")
    duration_assumption: LeadTimeAssumption | None = Field(None, description="a NEW lead-time assumption when "
                                                                             "`duration` names none that exists")
    duration_label: Literal["PROVISIONAL ASSUMPTION"] = "PROVISIONAL ASSUMPTION"


class DependencyPayload(_Strict):
    """One entry of the relationships file (tenderpack.relationships), as a model may propose it: it lands only as
    `proposed` (or `possible`) through relationships.append_proposed; a model never confirms a link."""
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    from_: str | list[str] = Field(alias="from", description="a row id, a unit id (a table or form id stands for its "
                                                             "members), calc:<name>, or words:<phrase>")
    to: str | list[str] = Field(description="a row id, a unit id, an A5 activity id, an evidence item id, a date rule "
                                            "id, or calc:<name>")
    kind: Literal["cites", "depends_on", "feeds_calculation", "member_scope", "limit_applies", "missing_document"]
    basis: str = Field(description="why the link is believed, citing the item's evidence")
    note: str | None = None
    issues: list[str] = Field(default_factory=list)
    document: str | None = Field(None, description="missing_document only: the document the pack does not supply")
    document_id: str | None = None
    blocks: str | None = Field(None, description="missing_document only: the conclusion it prevents")
    status: Literal["proposed", "possible"] = Field("proposed", description="proposed or possible: an inferred link is "
                                                                           "never confirmed by a model")


class DownstreamItem(_Strict):
    id: str
    state: StateIdentity
    statement_type: Literal["row_reading", "row_new", "issue", "clarification_item", "evidence_item", "activity",
                            "dependency", "escalation", "no_change"]
    task: str = Field(description="the id of the downstream task in the packet this item answers")
    provision: str | None = Field(None, description="the addendum provision whose change the item follows")
    target: str | None = None
    payload: dict = Field(description="row_reading: {row, interpretation, replace_requirement: {old, new} when the requirement text changes}; row_new: {row}; "
                                      "issue: IssueItemPayload; clarification_item: {entry}; evidence_item: {id, "
                                      "item}; activity: ActivityPayload; dependency: DependencyPayload; escalation: "
                                      "{why, what_is_unsupported}; no_change: {why}")
    evidence: list[EvidenceRef] = Field(default_factory=list, description="at least one verbatim quotation, an "
                                        "escalation included (from units_after or the addendum's own text)")
    dependencies: list[str] = Field(default_factory=list, description="ids of rows, items, activities it relies on")
    conflicts: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    statements: list[str] = Field(default_factory=list, description="ids of entries of the set's `statements` "
                                                                  "this item depends on (ids only, never free text)")
    validation: list[ValidationRecord] = Field(default_factory=list, description="controller-written")
    verification_status: Literal["unverified", "evidence_verified", "insufficient_evidence", "invalid", "conflicting",
                                 "escalated", "interpretation_pending"] = Field("unverified",
                                                                               description="controller-written")
    model_rationale: str | None = Field(None, description="free text; never read by code")


class DownstreamSet(_Strict):
    run_id: str
    created: str
    route: str
    provider: str
    model_requested: str
    model_reported: str | None = None
    task: str = DOWNSTREAM_TASK
    addendum: str
    state: StateIdentity
    statements: list[Statement] = Field(default_factory=list)
    items: list[DownstreamItem] = Field(default_factory=list)
    usage: Usage = Field(default_factory=Usage)
    status: Literal["complete", "partial", "malformed", "provider_failed", "budget_exhausted", "stale"] = "partial"
    controller_version: str = CONTROLLER_VERSION


DOWNSTREAM_MODEL_FIELDS = ("addendum", "state", "statements", "items")


def downstream_fill_schema() -> dict:
    """DownstreamSet.model_json_schema() trimmed to what the proposer fills (as model_fill_schema)."""
    s = copy.deepcopy(DownstreamSet.model_json_schema())
    _strip_props(s, None, CONTROLLER_SET_FIELDS)
    _strip_props(s, "DownstreamItem", ("validation", "verification_status"))
    for k in ("Usage", "ValidationRecord"):
        s.get("$defs", {}).pop(k, None)
    s["title"] = "DownstreamSet (fields the proposer fills)"
    s["description"] = ("Return exactly one JSON object of this shape. verification_status and validation are written "
                        "by the controller; any value you supply is overwritten.")
    return s


def downstream_payload_schemas() -> dict:
    """The payload shapes per downstream statement type (register.Row / register.Interp come from the register)."""
    from ..evidence import EvidenceItem
    from ..register import Interp, Row
    return {"row_reading": {**RowReadingPayload.model_json_schema(), "interpretation_schema": Interp.model_json_schema()},
            "row_new": {**RowNewPayload.model_json_schema(), "row_schema": Row.model_json_schema()},
            "issue": IssueItemPayload.model_json_schema(), "clarification_item": ClarificationItemPayload.model_json_schema(),
            "evidence_item": {**EvidenceItemPayload.model_json_schema(), "item_schema": EvidenceItem.model_json_schema()},
            "activity": ActivityPayload.model_json_schema(), "dependency": DependencyPayload.model_json_schema(),
            "escalation": EscalationPayload.model_json_schema(), "no_change": NoChangePayload.model_json_schema()}


# ---------------------------------------------------------------------------------------------- region readings (s10)
# Appended by the workflow (session 10, readings step; tenderpack/ai/regionread.py). An addendum page that carries an
# image with no text layer cannot be ingested until the region has a reading (C05). A proposer (a host session over the
# MCP tools get_region / validate_reading, a recorded cassette or an API route) PROPOSES one: `reading` is a
# tenderpack.readings.Reading in the exact shape of the pack's own readings (curation/readings/*.yaml). The controller
# validates it with readings.check_reading; a reading is an interpretation of an image, so its status is at most
# `interpretation_pending`; `prepared_by` is written by the controller (AI-assisted, the session and the run); it is
# written to the CANDIDATE's readings only, PENDING HUMAN REVIEW, and never approved.

READING_TASK = "propose_region_reading"
READING_MODEL_FIELDS = ("region_id", "reading", "model_rationale")


class RegionReadingProposal(_Strict):
    run_id: str
    created: str
    route: str
    provider: str
    model_requested: str
    model_reported: str | None = None
    task: str = READING_TASK
    region_id: str
    reading: dict = Field(description="a tenderpack.readings.Reading (region_id, unit_id, title, source, content_type, "
                                      "languages, prepared_by, method, table | blocks | description, uncertainties): "
                                      "`source` is the packet's `state`; text as printed, translations separate")
    model_rationale: str | None = Field(None, description="free text; never read by code")
    validation: list[ValidationRecord] = Field(default_factory=list, description="controller-written")
    verification_status: Literal["unverified", "evidence_verified", "insufficient_evidence", "invalid", "conflicting",
                                 "escalated", "interpretation_pending"] = Field("unverified",
                                                                               description="controller-written")


def reading_fill_schema() -> dict:
    """The JSON schema of what a reading proposer fills: {region_id, reading, model_rationale}; the reading's own shape
    is tenderpack.readings.Reading (given beside it)."""
    from ..readings import Reading
    s = copy.deepcopy(RegionReadingProposal.model_json_schema())
    keep = set(READING_MODEL_FIELDS)
    s["properties"] = {k: v for k, v in s["properties"].items() if k in keep}
    s["required"] = [k for k in s.get("required", []) if k in keep]
    s.get("$defs", {}).pop("ValidationRecord", None)
    s["title"] = "RegionReadingProposal (fields the proposer fills)"
    s["description"] = "Return exactly one JSON object of this shape; `reading` follows reading_schema."
    return {"proposal": s, "reading_schema": Reading.model_json_schema()}


# ---------------------------------------------------------------------------------------------- inner payloads (s14, W1)
# Session 14 (W1; blind-07 defects 1 and 5). An item's envelope (ChangeProposal) can be well formed while its inner
# payload is not: every blind-07 analysis `row_new` failed the register.Row schema (a consequence given as a string,
# `scope` as a string, `discipline` / `confidence` / `confidence_reason` missing) and none was repaired. These checks
# give the EXACT errors of an inner payload (the same models the controller validates with), so the request layer
# (requests.check: the bounded re-ask) and the host route's submission gate (mcp_server: one bounded re-submission of
# the failing items only) can ask for that item again with its errors and its full schema (payload_schema), while
# the valid siblings of the set are kept as first given. A payload still invalid after the bound stays in the set and
# the controller marks it `invalid` with these errors. A `fact` with empty evidence is refused the same way: a summary
# or a paraphrase is not a fact (one such "fact" sank twelve blind-07 items).

def _errors(e, prefix: str = "") -> list[str]:
    out = []
    for x in e.errors():
        loc = ".".join(str(p) for p in x.get("loc") or ())
        got = "" if x.get("type") == "missing" else f" (got {json.dumps(x.get('input'), ensure_ascii=False, default=str)[:80]})"
        out.append(f"{prefix}{loc}: {x.get('msg')}{got}")
    return list(dict.fromkeys(out))


def payload_errors(statement_type: str, payload, provision: str | None = None, item_id: str | None = None) -> list[str]:
    """The exact validation errors of an analysis item's inner payload ([] when it is well formed): amend.Op,
    amend.Disposition, the row payloads with the full register.Row / register.Interp models, and the other payloads."""
    from pydantic import ValidationError
    if statement_type not in STATEMENT_TYPES:
        return [f"statement_type: no type {statement_type!r} ({', '.join(STATEMENT_TYPES)})"]
    if isinstance(payload, str):                  # a payload sent as a JSON-encoded string (structured output)
        try:
            payload = json.loads(payload)
        except ValueError:
            pass
    if not isinstance(payload, dict):
        return ["payload: must be a JSON object"]
    p = dict(payload)
    try:
        if statement_type == "amendment_op":
            from ..amend import Op
            if provision:
                p.setdefault("provision", provision)
            if item_id:
                p.setdefault("id", item_id)
            p.update(origin="assistant", review="proposed", reviewer=None)    # as the controller forces them
            Op.model_validate(p)
        elif statement_type == "disposition":
            from ..amend import Disposition
            if provision:
                p.setdefault("provision", provision)
            p["origin"] = "assistant"
            Disposition.model_validate(p)
        elif statement_type == "row_reading":
            from ..register import Interp
            pl = RowReadingPayload.model_validate(p)
            Interp.model_validate({k: v for k, v in pl.interpretation.items() if k != "pins"})
        elif statement_type == "row_new":
            from ..register import Row
            Row.model_validate(RowNewPayload.model_validate(p).row)
        else:
            {"issue": IssuePayload, "clarification": ClarificationPayload,
             "escalation": EscalationPayload}[statement_type].model_validate(p)
    except ValidationError as e:
        prefix = {"row_new": "payload.row.", "row_reading": "payload.interpretation."}.get(statement_type, "payload.")
        if statement_type in ("row_new", "row_reading") and e.title in ("RowNewPayload", "RowReadingPayload"):
            prefix = "payload."
        return _errors(e, prefix)
    return []


FACT_NEEDS_EVIDENCE = ("a fact needs at least one verbatim quotation in `evidence` (an EvidenceRef); a summary, a "
                       "paraphrase or a translation is not a fact: state it as an interpretation (or an assumption)")


def statement_errors(statements) -> list[dict]:
    """[{id, errors}] for the set's statements that are refused at submission: a `fact` with empty evidence."""
    out = []
    for s in statements or []:
        if isinstance(s, dict) and s.get("kind") == "fact" and not s.get("evidence"):
            out.append({"id": s.get("id"), "errors": [FACT_NEEDS_EVIDENCE]})
    return out


# the payloads re-asked by the bounded repair: an op is checked by the amendment engine itself (simulate_amendment
# before answering; the controller's dry run after), and an op type the engine lacks is an escalation, never a re-asked
# guess: its payload errors are rated `invalid` with the errors (visible), as before
REPAIRABLE = ("disposition", "row_reading", "row_new", "issue", "clarification", "escalation")


def submission_problems(data) -> list[dict]:
    """Session 14 (W1): the inner problems of a submitted set (a dict as given): [{index, id, statement_type, kind,
    errors}] with kind `payload` (an item's payload fails its full schema) or `statement` (a fact with no evidence; the
    index is None). The envelope itself is the parser's (controller.parse_set / requests.check)."""
    if not isinstance(data, dict):
        return []
    out = []
    for i, it in enumerate(data.get("items") or []):
        if not isinstance(it, dict) or it.get("statement_type") not in REPAIRABLE:
            continue
        errs = payload_errors(it.get("statement_type"), it.get("payload"), it.get("provision"), it.get("id"))
        if errs:
            out.append({"index": i, "id": it.get("id"), "statement_type": it.get("statement_type"), "kind": "payload",
                        "errors": errs})
    for s in statement_errors(data.get("statements")):
        out.append({"index": None, "id": s["id"], "statement_type": "statement", "kind": "statement",
                    "errors": s["errors"]})
    return out


def repair_schemas(problems: list[dict]) -> dict:
    """The full schema of every statement type named by `problems` (payload problems), once each; a statement problem
    adds the Statement schema."""
    out = {}
    for p in problems:
        t = p.get("statement_type")
        if p.get("kind") == "payload" and t in STATEMENT_TYPES and t not in out:
            out[t] = payload_schema(t)
        elif p.get("kind") == "statement" and "statement" not in out:
            out["statement"] = Statement.model_json_schema()
    return out


def merge_repair(first: dict, repaired: dict, ids, indices=()) -> tuple[dict, dict]:
    """Session 14 (W1): the set after a bounded repair of the items named by `ids` (item ids, or statement ids): every
    item of `first` NOT named is kept exactly as first given (a valid sibling is never re-asked and never changed by the
    repair); a named item is replaced by the repaired item of the same id when the repair gives one (otherwise the first
    stands, and is rated as it is). Returns (merged set, notes {replaced, kept, missing, refused, why_refused}).
    Session 14 (F4; R4-4): the repair replaces ONLY what it names. Any other item it carries is refused (named in
    `refused`, why in `why_refused`; the first stands as first given). A statement is replaced only when named; a NEW
    statement is added only when a replaced item cites it and no kept item does (it cannot change a sibling's basis);
    every other statement of the repair is refused the same way."""
    ids = {str(x) for x in ids if x is not None}
    indices = {int(x) for x in indices if x is not None}
    rep_list = [it for it in (repaired or {}).get("items") or []]
    rep_items = {it.get("id"): it for it in rep_list if isinstance(it, dict) and it.get("id") is not None}
    items, notes = [], {"replaced": [], "kept": [], "missing": [], "refused": [], "why_refused": {}}

    def refuse(key, why: str) -> None:
        notes["refused"].append(key)
        notes["why_refused"][key] = why
    for n, it in enumerate(first.get("items") or []):
        iid = it.get("id") if isinstance(it, dict) else None
        named = (iid is not None and str(iid) in ids) or n in indices
        # an item without an id (an envelope error) is matched by its position in the repaired answer
        rep = rep_items.get(iid) if iid is not None else (rep_list[n] if n < len(rep_list) else None)
        if named and rep is not None:
            items.append(rep)
            notes["replaced"].append(iid if iid is not None else f"#{n}")
        else:
            items.append(it)
            (notes["missing"] if named else notes["kept"]).append(iid if iid is not None else f"#{n}")
    named_ids = {x for x in notes["replaced"] + notes["missing"]}
    for k in rep_items:                                    # a sibling resent unasked: the first stands
        if k not in named_ids:
            refuse(k, "item not named in the repair request: the first submission's item stands as first given"
                   if any(isinstance(i, dict) and i.get("id") == k for i in first.get("items") or []) else
                   "item not named in the repair request (a repair adds no item)")
    cited_new = {str(c) for it in items for c in ((it.get("statements") or []) if isinstance(it, dict) else [])
                 if isinstance(it, dict) and it.get("id") in notes["replaced"]}
    cited_kept = {str(c) for it in items if isinstance(it, dict) and it.get("id") not in notes["replaced"]
                  for c in it.get("statements") or []}
    sts = [dict(s) if isinstance(s, dict) else s for s in first.get("statements") or []]
    pos = {s.get("id"): n for n, s in enumerate(sts) if isinstance(s, dict)}
    for s in (repaired or {}).get("statements") or []:
        if not isinstance(s, dict):
            continue
        sid = s.get("id")
        if sid in pos and str(sid) in ids:
            sts[pos[sid]] = s
        elif sid in pos:
            refuse(sid, "statement not named in the repair request: the first submission's statement stands")
        elif str(sid) in cited_new and str(sid) not in cited_kept:
            pos[sid] = len(sts)
            sts.append(s)
        else:
            refuse(sid, "new statement not cited by a repaired item alone (it would change the basis of an item "
                        "kept as first given, or nothing repaired cites it)")
    return {**first, "statements": sts, "items": items}, notes
