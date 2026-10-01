"""Reproducible rebuild and traceability from a unit back to its page."""
import json

import pymupdf

from tenderpack.cli import ingest, show

from conftest import ROOT


def test_rebuild_is_byte_identical(pack, tmp_path):
    again = ingest(ROOT / "config/pack.yaml", tmp_path / "b2", ROOT, quiet=True)  # noqa: F841
    a = json.loads((pack["out"] / "BUILD_MANIFEST.json").read_text(encoding="utf-8"))["outputs"]
    b = json.loads((tmp_path / "b2" / "BUILD_MANIFEST.json").read_text(encoding="utf-8"))["outputs"]
    assert a == b      # output paths are relative to the build directory, so they compare directly


def test_text_layer_units_trace_to_their_page(pack):
    """For every text-layer unit, re-extracting the page inside its anchor box finds its words."""
    docs = {d.doc.doc_id: pymupdf.open(d.doc.path) for d in pack["pack"].docs}
    checked = 0
    for u in pack["units"]:
        if u.get("origin", "text_layer") != "text_layer" or not u.get("text") or u["kind"] in ("table", "region"):
            continue
        a = u["anchors"][0]
        page = docs[u["doc"]][a["page"] - 1]
        clip = pymupdf.Rect(a["bbox"]) + (-1, -1, 1, 1)
        words = page.get_text("words", clip=clip)
        if u["kind"] in ("table_row", "form_field"):
            text = next((v for v in (u.get("cells") or {}).values() if v), "")   # headings are added by us
        else:
            text = u["text"]
        if not text:
            continue
        first = text.split()[0].strip("‘’\"'(")[:6]
        assert any(first[:4] in w[4] for w in words), (u["unit_id"], first)
        checked += 1
    assert checked > 300


def test_show_prints_source_and_writes_highlight(pack, capsys):
    assert show("VOL-I:8.5#fn12", pack["out"], ROOT) == 0
    out = capsys.readouterr().out
    assert "page 4" in out and "rejected without further evaluation" in out
    assert (pack["out"] / "show" / "VOL-I_8.5_fn12.png").exists()
