"""Session 13, fixer F4: the follow-ups reviewers R1 and R2 raised in their rechecks after F1, F2 and F3.

  R1-7  one set of rows per issue in A1 and A2: an issue bears on the rows that list it, plus the rows a curated
        relationship carrying it reaches (and an evidence field a reissued form drops): stage2.row_issues, the function
        behind A1's Issues cell and A2's pending list (signals.attach_pending). An issue named in an op's note is
        context for the op, not a link to every row the op targets.
  R1-8  an op awaiting a person's acceptance is an approval blocker, not a judgment: A2 never lists an op as "human
        decision pending"; a confirming op in a NOT SETTLED line reads "proposed op <id> (awaiting a person's
        acceptance)".
  R1-9  an issue bears on a row from the stage its evidence first exists (`since`, or derived from the `units` it
        cites: the latest stage at which one of them is first issued); the pending rule, A2's labels and A5's deltas
        follow it.
  R1 nits  the 'at all times' limb lives in I-VOL-II-AT-ALL-TIMES only; a2_relationship_impact carries the Permit's
        non-binding context in a column named as a2.md words it.
  R2-11 a pending human-owned issue folded under another issue on the A3 page is named on the parent line with ⚑.
  R2-12 the page's label for a drafted question comes from the entry's subject words, never a category.
  R2 note an open decision of an activity has a decision date (the drafted question's ask-by, else the activity's own
        latest start, labelled).
  R2-8  the compliance point of Table 2-4 is an open, PROPOSED issue with the three printed candidates; no question drafted.
  R1    citations.quantified_row never matches an addendum's cover text.
Real pack (the committed evidence build) and synthetic cases. Nothing is written in the repository; nothing is
approved, accepted or decided."""
from __future__ import annotations

import json
import re

import pytest

from tenderpack import programme, signals, stage2
from tenderpack import human_owned as H
from tenderpack.util import ROOT

EVIDENCE = ROOT / "build"
PACK = ROOT / "config/pack.yaml"
T24 = "I-VOL-II-T24-TENSIONS"
Q2 = "I-VOL-I-PAGE-LIMIT-Q2"
CP = "I-VOL-II-COMPLIANCE-POINT"
OP = "ADD-02/5.1/unchanged"
NINE = ["BOD5", "COD", "TSS", "TP", "Turbidity", "FaecalColiforms", "ResidualChlorine", "pH", "OilGrease"]
AWAIT = "awaiting a person's acceptance"


@pytest.fixture(scope="module")
def real():
    return stage2.run(EVIDENCE, PACK, ROOT)


@pytest.fixture(scope="module")
def a2d(real):
    return stage2.a2(real)


@pytest.fixture(scope="module")
def a1(real):
    return stage2.a1_table(real, stage2.collect_issues(real, None))


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("s13-f4-out") / "out"
    res = stage2.build(EVIDENCE, out, PACK, ROOT, quiet=True)
    assert res["status"] == "ok", res.get("status")
    return out


def _txt(p) -> str:
    return p.read_text(encoding="utf-8")


def _a1_rows_of(a1, iid) -> set[str]:
    sheet = {i["id"]: i for i in a1["sheets"]["Issues"]["rows"]}
    return {str(x).split(" ")[0] for x in sheet[iid]["rows"]}


# ---------------------------------------------------------------------------------------------- R1-7

def test_r1_7_one_issue_set_per_row_synthetic():
    links = [{"issue": "I-X", "via": "REL-A", "status": "confirmed"}, {"issue": "I-Y", "why": "dropped field"},
             {"issue": "I-X", "via": "REL-B", "status": "proposed"}]
    cell = stage2.linked_issue_cells(["I-Z", "I-Y"], links)
    ids = signals.issue_ids_of(["I-Z", "I-Y"], links)
    assert ids == ["I-Z", "I-Y", "I-X"]
    assert [c.split(" ")[0] for c in cell] == ids                    # A1's cell and A2's set: one function
    # the pending list of every stage is the pending part of that set (attach_pending)
    from types import SimpleNamespace as NS
    ev = {"BASE": {}, "ADD-01": {}}
    r = {"curated_issues": {"I-X": {"text": "t", "owner": "Legal"}, "I-Z": {"text": "t", "owner": "Bid manager"}},
         "evals": [{"row": NS(id="R-1", issues=["I-Z"]), "stages": ev}], "order": ["BASE", "ADD-01"]}
    signals.attach_pending(r, {"R-1": ids})
    assert ev["ADD-01"]["pending"] == [signals.pending_note("I-X")], ev     # I-X: Legal (owner_judgment); I-Z: not


