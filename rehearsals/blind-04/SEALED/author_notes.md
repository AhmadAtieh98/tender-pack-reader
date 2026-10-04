# Blind rehearsal 04: author notes (SEALED)

Input: `rehearsals/blind-04/input/ADD-03_Addendum_No_3.pdf` (5 pages, "Issued 9 November 2026", a Monday).
Answer key: `expected_findings.yaml` in this directory. Builder: `build_addendum.py`. Author: W6, working cold.
PDF SHA-256: `99728136b5653acdd75d0e7b682f990f877ae2587452ffee58be0bd85b28452e`. Model: claude-opus-5-5 (per the system prompt); the session record from `get_session` shows
configured_model claude-opus-5-5 and session_context.model / last_served_model claude-fable-5-1.

The builder is deterministic. Run `python build_addendum.py out.pdf [--check <candidate_pack_dir>]` with the
repository's virtualenv and it gives identical bytes on every run. I built twice and the SHA-256 matched. It
refuses to run unless these are exactly as pinned:

- PyMuPDF 1.28.2 and numpy 2.4.6;
- `/usr/share/fonts/truetype/freefont/FreeSerif.ttf` (`c57bf5de…b7d2`) and `FreeSerifBold.ttf`
  (`f078f2ac…0f4d`), because the Arabic raster depends on them.

`--check` re-verifies every quotation against the pack and prints the derived dates and figures.

## What I read

Allowed sources only:

- the six pack PDFs (VOL-I, VOL-II, VOL-IV, VOL-V, ADD-01, ADD-02), read in full. I rendered the VOL-II
  Table 2-4 image and the VOL-IV Form 4-C image and read them at full resolution;
- the brief (`sources/brief/…Round2_Brief.pdf`) and the three correspondence `.md` files
  (`sources/correspondence/`). These gave me the A1–A5 meanings, the "same format as Addenda 1 and 2" reply,
  the three-member planning assumption and the rule that the planning date is the latest addendum date;
- the blind-01, blind-02 and blind-03 input PDFs, only to list their subjects and avoid them;
- `rehearsals/blind-03/SEALED/build_addendum.py` and `author_notes.md`, as a technique and style example. The
  layout engine and the furniture strings are adapted from that builder.

I did not open the tool's code (`tenderpack/`), the tests, `curation/`, `config/`, `build/`, `out*/`,
`docs/`, `worklog/`, `scripts/` or `staging/`. Nor did I open any rehearsal's `work/`, `out-*`,
`COMPARISON.md` or `expected_findings.yaml`, or the blind-03 key. I did not read the `.eml` or Gmail PDF in
`correspondence/`.

The only file I wrote inside the repository is the input PDF; its directory `rehearsals/blind-04/input/` had
to be created. `git status` was run once, read-only. Nothing was staged or committed.

## Style fidelity

**Fonts and the absence of Arabic text.** The text layer uses only Base-14 Type1 fonts (Helvetica,
Helvetica-Bold, Times-Roman, Times-Bold, WinAnsi, not embedded), as in ADD-01 and ADD-02. There are no
embedded fonts and no Arabic in the text layer. Blind-03 departed from this to set Arabic as text. This
addendum does not: the Arabic is carried by an image page, which is how the issued pack itself carries Arabic
(VOL-IV Form 4-C).

**Furniture.** It is copied byte-for-byte from the ADD-01/02 content streams:

- the diagonal "FICTIONAL — ASSESSMENT PACK" watermark;
- the header "Addendum No. 3" / "NUPA/ISTP/2026/014" and its rule;
- the footer disclaimer, "Page N" and its rule.

I checked with PyMuPDF that the watermark, header and footer spans (text, font, size, origin, direction and
colour) equal ADD-02 page 1 on all 5 pages. The rules and the cover band rectangle (56.69–538.58 × 74.36–114.36)
are equal too.

**Body layout.** These follow ADD-02:

- the cover band, the project line, the summary and the standard precedence paragraph;
- numbered headings (Helvetica-Bold 13);
- provisions in justified Times 9.6 on 13.4 leading, with a bold number and a 36.85 pt hanging indent;
- inline ‘…’ quotes with the new text in bold;
- the quoted-clause style of ADD-02 9.1 (‘**11.3** …’).

**Table 1-1 (second revision).** It copies the ADD-02 Table 1-1 geometry, measured from its raw stream:

