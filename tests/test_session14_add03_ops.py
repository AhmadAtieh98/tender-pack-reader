"""Session 14 (W3): the ADD-03 changes the engine could not write (report §9 L25; rehearsals/blind-07/COMPARISON.md §8
item 6; the escalations of rehearsals/blind-07/review/index.md "First: unresolved provisions and escalations").

Blind-07 escalated five kinds of change as "software limitation": a clause relocated between volumes, a clause inserted
where the provision names no target (only its new number), a table that "forms part of" a volume, a scoped
disapplication of a clause, and a relative change of an amount ("reduced by SAR 1,000,000", with not even a computed
value offered). Each is reproduced here on a SYNTHETIC pack (invented volumes and addenda built in this file, never the
real pack's text), then handled by the existing op model:

  relocate_unit   (new op type)  {target, to, anchor?, new_text?}
  insert_unit     (extended)     {anchor, number, new_text}: the position is the one the stated number implies
  insert_table    (new op type)  {new_group, into, number}
  annotate        (new effect)   effect: disapplies, scope: the class the clause does not apply to
  adjust_value    (new op type)  {target, change, old?, column?}: the value is computed (calc.relative_change), never typed

and blocked ops, unresolved dispositions and pending image readings make CONDITIONAL impact investigations
(amend.conditional_impacts; StageResult.impacts), never accepted facts.
"""
from __future__ import annotations

import pytest

from tenderpack import calc
from tenderpack.amend import (Disposition, Engine, Op, OpFile, conditional_impacts, describe_op,
                              unevidenced_additions, validated_stage)

# ---------------------------------------------------------------------------------------------- the synthetic pack


def U(uid, text, kind="clause", page=1, **kw):
    doc = uid.split(":")[0]
    d = {"unit_id": uid, "doc": doc, "kind": kind, "pages": [page], "text": text}
    if kind == "clause" and "label" not in kw:
        d["label"] = uid.split(":")[1]
    d.update(kw)
    return d


VOLUMES = [
    U("VOL-I:H:C3", "3 Communications", kind="heading"),
    U("VOL-I:3.2", "No Bidder shall contact any officer, employee, consultant or advisor of the Authority other than "
                   "through the Portal. Breach of this Clause shall result in the disqualification of the Bidder."),
    U("VOL-I:3.3", "The Authority may arrange site visits for Bidders."),
    U("VOL-II:H:C8", "8 Handover", kind="heading", page=2),
    U("VOL-II:8.4", "The Project Company shall keep as-built records.", page=2),
    U("VOL-II:8.5", "A plant condition audit shall be carried out in the final three (3) years of the term, and any "
                    "defects found shall be remedied before handover:", page=2),
    U("VOL-II:8.5(a)", "(a) by an auditor approved by the Authority; and", kind="list_item", page=2,
      parent="VOL-II:8.5", label="(a)"),
    U("VOL-II:8.5(b)", "(b) at the cost of the Project Company.", kind="list_item", page=2, parent="VOL-II:8.5",
      label="(b)"),
    U("VOL-II:8.6", "Spare parts shall be handed over with the plant.", page=2),
    U("VOL-V:H:C30", "30 Change in Law", kind="heading", page=3),
    U("VOL-V:30.1", "A General Change in Law entitles the Project Company to compensation only to the extent that the "
                    "capital expenditure it requires exceeds SAR 4,000,000 in aggregate over the term.", page=3),
    U("VOL-V:30.2", "Compensation is capped at five million Saudi Riyals (SAR 5,000,000) per event.", page=3),
    U("VOL-V:T30-1", "Table 30-1 Indexation", kind="table", page=3, label="Table 30-1 Indexation"),
    U("VOL-V:T30-1/A", "Item: A | Unit: % | Rate: 2.5", kind="table_row", page=3, parent="VOL-V:T30-1", label="A",
      cells={"Item": "A", "Unit": "%", "Rate": "2.5"}),
    U("VOL-V:T30-1/B", "Item: B | Unit: SAR | Rate: 200,000", kind="table_row", page=3, parent="VOL-V:T30-1",
      label="B", cells={"Item": "B", "Unit": "SAR", "Rate": "200,000"}),
    U("VOL-V:H:C50", "50 Handback", kind="heading", page=4),
    U("VOL-V:50.1", "The handback requirements are those of Volume II Clause 8.5 and of this Clause 50.", page=4),
    U("VOL-V:50.2", "A handback reserve shall be funded from year twenty (20) of the term.", page=4),
    U("VOL-V:H:C52", "52 Spares", kind="heading", page=4),
    U("VOL-V:52.1", "The Project Company shall hold the spares listed in Schedule 4.", page=4),
]

