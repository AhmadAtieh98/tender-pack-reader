"""Session 11 audit, fixer F2: the one-page A3 and the statements beside the image readings (findings A3-1 .. A3-9 and
R-1, R-4, R-5, R-6, R-8 of the independent audit). Each test reproduces one finding on the real pack (the evidence build
in build/ and the curated inputs) or on small synthetic inputs. Passing them approves nothing."""
from __future__ import annotations

import copy
import json
import re
import unicodedata

import pymupdf
import pytest

from tenderpack import packets, register, stage2
from tenderpack.render import A3_MIN_TEXT_PT, A3OverflowError, write_a3_pdf
from tenderpack.util import ROOT, load_yaml


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    """stage2.run on the real build, and A3 as stage2.write makes it (first condensation level that fits one page)."""
    r = stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)
    v = r["validated"].stage
    main = stage2.a5_all(r)[v]
    issues = stage2.collect_issues(r, main)
    a3 = stage2.a3(r, issues, main)
    out = tmp_path_factory.mktemp("a3audit")
    fit, level = None, None
    for level in range(getattr(stage2, "A3_LEVELS", 3) + 1):
        try:
            fit = write_a3_pdf(stage2.condense_a3(a3, level), out / "a3.pdf")
            break
        except A3OverflowError:
            continue
    page = pymupdf.open(out / "a3.pdf")[0]
    lines = [ln for b in page.get_text("dict")["blocks"] for ln in b.get("lines", [])]
    nfkc = lambda s: unicodedata.normalize("NFKC", s)  # noqa: E731  (ligatures such as 'ﬁ' in the extracted text)
    line_texts = [nfkc("".join(s["text"] for s in ln["spans"])) for ln in lines]
    text = " ".join(" ".join(line_texts).split())
    detail = stage2.a3_detail_html(a3)
    return {"r": r, "a3": a3, "issues": issues, "a5": main, "fit": fit, "level": level, "text": text,
            "lines": line_texts, "detail": detail, "out": out}


def _item(a3, rid):
    return next(i for s in a3["sections"] for i in s["items"] if i["id"] == rid)


def _listed(a3):
    return [i for g in a3["groups"]["groups"] for i in g["items"]]


# ---------------------------------------------------------------------------------------------- A3-1, R-3: the 'why'

def test_a3_1_every_listed_issue_shows_its_reason_and_owner_on_the_one_page(built):
    a3, text, fit = built["a3"], built["text"], built["fit"]
    assert fit and fit["pages"] == 1 and fit["min_text_pt"] >= A3_MIN_TEXT_PT
    listed = _listed(a3)
    assert listed and all(i["short"] for i in listed)
    for i in listed:                                  # id, its reason and its owner, on the page
        assert i["id"] in text, i["id"]
        assert " ".join(i["short"].split())[:40] in text, (i["id"], i["short"])
        assert f"({i['owner']})" in text, i["id"]
    # the gate's 36 ids became a count before any issue text was removed (session 12, F1, audit A1-4: changed
    # deliberately from 37: ADD-02-5.2-01 states no consequence and is now classed scored, not a pass/fail gate)
    gate = next(s for s in a3["sections"] if s["heading"].startswith("General gate"))
    assert len(gate["ids"]) == 36 and "VOL-I-10.1-01" not in text and "a3_detail.html" in text
    # the curated 'unresolved' (9) and 'missing' (6) lists are merged into the grouped list, marked †, never dropped
    roots = {i["id"] for i in listed if i.get("decide")}
    for key in ("unresolved", "missing"):
        for i in a3[key]["items"]:
            assert i["listed_as"] in roots and i["listed_as"] in text, i


# ---------------------------------------------------------------------------------------------- A3-5, R-5: folding

