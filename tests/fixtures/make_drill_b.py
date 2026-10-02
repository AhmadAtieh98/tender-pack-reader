"""Builds "drill B": a second synthetic future "Addendum No. 3" (ADD-03) and a 7-document drill pack around it.

NOT tender content. Drill B rehearses the same live-session situation as tests/fixtures/make_drill.py (a new
addendum arrives; ingest -> units -> `draft` -> op file -> amendment engine) with different provisions:
  2.1  two replace_text changes in ONE paragraph (VOL-I 5.2 and VOL-I 7.1)
  3.1  a new obligation with a consequence, amending no clause (certificates of good standing)
  4.1  a cell of the image-reading Table 2-4 (TSS)
  5.1  a clause deleted and replaced by quoted text (VOL-I 6.7)        -- a change type ADD-01/ADD-02 do not use
  6.1  a new clause inserted after an existing one (VOL-I 4.4 after 4.3) -- likewise
  Q15  quotes the value 2.1 replaces;  Q16  negative control (cites VOL-I 6.4, which ADD-03 does not change)

Layout, fonts, furniture, cover band, Q&A table and the WinAnsi encoding of '—', '‘', '’' are make_drill.py's,
used by import (its constants and helpers are not changed or copied). The one addition is the indented quoted
clause of ADD-02 9.1 (measured on ADD-02 page 3): an opening quote at x 99.54 followed by the clause number in
Times-Bold, wrapped lines at x 125.06 (99.54 + 9 mm), 18.4 pt below the provision's own line.

The pack is make_drill's, except that `amendments_dir` is OUT_DIR/amendments, holding byte copies of
curation/amendments/ADD-01.yaml and ADD-02.yaml: during a rehearsal a person may save ADD-03.yaml there without
touching curation/. A rebuild refreshes the two copies and leaves any ADD-03.yaml in place.

`expected.yaml` is written from the builder's own inputs (what it printed and the outcome each provision is meant
to drill), never from the program's output. Unit ids follow the segmenter's documented naming.

Usage:  python tests/fixtures/make_drill_b.py OUT_DIR
        python -m tenderpack ingest --pack OUT_DIR/pack.yaml --out SOME_BUILD_DIR
        python -m tenderpack draft ADD-03 --evidence SOME_BUILD_DIR
"""
from __future__ import annotations

import hashlib
import json
import sys
from contextlib import contextmanager
from pathlib import Path

import pymupdf
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_drill as md  # noqa: E402  (layout constants and drawing helpers, used unchanged)

ROOT = md.ROOT
PDF_NAME = md.PDF_NAME
PACK_ID = "NUPA-ISTP-2026-014-DRILL-B"
ME = "tests/fixtures/make_drill_b.py"
QUOTE_X, QUOTE_WRAP_X = md.CLAUSE_WRAP_X, 125.06      # ADD-02 9.1: '‘8.6 ...' at 99.54, wrapped lines at 125.06

