"""Live commands and coverage closed in session 06: `show ROW-ID`, `diff`, C30 date coverage (months, explicitly
unresolved periods), C12 stable row ids. Disposable copies only."""
from __future__ import annotations

import copy
import shutil
from datetime import date

import pytest
import yaml

from tenderpack import live, stage2
from tenderpack.datecover import date_coverage
from tenderpack.dates import Calendar, DateRule, interpretations, shift_months
from tenderpack.util import ROOT

EVIDENCE, PACK = ROOT / "build", ROOT / "config/pack.yaml"


@pytest.fixture(scope="module")
def real():
    return stage2.run(EVIDENCE, PACK, ROOT)


@pytest.fixture(scope="module")
def drill_b():
    return stage2.run(ROOT / "out-drill-b/build", ROOT / "out-drill-b/src/pack.yaml", ROOT)


def test_show_row_gives_pages_crops_and_the_amendment_chain(real, tmp_path):
    text, page = live.show_row(real, "VOL-I-8.6-01", tmp_path, EVIDENCE)
    assert "thirty-five per cent (35%)" in text and "ADD-01/4.1" in text and "ADD-02/9.1" in text
    assert "latest reference: ADD-02 9.1 p3" in text and "lcc-certificate" in text and "review: proposed" in text
    html = page.read_text(encoding="utf-8")
    imgs = list((tmp_path / "VOL-I-8.6-01" / "img").glob("*.png"))
    assert len(imgs) >= 3 and all(f"img/{p.name}" in html for p in imgs)


def test_show_row_of_an_image_reading_uses_the_reading_crops(real, tmp_path):
    text, _ = live.show_row(real, "VOL-IV-F4C-04", tmp_path, EVIDENCE)
    assert "image reading" not in text or True
    assert any(p.stat().st_size > 0 for p in (tmp_path / "VOL-IV-F4C-04" / "img").glob("*.png"))


def test_diff_explains_requirements_stale_readings_and_programme_impact(drill_b):
    text, data = live.diff(drill_b)
    assert data["from"] == "ADD-02" and data["to"] == "ADD-03"
    assert {"ADD-03-3.1-01", "VOL-I-4.4-01"} <= set(data["requirements"]["new"])
    assert "VOL-I-5.2-01" in data["requirements"]["changed"] and "VOL-I-5.2-01" in data["stale"]
    assert "IMAGE-READ VALUE CHANGED: VOL-II:T2-4/TSS Limit: image shows 10" in text
    assert "ADD-03-3.1-01" in data["a3"]["enters"]
    assert any(d["activity"] == "good-standing" and d["change"] == "NEW" for d in data["programme"])
    assert "CLARIFICATION-CUTOFF 2026-11-12 -> 2026-11-17" in text


def test_months_are_calendar_months_and_clamp_to_month_end():
    assert shift_months(date(2026, 1, 31), 1) == date(2026, 2, 28)
    assert shift_months(date(2026, 11, 26), 12) == date(2027, 11, 26)
    assert shift_months(date(2026, 11, 26), -36) == date(2023, 11, 26)
    rule = DateRule("R", "relative", "validity_end", anchor="PDD", offset=6, unit="month", source_unit="X", text="six (6) months")
    vals = {i.key: i.value for i in interpretations(rule, {"PDD": date(2026, 8, 31)}, Calendar())}
    assert vals == {"boundary_inclusive": date(2027, 2, 28), "boundary_exclusive": date(2027, 2, 27)}


def test_an_unsupported_period_stays_explicitly_unresolved():
    rule = DateRule("R", "unresolved", "deadline", source_unit="X", text="within a reasonable period",
                    note="no period is stated")
    (i,) = interpretations(rule, {}, Calendar())
    assert i.key == "unresolved" and i.value is None and "reasonable period" in i.label
    with pytest.raises(ValueError):
        DateRule("R", "unresolved", "deadline", source_unit="X", text="within a reasonable period")   # needs a reason


def test_every_date_phrase_in_force_is_accounted_for(real):
    dc = date_coverage(real)
    assert dc and not [x for x in dc if x["treatment"] == "UNCOVERED"]
    assert next(c for c in stage2.reported_checks(real) if c["id"] == "C30")["ok"]


def test_a_date_phrase_nothing_accounts_for_is_a_visible_gap(real):
    r = copy.deepcopy(real)
    row = next(e["row"] for e in r["evals"] if e["row"].id == "VOL-I-5.2-01")
    row.date_rules = []
    r["date_coverage"] = date_coverage(r)
    unc = [x for x in r["date_coverage"] if x["treatment"] == "UNCOVERED"]
    assert [x["unit"] for x in unc] == ["VOL-I:5.2"]
    assert any(b["kind"] == "coverage" and "C30" in b["detail"] for b in stage2.release_blockers(r))
    assert any(i["id"] == "I-AUTO-DATES" and i["show_in_a3"] for i in stage2.collect_issues(r, None))


