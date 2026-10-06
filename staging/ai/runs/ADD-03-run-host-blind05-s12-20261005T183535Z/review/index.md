# Review packet: ADD-03, AI workflow run ADD-03-run-host-blind05-s12-20261005T183535Z

> **CANDIDATE: proposed by the AI workflow; not reviewed; nothing accepted.** Statuses are the controller's; a person decides every item. The real `curation/`, `config/` and `out/` were only read: everything below lives in this run's folder.

- PDF: `/home/user/tender-pack-reader/rehearsals/blind-05/input/ADD-03_Addendum_No_3.pdf` (sha256 9c5e22d59a80d48f…, 5 pages); preceding state: pack `/home/user/tender-pack-reader/config/pack.yaml` (NUPA-ISTP-2026-014), previous evidence build `/home/user/tender-pack-reader/build`
- route **host**; model requested `claude-code headless (opus)`, reported `None`; host sessions report: claude-opus-5-5
- status **partial**: 17 provision(s) unresolved in the candidate (listed first in the review packet); 27 downstream task(s) answered only by items that cannot be promoted: row:VOL-I-8.3-01, c46:ADD-03/2.1(a), c46:ADD-03/3.2, c46:ADD-03/7.1, clar:CQ-VOL-V-SCHEDULES, act:iso-copy, act:technical-proposal, act:form-4f …; check-register on the candidate: exit 1, 4 finding(s) {'disposition': 1, 'assessment': 1, 'C46': 2}; C46: [C46] ADD-03/3.2: [A1] ADD-03/3.2 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-V:1.1; a r…; [C46] ADD-03/7.1: [A1] ADD-03/7.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-II:5.5; a …
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed

## Execution, completeness and approval (three separate things)

- **Execution** (what ran): ingest done, readings done, analysis done, validation done, downstream done, downstream_validation done, critic done, promotion done, pin done, check_register done, outputs done, diff done, review running; batches reading: {'done': 1}; analysis: {'done': 9}; downstream: {'done': 6}
- **Completeness** (what the run completed): **partial**: 17 provision(s) unresolved in the candidate (listed first in the review packet); 27 downstream task(s) answered only by items that cannot be promoted: row:VOL-I-8.3-01, c46:ADD-03/2.1(a), c46:ADD-03/3.2, c46:ADD-03/7.1, clar:CQ-VOL-V-SCHEDULES, act:iso-copy, act:technical-proposal, act:form-4f …; check-register on the candidate: exit 1, 4 finding(s) {'disposition': 1, 'assessment': 1, 'C46': 2}; C46: [C46] ADD-03/3.2: [A1] ADD-03/3.2 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-V:1.1; a r…; [C46] ADD-03/7.1: [A1] ADD-03/7.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-II:5.5; a …
  - downstream tasks: 62; answered 35; unanswered 0; answered only by items that cannot be promoted 27; answered 'no change' 10
- **Human approval**: **none** (nothing approved, accepted, rejected or sent); no decision is recorded in the candidate's decisions file

## What is candidate and what is real

- **Candidate** (proposed by this run, nothing accepted): `../candidate/` — a copy of the curation and configuration with ADD-03 added, its evidence build, its op file, rows, issues, templates and outputs.
- **Last validated state**: `../candidate/out-before/` (the pre-addendum outputs built from the copied curation and the previous evidence build; done)
- **Real** (untouched): `curation/`, `config/`, `out/`; the owner's approvals and readings were copied unchanged and used read-only.

- real inputs changed since the run started: config/assumptions.yaml, curation/amendments/ADD-01.yaml, curation/clarifications/register.yaml, curation/register/issues.yaml, curation/register/issues/VOL-II-V.yaml, curation/register/pins.yaml, curation/register/rows/ADD.yaml, curation/register/rows/VOL-I.yaml, curation/register/rows/VOL-IV.yaml, curation/register/rows/VOL-V.yaml (by someone else: this run wrote nothing there; the candidate used the copies made at the start)

## Candidate outputs

Exit 0 (WORKING DRAFT (not releasable)); every file carries the banner (`../candidate/out/CANDIDATE.md`); A1 has a candidate status column {'PROPOSED BY THE AI WORKFLOW': 19, 'proposed (existing row; not changed by this run; not reviewed)': 183, 'UNRESOLVED': 4}.

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

- before → after: {"a1": {"rows_before": 205, "rows_after": 206, "new": 1, "gone": 0}, "a3": {"before": 17, "after": 17, "enters": 0, "leaves": 0}, "a5": {"activities_before": 44, "activities_after": 44, "new": 0, "gone": 0}}

- ADD-03 is **PARTIAL** in the candidate (provisions unresolved): A3 and the A5 programme show the validated state (ADD-02); ADD-03 as proposed is in A1's `Status after ADD-03` column, in A2, in the candidate A3 and A5 below, in `a5/working/ADD-03.json` and in the diff below.

### Validated and candidate A3 / A5 (partial should not mean useless)

- **Validated** (unchanged; ADD-02): [a3/a3.pdf](../candidate/out/a3/a3.pdf) (one page), [a5/README.md](../candidate/out/a5/README.md), [a5/gantt.html](../candidate/out/a5/gantt.html)
- **Candidate** (CANDIDATE — NOT VALIDATED; ADD-03 as proposed): [a3/a3_candidate.pdf](../candidate/out/a3/a3_candidate.pdf) (8 page(s)), [a3/a3_candidate.md](../candidate/out/a3/a3_candidate.md), [a5/candidate/README.md](../candidate/out/a5/candidate/README.md), [a5/candidate/gantt.html](../candidate/out/a5/candidate/gantt.html)

**What may be changing.** ADD-03 is PARTIAL: 17 of 57 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 19 op(s) that are valid there stood (each still a proposal: review proposed 19), A3 would gain 1 row(s) (ADD-03-2.1-01 (ADD-03/2.1(a))), lose 0 (none) and change 1 (VOL-I-8.3-01 (ADD-03/Q17)); A5, replanned at ADD-03's issue date (2026-11-15), would move the latest dates of 0 activities (none), add 0 (none) and remove 0 (none), and marks 7 REVIEW through relationships. Not settled: 7 activities blocked by an unresolved row (fin-model-build, technical-proposal, deviations-review, fin-model-freeze and 3 more), 2 STALE row(s), 2 obligation(s) reaching no output (C46), 0 relationship chain(s) blocked or incomplete, 6 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT and 5 more. Clarification route: the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person. Nothing here is validated, accepted or applied to the real state.

- ENTERS ADD-03-2.1-01: explicit (rejection): “a modification received after the time stated in this Clause, will be rejected unopened and returned to the Bidder.”; ops ADD-03/2.1(a) (interpretation_pending)
- CHANGES VOL-I-8.3-01: now STALE; ops ADD-03/Q17 (interpretation_pending)

- blockers: 17 unresolved provision(s), 7 blocked activit(y/ies), 2 STALE row(s), 2 C46 gap(s), 0 relationship chain(s) blocked or incomplete, 6 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT, I-VOL-III, I-VOL-II-MISSING, I-VOL-V-MISSING, I-VOL-IV-SCALE, I-OP-ADD-01/Q4
- conditional scenarios: 0

**Image-read units** (the review packet of each region shows every crop beside its reading; translations are proposals, not evidence):

- ADD-03-p4-r1 (ADD-03 p4; reading pending): [packet](../candidate/build/review/ADD-03-p4-r1/packet.html); 21 unit(s) touched
  - `ADD-03:p4-image`: “Appendix A (image, Arabic with English header): Northern Region Airspace Safeguarding Office letter reproducing Table 5-1, Maximum height of structures and equipment on site”
  - `ADD-03:p4-image/hdr-en`: “Northern Region Airspace Safeguarding Office”
  - `ADD-03:p4-image/hdr-ar`: “مكتب حماية المجال الجوي بالمنطقة الشمالية”; translation (apart): ‘Airspace Protection Office in the Northern Region’
  - `ADD-03:p4-image/date`: “التاريخ: ١٠ نوفمبر ٢٠٢٦م”; translation (apart): ‘Date: 10 November 2026 AD’
  - `ADD-03:p4-image/ref`: “الرقم: ٤٧١/٢٠٢٦”; translation (apart): ‘No.: 471/2026’
  - `ADD-03:p4-image/subject`: “الموضوع: اشتراطات الارتفاعات لموقع محطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان”; translation (apart): ‘Subject: Height requirements for the site of the Wadi Al-Sirhan Independent Sewage Treatment Plant’
  - `ADD-03:p4-image/tender-ref`: “مناقصة رقم: NUPA/ISTP/2026/014”; translation (apart): ‘Tender number: NUPA/ISTP/2026/014’
  - `ADD-03:p4-image/table-title`: “جدول ٥-١: الحدّ الأقصى لارتفاع المنشآت والمعدّات في الموقع”; translation (apart): ‘Table 5-1: Maximum height of structures and equipment on the site’
  - `ADD-03:p4-image/table-intro`: “يُحدِّد الحدّ الأقصى المسموح به للارتفاع في كل منطقة من مناطق الموقع على النحو الآتي:”; translation (apart): ‘The maximum permitted height in each zone of the site is determined as follows:’; uncertain: the first word appears to carry damma on ya and shadda with kasra on dal (يُحدِّد) as printed; a passive reading يُحدَّد would fit the sentence better grammatically. Reviewer to check the mark under …
  - `ADD-03:p4-image/th-left`: “الإنارة التحذيرية الحدّ الأقصى للارتفاع (متر فوق منسوب الأرض الطبيعية)”; translation (apart): ‘Column headings in the left half: 'Warning lighting'; 'Maximum height (metres above natural ground level)'’
  - `ADD-03:p4-image/th-right`: “الوصف المنطقة”; translation (apart): ‘Column headings in the right half: 'Description'; 'Zone'’
  - `ADD-03:p4-image/row-a-left`: “مطلوبة”; translation (apart): ‘Zone A, warning lighting: Required’
  - … 9 more in `a3/a3_candidate.md`
- VOL-II-p3-r1 (VOL-II p3; reading approved): [packet](../candidate/build/review/VOL-II-p3-r1/packet.html); not touched by this addendum
- VOL-IV-p6-r1 (VOL-IV p6; reading approved): [packet](../candidate/build/review/VOL-IV-p6-r1/packet.html); not touched by this addendum

## Timings (wall clock per step)

| Step | Seconds | Status |
|---|---|---|
| ingest | 16.1 | done |
| readings | 186.8 | done |
| analysis | 2529.0 | done |
| validation | 5.6 | done |
| downstream | 1315.8 | done |
| downstream_validation | 0.9 | done |
| critic | 67.8 | done |
| promotion | 22.8 | done |
| pin | 1.4 | done |
| check_register | 4.3 | done |
| outputs | 13.7 | done |
| diff | 3.0 | done |
| review | 0.0 | running |
| **total** | **4167.2** (69.5 min) | target 30 min from the PDF to candidate outputs and this packet, human review excluded |

## Readings of the addendum's image regions (AI-proposed, PENDING HUMAN REVIEW)

Ingest first refused the candidate because these image regions had no reading (C05): ADD-03-p4-r1. Each reading below was proposed by the route of this run, checked by readings.check_reading and written into the candidate's readings; it is an interpretation of an image, never approved, and every unit made from it carries `reading.status: pending`.

