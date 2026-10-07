"""Session 14 (F2): the fixes for the independent rechecks R3 (A5, the rendered files, the review cards) and R2 (the A3
page, A4), failing tests first, each general (no row, issue or rehearsal named in the code).

- R3-14-2 / R2-M1: a Form 4-E check finding that names a judgment is an open decision on the activity it concerns: the
  check (the documents final after Form 4-E starts, the strict order's feasibility) and the judgments (each by the issue
  that mirrors it: the curated issue's `check` names the check and the judgment) are on the form-4e activity wherever it
  appears (programme, Gantt status cell and notes, marshalling).
- R3-14-4: the checks print the finalisation state of each document (prepared / GATED by / NEEDS A DECISION), its
  finalise-by date and whether that is after Form 4-E starts; 'linked' (an input of Form 4-E), never 'final on' for a
  document whose finalisation awaits a person.
- R3-14-3: an open decision whose own words name a deliverable reaches the activities producing it and the Proposal
  documents built from it (the rule followed only the issue's rows; the row that sets the model's term is post-award).
- R3 m1 (the ordering's own cost beside the existing shortfall), m2 (one decision state), m3 (what the decide-by date
  is; a passed date marked), m7 (the clause that puts an inserted form in the Proposal), m8 (Arabic in the cards).
- R2 m1 (A3's dagger from A5's decide-by dates), m2 (one count on the A3 heading), m5 (a high-confidence A3 line names
  its pending judgments), m7 (a question's rows include every row of the pending issue it asks about).
"""
from __future__ import annotations

import copy
from datetime import date

import pytest

from tenderpack import batches, clarify, gantt, programme, stage2
from tenderpack.dates import Calendar
from tenderpack.util import ROOT


def _act(i, preds=(), dur=1, **kw):
    return {"id": i, "name": i, "predecessors": list(preds), "duration_wd": dur, "duration_assumption": f"k_{i}",
            "earliest_start": "2026-11-01", "status": "OK", "decision_status": "READY", "req_ids": [], "flags": [],
            "gated_by": [], **kw}


def _planned(acts, deadline=date(2026, 11, 20), start=date(2026, 11, 1)):
    cal = Calendar()
    net = programme.network({a["id"]: {"duration_wd": a["duration_wd"], "predecessors": a["predecessors"],
                                       "deadline_date": deadline if a["id"] == "deliver" else None, "buffer_wd": 0}
                             for a in acts}, cal, start)
    for a in acts:
        t = net[a["id"]]
        a.update(earliest_start=t["es"].isoformat(), earliest_finish=t["ef"].isoformat(),
                 latest_start=t["ls"].isoformat() if t["ls"] else None,
                 latest_finish=t["lf"].isoformat() if t["lf"] else None, float_wd=t["float_wd"])
    return cal


def _synthetic_prog():
    acts = [_act("dev", [], 3), _act("tp", [], 5), _act("bond", [], 8), _act("f4f", [], 12), _act("f4a", [], 1),
            _act("form-4e", ["dev", "tp"], 2), _act("assemble-envelope-a", ["form-4e", "tp", "bond", "f4a"], 1),
            _act("assemble-envelope-b", ["f4f"], 1),
            _act("deliver", ["assemble-envelope-a", "assemble-envelope-b"], 1, deadline_date="2026-11-20")]
    for a in acts:
        a["envelope"] = {"bond": "A", "tp": "A", "f4f": "B", "dev": "A", "form-4e": "A", "f4a": "A"}.get(a["id"], "A+B")
    cal = _planned(acts)
    by = {a["id"]: a for a in acts}
    by["f4a"].update(gated_by=["I-F"], finalise_by="2026-11-18", decision_needed_by="2026-11-10")
    by["bond"].update(open_decisions=["I-B"], open_decision_words={"I-B": "the bond (Legal)"},
                      decision_needed_by="2026-11-03")
    by["tp"].update(open_decisions=["I-T"], open_decision_words={"I-T": "the ranges (Process engineer)"},
                    decision_needed_by="2026-11-02")
    for a in acts:
        a["preparation"], a["finalisation"] = programme.readiness(a)
    return {"activities": acts, "status_date": "2026-11-01", "planning_date": "2026-11-01"}, cal


def _checks(prog, cal):
    return programme.form_4e_checks(prog, cal, clause_of=lambda a: "VOL-I 9.1",
                                    issues_of=lambda a: list(a.get("open_decisions") or []))


# ---------------------------------------------------------------------------------------------- R3-14-4

