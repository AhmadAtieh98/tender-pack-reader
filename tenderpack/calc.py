"""Deterministic calculations for derived quantities (session 11): narrow methods, never free arithmetic.

Blind rehearsal 04 left every derived quantity uncomputed (rehearsals/blind-04/COMPARISON.md): 25 % of the Estimated
Project Cost, 0.05 % of it per day, the 200 days at which a 10 % cap is reached at 0.05 % a day, 70 % of 120 marks, the
bore a 7,500 m3/h flow needs at 1.5 m/s. Each is one of these methods:

  percentage_of(percent, of)                 x % of a figure (the figure in its own unit)
  threshold_of_total(percent, total, rounding)   p % of a total, with the rounding rule stated (default: none, exact)
  ratio(numerator, denominator)              a / b: the same unit -> a pure number; a figure over a percentage -> the
                                             figure (the break-even: SAR 800,000,000 / 25 % = SAR 3,200,000,000)
  cap(cap, rate)                             a cap over a rate per period -> the count of periods at which the cap is
                                             reached ('% of EPC' over '% of EPC per day' -> days)
  unit_conversion(value, to_unit, anchor_date, direction)   a fixed, small table only: m3/h <-> m3/s, mm <-> m,
                                             per cent <-> fraction, calendar days <-> Working Days (through the
                                             register's calendar, from an anchor date); nothing outside the table
  relative_change(previous, change, direction)   session 14 (W3): a stated change of an amount ('reduced by SAR
                                             1,000,000', 'increased by 10%'): the same unit -> previous +/- change; a
                                             percentage of a figure in another unit -> previous x (1 +/- p/100); a
                                             percentage of a percentage (points or relative?) and a result below zero
                                             are left unresolved for a person
  approved_formula(formula, operands)        a named formula of the registry (config/formulas.yaml): its variables,
                                             units and source; evaluated by a safe evaluator over the registry's own
                                             expressions only (numbers, + - * / **, sqrt, ceil, floor, abs, min, max,
                                             pi): a caller names a formula id, never an expression

An operand is {"name", "value" (a literal number), "unit", "source": {"unit", "page", "words", "stage"}}: where it comes
from the pack, the quote is kept with it, its figure is read from the quoted words (a parenthesised numeral first:
'twenty-five per cent (25%)' -> 25 %) and, when a value is also given, the two must agree. `resolve_source` (the tools
layer) checks each quote against the unit's text at its stage. Nothing a caller passes is evaluated: a value that is
not a literal number, a missing operand, a unit outside the table or a unit mismatch leaves the result `unresolved`
with the reason; so does an unknown or malformed formula.

Every result: {method, status (resolved | unresolved), value, unit, text, formula (the method or formula as words),
symbolic (the same with the operands' names), operands [{name, value, unit, source, literal}], assumptions, rounding,
steps, reason, formula_id / formula_source / registry (approved formulas)}; the tools layer adds the inputs
fingerprint it was computed under (tools.computed_under).
"""
from __future__ import annotations

import ast
import hashlib
import json
import math
import re
from datetime import date, timedelta
from decimal import ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path

from .util import ROOT, load_yaml

METHODS = ("percentage_of", "threshold_of_total", "ratio", "cap", "unit_conversion", "approved_formula", "deadline",
           "relative_change")
REGISTRY = ROOT / "config/formulas.yaml"
ROUNDING = {"none": "not rounded (exact; the pack states no rounding rule)",
            "up": "rounded up to a whole number", "down": "rounded down to a whole number",
            "nearest": "rounded to the nearest whole number (half up)"}
PERIODS = {"day": "day", "days": "day", "calendar day": "day", "calendar days": "day",
           "working day": "working_day", "working days": "working_day", "working_day": "working_day",
           "week": "week", "weeks": "week", "month": "month", "months": "month", "year": "year", "years": "year"}
PLURAL = {"day": "days", "working_day": "Working Days", "week": "weeks", "month": "months", "year": "years"}


class CalcError(ValueError):
    """Why a calculation is left unresolved (never raised to the caller: it becomes the result's `reason`)."""


# ---------------------------------------------------------------------------------------------- units

_ALIASES = [(r"m³", "m3"), (r"\bcubic met(?:re|er)s? per hour\b", "m3/h"), (r"\bcubic met(?:re|er)s? per second\b", "m3/s"),
            (r"\bmet(?:re|er)s? per second\b", "m/s"), (r"\bper ?cent\b", "%"), (r"\bpercent\b", "%"),
            (r"\bmillimet(?:re|er)s?\b", "mm"), (r"\bmet(?:re|er)s?\b", "m"), (r"\bsaudi riyals?\b", "SAR")]


