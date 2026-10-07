"""Session 14 (W4), part 4: preparation readiness versus finalisation requiring a decision (report section 9 G7), and
Form 4-E against the whole proposal (VOL-I 9.6: "a qualification elsewhere in the Proposal").

Readiness (programme.readiness): every A5 activity says apart (a) whether its preparation can start (its inputs: the
predecessors and the earliest start) and (b) what its finalisation needs: a gate (GATED), the open decisions of the
rows it carries (HUMAN DECISION PENDING; a note while planning.gate_on_open_decisions stays off, the owner's pending
choice), or nothing. Shown in programme.csv/json (columns `preparation`, `finalisation`), gantt.html's table, the
Gantt (an amber tick at the date the finalisation needs the decision by) and the review cards of the rows the activity
carries. No approval is invented; no duration or setting changes.

Form 4-E (programme.form_4e_checks): every document of the Proposal (the documents placed in Envelope A or B: the
direct inputs of the envelope assembly steps) is checked against Form 4-E's finalisation, each check citing the clause
that places the document in the Proposal (VOL-I 9.1 item, 10.1, 10.3, 10.6) and VOL-I 9.6. A document final only after
Form 4-E starts cannot be cross-checked; the what-if that makes Form 4-E wait for every document is computed on the same
network (no duration changed) and an infeasibility is reported as a finding for a person, never resolved. The open
issues of the rows each document's activity carries are named beside it (e.g. the guarantee's wording, Form 4-G's
'No', the Envelope A prices)."""
from __future__ import annotations

from datetime import date

import pytest

from tenderpack import batches, programme, stage2
from tenderpack.dates import Calendar
from tenderpack.util import ROOT


def _act(i, preds=(), dur=1, **kw):
    return {"id": i, "name": i, "predecessors": list(preds), "duration_wd": dur, "duration_assumption": f"k_{i}",
            "earliest_start": "2026-11-01", "status": "OK", "decision_status": "READY", "req_ids": [], **kw}


def test_readiness_separates_preparation_from_finalisation_synthetic():
    a = _act("tp", ["ground"], earliest_start="2026-11-10", open_decisions=["I-X"],
             open_decision_words={"I-X": "the ranges (Process engineer)"}, decision_needed_by="2026-11-11")
    prep, fin = programme.readiness(a)
    assert prep == "PREPARATION READY: can start 2026-11-10 (after ground)"
    assert fin.startswith("FINALISATION NEEDS A DECISION: I-X: the ranges (Process engineer) by 2026-11-11")
    assert "HUMAN DECISION PENDING" in fin and "planning.gate_on_open_decisions is off" in fin
    g = _act("f4a", [], gated_by=["I-F"], decision_needed_by="2026-11-11",
             decision_status="GATED: finalisation waits on I-F")
    prep, fin = programme.readiness(g)
    assert prep == "PREPARATION READY: can start 2026-11-01 (inputs known; no predecessor)"
    assert fin.startswith("FINALISATION GATED: needs a person's decision on I-F by 2026-11-11")
    assert programme.readiness(_act("x"))[1] == "FINALISATION: no pending decision on the rows it carries"
    late = _act("y", status="INFEASIBLE by 3 WD")
    assert programme.readiness(late)[0].startswith("PREPARATION READY: can start 2026-11-01") and \
        "timing INFEASIBLE by 3 WD" in programme.readiness(late)[0]
    assert programme.readiness(_act("z", status="CONDITIONAL — window elapsed"))[0].startswith("NOT SCHEDULED")


def test_readiness_by_row_and_card_synthetic():
    acts = [_act("tp", req_ids=["R-1"], preparation="PREPARATION READY: x", finalisation="FINALISATION GATED: y")]
    by = programme.readiness_by_row({"activities": acts})
    assert by == {"R-1": ["tp: PREPARATION READY: x; FINALISATION GATED: y"]}
    h = batches.readiness_block_html(by["R-1"])
    assert "preparation and finalisation" in h and "FINALISATION GATED" in h


