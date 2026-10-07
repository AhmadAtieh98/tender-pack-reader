"""Session 11 audit, fixer F3: findings A5-1 .. A5-8 and R-9 (the bid programme, its Gantt and the replan deltas).

Each test reproduces one finding on the real pack (the committed evidence build, stage2.run) and checks the corrected
behaviour. Nothing writes to the repository (outputs go to pytest's temporary folders).
"""
from __future__ import annotations

import copy
import re

import pytest

from tenderpack import gantt, programme, schedule, stage2
from tenderpack.register import BID_OUT
from tenderpack.util import ROOT


@pytest.fixture(scope="module")
def r():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


@pytest.fixture(scope="module")
def base(r):
    return programme.stage_planner(r)(r["assumptions"])


@pytest.fixture(scope="module")
def written(base, tmp_path_factory):
    out = tmp_path_factory.mktemp("a5-audit")
    programme.write(base, None, out)
    a5 = out / "a5"
    return {k: (a5 / f).read_text(encoding="utf-8") for k, f in
            (("readme", "README.md"), ("svg", "gantt.svg"), ("html", "gantt.html"), ("csv", "programme.csv"),
             ("marsh", "marshalling.csv"))}


def acts(p):
    return {a["id"]: a for a in p["activities"]}


def _row_group(svg: str, aid: str) -> str:
    m = re.search(rf'<g id="act-{re.escape(aid)}">(.*?)</g>', svg, re.S)
    assert m, aid
    return m.group(1)


# ---------------------------------------------------------------------------------------------- A5-1
def test_a5_1_gates_with_a_drafted_question_have_an_ask_by_date(r, base, written):
    a = acts(base)
    route = a["clarifications"]
    assert route["deadline_rule"] == "CLARIFICATION-CUTOFF" and route["latest_start"] == "2026-11-11"
    qs = {i: [c["id"] for c in r["clarifications"]["clarifications"] if i in (c.get("linked_issues") or [])]
          for g in ("form-4a", "form-4b", "assemble-envelope-b", "copies") for i in a[g]["gated_by"]}
    for g in ("form-4a", "form-4b", "assemble-envelope-b", "copies"):
        x = a[g]
        want = sorted(q for i in x["gated_by"] for q in qs[i])
        # session 12 (F3, audit A5-1, deliberate): clarification_questions also lists the questions drafted on the issues
        # of the rows the activity carries, gated or not; the gate's own questions are still the ones decision_status names
        assert want and set(want) <= set(x["clarification_questions"]), g
        assert all(q in x["decision_status"] for q in want), g
        assert x["ask_by"] == "2026-11-11" and x["finalise_by"] == x["latest_start"], g
        assert x["decision_needed_by"] == "2026-11-11", g             # the first decision is whether to ask
        assert "decide whether to ask the Authority by 2026-11-11" in x["decision_status"], x["decision_status"]
        assert f"finalise by {x['latest_start']}" in x["decision_status"], x["decision_status"]
        row = _row_group(written["svg"], g)
        assert "ask by 11 Nov" in row and "finalise by" in row, g
    gates = written["readme"].split("## Decision gates")[1].split("\n## ")[0]
    assert "2026-11-11" in gates and "2026-11-23" in gates and "VOL-I 3.3" in gates and "VOL-I 5.2" in gates, gates
    head = written["csv"].splitlines()[0]
    assert "ask_by" in head and "finalise_by" in head and "clarification_questions" in head


def test_a5_1_without_a_question_the_gate_keeps_its_latest_start(r):
    p = programme.stage_planner(dict(r, clarifications={**r["clarifications"], "clarifications": []}))(r["assumptions"])
    x = acts(p)["form-4a"]
    assert x["ask_by"] is None and x["clarification_questions"] == [] and x["decision_needed_by"] == x["latest_start"]
    assert f"decision needed by {x['latest_start']}" in x["decision_status"]


