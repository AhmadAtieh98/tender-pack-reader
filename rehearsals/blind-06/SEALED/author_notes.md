# Blind rehearsal 06: author notes (SEALED)

Inputs:
- `rehearsals/blind-06/input/ADD-03_Addendum_No_3.pdf`: 5 pages, "Issued 10 November 2026" (a Tuesday). It stands on
  the base pack as amended by ADD-01 and ADD-02 only.
- `rehearsals/blind-06/input/ADD-04_Addendum_No_4.pdf`: 2 pages, "Issued 16 November 2026" (a Monday). It stands on
  ADD-03 and is used for the consecutive-addenda check.

Answer key: `expected_findings.yaml` in this directory. The `addendum_4` section is ADD-04's own small key. The
builder is `build_addendum.py`, which builds both PDFs. The author is independent and worked cold. Model:
claude-opus-5-5 (Opus 5.5), as the system prompt states.

Build command: `.venv/bin/python build_addendum.py <ADD-03 out.pdf> <ADD-04 out.pdf> [--check sources/candidate_pack]`.
The builder will not run unless PyMuPDF is 1.28.2, numpy is 2.4.6, and FreeSerif.ttf and FreeSerifBold.ttf in
`/usr/share/fonts/truetype/freefont/` have the pinned SHA-256 values. The Arabic raster depends on those fonts.
Three separate builds produced identical bytes for both files.

## What I read

I read the allowed sources only:

- All six pack PDFs, in full, via PyMuPDF text with the rotated watermark lines removed:
  - Volume I, Volume II, Volume IV, Volume V, ADD-01 and ADD-02.
  - The Volume II Table 2-4 image and the Volume IV Form 4-C image, extracted at full resolution and read.
  - The raw content streams of ADD-02 page 1 and ADD-01 page 3, to check the furniture strings, the cover band and
    the table styling.
- The brief (`sources/brief/Lamar_PPP_AI_Partner_Round2_Brief.pdf`) and the three correspondence `.md` files in
  `sources/correspondence/`. From these I took:
  - the meanings of A1 to A5;
  - "a PDF in the same format as Addenda 1 and 2";
  - planning date = the latest addendum date;
  - an editable three-member consortium.
- The blind-01 to blind-05 input PDFs, read only to list their subjects.
- `rehearsals/blind-05/SEALED/build_addendum.py` and `author_notes.md`, as a technique and style example. The layout
  engine, the furniture function and the Arabic line shaper are adapted from that builder.

What I did not open:
- `sources/correspondence/` beyond its three `.md` files: the `.eml`, the Gmail PDF and the PNG. I also did not open
  `sources/manifest.json`.
- Any `expected_findings.yaml` of an earlier rehearsal.
- The tool's code (`tenderpack/`), tests, `curation/`, `config/`, `build/`, `out/`, `out-drill*/`, `docs/`,
  `worklog/`, `scripts/` and `staging/`.
- Any rehearsal's `work/`, `out-*`, `review*`, `candidate-curation/`, `proposals/`, `batches/`, `downstream/`,
  `COMPARISON.md`, `REGRESSION*.md` or `FROZEN*`.

What I wrote and ran:
- Inside the repository, the only files written are the two input PDFs. Their directory, `rehearsals/blind-06/input/`,
  had to be created.
- No git command was run. Nothing was staged or committed.

## Subjects avoided (from the blind-01 to blind-05 inputs)

- **blind-01:**
  - Proposal Due Date (PDD); 5.2 period and time; 6.4 amount; 6.5 copies; footnote 12; 8.6.
  - New 10.5 and the renumbering that followed; 12.2.
  - Table 2-4 TSS; Table 2-6 row 2-6.2; Form 4-C sixth declaration; Form 4-A PDD.
  - Questions on: the Local Content Certificate (LCC); control-room manning (VOL-II 6.1); affiliate references; total
    nitrogen (TN) during the reliability run; the site visit; the page limit.
- **blind-02:**
  - 6.1 time; Appendix 3; new 6.8; validity periods (7.1 and 6.3); 10.3 audit opinion and new 12.5.
  - Form 4-F audit rows; VOL-II 3.5, 4.4 and 8.4; Table 2-2 and its notes; 9.1 re-lettering; Index of Forms.
  - Questions on: foreign-branch Bid Bond; Power of Attorney (PoA) legalisation; Operation and Maintenance (O&M)
    guarantee; when the term starts; Financial Model USB; PDD extension.
