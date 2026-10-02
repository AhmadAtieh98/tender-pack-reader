"""tenderpack.dates against hand-counted values.

Every expected date below is a literal counted by hand on a 2026 calendar, with the count in a
comment. Weekdays used: 1 October 2026 is a Thursday, so 8, 15, 22, 29 October and 5, 12, 19,
26 November 2026 are Thursdays. Working Days are Sunday-Thursday (VOL-I §2.4); Fri/Sat are the weekend.
"""
from datetime import date, timedelta

import pytest

from tenderpack.dates import (Calendar, DateRule, Interpretation, calendar_from_config, interpretations,
                              parse_date, planning_value)

CAL = Calendar()
PDD_A, PDD_B = date(2026, 11, 12), date(2026, 11, 26)     # the two Proposal Due Dates in play


def by_key(interps: list[Interpretation]) -> dict[str, date | None]:
    return {i.key: i.value for i in interps}


# ------------------------------------------------------------------ calendar

def test_weekend_is_friday_and_saturday():
    # 8-14 Nov 2026 = Sun Mon Tue Wed Thu Fri Sat (one week starting on a Sunday)
    week = [date(2026, 11, 8) + timedelta(days=i) for i in range(7)]
    assert [CAL.is_working_day(d) for d in week] == [True, True, True, True, True, False, False]
    # every Friday and Saturday over a whole year is a non-working day
    for i in range(366):
        d = date(2026, 1, 1) + timedelta(days=i)
        if d.weekday() in (4, 5):
            assert not CAL.is_working_day(d), d


def test_add_working_days_forward_does_not_count_start():
    # Thu 8 Oct +5: Sun 11 (1), Mon 12 (2), Tue 13 (3), Wed 14 (4), Thu 15 (5)
    assert CAL.add_working_days(date(2026, 10, 8), 5) == date(2026, 10, 15)
    # Thu 8 Oct +1: Fri 9 and Sat 10 skipped -> Sun 11
    assert CAL.add_working_days(date(2026, 10, 8), 1) == date(2026, 10, 11)


def test_add_working_days_backward_excludes_stated_date():
    # Thu 12 Nov -10 (12 Nov not counted, §2.4): Wed 11 (1), Tue 10 (2), Mon 9 (3), Sun 8 (4),
    # [Sat 7, Fri 6], Thu 5 (5), Wed 4 (6), Tue 3 (7), Mon 2 (8), Sun 1 (9), [Sat 31, Fri 30], Thu 29 Oct (10)
    assert CAL.add_working_days(date(2026, 11, 12), -10) == date(2026, 10, 29)
    # Thu 26 Nov -10: 25 (1), 24 (2), 23 (3), 22 (4), [21, 20], 19 (5), 18 (6), 17 (7), 16 (8), 15 (9), [14, 13], 12 (10)
    assert CAL.add_working_days(date(2026, 11, 26), -10) == date(2026, 11, 12)


def test_add_working_days_zero_and_weekend_starts():
    assert CAL.add_working_days(date(2026, 10, 9), 0) == date(2026, 10, 9)        # n == 0 -> d, even a Friday
    assert CAL.add_working_days(date(2026, 10, 9), 1) == date(2026, 10, 11)       # Fri 9 -> [Sat 10] -> Sun 11
    assert CAL.add_working_days(date(2026, 10, 10), -1) == date(2026, 10, 8)      # Sat 10 -> [Fri 9] -> Thu 8


def test_configured_holiday_moves_backward_count_one_day_earlier():
    cal = Calendar(holidays=frozenset({date(2026, 11, 5)}))
    assert not cal.is_working_day(date(2026, 11, 5))
    # Thu 12 Nov -10 with Thu 5 Nov a holiday: 11 (1), 10 (2), 9 (3), 8 (4), [7, 6, 5 holiday],
    # 4 (5), 3 (6), 2 (7), 1 (8), [31, 30], Thu 29 Oct (9), Wed 28 Oct (10)
    assert cal.add_working_days(date(2026, 11, 12), -10) == date(2026, 10, 28)


def test_working_days_between_half_open():
    a, b = date(2026, 10, 22), date(2026, 11, 26)            # both Thursdays, exactly 5 weeks apart
    # (22 Oct, 26 Nov]: Sun 25-Thu 29 Oct (5), 1-5 Nov (5), 8-12 (5), 15-19 (5), 22-26 (5) = 25.
    # NB the brief quoted 24: that is the count with BOTH ends excluded (26 Nov dropped -> 5+5+5+5+4).
    assert CAL.working_days_between(a, b) == 25
    assert CAL.working_days_between(a, b) - CAL.is_working_day(b) == 24
    assert CAL.working_days_between(b, a) == -25                                  # antisymmetric
    assert CAL.working_days_between(a, a) == 0
    # Thu 8 Oct -> Thu 15 Oct: 11, 12, 13, 14, 15 = 5, and it inverts add_working_days
    assert CAL.working_days_between(date(2026, 10, 8), date(2026, 10, 15)) == 5
    assert CAL.add_working_days(a, CAL.working_days_between(a, b)) == b


