"""Session 12, fixer F1: the content and wording findings of the session-12 audit (reports A1.md, A2.md, A3.md; R.md
R-1 and A4.md A4-2 for the clarification register). Each test reproduces one finding on the real pack (the committed
evidence build, read as tests/test_stage2.py reads it) or on small synthetic data, and states the general rule.

  concession  ADD-02 Q7 answers 'Which applies?' with "The Authority notes the question. The order of precedence at
              Volume I Clause 3.2 applies. The Authority does not consider further amendment necessary at this stage."
              It does not say which clause applies; VOL-I 3.3 puts a Bidder's own resolution "at its own risk"; no person
              has decided. The outputs must not say VOL-I 12.1 prevails, or that the term runs from PCOD, as settled.
  labels      a curated issue whose own words (quotations aside) assert a precedence/governing/interpretive judgment
              carries HUMAN DECISION PENDING until a person's decision is bound to it (human_owned.issue_label).
  checked     the clarification register's checked_no_question lists only points the pack's own words settle; a
              judgment is listed as pending with the person who owns it (pending_decision), never as settled.
  Q11         one wording: Q11 settles the question asked (design to the Volume II figures); "not contradictory" is an
              engineering reading, labelled as such; dry weather flow stays open.
  quotes      every 'Quoted words relied on' cell of A1 is a verbatim span of one page it cites.
  5.2         ADD-02-5.2-01 states no consequence: not a pass/fail gate.
  as issued   one rule for 'Text as issued' of a row first issued by an addendum: the addendum's own text, with its page.
  provenance  no A1 cell cites an internal audit id ('session 11 audit A1-3').
  answers     ADD-01 Q1 is to be re-read after ADD-02 5.1/5.2; ADD-01 4.1 and 4.2 are reversed and revoked by the pack.
  dates       A2 shows both readings of a date whose counting convention is not stated.
  indirect    the Local Content Certificate's path to VOL-I 9.1(i), the Form 4-G index, VOL-V 36.2 to Form 4-E.

Passing these tests does not make any interpretation correct or any reading approved; nothing here records a decision."""
from __future__ import annotations

import json
import re
import unicodedata

import pytest

from tenderpack import clarify, human_owned as H, stage2
from tenderpack.util import ROOT

EVIDENCE = ROOT / "build"
PACK = ROOT / "config/pack.yaml"
# quotations are evidence, not the curator's own words (human_owned.QUOTE_KEYS; the same rule for running text)
_QUOTED = re.compile(r"(?<![A-Za-z])'[^'\n]*?'(?![A-Za-z])|\"[^\"\n]*\"|‘[^’]*’|“[^”]*”")
# 'which clause governs ... is a decision for a person' asks the question; 'X prevails' or 'X governs' answers it
_ASSERTS_PRECEDENCE = re.compile(r"\bprevail(?:s|ed|ing)?\b|\bsubordinate\b|(?<!which )(?<!which clause )\bgoverns?\b|"
                                 r"\bas ADD-02 Q7 directs\b|"
                                 r"\bruns? (?:25 years )?from PCOD\b|\bQ7 precedence answer\b", re.I)


def _own(text: str) -> str:
    return _QUOTED.sub(" ", str(text or ""))


@pytest.fixture(scope="module")
def real():
    return stage2.run(EVIDENCE, PACK, ROOT)


@pytest.fixture(scope="module")
def issues(real):
    return stage2.collect_issues(real, None)


@pytest.fixture(scope="module")
def a1(real, issues):
    return stage2.a1_table(real, issues)


@pytest.fixture(scope="module")
def a2(real):
    return stage2.a2(real)


def _row(real, rid):
    return next(e["row"] for e in real["evals"] if e["row"].id == rid)


def _a1row(a1, rid):
    return next(x for x in a1["rows"] if x["id"] == rid)


def _op(real, oid):
    return next(x for s in real["stages"] for x in s.ops if x.op.id == oid).op


def _cq(real, cid):
    return next(c for c in real["clarifications"]["clarifications"] if c["id"] == cid)


# ---------------------------------------------------------------------------------------------- labels (synthetic)

