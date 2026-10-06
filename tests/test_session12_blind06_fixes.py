"""Session 12, fixer F6: the blind-06 scorer's larger workflow defects (rehearsals/blind-06/COMPARISON.md, "Follow-ups:
defects in the workflow", items 5, 6 (b), 9 and 12; the coordinator's fixes of the others are in
tests/test_session12_blind06_coord.py). Each test was written and run failing before its fix. The fixtures are small
and synthetic, modelled on blind-06's cases (synthetic content, not tender content): passing them makes no
interpretation correct and approves nothing."""
from __future__ import annotations

from tenderpack.amend import Engine, OpFile, unit_pin
from tenderpack.register import Register, RowFile, compute_pins, migrate_pins, pin_value


# ------------------------------------------------------------------------------------------ follow-up 9 (pins)

def _u(uid, doc, text, page=1, kind="clause", parent=None):
    return {"unit_id": uid, "doc": doc, "kind": kind, "text": text, "pages": [page], "parent": parent}


def _confirm_run(pin_rows: bool = True):
    """VOL-II 7.2 amended by ADD-03 3.1; 7.3 confirmed unchanged by ADD-03 3.2(b) (blind-06 false signal 4)."""
    units = [_u("VOL-II:7.2", "VOL-II", "The reliability run shall be at not less than 90 % of nominal capacity.", 7),
             _u("VOL-II:7.3", "VOL-II", "The reliability run shall last thirty (30) consecutive days.", 7),
             _u("ADD-03:cover/para1", "ADD-03", "Issued 10 November 2026", 1, "paragraph"),
             _u("ADD-03:3.1", "ADD-03", "In Volume II Clause 7.2, '90 %' is deleted and '85 %' is substituted.", 2),
             _u("ADD-03:3.2", "ADD-03", "(b) Volume II Clause 7.3 is unchanged.", 2)]
    of = OpFile.model_validate({
        "addendum": "ADD-03", "issued_from": "ADD-03:cover/para1", "prepared_by": "test", "method": "test",
        "ops": [{"id": "ADD-03/3.1", "provision": "ADD-03:3.1", "type": "replace_text", "target": "VOL-II:7.2",
                 "old": "90 %", "new": "85 %"},
                {"id": "ADD-03/3.2(b)", "provision": "ADD-03:3.2", "type": "annotate", "targets": ["VOL-II:7.3"],
                 "effect": "confirms", "note": "Volume II Clause 7.3 is unchanged."}],
        "dispositions": [{"provision": "ADD-03:cover/para1", "disposition": "no_effect", "reason": "issue date"}]})
    base = {"discipline": "Technical", "assessment": "pass_fail", "confidence": "high", "confidence_reason": "t",
            "scope": ["t"], "group": "VOL-II:7"}
    rf = RowFile.model_validate({"prepared_by": "t", "method": "t", "anchors": {}, "rows": [
        {**base, "id": "RUN-72", "requirement": "the run's flow and length", "units": ["VOL-II:7.2", "VOL-II:7.3"],
         "interpretations": [{"stage": "BASE", "quote": "not less than 90 % of nominal capacity"}]},
        {**base, "id": "RUN-73", "requirement": "the run's length", "units": ["VOL-II:7.3"],
         "interpretations": [{"stage": "BASE", "quote": "thirty (30) consecutive days"}]},
        {**base, "id": "RUN-73-REREAD", "requirement": "the run's length", "units": ["VOL-II:7.3"],
         "interpretations": [{"stage": "BASE", "quote": "thirty (30) consecutive days"},
                             {"stage": "ADD-03", "quote": "thirty (30) consecutive days"}]}]})
    stages = Engine(units, [of]).run()
    assert stages[1].status == "APPLIED", [x.checks for x in stages[1].ops]
    if pin_rows:
        compute_pins(rf, stages)
    return rf, stages


