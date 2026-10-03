# Author notes: Addendum No. 3 (blind fixture blind01)

## Timing (UTC)

- Start: 2026-10-03T00:43:15Z (first command in the session)
- End: 2026-10-03T01:05Z (sealing, when SHA256SUMS was written)
- Elapsed: about 22 minutes

## Information boundary

I read only these files:

- `sources/candidate_pack/*.pdf`: VOL-I, VOL-II, VOL-IV, VOL-V, ADD-01, ADD-02.
- `sources/brief/Lamar_PPP_AI_Partner_Round2_Brief.pdf`.
- `sources/correspondence/2026-10-02_reply_from_hiring.md`.

I read nothing else in the repository, did not use git history, and did not import the `tenderpack` package. I used PyMuPDF from `.venv` as a library only, for two things: to inspect the PDFs and to write the output PDF. I viewed the two image-only items as extracted PNGs:

- VOL-II Table 2-4, xref 19 on page 3.
- VOL-IV Form 4-C (Arabic), xref 26 on page 6.

## Method

1. I extracted the full text of all six pack PDFs and viewed the two image-only items.
2. I measured ADD-01 and ADD-02 with PyMuPDF using `get_text('dict')`, `get_drawings()`, `get_fonts()`, and the raw decompressed content streams. Both files are ReportLab output on A4 (595.2756 x 841.8898 pt). They use four Base-14 Type1 fonts, F1 Helvetica, F2 Helvetica-Bold, F3 Times-Roman and F4 Times-Bold, all with WinAnsiEncoding and none embedded. ADD-01 page 4 also uses Times-Italic, which ADD-03 does not need.
3. I wrote a small layout engine (`build_addendum.py`) that emits content streams in ReportLab's operator style (`Tm`, `TL`, `Tw`, `Td`, `T*`, `Ts`). It writes the font dictionaries and page resources by hand, so the fonts are exactly the same four non-embedded Base-14 fonts, F1 to F4, with WinAnsiEncoding. Text widths come from `pymupdf.Font(<base14>)`, which matches the Adobe AFM widths. For example, the watermark measures 574.26 pt, the same as ReportLab's `-287.13` offset.
4. I calibrated the engine by rebuilding parts of ADD-02: the cover, intro, provisions 1.1, 2.1, 3.1 and 9.1 with the quoted 8.6, and Q&A rows 7 to 11. I then compared span origins with the original.
   - The first comparison matched everywhere except some line-break decisions. ADD-01 and ADD-02 show that ReportLab lets a line overflow by up to about 1 pt and then compresses it with a negative `Tw`. The observed overflows were 0.98, 0.99, 0.71 and 0.16 pt, and no line broke with less than 4 pt of overflow.
   - I added a 1.0 pt tolerance. After that, line breaks, span origins and bold-run positions matched ADD-02 exactly. For example, ADD-02 2.1 has its bold run at x = 382.97–520.63, and the 9.1 quoted block has `thirty-five per cent (35%)` at x = 238.06–344.14.
5. I built ADD-03 (3 pages), rendered every page at 110 dpi and compared them with ADD-02's pages by eye. I also checked `page.get_text()` reading order, which follows the same pattern as ADD-02: watermark, header, footer, cover, then body in order. Finally I checked that every "old" quotation in the key occurs in the pack and every "new" text occurs in ADD-03, using a whitespace-normalised substring check.
6. I made the build deterministic by saving with `no_new_id=True`. Two rebuilds gave the same SHA-256.

### Layout measured in ADD-01 / ADD-02 and reproduced

All y values below are top-down, as PyMuPDF reports them.