- **ADD-03-p4-r1** — done; controller status **interpretation_pending**; unit `ADD-03:p4-image`; file `../candidate/curation/readings/ADD-03-p4-r1.yaml`
  - the reading beside its crops (the build's review packet): [../candidate/build/review/ADD-03-p4-r1/packet.html](../candidate/build/review/ADD-03-p4-r1/packet.html)
  - form reading, languages ['ar', 'en']; prepared by: AI-assisted: headless host session ADD-03-hostsession-20261005T183553Z-2863 (claude-code headless (opus); the CLI reported claude-opus-5-5), in AI workflow run ADD-03-run-host-blind05-s12-20261005T183535Z (reading-ADD-03-p4-r1), 2026-10-05T18:38:45Z; proposed for a person's review, not approved
  - uncertainty: No ruled grid was detected, although the image shows a ruled 4-column table (Zone | Description | Maximum height | Warning lighting, right to left) with two rows (أ, ب). Cells are recorded as lines of the band halves they fall in. A person…
  - uncertainty: Diacritics (shadda on الحدّ, المعدّات, معدّات; tanween on متراً, يوماً; hamza forms) were read at native resolution.
  - uncertainty: The letter's date (10 November 2026) and reference come from the image only. The page text layer says the Arabic text governs in accordance with Section 7 of the Addendum.

## First: unresolved provisions and escalations

17 of 57 provisions are not answered by a promoted item (each is `unresolved` in the candidate op file with the reason); 0 escalation(s).

- **Clarification route:** the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person (ADD-03 issued 2026-11-15; the cut-off is computed from VOL-I-5.2-01 at that stage). No question about it is suggested as sendable; a proposed entry stays a DRAFT, not sent.

- **UNRESOLVED ADD-03:5.1** (clause, p2): not promotable: ADD-03/5.1 conflicting (consistency: VOL-II:3.4: ADD-03/5.1, ADD-03/5.2 change the same unit in different ways across the set); ADD-03/5.1-clar insufficient_evidence (missing_information: the proposer declares missing: ESIA Figure 7-2) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:Q19** (table_row, p2): not promotable: ADD-03/Q19 conflicting (declared_conflicts: the proposer declares: ADD-03:3.3); ADD-03/Q19-issue conflicting (declared_conflicts: the proposer declares: ADD-03:3.3) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:7.3** (clause, p3): not promotable: ADD-03/7.3/row interpretation_pending (dropped: ) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:7.4** (clause, p3): not promotable: ADD-03/7.4/row interpretation_pending (dropped: ) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:p4-image/hdr-en** (reading_block, p4): not promotable: ADD-03/p4-image/hdr-en insufficient_evidence (missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:p4-image/hdr-ar** (reading_block, p4): not promotable: ADD-03/p4-image/hdr-ar insufficient_evidence (missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:p4-image/date** (reading_block, p4): not promotable: ADD-03/p4-image/date insufficient_evidence (missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.; I did not find the ADD-03 issue date, so I could not check whether the l…) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:p4-image/ref** (reading_block, p4): not promotable: ADD-03/p4-image/ref insufficient_evidence (missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:p4-image/subject** (reading_block, p4): not promotable: ADD-03/p4-image/subject insufficient_evidence (missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:p4-image/tender-ref** (reading_block, p4): not promotable: ADD-03/p4-image/tender-ref insufficient_evidence (missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:p4-image/table-title** (reading_block, p4): not promotable: ADD-03/p4-image/table-title insufficient_evidence (missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:p4-image/table-intro** (reading_block, p4): not promotable: ADD-03/p4-image/table-intro insufficient_evidence (missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval. The reading flags as uncertain whether the first word is active يُحدِّد o…) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:p4-image/note2** (reading_block, p4): not promotable: ADD-03/p4-image/note2 conflicting (declared_conflicts: the proposer declares: ADD-03:T5-1/note(2)); ADD-03/p4-image/note2-issue conflicting (declared_conflicts: the proposer declares: ADD-03:T5-1/note(2)) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:p4-image/note3** (reading_block, p4): not promotable: ADD-03/p4-image/note3 interpretation_pending (dropped: ) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:T5-1/note(1)** (note, p5): not promotable: ADD-03/T5-1/note(1) conflicting (declared_conflicts: the proposer declares: ADD-03:p4-image/note1); ADD-03/T5-1/note(1)/issue interpretation_pending (dropped: ); ADD-03/T5-1/note(1)/clar interpretation_pending (dropped: ) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:T5-1/note(2)** (note, p5): not promotable: ADD-03/T5-1/note(2) conflicting (declared_conflicts: the proposer declares: ADD-03:p4-image/note2; ADD-03:p4-image/th-left); ADD-03/T5-1/note(2)/issue interpretation_pending (dropped: ); ADD-03/T5-1/note(2)/clar interpretation_pending (dropped: ) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person
- **UNRESOLVED ADD-03:T5-1/note(3)** (note, p5): not promotable: ADD-03/T5-1/note(3) insufficient_evidence (dependencies: unknown ids ['ADD-03/T5-1/note(3)/row']); ADD-03/T5-1/note(3)/row interpretation_pending (dropped: ) — the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person

## Earlier answers to re-read against the new text (never revoked; a person decides)

- `ADD-01:Q1` (ADD-01): cites VOL-II:3.1, changed by ADD-03/4.1; to be re-read against the new text of VOL-II:3.1 (ADD-03/4.1); a person decides whether the answer still holds (downstream task `reread:ADD-01:Q1`)
- `ADD-01:Q6` (ADD-01): its annotation ADD-01/Q6 targets VOL-V:29.2, changed by ADD-03/3.3; to be re-read against the new text of VOL-V:29.2 (ADD-03/3.3); a person decides whether the answer still holds (downstream task `reread:ADD-01:Q6`)
- `ADD-03:Q17` (ADD-03): cites VOL-I:8.3, changed by ADD-03/Q17; to be re-read against the new text of VOL-I:8.3 (ADD-03/Q17); a person decides whether the answer still holds
- `ADD-03:Q18` (ADD-03): cites VOL-II:3.4, changed by ADD-03/5.2; to be re-read against the new text of VOL-II:3.4 (ADD-03/5.2); a person decides whether the answer still holds
- `ADD-03:Q19` (ADD-03): cites VOL-IV:F4-F, changed by ADD-03/Q20; cites VOL-V:29.2, changed by ADD-03/3.3; to be re-read against the new text of VOL-IV:F4-F, VOL-V:29.2 (ADD-03/Q20, ADD-03/3.3); a person decides whether the answer still holds
- `ADD-03:Q20` (ADD-03): cites VOL-IV:F4-F, changed by ADD-03/Q20; cites VOL-I:6.2, changed by ADD-03/Q20; cites VOL-V:29.2, changed by ADD-03/3.3; to be re-read against the new text of VOL-IV:F4-F, VOL-I:6.2, VOL-V:29.2 (ADD-03/Q20, ADD-03/3.3); a person decides whether the answer still holds
- `ADD-03:Q21` (ADD-03): cites VOL-I:9.7, changed by ADD-03/Q21; to be re-read against the new text of VOL-I:9.7 (ADD-03/Q21); a person decides whether the answer still holds

## Derived effects (session 12: pending readings, computed deadlines, conditions, consequences)

## Computed deadlines and the Working Days left (PROPOSED; nothing typed)

- Working Days left from the issue date (2026-11-15) to the PDD (2026-11-26): 9 (the issue date not counted, the PDD counted; Working Days per VOL-I 2.4 (weekend [4, 5] as date.weekday numbers; holidays none declared))
- `VOL-I:6.6` p3: “two (2) Working Days before the Proposal Due Date” -> **2026-11-24** (computed: calc deadline, anchor PDD = 2026-11-26, rule working-days-before, fingerprint 481f6dfa2104; PROPOSED, not validated)
- `ADD-03:7.3` p3: “three (3) Working Days before the Proposal Due Date” -> **2026-11-23** (computed: calc deadline, anchor PDD = 2026-11-26, rule working-days-before, fingerprint 60b780e98a3a; PROPOSED, not validated); CONDITIONAL: “A Bidder whose Proposal provides for any structure, plant or equipment at the site exceeding thirty (30) metres in height shall notify the Authority through th…”
- `VOL-V:1.1+ADD-03` p1: “twenty-eight (28) days before the Proposal Due Date” -> **2026-10-29** (computed: calc deadline, anchor PDD = 2026-11-26, rule calendar-days-before, fingerprint 64184b01bf55; PROPOSED, not validated)

## Conditions switched and definitions changed (rows flagged: re-read; nothing decided)

- condition changed by ADD-03/4.1: re-read (VOL-II:3.2 applies 'Where a membrane process is proposed'; ADD-03/4.1 adds 'membrane' in an obligation of VOL-II:3.1: the condition may now always hold; a person decides)
- definition of 'Availability Payment' changed by ADD-03/3.1: re-read (VOL-V:1.1 as amended: 'Availability Payment means the annual payment, expressed at Base Date prices, calculated under Clause 29 and adjusted u…')

## Bands and the existing bid-out rules (derived consequences are PROPOSED; HUMAN DECISION PENDING)

- `VOL-V:29.2`: “not less than fifty per cent (50%) and not more than seventy per cent (70%)” — VOL-I-11.5-01 (non_responsive, VOL-I:11.5: “any response that does so shall render the Proposal non-responsive”); read with VOL-IV-F4F-01, VOL-IV-F4F-02
- `ADD-03:3.3`: “not less than fifty per cent (50%) and not more than seventy per cent (70%)” — VOL-I-9.6-01 (non_responsive, VOL-I:9.6: “A Proposal that states ‘no deviations’ in Form 4-E while containing a qualification elsewhere in th…”); VOL-I-10.5-01 (non_responsive, VOL-I:10.5: “Any conditional price, price subject to adjustment other than as provided in Volume V, or alternati…”); VOL-I-11.5-01 (non_responsive, VOL-I:11.5: “any response that does so shall render the Proposal non-responsive”); read with VOL-IV-F4F-01, VOL-IV-F4F-02

## Per provision: source evidence → proposed transition → validation → downstream impact → output difference

### ADD-03:cover/para1 (paragraph, p1) — answered
- source: “Issued 15 November 2026”
- transition: `ADD-03/cover/para1` disposition no_effect: Issue date line of the Addendum ('Issued 15 November 2026'); it states the date of issue and changes no provision of the RFP Documents.
  - validation: **evidence_verified**

### ADD-03:cover/para2 (paragraph, p1) — answered
- source: “Tender NUPA/ISTP/2026/014”
- transition: `ADD-03/cover/para2` disposition no_effect: Cover identification of the tender ('Tender NUPA/ISTP/2026/014' under the heading 'ADDENDUM NO. 3'); it changes no provision.
  - validation: **evidence_verified**

### ADD-03:cover/para3 (paragraph, p1) — answered
- source: “This Addendum consolidates Volume I Clauses 6.6 and 6.7 without change of substance, amends the definition of Availability Payment and the indexation of the Availability Payment under Volume V Clause 29.2, adds a membrane filtration requirement to Volume II Clause 3.1, replaces the odour criterion in Volume II Clause 3.5 by reference to the Environmental an…”
- transition: `ADD-03/cover/para3` amendment_op annotate VOL-IV:F4-A effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The VOL-IV Form 4-A group and the ADD-01 Appendix A field text are not printed in the units. I relied on the controller's verbatim checks for them.
    - concern: The provision says only 'acknowledge receipt in Form 4-A'. The note's 'Addendum No. 3' and the field reference come from the proposer's reading of the ADD-01 reissue. A person should confirm that the reissued Form 4-A is the current target.
- transition: `ADD-03/cover/para3/clarification-substance` clarification {"gap": "The cover of ADD-03 says Clauses 6.6 and 6.7 are consolidated 'without change of substance', but the new Clause 6.6 in ADD-03 Clause 2.1 limits modification of a Proposal to not later than t…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
- transition: `ADD-03/cover/para3/issue-odour` issue {"text": "The ADD-03 cover says it 'replaces the odour criterion in Volume II Clause 3.5', but Volume II Clause 3.5 as it stands at ADD-02 is a noise limit (55 dB(A) day / 45 dB(A) night). Check this…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-002` row_reading (row:VOL-IV-F4A-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-003` row_reading (row:VOL-IV-F4A-02): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-ACT-4A-PREP` no_change (act:form-4a-prep): **interpretation_pending**
  - downstream proposal `DS-ADD03-ACT-4A` no_change (act:form-4a): **interpretation_pending**
  - output difference: CHANGED VOL-IV-F4A-02; A5 NOT SETTLED form-4a; A5 NOT SETTLED form-4a-prep

### ADD-03:1.1 (clause, p1) — answered
- source: “This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.”
- transition: `ADD-03/1.1` disposition no_effect: Recital of authority and precedence: 'This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in accordance with Volum…
  - validation: **evidence_verified**

### ADD-03:1.2 (clause, p1) — answered
- source: “A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.”
- transition: `ADD-03/1.2` disposition no_effect: Interpretation rule for references within this Addendum: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended b…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'unless')

### ADD-03:1.3 (clause, p1) — answered
- source: “Requests for clarification received after the time stated in Volume I Clause 5.2 have not been answered.”
- transition: `ADD-03/1.3` disposition no_effect: Statement of fact applying VOL-I 5.2 ('Requests received after that time will not be answered.'): 'Requests for clarification received after the time stated in…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**

### ADD-03:2.1 (clause, p1) — answered
- source: “Volume I Clauses 6.6 and 6.7 are deleted and replaced by the following single Clause 6.6: ‘6.6 A Bidder may withdraw its Proposal at any time before the Proposal Due Date, and may modify its Proposal not later than two (2) Working Days before the Proposal Due Date, in each case by written notice through the Portal. A Proposal received after the time stated …”
- transition: `ADD-03/2.1(a)` amendment_op replace_text VOL-I:6.6 “A Proposal received after the time stated in Clause 6.1 will be rejected unopen…” → “A Bidder may withdraw its Proposal at any time before the Proposal Due Date, an…”
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
    - concern: The new 6.6 adds a modification cut-off of two Working Days before the due date. The old 6.7 allowed modification up to the due date. This is a substantive change, and the cover says 'without change of substance', so the two conflict. A person should review that wording.
    - concern: The 24 November 2026 date relies on the VOL-I 2.4 calendar, which is not printed here. I checked only that 26 Nov 2026 is a Thursday.
- transition: `ADD-03/2.1(b)` amendment_op set_status VOL-I:6.7
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): agrees — selected because removal; model claude-sonnet-5-5
    - concern: Deleting 6.7 is what the provision says. The 6.7 right to modify up to the due date is not carried over unchanged. The new 6.6 narrows it to two Working Days before the due date. The rationale's 'content is absorbed' therefore understates the change. The withdrawal right is kept.
  - downstream: units changed VOL-I:6.6, VOL-I:6.7; rows citing them VOL-I-6.7-01
  - downstream proposal `P-ADD03-VOL-I-6.1-01` row_reading (row:VOL-I-6.1-01): **interpretation_pending**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: VOL-I:6.1 text and the ADD-01 amendment of the date are not printed in the units shown; the date 26 November 2026 and 14:00 rely on the controller's verbatim check.
      - concern: The provision text shown (ADD-03:2.1) does not label sub-paragraphs (a) and (b); the note's '2.1(a)' is a label I cannot confirm from the text shown. This does not affect the substance.
      - concern: The rejection consequence does follow: the replaced 6.6 keeps 'A Proposal received after the time stated in Clause 6.1 ... will be rejected unopened and returned to the Bidder.'
  - downstream proposal `P-ADD03-ROW-2.1-01` row_new (row:VOL-I-6.7-01): **interpretation_pending — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: The quoted text, the withdraw and modify cut-offs and the late-modification rejection all match ADD-03:2.1. Deleted 6.7 is shown only in a statement, not in the units.
      - concern: The date rule ADD03-MODIFY-CUTOFF is validated with a planning value of 2026-11-26 (as_stated). That does not match the 24 November 2026 reading in the payload, which counts back from 26 November. The person should note this inconsistency.
      - concern: The 24 November calculation relies on the VOL-I 2.4 calendar (Sunday to Thursday), which is not printed here. It is consistent with the stated weekday of the 26th.
      - concern: The clause says 'the time stated in this Clause' but gives no time of day. This is correctly flagged. Whether 'before the Proposal Due Date' for withdrawal runs to 14:00 is also not stated.
      - concern: The cover versus clause substance conflict is correctly left to a person.
  - downstream proposal `P-ADD03-ISSUE-6.6-SUBSTANCE` issue (row:VOL-I-6.7-01): **interpretation_pending — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: The cover paragraph ('without change of substance') and deleted 6.7 are not in the printed units. Both are relied on through the statements and the controller's verbatim checks.
      - concern: The contrast between 6.7 ('at any time before') and the new 6.6 (two Working Days before for modification) is real on the words shown. The issue leaves the decision to a person, which is appropriate.
  - downstream proposal `P-ADD03-CQ-6.6` clarification_item (row:VOL-I-6.7-01): **insufficient_evidence**
  - downstream proposal `DS-ADD03-008` row_new (c46:ADD-03/2.1(a)): **invalid — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-009` issue (c46:ADD-03/2.1(a)): **invalid — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD-03-05` no_change (act:deliver): **interpretation_pending**
  - output difference: NEW ADD-03-2.1-01; OUT VOL-I-6.7-01; CHANGED VOL-I-6.1-01; A3 enters ADD-03-2.1-01; A5 REWORK assemble-envelope-a; A5 REWORK assemble-envelope-b; A5 REWORK copies; A5 REWORK deliver; A5 REWORK seal-and-mark

### ADD-03:2.2 (clause, p1) — answered
- source: “The number 6.7 is not reused. The Clauses of Volume I are not renumbered.”
- transition: `ADD-03/2.2` disposition no_effect: Confirms that no renumbering follows the consolidation in Clause 2.1: 'The number 6.7 is not reused. The Clauses of Volume I are not renumbered.' Op ADD-03/2.1…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'renumbered')

### ADD-03:3.1 (clause, p1) — answered
- source: “In Volume V Clause 1.1, ‘the annual payment calculated under Clause 29’ is deleted and ‘the annual payment, expressed at Base Date prices, calculated under Clause 29’ is substituted.”
- transition: `ADD-03/3.1` amendment_op replace_text VOL-V:1.1 “the annual payment calculated under Clause 29” → “the annual payment, expressed at Base Date prices, calculated under Clause 29”
  - validation: **evidence_verified**
  - downstream: units changed VOL-V:1.1; rows citing them none
  - downstream proposal `DS-ESC-DEFN-ROWS` escalation (defn:VOL-V:1.1): **escalated**

### ADD-03:3.2 (clause, p1) — answered
- source: “The following new Clause 1.1A is inserted in Volume V after Clause 1.1: ‘1.1A Base Date means the date falling twenty-eight (28) days before the Proposal Due Date.’”
- transition: `ADD-03/3.2` amendment_op insert_unit VOL-V:1.1 “Base Date means the date falling twenty-eight (28) days before the Proposal Due Date.”
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: Minor: the new definition is inserted after VOL-V:1.1, which is the Availability Payment definition. This matches the provision's 'after Clause 1.1'.
    - concern: The Base Date is not computed, which is correct, since the Proposal Due Date is not in the evidence.
  - downstream: units changed VOL-V:1.1+ADD-03; rows citing them none
  - downstream proposal `DS-ADD03-010` row_new (c46:ADD-03/3.2): **invalid**

### ADD-03:3.3 (clause, p1) — answered
- source: “Volume V Clause 29.2 is deleted and replaced by the following: ‘29.2 The Availability Payment shall be indexed annually from the Base Date in accordance with Schedule 9. The proportion of the payment indexed to the published consumer price index (the Indexed Proportion) shall be: (a) until the end of the tenth (10th) year of operations, the percentage state…”
- transition: `ADD-03/3.3` amendment_op replace_text VOL-V:29.2 “The Availability Payment shall be indexed annually in accordance with Schedule …” → “The Availability Payment shall be indexed annually from the Base Date in accord…”
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
    - concern: The printed 3.3 text ends at '(a)...; and'. Part (b) and the closing 'balance remain fixed' come from ADD-03:3.3(b), which is not in the units list. The controller verified it as verbatim, so the full replacement is supported.
    - concern: The 60/40 split is removed and replaced by a Bidder-stated 50–70% for years 1–10 and 75% from year 11. 'Deleted and replaced' supports replacing the whole of 29.2, so the old text matches the whole target.
    - concern: A person should confirm the old words match the target, as the controller flags.
- transition: `ADD-03/3.3-form` clarification {"gap": "Replacement Clause 29.2 requires the Indexed Proportion for years 1-10 to be 'the percentage stated by the Bidder in Form 4-F', but Form 4-F (as at ADD-02) has no field for that percentage; …
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The claim that Form 4-F has no field for the percentage is not verifiable from the evidence shown. Only one member field is quoted ('Indexation basis assumed: Per Volume V Clause 29.2'). The VOL-IV:F4-F group and its '20 members' are not printed.
    - concern: The claim that ADD-03 Section 3 does not amend Form 4-F is not shown either. Only 3.2, 3.3 and 3.4 are printed, and no unit says Form 4-F is untouched.
    - concern: The quoted evidence does show that the replacement 29.2 refers to a percentage 'stated by the Bidder in Form 4-F'. It also shows an indexation field that merely points to Clause 29.2. The ambiguity is plausible but not proven.
    - concern: The interim handling (state the percentage against the 'Indexation basis assumed' field) is a suggestion, not something the text supports.
  - downstream: units changed VOL-V:29.2; rows citing them VOL-V-29.2-01
  - downstream proposal `DS-ADD03-007` row_reading (row:VOL-V-29.2-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-012` clarification_item (clar:CQ-VOL-V-SCHEDULES): **insufficient_evidence — HUMAN DECISION PENDING**
  - downstream proposal `DS-ESC-REREAD-Q6` escalation (reread:ADD-01:Q6): **escalated**
  - downstream proposal `DS-RR-VOL-V-29.2-01` row_reading (defn:VOL-V:1.1): **interpretation_pending**
  - downstream proposal `D1` row_new (cons:ADD-03:3.3): **insufficient_evidence — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: The core requirement follows from the text shown. Replaced 29.2(a) says the Indexed Proportion is the percentage the Bidder states in Form 4-F, at least 50% and at most 70%, until the end of year 10. The old VOL-V 29.2 had a fixed 60/40 split.
      - concern: The second date_note quotes 'from the start of the eleventh (11th) year of operations'. The printed ADD-03:3.3 text stops at '(a) ... ; and', so that wording is not in the evidence shown. It is presumably in clause (b), which is not printed. I cannot verify it and it is not tied to any quotation.
      - concern: The row does not say what applies after year 10. Clause (b) is not shown, so the row may be incomplete for the full clause, and the statement that the band covers only the first ten years rests on part of the text.
      - concern: The consequence (non_responsive under VOL-I 10.5) is not stated anywhere in the pack. The item itself says so (S2, I-NO-CONSEQUENCE). Whether a value outside the band is 'price subject to adjustment other than as provided in Volume V' is a judgment. The item marks it as human decision pending, whic…
      - concern: The Form 4-F paragraph shown (para1) only confirms that the Availability Payment is unconditional. It does not show a field for the Indexed Proportion. The evidence therefore does not confirm that Form 4-F has a place to state it. I did not see the form layout.
      - concern: I did not see VOL-I 9.6 or 11.5, so I cannot check the rationale for excluding them. The 5.2 clarification-window-closed claim (S7) is attributed to a 'task packet' and is not supported by the quotation attached to it.
  - downstream proposal `D2` escalation (cons:VOL-V:29.2): **escalated**
  - output difference: CHANGED VOL-V-29.2-01; A5 REWORK deviations-review; A5 REWORK form-4e

### ADD-03:3.3(b) (list_item, p1) — answered
- source: “(b) from the start of the eleventh (11th) year of operations, seventy-five per cent (75%). The balance of the payment shall remain fixed.’”
- transition: content of ADD-03/3.3, ADD-03/3.3

### ADD-03:3.4 (clause, p1) — answered
- source: “Bidders shall reflect this Section 3 in the Financial Model submitted under Volume I Clause 10.3.”
- transition: `ADD-03/3.4` amendment_op annotate VOL-I:10.3 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: 'Shall reflect' is obligation wording with no text change, so an annotate with adds_obligation fits.
    - concern: The obligation applies to 'this Section 3', which includes the Base Date and Indexed Proportion changes. Its scope depends on the S6 interpretation, which a person must confirm.
  - downstream proposal `P-ADD03-VOL-I-10.3-01` row_reading (row:VOL-I-10.3-01): **interpretation_pending**
  - downstream proposal `P-ADD03-VOL-I-10.3-02` row_reading (row:VOL-I-10.3-02): **interpretation_pending**
  - downstream proposal `DS-ADD03-013` activity (act:fin-model-build): **interpretation_pending**
  - downstream proposal `DS-ADD-03-01` activity (act:fin-model-freeze): **interpretation_pending**
  - downstream proposal `DS-ADD-03-02` no_change (act:model-auditor-appoint): **interpretation_pending**
  - downstream proposal `DS-ADD-03-03` no_change (act:model-audit-review): **interpretation_pending**
  - downstream proposal `DS-ADD-03-04` no_change (act:model-audit-opinion): **interpretation_pending**
  - output difference: CONFIRMED (unchanged) VOL-I-10.3-01; CONFIRMED (unchanged) VOL-I-10.3-02; A5 CONFIRMED (unchanged) fin-model-build; A5 CONFIRMED (unchanged) fin-model-freeze; A5 CONFIRMED (unchanged) model-audit-opinion; A5 CONFIRMED (unchanged) model-audit-review; A5 CONFIRMED (unchanged) model-auditor-appoint; A5 REVIEW (confirmed dependency) fin-model-build; A5 REVIEW (proposed relationship) fin-model-build; A5 REVIEW (confirmed dependency) fin-model-freeze; A5 REVIEW (proposed relationship) fin-model-freeze; A5 REVIEW (confirmed dependency) form-4f

### ADD-03:4.1 (clause, p2) — answered
- source: “In Volume II Clause 3.1, ‘The Authority does not mandate a particular process train.’ is deleted and ‘The treatment process shall include a membrane filtration step, either in the tertiary treatment stage or as part of a membrane bioreactor, with a nominal pore size not exceeding 0.1 µm. Subject to the preceding sentence, the Authority does not mandate a pa…”
- transition: `ADD-03/4.1` amendment_op replace_text VOL-II:3.1 “The Authority does not mandate a particular process train.” → “The treatment process shall include a membrane filtration step, either in the t…”
  - validation: **evidence_verified**
  - downstream: units changed VOL-II:3.1; rows citing them VOL-II-3.1-01
  - downstream proposal `P-ADD03-VOL-II-3.1-01` row_reading (row:VOL-II-3.1-01): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ESC-REREAD-Q1` escalation (reread:ADD-01:Q1): **escalated**
  - downstream proposal `DS-RR-VOL-II-3.2-01` row_reading (cond:VOL-II:3.2): **interpretation_pending**
  - downstream proposal `DS-RR-VOL-II-3.2-02` row_reading (cond:VOL-II:3.2): **interpretation_pending**
  - output difference: CHANGED VOL-II-3.1-01; CHANGED VOL-II-3.2-01; CHANGED VOL-II-3.2-02; A5 REWORK technical-proposal

### ADD-03:4.2 (clause, p2) — answered
- source: “Bidders shall reflect this Section 4 in the process design submitted under Volume II Section 3.”
- transition: `ADD-03/4.2` amendment_op annotate VOL-II:S3 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The target is the group VOL-II:S3, evidenced only by its heading 'SECTION 3 — PROCESS REQUIREMENTS'. This matches the cited 'Volume II Section 3'.
    - concern: The content of ADD-03 Section 4 is not shown, so what the obligation covers cannot be checked.
    - concern: The adds_obligation effect depends on the S6 interpretation, which a person must confirm.

### ADD-03:5.1 (clause, p2) — UNRESOLVED
- source: “In Volume II Clause 3.4, ‘not more than 5 OU/m³ at the site boundary’ is deleted and ‘not more than the odour concentration shown for the nearest sensitive receptor in Figure 7-2 of the Environmental and Social Impact Assessment referred to in Volume II Clause 9.1, at that receptor’ is substituted. The basis of assessment (98th percentile hourly value) is u…”
- transition: `ADD-03/5.1` amendment_op replace_text VOL-II:3.4 “not more than 5 OU/m³ at the site boundary” → “not more than the odour concentration shown for the nearest sensitive receptor …”
  - validation: **conflicting** — consistency: VOL-II:3.4: ADD-03/5.1, ADD-03/5.2 change the same unit in different ways across the set
- transition: `ADD-03/5.1-clar` clarification {"gap": "The amended odour criterion in VOL-II:3.4 is defined by reference to Figure 7-2 of the ESIA, which is not in the evidence build; the numeric limit and the receptor cannot be established from…
  - validation: **insufficient_evidence — HUMAN DECISION PENDING** — missing_information: the proposer declares missing: ESIA Figure 7-2
  - downstream proposal `P-ADD03-ESC-ODOUR` escalation (row:VOL-II-3.4-01): **escalated**
  - downstream proposal `P-ADD03-ISSUE-ODOUR` issue (row:VOL-II-3.4-01): **interpretation_pending — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: ADD-03:5.1 and the base VOL-II 3.4 text support the issue: the substitution is stated, and the effective text is reported as unchanged.
      - concern: The cover's reference to Clause 3.5 is not in the printed units. The Q18 'data room' quote appears only in the evidence quotation.
      - concern: The issue appropriately leaves the decision and the odour design basis to a person.
  - downstream proposal `DS-ADD03-ESC-51` escalation (esc:ADD-03:5.1): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
      - concern: Provision text and target text match the item: 5.1 substitutes the nearest-receptor value for 5 OU/m³ at the site boundary, and VOL-II 3.4 still reads 5 OU/m³ at the site boundary in the evidence shown.
      - concern: Claims about 5.2, Q18 and the cover's 'Clause 3.5' wording rest on statements whose quotations I could check only as printed. The cover quotation says 'Clause 3.5', which does differ from 5.1's 'Clause 3.4'.
      - concern: I cannot check from the evidence shown that Figure 7-2 is absent from the build, or that clarifications closed on 2026-11-12 (VOL-I 5.2). The item's own statements assert both. The closure date is also after today's date of 2026-10-05, which is odd but is not a defect in the item.
      - concern: The 'not promoted' status is consistent with the unit status 'not_issued', but the evidence printed does not show the promotion record itself.
      - concern: The item correctly leaves the choice of criterion to a person.
  - downstream proposal `DS-ADD03-DEP-51-FIG72` dependency (esc:ADD-03:5.1): **invalid**

### ADD-03:5.2 (clause, p2) — answered
- source: “Bidders shall demonstrate compliance with Volume II Clause 3.4, as amended, in the Technical Proposal.”
- transition: `ADD-03/5.2` amendment_op annotate VOL-II:3.4 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The clause says "as amended", which points to some amendment of VOL-II 3.4, probably ADD-03/5.1 (listed as a dependency). The evidence shown does not include 5.1, so I could not check that annotating 3.4 without changing its text is right. If 5.1 amends 3.4, a person should check that this annotati…
    - concern: ADD-03:5.2 has status not_issued in the units. The evidence does not say what that means for whether the obligation takes effect. A person should confirm it.
  - downstream proposal `P-ADD03-VOL-II-3.4-01` row_reading (row:VOL-II-3.4-01): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
      - concern: ADD-03:5.1 quotes 'not more than 5 OU/m³ at the site boundary', which matches the VOL-II 3.4 text before the addendum. So the substitution is applicable on the words, and the unapplied op is a gap in the pipeline rather than a conflict between provisions.
      - concern: The statement that no op exists for 5.1 is a pipeline fact I cannot verify from the printed evidence.
      - concern: ESIA Figure 7-2 is absent, so the limit value cannot be stated. 'none_stated' and the 'insufficient evidence' note are appropriate.
      - concern: The cover naming Clause 3.5 is not printed in the units shown, so I cannot verify it.
      - concern: 5.1 confirms that the 98th percentile hourly basis is unchanged.
  - output difference: A5 REWORK technical-proposal

### ADD-03:Q15 (table_row, p2) — answered
- source: “No: 15 | Bidder question: Volume II Clause 6.4 requires process data to be retained for not less than seven (7) years. Would a retention period of ten (10) years be acceptable? | Authority response: Volume II Clause 6.4 states a minimum period. A Bidder may propose a longer period but is not required to do so.”
- transition: `ADD-03/Q15` amendment_op annotate VOL-II:6.4 effect interprets
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - downstream proposal `P-ADD03-VOL-II-6.4-01` row_reading (row:VOL-II-6.4-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-001` row_reading (row:VOL-II-6.4-02): **interpretation_pending**
  - output difference: CONFIRMED (unchanged) VOL-II-6.4-01; CONFIRMED (unchanged) VOL-II-6.4-02; A5 CONFIRMED (unchanged) technical-proposal

### ADD-03:Q16 (table_row, p2) — answered
- source: “No: 16 | Bidder question: May a Bidder state ‘no deviations’ in Form 4-E and set out its assumptions on Volume V in the Technical Proposal? | Authority response: A Bidder that states ‘no deviations’ in Form 4-E shall not include any qualification of Volume V elsewhere in its Proposal. An assumption that limits or qualifies an obligation in Volume V is a qua…”
- transition: `ADD-03/Q16` amendment_op annotate VOL-I:9.6, VOL-IV:F4-E effect interprets
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: The response also says a 'no deviations' Bidder shall not qualify Volume V elsewhere. This restates VOL-I:9.6 and is only partly captured by the annotation note. It does not change the interpretation.
  - downstream proposal `P-ADD03-VOL-I-9.6-01` row_reading (row:VOL-I-9.6-01): **interpretation_pending**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: Q16 supports the reading that assumptions limiting or qualifying Volume V must be listed in Form 4-E, and that 9.6 applies.
      - concern: VOL-I:9.6 text is not printed in the units shown; it relies on the controller's verbatim check.
      - concern: The reading correctly leaves the question of listing the concession-term point to a person.
  - downstream proposal `DS-ADD03-004` row_reading (row:VOL-IV-F4E-01): **interpretation_pending**
  - downstream proposal `DS-ADD-03-11` activity (act:deviations-review): **interpretation_pending**
  - downstream proposal `DS-ADD-03-12` no_change (act:form-4e): **interpretation_pending**
  - output difference: CHANGED VOL-IV-F4E-01; A5 REWORK deviations-review; A5 NOT SETTLED deviations-review; A5 REWORK form-4e; A5 NOT SETTLED form-4e; A5 REVIEW (confirmed dependency) deviations-review; A5 REVIEW (confirmed dependency) form-4e

### ADD-03:Q17 (table_row, p2) — answered
- source: “No: 17 | Bidder question: Where the proposed EPC Contractor is an unincorporated joint venture, which entity must hold the ISO 9001:2015 certificate required by Volume I Clause 8.3? | Authority response: Each member of the joint venture shall hold a certificate that meets Volume I Clause 8.3, and a copy of each certificate shall be submitted with Envelope A.”
- transition: `ADD-03/Q17` amendment_op annotate VOL-I:8.3 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - downstream proposal `P-ADD03-VOL-I-8.3-01` row_reading (row:VOL-I-8.3-01): **insufficient_evidence**
  - downstream proposal `DS-ADD-03-10` activity (act:iso-copy): **insufficient_evidence**
  - output difference: A5 REWORK iso-copy

### ADD-03:Q18 (table_row, p2) — answered
- source: “No: 18 | Bidder question: Will the Authority provide dispersion modelling inputs for the design of the odour control system? | Authority response: The nearest sensitive receptor, and the odour concentration applicable at it for the purposes of Volume II Clause 3.4 as amended by Section 5 of this Addendum, are shown in Figure 7-2 of the Environmental and Soc…”
- transition: `ADD-03/Q18` amendment_op annotate VOL-II:3.4 effect interprets
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The response refers to the nearest sensitive receptor and 'Clause 3.4 as amended by Section 5'. The printed VOL-II:3.4 sets the limit at the site boundary. ADD-03:5.1 is not in the evidence shown, so I cannot tell whether the measurement point or the 5 OU/m³ figure changes.
    - concern: The 'interprets / no text change' label follows for Q18 alone. The effect on 3.4 depends on Section 5, which is not shown.
    - concern: Figure 7-2 is not in the evidence, so the item correctly states no values.
  - downstream proposal `P-ADD03-DEP-ESIA` dependency (row:VOL-II-3.4-01): **invalid**

### ADD-03:Q19 (table_row, p2) — UNRESOLVED
- source: “No: 19 | Bidder question: Form 4-F requests the Availability Payment for year 1 of operations. Is that figure to be stated in the prices of year 1 of operations? | Authority response: Yes. The Availability Payment stated in Form 4-F is the amount payable for year 1 of operations, in the prices of that year. Indexation under Volume V Clause 29.2 applies from…”
- transition: `ADD-03/Q19` amendment_op annotate VOL-IV:F4-F, VOL-V:29.2 effect interprets
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:3.3
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The conflict with ADD-03:3.3 is plausible. 3.3 says 'indexed annually from the Base Date' and Q19 says indexation 'applies from the first anniversary of PCOD'. Only the quoted span of 3.3 is available, not the full unit.
    - concern: The target is the Form 4-F group, and I saw only the quoted label span for the Form 4-F entry.
- transition: `ADD-03/Q19-issue` issue {"text": "ADD-03 Q19 says indexation under Volume V Clause 29.2 'applies from the first anniversary of PCOD', while ADD-03:3.3 substitutes Clause 29.2 with 'indexed annually from the Base Date' (Base…
  - validation: **conflicting — HUMAN DECISION PENDING** — declared_conflicts: the proposer declares: ADD-03:3.3
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The core tension is supported by the two quoted spans.
    - concern: The claim that the Base Date is 28 days before the Proposal Due Date (ADD-03:3.2) is not supported by any evidence shown.
  - downstream proposal `DS-ADD03-ESC-Q19` escalation (esc:ADD-03:Q19): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
      - concern: Q19 says year 1 prices with indexation from the first anniversary of PCOD. 3.1 says Base Date prices and 3.3 says indexation from the Base Date. These are quoted verbatim and do look like different price bases, so the conflict is plausible.
      - concern: The conflict is not certain. Year 1 prices could coincide with Base Date prices, or Q19 could be read as a clarification of how the Form 4-F figure is entered. This is an interpretation that a person must confirm, and the item marks it so.
      - concern: The evidence shown does not include the text of Schedule 9, VOL-V 29.2, or the Base Date definition. These are needed to decide whether the two readings really diverge.
      - concern: The VOL-I 10.5 / 11.5 non_responsive rules are not in the evidence shown. They are only mentioned as PROPOSED.
  - downstream proposal `DS-ADD03-ISSUE-AP-BASIS` issue (esc:ADD-03:Q19): **interpretation_pending — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: The issue restates the Q19 versus 3.1/3.3 tension, and its quotations match the verified text.
      - concern: It is an interpretation that a person must confirm. It states no conclusion and leaves the decision to a person.
      - concern: Whether VOL-I 10.5 / 11.5 is engaged cannot be checked from the evidence shown, but the issue only raises it as a question.
      - concern: The 'clarification window is closed' statement relies on VOL-I 5.2, which is not in the printed evidence.

### ADD-03:Q20 (table_row, p2) — answered
- source: “No: 20 | Bidder question: Form 4-F states ‘Per Volume V Clause 29.2’ against ‘Indexation basis assumed’. Is any figure to be stated in that row? | Authority response: Yes. The Bidder shall complete that row by stating, after the words ‘Per Volume V Clause 29.2’, the Indexed Proportion as a percentage. The Indexed Proportion shall not be stated anywhere in E…”
- transition: `ADD-03/Q20` amendment_op annotate VOL-IV:F4-F, VOL-I:6.2 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The 'Indexed Proportion' is defined in the substituted 29.2 (ADD-03:3.3), which is not shown. The printed 29.2 states 60% and 40%. The item flags the dependency on 3.3.
    - concern: The consequence of stating it in Envelope A follows from VOL-I:6.2, which makes any commercial information in Envelope A non-responsive.
  - downstream proposal `P-ADD03-VOL-I-6.2-01` row_reading (row:VOL-I-6.2-01): **interpretation_pending**
  - downstream proposal `P-ADD03-VOL-I-6.2-02` row_reading (row:VOL-I-6.2-02): **interpretation_pending**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: The reading only records the words and does not decide whether the Indexed Proportion is 'other commercial information'. That is appropriate.
      - concern: VOL-I:6.2 text is not printed in the units shown; it relies on the controller's verbatim check.
      - concern: Form 4-F is not shown, so whether stating the Indexed Proportion there falls inside Envelope A is not determinable here. The item does not claim it.
  - downstream proposal `DS-ADD03-005` row_reading (row:VOL-IV-F4F-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-006` row_reading (row:VOL-IV-F4F-02): **interpretation_pending**
  - downstream proposal `DS-ADD-03-06` no_change (act:seal-and-mark): **interpretation_pending**
  - downstream proposal `DS-ADD-03-07` no_change (act:copies): **interpretation_pending**
  - downstream proposal `DS-ADD-03-08` activity (act:assemble-envelope-a): **interpretation_pending**
  - downstream proposal `DS-ADD-03-09` no_change (act:assemble-envelope-b): **interpretation_pending**
  - downstream proposal `DS-ADD03-ACT-4F` activity (act:form-4f): **insufficient_evidence**
  - output difference: CHANGED VOL-I-6.2-02; CHANGED VOL-IV-F4F-01; CONFIRMED (unchanged) VOL-I-6.2-01; A5 REWORK assemble-envelope-a; A5 CONFIRMED (unchanged) assemble-envelope-a; A5 CONFIRMED (unchanged) assemble-envelope-b; A5 CONFIRMED (unchanged) copies; A5 CONFIRMED (unchanged) deliver; A5 CONFIRMED (unchanged) fin-model-build; A5 CONFIRMED (unchanged) fin-model-freeze; A5 REWORK form-4b; A5 REWORK form-4f; A5 CONFIRMED (unchanged) form-4f; A5 CONFIRMED (unchanged) seal-and-mark; A5 REVIEW (confirmed dependency) fin-model-build; A5 REVIEW (proposed relationship) fin-model-build; A5 REVIEW (confirmed dependency) fin-model-freeze; A5 REVIEW (proposed relationship) fin-model-freeze; A5 REVIEW (confirmed dependency) form-4f; A5 REVIEW (proposed relationship) form-4f

### ADD-03:Q21 (table_row, p2) — answered
- source: “No: 21 | Bidder question: Does the Technical Proposal need to address construction plant in addition to the matters listed in Volume I Clause 9.7? | Authority response: Yes. The construction methodology in the Technical Proposal shall include a crane and lifting plan that demonstrates compliance with Table 5-1 (Volume II Clause 5.6, inserted by Section 7 of…”
- transition: `ADD-03/Q21` amendment_op annotate VOL-I:9.7 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The crane and lifting plan depends on Clause 5.6 / Table 5-1 from ADD-03:7.1, which is not shown. The item correctly relies on no values from it.
  - downstream proposal `P-ADD03-VOL-I-9.7-01` row_reading (row:VOL-I-9.7-01): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-ACT-TP` activity (act:technical-proposal): **insufficient_evidence**
  - output difference: CHANGED VOL-I-9.7-01; A5 REWORK technical-proposal

### ADD-03:7.1 (clause, p2) — answered
- source: “The following new Clause 5.6 is inserted in Volume II after Clause 5.5: ‘5.6 The Project Company shall comply with the height limits in Table 5-1, which is reproduced at Appendix A to this Addendum as issued by the Northern Region Airspace Safeguarding Office and is incorporated into this Volume by reference.’”
- transition: `ADD-03/7.1` amendment_op insert_unit VOL-II:5.5 “The Project Company shall comply with the height limits in Table 5-1, which is reproduced at Appendix A to this Addendu…”
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: Anchor VOL-II:5.5 is correct: the provision inserts new 5.6 after 5.5 and nothing in 5.5 is changed or removed. The new text matches the quoted clause.
- transition: `ADD-03/7.1/row` row_new {"row": {"id": "VOL-II-5.6-01", "group": "VOL-II-5", "scope": ["Project Company", "design", "construction"], "requirement": "The Project Company shall comply with the height limits in Table 5-1 (ADD-…
  - validation: **interpretation_pending**
  - downstream: units changed VOL-II:5.5+ADD-03; rows citing them none
  - downstream proposal `DS-ADD03-011` row_new (c46:ADD-03/7.1): **insufficient_evidence — HUMAN DECISION PENDING**
  - downstream proposal `DS-ROW-P4-01` row_new (reading:ADD-03-p4-r1): **insufficient_evidence** — held back: issue references not among the promoted issues: ['I-ADD03-T51-RENDERINGS']
  - downstream proposal `DS-ROW-P4-02` row_new (reading:ADD-03-p4-r1): **insufficient_evidence** — held back: issue references not among the promoted issues: ['I-ADD03-T51-RENDERINGS']
  - downstream proposal `DS-ROW-P4-03` row_new (reading:ADD-03-p4-r1): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
      - concern: The Arabic quote matches note 1, and the row is marked pending reading and not in force. The conflict with English note (1) is declared and real.
      - concern: The row's requirement text states the Arabic scope, while the note says no rendering is chosen. A reader could take the row as adopting the Arabic reading. Section 7.2 ('The Arabic text governs') is not addressed in the row itself.
      - concern: The post_award_evidence text ('Crane, lifting and temporary works planning…') is the proposer's own wording. The only basis cited is note 1.
      - concern: The row cites units notes-head and p4-image, which are not printed in the request, so I could not check them.
  - downstream proposal `DS-ROW-P4-04` row_new (reading:ADD-03-p4-r1): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
      - concern: The row stays neutral on the datum and marks its post-award evidence 'unresolved', which fits the unresolved conflict.
      - concern: The row's requirement text follows the Arabic reading. This is the same concern as for row 03: Section 7.2 is a person's decision.
      - concern: The th-left unit is cited but not printed in the units section.
  - downstream proposal `DS-ROW-P4-05` row_new (reading:ADD-03-p4-r1): **insufficient_evidence** — held back: issue references not among the promoted issues: ['I-ADD03-T51-RENDERINGS']

### ADD-03:7.2 (clause, p3) — answered
- source: “Table 5-1 is issued in the Arabic language. The Arabic text governs. The English translation at Appendix B is provided for convenience only.”
- transition: `ADD-03/7.2` amendment_op annotate ADD-03:p4-image, ADD-03:T5-1 effect interprets
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The evidence never states that ADD-03:T5-1 is Appendix B. It is inferred from the English table text. A person should confirm it.
    - concern: The Arabic reading (th-left) is pending approval (A2). It does read 'الأرض الطبيعية', natural ground, so F3 follows from it.
    - concern: Section 7.2 and AppA/para1 both support Arabic governing over the English. Whether that precedence settles the specific differences is a human decision.
- transition: `ADD-03/7.2/issue` issue {"text": "The English translation of Table 5-1 (Appendix B) departs materially from the governing Arabic text (Appendix A). (1) Height reference: the Arabic says natural ground level before grading a…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The two differences are supported by the quoted readings. Arabic note 1 covers permanent and temporary structures, including cranes and construction equipment. English note (1) covers permanent structures only. Arabic note 2 measures from natural ground before grading and filling. English note (2) …
    - concern: The claim that cranes in Zone A are limited to 25 m is not backed by any quoted evidence. The Zone A row and its 25 m value are not shown. Verify it against the table.
    - concern: The reference to ADD-03 Q21 is not in the evidence shown.
    - concern: Everything relies on the pending Arabic reading (A2) and on interpretation I1. Both need a person to confirm them.
- transition: `ADD-03/7.2/clar` clarification {"gap": "The governing Arabic Table 5-1 measures height from natural ground level before grading and filling, and applies the limits to temporary structures, cranes and construction equipment. The En…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The gap and the question follow from the quoted Arabic heading and the notes in the related statements.
    - concern: The Zone A 25 m figure is not in the evidence shown.
    - concern: The clarification cut-off date (2026-11-12) and the ADD-03 issue date (2026-11-15) are not in the evidence shown. Treat them as unverified.
    - concern: The proposed question depends on interpretation I1 and on the pending Arabic reading.
  - downstream proposal `DS-ISSUE-RENDERINGS` issue (reading:ADD-03-p4-r1): **conflicting — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
      - concern: The differences on scope (note 1) and datum (note 2) follow from the quotes shown. The note 3 difference ('installation' in the Arabic, 'erected' in the English) is described as slight, and both renderings give thirty days. That is consistent with the statement.
      - concern: The issue refers to the crane and lifting plan (ADD-03 Q21) and to a closed clarification window. Neither appears in the printed evidence.
      - concern: The wording in 7.2 ('The Arabic text governs') is stated neutrally and the decision is left to a person. That is appropriate.

### ADD-03:7.3 (clause, p3) — UNRESOLVED
- source: “A Bidder whose Proposal provides for any structure, plant or equipment at the site exceeding thirty (30) metres in height shall notify the Authority through the Portal, not later than three (3) Working Days before the Proposal Due Date, of the zone of Table 5-1 in which it is to be located and its proposed height.”
- transition: `ADD-03/7.3/row` row_new {"row": {"id": "ADD-03-7.3-01", "group": "ADD-03-7", "scope": ["Bidder", "Proposal"], "requirement": "A Bidder whose Proposal provides for any structure, plant or equipment at the site exceeding thir…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The requirement text is verbatim from ADD-03:7.3.
    - concern: The 23 Nov 2026 date assumes a PDD of 26 Nov 2026 (A1) and that 'Working Days' has no holiday exclusions. Neither the PDD nor the definition of Working Days is shown in the evidence. It is a Thursday under a Mon–Fri week.
    - concern: The note that cranes may count as equipment depends on I1. It is not stated in 7.3 itself.
  - downstream proposal `DS-ROW-73` row_new (date:ADD-03:7.3): **invalid**
  - downstream proposal `DS-EV-HEIGHT-NOTICE` evidence_item (date:ADD-03:7.3): **insufficient_evidence** — held back: no promotable row or activity uses EV-HEIGHT-NOTICE
  - downstream proposal `DS-ACT-HEIGHT-NOTICE` activity (date:ADD-03:7.3): **insufficient_evidence** — held back: rows not promotable: ['ADD-03-7.3-01']

### ADD-03:7.4 (clause, p3) — UNRESOLVED
- source: “Bidders shall reflect Table 5-1 in the Technical Proposal.”
- transition: `ADD-03/7.4/row` row_new {"row": {"id": "ADD-03-7.4-01", "group": "ADD-03-7", "scope": ["Bidder", "Technical Proposal"], "requirement": "Bidders shall reflect Table 5-1 in the Technical Proposal.", "units": ["ADD-03:7.4"], "…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The assessment 'pass_fail' has no support in ADD-03:7.4. The item itself calls it a guess. It should be left unstated or marked unknown, not set to pass_fail.
    - concern: The requirement text is verbatim. The reading 'on the Arabic text' depends on pending interpretation I1.
    - concern: The link to ADD-03/7.1 is reasonable.

### ADD-03:AppA/para1 (paragraph, p4) — answered
- source: “Table 5-1 is reproduced below as issued by the Northern Region Airspace Safeguarding Office. The Arabic text governs in accordance with Section 7 of this Addendum.”
- transition: `ADD-03/AppA/para1` amendment_op annotate ADD-03:p4-image effect confirms
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The paragraph says the Arabic text governs in accordance with Section 7. Annotating the p4-image with 'confirms' is consistent with that.
    - concern: It adds no new obligation. Whether this is a precedence question is for a person to confirm.

### ADD-03:p4-image/hdr-en (reading_block, p4) — UNRESOLVED
- source: “Northern Region Airspace Safeguarding Office”
- transition: `ADD-03/p4-image/hdr-en` disposition no_effect: English letterhead of the issuing office ('Northern Region Airspace Safeguarding Office'); it identifies the issuer and changes, obliges or excepts nothing.
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading ADD-03-p4-r1 is still pending approval, so the text is not yet confirmed.
    - concern: The no_effect conclusion rests on interpretation I1, which a person must confirm.
  - downstream proposal `DS-ADD03-ESC-P4-HDR-EN` escalation (esc:ADD-03:p4-image/hdr-en): **escalated**

### ADD-03:p4-image/hdr-ar (reading_block, p4) — UNRESOLVED
- source: “مكتب حماية المجال الجوي بالمنطقة الشمالية”
- transition: `ADD-03/p4-image/hdr-ar` disposition no_effect: Arabic letterhead of the issuing office ('مكتب حماية المجال الجوي بالمنطقة الشمالية'); it identifies the issuer only and changes, obliges or excepts nothing.
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading ADD-03-p4-r1 is still pending approval.
    - concern: The no_effect conclusion rests on interpretation I1, which a person must confirm.
  - downstream proposal `DS-ADD03-ESC-P4-HDR-AR` escalation (esc:ADD-03:p4-image/hdr-ar): **escalated**

### ADD-03:p4-image/date (reading_block, p4) — UNRESOLVED
- source: “التاريخ: ١٠ نوفمبر ٢٠٢٦م”
- transition: `ADD-03/p4-image/date` disposition no_effect: Date line of the reproduced letter ('التاريخ: ١٠ نوفمبر ٢٠٢٦م'); it records the letter's date and sets no deadline, milestone or obligation in the pack.
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.; I did not find the ADD-03 issue date, so I could not check whether the letter date of 10 November 2026 is consistent with it.
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: The letter date (10 Nov 2026) could not be compared with the ADD-03 issue date, and the evidence does not show that date. It is later than today's date of 2026-10-05, which a person may want to check.
    - concern: The date is a bare identifier with no deadline wording, so no_effect follows from its words.
  - downstream proposal `DS-ADD03-ESC-P4-DATE` escalation (esc:ADD-03:p4-image/date): **escalated**

### ADD-03:p4-image/ref (reading_block, p4) — UNRESOLVED
- source: “الرقم: ٤٧١/٢٠٢٦”
- transition: `ADD-03/p4-image/ref` disposition no_effect: Reference number of the reproduced letter ('الرقم: ٤٧١/٢٠٢٦'); it is an identifier only and changes, obliges or excepts nothing.
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: The no_effect conclusion rests on interpretation I1, which a person must confirm.
  - downstream proposal `DS-ADD03-ESC-P4-REF` escalation (esc:ADD-03:p4-image/ref): **escalated**

### ADD-03:p4-image/subject (reading_block, p4) — UNRESOLVED
- source: “الموضوع: اشتراطات الارتفاعات لموقع محطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان”
- transition: `ADD-03/p4-image/subject` disposition no_effect: Subject line of the letter ('الموضوع: اشتراطات الارتفاعات لموقع محطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان'); it describes what the letter is about. T…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: The subject line is a heading with no obligation. Clause 7.1 text is verbatim, but only a fragment is shown, so the claim that 7.1 inserts Volume II Clause 5.6 is not checkable here.
  - downstream proposal `DS-ADD03-ESC-P4-SUBJECT` escalation (esc:ADD-03:p4-image/subject): **escalated**

### ADD-03:p4-image/tender-ref (reading_block, p4) — UNRESOLVED
- source: “مناقصة رقم: NUPA/ISTP/2026/014”
- transition: `ADD-03/p4-image/tender-ref` disposition no_effect: Tender reference line ('مناقصة رقم: NUPA/ISTP/2026/014'); it identifies the tender the letter concerns and changes, obliges or excepts nothing.
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: The match with the pack's tender ID is asserted by the proposer. It is not shown in the evidence printed here, but it does not affect the no_effect conclusion.
  - downstream proposal `DS-ADD03-ESC-P4-TENDERREF` escalation (esc:ADD-03:p4-image/tender-ref): **escalated**

### ADD-03:p4-image/table-title (reading_block, p4) — UNRESOLVED
- source: “جدول ٥-١: الحدّ الأقصى لارتفاع المنشآت والمعدّات في الموقع”
- transition: `ADD-03/p4-image/table-title` disposition no_effect: Title of Table 5-1 ('جدول ٥-١: الحدّ الأقصى لارتفاع المنشآت والمعدّات في الموقع'); it is a caption. The limits are in the table rows and are incorporated by AD…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: The no_effect conclusion rests on interpretation I2, which a person must confirm. The table rows that carry the limits are not in this evidence.
  - downstream proposal `DS-ESC-TABLE-TITLE` escalation (esc:ADD-03:p4-image/table-title): **escalated**

### ADD-03:p4-image/table-intro (reading_block, p4) — UNRESOLVED
- source: “يُحدِّد الحدّ الأقصى المسموح به للارتفاع في كل منطقة من مناطق الموقع على النحو الآتي:”
- transition: `ADD-03/p4-image/table-intro` disposition no_effect: Lead-in sentence ('يُحدِّد الحدّ الأقصى المسموح به للارتفاع في كل منطقة من مناطق الموقع على النحو الآتي:') that introduces the table 'as follows'. It has no sh…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval. The reading flags as uncertain whether the first word is active يُحدِّد or passive يُحدَّد; either way the sentence only introduces t…
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval. The proposer flags the first word as uncertain between active يُحدِّد and passive يُحدَّد.
    - concern: The sentence says the maximum permitted height in each zone is set 'as follows', so it has some declarative content. It states no limit itself, and the limits sit in the rows and in Clause 7.1. The no_effect call is reasonable, but a person should confirm it as the proposer says.
    - concern: The table rows are not in this evidence, so it cannot be checked that the intro adds nothing to them.
  - downstream proposal `DS-ESC-TABLE-INTRO` escalation (esc:ADD-03:p4-image/table-intro): **escalated**

### ADD-03:p4-image/th-left (reading_block, p4) — answered
- source: “الإنارة التحذيرية الحدّ الأقصى للارتفاع (متر فوق منسوب الأرض الطبيعية)”
- transition: `ADD-03/p4-image/th-left` disposition no_effect: Column headings of Table 5-1 only ('الإنارة التحذيرية' and 'الحدّ الأقصى للارتفاع (متر فوق منسوب الأرض الطبيعية)'): they print no change, obligation or excepti…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- transition: `ADD-03/p4-image/th-left/issue` issue {"text": "Height datum conflict in Table 5-1: the governing Arabic heading measures maximum height in metres above natural ground level ('متر فوق منسوب الأرض الطبيعية'), while the English convenience…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The consequence about site filling reducing available height is an inference. It is not printed in the evidence, though it follows from the datum difference.
    - concern: The quote shown for 7.2 is only 'The Arabic text governs.' The 'convenience only' wording for Appendix B is cited in F1 but is not in the quoted span.

### ADD-03:p4-image/th-right (reading_block, p4) — answered
- source: “الوصف المنطقة”
- transition: `ADD-03/p4-image/th-right` disposition no_effect: Column headings 'الوصف' (Description) and 'المنطقة' (Zone) of Table 5-1 only: no change, obligation or exception is printed and no volume unit is amended; the …
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5

### ADD-03:p4-image/row-a-left (reading_block, p4) — answered
- source: “مطلوبة”
- transition: `ADD-03/p4-image/row-a-left/disposition` disposition no_effect: Amends no volume unit: the cell 'مطلوبة' (required) is part of Table 5-1, which enters Volume II only through new Clause 5.6 inserted by ADD-03:7.1 ('is incorp…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- transition: `ADD-03/p4-image/row-a-left` row_new {"row": {"id": "ADD-03-T5-1-ZONE-A-LIGHTING", "group": "height-of-structures", "scope": ["site"], "requirement": "Zone A (the part of the site within 1,500 m of the eastern site boundary): obstacle w…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The cell text alone does not tie the cell to Zone A. That link rests on row alignment in the image crops, which the printed text does not show.

### ADD-03:p4-image/row-a-right (reading_block, p4) — answered
- source: “٢٥ الجزء من الموقع الواقع ضمن مسافة ١٬٥٠٠ متر من الحدّ الشرقي للموقع أ”
- transition: `ADD-03/p4-image/row-a-right/disposition` disposition no_effect: Amends no volume unit: the Zone A cells '٢٥ الجزء من الموقع الواقع ضمن مسافة ١٬٥٠٠ متر من الحدّ الشرقي للموقع أ' are part of Table 5-1, which enters Volume II …
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- transition: `ADD-03/p4-image/row-a-right` row_new {"row": {"id": "ADD-03-T5-1-ZONE-A-HEIGHT", "group": "height-of-structures", "scope": ["site"], "requirement": "Zone A (the part of the site within 1,500 m of the eastern site boundary): maximum heig…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The 25 m limit depends on the natural-ground-level datum (I2), which is a pending human decision. The row correctly notes the conflict with the English text.

### ADD-03:p4-image/row-b-left (reading_block, p4) — answered
- source: “مطلوبة لأي جزء يزيد ارتفاعه على ٣٠ متراً ٤٠”
- transition: `ADD-03/p4-image/row-b-left/disposition` disposition no_effect: Amends no volume unit: the Zone B cells 'مطلوبة لأي جزء يزيد ارتفاعه على ٣٠ متراً ٤٠' are part of Table 5-1, which enters Volume II only through new Clause 5.6…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- transition: `ADD-03/p4-image/row-b-left` row_new {"row": {"id": "ADD-03-T5-1-ZONE-B", "group": "height-of-structures", "scope": ["site"], "requirement": "Zone B (the remainder of the site): maximum height of structures and equipment 40 m above natu…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The reading merges the lighting cell and the height cell into one string. Assigning 40 as the height and 30 m as the lighting threshold follows from the crops, not from the text alone.

### ADD-03:p4-image/row-b-right (reading_block, p4) — answered
- source: “باقي مساحة الموقع ب”
- transition: `ADD-03/p4-image/row-b-right` disposition no_effect: Zone label and description only ('باقي مساحة الموقع ب', the remainder of the site, Zone B): it prints no change, obligation or exception of its own and amends …
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5

### ADD-03:p4-image/notes-head (reading_block, p4) — answered
- source: “ملاحظات:”
- transition: `ADD-03/p4-image/notes-head` disposition no_effect: The heading 'ملاحظات:' (Notes:) introduces the notes to Table 5-1; it prints no change, obligation or exception and amends no volume unit.
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5

### ADD-03:p4-image/note1 (reading_block, p4) — answered
- source: “١. تسري هذه الحدود على جميع المنشآت الدائمة والمؤقتة، بما في ذلك المداخن والرافعات ومعدّات الإنشاء.”
- transition: `ADD-03/p4-image/note1/disposition` disposition no_effect: Amends no volume unit: the note 'تسري هذه الحدود على جميع المنشآت الدائمة والمؤقتة' is part of Table 5-1, which enters Volume II only through new Clause 5.6 in…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- transition: `ADD-03/p4-image/note1` row_new {"row": {"id": "ADD-03-T5-1-NOTE-1-APPLICABILITY", "group": "height-of-structures", "scope": ["site"], "requirement": "The Table 5-1 height limits apply to all permanent and temporary structures, inc…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The row's target is its own provision. The English counterpart is only cited in the confidence reason. This is acceptable, but the Arabic/English difference is carried by the separate issue item.
- transition: `ADD-03/p4-image/note1/issue` issue {"text": "Scope of Table 5-1 note 1 differs between languages: the governing Arabic note applies the height limits to all permanent and temporary structures including stacks, cranes and construction …
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The link to the crane and lifting content of the Technical Proposal is an inference and is not shown in the evidence.

### ADD-03:p4-image/note2 (reading_block, p4) — UNRESOLVED
- source: “٢. يُقاس الارتفاع من منسوب الأرض الطبيعية قبل أعمال التسوية والردم.”
- transition: `ADD-03/p4-image/note2` row_new {"row": {"id": "ADD03-HGT-DATUM", "group": "Height of structures", "scope": ["design", "construction"], "requirement": "Measure the Table 5-1 maximum heights from natural ground level before grading …
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:T5-1/note(2)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Row relies on Arabic governing (7.2), which is a person's decision (I2). The row's own text says the English contradicts it; the conflict with ADD-03:T5-1/note(2) is real.
    - concern: Reading of the image is pending approval; I only have the printed Arabic text, not the crop.
    - concern: The row's mention of the 'Arabic column header' and 'English column header' is not in the evidence shown; I could not verify it.
    - concern: Clause 5.6 and 7.1 incorporation: 7.1 text says Table 5-1 is incorporated by reference; reference to 'Clause 5.6' is not in the evidence shown.
- transition: `ADD-03/p4-image/note2-issue` issue {"text": "The height datum differs between the governing Arabic Table 5-1 and its English convenience translation. Arabic note 2 measures height from natural ground level before grading and filling. …
  - validation: **conflicting — HUMAN DECISION PENDING** — declared_conflicts: the proposer declares: ADD-03:T5-1/note(2)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The conflict is real: Arabic says natural ground before grading and filling; English says finished ground after grading and filling.
    - concern: The claim about the English column header is not in the evidence shown; I could not verify it.
    - concern: The issue's consequence (English-based designs could exceed limits where fill raises ground) follows from the words, assuming Arabic governs. Which clause governs is a human decision.
  - downstream proposal `DS-ESC-P4-NOTE2` escalation (esc:ADD-03:p4-image/note2): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
      - concern: The conflict is real: Arabic note 2 says natural ground before grading and filling, and English note (2) says finished ground after grading and filling.
      - concern: The claim that the Arabic column heading also says natural ground rests on a statement quote. The item's own evidence list quotes only note 2 and the English note.
      - concern: The 'clarification window has closed' claim is not shown in the printed evidence. It does not change the conflict.

### ADD-03:p4-image/note3 (reading_block, p4) — UNRESOLVED
- source: “٣. يجب إخطار المكتب قبل ثلاثين (٣٠) يوماً على الأقل من تركيب أي رافعة في الموقع.”
- transition: `ADD-03/p4-image/note3` row_new {"row": {"id": "ADD03-HGT-CRANE-NOTICE", "group": "Height of structures", "scope": ["construction"], "requirement": "Notify the Northern Region Airspace Safeguarding Office at least thirty (30) days …
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Arabic text supports a 30-day prior notice to the Office for any crane installed on the site; the row matches that.
    - concern: Calendar vs Working Days is unstated; the row correctly leaves this open.
    - concern: The Office is named in the row as the Northern Region Airspace Safeguarding Office; the Arabic says only 'المكتب' (the Office). The name comes from 7.1, which is plausible but an inference.
    - concern: The rationale says the note is consistent with English note (3); that English note is not in the evidence shown, so I could not check it.
    - concern: Binding via Clause 5.6 is not shown in the evidence; 7.1 incorporates Table 5-1 by reference.

### ADD-03:p4-image/signatory (reading_block, p4) — answered
- source: “مدير المكتب”
- transition: `ADD-03/p4-image/signatory` disposition no_effect: This is the issuing office's signature block. The image prints only the title 'مدير المكتب' above a drawn signature stroke with no legible name. It prints no c…
  - validation: **evidence_verified**

### ADD-03:p4-image/stamp (reading_block, p4) — answered
- source: “”
- transition: `ADD-03/p4-image/stamp` disposition no_effect: This is an empty stamp outline (an oval) with no legible text. The unit's source text is empty, and it prints no change, obligation or exception.
  - validation: **evidence_verified**

### ADD-03:AppA/para2 (paragraph, p4) — answered
- source: “End of reproduction.”
- transition: `ADD-03/AppA/para2` disposition no_effect: 'End of reproduction.' only marks the end of the reproduced Arabic letter. It prints no change, obligation or exception.
  - validation: **evidence_verified**

### ADD-03:AppB/para1 (paragraph, p5) — answered
- source: “This translation is provided for convenience only. The Arabic text of Table 5-1 at Appendix A governs.”
- transition: `ADD-03/AppB/para1` disposition no_effect: This paragraph restates Clause 7.2 ('The Arabic text governs. The English translation at Appendix B is provided for convenience only.') in the words 'This tran…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'provided')

### ADD-03:T5-1/a (table_row, p5) — answered
- source: “Zone: A | Description: The part of the site within 1,500 m of the eastern site boundary | Maximum height (m above finished ground level): 25 | Obstacle lighting: Required”
- transition: `ADD-03/T5-1/a` disposition no_effect: Row A of the English translation ('The part of the site within 1,500 m of the eastern site boundary', height '25', obstacle lighting 'Required') sits in Append…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'Required')
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Controller semantic check flagged 'Required' as amendment-like language; a person must confirm no_effect.
    - concern: Relies on pending Arabic readings (A1) and interpretation I1.
    - concern: The reason text mentions the datum discrepancy in the column heading, which is not part of row A's own text; this is peripheral but accurate per the Arabic heading reading.

### ADD-03:T5-1/b (table_row, p5) — answered
- source: “Zone: B | Description: The remainder of the site | Maximum height (m above finished ground level): 40 | Obstacle lighting: Required for any part exceeding 30 m”
- transition: `ADD-03/T5-1/b` disposition no_effect: Row B of the English translation ('The remainder of the site', height '40', obstacle lighting 'Required for any part exceeding 30 m') sits in Appendix B, which…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'Required')
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Controller semantic check flagged 'Required' as amendment-like language; a person must confirm.
    - concern: Relies on pending Arabic readings (A1) and interpretation I1.

### ADD-03:T5-1/notes (note_intro, p5) — answered
- source: “Notes to Table 5-1:”
- transition: `ADD-03/T5-1/notes` disposition no_effect: A heading only ('Notes to Table 5-1:') in the convenience translation; it prints no change, obligation or exception. ADD-03:7.2: 'The English translation at Ap…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Heading only; depends on I1 which a person must confirm.

### ADD-03:T5-1/note(1) (note, p5) — UNRESOLVED
- source: “(1) These limits apply to all permanent structures, including stacks.”
- transition: `ADD-03/T5-1/note(1)` disposition no_effect: English convenience translation of Arabic note 1; ADD-03:7.2: 'The Arabic text governs. The English translation at Appendix B is provided for convenience only.…
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:p4-image/note1
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
    - concern: The English and Arabic note 1 conflict on scope, as the item states; the conflict is real on the quoted text (permanent only vs permanent and temporary including cranes and equipment).
    - concern: Depends on the pending Arabic reading (A1).
    - concern: The no_effect disposition rests on the Arabic governing (7.2). That makes the Arabic scope the operative one, handled elsewhere.
- transition: `ADD-03/T5-1/note(1)/issue` issue {"text": "The English translation of Table 5-1 note (1) limits the height limits to 'all permanent structures, including stacks', but the governing Arabic note 1 applies them to all permanent and tem…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Target ADD-03:p4-image/note1 is not among the cited units but is the right counterpart.
    - concern: The claim about the 25/40 m limits applying to cranes follows from the Arabic reading only, which is pending (A1).
    - concern: The reference to 'the crane and lifting plan that Q21 requires' is not supported by any evidence shown here.
- transition: `ADD-03/T5-1/note(1)/clar` clarification {"gap": "The English note (1) of Table 5-1 (permanent structures only) differs from the governing Arabic note 1 (permanent and temporary structures, including cranes and construction equipment).", "p…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The question follows from the discrepancy. Its evidence list quotes only the English note, not the Arabic. The Arabic is covered through F5.
    - concern: Depends on the pending Arabic reading (A1/I2).
  - downstream proposal `DS-ESC-T51-NOTE1` escalation (esc:ADD-03:T5-1/note(1)): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
      - concern: The conflict is real: Arabic note 1 covers permanent and temporary structures, including cranes and equipment, while English note (1) covers permanent structures including stacks.
      - concern: The link to the crane and lifting plan in ADD-03 Q21 is not supported by anything printed in the request. It is context only.
      - concern: The 'clarification window has closed' claim is likewise not shown in the printed evidence.

### ADD-03:T5-1/note(2) (note, p5) — UNRESOLVED
- source: “(2) Height is measured from finished ground level after grading and filling.”
- transition: `ADD-03/T5-1/note(2)` disposition no_effect: English convenience translation of Arabic note 2; ADD-03:7.2: 'The Arabic text governs. The English translation at Appendix B is provided for convenience only.…
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:p4-image/note2; ADD-03:p4-image/th-left
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
    - concern: The datum conflict is real on the quoted text: English 'finished ground level after grading and filling' vs Arabic 'natural ground level before grading and filling'.
    - concern: The claim about the English column heading is not shown in the evidence here; only the Arabic heading reading is printed.
    - concern: Depends on the pending Arabic readings (A1).
- transition: `ADD-03/T5-1/note(2)/issue` issue {"text": "The English translation of Table 5-1 (note (2) and the height column heading) measures height from finished ground level after grading and filling. The governing Arabic measures it from nat…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The consequence about fill reducing and cut increasing usable height follows logically from the datum change, but is not printed in the evidence.
    - concern: Depends on the pending Arabic readings (A1).
    - concern: The English column heading text is not shown, only the note; the unit text for the heading is not in the evidence.
- transition: `ADD-03/T5-1/note(2)/clar` clarification {"gap": "Height datum: English note (2) and the column heading use finished ground level after grading and filling; the governing Arabic uses natural ground level before grading and filling.", "propo…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The question follows from the discrepancy and is reasonable.
    - concern: Its evidence quotes only the English note; the Arabic is covered through F6.
    - concern: Depends on the pending Arabic readings (A1/I2).
  - downstream proposal `DS-ESC-T51-NOTE2` escalation (esc:ADD-03:T5-1/note(2)): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
      - concern: The conflict is real and no datum is chosen.
      - concern: The th-left quote in this item's evidence reads 'الإنارة التحذيرية الحدّ الأقصى للارتفاع (…)'. It includes extra words, apparently a neighbouring 'warning lighting' column heading. The same unit is quoted without those words in statement S-F-NOTE2-AR. The person should check the crop to confirm whi…
      - concern: The th-left unit text is not printed in the units section, so I could not check it independently.

### ADD-03:T5-1/note(3) (note, p5) — UNRESOLVED
- source: “(3) The Office shall be notified at least thirty (30) days before any crane is erected at the site.”
- transition: `ADD-03/T5-1/note(3)` disposition no_effect: No volume unit is amended. 'The Office shall be notified at least thirty (30) days before any crane is erected at the site.' is a free-standing obligation of t…
  - validation: **insufficient_evidence** — dependencies: unknown ids ['ADD-03/T5-1/note(3)/row']
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Controller status is insufficient_evidence: the dependency 'ADD-03/T5-1/note(3)/row' is an unknown id for the controller.
    - concern: The semantic check flags the words 'be notified' and 'shall' as obligation language, so no_effect needs human confirmation.
    - concern: The disposition no_effect is paired with a row_new that carries the same obligation. This is a coherent split only if the person accepts it, and the row_new item is itself pending.
    - concern: It relies on the Arabic note 3 (F7), which is pending (A1). The F7 quote is not cited in the item's own evidence, which has only the English span.
- transition: `ADD-03/T5-1/note(3)/row` row_new {"row": {"id": "ADD-03-T5-1-N3", "group": "Height of structures", "scope": ["post_award"], "requirement": "The Office shall be notified at least thirty (30) days before any crane is erected at the si…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The English and Arabic note 3 agree on the 30-day notice for crane erection/installation (Arabic 'تركيب' = install; English 'erected').
    - concern: The row's assertion that the obligation 'falls to the Project Company through Clause 5.6' is an interpretation; the notifying party is not named. Clause 5.6/7.1 text says the Project Company shall comply with the Table 5-1 height limits, which does not itself clearly assign the notice duty.
    - concern: The row is derived from the English convenience translation, which is not governing. It could duplicate a row from the Arabic note 3 batch.
    - concern: Scope 'post_award' and the 'none_stated' consequence are not contradicted by the evidence shown.
    - concern: Depends on pending Arabic reading (A1).
  - downstream proposal `DS-ESC-T51-NOTE3` escalation (esc:ADD-03:T5-1/note(3)): **escalated**

## Downstream proposals (validated in the candidate)

| Item | Type | Task | Status | First failed check, or what a person confirms |
|---|---|---|---|---|
| P-ADD03-VOL-I-10.3-01 | row_reading | row:VOL-I-10.3-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| P-ADD03-VOL-I-10.3-02 | row_reading | row:VOL-I-10.3-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| P-ADD03-VOL-I-6.1-01 | row_reading | row:VOL-I-6.1-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| P-ADD03-VOL-I-6.2-01 | row_reading | row:VOL-I-6.2-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| P-ADD03-VOL-I-6.2-02 | row_reading | row:VOL-I-6.2-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| P-ADD03-ROW-2.1-01 | row_new | row:VOL-I-6.7-01 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words withdraws a question ('Withdrawal'); its own words decides which clause governs ('governs') |
| P-ADD03-ISSUE-6.6-SUBSTANCE | issue | row:VOL-I-6.7-01 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words decides which clause go… |
| P-ADD03-CQ-6.6 | clarification_item | row:VOL-I-6.7-01 | insufficient_evidence | clarify.check: CQ-ADD03-6.6-CUTOFF: not verbatim in VOL-I:6.6: 'may modify its Proposal not later than two (2) Working Days before the Proposal ' |
| P-ADD03-VOL-I-8.3-01 | row_reading | row:VOL-I-8.3-01 | insufficient_evidence | missing_information: the proposer declares missing: whether the proposed EPC Contractor is an unincorporated joint venture, and its members (bidder fact) |
| P-ADD03-VOL-I-9.6-01 | row_reading | row:VOL-I-9.6-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| P-ADD03-VOL-I-9.7-01 | row_reading | row:VOL-I-9.7-01 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words declares a matter settled ('settled'); its own words decides which clause governs ('governs') |
| P-ADD03-VOL-II-3.1-01 | row_reading | row:VOL-II-3.1-01 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words interprets a term (legal or commercial interpretation) ('are to be read') |
| P-ADD03-VOL-II-3.4-01 | row_reading | row:VOL-II-3.4-01 | conflicting | declared_conflicts: the proposer declares: ADD-03:5.1 substitution not applied in units_after |
| P-ADD03-ESC-ODOUR | escalation | row:VOL-II-3.4-01 | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| P-ADD03-ISSUE-ODOUR | issue | row:VOL-II-3.4-01 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| P-ADD03-DEP-ESIA | dependency | row:VOL-II-3.4-01 | invalid | relationships.validate: missing_document needs `document_id` (the document, a short id, the conclusion it blocks) |
| P-ADD03-VOL-II-6.4-01 | row_reading | row:VOL-II-6.4-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-001 | row_reading | row:VOL-II-6.4-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-002 | row_reading | row:VOL-IV-F4A-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-003 | row_reading | row:VOL-IV-F4A-02 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words declares a matter resolved ('resolved') |
| DS-ADD03-004 | row_reading | row:VOL-IV-F4E-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-005 | row_reading | row:VOL-IV-F4F-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-006 | row_reading | row:VOL-IV-F4F-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-007 | row_reading | row:VOL-V-29.2-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-008 | row_new | c46:ADD-03/2.1(a) | invalid — HUMAN DECISION PENDING | id: row id ADD-03-2.1-01 already exists or was listed before (id ledger) |
| DS-ADD03-009 | issue | c46:ADD-03/2.1(a) | invalid — HUMAN DECISION PENDING | id: issue id I-ADD03-6.6-SUBSTANCE is not a new I-... id |
| DS-ADD03-010 | row_new | c46:ADD-03/3.2 | invalid | register: the row does not evaluate: ValueError: rule ADD-03-3.2-01-base-date: kind 'deadline' not in ('anchor', 'relative', 'fixed', 'as_at', 'external', 'unresolved') |
| DS-ADD03-011 | row_new | c46:ADD-03/7.1 | insufficient_evidence — HUMAN DECISION PENDING | missing_information: the proposer declares missing: Table 5-1 height values (Arabic image reading, approval by a person) |
| DS-ADD03-012 | clarification_item | clar:CQ-VOL-V-SCHEDULES | insufficient_evidence — HUMAN DECISION PENDING | clarify.check: CQ-VOL-V-SCHEDULES: not verbatim in VOL-V:29.2: 'The Availability Payment shall be indexed annually from the Base Date in accorda' |
| DS-ADD03-013 | activity | act:fin-model-build | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| DS-ADD-03-01 | activity | act:fin-model-freeze | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| DS-ADD-03-02 | no_change | act:model-auditor-appoint | interpretation_pending |  |
| DS-ADD-03-03 | no_change | act:model-audit-review | interpretation_pending |  |
| DS-ADD-03-04 | no_change | act:model-audit-opinion | interpretation_pending |  |
| DS-ADD-03-05 | no_change | act:deliver | interpretation_pending |  |
| DS-ADD-03-06 | no_change | act:seal-and-mark | interpretation_pending |  |
| DS-ADD-03-07 | no_change | act:copies | interpretation_pending |  |
| DS-ADD-03-08 | activity | act:assemble-envelope-a | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| DS-ADD-03-09 | no_change | act:assemble-envelope-b | interpretation_pending |  |
| DS-ADD-03-10 | activity | act:iso-copy | insufficient_evidence | missing_information: the proposer declares missing: Whether the proposed EPC Contractor is an unincorporated joint venture, and how many members it has (bidder fact; insufficient evidence in the pack) |
| DS-ADD-03-11 | activity | act:deviations-review | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| DS-ADD-03-12 | no_change | act:form-4e | interpretation_pending |  |
| DS-ADD03-ACT-TP | activity | act:technical-proposal | insufficient_evidence | missing_information: the proposer declares missing: The content of Table 5-1 depends on image reading ADD-03-p4-r1, which is pending approval.; ESIA Figure 7-2 (the odour value at the receptor) is no… |
| DS-ADD03-ACT-4A-PREP | no_change | act:form-4a-prep | interpretation_pending |  |
| DS-ADD03-ACT-4A | no_change | act:form-4a | interpretation_pending |  |
| DS-ADD03-ACT-4F | activity | act:form-4f | insufficient_evidence | missing_information: the proposer declares missing: The price basis of the Form 4-F Availability Payment (year 1 prices under Q19, or Base Date prices under ADD-03 3.1) is escalated under esc:ADD-03:… |
| DS-ADD03-ESC-51 | escalation | esc:ADD-03:5.1 | conflicting | declared_conflicts: the proposer declares: ADD-03/5.1; ADD-03/5.2; ADD-03/Q18 |
| DS-ADD03-DEP-51-FIG72 | dependency | esc:ADD-03:5.1 | invalid | missing_information: the proposer declares missing: ESIA Figure 7-2 |
| DS-ADD03-ESC-Q19 | escalation | esc:ADD-03:Q19 | conflicting | declared_conflicts: the proposer declares: ADD-03/Q19; ADD-03/3.1; ADD-03/3.3 |
| DS-ADD03-ISSUE-AP-BASIS | issue | esc:ADD-03:Q19 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words declares a matter close… |
| DS-ADD03-ESC-P4-HDR-EN | escalation | esc:ADD-03:p4-image/hdr-en | escalated | missing_information: the proposer declares missing: Approval of reading ADD-03-p4-r1 |
| DS-ADD03-ESC-P4-HDR-AR | escalation | esc:ADD-03:p4-image/hdr-ar | escalated | missing_information: the proposer declares missing: Approval of reading ADD-03-p4-r1 |
| DS-ADD03-ESC-P4-DATE | escalation | esc:ADD-03:p4-image/date | escalated | missing_information: the proposer declares missing: Approval of reading ADD-03-p4-r1; ADD-03 issue date |
| DS-ADD03-ESC-P4-REF | escalation | esc:ADD-03:p4-image/ref | escalated | missing_information: the proposer declares missing: Approval of reading ADD-03-p4-r1 |
| DS-ADD03-ESC-P4-SUBJECT | escalation | esc:ADD-03:p4-image/subject | escalated | missing_information: the proposer declares missing: Approval of reading ADD-03-p4-r1 |
| DS-ADD03-ESC-P4-TENDERREF | escalation | esc:ADD-03:p4-image/tender-ref | escalated | missing_information: the proposer declares missing: Approval of reading ADD-03-p4-r1 |
| DS-ESC-TABLE-TITLE | escalation | esc:ADD-03:p4-image/table-title | escalated | missing_information: the proposer declares missing: approval of reading ADD-03-p4-r1 |
| DS-ESC-TABLE-INTRO | escalation | esc:ADD-03:p4-image/table-intro | escalated | missing_information: the proposer declares missing: approval of reading ADD-03-p4-r1; reviewer check of the mark under the shadda on the first word |
| DS-ESC-P4-NOTE2 | escalation | esc:ADD-03:p4-image/note2 | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(2) |
| DS-ESC-T51-NOTE1 | escalation | esc:ADD-03:T5-1/note(1) | conflicting | declared_conflicts: the proposer declares: ADD-03:p4-image/note1 |
| DS-ESC-T51-NOTE2 | escalation | esc:ADD-03:T5-1/note(2) | conflicting | declared_conflicts: the proposer declares: ADD-03:p4-image/note2; ADD-03:p4-image/th-left |
| DS-ESC-T51-NOTE3 | escalation | esc:ADD-03:T5-1/note(3) | escalated | missing_information: the proposer declares missing: approval of reading ADD-03-p4-r1 |
| DS-ESC-REREAD-Q1 | escalation | reread:ADD-01:Q1 | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-ESC-REREAD-Q6 | escalation | reread:ADD-01:Q6 | escalated | the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person |
| DS-ROW-P4-01 | row_new | reading:ADD-03-p4-r1 | insufficient_evidence | held back: issue references not among the promoted issues: ['I-ADD03-T51-RENDERINGS'] |
| DS-ROW-P4-02 | row_new | reading:ADD-03-p4-r1 | insufficient_evidence | held back: issue references not among the promoted issues: ['I-ADD03-T51-RENDERINGS'] |
| DS-ROW-P4-03 | row_new | reading:ADD-03-p4-r1 | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(1) |
| DS-ROW-P4-04 | row_new | reading:ADD-03-p4-r1 | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(2) |
| DS-ROW-P4-05 | row_new | reading:ADD-03-p4-r1 | insufficient_evidence | held back: issue references not among the promoted issues: ['I-ADD03-T51-RENDERINGS'] |
| DS-ISSUE-RENDERINGS | issue | reading:ADD-03-p4-r1 | conflicting — HUMAN DECISION PENDING | declared_conflicts: the proposer declares: ADD-03:T5-1/note(1); ADD-03:T5-1/note(2) |
| DS-ROW-73 | row_new | date:ADD-03:7.3 | invalid | register: the row does not evaluate: ValueError: rule ADD-03-7.3-01-height-notice: kind 'deadline' not in ('anchor', 'relative', 'fixed', 'as_at', 'external', 'unresolved') |
| DS-EV-HEIGHT-NOTICE | evidence_item | date:ADD-03:7.3 | insufficient_evidence | held back: no promotable row or activity uses EV-HEIGHT-NOTICE |
| DS-ACT-HEIGHT-NOTICE | activity | date:ADD-03:7.3 | insufficient_evidence | held back: rows not promotable: ['ADD-03-7.3-01'] |
| DS-RR-VOL-II-3.2-01 | row_reading | cond:VOL-II:3.2 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-RR-VOL-II-3.2-02 | row_reading | cond:VOL-II:3.2 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-RR-VOL-V-29.2-01 | row_reading | defn:VOL-V:1.1 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ESC-DEFN-ROWS | escalation | defn:VOL-V:1.1 | escalated | missing_information: the proposer declares missing: the effective text of the units of VOL-I-10.2-01, VOL-I-10.6-01, VOL-I-11.5-01, VOL-IV-F4F-01, VOL-IV-F4F-02 and VOL-V-29.3-01 in units_after |
| D1 | row_new | cons:ADD-03:3.3 | insufficient_evidence — HUMAN DECISION PENDING | missing_information: the proposer declares missing: The pack does not state a consequence for an Indexed Proportion outside the 50% to 70% band. A person decides whether VOL-I 10.5 applies. The clari… |
| D2 | escalation | cons:VOL-V:29.2 | escalated | missing_information: the proposer declares missing: The pack does not state a consequence for an Indexed Proportion outside the 50% to 70% band. |

- interactions: A5 with the proposals: C45: the programme cannot be planned with the proposals: ValueError: rule ADD-03-3.2-01-base-date: kind 'deadline' not in ('anchor', 'relative', 'fixed', 'as_at', 'external', '…
- A5 problems the proposals would add: C45: the programme cannot be planned with the proposals: ValueError: rule ADD-03-3.2-01-base-date: kind 'deadline' not in ('anchor', 'relative', 'fixed', 'as_at', 'external', 'unresolved')

## Promoted into the candidate (PROPOSED; nothing accepted)

- ops: ADD-03/cover/para3, ADD-03/2.1(a), ADD-03/2.1(b), ADD-03/3.1, ADD-03/3.2, ADD-03/3.3, ADD-03/3.4, ADD-03/4.1, ADD-03/4.2, ADD-03/5.2, ADD-03/Q15, ADD-03/Q16, ADD-03/Q17, ADD-03/Q18, ADD-03/Q20, ADD-03/Q21, ADD-03/7.1, ADD-03/7.2, ADD-03/AppA/para1
- dispositions: ADD-03:cover/para1: no_effect, ADD-03:cover/para2: no_effect, ADD-03:1.1: no_effect, ADD-03:1.2: no_effect, ADD-03:1.3: no_effect, ADD-03:2.2: no_effect, ADD-03:p4-image/th-left: no_effect, ADD-03:p4-image/th-right: no_effect, ADD-03:p4-image/row-a-left: no_effect, ADD-03:p4-image/row-a-right: no_effect, ADD-03:p4-image/row-b-left: no_effect, ADD-03:p4-image/row-b-right: no_effect, ADD-03:p4-image/notes-head: no_effect, ADD-03:p4-image/note1: no_effect, ADD-03:p4-image/signatory: no_effect, ADD-03:p4-image/stamp: no_effect, ADD-03:AppA/para2: no_effect, ADD-03:AppB/para1: no_effect, ADD-03:T5-1/a: no_effect, ADD-03:T5-1/b: no_effect, ADD-03:T5-1/notes: no_effect
- rows new: ADD-03-2.1-01
- readings: VOL-I-10.3-01, VOL-I-10.3-02, VOL-I-6.1-01, VOL-I-6.2-01, VOL-I-6.2-02, VOL-I-9.6-01, VOL-I-9.7-01, VOL-II-3.1-01, VOL-II-6.4-01, VOL-II-6.4-02, VOL-IV-F4A-01, VOL-IV-F4A-02, VOL-IV-F4E-01, VOL-IV-F4F-01, VOL-IV-F4F-02, VOL-V-29.2-01, VOL-II-3.2-01, VOL-II-3.2-02, VOL-V-29.2-01
- issues: I-ADD03-6.6-SUBSTANCE, I-ADD03-AP-PRICE-BASIS, I-ADD03-ODOUR-OP
- activities: fin-model-build, fin-model-freeze, assemble-envelope-a, deviations-review
- no change: act:model-auditor-appoint, act:model-audit-review, act:model-audit-opinion, act:deliver, act:seal-and-mark, act:copies, act:assemble-envelope-b, act:form-4e, act:form-4a-prep, act:form-4a
- unresolved provisions: 17
- note: rows.yaml: 2 comment line(s) inside row VOL-I-6.1-01 were not kept (the row was rewritten; the file's other comments are kept)

## check-register on the candidate

- exit 1; 4 finding(s) {'disposition': 1, 'assessment': 1, 'C46': 2}
  - [disposition] VOL-I: row ADD-03-2.1-01 uses VOL-I:6.6, whose disposition does not list it as a requirement
  - [assessment] ADD-03-2.1-01: assessment 'procedural', but a breach puts the Proposal out (rejection): pass_fail (ASSESSMENT_WORDS)
  - [C46] ADD-03/3.2: [A1] ADD-03/3.2 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-V:1.1; a row of the anchor VOL-V:1.1 does not count): 'The following…
  - [C46] ADD-03/7.1: [A1] ADD-03/7.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-II:5.5; a row of the anchor VOL-II:5.5 does not count): 'The followi…

## Coverage

- provisions: 57; accounted for by the combined set: 53; states {'validated': 57}
- resolution (controller): resolved 10, pending 43, invalid 0, unaccounted 4; approved 0
- structural units of ADD-03 that are not provisions (listed so nothing is dropped): ADD-03:H:cover (heading), ADD-03:H:cover-2 (heading), ADD-03:H:S1 (heading), ADD-03:H:S2 (heading), ADD-03:H:S3 (heading), ADD-03:H:S4 (heading), ADD-03:H:S5 (heading), ADD-03:H:S6 (heading), ADD-03:S6/QA (table), ADD-03:H:S7 (heading), ADD-03:H:AppA (heading), ADD-03:region:ADD-03-p4-r1 (region), ADD-03:p4-image (image_text), ADD-03:H:AppB (heading), ADD-03:T5-1 (table)
- batches: reading-ADD-03-p4-r1 done, analysis-001 done, analysis-002 done, analysis-003 done, analysis-004 done, analysis-005 done, analysis-006 done, analysis-007 done, analysis-008 done, analysis-009 done, downstream-001 done, downstream-002 done, downstream-003 done, downstream-004 done, downstream-005 done, downstream-006 done

## Critic (a second model over the selected items; it changed no status)

**Agreement between the critic and the proposer is not approval**: every item still needs a person's decision, and a disagreement is a concern for that person, not a rejection. The critic reviews only the selected classes (consequential interpretations, uncertain targets, removals, conflicting evidence), in one request per batch.

| Batch | Critic | Selected | Reviewed | Agrees | Does not agree | Note |
|---|---|---|---|---|---|---|
| analysis-001 | done | 3 | 3 | 3 | 0 |  |
| analysis-002 | done | 5 | 5 | 4 | 1 |  |
| analysis-003 | done | 1 | 1 | 1 | 0 |  |
| analysis-004 | done | 8 | 8 | 7 | 1 |  |
| analysis-005 | done | 7 | 7 | 6 | 1 |  |
| analysis-006 | done | 8 | 8 | 8 | 0 |  |
| analysis-007 | done | 14 | 14 | 14 | 0 |  |
| analysis-008 | done | 3 | 3 | 3 | 0 |  |
| analysis-009 | done | 11 | 11 | 10 | 1 |  |
| downstream-001 | done | 7 | 7 | 7 | 0 |  |
| downstream-002 | not_needed | 0 | - | - | - |  |
| downstream-003 | not_needed | 0 | - | - | - |  |
| downstream-004 | done | 3 | 3 | 3 | 0 |  |
| downstream-005 | done | 6 | 6 | 6 | 0 |  |
| downstream-006 | done | 1 | 1 | 0 | 1 |  |

- **ADD-03/cover/para3** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The VOL-IV Form 4-A group and the ADD-01 Appendix A field text are not printed in the units. I relied on the controller's verbatim checks for them.
    - concern: The provision says only 'acknowledge receipt in Form 4-A'. The note's 'Addendum No. 3' and the field reference come from the proposer's reading of the ADD-01 reissue. A person should confirm that the reissued Form 4-A is the current target.
- **ADD-03/2.1(a)** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
    - concern: The new 6.6 adds a modification cut-off of two Working Days before the due date. The old 6.7 allowed modification up to the due date. This is a substantive change, and the cover says 'without change of substance', so the two conflict. A person should review that wording.
    - concern: The 24 November 2026 date relies on the VOL-I 2.4 calendar, which is not printed here. I checked only that 26 Nov 2026 is a Thursday.
- **ADD-03/2.1(b)** (analysis-001; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because removal; model claude-sonnet-5-5
    - concern: Deleting 6.7 is what the provision says. The 6.7 right to modify up to the due date is not carried over unchanged. The new 6.6 narrows it to two Working Days before the due date. The rationale's 'content is absorbed' therefore understates the change. The withdrawal right is kept.
- **ADD-03/3.2** (analysis-002; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: Minor: the new definition is inserted after VOL-V:1.1, which is the Availability Payment definition. This matches the provision's 'after Clause 1.1'.
    - concern: The Base Date is not computed, which is correct, since the Proposal Due Date is not in the evidence.
- **ADD-03/3.3** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
    - concern: The printed 3.3 text ends at '(a)...; and'. Part (b) and the closing 'balance remain fixed' come from ADD-03:3.3(b), which is not in the units list. The controller verified it as verbatim, so the full replacement is supported.
    - concern: The 60/40 split is removed and replaced by a Bidder-stated 50–70% for years 1–10 and 75% from year 11. 'Deleted and replaced' supports replacing the whole of 29.2, so the old text matches the whole target.
    - concern: A person should confirm the old words match the target, as the controller flags.
- **ADD-03/3.3-form** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The claim that Form 4-F has no field for the percentage is not verifiable from the evidence shown. Only one member field is quoted ('Indexation basis assumed: Per Volume V Clause 29.2'). The VOL-IV:F4-F group and its '20 members' are not printed.
    - concern: The claim that ADD-03 Section 3 does not amend Form 4-F is not shown either. Only 3.2, 3.3 and 3.4 are printed, and no unit says Form 4-F is untouched.
    - concern: The quoted evidence does show that the replacement 29.2 refers to a percentage 'stated by the Bidder in Form 4-F'. It also shows an indexation field that merely points to Clause 29.2. The ambiguity is plausible but not proven.
    - concern: The interim handling (state the percentage against the 'Indexation basis assumed' field) is a suggestion, not something the text supports.
- **ADD-03/3.4** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: 'Shall reflect' is obligation wording with no text change, so an annotate with adds_obligation fits.
    - concern: The obligation applies to 'this Section 3', which includes the Base Date and Indexed Proportion changes. Its scope depends on the S6 interpretation, which a person must confirm.
- **ADD-03/4.2** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The target is the group VOL-II:S3, evidenced only by its heading 'SECTION 3 — PROCESS REQUIREMENTS'. This matches the cited 'Volume II Section 3'.
    - concern: The content of ADD-03 Section 4 is not shown, so what the obligation covers cannot be checked.
    - concern: The adds_obligation effect depends on the S6 interpretation, which a person must confirm.
- **ADD-03/5.2** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The clause says "as amended", which points to some amendment of VOL-II 3.4, probably ADD-03/5.1 (listed as a dependency). The evidence shown does not include 5.1, so I could not check that annotating 3.4 without changing its text is right. If 5.1 amends 3.4, a person should check that this annotati…
    - concern: ADD-03:5.2 has status not_issued in the units. The evidence does not say what that means for whether the obligation takes effect. A person should confirm it.
- **ADD-03/Q15** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- **ADD-03/Q16** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: The response also says a 'no deviations' Bidder shall not qualify Volume V elsewhere. This restates VOL-I:9.6 and is only partly captured by the annotation note. It does not change the interpretation.
- **ADD-03/Q17** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- **ADD-03/Q18** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The response refers to the nearest sensitive receptor and 'Clause 3.4 as amended by Section 5'. The printed VOL-II:3.4 sets the limit at the site boundary. ADD-03:5.1 is not in the evidence shown, so I cannot tell whether the measurement point or the 5 OU/m³ figure changes.
    - concern: The 'interprets / no text change' label follows for Q18 alone. The effect on 3.4 depends on Section 5, which is not shown.
    - concern: Figure 7-2 is not in the evidence, so the item correctly states no values.
- **ADD-03/Q19** (analysis-004; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The conflict with ADD-03:3.3 is plausible. 3.3 says 'indexed annually from the Base Date' and Q19 says indexation 'applies from the first anniversary of PCOD'. Only the quoted span of 3.3 is available, not the full unit.
    - concern: The target is the Form 4-F group, and I saw only the quoted label span for the Form 4-F entry.
- **ADD-03/Q19-issue** (analysis-004; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The core tension is supported by the two quoted spans.
    - concern: The claim that the Base Date is 28 days before the Proposal Due Date (ADD-03:3.2) is not supported by any evidence shown.
- **ADD-03/Q20** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The 'Indexed Proportion' is defined in the substituted 29.2 (ADD-03:3.3), which is not shown. The printed 29.2 states 60% and 40%. The item flags the dependency on 3.3.
    - concern: The consequence of stating it in Envelope A follows from VOL-I:6.2, which makes any commercial information in Envelope A non-responsive.
- **ADD-03/Q21** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The crane and lifting plan depends on Clause 5.6 / Table 5-1 from ADD-03:7.1, which is not shown. The item correctly relies on no values from it.
- **ADD-03/7.1** (analysis-005; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: Anchor VOL-II:5.5 is correct: the provision inserts new 5.6 after 5.5 and nothing in 5.5 is changed or removed. The new text matches the quoted clause.
- **ADD-03/7.2** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The evidence never states that ADD-03:T5-1 is Appendix B. It is inferred from the English table text. A person should confirm it.
    - concern: The Arabic reading (th-left) is pending approval (A2). It does read 'الأرض الطبيعية', natural ground, so F3 follows from it.
    - concern: Section 7.2 and AppA/para1 both support Arabic governing over the English. Whether that precedence settles the specific differences is a human decision.
- **ADD-03/7.2/issue** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The two differences are supported by the quoted readings. Arabic note 1 covers permanent and temporary structures, including cranes and construction equipment. English note (1) covers permanent structures only. Arabic note 2 measures from natural ground before grading and filling. English note (2) …
    - concern: The claim that cranes in Zone A are limited to 25 m is not backed by any quoted evidence. The Zone A row and its 25 m value are not shown. Verify it against the table.
    - concern: The reference to ADD-03 Q21 is not in the evidence shown.
    - concern: Everything relies on the pending Arabic reading (A2) and on interpretation I1. Both need a person to confirm them.
- **ADD-03/7.2/clar** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The gap and the question follow from the quoted Arabic heading and the notes in the related statements.
    - concern: The Zone A 25 m figure is not in the evidence shown.
    - concern: The clarification cut-off date (2026-11-12) and the ADD-03 issue date (2026-11-15) are not in the evidence shown. Treat them as unverified.
    - concern: The proposed question depends on interpretation I1 and on the pending Arabic reading.
- **ADD-03/7.3/row** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The requirement text is verbatim from ADD-03:7.3.
    - concern: The 23 Nov 2026 date assumes a PDD of 26 Nov 2026 (A1) and that 'Working Days' has no holiday exclusions. Neither the PDD nor the definition of Working Days is shown in the evidence. It is a Thursday under a Mon–Fri week.
    - concern: The note that cranes may count as equipment depends on I1. It is not stated in 7.3 itself.
- **ADD-03/7.4/row** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The assessment 'pass_fail' has no support in ADD-03:7.4. The item itself calls it a guess. It should be left unstated or marked unknown, not set to pass_fail.
    - concern: The requirement text is verbatim. The reading 'on the Arabic text' depends on pending interpretation I1.
    - concern: The link to ADD-03/7.1 is reasonable.
- **ADD-03/AppA/para1** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The paragraph says the Arabic text governs in accordance with Section 7. Annotating the p4-image with 'confirms' is consistent with that.
    - concern: It adds no new obligation. Whether this is a precedence question is for a person to confirm.
- **ADD-03/p4-image/hdr-en** (analysis-006; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading ADD-03-p4-r1 is still pending approval, so the text is not yet confirmed.
    - concern: The no_effect conclusion rests on interpretation I1, which a person must confirm.
- **ADD-03/p4-image/hdr-ar** (analysis-006; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading ADD-03-p4-r1 is still pending approval.
    - concern: The no_effect conclusion rests on interpretation I1, which a person must confirm.
- **ADD-03/p4-image/date** (analysis-006; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: The letter date (10 Nov 2026) could not be compared with the ADD-03 issue date, and the evidence does not show that date. It is later than today's date of 2026-10-05, which a person may want to check.
    - concern: The date is a bare identifier with no deadline wording, so no_effect follows from its words.
- **ADD-03/p4-image/ref** (analysis-006; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: The no_effect conclusion rests on interpretation I1, which a person must confirm.
- **ADD-03/p4-image/subject** (analysis-006; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: The subject line is a heading with no obligation. Clause 7.1 text is verbatim, but only a fragment is shown, so the claim that 7.1 inserts Volume II Clause 5.6 is not checkable here.
- **ADD-03/p4-image/tender-ref** (analysis-006; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: The match with the pack's tender ID is asserted by the proposer. It is not shown in the evidence printed here, but it does not affect the no_effect conclusion.
- **ADD-03/p4-image/table-title** (analysis-006; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: The no_effect conclusion rests on interpretation I2, which a person must confirm. The table rows that carry the limits are not in this evidence.
- **ADD-03/p4-image/table-intro** (analysis-006; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval. The proposer flags the first word as uncertain between active يُحدِّد and passive يُحدَّد.
    - concern: The sentence says the maximum permitted height in each zone is set 'as follows', so it has some declarative content. It states no limit itself, and the limits sit in the rows and in Clause 7.1. The no_effect call is reasonable, but a person should confirm it as the proposer says.
    - concern: The table rows are not in this evidence, so it cannot be checked that the intro adds nothing to them.
- **ADD-03/p4-image/th-left** (analysis-007; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- **ADD-03/p4-image/th-left/issue** (analysis-007; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The consequence about site filling reducing available height is an inference. It is not printed in the evidence, though it follows from the datum difference.
    - concern: The quote shown for 7.2 is only 'The Arabic text governs.' The 'convenience only' wording for Appendix B is cited in F1 but is not in the quoted span.
- **ADD-03/p4-image/th-right** (analysis-007; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- **ADD-03/p4-image/row-a-left/disposition** (analysis-007; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- **ADD-03/p4-image/row-a-left** (analysis-007; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The cell text alone does not tie the cell to Zone A. That link rests on row alignment in the image crops, which the printed text does not show.
- **ADD-03/p4-image/row-a-right/disposition** (analysis-007; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- **ADD-03/p4-image/row-a-right** (analysis-007; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The 25 m limit depends on the natural-ground-level datum (I2), which is a pending human decision. The row correctly notes the conflict with the English text.
- **ADD-03/p4-image/row-b-left/disposition** (analysis-007; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- **ADD-03/p4-image/row-b-left** (analysis-007; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The reading merges the lighting cell and the height cell into one string. Assigning 40 as the height and 30 m as the lighting threshold follows from the crops, not from the text alone.
- **ADD-03/p4-image/row-b-right** (analysis-007; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- **ADD-03/p4-image/notes-head** (analysis-007; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- **ADD-03/p4-image/note1/disposition** (analysis-007; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- **ADD-03/p4-image/note1** (analysis-007; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The row's target is its own provision. The English counterpart is only cited in the confidence reason. This is acceptable, but the Arabic/English difference is carried by the separate issue item.
- **ADD-03/p4-image/note1/issue** (analysis-007; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The link to the crane and lifting content of the Technical Proposal is an inference and is not shown in the evidence.
- **ADD-03/p4-image/note2** (analysis-008; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Row relies on Arabic governing (7.2), which is a person's decision (I2). The row's own text says the English contradicts it; the conflict with ADD-03:T5-1/note(2) is real.
    - concern: Reading of the image is pending approval; I only have the printed Arabic text, not the crop.
    - concern: The row's mention of the 'Arabic column header' and 'English column header' is not in the evidence shown; I could not verify it.
    - concern: Clause 5.6 and 7.1 incorporation: 7.1 text says Table 5-1 is incorporated by reference; reference to 'Clause 5.6' is not in the evidence shown.
- **ADD-03/p4-image/note2-issue** (analysis-008; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The conflict is real: Arabic says natural ground before grading and filling; English says finished ground after grading and filling.
    - concern: The claim about the English column header is not in the evidence shown; I could not verify it.
    - concern: The issue's consequence (English-based designs could exceed limits where fill raises ground) follows from the words, assuming Arabic governs. Which clause governs is a human decision.
- **ADD-03/p4-image/note3** (analysis-008; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Arabic text supports a 30-day prior notice to the Office for any crane installed on the site; the row matches that.
    - concern: Calendar vs Working Days is unstated; the row correctly leaves this open.
    - concern: The Office is named in the row as the Northern Region Airspace Safeguarding Office; the Arabic says only 'المكتب' (the Office). The name comes from 7.1, which is plausible but an inference.
    - concern: The rationale says the note is consistent with English note (3); that English note is not in the evidence shown, so I could not check it.
    - concern: Binding via Clause 5.6 is not shown in the evidence; 7.1 incorporates Table 5-1 by reference.
- **ADD-03/T5-1/a** (analysis-009; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Controller semantic check flagged 'Required' as amendment-like language; a person must confirm no_effect.
    - concern: Relies on pending Arabic readings (A1) and interpretation I1.
    - concern: The reason text mentions the datum discrepancy in the column heading, which is not part of row A's own text; this is peripheral but accurate per the Arabic heading reading.
- **ADD-03/T5-1/b** (analysis-009; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Controller semantic check flagged 'Required' as amendment-like language; a person must confirm.
    - concern: Relies on pending Arabic readings (A1) and interpretation I1.
- **ADD-03/T5-1/notes** (analysis-009; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Heading only; depends on I1 which a person must confirm.
- **ADD-03/T5-1/note(1)** (analysis-009; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
    - concern: The English and Arabic note 1 conflict on scope, as the item states; the conflict is real on the quoted text (permanent only vs permanent and temporary including cranes and equipment).
    - concern: Depends on the pending Arabic reading (A1).
    - concern: The no_effect disposition rests on the Arabic governing (7.2). That makes the Arabic scope the operative one, handled elsewhere.
- **ADD-03/T5-1/note(1)/issue** (analysis-009; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Target ADD-03:p4-image/note1 is not among the cited units but is the right counterpart.
    - concern: The claim about the 25/40 m limits applying to cranes follows from the Arabic reading only, which is pending (A1).
    - concern: The reference to 'the crane and lifting plan that Q21 requires' is not supported by any evidence shown here.
- **ADD-03/T5-1/note(1)/clar** (analysis-009; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The question follows from the discrepancy. Its evidence list quotes only the English note, not the Arabic. The Arabic is covered through F5.
    - concern: Depends on the pending Arabic reading (A1/I2).
- **ADD-03/T5-1/note(2)** (analysis-009; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
    - concern: The datum conflict is real on the quoted text: English 'finished ground level after grading and filling' vs Arabic 'natural ground level before grading and filling'.
    - concern: The claim about the English column heading is not shown in the evidence here; only the Arabic heading reading is printed.
    - concern: Depends on the pending Arabic readings (A1).
- **ADD-03/T5-1/note(2)/issue** (analysis-009; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The consequence about fill reducing and cut increasing usable height follows logically from the datum change, but is not printed in the evidence.
    - concern: Depends on the pending Arabic readings (A1).
    - concern: The English column heading text is not shown, only the note; the unit text for the heading is not in the evidence.
- **ADD-03/T5-1/note(2)/clar** (analysis-009; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The question follows from the discrepancy and is reasonable.
    - concern: Its evidence quotes only the English note; the Arabic is covered through F6.
    - concern: Depends on the pending Arabic readings (A1/I2).
- **ADD-03/T5-1/note(3)** (analysis-009; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Controller status is insufficient_evidence: the dependency 'ADD-03/T5-1/note(3)/row' is an unknown id for the controller.
    - concern: The semantic check flags the words 'be notified' and 'shall' as obligation language, so no_effect needs human confirmation.
    - concern: The disposition no_effect is paired with a row_new that carries the same obligation. This is a coherent split only if the person accepts it, and the row_new item is itself pending.
    - concern: It relies on the Arabic note 3 (F7), which is pending (A1). The F7 quote is not cited in the item's own evidence, which has only the English span.
- **ADD-03/T5-1/note(3)/row** (analysis-009; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The English and Arabic note 3 agree on the 30-day notice for crane erection/installation (Arabic 'تركيب' = install; English 'erected').
    - concern: The row's assertion that the obligation 'falls to the Project Company through Clause 5.6' is an interpretation; the notifying party is not named. Clause 5.6/7.1 text says the Project Company shall comply with the Table 5-1 height limits, which does not itself clearly assign the notice duty.
    - concern: The row is derived from the English convenience translation, which is not governing. It could duplicate a row from the Arabic note 3 batch.
    - concern: Scope 'post_award' and the 'none_stated' consequence are not contradicted by the evidence shown.
    - concern: Depends on pending Arabic reading (A1).
- **P-ADD03-VOL-I-6.1-01** (downstream-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: VOL-I:6.1 text and the ADD-01 amendment of the date are not printed in the units shown; the date 26 November 2026 and 14:00 rely on the controller's verbatim check.
    - concern: The provision text shown (ADD-03:2.1) does not label sub-paragraphs (a) and (b); the note's '2.1(a)' is a label I cannot confirm from the text shown. This does not affect the substance.
    - concern: The rejection consequence does follow: the replaced 6.6 keeps 'A Proposal received after the time stated in Clause 6.1 ... will be rejected unopened and returned to the Bidder.'
- **P-ADD03-VOL-I-6.2-02** (downstream-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading only records the words and does not decide whether the Indexed Proportion is 'other commercial information'. That is appropriate.
    - concern: VOL-I:6.2 text is not printed in the units shown; it relies on the controller's verbatim check.
    - concern: Form 4-F is not shown, so whether stating the Indexed Proportion there falls inside Envelope A is not determinable here. The item does not claim it.
- **P-ADD03-ROW-2.1-01** (downstream-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The quoted text, the withdraw and modify cut-offs and the late-modification rejection all match ADD-03:2.1. Deleted 6.7 is shown only in a statement, not in the units.
    - concern: The date rule ADD03-MODIFY-CUTOFF is validated with a planning value of 2026-11-26 (as_stated). That does not match the 24 November 2026 reading in the payload, which counts back from 26 November. The person should note this inconsistency.
    - concern: The 24 November calculation relies on the VOL-I 2.4 calendar (Sunday to Thursday), which is not printed here. It is consistent with the stated weekday of the 26th.
    - concern: The clause says 'the time stated in this Clause' but gives no time of day. This is correctly flagged. Whether 'before the Proposal Due Date' for withdrawal runs to 14:00 is also not stated.
    - concern: The cover versus clause substance conflict is correctly left to a person.
- **P-ADD03-ISSUE-6.6-SUBSTANCE** (downstream-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The cover paragraph ('without change of substance') and deleted 6.7 are not in the printed units. Both are relied on through the statements and the controller's verbatim checks.
    - concern: The contrast between 6.7 ('at any time before') and the new 6.6 (two Working Days before for modification) is real on the words shown. The issue leaves the decision to a person, which is appropriate.
- **P-ADD03-VOL-I-9.6-01** (downstream-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Q16 supports the reading that assumptions limiting or qualifying Volume V must be listed in Form 4-E, and that 9.6 applies.
    - concern: VOL-I:9.6 text is not printed in the units shown; it relies on the controller's verbatim check.
    - concern: The reading correctly leaves the question of listing the concession-term point to a person.
- **P-ADD03-VOL-II-3.4-01** (downstream-001; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: ADD-03:5.1 quotes 'not more than 5 OU/m³ at the site boundary', which matches the VOL-II 3.4 text before the addendum. So the substitution is applicable on the words, and the unapplied op is a gap in the pipeline rather than a conflict between provisions.
    - concern: The statement that no op exists for 5.1 is a pipeline fact I cannot verify from the printed evidence.
    - concern: ESIA Figure 7-2 is absent, so the limit value cannot be stated. 'none_stated' and the 'insufficient evidence' note are appropriate.
    - concern: The cover naming Clause 3.5 is not printed in the units shown, so I cannot verify it.
    - concern: 5.1 confirms that the 98th percentile hourly basis is unchanged.
- **P-ADD03-ISSUE-ODOUR** (downstream-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: ADD-03:5.1 and the base VOL-II 3.4 text support the issue: the substitution is stated, and the effective text is reported as unchanged.
    - concern: The cover's reference to Clause 3.5 is not in the printed units. The Q18 'data room' quote appears only in the evidence quotation.
    - concern: The issue appropriately leaves the decision and the odour design basis to a person.
- **DS-ADD03-ESC-51** (downstream-004; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: Provision text and target text match the item: 5.1 substitutes the nearest-receptor value for 5 OU/m³ at the site boundary, and VOL-II 3.4 still reads 5 OU/m³ at the site boundary in the evidence shown.
    - concern: Claims about 5.2, Q18 and the cover's 'Clause 3.5' wording rest on statements whose quotations I could check only as printed. The cover quotation says 'Clause 3.5', which does differ from 5.1's 'Clause 3.4'.
    - concern: I cannot check from the evidence shown that Figure 7-2 is absent from the build, or that clarifications closed on 2026-11-12 (VOL-I 5.2). The item's own statements assert both. The closure date is also after today's date of 2026-10-05, which is odd but is not a defect in the item.
    - concern: The 'not promoted' status is consistent with the unit status 'not_issued', but the evidence printed does not show the promotion record itself.
    - concern: The item correctly leaves the choice of criterion to a person.
- **DS-ADD03-ESC-Q19** (downstream-004; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: Q19 says year 1 prices with indexation from the first anniversary of PCOD. 3.1 says Base Date prices and 3.3 says indexation from the Base Date. These are quoted verbatim and do look like different price bases, so the conflict is plausible.
    - concern: The conflict is not certain. Year 1 prices could coincide with Base Date prices, or Q19 could be read as a clarification of how the Form 4-F figure is entered. This is an interpretation that a person must confirm, and the item marks it so.
    - concern: The evidence shown does not include the text of Schedule 9, VOL-V 29.2, or the Base Date definition. These are needed to decide whether the two readings really diverge.
    - concern: The VOL-I 10.5 / 11.5 non_responsive rules are not in the evidence shown. They are only mentioned as PROPOSED.
- **DS-ADD03-ISSUE-AP-BASIS** (downstream-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The issue restates the Q19 versus 3.1/3.3 tension, and its quotations match the verified text.
    - concern: It is an interpretation that a person must confirm. It states no conclusion and leaves the decision to a person.
    - concern: Whether VOL-I 10.5 / 11.5 is engaged cannot be checked from the evidence shown, but the issue only raises it as a question.
    - concern: The 'clarification window is closed' statement relies on VOL-I 5.2, which is not in the printed evidence.
- **DS-ESC-P4-NOTE2** (downstream-005; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The conflict is real: Arabic note 2 says natural ground before grading and filling, and English note (2) says finished ground after grading and filling.
    - concern: The claim that the Arabic column heading also says natural ground rests on a statement quote. The item's own evidence list quotes only note 2 and the English note.
    - concern: The 'clarification window has closed' claim is not shown in the printed evidence. It does not change the conflict.
- **DS-ESC-T51-NOTE1** (downstream-005; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The conflict is real: Arabic note 1 covers permanent and temporary structures, including cranes and equipment, while English note (1) covers permanent structures including stacks.
    - concern: The link to the crane and lifting plan in ADD-03 Q21 is not supported by anything printed in the request. It is context only.
    - concern: The 'clarification window has closed' claim is likewise not shown in the printed evidence.
- **DS-ESC-T51-NOTE2** (downstream-005; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The conflict is real and no datum is chosen.
    - concern: The th-left quote in this item's evidence reads 'الإنارة التحذيرية الحدّ الأقصى للارتفاع (…)'. It includes extra words, apparently a neighbouring 'warning lighting' column heading. The same unit is quoted without those words in statement S-F-NOTE2-AR. The person should check the crop to confirm whi…
    - concern: The th-left unit text is not printed in the units section, so I could not check it independently.
- **DS-ROW-P4-03** (downstream-005; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The Arabic quote matches note 1, and the row is marked pending reading and not in force. The conflict with English note (1) is declared and real.
    - concern: The row's requirement text states the Arabic scope, while the note says no rendering is chosen. A reader could take the row as adopting the Arabic reading. Section 7.2 ('The Arabic text governs') is not addressed in the row itself.
    - concern: The post_award_evidence text ('Crane, lifting and temporary works planning…') is the proposer's own wording. The only basis cited is note 1.
    - concern: The row cites units notes-head and p4-image, which are not printed in the request, so I could not check them.
- **DS-ROW-P4-04** (downstream-005; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The row stays neutral on the datum and marks its post-award evidence 'unresolved', which fits the unresolved conflict.
    - concern: The row's requirement text follows the Arabic reading. This is the same concern as for row 03: Section 7.2 is a person's decision.
    - concern: The th-left unit is cited but not printed in the units section.
- **DS-ISSUE-RENDERINGS** (downstream-005; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
    - concern: The differences on scope (note 1) and datum (note 2) follow from the quotes shown. The note 3 difference ('installation' in the Arabic, 'erected' in the English) is described as slight, and both renderings give thirty days. That is consistent with the statement.
    - concern: The issue refers to the crane and lifting plan (ADD-03 Q21) and to a closed clarification window. Neither appears in the printed evidence.
    - concern: The wording in 7.2 ('The Arabic text governs') is stated neutrally and the decision is left to a person. That is appropriate.
- **D1** (downstream-006; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The core requirement follows from the text shown. Replaced 29.2(a) says the Indexed Proportion is the percentage the Bidder states in Form 4-F, at least 50% and at most 70%, until the end of year 10. The old VOL-V 29.2 had a fixed 60/40 split.
    - concern: The second date_note quotes 'from the start of the eleventh (11th) year of operations'. The printed ADD-03:3.3 text stops at '(a) ... ; and', so that wording is not in the evidence shown. It is presumably in clause (b), which is not printed. I cannot verify it and it is not tied to any quotation.
    - concern: The row does not say what applies after year 10. Clause (b) is not shown, so the row may be incomplete for the full clause, and the statement that the band covers only the first ten years rests on part of the text.
    - concern: The consequence (non_responsive under VOL-I 10.5) is not stated anywhere in the pack. The item itself says so (S2, I-NO-CONSEQUENCE). Whether a value outside the band is 'price subject to adjustment other than as provided in Volume V' is a judgment. The item marks it as human decision pending, whic…
    - concern: The Form 4-F paragraph shown (para1) only confirms that the Availability Payment is unconditional. It does not show a field for the Indexed Proportion. The evidence therefore does not confirm that Form 4-F has a place to state it. I did not see the form layout.
    - concern: I did not see VOL-I 9.6 or 11.5, so I cannot check the rationale for excluding them. The 5.2 clarification-window-closed claim (S7) is attributed to a 'task packet' and is not supported by the quotation attached to it.

## Requests: failures, deferrals, repairs and route notices

- **analysis-004** (done): 1 failed call(s) (rate_limit); DEFERRED 2026-10-05T18:55:13Z: host rate limit (the host ended with an error (success: 429) You've hit your session limit · resets 10:30pm (UTC)); the host names a reset in 12886.5 s, beyond 300 s (reset named in about 215 min)
- **analysis-005** (done): 1 failed call(s) (rate_limit); DEFERRED 2026-10-05T18:55:13Z: host rate limit (the host ended with an error (success: 429) You've hit your session limit · resets 10:30pm (UTC)); the host names a reset in 12949.8 s, beyond 300 s (reset named in about 216 min)
- **downstream-001** (done): repaired once (1 problem(s) before the re-ask)

Route notices (how the requests were served; they change no status):
- **capabilities_declared** (reading-ADD-03-p4-r1): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the reading request was checked a…
- **capabilities_declared** (analysis-001): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request was checked …
- **capabilities_declared** (analysis-002): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request was checked …
- **capabilities_declared** (analysis-003): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request was checked …
- **capabilities_declared** (analysis-004): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request was checked …
- **capabilities_declared** (analysis-005): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request was checked …
- **capabilities_declared** (analysis-006): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request was checked …
- **capabilities_declared** (analysis-007): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request was checked …
- **capabilities_declared** (analysis-008): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request was checked …
- **capabilities_declared** (analysis-009): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request was checked …
- **capabilities_declared** (downstream-001): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request was checke…
- **capabilities_declared** (downstream-002): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request was checke…
- **capabilities_declared** (downstream-003): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request was checke…
- **capabilities_declared** (downstream-004): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request was checke…
- **capabilities_declared** (downstream-005): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request was checke…
- **capabilities_declared** (downstream-006): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request was checke…

## Manual interventions (and automatic host sessions, named as such: not a person)

- 2026-10-05T18:38:45Z: host session (automatic) — batch reading-ADD-03-p4-r1 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session reading an image; not a person
- 2026-10-05T18:45:35Z: host session (automatic) — batch analysis-001 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T18:45:51Z: host session (automatic) — batch analysis-002 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T18:48:15Z: host session (automatic) — batch analysis-003 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T18:55:13Z: host session (automatic) — batch analysis-004 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T18:55:13Z: host session (automatic) — batch analysis-005 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T21:17:17Z: host session (automatic) — batch analysis-004 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T21:23:26Z: host session (automatic) — batch analysis-005 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T21:23:50Z: host session (automatic) — batch analysis-006 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T21:34:25Z: host session (automatic) — batch analysis-007 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T21:34:50Z: host session (automatic) — batch analysis-008 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T21:46:17Z: host session (automatic) — batch analysis-009 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T21:56:34Z: host session (automatic) — batch downstream-001 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-05T21:56:34Z: host session (automatic) — batch downstream-002 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-05T22:00:01Z: host session (automatic) — batch downstream-003 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-05T22:01:10Z: host session (automatic) — batch downstream-004 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-05T22:08:34Z: host session (automatic) — batch downstream-005 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-05T22:08:35Z: host session (automatic) — batch downstream-006 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person

## The diff (ADD-02 → ADD-03; [diff.md](diff.md))

## What changed from ADD-02 to ADD-03

### ADD-03: PARTIAL (issued 2026-11-15)

- ops: 19 (0 invalid); provisions: 57 (17 unresolved)
- validated state: ADD-02 — this addendum does NOT replace it until every provision is treated and every op is valid
- UNRESOLVED ADD-03:5.1: In Volume II Clause 3.4, ‘not more than 5 OU/m³ at the site boundary’ is deleted and ‘not more than the odour concentration shown for the nearest sensitive rece
- UNRESOLVED ADD-03:Q19: No: 19 | Bidder question: Form 4-F requests the Availability Payment for year 1 of operations. Is that figure to be stated in the prices of year 1 of operations
- UNRESOLVED ADD-03:7.3: A Bidder whose Proposal provides for any structure, plant or equipment at the site exceeding thirty (30) metres in height shall notify the Authority through the
- UNRESOLVED ADD-03:7.4: Bidders shall reflect Table 5-1 in the Technical Proposal.
- UNRESOLVED ADD-03:p4-image/hdr-en: Northern Region Airspace Safeguarding Office
- UNRESOLVED ADD-03:p4-image/hdr-ar: مكتب حماية المجال الجوي بالمنطقة الشمالية
- UNRESOLVED ADD-03:p4-image/date: التاريخ: ١٠ نوفمبر ٢٠٢٦م
- UNRESOLVED ADD-03:p4-image/ref: الرقم: ٤٧١/٢٠٢٦
- UNRESOLVED ADD-03:p4-image/subject: الموضوع: اشتراطات الارتفاعات لموقع محطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان
- UNRESOLVED ADD-03:p4-image/tender-ref: مناقصة رقم: NUPA/ISTP/2026/014
- UNRESOLVED ADD-03:p4-image/table-title: جدول ٥-١: الحدّ الأقصى لارتفاع المنشآت والمعدّات في الموقع
- UNRESOLVED ADD-03:p4-image/table-intro: يُحدِّد الحدّ الأقصى المسموح به للارتفاع في كل منطقة من مناطق الموقع على النحو الآتي:
- UNRESOLVED ADD-03:p4-image/note2: ٢. يُقاس الارتفاع من منسوب الأرض الطبيعية قبل أعمال التسوية والردم.
- UNRESOLVED ADD-03:p4-image/note3: ٣. يجب إخطار المكتب قبل ثلاثين (٣٠) يوماً على الأقل من تركيب أي رافعة في الموقع.
- UNRESOLVED ADD-03:T5-1/note(1): (1)  These limits apply to all permanent structures, including stacks.
- UNRESOLVED ADD-03:T5-1/note(2): (2)  Height is measured from finished ground level after grading and filling.
- UNRESOLVED ADD-03:T5-1/note(3): (3)  The Office shall be notified at least thirty (30) days before any crane is erected at the site.
- cover summary vs provisions (C28, report only): 12 finding(s)
  - unknown verb: 'consolidates Volume I Clauses 6.6 and 6.7 without change of substance': C28 does not know the verb 'consolidates', so what it claims is compared by its targets only; a person reads it against the provisions
  - consequence not mentioned: ADD-03:2.1 states 'A Proposal received after the time stated in Clause 6.1, and a modification received after the time stated in this Clause, will be rejected unopened and returned to the Bidder.'; the summary says only 'consolidates Volume I Clauses 6.6 and 6.7 without change of substance'
  - not found: 'replaces the odour criterion in Volume II Clause 3.5 by reference to the Environmental and Social Impact Assessment': no provision of ADD-03 does this
  - scope (governing language): 'inserts a new Volume II Clause 5.6 limiting the height of permanent structures at the site in accordance with Table 5-1': its scope word(s) permanent are printed in ADD-03:T5-1, which does not govern ('The Arabic text governs. The English translation at Appendix B is provided for convenience only.', ADD-03:7.2); ADD-03:p4-image governs: unchecked against it, a person compares
  - understated: 'responds to clarification requests 15 to 21', but ADD-03/Q17 adds an obligation (VOL-I:8.3): 'Each member of the joint venture shall hold a certificate that meets Volume I Clause 8.3, and a copy of each certificate shall be submitted with Envelope A.'
  - understated: 'responds to clarification requests 15 to 21', but ADD-03/Q20 adds an obligation (VOL-IV:F4-F, VOL-I:6.2): 'Yes. The Bidder shall complete that row by stating, after the words ‘Per Volume V Clause 29.2’, the Indexed Proportion as a percentage. The Indexed Proportion shall not be stated anywhere in Envelope A. Volume I Clause 6.2 applies.'
  - understated: 'responds to clarification requests 15 to 21', but ADD-03/Q21 adds an obligation (VOL-I:9.7): 'Yes. The construction methodology in the Technical Proposal shall include a crane and lifting plan that demonstrates compliance with Table 5-1 (Volume II Clause 5.6, inserted by Section 7 of this Addendum).'
  - omitted: ADD-03/3.2 inserts new text after VOL-V:1.1; the summary does not mention it: 'The following new Clause 1.1A is inserted in Volume V after Clause 1.1: ‘1.1A Base Date means the date falling twenty-eight (28) days before the Proposal Due Date.’'
  - omitted: ADD-03/3.4 adds an obligation (VOL-I:10.3); the summary does not mention it: 'Bidders shall reflect this Section 3 in the Financial Model submitted under Volume I Clause 10.3.'
  - omitted: ADD-03/4.2 adds an obligation (VOL-II:S3); the summary does not mention it: 'Bidders shall reflect this Section 4 in the process design submitted under Volume II Section 3.'
  - omitted: ADD-03/5.2 adds an obligation (VOL-II:3.4); the summary does not mention it: 'Bidders shall demonstrate compliance with Volume II Clause 3.4, as amended, in the Technical Proposal.'
  - omitted: ADD-03/AppA/para1 confirms ADD-03:p4-image; the summary does not mention it: 'Table 5-1 is reproduced below as issued by the Northern Region Airspace Safeguarding Office. The Arabic text governs in accordance with Section 7 of this Addendum.'

#### Validated vs candidate (partial should not mean useless)

- validated (unchanged, ADD-02): `<outputs>/a3/a3.pdf` (one page), `<outputs>/a5/`
- candidate (CANDIDATE — NOT VALIDATED, ADD-03 as proposed): `<outputs>/a3/a3_candidate.pdf` / `.md`, `<outputs>/a5/candidate/`

**What may be changing.** ADD-03 is PARTIAL: 17 of 57 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 19 op(s) that are valid there stood (each still a proposal: review proposed 19), A3 would gain 1 row(s) (ADD-03-2.1-01 (ADD-03/2.1(a))), lose 0 (none) and change 1 (VOL-I-8.3-01 (ADD-03/Q17)); A5, replanned at ADD-03's issue date (2026-11-15), would move the latest dates of 0 activities (none), add 0 (none) and remove 0 (none), and marks 7 REVIEW through relationships. Not settled: 7 activities blocked by an unresolved row (fin-model-build, technical-proposal, deviations-review, fin-model-freeze and 3 more), 2 STALE row(s), 2 obligation(s) reaching no output (C46), 0 relationship chain(s) blocked or incomplete, 6 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT and 5 more. Clarification route: the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person. Nothing here is validated, accepted or applied to the real state.

- **Clarification route:** the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person (ADD-03 issued 2026-11-15; the cut-off is computed from VOL-I-5.2-01 at that stage). No question about it is suggested as sendable; a proposed entry stays a DRAFT, not sent.

### Requirements

- new: 1; out of force: 1; changed: 11

- NEW ADD-03-2.1-01: NEW (introduced by ADD-03/2.1(a)) (by ADD-03/2.1(a))
- OUT VOL-I-6.7-01: DELETED (ADD-03/2.1(b))
- CHANGED VOL-I-6.1-01: VOL-I 6.6: + 'A Bidder may withdraw its Proposal at any time before the Proposal Due Date, and may modify its Proposal not later than two (2) Working Days before the Proposal Due Date, in each case by written notice through the Portal.'; '6.1' -> '6.1, and a modification received after the time stated in this Clause,' by ADD-03/2.1(a) (depends on it: the unit its consequence is quoted from)
- CHANGED VOL-V-29.2-01: wording; quoted words; reading: parameters (by ADD-03/3.3)
- CHANGED VOL-I-6.2-02: reading: parameters
- CHANGED VOL-I-9.7-01: reading: parameters
- CHANGED VOL-I-10.2-01: VOL-V 29.2: + 'from the Base Date'; '9, with sixty per cent (60%)' -> '9. The proportion'; 'and forty per cent (40%) remaining' -> '(the Indexed Proportion) shall be: (a) until the end of the tenth (10th) year of operations, the percentage stated by the Bidder in Form 4-F, which shall be not less than fifty per cent (50%) and not more than seventy per cent (70%); and (b) from the start of the eleventh (11th) year of operations, seventy-five per cent (75%). The balance of the payment shall remain' by ADD-03/3.3 (depends on it: REL-PAY-QUOTED-PRICE (feeds_calculation, confirmed) < REL-PAY-MECHANISM (feeds_calculation, confirmed))
- CHANGED VOL-II-3.1-01: wording; quoted words; secondary unit VOL-II:H:S3 annotated by ADD-03/4.2; reading: parameters (by ADD-03/4.1, ADD-03/4.2)
- CHANGED VOL-II-3.2-01: reading: parameters
- CHANGED VOL-II-3.2-02: quoted words; reading: parameters
- CHANGED VOL-IV-F4A-02: secondary units VOL-IV:F4-A/tender-reference, VOL-IV:F4-A/project, VOL-IV:F4-A/proposal-due-date, VOL-IV:F4-A/commercial-registration-number, VOL-IV:F4-A/registered-address, VOL-IV:F4-A/single-point-of-contact-name-title, VOL-IV:F4-A/contact-email-and-telephone, VOL-IV:F4-A/signature, VOL-IV:F4-A/name-of-signatory, VOL-IV:F4-A/capacity, VOL-IV:F4-A/power-of-attorney-reference-and-date, VOL-IV:F4-A/date, VOL-IV:F4-A/company-seal annotated by ADD-03/cover/para3 (by ADD-03/cover/para3)
- CHANGED VOL-IV-F4E-01: VOL-V 1.1: 'payment' -> 'payment, expressed at Base Date prices,' by ADD-03/3.1 (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed)); VOL-V 29.2: + 'from the Base Date'; '9, with sixty per cent (60%)' -> '9. The proportion'; 'and forty per cent (40%) remaining' -> '(the Indexed Proportion) shall be: (a) until the end of the tenth (10th) year of operations, the percentage stated by the Bidder in Form 4-F, which shall be not less than fifty per cent (50%) and not more than seventy per cent (70%); and (b) from the start of the eleventh (11th) year of operations, seventy-five per cent (75%). The balance of the payment shall remain' by ADD-03/3.3 (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed))
- CHANGED VOL-IV-F4F-01: secondary units VOL-IV:F4-F/bidder, VOL-IV:F4-F/availability-payment-sar-per-annum-year-1-of-operations, VOL-IV:F4-F/availability-payment-in-words, VOL-IV:F4-F/estimated-project-cost-sar, VOL-IV:F4-F/assumed-senior-debt-tenor-years-from-financial-close, VOL-IV:F4-F/assumed-senior-debt-margin-bps, VOL-IV:F4-F/assumed-gearing-debt-equity, VOL-IV:F4-F/project-irr-nominal-post-tax, VOL-IV:F4-F/equity-irr-nominal-post-tax, VOL-IV:F4-F/indexation-basis-assumed, VOL-IV:F4-F/model-auditor, VOL-IV:F4-F/date-of-model-audit-opinion, VOL-IV:F4-F/signature, VOL-IV:F4-F/name-and-capacity, VOL-IV:F4-F/date annotated by ADD-03/Q20; VOL-V 29.2: + 'from the Base Date'; '9, with sixty per cent (60%)' -> '9. The proportion'; 'and forty per cent (40%) remaining' -> '(the Indexed Proportion) shall be: (a) until the end of the tenth (10th) year of operations, the percentage stated by the Bidder in Form 4-F, which shall be not less than fifty per cent (50%) and not more than seventy per cent (70%); and (b) from the start of the eleventh (11th) year of operations, seventy-five per cent (75%). The balance of the payment shall remain' by ADD-03/3.3 (depends on it: REL-PAY-FORM-4F (feeds_calculation, confirmed) < REL-PAY-MECHANISM (feeds_calculation, confirmed)) (by ADD-03/Q20)
- CONFIRMED (unchanged) VOL-I-6.2-01: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Words unchanged at ADD-03. ADD-03 Q20 cites VOL-I 6.2: the Indexed Proportion goes in Form 4-F (Envelope B) and must not be stated anywhere in Envelope A. The …'); other ops on its units (the re-made reading records no change from them; a person checks): ADD-03/Q20 (adds_obligation; ADD-03:Q20; answer reads 'adds' (summary.classify_answer))
- CONFIRMED (unchanged) VOL-I-10.3-01: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Words of VOL-I 10.3 unchanged at ADD-03. ADD-03 3.4 adds: 'Bidders shall reflect this Section 3 in the Financial Model submitted under Volume I Clause 10.3.' S…'); other ops on its units (the re-made reading records no change from them; a person checks): ADD-03/3.4 (adds_obligation; ADD-03:3.4)
- CONFIRMED (unchanged) VOL-I-10.3-02: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Words of VOL-I 10.3 unchanged at ADD-03. Under ADD-03 3.4 the Financial Model must reflect ADD-03 Section 3. Whether the auditor's opinion must cover the Secti…'); other ops on its units (the re-made reading records no change from them; a person checks): ADD-03/3.4 (adds_obligation; ADD-03:3.4)
- CONFIRMED (unchanged) VOL-II-6.4-01: confirmed by ADD-03/Q15 (interprets; ADD-03:Q15; answer reads 'adds' (summary.classify_answer)); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Words of VOL-II 6.4 unchanged at ADD-03. ADD-03 Q15: 'Volume II Clause 6.4 states a minimum period. A Bidder may propose a longer period but is not required to…')
- CONFIRMED (unchanged) VOL-II-6.4-02: confirmed by ADD-03/Q15 (interprets; ADD-03:Q15; answer reads 'adds' (summary.classify_answer)); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03. The data-availability words are unchanged. ADD-03 Q15 (annotation, 'interprets') addresses only the retention period in the same clause ('st…')
- NOT SETTLED VOL-IV-F4A-01: unchanged by the applied ops; not confirmed while: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides)
- NOT SETTLED VOL-I-9.6-01: unchanged by the applied ops; not confirmed while: open: I-CONCESSION, human decision pending (the confirming op(s) ADD-03/Q16 (interprets; ADD-03:Q16; answer reads 'adds' (summary.classify_answer)) do not settle it)
- NOT SETTLED VOL-IV-F4F-02: unchanged by the applied ops; not confirmed while: ADD-03:Q19 UNRESOLVED: not promotable: ADD-03/Q19 conflicting (declared_conflicts: the proposer declares: ADD-03:3.3); ADD-03/Q19-issue conflicting (declared_conflicts: the proposer …

### Stale readings and decisions

- STALE VOL-I-8.3-01: new dependency ADD-03:Q17; VOL-I:8.3 changed since ADD-01 (by ADD-03/Q17)
- STALE VOL-II-3.4-01: new dependency ADD-03:5.2; new dependency ADD-03:Q18; VOL-II:3.4 changed since BASE (by ADD-03/5.2, ADD-03/Q18)

### Obligations not reaching the outputs (C46)

- ADD-03/3.2 [A1]: ADD-03/3.2 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-V:1.1; a row of the anchor VOL-V:1.1 does not count): 'The following new Clause 1.1A is inserted in Volume V after
- ADD-03/7.1 [A1]: ADD-03/7.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-II:5.5; a row of the anchor VOL-II:5.5 does not count): 'The following new Clause 5.6 is inserted in Volume II aft

### Reached through relationships (indirect: for review, not direct citations)

Curated links (relationships file) followed from what changed. The requirements above cite a changed unit; these are reached through another provision, in three classes that are never merged. A5 marks the activities that serve them REVIEW with their dates unchanged.

Relationship status: confirmed = stated in the documents (the entry quotes the cross-reference), not confirmed by a person; proposed = inferred by a curator or a model, a person decides; possible = a weaker inference.

#### Confirmed dependency (5)
- VOL-I-10.2-01 (row; ACTIVE) <- VOL-V:29.2 via REL-PAY-MECHANISM > REL-PAY-QUOTED-PRICE [feeds_calculation; link confirmed]
- VOL-IV-F4E-01 (row; ACTIVE) <- VOL-V:1.1, VOL-V:29.2 via REL-VOL-V-FORM-4E [depends_on; link confirmed]; also changed directly
- VOL-IV-F4F-01 (row; ACTIVE) <- VOL-V:29.2 via REL-PAY-MECHANISM > REL-PAY-FORM-4F [feeds_calculation; link confirmed]; also changed directly
- VOL-IV-F4F-02 (row; ACTIVE) <- VOL-I-10.3-01 via REL-MODEL-FORM-4F [feeds_calculation; link confirmed]; also changed directly
- calc:availability-payment (calculation) <- VOL-V:29.2 via REL-PAY-MECHANISM [feeds_calculation; link confirmed]

#### Proposed relationship (2)
- VOL-I-10.3-01 (row; ACTIVE) <- VOL-V:29.2 via REL-PAY-MECHANISM > REL-PAY-FINANCIAL-MODEL [depends_on; link proposed]; also changed directly
- VOL-IV-F4F-02 (row; ACTIVE) <- VOL-V:29.2 via REL-PAY-MECHANISM > REL-PAY-FINANCIAL-MODEL > REL-MODEL-FORM-4F [feeds_calculation; link proposed]; also changed directly

#### Possible impact (1)
- VOL-I-10.6-01 (row; ACTIVE) <- VOL-V:29.2 via REL-PAY-MECHANISM > REL-PAY-FINANCING-ASSUMPTIONS [depends_on; link possible]

#### Referenced but not supplied: conclusions in play that cannot be established (0)
- none

### Disqualifiers (A3)

- ENTERS ADD-03-2.1-01: rejection “a modification received after the time stated in this Clause, will be rejected unopened and returned to the Bidder.”

### Earlier answers to re-read against the new text (never revoked; a person decides)

- `ADD-01:Q1` (ADD-01): cites VOL-II:3.1, changed by ADD-03/4.1; to be re-read against the new text of VOL-II:3.1 (ADD-03/4.1); a person decides whether the answer still holds
- `ADD-01:Q6` (ADD-01): its annotation ADD-01/Q6 targets VOL-V:29.2, changed by ADD-03/3.3; to be re-read against the new text of VOL-V:29.2 (ADD-03/3.3); a person decides whether the answer still holds
- `ADD-03:Q17` (ADD-03): cites VOL-I:8.3, changed by ADD-03/Q17; to be re-read against the new text of VOL-I:8.3 (ADD-03/Q17); a person decides whether the answer still holds
- `ADD-03:Q18` (ADD-03): cites VOL-II:3.4, changed by ADD-03/5.2; to be re-read against the new text of VOL-II:3.4 (ADD-03/5.2); a person decides whether the answer still holds
- `ADD-03:Q19` (ADD-03): cites VOL-IV:F4-F, changed by ADD-03/Q20; cites VOL-V:29.2, changed by ADD-03/3.3; to be re-read against the new text of VOL-IV:F4-F, VOL-V:29.2 (ADD-03/Q20, ADD-03/3.3); a person decides whether the answer still holds
- `ADD-03:Q20` (ADD-03): cites VOL-IV:F4-F, changed by ADD-03/Q20; cites VOL-I:6.2, changed by ADD-03/Q20; cites VOL-V:29.2, changed by ADD-03/3.3; to be re-read against the new text of VOL-IV:F4-F, VOL-I:6.2, VOL-V:29.2 (ADD-03/Q20, ADD-03/3.3); a person decides whether the answer still holds
- `ADD-03:Q21` (ADD-03): cites VOL-I:9.7, changed by ADD-03/Q21; to be re-read against the new text of VOL-I:9.7 (ADD-03/Q21); a person decides whether the answer still holds

### Programme impact (status date 2026-10-22 -> 2026-11-15)

- REWORK assemble-envelope-a: requirement changed: VOL-I-6.1-01 (dependency: VOL-I 6.6: + 'A Bidder may withdraw its Proposal at any time before the Proposal Due Date, and may modify its Proposal not later than two (2) Working Days before the Proposal Due Date, in each case by written notice through the Portal.'; '6.1' -> '6.1, and a modification received after the time stated in this Clause,' by ADD-03/2.1(a) (depends on it: the unit its consequence is quoted from)), VOL-I-6.2-02 (parameters)
- CONFIRMED (unchanged) assemble-envelope-a: VOL-I-6.2-01: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Words unchanged at ADD-03. ADD-03 Q20 cites VOL-I 6.2: the Indexed Proportion goes in Form 4-F (Envelope B) and must not be stated anywhere in Envelope A. The …'); other ops on its units (the re-made reading records no change from them; a person checks): ADD-03/Q20 (adds_obligation; ADD-03:Q20; answer reads 'adds' (summary.classify_answer)); text, cells, dates, status and consequence unchanged: work done stands
- STATUS assemble-envelope-a: timing INFEASIBLE by 12 WD -> INFEASIBLE by 28 WD; total float -12 -> -28 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- REWORK assemble-envelope-b: requirement changed: VOL-I-6.1-01 (dependency: VOL-I 6.6: + 'A Bidder may withdraw its Proposal at any time before the Proposal Due Date, and may modify its Proposal not later than two (2) Working Days before the Proposal Due Date, in each case by written notice through the Portal.'; '6.1' -> '6.1, and a modification received after the time stated in this Clause,' by ADD-03/2.1(a) (depends on it: the unit its consequence is quoted from))
- CONFIRMED (unchanged) assemble-envelope-b: VOL-I-6.2-01: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Words unchanged at ADD-03. ADD-03 Q20 cites VOL-I 6.2: the Indexed Proportion goes in Form 4-F (Envelope B) and must not be stated anywhere in Envelope A. The …'); other ops on its units (the re-made reading records no change from them; a person checks): ADD-03/Q20 (adds_obligation; ADD-03:Q20; answer reads 'adds' (summary.classify_answer)); text, cells, dates, status and consequence unchanged: work done stands
- STATUS assemble-envelope-b: timing OK -> INFEASIBLE by 16 WD; total float 0 -> -16 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS attendance-notice: timing CONDITIONAL — window elapsed 2026-10-14; whether the condition arose is not known -> CONDITIONAL — window elapsed 2026-10-14; whether the condition arose is not known; total float -7 -> -23 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS bond-approval: timing OK -> INFEASIBLE by 6 WD; total float +10 -> -6 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS bond-issue: timing OK -> INFEASIBLE by 6 WD; total float +10 -> -6 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS clarifications: timing OK -> DEADLINE PASSED; total float +13 -> -3 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS completion-certs: timing OK -> INFEASIBLE by 9 WD; total float +7 -> -9 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS consortium-check: timing OK -> INFEASIBLE by 3 WD; total float +13 -> -3 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- REWORK copies: requirement changed: VOL-I-6.1-01 (dependency: VOL-I 6.6: + 'A Bidder may withdraw its Proposal at any time before the Proposal Due Date, and may modify its Proposal not later than two (2) Working Days before the Proposal Due Date, in each case by written notice through the Portal.'; '6.1' -> '6.1, and a modification received after the time stated in this Clause,' by ADD-03/2.1(a) (depends on it: the unit its consequence is quoted from))
- CONFIRMED (unchanged) copies: VOL-I-6.2-01: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Words unchanged at ADD-03. ADD-03 Q20 cites VOL-I 6.2: the Indexed Proportion goes in Form 4-F (Envelope B) and must not be stated anywhere in Envelope A. The …'); other ops on its units (the re-made reading records no change from them; a person checks): ADD-03/Q20 (adds_obligation; ADD-03:Q20; answer reads 'adds' (summary.classify_answer)); text, cells, dates, status and consequence unchanged: work done stands
- STATUS copies: timing INFEASIBLE by 12 WD -> INFEASIBLE by 28 WD; total float -12 -> -28 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- REWORK deliver: requirement changed: VOL-I-6.1-01 (dependency: VOL-I 6.6: + 'A Bidder may withdraw its Proposal at any time before the Proposal Due Date, and may modify its Proposal not later than two (2) Working Days before the Proposal Due Date, in each case by written notice through the Portal.'; '6.1' -> '6.1, and a modification received after the time stated in this Clause,' by ADD-03/2.1(a) (depends on it: the unit its consequence is quoted from))
- CONFIRMED (unchanged) deliver: VOL-I-6.2-01: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Words unchanged at ADD-03. ADD-03 Q20 cites VOL-I 6.2: the Indexed Proportion goes in Form 4-F (Envelope B) and must not be stated anywhere in Envelope A. The …'); other ops on its units (the re-made reading records no change from them; a person checks): ADD-03/Q20 (adds_obligation; ADD-03:Q20; answer reads 'adds' (summary.classify_answer)); text, cells, dates, status and consequence unchanged: work done stands
- STATUS deliver: timing INFEASIBLE by 12 WD -> INFEASIBLE by 28 WD; total float -12 -> -28 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- REWORK deviations-review: requirement changed: VOL-IV-F4E-01 (dependency: VOL-V 1.1: 'payment' -> 'payment, expressed at Base Date prices,' by ADD-03/3.1 (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed)); VOL-V 29.2: + 'from the Base Date'; '9, with sixty per cent (60%)' -> '9. The proportion'; 'and forty per cent (40%) remaining' -> '(the Indexed Proportion) shall be: (a) until the end of the tenth (10th) year of operations, the percentage stated by the Bidder in Form 4-F, which shall be not less than fifty per cent (50%) and not more than seventy per cent (70%); and (b) from the start of the eleventh (11th) year of operations, seventy-five per cent (75%). The balance of the payment shall remain' by ADD-03/3.3 (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed))), VOL-V-29.2-01 (text, status, quote, parameters)
- NOT SETTLED deviations-review: VOL-I-9.6-01: open: I-CONCESSION, human decision pending (the confirming op(s) ADD-03/Q16 (interprets; ADD-03:Q16; answer reads 'adds' (summary.classify_answer)) do not settle it); unchanged at this stage but not confirmed: a person decides
- STATUS deviations-review: timing OK -> INFEASIBLE by 5 WD; total float +11 -> -5 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS fin-assumptions: timing OK -> INFEASIBLE by 11 WD; total float +5 -> -11 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- CONFIRMED (unchanged) fin-model-build: VOL-I-10.3-01: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Words of VOL-I 10.3 unchanged at ADD-03. ADD-03 3.4 adds: 'Bidders shall reflect this Section 3 in the Financial Model submitted under Volume I Clause 10.3.' S…'); other ops on its units (the re-made reading records no change from them; a person checks): ADD-03/3.4 (adds_obligation; ADD-03:3.4); VOL-IV-F4F-02: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03. The confirmation's words are unchanged. ADD-03 Q20 adds a stated Indexed Proportion to the indexation row of the same form; whether a stated…'); other ops on its units (the re-made reading records no change from them; a person checks): ADD-03/Q20 (adds_obligation; ADD-03:Q20; answer reads 'adds' (summary.classify_answer)); text, cells, dates, status and consequence unchanged: work done stands
- STATUS fin-model-build: timing OK -> INFEASIBLE by 16 WD; total float 0 -> -16 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- CONFIRMED (unchanged) fin-model-freeze: VOL-I-10.3-01: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Words of VOL-I 10.3 unchanged at ADD-03. ADD-03 3.4 adds: 'Bidders shall reflect this Section 3 in the Financial Model submitted under Volume I Clause 10.3.' S…'); other ops on its units (the re-made reading records no change from them; a person checks): ADD-03/3.4 (adds_obligation; ADD-03:3.4); VOL-IV-F4F-02: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03. The confirmation's words are unchanged. ADD-03 Q20 adds a stated Indexed Proportion to the indexation row of the same form; whether a stated…'); other ops on its units (the re-made reading records no change from them; a person checks): ADD-03/Q20 (adds_obligation; ADD-03:Q20; answer reads 'adds' (summary.classify_answer)); text, cells, dates, status and consequence unchanged: work done stands
- STATUS fin-model-freeze: timing OK -> INFEASIBLE by 16 WD; total float 0 -> -16 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS fin-standing: timing OK -> INFEASIBLE by 1 WD; total float +15 -> -1 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS fin-statements: timing OK -> INFEASIBLE by 1 WD; total float +15 -> -1 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- REWORK form-4a: requirement changed: ADD-01-AppA-01 (Addenda to acknowledge: ADD-03 issued since ADD-02: 'Bidders shall acknowledge receipt in Form 4-A.')
- NOT SETTLED form-4a: VOL-IV-F4A-01: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); VOL-IV-F4A-02: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); unchanged at this stage but not confirmed: a person decides
- STATUS form-4a: timing OK -> INFEASIBLE by 4 WD; total float +12 -> -4 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- REWORK form-4a-prep: requirement changed: ADD-01-AppA-01 (Addenda to acknowledge: ADD-03 issued since ADD-02: 'Bidders shall acknowledge receipt in Form 4-A.')
- NOT SETTLED form-4a-prep: VOL-IV-F4A-01: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); VOL-IV-F4A-02: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); unchanged at this stage but not confirmed: a person decides
- STATUS form-4a-prep: timing OK -> OK; total float +20 -> +4 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- REWORK form-4b: requirement changed: VOL-I-6.2-02 (parameters)
- STATUS form-4b: timing OK -> INFEASIBLE by 9 WD; total float +7 -> -9 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS form-4b-prep: timing OK -> INFEASIBLE by 7 WD; total float +9 -> -7 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS form-4c-prep: timing OK -> OK; total float +18 -> +2 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS form-4c-sign: timing OK -> INFEASIBLE by 6 WD; total float +10 -> -6 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- REWORK form-4e: requirement changed: VOL-IV-F4E-01 (dependency: VOL-V 1.1: 'payment' -> 'payment, expressed at Base Date prices,' by ADD-03/3.1 (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed)); VOL-V 29.2: + 'from the Base Date'; '9, with sixty per cent (60%)' -> '9. The proportion'; 'and forty per cent (40%) remaining' -> '(the Indexed Proportion) shall be: (a) until the end of the tenth (10th) year of operations, the percentage stated by the Bidder in Form 4-F, which shall be not less than fifty per cent (50%) and not more than seventy per cent (70%); and (b) from the start of the eleventh (11th) year of operations, seventy-five per cent (75%). The balance of the payment shall remain' by ADD-03/3.3 (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed))), VOL-V-29.2-01 (text, status, quote, parameters)
- NOT SETTLED form-4e: VOL-I-9.6-01: open: I-CONCESSION, human decision pending (the confirming op(s) ADD-03/Q16 (interprets; ADD-03:Q16; answer reads 'adds' (summary.classify_answer)) do not settle it); unchanged at this stage but not confirmed: a person decides
- STATUS form-4e: timing OK -> INFEASIBLE by 15 WD; total float +1 -> -15 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- REWORK form-4f: requirement changed: VOL-I-10.2-01 (dependency: VOL-V 29.2: + 'from the Base Date'; '9, with sixty per cent (60%)' -> '9. The proportion'; 'and forty per cent (40%) remaining' -> '(the Indexed Proportion) shall be: (a) until the end of the tenth (10th) year of operations, the percentage stated by the Bidder in Form 4-F, which shall be not less than fifty per cent (50%) and not more than seventy per cent (70%); and (b) from the start of the eleventh (11th) year of operations, seventy-five per cent (75%). The balance of the payment shall remain' by ADD-03/3.3 (depends on it: REL-PAY-QUOTED-PRICE (feeds_calculation, confirmed) < REL-PAY-MECHANISM (feeds_calculation, confirmed))), VOL-IV-F4F-01 (dependency: VOL-V 29.2: + 'from the Base Date'; '9, with sixty per cent (60%)' -> '9. The proportion'; 'and forty per cent (40%) remaining' -> '(the Indexed Proportion) shall be: (a) until the end of the tenth (10th) year of operations, the percentage stated by the Bidder in Form 4-F, which shall be not less than fifty per cent (50%) and not more than seventy per cent (70%); and (b) from the start of the eleventh (11th) year of operations, seventy-five per cent (75%). The balance of the payment shall remain' by ADD-03/3.3 (depends on it: REL-PAY-FORM-4F (feeds_calculation, confirmed) < REL-PAY-MECHANISM (feeds_calculation, confirmed)))
- CONFIRMED (unchanged) form-4f: VOL-IV-F4F-02: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03. The confirmation's words are unchanged. ADD-03 Q20 adds a stated Indexed Proportion to the indexation row of the same form; whether a stated…'); other ops on its units (the re-made reading records no change from them; a person checks): ADD-03/Q20 (adds_obligation; ADD-03:Q20; answer reads 'adds' (summary.classify_answer)); text, cells, dates, status and consequence unchanged: work done stands
- STATUS form-4f: timing OK -> INFEASIBLE by 16 WD; total float 0 -> -16 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS form-4g-review: timing OK -> OK; total float +17 -> +1 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS form-4g-sign: timing OK -> INFEASIBLE by 4 WD; total float +12 -> -4 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS ground-dd: timing OK -> INFEASIBLE by 11 WD; total float +5 -> -11 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS investment-licence: timing OK -> INFEASIBLE by 8 WD; total float +8 -> -8 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- REWORK iso-copy: requirement changed: VOL-I-8.3-01 (stale)
- STATUS iso-copy: timing OK -> OK; total float +21 -> +5 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS lcc-certificate: timing INFEASIBLE by 12 WD -> INFEASIBLE by 28 WD; total float -12 -> -28 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS lcc-ratio: timing INFEASIBLE by 12 WD -> INFEASIBLE by 28 WD; total float -12 -> -28 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS lender-terms: timing OK -> INFEASIBLE by 11 WD; total float +5 -> -11 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- CONFIRMED (unchanged) model-audit-opinion: VOL-I-10.3-02: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Words of VOL-I 10.3 unchanged at ADD-03. Under ADD-03 3.4 the Financial Model must reflect ADD-03 Section 3. Whether the auditor's opinion must cover the Secti…'); other ops on its units (the re-made reading records no change from them; a person checks): ADD-03/3.4 (adds_obligation; ADD-03:3.4); text, cells, dates, status and consequence unchanged: work done stands
- STATUS model-audit-opinion: timing OK -> INFEASIBLE by 16 WD; total float 0 -> -16 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- CONFIRMED (unchanged) model-audit-review: VOL-I-10.3-02: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Words of VOL-I 10.3 unchanged at ADD-03. Under ADD-03 3.4 the Financial Model must reflect ADD-03 Section 3. Whether the auditor's opinion must cover the Secti…'); other ops on its units (the re-made reading records no change from them; a person checks): ADD-03/3.4 (adds_obligation; ADD-03:3.4); text, cells, dates, status and consequence unchanged: work done stands
- STATUS model-audit-review: timing OK -> INFEASIBLE by 15 WD; total float +1 -> -15 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- CONFIRMED (unchanged) model-auditor-appoint: VOL-I-10.3-02: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Words of VOL-I 10.3 unchanged at ADD-03. Under ADD-03 3.4 the Financial Model must reflect ADD-03 Section 3. Whether the auditor's opinion must cover the Secti…'); other ops on its units (the re-made reading records no change from them; a person checks): ADD-03/3.4 (adds_obligation; ADD-03:3.4); text, cells, dates, status and consequence unchanged: work done stands
- STATUS model-auditor-appoint: timing OK -> INFEASIBLE by 15 WD; total float +1 -> -15 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS om-evidence: timing OK -> INFEASIBLE by 3 WD; total float +13 -> -3 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS pcg-execution: timing OK -> INFEASIBLE by 13 WD; total float +3 -> -13 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS pcg-wording: timing OK -> INFEASIBLE by 13 WD; total float +3 -> -13 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS poa: timing OK -> INFEASIBLE by 8 WD; total float +8 -> -8 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS poa-resolutions: timing OK -> INFEASIBLE by 8 WD; total float +8 -> -8 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS references: timing OK -> INFEASIBLE by 7 WD; total float +9 -> -7 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- REWORK seal-and-mark: requirement changed: VOL-I-6.1-01 (dependency: VOL-I 6.6: + 'A Bidder may withdraw its Proposal at any time before the Proposal Due Date, and may modify its Proposal not later than two (2) Working Days before the Proposal Due Date, in each case by written notice through the Portal.'; '6.1' -> '6.1, and a modification received after the time stated in this Clause,' by ADD-03/2.1(a) (depends on it: the unit its consequence is quoted from))
- CONFIRMED (unchanged) seal-and-mark: VOL-I-6.2-01: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Words unchanged at ADD-03. ADD-03 Q20 cites VOL-I 6.2: the Indexed Proportion goes in Form 4-F (Envelope B) and must not be stated anywhere in Envelope A. The …'); other ops on its units (the re-made reading records no change from them; a person checks): ADD-03/Q20 (adds_obligation; ADD-03:Q20; answer reads 'adds' (summary.classify_answer)); text, cells, dates, status and consequence unchanged: work done stands
- STATUS seal-and-mark: timing INFEASIBLE by 12 WD -> INFEASIBLE by 28 WD; total float -12 -> -28 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- STATUS spoc: timing OK -> OK; total float +21 -> +5 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- REWORK technical-proposal: requirement changed: VOL-I-9.7-01 (parameters), VOL-II-3.1-01 (text, status, quote, parameters), VOL-II-3.2-01 (parameters), VOL-II-3.2-02 (quote, parameters), VOL-II-3.4-01 (stale)
- CONFIRMED (unchanged) technical-proposal: VOL-II-6.4-01: confirmed by ADD-03/Q15 (interprets; ADD-03:Q15; answer reads 'adds' (summary.classify_answer)); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Words of VOL-II 6.4 unchanged at ADD-03. ADD-03 Q15: 'Volume II Clause 6.4 states a minimum period. A Bidder may propose a longer period but is not required to…'); VOL-II-6.4-02: confirmed by ADD-03/Q15 (interprets; ADD-03:Q15; answer reads 'adds' (summary.classify_answer)); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03. The data-availability words are unchanged. ADD-03 Q15 (annotation, 'interprets') addresses only the retention period in the same clause ('st…'); text, cells, dates, status and consequence unchanged: work done stands
- STATUS technical-proposal: timing OK -> INFEASIBLE by 15 WD; total float +1 -> -15 WD; the planning date moved 2026-10-22 -> 2026-11-15, which by itself shifts every float by the Working Days between them
- REVIEW (confirmed dependency) deviations-review: VOL-IV-F4E-01 reached from VOL-V:1.1, VOL-V:29.2 via REL-VOL-V-FORM-4E; dates unchanged
- REVIEW (possible impact) fin-assumptions: VOL-I-10.6-01 reached from VOL-V:29.2 via REL-PAY-FINANCING-ASSUMPTIONS, REL-PAY-MECHANISM; dates unchanged
- REVIEW (confirmed dependency) fin-model-build: VOL-IV-F4F-02 reached from VOL-I-10.3-01 via REL-MODEL-FORM-4F; dates unchanged
- REVIEW (proposed relationship) fin-model-build: VOL-I-10.3-01, VOL-IV-F4F-02 reached from VOL-V:29.2 via REL-MODEL-FORM-4F, REL-PAY-FINANCIAL-MODEL, REL-PAY-MECHANISM; dates unchanged
- REVIEW (confirmed dependency) fin-model-freeze: VOL-IV-F4F-02 reached from VOL-I-10.3-01 via REL-MODEL-FORM-4F; dates unchanged
- REVIEW (proposed relationship) fin-model-freeze: VOL-I-10.3-01, VOL-IV-F4F-02 reached from VOL-V:29.2 via REL-MODEL-FORM-4F, REL-PAY-FINANCIAL-MODEL, REL-PAY-MECHANISM; dates unchanged
- REVIEW (confirmed dependency) form-4e: VOL-IV-F4E-01 reached from VOL-V:1.1, VOL-V:29.2 via REL-VOL-V-FORM-4E; dates unchanged
- REVIEW (confirmed dependency) form-4f: VOL-I-10.2-01, VOL-IV-F4F-01, VOL-IV-F4F-02 reached from VOL-I-10.3-01, VOL-V:29.2 via REL-MODEL-FORM-4F, REL-PAY-FORM-4F, REL-PAY-MECHANISM, REL-PAY-QUOTED-PRICE; dates unchanged
- REVIEW (proposed relationship) form-4f: VOL-IV-F4F-02 reached from VOL-V:29.2 via REL-MODEL-FORM-4F, REL-PAY-FINANCIAL-MODEL, REL-PAY-MECHANISM; dates unchanged
- REVIEW (possible impact) lender-terms: VOL-I-10.6-01 reached from VOL-V:29.2 via REL-PAY-FINANCING-ASSUMPTIONS, REL-PAY-MECHANISM; dates unchanged
- FEASIBILITY lcc-ratio: INFEASIBLE by 12 WD -> INFEASIBLE by 28 WD
- FEASIBILITY lcc-certificate: INFEASIBLE by 12 WD -> INFEASIBLE by 28 WD
- FEASIBILITY fin-model-build: OK -> INFEASIBLE by 16 WD
- FEASIBILITY model-auditor-appoint: OK -> INFEASIBLE by 15 WD
- FEASIBILITY technical-proposal: OK -> INFEASIBLE by 15 WD
- FEASIBILITY pcg-wording: OK -> INFEASIBLE by 13 WD
- FEASIBILITY ground-dd: OK -> INFEASIBLE by 11 WD
- FEASIBILITY lender-terms: OK -> INFEASIBLE by 11 WD
- FEASIBILITY model-audit-review: OK -> INFEASIBLE by 15 WD
- FEASIBILITY completion-certs: OK -> INFEASIBLE by 9 WD
- FEASIBILITY poa-resolutions: OK -> INFEASIBLE by 8 WD
- FEASIBILITY references: OK -> INFEASIBLE by 7 WD
- FEASIBILITY bond-approval: OK -> INFEASIBLE by 6 WD
- FEASIBILITY deviations-review: OK -> INFEASIBLE by 5 WD
- FEASIBILITY consortium-check: OK -> INFEASIBLE by 3 WD
- FEASIBILITY om-evidence: OK -> INFEASIBLE by 3 WD
- FEASIBILITY pcg-execution: OK -> INFEASIBLE by 13 WD
- FEASIBILITY poa: OK -> INFEASIBLE by 8 WD
- FEASIBILITY clarifications: OK -> DEADLINE PASSED
- FEASIBILITY fin-model-freeze: OK -> INFEASIBLE by 16 WD
- FEASIBILITY fin-statements: OK -> INFEASIBLE by 1 WD
- FEASIBILITY model-audit-opinion: OK -> INFEASIBLE by 16 WD
- FEASIBILITY investment-licence: OK -> INFEASIBLE by 8 WD
- FEASIBILITY form-4b-prep: OK -> INFEASIBLE by 7 WD
- FEASIBILITY bond-issue: OK -> INFEASIBLE by 6 WD
- FEASIBILITY fin-standing: OK -> INFEASIBLE by 1 WD
- FEASIBILITY form-4c-sign: OK -> INFEASIBLE by 6 WD
- FEASIBILITY fin-assumptions: OK -> INFEASIBLE by 11 WD
- FEASIBILITY form-4e: OK -> INFEASIBLE by 15 WD
- FEASIBILITY form-4f: OK -> INFEASIBLE by 16 WD
- FEASIBILITY form-4a: OK -> INFEASIBLE by 4 WD
- FEASIBILITY form-4b: OK -> INFEASIBLE by 9 WD
- FEASIBILITY form-4g-sign: OK -> INFEASIBLE by 4 WD
- FEASIBILITY assemble-envelope-a: INFEASIBLE by 12 WD -> INFEASIBLE by 28 WD
- FEASIBILITY assemble-envelope-b: OK -> INFEASIBLE by 16 WD
- FEASIBILITY copies: INFEASIBLE by 12 WD -> INFEASIBLE by 28 WD
- FEASIBILITY seal-and-mark: INFEASIBLE by 12 WD -> INFEASIBLE by 28 WD
- FEASIBILITY deliver: INFEASIBLE by 12 WD -> INFEASIBLE by 28 WD

## Next (a person)

- read the unresolved and escalated provisions first, then each item against its evidence (`../ai/ADD-03-run-host-blind05-s12-20261005T183535Z-combined/proposals.yaml`, `../downstream/proposals.yaml`)
- nothing here is applied to the real curation: to take an item over, add the PDF to the pack (OPERATING_GUIDE §3 steps 1-2) and copy the reviewed files listed in `promotion.json`; then `pin`, `check-register`, `outputs` and decide with `accept` / `reject` as usual
