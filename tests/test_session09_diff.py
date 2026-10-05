"""Session 09, finding C: `tenderpack diff` compared only a row's primary unit (its text, status and quote), so in blind
rehearsal 02 the rows VOL-II-2.1-01 and VOL-II-3.1-01, which cite the Table 2-2 rows that ADD-03/6.1 replaces, were
not listed as changed. Every unit a row cites is now compared (status, text, cells, effective replacement,
annotations) and reported as "secondary unit ... replaced by ADD-03/6.1". Read-only: nothing is written.
"""
from __future__ import annotations

import pytest

from tenderpack import live, stage2
from tenderpack.amend import UState
from tenderpack.util import ROOT

T22 = ["bod5", "cod", "total-suspended-solids", "total-nitrogen", "total-phosphorus", "temperature"]
HEADINGS = ["# What changed from", "## Requirements", "## Stale readings and decisions",
            "## Obligations not reaching the outputs (C46)", "## Disqualifiers (A3)", "## Programme impact"]


@pytest.fixture(scope="module")
def real():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


@pytest.fixture(scope="module")
def blind02(blind02_run):
    """Blind rehearsal 02 on a fresh, disposable ingest of its pack (tests/conftest.py)."""
    return blind02_run


def _line(text, rid):
    return next(x for x in text.splitlines() if x.startswith(f"- CHANGED {rid}:"))


def _without_secondary(monkeypatch, r, frm, to):
    """What diff printed before session 09 (the primary unit only), for comparison."""
    with monkeypatch.context() as m:
        m.setattr(live, "_secondary", lambda row, sa, sb: ([], []))
        return live.diff(r, frm, to)


def test_blind_02_rows_citing_the_replaced_table_2_2_rows_are_changed(blind02, monkeypatch):
    old_text, old = _without_secondary(monkeypatch, blind02, "ADD-02", "ADD-03")
    assert not {"VOL-II-2.1-01", "VOL-II-3.1-01"} & set(old["requirements"]["changed"])     # the finding, reproduced
    text, data = live.diff(blind02, "ADD-02", "ADD-03")
    assert {"VOL-II-2.1-01", "VOL-II-3.1-01"} <= set(data["requirements"]["changed"])
    for rid in ("VOL-II-2.1-01", "VOL-II-3.1-01"):
        line = _line(text, rid)
        assert "secondary units " + ", ".join(f"VOL-II:T2-2/{k}" for k in T22) + " replaced by ADD-03/6.1" in line, line
        assert "ADD-03:T2-2-rev/total-nitrogen" in line and line.endswith("(by ADD-03/6.1)")
        assert data["requirements"]["secondary"][rid]
    assert "secondary unit ADD-03:T2-2-rev/ammonia-nitrogen-nh4-n issued" in _line(text, "VOL-II-2.1-01")
    f4f = _line(text, "VOL-IV-F4F-01")                                   # two form rows deleted inside a kept form
    assert "secondary unit VOL-IV:F4-F/model-auditor deleted by ADD-03/4.3(a)" in f4f
    # nothing reported before is lost, and the headings and line format are the same
    assert set(old["requirements"]["changed"]) <= set(data["requirements"]["changed"])
    for h in HEADINGS:
        assert any(x.startswith(h) for x in text.splitlines()), h
    # session 12 (W3a): a row with no change of its own is listed CONFIRMED (unchanged) or NOT SETTLED; with its secondary
    # units it can move from that line to a CHANGED line, so those lines are compared with the CHANGED ones
    moved_lines = ("- CHANGED", "- new:", "- CONFIRMED (unchanged)", "- NOT SETTLED")
    assert [x for x in old_text.splitlines() if not x.startswith(moved_lines)] == \
        [x for x in text.splitlines() if not x.startswith(moved_lines)]


