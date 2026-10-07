"""Session 14 (W1; blind-07 COMPARISON §8 defect 1, report §9 L21): the full row and interpretation schemas are
exposed, an invalid inner payload is repaired within a bound, and its VALID siblings are kept.

blind-07: every analysis `row_new` failed the register.Row schema (a consequence given as the string "none stated in
this provision", `scope` as a string, `discipline`, `confidence` and `confidence_reason` missing). The packet described
`row` only as "register.Row fields (...)"; the request layer checked the item's envelope (ChangeProposal, whose payload
is a free dict), so the failure was never re-asked; on the host route the submission was staged as it was. Now:
  * the packet's `payload_schemas`, validate_proposal(schemas=...) and the policy expose the FULL shapes;
  * on the provider routes the one bounded re-ask carries the exact errors and the full schema, and only the failing
    items are taken from it (a sibling resent changed is ignored);
  * on the host route the MCP submission gate stages the first submission, answers with a repair request (exact errors,
    full schemas) and accepts ONE re-submission of the failing items only, merged into the first;
  * a payload still invalid after the bound stays in the set, `invalid`, with its errors visible.
Synthetic items on the blind-02 rehearsal pack (not tender content)."""
from __future__ import annotations

import copy
import json

import pytest

from ai_fixture import workspace
from tenderpack.ai import config as C
from tenderpack.ai import contract as K
from tenderpack.ai import requests as R
from tenderpack.ai.providers.recorded import RecordedProvider

Q31 = {"doc": "ADD-03", "unit_id": "ADD-03:3.1", "page": 1, "kind": "span",
       "words": "‘one hundred and fifty (150) days’ is deleted and ‘one hundred and eighty (180) days’ is substituted"}
Q24 = {"doc": "ADD-03", "unit_id": "ADD-03:2.4", "page": 1, "kind": "span",
       "words": "The following new Clause 6.8 is inserted in Volume I after Clause 6.7"}
# the blind-07 shapes: a consequence string, scope a string, discipline / confidence / confidence_reason missing
BAD_ROW = {"id": "ADD-03-2.4-91", "group": "ADD-03:2.4", "scope": "submission", "requirement": "test data",
           "units": ["ADD-03:2.4"], "assessment": "procedural", "evidence": [],
           "interpretations": [{"stage": "ADD-03", "quote": "The following new Clause 6.8 is inserted",
                                "consequence": "none stated in this provision"}]}
GOOD_ROW = {**{k: v for k, v in BAD_ROW.items()}, "scope": ["submission"], "discipline": "Commercial",
            "confidence": "low", "confidence_reason": "test data",
            "interpretations": [{"stage": "ADD-03", "quote": "The following new Clause 6.8 is inserted",
                                 "consequence": "none_stated"}]}


@pytest.fixture(scope="module")
def ws(request, tmp_path_factory):
    return workspace(tmp_path_factory.mktemp("s14-repair"), evidence=request.getfixturevalue("blind02_build"))


def _op(st, new="one hundred and eighty (180) days"):
    return {"id": "ADD-03/3.1", "state": st, "statement_type": "amendment_op", "provision": "ADD-03:3.1",
            "target": "VOL-I:7.1", "payload": {"type": "replace_text", "target": "VOL-I:7.1",
                                               "old": "one hundred and fifty (150) days", "new": new},
            "evidence": [Q31]}


def _row(st, row):
    return {"id": "ADD-03/2.4/row", "state": st, "statement_type": "row_new", "provision": "ADD-03:2.4",
            "payload": {"row": row}, "evidence": [Q24]}


def _set(st, items, statements=()):
    return {"addendum": "ADD-03", "state": st, "statements": list(statements), "items": items}


# ---------------------------------------------------------------------------------------------- the schemas

