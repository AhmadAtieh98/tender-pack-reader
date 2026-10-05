"""Session 12, part 1 (the owner's message): legal and commercial judgments stay with people (the brief's section 6).

Reproduced first against the committed code (6053493):
  a  an issue claiming that all concession-term conflicts are resolved became `evidence_verified` because it quoted
     ADD-02 Q7 verbatim: valid evidence validated the conclusion.
  b  an existing clarification entry (CQ-CONCESSION-TERM, CQ-BOND-FC-COVERAGE) could become "answered by addendum" or
     "withdrawn (not sent)" through a proposal: the draft-only rule applied to new ids only, promotion wrote the status
     into the candidate's register, and A5 (programme.gate_questions) then treated the question as closed.
  c  an issue proposal cannot close an existing issue (no status or resolution is ever applied).
  d  the rendered register, the candidate A3 and the run's review packet say HUMAN DECISION PENDING for every
     human-owned proposal and never "answered"/"withdrawn" without a person's recorded decision.
  e  deterministic facts stay usable: an evidence item and a substitution op stay `evidence_verified` and promotable.
  f  the analysis phase: an annotation that `confirms` a precedence answer (or whose note declares a conflict resolved)
     is `interpretation_pending`, never `evidence_verified`.
The workspace is the real pack plus page 1 of blind-02's Addendum No. 3 in a disposable folder (the session 11 D1
fixtures, reused); the cassette is the hand-written session 11 recording with items added here. Nothing is written under
the repository and no decision file is created except inside tmp, by the test acting as the person who runs `accept`."""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path

import pytest
import yaml

from test_session11_downstream import CASSETTE, _start, _stopped, _yaml, area, prev_build  # noqa: F401 (fixtures)
from tenderpack import clarify, human_owned as H, programme
from tenderpack.ai import controller
from tenderpack.ai import downstream as DS
from tenderpack.ai import workflow as W
from tenderpack.ai.contract import DownstreamItem, DownstreamSet, EvidenceRef, ProposalSet

Q7_WORDS = "The order of precedence at Volume I Clause 3.2 applies."
Q7 = EvidenceRef(doc="ADD-02", unit_id="ADD-02:Q7", page=2, kind="span", words=Q7_WORDS)
Q7_ANSWER = {"unit": "ADD-02:Q7", "page": 2, "words": Q7_WORDS}
RESOLVED_ISSUE = {"id": "I-S12-CONCESSION-RESOLVED", "owner": "Legal", "theme": "contract",
                  "text": "All concession-term conflicts are resolved: ADD-02 Q7 applies the VOL-I 3.2 order of precedence, "
                          "so Volume I prevails and the concession runs 25 years from PCOD.",
                  "short": "concession term resolved by ADD-02 Q7", "show_in_a3": True}


def _set(ws, items) -> DownstreamSet:
    st = ws.identity()
    return DownstreamSet(run_id="s12", created="2026-10-05T00:00:00Z", route="recorded", provider="test",
                         model_requested="test", addendum="ADD-03", state=st,
                         items=[DownstreamItem(state=st, **it) for it in items])


def _entry(ws, cid: str) -> dict:
    return copy.deepcopy(next(c for c in ws.r["clarifications"]["clarifications"] if c["id"] == cid))


@pytest.fixture(scope="module")
def ctx12(prev_build, area):  # noqa: F811
    return _stopped(prev_build, area, "s12-validate")


# ---------------------------------------------------------------------------------------------- a

def test_a_an_issue_declaring_the_concession_conflicts_resolved_is_not_evidence_verified(ctx12):
    ws = ctx12.ws
    ds = _set(ws, [{"id": "H1", "statement_type": "issue", "task": "t:x", "payload": RESOLVED_ISSUE, "evidence": [Q7]}])
    DS.validate(ws, ds, ctx12.promoted(fresh=True), {"t:x": "escalation"})
    it = ds.items[0]
    ev = [v for v in it.validation if v.check == "evidence" or "ADD-02:Q7" in v.detail]
    assert all(v.ok for v in ev) and ev, [v.detail for v in it.validation]            # the quotation is genuine
    assert it.verification_status != "evidence_verified", [v.detail for v in it.validation]
    assert it.verification_status == "interpretation_pending" and H.is_human_owned(it)
    rec = next(v for v in it.validation if v.check == H.CHECK)
    assert H.EVIDENCE_NOT_CONCLUSION in rec.detail and "resolved" in rec.detail and "prevail" in rec.detail


