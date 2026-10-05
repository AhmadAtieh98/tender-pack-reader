"""Session 11, owner's section 3: conditional and effective-dated amendments, an amendment of an earlier amendment,
confirming versus changing answers, and the cover's direction words checked against the numbers.

Blind rehearsal 04 (rehearsals/blind-04/COMPARISON.md; its answer key is public since 16:42 UTC on 4 Oct 2026, so its
numbers are used as expected values here):
  5.2  "With effect from 8 October 2026, Section 5.1 of Addendum No. 1 is amended by deleting ... and substituting ..."
       The proposer escalated it: "A replace_text on ADD-01:5.1 simulates as structurally valid, but the engine reports
       the same words also in VOL-II:5.3 (where ADD-01:5.1 placed them) and that op changes only ADD-01:5.1, leaving
       the operative clause VOL-II:5.3 unchanged." Reproduced first, then fixed: the change flows to the volume unit
       the earlier amendment had amended (VOL-II 5.3 <- ADD-01 5.1 <- ADD-03 5.2), with its effective date, and the
       state at ADD-01 still shows ADD-01's words.
  7    a conditional amendment that is not in effect: the trigger, its deadline (Thu 12 Nov 2026), the applicability,
       both states; the register shows VOL-II 1.4 CONDITIONAL, never amended; nothing assumes the trigger occurred.
  E1   the cover says "relaxes the velocity limit" for a lowered maximum (2.0 -> 1.5 m/s): contradicted by the numbers.
  Q15  a decoy that restates VOL-I 8.7 and Form 4-D: it confirms, it adds no requirement.

Synthetic ADD-03 units with the addendum's own words over the real pack's committed build (read only). Nothing is
accepted, approved or sent.
"""
from __future__ import annotations

import json

import pytest

from tenderpack.amend import Disposition, Engine, Op, OpFile, load_opfile
from tenderpack.util import ROOT

FIVE_TWO = ("With effect from 8 October 2026, Section 5.1 of Addendum No. 1 is amended by deleting ‘for the buried "
            "sections of the transmission main’ and substituting ‘for the buried sections of the transmission main other "
            "than the trenchless crossings required by Volume II Clause 5.4, at which ductile iron only shall be used’.")
OLD_52 = "for the buried sections of the transmission main"
NEW_52 = ("for the buried sections of the transmission main other than the trenchless crossings required by Volume II "
          "Clause 5.4, at which ductile iron only shall be used")


def add03_unit(uid: str, text: str, page: int = 1, kind: str = "clause", **kw) -> dict:
    return {"unit_id": uid, "doc": "ADD-03", "kind": kind, "pages": [page], "text": text, **kw}


@pytest.fixture(scope="module")
def base_units() -> list[dict]:
    return json.load(open(ROOT / "build/units.json", encoding="utf-8"))["units"]


@pytest.fixture(scope="module")
def earlier() -> list[OpFile]:
    return [load_opfile(ROOT / "curation/amendments" / f"{a}.yaml") for a in ("ADD-01", "ADD-02")]


COVER = Disposition(provision="ADD-03:cover/para1", disposition="no_effect", reason="the issue date line")


def run(units, earlier, ops, dispositions=(COVER,), **kw):
    f = OpFile(addendum="ADD-03", issued_from="ADD-03:cover/para1", prepared_by="test", method="test", ops=ops,
               dispositions=list(dispositions))
    return Engine(units, earlier + [f], **kw).run()


# ---------------------------------------------------------------------------------------------- an amendment of an amendment

@pytest.fixture(scope="module")
def units52(base_units):
    return base_units + [add03_unit("ADD-03:cover/para1", "Issued 9 November 2026", kind="paragraph"),
                         add03_unit("ADD-03:5.2", FIVE_TWO, label="5.2")]


