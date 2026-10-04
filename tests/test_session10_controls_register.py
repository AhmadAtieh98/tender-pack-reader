"""Session 10, controls (owner's section 1, bullets 2 and 4).

A1 (register.py). The removal validator accepted `removed: {by: <op>}` on a row whose quoted words SURVIVE the op: it
checked that the op changed one of the row's units and that the quote was in the unit before the op, not that the quote
went with the words the op removed. Blind rehearsal 02's ADD-03 4.1 deleted only the model-auditor words from VOL-I 10.3;
marking the surviving Financial Model row (VOL-I-10.3-01) removed by that op passed, took the row out of force and
dropped it from A3's gate and from the A5 activities that plan it. A removal is now valid only if the row's quote is in
one of the op's units immediately before the op and absent from the same unit immediately after it; otherwise the
finding says that the row's words survive the op and the row stays in force (status, consequence, A5 activities).

A2 (clarify.py). clarify.check() accepted a source whose `words` were "" or whitespace (found("", text) is True) and a
`decision_owner` of whitespace only. Both are findings now (unit, page and words required and non-blank after strip;
every required field non-blank).

Each regression was run on the code before the fix and failed (recorded in the session report). Nothing here writes to
the repository: the blind rehearsal 02 case runs on a disposable copy of its curation and a fresh ingest in a tmp dir.
"""
from __future__ import annotations

import copy
import re
import shutil

import pytest

from tenderpack import clarify, stage2
from tenderpack.amend import Engine, OpFile
from tenderpack.dates import Calendar
from tenderpack.register import Register, RowFile
from tenderpack.schedule import in_force
from tenderpack.util import ROOT

# ---------------------------------------------------------------------------------------------- A1: synthetic units

OPINION = ", and shall be accompanied by an opinion from an independent model auditor"
SUBMIT = "The Financial Model shall be submitted in Excel"
CONSEQ = "A Proposal without a Financial Model shall be rejected."


def _stages():
    u = lambda uid, doc, kind, text: {"unit_id": uid, "doc": doc, "kind": kind, "text": text, "pages": [1]}  # noqa: E731
    units = [u("VOL-I:10.3", "VOL-I", "clause", f"{SUBMIT}{OPINION}. {CONSEQ}"),
             u("ADD-01:cover/para1", "ADD-01", "paragraph", "Issued 3 November 2026"),
             u("ADD-01:4.1", "ADD-01", "clause", f"In Volume I Clause 10.3, the words '{OPINION}' are deleted.")]
    f = OpFile.model_validate({"addendum": "ADD-01", "issued_from": "ADD-01:cover/para1", "prepared_by": "test", "method": "test",
                               "ops": [{"id": "ADD-01/4.1", "provision": "ADD-01:4.1", "type": "replace_text",
                                        "target": "VOL-I:10.3", "old": OPINION, "new": ""}],
                               "dispositions": [{"provision": "ADD-01:cover/para1", "disposition": "no_effect",
                                                 "reason": "issue date"}]})
    stages = Engine(units, [f]).run()
    assert stages[-1].status == "APPLIED"
    return stages


def _row(rid: str, quote: str, later: dict | None, consequence: dict | None = None) -> dict:
    base = {"stage": "BASE", "quote": quote, **({"consequence": consequence} if consequence else {})}
    interps = [base] + ([{"stage": "ADD-01", "quote": quote, **({"consequence": consequence} if consequence else {}),
                          **later}] if later is not None else [])
    return {"id": rid, "group": "VOL-I:10.3", "scope": ["financial_model"], "requirement": rid, "units": ["VOL-I:10.3"],
            "discipline": "Finance", "assessment": "pass_fail", "evidence": ["EV-FIN-MODEL"], "interpretations": interps,
            "confidence": "high", "confidence_reason": "test"}


def _evaluate(rows: list[dict], stage: int = 1):
    stages = _stages()
    rf = RowFile.model_validate({"prepared_by": "test", "method": "test", "anchors": {}, "rows": rows})
    reg = Register(rf, stages, Calendar())
    return {r.id: reg.evaluate(r, stages[stage]) for r in rf.rows}


REJECT = {"class": "rejection", "unit": "VOL-I:10.3", "quote": CONSEQ}