def test_a_confirming_annotation_is_never_reported_as_a_change_since_base():
    """Follow-up 9: 'VOL-II:7.3 changed since BASE (by ADD-03/3.2(b))' although 3.2(b) says 7.3 is unchanged: the pin
    hashed every annotating op id, so a confirmation changed it and the reason listed it among the changing ops."""
    rf, stages = _confirm_run()
    reg = Register(rf, stages)
    ev = {r.id: reg.evaluate(r, stages[1]) for r in rf.rows}
    why = "; ".join(ev["RUN-72"]["stale"])
    assert "VOL-II:7.2 changed since BASE (by ADD-03/3.1)" in why, why          # the real change is still reported
    assert "VOL-II:7.3 changed since" not in why and "(by ADD-03/3.2(b))" not in why, why
    for rid in ("RUN-73", "RUN-73-REREAD"):
        assert not any("changed since" in x for x in ev[rid]["stale"]), (rid, ev[rid]["stale"])
    # the confirming provision is still a new dependency of a row read before it, named as a confirmation
    assert any(x.startswith("new dependency ADD-03:3.2") and "confirms" in x for x in ev["RUN-73"]["stale"]), ev["RUN-73"]
    assert ev["RUN-73-REREAD"]["stale"] == []


def test_the_pin_ignores_confirming_annotations_and_the_decision_binding_does_not():
    rf, stages = _confirm_run(pin_rows=False)
    base, add = stages[0].state, stages[1].state
    assert add["VOL-II:7.3"].annotations == ["ADD-03/3.2(b)"]
    assert pin_value(add, "VOL-II:7.3", {"ADD-03/3.2(b)"}) == pin_value(base, "VOL-II:7.3")
    assert pin_value(add, "VOL-II:7.3") != pin_value(base, "VOL-II:7.3")          # without the set: format 2's value
    ev = {"VOL-II:7.3": {"doc": "VOL-II", "pages": [7]}}
    assert unit_pin(add, "VOL-II:7.3", ev) != unit_pin(base, "VOL-II:7.3", ev)   # decision binding: unchanged rule
    reg = Register(rf, stages)
    assert reg.confirming == {"ADD-03/3.2(b)"}
    row = next(r for r in rf.rows if r.id == "RUN-73")
    assert reg.pins_for(row, row.interpretations[0], stages[1])["VOL-II:7.3"] == pin_value(base, "VOL-II:7.3")


def test_format_2_pins_are_migrated_only_where_nothing_changed():
    """A pins.yaml written under format 2 (confirming annotations hashed) is re-pinned under format 3 only for the
    interpretations whose every dependency still has its format-2 value; anything else is left STALE for a person."""
    rf, stages = _confirm_run(pin_rows=False)
    reg = Register(rf, stages)
    by = {s.stage: s for s in stages}
    for row in rf.rows:
        for it in row.interpretations:
            it.pins = {d: unit_pin(by[it.stage].state, d) for d in reg.pins_for(row, it, by[it.stage])}   # format 2
    reread = next(r for r in rf.rows if r.id == "RUN-73-REREAD").interpretations[1]
    old = dict(reread.pins)
    n, kept = migrate_pins(rf, stages)
    assert reread.pins != old and reread.pins == reg.pins_for(next(r for r in rf.rows if r.id == "RUN-73-REREAD"),
                                                              reread, by["ADD-03"])
    assert "RUN-73-REREAD@ADD-03" not in kept and n >= 1
    stale = Register(rf, stages).evaluate(next(r for r in rf.rows if r.id == "RUN-73-REREAD"), stages[1])["stale"]
    assert stale == []
    # a pin that no longer matches its format-2 value (the unit changed after pinning) is left as it is
    rf2, stages2 = _confirm_run(pin_rows=False)
    r72 = next(r for r in rf2.rows if r.id == "RUN-72")
    r72.interpretations[0].pins = {"VOL-II:7.2": "0" * 16, "VOL-II:7.3": unit_pin(stages2[0].state, "VOL-II:7.3")}
    _, kept2 = migrate_pins(rf2, stages2)
    assert "RUN-72@BASE" in kept2 and r72.interpretations[0].pins["VOL-II:7.2"] == "0" * 16


