# Subagent brief 2: Build dates.py with counting interpretations

Launched 2026-10-02 07:50:37 UTC; model option requested: `(default)`; subagent type: `general-purpose`.
The text below is the prompt exactly as sent by the coordinator (exported from the session transcript on 4 Oct 2026, session 11).

---

Implement a small, pure date module for a deterministic tender-pack reader. Repository: /home/user/tender-pack-reader (Python 3.11; run with `.venv/bin/python`; tests with `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_dates.py`). You may create/edit ONLY these two files: `tenderpack/dates.py` and `tests/test_dates.py`. Do not edit anything else, do not commit or push, and do not read docs/PLAN.md (the expected values below must be checked independently by your tests). Standard library only (datetime, dataclasses, re). Match the repo's style: module docstring explaining rules, type hints, concise comments.

Facts from the tender (VOL-I §2.4): "Working Day means any day from Sunday to Thursday inclusive, other than a day declared a public holiday in the Kingdom. Where a period expressed in Working Days is to be counted backwards from a stated date, the stated date itself shall not be counted." Weekend = Friday and Saturday. No public holidays are declared in the pack (holidays are a configurable assumption, default empty).

Required API (keep these names and signatures exactly; others may rely on them):

```python
@dataclass(frozen=True)
class Calendar:
    weekend: frozenset[int] = frozenset({4, 5})        # date.weekday(): Fri=4, Sat=5
    holidays: frozenset[date] = frozenset()
    def is_working_day(self, d: date) -> bool
    def add_working_days(self, d: date, n: int) -> date
        # n > 0: the n-th Working Day after d (d itself not counted)
        # n < 0: the |n|-th Working Day before d (d itself not counted, per §2.4)
        # n == 0: d
    def working_days_between(self, a: date, b: date) -> int   # Working Days in the half-open range (a, b]; negative if b < a

def calendar_from_config(cfg: dict | None) -> Calendar      # cfg like {"weekend": ["Fri","Sat"], "holidays": ["2026-11-19", ...]}; None -> default

def parse_date(text: str) -> tuple[date, str | None] | None
    # Find the FIRST date written like "Thursday 26 November 2026", "26 November 2026", "on Thursday 12 November 2026"
    # in free text, and an optional time "14:00" / "14:00 hours" anywhere in the same text. Returns (date, "14:00") or (date, None);
    # None if no date. Weekday name, if present, must match the date; if it does not, raise ValueError (printed weekday contradicts date).

@dataclass(frozen=True)
class DateRule:
    rule_id: str
    kind: str          # "anchor" | "relative" | "fixed" | "as_at" | "external"
    purpose: str       # "deadline" | "validity_end" | "window_start" | "as_at" | "event"
    anchor: str | None = None     # e.g. "PDD", "ADD-01-issue", "PBN" (external events have no value)
    offset: int = 0
    unit: str = "calendar_day"    # "calendar_day" | "working_day" | "year"
    direction: str = "after"      # "after" | "before"
    fixed: date | None = None     # kind == "fixed"
    source_unit: str = ""         # unit id the rule was read from, e.g. "VOL-I:5.2"
    text: str = ""                # the words the rule was read from (quoted from the source)

@dataclass(frozen=True)
class Interpretation:
    key: str          # stable machine key, e.g. "day0", "day1", "stated_date_excluded", "event_day_excluded", "event_day_counted", "boundary_inclusive", "boundary_exclusive", "as_stated"
    label: str        # one plain-English sentence saying how the period was counted
    value: date | None
    basis: str        # where the counting convention comes from: a clause (e.g. "VOL-I §2.4") or "not stated in the pack"

def interpretations(rule: DateRule, anchors: dict[str, date | None], cal: Calendar) -> list[Interpretation]
    # Every plausible way of counting the rule; ordered deterministically.
    #  - relative calendar days ("N days from X"): two readings: "day0" X is day zero -> X+N; "day1" X counts as day one -> X+N-1. basis "not stated in the pack".
    #  - relative working days BEFORE X: ONE reading "stated_date_excluded" (basis "VOL-I §2.4"): cal.add_working_days(X, -N).
    #  - relative working days AFTER X (e.g. "within five (5) Working Days of this Addendum"): two readings:
    #      "event_day_excluded": cal.add_working_days(X, N); "event_day_counted": if X is a working day, cal.add_working_days(X, N-1) else same as excluded. basis "not stated in the pack (VOL-I §2.4 covers backward counting only)".
    #  - relative years BEFORE X ("within the ten (10) years preceding X"): window start X minus N years (29 Feb -> 28 Feb); two readings
    #      "boundary_inclusive" (value = start date; an event on that date counts) and "boundary_exclusive" (value = start date + 1 day). basis "not stated in the pack".
    #  - as_at: one reading "as_stated" = X.   fixed: one reading "as_stated" = fixed.   anchor: one reading "as_stated" = anchors[anchor].
    #  - external, or anchor value missing/None: one reading "unknown_anchor" with value None and label saying the anchor event has not occurred / is not known.

def planning_value(rule: DateRule, interps: list[Interpretation], policy: str = "conservative") -> Interpretation
    # The interpretation used for planning. "conservative": purpose deadline -> earliest value; validity_end -> latest value;
    # window_start -> latest value (narrowest window); as_at/event -> the only/first value. Any other policy string must be
    # the key of an interpretation to use when present (fall back to conservative otherwise). Values None are ignored unless all None.
```

Tests you must write (tests/test_dates.py), with expected values you compute independently in the test (hand-derived, written as literals with a comment showing the counting), at least:
- Calendar: 2026-10-08 (Thu) +5 WD = 2026-10-15 (Thu); 2026-11-12 (Thu) -10 WD = 2026-10-29 (Thu); 2026-11-26 -10 WD = 2026-11-12; Fri/Sat never working days; a configured holiday on 2026-11-05 moves 2026-11-12 -10 WD one working day earlier to 2026-10-28; working_days_between(2026-10-22, 2026-11-26) = 24.
- parse_date: "Proposals shall be received by the Authority not later than 14:00 hours Riyadh time on Thursday 12 November 2026 at the address given in Appendix 3." -> (2026-11-12, "14:00"); "Proposal Due Date: 12 November 2026, 14:00 Riyadh time" -> (2026-11-12, "14:00"); "Issued 22 October 2026" -> (2026-10-22, None); "Friday 12 November 2026" raises ValueError; "no date here" -> None.
- interpretations with PDD 2026-11-12 and 2026-11-26: bid bond "valid for one hundred and eighty (180) days from the Proposal Due Date": day0 2027-05-11 / day1 2027-05-10 (and 2027-05-25 / 2027-05-24 for 26 Nov); proposal validity 150 days: 2027-04-11 / 2027-04-10 (2027-04-25 / 2027-04-24); clarification cut-off 10 WD before PDD: 2026-10-29 (2026-11-12 for 26 Nov), single reading with basis VOL-I §2.4; reference-plant look-back 10 years preceding PDD: inclusive 2016-11-12, exclusive 2016-11-13; ADD-01 §3.1 five WD of 2026-10-08: excluded 2026-10-15, counted 2026-10-14; external anchor PBN -> unknown_anchor with value None.
- planning_value conservative picks: bond validity -> 2027-05-11 (latest); cut-off deadline -> earliest; look-back window -> 2016-11-13 (latest start); explicit policy "day1" picks day1.
- Determinism: interpretations() returns the same ordered list on repeated calls.

Make sure all tests pass. In your final message, report: the API as implemented (any deviation from the spec and why), the list of tests and their result line from pytest, and any ambiguity you noticed in the counting rules.