def test_r1_7_an_issue_named_in_an_op_note_is_context_not_a_row_link(real):
    assert not hasattr(signals, "op_pending"), "an op's note must not attach its issues to every target row"
    for x in programme.answers_by_row(real, "ADD-02").get("VOL-II-T2-4-BOD5") or []:
        assert not x.get("pending"), x


def test_r1_7_t24_rows_are_one_set_in_a1_and_a2(real, a1, a2d):
    by_row = stage2.row_issues(real)
    fn = {rid for rid, ids in by_row.items() if T24 in ids}
    a1_set = _a1_rows_of(a1, T24)
    a1_cells = {x["id"] for x in a1["rows"] if any(c.split(" ")[0] == T24 for c in x["issues"])}
    a2_pending = {e["row"].id for e in real["evals"] if signals.pending_note(T24) in e["stages"]["ADD-02"]["pending"]}
    assert fn == a1_set == a1_cells == a2_pending, (fn ^ a1_set, fn ^ a1_cells, fn ^ a2_pending)
    # the two range rows carry it; the seven single-value rows do not (the ambiguity is about the ranges)
    assert {"VOL-II-T2-4-ResidualChlorine", "VOL-II-T2-4-pH"} <= fn
    assert not {f"VOL-II-T2-4-{p}" for p in NINE if p not in ("ResidualChlorine", "pH")} & fn
    # A2's text names it only on rows of that set, and on every NOT SETTLED row of that set
    for m in a2d["rows_moved"]:
        says = any(w.startswith(f"open: {T24}") or f"open: {T24}," in w for w in m["why"])
        if says:
            assert m["row"] in fn, m
        if m["change"] == "NOT SETTLED" and m["row"] in fn and m["stage"] == "ADD-02":
            assert says, m
    ops = next(o for s in real["stages"] for o in s.ops if o.op.id == OP)
    assert T24 in ops.op.note                                   # the op's note still quotes the question


# ---------------------------------------------------------------------------------------------- R1-8

def test_r1_8_an_op_is_never_a_pending_decision_synthetic():
    a = {"text": "x", "cells": None, "dates": [], "status": "ACTIVE", "units_detail": [], "interpretation": None}
    b = dict(a, pending=[signals.pending_note("I-P")])
    c = {"op": "OP-1", "type": "annotate", "effect": "confirms", "provision": "P:1", "answer": False, "class": "confirms"}
    d = signals.requirement_delta(a, b, [c])
    assert d["unsettled"] and "open: I-P, human decision pending" in d["detail"], d
    assert f"proposed op OP-1 ({AWAIT})" in d["detail"] and "open: OP-1" not in d["detail"], d
    d2 = signals.requirement_delta(a, b, [dict(c, accepted=True)])
    assert AWAIT not in d2["detail"] and "OP-1" in d2["detail"], d2
    assert signals.requirement_delta(a, dict(a, pending=[]), [c])["confirmed"]       # no issue: confirmed by the op


def test_r1_8_real_a2_names_the_op_as_awaiting_acceptance(a2d):
    md = a2d["markdown"]
    assert f"open: {OP}" not in md and not any(f"open: {OP}" in w for m in a2d["rows_moved"] for w in m["why"])
    moved = {m["row"]: m for m in a2d["rows_moved"] if m["stage"] == "ADD-02"}
    for p in NINE:
        why = " ".join(moved[f"VOL-II-T2-4-{p}"]["why"])
        assert f"proposed op {OP} ({AWAIT})" in why, (p, why)


# ---------------------------------------------------------------------------------------------- R1-9

def test_r1_9_issue_since_synthetic():
    order = ["BASE", "ADD-01", "ADD-02"]
    first = {"V:1": "BASE", "A1:Q2": "ADD-01", "A2:2.1": "ADD-02"}.get
    assert signals.issue_since({"since": "ADD-01"}, order, first) == "ADD-01"
    assert signals.issue_since({"units": ["V:1", "A2:2.1", "A1:Q2"]}, order, first) == "ADD-02"
    assert signals.issue_since({"text": "no units"}, order, first) == "BASE"
    from types import SimpleNamespace as NS
    ev = {s: {} for s in order}
    r = {"curated_issues": {"I-Q": {"text": "t", "owner": "Legal"}}, "order": order,
         "evals": [{"row": NS(id="R", issues=["I-Q"]), "stages": ev}]}
    signals.attach_pending(r, None, {"I-Q": "ADD-02"})
    assert ev["BASE"]["pending"] == ev["ADD-01"]["pending"] == [] and ev["ADD-02"]["pending"] == ["open: I-Q, human decision pending"]