ADD01 = [
    U("ADD-01:cover/para1", "Issued 1 October 2026", kind="paragraph"),
    U("ADD-01:1.1", "In Volume V Clause 30.1, ‘SAR 4,000,000’ is deleted and ‘SAR 3,000,000’ is substituted."),
]
ADD01_OPS = OpFile(addendum="ADD-01", issued_from="ADD-01:cover/para1", prepared_by="test", method="test",
                   ops=[Op(id="ADD-01/1.1", provision="ADD-01:1.1", type="replace_text", target="VOL-V:30.1",
                           old="SAR 4,000,000", new="SAR 3,000,000")],
                   dispositions=[Disposition(provision="ADD-01:cover/para1", disposition="no_effect", reason="date")])

COVER2 = U("ADD-02:cover/para1", "Issued 20 October 2026", kind="paragraph")


def run(add02_units, ops, dispositions=(), withdrawn=None):
    f = OpFile(addendum="ADD-02", issued_from="ADD-02:cover/para1", prepared_by="test", method="test", ops=list(ops),
               dispositions=[Disposition(provision="ADD-02:cover/para1", disposition="no_effect", reason="date"),
                             *dispositions])
    units = VOLUMES + ADD01 + [COVER2] + list(add02_units)
    eng = Engine(units, [ADD01_OPS, f], withdrawn=withdrawn)
    stages = eng.run()
    run.engine = eng                                  # the unit order after the run (insertions and relocations)
    return {s.stage: s for s in stages}, stages


def failed(x):
    return [c for c in x.checks if not c["ok"]]


def res(by, op_id):
    return next(x for x in by["ADD-02"].ops if x.op.id == op_id)


# ---------------------------------------------------------------------------------------------- (e) relative change

P_REDUCE = U("ADD-02:1.1", "The amount stated in Volume V Clause 30.1 is reduced by SAR 1,000,000.")


def test_relative_change_is_computed_from_the_previous_effective_value_never_typed():
    op = Op(id="ADD-02/1.1", provision="ADD-02:1.1", type="adjust_value", target="VOL-V:30.1",
            change="reduced by SAR 1,000,000")
    by, stages = run([P_REDUCE], [op])
    x = res(by, "ADD-02/1.1")
    assert x.applied, failed(x)
    # the previous EFFECTIVE value is ADD-01's SAR 3,000,000, never the issued SAR 4,000,000
    assert "exceeds SAR 2,000,000 in aggregate" in by["ADD-02"].state["VOL-V:30.1"].text
    assert by["ADD-01"].state["VOL-V:30.1"].text.count("SAR 3,000,000") == 1          # earlier stages are copies
    c = x.details["computed"]
    assert c["method"] == "relative_change" and c["status"] == "resolved" and c["value"] == 2000000
    assert c["steps"] == ["SAR 3,000,000 - SAR 1,000,000 = SAR 2,000,000"]
    srcs = {o["name"]: o["source"] for o in c["operands"]}
    assert srcs["previous"]["unit"] == "VOL-V:30.1" and srcs["previous"]["words"] == "SAR 3,000,000"
    assert srcs["change"]["unit"] == "ADD-02:1.1" and srcs["change"]["words"] == "reduced by SAR 1,000,000"
    assert x.details["previous_value"] == "SAR 3,000,000" and x.details["new_value"] == "SAR 2,000,000"
    assert "ADD-01/1.1" in x.details["previous_as_of"]
    assert "PROPOSED" in x.details["proposal"]
    assert x.changed == ["VOL-V:30.1"] and by["ADD-02"].state["VOL-V:30.1"].history == ["ADD-01/1.1", "ADD-02/1.1"]
    assert by["ADD-02"].status == "APPLIED"
    # the C47 guard accepts the computed figure (it is derived from printed words), and nothing else
    assert unevidenced_additions(by["ADD-01"].state, by["ADD-02"].state, "ADD-02") == []
    assert "SAR 3,000,000 -> SAR 2,000,000" in describe_op(x)


def test_relative_change_refuses_a_typed_value_and_unprinted_change_words():
    typed = Op(id="ADD-02/1.1", provision="ADD-02:1.1", type="adjust_value", target="VOL-V:30.1",
               change="reduced by SAR 1,000,000", new="SAR 2,000,000")
    by, _ = run([P_REDUCE], [typed])
    x = res(by, "ADD-02/1.1")
    assert not x.valid and any("never typed" in c["detail"] for c in failed(x))
    assert "SAR 3,000,000" in by["ADD-02"].state["VOL-V:30.1"].text            # nothing half applied
    unprinted = Op(id="ADD-02/1.1", provision="ADD-02:1.1", type="adjust_value", target="VOL-V:30.1",
                   change="reduced by SAR 2,000,000")
    by, _ = run([P_REDUCE], [unprinted])
    assert not res(by, "ADD-02/1.1").valid


