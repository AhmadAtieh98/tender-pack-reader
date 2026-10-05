"""Session 11, D1: a requirement through four consecutive addenda (synthetic units in the pack's style, as
tests/test_session09_removed.py does; the engine, the register and the outputs' own functions on them).

    ADD-01  introduces the obligation (a new clause, or a sentence added to a clause that existed from BASE), with a
            stated consequence; the row says so: `introduced: {stage: ADD-01, by: <op>, evidence: {unit, page, words}}`
    ADD-02  changes its words / value
    ADD-03  takes it away (the clause deleted; or the sentence struck from a clause that stays in force: REMOVED)
    ADD-04  puts it back (the clause reinstated in an amended form; or the sentence added again)

For each stage: the row's status (NOT IN FORCE -> NEW -> AMENDED -> DELETED/REMOVED -> REINSTATED-AMENDED/AMENDED),
its quote verbatim in the effective text of that stage, the removal's evidence (the words in the unit immediately
before the op, gone immediately after it), the reinstatement's (the op, its provision and the words it puts back), its
consequence and whether A3 lists it, and the A5 activity its evidence item needs (present at ADD-01, ADD-02 and
ADD-04; absent at ADD-03). Nothing of an earlier stage is rewritten by a later one: the ADD-02 state, asked for, still
shows the ADD-02 words, identical to a run that stops at ADD-02."""
from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from tenderpack import stage2
from tenderpack.amend import Engine, OpFile
from tenderpack.dates import calendar_from_config
from tenderpack.dispositions import check_sweeps
from tenderpack.evidence import EvidenceItem
from tenderpack.register import RowFile, compute_pins
from tenderpack.schedule import in_force

ROOT = Path(__file__).resolve().parents[1]

CYBER3 = ("Each Bidder shall submit in Envelope A a Cybersecurity Undertaking covering a period of three (3) years. "
          "A Proposal without the Cybersecurity Undertaking shall be rejected.")
CYBER4 = CYBER3.replace("three (3) years", "four (4) years")
NOTARY = "Each signature shall be witnessed by a notary public."
NOTARY2 = "Each signature shall be witnessed by a notary public or a consulate of the Kingdom."
SIGN = "Each document in Envelope A shall be signed by the Bidder's authorised signatory."
ISSUED = {"ADD-01": "Issued 1 October 2026", "ADD-02": "Issued 8 October 2026", "ADD-03": "Issued 15 October 2026",
          "ADD-04": "Issued 22 October 2026"}


def _units() -> list[dict]:
    u = lambda uid, doc, kind, text, page=1: {"unit_id": uid, "doc": doc, "kind": kind, "text": text, "pages": [page]}  # noqa: E731
    out = [u("VOL-I:6.1", "VOL-I", "clause", "Proposals shall be received by the Authority not later than 14:00 hours Riyadh "
                                             "time on Thursday 26 November 2026 at the address given in Appendix 3.", 3),
           u("VOL-I:9.1", "VOL-I", "clause", "Envelope A shall contain the documents listed in this Section.", 5),
           u("VOL-I:9.2", "VOL-I", "clause", SIGN, 5),
           u("VOL-I:9.4", "VOL-I", "clause", "An unsigned or improperly executed document shall render the Proposal "
                                             "non-responsive.", 5)]
    provisions = {
        "ADD-01": {"2.1": f"The following new Clause 9.3 is inserted in Volume I after Clause 9.2: ‘{CYBER3}’",
                   "2.2": f"At the end of Volume I Clause 9.2 the following is added: ‘{NOTARY}’"},
        "ADD-02": {"2.1": "In Volume I Clause 9.3, ‘three (3) years’ is deleted and ‘five (5) years’ is substituted.",
                   "2.2": "In Volume I Clause 9.2, ‘a notary public’ is deleted and ‘a notary public or a consulate of the "
                          "Kingdom’ is substituted."},
        "ADD-03": {"2.1": "Volume I Clause 9.3 is deleted.",
                   "2.2": f"In Volume I Clause 9.2, the sentence ‘{NOTARY2}’ is deleted."},
        "ADD-04": {"2.1": f"Volume I Clause 9.3, deleted by Addendum No. 3, is reinstated as follows: ‘{CYBER4}’",
                   "2.2": f"At the end of Volume I Clause 9.2 the following is added: ‘{NOTARY}’"},
    }
    for add, provs in provisions.items():
        out.append(u(f"{add}:cover/para1", add, "paragraph", ISSUED[add]))
        out += [u(f"{add}:{k}", add, "clause", v) for k, v in provs.items()]
    return out


