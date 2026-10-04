"""Session 09: three C28 gaps that blind rehearsal 02 exposed (rehearsals/blind-02/COMPARISON.md, "Tool follow-ups").

1. "The Proposal Due Date is unchanged." was never read as a claim, while ADD-03 2.1 moves the time in VOL-I 6.1 from
   14:00 to 11:00 (VOL-I 2.6 defines the Proposal Due Date as the date and time stated in Clause 6.1).
2. "extends the Proposal validity period" was matched to ADD-03 3.2 (VOL-I 6.3, the Bid Bond validity, whose text says
   "the period of Proposal validity") instead of 3.1 (VOL-I 7.1), so the real omission (3.2) was reported inverted.
3. "removes the model audit opinion from the Proposal, re-letters Volume I Clause 9.1" was one claim, so 4.1 and 7.1
   were reported as omitted.

The regressions run on the blind-02 engine stages (the curated op files; no build is needed). They are NOT blind
evidence: they were written after the key was unsealed. The real-pack and blind-01 expectations stay in
tests/test_session07_summary.py.
"""
from __future__ import annotations

import copy
import json

import pytest

from tenderpack.amend import Engine, load_opfile
from tenderpack.register import load_rows
from tenderpack.summary import parse_claims, rule_index, summary_check, unchanged_claims
from tenderpack.util import ROOT

B = ROOT / "rehearsals/blind-02"


@pytest.fixture(scope="module")
def blind02(blind02_build):
    units = json.loads((blind02_build / "units.json").read_text(encoding="utf-8"))["units"]
    opfiles = [load_opfile(B / f"work/amendments/ADD-0{i}.yaml") for i in (1, 2, 3)]
    rf = load_rows(B / "work/register/rows.yaml")
    return {"units": units, "opfiles": opfiles, "stages": Engine(units, opfiles, set()).run(), "rf": rf}


def check(b, units=None, stages=None):
    units = units or b["units"]
    stages = stages or b["stages"]
    sc = summary_check(stages, units, b["rf"].anchors, rule_index(b["rf"].rows))
    return next(x for x in sc if x["addendum"] == "ADD-03")


def kinds(sc):
    return {(f["kind"], f.get("op") or f.get("provision")) for f in sc["findings"]}


def claim(sc, start):
    return next(c for c in sc["claims"] if c["text"].startswith(start))


def test_an_unchanged_claim_is_contradicted_by_the_time_change_in_the_defining_clause(blind02):
    sc = check(blind02)
    c = claim(sc, "The Proposal Due Date is unchanged")
    assert c["kind"] == "unchanged" and c["status"] == "contradicted"
    assert {"VOL-I:6.1", "VOL-I:2.6"} <= set(c["targets"])            # the anchor's clause and the volume's definition
    f = next(f for f in sc["findings"] if f.get("claim") == c["n"])
    assert f["kind"] == "contradicted" and f["op"] == "ADD-03/2.1"
    for words in ("'14:00 hours Riyadh time'", "'11:00 hours Riyadh time'", "VOL-I 6.1", "VOL-I 2.6",
                  "the date and time stated in Clause 6.1"):
        assert words in f["detail"], words
    # the confirmation that the DATE is not changed (an annotate op) is not what contradicts it
    assert not any(f.get("op") == "ADD-03/2.1(date)" and f.get("claim") == c["n"] for f in sc["findings"])
    # boilerplate names nothing that can change; the answer to Q21 is an answer, not a cover claim
    assert not any("All other terms" in x["text"] or "not extended" in x["text"] for x in sc["claims"])