def norm_unit(u) -> str:
    """A unit as the table reads it: 'm³/h' -> 'm3/h'; 'per cent' -> '%'; 'Working Days' -> 'working_day'; 'days' ->
    'day'; a rate '<base> per <period>' keeps its base ('% of Estimated Project Cost per day'). Case is kept for the
    base words (a defined term), lowered for the units."""
    s = " ".join(str(u or "").replace("’", "'").split())
    for rx, rep in _ALIASES:
        s = re.sub(rx, rep, s, flags=re.I)
    low = s.lower()
    if low in PERIODS:
        return PERIODS[low]
    if low in ("fraction", "ratio", "", "number"):
        return "fraction" if low == "fraction" else ""
    if low in ("sar", "marks", "mark"):
        return "SAR" if low == "sar" else "marks"
    m = re.fullmatch(r"(.+?)\s+per\s+(calendar day|working day|day|week|month|year)s?", s, re.I)
    if m:
        return f"{norm_unit(m.group(1))} per {PERIODS[m.group(2).lower()]}"
    m = re.fullmatch(r"%\s*(of\s+.+)", s)
    if m:
        return "% " + m.group(1)
    return s if low not in ("m3/h", "m3/s", "m/s", "mm", "m", "%") else low


def _rate(u: str) -> tuple[str, str] | None:
    m = re.fullmatch(r"(.+) per (day|working_day|week|month|year)", u or "")
    return (m.group(1), m.group(2)) if m else None


def _is_percent(u: str) -> bool:
    return u == "%" or u.startswith("% of ")


# ---------------------------------------------------------------------------------------------- numbers

def _dec(v) -> Decimal:
    if isinstance(v, bool) or not isinstance(v, (int, float, Decimal)):
        raise CalcError(f"not a literal number: {v!r} (values are literal numbers or quoted words from the pack; "
                        "nothing is evaluated)")
    d = Decimal(str(v))
    if not d.is_finite():
        raise CalcError(f"not a finite number: {v!r}")
    return d


def _num_text(s: str) -> Decimal | None:
    s = s.strip()
    if not re.fullmatch(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?", s):
        return None
    return Decimal(s.replace(",", ""))


_FIG = re.compile(r"(?P<pre>SAR\s*)?(?<![\w.])(?P<n>\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)(?![\d])\s*"
                  r"(?P<u>%|per cent|m3/h|m³/h|m3/s|m³/s|m/s|mm|m(?![\w/])|Working Days?|days?|marks?|months?|years?|weeks?)?",
                  re.I)


def parse_quantity(words: str) -> list[tuple[Decimal, str]]:
    """The figures the words state, with their units: '(25%)' -> [(25, '%')]; 'SAR 800,000,000' -> [(800000000,
    'SAR')]; '7,500 m3/h' -> [(7500, 'm3/h')]. A parenthesised numeral restating number words ('twenty-five per cent
    (25%)') is the figure; otherwise every figure is returned (the caller decides whether one is meant)."""
    w = " ".join(str(words or "").split())
    par = [m for m in re.finditer(r"\(\s*(\d[\d,]*(?:\.\d+)?)\s*(%|per cent)?\s*\)", w)]
    out = []
    for m in par:
        n = _num_text(m.group(1))
        if n is not None:
            out.append((n, "%" if m.group(2) else ""))
    if out:
        return out
    for m in _FIG.finditer(w):
        n = _num_text(m.group("n"))
        if n is None:
            continue
        unit = "SAR" if m.group("pre") else norm_unit(m.group("u") or "")
        out.append((n, unit))
    return out


def _show(d: Decimal | float | None, unit: str = "") -> str:
    if d is None:
        return ""
    d = Decimal(str(d)) if not isinstance(d, Decimal) else d
    if d == d.to_integral_value():
        s = f"{int(d):,}"
    else:                                     # shown to six decimal places at most (the value keeps its precision)
        q = d.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP).normalize()
        s = f"{q:,f}" if abs(q) >= 1 else format(q, "f")
    u = PLURAL.get(unit, unit)
    if unit == "SAR":
        return f"SAR {s}"
    if unit == "%":
        return f"{s}%"
    return f"{s} {u}".strip()


def _out(d: Decimal | float):
    """A JSON value: an int when whole, else a float."""
    if isinstance(d, float):
        return int(d) if d.is_integer() else d
    return int(d) if d == d.to_integral_value() else float(d)


# ---------------------------------------------------------------------------------------------- operands