- **blind-03:**
  - Working Day definition and office closure; 8.8 and 8.1 O&M membership; Form 4-C fourth declaration.
  - Table 2-4 TP; VOL-V 29.3, 31.4 and 39.3; Form 4-G reissue.
  - Questions on: the Form 4-C translation; construction water; the consent deadline; Form 4-C signatories.
- **blind-04:**
  - Estimated Project Cost; 8.4(a); 18.1 liquidated damages (LDs); VOL-II 5.2 velocity; ADD-01 5.1 glass-reinforced
    plastic (GRP) pipe at crossings.
  - Table 1-1 second revision; 11.3 and 11.3A; conditional VOL-II 1.4 (grid); Form 4-H.
  - Questions on: the Parent Company Guarantee (PCG) amount; grid cost; Appendix C; velocity at crossings; 8.4(a)
    evidence; register legalisation.
- **blind-05:**
  - Merger of 6.6 and 6.7; VOL-V 1.1 and new 1.1A Base Date; 29.2 indexation; VOL-II 3.1 membranes; VOL-II 3.4 odour
    via ESIA Figure 7-2; new VOL-II 5.6 and Arabic Table 5-1.
  - Questions on: VOL-II 6.4 data retention; Form 4-E "no deviations"; ISO 9001 for joint-venture members; dispersion
    modelling; Form 4-F year-1 prices; Indexed Proportion row; crane plan.

What ADD-03 touches:
- VOL-II 1.3, plus the new incorporated Table 1-3 (tie-in points, which no rehearsal has used).
- Free-standing provisions 2.3 to 2.7 and 3.2.
- VOL-II 7.2, VOL-II 8.1 to 8.3, VOL-V 31.1 and VOL-V 31.3.
- Through the answers: VOL-II 3.3 (confirming), VOL-V 12.3 and VOL-II 7.4.

What ADD-04 touches: ADD-03 2.5, VOL-II 8.2 and VOL-I Appendix 2.

Two subjects come near earlier rehearsals, and I judged both to be different:
- blind-01 response 18 asked whether TN applies during the reliability run, which is about a parameter. ADD-03 changes
  the run's throughput.
- blind-01 response 16 said only that 8.3 was "unchanged", in the context of control-room manning. ADD-03 replaces
  8.3's plant-manager wording.

The missing evidence (the "maximum transfer flow") is none of the excluded items: the Environmental Permit, Schedule 11,
an Appendix C or an ESIA figure.

## Style fidelity

- **Fonts.** The text layer uses only Helvetica, Helvetica-Bold, Times-Roman and Times-Bold, as Type1 fonts with
  WinAnsi encoding and not embedded, exactly as in ADD-01 and ADD-02. The text layer contains no Arabic code point.
- **Furniture.** The watermark, the header ("Addendum No. N" and "NUPA/ISTP/2026/014"), the header rule, the footer
  disclaimer, "Page N" and the footer rule all use the ADD-01/02 content-stream strings.
  - I checked this with PyMuPDF on all 5 + 2 pages. The furniture spans match the spans on every page of ADD-01 and
    ADD-02 in text, font, size, origin, direction and colour.
  - The header and footer rules match too.
- **Body.**
  - Cover band, project line, summary and precedence paragraph.
  - Headings in Helvetica-Bold 13.
  - Provisions in Times 9.6 on 13.4 leading, justified, with bold numbers and a 36.85 pt hang.
  - Bold substituted text, as in ADD-02 2.1.
  - Quoted clauses in the style of ADD-02 9.1.
  - The clarification grid uses the ADD-01/02 column positions.
  - The Appendix B table sits on the outer edges of ADD-02 Table 1-1, with the short centred rule and notes in
    Times 7.2.
  - Each appendix starts on a new page.