def test_a3_5_overlapping_issues_are_folded_and_pipeline_items_stay_on_the_detail_page(built):
    a3 = built["a3"]
    listed = {i["id"]: i for i in _listed(a3)}
    late = [a["id"] for a in built["a5"]["activities"] if a["status"].startswith("INFEASIBLE")]
    assert set(late) >= {"lcc-ratio", "lcc-certificate", "assemble-envelope-a", "copies", "seal-and-mark", "deliver"}
    assert {"I-A5-FEASIBILITY", *[f"I-A5-{a}" for a in late]} <= set(listed["I-LCC-ISSUER"]["folds"])
    assert "I-AUTO-NOT-SUPPLIED-ENVIRONMENTAL-PERMIT" in listed["I-PERMIT"]["folds"]
    assert {"I-AUTO-NOT-SUPPLIED-VOL-V-SCHEDULE-7", "I-AUTO-NOT-SUPPLIED-VOL-V-SCHEDULE-11"} <= set(listed["I-VOL-V-MISSING"]["folds"])
    detail = {i["id"]: i for i in a3["issues_detail"]}
    for iid in ("I-OP-ADD-02/T1-1-rev/note(2)", "I-AUTO-SUMMARY-ADD-01", "I-AUTO-SUMMARY-ADD-02", "I-READING-F4C"):
        assert iid not in listed and detail[iid]["detail_only"], iid
    for iid in listed["I-LCC-ISSUER"]["folds"]:
        assert detail[iid]["folded_into"] == "I-LCC-ISSUER"
    assert len(listed) <= 25 and "A5: 6 INFEASIBLE by 12 WD" in listed["I-LCC-ISSUER"]["short"]


# ---------------------------------------------------------------------------------------------- A3-8, R-4: counts

def test_a3_8_counts_and_lists_agree_across_pdf_html_and_json(built):
    a3, text, detail = built["a3"], built["text"], built["detail"]
    c = a3["groups"]["counts"]
    assert c["all"] == len(a3["issues_detail"]) == c["listed"] + c["folded"] + c["detail_only"] + len(c["gate_note"])
    assert c["listed"] == len(_listed(a3)) and f"— {c['listed']} open issues" in a3["groups"]["heading"]
    assert " ".join(a3["groups"]["heading"].split()) in text and a3["issue_counts"] in " ".join(text.split())
    assert a3["issue_counts"] in detail and f"{c['all']} open issues: {c['listed']} listed, {c['folded']} folded" in detail
    for key in ("unresolved", "missing"):                 # rendered on the detail page too (grep 'Could not resolve')
        assert a3[key]["heading"] in detail
    # session 12 (F2, audit A3-3): '(17 rows, 1 corroborating)' was a pipeline term; the corroborating row is shown on
    # the line of the row it restates ('also stated in ...'), so the subtitle counts the triggers only
    assert "16 explicit bid-out triggers + 1 below the score threshold" in a3["subtitle"]
    assert sum(int(s["heading"].rsplit(": ", 1)[1]) for s in a3["sections"] if s["heading"].startswith("Explicit")) == 16 + 1


# ---------------------------------------------------------------------------------------------- A3-2: INFEASIBLE basis

def test_a3_2_infeasible_flags_state_the_assumed_lead_time_they_rest_on(built):
    lead = built["r"]["assumptions"]["lead_times"]["lcc_certificate"]
    for rid in ("VOL-I-6.1-01", "VOL-I-8.6-01"):
        flag = next(f for f in _item(built["a3"], rid)["flags"] if f.startswith("INFEASIBLE"))
        assert f"Local Content Certificate {lead['value']} WD, not stated in the pack" in flag
        # session 12 (F2, audit A3-3): the flag cites the issue as listed on the page; I-A5-FEASIBILITY is folded into
        # I-LCC-ISSUER, so the flag cites I-LCC-ISSUER
        assert "PROVISIONAL" in flag and "float -12 WD" in flag and "I-LCC-ISSUER" in flag
        assert " ".join(flag.split())[:60] in built["text"]


# ---------------------------------------------------------------------------------------------- A3-3: the gate heading

def test_a3_3_gate_heading_claims_no_stage_and_counts_envelope_b_rows(built):
    gate = next(s for s in built["a3"]["sections"] if s["heading"].startswith("General gate"))
    note = gate["note"]
    assert "stage (i)" not in note and "state no consequence of their own" not in note
    assert "Mandatory; no bid-out consequence stated" in note
    assert "the pack does not say which clause is checked at which stage" in note
    env_b = set(gate["envelope_b_ids"])
    assert {"VOL-I-10.1-01", "VOL-I-10.2-01", "VOL-I-10.3-01", "VOL-I-10.3-02", "VOL-I-10.4-01", "VOL-I-10.6-01",
            "VOL-IV-F4F-01", "VOL-IV-F4F-02"} == env_b and f"{len(env_b)} are Envelope B items" in note
    assert "Pass/fail with no stated consequence" not in built["detail"]