# ------------------------------------------------------------------------------------------ follow-up 5 (computed dates)

def _dates_run(rows: list[dict] | None = None):
    """Blind-06's shape: the PDD Thu 26 Nov; the addendum issued Tue 10 Nov; 2.5 'not later than eight (8) Working Days
    before the Proposal Due Date' and 'within five (5) Working Days of receipt of a complete application'; the cover's
    'within eight (8) Working Days of the date of this Addendum' (Fri/Sat weekend)."""
    from tenderpack.dates import Calendar
    units = [_u("VOL-I:2.4", "VOL-I", "Where a period expressed in Working Days is to be counted backwards from a stated "
                                      "date, the stated date itself shall not be counted.", 2),
             _u("VOL-I:6.1", "VOL-I", "The Proposal Due Date is 14:00 Riyadh time on Thursday 26 November 2026.", 3),
             _u("ADD-03:cover/para1", "ADD-03", "Issued 10 November 2026", 1, "paragraph"),
             _u("ADD-03:cover/para3", "ADD-03", "This Addendum requires a Bidder that elects to interrupt flows to obtain "
                                               "the Authority's acceptance of its shutdown programme, applications for "
                                               "which shall be made within eight (8) Working Days of the date of this "
                                               "Addendum.", 1, "paragraph"),
             _u("ADD-03:2.5", "ADD-03", "Where the Bidder elects method (b), it shall submit a Shutdown Acceptance "
                                        "Letter in Envelope A. Applications for a Shutdown Acceptance Letter shall be "
                                        "made to the Network Operator not later than eight (8) Working Days before the "
                                        "Proposal Due Date. The Network Operator has undertaken to respond within five "
                                        "(5) Working Days of receipt of a complete application.", 2)]
    of = OpFile.model_validate({"addendum": "ADD-03", "issued_from": "ADD-03:cover/para1", "prepared_by": "test",
                                "method": "test", "ops": [], "dispositions": [
                                    {"provision": "ADD-03:cover/para1", "disposition": "no_effect", "reason": "issue date"}]})
    base = {"discipline": "Technical", "assessment": "procedural", "confidence": "medium", "confidence_reason": "t",
            "scope": ["t"]}
    rf = RowFile.model_validate({"prepared_by": "t", "method": "t", "anchors": {"PDD": {"name": "Proposal Due Date",
                                                                                         "defined_in": "VOL-I:6.1"}},
                                 "rows": [{**base, **r} for r in (rows or [])]})
    stages = Engine(units, [of]).run()
    reg = Register(rf, stages, Calendar(weekend={4, 5}))
    return {"register": reg, "stages": stages, "evals": reg.all(), "units": units, "rowfile": rf}


def test_a_computed_deadline_carries_a_date_rule_the_register_accepts():
    """Follow-up 5: the computed_date task asked for 'a row's date rule with these words' without its shape, and the
    proposed rule used kind 'deadline' (a purpose), which dates.KINDS refuses: 'kind 'deadline' not in ('anchor',
    'relative', ...)'. The deadline now carries the relative rule (anchor, count, unit, direction, words) to copy."""
    from tenderpack import derived
    from tenderpack.dates import DateRule
    r = _dates_run()
    cd = {(d["unit"], d["words"]): d for d in derived.computed_deadlines(r, "ADD-03")}
    d = cd[("ADD-03:2.5", "eight (8) Working Days before the Proposal Due Date")]
    assert d["result"]["value"] == "2026-11-16"
    rule = d["date_rule"]
    assert {k: rule[k] for k in ("kind", "purpose", "anchor", "offset", "unit", "direction", "source_unit", "text")} == {
        "kind": "relative", "purpose": "deadline", "anchor": "PDD", "offset": 8, "unit": "working_day",
        "direction": "before", "source_unit": "ADD-03:2.5", "text": "eight (8) Working Days before the Proposal Due Date"}
    DateRule(rule_id="t", **{k: v for k, v in rule.items() if k != "rule_id"})        # the register accepts it