# ---------------------------------------------------------------------------------------------- b

@pytest.mark.parametrize("status, answer", [("answered by addendum", Q7_ANSWER), ("withdrawn (not sent)", None)])
def test_b_an_existing_clarification_entrys_status_never_changes_through_a_proposal(ctx12, status, answer):
    ws = ctx12.ws
    e = _entry(ws, "CQ-CONCESSION-TERM")
    assert e["response_status"] == "draft, not sent"
    e["response_status"] = status
    if answer:
        e["answer"] = dict(answer)
    ds = _set(ws, [{"id": "C1", "statement_type": "clarification_item", "task": "t:x", "payload": {"entry": e},
                    "evidence": [Q7]}])
    rep = DS.validate(ws, ds, ctx12.promoted(fresh=True), {"t:x": "clarification"})
    it = ds.items[0]
    got = it.payload["entry"]
    assert got["response_status"] == "draft, not sent", (got["response_status"], [v.detail for v in it.validation])
    assert "answer" not in got
    if answer:
        assert got["recorded_answer"] == answer                 # recorded, not declared resolving
    assert it.verification_status == "interpretation_pending" and H.is_human_owned(it), it.verification_status
    assert any(o.get("field") == "entry.response_status" and o.get("proposer_value") == status for o in rep["overwrites"])


def test_b_a_new_clarification_id_is_a_draft_and_its_answer_is_only_recorded(ctx12):
    ws = ctx12.ws
    e = _entry(ws, "CQ-CONCESSION-TERM")
    e.update(id="CQ-S12-NEW", response_status="answered by addendum", answer=dict(Q7_ANSWER))
    ds = _set(ws, [{"id": "C2", "statement_type": "clarification_item", "task": "t:x", "payload": {"entry": e},
                    "evidence": [Q7]}])
    DS.validate(ws, ds, ctx12.promoted(fresh=True), {"t:x": "clarification"})
    got = ds.items[0].payload["entry"]
    assert got["response_status"] == "draft, not sent" and "answer" not in got and got["recorded_answer"] == Q7_ANSWER
    # validated again (the workflow re-validates the rewritten set before promotion): the same status and record
    rep2 = DS.validate(ws, ds, ctx12.promoted(fresh=True), {"t:x": "clarification"})
    assert ds.items[0].verification_status == "interpretation_pending" and H.is_human_owned(ds.items[0])
    assert any(o.get("field") == "entry.response_status" and o.get("proposer_value") == "answered by addendum"
               for o in rep2["overwrites"])
    assert "not applied" in H.clarification_status(ds.items[0].payload["entry"], [])


def test_b_promotion_keeps_the_registers_status_and_a5_keeps_the_question_open(ctx12):
    ws = ctx12.ws
    e = _entry(ws, "CQ-CONCESSION-TERM")
    e.update(response_status="answered by addendum", answer=dict(Q7_ANSWER))
    ds = _set(ws, [{"id": "C3", "statement_type": "clarification_item", "task": "t:x", "payload": {"entry": e},
                    "evidence": [Q7]}])
    promoted = ctx12.promoted(fresh=True)
    DS.validate(ws, ds, promoted, {"t:x": "clarification"})
    cps, _ = ctx12.combined()
    snap_dir = Path(ctx12.cp.data["candidate"]["dir"])
    DS.promote(ws, ctx12.cp.data["candidate"], "s12-validate", cps, promoted, ds, "test origin", {})
    try:
        cand = _yaml(Path(ctx12.cp.data["candidate"]["dir"]) / "curation/clarifications/register.yaml")
        got = next(c for c in cand["clarifications"] if c["id"] == "CQ-CONCESSION-TERM")
        assert got["response_status"] == "draft, not sent" and "answer" not in got, got
        assert got["recorded_answer"] == Q7_ANSWER and got[H.MARKER] == "pending"
        units = ws.r["units"]
        assert clarify.check({"clarifications": [got]}, units, set(ws.r["curated_issues"])) == []
        shown = H.clarification_status(got, [])
        assert H.HUMAN_DECISION_PENDING in shown and "ADD-02:Q7 p2" in shown and "whether it resolves" in shown
        assert "CQ-CONCESSION-TERM" in programme.gate_questions({"clarifications": cand, "decisions": []})["I-CONCESSION"]
    finally:
        DS._snapshot(snap_dir, snap_dir / ".pre-promotion")      # the candidate as it was (other tests share it)
        ws.refresh()