- columns 70.87 / 116.22 / 467.72 / 524.41, with 17.4 pt rows;
- a Helvetica-Bold 8.5 title, 17 pt below the provision and 3 pt above the grid;
- a bold Total row;
- the short centred 0.5 pt rule (223.94 → 371.34), 3 pt below the grid;
- "Notes to …" in Times 7.2 on 9 pt leading with "(n)" plus two spaces.

**Clarification grid.** It uses the ADD-01/02 columns (90.71 / 300.47).

**Image page (page 4).** It is drawn exactly as VOL-IV page 6 draws Form 4-C:

- `q 1 0 0 1 66.61417 120.1246 cm q 462.0472 0 0 653.403 0 0 cm /FormXob.<md5> Do Q Q`, drawn after the
  furniture (so the image covers the watermark, as in VOL-IV);
- an RGB 8-bit FlateDecode raster of 1654 × 2339 px (A4 at 200 dpi), the same as the pack's;
- an XObject named in ReportLab's `FormXob.<md5>` convention.

The raster is made from a vector master:

- the Arabic is shaped by MuPDF's HTML engine (HarfBuzz) in FreeSerif and FreeSerifBold;
- the English is in Times;
- the layout mirrors Form 4-C: a bilingual header box, "FORM 4-H" and "النموذج ٤-ح", a bold title, numbered
  declarations, field lines with the Arabic label right and the English label left, the note, and the grey
  footer;
- the master is rotated by 0.35° and rasterised at 200 dpi, then speckled with fixed-seed numpy noise.

I tuned the speckle to the pack scans. On a blank strip, the pack Form 4-C has a mean of 251.5 and 0.5% of
pixels below 200; mine has 254.6 and 0.4%.

**Metadata and file structure.** These follow the issued addenda:

- title and author "(anonymous)", subject and creator "(unspecified)", keywords empty;
- producer "ReportLab PDF Library - (opensource)", as in ADD-01/02;
- creation and modification date `D:20261109102501+00'00'`: the issue date, at the originals' time of day;
- header `%PDF-1.4` (ADD-01/02 are 1.4; the same-length header patch leaves the xref offsets unchanged);
- a fixed trailer `/ID` with two equal halves, as ReportLab writes it;
- page dictionaries with `/Rotate 0` and `/Trans <<>>`, and a catalog with `/PageMode /UseNone`.

## Subjects avoided

None of the blind-01, blind-02 or blind-03 subjects is touched:

- **blind-01:** the PDD; the 5.2 period; 6.4; 6.5; footnote 12; 8.6; 10.5 insertion and renumbering; 12.2;
  Table 2-4 TSS; Table 2-6; the Form 4-C sixth declaration; Form 4-A; and the Q topics LCC timing, 6.1
  control room, affiliate references, TN in the reliability run, site visit and page limit.
- **blind-02:** the time; Appendix 3; 6.8; 7.1/6.3; 10.3/12.5; the Form 4-F rows; VOL-II 3.5/4.4/8.4;
  Table 2-2; the 9.1 re-lettering and the Index of Forms; and ADD-01 Q3, the PoA legalisation, ADD-02 Q10,
  ADD-02 Q7 and the Financial Model USB.
- **blind-03:** the Working Day definition and the office closure; 8.8/8.1 O&M membership; the Form 4-C
  fourth declaration; Table 2-4 TP; VOL-V 29.3, 31.4 and 39.3; the Form 4-G reissue; ADD-02 Q9;
  construction water; the Environmental Permit; Schedule 11.

The PDD and its time are unchanged.

## Design

