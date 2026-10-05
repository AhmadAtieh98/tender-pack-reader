"""Session 12 (W3b; the owner's part 2): conditional obligations and indirect effects reach the affected rows, and
derived consequences are proposed only within the pack's own rules (blind-05 follow-ups 8 and 9; the key's S5, IE1-IE3,
D1 and the A3 delta).

  * A condition switched on: VOL-II 3.2 applies "Where a membrane process is proposed"; ADD-03 4.1 makes a membrane
    filtration step mandatory in VOL-II 3.1. Blind-05 left 3.2's rows untouched (S5 missed). The rows of a unit whose
    condition an op's words now make always (or never) true are flagged "condition changed by <op>: re-read" in the
    register (A1's change column, the candidate A3), a downstream task is made for a person, and an earlier answer
    that relied on the conditional unit goes through the superseded-answer list (stage2.answers_to_review).
  * A definition changed: ADD-03 3.1 amends "Availability Payment means ..." (VOL-V 1.1); rows whose units use the
    term (VOL-I 10.2, 11.5, Form 4-F) are flagged "definition of 'Availability Payment' changed by <op>: re-read".
  * Derived consequences: ADD-03 3.3 sets a band (an Indexed Proportion of 50 % to 70 %). An EXISTING
    non-responsiveness rule (VOL-I 10.5) may be proposed as the consequence of a value outside it, quoting that rule's
    words: PROPOSED, and human-owned when the rule's words do not themselves name the value (W1's rule). A consequence
    the pack does not state is invalid; where no rule covers the band the task says "no bid-out consequence stated".
Nothing is decided: every flag asks a person to re-read; the conditional unit's status is unchanged."""
from __future__ import annotations

import pytest

import s12_blind05 as F
import s12_w3b as W
from tenderpack import derived, human_owned as H, partial, stage2
from tenderpack.ai import downstream as DS
from tenderpack.ai.contract import EvidenceRef
from tenderpack.util import ROOT


@pytest.fixture(scope="module")
def r(tmp_path_factory):
    return F.run(tmp_path_factory)["r"]


@pytest.fixture(scope="module")
def real():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


def _ev(r, rid, stage):
    return next(e for e in r["evals"] if e["row"].id == rid)["stages"][stage]


# ---------------------------------------------------------------------------------------------- conditions

def test_a_condition_switched_on_is_found(r):
    sw = {(x["unit"], x["kind"]): x for x in derived.switched(r, "ADD-03")}
    c = sw[("VOL-II:3.2", "condition")]
    assert c["op"] == "ADD-03/4.1" and c["changed_unit"] == "VOL-II:3.1" and "membrane" in c["terms"]
    assert "Where a membrane process is proposed" in c["condition"]
    assert c["flag"].startswith("condition changed by ADD-03/4.1: re-read")


def test_the_rows_of_the_conditional_unit_are_flagged_at_that_stage_only(r):
    for rid in ("VOL-II-3.2-01", "VOL-II-3.2-02"):
        assert any(f.startswith("condition changed by ADD-03/4.1: re-read") for f in _ev(r, rid, "ADD-03")["flags"])
        assert not any("condition changed" in f for f in _ev(r, rid, "ADD-02")["flags"])
        assert _ev(r, rid, "ADD-03")["status"] == "ACTIVE"                 # nothing decided: the status is unchanged


def test_a_changed_definition_reaches_the_rows_using_the_term(r):
    sw = [x for x in derived.switched(r, "ADD-03") if x["kind"] == "definition"]
    d = next(x for x in sw if x["term"] == "Availability Payment")
    assert d["op"] == "ADD-03/3.1" and d["unit"] == "VOL-V:1.1"
    for rid in ("VOL-I-10.2-01", "VOL-I-11.5-01", "VOL-IV-F4F-02"):
        assert any("definition of 'Availability Payment' changed by ADD-03/3.1: re-read" in f
                   for f in _ev(r, rid, "ADD-03")["flags"]), (rid, _ev(r, rid, "ADD-03")["flags"])