def test_forward_periods_and_the_covers_own_anchor_are_computed_or_say_why_not():
    """Follow-up 5: 'within five (5) Working Days of receipt' and the cover's 'within eight (8) Working Days of the date
    of this Addendum' got no calculation and no note (D3, D4 on blind-06)."""
    from tenderpack import derived
    from tenderpack.dates import DateRule
    r = _dates_run()
    cd = {(d["unit"], d["words"]): d for d in derived.computed_deadlines(r, "ADD-03")}
    cover = cd[("ADD-03:cover/para3", "within eight (8) Working Days of the date of this Addendum")]
    assert cover["anchor"] == "ADD-03-issue" and cover["anchor_date"] == "2026-11-10"
    assert cover["result"]["status"] == "ambiguous" and cover["result"]["escalate"]      # no forward rule in the registry
    assert {x["value"] for x in cover["result"]["readings"]} == {"2026-11-22", "2026-11-19"}
    assert cover["note"].startswith("not computed: no rule") and "counted after" in cover["note"]
    assert cover["date_rule"]["kind"] == "relative" and cover["date_rule"]["anchor"] == "ADD-03-issue"
    resp = cd[("ADD-03:2.5", "within five (5) Working Days of receipt of a complete application")]
    assert resp["result"]["status"] == "unresolved" and resp["anchor_date"] is None
    assert resp["note"].startswith("not computed: no rule") and "receipt of a complete application" in resp["note"]
    assert resp["date_rule"]["kind"] == "unresolved" and resp["date_rule"]["note"] == resp["note"]
    DateRule(rule_id="t", **{k: v for k, v in resp["date_rule"].items() if k != "rule_id"})
    lines = "\n".join(derived.review_lines(derived.summary(r, "ADD-03")))
    assert "not computed: no rule" in lines and "receipt of a complete application" in lines


def test_the_task_hands_the_rule_over_and_an_activity_with_the_inputs_only_is_recomputed():
    """Follow-up 5: blind-06's activity gave `computed_from` with its method and inputs but no fingerprint, and the
    validator matched on the fingerprint only: 'computed_from matches no deadline the program computed'. The claim is
    recomputed from its inputs by the same function (calc.deadline) the program used."""
    from tenderpack import derived
    from tenderpack.ai import derived_tasks
    r = _dates_run()
    ts = {t["id"]: t for t in derived_tasks.tasks(None, r, "ADD-03", [])}
    t = ts["date:ADD-03:2.5"]
    assert t["date_rule"]["kind"] == "relative" and "date_rule" in t["expect"] and "'relative'" in t["expect"]
    claim = {"method": "deadline", "inputs": {"offset": {"count": 8, "unit": "working_day",
                                                         "words": "eight (8) Working Days before the Proposal Due Date"},
                                              "anchor": {"name": "PDD", "date": "2026-11-26", "source": "VOL-I:6.1"},
                                              "direction": "before"}}            # D-19's claim on blind-06, verbatim
    deadlines = derived.computed_deadlines(r, "ADD-03")
    known = derived.match_computed_from(claim, deadlines, r["register"].cal_by_stage["ADD-03"])
    assert known is not None and known["computed_from"]["result"] == "2026-11-16"
    wrong = {"method": "deadline", "inputs": dict(claim["inputs"], offset={"count": 9, "unit": "working_day",
                                                                           "words": "nine (9) Working Days"})}
    assert derived.match_computed_from(wrong, deadlines, r["register"].cal_by_stage["ADD-03"]) is None