- **Image (ADD-03 page 4).** Drawn the way VOL-II page 3 draws Table 2-4:
  - Placed 9 pt below the introductory paragraph, at x = 56.69, over the full frame width 481.89 pt.
  - 1750 x 1550 px, RGB with equal channels, FlateDecode, with a ReportLab-style `FormXob.<md5>` name.
  - The Arabic is shaped by MuPDF/HarfBuzz in FreeSerif. The master is rotated 0.35 degrees, the paper is toned to
    252 and the speckle uses a fixed seed.
  - Top-strip statistics: pack Table 2-4 mean 251.13, 0.77% of pixels below 200, 1.19% below 250. Mine: mean 251.38,
    0.67% below 200, 0.84% below 250.
  - The image shows the issuer header (Arabic plus a small English line), reference and date, subject, tender number,
    title, intro, a 6-column table with units (mm, hours, Working Days), four notes, a signature, a stamp outline and
    the fictional-document line.
- **Metadata.** Matches the ADD-01/02 conventions:
  - title and author "(anonymous)"; subject and creator "(unspecified)";
  - producer "ReportLab PDF Library - (opensource)";
  - dates `D:20261110102501+00'00'` (ADD-03) and `D:20261116102501+00'00'` (ADD-04);
  - header %PDF-1.4; a fixed two-half /ID; /Rotate 0, /Trans and /PageMode /UseNone.

## Cut-off choice (deliberate)

The Volume I 5.2 clarification cut-off is 10 Working Days before Thursday 26 November, counted backwards: Thursday
12 November 2026.

- **ADD-03 is issued before the cut-off,** on Tuesday 10 November, two Working Days earlier. Bidders could still
  raise requests on ADD-03 on 10, 11 and 12 November. This is the opposite of blind-05, which issued after the cut-off.
  The choice has three effects:
  - the CMMS inconsistency (II1) can legitimately be answered later;
  - the reliability-run ambiguity (DA1) is something a Bidder should raise now;
  - the planning date becomes 10 November, with 12 Working Days left.
- **ADD-04 is issued after the cut-off,** on Monday 16 November. Its recital 1.3 says request 21 was received on
  Wednesday 11 November, before the cut-off. ADD-04 answers request 21 and reinstates 8.2 (resolving II1). It leaves
  DA1 and the missing value ME1 open.
- 16 November is also the day ADD-03's own application deadline fell. ADD-04 moves that deadline to Thursday
  19 November, and its 2.3 keeps letters already issued valid.

## Design

