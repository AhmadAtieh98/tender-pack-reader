"""Session 12 (W3b; the owner's part 2): calculated deadlines reach A1 and A5 (blind-05 follow-up 7; the key's S1, S2,
S6, DD3-DD5, DD8).

Blind-05 computed Tue 24 Nov (the merged 6.6's modification cut-off), Mon 23 Nov (7.3's Portal notice) and the Base Date
in its analysis statements, but none became an A1 date or an A5 milestone, the Base Date was given two dates on a
counting doubt the words do not raise, and the Working Days left from the issue date to the PDD were never stated. Now:
  * calc.deadline counts "N <unit> before/after X" under the counting rules of config/formulas.yaml (`counting`, each
    with its source: VOL-I 2.4 for Working Days counted backwards). Exactly one reading when a rule covers the case;
    otherwise the result is `ambiguous`, with every reading, and escalated, never chosen;
  * derived.computed_deadlines finds every such phrase in the addendum's provisions and the units it changes, with the
    inputs (the words, the anchor and its date), the counting rule, the result and the calc fingerprint; a deadline of a
    conditional obligation is conditional; the downstream phase gets a task per deadline (a milestone proposal with
    `computed_from`), and the validator recomputes what a proposal claims;
  * the candidate A5 README, the candidate A3 and the review packet state the Working Days left from the addendum's
    issue date to the PDD and list the computed milestones as PROPOSED (nothing typed)."""
from __future__ import annotations

import copy

import pytest

import s12_blind05 as F
import s12_w3b as W
from tenderpack import calc, derived, partial, programme
from tenderpack.ai import downstream as DS
from tenderpack.ai.contract import EvidenceRef
from tenderpack.dates import Calendar

CAL = Calendar(weekend={4, 5})
PDD = {"name": "PDD", "date": "2026-11-26"}


def _off(n, unit, words):
    return {"name": "period", "value": n, "unit": unit, "source": {"unit": "ADD-03:7.3", "page": 3, "words": words}}


def test_working_days_before_have_one_reading_under_vol_i_2_4():
    r = calc.compute("deadline", {"offset": _off(3, "Working Days", "three (3) Working Days"), "anchor": PDD,
                                  "direction": "before"}, calendar=CAL)
    assert r["status"] == "resolved" and r["value"] == "2026-11-23", r
    assert r["counting"]["source"]["unit"] == "VOL-I:2.4" and len(r["readings"]) == 1
    r2 = calc.compute("deadline", {"offset": _off(2, "Working Days", "two (2) Working Days"), "anchor": PDD,
                                   "direction": "before"}, calendar=CAL)
    assert r2["value"] == "2026-11-24" and r2["fingerprint"] != r["fingerprint"]


def test_calendar_days_before_have_one_reading_under_the_registry():
    r = calc.compute("deadline", {"offset": _off(28, "days", "twenty-eight (28) days"), "anchor": PDD,
                                  "direction": "before"}, calendar=CAL)
    assert r["status"] == "resolved" and r["value"] == "2026-10-29", r
    assert r["counting"]["id"] in calc.load_registry()["counting"]


def test_a_count_the_rules_do_not_cover_is_ambiguous_and_escalated():
    r = calc.compute("deadline", {"offset": _off(5, "Working Days", "five (5) Working Days"),
                                  "anchor": {"name": "issue", "date": "2026-11-15"}, "direction": "after"}, calendar=CAL)
    assert r["status"] == "ambiguous" and r["value"] is None and r["escalate"]
    assert len({x["value"] for x in r["readings"]}) == 2 and "not stated" in r["reason"]


def test_an_unknown_anchor_or_a_typed_value_is_unresolved():
    r = calc.compute("deadline", {"offset": _off(30, "days", "thirty (30) days"),
                                  "anchor": {"name": "crane erection", "date": None}, "direction": "before"}, calendar=CAL)
    assert r["status"] == "unresolved" and r["value"] is None
    r = calc.compute("deadline", {"offset": _off("three", "Working Days", "three (3) Working Days"), "anchor": PDD,
                                  "direction": "before"}, calendar=CAL)
    assert r["status"] == "unresolved"                                  # a value that is not a literal number


# ---------------------------------------------------------------------------------------------- blind-05

@pytest.fixture(scope="module")
def r(tmp_path_factory):
    return F.run(tmp_path_factory)["r"]


def test_the_addendums_deadlines_are_computed_with_their_inputs(r):
    cd = {x["unit"]: x for x in derived.computed_deadlines(r, "ADD-03")}
    n = cd["ADD-03:7.3"]
    assert n["result"]["value"] == "2026-11-23" and n["result"]["status"] == "resolved"
    assert "three (3) Working Days before the Proposal Due Date" in n["words"] and n["anchor"] == "PDD"
    assert n["computed_from"]["method"] == "deadline" and n["computed_from"]["result"] == "2026-11-23"
    assert n["computed_from"]["inputs"]["anchor"]["date"] == "2026-11-26" and n["computed_from"]["fingerprint"]
    assert n["conditional"], n                                          # only a Bidder whose Proposal provides for ...
    assert cd["ADD-03:2.1"]["result"]["value"] == "2026-11-24"
    assert cd["VOL-V:1.1+ADD-03"]["result"]["value"] == "2026-10-29"   # the Base Date: one reading


def test_the_working_days_left_are_stated(r):
    w = derived.working_days_left(r, "ADD-03")
    assert (w["issued"], w["pdd"], w["working_days"]) == ("2026-11-15", "2026-11-26", 9)
    assert "VOL-I 2.4" in w["calendar"] and "not counted" in w["convention"]


