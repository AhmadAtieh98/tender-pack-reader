"""Dates: the pack's Working Day calendar, printed dates, and every reading of a date rule.

What the pack states (VOL-I §2.4), and nothing more:
  * a Working Day is any day Sunday to Thursday inclusive, other than a declared public holiday
    in the Kingdom (weekend = Friday and Saturday);
  * counting a period of Working Days *backwards* from a stated date, the stated date itself is
    not counted: N Working Days before X is the N-th Working Day strictly before X.
The pack declares no public holidays. Holidays are a configurable assumption (default: none).

What the pack does NOT state, and so is never decided here:
  * whether the event day counts when Working Days are counted *forwards* ("within five (5)
    Working Days of this Addendum");
  * whether X is day 0 or day 1 for calendar days ("180 days from the Proposal Due Date");
  * whether the boundary day of a look-back window counts ("the ten (10) years preceding X").
For these, `interpretations` returns every plausible reading, each labelled with how it was
counted and where that convention comes from ("not stated in the pack" when nowhere).
`planning_value` then picks one by an explicit policy; the default ("conservative") takes the
earliest deadline, the latest validity end and the latest window start (narrowest window).

Year arithmetic: X minus/plus N years keeps month and day; 29 February becomes 28 February.
Pure and deterministic: no clock, no locale (weekday and month names are fixed English tables).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta

WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December")

BASIS_WD_BACKWARD = "VOL-I §2.4"
BASIS_NOT_STATED = "not stated in the pack"
BASIS_WD_FORWARD = "not stated in the pack (VOL-I §2.4 covers backward counting only)"

KINDS = ("anchor", "relative", "fixed", "as_at", "external", "unresolved")
PURPOSES = ("deadline", "validity_end", "window_start", "as_at", "event")
UNITS = ("calendar_day", "working_day", "week", "month", "year")
DIRECTIONS = ("after", "before")


def long_date(d: date) -> str:
    """'Thursday 12 November 2026' (locale-independent)."""
    return f"{WEEKDAYS[d.weekday()]} {d.day} {MONTHS[d.month - 1]} {d.year}"


def shift_months(d: date, n: int) -> date:
    """d moved by n calendar months, same day of the month, clamped to the month's last day (31 Jan + 1 -> 28/29 Feb)."""
    m = d.month - 1 + n
    y, m = d.year + m // 12, m % 12 + 1
    last = (date(y + (m == 12), m % 12 + 1, 1) - timedelta(days=1)).day
    return date(y, m, min(d.day, last))


def shift_years(d: date, n: int) -> date:
    """d moved by n years, same month and day; 29 February -> 28 February in a common year."""
    try:
        return d.replace(year=d.year + n)
    except ValueError:
        return d.replace(year=d.year + n, day=28)


# ------------------------------------------------------------------ calendar

@dataclass(frozen=True)
class Calendar:
    """Working Days per VOL-I §2.4. weekend uses date.weekday(): Mon=0 ... Fri=4, Sat=5, Sun=6."""
    weekend: frozenset[int] = frozenset({4, 5})
    holidays: frozenset[date] = frozenset()

    def __post_init__(self) -> None:
        object.__setattr__(self, "weekend", frozenset(self.weekend))
        object.__setattr__(self, "holidays", frozenset(self.holidays))
        if not all(isinstance(w, int) and 0 <= w <= 6 for w in self.weekend):
            raise ValueError(f"weekend days must be date.weekday() numbers 0-6, got {sorted(self.weekend)}")
        if len(self.weekend) == 7:
            raise ValueError("a weekend of all seven days leaves no Working Days")
        bad = [h for h in self.holidays if not isinstance(h, date) or isinstance(h, datetime)]
        if bad:
            raise ValueError(f"holidays must be dates (not datetimes or strings), got {bad}")

    def is_working_day(self, d: date) -> bool:
        return d.weekday() not in self.weekend and d not in self.holidays

    def add_working_days(self, d: date, n: int) -> date:
        """The |n|-th Working Day after (n > 0) or before (n < 0) d; d itself is never counted.

        Backwards this is VOL-I §2.4 ("the stated date itself shall not be counted"). n == 0 -> d,
        even when d is not a Working Day.
        """
        step = timedelta(days=1 if n > 0 else -1)
        left, cur = abs(n), d
        while left:
            cur += step
            if self.is_working_day(cur):
                left -= 1
        return cur

    def working_days_between(self, a: date, b: date) -> int:
        """Working Days in (a, b]: a not counted, b counted. Antisymmetric: b < a gives
        -working_days_between(b, a). For a Working Day b > a, add_working_days(a, result) == b."""
        if b < a:
            return -self.working_days_between(b, a)
        return sum(self.is_working_day(a + timedelta(days=i)) for i in range(1, (b - a).days + 1))