| Required element | Where | Mechanism |
|---|---|---|
| Change types an engine may lack (see `change_types` CT1-CT11) | 2-5, answers | **CT1:** band replacing a single minimum (7.2).<br>**CT2:** Addendum-only counting rule (3.2).<br>**CT3:** range replacement that silently drops the middle clause (8.1 to 8.3: 8.2 vanishes, "not renumbered").<br>**CT4:** old words spanning lettered items (b)-(c) across a line break, adding (d) and moving the "or" (31.1).<br>**CT5:** per-point Bidder election with a deeming fallback (2.3-2.6).<br>**CT6:** third-party Arabic image incorporated by reference that sets a rejection threshold (2.7).<br>**CT7:** amendments carried by answers (17: VOL-V 12.3; 19: VOL-II 7.4).<br>**CT8:** later provisions relying on new ones (5.2 on 31.1(d); answer 20 on 2.4).<br>**CT9:** defined terms that change meaning without any change to their text (PCOD via 7.2; Unavailability Event via 31.1).<br>**ADD-04:** amends an Addendum's own text (CT10) and reinstates a clause in amended form (CT11). |
| Indirect effects (incl. an earlier answer made wrong) | IE1-IE8 | 7.2 → VOL-V 1.5 PCOD → 12.1/18.1/18.3/29.x and VOL-I 12.1.<br>31.1(d) → 1.6, 24.3, 31.2, 31.4 → 39.3. 29.3 Ramp-Up relief does not reach (d). **ADD-01 response 6 becomes wrong.**<br>8.2 deletion vs answer 19.<br>CV appendix → page-limit exclusion (ADD-01 response 2 still right).<br>Answer 19 + new 8.1 → spares recorded before the run.<br>Election → letter → Arabic threshold → deemed method (a) → missing value.<br>Answer 17 ↔ DA1.<br>4.3 stream check (flag only). |
| Misleading cover (3 new mechanisms) | cover | **E1:** phantom provision ("no deduction during the Ramp-Up Period"; nothing amends 29.3).<br>**E2:** wrong temporal anchor ("within eight (8) Working Days of the date of this Addendum" vs "before the Proposal Due Date": Sun 22 Nov vs Mon 16 Nov).<br>**E3:** actor substitution ("the Authority's acceptance" vs a Network Operator letter).<br>None is a direct contradiction, an omission, a derived-date closure, a direction reversal, a half-true itemisation, an over-generalisation, a wrong clause number or a scope word. |
| Missing evidence | 2.4, answer 20 | **ME1:** "maximum transfer flow stated ... in Table 1-3". The table (Arabic and English) has no such column or note; only reading the image confirms the gap.<br>**ME2:** contents and channel of a "complete application".<br>**ME3:** the asset-register format (a base-pack gap, confirmed by answer 19). |
| Image-only element | ADD-03 p.4 | Table 1-3, Arabic letter extract from the Network Operator: 2 rows, 6 columns with units, 4 notes, signature and stamp. |
| Arabic governs; discrepancies | 2.2, App. A vs B | **AR1:** TP-2 maximum shutdown ٤ (4) h in Arabic, 6 h in English (the English window 01:00-05:00 is itself 4 h). This sets the 2.7 rejection threshold.<br>**AR2:** Arabic note 1 also bars shutdowns during the Eid al-Fitr and Eid al-Adha holidays; the English mentions only Ramadan. |
| Decoy / confirming / changing / human judgment | answers 15-20 | 15 decoy (ownership of the Network Operator).<br>16 confirming in imperative words (ozonation, VOL-II 3.3 restated).<br>17 changing (VOL-V 12.3 carve-out).<br>18 human judgment (is low network flow a "failure of a utility" Relief Event? time-only relief; a Form 4-E choice).<br>19 changing (asset register before the run) and internally inconsistent (cites deleted 8.2).<br>20 confirming of 2.4, pointing to the missing value. |
| Genuine ambiguity, no correct answer | DA1 | "continuous reliability run of thirty (30) days" (7.2), "shall not count" (3.2) and "7.3 is unchanged" (restart only on a Table 2-4 failure). Pause, restart or extend; and whether a Table 2-4 failure on an excluded day restarts the run. Escalate. Not resolved by ADD-04. |
| Must-not-report | key | 23 items for ADD-03 and 7 for ADD-04. |
| ADD-04 (stacked) | ADD-04 | Amends ADD-03 2.5: 8 → 5 WD before the PDD (Thu 19 Nov) and 5 → 3 WD response (Tue 24 Nov). Two substitutions in one sentence share "five (5) Working Days".<br>Reverses part of ADD-03 4.1 by reinstating 8.2 in amended form ("before the start of the reliability run").<br>Amends base VOL-I Appendix 2 (120 → 80 characters including the extension), which ADD-03 did not touch.<br>Answer 21 resolves II1.<br>Trap A4-T1: the "for convenience" consolidated Appendix A reproduces the stale original 8.2 ("before PCOD"). The operative 3.1 governs. |

## Traps and intended reasoning

- **8.1 to 8.3.** The range covers 8.2. Only 8.1 and 8.3 are restated, and 4.2 says "not renumbered", so 8.2 is
  deleted. Answer 19 then cites "Volume II Clause 8.2". Flag the clash and escalate; do not reinstate silently.
  ADD-04 3.1 settles it.
- **31.1.** Match the old words with whitespace normalised; they span "(b) the treated / effluent". The letters (a) to
  (c) do not move, so 31.3's cross-references still hold. 5.2 gives (d) no cure period.
  - The cover's Ramp-Up claim (E1) is false. Read 29.3: it relieves only rolling-average Table 2-4 parameters.
  - ADD-01 response 6 ("does not depend on volume delivered") becomes wrong.
- **Tie-ins.**
  - Values come from the image; TP-2 is 4 hours.
  - A missing letter is not a disqualifier (2.6 deems method (a)). The only new A3 item is 2.7, and it applies only
    when there is an interruption.
  - The drop-dead date for the letter is Monday 16 November and the issuer is the Network Operator (E2, E3).
  - The over-pumping design flow is unknown (ME1). Do not borrow Table 2-6's 7,500 or 1,800 m3/h.
  - VOL-II 4.1's "without reliance on pumped bypass" covers the permanent hydraulic profile, not temporary tie-in
    works. Do not report a conflict.
- **7.2.** The band is 102,000 to 132,000 m3/day. Before ADD-03 the requirement was at least 108,000 m3/day. PCOD rows
  move by meaning, not by text. DA1 has no correct answer.
