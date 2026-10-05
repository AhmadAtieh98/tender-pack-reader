"""Session 12 (blind-05 follow-ups 2 and 5, the owner's part 2): one quotation, one op.

Ingest splits a clause into the clause unit and its list items (VOL-X:3.3, VOL-X:3.3(a), ...), in the volumes and in
the addendum alike. Blind-05 3.3 printed the replacement of VOL-V 29.2 as one quotation that ingest split into
ADD-03:3.3 and ADD-03:3.3(b): the op carrying the whole replacement failed C21 (the words of limb (b) are not in 3.3)
and the limb had to be escalated. And an obligation attached to a unit the same addendum inserts (7.3, 7.4 on the new
VOL-II 5.6) failed C22, because the inserted unit is named by the number it is inserted as, and cites nothing.

Fixed generally: the quoted words of an op may run on from its provision into the provision's own list items (they
are then content of the op, C20); a replace_text whose old words span a target clause and its list items is matched
across them in order, replaced, and re-split into the clause body and the items it now has (ids kept where the words
are unchanged, new ids for new items, removed items deleted); a quotation that breaks says where; a unit an earlier
op of the same addendum inserted is a target for later ops by the number it was inserted as; and two renderings issued
together carry the precedence the addendum states (`precedence`), or `unstated`, never one the engine decides."""
from __future__ import annotations

from pathlib import Path

from tenderpack.amend import Engine, OpFile, unevidenced_additions


def u(uid, kind, text, doc, **kw):
    return {"unit_id": uid, "doc": doc, "kind": kind, "text": text, "pages": [kw.pop("page", 1)], **kw}


OLD_292 = ("The Availability Payment shall be indexed annually in accordance with Schedule 9, with sixty per cent (60%) "
           "of the payment indexed to the published consumer price index and forty per cent (40%) remaining fixed.")
P33 = ("Volume V Clause 29.2 is deleted and replaced by the following: ‘29.2 The Availability Payment shall be indexed "
       "annually from the Base Date in accordance with Schedule 9. The proportion of the payment indexed (the Indexed "
       "Proportion) shall be: (a) until the end of the tenth (10th) year of operations, the percentage stated by the "
       "Bidder in Form 4-F, which shall be not less than fifty per cent (50%) and not more than seventy per cent (70%); and")
P33B = "(b) from the start of the eleventh (11th) year of operations, seventy-five per cent (75%). The balance of the payment shall remain fixed.’"
NEW_292 = ("The Availability Payment shall be indexed annually from the Base Date in accordance with Schedule 9. The "
           "proportion of the payment indexed (the Indexed Proportion) shall be: (a) until the end of the tenth (10th) "
           "year of operations, the percentage stated by the Bidder in Form 4-F, which shall be not less than fifty per "
           "cent (50%) and not more than seventy per cent (70%); and (b) from the start of the eleventh (11th) year of "
           "operations, seventy-five per cent (75%). The balance of the payment shall remain fixed.")

VOL = [u("VOL-V:H:29", "heading", "29. AVAILABILITY PAYMENT", "VOL-V"),
       u("VOL-V:29.1", "clause", "From PCOD the Authority shall pay the Availability Payment.", "VOL-V"),
       u("VOL-V:29.2", "clause", OLD_292, "VOL-V", page=3),
       u("VOL-I:9.1", "clause", "Envelope A shall contain, in the following order:", "VOL-I"),
       u("VOL-I:9.1(a)", "list_item", "(a) Form 4-A — Proposal Submission Letter;", "VOL-I", parent="VOL-I:9.1"),
       u("VOL-I:9.1(b)", "list_item", "(b) Form 4-B — Reference Projects Schedule;", "VOL-I", parent="VOL-I:9.1"),
       u("VOL-I:9.1(c)", "list_item", "(c) the Technical Proposal narrative.", "VOL-I", parent="VOL-I:9.1"),
       u("VOL-II:5.5", "clause", "The Project Company shall keep the site secure.", "VOL-II")]


