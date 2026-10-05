"""Session 11 audit, fixer F1: findings A1-1 .. A1-11 and A2-1 .. A2-10 (reports A1.md, A2.md of the independent audit
of the real pack BASE -> ADD-01 -> ADD-02). Each test reproduces one finding on the real pack (the committed evidence
build, as tests/test_stage2.py reads it) or on small synthetic units, and states the rule the fix makes general.

Passing these tests does not make any interpretation correct or any reading approved."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from tenderpack import stage2
from tenderpack.amend import Engine, OpFile
from tenderpack.register import Register, RowFile, compute_pins
from tenderpack.render import status_fill
from tenderpack.util import ROOT

EVIDENCE = ROOT / "build"
PACK = ROOT / "config/pack.yaml"


@pytest.fixture(scope="module")
def real():
    return stage2.run(EVIDENCE, PACK, ROOT)


@pytest.fixture(scope="module")
def a1(real):
    return stage2.a1_table(real, stage2.collect_issues(real, None))


@pytest.fixture(scope="module")
def a2(real):
    return stage2.a2(real)


def _ev(r, rid):
    return next(e for e in r["evals"] if e["row"].id == rid)["stages"]


def _row(a1, rid):
    return next(x for x in a1["rows"] if x["id"] == rid)


# ------------------------------------------------------------------------------------------ synthetic list insertion

def _list_units() -> list[dict]:
    u = lambda uid, doc, kind, text, page, parent=None: {"unit_id": uid, "doc": doc, "kind": kind, "text": text,  # noqa: E731
                                                         "pages": [page], "parent": parent}
    return [u("VOL-I:9.1", "VOL-I", "clause", "Envelope A shall contain, in the following order:", 4),
            u("VOL-I:9.1(a)", "VOL-I", "list_item", "(a) Form 4-A — Submission Letter;", 4, "VOL-I:9.1"),
            u("VOL-I:9.1(b)", "VOL-I", "list_item", "(b) Form 4-B — References;", 4, "VOL-I:9.1"),
            u("VOL-I:9.2", "VOL-I", "clause", "The narrative shall not exceed one hundred (100) pages. Standby pumps "
                                              "shall be provided for seventy-two (72) hours.", 4),
            u("ADD-01:cover/para1", "ADD-01", "paragraph", "Issued 1 October 2026", 1),
            u("ADD-01:3.1", "ADD-01", "clause", "A new Form 4-Z is added to the list at Volume I Clause 9.1, to be inserted "
                                                "after item (a): ‘(a1) Form 4-Z — Cyber Undertaking;’", 2),
            u("ADD-01:3.2", "ADD-01", "clause", "In Volume I Clause 9.2, ‘seventy-two (72) hours’ is deleted and "
                                                "‘ninety-six (96) hours’ is substituted.", 2)]


def _list_run():
    units = _list_units()
    of = OpFile.model_validate({
        "addendum": "ADD-01", "issued_from": "ADD-01:cover/para1", "prepared_by": "test", "method": "test",
        "ops": [{"id": "ADD-01/3.1", "provision": "ADD-01:3.1", "type": "insert_unit", "anchor": "VOL-I:9.1(a)",
                 "new_text": "(a1) Form 4-Z — Cyber Undertaking;"},
                {"id": "ADD-01/3.2", "provision": "ADD-01:3.2", "type": "replace_text", "target": "VOL-I:9.2",
                 "old": "seventy-two (72) hours", "new": "ninety-six (96) hours"}],
        "dispositions": [{"provision": "ADD-01:cover/para1", "disposition": "no_effect", "reason": "issue date"}]})
    base = {"discipline": "Bid management", "assessment": "pass_fail", "confidence": "high", "confidence_reason": "t",
            "scope": ["t"]}
    rf = RowFile.model_validate({"prepared_by": "t", "method": "t", "anchors": {}, "rows": [
        {**base, "id": "LIST", "group": "VOL-I:9.1", "requirement": "Envelope A in order",
         "units": ["VOL-I:9.1", "VOL-I:9.1(a)", "VOL-I:9.1(b)"],
         "interpretations": [{"stage": "BASE", "quote": "Envelope A shall contain"}]},
        {**base, "id": "ITEM-A", "group": "VOL-I:9.1", "requirement": "Form 4-A", "units": ["VOL-I:9.1(a)"],
         "interpretations": [{"stage": "BASE", "quote": "Form 4-A"}]},
        {**base, "id": "PAGES", "group": "VOL-I:9.2", "requirement": "page limit", "units": ["VOL-I:9.2"],
         "interpretations": [{"stage": "BASE", "quote": "shall not exceed one hundred (100) pages"},
                             {"stage": "ADD-01", "quote": "shall not exceed one hundred (100) pages",
                              "note": "re-read at ADD-01: 3.2 changes the standby sentence only"}]},
        {**base, "id": "PAGES-NOT-REREAD", "group": "VOL-I:9.2", "requirement": "page limit", "units": ["VOL-I:9.2"],
         "interpretations": [{"stage": "BASE", "quote": "shall not exceed one hundred (100) pages"}]},
        {**base, "id": "STANDBY", "group": "VOL-I:9.2", "requirement": "standby", "units": ["VOL-I:9.2"],
         "interpretations": [{"stage": "BASE", "quote": "seventy-two (72) hours"},
                             {"stage": "ADD-01", "quote": "ninety-six (96) hours"}]}]})
    stages = Engine(units, [of]).run()
    assert stages[1].status == "APPLIED", [x.checks for x in stages[1].ops]
    compute_pins(rf, stages)
    reg = Register(rf, stages)
    return {r.id: {s.stage: reg.evaluate(r, s) for s in stages} for r in rf.rows}, stages


# ------------------------------------------------------------------------------------------ A1-2 / A2-2

def test_a1_2_an_item_inserted_into_a_rows_list_amends_the_row_real(real, a1):
    ev = _ev(real, "VOL-I-9.1-01")
    assert [ev[s]["status"] for s in ("BASE", "ADD-01", "ADD-02")] == ["ACTIVE", "ACTIVE", "AMENDED (ADD-02/7.1)"]
    eff = _row(a1, "VOL-I-9.1-01")["effective_text"]
    i_e, i_g, i_f = eff.index("(e) Form 4-E"), eff.index("FORM 4-G"), eff.index("(f) the Technical Proposal")
    assert i_e < i_g < i_f, eff                                   # the inserted item in its position, after (e)
    assert "I-F4G-LETTERING" in _row(a1, "VOL-I-9.1-01")["issues"]
    assert _ev(real, "ADD-02-7.2-01")["ADD-02"]["status"].startswith("NEW")     # the inserted form keeps its own row


def test_a1_2_insertion_rule_synthetic():
    ev, _ = _list_run()
    assert ev["LIST"]["ADD-01"]["status"] == "AMENDED (ADD-01/3.1)"
    assert ev["ITEM-A"]["ADD-01"]["status"] == "ACTIVE"            # inserting after (a) does not change (a)
    refs = [d["unit"] for d in ev["LIST"]["ADD-01"]["units_detail"]]
    assert refs == ["VOL-I:9.1", "VOL-I:9.1(a)", "VOL-I:9.1(a)+ADD-01", "VOL-I:9.1(b)"]
    assert any(c.startswith("ADD-01/3.1 ") for c in ev["LIST"]["ADD-01"]["chain"])


# ------------------------------------------------------------------------------------------ A1-5 / A2-3

def test_a1_5_an_inserted_unit_is_labelled_with_the_addendums_page_real(real, a1, a2):
    chain = _ev(real, "ADD-02-7.2-01")["ADD-02"]["chain"]
    ins = next(c for c in chain if c.startswith("VOL-I:9.1(e)+ADD-02"))
    assert "VOL-I p3" not in ins and "ADD-02 p3" in ins and "inserted after VOL-I 9.1(e), p4" in ins, ins
    eff = _row(a1, "ADD-02-7.2-01")["effective_text"]
    assert "[ADD-02 p3 (inserted after VOL-I 9.1(e), p4)] FORM 4-G" in eff, eff
    assert "+ADD-02 (VOL-I p3" not in a2["markdown"] and "VOL-I:9.1(e)+ADD-02 (ADD-02 p3;" in a2["markdown"]


def test_a1_5_inserted_unit_label_synthetic():
    ev, _ = _list_run()
    d = next(x for x in ev["LIST"]["ADD-01"]["units_detail"] if x["unit"] == "VOL-I:9.1(a)+ADD-01")
    assert d["effective_ref"] == "ADD-01 p2 (inserted after VOL-I 9.1(a), p4)", d
    assert any(c.startswith("VOL-I:9.1(a)+ADD-01 (ADD-01 p2;") and "inserted after VOL-I 9.1(a), p4" in c
               for c in ev["LIST"]["ADD-01"]["chain"]), ev["LIST"]["ADD-01"]["chain"]


# ------------------------------------------------------------------------------------------ A1-8 / A2-6 (first part)

def test_a1_8_rows_reissued_or_untouched_are_not_amended_real(real, a2):
    for rid in ("VOL-I-T1-1-A", "VOL-I-T1-1-C", "VOL-I-T1-1-E", "VOL-I-T1-1-F"):
        assert _ev(real, rid)["ADD-02"]["status"] == "ACTIVE (reissued by ADD-02/3.1, unchanged)", rid
    for rid in ("VOL-I-T1-1-B", "VOL-I-T1-1-D"):
        assert _ev(real, rid)["ADD-02"]["status"] == "AMENDED (ADD-02/3.1)"
    assert not _ev(real, "VOL-II-4.4-02")["ADD-02"]["status"].startswith("AMENDED")
    assert "unchanged" in _ev(real, "VOL-II-4.4-02")["ADD-02"]["status"]
    assert _ev(real, "VOL-II-4.4-01")["ADD-02"]["status"] == "AMENDED (ADD-02/4.1)"
    moved = {(m["stage"], m["row"]): m for m in a2["rows_moved"]}
    assert moved[("ADD-02", "VOL-I-T1-1-A")]["after"].startswith("ACTIVE (reissued by ADD-02/3.1, unchanged)")


def test_a1_8_unchanged_rule_synthetic():
    ev, _ = _list_run()
    assert ev["STANDBY"]["ADD-01"]["status"] == "AMENDED (ADD-01/3.2)"
    st = ev["PAGES"]["ADD-01"]["status"]
    assert not st.startswith("AMENDED") and "ADD-01/3.2" in st and "unchanged" in st, st
    # a row nobody re-read against the amended unit is not declared unchanged (words elsewhere can change its meaning)
    assert ev["PAGES-NOT-REREAD"]["ADD-01"]["status"] == "AMENDED (ADD-01/3.2)"


# ------------------------------------------------------------------------------------------ A1-1 / A2-7

def test_a1_1_each_stages_change_is_in_a1_and_in_the_chain(real, a1, a2):
    keys = [c["key"] for c in a1["columns"]]
    assert "change:ADD-01" in keys and "change:ADD-02" in keys and "note" in keys
    assert "Change at" in a1["notice"]
    r52 = _row(a1, "VOL-I-5.2-01")
    assert "ADD-01 §2.2" in r52["change:ADD-01"] and "dates moved" in r52["change:ADD-01"], r52["change:ADD-01"]
    assert any(c.startswith("ADD-01/2.2 ") and "ADD-01 p1" in c for c in r52["chain"]), r52["chain"]
    assert "not subject to any cap" in _row(a1, "VOL-V-31.1-01")["change:ADD-02"]
    assert "Q5" in _row(a1, "VOL-I-8.5-01")["change:ADD-01"]
    r83 = _row(a1, "VOL-I-8.3-01")                                 # moved by the PDD anchor, not named in 2.2
    assert any(c.startswith("ADD-01/2.1 ") for c in r83["chain"]), r83["chain"]
    moved = {(m["stage"], m["row"]): m for m in a2["rows_moved"]}
    assert any(c.startswith("ADD-01/2.2 ") for c in moved[("ADD-01", "VOL-I-5.2-01")]["chain"])
    assert any(c.startswith("ADD-02/Q7 ") for c in moved[("ADD-02", "VOL-I-12.1-01")]["chain"])
    sec = a2["markdown"].split("## Evidence chains")[1]
    assert "**VOL-I-5.2-01**" in sec and "**VOL-I-8.3-01**" in sec
    for base_only in ("VOL-IV-F4B-01", "VOL-IV-F4D-01", "VOL-II-2.1-01", "VOL-I-6.5-02"):
        assert f"**{base_only}**" not in sec


# ------------------------------------------------------------------------------------------ A1-3 / A2-9

def test_a1_3_one_concession_wording_and_no_inverted_confidence(real, a1):
    rank = {"low": 0, "medium": 1, "high": 2}
    rows = {e["row"].id: e["row"] for e in real["evals"]}
    assert rank[rows["VOL-I-12.1-01"].confidence] >= rank[rows["VOL-V-3.1-01"].confidence]
    issue = real["curated_issues"]["I-CONCESSION"]["text"]
    texts = [issue, rows["VOL-I-12.1-01"].confidence_reason, rows["VOL-V-3.1-01"].confidence_reason,
             rows["VOL-V-3.2-01"].confidence_reason, rows["VOL-V-42.2-01"].confidence_reason]
    for t in texts:
        assert not re.search(r"\b(settled|declined|unresolved term start)\b", t, re.I), t
    assert "VOL-I 3.2" in rows["VOL-I-12.1-01"].confidence_reason and "prevail" in rows["VOL-I-12.1-01"].confidence_reason
    assert "CQ-CONCESSION-TERM" in issue and "Form 4-E" in issue


# ------------------------------------------------------------------------------------------ A1-4

def test_a1_4_an_assumption_is_never_shown_as_stated_in_the_pack(a1):
    rows = {x["key"]: x for x in a1["sheets"]["Assumptions"]["rows"]}
    b = rows["submission.usb_per_envelope"]["basis"]
    assert "PROVISIONAL ASSUMPTION" in b and "I-VOL-I-COPIES" in b and not b.startswith("stated in"), b
    assert rows["submission.hard_copies"]["basis"].startswith("stated in")


# ------------------------------------------------------------------------------------------ A1-6

def test_a1_6_the_delay_damages_cap_is_recorded_where_the_disposition_says(a1):
    r = _row(a1, "VOL-V-12.1-01")
    assert "ten per cent (10%) of the Estimated Project Cost" in r["note"] and "18.4" in r["note"], r["note"]


# ------------------------------------------------------------------------------------------ A1-7

def test_a1_7_evidence_codes_are_defined_in_a1(real, a1):
    ev = a1["sheets"]["Evidence"]["rows"]
    codes = {x["code"]: x for x in ev}
    used = {c for x in a1["rows"] for c in x["evidence"] if c.startswith("EV-")}
    assert used <= set(codes)
    assert codes["EV-DELIVERY"]["envelope"] == "A+B" and codes["EV-DELIVERY"]["name"]
    assert a1["evidence_items"]["EV-FORM-4G"]["name"].startswith("Form 4-G")


# ------------------------------------------------------------------------------------------ A1-9

def test_a1_9_no_dates_at_a_stage_where_the_row_is_not_in_force(real, a1):
    st = {(e["row"].id, s): v for e in real["evals"] for s, v in e["stages"].items()}
    for d in a1["sheets"]["Dates"]["rows"]:
        assert st[(d["row"], d["stage"])]["active"], d
    assert not [d for d in a1["sheets"]["Dates"]["rows"] if d["row"] == "ADD-01-3.1-01" and d["stage"] == "BASE"]


# ------------------------------------------------------------------------------------------ A1-10

def test_a1_10_assessment_values_defined_and_bid_out_rows_are_pass_fail(real, a1):
    for v in ("pass_fail", "scored", "procedural", "contractual_post_award"):
        assert f"{v} =" in a1["notice"], v
    from tenderpack.register import BID_OUT, Consequence
    for e in real["evals"]:
        row = e["row"]
        if any(isinstance(i.consequence, Consequence) and i.consequence.cls in BID_OUT for i in row.interpretations):
            assert row.assessment in ("pass_fail", "scored"), (row.id, row.assessment)
    rows = {e["row"].id: e["row"] for e in real["evals"]}
    assert rows["VOL-I-4.2-01"].assessment == rows["VOL-I-11.5-01"].assessment == "pass_fail"


# ------------------------------------------------------------------------------------------ A1-11

def test_a1_11_replaced_has_its_own_fill():
    fills = {status_fill(s) for s in ("REPLACED (by ADD-01:AppA)", "DELETED (ADD-01/4.1)", "ACTIVE", "AMENDED (X)",
                                       "NEW")}
    assert status_fill("REPLACED (by ADD-01:AppA)") is not None and len(fills) == 5


# ------------------------------------------------------------------------------------------ A2-1

def test_a2_1_added_and_reinstated_words_are_shown(a2):
    ch = {x["op"]: x["change"] for x in a2["changes"]}
    assert ch["ADD-01/5.1"].startswith("+ 'Glass reinforced plastic pipe") and ch["ADD-01/5.1"].endswith("this Clause.'")
    r = ch["ADD-02/9.1"]
    assert "thirty-five per cent (35%)" in r and "Failure to submit the certificate shall render the Proposal " \
                                                 "non-responsive." in r and "thirty per cent (30%)" in r, r
    assert all(v and v != "None" and "None" not in v.split() for v in ch.values()), [k for k, v in ch.items() if "None" in v]
    assert "FORM 4-G" in ch["ADD-02/7.1"]


# ------------------------------------------------------------------------------------------ A2-4

def test_a2_4_op_issues_are_on_the_page_untruncated(real, a2):
    md = a2["markdown"]
    q7 = next(x for s in real["stages"] for x in s.ops if x.op.id == "ADD-02/Q7").op
    assert q7.issue in md
    line = next(ln for ln in md.splitlines() if ln.startswith("| ADD-02/Q7 |"))
    assert "confirms, with open question" in line and "CQ-CONCESSION-TERM" in line and "I-CONCESSION" in line, line
    rows = [ln for ln in md.splitlines() if ln.startswith("| VOL-IV-F4A-01 |")]
    assert rows and "…" not in rows[0], rows


# ------------------------------------------------------------------------------------------ A2-5

def test_a2_5_blocks_travel_along_limit_links_and_op_documents_are_counted(real, a2):
    recs = real["relationship_impact"]["ADD-02"]["records"]
    for rid in ("VOL-II-3.1-01", "VOL-II-4.3-02", "VOL-II-7.2-01", "VOL-V-29.3-01", "VOL-V-31.1-02"):
        rec = next(x for x in recs if x["target"] == rid and x["kind"] == "limit_applies")
        assert any(b["entry_id"] == "REL-MISSING-ENVIRONMENTAL-PERMIT" for b in rec["blockers"]), rid
    rel = [x for x in a2["relationships"] if x["stage"] == "ADD-02" and x["target"] == "VOL-II-3.1-01"]
    assert rel and all("blocked_by" in x for x in rel) and "REL-MISSING-ENVIRONMENTAL-PERMIT" in " ".join(rel[0]["blocked_by"])
    sec = a2["markdown"].split("## ADD-01")[1].split("## ADD-02")[0]
    m = re.search(r"Referenced but not supplied[^\n]*\((\d+)\)", sec)
    assert m and int(m.group(1)) >= 1 and "geotechnical report" in sec.split("Referenced but not supplied")[1]


# ------------------------------------------------------------------------------------------ A2-6 (second part)

def test_a2_6_a_confirming_answer_is_not_an_understated_obligation(real):
    sc = next(x for x in real["summary_check"] if x["stage"] == "ADD-01")
    assert not [f for f in sc["findings"] if f["kind"] == "understated" and f.get("op") == "ADD-01/Q4"], sc["findings"]
    row = next(e["row"] for e in real["evals"] if e["row"].id == "ADD-01-Q4-01")
    assert "confirms VOL-I 5.5" in row.requirement and "VOL-I-5.5-01" in (row.interpretations[-1].note or "")
    x = next(x for s in real["stages"] for x in s.ops if x.op.id == "ADD-01/Q4")
    assert x.valid and x.details.get("answer_class", {}).get("restates") == ["VOL-I:5.5"]


# ------------------------------------------------------------------------------------------ A2-8

def test_a2_8_the_minutes_claim_matches_the_provision_that_publishes_them(real):
    sc = next(x for x in real["summary_check"] if x["stage"] == "ADD-01")
    c4 = next(c for c in sc["claims"] if c["text"].startswith("publishes the minutes"))
    assert "ADD-01:1.1" in c4["matched_provisions"] and any(p.startswith("ADD-01:AppB") for p in c4["matched_provisions"])


# ------------------------------------------------------------------------------------------ A2-10

def test_a2_10_earlier_ops_a_later_op_reverses_are_listed(a2):
    ans = [x for x in a2["answers"] if x["stage"] == "ADD-02"]
    assert any(x["answer"] == "ADD-01/4.1" and "ADD-02/9.1" in x["why"] for x in ans), ans
    assert any(x["answer"] == "ADD-01/4.2" and "ADD-02/9.2" in x["why"] for x in ans), ans
    assert any(x["answer"] == "ADD-01:Q2" for x in ans)