def test_relative_change_by_a_percentage_and_on_a_table_cell():
    p = U("ADD-02:1.2", "In Table 30-1 of Volume V, the Rate in row 'B' is increased by 10%.")
    op = Op(id="ADD-02/1.2", provision="ADD-02:1.2", type="adjust_value", target="VOL-V:T30-1/B", column="Rate",
            change="increased by 10%")
    by, _ = run([p], [op])
    x = res(by, "ADD-02/1.2")
    assert x.applied, failed(x)
    row = by["ADD-02"].state["VOL-V:T30-1/B"]
    assert row.cells["Rate"] == "220,000" and "Rate: 220,000" in row.text
    assert x.details["computed"]["steps"] == ["SAR 200,000 x (1 + 10%) = SAR 220,000"]
    assert unevidenced_additions(by["ADD-01"].state, by["ADD-02"].state, "ADD-02") == []


def test_relative_change_of_a_percentage_by_a_percentage_is_left_to_a_person():
    # 'increased by 10%' of a rate in % is either ten points or a tenth more: the engine never picks one
    p = U("ADD-02:1.3", "In Table 30-1 of Volume V, the Rate in row 'A' is increased by 10%.")
    op = Op(id="ADD-02/1.3", provision="ADD-02:1.3", type="adjust_value", target="VOL-V:T30-1/A", column="Rate",
            change="increased by 10%")
    by, _ = run([p], [op])
    x = res(by, "ADD-02/1.3")
    assert not x.valid and any("percentage points" in c["detail"] for c in failed(x))
    assert by["ADD-02"].state["VOL-V:T30-1/A"].cells["Rate"] == "2.5"


def test_relative_change_refuses_an_amount_also_written_in_words_and_an_ambiguous_figure():
    p = U("ADD-02:1.4", "The cap stated in Volume V Clause 30.2 is reduced by SAR 1,000,000.")
    op = Op(id="ADD-02/1.4", provision="ADD-02:1.4", type="adjust_value", target="VOL-V:30.2",
            change="reduced by SAR 1,000,000")
    by, _ = run([p], [op])
    x = res(by, "ADD-02/1.4")
    assert not x.valid and any("in words" in c["detail"] for c in failed(x)), failed(x)
    # a clause with two figures of the change's unit needs `old` to name the previous value
    two = U("VOL-V:30.3", "The deductible is SAR 100,000 per claim and SAR 500,000 per year.", page=3)
    p2 = U("ADD-02:1.5", "The yearly amount in Volume V Clause 30.3 is increased by SAR 50,000.")
    amb = Op(id="ADD-02/1.5", provision="ADD-02:1.5", type="adjust_value", target="VOL-V:30.3",
             change="increased by SAR 50,000")
    f = OpFile(addendum="ADD-02", issued_from="ADD-02:cover/para1", prepared_by="t", method="t", ops=[amb],
               dispositions=[Disposition(provision="ADD-02:cover/para1", disposition="no_effect", reason="d")])
    by2 = {s.stage: s for s in Engine(VOLUMES + [two] + ADD01 + [COVER2, p2], [ADD01_OPS, f]).run()}
    x2 = next(x for x in by2["ADD-02"].ops)
    assert not x2.valid and any("`old`" in c["detail"] for c in failed(x2)), failed(x2)
    named = amb.model_copy(update={"old": "SAR 500,000 per year"})
    f2 = f.model_copy(update={"ops": [named]})
    by3 = {s.stage: s for s in Engine(VOLUMES + [two] + ADD01 + [COVER2, p2], [ADD01_OPS, f2]).run()}
    x3 = next(x for x in by3["ADD-02"].ops)
    assert x3.applied, failed(x3)
    assert by3["ADD-02"].state["VOL-V:30.3"].text == "The deductible is SAR 100,000 per claim and SAR 550,000 per year."


def test_calc_relative_change_methods():
    r = calc.compute("relative_change", {"previous": {"value": 2500000, "unit": "SAR"},
                                         "change": {"source": {"unit": "X", "words": "reduced by SAR 1,000,000"}},
                                         "direction": "decrease"})
    assert r["status"] == "resolved" and r["value"] == 1500000 and r["text"] == "SAR 1,500,000"
    neg = calc.compute("relative_change", {"previous": {"value": 500000, "unit": "SAR"},
                                           "change": {"value": 1000000, "unit": "SAR"}, "direction": "decrease"})
    assert neg["status"] == "unresolved" and "below zero" in neg["reason"]
    mism = calc.compute("relative_change", {"previous": {"value": 5, "unit": "mm"},
                                            "change": {"value": 1, "unit": "SAR"}, "direction": "increase"})
    assert mism["status"] == "unresolved" and "unit mismatch" in mism["reason"]
    expr = calc.compute("relative_change", {"previous": {"value": "2,500,000 - 1", "unit": "SAR"},
                                            "change": {"value": 1, "unit": "SAR"}, "direction": "increase"})
    assert expr["status"] == "unresolved"                                     # nothing is evaluated
    assert "relative_change" in calc.METHODS