def _run(add_units, ops, dispositions=()):
    units = VOL + [u("ADD-03:cover/para1", "paragraph", "Issued 15 November 2026", "ADD-03")] + add_units
    f = OpFile.model_validate({"addendum": "ADD-03", "issued_from": "ADD-03:cover/para1", "prepared_by": "test",
                               "method": "test", "ops": ops,
                               "dispositions": [{"provision": "ADD-03:cover/para1", "disposition": "no_effect",
                                                 "reason": "issue date"}] + list(dispositions)})
    stages = Engine(units, [f]).run()
    return stages, stages[-1]


def _failed(r):
    return [f"{c['id']} {c['detail']}" for c in r.checks if not c["ok"]]


# ------------------------------------------------------------------------------- the provision split (blind-05 3.3)

def test_a_replacement_quoted_across_the_provision_and_its_list_item_is_one_op():
    add = [u("ADD-03:3.3", "clause", P33, "ADD-03"),
           u("ADD-03:3.3(b)", "list_item", P33B, "ADD-03", parent="ADD-03:3.3")]
    stages, s = _run(add, [{"id": "ADD-03/3.3", "provision": "ADD-03:3.3", "type": "replace_text",
                            "target": "VOL-V:29.2", "old": OLD_292, "old_resolved": "matched_in_target",
                            "new": NEW_292}])
    r = s.ops[0]
    assert r.valid, _failed(r)
    assert s.state["VOL-V:29.2"].text == NEW_292
    assert "ADD-03:3.3(b)" in r.details["content"]                      # the list item is content of the op (C20)
    cov = {c["provision"]: c["disposition"] for c in s.coverage}
    assert cov["ADD-03:3.3"] == "op" and cov["ADD-03:3.3(b)"] == "op"
    assert s.status == "APPLIED", (s.problems, s.scope_leak, s.coverage)
    assert unevidenced_additions(stages[-2].state, s.state, "ADD-03") == []   # C47: every new word is printed


def test_words_not_printed_in_the_provision_or_its_items_still_fail_c21():
    add = [u("ADD-03:3.3", "clause", P33, "ADD-03"),
           u("ADD-03:3.3(b)", "list_item", P33B, "ADD-03", parent="ADD-03:3.3")]
    _, s = _run(add, [{"id": "ADD-03/3.3", "provision": "ADD-03:3.3", "type": "replace_text", "target": "VOL-V:29.2",
                       "old": OLD_292, "old_resolved": "matched_in_target", "new": NEW_292 + " Words nobody printed."}])
    assert not s.ops[0].valid and any(c["id"] == "C21" and not c["ok"] for c in s.ops[0].checks)


# ------------------------------------------------------------------------------- the target split (clause + items)

P71 = ("In Volume I Clause 9.1, ‘Envelope A shall contain, in the following order: (a) Form 4-A — Proposal "
       "Submission Letter; (b) Form 4-B — Reference Projects Schedule;’ is deleted and ‘Envelope A shall "
       "contain, in the following order: (a) Form 4-A — Proposal Submission Letter; (b) Form 4-B — Reference "
       "Projects Schedule (one per project); (c) Form 4-G — Cybersecurity Undertaking;’ is substituted.")
OLD71 = ("Envelope A shall contain, in the following order: (a) Form 4-A — Proposal Submission Letter; (b) Form 4-B "
         "— Reference Projects Schedule;")
NEW71 = ("Envelope A shall contain, in the following order: (a) Form 4-A — Proposal Submission Letter; (b) Form 4-B "
         "— Reference Projects Schedule (one per project); (c) Form 4-G — Cybersecurity Undertaking;")