NEW_CLAUSE = "VOL-I:9.2+ADD-01"                  # the engine names the inserted clause after its anchor and addendum


def _opfiles() -> list[OpFile]:
    ops = {
        "ADD-01": [{"type": "insert_unit", "anchor": "VOL-I:9.2", "new_text": CYBER3},
                   {"type": "append_text", "target": "VOL-I:9.2", "new": NOTARY}],
        "ADD-02": [{"type": "replace_text", "target": NEW_CLAUSE, "old": "three (3) years", "new": "five (5) years"},
                   {"type": "replace_text", "target": "VOL-I:9.2", "old": "a notary public",
                    "new": "a notary public or a consulate of the Kingdom"}],
        "ADD-03": [{"type": "set_status", "target": NEW_CLAUSE, "status": "deleted"},
                   {"type": "replace_text", "target": "VOL-I:9.2", "old": " " + NOTARY2, "new": "",
                    "old_resolved": "matched_in_target"}],
        "ADD-04": [{"type": "set_status", "target": NEW_CLAUSE, "status": "reinstated", "new_text": CYBER4},
                   {"type": "append_text", "target": "VOL-I:9.2", "new": NOTARY}],
    }
    out = []
    for add, lst in ops.items():
        out.append(OpFile.model_validate({
            "addendum": add, "issued_from": f"{add}:cover/para1", "prepared_by": "test", "method": "test",
            "ops": [{"id": f"{add}/2.{i + 1}", "provision": f"{add}:2.{i + 1}", **o} for i, o in enumerate(lst)],
            "dispositions": [{"provision": f"{add}:cover/para1", "disposition": "no_effect", "reason": "issue date"}]}))
    return out


CONS_REJ = {"class": "rejection", "unit": NEW_CLAUSE, "quote": "A Proposal without the Cybersecurity Undertaking shall be rejected."}
CONS_NR = {"class": "non_responsive", "unit": "VOL-I:9.4", "quote": "shall render the Proposal non-responsive"}


def _rows() -> list[dict]:
    base = {"discipline": "Legal", "owner": "Legal counsel", "assessment": "pass_fail", "confidence": "high",
            "confidence_reason": "synthetic"}
    return [
        {**base, "id": "VOL-I-6.1-01", "group": "VOL-I:6.1", "scope": ["deadline"], "requirement": "Deliver by the PDD",
         "units": ["VOL-I:6.1"], "evidence": ["EV-DELIVERY"], "discipline": "Bid management",
         "date_rules": [{"rule_id": "PDD", "kind": "anchor", "purpose": "deadline", "anchor": "PDD", "source_unit": "VOL-I:6.1",
                         "text": "not later than 14:00 hours Riyadh time on <date>"}],
         "interpretations": [{"stage": "BASE", "quote": "not later than 14:00 hours Riyadh time on Thursday 26 November 2026"}]},
        {**base, "id": "VOL-I-9.2-01", "group": "VOL-I:9.2", "scope": ["envelope_A"], "requirement": "Sign every document",
         "units": ["VOL-I:9.2"], "evidence": ["EV-SIGNING"],
         "interpretations": [{"stage": "BASE", "quote": SIGN, "consequence": CONS_NR}]},
        # scenario 1: a new clause (inserted, changed, deleted, reinstated amended)
        {**base, "id": "ADD-01-2.1-01", "group": "ADD-01:2.1", "scope": ["envelope_A", "cyber", "new_in_addendum"],
         "requirement": "Submit a Cybersecurity Undertaking in Envelope A", "units": [NEW_CLAUSE, "ADD-01:2.1"],
         "evidence": ["EV-CYBER"],
         "introduced": {"stage": "ADD-01", "by": "ADD-01/2.1", "evidence": {
             "unit": "ADD-01:2.1", "page": 1, "words": "The following new Clause 9.3 is inserted in Volume I after Clause 9.2"}},
         "interpretations": [
             {"stage": "ADD-01", "quote": "a Cybersecurity Undertaking covering a period of three (3) years",
              "parameters": {"years": 3}, "consequence": CONS_REJ},
             {"stage": "ADD-02", "quote": "a Cybersecurity Undertaking covering a period of five (5) years",
              "parameters": {"years": 5}, "consequence": CONS_REJ},
             {"stage": "ADD-04", "quote": "a Cybersecurity Undertaking covering a period of four (4) years",
              "parameters": {"years": 4}, "consequence": CONS_REJ, "note": "reinstated amended by ADD-04 2.1"}]},
        # scenario 2: a sentence added to a clause in force since BASE (the blind-04 shape), changed, struck, added again
        {**base, "id": "ADD-01-2.2-01", "group": "ADD-01:2.2", "scope": ["envelope_A", "signing", "new_in_addendum"],
         "requirement": "Have each signature witnessed", "units": ["VOL-I:9.2"], "evidence": ["EV-NOTARY"],
         "introduced": {"stage": "ADD-01", "by": "ADD-01/2.2", "evidence": {"unit": "ADD-01:2.2", "page": 1, "words": NOTARY}},
         "interpretations": [
             {"stage": "ADD-01", "quote": NOTARY, "consequence": CONS_NR},
             {"stage": "ADD-02", "quote": NOTARY2, "consequence": CONS_NR},
             {"stage": "ADD-03", "quote": NOTARY2, "removed": {"by": "ADD-03/2.2", "note": "the sentence is struck"}},
             {"stage": "ADD-04", "quote": NOTARY, "consequence": CONS_NR, "note": "added again by ADD-04 2.2"}]},
    ]