def test_issue_label_marks_a_curated_issue_that_asserts_a_judgment():
    judged = {"text": "Concession term: under VOL-I 3.2 Volume I prevails, so the term runs from PCOD", "owner": "Legal"}
    lab = H.issue_label("I-X", judged, [])
    assert lab and lab.startswith(H.HUMAN_DECISION_PENDING), lab
    # a quotation is evidence, not the curator's judgment; 'means of' is a noun, not an interpretation
    assert H.issue_label("I-Y", {"text": "the preamble prints 'the Environmental Permit shall prevail'", "owner": "T"},
                         []) is None
    assert H.issue_label("I-Z", {"text": "how its means of decryption is given", "owner": "Bid manager"}, []) is None
    # an open curated issue: unchanged. Session 12, F5 (audit A3-5): owner 'Legal' was the example here; an issue owned
    # by Legal or Commercial is now a person's judgment by its owner (human_owned.owner_judgment), so the open-issue case
    # uses an owner who is neither (behaviour changed deliberately; tested in test_session12_recheck_fixes.py)
    assert H.issue_label("I-W", {"text": "x", "owner": "Bid manager"}, []) is None
    # only a person's decision bound to the issue as it reads lifts the label
    dec = [{"kind": "issue", "item": "I-X", "decision": "accept", "reviewer": "Ahmad", "date": "2026-10-05",
            "fingerprint": H.entry_fingerprint("issue", judged)}]
    lab2 = H.issue_label("I-X", judged, dec)
    assert lab2 and H.HUMAN_DECISION_PENDING not in lab2 and "decision recorded: Ahmad" in lab2
    stale = [dict(dec[0], fingerprint=H.entry_fingerprint("issue", {**judged, "text": "older words"}))]
    assert H.issue_label("I-X", judged, stale).startswith(H.HUMAN_DECISION_PENDING)


# ---------------------------------------------------------------------------------------------- concession (A1-1 = A2-1 = A3-1)

CONCESSION_ROWS = ("VOL-I-12.1-01", "VOL-V-3.1-01", "VOL-V-3.2-01", "VOL-V-42.2-01")


def test_concession_rows_do_not_decide_which_clause_governs(real, a1):
    texts = []
    for rid in CONCESSION_ROWS:
        row = _row(real, rid)
        texts += [(rid, "confidence_reason", row.confidence_reason)]
        texts += [(rid, f"note@{it.stage}", it.note) for it in row.interpretations]
        if row.post_award_evidence:
            texts += [(rid, "when", row.post_award_evidence.when), (rid, "bid_stage_note", row.post_award_evidence.bid_stage_note)]
    bad = [(rid, k, t) for rid, k, t in texts if _ASSERTS_PRECEDENCE.search(_own(t))]
    assert not bad, bad
    i12, v31 = _row(real, "VOL-I-12.1-01"), _row(real, "VOL-V-3.1-01")
    assert i12.confidence == v31.confidence                         # the same confidence, the same reason
    for row in (i12, v31):
        assert "no decision recorded" in row.confidence_reason, row.confidence_reason
        note = row.interpretations[-1].note
        assert "The Authority notes the question." in note and "no decision recorded" in note, note
        assert "VOL-I 3.3" in note and "(a) the Addenda" in note, note
    for rid in CONCESSION_ROWS:                                     # no internal audit ids in the deliverable either
        assert not re.search(r"session \d+ audit|audit A\d", json.dumps(_a1row(a1, rid))), rid


def test_concession_issue_op_and_question_present_the_precedence_as_pending(real, issues, a1):
    iss = real["curated_issues"]["I-CONCESSION"]
    for k in ("text", "a3", "short"):
        assert not _ASSERTS_PRECEDENCE.search(_own(iss.get(k))), (k, iss.get(k))
    assert "no decision recorded" in iss["text"] and "VOL-V 3.1" in iss["text"] and "Effective Date" in iss["text"]
    lab = next(i for i in issues if i["id"] == "I-CONCESSION")
    assert lab["text"].startswith(H.HUMAN_DECISION_PENDING) and lab["short"].startswith(H.HUMAN_DECISION_PENDING)
    sheet = next(x for x in a1["sheets"]["Issues"]["rows"] if x["id"] == "I-CONCESSION")
    assert sheet["text"].startswith(H.HUMAN_DECISION_PENDING)
    q7 = _op(real, "ADD-02/Q7")
    assert q7.effect != "confirms"                                  # Q7 confirms nothing about which clause governs
    assert "The Authority notes the question." in q7.note and not _ASSERTS_PRECEDENCE.search(_own(q7.note)), q7.note
    assert "follow-up only" not in (q7.issue or "")
    cq = _cq(real, "CQ-CONCESSION-TERM")
    for k in ("gap", "already_settled", "interim_handling", "practical_impact"):
        assert not _ASSERTS_PRECEDENCE.search(_own(cq.get(k))), (k, cq.get(k))
    # session 13 (F2; audit R2-4, deliberate): the 'pending, no decision recorded' label is the register writer's rule
    # (clarify.presented: every question linked to a pending issue), no longer typed into this one entry by hand
    from tenderpack import clarify
    shown = next(c for c in clarify.presented(real["clarifications"], real.get("decisions"), real.get("pending_issues"),
                                              real["curated_issues"]) if c["id"] == "CQ-CONCESSION-TERM")
    assert "no decision recorded" in shown["interim_handling"] and "Legal" in shown["interim_handling"]