def test_old_words_spanning_a_clause_and_its_items_are_replaced_and_re_split():
    _, s = _run([u("ADD-03:7.1", "clause", P71, "ADD-03")],
                [{"id": "ADD-03/7.1", "provision": "ADD-03:7.1", "type": "replace_text", "target": "VOL-I:9.1",
                  "old": OLD71, "new": NEW71}])
    r = s.ops[0]
    assert r.valid, _failed(r)
    st = s.state
    assert st["VOL-I:9.1"].text == "Envelope A shall contain, in the following order:"
    assert st["VOL-I:9.1(a)"].text == "(a) Form 4-A — Proposal Submission Letter;"   # unchanged words, same id
    assert "ADD-03/7.1" not in st["VOL-I:9.1(a)"].history
    assert st["VOL-I:9.1(b)"].text == "(b) Form 4-B — Reference Projects Schedule (one per project);"
    assert "ADD-03/7.1" in st["VOL-I:9.1(b)"].history                     # changed in place: same id, marked
    # the old (c) keeps its words and its id; the new item (c) gets a new id, printed in the addendum; the addendum did
    # not re-letter the old (c), so two items are now lettered (c): said, never corrected
    assert st["VOL-I:9.1(c)"].text == "(c) the Technical Proposal narrative." and st["VOL-I:9.1(c)"].status == "active"
    assert "ADD-03/7.1" not in st["VOL-I:9.1(c)"].history
    new = [k for k in st if k.startswith("VOL-I:9.1(") and k not in ("VOL-I:9.1(a)", "VOL-I:9.1(b)", "VOL-I:9.1(c)")]
    assert len(new) == 1 and st[new[0]].text == "(c) Form 4-G \u2014 Cybersecurity Undertaking;"
    assert st[new[0]].parent == "VOL-I:9.1" and st[new[0]].kind == "list_item"
    assert st[new[0]].printed_in == "ADD-03" and st[new[0]].pages == [1]
    assert set(r.changed) == {"VOL-I:9.1", "VOL-I:9.1(b)", new[0]}
    assert "(c)" in r.details["lettering"]
    assert list(r.details["span"]["after"]) == ["VOL-I:9.1", "VOL-I:9.1(a)", "VOL-I:9.1(b)", new[0], "VOL-I:9.1(c)"]
    assert s.status == "APPLIED", (s.problems, s.scope_leak)


def test_a_span_replacement_with_fewer_items_deletes_the_items_it_no_longer_has():
    p = ("In Volume I Clause 9.1, ‘(b) Form 4-B — Reference Projects Schedule; (c) the Technical Proposal "
         "narrative.’ is deleted and ‘(b) the Technical Proposal narrative.’ is substituted.")
    _, s = _run([u("ADD-03:7.1", "clause", p, "ADD-03")],
                [{"id": "ADD-03/7.1", "provision": "ADD-03:7.1", "type": "replace_text", "target": "VOL-I:9.1",
                  "old": "(b) Form 4-B — Reference Projects Schedule; (c) the Technical Proposal narrative.",
                  "new": "(b) the Technical Proposal narrative."}])
    r = s.ops[0]
    assert r.valid, _failed(r)
    st = s.state
    kept = [k for k in ("VOL-I:9.1(b)", "VOL-I:9.1(c)") if st[k].status == "active"]
    assert len(kept) == 1 and st[kept[0]].text == "(b) the Technical Proposal narrative."
    gone = [k for k in ("VOL-I:9.1(b)", "VOL-I:9.1(c)") if k not in kept][0]
    assert st[gone].status == "deleted" and "ADD-03/7.1" in st[gone].history


def test_a_quotation_that_breaks_says_where():
    p = ("In Volume I Clause 9.1, ‘Envelope A shall contain, in the following order: (a) Form 4-A — Proposal "
         "Submission Letter; (b) Form 4-Z — Something Else;’ is deleted and ‘Envelope A’ is substituted.")
    _, s = _run([u("ADD-03:7.1", "clause", p, "ADD-03")],
                [{"id": "ADD-03/7.1", "provision": "ADD-03:7.1", "type": "replace_text", "target": "VOL-I:9.1",
                  "old": "Envelope A shall contain, in the following order: (a) Form 4-A — Proposal Submission "
                         "Letter; (b) Form 4-Z — Something Else;", "new": "Envelope A"}])
    r = s.ops[0]
    assert not r.valid
    why = " ".join(_failed(r))
    assert "VOL-I:9.1(a)" in why and "VOL-I:9.1(b)" in why and "breaks" in why


