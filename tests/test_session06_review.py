"""Regression tests for the owner's code review in session 06 (four findings).

Written BEFORE the fixes and run against commit 3c97a8d to confirm each failure (session 06 log, §3).
Every scenario changes in-memory copies of the curated inputs or disposable copies; nothing writes to the
repository and nothing is approved or accepted in it.
"""
from __future__ import annotations

import copy
import json
import re
import shutil
from pathlib import Path

import pymupdf
import pytest
import yaml

from tenderpack import stage2
from tenderpack.amend import Engine, load_opfile
from tenderpack.draft import draft
from tenderpack.util import ROOT

UNITS = json.loads((ROOT / "build/units.json").read_text(encoding="utf-8"))["units"]
WAIVER = "all tender requirements are waived"


def opfiles():
    return [load_opfile(ROOT / "curation/amendments/ADD-01.yaml"), load_opfile(ROOT / "curation/amendments/ADD-02.yaml")]


def run_mut(mutate):
    a, b = opfiles()
    mutate(a, b)
    return Engine(copy.deepcopy(UNITS), [a, b]).run()


def op_of(f, oid):
    return next(o for o in f.ops if o.id == oid)


def result(stages, oid):
    return next(x for s in stages for x in s.ops if x.op.id == oid)


# ============================================================================ 1. amend.py: evidence for the whole change

def test_the_legitimate_form_4g_insertion_stays_valid():
    s = run_mut(lambda a, b: None)
    assert result(s, "ADD-02/7.1").valid
    assert s[2].state["VOL-I:9.1(e)+ADD-02"].text == "FORM 4-G — CYBERSECURITY COMPLIANCE UNDERTAKING"


def test_inserted_words_the_addendum_does_not_print_make_the_op_invalid():
    def m(a, b):
        op_of(b, "ADD-02/7.1").new_text = "Form 4-G — Cybersecurity Compliance Undertaking; " + WAIVER
    s = run_mut(m)
    x = result(s, "ADD-02/7.1")
    assert not x.valid and any(c["id"] == "C21" and not c["ok"] for c in x.checks)
    assert "VOL-I:9.1(e)+ADD-02" not in s[2].state                                  # nothing inserted


def test_inserted_text_must_come_from_the_addendum_itself():
    """A unit of the pack is not evidence of what the addendum adds."""
    def m(a, b):
        o = op_of(b, "ADD-02/7.1")
        o.new_text, o.new_text_from = None, "VOL-I:8.6"
    s = run_mut(m)
    assert not result(s, "ADD-02/7.1").valid


def test_full_outputs_refuse_a_change_whose_words_no_addendum_prints():
    """Defence in depth, independent of the op types: whatever produced it, a unit whose text gains words that its
    addendum does not print is a structural failure of the outputs (C47)."""
    r = stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)
    assert next(c for c in stage2.structural_checks(r, None, {}) if c["id"] == "C47")["ok"]
    st = next(s for s in r["stages"] if s.stage == "ADD-02").state
    st["VOL-I:9.1(e)+ADD-02"].text += "; " + WAIVER
    c47 = next(c for c in stage2.structural_checks(r, None, {}) if c["id"] == "C47")
    assert not c47["ok"] and WAIVER in c47["detail"]


# ============================================================================ 2. draft.py: no exception discarded as harmless

def _synthetic(text: str, extra: list[dict] | None = None) -> list[dict]:
    base = [u for u in UNITS if not u["doc"].startswith("ADD-")]
    return base + [{"unit_id": "ADD-09:cover/para1", "doc": "ADD-09", "kind": "paragraph", "text": "Issued 1 December 2026",
                    "pages": [1]}, *(extra or []),
                   {"unit_id": "ADD-09:2.1", "doc": "ADD-09", "kind": "clause", "label": "2.1", "pages": [1], "text": text}]


CHANGE = ("In Volume I Clause 9.2, ‘one hundred and twenty (120) pages’ is deleted and ‘one hundred and fifty (150) pages’ "
          "is substituted.")
EXCEPT = "All other terms remain unchanged except that each bidder shall submit a certificate of good standing."