def _operand(name: str, raw, resolve_source=None, need_value: bool = True) -> dict:
    """{name, value (Decimal | None), unit, source, literal}: a literal value, or the figure the quoted words state."""
    if raw is None:
        raise CalcError(f"missing operand `{name}`")
    if not isinstance(raw, dict):
        raw = {"value": raw}
    extra = set(raw) - {"name", "value", "unit", "source"}
    if extra:
        raise CalcError(f"operand `{name}`: unknown field(s) {sorted(extra)} (name, value, unit, source)")
    label = str(raw.get("name") or name)
    unit = norm_unit(raw.get("unit"))
    src = raw.get("source")
    value = None
    if raw.get("value") is not None:
        v = raw["value"]
        value = _num_text(v) if isinstance(v, str) else _dec(v)
        if value is None:
            raise CalcError(f"operand `{label}`: {v!r} is not a literal number (nothing is evaluated)")
    checked = None
    if src is not None:
        if not isinstance(src, dict) or not str(src.get("words") or "").strip():
            raise CalcError(f"operand `{label}`: a source is {{unit, words[, page, stage]}} with the quoted words")
        src = {k: src.get(k) for k in ("unit", "unit_id", "page", "words", "stage") if src.get(k) is not None}
        if "unit_id" in src:
            src["unit"] = src.pop("unit_id")
        if resolve_source is not None:
            checked = resolve_source(src)
            if not checked.get("verified"):
                raise CalcError(f"operand `{label}`: {checked.get('why') or 'the quote is not in the unit'}")
            src = {k: checked.get(k, src.get(k)) for k in ("unit", "page", "words", "stage")}
        figs = parse_quantity(src["words"])
        if value is None:
            if len({f[0] for f in figs}) != 1:
                raise CalcError(f"operand `{label}`: the quoted words '{src['words']}' state "
                                + (f"{len(figs)} figures ({', '.join(_show(*f) for f in figs)}); give the value"
                                   if figs else "no figure; give the value"))
            value = figs[0][0]
            unit = unit or figs[0][1]
        elif figs and value not in {f[0] for f in figs}:
            raise CalcError(f"operand `{label}`: the quoted words '{src['words']}' state "
                            f"{', '.join(_show(*f) for f in figs)}, not {_show(value)}")
        fig_units = {f[1] for f in figs if f[0] == value and f[1]}
        if unit and fig_units and unit not in fig_units and not unit.startswith(tuple(fig_units)):
            if not (_is_percent(unit) and "%" in fig_units):
                raise CalcError(f"operand `{label}`: the quoted words give the unit {sorted(fig_units)}, not '{unit}'")
        if not unit and len(fig_units) == 1:
            unit = next(iter(fig_units))
    if value is None and need_value:
        raise CalcError(f"missing operand `{label}`: no value" + (f" ({src['words']})" if src else ""))
    return {"name": label, "value": value, "unit": unit, "source": src, "literal": src is None}


def _public(ops: list[dict]) -> list[dict]:
    return [{**o, "value": _out(o["value"]) if o["value"] is not None else None} for o in ops]


def _result(method: str, *, value=None, unit: str = "", formula: str = "", symbolic: str = "", operands=(),
            assumptions=(), rounding: str = "", steps=(), reason: str | None = None, **extra) -> dict:
    status = "resolved" if reason is None and value is not None else "unresolved"
    return {"method": method, "status": status, "value": _out(value) if value is not None else None,
            "unit": unit if status == "resolved" else unit, "text": _show(value, unit) if status == "resolved" else "",
            "formula": formula, "symbolic": symbolic, "operands": _public(list(operands)),
            "assumptions": list(assumptions), "rounding": rounding, "steps": list(steps),
            "reason": reason if status == "unresolved" else None, **extra}


# ---------------------------------------------------------------------------------------------- methods

def percentage_of(percent, of, resolve_source=None) -> dict:
    m, formula = "percentage_of", "value = percent / 100 x figure"
    ops: list[dict] = []
    try:
        p = _operand("percent", percent, resolve_source)
        ops.append(p)
        if p["unit"] == "fraction":
            p["value"], p["unit"] = p["value"] * 100, "%"
        if p["unit"] != "%":
            raise CalcError(f"unit mismatch: `{p['name']}` must be a percentage (%), not '{p['unit'] or 'no unit'}'")
        f = _operand("of", of, resolve_source, need_value=False)
        ops.append(f)
        sym = f"{_show(p['value'], '%')} x {f['name']}"
        if f["value"] is None:
            raise CalcError(f"missing operand `{f['name']}`: no value in the pack"
                            + (f" (the words: '{f['source']['words']}')" if f.get("source") else "")
                            + f"; the result stays the expression {sym}")
        v = p["value"] / 100 * f["value"]
        return _result(m, value=v, unit=f["unit"], formula=formula, symbolic=sym, operands=ops,
                       steps=[f"{_show(p['value'], '%')} x {_show(f['value'], f['unit'])} = {_show(v, f['unit'])}"])
    except CalcError as e:
        sym = (f"{_show(ops[0]['value'], '%')} x {ops[1]['name'] if len(ops) > 1 else 'of'}" if ops else "")
        return _result(m, formula=formula, symbolic=sym, operands=ops, reason=str(e))


def threshold_of_total(percent, total, rounding: str = "none", resolve_source=None) -> dict:
    m, formula = "threshold_of_total", "threshold = percent / 100 x total"
    ops: list[dict] = []
    try:
        if rounding not in ROUNDING:
            raise CalcError(f"rounding must be one of {sorted(ROUNDING)}")
        p = _operand("percent", percent, resolve_source)
        ops.append(p)
        if p["unit"] != "%":
            raise CalcError(f"unit mismatch: `{p['name']}` must be a percentage (%), not '{p['unit'] or 'no unit'}'")
        t = _operand("total", total, resolve_source)
        ops.append(t)
        exact = p["value"] / 100 * t["value"]
        v = {"none": exact, "up": exact.to_integral_value(ROUND_CEILING), "down": exact.to_integral_value(ROUND_FLOOR),
             "nearest": exact.to_integral_value(ROUND_HALF_UP)}[rounding]
        steps = [f"{_show(p['value'], '%')} x {_show(t['value'], t['unit'])} = {_show(exact, t['unit'])}"]
        if v != exact:
            steps.append(f"{ROUNDING[rounding]}: {_show(v, t['unit'])}")
        return _result(m, value=v, unit=t["unit"], formula=formula,
                       symbolic=f"{_show(p['value'], '%')} x {t['name']}", operands=ops, rounding=ROUNDING[rounding],
                       steps=steps, exact=_out(exact))
    except CalcError as e:
        return _result(m, formula=formula, operands=ops, rounding=ROUNDING.get(rounding, ""), reason=str(e))


