# Review packet: ADD-03, AI workflow run ADD-03-run-host-20261008T053735Z-77b2

> **CANDIDATE: proposed by the AI workflow; not reviewed; nothing accepted.** Statuses are the controller's; a person decides every item. The real `curation/`, `config/` and `out/` were only read: everything below lives in this run's folder.

- PDF: `/tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s14/pkg/blind08/unzipped/LAMAR-PPP-R2-INTERVIEW_7c721d4+wt_20261008T0536Z/staging/panel/uploads/6a7adf78638ecf2f4a982950c072467c96dab977ad50cf87946f22e644b74164.pdf` (sha256 6a7adf78638ecf2f…, 4 pages); preceding state: pack `/tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s14/pkg/blind08/unzipped/LAMAR-PPP-R2-INTERVIEW_7c721d4+wt_20261008T0536Z/config/pack.yaml` (NUPA-ISTP-2026-014), previous evidence build `/tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s14/pkg/blind08/unzipped/LAMAR-PPP-R2-INTERVIEW_7c721d4+wt_20261008T0536Z/build`
- route **host**; model requested `claude-code headless (claude-opus-5-5)`, reported `None`; host sessions report: claude-opus-5-5
- status **partial**: 23 provision(s) unresolved in the candidate (listed first in the review packet); 4 downstream task(s) answered only by items that cannot be promoted: esc:ADD-03:3.3, esc:ADD-03:Q16, impact:APPENDIX A — TABLE 8-1 (ARABIC), impact:APPENDIX B — ENGLISH TRANSLATION OF TABLE 8-1; check-register on the candidate: exit 1, 2 finding(s) {'C46': 1, 'pending_settled': 1} (0 missing because the downstream phase did not propose them, 2 defect(s)); C46: [C46] ADD-03/cover/para3: [A3] ADD-03/cover/para3 brings in consequence words ['rejected'] that no row's consequence carries at ADD-03: 'SYNTHETIC: not tender …
- usage (application routes): none: the run's route is host, every exchange ran in a host session (below)
- host sessions: 3 (their own records); usage of the 3 that reported it: input 36, cache write 142641, cache read 527593 / output 44860 tokens
- code at start: content a9ebd02ab0cbf8a7… over 99 files; git not available; recorded 2026-10-08T05:37:36Z

## Execution, completeness and approval (three separate things)

- **Execution** (what ran): ingest done, readings done, analysis done, validation done, downstream done, downstream_validation done, critic done, promotion done, pin done, check_register done, outputs done, diff done, review running; batches reading: {'done': 1}; analysis: {'done': 6}; downstream: {'done': 3}
- **Completeness** (what the run completed): **partial**: 23 provision(s) unresolved in the candidate (listed first in the review packet); 4 downstream task(s) answered only by items that cannot be promoted: esc:ADD-03:3.3, esc:ADD-03:Q16, impact:APPENDIX A — TABLE 8-1 (ARABIC), impact:APPENDIX B — ENGLISH TRANSLATION OF TABLE 8-1; check-register on the candidate: exit 1, 2 finding(s) {'C46': 1, 'pending_settled': 1} (0 missing because the downstream phase did not propose them, 2 defect(s)); C46: [C46] ADD-03/cover/para3: [A3] ADD-03/cover/para3 brings in consequence words ['rejected'] that no row's consequence carries at ADD-03: 'SYNTHETIC: not tender …
  - downstream tasks: 25; answered 21; unanswered 0; answered only by items that cannot be promoted 4; answered 'no change' 3
- **Human approval**: **none** (nothing approved, accepted, rejected or sent); no decision is recorded in the candidate's decisions file

## What is candidate and what is real

- **Candidate** (proposed by this run, nothing accepted): `../candidate/` — a copy of the curation and configuration with ADD-03 added, its evidence build, its op file, rows, issues, templates and outputs.
- **Last validated state**: `../candidate/out-before/` (the pre-addendum outputs built from the copied curation and the previous evidence build; done)
- **Real** (untouched): `curation/`, `config/`, `out/`; the owner's approvals and readings were copied unchanged and used read-only.

- real inputs changed since the run started: none

## Candidate outputs

Exit 0 (WORKING DRAFT (not releasable)); every file carries the banner (`../candidate/out/CANDIDATE.md`); A1 has a candidate status column {'proposed (existing row; not changed by this run; not reviewed)': 200, 'PROPOSED BY THE AI WORKFLOW': 14, 'UNRESOLVED (value in question)': 1}.

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

- before → after: {"a1": {"rows_before": 205, "rows_after": 215, "new": 10, "gone": 0}, "a3": {"before": 17, "after": 17, "enters": 0, "leaves": 0}, "a5": {"activities_before": 44, "activities_after": 45, "new": 1, "gone": 0}}

- ADD-03 is **PARTIAL** in the candidate (provisions unresolved): A3 and the A5 programme show the validated state (ADD-02); ADD-03 as proposed is in A1's `Status after ADD-03` column, in A2, in the candidate A3 and A5 below, in `a5/working/ADD-03.json` and in the diff below.

### Validated and candidate A3 / A5 (partial should not mean useless)

- **Validated** (unchanged; ADD-02): [a3/a3.pdf](../candidate/out/a3/a3.pdf) (one page), [a5/README.md](../candidate/out/a5/README.md), [a5/gantt.html](../candidate/out/a5/gantt.html)
- **Candidate** (CANDIDATE — NOT VALIDATED; ADD-03 as proposed): [a3/a3_candidate.pdf](../candidate/out/a3/a3_candidate.pdf) (9 page(s)), [a3/a3_candidate.md](../candidate/out/a3/a3_candidate.md), [a5/candidate/README.md](../candidate/out/a5/candidate/README.md), [a5/candidate/gantt.html](../candidate/out/a5/candidate/gantt.html)

**What may be changing.** ADD-03 is PARTIAL: 23 of 52 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 7 op(s) that are valid there stood (each still a proposal: review proposed 7), A3 would gain 1 row(s) (ADD-03-2.4-01 (register)), lose 0 (none) and change 0 (none); A5, replanned at ADD-03's issue date (2026-11-18), would move the latest dates of 0 activities (none), add 1 (cir-portal-notification) and remove 0 (none), and marks 9 REVIEW through relationships. Not settled: 4 activities blocked by an unresolved row (deviations-review, investment-licence, form-4e, cir-portal-notification), 0 STALE row(s), 1 obligation(s) reaching no output (C46), 0 relationship chain(s) blocked or incomplete, 5 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT and 6 more. Clarification route: the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person. Nothing here is validated, accepted or applied to the real state.

- ENTERS ADD-03-2.4-01: gate (pass/fail gate); ops none (reading re-made at ADD-03 (register); status NOT IN FORCE (introduced at ADD-03 by ADD-03:2.4) -> NEW (introduced by ADD-03:2.4); NOT SETTLED: ADD-03:2.4 UNRESOLVED: not promotable: ADD-03/2.4 interpretation_pending (dropped: not ready: promotion waits while depends on ADD-03/2.1 (amendment_op, conflicting)); ADD-03/2.4-row…)

- blockers: 23 unresolved provision(s), 4 blocked activit(y/ies), 0 STALE row(s), 1 C46 gap(s), 0 relationship chain(s) blocked or incomplete, 5 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT, I-VOL-III, I-VOL-II-MISSING, I-VOL-V-MISSING, I-VOL-II-COMPLIANCE-POINT, I-VOL-IV-SCALE, I-OP-ADD-01/Q4
- conditional scenarios: 0

**Image-read units** (the review packet of each region shows every crop beside its reading; translations are proposals, not evidence):

- ADD-03-p3-r1 (ADD-03 p3; reading pending): [packet](../candidate/build/review/ADD-03-p3-r1/packet.html); 18 unit(s) touched
  - `ADD-03:p3-image`: “جدول ٨-١: مدد إصدار شهادة تسجيل الاستثمار يُصدر المكتب شهادة تسجيل الاستثمار للعضو المؤسس خارج المملكة خلال المدة المبيِّنة أدناه لفئته:”; issues I-INVREG-CONSEQUENCE, I-INVREG-VALIDITY
  - `ADD-03:p3-image/r1`: “م: ١ / فئة العضو: شركة مؤسسة في إحدى دول مجلس التعاون الخليجي / المستندات المطلوبة مع الطلب: السجل التجاري مصدقاً / مدة الإصدار (أيام عمل): ٣”; issues I-INVREG-CONSEQUENCE
  - `ADD-03:p3-image/r2`: “م: ٢ / فئة العضو: شركة مؤسسة خارج دول مجلس التعاون الخليجي / المستندات المطلوبة مع الطلب: السجل التجاري والقوائم المالية المدققة لآخر سنة مالية، مصدقة / مدة الإصدار (أيام عمل): ٥”
  - `ADD-03:p3-image/r3`: “م: ٣ / فئة العضو: فرع مسجل في المملكة لشركة أجنبية / المستندات المطلوبة مع الطلب: شهادة تسجيل الفرع وقرار مجلس إدارة الشركة الأم بتفويض الفرع / مدة الإصدار (أيام عمل): ٨”; issues I-INVREG-CONSEQUENCE
  - `ADD-03:p3-image/hdr-en`: “Northern Region Investment Services Office”
  - `ADD-03:p3-image/hdr-ar`: “مكتب خدمات الاستثمار بالمنطقة الشمالية”; translation (apart): ‘Investment Services Office in the Northern Region’
  - `ADD-03:p3-image/date`: “التاريخ: ١٦ نوفمبر ٢٠٢٦م”; translation (apart): ‘Date: 16 November 2026 AD’
  - `ADD-03:p3-image/ref`: “الرقم: ٢٢٨/٢٠٢٦”; translation (apart): ‘No.: 228/2026’
  - `ADD-03:p3-image/to`: “إلى: الهيئة الشمالية للمشتريات المرفقية”; translation (apart): ‘To: the Northern Utilities Procurement Authority’
  - `ADD-03:p3-image/subject`: “الموضوع: تسجيل استثمار أعضاء الائتلافات المؤسسين خارج المملكة”; translation (apart): ‘Subject: investment registration of consortium founding members outside the Kingdom’
  - `ADD-03:p3-image/tender`: “مناقصة رقم: NUPA/ISTP/2026/014 (محطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان)”; translation (apart): ‘Tender No.: NUPA/ISTP/2026/014 (Wadi Al-Sirhan Independent Sewage Treatment Plant)’
  - `ADD-03:p3-image/notes-heading`: “ملاحظات:”; translation (apart): ‘Notes:’
  - … 6 more in `a3/a3_candidate.md`
- VOL-II-p3-r1 (VOL-II p3; reading approved): [packet](../candidate/build/review/VOL-II-p3-r1/packet.html); not touched by this addendum
- VOL-IV-p6-r1 (VOL-IV p6; reading approved): [packet](../candidate/build/review/VOL-IV-p6-r1/packet.html); 4 unit(s) touched
  - `VOL-IV:F4-C/image`: “Form 4-C (image, Arabic with English labels): Conflict of Interest and Debarment Declaration”; issues I-BIDDER-FACTS
  - `VOL-IV:F4-C/image/decl2`: “ثانياً: أن الشركة لم تشارك، بصورة مباشرة أو غير مباشرة، في أكثر من عرض واحد لهذه المناقصة.”; translation (apart): ‘Second: that the company has not participated, directly or indirectly, in more than one proposal for this tender.’; issues I-BIDDER-FACTS, I-NO-CONSEQUENCE, I-READING-F4C
  - `VOL-IV:F4-C/image/decl3`: “ثالثاً: أن الشركة غير مدرجة، ولم تكن مدرجة خلال الخمس سنوات السابقة، في أي قائمة حظر صادرة عن جهة حكومية في المملكة.”; translation (apart): ‘Third: that the company is not listed, and has not been listed during the previous five years, on any debarment list issued by a government body in the Kingdom.’; issues I-BIDDER-FACTS, I-NO-CONSEQUENCE, I-READING-F4C
  - `VOL-IV:F4-C/image/note`: “ملاحظة: يجب تقديم هذا النموذج باللغة العربية عن كل عضو من أعضاء الائتلاف. عدم تقديمه كاملاً يجعل العرض غير مستجيب.”; translation (apart): ‘Note: this form must be submitted in Arabic for each member of the consortium. Failure to submit it complete renders the proposal non-responsive.’; issues I-READING-F4C

## Timings (wall clock per step)

| Step | Seconds | Status |
|---|---|---|
| ingest | 14.4 | done |
| readings | 156.7 | done |
| analysis | 1638.4 | done |
| validation | 6.1 | done |
| downstream | 712.4 | done |
| downstream_validation | 0.9 | done |
| critic | 117.6 | done |
| promotion | 13.7 | done |
| pin | 1.4 | done |
| check_register | 4.7 | done |
| outputs | 25.2 | done |
| diff | 4.9 | done |
| review | 0.0 | running |
| **total** | **2696.4** (44.9 min) | target 30 min from the PDF to candidate outputs and this packet, human review excluded |

## Readings of the addendum's image regions (AI-proposed, PENDING HUMAN REVIEW)

Ingest first refused the candidate because these image regions had no reading (C05): ADD-03-p3-r1. Each reading below was proposed by the route of this run, checked by readings.check_reading and written into the candidate's readings; it is an interpretation of an image, never approved, and every unit made from it carries `reading.status: pending`.