def test_b_a5_counts_a_closing_status_only_with_a_persons_decision_bound_to_it():
    e = {"id": "CQ-X", "response_status": "answered by addendum", "answer": dict(Q7_ANSWER), "linked_issues": ["I-X"]}
    reg = {"clarifications": [e]}
    assert programme.gate_questions({"clarifications": reg, "decisions": []}) == {"I-X": ["CQ-X"]}
    assert H.HUMAN_DECISION_PENDING in H.clarification_status(e, [])
    assert "answered" not in H.clarification_status(e, []).lower().replace("an addendum answer", "")
    dec = [{"kind": "clarification", "item": "CQ-X", "decision": "accept", "reviewer": "Ahmad", "date": "2026-10-05",
            "fingerprint": H.entry_fingerprint("clarification", e)}]
    assert programme.gate_questions({"clarifications": reg, "decisions": dec}) == {}
    assert H.clarification_status(e, dec).startswith("answered by addendum (decision recorded: Ahmad")
    e2 = dict(e, answer={**Q7_ANSWER, "words": "The Authority does not consider further amendment necessary"})
    assert programme.gate_questions({"clarifications": {"clarifications": [e2]}, "decisions": dec}) == {"I-X": ["CQ-X"]}


# ---------------------------------------------------------------------------------------------- c

@pytest.mark.parametrize("payload", [
    {"id": "I-CONCESSION", "text": "Resolved by ADD-02 Q7.", "owner": "Legal", "theme": "contract"},
    {"id": "I-CONCESSION", "text": "x", "owner": "Legal", "theme": "contract", "status": "resolved"},
    {"id": "I-S12-NEW", "text": "x", "owner": "Legal", "theme": "contract", "resolution": "Volume I prevails"},
])
def test_c_an_issue_proposal_never_changes_an_existing_issue_or_carries_a_resolution(ctx12, payload):
    ws = ctx12.ws
    ds = _set(ws, [{"id": "I1", "statement_type": "issue", "task": "t:x", "payload": payload, "evidence": [Q7]}])
    DS.validate(ws, ds, ctx12.promoted(fresh=True), {"t:x": "escalation"})
    assert ds.items[0].verification_status == "invalid", [v.detail for v in ds.items[0].validation]


def test_c_an_issue_with_a_status_or_resolution_shows_pending_until_a_person_decides():
    iss = {"text": "x", "owner": "Legal", "status": "resolved", "resolution": "Volume I prevails"}
    assert H.issue_label("I-X", iss, []).startswith(H.HUMAN_DECISION_PENDING)
    dec = [{"kind": "issue", "item": "I-X", "decision": "accept", "reviewer": "Ahmad", "date": "2026-10-05",
            "fingerprint": H.entry_fingerprint("issue", iss)}]
    assert H.issue_label("I-X", iss, dec).startswith("RESOLVED (decision recorded: Ahmad")
    # an open curated issue: unchanged. Session 12, F5 (audit A3-5, deliberate): an issue owned by Legal or Commercial is
    # a person's judgment by its owner, so the open-issue case uses another owner
    assert H.issue_label("I-X", {"text": "x", "owner": "Bid manager"}, []) is None