def ratio(numerator, denominator, resolve_source=None) -> dict:
    m = "ratio"
    ops: list[dict] = []
    try:
        a = _operand("numerator", numerator, resolve_source)
        ops.append(a)
        b = _operand("denominator", denominator, resolve_source)
        ops.append(b)
        if b["value"] == 0:
            raise CalcError(f"`{b['name']}` is zero")
        if a["unit"] == b["unit"]:
            v, unit, how = a["value"] / b["value"], "", "the same unit on both sides: a pure number"
        elif b["unit"] == "%" and not _is_percent(a["unit"]):
            v, unit, how = a["value"] / (b["value"] / 100), a["unit"], "a figure over a percentage: the whole it is that percentage of"
        else:
            raise CalcError(f"unit mismatch: {a['unit'] or 'no unit'} / {b['unit'] or 'no unit'} is not a ratio the "
                            "table knows (the same unit, or a figure over a percentage)")
        return _result(m, value=v, unit=unit, formula="value = numerator / denominator",
                       symbolic=f"{a['name']} / {b['name']}", operands=ops, assumptions=[how],
                       steps=[f"{_show(a['value'], a['unit'])} / {_show(b['value'], b['unit'])} = {_show(v, unit)}"])
    except (CalcError, InvalidOperation) as e:
        return _result(m, formula="value = numerator / denominator", operands=ops, reason=str(e))


def cap(cap, rate, resolve_source=None) -> dict:
    m, formula = "cap", "count = cap / rate per period; reached in period ceil(count)"
    ops: list[dict] = []
    try:
        c = _operand("cap", cap, resolve_source)
        ops.append(c)
        r = _operand("rate", rate, resolve_source)
        ops.append(r)
        rr = _rate(r["unit"])
        if rr is None:
            raise CalcError(f"unit mismatch: the rate's unit must be '<cap unit> per <period>', not '{r['unit']}'")
        base, period = rr
        if base != c["unit"]:
            raise CalcError(f"unit mismatch: the cap is in '{c['unit']}', the rate in '{base}' per {period}")
        if r["value"] <= 0:
            raise CalcError(f"`{r['name']}` must be positive")
        count = c["value"] / r["value"]
        reached = count.to_integral_value(ROUND_CEILING)
        exact = count == reached
        steps = [f"{_show(c['value'], c['unit'])} / {_show(r['value'], base)} per {period} = {_show(count)} "
                 f"{PLURAL[period]}"]
        return _result(m, value=count, unit=period, formula=formula, symbolic=f"{c['name']} / {r['name']}",
                       operands=ops, steps=steps, reached_in_period=int(reached), exact=exact,
                       assumptions=["the rate accrues uniformly from the first period; "
                                    + (f"the cap is reached at the end of period {int(reached)}" if exact else
                                       f"the cap is reached during period {int(reached)} (the count is not whole)")],
                       rounding="not rounded; the period in which the cap is reached is ceil(count)")
    except CalcError as e:
        return _result(m, formula=formula, operands=ops, reason=str(e))


# session 14 (W3): a relative change of an amount (blind-07 2.1, 'is reduced by SAR 1,000,000'; COMPARISON.md §8 item 6:
# "not even a computed value is offered"). The previous value is the target's EFFECTIVE value before the op (the amend
# engine passes it with its quote); the change is the provision's own words. Nothing is evaluated and nothing is typed.
DIRECTIONS = {"increase": 1, "decrease": -1}


