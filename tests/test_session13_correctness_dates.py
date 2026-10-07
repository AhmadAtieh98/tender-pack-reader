"""Session 13 (part 2, item 1): a date rule of kind `anchor` (or `as_at`) carrying a counted period is refused.

The blind-05 regression (rehearsals/blind-05/REGRESSION-S12.md, defect 4; synthetic) promoted a row whose date rule was
`kind: anchor, offset: 2, unit: working_day, direction: before`: dates.interpretations() returns the anchor itself "with
no period counted" for every anchor rule, so the planner placed the milestone on the PDD and the two Working Days were
silently ignored. A rule of kind anchor counts no period; a counted period is kind relative with its offset, unit and
direction. The rule is refused (never converted) by the dataclass, the register's row model (the register loader and
every downstream row proposal), a condition's trigger deadline (C21) and the register's evaluation of a trigger
deadline: never a date planned on the anchor."""
from __future__ import annotations

import copy
from datetime import date

import pytest
from pydantic import ValidationError

from tenderpack.dates import Calendar, DateRule, interpretations
from tenderpack.register import Row, RuleDef, load_rows

CAL = Calendar(weekend={4, 5})
PDD = date(2026, 11, 26)
WORDS = "not later than two (2) Working Days before the Proposal Due Date"
BAD = {"rule_id": "T-R1", "kind": "anchor", "purpose": "deadline", "anchor": "PDD", "offset": 2,
       "unit": "working_day", "direction": "before", "source_unit": "ADD-03:6.7", "text": WORDS}


def test_the_dataclass_refuses_an_anchor_rule_with_a_counted_period():
    with pytest.raises(ValueError, match="kind anchor counts no period.*kind relative with its offset, unit and direction"):
        DateRule(rule_id="T", kind="anchor", purpose="deadline", anchor="PDD", offset=2, unit="working_day",
                 direction="before", text=WORDS)
    with pytest.raises(ValueError, match="kind as_at counts no period"):
        DateRule(rule_id="T", kind="as_at", purpose="as_at", anchor="PDD", offset=3)


def test_an_anchor_rule_without_a_period_and_the_relative_rule_still_compute():
    on = DateRule(rule_id="T", kind="anchor", purpose="deadline", anchor="PDD")
    assert [i.value for i in interpretations(on, {"PDD": PDD}, CAL)] == [PDD]
    rel = DateRule(rule_id="T", kind="relative", purpose="deadline", anchor="PDD", offset=2, unit="working_day",
                   direction="before", text=WORDS)
    assert [i.value for i in interpretations(rel, {"PDD": PDD}, CAL)] == [date(2026, 11, 24)]   # never the PDD


def test_the_register_row_model_refuses_it_with_the_reason():
    with pytest.raises(ValidationError, match="kind anchor counts no period"):
        RuleDef.model_validate(BAD)
    RuleDef.model_validate(dict(BAD, kind="relative"))                     # the consistent rule loads


ROW = {"id": "T-01", "group": "VOL-I:6.7", "scope": ["submission"], "requirement": "test data", "units": ["VOL-I:6.7"],
       "discipline": "Legal", "assessment": "procedural", "evidence": [], "no_deliverable": "test data",
       "interpretations": [{"stage": "BASE", "quote": "test data"}], "date_rules": [BAD],
       "confidence": "low", "confidence_reason": "test data"}


def test_the_register_loader_reports_it_as_a_finding_with_the_reason(tmp_path):
    import yaml
    (tmp_path / "rows").mkdir()
    (tmp_path / "rows.yaml").write_text(yaml.safe_dump({"prepared_by": "test", "method": "test", "anchors": {
        "PDD": {"name": "Proposal Due Date", "defined_in": "VOL-I:6.1"}}, "include": ["rows/*.yaml"], "rows": []}))
    (tmp_path / "rows" / "T.yaml").write_text(yaml.safe_dump({"doc": "VOL-I", "prepared_by": "test", "rows": [ROW]}))
    lenient: list = []
    rf = load_rows(tmp_path / "rows.yaml", lenient)
    assert not rf.rows and len(lenient) == 1 and "kind anchor counts no period" in lenient[0], lenient
    with pytest.raises(ValueError, match="kind anchor counts no period"):
        load_rows(tmp_path / "rows.yaml")


def test_a_trigger_deadline_of_kind_anchor_with_a_period_fails_c21():
    from tenderpack.amend import DeadlineRule, deadline_rule_problem
    d = DeadlineRule(kind="anchor", anchor="PDD", offset=2, unit="working_day", direction="before", text=WORDS)
    assert "kind anchor counts no period" in (deadline_rule_problem(d) or "")
    assert deadline_rule_problem(DeadlineRule(kind="relative", anchor="PDD", offset=2, unit="working_day",
                                              direction="before", text=WORDS)) is None


def test_the_register_never_plans_a_trigger_deadline_on_the_anchor():
    from tenderpack.register import trigger_deadline_rule
    rule, why = trigger_deadline_rule("TRIGGER-X", {"kind": "anchor", "anchor": "PDD", "offset": 2,
                                                   "unit": "working_day", "direction": "before", "text": WORDS}, "ADD-03:7.1")
    assert rule is None and "kind anchor counts no period" in why


# ---------------------------------------------------------------------------------------------- downstream proposals

import s12_w3b as W                                                       # noqa: E402
from tenderpack.ai import downstream as DS                                # noqa: E402
from tenderpack.ai.contract import EvidenceRef                            # noqa: E402

NOTICE = {"id": "ADD-03-7.3-91", "group": "ADD-03:7.3", "scope": ["submission", "portal"],
          "requirement": "Portal notice (session 13 test data)", "units": ["ADD-03:7.3"], "discipline": "Technical",
          "assessment": "procedural", "evidence": [], "no_deliverable": "a Portal notice (test data)",
          "interpretations": [{"stage": "ADD-03",
                               "quote": "not later than three (3) Working Days before the Proposal Due Date"}],
          "date_rules": [{"rule_id": "ADD-03-7.3-91-R1", "kind": "anchor", "purpose": "deadline", "anchor": "PDD",
                          "offset": 3, "unit": "working_day", "direction": "before", "source_unit": "ADD-03:7.3",
                          "text": "not later than three (3) Working Days before the Proposal Due Date"}],
          "confidence": "medium", "confidence_reason": "test data"}


@pytest.fixture(scope="module")
def ws(tmp_path_factory):
    return W.workspace(tmp_path_factory)


def test_a_downstream_row_with_an_anchor_rule_and_a_period_is_invalid_with_the_reason(ws):
    prom = W.promoted(ws)
    ev = EvidenceRef(doc="ADD-03", unit_id="ADD-03:7.3", page=3, kind="span",
                     words="not later than three (3) Working Days before the Proposal Due Date")
    ds = W.dset(ws, [{"id": "R1", "statement_type": "row_new", "task": "date:ADD-03:7.3", "provision": "ADD-03:7.3",
                      "payload": {"row": copy.deepcopy(NOTICE)}, "evidence": [ev]}])
    DS.validate(ws, ds, prom, {"date:ADD-03:7.3": "computed_date"})
    it = ds.items[0]
    assert it.verification_status == "invalid", it.verification_status
    assert any(not v.ok and "kind anchor counts no period" in v.detail for v in it.validation), \
        [v.detail for v in it.validation]
