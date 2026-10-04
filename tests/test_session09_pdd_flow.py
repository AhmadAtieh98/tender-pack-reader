"""Session 09: the Proposal Due Date's date, time of day, timezone words and source flow from the effective text of
its defining unit (rows.yaml `anchors: PDD: {defined_in: VOL-I:6.1}`) at each stage, into A5 (milestones, README,
planning basis, activity names, marshalling, drivers, scenarios, Gantt) and the A3 subtitle. Nothing types the time.

Regression for blind rehearsal 02 (out-after-fixes): ADD-03 2.1 moved the time to 11:00, A1 showed it, but A5 and
the A3 subtitle still said 14:00 (a typed template label, `planning.delivery_cutoff_time` in the assumptions, typed
activity names, a typed A3 f-string). The real pack must read exactly as before (14:00).
Builds into disposable folders only (two builds: blind-02 and the real pack); nothing writes to the repository.
"""
from __future__ import annotations

import copy
import csv
import io
import json
from datetime import date

import pytest

from tenderpack import schedule, stage2
from tenderpack.util import ROOT

LEGACY_LABEL = ("Proposal Due Date, 14:00 Riyadh time (VOL-I 6.1 as amended by ADD-01 2.1; late Proposals rejected "
                "unopened, VOL-I 6.6)")
# The address is the Appendix 3 row's own words ({ROW:VOL-I-App3-01:address}, session 09), no longer typed in the template
LEGACY_DELIVER = ("Deliver both sealed envelopes to Tender Box 4, Ground Floor, Northern Utilities Procurement Authority, "
                  "Administrative Building C, Sakaka before 14:00 Riyadh time on the PDD (VOL-I 6.1, Appendix 3; late "
                  "Proposals are rejected unopened, VOL-I 6.6)")
LEGACY_SEAL = ("Seal Envelopes A and B separately and mark each 'NUPA/ISTP/2026/014 — NOT TO BE OPENED BEFORE 14:00 ON "
               "THE PROPOSAL DUE DATE' (VOL-I 6.2, Appendix 3)")
PLACEHOLDERS = ("{time}", "{tz}", "{date}", "{source}", "{PDD_", "{ROW:")


def _build(evidence, pack, tmp_path_factory, name):
    r = stage2.run(evidence, pack, ROOT)
    out = tmp_path_factory.mktemp(name)
    stage2.write(r, out)
    return r, out


@pytest.fixture(scope="module")
def blind02(tmp_path_factory):
    return _build(ROOT / "rehearsals/blind-02/build", ROOT / "rehearsals/blind-02/work/pack.yaml", tmp_path_factory, "b02")


@pytest.fixture(scope="module")
def real(tmp_path_factory):
    return _build(ROOT / "build", ROOT / "config/pack.yaml", tmp_path_factory, "real")


def _csv(path):
    return list(csv.DictReader(io.StringIO(path.read_text(encoding="utf-8-sig"))))


def _pdd_row(out):
    return next(m for m in _csv(out / "a5/milestones.csv") if m["id"] == "PDD")


def _readme_pdd_line(out):
    return next(x for x in (out / "a5/README.md").read_text(encoding="utf-8").splitlines()
                if x.startswith("- **") and "** Proposal Due Date, " in x)


def _acts(out, rel="a5/programme.json"):
    return {a["id"]: a for a in json.loads((out / rel).read_text(encoding="utf-8"))["rows"]}


def _no_none_or_placeholder(out):
    none_free = ("a5/milestones.csv", "a5/milestones.json", "a5/README.md")
    for f in none_free + ("a5/programme.csv", "a5/marshalling.csv", "a5/drivers.csv", "a3/a3.json"):
        t = (out / f).read_text(encoding="utf-8-sig")
        assert f not in none_free or "None" not in t, f                  # a value the pack does not state is never "None"
        assert not [p for p in PLACEHOLDERS if p in t], f                # every placeholder is filled


# ============================================================================ blind rehearsal 02: 11:00 by ADD-03 2.1

def test_blind02_anchor_details_follow_the_effective_text(blind02):
    r, _ = blind02
    d = r["anchor_details"]["ADD-03"]["PDD"]
    assert d["date"] == date(2026, 11, 26) and d["time"] == "11:00" and d["tz"] == "Riyadh time"
    assert d["unit"] == "VOL-I:6.1" and d["as_amended_by"] == ["ADD-01/2.1", "ADD-03/2.1"]
    assert d["source"] == "VOL-I 6.1 as amended by ADD-01 2.1, ADD-03 2.1"
    before = r["anchor_details"]["ADD-02"]["PDD"]
    assert before["time"] == "14:00" and before["as_amended_by"] == ["ADD-01/2.1"]
    base = r["anchor_details"]["BASE"]["PDD"]
    assert base["date"] == date(2026, 11, 12) and base["source"] == "VOL-I 6.1" and base["as_amended_by"] == []


