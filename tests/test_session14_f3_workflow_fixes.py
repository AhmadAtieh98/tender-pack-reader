"""Session 14 (F3): the workflow fixes the blind-07 regression's scorer prompted (rehearsals/blind-07/regression-s14/
COMPARISON-S14.md §9 N1-N12, §8 defects 11 and 15, §10). Each test reproduces a defect first.

  N1   a forward-counted deadline with two readings ("within three (3) Working Days of the date of this Addendum") lost
       its planning value (the row carried kind 'unresolved'), and a new request activity was made a predecessor of an
       activity that must finish before the request's window opens
  N7   an exception in the programme check was reported as the finding "C45: the programme cannot be planned with the
       proposals: AttributeError: 'str' object has no attribute 'get'" (an activity's `finish` given as a string)

The workspace is blind rehearsal 05's committed candidate (tests/fixtures/s12_blind05.py, ingested into tmp); the items
are this test's data (synthetic, labelled), never the truth about the tender."""
from __future__ import annotations

import copy
from datetime import date
from pathlib import Path

import pytest

import s12_w3b as W
from tenderpack import dates
from tenderpack.ai import downstream as DS
from tenderpack.ai.contract import EvidenceRef

ROOT = Path(__file__).resolve().parents[1]
TEST = "(session 14 test data)"
FWD = "within three (3) Working Days of the date of this Addendum"


@pytest.fixture(scope="module")
def ws(tmp_path_factory):
    return W.workspace(tmp_path_factory)


@pytest.fixture(scope="module")
def prom(ws):
    return W.promoted(ws)


# ---------------------------------------------------------------------------------------------- N1

COMPUTED = [{"unit": "ADD-03:4.3", "pages": [2], "words": FWD, "anchor": "ADD-03-issue", "anchor_date": "2026-11-17",
             "result": {"status": "ambiguous", "value": None, "escalate": True,
                        "readings": [{"key": "event_day_excluded", "value": "2026-11-22"},
                                     {"key": "event_day_counted", "value": "2026-11-19"}]},
             "date_rule": {"kind": "relative", "purpose": "deadline", "anchor": "ADD-03-issue", "offset": 3,
                           "unit": "working_day", "direction": "after", "source_unit": "ADD-03:4.3", "text": FWD}}]


def _row(rules):
    return {"id": "ADD-03-4.3-01", "date_rules": rules}


def test_N1_a_forward_count_written_unresolved_is_planned_at_the_earlier_reading_with_the_later_kept():
    # the blind-07 run's own rule (frozen shape): kind 'unresolved' with the two readings in its note
    row = _row([{"rule_id": "ADD03-4.3-request", "kind": "unresolved", "purpose": "deadline", "source_unit": "ADD-03:4.3",
                 "text": FWD, "note": "ambiguous counting: 2026-11-19 if the issue day counts or 2026-11-22 if it "
                                      f"does not. Escalated; not chosen. {TEST}"}])
    notes = DS.program_counted_rules(row, COMPUTED)
    assert notes and "ADD03-4.3-request" in notes[0] and "earlier" in notes[0], notes
    rd = row["date_rules"][0]
    assert rd["kind"] == "relative" and rd["rule_id"] == "ADD03-4.3-request" and rd["anchor"] == "ADD-03-issue"
    assert rd["direction"] == "after" and rd["offset"] == 3 and rd["text"] == FWD
    rule = dates.DateRule(**rd)
    its = dates.interpretations(rule, {"ADD-03-issue": date(2026, 11, 17)}, dates.Calendar(weekend={4, 5}))
    assert dates.planning_value(rule, its).value == date(2026, 11, 19)
    assert date(2026, 11, 22) in {x.value for x in its}                  # the later reading is kept


def test_N1_a_words_the_program_did_not_count_stay_unresolved():
    other = {"rule_id": "X", "kind": "unresolved", "purpose": "deadline", "source_unit": "ADD-03:4.3",
             "text": "promptly after the site visit", "note": f"an event with no date {TEST}"}
    row = _row([dict(other)])
    assert DS.program_counted_rules(row, COMPUTED) == [] and row["date_rules"][0] == other
    row = _row([dict(other, source_unit="ADD-03:9.9", text=FWD)])        # same words, another unit: not the program's
    assert DS.program_counted_rules(row, COMPUTED) == [] and row["date_rules"][0]["kind"] == "unresolved"


