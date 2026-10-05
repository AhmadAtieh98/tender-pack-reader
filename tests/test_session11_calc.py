"""Session 11, owner's section 3: deterministic calculation tools for the derived quantities.

Blind rehearsal 04 computed none of its derived quantities (rehearsals/blind-04/COMPARISON.md, "Dates" and S1/S3/S7):
25 % of the Estimated Project Cost, the LD of 0.05 % of it a day, the 200 days at which the 10 % cap is reached, the
84-mark threshold (70 % of 120), the bore a 7,500 m3/h flow needs at 1.5 m/s (DN1200 no longer enough). The answer
key is public since the rehearsal's unsealing (16:42 UTC, 4 Oct 2026), so its numbers are the expected values here.
Operands are synthetic (literal numbers, or the addendum's own words quoted); the real pack's committed build is only
read. Every result carries its operands with their sources, the units, the method or formula, the assumptions and,
through the tools layer, the inputs fingerprint; a missing operand, a unit mismatch or an unsupported formula is
`unresolved` with the reason, and nothing a caller passes is evaluated.
"""
from __future__ import annotations

import pytest

from tenderpack import calc as C
from tenderpack.dates import Calendar
from tenderpack.util import ROOT


def q(words: str, unit: str | None = None, **kw) -> dict:
    """An operand quoted from the addendum (ADD-03, blind rehearsal 04)."""
    return {"source": {"unit": kw.pop("at", "ADD-03:3.1"), "words": words}, **({"unit": unit} if unit else {}), **kw}


# ---------------------------------------------------------------------------------------------- the blind-04 quantities

def test_25_percent_of_the_epc_stays_an_expression_until_the_epc_is_known():
    """3.1: 8.4(a) becomes 25 % of the EPC; the EPC is the Bidder's Form 4-F figure, not in the pack."""
    r = C.compute("percentage_of", {"percent": q("twenty-five per cent (25%)"),
                                    "of": {"name": "Estimated Project Cost", "unit": "SAR"}})
    assert r["status"] == "unresolved" and r["value"] is None
    assert "missing operand `Estimated Project Cost`" in r["reason"]
    assert r["symbolic"] == "25% x Estimated Project Cost"
    assert r["operands"][0] == {"name": "percent", "value": 25, "unit": "%", "literal": False,
                                "source": {"unit": "ADD-03:3.1", "words": "twenty-five per cent (25%)"}}
    ok = C.compute("percentage_of", {"percent": q("twenty-five per cent (25%)"),
                                     "of": {"name": "EPC", "value": 3_200_000_000, "unit": "SAR"}})
    assert (ok["status"], ok["value"], ok["unit"], ok["text"]) == ("resolved", 800_000_000, "SAR", "SAR 800,000,000")
    assert ok["formula"] == "value = percent / 100 x figure"


def test_the_break_even_epcs_of_the_net_worth_test_and_the_ld_rate():
    """3.1 'equal to the old SAR 800,000,000 only when EPC = SAR 3,200,000,000'; 4.1 break-even SAR 360,000,000."""
    nw = C.compute("ratio", {"numerator": q("SAR 800,000,000", at="VOL-I:8.4"), "denominator": q("(25%)")})
    assert (nw["status"], nw["value"], nw["unit"]) == ("resolved", 3_200_000_000, "SAR")
    ld = C.compute("ratio", {"numerator": q("SAR 180,000 for each day of delay", at="VOL-V:18.1"),
                             "denominator": q("one-twentieth of one per cent (0.05%)", at="ADD-03:4.1")})
    assert (ld["value"], ld["unit"], ld["text"]) == (360_000_000, "SAR", "SAR 360,000,000")
    assert "a figure over a percentage" in ld["assumptions"][0]


