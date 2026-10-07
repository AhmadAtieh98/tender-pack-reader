"""Session 12 audit, fixer F3: findings A5-1 .. A5-10 (the bid programme, its coverage of A1, the replan deltas, the
Gantt). Each test reproduces one finding on the real pack (the committed evidence build, stage2.run) and checks the
corrected behaviour. Nothing writes to the repository (outputs go to pytest's temporary folders).
"""
from __future__ import annotations

import copy
import csv
import io
import re

import pytest

from tenderpack import gantt, programme, schedule, stage2
from tenderpack.util import ROOT


@pytest.fixture(scope="module")
def r():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


@pytest.fixture(scope="module")
def base(r):
    return programme.stage_planner(r)(r["assumptions"])


@pytest.fixture(scope="module")
def written(base, tmp_path_factory):
    out = tmp_path_factory.mktemp("a5-audit-s12")
    programme.write(base, None, out)
    a5 = out / "a5"
    return {"dir": a5, **{k: (a5 / f).read_text(encoding="utf-8") for k, f in
            (("readme", "README.md"), ("svg", "gantt.svg"), ("html", "gantt.html"), ("csv", "programme.csv"),
             ("marsh", "marshalling.csv"), ("drivers", "drivers.csv"))}}


@pytest.fixture(scope="module")
def replan(r):
    progs = stage2.a5_all(r)
    ea = {e["row"].id: e["stages"]["ADD-01"] for e in r["evals"]}
    eb = {e["row"].id: e["stages"]["ADD-02"] for e in r["evals"]}
    return schedule.deltas(progs["ADD-01"], progs["ADD-02"], ea, eb, answers=programme.answers_by_row(r, "ADD-02"))


def acts(p):
    return {a["id"]: a for a in p["activities"]}


def rows_of(text: str) -> list[dict]:
    return list(csv.DictReader(io.StringIO(text.lstrip("﻿"))))


def _row_group(svg: str, aid: str) -> str:
    m = re.search(rf'<g id="act-{re.escape(aid)}">(.*?)</g>', svg, re.S)
    assert m, aid
    return m.group(1)


def in_force_rows(r, stage):
    return {e["row"].id: e["row"] for e in r["evals"] if schedule.in_force(e["stages"][stage]["status"])}


# ---------------------------------------------------------------------------------------------- A5-1
def test_a5_1_lcc_lines_link_the_drafted_question_and_the_last_day_to_ask(r, base, written):
    a = acts(base)
    route = a["clarifications"]
    ask = route["latest_start"]                     # computed: the route must finish by the clarification cut-off
    cutoff = base["deadlines"]["CLARIFICATION-CUTOFF"]["date"]
    assert ask == "2026-11-11" and cutoff == "2026-11-12"
    for aid in ("lcc-ratio", "lcc-certificate"):
        x = a[aid]
        assert "CQ-LCC-ISSUER" in x["clarification_questions"], (aid, x["clarification_questions"])
        assert x["ask_by"] == ask, (aid, x["ask_by"])
        # not gated: preparation and the application continue (session 14, F2; R3 m2: NOT GATED, with what it needs)
        assert x["decision_status"].startswith("NOT GATED (") and "I-LCC-ISSUER" in x["decision_status"]
        assert any("CQ-LCC-ISSUER" in f and ask in f and "not sent" in f for f in x["flags"]), x["flags"]
    m = next(x for x in base["marshalling"] if x["evidence"] == "EV-LCC")
    assert "CQ-LCC-ISSUER" in m["clarification_questions"] and m["ask_by"] == ask, m
    assert any("CQ-LCC-ISSUER" in f for f in m["flags"]), m["flags"]
    d = next(x for x in base["drivers"] if x["activity"] == "lcc-certificate")
    assert any("CQ-LCC-ISSUER" in o and ask in o for o in d["would_make_feasible"]), d["would_make_feasible"]
    timing = written["readme"].split("## Timing at the planning date")[1].split("\n## ")[0]
    line = next(x for x in timing.splitlines() if x.startswith("- `lcc-certificate`"))
    assert "CQ-LCC-ISSUER" in line and ask in line, line
    assert "ask by 11 Nov" in _row_group(written["svg"], "lcc-certificate")
    head = rows_of(written["marsh"])[0]
    assert "clarification_questions" in head and "ask_by" in head


def test_a5_1_no_question_no_route(r):
    p = programme.stage_planner(dict(r, clarifications={**r["clarifications"], "clarifications": []}))(r["assumptions"])
    x = acts(p)["lcc-certificate"]
    assert x["clarification_questions"] == [] and x["ask_by"] is None
    assert not any("not sent" in f for f in x["flags"])


