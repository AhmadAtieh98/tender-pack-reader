"""Regression tests for the owner's Stage 1 review (session 03).

Written BEFORE the fixes and run against commit 79ef49c to confirm each failure (see the session 03 log).
Synthetic inputs are built in pytest's temporary directories; nothing here writes to the repository.
"""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pymupdf
import pytest
import yaml

import make_fixture as mf
from conftest import ROOT
from tenderpack.cli import ingest
from guards import only_owner_approvals


# ----------------------------------------------------------------------------- helpers

def mini_pack(d: Path, build_pages, rules=("FOOTER-PAGE",)) -> Path:
    """A one-document pack in a disposable directory. Returns the pack.yaml path."""
    d.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open()
    build_pages(doc)
    pdf = d / "T-01.pdf"
    doc.save(pdf)
    (d / "manifest.json").write_text(json.dumps({"files": [{"path": pdf.as_posix(), "pages": doc.page_count,
                                                            "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest()}]}))
    furn = yaml.safe_load((ROOT / "config/furniture.yaml").read_text(encoding="utf-8"))
    furn["rules"] = [r for r in furn["rules"] if r["id"] in rules]
    (d / "furniture.yaml").write_text(yaml.safe_dump(furn, allow_unicode=True))
    (d / "pack.yaml").write_text(yaml.safe_dump({
        "pack_id": d.name, "manifest": (d / "manifest.json").as_posix(), "furniture": (d / "furniture.yaml").as_posix(),
        "readings_dir": (d / "readings").as_posix(), "approvals": (d / "approvals.yaml").as_posix(),
        "documents": [{"doc_id": "T-01", "kind": "volume", "path": pdf.as_posix()}]}))
    return d / "pack.yaml"


def failing(res) -> set[str]:
    return {c["id"] for c in res["coverage"]["checks"] if not c["ok"]}


def text_page(doc):
    return doc.new_page(width=595, height=842)


def two_clauses_same_number(doc):
    p = text_page(doc)
    mf.clause(p, 100, "1.1", "First clause with this number.")
    mf.clause(p, 130, "1.1", "Second clause with the same number.")


# ============================================================================ 1. boundaries

def test_number_at_line_start_inside_a_sentence_stays_in_the_clause(pack):
    u = pack["by_id"]["VOL-I:3.3"]
    assert "under Section 5. A Bidder that resolves such a conflict unilaterally" in u["normalized"]
    assert not [k for k in pack["by_id"] if k.startswith("VOL-I:S3/item")]


def test_genuine_numbered_paragraphs_still_split(pack):
    for form, n in (("VOL-IV:F4-A", 6), ("VOL-IV:F4-D", 3)):
        for i in range(1, n + 1):
            assert pack["by_id"][f"{form}/item{i}"]["kind"] == "numbered_paragraph"


def test_synthetic_wrapped_number_vs_numbered_list(tmp_path):
    def pages(doc):
        p = text_page(doc)
        p.insert_text((62.7, 100), "1.1", fontname="tibo", fontsize=9.6)
        p.insert_text((88.0, 100), "The Bidder shall comply with the rules in Clause", fontname="tiro", fontsize=9.6)
        p.insert_text((88.0, 112), "1. All other terms of the documents apply.", fontname="tiro", fontsize=9.6)
        p.insert_text((62.7, 160), "To: The Authority", fontname="tiro", fontsize=9.6)
        p.insert_text((62.7, 180), "1. We confirm the first point.", fontname="tiro", fontsize=9.6)
        p.insert_text((62.7, 195), "2. We confirm the second point.", fontname="tiro", fontsize=9.6)
    res = ingest(mini_pack(tmp_path / "num", pages), tmp_path / "out", ROOT, quiet=True)
    by = {u["unit_id"]: u for u in res["units"]}
    assert "Clause 1. All other terms" in by["T-01:1.1"]["normalized"]
    items = [u["text"] for u in res["units"] if u["kind"] == "numbered_paragraph"]
    assert items == ["1. We confirm the first point.", "2. We confirm the second point."]


@pytest.mark.parametrize("header", [["Ref", "Item", "Value"], None])
def test_tables_separated_by_content_are_not_merged(tmp_path, header):
    def pages(doc):
        p = text_page(doc)
        mf.ruled_table(p, 71, 600, [80, 220, 80], [["1", "Alpha", "10"], ["2", "Beta", "20"]], header=header)
        p.insert_text((62.7, 700), "SECTION 2 - SOMETHING ELSE", fontname="hebo", fontsize=13)
        p.insert_text((62.7, 730), "Unrelated text between the tables.", fontname="tiro", fontsize=9.6)
        p = text_page(doc)
        mf.ruled_table(p, 71, 68, [80, 220, 80], [["7", "Gamma", "70"], ["8", "Delta", "80"]], header=header)
    res = ingest(mini_pack(tmp_path / "t", pages), tmp_path / "out", ROOT, quiet=True)
    tables = [u for u in res["units"] if u["kind"] == "table"]
    assert len(tables) == 2 and all(len(t["pages"]) == 1 for t in tables)


def test_genuine_split_table_still_joins(tmp_path):
    def pages(doc):
        p = text_page(doc)
        p.insert_text((62.7, 600), "Some text before the table.", fontname="tiro", fontsize=9.6)
        mf.ruled_table(p, 71, 700, [80, 220, 80], [["1", "Alpha", "10"], ["2", "Beta", "20"]], header=["Ref", "Item", "Value"])
        p = text_page(doc)
        mf.ruled_table(p, 71, 68, [80, 220, 80], [["3", "Gamma", "30"]], header=["Ref", "Item", "Value"])
        p.insert_text((62.7, 200), "Text after the table.", fontname="tiro", fontsize=9.6)
    res = ingest(mini_pack(tmp_path / "t", pages), tmp_path / "out", ROOT, quiet=True)
    tables = [u for u in res["units"] if u["kind"] == "table"]
    assert len(tables) == 1 and tables[0]["pages"] == [1, 2] and len(tables[0]["children"]) == 3


# ============================================================================ 2. structural failures

def test_duplicate_clause_ids_fail_with_nonzero_exit(tmp_path):
    pack = mini_pack(tmp_path / "dup", two_clauses_same_number)
    r = subprocess.run([sys.executable, "-m", "tenderpack", "ingest", "--pack", str(pack), "--out", str(tmp_path / "out")],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 2, r.stdout + r.stderr
    assert "STRUCTURAL FAILURE" in r.stdout and "C07" in r.stdout


def test_span_in_two_units_fails(tmp_path, monkeypatch):
    import tenderpack.segment as seg
    orig = seg.Segmenter.run

    def run(self):
        units = orig(self)
        ids = [u for u in self.order if units[u].anchors and units[u].anchors[0]["spans"]]
        units[ids[1]].anchors[0]["spans"].append(units[ids[0]].anchors[0]["spans"][0])
        return units
    monkeypatch.setattr(seg.Segmenter, "run", run)
    def pages(doc):
        p = text_page(doc)
        mf.clause(p, 100, "1.1", "One.")
        mf.clause(p, 130, "1.2", "Two.")
    res = ingest(mini_pack(tmp_path / "a", pages), tmp_path / "out", ROOT, quiet=True)
    assert "C08" in failing(res) and res["status"] == "structural_failure"


@pytest.mark.parametrize("field", ["text", "normalized", "both"])   # split per field after mutation M4 survived
def test_altered_unit_text_fails_full_evidence_check(tmp_path, monkeypatch, field):
    import tenderpack.segment as seg
    orig = seg.Segmenter.run

    def run(self):
        units = orig(self)
        u = units["T-01:1.1"]
        fake = u.text.split()[0] + " invented words that are not on the page"
        if field in ("text", "both"):
            u.text = fake
        if field in ("normalized", "both"):
            u.normalized = fake
        return units
    monkeypatch.setattr(seg.Segmenter, "run", run)
    pack = mini_pack(tmp_path / "e", lambda doc: mf.clause(text_page(doc), 100, "1.1", "The real clause text."))
    res = ingest(pack, tmp_path / "out", ROOT, quiet=True)
    assert "C10" in failing(res)


def test_altered_table_cell_fails_full_evidence_check(tmp_path, monkeypatch):   # added after mutation M4c survived
    import tenderpack.segment as seg
    orig = seg.Segmenter.run

    def run(self):
        units = orig(self)
        row = next(u for u in units.values() if u.kind == "table_row")
        col = next(iter(row.cells))
        row.text = row.text.replace(f"{col}: {row.cells[col]}", f"{col}: {row.cells[col]}9")
        row.cells[col] = row.cells[col] + "9"           # one invented digit, consistent in cells and row text
        return units
    monkeypatch.setattr(seg.Segmenter, "run", run)
    pack = mini_pack(tmp_path / "c", lambda doc: mf.ruled_table(text_page(doc), 71, 100, [80, 220, 80],
                                                                 [["1", "Alpha", "10"]], header=["Ref", "Item", "Value"]))
    assert "C10" in failing(ingest(pack, tmp_path / "out", ROOT, quiet=True))


def test_real_pack_passes_full_evidence_check(pack):
    c10 = next(c for c in pack["coverage"]["checks"] if c["id"] == "C10")
    assert c10["ok"], c10["detail"]
    assert pack["coverage"]["evidence"]["units_checked"] > 400


def test_real_pack_exit_codes_separate_structure_from_pending_review(tmp_path, pending):
    # without approvals (the disposable no-approval pack): structure OK (0) but the approval gate refuses (3)
    r = subprocess.run([sys.executable, "-m", "tenderpack", "ingest", "--pack", str(pending["pack"]), "--out", str(tmp_path / "b")],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0 and "PENDING HUMAN REVIEW" in r.stdout, r.stdout + r.stderr
    r = subprocess.run([sys.executable, "-m", "tenderpack", "ingest", "--pack", str(pending["pack"]), "--out", str(tmp_path / "b"),
                        "--require-approved"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 3, r.stdout + r.stderr
    # the real pack, with the owner's two confirmations (3 Oct 2026): the reading gate opens (rows and ops are separate)
    r = subprocess.run([sys.executable, "-m", "tenderpack", "ingest", "--out", str(tmp_path / "c"), "--require-approved"],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0 and "PENDING HUMAN REVIEW: none" in r.stdout, r.stdout + r.stderr


# ============================================================================ 3. approvals

@pytest.fixture()
def t24(pack):
    from tenderpack.readings import load_readings
    reading, _ = load_readings(ROOT / "curation/readings")["VOL-II-p3-r1"]
    region = next(g for d in pack["pack"].docs for g in d.regions if g.region_id == "VOL-II-p3-r1")
    doc_sha = next(d.doc.sha256 for d in pack["pack"].docs if d.doc.doc_id == "VOL-II")
    return reading, region, doc_sha


def _approval(subject, reviewer="Reviewer Name"):
    return [{"region_id": "VOL-II-p3-r1", "reviewer": reviewer, "date": "2026-10-02", "subject_sha256": subject["sha256"]}]


def test_approval_requires_identified_reviewer(t24):
    from tenderpack.readings import review_status, review_subject
    reading, region, doc_sha = t24
    subj = review_subject(reading, region, doc_sha)
    assert review_status(reading, _approval(subj), subj)["status"] == "approved"
    for who in (None, "", "<name>"):
        st = review_status(reading, _approval(subj, who), subj)
        assert st["status"] == "pending" and "reviewer" in st["reason"]


def test_changed_evidence_requires_review_again(t24):
    from tenderpack.readings import review_status, review_subject
    reading, region, doc_sha = t24
    approvals = _approval(review_subject(reading, region, doc_sha))
    region2 = copy.deepcopy(region)
    region2.native = dict(region.native, sha256="1" * 64)          # image replaced ...
    reading2 = reading.model_copy(deep=True)
    reading2.source.native_sha256 = "1" * 64                         # ... and the reading's hash updated to match
    assert review_status(reading2, approvals, review_subject(reading2, region2, doc_sha))["status"] == "pending"
    moved = reading.model_copy(deep=True)
    moved.source.bbox_pt = [0.0, 0.0, 10.0, 10.0]
    assert review_status(moved, approvals, review_subject(moved, region, doc_sha))["status"] == "pending"
    assert review_status(reading, approvals, review_subject(reading, region, "2" * 64))["status"] == "pending"


def test_added_uncertainty_requires_review_again(t24):
    from tenderpack.readings import review_status, review_subject
    reading, region, doc_sha = t24
    approvals = _approval(review_subject(reading, region, doc_sha))
    r2 = reading.model_copy(deep=True)
    r2.uncertainties.append("new doubt about a value")
    assert review_status(r2, approvals, review_subject(r2, region, doc_sha))["status"] == "pending"


def test_approve_command_refuses_placeholder_reviewer(tmp_path):
    r = subprocess.run([sys.executable, "-m", "tenderpack", "approve", "VOL-II-p3-r1", "--reviewer", "<name>",
                        "--approvals", str(tmp_path / "approvals.yaml")], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode != 0 and not (tmp_path / "approvals.yaml").exists()


def test_nothing_is_approved_on_the_owners_behalf():
    assert only_owner_approvals()


# ============================================================================ 4. table readings

def _t24_failures(t24, mutate):
    from tenderpack.readings import check_reading
    reading, region, _ = t24
    r = reading.model_copy(deep=True)
    mutate(r)
    pdf = pymupdf.open(ROOT / "sources/candidate_pack/VOL-II_Technical_Requirements.pdf")
    return [c for c in check_reading(r, region, pdf) if not c["ok"]]


def test_missing_cells_fail(t24):
    def m(r):
        tn = next(x for x in r.table.rows if x.key == "TN")
        del tn.cells["unit"], tn.cells["basis"]
    f = _t24_failures(t24, m)
    assert any(c["check"] == "RD8" and "TN" in c["detail"] and "unit" in c["detail"] for c in f)


def test_duplicate_row_key_fails(t24):
    f = _t24_failures(t24, lambda r: setattr(r.table.rows[1], "key", r.table.rows[0].key))
    assert any(c["check"] == "RD8" and "duplicate" in c["detail"] for c in f)


def test_blank_cell_must_be_declared(t24):
    def m(r):
        r.table.rows[0].cells["basis"] = ""
    assert any(c["check"] == "RD8" and "blank" in c["detail"] for c in _t24_failures(t24, m))


def test_unknown_cell_key_fails(t24):
    def m(r):
        r.table.rows[0].cells["colour"] = "x"
    assert any(c["check"] == "RD8" and "colour" in c["detail"] for c in _t24_failures(t24, m))


def test_numeric_reading_carries_no_meaning(pack):
    from tenderpack.readings import numeric_reading
    assert numeric_reading("10") == {"form": "single", "values": [10.0], "text": "10"}
    assert numeric_reading("0.5 - 1.0") == {"form": "range", "values": [0.5, 1.0], "text": "0.5 - 1.0"}
    tn = pack["by_id"]["VOL-II:T2-4/TN"]
    assert "parsed" not in tn
    assert tn["numeric"]["Limit"] == {"form": "single", "values": [5.0], "text": "5"}
    assert tn["context"]["interpretation"] is None
    assert "all values are maxima" in tn["context"]["qualifier"]


# ============================================================================ 5. drawings and Arabic image tables

def _regions_of(page):
    from tenderpack.extract import FurnitureRules, extract_page
    from tenderpack.regions import detect_regions
    return detect_regions("T", page, extract_page("T", page, FurnitureRules({"rules": []})))


def test_straight_line_triangle_is_a_region():
    doc = pymupdf.open()
    p = text_page(doc)
    p.draw_polyline([(50, 250), (150, 60), (250, 250), (50, 250)], color=(0, 0, 0), width=1.5)
    assert [g.kind for g in _regions_of(p)] == ["vector_graphic"]


def test_dark_box_without_text_is_a_region_but_header_fill_is_not():
    doc = pymupdf.open()
    p = text_page(doc)
    p.draw_rect(pymupdf.Rect(60, 100, 240, 140), color=None, fill=(0, 0, 0))
    mf.ruled_table(p, 71, 400, [80, 220, 80], [["1", "Alpha", "10"]], header=["Ref", "Item", "Value"])
    regs = _regions_of(p)
    assert [(g.kind, g.bbox[1] < 200) for g in regs] == [("vector_graphic", True)]


def test_arabic_rtl_image_table_end_to_end(synthetic):
    by = synthetic["by_id"]
    pk = synthetic["packets"]["SYN-01-p4-r1"]
    assert pk["status"] == "pending"
    assert all(c["ok"] for c in pk["checks"]), [c for c in pk["checks"] if not c["ok"]]
    # transcription kept as typed, with Arabic headings, explicit blank, and the mixed-numeral cells
    noise = by["SYN-01:T-AR-1/noise"]
    assert noise["cells"] == {"البند": "الضوضاء ليلاً", "الحد": "45 dB(A)", "ملاحظة": "من ٢٢:٠٠-٠٦:٠٠"}
    assert by["SYN-01:T-AR-1/ph"]["blank"] == ["ملاحظة"]
    # right-to-left layout: the first logical column is the rightmost cell crop on the page
    xs = [noise["anchors"][0]["cell_bbox_pt"][h][0] for h in ("البند", "الحد", "ملاحظة")]
    assert xs[0] > xs[1] > xs[2]
    # rendering: every declared numeral renders in the order seen in the image
    nums = [n for n in pk["numerals"]]
    assert len(nums) == 4 and all(n["render_check"]["ok"] for n in nums)
    assert pk["compare"] and all((synthetic["out"] / c).exists() for c in pk["compare"])


def test_arabic_rtl_table_wrong_logical_order_fails(synthetic):
    from tenderpack.readings import check_reading, load_readings
    reading, _ = load_readings(synthetic["src"] / "readings")["SYN-01-p4-r1"]
    region = next(g for d in synthetic["pack"].docs for g in d.regions if g.region_id == "SYN-01-p4-r1")
    pdf = pymupdf.open(synthetic["src"] / "SYN-01_Synthetic_Test_Volume.pdf")
    r = reading.model_copy(deep=True)
    row = next(x for x in r.table.rows if x.key == "noise")
    row.cells["note"] = "من ٠٦:٠٠-٢٢:٠٠"                    # same characters, logical order swapped
    row.numerals[1].text = "٠٦:٠٠-٢٢:٠٠"
    assert any(c["check"] == "RD6" and not c["ok"] for c in check_reading(r, region, pdf))
    r2 = reading.model_copy(deep=True)
    del next(x for x in r2.table.rows if x.key == "samples").cells["note"]
    assert any(c["check"] == "RD8" and not c["ok"] for c in check_reading(r2, region, pdf))


def test_unread_region_is_a_structural_failure(tmp_path):
    def pages(doc):
        p = text_page(doc)
        p.draw_polyline([(50, 250), (150, 60), (250, 250), (50, 250)], color=(0, 0, 0), width=1.5)
    res = ingest(mini_pack(tmp_path / "g", pages), tmp_path / "out", ROOT, quiet=True)
    assert "C05" in failing(res) and res["status"] == "structural_failure"


# ============================================================================ 6. output safety

@pytest.fixture()
def fake_repo(tmp_path):
    """A disposable stand-in for the repository, with inputs and a sentinel file."""
    repo = tmp_path / "repo"
    pack = mini_pack(repo / "inputs", lambda doc: mf.clause(text_page(doc), 100, "1.1", "Text."))
    (repo / "sources").mkdir()
    (repo / "keep.txt").write_text("must survive")
    return repo, pack


@pytest.mark.parametrize("target", ["repo", "parent", "inputs", "sources"])
def test_unsafe_output_paths_are_refused(fake_repo, target):
    from tenderpack.cli import UnsafeOutputError
    repo, pack = fake_repo
    out = {"repo": repo, "parent": repo.parent, "inputs": repo / "inputs", "sources": repo / "sources"}[target]
    with pytest.raises(UnsafeOutputError):
        ingest(pack, out, repo, quiet=True)
    assert (repo / "keep.txt").read_text() == "must survive" and (repo / "inputs/pack.yaml").exists()


def test_existing_non_build_directory_is_refused(fake_repo, tmp_path):
    from tenderpack.cli import UnsafeOutputError
    repo, pack = fake_repo
    other = tmp_path / "notes"
    other.mkdir()
    (other / "mine.txt").write_text("x")
    with pytest.raises(UnsafeOutputError):
        ingest(pack, other, repo, quiet=True)
    assert (other / "mine.txt").exists()


def test_failed_build_keeps_previous_results(fake_repo, monkeypatch):
    import tenderpack.cli as cli
    repo, pack = fake_repo
    out = repo / "build"
    ingest(pack, out, repo, quiet=True)
    before = (out / "units.json").read_bytes()
    monkeypatch.setattr(cli, "run_pack", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("simulated failure")))
    with pytest.raises(RuntimeError):
        cli.ingest(pack, out, repo, quiet=True)
    assert (out / "units.json").read_bytes() == before
    assert not [p for p in out.parent.iterdir() if p.name.startswith(".build.")]   # no temporary leftovers


def test_structural_failure_keeps_previous_results(fake_repo):
    repo, pack = fake_repo
    out = repo / "build"
    ingest(pack, out, repo, quiet=True)
    before = (out / "units.json").read_bytes()
    bad = mini_pack(repo / "inputs-bad", two_clauses_same_number)
    res = ingest(bad, out, repo, quiet=True)
    assert res["status"] == "structural_failure"
    assert (out / "units.json").read_bytes() == before
    assert (repo / "build.failed" / "coverage.md").exists()


def test_successful_build_replaces_previous(fake_repo):
    repo, pack = fake_repo
    out = repo / "build"
    ingest(pack, out, repo, quiet=True)
    (out / "stale.txt").write_text("from an old build")
    res = ingest(pack, out, repo, quiet=True)
    assert res["status"] == "ok" and not (out / "stale.txt").exists() and (out / ".tenderpack-build").exists()


# ============================================================================ added after the failing-first run
# These two were written while fixing, not before; they are recorded as such in the session 03 log.

def test_arabic_rtl_table_matches_what_was_drawn(synthetic):
    """Independent oracle: the fixture records, from the vector page it rasterised, where each cell was drawn and
    the left-to-right order of its digit/Latin glyphs. The reading's column mapping and declared visual orders must
    agree with that, not just with UAX #9 reasoning."""
    cells = synthetic["expected"]["p4"]["rtl_cells"]
    from tenderpack.readings import load_readings
    reading, _ = load_readings(synthetic["src"] / "readings")["SYN-01-p4-r1"]
    heading = {c.key: c.heading for c in reading.table.columns}
    for row in reading.table.rows:
        unit = synthetic["by_id"][f"SYN-01:T-AR-1/{row.key}"]
        for key, drawn in cells[row.key].items():
            x0, y0, x1, y1 = unit["anchors"][0]["cell_bbox_pt"][heading[key]]
            cx, cy = drawn["centre_pt"]
            assert x0 <= cx <= x1 and y0 <= cy <= y1, (row.key, key)
        for n in row.numerals:
            assert n.visual_ltr_expected == cells[row.key][n.column]["drawn_visual_ltr"], (row.key, n.column)


def test_thin_filled_border_rects_are_structure():
    """Table borders drawn as thin filled black boxes (common in generated PDFs) are rules, not drawings."""
    doc = pymupdf.open()
    p = text_page(doc)
    for x in (60, 200, 340):
        p.draw_rect(pymupdf.Rect(x, 100, x + 1, 300), color=None, fill=(0, 0, 0))
    for y in (100, 200, 300):
        p.draw_rect(pymupdf.Rect(60, y, 341, y + 1), color=None, fill=(0, 0, 0))
    assert _regions_of(p) == []


def test_approve_command_end_to_end_on_disposable_fixture(tmp_path):
    """The approve command on a disposable copy of the synthetic fixture (never the owner's pack): a named
    reviewer's approval shows as approved; adding an uncertainty afterwards makes the reading pending again."""
    src = tmp_path / "src"
    mf.build(src)
    run = lambda *a: subprocess.run([sys.executable, "-m", "tenderpack", *a], cwd=ROOT, capture_output=True, text=True)
    r = run("approve", "SYN-01-p4-r1", "--reviewer", "Fixture Test Reviewer", "--pack", str(src / "pack.yaml"))
    assert r.returncode == 0, r.stdout + r.stderr
    entry = yaml.safe_load((src / "approvals.yaml").read_text(encoding="utf-8"))["approvals"][0]
    assert entry["reviewer"] == "Fixture Test Reviewer" and len(entry["subject_sha256"]) == 64
    res = ingest(src / "pack.yaml", tmp_path / "out", ROOT, quiet=True)
    assert res["packets"]["SYN-01-p4-r1"]["status"] == "approved"
    assert res["packets"]["SYN-01-p4-r2"]["status"] == "pending"            # only what was approved
    rp = src / "readings/SYN-01-p4-r1.yaml"
    data = yaml.safe_load(rp.read_text(encoding="utf-8"))
    data["uncertainties"] = ["a new doubt"]
    rp.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    res = ingest(src / "pack.yaml", tmp_path / "out", ROOT, quiet=True)
    assert res["packets"]["SYN-01-p4-r1"]["status"] == "pending"
