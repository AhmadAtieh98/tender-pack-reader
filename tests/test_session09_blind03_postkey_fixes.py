"""Session 09, blind rehearsal 03: fixes made AFTER the answer key was opened (11:05 UTC), so they are not scored
(rehearsals/blind-03/COMPARISON.md). Each failed before its fix.

1. C28 did not test the cover claim "The closure ... does not affect any deadline under the RFP Documents" (the
   planted E1): the clarification cut-off moved from 12 to 11 November 2026 through the amended Working Day definition.
   Such a claim is now checked against the date rules whose computed date changed between the stages.
2. C28 read the curator's insert_unit + set_status deleted at one anchor (the Form 4-C fourth declaration) as three
   contradictions of "replaces the fourth declaration in Form 4-C": that pair is a substitution.
3. citations() matched "Form N-X" case-sensitively, so a provision whose only naming of the form is its section
   heading ("4. AMENDMENT TO FORM 4-C") could not carry an op on that form.

The blind-03 build is used where the rehearsal's own build is current (it is not committed), else a fresh ingest."""
from __future__ import annotations

import pytest

from tenderpack import stage2, summary
from tenderpack.amend import Engine, Op, OpFile, load_opfile
from tenderpack.citations import citations, resolve
from tenderpack.cli import ingest
from tenderpack.util import ROOT

B = ROOT / "rehearsals/blind-03"


@pytest.fixture(scope="module")
def blind03(tmp_path_factory):
    evidence = B / "build"
    if not (evidence.exists() and not stage2.load_evidence(evidence, ROOT)[1]):
        evidence = tmp_path_factory.mktemp("blind-03") / "build"
        assert ingest(B / "work/pack.yaml", evidence, ROOT, quiet=True)["exit_code"] == 0
    return stage2.run(evidence, B / "work/pack.yaml", ROOT)


def _rec(r, add="ADD-03"):
    return next(x for x in r["summary_check"] if x["addendum"] == add)


# ---------------------------------------------------------------------------- 1. "does not affect any deadline"

CLOSURE = "The closure of the Authority's offices does not affect any deadline under the RFP Documents."


def test_a_no_deadline_claim_is_parsed_and_judged_by_the_computed_dates():
    (c,) = summary.no_date_effect_claims("This Addendum amends things. " + CLOSURE + " All other terms stand.")
    assert c["kind"] == "no_date_effect" and c["object"].startswith("The closure") and "any deadline" in c["scope"]
    assert summary.no_date_effect_claims("The Proposal Due Date is unchanged.") == []      # that is an 'unchanged' claim
    rec = {"claims": [], "findings": [], "sentence": ""}
    moved = [{"row": "VOL-I-5.2-01", "rule_id": "CLARIFICATION-CUTOFF", "old": "2026-11-12", "new": "2026-11-11",
              "anchor": "PDD", "source_unit": "VOL-I:5.2"}]
    summary._check_no_date_effect(rec, "ADD-03", [{"text": CLOSURE}], {"ADD-03": moved}, {}, {})
    assert rec["claims"][0]["status"] == "contradicted"
    assert any(f["kind"] == "contradicted" and "CLARIFICATION-CUTOFF" in f["detail"] and "2026-11-12" in f["detail"]
               and "2026-11-11" in f["detail"] for f in rec["findings"]), rec["findings"]
    rec = {"claims": [], "findings": [], "sentence": ""}
    summary._check_no_date_effect(rec, "ADD-03", [{"text": CLOSURE}], {"ADD-03": []}, {}, {})
    assert rec["claims"][0]["status"] == "supported" and rec["findings"] == []
    rec = {"claims": [], "findings": [], "sentence": ""}
    summary._check_no_date_effect(rec, "ADD-03", [{"text": CLOSURE}], None, {}, {})
    assert rec["claims"][0]["status"] == "not checked" and rec["findings"][0]["kind"] == "unchecked"