def test_an_exception_after_unchanged_wording_is_unresolved():
    units = _synthetic(CHANGE + " " + EXCEPT)
    f = draft(units, "ADD-09")
    d = [x for x in f.dispositions if x.provision == "ADD-09:2.1"]
    assert d and d[0].disposition == "unresolved" and "certificate of good standing" in d[0].reason
    st = Engine(units, [f]).run()[-1]
    assert st.status == "PARTIAL"


def test_cover_text_with_an_obligation_is_not_no_effect():
    units = _synthetic(CHANGE, [{"unit_id": "ADD-09:cover/para2", "doc": "ADD-09", "kind": "paragraph", "pages": [1],
                                 "text": EXCEPT}])
    f = draft(units, "ADD-09")
    d = next(x for x in f.dispositions if x.provision == "ADD-09:cover/para2")
    assert d.disposition == "unresolved" and "good standing" in d.reason


@pytest.mark.parametrize("benign", [
    "All other terms remain unchanged.",
    "All other parameters in Table 2-4 are unchanged.",
    "The time of 14:00 Riyadh time is unchanged.",
])
def test_plain_no_change_statements_stay_benign(benign):
    f = draft(_synthetic(CHANGE + " " + benign), "ADD-09")
    assert not [x for x in f.dispositions if x.provision == "ADD-09:2.1"]


# ============================================================================ 3. obligations must reach A1, A3 and A5

DRILL_B = (ROOT / "out-drill-b/build", ROOT / "out-drill-b/src/pack.yaml")


@pytest.fixture(scope="module")
def drill_b():
    return stage2.run(*DRILL_B, ROOT)


def _without(r, row_id):
    r = copy.deepcopy(r)
    r["rowfile"].rows = [x for x in r["rowfile"].rows if x.id != row_id]
    r["evals"] = [e for e in r["evals"] if e["row"].id != row_id]
    r["trace"] = stage2.obligation_trace(r)
    return r


def test_with_its_row_the_new_obligation_is_traced(drill_b):
    assert not [t for t in drill_b["trace"] if t["op"] == "ADD-03/3.1"]


def test_an_obligation_no_row_holds_is_a_visible_coverage_failure(drill_b):
    r = _without(drill_b, "ADD-03-3.1-01")
    found = [t for t in r["trace"] if t["op"] == "ADD-03/3.1"]
    assert {t["output"] for t in found} >= {"A1", "A3"}
    assert any(b["kind"] == "coverage" and "ADD-03/3.1" in b["detail"] for b in stage2.release_blockers(r))
    assert any(f["kind"] == "C46" for f in stage2.register_findings(r))
    a3 = stage2.a3(r, stage2.collect_issues(r, None), None)
    assert any("ADD-03/3.1" in i["text"] and "good standing" in i["text"].lower() for i in a3["issues_detail"])


def test_an_obligation_without_a_deliverable_is_an_a5_gap(drill_b):
    r = copy.deepcopy(drill_b)
    row = next(x for x in r["rowfile"].rows if x.id == "ADD-03-3.1-01")
    row.evidence, row.no_deliverable = [], None
    found = [t for t in stage2.obligation_trace(r) if t["op"] == "ADD-03/3.1"]
    assert [t for t in found if t["output"] == "A5"]


def test_the_real_pack_obligations_are_all_traced():
    r = stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)
    assert r["trace"] == []


# ============================================================================ 4. release gate, A3 page, labels

@pytest.fixture(scope="module")
def real():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


def test_status_flags_alone_are_not_acceptance(real):
    r = copy.deepcopy(real)
    for e in r["evals"]:
        e["row"].review, e["row"].reviewer = "accepted", None
    for s in r["stages"][1:]:
        for x in s.ops:
            x.op.review, x.op.reviewer = "accepted", "Someone"            # a name in the file is still only a flag
    details = " ".join(b["detail"] for b in stage2.release_blockers(r) if b["kind"] == "approval")
    assert f"{len(r['evals'])} of {len(r['evals'])} register rows not accepted" in details
    assert "amendment op(s) not accepted" in details


@pytest.fixture(scope="module")
def page(tmp_path_factory, real):
    out = tmp_path_factory.mktemp("s06") / "out"
    stage2.write(real, out)
    text = " ".join(pymupdf.open(out / "a3/a3.pdf")[0].get_text().split())
    return text, json.loads((out / "a3/a3.json").read_text(encoding="utf-8")), out