def test_calendar_from_config():
    assert calendar_from_config(None) == Calendar()
    cal = calendar_from_config({"weekend": ["Fri", "saturday"], "holidays": ["2026-11-19", date(2026, 11, 5)]})
    assert cal.weekend == frozenset({4, 5})
    assert cal.holidays == frozenset({date(2026, 11, 19), date(2026, 11, 5)})
    assert calendar_from_config({"holidays": []}) == Calendar()                  # weekend defaults to Fri/Sat
    with pytest.raises(ValueError):
        calendar_from_config({"weekends": ["Fri"]})                               # misspelt key
    with pytest.raises(ValueError):
        calendar_from_config({"weekend": ["Fry"]})
    with pytest.raises(ValueError):
        calendar_from_config({"holidays": ["19/11/2026"]})


# ------------------------------------------------------------------ printed dates

def test_parse_date_examples():
    assert parse_date("Proposals shall be received by the Authority not later than 14:00 hours Riyadh time on "
                      "Thursday 12 November 2026 at the address given in Appendix 3.") == (date(2026, 11, 12), "14:00")
    assert parse_date("Proposal Due Date: 12 November 2026, 14:00 Riyadh time") == (date(2026, 11, 12), "14:00")
    assert parse_date("Issued 22 October 2026") == (date(2026, 10, 22), None)
    assert parse_date("on Thursday 26 November 2026") == (date(2026, 11, 26), None)
    assert parse_date("no date here") is None


def test_parse_date_first_date_wins_and_contradictions_raise():
    assert parse_date("from 8 October 2026 to 22 October 2026") == (date(2026, 10, 8), None)
    with pytest.raises(ValueError, match="weekday"):
        parse_date("Friday 12 November 2026")                                     # 12 Nov 2026 is a Thursday
    with pytest.raises(ValueError):
        parse_date("31 November 2026")                                            # November has 30 days
    assert parse_date("scale 1:50, issued 22 October 2026") == (date(2026, 10, 22), None)   # not a time


# ------------------------------------------------------------------ interpretations

def bond_rule() -> DateRule:
    return DateRule("bid-bond-validity", "relative", "validity_end", anchor="PDD", offset=180,
                    text="valid for one hundred and eighty (180) days from the Proposal Due Date")


def test_bid_bond_180_days():
    # 12 Nov + 180: to 30 Nov 18, Dec 49, Jan 80, Feb 108, Mar 139, Apr 169, +11 -> 11 May 2027
    got = interpretations(bond_rule(), {"PDD": PDD_A}, CAL)
    assert [i.key for i in got] == ["day0", "day1"]
    assert by_key(got) == {"day0": date(2027, 5, 11), "day1": date(2027, 5, 10)}
    assert all(i.basis == "not stated in the pack" for i in got)
    # 26 Nov + 180: to 30 Nov 4, Dec 35, Jan 66, Feb 94, Mar 125, Apr 155, +25 -> 25 May 2027
    got = interpretations(bond_rule(), {"PDD": PDD_B}, CAL)
    assert by_key(got) == {"day0": date(2027, 5, 25), "day1": date(2027, 5, 24)}


def test_proposal_validity_150_days():
    rule = DateRule("proposal-validity", "relative", "validity_end", anchor="PDD", offset=150)
    # 12 Nov + 150: Apr 30 is +169, so +150 is 19 days earlier -> 11 Apr 2027
    assert by_key(interpretations(rule, {"PDD": PDD_A}, CAL)) == {"day0": date(2027, 4, 11), "day1": date(2027, 4, 10)}
    # 26 Nov + 150: Apr 30 is +155, so +150 is 5 days earlier -> 25 Apr 2027
    assert by_key(interpretations(rule, {"PDD": PDD_B}, CAL)) == {"day0": date(2027, 4, 25), "day1": date(2027, 4, 24)}


def cutoff_rule() -> DateRule:
    return DateRule("clarification-cutoff", "relative", "deadline", anchor="PDD", offset=10,
                    unit="working_day", direction="before")


def test_clarification_cutoff_10_working_days_before_pdd():
    # counted in test_add_working_days_backward_excludes_stated_date: 12 Nov -> 29 Oct, 26 Nov -> 12 Nov
    got = interpretations(cutoff_rule(), {"PDD": PDD_A}, CAL)
    assert len(got) == 1
    assert (got[0].key, got[0].value, got[0].basis) == ("stated_date_excluded", date(2026, 10, 29), "VOL-I §2.4")
    assert by_key(interpretations(cutoff_rule(), {"PDD": PDD_B}, CAL)) == {"stated_date_excluded": date(2026, 11, 12)}


def lookback_rule() -> DateRule:
    return DateRule("reference-plant-lookback", "relative", "window_start", anchor="PDD", offset=10,
                    unit="year", direction="before", text="within the ten (10) years preceding")