def test_a_row_made_from_the_tasks_rule_plans_the_date_with_the_same_fingerprint():
    """End to end on the synthetic stage: a row whose date rule is the task's rule evaluates (no ValueError), plans
    Mon 16 Nov, and the milestone fingerprint (derived.rule_computed_from, what the programme attaches) is the one the
    computed deadline records, even when the row quotes more words than the phrase."""
    from tenderpack import derived
    r0 = _dates_run()
    d = next(x for x in derived.computed_deadlines(r0, "ADD-03") if x["unit"] == "ADD-03:2.5" and x["anchor"] == "PDD")
    rule = dict(d["date_rule"], rule_id="ADD-03-2.5-01-R1",
                text="not later than eight (8) Working Days before the Proposal Due Date")
    row = {"id": "ADD-03-2.5-01", "group": "ADD-03:2.5", "requirement": "apply for the letter (test data)",
           "units": ["ADD-03:2.5"], "evidence": [], "no_deliverable": "test data",
           "interpretations": [{"stage": "ADD-03", "quote": "not later than eight (8) Working Days before the Proposal "
                                                            "Due Date"}], "date_rules": [rule]}
    r = _dates_run([row])
    ev = next(e for e in r["evals"] if e["row"].id == "ADD-03-2.5-01")["stages"]["ADD-03"]
    date = next(x for x in ev["dates"] if x["rule_id"] == "ADD-03-2.5-01-R1")
    assert date["planning"]["value"] == "2026-11-16", date
    cf = derived.rule_computed_from(r["rowfile"].rows[0].date_rules[0], date["anchor_value"], "VOL-I:6.1",
                                    r["register"].cal_by_stage["ADD-03"], r["rowfile"].anchors)
    assert cf["fingerprint"] == d["computed_from"]["fingerprint"] and cf["result"] == "2026-11-16"
    assert "= computed: calc deadline 2026-11-16" in derived.date_derivation(derived.computed_deadlines(r, "ADD-03"), date)