# ---------------------------------------------------------------------------------------------- (a) relocation

P_RELOC = U("ADD-02:2.1", "Volume II Clause 8.5 is relocated to Volume V, in which it becomes Clause 50.3. Its text is "
                          "unchanged.")


def test_a_clause_relocated_between_volumes_keeps_history_and_lineage():
    op = Op(id="ADD-02/2.1", provision="ADD-02:2.1", type="relocate_unit", target="VOL-II:8.5", to="VOL-V:50.3")
    by, stages = run([P_RELOC], [op])
    x = res(by, "ADD-02/2.1")
    assert x.applied, failed(x)
    st = by["ADD-02"].state
    old, new = st["VOL-II:8.5"], st["VOL-V:50.3"]
    assert old.status == "superseded" and old.superseded_by == "VOL-V:50.3" and old.relocated_to == "VOL-V:50.3"
    assert new.doc == "VOL-V" and new.status == "active" and new.relocated_from == "VOL-II:8.5"
    assert new.text == by["ADD-01"].state["VOL-II:8.5"].text and new.label == "50.3"
    assert old.history == ["ADD-02/2.1"] and new.history == ["ADD-02/2.1"]
    # its list items move with it, in order, after VOL-V 50.2 and before the next clause group
    assert st["VOL-V:50.3(a)"].parent == "VOL-V:50.3" and st["VOL-II:8.5(a)"].superseded_by == "VOL-V:50.3(a)"
    eng_order = [k for k in run.engine.order if k.startswith("VOL-V:")]
    assert x.details["placed"] == ["VOL-V:50.3", "VOL-V:50.3(a)", "VOL-V:50.3(b)"]
    assert eng_order[eng_order.index("VOL-V:50.2") + 1: eng_order.index("VOL-V:50.2") + 4] == [
        "VOL-V:50.3", "VOL-V:50.3(a)", "VOL-V:50.3(b)"]
    assert x.details["lineage"] == {"VOL-II:8.5": "VOL-V:50.3", "VOL-II:8.5(a)": "VOL-V:50.3(a)",
                                    "VOL-II:8.5(b)": "VOL-V:50.3(b)"}
    # rows following replacements reach the new unit; others see the old unit REPLACED, never unchanged
    from tenderpack.register import effective
    assert effective(st, "VOL-II:8.5", True).unit_id == "VOL-V:50.3"
    assert effective(st, "VOL-II:8.5", False).status == "superseded"
    assert by["ADD-02"].status == "APPLIED" and not by["ADD-02"].scope_leak
    assert unevidenced_additions(by["ADD-01"].state, st, "ADD-02") == []        # the text is the old unit's own
    assert "relocated VOL-II:8.5 -> VOL-V:50.3" in describe_op(x)


def test_a_relocation_is_refused_atomically_when_the_destination_number_is_taken_or_unprinted():
    taken = U("ADD-02:2.1", "Volume II Clause 8.5 is relocated to Volume V, in which it becomes Clause 50.2.")
    op = Op(id="ADD-02/2.1", provision="ADD-02:2.1", type="relocate_unit", target="VOL-II:8.5", to="VOL-V:50.2")
    by, stages = run([taken], [op])
    x = res(by, "ADD-02/2.1")
    assert not x.valid and by["ADD-02"].status == "PARTIAL"
    st = by["ADD-02"].state
    assert st["VOL-II:8.5"].status == "active" and st["VOL-II:8.5"].history == [] and "VOL-V:50.2+ADD-02" not in st
    # the staged set rolls back to the validated state: the last stage reached through APPLIED addenda only
    assert validated_stage(stages).stage == "ADD-01"
    unprinted = Op(id="ADD-02/2.1", provision="ADD-02:2.1", type="relocate_unit", target="VOL-II:8.5",
                   to="VOL-V:50.4")
    by, _ = run([P_RELOC], [unprinted])
    assert not res(by, "ADD-02/2.1").valid


