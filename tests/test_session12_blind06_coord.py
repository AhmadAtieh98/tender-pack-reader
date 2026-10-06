"""Session 12, the coordinator's fixes for the blind-06 scorer's smaller workflow defects (rehearsals/blind-06/
COMPARISON.md, "Follow-ups"); failing first on the tree of eaea64d, then the general rule. The larger items are F6's."""
from __future__ import annotations

from tenderpack import clarify
from tenderpack.amend import UState


def _unit(uid: str, text: str, doc: str = "VOL-I", status: str = "active", pages=(3,)) -> UState:
    return UState(unit_id=uid, doc=doc, kind="paragraph", status=status, text=text, cells=None, pages=list(pages),
                  origin="text_layer", reading_status=None)


def _entry(words: str) -> dict:
    return {"id": "CQ-TEST", "topic": "t", "question": "q?", "why_it_matters": "w", "decision_owner": "Legal",
            "response_status": "draft, not sent", "sources": [{"unit": "VOL-I:6.1", "page": 3, "words": words}],
            "linked_issues": []}


PRINTED = "The Proposal shall be delivered by 12:00 on the Proposal Due Date."
AMENDED = "The Proposal shall be delivered by 14:00 on the Proposal Due Date."
UNITS = [{"unit_id": "VOL-I:6.1", "doc": "VOL-I", "kind": "paragraph", "text": PRINTED, "pages": [3]}]


def test_a_quotation_of_the_words_as_amended_passes_with_the_working_state_and_fails_without_it():
    """Follow-up 2: clarify.check compared a draft's quoted words with the printed unit only, so every question that
    quotes amended text failed (3 of 3 on blind-06). With the working stage's state the words as amended are verbatim."""
    state = {"VOL-I:6.1": _unit("VOL-I:6.1", AMENDED)}
    reg = {"clarifications": [_entry("delivered by 14:00")]}
    assert not [f for f in clarify.check(reg, UNITS, set(), state=state) if "not verbatim" in f]
    without = [f for f in clarify.check(reg, UNITS, set()) if "not verbatim" in f]     # the printed text alone
    assert without and "delivered by 14:00" in without[0]


def test_printed_words_still_pass_and_words_in_neither_text_name_both():
    state = {"VOL-I:6.1": _unit("VOL-I:6.1", AMENDED)}
    assert not [f for f in clarify.check({"clarifications": [_entry("delivered by 12:00")]}, UNITS, set(), state=state)
                if "not verbatim" in f]                                                   # as printed: still verbatim
    bad = [f for f in clarify.check({"clarifications": [_entry("delivered by 16:00")]}, UNITS, set(), state=state)
           if "not verbatim" in f]
    assert bad and "neither as printed nor as amended" in bad[0]


def test_a_superseded_unit_is_followed_to_its_replacement_and_a_deleted_one_gives_no_amended_text():
    state = {"VOL-I:6.1": _unit("VOL-I:6.1", PRINTED, status="superseded"),
             "VOL-I:6.1+ADD-03": _unit("VOL-I:6.1+ADD-03", AMENDED, doc="ADD-03")}
    state["VOL-I:6.1"].superseded_by = "VOL-I:6.1+ADD-03"
    assert not [f for f in clarify.check({"clarifications": [_entry("delivered by 14:00")]}, UNITS, set(), state=state)
                if "not verbatim" in f]
    gone = {"VOL-I:6.1": _unit("VOL-I:6.1", AMENDED, status="deleted")}
    bad = [f for f in clarify.check({"clarifications": [_entry("delivered by 14:00")]}, UNITS, set(), state=gone)
           if "not verbatim" in f]
    assert bad and "neither" not in bad[0]        # no active amended text to compare with: the plain finding


