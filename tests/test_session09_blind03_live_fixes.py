"""Session 09, blind rehearsal 03: the tool gaps the host-route proposer hit, fixed live before the curation (logged in
rehearsals/blind-03/clock.txt). Synthetic texts; the blind-03 evidence build is used only for the engine checks."""
from __future__ import annotations

import datetime as dt
import json

import pytest

from tenderpack import amend
from tenderpack.amend import Disposition, Engine, Op, OpFile, load_opfile
from tenderpack.citations import citations, resolve, verify_target
from tenderpack.dates import Calendar
from tenderpack.register import Register, load_rows
from tenderpack.util import ROOT, load_yaml

B = ROOT / "rehearsals/blind-03"


# ---------------------------------------------------------------------------- a form an addendum inserted is citable

def test_a_form_that_an_addendum_inserted_resolves_under_the_addendum():
    ids = {"ADD-02:F4-G/T1/1", "ADD-02:F4-G/para1", "ADD-03:F4-G/T1/1", "VOL-IV:F4-A/para1"}
    text = "Form 4-G, added to Volume IV by Section 7 of Addendum No. 2, is deleted and replaced by the reissued Form 4-G"
    got = resolve(citations(text), ids)
    assert "ADD-02:F4-G" in got and "ADD-03:F4-G" in got and "VOL-IV:F4-G" not in got
    assert verify_target("ADD-02:F4-G", text, ids)[0]
    assert resolve(citations("Form 4-A is reissued"), ids) == ["VOL-IV:F4-A"]      # a Volume IV form stays itself


# ---------------------------------------------------------------------------- Arabic words match without diacritics

AR_ISSUED = "رابعاً: أن جميع المعلومات المقدمة في هذا العرض صحيحة وكاملة"
AR_PLAIN = "رابعا: ان جميع المعلومات المقدمة في هذا العرض صحيحة وكاملة"      # no tanween, plain alef


def test_arabic_old_words_are_found_and_replaced_whatever_the_diacritics():
    assert amend._contains(AR_ISSUED, AR_PLAIN) == 1 and amend._contains(AR_PLAIN, AR_ISSUED) == 1
    assert amend._quoted_in("The declaration " + AR_ISSUED + " is deleted", AR_PLAIN)
    new = "رابعاً: نص جديد"
    out = amend._replace_once("Intro. " + AR_ISSUED + " End.", AR_PLAIN, new)
    assert out == "Intro. " + new + " End."
    assert amend._replace_once("nothing Arabic here", AR_PLAIN, new) == "nothing Arabic here"
    assert amend._arabic_span("x " + AR_ISSUED, AR_PLAIN) == (2, 2 + len(AR_ISSUED))


# ---------------------------------------------------------------------------- a notified non-working day

@pytest.fixture(scope="module")
def units():
    return json.load(open(B / "build/units.json", encoding="utf-8"))["units"]


def _stages(units, extra_ops, dispositions=()):
    files = [load_opfile(B / "work/amendments" / f"{a}.yaml") for a in ("ADD-01", "ADD-02")]
    f = OpFile(addendum="ADD-03", issued_from="ADD-03:cover/para1", prepared_by="test", method="test",
               ops=extra_ops, dispositions=list(dispositions))
    return Engine(units, files + [f], set()).run()


def test_a_day_an_addendum_notifies_is_non_working_from_that_stage(units):
    prov = next(u for u in units if u["unit_id"] == "ADD-03:2.2")
    assert "22 November 2026" in prov["text"]
    op = Op(id="ADD-03/2.2", provision="ADD-03:2.2", type="annotate", targets=["ADD-03:2.2"], effect="non_working_day",
            date="2026-11-22", origin="assistant", review="proposed")
    stages = _stages(units, [op])
    x = next(r for r in stages[-1].ops if r.op.id == "ADD-03/2.2")
    assert x.valid and x.details["non_working_day"] == "2026-11-22"
    assert stages[-1].non_working_days == ["2026-11-22"] and stages[-2].non_working_days == []
    reg = Register(load_rows(B / "work/register/rows.yaml"), stages, Calendar(), "conservative")
    assert reg.cal_by_stage["ADD-02"].is_working_day(dt.date(2026, 11, 22))
    assert not reg.cal_by_stage["ADD-03"].is_working_day(dt.date(2026, 11, 22))
    # the date rules of that stage count it: four Working Days before Thursday 26 November skip Sunday the 22nd
    assert reg.cal_by_stage["ADD-03"].add_working_days(dt.date(2026, 11, 26), -4) == dt.date(2026, 11, 19)
    assert reg.cal_by_stage["ADD-02"].add_working_days(dt.date(2026, 11, 26), -4) == dt.date(2026, 11, 22)
    # a wrong date is refused (C21): the day must be the one the provision prints
    bad = op.model_copy(update={"date": "2026-11-23"})
    y = next(r for r in _stages(units, [bad])[-1].ops if r.op.id == "ADD-03/2.2")
    assert not y.valid and any(c["id"] == "C21" and not c["ok"] for c in y.checks)


def test_calendar_with_days_is_pure():
    c = Calendar()
    d = c.with_days(["2026-11-22"])
    assert d is not c and c.is_working_day(dt.date(2026, 11, 22)) and not d.is_working_day(dt.date(2026, 11, 22))
    assert c.with_days([]) is c


# ---------------------------------------------------------------------------- `pin --rows` after the calendar change

def test_pin_rows_builds_the_register_with_the_packs_calendar(monkeypatch):
    """Found by the blind-03 curator (10:56): after the non-working-day fix the register needs a calendar, and
    `pin --rows` passed None (AttributeError on `with_days`). The command now builds the pack's own calendar.
    Nothing is written: the pin writer is replaced for the test."""
    from tenderpack import cli, register
    written = {}
    monkeypatch.setattr(register, "write_pins", lambda rf, path, header: written.setdefault("path", path))
    rf = register.load_rows(ROOT / "curation/register/rows.yaml")
    row = next(r for r in rf.rows if r.interpretations)
    rc = cli.pin_cmd(ROOT / "build", ROOT / "config/pack.yaml", refresh=False, only=f"{row.id}@{row.interpretations[0].stage}")
    assert rc == 0 and written["path"] == register.pins_path(ROOT / "curation/register/rows.yaml")


# ---------------------------------------------------------------------------- the controller's evidence rule

def test_a_whole_cell_value_is_evidence_however_short_and_an_approved_reading_amended_is_not_a_conflict(tmp_path):
    from tenderpack.ai import controller as C
    from tenderpack.ai.contract import EvidenceRef
    from tests.fixtures.ai_fixture import workspace
    ws = workspace(tmp_path)
    r = ws.r
    st = next(s for s in r["stages"] if s.stage == "ADD-02").state
    row = next(u for u in st.values() if u.doc == "VOL-II" and u.kind == "table_row" and u.cells
               and u.unit_id.startswith("VOL-II:T2-4/") and (u.cells.get("Limit") or "").strip().isdigit())
    col, val = "Limit", row.cells["Limit"].strip()
    ok = C.check_ref(ws, st, EvidenceRef(doc="VOL-II", unit_id=row.unit_id, page=row.pages[0], kind="cell", words=val,
                                         cell={"row_key": row.label, "column": col}), "ADD-02")
    assert ok.ok, ok.detail
    short = C.check_ref(ws, st, EvidenceRef(doc="VOL-II", unit_id=row.unit_id, page=row.pages[0], kind="span", words="5"),
                        "ADD-02")
    assert not short.ok and "too short" in short.detail
    assert "approved reading" not in C.__doc__.split("conflicting")[1].split("escalated")[0]