def test_reference_plant_lookback_10_years():
    # 12 Nov 2026 - 10 years = 12 Nov 2016; exclusive boundary starts the next day, 13 Nov 2016
    got = interpretations(lookback_rule(), {"PDD": PDD_A}, CAL)
    assert [i.key for i in got] == ["boundary_inclusive", "boundary_exclusive"]
    assert by_key(got) == {"boundary_inclusive": date(2016, 11, 12), "boundary_exclusive": date(2016, 11, 13)}
    # 29 Feb 2028 - 10 years: 2018 has no 29 Feb -> 28 Feb 2018 (exclusive: 1 Mar 2018)
    leap = by_key(interpretations(lookback_rule(), {"PDD": date(2028, 2, 29)}, CAL))
    assert leap == {"boundary_inclusive": date(2018, 2, 28), "boundary_exclusive": date(2018, 3, 1)}


def addendum_rule() -> DateRule:
    return DateRule("add01-ack", "relative", "deadline", anchor="ADD-01-issue", offset=5, unit="working_day",
                    source_unit="ADD-01:3.1", text="within five (5) Working Days of this Addendum")


def test_addendum_five_working_days_after_issue():
    got = interpretations(addendum_rule(), {"ADD-01-issue": date(2026, 10, 8)}, CAL)
    assert [i.key for i in got] == ["event_day_excluded", "event_day_counted"]
    # excluded: Thu 8 Oct not counted -> 11, 12, 13, 14, 15 -> Thu 15 Oct
    # counted:  Thu 8 Oct is day 1 -> 8, 11, 12, 13, 14 -> Wed 14 Oct
    assert by_key(got) == {"event_day_excluded": date(2026, 10, 15), "event_day_counted": date(2026, 10, 14)}
    assert all(i.basis == "not stated in the pack (VOL-I §2.4 covers backward counting only)" for i in got)
    # issued on Fri 9 Oct (not a Working Day): it cannot be counted; both readings 11..15 -> Thu 15 Oct
    fri = by_key(interpretations(addendum_rule(), {"ADD-01-issue": date(2026, 10, 9)}, CAL))
    assert fri == {"event_day_excluded": date(2026, 10, 15), "event_day_counted": date(2026, 10, 15)}


def test_external_and_missing_anchors_are_unknown():
    pbn = DateRule("pbn-event", "external", "event", anchor="PBN")
    for rule, anchors in ((pbn, {}), (pbn, {"PBN": date(2026, 12, 1)}),        # external: never a value
                          (bond_rule(), {}), (bond_rule(), {"PDD": None})):
        got = interpretations(rule, anchors, CAL)
        assert len(got) == 1 and got[0].key == "unknown_anchor" and got[0].value is None
        assert "not known" in got[0].label


def test_stated_dates_have_one_reading():
    pdd = DateRule("pdd", "anchor", "deadline", anchor="PDD")
    asat = DateRule("fin-asat", "as_at", "as_at", anchor="PDD")
    fixed = DateRule("site-visit", "fixed", "event", fixed=date(2026, 10, 20), source_unit="VOL-I:5.2")
    for rule, want in ((pdd, PDD_A), (asat, PDD_A), (fixed, date(2026, 10, 20))):
        got = interpretations(rule, {"PDD": PDD_A}, CAL)
        assert [(i.key, i.value) for i in got] == [("as_stated", want)]


def test_malformed_rules_are_rejected():
    with pytest.raises(ValueError):
        DateRule("x", "relative", "deadline", anchor="PDD", offset=5, unit="working_days")   # typo in unit
    with pytest.raises(ValueError):
        DateRule("x", "relative", "deadline", anchor="PDD", offset=0)
    with pytest.raises(ValueError):
        DateRule("x", "fixed", "event")


def test_interpretations_are_deterministic():
    anchors = {"PDD": PDD_A, "ADD-01-issue": date(2026, 10, 8)}
    for rule in (bond_rule(), cutoff_rule(), lookback_rule(), addendum_rule()):
        first = interpretations(rule, anchors, CAL)
        assert all(interpretations(rule, dict(reversed(anchors.items())), Calendar()) == first for _ in range(5))


# ------------------------------------------------------------------ planning value

def test_planning_value_conservative():
    anchors = {"PDD": PDD_A, "ADD-01-issue": date(2026, 10, 8)}
    for rule, want in ((bond_rule(), date(2027, 5, 11)),          # validity_end: latest of 11 May / 10 May
                       (cutoff_rule(), date(2026, 10, 29)),       # deadline: the single §2.4 reading
                       (addendum_rule(), date(2026, 10, 14)),     # deadline: earliest of 15 Oct / 14 Oct
                       (lookback_rule(), date(2016, 11, 13))):    # window_start: latest start, narrowest window
        assert planning_value(rule, interpretations(rule, anchors, CAL)).value == want, rule.rule_id


def test_planning_value_explicit_policy_and_unknowns():
    interps = interpretations(bond_rule(), {"PDD": PDD_A}, CAL)
    assert planning_value(bond_rule(), interps, "day1").value == date(2027, 5, 10)
    assert planning_value(bond_rule(), interps, "no-such-key").value == date(2027, 5, 11)   # falls back
    unknown = interpretations(bond_rule(), {}, CAL)
    assert planning_value(bond_rule(), unknown).key == "unknown_anchor"