def test_a_cover_annotation_never_brings_the_cover_paragraphs_consequence_words_under_c46():
    """Follow-up 8: an `adds_obligation` annotate on a cover paragraph brought the whole paragraph's words under C46,
    so the cover's phantom "deduction" made check-register exit 1 on blind-06. The provision's words count only for an
    operative clause; for a cover paragraph the annotation's own note states the obligation."""
    from types import SimpleNamespace as NS
    from tenderpack.trace import provision_consequence_words as pcw
    cover = _unit("ADD-03:cover/para3", "This Addendum incorporates a deduction regime and requires Form 4-A to be "
                                        "re-submitted; a Proposal without it shall be rejected.", doc="ADD-03")
    op_cover = NS(type="annotate", provision="ADD-03:cover/para3", effect="adds_obligation", targets=["VOL-IV:F4A"],
                  note="Form 4-A re-submitted, failing which the Proposal shall be rejected")
    assert pcw(op_cover, cover) == {"rejected"}                 # the note's words, not the paragraph's "deduction"
    op_cover_no_note = NS(type="annotate", provision="ADD-03:cover/para3", effect="adds_obligation", targets=["VOL-IV:F4A"], note=None)
    assert pcw(op_cover_no_note, cover) == set()
    clause = _unit("ADD-03:5.2", "Late delivery shall incur a deduction and the Proposal shall be rejected.", doc="ADD-03")
    op_clause = NS(type="annotate", provision="ADD-03:5.2", effect="adds_obligation", targets=["VOL-I:6.1"], note=None)
    assert pcw(op_clause, clause) == {"deduction", "rejected"}  # an operative clause: its own words
    op_insert = NS(type="insert_unit", provision="ADD-03:5.3", effect=None, targets=[], note=None)
    assert pcw(op_insert, clause) == {"deduction", "rejected"}
    assert pcw(NS(type="replace_text", provision="ADD-03:5.4", effect=None, targets=[], note=None), clause) == set()


def test_an_introduces_claim_is_supported_by_an_amendment_that_only_adds_words_to_the_target():
    """Follow-up 7: C28 called "introduces a flow range for the reliability run in Clause 7.2" contradicted because the
    provision does it by amending 7.2 (class "change"), which the "add" kind did not allow. An amendment whose new words
    contain every old word and more adds to the clause; one that removes or rewrites words does not fit "adds"."""
    from types import SimpleNamespace as NS
    from tenderpack.summary import claim_fits
    adds = NS(type="replace_text", target="VOL-II:7.2", old="The reliability run shall last 30 days.",
              new="The reliability run shall last 30 days at a flow between 80 % and 110 % of the design flow.")
    rewrites = NS(type="replace_text", target="VOL-II:7.2", old="The reliability run shall last 30 days.",
                  new="The reliability run shall last 45 days.")
    deletes = NS(type="replace_text", target="VOL-II:7.2", old="at a flow between 80 % and 110 %", new="")
    assert claim_fits("add", "change", adds)
    assert not claim_fits("add", "change", rewrites) and not claim_fits("add", "delete", deletes)
    assert claim_fits("change", "change", rewrites) and claim_fits("add", "add", NS(type="insert_unit", old=None, new=None))
    assert not claim_fits("delete", "change", adds)                      # the other kinds follow ALLOWS unchanged


def test_a_provision_with_a_promoted_item_and_an_escalated_sibling_is_partly_answered_not_answered():
    """Follow-up 1: a provision counted as answered when one sub-item was promoted and a sibling escalated, so the
    escalation dropped off the unresolved list, the packet's first section and A4 (the DA1 case on blind-06)."""
    from tenderpack.ai.downstream import partly_answered
    from tenderpack.ai.workflow import answer_state
    assert answer_state(["ADD-03/2.1"], []) == {"answered": True}
    st = answer_state(["ADD-03/2.1"], ["which of the two readings of 2.1(b) applies is for Legal"])
    assert st["answered"] is False and st["partly"] is True
    assert st["why"] == "partly answered by ADD-03/2.1; escalated: which of the two readings of 2.1(b) applies is for Legal"
    assert partly_answered(st["why"]) and not partly_answered("no promotable item answers it") and not partly_answered(None)
    assert answer_state([], ["x"])["why"] == "partly answered; escalated: x"


def test_an_inserted_unit_and_its_anchor_count_as_changed_for_the_re_read_of_earlier_answers():
    """Follow-up 11: the re-read list started only from replaced, set, deleted, renumbered, appended or annotated units,
    so a NEW event inserted as 31.1(d) never reached an earlier answer on 29.x through the relationship that joins
    them. An inserted unit, its anchor and its new group now start the trace too."""
    from types import SimpleNamespace as NS
    from tenderpack.stage2 import changed_units_for_reread
    ins = NS(applied=True, changed=["VOL-V:31.1(d)"], op=NS(type="insert_unit", target=None, anchor="VOL-V:31.1(c)",
                                                            new_group="VOL-V:31.1", effect=None, targets=[], renumber=[]))
    rep = NS(applied=True, changed=["VOL-II:7.2"], op=NS(type="replace_text", target="VOL-II:7.2", anchor=None,
                                                          new_group=None, effect=None, targets=[], renumber=[]))
    conf = NS(applied=True, changed=[], op=NS(type="annotate", target=None, anchor=None, new_group=None,
                                              effect="confirms", targets=["VOL-II:3.3"], renumber=[]))
    skipped = NS(applied=False, changed=["VOL-I:1.1"], op=NS(type="replace_text", target="VOL-I:1.1", anchor=None,
                                                             new_group=None, effect=None, targets=[], renumber=[]))
    got = changed_units_for_reread([ins, rep, conf, skipped], {"VOL-I:9.9": rep})
    assert set(got) == {"VOL-V:31.1(d)", "VOL-V:31.1(c)", "VOL-V:31.1", "VOL-II:7.2", "VOL-I:9.9"}
    assert got["VOL-V:31.1"] is ins and got["VOL-II:7.2"] is rep        # a confirming annotation changes nothing