def test_r1_9_page_limit_q2_bears_from_add02(real, a2d):
    cur = real["curated_issues"][Q2]
    order = real["order"]
    assert stage2.issue_stages(real)[Q2] == "ADD-02", cur
    e = next(x for x in real["evals"] if x["row"].id == "VOL-I-9.2-01")
    # session 14 (F1; R1-4): Q2 is re-presented as an applied rule awaiting the Bid manager's confirmation (not a
    # human decision pending); it still bears from ADD-02 only and its row stays not settled there
    assert signals.awaiting_note(Q2) not in e["stages"]["ADD-01"]["pending"]
    assert signals.awaiting_note(Q2) in e["stages"]["ADD-02"]["pending"]
    assert signals.pending_note(Q2) not in e["stages"]["ADD-02"]["pending"]
    moved = {(m["stage"], m["row"]): m for m in a2d["rows_moved"]}
    assert moved[("ADD-01", "VOL-I-9.2-01")]["change"] == signals.CONFIRMED, moved[("ADD-01", "VOL-I-9.2-01")]
    at2 = moved[("ADD-02", "VOL-I-9.2-01")]
    # ADD-02 amends the row (2.1: 150 pages), so the label is CHANGED, which outranks NOT SETTLED; it is never
    # CONFIRMED, and the open decision is named on the line
    assert at2["change"] != signals.CONFIRMED and signals.awaiting_note(Q2) in " ".join(at2["why"]), at2  # s14 F1 R1-4
    assert order.index("ADD-02") > order.index("ADD-01")


# ---------------------------------------------------------------------------------------------- R1 nits

def test_r1_nit_at_all_times_lives_in_its_own_issue(real):
    cur = real["curated_issues"]
    t = cur[T24]["text"]
    assert "the 'at all times' reading is I-VOL-II-AT-ALL-TIMES" in t, t
    assert "continuous compliance" not in t and "Proposed reading" not in t, t
    assert "continuous compliance" in cur["I-VOL-II-AT-ALL-TIMES"]["text"]
    assert stage2.pending_wording_findings(real) == []


def test_r1_nit_relationship_impact_carries_the_context(built):
    col = "context (not binding)"
    j = json.loads(_txt(built / "a2/a2_relationship_impact.json"))
    assert col in [c["header"] for c in j["columns"]]
    permit = [x for x in j["rows"] if "REL-MISSING-ENVIRONMENTAL-PERMIT" in " ".join(x["path"]) + " ".join(x["blocked_by"])]
    assert permit and all("the permit was under review by the regulator" in x[col] for x in permit), permit[:1]
    assert "context (not binding)" in _txt(built / "a2/a2_relationship_impact.csv").splitlines()[0]
    assert all(not x[col] for x in j["rows"] if x not in permit and "REL-MISSING-ENVIRONMENTAL-PERMIT" not in str(x))


# ---------------------------------------------------------------------------------------------- R2-11

def test_r2_11_folded_pending_issue_named_on_the_parent_synthetic():
    issues = [{"id": "I-P", "owner": "Bid manager"}, {"id": "I-C", "owner": "Bid manager",
                                                       "human_decision": H.HUMAN_DECISION_PENDING}]
    issues.append({"id": "I-D", "owner": "Legal", "human_decision": H.HUMAN_DECISION_PENDING + " (x)"})
    assert stage2.folded_pending(["I-C"], issues) == ["I-C (Bid manager)"]
    assert stage2.folded_pending(["I-C"], issues, "Bid manager") == ["I-C"]            # the line shows its owner
    assert stage2.folded_pending(["I-P", "I-C", "I-D"], issues, "Bid manager") == ["I-C", "I-D (Legal)"]
    assert stage2.folded_pending(["I-P"], issues) == []


