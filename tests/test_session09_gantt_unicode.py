"""Session 09: the A5 Gantt keeps non-ASCII text (Arabic) instead of replacing it with '?'.

SVG and HTML carry the text as written (XML-escaped); the PDF draws it with MuPDF's Story engine (shaped, bidi,
fallback font) wrapped in /ActualText, and plain ASCII text keeps the Base-14 path. A small programme dict in the
shape gantt.layout reads; nothing writes to the repository.
"""
from __future__ import annotations

import unicodedata
from collections import Counter

import pymupdf
import pytest

from tenderpack import gantt

AR_NAME = "إقرار تضارب المصالح والحظر — Form 4-C"
AR_SHORT = "الموعد النهائي لتقديم العروض 11:00"
AR_LABEL = "الموعد النهائي لتقديم العروض، الساعة 11:00 بتوقيت الرياض"


def _act(aid, name, es, ef, ls, lf, env="A", disc="Legal"):
    return {"id": aid, "name": name, "req_ids": ["VOL-IV-4C-01", "VOL-I-8.6-01"], "envelope": env, "discipline": disc,
            "earliest_start": es, "earliest_finish": ef, "latest_start": ls, "latest_finish": lf, "float_wd": 3,
            "status": "OK", "timing_status": "OK", "decision_status": "READY", "resource_status": "OK",
            "resource": "legal_counsel", "count": 1, "duration_wd": 2, "duration_assumption": "form_4c_signature",
            "effort_total_wd": 2, "waiting_on": "", "gated_by": [], "predecessors": []}


def programme(arabic: bool = True) -> dict:
    name = AR_NAME if arabic else "Form 4-C conflict of interest and prohibition - Form 4-C"
    ms = [{"id": "PDD", "date": "2026-11-26", "time": "11:00", "short": AR_SHORT if arabic else "PDD 11:00",
           "label": AR_LABEL if arabic else "Proposal Due Date, 11:00 Riyadh time", "purpose": "deadline",
           "source": "VOL-I:6.1", "kind": "dated", "conditional": False},
          {"id": "PRE-BID", "date": "2026-11-05", "time": "10:00", "short": "Pre-Bid Conference 10:00",
           "label": "Pre-Bid Conference, 10:00", "purpose": "event", "source": "VOL-I:5.4", "kind": "dated",
           "conditional": False}]
    return {"stage": "ADD-03", "status_date": "2026-11-03", "planning_date": "2026-11-03", "start_date": "2026-11-03",
            "planning_basis": "test programme", "calendar": {"weekend": [4, 5], "holidays": []},
            "resources": {"overloads": []}, "milestones": ms,
            "activities": [_act("form-4c", name, "2026-11-04", "2026-11-05", "2026-11-18", "2026-11-19"),
                           _act("deliver", "Deliver both sealed envelopes", "2026-11-08", "2026-11-08", "2026-11-26",
                                "2026-11-26", env="A+B", disc="Document control")]}


def _arabic_letters(s: str) -> Counter:
    return Counter(c for c in s if "\u0600" <= c <= "\u06ff" and unicodedata.category(c).startswith("L"))


@pytest.fixture(scope="module")
def drawn(tmp_path_factory):
    out = tmp_path_factory.mktemp("gantt-unicode")
    gantt.write(programme(), out)
    return out


def test_svg_and_html_keep_the_arabic_as_written(drawn):
    svg = (drawn / "gantt.svg").read_text(encoding="utf-8")
    html = (drawn / "gantt.html").read_text(encoding="utf-8")
    for doc in (svg, html):
        assert AR_NAME in doc and AR_SHORT in doc                       # the row title and the milestone label
        assert "??" not in doc
    assert AR_LABEL in html                                              # the milestones table
    # drawn, not only in a title; a LEFT-TO-RIGHT MARK keeps the appended date out of the right-to-left run
    assert f">{AR_SHORT}\u200e 26 Nov</text>" in svg


def test_pdf_draws_the_arabic_shaped_and_extractable(drawn):
    doc = pymupdf.open(drawn / "gantt.pdf")
    page = doc[0]
    text = unicodedata.normalize("NFKC", page.get_text())
    want = _arabic_letters(AR_SHORT)
    assert want and not (want - _arabic_letters(text)), want - _arabic_letters(text)   # every letter, as a multiset
    assert "?" not in page.get_text()
    fonts = {f[3] for f in page.get_fonts(full=True)}
    assert any("Noto Naskh Arabic" in f for f in fonts), fonts           # glyphs from the bundled Arabic font
    assert {"Helvetica", "Helvetica-Bold"} <= fonts                      # the ASCII text kept its Base-14 path
    assert "Pre-Bid Conference 10:00" in page.get_text()


def test_pdf_is_deterministic_with_unicode_text():
    assert gantt.pdf_bytes(programme()) == gantt.pdf_bytes(programme())


def test_ascii_text_keeps_the_base14_path():
    data = gantt.pdf_bytes(programme(arabic=False))
    page = pymupdf.open("pdf", data)[0]
    assert {f[3] for f in page.get_fonts(full=True)} == {"Helvetica", "Helvetica-Bold"}
    assert b"ActualText" not in data and "PDD 11:00" in page.get_text()
    assert gantt._t("a — b’s “x” ≤ 1") == "a - b's \"x\" <= 1"           # typographic punctuation still mapped
    assert gantt._t(AR_NAME) == AR_NAME                                  # anything else kept as written


def test_width_of_arabic_is_estimated_and_fit_truncates_it():
    w = gantt._w(AR_SHORT, 6.0)
    assert 0.3 * 6 * len(AR_SHORT) < w < 0.7 * 6 * len(AR_SHORT)
    cut = gantt._fit(AR_LABEL, 6.0, 40)
    assert cut.endswith("...") and AR_LABEL.startswith(cut[:-3]) and gantt._w(cut, 6.0) <= 40