def relative_change(previous, change, direction: str, resolve_source=None) -> dict:
    m = "relative_change"
    formula = "new = previous +/- change (same unit); new = previous x (1 +/- change / 100) (a percentage)"
    ops: list[dict] = []
    try:
        if direction not in DIRECTIONS:
            raise CalcError(f"direction must be one of {sorted(DIRECTIONS)}, not {direction!r}")
        a = _operand("previous", previous, resolve_source)
        ops.append(a)
        c = _operand("change", change, resolve_source)
        ops.append(c)
        sign, word = DIRECTIONS[direction], ("+" if direction == "increase" else "-")
        if c["value"] < 0:
            raise CalcError(f"`{c['name']}` is negative; the direction carries the sign")
        if c["unit"] == a["unit"] and not _is_percent(a["unit"]):
            v = a["value"] + sign * c["value"]
            step = f"{_show(a['value'], a['unit'])} {word} {_show(c['value'], c['unit'])} = {_show(v, a['unit'])}"
            sym, how = f"{a['name']} {word} {c['name']}", "the change is in the amount's own unit"
        elif _is_percent(c["unit"]) and not _is_percent(a["unit"]):
            v = a["value"] * (1 + sign * c["value"] / 100)
            step = f"{_show(a['value'], a['unit'])} x (1 {word} {_show(c['value'], '%')}) = {_show(v, a['unit'])}"
            sym, how = f"{a['name']} x (1 {word} {c['name']} / 100)", "a percentage of the amount itself"
        elif _is_percent(c["unit"]) and _is_percent(a["unit"]):
            raise CalcError(f"a change of {_show(c['value'], '%')} to a value in % may be percentage points or a "
                            "relative change; the words do not settle it, so a person decides (nothing is computed)")
        else:
            raise CalcError(f"unit mismatch: the amount is in '{a['unit'] or 'no unit'}', the change in "
                            f"'{c['unit'] or 'no unit'}'")
        if v < 0:
            raise CalcError(f"the change takes the amount below zero ({step}); a person reads the provision")
        return _result(m, value=v, unit=a["unit"], formula=formula, symbolic=sym, operands=ops, steps=[step],
                       assumptions=[how], rounding="not rounded (exact; the pack states no rounding rule)",
                       direction=direction)
    except (CalcError, InvalidOperation) as e:
        return _result(m, formula=formula, operands=ops, reason=str(e), direction=direction)


_FACTORS = {("m3/h", "m3/s"): Decimal(1) / Decimal(3600), ("m3/s", "m3/h"): Decimal(3600),
            ("mm", "m"): Decimal("0.001"), ("m", "mm"): Decimal(1000),
            ("%", "fraction"): Decimal("0.01"), ("fraction", "%"): Decimal(100)}
CONVERSIONS = sorted(f"{a} -> {b}" for a, b in _FACTORS) + ["day -> working_day (anchor_date)",
                                                             "working_day -> day (anchor_date)"]


def unit_conversion(value, to_unit: str, anchor_date: str | None = None, direction: str = "after", calendar=None,
                    resolve_source=None) -> dict:
    m = "unit_conversion"
    ops: list[dict] = []
    try:
        x = _operand("value", value, resolve_source)
        ops.append(x)
        frm, to = x["unit"], norm_unit(to_unit)
        if (frm, to) in _FACTORS:
            f = _FACTORS[(frm, to)]
            v = x["value"] * f
            return _result(m, value=v, unit=to, formula=f"{frm} -> {to}: x {_show(f)}", symbolic=f"{x['name']} in {to}",
                           operands=ops, steps=[f"{_show(x['value'], frm)} = {_show(v, to)}"],
                           assumptions=["exact factor of the conversion table"])
        if {frm, to} == {"day", "working_day"}:
            if calendar is None:
                raise CalcError("a Working Day count needs the register's calendar")
            if not anchor_date:
                raise CalcError("days <-> Working Days depends on the dates: give anchor_date (and direction)")
            if direction not in ("after", "before"):
                raise CalcError("direction must be 'after' or 'before'")
            try:
                a = date.fromisoformat(str(anchor_date))
            except ValueError:
                raise CalcError(f"anchor_date must be an ISO date, got {anchor_date!r}") from None
            n = x["value"]
            if n != n.to_integral_value() or n < 0:
                raise CalcError("a count of days is a whole, non-negative number")
            n, sign = int(n), (1 if direction == "after" else -1)
            if frm == "day":
                end = a + timedelta(days=sign * n)
                v = abs(calendar.working_days_between(a, end))
                how = (f"Working Days in the {n} calendar days {direction} {a.isoformat()} (the anchor not counted, "
                       f"{end.isoformat()} counted)")
            else:
                end = calendar.add_working_days(a, sign * n)
                v = abs((end - a).days)
                how = (f"{n} Working Days {direction} {a.isoformat()} end on {end.isoformat()} (the anchor never "
                       "counted, VOL-I 2.4 backwards; the forward convention is not stated in the pack)")
            return _result(m, value=Decimal(v), unit=to, formula=f"{frm} -> {to} through the register's calendar",
                           symbolic=f"{x['name']} in {to}", operands=ops, steps=[how], end_date=end.isoformat(),
                           assumptions=[f"weekend {sorted(calendar.weekend)} (date.weekday numbers); holidays "
                                        f"{sorted(h.isoformat() for h in calendar.holidays) or 'none'}"])
        raise CalcError(f"'{frm or 'no unit'}' -> '{to or 'no unit'}' is not in the conversion table "
                        f"({'; '.join(CONVERSIONS)})")
    except CalcError as e:
        return _result(m, operands=ops, reason=str(e))


# ---------------------------------------------------------------------------------------------- deadlines (s12)