def test_a_relocated_clause_is_cited_by_later_ops_by_its_new_number():
    p = U("ADD-02:2.2", "In Volume V Clause 50.1, ‘Volume II Clause 8.5’ is deleted and ‘Clause 50.3’ is substituted.")
    ops = [Op(id="ADD-02/2.1", provision="ADD-02:2.1", type="relocate_unit", target="VOL-II:8.5", to="VOL-V:50.3"),
           Op(id="ADD-02/2.2", provision="ADD-02:2.2", type="replace_text", target="VOL-V:50.1",
              old="Volume II Clause 8.5", new="Clause 50.3")]
    by, _ = run([P_RELOC, p], ops)
    assert all(x.applied for x in by["ADD-02"].ops), [failed(x) for x in by["ADD-02"].ops]
    assert by["ADD-02"].status == "APPLIED"


# ---------------------------------------------------------------------------------------------- (b) insertion by number

P_NEW = U("ADD-02:3.1", "The following new Clause 52.2 is added to Volume V: ‘The Project Company shall keep a "
                        "register of spare parts.’")


def test_a_clause_inserted_by_its_stated_number_where_the_provision_names_no_target():
    op = Op(id="ADD-02/3.1", provision="ADD-02:3.1", type="insert_unit", anchor="VOL-V:52.1", number="52.2",
            new_text="The Project Company shall keep a register of spare parts.")
    by, _ = run([P_NEW], [op])
    x = res(by, "ADD-02/3.1")
    assert x.applied, failed(x)
    u = by["ADD-02"].state["VOL-V:52.1+ADD-02"]
    assert u.doc == "VOL-V" and u.label == "52.2" and u.inserted_after == "VOL-V:52.1"
    assert x.details["inserted_as"] == "52.2" and x.details["position"].startswith("stated by its number")
    assert by["ADD-02"].status == "APPLIED"


@pytest.mark.parametrize("anchor,number,why", [
    ("VOL-V:50.2", "52.2", "is not the clause"),          # the stated number puts it after 52.1, not 50.2
    ("VOL-V:52.1", "52.3", "not printed"),                # the provision prints 52.2
    ("VOL-V:30.1", "30.2", "not printed"),                # 30.2 exists and is not printed either
])
def test_an_insertion_by_number_is_refused_when_the_position_does_not_follow_from_it(anchor, number, why):
    op = Op(id="ADD-02/3.1", provision="ADD-02:3.1", type="insert_unit", anchor=anchor, number=number,
            new_text="The Project Company shall keep a register of spare parts.")
    by, _ = run([P_NEW], [op])
    x = res(by, "ADD-02/3.1")
    assert not x.valid and any(why in c["detail"] for c in failed(x)), failed(x)
    assert not any(k.endswith("+ADD-02") for k in by["ADD-02"].state)


def test_an_insertion_by_number_is_refused_when_that_number_exists():
    p = U("ADD-02:3.2", "The following new Clause 50.2 is added to Volume V: ‘The reserve shall be audited.’")
    op = Op(id="ADD-02/3.2", provision="ADD-02:3.2", type="insert_unit", anchor="VOL-V:50.1", number="50.2",
            new_text="The reserve shall be audited.")
    by, _ = run([p], [op])
    x = res(by, "ADD-02/3.2")
    assert not x.valid and any("already" in c["detail"] for c in failed(x)), failed(x)


# ---------------------------------------------------------------------------------------------- (c) a table into a volume

P_TABLE = U("ADD-02:4.1", "Table 50-1 is reproduced in the Appendix to this Addendum and forms part of Volume V.")
TABLE = [U("ADD-02:T50-1", "Table 50-1 Residual life", kind="table", page=2, label="Table 50-1 Residual life"),
         U("ADD-02:T50-1/1", "Class: Civil | Years: 20", kind="table_row", page=2, parent="ADD-02:T50-1", label="1",
           cells={"Class": "Civil", "Years": "20"}),
         U("ADD-02:T50-1/2", "Class: Mechanical | Years: 5", kind="table_row", page=2, parent="ADD-02:T50-1",
           label="2", cells={"Class": "Mechanical", "Years": "5"})]


def test_a_table_inserted_into_a_volume_as_a_new_group():
    op = Op(id="ADD-02/4.1", provision="ADD-02:4.1", type="insert_table", new_group="ADD-02:T50-1", into="VOL-V",
            number="50-1")
    by, _ = run([P_TABLE] + TABLE, [op])
    x = res(by, "ADD-02/4.1")
    assert x.applied, failed(x)
    st = by["ADD-02"].state
    assert all(st[k].part_of == "VOL-V" for k in ("ADD-02:T50-1", "ADD-02:T50-1/1", "ADD-02:T50-1/2"))
    assert x.details["inserted_as"] == "VOL-V:T50-1" and "reading_status" not in x.details
    cov = {c["provision"]: c["disposition"] for c in by["ADD-02"].coverage}
    assert cov["ADD-02:T50-1/1"] == "op" and cov["ADD-02:T50-1/2"] == "op"          # the rows are content of the op
    assert by["ADD-02"].status == "APPLIED" and by["ADD-02"].impacts == []
    assert "forms part of VOL-V as Table 50-1" in describe_op(x)