# ---------------------------------------------------------------------------------------------- A5-2
def test_a5_2_every_a3_row_in_force_is_carried_or_excepted(r, base, written):
    a = acts(base)
    assert "VOL-I-6.2-02" in a["assemble-envelope-a"]["req_ids"] and "VOL-I-6.2-02" in a["form-4b"]["req_ids"]
    carriers = [x for x in base["activities"] if "VOL-I-8.1-01" in x["req_ids"]]
    assert carriers and all("prequalified" in x["name"] for x in carriers)
    # session 12 (F3, audit A5-9, deliberate): the owner's label "PROVISIONAL ASSUMPTION" (was "ASSUMPTION (PROVISIONAL")
    assert all(x["duration_basis"].startswith("PROVISIONAL ASSUMPTION") for x in carriers)
    stage = r["validated"].stage
    a3 = {e["row"].id for e in r["evals"] if schedule.in_force(e["stages"][stage]["status"])
          and isinstance((e["stages"][stage]["interpretation"] or {}).get("consequence"), dict)
          and e["stages"][stage]["interpretation"]["consequence"]["class"] in BID_OUT}
    # session 13 (F3, audit R3-5, deliberate): A5's A3 rows are the rows the A3 page lists (schedule.a3_rows, one set
    # for both): the BID_OUT rows above and the row whose Envelope B is returned unopened (score_elimination)
    assert a3 < set(schedule.a3_rows(r["evals"], stage))
    a3 = set(schedule.a3_rows(r["evals"], stage))
    cov = base["a3_coverage"]
    assert set(cov["carried"]) | set(cov["excepted"]) == a3 and cov["uncarried"] == []
    assert all(cov["excepted"].values())
    assert "VOL-I-6.2-02" in cov["carried"] and "A3 rows" in written["readme"]
    assert not [p for p in base["problems"] if "A3" in p]


def test_a5_2_an_uncarried_a3_row_is_a_problem(r):
    t = copy.deepcopy(r["templates"])
    t["_row_checks"].pop("VOL-I-6.2-02")
    p = programme.stage_planner(dict(r, templates=t))(r["assumptions"])
    assert "VOL-I-6.2-02" in p["a3_coverage"]["uncarried"]
    assert any(x.startswith("C48: VOL-I-6.2-02 ") and "A3" in x for x in p["problems"]), p["problems"]
    assert not any(x.startswith(("C44", "C45")) for x in p["problems"])          # reported, not structural


# ---------------------------------------------------------------------------------------------- A5-3
def test_a5_3_forms_wait_for_what_they_record(base):
    a = acts(base)
    assert "model-audit-opinion" in a["form-4f"]["predecessors"]
    assert "completion-certs" in a["form-4b"]["predecessors"]
    for k in ("fin-model-build", "fin-model-freeze", "model-audit-opinion"):
        assert a[k]["float_wd"] == 0 and a[k]["status"] == "OK", (k, a[k]["float_wd"], a[k]["status"])
    assert a["model-audit-opinion"]["latest_finish"] == "2026-11-19"


# ---------------------------------------------------------------------------------------------- A5-4 / A5-5
@pytest.fixture(scope="module")
def replan(r):
    progs = stage2.a5_all(r)
    ea = {e["row"].id: e["stages"]["ADD-01"] for e in r["evals"]}
    eb = {e["row"].id: e["stages"]["ADD-02"] for e in r["evals"]}
    return {"plain": schedule.deltas(progs["ADD-01"], progs["ADD-02"], ea, eb),
            "answers": schedule.deltas(progs["ADD-01"], progs["ADD-02"], ea, eb,
                                       answers=programme.answers_by_row(r, "ADD-02"))}


@pytest.mark.parametrize("kind", ["plain", "answers"])
def test_a5_4_a_note_added_is_not_a_requirement_change(replan, kind):
    dl = replan[kind]
    rework = {d["activity"]: d["detail"] for d in dl if d["change"] == "REWORK"}
    for aid, row in (("bond-approval", "VOL-I-6.4-01"), ("bond-issue", "VOL-I-6.4-01"), ("form-4c-sign", "VOL-I-9.4-01"),
                     ("pcg-wording", "VOL-I-8.7-01"), ("pcg-execution", "VOL-I-8.7-01"), ("form-4f", "VOL-I-10.5-01"),
                     ("clarifications", "VOL-II-4.2-01")):
        assert row not in rework.get(aid, ""), (aid, rework.get(aid))
        # session 12 (W3a, deliberate): one label for a confirmation or a reading re-made with the same substance,
        # CONFIRMED (unchanged) (was 'REVIEW (clarification noted, no change)'); the detail cites the confirming op
        # session 12, F5 (audit A2-1/A5 N1, deliberate): a row under an issue a person has not decided is NOT SETTLED,
        # never CONFIRMED (VOL-II-4.2-01: I-FLOWS, linked from a pending decision of the clarification register)
        want = "NOT SETTLED" if row == "VOL-II-4.2-01" else "CONFIRMED (unchanged)"
        assert any(d["activity"] == aid and d["change"] == want and row in d["detail"] for d in dl), aid
    assert "VOL-I-9.1-01" in rework["assemble-envelope-a"]          # Form 4-G inserted: the reading did change


def test_a5_4_confirming_answers_are_classified(r, replan):
    ans = programme.answers_by_row(r, "ADD-02")
    q8 = [x for x in ans["VOL-I-6.4-01"] if x["op"] == "ADD-02/Q8"]
    assert q8 and q8[0]["answer"] and q8[0]["class"] in ("none", "confirms")
    d = next(d for d in replan["answers"] if d["activity"] == "bond-approval" and d["change"] == "CONFIRMED (unchanged)")
    assert "ADD-02/Q8" in d["detail"] and "confirms" in d["detail"]