def test_an_amendment_of_an_earlier_amendment_flows_to_the_volume_unit_it_amended(units52, earlier):
    op = Op(id="ADD-03/5.2", provision="ADD-03:5.2", type="replace_text", target="ADD-01:5.1", old=OLD_52, new=NEW_52)
    stages = run(units52, earlier, [op])
    by = {s.stage: s for s in stages}
    x = next(r for r in by["ADD-03"].ops if r.op.id == "ADD-03/5.2")
    assert x.applied, [c for c in x.checks if not c["ok"]]
    v = by["ADD-03"].state["VOL-II:5.3"]
    # session 10: the op changed ADD-01:5.1 only and left the operative clause as ADD-01 had made it
    assert NEW_52 + ", subject to the whole-life cost comparison required by this Clause." in v.text, v.text
    assert v.history == ["ADD-01/5.1", "ADD-03/5.2"]
    assert by["ADD-03"].state["ADD-01:5.1"].text.count(NEW_52) == 1
    assert "VOL-II:5.3" in x.changed and x.details["flowed"][0]["via"] == "ADD-01/5.1"
    # the historical state is never rewritten: at ADD-01 the clause still reads as ADD-01 made it
    old = by["ADD-01"].state["VOL-II:5.3"].text
    assert "acceptable for the buried sections of the transmission main, subject to" in old and "trenchless" not in old
    assert "trenchless" not in by["ADD-02"].state["ADD-01:5.1"].text
    assert by["ADD-03"].status == "APPLIED" and not by["ADD-03"].scope_leak


def test_an_effective_date_is_the_one_the_provision_prints_and_the_register_shows_it(units52, earlier):
    from tenderpack.dates import Calendar
    from tenderpack.register import Register, load_rows
    ok = Op(id="ADD-03/5.2", provision="ADD-03:5.2", type="replace_text", target="ADD-01:5.1", old=OLD_52, new=NEW_52,
            effective_from="2026-10-08")
    stages = run(units52, earlier, [ok])
    x = stages[-1].ops[0]
    assert x.applied and x.details["effective_from"] == "2026-10-08" and x.details["effective"] == "retroactive"
    bad = run(units52, earlier, [ok.model_copy(update={"effective_from": "2026-10-09"})])[-1].ops[0]
    assert not bad.valid and any("effective date must be a date the provision prints" in c["detail"] for c in bad.checks)
    assert stages[-1].state["VOL-II:5.3"].history == ["ADD-01/5.1", "ADD-03/5.2"]
    reg = Register(load_rows(ROOT / "curation/register/rows.yaml"), stages, Calendar())
    row = next(r for r in reg.rf.rows if r.id == "VOL-II-5.3-01")
    at3, at1 = reg.evaluate(row, stages[-1]), reg.evaluate(row, stages[1])
    assert at3["status"].startswith("AMENDED (ADD-03/5.2)") and at3["effective"] == [
        {"op": "ADD-03/5.2", "effective_from": "2026-10-08", "effective": "retroactive"}]
    assert any(f.startswith("ADD-03/5.2: effective from 2026-10-08 (retroactive to before its issue on 2026-11-09)")
               for f in at3["flags"])
    line = next(c for c in at3["chain"] if c.startswith("ADD-03/5.2 "))
    assert "amends ADD-01:5.1, whose op ADD-01/5.1 had written the words into VOL-II:5.3" in line
    assert "trenchless" in at3["text"] and "trenchless" not in at1["text"]       # ADD-01's words at ADD-01, unchanged
    assert "acceptable for the buried sections of the transmission main, subject to" in at1["text"]


def test_words_the_earlier_op_never_wrote_change_only_that_addendum(units52, earlier):
    """Blind rehearsal 02's ADD-03 2.2 strikes ADD-01 2.1's 'The time of 14:00 Riyadh time is unchanged.', words ADD-01
    wrote nowhere: only ADD-01:2.1 changes, as before session 11 (a first draft of the flow refused this; the blind-02
    regression in test_session09_removed caught it)."""
    units = [dict(u, text=u["text"] + " Section 5.1 of Addendum No. 1 is amended by deleting ‘Volume II Clause 5.3 "
                  "is amended by adding at the end:’.") if u["unit_id"] == "ADD-03:5.2" else u for u in units52]
    op = Op(id="ADD-03/5.2", provision="ADD-03:5.2", type="replace_text", target="ADD-01:5.1",
            old="Volume II Clause 5.3 is amended by adding at the end:", new="")
    st = run(units, earlier, [op])[-1]
    x = st.ops[0]
    assert x.applied and x.changed == ["ADD-01:5.1"] and "flowed" not in x.details and "flow" not in x.details
    assert st.state["VOL-II:5.3"].history == ["ADD-01/5.1"]


