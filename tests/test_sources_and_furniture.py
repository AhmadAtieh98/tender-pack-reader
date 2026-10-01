"""C01 source integrity and C04 furniture exclusion: specific, audited, and never broader than declared."""
import json
import shutil

import pytest

from tenderpack.sources import SourceIntegrityError, load_documents
from tenderpack.util import load_yaml

from conftest import ROOT


def test_sources_match_manifest(golden):
    docs = load_documents(load_yaml(ROOT / "config/pack.yaml"), ROOT)
    assert sum(d.pages for d in docs) == golden["pages_total"]


def test_a_changed_source_is_refused(tmp_path):
    """Deliberate input change: one appended byte must stop the build (curated work is pinned to hashes)."""
    cfg = load_yaml(ROOT / "config/pack.yaml")
    (tmp_path / "sources/candidate_pack").mkdir(parents=True)
    for d in cfg["documents"]:
        shutil.copy(ROOT / d["path"], tmp_path / d["path"])
    shutil.copy(ROOT / cfg["manifest"], tmp_path / cfg["manifest"])
    victim = tmp_path / cfg["documents"][0]["path"]
    victim.write_bytes(victim.read_bytes() + b"\n%tampered\n")
    with pytest.raises(SourceIntegrityError, match="sha256"):
        load_documents(cfg, tmp_path)


def test_one_watermark_per_page_and_nothing_else_rotated(pack, golden):
    cov = pack["coverage"]
    per_page = {}
    for e in cov["exclusions"]:
        if e["rule"] == "WATERMARK":
            per_page[(e["doc"], e["page"])] = per_page.get((e["doc"], e["page"]), 0) + 1
    assert len(per_page) == golden["pages_total"]
    assert set(per_page.values()) == {golden["watermark_per_page"]}
    assert cov["rotated_content"] == []        # in the real pack the only rotated text is the watermark


def test_header_footer_excluded_and_printed_page_matches(pack):
    for p in pack["coverage"]["pages"]:
        assert p["excluded"] == {"FOOTER-DISCLAIMER": 1, "FOOTER-PAGE": 1, "HEADER-REF": 1, "HEADER-TITLE": 1, "WATERMARK": 1}
        assert p["printed_page"] == str(p["page"])


def test_text_resembling_furniture_is_kept(pack, golden):
    """The tender reference is a header pattern, but in body text it is content."""
    for item in golden["kept_as_content"]:
        assert item["contains"] in pack["by_id"][item["unit"]]["text"], item


def test_legitimate_rotated_text_is_content(synthetic):
    rotated = [u for u in synthetic["units"] if u["kind"] == "rotated_text"]
    texts = {u["text"]: u["angle"] for u in rotated}
    assert texts.get(synthetic["expected"]["p1"]["rotated_content"]) == 90.0
    # specificity: identical to the watermark (text, font, size, angle) except dark ink -> NOT excluded
    decoy = [u for u in rotated if u["text"].startswith("FICTIONAL")]
    assert len(decoy) == 1 and decoy[0]["angle"] == 52.0 and decoy[0]["style"]["max_size"] == 34.0
    wm = [e for e in synthetic["coverage"]["exclusions"] if e["rule"] == "WATERMARK"]
    assert len(wm) == synthetic["expected"]["pages"]
    assert all(e["color"] == "#dbdbdb" for e in wm)


def test_exclusion_report_lists_every_excluded_span(pack):
    md = (pack["out"] / "exclusions.md").read_text(encoding="utf-8")
    for e in pack["coverage"]["exclusions"]:
        assert e["span_id"] in md
    data = json.loads((pack["out"] / "coverage.json").read_text(encoding="utf-8"))
    assert len(data["exclusions"]) == 5 * 32
