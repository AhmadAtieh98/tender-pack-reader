"""Regression tests for the owner's second review (session 04).

Written BEFORE the fixes and run against commit cb8ff13 to confirm each failure (see the session 04 log).
Mutations are applied to in-memory copies or to disposable fixture copies; nothing writes to the repository.
"""
from __future__ import annotations

import copy
import subprocess
import sys

import pymupdf
import pytest
import yaml

import make_fixture as mf
from conftest import ROOT
from tenderpack.cli import ingest
from tenderpack.coverage import full_evidence


def _doc(pack, doc_id):
    return next(d for d in pack["pack"].docs if d.doc.doc_id == doc_id)


def _evidence_failures(pack, doc_id, mutate) -> list[dict]:
    d = copy.deepcopy(_doc(pack, doc_id))
    mutate(d.units)
    return full_evidence(d, pack["pack"].rules)["failures"]


def _failing(res) -> set[str]:
    return {c["id"] for c in res["coverage"]["checks"] if not c["ok"]}


# ============================================================================ 1. evidence checks

ROW = "VOL-II:T2-6/2-6.1"           # Average daily flow | 120,000 | m³/day


def test_reordered_digits_in_a_cell_fail(pack):
    """120,000 -> 210,000 has the same characters; the cell, row text and matching text are changed consistently."""
    def m(units):
        u = units[ROW]
        u.cells["Value"] = "210,000"
        u.text = u.text.replace("120,000", "210,000")
        u.normalized = u.normalized.replace("120,000", "210,000")
    assert ROW in [f["unit"] for f in _evidence_failures(pack, "VOL-II", m)]


def test_text_moved_between_columns_fails(pack):
    def m(units):
        u = units[ROW]
        u.cells["Criterion"], u.cells["Unit"] = u.cells["Unit"], u.cells["Criterion"]
        u.text = " | ".join(f"{k}: {v}" for k, v in u.cells.items() if v)
    assert ROW in [f["unit"] for f in _evidence_failures(pack, "VOL-II", m)]


def test_reordered_digits_in_displayed_cell_only_fail(pack):   # added after mutation R1a survived
    """Cell and row text changed, matching text left correct: only the per-cell comparison can catch it."""
    def m(units):
        u = units[ROW]
        u.cells["Value"] = "210,000"
        u.text = u.text.replace("120,000", "210,000")
    assert ROW in [f["unit"] for f in _evidence_failures(pack, "VOL-II", m)]


def test_cell_spans_moved_to_another_column_fail(pack):         # added after mutation R1b survived
    """Values AND their spans moved between columns, texts rebuilt consistently: only the geometry can tell."""
    def m(units):
        u = units[ROW]
        for d in (u.cells, u.cell_spans):
            d["Criterion"], d["Unit"] = d["Unit"], d["Criterion"]
        u.text = " | ".join(f"{k}: {u.cells[k]}" for k in ("Ref", "Criterion", "Value", "Unit"))
        u.normalized = "Ref: 2-6.1 | Criterion: m3/day | Value: 120,000 | Unit: Average daily flow"
    assert ROW in [f["unit"] for f in _evidence_failures(pack, "VOL-II", m)]


def test_changed_normalized_table_text_fails(pack):
    def m(units):
        units[ROW].normalized = units[ROW].normalized.replace("120,000", "125,000")
    assert ROW in [f["unit"] for f in _evidence_failures(pack, "VOL-II", m)]


@pytest.mark.parametrize("what", ["page", "bbox"])
def test_wrong_anchor_page_or_geometry_fails_with_unchanged_span_ids(pack, what):
    def m(units):
        a = units["VOL-II:2.1"].anchors[0]
        if what == "page":
            a["page"] = a["page"] + 1
        else:
            a["bbox"] = [a["bbox"][0], a["bbox"][1] + 40, a["bbox"][2], a["bbox"][3] + 40]
    assert "VOL-II:2.1" in [f["unit"] for f in _evidence_failures(pack, "VOL-II", m)]


def test_span_order_within_an_anchor_is_checked(pack):
    """Same spans, same characters, different order: text and span list permuted together."""
    def m(units):
        u = units["VOL-II:2.1"]
        sp = u.anchors[0]["spans"]
        sp[0], sp[1] = sp[1], sp[0]
        pg = pymupdf.open(ROOT / "sources/candidate_pack/VOL-II_Technical_Requirements.pdf")  # noqa: F841
    fails = _evidence_failures(pack, "VOL-II", m)
    assert "VOL-II:2.1" in [f["unit"] for f in fails]


@pytest.fixture()
def fixture_src(tmp_path):
    src = tmp_path / "src"
    mf.build(src)
    return src


@pytest.mark.parametrize("what", ["crop", "page"])
def test_wrong_reading_crop_or_page_reference_fails(fixture_src, tmp_path, monkeypatch, what):
    import tenderpack.cli as cli
    orig = cli.reading_units

    def swapped(reading, region, status, ev):
        units = orig(reading, region, status, ev)
        rows = [u for u in units if u["kind"] == "table_row"]
        if len(rows) >= 2:
            if what == "crop":
                rows[0]["anchors"][0]["crop"], rows[1]["anchors"][0]["crop"] = \
                    rows[1]["anchors"][0]["crop"], rows[0]["anchors"][0]["crop"]
            else:
                rows[0]["anchors"][0]["page"] = rows[0]["anchors"][0]["page"] + 1
        return units
    monkeypatch.setattr(cli, "reading_units", swapped)
    res = ingest(fixture_src / "pack.yaml", tmp_path / "out", ROOT, quiet=True)
    assert "C10" in _failing(res)


