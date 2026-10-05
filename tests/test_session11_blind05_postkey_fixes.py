"""Session 11, after the blind-05 key was opened (post-key; labelled, not scored). The scorer's one false positive:
ADD-03 2.1 "Volume I Clauses 6.6 and 6.7 are deleted and replaced by the following single Clause 6.6" cited, for the
parser, only the later "Clause 6.6": the plural "Clauses N and M" (and "Clauses N, M and K", "Clauses N to M") matched
nothing, so clause 6.7 was never a target and row VOL-I-6.7-01 stayed in the candidate unflagged."""
from tenderpack.citations import citations


def _targets(text):
    return [c.target for c in citations(text) if c.kind == "clause"]


def test_plural_clauses_with_and_cite_every_clause():
    assert _targets("Volume I Clauses 6.6 and 6.7 are deleted") == ["VOL-I:6.6", "VOL-I:6.7"]


def test_the_blind05_sentence_cites_both_deleted_clauses_and_the_new_one():
    t = "Volume I Clauses 6.6 and 6.7 are deleted and replaced by the following single Clause 6.6:"
    assert set(_targets(t)) >= {"VOL-I:6.6", "VOL-I:6.7"}


def test_plural_clauses_with_commas_and_a_range_cite_the_listed_ends():
    assert _targets("Volume II Clauses 3.1, 3.2 and 3.4 apply") == ["VOL-II:3.1", "VOL-II:3.2", "VOL-II:3.4"]
    # session 12 (deliberate change): a range is no longer read as its two ends; it is one `clause_range` citation that
    # resolve() expands against the document's structure (tests/test_session12_citations.py)
    from tenderpack.citations import resolve
    assert _targets("Volume V Clauses 29.1 to 29.3 are amended") == []
    assert [c.kind for c in citations("Volume V Clauses 29.1 to 29.3 are amended")] == ["clause_range"]
    assert resolve(citations("Volume V Clauses 29.1 to 29.3 are amended"),
                   {"VOL-V:29.1", "VOL-V:29.2", "VOL-V:29.3"}) == ["VOL-V:29.1", "VOL-V:29.2", "VOL-V:29.3"]


def test_the_singular_forms_are_unchanged():
    assert _targets("Volume I Clause 6.6 and Clause 6.7 are deleted") == ["VOL-I:6.6", "VOL-I:6.7"]
    assert _targets("Volume I Clause 6.6 is deleted") == ["VOL-I:6.6"]
