"""Session 12 (blind-05 follow-up 1, the owner's part 2): a clause range is resolved against the document's structure.

"Clauses 29.1 to 29.3" used to cite only its two ends, so an op on 29.2 failed C22 although 29.2 exists. A range now
yields one `clause_range` citation that resolve() expands to every clause between its ends that the document has
(siblings under the same parent, in numeric order, each treated as a cited clause is). A range whose end does not
exist, or that crosses parents, is flagged INCOMPLETE SCOPE (a reason the caller shows) instead of silently taking its
ends. The list form of session 11 ("Clauses 6.6 and 6.7", "Clauses 3.1, 3.2 and 3.4") is unchanged."""
import pytest

from tenderpack.citations import citations, resolve, resolve_scope, verify_target

IDS = {"VOL-V:29.1", "VOL-V:29.2", "VOL-V:29.3", "VOL-V:29.4", "VOL-V:29.2(a)", "VOL-V:29.2(b)", "VOL-V:30.1",
       "VOL-V:30.2", "VOL-V:28", "VOL-I:6.6", "VOL-I:6.7", "VOL-II:3.1", "VOL-II:3.2", "VOL-II:3.4",
       "VOL-V:31.1", "VOL-V:31.3"}


@pytest.mark.parametrize("text", [
    "Volume V Clauses 29.1 to 29.3 are deleted.",
    "Volume V Clauses 29.1–29.3 are deleted.",
    "Volume V Clauses 29.1 through 29.3 are deleted.",
    "Volume V Clauses 29.1 to 29.3 inclusive are deleted.",
    "In Volume V, Clauses 29.1 to 29.3 are deleted.",
])
def test_a_range_cites_every_clause_between_its_ends(text):
    cites = citations(text)
    assert [c.kind for c in cites if c.kind.startswith("clause")] == ["clause_range"]
    assert resolve(cites, IDS) == ["VOL-V:29.1", "VOL-V:29.2", "VOL-V:29.3"]


def test_verify_target_accepts_the_clause_inside_the_range():
    ok, why, cited = verify_target("VOL-V:29.2", "Volume V Clauses 29.1 to 29.3 are deleted.", IDS)
    assert ok, why
    assert "VOL-V:29.2" in cited
    ok, why, _ = verify_target("VOL-V:29.4", "Volume V Clauses 29.1 to 29.3 are deleted.", IDS)
    assert not ok


def test_a_missing_clause_between_the_ends_resolves_to_what_exists():
    targets, flags = resolve_scope(citations("Volume V Clauses 31.1 to 31.3 are deleted."), IDS)
    assert targets == ["VOL-V:31.1", "VOL-V:31.3"]
    assert flags == []


def test_a_missing_end_is_flagged_incomplete_scope():
    text = "Volume V Clauses 29.2 to 29.6 are deleted."
    targets, flags = resolve_scope(citations(text), IDS)
    assert targets == ["VOL-V:29.2", "VOL-V:29.3", "VOL-V:29.4"]
    assert flags and "INCOMPLETE SCOPE" in flags[0] and "VOL-V:29.6" in flags[0]
    ok, why, _ = verify_target("VOL-V:29.3", text, IDS)
    assert ok and "INCOMPLETE SCOPE" in why                 # accepted, and the caller is told the scope is incomplete
    ok, why, _ = verify_target("VOL-V:30.1", text, IDS)
    assert not ok and "INCOMPLETE SCOPE" in why


def test_a_range_crossing_parents_is_flagged_and_not_filled_in():
    text = "Volume V Clauses 29.3 to 30.2 are deleted."
    targets, flags = resolve_scope(citations(text), IDS)
    assert flags and "INCOMPLETE SCOPE" in flags[0] and "crosses" in flags[0]
    assert "VOL-V:29.4" not in targets and "VOL-V:30.1" not in targets   # nothing inferred across the parents


def test_a_range_of_whole_clauses_takes_their_subclauses():
    assert resolve(citations("Volume V Clauses 29 to 30 apply."), IDS) == [
        "VOL-V:29.1", "VOL-V:29.2", "VOL-V:29.3", "VOL-V:29.4", "VOL-V:30.1", "VOL-V:30.2"]


def test_a_mixed_list_and_range():
    assert resolve(citations("Volume V Clauses 28, 29.1 to 29.3 and 30.2 apply."), IDS) == [
        "VOL-V:28", "VOL-V:29.1", "VOL-V:29.2", "VOL-V:29.3", "VOL-V:30.2"]


def test_the_session11_list_forms_are_unchanged():
    assert [c.target for c in citations("Volume I Clauses 6.6 and 6.7 are deleted")] == ["VOL-I:6.6", "VOL-I:6.7"]
    assert [c.target for c in citations("Volume II Clauses 3.1, 3.2 and 3.4 apply")] == [
        "VOL-II:3.1", "VOL-II:3.2", "VOL-II:3.4"]
    assert resolve(citations("Volume I Clauses 6.6 and 6.7 are deleted"), IDS) == ["VOL-I:6.6", "VOL-I:6.7"]


def test_a_hyphenated_table_or_form_number_is_not_a_range():
    assert [c.kind for c in citations("Volume II Table 2-4 is amended")] == ["table"]
    assert [c.kind for c in citations("Form 4-F is amended")] == ["form"]