# ---------------------------------------------------------------------------------------------- content
ISSUED = "Issued 5 November 2026"
FRONT = [
    "This Addendum amends Volume I Clauses 5.2, 6.7 and 7.1, adds Volume I Clause 4.4 and a requirement for "
    "certificates of good standing, amends Volume II Table 2-4, and responds to clarification requests 15 and 16.",
    "This Addendum forms part of the RFP Documents and takes precedence in accordance with Volume I Clause 3.2. "
    "Bidders shall acknowledge receipt in Form 4-A. All other terms of the RFP Documents remain unchanged.",
]
R_, B_ = md.R_, md.B_
# (heading, [(clause number, [(text, font), ...], quoted clause (number, text) printed indented below, or None)])
SECTIONS = [
    ("1. RECITALS", [
        ("1.1", [("This Addendum is issued under Volume I Clause 5.3 and takes precedence in accordance with "
                  "Volume I Clause 3.2.", R_)], None)]),
    ("2. AMENDMENTS TO VOLUME I CLAUSES 5.2 AND 7.1", [
        ("2.1", [("In Volume I Clause 5.2, ‘ten (10) Working Days’ is deleted and ‘", R_),
                 ("seven (7) Working Days", B_),
                 ("’ is substituted, and in Volume I Clause 7.1, ‘one hundred and fifty (150) days’ is deleted and ‘", R_),
                 ("one hundred and eighty (180) days", B_), ("’ is substituted.", R_)], None)]),
    ("3. CERTIFICATES OF GOOD STANDING", [
        ("3.1", [("Each member of the Bidder shall submit with Envelope A a certificate of good standing issued not "
                  "earlier than thirty (30) days before the Proposal Due Date. ", R_),
                 ("Failure to submit the certificate for any member shall render the Proposal non-responsive.", B_)],
         None)]),
    ("4. AMENDMENT TO VOLUME II TABLE 2-4", [
        ("4.1", [("In Volume II Table 2-4, the limit for ", R_), ("Total Suspended Solids (TSS)", B_),
                 (" is amended from the value shown to ", R_), ("5 mg/l", B_),
                 (", assessed on the same basis. All other parameters in Table 2-4 are unchanged.", R_)], None)]),
    ("5. REPLACEMENT OF VOLUME I CLAUSE 6.7", [
        ("5.1", [("Volume I Clause 6.7 is ", R_), ("deleted and replaced", B_), (" by the following:", R_)],
         ("6.7", "A Bidder may withdraw its Proposal by written notice through the Portal received before the "
                 "Proposal Due Date. No Proposal may be modified after it has been submitted."))]),
    ("6. NEW CLAUSE 4.4 OF VOLUME I", [
        ("6.1", [("The following Clause 4.4 is ", R_), ("added", B_), (" to Volume I after Clause 4.3:", R_)],
         ("4.4", "Each Bidder shall confirm in writing through the Portal, within three (3) Working Days of this "
                 "Addendum, the name of its single point of contact."))]),
]
QA_HEADING = "7. RESPONSES TO CLARIFICATION REQUESTS 15 TO 16"
QA_HEADER = md.QA_HEADER
QA_ROWS = [
    ["15", "Clause 5.2 allows ten (10) Working Days before the Proposal Due Date for clarification requests. "
           "Will late requests be answered?",
     "No. Requests received after the period in Clause 5.2 will not be answered."],
    ["16", "Is the Bid Bond amount unchanged?", "Yes. Volume I Clause 6.4 is unchanged."],
]

# What each provision is meant to drill. Written here, from the wording above; never read back from the program.
UNRESOLVED_WHY = "no phrasing the drafter knows from ADD-01/ADD-02; it must come out unresolved (never dropped, " \
                 "never typed as a deletion or a single text change) until a person writes the op or a disposition"
INTENDED = {
    "ADD-03:cover/para1": {"draft": "no_effect", "why": "the addendum's issue date line (issued_from; stage date "
                                                        "2026-11-05, after ADD-02's 2026-10-22)"},
    "ADD-03:cover/para2": {"draft": "no_effect", "why": "cover text"},
    "ADD-03:cover/para3": {"draft": "no_effect", "why": "front matter on the cover; changes nothing by itself"},
    "ADD-03:1.1": {"draft": "no_effect", "why": "recital (section 1. RECITALS)"},
    "ADD-03:2.1": {"draft": "replace_text x2",
                   "ops": [{"type": "replace_text", "target": "VOL-I:5.2", "old": "ten (10) Working Days",
                            "new": "seven (7) Working Days", "engine": "valid"},
                           {"type": "replace_text", "target": "VOL-I:7.1", "old": "one hundred and fifty (150) days",
                            "new": "one hundred and eighty (180) days", "engine": "valid"}],
                   "effect": "TWO changes in one paragraph: both must be proposed. A single op for the first change "
                             "would account for the provision (C20) while silently losing the VOL-I:7.1 change; the "
                             "clarification cut-off (from the Proposal Due Date) and the Proposal validity period are "
                             "both recomputed"},
    "ADD-03:3.1": {"draft": "unresolved", "why": UNRESOLVED_WHY,
                   "effect": "a NEW obligation that amends no cited clause: a certificate of good standing for each "
                             "member, with Envelope A, issued not earlier than thirty (30) days before the Proposal "
                             "Due Date (26 November 2026 after ADD-01: issued on or after 27 October 2026); "
                             "consequence words 'shall render the Proposal non-responsive' (C15)"},
    "ADD-03:4.1": {"draft": "set_value", "target": "VOL-II:T2-4/TSS", "column": "Limit", "old": "10", "new": "5",
                   "engine": "valid",
                   "effect": "a cell of an image-reading table whose reading (VOL-II-p3-r1) is still pending; the "
                             "result carries reading status pending; TN (ADD-02 5.1) is untouched"},
    "ADD-03:5.1": {"draft": "unresolved", "why": UNRESOLVED_WHY,
                   "target": "VOL-I:6.7",
                   "new_text": "A Bidder may withdraw its Proposal by written notice through the Portal received before "
                               "the Proposal Due Date. No Proposal may be modified after it has been submitted.",
                   "effect": "the whole text of VOL-I:6.7 is replaced (the quoted '6.7' is the clause number, not "
                             "text): modification is no longer allowed once a Proposal is submitted. A person can "
                             "write it today as replace_text of the whole current text (old_resolved: "
                             "matched_in_target)"},
    "ADD-03:6.1": {"draft": "unresolved", "why": UNRESOLVED_WHY,
                   "anchor": "VOL-I:4.3", "new_clause": "VOL-I:4.4",
                   "new_text": "Each Bidder shall confirm in writing through the Portal, within three (3) Working Days "
                               "of this Addendum, the name of its single point of contact.",
                   "effect": "a new clause 4.4 after 4.3 (VOL-I:4.4 does not exist in the base); a new obligation "
                             "with a deadline counted from this Addendum's issue date (5 November 2026). A person can "
                             "write it today as insert_unit anchored at VOL-I:4.3 with the quoted text (the engine "
                             "names the new unit VOL-I:4.3+ADD-03, not VOL-I:4.4)"},
    "ADD-03:Q15": {"draft": "unresolved", "cites": ["VOL-I:5.2"],
                   "effect": "quotes 'ten (10) Working Days', the value ADD-03 2.1 replaces: must be listed for review, "
                             "never revoked or changed automatically"},
    "ADD-03:Q16": {"draft": "unresolved", "cites": ["VOL-I:6.4"],
                   "effect": "negative control: cites a unit ADD-03 does not change (VOL-I:6.4); nothing about it "
                             "should be flagged by ADD-03"},
}