def test_r2_11_page_limit_q2_is_named_with_the_mark_on_its_parent(built):
    a3 = json.loads(_txt(built / "a3/a3.json"))
    pg = stage2.condense_a3(a3, max(2, a3["condensed"]))
    assert a3["condensed"] <= 2, a3["condensed"]
    items = {i["id"]: i for g in pg["groups"]["groups"] for i in g["items"]}
    par = next(i for i in items.values() if Q2 in (i.get("folds") or []))
    # session 14 (F1; R1-4): Q2 is now an applied rule awaiting the Bid manager's confirmation, not a pending decision,
    # so the parent folds it without the pending mark (the rule for a folded PENDING issue is checked synthetically)
    assert par["folds_pending"] == [] and par["owner"] == "Bid manager", par
    from tenderpack import render
    html = render._a3_html(pg)
    text = re.sub(r"<[^>]+>", "", html)
    assert "(Bid manager) +1" in text and f"{stage2.A3_PENDING_MARK} {Q2}" not in text, re.findall(r"\+\d[^\n]*", text)


# ---------------------------------------------------------------------------------------------- R2-12

def _words(t) -> set[str]:
    return {w for w in re.split(r"[^a-z0-9]+", str(t).lower()) if w}


def test_r2_12_question_label_from_subject_words_synthetic():
    assert stage2.question_subject({"id": "CQ-F4D-GUARANTEE-SCOPE", "topic": "guarantee wording"}) == "guarantee scope"
    assert stage2.question_subject({"id": "CQ-RESERVOIR", "topic": "other (scope definition: treated effluent "
                                    "storage reservoir)"}) == "treated effluent storage reservoir"
    assert stage2.question_subject({"id": "CQ-X-RUN", "topic": "permit (rolling averages in the run)"}) == \
        "rolling averages in the run"


def test_r2_12_no_page_label_contradicts_its_entry(built, real):
    a3 = json.loads(_txt(built / "a3/a3.json"))
    note = " ".join(g.get("unlisted") or "" for g in a3["groups"]["groups"])
    assert "CQ-F4D-GUARANTEE-SCOPE (guarantee scope" in note, note
    qs = {str(c["id"]): c for c in real["clarifications"]["clarifications"]}
    for cid, label in re.findall(r"(CQ-[A-Z0-9-]+) \(([^;)]+)", note):
        q = qs[cid]
        m = re.match(r"^[^()]*\((.+)\)$", str(q.get("topic") or ""))
        allowed = _words(cid) | _words(m.group(1) if m else "")
        assert _words(label) <= allowed, (cid, label, _words(label) - allowed)


# ---------------------------------------------------------------------------------------------- R2 note (A5)

def test_r2_note_open_decision_date_synthetic():
    # R3's rule (coordinator, 11:5x): min(the clarification route's ask-by, the activity's latest start)
    acts = [{"id": "a", "req_ids": ["R1"], "flags": [], "decision_status": "READY", "latest_start": "2026-11-20",
             "ask_by": "2026-11-11", "decision_needed_by": None},
            {"id": "b", "req_ids": ["R2"], "flags": [], "decision_status": "READY", "latest_start": "2026-11-05",
             "ask_by": None, "decision_needed_by": None},
            {"id": "c", "req_ids": ["R3"], "flags": [], "decision_status": "READY", "latest_start": "2026-11-25",
             "ask_by": None, "decision_needed_by": None},
            {"id": "d", "req_ids": [], "flags": [], "decision_status": "READY", "latest_start": "2026-11-01",
             "ask_by": None, "decision_needed_by": None}]
    pend = {"I-Q": {"short": "q", "owner": "Legal"}, "I-N": {"short": "n", "owner": "Legal"}}
    programme.inherit_open_decisions(acts, {"R1": ["I-Q"], "R2": ["I-N"], "R3": ["I-N"]}, pend,
                                     questions={"I-Q": ["CQ-Q"]}, route_ask_by="2026-11-11")
    a, b, c, d = acts
    assert a["decision_needed_by"] == "2026-11-11" and "CQ-Q" in a["decision_needed_by_basis"], a
    assert a["decision_needed_by_basis"].startswith(programme.ASK_BY_BASIS)
    assert b["decision_needed_by"] == "2026-11-05" and b["decision_needed_by_basis"] == programme.NO_QUESTION_BASIS, b
    assert c["decision_needed_by"] == "2026-11-11" and "no question drafted" in c["decision_needed_by_basis"], c
    assert d["decision_needed_by"] is None and d["decision_needed_by_basis"] is None        # no open decision