def test_a1_and_the_candidate_a3_show_it(r):
    a1 = stage2.a1_table(r, [])
    rec = next(x for x in a1["rows"] if x["id"] == "VOL-II-3.2-01")
    assert "condition changed by ADD-03/4.1" in rec["change:ADD-03"]
    cand = partial.compute(r)
    row = next(x for sec in ("explicit", "none_stated", "score", "refused", "zero")
               for x in cand["a3"].get(sec) or [] if x.get("id") == "VOL-I-11.5-01")
    assert any("definition of 'Availability Payment' changed by ADD-03/3.1" in f for f in row["flags"]), row["flags"]


def test_the_downstream_phase_gets_a_task_and_answers_go_through_the_reread_list(r, tmp_path_factory):
    ws = W.workspace(tmp_path_factory)
    ts, _ = W.tasks(ws, W.promoted(ws))
    t = next((x for x in ts if x["id"] == "cond:VOL-II:3.2"), None)
    assert t is not None and t["kind"] == "condition_changed"
    assert set(t["scope"]["rows"]) >= {"VOL-II-3.2-01", "VOL-II-3.2-02"} and t["op"] == "ADD-03/4.1"
    # an earlier answer relying on the conditional unit is listed for a re-read (W3a's mechanism, not a copy of it)
    s3 = next(s for s in r["stages"] if s.stage == "ADD-03")
    assert "VOL-II:3.2" in derived.switched_units(r, s3)
    ids = [x["id"] for x in ts]
    assert len(ids) == len(set(ids))


def test_the_real_pack_has_no_switched_condition_where_none_switched(real):
    # BASE -> ADD-01 -> ADD-02: no op adds or removes the words of a clause's condition (checked by hand: VOL-II 3.2's
    # membrane, VOL-V 18.1 and 18.3's PCOD); the definitions ADD-01/ADD-02 change, if any, are listed with their op
    for s in real["stages"][1:]:
        assert [x for x in derived.switched(real, s.stage) if x["kind"] == "condition"] == []


# ---------------------------------------------------------------------------------------------- consequences

def test_a_band_gets_the_existing_bid_out_rules_that_may_cover_it(r):
    c = {x["unit"]: x for x in derived.consequence_candidates(r, "ADD-03")}
    b = c["ADD-03:3.3"]
    assert b["band"]["low"] == 50 and b["band"]["high"] == 70
    rules = {x["row"]: x for x in b["rules"]}
    assert "VOL-I-10.5-01" in rules and rules["VOL-I-10.5-01"]["class"] == "non_responsive"
    assert "price subject to adjustment other than as provided in Volume V" in rules["VOL-I-10.5-01"]["quote"]
    assert not b["silent"]


def test_a_silent_pack_gives_no_bid_out_consequence_stated():
    units = {"X:1": "The Bidder shall state a figure of not less than ten per cent (10%) and not more than twenty per "
                    "cent (20%) of the cost."}
    out = derived.bands_with_rules(units, rules=[])
    assert out and out[0]["silent"] and out[0]["note"] == "no bid-out consequence stated"


BAND_ROW = {"id": "ADD-03-3.3-02", "group": "VOL-V:29.2", "scope": ["commercial", "price"],
            "requirement": "An Indexed Proportion stated in Form 4-F outside 50% to 70% risks non-responsiveness under "
                           "VOL-I 10.5 (proposed for a person)",
            "units": ["ADD-03:3.3"], "discipline": "Commercial", "assessment": "pass_fail", "evidence": ["EV-FORM-4F"],
            "interpretations": [{"stage": "ADD-03",
                                 "quote": "which shall be not less than fifty per cent (50%) and not more than seventy per "
                                          "cent (70%)",
                                 "parameters": {"indexed_proportion_min_pct": 50, "indexed_proportion_max_pct": 70},
                                 "consequence": {"class": "non_responsive", "unit": "VOL-I:10.5",
                                                 "quote": "Any conditional price, price subject to adjustment other than "
                                                          "as provided in Volume V, or alternative price shall render the "
                                                          "Proposal non-responsive."}}],
            "confidence": "low", "confidence_reason": "a derived consequence (test data)"}