def test_the_candidate_a5_and_a3_state_them(r):
    cand = partial.compute(r)
    readme = programme.candidate_readme(cand["a5"], cand["paragraph"])
    assert "Working Days left from the issue date (2026-11-15) to the PDD (2026-11-26): 9" in readme
    assert "2026-11-23" in readme and "ADD-03:7.3" in readme and "PROPOSED" in readme
    md = partial.markdown(cand)
    assert "Working Days left from the issue date (2026-11-15) to the PDD (2026-11-26): 9" in md


def test_the_review_packet_lines_state_them(r):
    lines = "\n".join(derived.review_lines(derived.summary(r, "ADD-03")))
    assert "Working Days left from the issue date (2026-11-15) to the PDD (2026-11-26): 9" in lines
    assert "2026-11-24" in lines and "computed" in lines


# ---------------------------------------------------------------------------------------------- downstream

@pytest.fixture(scope="module")
def ws(tmp_path_factory):
    return W.workspace(tmp_path_factory)


@pytest.fixture(scope="module")
def prom(ws):
    return W.promoted(ws)


def test_a_task_per_computed_deadline(ws, prom):
    ts, _ = W.tasks(ws, prom)
    t = next((x for x in ts if x["id"] == "date:ADD-03:7.3"), None)
    assert t is not None and t["kind"] == "computed_date", sorted({x["kind"] for x in ts})
    assert t["computed_from"]["result"] == "2026-11-23" and t["conditional"]
    assert "milestone" in t["expect"] and "computed_from" in t["expect"]


def _act(ws, computed_from, aid="portal-height-notice"):
    a = copy.deepcopy(next(t for t in ws.r["templates"]["EV-TECH-PROPOSAL"] if t["id"] == "technical-proposal"))
    a.update(id=aid, name="Notify the Authority through the Portal of the zone and height of any "
             "structure over 30 m (ADD-03 7.3)", milestone=True, computed_from=computed_from)
    return a


def test_the_validator_recomputes_a_milestone_claim(ws, prom):
    t = next(x for x in W.tasks(ws, prom)[0] if x["id"] == "date:ADD-03:7.3")
    good = copy.deepcopy(t["computed_from"])
    bad = dict(copy.deepcopy(good), result="2026-11-22")
    ev = EvidenceRef(doc="ADD-03", unit_id="ADD-03:7.3", page=3, kind="span",
                     words="not later than three (3) Working Days before the Proposal Due Date")
    items = [{"id": f"M{i}", "statement_type": "activity", "task": "date:ADD-03:7.3", "provision": "ADD-03:7.3",
              "payload": {"evidence_item": "EV-TECH-PROPOSAL", "activity": _act(ws, cf, f"portal-height-notice-{i}"),
                          "rows": ["VOL-I-9.2-01"]},
              "evidence": [ev]} for i, cf in enumerate((good, bad))]
    ds = W.dset(ws, items)
    DS.validate(ws, ds, prom, {"date:ADD-03:7.3": "computed_date"})
    ok, wrong = ds.items
    rec = next(v for v in ok.validation if v.check == "computed_from")
    assert rec.ok and "2026-11-23" in rec.detail
    assert wrong.verification_status == "invalid" and any(v.check == "computed_from" and not v.ok for v in wrong.validation)


NOTICE = {"id": "ADD-03-7.3-01", "group": "ADD-03:7.3", "scope": ["submission", "portal"],
          "requirement": "Portal notice of the zone and height of anything over 30 m, not later than three Working Days "
                         "before the PDD (test data)",
          "units": ["ADD-03:7.3"], "discipline": "Technical", "assessment": "procedural", "evidence": [],
          "no_deliverable": "a Portal notice (test data)",
          "interpretations": [{"stage": "ADD-03",
                               "quote": "not later than three (3) Working Days before the Proposal Due Date"}],
          "date_rules": [{"rule_id": "ADD-03-7.3-01-R1", "kind": "relative", "purpose": "deadline", "anchor": "PDD",
                          "offset": 3, "unit": "working_day", "direction": "before", "source_unit": "ADD-03:7.3",
                          "text": "not later than three (3) Working Days before the Proposal Due Date"}],
          "confidence": "medium", "confidence_reason": "test data"}


def test_a1_shows_the_computed_date_with_its_derivation_and_a5_plans_the_milestone(tmp_path_factory):
    from tenderpack import stage2
    tmp = tmp_path_factory.mktemp("s12w3b-dates")
    rr = stage2.run(F.build(tmp_path_factory), W.copy_candidate(tmp, rows=[NOTICE]), F.ROOT)
    a1 = stage2.a1_table(rr, [])
    sh = a1["sheets"]["Dates"]
    d = next(x for x in (sh.get("rows") if isinstance(sh, dict) else sh) if x["row"] == "ADD-03-7.3-01"
             and x["stage"] == "ADD-03")
    assert d["planning"].startswith("2026-11-23") and "= computed: calc deadline 2026-11-23" in d["planning"]
    assert "VOL-I:2.4" in d["planning"] and "fingerprint" in d["planning"]
    prog = programme.stage_planner(rr, "ADD-03")(rr["assumptions"])
    assert any("2026-11-23" in str(m.get("date")) and "ADD-03-7.3-01" in str(m) for m in prog["milestones"]), \
        [m for m in prog["milestones"]][:3]