def test_unchanged_claims_by_citation_are_supported_or_contradicted_by_the_ops_alone(blind02):
    units = copy.deepcopy(blind02["units"])
    cover = next(u for u in units if u["unit_id"] == "ADD-03:cover/para3")
    cover["text"] += (" Volume II Clause 4.4 is unchanged. Volume I Clause 8.7 remains unchanged. The Bid Bond amount is "
                      "not changed.")
    assert [x["object"] for x in unchanged_claims(cover["text"])] == [
        "The Proposal Due Date", "Volume II Clause 4.4", "Volume I Clause 8.7", "The Bid Bond amount"]
    stages = Engine(units, blind02["opfiles"], set()).run()
    sc = check(blind02, units, stages)
    assert claim(sc, "Volume II Clause 4.4 is unchanged")["status"] == "contradicted"        # 72 hours again (5.2)
    assert claim(sc, "Volume I Clause 8.7 remains unchanged")["status"] == "supported"       # Q17 only confirms it
    bond = claim(sc, "The Bid Bond amount is not changed")
    assert bond["status"] == "not checked" and not bond["targets"]           # no clause, anchor or row: left to a person
    assert any(f["kind"] == "unchecked" and f.get("claim") == bond["n"] for f in sc["findings"])
    f =[f for f in sc["findings"] if f.get("claim") == claim(sc, "Volume II Clause 4.4 is unchanged")["n"]]
    assert {x["op"] for x in f} == {"ADD-03/5.2(b)"} and "ninety-six (96) hours" in f[0]["detail"]


def test_the_validity_claim_names_the_proposal_validity_rule_and_the_bond_extension_is_omitted(blind02):
    sc = check(blind02)
    c = claim(sc, "extends the Proposal validity period")
    assert c["matched"] == ["ADD-03/3.1"] and c["status"] == "supported" and "VOL-I:7.1" in c["targets"]
    ks = kinds(sc)
    assert ("omitted", "ADD-03/3.2") in ks and ("omitted", "ADD-03/3.1") not in ks
    om = next(f for f in sc["findings"] if f["kind"] == "omitted" and f["op"] == "ADD-03/3.2")
    assert "VOL-I:6.3" in om["detail"] and "two hundred and ten (210) days" in om["detail"]


def test_without_the_register_rules_word_overlap_still_decides(blind02):
    """The rule route needs the register's date rules; without them the old word match stands (documented, not hidden)."""
    sc = summary_check(blind02["stages"], blind02["units"], blind02["rf"].anchors)
    sc = next(x for x in sc if x["addendum"] == "ADD-03")
    assert claim(sc, "extends the Proposal validity period")["matched"] == ["ADD-03/3.2"]


def test_a_claim_naming_two_changes_is_split_at_each_verb(blind02):
    text = ("This Addendum removes the model audit opinion from the Proposal, re-letters Volume I Clause 9.1, re-issues "
            "Volume II Table 2-2 and responds to clarification requests 15 to 21.")
    assert [(c["verb"], c["object"]) for c in parse_claims(text)] == [
        ("removes", "the model audit opinion from the Proposal"), ("re-letters", "Volume I Clause 9.1"),
        ("re-issues", "Volume II Table 2-2"), ("responds to", "clarification requests 15 to 21")]
    sc = check(blind02)
    removes = claim(sc, "removes the model audit opinion from the Proposal")
    reletters = claim(sc, "re-letters Volume I Clause 9.1")
    assert "ADD-03/4.1" in removes["matched"] and removes["status"] == "supported"
    assert reletters["matched"] == ["ADD-03/7.1"] and reletters["status"] == "supported"
    ks = kinds(sc)
    assert ("omitted", "ADD-03/4.1") not in ks and ("omitted", "ADD-03/7.1") not in ks
    # the true omissions the key lists stay reported
    for op in ("ADD-03/2.2", "ADD-03/4.2", "ADD-03/6.2", "ADD-03/7.2", "ADD-03/T2-2-rev/note(4)", "ADD-03/3.2"):
        assert ("omitted", op) in ks, op


def test_planted_cover_errors_of_the_sealed_key_are_both_reported(blind02):
    import yaml
    key = yaml.safe_load((B / "SEALED/expected_findings.yaml").read_text(encoding="utf-8"))
    errs = {e["id"]: e for e in key["cover_summary"]["planted_errors"]}
    assert errs["E1"]["cover_says"] == "The Proposal Due Date is unchanged." and "3.2" in errs["E2"]["truth"]
    sc = check(blind02)
    ks = kinds(sc)
    assert ("contradicted", "ADD-03/2.1") in ks                       # E1
    assert ("omitted", "ADD-03/3.2") in ks                            # E2