def _templates() -> dict:
    act = lambda i, n, d, s: {"id": i, "name": n, "owner": "Legal", "discipline": "Legal", "resource": "legal_counsel",  # noqa: E731
                              "issuer": "Bidder", "duration": d, "predecessors": [], "successors": s}
    return {"EV-DELIVERY": [dict(act("deliver", "Deliver the Proposal", "delivery", []), finish={"deadline_of": "PDD"},
                                 discipline="Document control", resource="document_controller")],
            "EV-SIGNING": [act("sign-envelope-a", "Sign the documents of Envelope A", "s11_signing", ["deliver"])],
            "EV-CYBER": [act("cyber-undertaking", "Prepare and sign the Cybersecurity Undertaking", "s11_cyber", ["deliver"])],
            "EV-NOTARY": [act("witness-signatures", "Have the signatures witnessed", "s11_witness", ["deliver"])]}


def _evidence_items() -> dict:
    return {k: EvidenceItem(name=k, envelope="A", issuer="Bidder", source="synthetic")
            for k in ("EV-DELIVERY", "EV-SIGNING", "EV-CYBER", "EV-NOTARY")}


def _run(tmp: Path, n: int = 4) -> dict:
    """stage2.evaluate on the synthetic state with the first `n` addenda (the inputs stage2.run would load)."""
    a = yaml.safe_load((ROOT / "config/assumptions.yaml").read_text(encoding="utf-8"))
    a["lead_times"].update({k: {"value": 2, "basis": "PROVISIONAL ASSUMPTION: synthetic", "owner": "Legal"}
                            for k in ("s11_signing", "s11_cyber", "s11_witness")})
    units = _units()
    rowfile = RowFile.model_validate({"prepared_by": "test", "method": "test", "rows": _rows(),
                                      "anchors": {"PDD": {"name": "Proposal Due Date", "defined_in": "VOL-I:6.1"}}})
    compute_pins(rowfile, Engine(units, _opfiles()[:n]).run())   # each reading pinned where it is made (`tenderpack pin`)
    r = {"cfg": {"pack_id": "S11-STAGES"}, "root": tmp, "units": units, "problems": [], "assumptions": a,
         "cal": calendar_from_config(a.get("calendar")), "policy": a["planning"].get("counting_policy", "conservative"),
         "templates": _templates(), "curated_issues": {}, "rowfile": rowfile, "opfiles": _opfiles()[:n], "drafted": {},
         "dispositions": {}, "disposition_problems": [], "evidence_items": _evidence_items(), "evidence_problems": [],
         "load_problems": [], "sweeps": check_sweeps(units, {}, rowfile.rows), "decisions_file": tmp / "decisions.yaml",
         "decisions": [], "evidence_dir": tmp, "clarifications": {}, "relationships": [],
         "relationships_path": tmp / "relationships.yaml"}
    return stage2.evaluate(r)


@pytest.fixture(scope="module")
def run(tmp_path_factory):
    r = _run(tmp_path_factory.mktemp("s11-stages"))
    assert [s.stage for s in r["stages"]] == ["BASE", "ADD-01", "ADD-02", "ADD-03", "ADD-04"]
    assert all(s.status == "APPLIED" for s in r["stages"][1:]), [(s.stage, s.status, [x.checks for x in s.ops if not x.valid])
                                                                 for s in r["stages"]]
    return r