def test_replace_requirement_has_a_typed_shape_and_the_validator_names_the_missing_field():
    """Follow-up 3: the payload was untyped in the packet schema while the validator needed `old` and `new`, so all
    three such row readings failed on blind-06 and the amended rows stayed STALE."""
    import pytest
    from pydantic import ValidationError
    from tenderpack.ai.contract import ReplaceRequirement, RowReadingPayload
    from tenderpack.ai.downstream import replace_requirement_problem
    schema = RowReadingPayload.model_json_schema()
    assert "ReplaceRequirement" in schema.get("$defs", {}) and set(schema["$defs"]["ReplaceRequirement"]["required"]) == {"old", "new"}
    ok = RowReadingPayload(row="VOL-II-7.2-01", interpretation={"stage": "ADD-03"},
                           replace_requirement={"old": "run for 30 days", "new": "run for 30 days at 80-110 % flow"})
    assert isinstance(ok.replace_requirement, ReplaceRequirement)
    with pytest.raises(ValidationError, match="new"):
        RowReadingPayload(row="r", interpretation={}, replace_requirement={"old": "x"})
    assert replace_requirement_problem(None, "a") is None
    assert replace_requirement_problem({"old": "a", "new": "b"}, "a") is None
    assert "missing or empty: new" in replace_requirement_problem({"old": "a", "new": " "}, "a")
    assert "missing or empty: old, new" in replace_requirement_problem({}, "a")
    p = replace_requirement_problem({"old": "wrong", "new": "b"}, "the row's words")
    assert "not the row's current requirement" in p and "wrong" in p and "the row's words" in p


def test_an_image_region_whose_blocks_are_provisions_is_an_acceptable_cited_unit():
    """Follow-up 4: `reading_rows` proposals cited the image region's parent ("ADD-03:p4-image") and were refused as
    "not a provision" although its blocks are provisions (7 of 7 invalid on blind-06)."""
    from tenderpack.ai.controller import region_parents
    units = [{"unit_id": "ADD-03:p4-image", "kind": "figure"},
             {"unit_id": "ADD-03:p4-image/1", "kind": "paragraph", "parent": "ADD-03:p4-image"},
             {"unit_id": "ADD-03:p4-image/2", "kind": "table_row", "parent": "ADD-03:p4-image"},
             {"unit_id": "ADD-03:cover/para1", "kind": "paragraph", "parent": "ADD-03:cover"},
             {"unit_id": "ADD-03:3.1", "kind": "paragraph"}]
    provisions = ["ADD-03:p4-image/1", "ADD-03:p4-image/2", "ADD-03:3.1"]
    assert region_parents(units, provisions) == {"ADD-03:p4-image"}      # the cover's parent: no provision under it
    assert region_parents(units, ["ADD-03:3.1"]) == set()


def test_opposite_treatments_of_one_unit_across_a_set_are_conflicts_for_both_items():
    """Follow-up 6 (a): the same Table 1-3 cells were unresolved in one batch and settled as no effect in two others;
    nothing checked the combined set for that. A no_effect disposition on a provision whose unit another item's op
    changes, or two ops setting one target differently, now mark both items conflicting with the reason."""
    from types import SimpleNamespace as NS
    from tenderpack.ai.controller import cross_item_conflicts
    rep = NS(id="ADD-03/4.1", type="replace_text", provision="ADD-03:4.1", target="VOL-II:T1-3/n2", targets=[], old="a", new="b", status=None, effect=None)
    ne = NS(provision="ADD-03:4.1", disposition="no_effect")
    other = NS(provision="ADD-03:9.9", disposition="no_effect")
    conf = NS(id="ADD-03/Q3", type="annotate", provision="ADD-03:Q3", target=None, targets=["VOL-II:T1-3/n2"], old=None, new=None, status=None, effect="confirms")
    got = cross_item_conflicts([(0, rep), (3, conf)], [(1, ne), (2, other)])
    assert set(got) == {0, 1} and "no_effect" in got[0] and got[0] == got[1]      # the confirming annotation is no conflict
    a = NS(id="ADD-03/2.1", type="replace_text", provision="ADD-03:2.1", target="VOL-I:6.6", targets=[], old="x", new="y", status=None, effect=None)
    b = NS(id="ADD-03/2.2", type="replace_text", provision="ADD-03:2.2", target="VOL-I:6.6", targets=[], old="x", new="z", status=None, effect=None)
    got2 = cross_item_conflicts([(0, a), (1, b)], [])
    assert set(got2) == {0, 1} and "different ways" in got2[0]
    same = NS(id="ADD-03/2.3", type="replace_text", provision="ADD-03:2.3", target="VOL-I:6.6", targets=[], old="x", new="y", status=None, effect=None)
    assert cross_item_conflicts([(0, a), (1, same)], []) == {}                     # the same change twice: not a conflict
    assert cross_item_conflicts([(0, a)], [(1, other)]) == {}                       # different units: nothing


