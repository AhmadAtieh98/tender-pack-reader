"""Native structured outputs for the proposal set, ALONGSIDE the controller's own parsing and pydantic validation (never
instead of it): the provider constrains the shape of the final answer; the controller still parses it strictly, validates
it against contract.ProposalSet and assigns every status.

The schema is derived from contract.ProposalSet.model_json_schema(), trimmed to what the proposer fills
(contract.model_fill_schema()), then fitted to the provider's schema limits by `for_provider`:

  anthropic   Messages API `output_config: {format: {type: "json_schema", schema}}`, sent with the tools on every turn
              (shape from the bundled claude-api skill: python/claude-api/tool-use.md "Structured Outputs" -> "Raw
              Schema" and "Using Both Together"; limits from shared/tool-use-concepts.md "JSON Schema Limitations":
              `additionalProperties: false` on every object; no recursive schemas; no numerical, string-length or
              complex array constraints; `additionalProperties` never anything but false). The same fitted schema is
              sent to OpenRouter (`response_format: {type: "json_schema", json_schema: {name, strict: true, schema}}`)
              when its model listing names `structured_outputs`.
  ollama      `format: <schema>` on /api/chat; free-form objects are allowed there, so only titles/defaults go.

The one free-form object the proposer fills is an item's `payload` (an amend.Op, an amend.Disposition, a row reading,
...: its own shapes are given in the task packet's `payload_schemas`). Under the anthropic limits a free-form object
cannot be expressed, so there the payload travels as a JSON-ENCODED STRING; `decode_payloads` turns it back into the
object before the controller's strict parse, which then validates it as before. Nothing else is transformed.

A provider that rejects the schema (`is_schema_rejection`) is answered by the plain tool-use path (the final answer as
text, parsed locally) with a route notice in the run log and the review request; never silently.
"""
from __future__ import annotations

import copy
import json
import re

SCHEMA_NAME = "proposal_set"
FLAVOURS = ("anthropic", "ollama")
# keywords the anthropic limits exclude (or that only carry documentation); the local pydantic validation still applies
_STRIP = {"title", "default", "examples", "minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "multipleOf",
          "minLength", "maxLength", "pattern", "minItems", "maxItems", "uniqueItems", "minProperties", "maxProperties",
          "patternProperties", "propertyNames", "dependentRequired", "dependentSchemas"}
_FORMATS = {"date-time", "time", "date", "duration", "email", "hostname", "uri", "ipv4", "ipv6", "uuid"}
STRING_PAYLOAD_NOTE = (" Under native structured outputs this object is sent as a JSON-ENCODED STRING (the provider's "
                       "schema limits forbid free-form objects); the controller decodes it and validates it against "
                       "payload_schemas.")


class SchemaUnsupported(Exception):
    """The derived schema cannot be expressed within the provider's limits (e.g. it is recursive)."""


def proposal_schema() -> dict:
    """The proposer's schema: contract.ProposalSet.model_json_schema() trimmed to the fields the proposer fills."""
    from ..contract import model_fill_schema
    return model_fill_schema()


def _refs(node, out: set) -> set:
    if isinstance(node, dict):
        r = node.get("$ref")
        if isinstance(r, str) and r.startswith("#/$defs/"):
            out.add(r.rsplit("/", 1)[-1])
        for v in node.values():
            _refs(v, out)
    elif isinstance(node, list):
        for v in node:
            _refs(v, out)
    return out


def check_not_recursive(schema: dict) -> None:
    defs = schema.get("$defs") or {}
    graph = {k: _refs(v, set()) for k, v in defs.items()}

    def visit(k, path):
        if k in path:
            raise SchemaUnsupported(f"recursive schema: {' -> '.join([*path, k])}")
        for n in graph.get(k, ()):
            visit(n, [*path, k])
    for k in graph:
        visit(k, [])


def _free_form(node: dict) -> bool:
    return node.get("type") == "object" and not node.get("properties") and "$ref" not in node


def for_provider(schema: dict, flavour: str = "anthropic") -> dict:
    """Fit a JSON schema to a provider's structured-output limits (see the module docstring). Raises SchemaUnsupported."""
    if flavour not in FLAVOURS:
        raise SchemaUnsupported(f"no structured-output flavour {flavour!r}")
    s = copy.deepcopy(schema)
    check_not_recursive(s)

    def walk(node):
        if isinstance(node, list):
            return [walk(x) for x in node]
        if not isinstance(node, dict):
            return node
        out = {}
        for k, v in node.items():
            if k in ("properties", "$defs"):
                out[k] = {name: walk(sub) for name, sub in v.items()}
            elif k in _STRIP and flavour == "anthropic":
                continue
            elif k in ("title", "default") and flavour == "ollama":
                continue
            elif k == "format" and isinstance(v, str) and v not in _FORMATS and flavour == "anthropic":
                continue
            else:
                out[k] = walk(v)
        if flavour == "anthropic":
            if _free_form(out):
                desc = (out.get("description") or "an object") + STRING_PAYLOAD_NOTE
                return {"type": "string", "description": desc}
            if out.get("type") == "object" or "properties" in out:
                out["additionalProperties"] = False
        return out
    return walk(s)


def decode_payloads(data):
    """An item payload sent as a JSON-encoded string (anthropic-flavour schemas) is decoded back into its object; a
    string that is not a JSON object is left as it is, so the strict parse reports it. Returns `data` (a copy when
    anything was decoded)."""
    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        return data
    if not any(isinstance(it, dict) and isinstance(it.get("payload"), str) for it in data["items"]):
        return data
    data = dict(data)
    items = []
    for it in data["items"]:
        if isinstance(it, dict) and isinstance(it.get("payload"), str):
            try:
                obj = json.loads(it["payload"])
            except ValueError:
                obj = None
            if isinstance(obj, dict):
                it = {**it, "payload": obj}
        items.append(it)
    data["items"] = items
    return data


_REJECT = re.compile(r"output_config|output_format|json_schema|response_format|\bschema\b|\bformat\b", re.I)


def is_schema_rejection(err) -> bool:
    """A 4xx (or an API error body) that names the structured-output parameter or the schema: the provider rejected it."""
    status = getattr(err, "status", None)
    kind = str(getattr(err, "kind", ""))
    client_error = (status is not None and 400 <= int(status) < 500 and int(status) not in (401, 403, 404, 408, 409, 429)) \
        or kind.startswith("api_error")
    return bool(client_error and _REJECT.search(str(getattr(err, "message", "")) or ""))
