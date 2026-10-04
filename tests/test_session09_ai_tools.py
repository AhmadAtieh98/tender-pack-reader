"""Session 09, the AI layer's read-only tools on blind rehearsal 02 (ADD-03 as a fresh addendum; disposable
directories). The tools compute from the evidence build and the curated inputs and write nothing."""
from __future__ import annotations

import copy

import pytest
import yaml

from ai_fixture import CURATED_ADD03, Untouched, workspace
from tenderpack.ai.tools import MODEL_TOOLS, TOOLS, ToolError, call_tool


@pytest.fixture(scope="module")
def ws(tmp_path_factory, blind02_build):
    return workspace(tmp_path_factory.mktemp("ai-tools"), evidence=blind02_build)


def test_the_state_identity_names_the_build_and_the_stages(ws):
    st = ws.identity()
    assert st.pack_id == "NUPA-ISTP-2026-014-BLIND-02" and len(st.evidence_build_id) == 64
    assert (st.validated_stage, st.working_stage, st.decisions_sha256) == ("ADD-02", "ADD-03", None)
    assert call_tool(ws, "get_state", {}, "cli")["state"] == st.model_dump()


def test_search_finds_the_provision_that_moves_the_time(ws):
    res = call_tool(ws, "search_evidence", {"query": "11:00 hours"}, "model")["results"]
    assert res[0]["unit_id"] == "ADD-03:2.1" and res[0]["phrase"] and res[0]["pages"] == [1]
    assert "11:00 hours Riyadh time" in res[0]["snippet"]
    only = call_tool(ws, "search_evidence", {"query": "Bid Bond", "docs": ["VOL-I"], "limit": 3}, "model")["results"]
    assert len(only) == 3 and all(r["doc"] == "VOL-I" for r in only)
    assert call_tool(ws, "search_evidence", {"query": "Bid Bond"}, "model") == \
        call_tool(ws, "search_evidence", {"query": "Bid Bond"}, "model")            # deterministic
    ar = call_tool(ws, "search_evidence", {"query": "الهيئة الشمالية"}, "model")["results"]
    assert ar and ar[0]["unit_id"].startswith("VOL-IV:F4-C/image/") and ar[0]["matched_in"] == "text"


def test_get_unit_gives_issued_and_effective_text_and_the_reading_fields_apart(ws):
    u = call_tool(ws, "get_unit", {"unit_id": "VOL-I:6.1", "stage": "ADD-03"}, "model")
    assert "14:00 hours" in u["text_as_issued"] and "12 November 2026" in u["text_as_issued"]
    assert "11:00 hours Riyadh time on Thursday 26 November 2026" in u["effective_text"]
    assert [h["op"] for h in u["history"]] == ["ADD-01/2.1", "ADD-03/2.1"] and u["pages"] == [3]
    before = call_tool(ws, "get_unit", {"unit_id": "VOL-I:6.1"}, "model")         # default: the validated stage
    assert before["stage"] == "ADD-02" and "14:00 hours" in before["effective_text"]
    a = call_tool(ws, "get_unit", {"unit_id": "VOL-IV:F4-C/image/hdr-ar"}, "model")["reading"]
    assert a["source_text"] == "الهيئة الشمالية للمشتريات المرفقية"
    assert a["translation"] == "Northern Utilities Procurement Authority" and a["match_text"] and a["status"] == "approved"
    with pytest.raises(ToolError, match="no unit"):
        call_tool(ws, "get_unit", {"unit_id": "../../curation/approvals.yaml"}, "model")
    with pytest.raises(ToolError, match="unknown argument"):
        call_tool(ws, "get_unit", {"unit_id": "VOL-I:6.1", "path": "/etc/passwd"}, "model")


def test_get_group_and_get_crop(ws):
    g = call_tool(ws, "get_group", {"group_id": "VOL-II:T2-4"}, "model")
    assert g["count"] >= 8 and g["image_table_context"]["qualifier"].startswith("(all values are maxima")
    assert any(m["unit_id"] == "VOL-II:T2-4/BOD5" and m["cells"]["Limit"] == "10" for m in g["members"])
    c = call_tool(ws, "get_crop", {"unit_id": "VOL-II:T2-4/BOD5"}, "model")
    kinds = {x["kind"] for x in c["crops"]}
    assert {"native", "unit", "cell"} <= kinds and all(len(x["sha256"]) == 64 for x in c["crops"])
    assert all(x["path"].startswith(str(ws.evidence)) for x in c["crops"])
    with pytest.raises(ToolError, match="text-layer unit"):
        call_tool(ws, "get_crop", {"unit_id": "VOL-I:6.1"}, "model")