def test_an_image_table_whose_reading_is_pending_stays_conditional():
    img = [U("ADD-02:T50-1", "Table 50-1", kind="table", page=2),
           U("ADD-02:T50-1/image/r1", "م: ١ | الفئة: مدني | السنوات: ٢٠", kind="table_row", page=2,
             parent="ADD-02:T50-1", origin="image_reading", cells={"م": "١", "السنوات": "٢٠"},
             reading={"status": "pending", "region": "ADD-02-p2-r1", "subject_sha256": "abc"})]
    op = Op(id="ADD-02/4.1", provision="ADD-02:4.1", type="insert_table", new_group="ADD-02:T50-1", into="VOL-V",
            number="50-1")
    by, _ = run([P_TABLE] + img, [op])
    x = res(by, "ADD-02/4.1")
    assert x.applied, failed(x)
    assert x.details["reading_status"] == "pending"
    assert x.details["conditional_on_readings"] == {"ADD-02-p2-r1": ["ADD-02:T50-1/image/r1"]}
    imp = [i for i in by["ADD-02"].impacts if i["conditional_on"]["kind"] == "reading"]
    assert imp and imp[0]["conditional_on"]["ref"] == "ADD-02-p2-r1" and imp[0]["accepted"] is False
    assert "conditional on reading ADD-02-p2-r1" in imp[0]["investigate"]
    assert "CONDITIONAL" in describe_op(x)


def test_a_table_insertion_is_refused_when_the_provision_does_not_make_it_part_of_that_volume():
    p = U("ADD-02:4.1", "Table 50-1 is reproduced in the Appendix to this Addendum for information.")
    op = Op(id="ADD-02/4.1", provision="ADD-02:4.1", type="insert_table", new_group="ADD-02:T50-1", into="VOL-V",
            number="50-1")
    by, _ = run([p] + TABLE, [op])
    x = res(by, "ADD-02/4.1")
    assert not x.valid and all(by["ADD-02"].state[k].part_of is None for k in ("ADD-02:T50-1", "ADD-02:T50-1/1"))


# ---------------------------------------------------------------------------------------------- (d) disapplication

P_DIS = U("ADD-02:5.1", "Volume I Clause 3.2 does not apply to communications with the Authority's survey contractor "
                        "during a site visit under Volume I Clause 3.3.")
SCOPE = "communications with the Authority's survey contractor during a site visit under Volume I Clause 3.3"


def test_a_scoped_disapplication_records_an_exception_and_leaves_the_clause_text():
    op = Op(id="ADD-02/5.1", provision="ADD-02:5.1", type="annotate", targets=["VOL-I:3.2"], effect="disapplies",
            scope=SCOPE)
    by, _ = run([P_DIS], [op])
    x = res(by, "ADD-02/5.1")
    assert x.applied, failed(x)
    u = by["ADD-02"].state["VOL-I:3.2"]
    assert u.text == by["ADD-01"].state["VOL-I:3.2"].text and u.status == "active"
    assert "ADD-02/5.1" in u.annotations                     # its pin changes: rows on the clause are re-read
    assert u.exceptions == [{"op": "ADD-02/5.1", "provision": "ADD-02:5.1", "scope": SCOPE,
                             "words": "does not apply"}]
    assert x.details["exception"]["scope"] == SCOPE
    assert "disapplies VOL-I:3.2" in describe_op(x) and SCOPE in describe_op(x)


@pytest.mark.parametrize("scope,text", [
    (None, None),                                                          # no scope: that is a deletion, not an exception
    ("communications with any person", None),                             # scope not printed
    (SCOPE, "Volume I Clause 3.2 is clarified for communications with the Authority's survey contractor during a "
            "site visit under Volume I Clause 3.3."),                    # no disapplication words
])
def test_a_disapplication_needs_its_printed_scope_and_words(scope, text):
    p = U("ADD-02:5.1", text) if text else P_DIS
    op = Op(id="ADD-02/5.1", provision="ADD-02:5.1", type="annotate", targets=["VOL-I:3.2"], effect="disapplies",
            scope=scope)
    by, _ = run([p], [op])
    x = res(by, "ADD-02/5.1")
    assert not x.valid
    assert by["ADD-02"].state["VOL-I:3.2"].exceptions == [] and by["ADD-02"].state["VOL-I:3.2"].annotations == []