def test_r3_14_4_checks_state_the_finalisation_not_final_on_synthetic():
    prog, cal = _synthetic_prog()
    res = _checks(prog, cal)
    by = {c["document_activity"]: c for c in res["checks"]}
    es = next(a for a in prog["activities"] if a["id"] == "form-4e")["earliest_start"]
    # an input of Form 4-E is 'linked' (never 'checked'), and its pending finalisation is said
    assert by["tp"]["status"].startswith("linked"), by["tp"]["status"]
    assert "NEEDS A DECISION" in by["tp"]["status"] and "I-T" in by["tp"]["status"]
    # a gated document whose finalise-by falls after Form 4-E starts cannot be cross-checked
    assert by["f4a"]["status"].startswith("NOT CHECKABLE"), by["f4a"]["status"]
    assert "GATED by I-F" in by["f4a"]["status"] and "finalise by 2026-11-18" in by["f4a"]["status"]
    assert f"after Form 4-E starts on {es}" in by["f4a"]["status"]
    assert by["f4a"]["after_form_4e_start"] is True and by["f4a"]["finalise_by"] == "2026-11-18"
    # an unlinked document awaiting a decision: its earliest finish is not 'final'
    assert "final on" not in by["bond"]["status"] and "earliest finish" in by["bond"]["status"]
    assert "NEEDS A DECISION" in by["bond"]["status"] and "I-B" in by["bond"]["status"]
    assert by["bond"]["finalisation"].startswith("NEEDS A DECISION")
    assert all("earliest_finish" in c and "finish" not in c for c in res["checks"])
    assert "f4a" in res["what_if"]["added_predecessors"] and "tp" not in res["what_if"]["added_predecessors"]


# ---------------------------------------------------------------------------------------------- R3 m1

def test_r3_m1_the_ordering_cost_is_said_beside_the_existing_shortfall_synthetic():
    acts = [_act("late", [], 30), _act("doc", ["late"], 1), _act("tp", [], 2), _act("f4f", [], 12),
            _act("form-4e", ["tp"], 2), _act("assemble-envelope-a", ["form-4e", "doc"], 1),
            _act("assemble-envelope-b", ["f4f"], 1),
            _act("deliver", ["assemble-envelope-a", "assemble-envelope-b"], 1, deadline_date="2026-11-20")]
    for a in acts:
        a["envelope"] = {"doc": "A", "tp": "A", "f4f": "B", "late": "A", "form-4e": "A"}.get(a["id"], "A+B")
    cal = _planned(acts)
    prog = {"activities": acts, "status_date": "2026-11-01", "planning_date": "2026-11-01"}
    w = _checks(prog, cal)["what_if"]
    assert w["feasible"] is False
    assert w["existing_shortfall_wd"] > 0 and w["ordering_cost_wd"] > 0
    assert w["shortfall_wd"] == w["existing_shortfall_wd"] + w["ordering_cost_wd"]
    assert "f4f" in w["newly_late"] and "late" not in w["newly_late"]
    f = _checks(prog, cal)["findings"][0]
    assert f"INFEASIBLE by {w['shortfall_wd']} WD" in f and f"{w['existing_shortfall_wd']} WD" in f
    assert f"the ordering itself adds {w['ordering_cost_wd']} WD" in f


# ---------------------------------------------------------------------------------------------- R3-14-2 / R2-M1

def _curated_with_check_issues():
    return {
        "I-SYN-CROSS": {"text": "how Form 4-E is cross-checked (synthetic)", "owner": "Bid manager",
                        "short": "Form 4-E cross-check against later documents",
                        programme.JUDGMENT_LINK: [f"{programme.JUDGMENT_CHECK}: {programme.CHECK_CROSS}"]},
        "I-SYN-COMM": {"text": "commercial qualification in Form 4-E (synthetic)", "owner": "Legal counsel",
                       "short": "commercial qualification in Form 4-E",
                       programme.JUDGMENT_LINK: f"{programme.JUDGMENT_CHECK}: {programme.CHECK_COMMERCIAL}"},
    }