def _ev(r, rid):
    return next(e for e in r["evals"] if e["row"].id == rid)["stages"]


STAGES = ["BASE", "ADD-01", "ADD-02", "ADD-03", "ADD-04"]


@pytest.mark.parametrize("rid, statuses", [
    ("ADD-01-2.1-01", ["NOT IN FORCE (introduced at ADD-01 by ADD-01/2.1)", "NEW (introduced by ADD-01/2.1)",
                       "AMENDED (ADD-02/2.1)", "DELETED (ADD-03/2.1)", "REINSTATED-AMENDED (ADD-04/2.1)"]),
    ("ADD-01-2.2-01", ["NOT IN FORCE (introduced at ADD-01 by ADD-01/2.2)", "NEW (introduced by ADD-01/2.2)",
                       "AMENDED (ADD-02/2.2)", "REMOVED (ADD-03/2.2)", "AMENDED (ADD-04/2.2)"]),
])
def test_the_history_of_a_requirement_through_four_addenda(run, rid, statuses):
    ev = _ev(run, rid)
    assert [ev[s]["status"] for s in STAGES] == statuses
    assert [in_force(ev[s]["status"]) for s in STAGES] == [False, True, True, False, True]
    for s in STAGES:                                        # nothing to fix at any stage: no C16, never STALE
        assert ev[s]["problems"] == [] and ev[s]["stale"] == [], (s, ev[s]["problems"], ev[s]["stale"])
    assert ev["BASE"]["introduction"]["explicit"] and ev["BASE"]["interpretation"] is None
    # the BASE row of the clause that existed all along is untouched by the obligation added to it
    assert [_ev(run, "VOL-I-9.2-01")[s]["status"].split(" ")[0] for s in STAGES] == \
        ["ACTIVE", "AMENDED", "AMENDED", "AMENDED", "AMENDED"]


def test_the_evidence_at_each_stage_is_verbatim_there(run):
    ev = _ev(run, "ADD-01-2.1-01")
    words = {"ADD-01": "three (3) years", "ADD-02": "five (5) years", "ADD-04": "four (4) years"}
    for s, w in words.items():
        assert w in ev[s]["text"] and w in ev[s]["interpretation"]["quote"] and ev[s]["interpretation"]["stage"] == s
        assert ev[s]["interpretation"]["consequence"]["quote"] in ev[s]["text"]       # the consequence stated there
    assert ev["ADD-03"]["text"] == CYBER3.replace("three (3)", "five (5)") and ev["ADD-03"]["active"] is False
    # the reinstatement's evidence: its op, the provision that prints the words, the words it puts back
    reg = run["register"]
    x = reg.op_result["ADD-04/2.1"]
    assert x.applied and x.details["before"] == ev["ADD-03"]["text"] and CYBER4 in run["stages"][4].state["ADD-04:2.1"].text
    assert any(c.startswith("ADD-04/2.1 [ADD-04") for c in ev["ADD-04"]["chain"])
    # the removal's evidence: the row's words are in VOL-I 9.2 immediately before the op and gone immediately after
    ev2 = _ev(run, "ADD-01-2.2-01")
    before, after = reg._text_around("ADD-03/2.2", "VOL-I:9.2", False)
    assert NOTARY2 in before and NOTARY2 not in after and SIGN in after
    assert ev2["ADD-03"]["interpretation"]["removed"]["by"] == "ADD-03/2.2" and ev2["ADD-03"]["problems"] == []
    assert ev2["ADD-04"]["text"] == f"{SIGN} {NOTARY}"
    for s, q in (("ADD-01", NOTARY), ("ADD-02", NOTARY2), ("ADD-04", NOTARY)):
        assert q in ev2[s]["text"] and ev2[s]["interpretation"]["consequence"]["class"] == "non_responsive"