# ---------------------------------------------------------------------------------------------- the addendum
def _quote_runs(num: str, text: str) -> list[tuple[str, str]]:
    """An indented quoted clause as ADD-02 9.1 prints it: opening quote, bold number, text, closing quote."""
    return [("‘", R_), (num, B_), (f" {text}’", R_)]


def _runs(num_runs, quote) -> list[tuple[str, str]]:
    """All runs of a provision, in reading order (the quoted clause is its last line(s))."""
    return list(num_runs) + ([(" ", R_)] + _quote_runs(*quote) if quote else [])


@contextmanager
def _qa_rows(rows):
    """make_drill._qa_table prints make_drill.QA_ROWS; lend it drill B's rows for the duration of one call."""
    saved, md.QA_ROWS = md.QA_ROWS, rows
    try:
        yield
    finally:
        md.QA_ROWS = saved


def _make_pdf(path: Path) -> dict:
    doc = pymupdf.open()
    layout: dict = {"pages": {}}

    # ---- page 1: cover band, front matter, sections 1-6
    p = doc.new_page(width=md.W, height=md.H)
    md._furniture(p, 1)
    p.draw_rect(pymupdf.Rect(*md.BAND), color=None, fill=md.BAND_FILL)
    md._text(p, 66.69, 100.36, "ADDENDUM NO. 3", "hebo", 15, md.WHITE)
    md._text(p, 528.58 - md._width(ISSUED, "hebo", 8.5), 91.86, ISSUED, "hebo", 8.5, md.WHITE)
    tender = "Tender NUPA/ISTP/2026/014"
    md._text(p, 528.58 - md._width(tender, "helv", 8.5), 102.86, tender, "helv", 8.5, md.WHITE)
    md._text(p, md.TEXT_X, 142.86, "Wadi Sirhan Independent Sewage Treatment Plant", "hebo", 10.5)
    y, lines1 = md._flow(p, 158.96, [(FRONT[0], R_)], md.TEXT_X, md.TEXT_X)
    y, lines2 = md._flow(p, y + md.AFTER_PARA, [(FRONT[1], R_)], md.TEXT_X, md.TEXT_X)
    p1 = {"front_matter_lines": lines1 + lines2, "sections": {}}
    for heading, clauses in SECTIONS:
        y += md.BEFORE_HEAD
        md._text(p, md.TEXT_X, y, heading, "hebo", 13)
        sec = p1["sections"][heading] = {"heading_baseline": round(y, 2), "clauses": {}}
        for i, (num, runs, quote) in enumerate(clauses):
            y += md.AFTER_HEAD if i == 0 else md.AFTER_PARA
            first = y
            md._text(p, md.TEXT_X, y, num, "tibo", md.BODY)
            y, printed = md._flow(p, y, runs, md.CLAUSE_TEXT_X, md.CLAUSE_WRAP_X, lead_in="   ")
            rec = sec["clauses"][num] = {"first_baseline": round(first, 2), "lines": printed}
            if quote:
                y += md.AFTER_PARA
                rec["quote_first_baseline"] = round(y, 2)
                y, rec["quote_lines"] = md._flow(p, y, _quote_runs(*quote), QUOTE_X, QUOTE_WRAP_X)
    assert y < md.FOOTER_RULE_Y - 20, f"sections 1-6 overflow page 1 (last baseline {y:.1f})"
    layout["pages"][1] = p1

    # ---- page 2: section 7, the clarification table
    p = doc.new_page(width=md.W, height=md.H)
    md._furniture(p, 2)
    y = 81.36
    md._text(p, md.TEXT_X, y, QA_HEADING, "hebo", 13)
    with _qa_rows(QA_ROWS):
        table = md._qa_table(p, y + md.HEAD_TO_TABLE)
    layout["pages"][2] = {"heading_baseline": y, "table": table}

    doc.set_metadata({"title": "Addendum No. 3 (synthetic drill B, not tender content)",
                      "author": ME, "creator": ME, "producer": f"PyMuPDF via {ME}",
                      "creationDate": "D:20261105090000+00'00'", "modDate": "D:20261105090000+00'00'"})
    doc.save(path, garbage=3, deflate=True, no_new_id=True)
    doc.close()
    return layout


