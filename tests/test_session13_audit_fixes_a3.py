"""Session 13, fixer F2: reviewer R2's findings on A3, the human-owned decisions across the deliverables and the
clarification register (audit report R2, findings R2-1 .. R2-10), and R3-1's A5 part (an activity shows the open
human-owned issues of the rows it carries). Each test states the general rule and checks it on the real pack (the
committed evidence build, rendered into pytest's temporary folders) and, where the rule is code, on small synthetic data.
Nothing writes to the repository; nothing here records, accepts or approves anything.

  R2-1  every `pending_decision` entry of the clarification register is mirrored by an issue (it links one), so A1's
        Issues sheet, the A3 page, a3_detail.html and A4 name ONE pending set, A4's pending_decision list included.
  R2-5  one owner per judgment: a register entry's decision owner is the owner of the issue it is about (its first linked
        issue; one function, human_owned.judgment_owner) in A1, A3 and A4; ENV-A-PRICES and ENV-B carry the ⚑.
  R2-3  when an issue has a curated `a3` text, the A3 page uses it before any generated summary; the maxima/range line
        names the qualifier and is marked † (decide before submission).
  R2-4  the interim handling of a register entry whose question is a pending human decision (it links an issue that is
        HUMAN DECISION PENDING) is labelled 'Proposed interim basis, pending <owner> (no decision recorded):'.
  R2-6  A3 calls the register 'clarification register (supporting record, out/a4/clarification_register.*)', not 'A4'.
  R2-7  the register's csv, json and md carry 'Rows/units its answer would change'; every entry reaches a row or issue.
  R2-8  a row read from a table row keeps the table's printed title (Table 2-4: 'at the Point of Discharge').
  R2-9  one count for the trigger set: '16 (+ VOL-IV-F4C-N1, which restates VOL-I-9.4-01)' on the page, the detail, the
        batch and checks.json.
  R2-10 a mixed Arabic/Latin line of a reading renders right-to-left (dir rtl/auto) in the review pages.
  R2-2/R3-1 (A5) an activity inherits the open human-owned issues of the rows it carries (a readable note, the Gantt);
        whether that changes READY is one named rule (programme.OPEN_DECISION_RULE), off unless the owner turns it on.
"""
from __future__ import annotations

import csv
import io
import json
import re
from pathlib import Path

import pytest

from tenderpack import clarify, programme, stage2
from tenderpack import human_owned as H
from tenderpack.util import ROOT

EVIDENCE = ROOT / "build"
PACK = ROOT / "config/pack.yaml"


@pytest.fixture(scope="module")
def real():
    return stage2.run(EVIDENCE, PACK, ROOT)


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("s13-f2-out") / "out"
    res = stage2.build(EVIDENCE, out, PACK, ROOT, quiet=True)
    assert res["status"] == "ok", res.get("status")
    return out