- **Answers.** 15 has no effect. 16 changes nothing. 17 and 19 change requirements. 18 is for a person. 20 restates
  2.4 and points to a gap.
- **ADD-04.**
  - Match the full phrases; a bare "five (5) Working Days" occurs twice after 2.1.
  - 8.2 comes back in amended form; Appendix A is stale.
  - Appendix 2's consequence stays "corrected ... at the Bidder's risk" (not an A3 item).
  - The issue date after the cut-off is valid.

## Internal-consistency checks done

- **Quotations.** The builder's `--check` verifies 62 quotations verbatim against the pack, page by page. They are:
  - every "old" text in ADD-03 (1.3 anchor, 7.2, 31.1 span, 31.3);
  - every base-pack "old" text in ADD-04 (8.2, Appendix 2);
  - the state_before texts.

  Each "old" string in a volume is asserted to occur exactly once. ADD-04's quotations of ADD-03 2.5 are verified
  against the built ADD-03 text layer, each occurring once.
- **Key against the sources.** A separate script:
  - re-verified all 37 `state_before` entries against the pack, on the stated page;
  - confirmed every provision `old` is in the pack;
  - confirmed every provision `new`/`text`, every question and response, the cover text and each planted error's
    `cover_says` appear verbatim in the ADD-03 text layer;
  - confirmed the ADD-04 provisions, cover and answer appear in the ADD-04 text layer;
  - confirmed both the stale and the operative 8.2 texts are present in ADD-04;
  - confirmed the 31 Arabic strings in the key equal the builder's source dictionary, which is what the image is
    rendered from;
  - found no Arabic code point in either text layer.
- **Arabic layout.** Manual line breaks join back to the full strings (asserted). Every Arabic cell is asserted to fit
  its column. The rendered table was inspected at 260 dpi: bidi of "MH-41", "٢٣:٠٠" and the Arabic-Indic digits is
  correct, and the diacritics (يُسمح, إجازتَي, بإيقافٍ واحدٍ, تُقدَّم, مدّة) render.
- **Dates.** All are computed and asserted in the builder:
  - Issue dates: ADD-03 Tue 10 Nov and ADD-04 Mon 16 Nov, both after ADD-02 (Thu 22 Oct) and the letter (Thu 5 Nov),
    and before the PDD (Thu 26 Nov).
  - Cut-off Thu 12 Nov, between the two issue dates. Request 21 received Wed 11 Nov.
  - Application deadline (ADD-03) Mon 16 Nov, with the latest response Mon 23 Nov. The cover's wrong anchor gives
    Sun 22 Nov (or Thu 19 Nov if the issue day is counted).
  - Application deadline (ADD-04) Thu 19 Nov, with the latest response Tue 24 Nov.
  - 12 Working Days from ADD-03 to the PDD and 8 from ADD-04.
  - There is no Saudi public holiday from October to December 2026. Forward counts mirror Clause 2.4 (start day not
    counted), and the key says this is an assumption.
- **Cross-references.** Every cited clause, table, form and section exists:
  - VOL-I 3.2, 5.2, 5.3 and Appendix 2;
  - VOL-II 1.3, 3.3, 7.2, 7.3, 7.4, 8.1-8.5;
  - VOL-V 12.3, 31.1, 31.3 and Clause 34;
  - Form 4-A;
  - ADD-03 Sections 2.2, 2.4 and 2.5 and Appendices A-B;
  - ADD-04 Sections 2-3 and Appendix A.

  "Table 1-3" is new by design, and the "maximum transfer flow" is deliberately missing.

## Verification

- Two or more builds gave identical bytes. The PDF hashes are in `SHA256SUMS`.
- PyMuPDF on ADD-03:
  - 5 pages; fonts {Helvetica, Helvetica-Bold, Times-Roman, Times-Bold};
  - one image, on page 4 only (1750 x 1550, bbox 56.69, 127.16, 538.58, 553.98);
  - page 3 holds the last two clarification rows.
- PyMuPDF on ADD-04: 2 pages and no image.

```
cd <this sealed directory>   && sha256sum -c --ignore-missing SHA256SUMS   # three sealed files
cd <repository root>         && sha256sum -c --ignore-missing <sealed>/SHA256SUMS   # the two PDFs
```