- **Watermark:** "FICTIONAL — ASSESSMENT PACK", Helvetica-Bold 34, grey .86. The transform is `.615661 .788011 -0.788011 .615661 297.6378 420.9449 cm`, a rotation of about 52° about the page centre, with the text at x = −287.13. It is drawn first.
- **Header:** "Addendum No. N" on the left at x = 56.69 and "NUPA/ISTP/2026/014" right-aligned to x = 538.58. Both are Helvetica 6.8, colour #5a5a5a, baseline 39.69. A rule at y = 45.35 runs from x = 56.69 to 538.58, 0.4 pt wide, colour #b8b8b8.
- **Footer:** a rule at y = 799.37. Below it, Helvetica 6.4 at baseline 809.29: the fictional-document notice on the left and "Page N" right-aligned to x = 538.58. There is no "of M".
- **Cover band:** a #2a2a2a box from (56.69, 74.36) to (538.58, 114.36).
  - "ADDENDUM NO. N" in Helvetica-Bold 15, white, at x = 66.69, baseline 100.36.
  - "Issued <date>" in Helvetica-Bold 8.5, right edge 528.58, baseline 91.86.
  - "Tender NUPA/ISTP/2026/014" in Helvetica 8.5, right edge 528.58, baseline 102.86.
- **Project line:** Helvetica-Bold 10.5 at baseline 142.86.
- **Body paragraphs:** Times-Roman 9.6, leading 13.4, colour #1a1a1a, justified from x = 62.69 to 532.58.
- **Section headings:** "N. TITLE" in Helvetica-Bold 13, leading 16.
- **Provisions:**
  - The number is in Times-Bold, followed by three spaces, starting at x = 62.69.
  - Continuation lines use a 36.85 pt hanging indent (x = 99.54).
  - A quoted clause starts its first line at x = 99.54 and continues at x = 125.06.
- **Vertical spacing (gap from the bottom of one element to the top of the next):**

  | From | To | Gap (pt) |
  |---|---|---|
  | paragraph | paragraph | 5 |
  | project line | body | 4 |
  | anything | heading | 14 |
  | heading | next element | 7 |
  | cover band | project line | 18 |

  - The first baseline sits one font size below the top of its element.
  - Content runs from y = 68.36 to a bottom limit of about 779.2.
- **Q&A table:**
  - Columns are at x = 56.69, 90.71, 300.47 and 538.58.
  - The header band is #3a3a3a with white Helvetica-Bold 8.2 text.
  - Body text is Times-Roman 8.2 with leading 10.4, padding 3.5 top and bottom and 4 at the sides, and the first baseline 11.7 below the top of the row.
  - Grid lines are 0.4 pt, #b8b8b8, drawn with round caps and joins.
  - When the table splits across pages, the header row repeats, as in ADD-01.
- **Superscripts** (as in "m3"): 0.8 × the font size, raised by 0.5 × the font size with `Ts`.
- **Editorial style follows ADD-02:**
  - Substituted text is in bold inside the quote marks, using curly quotes ‘…’.
  - Single key words such as **inserted** and **superseded** are also bold.
  - The cover summary paragraph is followed by the standard paragraph on precedence and acknowledgement.
- **Metadata:** title and author are "(anonymous)", subject and creator are "(unspecified)", as in ADD-01/02. The producer field is left empty rather than claiming ReportLab, and the creation date is the real build date.
- **Known non-visual differences:** the header says PDF 1.7 rather than 1.4, and the object numbering differs. Neither affects text, layout or rendering.

## Content design

- **Dates:**
  - ADD-03 is dated Thursday 5 November 2026. That is after ADD-02 (22 October 2026), and ADD-01 and ADD-02 were both issued on Thursdays.
  - It moves the Proposal Due Date from 26 November 2026 to Thursday 10 December 2026, keeping 14:00.
  - Every derived date in the key was computed from the pack's own definitions. Working Days are counted under VOL-I 2.4 (Sunday to Thursday, with the stated date not counted when counting back). Calendar-day periods count the PDD as day 0, and the alternative is also shown.