def test_r2_note_every_open_decision_has_a_date(built):
    prog = {a["id"]: a for a in json.loads(_txt(built / "a5/programme.json"))["rows"]}
    tp = prog["technical-proposal"]
    assert tp["decision_needed_by"] == min(tp["latest_start"], tp["ask_by"]), tp
    assert "CQ-T24-RANGES" in tp["decision_needed_by_basis"], tp["decision_needed_by_basis"]
    for a in prog.values():                     # every activity with an open decision has a date and its basis
        if any(f.startswith(programme.OPEN_DECISION_FLAG) for f in a["flags"]):
            assert a["decision_needed_by"] and (a["gated_by"] or a["decision_needed_by_basis"]), a["id"]
            if not a["gated_by"]:
                assert a["decision_needed_by"] == min(x for x in (a["latest_start"], a["ask_by"] or "2026-11-11") if x)
    assert prog["pcg-wording"]["decision_needed_by"], prog["pcg-wording"]      # R3 N-2: no ask_by, still a date


# ---------------------------------------------------------------------------------------------- R3 recheck N-1 (A5)

def test_n1_open_decision_reach_synthetic():
    acts = [{"id": "f4a", "req_ids": ["F4A-1", "GEN"], "evidence": "EV-4A"},
            {"id": "f4a-prep", "req_ids": ["F4A-1", "VALID"], "evidence": "EV-4A"},
            {"id": "poa", "req_ids": ["GEN"], "evidence": "EV-POA"},
            {"id": "f4b", "req_ids": ["GEN"], "evidence": "EV-4B"},
            {"id": "clar", "req_ids": ["Q-ROW"], "evidence": "EV-CLAR"}]
    by_row = {"F4A-1": ["I-F"], "GEN": ["I-F"], "VALID": ["I-F"], "Q-ROW": ["I-F"]}
    reach = programme.open_decision_reach(acts, by_row, {"I-F": {}}, route="clar")
    assert reach == {"I-F": {"f4a", "f4a-prep"}}, reach              # the generic row does not spread it
    for a in acts:
        a.update(flags=[], decision_status="READY")
    programme.inherit_open_decisions(acts, by_row, {"I-F": {"short": "s", "owner": "Legal"}}, reach=reach, route="clar")
    assert {a["id"] for a in acts if a["open_decisions"]} == {"f4a", "f4a-prep", "clar"}


def test_n1_f4a_fields_on_the_form_4a_steps_and_the_clarifications_step_only(built):
    prog = {a["id"]: a for a in json.loads(_txt(built / "a5/programme.json"))["rows"]}
    on = {k for k, a in prog.items() if any(f.startswith(programme.OPEN_DECISION_FLAG) and "I-F4A-FIELDS:" in f
                                            for f in a["flags"])}
    assert on == {"form-4a-prep", "form-4a", "clarifications"}, on
    t24 = {k for k, a in prog.items() if any(f.startswith(programme.OPEN_DECISION_FLAG) and f"{T24}:" in f
                                             for f in a["flags"])}
    assert {"technical-proposal", "deviations-review", "form-4e"} <= t24, t24
    clar = next(f for f in prog["clarifications"]["flags"] if f.startswith(programme.OPEN_DECISION_FLAG))
    pend = {i for i in re.findall(r"(I-[A-Z0-9-]+): ", clar)}
    assert T24 in pend and "I-F4A-FIELDS" in pend and CP in pend, pend


# ---------------------------------------------------------------------------------------------- R3 recheck R3-1 (Gantt)

def test_r3_1_the_open_decision_tag_yields_last_synthetic():
    from tenderpack import gantt
    tags = [("REVIEW (confirmed dependency)", "w", "square"),
            ("BLOCKED: cannot be established: the Environmental Permit issued for the site not supplied", "c", "square"),
            ("OPEN DECISION (7); question drafted: ask by 11 Nov", "w", "diamond")]
    vs = gantt.tag_variants(tags)
    assert vs[0] == tags and all(any(t[0].startswith("OPEN DECISION") for t in v) for v in vs[:-1])
    assert not any(t[0].startswith("OPEN DECISION") for t in vs[-1])          # only the last variant drops it
    assert all(any(t[0].startswith("BLOCKED") for t in v) for v in vs)        # BLOCKED is never dropped
    assert ("BLOCKED, not supplied: Environmental Permit issued for the site", "c", "square") in vs[4]