def test_N1_a_the_policy_asks_for_the_relative_rule_when_the_counting_is_ambiguous():
    pol = (ROOT / "tenderpack/ai/policy/60_derived.md").read_text(encoding="utf-8")
    assert "never kind 'unresolved'" in pol and "earlier reading" in pol
    src = (ROOT / "tenderpack/ai/derived_tasks.py").read_text(encoding="utf-8")
    assert "carry the relative `date_rule` unchanged all the same" in src


def _ev(unit, words, page=3):
    return EvidenceRef(doc=unit.split(":")[0], unit_id=unit, page=page, kind="span", words=words)


NEW_ROW = {"id": "ADD-03-7.3-T1", "group": "procedure", "scope": ["Bidder"],
           "requirement": f"Portal notice of the zone and height (test data) {TEST}", "units": ["ADD-03:7.3"],
           "discipline": "Technical", "assessment": "procedural", "evidence": ["EV-TEST-NOTICE"],
           "interpretations": [{"stage": "ADD-03", "quote": "shall notify the Authority through the Portal"}],
           "confidence": "medium", "confidence_reason": "test data",
           "introduced": {"stage": "ADD-03", "by": "ADD-03:7.3",
                          "evidence": {"unit": "ADD-03:7.3", "page": 3,
                                       "words": "shall notify the Authority through the Portal"}}}


def _items(act_extra):
    act = {"id": "test-notice", "name": f"Send the Portal notice {TEST}", "owner": "Technical", "discipline": "Technical",
           "resource": "technical_lead", "issuer": "Bidder", "duration": "test_notice", "per": "proposal",
           "predecessors": [], **act_extra}
    words = "shall notify the Authority through the Portal"
    return [
        {"id": "T-ROW", "statement_type": "row_new", "task": "date:ADD-03:7.3", "provision": "ADD-03:7.3",
         "payload": {"row": copy.deepcopy(NEW_ROW)}, "evidence": [_ev("ADD-03:7.3", words)]},
        {"id": "T-EV", "statement_type": "evidence_item", "task": "date:ADD-03:7.3", "provision": "ADD-03:7.3",
         "payload": {"id": "EV-TEST-NOTICE", "item": {"name": f"Portal notice {TEST}", "envelope": "none",
                                                      "issuer": "Bidder", "per": "proposal", "source": "ADD-03:7.3"}},
         "evidence": [_ev("ADD-03:7.3", words)]},
        {"id": "T-ACT", "statement_type": "activity", "task": "date:ADD-03:7.3", "provision": "ADD-03:7.3",
         "payload": {"evidence_item": "EV-TEST-NOTICE", "activity": act, "rows": ["ADD-03-7.3-T1"],
                     "duration_assumption": {"key": "test_notice", "value": 1, "owner": "Technical",
                                             "basis": f"PROVISIONAL ASSUMPTION: one Working Day {TEST}"}},
         "evidence": [_ev("ADD-03:7.3", words)]}]


def test_N1_b_a_new_activity_is_never_made_a_predecessor_of_one_that_must_finish_before_its_window_opens(ws, prom):
    # blind-05's ADD-03 is issued 2026-11-15; pcg-wording must finish by 2026-11-09 at ADD-03, technical-proposal by
    # 2026-11-23: the notice (a new obligation of ADD-03) can feed the second, never the first
    ds = W.dset(ws, _items({"successors": ["pcg-wording", "technical-proposal"]}))
    DS.validate(ws, ds, prom, {"date:ADD-03:7.3": "computed_date"})
    act = next(x for x in ds.items if x.id == "T-ACT")
    assert act.payload["activity"]["successors"] == ["technical-proposal"], act.payload["activity"]
    rec = next((v for v in act.validation if v.check == "successors (window)"), None)
    assert rec is not None and "pcg-wording" in rec.detail and "2026-11-15" in rec.detail, act.validation


# ---------------------------------------------------------------------------------------------- N7

def test_N7_an_activity_whose_finish_is_a_string_gets_a_named_finding_and_the_programme_is_still_checked(ws, prom):
    # the blind-07 run's shape (frozen): "finish": "milestone" on a proposed activity
    ds = W.dset(ws, _items({"successors": [], "finish": "milestone"}))
    rep = DS.validate(ws, ds, prom, {"date:ADD-03:7.3": "computed_date"})
    act = next(x for x in ds.items if x.id == "T-ACT")
    bad = [v for v in act.validation if v.check == "activity shape" and not v.ok]
    assert bad and "finish" in bad[0].detail and "milestone" in bad[0].detail, act.validation
    assert act.verification_status == "invalid"
    allp = " ".join(rep.get("schedule_problems") or []) + " ".join(rep.get("interactions") or [])
    assert "cannot be planned" not in allp and "AttributeError" not in allp, allp