def test_a1_shows_every_stage_and_a3_lists_the_row_only_while_it_is_in_force(run):
    a1 = {x["id"]: x for x in stage2.a1_table(run, [])["rows"]}
    row = a1["ADD-01-2.1-01"]
    assert row["status:BASE"].startswith("NOT IN FORCE") and row["source:BASE"] == ""
    assert row["status:ADD-03"] == "DELETED (ADD-03/2.1)" and row["status:ADD-04"].startswith("REINSTATED-AMENDED")
    progs = stage2.a5_all(run)
    for s, listed in (("ADD-01", True), ("ADD-02", True), ("ADD-03", False), ("ADD-04", True)):
        r = dict(run, validated=next(x for x in run["stages"] if x.stage == s))
        a3 = stage2.a3(r, stage2.collect_issues(r, progs[s]), progs[s])
        for rid in ("ADD-01-2.1-01", "ADD-01-2.2-01"):
            assert (rid in a3["explicit_ids"]) is listed, (s, rid, a3["explicit_ids"])


def test_a5_plans_the_activity_while_the_requirement_is_in_force(run):
    progs = stage2.a5_all(run)
    for s, planned in (("ADD-01", True), ("ADD-02", True), ("ADD-03", False), ("ADD-04", True)):
        acts = {a["id"]: a for a in progs[s]["activities"]}
        for aid, rid in (("cyber-undertaking", "ADD-01-2.1-01"), ("witness-signatures", "ADD-01-2.2-01")):
            assert (aid in acts) is planned, (s, aid, sorted(acts))
            if planned:
                assert rid in acts[aid]["req_ids"]
        assert "sign-envelope-a" in acts                       # the BASE obligation is planned at every stage
        assert not [p for p in progs[s].get("problems") or [] if p.startswith(("C44", "C45"))], progs[s]["problems"]


def test_a_later_addendum_rewrites_nothing_of_an_earlier_stage(run, tmp_path):
    early = _run(tmp_path, n=2)                                 # the same state, stopped at ADD-02
    for rid in ("ADD-01-2.1-01", "ADD-01-2.2-01", "VOL-I-9.2-01"):
        a, b = _ev(early, rid), _ev(run, rid)
        for s in ("BASE", "ADD-01", "ADD-02"):
            for k in ("status", "active", "text", "interpretation", "problems", "dates", "consequence_source"):
                assert a[s][k] == b[s][k], (rid, s, k)
    assert "five (5) years" in _ev(run, "ADD-01-2.1-01")["ADD-02"]["text"]


def test_without_the_introduction_the_sentence_row_is_in_force_from_base_and_reported(tmp_path):
    """The same rows without `introduced`: the clause row is derived from its inserted unit (NOT ISSUED before ADD-01,
    unchanged behaviour); the row on a BASE clause is in force from BASE with no reading there (C16, as in blind-04)."""
    import tenderpack.register as REG
    rows = copy.deepcopy(_rows())
    for x in rows:
        x.pop("introduced", None)
    rf = RowFile.model_validate({"prepared_by": "t", "method": "t", "rows": rows,
                                 "anchors": {"PDD": {"name": "Proposal Due Date", "defined_in": "VOL-I:6.1"}}})
    from tenderpack.amend import Engine
    stages = Engine(_units(), _opfiles()).run()
    reg = REG.Register(rf, stages)
    e1 = {s.stage: reg.evaluate(rf.rows[2], s) for s in stages}
    e2 = {s.stage: reg.evaluate(rf.rows[3], s) for s in stages}
    assert e1["BASE"]["status"] == "NOT ISSUED" and e1["ADD-01"]["status"] == "NEW"
    assert not e1["BASE"]["introduction"]["explicit"] and "derived from the primary unit" in e1["BASE"]["introduction"]["basis"]
    assert e2["BASE"]["status"] == "ACTIVE" and e2["BASE"]["problems"] == ["no interpretation made at or before BASE"]
    assert e2["BASE"]["introduction"]["basis"] == "derived from the primary unit VOL-I:9.2 (issued in BASE)"


def test_an_introduction_by_a_held_conditional_op_says_so():
    """An `introduced` claim whose op is a conditional amendment held for want of a recorded trigger is reported as
    that, not as a rejected or invalid op."""
    from tenderpack.register import Register
    rf = RowFile.model_validate({"prepared_by": "t", "method": "t", "rows": _rows(),
                                 "anchors": {"PDD": {"name": "Proposal Due Date", "defined_in": "VOL-I:6.1"}}})
    reg = Register(rf, Engine(_units(), _opfiles()).run())
    reg.op_result["ADD-01/2.2"].pending = True                 # as the engine leaves a conditional op with no trigger fact
    probs = reg._introduction_problems(rf.rows[3], rf.rows[3].introduced)
    assert any("conditional amendment held at ADD-01" in p for p in probs), probs
    assert not any("rejection" in p or "invalid" in p for p in probs), probs
