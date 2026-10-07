"""Session 12, fixer F5: the leftovers of the six reviewers' rechecks (audit reports A1_recheck .. A5_recheck and
R_recheck). Each test reproduces one finding on the real pack (the committed evidence build, stage2.run / stage2.build
into pytest's temporary folders) or on small synthetic data, and states the general rule. Nothing writes to the
repository; nothing here records, accepts or approves anything.

  answers     an answer that points to a rule without choosing ('The order of precedence at Volume I Clause 3.2
              applies.') does not confirm the clauses it is asked about: summary.classify_answer reads it as
              `interprets` (A2-1 leftover, A5 N1).
  pending     a row whose linked issue is human-owned and undecided (human_owned.pending_reasons) is never
              CONFIRMED (unchanged): it is NOT SETTLED with "open: <issue>, human decision pending", in A2, A5's
              deltas and the diff alike (signals.requirement_delta reads the evaluation's `pending`).
  one label   A2's label for a row at an addendum and A5's delta label for the same row come from one function
              (signals.row_label): ADD-01-AppA-01 (Form 4-A must acknowledge ADD-02) is CHANGED in A2 as REWORK in A5;
              VOL-IV-F4A-01/-02 are NOT SETTLED at ADD-02 in both (R-f).
  why         an A2 'why' that shows a replaced text shows different words before and after (A2-8).
  flag        ⚑ marks every unresolved issue a person owns: owner Legal or Commercial, own words asserting a judgment,
              or linked from a pending decision of the clarification register; † and ⚑ are both defined in the A3
              legend; the A3 page, a3_detail.html, A4's pending section and A1's Issues sheet name one pending set
              (A3-5, R-a, R1-1).
  gate        I-NO-CONSEQUENCE's rows are the gate's rows (A3-6).
  wording     I-AUTO-COUNTING names clauses, I-BIDDER-FACTS names the facts, ESIA is written out (A3 leftovers); no
              A1 sheet cites an internal audit id (A1-6); one Confidence wording for one approval (R-b).
  A5          a question reaches an activity only through the rows its answer would change (N2); "carried" is split
              into discharged / reviewed for deviations / excepted (N3); the relationship status legend is printed in
              the Gantt and the A5 README (R-e); no status cell of the Gantt is cut (R-d).
  cards       an applied batch-04 card prints no apply command; a superseded card says where its replacement is (R-c).
  cover       a cover that names "Clause 6.8 as inserted by Addendum No. 3" covers an op on VOL-I:6.7+ADD-03 (W5).
"""
from __future__ import annotations

import csv
import io
import json
import re
from pathlib import Path

import pytest

from tenderpack import human_owned as H
from tenderpack import programme, schedule, signals, stage2
from tenderpack.summary import classify_answer
from tenderpack.util import ROOT

EVIDENCE = ROOT / "build"
PACK = ROOT / "config/pack.yaml"
Q7 = ("The Authority notes the question. The order of precedence at Volume I Clause 3.2 applies. The Authority does "
      "not consider further amendment necessary at this stage.")


@pytest.fixture(scope="module")
def real():
    return stage2.run(EVIDENCE, PACK, ROOT)


@pytest.fixture(scope="module")
def issues(real):
    return stage2.collect_issues(real, None)


@pytest.fixture(scope="module")
def a2(real):
    return stage2.a2(real)


@pytest.fixture(scope="module")
def replan(real):
    progs = stage2.a5_all(real)
    ea = {e["row"].id: e["stages"]["ADD-01"] for e in real["evals"]}
    eb = {e["row"].id: e["stages"]["ADD-02"] for e in real["evals"]}
    return schedule.deltas(progs["ADD-01"], progs["ADD-02"], ea, eb, answers=programme.answers_by_row(real, "ADD-02"))


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("f5-out") / "out"
    res = stage2.build(EVIDENCE, out, PACK, ROOT, quiet=True)
    assert res["status"] == "ok", res.get("status")
    return out