def test_the_a3_concession_line_carries_the_pending_label(real, issues):
    a3 = stage2.a3(real, issues, None)
    items = [i for g in a3["groups"]["groups"] for i in g["items"] if i["id"] == "I-CONCESSION"]
    assert items and all(H.HUMAN_DECISION_PENDING in (i.get("short") or "") for i in items), items


# ---------------------------------------------------------------------------------------------- checked, no question (R-1, A4-2)

def test_checked_no_question_holds_no_judgment_and_pending_readings_are_labelled(real, tmp_path):
    reg = real["clarifications"]
    bad = [(c["topic"], H.triggers(_own(c["topic"] + " " + c["finding"])))
           for c in reg.get("checked_no_question") or [] if H.triggers(_own(c["topic"] + " " + c["finding"]))]
    assert not bad, bad                       # no decision can be recorded on these entries: none may assert one
    assert clarify.judgment_findings(reg) == []
    pend = {c["topic"]: c for c in reg.get("pending_decision") or []}
    for t in ("concession term (which clause governs)", "Form 4-G 'No' answers", "page limit: ADD-01 Q2 after ADD-02 2.1"):
        assert t in pend and pend[t]["decision_owner"].strip(), t
    assert clarify.check(reg, real["units"], set(real["curated_issues"])) == []
    md = clarify.markdown(reg)
    sec = md.split("## Proposed readings")[1].split("\n## ")[0]
    assert H.HUMAN_DECISION_PENDING in sec and "concession term (which clause governs)" in sec
    closed = md.split("## Checked, no question")[1].split("\n## ")[0]
    assert "concession" not in closed and "Form 4-G" not in closed


# ---------------------------------------------------------------------------------------------- Q11 (A1-2, A2-6)

def test_q11_one_wording_settles_the_question_asked_and_labels_the_engineering_reading(real):
    iss = real["curated_issues"]["I-FLOWS"]
    q11 = _op(real, "ADD-02/Q11")
    note42 = _row(real, "VOL-II-4.2-01").interpretations[-1].note
    dwf = _cq(real, "CQ-DWF-STORM-FLOW")["already_settled"]
    assert "engineering reading" in dwf and "not re-asked" in dwf, dwf
    for t in (iss["text"], iss["short"], q11.note, note42, dwf):
        assert "Bidders shall design to the figures stated in Volume II" in t or "design to the Volume II figures" in t, t
        assert "dry weather flow" in t.lower(), t
        own = _own(t)
        assert "not contradictory" not in own or "engineering reading" in own.lower(), t
        assert not re.search(r"\bsettled by ADD-02 Q11\b|\bstand and are\b", own), t


# ---------------------------------------------------------------------------------------------- quotes (A1-3)

def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "")
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip().lower()


_REF = re.compile(r"\b(VOL-[IV]+|ADD-\d+) \S+ p(\d+)")
_CELL = re.compile(r"^([A-Z][^:|]{0,40}): (.+)$")


def test_every_a1_quote_is_verbatim_on_one_page_it_cites(real, a1):
    pages: dict[tuple, list[str]] = {}
    kinds = {}
    for u in real["units"]:
        kinds[u["unit_id"]] = u.get("kind")
        for p in u.get("pages") or []:
            pages.setdefault((u["doc"], p), []).append(u.get("text") or "")
    text = {k: _norm(" ".join(v)) for k, v in pages.items()}
    bad = []
    for x in a1["rows"]:
        q = _norm(x["quote"])
        if not q:
            continue
        refs = [(m.group(1), int(m.group(2))) for m in _REF.finditer(x["source"])]
        ok = any(q in text.get(k, "") for k in refs)
        m = _CELL.match(x["quote"])
        cells = [":".join(u.split(" ")[:2]) for u in x["units"]]
        if not ok and m and any(kinds.get(u) in ("table_row", "form_field") for u in cells):
            # a table or form cell rendered 'Label: value' (the build's text form of a cell): the value is verbatim,
            # as a whole token, on a cited page
            v = re.escape(_norm(m.group(2)))
            ok = any(re.search(r"(?<![\w.,])" + v + r"(?![\w.,])", text.get(k, "")) for k in refs)
        if not ok:
            bad.append((x["id"], x["source"], x["quote"]))
    assert not bad, bad


# ---------------------------------------------------------------------------------------------- ADD-02 5.2 (A1-4)

def test_add02_5_2_is_not_a_gate_without_a_stated_consequence(real, a1):
    row = _row(real, "ADD-02-5.2-01")
    rec = _a1row(a1, "ADD-02-5.2-01")
    assert rec["consequence"] == "none stated in the documents"
    assert row.assessment != "pass_fail", row.assessment            # the notice: pass_fail is a stated consequence or an
    assert row.assessment == _row(real, "VOL-II-3.1-01").assessment  # 11.1 document; the same as the design it governs
    assert "Process design, treatment performance and compliance with Volume II" in row.confidence_reason