_DAY_NAMES = {**{n.lower(): i for i, n in enumerate(WEEKDAYS)},
              **{n[:3].lower(): i for i, n in enumerate(WEEKDAYS)}}
_CONFIG_KEYS = {"weekend", "holidays"}


def calendar_from_config(cfg: dict | None) -> Calendar:
    """{"weekend": ["Fri", "Sat"], "holidays": ["2026-11-19", ...]} -> Calendar; None -> default.

    Weekend days are names (full or three-letter, any case). Holidays are ISO strings or dates
    (YAML loads an unquoted 2026-11-19 as a date). Unknown keys and names are rejected so a typo
    cannot silently fall back to the default.
    """
    if cfg is None:
        return Calendar()
    unknown = sorted(set(cfg) - _CONFIG_KEYS)
    if unknown:
        raise ValueError(f"unknown calendar config keys {unknown}; allowed: {sorted(_CONFIG_KEYS)}")
    kw = {}
    if "weekend" in cfg:
        days = []
        for name in cfg["weekend"] or []:
            if not isinstance(name, str) or name.strip().lower() not in _DAY_NAMES:
                raise ValueError(f"unknown weekend day {name!r}; use e.g. 'Fri' or 'Friday'")
            days.append(_DAY_NAMES[name.strip().lower()])
        kw["weekend"] = frozenset(days)
    if "holidays" in cfg:
        hols = []
        for h in cfg["holidays"] or []:
            if isinstance(h, datetime):
                h = h.date()
            elif isinstance(h, str):
                h = date.fromisoformat(h.strip())
            elif not isinstance(h, date):
                raise ValueError(f"holiday {h!r} is not an ISO date string or a date")
            hols.append(h)
        kw["holidays"] = frozenset(hols)
    return Calendar(**kw)


# ------------------------------------------------------------------ printed dates

_DATE = re.compile(
    rf"\b(?:(?P<wd>{'|'.join(WEEKDAYS)}),?\s+)?(?P<d>\d{{1,2}})\s+(?P<m>{'|'.join(MONTHS)}),?\s+(?P<y>\d{{4}})\b",
    re.IGNORECASE)
# HH:MM with a two-digit hour (so a scale such as 1:50 is not a time); a trailing "hours" is ignored
_TIME = re.compile(r"(?<![\d:.])(?P<h>[01]\d|2[0-3]):(?P<min>[0-5]\d)(?![\d:])")
_MONTH_NO = {m.lower(): i + 1 for i, m in enumerate(MONTHS)}
_WEEKDAY_NO = {w.lower(): i for i, w in enumerate(WEEKDAYS)}


def parse_date(text: str) -> tuple[date, str | None] | None:
    """The first date printed like '[Thursday] 26 November 2026' in text, and the first 'HH:MM'
    time ('14:00', '14:00 hours') anywhere in the same text: (date, '14:00') or (date, None).

    None if no date is printed. ValueError if the first date is not a calendar date (31 November)
    or its printed weekday contradicts it: a contradiction is reported, never resolved here.
    """
    m = _DATE.search(text)
    if m is None:
        return None
    try:
        d = date(int(m["y"]), _MONTH_NO[m["m"].lower()], int(m["d"]))
    except ValueError as e:
        raise ValueError(f"'{m.group(0)}' is not a calendar date: {e}") from None
    if m["wd"] and _WEEKDAY_NO[m["wd"].lower()] != d.weekday():
        raise ValueError(f"printed weekday contradicts date: '{m.group(0)}' but "
                         f"{d.day} {MONTHS[d.month - 1]} {d.year} is a {WEEKDAYS[d.weekday()]}")
    t = _TIME.search(text)
    return d, (f"{t['h']}:{t['min']}" if t else None)