EV33 = EvidenceRef(doc="ADD-03", unit_id="ADD-03:3.3", page=1, kind="span",
                   words="which shall be not less than fifty per cent (50%) and not more than seventy per cent (70%)")


def test_a_derived_consequence_is_proposed_and_human_owned(tmp_path_factory):
    ws = W.workspace(tmp_path_factory)
    prom = W.promoted(ws)
    ds = W.dset(ws, [{"id": "C1", "statement_type": "row_new", "task": "cons:ADD-03:3.3", "provision": "ADD-03:3.3",
                      "payload": {"row": dict(BAND_ROW)}, "evidence": [EV33]}])
    DS.validate(ws, ds, prom, {"cons:ADD-03:3.3": "derived_consequence"})
    it = ds.items[0]
    dc = it.payload["row"].get("derived_consequence")
    assert dc and dc["rule"] == "VOL-I-10.5-01" and dc["owner"] == "person", it.payload["row"]
    assert any(v.check == H.CHECK for v in it.validation), [(v.check, v.detail) for v in it.validation]
    assert it.verification_status == "interpretation_pending"


def test_a_consequence_the_pack_does_not_state_is_invalid(tmp_path_factory):
    ws = W.workspace(tmp_path_factory)
    prom = W.promoted(ws)
    row = dict(BAND_ROW, id="ADD-03-3.3-03")
    row["interpretations"] = [dict(BAND_ROW["interpretations"][0], consequence={
        "class": "disqualification", "unit": "ADD-03:3.3",
        "quote": "which shall be not less than fifty per cent (50%) and not more than seventy per cent (70%)"})]
    ds = W.dset(ws, [{"id": "C2", "statement_type": "row_new", "task": "cons:ADD-03:3.3", "provision": "ADD-03:3.3",
                      "payload": {"row": row}, "evidence": [EV33]}])
    DS.validate(ws, ds, prom, {"cons:ADD-03:3.3": "derived_consequence"})
    it = ds.items[0]
    assert it.verification_status == "invalid", [(v.check, v.detail) for v in it.validation]
    assert any(v.check == "derived consequence" and "does not state" in v.detail for v in it.validation)


def test_the_consequence_task_reads_the_price_basis_with_11_5_and_form_4f(tmp_path_factory):
    ws = W.workspace(tmp_path_factory)
    ts, _ = W.tasks(ws, W.promoted(ws))
    t = next((x for x in ts if x["id"] == "cons:ADD-03:3.3"), None)
    assert t is not None and t["kind"] == "derived_consequence"
    rules = {x["row"] for x in t["rules"]}
    assert {"VOL-I-10.5-01", "VOL-I-11.5-01"} <= rules, rules
    assert "VOL-IV-F4F-02" in {x["row"] for x in t["read_with"]}
    assert "no bid-out consequence stated" in t["expect"] and "never" in t["expect"].lower()


def test_an_escalation_on_the_price_basis_carries_the_rules_to_read_it_with(tmp_path_factory):
    # blind-05 D1: Q19 (year 1 prices) against Section 3 (Base Date prices). Escalated here as the drafter would when
    # the provision is unresolved; the task names VOL-I 11.5 and 10.5, never a consequence of its own
    from types import SimpleNamespace
    from tenderpack.ai import downstream as DS
    ws = W.workspace(tmp_path_factory)
    prom = W.promoted(ws)
    ts, _ = DS.tasks(ws, SimpleNamespace(addendum="ADD-03", items=[]), prom,
                     {"ADD-03:Q19": {"needs_person": True, "why": "conflicts with Section 3 (test data)"}})
    t = next(x for x in ts if x["id"] == "esc:ADD-03:Q19")
    assert {"VOL-I-11.5-01"} <= {x["row"] for x in t["bid_out_rules"]}, t["bid_out_rules"]
    assert "never invented" in t["consequence_note"]
