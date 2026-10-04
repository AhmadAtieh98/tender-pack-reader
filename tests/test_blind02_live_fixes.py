"""Session 08, blind rehearsal 02: the three tool gaps found while curating an unseen Addendum No. 3 (fixed live, logged
in rehearsals/blind-02/clock.txt). Synthetic text in the addendum's style; no tender content is needed."""
from __future__ import annotations

from tenderpack.amend import _letter_ranges
from tenderpack.citations import citations, row_names, verify_target


def test_a_volume_appendix_is_a_citation_and_its_only_paragraph_is_the_target():
    text = "Volume I Appendix 3 is deleted and replaced by the following: 'Tender Box 2, First Floor'"
    assert [c.target for c in citations(text)] == ["VOL-I:App3"]
    ids = {"VOL-I:H:App3", "VOL-I:App3/para1", "VOL-I:6.1"}
    ok, why, _ = verify_target("VOL-I:App3/para1", text, ids)
    assert ok and "only unit" in why
    ok, _, _ = verify_target("VOL-I:App3/para1", text, ids | {"VOL-I:App3/para2"})   # two paragraphs: name one
    assert not ok


def test_form_rows_named_in_quotes_are_row_names():
    text = "In Form 4-F, the rows ‘Model auditor’ and ‘Date of model audit opinion’ are deleted."
    assert row_names(text) == ["Model auditor", "Date of model audit opinion"]
    ids = {"VOL-IV:F4-F/model-auditor", "VOL-IV:F4-F/date-of-model-audit-opinion", "VOL-IV:F4-F/bidder"}
    assert verify_target("VOL-IV:F4-F/date-of-model-audit-opinion", text, ids)[0]
    assert not verify_target("VOL-IV:F4-F/bidder", text, ids)[0]


def test_a_relettering_stated_as_a_range_states_every_letter_in_it():
    text = "Form 4-G is item (f), and former items (f) to (i) become items (g) to (j) respectively."
    assert _letter_ranges(text).split() == ["(f)", "(g)", "(h)", "(i)", "(g)", "(h)", "(i)", "(j)"]
    assert "(k)" not in _letter_ranges(text) and _letter_ranges("items (a) and (c)") == ""


def test_a_deletion_that_moves_a_full_stop_gains_no_word():
    from tenderpack.amend import UState, unevidenced_additions

    def st(text):
        return {"VOL-I:10.3": UState(unit_id="VOL-I:10.3", doc="VOL-I", kind="clause", status="active", text=text, cells=None,
                                     pages=[5], origin="text_layer", reading_status=None)}
    before = st("without hard-coded values in calculation cells, and shall be accompanied by an opinion addressed to the Authority.")
    after = st("without hard-coded values in calculation cells.")
    assert unevidenced_additions(before, after, "ADD-03") == []
    gained = st("without hard-coded values in calculation sheets.")                  # a substituted word still counts
    assert unevidenced_additions(before, gained, "ADD-03") == ["VOL-I:10.3: 'sheets.'"]