def test_the_ld_cap_is_reached_on_the_200th_day_whatever_the_epc():
    """IE3 / S7: 10 % (VOL-V 18.4, unchanged) over 0.05 % a day (ADD-03 4.1) = 200 days."""
    r = C.compute("cap", {"cap": q("ten per cent (10%) of the Estimated Project Cost", "% of Estimated Project Cost",
                                   at="VOL-V:18.4"),
                          "rate": q("one-twentieth of one per cent (0.05%) of the Estimated Project Cost for each day",
                                    "% of Estimated Project Cost per day", at="ADD-03:4.1")})
    assert (r["status"], r["value"], r["unit"], r["text"]) == ("resolved", 200, "day", "200 days")
    assert r["reached_in_period"] == 200 and r["exact"] is True
    assert r["method"] == "cap" and "ceil" in r["formula"]
    mismatch = C.compute("cap", {"cap": {"value": 10, "unit": "% of Estimated Project Cost"},
                                 "rate": {"value": 180000, "unit": "SAR per day"}})
    assert mismatch["status"] == "unresolved" and "unit mismatch" in mismatch["reason"]


def test_the_technical_threshold_is_84_marks_of_120_with_the_rounding_rule_stated():
    """IE4 / S3: 70 % of the total marks in Table 1-1 (second revision, total 120) = 84, not 70."""
    r = C.compute("threshold_of_total", {"percent": q("seventy per cent (70%)", at="ADD-03:6.2"),
                                         "total": {"name": "Table 1-1 total", "value": 120, "unit": "marks"}})
    assert (r["value"], r["unit"], r["text"]) == (84, "marks", "84 marks")
    assert r["rounding"] == C.ROUNDING["none"]
    odd = C.compute("threshold_of_total", {"percent": {"value": 70, "unit": "%"}, "total": {"value": 115, "unit": "marks"},
                                           "rounding": "up"})
    assert odd["exact"] == 80.5 and odd["value"] == 81 and odd["rounding"] == "rounded up to a whole number"


def test_the_bore_at_1_5_m_s_is_1_330_m_so_dn1200_is_no_longer_enough():
    """IE1 / S1: 7,500 m3/h = 2.083 m3/s; d = sqrt(4Q/(pi v)) = 1.330 m at 1.5 m/s (1.152 m at 2.0); DN1200 runs at
    1.842 m/s; the next standard size is DN1400 (a labelled assumption)."""
    flow = q("Value: 7,500", "m3/h", at="VOL-II:T2-6/2-6.2")
    at15 = C.compute("approved_formula", {"formula": "pipe-bore-from-flow-velocity",
                                          "operands": {"Q": flow, "v": q("1.5 m/s", at="ADD-03:5.1")}})
    assert (at15["status"], at15["value"], at15["unit"]) == ("resolved", 1.33, "m")
    assert at15["next_standard_size"] == {"label": "DN1400", "value": 1.4, "unit": "m"}
    assert any("PROVISIONAL ASSUMPTION" in a for a in at15["assumptions"])
    assert at15["formula_id"] == "pipe-bore-from-flow-velocity" and "continuity" in at15["formula_source"]
    assert at15["registry"]["sha256"] and at15["steps"][0].startswith("Q: 7,500 m3/h = 2.083333 m3/s")
    at20 = C.compute("approved_formula", {"formula": "pipe-bore-from-flow-velocity",
                                          "operands": {"Q": flow, "v": q("a maximum velocity of 2.0 m/s", at="VOL-II:5.2")}})
    assert at20["value"] == 1.152 and at20["next_standard_size"]["label"] == "DN1200"
    v = C.compute("approved_formula", {"formula": "velocity-from-flow-and-bore",
                                       "operands": {"Q": flow, "d": {"name": "DN1200 bore", "value": 1200, "unit": "mm"}}})
    assert (v["value"], v["unit"]) == (1.842, "m/s")