def deadline(offset, anchor, direction: str = "before", calendar=None, registry: dict | None = None,
             resolve_source=None) -> dict:
    """Session 12 (W3b): the date "N <unit> before/after X" (blind-05 follow-up 7). `offset` is an operand (a literal
    count with its unit, Working Days or days, and its quoted words); `anchor` {name, date (ISO), source}. Counted under
    the counting rules of the registry (config/formulas.yaml `counting`, each with its source; VOL-I 2.4 for Working Days
    counted backwards): exactly one reading when a rule covers the unit and the direction (status `resolved`); otherwise
    every plausible reading (dates.interpretations) with status `ambiguous`, `escalate: true` and the reason (never one
    chosen). An anchor with no date, a count that is not a whole literal number or a unit other than days / Working
    Days is `unresolved`. The result carries the inputs, the counting rule and a fingerprint over them."""
    from .dates import DateRule, interpretations
    m = "deadline"
    reg = registry if registry is not None else load_registry()
    ops: list[dict] = []
    base = {"method": m, "status": "unresolved", "value": None, "unit": "date", "text": "", "readings": [],
            "counting": None, "escalate": False, "operands": [], "steps": [], "reason": None,
            "registry": {"path": reg.get("path"), "sha256": reg.get("sha256")}}
    try:
        x = _operand("offset", offset, resolve_source)
        ops.append(x)
        unit = {"day": "day", "working_day": "working_day", "week": "week"}.get(x["unit"])
        if unit is None:
            raise CalcError(f"the period's unit {x['unit'] or 'not stated'!r} is not days or Working Days: a person "
                            "reads it")
        n = x["value"]
        if n != n.to_integral_value() or n < 0:
            raise CalcError("a count of days is a whole, non-negative number")
        n = int(n) * (7 if unit == "week" else 1)
        unit = "day" if unit == "week" else unit
        if direction not in ("before", "after"):
            raise CalcError("direction must be 'before' or 'after'")
        a = dict(anchor or {})
        try:
            ad = date.fromisoformat(str(a.get("date")))
        except ValueError:
            raise CalcError(f"the anchor {a.get('name') or '?'} has no known date ({a.get('date')!r}): nothing is "
                            "computed until it occurs or is stated") from None
        if calendar is None:
            raise CalcError("a deadline needs the register's calendar")
        inputs = {"offset": {"count": n, "unit": unit, "words": (x.get("source") or {}).get("words")},
                  "anchor": {"name": a.get("name"), "date": ad.isoformat(), "source": a.get("source")},
                  "direction": direction}
        rule = DateRule(rule_id="calc", kind="relative", purpose="deadline", anchor="X", offset=n,
                        unit="calendar_day" if unit == "day" else "working_day", direction=direction, fixed=None,
                        source_unit=(x.get("source") or {}).get("unit") or "", text=str(inputs["offset"]["words"] or ""),
                        note="")
        readings = [{"key": i.key, "value": i.value.isoformat() if i.value else None, "basis": i.basis, "label": i.label}
                    for i in interpretations(rule, {"X": ad}, calendar)]
        hit = next(((cid, c) for cid, c in (reg.get("counting") or {}).items()
                    if c["unit"] == unit and c["direction"] == direction), None)
        fp = hashlib.sha256(json.dumps({"inputs": inputs, "rule": hit and hit[0], "registry": reg.get("sha256"),
                                        "weekend": sorted(calendar.weekend),
                                        "holidays": sorted(h.isoformat() for h in calendar.holidays)},
                                       sort_keys=True, default=str).encode()).hexdigest()
        base.update(operands=_public(ops), inputs=inputs, readings=readings, fingerprint=fp)
        if hit is None:
            base.update(status="ambiguous", escalate=True, reason=(
                f"the counting rules state nothing for {PLURAL.get(unit, unit)} counted {direction} a date ("
                f"{'VOL-I 2.4 covers Working Days counted backwards' if unit == 'working_day' else 'no rule in the registry'}"
                f"): not stated, so every reading is kept and a person decides"))
            return base
        cid, c = hit
        sign = -1 if direction == "before" else 1
        v = calendar.add_working_days(ad, sign * n) if unit == "working_day" else ad + timedelta(days=sign * n)
        base.update(status="resolved", value=v.isoformat(), text=v.isoformat(),
                    counting={"id": cid, "convention": c["convention"], "source": c["source"], "basis": c.get("basis")},
                    readings=[{"key": c["convention"], "value": v.isoformat(), "basis": c.get("basis") or c["source"]["unit"]}],
                    steps=[f"{n} {PLURAL.get(unit, unit)} {direction} {a.get('name')} ({ad.isoformat()}), {a.get('name')} "
                           f"itself not counted ({c['source']['unit']}): {v.isoformat()}"])
        return base
    except CalcError as e:
        base.update(operands=_public(ops), reason=str(e))
        return base


# ---------------------------------------------------------------------------------------------- approved formulas

_BIN = {ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b, ast.Mult: lambda a, b: a * b,
        ast.Div: lambda a, b: a / b, ast.Pow: lambda a, b: a ** b}
_FUNCS = {"sqrt": math.sqrt, "ceil": math.ceil, "floor": math.floor, "abs": abs, "min": min, "max": max}
_CONSTS = {"pi": math.pi}