# ------------------------------------------------------------------------------- a unit the same addendum inserts

P71N = ("The following new Clause 5.6 is inserted in Volume II after Clause 5.5: ‘5.6 The Project Company shall "
        "comply with the height limits in Table 5-1.’")
P73 = ("A Bidder whose Proposal provides for any structure exceeding thirty (30) metres in height shall notify the "
       "Authority of the zone of Table 5-1 in which it is to be located.")


def test_a_later_op_of_the_same_addendum_targets_the_inserted_unit_by_its_number():
    ins = {"id": "ADD-03/7.1", "provision": "ADD-03:7.1", "type": "insert_unit", "anchor": "VOL-II:5.5",
           "new_text": "The Project Company shall comply with the height limits in Table 5-1."}
    obl = {"id": "ADD-03/7.3", "provision": "ADD-03:7.3", "type": "annotate", "targets": ["VOL-II:5.6"],
           "effect": "adds_obligation"}
    _, s = _run([u("ADD-03:7.1", "clause", P71N, "ADD-03"), u("ADD-03:7.3", "clause", P73, "ADD-03", page=3)],
                [ins, obl])
    r1, r3 = s.ops
    assert r1.valid, _failed(r1)
    assert r3.valid, _failed(r3)
    assert r3.details.get("resolved_targets") == {"VOL-II:5.6": "VOL-II:5.5+ADD-03"}
    assert "ADD-03/7.3" in s.state["VOL-II:5.5+ADD-03"].annotations
    assert s.status == "APPLIED", (s.problems, s.coverage)


# ------------------------------------------------------------------------------- two renderings issued together

P72 = ("Table 5-1 is issued in the Arabic language. The Arabic text governs. The English translation at Appendix B "
       "is provided for convenience only.")


def _renderings(prec, text=P72):
    add = [u("ADD-03:7.2", "clause", text, "ADD-03"),
           u("ADD-03:AppA/T5-1", "table", "المنطقة | الارتفاع", "ADD-03", page=4),
           u("ADD-03:AppB/T5-1", "table", "Zone | Maximum height", "ADD-03", page=5)]
    op = {"id": "ADD-03/7.2", "provision": "ADD-03:7.2", "type": "annotate", "effect": "interprets",
          "targets": ["ADD-03:AppA/T5-1", "ADD-03:AppB/T5-1"], "precedence": prec}
    return _run(add, [op])[1]


def test_the_precedence_the_addendum_states_is_recorded_with_its_words():
    s = _renderings({"governs": "ADD-03:AppA/T5-1", "over": ["ADD-03:AppB/T5-1"], "words": "The Arabic text governs."})
    r = s.ops[0]
    assert r.valid, _failed(r)
    assert r.details["precedence"] == {"governs": "ADD-03:AppA/T5-1", "over": ["ADD-03:AppB/T5-1"],
                                       "words": "The Arabic text governs.", "stated_by": "ADD-03:7.2"}


def test_a_precedence_the_addendum_does_not_print_is_refused():
    s = _renderings({"governs": "ADD-03:AppB/T5-1", "over": ["ADD-03:AppA/T5-1"], "words": "The English text governs."})
    assert not s.ops[0].valid and any(c["id"] == "C21" and not c["ok"] for c in s.ops[0].checks)


def test_a_precedence_mapped_to_the_wrong_rendering_is_refused():
    s = _renderings({"governs": "ADD-03:AppB/T5-1", "over": ["ADD-03:AppA/T5-1"], "words": "The Arabic text governs."})
    assert not s.ops[0].valid and any(c["id"] == "C22" and "Arabic" in c["detail"] and not c["ok"] for c in s.ops[0].checks)


def test_unstated_precedence_is_carried_and_flagged_for_a_person():
    s = _renderings("unstated", text="Table 5-1 is issued in Arabic, with an English translation at Appendix B.")
    r = s.ops[0]
    assert r.valid, _failed(r)
    assert r.details["precedence"]["governs"] == "unstated"
    assert "a person" in r.details["precedence"]["flag"]