- **ADD-03-p3-r1** — done; controller status **interpretation_pending**; unit `ADD-03:p3-image`; file `../candidate/curation/readings/ADD-03-p3-r1.yaml`
  - the reading beside its crops (the build's review packet): [../candidate/build/review/ADD-03-p3-r1/packet.html](../candidate/build/review/ADD-03-p3-r1/packet.html)
  - form reading, languages ['ar', 'en']; prepared by: AI-assisted: headless host session ADD-03-hostsession-20261008T053751Z-4323 (claude-code headless (claude-opus-5-5); the CLI reported claude-opus-5-5), in AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (reading-ADD-03-p3-r1), 2026-10-08T05:40:14Z; proposed for a person's review, not approved
  - uncertainty: The letterhead, addressee, subject, tender reference, signature block, stamp and footer are recorded in table.notes with their own roles (letterhead, letter-date, addressee, subject, stamp, signature-block, image-footer). The reading check…
  - uncertainty: Band 18 left holds only an empty oval stamp outline with no legible text; its line is recorded with an empty source.
  - uncertainty: Column headings are printed over two lines (المستندات المطلوبة / مع الطلب; مدة الإصدار / (أيام عمل)); joined with a space.
  - uncertainty: Translations of the table headings and cells (the schema has no cell translation field): no = No.; category = Member category; documents = Documents required with the application; period = Issue period (working days). Row 1: company incorp…
  - uncertainty: Shadda/kasra on المبيِّنة (bands 6 and 17) read at native resolution; matching text removes tashkeel.

## First: unresolved provisions and escalations

23 of 52 provisions are not applied or settled by a promoted item (each is `unresolved` in the candidate op file with the reason); 2 escalation(s).
- states (session 14: kept distinct): applied 9, no effect 20, partly applied 0, unresolved but accounted for 5, unaccounted 18; approved by a person: none (only a person's recorded decision approves; see Human approval above)

- **Clarification route:** the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person (ADD-03 issued 2026-11-18; the cut-off is computed from VOL-I-5.2-01 at that stage). No question about it is suggested as sendable; a proposed entry stays a DRAFT, not sent.

- **ESCALATED ADD-03/Q16** (ADD-03:Q16): software limitation: Q16 prints a relative change 'the issue period in row 2 of Table 8-1 is reduced by two (2) Working Days' that applies only 'for an application lodged not later than Sunday 22 November 2026'. Table 8-1 does not exist at ADD-02: it is inserted by Section 2.2 of this same Addendum…
  - unsupported: an adjust_value on a cell of a table inserted by the same addendum from a pending image reading, applying per application by lodging date (a conditional, application-specific variant of a table value)
  - evidence: ADD-03:Q16 p2: “The Office has confirmed to the Authority that, for an application lodged not later than Sunday 22 November 2026, the issue period in row 2 of Table 8-1 is red…”; ADD-03:p3-image/r2 p3: “شركة مؤسسة خارج دول مجلس التعاون الخليجي | المستندات المطلوبة مع الطلب: السجل التجاري والقوائم المالية المدققة لآخر سنة مالية، مصدقة | مدة الإصدار (أيام عمل): ٥”
  - affected scope: units none; rows none; activities none; clarifications none
- **ESCALATED ADD-03/3.3** (ADD-03:3.3): software limitation: ADD-03:3.3 prints a relative change "the period of thirty-six (36) months is increased by six (6) months" of VOL-V:12.1, whose effective text at ADD-02 reads "The Project Company shall achieve PCOD within thirty-six (36) months of the Notice to Proceed (the Scheduled PCOD)." Th…
  - unsupported: adjust_value cannot rewrite a previous value stated in both words and figures ('thirty-six (36) months'); the op (e.g. a replace_text with the new words) must be written by a person (Document control).
  - evidence: ADD-03:3.3 p2: “In Volume V Clause 12.1, the period of thirty-six (36) months is increased by six (6) months.”; VOL-V:12.1 p2: “The Project Company shall achieve PCOD within thirty-six (36) months of the Notice to Proceed (the Scheduled PCOD).”; ADD-03:cover/para3 p1: “extends the Scheduled PCOD in Volume V Clause 12.1 to forty-two (42) months”
  - affected scope: units VOL-V:12.1; rows VOL-V-12.1-01; activities none; clarifications CQ-VOL-V-SCHEDULES
- **UNRESOLVED ADD-03:2.1** (clause, p1): not promotable: ADD-03/2.1 conflicting (consistency: VOL-I:8.9: ADD-03/2.1, ADD-03/2.4 change the same unit in different ways across the set); ADD-03/2.1-row interpretation_pending (dropped: not ready: promotion waits while depends on ADD-03/2.1 (amendment_op, conflicting)) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:2.2** (clause, p1): not promotable: ADD-03/2.2 insufficient_evidence (dependencies: unknown ids ['S-F3']); ADD-03/2.2-issue insufficient_evidence (dependencies: unknown ids ['S-F1', 'S-F2', 'S-F3', 'S-F6', 'S-I1'])
- **UNRESOLVED ADD-03:2.4** (clause, p1): not promotable: ADD-03/2.4 interpretation_pending (dropped: not ready: promotion waits while depends on ADD-03/2.1 (amendment_op, conflicting)); ADD-03/2.4-row interpretation_pending (dropped: not ready: promotion waits while depends on ADD-03/2.4, which is not ready); ADD-03/2.4-issue insufficient_evidence (dependencies: unknown ids ['S-F7', 'S-I2'])
- **UNRESOLVED ADD-03:2.5** (clause, p1): not promotable: ADD-03/2.5-row interpretation_pending (dropped: not ready: promotion waits while depends on ADD-03/2.1 (amendment_op, conflicting)); ADD-03/2.5-issue insufficient_evidence (dependencies: unknown ids ['S-F4', 'S-F5'])
- **UNRESOLVED ADD-03:p3-image/r1** (table_row, p3): no item proposed for it
- **UNRESOLVED ADD-03:p3-image/r2** (table_row, p3): no item proposed for it
- **UNRESOLVED ADD-03:p3-image/r3** (table_row, p3): no item proposed for it
- **UNRESOLVED ADD-03:p3-image/hdr-en** (reading_block, p3): no item proposed for it
- **UNRESOLVED ADD-03:p3-image/hdr-ar** (reading_block, p3): no item proposed for it
- **UNRESOLVED ADD-03:p3-image/date** (reading_block, p3): no item proposed for it
- **UNRESOLVED ADD-03:p3-image/ref** (reading_block, p3): no item proposed for it
- **UNRESOLVED ADD-03:p3-image/to** (reading_block, p3): no item proposed for it
- **UNRESOLVED ADD-03:p3-image/subject** (reading_block, p3): no item proposed for it
- **UNRESOLVED ADD-03:p3-image/tender** (reading_block, p3): no item proposed for it
- **UNRESOLVED ADD-03:p3-image/notes-heading** (reading_block, p3): no item proposed for it
- **UNRESOLVED ADD-03:p3-image/note1** (reading_block, p3): no item proposed for it
- **UNRESOLVED ADD-03:p3-image/note2** (reading_block, p3): no item proposed for it
- **UNRESOLVED ADD-03:p3-image/note3** (reading_block, p3): no item proposed for it
- **UNRESOLVED ADD-03:p3-image/stamp** (reading_block, p3): no item proposed for it
- **UNRESOLVED ADD-03:p3-image/signatory** (reading_block, p3): no item proposed for it
- **UNRESOLVED ADD-03:p3-image/image-footer** (reading_block, p3): no item proposed for it

## Earlier answers to re-read against the new text (never revoked; a person decides)

- `ADD-03:Q19` (ADD-03): cites VOL-V:39.4, changed by ADD-03/4.1; to be re-read against the new text of VOL-V:39.4 (ADD-03/4.1); a person decides whether the answer still holds

## Derived effects (session 12: pending readings, computed deadlines, conditions, consequences)

## Computed deadlines and the Working Days left (PROPOSED; nothing typed)

- Working Days left from the issue date (2026-11-18) to the PDD (2026-11-26): 6 (the issue date not counted, the PDD counted; Working Days per VOL-I 2.4 (weekend [4, 5] as date.weekday numbers; holidays none declared))
- `ADD-03:2.5` p1: “three (3) Working Days before the Proposal Due Date” -> **2026-11-23** (computed: calc deadline, anchor PDD = 2026-11-26, rule working-days-before, fingerprint 60b780e98a3a; PROPOSED, not validated)

## Proposed from a pending reading (not in force; not planned)

- `ADD-03-AppA-01` conditional on reading ADD-03-p3-r1 until approval: Table 8-1 row 1 (Arabic, as printed): a member that is a company incorporated in a GCC state applies to the Office with its certified commercial registration. …
- `ADD-03-AppA-03` conditional on reading ADD-03-p3-r1 until approval: Table 8-1 row 3 (Arabic, as printed): a member that is a branch registered in the Kingdom of a foreign company applies to the Office with the branch registrati…
- `ADD-03-AppA-04` conditional on reading ADD-03-p3-r1 until approval: Table 8-1 note 3 (Arabic, as printed): applications are made electronically through the Office's portal only. An application is complete only when all the docu…
- `ADD-03-AppA-05` conditional on reading ADD-03-p3-r1 until approval: Table 8-1 note 2 (Arabic, as printed): a Certificate of Investment Registration is valid for ninety days from its date of issue.
- activity `investment-registration-application` conditional on reading ADD-03-p3-r1 until approval (rows ADD-03-AppA-01, ADD-03-AppA-03, ADD-03-AppA-04, ADD-03-AppA-05)

## Conditional impact investigations (CONDITIONAL; never accepted facts)

- `impact:ADD-03:2.1` conditional on disposition ADD-03:2.1 (unresolved: not promotable: ADD-03/2.1 conflicting (consistency: VOL-I:8.9: ADD-03/2.1, ADD-03/2.4 change the same unit in different ways across the set); ADD-03/2.1-row interpretation_pending (dropped: not read…): investigate the rows, activities and prices that rest on VOL-I:8.9
- `impact:ADD-03:2.2` conditional on disposition ADD-03:2.2 (unresolved: not promotable: ADD-03/2.2 insufficient_evidence (dependencies: unknown ids ['S-F3']); ADD-03/2.2-issue insufficient_evidence (dependencies: unknown ids ['S-F1', 'S-F2', 'S-F3', 'S-F6', 'S-I1']) [AI …): investigate the rows, activities and prices that rest on the provision ADD-03:2.2
- `impact:ADD-03:2.4` conditional on disposition ADD-03:2.4 (unresolved: not promotable: ADD-03/2.4 interpretation_pending (dropped: not ready: promotion waits while depends on ADD-03/2.1 (amendment_op, conflicting)); ADD-03/2.4-row interpretation_pending (dropped: not re…): investigate the rows, activities and prices that rest on VOL-I:8.9
- `impact:ADD-03:2.5` conditional on disposition ADD-03:2.5 (unresolved: not promotable: ADD-03/2.5-row interpretation_pending (dropped: not ready: promotion waits while depends on ADD-03/2.1 (amendment_op, conflicting)); ADD-03/2.5-issue insufficient_evidence (dependenci…): investigate the rows, activities and prices that rest on VOL-I:8.9
- `impact:ADD-03:3.3` conditional on disposition ADD-03:3.3 (unresolved: escalated: software limitation: ADD-03:3.3 prints a relative change "the period of thirty-six (36) months is increased by six (6) months" of VOL-V:12.1, whose effective text at ADD-02 reads "The Proj…): investigate the rows, activities and prices that rest on VOL-V:12.1
- `impact:ADD-03:Q16` conditional on disposition ADD-03:Q16 (unresolved: escalated: software limitation: Q16 prints a relative change 'the issue period in row 2 of Table 8-1 is reduced by two (2) Working Days' that applies only 'for an application lodged not later than Su…): investigate the rows, activities and prices that rest on the provision ADD-03:Q16
- `impact:ADD-03:p3-image/r1` conditional on disposition ADD-03:p3-image/r1 (unresolved: no item proposed for it [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route host, model claude-code headless (claude-opus-5-5)); PROPOSED; not reviewed]: a person writes the op or a disposi…): investigate the rows, activities and prices that rest on the provision ADD-03:p3-image/r1
- `impact:ADD-03:p3-image/r2` conditional on disposition ADD-03:p3-image/r2 (unresolved: no item proposed for it [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route host, model claude-code headless (claude-opus-5-5)); PROPOSED; not reviewed]: a person writes the op or a disposi…): investigate the rows, activities and prices that rest on the provision ADD-03:p3-image/r2
- `impact:ADD-03:p3-image/r3` conditional on disposition ADD-03:p3-image/r3 (unresolved: no item proposed for it [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route host, model claude-code headless (claude-opus-5-5)); PROPOSED; not reviewed]: a person writes the op or a disposi…): investigate the rows, activities and prices that rest on the provision ADD-03:p3-image/r3
- `impact:ADD-03:p3-image/hdr-en` conditional on disposition ADD-03:p3-image/hdr-en (unresolved: no item proposed for it [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route host, model claude-code headless (claude-opus-5-5)); PROPOSED; not reviewed]: a person writes the op or a disposi…): investigate the rows, activities and prices that rest on the provision ADD-03:p3-image/hdr-en
- `impact:ADD-03:p3-image/hdr-ar` conditional on disposition ADD-03:p3-image/hdr-ar (unresolved: no item proposed for it [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route host, model claude-code headless (claude-opus-5-5)); PROPOSED; not reviewed]: a person writes the op or a disposi…): investigate the rows, activities and prices that rest on the provision ADD-03:p3-image/hdr-ar
- `impact:ADD-03:p3-image/date` conditional on disposition ADD-03:p3-image/date (unresolved: no item proposed for it [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route host, model claude-code headless (claude-opus-5-5)); PROPOSED; not reviewed]: a person writes the op or a disposi…): investigate the rows, activities and prices that rest on the provision ADD-03:p3-image/date
- `impact:ADD-03:p3-image/ref` conditional on disposition ADD-03:p3-image/ref (unresolved: no item proposed for it [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route host, model claude-code headless (claude-opus-5-5)); PROPOSED; not reviewed]: a person writes the op or a disposi…): investigate the rows, activities and prices that rest on the provision ADD-03:p3-image/ref
- `impact:ADD-03:p3-image/to` conditional on disposition ADD-03:p3-image/to (unresolved: no item proposed for it [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route host, model claude-code headless (claude-opus-5-5)); PROPOSED; not reviewed]: a person writes the op or a disposi…): investigate the rows, activities and prices that rest on the provision ADD-03:p3-image/to
- `impact:ADD-03:p3-image/subject` conditional on disposition ADD-03:p3-image/subject (unresolved: no item proposed for it [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route host, model claude-code headless (claude-opus-5-5)); PROPOSED; not reviewed]: a person writes the op or a disposi…): investigate the rows, activities and prices that rest on the provision ADD-03:p3-image/subject
- `impact:ADD-03:p3-image/tender` conditional on disposition ADD-03:p3-image/tender (unresolved: no item proposed for it [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route host, model claude-code headless (claude-opus-5-5)); PROPOSED; not reviewed]: a person writes the op or a disposi…): investigate the rows, activities and prices that rest on the provision ADD-03:p3-image/tender
- `impact:ADD-03:p3-image/notes-heading` conditional on disposition ADD-03:p3-image/notes-heading (unresolved: no item proposed for it [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route host, model claude-code headless (claude-opus-5-5)); PROPOSED; not reviewed]: a person writes the op or a disposi…): investigate the rows, activities and prices that rest on the provision ADD-03:p3-image/notes-heading
- `impact:ADD-03:p3-image/note1` conditional on disposition ADD-03:p3-image/note1 (unresolved: no item proposed for it [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route host, model claude-code headless (claude-opus-5-5)); PROPOSED; not reviewed]: a person writes the op or a disposi…): investigate the rows, activities and prices that rest on the provision ADD-03:p3-image/note1
- `impact:ADD-03:p3-image/note2` conditional on disposition ADD-03:p3-image/note2 (unresolved: no item proposed for it [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route host, model claude-code headless (claude-opus-5-5)); PROPOSED; not reviewed]: a person writes the op or a disposi…): investigate the rows, activities and prices that rest on the provision ADD-03:p3-image/note2
- `impact:ADD-03:p3-image/note3` conditional on disposition ADD-03:p3-image/note3 (unresolved: no item proposed for it [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route host, model claude-code headless (claude-opus-5-5)); PROPOSED; not reviewed]: a person writes the op or a disposi…): investigate the rows, activities and prices that rest on the provision ADD-03:p3-image/note3
- `impact:ADD-03:p3-image/stamp` conditional on disposition ADD-03:p3-image/stamp (unresolved: no item proposed for it [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route host, model claude-code headless (claude-opus-5-5)); PROPOSED; not reviewed]: a person writes the op or a disposi…): investigate the rows, activities and prices that rest on the provision ADD-03:p3-image/stamp
- `impact:ADD-03:p3-image/signatory` conditional on disposition ADD-03:p3-image/signatory (unresolved: no item proposed for it [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route host, model claude-code headless (claude-opus-5-5)); PROPOSED; not reviewed]: a person writes the op or a disposi…): investigate the rows, activities and prices that rest on the provision ADD-03:p3-image/signatory
- `impact:ADD-03:p3-image/image-footer` conditional on disposition ADD-03:p3-image/image-footer (unresolved: no item proposed for it [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route host, model claude-code headless (claude-opus-5-5)); PROPOSED; not reviewed]: a person writes the op or a disposi…): investigate the rows, activities and prices that rest on the provision ADD-03:p3-image/image-footer
- `impact:?` conditional on reading ? (pending_reading: the reading ? of ADD-03 is pending a person's approval: its values are not in force): investigate the rows, activities and prices that rest on ADD-03:region:ADD-03-p3-r1
- `impact:ADD-03-p3-r1` conditional on reading ADD-03-p3-r1 (pending_reading: the reading ADD-03-p3-r1 of ADD-03 is pending a person's approval: its values are not in force): investigate the rows, activities and prices that rest on ADD-03:p3-image, ADD-03:p3-image/r1, ADD-03:p3-image/r2, ADD-03:p3-image/r3, ADD-03:p3-image/hdr-en, ADD-03:p3-image/hdr-ar, ADD-03:p3-image/date, ADD-03:p3-image/ref, ADD-03:p3-image/to, ADD-03:p3-image/subject, ADD-03:p3-image/tender, ADD-03:p3-image/notes-heading (+6)

## Computed amounts (PROPOSED; computed by the engine from the previous effective value, never typed)

- `ADD-03/4.1` (ADD-03:4.1, 'reduced by forty per cent (40%)') on `VOL-V:39.4`: SAR 20,000,000 -> **SAR 12,000,000** — SAR 20,000,000 x (1 - 40%) = SAR 12,000,000 (the change 'reduced by forty per cent (40%)', ADD-03:4.1; the previous value 'SAR 20,000,000' in VOL-V:39.4 as issued)

## Per provision: source evidence → proposed transition → validation → downstream impact → output difference

### ADD-03:cover/para1 (paragraph, p1) — no effect (PROPOSED; not approved)
- source: “Issued 18 November 2026”
- transition: `ADD-03/disp/cover/para1` disposition no_effect: The issue-date line 'Issued 18 November 2026' states the Addendum's date of issue (the stage date). It amends, obliges and excepts nothing.
  - validation: **evidence_verified**

### ADD-03:cover/para2 (paragraph, p1) — no effect (PROPOSED; not approved)
- source: “Tender NUPA/ISTP/2026/014”
- transition: `ADD-03/disp/cover/para2` disposition no_effect: Title line 'Tender NUPA/ISTP/2026/014' under the heading 'ADDENDUM NO. 3'. It identifies the tender and amends, obliges and excepts nothing.
  - validation: **evidence_verified**

### ADD-03:cover/para3 (paragraph, p1) — applied (PROPOSED; not approved)
- source: “SYNTHETIC: not tender content. Test material for blind rehearsal 08; not issued by any authority. This Addendum replaces Volume I Clause 8.9 so that a member of a Bidder incorporated outside the Kingdom must submit either its investment licence or a Certificate of Investment Registration issued within the periods in Table 8-1 (issued in Arabic), subject to …”
- transition: `ADD-03/cover/para3` amendment_op annotate ADD-03:cover/para3 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The quoted obligation 'Bidders shall acknowledge receipt in Form 4-A.' is verbatim in ADD-03:cover/para3, and recording it as an interpretation pending a person is consistent with 'the cover summarises; it does not amend'. Annotating the cover's own procedural sentence is still a reading of a cover…
    - concern: S-I2 relies on how 'the same words in the cover texts of Addenda Nos. 1 and 2' were treated, but it carries no evidence and those units are not printed here. I cannot verify the precedent.
    - concern: The rationale says the cover's summaries (8.9, Table 8-1, Vol II 4.6, Vol V 12.1 and 39.4, and 'failing which the Proposal will be rejected') are covered by operative provisions in other batches. None of those provisions is printed here. Each cover summary still has to be compared with its operativ…
    - concern: The dependency VOL-IV:F4-A is not printed, so I cannot check that it is the right unit for Form 4-A as it stands at ADD-02.
- transition: `ADD-03/row/ack-4A` row_new {"row": {"id": "ADD03-ACK-4A", "group": "submission_forms", "scope": ["Envelope A", "Form 4-A"], "requirement": "Bidders shall acknowledge receipt of Addendum No. 3 in Form 4-A.", "units": ["ADD-03:c…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The row's requirement text 'Bidders shall acknowledge receipt of Addendum No. 3 in Form 4-A.' is not verbatim. The words 'of Addendum No. 3' are not in the cover. A1 needs the obligation quoted verbatim ('Bidders shall acknowledge receipt in Form 4-A.'), with any gloss kept separate and labelled.
    - concern: The scope 'Envelope A' is not supported by any evidence shown. No quoted unit puts Form 4-A in Envelope A, so this may be an unsupported placement.
    - concern: The rationale cites ADD-01:AppA/para1 and VOL-I:9.3, but neither is printed or attached as evidence. The row's own evidence list is empty.
    - concern: The proposer decided that VOL-I:9.3's non-responsiveness ('signing or execution of Form 4-A') does not apply to a failure to acknowledge Addendum No. 3 in Form 4-A. Whether that printed consequence reaches the acknowledgement at paragraph 1 of the reissued Form 4-A is a reading for a person (Legal …
    - concern: Same as the annotate item: it depends on S-I2's unevidenced precedent from Addenda 1 and 2.
  - downstream proposal `DS-05` row_new (c46:ADD-03/cover/para3): **interpretation_pending**
  - downstream proposal `DS-06` issue (c46:ADD-03/cover/para3): **interpretation_pending — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
      - concern: insufficient evidence: the full text of ADD-03:2.5 is not printed under units. Only one span is shown, and the controller check confirms only that this span is verbatim. The evidence shown does not prove the key claim that 'Operative Section 2.5 prints the notification obligation with no consequenc…
      - concern: The issue says 'The clarification window has closed (VOL-I 5.2)', but VOL-I:5.2 is not quoted and cannot be checked here.
      - concern: The framing itself (cover vs operative difference, both quoted, the cover not treated as amending, a human decision pending, owner Legal) is consistent with policy. If the full 2.5 is confirmed to state no consequence, the item would follow from it.
  - output difference: NEW ADD-03-cover-01; A5 REWORK form-4a; A5 REWORK form-4a-prep

### ADD-03:1.1 (clause, p1) — no effect (PROPOSED; not approved)
- source: “This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.”
- transition: `ADD-03/disp/1.1` disposition no_effect: Recital: 'This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.' It restates…
  - validation: **interpretation_pending — applied rule: ADD-03 1.1 provides: 'This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.' (applied, not decided); a person confirms the application**

### ADD-03:1.2 (clause, p1) — no effect (PROPOSED; not approved)
- source: “A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.”
- transition: `ADD-03/disp/1.2` disposition no_effect: Interpretation rule for the Addendum's own references: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by …
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The provision contains an exception, 'unless otherwise stated'. The controller's semantic check reports that no exception words remain, which looks wrong for these words. Under the shared rules, a no_effect on a provision with exception wording is a person's decision. The item does leave it for a p…
    - concern: Calling this 'no_effect' understates it. Clause 1.2 decides which version every reference in ADD-03 points to (for example Form 4-A as reissued by ADD-01, and Table 8-1). A person may prefer to record it as a reading rule that the other batches depend on, rather than as having no effect.
    - concern: S-I1 has no evidence attached apart from the provision itself. That is acceptable for a reading of this one clause.

### ADD-03:1.3 (clause, p1) — no effect (PROPOSED; not approved)
- source: “Clarification requests 15 to 19 were received before the time stated in Volume I Clause 5.2.”
- transition: `ADD-03/issue/cq20` issue {"text": "ambiguous: the cover and the operative text differ on which clarification requests are answered. The cover says 'and responds to clarification requests 15 to 20'. Clause 1.3 says 'Clarifica…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The difference is real: the cover says 'and responds to clarification requests 15 to 20', while ADD-03:1.3 and the Section 5 heading say 15 to 19. Raising it as an issue with both quotations, leaving it unresolved, follows the rule on cover/operative differences.
    - concern: Clause 1.3 only says requests 15 to 19 'were received before the time stated in Volume I Clause 5.2'. It does not itself say they are answered; the 'responses' wording comes from the Section 5 heading. The issue text should not imply that 1.3 states the answered set.
    - concern: Reading 3 (a response intended but omitted) is really a missing-evidence possibility, not an ambiguity in the words. A person may want that point raised separately with Document control as possible missing content, so the two classes are not merged under 'ambiguous:'.
    - concern: The 'no response to request 20 found' claim rests on a search that is not printed. The ADD-03:H:S5 and VOL-I:5.2 quotations are confirmed only by the controller's verbatim checks, because those units are not in the units shown.
    - concern: The controller's human-owned flag on 'answered' comes from quoted text and readings ('will not be answered', 'not answered'). The issue does not declare any question answered.
- transition: `ADD-03/disp/1.3` disposition no_effect: Recital of fact: 'Clarification requests 15 to 19 were received before the time stated in Volume I Clause 5.2.' It amends, obliges and excepts nothing, and lea…
  - validation: **evidence_verified**
  - downstream proposal `D-22` no_change (impact:1. RECITALS): **interpretation_pending**

### ADD-03:2.1 (clause, p1) — UNRESOLVED (accounted for, not applied)
- source: “Volume I Clause 8.9 is deleted and replaced by the following: ‘8.9 Each member of the Bidder that is incorporated outside the Kingdom shall submit with Envelope A either (a) a copy of its current investment licence or (b) a Certificate of Investment Registration issued by the Northern Region Investment Services Office (the Office) in accordance with Table 8…”
- transition: `ADD-03/2.1` amendment_op replace_text VOL-I:8.9 “The Bidder shall submit either evidence of a current investment licence for eac…” → “Each member of the Bidder that is incorporated outside the Kingdom shall submit…”
  - validation: **conflicting** — consistency: VOL-I:8.9: ADD-03/2.1, ADD-03/2.4 change the same unit in different ways across the set
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: old words located in the target; model claude-opus-5-5
    - concern: Q15 ('an undertaking is no longer accepted') is used to support the removal of the undertaking option, but Q15's text is not printed in this request, so I could not check it. The substitution does not need it: the words 'is deleted and replaced by the following' are enough.
    - concern: The controller's 'conflicting' flag treats ADD-03/2.4 as changing VOL-I:8.9 'in different ways'. As printed, 2.4 does not rewrite the text of 8.9. It disapplies Section 2.1 for one class of member. That makes it an exception to scope, not a competing text change. A person should decide whether the …
    - concern: The rationale says the undertaking is 'now kept only for the Section 2.4 class'. That depends on interpretation S-I2, which is pending. It should be labelled as an interpretation, not stated as the effect of the op.
    - concern: I checked the replace_text old and new values against the quotations, and they are correct. Leaving out the printed number '8.9' in the new text is disclosed.
- transition: `ADD-03/2.1-row` row_reading {"row": "VOL-I-8.9-01", "interpretation": {"stage": "ADD-03", "quote": "Each member of the Bidder that is incorporated outside the Kingdom shall submit with Envelope A either (a) a copy of its curren…
  - validation: **interpretation_pending** — readiness: not ready (promotion waits): depends on ADD-03/2.1 (amendment_op, conflicting)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The rejection consequence is quoted correctly from the new 8.9. It applies to 'each such member', meaning a member incorporated outside the Kingdom. Whether it also covers the 2.4 class's undertaking is still open (see ADD-03/2.4-row). The note should not suggest that the class split is settled.
    - concern: The row's current requirement text was not read. The proposer says so. The row stays incomplete until a person revises it, including any date rule tied to Financial Close.
  - downstream proposal `DS-17` no_change (act:investment-licence): **interpretation_pending**
  - downstream proposal `DS-18` issue (esc:ADD-03:2.1): **interpretation_pending — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
      - concern: The item says ADD-03/2.1 'conflicts' with ADD-03/2.4, but on the words shown 2.4 is an express carve-out from 2.1: 'Section 2.1 does not apply to a member ...'. This is not a contradiction. The real difficulties are different: (i) 2.4 refers to 'Volume I Clause 8.9 as issued', which 2.1 deletes; (i…
      - concern: The item says the effective VOL-I 8.9 'states no consequence'. Only one span of VOL-I:8.9 is shown, so this cannot be checked from the evidence printed.
      - concern: The item cites 'The clarification window has closed (VOL-I 5.2)', but VOL-I:5.2 is not quoted here.
      - concern: Holding 2.1 unapplied leaves a printed deletion-and-replacement, with a stated rejection, out of the effective text. This needs a prominent A2/A3 flag. The item's a3 line does this, and its list of dependent rows, activity and Table 8-1 lead times is appropriate.
      - concern: The quotations of 2.1, 2.4 and Q15 are accurate against the text shown.
  - downstream proposal `DS-19` escalation (esc:ADD-03:2.1): **escalated**
  - downstream proposal `D-10` dependency (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending**
  - downstream proposal `D-11` dependency (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending**
  - downstream proposal `D-12` issue (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-13` issue (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-14` escalation (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **escalated**
  - downstream proposal `D-ISS-02` issue (reading:ADD-03-p3-r1): **interpretation_pending — HUMAN DECISION PENDING**

### ADD-03:2.2 (clause, p1) — UNRESOLVED (unaccounted)
- source: “Table 8-1 is reproduced at Appendix A to this Addendum as issued by the Office and forms part of Volume I. Table 8-1 is issued in the Arabic language. The Arabic text governs. The English translation at Appendix B is provided for convenience only.”
- transition: `ADD-03/2.2` amendment_op insert_table ADD-03:p3-image
  - validation: **insufficient_evidence — applied rule: ADD-03 2.2 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application** — dependencies: unknown ids ['S-F3']
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Treating ADD-03:p3-image as Table 8-1 follows from 'reproduced at Appendix A ... and forms part of Volume I'. However, the image reading is pending. The detail described from the crop (three rows ٣/٥/٨, three notes, the Office letter ref and date, an empty stamp circle) is not in the units shown, a…
    - concern: The precedence 'over' ADD-03:T8-1 assumes T8-1 is the Appendix B translation. T8-1 is not printed in the units, so I could not confirm this. Applying 'The Arabic text governs.' still needs a person to confirm it.
    - concern: The stamp circle is described as empty, but nothing is raised about it. A person may want to note whether the table is authenticated as 'issued by the Office'. I make no finding on this.
- transition: `ADD-03/2.2-issue` issue {"text": "Table 8-1 row 2 (company incorporated outside the GCC states): the Arabic table at Appendix A prints 'مدة الإصدار (أيام عمل): ٥' (5 Working Days), while the English translation at Appendix …
  - validation: **insufficient_evidence — HUMAN DECISION PENDING** — dependencies: unknown ids ['S-F1', 'S-F2', 'S-F3', 'S-F6', 'S-I1']
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Row 2 showing ٥ is confirmed by ADD-03:p3-image/r2 cell 'مدة الإصدار (أيام عمل)': '٥'. The English figure 3 is verified only by the controller record. T8-1/2 is not printed in the units.
    - concern: The Q16 quotation in S-F6 (reduction of two Working Days for applications lodged by 22 November 2026) is not among the units printed, and the controller records no check of it. I could not verify it.
    - concern: The issue rightly leaves open which figure applies, even though 2.2 states that the Arabic governs. Applying a printed precedence rule is still a person's call, and the Arabic reading itself is pending.
    - concern: The claim that rows 1 and 3 agree with the translation cannot be checked here.
  - downstream proposal `D-01` escalation (esc:ADD-03:2.2): **escalated**
  - downstream proposal `D-02` dependency (esc:ADD-03:2.2): **interpretation_pending**
  - downstream proposal `D-10` dependency (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending**
  - downstream proposal `D-11` dependency (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending**
  - downstream proposal `D-12` issue (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-13` issue (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-14` escalation (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **escalated**
  - downstream proposal `D-ROW-01` row_new (reading:ADD-03-p3-r1): **interpretation_pending**
  - downstream proposal `D-ROW-02` row_new (reading:ADD-03-p3-r1): **conflicting**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The 'requirement' field is the proposer's own English rendering of the Arabic row, not a verbatim quotation. A1 needs the obligation quoted verbatim, and a translation is never evidence for the source. It also adds wording that is not in the quoted cells: the Arabic gives a member class and 'المستن…
      - concern: The row cites ADD-03:p3-image/note1 and ADD-03:p3-image/note3, and the date_note says the period is 'counted under note 1 from an event'. Neither note's text is in the evidence or the statements, so this cannot be checked against the request.
      - concern: consequence 'none_stated' rests on downstream-003/S-REJECT-2-1, which is an interpretation. ADD-03:2.1 prints 'A Proposal that does not include the evidence required by this Clause for each such member shall be rejected.' Linking that rejection to issue I-INVREG-CONSEQUENCE is right. However, the r…
      - concern: The rationale says the crop 'plainly shows ٥' and that the reading does not mark the numeral as uncertain, yet confidence is 'low'. The reason given (the conflict with Appendix B and Q16) is fair. Recording the figure from the image while holding the row as PENDING READING is consistent with the ru…
  - downstream proposal `D-ROW-03` row_new (reading:ADD-03-p3-r1): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-ROW-04` row_new (reading:ADD-03-p3-r1): **interpretation_pending**
  - downstream proposal `D-ROW-05` row_new (reading:ADD-03-p3-r1): **interpretation_pending**
  - downstream proposal `D-EV-01` evidence_item (reading:ADD-03-p3-r1): **interpretation_pending**
  - downstream proposal `D-ACT-01` activity (reading:ADD-03-p3-r1): **interpretation_pending**
  - downstream proposal `D-ISS-01` issue (reading:ADD-03-p3-r1): **conflicting — applied rule: ADD-03 2.2 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-opus-5-5
      - concern: The controller reports a phase-consistency failure: this item reverses ADD-03/2.2-issue, which applied 'The Arabic text governs.' Handing the point to a person is allowed, because which clause governs and what it settles is a person's decision. Even so, the issue should name ADD-03/2.2-issue explic…
      - concern: Reading (b), that Appendix B already shows the reduced period, implies arithmetic between ٥ and 3. That arithmetic must not be relied on without `calculate`. The issue correctly states no computed figure.
      - concern: The Q16 quotation here includes the lodging-date condition, but the quotation in S-Q16 does not. Both are reported as verbatim. The full Q16 unit text is not printed in the request, so the complete wording could not be checked here.
  - downstream proposal `D-ISS-03` issue (reading:ADD-03-p3-r1): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-CQ-01` clarification_item (reading:ADD-03-p3-r1): **conflicting — applied rule: ADD-03 2.2 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: practical_impact refers to 'the latest date to lodge a row-2 member's application, before Envelope A'. Nothing in the evidence shown links Table 8-1 or the Office application to Envelope A or to any submission deadline. Without a quotation this link may be invented.
      - concern: The Q16 entry in 'sources' leaves out the lodging-date condition ('for an application lodged not later than Sunday 22 November 2026'), but the proposed question depends on that condition. That clause should be quoted in sources.
      - concern: The question is neutral, already_settled correctly leaves to a person whether 'The Arabic text governs' settles the point, interim_handling chooses neither figure, and the status is 'draft, not sent'. All of these are sound.
      - concern: Same phase-consistency flag as D-ISS-01: the item should name ADD-03/2.2-issue so a person can reconcile the two.

### ADD-03:2.3 (clause, p1) — applied (PROPOSED; not approved)
- source: “Applications for a Certificate of Investment Registration shall be made by the member to the Office. The Office has undertaken to the Authority to issue a Certificate within the issue period stated in Table 8-1 for the class of the member, counted in accordance with the Notes to Table 8-1.”
- transition: `ADD-03/2.3-row` row_new {"row": {"id": "ADD-03-2.3-01", "group": "VOL-I-8", "scope": ["Bidder", "member incorporated outside the Kingdom relying on a Certificate of Investment Registration"], "requirement": "Applications fo…
  - validation: **interpretation_pending** — readiness: not ready (promotion waits): depends on ADD-03/2.1 (amendment_op, conflicting); depends on ADD-03/2.2 (amendment_op, insufficient_evidence)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The date note says the period is 'counted from receipt of a complete application (Table 8-1 Note 1)'. That paraphrases a note that is not printed here, and it differs from the 2.2 rationale ('counting starts the Working Day after receipt of a complete application'). The note should be quoted verbat…
    - concern: The row's dependencies leave out ADD-03/2.2-issue, even though the note relies on the row 2 discrepancy.
    - concern: Recording 'none_stated' for the consequence is right: 2.3 prints none. Treating the Office's undertaking as a lead time rather than a bidder deadline is a fair reading of the words.
  - downstream proposal `DS-10` row_new (ana:ADD-03/2.3-row): **interpretation_pending**
  - downstream proposal `D-10` dependency (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending**
  - downstream proposal `D-11` dependency (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending**
  - downstream proposal `D-12` issue (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-13` issue (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-14` escalation (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **escalated**
  - downstream proposal `D-ESC-01` escalation (reading:ADD-03-p3-r1): **escalated**
  - output difference: NEW ADD-03-2.3-01

### ADD-03:2.4 (clause, p1) — UNRESOLVED (accounted for, not applied)
- source: “Section 2.1 does not apply to a member of the Bidder that is to hold not more than ten per cent (10%) of the shares in the Project Company and that has no role in the design, construction or operation of the Facility. Such a member shall instead submit with Envelope A the signed undertaking described in Volume I Clause 8.9 as issued.”
- transition: `ADD-03/2.4` amendment_op annotate VOL-I:8.9 effect disapplies
  - validation: **interpretation_pending** — readiness: not ready (promotion waits): depends on ADD-03/2.1 (amendment_op, conflicting)
- transition: `ADD-03/2.4-row` row_new {"row": {"id": "ADD-03-2.4-01", "group": "VOL-I-8", "scope": ["member of the Bidder holding not more than ten per cent (10%) of the shares in the Project Company with no role in design, construction …
  - validation: **interpretation_pending** — readiness: not ready (promotion waits): depends on ADD-03/2.4, which is not ready
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The rationale says the undertaking's content is quoted from VOL-I:8.9 'as issued' (text_as_issued). The only text printed, and the only one the controller checked, is VOL-I:8.9's effective text at ADD-02 ('verbatim in VOL-I:8.9 at ADD-02'). Section 2.4 refers to Clause 8.9 'as issued'. Nothing show…
    - concern: 'assessment': 'pass_fail' is given even though the row records consequence 'none_stated' and leaves open whether the rejection words of the new 8.9 reach this class. 'pass_fail' suggests an assessed outcome that the evidence does not establish.
    - concern: ADD-03/2.4 (the op) and ADD-03/2.4-issue are referred to but not printed in this batch, so I could not check them.
    - concern: The scope paraphrases 'is to hold' as 'holding'. The reading of 'Section 2.1 does not apply' (S-I2) is rightly left pending.
- transition: `ADD-03/2.4-issue` issue {"text": "ambiguous: Section 2.4 says 'Section 2.1 does not apply to a member of the Bidder that is to hold not more than ten per cent (10%) of the shares in the Project Company and that has no role …
  - validation: **insufficient_evidence — HUMAN DECISION PENDING** — dependencies: unknown ids ['S-F7', 'S-I2']
  - downstream proposal `DS-11` row_new (ana:ADD-03/2.4-row): **interpretation_pending**
  - downstream proposal `D-03` escalation (esc:ADD-03:2.4): **escalated**
  - downstream proposal `D-04` issue (esc:ADD-03:2.4): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-10` dependency (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending**
  - downstream proposal `D-11` dependency (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending**
  - downstream proposal `D-12` issue (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-13` issue (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-14` escalation (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **escalated**
  - output difference: NEW ADD-03-2.4-01; A5 REWORK investment-licence

### ADD-03:2.5 (clause, p1) — UNRESOLVED (accounted for, not applied)
- source: “A Bidder that relies on paragraph (b) of Volume I Clause 8.9 for any member shall notify the Authority through the Portal, not later than three (3) Working Days before the Proposal Due Date, of the name of that member and the reference number of its application to the Office.”
- transition: `ADD-03/2.5-row` row_new {"row": {"id": "ADD-03-2.5-01", "group": "VOL-I-8", "scope": ["Bidder relying on paragraph (b) of Volume I Clause 8.9 for any member"], "requirement": "A Bidder that relies on paragraph (b) of Volume…
  - validation: **interpretation_pending** — readiness: not ready (promotion waits): depends on ADD-03/2.1 (amendment_op, conflicting)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The rationale says Q16's 22 November lodging date 'falls one Working Day before' the 23 November deadline. That count was not produced by calculate, and the Q16 text is not printed here. The figure should come from calculate, or be removed.
    - concern: The PDD value (2026-11-26) and the calculate result appear only in the note. I cannot check them against the units shown.
    - concern: 'issues': [] is empty, even though the interpretation note points to ADD-03/2.5-issue. The row should link that issue. With the cover and the operative text in disagreement, confidence 'high' may overstate how settled the consequence is.
    - concern: Recording 'none_stated' for the consequence matches the operative words of 2.5.
- transition: `ADD-03/2.5-issue` issue {"text": "The cover and the operative provision differ. Cover (ADD-03:cover/para3): 'requires a Bidder relying on a Certificate to notify the Authority of its applications, failing which the Proposal…
  - validation: **insufficient_evidence — HUMAN DECISION PENDING** — dependencies: unknown ids ['S-F4', 'S-F5']
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The cover quotation ('failing which the Proposal will be rejected') is verified only by the controller record. ADD-03:cover/para3 is not printed in the units.
    - concern: The item handles the conflict correctly: it reports both quotations, does not resolve which governs, and names Legal as the owner.
  - downstream proposal `DS-12` row_new (ana:ADD-03/2.5-row): **interpretation_pending**
  - downstream proposal `DS-13` evidence_item (ana:ADD-03/2.5-row): **evidence_verified**
  - downstream proposal `DS-14` activity (ana:ADD-03/2.5-row): **interpretation_pending**
  - downstream proposal `D-05` issue (esc:ADD-03:2.5): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-06` escalation (esc:ADD-03:2.5): **escalated**
  - downstream proposal `D-10` dependency (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending**
  - downstream proposal `D-11` dependency (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending**
  - downstream proposal `D-12` issue (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-13` issue (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-14` escalation (impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS): **escalated**
  - output difference: NEW ADD-03-2.5-01; A5 NEW cir-portal-notification

### ADD-03:2.6 (clause, p1) — applied (PROPOSED; not approved)
- source: “The periods in Volume I Clause 12.2 for Commercial Close and Financial Close are unchanged.”
- transition: `ADD-03/2.6` amendment_op annotate VOL-I:12.2 effect confirms
  - validation: **evidence_verified**
  - downstream proposal `DS-01` row_reading (row:VOL-I-12.2-01): **interpretation_pending**
  - downstream proposal `DS-02` row_reading (row:VOL-I-12.2-02): **interpretation_pending**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
      - concern: The consequence is tied to 'the long-stop date', not to the 270-day period. The row's quote and date rule (270 days after the Preferred Bidder Notification) do not show that the two are the same date. The note correctly leaves I-VOL-I-BOND-LONGSTOP open. The row must not be read as linking the Bid …
      - concern: The class 'contractual' for 'entitles the Authority to call the Bid Bond and to proceed with the next ranked Bidder' is a reading. Whether this also counts as an A3 bid-out consequence (exclusion in favour of the next ranked Bidder) is a person's call. The item should not settle it by its choice of…
      - concern: The stage is given as ADD-03, but the obligation has been in force since BASE. ADD-03:2.6 only confirms that the periods are unchanged. The register should make clear that ADD-03 is not the stage where the obligation came into force.
  - output difference: CONFIRMED (unchanged) VOL-I-12.2-01

### ADD-03:3.1 (clause, p2) — applied (PROPOSED; not approved)
- source: “The following new Clause 4.6 is inserted in Volume II after Clause 4.5: ‘4.6 The treated effluent storage reservoir referred to in Clause 1.2 shall provide a working volume of not less than six (6) hours of the design flow and shall be divided into not fewer than two (2) compartments, each capable of being isolated for cleaning while the other remains in se…”
- transition: `ADD-03/3.1` amendment_op insert_unit VOL-II:4.5 “The treated effluent storage reservoir referred to in Clause 1.2 shall provide a working volume of not less than six (6…”
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-opus-5-5
    - concern: The anchor is correct. ADD-03:3.1 says 'inserted in Volume II after Clause 4.5', so VOL-II:4.5 is the right anchor and 'number' 4.6 matches the provision. new_text matches the quoted text word for word; only the printed number '4.6' at the start is left out, which is right because it is carried in …
    - concern: The item's evidence quotes only the instruction ('The following new Clause 4.6 is inserted in Volume II after Clause 4.5'). It does not quote the inserted clause text, which appears only in the payload. Adding a span for the inserted text would make A2 complete.
    - concern: The rationale says no Volume II Clause 4.6 exists at ADD-02. The search result behind that is not shown in this request, so I could not check it.
    - concern: The rationale also mentions ADD-03:Q18, 'Clause 2.1 / Table 2-6' and an A1 row 'ADD-03/row-4.6'. None of these is shown here, so I could not check them. It correctly leaves the 'six (6) hours of the design flow' volume uncomputed.
- transition: `ADD-03/row-4.6` row_new {"row": {"id": "R-VOLII-4.6", "group": "VOL-II", "scope": ["Technical Proposal", "process design"], "requirement": "The treated effluent storage reservoir referred to in Clause 1.2 shall provide a wo…
  - validation: **interpretation_pending**
  - downstream: units changed VOL-II:4.5+ADD-03; rows citing them none
  - downstream proposal `DS-07` row_new (c46:ADD-03/3.1): **interpretation_pending**
  - downstream proposal `DS-08` issue (c46:ADD-03/3.1): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-09` dependency (c46:ADD-03/3.1): **interpretation_pending**
  - output difference: NEW ADD-03-3.1-01

### ADD-03:3.2 (clause, p2) — no effect (PROPOSED; not approved)
- source: “The insertion of Clause 4.6 does not renumber any other Clause of Volume II.”
- transition: `ADD-03/3.2` disposition no_effect: The provision states "The insertion of Clause 4.6 does not renumber any other Clause of Volume II." It prints no old/new pair, deletion or obligation; it confi…
  - validation: **evidence_verified**

### ADD-03:3.3 (clause, p2) — UNRESOLVED (accounted for, not applied)
- source: “In Volume V Clause 12.1, the period of thirty-six (36) months is increased by six (6) months.”
- transition: `ADD-03/3.3` escalation why: software limitation: ADD-03:3.3 prints a relative change "the period of thirty-six (36) months is increased by six (6) months" of VOL-V:12.1, whose effective text at ADD-02 reads "The Project Company…
  - validation: **escalated**
  - downstream proposal `DS-16` issue (ana:ADD-03/row-3.4): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-07` escalation (esc:ADD-03:3.3): **escalated**
  - downstream proposal `D-15` dependency (impact:3. TREATED EFFLUENT STORAGE AND SCHEDULED PCOD): **interpretation_pending**
  - downstream proposal `D-16` escalation (impact:3. TREATED EFFLUENT STORAGE AND SCHEDULED PCOD): **escalated**
  - downstream proposal `D-17` dependency (impact:3. TREATED EFFLUENT STORAGE AND SCHEDULED PCOD): **interpretation_pending**

### ADD-03:3.4 (clause, p2) — applied (PROPOSED; not approved)
- source: “Bidders shall reflect Sections 3.1 and 3.3 in the process design and the construction programme submitted in the Technical Proposal and in the Financial Model.”
- transition: `ADD-03/row-3.4` row_new {"row": {"id": "R-ADD03-3.4", "group": "ADD-03", "scope": ["Technical Proposal", "Financial Model"], "requirement": "Bidders shall reflect Sections 3.1 and 3.3 in the process design and the construct…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The requirement and the interpretation quote are word for word from ADD-03:3.4. 'consequence: none_stated' is correct, because ADD-03:3.4 prints no consequence.
    - concern: dependencies lists only ADD-03:3.4. The provision explicitly cites 'Sections 3.1 and 3.3', so the dependencies should also include ADD-03:3.1, ADD-03:3.3 and the new Volume II Clause 4.6 created by ADD-03/3.1. Without them the propagation is incomplete.
    - concern: The text of ADD-03:3.3 is not printed in this request, so I could not check what this row requires for Section 3.3. The row rightly treats that part as pending the escalated ADD-03/3.3.
    - concern: discipline is 'Technical' only, but the provision also requires reflection 'in the Financial Model', which is commercial. The decision owner may need to include Commercial.
    - concern: assessment 'procedural' is a proposed class. The obligation affects what goes into the process design, not only how the bid is submitted. A person should confirm this class.
    - concern: The words 'in the process design and the construction programme submitted in the Technical Proposal and in the Financial Model' could mean both items go in both documents, or each item goes in its own document. The row quotes the words without choosing a reading, which is correct; this may be worth…
  - downstream proposal `DS-15` row_new (ana:ADD-03/row-3.4): **interpretation_pending**
  - downstream proposal `DS-16` issue (ana:ADD-03/row-3.4): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-15` dependency (impact:3. TREATED EFFLUENT STORAGE AND SCHEDULED PCOD): **interpretation_pending**
  - downstream proposal `D-16` escalation (impact:3. TREATED EFFLUENT STORAGE AND SCHEDULED PCOD): **escalated**
  - downstream proposal `D-17` dependency (impact:3. TREATED EFFLUENT STORAGE AND SCHEDULED PCOD): **interpretation_pending**
  - output difference: NEW ADD-03-3.4-01; A5 REWORK fin-model-build; A5 REWORK fin-model-freeze; A5 REWORK technical-proposal

### ADD-03:4.1 (clause, p2) — applied (PROPOSED; not approved)
- source: “The amount stated in Volume V Clause 39.4 is reduced by forty per cent (40%).”
- transition: `ADD-03/4.1` amendment_op adjust_value VOL-V:39.4 “SAR 20,000,000” → “”
  - validation: **evidence_verified**
- transition: `ADD-03/issue-4.1` issue {"text": "Cover and operative provision differ. ADD-03:4.1 prints \"The amount stated in Volume V Clause 39.4 is reduced by forty per cent (40%).\" applied to \"SAR 20,000,000\" in VOL-V:39.4 (engine…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - downstream: units changed VOL-V:39.4; rows citing them none
  - downstream proposal `D-24` no_change (impact:4. AUTHORITY EVENT OF DEFAULT): **interpretation_pending**

### ADD-03:4.2 (clause, p2) — applied (PROPOSED; not approved)
- source: “The period of sixty (60) days in Volume V Clause 39.4 is unchanged.”
- transition: `ADD-03/4.2` amendment_op annotate VOL-V:39.4 effect confirms
  - validation: **evidence_verified**

### ADD-03:Q15 (table_row, p2) — applied (PROPOSED; not approved)
- source: “No: 15 | Bidder question: May the undertaking required by Volume I Clause 8.9 be given by the lead member on behalf of a foreign consortium member? | Authority response: No. Volume I Clause 8.9 is replaced by Section 2.1 of this Addendum and an undertaking is no longer accepted, save from a member described in Section 2.4, which shall give its own undertaki…”
- transition: `ADD-03/Q15` amendment_op annotate VOL-I:8.9 effect interprets
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: Q15 does more than restate. 'which shall give its own undertaking' adds that the Section 2.4 member must give the undertaking itself. The 2.4 words shown ('Such a member shall instead submit with Envelope A the signed undertaking described in Volume I Clause 8.9 as issued') do not say who signs. Th…
    - concern: The annotation is placed on VOL-I:8.9. Section 2.1 of this same addendum deletes that clause ('Volume I Clause 8.9 is deleted and replaced by the following:'). The interpretation is really about who gives the 2.4 undertaking. An annotation on a deleted unit may not carry forward to the effective te…
    - concern: Q15's opening 'No.' answers the bidder's question about the lead member giving the undertaking on a foreign member's behalf. The note covers this, but it is paraphrase; the verbatim words are in the evidence and match the unit.
  - downstream proposal `DS-03` row_reading (row:VOL-I-8.9-01): **interpretation_pending — HUMAN DECISION PENDING**
  - output difference: A5 CONFIRMED (unchanged) investment-licence; A5 REVIEW (possible impact) investment-licence

### ADD-03:Q16 (table_row, p2) — UNRESOLVED (accounted for, not applied)
- source: “No: 16 | Bidder question: Will the Authority assist foreign consortium members that have not obtained an investment licence before the Proposal Due Date? | Authority response: Section 2 of this Addendum applies. The Office has confirmed to the Authority that, for an application lodged not later than Sunday 22 November 2026, the issue period in row 2 of Tabl…”
- transition: `ADD-03/Q16` escalation why: software limitation: Q16 prints a relative change 'the issue period in row 2 of Table 8-1 is reduced by two (2) Working Days' that applies only 'for an application lodged not later than Sunday 22 Nov…
  - validation: **escalated**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The 'software limitation:' reason assumes Q16 amends the row 2 value (Reading A of S-Q16-I1). Whether it amends anything at all is itself the open ambiguity (Reading B: it only reports 'The Office has confirmed to the Authority that...'). The escalation should say it applies only if a person adopts…
    - concern: The 'why' text bundles an ambiguity (Arabic ٥ vs English 3) into a software-limitation reason. It points to a separate issue, which is acceptable, but under the one-point, one-class rule it should stay out of this escalation's reason.
    - concern: Two parts of Q16 are not accounted for in this item's evidence: the response's first sentence ('Section 2 of this Addendum applies.') and the bidder question.
    - concern: The target relies on an image reading that is still pending (ADD-03:p3-image). The rationale's statement that rows ١ and ٣ show ٣ and ٨ cannot be checked from the evidence printed here. The row 2 reading ('م: ٢', issue-period cell '٥') matches the unit text shown.
    - concern: The rationale says calculate confirmed 2026-11-22 is a Sunday and a Working Day. The calculate output is not in the evidence shown, so this could not be checked.
- transition: `ADD-03/Q16-issue` issue {"text": "ambiguous: Q16 states 'the issue period in row 2 of Table 8-1 is reduced by two (2) Working Days' for 'an application lodged not later than Sunday 22 November 2026'. (1) Row 2 of the Arabic…
  - validation: **interpretation_pending — HUMAN DECISION PENDING** — readiness: not ready (promotion waits): depends on ADD-03/Q16 (escalation, escalated)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Point (1) is labelled 'ambiguous:', but the words do not support two readings. The Arabic ٥ and the English 3 are a discrepancy between the original and its translation. Section 2.2 prints a precedence rule for it ('The Arabic text governs. The English translation at Appendix B is provided for conv…
    - concern: Point (2), whether Q16 amends Table 8-1 or only reports the Office's confirmation, is a genuine ambiguity. It should be a separate issue rather than merged with point (1) under one open question.
    - concern: The issue's Q16 quotation leaves out 'The Office has confirmed to the Authority that,' and 'The other issue periods in Table 8-1 are unchanged.'. Those words are what support Reading B and limit the scope, so the person deciding should see them in the issue's own evidence.
    - concern: The owner is Document control only. The rationale itself says Legal is needed on which text governs, and deciding which clause prevails is a Legal matter, so Legal should be named as owner for the precedence point.
  - downstream proposal `D-08` escalation (esc:ADD-03:Q16): **escalated**
  - downstream proposal `D-09` issue (esc:ADD-03:Q16): **insufficient_evidence — HUMAN DECISION PENDING**
  - downstream proposal `D-18` dependency (impact:5. RESPONSES TO CLARIFICATION REQUESTS 15 TO 19): **interpretation_pending**
  - downstream proposal `D-19` dependency (impact:5. RESPONSES TO CLARIFICATION REQUESTS 15 TO 19): **interpretation_pending**

### ADD-03:Q17 (table_row, p2) — applied (PROPOSED; not approved)
- source: “No: 17 | Bidder question: Will the arbitration under Volume V Clause 44.2 be conducted in English? | Authority response: Yes. Volume V Clause 44.2 applies.”
- transition: `ADD-03/Q17` amendment_op annotate VOL-V:44.2 effect confirms
  - validation: **evidence_verified**
  - downstream proposal `DS-04` row_reading (row:VOL-V-44.2-01): **interpretation_pending**
  - output difference: CONFIRMED (unchanged) VOL-V-44.2-01; A5 CONFIRMED (unchanged) deviations-review; A5 CONFIRMED (unchanged) form-4e

### ADD-03:Q18 (table_row, p2) — no effect (PROPOSED; not approved)
- source: “No: 18 | Bidder question: Volume II Clause 1.2 includes a treated effluent storage reservoir, but no capacity is stated. What capacity is required? | Authority response: See new Volume II Clause 4.6, inserted by Section 3.1 of this Addendum.”
- transition: `ADD-03/Q18-disp` disposition no_effect: The response only cross-refers: 'See new Volume II Clause 4.6, inserted by Section 3.1 of this Addendum.' It prints no change, obligation or exception of its o…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'but' (cites VOL-II:1.2))

### ADD-03:Q19 (table_row, p2) — no effect (PROPOSED; not approved)
- source: “No: 19 | Bidder question: Will the Authority reconsider the threshold for an Authority Event of Default in Volume V Clause 39.4? | Authority response: Yes. See Section 4 of this Addendum.”
- transition: `ADD-03/Q19-disp` disposition no_effect: The response only cross-refers: 'Yes. See Section 4 of this Addendum.' It prints no change, obligation or exception of its own; the change to Volume V Clause 3…
  - validation: **evidence_verified**
- transition: `ADD-03/Q19-issue` issue {"text": "ambiguous: the cover says the Addendum 'reduces the unpaid sum that constitutes an Authority Event of Default under Volume V Clause 39.4 to SAR 8,000,000'; Section 4.1 (to which the Q19 res…
  - validation: **interpretation_pending — applied rule: VOL-I 3.2 provides: 'In the event of any conflict, ambiguity or discrepancy between or within the RFP Documents, the following order of precedence shall apply, the first named prevailing:' — the cover is the addendum's summary of itself, n…**
  - downstream proposal `D-18` dependency (impact:5. RESPONSES TO CLARIFICATION REQUESTS 15 TO 19): **interpretation_pending**
  - downstream proposal `D-19` dependency (impact:5. RESPONSES TO CLARIFICATION REQUESTS 15 TO 19): **interpretation_pending**

### ADD-03:AppA/para1 (paragraph, p3) — no effect (PROPOSED; not approved)
- source: “The following letter and table are reproduced as issued by the Northern Region Investment Services Office under its reference No. 228/2026 dated 16 November 2026. The Arabic text governs in accordance with Section 2.2 of this Addendum.”
- transition: `ADD-03/AppA/para1` disposition no_effect: The paragraph introduces the reproduction of the Office's letter and Table 8-1 ("The following letter and table are reproduced as issued by the Northern Region…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: ambiguous: the paragraph may not simply restate Section 2.2; it may reach further. The only quotation of ADD-03:2.2 shown (S-2.2) limits the Arabic-precedence rule to Table 8-1: "Table 8-1 is issued in the Arabic language. The Arabic text governs." AppA/para1 introduces both items, "The following l…
    - concern: "The Arabic text governs" is precedence wording, so it says which text prevails. Shared policy makes which text governs or prevails a person's decision, and a no_effect is a person's call where the words print or except something. So the controller's semantic check, which found "no amendment, oblig…
    - concern: The paragraph does not say whether the reproduced letter is incorporated into the tender documents or is information only. The item does not identify this as an open point. It only says that Table 8-1's incorporation is dealt with elsewhere. The letter's own status is not dealt with in this item.
    - concern: Only fragments of the full text of ADD-03:2.2 are shown in this request: "The Arabic text governs." and "Table 8-1 is issued in the Arabic language. The Arabic text governs." So I could not check whether 2.2 covers the letter as well. The controller records the 2.2 quotation as "verbatim in ADD-03:…
    - concern: Change propagation: the item names no follow-on work. If the letter's Arabic text governs, then any requirement, date or reference taken from the letter, and any translation of it used in A1 or A5, depends on this paragraph. These are not listed.
    - concern: Interpretation S-AppA-I1 has no evidence of its own. It is the basis for the whole disposition, and it is correctly left pending for a person.

### ADD-03:p3-image/r1 (table_row, p3) — UNRESOLVED (unaccounted)
- source: “م: ١ | فئة العضو: شركة مؤسسة في إحدى دول مجلس التعاون الخليجي | المستندات المطلوبة مع الطلب: السجل التجاري مصدقاً | مدة الإصدار (أيام عمل): ٣”
- transition: content of ADD-03/2.2
  - downstream proposal `D-20` issue (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **conflicting — applied rule: ADD-03 1.2 provides: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.' — a reference is to the clause as the earlier addenda left it (app…**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The issue-period values the item states ('row ١ ٣, row ٢ ٥, row ٣ ٨') are not quoted anywhere in the evidence shown. The printed unit ADD-03:p3-image gives only the table heading and intro sentence ('cells': null). Rows ١ and ٣ have no quotation at all. Row ٢ '٥' rests only on statement downstream-…
      - concern: The conflict between Arabic row ٢ and English row 2 ('3') cannot be confirmed from what is shown. The 'Issue period (Working Days): 3' cell of ADD-03:T8-1/2 is verified. The Arabic '٥' is a one-character reading quote that the controller rejects elsewhere as 'too short to be evidence' (D-23), and t…
      - concern: The crop details the item relies on are not in the evidence list: the date 'التاريخ: ١٦ نوفمبر ٢٠٢٦م', the reference 'الرقم: ٢٢٨/٢٠٢٦', the empty stamp oval at ADD-03:p3-image/stamp, and the signature mark with no name. Only the signatory title and the main region's crop hash are evidenced. The rat…
      - concern: The item says the values 'would feed ... the Section 2.5 notification', but no unit or quotation for Section 2.5 is shown.
      - concern: The controller's consistency check says the item 'reverses ADD-03/disp/1.2'. The item text does not address ADD-03 1.2 or explain the handback, so the clash is left unexplained.
      - concern: Correct as far as shown: Notes ١–٣ in (b)–(d) match the quoted readings of note1, note2 and note3. The item is kept conditional and pending. Acceptance of the unstamped letter is correctly left to a person, as a question for Document control and Legal.
  - downstream proposal `D-21` no_change (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **insufficient_evidence**

### ADD-03:p3-image/r2 (table_row, p3) — UNRESOLVED (unaccounted)
- source: “م: ٢ | فئة العضو: شركة مؤسسة خارج دول مجلس التعاون الخليجي | المستندات المطلوبة مع الطلب: السجل التجاري والقوائم المالية المدققة لآخر سنة مالية، مصدقة | مدة الإصدار (أيام عمل): ٥”
- transition: content of ADD-03/2.2
  - downstream proposal `D-20` issue (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **conflicting — applied rule: ADD-03 1.2 provides: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.' — a reference is to the clause as the earlier addenda left it (app…**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The issue-period values the item states ('row ١ ٣, row ٢ ٥, row ٣ ٨') are not quoted anywhere in the evidence shown. The printed unit ADD-03:p3-image gives only the table heading and intro sentence ('cells': null). Rows ١ and ٣ have no quotation at all. Row ٢ '٥' rests only on statement downstream-…
      - concern: The conflict between Arabic row ٢ and English row 2 ('3') cannot be confirmed from what is shown. The 'Issue period (Working Days): 3' cell of ADD-03:T8-1/2 is verified. The Arabic '٥' is a one-character reading quote that the controller rejects elsewhere as 'too short to be evidence' (D-23), and t…
      - concern: The crop details the item relies on are not in the evidence list: the date 'التاريخ: ١٦ نوفمبر ٢٠٢٦م', the reference 'الرقم: ٢٢٨/٢٠٢٦', the empty stamp oval at ADD-03:p3-image/stamp, and the signature mark with no name. Only the signatory title and the main region's crop hash are evidenced. The rat…
      - concern: The item says the values 'would feed ... the Section 2.5 notification', but no unit or quotation for Section 2.5 is shown.
      - concern: The controller's consistency check says the item 'reverses ADD-03/disp/1.2'. The item text does not address ADD-03 1.2 or explain the handback, so the clash is left unexplained.
      - concern: Correct as far as shown: Notes ١–٣ in (b)–(d) match the quoted readings of note1, note2 and note3. The item is kept conditional and pending. Acceptance of the unstamped letter is correctly left to a person, as a question for Document control and Legal.
  - downstream proposal `D-21` no_change (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **insufficient_evidence**

### ADD-03:p3-image/r3 (table_row, p3) — UNRESOLVED (unaccounted)
- source: “م: ٣ | فئة العضو: فرع مسجل في المملكة لشركة أجنبية | المستندات المطلوبة مع الطلب: شهادة تسجيل الفرع وقرار مجلس إدارة الشركة الأم بتفويض الفرع | مدة الإصدار (أيام عمل): ٨”
- transition: content of ADD-03/2.2
  - downstream proposal `D-20` issue (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **conflicting — applied rule: ADD-03 1.2 provides: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.' — a reference is to the clause as the earlier addenda left it (app…**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The issue-period values the item states ('row ١ ٣, row ٢ ٥, row ٣ ٨') are not quoted anywhere in the evidence shown. The printed unit ADD-03:p3-image gives only the table heading and intro sentence ('cells': null). Rows ١ and ٣ have no quotation at all. Row ٢ '٥' rests only on statement downstream-…
      - concern: The conflict between Arabic row ٢ and English row 2 ('3') cannot be confirmed from what is shown. The 'Issue period (Working Days): 3' cell of ADD-03:T8-1/2 is verified. The Arabic '٥' is a one-character reading quote that the controller rejects elsewhere as 'too short to be evidence' (D-23), and t…
      - concern: The crop details the item relies on are not in the evidence list: the date 'التاريخ: ١٦ نوفمبر ٢٠٢٦م', the reference 'الرقم: ٢٢٨/٢٠٢٦', the empty stamp oval at ADD-03:p3-image/stamp, and the signature mark with no name. Only the signatory title and the main region's crop hash are evidenced. The rat…
      - concern: The item says the values 'would feed ... the Section 2.5 notification', but no unit or quotation for Section 2.5 is shown.
      - concern: The controller's consistency check says the item 'reverses ADD-03/disp/1.2'. The item text does not address ADD-03 1.2 or explain the handback, so the clash is left unexplained.
      - concern: Correct as far as shown: Notes ١–٣ in (b)–(d) match the quoted readings of note1, note2 and note3. The item is kept conditional and pending. Acceptance of the unstamped letter is correctly left to a person, as a question for Document control and Legal.
  - downstream proposal `D-21` no_change (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **insufficient_evidence**

### ADD-03:p3-image/hdr-en (reading_block, p3) — UNRESOLVED (unaccounted)
- source: “Northern Region Investment Services Office”
- transition: content of ADD-03/2.2
  - downstream proposal `D-20` issue (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **conflicting — applied rule: ADD-03 1.2 provides: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.' — a reference is to the clause as the earlier addenda left it (app…**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The issue-period values the item states ('row ١ ٣, row ٢ ٥, row ٣ ٨') are not quoted anywhere in the evidence shown. The printed unit ADD-03:p3-image gives only the table heading and intro sentence ('cells': null). Rows ١ and ٣ have no quotation at all. Row ٢ '٥' rests only on statement downstream-…
      - concern: The conflict between Arabic row ٢ and English row 2 ('3') cannot be confirmed from what is shown. The 'Issue period (Working Days): 3' cell of ADD-03:T8-1/2 is verified. The Arabic '٥' is a one-character reading quote that the controller rejects elsewhere as 'too short to be evidence' (D-23), and t…
      - concern: The crop details the item relies on are not in the evidence list: the date 'التاريخ: ١٦ نوفمبر ٢٠٢٦م', the reference 'الرقم: ٢٢٨/٢٠٢٦', the empty stamp oval at ADD-03:p3-image/stamp, and the signature mark with no name. Only the signatory title and the main region's crop hash are evidenced. The rat…
      - concern: The item says the values 'would feed ... the Section 2.5 notification', but no unit or quotation for Section 2.5 is shown.
      - concern: The controller's consistency check says the item 'reverses ADD-03/disp/1.2'. The item text does not address ADD-03 1.2 or explain the handback, so the clash is left unexplained.
      - concern: Correct as far as shown: Notes ١–٣ in (b)–(d) match the quoted readings of note1, note2 and note3. The item is kept conditional and pending. Acceptance of the unstamped letter is correctly left to a person, as a question for Document control and Legal.
  - downstream proposal `D-21` no_change (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **insufficient_evidence**

### ADD-03:p3-image/hdr-ar (reading_block, p3) — UNRESOLVED (unaccounted)
- source: “مكتب خدمات الاستثمار بالمنطقة الشمالية”
- transition: content of ADD-03/2.2
  - downstream proposal `D-20` issue (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **conflicting — applied rule: ADD-03 1.2 provides: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.' — a reference is to the clause as the earlier addenda left it (app…**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The issue-period values the item states ('row ١ ٣, row ٢ ٥, row ٣ ٨') are not quoted anywhere in the evidence shown. The printed unit ADD-03:p3-image gives only the table heading and intro sentence ('cells': null). Rows ١ and ٣ have no quotation at all. Row ٢ '٥' rests only on statement downstream-…
      - concern: The conflict between Arabic row ٢ and English row 2 ('3') cannot be confirmed from what is shown. The 'Issue period (Working Days): 3' cell of ADD-03:T8-1/2 is verified. The Arabic '٥' is a one-character reading quote that the controller rejects elsewhere as 'too short to be evidence' (D-23), and t…
      - concern: The crop details the item relies on are not in the evidence list: the date 'التاريخ: ١٦ نوفمبر ٢٠٢٦م', the reference 'الرقم: ٢٢٨/٢٠٢٦', the empty stamp oval at ADD-03:p3-image/stamp, and the signature mark with no name. Only the signatory title and the main region's crop hash are evidenced. The rat…
      - concern: The item says the values 'would feed ... the Section 2.5 notification', but no unit or quotation for Section 2.5 is shown.
      - concern: The controller's consistency check says the item 'reverses ADD-03/disp/1.2'. The item text does not address ADD-03 1.2 or explain the handback, so the clash is left unexplained.
      - concern: Correct as far as shown: Notes ١–٣ in (b)–(d) match the quoted readings of note1, note2 and note3. The item is kept conditional and pending. Acceptance of the unstamped letter is correctly left to a person, as a question for Document control and Legal.
  - downstream proposal `D-21` no_change (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **insufficient_evidence**

### ADD-03:p3-image/date (reading_block, p3) — UNRESOLVED (unaccounted)
- source: “التاريخ: ١٦ نوفمبر ٢٠٢٦م”
- transition: content of ADD-03/2.2
  - downstream proposal `D-20` issue (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **conflicting — applied rule: ADD-03 1.2 provides: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.' — a reference is to the clause as the earlier addenda left it (app…**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The issue-period values the item states ('row ١ ٣, row ٢ ٥, row ٣ ٨') are not quoted anywhere in the evidence shown. The printed unit ADD-03:p3-image gives only the table heading and intro sentence ('cells': null). Rows ١ and ٣ have no quotation at all. Row ٢ '٥' rests only on statement downstream-…
      - concern: The conflict between Arabic row ٢ and English row 2 ('3') cannot be confirmed from what is shown. The 'Issue period (Working Days): 3' cell of ADD-03:T8-1/2 is verified. The Arabic '٥' is a one-character reading quote that the controller rejects elsewhere as 'too short to be evidence' (D-23), and t…
      - concern: The crop details the item relies on are not in the evidence list: the date 'التاريخ: ١٦ نوفمبر ٢٠٢٦م', the reference 'الرقم: ٢٢٨/٢٠٢٦', the empty stamp oval at ADD-03:p3-image/stamp, and the signature mark with no name. Only the signatory title and the main region's crop hash are evidenced. The rat…
      - concern: The item says the values 'would feed ... the Section 2.5 notification', but no unit or quotation for Section 2.5 is shown.
      - concern: The controller's consistency check says the item 'reverses ADD-03/disp/1.2'. The item text does not address ADD-03 1.2 or explain the handback, so the clash is left unexplained.
      - concern: Correct as far as shown: Notes ١–٣ in (b)–(d) match the quoted readings of note1, note2 and note3. The item is kept conditional and pending. Acceptance of the unstamped letter is correctly left to a person, as a question for Document control and Legal.
  - downstream proposal `D-21` no_change (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **insufficient_evidence**

### ADD-03:p3-image/ref (reading_block, p3) — UNRESOLVED (unaccounted)
- source: “الرقم: ٢٢٨/٢٠٢٦”
- transition: content of ADD-03/2.2
  - downstream proposal `D-20` issue (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **conflicting — applied rule: ADD-03 1.2 provides: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.' — a reference is to the clause as the earlier addenda left it (app…**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The issue-period values the item states ('row ١ ٣, row ٢ ٥, row ٣ ٨') are not quoted anywhere in the evidence shown. The printed unit ADD-03:p3-image gives only the table heading and intro sentence ('cells': null). Rows ١ and ٣ have no quotation at all. Row ٢ '٥' rests only on statement downstream-…
      - concern: The conflict between Arabic row ٢ and English row 2 ('3') cannot be confirmed from what is shown. The 'Issue period (Working Days): 3' cell of ADD-03:T8-1/2 is verified. The Arabic '٥' is a one-character reading quote that the controller rejects elsewhere as 'too short to be evidence' (D-23), and t…
      - concern: The crop details the item relies on are not in the evidence list: the date 'التاريخ: ١٦ نوفمبر ٢٠٢٦م', the reference 'الرقم: ٢٢٨/٢٠٢٦', the empty stamp oval at ADD-03:p3-image/stamp, and the signature mark with no name. Only the signatory title and the main region's crop hash are evidenced. The rat…
      - concern: The item says the values 'would feed ... the Section 2.5 notification', but no unit or quotation for Section 2.5 is shown.
      - concern: The controller's consistency check says the item 'reverses ADD-03/disp/1.2'. The item text does not address ADD-03 1.2 or explain the handback, so the clash is left unexplained.
      - concern: Correct as far as shown: Notes ١–٣ in (b)–(d) match the quoted readings of note1, note2 and note3. The item is kept conditional and pending. Acceptance of the unstamped letter is correctly left to a person, as a question for Document control and Legal.
  - downstream proposal `D-21` no_change (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **insufficient_evidence**

### ADD-03:p3-image/to (reading_block, p3) — UNRESOLVED (unaccounted)
- source: “إلى: الهيئة الشمالية للمشتريات المرفقية”
- transition: content of ADD-03/2.2
  - downstream proposal `D-20` issue (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **conflicting — applied rule: ADD-03 1.2 provides: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.' — a reference is to the clause as the earlier addenda left it (app…**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The issue-period values the item states ('row ١ ٣, row ٢ ٥, row ٣ ٨') are not quoted anywhere in the evidence shown. The printed unit ADD-03:p3-image gives only the table heading and intro sentence ('cells': null). Rows ١ and ٣ have no quotation at all. Row ٢ '٥' rests only on statement downstream-…
      - concern: The conflict between Arabic row ٢ and English row 2 ('3') cannot be confirmed from what is shown. The 'Issue period (Working Days): 3' cell of ADD-03:T8-1/2 is verified. The Arabic '٥' is a one-character reading quote that the controller rejects elsewhere as 'too short to be evidence' (D-23), and t…
      - concern: The crop details the item relies on are not in the evidence list: the date 'التاريخ: ١٦ نوفمبر ٢٠٢٦م', the reference 'الرقم: ٢٢٨/٢٠٢٦', the empty stamp oval at ADD-03:p3-image/stamp, and the signature mark with no name. Only the signatory title and the main region's crop hash are evidenced. The rat…
      - concern: The item says the values 'would feed ... the Section 2.5 notification', but no unit or quotation for Section 2.5 is shown.
      - concern: The controller's consistency check says the item 'reverses ADD-03/disp/1.2'. The item text does not address ADD-03 1.2 or explain the handback, so the clash is left unexplained.
      - concern: Correct as far as shown: Notes ١–٣ in (b)–(d) match the quoted readings of note1, note2 and note3. The item is kept conditional and pending. Acceptance of the unstamped letter is correctly left to a person, as a question for Document control and Legal.
  - downstream proposal `D-21` no_change (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **insufficient_evidence**

### ADD-03:p3-image/subject (reading_block, p3) — UNRESOLVED (unaccounted)
- source: “الموضوع: تسجيل استثمار أعضاء الائتلافات المؤسسين خارج المملكة”
- transition: content of ADD-03/2.2
  - downstream proposal `D-20` issue (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **conflicting — applied rule: ADD-03 1.2 provides: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.' — a reference is to the clause as the earlier addenda left it (app…**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The issue-period values the item states ('row ١ ٣, row ٢ ٥, row ٣ ٨') are not quoted anywhere in the evidence shown. The printed unit ADD-03:p3-image gives only the table heading and intro sentence ('cells': null). Rows ١ and ٣ have no quotation at all. Row ٢ '٥' rests only on statement downstream-…
      - concern: The conflict between Arabic row ٢ and English row 2 ('3') cannot be confirmed from what is shown. The 'Issue period (Working Days): 3' cell of ADD-03:T8-1/2 is verified. The Arabic '٥' is a one-character reading quote that the controller rejects elsewhere as 'too short to be evidence' (D-23), and t…
      - concern: The crop details the item relies on are not in the evidence list: the date 'التاريخ: ١٦ نوفمبر ٢٠٢٦م', the reference 'الرقم: ٢٢٨/٢٠٢٦', the empty stamp oval at ADD-03:p3-image/stamp, and the signature mark with no name. Only the signatory title and the main region's crop hash are evidenced. The rat…
      - concern: The item says the values 'would feed ... the Section 2.5 notification', but no unit or quotation for Section 2.5 is shown.
      - concern: The controller's consistency check says the item 'reverses ADD-03/disp/1.2'. The item text does not address ADD-03 1.2 or explain the handback, so the clash is left unexplained.
      - concern: Correct as far as shown: Notes ١–٣ in (b)–(d) match the quoted readings of note1, note2 and note3. The item is kept conditional and pending. Acceptance of the unstamped letter is correctly left to a person, as a question for Document control and Legal.
  - downstream proposal `D-21` no_change (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **insufficient_evidence**

### ADD-03:p3-image/tender (reading_block, p3) — UNRESOLVED (unaccounted)
- source: “مناقصة رقم: NUPA/ISTP/2026/014 (محطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان)”
- transition: content of ADD-03/2.2
  - downstream proposal `D-20` issue (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **conflicting — applied rule: ADD-03 1.2 provides: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.' — a reference is to the clause as the earlier addenda left it (app…**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The issue-period values the item states ('row ١ ٣, row ٢ ٥, row ٣ ٨') are not quoted anywhere in the evidence shown. The printed unit ADD-03:p3-image gives only the table heading and intro sentence ('cells': null). Rows ١ and ٣ have no quotation at all. Row ٢ '٥' rests only on statement downstream-…
      - concern: The conflict between Arabic row ٢ and English row 2 ('3') cannot be confirmed from what is shown. The 'Issue period (Working Days): 3' cell of ADD-03:T8-1/2 is verified. The Arabic '٥' is a one-character reading quote that the controller rejects elsewhere as 'too short to be evidence' (D-23), and t…
      - concern: The crop details the item relies on are not in the evidence list: the date 'التاريخ: ١٦ نوفمبر ٢٠٢٦م', the reference 'الرقم: ٢٢٨/٢٠٢٦', the empty stamp oval at ADD-03:p3-image/stamp, and the signature mark with no name. Only the signatory title and the main region's crop hash are evidenced. The rat…
      - concern: The item says the values 'would feed ... the Section 2.5 notification', but no unit or quotation for Section 2.5 is shown.
      - concern: The controller's consistency check says the item 'reverses ADD-03/disp/1.2'. The item text does not address ADD-03 1.2 or explain the handback, so the clash is left unexplained.
      - concern: Correct as far as shown: Notes ١–٣ in (b)–(d) match the quoted readings of note1, note2 and note3. The item is kept conditional and pending. Acceptance of the unstamped letter is correctly left to a person, as a question for Document control and Legal.
  - downstream proposal `D-21` no_change (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **insufficient_evidence**

### ADD-03:p3-image/notes-heading (reading_block, p3) — UNRESOLVED (unaccounted)
- source: “ملاحظات:”
- transition: content of ADD-03/2.2
  - downstream proposal `D-20` issue (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **conflicting — applied rule: ADD-03 1.2 provides: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.' — a reference is to the clause as the earlier addenda left it (app…**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The issue-period values the item states ('row ١ ٣, row ٢ ٥, row ٣ ٨') are not quoted anywhere in the evidence shown. The printed unit ADD-03:p3-image gives only the table heading and intro sentence ('cells': null). Rows ١ and ٣ have no quotation at all. Row ٢ '٥' rests only on statement downstream-…
      - concern: The conflict between Arabic row ٢ and English row 2 ('3') cannot be confirmed from what is shown. The 'Issue period (Working Days): 3' cell of ADD-03:T8-1/2 is verified. The Arabic '٥' is a one-character reading quote that the controller rejects elsewhere as 'too short to be evidence' (D-23), and t…
      - concern: The crop details the item relies on are not in the evidence list: the date 'التاريخ: ١٦ نوفمبر ٢٠٢٦م', the reference 'الرقم: ٢٢٨/٢٠٢٦', the empty stamp oval at ADD-03:p3-image/stamp, and the signature mark with no name. Only the signatory title and the main region's crop hash are evidenced. The rat…
      - concern: The item says the values 'would feed ... the Section 2.5 notification', but no unit or quotation for Section 2.5 is shown.
      - concern: The controller's consistency check says the item 'reverses ADD-03/disp/1.2'. The item text does not address ADD-03 1.2 or explain the handback, so the clash is left unexplained.
      - concern: Correct as far as shown: Notes ١–٣ in (b)–(d) match the quoted readings of note1, note2 and note3. The item is kept conditional and pending. Acceptance of the unstamped letter is correctly left to a person, as a question for Document control and Legal.
  - downstream proposal `D-21` no_change (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **insufficient_evidence**

### ADD-03:p3-image/note1 (reading_block, p3) — UNRESOLVED (unaccounted)
- source: “١. تُحسب مدة الإصدار بأيام العمل اعتباراً من يوم العمل التالي ليوم استلام الطلب المكتمل.”
- transition: content of ADD-03/2.2
  - downstream proposal `D-20` issue (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **conflicting — applied rule: ADD-03 1.2 provides: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.' — a reference is to the clause as the earlier addenda left it (app…**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The issue-period values the item states ('row ١ ٣, row ٢ ٥, row ٣ ٨') are not quoted anywhere in the evidence shown. The printed unit ADD-03:p3-image gives only the table heading and intro sentence ('cells': null). Rows ١ and ٣ have no quotation at all. Row ٢ '٥' rests only on statement downstream-…
      - concern: The conflict between Arabic row ٢ and English row 2 ('3') cannot be confirmed from what is shown. The 'Issue period (Working Days): 3' cell of ADD-03:T8-1/2 is verified. The Arabic '٥' is a one-character reading quote that the controller rejects elsewhere as 'too short to be evidence' (D-23), and t…
      - concern: The crop details the item relies on are not in the evidence list: the date 'التاريخ: ١٦ نوفمبر ٢٠٢٦م', the reference 'الرقم: ٢٢٨/٢٠٢٦', the empty stamp oval at ADD-03:p3-image/stamp, and the signature mark with no name. Only the signatory title and the main region's crop hash are evidenced. The rat…
      - concern: The item says the values 'would feed ... the Section 2.5 notification', but no unit or quotation for Section 2.5 is shown.
      - concern: The controller's consistency check says the item 'reverses ADD-03/disp/1.2'. The item text does not address ADD-03 1.2 or explain the handback, so the clash is left unexplained.
      - concern: Correct as far as shown: Notes ١–٣ in (b)–(d) match the quoted readings of note1, note2 and note3. The item is kept conditional and pending. Acceptance of the unstamped letter is correctly left to a person, as a question for Document control and Legal.
  - downstream proposal `D-21` no_change (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **insufficient_evidence**

### ADD-03:p3-image/note2 (reading_block, p3) — UNRESOLVED (unaccounted)
- source: “٢. تكون الشهادة سارية لمدة تسعين (٩٠) يوماً من تاريخ إصدارها.”
- transition: content of ADD-03/2.2
  - downstream proposal `D-20` issue (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **conflicting — applied rule: ADD-03 1.2 provides: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.' — a reference is to the clause as the earlier addenda left it (app…**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The issue-period values the item states ('row ١ ٣, row ٢ ٥, row ٣ ٨') are not quoted anywhere in the evidence shown. The printed unit ADD-03:p3-image gives only the table heading and intro sentence ('cells': null). Rows ١ and ٣ have no quotation at all. Row ٢ '٥' rests only on statement downstream-…
      - concern: The conflict between Arabic row ٢ and English row 2 ('3') cannot be confirmed from what is shown. The 'Issue period (Working Days): 3' cell of ADD-03:T8-1/2 is verified. The Arabic '٥' is a one-character reading quote that the controller rejects elsewhere as 'too short to be evidence' (D-23), and t…
      - concern: The crop details the item relies on are not in the evidence list: the date 'التاريخ: ١٦ نوفمبر ٢٠٢٦م', the reference 'الرقم: ٢٢٨/٢٠٢٦', the empty stamp oval at ADD-03:p3-image/stamp, and the signature mark with no name. Only the signatory title and the main region's crop hash are evidenced. The rat…
      - concern: The item says the values 'would feed ... the Section 2.5 notification', but no unit or quotation for Section 2.5 is shown.
      - concern: The controller's consistency check says the item 'reverses ADD-03/disp/1.2'. The item text does not address ADD-03 1.2 or explain the handback, so the clash is left unexplained.
      - concern: Correct as far as shown: Notes ١–٣ in (b)–(d) match the quoted readings of note1, note2 and note3. The item is kept conditional and pending. Acceptance of the unstamped letter is correctly left to a person, as a question for Document control and Legal.
  - downstream proposal `D-21` no_change (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **insufficient_evidence**

### ADD-03:p3-image/note3 (reading_block, p3) — UNRESOLVED (unaccounted)
- source: “٣. تُقدِّم الطلبات إلكترونياً عبر بوابة المكتب فقط، ولا يُعدّ الطلب مكتملاً إلا بإرفاق جميع المستندات المبيِّنة أعلاه.”
- transition: content of ADD-03/2.2
  - downstream proposal `D-20` issue (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **conflicting — applied rule: ADD-03 1.2 provides: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.' — a reference is to the clause as the earlier addenda left it (app…**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The issue-period values the item states ('row ١ ٣, row ٢ ٥, row ٣ ٨') are not quoted anywhere in the evidence shown. The printed unit ADD-03:p3-image gives only the table heading and intro sentence ('cells': null). Rows ١ and ٣ have no quotation at all. Row ٢ '٥' rests only on statement downstream-…
      - concern: The conflict between Arabic row ٢ and English row 2 ('3') cannot be confirmed from what is shown. The 'Issue period (Working Days): 3' cell of ADD-03:T8-1/2 is verified. The Arabic '٥' is a one-character reading quote that the controller rejects elsewhere as 'too short to be evidence' (D-23), and t…
      - concern: The crop details the item relies on are not in the evidence list: the date 'التاريخ: ١٦ نوفمبر ٢٠٢٦م', the reference 'الرقم: ٢٢٨/٢٠٢٦', the empty stamp oval at ADD-03:p3-image/stamp, and the signature mark with no name. Only the signatory title and the main region's crop hash are evidenced. The rat…
      - concern: The item says the values 'would feed ... the Section 2.5 notification', but no unit or quotation for Section 2.5 is shown.
      - concern: The controller's consistency check says the item 'reverses ADD-03/disp/1.2'. The item text does not address ADD-03 1.2 or explain the handback, so the clash is left unexplained.
      - concern: Correct as far as shown: Notes ١–٣ in (b)–(d) match the quoted readings of note1, note2 and note3. The item is kept conditional and pending. Acceptance of the unstamped letter is correctly left to a person, as a question for Document control and Legal.
  - downstream proposal `D-21` no_change (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **insufficient_evidence**

### ADD-03:p3-image/stamp (reading_block, p3) — UNRESOLVED (unaccounted)
- source: “”
- transition: content of ADD-03/2.2
  - downstream proposal `D-20` issue (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **conflicting — applied rule: ADD-03 1.2 provides: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.' — a reference is to the clause as the earlier addenda left it (app…**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The issue-period values the item states ('row ١ ٣, row ٢ ٥, row ٣ ٨') are not quoted anywhere in the evidence shown. The printed unit ADD-03:p3-image gives only the table heading and intro sentence ('cells': null). Rows ١ and ٣ have no quotation at all. Row ٢ '٥' rests only on statement downstream-…
      - concern: The conflict between Arabic row ٢ and English row 2 ('3') cannot be confirmed from what is shown. The 'Issue period (Working Days): 3' cell of ADD-03:T8-1/2 is verified. The Arabic '٥' is a one-character reading quote that the controller rejects elsewhere as 'too short to be evidence' (D-23), and t…
      - concern: The crop details the item relies on are not in the evidence list: the date 'التاريخ: ١٦ نوفمبر ٢٠٢٦م', the reference 'الرقم: ٢٢٨/٢٠٢٦', the empty stamp oval at ADD-03:p3-image/stamp, and the signature mark with no name. Only the signatory title and the main region's crop hash are evidenced. The rat…
      - concern: The item says the values 'would feed ... the Section 2.5 notification', but no unit or quotation for Section 2.5 is shown.
      - concern: The controller's consistency check says the item 'reverses ADD-03/disp/1.2'. The item text does not address ADD-03 1.2 or explain the handback, so the clash is left unexplained.
      - concern: Correct as far as shown: Notes ١–٣ in (b)–(d) match the quoted readings of note1, note2 and note3. The item is kept conditional and pending. Acceptance of the unstamped letter is correctly left to a person, as a question for Document control and Legal.
  - downstream proposal `D-21` no_change (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **insufficient_evidence**

### ADD-03:p3-image/signatory (reading_block, p3) — UNRESOLVED (unaccounted)
- source: “مدير مكتب خدمات الاستثمار بالمنطقة الشمالية”
- transition: content of ADD-03/2.2
  - downstream proposal `D-20` issue (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **conflicting — applied rule: ADD-03 1.2 provides: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.' — a reference is to the clause as the earlier addenda left it (app…**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The issue-period values the item states ('row ١ ٣, row ٢ ٥, row ٣ ٨') are not quoted anywhere in the evidence shown. The printed unit ADD-03:p3-image gives only the table heading and intro sentence ('cells': null). Rows ١ and ٣ have no quotation at all. Row ٢ '٥' rests only on statement downstream-…
      - concern: The conflict between Arabic row ٢ and English row 2 ('3') cannot be confirmed from what is shown. The 'Issue period (Working Days): 3' cell of ADD-03:T8-1/2 is verified. The Arabic '٥' is a one-character reading quote that the controller rejects elsewhere as 'too short to be evidence' (D-23), and t…
      - concern: The crop details the item relies on are not in the evidence list: the date 'التاريخ: ١٦ نوفمبر ٢٠٢٦م', the reference 'الرقم: ٢٢٨/٢٠٢٦', the empty stamp oval at ADD-03:p3-image/stamp, and the signature mark with no name. Only the signatory title and the main region's crop hash are evidenced. The rat…
      - concern: The item says the values 'would feed ... the Section 2.5 notification', but no unit or quotation for Section 2.5 is shown.
      - concern: The controller's consistency check says the item 'reverses ADD-03/disp/1.2'. The item text does not address ADD-03 1.2 or explain the handback, so the clash is left unexplained.
      - concern: Correct as far as shown: Notes ١–٣ in (b)–(d) match the quoted readings of note1, note2 and note3. The item is kept conditional and pending. Acceptance of the unstamped letter is correctly left to a person, as a question for Document control and Legal.
  - downstream proposal `D-21` no_change (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **insufficient_evidence**

### ADD-03:p3-image/image-footer (reading_block, p3) — UNRESOLVED (unaccounted)
- source: “FICTIONAL DOCUMENT - Lamar Holding internal assessment pack - not a real tender. SYNTHETIC: not tender content.”
- transition: content of ADD-03/2.2
  - downstream proposal `D-20` issue (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **conflicting — applied rule: ADD-03 1.2 provides: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.' — a reference is to the clause as the earlier addenda left it (app…**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: The issue-period values the item states ('row ١ ٣, row ٢ ٥, row ٣ ٨') are not quoted anywhere in the evidence shown. The printed unit ADD-03:p3-image gives only the table heading and intro sentence ('cells': null). Rows ١ and ٣ have no quotation at all. Row ٢ '٥' rests only on statement downstream-…
      - concern: The conflict between Arabic row ٢ and English row 2 ('3') cannot be confirmed from what is shown. The 'Issue period (Working Days): 3' cell of ADD-03:T8-1/2 is verified. The Arabic '٥' is a one-character reading quote that the controller rejects elsewhere as 'too short to be evidence' (D-23), and t…
      - concern: The crop details the item relies on are not in the evidence list: the date 'التاريخ: ١٦ نوفمبر ٢٠٢٦م', the reference 'الرقم: ٢٢٨/٢٠٢٦', the empty stamp oval at ADD-03:p3-image/stamp, and the signature mark with no name. Only the signatory title and the main region's crop hash are evidenced. The rat…
      - concern: The item says the values 'would feed ... the Section 2.5 notification', but no unit or quotation for Section 2.5 is shown.
      - concern: The controller's consistency check says the item 'reverses ADD-03/disp/1.2'. The item text does not address ADD-03 1.2 or explain the handback, so the clash is left unexplained.
      - concern: Correct as far as shown: Notes ١–٣ in (b)–(d) match the quoted readings of note1, note2 and note3. The item is kept conditional and pending. Acceptance of the unstamped letter is correctly left to a person, as a question for Document control and Legal.
  - downstream proposal `D-21` no_change (impact:APPENDIX A — TABLE 8-1 (ARABIC)): **insufficient_evidence**

### ADD-03:AppA/para2 (paragraph, p3) — no effect (PROPOSED; not approved)
- source: “End of reproduction.”
- transition: `ADD-03/AppA/para2` disposition no_effect: The paragraph reads only "End of reproduction.": it marks the end of the reproduced letter and table in Appendix A, names no unit and prints no change, obligat…
  - validation: **evidence_verified**

### ADD-03:AppB/para1 (paragraph, p3) — no effect (PROPOSED; not approved)
- source: “This translation is provided for convenience only. The Arabic text of Table 8-1 at Appendix A governs. Northern Region Investment Services Office, reference No. 228/2026 dated 16 November 2026, to the Northern Utilities Procurement Authority. Subject: investment registration of consortium members incorporated outside the Kingdom. Tender No. NUPA/ISTP/2026/0…”
- transition: `ADD-03/AppB/para1:disp` disposition no_effect: The paragraph introduces a convenience translation and amends no volume unit. It prints 'This translation is provided for convenience only. The Arabic text of …
  - validation: **evidence_verified**

### ADD-03:AppB/para2 (paragraph, p4) — no effect (PROPOSED; not approved)
- source: “The Office issues a Certificate of Investment Registration to a member incorporated outside the Kingdom within the period stated below for its class.”
- transition: `ADD-03/AppB/para2:disp` disposition no_effect: This translates the Arabic qualifier of Table 8-1 and amends no unit. The translation is non-governing: ADD-03:AppB/para1 prints 'This translation is provided …
  - validation: **evidence_verified**

### ADD-03:T8-1/1 (table_row, p4) — no effect (PROPOSED; not approved)
- source: “No: 1 | Class of member: Company incorporated in a GCC state | Documents required with the application: Certified commercial registration | Issue period (Working Days): 3”
- transition: `ADD-03/T8-1/1:disp` disposition no_effect: This is the convenience translation of row 1 of Table 8-1. The word 'required' appears only in the translated column heading 'Documents required with the appli…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'required')

### ADD-03:T8-1/2 (table_row, p4) — no effect (PROPOSED; not approved)
- source: “No: 2 | Class of member: Company incorporated outside the GCC states | Documents required with the application: Commercial registration and audited financial statements for the last financial year, certified | Issue period (Working Days): 3”
- transition: `ADD-03/T8-1/2:disp` disposition no_effect: This is the convenience translation of row 2 of Table 8-1. The word 'required' appears only in the translated column heading 'Documents required with the appli…
  - validation: **interpretation_pending — applied rule: the stated precedence orders the two renderings (ADD-03:p3-image/r2 against ADD-03:T8-1/2): ADD-03 2.2 provides: 'The Arabic text governs.' (applied, not decided); ADD-03:T8-1/2 is the rendering the rule makes subordinate: ADD-03:p3-image …** — semantic: no_effect on amendment language: a person must confirm (its words carry 'required')
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
    - concern: The no_effect reason goes beyond recording that the translation amends nothing. It says 'the 3 must not be used as the row 2 period'. That applies ADD-03:2.2 to settle the discrepancy, but which figure governs is a person's decision. It also contradicts the companion issue ADD-03/T8-1/2:issue, whic…
    - concern: It calls ADD-03:p3-image/r2 the 'governing Arabic row', but the rationale and S-F3 both say the reading of that row is still pending approval. A disposition that settles the effect of the translation should not rest on an unapproved reading as if it were confirmed.
    - concern: The heading 'Documents required with the application' carries 'required', so the controller rightly flags no_effect on wording that obliges. The proposer's line 'A person confirms' is fine, but the item is marked ready:true while it depends on a pending reading and an open issue.
    - concern: The follow-on work names 'Clause 2.3's undertaking' and other dependents. ADD-03:2.3 is not among the evidence shown, so I cannot check those links.
    - concern: Not a defect: the documents cell matches the Arabic cell ('السجل التجاري والقوائم المالية المدققة لآخر سنة مالية، مصدقة'). The only difference shown is the issue period, 3 against ٥.
- transition: `ADD-03/T8-1/2:issue` issue {"text": "ambiguous: Table 8-1 row 2 (company incorporated outside the GCC states). The governing Arabic (ADD-03:p3-image/r2, reading pending) prints 'مدة الإصدار (أيام عمل): ٥'. The English translat…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Reading (b) assumes the translation's 3 is the 5 after Q16's two-day reduction. That rests on unstated arithmetic and nothing printed supports it. It is a plausible alternative, but the issue should say that reading (b) is an inference from the figures, not something the pack says.
    - concern: The decision owner here is Legal, but the linked clarification ADD-03/T8-1/2:q names Bid management. The owners should be made consistent, or the split explained.
    - concern: The target is ADD-03:p3-image/r2, which the provision does not cite (the controller flags uncertain_target). The issue really concerns both units. The person deciding should know the target was chosen by the proposer.
    - concern: The dependency ADD-03:2.3 is listed, but no evidence for it is shown, so I cannot check it.
    - concern: The Arabic reading of ٥ is still pending approval. The issue says so, which is correct, but the open question also depends on that reading being approved.
- transition: `ADD-03/T8-1/2:q` clarification {"gap": "ambiguous: for row 2 of Table 8-1, the governing Arabic prints ٥ Working Days and the English translation at Appendix B prints 3. Q16 separately reduces the row 2 period by two Working Days …
  - validation: **interpretation_pending — HUMAN DECISION PENDING — applied rule: ADD-03 2.2 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The draft question is leading. It asks the issuer to 'confirm that the Arabic figure of five (5) Working Days governs' and that the reduction applies to that figure. That builds in reading (a) and leaves out reading (b) from S-I1. A neutral draft would ask which row 2 issue period applies and how t…
    - concern: interim_handling ('Plan on the governing Arabic figure without the conditional reduction... Do not use the translation's 3') chooses a reading and sets a planning basis. If the proposer wants an interim basis, it must be a separate statement labelled 'PROVISIONAL ASSUMPTION:' with its basis. As wri…
    - concern: practical_impact cites Clause 2.1 ('shall be rejected') and a 'Certificate of Investment Registration'. Neither Clause 2.1 nor any unit naming that certificate is in the item's evidence or in the units shown. A rejection consequence must be quoted from the unit that states it, and here it cannot be…
    - concern: The decision owner is Bid management, but the linked issue names Legal. The owners are inconsistent.
    - concern: The Arabic ٥ comes from a reading that is still pending approval. Sending a question that states it as fact before the reading is approved should be flagged.
  - downstream proposal `D-23` dependency (impact:APPENDIX B — ENGLISH TRANSLATION OF TABLE 8-1): **conflicting — applied rule: ADD-03 2.2 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
      - concern: One end of the dependency is ADD-03:p3-image/r2 '٥'. That unit is not among the printed units, and the controller rejects its quotation as 'too short to be evidence'. The supporting statement downstream-002/ST-F5 is marked 'not supported verbatim'. The Arabic side of the dependency is therefore not…
      - concern: The basis is 'CONDITIONAL on analysis issue ADD-03/T8-1/2:issue', yet the payload's 'issues' list is empty. The condition is not linked.
      - concern: The controller says this item 'reverses ADD-03/2.2-issue', which applied 'The Arabic text governs.' The item quotes 2.2 but then leaves the choice of value to a person without saying how this squares with the rule already applied. Leaving the choice to a person is right while the reading is pending…
      - concern: ST-F4 says Section 2.2 states that 'Table 8-1 is issued in Arabic'. The quoted words ('The Arabic text governs. The English translation at Appendix B is provided for convenience only.') do not say that in terms; the statement goes further than its quote.
      - concern: Correct as far as shown: the English cell '3' is verified at ADD-03:T8-1/2. The relationship stays 'possible'. The lead-time key investment_licence is labelled a PROVISIONAL ASSUMPTION. The program does not pick a value.

### ADD-03:T8-1/3 (table_row, p4) — no effect (PROPOSED; not approved)
- source: “No: 3 | Class of member: Branch registered in the Kingdom of a foreign company | Documents required with the application: Branch registration certificate and parent company board resolution authorising the branch | Issue period (Working Days): 8”
- transition: `ADD-03/T8-1/3:disp` disposition no_effect: This is the convenience translation of row 3 of Table 8-1. The word 'required' appears only in the translated column heading 'Documents required with the appli…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'required')

### ADD-03:T8-1/notes (note_intro, p4) — no effect (PROPOSED; not approved)
- source: “Notes to Table 8-1:”
- transition: `ADD-03/T8-1/notes:disp` disposition no_effect: This is a heading only ('Notes to Table 8-1:') in the convenience translation and amends nothing. ADD-03:2.2 prints 'The English translation at Appendix B is p…
  - validation: **evidence_verified**

### ADD-03:T8-1/note(1) (note, p4) — no effect (PROPOSED; not approved)
- source: “(1) The issue period is counted in Working Days from the Working Day following the day of receipt of a complete application.”
- transition: `ADD-03/T8-1/note(1):disp` disposition no_effect: This is the convenience translation of Note 1 (the counting rule) and amends no unit. ADD-03:AppB/para1 prints 'This translation is provided for convenience on…
  - validation: **evidence_verified**

### ADD-03:T8-1/note(2) (note, p4) — no effect (PROPOSED; not approved)
- source: “(2) A Certificate is valid for ninety (90) days from its date of issue.”
- transition: `ADD-03/T8-1/note(2):disp` disposition no_effect: This is the convenience translation of Note 2 (90-day certificate validity) and amends no unit. ADD-03:2.2 prints 'The English translation at Appendix B is pro…
  - validation: **evidence_verified**

### ADD-03:T8-1/note(3) (note, p4) — no effect (PROPOSED; not approved)
- source: “(3) Applications are made electronically through the Office's portal only. An application is complete only when all the documents listed above are attached.”
- transition: `ADD-03/T8-1/note(3):disp` disposition no_effect: This is the convenience translation of Note 3. Its words restrict ('through the Office's portal only'; 'complete only when all the documents listed above are a…
  - validation: **evidence_verified**

### ADD-03:AppB/para3 (paragraph, p4) — no effect (PROPOSED; not approved)
- source: “Signed: Director, Northern Region Investment Services Office (signature and stamp).”
- transition: `ADD-03/AppB/para3:disp` disposition no_effect: This is the translated signature block of the Office's letter and amends nothing. ADD-03:2.2 prints 'The English translation at Appendix B is provided for conv…
  - validation: **evidence_verified**

## Downstream proposals (validated in the candidate)

| Item | Type | Task | Status | First failed check, or what a person confirms |
|---|---|---|---|---|
| DS-01 | row_reading | row:VOL-I-12.2-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-02 | row_reading | row:VOL-I-12.2-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-03 | row_reading | row:VOL-I-8.9-01 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words decides which clause governs ('governs') |
| DS-04 | row_reading | row:VOL-V-44.2-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-05 | row_new | c46:ADD-03/cover/para3 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-06 | issue | c46:ADD-03/cover/para3 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-07 | row_new | c46:ADD-03/3.1 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-08 | issue | c46:ADD-03/3.1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-09 | dependency | c46:ADD-03/3.1 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| DS-10 | row_new | ana:ADD-03/2.3-row | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-11 | row_new | ana:ADD-03/2.4-row | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-12 | row_new | ana:ADD-03/2.5-row | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-13 | evidence_item | ana:ADD-03/2.5-row | evidence_verified |  |
| DS-14 | activity | ana:ADD-03/2.5-row | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| DS-15 | row_new | ana:ADD-03/row-3.4 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-16 | issue | ana:ADD-03/row-3.4 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-17 | no_change | act:investment-licence | interpretation_pending |  |
| DS-18 | issue | esc:ADD-03:2.1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-19 | escalation | esc:ADD-03:2.1 | escalated |  |
| D-01 | escalation | esc:ADD-03:2.2 | escalated | statements: fact downstream-002/ST-F5 is not supported verbatim |
| D-02 | dependency | esc:ADD-03:2.2 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| D-03 | escalation | esc:ADD-03:2.4 | escalated |  |
| D-04 | issue | esc:ADD-03:2.4 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| D-05 | issue | esc:ADD-03:2.5 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| D-06 | escalation | esc:ADD-03:2.5 | escalated |  |
| D-07 | escalation | esc:ADD-03:3.3 | escalated |  |
| D-08 | escalation | esc:ADD-03:Q16 | escalated | statements: fact downstream-002/ST-F5 is not supported verbatim |
| D-09 | issue | esc:ADD-03:Q16 | insufficient_evidence — HUMAN DECISION PENDING | evidence ADD-03:p3-image/r2 p3: the quotation is too short to be evidence |
| D-10 | dependency | impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS | interpretation_pending | an inferred relationship stays `possible`: a person confirms or rejects it |
| D-11 | dependency | impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS | interpretation_pending | an inferred relationship stays `possible`: a person confirms or rejects it |
| D-12 | issue | impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| D-13 | issue | impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| D-14 | escalation | impact:2. INVESTMENT REGISTRATION OF FOREIGN MEMBERS | escalated |  |
| D-15 | dependency | impact:3. TREATED EFFLUENT STORAGE AND SCHEDULED PCOD | interpretation_pending | an inferred relationship stays `possible`: a person confirms or rejects it |
| D-16 | escalation | impact:3. TREATED EFFLUENT STORAGE AND SCHEDULED PCOD | escalated |  |
| D-17 | dependency | impact:3. TREATED EFFLUENT STORAGE AND SCHEDULED PCOD | interpretation_pending | an inferred relationship stays `possible`: a person confirms or rejects it |
| D-18 | dependency | impact:5. RESPONSES TO CLARIFICATION REQUESTS 15 TO 19 | interpretation_pending | an inferred relationship stays `possible`: a person confirms or rejects it |
| D-19 | dependency | impact:5. RESPONSES TO CLARIFICATION REQUESTS 15 TO 19 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| D-20 | issue | impact:APPENDIX A — TABLE 8-1 (ARABIC) | conflicting — applied rule: ADD-03 1.2 provides: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.' — a reference is to the clause as the earlier addenda left it (app… | statements: fact downstream-002/ST-F5 is not supported verbatim |
| D-21 | no_change | impact:APPENDIX A — TABLE 8-1 (ARABIC) | insufficient_evidence | statements: fact downstream-002/ST-F5 is not supported verbatim |
| D-22 | no_change | impact:1. RECITALS | interpretation_pending |  |
| D-23 | dependency | impact:APPENDIX B — ENGLISH TRANSLATION OF TABLE 8-1 | conflicting — applied rule: ADD-03 2.2 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application | evidence ADD-03:p3-image/r2 p3: the quotation is too short to be evidence |
| D-24 | no_change | impact:4. AUTHORITY EVENT OF DEFAULT | interpretation_pending |  |
| D-ROW-01 | row_new | reading:ADD-03-p3-r1 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-ROW-02 | row_new | reading:ADD-03-p3-r1 | conflicting | declared_conflicts: the proposer declares: ADD-03:T8-1/2; ADD-03:Q16 |
| D-ROW-03 | row_new | reading:ADD-03-p3-r1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words declares a matter resolved ('resolution') |
| D-ROW-04 | row_new | reading:ADD-03-p3-r1 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-ROW-05 | row_new | reading:ADD-03-p3-r1 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-EV-01 | evidence_item | reading:ADD-03-p3-r1 | interpretation_pending |  |
| D-ACT-01 | activity | reading:ADD-03-p3-r1 | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| D-ISS-01 | issue | reading:ADD-03-p3-r1 | conflicting — applied rule: ADD-03 2.2 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application | consistency (phases): reverses ADD-03/2.2-issue (ADD-03:2.2), which applied ADD-03 2.2 ('Section 2.2 says 'The Arabic text governs.'): this item hands the point back to a person; ADD-03 2.2 provides:… |
| D-ISS-02 | issue | reading:ADD-03-p3-r1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| D-ISS-03 | issue | reading:ADD-03-p3-r1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| D-CQ-01 | clarification_item | reading:ADD-03-p3-r1 | conflicting — applied rule: ADD-03 2.2 provides: 'The Arabic text governs.' (applied, not decided); a person confirms the application | consistency (phases): reverses ADD-03/2.2-issue (ADD-03:2.2), which applied ADD-03 2.2 ('Section 2.2 says 'The Arabic text governs.'): this item hands the point back to a person; ADD-03 2.2 provides:… |
| D-ESC-01 | escalation | reading:ADD-03-p3-r1 | escalated |  |

- interactions: D-20: reverses ADD-03/disp/1.2 (ADD-03:1.2), which applied ADD-03 1.2 ('Interpretation rule for the Addendum's own references: 'A reference in this Addendum to a Clause, Table or Form is to that Clau…; D-23: reverses ADD-03/2.2-issue (ADD-03:2.2), which applied ADD-03 2.2 ('Section 2.2 says 'The Arabic text governs.'): this item hands the point back to a person; ADD-03 2.2 provides: 'The Arabic tex…; D-ISS-01: reverses ADD-03/2.2-issue (ADD-03:2.2), which applied ADD-03 2.2 ('Section 2.2 says 'The Arabic text governs.'): this item hands the point back to a person; ADD-03 2.2 provides: 'The Arabic…; D-CQ-01: reverses ADD-03/2.2-issue (ADD-03:2.2), which applied ADD-03 2.2 ('Section 2.2 says 'The Arabic text governs.'): this item hands the point back to a person; ADD-03 2.2 provides: 'The Arabic …
- A5 problems the proposals would add: none

## Promoted into the candidate (PROPOSED; nothing accepted)

- ops: ADD-03/cover/para3, ADD-03/2.6, ADD-03/3.1, ADD-03/4.1, ADD-03/4.2, ADD-03/Q15, ADD-03/Q17
- dispositions: ADD-03:cover/para1: no_effect, ADD-03:cover/para2: no_effect, ADD-03:1.1: no_effect, ADD-03:1.2: no_effect, ADD-03:1.3: no_effect, ADD-03:Q18: no_effect, ADD-03:Q19: no_effect, ADD-03:AppA/para1: no_effect, ADD-03:AppA/para2: no_effect, ADD-03:AppB/para1: no_effect, ADD-03:AppB/para2: no_effect, ADD-03:T8-1/1: no_effect, ADD-03:T8-1/2: no_effect, ADD-03:T8-1/3: no_effect, ADD-03:T8-1/notes: no_effect, ADD-03:T8-1/note(1): no_effect, ADD-03:T8-1/note(2): no_effect, ADD-03:T8-1/note(3): no_effect, ADD-03:AppB/para3: no_effect, ADD-03:3.2: no_effect, ADD-03:2.3: no_effect, ADD-03:3.4: no_effect
- rows new: ADD-03-cover-01, ADD-03-3.1-01, ADD-03-2.3-01, ADD-03-2.4-01, ADD-03-2.5-01, ADD-03-3.4-01, ADD-03-AppA-01, ADD-03-AppA-03, ADD-03-AppA-04, ADD-03-AppA-05
- readings: VOL-I-12.2-01, VOL-I-12.2-02, VOL-I-8.9-01, VOL-V-44.2-01
- issues: I-ADD-03-1-3-CQ20-ANA, I-ADD-03-2-4-EXCEPTION-REACH, I-ADD-03-2-5-COVER-REJECTION, I-ADD-03-4-1-ISSUE-4-1-ANA, I-ADD-03-INVLIC-EVIDENCE-SCOPE, I-ADD-03-Q16-Q16-ISSUE-ANA, I-ADD-03-Q19-Q19-ISSUE-ANA, I-ADD-03-T8-1-2-2-ISSUE-ANA, I-ADD-03-T8-1-CLASS-COVERAGE, I-ADD03-8.9-CONDITIONAL, I-ADD03-COVER-2.5, I-ADD03-DESIGN-FLOW, I-ADD03-PCOD-3.3, I-AUTO-CLASS-SCOPE-ADD-03-T8-1, I-AUTO-CLASS-SCOPE-ADD-03-p3-image, I-INVREG-CONSEQUENCE, I-INVREG-VALIDITY
- analysis issues: I-ADD-03-1-3-CQ20-ANA, I-ADD-03-Q16-Q16-ISSUE-ANA, I-ADD-03-Q19-Q19-ISSUE-ANA, I-ADD-03-T8-1-2-2-ISSUE-ANA, I-ADD-03-4-1-ISSUE-4-1-ANA
- output time issues: I-AUTO-CLASS-SCOPE-ADD-03-T8-1, I-AUTO-CLASS-SCOPE-ADD-03-p3-image
- evidence items: EV-CIR-NOTIFICATION, EV-INVESTMENT-REG-CERT
- activities: cir-portal-notification, investment-registration-application
- lead times: cir_portal_notification, investment_registration_application
- relationships: REL-AI-001, REL-AI-002, REL-AI-003, REL-AI-004, REL-AI-005, REL-AI-006, REL-AI-007, REL-AI-008
- no change: act:investment-licence, impact:1. RECITALS, impact:4. AUTHORITY EVENT OF DEFAULT
  - raised at output time (the class-scope rule): HUMAN DECISION PENDING, written into the candidate register as PROPOSED
- applied through a new row (the provision's obligation is the row; PROPOSED): ADD-03:2.3 -> ADD-03-2.3-01; ADD-03:3.4 -> ADD-03-3.4-01
- unresolved provisions: 23

- left out of the promoted ops: ADD-03/2.1-row: an analysis row_reading is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `row:VOL-I-8.9-01` as an UNVE…; ADD-03/2.3-row: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/2.3-row` as an UNVERI…; ADD-03/2.4: not ready: promotion waits while depends on ADD-03/2.1 (amendment_op, conflicting); ADD-03/2.4-row: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/2.4-row` as an UNVERI…; ADD-03/2.5-row: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/2.5-row` as an UNVERI…; ADD-03/Q16-issue: not ready: promotion waits while depends on ADD-03/Q16 (escalation, escalated); ADD-03/row/ack-4A: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/cover/para3` as an UN…; ADD-03/issue/cq20: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-1-3-CQ20-ANA; HUMAN DECISION PENDING…; ADD-03/Q19-issue: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-Q19-Q19-ISSUE-ANA; HUMAN DECISION PE…; ADD-03/T8-1/2:issue: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-T8-1-2-2-ISSUE-ANA; HUMAN DECISION P…; ADD-03/T8-1/2:q: an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; th…; ADD-03/row-3.4: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/row-3.4` as an UNVERI…; ADD-03/row-4.6: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/3.1` as an UNVERIFIED…; ADD-03/issue-4.1: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-4-1-ISSUE-4-1-ANA; HUMAN DECISION PE…

## check-register on the candidate

- exit 1; 2 finding(s) {'C46': 1, 'pending_settled': 1}
- missing because the downstream phase did not propose them (the run's own new rows): 0
- defects: 2
  - [C46] ADD-03/cover/para3: [A3] ADD-03/cover/para3 brings in consequence words ['rejected'] that no row's consequence carries at ADD-03: 'SYNTHETIC: not tender content. Test material for blind rehearsal 08; not issued by any a…
  - [pending_settled] I-ADD-03-Q16-Q16-ISSUE-ANA: labelled HUMAN DECISION PENDING, yet its own words settle a limb of it ('therefore'): reword it as open (the proposed reading, 'not decided', and who decides) or record a person's decision

## Analysis rows carried to downstream tasks (and other analysis items not promoted)

- `ADD-03/row/ack-4A` row_new (ADD-03:cover/para3, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/cover/para3` as an UNVERIFIED reference — applied as the new row(s) ADD-03-cover-01 (proposed downstream: ADD-03-cover-01 (row_new, interpretation_pending), DS-06 (issue, interpretation_pending); task(s) c46:ADD-03/cover/para3; PROPOSED, not approved): the provision's obligation is that row; a person confirms it
- `ADD-03/issue/cq20` issue (ADD-03:1.3, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-1-3-CQ20-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task — clarification route: bid decision (window closed 2026-11-12) (its suggestion of a clarification is a bid decision now)
- `ADD-03/2.1-row` row_reading (ADD-03:2.1, interpretation_pending): an analysis row_reading is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `row:VOL-I-8.9-01` as an UNVERIFIED reference — its obligation is proposed downstream as VOL-I-8.9-01 (row_reading, interpretation_pending) (task(s) row:VOL-I-8.9-01; PROPOSED): no op or disposition answers the provision; a person confirms the row and the provision's disposition
- `ADD-03/2.3-row` row_new (ADD-03:2.3, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/2.3-row` as an UNVERIFIED reference — applied as the new row(s) ADD-03-2.3-01 (proposed downstream: ADD-03-2.3-01 (row_new, interpretation_pending); task(s) ana:ADD-03/2.3-row; PROPOSED, not approved): the provision's obligation is that row; a person confirms it
- `ADD-03/2.4-row` row_new (ADD-03:2.4, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/2.4-row` as an UNVERIFIED reference — applied as the new row(s) ADD-03-2.4-01 (proposed downstream: ADD-03-2.4-01 (row_new, interpretation_pending); task(s) ana:ADD-03/2.4-row; PROPOSED, not approved): the provision's obligation is that row; a person confirms it
- `ADD-03/2.5-row` row_new (ADD-03:2.5, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/2.5-row` as an UNVERIFIED reference — applied as the new row(s) ADD-03-2.5-01 (proposed downstream: ADD-03-2.5-01 (row_new, interpretation_pending), DS-13 (evidence_item, evidence_verified), DS-14 (activity, interpretation_pending); task(s) ana:ADD-03/2.5-row; PROPOSED, not approved): the provision's obligation is that row; a person co…
- `ADD-03/Q16-issue` issue (ADD-03:Q16, interpretation_pending): not ready: promotion waits while depends on ADD-03/Q16 (escalation, escalated)
- `ADD-03/Q19-issue` issue (ADD-03:Q19, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-Q19-Q19-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ADD-03/T8-1/2:issue` issue (ADD-03:T8-1/2, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-T8-1-2-2-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ADD-03/T8-1/2:q` clarification (ADD-03:T8-1/2, interpretation_pending): an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; the downstream phase proposes issues and clarification entries against the candidate
- `ADD-03/row-3.4` row_new (ADD-03:3.4, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/row-3.4` as an UNVERIFIED reference — applied as the new row(s) ADD-03-3.4-01 (proposed downstream: ADD-03-3.4-01 (row_new, interpretation_pending), DS-16 (issue, interpretation_pending); task(s) ana:ADD-03/row-3.4; PROPOSED, not approved): the provision's obligation is that row; a person confirms it
- `ADD-03/row-4.6` row_new (ADD-03:3.1, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/3.1` as an UNVERIFIED reference — applied as the new row(s) ADD-03-3.1-01 (proposed downstream: ADD-03-3.1-01 (row_new, interpretation_pending), DS-08 (issue, interpretation_pending), DS-09 (dependency, interpretation_pending); task(s) c46:ADD-03/3.1; PROPOSED, not approved): the provision's obligation is that row; a person confirm…
- `ADD-03/issue-4.1` issue (ADD-03:4.1, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-4-1-ISSUE-4-1-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task — clarification route: bid decision (window closed 2026-11-12) (its suggestion of a clarification is a bid decision now)

## Coverage

- provisions: 52; accounted for by the combined set: 49; states {'validated': 52}
- accounted for through downstream tasks (analysis rows carried; never a silent gap): 2 ADD-03:2.3 → ana:ADD-03/2.3-row; ADD-03:3.4 → ana:ADD-03/row-3.4
- the analysis ITEMS' resolution by the controller (items, not provisions; session 14): resolved 18, pending 31, invalid 0, unaccounted 3; approved 0
- structural units of ADD-03 that are not provisions (listed so nothing is dropped): ADD-03:H:cover (heading), ADD-03:H:cover-2 (heading), ADD-03:H:S1 (heading), ADD-03:H:S2 (heading), ADD-03:H:S3 (heading), ADD-03:H:S4 (heading), ADD-03:H:S5 (heading), ADD-03:S5/QA (table), ADD-03:H:AppA (heading), ADD-03:region:ADD-03-p3-r1 (region), ADD-03:p3-image (table), ADD-03:H:AppB (heading), ADD-03:T8-1 (table)
- batches: reading-ADD-03-p3-r1 done, analysis-001 done, analysis-002 done, analysis-003 done, analysis-004 done, analysis-005 done, analysis-006 done, downstream-001 done, downstream-002 done, downstream-003 done

## Critic (a second model over the selected items; it changed no status)

**Agreement between the critic and the proposer is not approval**: every item still needs a person's decision, and a disagreement is a concern for that person, not a rejection. The critic reviews only the selected classes (consequential interpretations, uncertain targets, removals, conflicting evidence), in one request per batch.

| Batch | Critic | Selected | Reviewed | Agrees | Does not agree | Note |
|---|---|---|---|---|---|---|
| analysis-001 | done | 4 | 4 | 3 | 1 |  |
| analysis-002 | done | 8 | 8 | 7 | 1 |  |
| analysis-003 | done | 3 | 3 | 2 | 1 |  |
| analysis-004 | done | 1 | 1 | 0 | 1 |  |
| analysis-005 | done | 3 | 3 | 1 | 2 |  |
| analysis-006 | done | 2 | 2 | 2 | 0 |  |
| downstream-001 | done | 3 | 3 | 1 | 2 |  |
| downstream-002 | done | 2 | 2 | 0 | 2 |  |
| downstream-003 | done | 3 | 3 | 1 | 2 |  |

- **ADD-03/cover/para3** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The quoted obligation 'Bidders shall acknowledge receipt in Form 4-A.' is verbatim in ADD-03:cover/para3, and recording it as an interpretation pending a person is consistent with 'the cover summarises; it does not amend'. Annotating the cover's own procedural sentence is still a reading of a cover…
    - concern: S-I2 relies on how 'the same words in the cover texts of Addenda Nos. 1 and 2' were treated, but it carries no evidence and those units are not printed here. I cannot verify the precedent.
    - concern: The rationale says the cover's summaries (8.9, Table 8-1, Vol II 4.6, Vol V 12.1 and 39.4, and 'failing which the Proposal will be rejected') are covered by operative provisions in other batches. None of those provisions is printed here. Each cover summary still has to be compared with its operativ…
    - concern: The dependency VOL-IV:F4-A is not printed, so I cannot check that it is the right unit for Form 4-A as it stands at ADD-02.
- **ADD-03/row/ack-4A** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The row's requirement text 'Bidders shall acknowledge receipt of Addendum No. 3 in Form 4-A.' is not verbatim. The words 'of Addendum No. 3' are not in the cover. A1 needs the obligation quoted verbatim ('Bidders shall acknowledge receipt in Form 4-A.'), with any gloss kept separate and labelled.
    - concern: The scope 'Envelope A' is not supported by any evidence shown. No quoted unit puts Form 4-A in Envelope A, so this may be an unsupported placement.
    - concern: The rationale cites ADD-01:AppA/para1 and VOL-I:9.3, but neither is printed or attached as evidence. The row's own evidence list is empty.
    - concern: The proposer decided that VOL-I:9.3's non-responsiveness ('signing or execution of Form 4-A') does not apply to a failure to acknowledge Addendum No. 3 in Form 4-A. Whether that printed consequence reaches the acknowledgement at paragraph 1 of the reissued Form 4-A is a reading for a person (Legal …
    - concern: Same as the annotate item: it depends on S-I2's unevidenced precedent from Addenda 1 and 2.
- **ADD-03/issue/cq20** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The difference is real: the cover says 'and responds to clarification requests 15 to 20', while ADD-03:1.3 and the Section 5 heading say 15 to 19. Raising it as an issue with both quotations, leaving it unresolved, follows the rule on cover/operative differences.
    - concern: Clause 1.3 only says requests 15 to 19 'were received before the time stated in Volume I Clause 5.2'. It does not itself say they are answered; the 'responses' wording comes from the Section 5 heading. The issue text should not imply that 1.3 states the answered set.
    - concern: Reading 3 (a response intended but omitted) is really a missing-evidence possibility, not an ambiguity in the words. A person may want that point raised separately with Document control as possible missing content, so the two classes are not merged under 'ambiguous:'.
    - concern: The 'no response to request 20 found' claim rests on a search that is not printed. The ADD-03:H:S5 and VOL-I:5.2 quotations are confirmed only by the controller's verbatim checks, because those units are not in the units shown.
    - concern: The controller's human-owned flag on 'answered' comes from quoted text and readings ('will not be answered', 'not answered'). The issue does not declare any question answered.
- **ADD-03/disp/1.2** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The provision contains an exception, 'unless otherwise stated'. The controller's semantic check reports that no exception words remain, which looks wrong for these words. Under the shared rules, a no_effect on a provision with exception wording is a person's decision. The item does leave it for a p…
    - concern: Calling this 'no_effect' understates it. Clause 1.2 decides which version every reference in ADD-03 points to (for example Form 4-A as reissued by ADD-01, and Table 8-1). A person may prefer to record it as a reading rule that the other batches depend on, rather than as having no effect.
    - concern: S-I1 has no evidence attached apart from the provision itself. That is acceptable for a reading of this one clause.
- **ADD-03/2.1** (analysis-002; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: old words located in the target; model claude-opus-5-5
    - concern: Q15 ('an undertaking is no longer accepted') is used to support the removal of the undertaking option, but Q15's text is not printed in this request, so I could not check it. The substitution does not need it: the words 'is deleted and replaced by the following' are enough.
    - concern: The controller's 'conflicting' flag treats ADD-03/2.4 as changing VOL-I:8.9 'in different ways'. As printed, 2.4 does not rewrite the text of 8.9. It disapplies Section 2.1 for one class of member. That makes it an exception to scope, not a competing text change. A person should decide whether the …
    - concern: The rationale says the undertaking is 'now kept only for the Section 2.4 class'. That depends on interpretation S-I2, which is pending. It should be labelled as an interpretation, not stated as the effect of the op.
    - concern: I checked the replace_text old and new values against the quotations, and they are correct. Leaving out the printed number '8.9' in the new text is disclosed.
- **ADD-03/2.1-row** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The rejection consequence is quoted correctly from the new 8.9. It applies to 'each such member', meaning a member incorporated outside the Kingdom. Whether it also covers the 2.4 class's undertaking is still open (see ADD-03/2.4-row). The note should not suggest that the class split is settled.
    - concern: The row's current requirement text was not read. The proposer says so. The row stays incomplete until a person revises it, including any date rule tied to Financial Close.
- **ADD-03/2.2** (analysis-002; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Treating ADD-03:p3-image as Table 8-1 follows from 'reproduced at Appendix A ... and forms part of Volume I'. However, the image reading is pending. The detail described from the crop (three rows ٣/٥/٨, three notes, the Office letter ref and date, an empty stamp circle) is not in the units shown, a…
    - concern: The precedence 'over' ADD-03:T8-1 assumes T8-1 is the Appendix B translation. T8-1 is not printed in the units, so I could not confirm this. Applying 'The Arabic text governs.' still needs a person to confirm it.
    - concern: The stamp circle is described as empty, but nothing is raised about it. A person may want to note whether the table is authenticated as 'issued by the Office'. I make no finding on this.
- **ADD-03/2.2-issue** (analysis-002; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Row 2 showing ٥ is confirmed by ADD-03:p3-image/r2 cell 'مدة الإصدار (أيام عمل)': '٥'. The English figure 3 is verified only by the controller record. T8-1/2 is not printed in the units.
    - concern: The Q16 quotation in S-F6 (reduction of two Working Days for applications lodged by 22 November 2026) is not among the units printed, and the controller records no check of it. I could not verify it.
    - concern: The issue rightly leaves open which figure applies, even though 2.2 states that the Arabic governs. Applying a printed precedence rule is still a person's call, and the Arabic reading itself is pending.
    - concern: The claim that rows 1 and 3 agree with the translation cannot be checked here.
- **ADD-03/2.3-row** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The date note says the period is 'counted from receipt of a complete application (Table 8-1 Note 1)'. That paraphrases a note that is not printed here, and it differs from the 2.2 rationale ('counting starts the Working Day after receipt of a complete application'). The note should be quoted verbat…
    - concern: The row's dependencies leave out ADD-03/2.2-issue, even though the note relies on the row 2 discrepancy.
    - concern: Recording 'none_stated' for the consequence is right: 2.3 prints none. Treating the Office's undertaking as a lead time rather than a bidder deadline is a fair reading of the words.
- **ADD-03/2.4-row** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The rationale says the undertaking's content is quoted from VOL-I:8.9 'as issued' (text_as_issued). The only text printed, and the only one the controller checked, is VOL-I:8.9's effective text at ADD-02 ('verbatim in VOL-I:8.9 at ADD-02'). Section 2.4 refers to Clause 8.9 'as issued'. Nothing show…
    - concern: 'assessment': 'pass_fail' is given even though the row records consequence 'none_stated' and leaves open whether the rejection words of the new 8.9 reach this class. 'pass_fail' suggests an assessed outcome that the evidence does not establish.
    - concern: ADD-03/2.4 (the op) and ADD-03/2.4-issue are referred to but not printed in this batch, so I could not check them.
    - concern: The scope paraphrases 'is to hold' as 'holding'. The reading of 'Section 2.1 does not apply' (S-I2) is rightly left pending.
- **ADD-03/2.5-row** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The rationale says Q16's 22 November lodging date 'falls one Working Day before' the 23 November deadline. That count was not produced by calculate, and the Q16 text is not printed here. The figure should come from calculate, or be removed.
    - concern: The PDD value (2026-11-26) and the calculate result appear only in the note. I cannot check them against the units shown.
    - concern: 'issues': [] is empty, even though the interpretation note points to ADD-03/2.5-issue. The row should link that issue. With the cover and the operative text in disagreement, confidence 'high' may overstate how settled the consequence is.
    - concern: Recording 'none_stated' for the consequence matches the operative words of 2.5.
- **ADD-03/2.5-issue** (analysis-002; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The cover quotation ('failing which the Proposal will be rejected') is verified only by the controller record. ADD-03:cover/para3 is not printed in the units.
    - concern: The item handles the conflict correctly: it reports both quotations, does not resolve which governs, and names Legal as the owner.
- **ADD-03/Q15** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: Q15 does more than restate. 'which shall give its own undertaking' adds that the Section 2.4 member must give the undertaking itself. The 2.4 words shown ('Such a member shall instead submit with Envelope A the signed undertaking described in Volume I Clause 8.9 as issued') do not say who signs. Th…
    - concern: The annotation is placed on VOL-I:8.9. Section 2.1 of this same addendum deletes that clause ('Volume I Clause 8.9 is deleted and replaced by the following:'). The interpretation is really about who gives the 2.4 undertaking. An annotation on a deleted unit may not carry forward to the effective te…
    - concern: Q15's opening 'No.' answers the bidder's question about the lead member giving the undertaking on a foreign member's behalf. The note covers this, but it is paraphrase; the verbatim words are in the evidence and match the unit.
- **ADD-03/Q16** (analysis-003; controller status **escalated**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The 'software limitation:' reason assumes Q16 amends the row 2 value (Reading A of S-Q16-I1). Whether it amends anything at all is itself the open ambiguity (Reading B: it only reports 'The Office has confirmed to the Authority that...'). The escalation should say it applies only if a person adopts…
    - concern: The 'why' text bundles an ambiguity (Arabic ٥ vs English 3) into a software-limitation reason. It points to a separate issue, which is acceptable, but under the one-point, one-class rule it should stay out of this escalation's reason.
    - concern: Two parts of Q16 are not accounted for in this item's evidence: the response's first sentence ('Section 2 of this Addendum applies.') and the bidder question.
    - concern: The target relies on an image reading that is still pending (ADD-03:p3-image). The rationale's statement that rows ١ and ٣ show ٣ and ٨ cannot be checked from the evidence printed here. The row 2 reading ('م: ٢', issue-period cell '٥') matches the unit text shown.
    - concern: The rationale says calculate confirmed 2026-11-22 is a Sunday and a Working Day. The calculate output is not in the evidence shown, so this could not be checked.
- **ADD-03/Q16-issue** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Point (1) is labelled 'ambiguous:', but the words do not support two readings. The Arabic ٥ and the English 3 are a discrepancy between the original and its translation. Section 2.2 prints a precedence rule for it ('The Arabic text governs. The English translation at Appendix B is provided for conv…
    - concern: Point (2), whether Q16 amends Table 8-1 or only reports the Office's confirmation, is a genuine ambiguity. It should be a separate issue rather than merged with point (1) under one open question.
    - concern: The issue's Q16 quotation leaves out 'The Office has confirmed to the Authority that,' and 'The other issue periods in Table 8-1 are unchanged.'. Those words are what support Reading B and limit the scope, so the person deciding should see them in the issue's own evidence.
    - concern: The owner is Document control only. The rationale itself says Legal is needed on which text governs, and deciding which clause prevails is a Legal matter, so Legal should be named as owner for the precedence point.
- **ADD-03/AppA/para1** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: ambiguous: the paragraph may not simply restate Section 2.2; it may reach further. The only quotation of ADD-03:2.2 shown (S-2.2) limits the Arabic-precedence rule to Table 8-1: "Table 8-1 is issued in the Arabic language. The Arabic text governs." AppA/para1 introduces both items, "The following l…
    - concern: "The Arabic text governs" is precedence wording, so it says which text prevails. Shared policy makes which text governs or prevails a person's decision, and a no_effect is a person's call where the words print or except something. So the controller's semantic check, which found "no amendment, oblig…
    - concern: The paragraph does not say whether the reproduced letter is incorporated into the tender documents or is information only. The item does not identify this as an open point. It only says that Table 8-1's incorporation is dealt with elsewhere. The letter's own status is not dealt with in this item.
    - concern: Only fragments of the full text of ADD-03:2.2 are shown in this request: "The Arabic text governs." and "Table 8-1 is issued in the Arabic language. The Arabic text governs." So I could not check whether 2.2 covers the letter as well. The controller records the 2.2 quotation as "verbatim in ADD-03:…
    - concern: Change propagation: the item names no follow-on work. If the letter's Arabic text governs, then any requirement, date or reference taken from the letter, and any translation of it used in A1 or A5, depends on this paragraph. These are not listed.
    - concern: Interpretation S-AppA-I1 has no evidence of its own. It is the basis for the whole disposition, and it is correctly left pending for a person.
- **ADD-03/T8-1/2:disp** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
    - concern: The no_effect reason goes beyond recording that the translation amends nothing. It says 'the 3 must not be used as the row 2 period'. That applies ADD-03:2.2 to settle the discrepancy, but which figure governs is a person's decision. It also contradicts the companion issue ADD-03/T8-1/2:issue, whic…
    - concern: It calls ADD-03:p3-image/r2 the 'governing Arabic row', but the rationale and S-F3 both say the reading of that row is still pending approval. A disposition that settles the effect of the translation should not rest on an unapproved reading as if it were confirmed.
    - concern: The heading 'Documents required with the application' carries 'required', so the controller rightly flags no_effect on wording that obliges. The proposer's line 'A person confirms' is fine, but the item is marked ready:true while it depends on a pending reading and an open issue.
    - concern: The follow-on work names 'Clause 2.3's undertaking' and other dependents. ADD-03:2.3 is not among the evidence shown, so I cannot check those links.
    - concern: Not a defect: the documents cell matches the Arabic cell ('السجل التجاري والقوائم المالية المدققة لآخر سنة مالية، مصدقة'). The only difference shown is the issue period, 3 against ٥.
- **ADD-03/T8-1/2:issue** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Reading (b) assumes the translation's 3 is the 5 after Q16's two-day reduction. That rests on unstated arithmetic and nothing printed supports it. It is a plausible alternative, but the issue should say that reading (b) is an inference from the figures, not something the pack says.
    - concern: The decision owner here is Legal, but the linked clarification ADD-03/T8-1/2:q names Bid management. The owners should be made consistent, or the split explained.
    - concern: The target is ADD-03:p3-image/r2, which the provision does not cite (the controller flags uncertain_target). The issue really concerns both units. The person deciding should know the target was chosen by the proposer.
    - concern: The dependency ADD-03:2.3 is listed, but no evidence for it is shown, so I cannot check it.
    - concern: The Arabic reading of ٥ is still pending approval. The issue says so, which is correct, but the open question also depends on that reading being approved.
- **ADD-03/T8-1/2:q** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The draft question is leading. It asks the issuer to 'confirm that the Arabic figure of five (5) Working Days governs' and that the reduction applies to that figure. That builds in reading (a) and leaves out reading (b) from S-I1. A neutral draft would ask which row 2 issue period applies and how t…
    - concern: interim_handling ('Plan on the governing Arabic figure without the conditional reduction... Do not use the translation's 3') chooses a reading and sets a planning basis. If the proposer wants an interim basis, it must be a separate statement labelled 'PROVISIONAL ASSUMPTION:' with its basis. As wri…
    - concern: practical_impact cites Clause 2.1 ('shall be rejected') and a 'Certificate of Investment Registration'. Neither Clause 2.1 nor any unit naming that certificate is in the item's evidence or in the units shown. A rejection consequence must be quoted from the unit that states it, and here it cannot be…
    - concern: The decision owner is Bid management, but the linked issue names Legal. The owners are inconsistent.
    - concern: The Arabic ٥ comes from a reading that is still pending approval. Sending a question that states it as fact before the reading is approved should be flagged.
- **ADD-03/3.1** (analysis-006; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-opus-5-5
    - concern: The anchor is correct. ADD-03:3.1 says 'inserted in Volume II after Clause 4.5', so VOL-II:4.5 is the right anchor and 'number' 4.6 matches the provision. new_text matches the quoted text word for word; only the printed number '4.6' at the start is left out, which is right because it is carried in …
    - concern: The item's evidence quotes only the instruction ('The following new Clause 4.6 is inserted in Volume II after Clause 4.5'). It does not quote the inserted clause text, which appears only in the payload. Adding a span for the inserted text would make A2 complete.
    - concern: The rationale says no Volume II Clause 4.6 exists at ADD-02. The search result behind that is not shown in this request, so I could not check it.
    - concern: The rationale also mentions ADD-03:Q18, 'Clause 2.1 / Table 2-6' and an A1 row 'ADD-03/row-4.6'. None of these is shown here, so I could not check them. It correctly leaves the 'six (6) hours of the design flow' volume uncomputed.
- **ADD-03/row-3.4** (analysis-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The requirement and the interpretation quote are word for word from ADD-03:3.4. 'consequence: none_stated' is correct, because ADD-03:3.4 prints no consequence.
    - concern: dependencies lists only ADD-03:3.4. The provision explicitly cites 'Sections 3.1 and 3.3', so the dependencies should also include ADD-03:3.1, ADD-03:3.3 and the new Volume II Clause 4.6 created by ADD-03/3.1. Without them the propagation is incomplete.
    - concern: The text of ADD-03:3.3 is not printed in this request, so I could not check what this row requires for Section 3.3. The row rightly treats that part as pending the escalated ADD-03/3.3.
    - concern: discipline is 'Technical' only, but the provision also requires reflection 'in the Financial Model', which is commercial. The decision owner may need to include Commercial.
    - concern: assessment 'procedural' is a proposed class. The obligation affects what goes into the process design, not only how the bid is submitted. A person should confirm this class.
    - concern: The words 'in the process design and the construction programme submitted in the Technical Proposal and in the Financial Model' could mean both items go in both documents, or each item goes in its own document. The row quotes the words without choosing a reading, which is correct; this may be worth…
- **DS-02** (downstream-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The consequence is tied to 'the long-stop date', not to the 270-day period. The row's quote and date rule (270 days after the Preferred Bidder Notification) do not show that the two are the same date. The note correctly leaves I-VOL-I-BOND-LONGSTOP open. The row must not be read as linking the Bid …
    - concern: The class 'contractual' for 'entitles the Authority to call the Bid Bond and to proceed with the next ranked Bidder' is a reading. Whether this also counts as an A3 bid-out consequence (exclusion in favour of the next ranked Bidder) is a person's call. The item should not settle it by its choice of…
    - concern: The stage is given as ADD-03, but the obligation has been in force since BASE. ADD-03:2.6 only confirms that the periods are unchanged. The register should make clear that ADD-03 is not the stage where the obligation came into force.
- **DS-06** (downstream-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: insufficient evidence: the full text of ADD-03:2.5 is not printed under units. Only one span is shown, and the controller check confirms only that this span is verbatim. The evidence shown does not prove the key claim that 'Operative Section 2.5 prints the notification obligation with no consequenc…
    - concern: The issue says 'The clarification window has closed (VOL-I 5.2)', but VOL-I:5.2 is not quoted and cannot be checked here.
    - concern: The framing itself (cover vs operative difference, both quoted, the cover not treated as amending, a human decision pending, owner Legal) is consistent with policy. If the full 2.5 is confirmed to state no consequence, the item would follow from it.
- **DS-18** (downstream-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The item says ADD-03/2.1 'conflicts' with ADD-03/2.4, but on the words shown 2.4 is an express carve-out from 2.1: 'Section 2.1 does not apply to a member ...'. This is not a contradiction. The real difficulties are different: (i) 2.4 refers to 'Volume I Clause 8.9 as issued', which 2.1 deletes; (i…
    - concern: The item says the effective VOL-I 8.9 'states no consequence'. Only one span of VOL-I:8.9 is shown, so this cannot be checked from the evidence printed.
    - concern: The item cites 'The clarification window has closed (VOL-I 5.2)', but VOL-I:5.2 is not quoted here.
    - concern: Holding 2.1 unapplied leaves a printed deletion-and-replacement, with a stated rejection, out of the effective text. This needs a prominent A2/A3 flag. The item's a3 line does this, and its list of dependent rows, activity and Table 8-1 lead times is appropriate.
    - concern: The quotations of 2.1, 2.4 and Q15 are accurate against the text shown.
- **D-20** (downstream-002; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
    - concern: The issue-period values the item states ('row ١ ٣, row ٢ ٥, row ٣ ٨') are not quoted anywhere in the evidence shown. The printed unit ADD-03:p3-image gives only the table heading and intro sentence ('cells': null). Rows ١ and ٣ have no quotation at all. Row ٢ '٥' rests only on statement downstream-…
    - concern: The conflict between Arabic row ٢ and English row 2 ('3') cannot be confirmed from what is shown. The 'Issue period (Working Days): 3' cell of ADD-03:T8-1/2 is verified. The Arabic '٥' is a one-character reading quote that the controller rejects elsewhere as 'too short to be evidence' (D-23), and t…
    - concern: The crop details the item relies on are not in the evidence list: the date 'التاريخ: ١٦ نوفمبر ٢٠٢٦م', the reference 'الرقم: ٢٢٨/٢٠٢٦', the empty stamp oval at ADD-03:p3-image/stamp, and the signature mark with no name. Only the signatory title and the main region's crop hash are evidenced. The rat…
    - concern: The item says the values 'would feed ... the Section 2.5 notification', but no unit or quotation for Section 2.5 is shown.
    - concern: The controller's consistency check says the item 'reverses ADD-03/disp/1.2'. The item text does not address ADD-03 1.2 or explain the handback, so the clash is left unexplained.
    - concern: Correct as far as shown: Notes ١–٣ in (b)–(d) match the quoted readings of note1, note2 and note3. The item is kept conditional and pending. Acceptance of the unstamped letter is correctly left to a person, as a question for Document control and Legal.
- **D-23** (downstream-002; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
    - concern: One end of the dependency is ADD-03:p3-image/r2 '٥'. That unit is not among the printed units, and the controller rejects its quotation as 'too short to be evidence'. The supporting statement downstream-002/ST-F5 is marked 'not supported verbatim'. The Arabic side of the dependency is therefore not…
    - concern: The basis is 'CONDITIONAL on analysis issue ADD-03/T8-1/2:issue', yet the payload's 'issues' list is empty. The condition is not linked.
    - concern: The controller says this item 'reverses ADD-03/2.2-issue', which applied 'The Arabic text governs.' The item quotes 2.2 but then leaves the choice of value to a person without saying how this squares with the rule already applied. Leaving the choice to a person is right while the reading is pending…
    - concern: ST-F4 says Section 2.2 states that 'Table 8-1 is issued in Arabic'. The quoted words ('The Arabic text governs. The English translation at Appendix B is provided for convenience only.') do not say that in terms; the statement goes further than its quote.
    - concern: Correct as far as shown: the English cell '3' is verified at ADD-03:T8-1/2. The relationship stays 'possible'. The lead-time key investment_licence is labelled a PROVISIONAL ASSUMPTION. The program does not pick a value.
- **D-ROW-02** (downstream-003; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
    - concern: The 'requirement' field is the proposer's own English rendering of the Arabic row, not a verbatim quotation. A1 needs the obligation quoted verbatim, and a translation is never evidence for the source. It also adds wording that is not in the quoted cells: the Arabic gives a member class and 'المستن…
    - concern: The row cites ADD-03:p3-image/note1 and ADD-03:p3-image/note3, and the date_note says the period is 'counted under note 1 from an event'. Neither note's text is in the evidence or the statements, so this cannot be checked against the request.
    - concern: consequence 'none_stated' rests on downstream-003/S-REJECT-2-1, which is an interpretation. ADD-03:2.1 prints 'A Proposal that does not include the evidence required by this Clause for each such member shall be rejected.' Linking that rejection to issue I-INVREG-CONSEQUENCE is right. However, the r…
    - concern: The rationale says the crop 'plainly shows ٥' and that the reading does not mark the numeral as uncertain, yet confidence is 'low'. The reason given (the conflict with Appendix B and Q16) is fair. Recording the figure from the image while holding the row as PENDING READING is consistent with the ru…
- **D-ISS-01** (downstream-003; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-opus-5-5
    - concern: The controller reports a phase-consistency failure: this item reverses ADD-03/2.2-issue, which applied 'The Arabic text governs.' Handing the point to a person is allowed, because which clause governs and what it settles is a person's decision. Even so, the issue should name ADD-03/2.2-issue explic…
    - concern: Reading (b), that Appendix B already shows the reduced period, implies arithmetic between ٥ and 3. That arithmetic must not be relied on without `calculate`. The issue correctly states no computed figure.
    - concern: The Q16 quotation here includes the lodging-date condition, but the quotation in S-Q16 does not. Both are reported as verbatim. The full Q16 unit text is not printed in the request, so the complete wording could not be checked here.
- **D-CQ-01** (downstream-003; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-opus-5-5
    - concern: practical_impact refers to 'the latest date to lodge a row-2 member's application, before Envelope A'. Nothing in the evidence shown links Table 8-1 or the Office application to Envelope A or to any submission deadline. Without a quotation this link may be invented.
    - concern: The Q16 entry in 'sources' leaves out the lodging-date condition ('for an application lodged not later than Sunday 22 November 2026'), but the proposed question depends on that condition. That clause should be quoted in sources.
    - concern: The question is neutral, already_settled correctly leaves to a person whether 'The Arabic text governs' settles the point, interim_handling chooses neither figure, and the status is 'draft, not sent'. All of these are sound.
    - concern: Same phase-consistency flag as D-ISS-01: the item should name ADD-03/2.2-issue so a person can reconcile the two.

## Requests: failures, deferrals, repairs and route notices

- every request was answered at the first call, parsed, and fitted its context

Route notices (how the requests were served; they change no status):
- **capabilities_declared** (reading-ADD-03-p3-r1): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the reading request wa…
- **capabilities_declared** (analysis-001): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request w…
- **capabilities_declared** (analysis-003): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request w…
- **capabilities_declared** (analysis-004): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request w…
- **capabilities_declared** (analysis-005): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request w…
- **capabilities_declared** (analysis-006): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request w…
- **capabilities_declared** (downstream-001): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request…
- **capabilities_declared** (downstream-002): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request…
- **capabilities_declared** (downstream-003): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request…

## Manual interventions (the person's actions)

- 2026-10-08T05:47:55Z: stop (the person's action) by a person (a signal from outside the run: the panel's Stop, Ctrl-C or a kill); SIGTERM during step analysis; 2 host session process(es) stopped
- 2026-10-08T05:48:01Z: resume (the person's action) by a person (tenderpack ai resume, or the panel's Resume); process 6988; status before: stopped

### What the run did with them, and its automatic host sessions (not a person)

- 2026-10-08T05:40:14Z: host session (automatic) — batch reading-ADD-03-p3-r1 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session reading an image; not a person
- 2026-10-08T05:45:14Z: host session (automatic) — batch analysis-001 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session over the MCP tools; not a person
- 2026-10-08T05:47:55Z: host session stopped by the person's stop — batch analysis-002 by tenderpack.ai.workflow (automatic); its exchange was cut before its answer was taken; on resume its staged submission is reused if it made one, else it is asked again
- 2026-10-08T05:47:55Z: host session stopped by the person's stop — batch analysis-003 by tenderpack.ai.workflow (automatic); its exchange was cut before its answer was taken; on resume its staged submission is reused if it made one, else it is asked again
- 2026-10-08T05:48:10Z: submission reused (automatic) — batch analysis-002 by tenderpack.ai.workflow; the host session's staged set ADD-03-host-20261008T054750Z-c3d5 (made in this drive) was revalidated and taken instead of asking the batch again
- 2026-10-08T05:54:43Z: host session (automatic) — batch analysis-003 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session over the MCP tools; not a person
- 2026-10-08T06:02:23Z: host session (automatic) — batch analysis-004 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session over the MCP tools; not a person
- 2026-10-08T06:03:05Z: host session (automatic) — batch analysis-005 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session over the MCP tools; not a person
- 2026-10-08T06:07:31Z: host session (automatic) — batch analysis-006 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session over the MCP tools; not a person
- 2026-10-08T06:14:51Z: host session (automatic) — batch downstream-001 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session; not a person
- 2026-10-08T06:16:12Z: host session (automatic) — batch downstream-002 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session; not a person
- 2026-10-08T06:19:50Z: host session (automatic) — batch downstream-003 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session; not a person

## The diff (ADD-02 → ADD-03; [diff.md](diff.md))

## What changed from ADD-02 to ADD-03

### ADD-03: PARTIAL (issued 2026-11-18)

- ops: 7 (0 invalid); provisions: 52 (23 unresolved)
- validated state: ADD-02 — this addendum does NOT replace it until every provision is treated and every op is valid
- UNRESOLVED ADD-03:2.1: Volume I Clause 8.9 is deleted and replaced by the following: ‘8.9  Each member of the Bidder that is incorporated outside the Kingdom shall submit with Envelop
- UNRESOLVED ADD-03:2.2: Table 8-1 is reproduced at Appendix A to this Addendum as issued by the Office and forms part of Volume I. Table 8-1 is issued in the Arabic language. The Arabi
- UNRESOLVED ADD-03:2.4: Section 2.1 does not apply to a member of the Bidder that is to hold not more than ten per cent (10%) of the shares in the Project Company and that has no role 
- UNRESOLVED ADD-03:2.5: A Bidder that relies on paragraph (b) of Volume I Clause 8.9 for any member shall notify the Authority through the Portal, not later than three (3) Working Days
- UNRESOLVED ADD-03:3.3: In Volume V Clause 12.1, the period of thirty-six (36) months is increased by six (6) months.
- UNRESOLVED ADD-03:Q16: No: 16 | Bidder question: Will the Authority assist foreign consortium members that have not obtained an investment licence before the Proposal Due Date? | Auth
- UNRESOLVED ADD-03:p3-image/r1: م: ١ | فئة العضو: شركة مؤسسة في إحدى دول مجلس التعاون الخليجي | المستندات المطلوبة مع الطلب: السجل التجاري مصدقاً | مدة الإصدار (أيام عمل): ٣
- UNRESOLVED ADD-03:p3-image/r2: م: ٢ | فئة العضو: شركة مؤسسة خارج دول مجلس التعاون الخليجي | المستندات المطلوبة مع الطلب: السجل التجاري والقوائم المالية المدققة لآخر سنة مالية، مصدقة | مدة الإ
- UNRESOLVED ADD-03:p3-image/r3: م: ٣ | فئة العضو: فرع مسجل في المملكة لشركة أجنبية | المستندات المطلوبة مع الطلب: شهادة تسجيل الفرع وقرار مجلس إدارة الشركة الأم بتفويض الفرع | مدة الإصدار (أيا
- UNRESOLVED ADD-03:p3-image/hdr-en: Northern Region Investment Services Office
- UNRESOLVED ADD-03:p3-image/hdr-ar: مكتب خدمات الاستثمار بالمنطقة الشمالية
- UNRESOLVED ADD-03:p3-image/date: التاريخ: ١٦ نوفمبر ٢٠٢٦م
- UNRESOLVED ADD-03:p3-image/ref: الرقم: ٢٢٨/٢٠٢٦
- UNRESOLVED ADD-03:p3-image/to: إلى: الهيئة الشمالية للمشتريات المرفقية
- UNRESOLVED ADD-03:p3-image/subject: الموضوع: تسجيل استثمار أعضاء الائتلافات المؤسسين خارج المملكة
- UNRESOLVED ADD-03:p3-image/tender: مناقصة رقم: NUPA/ISTP/2026/014 (محطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان)
- UNRESOLVED ADD-03:p3-image/notes-heading: ملاحظات:
- UNRESOLVED ADD-03:p3-image/note1: ١. تُحسب مدة الإصدار بأيام العمل اعتباراً من يوم العمل التالي ليوم استلام الطلب المكتمل.
- UNRESOLVED ADD-03:p3-image/note2: ٢. تكون الشهادة سارية لمدة تسعين (٩٠) يوماً من تاريخ إصدارها.
- UNRESOLVED ADD-03:p3-image/note3: ٣. تُقدِّم الطلبات إلكترونياً عبر بوابة المكتب فقط، ولا يُعدّ الطلب مكتملاً إلا بإرفاق جميع المستندات المبيِّنة أعلاه.
- UNRESOLVED ADD-03:p3-image/stamp: 
- UNRESOLVED ADD-03:p3-image/signatory: مدير مكتب خدمات الاستثمار بالمنطقة الشمالية
- UNRESOLVED ADD-03:p3-image/image-footer: FICTIONAL DOCUMENT - Lamar Holding internal assessment pack - not a real tender. SYNTHETIC: not tender content.
- cover summary vs provisions (C28, report only): 3 finding(s)
  - figure differs: the summary says 'reduces the unpaid sum that constitutes an Authority Event of Default under Volume V Clause 39.4 to SAR 8,000,000' (SAR 8,000,000); ADD-03:4.1 says 'The amount stated in Volume V Clause 39.4 is reduced by forty per cent (40%).'; ADD-03:4.2 says 'The period of sixty (60) days in Volume V Clause 39.4 is unchanged.' (no figure SAR 8,000,000 is stated there)
  - contradicted: 'responds to clarification requests 15 to 20': the summary names requests 15 to 20; the addendum answers 15, 16, 17, 18, 19
  - omitted: ADD-03/2.6 confirms VOL-I:12.2; the summary does not mention it: 'The periods in Volume I Clause 12.2 for Commercial Close and Financial Close are unchanged.'

#### Validated vs candidate (partial should not mean useless)

- validated (unchanged, ADD-02): `<outputs>/a3/a3.pdf` (one page), `<outputs>/a5/`
- candidate (CANDIDATE — NOT VALIDATED, ADD-03 as proposed): `<outputs>/a3/a3_candidate.pdf` / `.md`, `<outputs>/a5/candidate/`

**What may be changing.** ADD-03 is PARTIAL: 23 of 52 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 7 op(s) that are valid there stood (each still a proposal: review proposed 7), A3 would gain 1 row(s) (ADD-03-2.4-01 (register)), lose 0 (none) and change 0 (none); A5, replanned at ADD-03's issue date (2026-11-18), would move the latest dates of 0 activities (none), add 1 (cir-portal-notification) and remove 0 (none), and marks 9 REVIEW through relationships. Not settled: 4 activities blocked by an unresolved row (deviations-review, investment-licence, form-4e, cir-portal-notification), 0 STALE row(s), 1 obligation(s) reaching no output (C46), 0 relationship chain(s) blocked or incomplete, 5 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT and 6 more. Clarification route: the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person. Nothing here is validated, accepted or applied to the real state.

- **Clarification route:** the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person (ADD-03 issued 2026-11-18; the cut-off is computed from VOL-I-5.2-01 at that stage). No question about it is suggested as sendable; a proposed entry stays a DRAFT, not sent.

### Requirements

- new: 6; out of force: 0; changed: 1

- NEW ADD-03-cover-01: NEW (introduced by ADD-03/cover/para3)
- NEW ADD-03-3.1-01: NEW (introduced by ADD-03/3.1) (by ADD-03/3.1)
- NEW ADD-03-2.3-01: NEW (introduced by ADD-03:2.3)
- NEW ADD-03-2.4-01: NEW (introduced by ADD-03:2.4)
- NEW ADD-03-2.5-01: NEW (introduced by ADD-03:2.5)
- NEW ADD-03-3.4-01: NEW (introduced by ADD-03:3.4)
- CHANGED VOL-IV-F4E-01: VOL-V 39.4: '20,000,000' -> '12,000,000' by ADD-03/4.1 (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed))
- CONFIRMED (unchanged) VOL-I-12.2-01: confirmed by ADD-03/2.6 (confirms; ADD-03:2.6) (proposed op, awaiting a person's acceptance); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'ADD-03 2.6: 'The periods in Volume I Clause 12.2 for Commercial Close and Financial Close are unchanged.' The effective text is unchanged, so the reading is re…') (proposed reading, awaiting a person's acceptance)
- CONFIRMED (unchanged) VOL-V-44.2-01: confirmed by ADD-03/Q17 (confirms; ADD-03:Q17; answer reads 'none' (summary.classify_answer)) (proposed op, awaiting a person's acceptance); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'The ADD-03 Q17 response, 'Yes. Volume V Clause 44.2 applies.', confirms the clause unchanged. [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route hos…') (proposed reading, awaiting a person's acceptance)
- NOT SETTLED VOL-I-8.9-01: unchanged by the applied ops; not confirmed while: ADD-03:2.1 UNRESOLVED: not promotable: ADD-03/2.1 conflicting (consistency: VOL-I:8.9: ADD-03/2.1, ADD-03/2.4 change the same unit in different ways across the set); ADD-03/2.1-row i…; ADD-03:2.4 UNRESOLVED: not promotable: ADD-03/2.4 interpretation_pending (dropped: not ready: promotion waits whil…
- NOT SETTLED VOL-I-12.2-02: unchanged by the applied ops; not confirmed while: open: I-VOL-I-BOND-LONGSTOP, human decision pending (the confirming op(s) do not settle it: proposed op ADD-03/2.6 (awaiting a person's acceptance): confirms; ADD-03:2.6)

### Stale readings and decisions

- no row is STALE

### Obligations not reaching the outputs (C46)

- ADD-03/cover/para3 [A3]: ADD-03/cover/para3 brings in consequence words ['rejected'] that no row's consequence carries at ADD-03: 'SYNTHETIC: not tender content. Test material for blind rehearsal 08; not issued by any authority. This Addendum replaces Volume I Clau

### Reached through relationships (indirect: for review, not direct citations)

Curated links (relationships file) followed from what changed. The requirements above cite a changed unit; these are reached through another provision, in three classes that are never merged. A5 marks the activities that serve them REVIEW with their dates unchanged.

Relationship status: confirmed = stated in the documents (the entry quotes the cross-reference), not confirmed by a person; proposed = inferred by a curator or a model, a person decides; possible = a weaker inference.

#### Confirmed dependency (1)
- VOL-IV-F4E-01 (row; ACTIVE) <- VOL-V:39.4 via REL-VOL-V-FORM-4E [depends_on; link confirmed]

#### Proposed relationship (2)
- ADD-03-3.1-01 (row; NEW (introduced by ADD-03/3.1)) <- ADD-03-3.4-01 via REL-AI-001 [depends_on; link proposed]; also changed directly
- ADD-03:p3-image (unit; ACTIVE) <- ADD-03:2.2 via REL-AI-002 [cites; link proposed]; also changed directly

#### Possible impact (17)
- ADD-03:4.1 (unit; ACTIVE) <- ADD-03:Q19 via REL-AI-008 [cites; link possible]; also changed directly
- VOL-I-8.10-01 (row; ACTIVE) <- words:consortium member via REL-MEMBER-DEBARMENT [member_scope; link possible]
- VOL-I-8.2-01 (row; ACTIVE) <- words:consortium member via REL-MEMBER-MULTIPLE-PARTICIPATION [member_scope; link possible]
- VOL-I-8.4-01 (row; ACTIVE) <- words:consortium member via REL-MEMBER-FIN-STANDING [member_scope; link possible]
- VOL-I-8.4-02 (row; ACTIVE) <- words:consortium member via REL-MEMBER-FIN-STANDING [member_scope; link possible]
- VOL-I-8.9-01 (row; ACTIVE) <- ADD-03:2.1 via REL-AI-003 [depends_on; link possible]; also changed directly
- VOL-I-8.9-01 (row; ACTIVE) <- words:consortium member via REL-MEMBER-INVESTMENT-LICENCE [member_scope; link possible]; also changed directly
- VOL-I-9.4-01 (row; ACTIVE) <- words:consortium member via REL-MEMBER-FORM-4C [member_scope; link possible]
- VOL-IV-F4C-02 (row; ACTIVE) <- words:consortium member via REL-MEMBER-MULTIPLE-PARTICIPATION [member_scope; link possible]
- VOL-IV-F4C-03 (row; ACTIVE) <- words:consortium member via REL-MEMBER-DEBARMENT [member_scope; link possible]
- VOL-IV-F4C-N1 (row; ACTIVE) <- words:consortium member via REL-MEMBER-FORM-4C [member_scope; link possible]
- VOL-V-12.1-01 (row; ACTIVE) <- ADD-03:3.3 via REL-AI-005 [depends_on; link possible]
- calc:financial-standing (calculation) <- words:consortium member via REL-MEMBER-FIN-STANDING [member_scope; link possible]
- fin-model-build (activity) <- ADD-03:3.4 via REL-AI-006 [depends_on; link possible]
- investment-licence (activity) <- ADD-03:2.1, ADD-03:2.3 via REL-AI-004 [depends_on; link possible]
- investment-licence (activity) <- ADD-03:Q16 via REL-AI-007 [depends_on; link possible]
- technical-proposal (activity) <- ADD-03:3.4 via REL-AI-006 [depends_on; link possible]

#### Referenced but not supplied: conclusions in play that cannot be established (0)
- none

### Disqualifiers (A3)

- no change

### Earlier answers to re-read against the new text (never revoked; a person decides)

- `ADD-03:Q19` (ADD-03): cites VOL-V:39.4, changed by ADD-03/4.1; to be re-read against the new text of VOL-V:39.4 (ADD-03/4.1); a person decides whether the answer still holds

### Programme impact (status date 2026-10-22 -> 2026-11-18)

- STATUS assemble-envelope-a: timing INFEASIBLE by 12 WD -> INFEASIBLE by 31 WD; total float -12 -> -31 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS assemble-envelope-b: timing OK -> INFEASIBLE by 19 WD; total float 0 -> -19 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS attendance-notice: timing CONDITIONAL — window elapsed 2026-10-14; whether the condition arose is not known -> CONDITIONAL — window elapsed 2026-10-14; whether the condition arose is not known; total float -7 -> -26 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS bond-approval: timing OK -> INFEASIBLE by 9 WD; total float +10 -> -9 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS bond-issue: timing OK -> INFEASIBLE by 9 WD; total float +10 -> -9 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- NEW cir-portal-notification: needed by ADD-03-2.5-01
- STATUS clarifications: timing OK -> DEADLINE PASSED; total float +13 -> -6 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS completion-certs: timing OK -> INFEASIBLE by 12 WD; total float +7 -> -12 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS consortium-check: timing OK -> INFEASIBLE by 6 WD; total float +13 -> -6 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS copies: timing INFEASIBLE by 12 WD -> INFEASIBLE by 31 WD; total float -12 -> -31 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS deliver: timing INFEASIBLE by 12 WD -> INFEASIBLE by 31 WD; total float -12 -> -31 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- REWORK deviations-review: requirement changed: VOL-IV-F4E-01 (dependency: VOL-V 39.4: '20,000,000' -> '12,000,000' by ADD-03/4.1 (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed)))
- CONFIRMED (unchanged) deviations-review: VOL-V-44.2-01: confirmed by ADD-03/Q17 (confirms; ADD-03:Q17; answer reads 'none' (summary.classify_answer)) (proposed op, awaiting a person's acceptance); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'The ADD-03 Q17 response, 'Yes. Volume V Clause 44.2 applies.', confirms the clause unchanged. [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route hos…') (proposed reading, awaiting a person's acceptance); text, cells, dates, status and consequence unchanged: work done stands
- STATUS deviations-review: timing OK -> INFEASIBLE by 8 WD; total float +11 -> -8 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS fin-assumptions: timing OK -> INFEASIBLE by 14 WD; total float +5 -> -14 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- REWORK fin-model-build: requirement changed: ADD-03-3.4-01 (text, status, consequence, quote, parameters)
- STATUS fin-model-build: timing OK -> INFEASIBLE by 19 WD; total float 0 -> -19 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- REWORK fin-model-freeze: requirement changed: ADD-03-3.4-01 (text, status, consequence, quote, parameters)
- STATUS fin-model-freeze: timing OK -> INFEASIBLE by 19 WD; total float 0 -> -19 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS fin-standing: timing OK -> INFEASIBLE by 4 WD; total float +15 -> -4 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS fin-statements: timing OK -> INFEASIBLE by 4 WD; total float +15 -> -4 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- REWORK form-4a: requirement changed: ADD-01-AppA-01 (Addenda to acknowledge: ADD-03 issued since ADD-02: 'Bidders shall acknowledge receipt in Form 4-A.'), ADD-03-cover-01 (text, status, consequence, quote, parameters)
- NOT SETTLED form-4a: VOL-IV-F4A-01: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); VOL-IV-F4A-02: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); unchanged at this stage but not confirmed: a person decides
- STATUS form-4a: timing OK -> INFEASIBLE by 7 WD; total float +12 -> -7 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- REWORK form-4a-prep: requirement changed: ADD-01-AppA-01 (Addenda to acknowledge: ADD-03 issued since ADD-02: 'Bidders shall acknowledge receipt in Form 4-A.'), ADD-03-cover-01 (text, status, consequence, quote, parameters)
- NOT SETTLED form-4a-prep: VOL-IV-F4A-01: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); VOL-IV-F4A-02: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); unchanged at this stage but not confirmed: a person decides
- STATUS form-4a-prep: timing OK -> OK; total float +20 -> +1 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS form-4b: timing OK -> INFEASIBLE by 12 WD; total float +7 -> -12 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS form-4b-prep: timing OK -> INFEASIBLE by 10 WD; total float +9 -> -10 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS form-4c-prep: timing OK -> INFEASIBLE by 1 WD; total float +18 -> -1 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS form-4c-sign: timing OK -> INFEASIBLE by 9 WD; total float +10 -> -9 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- REWORK form-4e: requirement changed: VOL-IV-F4E-01 (dependency: VOL-V 39.4: '20,000,000' -> '12,000,000' by ADD-03/4.1 (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed)))
- CONFIRMED (unchanged) form-4e: VOL-V-44.2-01: confirmed by ADD-03/Q17 (confirms; ADD-03:Q17; answer reads 'none' (summary.classify_answer)) (proposed op, awaiting a person's acceptance); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'The ADD-03 Q17 response, 'Yes. Volume V Clause 44.2 applies.', confirms the clause unchanged. [AI workflow run ADD-03-run-host-20261008T053735Z-77b2 (route hos…') (proposed reading, awaiting a person's acceptance); text, cells, dates, status and consequence unchanged: work done stands
- STATUS form-4e: timing OK -> INFEASIBLE by 18 WD; total float +1 -> -18 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS form-4f: timing OK -> INFEASIBLE by 19 WD; total float 0 -> -19 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS form-4g-review: timing OK -> INFEASIBLE by 2 WD; total float +17 -> -2 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS form-4g-sign: timing OK -> INFEASIBLE by 7 WD; total float +12 -> -7 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS ground-dd: timing OK -> INFEASIBLE by 14 WD; total float +5 -> -14 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- REWORK investment-licence: requirement changed: ADD-03-2.4-01 (text, status, consequence, quote, parameters)
- CONFIRMED (unchanged) investment-licence: VOL-I-8.9-01: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'The effective text in units_after is unchanged because op ADD-03/2.1 (the replacement) is not applied: it conflicts with ADD-03/2.4. The ADD-03 Q15 response (a…') (proposed reading, awaiting a person's acceptance); other ops on its units (the re-made reading records no change from them; a person checks): ADD-03/Q15 (interprets; ADD-03:Q15; answer reads 'changes' (summary.classify_answer)); text, cells, dates, status and consequence unchanged: work done stands
- STATUS investment-licence: timing OK -> INFEASIBLE by 11 WD; total float +8 -> -11 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS iso-copy: timing OK -> OK; total float +21 -> +2 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS lcc-certificate: timing INFEASIBLE by 12 WD -> INFEASIBLE by 31 WD; total float -12 -> -31 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS lcc-ratio: timing INFEASIBLE by 12 WD -> INFEASIBLE by 31 WD; total float -12 -> -31 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS lender-terms: timing OK -> INFEASIBLE by 14 WD; total float +5 -> -14 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS model-audit-opinion: timing OK -> INFEASIBLE by 19 WD; total float 0 -> -19 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS model-audit-review: timing OK -> INFEASIBLE by 18 WD; total float +1 -> -18 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS model-auditor-appoint: timing OK -> INFEASIBLE by 18 WD; total float +1 -> -18 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS om-evidence: timing OK -> INFEASIBLE by 6 WD; total float +13 -> -6 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS pcg-execution: timing OK -> INFEASIBLE by 16 WD; total float +3 -> -16 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS pcg-wording: timing OK -> INFEASIBLE by 16 WD; total float +3 -> -16 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS poa: timing OK -> INFEASIBLE by 11 WD; total float +8 -> -11 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS poa-resolutions: timing OK -> INFEASIBLE by 11 WD; total float +8 -> -11 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS references: timing OK -> INFEASIBLE by 10 WD; total float +9 -> -10 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS seal-and-mark: timing INFEASIBLE by 12 WD -> INFEASIBLE by 31 WD; total float -12 -> -31 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- STATUS spoc: timing OK -> OK; total float +21 -> +2 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- REWORK technical-proposal: requirement changed: ADD-03-3.4-01 (text, status, consequence, quote, parameters)
- STATUS technical-proposal: timing OK -> INFEASIBLE by 18 WD; total float +1 -> -18 WD; the planning date moved 2026-10-22 -> 2026-11-18, which by itself shifts every float by the Working Days between them
- REVIEW (confirmed dependency) deviations-review: VOL-IV-F4E-01 reached from VOL-V:39.4 via REL-VOL-V-FORM-4E; dates unchanged
- REVIEW (possible impact) deviations-review: VOL-V-12.1-01 reached from ADD-03:3.3 via REL-AI-005; dates unchanged
- REVIEW (possible impact) fin-model-build: fin-model-build reached from ADD-03:3.4 via REL-AI-006; dates unchanged
- REVIEW (possible impact) fin-standing: VOL-I-8.4-01, VOL-I-8.4-02 reached from words:consortium member via REL-MEMBER-FIN-STANDING; dates unchanged
- REVIEW (possible impact) fin-statements: VOL-I-8.4-01, VOL-I-8.4-02 reached from words:consortium member via REL-MEMBER-FIN-STANDING; dates unchanged
- REVIEW (possible impact) form-4c-prep: VOL-I-8.10-01, VOL-I-8.2-01, VOL-I-9.4-01, VOL-IV-F4C-02, VOL-IV-F4C-03, VOL-IV-F4C-N1 reached from words:consortium member via REL-MEMBER-DEBARMENT, REL-MEMBER-FORM-4C, REL-MEMBER-MULTIPLE-PARTICIPATION; dates unchanged
- REVIEW (possible impact) form-4c-sign: VOL-I-8.10-01, VOL-I-8.2-01, VOL-I-9.4-01, VOL-IV-F4C-02, VOL-IV-F4C-03, VOL-IV-F4C-N1 reached from words:consortium member via REL-MEMBER-DEBARMENT, REL-MEMBER-FORM-4C, REL-MEMBER-MULTIPLE-PARTICIPATION; dates unchanged
- REVIEW (confirmed dependency) form-4e: VOL-IV-F4E-01 reached from VOL-V:39.4 via REL-VOL-V-FORM-4E; dates unchanged
- REVIEW (possible impact) form-4e: VOL-V-12.1-01 reached from ADD-03:3.3 via REL-AI-005; dates unchanged
- REVIEW (possible impact) investment-licence: VOL-I-8.9-01, investment-licence reached from ADD-03:2.1, ADD-03:2.3, ADD-03:Q16, words:consortium member via REL-AI-003, REL-AI-004, REL-AI-007, REL-MEMBER-INVESTMENT-LICENCE; dates unchanged
- REVIEW (possible impact) technical-proposal: technical-proposal reached from ADD-03:3.4 via REL-AI-006; dates unchanged
- FEASIBILITY lcc-ratio: INFEASIBLE by 12 WD -> INFEASIBLE by 31 WD
- FEASIBILITY lcc-certificate: INFEASIBLE by 12 WD -> INFEASIBLE by 31 WD
- FEASIBILITY fin-model-build: OK -> INFEASIBLE by 19 WD
- FEASIBILITY model-auditor-appoint: OK -> INFEASIBLE by 18 WD
- FEASIBILITY technical-proposal: OK -> INFEASIBLE by 18 WD
- FEASIBILITY pcg-wording: OK -> INFEASIBLE by 16 WD
- FEASIBILITY ground-dd: OK -> INFEASIBLE by 14 WD
- FEASIBILITY lender-terms: OK -> INFEASIBLE by 14 WD
- FEASIBILITY model-audit-review: OK -> INFEASIBLE by 18 WD
- FEASIBILITY completion-certs: OK -> INFEASIBLE by 12 WD
- FEASIBILITY poa-resolutions: OK -> INFEASIBLE by 11 WD
- FEASIBILITY references: OK -> INFEASIBLE by 10 WD
- FEASIBILITY bond-approval: OK -> INFEASIBLE by 9 WD
- FEASIBILITY deviations-review: OK -> INFEASIBLE by 8 WD
- FEASIBILITY consortium-check: OK -> INFEASIBLE by 6 WD
- FEASIBILITY om-evidence: OK -> INFEASIBLE by 6 WD
- FEASIBILITY pcg-execution: OK -> INFEASIBLE by 16 WD
- FEASIBILITY poa: OK -> INFEASIBLE by 11 WD
- FEASIBILITY clarifications: OK -> DEADLINE PASSED
- FEASIBILITY fin-model-freeze: OK -> INFEASIBLE by 19 WD
- FEASIBILITY fin-statements: OK -> INFEASIBLE by 4 WD
- FEASIBILITY model-audit-opinion: OK -> INFEASIBLE by 19 WD
- FEASIBILITY form-4g-review: OK -> INFEASIBLE by 2 WD
- FEASIBILITY form-4c-prep: OK -> INFEASIBLE by 1 WD
- FEASIBILITY investment-licence: OK -> INFEASIBLE by 11 WD
- FEASIBILITY form-4b-prep: OK -> INFEASIBLE by 10 WD
- FEASIBILITY bond-issue: OK -> INFEASIBLE by 9 WD
- FEASIBILITY fin-standing: OK -> INFEASIBLE by 4 WD
- FEASIBILITY form-4c-sign: OK -> INFEASIBLE by 9 WD
- FEASIBILITY fin-assumptions: OK -> INFEASIBLE by 14 WD
- FEASIBILITY form-4e: OK -> INFEASIBLE by 18 WD
- FEASIBILITY form-4f: OK -> INFEASIBLE by 19 WD
- FEASIBILITY form-4a: OK -> INFEASIBLE by 7 WD
- FEASIBILITY form-4b: OK -> INFEASIBLE by 12 WD
- FEASIBILITY form-4g-sign: OK -> INFEASIBLE by 7 WD
- FEASIBILITY assemble-envelope-a: INFEASIBLE by 12 WD -> INFEASIBLE by 31 WD
- FEASIBILITY assemble-envelope-b: OK -> INFEASIBLE by 19 WD
- FEASIBILITY copies: INFEASIBLE by 12 WD -> INFEASIBLE by 31 WD
- FEASIBILITY seal-and-mark: INFEASIBLE by 12 WD -> INFEASIBLE by 31 WD
- FEASIBILITY deliver: INFEASIBLE by 12 WD -> INFEASIBLE by 31 WD
- FEASIBILITY cir-portal-notification: absent -> NO DEADLINE REACHED

## Next (a person)

- read the unresolved and escalated provisions first, then each item against its evidence (`../ai/ADD-03-run-host-20261008T053735Z-77b2-combined/proposals.yaml`, `../downstream/proposals.yaml`)
- nothing here is applied to the real curation: to take an item over, add the PDF to the pack (OPERATING_GUIDE §3 steps 1-2) and copy the reviewed files listed in `promotion.json`; then `pin`, `check-register`, `outputs` and decide with `accept` / `reject` as usual