def test_N7_an_exception_in_the_programme_check_is_never_a_programme_finding(ws, prom, monkeypatch):
    def boom(*a, **k):
        raise AttributeError("'str' object has no attribute 'get'")
    monkeypatch.setattr(DS, "_plan_problems", boom)
    ds = W.dset(ws, _items({"successors": []}))
    rep = DS.validate(ws, ds, prom, {"date:ADD-03:7.3": "computed_date"})
    assert not any(str(p).startswith("C45") for p in rep.get("schedule_problems") or []), rep["schedule_problems"]
    assert not any("C45: the programme cannot be planned" in str(p) for p in rep.get("interactions") or [])
    assert "software limitation" in str(rep.get("programme_check")), rep.get("programme_check")
    act = next(x for x in ds.items if x.id == "T-ACT")
    rec = next(v for v in act.validation if v.check == "C40/C44/C45")
    assert not rec.ok and "not checked" in rec.detail and "AttributeError" in rec.detail


# ---------------------------------------------------------------------------------------------- N2 + N3

def _tasks_one_obligation():
    # the blind-07 run's task shapes (frozen ids): one obligation reached downstream as c46:, oblig:, ana: and date:
    return [
        {"id": "c46:ADD-03/4.1", "kind": "row_new", "op": "ADD-03/4.1", "provisions": ["ADD-03:4.1"],
         "units_changed": ["VOL-V:12.4+ADD-03"], "outputs": [], "details": [], "rows": [],
         "analysis_items": [{"item": "ADD-03/4.1/row"}]},
        {"id": "oblig:ADD-03/4.1", "kind": "obligation_impact", "op": "ADD-03/4.1", "provisions": ["ADD-03:4.1"],
         "units_changed": ["VOL-V:12.4+ADD-03"], "terms": ["Scheduled PCOD"], "related": {"units": [], "rows": []},
         "expect": "a hint only"},
        {"id": "ana:ADD-03/Q17/row-dscr", "kind": "row_new", "provisions": ["ADD-03:Q17"], "units_changed": [],
         "analysis_items": [{"item": "ADD-03/Q17/row-dscr"}]},
        {"id": "oblig:ADD-03/Q17(b)", "kind": "obligation_impact", "op": "ADD-03/Q17(b)", "provisions": ["ADD-03:Q17"],
         "units_changed": [], "terms": [], "related": {}, "expect": "a hint only"},
        {"id": "ana:ADD-03/4.3/row", "kind": "row_new", "provisions": ["ADD-03:4.3"], "units_changed": [],
         "analysis_items": [{"item": "ADD-03/4.3/row"}]},
        {"id": f"date:ADD-03:4.3:{FWD}", "kind": "computed_date", "unit": "ADD-03:4.3", "words": FWD,
         "date_rule": COMPUTED[0]["date_rule"], "status": "ambiguous", "computed_from": {}},
        {"id": "oblig:ADD-03/9.9", "kind": "obligation_impact", "op": "ADD-03/9.9", "provisions": ["ADD-03:9.9"],
         "units_changed": [], "terms": [], "related": {}, "expect": "a hint only"}]


def test_N2_one_obligation_gets_one_task_with_its_origins_recorded():
    out = DS.merge_obligation_tasks(_tasks_one_obligation())
    ids = [t["id"] for t in out]
    assert ids == ["c46:ADD-03/4.1", "ana:ADD-03/Q17/row-dscr", "ana:ADD-03/4.3/row", "oblig:ADD-03/9.9"], ids
    c46 = out[0]
    assert c46["origins"] == ["c46:ADD-03/4.1", "oblig:ADD-03/4.1", "ana:ADD-03/4.1/row"], c46["origins"]
    assert c46["obligation"]["terms"] == ["Scheduled PCOD"] and c46["obligation"]["op"] == "ADD-03/4.1"
    assert out[1]["origins"] == ["ana:ADD-03/Q17/row-dscr", "oblig:ADD-03/Q17(b)"]
    assert out[2]["origins"][1].startswith("date:ADD-03:4.3") and out[2]["computed_dates"][0]["words"] == FWD
    assert "origins" not in out[3]                        # an obligation no row task names keeps its own task


