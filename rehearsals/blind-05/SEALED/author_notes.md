# Blind rehearsal 05: author notes (SEALED)

Input: `rehearsals/blind-05/input/ADD-03_Addendum_No_3.pdf` (5 pages, "Issued 15 November 2026", a Sunday).
Answer key: `expected_findings.yaml` in this directory. Builder: `build_addendum.py`. Author: independent, working cold.
PDF SHA-256: `9c5e22d59a80d48f82f07cbb0cfb7649f14a8618fb8fc4503a576f4a0293eae3`. Model: claude-opus-5-5 (Opus 5.5), per the system prompt.

The builder is deterministic. Run `python build_addendum.py out.pdf [--check <candidate_pack_dir>]` with the
repository's virtualenv (`.venv/bin/python`). Two builds gave identical bytes. It refuses to run unless
PyMuPDF is 1.28.2, numpy is 2.4.6 and `/usr/share/fonts/truetype/freefont/FreeSerif.ttf` and
`FreeSerifBold.ttf` have the pinned SHA-256 (the Arabic raster depends on them). `--check` re-verifies 47
quotations against the pack, page by page, and prints the derived dates and figures.

## What I read

Allowed sources only:

- the six pack PDFs (VOL-I, VOL-II, VOL-IV, VOL-V, ADD-01, ADD-02), read in full; the VOL-II Table 2-4 image
  and the VOL-IV Form 4-C image rendered and read; the raw content streams of ADD-02 page 1 and VOL-II page 3
  inspected for furniture, superscript and image-placement conventions;
- the brief (`sources/brief/Lamar_PPP_AI_Partner_Round2_Brief.pdf`) and the three correspondence `.md` files
  in `sources/correspondence/` (A1-A5 meanings; "a PDF in the same format as Addenda 1 and 2"; planning date =
  latest addendum date; three-member consortium as an editable setting). I did not open the `.eml`, the Gmail
  PDF, the PNG or `sources/manifest.json`;
- the blind-01, blind-02, blind-03 and blind-04 input PDFs, only to list their subjects;
- `rehearsals/blind-04/SEALED/build_addendum.py` and `author_notes.md`, as a technique and style example. The
  layout engine and furniture strings are adapted from that builder. I did not open blind-04's
  `expected_findings.yaml` or any other sealed key.

I did not open the tool's code (`tenderpack/`), tests, `curation/`, `config/`, `build/`, `out/`, `docs/`,
`worklog/`, `scripts/`, `staging/`, or any rehearsal's `work/`, `out-*`, `review*`, `candidate-curation/`,
`proposals/` or `COMPARISON.md`. The only file written inside the repository is the input PDF (its directory
`rehearsals/blind-05/input/` had to be created). No git command was run. Nothing was staged or committed.

## Subjects avoided

- **blind-01:** PDD; 5.2 period/time; 6.4 amount; 6.5 copies; footnote 12; 8.6; new 10.5 and renumbering; 12.2;
  Table 2-4 TSS; Table 2-6 2-6.2; Form 4-C sixth declaration; Form 4-A PDD; Qs on LCC, 6.1 control room,
  affiliate references, TN in the reliability run, site visit, page limit.
- **blind-02:** 6.1 time; Appendix 3; new 6.8 registration; 7.1/6.3 validity; 10.3 audit opinion / new 12.5;
  Form 4-F model-audit rows; VOL-II 3.5 noise, 4.4, 8.4; Table 2-2 and its notes (2.3 expansion, simulation
  report); 9.1 re-lettering; Index of Forms; Qs on foreign-bank Bid Bond, PoA legalisation, O&M guarantee,
  term commencement, Financial Model USB, PDD extension.
- **blind-03:** Working Day definition and office closure; 8.8/8.1 O&M membership; Form 4-C fourth declaration;
  Table 2-4 TP; VOL-V 29.3, 31.4, 39.3; Form 4-G reissue; Qs on the Form 4-C translation, construction water,
  consent deadline, Form 4-C signatories.
- **blind-04:** Estimated Project Cost; 8.4(a); 18.1/18.4 LDs; VOL-II 5.2 velocity and ADD-01 5.1 GRP / 5.4
  crossings; Table 1-1 second revision and Notes; 11.3/11.3A; conditional VOL-II 1.4; Form 4-H; Qs on 8.7/Form
  4-D, grid cost, Appendix C, velocity at crossings, 8.4(a) in Envelope A, register legalisation.

ADD-03 here touches: VOL-I 6.6/6.7 (merger), VOL-V 1.1 and new 1.1A, VOL-V 29.2, VOL-II 3.1 (and through it
3.2), VOL-II 3.4, new VOL-II 5.6 with Table 5-1, a new Portal notice (7.3), and in the answers VOL-II 6.4
(decoy), VOL-I 9.6 (confirming), VOL-I 8.3, Form 4-F's indexation row and VOL-I 9.7. Noise (3.5) appears only
as the cover's wrong clause number, and is unchanged.

## Style fidelity

