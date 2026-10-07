"""Session 14 (W4), part 3 (c): keyword triggers respect negation and scope (blind-07 COMPARISON.md section 8 item 14;
section 4 false signals 6 and 7; report section 9 L29).

  * human_owned.triggers: a closure word under a negation in its own clause ('unit not resolved', 'has not been
    settled', 'is not answered', 'whether it resolves') declares nothing closed, so it never makes an item HUMAN
    DECISION PENDING; the same word asserted ('the unit is resolved') still does. Topic words (precedence, governs,
    means) are unchanged: a negated precedence statement still puts the judgment in play.
  * controller.amendment_language: 'the Clauses of Volume II are not renumbered' carries no amendment language, so a
    no_effect answer on it is not flagged 'no_effect on amendment language'; 'are renumbered' still is.
The exact phrases are the blind-07 ones (rehearsals/blind-07/downstream/proposals.yaml L1487, review/index.md L225)."""
from __future__ import annotations

from tenderpack import human_owned as H
from tenderpack.ai.controller import amendment_language


# ---------------------------------------------------------------------------------------------- human_owned.triggers

def test_unit_not_resolved_is_not_a_closure_blind07_false_signal_7():
    note = ("PROPOSED; pending approval of reading ADD-03-p3-r1. The life is printed in months under a years heading; "
            "unit not resolved (see I-ADD-03-T42-5-UNIT).")
    assert H.triggers(note, ("closure",)) == []
    # the downstream classifier on a row payload carrying the note: no 'declares a matter resolved'
    payload = {"row": {"id": "ADD-03-T42-1-05", "interpretations": [{"note": note}]}}
    assert not any("resolved" in x for x in H.downstream_reasons("row_new", payload)), \
        H.downstream_reasons("row_new", payload)


def test_negated_closure_words_in_their_own_clause():
    for t in ("The question has not been resolved.", "This is not settled by the addendum.",
              "The ambiguity is never closed by ADD-02.", "The question is not answered.",
              "Whether it resolves the question is a human decision.", "The point is yet to be resolved.",
              "It cannot be resolved without the Permit.", "No answer has been withdrawn, and nothing is not answered."):
        assert H.triggers(t, ("closure",)) == [], t


def test_asserted_closure_words_still_fire():
    assert H.triggers("The unit is resolved: 24 months.", ("closure",)) == ["declares a matter resolved ('resolved')"]
    assert H.triggers("ADD-02 Q7 settles the term.", ("closure",)) == ["declares a matter settled ('settles')"]
    # a negation in another clause does not reach the word
    assert H.triggers("The unit is not printed in years; it is resolved as months.", ("closure",)) \
        == ["declares a matter resolved ('resolved')"]
    # the first asserted occurrence counts even after a negated one
    assert H.triggers("Row 4 is not resolved. Row 5 is resolved.", ("closure",)) == \
        ["declares a matter resolved ('resolved')"]
    # a trigger that is itself a negative phrase is kept
    assert H.triggers("The Form is no longer required.", ("closure",)) \
        == ["declares an obligation or a question ended ('no longer required')"]


def test_negated_topic_words_still_put_the_judgment_in_play():
    assert H.triggers("Volume I does not prevail over Volume V.", ("topic",)) \
        == ["decides which document prevails (precedence) ('prevail')"]


# ---------------------------------------------------------------------------------------------- amendment_language

def test_not_renumbered_is_no_amendment_language_blind07_false_signal_6():
    t = "The number 8.5 is not reused in Volume II, and the Clauses of Volume II are not renumbered."
    assert amendment_language(t) == []


def test_renumbered_asserted_is_amendment_language():
    assert amendment_language("The Clauses of Volume II are renumbered 8.1 to 8.4.") == ["'are renumbered'"]
    assert amendment_language("Clause 8.6 is not reused; Clause 8.7 is renumbered as 8.6.") == ["'is renumbered'"]
    assert amendment_language("Clause 8.6 is not reused; Clauses 8.7 and 8.8, renumbered, follow.") == ["'renumbered'"]