# ---------------------------------------------------------------------------------------------- A3-4, R-1: gloss labels

CONFIRMED = "translation confirmed by the owner 2026-10-03 (VOL-IV-p6-r1)"


def test_a3_4_gloss_label_is_derived_from_the_approval_state(built):
    a3, r = built["a3"], built["r"]
    assert _item(a3, "VOL-IV-F4C-04")["gloss_label"] == CONFIRMED + "; category mapping open (I-F4C-EXCLUSION)"
    assert _item(a3, "VOL-IV-F4C-N1")["gloss_label"] == CONFIRMED
    assert "not reviewed: ‘leads to" not in built["detail"] and CONFIRMED in built["detail"]
    a1 = {x["id"]: x for x in stage2.a1_table(r, built["issues"])["rows"]}
    assert CONFIRMED in a1["VOL-IV-F4C-04"]["consequence"] and "not reviewed" not in a1["VOL-IV-F4C-04"]["consequence"]
    # the same rule says 'not reviewed' when the reading is pending, or when the gloss is not the approved translation
    unit = {"translation": "Any incorrect statement leads to the exclusion of the proposal.",
            "reading": {"region": "R1", "status": "approved"}}
    appr = {"date": "2026-10-03", "reviewer": "A Person"}
    assert register.gloss_label("leads to the exclusion of the proposal", unit, appr) == "translation confirmed by the owner 2026-10-03 (R1)"
    assert register.gloss_label("leads to the exclusion of the proposal", {**unit, "reading": {"region": "R1", "status": "pending"}},
                       appr) == register.GLOSS_NOT_REVIEWED
    assert register.gloss_label("results in disqualification", unit, appr) == register.GLOSS_NOT_REVIEWED
    assert register.gloss_label("leads to the exclusion of the proposal", unit, None) == register.GLOSS_NOT_REVIEWED


def test_c52_fails_when_an_output_calls_an_approved_translation_not_reviewed(built, tmp_path):
    r = built["r"]
    (tmp_path / "a1").mkdir()
    (tmp_path / "a1" / "a1.csv").write_text("VOL-IV-F4C-04,\"exclusion (proposed translation, not reviewed: "
                                            "'leads to the exclusion of the proposal')\"\n", encoding="utf-8")
    bad = stage2.gloss_currency_check(r, tmp_path)
    assert bad["id"] == "C52" and not bad["ok"] and "a1/a1.csv" in bad["detail"]
    (tmp_path / "a1" / "a1.csv").write_text(f"VOL-IV-F4C-04,\"exclusion ({CONFIRMED}: 'leads to the exclusion of the "
                                            "proposal')\"\n", encoding="utf-8")
    assert stage2.gloss_currency_check(r, tmp_path)["ok"]


# ---------------------------------------------------------------------------------------------- A3-6: counted twice

def test_a3_6_form_4c_trigger_is_listed_once_with_its_corroborating_sources(built):
    a3, text = built["a3"], built["text"]
    n1, main = _item(a3, "VOL-IV-F4C-N1"), _item(a3, "VOL-I-9.4-01")
    assert n1["corroborates"] == "VOL-I-9.4-01"
    c = next(x for x in main["corroborated_by"] if x["id"] == "VOL-IV-F4C-N1")
    assert c["adds"] == "ADD-02 Q9: English with an Arabic translation is not acceptable"
    assert any("May Form 4-C be submitted in English with an Arabic translation?" in q for q in c["adds_evidence"])
    assert any(a.startswith("VOL-IV") and "p5" in a for a in c["also"])
    nr = next(s for s in a3["sections"] if s["heading"].startswith("Explicit — Non-responsive"))
    assert nr["heading"].endswith(": 8")
    assert "also stated in VOL-IV-F4C-N1" in text and "English with an Arabic translation is not acceptable" in text
    assert text.count("VOL-IV-F4C-N1") == 1                                   # one line, not two


def test_a3_6_unverified_corroboration_is_flagged_not_folded(built):
    r = built["r"]
    row = next(e["row"] for e in r["evals"] if e["row"].id == "VOL-IV-F4C-N1")
    fake = row.model_copy(update={"corroborates": register.Corroboration(row="VOL-I-9.4-01", also=[
        register.Quotation(unit="VOL-IV:F4-C/para1", page=5, words="these words are not printed there")])})
    rr = {"stages": r["stages"], "validated": r["validated"], "evals": [{"row": fake}]}
    explicit = [{"id": "VOL-IV-F4C-N1", "cls": "non_responsive", "class": "non-responsive"},
                {"id": "VOL-I-9.4-01", "cls": "non_responsive", "class": "non-responsive"}]
    got = stage2._corroborations(rr, r["validated"].stage, explicit)
    assert "not found" in got["VOL-IV-F4C-N1"]["problem"]


