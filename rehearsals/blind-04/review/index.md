# Review packet: ADD-03, AI workflow run ADD-03-run-host-blind04-20261004T152505Z

> **CANDIDATE: proposed by the AI workflow; not reviewed; nothing accepted.** Statuses are the controller's; a person decides every item. The real `curation/`, `config/` and `out/` were only read: everything below lives in this run's folder.

- PDF: `/home/user/tender-pack-reader/rehearsals/blind-04/input/ADD-03_Addendum_No_3.pdf` (sha256 99728136b5653acd…, 5 pages); preceding state: pack `/home/user/tender-pack-reader/config/pack.yaml` (NUPA-ISTP-2026-014), previous evidence build `/home/user/tender-pack-reader/build`
- route **host**; model requested `claude-code headless (opus)`, reported `None`; host sessions report: claude-opus-5-5
- status **partial**: 24 provision(s) unresolved in the candidate (listed first in the review packet)
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed

## What is candidate and what is real

- **Candidate** (proposed by this run, nothing accepted): `../candidate/` — a copy of the curation and configuration with ADD-03 added, its evidence build, its op file, rows, issues, templates and outputs.
- **Last validated state**: `../candidate/out-before/` (the pre-addendum outputs built from the copied curation and the previous evidence build; done)
- **Real** (untouched): `curation/`, `config/`, `out/`; the owner's approvals and readings were copied unchanged and used read-only.

- real inputs changed since the run started: none

## Candidate outputs

Exit 0 (WORKING DRAFT (not releasable)); every file carries the banner (`../candidate/out/CANDIDATE.md`); A1 has a candidate status column {'proposed (existing row; not changed by this run; not reviewed)': 175, 'UNRESOLVED': 30}.

| Output | Candidate | Before (ADD-03 not applied) |
|---|---|---|
| A1 register | [../candidate/out/a1/a1.xlsx](../candidate/out/a1/a1.xlsx) | [../candidate/out-before/a1/a1.xlsx](../candidate/out-before/a1/a1.xlsx) |
| A2 changes | [../candidate/out/a2/a2.md](../candidate/out/a2/a2.md) | [../candidate/out-before/a2/a2.md](../candidate/out-before/a2/a2.md) |
| A3 consequences | [../candidate/out/a3/a3.pdf](../candidate/out/a3/a3.pdf) | [../candidate/out-before/a3/a3.pdf](../candidate/out-before/a3/a3.pdf) |
| A4 clarification register | [../candidate/out/a4/clarification_register.md](../candidate/out/a4/clarification_register.md) | [../candidate/out-before/a4/clarification_register.md](../candidate/out-before/a4/clarification_register.md) |
| A5 programme | [../candidate/out/a5/README.md](../candidate/out/a5/README.md) | [../candidate/out-before/a5/README.md](../candidate/out-before/a5/README.md) |
| A5 Gantt | [../candidate/out/a5/gantt.html](../candidate/out/a5/gantt.html) | [../candidate/out-before/a5/gantt.html](../candidate/out-before/a5/gantt.html) |
| A5 marshalling | [../candidate/out/a5/marshalling.csv](../candidate/out/a5/marshalling.csv) | [../candidate/out-before/a5/marshalling.csv](../candidate/out-before/a5/marshalling.csv) |
| Checks | [../candidate/out/checks.json](../candidate/out/checks.json) | [../candidate/out-before/checks.json](../candidate/out-before/checks.json) |

- before → after: {"a1": {"rows_before": 205, "rows_after": 205, "new": 0, "gone": 0}, "a3": {"before": 17, "after": 17, "enters": 0, "leaves": 0}, "a5": {"activities_before": 43, "activities_after": 43, "new": 0, "gone": 0}}

- ADD-03 is **PARTIAL** in the candidate (provisions unresolved): A3 and the A5 programme show the validated state (ADD-02); ADD-03 as proposed is in A1's `Status after ADD-03` column, in A2, in `a5/working/ADD-03.json` and in the diff below.

## Timings (wall clock per step)

| Step | Seconds | Status |
|---|---|---|
| ingest | 19.4 | done |
| readings | 230.7 | done |
| analysis | 2338.7 | done |
| validation | 3.9 | done |
| downstream | 13.7 | done |
| downstream_validation | 0.3 | done |
| promotion | 2.7 | done |
| pin | 1.8 | done |
| check_register | 4.7 | done |
| outputs | 114.0 | done |
| diff | 2.6 | done |
| review | 0.0 | running |
| **total** | **2732.5** (45.5 min) | target 30 min from the PDF to candidate outputs and this packet, human review excluded |

## Readings of the addendum's image regions (AI-proposed, PENDING HUMAN REVIEW)

Ingest first refused the candidate because these image regions had no reading (C05): ADD-03-p4-r1. Each reading below was proposed by the route of this run, checked by readings.check_reading and written into the candidate's readings; it is an interpretation of an image, never approved, and every unit made from it carries `reading.status: pending`.