def _check_expr(expr: str, variables: set[str]) -> ast.Expression:
    """The registry expression parsed and checked: only numbers, the declared variables, pi, + - * / **, unary +/-
    and the whitelisted functions. Anything else is refused (CalcError)."""
    try:
        tree = ast.parse(str(expr), mode="eval")
    except SyntaxError as e:
        raise CalcError(f"the expression does not parse: {e.msg}") from None
    for n in ast.walk(tree):
        if isinstance(n, (ast.Expression, ast.Load)) or type(n) in _BIN or isinstance(n, (ast.UAdd, ast.USub)):
            continue
        if isinstance(n, ast.BinOp) and type(n.op) in _BIN:
            continue
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.UAdd, ast.USub)):
            continue
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool):
            continue
        if isinstance(n, ast.Name) and (n.id in variables or n.id in _CONSTS or n.id in _FUNCS):
            continue
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in _FUNCS and not n.keywords:
            continue
        what = n.id if isinstance(n, ast.Name) else (n.func.id if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                                                     else None)
        raise CalcError(f"the expression uses {type(n).__name__}" + (f" '{what}'" if what else "")
                        + ", which the safe evaluator refuses")
    return tree


def _eval(node, env: dict):
    if isinstance(node, ast.Expression):
        return _eval(node.body, env)
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in env:
            return env[node.id]
        if node.id in _CONSTS:
            return _CONSTS[node.id]
        raise CalcError(f"unknown name {node.id}")
    if isinstance(node, ast.UnaryOp):
        v = _eval(node.operand, env)
        return -v if isinstance(node.op, ast.USub) else v
    if isinstance(node, ast.BinOp):
        a, b = _eval(node.left, env), _eval(node.right, env)
        if isinstance(node.op, ast.Pow) and abs(b) > 10:
            raise CalcError("an exponent above 10 is refused")
        if isinstance(node.op, ast.Div) and b == 0:
            raise CalcError("division by zero")
        return _BIN[type(node.op)](a, b)
    if isinstance(node, ast.Call):
        args = [_eval(a, env) for a in node.args]
        if node.func.id == "sqrt" and args and args[0] < 0:
            raise CalcError("square root of a negative number")
        return _FUNCS[node.func.id](*args)
    raise CalcError(f"refused: {type(node).__name__}")


def load_registry(path: Path | str | None = None) -> dict:
    """{"formulas": {id: spec}, "problems": {id: why}, "path", "sha256"}: the approved formulas, each checked (its
    expression with the safe evaluator's rules, its variables' units, its result unit and its source). A formula with
    a problem is listed under `problems` and is not usable."""
    p = Path(path) if path else REGISTRY
    raw = p.read_bytes() if p.exists() else b""
    data = (load_yaml(p) or {}) if p.exists() else {}
    good, bad = {}, {}
    for fid, spec in sorted(((data or {}).get("formulas") or {}).items()):
        try:
            if not isinstance(spec, dict):
                raise CalcError("not a mapping")
            variables = spec.get("variables") or {}
            if not isinstance(variables, dict) or not variables:
                raise CalcError("no variables")
            for v, vs in variables.items():
                if not re.fullmatch(r"[A-Za-z_]\w*", str(v)) or v in _FUNCS or v in _CONSTS:
                    raise CalcError(f"bad variable name {v!r}")
                if not isinstance(vs, dict) or not str(vs.get("unit") or "").strip():
                    raise CalcError(f"variable {v} needs a unit")
            if not str((spec.get("result") or {}).get("unit") or "").strip():
                raise CalcError("the result needs a unit")
            if not str(spec.get("source") or "").strip():
                raise CalcError("a formula needs its source")
            _check_expr(spec.get("expression"), set(variables))
            good[fid] = spec
        except CalcError as e:
            bad[fid] = str(e)
    counting = {}                                      # session 12 (W3b): the counting rules calc.deadline reads
    for cid, spec in sorted(((data or {}).get("counting") or {}).items()):
        if not isinstance(spec, dict) or spec.get("unit") not in ("day", "working_day") or \
                spec.get("direction") not in ("before", "after") or not (spec.get("source") or {}).get("unit") or \
                spec.get("convention") != "stated_date_excluded":
            bad[f"counting:{cid}"] = "a counting rule needs unit (day | working_day), direction, convention " \
                                     "(stated_date_excluded) and its source {unit, page, words}"
            continue
        counting[cid] = spec
    return {"formulas": good, "problems": bad, "counting": counting, "path": str(p),
            "sha256": hashlib.sha256(raw).hexdigest() if raw else None}