def test_the_packet_and_the_tool_expose_the_full_row_and_interpretation_schemas(ws):
    from tenderpack.ai import controller
    from tenderpack.ai.tools import call_tool
    ps = K.payload_schemas()
    row = ps["row_new"]
    assert row["properties"]["row"]["$ref"] == "#/$defs/Row", row["properties"]["row"]
    assert {"discipline", "confidence", "confidence_reason", "scope"} <= set(row["$defs"]["Row"]["required"])
    assert row["$defs"]["Row"]["properties"]["scope"]["type"] == "array" and "Consequence" in row["$defs"]
    assert ps["row_reading"]["properties"]["interpretation"]["$ref"] == "#/$defs/Interp"
    pk = controller.task_packet(ws, "ADD-03", ["ADD-03:2.4"])
    assert "Row" in pk["payload_schemas"]["row_new"]["$defs"]
    compact = R.compact_analysis(dict(pk, crops=[]))           # the shared part lifts the $defs once, keeps them
    assert "Row" in json.dumps(compact.get("schema_defs") or compact["payload_schemas"])
    got = call_tool(ws, "validate_proposal", {"schemas": ["row_new"]}, "model")
    assert "confidence_reason" in got["schemas"]["row_new"]["$defs"]["Row"]["properties"]
    # the policy says so where the payload is described (the analysis prompt every route composes)
    assert "register.Row" in controller.SYSTEM and "none_stated" in controller.SYSTEM


def test_validate_proposal_returns_the_exact_errors_and_the_schema_of_a_failing_payload(ws):
    from tenderpack.ai.tools import call_tool
    st = ws.identity().model_dump()
    res = call_tool(ws, "validate_proposal", {"proposal": _row(st, BAD_ROW)}, "model")
    errs = " ".join(res["payload_problems"][0]["errors"])
    for w in ("payload.row.scope", "payload.row.discipline: Field required", "payload.row.confidence: Field required",
              "payload.row.confidence_reason: Field required", "consequence"):
        assert w in errs, (w, errs)
    assert "Row" in res["schemas"]["row_new"]["$defs"]
    assert res["items"][0]["verification_status"] == "invalid"


# ---------------------------------------------------------------------------------------------- the provider routes

def test_the_request_check_reasks_a_failing_inner_payload_with_its_errors_and_schema(ws):
    st = ws.identity().model_dump()
    sp = R.spec("analysis")
    data, env, probs = R.check(sp, _set(st, [_op(st), _row(st, BAD_ROW)]))
    assert env == [] and [p["kind"] for p in probs] == ["payload"] and probs[0]["id"] == "ADD-03/2.4/row", probs
    msg = R.repair_message(sp, env, probs)
    assert "payload.row.confidence_reason: Field required" in msg
    assert "FULL SCHEMA of the row_new payload" in msg and "confidence_reason" in msg.split("FULL SCHEMA")[1]


def _recorded(turns):
    return RecordedProvider({"name": "s14", "model": "recorded-fixture-model", "turns": turns,
                             "capabilities": {"images": True, "tools": True, "structured_output": False,
                                              "context_tokens": 400000, "source": "cassette (recorded fixture)"}})


def test_one_bounded_repair_fixes_the_item_and_keeps_its_valid_sibling_as_first_given(ws):
    from tenderpack.ai import controller
    st = ws.identity().model_dump()
    first = json.dumps(_set(st, [_op(st), _row(st, BAD_ROW)]))
    # the repair resends the sibling CHANGED (190 days): only the listed item is taken from the repair
    second = json.dumps(_set(st, [_op(st, new="one hundred and ninety (190) days"), _row(st, GOOD_ROW)]))
    prov = _recorded([{"response": {"text": first}},
                      {"match": {"last_role": "user", "contains": ["REPAIR REQUEST", "FULL SCHEMA of the row_new"]},
                       "response": {"text": second}}])
    ps = controller.propose(ws, "ADD-03", "recorded", C.load(), provider=prov, sleep=lambda s: None,
                            provisions=["ADD-03:3.1", "ADD-03:2.4"])
    assert len(prov.requests) == 2
    by = {it.id: it for it in ps.items}
    assert by["ADD-03/3.1"].payload["new"] == "one hundred and eighty (180) days"        # the sibling as first given
    assert by["ADD-03/3.1"].verification_status == "evidence_verified"
    assert by["ADD-03/2.4/row"].payload["row"]["confidence"] == "low"                    # the repaired item
    assert by["ADD-03/2.4/row"].verification_status != "invalid", by["ADD-03/2.4/row"].validation