def _line(text: str, rid: str, ids: list[str]) -> str:
    start = text.index(rid + " ")
    nxt = [text.find(i + " ", start + len(rid)) for i in ids if i != rid]
    nxt = [n for n in nxt if n > start]
    return text[start:min(nxt) if nxt else start + 600]


def test_a3_page_keeps_the_lcc_threshold_and_every_items_confidence(page, real):
    text, a3, _ = page
    ids = [i["id"] for i in a3["explicit"] + a3["score"]] + [i["id"] for i in a3["issues_detail"]]
    lcc = _line(text, "VOL-I-8.6-01", ids)
    assert "35%" in lcc
    for item in a3["explicit"] + a3["score"]:
        line = _line(text, item["id"], ids)
        assert item["confidence"] in line, item["id"]
        it = real["register"].interp_at(next(e["row"] for e in real["evals"] if e["row"].id == item["id"]),
                                        real["validated"].stage)
        for fig in re.findall(r"\d+(?:[.,]\d+)*%?", it.quote if it else ""):
            assert fig in line, (item["id"], fig)


def test_no_stage_2_slice_labels_remain(page):
    _, _, out = page
    for p in ("README.md", "a1/a1.json", "a2/a2.md", "a3/a3.json"):
        assert not re.search(r"slice", (out / p).read_text(encoding="utf-8"), re.I), p


# ============================================================================ blind rehearsal live fix (session 06)

@pytest.mark.parametrize("text,target,old,new", [
    ("Volume I Clause 6.1, as amended by Addendum No. 1 Section 2.1, is further amended by deleting ‘Thursday 26 November "
     "2026’ and substituting ‘Thursday 3 December 2026’.", "VOL-I:6.1", "Thursday 26 November 2026", "Thursday 3 December 2026"),
    ("In footnote 12 to Volume I Clause 8.5, ‘80,000 m³/day’ is deleted and ‘70,000 m³/day’ is substituted.",
     "VOL-I:8.5#fn12", "80,000 m3/day", "70,000 m3/day"),                 # quoted words are normalized
    ("In Volume I Clause 8.6, as reinstated by Addendum No. 2 Section 9.1, ‘thirty-five per cent (35%)’ is deleted and "
     "‘forty per cent (40%)’ is substituted.", "VOL-I:8.6", "thirty-five per cent (35%)", "forty per cent (40%)"),
])
def test_drafter_reads_qualified_citations_and_footnotes(text, target, old, new):
    """Phrasings the blind addendum used and ADD-01/ADD-02 did not (session 06 live fix); generic, nothing hardcoded."""
    units = _synthetic(text)
    f = draft(units, "ADD-09")
    ops = [o for o in f.ops if o.provision == "ADD-09:2.1"]
    assert [(o.type, o.target, o.old, o.new) for o in ops] == [("replace_text", target, old, new)]


def test_drafter_reads_a_new_clause_inserted_after_another():
    units = _synthetic("The following new Clause 10.9 is inserted in Volume I after Clause 10.4: ‘10.9  Prices shall be "
                       "firm for the term.’")
    f = draft(units, "ADD-09")
    (o,) = [o for o in f.ops if o.provision == "ADD-09:2.1"]
    assert o.type == "insert_unit" and o.anchor == "VOL-I:10.4" and o.new_text == "Prices shall be firm for the term."


def _units_with(provision: str) -> list[dict]:
    return _synthetic(provision)


def test_set_value_on_a_text_cell_needs_the_quoted_words_not_a_unit():
    """Blind rehearsal live fix: 'the basis of assessment is amended to ...' sets a text cell; a figure still needs its
    unit (finding 1 of session 05 stays fixed)."""
    from tenderpack.amend import Op, OpFile
    units = _synthetic("In Volume II Table 2-4, in the row for Total Nitrogen (TN), the basis of assessment is amended to "
                       "‘Maximum, any single sample’.")
    f = OpFile(addendum="ADD-09", issued_from="ADD-09:cover/para1", prepared_by="test", method="test",
               ops=[Op(id="ADD-09/2.1", provision="ADD-09:2.1", type="set_value", target="VOL-II:T2-4/TN",
                       column="Basis of assessment", new="Maximum, any single sample", origin="assistant")])
    st = Engine(units, [f]).run()[-1]
    assert st.ops[0].valid and st.state["VOL-II:T2-4/TN"].cells["Basis of assessment"] == "Maximum, any single sample"
    f.ops[0].new = "Maximum, any sample"                                                   # words not printed
    assert not Engine(units, [f]).run()[-1].ops[0].valid