def test_r3_14_2_check_judgments_are_open_decisions_on_form_4e_synthetic():
    prog, cal = _synthetic_prog()
    res = _checks(prog, cal)
    res["judgments"].append({"key": programme.CHECK_COMMERCIAL, "activity": "form-4e",
                             "owner": "Legal and Commercial", "finding": "the 9.6 / 6.2 / 10.5 tension"})
    cur = _curated_with_check_issues()
    pending = {"I-SYN-CROSS": {"short": "Form 4-E cross-check", "owner": "Bid manager", "brief": "cross-check"},
               "I-SYN-COMM": {"short": "commercial qualification", "owner": "Legal counsel", "brief": "qualification"}}
    prog["open_decision_index"] = {}
    programme.attach_check_findings(prog, res, cur, pending)
    f4e = next(a for a in prog["activities"] if a["id"] == "form-4e")
    assert {"I-SYN-CROSS", "I-SYN-COMM"} <= set(f4e["open_decisions"])
    assert f4e["finalisation"].startswith("FINALISATION NEEDS A DECISION") and "I-SYN-CROSS" in f4e["finalisation"]
    assert f4e["decision_needed_by"]
    chk = [x for x in f4e["flags"] if x.startswith(programme.CHECK_FLAG)]
    assert chk and "bond" in chk[0] and "f4f" in chk[0] and "INFEASIBLE" in chk[0], chk
    assert "HUMAN DECISION PENDING" in chk[0] and "I-SYN-CROSS (Bid manager)" in chk[0]
    assert "I-SYN-COMM (Legal counsel)" in chk[0]
    od = [x for x in f4e["flags"] if x.startswith(programme.OPEN_DECISION_FLAG)]
    assert od and "I-SYN-CROSS" in od[0]
    assert set(prog["open_decision_index"]) >= {"I-SYN-CROSS", "I-SYN-COMM"}
    assert [c["issues"] for c in res["judgments"]] == [["I-SYN-CROSS"], ["I-SYN-COMM"]]
    # the Gantt's status cell carries the check (the notes print it in full)
    tags = [t[0] for t in gantt._tags(f4e)]
    assert any(t.startswith("9.6 CHECK") for t in tags), tags
    assert any(t.startswith("OPEN DECISION (") for t in tags)


def test_r3_14_2_an_unmirrored_judgment_still_shows_on_the_activity_synthetic():
    prog, cal = _synthetic_prog()
    res = _checks(prog, cal)
    programme.attach_check_findings(prog, res, {}, {})
    f4e = next(a for a in prog["activities"] if a["id"] == "form-4e")
    chk = [x for x in f4e["flags"] if x.startswith(programme.CHECK_FLAG)]
    assert chk and "HUMAN DECISION PENDING" in chk[0] and "no curated issue mirrors it" in chk[0], chk
    assert "VOL-I 9.6 CHECK" in f4e["finalisation"]


def test_r3_14_2_a_mirrored_judgment_follows_its_issue_synthetic():
    """A judgment mirrored by an issue outside the pending index stays pending on the activity, named by the issue; one
    whose mirroring issue has a recorded decision is said to be decided, never pending."""
    cur = _curated_with_check_issues()
    prog, cal = _synthetic_prog()
    res = _checks(prog, cal)
    programme.attach_check_findings(prog, res, cur, {})
    f4e = next(a for a in prog["activities"] if a["id"] == "form-4e")
    chk = [x for x in f4e["flags"] if x.startswith(programme.CHECK_FLAG)][0]
    assert "I-SYN-CROSS (Bid manager)" in chk and "no curated issue mirrors it" not in chk, chk
    assert "mirrored by I-SYN-CROSS, no decision recorded" in f4e["finalisation"], f4e["finalisation"]
    prog, cal = _synthetic_prog()
    res = _checks(prog, cal)
    programme.attach_check_findings(prog, res, cur, {}, decided={"I-SYN-CROSS"})
    f4e = next(a for a in prog["activities"] if a["id"] == "form-4e")
    chk = [x for x in f4e["flags"] if x.startswith(programme.CHECK_FLAG)][0]
    assert "decision recorded on I-SYN-CROSS" in chk and "HUMAN DECISION PENDING" not in chk, chk
    assert not f4e.get("check_judgments") and "VOL-I 9.6 CHECK" not in f4e["finalisation"]


@pytest.fixture(scope="module")
def real():
    r = stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)
    progs = stage2.a5_all(r)
    return r, progs[r["validated"].stage]


@pytest.fixture(scope="module")
def real_with_check_issues():
    """The real pack with two synthetic curated issues mirroring the Form 4-E judgments (the ids F1 creates are not in
    this worktree): the coordinator's merge gives the real ones."""
    r = stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)
    r = dict(r, curated_issues={**r["curated_issues"], **_curated_with_check_issues()},
             pending_issues={**r["pending_issues"], "I-SYN-CROSS": ["synthetic"], "I-SYN-COMM": ["synthetic"]})
    return r, programme.stage_planner(r)(r["assumptions"])          # extended: marshalling as A5 writes it


