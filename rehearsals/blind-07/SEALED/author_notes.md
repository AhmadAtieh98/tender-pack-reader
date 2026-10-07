# Blind rehearsal 07: author notes (SEALED)

## Input and status

- **The input:** `rehearsals/blind-07/input/ADD-03_Addendum_No_3.pdf`, 4 pages, "Issued 17 November 2026" (a
  Tuesday).
- **What it stands on:** the base pack as amended by ADD-01 and ADD-02 only. It stacks on no rehearsal's
  addendum.
- **Answer key:** `expected_findings.yaml` in this directory.
- **Builder:** `build_addendum.py`, also in this directory.
- **Author:** independent and cold-started. Model claude-opus-5-5 (Opus 5.5); the runtime showed a reasoning-effort
  setting of 40.

**Build command:**
`.venv/bin/python -I build_addendum.py <out.pdf> [--check sources/candidate_pack]`

The builder refuses to run unless all of these hold:
- PyMuPDF is 1.28.2;
- numpy is 2.4.6;
- `FreeSerif.ttf` and `FreeSerifBold.ttf` in `/usr/share/fonts/truetype/freefont/` have the pinned SHA-256 values.
  The Arabic raster depends on them.

Four builds produced identical bytes: the repository copy, two repeats and an earlier test build.

## What I read

I read only the allowed sources.

- **The six pack PDFs, in full.**
  - Source: PyMuPDF text, with the rotated watermark lines dropped.
  - Volumes: I, II, IV, V, ADD-01 and ADD-02.
  - Images: the Volume II Table 2-4 image and the Volume IV Form 4-C image, extracted at full resolution and read.
  - From Form 4-C I took the fifth declaration, which refers to Volume I Clause 4.2 as "البند ٤-٢ من المجلد الأول".
- **The brief and correspondence.**
  - `sources/brief/Lamar_PPP_AI_Partner_Round2_Brief.pdf`.
  - The three correspondence `.md` files. From these I took two points:
    - "a PDF in the same format as Addenda 1 and 2";
    - planning date = latest addendum date.