def test_replace_text_in_a_table_row_changes_the_cell_too():
    units = _synthetic("In Volume II Table 2-6, in row 2-6.2, ‘7,500’ is deleted and ‘9,000’ is substituted.")
    from tenderpack.amend import Op, OpFile
    f = OpFile(addendum="ADD-09", issued_from="ADD-09:cover/para1", prepared_by="test", method="test",
               ops=[Op(id="ADD-09/2.1", provision="ADD-09:2.1", type="replace_text", target="VOL-II:T2-6/2-6.2",
                       old="7,500", new="9,000", origin="assistant")])
    st = Engine(units, [f]).run()[-1]
    u = st.state["VOL-II:T2-6/2-6.2"]
    assert st.ops[0].valid and "9,000" in u.text and u.cells["Value"] == "9,000"


@pytest.mark.parametrize("text,target", [
    ("In the revised Form 4-A at Appendix A to Addendum No. 1, the entry against ‘Proposal Due Date’ is corrected to read "
     "‘3 December 2026, 14:00 Riyadh time’.", "ADD-01:AppA/proposal-due-date"),
    ("The response to clarification request 13 in Addendum No. 2 is superseded.", "ADD-02:Q13"),
    ("Form 4-C is amended by adding, after the fifth numbered declaration, the following declaration.", "VOL-IV:F4-C/image/decl5"),
    ("In Volume II Table 2-6, in row 2-6.2, ‘7,500’ is deleted and ‘9,000’ is substituted.", "VOL-II:T2-6/2-6.2"),
])
def test_targets_named_the_way_the_blind_addendum_names_them_are_verified(text, target):
    """Blind rehearsal live fix 3: citation forms ADD-01/ADD-02 did not use. Verification stays strict: the wrong
    field or declaration is still refused."""
    from tenderpack.citations import verify_target
    ids = {u["unit_id"] for u in UNITS}
    label = {u["unit_id"]: u.get("label") for u in UNITS}.get
    assert verify_target(target, text, ids, label)[0]
    wrong = {"ADD-01:AppA/proposal-due-date": "ADD-01:AppA/name-of-bidder-lead-member", "ADD-02:Q13": "ADD-02:Q12",
             "VOL-IV:F4-C/image/decl5": "VOL-IV:F4-C/image/decl4", "VOL-II:T2-6/2-6.2": "VOL-II:T2-6/2-6.3"}[target]
    if wrong in ids:
        assert not verify_target(wrong, text, ids, label)[0]


def test_a3_condenses_in_labelled_steps_and_never_drops_a_disqualifier(page, tmp_path):
    """Blind rehearsal finding: an addendum adding disqualifiers can push A3 past one page. The fallback is
    deterministic, stated on the page, and never touches the explicit consequences."""
    from tenderpack.render import write_a3_pdf
    _, a3, _ = page
    # session 11 (audit A3-1): the gate list goes first (level 1), then the question ids (level 2: the real pack fits here,
    # every issue with its reason); level 3 (ids and owners only) is the earlier level 1
    for level in (2, 3):
        cond = stage2.condense_a3(a3, level)
        fit = write_a3_pdf(cond, tmp_path / f"a3-{level}.pdf")
        text = " ".join(pymupdf.open(tmp_path / f"a3-{level}.pdf")[0].get_text().split()).replace("- ", "-")  # wrapped ids
        assert fit["pages"] == 1 and f"Condensed (level {level})" in text
        assert all(i["id"] in text for i in a3["explicit"] + a3["score"])
        # ids stay, linked: each issue shown, or folded into the issue it duplicates (session 08 grouping)
        folded = {f: i["id"] for g in a3["groups"]["groups"] for i in g["items"] for f in i["folds"]}
        assert all(i["id"] in text or folded.get(i["id"], "") in text for i in a3["unresolved"]["items"])
        assert "a3_detail.html" in text
