# Blind rehearsal 03: author notes (SEALED)

Input: `rehearsals/blind-03/input/ADD-03_Addendum_No_3.pdf` (4 pages, "Issued 1 November 2026", a Sunday).
Answer key: `expected_findings.yaml` in this directory. Builder: `build_addendum.py`. It is deterministic:
`python build_addendum.py out.pdf` with the repository's virtualenv (PyMuPDF 1.28.2) gives identical bytes on
every run. The builder refuses to run if `/usr/share/fonts/truetype/freefont/FreeSerif.ttf` does not have the
pinned SHA-256 (`c57bf5de…b7d2`), because the embedded Arabic subset depends on it.

## What I read

Allowed sources only:

- the six pack PDFs (VOL-I, VOL-II including the Table 2-4 image, VOL-IV including the Form 4-C image, VOL-V,
  ADD-01, ADD-02), read in full; I rendered both images to read them;
- the brief (`sources/brief/…Round2_Brief.pdf`) and the correspondence `.md` files, for the A1 to A5 meanings and
  the "same format as Addenda 1 and 2" statement;
- the blind-01 and blind-02 input PDFs, only to avoid their changes;
- the blind-02 `build_addendum.py` and `author_notes.md`, as a technique and style example.

I did not open the tool's code (`tenderpack/`), tests, `curation/`, `config/`, `build/`, `out/`, `docs/`,
`worklog/`, `scripts/`, or any earlier rehearsal's `work/`, `out-*`, `COMPARISON.md` or `expected_findings.yaml`.
`git status` was run once, read-only. Nothing was committed or staged. The only file written inside the
repository is the input PDF.

## Style fidelity

- A4. All Latin text uses Base-14 Type1 fonts (Helvetica, Helvetica-Bold, Times-Roman, Times-Bold, WinAnsi, not
  embedded), as in ADD-01 and ADD-02. There are no images.
- **The one deliberate departure is the Arabic.** No Base-14 font carries Arabic, so the two Arabic blocks in
  Section 4 use an embedded subset of GNU FreeSerif (Type0, Identity-H, resource `/F5`). The builder does its own
  shaping: contextual presentation forms, lam-alef ligatures, and tanween placed over its alef. It draws the
  glyphs right to left in logical order. A hand-written ToUnicode CMap maps every glyph back to the base Arabic
  letters, so extraction returns ordinary logical-order Arabic with no presentation forms. ADD-02 Q9 and VOL-I
  9.4 make Form 4-C an Arabic-governed form, so an Authority amending it would print Arabic. A text layer, not a
  picture, is what lets the "Arabic source must be preserved" test work.