def _txt(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _csv(p: Path) -> list[dict]:
    return list(csv.DictReader(io.StringIO(_txt(p).lstrip("﻿"))))


# ---------------------------------------------------------------------------------------------- answers (A2-1, N1)

def test_an_answer_that_points_to_a_precedence_rule_does_not_confirm(real):
    from tenderpack.summary import answer_targets
    op = next(x.op for s in real["stages"] for x in s.ops if x.op.id == "ADD-02/Q7")
    prev = next(s for s in real["stages"] if s.stage == "ADD-01").state
    targets = answer_targets(prev, [t for t in op.targets if t != op.provision])
    assert "VOL-I:3.2" in targets                     # the rule it points to is among the targets: its words are known
    c = classify_answer("Authority response: " + Q7, targets)
    assert c["class"] not in ("none", "confirms"), c
    assert any("precedence" in s["text"] and s["kind"] == "interprets" for s in c["sentences"]), c["sentences"]
    # a plain restatement still confirms (the session-11 rule is kept)
    c2 = classify_answer("Authority response: Volume I Clause 12.1 applies.", targets)
    assert c2["class"] in ("none", "confirms"), c2
    # and in the rows' causes: the answer no longer 'reads confirms'
    recs = programme.answers_by_row(real, "ADD-02").get("VOL-V-3.1-01") or []
    q7 = next(x for x in recs if x["op"] == "ADD-02/Q7")
    assert q7["class"] == "interprets", q7


# ---------------------------------------------------------------------------------------------- pending (A2-1, N1)

def test_issue_label_marks_owner_legal_or_commercial_and_pending_links():
    plain = {"text": "Form 4-C: how the exclusion maps is open", "owner": "Legal"}
    assert H.issue_label("I-X", plain, []) == H.HUMAN_DECISION_PENDING
    assert H.issue_label("I-X", dict(plain, owner="Commercial lead"), []) == H.HUMAN_DECISION_PENDING
    assert H.issue_label("I-X", dict(plain, owner="Bid manager"), []) is None
    assert H.issue_label("I-X", dict(plain, owner="Technical"), [], linked=["Form 4-G 'No' answers"]) \
        == H.HUMAN_DECISION_PENDING
    assert H.pending_reasons("I-X", dict(plain, owner="Technical"), [], linked=["t"]), "a pending decision links it"
    assert not H.pending_reasons("I-X", dict(plain, owner="Owner"), [])


def test_requirement_delta_never_confirms_a_row_under_a_pending_issue():
    a = {"text": "x", "cells": None, "dates": [], "status": "ACTIVE", "units_detail": [], "interpretation": None}
    b = dict(a, pending=["open: I-CONCESSION, human decision pending"])
    cause = [{"op": "ADD-02/Q7", "type": "annotate", "effect": "interprets", "provision": "ADD-02:Q7",
              "answer": True, "class": "interprets"}]
    d = signals.requirement_delta(a, b, cause)
    assert not d["confirmed"] and d["unsettled"], d
    assert "open: I-CONCESSION, human decision pending" in d["detail"], d
    assert signals.requirement_delta(a, a, cause)["confirmed"]       # without the pending issue: confirmed


def test_concession_rows_are_not_settled_in_a2(a2):
    got = {m["row"]: m for m in a2["rows_moved"] if m["stage"] == "ADD-02"}
    for rid in ("VOL-I-12.1-01", "VOL-V-3.1-01"):
        m = got.get(rid)
        assert m is not None and m["change"] == "NOT SETTLED", (rid, m)
        assert "open: I-CONCESSION, human decision pending" in " ".join(m["why"]), m
        assert "answer reads 'confirms'" not in " ".join(m["why"]), m
    md = a2["markdown"]
    conf = md[md.index("### Rows confirmed or re-read"):] if "### Rows confirmed or re-read" in md else ""
    conf = conf.split("\n### ", 2)[1] if conf.count("\n### ") else conf
    assert "| VOL-I-12.1-01 |" not in conf.split("### Reached through")[0]


def test_no_confirmed_label_names_a_row_under_a_pending_issue(real, a2, replan, issues):
    pending = {i["id"] for i in issues if i.get("human_decision")}
    assert {"I-CONCESSION", "I-FLOWS", "I-F4G-NO"} <= pending, pending
    rows = {e["row"].id: e["row"] for e in real["evals"]}
    under = {k for k, row in rows.items() if set(row.issues) & pending}
    # session 13 (F4; audit R1-9, deliberate): an issue bears on its rows from the stage its evidence first exists
    # (stage2.issue_stages: I-VOL-I-PAGE-LIMIT-Q2 from ADD-02, which raises it), so VOL-I-9.2-01 stays CONFIRMED at
    # ADD-01; the rule checked is the same, at the stages each issue bears
    since, order = stage2.issue_stages(real), real["order"]
    bears = lambda k, st: any(i in pending and order.index(since.get(i, order[0])) <= order.index(st)  # noqa: E731
                              for i in rows[k].issues)
    bad = [(m["stage"], m["row"]) for m in a2["rows_moved"] if m["change"] == signals.CONFIRMED and m["row"] in under
           and bears(m["row"], m["stage"])]
    assert not bad, bad
    bad5 = [(d["activity"], r) for d in replan if d["change"] == signals.CONFIRMED for r in d.get("rows") or []
            if r in under]
    assert not bad5, bad5
    for d in replan:
        if d["activity"] in ("deviations-review", "form-4e") and d["change"] == signals.CONFIRMED:
            assert "VOL-V-3.1-01" not in d["detail"], d


# ---------------------------------------------------------------------------------------------- one label (R-f)

_MAP = {"REWORK": "CHANGED", signals.CONFIRMED: signals.CONFIRMED, "NOT SETTLED": "NOT SETTLED"}


def test_a2_and_a5_give_one_label_per_row_at_add02(a2, replan):
    a2l = {m["row"]: m["change"] for m in a2["rows_moved"] if m["stage"] == "ADD-02"}
    pairs, bad = 0, []
    for d in replan:
        want = _MAP.get(d["change"])
        if want is None:
            continue
        for r in d.get("rows") or []:
            pairs += 1
            if a2l.get(r) != want:
                bad.append((d["activity"], d["change"], r, a2l.get(r)))
    assert pairs > 40, pairs
    assert not bad, bad
    assert a2l.get("ADD-01-AppA-01") == "CHANGED"
    assert a2l.get("VOL-IV-F4A-01") == "NOT SETTLED" and a2l.get("VOL-IV-F4A-02") == "NOT SETTLED"
    m = next(x for x in a2["rows_moved"] if x["stage"] == "ADD-02" and x["row"] == "VOL-IV-F4A-01")
    assert "prints 2026-11-12" in " ".join(m["why"]), m


# ---------------------------------------------------------------------------------------------- why (A2-8)

def test_every_replaced_text_in_a2_why_differs_before_and_after(a2):
    bad = []
    for m in a2["rows_moved"]:
        for w in m["why"]:
            for x, y in re.findall(r"'([^']{3,}?)' -> '([^']{3,}?)'", w):
                if x == y:
                    bad.append((m["stage"], m["row"], x))
    assert not bad, bad
    f4e = next(m for m in a2["rows_moved"] if m["stage"] == "ADD-02" and m["row"] == "VOL-IV-F4E-01")
    assert "5,000,000" in " ".join(f4e["why"]) and "2,500,000" in " ".join(f4e["why"]), f4e["why"]


# ---------------------------------------------------------------------------------------------- flag (A3-5, R-a, R1-1)

def test_the_pending_set_is_one_set_in_a1_a3_page_a3_detail_and_a4(built, real, issues):
    a1 = json.loads(_txt(built / "a1/a1.json"))
    a1_set = {r["id"] for r in a1["sheets"]["Issues"]["rows"]
              if str(r.get("text") or "").startswith(H.HUMAN_DECISION_PENDING)}
    a3 = json.loads(_txt(built / "a3/a3.json"))
    pg = stage2.condense_a3(a3, max(2, a3["condensed"]))
    page = {i["id"] for g in pg["groups"]["groups"] for i in g["items"] if stage2.A3_PENDING_MARK in i["short"]}
    page_folded = {f for g in pg["groups"]["groups"] for i in g["items"] for f in i.get("folds") or []}
    detail = _txt(built / "a3/a3_detail.html")
    det = set(re.findall(r'<tr id="([^"]+)"><td><b>[^<]+</b>[^<]*' + stage2.A3_PENDING_MARK, detail))
    a4 = json.loads(_txt(built / "a4/clarification_register.json"))
    a4_set = {i for c in a4["pending_decision"] for i in c.get("linked_issues") or []} \
        | {x["id"] for x in a4.get("pending_issues") or []}
    curated = set(real["curated_issues"])
    a1_set, a4_set, det = a1_set & curated, a4_set & curated, det & curated
    assert {"I-F4G-NO", "I-FLOWS", "I-CONCESSION", "I-F4A-FIELDS", "I-F4C-EXCLUSION", "I-F4D-WORDING"} <= a1_set, a1_set
    assert a1_set == a4_set == det, (a1_set ^ a4_set, a1_set ^ det)
    assert (page | (page_folded & a1_set)) & curated == a1_set, a1_set ^ (page & curated)
    md = _txt(built / "a4/clarification_register.md")
    assert "I-F4D-WORDING" in md


def test_the_a3_legend_defines_both_marks(built):
    a3 = json.loads(_txt(built / "a3/a3.json"))
    sub = stage2.condense_a3(a3, max(2, a3["condensed"]))["subtitle"]
    assert a3["condensed"] <= 2, a3["condensed"]
    assert "†: decide before submission (no decision recorded)" in sub, sub
    assert re.search(r"⚑: a (?:legal, commercial or technical )?judgment no one has recorded", sub), sub


def test_issues_sheet_labels_issues_linked_from_a_pending_decision(issues):
    by = {i["id"]: i for i in issues}
    for iid in ("I-FLOWS", "I-F4G-NO", "I-F4D-WORDING"):
        assert by[iid]["text"].startswith(H.HUMAN_DECISION_PENDING), (iid, by[iid]["text"][:80])


# ---------------------------------------------------------------------------------------------- gate (A3-6)

def test_no_consequence_issue_rows_are_the_gate_rows(real, issues):
    a3 = stage2.a3(real, issues, None)
    gate = set(next(s for s in a3["sections"] if s["heading"].startswith("General gate"))["ids"])
    det = next(i for i in a3["issues_detail"] if i["id"] == "I-NO-CONSEQUENCE")
    assert set(det["rows"]) == gate, (set(det["rows"]) - gate, gate - set(det["rows"]))
    assert "ADD-02-5.2-01" not in det["rows"]


# ---------------------------------------------------------------------------------------------- wording

def test_auto_counting_names_clauses_and_bidder_facts_names_facts(real, issues):
    a3 = stage2.a3(real, issues, None)
    items = {i["id"]: i for g in a3["groups"]["groups"] for i in g["items"]}
    ac = items["I-AUTO-COUNTING"]["short"]
    assert not re.search(r"\b[A-Z]{4,}(?:-[A-Z0-9]+)+\b", ac.replace("I-AUTO-COUNTING", "")), ac
    assert "VOL-I 6.3" in ac and "Form 4-A" in ac, ac
    bf = items["I-BIDDER-FACTS"]["short"]
    for w in ("members", "reference plants", "signatories", "attendance"):
        assert w in bf, bf
    page = json.dumps(stage2.condense_a3(a3, 2), ensure_ascii=False)
    assert "Environmental and Social Impact Assessment (ESIA" in page or "ESIA" not in page


def test_no_a1_sheet_cites_an_internal_audit_id(real, issues):
    a1 = stage2.a1_table(real, issues)
    bad = []
    for name, s in a1["sheets"].items():
        for r in s.get("rows") or []:
            t = json.dumps(r, ensure_ascii=False)
            if re.search(r"session \d+, audit|audit A\d", t, re.I):
                bad.append((name, t[:120]))
    if re.search(r"session \d+|audit A\d", a1["notice"], re.I):
        bad.append(("notice", a1["notice"][:120]))
    assert not bad, bad


def test_one_confidence_wording_for_one_approval(real, issues):
    a1 = stage2.a1_table(real, issues)
    rows = {r["id"]: r for r in a1["rows"]}
    f4c = [k for k in rows if k.startswith("VOL-IV-F4C-")]
    assert len(f4c) == 6, f4c
    for k in f4c:
        assert "transcription and displayed translations confirmed by the owner" in rows[k]["confidence"], \
            (k, rows[k]["confidence"])


def test_vol_v_42_2_quotes_q7_and_links_it(real, issues):
    a1 = stage2.a1_table(real, issues)
    r = next(x for x in a1["rows"] if x["id"] == "VOL-V-42.2-01")
    t = json.dumps(r, ensure_ascii=False)
    assert "The order of precedence at Volume I Clause 3.2 applies." in t, t[:300]
    assert "ADD-02:Q7" in str(r.get("chain")) or "ADD-02/Q7" in str(r.get("chain")), r.get("chain")


def test_a2_nits_q13_wording_and_appa_dates(real, a2):
    row = next(e["row"] for e in real["evals"] if e["row"].id == "VOL-I-12.2-02")
    notes = " ".join(str(i.note or "") for i in row.interpretations)
    assert "will not extend" not in notes, notes
    op = next(x.op for s in real["stages"] for x in s.ops if x.op.id == "ADD-01/AppA/para1")
    assert "12 November 2026" in op.issue and "26 November 2026" in op.issue, op.issue


# ---------------------------------------------------------------------------------------------- A5 (N2, N3, R-d, R-e)

def test_a_question_reaches_only_the_activities_its_answer_changes(real):
    p = stage2.a5_all(real)[real["validated"].stage]
    on = sorted(a["id"] for a in p["activities"] if "CQ-F4A-REISSUE" in (a.get("clarification_questions") or []))
    assert on == ["clarifications", "form-4a", "form-4a-prep"], on
    clar = next(a for a in p["activities"] if a["id"] == "clarifications")
    allq = {c["id"] for c in real["clarifications"]["clarifications"]}
    assert set(clar["clarification_questions"]) == allq, allq - set(clar["clarification_questions"])
    lcc = [a["id"] for a in p["activities"] if "CQ-LCC-ISSUER" in (a.get("clarification_questions") or [])]
    assert {"lcc-ratio", "lcc-certificate"} <= set(lcc), lcc


def test_carried_is_split_into_discharged_reviewed_and_excepted(built):
    readme = _txt(built / "a5/README.md")
    m = re.search(r"(\d+) A1 rows in force at ADD-02: (\d+) discharged by an activity, (\d+) reviewed for deviations "
                  r"\(the VOL-V volume check\), (\d+) excepted with a reason", readme)
    assert m, readme[readme.find("## Requirements not carried"):][:600]
    n, d, rv, ex = map(int, m.groups())
    assert n == d + rv + ex == 200 and rv > 0, m.groups()
    checks = json.loads(_txt(built / "checks.json"))
    c48 = next(c for c in checks["reported"] if c["id"] == "C48")
    assert f"{d} discharged" in c48["detail"] and f"{rv} reviewed for deviations" in c48["detail"], c48["detail"]
    cov = _csv(built / "a5/requirements_coverage.csv")
    assert len(cov) == 200 and {r["carried_how"] for r in cov} == {"discharged", "reviewed for deviations", "excepted"}


def test_gantt_status_cells_are_not_cut_and_legend_is_printed(built):
    svg = _txt(built / "a5/gantt.svg")
    assert "BLOCKED..." not in svg and not re.search(r"[A-Za-z]\.\.\.</text>", svg), \
        re.findall(r">[^<]{0,60}\.\.\.</text>", svg)[:5]
    from tenderpack.relationships import STATUS_LEGEND
    for f in ("gantt.svg", "gantt.html", "README.md"):
        t = _txt(built / "a5" / f)
        if "REVIEW (confirmed" in t:
            assert STATUS_LEGEND.split(":")[0] in t and "stated in the documents" in t, f


# ---------------------------------------------------------------------------------------------- cards (R-c)

def test_batch04_cards_command_only_when_not_applied_and_replacement_position(built):
    pages = sorted((built / "review").rglob("batch-04*.html"))
    assert pages, sorted(p.name for p in (built / "review").rglob("*.html"))
    html = _txt(pages[0])
    cards = re.split(r'(?=<div class="item")', html)
    ids = [re.search(r'id="([^"]+)"', c).group(1) if re.search(r'id="([^"]+)"', c) else "" for c in cards]
    for i, c in enumerate(cards):
        if "Applied." in c or "applied (" in c.lower():
            assert "apply-proposal" not in c, c[:300]
        m = re.search(r"replaced by ([\w.\-]+)(?:\s*\((above|below)\))?", c)
        if m and m.group(2):
            j = next((k for k, x in enumerate(ids) if m.group(1) in x), None)
            assert j is not None and (m.group(2) == "above") == (j < i), (m.group(0), i, j)


# ---------------------------------------------------------------------------------------------- cover (W5)

from test_session12_consecutive import area, chain, prev_build  # noqa: E402,F401  (the W5 fixture: ADD-03 then ADD-04)


def test_a_cover_naming_the_inserted_clause_covers_the_op_on_its_unit(chain):
    out = chain["dir"] / "candidate/out"
    sc = json.loads(_txt(out / "a2/a2_cover_summary_check.json"))
    rows = sc.get("rows") if isinstance(sc, dict) else sc
    add04 = [x for x in rows if x.get("stage") == "ADD-04"]
    bad = [x for x in add04 if x.get("kind") == "omitted" and x.get("op") == "ADD-04/1.1"]
    assert not bad, bad
    a2 = _txt(out / "a2/a2.md")
    sec = a2[a2.index("## ADD-04"):]
    assert "### Cover summary vs provisions (C28)" in sec
    assert "ADD-04/1.1 amends VOL-I:6.7+ADD-03; the summary does not mention it" not in sec


def test_carried_words_name_the_volume_check_or_say_none_applies():
    """Session 12 (the coordinator): on a rehearsal build with no volume check the C48 line read "(the a volume
    check)"; it must name the check or say that none applies."""
    from tenderpack.programme import carried_words
    assert carried_words({"discharged": {"a": 1}, "reviewed": {"b": 1}, "volumes": ["VOL-V"]}) == \
        "1 discharged by an activity, 1 reviewed for deviations (the VOL-V volume check)"
    assert carried_words({"discharged": {"a": 1, "c": 1}, "reviewed": {}, "volumes": []}) == \
        "2 discharged by an activity, 0 reviewed for deviations (no volume check applies at this stage)"
    assert carried_words({"carried": {"a": 1}}) == "1 carried by the A5 programme"
