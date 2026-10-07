"""Session 08, A5: the bid programme and its Gantt, derived from A1 (tenderpack.schedule, programme, gantt).

Owner's instructions checked here: the planning date is the latest addendum date; earliest dates come from a
forward pass from it and latest dates from a backward pass from the pack deadlines, with total float in Working
Days (negative float = INFEASIBLE, never compressed); an assumed unnamed three-member consortium with one foreign
member, the foreign-member count applied to the documents the pack ties to foreign members; staff effort is
separate from external waiting and overloads are reported, not levelled; timing, decision readiness and resource
feasibility are separate statuses; gates hold finalisation only; an elapsed conditional window is not a missed
duty; the marshalling plan lists every required item; the Gantt is built from the same data, deterministically.
Runs on the real build and on in-memory copies; nothing writes to the repository.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from datetime import date
from types import SimpleNamespace

import pymupdf
import pytest

from tenderpack import gantt, programme, schedule, stage2
from tenderpack.dates import Calendar, calendar_from_config
from tenderpack.util import ROOT, load_yaml

SCENARIOS = load_yaml(ROOT / "config/scenarios.yaml")
GATES = {"form-4a": ["I-F4A-FIELDS"], "form-4b": ["I-VOL-I-ENV-A-PRICES"], "assemble-envelope-b": ["I-VOL-I-ENV-B"],
         "copies": ["I-VOL-I-COPIES"]}
NO_LEVELLING = "resource levelling is NOT implemented; overloads are reported, not resolved"


@pytest.fixture(scope="module")
def r():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


@pytest.fixture(scope="module")
def mk(r):
    return programme.stage_planner(r)


@pytest.fixture(scope="module")
def base(r, mk):
    return mk(r["assumptions"])


def acts(p):
    return {a["id"]: a for a in p["activities"]}


def with_(assumptions, **overrides):
    return programme.apply_overrides(assumptions, overrides, "test")


def full_plan(r, assumptions=None, templates=None):
    """The validated stage with one extra synthetic row in force that needs EVERY evidence item in the vocabulary."""
    a = assumptions or r["assumptions"]
    stage = r["validated"].stage
    src = next(e for e in r["evals"] if schedule.in_force(e["stages"][stage]["status"])
               and any(d["anchor"] == "PDD" for d in e["stages"][stage]["dates"]))
    ev = dict(src["stages"][stage], stale=[], transcription="n/a (synthetic)")
    row = SimpleNamespace(id="TEST-ALL-ITEMS", evidence=sorted(r["evidence_items"]))
    evals = r["evals"] + [{"row": row, "stages": {stage: ev}}]
    s = next(x for x in r["stages"] if x.stage == stage)
    cal = calendar_from_config(a.get("calendar"))
    pdd = next(d["anchor_value"] for d in ev["dates"] if d["anchor"] == "PDD")
    p = schedule.plan(stage, evals, templates or r["templates"], a, cal, date.fromisoformat(s.issued), {"PDD": pdd},
                      evidence_items=r["evidence_items"])
    return programme.extend(p, r["evidence_items"], a, cal)


def node(d, *preds, deadline=None):
    return {"duration_wd": d, "predecessors": list(preds), "deadline_date": deadline, "deadline_rule": "X" if deadline else None}


# ============================================================================ 1. forward / backward / float

def test_forward_and_backward_pass_and_float_on_a_small_graph():
    cal = Calendar()                                         # Sun-Thu Working Days (VOL-I 2.4)
    g = {"a": node(3), "b": node(2, "a"), "c": node(0, "b"), "e": node(1),
         "d": node(1, "c", "e", deadline=date(2026, 11, 12))}  # Thursday
    n = schedule.network(g, cal, date(2026, 10, 31))         # a Saturday: the first Working Day on or after is Sun 1 Nov
    D = date.fromisoformat
    want = {"a": ("2026-11-01", "2026-11-03", "2026-11-05", "2026-11-09", 4),
            "b": ("2026-11-04", "2026-11-05", "2026-11-10", "2026-11-11", 4),
            "c": ("2026-11-05", "2026-11-05", "2026-11-11", "2026-11-11", 4),     # 0 WD: end of its predecessor's day
            "d": ("2026-11-08", "2026-11-08", "2026-11-12", "2026-11-12", 4),
            "e": ("2026-11-01", "2026-11-01", "2026-11-11", "2026-11-11", 8)}
    for k, (es, ef, ls, lf, fl) in want.items():
        got = n[k]
        assert (got["es"], got["ef"], got["ls"], got["lf"], got["float_wd"]) == (D(es), D(ef), D(ls), D(lf), fl), k
    assert n["d"]["es_driven_by"] == "c" and n["a"]["es_driven_by"] == "planning date"
    assert n["d"]["driven_by"] == "deadline:X" and n["a"]["driven_by"] == "b"
    # a week later the a-b-c-d chain has total float 4 - 5 = -1 WD: INFEASIBLE by 1 WD all along it, even for d,
    # whose own latest start (12 Nov) is still after the status date; e keeps 3 WD of float. Nothing is compressed.
    late = schedule.network(g, cal, date(2026, 11, 8))
    assert {k: v["float_wd"] for k, v in late.items()} == {"a": -1, "b": -1, "c": -1, "d": -1, "e": 3}
    assert late["d"]["ls"] == n["d"]["ls"] and late["d"]["lf"] == date(2026, 11, 12)
    for k in "abcd":
        fl = schedule.window_flags(late[k], date(2026, 11, 8), cal)
        assert fl and fl[0].startswith("INFEASIBLE by 1 WD"), (k, fl)
    assert schedule.window_flags(late["e"], date(2026, 11, 8), cal) == []


def test_planning_basis_is_the_latest_addendum_date_and_dates_are_consistent(r, base):
    assert r["validated"].stage == base["stage"] == "ADD-02"
    assert base["status_date"] == "2026-10-22" == base["planning_date"]
    assert "ADD-02" in base["planning_basis"] and "2026-10-22" in base["planning_basis"]
    assert "forward pass" in base["planning_basis"] and "backward pass" in base["planning_basis"]
    cal = r["cal"]
    D = date.fromisoformat
    for a in base["activities"]:
        es, ef = D(a["earliest_start"]), D(a["earliest_finish"])
        assert es >= D("2026-10-22") and cal.is_working_day(es) and cal.is_working_day(ef), a["id"]
        if not a["predecessors"]:
            assert a["earliest_start"] == "2026-10-22", a["id"]
        assert a["status"] == a["timing_status"], a["id"]
        if a["latest_start"] is None:
            assert a["float_wd"] is None
            continue
        assert a["float_wd"] == cal.working_days_between(es, D(a["latest_start"])), a["id"]
        if a["status"].startswith(("CONDITIONAL", "DEADLINE PASSED", "NOT NEEDED")):
            continue
        if a["float_wd"] < 0:
            assert a["status"] == f"INFEASIBLE by {-a['float_wd']} WD", a["id"]
        else:
            assert not a["status"].startswith("INFEASIBLE"), a["id"]
    x = acts(base)
    # the LCC chain sets the delivery: the same negative float runs from the ratio to the delivery
    assert x["lcc-certificate"]["float_wd"] < 0
    assert x["deliver"]["float_wd"] == x["lcc-certificate"]["float_wd"] == x["lcc-ratio"]["float_wd"]
    assert x["deliver"]["latest_finish"] == "2026-11-26"            # the PDD is never moved
    drv = {d["activity"]: d for d in base["drivers"]}
    assert "lcc-certificate" in drv["deliver"]["forward_chain"]
    assert any(o.startswith("lcc_certificate <= ") for o in drv["deliver"]["would_make_feasible"])


# ============================================================================ 2. foreign members

def test_foreign_member_multiplicity():
    bidder = {"members": 3, "foreign_members": 1}
    assert schedule.multiplicity("foreign_member", bidder) == (1, "bidder.foreign_members = 1")
    assert schedule.multiplicity("member", bidder) == (3, "bidder.members = 3")
    with pytest.raises(KeyError):
        schedule.multiplicity("foreign_member", {"members": 3})


@pytest.mark.parametrize("foreign", [0, 1, 2])
def test_investment_licence_documents_follow_the_foreign_member_count(r, mk, foreign):
    p = mk(with_(r["assumptions"], bidder={"foreign_members": foreign}))
    items = {i["evidence"]: i for i in p["documents"]["items"]}
    il = items["EV-INVESTMENT-LICENCE"]
    assert il["per"] == "foreign_member" and il["multiplicity"] == foreign
    assert il["physical_count"] == 4 * foreign                         # 1 marked original + 3 hard copies each
    assert "foreign_members" in il["multiplicity_basis"]
    assert items["EV-FORM-4C"]["multiplicity"] == 3                     # still one per member
    a = acts(p)["investment-licence"]
    assert a["count"] == foreign and a["effort_total_wd"] == foreign * a["effort_wd"]
    if foreign == 0:
        assert a["status"].startswith("NOT NEEDED") and a["flags"][0].startswith("NOT NEEDED")
        assert il["flags"] and any("count 0" in f for f in il["flags"])
    m = next(x for x in p["marshalling"] if x["evidence"] == "EV-INVESTMENT-LICENCE")
    assert m["count"] == foreign and m["per"] == "foreign_member"


def test_foreign_member_scenarios_and_assumption_checks(r):
    assert r["assumptions"]["bidder"]["foreign_members"] == 1 and r["assumptions"]["bidder"]["members"] == 3
    assert r["assumptions"]["bidder_basis"]["foreign_members"]["basis"].startswith("PROVISIONAL ASSUMPTION")
    bad = with_(r["assumptions"], bidder={"foreign_members": 4})
    assert any("foreign_members" in p and p.startswith("C45") for p in schedule.check_templates(r["templates"], bad))
    assert {"foreign-0", "foreign-2"} <= set(SCENARIOS["scenarios"])
    # no legalisation or apostille is invented: no clause asks for one
    words = json.dumps(r["templates"]).lower()
    assert "legalis" not in words and "apostille" not in words


def test_foreign_member_scenarios_change_the_licence_count(r, mk):
    sc = {k: v for k, v in SCENARIOS["scenarios"].items() if k in ("foreign-0", "foreign-2")}
    res = programme.run_scenarios(mk, r["assumptions"], sc)
    rows = {x["scenario"]: x for x in res["comparison"]}
    assert any(c.startswith("EV-INVESTMENT-LICENCE: x1 -> x0") for c in rows["foreign-0"]["document_changes"])
    assert any(c.startswith("EV-INVESTMENT-LICENCE: x1 -> x2") for c in rows["foreign-2"]["document_changes"])
    assert rows["foreign-2"]["physical_A"] == rows["foreign-2"]["physical_A_base"] + 4


# ============================================================================ 3. effort vs waiting, load, overloads

def test_effort_is_spread_over_the_late_window_and_overloads_are_reported_not_levelled():
    cal = Calendar()
    rows = [{"id": "wait", "resource": "legal", "effort_total_wd": 2, "duration_wd": 5, "waiting_on": "notary",
             "latest_start": "2026-11-01", "latest_finish": "2026-11-05", "status": "OK"},
            {"id": "staff", "resource": "legal", "effort_total_wd": 3, "duration_wd": 3, "waiting_on": "",
             "latest_start": "2026-11-03", "latest_finish": "2026-11-05", "status": "OK"}]
    load = schedule.resource_load(rows, {"legal": {"capacity": 1}}, cal, date(2026, 11, 1))
    day = {d: v["load"] for d, v in load["daily"]["legal"].items()}
    # the waiting activity is 5 WD long but loads only its 2 staff days: 0.4 per Working Day
    assert day == {"2026-11-01": 0.4, "2026-11-02": 0.4, "2026-11-03": 1.4, "2026-11-04": 1.4, "2026-11-05": 1.4}
    assert [(o["resource"], o["from"], o["to"], o["peak_load"], o["capacity"]) for o in load["overloads"]] == \
        [("legal", "2026-11-03", "2026-11-05", 1.4, 1)]
    st = schedule.resource_statuses(rows, load)
    assert st["staff"].startswith("OVERLOAD legal on 2026-11-03..2026-11-05") and "1.4" in st["staff"]
    # clipped at the planning date: the same effort in fewer days
    late = schedule.resource_load(rows, {"legal": {"capacity": 5}}, cal, date(2026, 11, 4))
    assert late["daily"]["legal"]["2026-11-04"]["load"] == pytest.approx(1 + 1.5)
    assert not late["overloads"] and any("clipped" in n for n in late["notes"])


def test_every_activity_separates_effort_from_waiting_with_labelled_assumptions(r, base):
    lead = r["assumptions"]["lead_times"]
    for k, v in lead.items():
        assert isinstance(v["effort_wd"], (int, float)) and 0 <= v["effort_wd"], k
        assert isinstance(v["waiting_on"], str), k
        assert v["effort_basis"].startswith("PROVISIONAL ASSUMPTION:"), k
    for a in base["activities"]:
        assert a["effort_wd"] == lead[a["duration_assumption"]]["effort_wd"], a["id"]
        assert a["effort_total_wd"] == pytest.approx(a["effort_wd"] * a["count"]), a["id"]
        # session 12 (F3, audit A5-9, deliberate): the owner's label "PROVISIONAL ASSUMPTION" in every data file
        assert a["effort_basis"].startswith("PROVISIONAL ASSUMPTION (owner "), a["id"]
        assert a["discipline"] in schedule.DISCIPLINES, a["id"]
        assert a["work_type"] == ("external waiting + staff effort" if a["waiting_on"] else "staff effort"), a["id"]
    x = acts(base)
    assert x["lcc-certificate"]["waiting_on"].startswith("competent authority")
    assert x["bond-approval"]["waiting_on"].startswith("bank") and x["poa"]["waiting_on"] == "notary"
    assert x["model-audit-opinion"]["waiting_on"] == "independent model auditor"
    assert x["poa-resolutions"]["waiting_on"] == "each member's board"
    assert x["technical-proposal"]["waiting_on"] == ""


def test_real_overloads_are_listed_with_dates_load_and_capacity(r, base):
    res = base["resources"]
    caps = {k: v["capacity"] for k, v in r["assumptions"]["resources"].items()}
    assert res["window"].startswith("late") and NO_LEVELLING in " ".join(res["notes"])
    for row in res["rows"]:
        assert row["status"] == ("OVERLOAD" if row["load_wd"] > row["capacity"] + 1e-9 else "OK")
        assert row["capacity"] == caps[row["resource"]] and row["capacity_basis"].startswith("PROVISIONAL")
    assert res["overloads"], "the assumed capacities should show at least one overload"
    for o in res["overloads"]:
        assert o["peak_load"] > o["capacity"] and o["from"] <= o["to"] and o["activities"]
        for aid in o["activities"]:
            assert acts(base)[aid]["resource_status"].startswith(f"OVERLOAD {o['resource']}")
    tot = {d["discipline"]: d for d in base["disciplines"]}
    assert set(tot) <= set(schedule.DISCIPLINES) and len(tot) == 5
    assert sum(d["staff_effort_wd"] for d in tot.values()) == pytest.approx(
        sum(a["effort_total_wd"] for a in base["activities"]), abs=0.05)


# ============================================================================ 4. three statuses; gates

def test_gates_hold_finalisation_only_and_name_the_decision_date(r, base):
    x = acts(base)
    assert {k: v["gated_by"] for k, v in x.items() if v["gated_by"]} == GATES
    for aid, issues in GATES.items():
        a = x[aid]
        assert a["decision_status"].startswith("GATED") and all(i in a["decision_status"] for i in issues)
        # session 11 (audit A5-1): a gate whose issue has a drafted clarification question also names the last day to
        # decide whether to ask (the clarification route's latest start); decision_needed_by is the earlier date
        assert a["finalise_by"] == a["latest_start"]
        if a["ask_by"]:
            assert a["decision_needed_by"] == min(a["ask_by"], a["latest_start"])
            assert f"finalise by {a['latest_start']}" in a["decision_status"] and a["ask_by"] in a["decision_status"]
        else:
            assert a["decision_needed_by"] == a["latest_start"] and f"decision needed by {a['latest_start']}" in a["decision_status"]
        assert a["timing_status"] == a["status"] and not a["status"].startswith("GATED")   # timing stays separate
        assert all(i in r["curated_issues"] for i in issues)                         # open issues in the register
    for prep in ("form-4a-prep", "poa", "spoc", "form-4b-prep", "references", "completion-certs", "model-audit-opinion",
                 "fin-assumptions", "fin-model-freeze", "form-4f", "assemble-envelope-a", "deliver"):
        # session 14 (F2; R3 m2): not gated: READY, or NOT GATED with the decision its finalisation needs (one state)
        assert x[prep]["decision_status"] == "READY" or x[prep]["decision_status"].startswith("NOT GATED ("), prep
    assert "form-4a-prep" in x["form-4a"]["predecessors"] and "form-4b-prep" in x["form-4b"]["predecessors"]
    for a in base["activities"]:
        assert {"timing_status", "decision_status", "resource_status", "status", "flags"} <= set(a), a["id"]
        assert a["resource_status"] == "OK" or a["resource_status"].startswith(("OVERLOAD", "NOT LOADED")), a["id"]


def test_lifting_a_gate_changes_decision_status_only(r):
    tpl = copy.deepcopy(r["templates"])
    for t in tpl["EV-FORM-4A"]:
        t.pop("gated_by", None)
    a, b = acts(full_plan(r)), acts(full_plan(r, templates=tpl))
    assert a["form-4a"]["decision_status"].startswith("GATED") and b["form-4a"]["decision_status"] == "READY"
    for k in ("earliest_start", "latest_start", "float_wd", "status", "resource_status"):
        assert a["form-4a"][k] == b["form-4a"][k], k


# ============================================================================ 5. conditional obligations, milestones

def test_an_elapsed_conditional_window_is_not_a_missed_duty(r, base):
    a = acts(base)["attendance-notice"]
    assert a["condition"] and "incorrectly recorded" in a["condition"]
    assert a["timing_status"] == a["status"] == ("CONDITIONAL — window elapsed 2026-10-14; whether the condition "
                                                  "arose is not known")
    assert not any("DEADLINE PASSED" in f for f in a["flags"]) and a["flags"][0].startswith("CONDITIONAL")
    assert a["id"] not in {d["activity"] for d in base["drivers"]}
    assert a["resource_status"].startswith("NOT LOADED")
    # at ADD-01 (planning date 8 Oct) its window is open: timing OK, still marked conditional
    p1 = programme.stage_planner(r, "ADD-01")(r["assumptions"])
    a1 = acts(p1)["attendance-notice"]
    assert a1["status"] == "OK" and any(f.startswith("CONDITIONAL (only if") for f in a1["flags"])
    # without a condition the same elapsed deadline is DEADLINE PASSED (unchanged semantics)
    cal = Calendar()
    t = schedule.backward_pass({"t": node(2, deadline=date(2026, 10, 14))}, cal)["t"]
    assert schedule.window_flags(t, date(2026, 10, 22), cal)[0].startswith("DEADLINE PASSED")
    fl = schedule.window_flags({**t, "condition": "something happened"}, date(2026, 10, 22), cal)
    assert fl[0].startswith("CONDITIONAL — window elapsed 2026-10-14; whether the condition arose is not known")


def test_fixed_pack_dates_are_milestones(base):
    ms = {m["id"]: m for m in base["milestones"]}
    assert ms["PRE-BID"]["date"] == "2026-09-30" and ms["PRE-BID"]["time"] == "10:00"
    assert ms["SITE-VISIT"]["date"] == "2026-10-01" and ms["SITE-VISIT"]["derived"]
    assert ms["CLARIFICATION-CUTOFF"]["date"] == "2026-11-12"
    assert ms["PDD"]["date"] == "2026-11-26" and ms["PDD"]["time"] == "14:00"
    assert ms["BID-BOND-VALIDITY"]["date"] == "2027-05-25"
    assert ms["ATTENDANCE-NOTICE"]["conditional"]
    for m in base["milestones"]:
        assert m["source"] and m["label"] and (m["rows"] or m["derived"]), m["id"]


# ============================================================================ 6. marshalling plan

@pytest.mark.parametrize("which", ["stage", "all-items"])
def test_marshalling_lists_every_required_item_once(r, base, which):
    p = base if which == "stage" else full_plan(r)
    need = p["evidence_needed"]
    rows = p["marshalling"]
    assert sorted(m["evidence"] for m in rows) == sorted(need)               # every item, each exactly once
    docs = {i["evidence"]: i for i in p["documents"]["items"]}
    for m in rows:
        assert m["req_ids"] == need[m["evidence"]] and m["req_ids"], m["evidence"]
        assert m["issuer"] and m["envelope"] and m["per"], m["evidence"]
        assert m["count"] == docs[m["evidence"]]["multiplicity"], m["evidence"]
        assert m["lead_time_wd"] >= 0 and m["lead_time_keys"], m["evidence"]
        assert "ASSUMPTION" in m["lead_time_basis"] and "PROVISIONAL" in m["lead_time_basis"], m["evidence"]
        assert m["drop_dead_start"] and m["needed_by"], m["evidence"]
        assert m["activity"] in {a["id"] for a in p["activities"]}, m["evidence"]


# ============================================================================ 7. outputs and the Gantt

@pytest.fixture(scope="module")
def written(base, tmp_path_factory):
    outs = []
    for name in ("a", "b"):
        d = tmp_path_factory.mktemp(f"a5-{name}")
        programme.write(base, None, d)
        outs.append(d)
    return outs


def test_gantt_files_are_written_and_deterministic(written):
    files = ("a5/gantt.svg", "a5/gantt.html", "a5/gantt.pdf", "a5/README.md", "a5/programme.json", "a5/marshalling.json",
             "a5/milestones.json", "a5/overloads.json", "a5/disciplines.json", "a5/resources.json")
    for f in files:
        a, b = (written[0] / f).read_bytes(), (written[1] / f).read_bytes()
        assert a and hashlib.sha256(a).hexdigest() == hashlib.sha256(b).hexdigest(), f
    doc = pymupdf.open(written[0] / "a5/gantt.pdf")
    assert doc.page_count == 1 and doc[0].rect.width > doc[0].rect.height                  # one landscape page
    assert doc.metadata["creationDate"] == doc.metadata["modDate"] and "tenderpack" in doc.metadata["producer"]
    assert "INFEASIBLE" in doc[0].get_text() and "PDD" in doc[0].get_text()


def test_gantt_shows_the_same_programme(base, written):
    svg = (written[0] / "a5/gantt.svg").read_text(encoding="utf-8")
    html_ = (written[0] / "a5/gantt.html").read_text(encoding="utf-8")
    assert svg == gantt.svg(base)                                       # from the programme data, nothing else
    assert "<svg" in html_ and NO_LEVELLING in html_ and "PROVISIONAL" in html_
    for a in base["activities"]:
        assert f'id="act-{a["id"]}"' in svg, a["id"]
        title = re.search(rf'<g id="act-{re.escape(a["id"])}"[^>]*>\s*<title>([^<]*)</title>', svg).group(1)
        assert all(rid in title for rid in a["req_ids"]), a["id"]        # every A1 id on the row (hover title)
        assert a["id"] in html_
    for word in ("Planning date 2026-10-22", "PDD 14:00", "Clarification cut-off", "Pre-Bid Conference", "Site visit",
                 "INFEASIBLE", "GATED", "OVERLOAD", "external waiting", "staff effort", "late window", "float"):
        assert word in svg, word


def test_outputs_carry_requirement_ids_statuses_and_the_explanation(base, written):
    out = written[0] / "a5"
    prog = json.loads((out / "programme.json").read_text(encoding="utf-8"))
    assert prog["planning_date"] == "2026-10-22" and prog["planning_basis"]
    for row in prog["rows"]:
        assert row["req_ids"], row["id"]
        for k in ("earliest_start", "earliest_finish", "latest_start", "latest_finish", "float_wd", "timing_status",
                  "decision_status", "resource_status", "discipline", "effort_total_wd", "waiting_on"):
            assert k in row, (row["id"], k)
    for row in json.loads((out / "marshalling.json").read_text(encoding="utf-8"))["rows"]:
        assert row["req_ids"], row["evidence"]
    readme = (out / "README.md").read_text(encoding="utf-8")
    for must in ("2026-10-22", "ADD-02", "forward pass", "backward pass", "float", NO_LEVELLING,
                 "No bidder references, certificates, attendance or financial standing are assumed",
                 "timing_status", "decision_status", "resource_status", "I-F4A-FIELDS", "I-VOL-I-ENV-B",
                 "I-VOL-I-ENV-A-PRICES", "I-VOL-I-COPIES", "CONDITIONAL", "foreign_members"):
        assert must in readme, must
    for k in list(base["assumptions"]["lead_times"]) + list(base["assumptions"]["resources"]):
        assert k in readme, k


def test_stage2_calls_still_work_and_issues_read_the_timing_status(r):
    progs = stage2.a5_all(r)
    p = progs["ADD-02"]
    for a in p["activities"]:
        assert a["req_ids"] and a["status"] == a["timing_status"]
        if a["status"] != "OK":                                          # collect_issues quotes flags[0]
            assert a["flags"][0].startswith(a["status"].split(" ")[0]), a["id"]
    issues = {i["id"]: i for i in stage2.collect_issues(r, p)}
    assert "CONDITIONAL" in issues["I-A5-attendance-notice"]["text"]
    assert "attendance-notice" not in issues["I-A5-FEASIBILITY"]["text"]