def test_r3_14_2_real_form_4e_carries_the_check_and_its_judgments(real_with_check_issues, tmp_path):
    r, prog = real_with_check_issues
    acts = {a["id"]: a for a in prog["activities"]}
    f4e = acts["form-4e"]
    assert {"I-SYN-CROSS", "I-SYN-COMM"} <= set(f4e["open_decisions"]), f4e["open_decisions"]
    chk = " ".join(x for x in f4e["flags"] if x.startswith(programme.CHECK_FLAG))
    for d in ("lcc-certificate", "form-4f", "model-audit-opinion"):
        assert d in chk, d
    assert "INFEASIBLE by" in chk and "WD" in chk
    assert "I-SYN-CROSS" in f4e["finalisation"] and "I-SYN-COMM" in f4e["finalisation"]
    m = next(x for x in prog["marshalling"] if x["evidence"] == "EV-FORM-4E")
    assert any(programme.CHECK_FLAG in f for f in m["flags"]), m["flags"]
    s = gantt.svg(prog)
    assert "9.6 CHECK" in s and "I-SYN-CROSS" in s and "I-SYN-COMM" in s
    readme = programme.readme(prog)
    assert "I-SYN-CROSS" in readme


def test_r3_14_2_real_without_mirroring_issue_still_on_form_4e(real):
    r, prog = real
    f4e = next(a for a in prog["activities"] if a["id"] == "form-4e")
    chk = " ".join(x for x in f4e["flags"] if x.startswith(programme.CHECK_FLAG))
    assert "lcc-certificate" in chk and "INFEASIBLE" in chk and "HUMAN DECISION PENDING" in chk
    assert "9.6 CHECK" in gantt.svg(prog)


# ---------------------------------------------------------------------------------------------- R3-14-4 (real)

def test_r3_14_4_real_checks_follow_the_gates(real):
    r, prog = real
    docs = {c["document_activity"]: c for c in prog["form_4e_checks"]["checks"]}
    for d in ("form-4a", "form-4b"):                              # GATED, finalise by after Form 4-E starts
        assert docs[d]["status"].startswith("NOT CHECKABLE") and "GATED by" in docs[d]["status"], docs[d]["status"]
    for d in ("form-4c-sign", "form-4g-sign", "pcg-execution", "fin-model-freeze", "fin-assumptions"):
        assert "final on" not in docs[d]["status"] and "NEEDS A DECISION" in docs[d]["status"], (d, docs[d]["status"])
    assert docs["technical-proposal"]["status"].startswith("linked")


# ---------------------------------------------------------------------------------------------- R3-14-3

def test_r3_14_3_an_issue_naming_a_deliverable_reaches_its_producers_and_what_is_built_from_it_synthetic():
    acts = [{"id": "model", "req_ids": [], "evidence": "EV-M", "envelope": "B", "predecessors": []},
            {"id": "audit", "req_ids": [], "evidence": "EV-AUD", "envelope": "B", "predecessors": ["model"]},
            {"id": "f4f", "req_ids": ["R-F"], "evidence": "EV-F", "envelope": "B", "predecessors": ["model", "audit"]},
            {"id": "asm-b", "req_ids": [], "evidence": "EV-DEL", "envelope": "A+B", "predecessors": ["f4f"]},
            {"id": "dev", "req_ids": ["R-T"], "evidence": "EV-E", "envelope": "A", "predecessors": []},
            {"id": "other", "req_ids": [], "evidence": "EV-O", "envelope": "A", "predecessors": []}]
    by_row = {"R-T": ["I-TERM"], "R-POST": ["I-TERM"]}
    pending = {"I-TERM": {"short": "term", "owner": "Legal"}}
    names = {"EV-M": "Financial Model (unlocked)", "EV-AUD": "Auditor's opinion", "EV-F": "Form 4-F",
             "EV-E": "Form 4-E", "EV-DEL": "Delivery", "EV-O": "Other"}
    words = {"I-TERM": "Which clause governs the term. It sets the term start in the Financial Model."}
    reach = programme.open_decision_reach(acts, by_row, pending, deliverables=names, issue_words=words)
    assert reach["I-TERM"] == {"dev", "model", "audit", "f4f"}, reach
    assert programme.open_decision_reach(acts, by_row, pending)["I-TERM"] == {"dev"}       # rows only: as before
    # a deliverable whose producer already carries one of the issue's rows is the row rule's: the words add nothing
    # (the Proposal documents built from it are not reached by the words)
    by_row2 = {"R-T": ["I-TERM"], "R-M": ["I-TERM"]}
    acts2 = copy.deepcopy(acts)
    acts2[0]["req_ids"] = ["R-M"]
    reach2 = programme.open_decision_reach(acts2, by_row2, pending, deliverables=names, issue_words=words)
    assert reach2["I-TERM"] == programme.open_decision_reach(acts2, by_row2, pending)["I-TERM"], reach2