def test_N2_an_answer_to_a_merged_task_still_names_a_task_of_the_packet():
    """session 14 (N2, the s11 downstream run): a model (or a recorded answer) that answers the obligation task by its
    own id (`oblig:<op>`, now merged into the row task) is answering a task of the packet: the request layer and the
    validation take the merged task's origins as its ids (the origin's own kind decides where `no_change` may answer)."""
    from tenderpack.ai import requests as RQ
    tasks = DS.merge_obligation_tasks(_tasks_one_obligation())
    ids = DS.task_kinds(tasks)
    assert ids["oblig:ADD-03/4.1"] == "obligation_impact" and ids["c46:ADD-03/4.1"] == "row_new", ids
    assert ids[f"date:ADD-03:4.3:{FWD}"] == "computed_date"
    assert DS.task_aliases(tasks)["oblig:ADD-03/4.1"] == "c46:ADD-03/4.1"
    packet = {"tasks": tasks}
    known = RQ.packet_task_ids(packet)
    assert {"oblig:ADD-03/4.1", "c46:ADD-03/4.1", "ana:ADD-03/4.1/row"} <= known, known


def _it(iid, task, status, rid, st="row_new"):
    from types import SimpleNamespace as NS
    return NS(id=iid, task=task, statement_type=st, verification_status=status, validation=[],
              payload={"row": {"id": rid}} if st == "row_new" else {"id": rid})


def test_N2_a_promoted_row_never_reads_invalid_because_of_a_later_duplicate():
    items = [_it("DS-ADD03-4.1-row", "c46:ADD-03/4.1", "interpretation_pending", "ADD-03-4.1-01"),
             _it("DS-41-ROW", "oblig:ADD-03/4.1", "invalid", "ADD-03-4.1-01"),
             _it("DS-X", "c46:X", "invalid", "ADD-03-X-01")]
    st = DS.row_item_status(items)
    assert st == {"ADD-03-4.1-01": "interpretation_pending", "ADD-03-X-01": "invalid"}, st


def test_N2_a_second_proposal_of_the_same_row_is_named_a_duplicate(ws, prom):
    its = _items({"successors": []})
    dup = copy.deepcopy(its[0])
    dup["id"], dup["task"] = "T-ROW-AGAIN", "date:ADD-03:7.3"
    ds = W.dset(ws, its + [dup])
    rep = DS.validate(ws, ds, prom, {"date:ADD-03:7.3": "computed_date"})
    again = next(x for x in ds.items if x.id == "T-ROW-AGAIN")
    rec = next((v for v in again.validation if v.check == "duplicate"), None)
    assert rec is not None and "T-ROW" in rec.detail and "duplicate" in rec.detail, again.validation
    assert not any(v.check == "id" and not v.ok for v in again.validation)
    assert rep["duplicates"] == {"T-ROW-AGAIN": "T-ROW"}
    first = next(x for x in ds.items if x.id == "T-ROW")
    assert DS.row_item_status(ds.items)["ADD-03-7.3-T1"] == first.verification_status


def test_N3_a_provision_whose_obligation_row_is_promoted_is_applied_and_names_the_row():
    from types import SimpleNamespace as NS
    from tenderpack.ai import workflow as WF
    tasks = [{"id": "ana:ADD-03/4.3/row", "analysis_items": [{"item": "ADD-03/4.3/row"}]}]
    ds = NS(items=[_it("DS-ADD03-4.3-row", "ana:ADD-03/4.3/row", "interpretation_pending", "ADD-03-4.3-01"),
                   _it("DS-ADD03-4.3-ev", "ana:ADD-03/4.3/row", "evidence_verified", "EV-X", st="evidence_item")])
    a = WF.carried_answer(["ADD-03/4.3/row"], tasks, ds, {})
    assert a["answered"] and a["applied_by_rows"] == ["ADD-03-4.3-01"] and "ADD-03-4.3-01" in a["why"], a
    assert WF.state_of({**a, "state": "applied"}).startswith("applied")
    d = DS.applied_row_disposition("ADD-03:4.3", a["applied_by_rows"], f"origin {TEST}")
    assert d.disposition != "unresolved" and "ADD-03-4.3-01" in d.reason and "PROPOSED" in d.reason
    # a row held back (not promotable) leaves the provision unresolved, as before
    a2 = WF.carried_answer(["ADD-03/4.3/row"], tasks, ds, {"DS-ADD03-4.3-row": "held: test", "DS-ADD03-4.3-ev": "held"})
    assert not a2["answered"] and not a2.get("applied_by_rows")


# ---------------------------------------------------------------------------------------------- defect 11 (§10)

RULE_TEXTS = {"ADD-03:3.5": "Table 42-1 is issued in the Arabic language. The Arabic text governs. The English "
                            "translation at Appendix B is provided for convenience only.",
              "ADD-03:p3-image": "(test data) the Arabic table", "ADD-03:T42-1": "(test data) the translation"}