def test_c_accept_records_a_persons_decision_on_a_clarification_entry(tmp_path):
    from tenderpack import review
    e = {"id": "CQ-X", "kind": "ambiguity", "volume": "Addendum No. 2", "clause": "Q7", "page": 2, "gap": "g",
         "practical_impact": "p", "proposed_question": "q", "interim_handling": "h", "decision_owner": "Legal",
         "response_status": "withdrawn (not sent)", "theme": "contract", "linked_issues": ["I-X"],
         "sources": [dict(Q7_ANSWER)]}
    units = [{"unit_id": "ADD-02:Q7", "doc": "ADD-02", "text": Q7_WORDS, "pages": [2]}]
    r = {"problems": [], "evals": [], "order": ["BASE"], "stages": [], "clarifications": {"clarifications": [e]},
         "curated_issues": {"I-X": {"text": "x", "owner": "Legal"}}, "units": units}
    r["reviews"] = review.compute(r, [])
    path = tmp_path / "decisions.yaml"
    assert review.decide(r, ["CQ-X"], "accept", "assistant", None, path)[0] == 2           # never the program
    bad = dict(r, clarifications={"clarifications": [{"id": "CQ-X", "response_status": "withdrawn (not sent)"}]})
    bad["reviews"] = review.compute(bad, [])
    assert review.decide(bad, ["CQ-X"], "accept", "Ahmad", None, path)[0] == 1 and not path.exists()  # checks first
    code, msgs = review.decide(r, ["CQ-X", "I-X"], "accept", "Ahmad", "withdrawn after the call", path,
                               today="2026-10-05")
    assert code == 0, msgs
    dec = review.load_decisions(path)
    assert {d["kind"] for d in dec} == {"clarification", "issue"}
    assert H.clarification_closed(e, dec) and not H.clarification_closed(dict(e, gap="changed"), dec)


# ---------------------------------------------------------------------------------------------- d, e: a whole run

def _cassette12(tmp: Path) -> Path:
    data = yaml.safe_load(CASSETTE.read_text(encoding="utf-8"))
    s = next(x for x in data["sessions"] if x["phase"] == "downstream")
    t = s["turns"][0]["response"]["text"]
    # D17 re-reads CQ-BOND-FC-COVERAGE: the proposer also declares it answered by ADD-02 Q13
    t, n = re.subn(r'("task": "clar:CQ-BOND-FC-COVERAGE".*?)"response_status": "draft, not sent"',
                   r'\1"response_status": "answered by addendum", "answer": {"unit": "ADD-02:Q13", "page": 2, '
                   r'"words": "The periods in Volume I Clause 12.2 are unchanged."}', t, count=1, flags=re.S)
    assert n == 1
    extra = {"id": "D90", "state": "${state}", "statement_type": "issue", "task": "clar:CQ-BOND-FC-COVERAGE",
             "payload": RESOLVED_ISSUE, "evidence": [Q7.model_dump()]}
    blob = json.dumps(extra, ensure_ascii=False).replace('"${state}"', "${state}")
    t = t.rstrip()
    assert t.endswith("]}")
    t = t[:-2] + ",\n  " + blob + "\n ]}"
    s["turns"][0]["response"]["text"] = t
    out = tmp / "s12-cassette.yaml"
    out.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return out


@pytest.fixture(scope="module")
def run12(prev_build, area, tmp_path_factory):  # noqa: F811
    cas = _cassette12(tmp_path_factory.mktemp("s12c"))
    res = _start(prev_build, area, "s12-full", cassette=cas)
    d = Path(res["run_dir"])
    return {"res": res, "dir": d, "cp": W.load("s12-full", area["staging"]).data,
            "items": {i["id"]: i for i in _yaml(d / "downstream/proposals.yaml")["downstream_set"]["items"]}}


def test_d_the_run_promotes_the_proposals_as_proposals_and_keeps_the_question_open(run12):
    items, d = run12["items"], run12["dir"]
    assert items["D90"]["verification_status"] == "interpretation_pending", items["D90"]["verification_status"]
    assert items["D17"]["verification_status"] == "interpretation_pending"
    reg = _yaml(d / "candidate/curation/clarifications/register.yaml")
    e = next(c for c in reg["clarifications"] if c["id"] == "CQ-BOND-FC-COVERAGE")
    assert e["response_status"] == "draft, not sent" and "answer" not in e and e["recorded_answer"]["unit"] == "ADD-02:Q13"
    iss = _yaml(d / "candidate/curation/register/issues/ADD-03-ai.yaml")["issues"]
    assert iss["I-S12-CONCESSION-RESOLVED"][H.MARKER] == "pending"
    cr = run12["cp"]["steps"]["check_register"]
    assert cr["exit_code"] == 0 and cr["findings"] == 0, cr.get("first")


