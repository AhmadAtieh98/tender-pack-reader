"""Stage 4: A5 generated from the A1 rows: documents, resources, drivers and scenarios (tenderpack.programme).

Runs on the real build (stage2.run) and on in-memory copies of the assumptions and templates; nothing writes to
the repository. Lead times, multiplicities and capacities are PROVISIONAL ASSUMPTIONS: these tests check how
the programme responds to them, not that any value is right.
"""
from __future__ import annotations

import copy
import hashlib
import re
from datetime import date
from types import SimpleNamespace

import pytest
import yaml

from tenderpack import programme, schedule, stage2
from tenderpack.dates import calendar_from_config
from tenderpack.util import ROOT, load_yaml
from guards import only_owner_approvals

SCENARIOS = load_yaml(ROOT / "config/scenarios.yaml")


@pytest.fixture(scope="module")
def r():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


@pytest.fixture(scope="module")
def mk(r):
    return programme.stage_planner(r)


@pytest.fixture(scope="module")
def base(r, mk):
    return mk(r["assumptions"])


@pytest.fixture(scope="module")
def scen(r, mk):
    return programme.run_scenarios(mk, r["assumptions"], SCENARIOS)


def with_(assumptions, **overrides):
    return programme.apply_overrides(assumptions, overrides, "test")


def full_plan(r, assumptions=None, templates=None):
    """The validated stage's programme with one extra synthetic row in force that needs EVERY evidence item in the
    vocabulary (so every template is expanded, whatever the register slice covers today)."""
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


def acts(p):
    return {a["id"]: a for a in p["activities"]}


# ============================================================================ templates and assumptions

def test_every_vocabulary_item_has_activities_or_a_justified_exception(r):
    exc = r["templates"].get("_exceptions") or {}
    missing = [k for k in sorted(r["evidence_items"]) if not r["templates"].get(k) and not (exc.get(k) or "").strip()]
    assert not missing, f"evidence items with no template and no exception: {missing}"
    p = full_plan(r)
    assert p["problems"] == []
    assert {"TEST-ALL-ITEMS"} <= {x for a in p["activities"] for x in a["req_ids"]}


def test_every_activity_has_a_resource_and_a_provisional_labelled_lead_time(r, base):
    asm = r["assumptions"]
    for p in (base, full_plan(r)):
        for a in p["activities"]:
            assert a["resource"] in asm["resources"], a["id"]
            assert a["duration_basis"].startswith("ASSUMPTION (PROVISIONAL; owner "), a["id"]
            assert a["duration_assumption"] in asm["lead_times"]
    for k, v in asm["lead_times"].items():
        assert v["basis"].startswith("PROVISIONAL ASSUMPTION:") and v["owner"], k
    for k, v in asm["resources"].items():
        assert v["basis"].startswith("PROVISIONAL ASSUMPTION:") and v["owner"] and isinstance(v["capacity"], int), k
    for k, v in asm["bidder_basis"].items():
        assert k in asm["bidder"] and v["basis"].startswith("PROVISIONAL ASSUMPTION") and v["owner"], k


def test_a_template_without_a_resource_or_with_an_unknown_role_is_a_c45_problem(r):
    tpl = copy.deepcopy(r["templates"])
    tpl["EV-LCC"][0].pop("resource")
    tpl["EV-LCC"][1]["resource"] = "astrologer"
    probs = schedule.check_templates(tpl, r["assumptions"])
    assert any("lcc-ratio" in x and "no resource" in x for x in probs)
    assert any("lcc-certificate" in x and "astrologer" in x for x in probs)
    assert all(x.startswith("C45") for x in probs)