# the blind-07 run's own op (frozen shape: candidate-curation/amendments/ADD-03.yaml)
OP35 = {"id": "ADD-03/3.5", "provision": "ADD-03:3.5", "type": "annotate", "targets": ["ADD-03:p3-image", "ADD-03:T42-1"],
        "effect": "interprets", "precedence": {"governs": "ADD-03:p3-image", "over": ["ADD-03:T42-1"],
                                               "words": "The Arabic text governs."}}


def _ci(iid, st, prov, payload, conflicts=()):
    from types import SimpleNamespace as NS
    return NS(id=iid, statement_type=st, provision=prov, payload=payload, conflicts=list(conflicts))


def test_11_the_stated_precedence_op_is_applied_not_handed_to_a_person():
    from tenderpack.ai import controller as C
    ar = C.applied_rule_review("amendment_op", OP35, "ADD-03:3.5", RULE_TEXTS, "ADD-03", list(RULE_TEXTS))
    assert not ar["human"], ar
    assert ar["lines"] and "The Arabic text governs." in ar["lines"][0] and "(applied, not decided)" in ar["lines"][0]
    # words that are not in the provision state no rule: the classifier's answer stands
    bad = dict(OP35, precedence={**OP35["precedence"], "words": "The English text governs."})
    assert C.applied_rule_review("amendment_op", bad, "ADD-03:3.5", RULE_TEXTS, "ADD-03", list(RULE_TEXTS))["human"]


def test_11_items_between_the_two_renderings_are_applied_by_the_one_rule_and_a_genuine_ambiguity_stays_pending():
    from tenderpack.ai import controller as C
    rules = C.stated_precedences([_ci("ADD-03/3.5", "amendment_op", "ADD-03:3.5", OP35)], RULE_TEXTS)
    assert len(rules) == 1 and rules[0]["governs"] == "ADD-03:p3-image"
    t4 = "ambiguous: the translation prints 'Minimum residual life (years): 5' while the Arabic row as read prints 7 " + TEST
    s = C.rendering_settled("ADD-03:T42-1/4", ["ADD-03:p3-image/r4"], t4, rules)
    assert s is not None and s["side"] == "convenience" and "(applied, not decided)" in s["line"]
    r4 = ("ambiguous: the Arabic row 4 prints seven years, while the Appendix B translation row ADD-03:T42-1/4 prints 5. "
          "Reading A: 7 years, under ADD-03:3.5. Reading B: 5 years, as the translation states. " + TEST)
    assert C.rendering_settled("ADD-03:p3-image/r4", C.named_units(r4), r4, rules)["side"] == "governing"
    assert C.rendering_settled("ADD-03:T42-1/note(4)", ["ADD-03:p3-image"], "note (4) " + TEST, rules) is not None
    # a genuine judgment stays pending: two readings of the same words, or a third text in conflict
    two = "the Arabic cell can be read as months or as years under its column heading " + TEST
    assert C.rendering_settled("ADD-03:p3-image/r5", ["ADD-03:T42-1/5"], two, rules) is None
    assert C.rendering_settled("ADD-03:T42-1/4", ["ADD-03:p3-image/r4", "VOL-V:42.1"], t4, rules) is None
    assert C.rendering_settled("VOL-V:42.1", ["ADD-03:p3-image/r4"], t4, rules) is None


def test_11_a_settled_unresolved_disposition_is_promoted_as_applied_with_the_rule_a_person_confirms():
    from tenderpack.amend import Disposition
    from tenderpack.ai import controller as C
    rules = C.stated_precedences([_ci("ADD-03/3.5", "amendment_op", "ADD-03:3.5", OP35)], RULE_TEXTS)
    t4 = "ambiguous: the translation prints 5 while the Arabic row prints 7 " + TEST
    s = C.rendering_settled("ADD-03:T42-1/4", ["ADD-03:p3-image/r4"], t4, rules)
    rec = C.rendering_record(s, "ADD-03:T42-1/4")
    d = DS.re_present_disposition(Disposition(provision="ADD-03:T42-1/4", disposition="unresolved", reason=t4),
                                  [rec])
    assert d.disposition == "no_effect" and "(applied, not decided)" in d.reason and C.CONFIRM in d.reason
    assert "proposed reason" in d.reason and t4 in d.reason
    keep = Disposition(provision="ADD-03:p3-image/r5", disposition="unresolved", reason="two readings " + TEST)
    assert DS.re_present_disposition(keep, []) == keep


# ---------------------------------------------------------------------------------------------- N4