def _row_texts(words, aid):
    """The texts on the Gantt row of `aid` (pdf words: x0, y0, x1, y1, text): the row's label line and the line below."""
    ys = [w[1] for w in words if w[4] == aid and w[0] < 120]
    assert ys, aid
    return " ".join(w[4] for w in words if any(-2 <= w[1] - y <= 9 for y in ys))


def test_r3_1_the_gantt_names_the_open_decision_on_the_three_activities(built):
    import pymupdf
    doc = pymupdf.open(built / "a5/gantt.pdf")
    words = doc[0].get_text("words")
    text = doc[0].get_text()
    for aid in ("technical-proposal", "deviations-review", "form-4e"):
        assert "OPEN DECISION" in _row_texts(words, aid), (aid, _row_texts(words, aid))
    assert "maxima" in text and T24 in text, "the printed notes say what is open"
    assert max(w[3] for w in words) <= doc[0].rect.height, "nothing runs past the page"
    for name in ("gantt.svg", "gantt.html"):
        src = _txt(built / "a5" / name)
        assert "all values are maxima" in src, name
        rows = {}
        for m in re.finditer(r'<text x="([\d.]+)" y="([\d.]+)"[^>]*>([^<]*)</text>', src):
            rows.setdefault(round(float(m.group(2))), []).append((float(m.group(1)), m.group(3)))
        for aid in ("technical-proposal", "deviations-review", "form-4e"):
            y = next(y for y, ts in rows.items() if any(t.startswith(aid) for _, t in ts))
            near = " ".join(t for yy, ts in rows.items() if -6 <= yy - y <= 6 for _, t in ts)
            assert "OPEN DECISION" in near, (name, aid, near[:300])


# ---------------------------------------------------------------------------------------------- R2-8

def test_r2_8_compliance_point_is_an_open_pending_issue(real, a1, built):
    cur = real["curated_issues"]
    assert CP in cur, "no issue says the compliance point of Table 2-4 is open"
    it = cur[CP]
    assert it["owner"] == "Process engineer" and it["theme"] == cur[T24]["theme"]
    t = it["text"]
    texts = {u["unit_id"]: u.get("text") or "" for u in real["units"]}
    for words, unit in (("Minimum Effluent Quality Parameters at the Point of Discharge", "VOL-II:T2-4"),
                        ("Continuous at outlet", "VOL-II:T2-4/pH"),
                        ("the delivery point shown on Drawing 03-C-114", "VOL-II:5.1")):
        assert words in t and words in " ".join(texts[unit].split()), (words, unit)
    assert "p3" in t and "p4" in t and "Volume III" in t and "not supplied" in t
    assert "whether to raise it with the Authority" in t and "Process engineer" in t
    assert CP in real["pending_issues"]
    assert not any(CP in (c.get("linked_issues") or []) for c in real["clarifications"]["clarifications"])
    rows = _a1_rows_of(a1, CP)
    want = {f"VOL-II-T2-4-{p}" for p in NINE + ["TN"]} | {"VOL-II-5.1-01"}
    assert want <= rows, want - rows
    a3 = json.loads(_txt(built / "a3/a3.json"))
    assert a3["condensed"] <= 2, a3["condensed"]
    pg = stage2.condense_a3(a3, max(2, a3["condensed"]))
    on = {i["id"] for g in pg["groups"]["groups"] for i in g["items"]}
    folded = " ".join(f for g in pg["groups"]["groups"] for i in g["items"] for f in i.get("folds_pending") or [])
    assert CP in on or CP in folded


# ---------------------------------------------------------------------------------------------- R1 (quantified_row)

def test_quantified_row_does_not_match_cover_text_synthetic():
    from tenderpack.citations import quantified_row
    ids = {"VOL-II:T2-4", "VOL-II:T2-4/BOD5", "VOL-I:3.2"}
    for t in ("All other terms and conditions remain unchanged.",
              "All other terms of the RFP Documents remain unchanged.",
              "All other provisions of the RFP remain unchanged and in full force and effect.",
              "Except as amended by this Addendum, all other items of the RFP Documents remain unchanged."):
        assert not quantified_row("VOL-II:T2-4/BOD5", t, ids)[0], t