- **Fonts:** text layer uses only Helvetica, Helvetica-Bold, Times-Roman, Times-Bold (Type1, WinAnsi, not
  embedded) as ADD-01/02. No Arabic code point in the text layer; Arabic exists only in the image, as in the
  pack. Superscript "m3" drawn as ADD-02 does (0.8 x size, rise 0.5 x size).
- **Furniture:** watermark, header ("Addendum No. 3" / "NUPA/ISTP/2026/014") with rule, footer disclaimer,
  "Page N" and rule are the ADD-01/02 content-stream strings. Verified with PyMuPDF: on all 5 pages the
  furniture spans (text, font, size, origin, direction, colour) equal ADD-02 page 1, and the two rules match.
- **Body:** cover band, project line, summary and precedence paragraph; Helvetica-Bold 13 headings; Times 9.6 on
  13.4 justified provisions with bold numbers and a 36.85 pt hang; quoted clauses in ADD-02 9.1 style; the
  clarification grid on the ADD-01/02 columns; Appendix B table on the ADD-02 Table 1-1 outer edges, with the
  short centred rule and Times 7.2 notes. Each appendix starts on a new page, as in ADD-01.
- **Image (page 4):** drawn exactly as VOL-II page 3 draws Table 2-4: `q 1 0 0 1 56.69291 y cm q 481.8898 0 0 h
  0 0 cm /FormXob.<md5> Do Q Q`, 9 pt below the introductory paragraph, after the furniture; 1750 px across
  (the Table 2-4 raster width), 1750 x 1500, RGB with equal channels, FlateDecode, ReportLab-style XObject
  name. Arabic shaped by MuPDF/HarfBuzz in FreeSerif, master rotated 0.3 degrees, paper toned to 252 as in the
  pack, fixed-seed speckle. Top-strip statistics: pack Table 2-4 mean 251.38, 0.64% < 200, 0.87% < 250;
  mine 251.35, 0.69%, 0.90%.
- **Metadata:** title/author "(anonymous)", subject/creator "(unspecified)", producer "ReportLab PDF Library -
  (opensource)", dates `D:20261115102501+00'00'`, header %PDF-1.4, fixed two-half /ID, /Rotate 0, /Trans,
  /PageMode /UseNone.

## Design

| Required element | Where | Mechanism |
|---|---|---|
| Merger of two clauses | 2.1-2.2 | VOL-I 6.6 + 6.7 become one 6.6. Hidden change: modification only until 2 WD before the PDD (Tue 24 Nov); late modification rejected unopened. 6.7 left as a gap, no renumbering |
| Definition change with the term used in forms | 3.1-3.2 | VOL-V 1.1 AP "expressed at Base Date prices"; new 1.1A Base Date = PDD - 28 days (Thu 29 Oct). Form 4-F uses the term three times and is not amended |
| Tolerance band + Bidder election + staged phases | 3.3 | 29.2: 60/40 replaced by a Bidder-elected Indexed Proportion 50%-70% (years 1-10) and a fixed 75% from year 11; indexation from the Base Date |
| Change that triggers a conditional clause / overtakes an earlier answer | 4.1 | Membrane filtration (tertiary or MBR, <= 0.1 um) made mandatory: VOL-II 3.2 (7-year warranted membrane life) now always applies; ADD-01 response 1 partly wrong; 4.3 four streams apply to the membrane stage |
| Change by cross-reference to another document's figure | 5.1 | VOL-II 3.4 odour: 5 OU/m3 at the site boundary replaced by the value for the nearest sensitive receptor in ESIA Figure 7-2 |
| Missing evidence | 5.1, Q18 | ESIA Figure 7-2 (value and receptor) is not in the pack; Q18 refuses to reproduce it. Secondary: zone line and ground levels (Volume III), Schedule 9 |
| Image-only element with cells, units and notes | App. A, p.4 | Table 5-1 (Arabic letter extract): zones, 25 m / 40 m with the datum in the unit header, lighting, 3 notes, signature/stamp |
| Arabic governs over a convenience translation, with discrepancies | 7.2, App. A vs B | AR1 datum: natural ground before grading (Arabic) vs finished ground after grading (English). AR2 scope: permanent and temporary incl. cranes and construction equipment (Arabic) vs permanent structures incl. stacks (English) |
| Election-dependent bid-stage action with a derived date | 7.3 | Portal notice by Mon 23 Nov 2026 if any structure, plant or equipment (cranes included) exceeds 30 m; no consequence stated |
| Cover planted errors (3 new mechanisms) | cover | E1 false "without change of substance" label; E2 wrong clause number (3.5 noise for 3.4 odour); E3 the cover repeats the non-governing translation's scope ("permanent structures") |
| Decoy | Q15 | Data retention 10 vs 7 years: "not required" - no effect |
| Confirming in imperative words | Q16 | Restates VOL-I 9.6 ("shall not include", "shall be listed") - no change |
| Genuinely changing answers | Q17, Q20, Q21 | 8.3 per JV member; Form 4-F indexation row completed with the elected % (never in Envelope A); crane and lifting plan added to 9.7 |
| Genuine ambiguity, no correct answer | 3.1/3.3 vs Q19 | AP at Base Date prices indexed from the Base Date (body) vs AP in year-1 prices with indexation from the first anniversary of PCOD (Q19). Same Addendum, issued after the 5.2 cut-off; qualifying the price is non-responsive (10.5, Form 4-F confirmation, 6.2 via Form 4-E), and it cannot be fixed later (11.5). Escalate |
| Must-not-report list | key | 19 items |