def test_a_change_that_cannot_flow_is_refused_never_half_applied(base_units, earlier):
    """The words ADD-01/5.1 wrote into VOL-II:5.3 were changed by another op before ADD-03 5.2 runs: the change cannot
    flow, the op is invalid and nothing of it is applied."""
    pre = add03_unit("ADD-03:5.0", "In Volume II Clause 5.3, ‘Glass reinforced plastic pipe’ is deleted and ‘GRP pipe’ "
                     "is substituted.", label="5.0")
    units = base_units + [add03_unit("ADD-03:cover/para1", "Issued 9 November 2026", kind="paragraph"), pre,
                          add03_unit("ADD-03:5.2", FIVE_TWO, label="5.2")]
    ops = [Op(id="ADD-03/5.0", provision="ADD-03:5.0", type="replace_text", target="VOL-II:5.3",
              old="Glass reinforced plastic pipe", new="GRP pipe"),
           Op(id="ADD-03/5.2", provision="ADD-03:5.2", type="replace_text", target="ADD-01:5.1", old=OLD_52, new=NEW_52)]
    st = run(units, earlier, ops)[-1]
    x = next(r for r in st.ops if r.op.id == "ADD-03/5.2")
    assert not x.valid and any("are no longer there once as written" in c["detail"] for c in x.checks)
    assert "trenchless" not in st.state["ADD-01:5.1"].text and "trenchless" not in st.state["VOL-II:5.3"].text
    assert st.state["VOL-II:5.3"].history == ["ADD-01/5.1", "ADD-03/5.0"] and st.status == "PARTIAL"


# ---------------------------------------------------------------------------------------------- a conditional amendment

SEVEN_ONE = ("This Section 7 has effect only if the Authority notifies Bidders through the Portal, not later than ten (10) "
             "Working Days before the Proposal Due Date, that the grid connection point referred to in Volume II Clause "
             "1.4 will not be energised at least twelve (12) months before the Scheduled PCOD. If no such notice is "
             "given by that time, this Section 7 lapses.")
SEVEN_TWO = ("Where this Section 7 has effect: (a) in Volume II Clause 1.4, the words ‘together with a grid connection "
             "point at the site boundary’, and the comma before them, are deleted; (b) the grid connection is a utility "
             "to be procured by the Project Company under the second sentence of Volume II Clause 1.4; and (c) the cost "
             "of the grid connection works forms part of the Estimated Project Cost.")
TRIGGER = ("the Authority notifies Bidders through the Portal, not later than ten (10) Working Days before the Proposal "
           "Due Date, that the grid connection point referred to in Volume II Clause 1.4 will not be energised at least "
           "twelve (12) months before the Scheduled PCOD")


@pytest.fixture(scope="module")
def units7(base_units):
    return base_units + [add03_unit("ADD-03:cover/para1", "Issued 9 November 2026", kind="paragraph"),
                         add03_unit("ADD-03:7.1", SEVEN_ONE, page=2, label="7.1"),
                         add03_unit("ADD-03:7.2", SEVEN_TWO, page=2, label="7.2")]


def seven(**cond) -> Op:
    from tenderpack.amend import Condition, DeadlineRule
    c = {"id": "ADD-03/S7", "trigger": TRIGGER, "trigger_unit": "ADD-03:7.1",
         "applicability": "This Section 7 has effect only if",
         "deadline": DeadlineRule(kind="relative", anchor="PDD", offset=10, unit="working_day", direction="before",
                                  text="not later than ten (10) Working Days before the Proposal Due Date"),
         "if_not_triggered": "If no such notice is given by that time, this Section 7 lapses."}
    c.update(cond)
    return Op(id="ADD-03/7.2(a)", provision="ADD-03:7.2", type="replace_text", target="VOL-II:1.4",
              old=", together with a grid connection point at the site boundary", old_resolved="matched_in_target",
              new="", condition=Condition(**c))


FACT = {"condition": "ADD-03/S7", "occurred": True, "date": "2026-11-10", "recorded_by": "Ahmad Atieh",
        "evidence": [{"source": "Portal notice (synthetic, for this test)", "words": "will not be energised"}]}