def test_blind02_a5_milestone_readme_and_a3_read_11(blind02):
    r, out = blind02
    assert r["validated"].stage == "ADD-03"
    pdd = _pdd_row(out)
    assert pdd["time"] == "11:00" and pdd["short"] == "PDD 11:00", pdd
    assert "11:00 Riyadh time" in pdd["label"] and "ADD-03 2.1" in pdd["label"] and "14:00" not in pdd["label"]
    line = _readme_pdd_line(out)
    assert line.startswith("- **2026-11-26 11:00**") and "11:00 Riyadh time" in line and "ADD-03 2.1" in line, line
    sub = json.loads((out / "a3/a3.json").read_text(encoding="utf-8"))["subtitle"]
    assert "Proposal Due Date 2026-11-26 11:00 Riyadh time" in sub and "14:00" not in sub, sub
    basis = json.loads((out / "a5/programme.json").read_text(encoding="utf-8"))["planning_basis"]
    assert "PDD 2026-11-26 11:00" in basis and "PDD 2026-11-26 14:00" not in basis
    _no_none_or_placeholder(out)


def test_blind02_activity_names_take_the_time_and_the_marking_from_the_stage(blind02):
    _, out = blind02
    acts = _acts(out)
    assert "before 11:00 Riyadh time on the PDD" in acts["deliver"]["name"], acts["deliver"]["name"]
    assert "NOT TO BE OPENED BEFORE 11:00" in acts["seal-and-mark"]["name"], acts["seal-and-mark"]["name"]
    gantt_svg = (out / "a5/gantt.svg").read_text(encoding="utf-8")
    assert "PDD 11:00" in gantt_svg and "PDD 14:00" not in gantt_svg
    # the earlier stage still reads what the pack said then
    st = json.loads((out / "a5/stages/ADD-02.json").read_text(encoding="utf-8"))
    acts2 = {a["id"]: a for a in st["activities"]}
    assert "before 14:00 Riyadh time" in acts2["deliver"]["name"]
    assert "NOT TO BE OPENED BEFORE 14:00" in acts2["seal-and-mark"]["name"]
    ms = {m["id"]: m for m in st["milestones"]}
    assert ms["PDD"]["time"] == "14:00" and ms["PDD"]["short"] == "PDD 14:00"
    assert ms["PDD"]["label"] == LEGACY_LABEL


# ============================================================================ the real pack reads exactly as before

def test_real_pack_reads_exactly_as_before(real):
    r, out = real
    d = r["anchor_details"][r["validated"].stage]["PDD"]
    assert (d["time"], d["tz"], d["as_amended_by"]) == ("14:00", "Riyadh time", ["ADD-01/2.1"])
    assert d["source"] == "VOL-I 6.1 as amended by ADD-01 2.1"
    pdd = _pdd_row(out)
    assert (pdd["time"], pdd["short"], pdd["label"]) == ("14:00", "PDD 14:00", LEGACY_LABEL)
    assert _readme_pdd_line(out) == f"- **2026-11-26 14:00** {LEGACY_LABEL} (dated; VOL-I:6.1)"
    acts = _acts(out)
    assert acts["deliver"]["name"] == LEGACY_DELIVER and acts["seal-and-mark"]["name"] == LEGACY_SEAL
    sub = json.loads((out / "a3/a3.json").read_text(encoding="utf-8"))["subtitle"]
    assert "Proposal Due Date 2026-11-26 14:00 Riyadh time" in sub, sub
    assert "PDD 2026-11-26 14:00" in json.loads((out / "a5/programme.json").read_text(encoding="utf-8"))["planning_basis"]
    assert "PDD 14:00" in (out / "a5/gantt.svg").read_text(encoding="utf-8")
    _no_none_or_placeholder(out)


# ============================================================================ nothing types the time

def test_a_typed_cutoff_time_is_refused_as_an_assumption(real):
    r, _ = real
    assert "delivery_cutoff_time" not in r["assumptions"]["planning"]
    bad = copy.deepcopy(r["assumptions"])
    bad["planning"]["delivery_cutoff_time"] = "14:00"
    probs = [p for p in schedule.check_templates(r["templates"], bad) if "delivery_cutoff_time" in p]
    assert probs and probs[0].startswith("C45") and "pack-stated facts are derived" in probs[0] \
        and "not assumed" in probs[0]