def test_N4_a_trigger_word_inside_a_quotation_decides_nothing():
    from tenderpack import human_owned as H
    # the blind-07 shape (DS-10, DS-11): the governing-language rule quoted in the model's prose
    q = ("Row 4 of the table is read as printed; ADD-03 3.5 states 'The Arabic text governs.' and the row follows "
         f"that text {TEST}")
    assert H.triggers(q) == [], H.triggers(q)
    assert H.triggers(f"In our reading the Arabic text governs the row {TEST}")       # its own words still count


def test_N4_unless_in_a_reference_recital_is_not_amendment_language():
    from tenderpack.ai import controller as C
    recital = ("A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by "
               "Addenda Nos. 1 and 2, unless otherwise stated.")
    assert C.amendment_language(recital) == [], C.amendment_language(recital)
    assert C.amendment_language("The Bidder shall submit Form 4-G unless otherwise stated.")   # an operative clause


def test_N4_provided_for_convenience_only_is_not_a_proviso():
    from tenderpack.ai import controller as C
    note = "The English translation at Appendix B is provided for convenience only."
    assert C.amendment_language(note) == [], C.amendment_language(note)
    assert C.amendment_language("The bond is returned, provided that the Bidder signs the Agreement.")


# ---------------------------------------------------------------------------------------------- N11

def _iss(iid, prov, quotes, status="interpretation_pending", pid=None, text="test"):
    from types import SimpleNamespace as NS
    ev = [NS(unit_id=u, words=w) for u, w in quotes]
    return NS(id=iid, statement_type="issue", provision=prov, verification_status=status, evidence=ev,
              payload={"text": f"{text} {TEST}", **({"id": pid} if pid else {})})


def test_N11_analysis_issues_on_a_downstream_issue_s_subject_are_merged_into_it():
    from types import SimpleNamespace as NS
    q = ("ADD-03:3.5", "The Arabic text governs.")
    a1 = _iss("ADD-03/p3-image/r4/issue", "ADD-03:3.5", [q, ("ADD-03:p3-image/r4", "٧")])
    a2 = _iss("ADD-03/T42-1/5/issue", "ADD-03:T42-1/5", [("ADD-03:T42-1/5", "24"), q])
    a3 = _iss("ADD-03/4.1/issue-q4", "ADD-03:4.1", [("ADD-03:4.1", "materially more adverse")])
    d = _iss("DS-RENDER", "ADD-03:3.5", [("ADD-03:3.5", "The Arabic text governs. The English translation")],
             pid="I-ADD03-T42-1-RENDERINGS")
    m = DS.issue_subject_merges(NS(items=[a1, a2, a3]), [d])
    assert m == {DS.analysis_issue_id(a1): "I-ADD03-T42-1-RENDERINGS",
                 DS.analysis_issue_id(a2): "I-ADD03-T42-1-RENDERINGS"}, m
    # references to a merged id point at the one issue
    pl = {"row": {"id": "R1", "issues": [DS.analysis_issue_id(a1), "I-OTHER"]}}
    assert DS.remap_issue_ids(pl, m) == {"row": {"id": "R1", "issues": ["I-ADD03-T42-1-RENDERINGS", "I-OTHER"]}}


# ---------------------------------------------------------------------------------------------- N6 + defect 15

def _killed_run(tmp_path):
    import json
    import os
    from datetime import datetime, timezone
    run = tmp_path / "run"
    for sid, done in (("S-SEG1", True), ("S-KILLED-1", False), ("S-KILLED-2", False), ("S-DONE-2", True)):
        d = run / "ai" / sid
        d.mkdir(parents=True)
        (d / "prompt.txt").write_text(f"prompt {TEST}", encoding="utf-8")
        if done:
            (d / "session.json").write_text(json.dumps({"run_id": sid, "elapsed_s": 5}), encoding="utf-8")
        t = datetime(2026, 10, 7, *((16, 25) if sid == "S-SEG1" else (18, 0)), tzinfo=timezone.utc).timestamp()
        os.utime(d / "prompt.txt", (t, t))
    # the blind-07 shape (frozen timestamps): segment 1 ended, segment 2 resumed at 17:43:24 and was killed after its
    # last recorded event at 18:05:12 (no end); its drive was never recorded
    data = {"run_id": "R-TEST", "created": "2026-10-07T16:19:47Z", "updated": "2026-10-07T18:05:12Z",
            "status": "running", "settings": {}, "batches": {}, "interventions": [],
            "events": [{"ts": "2026-10-07T16:19:47Z", "event": "started"},
                       {"ts": "2026-10-07T16:30:00Z", "event": "segment_ended", "status": "deferred"},
                       {"ts": "2026-10-07T17:43:24Z", "event": "resumed"},
                       {"ts": "2026-10-07T18:05:12Z", "event": "submission_reused"}],
            "concurrency_drives": [{"drive": "2026-10-07T16:30:00Z", "segment": 1, "interrupted": False, "phases": {}}]}
    (run / "checkpoint.json").write_text(json.dumps(data), encoding="utf-8")
    return run, data