def register(stages):
    from tenderpack.dates import Calendar
    from tenderpack.register import Register, load_rows
    reg = Register(load_rows(ROOT / "curation/register/rows.yaml"), stages, Calendar())
    return reg, next(r for r in reg.rf.rows if r.id == "VOL-II-1.4-01")


def test_a_conditional_amendment_is_kept_with_both_states_and_never_applied_without_a_recorded_trigger(units7, earlier):
    stages = run(units7, earlier, [seven()])
    st = stages[-1]
    x = st.ops[0]
    assert x.valid and x.pending and not x.applied and x.conditional_pending
    assert st.status == "APPLIED", (st.problems, [c for c in st.coverage if c["disposition"] not in ("op", "no_effect")])
    cov = {c["provision"]: c for c in st.coverage}
    assert cov["ADD-03:7.2"]["disposition"] == "conditional" == cov["ADD-03:7.1"]["disposition"]
    assert "nothing" not in cov["ADD-03:7.2"]["reason"] and "no person has recorded that it did" in cov["ADD-03:7.2"]["reason"]
    v14 = st.state["VOL-II:1.4"]
    assert v14.history == [] and "together with a grid connection point" in v14.text       # VOL-II 1.4 NOT amended
    cd = x.details["conditional"]
    assert cd["state"] == "pending" and cd["fact"] is None and cd["trigger_unit"] == "ADD-03:7.1"
    assert cd["if_triggered"]["VOL-II:1.4"]["after"] == ("The Authority will provide the site free of encumbrance. All "
                                                         "other utilities shall be procured by the Project Company.")
    assert [c["op"] for c in st.conditions] == ["ADD-03/7.2(a)"] and st.conditions[0]["state"] == "pending"
    reg, row = register(stages)
    ev = reg.evaluate(row, st)
    assert ev["status"].startswith("CONDITIONAL (ADD-03/7.2(a): not in effect unless the Authority notifies Bidders")
    assert "decide by 2026-11-12 (TRIGGER-ADD-03-S7)" in ev["status"] and ev["status"].endswith("in force: ACTIVE)")
    assert "AMENDED" not in ev["status"] and ev["active"]
    from tenderpack.schedule import in_force
    assert in_force(ev["status"])
    (c,) = ev["conditional"]
    assert c["deadline"]["value"] == "2026-11-12" and c["state"] == "pending"            # Thu 12 Nov 2026 (key IE5)
    assert c["state_if_not_triggered"]["VOL-II:1.4"] == v14.text
    assert c["state_if_triggered"]["VOL-II:1.4"].startswith("The Authority will provide the site free of encumbrance. All")
    trig = next(d for d in ev["dates"] if d["rule_id"] == "TRIGGER-ADD-03-S7")
    assert trig["planning"]["value"] == "2026-11-12" and trig["conditional"]["condition"] == "ADD-03/S7"
    assert any(f.startswith("CONDITIONAL: ADD-03/7.2(a)") and "nothing assumes the trigger occurred" in f
               for f in ev["flags"])
    # the A5 decision milestone (schedule.milestones reads the rule as plan() collects it)
    from tenderpack.schedule import milestones
    ms = milestones({trig["rule_id"]: {**trig, "rows": {row.id}}}, {}, {}, {}, set())
    assert ms[0]["date"] == "2026-11-12" and ms[0]["conditional"] and ms[0]["kind"] == "decision (conditional amendment)"
    assert ms[0]["decision"]["condition"] == "ADD-03/S7" and ms[0]["label"].startswith("Decision milestone")
    # at ADD-01 nothing of this exists
    assert "conditional" not in reg.evaluate(row, stages[1]) and reg.evaluate(row, stages[1])["status"] == "ACTIVE"