| Required element | Where | Mechanism |
|---|---|---|
| Definition used in several volumes | 2.1–2.2 | VOL-V 1.3 Estimated Project Cost becomes "as stated by the Bidder in Form 4-F, excluding financing costs, IDC and development fees". It applies wherever the term is used (VOL-IV Form 4-F row; VOL-V 18.1, 18.4; VOL-I 8.4(a)), but the uses are not listed |
| Change as a percentage of another value | 3.1 | VOL-I 8.4(a) TNW: SAR 800m → 25% of EPC (break-even EPC SAR 3.2bn) |
| Change as a formula | 4.1 | VOL-V 18.1 LD: SAR 180,000/day → 0.05% of EPC/day (break-even EPC SAR 360m). 18.4 is unchanged, so the cap is hit on day 200, against the 365-day termination right |
| Value change whose effect runs through a calculation | 5.1 | VOL-II 5.2 v_max 2.0 → 1.5 m/s. At 7,500 m³/h the bore must be ≥ 1.33 m, so DN1200 (VOL-II 5.3) fails at 1.84 m/s and DN1400 follows; Q18 extends it to the crossings |
| Amendment of an amendment with a stated effective date | 5.2 | ADD-01 5.1 (GRP) narrowed "with effect from 8 October 2026" (retroactive): ductile iron only at the 4 trenchless crossings |
| Weight change in the evaluation table that shifts a threshold | 6.1 | Table 1-1 reissued with new criterion G (20) and a total of 120. Note (1) re-states the threshold as 70%, which is 84 marks, not 70. Hidden Note (2) changes the weighting 65/35 → 70/30 |
| Split of one clause into two | 6.2 | VOL-I 11.3 → 11.3 (70% of total marks) and 11.3A (Envelope B *retained* until after the PBN, then returned). Content changes inside the split; no renumbering |
| Conditional amendment on an event | 7 | VOL-II 1.4 grid connection moves to the Project Company only if the Authority gives Portal notice by 10 WD before the PDD (Thu 12 Nov 2026); otherwise it lapses. If triggered, grid cost enters EPC, which feeds the LD and 8.4 chain |
| Image-only element (form with table cells, a unit and a note) | Appendix A, page 4 | New Form 4-H (beneficial ownership) in Arabic: three declarations, a 5-column owner table with "نسبة الملكية (٪)", field lines and a note |
| Arabic governs over a convenience translation, with a discrepancy | 8.2 + App. A vs App. B | Arabic "عشرة في المائة (١٠٪)" against English "twenty-five per cent (25%)". The Arabic (10%) governs. 25% is also the figure a model may "know" from general practice |
| Missing evidence | Note (4), Q17 | "Appendix C" (Energy Performance Statement format and the reference kWh/m³) is referenced twice; the addendum has Appendices A and B only |
| Cover planted errors (3 mechanisms) | cover | E1 direction reversal ("relaxes the velocity limit"). E2 half-true itemisation hiding a change inside a reissued item (the table "to add a criterion" also changes the weighting and the threshold in its Notes). E3 "all Bidders may submit … after the PDD" when 8.3 limits that to members incorporated outside the Kingdom |
| Decoy with no effect | Q15 | Restates VOL-I 8.7 and Form 4-D (unlimited; not conditional on prior demand) in imperative "shall" words; no change |
| Genuine ambiguity, no correct answer | 3.1 + 2.1 + Q19 | 8.4(a) depends on the EPC, which is only in Form 4-F (Envelope B). The 8.4 check is stage (i), before B is opened. Putting EPC in A risks 6.2 non-responsiveness. Q19 declines to answer. Escalate |
| Must-not-report list | key | 18 items, including the decoy, the conditional, the translation's 25%, the direction of the formula changes, renumbering, the Index of Forms and Appendix C content |

The three cover mechanisms differ from blind-02 (a direct contradiction; a misleading heading or shared
string) and from blind-03 (a derived-date closure; a plain omission). E1 names the right item but inverts the
direction, and the number falls while the requirement tightens. E2's claim is true; the second change is
inside the replaced Notes. E3 overstates who gets the post-PDD route, which is dangerous because it
over-promises relief.

## Traps and intended reasoning

- **E1 and S1.** "Maximum velocity" is a ceiling. Lowering it means a bigger pipe, so the cover is wrong.
  Tracing the effect needs the Table 2-6 peak flow, the continuity equation, the DN1200 in 5.3, the
  crossings in 5.4 (Q18) and the EPC.
- **E2 and S2/S3.** Diff the Notes. ADD-02 Note (2) gave 65/35 and the new Note (2) gives 70/30. The ADD-01
  minutes' "seventy / thirty" remark remains non-binding: the source is ADD-03 Note (2). The threshold is
  70% × 120 = 84.
- **E3 and 8.3/8.4.** Envelope A at 14:00 on Thu 26 Nov is the rule. Only a foreign-incorporated member's own
  Form 4-H may come through the Portal, by Thu 3 Dec 2026. Lateness otherwise is non-responsive.
- **Arabic image.** Only the image says 10%. The tool must read the image, keep the Arabic verbatim and flag
  that the translation does not govern. The second declaration (no beneficial-owner interest in any member
  of another bidding consortium) is stricter than VOL-I 8.2. The third requires a register issued 27 Oct to
  25 Nov 2026.
- **Section 7.** It is conditional and not triggered at issue. Register VOL-II 1.4 as unchanged with a flag;
  the trigger window closes Thu 12 Nov 2026.