def test_working_days_convert_through_the_calendar_from_an_anchor():
    """Section 7's trigger deadline: ten Working Days before Thu 26 Nov 2026, the 26th not counted = Thu 12 Nov."""
    r = C.compute("unit_conversion", {"value": {"value": 10, "unit": "Working Days"}, "to_unit": "days",
                                      "anchor_date": "2026-11-26", "direction": "before"}, calendar=Calendar())
    assert (r["value"], r["unit"], r["end_date"]) == (14, "day", "2026-11-12")
    back = C.compute("unit_conversion", {"value": {"value": 14, "unit": "days"}, "to_unit": "Working Days",
                                         "anchor_date": "2026-11-26", "direction": "before"}, calendar=Calendar())
    assert back["value"] == 10
    no_anchor = C.compute("unit_conversion", {"value": {"value": 10, "unit": "Working Days"}, "to_unit": "days"},
                          calendar=Calendar())
    assert no_anchor["status"] == "unresolved" and "anchor_date" in no_anchor["reason"]
    pct = C.compute("unit_conversion", {"value": {"value": 0.05, "unit": "%"}, "to_unit": "fraction"})
    assert pct["value"] == 0.0005


# ---------------------------------------------------------------------------------------------- unresolved, never guessed

@pytest.mark.parametrize("method, args, why", [
    ("approved_formula", {"formula": "__import__('os').system('true')", "operands": {}}, "no approved formula"),
    ("approved_formula", {"formula": "pipe-bore-from-flow-velocity", "operands": {"Q": {"value": 2, "unit": "m3/s"}}},
     "missing operand `v`"),
    ("approved_formula", {"formula": "pipe-bore-from-flow-velocity",
                          "operands": {"Q": {"value": 2, "unit": "kg/s"}, "v": {"value": 1.5, "unit": "m/s"}}},
     "unit mismatch for Q"),
    ("approved_formula", {"formula": "pipe-bore-from-flow-velocity",
                          "operands": {"Q": {"value": 2, "unit": "m3/s"}, "v": 1.5, "x": 1}}, "variables the formula does not have"),
    ("percentage_of", {"percent": {"value": "7500*2", "unit": "%"}, "of": 1}, "not a literal number"),
    ("percentage_of", {"percent": {"value": 25, "unit": "SAR"}, "of": 1}, "must be a percentage"),
    ("percentage_of", {"percent": q("twenty-five per cent (25%)", value=10), "of": 1}, "state 25%, not 10"),
    ("ratio", {"numerator": q("between 2 and 3"), "denominator": 1}, "state 2 figures"),
    ("ratio", {"numerator": {"value": 1, "unit": "m"}, "denominator": {"value": 0, "unit": "m"}}, "is zero"),
    ("ratio", {"numerator": {"value": 1, "unit": "m"}, "denominator": {"value": 2, "unit": "SAR"}}, "unit mismatch"),
    ("unit_conversion", {"value": {"value": 30, "unit": "kg"}, "to_unit": "lb"}, "not in the conversion table"),
    ("cap", {"cap": {"value": 10, "unit": "%"}}, "missing operand(s) ['rate']"),
    ("eval", {"expr": "1+1"}, "unknown method"),
])
def test_what_cannot_be_computed_is_unresolved_with_the_reason(method, args, why):
    r = C.compute(method, args, calendar=Calendar())
    assert r["status"] == "unresolved" and r["value"] is None, r
    assert why in r["reason"], r["reason"]