def test_the_trigger_applies_the_ops_only_when_a_person_records_it_with_evidence(units7, earlier):
    stages = run(units7, earlier, [seven()], triggers={"ADD-03/S7": FACT})
    st = stages[-1]
    x = st.ops[0]
    assert x.applied and x.details["conditional"]["state"] == "triggered"
    assert x.details["effective_from"] == "2026-11-10"
    assert st.state["VOL-II:1.4"].text.startswith("The Authority will provide the site free of encumbrance. All")
    reg, row = register(stages)
    ev = reg.evaluate(row, st)
    assert ev["status"].startswith("AMENDED (ADD-03/7.2(a))") and "CONDITIONAL" not in ev["status"]
    assert any("applies on its trigger (ADD-03/S7): recorded by Ahmad Atieh as occurred on 2026-11-10" in f
               for f in ev["flags"])
    # a record that is not a person's, or has no evidence, applies nothing and is a problem
    for bad in ({**FACT, "recorded_by": "Claude (assistant)"}, {**FACT, "evidence": []}, {**FACT, "date": "soon"}):
        st2 = run(units7, earlier, [seven()], triggers={"ADD-03/S7": bad})[-1]
        assert st2.ops[0].pending and not st2.ops[0].applied and "together with" in st2.state["VOL-II:1.4"].text
        assert st2.status == "PARTIAL" and any(p.startswith("trigger record for ADD-03/S7") for p in st2.problems)
    # recorded as NOT occurred: the unit stands, the row is ACTIVE with a flag
    st3 = run(units7, earlier, [seven()], triggers={"ADD-03/S7": {**FACT, "occurred": False, "date": "2026-11-12"}})
    reg3, row3 = register(st3)
    ev3 = reg3.evaluate(row3, st3[-1])
    assert ev3["status"] == "ACTIVE" and any("not triggered: recorded by Ahmad Atieh" in f for f in ev3["flags"])


def test_a_condition_whose_words_are_not_printed_is_invalid(units7, earlier):
    st = run(units7, earlier, [seven(trigger="the Authority decides to energise the grid connection later")])[-1]
    x = st.ops[0]
    assert not x.valid and not x.pending and st.status == "PARTIAL"
    assert any(c["id"] == "C21" and "the trigger is not in ADD-03:7.1" in c["detail"] for c in x.checks)


def test_a_pending_condition_is_carried_to_later_stages_and_never_assumed(units7, earlier):
    units = units7 + [{"unit_id": "ADD-04:cover/para1", "doc": "ADD-04", "kind": "paragraph", "pages": [1],
                       "text": "Issued 16 November 2026"}]
    f4 = OpFile(addendum="ADD-04", issued_from="ADD-04:cover/para1", prepared_by="test", method="test",
                dispositions=[Disposition(provision="ADD-04:cover/para1", disposition="no_effect", reason="issue date")])
    f3 = OpFile(addendum="ADD-03", issued_from="ADD-03:cover/para1", prepared_by="test", method="test", ops=[seven()],
                dispositions=[COVER])
    stages = Engine(units, earlier + [f3, f4]).run()
    s4 = stages[-1]
    assert s4.stage == "ADD-04" and [c["op"] for c in s4.conditions] == ["ADD-03/7.2(a)"]
    assert s4.conditions[0]["stated_at"] == "ADD-03" and s4.conditions[0]["state"] == "pending"
    reg, row = register(stages)
    ev = reg.evaluate(row, s4)                    # planned on 16 Nov, after the 12 Nov deadline: still not assumed
    assert ev["status"].startswith("CONDITIONAL (ADD-03/7.2(a)") and "together with" in s4.state["VOL-II:1.4"].text