# ---------------------------------------------------------------------------------------------- A3-7: footnote 12

def test_a3_7_footnote_12_keeps_its_words_and_the_window_start_is_computed(built):
    r, a3 = built["r"], built["a3"]
    e = next(x for x in r["evals"] if x["row"].id == "VOL-I-8.5-01")
    row, v = e["row"], r["validated"].stage
    assert "each having achieved commercial operation within the ten (10) years preceding" in row.requirement
    it = r["register"].interp_at(row, v)
    assert it.quote.endswith("80,000 m³/day and each having achieved commercial operation within the ten (10) years "
                             "preceding the Proposal Due Date")
    assert not e["stages"][v]["problems"]                                   # the full quote is found (C16)
    d = next(x for x in e["stages"][v]["dates"] if x["rule_id"] == "REFERENCE-LOOKBACK")
    other = next(i["value"] for i in d["interpretations"] if i["value"] != d["planning"]["value"])
    fact = next(f for f in _item(a3, "VOL-I-8.5-01")["facts"] if f.startswith("window starts"))
    assert fact.startswith(f"window starts {d['planning']['value']} ({other} if ") and f"PDD {d['anchor_value']}" in fact
    rows_text = (ROOT / "curation/register/rows.yaml").read_text(encoding="utf-8")
    block = rows_text.split("- id: VOL-I-8.5-01", 1)[1].split("\n  - id:", 1)[0]
    assert "2016" not in block                                               # computed, never typed
    assert " ".join(fact.split())[:40] in built["text"]


# ---------------------------------------------------------------------------------------------- A3-9: the pre-bid line

def test_a3_9_prebid_line_says_held_and_that_the_correction_window_closed(built):
    r, a3 = built["r"], built["a3"]
    facts = "; ".join(_item(a3, "VOL-I-5.4-01")["facts"])
    v = r["validated"].stage
    notice = next(d for e in r["evals"] if e["row"].id == "ADD-01-3.1-01" for d in e["stages"][v]["dates"])
    assert "held 2026-09-30" in facts and "compliance is a bidder fact to confirm (I-BIDDER-FACTS)" in facts
    assert f"ADD-01 3.1 window closed {notice['planning']['value']} (2026-10-15 if event day excluded)" in facts
    assert notice["planning"]["value"] == "2026-10-14" or str(notice["planning"]["value"]) == "2026-10-14"
    assert "held 2026-09-30" in built["text"]


# ---------------------------------------------------------------------------------------------- R-6: ids unbroken

def test_r6_no_id_is_broken_at_an_internal_hyphen(built):
    broken = [ln for ln in built["lines"] if re.search(r"\b[A-Z][A-Z0-9]*-$", ln.rstrip())]
    assert not broken, broken[:5]


# ---------------------------------------------------------------------------------------------- R-8: settled points

def test_r8_uncertainties_an_approval_settles_are_tagged_and_the_others_are_not():
    for rg, settled, open_ in (("VOL-IV-p6-r1", "`decl5` numeral `٤-٢`", "Diacritics (tanween"),
                               ("VOL-II-p3-r1", "row `FaecalColiforms`", "row `ResidualChlorine`")):
        p = json.loads((ROOT / "build/review" / rg / "packet.json").read_text(encoding="utf-8"))
        appr = p["approval"]
        s = next(d for d in p["decisions"] if d.startswith(settled))
        tag = packets.settled_by(s, appr)
        assert tag and tag.startswith(f"settled by {appr['reviewer']} {appr['date']}: ")
        assert packets.settled_by(next(d for d in p["decisions"] if d.startswith(open_)), appr) is None
        assert packets.settled_by(s, {"status": "pending"}) is None
    # the readings themselves are not edited (their headers are pinned by the approvals' sha256)
    import hashlib
    for a in load_yaml(ROOT / "curation/approvals.yaml")["approvals"]:
        f = a["reading_file"]
        assert hashlib.sha256((ROOT / f["path"]).read_bytes()).hexdigest() == f["sha256"]