def test_compare_state_and_the_approved_calculations(ws):
    cs = call_tool(ws, "compare_state", {"from_stage": "ADD-02", "to_stage": "ADD-03"}, "model")
    six = next(u for u in cs["units"] if u["unit"] == "VOL-I:6.1")
    assert "11:00" in six["text_after"] and six["ops"] == ["ADD-03/2.1"]
    assert cs["diff"]["from"] == "ADD-02" and "requirements" in cs["diff"]
    wd = call_tool(ws, "calculate", {"kind": "relative_date", "args": {"anchor_date": "2026-11-26", "offset": 5,
                                                                      "unit": "working_day", "direction": "before"}}, "model")
    assert wd["planning"]["value"] == "2026-11-19" and wd["readings"][0]["basis"] == "VOL-I §2.4"
    cd = call_tool(ws, "calculate", {"kind": "relative_date", "args": {"anchor_date": "2026-11-26", "offset": 180,
                                                                      "unit": "calendar_day", "purpose": "validity_end"}}, "model")
    assert {r["key"] for r in cd["readings"]} == {"day0", "day1"} and cd["readings_differ"]     # both readings kept
    assert call_tool(ws, "calculate", {"kind": "working_days_between", "args": {"from": "2026-11-19", "to": "2026-11-26"}},
                     "model")["result"] == 5
    pd = call_tool(ws, "calculate", {"kind": "printed_date", "args": {"unit_id": "VOL-I:6.1", "stage": "ADD-03"}}, "model")
    assert (pd["result"], pd["time"]) == ("2026-11-26", "11:00")
    with pytest.raises(ToolError, match="must be one of"):
        call_tool(ws, "calculate", {"kind": "eval", "args": {"expr": "1+1"}}, "model")
    with pytest.raises(ToolError, match="unknown arguments"):
        call_tool(ws, "calculate", {"kind": "is_working_day", "args": {"date": "2026-11-26", "expr": "x"}}, "model")


def test_simulate_amendment_on_the_curated_ops_and_on_a_wrong_old(ws):
    f = yaml.safe_load(CURATED_ADD03.read_text(encoding="utf-8"))
    with Untouched():
        sim = call_tool(ws, "simulate_amendment", {"addendum": "ADD-03", "ops": f["ops"],
                                                   "dispositions": f["dispositions"]}, "model")
    assert sim["from_stage"] == "ADD-02" and len(sim["ops"]) == len(f["ops"]) >= 31
    assert all(o["valid"] for o in sim["ops"]), [o["failed"] for o in sim["ops"] if not o["valid"]]
    assert sim["status"] == "APPLIED" and sim["unaccounted"] == [] and sim["c47_unevidenced_additions"] == []
    assert sim["scope_leak"] == [] and "VOL-I:6.1" in sim["changed_units"] and "VOL-I:6.7+ADD-03" in sim["changed_units"]
    assert sim["c46_needs"] == []                         # the rehearsal's register carries the new obligations
    ops = copy.deepcopy(f["ops"])
    op = next(o for o in ops if o["id"] == "ADD-03/3.1")
    op["old"], op["new"] = "one hundred and eighty (180) days", "one hundred and fifty (150) days"   # quoted, but wrong
    bad = call_tool(ws, "simulate_amendment", {"addendum": "ADD-03", "ops": ops, "dispositions": f["dispositions"]}, "model")
    x = next(o for o in bad["ops"] if o["id"] == "ADD-03/3.1")
    assert not x["valid"] and x["failed"][0]["id"] == "C23" and "occurs 0 time(s)" in x["failed"][0]["detail"]
    assert bad["status"] == "PARTIAL" and ws.r["validated"].stage == "ADD-02"     # nothing persisted


def test_simulate_programme_and_the_tool_surface(ws):
    p = call_tool(ws, "simulate_programme", {"stage": "ADD-02"}, "model")
    assert p["stage"] == "ADD-02" and p["milestones"] and len(p["infeasible"]) <= 30
    assert any(m["id"] == "PRE-BID" for m in p["milestones"])
    assert set(MODEL_TOOLS) == {"search_evidence", "get_unit", "get_group", "get_crop", "compare_state", "calculate",
                                "simulate_amendment", "simulate_programme", "validate_proposal"}
    assert {n for n, t in TOOLS.items() if t.writes} == {"get_task_packet", "request_review", "submit_proposals"}
    for name in ("request_review", "submit_proposals", "get_task_packet", "write_file"):
        with pytest.raises(ToolError, match="no tool"):
            call_tool(ws, name, {}, "model")                # a model never gets a writer


