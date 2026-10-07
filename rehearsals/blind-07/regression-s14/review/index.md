# Review packet: ADD-03, AI workflow run ADD-03-run-host-20261007T161946Z-e884

> **CANDIDATE: proposed by the AI workflow; not reviewed; nothing accepted.** Statuses are the controller's; a person decides every item. The real `curation/`, `config/` and `out/` were only read: everything below lives in this run's folder.

- PDF: `/tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s14/pkg/reg07b/unzipped/LAMAR-PPP-R2-INTERVIEW_a918d5e+wt_20261007T1619Z/staging/panel/uploads/06afe32fcaa678eeb991fbfe0c556f35443ab4b42a24f9dd91bb09e9fd2dbc8d.pdf` (sha256 06afe32fcaa678ee…, 4 pages); preceding state: pack `/tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s14/pkg/reg07b/unzipped/LAMAR-PPP-R2-INTERVIEW_a918d5e+wt_20261007T1619Z/config/pack.yaml` (NUPA-ISTP-2026-014), previous evidence build `/tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s14/pkg/reg07b/unzipped/LAMAR-PPP-R2-INTERVIEW_a918d5e+wt_20261007T1619Z/build`
- route **host**; model requested `claude-code headless (claude-opus-5-5)`, reported `None`; host sessions report: claude-opus-5-5
- status **partial**: 9 provision(s) unresolved in the candidate (listed first in the review packet); 15 downstream task(s) answered only by items that cannot be promoted: row:VOL-II-8.5-01, row:VOL-II-8.5-02, row:VOL-V-36.2-01, c46:ADD-03/2.2, c46:ADD-03/3.1, clar:CQ-HANDBACK-CONDITION, esc:ADD-03:p3-image/r4, esc:ADD-03:p3-image/r5 …; check-register on the candidate: exit 1, 2 finding(s) {'C46': 2} (0 missing because the downstream phase did not propose them, 2 defect(s)); C46: [C46] ADD-03/2.2: [A1] ADD-03/2.2 (annotate) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Bidders shall take Section 2.1 into acco…; [C46] ADD-03/3.1: [A1] ADD-03/3.1 (relocate_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Volume II Clause 8.5 is relocated t…
- usage (application routes): none: the run's route is host, every exchange ran in a host session (below)
- host sessions: 24 (their own records); usage of the 24 that reported it: input 202, cache write 1155973, cache read 4589675 / output 510058 tokens
- code at start: content 64dbc541896c4ac1… over 99 files; git not available; recorded 2026-10-07T16:19:47Z

## Execution, completeness and approval (three separate things)

- **Execution** (what ran): ingest done, readings done, analysis done, validation done, downstream done, downstream_validation done, critic done, promotion done, pin done, check_register done, outputs done, diff done, review running; batches reading: {'done': 1}; analysis: {'done': 6}; downstream: {'done': 4}
- **Completeness** (what the run completed): **partial**: 9 provision(s) unresolved in the candidate (listed first in the review packet); 15 downstream task(s) answered only by items that cannot be promoted: row:VOL-II-8.5-01, row:VOL-II-8.5-02, row:VOL-V-36.2-01, c46:ADD-03/2.2, c46:ADD-03/3.1, clar:CQ-HANDBACK-CONDITION, esc:ADD-03:p3-image/r4, esc:ADD-03:p3-image/r5 …; check-register on the candidate: exit 1, 2 finding(s) {'C46': 2} (0 missing because the downstream phase did not propose them, 2 defect(s)); C46: [C46] ADD-03/2.2: [A1] ADD-03/2.2 (annotate) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Bidders shall take Section 2.1 into acco…; [C46] ADD-03/3.1: [A1] ADD-03/3.1 (relocate_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Volume II Clause 8.5 is relocated t…
  - downstream tasks: 44; answered 29; unanswered 0; answered only by items that cannot be promoted 15; answered 'no change' 3
- **Human approval**: **none** (nothing approved, accepted, rejected or sent); no decision is recorded in the candidate's decisions file

## What is candidate and what is real

- **Candidate** (proposed by this run, nothing accepted): `../candidate/` — a copy of the curation and configuration with ADD-03 added, its evidence build, its op file, rows, issues, templates and outputs.
- **Last validated state**: `../candidate/out-before/` (the pre-addendum outputs built from the copied curation and the previous evidence build; done)
- **Real** (untouched): `curation/`, `config/`, `out/`; the owner's approvals and readings were copied unchanged and used read-only.

- real inputs changed since the run started: none

## Candidate outputs

Exit 0 (WORKING DRAFT (not releasable)); every file carries the banner (`../candidate/out/CANDIDATE.md`); A1 has a candidate status column {'proposed (existing row; not changed by this run; not reviewed)': 196, 'PROPOSED BY THE AI WORKFLOW': 14, 'UNRESOLVED (value in question)': 2, 'UNRESOLVED': 1}.

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

- before → after: {"a1": {"rows_before": 205, "rows_after": 213, "new": 8, "gone": 0}, "a3": {"before": 17, "after": 17, "enters": 0, "leaves": 0}, "a5": {"activities_before": 44, "activities_after": 45, "new": 1, "gone": 0}}

- ADD-03 is **PARTIAL** in the candidate (provisions unresolved): A3 and the A5 programme show the validated state (ADD-02); ADD-03 as proposed is in A1's `Status after ADD-03` column, in A2, in the candidate A3 and A5 below, in `a5/working/ADD-03.json` and in the diff below.

### Validated and candidate A3 / A5 (partial should not mean useless)

- **Validated** (unchanged; ADD-02): [a3/a3.pdf](../candidate/out/a3/a3.pdf) (one page), [a5/README.md](../candidate/out/a5/README.md), [a5/gantt.html](../candidate/out/a5/gantt.html)
- **Candidate** (CANDIDATE — NOT VALIDATED; ADD-03 as proposed): [a3/a3_candidate.pdf](../candidate/out/a3/a3_candidate.pdf) (8 page(s)), [a3/a3_candidate.md](../candidate/out/a3/a3_candidate.md), [a5/candidate/README.md](../candidate/out/a5/candidate/README.md), [a5/candidate/gantt.html](../candidate/out/a5/candidate/gantt.html)

**What may be changing.** ADD-03 is PARTIAL: 8 of 57 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 15 op(s) that are valid there stood (each still a proposal: review proposed 15), A3 would gain 0 row(s) (none), lose 0 (none) and change 0 (none); A5, replanned at ADD-03's issue date (2026-11-17), would move the latest dates of 0 activities (none), add 1 (core-inspection-request) and remove 0 (none), and marks 7 REVIEW through relationships. Not settled: 4 activities blocked by an unresolved row (technical-proposal, core-inspection-request, deviations-review, form-4e), 1 STALE row(s), 2 obligation(s) reaching no output (C46), 0 relationship chain(s) blocked or incomplete, 5 conflict(s); documents not supplied: the Environmental Permit issued for the site, Geotechnical Baseline Report (Revision C), Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions) and 7 more; conditional or effective-dated: ADD-03:T42-1/4 (conditional obligation); ADD-03:T42-1/5 (conditional obligation); ADD-03:T42-1/note(4) (conditional obligation). Clarification route: the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person. Nothing here is validated, accepted or applied to the real state.


- blockers: 8 unresolved provision(s), 4 blocked activit(y/ies), 1 STALE row(s), 2 C46 gap(s), 0 relationship chain(s) blocked or incomplete, 5 conflict(s); documents not supplied: the Environmental Permit issued for the site, Geotechnical Baseline Report (Revision C), Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT, I-VOL-III, I-VOL-II-MISSING, I-VOL-V-MISSING, I-VOL-II-COMPLIANCE-POINT, I-VOL-IV-SCALE, I-OP-ADD-01/Q4
- conditional scenarios: 3; ADD-03:T42-1/4 (conditional obligation); ADD-03:T42-1/5 (conditional obligation); ADD-03:T42-1/note(4) (conditional obligation)

**Image-read units** (the review packet of each region shows every crop beside its reading; translations are proposals, not evidence):

- ADD-03-p3-r1 (ADD-03 p3; reading pending): [packet](../candidate/build/review/ADD-03-p3-r1/packet.html); 20 unit(s) touched
  - `ADD-03:p3-image`: “جدول ٤٢-١: الحد الأدنى للعمر المتبقي للأصول عند النقل يجب ألا يقل العمر المتبقي لكل فئة من فئات الأصول في تاريخ نقل المرفق إلى الهيئة عمّا هو مبيِّن أدناه:”; issues I-ADD03-T42-1-MEMBRANE-UNIT, I-ADD03-T42-1-RENDERINGS
  - `ADD-03:p3-image/r1`: “م: ١ / فئة الأصول: المنشآت المدنية والخرسانية / الحد الأدنى للعمر المتبقي (سنة): ٢٠ / أقصى درجة للحالة: ٢”; issues I-ADD03-T42-1-MEMBRANE-UNIT, I-ADD03-T42-1-RENDERINGS
  - `ADD-03:p3-image/r2`: “م: ٢ / فئة الأصول: خط نقل المياه المعالجة / الحد الأدنى للعمر المتبقي (سنة): ٢٠ / أقصى درجة للحالة: ٢”; issues I-ADD03-T42-1-MEMBRANE-UNIT, I-ADD03-T42-1-RENDERINGS
  - `ADD-03:p3-image/r3`: “م: ٣ / فئة الأصول: المعدات الميكانيكية / الحد الأدنى للعمر المتبقي (سنة): ٥ / أقصى درجة للحالة: ٣”; issues I-ADD03-T42-1-MEMBRANE-UNIT, I-ADD03-T42-1-RENDERINGS
  - `ADD-03:p3-image/r4`: “م: ٤ / فئة الأصول: المعدات الكهربائية وأجهزة القياس والتحكم / الحد الأدنى للعمر المتبقي (سنة): ٧ / أقصى درجة للحالة: ٣”; issues I-ADD03-T42-1-MEMBRANE-UNIT, I-ADD03-T42-1-RENDERINGS
  - `ADD-03:p3-image/r5`: “م: ٥ / فئة الأصول: الأغشية (إن وُجدت) / الحد الأدنى للعمر المتبقي (سنة): ٢٤ شهراً / أقصى درجة للحالة: ٣”; uncertain: the cell prints '٢٤ شهراً' (24 months) while the column heading states the unit as (سنة) (year); recorded as printed; how the unit applies is for a person; issues I-ADD03-T42-1-MEMBRANE-UNIT, I-ADD03-T42-1-RENDERINGS
  - `ADD-03:p3-image/hdr-en`: “Northern Utilities Procurement Authority - Asset Transfer Committee”
  - `ADD-03:p3-image/hdr-ar`: “الهيئة الشمالية للمشتريات المرفقية”; translation (apart): ‘Northern Utilities Procurement Authority’
  - `ADD-03:p3-image/committee-ar`: “لجنة نقل الأصول”; translation (apart): ‘Asset Transfer Committee’
  - `ADD-03:p3-image/date-ar`: “التاريخ: ١٥ نوفمبر ٢٠٢٦م”; translation (apart): ‘Date: 15 November 2026 AD’
  - `ADD-03:p3-image/ref-ar`: “الرقم: ٤١٧/٢٠٢٦”; translation (apart): ‘No.: 417/2026’
  - `ADD-03:p3-image/subject`: “الموضوع: متطلبات حالة الأصول عند نقل محطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان”; translation (apart): ‘Subject: Asset condition requirements on transfer of the Wadi Al-Sirhan Independent Sewage Treatment Plant’
  - … 8 more in `a3/a3_candidate.md`
- VOL-II-p3-r1 (VOL-II p3; reading approved): [packet](../candidate/build/review/VOL-II-p3-r1/packet.html); not touched by this addendum
- VOL-IV-p6-r1 (VOL-IV p6; reading approved): [packet](../candidate/build/review/VOL-IV-p6-r1/packet.html); not touched by this addendum

## Timings (wall clock per step)

| Step | Seconds | Status |
|---|---|---|
| ingest | 23.6 | done |
| readings | 243.7 | done |
| analysis | 1724.6 | done |
| validation | 10.5 | done |
| downstream | 1210.8 | done |
| downstream_validation | 2.1 | done |
| critic | 118.8 | done |
| promotion | 25.3 | done |
| pin | 2.5 | done |
| check_register | 7.3 | done |
| outputs | 34.9 | done |
| diff | 7.0 | done |
| review | 0.0 | running |
| **total** | **3411.1** (56.9 min) | target 30 min from the PDF to candidate outputs and this packet, human review excluded |

## Readings of the addendum's image regions (AI-proposed, PENDING HUMAN REVIEW)

Ingest first refused the candidate because these image regions had no reading (C05): ADD-03-p3-r1. Each reading below was proposed by the route of this run, checked by readings.check_reading and written into the candidate's readings; it is an interpretation of an image, never approved, and every unit made from it carries `reading.status: pending`.

- **ADD-03-p3-r1** — done; controller status **interpretation_pending**; unit `ADD-03:p3-image`; file `../candidate/curation/readings/ADD-03-p3-r1.yaml`
  - the reading beside its crops (the build's review packet): [../candidate/build/review/ADD-03-p3-r1/packet.html](../candidate/build/review/ADD-03-p3-r1/packet.html)
  - table reading, languages ['ar', 'en']; prepared by: AI-assisted: headless host session ADD-03-hostsession-20261007T162011Z-1c3f (claude-code headless (claude-opus-5-5); the CLI reported claude-opus-5-5), in AI workflow run ADD-03-run-host-20261007T161946Z-e884 (reading-ADD-03-p3-r1), 2026-10-07T16:23:55Z; proposed for a person's review, not approved
  - uncertainty: Band 17 right half (x 630-891) is an empty oval seal outline with no text; it is recorded as a line with an empty source so that the band is accounted for, not as text.
  - uncertainty: Diacritics were read at native resolution; at reduced zoom they are unreliable.
  - uncertainty: Table 42-1 is a requirement table reproduced from an Asset Transfer Committee letter; this reading says only what the image shows. How the requirements are used (Note 3 replacement at the Project Company's expense; the months-vs-years unit…

## First: unresolved provisions and escalations

9 of 57 provisions are not applied or settled by a promoted item (each is `unresolved` in the candidate op file with the reason); 1 escalation(s).
- states (session 14: kept distinct): applied 13, no effect 35, partly applied 1, unresolved but accounted for 8, unaccounted 0; approved by a person: none (only a person's recorded decision approves; see Human approval above)

- **Clarification route:** the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person (ADD-03 issued 2026-11-17; the cut-off is computed from VOL-I-5.2-01 at that stage). No question about it is suggested as sendable; a proposed entry stays a DRAFT, not sent.

- **ESCALATED ADD-03/3.4(b)** (ADD-03:3.4): software limitation: 'Table 42-1 is reproduced at Appendix A to this Addendum and forms part of Volume V.' Appendix A is the Arabic image table ADD-03:p3-image (title 'جدول ٤٢-١: الحد الأدنى للعمر المتبقي للأصول عند النقل'). insert_table {new_group: ADD-03:p3-image, into: VOL-V, number: 42-1} was r…
  - unsupported: insert_table of a table read from an image whose number is printed in Arabic-Indic digits (ADD-03:p3-image as Volume V Table 42-1); Document control to record the insertion by hand, the reading staying pending approval.
  - evidence: ADD-03:3.4 p1: “Table 42-1 is reproduced at Appendix A to this Addendum and forms part of Volume V.”; ADD-03:p3-image p3: “جدول ٤٢-١: الحد الأدنى للعمر المتبقي للأصول عند النقل”; ADD-03:AppA/para1 p3: “The Arabic text governs in accordance with Section 3.5 of this Addendum.”
  - affected scope: units VOL-V:42.1; rows VOL-V-42.1-01, VOL-V-42.1-02; activities none; clarifications CQ-HANDBACK-CONDITION
- **UNRESOLVED ADD-03:3.6** (clause, p1): its obligation is proposed downstream as ADD-03-3.6-01 (row_new, interpretation_pending), DS-ADD03-3.6-issue (issue, interpretation_pending) (task(s) ana:ADD-03/row/3.6; PROPOSED): no op or disposition answers the provision; a person confirms the row and the provision's disposition — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:4.2** (clause, p2): its obligation is proposed downstream as ADD-03-4.2-01 (row_new, interpretation_pending) (task(s) ana:ADD-03/4.2/row; PROPOSED): no op or disposition answers the provision; a person confirms the row and the provision's disposition — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:4.3** (clause, p2): its obligation is proposed downstream as ADD-03-4.3-01 (row_new, interpretation_pending), DS-ADD03-4.3-ev (evidence_item, evidence_verified), DS-ADD03-4.3-act (activity, interpretation_pending) (task(s) ana:ADD-03/4.3/row; PROPOSED): no op or disposition answers the provision; a person confirms the row and the provision's disposition — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:p3-image/r4** (table_row, p3): unresolved (accounted for by the promoted `unresolved` disposition ADD-03/p3-image/r4; nothing applied): ambiguous: the Arabic row 4 prints 'الحد الأدنى للعمر المتبقي (سنة): ٧' (seven years) for 'المعدات الكهربائية وأجهزة القياس والتحكم', while the Appendix B translation row ADD-03:T42-1/4 prints 'Minimum residual life (years): 5'. Reading A: 7 years, under ADD-03:3.5 'The Arabic text governs.' Reading B: 5 years, as the translation states, with the Arabic being an error. Applying the precedence and… — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:p3-image/r5** (table_row, p3): unresolved (accounted for by the promoted `unresolved` disposition ADD-03/p3-image/r5; nothing applied): ambiguous: the Arabic row 5 cell prints '٢٤ شهراً' (24 months) under the column heading 'الحد الأدنى للعمر المتبقي (سنة)' (years), while the Appendix B translation row ADD-03:T42-1/5 prints 'Minimum residual life (years): 24'. Reading A: 24 months, as the governing Arabic cell states in words. Reading B: 24 years, from the column's unit and the translation. Reading C: the cell's own unit override… — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:T42-1/4** (table_row, p4): not promotable: D-T42-1-4 conflicting (declared_conflicts: the proposer declares: ADD-03:p3-image/r4); ISS-T42-row4 interpretation_pending (dropped: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-T42-1-4-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:T42-1/5** (table_row, p4): not promotable: D-T42-1-5 conflicting (declared_conflicts: the proposer declares: ADD-03:p3-image/r5); ISS-T42-row5 interpretation_pending (dropped: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-T42-1-5-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task); Q-T42-row5 interpretation_pending (dropped: an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; the downstream phase proposes issues and clarification entries against the candidate) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:T42-1/note(4)** (note, p4): not promotable: D-T42-1-note4 conflicting (declared_conflicts: the proposer declares: ADD-03:p3-image); ISS-T42-note4 interpretation_pending (dropped: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-T42-1-NOTE-4-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person

## Earlier answers to re-read against the new text (never revoked; a person decides)

- `ADD-03:Q17` (ADD-03): cites VOL-I:10.6, changed by ADD-03/Q17(b); to be re-read against the new text of VOL-I:10.6 (ADD-03/Q17(b)); a person decides whether the answer still holds

## Derived effects (session 12: pending readings, computed deadlines, conditions, consequences)

## Computed deadlines and the Working Days left (PROPOSED; nothing typed)

- Working Days left from the issue date (2026-11-17) to the PDD (2026-11-26): 7 (the issue date not counted, the PDD counted; Working Days per VOL-I 2.4 (weekend [4, 5] as date.weekday numbers; holidays none declared))
- `ADD-03:4.3` p2: “three (3) Working Days before the Proposal Due Date” -> **2026-11-23** (computed: calc deadline, anchor PDD = 2026-11-26, rule working-days-before, fingerprint 60b780e98a3a; PROPOSED, not validated)
- `ADD-03:4.3` p2: “within three (3) Working Days of the date of this Addendum” -> **AMBIGUOUS: 2026-11-22 (event_day_excluded); 2026-11-19 (event_day_counted)** (computed: calc deadline, anchor ADD-03-issue = 2026-11-17, rule none, fingerprint 4981e0314953; PROPOSED, not validated); ESCALATED: the counting rules do not settle it; not computed: no rule in the counting registry (config/formulas.yaml `counting`) for Working Days counted after a date (VOL-I 2.4 covers Working Days counted backwards): every reading is listed and a person decides
- `VOL-V:12.4+ADD-03` p2: “within five (5) Working Days of encountering them” -> **not computed: no rule in the counting registry (config/formulas.yaml `counting`) for Working Days counted after a date (VOL-I 2.4 covers Working Days counted backwards); its anchor 'encountering them' is an event, not a date the register holds** (computed: calc deadline, anchor encountering them = None, rule none, fingerprint ; PROPOSED, not validated); CONDITIONAL: “If the Project Company encounters at the site ground conditions that are materially more adverse than those described in the Geotechnical Baseline Report, it s…”

## Proposed from a pending reading (not in force; not planned)

- `ADD-03-T42-1-01` conditional on reading ADD-03-p3-r1 until approval: PENDING READING ADD-03-p3-r1. On the date the Facility is transferred to the Authority, the remaining life of each asset class must not be less than the minimu…

## Conditional impact investigations (CONDITIONAL; never accepted facts)

- `impact:ADD-03:p3-image/r4` conditional on disposition ADD-03:p3-image/r4 (unresolved: ambiguous: the Arabic row 4 prints 'الحد الأدنى للعمر المتبقي (سنة): ٧' (seven years) for 'المعدات الكهربائية وأجهزة القياس والتحكم', while the Appendix B translation row ADD-03:T42-1/4 prints 'Minim…): investigate the rows, activities and prices that rest on ADD-03:3.4, ADD-03:T42-1/4
- `impact:ADD-03:p3-image/r5` conditional on disposition ADD-03:p3-image/r5 (unresolved: ambiguous: the Arabic row 5 cell prints '٢٤ شهراً' (24 months) under the column heading 'الحد الأدنى للعمر المتبقي (سنة)' (years), while the Appendix B translation row ADD-03:T42-1/5 prints 'Minimum …): investigate the rows, activities and prices that rest on ADD-03:3.4, ADD-03:T42-1/5
- `impact:ADD-03:3.6` conditional on disposition ADD-03:3.6 (unresolved: its obligation is proposed downstream as ADD-03-3.6-01 (row_new, interpretation_pending), DS-ADD03-3.6-issue (issue, interpretation_pending) (task(s) ana:ADD-03/row/3.6; PROPOSED): no op or dispositi…): investigate the rows, activities and prices that rest on the provision ADD-03:3.6
- `impact:ADD-03:4.2` conditional on disposition ADD-03:4.2 (unresolved: its obligation is proposed downstream as ADD-03-4.2-01 (row_new, interpretation_pending) (task(s) ana:ADD-03/4.2/row; PROPOSED): no op or disposition answers the provision; a person confirms the row …): investigate the rows, activities and prices that rest on the provision ADD-03:4.2
- `impact:ADD-03:4.3` conditional on disposition ADD-03:4.3 (unresolved: its obligation is proposed downstream as ADD-03-4.3-01 (row_new, interpretation_pending), DS-ADD03-4.3-ev (evidence_item, evidence_verified), DS-ADD03-4.3-act (activity, interpretation_pending) (task…): investigate the rows, activities and prices that rest on the provision ADD-03:4.3
- `impact:ADD-03:T42-1/4` conditional on disposition ADD-03:T42-1/4 (unresolved: not promotable: D-T42-1-4 conflicting (declared_conflicts: the proposer declares: ADD-03:p3-image/r4); ISS-T42-row4 interpretation_pending (dropped: an analysis issue is not an op or a disposition: i…): investigate the rows, activities and prices that rest on the provision ADD-03:T42-1/4
- `impact:ADD-03:T42-1/5` conditional on disposition ADD-03:T42-1/5 (unresolved: not promotable: D-T42-1-5 conflicting (declared_conflicts: the proposer declares: ADD-03:p3-image/r5); ISS-T42-row5 interpretation_pending (dropped: an analysis issue is not an op or a disposition: i…): investigate the rows, activities and prices that rest on the provision ADD-03:T42-1/5
- `impact:ADD-03:T42-1/note(4)` conditional on disposition ADD-03:T42-1/note(4) (unresolved: not promotable: D-T42-1-note4 conflicting (declared_conflicts: the proposer declares: ADD-03:p3-image); ISS-T42-note4 interpretation_pending (dropped: an analysis issue is not an op or a disposition:…): investigate the rows, activities and prices that rest on VOL-II:2.2
- `impact:?` conditional on reading ? (pending_reading: the reading ? of ADD-03 is pending a person's approval: its values are not in force): investigate the rows, activities and prices that rest on ADD-03:region:ADD-03-p3-r1
- `impact:ADD-03-p3-r1` conditional on reading ADD-03-p3-r1 (pending_reading: the reading ADD-03-p3-r1 of ADD-03 is pending a person's approval: its values are not in force): investigate the rows, activities and prices that rest on ADD-03:p3-image, ADD-03:p3-image/r1, ADD-03:p3-image/r2, ADD-03:p3-image/r3, ADD-03:p3-image/r4, ADD-03:p3-image/r5, ADD-03:p3-image/hdr-en, ADD-03:p3-image/hdr-ar, ADD-03:p3-image/committee-ar, ADD-03:p3-image/date-ar, ADD-03:p3-image/ref-ar, ADD-03:p3-image/subject (+8)

## Computed amounts (PROPOSED; computed by the engine from the previous effective value, never typed)

- `ADD-03/2.1` (ADD-03:2.1, 'is reduced by SAR 1,000,000') on `VOL-V:36.2`: SAR 2,500,000 -> **SAR 1,500,000** — SAR 2,500,000 - SAR 1,000,000 = SAR 1,500,000 (the change 'is reduced by SAR 1,000,000', ADD-03:2.1; the previous value 'SAR 2,500,000' in VOL-V:36.2 as amended by ADD-02/8.1)

## Per provision: source evidence → proposed transition → validation → downstream impact → output difference

### ADD-03:cover/para1 (paragraph, p1) — no effect (PROPOSED; not approved)
- source: “Issued 17 November 2026”
- transition: `ADD-03:cover/para1/disp` disposition no_effect: Issue date line 'Issued 17 November 2026': records the addendum's date of issue and amends, obliges or excepts nothing.
  - validation: **evidence_verified**

### ADD-03:cover/para2 (paragraph, p1) — no effect (PROPOSED; not approved)
- source: “Tender NUPA/ISTP/2026/014”
- transition: `ADD-03:cover/para2/disp` disposition no_effect: Title line 'Tender NUPA/ISTP/2026/014' under the heading 'ADDENDUM NO. 3': identifies the tender and addendum; changes nothing.
  - validation: **evidence_verified**

### ADD-03:cover/para3 (paragraph, p1) — applied (PROPOSED; not approved)
- source: “This Addendum reduces the threshold in Volume V Clause 36.2 for compensation for a General Change in Law to SAR 4,000,000, relocates the handback condition survey from Volume II to Volume V, replaces the remaining design life required at handback with minimum residual service lives for four asset classes set out in Table 42-1 (issued in Arabic), invites Bid…”
- transition: `ADD-03/cover/para3` amendment_op annotate ADD-03:cover/para3 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The core reading holds up. The cover summarises, and its sentence 'Bidders shall acknowledge receipt in Form 4-A.' is the only one that sets a duty of its own, so annotating it as adds_obligation follows from the words.
    - concern: The rationale says the cover's 'SAR 4,000,000' conflicts with operative Section 2.1 and refers to a separate issue. That cannot be checked from the evidence shown. Section 2.1 (quoted only in S-F1) says the amount 'is reduced by SAR 1,000,000'. The cover says the threshold is reduced 'to SAR 4,000,…
    - concern: The rationale notes that the VOL-IV:F4-A group is superseded at ADD-02 and was reissued by ADD-01 Appendix A. So 'Form 4-A' in this cover may now mean the reissued form. The annotation names neither the reissued form nor its field 'Addenda acknowledged (numbers):' (ADD-01:AppA/addenda-acknowledged-…
    - concern: The other sentences in the cover are treated as summary handled elsewhere, but this cannot be confirmed from the evidence shown. They include 'takes precedence in accordance with Volume I Clause 3.2', 'All other terms of the RFP Documents remain unchanged', the invitation to address Table 42-1, and…
- transition: `ADD03-ACK` row_new {"row": {"id": "ADD03-ACK", "group": "Submission formalities", "scope": ["Bidder"], "requirement": "Bidders shall acknowledge receipt in Form 4-A.", "units": ["ADD-03:cover/para3"], "discipline": "Bi…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The requirement is quoted word for word from ADD-03:cover/para3. Recording the consequence as none_stated is correct, because the unit states no consequence.
    - concern: The rationale says VOL-I:9.3 is about signing Form 4-A. That unit is not printed here, so the claim cannot be checked. It does not affect the row, since no consequence is inferred from it.
    - concern: The row should name the reissued Form 4-A field ADD-01:AppA/addenda-acknowledged-numbers (VOL-IV:F4-A is superseded at ADD-02) as a dependent or evidence item. That is the form the bidder will actually fill in.
- transition: `ADD-03/cover/para3/issue` issue {"text": "ambiguous: the cover (ADD-03:cover/para3) says 'This Addendum reduces the threshold in Volume V Clause 36.2 for compensation for a General Change in Law to SAR 4,000,000', while operative S…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-12` row_new (c46:ADD-03/cover/para3): **interpretation_pending**
  - downstream proposal `DS-CIL-DEP` dependency (impact:Wadi Sirhan Independent Sewage Treatment Plant): **interpretation_pending**
  - downstream proposal `DS-CIL-ESC` escalation (impact:Wadi Sirhan Independent Sewage Treatment Plant): **escalated**
  - downstream proposal `DS-COVER-ROW` row_new (oblig:ADD-03/cover/para3): **interpretation_pending**
  - downstream proposal `DS-COVER-ISSUE` issue (oblig:ADD-03/cover/para3): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-COVER-DEP` dependency (oblig:ADD-03/cover/para3): **interpretation_pending**
  - output difference: NEW ADD-03-cover-para3-01; NEW ADD-03-cover-01; A5 REWORK form-4a; A5 REWORK form-4a-prep; A5 REVIEW (proposed relationship) form-4a-prep

### ADD-03:1.1 (clause, p1) — no effect (PROPOSED; not approved)
- source: “This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.”
- transition: `ADD-03:1.1/disp` disposition no_effect: Recital: 'This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.' It states t…
  - validation: **interpretation_pending — applied rule: ADD-03 1.1 provides: 'This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.' (applied, not decided); a person confirms the application**

### ADD-03:1.2 (clause, p1) — no effect (PROPOSED; not approved)
- source: “A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.”
- transition: `ADD-03:1.2/disp` disposition no_effect: Interpretation rule for the Addendum's own references: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by …
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'unless')

### ADD-03:1.3 (clause, p1) — no effect (PROPOSED; not approved)
- source: “Clarification requests 15 to 19 were received before the time stated in Volume I Clause 5.2.”
- transition: `ADD-03:1.3/disp` disposition no_effect: Recital of fact: 'Clarification requests 15 to 19 were received before the time stated in Volume I Clause 5.2.' It records timeliness and does not change VOL-I…
  - validation: **evidence_verified**

### ADD-03:2.1 (clause, p1) — applied (PROPOSED; not approved)
- source: “The amount stated in Volume V Clause 36.2 is reduced by SAR 1,000,000.”
- transition: `ADD-03/2.1` amendment_op adjust_value VOL-V:36.2
  - validation: **evidence_verified**
  - downstream: units changed VOL-V:36.2; rows citing them VOL-V-36.2-01
  - downstream proposal `DS-07` row_reading (row:VOL-V-36.2-01): **conflicting**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The parameter `threshold_sar: 1500000` and the quote 'exceeds SAR 1,500,000' record Reading 1 as the row's value. The proposer's own declared ambiguity (I-ADD03-CIL-THRESHOLD, S-36.2-WHICH) is still pending a person. The figure should be marked as provisional on that issue, or left unresolved, rath…
      - concern: S-36.2-WHICH's Reading 2 relies on a BASE figure of 'SAR 5,000,000'. That figure is not in any evidence printed here. Only the ADD-02 effective text (SAR 2,500,000) is shown, so Reading 2's basis cannot be checked.
      - concern: The cover says the threshold is reduced 'to SAR 4,000,000', but the ADD-02 effective figure is SAR 2,500,000. Measured against that text, 4,000,000 would be an increase, so the cover's wording is also inconsistent with its own word 'reduces'. Neither the item nor S-36.2-WHICH says this, and it is r…
      - concern: S-PAE-STALE says row VOL-V-36.2-01 still cites SAR 2,500,000. Its only evidence is ADD-03:3.4, which concerns a different clause and row (VOL-V-42.1-02). No evidence is shown for the claim about the 36.2 row.
      - concern: The consequence 'none_stated' fits VOL-V:36.2 as shown, which states no rejection or disqualification.
  - downstream proposal `DS-08` issue (row:VOL-V-36.2-01): **conflicting — applied rule: VOL-I 3.2 provides: 'In the event of any conflict, ambiguity or discrepancy between or within the RFP Documents, the following order of precedence shall apply, the first named prevailing:' — the cover is the addendum's summary of itself, n…**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-opus-5-5
      - concern: The issue is correctly framed as an ambiguity. It quotes both the cover and Section 2.1, states both readings, names an owner and leaves the decision to a person. That matches the rule that the cover summarises and the difference is reported, not resolved. Since the point turns on which figure gove…
      - concern: The controller's 'applied rule' and 'consistency (phases)' records treat VOL-I 3.2 as settling the point in favour of the operative provision. The only part of VOL-I 3.2 shown is its lead-in ('the following order of precedence shall apply, the first named prevailing:'); the order itself is not prin…
      - concern: The issue cites ADD-03 1.2 (references read as amended by Addenda Nos. 1 and 2) and ADD-03 2.2 / Form 4-F (Availability Payment price assumption). Neither is printed in this request, so those dependency claims could not be checked.
      - concern: The issue should also say that, against the ADD-02 figure of SAR 2,500,000, the cover's 'reduces ... to SAR 4,000,000' would be an increase.
      - concern: show_in_a3 false is consistent: neither unit states a bid-out consequence.
  - output difference: CHANGED VOL-V-36.2-01; A5 REWORK deviations-review; A5 REWORK form-4e

### ADD-03:2.2 (clause, p1) — applied (PROPOSED; not approved)
- source: “Bidders shall take Section 2.1 into account in the Availability Payment quoted in Form 4-F.”
- transition: `ADD-03/2.2` amendment_op annotate ADD-03:2.2 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The provision prints an obligation and does not change the words of Form 4-F, so an adds_obligation annotation on ADD-03:2.2 follows from the text. The dependency on ADD-03/2.1 is correct. The annotation does not itself name the Form 4-F Availability Payment field as a dependent; the paired row ADD…
- transition: `ADD03-2.2` row_new {"row": {"id": "ADD03-2.2", "group": "Financial Proposal", "scope": ["Bidder"], "requirement": "Bidders shall take Section 2.1 into account in the Availability Payment quoted in Form 4-F.", "units": …
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The requirement is quoted word for word, and no consequence is stated or inferred.
    - concern: The interpretation note calls Section 2.1 a reduction of 'the Change in Law compensation threshold'. That wording comes from the cover summary. The operative words in S-F1 are only 'The amount stated in Volume V Clause 36.2 is reduced by SAR 1,000,000.', and the text of Clause 36.2 is not shown. Th…
    - concern: Some listed dependents cannot be checked against the evidence shown: 'Financial Model' and 'VOL-IV:F4-F/para1 confirmation'. Only the Form 4-F Availability Payment field is quoted.
    - concern: The 'medium' confidence depends on the cover/operative discrepancy. As noted under the cover item, that discrepancy has not been shown from 36.2's effective text and a computed figure.
  - downstream proposal `DS-13` row_new (c46:ADD-03/2.2): **insufficient_evidence** — held back: issue references not among the promoted issues: ['I-ADD03-CIL-THRESHOLD']
  - downstream proposal `DS-ACT-FIN-MODEL-BUILD` no_change (act:fin-model-build): **interpretation_pending**
  - downstream proposal `DS-DEP-36.2-MODEL` dependency (act:fin-model-build): **interpretation_pending**
  - downstream proposal `DS-22-ROW` row_new (oblig:ADD-03/2.2): **invalid**
  - downstream proposal `DS-22-ISSUE` issue (oblig:ADD-03/2.2): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-22-DEP` dependency (oblig:ADD-03/2.2): **insufficient_evidence** — held back: endpoints not promotable: ['ADD-03-2.2-01']

### ADD-03:3.1 (clause, p1) — applied (PROPOSED; not approved)
- source: “Volume II Clause 8.5 is relocated to Volume V, in which it becomes Clause 42.3. Its text is unchanged and reads as follows: ‘42.3 A handback condition survey shall be carried out in the final two (2) years of the concession, and any remedial works identified shall be completed before transfer.’”
- transition: `ADD-03/3.1` amendment_op relocate_unit VOL-II:8.5
  - validation: **evidence_verified**
  - downstream: units changed VOL-II:8.5, VOL-V:42.3; rows citing them VOL-II-8.5-01, VOL-II-8.5-02
  - downstream proposal `DS-04` dependency (row:VOL-II-8.5-01): **insufficient_evidence** — held back: endpoints not promotable: ['ADD-03-3.1-01']
  - downstream proposal `DS-05` dependency (row:VOL-II-8.5-02): **insufficient_evidence** — held back: endpoints not promotable: ['ADD-03-3.1-02']
  - downstream proposal `DS-14` row_new (c46:ADD-03/3.1): **invalid**
  - downstream proposal `DS-15` row_new (c46:ADD-03/3.1): **invalid**
  - downstream proposal `DS-31-DEP` dependency (oblig:ADD-03/3.1): **interpretation_pending**
  - downstream proposal `DS-31-ISSUE` issue (oblig:ADD-03/3.1): **interpretation_pending — HUMAN DECISION PENDING**
  - output difference: OUT VOL-II-8.5-01; OUT VOL-II-8.5-02

### ADD-03:3.2 (clause, p1) — no effect (PROPOSED; not approved)
- source: “The number 8.5 is not reused in Volume II, and the Clauses of Volume II are not renumbered.”
- transition: `ADD-03/3.2` disposition no_effect: The provision prints no change of its own: 'The number 8.5 is not reused in Volume II, and the Clauses of Volume II are not renumbered.' It states only that th…
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The no_effect reason depends on a relocation of VOL-II:8.5 in ADD-03:3.1 (op ADD-03/3.1), but neither ADD-03:3.1 nor that op is printed in the request. I cannot check that 8.5 is relocated rather than deleted or replaced, so I cannot check that the sentence only confirms the numbering.
    - concern: 'The number 8.5 is not reused in Volume II' does more than describe: it sets a lasting rule that number 8.5 stays vacant in Volume II. Whether that rule needs recording (for example as a note on the vacated number) or truly has no effect is a person's decision. Under the shared rules, a no_effect w…
    - concern: The controller's semantic check found no amendment words only after setting aside 'the sentences that say nothing changes'. Here that set-aside sentence is the whole provision, so the check confirms little.

### ADD-03:3.3 (clause, p1) — applied (PROPOSED; not approved)
- source: “In Volume V Clause 42.1, ‘Volume II Clause 8.5’ is deleted and ‘Clause 42.3’ is substituted.”
- transition: `ADD-03/3.3` amendment_op replace_text VOL-V:42.1 “Volume II Clause 8.5” → “Clause 42.3”
  - validation: **evidence_verified**
  - downstream: units changed VOL-V:42.1; rows citing them VOL-V-42.1-01, VOL-V-42.1-02
  - downstream proposal `DS-09` row_reading (row:VOL-V-42.1-01): **interpretation_pending**
  - downstream proposal `DS-10` row_reading (row:VOL-V-42.1-02): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-11` issue (row:VOL-V-42.1-02): **interpretation_pending — HUMAN DECISION PENDING**
  - output difference: CHANGED VOL-V-42.1-01; CHANGED VOL-V-42.1-02; A5 REWORK deviations-review; A5 REWORK form-4e

### ADD-03:3.4 (clause, p1) — PARTLY APPLIED (an escalated sibling stays unresolved)
- source: “In Volume V Clause 42.1, ‘with a remaining design life of not less than five (5) years for all major assets’ is deleted and ‘with a residual service life, for each asset class, of not less than that stated in Table 42-1’ is substituted. Table 42-1 is reproduced at Appendix A to this Addendum and forms part of Volume V.”
- transition: `ADD-03/3.4(a)` amendment_op replace_text VOL-V:42.1 “with a remaining design life of not less than five (5) years for all major asse…” → “with a residual service life, for each asset class, of not less than that state…”
  - validation: **evidence_verified**
- transition: `ADD-03/3.4(b)` escalation why: software limitation: 'Table 42-1 is reproduced at Appendix A to this Addendum and forms part of Volume V.' Appendix A is the Arabic image table ADD-03:p3-image (title 'جدول ٤٢-١: الحد الأدنى للعمر ال…
  - validation: **escalated**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The escalation is classed as a software limitation and blames the engine's failure to match Arabic-Indic '٤٢-١' to 42-1. But the engine's recorded refusal says 'its id and title name another', and that full record is not in the request. The stated cause is the proposer's guess, so I can't confirm i…
    - concern: The rationale says the crop shows 'a letter of the Asset Transfer Committee No. ٤١٧/٢٠٢٦ dated ١٥ نوفمبر ٢٠٢٦م' around the table. That letter text (its sender, number and date) is not quoted as evidence or raised as a point anywhere. It is attachment content that is not accounted for, and it may be…
    - concern: Escalating the insertion to Document control, and declining to insert the English group because of ADD-03:3.5, is consistent with the printed words.
  - downstream: units changed VOL-V:42.1; rows citing them VOL-V-42.1-01, VOL-V-42.1-02
  - downstream proposal `DS-09` row_reading (row:VOL-V-42.1-01): **interpretation_pending**
  - downstream proposal `DS-10` row_reading (row:VOL-V-42.1-02): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-11` issue (row:VOL-V-42.1-02): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-CQ-HANDBACK` clarification_item (clar:CQ-HANDBACK-CONDITION): **invalid — HUMAN DECISION PENDING**
  - downstream proposal `DS-3.4-ESC` escalation (esc:ADD-03:3.4): **escalated**
  - downstream proposal `DS-3.4-DEP` dependency (esc:ADD-03:3.4): **interpretation_pending**
  - downstream proposal `DS-HB-ESC` escalation (impact:3. HANDBACK): **escalated**
  - downstream proposal `DS-HB-DEP` dependency (impact:3. HANDBACK): **interpretation_pending**
  - downstream proposal `DS-READ-ROW` row_new (reading:ADD-03-p3-r1): **interpretation_pending**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
      - concern: insufficient evidence: the request does not print the reading for rows r1, r2 and r3 or for note1. Only r4, r5, note2, note3 and the intro sentence are quoted. So I cannot check the life values ٢٠, ٢٠ and ٥, the grades ٢, ٢ and ٣, or the grade-scale note against the evidence. The crop sha is cited,…
      - concern: Who decides: Legal. The row takes the Arabic values as the operative ones: row 4 is ٧ rather than 5, and row 5 is ٢٤ شهراً rather than 24 years. It also calls Appendix B 'the translation' and 'not evidence'. The only support shown is the three words 'The Arabic text governs.' from ADD-03:3.5. That …
      - concern: Possible mismatch over which appendix holds the table. Provision ADD-03:3.4 says 'Table 42-1 is reproduced at Appendix A to this Addendum and forms part of Volume V.' The row reads the table from the Arabic image on p3 and calls the English version on p4 'Appendix B'. The request does not show whet…
      - concern: The 'requirement' field is an English paraphrase of the Arabic. It adds content, such as 'condition grade not worse than the maximum stated', that is not in the quoted intro sentence. That content comes from the column heading 'أقصى درجة للحالة', which needs the r1–r5 crops to check. The paraphrase…
      - concern: Follow-on work is not listed, and 'dependencies' is empty. 3.4 deletes 'with a remaining design life of not less than five (5) years for all major assets', so any existing A1 row built on that wording is superseded and should be named. ADD-03:3.6 (lifecycle plan in the Technical Proposal) depends o…
      - concern: Minor: the row's scope is ['proposal'] but its assessment is contractual_post_award, and it is off A3 and A5. The scope and the assessment do not match.
  - downstream proposal `DS-READ-ISSUE-UNIT` issue (reading:ADD-03-p3-r1): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-READ-DEP-TP` dependency (reading:ADD-03-p3-r1): **interpretation_pending**
  - output difference: CHANGED VOL-V-42.1-01; CHANGED VOL-V-42.1-02; A5 REWORK deviations-review; A5 REWORK form-4e; A5 REVIEW (possible impact) fin-model-build; A5 REVIEW (possible impact) technical-proposal

### ADD-03:3.5 (clause, p1) — applied (PROPOSED; not approved)
- source: “Table 42-1 is issued in the Arabic language. The Arabic text governs. The English translation at Appendix B is provided for convenience only.”
- transition: `ADD-03/3.5` amendment_op annotate ADD-03:p3-image, ADD-03:T42-1 effect interprets
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The text of ADD-03:T42-1 (the English Appendix B group) is not printed in the units, so I cannot independently check it as the 'over' target. The annotation correctly quotes 'The Arabic text governs.' and stays interpretation_pending for a person.
- transition: `ADD-03/issue/3.5` issue {"text": "ambiguous: Table 42-1 is printed twice and the renderings differ. Section 3.5: 'The Arabic text governs. The English translation at Appendix B is provided for convenience only.' (1) Row 4 (…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: S-F4 is labelled a fact but says the English note (4) 'amends Volume II Clause 2.2'. Whether it amends anything is one of the readings the issue itself leaves open, so that part is an interpretation, not a fact.
    - concern: The Arabic row labels for rows 4 and 5 are not quoted as evidence; only the value cells are. The class names in the issue text are taken from the English translation.
    - concern: The owner is Technical, but the open questions are which rendering binds and whether an English-only note amends Volume II Clause 2.2. Those also read on precedence, which may need Legal as decision owner.
    - concern: The committee-letter text in the same crop (No. ٤١٧/٢٠٢٦, dated ١٥ نوفمبر ٢٠٢٦م) is not mentioned.
  - downstream proposal `DS-HB-ESC` escalation (impact:3. HANDBACK): **escalated**
  - downstream proposal `DS-HB-DEP` dependency (impact:3. HANDBACK): **interpretation_pending**
  - downstream proposal `DS-READ-ISSUE-RENDER` issue (reading:ADD-03-p3-r1): **interpretation_pending — HUMAN DECISION PENDING**

### ADD-03:3.6 (clause, p1) — UNRESOLVED (accounted for, not applied)
- source: “The Bidder shall demonstrate in the Technical Proposal how its lifecycle plan achieves the residual service lives in Table 42-1.”
- transition: `ADD-03/row/3.6` row_new {"row": {"id": "R-ADD03-3.6", "group": "Technical Proposal", "scope": ["Technical Proposal"], "requirement": "The Bidder shall demonstrate in the Technical Proposal how its lifecycle plan achieves th…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The row states assessment 'pass_fail', but its own confidence_reason says 'whether it is pass/fail or scored is not stated in ADD-03:3.6'. The classification has no basis in the pack's words. It should stay unresolved or be clearly marked as a proposal or assumption, not set as the row's value.
    - concern: The row's evidence list is empty, while the rationale names a Technical Proposal lifecycle-plan section as the evidence item. That evidence item should be recorded or listed as follow-on work for A5.
    - concern: The verbatim quote, 'none_stated' consequence, ADD-03 introduction stage and cross-reference to the Arabic/English difference are consistent with the printed words.
  - downstream proposal `DS-ADD03-3.6-row` row_new (ana:ADD-03/row/3.6): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-3.6-issue` issue (ana:ADD-03/row/3.6): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ACT-TECH-PROPOSAL` activity (act:technical-proposal): **interpretation_pending**
  - downstream proposal `DS-HB-ESC` escalation (impact:3. HANDBACK): **escalated**
  - downstream proposal `DS-HB-DEP` dependency (impact:3. HANDBACK): **interpretation_pending**
  - output difference: NEW ADD-03-3.6-01; A5 REWORK technical-proposal

### ADD-03:4.1 (clause, p2) — applied (PROPOSED; not approved)
- source: “The following new Clause 12.5 is inserted in Volume V after Clause 12.4: ‘12.5 If the Project Company encounters at the site ground conditions that are materially more adverse than those described in the Geotechnical Baseline Report, it shall be entitled to an extension of the Scheduled PCOD and to payment of its reasonable additional costs, provided that i…”
- transition: `ADD-03/4.1` amendment_op insert_unit VOL-V:12.4 “If the Project Company encounters at the site ground conditions that are materially more adverse than those described i…”
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-opus-5-5
    - concern: The follow-on list cites VOL-V:3.3 and 'Form 4-E deviations', but neither unit is printed in this request. That dependency can't be checked here.
    - concern: The provision limits its definition with 'In this Clause, the Geotechnical Baseline Report means Revision C...'. ADD-03:4.2 and 4.3 use the same term outside Clause 12.5, so whether they mean Revision C is open. This should be listed as follow-on work for those rows.
- transition: `ADD-03/4.1/row` row_new {"row": {"id": "R-VOLV-12.5", "group": "project_agreement", "scope": ["Project Company"], "requirement": "If the Project Company encounters at the site ground conditions that are materially more adve…
  - validation: **interpretation_pending**
- transition: `ADD-03/4.1/issue-gbr` clarification {"gap": "insufficient evidence: ADD-03:4.1 defines 'the Geotechnical Baseline Report means Revision C of the report of that name issued by the Authority', and ADD-03:4.2 and 4.3 rely on it, but no do…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The claim that no report with that name or revision is in the pack rests on a search ('hits only in ADD-03:4.1-4.4') that isn't shown here, and ADD-03:4.4 isn't printed. The controller records check the quotations, not that the report is absent. The request doesn't show enough to confirm the 'insuf…
    - concern: The gap says 'ADD-03:4.2 and 4.3 rely on it', but the definition is limited by 'In this Clause'. Whether 4.2 and 4.3 mean Revision C is a separate ambiguity. It is folded into a missing-evidence item instead of being raised as its own 'ambiguous:' point.
    - concern: Whether the GBR Revision C is the same document as ADD-01:Q4's 'geotechnical report in the data room' is also an ambiguity, not missing evidence. The question asks about it, which is right, but the gap doesn't classify it.
- transition: `ADD-03/4.1/issue-q4` issue {"text": "ambiguous: new Volume V Clause 12.5 (ADD-03:4.1) gives an extension of the Scheduled PCOD and additional costs for ground conditions 'materially more adverse than those described in the Geo…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Reading 1 relies on 'ADD-03 (which takes precedence under ADD-03:1.1)', but ADD-03:1.1 isn't quoted or printed. The precedence premise has no evidence and leans the issue toward one answer.
    - concern: Reading 1 also says VOL-V:3.3's 'the term' does not touch the Scheduled PCOD. No definition of 'term' or 'Scheduled PCOD' is quoted, so this is an unsupported reading, not a fact.
    - concern: Reading 2 combines two separate questions: how far ADD-01:Q4 still applies, and whether VOL-V:3.3 needs a conforming change. Each should be stated as its own question with its own readings.
    - concern: The issue describes a tension, but its conflicts field is empty.
    - concern: ADD-01:Q4 refers to 'the geotechnical report in the data room', and Clause 12.5 refers to the GBR Revision C. Nothing shown establishes that they are the same document, and the issue's readings assume a link between them.
  - downstream: units changed VOL-V:12.4+ADD-03; rows citing them none
  - downstream proposal `DS-ADD03-4.1-row` row_new (c46:ADD-03/4.1): **interpretation_pending**
  - downstream proposal `DS-ADD03-4.1-issue` issue (c46:ADD-03/4.1): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-4.1-dep` dependency (c46:ADD-03/4.1): **invalid**
  - downstream proposal `DS-GROUND-ISSUE` issue (impact:4. GROUND CONDITIONS): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-GROUND-MISSING` dependency (impact:4. GROUND CONDITIONS): **invalid**
  - downstream proposal `DS-GROUND-4.2-ESC` escalation (impact:4. GROUND CONDITIONS): **escalated**
  - downstream proposal `DS-41-ROW` row_new (oblig:ADD-03/4.1): **invalid**
  - downstream proposal `DS-41-ISSUE-PROVISO` issue (oblig:ADD-03/4.1): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-41-ISSUE-GBR` issue (oblig:ADD-03/4.1): **invalid — HUMAN DECISION PENDING**
  - downstream proposal `DS-41-MISSING` dependency (oblig:ADD-03/4.1): **invalid**
  - downstream proposal `DS-41-DEP-PCOD` dependency (oblig:ADD-03/4.1): **interpretation_pending**
  - output difference: NEW ADD-03-4.1-01; A5 REWORK deviations-review; A5 REWORK form-4e

### ADD-03:4.2 (clause, p2) — UNRESOLVED (accounted for, not applied)
- source: “Each Bidder shall state in the Technical Proposal the ground conditions assumed for the design of foundations, by reference to the Geotechnical Baseline Report.”
- transition: `ADD-03/4.2/row` row_new {"row": {"id": "R-ADD03-4.2", "group": "technical_proposal", "scope": ["Bidder"], "requirement": "Each Bidder shall state in the Technical Proposal the ground conditions assumed for the design of fou…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: confidence_reason assumes the report referred to in 4.2 is 'Revision C'. The definition in ADD-03:4.1 is limited to 'this Clause' (12.5), so that link is an interpretation and should not be stated as fact.
    - concern: The rationale cites ADD-03:cover/para3 and VOL-I:9.7, but neither is printed here, so I couldn't check that the cover matches or that 9.7 is unaffected.
  - downstream proposal `DS-ADD03-4.2-row` row_new (ana:ADD-03/4.2/row): **interpretation_pending**
  - downstream proposal `DS-GROUND-ISSUE` issue (impact:4. GROUND CONDITIONS): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-GROUND-MISSING` dependency (impact:4. GROUND CONDITIONS): **invalid**
  - downstream proposal `DS-GROUND-4.2-ESC` escalation (impact:4. GROUND CONDITIONS): **escalated**
  - output difference: NEW ADD-03-4.2-01; A5 REWORK technical-proposal

### ADD-03:4.3 (clause, p2) — UNRESOLVED (accounted for, not applied)
- source: “A Bidder that wishes to inspect the borehole cores and laboratory records on which the Geotechnical Baseline Report is based shall request an appointment through the Portal within three (3) Working Days of the date of this Addendum. Appointments will be held at the Authority's core store in Sakaka not later than three (3) Working Days before the Proposal Du…”
- transition: `ADD-03/4.3/row` row_new {"row": {"id": "R-ADD03-4.3", "group": "procedure", "scope": ["Bidder"], "requirement": "A Bidder that wishes to inspect the borehole cores and laboratory records on which the Geotechnical Baseline R…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The date rule notes give typed dates (2026-11-19 / 2026-11-22 / 2026-11-23) said to come from calculate. No calculate record appears in the controller validation shown, and VOL-I 2.4 (said to make the backward count a single reading) isn't printed. These can't be checked here.
    - concern: S-I2 says 'Planning uses the conservative 19 November 2026 pending a person'. That is a planning choice and should be labelled 'PROVISIONAL ASSUMPTION:' with its basis, not left in an interpretation statement.
    - concern: Q19's 'the period stated in that Section' could refer to the request period or the appointment window, since Section 4.3 states both. It most likely means the request period, but tying the 'lesser' consequence to the request deadline is itself an interpretation.
    - concern: ADD-03:Q19 is cited as a unit but isn't printed under units. Its text is only available through S-F6.
- transition: `ADD-03/4.3/q-count` clarification {"gap": "ambiguous: 'within three (3) Working Days of the date of this Addendum' (ADD-03:4.3), the Addendum being 'Issued 17 November 2026'. Reading 1 (issue day counted): last day Thursday 19 Novemb…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: interim_handling ('Plan to request by Thursday 19 November 2026 (conservative reading)') is a planning assumption and should be labelled 'PROVISIONAL ASSUMPTION:' with its basis.
    - concern: Both dates are said to come from calculate, but no calculate record appears in the controller validation shown. The claim that VOL-I 2.4 covers only backward counting can't be checked because that unit isn't printed.
    - concern: The anchor treats 'the date of this Addendum' as the printed 'Issued 17 November 2026'. That is reasonable on the evidence shown, but it is an assumption, and the gap doesn't state it.
  - downstream proposal `DS-ADD03-4.3-row` row_new (ana:ADD-03/4.3/row): **interpretation_pending**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
      - concern: The consequence comes from ADD-03:Q19, quoted as 'Requests made after the period stated in that Section will not be accommodated.' Q19 is not printed under `units`. That means I cannot check from the evidence shown that 'that Section' refers to ADD-03 Section 4.3, or that the quotation is complete.…
      - concern: The interpretation note says 'VOL-I 4.2 is disapplied for the communications described in ADD-03 4.4.' Neither VOL-I 4.2 nor ADD-03 4.4 is printed. The point does not come from ADD-03:4.3, and it brings another clause into this row. That widens the row beyond what its provision names. It should be …
      - concern: The forward-counting date rule is marked 'ambiguous counting' and also 'Escalated'. The stated reason is that 'VOL-I 2.4 covers backward counting only', meaning no approved method covers forward counting. That reason points to a software limitation (no approved method) or a gap in the pack's counti…
      - concern: The note calls the reading that counts the issue day 'conservative planning'. That leans toward one reading. If the planning tools or A5 use 2026-11-19, it should be labelled 'PROVISIONAL ASSUMPTION:' with its basis. Otherwise the reading is in effect being chosen.
      - concern: The anchor 'Issued 17 November 2026' (ADD-03 cover) and the Proposal Due Date of 2026-11-26 (VOL-I:6.1 at ADD-03) are not printed in this request. The computed values rest only on statement downstream-002/S-F-4.3-DATES.
      - concern: The 'requirement' quotes only the first sentence of 4.3, which is right for the Bidder's obligation. The second sentence, about when appointments are held, is the Authority's undertaking. It is kept only as a date rule and in the note. I see no problem with that, provided it is never presented as a…
  - downstream proposal `DS-ADD03-4.3-ev` evidence_item (ana:ADD-03/4.3/row): **evidence_verified**
  - downstream proposal `DS-ADD03-4.3-act` activity (ana:ADD-03/4.3/row): **interpretation_pending**
  - downstream proposal `DS-ADD03-4.3-esc` escalation (ana:ADD-03/4.3/row): **escalated**
  - downstream proposal `DS-GROUND-ISSUE` issue (impact:4. GROUND CONDITIONS): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-GROUND-MISSING` dependency (impact:4. GROUND CONDITIONS): **invalid**
  - downstream proposal `DS-GROUND-4.2-ESC` escalation (impact:4. GROUND CONDITIONS): **escalated**
  - downstream proposal `DS-43-ROW` row_new (date:ADD-03:4.3:within three (3) Working Days of the date of this Addendum): **invalid**
  - downstream proposal `DS-43-ESC` escalation (date:ADD-03:4.3:within three (3) Working Days of the date of this Addendum): **escalated**
  - downstream proposal `DS-43-MILESTONE` activity (date:ADD-03:4.3): **invalid**
  - output difference: NEW ADD-03-4.3-01; A5 NEW core-inspection-request

### ADD-03:4.4 (clause, p2) — applied (PROPOSED; not approved)
- source: “Volume I Clause 4.2 does not apply to communications with the Authority's geotechnical consultant during an appointment under Section 4.3, to the extent that they concern the identification and handling of cores and records.”
- transition: `ADD-03/4.4` amendment_op annotate VOL-I:4.2 effect disapplies
  - validation: **interpretation_pending**
  - downstream proposal `DS-03` row_reading (row:VOL-I-4.2-01): **interpretation_pending**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
      - concern: The interpretation's `quote` gives the prohibition with no qualification. The ADD-03:4.4 exception appears only in the free-text `note`. A1 or A3 output that uses just the quote and the disqualification consequence would overstate the prohibition at ADD-03. The exception should travel with the row …
      - concern: The exception only applies 'during an appointment under Section 4.3'. Section 4.3 (presumably ADD-03 Section 4.3) is not printed here, and `dependencies` is empty. The window and the appointment it depends on should be listed as a dependency, as change propagation requires.
      - concern: The rationale says the date rules BLACKOUT-START and BLACKOUT-END 'carry over unchanged'. No evidence for those rules is shown here, so I could not check that statement.
      - concern: The note correctly leaves to a person (Legal / Bid management) whether a particular communication falls inside the exception. It also correctly keeps the text of VOL-I:4.2 unchanged and does not widen the carve-out beyond 'identification and handling of cores and records'.
  - output difference: CONFIRMED (unchanged) VOL-I-4.2-01

### ADD-03:Q15 (table_row, p2) — applied (PROPOSED; not approved)
- source: “No: 15 | Bidder question: Will the minutes of the Pre-Bid Conference at Appendix B to Addendum No. 1 be issued in Arabic? | Authority response: No. The minutes are issued in English only. Section 3.2 of Addendum No. 1 continues to apply to them.”
- transition: `ADD-03/Q15` amendment_op annotate ADD-01:3.2 effect interprets
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The response's first statement ('The minutes are issued in English only.') is about the language of the minutes. The item shows no check of whether any language or translation clause in the pack bears on Appendix B. If one exists, it is a dependency that has not been named.
    - concern: ADD-01:AppB is listed as a dependency but is not printed in the evidence, so I could not check it.

### ADD-03:Q16 (table_row, p2) — applied (PROPOSED; not approved)
- source: “No: 16 | Bidder question: At what stage must the grievance mechanism referred to in Volume II Clause 9.3 be in place? | Authority response: The grievance mechanism shall be established before construction, shall be accessible to the affected community and shall be maintained for the concession period. Volume II Clause 9.3 applies.”
- transition: `ADD-03/Q16` amendment_op annotate VOL-II:9.3 effect confirms
  - validation: **evidence_verified**
  - downstream proposal `DS-06` row_reading (row:VOL-II-9.3-01): **interpretation_pending**
  - output difference: CONFIRMED (unchanged) VOL-II-9.3-01; A5 CONFIRMED (unchanged) technical-proposal

### ADD-03:Q17 (table_row, p2) — applied (PROPOSED; not approved)
- source: “No: 17 | Bidder question: Volume I Clause 10.1 states that no document other than Form 4-F and the Financial Model shall be placed in Envelope B, but Volume I Clause 10.6 requires a schedule of financing assumptions to be submitted with Form 4-F. Where is the schedule to be placed? | Authority response: The schedule required by Volume I Clause 10.6 forms pa…”
- transition: `ADD-03/Q17(a)` amendment_op annotate VOL-I:10.1, VOL-I:10.6 effect interprets
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group; model claude-opus-5-5
    - concern: The annotate/interprets op on VOL-I:10.1 and VOL-I:10.6 is supported by the words 'forms part of Form 4-F and shall be attached to it in Envelope B'. However, the rationale says the response 'settles where the schedule goes' and 'does not breach the 'only' rule in 10.1'. That treats the apparent co…
    - concern: 'shall be attached to it in Envelope B' puts a placement obligation on the bidder that 10.6 ('submit with Form 4-F') does not state. The effect may be 'adds_obligation' rather than plain 'interprets'. A person should confirm which.
    - concern: The third sentence of the response ('A schedule placed in Envelope A will be treated in accordance with Volume I Clause 6.2.') is not covered by this op. It is raised only through the row's issue (ADD-03/Q17/issue), and that issue is not shown here.
    - concern: S-Q17-fact quotes VOL-I:6.2. That unit is not printed in the request's units, and the controller records no verbatim check for it in this item, so the quotation is unverified.
    - concern: VOL-IV:F4-F is named as a dependency but not printed. I could not check whether Form 4-F already provides for an attachment.
- transition: `ADD-03/Q17(b)` amendment_op annotate VOL-I:10.6 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The annotate/adds_obligation op on VOL-I:10.6 is supported by 'The schedule shall also state the minimum annual debt service cover ratio assumed.' However, the rationale's follow-on says 'the financial model and the Form 4-F schedule must include the DSCR figure'. The response names only 'The sched…
    - concern: S-Q17-fact quotes VOL-I:6.2, which is not printed in units and was not verified by the controller in this item.
- transition: `ADD-03/Q17/row-dscr` row_new {"row": {"id": "ADD-03-Q17-1", "group": "Commercial", "scope": ["Envelope B", "Form 4-F"], "requirement": "The schedule required by Volume I Clause 10.6 forms part of Form 4-F and shall be attached t…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The requirement is quoted verbatim from ADD-03:Q17. Setting the consequence to 'none_stated' and handing the Envelope A / 6.2 point to an issue is consistent with not inferring a consequence.
    - concern: assessment 'pass_fail' is not stated in the evidence shown. If it is a default, it should be labelled as a provisional reading.
    - concern: The note quotes VOL-I:6.2. That text is not printed in the request's units, and the controller records no verbatim check of it, so the quotation is unverified here.
    - concern: The row's own 'evidence' list is empty. The items the bidder must produce (the schedule, with DSCR, attached to Form 4-F) are not listed for A5.
- transition: `ADD-03/Q17/issue` issue {"text": "ambiguous: ADD-03:Q17 says 'A schedule placed in Envelope A will be treated in accordance with Volume I Clause 6.2.' VOL-I:6.2 says 'The appearance of any price, rate, or other commercial i…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-01` row_reading (row:VOL-I-10.1-01): **interpretation_pending**
  - downstream proposal `DS-02` row_reading (row:VOL-I-10.6-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-Q17-row` row_new (ana:ADD-03/Q17/row-dscr): **interpretation_pending**
  - downstream proposal `DS-ADD03-Q17-issue` issue (ana:ADD-03/Q17/row-dscr): **interpretation_pending — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
      - concern: The issue's owner is 'Commercial', but statement S-I-Q17-6.2 says 'Commercial/Legal'. Whether VOL-I 6.2 applies to the schedule is partly about what 'other commercial information' means. Legal should probably be named as a co-owner, or the difference should be reconciled.
      - concern: Q17 also adds an obligation: 'The schedule shall also state the minimum annual debt service cover ratio assumed.' It also says the schedule 'forms part of Form 4-F and shall be attached to it in Envelope B.' This issue does not cover either point. Check that each is captured as its own register row…
      - concern: The bidder's question points to a tension between VOL-I 10.1 ('no document other than Form 4-F and the Financial Model') and VOL-I 10.6. Whether Q17's answer settles that tension is for a person to decide. No item shown here records it. Neither VOL-I 10.1 nor 10.6 is printed.
      - concern: Only the quoted span of VOL-I:6.2 is printed, not the full clause. I relied on the controller's verbatim check for it.
      - concern: Both readings are fairly drawn from the words quoted, and no reading is chosen. 'show_in_a3' is false, which is right while the reading is still pending.
  - downstream proposal `DS-ACT-FORM-4F` activity (act:form-4f): **interpretation_pending**
  - downstream proposal `DS-ACT-FIN-MODEL-FREEZE` no_change (act:fin-model-freeze): **interpretation_pending**
  - downstream proposal `DS-ACT-LENDER-TERMS` no_change (act:lender-terms): **interpretation_pending**
  - downstream proposal `DS-ACT-FIN-ASSUMPTIONS` activity (act:fin-assumptions): **interpretation_pending**
  - downstream proposal `DS-Q17-ESC` escalation (impact:5. RESPONSES TO CLARIFICATION REQUESTS 15 TO 19): **escalated**
  - downstream proposal `DS-Q18-ESC` escalation (impact:5. RESPONSES TO CLARIFICATION REQUESTS 15 TO 19): **escalated**
  - downstream proposal `DS-Q17-ROW` row_new (oblig:ADD-03/Q17(b)): **invalid**
  - downstream proposal `DS-Q17-DEP` dependency (oblig:ADD-03/Q17(b)): **insufficient_evidence** — held back: endpoints not promotable: ['ADD-03-Q17-01']
  - output difference: NEW ADD-03-Q17-01; A5 NOT SETTLED assemble-envelope-b; A5 REWORK fin-assumptions; A5 NOT SETTLED fin-assumptions; A5 NOT SETTLED fin-model-build; A5 NOT SETTLED fin-model-freeze; A5 REWORK form-4f; A5 NOT SETTLED form-4f; A5 REWORK lender-terms; A5 NOT SETTLED lender-terms

### ADD-03:Q18 (table_row, p2) — applied (PROPOSED; not approved)
- source: “No: 18 | Bidder question: Volume V Clause 39.5 refers to a Direct Agreement with the Senior Lenders. If the Direct Agreement provides for compensation on termination for Project Company default that differs from Volume V Clause 40.2, which prevails? | Authority response: The Authority notes the question. The order of precedence at Volume I Clause 3.2 applie…”
- transition: `ADD-03/Q18` amendment_op annotate VOL-I:3.2 effect interprets
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: S-Q18-fact says 'VOL-I:3.1 lists the RFP Documents without naming a Direct Agreement'. VOL-I:3.1 is not printed in the units, and the controller has no verbatim check of it, so I cannot verify the quotation or the inference.
    - concern: Only the lead-in of VOL-I:3.2 is shown, not the precedence list, so whether a Direct Agreement falls within it cannot be checked. Correctly, the point stays an ambiguity for Legal.
    - concern: The third sentence ('The Direct Agreement will be negotiated with the Senior Lenders after the Preferred Bidder Notification.') is not reflected in the note. Its follow-on, if any (A5 or Commercial), is not listed.
    - concern: The referenced issue and draft clarification (ADD-03/Q18/issue) are not shown.
- transition: `ADD-03/Q18/issue` issue {"text": "ambiguous: the bidder asked whether a Direct Agreement term on compensation for termination for Project Company default prevails over VOL-V:40.2. The response says only 'The order of preced…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
- transition: `ADD-03/Q18/question` clarification {"gap": "The response to clarification 18 does not say whether a Direct Agreement term on compensation for termination for Project Company default can depart from VOL-V:40.2. The Direct Agreement is …
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-Q17-ESC` escalation (impact:5. RESPONSES TO CLARIFICATION REQUESTS 15 TO 19): **escalated**
  - downstream proposal `DS-Q18-ESC` escalation (impact:5. RESPONSES TO CLARIFICATION REQUESTS 15 TO 19): **escalated**

### ADD-03:Q19 (table_row, p2) — applied (PROPOSED; not approved)
- source: “No: 19 | Bidder question: May Bidders inspect the borehole cores and laboratory records from the site investigation? | Authority response: Yes, by appointment. Section 4.3 of this Addendum applies. Requests made after the period stated in that Section will not be accommodated.”
- transition: `ADD-03/Q19` amendment_op annotate ADD-03:4.3 effect interprets
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The target ADD-03:4.3 is identified with certainty: Q19 names 'Section 4.3 of this Addendum'.
    - concern: 'Requests made after the period stated in that Section will not be accommodated' attaches a consequence that 4.3 does not print. The effect may be better recorded as adding a (non-bid-out) consequence on the 4.3 row than as 'interprets' alone. It is correctly kept out of A3.
    - concern: The follow-on names only the 'within three (3) Working Days of the date of this Addendum' rule. It omits 4.3's second date rule, 'not later than three (3) Working Days before the Proposal Due Date', which the A5 programme also needs.
  - downstream proposal `DS-43-DEP-Q19` dependency (date:ADD-03:4.3:within three (3) Working Days of the date of this Addendum): **insufficient_evidence** — held back: endpoints not promotable: ['ADD-03-4.3-01']

### ADD-03:AppA/para1 (paragraph, p3) — no effect (PROPOSED; not approved)
- source: “The following table is reproduced as issued by the Authority's Asset Transfer Committee under cover of its letter No. 417/2026 dated 15 November 2026. The Arabic text governs in accordance with Section 3.5 of this Addendum.”
- transition: `ADD-03/AppA/para1` disposition no_effect: An introductory paragraph to the reproduced letter. It amends no volume unit: it says 'The following table is reproduced as issued by the Authority's Asset Tra…
  - validation: **interpretation_pending — applied rule: ADD-03 3.5 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application**

### ADD-03:p3-image/r1 (table_row, p3) — no effect (PROPOSED; not approved)
- source: “م: ١ | فئة الأصول: المنشآت المدنية والخرسانية | الحد الأدنى للعمر المتبقي (سنة): ٢٠ | أقصى درجة للحالة: ٢”
- transition: `ADD-03/p3-image/r1` disposition no_effect: Row 1 of Table 42-1 as issued in Arabic ('م: ١ | فئة الأصول: المنشآت المدنية والخرسانية | الحد الأدنى للعمر المتبقي (سنة): ٢٠ | أقصى درجة للحالة: ٢'). It amend…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The table qualifier 'يجب ألا يقل العمر المتبقي' creates an obligation, so this no_effect is for a person to decide. The reason says so, and the status interpretation_pending is right. The controller's semantic check found no obligation words, but it read only the row text, not the qualifier.
    - concern: The rationale checks the Arabic against the English translation. That is fine as a cross-check only. A translation is never evidence for the source, so the reading must rest on crop r01 and the cell crops.
    - concern: The reason names no dependants beyond 3.4. The row's obligation will need an A1 row, and the Section 3.6 lifecycle plan relies on it. This should be listed as follow-on work, as note3 does.
    - concern: ADD-03:3.4's insert_table op is in another batch and is not shown here, so I cannot confirm the row actually enters the state through it.

### ADD-03:p3-image/r2 (table_row, p3) — no effect (PROPOSED; not approved)
- source: “م: ٢ | فئة الأصول: خط نقل المياه المعالجة | الحد الأدنى للعمر المتبقي (سنة): ٢٠ | أقصى درجة للحالة: ٢”
- transition: `ADD-03/p3-image/r2` disposition no_effect: Row 2 of Table 42-1 as issued in Arabic ('م: ٢ | فئة الأصول: خط نقل المياه المعالجة | الحد الأدنى للعمر المتبقي (سنة): ٢٠ | أقصى درجة للحالة: ٢'). It amends no…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: Same as r1: the table's obliging qualifier makes this no_effect a person's decision, and the item correctly leaves it pending.
    - concern: Matching against the English row 2 is corroboration only, not evidence for the Arabic.
    - concern: Follow-on A1 and lifecycle-plan dependants are not listed.
    - concern: I cannot check 3.4's insert_table op, which is in another batch.

### ADD-03:p3-image/r3 (table_row, p3) — no effect (PROPOSED; not approved)
- source: “م: ٣ | فئة الأصول: المعدات الميكانيكية | الحد الأدنى للعمر المتبقي (سنة): ٥ | أقصى درجة للحالة: ٣”
- transition: `ADD-03/p3-image/r3` disposition no_effect: Row 3 of Table 42-1 as issued in Arabic ('م: ٣ | فئة الأصول: المعدات الميكانيكية | الحد الأدنى للعمر المتبقي (سنة): ٥ | أقصى درجة للحالة: ٣'). It amends no vol…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: Same as r1: the table's obliging qualifier makes this no_effect a person's decision, and the item correctly leaves it pending.
    - concern: Matching against the English row 3 is corroboration only, not evidence for the Arabic.
    - concern: Follow-on A1 and lifecycle-plan dependants are not listed.
    - concern: I cannot check 3.4's insert_table op, which is in another batch.

### ADD-03:p3-image/r4 (table_row, p3) — UNRESOLVED (accounted for, not applied)
- source: “م: ٤ | فئة الأصول: المعدات الكهربائية وأجهزة القياس والتحكم | الحد الأدنى للعمر المتبقي (سنة): ٧ | أقصى درجة للحالة: ٣”
- transition: `ADD-03/p3-image/r4` disposition unresolved: ambiguous: the Arabic row 4 prints 'الحد الأدنى للعمر المتبقي (سنة): ٧' (seven years) for 'المعدات الكهربائية وأجهزة القياس والتحكم', while the Appendix B tran…
  - validation: **interpretation_pending — applied rule: ADD-03 3.5 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application**
- transition: `ISS-ADD03-T42-1-r4` issue {"text": "ambiguous: Table 42-1 row 4 (electrical, instrumentation and control equipment). The governing Arabic prints 'الحد الأدنى للعمر المتبقي (سنة): ٧' (7 years); the Appendix B translation print…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Section 3.5 says 'The Arabic text governs.', so the Arabic is not itself unclear. This is a discrepancy between the Arabic and the translation. Keeping it open is still right, because deciding which text governs belongs to a person.
    - concern: The open question is about the governing-language clause, so Legal should probably share ownership with Technical.
  - downstream proposal `DS-R4-ESC` escalation (esc:ADD-03:p3-image/r4): **escalated**
  - downstream proposal `DS-APPA-ISSUE` issue (impact:APPENDIX A — TABLE 42-1 (ARABIC)): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-APPA-ESC` escalation (impact:APPENDIX A — TABLE 42-1 (ARABIC)): **invalid**

### ADD-03:p3-image/r5 (table_row, p3) — UNRESOLVED (accounted for, not applied)
- source: “م: ٥ | فئة الأصول: الأغشية (إن وُجدت) | الحد الأدنى للعمر المتبقي (سنة): ٢٤ شهراً | أقصى درجة للحالة: ٣”
- transition: `ADD-03/p3-image/r5` disposition unresolved: ambiguous: the Arabic row 5 cell prints '٢٤ شهراً' (24 months) under the column heading 'الحد الأدنى للعمر المتبقي (سنة)' (years), while the Appendix B transla…
  - validation: **interpretation_pending — applied rule: ADD-03 3.5 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application**
- transition: `ISS-ADD03-T42-1-r5` issue {"text": "ambiguous: Table 42-1 row 5 (membranes, where provided). The governing Arabic cell prints '٢٤ شهراً' (24 months) in the column headed 'الحد الأدنى للعمر المتبقي (سنة)' (years); the Appendix…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The ambiguity is real within the Arabic alone: the cell says 'شهراً' (months) under a column headed 'سنة' (years). The 24-years reading should rest on the Arabic column heading. Citing the translation as support for a reading of the source goes against 'a translation is never evidence for the sourc…
    - concern: Unlike the r4 issue, this one lists no dependants. It should name note ٣'s replacement obligation, the Section 3.6 lifecycle plan and any A1 row.
- transition: `ISS-ADD03-cover-four-classes` issue {"text": "The cover text and the operative table differ. The cover says 'minimum residual service lives for four asset classes set out in Table 42-1 (issued in Arabic)'; the Arabic Table 42-1 prints …
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The open question suggests a possible resolution ('e.g. if row 5 applies only where provided'). It leans toward one reading and would be better stated neutrally.
- transition: `Q-ADD03-T42-1-r4-r5` clarification {"gap": "Table 42-1 as issued in Arabic (which governs under Addendum No. 3 Section 3.5) differs from the Appendix B translation. Row 4 prints '٧' years where the translation prints 5. Row 5 prints '…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Part (c) cites note (4) and the gap cites Section 3.5, but neither ADD-03:T42-1/note(4) nor ADD-03:3.5 is in the item's own evidence list. S-F3 is also missing from its statements.
    - concern: 'Handback cost allowance' in practical_impact is not quoted from any unit in the pack. It should be tied to pack words or dropped.
    - concern: The Section 3.6 lifecycle plan text is not printed here, so I cannot verify it.
    - concern: Part (b) puts the translation alongside the column heading as a basis for the 24-years reading. The Arabic heading alone is enough.
  - downstream proposal `DS-R5-ESC` escalation (esc:ADD-03:p3-image/r5): **escalated**
  - downstream proposal `DS-APPA-ISSUE` issue (impact:APPENDIX A — TABLE 42-1 (ARABIC)): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-APPA-ESC` escalation (impact:APPENDIX A — TABLE 42-1 (ARABIC)): **invalid**

### ADD-03:p3-image/hdr-en (reading_block, p3) — no effect (PROPOSED; not approved)
- source: “Northern Utilities Procurement Authority - Asset Transfer Committee”
- transition: `ADD-03/p3-image/hdr-en` disposition no_effect: Letterhead identifying the issuer: 'Northern Utilities Procurement Authority - Asset Transfer Committee'. It prints no change, obligation or exception.
  - validation: **evidence_verified**

### ADD-03:p3-image/hdr-ar (reading_block, p3) — no effect (PROPOSED; not approved)
- source: “الهيئة الشمالية للمشتريات المرفقية”
- transition: `ADD-03/p3-image/hdr-ar` disposition no_effect: Arabic letterhead naming the Authority: 'الهيئة الشمالية للمشتريات المرفقية'. It prints no change, obligation or exception.
  - validation: **evidence_verified**

### ADD-03:p3-image/committee-ar (reading_block, p3) — no effect (PROPOSED; not approved)
- source: “لجنة نقل الأصول”
- transition: `ADD-03/p3-image/committee-ar` disposition no_effect: Arabic letterhead naming the committee: 'لجنة نقل الأصول' (Asset Transfer Committee). It prints no change, obligation or exception.
  - validation: **evidence_verified**

### ADD-03:p3-image/date-ar (reading_block, p3) — no effect (PROPOSED; not approved)
- source: “التاريخ: ١٥ نوفمبر ٢٠٢٦م”
- transition: `ADD-03/p3-image/date-ar` disposition no_effect: The letter's date: 'التاريخ: ١٥ نوفمبر ٢٠٢٦م'. It identifies the letter and sets no date rule, obligation or exception. It agrees with ADD-03:AppA/para1, 'lett…
  - validation: **evidence_verified**

### ADD-03:p3-image/ref-ar (reading_block, p3) — no effect (PROPOSED; not approved)
- source: “الرقم: ٤١٧/٢٠٢٦”
- transition: `ADD-03/p3-image/ref-ar` disposition no_effect: The letter's reference number: 'الرقم: ٤١٧/٢٠٢٦'. It identifies the letter and agrees with ADD-03:AppA/para1, 'letter No. 417/2026'. It prints no change, oblig…
  - validation: **evidence_verified**

### ADD-03:p3-image/subject (reading_block, p3) — no effect (PROPOSED; not approved)
- source: “الموضوع: متطلبات حالة الأصول عند نقل محطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان”
- transition: `ADD-03/p3-image/subject` disposition no_effect: The letter's subject line: 'الموضوع: متطلبات حالة الأصول عند نقل محطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان'. It describes and does not amend, oblige …
  - validation: **evidence_verified**

### ADD-03:p3-image/tender-ref (reading_block, p3) — no effect (PROPOSED; not approved)
- source: “مناقصة رقم: NUPA/ISTP/2026/014”
- transition: `ADD-03/p3-image/tender-ref` disposition no_effect: The tender reference: 'مناقصة رقم: NUPA/ISTP/2026/014'. It identifies the tender and prints no change, obligation or exception.
  - validation: **evidence_verified**

### ADD-03:p3-image/notes-heading (reading_block, p3) — no effect (PROPOSED; not approved)
- source: “ملاحظات:”
- transition: `ADD-03/p3-image/notes-heading` disposition no_effect: A heading only: 'ملاحظات:' (Notes:). It prints no change, obligation or exception. It introduces the notes of Table 42-1, which ADD-03:3.4 incorporates into Vo…
  - validation: **evidence_verified**

### ADD-03:p3-image/note1 (reading_block, p3) — no effect (PROPOSED; not approved)
- source: “١. تُقيِّم درجة الحالة وفق مقياس الهيئة لتصنيف حالة الأصول المكوَّن من خمس درجات، وتعني الدرجة ١ أن الأصل بحالة جديدة.”
- transition: `ADD-03/p3-image/note1` disposition no_effect: A definitional note of Table 42-1: '١. تُقيِّم درجة الحالة وفق مقياس الهيئة لتصنيف حالة الأصول المكوَّن من خمس درجات، وتعني الدرجة ١ أن الأصل بحالة جديدة.' It …
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The note refers to 'مقياس الهيئة لتصنيف حالة الأصول' (the Authority's five-grade condition scale). The item does not say whether that scale is supplied in the pack. If it is not, this is missing evidence and should be recorded as such.

### ADD-03:p3-image/note2 (reading_block, p3) — no effect (PROPOSED; not approved)
- source: “٢. يحدِّد المهندس المستقل العمر المتبقي لكل أصل في مسح الحالة الذي يُجرى قبل النقل.”
- transition: `ADD-03/p3-image/note2` disposition no_effect: A procedural note of Table 42-1: '٢. يحدِّد المهندس المستقل العمر المتبقي لكل أصل في مسح الحالة الذي يُجرى قبل النقل.' It amends no volume unit by itself. It i…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The reason says the condition survey 'is the subject of ADD-03:3.1 (Clause 42.3)'. ADD-03:3.1 is not printed in this request, so I cannot verify that cross-reference.
    - concern: The note gives the Independent Engineer a role in setting residual life. Possible A1 and A5 dependants, such as the condition survey activity, are not listed.

### ADD-03:p3-image/note3 (reading_block, p3) — no effect (PROPOSED; not approved)
- source: “٣. يُستبدَل على نفقة شركة المشروع قبل تاريخ النقل كلَّ أصل لا يستوفي متطلبات هذا الجدول.”
- transition: `ADD-03/p3-image/note3` disposition no_effect: This note obliges: '٣. يُستبدَل على نفقة شركة المشروع قبل تاريخ النقل كلَّ أصل لا يستوفي متطلبات هذا الجدول.' (an asset not meeting the table is replaced at th…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The note obliges replacement at the Project Company's cost, so a no_effect is a person's decision. The item correctly flags this and lists the A1 follow-on work.
    - concern: The scope of the replacement obligation depends on the open row 4 and row 5 values. ISS-ADD03-T42-1-r4 and ISS-ADD03-T42-1-r5 should be named as dependencies.
- transition: `ISS-ADD03-T42-1-note4` issue {"text": "ambiguous: the governing Arabic Table 42-1 prints three notes, the last being '٣. يُستبدَل على نفقة شركة المشروع قبل تاريخ النقل كلَّ أصل لا يستوفي متطلبات هذا الجدول.' The English translat…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Reading (b) would amend Volume II Clause 2.2. That unit is not named as a target, and its effective text at ADD-02 is not quoted, so a person cannot see what would change.
    - concern: The provision is cited as note3 and the target as the whole table, while the note (4) provision sits in another batch. The tie between this issue and that provision should be made explicit.
    - concern: The absence of an Arabic note ٤ rests on the proposer's crop observation. Only note ٣ is quoted as evidence, and I cannot check the absence myself.
    - concern: Dependants are not listed: the design-life basis in Volume II 2.2 and any A1 or A5 items for electrical design life.
  - downstream proposal `DS-APPA-ISSUE` issue (impact:APPENDIX A — TABLE 42-1 (ARABIC)): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-APPA-ESC` escalation (impact:APPENDIX A — TABLE 42-1 (ARABIC)): **invalid**

### ADD-03:p3-image/signatory (reading_block, p3) — no effect (PROPOSED; not approved)
- source: “رئيس لجنة نقل الأصول”
- transition: `ADD-03/p3-image/signatory` disposition no_effect: The signature block: 'رئيس لجنة نقل الأصول' (Chairman of the Asset Transfer Committee) above a signature stroke. It prints no change, obligation or exception.
  - validation: **evidence_verified**

### ADD-03:p3-image/seal (reading_block, p3) — no effect (PROPOSED; not approved)
- source: “”
- transition: `ADD-03/p3-image/seal` disposition no_effect: The seal position. The reading's text is empty, and crop b17-right shows only an empty oval outline with no legible words. It prints no change, obligation or e…
  - validation: **evidence_verified**

### ADD-03:p3-image/image-footer (reading_block, p3) — no effect (PROPOSED; not approved)
- source: “FICTIONAL DOCUMENT - Lamar Holding internal assessment pack - not a real tender.”
- transition: `ADD-03/p3-image/image-footer` disposition no_effect: The image footer: 'FICTIONAL DOCUMENT - Lamar Holding internal assessment pack - not a real tender.' A document-marking line that prints no change, obligation …
  - validation: **evidence_verified**

### ADD-03:AppA/para2 (paragraph, p3) — no effect (PROPOSED; not approved)
- source: “End of reproduction.”
- transition: `ADD-03/AppA/para2` disposition no_effect: A closing marker: 'End of reproduction.' It prints no change, obligation or exception.
  - validation: **evidence_verified**

### ADD-03:AppB/para1 (paragraph, p4) — no effect (PROPOSED; not approved)
- source: “This translation is provided for convenience only. The Arabic text of Table 42-1 at Appendix A governs. Asset Transfer Committee letter No. 417/2026 dated 15 November 2026. Subject: asset condition requirements on transfer of the Wadi Sirhan Independent Sewage Treatment Plant. Tender No. NUPA/ISTP/2026/014.”
- transition: `D-AppB-para1` disposition no_effect: Introductory words of the convenience translation; they amend no Volume unit. They state the translation's status: "This translation is provided for convenienc…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'is provided', 'provided')

### ADD-03:AppB/para2 (paragraph, p4) — no effect (PROPOSED; not approved)
- source: “The residual service life of each asset class at the date of transfer of the Facility to the Authority shall be not less than stated below.”
- transition: `D-AppB-para2` disposition no_effect: The words oblige ("shall be not less than stated below") but they are the convenience translation of the Arabic qualifier "يجب ألا يقل العمر المتبقي لكل فئة من…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'shall')

### ADD-03:T42-1/1 (table_row, p4) — no effect (PROPOSED; not approved)
- source: “No: 1 | Asset class: Civil and concrete structures | Minimum residual life (years): 20 | Maximum condition grade: 2”
- transition: `D-T42-1-1` disposition no_effect: Convenience translation of Arabic row 1 ("المنشآت المدنية والخرسانية | الحد الأدنى للعمر المتبقي (سنة): ٢٠ | أقصى درجة للحالة: ٢"); the values agree as read. "…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The reason quotes the Arabic asset class "المنشآت المدنية والخرسانية" and "أقصى درجة للحالة: ٢", but these words are not in the item's evidence. The only Arabic quotation in the evidence, which the controller verified, is "الحد الأدنى للعمر المتبقي (سنة): ٢٠". Unit ADD-03:p3-image/r1 is not printed…
    - concern: A no_effect disposition for a convenience-translation row depends on that row matching the governing Arabic row. Here the match rests on S-I2, an interpretation with no evidence that is still pending a person, so the disposition cannot be confirmed from the evidence shown.
    - concern: The reason says "The row enters Volume V with the Arabic table under ADD-03:3.4" without quoting ADD-03:3.4. That clause is not in the evidence.

### ADD-03:T42-1/2 (table_row, p4) — no effect (PROPOSED; not approved)
- source: “No: 2 | Asset class: Treated effluent transmission main | Minimum residual life (years): 20 | Maximum condition grade: 2”
- transition: `D-T42-1-2` disposition no_effect: Convenience translation of Arabic row 2 ("خط نقل المياه المعالجة", ٢٠ years, grade ٢); the values agree as read. "This translation is provided for convenience …
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The reason quotes "خط نقل المياه المعالجة" and grade ٢ from the Arabic row, but neither is in the evidence. Only the residual-life cell "الحد الأدنى للعمر المتبقي (سنة): ٢٠" is quoted and verified. Unit ADD-03:p3-image/r2 is not printed, so the claim that the values agree can be checked for residua…
    - concern: The no_effect depends on S-I2, an interpretation with no evidence that is pending a person.

### ADD-03:T42-1/3 (table_row, p4) — no effect (PROPOSED; not approved)
- source: “No: 3 | Asset class: Mechanical equipment | Minimum residual life (years): 5 | Maximum condition grade: 3”
- transition: `D-T42-1-3` disposition no_effect: Convenience translation of Arabic row 3 ("المعدات الميكانيكية", ٥ years, grade ٣); the values agree as read. "This translation is provided for convenience only…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The reason quotes "المعدات الميكانيكية" and grade ٣ from the Arabic row, but neither is in the evidence. Only "الحد الأدنى للعمر المتبقي (سنة): ٥" is quoted and verified. Unit ADD-03:p3-image/r3 is not printed, so the grade cannot be checked.
    - concern: The no_effect depends on S-I2, which is pending a person.

### ADD-03:T42-1/4 (table_row, p4) — UNRESOLVED (accounted for, not applied)
- source: “No: 4 | Asset class: Electrical, instrumentation and control equipment | Minimum residual life (years): 5 | Maximum condition grade: 3”
- transition: `D-T42-1-4` disposition unresolved: ambiguous: the translation prints "Minimum residual life (years): 5" for "Electrical, instrumentation and control equipment" while the Arabic row as read print…
  - validation: **conflicting — applied rule: ADD-03 3.5 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application** — declared_conflicts: the proposer declares: ADD-03:p3-image/r4
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-opus-5-5
    - concern: S-F2 is labelled a fact, but the Arabic figure ٧ comes from reading an image. Its standing should match S-I1 (a reading pending approval) unless that reading has been validated.
    - concern: Strictly, this is a conflict between two renderings where the pack states which one governs (ADD-03:3.5 "The Arabic text governs."), rather than a pure ambiguity of words. The proposer correctly applies the rule but does not decide it, and leaves the decision to a person. That is acceptable, but th…
    - concern: Follow-on effects (A1 rows and A5 lifecycle-plan activities that rely on the E&I residual life) are not listed in the item.
- transition: `ISS-T42-row4` issue {"text": "ambiguous: Table 42-1 row 4 (electrical, instrumentation and control equipment): the English translation prints \"Minimum residual life (years): 5\"; the governing Arabic row as read prints…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The issue calls the Arabic row "governing". This follows ADD-03:3.5, but the open question should stay neutral about whether that rule is applied.
    - concern: The issue cites ADD-03:3.6, which is not quoted in the evidence.
    - concern: The target ADD-03:p3-image/r4 is the Arabic counterpart of the provision rather than a unit the provision cites. That is reasonable for an issue, but a person should note it.
  - downstream proposal `DS-T4-ESC` escalation (esc:ADD-03:T42-1/4): **escalated**
  - downstream proposal `DS-APPB-DEP` dependency (impact:APPENDIX B — ENGLISH TRANSLATION OF TABLE 42-1): **interpretation_pending**
  - downstream proposal `DS-APPB-ESC` escalation (impact:APPENDIX B — ENGLISH TRANSLATION OF TABLE 42-1): **conflicting — applied rule: ADD-03 3.5 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The item calls this an ambiguity, but the words it relies on are not unclear about which text binds. The statement it relies on (downstream-003/S-F-3.5) quotes ADD-03:3.5 in full: 'The Arabic text governs. The English translation at Appendix B is provided for convenience only.' The item's own evide…
      - concern: The controller's consistency check failed: this item reverses ADD-03/issue/3.5, which applied 'The Arabic text governs.' The shared rules allow an earlier reading to be reopened only when its evidence or a dependency changes, and then the change must be quoted. The item quotes no such change. A per…
      - concern: The Arabic values the item cites (row 4 '٧', row 5 '٢٤ شهراً') and the claim that note (4) 'has no Arabic counterpart' have no supporting evidence. No Arabic unit is cited and every crop_sha256 is null. The rationale does not say what any image showed. The units printed for this review include only…
      - concern: The scope is wider than the named provision. The item names ADD-03:T42-1/4 as its provision, but it also covers T42-1/5 and note (4). Its evidence has nothing for row 4's Arabic value and no record for note (4) beyond a statement it relies on.
      - concern: Note (4) appears only in the English text, yet it reads as a change: 'The design life of electrical equipment stated in Volume II Clause 2.2 is increased to twenty-five (25) years.' If the Arabic text really has no counterpart, the point is a separate one: does the translation amend anything? It sh…
      - concern: The classes are mixed. The reason begins 'ambiguous:', but the escalation's what_is_unsupported field says 'nothing is unsupported by the software'. By the item's own account this is an interpretation pending a person, which belongs in an issue, not a software-limitation escalation.
      - concern: The item states several things that the evidence shown does not support: 'now that the window has closed' (no evidence about a clarification window is cited), 'No price row is reached directly', and that VOL-V:42.1 and VOL-II-2.2-01/-02 are affected. These should be quoted or listed as dependencies…
      - concern: The downstream effects (the lifecycle plan under ADD-03:3.6, CQ-HANDBACK-CONDITION) rest on downstream-003/S-I-CONDITIONAL, an interpretation with no evidence that a person must still confirm.

### ADD-03:T42-1/5 (table_row, p4) — UNRESOLVED (accounted for, not applied)
- source: “No: 5 | Asset class: Membranes (where provided) | Minimum residual life (years): 24 | Maximum condition grade: 3”
- transition: `D-T42-1-5` disposition unresolved: ambiguous: the translation prints "Minimum residual life (years): 24" for "Membranes (where provided)"; the Arabic cell as read prints "٢٤ شهراً" (24 months) u…
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:p3-image/r5
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-opus-5-5
    - concern: Two separate points are combined in one reason: the months/years discrepancy, and the cover's "four asset classes" against five printed rows. The cover summarises and does not amend, so the four/five point is a cover-vs-operative difference and would be better kept as its own point.
    - concern: S-F3 treats the Arabic image reading as a fact; it should be confirmed as a validated reading.
    - concern: ADD-03:cover/para3 is not printed among the units. Its quotation was verified only on ISS-T42-row5.
    - concern: Follow-on effects on the membrane replacement allowance and lifecycle-plan activities are not listed.
- transition: `ISS-T42-row5` issue {"text": "ambiguous: Table 42-1 row 5 (membranes): the governing Arabic cell as read prints \"٢٤ شهراً\" (months) under a column headed \"(سنة)\" (years); the English translation prints \"Minimum res…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: One issue combines two open questions that are independent: months vs years for membranes, and four vs five classes. Splitting them would let each be decided on its own.
    - concern: The issue calls the Arabic cell "governing". It should stay neutral about whether ADD-03:3.5 is applied.
    - concern: Technical as the owner is plausible, but which rendering governs is also a Legal point.
- transition: `Q-T42-row5` clarification {"gap": "Table 42-1 (Arabic, governing) row 5 prints \"٢٤ شهراً\" in the column headed \"(سنة)\"; the translation prints 24 years; row 4 prints ٧ in Arabic and 5 in the translation; translation note …
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Part (c) tells the Authority that Note (4) "has no counterpart in the Arabic table". That rests on S-I1, an image reading still pending approval. The draft should not assert it until the reading is confirmed.
    - concern: The evidence list omits ADD-03:p3-image/r4 and ADD-03:p3-image/r5 and the cover quotation; these come in only through the statements.
    - concern: The question bundles four separate points under the row 5 provision, so its traceability to rows 4 and note (4) is indirect.
    - concern: It remains a DRAFT, and a person decides whether to send it.
  - downstream proposal `DS-T5-ESC` escalation (esc:ADD-03:T42-1/5): **escalated**
  - downstream proposal `DS-APPB-DEP` dependency (impact:APPENDIX B — ENGLISH TRANSLATION OF TABLE 42-1): **interpretation_pending**
  - downstream proposal `DS-APPB-ESC` escalation (impact:APPENDIX B — ENGLISH TRANSLATION OF TABLE 42-1): **conflicting — applied rule: ADD-03 3.5 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The item calls this an ambiguity, but the words it relies on are not unclear about which text binds. The statement it relies on (downstream-003/S-F-3.5) quotes ADD-03:3.5 in full: 'The Arabic text governs. The English translation at Appendix B is provided for convenience only.' The item's own evide…
      - concern: The controller's consistency check failed: this item reverses ADD-03/issue/3.5, which applied 'The Arabic text governs.' The shared rules allow an earlier reading to be reopened only when its evidence or a dependency changes, and then the change must be quoted. The item quotes no such change. A per…
      - concern: The Arabic values the item cites (row 4 '٧', row 5 '٢٤ شهراً') and the claim that note (4) 'has no Arabic counterpart' have no supporting evidence. No Arabic unit is cited and every crop_sha256 is null. The rationale does not say what any image showed. The units printed for this review include only…
      - concern: The scope is wider than the named provision. The item names ADD-03:T42-1/4 as its provision, but it also covers T42-1/5 and note (4). Its evidence has nothing for row 4's Arabic value and no record for note (4) beyond a statement it relies on.
      - concern: Note (4) appears only in the English text, yet it reads as a change: 'The design life of electrical equipment stated in Volume II Clause 2.2 is increased to twenty-five (25) years.' If the Arabic text really has no counterpart, the point is a separate one: does the translation amend anything? It sh…
      - concern: The classes are mixed. The reason begins 'ambiguous:', but the escalation's what_is_unsupported field says 'nothing is unsupported by the software'. By the item's own account this is an interpretation pending a person, which belongs in an issue, not a software-limitation escalation.
      - concern: The item states several things that the evidence shown does not support: 'now that the window has closed' (no evidence about a clarification window is cited), 'No price row is reached directly', and that VOL-V:42.1 and VOL-II-2.2-01/-02 are affected. These should be quoted or listed as dependencies…
      - concern: The downstream effects (the lifecycle plan under ADD-03:3.6, CQ-HANDBACK-CONDITION) rest on downstream-003/S-I-CONDITIONAL, an interpretation with no evidence that a person must still confirm.

### ADD-03:T42-1/notes (note_intro, p4) — no effect (PROPOSED; not approved)
- source: “Notes to Table 42-1:”
- transition: `D-T42-1-notes` disposition no_effect: A heading only ("Notes to Table 42-1:"), translating the Arabic "ملاحظات:"; it states nothing and amends no unit.
  - validation: **evidence_verified**

### ADD-03:T42-1/note(1) (note, p4) — no effect (PROPOSED; not approved)
- source: “(1) Condition grade is assessed on the Authority's five-point asset condition grading scale, grade 1 meaning as new.”
- transition: `D-T42-1-note1` disposition no_effect: Convenience translation of Arabic note ١ ("١. تُقيِّم درجة الحالة وفق مقياس الهيئة لتصنيف حالة الأصول المكوَّن من خمس درجات، وتعني الدرجة ١ أن الأصل بحالة جديد…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The reason quotes Arabic note ١ in full, but no evidence item, crop hash or controller check covers that text, and ADD-03:p3-image/note1 is not printed. The quotation cannot be verified.
    - concern: The no_effect depends on S-I2, which is pending a person. Note (1) is definitional, which supports no_effect, but whether it matches the Arabic is not shown.

### ADD-03:T42-1/note(2) (note, p4) — no effect (PROPOSED; not approved)
- source: “(2) The Independent Engineer determines the residual service life of each asset in the condition survey carried out before transfer.”
- transition: `D-T42-1-note2` disposition no_effect: Convenience translation of Arabic note ٢ ("٢. يحدِّد المهندس المستقل العمر المتبقي لكل أصل في مسح الحالة الذي يُجرى قبل النقل."); the translation amends no uni…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The Arabic note ٢ quoted in the reason is not in the evidence and was not verified by the controller. ADD-03:p3-image/note2 is not printed.
    - concern: The no_effect depends on S-I2, which is pending a person.

### ADD-03:T42-1/note(3) (note, p4) — no effect (PROPOSED; not approved)
- source: “(3) Any asset that does not meet this Table shall be replaced at the Project Company's cost before the date of transfer.”
- transition: `D-T42-1-note3` disposition no_effect: The words oblige ("shall be replaced at the Project Company's cost before the date of transfer") but are the convenience translation of Arabic note ٣ ("٣. يُست…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'shall')
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The words create an obligation ("shall be replaced at the Project Company's cost before the date of transfer"), so a no_effect is a person's decision, as the controller flags.
    - concern: The Arabic note ٣ quoted in the reason is not in the evidence and was not verified. ADD-03:p3-image/note3 is not printed.
    - concern: "A post-award contractual obligation" is a characterisation that the pack's words do not state.
    - concern: ADD-03:3.4 is cited without a quotation.
    - concern: "does not meet this Table" depends on the unresolved rows 4 and 5 (D-T42-1-4 and D-T42-1-5). This dependency is not named.
    - concern: The A1 follow-on is mentioned only in the rationale and is not proposed.

### ADD-03:T42-1/note(4) (note, p4) — UNRESOLVED (accounted for, not applied)
- source: “(4) The design life of electrical equipment stated in Volume II Clause 2.2 is increased to twenty-five (25) years.”
- transition: `D-T42-1-note4` disposition unresolved: ambiguous: the note prints a change ("The design life of electrical equipment stated in Volume II Clause 2.2 is increased to twenty-five (25) years.") but only…
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:p3-image
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-opus-5-5
    - concern: The declared conflict names the whole image, ADD-03:p3-image, rather than a unit id. The conflict rests on the absence of a note, read under S-I1, which is still pending approval. If that reading is not confirmed, the point is partly missing evidence rather than ambiguity.
    - concern: Reading 1 could also turn on whether note (4), which amends Volume II, counts as "text of Table 42-1" at all for the purposes of "The Arabic text of Table 42-1 at Appendix A governs." This could be stated for the person deciding.
    - concern: The VOL-II:2.2 quotation is verbatim. Leaving it unchanged pending Legal is correct.
    - concern: The dependants named in the rationale (A1 design-life rows and lifecycle-plan activities) are listed but not proposed. The link to the row 4 E&I residual-life conflict is not named.
- transition: `ISS-T42-note4` issue {"text": "ambiguous: translation note (4) reads \"The design life of electrical equipment stated in Volume II Clause 2.2 is increased to twenty-five (25) years.\" The governing Arabic Table 42-1 (cro…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-N4-ESC` escalation (esc:ADD-03:T42-1/note(4)): **escalated**
  - downstream proposal `DS-APPB-DEP` dependency (impact:APPENDIX B — ENGLISH TRANSLATION OF TABLE 42-1): **interpretation_pending**
  - downstream proposal `DS-APPB-ESC` escalation (impact:APPENDIX B — ENGLISH TRANSLATION OF TABLE 42-1): **conflicting — applied rule: ADD-03 3.5 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The item calls this an ambiguity, but the words it relies on are not unclear about which text binds. The statement it relies on (downstream-003/S-F-3.5) quotes ADD-03:3.5 in full: 'The Arabic text governs. The English translation at Appendix B is provided for convenience only.' The item's own evide…
      - concern: The controller's consistency check failed: this item reverses ADD-03/issue/3.5, which applied 'The Arabic text governs.' The shared rules allow an earlier reading to be reopened only when its evidence or a dependency changes, and then the change must be quoted. The item quotes no such change. A per…
      - concern: The Arabic values the item cites (row 4 '٧', row 5 '٢٤ شهراً') and the claim that note (4) 'has no Arabic counterpart' have no supporting evidence. No Arabic unit is cited and every crop_sha256 is null. The rationale does not say what any image showed. The units printed for this review include only…
      - concern: The scope is wider than the named provision. The item names ADD-03:T42-1/4 as its provision, but it also covers T42-1/5 and note (4). Its evidence has nothing for row 4's Arabic value and no record for note (4) beyond a statement it relies on.
      - concern: Note (4) appears only in the English text, yet it reads as a change: 'The design life of electrical equipment stated in Volume II Clause 2.2 is increased to twenty-five (25) years.' If the Arabic text really has no counterpart, the point is a separate one: does the translation amend anything? It sh…
      - concern: The classes are mixed. The reason begins 'ambiguous:', but the escalation's what_is_unsupported field says 'nothing is unsupported by the software'. By the item's own account this is an interpretation pending a person, which belongs in an issue, not a software-limitation escalation.
      - concern: The item states several things that the evidence shown does not support: 'now that the window has closed' (no evidence about a clarification window is cited), 'No price row is reached directly', and that VOL-V:42.1 and VOL-II-2.2-01/-02 are affected. These should be quoted or listed as dependencies…
      - concern: The downstream effects (the lifecycle plan under ADD-03:3.6, CQ-HANDBACK-CONDITION) rest on downstream-003/S-I-CONDITIONAL, an interpretation with no evidence that a person must still confirm.

### ADD-03:AppB/para3 (paragraph, p4) — no effect (PROPOSED; not approved)
- source: “Signed: Chairman, Asset Transfer Committee, Northern Utilities Procurement Authority (signature and stamp).”
- transition: `D-AppB-para3` disposition no_effect: Signature block of the translated letter ("Signed: Chairman, Asset Transfer Committee, Northern Utilities Procurement Authority (signature and stamp)."); it st…
  - validation: **evidence_verified**

## Downstream proposals (validated in the candidate)

| Item | Type | Task | Status | First failed check, or what a person confirms |
|---|---|---|---|---|
| DS-01 | row_reading | row:VOL-I-10.1-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-02 | row_reading | row:VOL-I-10.6-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-03 | row_reading | row:VOL-I-4.2-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-04 | dependency | row:VOL-II-8.5-01 | insufficient_evidence | held back: endpoints not promotable: ['ADD-03-3.1-01'] |
| DS-05 | dependency | row:VOL-II-8.5-02 | insufficient_evidence | held back: endpoints not promotable: ['ADD-03-3.1-02'] |
| DS-06 | row_reading | row:VOL-II-9.3-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-07 | row_reading | row:VOL-V-36.2-01 | conflicting | declared_conflicts: the proposer declares: I-ADD03-CIL-THRESHOLD |
| DS-08 | issue | row:VOL-V-36.2-01 | conflicting — applied rule: VOL-I 3.2 provides: 'In the event of any conflict, ambiguity or discrepancy between or within the RFP Documents, the following order of precedence shall apply, the first named prevailing:' — the cover is the addendum's summary of itself, n… | consistency (phases): reverses ADD-03/cover/para3 (ADD-03:cover/para3), which applied VOL-I 3.2 ('Bidders shall acknowledge receipt in Form 4-A (the remainder of the cover summarises the operative pr… |
| DS-09 | row_reading | row:VOL-V-42.1-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-10 | row_reading | row:VOL-V-42.1-02 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words decides which clause governs ('governs') |
| DS-11 | issue | row:VOL-V-42.1-02 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words decides which clause go… |
| DS-12 | row_new | c46:ADD-03/cover/para3 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-13 | row_new | c46:ADD-03/2.2 | insufficient_evidence | held back: issue references not among the promoted issues: ['I-ADD03-CIL-THRESHOLD'] |
| DS-14 | row_new | c46:ADD-03/3.1 | invalid | date rule: VOL-V-42.3-HANDBACK-SURVEY-WINDOW: unknown anchor End of the concession period |
| DS-15 | row_new | c46:ADD-03/3.1 | invalid | date rule: VOL-V-42.3-HANDBACK-REMEDIALS-DUE: unknown anchor Transfer of the Facility |
| DS-ADD03-4.1-row | row_new | c46:ADD-03/4.1 | interpretation_pending | date rule: ADD03-4.1-notice: planning value None (unresolved) |
| DS-ADD03-4.1-issue | issue | c46:ADD-03/4.1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-ADD03-4.1-dep | dependency | c46:ADD-03/4.1 | invalid | relationships.validate: missing_document needs `document_id` (the document, a short id, the conclusion it blocks) |
| DS-ADD03-3.6-row | row_new | ana:ADD-03/row/3.6 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words decides which clause governs ('governs') |
| DS-ADD03-3.6-issue | issue | ana:ADD-03/row/3.6 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words decides which clause go… |
| DS-ADD03-4.2-row | row_new | ana:ADD-03/4.2/row | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-4.3-row | row_new | ana:ADD-03/4.3/row | interpretation_pending | date rule: ADD03-4.3-request: planning value None (unresolved) |
| DS-ADD03-4.3-ev | evidence_item | ana:ADD-03/4.3/row | evidence_verified |  |
| DS-ADD03-4.3-act | activity | ana:ADD-03/4.3/row | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| DS-ADD03-4.3-esc | escalation | ana:ADD-03/4.3/row | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-ADD03-Q17-row | row_new | ana:ADD-03/Q17/row-dscr | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-Q17-issue | issue | ana:ADD-03/Q17/row-dscr | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-CQ-HANDBACK | clarification_item | clar:CQ-HANDBACK-CONDITION | invalid — HUMAN DECISION PENDING | clarify.check: CQ-HANDBACK-CONDITION: recorded answer unit VOL-V:42.1 is not a unit of an Addendum (ADD-) |
| DS-ACT-FORM-4F | activity | act:form-4f | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| DS-ACT-FIN-MODEL-BUILD | no_change | act:fin-model-build | interpretation_pending |  |
| DS-DEP-36.2-MODEL | dependency | act:fin-model-build | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| DS-ACT-FIN-MODEL-FREEZE | no_change | act:fin-model-freeze | interpretation_pending |  |
| DS-ACT-LENDER-TERMS | no_change | act:lender-terms | interpretation_pending |  |
| DS-ACT-FIN-ASSUMPTIONS | activity | act:fin-assumptions | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| DS-ACT-TECH-PROPOSAL | activity | act:technical-proposal | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| DS-3.4-ESC | escalation | esc:ADD-03:3.4 | escalated |  |
| DS-3.4-DEP | dependency | esc:ADD-03:3.4 | interpretation_pending | an inferred relationship stays `possible`: a person confirms or rejects it |
| DS-R4-ESC | escalation | esc:ADD-03:p3-image/r4 | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-R5-ESC | escalation | esc:ADD-03:p3-image/r5 | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-T4-ESC | escalation | esc:ADD-03:T42-1/4 | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-T5-ESC | escalation | esc:ADD-03:T42-1/5 | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-N4-ESC | escalation | esc:ADD-03:T42-1/note(4) | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-GROUND-ISSUE | issue | impact:4. GROUND CONDITIONS | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words decides which clause go… |
| DS-GROUND-MISSING | dependency | impact:4. GROUND CONDITIONS | invalid | relationships.validate: a missing_document entry blocks rows or units only; not: ['ground-dd'] |
| DS-GROUND-4.2-ESC | escalation | impact:4. GROUND CONDITIONS | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-APPA-ISSUE | issue | impact:APPENDIX A — TABLE 42-1 (ARABIC) | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-APPA-ESC | escalation | impact:APPENDIX A — TABLE 42-1 (ARABIC) | invalid | provision: ADD-03:region:ADD-03-p3-r1 is not a provision of ADD-03 |
| DS-APPB-DEP | dependency | impact:APPENDIX B — ENGLISH TRANSLATION OF TABLE 42-1 | interpretation_pending | an inferred relationship stays `possible`: a person confirms or rejects it |
| DS-APPB-ESC | escalation | impact:APPENDIX B — ENGLISH TRANSLATION OF TABLE 42-1 | conflicting — applied rule: ADD-03 3.5 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application | consistency (phases): reverses ADD-03/issue/3.5 (ADD-03:3.5), which applied ADD-03 3.5 ('Section 3.5: 'The Arabic text governs.'): this item hands the point back to a person; ADD-03 3.5 provides: 'Th… |
| DS-CIL-DEP | dependency | impact:Wadi Sirhan Independent Sewage Treatment Plant | interpretation_pending | an inferred relationship stays `possible`: a person confirms or rejects it |
| DS-CIL-ESC | escalation | impact:Wadi Sirhan Independent Sewage Treatment Plant | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-HB-ESC | escalation | impact:3. HANDBACK | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-HB-DEP | dependency | impact:3. HANDBACK | interpretation_pending | an inferred relationship stays `possible`: a person confirms or rejects it |
| DS-Q17-ESC | escalation | impact:5. RESPONSES TO CLARIFICATION REQUESTS 15 TO 19 | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-Q18-ESC | escalation | impact:5. RESPONSES TO CLARIFICATION REQUESTS 15 TO 19 | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-COVER-ROW | row_new | oblig:ADD-03/cover/para3 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-COVER-ISSUE | issue | oblig:ADD-03/cover/para3 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-COVER-DEP | dependency | oblig:ADD-03/cover/para3 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| DS-22-ROW | row_new | oblig:ADD-03/2.2 | invalid | id: row id ADD-03-2.2-01 already exists or was listed before (id ledger) |
| DS-22-ISSUE | issue | oblig:ADD-03/2.2 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words decides which clause go… |
| DS-22-DEP | dependency | oblig:ADD-03/2.2 | insufficient_evidence | held back: endpoints not promotable: ['ADD-03-2.2-01'] |
| DS-31-DEP | dependency | oblig:ADD-03/3.1 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| DS-31-ISSUE | issue | oblig:ADD-03/3.1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words a precedence question (… |
| DS-41-ROW | row_new | oblig:ADD-03/4.1 | invalid | id: row id ADD-03-4.1-01 already exists or was listed before (id ledger) |
| DS-41-ISSUE-PROVISO | issue | oblig:ADD-03/4.1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-41-ISSUE-GBR | issue | oblig:ADD-03/4.1 | invalid — HUMAN DECISION PENDING | id: issue id I-ADD03-GBR is not a new I-... id |
| DS-41-MISSING | dependency | oblig:ADD-03/4.1 | invalid | relationships.validate: a missing_document entry blocks rows or units only; not: ['EV-GROUND-DD'] |
| DS-41-DEP-PCOD | dependency | oblig:ADD-03/4.1 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| DS-Q17-ROW | row_new | oblig:ADD-03/Q17(b) | invalid | id: row id ADD-03-Q17-01 already exists or was listed before (id ledger) |
| DS-Q17-DEP | dependency | oblig:ADD-03/Q17(b) | insufficient_evidence | held back: endpoints not promotable: ['ADD-03-Q17-01'] |
| DS-READ-ROW | row_new | reading:ADD-03-p3-r1 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-READ-ISSUE-RENDER | issue | reading:ADD-03-p3-r1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words decides which clause go… |
| DS-READ-ISSUE-UNIT | issue | reading:ADD-03-p3-r1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-READ-DEP-TP | dependency | reading:ADD-03-p3-r1 | interpretation_pending | an inferred relationship stays `possible`: a person confirms or rejects it |
| DS-43-ROW | row_new | date:ADD-03:4.3:within three (3) Working Days of the date of this Addendum | invalid | id: row id ADD-03-4.3-01 already exists or was listed before (id ledger) |
| DS-43-ESC | escalation | date:ADD-03:4.3:within three (3) Working Days of the date of this Addendum | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-43-DEP-Q19 | dependency | date:ADD-03:4.3:within three (3) Working Days of the date of this Addendum | insufficient_evidence | held back: endpoints not promotable: ['ADD-03-4.3-01'] |
| DS-43-MILESTONE | activity | date:ADD-03:4.3 | invalid | rows: no listed row needs EV-GROUND-DD: the activity would not be planned (a row's evidence list says what it needs) |

- interactions: A5 with the proposals: C45: the programme cannot be planned with the proposals: AttributeError: 'str' object has no attribute 'get'; DS-08: reverses ADD-03/cover/para3 (ADD-03:cover/para3), which applied VOL-I 3.2 ('Bidders shall acknowledge receipt in Form 4-A (the remainder of the cover summarises the operative provisions and am…; DS-APPB-ESC: reverses ADD-03/issue/3.5 (ADD-03:3.5), which applied ADD-03 3.5 ('Section 3.5: 'The Arabic text governs.'): this item hands the point back to a person; ADD-03 3.5 provides: 'The Arabic …
- A5 problems the proposals would add: C45: the programme cannot be planned with the proposals: AttributeError: 'str' object has no attribute 'get'

## Promoted into the candidate (PROPOSED; nothing accepted)

- ops: ADD-03/cover/para3, ADD-03/2.1, ADD-03/2.2, ADD-03/3.1, ADD-03/3.3, ADD-03/3.4(a), ADD-03/3.5, ADD-03/4.1, ADD-03/4.4, ADD-03/Q15, ADD-03/Q16, ADD-03/Q17(a), ADD-03/Q17(b), ADD-03/Q18, ADD-03/Q19
- dispositions: ADD-03:cover/para1: no_effect, ADD-03:cover/para2: no_effect, ADD-03:1.1: no_effect, ADD-03:1.2: no_effect, ADD-03:1.3: no_effect, ADD-03:3.2: no_effect, ADD-03:AppA/para1: no_effect, ADD-03:p3-image/r1: no_effect, ADD-03:p3-image/r2: no_effect, ADD-03:p3-image/r3: no_effect, ADD-03:p3-image/notes-heading: no_effect, ADD-03:p3-image/note1: no_effect, ADD-03:p3-image/note2: no_effect, ADD-03:p3-image/note3: no_effect, ADD-03:p3-image/hdr-en: no_effect, ADD-03:p3-image/hdr-ar: no_effect, ADD-03:p3-image/committee-ar: no_effect, ADD-03:p3-image/date-ar: no_effect, ADD-03:p3-image/ref-ar: no_effect, ADD-03:p3-image/subject: no_effect, ADD-03:p3-image/tender-ref: no_effect, ADD-03:p3-image/signatory: no_effect, ADD-03:p3-image/seal: no_effect, ADD-03:p3-image/image-footer: no_effect, ADD-03:AppA/para2: no_effect, ADD-03:AppB/para1: no_effect, ADD-03:AppB/para2: no_effect, ADD-03:T42-1/1: no_effect, ADD-03:T42-1/2: no_effect, ADD-03:T42-1/3: no_effect, ADD-03:T42-1/notes: no_effect, ADD-03:T42-1/note(1): no_effect, ADD-03:T42-1/note(2): no_effect, ADD-03:T42-1/note(3): no_effect, ADD-03:AppB/para3: no_effect
- accounted unresolved: ADD-03:p3-image/r4, ADD-03:p3-image/r5
- rows new: ADD-03-cover-para3-01, ADD-03-4.1-01, ADD-03-3.6-01, ADD-03-4.2-01, ADD-03-4.3-01, ADD-03-Q17-01, ADD-03-cover-01, ADD-03-T42-1-01
- readings: VOL-I-10.1-01, VOL-I-10.6-01, VOL-I-4.2-01, VOL-II-9.3-01, VOL-V-42.1-01, VOL-V-42.1-02
- issues: I-ADD-03-3-5-3-5-ANA, I-ADD-03-4-1-ISSUE-Q4-ANA, I-ADD-03-COVER-PARA3-ISSUE-ANA, I-ADD-03-GROUND-DD-BASIS, I-ADD-03-P3-IMAGE-NOTE3-ISSUE-ANA, I-ADD-03-P3-IMAGE-R4-ISSUE-ANA, I-ADD-03-P3-IMAGE-R5-ISSUE-ANA, I-ADD-03-Q17-ISSUE-ANA, I-ADD-03-Q18-ISSUE-ANA, I-ADD-03-T42-1-4-ISSUE-ANA, I-ADD-03-T42-1-5-ISSUE-ANA, I-ADD-03-T42-1-LIFECYCLE-PRICING, I-ADD-03-T42-1-NOTE-4-ISSUE-ANA, I-ADD03-12.5-PROVISO, I-ADD03-COL-THRESHOLD, I-ADD03-COVER-DIFF, I-ADD03-GBR, I-ADD03-HANDBACK-LIFE, I-ADD03-HANDBACK-RELOCATION, I-ADD03-Q17-ENV, I-ADD03-T42-1, I-ADD03-T42-1-MEMBRANE-UNIT, I-ADD03-T42-1-RENDERINGS
- analysis issues: I-ADD-03-COVER-PARA3-ISSUE-ANA, I-ADD-03-3-5-3-5-ANA, I-ADD-03-P3-IMAGE-R4-ISSUE-ANA, I-ADD-03-P3-IMAGE-R5-ISSUE-ANA, I-ADD-03-P3-IMAGE-NOTE3-ISSUE-ANA, I-ADD-03-T42-1-4-ISSUE-ANA, I-ADD-03-T42-1-5-ISSUE-ANA, I-ADD-03-T42-1-NOTE-4-ISSUE-ANA, I-ADD-03-4-1-ISSUE-Q4-ANA, I-ADD-03-Q17-ISSUE-ANA, I-ADD-03-Q18-ISSUE-ANA
- evidence items: EV-CORE-INSPECTION-REQUEST
- activities: core-inspection-request, form-4f, fin-assumptions, technical-proposal
- lead times: core_inspection_request
- relationships: REL-AI-001, REL-AI-002, REL-AI-003, REL-AI-004, REL-AI-005, REL-AI-006, REL-AI-007, REL-AI-008, REL-AI-009, REL-REF-GEOTECHNICAL-BASELINE-REPORT-REV-C
- referenced documents: Geotechnical Baseline Report (Revision C)
- no change: act:fin-model-build, act:fin-model-freeze, act:lender-terms
- unresolved provisions: 9
- note: ADD-03:3.4: partly answered by ADD-03/3.4(a); escalated: software limitation: 'Table 42-1 is reproduced at Appendix A to this Addendum and forms part of Volume V.' Appendix A is the Arabic image table ADD-03:p3-image (title 'جدول ٤٢-١: الحد الأدنى للعمر ال… (the promoted item stands; the escalation is for a person)
- note: VOL-I.yaml: 2 comment line(s) inside row VOL-I-4.2-01 were not kept (the row was rewritten; the file's other comments are kept)

- left out of the promoted ops: ADD03-ACK: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/cover/para3` as an UN…; ADD-03/cover/para3/issue: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-COVER-PARA3-ISSUE-ANA; HUMAN DECISIO…; ADD03-2.2: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/2.2` as an UNVERIFIED…; ADD-03/issue/3.5: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-3-5-3-5-ANA; HUMAN DECISION PENDING)…; ADD-03/row/3.6: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/row/3.6` as an UNVERI…; ISS-ADD03-T42-1-r4: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-P3-IMAGE-R4-ISSUE-ANA; HUMAN DECISIO…; ISS-ADD03-T42-1-r5: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-P3-IMAGE-R5-ISSUE-ANA; HUMAN DECISIO…; ISS-ADD03-T42-1-note4: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-P3-IMAGE-NOTE3-ISSUE-ANA; HUMAN DECI…; ISS-ADD03-cover-four-classes: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-P3-IMAGE-R5-ISSUE-ANA; HUMAN DECISIO…; Q-ADD03-T42-1-r4-r5: an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; th…; ISS-T42-row4: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-T42-1-4-ISSUE-ANA; HUMAN DECISION PE…; ISS-T42-row5: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-T42-1-5-ISSUE-ANA; HUMAN DECISION PE…; Q-T42-row5: an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; th…; ISS-T42-note4: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-T42-1-NOTE-4-ISSUE-ANA; HUMAN DECISI…; ADD-03/4.1/row: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/4.1` as an UNVERIFIED…; ADD-03/4.1/issue-gbr: an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; th…; ADD-03/4.1/issue-q4: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-4-1-ISSUE-Q4-ANA; HUMAN DECISION PEN…; ADD-03/4.2/row: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/4.2/row` as an UNVERI…; ADD-03/4.3/row: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/4.3/row` as an UNVERI…; ADD-03/4.3/q-count: an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; th…; ADD-03/Q17/row-dscr: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/Q17/row-dscr` as an U…; ADD-03/Q17/issue: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-Q17-ISSUE-ANA; HUMAN DECISION PENDIN…; ADD-03/Q18/issue: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-Q18-ISSUE-ANA; HUMAN DECISION PENDIN…; ADD-03/Q18/question: an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; th…

## check-register on the candidate

- exit 1; 2 finding(s) {'C46': 2}
- missing because the downstream phase did not propose them (the run's own new rows): 0
- defects: 2
  - [C46] ADD-03/2.2: [A1] ADD-03/2.2 (annotate) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Bidders shall take Section 2.1 into account in the Availability Payment quoted in Form 4-F.'
  - [C46] ADD-03/3.1: [A1] ADD-03/3.1 (relocate_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Volume II Clause 8.5 is relocated to Volume V, in which it becomes Clause 42.3. Its text is u…

## Analysis rows carried to downstream tasks (and other analysis items not promoted)

- `ADD03-ACK` row_new (ADD-03:cover/para3, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/cover/para3` as an UNVERIFIED reference — its obligation is proposed downstream as ADD-03-cover-para3-01 (row_new, interpretation_pending) (task(s) c46:ADD-03/cover/para3; PROPOSED): no op or disposition answers the provision; a person confirms the row and the provision's disposition
- `ADD-03/cover/para3/issue` issue (ADD-03:cover/para3, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-COVER-PARA3-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ADD03-2.2` row_new (ADD-03:2.2, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/2.2` as an UNVERIFIED reference — unresolved: downstream task c46:ADD-03/2.2 answered only by items that cannot be promoted: DS-13 insufficient_evidence (issue references not among the promoted issues: ['I-ADD03-CIL-THRESHOLD'])
- `ADD-03/issue/3.5` issue (ADD-03:3.5, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-3-5-3-5-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ADD-03/row/3.6` row_new (ADD-03:3.6, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/row/3.6` as an UNVERIFIED reference — its obligation is proposed downstream as ADD-03-3.6-01 (row_new, interpretation_pending), DS-ADD03-3.6-issue (issue, interpretation_pending) (task(s) ana:ADD-03/row/3.6; PROPOSED): no op or disposition answers the provision; a person confirms the row and the provision's disposition
- `ISS-ADD03-T42-1-r4` issue (ADD-03:p3-image/r4, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-P3-IMAGE-R4-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ISS-ADD03-T42-1-r5` issue (ADD-03:p3-image/r5, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-P3-IMAGE-R5-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ISS-ADD03-T42-1-note4` issue (ADD-03:p3-image/note3, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-P3-IMAGE-NOTE3-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ISS-ADD03-cover-four-classes` issue (ADD-03:p3-image/r5, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-P3-IMAGE-R5-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `Q-ADD03-T42-1-r4-r5` clarification (ADD-03:p3-image/r5, interpretation_pending): an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; the downstream phase proposes issues and clarification entries against the candidate
- `ISS-T42-row4` issue (ADD-03:T42-1/4, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-T42-1-4-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ISS-T42-row5` issue (ADD-03:T42-1/5, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-T42-1-5-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `Q-T42-row5` clarification (ADD-03:T42-1/5, interpretation_pending): an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; the downstream phase proposes issues and clarification entries against the candidate
- `ISS-T42-note4` issue (ADD-03:T42-1/note(4), interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-T42-1-NOTE-4-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ADD-03/4.1/row` row_new (ADD-03:4.1, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/4.1` as an UNVERIFIED reference — its obligation is proposed downstream as ADD-03-4.1-01 (row_new, interpretation_pending), DS-ADD03-4.1-issue (issue, interpretation_pending) (task(s) c46:ADD-03/4.1; PROPOSED): no op or disposition answers the provision; a person confirms the row and the provision's disposition
- `ADD-03/4.1/issue-gbr` clarification (ADD-03:4.1, interpretation_pending): an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; the downstream phase proposes issues and clarification entries against the candidate — clarification route: bid decision (window closed 2026-11-12) (its suggestion of a clarification is a bid decision now)
- `ADD-03/4.1/issue-q4` issue (ADD-03:4.1, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-4-1-ISSUE-Q4-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ADD-03/4.2/row` row_new (ADD-03:4.2, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/4.2/row` as an UNVERIFIED reference — its obligation is proposed downstream as ADD-03-4.2-01 (row_new, interpretation_pending) (task(s) ana:ADD-03/4.2/row; PROPOSED): no op or disposition answers the provision; a person confirms the row and the provision's disposition
- `ADD-03/4.3/row` row_new (ADD-03:4.3, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/4.3/row` as an UNVERIFIED reference — its obligation is proposed downstream as ADD-03-4.3-01 (row_new, interpretation_pending), DS-ADD03-4.3-ev (evidence_item, evidence_verified), DS-ADD03-4.3-act (activity, interpretation_pending) (task(s) ana:ADD-03/4.3/row; PROPOSED): no op or disposition answers the provision; a person confirms the…
- `ADD-03/4.3/q-count` clarification (ADD-03:4.3, interpretation_pending): an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; the downstream phase proposes issues and clarification entries against the candidate
- `ADD-03/Q17/row-dscr` row_new (ADD-03:Q17, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/Q17/row-dscr` as an UNVERIFIED reference — its obligation is proposed downstream as ADD-03-Q17-01 (row_new, interpretation_pending), DS-ADD03-Q17-issue (issue, interpretation_pending) (task(s) ana:ADD-03/Q17/row-dscr; PROPOSED): no op or disposition answers the provision; a person confirms the row and the provision's disposition
- `ADD-03/Q17/issue` issue (ADD-03:Q17, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-Q17-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ADD-03/Q18/issue` issue (ADD-03:Q18, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-Q18-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ADD-03/Q18/question` clarification (ADD-03:Q18, interpretation_pending): an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; the downstream phase proposes issues and clarification entries against the candidate

## Coverage

- provisions: 57; accounted for by the combined set: 54; states {'validated': 57}
- accounted for through downstream tasks (analysis rows carried; never a silent gap): 3 ADD-03:3.6 → ana:ADD-03/row/3.6; ADD-03:4.2 → ana:ADD-03/4.2/row; ADD-03:4.3 → ana:ADD-03/4.3/row
- the analysis ITEMS' resolution by the controller (items, not provisions; session 14): resolved 23, pending 31, invalid 0, unaccounted 3; approved 0
- structural units of ADD-03 that are not provisions (listed so nothing is dropped): ADD-03:H:cover (heading), ADD-03:H:cover-2 (heading), ADD-03:H:S1 (heading), ADD-03:H:S2 (heading), ADD-03:H:S3 (heading), ADD-03:H:S4 (heading), ADD-03:H:S5 (heading), ADD-03:S5/QA (table), ADD-03:H:AppA (heading), ADD-03:region:ADD-03-p3-r1 (region), ADD-03:p3-image (table), ADD-03:H:AppB (heading), ADD-03:T42-1 (table)
- batches: reading-ADD-03-p3-r1 done, analysis-001 done, analysis-002 done, analysis-003 done, analysis-004 done, analysis-005 done, analysis-006 done, downstream-001 done, downstream-002 done, downstream-003 done, downstream-004 done

## Critic (a second model over the selected items; it changed no status)

**Agreement between the critic and the proposer is not approval**: every item still needs a person's decision, and a disagreement is a concern for that person, not a rejection. The critic reviews only the selected classes (consequential interpretations, uncertain targets, removals, conflicting evidence), in one request per batch.

| Batch | Critic | Selected | Reviewed | Agrees | Does not agree | Note |
|---|---|---|---|---|---|---|
| analysis-001 | done | 4 | 4 | 4 | 0 |  |
| analysis-002 | done | 5 | 5 | 2 | 3 |  |
| analysis-003 | done | 11 | 11 | 11 | 0 |  |
| analysis-004 | done | 12 | 12 | 6 | 6 |  |
| analysis-005 | done | 6 | 6 | 4 | 2 |  |
| analysis-006 | done | 6 | 6 | 4 | 2 |  |
| downstream-001 | done | 3 | 3 | 2 | 1 |  |
| downstream-002 | done | 2 | 2 | 1 | 1 |  |
| downstream-003 | done | 1 | 1 | 0 | 1 |  |
| downstream-004 | done | 1 | 1 | 0 | 1 |  |

- **ADD-03/cover/para3** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The core reading holds up. The cover summarises, and its sentence 'Bidders shall acknowledge receipt in Form 4-A.' is the only one that sets a duty of its own, so annotating it as adds_obligation follows from the words.
    - concern: The rationale says the cover's 'SAR 4,000,000' conflicts with operative Section 2.1 and refers to a separate issue. That cannot be checked from the evidence shown. Section 2.1 (quoted only in S-F1) says the amount 'is reduced by SAR 1,000,000'. The cover says the threshold is reduced 'to SAR 4,000,…
    - concern: The rationale notes that the VOL-IV:F4-A group is superseded at ADD-02 and was reissued by ADD-01 Appendix A. So 'Form 4-A' in this cover may now mean the reissued form. The annotation names neither the reissued form nor its field 'Addenda acknowledged (numbers):' (ADD-01:AppA/addenda-acknowledged-…
    - concern: The other sentences in the cover are treated as summary handled elsewhere, but this cannot be confirmed from the evidence shown. They include 'takes precedence in accordance with Volume I Clause 3.2', 'All other terms of the RFP Documents remain unchanged', the invitation to address Table 42-1, and…
- **ADD03-ACK** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The requirement is quoted word for word from ADD-03:cover/para3. Recording the consequence as none_stated is correct, because the unit states no consequence.
    - concern: The rationale says VOL-I:9.3 is about signing Form 4-A. That unit is not printed here, so the claim cannot be checked. It does not affect the row, since no consequence is inferred from it.
    - concern: The row should name the reissued Form 4-A field ADD-01:AppA/addenda-acknowledged-numbers (VOL-IV:F4-A is superseded at ADD-02) as a dependent or evidence item. That is the form the bidder will actually fill in.
- **ADD-03/2.2** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The provision prints an obligation and does not change the words of Form 4-F, so an adds_obligation annotation on ADD-03:2.2 follows from the text. The dependency on ADD-03/2.1 is correct. The annotation does not itself name the Form 4-F Availability Payment field as a dependent; the paired row ADD…
- **ADD03-2.2** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The requirement is quoted word for word, and no consequence is stated or inferred.
    - concern: The interpretation note calls Section 2.1 a reduction of 'the Change in Law compensation threshold'. That wording comes from the cover summary. The operative words in S-F1 are only 'The amount stated in Volume V Clause 36.2 is reduced by SAR 1,000,000.', and the text of Clause 36.2 is not shown. Th…
    - concern: Some listed dependents cannot be checked against the evidence shown: 'Financial Model' and 'VOL-IV:F4-F/para1 confirmation'. Only the Form 4-F Availability Payment field is quoted.
    - concern: The 'medium' confidence depends on the cover/operative discrepancy. As noted under the cover item, that discrepancy has not been shown from 36.2's effective text and a computed figure.
- **ADD-03/3.2** (analysis-002; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The no_effect reason depends on a relocation of VOL-II:8.5 in ADD-03:3.1 (op ADD-03/3.1), but neither ADD-03:3.1 nor that op is printed in the request. I cannot check that 8.5 is relocated rather than deleted or replaced, so I cannot check that the sentence only confirms the numbering.
    - concern: 'The number 8.5 is not reused in Volume II' does more than describe: it sets a lasting rule that number 8.5 stays vacant in Volume II. Whether that rule needs recording (for example as a note on the vacated number) or truly has no effect is a person's decision. Under the shared rules, a no_effect w…
    - concern: The controller's semantic check found no amendment words only after setting aside 'the sentences that say nothing changes'. Here that set-aside sentence is the whole provision, so the check confirms little.
- **ADD-03/3.4(b)** (analysis-002; controller status **escalated**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The escalation is classed as a software limitation and blames the engine's failure to match Arabic-Indic '٤٢-١' to 42-1. But the engine's recorded refusal says 'its id and title name another', and that full record is not in the request. The stated cause is the proposer's guess, so I can't confirm i…
    - concern: The rationale says the crop shows 'a letter of the Asset Transfer Committee No. ٤١٧/٢٠٢٦ dated ١٥ نوفمبر ٢٠٢٦م' around the table. That letter text (its sender, number and date) is not quoted as evidence or raised as a point anywhere. It is attachment content that is not accounted for, and it may be…
    - concern: Escalating the insertion to Document control, and declining to insert the English group because of ADD-03:3.5, is consistent with the printed words.
- **ADD-03/3.5** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The text of ADD-03:T42-1 (the English Appendix B group) is not printed in the units, so I cannot independently check it as the 'over' target. The annotation correctly quotes 'The Arabic text governs.' and stays interpretation_pending for a person.
- **ADD-03/issue/3.5** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: S-F4 is labelled a fact but says the English note (4) 'amends Volume II Clause 2.2'. Whether it amends anything is one of the readings the issue itself leaves open, so that part is an interpretation, not a fact.
    - concern: The Arabic row labels for rows 4 and 5 are not quoted as evidence; only the value cells are. The class names in the issue text are taken from the English translation.
    - concern: The owner is Technical, but the open questions are which rendering binds and whether an English-only note amends Volume II Clause 2.2. Those also read on precedence, which may need Legal as decision owner.
    - concern: The committee-letter text in the same crop (No. ٤١٧/٢٠٢٦, dated ١٥ نوفمبر ٢٠٢٦م) is not mentioned.
- **ADD-03/row/3.6** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The row states assessment 'pass_fail', but its own confidence_reason says 'whether it is pass/fail or scored is not stated in ADD-03:3.6'. The classification has no basis in the pack's words. It should stay unresolved or be clearly marked as a proposal or assumption, not set as the row's value.
    - concern: The row's evidence list is empty, while the rationale names a Technical Proposal lifecycle-plan section as the evidence item. That evidence item should be recorded or listed as follow-on work for A5.
    - concern: The verbatim quote, 'none_stated' consequence, ADD-03 introduction stage and cross-reference to the Arabic/English difference are consistent with the printed words.
- **ADD-03/p3-image/r1** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The table qualifier 'يجب ألا يقل العمر المتبقي' creates an obligation, so this no_effect is for a person to decide. The reason says so, and the status interpretation_pending is right. The controller's semantic check found no obligation words, but it read only the row text, not the qualifier.
    - concern: The rationale checks the Arabic against the English translation. That is fine as a cross-check only. A translation is never evidence for the source, so the reading must rest on crop r01 and the cell crops.
    - concern: The reason names no dependants beyond 3.4. The row's obligation will need an A1 row, and the Section 3.6 lifecycle plan relies on it. This should be listed as follow-on work, as note3 does.
    - concern: ADD-03:3.4's insert_table op is in another batch and is not shown here, so I cannot confirm the row actually enters the state through it.
- **ADD-03/p3-image/r2** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: Same as r1: the table's obliging qualifier makes this no_effect a person's decision, and the item correctly leaves it pending.
    - concern: Matching against the English row 2 is corroboration only, not evidence for the Arabic.
    - concern: Follow-on A1 and lifecycle-plan dependants are not listed.
    - concern: I cannot check 3.4's insert_table op, which is in another batch.
- **ADD-03/p3-image/r3** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: Same as r1: the table's obliging qualifier makes this no_effect a person's decision, and the item correctly leaves it pending.
    - concern: Matching against the English row 3 is corroboration only, not evidence for the Arabic.
    - concern: Follow-on A1 and lifecycle-plan dependants are not listed.
    - concern: I cannot check 3.4's insert_table op, which is in another batch.
- **ADD-03/p3-image/note1** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The note refers to 'مقياس الهيئة لتصنيف حالة الأصول' (the Authority's five-grade condition scale). The item does not say whether that scale is supplied in the pack. If it is not, this is missing evidence and should be recorded as such.
- **ADD-03/p3-image/note2** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The reason says the condition survey 'is the subject of ADD-03:3.1 (Clause 42.3)'. ADD-03:3.1 is not printed in this request, so I cannot verify that cross-reference.
    - concern: The note gives the Independent Engineer a role in setting residual life. Possible A1 and A5 dependants, such as the condition survey activity, are not listed.
- **ADD-03/p3-image/note3** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The note obliges replacement at the Project Company's cost, so a no_effect is a person's decision. The item correctly flags this and lists the A1 follow-on work.
    - concern: The scope of the replacement obligation depends on the open row 4 and row 5 values. ISS-ADD03-T42-1-r4 and ISS-ADD03-T42-1-r5 should be named as dependencies.
- **ISS-ADD03-T42-1-r4** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Section 3.5 says 'The Arabic text governs.', so the Arabic is not itself unclear. This is a discrepancy between the Arabic and the translation. Keeping it open is still right, because deciding which text governs belongs to a person.
    - concern: The open question is about the governing-language clause, so Legal should probably share ownership with Technical.
- **ISS-ADD03-T42-1-r5** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The ambiguity is real within the Arabic alone: the cell says 'شهراً' (months) under a column headed 'سنة' (years). The 24-years reading should rest on the Arabic column heading. Citing the translation as support for a reading of the source goes against 'a translation is never evidence for the sourc…
    - concern: Unlike the r4 issue, this one lists no dependants. It should name note ٣'s replacement obligation, the Section 3.6 lifecycle plan and any A1 row.
- **ISS-ADD03-T42-1-note4** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Reading (b) would amend Volume II Clause 2.2. That unit is not named as a target, and its effective text at ADD-02 is not quoted, so a person cannot see what would change.
    - concern: The provision is cited as note3 and the target as the whole table, while the note (4) provision sits in another batch. The tie between this issue and that provision should be made explicit.
    - concern: The absence of an Arabic note ٤ rests on the proposer's crop observation. Only note ٣ is quoted as evidence, and I cannot check the absence myself.
    - concern: Dependants are not listed: the design-life basis in Volume II 2.2 and any A1 or A5 items for electrical design life.
- **ISS-ADD03-cover-four-classes** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The open question suggests a possible resolution ('e.g. if row 5 applies only where provided'). It leans toward one reading and would be better stated neutrally.
- **Q-ADD03-T42-1-r4-r5** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Part (c) cites note (4) and the gap cites Section 3.5, but neither ADD-03:T42-1/note(4) nor ADD-03:3.5 is in the item's own evidence list. S-F3 is also missing from its statements.
    - concern: 'Handback cost allowance' in practical_impact is not quoted from any unit in the pack. It should be tied to pack words or dropped.
    - concern: The Section 3.6 lifecycle plan text is not printed here, so I cannot verify it.
    - concern: Part (b) puts the translation alongside the column heading as a basis for the 24-years reading. The Arabic heading alone is enough.
- **D-T42-1-1** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The reason quotes the Arabic asset class "المنشآت المدنية والخرسانية" and "أقصى درجة للحالة: ٢", but these words are not in the item's evidence. The only Arabic quotation in the evidence, which the controller verified, is "الحد الأدنى للعمر المتبقي (سنة): ٢٠". Unit ADD-03:p3-image/r1 is not printed…
    - concern: A no_effect disposition for a convenience-translation row depends on that row matching the governing Arabic row. Here the match rests on S-I2, an interpretation with no evidence that is still pending a person, so the disposition cannot be confirmed from the evidence shown.
    - concern: The reason says "The row enters Volume V with the Arabic table under ADD-03:3.4" without quoting ADD-03:3.4. That clause is not in the evidence.
- **D-T42-1-2** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The reason quotes "خط نقل المياه المعالجة" and grade ٢ from the Arabic row, but neither is in the evidence. Only the residual-life cell "الحد الأدنى للعمر المتبقي (سنة): ٢٠" is quoted and verified. Unit ADD-03:p3-image/r2 is not printed, so the claim that the values agree can be checked for residua…
    - concern: The no_effect depends on S-I2, an interpretation with no evidence that is pending a person.
- **D-T42-1-3** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The reason quotes "المعدات الميكانيكية" and grade ٣ from the Arabic row, but neither is in the evidence. Only "الحد الأدنى للعمر المتبقي (سنة): ٥" is quoted and verified. Unit ADD-03:p3-image/r3 is not printed, so the grade cannot be checked.
    - concern: The no_effect depends on S-I2, which is pending a person.
- **D-T42-1-4** (analysis-004; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-opus-5-5
    - concern: S-F2 is labelled a fact, but the Arabic figure ٧ comes from reading an image. Its standing should match S-I1 (a reading pending approval) unless that reading has been validated.
    - concern: Strictly, this is a conflict between two renderings where the pack states which one governs (ADD-03:3.5 "The Arabic text governs."), rather than a pure ambiguity of words. The proposer correctly applies the rule but does not decide it, and leaves the decision to a person. That is acceptable, but th…
    - concern: Follow-on effects (A1 rows and A5 lifecycle-plan activities that rely on the E&I residual life) are not listed in the item.
- **ISS-T42-row4** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The issue calls the Arabic row "governing". This follows ADD-03:3.5, but the open question should stay neutral about whether that rule is applied.
    - concern: The issue cites ADD-03:3.6, which is not quoted in the evidence.
    - concern: The target ADD-03:p3-image/r4 is the Arabic counterpart of the provision rather than a unit the provision cites. That is reasonable for an issue, but a person should note it.
- **D-T42-1-5** (analysis-004; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-opus-5-5
    - concern: Two separate points are combined in one reason: the months/years discrepancy, and the cover's "four asset classes" against five printed rows. The cover summarises and does not amend, so the four/five point is a cover-vs-operative difference and would be better kept as its own point.
    - concern: S-F3 treats the Arabic image reading as a fact; it should be confirmed as a validated reading.
    - concern: ADD-03:cover/para3 is not printed among the units. Its quotation was verified only on ISS-T42-row5.
    - concern: Follow-on effects on the membrane replacement allowance and lifecycle-plan activities are not listed.
- **ISS-T42-row5** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: One issue combines two open questions that are independent: months vs years for membranes, and four vs five classes. Splitting them would let each be decided on its own.
    - concern: The issue calls the Arabic cell "governing". It should stay neutral about whether ADD-03:3.5 is applied.
    - concern: Technical as the owner is plausible, but which rendering governs is also a Legal point.
- **Q-T42-row5** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Part (c) tells the Authority that Note (4) "has no counterpart in the Arabic table". That rests on S-I1, an image reading still pending approval. The draft should not assert it until the reading is confirmed.
    - concern: The evidence list omits ADD-03:p3-image/r4 and ADD-03:p3-image/r5 and the cover quotation; these come in only through the statements.
    - concern: The question bundles four separate points under the row 5 provision, so its traceability to rows 4 and note (4) is indirect.
    - concern: It remains a DRAFT, and a person decides whether to send it.
- **D-T42-1-note1** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The reason quotes Arabic note ١ in full, but no evidence item, crop hash or controller check covers that text, and ADD-03:p3-image/note1 is not printed. The quotation cannot be verified.
    - concern: The no_effect depends on S-I2, which is pending a person. Note (1) is definitional, which supports no_effect, but whether it matches the Arabic is not shown.
- **D-T42-1-note2** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The Arabic note ٢ quoted in the reason is not in the evidence and was not verified by the controller. ADD-03:p3-image/note2 is not printed.
    - concern: The no_effect depends on S-I2, which is pending a person.
- **D-T42-1-note3** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The words create an obligation ("shall be replaced at the Project Company's cost before the date of transfer"), so a no_effect is a person's decision, as the controller flags.
    - concern: The Arabic note ٣ quoted in the reason is not in the evidence and was not verified. ADD-03:p3-image/note3 is not printed.
    - concern: "A post-award contractual obligation" is a characterisation that the pack's words do not state.
    - concern: ADD-03:3.4 is cited without a quotation.
    - concern: "does not meet this Table" depends on the unresolved rows 4 and 5 (D-T42-1-4 and D-T42-1-5). This dependency is not named.
    - concern: The A1 follow-on is mentioned only in the rationale and is not proposed.
- **D-T42-1-note4** (analysis-004; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-opus-5-5
    - concern: The declared conflict names the whole image, ADD-03:p3-image, rather than a unit id. The conflict rests on the absence of a note, read under S-I1, which is still pending approval. If that reading is not confirmed, the point is partly missing evidence rather than ambiguity.
    - concern: Reading 1 could also turn on whether note (4), which amends Volume II, counts as "text of Table 42-1" at all for the purposes of "The Arabic text of Table 42-1 at Appendix A governs." This could be stated for the person deciding.
    - concern: The VOL-II:2.2 quotation is verbatim. Leaving it unchanged pending Legal is correct.
    - concern: The dependants named in the rationale (A1 design-life rows and lifecycle-plan activities) are listed but not proposed. The link to the row 4 E&I residual-life conflict is not named.
- **ADD-03/4.1** (analysis-005; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-opus-5-5
    - concern: The follow-on list cites VOL-V:3.3 and 'Form 4-E deviations', but neither unit is printed in this request. That dependency can't be checked here.
    - concern: The provision limits its definition with 'In this Clause, the Geotechnical Baseline Report means Revision C...'. ADD-03:4.2 and 4.3 use the same term outside Clause 12.5, so whether they mean Revision C is open. This should be listed as follow-on work for those rows.
- **ADD-03/4.1/issue-gbr** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The claim that no report with that name or revision is in the pack rests on a search ('hits only in ADD-03:4.1-4.4') that isn't shown here, and ADD-03:4.4 isn't printed. The controller records check the quotations, not that the report is absent. The request doesn't show enough to confirm the 'insuf…
    - concern: The gap says 'ADD-03:4.2 and 4.3 rely on it', but the definition is limited by 'In this Clause'. Whether 4.2 and 4.3 mean Revision C is a separate ambiguity. It is folded into a missing-evidence item instead of being raised as its own 'ambiguous:' point.
    - concern: Whether the GBR Revision C is the same document as ADD-01:Q4's 'geotechnical report in the data room' is also an ambiguity, not missing evidence. The question asks about it, which is right, but the gap doesn't classify it.
- **ADD-03/4.1/issue-q4** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Reading 1 relies on 'ADD-03 (which takes precedence under ADD-03:1.1)', but ADD-03:1.1 isn't quoted or printed. The precedence premise has no evidence and leans the issue toward one answer.
    - concern: Reading 1 also says VOL-V:3.3's 'the term' does not touch the Scheduled PCOD. No definition of 'term' or 'Scheduled PCOD' is quoted, so this is an unsupported reading, not a fact.
    - concern: Reading 2 combines two separate questions: how far ADD-01:Q4 still applies, and whether VOL-V:3.3 needs a conforming change. Each should be stated as its own question with its own readings.
    - concern: The issue describes a tension, but its conflicts field is empty.
    - concern: ADD-01:Q4 refers to 'the geotechnical report in the data room', and Clause 12.5 refers to the GBR Revision C. Nothing shown establishes that they are the same document, and the issue's readings assume a link between them.
- **ADD-03/4.2/row** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: confidence_reason assumes the report referred to in 4.2 is 'Revision C'. The definition in ADD-03:4.1 is limited to 'this Clause' (12.5), so that link is an interpretation and should not be stated as fact.
    - concern: The rationale cites ADD-03:cover/para3 and VOL-I:9.7, but neither is printed here, so I couldn't check that the cover matches or that 9.7 is unaffected.
- **ADD-03/4.3/row** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The date rule notes give typed dates (2026-11-19 / 2026-11-22 / 2026-11-23) said to come from calculate. No calculate record appears in the controller validation shown, and VOL-I 2.4 (said to make the backward count a single reading) isn't printed. These can't be checked here.
    - concern: S-I2 says 'Planning uses the conservative 19 November 2026 pending a person'. That is a planning choice and should be labelled 'PROVISIONAL ASSUMPTION:' with its basis, not left in an interpretation statement.
    - concern: Q19's 'the period stated in that Section' could refer to the request period or the appointment window, since Section 4.3 states both. It most likely means the request period, but tying the 'lesser' consequence to the request deadline is itself an interpretation.
    - concern: ADD-03:Q19 is cited as a unit but isn't printed under units. Its text is only available through S-F6.
- **ADD-03/4.3/q-count** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: interim_handling ('Plan to request by Thursday 19 November 2026 (conservative reading)') is a planning assumption and should be labelled 'PROVISIONAL ASSUMPTION:' with its basis.
    - concern: Both dates are said to come from calculate, but no calculate record appears in the controller validation shown. The claim that VOL-I 2.4 covers only backward counting can't be checked because that unit isn't printed.
    - concern: The anchor treats 'the date of this Addendum' as the printed 'Issued 17 November 2026'. That is reasonable on the evidence shown, but it is an assumption, and the gap doesn't state it.
- **ADD-03/Q15** (analysis-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The response's first statement ('The minutes are issued in English only.') is about the language of the minutes. The item shows no check of whether any language or translation clause in the pack bears on Appendix B. If one exists, it is a dependency that has not been named.
    - concern: ADD-01:AppB is listed as a dependency but is not printed in the evidence, so I could not check it.
- **ADD-03/Q17(a)** (analysis-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group; model claude-opus-5-5
    - concern: The annotate/interprets op on VOL-I:10.1 and VOL-I:10.6 is supported by the words 'forms part of Form 4-F and shall be attached to it in Envelope B'. However, the rationale says the response 'settles where the schedule goes' and 'does not breach the 'only' rule in 10.1'. That treats the apparent co…
    - concern: 'shall be attached to it in Envelope B' puts a placement obligation on the bidder that 10.6 ('submit with Form 4-F') does not state. The effect may be 'adds_obligation' rather than plain 'interprets'. A person should confirm which.
    - concern: The third sentence of the response ('A schedule placed in Envelope A will be treated in accordance with Volume I Clause 6.2.') is not covered by this op. It is raised only through the row's issue (ADD-03/Q17/issue), and that issue is not shown here.
    - concern: S-Q17-fact quotes VOL-I:6.2. That unit is not printed in the request's units, and the controller records no verbatim check for it in this item, so the quotation is unverified.
    - concern: VOL-IV:F4-F is named as a dependency but not printed. I could not check whether Form 4-F already provides for an attachment.
- **ADD-03/Q17(b)** (analysis-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The annotate/adds_obligation op on VOL-I:10.6 is supported by 'The schedule shall also state the minimum annual debt service cover ratio assumed.' However, the rationale's follow-on says 'the financial model and the Form 4-F schedule must include the DSCR figure'. The response names only 'The sched…
    - concern: S-Q17-fact quotes VOL-I:6.2, which is not printed in units and was not verified by the controller in this item.
- **ADD-03/Q17/row-dscr** (analysis-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The requirement is quoted verbatim from ADD-03:Q17. Setting the consequence to 'none_stated' and handing the Envelope A / 6.2 point to an issue is consistent with not inferring a consequence.
    - concern: assessment 'pass_fail' is not stated in the evidence shown. If it is a default, it should be labelled as a provisional reading.
    - concern: The note quotes VOL-I:6.2. That text is not printed in the request's units, and the controller records no verbatim check of it, so the quotation is unverified here.
    - concern: The row's own 'evidence' list is empty. The items the bidder must produce (the schedule, with DSCR, attached to Form 4-F) are not listed for A5.
- **ADD-03/Q18** (analysis-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: S-Q18-fact says 'VOL-I:3.1 lists the RFP Documents without naming a Direct Agreement'. VOL-I:3.1 is not printed in the units, and the controller has no verbatim check of it, so I cannot verify the quotation or the inference.
    - concern: Only the lead-in of VOL-I:3.2 is shown, not the precedence list, so whether a Direct Agreement falls within it cannot be checked. Correctly, the point stays an ambiguity for Legal.
    - concern: The third sentence ('The Direct Agreement will be negotiated with the Senior Lenders after the Preferred Bidder Notification.') is not reflected in the note. Its follow-on, if any (A5 or Commercial), is not listed.
    - concern: The referenced issue and draft clarification (ADD-03/Q18/issue) are not shown.
- **ADD-03/Q19** (analysis-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The target ADD-03:4.3 is identified with certainty: Q19 names 'Section 4.3 of this Addendum'.
    - concern: 'Requests made after the period stated in that Section will not be accommodated' attaches a consequence that 4.3 does not print. The effect may be better recorded as adding a (non-bid-out) consequence on the 4.3 row than as 'interprets' alone. It is correctly kept out of A3.
    - concern: The follow-on names only the 'within three (3) Working Days of the date of this Addendum' rule. It omits 4.3's second date rule, 'not later than three (3) Working Days before the Proposal Due Date', which the A5 programme also needs.
- **DS-03** (downstream-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The interpretation's `quote` gives the prohibition with no qualification. The ADD-03:4.4 exception appears only in the free-text `note`. A1 or A3 output that uses just the quote and the disqualification consequence would overstate the prohibition at ADD-03. The exception should travel with the row …
    - concern: The exception only applies 'during an appointment under Section 4.3'. Section 4.3 (presumably ADD-03 Section 4.3) is not printed here, and `dependencies` is empty. The window and the appointment it depends on should be listed as a dependency, as change propagation requires.
    - concern: The rationale says the date rules BLACKOUT-START and BLACKOUT-END 'carry over unchanged'. No evidence for those rules is shown here, so I could not check that statement.
    - concern: The note correctly leaves to a person (Legal / Bid management) whether a particular communication falls inside the exception. It also correctly keeps the text of VOL-I:4.2 unchanged and does not widen the carve-out beyond 'identification and handling of cores and records'.
- **DS-07** (downstream-001; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
    - concern: The parameter `threshold_sar: 1500000` and the quote 'exceeds SAR 1,500,000' record Reading 1 as the row's value. The proposer's own declared ambiguity (I-ADD03-CIL-THRESHOLD, S-36.2-WHICH) is still pending a person. The figure should be marked as provisional on that issue, or left unresolved, rath…
    - concern: S-36.2-WHICH's Reading 2 relies on a BASE figure of 'SAR 5,000,000'. That figure is not in any evidence printed here. Only the ADD-02 effective text (SAR 2,500,000) is shown, so Reading 2's basis cannot be checked.
    - concern: The cover says the threshold is reduced 'to SAR 4,000,000', but the ADD-02 effective figure is SAR 2,500,000. Measured against that text, 4,000,000 would be an increase, so the cover's wording is also inconsistent with its own word 'reduces'. Neither the item nor S-36.2-WHICH says this, and it is r…
    - concern: S-PAE-STALE says row VOL-V-36.2-01 still cites SAR 2,500,000. Its only evidence is ADD-03:3.4, which concerns a different clause and row (VOL-V-42.1-02). No evidence is shown for the claim about the 36.2 row.
    - concern: The consequence 'none_stated' fits VOL-V:36.2 as shown, which states no rejection or disqualification.
- **DS-08** (downstream-001; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-opus-5-5
    - concern: The issue is correctly framed as an ambiguity. It quotes both the cover and Section 2.1, states both readings, names an owner and leaves the decision to a person. That matches the rule that the cover summarises and the difference is reported, not resolved. Since the point turns on which figure gove…
    - concern: The controller's 'applied rule' and 'consistency (phases)' records treat VOL-I 3.2 as settling the point in favour of the operative provision. The only part of VOL-I 3.2 shown is its lead-in ('the following order of precedence shall apply, the first named prevailing:'); the order itself is not prin…
    - concern: The issue cites ADD-03 1.2 (references read as amended by Addenda Nos. 1 and 2) and ADD-03 2.2 / Form 4-F (Availability Payment price assumption). Neither is printed in this request, so those dependency claims could not be checked.
    - concern: The issue should also say that, against the ADD-02 figure of SAR 2,500,000, the cover's 'reduces ... to SAR 4,000,000' would be an increase.
    - concern: show_in_a3 false is consistent: neither unit states a bid-out consequence.
- **DS-ADD03-4.3-row** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The consequence comes from ADD-03:Q19, quoted as 'Requests made after the period stated in that Section will not be accommodated.' Q19 is not printed under `units`. That means I cannot check from the evidence shown that 'that Section' refers to ADD-03 Section 4.3, or that the quotation is complete.…
    - concern: The interpretation note says 'VOL-I 4.2 is disapplied for the communications described in ADD-03 4.4.' Neither VOL-I 4.2 nor ADD-03 4.4 is printed. The point does not come from ADD-03:4.3, and it brings another clause into this row. That widens the row beyond what its provision names. It should be …
    - concern: The forward-counting date rule is marked 'ambiguous counting' and also 'Escalated'. The stated reason is that 'VOL-I 2.4 covers backward counting only', meaning no approved method covers forward counting. That reason points to a software limitation (no approved method) or a gap in the pack's counti…
    - concern: The note calls the reading that counts the issue day 'conservative planning'. That leans toward one reading. If the planning tools or A5 use 2026-11-19, it should be labelled 'PROVISIONAL ASSUMPTION:' with its basis. Otherwise the reading is in effect being chosen.
    - concern: The anchor 'Issued 17 November 2026' (ADD-03 cover) and the Proposal Due Date of 2026-11-26 (VOL-I:6.1 at ADD-03) are not printed in this request. The computed values rest only on statement downstream-002/S-F-4.3-DATES.
    - concern: The 'requirement' quotes only the first sentence of 4.3, which is right for the Bidder's obligation. The second sentence, about when appointments are held, is the Authority's undertaking. It is kept only as a date rule and in the note. I see no problem with that, provided it is never presented as a…
- **DS-ADD03-Q17-issue** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The issue's owner is 'Commercial', but statement S-I-Q17-6.2 says 'Commercial/Legal'. Whether VOL-I 6.2 applies to the schedule is partly about what 'other commercial information' means. Legal should probably be named as a co-owner, or the difference should be reconciled.
    - concern: Q17 also adds an obligation: 'The schedule shall also state the minimum annual debt service cover ratio assumed.' It also says the schedule 'forms part of Form 4-F and shall be attached to it in Envelope B.' This issue does not cover either point. Check that each is captured as its own register row…
    - concern: The bidder's question points to a tension between VOL-I 10.1 ('no document other than Form 4-F and the Financial Model') and VOL-I 10.6. Whether Q17's answer settles that tension is for a person to decide. No item shown here records it. Neither VOL-I 10.1 nor 10.6 is printed.
    - concern: Only the quoted span of VOL-I:6.2 is printed, not the full clause. I relied on the controller's verbatim check for it.
    - concern: Both readings are fairly drawn from the words quoted, and no reading is chosen. 'show_in_a3' is false, which is right while the reading is still pending.
- **DS-APPB-ESC** (downstream-003; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
    - concern: The item calls this an ambiguity, but the words it relies on are not unclear about which text binds. The statement it relies on (downstream-003/S-F-3.5) quotes ADD-03:3.5 in full: 'The Arabic text governs. The English translation at Appendix B is provided for convenience only.' The item's own evide…
    - concern: The controller's consistency check failed: this item reverses ADD-03/issue/3.5, which applied 'The Arabic text governs.' The shared rules allow an earlier reading to be reopened only when its evidence or a dependency changes, and then the change must be quoted. The item quotes no such change. A per…
    - concern: The Arabic values the item cites (row 4 '٧', row 5 '٢٤ شهراً') and the claim that note (4) 'has no Arabic counterpart' have no supporting evidence. No Arabic unit is cited and every crop_sha256 is null. The rationale does not say what any image showed. The units printed for this review include only…
    - concern: The scope is wider than the named provision. The item names ADD-03:T42-1/4 as its provision, but it also covers T42-1/5 and note (4). Its evidence has nothing for row 4's Arabic value and no record for note (4) beyond a statement it relies on.
    - concern: Note (4) appears only in the English text, yet it reads as a change: 'The design life of electrical equipment stated in Volume II Clause 2.2 is increased to twenty-five (25) years.' If the Arabic text really has no counterpart, the point is a separate one: does the translation amend anything? It sh…
    - concern: The classes are mixed. The reason begins 'ambiguous:', but the escalation's what_is_unsupported field says 'nothing is unsupported by the software'. By the item's own account this is an interpretation pending a person, which belongs in an issue, not a software-limitation escalation.
    - concern: The item states several things that the evidence shown does not support: 'now that the window has closed' (no evidence about a clarification window is cited), 'No price row is reached directly', and that VOL-V:42.1 and VOL-II-2.2-01/-02 are affected. These should be quoted or listed as dependencies…
    - concern: The downstream effects (the lifecycle plan under ADD-03:3.6, CQ-HANDBACK-CONDITION) rest on downstream-003/S-I-CONDITIONAL, an interpretation with no evidence that a person must still confirm.
- **DS-READ-ROW** (downstream-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: insufficient evidence: the request does not print the reading for rows r1, r2 and r3 or for note1. Only r4, r5, note2, note3 and the intro sentence are quoted. So I cannot check the life values ٢٠, ٢٠ and ٥, the grades ٢, ٢ and ٣, or the grade-scale note against the evidence. The crop sha is cited,…
    - concern: Who decides: Legal. The row takes the Arabic values as the operative ones: row 4 is ٧ rather than 5, and row 5 is ٢٤ شهراً rather than 24 years. It also calls Appendix B 'the translation' and 'not evidence'. The only support shown is the three words 'The Arabic text governs.' from ADD-03:3.5. That …
    - concern: Possible mismatch over which appendix holds the table. Provision ADD-03:3.4 says 'Table 42-1 is reproduced at Appendix A to this Addendum and forms part of Volume V.' The row reads the table from the Arabic image on p3 and calls the English version on p4 'Appendix B'. The request does not show whet…
    - concern: The 'requirement' field is an English paraphrase of the Arabic. It adds content, such as 'condition grade not worse than the maximum stated', that is not in the quoted intro sentence. That content comes from the column heading 'أقصى درجة للحالة', which needs the r1–r5 crops to check. The paraphrase…
    - concern: Follow-on work is not listed, and 'dependencies' is empty. 3.4 deletes 'with a remaining design life of not less than five (5) years for all major assets', so any existing A1 row built on that wording is superseded and should be named. ADD-03:3.6 (lifecycle plan in the Technical Proposal) depends o…
    - concern: Minor: the row's scope is ['proposal'] but its assessment is contractual_post_award, and it is off A3 and A5. The scope and the assessment do not match.

## Requests: failures, deferrals, repairs and route notices

- **analysis-001** (done): 1 failed call(s) (rate_limit); DEFERRED 2026-10-07T16:24:35Z: host rate limit (the host ended with an error (success: 429) You've hit your session limit · resets 5:40pm (UTC)); the host names a reset in 4527.1 s, beyond 300 s (reset named in about 75 min)
- **analysis-002** (done): 1 failed call(s) (rate_limit); DEFERRED 2026-10-07T16:24:35Z: host rate limit (the host ended with an error (success: 429) You've hit your session limit · resets 5:40pm (UTC)); the host names a reset in 4527.7 s, beyond 300 s (reset named in about 75 min)
- **downstream-002** (done): repaired once (1 problem(s) before the re-ask)

Route notices (how the requests were served; they change no status):
- **capabilities_declared** (reading-ADD-03-p3-r1): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the reading request wa…
- **capabilities_declared** (analysis-001): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request w…
- **capabilities_declared** (analysis-002): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request w…
- **capabilities_declared** (analysis-003): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request w…
- **capabilities_declared** (analysis-005): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request w…
- **capabilities_declared** (analysis-006): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request w…
- **capabilities_declared** (downstream-001): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request…
- **capabilities_declared** (downstream-002): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request…
- **capabilities_declared** (downstream-003): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request…
- **capabilities_declared** (downstream-004): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request…

## Manual interventions (the person's actions)

- 2026-10-07T17:43:24Z: resume (the person's action) by a person (tenderpack ai resume, or the panel's Resume); process 1143; status before: running
- 2026-10-07T18:26:51Z: resume (the person's action) by a person (tenderpack ai resume, or the panel's Resume); process 627; status before: running

### What the run did with them, and its automatic host sessions (not a person)

- 2026-10-07T16:23:55Z: host session (automatic) — batch reading-ADD-03-p3-r1 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session reading an image; not a person
- 2026-10-07T16:24:35Z: host session (automatic) — batch analysis-001 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session over the MCP tools; not a person
- 2026-10-07T16:24:35Z: host session (automatic) — batch analysis-002 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session over the MCP tools; not a person
- 2026-10-07T17:49:55Z: host session (automatic) — batch analysis-001 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session over the MCP tools; not a person
- 2026-10-07T17:50:32Z: submission reused (automatic) — batch analysis-002 by tenderpack.ai.workflow; the host session's staged set ADD-03-host-20261007T174923Z-93d8 (made after the resume at 2026-10-07T17:43:24Z) was revalidated and taken instead of asking the batch again
- 2026-10-07T18:04:15Z: host session (automatic) — batch analysis-003 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session over the MCP tools; not a person
- 2026-10-07T18:05:12Z: submission reused (automatic) — batch analysis-004 by tenderpack.ai.workflow; the host session's staged set ADD-03-host-20261007T180030Z-7e0e (made after the resume at 2026-10-07T17:43:24Z) was revalidated and taken instead of asking the batch again
- 2026-10-07T18:08:29Z: host session (automatic) — batch analysis-005 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session over the MCP tools; not a person
- 2026-10-07T18:11:22Z: host session (automatic) — batch analysis-006 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session over the MCP tools; not a person
- 2026-10-07T18:32:06Z: host session (automatic) — batch downstream-001 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session; not a person
- 2026-10-07T18:38:15Z: host session (automatic) — batch downstream-002 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session; not a person
- 2026-10-07T18:38:39Z: host session (automatic) — batch downstream-003 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session; not a person
- 2026-10-07T18:47:02Z: host session (automatic) — batch downstream-004 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session; not a person

## The diff (ADD-02 → ADD-03; [diff.md](diff.md))

## What changed from ADD-02 to ADD-03

### ADD-03: PARTIAL (issued 2026-11-17)

- ops: 15 (0 invalid); provisions: 57 (8 unresolved)
- validated state: ADD-02 — this addendum does NOT replace it until every provision is treated and every op is valid
- UNRESOLVED ADD-03:3.6: The Bidder shall demonstrate in the Technical Proposal how its lifecycle plan achieves the residual service lives in Table 42-1.
- UNRESOLVED ADD-03:4.2: Each Bidder shall state in the Technical Proposal the ground conditions assumed for the design of foundations, by reference to the Geotechnical Baseline Report.
- UNRESOLVED ADD-03:4.3: A Bidder that wishes to inspect the borehole cores and laboratory records on which the Geotechnical Baseline Report is based shall request an appointment throug
- UNRESOLVED ADD-03:p3-image/r4: م: ٤ | فئة الأصول: المعدات الكهربائية وأجهزة القياس والتحكم | الحد الأدنى للعمر المتبقي (سنة): ٧ | أقصى درجة للحالة: ٣
- UNRESOLVED ADD-03:p3-image/r5: م: ٥ | فئة الأصول: الأغشية (إن وُجدت) | الحد الأدنى للعمر المتبقي (سنة): ٢٤ شهراً | أقصى درجة للحالة: ٣
- UNRESOLVED ADD-03:T42-1/4: No: 4 | Asset class: Electrical, instrumentation and control equipment | Minimum residual life (years): 5 | Maximum condition grade: 3
- UNRESOLVED ADD-03:T42-1/5: No: 5 | Asset class: Membranes (where provided) | Minimum residual life (years): 24 | Maximum condition grade: 3
- UNRESOLVED ADD-03:T42-1/note(4): (4)  The design life of electrical equipment stated in Volume II Clause 2.2 is increased to twenty-five (25) years.
- cover summary vs provisions (C28, report only): 9 finding(s)
  - figure differs: the summary says 'reduces the threshold in Volume V Clause 36.2 for compensation for a General Change in Law to SAR 4,000,000' (SAR 4,000,000); ADD-03:2.1 says 'The amount stated in Volume V Clause 36.2 is reduced by SAR 1,000,000.' (VOL-V 36.2 before ADD-03 states 'SAR 2,500,000'; reduced by SAR 1,000,000 gives SAR 1,500,000 (arithmetic for a person to check); SAR 4,000,000 is the earlier figure 'SAR 5,000,000' reduced by SAR 1,000,000: a superseded base)
  - count differs: the summary says 'four asset classes set out in Table 42-1'; ADD-03:T42-1 has 5 row(s)
  - not found: 'replaces the remaining design life required at handback with minimum residual service lives for four asset classes set out in Table 42-1 (issued in Arabic)': no provision of ADD-03 does this
  - modality differs: the summary says 'invites Bidders to describe in their Technical Proposals how their lifecycle plans address Table 42-1' (permission); ADD-03:3.6 says 'The Bidder shall demonstrate in the Technical Proposal how its lifecycle plan achieves the residual service lives in Table 42-1.' (obligation)
  - contradicted: 'provides for the inspection of borehole cores and laboratory records with a limited exception to Volume I Clause 4.2', but ADD-03/4.4 disapplies VOL-I:4.2 to: communications with the Authority's geotechnical consultant during an appointment under Section 4.3, to the extent that they concern the identification and handling of cores and records
  - understated: 'responds to clarification requests 15 to 19', but ADD-03/Q17(b) adds an obligation (VOL-I:10.6): 'The schedule required by Volume I Clause 10.6 forms part of Form 4-F and shall be attached to it in Envelope B. The schedule shall also state the minimum annual debt service cover ratio assumed. A schedule placed in Envelope A will be trea…'
  - omitted: ADD-03/2.2 adds an obligation (ADD-03:2.2); the summary does not mention it: 'Bidders shall take Section 2.1 into account in the Availability Payment quoted in Form 4-F.'
  - omitted: ADD-03/3.3 amends VOL-V:42.1; the summary does not mention it: 'In Volume V Clause 42.1, ‘Volume II Clause 8.5’ is deleted and ‘Clause 42.3’ is substituted.'
  - omitted: ADD-03/3.4(a) amends VOL-V:42.1; the summary does not mention it: 'In Volume V Clause 42.1, ‘with a remaining design life of not less than five (5) years for all major assets’ is deleted and ‘with a residual service life, for each asset class, of not less than that stated in Table 42-1’ is substituted. Ta…'

#### Validated vs candidate (partial should not mean useless)

- validated (unchanged, ADD-02): `<outputs>/a3/a3.pdf` (one page), `<outputs>/a5/`
- candidate (CANDIDATE — NOT VALIDATED, ADD-03 as proposed): `<outputs>/a3/a3_candidate.pdf` / `.md`, `<outputs>/a5/candidate/`

**What may be changing.** ADD-03 is PARTIAL: 8 of 57 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 15 op(s) that are valid there stood (each still a proposal: review proposed 15), A3 would gain 0 row(s) (none), lose 0 (none) and change 0 (none); A5, replanned at ADD-03's issue date (2026-11-17), would move the latest dates of 0 activities (none), add 1 (core-inspection-request) and remove 0 (none), and marks 7 REVIEW through relationships. Not settled: 4 activities blocked by an unresolved row (technical-proposal, core-inspection-request, deviations-review, form-4e), 1 STALE row(s), 2 obligation(s) reaching no output (C46), 0 relationship chain(s) blocked or incomplete, 5 conflict(s); documents not supplied: the Environmental Permit issued for the site, Geotechnical Baseline Report (Revision C), Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions) and 7 more; conditional or effective-dated: ADD-03:T42-1/4 (conditional obligation); ADD-03:T42-1/5 (conditional obligation); ADD-03:T42-1/note(4) (conditional obligation). Clarification route: the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person. Nothing here is validated, accepted or applied to the real state.

- **Clarification route:** the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person (ADD-03 issued 2026-11-17; the cut-off is computed from VOL-I-5.2-01 at that stage). No question about it is suggested as sendable; a proposed entry stays a DRAFT, not sent.

### Requirements

- new: 7; out of force: 2; changed: 4

- NEW ADD-03-cover-para3-01: NEW (introduced by ADD-03/cover/para3)
- NEW ADD-03-4.1-01: NEW (introduced by ADD-03/4.1) (by ADD-03/4.1)
- NEW ADD-03-3.6-01: NEW (introduced by ADD-03:3.6)
- NEW ADD-03-4.2-01: NEW (introduced by ADD-03:4.2)
- NEW ADD-03-4.3-01: NEW (introduced by ADD-03:4.3)
- NEW ADD-03-Q17-01: NEW (introduced by ADD-03/Q17(b))
- NEW ADD-03-cover-01: NEW (introduced by ADD-03/cover/para3)
- OUT VOL-II-8.5-01: REPLACED (by VOL-V:42.3)
- OUT VOL-II-8.5-02: REPLACED (by VOL-V:42.3)
- CHANGED VOL-IV-F4E-01: VOL-V 36.2: '2,500,000' -> '1,500,000' by ADD-03/2.1 (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed)); VOL-V 42.1: 'Volume II Clause 8.5,' -> 'Clause 42.3,'; 'remaining design life' -> 'residual service life, for each asset class,'; 'five (5) years for all major assets.' -> 'that stated in Table 42-1.' by ADD-03/3.3, ADD-03/3.4(a) (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed))
- CHANGED VOL-V-36.2-01: wording (by ADD-03/2.1)
- CHANGED VOL-V-42.1-01: wording; quoted words (by ADD-03/3.3, ADD-03/3.4(a))
- CHANGED VOL-V-42.1-02: wording; quoted words; reading: parameters (by ADD-03/3.3, ADD-03/3.4(a))
- CONFIRMED (unchanged) VOL-I-4.2-01: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'The text is unchanged at ADD-03. ADD-03 4.4 (op ADD-03/4.4, disapplies) excludes from the clause 'communications with the Authority's geotechnical consultant d…'); other ops on its units (the re-made reading records no change from them; a person checks): ADD-03/4.4 (disapplies; ADD-03:4.4)
- CONFIRMED (unchanged) VOL-II-9.3-01: confirmed by ADD-03/Q16 (confirms; ADD-03:Q16) (proposed op, awaiting a person's acceptance); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'The text is unchanged. ADD-03 Q16 (op ADD-03/Q16, confirms) restates the clause and says 'Volume II Clause 9.3 applies.' [AI workflow run ADD-03-run-host-20261…')
- NOT SETTLED VOL-I-10.1-01: unchanged by the applied ops; not confirmed while: open: I-VOL-I-ENV-B, human decision pending (the confirming op(s) do not settle it: proposed op ADD-03/Q17(a) (awaiting a person's acceptance): interprets; ADD-03:Q17; answer reads 'adds' (summary.classify_answer))
- NOT SETTLED VOL-I-10.6-01: unchanged by the applied ops; not confirmed while: open: I-VOL-I-ENV-B, human decision pending (the confirming op(s) do not settle it: proposed op ADD-03/Q17(a) (awaiting a person's acceptance): interprets; ADD-03:Q17; answer reads 'adds' (summary.classify_answer))

### Stale readings and decisions

- STALE VOL-V-36.2-01: VOL-V:36.2 changed since ADD-02 (by ADD-03/2.1); quote not found in the effective text at ADD-03: 'SAR 2,500,000' (expected: the interpretation predates the change)

### Obligations not reaching the outputs (C46)

- ADD-03/2.2 [A1]: ADD-03/2.2 (annotate) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Bidders shall take Section 2.1 into account in the Availability Payment quoted in Form 4-F.'
- ADD-03/3.1 [A1]: ADD-03/3.1 (relocate_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Volume II Clause 8.5 is relocated to Volume V, in which it becomes Clause 42.3. Its text is unchanged and reads as follows: ‘42.3  A handba

### Reached through relationships (indirect: for review, not direct citations)

Curated links (relationships file) followed from what changed. The requirements above cite a changed unit; these are reached through another provision, in three classes that are never merged. A5 marks the activities that serve them REVIEW with their dates unchanged.

Relationship status: confirmed = stated in the documents (the entry quotes the cross-reference), not confirmed by a person; proposed = inferred by a curator or a model, a person decides; possible = a weaker inference.

#### Confirmed dependency (1)
- VOL-IV-F4E-01 (row; ACTIVE) <- VOL-V:36.2, VOL-V:42.1 via REL-VOL-V-FORM-4E [depends_on; link confirmed]

#### Proposed relationship (5)
- VOL-V-12.1-01 (row; ACTIVE) <- VOL-V:12.4+ADD-03 via REL-AI-008 [depends_on; link proposed]
- VOL-V-18.3-01 (row; ACTIVE) <- VOL-V:12.4+ADD-03 via REL-AI-008 [depends_on; link proposed]
- VOL-V:42.3 (unit; ACTIVE) <- VOL-V:42.1 via REL-AI-007 [cites; link proposed]; also changed directly
- fin-model-build (activity) <- VOL-V:36.2 via REL-AI-001 [depends_on; link proposed]
- form-4a-prep (activity) <- ADD-03-cover-01 via REL-AI-006 [depends_on; link proposed]

#### Possible impact (8)
- ADD-03:p3-image (unit; ACTIVE) <- VOL-V:42.1 via REL-AI-002 [cites; link possible]; also changed directly
- VOL-I-10.3-01 (row; ACTIVE) <- VOL-V:36.2 via REL-CHANGE-IN-LAW-FINANCIAL-MODEL [depends_on; link possible]
- VOL-II:2.2 (unit; ACTIVE) <- ADD-03:T42-1/note(4) via REL-AI-003 [cites; link possible]
- VOL-IV-F4F-02 (row; ACTIVE) <- VOL-V:36.2 via REL-CHANGE-IN-LAW-FINANCIAL-MODEL > REL-MODEL-FORM-4F [feeds_calculation; link possible]
- fin-model-build (activity) <- ADD-03:cover/para3 via REL-AI-004 [feeds_calculation; link possible]
- fin-model-build (activity) <- ADD-03-T42-1-01 via REL-AI-009 [depends_on; link possible]
- technical-proposal (activity) <- ADD-03:3.6 via REL-AI-005 [depends_on; link possible]
- technical-proposal (activity) <- ADD-03-T42-1-01 via REL-AI-009 [depends_on; link possible]

#### Referenced but not supplied: conclusions in play that cannot be established (1)
- ADD-03:4.1 (unit; ACTIVE) <- ADD-03:4.1 via REL-REF-GEOTECHNICAL-BASELINE-REPORT-REV-C [missing_document; link proposed]; also changed directly. NOT SUPPLIED: Geotechnical Baseline Report (Revision C); cannot be established: what ADD-03:4.1 makes depend on it: ‘In this Clause, the Geotechnical Baseline Report means Revision C of the report of that name issued by the Authority.’’

### Disqualifiers (A3)

- no change

### Earlier answers to re-read against the new text (never revoked; a person decides)

- `ADD-03:Q17` (ADD-03): cites VOL-I:10.6, changed by ADD-03/Q17(b); to be re-read against the new text of VOL-I:10.6 (ADD-03/Q17(b)); a person decides whether the answer still holds

### Programme impact (status date 2026-10-22 -> 2026-11-17)

- STATUS assemble-envelope-a: timing INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD; total float -12 -> -30 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- NOT SETTLED assemble-envelope-b: VOL-I-10.1-01: open: I-VOL-I-ENV-B, human decision pending (the confirming op(s) do not settle it: proposed op ADD-03/Q17(a) (awaiting a person's acceptance): interprets; ADD-03:Q17; answer reads 'adds' (summary.classify_answer)); unchanged at this stage but not confirmed: a person decides
- STATUS assemble-envelope-b: timing OK -> INFEASIBLE by 18 WD; total float 0 -> -18 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS attendance-notice: timing CONDITIONAL — window elapsed 2026-10-14; whether the condition arose is not known -> CONDITIONAL — window elapsed 2026-10-14; whether the condition arose is not known; total float -7 -> -25 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS bond-approval: timing OK -> INFEASIBLE by 8 WD; total float +10 -> -8 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS bond-issue: timing OK -> INFEASIBLE by 8 WD; total float +10 -> -8 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS clarifications: timing OK -> DEADLINE PASSED; total float +13 -> -5 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS completion-certs: timing OK -> INFEASIBLE by 11 WD; total float +7 -> -11 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS consortium-check: timing OK -> INFEASIBLE by 5 WD; total float +13 -> -5 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS copies: timing INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD; total float -12 -> -30 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- NEW core-inspection-request: needed by ADD-03-4.3-01
- STATUS deliver: timing INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD; total float -12 -> -30 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- REWORK deviations-review: requirement changed: ADD-03-4.1-01 (text, status, consequence, quote), VOL-IV-F4E-01 (dependency: VOL-V 36.2: '2,500,000' -> '1,500,000' by ADD-03/2.1 (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed)); VOL-V 42.1: 'Volume II Clause 8.5,' -> 'Clause 42.3,'; 'remaining design life' -> 'residual service life, for each asset class,'; 'five (5) years for all major assets.' -> 'that stated in Table 42-1.' by ADD-03/3.3, ADD-03/3.4(a) (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed))), VOL-V-36.2-01 (text, status, stale), VOL-V-42.1-01 (text, status, quote), VOL-V-42.1-02 (text, status, quote, parameters)
- STATUS deviations-review: timing OK -> INFEASIBLE by 7 WD; total float +11 -> -7 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- REWORK fin-assumptions: requirement changed: ADD-03-Q17-01 (text, status, consequence, quote)
- NOT SETTLED fin-assumptions: VOL-I-10.6-01: open: I-VOL-I-ENV-B, human decision pending (the confirming op(s) do not settle it: proposed op ADD-03/Q17(a) (awaiting a person's acceptance): interprets; ADD-03:Q17; answer reads 'adds' (summary.classify_answer)); unchanged at this stage but not confirmed: a person decides
- STATUS fin-assumptions: timing OK -> INFEASIBLE by 15 WD; total float +3 -> -15 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- NOT SETTLED fin-model-build: VOL-I-10.1-01: open: I-VOL-I-ENV-B, human decision pending (the confirming op(s) do not settle it: proposed op ADD-03/Q17(a) (awaiting a person's acceptance): interprets; ADD-03:Q17; answer reads 'adds' (summary.classify_answer)); unchanged at this stage but not confirmed: a person decides
- STATUS fin-model-build: timing OK -> INFEASIBLE by 18 WD; total float 0 -> -18 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- NOT SETTLED fin-model-freeze: VOL-I-10.1-01: open: I-VOL-I-ENV-B, human decision pending (the confirming op(s) do not settle it: proposed op ADD-03/Q17(a) (awaiting a person's acceptance): interprets; ADD-03:Q17; answer reads 'adds' (summary.classify_answer)); unchanged at this stage but not confirmed: a person decides
- STATUS fin-model-freeze: timing OK -> INFEASIBLE by 18 WD; total float 0 -> -18 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS fin-standing: timing OK -> INFEASIBLE by 3 WD; total float +15 -> -3 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS fin-statements: timing OK -> INFEASIBLE by 3 WD; total float +15 -> -3 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- REWORK form-4a: requirement changed: ADD-01-AppA-01 (Addenda to acknowledge: ADD-03 issued since ADD-02: 'Bidders shall acknowledge receipt in Form 4-A.'), ADD-03-cover-01 (text, status, consequence, quote, parameters), ADD-03-cover-para3-01 (text, status, consequence, quote)
- NOT SETTLED form-4a: VOL-IV-F4A-01: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); VOL-IV-F4A-02: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); unchanged at this stage but not confirmed: a person decides
- STATUS form-4a: timing OK -> INFEASIBLE by 6 WD; total float +12 -> -6 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- REWORK form-4a-prep: requirement changed: ADD-01-AppA-01 (Addenda to acknowledge: ADD-03 issued since ADD-02: 'Bidders shall acknowledge receipt in Form 4-A.'), ADD-03-cover-01 (text, status, consequence, quote, parameters), ADD-03-cover-para3-01 (text, status, consequence, quote)
- NOT SETTLED form-4a-prep: VOL-IV-F4A-01: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); VOL-IV-F4A-02: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); unchanged at this stage but not confirmed: a person decides
- STATUS form-4a-prep: timing OK -> OK; total float +20 -> +2 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS form-4b: timing OK -> INFEASIBLE by 11 WD; total float +7 -> -11 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS form-4b-prep: timing OK -> INFEASIBLE by 9 WD; total float +9 -> -9 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS form-4c-prep: timing OK -> OK; total float +18 -> 0 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS form-4c-sign: timing OK -> INFEASIBLE by 8 WD; total float +10 -> -8 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- REWORK form-4e: requirement changed: ADD-03-4.1-01 (text, status, consequence, quote), VOL-IV-F4E-01 (dependency: VOL-V 36.2: '2,500,000' -> '1,500,000' by ADD-03/2.1 (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed)); VOL-V 42.1: 'Volume II Clause 8.5,' -> 'Clause 42.3,'; 'remaining design life' -> 'residual service life, for each asset class,'; 'five (5) years for all major assets.' -> 'that stated in Table 42-1.' by ADD-03/3.3, ADD-03/3.4(a) (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed))), VOL-V-36.2-01 (text, status, stale), VOL-V-42.1-01 (text, status, quote), VOL-V-42.1-02 (text, status, quote, parameters)
- STATUS form-4e: timing OK -> INFEASIBLE by 17 WD; total float +1 -> -17 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- REWORK form-4f: requirement changed: ADD-03-Q17-01 (text, status, consequence, quote)
- NOT SETTLED form-4f: VOL-I-10.1-01: open: I-VOL-I-ENV-B, human decision pending (the confirming op(s) do not settle it: proposed op ADD-03/Q17(a) (awaiting a person's acceptance): interprets; ADD-03:Q17; answer reads 'adds' (summary.classify_answer)); unchanged at this stage but not confirmed: a person decides
- STATUS form-4f: timing OK -> INFEASIBLE by 18 WD; total float 0 -> -18 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS form-4g-review: timing OK -> INFEASIBLE by 1 WD; total float +17 -> -1 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS form-4g-sign: timing OK -> INFEASIBLE by 6 WD; total float +12 -> -6 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS ground-dd: timing OK -> INFEASIBLE by 14 WD; total float +5 -> -14 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS investment-licence: timing OK -> INFEASIBLE by 10 WD; total float +8 -> -10 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS iso-copy: timing OK -> OK; total float +21 -> +3 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS lcc-certificate: timing INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD; total float -12 -> -30 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS lcc-ratio: timing INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD; total float -12 -> -30 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- REWORK lender-terms: requirement changed: ADD-03-Q17-01 (text, status, consequence, quote)
- NOT SETTLED lender-terms: VOL-I-10.6-01: open: I-VOL-I-ENV-B, human decision pending (the confirming op(s) do not settle it: proposed op ADD-03/Q17(a) (awaiting a person's acceptance): interprets; ADD-03:Q17; answer reads 'adds' (summary.classify_answer)); unchanged at this stage but not confirmed: a person decides
- STATUS lender-terms: timing OK -> INFEASIBLE by 13 WD; total float +5 -> -13 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS model-audit-opinion: timing OK -> INFEASIBLE by 18 WD; total float 0 -> -18 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS model-audit-review: timing OK -> INFEASIBLE by 17 WD; total float +1 -> -17 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS model-auditor-appoint: timing OK -> INFEASIBLE by 17 WD; total float +1 -> -17 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS om-evidence: timing OK -> INFEASIBLE by 5 WD; total float +13 -> -5 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS pcg-execution: timing OK -> INFEASIBLE by 15 WD; total float +3 -> -15 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS pcg-wording: timing OK -> INFEASIBLE by 15 WD; total float +3 -> -15 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS poa: timing OK -> INFEASIBLE by 10 WD; total float +8 -> -10 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS poa-resolutions: timing OK -> INFEASIBLE by 10 WD; total float +8 -> -10 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS references: timing OK -> INFEASIBLE by 9 WD; total float +9 -> -9 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS seal-and-mark: timing INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD; total float -12 -> -30 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS spoc: timing OK -> OK; total float +21 -> +3 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- REWORK technical-proposal: requirement changed: ADD-03-3.6-01 (text, status, consequence, quote), ADD-03-4.2-01 (text, status, consequence, quote)
- CONFIRMED (unchanged) technical-proposal: VOL-II-9.3-01: confirmed by ADD-03/Q16 (confirms; ADD-03:Q16) (proposed op, awaiting a person's acceptance); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'The text is unchanged. ADD-03 Q16 (op ADD-03/Q16, confirms) restates the clause and says 'Volume II Clause 9.3 applies.' [AI workflow run ADD-03-run-host-20261…'); text, cells, dates, status and consequence unchanged: work done stands
- STATUS technical-proposal: timing OK -> INFEASIBLE by 17 WD; total float +1 -> -17 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- REVIEW (confirmed dependency) deviations-review: VOL-IV-F4E-01 reached from VOL-V:36.2, VOL-V:42.1 via REL-VOL-V-FORM-4E; dates unchanged
- REVIEW (proposed relationship) deviations-review: VOL-V-12.1-01, VOL-V-18.3-01 reached from VOL-V:12.4+ADD-03 via REL-AI-008; dates unchanged
- REVIEW (proposed relationship) fin-model-build: fin-model-build reached from VOL-V:36.2 via REL-AI-001; dates unchanged
- REVIEW (possible impact) fin-model-build: VOL-I-10.3-01, VOL-IV-F4F-02, fin-model-build reached from ADD-03-T42-1-01, ADD-03:cover/para3, VOL-V:36.2 via REL-AI-004, REL-AI-009, REL-CHANGE-IN-LAW-FINANCIAL-MODEL, REL-MODEL-FORM-4F; dates unchanged
- REVIEW (possible impact) fin-model-freeze: VOL-I-10.3-01, VOL-IV-F4F-02 reached from VOL-V:36.2 via REL-CHANGE-IN-LAW-FINANCIAL-MODEL, REL-MODEL-FORM-4F; dates unchanged
- REVIEW (proposed relationship) form-4a-prep: form-4a-prep reached from ADD-03-cover-01 via REL-AI-006; dates unchanged
- REVIEW (confirmed dependency) form-4e: VOL-IV-F4E-01 reached from VOL-V:36.2, VOL-V:42.1 via REL-VOL-V-FORM-4E; dates unchanged
- REVIEW (proposed relationship) form-4e: VOL-V-12.1-01, VOL-V-18.3-01 reached from VOL-V:12.4+ADD-03 via REL-AI-008; dates unchanged
- REVIEW (possible impact) form-4f: VOL-IV-F4F-02 reached from VOL-V:36.2 via REL-CHANGE-IN-LAW-FINANCIAL-MODEL, REL-MODEL-FORM-4F; dates unchanged
- REVIEW (possible impact) technical-proposal: technical-proposal reached from ADD-03-T42-1-01, ADD-03:3.6 via REL-AI-005, REL-AI-009; dates unchanged
- FEASIBILITY lcc-ratio: INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD
- FEASIBILITY lcc-certificate: INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD
- FEASIBILITY fin-model-build: OK -> INFEASIBLE by 18 WD
- FEASIBILITY model-auditor-appoint: OK -> INFEASIBLE by 17 WD
- FEASIBILITY technical-proposal: OK -> INFEASIBLE by 17 WD
- FEASIBILITY pcg-wording: OK -> INFEASIBLE by 15 WD
- FEASIBILITY core-inspection-request: absent -> INFEASIBLE by 14 WD
- FEASIBILITY ground-dd: OK -> INFEASIBLE by 14 WD
- FEASIBILITY lender-terms: OK -> INFEASIBLE by 13 WD
- FEASIBILITY model-audit-review: OK -> INFEASIBLE by 17 WD
- FEASIBILITY completion-certs: OK -> INFEASIBLE by 11 WD
- FEASIBILITY poa-resolutions: OK -> INFEASIBLE by 10 WD
- FEASIBILITY references: OK -> INFEASIBLE by 9 WD
- FEASIBILITY bond-approval: OK -> INFEASIBLE by 8 WD
- FEASIBILITY deviations-review: OK -> INFEASIBLE by 7 WD
- FEASIBILITY consortium-check: OK -> INFEASIBLE by 5 WD
- FEASIBILITY om-evidence: OK -> INFEASIBLE by 5 WD
- FEASIBILITY pcg-execution: OK -> INFEASIBLE by 15 WD
- FEASIBILITY poa: OK -> INFEASIBLE by 10 WD
- FEASIBILITY clarifications: OK -> DEADLINE PASSED
- FEASIBILITY fin-model-freeze: OK -> INFEASIBLE by 18 WD
- FEASIBILITY fin-statements: OK -> INFEASIBLE by 3 WD
- FEASIBILITY model-audit-opinion: OK -> INFEASIBLE by 18 WD
- FEASIBILITY form-4g-review: OK -> INFEASIBLE by 1 WD
- FEASIBILITY investment-licence: OK -> INFEASIBLE by 10 WD
- FEASIBILITY fin-assumptions: OK -> INFEASIBLE by 15 WD
- FEASIBILITY form-4b-prep: OK -> INFEASIBLE by 9 WD
- FEASIBILITY bond-issue: OK -> INFEASIBLE by 8 WD
- FEASIBILITY fin-standing: OK -> INFEASIBLE by 3 WD
- FEASIBILITY form-4c-sign: OK -> INFEASIBLE by 8 WD
- FEASIBILITY form-4e: OK -> INFEASIBLE by 17 WD
- FEASIBILITY form-4f: OK -> INFEASIBLE by 18 WD
- FEASIBILITY form-4a: OK -> INFEASIBLE by 6 WD
- FEASIBILITY form-4b: OK -> INFEASIBLE by 11 WD
- FEASIBILITY form-4g-sign: OK -> INFEASIBLE by 6 WD
- FEASIBILITY assemble-envelope-a: INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD
- FEASIBILITY assemble-envelope-b: OK -> INFEASIBLE by 18 WD
- FEASIBILITY copies: INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD
- FEASIBILITY seal-and-mark: INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD
- FEASIBILITY deliver: INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD

## Next (a person)

- read the unresolved and escalated provisions first, then each item against its evidence (`../ai/ADD-03-run-host-20261007T161946Z-e884-combined/proposals.yaml`, `../downstream/proposals.yaml`)
- nothing here is applied to the real curation: to take an item over, add the PDF to the pack (OPERATING_GUIDE §3 steps 1-2) and copy the reviewed files listed in `promotion.json`; then `pin`, `check-register`, `outputs` and decide with `accept` / `reject` as usual
