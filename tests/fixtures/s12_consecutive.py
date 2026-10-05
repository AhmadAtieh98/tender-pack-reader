"""Session 12 (W5): two SYNTHETIC consecutive addenda for the consecutive-addenda regressions
(tests/test_session12_consecutive.py). NOT tender content: built the way tests/fixtures/make_drill.py builds its
Addendum No. 3 (the same page geometry, fonts, furniture and WinAnsi encoding, its drawing helpers reused), one page
each, into a disposable folder.

  ADD-03 (Addendum No. 3, issued 5 November 2026)
    1.1  inserts a new Clause 6.8 in Volume I after Clause 6.7 (delivery representatives; a unit ADD-03 introduces)
    2.1  amends Volume I Clause 7.1: 150 days -> 180 days (proposal validity)
  ADD-04 (Addendum No. 4, issued 19 November 2026)
    1.1  amends the Clause 6.8 that Addendum No. 3 inserted: two (2) -> three (3) representatives
    2.1  reverses ADD-03 2.1: in Volume I Clause 7.1 180 days -> 150 days
    3.1  amends a base clause: Volume I Clause 6.1, 14:00 hours -> 11:00 hours Riyadh time

What each provision is meant to drill is written here from the wording, never read back from the program."""
from __future__ import annotations

from pathlib import Path

import pymupdf

import make_drill as MD

NEW_68 = ("Each Bidder shall, not later than five (5) Working Days before the Proposal Due Date, register through the "
          "Portal the names of not more than two (2) representatives who will deliver its Proposal.")
R_, B_ = MD.R_, MD.B_

ADDENDA = {
    "ADD-03": {
        "number": 3, "issued": "Issued 5 November 2026", "date": "D:20261105090000+00'00'",
        "front": "This Addendum inserts a new Clause 6.8 in Volume I and amends Volume I Clause 7.1.",
        "sections": [
            ("1. NEW CLAUSE 6.8 IN VOLUME I", [
                ("1.1", [("The following new Clause 6.8 is inserted in Volume I after Clause 6.7: ‘", R_),
                         (NEW_68, B_), ("’", R_)])]),
            ("2. AMENDMENT TO VOLUME I CLAUSE 7.1", [
                ("2.1", [("In Volume I Clause 7.1, ‘one hundred and fifty (150) days’ is deleted and ‘", R_),
                         ("one hundred and eighty (180) days", B_), ("’ is substituted.", R_)])]),
        ]},
    "ADD-04": {
        "number": 4, "issued": "Issued 19 November 2026", "date": "D:20261119090000+00'00'",
        "front": "This Addendum amends Volume I Clause 6.8 as inserted by Addendum No. 3, and Volume I Clauses 7.1 "
                 "and 6.1.",
        "sections": [
            ("1. AMENDMENT TO VOLUME I CLAUSE 6.8", [
                ("1.1", [("In Volume I Clause 6.8, inserted by Addendum No. 3, ‘two (2) representatives’ is deleted "
                          "and ‘", R_), ("three (3) representatives", B_), ("’ is substituted.", R_)])]),
            ("2. AMENDMENT TO VOLUME I CLAUSE 7.1", [
                ("2.1", [("In Volume I Clause 7.1, ‘one hundred and eighty (180) days’ is deleted and ‘", R_),
                         ("one hundred and fifty (150) days", B_), ("’ is substituted.", R_)])]),
            ("3. AMENDMENT TO VOLUME I CLAUSE 6.1", [
                ("3.1", [("In Volume I Clause 6.1, ‘14:00 hours Riyadh time’ is deleted and ‘", R_),
                         ("11:00 hours Riyadh time", B_), ("’ is substituted.", R_)])]),
        ]},
}


def make(addendum: str, out: Path) -> Path:
    """One page: furniture, cover band, front matter, the sections (make_drill.py's layout)."""
    spec = ADDENDA[addendum]
    n = spec["number"]
    saved = MD.HEADER_TITLE
    MD.HEADER_TITLE = f"Addendum No. {n}"
    try:
        doc = pymupdf.open()
        p = doc.new_page(width=MD.W, height=MD.H)
        MD._furniture(p, 1)
        p.draw_rect(pymupdf.Rect(*MD.BAND), color=None, fill=MD.BAND_FILL)
        MD._text(p, 66.69, 100.36, f"ADDENDUM NO. {n}", "hebo", 15, MD.WHITE)
        MD._text(p, 528.58 - MD._width(spec["issued"], "hebo", 8.5), 91.86, spec["issued"], "hebo", 8.5, MD.WHITE)
        tender = "Tender NUPA/ISTP/2026/014"
        MD._text(p, 528.58 - MD._width(tender, "helv", 8.5), 102.86, tender, "helv", 8.5, MD.WHITE)
        MD._text(p, MD.TEXT_X, 142.86, "Wadi Sirhan Independent Sewage Treatment Plant", "hebo", 10.5)
        y, _ = MD._flow(p, 158.96, [(spec["front"], R_)], MD.TEXT_X, MD.TEXT_X)
        for heading, clauses in spec["sections"]:
            y += MD.BEFORE_HEAD
            MD._text(p, MD.TEXT_X, y, heading, "hebo", 13)
            for i, (num, runs) in enumerate(clauses):
                y += MD.AFTER_HEAD if i == 0 else MD.AFTER_PARA
                MD._text(p, MD.TEXT_X, y, num, "tibo", MD.BODY)
                y, _ = MD._flow(p, y, runs, MD.CLAUSE_TEXT_X, MD.CLAUSE_WRAP_X, lead_in="   ")
        doc.set_metadata({"title": f"Addendum No. {n} (synthetic, not tender content)",
                          "author": "tests/fixtures/s12_consecutive.py", "creator": "tests/fixtures/s12_consecutive.py",
                          "producer": "PyMuPDF via tests/fixtures/s12_consecutive.py",
                          "creationDate": spec["date"], "modDate": spec["date"]})
        path = Path(out) / f"{addendum}_Addendum_No_{n}.pdf"
        doc.save(path, garbage=3, deflate=True, no_new_id=True)
        doc.close()
        return path
    finally:
        MD.HEADER_TITLE = saved