# ------------------------------------------------------------------ rules and their readings

@dataclass(frozen=True)
class DateRule:
    rule_id: str
    kind: str          # "anchor" | "relative" | "fixed" | "as_at" | "external"
    purpose: str       # "deadline" | "validity_end" | "window_start" | "as_at" | "event"
    anchor: str | None = None     # e.g. "PDD", "ADD-01-issue", "PBN" (external events have no value)
    offset: int = 0
    unit: str = "calendar_day"    # "calendar_day" | "working_day" | "week" | "month" | "year"
    direction: str = "after"      # "after" | "before"
    fixed: date | None = None     # kind == "fixed"
    source_unit: str = ""         # unit id the rule was read from, e.g. "VOL-I:5.2"
    text: str = ""                # the words the rule was read from (quoted from the source)
    note: str = ""                # kind == "unresolved": why the program does not compute it

    def __post_init__(self) -> None:
        for field, value, allowed in (("kind", self.kind, KINDS), ("purpose", self.purpose, PURPOSES),
                                      ("unit", self.unit, UNITS), ("direction", self.direction, DIRECTIONS)):
            if value not in allowed:
                raise ValueError(f"rule {self.rule_id}: {field} {value!r} not in {allowed}")
        if self.kind in ("anchor", "relative") and not self.anchor:
            raise ValueError(f"rule {self.rule_id}: kind {self.kind} needs an anchor")
        if self.kind == "relative" and self.offset < 1:
            raise ValueError(f"rule {self.rule_id}: a relative rule needs offset >= 1 (direction gives the sign)")
        if self.kind == "fixed" and self.fixed is None:
            raise ValueError(f"rule {self.rule_id}: kind fixed needs a fixed date")
        if self.kind == "as_at" and not self.anchor and self.fixed is None:
            raise ValueError(f"rule {self.rule_id}: kind as_at needs an anchor or a fixed date")
        if self.kind == "unresolved" and not (self.text.strip() and self.note.strip()):
            raise ValueError(f"rule {self.rule_id}: kind unresolved needs the words (text) and why it is not computed (note)")


@dataclass(frozen=True)
class Interpretation:
    key: str          # stable machine key, e.g. "day0", "stated_date_excluded", "boundary_inclusive"
    label: str        # one plain-English sentence saying how the period was counted
    value: date | None
    basis: str        # clause the counting convention comes from, or "not stated in the pack"


def _unknown(rule: DateRule) -> list[Interpretation]:
    name = rule.anchor or rule.rule_id
    return [Interpretation("unknown_anchor",
                           f"{name} has not occurred or its date is not known, so this date cannot be computed yet.",
                           None, BASIS_NOT_STATED)]