def test_form_4e_checks_synthetic():
    cal = Calendar()
    acts = [_act("dev", [], 3), _act("tp", [], 5), _act("bond", [], 8), _act("f4f", [], 12),
            _act("form-4e", ["dev", "tp"], 2), _act("assemble-envelope-a", ["form-4e", "tp", "bond"], 1),
            _act("assemble-envelope-b", ["f4f"], 1), _act("deliver", ["assemble-envelope-a", "assemble-envelope-b"], 1,
                                                         deadline_date="2026-11-20")]
    for a in acts:
        a["envelope"] = {"bond": "A", "tp": "A", "f4f": "B", "dev": "A", "form-4e": "A"}.get(a["id"], "A+B")
    env = {"A": "VOL-I 9.1", "B": "VOL-I 10.1"}
    prog = {"activities": acts, "status_date": "2026-11-01", "planning_date": "2026-11-01"}
    net = programme.network({a["id"]: {"duration_wd": a["duration_wd"], "predecessors": a["predecessors"],
                                       "deadline_date": date(2026, 11, 20) if a["id"] == "deliver" else None,
                                       "buffer_wd": 0} for a in acts}, cal, date(2026, 11, 1))
    for a in acts:
        t = net[a["id"]]
        a.update(earliest_start=t["es"].isoformat(), earliest_finish=t["ef"].isoformat(),
                 latest_start=t["ls"].isoformat() if t["ls"] else None,
                 latest_finish=t["lf"].isoformat() if t["lf"] else None, float_wd=t["float_wd"])
    res = programme.form_4e_checks(prog, cal, clause_of=lambda a: env[a["envelope"]],
                                   issues_of=lambda a: ["I-BOND"] if a["id"] == "bond" else [])
    by = {c["document_activity"]: c for c in res["checks"]}
    assert set(by) == {"tp", "bond", "f4f"}                              # every Proposal document but Form 4-E
    assert by["tp"]["status"] == "checked (finalised before Form 4-E)"
    assert by["bond"]["status"].startswith("NOT CHECKABLE") and by["f4f"]["status"].startswith("NOT CHECKABLE")
    assert "VOL-I 9.6" in by["bond"]["clause"] and "VOL-I 9.1" in by["bond"]["clause"]
    assert "VOL-I 10.1" in by["f4f"]["clause"] and by["bond"]["open_issues"] == ["I-BOND"]
    w = res["what_if"]
    assert w["added_predecessors"] == ["bond", "f4f"] and w["form_4e_earliest_finish"] > by["f4f"]["finish"]
    assert w["feasible"] is False and w["shortfall_wd"] > 0
    assert res["findings"] and "a person" in res["findings"][0] and "INFEASIBLE" in res["findings"][0]


@pytest.fixture(scope="module")
def real():
    r = stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)
    progs = stage2.a5_all(r)
    return r, progs[r["validated"].stage]


def test_real_programme_states_readiness_apart(real):
    r, prog = real
    acts = {a["id"]: a for a in prog["activities"]}
    assert all(a.get("preparation") and a.get("finalisation") for a in acts.values())
    f4e = acts["form-4e"]
    assert f4e["preparation"].startswith("PREPARATION READY")
    assert f4e["finalisation"].startswith("FINALISATION NEEDS A DECISION") and "I-CONCESSION" in f4e["finalisation"]
    assert acts["form-4a"]["finalisation"].startswith("FINALISATION GATED")
    assert "preparation" in programme.PROGRAMME_COLS and "finalisation" in programme.PROGRAMME_COLS
    # nothing invented: the decision status keeps READY (the gate rule is the owner's pending choice)
    assert f4e["decision_status"] == "READY"
    by_row = programme.readiness_by_row(prog)
    assert any(x.startswith("form-4e: PREPARATION READY") for x in by_row["VOL-I-9.6-01"])


def test_real_form_4e_checks(real):
    r, prog = real
    res = programme.form_4e_checks_for(r, prog)
    docs = {c["document_activity"]: c for c in res["checks"]}
    for a in ("technical-proposal", "bond-issue", "pcg-execution", "form-4b", "form-4c-sign", "form-4g-sign",
              "form-4f", "fin-model-freeze", "fin-assumptions", "model-audit-opinion"):
        assert a in docs, a
    assert "form-4e" not in docs and "ground-dd" not in docs              # not a Proposal document
    assert docs["technical-proposal"]["status"].startswith("checked")
    assert "VOL-I 9.1(g)" in docs["bond-issue"]["clause"] and "VOL-I 9.6" in docs["bond-issue"]["clause"]
    assert "VOL-I 10.1" in docs["form-4f"]["clause"] and "VOL-I 10.6" in docs["fin-assumptions"]["clause"]
    assert "VOL-I 9.1(d)" in docs["pcg-execution"]["clause"]
    assert "I-F4D-WORDING" in docs["pcg-execution"]["open_issues"]
    assert res["what_if"]["added_predecessors"]
    assert res["findings"]                                              # reported for a person either way
    assert all("a person" in f for f in res["findings"])
    # the commercial-qualification tension is named with its three clauses, never resolved
    assert any("VOL-I 6.2" in f and "VOL-I 10.5" in f and "VOL-I 9.6" in f for f in res["findings"])
    assert prog.get("form_4e_checks") == res