# ---------------------------------------------------------------------------------------------- A5-2
def test_a5_2_an_amended_volume_v_clause_reworks_the_form_4e_work(replan):
    rw = {d["activity"]: d for d in replan if d["change"] == "REWORK"}
    for aid in ("deviations-review", "form-4e"):
        assert aid in rw, (aid, [d for d in replan if d["activity"] == aid])
        assert "VOL-V-36.2-01" in rw[aid]["rows"] and "VOL-V-36.2-01" in rw[aid]["detail"], rw[aid]


def test_a5_2_the_volume_check_carries_every_clause_in_force(r, base):
    a = acts(base)
    vol_v = {k for k, row in in_force_rows(r, base["stage"]).items() if any(u.startswith("VOL-V:") for u in row.units)}
    assert vol_v and vol_v <= set(a["deviations-review"]["req_ids"]) and vol_v <= set(a["form-4e"]["req_ids"])
    spec = r["templates"]["_volume_checks"]["VOL-V"]
    assert spec["review"] == "proposed" and "taken as accepted" in spec["basis"]
    # the mechanism, not the case: without the volume check the amended clause reaches no activity
    t = copy.deepcopy(r["templates"])
    t.pop("_volume_checks")
    p = programme.stage_planner(dict(r, templates=t))(r["assumptions"])
    assert "VOL-V-36.2-01" not in acts(p)["deviations-review"]["req_ids"]


# ---------------------------------------------------------------------------------------------- A5-3
def test_a5_3_form_4e_is_checked_against_the_technical_proposal(r, base):
    a = acts(base)
    assert "technical-proposal" in a["form-4e"]["predecessors"]
    assert a["technical-proposal"]["float_wd"] == 1 and a["form-4e"]["float_wd"] == 1
    assert a["technical-proposal"]["latest_finish"] == "2026-11-19"
    bad = sorted(k for k, x in a.items() if x["status"].startswith("INFEASIBLE"))
    assert bad == ["assemble-envelope-a", "copies", "deliver", "lcc-certificate", "lcc-ratio", "seal-and-mark"], bad
    t = next(x for x in r["templates"]["EV-FORM-4E"] if x["id"] == "form-4e")
    assert t["review"] == "proposed" and "qualification elsewhere in the Proposal" in t["basis"]


# ---------------------------------------------------------------------------------------------- A5-4
def test_a5_4_every_in_force_row_is_carried_or_excepted_with_its_reason(r, base, written):
    force = in_force_rows(r, base["stage"])
    cov = base["row_coverage"]
    assert set(cov["rows"]) == set(force)
    assert set(cov["carried"]) | set(cov["excepted"]) == set(force) and cov["uncarried"] == []
    assert all(v["reason"].strip() and v["source"] for v in cov["excepted"].values())
    carried = {x for a in base["activities"] for x in a["req_ids"]}
    assert set(cov["carried"]) == carried & set(force)
    sec = written["readme"].split("## Requirements not carried by an activity (with the reason)")[1].split("\n## ")[0]
    for k in cov["excepted"]:
        assert f"`{k}`" in sec, k
    table = rows_of((written["dir"] / "requirements_not_carried.csv").read_text(encoding="utf-8"))
    assert {x["row"] for x in table} == set(cov["excepted"]) and all(x["reason"] for x in table)
    assert "VOL-I-4.2-01" in cov["excepted"] and cov["excepted"]["VOL-I-4.2-01"]["source"].startswith("_row_exceptions")


def test_a5_4_the_three_named_rows_go_onto_the_activities_that_discharge_them(r, base):
    a = acts(base)
    assert "VOL-IV-FORMS-01" in a["form-4a"]["req_ids"] and "VOL-IV-FORMS-01" in a["form-4e"]["req_ids"]
    assert "VOL-I-4.1-01" in a["clarifications"]["req_ids"]
    assert "VOL-I-5.5-01" in a["ground-dd"]["req_ids"]
    for rid in ("VOL-IV-FORMS-01", "VOL-I-4.1-01", "VOL-I-5.5-01"):
        spec = r["templates"]["_row_checks"][rid]
        assert spec["review"] == "proposed" and "'" in spec["basis"], rid