def test_real_pack_add_01_to_add_02_changes_only_by_genuine_secondary_units(real, monkeypatch):
    old_text, old = _without_secondary(monkeypatch, real, "ADD-01", "ADD-02")
    text, data = live.diff(real, "ADD-01", "ADD-02")
    sec = data["requirements"]["secondary"]
    # the rows whose cited units genuinely changed at ADD-02 besides their first unit (session 09 report). Session 12
    # (W3a, deliberate): VOL-I-9.4-01's secondary unit is only annotated by ADD-02/Q9, labelled `confirms`: a confirmation
    # is not a change (blind-04 follow-up 6, blind-05 follow-up 10), so the row is listed CONFIRMED (unchanged) with the
    # annotation and the op, not CHANGED
    assert set(sec) == {"ADD-01-AppA-01", "VOL-II-3.1-01", "VOL-V-29.3-01"}, sec
    assert "secondary unit VOL-II:T2-4/TN amended by ADD-02/5.1 (Limit: 5 -> 3)" in _line(text, "VOL-V-29.3-01")
    conf = next(x for x in text.splitlines() if x.startswith("- CONFIRMED (unchanged) VOL-I-9.4-01:"))
    assert "secondary unit VOL-IV:F4-C/image annotated by ADD-02/Q9" in conf and "VOL-I-9.4-01" in data["requirements"]["confirmed"]
    assert "secondary unit VOL-II:H:S3 annotated by ADD-02/5.2" in _line(text, "VOL-II-3.1-01")
    assert "secondary unit ADD-02:cover/para3 issued" in _line(text, "ADD-01-AppA-01")
    # every other line is exactly as before
    # session 12 (W3a): without its secondary units a row may read CONFIRMED (unchanged); that line moves with it
    changed_lines = {f"{h} {rid}:" for rid in sec for h in ("- CHANGED", "- CONFIRMED (unchanged)", "- NOT SETTLED")}
    keep = lambda t: [x for x in t.splitlines() if not x.startswith(tuple(changed_lines)) and not x.startswith("- new:")]  # noqa: E731
    assert keep(old_text) == keep(text)
    assert set(data["requirements"]["changed"]) - set(old["requirements"]["changed"]) <= set(sec)


# ---------------------------------------------------------------------------------------------- unit level

def _u(uid, text="Limit: 5", status="active", cells=None, **kw):
    return UState(unit_id=uid, doc=uid.split(":")[0], kind="table_row", status=status, text=text, cells=cells, pages=[2],
                  origin="text_layer", reading_status=None, **kw)


def test_unit_changes_cover_status_cells_replacement_and_annotations():
    a = {"V:T/x": _u("V:T/x", cells={"Limit": "5"}), "A:T/x": _u("A:T/x", status="not_issued")}
    b = {"V:T/x": _u("V:T/x", text="Limit: 3", cells={"Limit": "3"}, history=["A/5.1"]), "A:T/x": _u("A:T/x")}
    assert live._unit_changes(a, b, "V:T/x") == [{"unit": "V:T/x", "change": "amended", "ops": ["A/5.1"],
                                                  "detail": "Limit: 5 -> 3"}]
    assert live._unit_changes(a, b, "A:T/x") == [{"unit": "A:T/x", "change": "issued", "ops": []}]
    gone = {"V:T/x": _u("V:T/x", status="deleted", history=["A/2.1"])}
    assert live._unit_changes(a, gone, "V:T/x")[0]["change"] == "deleted"
    noted = {"V:T/x": _u("V:T/x", cells={"Limit": "5"}, annotations=["A/Q4"])}
    assert live._unit_changes(a, noted, "V:T/x") == [{"unit": "V:T/x", "change": "annotated", "ops": ["A/Q4"]}]
    assert live._unit_changes(a, a, "V:T/x") == []


def test_a_replacement_amended_later_is_seen_through_the_replaced_unit():
    a = {"V:T/x": _u("V:T/x", status="superseded", superseded_by="A:R/x", history=["A/3.1"]),
         "A:R/x": _u("A:R/x", history=["A/3.1"])}
    b = {"V:T/x": _u("V:T/x", status="superseded", superseded_by="A:R/x", history=["A/3.1"]),
         "A:R/x": _u("A:R/x", text="Limit: 2", history=["A/3.1", "B/1.1"])}
    (c,) = live._unit_changes(a, b, "V:T/x")
    assert c["change"] == "replaced earlier; its replacement A:R/x amended" and c["ops"] == ["B/1.1"]