def test_r3_14_3_real_concession_reaches_the_model_chain_and_form_4f(real):
    r, prog = real
    acts = {a["id"]: a for a in prog["activities"]}
    for aid in ("fin-model-build", "fin-model-freeze", "model-audit-opinion", "fin-assumptions", "form-4f"):
        assert "I-CONCESSION" in (acts[aid].get("open_decisions") or []), (aid, acts[aid].get("open_decisions"))
        assert "I-CONCESSION" in acts[aid]["finalisation"]
    assert "I-CONCESSION" not in (acts["lcc-certificate"].get("open_decisions") or [])


# ---------------------------------------------------------------------------------------------- R3 m2, m3

def test_r3_m2_one_decision_state_and_m3_the_decide_by_date_is_said_synthetic():
    acts = [_act("a", req_ids=["R1"], latest_start="2026-10-06"), _act("b", req_ids=["R2"], latest_start="2026-11-20")]
    programme.inherit_open_decisions(acts, {"R1": ["I-P"], "R2": []}, {"I-P": {"short": "p", "owner": "Commercial"}})
    assert acts[0]["decision_status"].startswith("NOT GATED"), acts[0]["decision_status"]
    assert "NEEDS A DECISION" in acts[0]["decision_status"] and acts[1]["decision_status"] == "READY"
    prog = {"activities": acts, "planning_date": "2026-10-22"}
    programme.attach_readiness(prog)
    fin = acts[0]["finalisation"]
    assert "by 2026-10-06 (the activity's latest start" in fin, fin
    assert "ALREADY PASSED" in fin and "2026-10-22" in fin, fin
    m = programme.marshalling({"activities": [dict(acts[0], evidence="EV-X", evidence_items=["EV-X"], owner="o",
                                                   latest_finish="2026-10-07", earliest_finish="2026-10-23")],
                               "evidence_needed": {"EV-X": ["R1"]}},
                              {"items": [{"evidence": "EV-X", "name": "x", "kind": "action"}], "totals": []})
    assert m[0]["decision_status"].startswith("a: NOT GATED"), m[0]["decision_status"]


def test_r3_m2_legend_says_the_bar_is_the_activity():
    s = gantt.svg({"activities": [_act("a", earliest_finish="2026-11-01", latest_start="2026-11-02",
                                       latest_finish="2026-11-02", open_decisions=["I-P"],
                                       decision_needed_by="2026-11-02", float_wd=1, owner="o", resource="r",
                                       resource_status="OK", discipline="d")],
                   "planning_date": "2026-11-01", "status_date": "2026-11-01", "stage": "S", "milestones": []})
    assert "bar = preparation" not in s and "bar = the activity" in s


def test_r3_m2_m3_real(real):
    r, prog = real
    acts = {a["id"]: a for a in prog["activities"]}
    assert acts["form-4e"]["decision_status"].startswith("NOT GATED")
    assert "ALREADY PASSED" in acts["lcc-ratio"]["finalisation"], acts["lcc-ratio"]["finalisation"]
    assert "the activity's latest start" in acts["technical-proposal"]["finalisation"]
    # the Form 4-E checks say the same of a decide-by date already passed (one state, wherever the date is printed)
    docs = {c["document_activity"]: c for c in prog["form_4e_checks"]["checks"]}
    assert "ALREADY PASSED" in docs["lcc-certificate"]["status"], docs["lcc-certificate"]["status"]
    assert "ALREADY PASSED" not in docs["form-4f"]["status"]


# ---------------------------------------------------------------------------------------------- R3 m7

def test_r3_m7_an_inserted_form_cites_the_clause_that_inserted_it(real):
    r, prog = real
    docs = {c["document_activity"]: c for c in prog["form_4e_checks"]["checks"]}
    cl = docs["form-4g-sign"]["clause"]
    assert "ADD-02 7.1" in cl and "inserted after item (e)" in cl, cl
    assert "ADD-02 7.2" in cl and "Envelope A" in cl, cl


# ---------------------------------------------------------------------------------------------- R2 m1, m2, m5