# ---------------------------------------------------------------------------------------------- conditional impacts

def test_blocked_ops_and_unresolved_dispositions_make_conditional_investigations_never_facts():
    bad = Op(id="ADD-02/1.1", provision="ADD-02:1.1", type="adjust_value", target="VOL-V:30.1",
             change="reduced by SAR 9,000,000")                              # not printed: invalid
    p2 = U("ADD-02:6.1", "The handback reserve is to be reviewed.")
    d = Disposition(provision="ADD-02:6.1", disposition="unresolved", reason="ambiguous: which reserve",
                    candidates=["VOL-V:50.2"])
    by, _ = run([P_REDUCE, p2], [bad], dispositions=[d])
    imps = {i["conditional_on"]["ref"]: i for i in by["ADD-02"].impacts}
    a = imps["ADD-02/1.1"]
    assert a["conditional_on"] == {"kind": "op", "ref": "ADD-02/1.1", "state": "invalid", "why": a["conditional_on"]["why"]}
    assert "C21" in a["conditional_on"]["why"] and a["units"] == ["VOL-V:30.1"] and a["accepted"] is False
    assert a["investigate"].startswith("conditional on op ADD-02/1.1 (invalid")
    b = imps["ADD-02:6.1"]
    assert b["conditional_on"]["kind"] == "disposition" and b["units"] == ["VOL-V:50.2"]
    assert "ambiguous: which reserve" in b["conditional_on"]["why"]
    # the same list, recomputed from the stage (the one shape W2's downstream consumes)
    assert conditional_impacts(by["ADD-02"]) == by["ADD-02"].impacts
    # nothing was applied: the value stands, and the stage is PARTIAL
    assert "SAR 3,000,000" in by["ADD-02"].state["VOL-V:30.1"].text and by["ADD-02"].status == "PARTIAL"


def test_a_person_withdrawn_op_makes_no_investigation():
    op = Op(id="ADD-02/1.1", provision="ADD-02:1.1", type="adjust_value", target="VOL-V:30.1",
            change="reduced by SAR 1,000,000")
    by, _ = run([P_REDUCE], [op], withdrawn={"ADD-02/1.1": {"reviewer": "A Person", "date": "2026-10-21"}})
    assert by["ADD-02"].impacts == []


# ---------------------------------------------------------------------------------------------- schema and rendering

def test_the_payload_schema_and_the_policy_name_the_new_kinds():
    from tenderpack.ai.contract import payload_schemas
    from tenderpack.util import ROOT
    s = payload_schemas()["amendment_op"]
    types = s["properties"]["type"]["enum"]
    for t in ("relocate_unit", "insert_table", "adjust_value"):
        assert t in types
    for f in ("to", "number", "into", "scope", "change"):
        assert f in s["properties"]
    effects = [x for x in s["properties"]["effect"]["anyOf"] if "enum" in x][0]["enum"]
    assert "disapplies" in effects
    pol = (ROOT / "tenderpack/ai/policy/20_analysis.md").read_text(encoding="utf-8")
    for t in ("relocate_unit", "insert_table", "adjust_value", "disapplies"):
        assert t in pol


def test_an_existing_op_dumps_exactly_as_before():
    # the decision bindings hash an op's dump: the new fields are absent unless used
    d = Op(id="X/1", provision="X:1", type="replace_text", target="VOL-I:3.2", old="a", new="b").model_dump()
    assert not {"to", "number", "into", "scope", "change"} & set(d)


def test_a2_and_the_live_view_render_the_new_kinds():
    from tenderpack.stage2 import op_change
    from tenderpack.summary import _does
    ops = [Op(id="ADD-02/1.1", provision="ADD-02:1.1", type="adjust_value", target="VOL-V:30.1",
              change="reduced by SAR 1,000,000"),
           Op(id="ADD-02/2.1", provision="ADD-02:2.1", type="relocate_unit", target="VOL-II:8.5", to="VOL-V:50.3"),
           Op(id="ADD-02/4.1", provision="ADD-02:4.1", type="insert_table", new_group="ADD-02:T50-1", into="VOL-V",
              number="50-1"),
           Op(id="ADD-02/5.1", provision="ADD-02:5.1", type="annotate", targets=["VOL-I:3.2"], effect="disapplies",
              scope=SCOPE)]
    by, stages = run([P_REDUCE, P_RELOC, P_TABLE, P_DIS] + TABLE, ops)
    assert by["ADD-02"].status == "APPLIED", [failed(x) for x in by["ADD-02"].ops]
    texts = {x.op.id: op_change(x, by["ADD-01"], by["ADD-02"]) for x in by["ADD-02"].ops}
    assert "SAR 3,000,000 -> SAR 2,000,000" in texts["ADD-02/1.1"] and "computed" in texts["ADD-02/1.1"]
    assert "relocated VOL-II:8.5 -> VOL-V:50.3" in texts["ADD-02/2.1"]
    assert "Table 50-1" in texts["ADD-02/4.1"]
    assert SCOPE in texts["ADD-02/5.1"]
    does = {x.op.id: _does(x.op) for x in by["ADD-02"].ops}
    assert does["ADD-02/2.1"].startswith("relocates") and does["ADD-02/1.1"].startswith("changes an amount")
    assert does["ADD-02/4.1"].startswith("inserts a table") and does["ADD-02/5.1"].startswith("disapplies")