def test_validate_proposal_flags_a_change_to_an_approved_image_reading(ws):
    """The owner approved the transcription of Table 2-4 (approvals.yaml region VOL-II-p3-r1): a proposal that changes a
    cell of it is recorded as touching an approved reading (the approval covers the transcription, not the amendment;
    the engine flags every amended reading for a person), and is otherwise verified like any other. Nothing is written."""
    item = {"id": "ADD-02/5.1", "state": ws.identity().model_dump(), "statement_type": "amendment_op",
            "provision": "ADD-02:5.1", "target": "VOL-II:T2-4/TN",
            "payload": {"type": "set_value", "target": "VOL-II:T2-4/TN", "column": "Limit", "new": "3"},
            "previous_value": "5", "proposed_value": "3",
            "evidence": [{"doc": "ADD-02", "unit_id": "ADD-02:5.1", "page": 1, "kind": "span",
                          "words": "the limit for Total Nitrogen (TN) is amended from the value shown to 3 mg/l"},
                         {"doc": "VOL-II", "unit_id": "VOL-II:T2-4/TN", "page": 3, "kind": "cell",
                          "cell": {"row_key": "TN", "column": "Parameter"}, "words": "Total Nitrogen (TN)"}]}
    with Untouched():
        res = call_tool(ws, "validate_proposal", {"proposal": item}, "model")
    v = res["items"][0]
    assert v["verification_status"] == "evidence_verified", v
    assert any(x["check"] == "approvals" and x["ok"] and "VOL-II-p3-r1" in x["detail"] for x in v["validation"])
    assert any(x["check"].startswith("engine") and x["ok"] for x in v["validation"])
    assert any(x["check"] == "previous_value" and x["ok"] for x in v["validation"])
    wrong = dict(item, evidence=[item["evidence"][0], {**item["evidence"][1], "words": "Total Nitrogen (TN) 5 mg/l max"}])
    w = call_tool(ws, "validate_proposal", {"proposal": wrong}, "model")["items"][0]
    assert any(not x["ok"] and "not verbatim" in x["detail"] for x in w["validation"])


def test_validate_proposal_keeps_rows_issues_and_questions_apart_from_verified_changes(ws):
    st = ws.identity().model_dump()
    q31 = {"doc": "ADD-03", "unit_id": "ADD-03:3.1", "page": 1, "kind": "span",
           "words": "‘one hundred and fifty (150) days’ is deleted and ‘one hundred and eighty (180) days’ is substituted"}
    op = {"id": "ADD-03/3.1", "state": st, "statement_type": "amendment_op", "provision": "ADD-03:3.1", "target": "VOL-I:7.1",
          "payload": {"type": "replace_text", "target": "VOL-I:7.1", "old": "one hundred and fifty (150) days",
                      "new": "one hundred and eighty (180) days"}, "evidence": [q31]}
    row = {"id": "R1", "state": st, "statement_type": "row_reading", "provision": "ADD-03:3.1", "target": "VOL-I:7.1",
           "payload": {"row": "VOL-I-7.1-01", "interpretation": {
               "stage": "ADD-03", "quote": "one hundred and eighty (180) days from the Proposal Due Date",
               "parameters": {"validity_days": 180}}}, "evidence": [q31], "dependencies": ["ADD-03/3.1", "VOL-I-7.1-01"]}
    bad_row = dict(row, id="R2", payload={"row": "VOL-I-7.1-01", "interpretation": {"stage": "ADD-03",
                                                                                    "quote": "two hundred days"}})
    new_row = {"id": "R3", "state": st, "statement_type": "row_new", "provision": "ADD-03:3.1",
               "payload": {"row": {"id": "VOL-I-7.1-01"}}, "evidence": [q31]}
    issue = {"id": "I1", "state": st, "statement_type": "issue", "provision": "ADD-03:3.3",
             "payload": {"text": "Form 4-A as reissued has no paragraph 2", "owner": "Legal"},
             "evidence": [{"doc": "ADD-03", "unit_id": "ADD-03:3.3", "page": 1, "kind": "span",
                           "words": "Paragraph 2 of Form 4-A shall be read accordingly."}]}
    question = {"id": "C1", "state": st, "statement_type": "clarification", "provision": "ADD-03:3.3",
                "payload": {"gap": "which Form 4-A", "proposed_question": "Which paragraph 2 is meant?"},
                "evidence": issue["evidence"], "missing_information": ["the reissued form has no numbered paragraphs"]}
    unresolved = {"id": "D1", "state": st, "statement_type": "disposition", "provision": "ADD-03:7.1",
                  "payload": {"disposition": "unresolved", "reason": "a re-lettering stated as a range"},
                  "evidence": [{"doc": "ADD-03", "unit_id": "ADD-03:7.1", "page": 2, "kind": "span",
                                "words": "former items (f) to (i) become items (g) to (j) respectively"}],
                  "dependencies": ["NOT-A-UNIT"]}
    res = call_tool(ws, "validate_proposal", {"proposal": {"addendum": "ADD-03", "state": st, "items": [
        op, row, bad_row, new_row, issue, question, unresolved]}}, "model")
    got = {x["id"]: x["verification_status"] for x in res["items"]}
    assert got == {"ADD-03/3.1": "evidence_verified", "R1": "interpretation_pending", "R2": "insufficient_evidence",
                   "R3": "invalid", "I1": "evidence_verified", "C1": "insufficient_evidence", "D1": "insufficient_evidence"}
    assert res["set_status"] == "partial" and res["coverage"]["accounted"] == 2      # 3.1 (op) and 7.1 (disposition)
    assert "ADD-03:3.3" in res["coverage"]["unaccounted"]                       # an issue or a question accounts for nothing