- **The blind-01 to blind-06 input PDFs** (including blind-06's ADD-04), read only to list their subjects.
- **The blind-06 technique example:** `rehearsals/blind-06/SEALED/build_addendum.py` and `author_notes.md`.
  - These are a technique and style example only.
  - I adapted from that builder, and checked against ADD-01/02, the following:
    - the layout engine;
    - the furniture function;
    - the cover band;
    - the clarification grid;
    - the Arabic line shaper;
    - the raster pipeline.

What I did not open:
- In `sources/correspondence/`: the `.eml`, the Gmail PDF and the PNG.
- `sources/manifest.json`.
- Any `expected_findings.yaml`.
- The tool's code (`tenderpack/`), tests, `curation/`, `config/`, `build/`, `out/`, `out-drill*/`, `docs/`,
  `worklog/`, `scripts/` and `staging/`.
- Any rehearsal's `work/`, `out-*`, `review*`, `candidate-curation/`, `proposals/`, `batches/`, `downstream/`,
  `COMPARISON.md`, `REGRESSION*.md`, `FROZEN*`, or any `SEALED/` other than the two allowed blind-06 files.

What I wrote and ran:
- Inside the repository, the only file written is the PDF. Its directory, `rehearsals/blind-07/input/`, had to be
  created.
- No git command was run.

## Subjects avoided

These are listed from the blind-01 to blind-06 input PDFs.

- **blind-01:**
  - Proposal Due Date (PDD); 5.2; 6.4; 6.5; footnote 12; 8.6; new 10.5 and the renumbering; 12.2.
  - Table 2-4 TSS; Table 2-6 row 2-6.2; Form 4-C sixth declaration.
  - Questions on: the Local Content Certificate (LCC); control room (VOL-II 6.1); affiliate references; total nitrogen
    (TN) in the reliability run; the site visit; the page limit.
- **blind-02:**
  - 6.1 time; Appendix 3; new 6.8; 7.1 and 6.3; 10.3 and new 12.5 (Vol I); Form 4-F audit rows.
  - VOL-II 3.5, 4.4 and 8.4; Table 2-2; 9.1 re-lettering; Index of Forms.
  - Questions on: foreign-branch Bid Bond; Power of Attorney (PoA) legalisation; Operation and Maintenance (O&M)
    security; term start; Financial Model USB; PDD extension.
- **blind-03:**
  - Working Day definition and office closure; 8.8 and 8.1; Form 4-C fourth declaration; Table 2-4 TP.
  - VOL-V 29.3, 31.4 and 39.3; Form 4-G reissue.
  - Questions on: the Form 4-C translation; construction water; the consent deadline; Form 4-C signatories.
- **blind-04:**
  - Estimated Project Cost; 8.4; 18.1; VOL-II 5.2; ADD-01 5.1 crossings; Table 1-1 second revision; 11.3/11.3A.
  - Conditional VOL-II 1.4; Form 4-H (Arabic image).
  - Questions on: the Parent Company Guarantee (PCG); grid; Appendix C; velocity at crossings; 8.4(a); register
    legalisation.
- **blind-05:**
  - 6.6/6.7 merger; VOL-V 1.1 and 1.1A; 29.2; VOL-II 3.1 membranes; 3.4 odour via ESIA Figure 7-2.
  - New VOL-II 5.6 and Arabic Table 5-1.
  - Questions on: 6.4 data retention; Form 4-E; ISO 9001 for joint ventures; dispersion modelling; Form 4-F year 1 and
    the Indexed Proportion row; crane plan.
- **blind-06:**
  - VOL-II 1.3 and Table 1-3 tie-ins; 7.2; 8.1-8.3; VOL-V 31.1 and 31.3; 12.3 and 7.4 via answers.
  - Ozonation (3.3); Relief Event for low flow.
  - ADD-04: ADD-03 2.5; 8.2 reinstated; Appendix 2.

What this ADD-03 touches, all unused by blind-01 to blind-06:
- VOL-V 36.2 (only ADD-02 had touched it);
- VOL-II 8.5 relocated to VOL-V 42.3, and VOL-V 42.1 with the new Arabic Table 42-1 (handback);
- new VOL-V 12.5 (ground conditions);
- VOL-I 4.2 (blackout, by disapplication);
- VOL-I 10.1/10.6 (financing-assumptions schedule);
- VOL-V 39.5/40.2 (Direct Agreement);
- VOL-II 9.3 (grievance);
- the Pre-Bid minutes language.

Points near earlier rehearsals, each judged different:
- blind-06's 4.2 mentioned 8.5 only as "unchanged".
- Form 4-C appears only as an indirect effect (its fifth declaration cites 4.2). It is not amended.
- The relocated survey keeps the words "of the concession". I left the term-start question (blind-02) alone and list
  it only under `acceptable_if_raised`.

Missing evidence avoids the excluded items: the Environmental Permit, Schedule 11, any Appendix C and any ESIA figure.
- **ME1:** the Geotechnical Baseline Report, Revision C.
- **ME2:** the Authority's five-point condition grading scale.

## Cut-off choice (deliberate)

The Volume I 5.2 cut-off is ten Working Days before Thursday 26 November, counted backwards with the stated date not
counted (2.4). That gives Thursday 12 November 2026.

**ADD-03 issues after the cut-off,** on Tuesday 17 November. Recital 1.3 records that requests 15 to 19 arrived before
it. This has three effects:
- No Bidder can raise a clarification on ADD-03 itself, so the composite-asset ambiguity (DA1) and the Direct Agreement
  question (HJ1) must go to a person. Volume I 3.3 makes a unilateral resolution the Bidder's own risk.
- The planning date becomes 17 November, with 7 Working Days to the PDD.
- The core-inspection request window (4.3) falls after the cut-off.

The issue is still valid: 5.2 limits requests, not Addenda. "Invalid addendum" is a must-not-report item.

## Design

| Required element | Where | Mechanism |
|---|---|---|
| Change types an engine may lack | CT1-CT7 | **CT1:** relative delta on a value already amended by ADD-02 (36.2: "reduced by SAR 1,000,000"; result SAR 1,500,000 via recital 1.2).<br>**CT2:** cross-volume relocation with text unchanged, the number not reused and no renumbering. Rank moves from (d) to (c), and the clause enters Form 4-E's scope.<br>**CT3:** a single value replaced by a per-class schedule held only in a governing Arabic image, with a months cell under a years heading.<br>**CT4:** bounded disapplication of a disqualification clause with no text change in the target (4.4 on VOL-I 4.2).<br>**CT5:** an answer that deems a document part of a Form (answer 17) and adds content.<br>**CT6:** an operative-sounding note only in the convenience translation, with no force.<br>**CT7:** a new clause triggered by an unsupplied external document (12.5 and the Geotechnical Baseline Report (GBR) Rev C). |
| Indirect effects | IE1-IE9 | **ADD-01 response 4 made incomplete or wrong** by new 12.5 (IE1).<br>Relocation → Form 4-E and the Volume V deemed-acceptance note (IE2).<br>12.5 → Scheduled PCOD → 18.1 / 18.3 / 39.2 (IE3).<br>Arabic row 4 → VOL-II 2.2 lifecycle → Financial Model and 42.2 (IE4).<br>Months versus years against VOL-II 3.2 (IE5).<br>36.2 chain (IE6).<br>4.4 → A3 4.2 → Form 4-C fifth declaration in the image; 4.1 not disapplied (IE7).<br>Answer 17 → 10.1, Form 4-F, 6.2 (IE8).<br>Computed date D2 (IE9). |
| Computed dates | D0-D5 | **D1** is stated: Mon 23 Nov (3 WD before the PDD, backwards per 2.4).<br>**D2** is NOT stated, because the pack has no forward rule: Sun 22 Nov if the issue day is not counted, Thu 19 Nov if it is. The key says to plan to Thu 19 Nov and flag.<br>**D3** (the 12.5 notice) is event-based and its counting rule is not stated. |
| Misleading cover (3 new mechanisms) | cover | **E1:** stale-base arithmetic ("to SAR 4,000,000" is base 5.0M less 1.0M; the truth is 1.5M).<br>**E2:** modality downgrade ("invites Bidders to describe" against 3.6 "shall demonstrate").<br>**E3:** cardinality error ("four asset classes" against five rows).<br>None of these is a contradiction, an omission, a derived-date closure, a direction reversal, a half-truth, an over-generalisation, a wrong clause number, a scope word, a phantom provision, a temporal anchor or an actor substitution. I also removed an unplanned over-generalisation from my draft cover ("in their designs" became "for the design of foundations"). |
| Missing evidence | ME1, ME2 | **ME1:** GBR Revision C, cited in 12.5, 4.2 and 4.3 and not supplied. It may or may not be the ADD-01 response 4 "geotechnical report".<br>**ME2:** the condition grading scale. Only grade 1 is defined, yet the table's maxima are grades 2 and 3. |
| Image-only, Arabic governs | App. A p.3 | Table 42-1: an Asset Transfer Committee letter No. 417/2026 of Sun 15 Nov, with 5 rows, 4 columns, units (years, and months in row 5), 3 notes, a signature and a stamp.<br>**AR1:** row 4 is ٧ (7) in the Arabic and 5 in the English.<br>**AR2:** row 5 is ٢٤ شهراً (24 months) in the Arabic and "24" under a years heading in the English.<br>**AR3:** English note (4) has no Arabic counterpart and no force. |
| Answers | 15-19 | 15 decoy (minutes in Arabic).<br>16 confirming in imperative words (VOL-II 9.3).<br>17 changing (schedule is part of Form 4-F; DSCR added; 6.2 applies).<br>18 human judgment (Direct Agreement against 40.2; "The order of precedence at Volume I Clause 3.2 applies" is printed and does not settle it, because the Direct Agreement is not an RFP Document under 3.1).<br>19 confirming of 4.3. |
| Genuine ambiguity | DA1 | Composite electro-mechanical assets (pump sets): mechanical 5 years or electrical/I&C 7 years under the governing Arabic. It is invisible in the English, which reads 5 and 5. No correct answer; escalate. |
| Must-not-report | key | 24 items. |

## Traps and intended reasoning

- **36.2.** Apply the delta to ADD-02's figure, because recital 1.2 says references are to clauses as amended. Report
  SAR 1,500,000 and the chain 5.0M → 2.5M → 1.5M. The cover's 4.0M is E1.
- **Handback.**
  - Relocation is not deletion. The survey text is unchanged and Volume II is not renumbered.
  - 42.1 now points to 42.3 and to Table 42-1.
  - Read the image: there are five classes, electrical/I&C is 7 years, and membranes are 24 months.
  - Appendix B note (4) is English-only and has no force; VOL-II 2.2 is unchanged.
  - 3.6 is mandatory, scored under criterion C, and not an A3 item (E2).
- **Ground conditions.**
  - 12.5 gives time and cost. It is not a Relief Event, and it does not engage VOL-V 3.3, which concerns the term.
  - ADD-01 response 4 becomes incomplete.
  - The baseline report is missing (ME1).
- **4.4.** Only 4.2 is disapplied, and only narrowly. VOL-I 4.1 still applies. Form 4-C needs no change.
- **Answers.** 15 and 16 have no effect. 17 changes. 18 must be escalated. 19 points to 4.3, so plan to Thu 19 Nov.
- **Dates.** The issue date is after the cut-off and valid. 7 Working Days remain. D2 has two readings.

## Internal-consistency checks done

- **Pack quotations.** The builder's `--check` verifies, against the pack text with the watermark removed:
  - the 3 "old" texts quoted by ADD-03, each asserted to occur exactly once in its volume: VOL-II 8.5,
    "Volume II Clause 8.5" in VOL-V, and the 42.1 design-life phrase;
  - the 43 `state_before` quotations, with their page numbers.
- **Built text layer.** After the build, the builder's `self_check` asserts:
  - the cover, every provision, every question and response, every English table row and note, and the issue date are
    in the PDF text layer (40 strings);
  - no Arabic code point is in the text layer;
  - the 4.3 phrases, "SAR 4,000,000" and "SAR 1,000,000" each occur exactly once.
- **The key.** It is generated from the builder's own strings by a separate script, which checks that:
  - every provision text, question, response and the cover is in the built PDF;
  - each planted error's `cover_says` is in the cover;
  - every `state_before` entry is verbatim in the pack;
  - the Arabic strings equal the builder's source dictionary, which is what the image is rendered from. A YAML
    round-trip confirmed this.
- **Arabic layout.**
  - Each Arabic line and cell is asserted to fit.
  - The manual header breaks join back to the full strings.
  - The image was inspected: the bidi of ٤٢-١, ٤١٧/٢٠٢٦ and NUPA/ISTP/2026/014 is correct, and the diacritics
    (تُقيَّم، المكوَّن، يُستبدَل، وُجدت، مبيَّن) are correct.
  - The image is 1750 x 1700 px, RGB with equal channels, FlateDecode, with a `FormXob.<md5>` name, placed at
    x = 56.69 over the full frame width.
  - Whole-image mean is 239.5, against 237.2 for the pack's Table 2-4.
- **Dates.** All are computed and asserted in the builder:
  - Volume I 2.4 Working Days (Sunday to Thursday);
  - backward counts do not count the stated date;
  - forward counts are computed under both readings;
  - the order is ADD-02 (Thu 22 Oct) < cut-off (Thu 12 Nov) < letter (Sun 15 Nov) < issue (Tue 17 Nov) < PDD
    (Thu 26 Nov);
  - no public holiday in the Kingdom is assumed for October to December 2026. This is an external assumption, stated
    in the key.
- **Cross-references.** Every cited item exists:
  - VOL-I 2.4, 3.1-3.3, 4.1, 4.2, 5.2, 5.3, 6.2, 10.1, 10.6;
  - VOL-II 2.2, 3.2, 8.5, 9.3;
  - VOL-V 12.1-12.4, 36.2, 39.5, 40.2, 42.1;
  - ADD-01 Appendix B and 3.2;
  - Forms 4-A, 4-E, 4-F.

  Table 42-1, VOL-V 12.5 and 42.3 are new by design. The GBR Revision C and the grading scale are deliberately not
  supplied.
- **Furniture.**
  - On all 4 pages, the watermark, header, footer and "Page N" spans match the ADD-01/02 spans in text, font, size,
    origin, direction and colour. The header and footer rules match.
  - Fonts are {Helvetica, Helvetica-Bold, Times-Roman, Times-Bold}, Type1 WinAnsi, not embedded.
  - Metadata follows the ADD-01/02 conventions:
    - "(anonymous)" and "(unspecified)";
    - producer "ReportLab PDF Library - (opensource)";
    - dates `D:20261117102501+00'00'`;
    - `%PDF-1.4`;
    - a fixed two-half /ID.

## Verification

```
cd <this sealed directory>  && sha256sum -c --ignore-missing SHA256SUMS            # three sealed files
cd <repository root>        && sha256sum -c --ignore-missing <sealed>/SHA256SUMS   # the PDF
```