def test_the_programme_gives_the_milestone_the_computed_fingerprint(tmp_path_factory):
    """End to end on blind-05's candidate (synthetic; tests/fixtures/s12_blind05.py): the computed deadline of
    ADD-03 7.3 -> the task's `date_rule` -> a row (test data) -> A1 and an A5 milestone on 2026-11-23 whose
    `computed_from` fingerprint is the one the deadline recorded."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent / "fixtures"))
    import s12_blind05 as F
    import s12_w3b as W
    from tenderpack import derived, programme, stage2
    tmp = tmp_path_factory.mktemp("s12f6-dates")
    r0 = F.run(tmp_path_factory)["r"]
    d = next(x for x in derived.computed_deadlines(r0, "ADD-03") if x["unit"] == "ADD-03:7.3")
    rule = dict(d["date_rule"], rule_id="ADD-03-7.3-F6-R1")
    row = {"id": "ADD-03-7.3-F6", "group": "ADD-03:7.3", "scope": ["submission"], "units": ["ADD-03:7.3"],
           "requirement": "Portal notice not later than three Working Days before the PDD (test data)",
           "discipline": "Technical", "assessment": "procedural", "evidence": [], "no_deliverable": "test data",
           "interpretations": [{"stage": "ADD-03", "quote": d["words"]}], "date_rules": [rule],
           "confidence": "medium", "confidence_reason": "test data"}
    rr = stage2.run(F.build(tmp_path_factory), W.copy_candidate(tmp, rows=[row]), F.ROOT)
    prog = programme.stage_planner(rr, "ADD-03")(rr["assumptions"])
    m = next(x for x in prog["milestones"] if x["id"] == "ADD-03-7.3-F6-R1")
    assert m["date"] == "2026-11-23" and m["computed_from"]["fingerprint"] == d["computed_from"]["fingerprint"], m


# ------------------------------------------------------------------------------------------ follow-ups 12 and 6 (b)

TEXTS = {"VOL-I:3.2": "In the event of any conflict, ambiguity or discrepancy between or within the RFP Documents, the "
                      "following order of precedence shall apply, the first named prevailing:",
         "ADD-03:cover/para3": "This Addendum requires a Bidder to obtain the Authority's acceptance of its shutdown "
                               "programme, applications for which shall be made within eight (8) Working Days of the "
                               "date of this Addendum.",
         "ADD-03:2.2": "Table 1-3 is issued in Arabic, with an English convenience translation in Appendix B. The Arabic "
                       "text governs.",
         "ADD-03:2.5": "Applications for a Shutdown Acceptance Letter shall be made to the Network Operator not later "
                       "than eight (8) Working Days before the Proposal Due Date.",
         "ADD-03:Q17": "Bidder question: Who bears the IE costs of a second run? | Authority response: The Project Company "
                       "bears them. Volume V Clause 12.3 is amended accordingly.",
         "ADD-03:Q18": "Bidder question: Is a utility shortfall a Relief Event? | Authority response: Clause 34.1 applies."}
PROVS = ["ADD-03:cover/para3", "ADD-03:2.2", "ADD-03:2.5", "ADD-03:Q17", "ADD-03:Q18"]


def test_points_the_documents_settle_are_applied_with_the_clause_quoted():
    """Follow-up 12: the cover against the operative text, the addendum's own precedence clause (2.2 'The Arabic text
    governs.') and 'is amended accordingly' (Q17) were handed to Legal as decisions on blind-06."""
    from tenderpack.ai.controller import settled_points
    cover = settled_points("The cover summary says the Authority; 2.5 says the Network Operator. Which text governs is "
                           "a decision for Legal; nothing is resolved here.", "ADD-03:cover/para3", TEXTS, "ADD-03", PROVS)
    assert len(cover) == 1 and cover[0]["kind"] == "cover"
    assert cover[0]["line"].startswith("VOL-I 3.2 provides: 'In the event of any conflict") and \
        cover[0]["line"].endswith("(applied, not decided)") and "never an operative provision" in cover[0]["line"]
    arabic = settled_points("The Arabic table prints 4 for TP-2 and the English translation 6. Which rendering governs, "
                            "and which figure applies, is a person's decision.", "ADD-03:T1-3/tp-2", TEXTS, "ADD-03", PROVS)
    assert [p["line"] for p in arabic] == ["ADD-03 2.2 provides: 'The Arabic text governs.' (applied, not decided)"]
    q17 = settled_points("Whether the response amends the contract is a person's decision.", "ADD-03:Q17", TEXTS,
                         "ADD-03", PROVS)
    assert [p["line"] for p in q17] == ["ADD-03 Q17 provides: 'Volume V Clause 12.3 is amended accordingly.' (applied, "
                                        "not decided)"]
    # genuine judgments stay a person's: no clause of the documents settles them
    assert settled_points("Whether that shortfall is a Relief Event is a legal question.", "ADD-03:Q18", TEXTS,
                          "ADD-03", PROVS) == []
    assert settled_points("Answer 19 cites the deleted 8.2 and 7.4 keeps sixty days. Which text prevails is a person's "
                          "decision.", "ADD-03:Q19", TEXTS, "ADD-03", PROVS) == []