def test_dependencies_follow_the_bid_logic(r):
    p = full_plan(r)
    a = acts(p)
    d = lambda x: date.fromisoformat(x)                                               # noqa: E731

    def before(first, then):
        assert first in a[then]["predecessors"] or any(first in a[x]["predecessors"] for x in a[then]["predecessors"]), \
            (first, then)
        assert d(a[first]["latest_finish"]) <= d(a[then]["latest_start"]), (first, then)

    for signed in ("form-4a", "form-4c-sign", "form-4e", "form-4f", "form-4g-sign", "investment-licence"):
        before("poa", signed)                                       # Powers of Attorney before signatures
    before("bond-approval", "bond-issue")                            # bond after bank approval
    before("fin-model-freeze", "model-audit-opinion")                # audit opinion on a frozen model
    before("fin-model-freeze", "form-4f")                            # Form 4-F from the model
    before("assemble-envelope-a", "copies")                          # copies after assembly
    before("assemble-envelope-b", "copies")
    before("copies", "seal-and-mark")
    before("seal-and-mark", "deliver")                               # both envelopes sealed before delivery
    for x, v in a.items():                                           # every Envelope B document feeds assembly B
        if v["envelope"] == "B" and v["item"]:
            assert x in a["assemble-envelope-b"]["predecessors"], x
        if v["envelope"] == "A" and v["item"]:
            assert x in a["assemble-envelope-a"]["predecessors"], x
    assert a["deliver"]["latest_finish"] == p["anchors"]["PDD"]
    # sealing takes no Working Day of its own: done at the end of the copies day
    assert a["seal-and-mark"]["duration_wd"] == 0 and a["seal-and-mark"]["latest_start"] == a["copies"]["latest_finish"]


# ============================================================================ documents

def test_both_envelopes_appear_with_their_items(r, base):
    tot = {t["envelope"]: t for t in base["documents"]["totals"]}
    assert set(tot) == {"A", "B"}
    p = full_plan(r)
    tot = {t["envelope"]: t for t in p["documents"]["totals"]}
    assert {"EV-FORM-4A", "EV-FORM-4C", "EV-BID-BOND", "EV-POA", "EV-TECH-PROPOSAL", "EV-FORM-4G"} <= set(tot["A"]["evidence"])
    assert {"EV-FORM-4F", "EV-FIN-MODEL", "EV-MODEL-AUDIT", "EV-FIN-ASSUMPTIONS"} <= set(tot["B"]["evidence"])
    for e in ("A", "B"):
        t = tot[e]
        assert t["physical_count"] == t["marked_originals"] + t["hard_copies"] == 4 * t["documents"] > 0
        assert t["usb"] == 1
    # Envelope B: VOL-I 10.1 says 'only' Form 4-F and the Financial Model -> the other two are an open issue
    items = {i["evidence"]: i for i in p["documents"]["items"]}
    assert any(f.startswith("OPEN ISSUE") for f in items["EV-MODEL-AUDIT"]["flags"])
    assert not any(f.startswith("OPEN ISSUE") for f in items["EV-FORM-4F"]["flags"])
    # actions are listed but not counted in the copies
    assert items["EV-DELIVERY"]["kind"] == "action" and items["EV-DELIVERY"]["physical_count"] == 0


@pytest.mark.parametrize("members", [2, 3, 4])
def test_document_counts_follow_the_member_count(r, mk, members):
    p = mk(with_(r["assumptions"], bidder={"members": members}))
    items = {i["evidence"]: i for i in p["documents"]["items"]}
    per_member = [k for k, i in items.items() if i["per"] in ("member", "signatory")]
    assert "EV-FORM-4C" in per_member
    for k in per_member:
        assert items[k]["multiplicity"] == members                        # 1 signatory per member (assumption)
        assert items[k]["physical_count"] == 4 * members                 # 1 marked original + 3 hard copies
    assert acts(p)["form-4c-sign"]["count"] == members


def test_member_scenarios_change_document_totals_in_step(scen):
    a = {row["scenario"]: row for row in scen["comparison"]}
    assert a["consortium-2"]["physical_A"] < a["consortium-2"]["physical_A_base"] < a["consortium-4"]["physical_A"]
    assert any(c.startswith("EV-FORM-4C: x3 -> x2") for c in a["consortium-2"]["document_changes"])
    assert any(c.startswith("EV-FORM-4C: x3 -> x4") for c in a["consortium-4"]["document_changes"])


