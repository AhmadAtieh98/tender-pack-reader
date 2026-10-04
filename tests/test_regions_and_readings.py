"""Regions, raster structure, readings and review status. Not tailored to the two pack images:
the synthetic fixture exercises an image table with Arabic, a vector graphic, and an OCR layer."""
import copy

import numpy as np
import pymupdf
import pytest

from tenderpack import arabic
from tenderpack.readings import Reading, check_reading, load_readings, review_status, review_subject
from tenderpack.regions import despeckle, detect_grid, image_array, text_bands, unexplained_ink
from tenderpack.textnorm import normalize_arabic

from conftest import ROOT


def _region(pack, rid):
    return next(g for d in pack["pack"].docs for g in d.regions if g.region_id == rid)


def test_pack_regions_are_exactly_the_two_images(pack, golden):
    regs = pack["coverage"]["regions"]
    assert sorted((r["doc"], r["page"], r["kind"]) for r in regs) == sorted(
        (g["doc"], g["page"], "image") for g in golden["image_regions"])


def test_image_page_with_text_layer_still_needs_reading(pack):
    """VOL-IV p6 has header, footer and watermark text; that must not count as the page being read."""
    p6 = next(p for p in pack["coverage"]["pages"] if p["doc"] == "VOL-IV" and p["page"] == 6)
    assert sum(p6["excluded"].values()) >= 4 and p6["regions"]


def test_synthetic_regions(synthetic):
    """Every region the builder placed is detected (image table, straight-line triangle, curve, scan, dark box);
    each has a reading from the builder's ground truth, so coverage passes and every reading stays PENDING."""
    exp = synthetic["expected"]
    kinds = sorted((r["page"], r["kind"]) for r in synthetic["coverage"]["regions"])
    assert kinds == sorted([(4, k) for k in exp["p4"]["regions"]] + [(5, k) for k in exp["p5"]["regions"]])
    p5 = next(r for r in synthetic["coverage"]["regions"] if r["page"] == 5 and r["kind"] == "image")
    assert any("invisible text" in n for n in p5["notes"])
    inv = synthetic["by_id"]["SYN-01:invisible:p5"]
    assert inv["text"] == exp["p5"]["invisible_text"]
    c05 = next(c for c in synthetic["coverage"]["checks"] if c["id"] == "C05")
    assert c05["ok"] and "PENDING HUMAN REVIEW" in c05["detail"]
    assert {pk["status"] for pk in synthetic["packets"].values()} == {"pending"}   # nothing approved by itself


def test_unexplained_ink_is_found_when_nothing_explains_it():
    doc = pymupdf.open()
    page = doc.new_page(width=300, height=200)
    page.insert_text((20, 50), "Text that the text layer explains", fontsize=12)
    page.draw_rect(pymupdf.Rect(40, 100, 140, 160), color=None, fill=(0, 0, 0))
    words = [pymupdf.Rect(w[:4]) for w in page.get_text("words")]
    assert unexplained_ink(page, words)                 # the black box is unexplained
    assert not unexplained_ink(page, words + [pymupdf.Rect(40, 100, 140, 160)])


def test_despeckle_keeps_strokes_drops_dots():
    a = np.zeros((20, 20), bool)
    a[5, 5] = True                       # isolated dot
    a[10, 2:18] = True                   # a stroke
    d = despeckle(a)
    assert not d[5, 5] and d[10, 3:17].all()


def test_table_2_4_grid_from_pixels(pack, golden):
    g = detect_grid(image_array(pymupdf.open(ROOT / "sources/candidate_pack/VOL-II_Technical_Requirements.pdf"),
                                _region(pack, "VOL-II-p3-r1")))
    assert (g.rows, g.cols) == (golden["table_2_4_image"]["rows"] + 1, golden["table_2_4_image"]["cols"])
    assert -1.0 < g.skew_deg < 0.0


def test_synthetic_image_table_grid(synthetic):
    rid = "SYN-01-p4-r1"
    reg = next(g for d in synthetic["pack"].docs for g in d.regions if g.region_id == rid)
    pdf = pymupdf.open(synthetic["src"] / "SYN-01_Synthetic_Test_Volume.pdf")
    g = detect_grid(image_array(pdf, reg))
    assert (g.rows, g.cols) == (synthetic["expected"]["p4"]["image_text_rows"], synthetic["expected"]["p4"]["image_text_cols"])


def test_form_4c_bands_include_faint_footer(pack, golden):
    reg = _region(pack, "VOL-IV-p6-r1")
    bands = text_bands(image_array(pymupdf.open(ROOT / "sources/candidate_pack/VOL-IV_Form_Sheets.pdf"), reg))
    assert sum(b["kind"] == "text" for b in bands) == golden["form_4c_image"]["text_bands"]
    assert sum(b["kind"] == "rule" for b in bands) == golden["form_4c_image"]["rule_bands"]
    reading, _ = load_readings(ROOT / "curation/readings")["VOL-IV-p6-r1"]
    footer = next(b for b in reading.blocks if b.role == "image-footer")
    assert footer.source == golden["form_4c_image"]["footer_band_text"]