def test_N6_a_segment_ended_by_a_kill_gets_its_end_record_on_resume(tmp_path):
    from types import SimpleNamespace as NS
    from tenderpack.ai import workflow as WF
    run, data = _killed_run(tmp_path)
    cp = NS(data=data, path=run / "checkpoint.json",
            event=lambda name, **kw: data["events"].append({"ts": "2026-10-07T18:26:51Z", "event": name, **kw}))
    rec = WF.record_killed_segment(cp)
    assert rec is not None and rec["segment"] == 2, rec
    assert rec["note"] == ("ended by a stop at 2026-10-07T18:05:12Z; sessions without a result: S-KILLED-1, "
                           "S-KILLED-2 (killed)"), rec["note"]
    ev = [e for e in data["events"] if e["event"] == "segment_end_recorded"]
    assert len(ev) == 1 and ev[0]["note"] == rec["note"]
    dr = data["concurrency_drives"]
    assert [d["segment"] for d in dr] == [1, 2] and dr[1]["interrupted"] and "stop" in dr[1]["ended_by"]
    dw = data["destroyed_work"]
    assert dw and dw[0]["segment"] == 2 and [s["session"] for s in dw[0]["sessions"]] == ["S-KILLED-1", "S-KILLED-2"]
    assert any("killed" in str(x.get("note")) for x in data["interventions"])
    assert WF.record_killed_segment(cp) is None                    # recorded once
    # a segment that ended needs nothing
    data2 = {"events": [{"ts": "2026-10-07T16:19:47Z", "event": "started"},
                        {"ts": "2026-10-07T16:30:00Z", "event": "segment_ended"}]}
    assert WF.record_killed_segment(NS(data=data2, path=run / "checkpoint.json", event=None)) is None


def test_N6_bench_shows_the_destroyed_work(tmp_path, capsys):
    import importlib.util
    import json
    from types import SimpleNamespace as NS
    from tenderpack.ai import workflow as WF
    run, data = _killed_run(tmp_path)
    cp = NS(data=data, path=run / "checkpoint.json",
            event=lambda name, **kw: data["events"].append({"ts": "2026-10-07T18:26:51Z", "event": name, **kw}))
    WF.record_killed_segment(cp)
    (run / "checkpoint.json").write_text(json.dumps(data), encoding="utf-8")
    spec = importlib.util.spec_from_file_location("bench_workflow_f3", ROOT / "scripts/bench_workflow.py")
    bench = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bench)
    r = bench.from_run(str(run))
    assert r["segments"][1]["end"] == "2026-10-07T18:05:12Z", r["segments"]
    bench.print_run(r)
    out = capsys.readouterr().out
    line = next((x for x in out.splitlines() if x.strip().startswith("destroyed")), None)
    assert line and "segment 2" in line and "S-KILLED-1" in line and "2 session(s)" in line, out


def test_N4_R4_1_a_negation_counts_only_when_it_negates_the_trigger_word_itself():
    from tenderpack import human_owned as H
    from tenderpack.ai import controller as C
    # the final reviewer's case: "no doubt" negates nothing about "resolved": the reason settles the point
    t = "There is no doubt the ambiguity is resolved by Volume I Clause 3.2"
    assert H.triggers(t, ("closure",)) == ["declares a matter resolved ('resolved')"], H.triggers(t, ("closure",))
    assert H.analysis_reasons("disposition", {"disposition": "no_effect", "reason": t}), "human-owned (as on a918d5e)"
    for neg in ("The question is not resolved.", "It cannot be resolved without the Permit.",
                "The matter is no longer resolved by ADD-02.", "Whether it is resolved is a person's decision.",
                "Whether the matter is resolved is a person's decision.", "unit not resolved (see the issue)",
                "The question has not yet been settled.", "No answer has been withdrawn."):
        assert H.triggers(neg, ("closure",)) == [], neg
    assert C.amendment_language("The clauses that follow are not renumbered.") == []


# ---------------------------------------------------------------------------------------------- N8