# ============================================================================ 2. Latin expressions in Arabic layout

def test_fixture_source_renders_the_latin_expression_correctly(synthetic):
    """The fixture's image is a correctly rendered source: '45 dB(A)' reads left to right inside the RTL cell."""
    assert synthetic["expected"]["p4"]["rtl_cells"]["noise"]["limit"]["drawn_visual_ltr"] == "45 dB(A)"


def test_reading_keeps_raw_transcription_and_renders_it_correctly(synthetic):
    from tenderpack.arabic import storage_problems
    from tenderpack.readings import load_readings
    reading, _ = load_readings(synthetic["src"] / "readings")["SYN-01-p4-r1"]
    noise = next(r for r in reading.table.rows if r.key == "noise")
    assert noise.cells["limit"] == "45 dB(A)" and not storage_problems(noise.cells["limit"])   # raw text, no controls
    n = next(x for x in noise.numerals if x.column == "limit")
    assert n.visual_ltr_expected == "45 dB(A)"
    pk = synthetic["packets"]["SYN-01-p4-r1"]
    rd6 = [c for c in pk["checks"] if c["check"] == "RD6" and "cell limit" in c["detail"] and "noise" in c["detail"]]
    assert rd6 and all(c["ok"] and c.get("result", "pass") == "pass" for c in rd6)


def test_scrambled_latin_expression_is_rejected(synthetic):
    from tenderpack.readings import check_reading, load_readings
    reading, _ = load_readings(synthetic["src"] / "readings")["SYN-01-p4-r1"]
    region = next(g for d in synthetic["pack"].docs for g in d.regions if g.region_id == "SYN-01-p4-r1")
    pdf = pymupdf.open(synthetic["src"] / "SYN-01_Synthetic_Test_Volume.pdf")
    r = reading.model_copy(deep=True)
    next(x for x in next(x for x in r.table.rows if x.key == "noise").numerals if x.column == "limit") \
        .visual_ltr_expected = "(dB(A 45"
    assert any(c["check"] == "RD6" and not c["ok"] for c in check_reading(r, region, pdf))


def test_digits_only_verification_is_labelled_partial():
    """Corrected after the failing-first run (see the session 04 log): the first version used a Latin-letter
    mismatch ('dB(X)'), which is verifiable and must FAIL; PARTIAL is for tokens whose Arabic letters cannot be
    read back from the renderer, so only digits/punctuation are verified."""
    from tenderpack.arabic import visual_check
    res, how = visual_check("في البند ٤-٢ من المجلد", "٢-٤ دنبلا")   # Arabic letter order wrong, digits right
    assert res == "partial" and "partial" in how.lower()
    assert visual_check("القيمة 45 dB(A) تقريباً", "45 dB(X)")[0] == "fail"   # Latin letters are verifiable
    assert visual_check("القيمة 45 dB(A) تقريباً", "45 dB(A)")[0] == "pass"


# ============================================================================ 3. --require-approved gate

def test_require_approved_rejects_before_publishing(fixture_src, tmp_path):
    out = tmp_path / "build"
    run = lambda *a: subprocess.run([sys.executable, "-m", "tenderpack", "ingest", "--pack", str(fixture_src / "pack.yaml"),  # noqa: E731
                                     "--out", str(out), *a], cwd=ROOT, capture_output=True, text=True)
    r = run()
    assert r.returncode == 0, r.stdout + r.stderr
    before = (out / "units.json").read_bytes()
    (out / "previous-build-sentinel.txt").write_text("from the previous build")
    r = run("--require-approved")
    assert r.returncode == 3, r.stdout + r.stderr
    assert (out / "previous-build-sentinel.txt").exists() and (out / "units.json").read_bytes() == before
    rejected = tmp_path / "build.rejected"
    assert (rejected / "units.json").exists() and "pending" in (rejected / "REJECTED.md").read_text().lower()
    assert not [p for p in tmp_path.iterdir() if ".building-" in p.name or ".old-" in p.name]


def test_require_approved_on_first_build_publishes_nothing(fixture_src, tmp_path):
    out = tmp_path / "build"
    r = subprocess.run([sys.executable, "-m", "tenderpack", "ingest", "--pack", str(fixture_src / "pack.yaml"),
                        "--out", str(out), "--require-approved"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 3 and not out.exists() and (tmp_path / "build.rejected" / "units.json").exists()


def test_gate_passes_when_everything_is_approved(fixture_src, tmp_path):
    """With every reading approved (disposable fixture copy, test reviewer name), the gate publishes."""
    run = lambda *a: subprocess.run([sys.executable, "-m", "tenderpack", *a], cwd=ROOT, capture_output=True, text=True)  # noqa: E731
    for rid in sorted(p.stem for p in (fixture_src / "readings").glob("*.yaml")):
        r = run("approve", rid, "--reviewer", "Fixture Test Reviewer", "--pack", str(fixture_src / "pack.yaml"))
        assert r.returncode == 0, r.stdout
    r = run("ingest", "--pack", str(fixture_src / "pack.yaml"), "--out", str(tmp_path / "b"), "--require-approved")
    assert r.returncode == 0 and (tmp_path / "b" / "units.json").exists(), r.stdout
    assert yaml.safe_load((fixture_src / "approvals.yaml").read_text())["approvals"]