Issue date: Sunday 15 November 2026, the first Working Day after the clarification cut-off (Thu 12 Nov), so
no ambiguity in ADD-03 can be clarified (recital 1.3 says late requests went unanswered). Nine Working Days
remain before the PDD; the planning date becomes 15 Nov.

The three cover mechanisms differ from blind-02 (direct contradiction; omission under a shared string),
blind-03 (derived-date closure; plain omission) and blind-04 (direction reversal; half-true itemisation;
"all Bidders" over-generalisation). E1 is a false editorial label, E2 a wrong provision number, E3 a summary
that inherits the convenience translation's error.

## Traps and intended reasoning

- **E1 / merger.** Diff the quoted 6.6 against SB01 + SB02. Withdrawal unchanged; modification earlier; late
  modification rejected. Re-point any 6.7 rows; no renumbering.
- **E2.** The deleted words "not more than 5 OU/m3 at the site boundary" exist only in 3.4. Noise stays.
- **E3 / Arabic.** Only the image says natural ground and temporary works, cranes and construction equipment.
  Q21 (lifting plan against Table 5-1) and 7.3 ("structure, plant or equipment") corroborate. English Note (3)
  mentions cranes although English Note (1) leaves them out: a clue for careful readers.
- **AP / indexation.** Register the band, the election, both stages and the Base Date; never a single
  percentage. 75% from year 11 is outside the 50%-70% band on purpose. Out-of-band or stated in Envelope A:
  non-responsive (10.5 / 6.2), derived.
- **D1.** Report both horns and the constraints; no canon (specific over general, body over Q&A) may decide it.
- **Membranes.** 3.2 flips from conditional to applicable; ADD-01 response 1 becomes partly wrong; optional
  lifecycle chain (3 replacements in 25 years at a 7-year life; for 5 years' residual life at expiry the last set
  goes in at year 23 or later, if membranes are "major assets").
- **Odour.** The value is gone and unknown. Do not keep 5 OU/m3 or supply a typical value.
- **7.3.** Conditional on the Bidder's design and crane plan; not a disqualifier; Mon 23 Nov 2026.
- **Q15-Q21.** Q15 decoy; Q16 confirming; Q17, Q20, Q21 changing; Q18 missing-evidence pointer; Q19 the
  conflicting answer.

## Internal-consistency checks done

- **Quotations.** 47 "old" quotations in the builder verified verbatim in the pack with page numbers
  (`--check`); all 40 `state_before` texts in the key verified verbatim on the stated page; every
  provision `old` verified in the pack.
- **Key against PDF.** Every provision `new`, every response, the cover text and each planted-error claim
  appear verbatim (whitespace-normalised) in the ADD-03 text layer. The translation strings are present; the
  Arabic-only facts ("natural ground", "temporary", the letter number) are absent from the text layer.
- **Arabic.** The 24 strings in the key equal the builder's source dictionary exactly; manual line breaks join
  back to the full strings (asserted in the builder); every Arabic cell is asserted to fit its column.
- **Dates.** Computed in the builder and asserted: issue Sun 15 Nov 2026 (after ADD-02 Thu 22 Oct and the Table
  5-1 letter Tue 10 Nov; before the PDD Thu 26 Nov); cut-off Thu 12 Nov (before issue); Base Date Thu 29 Oct;
  modification Tue 24 Nov; 7.3 notice Mon 23 Nov; 9 WD from issue to the PDD. No Saudi public holiday in the
  window. The key's derived dates are checked against the builder's.
- **Cross-references.** Every cited clause, table, form and section exists: VOL-I 3.2, 5.2, 5.3, 6.1, 6.2, 6.6,
  6.7, 8.3, 9.6, 9.7, 10.3; VOL-II 3.1, 3.4, 5.5, 6.4, 9.1, Section 3; VOL-V 1.1, 29.2; Form 4-A, 4-E, 4-F;
  ADD-03 Sections 3-7 and Appendices A-B. ESIA Figure 7-2 and Schedule 9 are deliberate external references.

## Verification

- Two builds gave identical bytes.
- PyMuPDF: 5 pages; fonts = {Helvetica, Helvetica-Bold, Times-Roman, Times-Bold}; furniture equal to ADD-02 on
  every page; one image, on page 4 only (1750 x 1500, bbox 56.69, 127.16, 538.58, 540.21); page 4 text is the
  heading, one paragraph, "End of reproduction." and furniture.

```
cd <this sealed directory>   && sha256sum -c --ignore-missing SHA256SUMS   # three sealed files
cd <repository root>         && sha256sum -c --ignore-missing <sealed>/SHA256SUMS   # the PDF
```