def approved_formula(formula: str, operands: dict | None, registry: dict | None = None, resolve_source=None) -> dict:
    m = "approved_formula"
    reg = registry if registry is not None else load_registry()
    info = {"formula_id": formula, "registry": {"path": reg.get("path"), "sha256": reg.get("sha256")}}
    ops: list[dict] = []
    try:
        if formula in reg.get("problems", {}):
            raise CalcError(f"formula {formula!r} is in the registry but not usable: {reg['problems'][formula]}")
        spec = reg.get("formulas", {}).get(formula)
        if spec is None:
            raise CalcError(f"no approved formula {formula!r} in {reg.get('path')} (approved: "
                            f"{', '.join(sorted(reg.get('formulas', {}))) or 'none'}); an unsupported formula is left "
                            "unresolved")
        info.update({"formula_source": spec["source"], "formula_name": spec.get("name", formula)})
        if not isinstance(operands, dict):
            raise CalcError("operands must be a mapping {variable: operand}")
        variables = spec["variables"]
        extra = sorted(set(operands) - set(variables))
        if extra:
            raise CalcError(f"operands for variables the formula does not have: {extra} (it has {sorted(variables)})")
        env, steps = {}, []
        for v, vs in variables.items():
            o = _operand(v, operands.get(v), resolve_source)
            ops.append(o)
            want = norm_unit(vs["unit"])
            if o["unit"] != want:
                conv = unit_conversion({"name": o["name"], "value": float(o["value"]), "unit": o["unit"]}, want)
                if conv["status"] != "resolved":
                    raise CalcError(f"unit mismatch for {v}: given '{o['unit'] or 'no unit'}', the formula needs "
                                    f"'{want}' ({conv['reason']})")
                steps.append(f"{v}: {conv['steps'][0]}")
                env[v] = float(conv["value"])
            else:
                env[v] = float(o["value"])
        tree = _check_expr(spec["expression"], set(variables))
        val = float(_eval(tree, env))
        if not math.isfinite(val):
            raise CalcError("the result is not a finite number")
        res = spec["result"]
        unit = norm_unit(res["unit"])
        dec = res.get("decimals")
        shown = round(val, int(dec)) if dec is not None else val
        steps.append(f"{res.get('symbol', 'result')} = {spec['expression']} with "
                     + ", ".join(f"{k} = {env[k]:.6g} {norm_unit(variables[k]['unit'])}" for k in variables)
                     + f" = {val:.6g} {unit}")
        assumptions = list(spec.get("assumptions") or [])
        rounding = f"shown to {dec} decimal places" if dec is not None else "not rounded"
        extra_out = {}
        sizes = spec.get("standard_sizes")
        if sizes:
            vals, labels = list(sizes.get("values") or []), list(sizes.get("labels") or [])
            nxt = next(((labels[i] if i < len(labels) else vals[i], vals[i]) for i in range(len(vals))
                        if vals[i] >= val - 1e-12), None)
            extra_out["next_standard_size"] = ({"label": nxt[0], "value": nxt[1], "unit": norm_unit(sizes.get("unit") or res["unit"])}
                                               if nxt else None)
            assumptions.append(f"standard sizes: {sizes.get('basis')}")
            steps.append(f"the next size at or above {shown} {unit}: {nxt[0] if nxt else 'none in the list'}")
        return _result(m, value=shown, unit=unit, formula=f"{res.get('symbol', 'result')} = {spec['expression']}",
                       symbolic=spec["expression"], operands=ops, assumptions=assumptions, rounding=rounding,
                       steps=steps, unrounded=val, **info, **extra_out)
    except (CalcError, ArithmeticError, ValueError, TypeError) as e:
        return _result(m, operands=ops, reason=str(e), **info)


# ---------------------------------------------------------------------------------------------- dispatch

_ARGS = {"deadline": ({"offset", "anchor"}, {"direction"}),
         "percentage_of": ({"percent", "of"}, set()), "threshold_of_total": ({"percent", "total"}, {"rounding"}),
         "ratio": ({"numerator", "denominator"}, set()), "cap": ({"cap", "rate"}, set()),
         "unit_conversion": ({"value", "to_unit"}, {"anchor_date", "direction"}),
         "approved_formula": ({"formula", "operands"}, set()),
         "relative_change": ({"previous", "change", "direction"}, set())}       # session 14 (W3)


def compute(method: str, args: dict, *, resolve_source=None, calendar=None, registry: dict | None = None) -> dict:
    """One calculation by method id; never raises for a calculation that cannot be done (the result is `unresolved`
    with the reason). Unknown arguments, a missing argument or an unknown method are `unresolved` too."""
    if method not in _ARGS:
        return _result(str(method), reason=f"unknown method {method!r}; methods: {', '.join(METHODS)} (no free arithmetic)")
    need, opt = _ARGS[method]
    args = dict(args or {})
    extra = sorted(set(args) - need - opt)
    missing = sorted(k for k in need if k not in args)
    if extra or missing:
        return _result(method, reason=(f"unknown argument(s) {extra}" if extra else "")
                       + ("; " if extra and missing else "") + (f"missing operand(s) {missing}" if missing else "")
                       + f" (arguments: {sorted(need | opt)})")
    if method == "percentage_of":
        return percentage_of(args["percent"], args["of"], resolve_source)
    if method == "threshold_of_total":
        return threshold_of_total(args["percent"], args["total"], args.get("rounding", "none"), resolve_source)
    if method == "ratio":
        return ratio(args["numerator"], args["denominator"], resolve_source)
    if method == "cap":
        return cap(args["cap"], args["rate"], resolve_source)
    if method == "deadline":
        return deadline(args["offset"], args["anchor"], args.get("direction", "before"), calendar, registry,
                        resolve_source)
    if method == "relative_change":                                   # session 14 (W3)
        return relative_change(args["previous"], args["change"], args["direction"], resolve_source)
    if method == "unit_conversion":
        return unit_conversion(args["value"], args["to_unit"], args.get("anchor_date"), args.get("direction", "after"),
                               calendar, resolve_source)
    return approved_formula(args["formula"], args["operands"], registry, resolve_source)