def test_the_registry_is_checked_and_its_expressions_alone_are_evaluated(tmp_path):
    reg = tmp_path / "formulas.yaml"
    reg.write_text("formulas:\n"
                   "  ok: {expression: 'a * 2', variables: {a: {unit: m}}, result: {unit: m}, source: test}\n"
                   "  attr: {expression: \"a.__class__\", variables: {a: {unit: m}}, result: {unit: m}, source: test}\n"
                   "  call: {expression: \"open('x')\", variables: {a: {unit: m}}, result: {unit: m}, source: test}\n"
                   "  lam: {expression: '(lambda: 1)()', variables: {a: {unit: m}}, result: {unit: m}, source: test}\n"
                   "  nosrc: {expression: 'a', variables: {a: {unit: m}}, result: {unit: m}}\n"
                   "  free: {expression: 'a + b', variables: {a: {unit: m}}, result: {unit: m}, source: test}\n"
                   "  big: {expression: 'a ** 99', variables: {a: {unit: m}}, result: {unit: m}, source: test}\n",
                   encoding="utf-8")
    R = C.load_registry(reg)
    assert set(R["formulas"]) == {"ok", "big"}
    assert set(R["problems"]) == {"attr", "call", "lam", "nosrc", "free"}
    assert "Attribute" in R["problems"]["attr"] and "'open'" in R["problems"]["call"] and "'b'" in R["problems"]["free"]
    assert C.compute("approved_formula", {"formula": "ok", "operands": {"a": {"value": 2, "unit": "m"}}},
                     registry=R)["value"] == 4
    bad = C.compute("approved_formula", {"formula": "call", "operands": {"a": 1}}, registry=R)
    assert bad["status"] == "unresolved" and "not usable" in bad["reason"]
    big = C.compute("approved_formula", {"formula": "big", "operands": {"a": {"value": 2, "unit": "m"}}}, registry=R)
    assert big["status"] == "unresolved" and "exponent" in big["reason"]
    real = C.load_registry()
    assert real["problems"] == {} and set(real["formulas"]) >= {"pipe-bore-from-flow-velocity",
                                                               "velocity-from-flow-and-bore"}


# ---------------------------------------------------------------------------------------------- through the tool layer

@pytest.fixture(scope="module")
def ws(tmp_path_factory):
    from tenderpack.ai.tools import Workspace
    d = tmp_path_factory.mktemp("calc-ws")
    return Workspace(ROOT / "build", ROOT / "config/pack.yaml", ROOT, d / "staging", d / "worklog")


def test_the_tool_checks_every_quote_against_the_pack_and_carries_the_inputs_fingerprint(ws):
    from tenderpack.ai.tools import call_tool
    args = {"formula": "pipe-bore-from-flow-velocity",
            "operands": {"Q": {"unit": "m3/h", "source": {"unit": "VOL-II:T2-6/2-6.2", "words": "Value: 7,500"}},
                         "v": {"source": {"unit": "VOL-II:5.2", "words": "a maximum velocity of 2.0 m/s"}}}}
    r = call_tool(ws, "calculate", {"kind": "approved_formula", "args": args}, "model")
    assert (r["status"], r["value"], r["unit"]) == ("resolved", 1.152, "m")
    assert r["inputs_fingerprint"] == ws.identity().fingerprint() and r["computed_under"]["evidence_build_id"]
    q_src = r["operands"][0]["source"]
    assert q_src == {"unit": "VOL-II:T2-6/2-6.2", "page": 3, "words": "Value: 7,500", "stage": ws.r["validated"].stage}
    wrong = dict(args, operands={**args["operands"], "v": {"source": {"unit": "VOL-II:5.2", "words": "a maximum velocity of 1.5 m/s"}}})
    w = call_tool(ws, "calculate", {"kind": "approved_formula", "args": wrong}, "model")
    assert w["status"] == "unresolved" and "the quote is not in VOL-II:5.2" in w["reason"]
    page = call_tool(ws, "calculate", {"kind": "ratio", "args": {
        "numerator": {"source": {"unit": "VOL-I:8.4", "page": 9, "words": "SAR 800,000,000"}}, "denominator": 1}}, "model")
    assert page["status"] == "unresolved" and "not p9" in page["reason"]
    wd = call_tool(ws, "calculate", {"kind": "unit_conversion", "args": {
        "value": {"value": 10, "unit": "Working Days"}, "to_unit": "days", "anchor_date": "2026-11-26",
        "direction": "before"}}, "model")
    assert wd["end_date"] == "2026-11-12" and wd["calendar"]["basis"].startswith("VOL-I 2.4")