# ---------------------------------------------------------------------------------------------- text as issued (A1-5)

def test_text_as_issued_of_a_row_first_issued_by_an_addendum_is_the_addendums_text(a1, real):
    born = [x for x in a1["rows"] if x["status:BASE"] == "NOT ISSUED"]
    assert len(born) >= 10
    for x in born:
        assert "(not in the volumes as issued)" not in x["original_text"], (x["id"], x["original_text"])
        assert x["original_text"].strip(), x["id"]
    r72 = _a1row(a1, "ADD-02-7.2-01")["original_text"]
    assert r72.startswith("[ADD-02 7.2 p3; issued by ADD-02] Form 4-G shall be completed"), r72
    assert "[ADD-01 3.1 p1" in _a1row(a1, "ADD-01-3.1-01")["original_text"] or \
        _a1row(a1, "ADD-01-3.1-01")["original_text"].startswith("The attendance record")


# ---------------------------------------------------------------------------------------------- provenance (A1-6)

def test_no_a1_cell_cites_an_internal_audit_id(a1):
    bad = [(x["id"], k) for x in a1["rows"] for k, v in x.items()
           if re.search(r"session 1\d|audit A\d", json.dumps(v, ensure_ascii=False), re.I)]
    assert not bad, bad


# ---------------------------------------------------------------------------------------------- earlier answers (A2-4)

def test_earlier_answers_q1_listed_and_express_reversals_said_plainly(a2):
    ans = {x["answer"]: x for x in a2["answers"] if x["stage"] == "ADD-02"}
    assert "ADD-01:Q1" in ans, sorted(ans)
    q1 = ans["ADD-01:Q1"]
    assert q1["status"] == "REVIEW (not automatically revoked)" and "ADD-02/5.1" in q1["reread"], q1
    a41, a42 = ans["ADD-01/4.1"], ans["ADD-01/4.2"]
    assert a41["status"].startswith("REVERSED by ADD-02 9.1") and "a person decides" not in a41["reread"], a41
    assert a42["status"].startswith("REVOKED by ADD-02 9.2") and "a person decides" not in a42["reread"], a42
    assert "ceases to have effect" in a42["reread"] and "is reinstated" in a41["reread"]
    assert "a person decides" in ans["ADD-01:Q2"]["reread"]          # the pack is silent on Q2: a person decides


# ---------------------------------------------------------------------------------------------- dates (A2-5)

def test_a2_shows_both_readings_of_an_ambiguous_date(a2):
    rows = [x for x in a2["rows_moved"] if x["row"] in ("ADD-01-3.1-01", "VOL-I-8.5-01")]
    after = " ".join(x["after"] for x in rows)
    assert "ATTENDANCE-NOTICE 2026-10-14 (2026-10-15 if" in after, after
    lb = [x for x in a2["rows_moved"] if "REFERENCE-LOOKBACK" in x["after"]]
    assert lb and all("2016-11-26 if" in x["after"] for x in lb), [x["after"] for x in lb]


# ---------------------------------------------------------------------------------------------- indirect effects (A2-7)

def test_indirect_effects_are_curated(real, a1):
    rels = {e["id"]: e for e in real["relationships"]}
    lcc = [e for e in rels.values() if "VOL-I:8.6" in (e.get("from") or []) and "VOL-I:9.1(i)" in (e.get("to") or [])]
    assert lcc and lcc[0]["status"] == "confirmed", lcc
    f4e = [e for e in rels.values() if "VOL-V:36.2" in (e.get("from") or []) and "VOL-IV-F4E-01" in (e.get("to") or [])]
    assert f4e and f4e[0]["status"] == "confirmed", f4e
    fm = [e for e in rels.values() if "VOL-V:36.2" in (e.get("from") or []) and "VOL-I-10.3-01" in (e.get("to") or [])]
    assert fm and fm[0]["status"] in ("proposed", "possible") and fm[0].get("basis"), fm
    assert "VOL-I:9.1(i)" in _row(real, "VOL-I-9.1-01").units                       # the reached unit is the row's
    imp = (real.get("relationship_impact") or {})
    for st in ("ADD-01", "ADD-02"):                                                  # the path, both ways, in A2
        assert any(x["target"] == "VOL-I:9.1(i)" and "REL-LCC-ENVELOPE-A" in x["path"]
                   for x in (imp.get(st) or {}).get("records", [])), st
    assert "Index of Forms" in (_row(real, "ADD-02-7.2-01").interpretations[-1].note or "")
    n91 = _row(real, "VOL-I-9.1-01").interpretations[-1].note
    assert "Local Content Certificate" in n91 and "ADD-01 4.1" in n91 and "ADD-02 9.1" in n91, n91
