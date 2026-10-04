"""The shared, typed contract for claims and change proposals (every route uses it: application adapters, a coding
host through MCP or the CLI, and offline recordings).

    StateIdentity   which tender state a proposal was made against: pack id, the evidence build's identity (the
                    sha256 of its BUILD_MANIFEST.json), the validated and working stages, and the sha256 of the
                    decisions file. A proposal made against another state is STALE: every item is invalid.
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
                    the addendum, the state, statements, items, provision coverage, usage (cost null when no price
                    is configured), status and the controller version.

`model_fill_schema()` is the JSON schema given to the model: ProposalSet.model_json_schema() trimmed to the fields
the model fills (controller-written fields removed). Parsing (controller.parse_model_output) accepts the full item
model so that a model-supplied status is caught and overwritten rather than silently dropped.
"""
from __future__ import annotations

import copy
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

CONTROLLER_VERSION = "s09-ai-1"

STATEMENT_TYPES = ("amendment_op", "disposition", "row_reading", "row_new", "issue", "clarification", "escalation")
VERIFICATION = ("unverified", "evidence_verified", "insufficient_evidence", "invalid", "conflicting", "escalated",
                "interpretation_pending")
SET_STATUS = ("complete", "partial", "malformed", "provider_failed", "budget_exhausted", "stale")

# fields of a ProposalSet / ChangeProposal that only the controller writes
CONTROLLER_SET_FIELDS = ("run_id", "created", "route", "provider", "model_requested", "model_reported", "task",
                         "coverage", "usage", "status", "controller_version")
CONTROLLER_ITEM_FIELDS = ("validation", "verification_status")


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class StateIdentity(_Strict):
    pack_id: str
    evidence_build_id: str = Field(description="sha256 of the evidence build's BUILD_MANIFEST.json")
    validated_stage: str
    working_stage: str | None = None
    decisions_sha256: str | None = Field(None, description="sha256 of the decisions file; null when there is none")


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