def test_a_typed_time_in_an_activity_name_or_an_anchor_label_is_a_c45_problem(real):
    r, _ = real
    tpl = copy.deepcopy(r["templates"])
    tpl["EV-DELIVERY"][0]["name"] = "Deliver before 14:00 Riyadh time"
    assert any(p.startswith("C45: activity deliver") and "'14:00'" in p for p in schedule.check_templates(tpl, r["assumptions"]))
    tpl = copy.deepcopy(r["templates"])
    tpl["_milestones"]["labels"]["PDD"]["time"] = "14:00"
    st = r["validated"].stage
    prog = schedule.plan(st, r["evals"], tpl, r["assumptions"], r["cal"], _issued(r, st), {"PDD": "2026-11-26"},
                         anchor_details=r["anchor_details"][st])
    assert any("_milestones.labels.PDD types a time" in x for x in prog["problems"])


def _issued(r, stage):
    return date.fromisoformat(next(s for s in r["stages"] if s.stage == stage).issued)


def test_placeholders_that_cannot_be_filled_are_c45_and_never_print_none(real):
    r, _ = real
    st = r["validated"].stage
    det = copy.deepcopy(r["anchor_details"][st])
    det["PDD"]["time"] = None                                             # an amended text that states no time
    tpl = copy.deepcopy(r["templates"])
    seal = next(t for t in tpl["EV-DELIVERY"] if t["id"] == "seal-and-mark")
    seal["name"] = "Seal and mark '{ROW:VOL-I-App3-01:no_such_parameter}' {PDD_TIEM}"
    prog = schedule.plan(st, r["evals"], tpl, r["assumptions"], r["cal"], _issued(r, st), {"PDD": "2026-11-26"},
                         evidence_items=r["evidence_items"], anchor_details=det)
    probs = [p for p in prog["problems"] if p.startswith("C45")]
    assert any("{PDD_TIME} cannot be filled" in p for p in probs), probs
    assert any("{ROW:VOL-I-App3-01:no_such_parameter} cannot be filled" in p for p in probs), probs
    assert any("unknown placeholder {PDD_TIEM}" in p for p in probs), probs
    assert any("_milestones.labels.PDD" in p and "{time} cannot be filled" in p for p in probs), probs
    ms = {m["id"]: m for m in prog["milestones"]}
    assert ms["PDD"]["time"] == "" and ms["PDD"]["short"] == "PDD {time}"
    texts = json.dumps([prog["milestones"], [a["name"] for a in prog["activities"]], prog["planning_basis"]])
    assert "None" not in texts
    # the A3 subtitle omits what the text does not state
    r2 = dict(r, anchor_details={**r["anchor_details"], st: det})
    sub = stage2.a3(r2, [], None)["subtitle"]
    assert "Proposal Due Date 2026-11-26 Riyadh time" in sub and "None" not in sub


def test_fill_is_pure_and_reports_every_gap():
    probs: list[str] = []
    vals = {"PDD_TIME": "11:00", "PDD_TZ": None}
    out = schedule.fill("a {PDD_TIME} b {PDD_TZ} c {X} d {ROW:R-1:p}", vals, "where", probs,
                        lambda rid, p: (None, f"row {rid} has no parameter '{p}'"))
    assert out == "a 11:00 b {PDD_TZ} c {X} d {ROW:R-1:p}"
    assert len(probs) == 3 and all(p.startswith("C45: where") for p in probs)
    assert schedule.fill("{ok} and {a: b}", {"ok": "yes"}, "w", probs) == "yes and {a: b}"   # YAML-like text is not a placeholder


def test_plan_without_anchor_details_reads_them_from_the_evaluations(real):
    r, _ = real
    st = r["validated"].stage
    pdd = next(d["anchor_value"] for e in r["evals"] for d in e["stages"][st]["dates"] if d["anchor"] == "PDD")
    got = schedule.details_from_evals(r["evals"], st, {"PDD": pdd})
    want = r["anchor_details"][st]
    assert got["PDD"] == want["PDD"]


def test_a_fixed_milestones_time_comes_from_the_rules_own_words_not_the_label(real):
    r, out = real
    pb = next(m for m in _csv(out / "a5/milestones.csv") if m["id"] == "PRE-BID")
    assert (pb["time"], pb["short"]) == ("10:00", "Pre-Bid Conference 10:00")
    assert pb["label"].startswith("Pre-Bid Conference, 10:00 Riyadh time (VOL-I 5.4")
    assert "time" not in r["templates"]["_milestones"]["labels"]["PRE-BID"]          # nothing types it
    assert schedule.stated_time("Wednesday 30 September 2026 at 10:00 Riyadh time") == ("10:00", "Riyadh time")
    assert schedule.stated_time("within five (5) Working Days") is None
    tpl = copy.deepcopy(r["templates"])
    tpl["_milestones"]["labels"]["PRE-BID"]["time"] = "10:00"
    st = r["validated"].stage
    prog = schedule.plan(st, r["evals"], tpl, r["assumptions"], r["cal"], _issued(r, st), {"PDD": "2026-11-26"},
                         anchor_details=r["anchor_details"][st])
    assert any("_milestones.labels.PRE-BID types a time" in x for x in prog["problems"])
