# Blind rehearsal 08: author notes (SEALED). SYNTHETIC: not tender content

## Input and status

- **The input:** `ADD-03_Addendum_No_3.pdf`, 4 pages, A4, printed "Issued 18 November 2026" (a Wednesday).
- **What it stands on:** the base pack (Volumes I, II, IV, V) as amended by ADD-01 and ADD-02 only. It stacks on no
  rehearsal's addendum. Volume III was never supplied and is not used.
- **Label:** "SYNTHETIC: not tender content" appears:
  - in the text layer of the page 1 cover, as its own line under the project name;
  - in the Subject, Keywords and Producer metadata;
  - in the image footer, as pixels.
- **Producer line:** `blind-08 build_addendum.py (PyMuPDF 1.28.2) - SYNTHETIC: not tender content`. I chose a truthful
  producer over imitating the pack's ReportLab string.
- **Author:** an independent, cold-started agent. Model claude-opus-5-5 (Opus 5.5); the runtime showed a
  reasoning-effort setting of 15.
- **Times:** started 2026-10-07T07:02:58Z, ended 2026-10-07T07:22:28Z. Elapsed 19 min 30 s.
- **The files in this folder:**
  - `ADD-03_Addendum_No_3.pdf`;
  - `build_addendum.py`;
  - `expected_findings.yaml`, the key;
  - this note;
  - `SHA256SUMS`.

**Build and verify (from the repository root, read-only):**
`.venv/bin/python -I <sealed>/build_addendum.py <out.pdf> --check sources/candidate_pack --verify-key <sealed>/expected_findings.yaml`

The builder refuses to run unless all of these hold:
- PyMuPDF is 1.28.2;
- numpy is 2.4.6;
- the FreeSerif and FreeSerif Bold font files match their pinned SHA-256 values.

Three builds gave identical bytes, sha256 `6a7adf78…4b74164`. The full hash is in `SHA256SUMS`.

## What I read

- **The six pack PDFs, in full** (PyMuPDF text with the watermark dropped), and both pack images:
  - the Volume II Table 2-4 raster;
  - the Form 4-C raster.
- **The brief and the three correspondence `.md` files.** From these I took three points:
  - "a PDF in the same format as Addenda 1 and 2";
  - the planning date is the latest addendum date;
  - Volume III is referenced but not supplied.