def test_a5_5_status_and_float_flips_are_deltas(replan):
    st = {d["activity"]: d["detail"] for d in replan["plain"] if d["change"] == "STATUS"}
    # ADD-01: OK with positive float (+12 before A5-3 added model-audit-opinion -> form-4f, +10 since); ADD-02: -12
    assert "deliver" in st and "OK -> INFEASIBLE by 12 WD" in st["deliver"], st.get("deliver")
    assert re.search(r"total float \+\d+ -> -12 WD", st["deliver"]), st["deliver"]
    for k in ("assemble-envelope-a", "copies", "seal-and-mark"):
        assert k in st and "OK -> INFEASIBLE by 12 WD" in st[k], k
    new = {d["activity"] for d in replan["plain"] if d["change"] == "NEW"}
    assert {"lcc-ratio", "lcc-certificate"} <= new                  # reinstated at ADD-02: NEW, not a status change


# ---------------------------------------------------------------------------------------------- A5-6
def test_a5_6_flags_and_dependencies_are_in_every_view(base, written):
    tp = acts(base)["technical-proposal"]
    assert any("Environmental Permit" in f for f in tp["flags"])
    row = _row_group(written["svg"], "technical-proposal")
    assert "Environmental Permit" in row and "BLOCKED" in row
    assert "Environmental Permit" in written["readme"].split("## Flags on activities")[1].split("\n## ")[0]
    assert any("Environmental Permit" in line for line in written["marsh"].splitlines() if line.startswith("EV-TECH-PROPOSAL"))
    assert "<th>Predecessors</th>" in written["html"] and "<th>Flags</th>" in written["html"]
    assert re.search(r"<b>lcc-certificate</b>.*?<td>lcc-ratio</td>", written["html"], re.S)


# ---------------------------------------------------------------------------------------------- A5-7
def test_a5_7_delivery_carries_the_time_and_an_explicit_buffer(r, base):
    d = acts(base)["deliver"]
    assert "2026-11-26 14:00" in d["deadline"] and d["latest_finish"] == "2026-11-26"
    assert "delivery buffer 0 WD" in d["deadline"] and "PROVISIONAL ASSUMPTION" in d["deadline"]
    m = next(x for x in base["marshalling"] if x["evidence"] == "EV-DELIVERY")
    assert m["needed_by"] == "2026-11-26 14:00"
    sub = r["assumptions"]["submission"]
    assert sub["delivery_buffer_wd"] == 0 and sub["delivery_buffer_basis"]["owner"] == "Bid manager"
    a2 = programme.apply_overrides(r["assumptions"], {"submission": {"delivery_buffer_wd": 1}}, "t")
    d2 = acts(programme.stage_planner(r)(a2))["deliver"]
    assert d2["latest_finish"] == "2026-11-25" and "2026-11-26 14:00" in d2["deadline"]
    assert "delivery buffer 1 WD" in d2["deadline"]


# ---------------------------------------------------------------------------------------------- A5-8
def test_a5_8_attendance_window_end_shows_both_readings(base, written):
    m = next(x for x in base["milestones"] if x["id"] == "ATTENDANCE-NOTICE")
    assert m["date"] == "2026-10-14" and "2026-10-15" in m["other_readings"]
    line = next(x for x in written["readme"].splitlines() if "attendance" in x and x.startswith("- **2026-10-14"))
    assert "conservative" in line and "2026-10-15 if the ADD-01 issue day is excluded" in line, line
    assert "14 Oct (conservative; 15 Oct if the ADD-01 issue day is excluded)" in written["svg"]


# ---------------------------------------------------------------------------------------------- R-9
def test_r9_status_column_is_wrapped_not_truncated(base):
    items = gantt.layout(base)
    x0 = gantt.MARGIN + gantt.LABEL_W
    rows, cur = {}, None
    for it in items:
        if it[0] == "open":
            cur = it[1][4:]
            rows[cur] = []
        elif it[0] == "close":
            cur = None
        elif cur and it[0] == "text" and x0 <= it[1] < x0 + gantt.STATUS_W:
            rows[cur].append(it)
    for aid in ("form-4a", "copies"):
        texts = [t[3] for t in rows[aid]]
        joined = " ".join(texts)
        assert not any(t.endswith("...") for t in texts), texts
        assert "GATED" in joined and "finalise by" in joined, texts
        assert len({t[2] for t in rows[aid]}) == 2, texts            # two lines
    assert "OVERLOAD legal_counsel" in " ".join(t[3] for t in rows["form-4a"])
    assert "INFEASIBLE by 12 WD" in " ".join(t[3] for t in rows["copies"])