# ============================================================================ feasibility, drivers, scenarios

def test_drivers_name_the_lead_time_behind_each_infeasible_activity(r, base, scen):
    for p in [base] + [s["programme"] for s in scen["scenarios"].values()]:
        drv = {d["activity"]: d for d in p["drivers"]}
        for a in p["activities"]:
            if not a["status"].startswith(("INFEASIBLE", "DEADLINE PASSED")):
                assert a["id"] not in drv
                continue
            d = drv[a["id"]]
            assert a["duration_assumption"] in d["lead_times"]
            assert d["chain"][0] == a["id"] and acts(p)[d["chain"][-1]]["deadline_rule"]
            assert all("PROVISIONAL ASSUMPTION" in x for x in d["lead_time_values"])
            if a["status"].startswith("INFEASIBLE"):
                assert a["status"] == f"INFEASIBLE by {d['shortfall_wd']} WD"


def test_lcc_is_infeasible_at_the_validated_stage_and_its_driver_threshold_is_exact(r, mk, base):
    lcc = acts(base)["lcc-certificate"]
    assert lcc["status"].startswith("INFEASIBLE")
    d = next(x for x in base["drivers"] if x["activity"] == "lcc-certificate")
    assert d["chain"][-1] == "deliver" and d["deadline"].startswith("PDD")
    m = next(re.match(r"lcc_certificate <= (\d+) WD", o) for o in d["would_make_feasible"] if o.startswith("lcc_certificate"))
    n = int(m.group(1))
    ok = mk(with_(r["assumptions"], lead_times={"lcc_certificate": {"value": n}}))
    late = mk(with_(r["assumptions"], lead_times={"lcc_certificate": {"value": n + 1}}))
    assert acts(ok)["lcc-certificate"]["status"] == "OK"
    assert acts(late)["lcc-certificate"]["status"] == "INFEASIBLE by 1 WD"
    assert "SCENARIO test: 30 -> " in acts(late)["lcc-certificate"]["duration_basis"]    # an override is labelled


def test_a_shorter_lcc_lead_time_makes_it_feasible_or_reduces_the_shortfall(r, base, scen):
    s = scen["scenarios"]["lcc-15wd"]
    b, a = acts(base)["lcc-certificate"], acts(s["programme"])["lcc-certificate"]
    short = lambda st: int(re.search(r"by (\d+) WD", st).group(1)) if st.startswith("INFEASIBLE") else 0  # noqa: E731
    assert short(a["status"]) < short(b["status"])
    assert a["duration_wd"] == 15 and a["duration_basis"].startswith("ASSUMPTION") and "SCENARIO lcc-15wd" in a["duration_basis"]
    # session 08 (owner: forward pass and float): the shortfall is the negative total float of the whole LCC chain
    # (ratio + certificate from the planning date), 12 WD, and it runs on to the delivery; 15 WD clears all of it
    assert "lcc-certificate: INFEASIBLE by 12 WD -> OK" in s["changes"]["status_changes"]
    assert "deliver: INFEASIBLE by 12 WD -> OK" in s["changes"]["status_changes"]


def test_a_declared_holiday_moves_latest_starts_earlier(r, mk, base):
    hol = "2026-11-16"                                       # a Monday inside the bid window (hypothetical)
    p = mk(with_(r["assumptions"], calendar={"holidays": [hol]}))
    b, h = acts(base), acts(p)
    assert h["deliver"]["latest_finish"] == b["deliver"]["latest_finish"]          # the PDD is a stated date
    for k, x in b.items():
        assert h[k]["latest_start"] <= x["latest_start"], k                        # never later
        if x["latest_start"] < hol and k != "attendance-notice":                   # (its deadline is before the holiday)
            assert h[k]["latest_start"] < x["latest_start"], k                     # its chain to its deadline crosses it
    assert sum(h[k]["latest_start"] < x["latest_start"] for k, x in b.items()) >= 5
    # a pack date counted in Working Days moves too (the register is re-evaluated with the new calendar)
    if "clarifications" in b:
        assert h["clarifications"]["latest_finish"] < b["clarifications"]["latest_finish"]


