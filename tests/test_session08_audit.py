"""Session 08 audit findings, reproduced before the fixes (disposable data only).

1. Rejecting ADD-02/3.1, rebuilding and rejecting it again must never make the rejected amendment apply.
2. Changing an old member row of the evaluation table must void a decision on the table's replacement.
3. An obligation inserted after an existing clause needs its own A1 coverage; the anchor's row is not enough.
4. A one-Working-Day task with a Friday or holiday deadline gets a valid working window or an explicit
   conflict, and the legal deadline is never moved.

Decisions are written only to disposable files by "Fixture Test Reviewer"; nothing in the repository is
accepted, rejected or applied.
"""
from __future__ import annotations

import copy
from datetime import date, timedelta
from pathlib import Path

import pytest
import yaml

from tenderpack import review, stage2
from tenderpack.dates import Calendar
from tenderpack.schedule import backward_pass
from tenderpack.trace import obligation_trace
from tenderpack.util import ROOT

EVIDENCE, PACK = ROOT / "build", ROOT / "config/pack.yaml"
WHO = "Fixture Test Reviewer"


def _pack_with_decisions(tmp_path, decisions):
    cfg = yaml.safe_load(PACK.read_text())
    cfg["decisions"] = str(decisions)
    p = tmp_path / "pack.yaml"
    p.write_text(yaml.safe_dump(cfg))
    return p


def _stage(r, name):
    return next(s for s in r["stages"] if s.stage == name)


def _table_replaced(r) -> bool:
    return _stage(r, "ADD-02").state["VOL-I:T1-1/B"].status == "superseded"


# ---------------------------------------------------------------------------------------------- 1

def test_reject_rebuild_reject_never_applies_the_rejected_op(tmp_path):
    dec = tmp_path / "decisions.yaml"
    pack = _pack_with_decisions(tmp_path, dec)
    r = stage2.run(EVIDENCE, pack, ROOT)
    assert _table_replaced(r)                                              # proposed: applied in the working draft
    assert review.decide(r, ["ADD-02/3.1"], "reject", WHO, "fixture: first rejection", dec)[0] == 0
    r2 = stage2.run(EVIDENCE, pack, ROOT)
    assert not _table_replaced(r2)
    st2 = r2["reviews"][("op", "ADD-02/3.1")]
    assert st2["status"] == "rejected", review.label(st2)                  # the rejection still matches what was reviewed
    code, msgs = review.decide(r2, ["ADD-02/3.1"], "reject", WHO, "fixture: rejected again", dec)
    assert code == 0, msgs
    assert yaml.safe_load(dec.read_text())["decisions"][0]["fingerprint"] == \
        yaml.safe_load(dec.read_text())["decisions"][1]["fingerprint"]      # same subject both times
    for _ in range(2):                                                    # rebuild twice more
        r3 = stage2.run(EVIDENCE, pack, ROOT)
        assert not _table_replaced(r3), "a rejected amendment applied after a rebuild"
        assert r3["reviews"][("op", "ADD-02/3.1")]["status"] == "rejected"
        assert _stage(r3, "ADD-02").status == "PARTIAL" and r3["validated"].stage == "ADD-01"
    # rejection, structural failure and pending review stay distinct
    x = next(x for x in _stage(r3, "ADD-02").ops if x.op.id == "ADD-02/3.1")
    assert x.valid and x.withdrawn and not x.applied                     # structurally valid, withdrawn by a person
    cov = next(c for c in _stage(r3, "ADD-02").coverage if c["provision"] == "ADD-02:3.1")
    assert cov["disposition"] == "rejected"


def test_a_changed_rejection_still_withholds_the_op(tmp_path):
    """A rejection made against a different subject is shown as needing review again, and the op stays out."""
    dec = tmp_path / "decisions.yaml"
    pack = _pack_with_decisions(tmp_path, dec)
    r = stage2.run(EVIDENCE, pack, ROOT)
    assert review.decide(r, ["ADD-02/3.1"], "reject", WHO, "fixture", dec)[0] == 0
    data = yaml.safe_load(dec.read_text())
    data["decisions"][0]["fingerprint"] = "0" * 64                         # as if the subject changed since
    dec.write_text(yaml.safe_dump(data))
    r2 = stage2.run(EVIDENCE, pack, ROOT)
    st = r2["reviews"][("op", "ADD-02/3.1")]
    assert st["status"] == "changed" and st["decision"] == "reject"
    assert not _table_replaced(r2)
    assert "still withheld" in review.label(st)


# ---------------------------------------------------------------------------------------------- 2

def test_a_changed_old_member_row_voids_the_replacement_decision(tmp_path):
    dec = tmp_path / "decisions.yaml"
    pack = _pack_with_decisions(tmp_path, dec)
    r = stage2.run(EVIDENCE, pack, ROOT)
    assert review.decide(r, ["ADD-02/3.1"], "accept", WHO, "fixture", dec)[0] == 0
    same = copy.deepcopy(r)
    same["decisions"] = review.load_decisions(dec)
    stage2.evaluate(same)
    assert same["reviews"][("op", "ADD-02/3.1")]["status"] == "accepted"
    for uid in ("VOL-I:T1-1/B", "ADD-02:T1-1-rev/D"):                     # an old member row; a replacement row
        r2 = copy.deepcopy(r)
        r2["decisions"] = review.load_decisions(dec)
        u = next(u for u in r2["units"] if u["unit_id"] == uid)
        u["cells"]["Marks"] = str(int(u["cells"]["Marks"]) + 1)
        u["text"] = " | ".join(f"{k}: {v}" for k, v in u["cells"].items())
        stage2.evaluate(r2)
        assert r2["reviews"][("op", "ADD-02/3.1")]["status"] == "changed", uid
        assert uid in r2["reviews"][("op", "ADD-02/3.1")]["binding"]["before"]