- Furniture is copied byte-for-byte from the ADD-01/02 content streams and checked with PyMuPDF on every page.
  It covers the diagonal grey "FICTIONAL — ASSESSMENT PACK" watermark (same matrix), the header "Addendum No. 3"
  / "NUPA/ISTP/2026/014" at baseline 802.2047 with its rule at y 796.5354, and the footer disclaimer, "Page N"
  (right edge 538.58) and rule at y 42.51969. The cover band (#2a2a2a, 56.69–538.58 × 74.36–114.36 td) has
  "ADDENDUM NO. 3" and, right-aligned to 528.58 at the same baselines as ADD-01/02, "Issued 1 November 2026"
  (bold) and "Tender NUPA/ISTP/2026/014". The project line, the "This Addendum …" summary and the standard
  precedence paragraph follow.
- Numbered headings (Helvetica-Bold 13), provisions (bold number, 36.85 pt hanging indent, justified Times 9.6
  on 13.4 leading) and inline ‘…’ quotes with bold new text all follow ADD-02. The "adding at the end: ‘…’" form
  follows ADD-01 5.1. The clarification grid uses the ADD-01/02 columns (90.71 / 300.47) and repeats its header
  across the page split.
- Appendix A starts a new page in the ADD-01 appendix layout: heading, one-line body, then the ADD-02 Form 4-G
  title (Helvetica-Bold 10.5) and grid (columns 96.38 / 459.21; Item / Undertaking / Confirmed). The
  justified signature line wraps exactly as in ADD-02.
- Metadata: anonymous/unspecified as in the originals, empty producer, and creation/modification date fixed at
  `D:20261101070000+00'00'` (10:00 Riyadh on the issue date).
- Extraction: default `get_text()`, `dict`, `blocks` and `words` all give clean text. `get_text(sort=True)`
  reverses the word order inside the Arabic lines. MuPDF does this for any RTL text, and PyMuPDF's own HTML
  Arabic output does the same thing and worse. I left it as a realistic hazard for the tool.

## Design: how this differs from blind-01 and blind-02

None of the blind-01 subjects are touched (date moved; 5.2 period; 6.4; 6.5; footnote 12; 8.6; 12.2; 10.5
insertion; Table 2-4 TSS; Table 2-6; Form 4-C sixth declaration; Form 4-A date). None of the blind-02 subjects
are touched either (time moved; Appendix 3; 6.8; 7.1/6.3; 10.3; 12.5; Form 4-F rows; VOL-II 3.5/4.4/8.4;
Table 2-2; 9.1 re-lettering; Index of Forms). The PDD is unchanged.

| Required element | Where | Mechanism |
|---|---|---|
| Value change in an IMAGE-ONLY table, in words, old and new | 5.1 | VOL-II Table 2-4 TP 1 → 0.5 mg/l; basis unchanged; TN (ADD-02) restated as unchanged |
| Arabic form change, Arabic text + English translation | 4.1–4.4 | Form 4-C fourth declaration replaced; old and new Arabic printed; translation "for convenience only, Arabic governs" |
| Change inside a definition | 2.1 | VOL-I 2.4 Working Day now also excludes a day notified by Addendum as an office-closure day |
| Deadline on a Friday / declared non-working day, counted in Working Days | 2.2, 3.2, 3.3, Q17 | 3.3: five WD after Sun 1 Nov = Sun 8 Nov (calendar count lands on Fri 6 Nov). 3.2: four WD before the PDD = Thu 19 Nov (a count that ignores the closure lands on the closure day, Sun 22 Nov). Q17 itself prints Sun 22 Nov |
| Deletion of a whole clause + cross-references | 6.2 | VOL-V 31.4 deleted, 39.3 (which cites it) deleted expressly, no renumbering; Schedule 11 not supplied, so cannot be checked |
| New obligation CONDITIONAL ON AN EVENT | 3.4; Arabic fourth declaration | Notify within 2 WD if the O&M Operator ceases to be a member; notify within 3 WD of becoming aware of any change in Proposal information (exclusion for breach) |
| Amendment of an ADD-01/ADD-02 provision | 7.1 (ADD-02 Form 4-G replaced); Q15 (ADD-02 response 9 amended) | Reissue of an addendum's own form; an earlier answer extended with a new obligation |
| Relationship / authority change | 3.1; 7.1–7.2 | O&M Operator must be a member holding ≥ 10%; Form 4-G countersigned by the O&M Operator or treated as not submitted |
| Quantity in VOL-V payment mechanism | 6.1 | 29.3 Ramp-Up payment 90% → 85% |
| Cover with two planted errors | cover | E1 misleading: "closure … does not affect any deadline". E2 omission: 6.1 (29.3) not listed |
| Decoy answer | Q16 | Restates VOL-II 9.4 in imperative words ("shall … whether or not it is treated"); no change |
| Table entry that changes something the narrative does not mention | Appendix A item 7 | New Form 4-G undertaking (security screening); 7.1 mentions only the countersignature |
| Genuinely ambiguous item | 3.2 vs Q17 | Same Addendum, two deadlines for the same application (Thu 19 Nov vs Sun 22 Nov). VOL-I 3.2(a) ranks Addenda only by date; VOL-I 3.3 says raise it and do not resolve it unilaterally |

Neutral items: Q18 (31.4 question moot after 6.2) and Q19 (restates VOL-I 9.4).

E1/E2 are not the blind-02 mechanisms. In blind-02, E1 was a cover statement ("PDD unchanged") contradicted by a
direct time amendment. Here E1 is contradicted only by a derived date that no sentence states: the 5.2 cut-off
moves from Thu 12 Nov to Wed 11 Nov because the closure day drops out of the count. Blind-02's E2 relied on a
misleading heading and a shared "180 days" string. Here E2 is a plain omission inside a section the cover
half-describes ("deletes Volume V Clause 31.4").

## Traps and intended reasoning

- **E1 and the cut-off.** A reader that trusts the cover keeps Thu 12 Nov 2026 for clarifications. The correct
  date is Wed 11 Nov 2026: 10 WD back from Thu 26 Nov, the 26th not counted, Fri/Sat and Sun 22 Nov skipped.
- **Arabic governs.** The Arabic says "ثلاثة أيام عمل" (three Working Days). The English translation says
  "three (3) days". By 4.3 and VOL-I 9.4 the period is three Working Days. The tool must keep the Arabic
  verbatim as the source text and must not replace it by the translation.
- **4.4 chain.** A Form 4-C with the old fourth declaration is not properly executed, so VOL-I 9.4 makes the
  Proposal non-responsive (stated, high confidence).
- **7.2 chain.** No O&M countersignature means the form is "treated as not submitted", so ADD-02 7.2 makes the
  Proposal non-responsive (stated, high confidence).
- **8.8 has no stated consequence.** Non-compliance is a fail only by inference from Section 8's heading and
  VOL-I 11.1(i). A3 should carry it at medium confidence.
- **Knock-ons a careful reader adds.** The O&M Operator, once a member, needs its own Form 4-C (9.4 "each
  member"). It counts in the 8.4 weighting and falls under 8.2. Its admission needs 8.1 consent, and an
  unapproved change means rejection.
- **Image-only table.** The Table 2-4 image still shows 1 mg/l. Only the words of 5.1 change it to 0.5. The
  knock-ons are the 7.2/7.3 reliability run, VOL-V 31.1(b), and the 29.3 Ramp-Up relief, which still covers TP
  because TP stays on a rolling-average basis.
- **Deletion.** 31.4 and 39.3 are both gone and nothing is renumbered. Q18 is not a second deletion. The
  deletion is contract-stage, not an A3 item.
- **Decoy and neutral answers.** Q16 and Q19 change nothing.
- **Friday trap.** 3.3 counted in calendar days gives Fri 6 Nov. The correct date is Sun 8 Nov, or Thu 5 Nov
  if the tool states that it counts the issue day.

## Deliberate ambiguities

1. **A1 (the "no correct answer" item):** 3.2 (Thu 19 Nov 2026) vs Q17 (Sun 22 Nov 2026, the closure day,
   Portal open). Expected: escalate with both sources. A labelled conservative planning date of 19 Nov is fine.
   No machine resolution.
2. The forward-count convention for 3.3 (accept 5 Nov if stated).
3. Whether the amended 2.4 governs Volume V Working-Day periods (29.4, 34.3). Accept either if flagged.
4. The consequences that are not stated: Q15 translation, 3.3 notice, 8.8 breach.
5. The validity-date convention, as in earlier rehearsals.

## Internal-consistency checks done

- Every quoted "old" string and every pre-ADD-03 text in `state_before` was matched by script against the
  extracted pack text: VOL-I 2.4, 5.2, 8.1, 8.8, 9.4; VOL-II 9.4; VOL-V 29.3, 31.4, 39.3; ADD-02 7.1, 7.2 and
  responses 9 and 10. ADD-01 2.1 was checked for the PDD.
- The Arabic of the fourth declaration as issued was read from the Form 4-C image at high resolution and
  matches it word for word. Form 4-G items 1–6 in Appendix A match ADD-02 verbatim, checked by script.
- Every cited clause, table, form and answer exists: VOL-I 2.4, 3.2, 3.3, 5.2, 5.3, 8.1, 8.8, 9.4, 11.1; VOL-II
  Table 2-4, Section 3, 9.4; VOL-IV Form 4-C, Form 4-G; VOL-V 29.3, 31.4, 39.3; ADD-02 Section 7, 7.2 and
  response 9.
- Dates were computed by script. The issue date, Sun 1 Nov 2026, is after ADD-02 (Thu 22 Oct) and before both
  the old (Thu 12 Nov) and new (Wed 11 Nov) clarification cut-offs. Every new deadline (8 Nov, 19 Nov) falls
  after the issue date and before the PDD. No Saudi public holiday falls in Oct–Nov 2026.
- Nothing is renumbered. The 8.8 addition is appended at the end of the clause. 31.4 and 39.3 are removed with
  an express "not renumbered".
- The extracted Arabic equals the builder's source strings exactly (whitespace-normalised), and no
  presentation-form code points appear in the extraction.

## Verification

- Two builds give identical bytes.
- The repository PDF hash is in `SHA256SUMS`.
- PyMuPDF checks:
  - 4 pages;
  - Latin span fonts ⊆ {Helvetica, Helvetica-Bold, Times-Roman, Times-Bold};
  - Arabic spans only in FreeSerif;
  - watermark, header and footer spans (font, size, origin, direction, colour) equal to ADD-02 on every page;
  - header and footer rules, the cover band rectangle and the cover text right edges equal to ADD-01/02.

```
cd <this sealed directory>   && sha256sum -c --ignore-missing SHA256SUMS   # three sealed files
cd <repository root>         && sha256sum -c --ignore-missing <sealed>/SHA256SUMS   # the PDF
```