- **Formula items.** Do not call 8.4(a) or the LD rate "relaxed", "tightened", "reduced" or "increased"
  without an EPC. Give the break-even points instead (SAR 3.2bn and SAR 360m). The 200-day cap point
  is EPC-independent.
- **5.2.** It is a chain record (VOL-II 5.3 ← ADD-01 5.1 ← ADD-03 5.2, effective 8 Oct 2026). GRP is still
  acceptable elsewhere on the main.
- **Missing evidence.** Appendix C does not exist in the PDF. No value or format may be invented.
- **Decoy.** Q15 changes nothing. Q16, Q18 and Q20 are confirming or neutral. Q17 points at the missing
  appendix. Q19 is a non-answer.

## Deliberate ambiguities

1. **A1 (no correct answer).** The 8.4(a) EPC dependency clashes with the envelope separation (6.2, 10.1,
   11.1, 11.3A) and Q19 refuses to resolve it. Expected: escalate with both horns; optionally recommend a
   further clarification before the Thu 12 Nov cut-off (VOL-I 3.3). No machine resolution.
2. **A2.** The forward count for 8.3: Thu 3 Dec, or Wed 2 Dec if the PDD is counted and the tool says so. The
   time of day is not stated.
3. **A3.** The boundary of the 30-day register window.
4. **A4.** Whether the Energy Performance Statement counts toward the 150-page limit.
5. **A5.** DN1400 is derived, not stated.
6. **A6.** The retroactive date in 5.2 has no practical bid-stage effect.

## Internal-consistency checks done

- **Quotations.** Every "old" quotation in the PDF and all 40 `state_before` texts in the key were matched
  by script against the extracted pack text, with page numbers. These cover:
  - VOL-I 2.4, 3.2(a), 3.3, 5.2, 6.2, 6.7, 8.2, 8.4, 8.7, 9.1, 9.7, 10.1, 11.1, 11.2 and 11.3;
  - VOL-II 1.4, 4.5, 5.2, 5.3, 5.4 and row 2-6.2;
  - VOL-IV Form 4-D, the Form 4-F row and the Index note;
  - VOL-V 1.3, 12.1 and 18.1–18.4;
  - ADD-01's date, 5.1 and Appendix B item 3;
  - ADD-02 3.1, Notes (1)–(3), 2.1 and 7.1.
- **Key against PDF.** Every `old`/`new` string in the key's provisions and every new Note appears in the
  extracted ADD-03 text, and the cover text in the key equals the PDF's.
- **Arabic.** The strings in the key equal the builder's source strings exactly. A `" ".join` of the manual
  line breaks equals each paragraph (asserted in the builder). The text layer contains no Arabic or
  presentation-form code points.
- **Dates.** All dates were computed in the builder and asserted:
  - issue Mon 9 Nov 2026, which is after ADD-02 (Thu 22 Oct) and before the trigger and cut-off (Thu 12 Nov)
    and the PDD (Thu 26 Nov);
  - Form 4-H Portal route Thu 3 Dec 2026;
  - register window from Tue 27 Oct 2026.
  No Saudi public holiday falls in the window.
- **Figures.** Computed by script: bores of 1.152 m and 1.330 m, DN1200 at 1.842 m/s, the LD cap at
  200 days, the threshold of 84/120.
- **Cross-references.** Every cited clause, table, form and section exists: VOL-I 3.2, 5.3, 6.2, 8.4, 8.7,
  9.1, 11.1, 11.2 and 11.3; VOL-II 1.4, 5.2, 5.4 and Table 2-6; VOL-IV Forms 4-D, 4-F and 4-G; VOL-V 1.3,
  18.1, 18.4 and Scheduled PCOD (12.1); ADD-01 5.1; ADD-02 Section 3. Appendix C is the only deliberate
  dangling reference.

## Verification

- Two builds gave identical bytes.
- PyMuPDF checks:
  - 5 pages;
  - Latin span fonts = {Helvetica, Helvetica-Bold, Times-Roman, Times-Bold};
  - furniture spans equal ADD-02 on every page;
  - the rules and the cover band equal ADD-02;
  - the only image is on page 4 (1654 × 2339, bbox 66.61, 68.36, 528.66, 721.77, the same as VOL-IV
    Form 4-C);
  - page 4 text is furniture only.

```
cd <this sealed directory>   && sha256sum -c --ignore-missing SHA256SUMS   # three sealed files
cd <repository root>         && sha256sum -c --ignore-missing <sealed>/SHA256SUMS   # the PDF
```