def test_both_readings_pass_their_checks_and_carry_only_the_owners_approval(pack):
    """Session 08: the owner (Ahmad) confirmed both readings on 3 Oct 2026; each approval is pinned to the reviewed
    subject, names its confirmation record and says what it does not cover."""
    for rid in ("VOL-II-p3-r1", "VOL-IV-p6-r1"):
        pk = pack["packets"][rid]
        assert pk["status"] == "approved" and pk["approval"]["reviewer"] == "Ahmad" and pk["approval"]["date"] == "2026-10-03"
        assert pk["approval"]["does_not_cover"] and "session-08_prompt" in pk["approval"]["confirmation_record"]
        failed = [c for c in pk["checks"] if not c["ok"]]
        assert not failed, failed
    assert any("4.2" in x for x in pack["packets"]["VOL-IV-p6-r1"]["approval"]["resolutions"])
    assert "not_confirmed" in pack["packets"]["VOL-II-p3-r1"]["approval"]["permit"]
    tn = pack["by_id"]["VOL-II:T2-4/TN"]
    assert tn["reading"]["status"] == "approved" and tn["origin"] == "image_reading"
    assert tn["cells"]["Limit"] == "5" and tn["numeric"]["Limit"]["values"] == [5.0]
    assert tn["cells"]["Basis of assessment"] == "30-day rolling average"
    assert pack["by_id"]["VOL-IV:F4-C/image/decl4"]["reading"]["status"] == "approved"


def test_edge_contact_warning_on_table_2_4(pack):
    rd7 = [c for c in pack["packets"]["VOL-II-p3-r1"]["checks"] if c["check"] == "RD7"]
    assert rd7 and rd7[0]["severity"] == "warning"


# ---------------------------------------------------------------- deliberate reading changes

@pytest.fixture()
def form4c(pack):
    reading, _ = load_readings(ROOT / "curation/readings")["VOL-IV-p6-r1"]
    pdf = pymupdf.open(ROOT / "sources/candidate_pack/VOL-IV_Form_Sheets.pdf")
    return reading, _region(pack, "VOL-IV-p6-r1"), pdf


def _failed(reading, region, pdf, check):
    return [c for c in check_reading(reading, region, pdf) if c["check"] == check and not c["ok"]]


def test_unread_band_is_detected(form4c):
    reading, region, pdf = form4c
    r = Reading.model_validate(copy.deepcopy(reading.model_dump()))
    r.blocks = [b for b in r.blocks if b.key != "decl3"]
    f = _failed(r, region, pdf, "RD4")
    assert f and "(11, 'full')" in f[0]["detail"] and "(12, 'full')" in f[0]["detail"]


def test_missing_translation_is_detected(form4c):
    reading, region, pdf = form4c
    r = Reading.model_validate(copy.deepcopy(reading.model_dump()))
    next(b for b in r.blocks if b.key == "decl4").translation = None
    assert _failed(r, region, pdf, "RD5")


def test_wrong_logical_order_of_numeral_is_detected(form4c):
    """Same characters, swapped logical order: renders as the opposite of what the crop shows."""
    reading, region, pdf = form4c
    r = Reading.model_validate(copy.deepcopy(reading.model_dump()))
    line = next(b for b in r.blocks if b.key == "decl5").lines[0]
    line.source = line.source.replace("٤-٢", "٢-٤")
    line.numerals[0].text = "٢-٤"
    assert _failed(r, region, pdf, "RD6")


def test_presentation_forms_are_rejected(form4c):
    reading, region, pdf = form4c
    r = Reading.model_validate(copy.deepcopy(reading.model_dump()))
    next(b for b in r.blocks if b.key == "title").lines[0].source = "ﺇﻗﺮﺍﺭ"   # visual glyph forms
    assert _failed(r, region, pdf, "RD5")


def test_approval_is_pinned_to_content(form4c, pack):
    reading, region, _ = form4c
    doc_sha = next(d.doc.sha256 for d in pack["pack"].docs if d.doc.doc_id == "VOL-IV")
    subj = review_subject(reading, region, doc_sha)
    approvals = [{"region_id": reading.region_id, "reviewer": "Test Reviewer", "date": "2026-10-02",
                  "subject_sha256": subj["sha256"]}]
    assert review_status(reading, approvals, subj)["status"] == "approved"
    changed = Reading.model_validate(copy.deepcopy(reading.model_dump()))
    changed.blocks[0].lines[0].source += " x"
    st = review_status(changed, approvals, review_subject(changed, region, doc_sha))
    assert st["status"] == "pending" and "changed after" in st["reason"]
    old_style = [{"region_id": reading.region_id, "reviewer": "Test Reviewer", "content_sha256": "x" * 64}]
    assert review_status(reading, old_style, subj)["status"] == "pending"


def test_bidi_render_oracle():
    """UAX #9: in an RTL paragraph, Arabic-Indic digits are AN; a hyphen between them is ES/ON and does not
    join them into one run, so logical ٤-٢ is displayed ٢-٤. A dot (CS) does join: ٤.٢ stays ٤.٢."""
    assert arabic.visual_numeral_runs("البند ٤-٢ من") == ["٢-٤"]
    assert arabic.visual_numeral_runs("البند ٤.٢ من") == ["٤.٢"]


def test_arabic_normalization_is_for_matching_only():
    src = "أولاً: في البند ٤-٢ من أعضاء الائتلاف"
    norm = normalize_arabic(src)
    assert "ً" not in norm and "أ" not in norm and "4-2" in norm
    assert "ة" in normalize_arabic("الهيئة")           # ta marbuta is not folded
    assert src == "أولاً: في البند ٤-٢ من أعضاء الائتلاف"  # source untouched
