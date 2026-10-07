"""Session 13 (part 2, item 5): the supported scope of "applied, not decided" (controller.settled_points,
applied_rule_review, re_present_issue).

The owner: "a clear printed rule can be extracted and applied within its supported scope, but quoting precedence
wording must not automatically resolve a contractual ambiguity or remove human ownership." The scope, now in code:
an applied rule only restates a STATED outcome (a sentence that itself says what governs or prevails, or "X is amended
accordingly" on X) for the exact point the clause names (the same unit or number, or the clause's own distinctive
words), and it keeps the issue's owner with a confirmation line; two readings of the same words, or the human-owned
classifier firing on the point's own words outside the quotation, stay HUMAN DECISION PENDING with the rule quoted as
context; a pointer to an order of precedence applies nothing. Synthetic texts (blind-06 style), not the pack's."""
from __future__ import annotations

from tenderpack.ai.controller import applied_rule_review, re_present_issue, settled_points

TEXTS = {"VOL-I:3.2": "In the event of any conflict, ambiguity or discrepancy between or within the RFP Documents, the "
                      "following order of precedence shall apply, the first named prevailing:",
         "ADD-03:2.2": "Table 1-3 is issued in Arabic, with an English convenience translation in Appendix B. The Arabic "
                       "text governs.",
         "ADD-03:T5-1/row-a": "Zone A: 12 m",
         "ADD-03:Q20": "Bidder question: Which text governs the concession term? | Authority response: The order of "
                       "precedence at Volume I Clause 3.2 applies."}
PROVS = ["ADD-03:2.2", "ADD-03:T5-1/row-a", "ADD-03:Q20"]
LINE = "ADD-03 2.2 provides: 'The Arabic text governs.' (applied, not decided)"


def test_a_precedence_sentence_is_not_applied_to_a_point_on_another_unit():
    pts = settled_points("The Arabic Table 5-1 prints 12 m for zone A and the English translation 15 m. Which rendering "
                         "governs is a decision for Legal.", "ADD-03:T5-1/row-a", TEXTS, "ADD-03", PROVS)
    assert pts == [], [p["line"] for p in pts]


def test_two_readings_of_the_same_words_stay_pending_with_the_rule_quoted_as_context():
    issue = {"id": "I-T", "owner": "Legal counsel",
             "text": "The Arabic words for TP-2 in Table 1-3 can be read as four hours per event or as four hours per "
                     "day. Which rendering governs is a decision for Legal."}
    r = applied_rule_review("issue", issue, "ADD-03:T1-3/tp-2", TEXTS, "ADD-03", PROVS)
    assert r["lines"] == [], r["lines"]
    assert any("two readings" in h and "The Arabic text governs." in h for h in r["human"]), r["human"]


def test_the_classifier_firing_on_the_points_own_words_keeps_it_pending():
    issue = {"id": "I-T", "owner": "Legal counsel",
             "text": "Which rendering of Table 1-3 is deemed accepted, and so governs, is a decision for Legal."}
    r = applied_rule_review("issue", issue, "ADD-03:2.2", TEXTS, "ADD-03", PROVS)
    assert r["lines"] == [] and any("deemed" in h for h in r["human"]) and \
        any("The Arabic text governs." in h for h in r["human"]), r


def test_a_stated_outcome_on_the_exact_unit_is_applied_and_keeps_its_owner_with_a_confirmation_line():
    issue = {"id": "I-T13", "owner": "Legal counsel", "short": "Table 1-3: Arabic vs English values differ",
             "text": "The pending reading of the Arabic Table 1-3 gives a different TP-2 maximum from the English 6 "
                     "hours. Which rendering governs is a decision for Legal."}
    r = applied_rule_review("issue", issue, "ADD-03:2.2", TEXTS, "ADD-03", PROVS)
    assert r["lines"] == [LINE] and r["human"] == []
    e = re_present_issue(dict(issue), r["lines"], r["sentences"], r["confirm"])
    assert e["owner"] == "Legal counsel" and "proposed_owner" not in e, e
    assert "applied rule: ADD-03 2.2 'The Arabic text governs.'; a person confirms the application" in e["text"], e["text"]
    assert e["confirm"] == r["confirm"] and e["proposed_text"] == issue["text"]


def test_a_pointer_to_an_order_of_precedence_applies_nothing():
    assert settled_points("Which text governs the concession term is a decision for Legal.", "ADD-03:Q20", TEXTS,
                          "ADD-03", PROVS) == []