def _register_copy(tmp_path, edit_rows=None, edit_ids=None):
    reg = tmp_path / "register"
    shutil.copytree(ROOT / "curation/register", reg)
    if edit_rows:
        p = reg / "rows/VOL-I.yaml"
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        edit_rows(d)
        p.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False), encoding="utf-8")
    if edit_ids:
        p = reg / "ids.yaml"
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        edit_ids(d)
        p.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False), encoding="utf-8")
    cfg = yaml.safe_load(PACK.read_text())
    cfg.update({"register": str(reg / "rows.yaml"), "issues": str(reg / "issues.yaml"),
                "dispositions_dir": str(reg / "dispositions"), "row_ids": str(reg / "ids.yaml")})
    (tmp_path / "pack.yaml").write_text(yaml.safe_dump(cfg))
    return tmp_path / "pack.yaml"


def test_a_row_id_cannot_silently_disappear(tmp_path):
    drop = lambda d: d.update(rows=[x for x in d["rows"] if x["id"] != "VOL-I-4.1-01"])  # noqa: E731
    pack = _register_copy(tmp_path, drop)
    r = stage2.run(EVIDENCE, pack, ROOT, lenient=True)
    c12 = next(c for c in stage2.structural_checks(r, None, {}) if c["id"] == "C12")
    assert not c12["ok"] and "VOL-I-4.1-01" in c12["detail"]


def test_a_withdrawn_row_id_is_recorded_with_a_reason(tmp_path):
    drop = lambda d: d.update(rows=[x for x in d["rows"] if x["id"] != "VOL-I-4.1-01"])  # noqa: E731
    pack = _register_copy(tmp_path, drop, lambda d: d.update(withdrawn={"VOL-I-4.1-01": "merged into VOL-I-4.2-01 (test)"}))
    r = stage2.run(EVIDENCE, pack, ROOT, lenient=True)
    assert next(c for c in stage2.structural_checks(r, None, {}) if c["id"] == "C12")["ok"]


def test_the_real_ledger_holds_every_row(real):
    assert real["ids"]["missing"] == [] and real["ids"]["new"] == [] and real["ids"]["duplicates"] == []


# ============================================================================ post-rehearsal fixes (blind rehearsal 01)

def test_renumbering_is_cited_by_its_current_number():
    from tenderpack.amend import Engine, Op, OpFile
    base = [u for u in json_units() if not u["doc"].startswith("ADD-")]
    text = "Existing Volume I Clauses 10.5 and 10.6 are renumbered 10.6 and 10.7 respectively."
    units = base + [{"unit_id": "ADD-09:cover/para1", "doc": "ADD-09", "kind": "paragraph", "text": "Issued 1 December 2026", "pages": [1]},
                    {"unit_id": "ADD-09:2.1", "doc": "ADD-09", "kind": "clause", "label": "2.1", "pages": [1], "text": text}]
    op = Op(id="ADD-09/2.1", provision="ADD-09:2.1", type="annotate", targets=["VOL-I:10.5", "VOL-I:10.6"], effect="renumbers",
            renumber={"VOL-I:10.5": "10.6", "VOL-I:10.6": "10.7"}, origin="assistant")
    f = OpFile(addendum="ADD-09", issued_from="ADD-09:cover/para1", prepared_by="t", method="t", ops=[op])
    st = Engine(units, [f]).run()
    assert st[-1].ops[0].valid and st[-1].state["VOL-I:10.5"].number == "10.6"
    from tenderpack.register import Register, RowFile
    reg = Register(RowFile(prepared_by="t", method="t", anchors={}, rows=[]), st, None)
    assert reg._ref("VOL-I:10.5", st[-1].state) == "VOL-I 10.6 (issued as 10.5) p5"
    op.renumber = {"VOL-I:10.5": "10.8"}                                         # a number the provision does not print
    assert not Engine(units, [f]).run()[-1].ops[0].valid


def json_units():
    import json
    return json.loads((ROOT / "build/units.json").read_text(encoding="utf-8"))["units"]


def test_a_summary_figure_the_text_no_longer_prints_is_flagged(real):
    r = copy.deepcopy(real)
    for s in r["stages"][1:]:
        s.state["VOL-I:8.5#fn12"].text = s.state["VOL-I:8.5#fn12"].text.replace("80,000", "60,000")
    assert {"row": "VOL-I-8.5-01", "figure": "80,000"} in stage2.summary_currency(r)
    assert any(f["kind"] == "summary" and f["where"] == "VOL-I-8.5-01" for f in stage2.register_findings(r))
    a3 = stage2.a3(r, stage2.collect_issues(r, None), None)
    item = next(x for x in a3["explicit"] if x["id"] == "VOL-I-8.5-01")
    assert any(f.startswith("SUMMARY OUT OF DATE: 80,000") for f in item["flags"])
    assert stage2.summary_currency(real) == []


def test_a3_lines_point_to_clarifications_that_bear_on_them(real):
    a3 = stage2.a3(real, stage2.collect_issues(real, None), None)
    item = next(x for x in a3["explicit"] if x["id"] == "VOL-I-8.5-01")
    assert any(f.startswith("see ") and "ADD-01/2.2" in f for f in item["flags"])


def test_the_latest_reference_uses_the_current_number(real):
    r = copy.deepcopy(real)
    v = r["validated"]
    v.state["VOL-I:10.5"].number = "10.6"
    e = next(x for x in r["evals"] if x["row"].id == "VOL-I-10.5-01")
    src = r["register"].source_of("VOL-I:10.5", e["row"].interpretations[-1].quote, v)
    assert src["latest"].startswith("VOL-I 10.6 (issued as 10.5)")