def _row_flags(prec, row_unit, text=P72):
    from tenderpack.dates import Calendar
    from tenderpack.register import Register, RowFile
    add = [u("ADD-03:7.2", "clause", text, "ADD-03"),
           u("ADD-03:AppA/T5-1", "table", "\u0627\u0644\u0645\u0646\u0637\u0642\u0629", "ADD-03", page=4),
           u("ADD-03:AppB/T5-1", "table", "Zone | Maximum height", "ADD-03", page=5)]
    op = {"id": "ADD-03/7.2", "provision": "ADD-03:7.2", "type": "annotate", "effect": "interprets",
          "targets": ["ADD-03:AppA/T5-1", "ADD-03:AppB/T5-1"], "precedence": prec}
    stages, s = _run(add, [op])
    quote = "Zone | Maximum height" if row_unit.endswith("AppB/T5-1") else "\u0627\u0644\u0645\u0646\u0637\u0642\u0629"
    rf = RowFile.model_validate({"prepared_by": "test", "method": "test", "anchors": {}, "rows": [
        {"id": "ADD-03-7.1-01", "group": "ADD-03:7.1", "scope": ["heights"], "requirement": "height limits",
         "units": [row_unit], "discipline": "Technical", "assessment": "contractual_post_award",
         "interpretations": [{"stage": "ADD-03", "quote": quote}], "confidence": "low", "confidence_reason": "test"}]})
    return Register(rf, stages, Calendar()).evaluate(rf.rows[0], s)["flags"]


def test_a_row_on_renderings_with_unstated_precedence_is_flagged_for_a_person():
    flags = _row_flags("unstated", "ADD-03:AppB/T5-1",
                       text="Table 5-1 is issued in Arabic, with an English translation at Appendix B.")
    assert any("precedence unstated" in f and "a person decides" in f for f in flags), flags


def test_a_row_on_the_non_governing_rendering_says_so_and_one_on_the_governing_one_does_not():
    prec = {"governs": "ADD-03:AppA/T5-1", "over": ["ADD-03:AppB/T5-1"], "words": "The Arabic text governs."}
    assert any("does not govern" in f and "The Arabic text governs." in f for f in _row_flags(prec, "ADD-03:AppB/T5-1"))
    assert not any("govern" in f for f in _row_flags(prec, "ADD-03:AppA/T5-1"))


# ------------------------------------------------------------------------------- the quote check (follow-up 13)

def test_the_quote_check_accepts_the_inserting_provisions_page_for_an_inserted_unit():
    """Blind-05 check-register's one finding: ADD-03-7.1-01's post-award basis quoted VOL-II:5.5+ADD-03 (the new 5.6)
    at page 2, the page of the provision that inserts it; the check looked only among the evidence build's units."""
    from tenderpack.stage2 import basis_found
    ins = {"id": "ADD-03/7.1", "provision": "ADD-03:7.1", "type": "insert_unit", "anchor": "VOL-II:5.5",
           "new_text": "The Project Company shall comply with the height limits in Table 5-1."}
    stages, s = _run([u("ADD-03:7.1", "clause", P71N, "ADD-03", page=2)], [ins])
    units = {x["unit_id"]: x for x in VOL}
    ok = {"unit": "VOL-II:5.5+ADD-03", "page": 2, "words": "The Project Company shall comply with the height limits"}
    assert basis_found(ok, units, s.state)
    assert not basis_found(dict(ok, page=3), units, s.state)                         # another page: still a finding
    assert not basis_found(dict(ok, words="shall comply with Table 9-9"), units, s.state)
    assert basis_found({"unit": "VOL-II:5.5", "page": 1, "words": "keep the site secure"}, units, s.state)


# ------------------------------------------------------------------------------- blind-05 regression (post-key)

