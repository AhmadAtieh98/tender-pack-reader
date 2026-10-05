# Subagent brief 5: Build synthetic ADD-03 drill fixture

Launched 2026-10-02 08:30:28 UTC; model option requested: `(default)`; subagent type: `general-purpose`.
The text below is the prompt exactly as sent by the coordinator (exported from the session transcript on 4 Oct 2026, session 11).

---

Build a synthetic "Addendum No. 3" PDF for a drill of a deterministic tender-pack reader. Repository: /home/user/tender-pack-reader (Python 3.11, `.venv/bin/python`). You may create/edit ONLY `tests/fixtures/make_drill.py` (and scratch files under /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/drill-agent/). Do not edit anything else; do not commit or push; never write into the repository's build/, curation/, config/ or sources/.

Goal: `make_drill.build(out_dir: Path) -> dict` writes into out_dir (a disposable directory):
- `ADD-03_Addendum_No_3.pdf` — a synthetic addendum that is typographically indistinguishable, for the program, from the real addenda `sources/candidate_pack/ADD-01_Addendum_No_1.pdf` and `ADD-02_Addendum_No_2.pdf`. Study those with PyMuPDF (`page.get_text("dict")` / `"rawdict"`: fonts, sizes, colours, flags, positions, the running header, the footer lines, the rotated watermark, bold clause numbers, section heading style, the cover block, the clarification Q&A ruled table with a white-on-dark header row). Reproduce them with PyMuPDF drawing calls (insert_text with base-14 fonts matching what the real PDFs use, draw_rect/draw_line for table rules and the dark header fill, morph for the rotated watermark). The furniture must satisfy the furniture rules in config/furniture.yaml exactly (each rule may have per-page expected counts — read the file), and the cover/issue line, header texts etc. should say "ADDENDUM NO. 3" / "Issued 5 November 2026" where the real addenda say their own number/date. Mark nothing as real tender content beyond what the existing pack already contains (the pack is itself fictional).
- `manifest.json` and `pack.yaml` for a 7-document pack: the six real documents exactly as listed in config/pack.yaml (same doc_id, kind, number, path strings relative to the repository root, and the manifest entries copied from sources/manifest.json — read tenderpack/sources.py to see how paths and hashes are matched) plus `{doc_id: "ADD-03", kind: "addendum", number: 3, path: <absolute path of the new PDF>}` with its sha256 and page count in the manifest. Keep `furniture: config/furniture.yaml` and `readings_dir: curation/readings` (repository-relative, read-only use), and set `approvals:` to `<out_dir>/approvals.yaml` (which must NOT be created). Look at config/pack.yaml for all keys.
- returns a dict describing what it placed (provision ids you expect, e.g. "ADD-03:2.1", with their text).
Deterministic: same bytes on every run (fixed metadata dates, `doc.save(..., garbage=3, deflate=True, no_new_id=True)`), no network.

Content of ADD-03 (keep the real addenda's wording style; one or two pages):
- Cover block as in the real addenda: "Issued 5 November 2026", "ADDENDUM NO. 3", "Tender NUPA/ISTP/2026/014", project name, and a one-sentence cover summary paragraph.
- "1. RECITALS" — 1.1 "This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda No. 1 and No. 2 in accordance with Volume I Clause 3.2."
- "2. AMENDMENT TO VOLUME I CLAUSE 6.1" — 2.1 "Volume I Clause 6.1 is amended by deleting ‘Thursday 26 November 2026’ and substituting ‘Thursday 10 December 2026’. The time of 14:00 Riyadh time is unchanged."
- "3. AMENDMENT TO VOLUME V CLAUSE 31.3" — 3.1 "In Volume V Clause 31.3, ‘seventy-two (72) hours’ is deleted and ‘forty-eight (48) hours’ is substituted."
- "4. DELETION OF VOLUME I CLAUSE 8.6" — 4.1 "Volume I Clause 8.6 (Local Content Certificate) is deleted in its entirety."
- "5. AMENDMENT TO VOLUME II TABLE 2-4" — 5.1 "In Volume II Table 2-4, the limit for Total Phosphorus (TP) is amended from the value shown to 0.5 mg/l, assessed on the same basis."
- "6. BID SECURITY" — 6.1 "The bid security period is extended by thirty days."
- "7. AMENDMENT TO VOLUME II CLAUSE 4.4" — 7.1 "In Volume II Clause 4.4, ‘seventy-two (72) hours’ is deleted and ‘sixty (60) hours’ is substituted."
- "8. RESPONSES TO CLARIFICATION REQUESTS 15 TO 16" — a ruled Q&A table exactly like the real addenda's (columns "No | Bidder question | Authority response"): row 15: "Does the amended weighting in Addendum No. 2 change the technical threshold?" / "No. The threshold at Volume I Clause 11.3 is unchanged."; row 16: "Does the 120-page limit in Volume I Clause 9.2 still apply?" / "Volume I Clause 9.2 as amended by Addendum No. 2 applies."
Curly quotes ‘ ’ exactly as above (the real addenda use them).

Verification you must do before finishing (all output under your scratch folder):
1. `.venv/bin/python -m tenderpack ingest --pack <out_dir>/pack.yaml --out <scratch>/drill-build` exits 0 and prints STRUCTURE OK with C01–C10 all "pass" (C04 furniture counts included). If a check fails, fix the PDF, not the program.
2. In `<scratch>/drill-build/units.json`, the ADD-03 units include clause units ADD-03:1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1 with exactly the texts above (the clause number is the label, not in the text), headings ADD-03:H:S1..S8, the cover paragraph with "Issued 5 November 2026", and table rows ADD-03:Q15 and ADD-03:Q16 with cells "No", "Bidder question", "Authority response".
3. Building twice gives byte-identical PDFs.
Final message: the API, what the PDF contains, the exact verification output lines (C01–C10 and the unit ids/texts found), and anything you had to approximate.
