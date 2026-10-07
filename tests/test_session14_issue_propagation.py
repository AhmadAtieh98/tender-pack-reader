"""Session 14 (W4), part 4: issue propagation against its actual scope (report section 9 A4; R1's finding that the
maxima/range issue reaches VOL-V-29.3-01 through the ramp-up relationship on a weak link).

The rule (relationships.issue_reaches): an issue reaches a row through a relationship only when the relationship's
scope includes the issue's subject. A relationship's scope is the whole of what it links unless its entry narrows it
with `scope_words` (words that must be verbatim in its own evidence): then it is the members of its `from` table whose
own words carry them. An issue's subject is its `subject` (unit ids; a table id stands for its members); an issue
without one reaches every row the relationship names, as before (nothing is dropped on a guess).

REL-T24-RAMP-UP-DEDUCTIONS quotes VOL-V 29.3: "no availability deduction shall apply to a parameter listed in Table
2-4 as assessed on a rolling average basis": its scope is the Table 2-4 rows assessed on a rolling average (BOD5, COD,
TSS, TN, TP). I-VOL-II-T24-TENSIONS is about the chlorine and pH ranges, both "Continuous at outlet": outside that
scope, so the issue no longer reaches VOL-V-29.3-01 through it; it still reaches VOL-V-31.1-02 (31.1(b): "fails any
parameter in Volume II Table 2-4"), VOL-II-7.2-01 and VOL-II-3.1-01, whose relationships carry the whole table."""
from __future__ import annotations

import pytest

from tenderpack import relationships, signals, stage2
from tenderpack.util import ROOT

T24 = "I-VOL-II-T24-TENSIONS"
UNITS = [{"unit_id": "V:T1", "text": "table", "pages": [1]},
         {"unit_id": "V:T1/A", "text": "Parameter: A | Basis of assessment: 30-day rolling average", "pages": [1]},
         {"unit_id": "V:T1/B", "text": "Parameter: B | Basis of assessment: Continuous at outlet", "pages": [1]},
         {"unit_id": "W:1", "text": "no deduction shall apply to a parameter listed in Table 1 as assessed on a rolling "
                                    "average basis.", "pages": [2]}]
NARROW = {"id": "REL-N", "from": ["V:T1"], "to": ["ROW-W"], "kind": "limit_applies", "status": "confirmed",
          "evidence": [{"unit": "W:1", "page": 2, "words": "as assessed on a rolling average basis"}],
          "scope_words": "rolling average", "issues": ["I-B", "I-A", "I-ANY"], "origin": "curator"}
WHOLE = {"id": "REL-W", "from": ["V:T1"], "to": ["ROW-X"], "kind": "limit_applies", "status": "confirmed",
         "evidence": [{"unit": "W:1", "page": 2, "words": "no deduction shall apply"}], "issues": ["I-B"],
         "origin": "curator"}
ISSUES = {"I-B": {"text": "B's range", "subject": ["V:T1/B"]}, "I-A": {"text": "A", "subject": ["V:T1"]},
          "I-ANY": {"text": "no subject given"}}


def test_scope_and_subject_synthetic():
    by = {u["unit_id"]: u for u in UNITS}
    assert relationships.entry_scope(NARROW, by) == {"V:T1/A"}
    assert relationships.entry_scope(WHOLE, by) is None
    assert relationships.issue_subject(ISSUES["I-A"], by) == {"V:T1/A", "V:T1/B"}     # a table stands for its members
    ok, why = relationships.issue_reaches(NARROW, "I-B", ISSUES, by)
    assert not ok and "REL-N" in why and "rolling average" in why and "subject is B" in why, why
    assert relationships.issue_reaches(NARROW, "I-A", ISSUES, by)[0]
    assert relationships.issue_reaches(NARROW, "I-ANY", ISSUES, by)[0]               # no subject: kept
    assert relationships.issue_reaches(WHOLE, "I-B", ISSUES, by)[0]                  # whole scope: kept


def test_issue_links_follow_the_rule_synthetic():
    by = {u["unit_id"]: u for u in UNITS}
    links = relationships.issue_links([NARROW, WHOLE], {"ROW-W", "ROW-X"}, issues=ISSUES, units=by)
    assert [x["issue"] for x in links["ROW-W"]] == ["I-A", "I-ANY"]
    assert [x["issue"] for x in links["ROW-X"]] == ["I-B"]
    # without the issues and units the links are as before (a caller that cannot apply the rule drops nothing)
    assert [x["issue"] for x in relationships.issue_links([NARROW], {"ROW-W"})["ROW-W"]] == ["I-B", "I-A", "I-ANY"]
    out = relationships.out_of_scope_links([NARROW, WHOLE], {"ROW-W", "ROW-X"}, ISSUES, by)
    assert list(out) == ["ROW-W"] and out["ROW-W"][0]["issue"] == "I-B"


def test_relationship_issue_notes_follow_the_rule_synthetic():
    by = {u["unit_id"]: u for u in UNITS}
    notes = signals.relationship_issue_notes([NARROW], ["REL-N"], {}, issues=ISSUES, units=by)
    assert notes == ["open: I-A (via REL-N)", "open: I-ANY (via REL-N)"], notes


def test_scope_words_must_be_in_the_entrys_own_evidence_synthetic():
    bad = dict(NARROW, scope_words="continuous")
    f = relationships.validate([bad], UNITS, ["ROW-W"], {}, issues=set(ISSUES))
    assert any("scope_words" in x and "evidence" in x for x in f), f
    empty = dict(NARROW, scope_words="rolling average", evidence=[{"unit": "W:1", "page": 2, "words":
                                                                   "as assessed on a rolling average basis"}],
                 **{"from": ["W:1"]})
    f = relationships.validate([empty], UNITS, ["ROW-W"], {}, issues=set(ISSUES))
    assert any("scope_words" in x and "no member" in x for x in f), f
    assert not [x for x in relationships.validate([NARROW], UNITS, ["ROW-W"], {}, issues=set(ISSUES))
                if "scope" in x]


@pytest.fixture(scope="module")
def real():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


def test_ramp_up_row_no_longer_carries_the_maxima_range_issue(real):
    links = stage2.row_issue_links(real)
    assert T24 not in [x["issue"] for x in links.get("VOL-V-29.3-01", [])]
    assert T24 not in stage2.row_issues(real)["VOL-V-29.3-01"]
    for rid in ("VOL-V-31.1-02", "VOL-II-7.2-01", "VOL-II-3.1-01", "VOL-II-2.5-01"):
        assert T24 in stage2.row_issues(real)[rid], rid
    # the dropped link is shown on the row with its reason (A1's Relationships cell), never silently
    a1 = stage2.a1_table(real, stage2.collect_issues(real, None))
    row = next(x for x in a1["rows"] if x["id"] == "VOL-V-29.3-01")
    assert T24 not in " ".join(row["issues"])
    said = " ".join(row["relationships"])
    assert f"{T24} not carried" in said and "REL-T24-RAMP-UP-DEDUCTIONS" in said and "rolling average" in said, said


def test_a2_ramp_up_line_has_no_maxima_range_note(real):
    a2 = stage2.a2(real)
    lines = [m for m in a2["rows_moved"] if m["row"] == "VOL-V-29.3-01"]
    assert lines
    md = a2["markdown"]
    for m in lines:
        assert T24 not in str(m), m
    for ln in md.splitlines():
        if ln.startswith("| VOL-V-29.3-01 "):
            assert T24 not in ln, ln