def interpretations(rule: DateRule, anchors: dict[str, date | None], cal: Calendar) -> list[Interpretation]:
    """Every plausible way of counting `rule`, in a fixed order (see the module docstring)."""
    if rule.kind == "external":
        return _unknown(rule)
    if rule.kind == "unresolved":
        return [Interpretation("unresolved", f"Not computed: {rule.note}. The words '{rule.text}' stay with a person.",
                               None, BASIS_NOT_STATED)]
    if rule.kind == "fixed":
        return [Interpretation("as_stated", f"Stated date: {long_date(rule.fixed)}.", rule.fixed,
                               f"stated in {rule.source_unit}" if rule.source_unit else "stated in the pack")]
    if rule.kind == "as_at" and not rule.anchor:
        return [Interpretation("as_stated", f"As at the stated date, {long_date(rule.fixed)}.", rule.fixed,
                               f"stated in {rule.source_unit}" if rule.source_unit else "stated in the pack")]
    x = anchors.get(rule.anchor)
    if x is None:
        return _unknown(rule)
    a, n, back = rule.anchor, rule.offset, rule.direction == "before"
    ax = f"{a} ({long_date(x)})"
    if rule.kind in ("anchor", "as_at"):
        word = "As at" if rule.kind == "as_at" else "On"
        return [Interpretation("as_stated", f"{word} {ax}, with no period counted.", x,
                               f"stated in {rule.source_unit}" if rule.source_unit else "stated in the pack")]

    # kind == "relative"
    if rule.unit in ("calendar_day", "week"):
        if rule.unit == "week":
            n, ax = n * 7, f"{ax} ({rule.offset} week{'s' if rule.offset != 1 else ''} = {n * 7} calendar days)"
        sign, way = (-1, "before") if back else (1, "after")
        v0, v1 = x + timedelta(days=sign * n), x + timedelta(days=sign * (n - 1))
        return [
            Interpretation("day0", f"{ax} is day 0, so {n} calendar days {way} it is {long_date(v0)}.",
                           v0, BASIS_NOT_STATED),
            Interpretation("day1", f"{ax} counts as day 1, so day {n}{' counting back' if back else ''} "
                                   f"is {long_date(v1)}.",
                           v1, BASIS_NOT_STATED),
        ]
    if rule.unit == "working_day":
        if back:
            v = cal.add_working_days(x, -n)
            return [Interpretation("stated_date_excluded",
                                   f"Counting {n} Working Days back from {ax}, not counting {a} itself, "
                                   f"gives {long_date(v)}.", v, BASIS_WD_BACKWARD)]
        excl = cal.add_working_days(x, n)
        if cal.is_working_day(x):
            cnt = cal.add_working_days(x, n - 1)
            cnt_label = f"Counting {ax} as the first of {n} Working Days, the last is {long_date(cnt)}."
        else:
            cnt = excl
            cnt_label = (f"{ax} is not a Working Day so it cannot be counted; {n} Working Days after it "
                         f"end on {long_date(cnt)}.")
        return [
            Interpretation("event_day_excluded", f"Counting {n} Working Days forward from {ax}, not counting "
                                                 f"{a} itself, gives {long_date(excl)}.", excl, BASIS_WD_FORWARD),
            Interpretation("event_day_counted", cnt_label, cnt, BASIS_WD_FORWARD),
        ]
    # rule.unit == "month" or "year": a window of n months / years before x (start) or after x (end)
    shift, word = (shift_months, "month") if rule.unit == "month" else (shift_years, "year")
    if back:
        start = shift(x, -n)
        nxt = start + timedelta(days=1)
        return [
            Interpretation("boundary_inclusive", f"The {n}-{word} window before {ax} starts on {long_date(start)}, "
                                                 f"and an event on that day counts.", start, BASIS_NOT_STATED),
            Interpretation("boundary_exclusive", f"The {n}-{word} window before {ax} excludes {long_date(start)}, "
                                                 f"so the earliest day that counts is {long_date(nxt)}.",
                           nxt, BASIS_NOT_STATED),
        ]
    end = shift(x, n)
    prev = end - timedelta(days=1)
    return [
        Interpretation("boundary_inclusive", f"The {n}-{word} period after {ax} ends on {long_date(end)}, "
                                             f"and an event on that day counts.", end, BASIS_NOT_STATED),
        Interpretation("boundary_exclusive", f"The {n}-{word} period after {ax} excludes {long_date(end)}, "
                                             f"so the last day that counts is {long_date(prev)}.",
                       prev, BASIS_NOT_STATED),
    ]


def planning_value(rule: DateRule, interps: list[Interpretation], policy: str = "conservative") -> Interpretation:
    """The reading used for planning.

    "conservative": deadline -> earliest; validity_end -> latest; window_start -> latest (narrowest
    window); as_at / event -> the first. Any other policy names an interpretation key, used when that
    reading exists with a value; otherwise conservative. Readings without a value are ignored unless
    none has one (then the first is returned, e.g. unknown_anchor). Ties keep list order.
    """
    if not interps:
        raise ValueError(f"rule {rule.rule_id}: no interpretations to choose from")
    known = [i for i in interps if i.value is not None]
    if not known:
        return interps[0]
    if policy != "conservative":
        hit = next((i for i in known if i.key == policy), None)
        if hit is not None:
            return hit
    if rule.purpose == "deadline":
        return min(known, key=lambda i: i.value)
    if rule.purpose in ("validity_end", "window_start"):
        return max(known, key=lambda i: i.value)
    return known[0]