def _txt(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _csv(p: Path) -> list[dict]:
    return list(csv.DictReader(io.StringIO(_txt(p).lstrip("﻿"))))


def _page(built):
    a3 = json.loads(_txt(built / "a3/a3.json"))
    return a3, stage2.condense_a3(a3, max(2, a3["condensed"]))


def _items(pg):
    return {i["id"]: i for g in pg["groups"]["groups"] for i in g["items"]}


# ---------------------------------------------------------------------------------------------- R2-1

def test_r2_1_a_pending_decision_without_an_issue_is_a_finding():
    reg = {"pending_decision": [{"topic": "t", "finding": "f", "decision_owner": "Legal", "linked_issues": [],
                                 "sources": []}]}
    found = clarify.check(reg, [], {"I-X"})
    assert any("mirrored by an issue" in f for f in found), found
    reg["pending_decision"][0]["linked_issues"] = ["I-X"]
    assert not any("mirrored by an issue" in f for f in clarify.check(reg, [], {"I-X"}))


def test_r2_1_every_pending_decision_of_the_real_register_links_a_curated_issue(real):
    cur = real["curated_issues"]
    pend = real["clarifications"]["pending_decision"]
    assert pend
    for c in pend:
        assert [i for i in c.get("linked_issues") or [] if i in cur], c["topic"]
    at = next(c for c in pend if "at all times" in c["topic"])
    # session 14 (F1; R1-4): the page-limit point is re-presented as an applied rule (PROPOSED BASIS; its issue stays
    # open for the Bid manager to confirm) and listed as checked with no question, so it is no pending decision
    assert not [c for c in pend if c["topic"].startswith("page limit")]
    new = {i for i in at["linked_issues"]} - {"I-VOL-II-T24-TENSIONS"}
    assert len(new) >= 1, new
    for i in new:                       # PROPOSED curated issues in the words A4 uses, with A4's owner
        assert cur[i]["owner"] in ("Process engineer", "Bid manager"), (i, cur[i]["owner"])


def test_r2_1_one_pending_set_in_a1_a3_page_a3_detail_and_a4_pending_decision(built, real):
    a1 = json.loads(_txt(built / "a1/a1.json"))
    a1_set = {r["id"] for r in a1["sheets"]["Issues"]["rows"]
              if str(r.get("text") or "").startswith(H.HUMAN_DECISION_PENDING)}
    a3, pg = _page(built)
    page = {i["id"] for g in pg["groups"]["groups"] for i in g["items"] if stage2.A3_PENDING_MARK in i["short"]}
    page_folded = {f for g in pg["groups"]["groups"] for i in g["items"] for f in i.get("folds") or []}
    det = set(re.findall(r'<tr id="([^"]+)"><td><b>[^<]+</b>[^<]*' + stage2.A3_PENDING_MARK,
                         _txt(built / "a3/a3_detail.html")))
    a4 = json.loads(_txt(built / "a4/clarification_register.json"))
    per_entry = [set(c.get("linked_issues") or []) for c in a4["pending_decision"]]
    a4_set = set().union(*per_entry) | {x["id"] for x in a4.get("pending_issues") or []}
    cur = set(real["curated_issues"])
    a1_set, a4_set, det = a1_set & cur, a4_set & cur, det & cur
    # every pending decision of A4 is one of the pending issues of A1, A3 and the detail (none is A4-only)
    assert all(s & a1_set for s in per_entry), [c["topic"] for c, s in zip(a4["pending_decision"], per_entry)
                                                 if not s & a1_set]
    rows = {r["id"]: r.get("rows") for r in a1["sheets"]["Issues"]["rows"]}
    assert "VOL-II-2.4-01" in str(rows["I-VOL-II-AT-ALL-TIMES"]) and "VOL-I-9.2-01" in str(rows["I-VOL-I-PAGE-LIMIT-Q2"])
    assert a1_set == a4_set == det, (a1_set ^ a4_set, a1_set ^ det)
    assert (page | (page_folded & a1_set)) & cur == a1_set, a1_set ^ (page & cur)


# ---------------------------------------------------------------------------------------------- R2-5

def test_r2_5_owner_is_one_function_and_a_mismatch_is_a_finding():
    issues = {"I-A": {"owner": "Legal counsel"}, "I-B": {"owner": "Bid manager"}}
    assert H.judgment_owner({"decision_owner": "Legal", "linked_issues": ["I-A"]}, issues) == "Legal counsel"
    assert H.judgment_owner({"decision_owner": "Legal", "linked_issues": []}, issues) == "Legal"
    assert H.same_owner("Legal", "Legal counsel") and not H.same_owner("Technical", "Process engineer")
    reg = {"clarifications": [{"id": "CQ-X", "decision_owner": "Legal", "linked_issues": ["I-B"]}]}
    assert any("decision owner" in f and "I-B" in f for f in H.owner_findings(reg, issues))


def test_r2_5_real_pack_one_owner_per_judgment(real, built):
    cur = real["curated_issues"]
    assert not H.owner_findings(real["clarifications"], cur), H.owner_findings(real["clarifications"], cur)
    assert H.same_owner(cur["I-VOL-I-ENV-A-PRICES"]["owner"], "Legal")       # VOL-I 6.2 non-responsiveness: Legal
    assert cur["I-FLOWS"]["owner"] == "Process engineer"                       # flows: the Process engineer
    a4 = json.loads(_txt(built / "a4/clarification_register.json"))
    rows = {r["id"]: r for r in a4["rows"]}
    assert H.same_owner(rows["CQ-F4B-CONTRACT-VALUE"]["decision_owner"], cur["I-VOL-I-ENV-A-PRICES"]["owner"])
    flows = next(c for c in a4["pending_decision"] if "I-FLOWS" in (c.get("linked_issues") or []))
    assert flows["decision_owner"] == cur["I-FLOWS"]["owner"]


def test_r2_5_env_a_prices_and_env_b_carry_the_pending_mark(built):
    _, pg = _page(built)
    items = _items(pg)
    for iid in ("I-VOL-I-ENV-A-PRICES", "I-VOL-I-ENV-B"):
        assert items[iid]["short"].startswith(stage2.A3_PENDING_MARK), items[iid]
        assert items[iid]["decide"], items[iid]


# ---------------------------------------------------------------------------------------------- R2-3

def test_r2_3_the_page_uses_the_curated_a3_text_before_a_generated_summary():
    i = {"id": "I-X", "a3": "the curated A3 words", "short": "a short", "text": "Long text. Open: the gap"}
    assert stage2.issue_short(i) == "the curated A3 words"
    lab = f"{H.HUMAN_DECISION_PENDING}: "
    j = {"id": "I-Y", "a3": lab + "curated", "short": lab + "short", "text": lab + "text. Open: gap"}
    assert stage2.issue_short(j) == lab + "curated"


def test_r2_3_maxima_and_permit_lines_on_the_real_page(built):
    _, pg = _page(built)
    items = _items(pg)
    t24 = items["I-VOL-II-T24-TENSIONS"]
    assert "all values are maxima" in t24["short"] and "0.5" in t24["short"] and "6.0" in t24["short"], t24
    assert t24["decide"], t24                                         # † decide before submission
    assert "prevails over the Table 2-4 reproduction" in items["I-PERMIT"]["short"], items["I-PERMIT"]


# ---------------------------------------------------------------------------------------------- R2-4

def test_r2_4_interim_handling_of_a_pending_question_is_labelled_proposed():
    reg = {"clarifications": [
        {"id": "CQ-P", "decision_owner": "Legal", "linked_issues": ["I-P"], "interim_handling": "Carry both readings."},
        {"id": "CQ-O", "decision_owner": "Bid manager", "linked_issues": ["I-O"], "interim_handling": "Do x."}]}
    pending = [{"id": "I-P", "owner": "Legal", "text": "t", "reasons": ["r"]}]
    out = clarify.presented(reg, None, pending, {"I-P": {"owner": "Legal"}, "I-O": {"owner": "Bid manager"}})
    by = {c["id"]: c for c in out}
    assert by["CQ-P"]["interim_handling"] == ("Proposed interim basis, pending Legal (no decision recorded): "
                                              "Carry both readings.")
    assert by["CQ-O"]["interim_handling"] == "Do x."
    again = clarify.presented({"clarifications": out}, None, pending, {"I-P": {"owner": "Legal"}})
    assert again[0]["interim_handling"].count("Proposed interim basis") == 1     # never prefixed twice


def test_r2_4_real_register_t24_ranges_and_concession(built):
    a4 = json.loads(_txt(built / "a4/clarification_register.json"))
    rows = {r["id"]: r for r in a4["rows"]}
    for cid in ("CQ-T24-RANGES", "CQ-CONCESSION-TERM", "CQ-F4B-CONTRACT-VALUE"):
        ih = rows[cid]["interim_handling"]
        assert ih.startswith(f"Proposed interim basis, pending {rows[cid]['decision_owner']} (no decision recorded): "), ih
        assert ih.count("no decision recorded") == 1, ih
    det = _txt(built / "a3/a3_detail.html")
    assert "Proposed interim basis, pending Process engineer (no decision recorded): Treat both ranges" in det


# ---------------------------------------------------------------------------------------------- R2-6

def test_r2_6_a3_names_the_clarification_register_not_a4(built):
    a3, pg = _page(built)
    det = _txt(built / "a3/a3_detail.html")
    label = "clarification register (supporting record, out/a4/clarification_register.*)"
    assert label in pg["groups"]["heading"] + pg["groups"]["note"] and label in det, pg["groups"]["heading"]
    assert "(not sent; A4)" not in json.dumps(pg) and "A4 clarification register" not in det


# ---------------------------------------------------------------------------------------------- R2-7

def test_r2_7_register_rows_column_in_csv_json_md(built, real):
    col = "Rows/units its answer would change"
    j = json.loads(_txt(built / "a4/clarification_register.json"))
    assert col in [c["header"] for c in j["columns"]]
    c = _csv(built / "a4/clarification_register.csv")
    assert col in c[0]
    md = _txt(built / "a4/clarification_register.md")
    assert f"**{col}:**" in md
    by = {r["id"]: r for r in j["rows"]}
    rows_in_force = {e["row"].id for e in real["evals"]}
    for cid, r in by.items():               # every entry reaches at least one row (or issue)
        assert r["answer_rows"] or r["linked_issues"], cid
        assert set(r["answer_rows"]) <= rows_in_force, (cid, set(r["answer_rows"]) - rows_in_force)
    assert "VOL-II-7.2-01" in by["CQ-PCOD-RELIABILITY-RUN"]["answer_rows"]
    assert "VOL-V-42.1-02" in by["CQ-HANDBACK-CONDITION"]["answer_rows"]
    assert "VOL-II-1.2-01" in by["CQ-RESERVOIR"]["answer_rows"]
    assert {"VOL-IV-F4D-02", "VOL-IV-F4D-08"} <= set(by["CQ-F4D-GUARANTEE-SCOPE"]["answer_rows"])


def test_r2_7_a3_page_names_the_questions_tied_to_no_listed_issue(built):
    _, pg = _page(built)
    note = " ".join(g.get("unlisted") or "" for g in pg["groups"]["groups"])
    assert "no bid-out row" in note, note
    for cid in ("CQ-PCOD-RELIABILITY-RUN", "CQ-HANDBACK-CONDITION", "CQ-RESERVOIR", "CQ-F4D-GUARANTEE-SCOPE"):
        assert cid in note, (cid, note)


# ---------------------------------------------------------------------------------------------- R2-8

def test_r2_8_table_rows_keep_the_printed_table_title(built):
    a1 = json.loads(_txt(built / "a1/a1.json"))
    rows = [r for r in a1["rows"] if str(r["id"]).startswith("VOL-II-T2-4-")
            and r["id"] != "VOL-II-T2-4-NOTE1"]
    assert len(rows) == 10
    for r in rows:
        assert "Minimum Effluent Quality Parameters at the Point of Discharge" in r["note"], (r["id"], r["note"])


# ---------------------------------------------------------------------------------------------- R2-9

def test_r2_9_one_count_for_the_trigger_set(built, real):
    from tenderpack.schedule import a3_rows
    words = "16 (+ VOL-IV-F4C-N1, which restates VOL-I-9.4-01)"
    n = len(a3_rows(real["evals"], real["validated"].stage))          # F3's one set: the page, A5 and the live diff
    full = f"{words} explicit bid-out triggers + 1 below the score threshold = {n} A3 rows"
    a3, pg = _page(built)
    assert full in pg["subtitle"], pg["subtitle"]
    assert n == len(a3["explicit"]) + len(a3["score"]) == 18
    det = _txt(built / "a3/a3_detail.html")
    assert f"Explicit consequences ({words})" in det
    b2 = _txt(built / "review/batch-02-disqualifiers.html")
    assert full in b2 and "18 rows" not in b2
    c13 = next(c for c in json.loads(_txt(built / "checks.json"))["structural"] if c["id"] == "C13")
    assert full in c13["detail"] and not re.search(r"\b1[78]\b", c13["detail"].replace(full, "")), c13
    c48 = next(c for c in json.loads(_txt(built / "checks.json"))["reported"] if c["id"] == "C48")
    assert f"{n} A3 (bid-out) rows" in c48["detail"] and "explicit plus the score row" in c48["detail"], c48
    cov = json.loads(_txt(built / "a5/requirements_coverage.json"))
    assert "explicit plus the score row" in json.dumps(cov), str(cov)[:300]
    assert "explicit plus the score row" in _txt(built / "a5/README.md")


# ---------------------------------------------------------------------------------------------- R2-10

def test_r2_10_mixed_lines_render_right_to_left(built):
    b1 = _txt(built / "review/batch-01-image-readings.html")
    m = re.search(r'<p dir="(\w+)">مناقصة رقم: NUPA/ISTP/2026/014</p>', b1)
    assert m and m.group(1) in ("rtl", "auto"), m and m.group(0)


def test_r2_10_direction_rule():
    from tenderpack.batches import text_dir
    assert text_dir({"lang": "ar", "text": "أ"}) == "rtl"
    assert text_dir({"lang": "mixed", "text": "مناقصة رقم: NUPA"}) == "rtl"
    assert text_dir({"lang": "mixed", "text": "NUPA رقم"}) == "auto"
    assert text_dir({"lang": "en", "text": "x"}) == "ltr"


# ---------------------------------------------------------------------------------------------- R2-2 / R3-1 (A5)

def test_a5_activity_inherits_the_open_issues_of_the_rows_it_carries_synthetic():
    acts = [{"id": "a1", "req_ids": ["R1", "R2"], "flags": [], "decision_status": "READY", "gated_by": []},
            {"id": "a2", "req_ids": ["R3"], "flags": [], "decision_status": "READY", "gated_by": []}]
    by_row = {"R1": ["I-P"], "R2": ["I-P", "I-Q"], "R3": ["I-Q"]}
    pending = {"I-P": {"short": "the point", "owner": "Process engineer"}}
    programme.inherit_open_decisions(acts, by_row, pending, gate=False)
    # session 14 (F2; R3 m2): one decision state: not gated, its finalisation needs the decision
    assert acts[0]["open_decisions"] == ["I-P"] and acts[0]["decision_status"].startswith("NOT GATED (")
    f = [x for x in acts[0]["flags"] if x.startswith("OPEN DECISION")]
    assert f and "I-P: the point (Process engineer; rows R1, R2)" in f[0], f
    assert acts[1].get("open_decisions") in (None, []) and not acts[1]["flags"]
    programme.inherit_open_decisions(acts, by_row, pending, gate=True)
    assert acts[0]["decision_status"].startswith("REVIEW (open decision)"), acts[0]["decision_status"]


def test_a5_real_pack_t24_on_the_three_activities_and_the_gantt(built):
    prog = {a["id"]: a for a in json.loads(_txt(built / "a5/programme.json"))["rows"]}
    for aid in ("technical-proposal", "deviations-review", "form-4e"):
        a = prog[aid]
        f = " | ".join(x for x in a["flags"] if x.startswith("OPEN DECISION"))
        assert "I-VOL-II-T24-TENSIONS: " in f and "all values are maxima" in f, (aid, f[:300])
        # the gate rule is off unless turned on (session 14, F2; R3 m2: said as NOT GATED, never READY)
        assert a["decision_status"].startswith("NOT GATED ("), a["decision_status"]
    for name in ("gantt.svg", "gantt.html"):
        assert "OPEN DECISION" in _txt(built / "a5" / name), name
    readme = _txt(built / "a5/README.md")
    assert "I-VOL-II-T24-TENSIONS" in readme and "all values are maxima" in readme
    assert programme.OPEN_DECISION_RULE in readme


# ---------------------------------------------------------------------------------------------- F3 leftover (R3-5)

def test_the_a3_set_is_one_set_on_the_page_in_a5_and_in_the_live_diff(real, built):
    """The live diff's 'Disqualifiers (A3)' reads schedule.a3_rows like the page and A5 (it used BID_OUT only and left
    the score row out): the three sets are equal on the real pack."""
    from tenderpack.schedule import a3_rows
    from tenderpack import live
    v = real["validated"].stage
    a3 = json.loads(_txt(built / "a3/a3.json"))
    page = {x["id"] for x in a3["explicit"]} | {x["id"] for x in a3["score"]}
    a5 = set(json.loads(_txt(built / "a5/stages" / f"{v}.json"))["a3_coverage"]["rows"])
    one = set(a3_rows(real["evals"], v))
    stages = [s.stage for s in real["stages"]]
    _, data = live.diff(real, stages[stages.index(v) - 1], v)
    diffset = set(data["a3"]["rows"])
    assert page == a5 == one == diffset, (page ^ a5, page ^ one, page ^ diffset)
    assert "VOL-I-11.3-01" in one                               # the score row is a member