def test_an_issue_on_a_settled_point_is_an_applied_rule_not_a_decision_for_legal():
    from tenderpack.ai.controller import applied_rule_review, re_present_issue
    issue = {"id": "I-T13", "owner": "Legal counsel", "short": "Table 1-3: Arabic (governing) vs English values differ",
             "text": "The pending reading of the Arabic gives a different TP-2 maximum from the English 6 hours. Which "
                     "rendering governs is a decision for Legal."}
    r = applied_rule_review("issue", issue, "ADD-03:2.2", TEXTS, "ADD-03", PROVS)
    assert r["lines"] == ["ADD-03 2.2 provides: 'The Arabic text governs.' (applied, not decided)"]
    assert r["human"] == []                                   # nothing outside the settled sentence is a judgment
    e = re_present_issue(dict(issue), r["lines"], r["sentences"])
    assert e["owner"] == "Bid manager" and e["proposed_owner"] == "Legal counsel"
    assert "decision for Legal" not in e["text"] and "ADD-03 2.2 provides: 'The Arabic text governs.'" in e["text"]
    assert e["proposed_text"] == issue["text"] and e["applied_rule"] == r["lines"]
    # a judgment outside the quotation keeps the label (the human-owned classifier's own words fire)
    judged = dict(issue, text=issue["text"] + " The missing letter is deemed an election of method (a).")
    assert applied_rule_review("issue", judged, "ADD-03:2.2", TEXTS, "ADD-03", PROVS)["human"]
    # an issue on a genuine judgment is unchanged (human-owned by type)
    plain = {"id": "I-Q18", "owner": "Legal counsel", "text": "Whether that shortfall is a Relief Event is a legal question."}
    g = applied_rule_review("issue", plain, "ADD-03:Q18", TEXTS, "ADD-03", PROVS)
    assert g["lines"] == [] and g["human"]


def test_a_downstream_item_that_hands_back_a_point_the_analysis_concluded_is_a_reversal():
    """Follow-up 6 (b): analyses 002, 008 and 010 applied 2.2 (the Arabic governs: TP-2 is 4 h); downstream D-05/D-07
    handed 'which rendering governs' to a person. Flagged as a reversal naming the analysis item, not promoted silently."""
    from tenderpack.ai.controller import phase_reversals
    analysis = {"ADD-03/2.7": ("ADD-03:2.7", "The governing maximum shutdown duration for TP-2, which ADD-03:2.7 uses as "
                                             "the threshold, is 4 hours (Arabic), not the 6 hours in the English "
                                             "convenience translation."),
                "ADD-03/2.3": ("ADD-03:2.3", "The Bidder elects a method per tie-in point.")}
    ds = [(0, "ADD-03:T1-3/tp-2", "The English translation prints 6 and the Arabic 4. Which rendering governs is a "
                                  "legal question for a person."),
          (1, "ADD-03:Q18", "Whether that shortfall is a Relief Event is a legal question."),
          (2, "ADD-03:T1-3/tp-2", "The TP-2 window is 01:00 to 05:00.")]
    got = phase_reversals(ds, analysis, TEXTS, "ADD-03", PROVS)
    assert set(got) == {0} and "ADD-03/2.7" in got[0] and "ADD-03 2.2" in got[0] and "reverses" in got[0]
    # no analysis item concluded it: an applied rule (follow-up 12), no reversal
    assert phase_reversals(ds[:1], {"ADD-03/2.3": analysis["ADD-03/2.3"]}, TEXTS, "ADD-03", PROVS) == {}