- **Rule coverage:**
  - Date change with knock-on effects: 2.1 to 2.3, plus the mutatis mutandis application of ADD-01 2.2.
  - Change to a period in Working Days: 3.1, which goes from 10 to 15 and is scoped to Clause 5.2 only, although the same words also appear in VOL-I 12.3 and VOL-V 29.4. Section 3.2 also adds a time of day to the cut-off.
  - Value changes in clause text: 4.1 (Bid Bond), 7.1 (local content percentage) and 9.1 (Financial Close days).
  - Change to a text-layer table cell: 11.1, Table 2-6 row 2-6.2.
  - Deletion of a requirement: 5.1, the three hard copies.
  - New requirement with an explicit consequence: the new Clause 10.5 in 8.1 (affordability ceiling, "shall be rejected").
  - Changes to image-only items: 10.1 (Table 2-4 TSS row, limit and basis) and 12.1 (Arabic Form 4-C).
  - Q&A that changes substance: Q16, which amends VOL-II 6.1 inside an answer, and Q17, which excludes affiliates' reference projects.
  - Q&A that only restates the pack: Q15, Q18 and Q20. Q19 has no effect.
  - The designated ambiguity is 12.1/12.2. The sixth Form 4-C declaration is given only in English, but VOL-I 9.4 and ADD-02 Q9 require Arabic, with the Arabic governing. No Arabic text or reissued form is supplied.

### Change types not used in ADD-01 / ADD-02, and why I chose them

ADD-01 and ADD-02 use these types:

- date substitution with a general "periods adjusted" clause;
- deletion of a clause in its entirety;
- adding words at the end of a clause;
- value substitution in clause text;
- reissuing a whole table, with an amendment carried in a table note;
- changing a cell of an image-only table;
- a new form with a consequence;
- reinstating a deleted clause and ending an earlier addendum's sub-provision;
- a reissued form in an appendix;
- non-binding minutes;
- a Q&A table.

ADD-03 adds these types:

1. **Renumbering clauses and re-pointing cross-references, including a reference inside an earlier addendum** (8.2: 10.5 → 10.6 and 10.6 → 10.7, so ADD-02 Q14 now points to 10.6). This tests whether a register keeps lineage when identifiers change, instead of treating the change as a delete plus an add.
2. **Amending a footnote**, here footnote 12, which carries a rejection consequence (6.1). Footnotes are easy to drop during extraction, and this one contains a disqualifier.
3. **Correcting an erratum in an earlier addendum** (2.3). ADD-01 Appendix A never updated its own Proposal Due Date field. This tests whether the addendum chain is applied to earlier addenda as well as to the volumes.
4. **Applying an earlier addendum's provision mutatis mutandis** (2.2). The knock-on dates must be derived, because the addendum does not state them.
5. **Superseding an earlier clarification response** (9.2, ADD-02 Q13). This is the A2 question "which earlier answers are now wrong".
6. **Amending text through a Q&A answer instead of the body, with the change missing from the cover summary** (Q16).

I chose these because each is realistic for a tender office. Each also exercises a separate failure mode in a register or reconciliation system: identifier lineage, footnote extraction, recursion through earlier addenda, derived dates, Q&A supersession, and over-reliance on summaries.

### Fairness checks

- Every "deleted" quotation matches the pack text exactly. The one exception is 2.1, which quotes the text as amended by ADD-01; the addendum says so ("as amended by Addendum No. 1 Section 2.1").
- No provision needs information outside the pack, apart from ordinary engineering arithmetic in the advanced finding on transmission-main velocity.
- Exactly one ambiguity is deliberate (Form 4-C). Other "human decision" items in the key are judgement calls that are fair to expect, not puzzles.

## Files

- `../ADD-03_Addendum_No_3.pdf`: the fixture, 3 pages.
- `expected_findings.yaml`: the sealed answer key.
- `build_addendum.py`: the deterministic builder. Run it with `python build_addendum.py ADD-03_Addendum_No_3.pdf` and PyMuPDF 1.28.2.
- `author_notes.md`: this file.
- `SHA256SUMS`: hashes of the PDF and of the SEALED files.