- **ADD-03-p4-r1** — done; controller status **interpretation_pending**; unit `ADD-03:p4-image`; file `../candidate/curation/readings/ADD-03-p4-r1.yaml`
  - the reading beside its crops (the build's review packet): [../candidate/build/review/ADD-03-p4-r1/packet.html](../candidate/build/review/ADD-03-p4-r1/packet.html)
  - form reading, languages ['ar', 'en']; prepared by: AI-assisted: headless host session ADD-03-hostsession-20261004T152526Z-9f15 (claude-code headless (opus); the CLI reported claude-opus-5-5), in AI workflow run ADD-03-run-host-blind04-20261004T152505Z (reading-ADD-03-p4-r1), 2026-10-04T15:28:59Z; proposed for a person's review, not approved
  - uncertainty: Diacritics (tanween on أولاً, ثانياً, ثالثاً, عرضاً, يوماً, كاملاً; shadda with tanween on أيٌّ; hamza forms) were read on the enlarged crops; review the native crops, not a scaled view.
  - uncertainty: Bands 22, 23, 24, 27 and 28 were not split by the band measurement although each holds an English label on the left and an Arabic label on the right; both labels are recorded against the full band.
  - uncertainty: The beneficial-owner table (bands 14-21) is an empty fill-in table of 5 columns and 4 numbered rows; no vertical rules were measured, so it is read as blocks (header band 15, row ٤ band 19).
  - uncertainty: Blank fill-in lines under each field label are rule bands (structure), not text.

## First: unresolved provisions and escalations

24 of 70 provisions are not answered by a promoted item (each is `unresolved` in the candidate op file with the reason); 3 escalation(s).

- **ESCALATED ADD-03/5.2** (ADD-03:5.2): The provision amends an earlier addendum's amending text (ADD-01:5.1) 'With effect from 8 October 2026'. A replace_text on ADD-01:5.1 simulates as structurally valid, but the engine reports the same words also in VOL-II:5.3 (where ADD-01:5.1 placed them) and that op changes only ADD-01:5.1, leaving…
  - unsupported: A change to an earlier addendum's amending words that must cascade to the clause it amended (VOL-II:5.3), with a deferred effective date (8 October 2026). A person must decide the target (ADD-01:5.1, VOL-II:5.3 or both) and how the effective date is recorded. Candidate op for review: replace_text, …
  - evidence: ADD-03:5.2 p1: “With effect from 8 October 2026, Section 5.1 of Addendum No. 1 is amended by deleting ‘for the buried sections of the transmission main’ and substituting ‘for …”; ADD-01:5.1 p1: “Glass reinforced plastic pipe of an equivalent pressure class is acceptable for the buried sections of the transmission main, subject to the whole-life cost co…”; VOL-II:5.3 p4: “Glass reinforced plastic pipe of an equivalent pressure class is acceptable for the buried sections of the transmission main, subject to the whole-life cost co…”; VOL-II:5.4 p4: “Three (3) road crossings and one (1) wadi crossing shall be executed by trenchless methods.”
  - affected scope: units ADD-01:5.1, VOL-II:5.4; rows VOL-II-5.4-01, VOL-II-5.4-02; activities technical-proposal; clarifications none
- **ESCALATED ADD-03/6.1** (ADD-03:6.1): The provision replaces Table 1-1 (revised) and its Notes issued by ADD-02 Section 3. The natural op (replace_unit ADD-02:T1-1-rev with replacement ADD-03:T1-1) fails C22 in simulation: 'the provision cites no clause, table, form or section that exists in the pack'. The provision refers to the table…
  - unsupported: Replacing an addendum-issued table and its separate Notes units when the citation ('Section 3 of Addendum No. 2') is not resolvable by the engine (C22). A person must confirm the target ADD-02:T1-1-rev (+ notes) and the replacement ADD-03:T1-1 (+ ADD-03:S6/para1).
  - evidence: ADD-03:6.1 p2: “Table 1-1 (revised) and the Notes to it, issued by Section 3 of Addendum No. 2, are deleted and replaced by the table and Notes below, which add criterion G (e…”; ADD-02:T1-1-rev p1: “Table 1-1 (revised) — Technical evaluation criteria — Ref | Criterion | Marks”; ADD-02:T1-1-rev/note(1) p1: “The technical score threshold in Volume I Clause 11.3 is unchanged at seventy (70) marks.”
  - affected scope: units none; rows none; activities none; clarifications none
- **ESCALATED ADD-03/7.2** (ADD-03:7.2): ADD-03:7.2 prints a deletion in VOL-II:1.4 (', together with a grid connection point at the site boundary') and moves the grid connection, and its cost, to the Project Company, but only 'Where this Section 7 has effect', that is, only if the Authority gives the notice in ADD-03:7.1 by 12 November 2…
  - unsupported: A conditional amendment: the op types have no condition or trigger, so replace_text (deleting ', together with a grid connection point at the site boundary') cannot be made to depend on a future Authority notice. Limbs (b) and (c) also add a scope and cost allocation (grid connection procured by th…
  - evidence: ADD-03:7.2 p2: “Where this Section 7 has effect: (a) in Volume II Clause 1.4, the words ‘together with a grid connection point at the site boundary’, and the comma before them…”; ADD-03:7.2 p2: “(c) the cost of the grid connection works forms part of the Estimated Project Cost.”; VOL-II:1.4 p2: “, together with a grid connection point at the site boundary”
  - affected scope: units VOL-II:1.4; rows VOL-II-1.4-01; activities technical-proposal; clarifications none
- **UNRESOLVED ADD-03:cover/para3** (paragraph, p1): not promotable: ADD-03/cover/para3 conflicting (declared_conflicts: the proposer declares: ADD-03:8.3)
- **UNRESOLVED ADD-03:T1-1/G** (table_row, p2): not promotable: ADD-03/T1-1/G insufficient_evidence (missing_information: the proposer declares missing: the accepted op answering ADD-03:6.1 (replacement of ADD-02:T1-1-rev by ADD-03:T1-1); a dry run of that op failed C22)
- **UNRESOLVED ADD-03:T1-1/total** (table_row, p2): not promotable: ADD-03/T1-1/total insufficient_evidence (missing_information: the proposer declares missing: the accepted op answering ADD-03:6.1; a dry run of that op failed C22; how the threshold in VOL-I:11.3 is read once the total is…)
- **UNRESOLVED ADD-03:7.1** (clause, p2): not promotable: ADD-03/7.1 insufficient_evidence (missing_information: the proposer declares missing: whether the Authority will give the Portal notice under ADD-03:7.1 by 12 November 2026)
- **UNRESOLVED ADD-03:8.2** (clause, p2): not promotable: ADD-03/8.2 conflicting (declared_conflicts: the proposer declares: Arabic Form 4-H (governing) threshold ١٠٪ vs English Appendix B 25%); ADD-03/8.2-issue conflicting (declared_conflicts: the proposer declares: ADD-03:p4-image/decl1 vs ADD-03:F4-H/para1)
- **UNRESOLVED ADD-03:8.3** (clause, p2): not promotable: ADD-03/8.3 insufficient_evidence (missing_information: the proposer declares missing: the pack's rule for counting Working Days forward from an event (VOL-I 2.4 covers backward counting only); the deadline is 2 or …)
- **UNRESOLVED ADD-03:Q17** (table_row, p3): not promotable: ADD-03/Q17 insufficient_evidence (missing_information: the proposer declares missing: Appendix C to ADD-03 (reference specific energy consumption in kWh/m3 and Energy Performance Statement format) is not in the evi…)
- **UNRESOLVED ADD-03:p4-image/decl1** (reading_block, p4): not promotable: ADD-03/p4-image/decl1 conflicting (declared_conflicts: the proposer declares: ADD-03:F4-H/para1); ADD-03/p4-image/decl1/issue conflicting (declared_conflicts: the proposer declares: ADD-03:F4-H/para1)
- **UNRESOLVED ADD-03:p4-image/field-cr-en** (reading_block, p4): not analysed: batch analysis-008 failed (the host session submitted nothing (the host ended with an error (success: 429)))
- **UNRESOLVED ADD-03:p4-image/field-cr-ar** (reading_block, p4): not analysed: batch analysis-008 failed (the host session submitted nothing (the host ended with an error (success: 429)))
- **UNRESOLVED ADD-03:p4-image/field-signatory-en** (reading_block, p4): not analysed: batch analysis-008 failed (the host session submitted nothing (the host ended with an error (success: 429)))
- **UNRESOLVED ADD-03:p4-image/field-signatory-ar** (reading_block, p4): not analysed: batch analysis-008 failed (the host session submitted nothing (the host ended with an error (success: 429)))
- **UNRESOLVED ADD-03:p4-image/field-capacity-en** (reading_block, p4): not analysed: batch analysis-008 failed (the host session submitted nothing (the host ended with an error (success: 429)))
- **UNRESOLVED ADD-03:p4-image/field-capacity-ar** (reading_block, p4): not analysed: batch analysis-008 failed (the host session submitted nothing (the host ended with an error (success: 429)))
- **UNRESOLVED ADD-03:p4-image/field-date-en** (reading_block, p4): not analysed: batch analysis-008 failed (the host session submitted nothing (the host ended with an error (success: 429)))
- **UNRESOLVED ADD-03:p4-image/field-date-ar** (reading_block, p4): not analysed: batch analysis-008 failed (the host session submitted nothing (the host ended with an error (success: 429)))
- **UNRESOLVED ADD-03:p4-image/field-signature-en** (reading_block, p4): not analysed: batch analysis-009 failed (the host session submitted nothing (the host ended with an error (success: 429)))
- **UNRESOLVED ADD-03:p4-image/field-signature-ar** (reading_block, p4): not analysed: batch analysis-009 failed (the host session submitted nothing (the host ended with an error (success: 429)))
- **UNRESOLVED ADD-03:p4-image/note** (reading_block, p4): not analysed: batch analysis-009 failed (the host session submitted nothing (the host ended with an error (success: 429)))
- **UNRESOLVED ADD-03:p4-image/image-footer** (reading_block, p4): not analysed: batch analysis-009 failed (the host session submitted nothing (the host ended with an error (success: 429)))
- **UNRESOLVED ADD-03:AppB/para1** (paragraph, p5): not analysed: batch analysis-009 failed (the host session submitted nothing (the host ended with an error (success: 429)))

## Per provision: source evidence → proposed transition → validation → downstream impact → output difference

### ADD-03:cover/para1 (paragraph, p1) — answered
- source: “Issued 9 November 2026”
- transition: `ADD-03/cover/para1` disposition no_effect: Issue date line 'Issued 9 November 2026'; dates the addendum (stage date) and changes no provision.
  - validation: **evidence_verified**

### ADD-03:cover/para2 (paragraph, p1) — answered
- source: “Tender NUPA/ISTP/2026/014”
- transition: `ADD-03/cover/para2` disposition no_effect: Title/reference line 'Tender NUPA/ISTP/2026/014' under heading 'ADDENDUM NO. 3'; identifies the tender, changes nothing.
  - validation: **evidence_verified**

### ADD-03:cover/para3 (paragraph, p1) — UNRESOLVED
- source: “This Addendum amends the definition of Estimated Project Cost, the financial capacity requirement in Volume I Clause 8.4 and the delay liquidated damages in Volume V Clause 18.1, relaxes the velocity limit for the treated effluent transmission main, amends Section 5.1 of Addendum No. 1, reissues the technical evaluation table to add a criterion for energy e…”
- transition: `ADD-03/cover/para3` amendment_op annotate ADD-03:cover/para3 effect adds_obligation
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:8.3

### ADD-03:1.1 (clause, p1) — answered
- source: “This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.”
- transition: `ADD-03/1.1` disposition no_effect: Recital: 'takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2' restates the existing rule in VOL-I 3.2(a) '(a) the Addenda, a lat…
  - validation: **evidence_verified**

### ADD-03:1.2 (clause, p1) — answered
- source: “A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.”
- transition: `ADD-03/1.2` disposition no_effect: Interpretation rule for references within this Addendum: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended b…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'unless')

### ADD-03:2.1 (clause, p1) — answered
- source: “In Volume V Clause 1.3, ‘as set out in the agreed Financial Model at Financial Close’ is deleted and ‘as stated by the Bidder in Form 4-F, excluding financing costs, interest during construction and development fees’ is substituted.”
- transition: `ADD-03/2.1` amendment_op replace_text VOL-V:1.3 “as set out in the agreed Financial Model at Financial Close” → “as stated by the Bidder in Form 4-F, excluding financing costs, interest during…”
  - validation: **evidence_verified**
  - downstream: units changed VOL-V:1.3; rows citing them none

### ADD-03:2.2 (clause, p1) — answered
- source: “The definition in Volume V Clause 1.3, as amended by Section 2.1, applies wherever the expression Estimated Project Cost is used in the RFP Documents.”
- transition: `ADD-03/2.2` amendment_op annotate VOL-V:1.3 effect interprets
  - validation: **interpretation_pending**

### ADD-03:3.1 (clause, p1) — answered
- source: “In Volume I Clause 8.4, ‘SAR 800,000,000’ is deleted and ‘twenty-five per cent (25%) of the Estimated Project Cost’ is substituted. Limb (b) of Clause 8.4 is unchanged.”
- transition: `ADD-03/3.1` amendment_op replace_text VOL-I:8.4 “SAR 800,000,000” → “twenty-five per cent (25%) of the Estimated Project Cost”
  - validation: **evidence_verified**
  - downstream: units changed VOL-I:8.4; rows citing them VOL-I-8.4-01, VOL-I-8.4-02
  - output difference: CHANGED VOL-I-8.4-01; CHANGED VOL-I-8.4-02; A5 REWORK fin-standing; A5 REWORK fin-statements; A5 REVIEW (possible impact) fin-standing; A5 REVIEW (possible impact) fin-statements

### ADD-03:4.1 (clause, p1) — answered
- source: “In Volume V Clause 18.1, ‘SAR 180,000 for each day of delay’ is deleted and ‘one-twentieth of one per cent (0.05%) of the Estimated Project Cost for each day of delay’ is substituted. Volume V Clause 18.4 is unchanged.”
- transition: `ADD-03/4.1` amendment_op replace_text VOL-V:18.1 “SAR 180,000 for each day of delay” → “one-twentieth of one per cent (0.05%) of the Estimated Project Cost for each da…”
  - validation: **evidence_verified**
  - downstream: units changed VOL-V:18.1; rows citing them none

### ADD-03:5.1 (clause, p1) — answered
- source: “In Volume II Clause 5.2, ‘2.0 m/s’ is deleted and ‘1.5 m/s’ is substituted. The minimum residual head of 15 m at the delivery point is unchanged.”
- transition: `ADD-03/5.1` amendment_op replace_text VOL-II:5.2 “2.0 m/s” → “1.5 m/s”
  - validation: **evidence_verified**
  - downstream: units changed VOL-II:5.2; rows citing them VOL-II-5.2-01, VOL-II-5.2-02
  - output difference: CHANGED VOL-II-5.2-01; CHANGED VOL-II-5.2-02; A5 REWORK technical-proposal

### ADD-03:5.2 (clause, p1) — UNRESOLVED
- source: “With effect from 8 October 2026, Section 5.1 of Addendum No. 1 is amended by deleting ‘for the buried sections of the transmission main’ and substituting ‘for the buried sections of the transmission main other than the trenchless crossings required by Volume II Clause 5.4, at which ductile iron only shall be used’.”
- transition: `ADD-03/5.2` escalation why: The provision amends an earlier addendum's amending text (ADD-01:5.1) 'With effect from 8 October 2026'. A replace_text on ADD-01:5.1 simulates as structurally valid, but the engine reports the same …
  - validation: **escalated** — missing_information: the proposer declares missing: How the engine should carry a deferred effective date (8 October 2026); Whether the change must be applied to VOL-II:5.3 as well as ADD-01:5.1

### ADD-03:6.1 (clause, p2) — UNRESOLVED
- source: “Table 1-1 (revised) and the Notes to it, issued by Section 3 of Addendum No. 2, are deleted and replaced by the table and Notes below, which add criterion G (energy efficiency). The marks for criteria A to F are unchanged.”
- transition: `ADD-03/6.1` escalation why: The provision replaces Table 1-1 (revised) and its Notes issued by ADD-02 Section 3. The natural op (replace_unit ADD-02:T1-1-rev with replacement ADD-03:T1-1) fails C22 in simulation: 'the provision…
  - validation: **escalated** — missing_information: the proposer declares missing: A resolvable target for 'Table 1-1 (revised) ... issued by Section 3 of Addendum No. 2'; How the Notes units are to be replaced

### ADD-03:T1-1/A (table_row, p2) — answered
- source: “Ref: A | Criterion: Process design, treatment performance and compliance with Volume II | Marks: 25”
- transition: `ADD-03/T1-1/A` disposition no_effect: Row A of the replacement Table 1-1 (second revision). Its cells are identical to ADD-02:T1-1-rev/A and ADD-03:6.1 states 'The marks for criteria A to F are unc…
  - validation: **interpretation_pending**

### ADD-03:T1-1/B (table_row, p2) — answered
- source: “Ref: B | Criterion: Construction methodology, programme and interface management | Marks: 15”
- transition: `ADD-03/T1-1/B` disposition no_effect: Row B of the replacement Table 1-1 (second revision). Its cells are identical to ADD-02:T1-1-rev/B and ADD-03:6.1 states 'The marks for criteria A to F are unc…
  - validation: **interpretation_pending**

### ADD-03:T1-1/C (table_row, p2) — answered
- source: “Ref: C | Criterion: Operations and maintenance philosophy and lifecycle strategy | Marks: 20”
- transition: `ADD-03/T1-1/C` disposition no_effect: Row C of the replacement Table 1-1 (second revision). Its cells are identical to ADD-02:T1-1-rev/C and ADD-03:6.1 states 'The marks for criteria A to F are unc…
  - validation: **interpretation_pending**

### ADD-03:T1-1/D (table_row, p2) — answered
- source: “Ref: D | Criterion: Environmental and social management | Marks: 20”
- transition: `ADD-03/T1-1/D` disposition no_effect: Row D of the replacement Table 1-1 (second revision). Its cells are identical to ADD-02:T1-1-rev/D and ADD-03:6.1 states 'The marks for criteria A to F are unc…
  - validation: **interpretation_pending**

### ADD-03:T1-1/E (table_row, p2) — answered
- source: “Ref: E | Criterion: Organisation, key personnel and consortium governance | Marks: 10”
- transition: `ADD-03/T1-1/E` disposition no_effect: Row E of the replacement Table 1-1 (second revision). Its cells are identical to ADD-02:T1-1-rev/E and ADD-03:6.1 states 'The marks for criteria A to F are unc…
  - validation: **interpretation_pending**

### ADD-03:T1-1/F (table_row, p2) — answered
- source: “Ref: F | Criterion: Health, safety and security of supply | Marks: 10”
- transition: `ADD-03/T1-1/F` disposition no_effect: Row F of the replacement Table 1-1 (second revision). Its cells are identical to ADD-02:T1-1-rev/F and ADD-03:6.1 states 'The marks for criteria A to F are unc…
  - validation: **interpretation_pending**

### ADD-03:T1-1/G (table_row, p2) — UNRESOLVED
- source: “Ref: G | Criterion: Energy efficiency and specific energy consumption | Marks: 20”
- transition: `ADD-03/T1-1/G` disposition unresolved: Insufficient evidence in this batch. Row G is a new criterion, not present in ADD-02 Table 1-1 (revised), and is introduced by ADD-03:6.1: 'which add criterion…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: the accepted op answering ADD-03:6.1 (replacement of ADD-02:T1-1-rev by ADD-03:T1-1); a dry run of that op failed C22

### ADD-03:T1-1/total (table_row, p2) — UNRESOLVED
- source: “Criterion: Total | Marks: 120”
- transition: `ADD-03/T1-1/total` disposition unresolved: Insufficient evidence in this batch. The Total changes from 'Criterion: Total | Marks: 100' (ADD-02:T1-1-rev/total) to 'Criterion: Total | Marks: 120'. That ch…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: the accepted op answering ADD-03:6.1; a dry run of that op failed C22; how the threshold in VOL-I:11.3 is read once the total is 120 (this depends on ADD-03:6.2, which is in another batch)

### ADD-03:S6/para1 (paragraph, p2) — answered
- source: “Notes to Table 1-1 (second revision): (1) The technical score threshold in Volume I Clause 11.3 is unchanged at seventy per cent (70%). (2) The combined score weighting stated in Volume I Clause 11.2 is amended to seventy per cent (70%) technical and thirty per cent (30%) commercial. (3) Marks are awarded on the Authority's standard five-point scale and mul…”
- transition: `ADD-03/S6/para1(a)` amendment_op annotate VOL-I:11.3 effect confirms
  - validation: **conflicting** — declared_conflicts: the proposer declares: VOL-I:11.3 as it stands at ADD-02 sets 70 marks out of 100; Note (1) calls a 70% threshold 'unchanged' while Table 1-1 now totals 120 marks
- transition: `ADD-03/S6/para1(b)` amendment_op replace_text VOL-I:11.2 “sixty-five per cent (65%) technical and thirty-five per cent (35%) commercial” → “seventy per cent (70%) technical and thirty per cent (30%) commercial”
  - validation: **interpretation_pending**
- transition: `ADD-03/S6/para1(c)` amendment_op annotate ADD-03:T1-1 effect confirms
  - validation: **interpretation_pending**
- transition: `ADD-03/S6/para1(d)` amendment_op annotate ADD-03:T1-1/G effect adds_obligation
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: Appendix C to ADD-03 (format of the Energy Performance Statement and reference specific energy consumption) is not in the evidence build
  - downstream: units changed VOL-I:11.2; rows citing them VOL-I-11.2-01
  - output difference: CHANGED VOL-I-11.2-01

### ADD-03:6.2 (clause, p2) — answered
- source: “Volume I Clause 11.3 is deleted and replaced by the following two Clauses: ‘11.3 A Proposal whose technical score is less than seventy per cent (70%) of the total marks available in Table 1-1 shall not proceed to commercial evaluation.’ ‘11.3A The Envelope B of a Proposal that does not proceed to commercial evaluation shall be retained unopened by the Autho…”
- transition: `ADD-03/6.2(a)` amendment_op replace_text VOL-I:11.3 “A Proposal scoring less than seventy (70) marks out of one hundred (100) at the…” → “A Proposal whose technical score is less than seventy per cent (70%) of the tot…”
  - validation: **interpretation_pending**
- transition: `ADD-03/6.2(b)` amendment_op insert_unit VOL-I:11.3 “The Envelope B of a Proposal that does not proceed to commercial evaluation shall be retained unopened by the Authority…”
  - validation: **evidence_verified**
  - downstream: units changed VOL-I:11.3, VOL-I:11.3+ADD-03; rows citing them VOL-I-11.3-01
  - output difference: CHANGED VOL-I-11.3-01; A5 REWORK technical-proposal

### ADD-03:7.1 (clause, p2) — UNRESOLVED
- source: “This Section 7 has effect only if the Authority notifies Bidders through the Portal, not later than ten (10) Working Days before the Proposal Due Date, that the grid connection point referred to in Volume II Clause 1.4 will not be energised at least twelve (12) months before the Scheduled PCOD. If no such notice is given by that time, this Section 7 lapses.”
- transition: `ADD-03/7.1` amendment_op annotate VOL-II:1.4 effect interprets
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: whether the Authority will give the Portal notice under ADD-03:7.1 by 12 November 2026

### ADD-03:7.2 (clause, p2) — UNRESOLVED
- source: “Where this Section 7 has effect: (a) in Volume II Clause 1.4, the words ‘together with a grid connection point at the site boundary’, and the comma before them, are deleted; (b) the grid connection is a utility to be procured by the Project Company under the second sentence of Volume II Clause 1.4; and (c) the cost of the grid connection works forms part of…”
- transition: `ADD-03/7.2` escalation why: ADD-03:7.2 prints a deletion in VOL-II:1.4 (', together with a grid connection point at the site boundary') and moves the grid connection, and its cost, to the Project Company, but only 'Where this S…
  - validation: **escalated** — missing_information: the proposer declares missing: whether the Authority notice under ADD-03:7.1 is given by 12 November 2026

### ADD-03:8.1 (clause, p2) — answered
- source: “A new Form 4-H (Declaration of Beneficial Ownership) is added to Volume IV and to the list at Volume I Clause 9.1, to be inserted after Form 4-G. Form 4-H is reproduced at Appendix A to this Addendum.”
- transition: `ADD-03/8.1` amendment_op insert_unit VOL-I:9.1
  - validation: **interpretation_pending**
  - downstream: units changed ADD-03:F4-H/T1, ADD-03:F4-H/T1/1, ADD-03:F4-H/T1/2, ADD-03:F4-H/T1/3, ADD-03:F4-H/T1/4, ADD-03:F4-H/para1, ADD-03:F4-H/para2, ADD-03:H:F4-H, VOL-I:9.1+ADD-03; rows citing them none

### ADD-03:8.2 (clause, p2) — UNRESOLVED
- source: “Form 4-H shall be completed in the Arabic language, signed and stamped by an authorised signatory of each member of the Bidder. The Arabic text governs. The English translation at Appendix B is provided for convenience only.”
- transition: `ADD-03/8.2` amendment_op annotate ADD-03:H:F4-H effect adds_obligation
  - validation: **conflicting** — declared_conflicts: the proposer declares: Arabic Form 4-H (governing) threshold ١٠٪ vs English Appendix B 25%
- transition: `ADD-03/8.2-issue` issue {"text": "The governing Arabic Form 4-H (Appendix A) defines a beneficial owner at ten per cent (١٠٪) or more, while the English translation at Appendix B states twenty-five per cent (25%). Under ADD…
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:p4-image/decl1 vs ADD-03:F4-H/para1

### ADD-03:8.3 (clause, p2) — UNRESOLVED
- source: “Form 4-H shall be submitted with Envelope A. A member of the Bidder that is incorporated outside the Kingdom may instead submit its Form 4-H through the Portal not later than five (5) Working Days after the Proposal Due Date.”
- transition: `ADD-03/8.3` amendment_op annotate ADD-03:H:F4-H effect adds_obligation
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: the pack's rule for counting Working Days forward from an event (VOL-I 2.4 covers backward counting only); the deadline is 2 or 3 December 2026

### ADD-03:8.4 (clause, p2) — answered
- source: “Failure to submit a complete and properly executed Form 4-H for each member of the Bidder by the time required by Section 8.3 shall render the Proposal non-responsive.”
- transition: `ADD-03/8.4` amendment_op annotate ADD-03:H:F4-H effect adds_obligation
  - validation: **interpretation_pending**

### ADD-03:Q15 (table_row, p3) — answered
- source: “No: 15 | Bidder question: Volume I Clause 8.7 requires a Parent Company Guarantee that is unconditional as to the EPC Contractor's obligations during the construction period. Will the Authority accept a guarantee limited to a fixed amount? | Authority response: No. The Parent Company Guarantee shall be unlimited as to the guaranteed obligations and shall no…”
- transition: `ADD-03/Q15` amendment_op annotate VOL-I:8.7, VOL-IV:F4-D effect confirms
  - validation: **interpretation_pending**

### ADD-03:Q16 (table_row, p3) — answered
- source: “No: 16 | Bidder question: Does the Estimated Project Cost to be stated in Form 4-F include the cost of the grid connection works? | Authority response: Only if Section 7 of this Addendum has effect. Otherwise the grid connection point is provided by the Authority in accordance with Volume II Clause 1.4.”
- transition: `ADD-03/Q16` amendment_op annotate VOL-II:1.4, VOL-IV:F4-F effect interprets
  - validation: **interpretation_pending**

### ADD-03:Q17 (table_row, p3) — UNRESOLVED
- source: “No: 17 | Bidder question: Will the Authority publish the reference specific energy consumption against which criterion G of Table 1-1 will be assessed? | Authority response: The reference specific energy consumption, in kWh per cubic metre of treated effluent, is stated in Appendix C to this Addendum together with the format of the Energy Performance Statem…”
- transition: `ADD-03/Q17` disposition unresolved: insufficient evidence: the response says the reference specific energy consumption 'is stated in Appendix C to this Addendum together with the format of the En…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: Appendix C to ADD-03 (reference specific energy consumption in kWh/m3 and Energy Performance Statement format) is not in the evidence build

### ADD-03:Q18 (table_row, p3) — answered
- source: “No: 18 | Bidder question: Does the maximum velocity in Volume II Clause 5.2 apply to the trenchless crossings? | Authority response: Yes. Volume II Clause 5.2, as amended by Section 5.1 of this Addendum, applies to the whole length of the transmission main, including the crossings required by Volume II Clause 5.4.”
- transition: `ADD-03/Q18` amendment_op annotate VOL-II:5.2, VOL-II:5.4 effect interprets
  - validation: **interpretation_pending**

### ADD-03:Q19 (table_row, p3) — answered
- source: “No: 19 | Bidder question: How is compliance with Volume I Clause 8.4(a), as amended, to be demonstrated in Envelope A, given that the Estimated Project Cost is stated only in Form 4-F? | Authority response: The Authority notes the question. Volume I Clauses 6.2 and 11.1 apply. The Authority does not consider further amendment necessary at this stage.”
- transition: `ADD-03/Q19` amendment_op annotate VOL-I:8.4, VOL-I:6.2, VOL-I:11.1 effect none
  - validation: **interpretation_pending**
- transition: `ADD-03/Q19/issue` issue {"text": "If ADD-03 3.1 makes the VOL-I 8.4(a) net worth threshold a percentage of the Estimated Project Cost, a figure stated only in Form 4-F (Envelope B only), then showing compliance in Envelope …
  - validation: **interpretation_pending**

### ADD-03:Q20 (table_row, p3) — answered
- source: “No: 20 | Bidder question: Must the certified copy of the register of shareholders attached to Form 4-H be legalised where the member is incorporated outside the Kingdom? | Authority response: No. Legalisation is not required for the purposes of Form 4-H.”
- transition: `ADD-03/Q20` amendment_op annotate ADD-03:p4-image/decl3, ADD-03:F4-H/para1 effect interprets
  - validation: **interpretation_pending**

### ADD-03:AppA/para1 (paragraph, p3) — answered
- source: “Form 4-H is reproduced on the following page as issued. It shall be completed in the Arabic language in accordance with Section 8 of this Addendum.”
- transition: `ADD-03/AppA/para1` disposition no_effect: introductory text to Appendix A. The words 'Form 4-H is reproduced on the following page as issued. It shall be completed in the Arabic language in accordance …
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'shall' (cites ADD-03:F4-H))
- transition: `ADD-03/AppA/para1/issue` issue {"text": "The Arabic Form 4-H reproduced 'as issued' at Appendix A (which governs under ADD-03 8.2) defines a beneficial owner at ten per cent (10%) or more. The English translation at Appendix B (F4…
  - validation: **evidence_verified**

### ADD-03:p4-image/hdr-en (reading_block, p4) — answered
- source: “NORTHERN UTILITIES PROCUREMENT AUTHORITY”
- transition: `ADD-03/p4-image/hdr-en` disposition no_effect: Letterhead line of the Form 4-H image reproduced at Appendix A ('NORTHERN UTILITIES PROCUREMENT AUTHORITY'); names the issuing authority and changes no clause,…
  - validation: **interpretation_pending**

### ADD-03:p4-image/hdr-ar (reading_block, p4) — answered
- source: “الهيئة الشمالية للمشتريات المرفقية”
- transition: `ADD-03/p4-image/hdr-ar` disposition no_effect: Arabic letterhead line of the Form 4-H image ('الهيئة الشمالية للمشتريات المرفقية'); names the issuing authority and changes nothing by itself. The form's addi…
  - validation: **interpretation_pending**

### ADD-03:p4-image/ref-en (reading_block, p4) — answered
- source: “Tender Ref: NUPA/ISTP/2026/014”
- transition: `ADD-03/p4-image/ref-en` disposition no_effect: Tender reference line of the Form 4-H image ('Tender Ref: NUPA/ISTP/2026/014'); identification only, changes nothing.
  - validation: **interpretation_pending**

### ADD-03:p4-image/ref-ar (reading_block, p4) — answered
- source: “مناقصة رقم: NUPA/ISTP/2026/014”
- transition: `ADD-03/p4-image/ref-ar` disposition no_effect: Arabic tender reference line of the Form 4-H image ('مناقصة رقم: NUPA/ISTP/2026/014'); identification only, changes nothing.
  - validation: **interpretation_pending**

### ADD-03:p4-image/form-en (reading_block, p4) — answered
- source: “FORM 4-H”
- transition: `ADD-03/p4-image/form-en` disposition no_effect: Form label 'FORM 4-H' on the reproduced form; the form itself is added by ADD-03:8.1 ('A new Form 4-H (Declaration of Beneficial Ownership) is added to Volume …
  - validation: **interpretation_pending**

### ADD-03:p4-image/form-ar (reading_block, p4) — answered
- source: “النموذج ٤-ح”
- transition: `ADD-03/p4-image/form-ar` disposition no_effect: Arabic form label 'النموذج ٤-ح' on the reproduced form; the form is added by ADD-03:8.1; this label changes nothing by itself.
  - validation: **interpretation_pending**

### ADD-03:p4-image/title (reading_block, p4) — answered
- source: “إقرار المستفيد الحقيقي”
- transition: `ADD-03/p4-image/title` disposition no_effect: Arabic form title 'إقرار المستفيد الحقيقي' on the reproduced form; heading only; the form is added by ADD-03:8.1.
  - validation: **interpretation_pending**

### ADD-03:p4-image/intro (reading_block, p4) — answered
- source: “نحن الموقعون أدناه، بصفتنا ممثلين مفوضين عن العضو المذكور أدناه في ائتلاف مقدم العرض، نقر ونتعهد بما يلي:”
- transition: `ADD-03/p4-image/intro` disposition no_effect: Opening words of the declaration inside the reproduced Form 4-H: 'نحن الموقعون أدناه، بصفتنا ممثلين مفوضين عن العضو المذكور أدناه في ائتلاف مقدم العرض، نقر ونت…
  - validation: **interpretation_pending**

### ADD-03:p4-image/decl1 (reading_block, p4) — UNRESOLVED
- source: “أولاً: أن الأشخاص الطبيعيين المبينين في الجدول أدناه هم جميع المستفيدين الحقيقيين من العضو، والمستفيد الحقيقي هو كل شخص طبيعي يملك، بصورة مباشرة أو غير مباشرة، ما نسبته عشرة في المائة (١٠٪) أو أكثر من رأس مال العضو أو من حقوق التصويت فيه، أو يسيطر على العضو بأي وسيلة أخرى.”
- transition: `ADD-03/p4-image/decl1` disposition unresolved: Insufficient evidence to settle by an op or no_effect. This is the first declaration of the new Form 4-H (added by ADD-03:8.1, another batch). The Arabic print…
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:F4-H/para1
- transition: `ADD-03/p4-image/decl1/issue` issue {"text": "Form 4-H beneficial-owner threshold differs between the governing Arabic text (Appendix A: 'عشرة في المائة (١٠٪)', 10%) and the English convenience translation (Appendix B: 'twenty-five per…
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:F4-H/para1

### ADD-03:p4-image/decl2 (reading_block, p4) — answered
- source: “ثانياً: أنه لا يملك أيٌّ من المستفيدين الحقيقيين، بصورة مباشرة أو غير مباشرة، أي حصة في عضو في ائتلاف آخر يقدم عرضاً لهذه المناقصة.”
- transition: `ADD-03/p4-image/decl2` disposition no_effect: Content of the new Form 4-H reproduced at Appendix A ('Form 4-H is reproduced at Appendix A to this Addendum', ADD-03:8.1); the declaration 'أنه لا يملك أيٌّ م…
  - validation: **interpretation_pending**

### ADD-03:p4-image/decl3 (reading_block, p4) — answered
- source: “ثالثاً: أننا أرفقنا بهذا الإقرار نسخة مصدقة من سجل الشركاء أو المساهمين في العضو، صادرة خلال الثلاثين (٣٠) يوماً السابقة لتاريخ تقديم العروض.”
- transition: `ADD-03/p4-image/decl3` disposition no_effect: Content of the new Form 4-H reproduced at Appendix A ('Form 4-H is reproduced at Appendix A to this Addendum', ADD-03:8.1). The declaration 'أننا أرفقنا بهذا ا…
  - validation: **interpretation_pending**

### ADD-03:p4-image/table-header (reading_block, p4) — answered
- source: “م | اسم المستفيد الحقيقي | الجنسية | نسبة الملكية (٪) | مباشرة / غير مباشرة”
- transition: `ADD-03/p4-image/table-header` disposition no_effect: Column headings of the beneficial-owner table in the new Form 4-H ('م | اسم المستفيد الحقيقي | الجنسية | نسبة الملكية (٪) | مباشرة / غير مباشرة'); form layout …
  - validation: **interpretation_pending**

### ADD-03:p4-image/table-row4 (reading_block, p4) — answered
- source: “٤”
- transition: `ADD-03/p4-image/table-row4` disposition no_effect: Row number '٤' (4) of the blank beneficial-owner table in the new Form 4-H; form layout carried in by ADD-03:8.1 ('Form 4-H is reproduced at Appendix A to this…
  - validation: **interpretation_pending**

### ADD-03:p4-image/table-row4-blank (reading_block, p4) — answered
- source: “”
- transition: `ADD-03/p4-image/table-row4-blank` disposition no_effect: Empty cells of row 4 of the beneficial-owner table in the new Form 4-H (the unit's text is empty: nothing is printed); blanks for the bidder to complete, carri…
  - validation: **interpretation_pending**

### ADD-03:p4-image/field-member-en (reading_block, p4) — answered
- source: “Name of consortium member”
- transition: `ADD-03/p4-image/field-member-en` disposition no_effect: English field label 'Name of consortium member' of the new Form 4-H; form layout carried in by ADD-03:8.1 ('Form 4-H is reproduced at Appendix A to this Addend…
  - validation: **interpretation_pending**

### ADD-03:p4-image/field-member-ar (reading_block, p4) — answered
- source: “اسم العضو في الائتلاف :”
- transition: `ADD-03/p4-image/field-member-ar` disposition no_effect: Arabic field label 'اسم العضو في الائتلاف :' of the new Form 4-H; form layout carried in by ADD-03:8.1 ('Form 4-H is reproduced at Appendix A to this Addendum'…
  - validation: **interpretation_pending**

### ADD-03:p4-image/field-cr-en (reading_block, p4) — UNRESOLVED
- source: “Commercial registration number”
- transition: none (not analysed: batch analysis-008 failed (the host session submitted nothing (the host ended with an error (success: 429))))

### ADD-03:p4-image/field-cr-ar (reading_block, p4) — UNRESOLVED
- source: “رقم السجل التجاري :”
- transition: none (not analysed: batch analysis-008 failed (the host session submitted nothing (the host ended with an error (success: 429))))

### ADD-03:p4-image/field-signatory-en (reading_block, p4) — UNRESOLVED
- source: “Name of authorised signatory”
- transition: none (not analysed: batch analysis-008 failed (the host session submitted nothing (the host ended with an error (success: 429))))

### ADD-03:p4-image/field-signatory-ar (reading_block, p4) — UNRESOLVED
- source: “اسم المفوض بالتوقيع :”
- transition: none (not analysed: batch analysis-008 failed (the host session submitted nothing (the host ended with an error (success: 429))))

### ADD-03:p4-image/field-capacity-en (reading_block, p4) — UNRESOLVED
- source: “Capacity”
- transition: none (not analysed: batch analysis-008 failed (the host session submitted nothing (the host ended with an error (success: 429))))

### ADD-03:p4-image/field-capacity-ar (reading_block, p4) — UNRESOLVED
- source: “الصفة :”
- transition: none (not analysed: batch analysis-008 failed (the host session submitted nothing (the host ended with an error (success: 429))))

### ADD-03:p4-image/field-date-en (reading_block, p4) — UNRESOLVED
- source: “Date”
- transition: none (not analysed: batch analysis-008 failed (the host session submitted nothing (the host ended with an error (success: 429))))

### ADD-03:p4-image/field-date-ar (reading_block, p4) — UNRESOLVED
- source: “التاريخ :”
- transition: none (not analysed: batch analysis-008 failed (the host session submitted nothing (the host ended with an error (success: 429))))

### ADD-03:p4-image/field-signature-en (reading_block, p4) — UNRESOLVED
- source: “Signature and company seal”
- transition: none (not analysed: batch analysis-009 failed (the host session submitted nothing (the host ended with an error (success: 429))))

### ADD-03:p4-image/field-signature-ar (reading_block, p4) — UNRESOLVED
- source: “التوقيع والختم :”
- transition: none (not analysed: batch analysis-009 failed (the host session submitted nothing (the host ended with an error (success: 429))))

### ADD-03:p4-image/note (reading_block, p4) — UNRESOLVED
- source: “ملاحظة: يجب تقديم هذا النموذج باللغة العربية عن كل عضو من أعضاء الائتلاف، والنص العربي هو المعتمد. عدم تقديمه كاملاً يجعل العرض غير مستجيب.”
- transition: none (not analysed: batch analysis-009 failed (the host session submitted nothing (the host ended with an error (success: 429))))

### ADD-03:p4-image/image-footer (reading_block, p4) — UNRESOLVED
- source: “FICTIONAL DOCUMENT - Lamar Holding internal assessment pack - not a real tender.”
- transition: none (not analysed: batch analysis-009 failed (the host session submitted nothing (the host ended with an error (success: 429))))

### ADD-03:AppB/para1 (paragraph, p5) — UNRESOLVED
- source: “This translation is provided for convenience only. The Arabic text of Form 4-H at Appendix A governs.”
- transition: none (not analysed: batch analysis-009 failed (the host session submitted nothing (the host ended with an error (success: 429))))

### ADD-03:F4-H/para1 (paragraph, p5) — answered
- source: “We, the undersigned, as the authorised representatives of the member of the Bidder's consortium named below, declare and undertake as follows: First: that the natural persons listed in the table below are all of the beneficial owners of the member, a beneficial owner being each natural person who owns, directly or indirectly, twenty-five per cent (25%) or m…”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/T1/1 (table_row, p5) — answered
- source: “No: 1”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/T1/2 (table_row, p5) — answered
- source: “No: 2”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/T1/3 (table_row, p5) — answered
- source: “No: 3”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/T1/4 (table_row, p5) — answered
- source: “No: 4”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/para2 (paragraph, p5) — answered
- source: “Name of consortium member: _______________________ Commercial registration number: _______________ Name of authorised signatory: _______________________ Capacity: _______________ Date: ____________ Signature and company seal: _______________ Note: This Form shall be submitted in the Arabic language for each member of the consortium, and the Arabic text gove…”
- transition: content of ADD-03/8.1

## Downstream proposals (validated in the candidate)

| Item | Type | Task | Status | First failed check, or what a person confirms |
|---|---|---|---|---|

## Promoted into the candidate (PROPOSED; nothing accepted)

- ops: ADD-03/2.1, ADD-03/2.2, ADD-03/3.1, ADD-03/4.1, ADD-03/5.1, ADD-03/S6/para1(b), ADD-03/S6/para1(c), ADD-03/6.2(a), ADD-03/6.2(b), ADD-03/8.1, ADD-03/8.4, ADD-03/Q15, ADD-03/Q16, ADD-03/Q18, ADD-03/Q19, ADD-03/Q20
- dispositions: ADD-03:cover/para1: no_effect, ADD-03:cover/para2: no_effect, ADD-03:1.1: no_effect, ADD-03:1.2: no_effect, ADD-03:T1-1/A: no_effect, ADD-03:T1-1/B: no_effect, ADD-03:T1-1/C: no_effect, ADD-03:T1-1/D: no_effect, ADD-03:T1-1/E: no_effect, ADD-03:T1-1/F: no_effect, ADD-03:AppA/para1: no_effect, ADD-03:p4-image/hdr-en: no_effect, ADD-03:p4-image/hdr-ar: no_effect, ADD-03:p4-image/ref-en: no_effect, ADD-03:p4-image/ref-ar: no_effect, ADD-03:p4-image/form-en: no_effect, ADD-03:p4-image/form-ar: no_effect, ADD-03:p4-image/title: no_effect, ADD-03:p4-image/intro: no_effect, ADD-03:p4-image/decl2: no_effect, ADD-03:p4-image/decl3: no_effect, ADD-03:p4-image/table-header: no_effect, ADD-03:p4-image/table-row4: no_effect, ADD-03:p4-image/table-row4-blank: no_effect, ADD-03:p4-image/field-member-en: no_effect, ADD-03:p4-image/field-member-ar: no_effect
- unresolved provisions: 24

## check-register on the candidate

- exit 1; 8 finding(s) {'C46': 8}
  - [C46] ADD-03/4.1: [A1] ADD-03/4.1 (replace_text) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'In Volume V Clause 18.1, ‘SAR 180,000 for each day of delay’ is deleted and ‘one-twentieth of …
  - [C46] ADD-03/6.2(b): [A1] ADD-03/6.2(b) (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-I:11.3; a row of the anchor VOL-I:11.3 does not count): 'Volume I…
  - [C46] ADD-03/6.2(b): [A3] ADD-03/6.2(b) brings in consequence words ['not proceed'] that no row's consequence carries at ADD-03: 'Volume I Clause 11.3 is deleted and replaced by the following two Clauses: ‘11.3 A Proposa…
  - [C46] ADD-03/8.1: [A1] ADD-03/8.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-I:9.1; a row of the anchor VOL-I:9.1 does not count): 'A new Form 4-…
  - [C46] ADD-03/8.1: [A1] ADD-03/8.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the new ADD-03:F4-H; a row of the anchor VOL-I:9.1 does not count): 'A new Form 4-H (Declaration…
  - [C46] ADD-03/8.1: [A3] ADD-03/8.1 brings in consequence words ['non-responsive'] that no row's consequence carries at ADD-03: 'A new Form 4-H (Declaration of Beneficial Ownership) is added to Volume IV and to the list…
  - [C46] ADD-03/8.4: [A1] ADD-03/8.4 (annotate) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Failure to submit a complete and properly executed Form 4-H for each member of the Bidder by the t…
  - [C46] ADD-03/8.4: [A3] ADD-03/8.4 brings in consequence words ['non-responsive'] that no row's consequence carries at ADD-03: 'Failure to submit a complete and properly executed Form 4-H for each member of the Bidder …

## Coverage

- provisions: 70; accounted for by the combined set: 57; states {'validated': 57, 'pending': 13}
- resolution (controller): resolved 7, pending 50, invalid 0, unaccounted 13; approved 0
- structural units of ADD-03 that are not provisions (listed so nothing is dropped): ADD-03:H:cover (heading), ADD-03:H:cover-2 (heading), ADD-03:H:S1 (heading), ADD-03:H:S2 (heading), ADD-03:H:S3 (heading), ADD-03:H:S4 (heading), ADD-03:H:S5 (heading), ADD-03:H:S6 (heading), ADD-03:T1-1 (table), ADD-03:H:S7 (heading), ADD-03:H:S8 (heading), ADD-03:H:S9 (heading), ADD-03:S9/QA (table), ADD-03:H:AppA (heading), ADD-03:region:ADD-03-p4-r1 (region), ADD-03:p4-image (image_text), ADD-03:H:AppB (heading), ADD-03:H:F4-H (heading), ADD-03:F4-H/T1 (table)
- batches: reading-ADD-03-p4-r1 done, analysis-001 done, analysis-002 done, analysis-003 done, analysis-004 done, analysis-005 done, analysis-006 done, analysis-007 done, analysis-008 failed (the host session submitted nothing (the host ended with an error (success: 429))), analysis-009 failed (the host session submitted nothing (the host ended with an error (success: 429))), analysis-010 skipped, downstream-001 failed (the host session's final message is not a DownstreamSet: the answer is not a si…), downstream-002 failed (the host session's final message is not a DownstreamSet: the answer is not a si…), downstream-003 failed (the host session's final message is not a DownstreamSet: the answer is not a si…), downstream-004 failed (the host session's final message is not a DownstreamSet: the answer is not a si…), downstream-005 failed (the host session's final message is not a DownstreamSet: the answer is not a si…)

## Manual interventions (and automatic host sessions, named as such: not a person)

- 2026-10-04T15:28:59Z: host session (automatic) — batch reading-ADD-03-p4-r1 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session reading an image; not a person
- 2026-10-04T15:33:47Z: host session (automatic) — batch analysis-001 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-04T15:36:52Z: host session (automatic) — batch analysis-002 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-04T15:41:07Z: host session (automatic) — batch analysis-003 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-04T15:48:44Z: host session (automatic) — batch analysis-004 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-04T15:55:29Z: host session (automatic) — batch analysis-005 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-04T15:59:57Z: host session (automatic) — batch analysis-006 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-04T16:05:57Z: host session (automatic) — batch analysis-007 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-04T16:08:13Z: host session (automatic) — batch analysis-008 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-04T16:08:15Z: host session (automatic) — batch analysis-009 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-04T16:08:24Z: host session (automatic) — batch downstream-001 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-04T16:08:26Z: host session (automatic) — batch downstream-002 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-04T16:08:28Z: host session (automatic) — batch downstream-003 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-04T16:08:30Z: host session (automatic) — batch downstream-004 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-04T16:08:32Z: host session (automatic) — batch downstream-005 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person

## The diff (ADD-02 → ADD-03; [diff.md](diff.md))

## What changed from ADD-02 to ADD-03

### ADD-03: PARTIAL (issued 2026-11-09)

- ops: 16 (0 invalid); provisions: 70 (24 unresolved)
- validated state: ADD-02 — this addendum does NOT replace it until every provision is treated and every op is valid
- UNRESOLVED ADD-03:cover/para3: This Addendum amends the definition of Estimated Project Cost, the financial capacity requirement in Volume I Clause 8.4 and the delay liquidated damages in Vol
- UNRESOLVED ADD-03:5.2: With effect from 8 October 2026, Section 5.1 of Addendum No. 1 is amended by deleting ‘for the buried sections of the transmission main’ and substituting ‘for t
- UNRESOLVED ADD-03:6.1: Table 1-1 (revised) and the Notes to it, issued by Section 3 of Addendum No. 2, are deleted and replaced by the table and Notes below, which add criterion G (en
- UNRESOLVED ADD-03:T1-1/G: Ref: G | Criterion: Energy efficiency and specific energy consumption | Marks: 20
- UNRESOLVED ADD-03:T1-1/total: Criterion: Total | Marks: 120
- UNRESOLVED ADD-03:7.1: This Section 7 has effect only if the Authority notifies Bidders through the Portal, not later than ten (10) Working Days before the Proposal Due Date, that the
- UNRESOLVED ADD-03:7.2: Where this Section 7 has effect: (a) in Volume II Clause 1.4, the words ‘together with a grid connection point at the site boundary’, and the comma before them,
- UNRESOLVED ADD-03:8.2: Form 4-H shall be completed in the Arabic language, signed and stamped by an authorised signatory of each member of the Bidder. The Arabic text governs. The Eng
- UNRESOLVED ADD-03:8.3: Form 4-H shall be submitted with Envelope A. A member of the Bidder that is incorporated outside the Kingdom may instead submit its Form 4-H through the Portal 
- UNRESOLVED ADD-03:Q17: No: 17 | Bidder question: Will the Authority publish the reference specific energy consumption against which criterion G of Table 1-1 will be assessed? | Author
- UNRESOLVED ADD-03:p4-image/decl1: أولاً: أن الأشخاص الطبيعيين المبينين في الجدول أدناه هم جميع المستفيدين الحقيقيين من العضو، والمستفيد الحقيقي هو كل شخص طبيعي يملك، بصورة مباشرة أو غير مباشرة، 
- UNRESOLVED ADD-03:p4-image/field-cr-en: Commercial registration number
- UNRESOLVED ADD-03:p4-image/field-cr-ar: رقم السجل التجاري :
- UNRESOLVED ADD-03:p4-image/field-signatory-en: Name of authorised signatory
- UNRESOLVED ADD-03:p4-image/field-signatory-ar: اسم المفوض بالتوقيع :
- UNRESOLVED ADD-03:p4-image/field-capacity-en: Capacity
- UNRESOLVED ADD-03:p4-image/field-capacity-ar: الصفة :
- UNRESOLVED ADD-03:p4-image/field-date-en: Date
- UNRESOLVED ADD-03:p4-image/field-date-ar: التاريخ :
- UNRESOLVED ADD-03:p4-image/field-signature-en: Signature and company seal
- UNRESOLVED ADD-03:p4-image/field-signature-ar: التوقيع والختم :
- UNRESOLVED ADD-03:p4-image/note: ملاحظة: يجب تقديم هذا النموذج باللغة العربية عن كل عضو من أعضاء الائتلاف، والنص العربي هو المعتمد. عدم تقديمه كاملاً يجعل العرض غير مستجيب.
- UNRESOLVED ADD-03:p4-image/image-footer: FICTIONAL DOCUMENT - Lamar Holding internal assessment pack - not a real tender.
- UNRESOLVED ADD-03:AppB/para1: This translation is provided for convenience only. The Arabic text of Form 4-H at Appendix A governs.
- cover summary vs provisions (C28, report only): 7 finding(s)
  - not found: 'amends the definition of Estimated Project Cost, the financial capacity requirement in Volume I Clause 8.4 and the delay liquidated damages in Volume V Clause 18.1, relaxes the velocity limit for the treated effluent transmission main': no provision of ADD-03 matches 'relaxes the velocity limit for the treated effluent transmission main'
  - not found: 'amends Section 5.1 of Addendum No. 1': no provision of ADD-03 does this
  - not found: 'reissues the technical evaluation table to add a criterion for energy efficiency, divides Volume I Clause 11.3 into two Clauses, makes a conditional amendment to Volume II Clause 1.4': no provision of ADD-03 matches 'makes a conditional amendment to Volume II Clause 1.4'
  - consequence not mentioned: ADD-03:8.4 states 'Failure to submit a complete and properly executed Form 4-H for each member of the Bidder by the time required by Section 8.3 shall render the Proposal non-responsive.'; the summary says only 'adds a Declaration of Beneficial Ownership (Form 4-H) which all Bidders may submit through the Portal within five Working Days after the Proposal Due Date'
  - omitted: ADD-03/2.1 amends VOL-V:1.3; the summary does not mention it: 'In Volume V Clause 1.3, ‘as set out in the agreed Financial Model at Financial Close’ is deleted and ‘as stated by the Bidder in Form 4-F, excluding financing costs, interest during construction and development fees’ is substituted.'
  - omitted: ADD-03/5.1 amends VOL-II:5.2; the summary does not mention it: 'In Volume II Clause 5.2, ‘2.0 m/s’ is deleted and ‘1.5 m/s’ is substituted. The minimum residual head of 15 m at the delivery point is unchanged.'
  - omitted: ADD-03/6.2(b) inserts new text after VOL-I:11.3; the summary does not mention it: 'Volume I Clause 11.3 is deleted and replaced by the following two Clauses: ‘11.3 A Proposal whose technical score is less than seventy per cent (70%) of the total marks available in Table 1-1 shall not proceed to commercial evaluation.’ ‘1…'

### Requirements

- new: 0; out of force: 0; changed: 8

- CHANGED VOL-I-11.2-01: wording (by ADD-03/S6/para1(b))
- CHANGED VOL-I-11.3-01: wording (by ADD-03/6.2(a))
- CHANGED VOL-I-8.4-01: wording (by ADD-03/3.1)
- CHANGED VOL-I-8.4-02: wording (by ADD-03/3.1)
- CHANGED VOL-II-5.2-01: wording (by ADD-03/5.1)
- CHANGED VOL-II-5.2-02: wording (by ADD-03/5.1)
- CHANGED VOL-IV-F4D-01: secondary units VOL-IV:F4-D/guarantor-ultimate-parent-of-epc-contractor, VOL-IV:F4-D/jurisdiction-of-incorporation, VOL-IV:F4-D/epc-contractor-guaranteed, VOL-IV:F4-D/guaranteed-obligations, VOL-IV:F4-D/limit-of-liability, VOL-IV:F4-D/expiry, VOL-IV:F4-D/governing-law, VOL-IV:F4-D/signature, VOL-IV:F4-D/name-and-capacity, VOL-IV:F4-D/date, VOL-IV:F4-D/corporate-authority-reference annotated by ADD-03/Q15 (by ADD-03/Q15)
- CHANGED VOL-IV-F4F-01: secondary units VOL-IV:F4-F/bidder, VOL-IV:F4-F/availability-payment-sar-per-annum-year-1-of-operations, VOL-IV:F4-F/availability-payment-in-words, VOL-IV:F4-F/estimated-project-cost-sar, VOL-IV:F4-F/assumed-senior-debt-tenor-years-from-financial-close, VOL-IV:F4-F/assumed-senior-debt-margin-bps, VOL-IV:F4-F/assumed-gearing-debt-equity, VOL-IV:F4-F/project-irr-nominal-post-tax, VOL-IV:F4-F/equity-irr-nominal-post-tax, VOL-IV:F4-F/indexation-basis-assumed, VOL-IV:F4-F/model-auditor, VOL-IV:F4-F/date-of-model-audit-opinion, VOL-IV:F4-F/signature, VOL-IV:F4-F/name-and-capacity, VOL-IV:F4-F/date annotated by ADD-03/Q16 (by ADD-03/Q16)

### Stale readings and decisions

- STALE VOL-I-11.2-01: VOL-I:11.2 changed since ADD-02 (by ADD-03/S6/para1(b)); quote not found in the effective text at ADD-03: 'sixty-five per cent (65%) technical and thirty-five per cent' (expected: the interpretation predates the change)
- STALE VOL-I-11.3-01: VOL-I:11.3 changed since ADD-02 (by ADD-03/6.2(a)); quote not found in the effective text at ADD-03: 'scoring less than seventy (70) marks out of one hundred (100' (expected: the interpretation predates the change); cons
- STALE VOL-I-6.2-01: new dependency ADD-03:Q19; VOL-I:6.2 changed since BASE (by ADD-03/Q19)
- STALE VOL-I-6.2-02: new dependency ADD-03:Q19; VOL-I:6.2 changed since BASE (by ADD-03/Q19)
- STALE VOL-I-8.4-01: new dependency ADD-03:Q19; VOL-I:8.4 changed since BASE (by ADD-03/3.1, ADD-03/Q19); quote not found in the effective text at ADD-03: '(a) a consolidated tangible net worth of not less than SAR 8' (expected: the interpre
- STALE VOL-I-8.4-02: new dependency ADD-03:Q19; VOL-I:8.4 changed since BASE (by ADD-03/3.1, ADD-03/Q19)
- STALE VOL-I-8.7-01: new dependency ADD-03:Q15; VOL-I:8.7 changed since ADD-02 (by ADD-03/Q15)
- STALE VOL-II-1.4-01: new dependency ADD-03:Q16; VOL-II:1.4 changed since BASE (by ADD-03/Q16)
- STALE VOL-II-5.2-01: new dependency ADD-03:Q18; VOL-II:5.2 changed since BASE (by ADD-03/5.1, ADD-03/Q18); quote not found in the effective text at ADD-03: 'The main shall be sized for the peak hourly flow in Table 2-' (expected: the interpr
- STALE VOL-II-5.2-02: new dependency ADD-03:Q18; VOL-II:5.2 changed since BASE (by ADD-03/5.1, ADD-03/Q18)
- STALE VOL-II-5.4-01: new dependency ADD-03:Q18; VOL-II:5.4 changed since BASE (by ADD-03/Q18)
- STALE VOL-II-5.4-02: new dependency ADD-03:Q18; VOL-II:5.4 changed since BASE (by ADD-03/Q18)
- STALE VOL-IV-F4D-01: new dependency ADD-03:Q15; new dependency VOL-IV:F4-D/T1; new dependency VOL-IV:F4-D/T2; VOL-IV:F4-D/corporate-authority-reference changed since BASE (by ADD-03/Q15); VOL-IV:F4-D/date changed since BASE (by ADD-03/Q15); 
- STALE VOL-IV-F4D-02: new dependency ADD-03:Q15; new dependency VOL-IV:F4-D/T1; VOL-IV:F4-D/guaranteed-obligations changed since BASE (by ADD-03/Q15)
- STALE VOL-IV-F4D-03: new dependency ADD-03:Q15; new dependency VOL-IV:F4-D/T1; VOL-IV:F4-D/limit-of-liability changed since BASE (by ADD-03/Q15)
- STALE VOL-IV-F4D-04: new dependency ADD-03:Q15; new dependency VOL-IV:F4-D/T1; VOL-IV:F4-D/expiry changed since BASE (by ADD-03/Q15)
- STALE VOL-IV-F4D-05: new dependency ADD-03:Q15; new dependency VOL-IV:F4-D/T1; VOL-IV:F4-D/governing-law changed since BASE (by ADD-03/Q15)
- STALE VOL-IV-F4D-06: new dependency ADD-03:Q15; VOL-IV:F4-D/item1 changed since BASE (by ADD-03/Q15)
- STALE VOL-IV-F4D-07: new dependency ADD-03:Q15; VOL-IV:F4-D/item2 changed since BASE (by ADD-03/Q15)
- STALE VOL-IV-F4D-08: new dependency ADD-03:Q15; VOL-IV:F4-D/item3 changed since BASE (by ADD-03/Q15)
- STALE VOL-IV-F4F-01: new dependency ADD-03:Q16; new dependency VOL-IV:F4-F/T1; new dependency VOL-IV:F4-F/T2; VOL-IV:F4-F/assumed-gearing-debt-equity changed since BASE (by ADD-03/Q16); VOL-IV:F4-F/assumed-senior-debt-margin-bps changed sinc
- STALE VOL-IV-F4F-02: new dependency ADD-03:Q16; VOL-IV:F4-F/para1 changed since BASE (by ADD-03/Q16)
- STALE VOL-V-12.1-01: VOL-V:18.1 changed since BASE (by ADD-03/4.1); consequence quote not found in VOL-V:18.1 at ADD-03 (expected: the interpretation predates the change)

### Obligations not reaching the outputs (C46)

- ADD-03/4.1 [A1]: ADD-03/4.1 (replace_text) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'In Volume V Clause 18.1, ‘SAR 180,000 for each day of delay’ is deleted and ‘one-twentieth of one per cent (0.05%) of the Estimated Project 
- ADD-03/6.2(b) [A1]: ADD-03/6.2(b) (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-I:11.3; a row of the anchor VOL-I:11.3 does not count): 'Volume I Clause 11.3 is deleted and replaced by the fo
- ADD-03/6.2(b) [A3]: ADD-03/6.2(b) brings in consequence words ['not proceed'] that no row's consequence carries at ADD-03: 'Volume I Clause 11.3 is deleted and replaced by the following two Clauses: ‘11.3  A Proposal whose technical score is less than seventy 
- ADD-03/8.1 [A1]: ADD-03/8.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-I:9.1; a row of the anchor VOL-I:9.1 does not count): 'A new Form 4-H (Declaration of Beneficial Ownership) is add
- ADD-03/8.1 [A1]: ADD-03/8.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the new ADD-03:F4-H; a row of the anchor VOL-I:9.1 does not count): 'A new Form 4-H (Declaration of Beneficial Ownership) is added to Volume I
- ADD-03/8.1 [A3]: ADD-03/8.1 brings in consequence words ['non-responsive'] that no row's consequence carries at ADD-03: 'A new Form 4-H (Declaration of Beneficial Ownership) is added to Volume IV and to the list at Volume I Clause 9.1, to be inserted after 
- ADD-03/8.4 [A1]: ADD-03/8.4 (annotate) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Failure to submit a complete and properly executed Form 4-H for each member of the Bidder by the time required by Section 8.3 shall render the P
- ADD-03/8.4 [A3]: ADD-03/8.4 brings in consequence words ['non-responsive'] that no row's consequence carries at ADD-03: 'Failure to submit a complete and properly executed Form 4-H for each member of the Bidder by the time required by Section 8.3 shall rend

### Reached through relationships (indirect: for review, not direct citations)

Curated links (relationships file) followed from what changed. The requirements above cite a changed unit; these are reached through another provision, in three classes that are never merged. A5 marks the activities that serve them REVIEW with their dates unchanged.

#### Confirmed dependency (0)
- none

#### Proposed relationship (0)
- none

#### Possible impact (10)
- VOL-I-8.10-01 (row; ACTIVE) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-DEBARMENT [member_scope; link possible]
- VOL-I-8.2-01 (row; ACTIVE) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-MULTIPLE-PARTICIPATION [member_scope; link possible]
- VOL-I-8.4-01 (row; AMENDED (ADD-03/3.1)) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-FIN-STANDING [member_scope; link possible]; also changed directly
- VOL-I-8.4-02 (row; AMENDED (ADD-03/3.1)) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-FIN-STANDING [member_scope; link possible]; also changed directly
- VOL-I-8.9-01 (row; ACTIVE) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-INVESTMENT-LICENCE [member_scope; link possible]
- VOL-I-9.4-01 (row; ACTIVE) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-FORM-4C [member_scope; link possible]
- VOL-IV-F4C-02 (row; ACTIVE) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-MULTIPLE-PARTICIPATION [member_scope; link possible]
- VOL-IV-F4C-03 (row; ACTIVE) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-DEBARMENT [member_scope; link possible]
- VOL-IV-F4C-N1 (row; ACTIVE) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-FORM-4C [member_scope; link possible]
- calc:financial-standing (calculation) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-FIN-STANDING [member_scope; link possible]

#### Referenced but not supplied: conclusions in play that cannot be established (0)
- none

### Disqualifiers (A3)

- no change

### Programme impact (status date 2026-10-22 -> 2026-11-09)

- REWORK assemble-envelope-a: requirement changed: VOL-I-6.2-01
- REWORK assemble-envelope-b: requirement changed: VOL-I-6.2-01
- REWORK copies: requirement changed: VOL-I-6.2-01
- REWORK deliver: requirement changed: VOL-I-6.2-01
- REWORK fin-model-build: requirement changed: VOL-IV-F4F-02
- REWORK fin-model-freeze: requirement changed: VOL-IV-F4F-02
- REWORK fin-standing: requirement changed: VOL-I-8.4-01, VOL-I-8.4-02
- REWORK fin-statements: requirement changed: VOL-I-8.4-01, VOL-I-8.4-02
- REWORK form-4f: requirement changed: VOL-IV-F4F-01, VOL-IV-F4F-02
- REWORK pcg-execution: requirement changed: VOL-I-8.7-01, VOL-IV-F4D-01, VOL-IV-F4D-02, VOL-IV-F4D-03, VOL-IV-F4D-04, VOL-IV-F4D-05, VOL-IV-F4D-06, VOL-IV-F4D-07, VOL-IV-F4D-08
- REWORK pcg-wording: requirement changed: VOL-I-8.7-01, VOL-IV-F4D-01, VOL-IV-F4D-02, VOL-IV-F4D-03, VOL-IV-F4D-04, VOL-IV-F4D-05, VOL-IV-F4D-06, VOL-IV-F4D-07, VOL-IV-F4D-08
- REWORK seal-and-mark: requirement changed: VOL-I-6.2-01
- REWORK technical-proposal: requirement changed: VOL-I-11.3-01, VOL-II-1.4-01, VOL-II-5.2-01, VOL-II-5.2-02, VOL-II-5.4-01, VOL-II-5.4-02
- REVIEW (possible impact) fin-standing: VOL-I-8.4-01, VOL-I-8.4-02 reached from words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-FIN-STANDING; dates unchanged
- REVIEW (possible impact) fin-statements: VOL-I-8.4-01, VOL-I-8.4-02 reached from words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-FIN-STANDING; dates unchanged
- REVIEW (possible impact) form-4c-prep: VOL-I-8.10-01, VOL-I-8.2-01, VOL-I-9.4-01, VOL-IV-F4C-02, VOL-IV-F4C-03, VOL-IV-F4C-N1 reached from words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-DEBARMENT, REL-MEMBER-FORM-4C, REL-MEMBER-MULTIPLE-PARTICIPATION; dates unchanged
- REVIEW (possible impact) form-4c-sign: VOL-I-8.10-01, VOL-I-8.2-01, VOL-I-9.4-01, VOL-IV-F4C-02, VOL-IV-F4C-03, VOL-IV-F4C-N1 reached from words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-DEBARMENT, REL-MEMBER-FORM-4C, REL-MEMBER-MULTIPLE-PARTICIPATION; dates unchanged
- REVIEW (possible impact) investment-licence: VOL-I-8.9-01 reached from words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-INVESTMENT-LICENCE; dates unchanged
- FEASIBILITY lcc-ratio: INFEASIBLE by 12 WD -> INFEASIBLE by 24 WD
- FEASIBILITY lcc-certificate: INFEASIBLE by 12 WD -> INFEASIBLE by 24 WD
- FEASIBILITY fin-model-build: OK -> INFEASIBLE by 10 WD
- FEASIBILITY model-auditor-appoint: OK -> INFEASIBLE by 9 WD
- FEASIBILITY pcg-wording: OK -> INFEASIBLE by 9 WD
- FEASIBILITY technical-proposal: OK -> INFEASIBLE by 9 WD
- FEASIBILITY ground-dd: OK -> INFEASIBLE by 5 WD
- FEASIBILITY lender-terms: OK -> INFEASIBLE by 5 WD
- FEASIBILITY completion-certs: OK -> INFEASIBLE by 4 WD
- FEASIBILITY model-audit-review: OK -> INFEASIBLE by 9 WD
- FEASIBILITY poa-resolutions: OK -> INFEASIBLE by 4 WD
- FEASIBILITY references: OK -> INFEASIBLE by 3 WD
- FEASIBILITY bond-approval: OK -> INFEASIBLE by 2 WD
- FEASIBILITY deviations-review: OK -> INFEASIBLE by 1 WD
- FEASIBILITY pcg-execution: OK -> INFEASIBLE by 9 WD
- FEASIBILITY poa: OK -> INFEASIBLE by 4 WD
- FEASIBILITY fin-model-freeze: OK -> INFEASIBLE by 10 WD
- FEASIBILITY investment-licence: OK -> INFEASIBLE by 4 WD
- FEASIBILITY model-audit-opinion: OK -> INFEASIBLE by 10 WD
- FEASIBILITY form-4b-prep: OK -> INFEASIBLE by 3 WD
- FEASIBILITY bond-issue: OK -> INFEASIBLE by 2 WD
- FEASIBILITY form-4c-sign: OK -> INFEASIBLE by 2 WD
- FEASIBILITY fin-assumptions: OK -> INFEASIBLE by 7 WD
- FEASIBILITY form-4e: OK -> INFEASIBLE by 1 WD
- FEASIBILITY form-4f: OK -> INFEASIBLE by 7 WD
- FEASIBILITY form-4b: OK -> INFEASIBLE by 3 WD
- FEASIBILITY assemble-envelope-a: INFEASIBLE by 12 WD -> INFEASIBLE by 24 WD
- FEASIBILITY assemble-envelope-b: OK -> INFEASIBLE by 10 WD
- FEASIBILITY copies: INFEASIBLE by 12 WD -> INFEASIBLE by 24 WD
- FEASIBILITY seal-and-mark: INFEASIBLE by 12 WD -> INFEASIBLE by 24 WD
- FEASIBILITY deliver: INFEASIBLE by 12 WD -> INFEASIBLE by 24 WD

## Next (a person)

- read the unresolved and escalated provisions first, then each item against its evidence (`../ai/ADD-03-run-host-blind04-20261004T152505Z-combined/proposals.yaml`, `../downstream/proposals.yaml`)
- nothing here is applied to the real curation: to take an item over, add the PDF to the pack (OPERATING_GUIDE §3 steps 1-2) and copy the reviewed files listed in `promotion.json`; then `pin`, `check-register`, `outputs` and decide with `accept` / `reject` as usual