def _expected(layout: dict) -> dict:
    units = [
        {"id": "ADD-03:cover/para1", "kind": "paragraph", "page": 1, "text": ISSUED},
        {"id": "ADD-03:H:cover", "kind": "heading", "page": 1, "text": "ADDENDUM NO. 3"},
        {"id": "ADD-03:cover/para2", "kind": "paragraph", "page": 1, "text": "Tender NUPA/ISTP/2026/014"},
        {"id": "ADD-03:H:cover-2", "kind": "heading", "page": 1, "text": "Wadi Sirhan Independent Sewage Treatment Plant"},
        # two printed paragraphs with ADD-02's spacing; ADD-02 prints its front matter the same way (ADD-02:cover/para3)
        {"id": "ADD-03:cover/para3", "kind": "paragraph", "page": 1, "text": " ".join(FRONT),
         "printed_paragraphs": list(FRONT)},
    ]
    for heading, clauses in SECTIONS:
        units.append({"id": f"ADD-03:H:S{heading.split('.')[0]}", "kind": "heading", "page": 1, "text": heading})
        for num, runs, quote in clauses:
            allr = _runs(runs, quote)
            u = {"id": f"ADD-03:{num}", "kind": "clause", "page": 1, "label": num, "text": "".join(t for t, _ in allr),
                 "bold_runs": [t for t, f in allr if f == B_]}
            if quote:
                # printed indented on its own line(s) like ADD-02 9.1; the segmenter joins it to the provision
                u["quoted_clause"] = {"number": quote[0], "text": quote[1]}
            units.append(u)
    sec = QA_HEADING.split(".")[0]
    units.append({"id": f"ADD-03:H:S{sec}", "kind": "heading", "page": 2, "text": QA_HEADING})
    units.append({"id": f"ADD-03:S{sec}/QA", "kind": "table", "page": 2, "text": " | ".join(QA_HEADER),
                  "columns": list(QA_HEADER)})
    for row in QA_ROWS:
        cells = dict(zip(QA_HEADER, row))
        units.append({"id": f"ADD-03:Q{row[0]}", "kind": "table_row", "page": 2, "parent": f"ADD-03:S{sec}/QA",
                      "cells": cells, "text": " | ".join(f"{k}: {v}" for k, v in cells.items())})
    for u in units:
        if u["id"] in INTENDED:
            u["intended"] = INTENDED[u["id"]]
    return {
        "pack_id": PACK_ID,
        "note": "synthetic drill addendum (drill B; NOT tender content); written from the builder's inputs, not from "
                "program output",
        "doc_id": "ADD-03", "kind": "addendum", "number": 3, "pdf": PDF_NAME, "pages": 2,
        "issued": {"unit": "ADD-03:cover/para1", "text": ISSUED, "date": "2026-11-05", "previous": "ADD-02 2026-10-22"},
        "furniture_per_page": {"WATERMARK": 1, "HEADER-TITLE": 1, "HEADER-REF": 1, "FOOTER-DISCLAIMER": 1,
                               "FOOTER-PAGE": 1},
        "printed_pages": ["1", "2"],
        "fonts": sorted(md.FONT_NAMES.values()),
        "regions": [],
        "provisions": [u["id"] for u in units if u["kind"] in ("paragraph", "clause", "table_row")],
        "units": units,
        "engine_outcome": {
            "status": "PARTIAL",
            "why": "ADD-03:3.1 (new obligation), 5.1 (clause replaced), 6.1 (clause inserted), Q15 and Q16 are "
                   "unresolved until a person decides them",
            "valid_ops": [{"provision": "ADD-03:2.1", "target": "VOL-I:5.2"},
                          {"provision": "ADD-03:2.1", "target": "VOL-I:7.1"},
                          {"provision": "ADD-03:4.1", "target": "VOL-II:T2-4/TSS"}],
            "invalid_ops": [],
            "unresolved": ["ADD-03:3.1", "ADD-03:5.1", "ADD-03:6.1", "ADD-03:Q15", "ADD-03:Q16"],
            "no_effect": ["ADD-03:cover/para1", "ADD-03:cover/para2", "ADD-03:cover/para3", "ADD-03:1.1"],
        },
        "layout": layout,
    }


