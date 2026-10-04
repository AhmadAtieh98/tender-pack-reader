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
SET_STATUS = ("complete", "partial", "malformed", "provider_failed", "budget_exhausted", "stale")

# fields of a ProposalSet / ChangeProposal that only the controller writes
CONTROLLER_SET_FIELDS = ("run_id", "created", "route", "provider", "model_requested", "model_reported", "task",
                         "coverage", "resolution", "usage", "status", "controller_version")
CONTROLLER_ITEM_FIELDS = ("validation", "verification_status")


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


class RowReadingPayload(_Strict):
    row: str = Field(description="an existing A1 row id")
    interpretation: dict = Field(description="register.Interp fields: stage, quote, parameters, consequence, note "
                                             "(no pins: pins are machine-written)")
    replace_requirement: dict | None = None


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
    dependencies: list[str] = Field(default_factory=list, description="ids of units, rows or ops this item relies on")
    conflicts: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    statements: list[str] = Field(default_factory=list, description="ids of the statements this item depends on")
    validation: list[ValidationRecord] = Field(default_factory=list, description="controller-written")
    verification_status: Literal["unverified", "evidence_verified", "insufficient_evidence", "invalid", "conflicting",
                                 "escalated", "interpretation_pending"] = Field("unverified",
                                                                               description="controller-written")
    model_rationale: str | None = Field(None, description="free text; never read by code")


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
    status: Literal["complete", "partial", "malformed", "provider_failed", "budget_exhausted", "stale"] = "partial"
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
    """The payload shapes per statement type (amend.Op and amend.Disposition come from the amendment engine)."""
    from ..amend import Disposition, Op
    return {"amendment_op": Op.model_json_schema(), "disposition": Disposition.model_json_schema(),
            "row_reading": RowReadingPayload.model_json_schema(), "row_new": RowNewPayload.model_json_schema(),
            "issue": IssuePayload.model_json_schema(), "clarification": ClarificationPayload.model_json_schema(),
            "escalation": EscalationPayload.model_json_schema()}


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
                    "escalation")


class IssueItemPayload(_Strict):
    id: str = Field(description="a new issue id, I-...")
    text: str
    owner: str
    theme: str
    short: str | None = None
    a3: str | None = Field(None, description="the A3 wording, when the issue belongs on the one-page sheet")
    show_in_a3: bool = False


class ClarificationItemPayload(_Strict):
    entry: dict = Field(description="one entry of the clarification register in its own shape: id (CQ-...), kind, "
                                    "volume, clause, page, units, sources [{unit, page, words}], gap, already_settled, "
                                    "practical_impact, proposed_question, interim_handling, decision_owner, "
                                    "response_status ('draft, not sent'), linked_issues, theme. A DRAFT: never sent")


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
                            "dependency", "escalation"]
    task: str = Field(description="the id of the downstream task in the packet this item answers")
    provision: str | None = Field(None, description="the addendum provision whose change the item follows")
    target: str | None = None
    payload: dict = Field(description="row_reading: {row, interpretation, replace_requirement}; row_new: {row}; "
                                      "issue: IssueItemPayload; clarification_item: {entry}; evidence_item: {id, "
                                      "item}; activity: ActivityPayload; dependency: DependencyPayload; escalation: "
                                      "{why, what_is_unsupported}")
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
            "escalation": EscalationPayload.model_json_schema()}


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