def test_a1_a_removal_of_words_that_survive_the_op_is_a_finding_and_the_row_stays_in_force():
    """The finding, reproduced: before the fix this row was 'REMOVED (ADD-01/4.1)', out of force, with no problem."""
    ev = _evaluate([_row("VOL-I-10.3-01", SUBMIT, {"removed": {"by": "ADD-01/4.1"}}, REJECT)])["VOL-I-10.3-01"]
    assert any("the row's words survive the op" in p for p in ev["problems"]), ev["problems"]
    assert ev["status"] == "AMENDED (ADD-01/4.1)" and ev["active"] and in_force(ev["status"]), ev["status"]
    assert ev["consequence_source"] is not None                  # its consequence is still read and sourced
    assert not any("survive" in x for x in ev["stale"])          # the finding is never explained away as STALE


def test_a1_a_removal_of_the_words_the_op_deleted_is_still_valid():
    ev = _evaluate([_row("VOL-I-10.3-02", OPINION.lstrip(", "), {"removed": {"by": "ADD-01/4.1"}})])["VOL-I-10.3-02"]
    assert ev["status"] == "REMOVED (ADD-01/4.1)" and not ev["active"] and ev["problems"] == [] and ev["stale"] == []


def test_a1_a_quote_straddling_the_deleted_words_is_removed_with_them():
    straddle = "submitted in Excel, and shall be accompanied by an opinion"
    ev = _evaluate([_row("R-1", straddle, {"removed": {"by": "ADD-01/4.1"}})])["R-1"]
    assert ev["status"] == "REMOVED (ADD-01/4.1)" and ev["problems"] == []


def test_a1_the_other_removal_checks_still_hold_and_an_unsupported_removal_keeps_the_row_in_force():
    for removed, why in (({"by": "ADD-01/9.9"}, "no op of the amendment path"),):
        ev = _evaluate([_row("R-1", SUBMIT, {"removed": removed})])["R-1"]
        assert any(why in p for p in ev["problems"]) and in_force(ev["status"]), (ev["status"], ev["problems"])
    ev = _evaluate([_row("R-1", "shall be certified by the Authority", {"removed": {"by": "ADD-01/4.1"}})])["R-1"]
    assert any("as it stood before the op" in p for p in ev["problems"]), ev["problems"]


# ---------------------------------------------------------------------------------------------- A1: blind rehearsal 02

@pytest.fixture(scope="module")
def blind02_copy(tmp_path_factory, blind02_build):
    """A disposable copy of blind rehearsal 02's curation in which the SURVIVING Financial Model row VOL-I-10.3-01 is
    marked removed by ADD-03/4.1 (which deleted only the model-auditor words from VOL-I 10.3), evaluated on the session's
    disposable ingest of the pack (tests/conftest.py). Only the copy is changed."""
    tmp = tmp_path_factory.mktemp("blind02-removal")
    build = blind02_build
    work = tmp / "work"
    shutil.copytree(ROOT / "rehearsals/blind-02/work", work)
    pack = work / "pack.yaml"
    pack.write_text(pack.read_text(encoding="utf-8").replace("rehearsals/blind-02/work/", f"{work}/"), encoding="utf-8")
    rows = work / "register/rows/VOL-I.yaml"
    text = rows.read_text(encoding="utf-8")
    start = text.index("  - id: VOL-I-10.3-01\n")
    end = text.index("  - id: ", start + 10)
    block = text[start:end]
    marked = re.sub(r"(\n      - stage: ADD-03\n)", r"\1        removed: {by: ADD-03/4.1, note: 'disposable test copy'}\n", block)
    assert marked != block
    rows.write_text(text[:start] + marked + text[end:], encoding="utf-8")
    return stage2.run(build, pack, ROOT)


def _ev(r, rid, stage):
    return next(e for e in r["evals"] if e["row"].id == rid)["stages"][stage]


def test_a1_blind02_the_surviving_financial_model_row_cannot_be_removed_by_4_1(blind02_copy):
    r = blind02_copy
    ev = _ev(r, "VOL-I-10.3-01", "ADD-03")
    assert any("the row's words survive the op" in p for p in ev["problems"]), ev["problems"]
    assert ev["status"].startswith("AMENDED (ADD-03/4.1") and ev["active"], ev["status"]
    assert [f for f in stage2.register_findings(r) if f["where"] == "VOL-I-10.3-01" and "survive" in f["detail"]]
    # the model-auditor row, whose words 4.1 did delete, is still validly removed
    op = _ev(r, "VOL-I-10.3-02", "ADD-03")
    assert op["status"] == "REMOVED (ADD-03/4.1)" and op["problems"] == []