def test_downstream_validation_applies_the_rule_and_flags_the_reversal(tmp_path_factory):
    """Follow-ups 12 and 6 (b) through tenderpack.ai.downstream.validate on blind-05's candidate (synthetic): an
    escalation that hands 'which text governs' between the cover and an operative provision to Legal gets the applied
    rule with VOL-I 3.2 quoted; because an analysis item (test data) concluded the point, it is also a reversal:
    `conflicting`, naming that analysis item."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent / "fixtures"))
    import s12_w3b as W
    from tenderpack.ai import controller
    from tenderpack.ai import downstream as DS
    from tenderpack.ai.contract import EvidenceRef
    ws = W.workspace(tmp_path_factory)
    prom = W.promoted(ws)
    cover = next(p for p in controller._provisions(ws, "ADD-03") if ":cover/" in p)
    words = " ".join(ws.units_by_id[cover]["text"].split()[:8])
    ev = EvidenceRef(doc="ADD-03", unit_id=cover, page=ws.units_by_id[cover]["pages"][0], kind="span", words=words)
    esc = {"why": "The cover summary differs from the operative provision. Which text governs is a decision for Legal.",
           "what_is_unsupported": "the cover against the operative provision"}
    items = [{"id": "E1", "statement_type": "escalation", "task": f"esc:{cover}", "provision": cover, "payload": esc,
              "evidence": [ev]},
             {"id": "E2", "statement_type": "escalation", "task": f"esc:{cover}", "provision": cover,
              "payload": {"why": "Whether the Bidder relies on the option is a bid strategy decision for a person.",
                          "what_is_unsupported": "a judgment"}, "evidence": [ev]}]
    concluded = dict(prom, analysis={"ADD-03/7.3": ("ADD-03:7.3", "The cover summary orders nothing: the operative "
                                                                  "provision governs over the cover (test data).")})
    ds = W.dset(ws, items)
    DS.validate(ws, ds, concluded, {f"esc:{cover}": "escalation"})
    e1, e2 = ds.items
    ap = next((v for v in e1.validation if v.check == "applied rule"), None)
    assert ap is not None and ap.detail.startswith("VOL-I 3.2 provides: '") and "(applied, not decided)" in ap.detail
    rev = next((v for v in e1.validation if v.check == "consistency (phases)"), None)
    assert rev is not None and not rev.ok and "ADD-03/7.3" in rev.detail and e1.verification_status == "conflicting"
    assert not any(v.check in ("applied rule", "consistency (phases)") for v in e2.validation)   # a genuine judgment
    ds2 = W.dset(ws, items[:1])
    DS.validate(ws, ds2, prom, {f"esc:{cover}": "escalation"})                  # no analysis conclusion: no reversal
    assert ds2.items[0].verification_status == "escalated" and \
        any(v.check == "applied rule" for v in ds2.items[0].validation)


def test_a_pack_pinned_under_format_2_is_read_right_without_re_pinning():
    """Found by the regression suite (tests/test_session11_partial.py: register-reps BLOCKED for MOVED on blind-02's
    pack, whose pins.yaml is format 2): a format-2 pin of a dependency that only a confirmation touched must not turn
    STALE when the pin formula changes; a dependency that really changed still does."""
    rf, stages = _confirm_run(pin_rows=False)
    by = {s.stage: s for s in stages}
    reg = Register(rf, stages)
    for row in rf.rows:
        for it in row.interpretations:
            it.pins = {d: unit_pin(by[it.stage].state, d) for d in reg.pins_for(row, it, by[it.stage])}   # format 2
    ev = {r.id: Register(rf, stages).evaluate(r, stages[1]) for r in rf.rows}
    assert ev["RUN-73-REREAD"]["stale"] == []
    assert any("VOL-II:7.2 changed since BASE (by ADD-03/3.1)" in x for x in ev["RUN-72"]["stale"])


# ------------------------------------------------------------------------------------------ follow-up 14 (part)

def test_the_next_batch_is_asked_before_a_batchs_critic_runs(tmp_path, pack, monkeypatch):
    """Follow-up 14 (the critic inside the collection loop): with sessions at once, each analysis batch's critic ran
    before the next batch was asked, so a slot sat idle for every critic request (about 177 s on blind-06). The next
    batch is now dispatched as soon as a batch is taken, before its critic. Results are still taken in plan order."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    import test_session12_concurrency as TC
    from tenderpack.ai import workflow as WF
    seen = []
    real = WF._critic_analysis

    def spy(ctx, bid):
        before = sorted(ctx.prefetch.recs) if ctx.prefetch else []
        WF._fill(ctx, "analysis", bid)                  # what could still be asked now: nothing, when the slots are full
        seen.append((bid, before, sorted(ctx.prefetch.recs) if ctx.prefetch else []))
        return real(ctx, bid)
    monkeypatch.setattr(WF, "_critic_analysis", spy)
    res = TC._run(tmp_path / "n2", pack["out"], 2, "crit2", TC._cassette(tmp_path))
    assert res["status"] in ("ok", "partial", "stopped"), res
    assert seen and any(b for _, b, _ in seen), seen                  # batches were in flight during critics
    assert all(b == a for _, b, a in seen), seen                      # none was left to ask while a critic ran