def test_hypothetical_holiday_scenario_is_labelled_and_lengthens_shortfalls(scen):
    s = scen["scenarios"]["hypothetical-holidays"]
    assert s["hypothetical"] and "HYPOTHETICAL" in s["purpose"]
    row = next(x for x in scen["comparison"] if x["scenario"] == "hypothetical-holidays")
    assert row["infeasible"] >= row["infeasible_base"] and row["activities_moved"] > 0


def test_resources_compare_staff_load_with_provisional_capacity(r, base):
    # session 08 (owner: effort vs waiting, show overloads): one row per role per Working Day; the load is staff
    # effort (person-days) spread over the late window, compared with the capacity in staff per Working Day
    rows = base["resources"]["rows"]
    assert rows and {x["resource"] for x in rows} <= set(r["assumptions"]["resources"])
    for x in rows:
        assert x["status"] == ("OVERLOAD" if x["load_wd"] > x["capacity"] else "OK")
        assert re.fullmatch(r"\d{4}-W\d{2}", x["iso_week"]) and x["capacity_basis"].startswith("PROVISIONAL")
        assert r["cal"].is_working_day(date.fromisoformat(x["date"]))
    # cutting every capacity to one can only add overloaded days
    tight = copy.deepcopy(r["assumptions"])
    for v in tight["resources"].values():
        v["capacity"] = 1
    over = lambda p: {(x["resource"], x["date"]) for x in p["resources"]["rows"] if x["status"].startswith("OVERLOAD")}  # noqa: E731
    assert over(base) <= over(programme.extend(base, r["evidence_items"], tight, r["cal"]))


def test_an_override_naming_nothing_is_rejected(r):
    with pytest.raises(ValueError, match="lcc_certifcate"):
        programme.apply_overrides(r["assumptions"], {"lead_times": {"lcc_certifcate": {"value": 1}}}, "typo")
    assert r["assumptions"]["lead_times"]["lcc_certificate"]["value"] == 30          # the original is not touched


def test_every_scenario_has_a_purpose_and_runs(scen):
    assert set(scen["scenarios"]) >= {"consortium-2", "consortium-4", "lcc-15wd", "hypothetical-holidays"}
    assert len(scen["comparison"]) == len(SCENARIOS["scenarios"]) >= 5
    for row in scen["comparison"]:
        assert row["purpose"] and row["overrides"]


# ============================================================================ outputs

def test_write_is_complete_and_deterministic(base, scen, tmp_path):
    hashes = []
    for name in ("a", "b"):
        programme.write(base, scen, tmp_path / name)
        hashes.append({p.relative_to(tmp_path / name).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in sorted((tmp_path / name).rglob("*")) if p.is_file()})
    assert hashes[0] == hashes[1]
    for stem in ("programme", "marshalling", "documents", "resources", "overloads", "disciplines", "milestones", "drivers",
                 "scenario_comparison"):
        assert f"a5/{stem}.csv" in hashes[0] and f"a5/{stem}.json" in hashes[0], stem
    for f in ("a5/gantt.svg", "a5/gantt.html", "a5/gantt.pdf", "a5/README.md"):
        assert f in hashes[0], f
    for s in SCENARIOS["scenarios"]:
        assert f"a5/scenarios/{s}.csv" in hashes[0]
    doc = yaml.safe_load((tmp_path / "a" / "a5/documents.json").read_text(encoding="utf-8"))
    assert {"TOTAL Envelope A", "TOTAL Envelope B"} <= {x["evidence"] for x in doc["rows"]}
    assert "PROVISIONAL" in doc["notice"]
    marsh = yaml.safe_load((tmp_path / "a" / "a5/marshalling.json").read_text(encoding="utf-8"))["rows"]
    lcc = next(m for m in marsh if m["activity"] == "lcc-certificate")
    assert lcc["envelope"] == "A" and lcc["physical_count"] == 4 and lcc["status"].startswith("INFEASIBLE")
    assert only_owner_approvals()