def test_N8_no_conditional_impact_task_for_a_structural_region_unit(ws, prom, monkeypatch):
    from types import SimpleNamespace as NS
    # the blind-07 shape (frozen): the engine's pending-reading investigation of the region unit itself, ref "?"
    region = {"id": "impact:?", "provision": "ADD-03:region:ADD-03-p3-r1", "accepted": False,
              "conditional_on": {"kind": "reading", "ref": "?", "state": "pending_reading",
                                 "why": f"the reading ? of ADD-03 is pending a person's approval {TEST}"},
              "units": ["ADD-03:region:ADD-03-p3-r1"], "investigate": f"conditional on reading ? {TEST}"}
    good = {"id": "impact:ADD-03/7.3", "provision": "ADD-03:7.3", "accepted": False,
            "conditional_on": {"kind": "op", "ref": "ADD-03/7.3", "state": "invalid", "why": f"not valid {TEST}"},
            "units": ["ADD-03:7.3"], "investigate": f"conditional on op ADD-03/7.3 {TEST}"}
    monkeypatch.setattr(DS, "_engine_impacts", lambda r2, addendum: [region, good])
    out = DS.conditional_tasks(ws, NS(items=[]), prom, {}, prom["r2"], "ADD-03")
    assert not any("?" in t["id"] for t in out), [t["id"] for t in out]
    recs = [x for t in out for x in t.get("items") or []]
    assert not any(":region:" in str(x.get("provision")) or (x.get("conditional_on") or {}).get("ref") == "?"
                   for x in recs), recs
    assert any((x.get("conditional_on") or {}).get("ref") == "ADD-03/7.3" for x in recs), recs


# ---------------------------------------------------------------------------------------------- N12

CLASS_UNITS = [{"unit_id": f"ADD-03:TX/r{i}", "kind": "table_row", "text": f"row {i} {TEST}",
                "context": {"column_headings": ["No.", "Asset class", "Minimum residual life (years)"]},
                "cells": {"No.": str(i), "Asset class": c, "Minimum residual life (years)": v}}
               for i, (c, v) in enumerate((("Civil structures", "20"), ("Electrical equipment", "7")), 1)]


def test_N12_an_issue_raised_only_at_output_time_reaches_the_candidate_register_and_the_packet():
    from tenderpack import signals
    from tenderpack.ai import workflow as WF
    got = DS.output_time_issues(CLASS_UNITS, {"R-TX": ["ADD-03:TX/r1"]}, existing=set())
    assert list(got) == ["I-AUTO-CLASS-SCOPE-ADD-03-TX"], got
    e = got["I-AUTO-CLASS-SCOPE-ADD-03-TX"]
    assert e["text"].startswith("HUMAN DECISION PENDING") and e["rows"] == ["R-TX"] and "output time" in e["source"]
    # written once: the output-time rule does not raise it again beside the register's entry
    assert DS.output_time_issues(CLASS_UNITS, {}, existing=set(got)) == {}
    assert signals.class_scope_issues(CLASS_UNITS, {}, existing=set(got)) == []
    lines = WF.promotion_lines({"output_time_issues": list(got), "issues": list(got)}, {})
    assert any("output time issues" in x and "I-AUTO-CLASS-SCOPE-ADD-03-TX" in x for x in lines), lines


# ---------------------------------------------------------------------------------------------- N9

def _gate_policy(on_deferred, pause_s):
    from tenderpack.ai import requests as R
    t = [1000.0]
    gate = R.RateGate(clock=lambda: t[0])
    gate.pause(pause_s)                     # another worker's host 429: "resets 5:40pm" (about 75 min away)
    p = R.FailurePolicy()
    p.on_deferred, p.gate = on_deferred, gate
    slept = []

    def sleep(s):
        slept.append(s)
        t[0] += s
    return p, slept


def test_N9_with_on_deferred_stop_a_batch_asked_ahead_never_waits_out_a_reset_beyond_the_limit():
    from tenderpack.ai import requests as R
    p, slept = _gate_policy("stop", 4500.0)
    started = []
    with pytest.raises(R.RateLimited) as e:
        R.call_host(lambda: started.append(1), p, sleep=slept.append)
    assert not started and not slept, (started, slept)     # no session started, no 75-minute wait
    assert "deferred" in e.value.message and "not started" in e.value.message, e.value.message
    with pytest.raises(R.RateLimited):
        R.call_provider(object(), None, p, sleep=slept.append)
    assert not slept


def test_N9_a_short_pause_or_on_deferred_continue_still_waits():
    from tenderpack.ai import requests as R
    p, slept = _gate_policy("stop", 120.0)                  # within honour_reset_up_to_s: waited out as before
    R._gate_wait(p, slept.append)
    assert slept == [120.0]
    p2, slept2 = _gate_policy("continue", 4500.0)
    R._gate_wait(p2, slept2.append)
    assert slept2 == [4500.0]