def test_a_claim_about_one_anchor_is_judged_by_that_anchors_rules_only():
    rec = {"claims": [], "findings": [], "sentence": ""}
    text = "The closure does not affect the Proposal Due Date."
    moved = [{"row": "VOL-I-5.2-01", "rule_id": "CLARIFICATION-CUTOFF", "old": "2026-11-12", "new": "2026-11-11",
              "anchor": "PDD", "source_unit": "VOL-I:5.2"}]
    anchors = {"PDD": {"name": "Proposal Due Date", "defined_in": "VOL-I:6.1"}}
    summary._check_no_date_effect(rec, "ADD-03", [{"text": text}], {"ADD-03": moved}, anchors, {})
    assert rec["claims"][0]["status"] == "supported"            # the PDD itself did not move; a rule counted from it did
    moved_pdd = [{"row": "VOL-I-6.1-01", "rule_id": "PDD", "old": "2026-11-26", "new": "2026-12-10", "anchor": None,
                  "source_unit": "VOL-I:6.1"}]
    rec = {"claims": [], "findings": [], "sentence": ""}
    summary._check_no_date_effect(rec, "ADD-03", [{"text": text}], {"ADD-03": moved_pdd}, anchors, {})
    assert rec["claims"][0]["status"] == "contradicted"


def test_blind_03s_planted_cover_sentence_is_contradicted_by_the_moved_cut_off(blind03):
    rec = _rec(blind03)
    c = next(x for x in rec["claims"] if x["kind"] == "no_date_effect")
    assert c["status"] == "contradicted"
    f = [x for x in rec["findings"] if x["kind"] == "contradicted" and x.get("claim") == c["n"]]
    assert any("CLARIFICATION-CUTOFF" in x["detail"] and "2026-11-12" in x["detail"] and "2026-11-11" in x["detail"]
               for x in f), f
    assert "no_date_effect" not in {x["kind"] for x in _rec(blind03, "ADD-02")["claims"]}


# ---------------------------------------------------------------------------- 2. insert + delete at one anchor

def test_insert_and_delete_at_one_anchor_is_a_substitution(blind03):
    rec = _rec(blind03)
    c = next(x for x in rec["claims"] if x["text"].startswith("replaces the fourth declaration"))
    assert c["status"] == "supported", c
    assert {"ADD-03/4.1(a)", "ADD-03/4.1(b)"} <= set(c["matched"])
    assert not [f for f in rec["findings"] if f["kind"] == "contradicted" and f.get("op") in ("ADD-03/4.1(a)", "ADD-03/4.1(b)")]
    # the obligation 4.4 adds is still reported as something the summary leaves out
    assert any(f.get("op") == "ADD-03/4.4" and f["kind"] in ("omitted", "understated") for f in rec["findings"])
    # the planted omission (E2) is still found
    assert any(f["kind"] == "omitted" and f.get("op") == "ADD-03/6.1" for f in rec["findings"])


# ---------------------------------------------------------------------------- 3. a heading names the form

def test_a_heading_names_the_form_whatever_its_case():
    ids = {"VOL-IV:F4-C/image/decl4", "VOL-IV:F4-C/para1"}
    assert resolve(citations("4. AMENDMENT TO FORM 4-C"), ids) == ["VOL-IV:F4-C"]
    assert resolve(citations("Form 4-C shall be completed"), ids) == ["VOL-IV:F4-C"]
    assert [c.target for c in citations("in the FORM 4-C image")] == ["VOL-IV:F4-C"]


def test_a_substitution_can_be_written_under_the_provision_that_prints_the_new_text(blind03):
    """ADD-03 4.2 prints the substituted declaration under the heading '4. AMENDMENT TO FORM 4-C' and names no other
    target. A replace_text under 4.2 on the issued declaration now passes C21 and C22 (the curator had to write
    insert_unit + set_status under 4.1 instead)."""
    units = blind03["units"]
    files = [load_opfile(B / "work/amendments" / f"{a}.yaml") for a in ("ADD-01", "ADD-02")]
    before = Engine(units, files).run()[-1].state
    old = before["VOL-IV:F4-C/image/decl4"].text
    new = next(o for o in load_opfile(B / "work/amendments/ADD-03.yaml").ops if o.id == "ADD-03/4.1(a)").new_text
    op = Op(id="T/4.2", provision="ADD-03:4.2", type="replace_text", target="VOL-IV:F4-C/image/decl4", old=old, new=new,
            old_resolved="matched_in_target", origin="assistant", review="proposed")      # 4.1 quotes the old words, 4.2 does not
    f = OpFile(addendum="ADD-03", issued_from="ADD-03:cover/para1", prepared_by="test", method="test", ops=[op])
    x = next(r for r in Engine(units, files + [f]).run()[-1].ops if r.op.id == "T/4.2")
    assert x.valid, [c for c in x.checks if not c["ok"]]
    assert x.applied and "خلال ثلاثة أيام عمل" in Engine(units, files + [f]).run()[-1].state["VOL-IV:F4-C/image/decl4"].text