def test_a_payload_still_invalid_after_the_bound_stays_invalid_with_its_errors_visible(ws):
    from tenderpack.ai import controller
    st = ws.identity().model_dump()
    first = json.dumps(_set(st, [_op(st), _row(st, BAD_ROW)]))
    prov = _recorded([{"response": {"text": first}}, {"response": {"text": first}},
                      {"response": {"text": first}}])
    ps = controller.propose(ws, "ADD-03", "recorded", C.load(), provider=prov, sleep=lambda s: None,
                            provisions=["ADD-03:3.1", "ADD-03:2.4"])
    assert len(prov.requests) == 2                                  # the bound: one re-ask, no more
    by = {it.id: it for it in ps.items}
    row = by["ADD-03/2.4/row"]                                      # kept, never set aside
    assert row.verification_status == "invalid"
    detail = " ".join(v.detail for v in row.validation if not v.ok)
    assert "payload.row.confidence_reason: Field required" in detail and "payload.row.scope" in detail, detail
    assert by["ADD-03/3.1"].verification_status == "evidence_verified"


# ---------------------------------------------------------------------------------------------- the host route (MCP)

def _call(srv, n, name, args):
    r = srv.handle({"jsonrpc": "2.0", "id": n, "method": "tools/call", "params": {"name": name, "arguments": args}})
    res = r["result"]
    return json.loads(res["content"][0]["text"]), res["isError"]


def test_the_submission_gate_asks_one_repair_of_the_failing_items_only_and_merges_it(ws, tmp_path):
    from pathlib import Path

    import yaml

    from tenderpack.mcp_server import Server
    st = ws.identity().model_dump()
    srv = Server(ws, None, tools=["submit_proposals", "validate_proposal"], submit_once=True,
                 submission_record=tmp_path / "rec.json")
    a, err = _call(srv, 1, "submit_proposals", {"proposal_set": _set(st, [_op(st), _row(st, BAD_ROW)]),
                                                "host_model": "test-host"})
    assert not err and a["run_id"] and a["repair"]["tries_left"] == 1, a
    assert [p["id"] for p in a["repair"]["problems"]] == ["ADD-03/2.4/row"]
    assert "Row" in a["repair"]["schemas"]["row_new"]["$defs"]
    assert json.loads((tmp_path / "rec.json").read_text())["run_id"] == a["run_id"]      # never lost
    # the one repair: only the failing item (a resent, changed sibling is refused and named; session 14 F4, R4-4)
    b, err = _call(srv, 2, "submit_proposals", {"proposal_set": _set(st, [_row(st, GOOD_ROW),
                                                                          _op(st, "one hundred and ninety (190) days")]),
                                                "host_model": "test-host"})
    assert not err and b["repair_of"] == a["run_id"] and b["run_id"] != a["run_id"], b
    assert b["repair_merge"]["replaced"] == ["ADD-03/2.4/row"] and b["repair_merge"]["refused"] == ["ADD-03/3.1"]
    assert json.loads((tmp_path / "rec.json").read_text())["run_id"] == b["run_id"]
    assert json.loads((Path(a["staging"]) / "superseded.json").read_text())["superseded_by"] == b["run_id"]
    ps = yaml.safe_load((Path(b["staging"]) / "proposals.yaml").read_text())["proposal_set"]
    by = {it["id"]: it for it in ps["items"]}
    assert by["ADD-03/3.1"]["payload"]["new"] == "one hundred and eighty (180) days"
    assert by["ADD-03/3.1"]["verification_status"] == "evidence_verified"
    assert by["ADD-03/2.4/row"]["verification_status"] != "invalid", by["ADD-03/2.4/row"]["validation"]
    c, err = _call(srv, 3, "submit_proposals", {"proposal_set": _set(st, [_row(st, GOOD_ROW)]), "host_model": "t"})
    assert err and "already submitted" in c["error"]                 # the bound: no second repair


def test_the_gate_refuses_a_fact_with_empty_evidence_and_asks_for_it_again(ws, tmp_path):
    from tenderpack.mcp_server import Server
    st = ws.identity().model_dump()
    srv = Server(ws, None, tools=["submit_proposals"], submit_once=True)
    fact = {"id": "S1", "kind": "fact", "text": "the period moves to 180 days", "evidence": []}
    a, err = _call(srv, 1, "submit_proposals", {"proposal_set": _set(st, [{**_op(st), "statements": ["S1"]}], [fact]),
                                                "host_model": "test-host"})
    assert not err and a["repair"]["problems"][0]["kind"] == "statement", a
    assert "verbatim quotation" in a["repair"]["problems"][0]["errors"][0]
    assert a["blast_radius"][0]["statement"] == "S1" and a["blast_radius"][0]["refused"] is True