def test_a1_blind02_the_surviving_row_keeps_its_a5_activities_and_its_place_in_the_a3_gate(blind02_copy):
    r = blind02_copy
    progs = stage2.a5_all(r)
    acts = {a["id"]: a for a in progs["ADD-03"]["activities"]}
    for aid in ("fin-model-build", "fin-model-freeze"):
        assert "VOL-I-10.3-01" in acts[aid]["req_ids"], (aid, acts[aid]["req_ids"])
    a3 = stage2.a3(r, stage2.collect_issues(r, progs["ADD-03"]), progs["ADD-03"])
    assert "VOL-I-10.3-01" in a3["none_stated_ids"]


# ---------------------------------------------------------------------------------------------- A2: clarify.check

UNITS = [{"unit_id": "VOL-I:5.2", "doc": "VOL-I", "pages": [3],
          "text": "Requests for clarification shall be submitted no later than ten (10) Working Days before the Proposal Due Date."}]
ENTRY = {"id": "CQ-SYN", "kind": "ambiguity", "volume": "Volume I", "clause": "5.2", "page": 3, "gap": "g",
         "practical_impact": "p", "proposed_question": "Volume I, Clause 5.2, page 3: ...", "interim_handling": "h",
         "decision_owner": "Bid manager", "response_status": "draft, not sent", "theme": "submission",
         "sources": [{"unit": "VOL-I:5.2", "page": 3, "words": "ten (10) Working Days before the Proposal Due Date"}]}


def _check(**changes):
    entry = {**copy.deepcopy(ENTRY), **changes}
    return clarify.check({"clarifications": [entry]}, UNITS, set())


def test_a2_the_complete_entry_passes():
    assert _check() == []


@pytest.mark.parametrize("words", ["", "   ", "\n\t "])
def test_a2_an_empty_or_blank_source_quotation_is_a_finding(words):
    found = _check(sources=[{"unit": "VOL-I:5.2", "page": 3, "words": words}])
    assert any("CQ-SYN" in f and "empty quotation" in f for f in found), found


@pytest.mark.parametrize("missing", [{"unit": " "}, {"page": None}, {"page": " "}])
def test_a2_a_source_without_unit_or_page_is_a_finding(missing):
    src = {"unit": "VOL-I:5.2", "page": 3, "words": "ten (10) Working Days", **missing}
    found = _check(sources=[src])
    assert any("CQ-SYN" in f and "needs a unit, a page and the words" in f for f in found), found


@pytest.mark.parametrize("owner", ["   ", "\t", "\n"])
def test_a2_a_whitespace_only_decision_owner_is_a_finding(owner):
    found = _check(decision_owner=owner)
    assert any("CQ-SYN" in f and "decision_owner" in f for f in found), found


def test_a2_blank_answer_words_and_blank_unavailable_material_quotes_are_findings():
    ans = {"unit": "VOL-I:5.2", "page": 3, "words": "  "}
    assert any("without answer evidence" in f or "empty quotation" in f
               for f in _check(response_status="answered by addendum", answer=ans))
    reg = {"clarifications": [copy.deepcopy(ENTRY)],
           "unavailable_material": [{"item": "X", "referenced_in": [{"unit": "VOL-I:5.2", "page": 3, "words": ""}]}]}
    assert any("unavailable_material[X]" in f and "empty quotation" in f for f in clarify.check(reg, UNITS, set()))


def test_a2_the_real_and_rehearsal_registers_have_no_blank_quotes_or_owners():
    from tenderpack.util import load_yaml
    for p in ("curation/clarifications/register.yaml", "rehearsals/blind-02/work/clarifications/register.yaml",
              "rehearsals/blind-03/work/clarifications/register.yaml"):
        reg = load_yaml(ROOT / p)
        for c in reg.get("clarifications") or []:
            assert str(c.get("decision_owner") or "").strip(), (p, c.get("id"))
            for q in c.get("sources") or []:
                assert str(q.get("words") or "").strip() and str(q.get("unit") or "").strip(), (p, c.get("id"))
