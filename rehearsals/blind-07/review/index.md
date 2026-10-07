# Review packet: ADD-03, AI workflow run ADD-03-run-host-20261006T201359Z-2503

> **CANDIDATE: proposed by the AI workflow; not reviewed; nothing accepted.** Statuses are the controller's; a person decides every item. The real `curation/`, `config/` and `out/` were only read: everything below lives in this run's folder.

- PDF: `/tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s13/final/unzipped4/LAMAR-PPP-R2-INTERVIEW_0a63e3a+wt_20261006T2012Z/staging/panel/uploads/06afe32fcaa678eeb991fbfe0c556f35443ab4b42a24f9dd91bb09e9fd2dbc8d.pdf` (sha256 06afe32fcaa678ee…, 4 pages); preceding state: pack `/tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s13/final/unzipped4/LAMAR-PPP-R2-INTERVIEW_0a63e3a+wt_20261006T2012Z/config/pack.yaml` (NUPA-ISTP-2026-014), previous evidence build `/tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s13/final/unzipped4/LAMAR-PPP-R2-INTERVIEW_0a63e3a+wt_20261006T2012Z/build`
- route **host**; model requested `claude-code headless (the CLI's default model; recorded from the CLI output)`, reported `None`; host sessions report: claude-sonnet-5-5
- status **partial**: 19 provision(s) unresolved in the candidate (listed first in the review packet); 12 downstream task(s) answered only by items that cannot be promoted: esc:ADD-03:3.1, esc:ADD-03:3.3, esc:ADD-03:3.4, esc:ADD-03:4.4, esc:ADD-03:Q18, esc:ADD-03:T42-1/image/r2, esc:ADD-03:T42-1/image/r4, esc:ADD-03:T42-1/image/r5 …; check-register on the candidate: exit 1, 8 finding(s) {'deliverable': 8}
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed
- code at start: content f5e50e87f754dc53… over 98 files; git not available; recorded 2026-10-06T20:13:59Z

## Execution, completeness and approval (three separate things)

- **Execution** (what ran): ingest done, readings done, analysis done, validation done, downstream done, downstream_validation done, critic done, promotion done, pin done, check_register done, outputs done, diff done, review running; batches reading: {'done': 1}; analysis: {'done': 5}; downstream: {'done': 2}
- **Completeness** (what the run completed): **partial**: 19 provision(s) unresolved in the candidate (listed first in the review packet); 12 downstream task(s) answered only by items that cannot be promoted: esc:ADD-03:3.1, esc:ADD-03:3.3, esc:ADD-03:3.4, esc:ADD-03:4.4, esc:ADD-03:Q18, esc:ADD-03:T42-1/image/r2, esc:ADD-03:T42-1/image/r4, esc:ADD-03:T42-1/image/r5 …; check-register on the candidate: exit 1, 8 finding(s) {'deliverable': 8}
  - downstream tasks: 17; answered 5; unanswered 0; answered only by items that cannot be promoted 12; answered 'no change' 0
- **Human approval**: **none** (nothing approved, accepted, rejected or sent); no decision is recorded in the candidate's decisions file

## What is candidate and what is real

- **Candidate** (proposed by this run, nothing accepted): `../candidate/` — a copy of the curation and configuration with ADD-03 added, its evidence build, its op file, rows, issues, templates and outputs.
- **Last validated state**: `../candidate/out-before/` (the pre-addendum outputs built from the copied curation and the previous evidence build; done)
- **Real** (untouched): `curation/`, `config/`, `out/`; the owner's approvals and readings were copied unchanged and used read-only.

- real inputs changed since the run started: none

## Candidate outputs

Exit 0 (WORKING DRAFT (not releasable)); every file carries the banner (`../candidate/out/CANDIDATE.md`); A1 has a candidate status column {'proposed (existing row; not changed by this run; not reviewed)': 191, 'PROPOSED BY THE AI WORKFLOW': 9, 'UNRESOLVED': 14}.

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

- before → after: {"a1": {"rows_before": 205, "rows_after": 214, "new": 9, "gone": 0}, "a3": {"before": 17, "after": 17, "enters": 0, "leaves": 0}, "a5": {"activities_before": 44, "activities_after": 44, "new": 0, "gone": 0}}

- ADD-03 is **PARTIAL** in the candidate (provisions unresolved): A3 and the A5 programme show the validated state (ADD-02); ADD-03 as proposed is in A1's `Status after ADD-03` column, in A2, in the candidate A3 and A5 below, in `a5/working/ADD-03.json` and in the diff below.

### Validated and candidate A3 / A5 (partial should not mean useless)

- **Validated** (unchanged; ADD-02): [a3/a3.pdf](../candidate/out/a3/a3.pdf) (one page), [a5/README.md](../candidate/out/a5/README.md), [a5/gantt.html](../candidate/out/a5/gantt.html)
- **Candidate** (CANDIDATE — NOT VALIDATED; ADD-03 as proposed): [a3/a3_candidate.pdf](../candidate/out/a3/a3_candidate.pdf) (10 page(s)), [a3/a3_candidate.md](../candidate/out/a3/a3_candidate.md), [a5/candidate/README.md](../candidate/out/a5/candidate/README.md), [a5/candidate/gantt.html](../candidate/out/a5/candidate/gantt.html)

**What may be changing.** ADD-03 is PARTIAL: 36 of 49 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 2 op(s) that are valid there stood (each still a proposal: review proposed 2), A3 would gain 0 row(s) (none), lose 0 (none) and change 0 (none); A5, replanned at ADD-03's issue date (2026-11-17), would move the latest dates of 0 activities (none), add 0 (none) and remove 0 (none), and marks 0 REVIEW through relationships. Not settled: 14 activities blocked by an unresolved row (fin-model-build, technical-proposal, lender-terms, deviations-review and 10 more), 0 STALE row(s), 0 obligation(s) reaching no output (C46), 0 relationship chain(s) blocked or incomplete, 3 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT and 6 more. Clarification route: the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person. Nothing here is validated, accepted or applied to the real state.


- blockers: 36 unresolved provision(s), 14 blocked activit(y/ies), 0 STALE row(s), 0 C46 gap(s), 0 relationship chain(s) blocked or incomplete, 3 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT, I-VOL-III, I-VOL-II-MISSING, I-VOL-V-MISSING, I-VOL-II-COMPLIANCE-POINT, I-VOL-IV-SCALE, I-OP-ADD-01/Q4
- conditional scenarios: 0

**Image-read units** (the review packet of each region shows every crop beside its reading; translations are proposals, not evidence):

- ADD-03-p3-r1 (ADD-03 p3; reading pending): [packet](../candidate/build/review/ADD-03-p3-r1/packet.html); 12 unit(s) touched
  - `ADD-03:T42-1/image`: “الهيئة الشمالية للمشتريات المرفقية لجنة نقل الأصول الرقم: ٤١٧/٢٠٢٦ التاريخ: ١٥ نوفمبر ٢٠٢٦م الموضوع: متطلبات حالة الأصول عند نقل محطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان مناقصة رقم: NUPA/I…”; issues I-ADD-03-T42-5-UNIT
  - `ADD-03:T42-1/image/r1`: “م: ١ / فئة الأصول: المنشآت المدنية والخرسانية / الحد الأدنى للعمر المتبقي (سنة): ٢٠ / أقصى درجة للحالة: ٢”
  - `ADD-03:T42-1/image/r2`: “م: ٢ / فئة الأصول: خط نقل المياه المعالجة / الحد الأدنى للعمر المتبقي (سنة): ٢٠ / أقصى درجة للحالة: ٢”
  - `ADD-03:T42-1/image/r3`: “م: ٣ / فئة الأصول: المعدات الميكانيكية / الحد الأدنى للعمر المتبقي (سنة): ٥ / أقصى درجة للحالة: ٣”
  - `ADD-03:T42-1/image/r4`: “م: ٤ / فئة الأصول: المعدات الكهربائية وأجهزة القياس والتحكم / الحد الأدنى للعمر المتبقي (سنة): ٧ / أقصى درجة للحالة: ٣”
  - `ADD-03:T42-1/image/r5`: “م: ٥ / فئة الأصول: الأغشية (إن وُجدت) / الحد الأدنى للعمر المتبقي (سنة): ٢٤ شهراً / أقصى درجة للحالة: ٣”; uncertain: min_life for row 5 is printed in months (24 months) under a column heading that says years (سنة); the difference is not resolved here; issues I-ADD-03-T42-5-UNIT
  - `ADD-03:T42-1/image/notes-heading`: “ملاحظات:”; translation (apart): ‘Notes:’
  - `ADD-03:T42-1/image/note1`: “١. تُقيَّم درجة الحالة وفق مقياس الهيئة لتصنيف حالة الأصول المكوَّن من خمس درجات، وتعني الدرجة ١ أن الأصل بحالة جديدة.”; translation (apart): ‘1. The condition grade is assessed according to the Authority's asset condition rating scale of five grades; grade 1 means the asset is in new condition.’; uncertain: vocalisation marks read at native resolution; not verified
  - `ADD-03:T42-1/image/note2`: “٢. يحدِّد المهندس المستقل العمر المتبقي لكل أصل في مسح الحالة الذي يُجرى قبل النقل.”; translation (apart): ‘2. The independent engineer determines the remaining life of each asset in the condition survey carried out before transfer.’
  - `ADD-03:T42-1/image/note3`: “٣. يُستبدَل على نفقة شركة المشروع قبل تاريخ النقل كلَّ أصل لا يستوفي متطلبات هذا الجدول.”; translation (apart): ‘3. Any asset that does not meet the requirements of this table is replaced before the transfer date at the Project Company's expense.’; issues I-ADD-03-T42-5-UNIT
  - `ADD-03:T42-1/image/signatory`: “رئيس لجنة نقل الأصول”; translation (apart): ‘Chairman of the Asset Transfer Committee’
  - `ADD-03:T42-1/image/english`: “Northern Utilities Procurement Authority - Asset Transfer Committee FICTIONAL DOCUMENT - Lamar Holding internal assessment pack - not a real tender.”; uncertain: band 17 right holds only the oval seal, with no legible text; the empty line records that it was examined
- VOL-II-p3-r1 (VOL-II p3; reading approved): [packet](../candidate/build/review/VOL-II-p3-r1/packet.html); not touched by this addendum
- VOL-IV-p6-r1 (VOL-IV p6; reading approved): [packet](../candidate/build/review/VOL-IV-p6-r1/packet.html); not touched by this addendum

## Timings (wall clock per step)

| Step | Seconds | Status |
|---|---|---|
| ingest | 16.4 | done |
| readings | 124.6 | done |
| analysis | 719.5 | done |
| validation | 13.6 | done |
| downstream | 190.6 | done |
| downstream_validation | 0.6 | done |
| critic | 38.6 | done |
| promotion | 19.6 | done |
| pin | 1.1 | done |
| check_register | 6.0 | done |
| outputs | 35.4 | done |
| diff | 10.7 | done |
| review | 0.0 | running |
| **total** | **1176.7** (19.6 min) | target 30 min from the PDF to candidate outputs and this packet, human review excluded |

## Readings of the addendum's image regions (AI-proposed, PENDING HUMAN REVIEW)

Ingest first refused the candidate because these image regions had no reading (C05): ADD-03-p3-r1. Each reading below was proposed by the route of this run, checked by readings.check_reading and written into the candidate's readings; it is an interpretation of an image, never approved, and every unit made from it carries `reading.status: pending`.