def test_a5_4_c48_counts_every_in_force_row(r, base):
    c = programme.coverage_check(base)
    n = len(in_force_rows(r, base["stage"]))
    assert c["id"] == "C48" and c["ok"], c
    assert f"{n} A1 rows in force" in c["detail"] and "carried" in c["detail"] and "excepted with a reason" in c["detail"]
    assert "not carried: none" in c["detail"] and "A3" in c["detail"], c["detail"]
    # a row with no activity and no reason is reported
    evals = []
    for e in r["evals"]:
        if e["row"].id == "VOL-I-6.7-01":
            e = {**e, "row": e["row"].model_copy(update={"no_deliverable": None})}
        evals.append(e)
    p = programme.stage_planner(dict(r, evals=evals))(r["assumptions"])
    assert "VOL-I-6.7-01" in p["row_coverage"]["uncarried"]
    c2 = programme.coverage_check(p)
    assert not c2["ok"] and "VOL-I-6.7-01" in c2["detail"]
    assert any(x.startswith("C48: VOL-I-6.7-01 ") for x in p["problems"])


# ---------------------------------------------------------------------------------------------- A5-5
def test_a5_5_envelope_b_carries_the_envelope_b_rule(base, replan):
    a = acts(base)
    assert "VOL-I-10.1-01" in a["assemble-envelope-b"]["req_ids"]
    assert "VOL-I-9.1-01" not in a["assemble-envelope-b"]["req_ids"]
    assert "VOL-I-9.1-01" in a["assemble-envelope-a"]["req_ids"]
    assert not any(d["activity"] == "assemble-envelope-b" and "VOL-I-9.1-01" in d["detail"] for d in replan)


# ---------------------------------------------------------------------------------------------- A5-6
def test_a5_6_form_4a_reworks_when_an_addendum_is_issued(replan):
    for aid in ("form-4a", "form-4a-prep"):
        rw = [d for d in replan if d["activity"] == aid and d["change"] == "REWORK"]
        assert rw and "ADD-01-AppA-01" in rw[0]["rows"], (aid, [d for d in replan if d["activity"] == aid])
        assert "ADD-02" in rw[0]["detail"] and "Bidders shall acknowledge receipt in Form 4-A." in rw[0]["detail"]
        assert not any(d["activity"] == aid and d["change"] == schedule.CONFIRMED and "ADD-01-AppA-01" in d["rows"]
                       for d in replan), aid


# ---------------------------------------------------------------------------------------------- A5-7
def test_a5_7_new_lines_fill_rows(replan):
    new = [d for d in replan if d["change"] == "NEW"]
    assert new and all(d.get("rows") for d in new), new


# ---------------------------------------------------------------------------------------------- A5-8
def test_a5_8_one_discipline_vocabulary_or_a_stated_mapping(r, base, written):
    a1 = {row.discipline for row in (e["row"] for e in r["evals"])}
    m = programme.discipline_map(r["templates"])
    for a in base["activities"]:
        d = a["discipline"]
        assert d in a1 or (d in m and set(m[d]) <= a1), d
    assert all(set(v) <= a1 for v in m.values())
    covered = {d for d in schedule.DISCIPLINES if d in a1} | {x for v in m.values() for x in v}
    carried = {x for a in base["activities"] for x in a["req_ids"]}
    rows = {e["row"].id: e["row"] for e in r["evals"]}
    assert {rows[k].discipline for k in carried} <= covered
    sec = written["readme"].split("## Disciplines: A1 to A5")[1].split("\n## ")[0]
    assert "Finance" in sec and "Operations" in sec and "Commercial" in sec and "Technical" in sec


# ---------------------------------------------------------------------------------------------- A5-9
def test_a5_9_the_owners_label_finds_every_assumption(base, written):
    assert schedule.PROVISIONAL == "PROVISIONAL ASSUMPTION"
    prog = rows_of(written["csv"])
    assert prog and all(schedule.PROVISIONAL in x["duration_basis"] and schedule.PROVISIONAL in x["effort_basis"]
                        for x in prog)
    marsh = [x for x in rows_of(written["marsh"]) if x["lead_time_basis"]]
    assert marsh and all(schedule.PROVISIONAL in x["lead_time_basis"] for x in marsh)
    assert "ASSUMPTION (PROVISIONAL" not in written["csv"] + written["marsh"]


# ---------------------------------------------------------------------------------------------- A5-10
def test_a5_10_the_html_chart_is_readable_at_a_normal_window(base, written):
    html = written["html"]
    assert written["svg"] in html                                       # the identical SVG is embedded
    m = re.search(r"\.chart svg\{[^}]*width:(\d+(?:\.\d+)?)px", html)
    assert m, "the chart has no fixed display width"
    width = float(m.group(1))
    sizes = [it[4] for it in gantt.layout(base) if it[0] == "text"]
    smallest = min(sizes) * width / gantt.PAGE_W
    assert smallest >= gantt.HTML_MIN_FONT_PX - 0.01, smallest
    assert "overflow-x:auto" in html and "max-width:none" in html