# ---------------------------------------------------------------------------------------------- the drill pack
def build(out_dir: Path) -> dict:
    out = Path(out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    pdf_path = out / PDF_NAME
    layout = _make_pdf(pdf_path)
    data = pdf_path.read_bytes()
    pages = pymupdf.open(pdf_path).page_count

    real = yaml.safe_load((ROOT / "config/pack.yaml").read_text(encoding="utf-8"))
    documents = [dict(d) for d in real["documents"]]
    assert [d["doc_id"] for d in documents] == ["VOL-I", "VOL-II", "VOL-IV", "VOL-V", "ADD-01", "ADD-02"], documents
    documents.append({"doc_id": "ADD-03", "kind": "addendum", "number": 3, "path": md._rel(pdf_path)})

    received = {f["path"]: f for f in json.loads((ROOT / "sources/manifest.json").read_text(encoding="utf-8"))["files"]}
    files = [received[d["path"]] for d in documents[:-1]]
    files.append({"path": documents[-1]["path"], "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                  "pages": pages, "producer": f"PyMuPDF via {ME}", "creation_date": "D:20261105090000+00'00'",
                  "note": f"synthetic drill addendum (drill B) built by {ME} (not tender content)"})
    (out / "manifest.json").write_text(json.dumps({"files": files}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    (out / "furniture.yaml").write_bytes((ROOT / "config/furniture.yaml").read_bytes())   # unchanged: '—' is encoded

    amend = out / "amendments"                          # rehearsal copy: a person may add ADD-03.yaml here
    amend.mkdir(exist_ok=True)
    for name in ("ADD-01.yaml", "ADD-02.yaml"):
        (amend / name).write_bytes((ROOT / "curation/amendments" / name).read_bytes())

    pack = {"pack_id": PACK_ID,
            "manifest": md._rel(out / "manifest.json"),
            "furniture": md._rel(out / "furniture.yaml"),
            "readings_dir": "curation/readings",               # the real image readings (still pending review)
            "approvals": md._rel(out / "approvals.yaml"),      # never created: no reading is approved in a drill
            "amendments_dir": md._rel(amend),
            "register": "curation/register/rows.yaml",
            "documents": documents}
    (out / "pack.yaml").write_text(
        "# Drill B pack: the six received documents as in config/pack.yaml, plus a SYNTHETIC Addendum No. 3\n"
        f"# ({ME}; not tender content). amendments_dir holds copies of the curated ADD-01 and\n"
        "# ADD-02 op files, so an ADD-03.yaml written during the rehearsal stays out of curation/. Paths are\n"
        "# repository-relative, or absolute when the drill was built outside the repository; tenderpack resolves\n"
        "# either as root / path.\n"
        + yaml.safe_dump(pack, sort_keys=False, allow_unicode=True, width=200), encoding="utf-8")

    expected = _expected(layout)
    expected["sha256"] = hashlib.sha256(data).hexdigest()
    (out / "expected.yaml").write_text(yaml.safe_dump(expected, allow_unicode=True, sort_keys=False, width=110),
                                       encoding="utf-8")
    return expected


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python tests/fixtures/make_drill_b.py OUT_DIR")
    build(Path(sys.argv[1]))