# ---------------------------------------------------------------------------------------------- 3

def test_an_inserted_obligation_needs_its_own_row_not_the_anchors(tmp_path):
    r = stage2.run(EVIDENCE, PACK, ROOT)
    assert not [t for t in obligation_trace(r) if t["op"] == "ADD-02/7.1" and t["output"] == "A1"]
    r2 = copy.deepcopy(r)
    x = next(x for x in _stage(r2, "ADD-02").ops if x.op.id == "ADD-02/7.1")
    inserted = set(x.changed) | {x.op.provision}
    keep_anchor = [e for e in r2["evals"] if x.op.anchor in e["row"].units]
    assert keep_anchor                                                   # the anchor clause has rows of its own
    r2["evals"] = [e for e in r2["evals"]
                   if not (set(e["row"].units) & inserted or any(u.startswith("ADD-02:F4-G") or u.startswith("ADD-02:7")
                                                                for u in e["row"].units))]
    found = [t for t in obligation_trace(r2) if t["op"] == "ADD-02/7.1" and t["output"] == "A1"]
    assert found, "the anchor's existing row satisfied the coverage of a newly inserted obligation"


# ---------------------------------------------------------------------------------------------- 4

def _next(weekday: int, start=date(2026, 11, 1)) -> date:
    return start + timedelta(days=(weekday - start.weekday()) % 7)


@pytest.mark.parametrize("dur", [0, 1, 2])
def test_a_friday_deadline_gets_a_working_window_and_keeps_the_legal_date(dur):
    cal = Calendar()                                                     # Fri/Sat weekend (VOL-I 2.4)
    fri = _next(4)
    res = backward_pass({"t": {"duration_wd": dur, "predecessors": [], "deadline_date": fri, "deadline_rule": "X"}}, cal)
    t = res["t"]
    assert cal.is_working_day(t["lf"]) and t["lf"] <= fri
    assert cal.is_working_day(t["ls"]) and t["ls"] <= t["lf"]
    assert cal.working_days_between(t["ls"], t["lf"]) + 1 == max(dur, 1)  # the window holds the whole duration
    assert t["deadline"] == fri                                          # the legal deadline is not moved
    assert t["deadline_nonworking"]


def test_a_holiday_deadline_gets_a_working_window():
    thu = _next(3)
    cal = Calendar(holidays=frozenset({thu}))
    res = backward_pass({"t": {"duration_wd": 1, "predecessors": [], "deadline_date": thu, "deadline_rule": "X"}}, cal)
    assert res["t"]["lf"] == thu - timedelta(days=1) and res["t"]["ls"] == res["t"]["lf"]
    assert res["t"]["deadline"] == thu


def test_no_working_window_is_an_explicit_conflict():
    """Status date on the Friday deadline itself: the last Working Day before it has passed; the activity is
    flagged, its legal deadline is still the Friday, and nothing is compressed."""
    from tenderpack.schedule import window_flags
    cal = Calendar()
    fri = _next(4)
    res = backward_pass({"t": {"duration_wd": 1, "predecessors": [], "deadline_date": fri, "deadline_rule": "X"}}, cal)
    flags = window_flags(res["t"], status_date=fri, cal=cal)
    assert any(f.startswith("NO WORKING WINDOW") for f in flags), flags
    assert res["t"]["deadline"] == fri


# ---------------------------------------------------------------------------------------------- approvals (S08 §2)

def test_approval_records_versions_and_shows_differences_before_extending(tmp_path, capsys):
    """Disposable copies only: an approval records the reading file version, a snapshot, the confirmation record and
    the scope; a changed reading is never approved silently: its differences are shown and nothing is written until
    the reviewer confirms having seen them."""
    import shutil
    from tenderpack.cli import approve
    readings = tmp_path / "readings"
    shutil.copytree(ROOT / "curation/readings", readings)
    cfg = yaml.safe_load(PACK.read_text())
    cfg["readings_dir"] = str(readings)
    (tmp_path / "pack.yaml").write_text(yaml.safe_dump(cfg))
    appr = tmp_path / "reviews/approvals.yaml"
    assert approve("VOL-II-p3-r1", WHO, "fixture", ROOT, tmp_path / "pack.yaml", appr, record="fixture record",
                   resolutions=["fixture resolution"], keeps_open=["fixture open point"],
                   not_covered=["register interpretations"]) == 0
    e = yaml.safe_load(appr.read_text())["approvals"][0]
    assert e["date"] == date.today().isoformat() and e["confirmation_record"] == "fixture record"
    assert e["reading_file"]["sha256"] and Path(e["reading_file"]["snapshot"]).is_file()
    assert Path(e["reading_file"]["snapshot"]).is_relative_to(tmp_path)                 # the repository is untouched
    assert e["keeps_open"] == ["fixture open point"] and e["does_not_cover"] == ["register interpretations"]
    # change one cell in the disposable reading: approval is not extended silently
    f = readings / "VOL-II-p3-r1.yaml"
    f.write_text(f.read_text().replace('limit: "5", basis', 'limit: "6", basis'))
    capsys.readouterr()
    assert approve("VOL-II-p3-r1", WHO, None, ROOT, tmp_path / "pack.yaml", appr) == 3
    out = capsys.readouterr().out
    assert "table.rows[TN].cells.limit: '5' -> '6'" in out
    assert len(yaml.safe_load(appr.read_text())["approvals"]) == 1                     # nothing written
    assert approve("VOL-II-p3-r1", WHO, None, ROOT, tmp_path / "pack.yaml", appr, confirm_changes=True) == 0
    assert len(yaml.safe_load(appr.read_text())["approvals"]) == 2