- **ADD-03-p3-r1** — done; controller status **interpretation_pending**; unit `ADD-03:T42-1/image`; file `../candidate/curation/readings/ADD-03-p3-r1.yaml`
  - the reading beside its crops (the build's review packet): [../candidate/build/review/ADD-03-p3-r1/packet.html](../candidate/build/review/ADD-03-p3-r1/packet.html)
  - table reading, languages ['ar', 'en']; prepared by: AI-assisted: headless host session ADD-03-hostsession-20261006T201416Z-75cd (claude-code headless (the CLI's default model; recorded from the CLI output); the CLI reported claude-sonnet-5-5), in AI workflow run ADD-03-run-host-20261006T201359Z-2503 (reading-ADD-03-p3-r1), 2026-10-06T20:16:05Z; prop…
  - uncertainty: Signature scribble and oval seal carry no legible text.
  - uncertainty: Row 5 life is printed in months under a years heading.
  - uncertainty: Vocalisation marks (tashkeel) were read at native resolution and not verified.

## First: unresolved provisions and escalations

19 of 49 provisions are not answered by a promoted item (each is `unresolved` in the candidate op file with the reason); 3 escalation(s).

- **Clarification route:** the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person (ADD-03 issued 2026-11-17; the cut-off is computed from VOL-I-5.2-01 at that stage). No question about it is suggested as sendable; a proposed entry stays a DRAFT, not sent.

- **ESCALATED ADD-03/3.1(a)** (ADD-03:3.1): software limitation: ADD-03:3.1 inserts a new Volume V Clause 42.3 ('42.3 A handback condition survey shall be carried out in the final two (2) years of the concession, and any remedial works identified shall be completed before transfer.'). simulate_amendment rejects insert_unit with VOL-V:42.3 (C…
  - clarification route: the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
  - unsupported: insert_unit of a new VOL-V clause not cited as a target by the provision; a person must record the insertion of VOL-V:42.3 (after VOL-V:42.2).
  - evidence: ADD-03:3.1 p1: “Volume II Clause 8.5 is relocated to Volume V, in which it becomes Clause 42.3.”; VOL-II:8.5 p5: “A handback condition survey shall be carried out in the final two (2) years of the concession, and any remedial works identified shall be completed before tran…”
  - affected scope: units VOL-II:8.5; rows VOL-II-8.5-01, VOL-II-8.5-02; activities technical-proposal; clarifications CQ-HANDBACK-CONDITION
- **ESCALATED ADD-03/3.4-issue** (ADD-03:3.4): software limitation: the sentence 'Table 42-1 is reproduced at Appendix A to this Addendum and forms part of Volume V.' makes the table part of Volume V, but no op type inserts a table into a volume; VOL-V has no Table 42-1 unit.
  - clarification route: the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
  - unsupported: insertion of a table (Table 42-1, ADD-03:T42-1) into Volume V as a new group; a person records it.
  - evidence: ADD-03:3.4 p1: “Table 42-1 is reproduced at Appendix A to this Addendum and forms part of Volume V.”
  - affected scope: units VOL-V:42.1; rows VOL-V-42.1-01, VOL-V-42.1-02; activities none; clarifications CQ-HANDBACK-CONDITION
- **ESCALATED ADD-03/4.4/esc** (ADD-03:4.4): software limitation: ADD-03:4.4 states that Volume I Clause 4.2 'does not apply' to a class of communications. That is a partial disapplication of a clause that carries disqualification ('Breach of this Clause shall result in the disqualification of the Bidder.'). It is not a text replacement, dele…
  - clarification route: the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
  - unsupported: an exception/disapplication of one clause for a defined class of communications, leaving VOL-I:4.2 text unchanged
  - evidence: ADD-03:4.4 p2: “Volume I Clause 4.2 does not apply to communications with the Authority's geotechnical consultant during an appointment under Section 4.3, to the extent that t…”; VOL-I:4.2 p3: “no Bidder, and no person acting for a Bidder, shall contact any board member, officer, employee, consultant or advisor of the Authority in relation to the Proj…”
  - affected scope: units VOL-I:4.2; rows VOL-I-4.2-01; activities none; clarifications none
- **UNRESOLVED ADD-03:2.2** (clause, p1): not promotable: ADD-03/2.2/row invalid (payload: not a register.Row: 2 validation errors for Row interpretations.0.consequence.Consequence Input should be a valid dictionary or instance of Consequence [type=m…) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:3.3** (clause, p1): not promotable: ADD-03/3.3 conflicting (dependencies: unknown ids ['ADD-03/3.1(a)']) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:3.6** (clause, p1): not promotable: ADD-03/3.6 invalid (payload: not a register.Row: 5 validation errors for Row scope Input should be a valid list [type=list_type, input_value='Technical Proposal', input_type=str] For furth…) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:4.2** (clause, p2): not promotable: ADD-03/4.2/row invalid (payload: not a register.Row: 2 validation errors for Row confidence Field required [type=missing, input_value={'id': 'A1-ADD03-4.2', 'g...a person to confirm."}]}, inpu…) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:4.3** (clause, p2): not promotable: ADD-03/4.3/row invalid (payload: not a register.Row: 2 validation errors for Row confidence Field required [type=missing, input_value={'id': 'A1-ADD03-4.3', 'g... no date typed here."}]}, inpu…) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:Q15** (table_row, p2): not promotable: ADD-03/Q15 invalid (previous_value: no target to compare the previous value "Bidders' attention is drawn to Volume I Clause 5.3. Statements recorded in the minutes at Appendix B are a record of w…) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:Q16** (table_row, p2): not promotable: ADD-03/Q16 invalid (previous_value: no target to compare the previous value 'A grievance mechanism accessible to the affected community shall be established before construction and maintained for…) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:Q17** (table_row, p2): not promotable: ADD-03/Q17 invalid (previous_value: no target to compare the previous value 'The Bidder shall submit with Form 4-F a schedule of the principal financing assumptions underlying the Availability Pa…) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:Q18** (table_row, p2): not promotable: ADD-03/Q18 insufficient_evidence (evidence VOL-V:39.5 p0: page 0 is not a page of VOL-V:39.5 ([4])); ADD-03/Q18-issue interpretation_pending (dropped: an analysis issue is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; the downstream phase proposes issues and clarification entries against the candidate) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:T42-1/image/r2** (table_row, p3): not promotable: ADD-03/T42-1/image/r2/disp insufficient_evidence (statements: fact analysis-003/S2 is not supported verbatim) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:T42-1/image/r4** (table_row, p3): not promotable: ADD-03/T42-1/image/r4/disp insufficient_evidence (statements: fact analysis-003/S2 is not supported verbatim); ADD-03/ISSUE/T42-1-arabic-english insufficient_evidence (statements: fact analysis-003/S2 is not supported verbatim) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:T42-1/image/r5** (table_row, p3): not promotable: ADD-03/T42-1/image/r5/disp insufficient_evidence (statements: fact analysis-003/S2 is not supported verbatim) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:T42-1/2** (table_row, p4): not promotable: ADD-03/T42-1/2/disp insufficient_evidence (statements: fact analysis-003/S2 is not supported verbatim) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:T42-1/4** (table_row, p4): not promotable: ADD-03/T42-1/4/disp insufficient_evidence (statements: fact analysis-003/S2 is not supported verbatim) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:T42-1/5** (table_row, p4): not promotable: ADD-03/T42-1/5/disp insufficient_evidence (statements: fact analysis-003/S2 is not supported verbatim) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:T42-1/note(4)** (note, p4): not promotable: ADD-03/T42-1/note(4)/disp insufficient_evidence (statements: fact analysis-003/S2 is not supported verbatim) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person

## Derived effects (session 12: pending readings, computed deadlines, conditions, consequences)

## Computed deadlines and the Working Days left (PROPOSED; nothing typed)

- Working Days left from the issue date (2026-11-17) to the PDD (2026-11-26): 7 (the issue date not counted, the PDD counted; Working Days per VOL-I 2.4 (weekend [4, 5] as date.weekday numbers; holidays none declared))
- `ADD-03:4.3` p2: “three (3) Working Days before the Proposal Due Date” -> **2026-11-23** (computed: calc deadline, anchor PDD = 2026-11-26, rule working-days-before, fingerprint 60b780e98a3a; PROPOSED, not validated)
- `ADD-03:4.3` p2: “within three (3) Working Days of the date of this Addendum” -> **AMBIGUOUS: 2026-11-22 (event_day_excluded); 2026-11-19 (event_day_counted)** (computed: calc deadline, anchor ADD-03-issue = 2026-11-17, rule none, fingerprint 4981e0314953; PROPOSED, not validated); ESCALATED: the counting rules do not settle it; not computed: no rule in the counting registry (config/formulas.yaml `counting`) for Working Days counted after a date (VOL-I 2.4 covers Working Days counted backwards): every reading is listed and a person decides
- `VOL-V:12.4+ADD-03` p2: “within five (5) Working Days of encountering them” -> **not computed: no rule in the counting registry (config/formulas.yaml `counting`) for Working Days counted after a date (VOL-I 2.4 covers Working Days counted backwards); its anchor 'encountering them' is an event, not a date the register holds** (computed: calc deadline, anchor encountering them = None, rule none, fingerprint ; PROPOSED, not validated); CONDITIONAL: “If the Project Company encounters at the site ground conditions that are materially more adverse than those described in the Geotechnical Baseline Report, it s…”

## Proposed from a pending reading (not in force; not planned)

- `ADD-03-T42-1-01` conditional on reading ADD-03-p3-r1 until approval: م: ١ | فئة الأصول: المنشآت المدنية والخرسانية | الحد الأدنى للعمر المتبقي (سنة): ٢٠ | أقصى درجة للحالة: ٢
- `ADD-03-T42-1-02` conditional on reading ADD-03-p3-r1 until approval: م: ٢ | فئة الأصول: خط نقل المياه المعالجة | الحد الأدنى للعمر المتبقي (سنة): ٢٠ | أقصى درجة للحالة: ٢
- `ADD-03-T42-1-03` conditional on reading ADD-03-p3-r1 until approval: م: ٣ | فئة الأصول: المعدات الميكانيكية | الحد الأدنى للعمر المتبقي (سنة): ٥ | أقصى درجة للحالة: ٣
- `ADD-03-T42-1-04` conditional on reading ADD-03-p3-r1 until approval: م: ٤ | فئة الأصول: المعدات الكهربائية وأجهزة القياس والتحكم | الحد الأدنى للعمر المتبقي (سنة): ٧ | أقصى درجة للحالة: ٣
- `ADD-03-T42-1-05` conditional on reading ADD-03-p3-r1 until approval: م: ٥ | فئة الأصول: الأغشية (إن وُجدت) | الحد الأدنى للعمر المتبقي (سنة): ٢٤ شهراً | أقصى درجة للحالة: ٣

## Per provision: source evidence → proposed transition → validation → downstream impact → output difference

### ADD-03:cover/para1 (paragraph, p1) — answered
- source: “Issued 17 November 2026”
- transition: `ADD-03/cover/para1/disp` disposition no_effect: Issue date line only: 'Issued 17 November 2026'. It amends nothing and imposes nothing; it fixes the stage date.
  - validation: **evidence_verified**

### ADD-03:cover/para2 (paragraph, p1) — answered
- source: “Tender NUPA/ISTP/2026/014”
- transition: `ADD-03/cover/para2/disp` disposition no_effect: Tender reference line only: 'Tender NUPA/ISTP/2026/014'. Identifies the tender; no amendment or obligation.
  - validation: **evidence_verified**

### ADD-03:cover/para3 (paragraph, p1) — answered
- source: “This Addendum reduces the threshold in Volume V Clause 36.2 for compensation for a General Change in Law to SAR 4,000,000, relocates the handback condition survey from Volume II to Volume V, replaces the remaining design life required at handback with minimum residual service lives for four asset classes set out in Table 42-1 (issued in Arabic), invites Bid…”
- transition: `ADD-03/cover/para3` amendment_op annotate ADD-03:cover/para3 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Target is the provision itself (cover/para3), not a unit of the pack that the provision amends. The op type 'annotate' on the cover paragraph does not amend any pack target; the obligation to acknowledge receipt in Form 4-A should be linked to Form 4-A (or the relevant requirement unit) if it exist…
    - concern: The cover text summarises and does not amend (shared policy). Treating a cover sentence as an operative obligation with effect 'adds_obligation' conflicts with that rule. Whether the cover sentence creates an obligation, or whether an operative provision elsewhere does, is for a person to decide. T…
    - concern: The note says other cover statements, e.g. 'SAR 4,000,000 in Vol V 36.2', differ from operative clause 2.1, and are reported in a separate issue. The evidence shown does not include clause 2.1 or that issue, so this claim can't be checked. The cover/operative differences are not quoted on both side…
    - concern: The cover also lists other changes: Table 42-1 issued in Arabic, Clause 12.5, borehole core inspection with an exception to Vol I Clause 4.2, and clarifications 15-19. This item does not account for them. The rationale says other batches cover them, but that can't be verified from this request.
    - concern: The cover text ends 'All other terms of the RFP Documents remain unchanged.' Its relationship to the new obligation is not addressed. No consequence for failing to acknowledge is stated in the evidence, and none should be inferred.
    - concern: The controller marks this interpretation_pending, which is appropriate. The quoted words 'Bidders shall acknowledge receipt in Form 4-A.' are verbatim, so the evidence quotation itself is fine.
  - downstream proposal `DS-001` row_new (c46:ADD-03/cover/para3): **interpretation_pending**
  - output difference: NEW ADD-03-cover-para3-01; A5 REWORK form-4a; A5 REWORK form-4a-prep

### ADD-03:1.1 (clause, p1) — answered
- source: “This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.”
- transition: `ADD-03/1.1/disp` disposition no_effect: Recital stating the authority for issue and that the Addendum 'takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2'; it restates …
  - validation: **evidence_verified**

### ADD-03:1.2 (clause, p1) — answered
- source: “A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.”
- transition: `ADD-03/1.2/disp` disposition unresolved: interpretive rule containing an exception ('unless otherwise stated'): 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or For…
  - validation: **evidence_verified**

### ADD-03:1.3 (clause, p1) — answered
- source: “Clarification requests 15 to 19 were received before the time stated in Volume I Clause 5.2.”
- transition: `ADD-03/1.3/disp` disposition no_effect: Recital of fact that requests 15 to 19 were received in time under Volume I Clause 5.2; no amendment or obligation. (Whether receipt was in time is a factual c…
  - validation: **evidence_verified**

### ADD-03:2.1 (clause, p1) — answered
- source: “The amount stated in Volume V Clause 36.2 is reduced by SAR 1,000,000.”
- transition: `ADD-03/cover/para3/issue` issue {"text": "ambiguous: the cover (ADD-03:cover/para3) says 'This Addendum reduces the threshold in Volume V Clause 36.2 for compensation for a General Change in Law to SAR 4,000,000', while operative c…
  - validation: **interpretation_pending — applied rule: VOL-I 3.2 provides: 'In the event of any conflict, ambiguity or discrepancy between or within the RFP Documents, the following order of precedence shall apply, the first named prevailing:' — the cover is the addendum's summary of itself, n…**
- transition: `ADD-03/2.1/disp` disposition unresolved: ambiguous: 2.1 prints a change ('is reduced by SAR 1,000,000') to VOL-V:36.2, whose ADD-02 text states SAR 2,500,000, but the cover states the threshold become…
  - validation: **evidence_verified**

### ADD-03:2.2 (clause, p1) — UNRESOLVED
- source: “Bidders shall take Section 2.1 into account in the Availability Payment quoted in Form 4-F.”
- transition: `ADD-03/2.2/row` row_new {"row": {"id": "ADD-03-2.2", "group": "ADD-03", "scope": ["Form 4-F"], "requirement": "Bidders shall take Section 2.1 into account in the Availability Payment quoted in Form 4-F.", "units": ["ADD-03:…
  - validation: **invalid** — payload: not a register.Row: 2 validation errors for Row interpretations.0.consequence.Consequence Input should be a valid dictionary or instance of Consequence [type=model_type, input_value='none stated in this provision', inpu…

### ADD-03:3.1 (clause, p1) — UNRESOLVED
- source: “Volume II Clause 8.5 is relocated to Volume V, in which it becomes Clause 42.3. Its text is unchanged and reads as follows: ‘42.3 A handback condition survey shall be carried out in the final two (2) years of the concession, and any remedial works identified shall be completed before transfer.’”
- transition: `ADD-03/3.1(a)` escalation why: software limitation: ADD-03:3.1 inserts a new Volume V Clause 42.3 ('42.3 A handback condition survey shall be carried out in the final two (2) years of the concession, and any remedial works identif…
  - validation: **escalated**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The 'software limitation' class fits: the dry run rejected insert_unit for VOL-V:42.3, which does not exist, and for VOL-V:42.2, which the provision does not cite. That is a tool limitation, not missing evidence.
    - concern: The provision says 'relocated'. Only the insertion of 42.3 is escalated here. The matching removal or relocation of VOL-II:8.5 is not covered by this item, and a person should confirm it is handled. VOL-II:8.5 is not shown as a unit with a stage text, so I cannot confirm that either way.
    - concern: The statement that the text is unchanged rests on ADD-03:3.1. The comparison with VOL-II:8.5 matches word for word on the evidence shown. The placement 'after VOL-V:42.2' is the proposer's inference, because the provision does not name a position. It should be flagged as such.
- transition: `ADD-03/3.1(b)` amendment_op set_status VOL-II:8.5
  - validation: **invalid** — previous_value: 'active' does not match VOL-II:8.5 at ADD-02 (it reads: 'A handback condition survey shall be carried out in the final two (2) years of the concession, and any remedial works identified shall be completed before tran…')
  - downstream proposal `DS-003` escalation (esc:ADD-03:3.1): **escalated**

### ADD-03:3.2 (clause, p1) — answered
- source: “The number 8.5 is not reused in Volume II, and the Clauses of Volume II are not renumbered.”
- transition: `ADD-03/3.2` disposition no_effect: Clarifies the numbering consequence of the relocation in 3.1 and prints no change of its own: 'The number 8.5 is not reused in Volume II, and the Clauses of Vo…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'renumbered')

### ADD-03:3.3 (clause, p1) — UNRESOLVED
- source: “In Volume V Clause 42.1, ‘Volume II Clause 8.5’ is deleted and ‘Clause 42.3’ is substituted.”
- transition: `ADD-03/3.3` amendment_op replace_text VOL-V:42.1 “Volume II Clause 8.5” → “Clause 42.3”
  - validation: **conflicting** — dependencies: unknown ids ['ADD-03/3.1(a)']
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-sonnet-5-5
    - concern: The replace_text op matches the provision wording and the previous_value of VOL-V:42.1 as it stood at ADD-02.
    - concern: The dependency id 'ADD-03/3.1(a)' failed validation as an unknown id. The dependency should be fixed or restated.
    - concern: Ops 3.3 and 3.4 both change VOL-V:42.1 at different spans. The controller flagged this as a consistency conflict. The two spans, 'Volume II Clause 8.5' and 'with a remaining design life...', do not overlap, so they look compatible. Whether the flag is a real conflict is for a person to decide. The …
    - concern: The change makes 42.1 point to Clause 42.3, which exists only if the escalated insertion in 3.1(a) is recorded. A person must resolve that first.
    - concern: The rationale says 'Simulated valid', but the dependency check failed. The rationale should not suggest a clean result.
  - downstream proposal `DS-004` escalation (esc:ADD-03:3.3): **escalated**

### ADD-03:3.4 (clause, p1) — UNRESOLVED
- source: “In Volume V Clause 42.1, ‘with a remaining design life of not less than five (5) years for all major assets’ is deleted and ‘with a residual service life, for each asset class, of not less than that stated in Table 42-1’ is substituted. Table 42-1 is reproduced at Appendix A to this Addendum and forms part of Volume V.”
- transition: `ADD-03/3.4` amendment_op replace_text VOL-V:42.1 “with a remaining design life of not less than five (5) years for all major asse…” → “with a residual service life, for each asset class, of not less than that state…”
  - validation: **conflicting** — statements: fact analysis-002/S1 is not supported verbatim
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-sonnet-5-5
    - concern: The replace_text op matches the provision wording and the target text.
    - concern: The controller says fact S1 is not supported verbatim, and the item itself declares missing information. The item therefore rests on unsupported evidence.
    - concern: The item states the Arabic row 5 value as '24 months' and the English as '24 (years)'. The English cell reads 24 under the column 'Minimum residual life (years)', and the Arabic reads ٢٤ شهراً, which means 24 months. S1 is presented as a fact. The conflict between 7 and 5, and between 24 months and…
    - concern: Evidence span for VOL-V:42.1 on page 4 is 'free of encumbrance and with a remaining design life...' and the proposer gives only part of the sentence. This is acceptable as a span, but the key change appears in the replacement text.
    - concern: The new wording makes 42.1 depend on Table 42-1. Which rendering of rows 4 and 5 applies is unresolved. The item correctly does not apply ADD-03:3.5. Even so, it is submitted as an amendment op that cannot be fully evaluated until the table question is settled.
    - concern: The consistency flag with 3.3 remains. The model rationale mixes an op with an issue; it should be kept apart.
    - concern: The rationale mentions English note (4) about the electrical equipment design life in Volume II Clause 2.2 being increased to 25 years. This is outside the batch but could be a further amendment and is not accounted for in the items shown. It should be listed as follow-on work.
- transition: `ADD-03/3.4-issue` escalation why: software limitation: the sentence 'Table 42-1 is reproduced at Appendix A to this Addendum and forms part of Volume V.' makes the table part of Volume V, but no op type inserts a table into a volume;…
  - validation: **escalated**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The sentence 'Table 42-1 is reproduced at Appendix A to this Addendum and forms part of Volume V.' does make the table part of Volume V. The software limitation class fits, because no op type inserts a table.
    - concern: The target ADD-03:T42-1 is the addendum's own table, not a VOL-V unit. The controller marked this as an uncertain target. A person should record where the table lands in Volume V.
    - concern: Appendix A is described as the place where the table is reproduced, while the Arabic rendering is on page 3 and the English at Appendix B is on page 4. The item does not say which one is 'Appendix A', so a person should check this. I cannot tell from the evidence shown.
  - downstream proposal `DS-005` escalation (esc:ADD-03:3.4): **escalated**

### ADD-03:3.5 (clause, p1) — answered
- source: “Table 42-1 is issued in the Arabic language. The Arabic text governs. The English translation at Appendix B is provided for convenience only.”
- transition: `ADD-03/3.5-issue` issue {"text": "ambiguous/conflict: ADD-03:3.5 says 'Table 42-1 is issued in the Arabic language. The Arabic text governs. The English translation at Appendix B is provided for convenience only.' The Arabi…
  - validation: **insufficient_evidence — HUMAN DECISION PENDING** — evidence ADD-03:T42-1/4 p4: cell evidence needs a column of ADD-03:T42-1/4 (['Asset class', 'Maximum condition grade', 'Minimum residual life (years)', 'No'])
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The issue is well founded in substance. 3.5 says the Arabic governs, and the Arabic rows 4 and 5 appear to differ from the English. The issue correctly reserves the reading for Legal.
    - concern: The controller status is insufficient_evidence. The two English cell evidence entries failed because they carry no column, and fact S1 is not supported verbatim. The evidence therefore needs correcting before the item can stand.
    - concern: The issue text opens with 'ambiguous/conflict', which merges two classes. The rules require one class per point. Here the real point is a conflict between the Arabic and English renderings, with 3.5 stating which governs. Whether the Arabic overrides the English is for a person, so it should be put…
    - concern: The English table row 5 gives 24 under a column headed 'years', and the Arabic gives 24 months in a column headed (سنة). I cannot verify from the evidence that the Arabic cell reading is complete. The crop itself is not shown, so the reading is not checked against the image here.
    - concern: The issue brings in the Arabic header date ١٥ نوفمبر ٢٠٢٦م and number ٤١٧/٢٠٢٦ with no evidence entry, and no reason is given for why it matters. Either quote it with evidence or remove it.
    - concern: The issue notes that rows 1 to 3 match. No evidence for rows 1 to 3 is listed in the item, so that claim is unsupported here.
- transition: `ADD-03/3.5` disposition unresolved: A language-precedence statement ('The Arabic text governs') that amends no unit text by itself; which rendering governs is a person's decision (Legal). The row…
  - validation: **evidence_verified**

### ADD-03:3.6 (clause, p1) — UNRESOLVED
- source: “The Bidder shall demonstrate in the Technical Proposal how its lifecycle plan achieves the residual service lives in Table 42-1.”
- transition: `ADD-03/3.6` row_new {"row": {"id": "ADD-03-3.6", "group": "ADD-03", "scope": "Technical Proposal", "requirement": "The Bidder shall demonstrate in the Technical Proposal how its lifecycle plan achieves the residual serv…
  - validation: **invalid** — payload: not a register.Row: 5 validation errors for Row scope Input should be a valid list [type=list_type, input_value='Technical Proposal', input_type=str] For further information visit https://errors.pydantic.dev/2.13/v/list…

### ADD-03:4.1 (clause, p2) — answered
- source: “The following new Clause 12.5 is inserted in Volume V after Clause 12.4: ‘12.5 If the Project Company encounters at the site ground conditions that are materially more adverse than those described in the Geotechnical Baseline Report, it shall be entitled to an extension of the Scheduled PCOD and to payment of its reasonable additional costs, provided that i…”
- transition: `ADD-03/4.1` amendment_op insert_unit VOL-V:12.4 “If the Project Company encounters at the site ground conditions that are materially more adverse than those described i…”
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: Minor: new_text omits the clause number label '12.5' and the surrounding quotation marks. The number appears only in the provision's lead-in, so the A2 record should keep the lead-in and the new clause number together.
    - concern: Minor: the inserted clause creates an entitlement (extension of Scheduled PCOD and reasonable additional costs) conditional on notice within five (5) Working Days. The evidence shows no stated consequence for late notice beyond the proviso itself, so none should be inferred. The A1 row and the date…
    - concern: Minor: the clause depends on the defined terms 'Scheduled PCOD' and 'Working Days' and on 'Revision C' of the Geotechnical Baseline Report. The evidence shown does not include the definitions or the report, so the dependency list covers only VOL-V:12.4. Whether the report was supplied in the pack i…
- transition: `ADD-03/4.1/row` row_new {"row": {"id": "A1-ADD03-4.1", "group": "ADD-03", "scope": ["Project Company", "Volume V Clause 12.5"], "requirement": "If the Project Company encounters at the site ground conditions that are materi…
  - validation: **invalid** — payload: not a register.Row: 2 validation errors for Row confidence Field required [type=missing, input_value={'id': 'A1-ADD03-4.1', 'g...llows a late notice.'}]}, input_type=dict] For further information visit https://errors.py…
  - downstream: units changed VOL-V:12.4+ADD-03; rows citing them none
  - downstream proposal `DS-002` row_new (c46:ADD-03/4.1): **interpretation_pending**
  - output difference: NEW ADD-03-4.1-01; A5 REWORK deviations-review; A5 REWORK form-4e

### ADD-03:4.2 (clause, p2) — UNRESOLVED
- source: “Each Bidder shall state in the Technical Proposal the ground conditions assumed for the design of foundations, by reference to the Geotechnical Baseline Report.”
- transition: `ADD-03/4.2/row` row_new {"row": {"id": "A1-ADD03-4.2", "group": "ADD-03", "scope": ["Bidder", "Technical Proposal"], "requirement": "Each Bidder shall state in the Technical Proposal the ground conditions assumed for the de…
  - validation: **invalid** — payload: not a register.Row: 2 validation errors for Row confidence Field required [type=missing, input_value={'id': 'A1-ADD03-4.2', 'g...a person to confirm."}]}, input_type=dict] For further information visit https://errors.py…

### ADD-03:4.3 (clause, p2) — UNRESOLVED
- source: “A Bidder that wishes to inspect the borehole cores and laboratory records on which the Geotechnical Baseline Report is based shall request an appointment through the Portal within three (3) Working Days of the date of this Addendum. Appointments will be held at the Authority's core store in Sakaka not later than three (3) Working Days before the Proposal Du…”
- transition: `ADD-03/4.3/row` row_new {"row": {"id": "A1-ADD03-4.3", "group": "ADD-03", "scope": ["Bidder", "Portal", "Authority's core store, Sakaka"], "requirement": "A Bidder that wishes to inspect the borehole cores and laboratory re…
  - validation: **invalid** — payload: not a register.Row: 2 validation errors for Row confidence Field required [type=missing, input_value={'id': 'A1-ADD03-4.3', 'g... no date typed here."}]}, input_type=dict] For further information visit https://errors.py…
  - downstream proposal `ADD-03-4.3-01` row_new (date:ADD-03:4.3): **interpretation_pending**
  - downstream proposal `ADD-03-4.3-02` row_new (date:ADD-03:4.3:within three (3) Working Days of the date of this Addendum): **interpretation_pending**
  - downstream proposal `ESC-DATE-4.3-WITHIN` escalation (date:ADD-03:4.3:within three (3) Working Days of the date of this Addendum): **escalated**
  - output difference: NEW ADD-03-4.3-01; NEW ADD-03-4.3-02

### ADD-03:4.4 (clause, p2) — UNRESOLVED
- source: “Volume I Clause 4.2 does not apply to communications with the Authority's geotechnical consultant during an appointment under Section 4.3, to the extent that they concern the identification and handling of cores and records.”
- transition: `ADD-03/4.4/esc` escalation why: software limitation: ADD-03:4.4 states that Volume I Clause 4.2 'does not apply' to a class of communications. That is a partial disapplication of a clause that carries disqualification ('Breach of t…
  - validation: **escalated**
- transition: `ADD-03/4.4/issue` issue {"text": "ambiguous: ADD-03:4.4 says 'Volume I Clause 4.2 does not apply to communications with the Authority's geotechnical consultant during an appointment under Section 4.3, to the extent that the…
  - validation: **insufficient_evidence — HUMAN DECISION PENDING** — evidence: no evidence given
  - downstream proposal `DS-006` escalation (esc:ADD-03:4.4): **escalated**

### ADD-03:Q15 (table_row, p2) — UNRESOLVED
- source: “No: 15 | Bidder question: Will the minutes of the Pre-Bid Conference at Appendix B to Addendum No. 1 be issued in Arabic? | Authority response: No. The minutes are issued in English only. Section 3.2 of Addendum No. 1 continues to apply to them.”
- transition: `ADD-03/Q15` amendment_op annotate ADD-01:3.2 effect confirms
  - validation: **invalid** — previous_value: no target to compare the previous value "Bidders' attention is drawn to Volume I Clause 5.3. Statements recorded in the minutes at Appendix B are a record of what was said and do not bind the Authority unless the substa…

### ADD-03:Q16 (table_row, p2) — UNRESOLVED
- source: “No: 16 | Bidder question: At what stage must the grievance mechanism referred to in Volume II Clause 9.3 be in place? | Authority response: The grievance mechanism shall be established before construction, shall be accessible to the affected community and shall be maintained for the concession period. Volume II Clause 9.3 applies.”
- transition: `ADD-03/Q16` amendment_op annotate VOL-II:9.3 effect confirms
  - validation: **invalid** — previous_value: no target to compare the previous value 'A grievance mechanism accessible to the affected community shall be established before construction and maintained for the concession period.' with

### ADD-03:Q17 (table_row, p2) — UNRESOLVED
- source: “No: 17 | Bidder question: Volume I Clause 10.1 states that no document other than Form 4-F and the Financial Model shall be placed in Envelope B, but Volume I Clause 10.6 requires a schedule of financing assumptions to be submitted with Form 4-F. Where is the schedule to be placed? | Authority response: The schedule required by Volume I Clause 10.6 forms pa…”
- transition: `ADD-03/Q17` amendment_op annotate VOL-I:10.6 effect adds_obligation
  - validation: **invalid** — previous_value: no target to compare the previous value 'The Bidder shall submit with Form 4-F a schedule of the principal financing assumptions underlying the Availability Payment, including the assumed debt tenor, margin and gearing.…

### ADD-03:Q18 (table_row, p2) — UNRESOLVED
- source: “No: 18 | Bidder question: Volume V Clause 39.5 refers to a Direct Agreement with the Senior Lenders. If the Direct Agreement provides for compensation on termination for Project Company default that differs from Volume V Clause 40.2, which prevails? | Authority response: The Authority notes the question. The order of precedence at Volume I Clause 3.2 applie…”
- transition: `ADD-03/Q18` disposition unresolved: ambiguous: the response says 'The order of precedence at Volume I Clause 3.2 applies' but does not say which of Volume V Clause 40.2 or a Direct Agreement prev…
  - validation: **insufficient_evidence** — evidence VOL-V:39.5 p0: page 0 is not a page of VOL-V:39.5 ([4])
- transition: `ADD-03/Q18-issue` issue {"text": "ambiguous: ADD-03:Q18 answers a question on whether a Direct Agreement or Volume V Clause 40.2 prevails on termination compensation with 'The order of precedence at Volume I Clause 3.2 appl…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-007` escalation (esc:ADD-03:Q18): **escalated**

### ADD-03:Q19 (table_row, p2) — answered
- source: “No: 19 | Bidder question: May Bidders inspect the borehole cores and laboratory records from the site investigation? | Authority response: Yes, by appointment. Section 4.3 of this Addendum applies. Requests made after the period stated in that Section will not be accommodated.”
- transition: `ADD-03/Q19` disposition unresolved: The response defers to ADD-03:4.3 ('Section 4.3 of this Addendum applies. Requests made after the period stated in that Section will not be accommodated.'), wh…
  - validation: **evidence_verified**

### ADD-03:AppA/para1 (paragraph, p3) — answered
- source: “The following table is reproduced as issued by the Authority's Asset Transfer Committee under cover of its letter No. 417/2026 dated 15 November 2026. The Arabic text governs in accordance with Section 3.5 of this Addendum.”
- transition: `ADD-03/AppA/para1/disp` disposition unresolved: The paragraph states 'The Arabic text governs in accordance with Section 3.5 of this Addendum.' This is a precedence statement; which text prevails is a person…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**

### ADD-03:T42-1/image/r1 (table_row, p3) — answered
- source: “م: ١ | فئة الأصول: المنشآت المدنية والخرسانية | الحد الأدنى للعمر المتبقي (سنة): ٢٠ | أقصى درجة للحالة: ٢”
- transition: `ADD-03/T42-1/image/r1/disp` disposition unresolved: Row 1 of the governing Arabic Table 42-1 (civil and concrete structures: minimum residual life 20, maximum condition grade 2) is operative content that clause …
  - validation: **evidence_verified**

### ADD-03:T42-1/image/r2 (table_row, p3) — UNRESOLVED
- source: “م: ٢ | فئة الأصول: خط نقل المياه المعالجة | الحد الأدنى للعمر المتبقي (سنة): ٢٠ | أقصى درجة للحالة: ٢”
- transition: `ADD-03/T42-1/image/r2/disp` disposition unresolved: ambiguous: Arabic row 2 reads 'خط نقل المياه المعالجة' (treated water transmission line) while English row 2 reads 'Treated effluent transmission main'. Crop v…
  - validation: **insufficient_evidence** — statements: fact analysis-003/S2 is not supported verbatim
  - downstream proposal `DS-008` escalation (esc:ADD-03:T42-1/image/r2): **escalated**

### ADD-03:T42-1/image/r3 (table_row, p3) — answered
- source: “م: ٣ | فئة الأصول: المعدات الميكانيكية | الحد الأدنى للعمر المتبقي (سنة): ٥ | أقصى درجة للحالة: ٣”
- transition: `ADD-03/T42-1/image/r3/disp` disposition unresolved: Row 3 of the Arabic Table 42-1 (mechanical equipment: 5 years, grade 3) is operative content made part of Volume V by clause 3.4; agrees with English row 3 as …
  - validation: **evidence_verified**

### ADD-03:T42-1/image/r4 (table_row, p3) — UNRESOLVED
- source: “م: ٤ | فئة الأصول: المعدات الكهربائية وأجهزة القياس والتحكم | الحد الأدنى للعمر المتبقي (سنة): ٧ | أقصى درجة للحالة: ٣”
- transition: `ADD-03/T42-1/image/r4/disp` disposition unresolved: ambiguous: Arabic row 4 (electrical, instrumentation and control equipment) shows minimum residual life ٧ (7) years, while English row 4 shows 5. Crop viewed: …
  - validation: **insufficient_evidence** — statements: fact analysis-003/S2 is not supported verbatim
- transition: `ADD-03/ISSUE/T42-1-arabic-english` issue {"text": "ambiguous: Table 42-1 Arabic (Appendix A) and English (Appendix B) differ. Row 2 class: Arabic 'خط نقل المياه المعالجة' vs English 'Treated effluent transmission main'. Row 4 minimum residu…
  - validation: **insufficient_evidence — HUMAN DECISION PENDING** — statements: fact analysis-003/S2 is not supported verbatim
  - downstream proposal `DS-009` escalation (esc:ADD-03:T42-1/image/r4): **conflicting — applied rule: ADD-03 3.5 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-sonnet-5-5
      - concern: The difference is real: Arabic row 4 (p3) gives ٧ (7) and English row 4 (p4) gives 5 for the same asset class. Both quotations are verbatim.
      - concern: The item ignores ADD-03 3.5, 'The Arabic text governs.', which the controller applied to this pair (applied, not decided). The rationale never quotes or mentions it. It calls the point 'ambiguous:' and says which rendering governs is open, without addressing the pack's own rule. A reader cannot tel…
      - concern: The controller's consistency check failed: the item reverses the earlier ADD-03/3.5-issue, which applied the Arabic-governs rule. The reversal is not justified by any new evidence.
      - concern: 'what_is_unsupported' says 'choosing between the Arabic and English renderings'. That is a human-decision point, not a software limitation, so the class is mislabelled. Class 1 (software limitation) is the wrong place for it.
      - concern: The proposer states 'I did not view the crop', and crop_sha256 is null. The shared rules require looking at the crop before proposing on a unit read from an image (Arabic table row). The digit ٧ is therefore unverified against the image, and the Arabic reading itself could be a misread.
      - concern: The item does not name dependants, such as any requirement or A5 rows built on the residual-life threshold. It says only that Arabic-based rows are conditional.

### ADD-03:T42-1/image/r5 (table_row, p3) — UNRESOLVED
- source: “م: ٥ | فئة الأصول: الأغشية (إن وُجدت) | الحد الأدنى للعمر المتبقي (سنة): ٢٤ شهراً | أقصى درجة للحالة: ٣”
- transition: `ADD-03/T42-1/image/r5/disp` disposition unresolved: ambiguous: Arabic row 5 (membranes, where provided) shows '٢٤ شهراً' (24 months) in a column headed 'الحد الأدنى للعمر المتبقي (سنة)' (minimum residual life, y…
  - validation: **insufficient_evidence** — statements: fact analysis-003/S2 is not supported verbatim
  - downstream proposal `DS-010` escalation (esc:ADD-03:T42-1/image/r5): **escalated**

### ADD-03:T42-1/image/notes-heading (reading_block, p3) — answered
- source: “ملاحظات:”
- transition: `ADD-03/T42-1/image/notes-heading/disp` disposition no_effect: Heading 'ملاحظات:' ('Notes:') only introduces the Arabic notes; it contains no obligation, exception or change. A person confirms.
  - validation: **evidence_verified**

### ADD-03:T42-1/image/note1 (reading_block, p3) — answered
- source: “١. تُقيَّم درجة الحالة وفق مقياس الهيئة لتصنيف حالة الأصول المكوَّن من خمس درجات، وتعني الدرجة ١ أن الأصل بحالة جديدة.”
- transition: `ADD-03/T42-1/image/note1/disp` disposition unresolved: Arabic note 1 defines how condition grade is assessed (Authority's five-point scale, grade 1 = new) and so gives meaning to the 'maximum condition grade' colum…
  - validation: **evidence_verified**

### ADD-03:T42-1/image/note2 (reading_block, p3) — answered
- source: “٢. يحدِّد المهندس المستقل العمر المتبقي لكل أصل في مسح الحالة الذي يُجرى قبل النقل.”
- transition: `ADD-03/T42-1/image/note2/disp` disposition unresolved: Arabic note 2 says the Independent Engineer determines each asset's residual life in the pre-transfer condition survey; it allocates a determination and ties t…
  - validation: **evidence_verified**

### ADD-03:T42-1/image/note3 (reading_block, p3) — answered
- source: “٣. يُستبدَل على نفقة شركة المشروع قبل تاريخ النقل كلَّ أصل لا يستوفي متطلبات هذا الجدول.”
- transition: `ADD-03/T42-1/image/note3/disp` disposition unresolved: Arabic note 3 obliges replacement, at the Project Company's cost before the transfer date, of any asset that does not meet the Table (matches English note (3))…
  - validation: **evidence_verified**

### ADD-03:T42-1/image/signatory (reading_block, p3) — answered
- source: “رئيس لجنة نقل الأصول”
- transition: `ADD-03/T42-1/image/signatory/disp` disposition no_effect: Signature block title 'رئيس لجنة نقل الأصول' (Chairman, Asset Transfer Committee) identifies the signatory only; no obligation, exception or change. A person c…
  - validation: **evidence_verified**

### ADD-03:T42-1/image/english (reading_block, p3) — answered
- source: “Northern Utilities Procurement Authority - Asset Transfer Committee FICTIONAL DOCUMENT - Lamar Holding internal assessment pack - not a real tender.”
- transition: `ADD-03/T42-1/image/english/disp` disposition no_effect: Letterhead/footer text on the page image (committee name and a fictional-document legend); it states no requirement, obligation or exception. A person confirms.
  - validation: **evidence_verified**

### ADD-03:AppA/para2 (paragraph, p3) — answered
- source: “End of reproduction.”
- transition: `ADD-03/AppA/para2/disp` disposition no_effect: 'End of reproduction.' only marks the end of Appendix A; no obligation, exception or change. A person confirms.
  - validation: **evidence_verified**

### ADD-03:AppB/para1 (paragraph, p4) — answered
- source: “This translation is provided for convenience only. The Arabic text of Table 42-1 at Appendix A governs. Asset Transfer Committee letter No. 417/2026 dated 15 November 2026. Subject: asset condition requirements on transfer of the Wadi Sirhan Independent Sewage Treatment Plant. Tender No. NUPA/ISTP/2026/014.”
- transition: `ADD-03/AppB/para1/disp` disposition unresolved: Precedence statement: 'The Arabic text of Table 42-1 at Appendix A governs.' Which text governs is a person's decision (Legal); the paragraph also records the …
  - validation: **interpretation_pending — HUMAN DECISION PENDING**

### ADD-03:AppB/para2 (paragraph, p4) — answered
- source: “The residual service life of each asset class at the date of transfer of the Facility to the Authority shall be not less than stated below.”
- transition: `ADD-03/AppB/para2/disp` disposition unresolved: This is the English qualifier of Table 42-1 ('shall be not less than stated below'), a convenience translation of the Arabic qualifier. It states an obligation…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**

### ADD-03:T42-1/1 (table_row, p4) — answered
- source: “No: 1 | Asset class: Civil and concrete structures | Minimum residual life (years): 20 | Maximum condition grade: 2”
- transition: `ADD-03/T42-1/1/disp` disposition unresolved: English convenience-translation row 1; agrees with Arabic row 1. Not governing per clause 3.5 (a person confirms); the register row follows the Arabic row and …
  - validation: **evidence_verified**

### ADD-03:T42-1/2 (table_row, p4) — UNRESOLVED
- source: “No: 2 | Asset class: Treated effluent transmission main | Minimum residual life (years): 20 | Maximum condition grade: 2”
- transition: `ADD-03/T42-1/2/disp` disposition unresolved: ambiguous: English row 2 'Treated effluent transmission main' differs from Arabic row 2 'خط نقل المياه المعالجة' (treated water transmission line). Translation…
  - validation: **insufficient_evidence** — statements: fact analysis-003/S2 is not supported verbatim
  - downstream proposal `DS-011` escalation (esc:ADD-03:T42-1/2): **escalated**

### ADD-03:T42-1/3 (table_row, p4) — answered
- source: “No: 3 | Asset class: Mechanical equipment | Minimum residual life (years): 5 | Maximum condition grade: 3”
- transition: `ADD-03/T42-1/3/disp` disposition unresolved: English convenience-translation row 3; agrees with Arabic row 3. Not governing per clause 3.5 (a person confirms).
  - validation: **evidence_verified**

### ADD-03:T42-1/4 (table_row, p4) — UNRESOLVED
- source: “No: 4 | Asset class: Electrical, instrumentation and control equipment | Minimum residual life (years): 5 | Maximum condition grade: 3”
- transition: `ADD-03/T42-1/4/disp` disposition unresolved: ambiguous: English row 4 shows minimum residual life 5 years; Arabic row 4 shows ٧ (7). Translation is for convenience only per clause 3.5; which value applies…
  - validation: **insufficient_evidence** — statements: fact analysis-003/S2 is not supported verbatim
  - downstream proposal `DS-012` escalation (esc:ADD-03:T42-1/4): **conflicting — applied rule: ADD-03 3.5 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-sonnet-5-5
      - concern: The figures differ as quoted: English 5 against Arabic ٧ (7). The evidence quotations are verbatim.
      - concern: The item does not mention ADD-03 3.5, 'The Arabic text governs.', which the controller applied to this pair. It presents the point as 'ambiguous:' without addressing the pack's own rule, and the stated owner (Technical/Legal) is not tied to any question about 3.5.
      - concern: It reverses the earlier ADD-03/3.5-issue (consistency check failed) with no new evidence.
      - concern: 'what_is_unsupported' is a human-decision matter, not a software limitation, so it is mislabelled. The note 'The controller did not support the analysis fact for this row' is unexplained and not backed by the evidence shown.
      - concern: No crop is cited (crop_sha256 null) for the Arabic row, which is read from an image. Nothing shows the image was checked.
      - concern: The item duplicates DS-009 from the English side and adds no distinct evidence or dependants.

### ADD-03:T42-1/5 (table_row, p4) — UNRESOLVED
- source: “No: 5 | Asset class: Membranes (where provided) | Minimum residual life (years): 24 | Maximum condition grade: 3”
- transition: `ADD-03/T42-1/5/disp` disposition unresolved: ambiguous: English row 5 shows 24 in the years column; Arabic row 5 shows '٢٤ شهراً' (24 months). Translation is for convenience only per clause 3.5; which uni…
  - validation: **insufficient_evidence** — statements: fact analysis-003/S2 is not supported verbatim
  - downstream proposal `ESC-T42-5` escalation (esc:ADD-03:T42-1/5): **escalated**

### ADD-03:T42-1/notes (note_intro, p4) — answered
- source: “Notes to Table 42-1:”
- transition: `ADD-03/T42-1/notes/disp` disposition no_effect: 'Notes to Table 42-1:' only introduces the notes; no obligation, exception or change. A person confirms.
  - validation: **evidence_verified**

### ADD-03:T42-1/note(1) (note, p4) — answered
- source: “(1) Condition grade is assessed on the Authority's five-point asset condition grading scale, grade 1 meaning as new.”
- transition: `ADD-03/T42-1/note(1)/disp` disposition unresolved: English note (1), a convenience translation of Arabic note 1, defines the condition-grade scale; agrees with Arabic. Governing text is the Arabic (clause 3.5);…
  - validation: **evidence_verified**

### ADD-03:T42-1/note(2) (note, p4) — answered
- source: “(2) The Independent Engineer determines the residual service life of each asset in the condition survey carried out before transfer.”
- transition: `ADD-03/T42-1/note(2)/disp` disposition unresolved: English note (2), a convenience translation of Arabic note 2, assigns determination of residual life to the Independent Engineer in the pre-transfer condition …
  - validation: **evidence_verified**

### ADD-03:T42-1/note(3) (note, p4) — answered
- source: “(3) Any asset that does not meet this Table shall be replaced at the Project Company's cost before the date of transfer.”
- transition: `ADD-03/T42-1/note(3)/disp` disposition unresolved: English note (3), a convenience translation of Arabic note 3: an obligation to replace non-compliant assets at the Project Company's cost before the transfer d…
  - validation: **evidence_verified**

### ADD-03:T42-1/note(4) (note, p4) — UNRESOLVED
- source: “(4) The design life of electrical equipment stated in Volume II Clause 2.2 is increased to twenty-five (25) years.”
- transition: `ADD-03/T42-1/note(4)/disp` disposition unresolved: ambiguous: English note (4) prints a change ('is increased to twenty-five (25) years') to the electrical-equipment design life in VOL-II:2.2 (effective text at…
  - validation: **insufficient_evidence** — statements: fact analysis-003/S2 is not supported verbatim
  - downstream proposal `ESC-NOTE4` escalation (esc:ADD-03:T42-1/note(4)): **escalated**

### ADD-03:AppB/para3 (paragraph, p4) — answered
- source: “Signed: Chairman, Asset Transfer Committee, Northern Utilities Procurement Authority (signature and stamp).”
- transition: `ADD-03/AppB/para3/disp` disposition no_effect: Signature block ('Signed: Chairman, Asset Transfer Committee ... (signature and stamp)') records who signed; no obligation, exception or change. A person confi…
  - validation: **evidence_verified**

## Downstream proposals (validated in the candidate)

| Item | Type | Task | Status | First failed check, or what a person confirms |
|---|---|---|---|---|
| DS-001 | row_new | c46:ADD-03/cover/para3 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-002 | row_new | c46:ADD-03/4.1 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-003 | escalation | esc:ADD-03:3.1 | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-004 | escalation | esc:ADD-03:3.3 | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-005 | escalation | esc:ADD-03:3.4 | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-006 | escalation | esc:ADD-03:4.4 | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-007 | escalation | esc:ADD-03:Q18 | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-008 | escalation | esc:ADD-03:T42-1/image/r2 | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-009 | escalation | esc:ADD-03:T42-1/image/r4 | conflicting — applied rule: ADD-03 3.5 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application | consistency (phases): reverses ADD-03/3.5-issue (ADD-03:3.5), which applied ADD-03 3.5 ('The Arabic text governs.'): this item hands the point back to a person; ADD-03 3.5 provides: 'The Arabic text … |
| DS-010 | escalation | esc:ADD-03:T42-1/image/r5 | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-011 | escalation | esc:ADD-03:T42-1/2 | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-012 | escalation | esc:ADD-03:T42-1/4 | conflicting — applied rule: ADD-03 3.5 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application | consistency (phases): reverses ADD-03/3.5-issue (ADD-03:3.5), which applied ADD-03 3.5 ('The Arabic text governs.'): this item hands the point back to a person; ADD-03 3.5 provides: 'The Arabic text … |
| ESC-T42-5 | escalation | esc:ADD-03:T42-1/5 | escalated | missing_information: the proposer declares missing: which unit (years or months) governs row 5 |
| ESC-NOTE4 | escalation | esc:ADD-03:T42-1/note(4) | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| ADD-03-T42-1-01 | row_new | reading:ADD-03-p3-r1 | interpretation_pending | a row reading is an interpretation: a person decides it |
| ADD-03-T42-1-02 | row_new | reading:ADD-03-p3-r1 | interpretation_pending | a row reading is an interpretation: a person decides it |
| ADD-03-T42-1-03 | row_new | reading:ADD-03-p3-r1 | interpretation_pending | a row reading is an interpretation: a person decides it |
| ADD-03-T42-1-04 | row_new | reading:ADD-03-p3-r1 | interpretation_pending | a row reading is an interpretation: a person decides it |
| ADD-03-T42-1-05 | row_new | reading:ADD-03-p3-r1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words declares a matter resolved ('resolved') |
| ISS-T42-5-UNIT | issue | reading:ADD-03-p3-r1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| ADD-03-4.3-01 | row_new | date:ADD-03:4.3 | interpretation_pending | a row reading is an interpretation: a person decides it |
| ADD-03-4.3-02 | row_new | date:ADD-03:4.3:within three (3) Working Days of the date of this Addendum | interpretation_pending | a row reading is an interpretation: a person decides it |
| ESC-DATE-4.3-WITHIN | escalation | date:ADD-03:4.3:within three (3) Working Days of the date of this Addendum | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |

- interactions: A5 with the proposals: C48: ADD-03-4.3-01 is an A1 row in force at ADD-03, but no activity carries it and no reason is given (its no_deliverable or post-award assessment in the register, or _row_chec…; A5 with the proposals: C48: ADD-03-4.3-02 is an A1 row in force at ADD-03, but no activity carries it and no reason is given (its no_deliverable or post-award assessment in the register, or _row_chec…; DS-009: reverses ADD-03/3.5-issue (ADD-03:3.5), which applied ADD-03 3.5 ('The Arabic text governs.'): this item hands the point back to a person; ADD-03 3.5 provides: 'The Arabic text governs.' (app…; DS-012: reverses ADD-03/3.5-issue (ADD-03:3.5), which applied ADD-03 3.5 ('The Arabic text governs.'): this item hands the point back to a person; ADD-03 3.5 provides: 'The Arabic text governs.' (app…
- A5 problems the proposals would add: C48: ADD-03-4.3-01 is an A1 row in force at ADD-03, but no activity carries it and no reason is given (its no_deliverable or post-award assessment in the register, or _row_checks / _row_exceptions in…; C48: ADD-03-4.3-02 is an A1 row in force at ADD-03, but no activity carries it and no reason is given (its no_deliverable or post-award assessment in the register, or _row_checks / _row_exceptions in…

## Promoted into the candidate (PROPOSED; nothing accepted)

- ops: ADD-03/cover/para3, ADD-03/4.1
- dispositions: ADD-03:cover/para1: no_effect, ADD-03:cover/para2: no_effect, ADD-03:1.1: no_effect, ADD-03:1.3: no_effect, ADD-03:3.2: no_effect, ADD-03:T42-1/image/notes-heading: no_effect, ADD-03:T42-1/image/signatory: no_effect, ADD-03:T42-1/image/english: no_effect, ADD-03:AppA/para2: no_effect, ADD-03:T42-1/notes: no_effect, ADD-03:AppB/para3: no_effect
- rows new: ADD-03-cover-para3-01, ADD-03-4.1-01, ADD-03-T42-1-01, ADD-03-T42-1-02, ADD-03-T42-1-03, ADD-03-T42-1-04, ADD-03-T42-1-05, ADD-03-4.3-01, ADD-03-4.3-02
- issues: I-ADD-03-T42-5-UNIT
- unresolved provisions: 19

- left out of the promoted ops: ADD-03/cover/para3/issue: an analysis issue is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; the downst…; ADD-03/Q18-issue: an analysis issue is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; the downst…

## check-register on the candidate

- exit 1; 8 finding(s) {'deliverable': 8}
  - [deliverable] ADD-03-4.1-01: post-award row with a blank 'evidence needed': give a proposed evidence requirement, a justified not-applicable entry or an unresolved specification
  - [deliverable] ADD-03-T42-1-01: post-award row with a blank 'evidence needed': give a proposed evidence requirement, a justified not-applicable entry or an unresolved specification
  - [deliverable] ADD-03-T42-1-02: post-award row with a blank 'evidence needed': give a proposed evidence requirement, a justified not-applicable entry or an unresolved specification
  - [deliverable] ADD-03-T42-1-03: post-award row with a blank 'evidence needed': give a proposed evidence requirement, a justified not-applicable entry or an unresolved specification
  - [deliverable] ADD-03-T42-1-04: post-award row with a blank 'evidence needed': give a proposed evidence requirement, a justified not-applicable entry or an unresolved specification
  - [deliverable] ADD-03-T42-1-05: post-award row with a blank 'evidence needed': give a proposed evidence requirement, a justified not-applicable entry or an unresolved specification
  - [deliverable] ADD-03-4.3-01: bid-stage row with no evidence item and no no_deliverable reason
  - [deliverable] ADD-03-4.3-02: bid-stage row with no evidence item and no no_deliverable reason

## Analysis rows carried to downstream tasks (and other analysis items not promoted)

- `ADD-03/cover/para3/issue` issue (ADD-03:2.1, interpretation_pending): an analysis issue is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; the downstream phase proposes issues and clarification entries against the candidate
- `ADD-03/Q18-issue` issue (ADD-03:Q18, interpretation_pending): an analysis issue is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; the downstream phase proposes issues and clarification entries against the candidate

## Coverage

- provisions: 49; accounted for by the combined set: 42; states {'validated': 49}
- resolution (controller): resolved 11, pending 30, invalid 4, unaccounted 4; approved 0
- structural units of ADD-03 that are not provisions (listed so nothing is dropped): ADD-03:H:cover (heading), ADD-03:H:cover-2 (heading), ADD-03:H:S1 (heading), ADD-03:H:S2 (heading), ADD-03:H:S3 (heading), ADD-03:H:S4 (heading), ADD-03:H:S5 (heading), ADD-03:S5/QA (table), ADD-03:H:AppA (heading), ADD-03:region:ADD-03-p3-r1 (region), ADD-03:T42-1/image (table), ADD-03:H:AppB (heading), ADD-03:T42-1 (table)
- batches: reading-ADD-03-p3-r1 done, analysis-001 done, analysis-002 done, analysis-003 done, analysis-004 done, analysis-005 done, downstream-001 done, downstream-002 done

## Critic (a second model over the selected items; it changed no status)

**Agreement between the critic and the proposer is not approval**: every item still needs a person's decision, and a disagreement is a concern for that person, not a rejection. The critic reviews only the selected classes (consequential interpretations, uncertain targets, removals, conflicting evidence), in one request per batch.

| Batch | Critic | Selected | Reviewed | Agrees | Does not agree | Note |
|---|---|---|---|---|---|---|
| analysis-001 | done | 1 | 1 | 0 | 1 |  |
| analysis-002 | done | 5 | 5 | 2 | 3 |  |
| analysis-003 | not_needed | 0 | - | - | - |  |
| analysis-004 | done | 1 | 1 | 1 | 0 |  |
| analysis-005 | not_needed | 0 | - | - | - |  |
| downstream-001 | done | 2 | 2 | 0 | 2 |  |
| downstream-002 | done | 5 | 5 | 4 | 1 |  |

- **ADD-03/cover/para3** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Target is the provision itself (cover/para3), not a unit of the pack that the provision amends. The op type 'annotate' on the cover paragraph does not amend any pack target; the obligation to acknowledge receipt in Form 4-A should be linked to Form 4-A (or the relevant requirement unit) if it exist…
    - concern: The cover text summarises and does not amend (shared policy). Treating a cover sentence as an operative obligation with effect 'adds_obligation' conflicts with that rule. Whether the cover sentence creates an obligation, or whether an operative provision elsewhere does, is for a person to decide. T…
    - concern: The note says other cover statements, e.g. 'SAR 4,000,000 in Vol V 36.2', differ from operative clause 2.1, and are reported in a separate issue. The evidence shown does not include clause 2.1 or that issue, so this claim can't be checked. The cover/operative differences are not quoted on both side…
    - concern: The cover also lists other changes: Table 42-1 issued in Arabic, Clause 12.5, borehole core inspection with an exception to Vol I Clause 4.2, and clarifications 15-19. This item does not account for them. The rationale says other batches cover them, but that can't be verified from this request.
    - concern: The cover text ends 'All other terms of the RFP Documents remain unchanged.' Its relationship to the new obligation is not addressed. No consequence for failing to acknowledge is stated in the evidence, and none should be inferred.
    - concern: The controller marks this interpretation_pending, which is appropriate. The quoted words 'Bidders shall acknowledge receipt in Form 4-A.' are verbatim, so the evidence quotation itself is fine.
- **ADD-03/3.1(a)** (analysis-002; controller status **escalated**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The 'software limitation' class fits: the dry run rejected insert_unit for VOL-V:42.3, which does not exist, and for VOL-V:42.2, which the provision does not cite. That is a tool limitation, not missing evidence.
    - concern: The provision says 'relocated'. Only the insertion of 42.3 is escalated here. The matching removal or relocation of VOL-II:8.5 is not covered by this item, and a person should confirm it is handled. VOL-II:8.5 is not shown as a unit with a stage text, so I cannot confirm that either way.
    - concern: The statement that the text is unchanged rests on ADD-03:3.1. The comparison with VOL-II:8.5 matches word for word on the evidence shown. The placement 'after VOL-V:42.2' is the proposer's inference, because the provision does not name a position. It should be flagged as such.
- **ADD-03/3.3** (analysis-002; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-sonnet-5-5
    - concern: The replace_text op matches the provision wording and the previous_value of VOL-V:42.1 as it stood at ADD-02.
    - concern: The dependency id 'ADD-03/3.1(a)' failed validation as an unknown id. The dependency should be fixed or restated.
    - concern: Ops 3.3 and 3.4 both change VOL-V:42.1 at different spans. The controller flagged this as a consistency conflict. The two spans, 'Volume II Clause 8.5' and 'with a remaining design life...', do not overlap, so they look compatible. Whether the flag is a real conflict is for a person to decide. The …
    - concern: The change makes 42.1 point to Clause 42.3, which exists only if the escalated insertion in 3.1(a) is recorded. A person must resolve that first.
    - concern: The rationale says 'Simulated valid', but the dependency check failed. The rationale should not suggest a clean result.
- **ADD-03/3.4** (analysis-002; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-sonnet-5-5
    - concern: The replace_text op matches the provision wording and the target text.
    - concern: The controller says fact S1 is not supported verbatim, and the item itself declares missing information. The item therefore rests on unsupported evidence.
    - concern: The item states the Arabic row 5 value as '24 months' and the English as '24 (years)'. The English cell reads 24 under the column 'Minimum residual life (years)', and the Arabic reads ٢٤ شهراً, which means 24 months. S1 is presented as a fact. The conflict between 7 and 5, and between 24 months and…
    - concern: Evidence span for VOL-V:42.1 on page 4 is 'free of encumbrance and with a remaining design life...' and the proposer gives only part of the sentence. This is acceptable as a span, but the key change appears in the replacement text.
    - concern: The new wording makes 42.1 depend on Table 42-1. Which rendering of rows 4 and 5 applies is unresolved. The item correctly does not apply ADD-03:3.5. Even so, it is submitted as an amendment op that cannot be fully evaluated until the table question is settled.
    - concern: The consistency flag with 3.3 remains. The model rationale mixes an op with an issue; it should be kept apart.
    - concern: The rationale mentions English note (4) about the electrical equipment design life in Volume II Clause 2.2 being increased to 25 years. This is outside the batch but could be a further amendment and is not accounted for in the items shown. It should be listed as follow-on work.
- **ADD-03/3.4-issue** (analysis-002; controller status **escalated**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The sentence 'Table 42-1 is reproduced at Appendix A to this Addendum and forms part of Volume V.' does make the table part of Volume V. The software limitation class fits, because no op type inserts a table.
    - concern: The target ADD-03:T42-1 is the addendum's own table, not a VOL-V unit. The controller marked this as an uncertain target. A person should record where the table lands in Volume V.
    - concern: Appendix A is described as the place where the table is reproduced, while the Arabic rendering is on page 3 and the English at Appendix B is on page 4. The item does not say which one is 'Appendix A', so a person should check this. I cannot tell from the evidence shown.
- **ADD-03/3.5-issue** (analysis-002; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The issue is well founded in substance. 3.5 says the Arabic governs, and the Arabic rows 4 and 5 appear to differ from the English. The issue correctly reserves the reading for Legal.
    - concern: The controller status is insufficient_evidence. The two English cell evidence entries failed because they carry no column, and fact S1 is not supported verbatim. The evidence therefore needs correcting before the item can stand.
    - concern: The issue text opens with 'ambiguous/conflict', which merges two classes. The rules require one class per point. Here the real point is a conflict between the Arabic and English renderings, with 3.5 stating which governs. Whether the Arabic overrides the English is for a person, so it should be put…
    - concern: The English table row 5 gives 24 under a column headed 'years', and the Arabic gives 24 months in a column headed (سنة). I cannot verify from the evidence that the Arabic cell reading is complete. The crop itself is not shown, so the reading is not checked against the image here.
    - concern: The issue brings in the Arabic header date ١٥ نوفمبر ٢٠٢٦م and number ٤١٧/٢٠٢٦ with no evidence entry, and no reason is given for why it matters. Either quote it with evidence or remove it.
    - concern: The issue notes that rows 1 to 3 match. No evidence for rows 1 to 3 is listed in the item, so that claim is unsupported here.
- **ADD-03/4.1** (analysis-004; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: Minor: new_text omits the clause number label '12.5' and the surrounding quotation marks. The number appears only in the provision's lead-in, so the A2 record should keep the lead-in and the new clause number together.
    - concern: Minor: the inserted clause creates an entitlement (extension of Scheduled PCOD and reasonable additional costs) conditional on notice within five (5) Working Days. The evidence shows no stated consequence for late notice beyond the proviso itself, so none should be inferred. The A1 row and the date…
    - concern: Minor: the clause depends on the defined terms 'Scheduled PCOD' and 'Working Days' and on 'Revision C' of the Geotechnical Baseline Report. The evidence shown does not include the definitions or the report, so the dependency list covers only VOL-V:12.4. Whether the report was supplied in the pack i…
- **DS-009** (downstream-001; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-sonnet-5-5
    - concern: The difference is real: Arabic row 4 (p3) gives ٧ (7) and English row 4 (p4) gives 5 for the same asset class. Both quotations are verbatim.
    - concern: The item ignores ADD-03 3.5, 'The Arabic text governs.', which the controller applied to this pair (applied, not decided). The rationale never quotes or mentions it. It calls the point 'ambiguous:' and says which rendering governs is open, without addressing the pack's own rule. A reader cannot tel…
    - concern: The controller's consistency check failed: the item reverses the earlier ADD-03/3.5-issue, which applied the Arabic-governs rule. The reversal is not justified by any new evidence.
    - concern: 'what_is_unsupported' says 'choosing between the Arabic and English renderings'. That is a human-decision point, not a software limitation, so the class is mislabelled. Class 1 (software limitation) is the wrong place for it.
    - concern: The proposer states 'I did not view the crop', and crop_sha256 is null. The shared rules require looking at the crop before proposing on a unit read from an image (Arabic table row). The digit ٧ is therefore unverified against the image, and the Arabic reading itself could be a misread.
    - concern: The item does not name dependants, such as any requirement or A5 rows built on the residual-life threshold. It says only that Arabic-based rows are conditional.
- **DS-012** (downstream-001; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-sonnet-5-5
    - concern: The figures differ as quoted: English 5 against Arabic ٧ (7). The evidence quotations are verbatim.
    - concern: The item does not mention ADD-03 3.5, 'The Arabic text governs.', which the controller applied to this pair. It presents the point as 'ambiguous:' without addressing the pack's own rule, and the stated owner (Technical/Legal) is not tied to any question about 3.5.
    - concern: It reverses the earlier ADD-03/3.5-issue (consistency check failed) with no new evidence.
    - concern: 'what_is_unsupported' is a human-decision matter, not a software limitation, so it is mislabelled. The note 'The controller did not support the analysis fact for this row' is unexplained and not backed by the evidence shown.
    - concern: No crop is cited (crop_sha256 null) for the Arabic row, which is read from an image. Nothing shows the image was checked.
    - concern: The item duplicates DS-009 from the English side and adds no distinct evidence or dependants.
- **ADD-03-T42-1-01** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The row is an image reading that no person has approved yet. crop_sha256 is null and model_rationale is null, so nothing shows that the crop was inspected.
    - concern: The text of note 3 (ADD-03:T42-1/image/note3) is not printed in the units shown. I rely on the controller's check that the quote was found.
    - concern: The consequence is a contractual replacement obligation at the project company's expense, not a rejection or disqualification. It should stay off A3. The controller already keeps it off A3 and A5 while the reading is pending.
    - concern: Whether the figures are a minimum or a maximum is read from the headings. The row quote carries 'الحد الأدنى للعمر المتبقي' and 'أقصى درجة للحالة', and the preamble says the remaining life 'يجب ألا يقل', so a minimum is consistent. A person still has to approve the reading.
- **ADD-03-T42-1-02** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: It is the same image reading, pending approval. crop_sha256 and model_rationale are null.
    - concern: The row cites reading ADD-03-p3-r1 while its evidence unit is r2. That matches the single table reading, but a person should confirm it.
    - concern: The text of note 3 is not printed in the units shown. I rely on the controller's check that the quote was found.
- **ADD-03-T42-1-03** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: It is the same image reading, pending approval. crop_sha256 and model_rationale are null.
    - concern: The text of note 3 is not printed in the units shown. I rely on the controller's check that the quote was found.
- **ADD-03-T42-1-04** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: It is the same image reading, pending approval. crop_sha256 and model_rationale are null.
    - concern: The text of note 3 is not printed in the units shown. I rely on the controller's check that the quote was found.
- **ADD-03-T42-1-05** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The printed '٢٤ شهراً' sits under a column headed '(سنة)'. That is a genuine ambiguity, but the note does not begin with 'ambiguous:' and does not quote both readings. It says only 'unit not resolved', and the confidence reason is not the required labelled statement.
    - concern: The confidence reason says 'the English-rendering cell says years'. No such cell appears in the evidence shown, and a translation is not evidence for the source. This claim is unsupported here and should be removed or quoted.
    - concern: The controller flagged the item as HUMAN DECISION PENDING because the word 'resolved' appears in its own words. The note should be reworded so it does not suggest the point is settled.
    - concern: min_remaining_life_printed keeps the text as printed, which is correct. But the row still carries the consequence from note 3 as if the threshold were fixed. It needs to state that the threshold (24 months or 24 years) is open, with the decision owner named (Technical). The issue I-ADD-03-T42-5-UNI…
    - concern: crop_sha256 is null, so nothing shows that the crop was inspected for the heading and unit.

## Requests: failures, deferrals, repairs and route notices

- every request was answered at the first call, parsed, and fitted its context

Route notices (how the requests were served; they change no status):
- **capabilities_declared** (reading-ADD-03-p3-r1): capabilities declared, not verified: host claude-code headless (the CLI's default model; recorded from the CLI output) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared,…
- **capabilities_declared** (analysis-001): capabilities declared, not verified: host claude-code headless (the CLI's default model; recorded from the CLI output) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared,…
- **capabilities_declared** (analysis-003): capabilities declared, not verified: host claude-code headless (the CLI's default model; recorded from the CLI output) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared,…
- **capabilities_declared** (downstream-001): capabilities declared, not verified: host claude-code headless (the CLI's default model; recorded from the CLI output) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared,…
- **capabilities_declared** (downstream-002): capabilities declared, not verified: host claude-code headless (the CLI's default model; recorded from the CLI output) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared,…

## Manual interventions (and automatic host sessions, named as such: not a person)

- 2026-10-06T20:16:05Z: host session (automatic) — batch reading-ADD-03-p3-r1 by tenderpack.ai.hostsession; host model claude-code headless (the CLI's default model; recorded from the CLI output); a headless host session reading an image; not a person
- 2026-10-06T20:20:03Z: host session (automatic) — batch analysis-001 by tenderpack.ai.hostsession; host model claude-code headless (the CLI's default model; recorded from the CLI output); a headless host session over the MCP tools; not a person
- 2026-10-06T20:27:54Z: host session (automatic) — batch analysis-003 by tenderpack.ai.hostsession; host model claude-code headless (the CLI's default model; recorded from the CLI output); a headless host session over the MCP tools; not a person
- 2026-10-06T20:31:31Z: host session (automatic) — batch downstream-001 by tenderpack.ai.hostsession; host model claude-code headless (the CLI's default model; recorded from the CLI output); a headless host session; not a person
- 2026-10-06T20:31:53Z: host session (automatic) — batch downstream-002 by tenderpack.ai.hostsession; host model claude-code headless (the CLI's default model; recorded from the CLI output); a headless host session; not a person

## The diff (ADD-02 → ADD-03; [diff.md](diff.md))

## What changed from ADD-02 to ADD-03

### ADD-03: PARTIAL (issued 2026-11-17)

- ops: 2 (0 invalid); provisions: 49 (36 unresolved)
- validated state: ADD-02 — this addendum does NOT replace it until every provision is treated and every op is valid
- UNRESOLVED ADD-03:1.2: A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.
- UNRESOLVED ADD-03:2.1: The amount stated in Volume V Clause 36.2 is reduced by SAR 1,000,000.
- UNRESOLVED ADD-03:2.2: Bidders shall take Section 2.1 into account in the Availability Payment quoted in Form 4-F.
- UNRESOLVED ADD-03:3.1: Volume II Clause 8.5 is relocated to Volume V, in which it becomes Clause 42.3. Its text is unchanged and reads as follows: ‘42.3  A handback condition survey s
- UNRESOLVED ADD-03:3.3: In Volume V Clause 42.1, ‘Volume II Clause 8.5’ is deleted and ‘Clause 42.3’ is substituted.
- UNRESOLVED ADD-03:3.4: In Volume V Clause 42.1, ‘with a remaining design life of not less than five (5) years for all major assets’ is deleted and ‘with a residual service life, for e
- UNRESOLVED ADD-03:3.5: Table 42-1 is issued in the Arabic language. The Arabic text governs. The English translation at Appendix B is provided for convenience only.
- UNRESOLVED ADD-03:3.6: The Bidder shall demonstrate in the Technical Proposal how its lifecycle plan achieves the residual service lives in Table 42-1.
- UNRESOLVED ADD-03:4.2: Each Bidder shall state in the Technical Proposal the ground conditions assumed for the design of foundations, by reference to the Geotechnical Baseline Report.
- UNRESOLVED ADD-03:4.3: A Bidder that wishes to inspect the borehole cores and laboratory records on which the Geotechnical Baseline Report is based shall request an appointment throug
- UNRESOLVED ADD-03:4.4: Volume I Clause 4.2 does not apply to communications with the Authority's geotechnical consultant during an appointment under Section 4.3, to the extent that th
- UNRESOLVED ADD-03:Q15: No: 15 | Bidder question: Will the minutes of the Pre-Bid Conference at Appendix B to Addendum No. 1 be issued in Arabic? | Authority response: No. The minutes 
- UNRESOLVED ADD-03:Q16: No: 16 | Bidder question: At what stage must the grievance mechanism referred to in Volume II Clause 9.3 be in place? | Authority response: The grievance mechan
- UNRESOLVED ADD-03:Q17: No: 17 | Bidder question: Volume I Clause 10.1 states that no document other than Form 4-F and the Financial Model shall be placed in Envelope B, but Volume I C
- UNRESOLVED ADD-03:Q18: No: 18 | Bidder question: Volume V Clause 39.5 refers to a Direct Agreement with the Senior Lenders. If the Direct Agreement provides for compensation on termin
- UNRESOLVED ADD-03:Q19: No: 19 | Bidder question: May Bidders inspect the borehole cores and laboratory records from the site investigation? | Authority response: Yes, by appointment. 
- UNRESOLVED ADD-03:AppA/para1: The following table is reproduced as issued by the Authority's Asset Transfer Committee under cover of its letter No. 417/2026 dated 15 November 2026. The Arabi
- UNRESOLVED ADD-03:T42-1/image/r1: م: ١ | فئة الأصول: المنشآت المدنية والخرسانية | الحد الأدنى للعمر المتبقي (سنة): ٢٠ | أقصى درجة للحالة: ٢
- UNRESOLVED ADD-03:T42-1/image/r2: م: ٢ | فئة الأصول: خط نقل المياه المعالجة | الحد الأدنى للعمر المتبقي (سنة): ٢٠ | أقصى درجة للحالة: ٢
- UNRESOLVED ADD-03:T42-1/image/r3: م: ٣ | فئة الأصول: المعدات الميكانيكية | الحد الأدنى للعمر المتبقي (سنة): ٥ | أقصى درجة للحالة: ٣
- UNRESOLVED ADD-03:T42-1/image/r4: م: ٤ | فئة الأصول: المعدات الكهربائية وأجهزة القياس والتحكم | الحد الأدنى للعمر المتبقي (سنة): ٧ | أقصى درجة للحالة: ٣
- UNRESOLVED ADD-03:T42-1/image/r5: م: ٥ | فئة الأصول: الأغشية (إن وُجدت) | الحد الأدنى للعمر المتبقي (سنة): ٢٤ شهراً | أقصى درجة للحالة: ٣
- UNRESOLVED ADD-03:T42-1/image/note1: ١. تُقيَّم درجة الحالة وفق مقياس الهيئة لتصنيف حالة الأصول المكوَّن من خمس درجات، وتعني الدرجة ١ أن الأصل بحالة جديدة.
- UNRESOLVED ADD-03:T42-1/image/note2: ٢. يحدِّد المهندس المستقل العمر المتبقي لكل أصل في مسح الحالة الذي يُجرى قبل النقل.
- UNRESOLVED ADD-03:T42-1/image/note3: ٣. يُستبدَل على نفقة شركة المشروع قبل تاريخ النقل كلَّ أصل لا يستوفي متطلبات هذا الجدول.
- UNRESOLVED ADD-03:AppB/para1: This translation is provided for convenience only. The Arabic text of Table 42-1 at Appendix A governs. Asset Transfer Committee letter No. 417/2026 dated 15 No
- UNRESOLVED ADD-03:AppB/para2: The residual service life of each asset class at the date of transfer of the Facility to the Authority shall be not less than stated below.
- UNRESOLVED ADD-03:T42-1/1: No: 1 | Asset class: Civil and concrete structures | Minimum residual life (years): 20 | Maximum condition grade: 2
- UNRESOLVED ADD-03:T42-1/2: No: 2 | Asset class: Treated effluent transmission main | Minimum residual life (years): 20 | Maximum condition grade: 2
- UNRESOLVED ADD-03:T42-1/3: No: 3 | Asset class: Mechanical equipment | Minimum residual life (years): 5 | Maximum condition grade: 3
- UNRESOLVED ADD-03:T42-1/4: No: 4 | Asset class: Electrical, instrumentation and control equipment | Minimum residual life (years): 5 | Maximum condition grade: 3
- UNRESOLVED ADD-03:T42-1/5: No: 5 | Asset class: Membranes (where provided) | Minimum residual life (years): 24 | Maximum condition grade: 3
- UNRESOLVED ADD-03:T42-1/note(1): (1)  Condition grade is assessed on the Authority's five-point asset condition grading scale, grade 1 meaning as new.
- UNRESOLVED ADD-03:T42-1/note(2): (2)  The Independent Engineer determines the residual service life of each asset in the condition survey carried out before transfer.
- UNRESOLVED ADD-03:T42-1/note(3): (3)  Any asset that does not meet this Table shall be replaced at the Project Company's cost before the date of transfer.
- UNRESOLVED ADD-03:T42-1/note(4): (4)  The design life of electrical equipment stated in Volume II Clause 2.2 is increased to twenty-five (25) years.
- cover summary vs provisions (C28, report only): 3 finding(s)
  - not found: 'reduces the threshold in Volume V Clause 36.2 for compensation for a General Change in Law to SAR 4, 000, 000, relocates the handback condition survey from Volume II to Volume V': no provision of ADD-03 does this
  - not found: 'replaces the remaining design life required at handback with minimum residual service lives for four asset classes set out in Table 42-1 (issued in Arabic), invites Bidders to describe in their Technical Proposals how their lifecycle plans address Table 42-1': no provision of ADD-03 does this
  - not found: 'requires Bidders to state the ground conditions assumed for the design of foundations, provides for the inspection of borehole cores and laboratory records with a limited exception to Volume I Clause 4.2': no provision of ADD-03 does this

#### Validated vs candidate (partial should not mean useless)

- validated (unchanged, ADD-02): `<outputs>/a3/a3.pdf` (one page), `<outputs>/a5/`
- candidate (CANDIDATE — NOT VALIDATED, ADD-03 as proposed): `<outputs>/a3/a3_candidate.pdf` / `.md`, `<outputs>/a5/candidate/`

**What may be changing.** ADD-03 is PARTIAL: 36 of 49 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 2 op(s) that are valid there stood (each still a proposal: review proposed 2), A3 would gain 0 row(s) (none), lose 0 (none) and change 0 (none); A5, replanned at ADD-03's issue date (2026-11-17), would move the latest dates of 0 activities (none), add 0 (none) and remove 0 (none), and marks 0 REVIEW through relationships. Not settled: 14 activities blocked by an unresolved row (fin-model-build, technical-proposal, lender-terms, deviations-review and 10 more), 0 STALE row(s), 0 obligation(s) reaching no output (C46), 0 relationship chain(s) blocked or incomplete, 3 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT and 6 more. Clarification route: the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person. Nothing here is validated, accepted or applied to the real state.

- **Clarification route:** the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person (ADD-03 issued 2026-11-17; the cut-off is computed from VOL-I-5.2-01 at that stage). No question about it is suggested as sendable; a proposed entry stays a DRAFT, not sent.

### Requirements

- new: 4; out of force: 0; changed: 0

- NEW ADD-03-cover-para3-01: NEW (introduced by ADD-03/cover/para3)
- NEW ADD-03-4.1-01: NEW (introduced by ADD-03/4.1) (by ADD-03/4.1)
- NEW ADD-03-4.3-01: NEW (introduced by ADD-03:4.3)
- NEW ADD-03-4.3-02: NEW (introduced by ADD-03:4.3)

### Stale readings and decisions

- no row is STALE

### Obligations not reaching the outputs (C46)

- none

### Reached through relationships (indirect: for review, not direct citations)

Curated links (relationships file) followed from what changed. The requirements above cite a changed unit; these are reached through another provision, in three classes that are never merged. A5 marks the activities that serve them REVIEW with their dates unchanged.

Relationship status: confirmed = stated in the documents (the entry quotes the cross-reference), not confirmed by a person; proposed = inferred by a curator or a model, a person decides; possible = a weaker inference.

#### Confirmed dependency (0)
- none

#### Proposed relationship (0)
- none

#### Possible impact (0)
- none

#### Referenced but not supplied: conclusions in play that cannot be established (0)
- none

### Disqualifiers (A3)

- no change

### Earlier answers to re-read against the new text (never revoked; a person decides)

- none

### Programme impact (status date 2026-10-22 -> 2026-11-17)

- STATUS assemble-envelope-a: timing INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD; total float -12 -> -30 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS assemble-envelope-b: timing OK -> INFEASIBLE by 18 WD; total float 0 -> -18 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS attendance-notice: timing CONDITIONAL — window elapsed 2026-10-14; whether the condition arose is not known -> CONDITIONAL — window elapsed 2026-10-14; whether the condition arose is not known; total float -7 -> -25 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS bond-approval: timing OK -> INFEASIBLE by 8 WD; total float +10 -> -8 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS bond-issue: timing OK -> INFEASIBLE by 8 WD; total float +10 -> -8 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS clarifications: timing OK -> DEADLINE PASSED; total float +13 -> -5 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS completion-certs: timing OK -> INFEASIBLE by 11 WD; total float +7 -> -11 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS consortium-check: timing OK -> INFEASIBLE by 5 WD; total float +13 -> -5 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS copies: timing INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD; total float -12 -> -30 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS deliver: timing INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD; total float -12 -> -30 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- REWORK deviations-review: requirement changed: ADD-03-4.1-01 (text, status, consequence, quote)
- STATUS deviations-review: timing OK -> INFEASIBLE by 7 WD; total float +11 -> -7 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS fin-assumptions: timing OK -> INFEASIBLE by 13 WD; total float +5 -> -13 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS fin-model-build: timing OK -> INFEASIBLE by 18 WD; total float 0 -> -18 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS fin-model-freeze: timing OK -> INFEASIBLE by 18 WD; total float 0 -> -18 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS fin-standing: timing OK -> INFEASIBLE by 3 WD; total float +15 -> -3 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS fin-statements: timing OK -> INFEASIBLE by 3 WD; total float +15 -> -3 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- REWORK form-4a: requirement changed: ADD-01-AppA-01 (Addenda to acknowledge: ADD-03 issued since ADD-02: 'Bidders shall acknowledge receipt in Form 4-A.'), ADD-03-cover-para3-01 (text, status, consequence, quote)
- NOT SETTLED form-4a: VOL-IV-F4A-01: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); VOL-IV-F4A-02: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); unchanged at this stage but not confirmed: a person decides
- STATUS form-4a: timing OK -> INFEASIBLE by 6 WD; total float +12 -> -6 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- REWORK form-4a-prep: requirement changed: ADD-01-AppA-01 (Addenda to acknowledge: ADD-03 issued since ADD-02: 'Bidders shall acknowledge receipt in Form 4-A.'), ADD-03-cover-para3-01 (text, status, consequence, quote)
- NOT SETTLED form-4a-prep: VOL-IV-F4A-01: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); VOL-IV-F4A-02: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); unchanged at this stage but not confirmed: a person decides
- STATUS form-4a-prep: timing OK -> OK; total float +20 -> +2 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS form-4b: timing OK -> INFEASIBLE by 11 WD; total float +7 -> -11 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS form-4b-prep: timing OK -> INFEASIBLE by 9 WD; total float +9 -> -9 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS form-4c-prep: timing OK -> OK; total float +18 -> 0 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS form-4c-sign: timing OK -> INFEASIBLE by 8 WD; total float +10 -> -8 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- REWORK form-4e: requirement changed: ADD-03-4.1-01 (text, status, consequence, quote)
- STATUS form-4e: timing OK -> INFEASIBLE by 17 WD; total float +1 -> -17 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS form-4f: timing OK -> INFEASIBLE by 18 WD; total float 0 -> -18 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS form-4g-review: timing OK -> INFEASIBLE by 1 WD; total float +17 -> -1 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS form-4g-sign: timing OK -> INFEASIBLE by 6 WD; total float +12 -> -6 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS ground-dd: timing OK -> INFEASIBLE by 13 WD; total float +5 -> -13 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS investment-licence: timing OK -> INFEASIBLE by 10 WD; total float +8 -> -10 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS iso-copy: timing OK -> OK; total float +21 -> +3 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS lcc-certificate: timing INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD; total float -12 -> -30 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- STATUS lcc-ratio: timing INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD; total float -12 -> -30 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
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
- STATUS technical-proposal: timing OK -> INFEASIBLE by 17 WD; total float +1 -> -17 WD; the planning date moved 2026-10-22 -> 2026-11-17, which by itself shifts every float by the Working Days between them
- FEASIBILITY lcc-ratio: INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD
- FEASIBILITY lcc-certificate: INFEASIBLE by 12 WD -> INFEASIBLE by 30 WD
- FEASIBILITY fin-model-build: OK -> INFEASIBLE by 18 WD
- FEASIBILITY model-auditor-appoint: OK -> INFEASIBLE by 17 WD
- FEASIBILITY technical-proposal: OK -> INFEASIBLE by 17 WD
- FEASIBILITY pcg-wording: OK -> INFEASIBLE by 15 WD
- FEASIBILITY ground-dd: OK -> INFEASIBLE by 13 WD
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
- FEASIBILITY form-4b-prep: OK -> INFEASIBLE by 9 WD
- FEASIBILITY bond-issue: OK -> INFEASIBLE by 8 WD
- FEASIBILITY fin-standing: OK -> INFEASIBLE by 3 WD
- FEASIBILITY form-4c-sign: OK -> INFEASIBLE by 8 WD
- FEASIBILITY fin-assumptions: OK -> INFEASIBLE by 13 WD
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

- read the unresolved and escalated provisions first, then each item against its evidence (`../ai/ADD-03-run-host-20261006T201359Z-2503-combined/proposals.yaml`, `../downstream/proposals.yaml`)
- nothing here is applied to the real curation: to take an item over, add the PDF to the pack (OPERATING_GUIDE §3 steps 1-2) and copy the reviewed files listed in `promotion.json`; then `pin`, `check-register`, `outputs` and decide with `accept` / `reject` as usual