def test_d_the_rendered_register_candidate_a3_and_review_packet_say_human_decision_pending(run12):
    d = run12["dir"]
    out = d / "candidate/out"
    md = (out / "a4/clarification_register.md").read_text(encoding="utf-8")
    block = md[md.index("### CQ-BOND-FC-COVERAGE"):]
    block = block[:block.index("\n### ") if "\n### " in block else len(block)]
    status = next(x for x in block.splitlines() if x.startswith("- **Response status:**"))
    assert H.HUMAN_DECISION_PENDING in status and "ADD-02:Q13 p2" in status and "whether it resolves" in status, status
    rows = json.loads((out / "a4/clarification_register.json").read_text(encoding="utf-8"))["rows"]
    st = next(r for r in rows if r["id"] == "CQ-BOND-FC-COVERAGE")["response_status"]
    assert st.startswith("draft, not sent") and H.HUMAN_DECISION_PENDING in st
    a3c = (out / "a3/a3_candidate.md").read_text(encoding="utf-8")
    line = next(x for x in a3c.splitlines() if "I-S12-CONCESSION-RESOLVED" in x and "resolved" in x.lower())
    assert H.HUMAN_DECISION_PENDING in line, line
    a3d = (out / "a3/a3_detail.html").read_text(encoding="utf-8")
    assert H.HUMAN_DECISION_PENDING in a3d[a3d.index('id="I-S12-CONCESSION-RESOLVED"'):][:1500]
    rv = (d / "review/index.md").read_text(encoding="utf-8")
    for iid in ("D90", "D17"):
        row = next(x for x in rv.splitlines() if x.startswith(f"| {iid} |"))
        assert H.HUMAN_DECISION_PENDING in row, row


def test_e_deterministic_facts_stay_evidence_verified_and_promotable(run12):
    items = run12["items"]
    ev = next(i for i in items.values() if i["statement_type"] == "evidence_item")
    assert ev["verification_status"] == "evidence_verified", [v["detail"] for v in ev["validation"]]
    assert "EV-DELIVERY-REGISTRATION" in run12["cp"]["steps"]["promotion"]["evidence_items"]
    staged = _yaml(run12["dir"] / "ai/s12-full-combined/proposals.yaml")
    sets = [v for v in (staged.values() if "items" not in staged else [staged]) if isinstance(v, dict) and "items" in v]
    ops = {i["id"]: i for s in sets for i in s["items"]}
    assert ops["ADD-03/3.2"]["verification_status"] == "evidence_verified", ops["ADD-03/3.2"]["validation"]


# ---------------------------------------------------------------------------------------------- f: the analysis phase

def test_f_an_annotation_confirming_a_precedence_answer_is_interpretation_pending(ctx12):
    ws = ctx12.ws
    cps, _ = ctx12.combined()
    ps = ProposalSet.model_validate(cps.model_dump(mode="json", by_alias=True))
    i = next(k for k, it in enumerate(ps.items) if it.id == "ADD-03/1.1")
    base = ps.items[i]
    ps.items[i] = base.model_copy(update={
        "statement_type": "amendment_op", "target": "VOL-I:3.2",
        "payload": {"id": "ADD-03/1.1", "provision": "ADD-03:1.1", "type": "annotate", "targets": ["VOL-I:3.2"],
                    "effect": "confirms", "note": "Under VOL-I 3.2 Volume I prevails over Volume V: the concession-term "
                                                  "conflict is resolved and no question remains"},
        "verification_status": "unverified", "validation": []})
    controller.validate_set(ws, ps, None, expected_addendum="ADD-03")
    it = ps.items[i]
    assert it.verification_status != "evidence_verified", [v.detail for v in it.validation]
    assert it.verification_status == "interpretation_pending" and H.is_human_owned(it)
    # a substitution op of the same set is a deterministic edit: untouched
    assert next(x for x in ps.items if x.id == "ADD-03/3.2").verification_status == "evidence_verified"