def test_a_no_effect_on_an_obligation_no_row_carries_is_a_decision_for_a_person():
    """Follow-up 6 (c): two promoted no_effect dispositions settled Table 1-3 notes (one shutdown per tie-in point;
    portal requests) whose obligations reached no row because a check had rejected the rows; nothing said so."""
    from types import SimpleNamespace as NS
    from tenderpack.ai.controller import obligation_without_row
    rows = [NS(id="VOL-I-6.3-01", units=["VOL-I:6.3"]), NS(id="VOL-II-7.2-01", units=["VOL-II:7.2", "VOL-II:T1-3/n1"])]
    note = "Note 2: The Bidder shall allow one shutdown per tie-in point and shall request each through the Portal."
    gap = obligation_without_row(note, "repeats the general rule; no register effect", rows)
    assert gap and "no row carries" in gap and "shall" in gap
    assert obligation_without_row(note, "already carried by row VOL-I-6.3-01", rows) is None
    assert obligation_without_row(note, "restates VOL-II:7.2, which the register holds", rows) is None
    assert obligation_without_row("Note 3: For information only.", "nothing to carry", rows) is None


def test_an_answer_that_restates_an_exclusion_the_clause_already_makes_confirms_it():
    """Follow-up 10: the semantic check read a confirming answer as "adds" because its first sentence excluded a
    method in other words than the clause ("shall not be used as the sole means" for "alone is not acceptable"):
    an exclusion the targets already state confirms; one they never state still adds."""
    from tenderpack.summary import classify_answer
    clause = ("Treatment shall be by membrane filtration with a validated pore size, or by sand filtration with "
              "coagulation, or by a combination. Lagooning alone is not acceptable.")
    answer = ("Bidder question: May lagooning be used as the treatment process? | Authority response: Lagooning shall "
              "not be used as the sole means of treatment. Treatment shall be by membrane filtration with a validated "
              "pore size, or by sand filtration with coagulation, or by a combination. Volume II Clause 3.3 applies.")
    c = classify_answer(answer, {"VOL-II:3.3": clause})
    assert c["class"] == "confirms", c
    assert [x["kind"] for x in c["sentences"]] == ["confirms", "confirms", "none"] or \
        [x["kind"] for x in c["sentences"]][:2] == ["confirms", "confirms"]
    adds = ("Authority response: Chlorination shall not be used as the sole means of treatment. Treatment shall be by "
            "membrane filtration with a validated pore size, or by sand filtration with coagulation, or by a combination.")
    assert classify_answer(adds, {"VOL-II:3.3": clause})["class"] == "adds"      # an exclusion the clause never makes


def test_the_analysis_instructions_give_free_standing_provisions_a_row_path():
    """Follow-up 13: free-standing addendum provisions (2.4-2.7, 3.2(a) on blind-06) were escalated "for want of a
    cited unit" although the register holds rows on addendum units (ADD-02-5.2-01): the packet's instructions now say
    so, and a row_new on an addendum unit is a well-formed payload."""
    from tenderpack.ai.controller import INSTRUCTIONS
    from tenderpack.ai.contract import RowNewPayload
    rule = [x for x in INSTRUCTIONS if "free-standing provision" in x]
    assert len(rule) == 1 and "row_new" in rule[0] and "own unit id" in rule[0] and "never escalated" in rule[0]
    row = {"id": "ADD-03-2.4-01", "group": "Submission", "scope": "all", "requirement": "The Bidder shall submit X.",
           "units": ["ADD-03:2.4"], "discipline": "Bid management", "assessment": "pass/fail", "evidence": [],
           "interpretations": [], "confidence": "medium", "confidence_reason": "the addendum's own words"}
    assert RowNewPayload(row=row).row["units"] == ["ADD-03:2.4"]