def test_trigger_records_load_from_a_file(tmp_path):
    from tenderpack.amend import load_triggers, triggers_path
    p = tmp_path / "triggers.yaml"
    p.write_text("triggers:\n  - condition: ADD-03/S7\n    occurred: true\n    date: 2026-11-10\n"
                 "    recorded_by: Ahmad Atieh\n    evidence: [{source: Portal notice, words: will not be energised}]\n",
                 encoding="utf-8")
    t = load_triggers(p)
    assert t["ADD-03/S7"]["date"] == "2026-11-10" and t["ADD-03/S7"]["occurred"] is True
    assert load_triggers(tmp_path / "none.yaml") == {}
    assert triggers_path({}, tmp_path) == tmp_path / "curation/triggers.yaml"
    p.write_text("triggers:\n  - {condition: X}\n  - {condition: X}\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_triggers(p)


# ---------------------------------------------------------------------------------------------- 4. the cover's direction words

COVER_SENTENCE = (
    "This Addendum amends the definition of Estimated Project Cost, the financial capacity requirement in Volume I "
    "Clause 8.4 and the delay liquidated damages in Volume V Clause 18.1, relaxes the velocity limit for the treated "
    "effluent transmission main, amends Section 5.1 of Addendum No. 1, reissues the technical evaluation table to add a "
    "criterion for energy efficiency, divides Volume I Clause 11.3 into two Clauses, makes a conditional amendment to "
    "Volume II Clause 1.4, adds a Declaration of Beneficial Ownership (Form 4-H) which all Bidders may submit through the "
    "Portal within five Working Days after the Proposal Due Date, and responds to clarification requests 15 to 20.")
FIVE_ONE = ("In Volume II Clause 5.2, ‘2.0 m/s’ is deleted and ‘1.5 m/s’ is substituted. The minimum residual head of 15 m "
            "at the delivery point is unchanged.")
THREE_ONE = ("In Volume I Clause 8.4, ‘SAR 800,000,000’ is deleted and ‘twenty-five per cent (25%) of the Estimated "
             "Project Cost’ is substituted. Limb (b) of Clause 8.4 is unchanged.")


@pytest.fixture(scope="module")
def cover_run(base_units, earlier):
    units = base_units + [add03_unit("ADD-03:cover/para1", "Issued 9 November 2026", kind="paragraph"),
                          add03_unit("ADD-03:cover/para3", COVER_SENTENCE, kind="paragraph"),
                          add03_unit("ADD-03:3.1", THREE_ONE, label="3.1"),
                          add03_unit("ADD-03:5.1", FIVE_ONE, label="5.1")]
    ops = [Op(id="ADD-03/3.1", provision="ADD-03:3.1", type="replace_text", target="VOL-I:8.4", old="SAR 800,000,000",
              new="twenty-five per cent (25%) of the Estimated Project Cost"),
           Op(id="ADD-03/5.1", provision="ADD-03:5.1", type="replace_text", target="VOL-II:5.2", old="2.0 m/s",
              new="1.5 m/s")]
    disps = [COVER, Disposition(provision="ADD-03:cover/para3", disposition="no_effect", reason="the cover summary")]
    stages = run(units, earlier, ops, dispositions=disps)
    from tenderpack.summary import summary_check
    return units, stages, summary_check(stages, units)[-1]


def test_relaxes_on_a_lowered_maximum_is_contradicted_by_the_numbers(cover_run):
    """E1: the cover says 'relaxes the velocity limit'; 5.1 lowers a MAXIMUM velocity (2.0 -> 1.5 m/s): a tightening."""
    _, _, rec = cover_run
    claim = next(c for c in rec["claims"] if c["verb"] == "relaxes")
    assert claim["matched"] == ["ADD-03/5.1"], claim
    assert claim["status"] == "contradicted", claim
    f = next(x for x in rec["findings"] if x.get("claim") == claim["n"] and x["kind"] == "contradicted")
    assert "contradicted by the numbers" in f["detail"] and "maximum" in f["detail"] and "tightens" in f["detail"]
    assert "2.0 m/s -> 1.5 m/s" in f["detail"]


def test_a_direction_the_numbers_do_not_decide_is_handed_to_the_critic_with_its_evidence(base_units, earlier):
    """3.1 turns SAR 800,000,000 into 25 % of the EPC: no direction can be stated without the EPC (key: 'do NOT
    state that the requirement is relaxed or tightened'). A synthetic cover says it relaxes; C28 leaves it to a person."""
    from tenderpack.summary import critic_direction_items, summary_check
    cover = ("This Addendum relaxes the financial capacity requirement in Volume I Clause 8.4 and tightens the velocity "
             "limit for the treated effluent transmission main.")
    units = base_units + [add03_unit("ADD-03:cover/para1", "Issued 9 November 2026", kind="paragraph"),
                          add03_unit("ADD-03:cover/para3", cover, kind="paragraph"),
                          add03_unit("ADD-03:3.1", THREE_ONE, label="3.1"), add03_unit("ADD-03:5.1", FIVE_ONE, label="5.1")]
    ops = [Op(id="ADD-03/3.1", provision="ADD-03:3.1", type="replace_text", target="VOL-I:8.4", old="SAR 800,000,000",
              new="twenty-five per cent (25%) of the Estimated Project Cost"),
           Op(id="ADD-03/5.1", provision="ADD-03:5.1", type="replace_text", target="VOL-II:5.2", old="2.0 m/s",
              new="1.5 m/s")]
    stages = run(units, earlier, ops, dispositions=[COVER, Disposition(provision="ADD-03:cover/para3",
                                                                       disposition="no_effect", reason="cover")])
    rec = summary_check(stages, units)[-1]
    by = {c["verb"]: c for c in rec["claims"]}
    relax, tight = by["relaxes"], by["tightens"]
    assert relax["matched"] == ["ADD-03/3.1"] and relax["direction"][0]["verdict"] == "undecided"
    assert relax["status"] == "supported"                    # not contradicted: the numbers do not decide it
    assert "the figure changes kind" in relax["direction"][0]["why"]
    assert any(f["kind"] == "unchecked" and f["claim"] == relax["n"] and "left for the critic" in f["detail"]
               for f in rec["findings"])
    assert tight["direction"][0]["verdict"] == "supported" and tight["direction"][0]["effect"] == "tightens"
    assert tight["direction"][0]["sense"] == "maximum" and tight["direction"][0]["sense_words"] == "maximum"
    items = critic_direction_items([rec])
    assert [i["op"] for i in items] == ["ADD-03/3.1"]
    assert items[0]["evidence"]["target_text_before"].startswith("The Bidder shall demonstrate")
    assert "SAR 800,000,000" in items[0]["evidence"]["target_text_before"] and items[0]["question"]


def test_the_sense_of_a_limit_is_read_from_the_target_words():
    from tenderpack.summary import limit_sense
    t = ("The main shall be sized for the peak hourly flow in Table 2-6 with a maximum velocity of 2.0 m/s and a minimum "
         "residual head of 15 m at the delivery point.")
    assert limit_sense(t, "2.0 m/s") == ("maximum", "maximum")
    assert limit_sense(t, "15 m") == ("minimum", "minimum")
    assert limit_sense("a tangible net worth of not less than SAR 800,000,000", "SAR 800,000,000")[0] == "minimum"
    assert limit_sense("shall not exceed ten per cent (10%) of the cost", "ten per cent (10%)")[0] == "maximum"
    assert limit_sense("a period of 30 days", "30 days") == (None, "")


# ---------------------------------------------------------------------------------------------- confirming vs changing

@pytest.fixture(scope="module")
def base_state(base_units):
    from tenderpack.amend import base_state
    return base_state(base_units, ["ADD-01", "ADD-02"])


Q15 = ("No: 15 | Bidder question: Volume I Clause 8.7 requires a Parent Company Guarantee that is unconditional as to "
       "the EPC Contractor's obligations during the construction period. Will the Authority accept a guarantee limited "
       "to a fixed amount? | Authority response: No. The Parent Company Guarantee shall be unlimited as to the "
       "guaranteed obligations and shall not be conditional on any demand first being made of the EPC Contractor. "
       "Volume I Clause 8.7 and Form 4-D apply.")
Q16 = ("No: 16 | Bidder question: Does the Estimated Project Cost to be stated in Form 4-F include the cost of the grid "
       "connection works? | Authority response: Only if Section 7 of this Addendum has effect. Otherwise the grid "
       "connection point is provided by the Authority in accordance with Volume II Clause 1.4.")
Q18 = ("No: 18 | Bidder question: Does the maximum velocity in Volume II Clause 5.2 apply to the trenchless crossings? | "
       "Authority response: Yes. Volume II Clause 5.2, as amended by Section 5.1 of this Addendum, applies to the whole "
       "length of the transmission main, including the crossings required by Volume II Clause 5.4.")
Q19 = ("No: 19 | Bidder question: How is compliance with Volume I Clause 8.4(a), as amended, to be demonstrated in "
       "Envelope A, given that the Estimated Project Cost is stated only in Form 4-F? | Authority response: The Authority "
       "notes the question. Volume I Clauses 6.2 and 11.1 apply. The Authority does not consider further amendment "
       "necessary at this stage.")


def test_a_decoy_that_restates_the_clause_and_the_form_confirms_and_adds_nothing(base_state):
    from tenderpack.summary import answer_targets, classify_answer, confirms_check
    tg = answer_targets(base_state, ["VOL-I:8.7", "VOL-IV:F4-D"])
    assert "VOL-IV:F4-D/item3" in tg and "VOL-I:8.7" in tg
    c = classify_answer(Q15, tg)
    assert c["class"] == "confirms" and c["evidence"] == [], c
    ok, detail, _ = confirms_check(Q15, tg)
    assert ok and detail.startswith("a confirming answer")
    q16 = classify_answer(Q16, answer_targets(base_state, ["VOL-II:1.4", "VOL-IV:F4-F"]), context=[SEVEN_TWO])
    assert q16["class"] == "confirms", q16
    assert classify_answer(Q19, answer_targets(base_state, ["VOL-I:8.4"]))["class"] in ("none", "confirms")


def test_an_answer_that_changes_or_adds_a_requirement_is_not_a_confirmation_and_names_its_words(base_state):
    from tenderpack.summary import answer_targets, classify_answer, confirms_check
    q18 = classify_answer(Q18, answer_targets(base_state, ["VOL-II:5.2", "VOL-II:5.4"]))
    assert q18["class"] == "interprets" and {"length", "transmission"} <= set(q18["evidence"][0]["words"]), q18
    tg = answer_targets(base_state, ["VOL-I:9.4"])
    adds = "Authority response: Yes. Each member shall also submit a certified copy of its commercial registration."
    a = classify_answer(adds, tg)
    assert a["class"] == "adds" and {"certified", "commercial", "registration"} <= set(a["evidence"][0]["words"])
    ok, detail, _ = confirms_check(adds, tg)
    assert not ok and "annotated 'confirms', but the answer adds" in detail and "registration" in detail
    chg = classify_answer("Authority response: The period is extended to fifteen (15) Working Days.",
                          answer_targets(base_state, ["VOL-I:5.2"]))
    assert chg["class"] == "changes" and "is extended" in chg["evidence"][0]["words"][0]
    fig = classify_answer("Authority response: Requests shall be submitted no later than twelve (12) Working Days "
                          "before the Proposal Due Date.", answer_targets(base_state, ["VOL-I:5.2"]))
    assert fig["class"] == "changes" and "12" in fig["evidence"][0]["words"]


def test_the_controller_holds_a_confirms_annotation_whose_answer_adds_words_for_a_person(tmp_path):
    """The semantic check's hook (controller._semantic_checks, session 11): ADD-02 Q10 restates VOL-I 8.7 and verifies;
    Q9 ('An English translation may be attached for convenience only') prints words Form 4-C does not: a 'confirms'
    annotation on it is pending for a person (never invalid), with the words named."""
    from test_session10_controls_ai import _ref, _set, hermetic_workspace

    from tenderpack.ai import controller
    from tenderpack.ai.contract import ChangeProposal
    ws = hermetic_workspace(tmp_path)
    st = ws.identity()

    def confirms(q, targets):
        return ChangeProposal(id=f"ADD-02/{q}", state=st, statement_type="amendment_op", provision=f"ADD-02:{q}",
                              payload={"type": "annotate", "targets": targets, "effect": "confirms"},
                              evidence=[_ref(f"ADD-02:{q}")])
    ps = _set(ws, "ADD-02", [confirms("Q10", ["VOL-I:8.7"]), confirms("Q9", ["VOL-IV:F4-C"])])
    controller.validate_set(ws, ps)
    by = {it.provision: it for it in ps.items}
    q10 = [v for v in by["ADD-02:Q10"].validation if v.check == "semantic"]
    assert by["ADD-02:Q10"].verification_status == "evidence_verified"
    assert any(v.ok and v.detail.startswith("a confirming answer") for v in q10)
    q9 = by["ADD-02:Q9"]
    assert q9.verification_status == "interpretation_pending", [(v.check, v.ok, v.detail) for v in q9.validation]
    sem = next(v for v in q9.validation if v.check == "semantic" and not v.ok)
    assert "annotated 'confirms', but the answer interprets" in sem.detail and "translation" in sem.detail
    assert "ADD-02:Q9" not in ps.resolution.no_change_on_amendment_language    # that list is provision_semantics'