def test_blind05_provisions_the_run_could_not_carry_are_now_valid_ops():
    """Labelled post-key regression: blind-05's ADD-03 provisions (the frozen analysis packets) on the pack's units and
    curated ADD-01/ADD-02 op files, with the frozen candidate's promoted ADD-03 ops and the ops the run had to escalate
    (6.7 deleted, 3.3's replacement quoted across 3.3 and 3.3(b), 7.3 and 7.4 on the new 5.6, 7.2's precedence). Each is
    valid through the engine and C47 finds no unprinted word. The ops are the addendum's own words, not answers keyed."""
    import glob
    import json
    import re

    import yaml

    from tenderpack.amend import load_opfile
    from tenderpack.util import ROOT
    b05 = ROOT / "rehearsals/blind-05"
    units = json.loads((ROOT / "build/units.json").read_text())["units"]
    add = []
    for f in sorted(glob.glob(str(b05 / "batches/analysis-*.packet.json"))):
        for p in json.loads(Path(f).read_text())["provisions"]:
            x = {"unit_id": p["unit_id"], "doc": "ADD-03", "kind": p["kind"], "text": p["text"], "pages": p["pages"]}
            if p["kind"] == "list_item":
                x["parent"] = p["unit_id"].rsplit("(", 1)[0]
            add.append(x)
    txt = {x["unit_id"]: x["text"] for x in add}
    vol = {x["unit_id"]: x.get("text", "") for x in units}
    new292 = re.sub(r"^29\.2\s+", "", (txt["ADD-03:3.3"] + " " + txt["ADD-03:3.3(b)"]).split("‘", 1)[1].rsplit("’", 1)[0])
    more = [{"id": "ADD-03/2.1-del", "provision": "ADD-03:2.1", "type": "set_status", "target": "VOL-I:6.7", "status": "deleted"},
            {"id": "ADD-03/3.3", "provision": "ADD-03:3.3", "type": "replace_text", "target": "VOL-V:29.2",
             "old": vol["VOL-V:29.2"], "old_resolved": "matched_in_target", "new": new292},
            {"id": "ADD-03/7.3", "provision": "ADD-03:7.3", "type": "annotate", "targets": ["VOL-II:5.6"], "effect": "adds_obligation"},
            {"id": "ADD-03/7.4", "provision": "ADD-03:7.4", "type": "annotate", "targets": ["VOL-II:5.6"], "effect": "adds_obligation"},
            {"id": "ADD-03/7.2", "provision": "ADD-03:7.2", "type": "annotate", "effect": "interprets",
             "targets": ["ADD-03:p4-image", "ADD-03:T5-1"],
             "precedence": {"governs": "ADD-03:p4-image", "over": ["ADD-03:T5-1"], "words": "The Arabic text governs."}}]
    frozen = yaml.safe_load((b05 / "candidate-curation/amendments/ADD-03.yaml").read_text())["ops"]
    of3 = OpFile.model_validate({"addendum": "ADD-03", "issued_from": "ADD-03:cover/para1", "prepared_by": "test",
                                 "method": "test", "ops": frozen + more, "dispositions": []})
    stages = Engine(units + add, [load_opfile(ROOT / f"curation/amendments/ADD-0{n}.yaml") for n in (1, 2)] + [of3]).run()
    s = stages[-1]
    res = {r.op.id: r for r in s.ops}
    for o in more:
        assert res[o["id"]].valid, (o["id"], _failed(res[o["id"]]))
    assert all(r.valid for r in s.ops), [(r.op.id, _failed(r)) for r in s.ops if not r.valid]
    assert res["ADD-03/3.3"].details["quoted_across"] == ["ADD-03:3.3", "ADD-03:3.3(b)"]
    assert s.state["VOL-V:29.2"].text.endswith("seventy-five per cent (75%). The balance of the payment shall remain fixed.")
    assert s.state["VOL-I:6.7"].status == "deleted"
    assert res["ADD-03/7.4"].details["resolved_targets"] == {"VOL-II:5.6": "VOL-II:5.5+ADD-03"}
    assert unevidenced_additions(stages[-2].state, s.state, "ADD-03") == []