@pytest.fixture(scope="module")
def a3page(real):
    r, prog = real
    return stage2.a3(r, stage2.collect_issues(r, prog), prog)


def _items(a3d):
    return {i["id"]: i for g in a3d["groups"]["groups"] for i in g["items"]}


def test_r2_m1_dagger_agrees_with_a5_decide_by(real, a3page):
    r, prog = real
    by = programme.decide_by(prog)
    pdd = "2026-11-26"
    items = _items(a3page)
    folded = stage2.fold_issues(r, stage2.collect_issues(r, prog), prog, {})["folded"]
    for iid, (d, _) in by.items():
        if d < pdd:
            listed = folded.get(iid, iid)
            if listed in items:
                assert items[listed]["decide"], (iid, listed, d)
    for i in ("I-FLOWS", "I-VOL-V-PERSISTENT-BREACH"):
        assert i in by and items[i]["decide"], i
    assert items["I-FLOWS"]["decide_by"] == by["I-FLOWS"][0], items["I-FLOWS"]


def test_r2_m2_one_count_on_the_a3_heading(a3page):
    g = a3page["groups"]
    n_all = g["counts"]["all"]
    assert g["heading"].startswith(f"Unresolved matters, grouped — {n_all} open issues ({g['counts']['listed']} listed")
    assert g["note"].startswith(f"{n_all} open issues")


def test_r2_m5_a_high_confidence_line_names_its_pending_judgments(real, a3page):
    lines = {x["id"]: x for x in a3page["explicit"]}
    assert "I-F4A-FIELDS" in lines["VOL-I-9.3-01"]["confidence"], lines["VOL-I-9.3-01"]["confidence"]
    assert "I-CONCESSION" in lines["VOL-I-9.6-01"]["confidence"], lines["VOL-I-9.6-01"]["confidence"]


# ---------------------------------------------------------------------------------------------- R2 m7

def test_r2_m7_question_rows_take_every_row_of_the_pending_issue_it_asks_about():
    rows = {"R-T1": (["V:T/a"], ["I-P", "I-R"]), "R-T2": (["V:T/b"], ["I-P"]), "R-H": (["V:2.4"], ["I-P"]),
            "R-X": (["V:9"], ["I-R"])}
    assert clarify.question_rows(["V:2.4"], {"I-P", "I-R"}, rows) == ["R-H"]                  # as before
    got = clarify.question_rows(["V:2.4"], {"I-P", "I-R"}, rows, mirrored={"I-P"})
    assert set(got) == {"R-H", "R-T1", "R-T2"}, got                                          # not R-X (I-R: narrowed)


def test_r2_m7_real_permit_question_rows(real):
    r, prog = real
    qs = {q["id"]: q for q in clarify.presented(r["clarifications"], r.get("decisions"), r.get("pending_issues"),
                                                 r.get("curated_issues"), stage2.answer_row_index(r))}
    rows = set(qs["CQ-ENV-PERMIT"]["answer_rows"])
    assert {"VOL-II-T2-4-BOD5", "VOL-II-3.1-01", "VOL-II-7.2-01", "VOL-V-31.1-02"} <= rows, sorted(rows)


# ---------------------------------------------------------------------------------------------- R3 m8

def test_r3_m8_arabic_runs_in_the_cards_are_marked_rtl():
    h = batches.bidi_html("Quote: “البند ٤-٢ x” & more")
    assert '<bdi dir="rtl">البند ٤-٢</bdi>' in h and "&amp;" in h
    s = batches.states_block_html({"value": "value as read: 'يؤدي إلى استبعاد العرض'", "interpretation": "i",
                                   "approval": "a"})
    assert '<bdi dir="rtl">يؤدي إلى استبعاد العرض</bdi>' in s


def test_r2_m1_m2_m5_the_one_page_keeps_its_reasons(a3page, tmp_path):
    """The names and counts added to the A3 page do not push it to dropping each issue's reason (level 3)."""
    from tenderpack import render
    for level, words, page in stage2.a3_pages(a3page):
        try:
            render.write_a3_pdf(page, tmp_path / "a3.pdf")
            break
        except render.A3OverflowError:
            continue
    assert level <= 2, (level, words)
    lines = {x["id"]: x for x in a3page["explicit"]}
    assert lines["VOL-I-9.3-01"]["confidence"].startswith(f"high ({stage2.A3_PENDING_MARK} ")
    assert stage2.A3_MARKS[1][1] in stage2.condense_a3(a3page, level, reason_words=words)["subtitle"]