def test_the_relocated_clause_is_amended_by_its_new_number_and_c47_reads_the_diff_against_its_source():
    p = U("ADD-02:2.3", "In Volume V Clause 50.3, ‘three (3) years’ is deleted and ‘two (2) years’ is substituted.")
    ops = [Op(id="ADD-02/2.1", provision="ADD-02:2.1", type="relocate_unit", target="VOL-II:8.5", to="VOL-V:50.3"),
           Op(id="ADD-02/2.3", provision="ADD-02:2.3", type="replace_text", target="VOL-V:50.3",
              old="three (3) years", new="two (2) years")]
    by, _ = run([P_RELOC, p], ops)
    assert all(x.applied for x in by["ADD-02"].ops), [failed(x) for x in by["ADD-02"].ops]
    st = by["ADD-02"].state
    assert "final two (2) years" in st["VOL-V:50.3"].text and st["VOL-V:50.3"].history == ["ADD-02/2.1", "ADD-02/2.3"]
    assert "three (3) years" in st["VOL-II:8.5"].text                       # the superseded unit keeps its words
    assert unevidenced_additions(by["ADD-01"].state, st, "ADD-02") == []


def test_derived_lists_conditional_impacts_and_computed_amounts_for_a_person():
    from tenderpack import derived
    ok = Op(id="ADD-02/1.1", provision="ADD-02:1.1", type="adjust_value", target="VOL-V:30.1",
            change="reduced by SAR 1,000,000")
    img = [U("ADD-02:T50-1", "Table 50-1", kind="table", page=2),
           U("ADD-02:T50-1/image/r1", "م: ١ | السنوات: ٢٠", kind="table_row", page=2, parent="ADD-02:T50-1",
             origin="image_reading", cells={"م": "١", "السنوات": "٢٠"},
             reading={"status": "pending", "region": "ADD-02-p2-r1", "subject_sha256": "abc"})]
    units = [P_REDUCE, P_TABLE] + img
    d = Disposition(provision="ADD-02:4.1", disposition="unresolved", reason="software limitation: not drafted")
    by, stages = run(units, [ok], dispositions=[d])
    r = {"stages": stages, "units": VOLUMES + ADD01 + [COVER2] + units}
    imps = derived.conditional_impacts(r, "ADD-02")
    kinds = {(i["conditional_on"]["kind"], i["conditional_on"]["ref"]) for i in imps}
    assert ("reading", "ADD-02-p2-r1") in kinds and ("disposition", "ADD-02:4.1") in kinds
    amts = derived.computed_amounts(r, "ADD-02")
    assert amts[0]["new_value"] == "SAR 2,000,000" and amts[0]["applied"]
    lines = "\n".join(derived.impact_lines({"conditional_impacts": imps, "computed_amounts": amts}))
    assert "CONDITIONAL; never accepted facts" in lines and "conditional on reading ADD-02-p2-r1" in lines
    assert "SAR 3,000,000 -> **SAR 2,000,000**" in lines and "never typed" in lines


def test_earlier_answers_on_a_moved_recomputed_or_incorporated_unit_are_re_read():
    from tenderpack.stage2 import changed_units_for_reread
    ops = [Op(id="ADD-02/1.1", provision="ADD-02:1.1", type="adjust_value", target="VOL-V:30.1",
              change="reduced by SAR 1,000,000"),
           Op(id="ADD-02/2.1", provision="ADD-02:2.1", type="relocate_unit", target="VOL-II:8.5", to="VOL-V:50.3"),
           Op(id="ADD-02/4.1", provision="ADD-02:4.1", type="insert_table", new_group="ADD-02:T50-1", into="VOL-V",
              number="50-1")]
    by, _ = run([P_REDUCE, P_RELOC, P_TABLE] + TABLE, ops)
    got = changed_units_for_reread(by["ADD-02"].ops)
    for k in ("VOL-V:30.1", "VOL-II:8.5", "VOL-V:50.3", "ADD-02:T50-1"):
        assert k in got, (k, sorted(got))