- **The input PDFs of blind-01 to blind-07** (including blind-06's ADD-04), read only to avoid their subjects.
- **The blind-07 technique example:** `rehearsals/blind-07/SEALED/author_notes.md` and `build_addendum.py`. I copied
  from that builder, unchanged in substance:
  - the layout engine, furniture, grid, Arabic line shaper and raster pipeline (its lines 28-619);
  - the pattern of its `--check` and self-check.

  All content is new.

What I did not open:
- the `.eml`, the Gmail PDF and the PNG in correspondence;
- the tool's code, tests, curation, config, outputs, docs, work logs, staging;
- any rehearsal's work, outputs, comparison or key;
- any `SEALED/` file other than the two allowed blind-07 files.

What I wrote and ran:
- Nothing was written in the repository.
- No git command was run.
- Scratch files lived in `_work/` inside this folder and were deleted before sealing.

One discrepancy with the brief: it says ADD-02 carried an Arabic table image. It does not. ADD-02 has no image at all.
The pack's images are Volume II Table 2-4 (English) and Form 4-C (Arabic). I followed the Volume II reproduction
convention, which is also what blind-07 did.

## Subjects avoided, and what this ADD-03 touches

The earlier rehearsals' subjects are listed in the blind-07 notes and confirmed from the seven input PDFs. They
include:
- **Volume I:** PDD and time, 2.4, 4.2, 5.2, 6.3-6.8, 7.1, 8.1, 8.3-8.8, 9.1 re-lettering, 9.2/9.4/9.6/9.7 (questions),
  10.1/10.3/10.5/10.6, 11.3, Table 1-1, 12.2/12.3/12.5, Appendices 2 and 3.
- **Volume II:** 1.3, 1.4, 2.3, 3.1-3.5, 4.4, 5.2-5.4, new 5.6, 6.1, 6.4, 7.2, 7.4, 8.1-8.5, 9.3, 9.4, Tables 2-2/2-4/2-6.
- **Forms:** 4-A, 4-C, 4-E, 4-F rows, 4-G, 4-H.
- **Volume V:** 1.1, 1.1A, 1.3, 3.1 (question), 12.5, 18.1, 29.2, 29.3, 31.1, 31.4, 36.2, 39.3, 39.5/40.2, 42.1-42.3.

This ADD-03 uses only subjects none of them touched:
- **VOL-I 8.9** (investment licence), replaced, with a new **Table 8-1** made part of Volume I. Table 8-1 is an
  Arabic image of a fictional "Northern Region Investment Services Office" letter, No. 228/2026, dated Mon 16 Nov 2026.
- **The treated effluent storage reservoir** of VOL-II 1.2, given a capacity rule in a new **VOL-II 4.6**.
- **VOL-V 12.1** (Scheduled PCOD, 36 → 42 months).
- **VOL-V 39.4** (Authority Event of Default amount, −40%).
- **Q17**, the arbitration restatement on VOL-V 44.2.

Form 4-D, VOL-V 18.x/39.2/40.1 and Table 1-1 criterion B appear only as indirect effects and are not amended. That
blind-04 amended 18.1 is the reason I did not touch Clause 18 directly.

## Design: how each required element is exercised

| Brief item | Key ids | Mechanism |
|---|---|---|
| (1) Image | IMG1, AR1 | **Table 8-1, image only, page 3.** The issue periods (٣ / ٥ / ٨ Working Days) drive the A5 lead times, and Note ١ fixes the forward counting rule. The English row 2 says 3 while the Arabic says ٥; "the Arabic text governs" (S1). |
| (2) Calculations | C1-C4 | **C1:** 39.4, SAR 20,000,000 reduced BY 40% = SAR 12,000,000 (the cover's 8,000,000 is 40% OF it).<br>**C2:** 12.1, 36 + 6 = 42 months.<br>**C3:** Q16 reduces row 2 by 2 WD from the governing Arabic value. 5 − 2 = 3 is right; 3 − 2 = 1 is the stale English base. It applies only to applications lodged by Sun 22 Nov.<br>**C4:** reservoir arithmetic under both readings of GA1. |
| (3) New obligations | N1-N6 | **N1:** licence or Certificate in Envelope A, on pain of rejection (new A3 item).<br>**N2:** Office applications with drop-dead dates.<br>**N3:** Portal notification by Mon 23 Nov (A5, not A3).<br>**N4:** 2.4 undertakings.<br>**N5:** reservoir requirements.<br>**N6:** reflect in the process design, the programme and the Financial Model. |
| (4) Indirect effects | IE1-IE8 | **IE1:** 9.1(i) / 10.1 envelope placement.<br>**IE2:** the 8.9 modality change creates an A3 entry and retires the undertaking route.<br>**IE3:** image values → A5 dates, with row 3 infeasible.<br>**IE4:** Q16 modifies a value that exists only in the image.<br>**IE5:** 12.1 → 18.1/18.3/39.2.<br>**IE6:** 12.1 → Form 4-D (not to be altered).<br>**IE7:** criterion B is 15 marks (ADD-02, not the base 20) and feeds Form 4-F.<br>**IE8:** 39.4 → 40.1 and Form 4-E deemed acceptance. |
| (5) Ambiguity | GA1; S1-S5 | **GA1:** "six (6) hours of the design flow". The average daily flow gives 30,000 m3; the peak hourly flow (design) gives 45,000 m3. "Design flow" appears nowhere in the pack (the builder asserts its absence). Clarification is closed because the issue is after the cut-off, and Q18 only points back.<br>**S1:** Arabic governs.<br>**S2:** "as issued" against recital 1.2's "unless otherwise stated".<br>**S3:** VOL-I 2.4 backward counting gives Mon 23 Nov.<br>**S4:** Note ١ forward counting.<br>**S5:** an addendum issued after the cut-off is valid. |
| (6) Structure | ST1-ST4 | **ST1:** inserted VOL-II 4.6.<br>**ST2:** scoped exception 2.4.<br>**ST3:** Table 8-1 forms part of Volume I.<br>**ST4:** 8.9 replaced. |
| (7) Cover errors | E1-E3 | **E1:** figure (SAR 8,000,000).<br>**E2:** count ("15 to 20"; there are five requests, 15-19).<br>**E3:** modality ("failing which the Proposal will be rejected" for the 2.5 notification, which has no stated consequence).<br>Two true cover statements are listed so that they are not over-flagged. |
| (8) Decoys | DC1-DC9, MNR01-22, AIR1-9 | Restatements (2.6, 4.2, Q17), a numbering note (3.2), pointers (Q18, Q19), recitals and the SYNTHETIC label. Twenty-two must-not-report claims; nine acceptable-if-raised points. |

## Timing choice (deliberate)

The cut-off is Thu 12 Nov (10 WD before Thu 26 Nov, counted backwards). The Office letter is dated Mon 16 Nov and
ADD-03 is issued Wed 18 Nov, which leaves **6 Working Days** to the PDD. The short window is the point.

| Class | Latest lodging | Why |
|---|---|---|
| Row 1 | Sun 22 Nov | 3 WD gives issue on Wed 25 Nov. |
| Row 2 | Sun 22 Nov | Only with the Q16 reduction. Lodging on Mon 23 Nov loses it, and 5 WD runs to Mon 30 Nov. |
| Row 3 | — | Would have needed Sun 15 Nov, before the Addendum existed. It must be escalated, not scheduled. |

A planner that reads the English row 2 (3 WD) would schedule Mon 23 Nov. A planner that misapplies Q16 would schedule
Wed 25 Nov. Both are wrong.

## What a scorer should weigh most

1. **GA1 surfaced and not decided.** Both volumes shown, and the item placed in A3's "could not resolve" list. This is
   the brief's "one has no correct answer" case.
2. **The image read correctly:** row 2 = 5 and Arabic governs. C3 is computed from the governing value.
3. **A3 discipline.**
   - New 8.9 is in A3.
   - The 2.5 notification is not, despite the cover (E3).
   - The 2.4 undertaking is not a stated ground; flagging it as a risk is fine.
4. **The row 3 infeasibility** is flagged rather than scheduled.
5. **C1 = SAR 12,000,000**, and all three cover errors are detected.
6. **Indirect effects.** IE5-IE7 matter most for A5 and for pricing.

Lower weight:
- whether IE8 or the AIR points are mentioned;
- the exact wording of activity names.

## Internal-consistency checks done

- **`--check`:**
  - 4 "old" pack texts each occur exactly once;
  - 43 `state_before` quotes are verbatim, with their pages;
  - "design flow" is absent from all six pack PDFs;
  - every date, figure and the 6-WD count is asserted in code.
- **Self-check:**
  - 38 key strings are in the built text layer;
  - there is no Arabic code point in the text layer;
  - the planted phrases occur once each.
- **`--verify-key`:**
  - 62 ADD-03 quotes are on their stated pages;
  - 23 pack quotes are verbatim on their stated pages;
  - 17 Arabic strings equal the source dictionary that the image is rendered from.
- **Visual checks of the raster** (1750 x 1750 px, RGB with equal channels, FlateDecode):
  - the number direction is correct in ٢٢٨/٢٠٢٦, ١٦ نوفمبر ٢٠٢٦م and ٨-١ (pixel-checked);
  - the parentheses mirror correctly around the tender number;
  - the signature and stamp do not overlap the text.
- **Fonts:** the text layer uses Helvetica, Helvetica-Bold, Times-Roman and Times-Bold (Type1, WinAnsi, not embedded),
  as in ADD-01/02. The header, footer, watermark and "Page N" are as in ADD-01/02.
- **Assumption (also in the key):** no public holiday in the Kingdom between 22 Oct and 30 Nov 2026.
