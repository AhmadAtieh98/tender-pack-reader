"""The archive verifier reads A3's link targets as PDF literal strings (session 08: ids with parentheses)."""
from __future__ import annotations

import importlib.util

import pymupdf

from tenderpack.util import ROOT

spec = importlib.util.spec_from_file_location("verify_archive", ROOT / "scripts/verify_archive.py")
va = importlib.util.module_from_spec(spec)
spec.loader.exec_module(va)


def test_a_link_target_with_parentheses_is_read_whole(tmp_path):
    doc = pymupdf.open()
    page = doc.new_page()
    targets = ["a3_detail.html#I-OP-ADD-02/T1-1-rev/note(2)", "a3_detail.html#VOL-I-6.1-01"]
    for i, t in enumerate(targets):
        page.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(10, 10 + 20 * i, 100, 25 + 20 * i), "uri": t})
    doc.save(tmp_path / "a.pdf")
    got = [va.uri_of(pymupdf.open(tmp_path / "a.pdf").xref_object(ln["xref"]))
           for ln in pymupdf.open(tmp_path / "a.pdf")[0].get_links()]
    assert got == targets
    assert va.uri_of("<< /S /Launch /F (a3_detail.html) >>") is None
