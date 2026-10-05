# Review packet: ADD-03, AI workflow run ADD-03-run-host-blind05-20261005T025444Z

> **CANDIDATE: proposed by the AI workflow; not reviewed; nothing accepted.** Statuses are the controller's; a person decides every item. The real `curation/`, `config/` and `out/` were only read: everything below lives in this run's folder.

- PDF: `/home/user/tender-pack-reader/rehearsals/blind-05/input/ADD-03_Addendum_No_3.pdf` (sha256 9c5e22d59a80d48f…, 5 pages); preceding state: pack `/home/user/tender-pack-reader/config/pack.yaml` (NUPA-ISTP-2026-014), previous evidence build `/home/user/tender-pack-reader/build`
- route **host**; model requested `claude-code headless (opus)`, reported `None`; host sessions report: claude-opus-5-5
- status **partial**: 23 provision(s) unresolved in the candidate (listed first in the review packet); 23 downstream task(s) answered only by items that cannot be promoted: esc:ADD-03:cover/para3, esc:ADD-03:2.1, esc:ADD-03:3.3, esc:ADD-03:3.3(b), esc:ADD-03:5.1, esc:ADD-03:5.2, esc:ADD-03:Q18, esc:ADD-03:7.2 …; check-register on the candidate: exit 1, 1 finding(s) {'quote': 1}
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed

## Execution, completeness and approval (three separate things)

- **Execution** (what ran): ingest done, readings done, analysis done, validation done, downstream done, downstream_validation done, critic done, promotion done, pin done, check_register done, outputs done, diff done, review running; batches reading: {'done': 1}; analysis: {'done': 9}; downstream: {'done': 5}
- **Completeness** (what the run completed): **partial**: 23 provision(s) unresolved in the candidate (listed first in the review packet); 23 downstream task(s) answered only by items that cannot be promoted: esc:ADD-03:cover/para3, esc:ADD-03:2.1, esc:ADD-03:3.3, esc:ADD-03:3.3(b), esc:ADD-03:5.1, esc:ADD-03:5.2, esc:ADD-03:Q18, esc:ADD-03:7.2 …; check-register on the candidate: exit 1, 1 finding(s) {'quote': 1}
  - downstream tasks: 54; answered 31; unanswered 0; answered only by items that cannot be promoted 23; answered 'no change' 8
- **Human approval**: **none** (nothing approved, accepted, rejected or sent); no decision is recorded in the candidate's decisions file

## What is candidate and what is real

- **Candidate** (proposed by this run, nothing accepted): `../candidate/` — a copy of the curation and configuration with ADD-03 added, its evidence build, its op file, rows, issues, templates and outputs.
- **Last validated state**: `../candidate/out-before/` (the pre-addendum outputs built from the copied curation and the previous evidence build; done)
- **Real** (untouched): `curation/`, `config/`, `out/`; the owner's approvals and readings were copied unchanged and used read-only.

- real inputs changed since the run started: none

## Candidate outputs

Exit 0 (WORKING DRAFT (not releasable)); every file carries the banner (`../candidate/out/CANDIDATE.md`); A1 has a candidate status column {'UNRESOLVED': 14, 'proposed (existing row; not changed by this run; not reviewed)': 179, 'PROPOSED BY THE AI WORKFLOW': 14}.

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

- before → after: {"a1": {"rows_before": 205, "rows_after": 207, "new": 2, "gone": 0}, "a3": {"before": 17, "after": 17, "enters": 0, "leaves": 0}, "a5": {"activities_before": 43, "activities_after": 43, "new": 0, "gone": 0}}

- ADD-03 is **PARTIAL** in the candidate (provisions unresolved): A3 and the A5 programme show the validated state (ADD-02); ADD-03 as proposed is in A1's `Status after ADD-03` column, in A2, in the candidate A3 and A5 below, in `a5/working/ADD-03.json` and in the diff below.

### Validated and candidate A3 / A5 (partial should not mean useless)

- **Validated** (unchanged; ADD-02): [a3/a3.pdf](../candidate/out/a3/a3.pdf) (one page), [a5/README.md](../candidate/out/a5/README.md), [a5/gantt.html](../candidate/out/a5/gantt.html)
- **Candidate** (CANDIDATE — NOT VALIDATED; ADD-03 as proposed): [a3/a3_candidate.pdf](../candidate/out/a3/a3_candidate.pdf) (9 page(s)), [a3/a3_candidate.md](../candidate/out/a3/a3_candidate.md), [a5/candidate/README.md](../candidate/out/a5/candidate/README.md), [a5/candidate/gantt.html](../candidate/out/a5/candidate/gantt.html)

**What may be changing.** ADD-03 is PARTIAL: 23 of 54 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 12 op(s) that are valid there stood (each still a proposal: review proposed 12), A3 would gain 0 row(s) (none), lose 0 (none) and change 1 (VOL-IV-F4F-02 (register)); A5, replanned at ADD-03's issue date (2026-11-15), would move the latest dates of 0 activities (none), add 0 (none) and remove 0 (none), and marks 5 REVIEW through relationships. Not settled: 11 activities blocked by an unresolved row (fin-model-build, technical-proposal, fin-model-freeze, form-4a-prep and 7 more), 2 STALE row(s), 0 obligation(s) reaching no output (C46), 0 relationship chain(s) blocked or incomplete, 8 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT and 6 more. Nothing here is validated, accepted or applied to the real state.

- CHANGES VOL-IV-F4F-02: now STALE; ops none (no op of the pending stage names it: a register-level difference; NOT SETTLED: ADD-03:3.3 UNRESOLVED: not promotable: ADD-03/3.3 insufficient_evidence (missing_information: the proposer declares missing: Limb (b) of the replacement (ADD-03:3.3(b)) is not carrie…; NOT SETTLED: STALE at ADD-03: its reading was not re-made (new dependency ADD-03:Q19; new dependency ADD-03:Q20; VOL-IV:F4-F/para1 changed since BASE (by ADD-03/Q19, ADD-03/Q20)))

- blockers: 23 unresolved provision(s), 11 blocked activit(y/ies), 2 STALE row(s), 0 C46 gap(s), 0 relationship chain(s) blocked or incomplete, 8 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT, I-VOL-III, I-ADD03-29.2-NO-OP, I-VOL-II-MISSING, I-VOL-V-MISSING, I-VOL-IV-SCALE, I-OP-ADD-01/Q4
- conditional scenarios: 0

**Image-read units** (the review packet of each region shows every crop beside its reading; translations are proposals, not evidence):

- ADD-03-p4-r1 (ADD-03 p4; reading pending): [packet](../candidate/build/review/ADD-03-p4-r1/packet.html); 18 unit(s) touched
  - `ADD-03:p4-image`: “Appendix A image (Arabic with English office name): Northern Region Airspace Safeguarding Office letter, Table 5-1 Maximum height of structures and equipment on the site”
  - `ADD-03:p4-image/hdr-en`: “Northern Region Airspace Safeguarding Office”
  - `ADD-03:p4-image/hdr-ar`: “مكتب حماية المجال الجوي بالمنطقة الشمالية”; translation (apart): ‘Northern Region Airspace Safeguarding Office’
  - `ADD-03:p4-image/date`: “التاريخ: ١٠ نوفمبر ٢٠٢٦م”; translation (apart): ‘Date: 10 November 2026 AD’
  - `ADD-03:p4-image/ref`: “الرقم: ٤٧١/٢٠٢٦”; translation (apart): ‘Reference number: 471/2026’
  - `ADD-03:p4-image/subject`: “الموضوع: اشتراطات الارتفاعات لموقع محطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان”; translation (apart): ‘Subject: Height requirements for the site of the Wadi Al-Sirhan Independent Sewage Treatment Plant’
  - `ADD-03:p4-image/tender-ref`: “مناقصة رقم: NUPA/ISTP/2026/014”; translation (apart): ‘Tender number: NUPA/ISTP/2026/014’
  - `ADD-03:p4-image/table-title`: “جدول ٥-١: الحدّ الأقصى لارتفاع المنشآت والمعدّات في الموقع”; translation (apart): ‘Table 5-1: Maximum height of structures and equipment on the site’
  - `ADD-03:p4-image/table-intro`: “يُحدِّد الحدّ الأقصى المسموح به للارتفاع في كل منطقة من مناطق الموقع على النحو الآتي:”; translation (apart): ‘The maximum permitted height in each zone of the site is set as follows:’
  - `ADD-03:p4-image/table-header`: “المنطقة / الوصف الحدّ الأقصى للارتفاع (متر فوق منسوب الأرض الطبيعية) / الإنارة التحذيرية”; translation (apart): ‘Column headings, right to left: Zone / Description / Maximum height (metres above natural ground level) / Warning lighting’; uncertain: no ruled grid was detected although the image shows a ruled table; columns are separated here with ' / ' in reading (right-to-left) order, which is a reading convention, not printed text
  - `ADD-03:p4-image/row-a`: “أ / الجزء من الموقع الواقع ضمن مسافة ١٬٥٠٠ متر من الحدّ الشرقي للموقع / ٢٥ مطلوبة”; translation (apart): ‘Zone A / The part of the site lying within a distance of 1,500 m of the eastern boundary of the site / 25 / Required’; uncertain: the thousands separator in ١٬٥٠٠ is read as the Arabic thousands separator (U+066C); it could be printed as an apostrophe-like mark; reviewer to confirm it is not a decimal mark (1.5); the descriptio…
  - `ADD-03:p4-image/row-b`: “ب / باقي مساحة الموقع ٤٠ / مطلوبة لأي جزء يزيد ارتفاعه على ٣٠ متراً”; translation (apart): ‘Zone B / Remainder of the site area / 40 / Required for any part whose height exceeds 30 metres’
  - … 6 more in `a3/a3_candidate.md`
- VOL-II-p3-r1 (VOL-II p3; reading approved): [packet](../candidate/build/review/VOL-II-p3-r1/packet.html); not touched by this addendum
- VOL-IV-p6-r1 (VOL-IV p6; reading approved): [packet](../candidate/build/review/VOL-IV-p6-r1/packet.html); not touched by this addendum

## Timings (wall clock per step)

| Step | Seconds | Status |
|---|---|---|
| ingest | 17.9 | done |
| readings | 209.3 | done |
| analysis | 2675.7 | done |
| validation | 3.4 | done |
| downstream | 1260.1 | done |
| downstream_validation | 0.8 | done |
| critic | 66.4 | done |
| promotion | 16.9 | done |
| pin | 1.1 | done |
| check_register | 3.3 | done |
| outputs | 85.6 | done |
| diff | 2.0 | done |
| review | 0.0 | running |
| **total** | **4342.5** (72.4 min) | target 30 min from the PDF to candidate outputs and this packet, human review excluded |

## Readings of the addendum's image regions (AI-proposed, PENDING HUMAN REVIEW)

Ingest first refused the candidate because these image regions had no reading (C05): ADD-03-p4-r1. Each reading below was proposed by the route of this run, checked by readings.check_reading and written into the candidate's readings; it is an interpretation of an image, never approved, and every unit made from it carries `reading.status: pending`.

- **ADD-03-p4-r1** — done; controller status **interpretation_pending**; unit `ADD-03:p4-image`; file `../candidate/curation/readings/ADD-03-p4-r1.yaml`
  - the reading beside its crops (the build's review packet): [../candidate/build/review/ADD-03-p4-r1/packet.html](../candidate/build/review/ADD-03-p4-r1/packet.html)
  - form reading, languages ['ar', 'en']; prepared by: AI-assisted: headless host session ADD-03-hostsession-20261005T025503Z-0189 (claude-code headless (opus); the CLI reported claude-opus-5-5), in AI workflow run ADD-03-run-host-blind05-20261005T025444Z (reading-ADD-03-p4-r1), 2026-10-05T02:58:19Z; proposed for a person's review, not approved
  - uncertainty: The table is ruled in the image but no grid was detected from pixels; rows are therefore read as band lines with ' | ' between cells in right-to-left reading order.
  - uncertainty: Band 5 is measured from x=34 although the printed text starts near x=625; the extra extent is taken to be speckle, not text.
  - uncertainty: The signature in band 13 left is a drawn stroke, not text; it is not transcribed.
  - uncertainty: Diacritics (shadda on الحدّ, المعدّات; damma/kasra on يُحدِّد, يُقاس; tanween on يوماً, متراً) were read on the enlarged crops.
  - uncertainty: prepared_by is left empty for the controller to write.

## First: unresolved provisions and escalations

23 of 54 provisions are not answered by a promoted item (each is `unresolved` in the candidate op file with the reason); 8 escalation(s).

- **ESCALATED ADD-03/2.1(b)** (ADD-03:2.1): ADD-03:2.1 prints 'Volume I Clauses 6.6 and 6.7 are deleted', so VOL-I:6.7 must be set to status deleted. In simulate_amendment the engine rejects set_status on VOL-I:6.7 under C22 ('declared target VOL-I:6.7 is not cited; the provision cites [VOL-I:6.6, VOL-I:6.1]'): its citation parser does not p…
  - unsupported: A set_status 'deleted' op on VOL-I:6.7 for provision ADD-03:2.1 cannot pass C22 with the current citation parsing; a person must record the deletion of 6.7 (or the citation list must be corrected). Without it VOL-I:6.7 stays active and its 'withdraw or modify ... at any time before the Proposal Due…
  - evidence: ADD-03:2.1 p1: “Volume I Clauses 6.6 and 6.7 are deleted and replaced by the following single Clause 6.6”; VOL-I:6.7 p3: “A Bidder may withdraw or modify its Proposal at any time before the Proposal Due Date by written notice through the Portal. No modification will be accepted th…”
  - affected scope: units VOL-I:6.1, VOL-I:6.6; rows VOL-I-6.1-01; activities assemble-envelope-a, assemble-envelope-b, copies, deliver, seal-and-mark; clarifications none
- **ESCALATED ADD-03/3.3(b)** (ADD-03:3.3(b)): ADD-03:3.3(b) is the second half of the replacement Clause 29.2 quoted in ADD-03:3.3. It sets the Indexed Proportion at 75% from year 11 and states that the balance remains fixed. It must become part of VOL-V:29.2. In the dry run, append_text with provision ADD-03:3.3(b) failed C22 ('the provision …
  - unsupported: A single quoted replacement that is split across two provision units (a clause and its child list item), where the child does not itself cite the target. A person must append '(b) from the start of the eleventh (11th) year of operations, seventy-five per cent (75%). The balance of the payment shall…
  - evidence: ADD-03:3.3(b) p1: “(b) from the start of the eleventh (11th) year of operations, seventy-five per cent (75%). The balance of the payment shall remain fixed.’”; ADD-03:3.3 p1: “Volume V Clause 29.2 is deleted and replaced by the following:”; VOL-V:29.2 p3: “forty per cent (40%) remaining fixed.”
  - affected scope: units none; rows none; activities none; clarifications none
- **ESCALATED ADD-03/7.2** (ADD-03:7.2): 7.2 sets a governing-language rule: the Arabic Table 5-1 (Appendix A image) governs over the English translation (Appendix B). The governing Arabic differs in substance from the English. Note 1 covers permanent and temporary structures, including cranes and construction equipment, where the English…
  - unsupported: No op type records a language-precedence rule between two renderings of a table inside the same addendum. The units affected (ADD-03:T5-1, ADD-03:p4-image) are not in force at ADD-02, so they cannot be targeted. A person must record the precedence and the resulting content of Table 5-1 once the Ara…
  - evidence: ADD-03:7.2 p3: “Table 5-1 is issued in the Arabic language. The Arabic text governs. The English translation at Appendix B is provided for convenience only.”; ADD-03:p4-image/note1 p4: “١. تسري هذه الحدود على جميع المنشآت الدائمة والمؤقتة، بما في ذلك المداخن والرافعات ومعدّات الإنشاء.”; ADD-03:p4-image/note2 p4: “٢. يُقاس الارتفاع من منسوب الأرض الطبيعية قبل أعمال التسوية والردم.”
  - affected scope: units none; rows none; activities none; clarifications none
- **ESCALATED ADD-03/7.3** (ADD-03:7.3): 7.3 imposes a new free-standing bidder obligation with a pre-PDD deadline: notify the Authority through the Portal of the zone and height of any structure, plant or equipment over 30 m, not later than three Working Days before the PDD. It amends no unit in force at ADD-02. annotate (adds_obligation…
  - unsupported: A free-standing addendum obligation with no existing target unit. It needs an A1 register row (row_new) and an A5 programme milestone, which a person must create. The scope ('structure, plant or equipment') may, under the governing Arabic note 1, include construction cranes.
  - evidence: ADD-03:7.3 p3: “A Bidder whose Proposal provides for any structure, plant or equipment at the site exceeding thirty (30) metres in height shall notify the Authority through th…”
  - affected scope: units none; rows none; activities none; clarifications none
- **ESCALATED ADD-03/7.4** (ADD-03:7.4): 7.4 imposes a free-standing bidder obligation ('Bidders shall reflect Table 5-1 in the Technical Proposal') that amends no unit in force at ADD-02. annotate (adds_obligation) on the new Clause 5.6 fails C22 (no target at ADD-02). It obliges, so no_effect is not available.
  - unsupported: A free-standing proposal-content obligation with no existing target. It needs an A1 register row created by a person. What Table 5-1 contains depends on the governing Arabic text (see the 7.2 issue).
  - evidence: ADD-03:7.4 p3: “Bidders shall reflect Table 5-1 in the Technical Proposal.”
  - affected scope: units none; rows none; activities none; clarifications none
- **ESCALATED ADD-03/AppB/para1** (ADD-03:AppB/para1): AppB/para1 makes the Arabic Table 5-1 (Appendix A image) govern over the English translation at Appendix B ('The Arabic text of Table 5-1 at Appendix A governs.'). The two versions differ materially: the English note (2) and column header use finished ground level after grading and filling, while t…
  - unsupported: The op types (replace_text, annotate, etc.) act on units as they stand at the previous stage (ADD-02). Both Table 5-1 versions are first issued by ADD-03 and are not_issued at ADD-02, so no op can record that one ADD-03 unit prevails over another. A person must decide how the register records that …
  - evidence: ADD-03:AppB/para1 p5: “This translation is provided for convenience only. The Arabic text of Table 5-1 at Appendix A governs.”; ADD-03:T5-1/note(2) p5: “Height is measured from finished ground level after grading and filling.”; ADD-03:p4-image/note2 p4: “٢. يُقاس الارتفاع من منسوب الأرض الطبيعية قبل أعمال التسوية والردم.”; ADD-03:p4-image/note1 p4: “١. تسري هذه الحدود على جميع المنشآت الدائمة والمؤقتة، بما في ذلك المداخن والرافعات ومعدّات الإنشاء.”
  - affected scope: units none; rows none; activities none; clarifications none
- **ESCALATED ADD-03/T5-1/note(1)** (ADD-03:T5-1/note(1)): The English note (1), 'These limits apply to all permanent structures, including stacks.', does not match the governing Arabic note 1 (reading pending). The Arabic applies the limits to permanent AND temporary structures, including stacks, cranes and construction equipment ('المنشآت الدائمة والمؤقت…
  - unsupported: No op type records a conflict between a non-governing translation and its governing image-read source; deciding which scope applies, and whether to raise a clarification, is for a person.
  - evidence: ADD-03:T5-1/note(1) p5: “These limits apply to all permanent structures, including stacks.”; ADD-03:p4-image/note1 p4: “١. تسري هذه الحدود على جميع المنشآت الدائمة والمؤقتة، بما في ذلك المداخن والرافعات ومعدّات الإنشاء.”; ADD-03:7.2 p3: “The Arabic text governs.”
  - affected scope: units none; rows none; activities none; clarifications none
- **ESCALATED ADD-03/T5-1/note(2)** (ADD-03:T5-1/note(2)): The English note (2), 'Height is measured from finished ground level after grading and filling.', and the English column heading 'm above finished ground level' give the opposite datum to the governing Arabic (readings pending). Arabic note 2 reads 'يُقاس الارتفاع من منسوب الأرض الطبيعية قبل أعمال …
  - unsupported: No op type records a conflict between a non-governing translation and its governing image-read source; which datum is applied, and whether to clarify, is for a person.
  - evidence: ADD-03:T5-1/note(2) p5: “Height is measured from finished ground level after grading and filling.”; ADD-03:p4-image/note2 p4: “٢. يُقاس الارتفاع من منسوب الأرض الطبيعية قبل أعمال التسوية والردم.”; ADD-03:p4-image/table-header p4: “الحدّ الأقصى للارتفاع (متر فوق منسوب الأرض الطبيعية)”; ADD-03:7.2 p3: “The Arabic text governs.”
  - affected scope: units none; rows none; activities none; clarifications none
- **UNRESOLVED ADD-03:cover/para3** (paragraph, p1): not promotable: ADD-03/cover/para3 conflicting (declared_conflicts: the proposer declares: The cover says the 6.6/6.7 consolidation is 'without change of substance', but ADD-03:2.1 shortens the modification window to two Workin…)
- **UNRESOLVED ADD-03:3.3** (clause, p1): not promotable: ADD-03/3.3 insufficient_evidence (missing_information: the proposer declares missing: Limb (b) of the replacement (ADD-03:3.3(b)) is not carried by this op: see the escalation ADD-03/3.3(b).); ADD-03/3.3-clar evidence_verified (dropped: )
- **UNRESOLVED ADD-03:5.1** (clause, p2): not promotable: ADD-03/5.1 conflicting (declared_conflicts: the proposer declares: ADD-03:cover/para3 names Volume II Clause 3.5 for the odour criterion; the operative provision 5.1 names Clause 3.4 and quotes words fou…)
- **UNRESOLVED ADD-03:5.2** (clause, p2): not promotable: ADD-03/5.2 insufficient_evidence (missing_information: the proposer declares missing: Demonstrating compliance needs the ESIA Figure 7-2 concentration, which is not in the evidence build.)
- **UNRESOLVED ADD-03:Q18** (table_row, p2): not promotable: ADD-03/Q18 insufficient_evidence (missing_information: the proposer declares missing: ESIA Figure 7-2 content (receptor and concentration) is not in the evidence build reviewed)
- **UNRESOLVED ADD-03:p4-image/table-header** (reading_block, p4): not promotable: ADD-03/p4-image/table-header conflicting (declared_conflicts: the proposer declares: ADD-03:T5-1)
- **UNRESOLVED ADD-03:p4-image/row-a** (reading_block, p4): not promotable: ADD-03/p4-image/row-a insufficient_evidence (missing_information: the proposer declares missing: approved reading of region ADD-03-p4-r1 (row A column split between ٢٥ and مطلوبة))
- **UNRESOLVED ADD-03:p4-image/row-b** (reading_block, p4): not promotable: ADD-03/p4-image/row-b insufficient_evidence (missing_information: the proposer declares missing: approved reading of region ADD-03-p4-r1 (row B column split between باقي مساحة الموقع and ٤٠))
- **UNRESOLVED ADD-03:p4-image/note1** (reading_block, p4): not promotable: ADD-03/p4-image/note1 conflicting (declared_conflicts: the proposer declares: ADD-03:T5-1/note(1))
- **UNRESOLVED ADD-03:p4-image/note2** (reading_block, p4): not promotable: ADD-03/p4-image/note2 conflicting (declared_conflicts: the proposer declares: ADD-03:T5-1/note(2))
- **UNRESOLVED ADD-03:p4-image/note3** (reading_block, p4): not promotable: ADD-03/p4-image/note3 insufficient_evidence (missing_information: the proposer declares missing: approved reading of region ADD-03-p4-r1)
- **UNRESOLVED ADD-03:p4-image/stamp** (reading_block, p4): not promotable: ADD-03/p4-image/stamp insufficient_evidence (missing_information: the proposer declares missing: The stamp prints no text, so no words can be quoted from it; whether the absence of a stamp impression matters for the letter's …)
- **UNRESOLVED ADD-03:T5-1/a** (table_row, p5): not promotable: ADD-03/T5-1/a conflicting (declared_conflicts: the proposer declares: English column heading 'm above finished ground level' against the Arabic heading 'متر فوق منسوب الأرض الطبيعية' (natural ground level))
- **UNRESOLVED ADD-03:T5-1/b** (table_row, p5): not promotable: ADD-03/T5-1/b conflicting (declared_conflicts: the proposer declares: English column heading 'm above finished ground level' against the Arabic heading 'متر فوق منسوب الأرض الطبيعية' (natural ground level))
- **UNRESOLVED ADD-03:T5-1/note(3)** (note, p5): not promotable: ADD-03/T5-1/note(3) insufficient_evidence (missing_information: the proposer declares missing: whether 'days' are calendar or working days (unqualified in the Arabic))

## Per provision: source evidence → proposed transition → validation → downstream impact → output difference

### ADD-03:cover/para1 (paragraph, p1) — answered
- source: “Issued 15 November 2026”
- transition: `ADD-03/cover/para1` disposition no_effect: the issue date line 'Issued 15 November 2026' (the stage date); it amends, obliges or excepts nothing
  - validation: **evidence_verified**

### ADD-03:cover/para2 (paragraph, p1) — answered
- source: “Tender NUPA/ISTP/2026/014”
- transition: `ADD-03/cover/para2` disposition no_effect: title line identifying the tender ('Tender NUPA/ISTP/2026/014'); it amends, obliges or excepts nothing
  - validation: **evidence_verified**

### ADD-03:cover/para3 (paragraph, p1) — UNRESOLVED
- source: “This Addendum consolidates Volume I Clauses 6.6 and 6.7 without change of substance, amends the definition of Availability Payment and the indexation of the Availability Payment under Volume V Clause 29.2, adds a membrane filtration requirement to Volume II Clause 3.1, replaces the odour criterion in Volume II Clause 3.5 by reference to the Environmental an…”
- transition: `ADD-03/cover/para3` amendment_op annotate ADD-03:cover/para3 effect adds_obligation
  - validation: **conflicting** — declared_conflicts: the proposer declares: The cover says the 6.6/6.7 consolidation is 'without change of substance', but ADD-03:2.1 shortens the modification window to two Working Days before the Proposal Due Date (S-I1).; The cover says …
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Annotation (adds_obligation) of Form 4-A acknowledgement is consistent with the cover text. The target is the provision itself, which is acceptable for a self-annotation, but the cover also lists changes to Vol V 29.2, Vol II 3.1/3.5/5.6 that are not applied here (stated as carried elsewhere).
    - concern: Real conflicts: cover says 'without change of substance' but ADD-03:2.1 shortens the modification window (old 6.7: any time before due date; new: 2 Working Days before). Also the cover cites an 'odour criterion' in Vol II 3.5 while the evidence shows VOL-II:3.5 as a noise criterion (S-I2). Both are…
    - concern: The statement that the Form 4-A acknowledgement is at paragraph 1 as reissued by ADD-01 rests on ADD-01 text only; ADD-01 span says it is added at paragraph 1, which is fine. Whether ADD-02 changed Form 4-A is not shown.
  - downstream proposal `DS-ADD03-ESC-COVER` escalation (esc:ADD-03:cover/para3): **conflicting**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-sonnet-5-5
      - concern: The conflict between the cover and ADD-03 5.1 is real. The cover says the odour criterion is in VOL-II 3.5, but VOL-II:3.5 is a noise limit (55/45 dB(A)). The odour limit is in VOL-II 3.4, and that is the clause 5.1 amends.
      - concern: The claim that 2.1 contradicts 'without change of substance' is not shown. ADD-03:2.1 and the original VOL-I 6.6/6.7 text are not printed in the units. Only the 2.1 quote about a two-Working-Day modification deadline is given. Without the earlier 6.6/6.7 wording, we can't tell whether that deadline…
      - concern: The statement that the Form 4-A units in units_after are all superseded is not in the printed evidence. The unclear acknowledgement version therefore can't be checked.
      - concern: The item cites 'VOL-I 3.2 precedence within a document'. The cover itself only says the addendum takes precedence over the RFP Documents. No VOL-I 3.2 text is shown.
      - concern: The 'unsupported downstream changes' list names rows, activities and clarifications that are not in the evidence. This part can't be checked.

### ADD-03:1.1 (clause, p1) — answered
- source: “This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.”
- transition: `ADD-03/1.1` disposition no_effect: Recital. 'This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.' It restates…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Reading as a recital with no_effect follows from the words. It does restate precedence, but VOL-I:3.2 and 5.3 texts are not printed in the evidence, so the claim that it merely restates existing precedence cannot be verified here.

### ADD-03:1.2 (clause, p1) — answered
- source: “A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.”
- transition: `ADD-03/1.2` disposition no_effect: Rule of reading for this Addendum's own references: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Add…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'unless')
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: It is a rule of reading for the Addendum's own references, so no_effect on unit text is reasonable. However, 'unless otherwise stated' could change which version a reference points to; the controller flagged it for a person. No instance of an 'otherwise stated' reference is shown in this evidence.

### ADD-03:1.3 (clause, p1) — answered
- source: “Requests for clarification received after the time stated in Volume I Clause 5.2 have not been answered.”
- transition: `ADD-03/1.3` disposition no_effect: Recital applying the existing rule in VOL-I:5.2 ('Requests received after that time will not be answered.'): 'Requests for clarification received after the tim…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Recital reporting that late clarification requests were not answered; consistent with the VOL-I:5.2 quotation. No unit text changed.

### ADD-03:2.1 (clause, p1) — UNRESOLVED
- source: “Volume I Clauses 6.6 and 6.7 are deleted and replaced by the following single Clause 6.6: ‘6.6 A Bidder may withdraw its Proposal at any time before the Proposal Due Date, and may modify its Proposal not later than two (2) Working Days before the Proposal Due Date, in each case by written notice through the Portal. A Proposal received after the time stated …”
- transition: `ADD-03/2.1(a)` amendment_op replace_text VOL-I:6.6 “A Proposal received after the time stated in Clause 6.1 will be rejected unopen…” → “A Bidder may withdraw its Proposal at any time before the Proposal Due Date, an…”
  - validation: **conflicting** — declared_conflicts: the proposer declares: Cover ADD-03:cover/para3 says 'without change of substance'; the new text moves the modification cut-off to two Working Days before the Proposal Due Date (S-I1).
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
    - concern: Replacement text matches ADD-03:2.1 verbatim and the previous value matches VOL-I:6.6. The op replaces 6.6 text only; the deletion of 6.7 is handled separately (2.1(b)), so the two must be applied together or 6.7 will conflict.
    - concern: Real conflict with the cover's 'without change of substance': modification now cut off 2 Working Days before due date (S-I1). The operative text governs only if a person confirms this.
    - concern: The 24 Nov 2026 cut-off depends on assumption S-A1 (due date 26 Nov 2026 from VOL-I:6.1, and 'Working Days' definition/calendar not shown); it needs confirmation, including whether the due date is moved elsewhere. Note that new text also adds that late modifications are rejected unopened, a substan…
- transition: `ADD-03/2.1(b)` escalation why: ADD-03:2.1 prints 'Volume I Clauses 6.6 and 6.7 are deleted', so VOL-I:6.7 must be set to status deleted. In simulate_amendment the engine rejects set_status on VOL-I:6.7 under C22 ('declared target …
  - validation: **escalated**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Escalation is appropriate: 2.1 prints that Clauses 6.6 and 6.7 are deleted, and VOL-I:6.7 is a separate unit that must be deleted. The stated reason (engine C22 citation parsing missing 6.7) is a tool limitation reported by the proposer; it is not shown in the evidence printed here, so it cannot be…
  - downstream proposal `DS-ADD03-ESC-21` escalation (esc:ADD-03:2.1): **escalated**

### ADD-03:2.2 (clause, p1) — answered
- source: “The number 6.7 is not reused. The Clauses of Volume I are not renumbered.”
- transition: `ADD-03/2.2` disposition no_effect: 'The number 6.7 is not reused. The Clauses of Volume I are not renumbered.' It confirms that no renumbering follows the deletion of 6.7 under ADD-03:2.1 (escal…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'renumbered')
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Words say 6.7 is not reused and no renumbering; no_effect on text is consistent. The controller flagged 'renumbered' as amendment language; a person should confirm. It depends on 6.7 actually being recorded as deleted (2.1(b)).

### ADD-03:3.1 (clause, p1) — answered
- source: “In Volume V Clause 1.1, ‘the annual payment calculated under Clause 29’ is deleted and ‘the annual payment, expressed at Base Date prices, calculated under Clause 29’ is substituted.”
- transition: `ADD-03/3.1` amendment_op replace_text VOL-V:1.1 “the annual payment calculated under Clause 29” → “the annual payment, expressed at Base Date prices, calculated under Clause 29”
  - validation: **evidence_verified**
  - downstream: units changed VOL-V:1.1; rows citing them none

### ADD-03:3.2 (clause, p1) — answered
- source: “The following new Clause 1.1A is inserted in Volume V after Clause 1.1: ‘1.1A Base Date means the date falling twenty-eight (28) days before the Proposal Due Date.’”
- transition: `ADD-03/3.2` amendment_op insert_unit VOL-V:1.1 “Base Date means the date falling twenty-eight (28) days before the Proposal Due Date.”
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: The printed number 1.1A is not held in the stored text (S-A1). A person should confirm this convention.
    - concern: The Base Date depends on the Proposal Due Date in force. The item correctly does not compute it.
  - downstream: units changed VOL-V:1.1+ADD-03; rows citing them none
  - downstream proposal `DS-ADD03-06` row_new (c46:ADD-03/3.2): **interpretation_pending**
  - output difference: NEW ADD-03-3.2-01

### ADD-03:3.3 (clause, p1) — UNRESOLVED
- source: “Volume V Clause 29.2 is deleted and replaced by the following: ‘29.2 The Availability Payment shall be indexed annually from the Base Date in accordance with Schedule 9. The proportion of the payment indexed to the published consumer price index (the Indexed Proportion) shall be: (a) until the end of the tenth (10th) year of operations, the percentage state…”
- transition: `ADD-03/3.3` amendment_op replace_text VOL-V:29.2 “The Availability Payment shall be indexed annually in accordance with Schedule …” → “The Availability Payment shall be indexed annually from the Base Date in accord…”
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: Limb (b) of the replacement (ADD-03:3.3(b)) is not carried by this op: see the escalation ADD-03/3.3(b).
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
    - concern: The op leaves VOL-V:29.2 ending in '; and' until limb (b) is appended. The effective text is incomplete in the meantime, as S-I1 says.
    - concern: The old text is located in the target, not quoted by the provision. The old words match VOL-V:29.2 exactly, but a person must confirm that 'deleted and replaced' means the whole clause.
    - concern: The change is substantive. It moves from a fixed 60/40 split to a Bidder-chosen 50-70% in the first ten years, plus a Base Date indexation start. The text is stored without the '29.2' label, in the same way as S-A1.
    - concern: The claim that the engine rejects limb (b) under C21/C22 is not visible in the evidence shown. Only the dry-run result is asserted.
- transition: `ADD-03/3.3-clar` clarification {"gap": "The new Clause 29.2(a) requires 'the percentage stated by the Bidder in Form 4-F' (50%-70%). At ADD-02, Form 4-F has no field for that percentage; its only indexation field is 'Indexation ba…
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: Only one Form 4-F field, 'Indexation basis assumed: Per Volume V Clause 29.2', is shown in the evidence. The claim that none of the 20 members is a field for the Indexed Proportion cannot be checked from what is printed.
    - concern: The gap is real on the evidence shown. Clause 29.2(a) refers to a percentage stated in Form 4-F, and the only indexation field points back to Clause 29.2.
    - concern: ADD-03 provisions outside this batch might reissue Form 4-F. The proposer admits this was not checked.
    - concern: The interim handling is a suggestion for a person to decide.
  - downstream proposal `DS-ADD03-04` escalation (row:VOL-V-29.2-01): **escalated**
  - downstream proposal `DS-ADD03-05` issue (row:VOL-V-29.2-01): **evidence_verified**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: The printed VOL-V:29.2 text is still the 60%/40% wording, and the controller validated it as verbatim after the ops. ADD-03 3.3 plainly says the clause is deleted and replaced. This supports the claim that the replacement was not applied.
      - concern: The statement that no promoted op exists for 3.3 comes from the proposer's statement. The op list is not printed here.
      - concern: The statement that Schedule 9 is missing is not in the evidence shown.
      - concern: The 75% from year 11 rests on a 3.3(b) quote that is not printed in the units.
  - downstream proposal `DS-ADD03-ESC-33` escalation (esc:ADD-03:3.3): **escalated**

### ADD-03:3.3(b) (list_item, p1) — UNRESOLVED
- source: “(b) from the start of the eleventh (11th) year of operations, seventy-five per cent (75%). The balance of the payment shall remain fixed.’”
- transition: `ADD-03/3.3(b)` escalation why: ADD-03:3.3(b) is the second half of the replacement Clause 29.2 quoted in ADD-03:3.3. It sets the Indexed Proportion at 75% from year 11 and states that the balance remains fixed. It must become part…
  - validation: **escalated**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: ADD-03:3.3(b) does contain limb (b), with 75% from year 11 and the balance fixed, and the closing quote. The text supports the escalation.
    - concern: The engine rejections (C22, C21) are asserted by the proposer. They are not shown in the evidence.
    - concern: A person must append limb (b) to 29.2, or 29.2 stays incomplete.
    - concern: The (a)/(b) split leaves a gap. Limb (a) ends at the tenth year of operations, and limb (b) starts at the eleventh. Nothing in the evidence shows a gap in coverage, but a person should confirm the operations-year counting.
  - downstream proposal `DS-ADD03-ESC-33B` escalation (esc:ADD-03:3.3(b)): **escalated**

### ADD-03:3.4 (clause, p1) — answered
- source: “Bidders shall reflect this Section 3 in the Financial Model submitted under Volume I Clause 10.3.”
- transition: `ADD-03/3.4` amendment_op annotate VOL-I:10.3 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The words 'shall reflect this Section 3' do impose an obligation without changing the text of VOL-I:10.3.
    - concern: The note mentions 'Base Date pricing'. That comes from ADD-03/3.1, which is not in the evidence shown.
    - concern: Whether the obligation is 'adds_obligation' or 'no_effect' is an interpretation. A person must confirm it.
  - downstream proposal `DS-ADD03-R01` row_reading (row:VOL-I-10.3-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-R02` row_reading (row:VOL-I-10.3-02): **interpretation_pending**
  - downstream proposal `DS-ADD03-09` activity (act:fin-model-build): **interpretation_pending**
  - downstream proposal `DS-ADD03-10` no_change (act:fin-model-freeze): **interpretation_pending**
  - downstream proposal `DS-ADD03-11` no_change (act:model-auditor-appoint): **interpretation_pending**
  - downstream proposal `DS-ADD03-12` no_change (act:model-audit-review): **interpretation_pending**
  - downstream proposal `DS-ADD03-13` no_change (act:model-audit-opinion): **interpretation_pending**
  - output difference: A5 REWORK fin-model-build; A5 REWORK fin-model-freeze; A5 REWORK model-audit-opinion; A5 REWORK model-audit-review; A5 REWORK model-auditor-appoint; A5 REVIEW (confirmed dependency) fin-model-build; A5 REVIEW (proposed relationship) fin-model-build; A5 REVIEW (confirmed dependency) fin-model-freeze; A5 REVIEW (proposed relationship) fin-model-freeze; A5 REVIEW (confirmed dependency) form-4f

### ADD-03:4.1 (clause, p2) — answered
- source: “In Volume II Clause 3.1, ‘The Authority does not mandate a particular process train.’ is deleted and ‘The treatment process shall include a membrane filtration step, either in the tertiary treatment stage or as part of a membrane bioreactor, with a nominal pore size not exceeding 0.1 µm. Subject to the preceding sentence, the Authority does not mandate a pa…”
- transition: `ADD-03/4.1` amendment_op replace_text VOL-II:3.1 “The Authority does not mandate a particular process train.” → “The treatment process shall include a membrane filtration step, either in the t…”
  - validation: **evidence_verified**
  - downstream: units changed VOL-II:3.1; rows citing them VOL-II-3.1-01
  - downstream proposal `DS-ADD03-R08` row_reading (row:VOL-II-3.1-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-ACT-TECH` activity (act:technical-proposal): **interpretation_pending**
  - output difference: CHANGED VOL-II-3.1-01; A5 REWORK technical-proposal

### ADD-03:4.2 (clause, p2) — answered
- source: “Bidders shall reflect this Section 4 in the process design submitted under Volume II Section 3.”
- transition: `ADD-03/4.2` amendment_op annotate VOL-II:S3 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The note's detail about a membrane filtration step with pore size not exceeding 0.1 µm comes from ADD-03 Section 4.1. That is not in the evidence shown, so it cannot be verified here.
    - concern: The target VOL-II:S3 is a group. The evidence is only its heading. The obligation attaches to the design submission, not to any text.
    - concern: Whether the obligation is 'adds_obligation' or 'no_effect' is an interpretation. A person must confirm it.

### ADD-03:5.1 (clause, p2) — UNRESOLVED
- source: “In Volume II Clause 3.4, ‘not more than 5 OU/m³ at the site boundary’ is deleted and ‘not more than the odour concentration shown for the nearest sensitive receptor in Figure 7-2 of the Environmental and Social Impact Assessment referred to in Volume II Clause 9.1, at that receptor’ is substituted. The basis of assessment (98th percentile hourly value) is u…”
- transition: `ADD-03/5.1` amendment_op replace_text VOL-II:3.4 “not more than 5 OU/m³ at the site boundary” → “not more than the odour concentration shown for the nearest sensitive receptor …”
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:cover/para3 names Volume II Clause 3.5 for the odour criterion; the operative provision 5.1 names Clause 3.4 and quotes words found only in 3.4 (3.5 is the noise clause).
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: Real conflict: ADD-03 cover/para3 names Clause 3.5 (the noise clause), but operative 5.1 names Clause 3.4 and quotes words found only in 3.4. The operative text and the quoted words support targeting 3.4, but a person should confirm which clause the cover summary intends.
    - concern: The new limit's numeric value (ESIA Figure 7-2) is not in the evidence, so the replacement cannot be expressed as a number. This is a declared gap.
    - concern: The replacement changes the location from site boundary to nearest sensitive receptor. The trailing words ', assessed as a 98th percentile hourly value' remain, which matches the statement that the basis is unchanged.
    - concern: The old string appears exactly once in 3.4 and matches verbatim, including the m³ superscript.
  - downstream proposal `DS-ADD03-ESC-51` escalation (esc:ADD-03:5.1): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
      - concern: The conflict is real. 5.1 amends VOL-II 3.4, whose text before the addendum is the 5 OU/m³ site-boundary limit, while the cover names 3.5. It is probably a cover misreference, but a person should decide that.
      - concern: The new limit is whatever Figure 7-2 of the ESIA shows. Only the VOL-II 9.1 phrase 'available in the data room' is quoted, and the ESIA itself is not in the evidence, so the numeric criterion can't be stated. The item says this correctly.
      - concern: Statements such as 'the 5.1 op is not promotable' and the listed downstream rows go beyond the printed evidence. They are process or controller matters and can't be verified here.

### ADD-03:5.2 (clause, p2) — UNRESOLVED
- source: “Bidders shall demonstrate compliance with Volume II Clause 3.4, as amended, in the Technical Proposal.”
- transition: `ADD-03/5.2` amendment_op annotate VOL-II:3.4 effect adds_obligation
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: Demonstrating compliance needs the ESIA Figure 7-2 concentration, which is not in the evidence build.
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The obligation to demonstrate compliance in the Technical Proposal is clearly stated in ADD-03:5.2, so the adds_obligation annotation is plausible. But the interpretation I1 that it is a new obligation, not confirming an existing one, has no evidence attached. The evidence shown does not include an…
    - concern: Compliance demonstration depends on the ESIA Figure 7-2 value, which is not in the evidence, and on 5.1 and its unresolved cover-page conflict (Clause 3.4 vs 3.5). It therefore stays pending a person's confirmation.
    - concern: Controller status is insufficient_evidence, which is consistent with this.
  - downstream proposal `ESC-ADD03-5.2` escalation (esc:ADD-03:5.2): **escalated**

### ADD-03:Q15 (table_row, p2) — answered
- source: “No: 15 | Bidder question: Volume II Clause 6.4 requires process data to be retained for not less than seven (7) years. Would a retention period of ten (10) years be acceptable? | Authority response: Volume II Clause 6.4 states a minimum period. A Bidder may propose a longer period but is not required to do so.”
- transition: `ADD-03/Q15` amendment_op annotate VOL-II:6.4 effect interprets
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - downstream proposal `DS-ADD03-R09` row_reading (row:VOL-II-6.4-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-R10` row_reading (row:VOL-II-6.4-02): **interpretation_pending**
  - output difference: A5 REWORK technical-proposal

### ADD-03:Q16 (table_row, p2) — answered
- source: “No: 16 | Bidder question: May a Bidder state ‘no deviations’ in Form 4-E and set out its assumptions on Volume V in the Technical Proposal? | Authority response: A Bidder that states ‘no deviations’ in Form 4-E shall not include any qualification of Volume V elsewhere in its Proposal. An assumption that limits or qualifies an obligation in Volume V is a qua…”
- transition: `ADD-03/Q16` amendment_op annotate VOL-I:9.6, VOL-IV:F4-E effect interprets
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: Payload note says a 'no deviations' statement precludes any qualification elsewhere; this comes from the response's first sentence, which is supported. Clause 9.6 itself only makes such a Proposal non-responsive, so the response adds the 'shall not' wording. Target is 9.6 with Form 4-E as a second …
  - downstream proposal `DS-ADD03-R06` row_reading (row:VOL-I-9.6-01): **interpretation_pending**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: The evidence shown for VOL-I 9.6 is only the Form 4-E listing sentence. The 'no deviations' non-responsive consequence quote was checked only through the controller's register validation, not through printed text.
      - concern: Whether the concession-term point is a deviation is left open and is not decided by this reading.
  - downstream proposal `DS-ADD03-R11` row_reading (row:VOL-IV-F4E-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-ACT-DEVREV` activity (act:deviations-review): **interpretation_pending**
  - downstream proposal `DS-ADD03-ACT-F4E` activity (act:form-4e): **interpretation_pending**
  - output difference: CHANGED VOL-IV-F4E-01; A5 REWORK deviations-review; A5 REWORK form-4e

### ADD-03:Q17 (table_row, p2) — answered
- source: “No: 17 | Bidder question: Where the proposed EPC Contractor is an unincorporated joint venture, which entity must hold the ISO 9001:2015 certificate required by Volume I Clause 8.3? | Authority response: Each member of the joint venture shall hold a certificate that meets Volume I Clause 8.3, and a copy of each certificate shall be submitted with Envelope A.”
- transition: `ADD-03/Q17` amendment_op annotate VOL-I:8.3 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Clause 8.3 text is unchanged. The response adds a per-member requirement, so 'adds_obligation' fits. Cited evidence for the clause is only the first sentence.
  - downstream proposal `DS-ADD03-R05` row_reading (row:VOL-I-8.3-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-ACT-ISO` activity (act:iso-copy): **interpretation_pending**
  - output difference: A5 REWORK iso-copy

### ADD-03:Q18 (table_row, p2) — UNRESOLVED
- source: “No: 18 | Bidder question: Will the Authority provide dispersion modelling inputs for the design of the odour control system? | Authority response: The nearest sensitive receptor, and the odour concentration applicable at it for the purposes of Volume II Clause 3.4 as amended by Section 5 of this Addendum, are shown in Figure 7-2 of the Environmental and Soc…”
- transition: `ADD-03/Q18` amendment_op annotate VOL-II:3.4 effect interprets
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: ESIA Figure 7-2 content (receptor and concentration) is not in the evidence build reviewed
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The response points to ESIA Figure 7-2, which is not in the evidence, so the receptor and concentration cannot be checked. The proposer declares this missing.
    - concern: The response refers to Clause 3.4 'as amended by Section 5', and the amendment is not in the evidence. VOL-II:3.4 as printed says 'site boundary', so the response may conflict with it or change it. This cannot be judged from this evidence.
    - concern: The controller status is insufficient_evidence, so this should not be treated as a clean interpretation.
  - downstream proposal `ESC-ADD03-Q18` escalation (esc:ADD-03:Q18): **escalated**

### ADD-03:Q19 (table_row, p2) — answered
- source: “No: 19 | Bidder question: Form 4-F requests the Availability Payment for year 1 of operations. Is that figure to be stated in the prices of year 1 of operations? | Authority response: Yes. The Availability Payment stated in Form 4-F is the amount payable for year 1 of operations, in the prices of that year. Indexation under Volume V Clause 29.2 applies from…”
- transition: `ADD-03/Q19` amendment_op annotate VOL-IV:F4-F, VOL-V:29.2 effect interprets
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The proposer flags possible tension with ADD-03:3.1 and 3.3 (Base Date prices and indexation), which are not in the evidence. The response says year 1 prices and indexation from the first anniversary of PCOD. A person should check this.
    - concern: The VOL-V:29.2 text shown is only a fragment. It mentions Schedule 9 and does not show when indexation starts, so the start point cannot be compared with the response.
  - downstream proposal `DS-ADD03-I01` issue (row:VOL-IV-F4F-01): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
      - concern: The conflict is real on the words. Q19 states year 1 prices with indexation from the first anniversary of PCOD. 3.1 states Base Date prices, and 3.3 indexes annually from the Base Date.
      - concern: The Base Date definition in 3.2 and the content of Schedule 9 are not in the evidence shown. The proposer correctly lists them as missing, so the conflict cannot be resolved from the pack.
  - downstream proposal `DS-ADD03-CQ01` clarification_item (row:VOL-IV-F4F-01): **insufficient_evidence** — held back: linked issues not promotable: ['I-ADD03-AP-PRICE-BASIS']
  - downstream proposal `DS-ADD03-02` issue (row:VOL-IV-F4F-02): **interpretation_pending**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: The conflict follows from the quoted words: Base Date prices indexed from the Base Date (3.1, 3.3), against year 1 prices indexed from the first anniversary of PCOD (Q19).
      - concern: The Base Date being 28 days before the PDD is not in the evidence shown.
      - concern: The 2026-11-12 clarification cut-off and the 2026-11-15 issue date are not in the evidence shown.
      - concern: The 75% from year 11 rests on a 3.3(b) quote. The printed 3.3 text is truncated after '(a)... and'. That quote is not in this item's own evidence list.
      - concern: The ADD-03 3.4 Financial Model reference is not in the evidence shown.
      - concern: Pending a person's decision on the price basis.
  - downstream proposal `DS-ADD03-03` clarification_item (row:VOL-IV-F4F-02): **interpretation_pending**

### ADD-03:Q20 (table_row, p2) — answered
- source: “No: 20 | Bidder question: Form 4-F states ‘Per Volume V Clause 29.2’ against ‘Indexation basis assumed’. Is any figure to be stated in that row? | Authority response: Yes. The Bidder shall complete that row by stating, after the words ‘Per Volume V Clause 29.2’, the Indexed Proportion as a percentage. The Indexed Proportion shall not be stated anywhere in E…”
- transition: `ADD-03/Q20` amendment_op annotate VOL-IV:F4-F, VOL-I:6.2 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: Real conflict. Response 20 requires the Indexed Proportion to be stated in Form 4-F. It also says the Proportion must not appear anywhere in Envelope A. VOL-I:6.2 makes any commercial information in Envelope A non-responsive. The evidence does not show whether Form 4-F is in Envelope A or in anothe…
    - concern: The proposer states that I-Q20 'confirms the Indexed Proportion is commercial information'. The response does not say so. It only says it must not be in Envelope A and that 6.2 applies.
    - concern: 'Indexed Proportion' is defined in ADD-03:3.3, which is not in the evidence.
  - downstream proposal `DS-ADD03-R03` row_reading (row:VOL-I-6.2-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-R04` row_reading (row:VOL-I-6.2-02): **interpretation_pending**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: The reading is an interpretation. Q20 says only that Clause 6.2 applies, and 'other commercial information' is not defined, so a person must confirm it.
      - concern: Q20 also requires the figure in the Form 4-F row. The evidence shown does not say which envelope Form 4-F belongs to, so the reading depends on Form 4-F being outside Envelope A.
  - downstream proposal `DS-ADD03-R12` row_reading (row:VOL-IV-F4F-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-01` row_reading (row:VOL-IV-F4F-02): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
      - concern: The conflict is real on the words shown. Q19 says year 1 prices with indexation from the first anniversary of PCOD. ADD-03 3.3 says indexation runs 'from the Base Date', and the 3.1 quote says 'expressed at Base Date prices'.
      - concern: The 3.1 text is not printed in the units. I relied on the controller's verbatim check of that quote.
      - concern: The claim that Q20's field is not a qualification is an interpretation, and a person must confirm it. The target sentence is unchanged and states no consequence.
      - concern: Q20 also says 'Volume I Clause 6.2 applies'. The item does not discuss it, and its text is not in the evidence.
      - concern: The Base Date being 28 days before the PDD is not in the evidence shown.
  - downstream proposal `DS-ADD03-14` no_change (act:deliver): **interpretation_pending**
  - downstream proposal `DS-ADD03-15` no_change (act:seal-and-mark): **interpretation_pending**
  - downstream proposal `DS-ADD03-16` no_change (act:copies): **interpretation_pending**
  - downstream proposal `DS-ADD03-ACT-ENV-A` activity (act:assemble-envelope-a): **interpretation_pending**
  - downstream proposal `DS-ADD03-NC-ENV-B` no_change (act:assemble-envelope-b): **interpretation_pending**
  - downstream proposal `DS-ADD03-ACT-F4F` activity (act:form-4f): **interpretation_pending**
  - output difference: CHANGED VOL-IV-F4F-01; A5 REWORK assemble-envelope-a; A5 REWORK assemble-envelope-b; A5 REWORK copies; A5 REWORK deliver; A5 REWORK fin-model-build; A5 REWORK fin-model-freeze; A5 REWORK form-4f; A5 REWORK seal-and-mark; A5 REVIEW (confirmed dependency) fin-model-build; A5 REVIEW (proposed relationship) fin-model-build; A5 REVIEW (confirmed dependency) fin-model-freeze; A5 REVIEW (proposed relationship) fin-model-freeze; A5 REVIEW (confirmed dependency) form-4f; A5 REVIEW (proposed relationship) form-4f

### ADD-03:Q21 (table_row, p2) — answered
- source: “No: 21 | Bidder question: Does the Technical Proposal need to address construction plant in addition to the matters listed in Volume I Clause 9.7? | Authority response: Yes. The construction methodology in the Technical Proposal shall include a crane and lifting plan that demonstrates compliance with Table 5-1 (Volume II Clause 5.6, inserted by Section 7 of…”
- transition: `ADD-03/Q21` amendment_op annotate VOL-I:9.7 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Clause 5.6 and Table 5-1 are not in the evidence, so the content of the crane and lifting plan requirement cannot be checked. This is acknowledged in the item and is a dependency on ADD-03:7.1.
  - downstream proposal `DS-ADD03-R07` row_reading (row:VOL-I-9.7-01): **interpretation_pending**
  - output difference: A5 REWORK technical-proposal

### ADD-03:7.1 (clause, p2) — answered
- source: “The following new Clause 5.6 is inserted in Volume II after Clause 5.5: ‘5.6 The Project Company shall comply with the height limits in Table 5-1, which is reproduced at Appendix A to this Addendum as issued by the Northern Region Airspace Safeguarding Office and is incorporated into this Volume by reference.’”
- transition: `ADD-03/7.1` amendment_op insert_unit VOL-II:5.5 “The Project Company shall comply with the height limits in Table 5-1, which is reproduced at Appendix A to this Addendu…”
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: VOL-II:5.5 is only the insertion anchor and stays unchanged, which matches the provision text. The new clause incorporates Table 5-1 by reference, so what it requires depends on the Arabic Appendix A reading, which is still pending. The rationale's description of the crop (zone values, letter refer…
  - downstream: units changed VOL-II:5.5+ADD-03; rows citing them none
  - downstream proposal `DS-ADD03-07` row_new (c46:ADD-03/7.1): **interpretation_pending**
  - downstream proposal `DS-ADD03-08` issue (c46:ADD-03/7.1): **interpretation_pending**
  - output difference: NEW ADD-03-7.1-01

### ADD-03:7.2 (clause, p3) — UNRESOLVED
- source: “Table 5-1 is issued in the Arabic language. The Arabic text governs. The English translation at Appendix B is provided for convenience only.”
- transition: `ADD-03/7.2` escalation why: 7.2 sets a governing-language rule: the Arabic Table 5-1 (Appendix A image) governs over the English translation (Appendix B). The governing Arabic differs in substance from the English. Note 1 cover…
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:T5-1/note(1); ADD-03:T5-1/note(2)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The Arabic notes are a pending image reading, and the item says so. My own reading of the Arabic matches the proposer's: note 1 covers permanent and temporary structures including stacks, cranes and construction equipment. Note 2 measures from natural ground before grading and filling.
    - concern: The English notes in the evidence are the permanent-structures note and the finished-ground-level note, so the two conflicts are real.
    - concern: I2's claim that the Arabic is the more restrictive reading holds only where the site is filled. If the site is cut, the effect reverses. The statement should be conditional.
    - concern: Whether 7.2 has any effect depends on the target. T5-1 is not yet in force at ADD-02, so no existing op type can record the precedence. Escalation is a reasonable choice, but it rests on the C22 failure, which is not printed in the evidence.
- transition: `ADD-03/7.2/issue` issue {"text": "The governing Arabic Table 5-1 (ADD-03 Appendix A) differs from the convenience English translation (Appendix B) in two places. (1) Scope: the Arabic note 1 applies the limits to permanent …
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:T5-1/note(1); ADD-03:T5-1/note(2)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The headline 'wider and stricter' overstates the datum point. The Arabic is stricter only if the finished level is above natural ground (fill). The item lists fill depths as missing, which supports this caveat.
    - concern: The references to Q21 and the 7.3 notification of items over 30 m are not backed by evidence shown here.
    - concern: Everything depends on the pending Appendix A Arabic reading, which is a reading and not yet an approved text.
  - downstream proposal `ESC-ADD03-7.2` escalation (esc:ADD-03:7.2): **escalated**

### ADD-03:7.3 (clause, p3) — UNRESOLVED
- source: “A Bidder whose Proposal provides for any structure, plant or equipment at the site exceeding thirty (30) metres in height shall notify the Authority through the Portal, not later than three (3) Working Days before the Proposal Due Date, of the zone of Table 5-1 in which it is to be located and its proposed height.”
- transition: `ADD-03/7.3` escalation why: 7.3 imposes a new free-standing bidder obligation with a pre-PDD deadline: notify the Authority through the Portal of the zone and height of any structure, plant or equipment over 30 m, not later tha…
  - validation: **escalated** — missing_information: the proposer declares missing: The PDD at ADD-03 (other batches); Whether temporary cranes count as 'equipment' for 7.3 (Arabic note 1)
  - downstream proposal `ESC-ADD03-7.3` escalation (esc:ADD-03:7.3): **escalated**

### ADD-03:7.4 (clause, p3) — UNRESOLVED
- source: “Bidders shall reflect Table 5-1 in the Technical Proposal.”
- transition: `ADD-03/7.4` escalation why: 7.4 imposes a free-standing bidder obligation ('Bidders shall reflect Table 5-1 in the Technical Proposal') that amends no unit in force at ADD-02. annotate (adds_obligation) on the new Clause 5.6 fa…
  - validation: **escalated** — missing_information: the proposer declares missing: Approval of the Appendix A Arabic reading
  - downstream proposal `ESC-ADD03-7.4` escalation (esc:ADD-03:7.4): **escalated**

### ADD-03:AppA/para1 (paragraph, p4) — answered
- source: “Table 5-1 is reproduced below as issued by the Northern Region Airspace Safeguarding Office. The Arabic text governs in accordance with Section 7 of this Addendum.”
- transition: `ADD-03/AppA/para1` disposition no_effect: This is an introductory paragraph to Appendix A. 'Table 5-1 is reproduced below as issued by the Northern Region Airspace Safeguarding Office' describes the re…
  - validation: **evidence_verified**

### ADD-03:p4-image/hdr-en (reading_block, p4) — answered
- source: “Northern Region Airspace Safeguarding Office”
- transition: `ADD-03/p4-image/hdr-en` disposition no_effect: Letterhead of the issuing office ('Northern Region Airspace Safeguarding Office') on the Appendix A image; it identifies the issuer and changes no unit. The in…
  - validation: **evidence_verified**

### ADD-03:p4-image/hdr-ar (reading_block, p4) — answered
- source: “مكتب حماية المجال الجوي بالمنطقة الشمالية”
- transition: `ADD-03/p4-image/hdr-ar` disposition no_effect: Arabic letterhead 'مكتب حماية المجال الجوي بالمنطقة الشمالية' naming the issuing office; it changes no unit.
  - validation: **evidence_verified**

### ADD-03:p4-image/date (reading_block, p4) — answered
- source: “التاريخ: ١٠ نوفمبر ٢٠٢٦م”
- transition: `ADD-03/p4-image/date` disposition no_effect: Letter date 'التاريخ: ١٠ نوفمبر ٢٠٢٦م' of the Appendix A letter; a document identifier that sets no time limit and changes no unit.
  - validation: **evidence_verified**

### ADD-03:p4-image/ref (reading_block, p4) — answered
- source: “الرقم: ٤٧١/٢٠٢٦”
- transition: `ADD-03/p4-image/ref` disposition no_effect: Letter reference number 'الرقم: ٤٧١/٢٠٢٦'; an identifier only, it changes no unit.
  - validation: **evidence_verified**

### ADD-03:p4-image/subject (reading_block, p4) — answered
- source: “الموضوع: اشتراطات الارتفاعات لموقع محطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان”
- transition: `ADD-03/p4-image/subject` disposition no_effect: Subject line 'الموضوع: اشتراطات الارتفاعات لموقع محطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان'; it describes the letter's subject and changes no unit.
  - validation: **evidence_verified**

### ADD-03:p4-image/tender-ref (reading_block, p4) — answered
- source: “مناقصة رقم: NUPA/ISTP/2026/014”
- transition: `ADD-03/p4-image/tender-ref` disposition no_effect: Tender reference 'مناقصة رقم: NUPA/ISTP/2026/014'; an identifier, it changes no unit.
  - validation: **evidence_verified**

### ADD-03:p4-image/table-title (reading_block, p4) — answered
- source: “جدول ٥-١: الحدّ الأقصى لارتفاع المنشآت والمعدّات في الموقع”
- transition: `ADD-03/p4-image/table-title` disposition no_effect: Title of Table 5-1 'جدول ٥-١: الحدّ الأقصى لارتفاع المنشآت والمعدّات في الموقع'; a caption. The table is inserted/incorporated by ADD-03:7.1, not by this title.
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Evidence for ADD-03:7.1 supports that the table is incorporated by reference there, so a caption having no independent effect is consistent. The 'inserts Volume II Clause 5.6' part of F2 is not shown in the quoted words of 7.1, but this does not affect the no_effect conclusion. The reading text is …

### ADD-03:p4-image/table-intro (reading_block, p4) — answered
- source: “يُحدِّد الحدّ الأقصى المسموح به للارتفاع في كل منطقة من مناطق الموقع على النحو الآتي:”
- transition: `ADD-03/p4-image/table-intro` disposition no_effect: Lead-in 'يُحدِّد الحدّ الأقصى المسموح به للارتفاع في كل منطقة من مناطق الموقع على النحو الآتي:' introduces the zone rows; the limits themselves are in the tabl…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The lead-in says the maximum permitted height in each zone is determined 'as follows', which is introductory. The limits and their binding force sit in the rows and in 7.1, so no_effect is consistent. It depends on the table rows (not shown) carrying the actual limits. F2's reference to inserting C…

### ADD-03:p4-image/table-header (reading_block, p4) — UNRESOLVED
- source: “المنطقة | الوصف الحدّ الأقصى للارتفاع (متر فوق منسوب الأرض الطبيعية) | الإنارة التحذيرية”
- transition: `ADD-03/p4-image/table-header` disposition unresolved: Insufficient evidence for a settled effect. The governing Arabic heading 'متر فوق منسوب الأرض الطبيعية' (metres above natural ground level) conflicts with the …
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:T5-1
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The Arabic heading says natural ground level. The Appendix B quote (finished ground level) appears only in the statement S3 and the T5-1/a unit is not printed here.
    - concern: The reading's column separators are incomplete (الوصف and الحدّ الأقصى are run together), so a person must correct the structure.
  - downstream proposal `ESC-ADD03-P4-HEADER` escalation (esc:ADD-03:p4-image/table-header): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
      - concern: The conflict with ADD-03:T5-1 is declared by the proposer. The English T5-1 text is not printed, so I cannot confirm the conflict independently.
      - concern: The merged-cell claim is plausible. The header reads 'الوصف الحدّ الأقصى للارتفاع ...' with no separator between 'الوصف' and the height column, so the column split is unclear.
      - concern: The approved reading of region ADD-03-p4-r1 is missing, as the proposer says. Escalation to a person is appropriate.

### ADD-03:p4-image/row-a (reading_block, p4) — UNRESOLVED
- source: “أ | الجزء من الموقع الواقع ضمن مسافة ١٬٥٠٠ متر من الحدّ الشرقي للموقع | ٢٥ مطلوبة”
- transition: `ADD-03/p4-image/row-a` disposition no_effect: This is a row of the newly issued Table 5-1 ('أ | الجزء من الموقع الواقع ضمن مسافة ١٬٥٠٠ متر من الحدّ الشرقي للموقع | ٢٥ مطلوبة'). It prints no amendment to an…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: approved reading of region ADD-03-p4-r1 (row A column split between ٢٥ and مطلوبة)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Row A's words add no amendment to any ADD-02 unit, so no_effect on ADD-02 units is consistent. The row is still a substantive height limit that takes effect through 7.1, so the register must link it there.
    - concern: The claim that Arabic and Appendix B agree (1,500 m, lighting) is interpretation S6. Only the '25' is quoted from Appendix B, so the rest is unverified.
    - concern: The reading is unapproved and ٢٥ and مطلوبة are run together.
  - downstream proposal `ESC-ADD03-P4-ROWA` escalation (esc:ADD-03:p4-image/row-a): **escalated**

### ADD-03:p4-image/row-b (reading_block, p4) — UNRESOLVED
- source: “ب | باقي مساحة الموقع ٤٠ | مطلوبة لأي جزء يزيد ارتفاعه على ٣٠ متراً”
- transition: `ADD-03/p4-image/row-b` disposition no_effect: This is a row of the newly issued Table 5-1 ('ب | باقي مساحة الموقع ٤٠ | مطلوبة لأي جزء يزيد ارتفاعه على ٣٠ متراً'). It prints no amendment to any unit standin…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: approved reading of region ADD-03-p4-r1 (row B column split between باقي مساحة الموقع and ٤٠)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The same limits apply as for row A. The reading is unapproved and باقي مساحة الموقع and ٤٠ are run together.
    - concern: The claim that Arabic and Appendix B agree (40 m, lighting above 30 m) has no Appendix B quotation printed.
    - concern: This row carries the operative 40 m limit and the lighting requirement. A no_effect label must not hide that it takes effect via 7.1.
  - downstream proposal `ESC-ADD03-P4-ROWB` escalation (esc:ADD-03:p4-image/row-b): **escalated**

### ADD-03:p4-image/notes-head (reading_block, p4) — answered
- source: “ملاحظات:”
- transition: `ADD-03/p4-image/notes-head` disposition no_effect: 'ملاحظات:' (Notes:) is only a heading introducing the notes to Table 5-1. It prints no change, obligation or exception.
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5

### ADD-03:p4-image/note1 (reading_block, p4) — UNRESOLVED
- source: “١. تسري هذه الحدود على جميع المنشآت الدائمة والمؤقتة، بما في ذلك المداخن والرافعات ومعدّات الإنشاء.”
- transition: `ADD-03/p4-image/note1` disposition unresolved: Insufficient evidence for a settled effect. The governing Arabic Note 1 ('تسري هذه الحدود على جميع المنشآت الدائمة والمؤقتة، بما في ذلك المداخن والرافعات ومعدّ…
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:T5-1/note(1)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The Arabic reading is verbatim and the unresolved status is justified. The Appendix B text is quoted only in S5.
    - concern: The reading is unapproved.
  - downstream proposal `ESC-ADD03-P4-NOTE1` escalation (esc:ADD-03:p4-image/note1): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
      - concern: The English note (1) in ADD-03:T5-1 is not printed in the evidence, so the claimed conflict rests on the proposer's declaration.
      - concern: The Arabic text is quoted accurately: it covers permanent and temporary structures, including stacks, cranes and construction equipment.
      - concern: The link to the crane plan under Q21 is not supported by any evidence shown here.
      - concern: The reading has no approval, so escalation is reasonable.

### ADD-03:p4-image/note2 (reading_block, p4) — UNRESOLVED
- source: “٢. يُقاس الارتفاع من منسوب الأرض الطبيعية قبل أعمال التسوية والردم.”
- transition: `ADD-03/p4-image/note2` disposition unresolved: Insufficient evidence for a settled effect. The governing Arabic Note 2 ('يُقاس الارتفاع من منسوب الأرض الطبيعية قبل أعمال التسوية والردم') measures height fro…
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:T5-1/note(2)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The Arabic reading is verbatim and the datum opposition with Appendix B is quoted in S4.
    - concern: The Arabic table-header datum and Note 2 are consistent with each other, so the conflict is with Appendix B only. The reading is unapproved.
  - downstream proposal `ESC-ADD03-P4-NOTE2` escalation (esc:ADD-03:p4-image/note2): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
      - concern: The English note (2) is not printed, so the conflict is unverified beyond the proposer's declaration.
      - concern: The Arabic text is quoted accurately: height is measured from natural ground level before grading and fill.
      - concern: The reading has no approval, so the height datum stays unsettled and escalation is reasonable.

### ADD-03:p4-image/note3 (reading_block, p4) — UNRESOLVED
- source: “٣. يجب إخطار المكتب قبل ثلاثين (٣٠) يوماً على الأقل من تركيب أي رافعة في الموقع.”
- transition: `ADD-03/p4-image/note3` disposition no_effect: The words oblige ('يجب إخطار المكتب قبل ثلاثين (٣٠) يوماً على الأقل من تركيب أي رافعة في الموقع': the Office must be notified at least thirty (30) days before …
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: approved reading of region ADD-03-p4-r1
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The words contain an obligation ('يجب' = must; 30 days' notice before any crane). Labelling it no_effect risks losing it.
    - concern: The reason says it binds through 7.1's 'shall comply with the height limits in Table 5-1'. A crane-notice duty is not clearly a 'height limit', so this does not clearly follow from 7.1's words. It depends on the incorporation by reference of the whole table including notes.
    - concern: The claim that Appendix B Note (3) agrees is not supported by any quotation shown.
    - concern: The reading is unapproved.
  - downstream proposal `ESC-ADD03-P4-NOTE3` escalation (esc:ADD-03:p4-image/note3): **escalated**

### ADD-03:p4-image/signatory (reading_block, p4) — answered
- source: “مدير المكتب”
- transition: `ADD-03/p4-image/signatory` disposition no_effect: 'مدير المكتب' (the Office Director) is only the signatory's title on the issuing letter. It prints no change, obligation or exception.
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5

### ADD-03:p4-image/stamp (reading_block, p4) — UNRESOLVED
- source: “”
- transition: `ADD-03/p4-image/stamp` disposition no_effect: The stamp reading block has empty source text: the image shows only an empty oval outline beside the signatory line 'مدير المكتب'; it prints no words, so it am…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: The stamp prints no text, so no words can be quoted from it; whether the absence of a stamp impression matters for the letter's validity is not established by the evidence.
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Evidence is only a crop hash and empty text; I could not view the image, so the 'empty oval' description rests on the proposer's account. The no_effect conclusion follows from there being no words, but the controller marked insufficient_evidence and whether an unfilled stamp affects the letter's au…
  - downstream proposal `ESC-ADD03-P4-STAMP` escalation (esc:ADD-03:p4-image/stamp): **escalated**

### ADD-03:AppA/para2 (paragraph, p4) — answered
- source: “End of reproduction.”
- transition: `ADD-03/AppA/para2` disposition no_effect: 'End of reproduction.' only marks the end of the reproduced Arabic Table 5-1 at Appendix A; it contains no shall/must/unless words and changes no unit.
  - validation: **evidence_verified**

### ADD-03:AppB/para1 (paragraph, p5) — UNRESOLVED
- source: “This translation is provided for convenience only. The Arabic text of Table 5-1 at Appendix A governs.”
- transition: `ADD-03/AppB/para1` escalation why: AppB/para1 makes the Arabic Table 5-1 (Appendix A image) govern over the English translation at Appendix B ('The Arabic text of Table 5-1 at Appendix A governs.'). The two versions differ materially:…
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:T5-1/note(2) vs ADD-03:p4-image/note2 (height datum); ADD-03:T5-1/note(1) vs ADD-03:p4-image/note1 (scope of the limits); ADD-03:T5-1 header 'finished ground level' vs ADD-03:p4-image/table…
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The conflict is real on the quoted words: English note (2) says finished ground level after grading and filling, Arabic note 2 says natural ground level before grading and filling. Note 1 also differs: English says permanent structures including stacks, Arabic says permanent and temporary including…
    - concern: The claims about the Arabic table header, the zone heights (25, 40) and the 30 m lighting threshold are not quoted in the evidence shown, so I could not check them.
    - concern: The target ADD-03:T5-1 is flagged as not among the units the provision cites. Its text before the addendum shows only the table title, and the English notes come from sub-units (T5-1/note(2), note(1)) not printed in the units block. The target unit may be too coarse.
    - concern: S4 cites clause 7.2 ('The Arabic text governs.') but that unit's text is not printed here, so I could not verify it.
    - concern: S6 is an interpretation that a person must confirm. The escalation is reasonable because no amendment op can record precedence between two units both first issued by ADD-03.
  - downstream proposal `ESC-ADD03-APPB-PARA1` escalation (esc:ADD-03:AppB/para1): **escalated**

### ADD-03:T5-1/a (table_row, p5) — UNRESOLVED
- source: “Zone: A | Description: The part of the site within 1,500 m of the eastern site boundary | Maximum height (m above finished ground level): 25 | Obstacle lighting: Required”
- transition: `ADD-03/T5-1/a` disposition no_effect: This row ('Maximum height (m above finished ground level): 25 | Obstacle lighting: Required') is part of the English convenience translation. Clause 7.2: 'The …
  - validation: **conflicting** — declared_conflicts: the proposer declares: English column heading 'm above finished ground level' against the Arabic heading 'متر فوق منسوب الأرض الطبيعية' (natural ground level)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
    - concern: The Arabic reading (p4 image) is pending approval, so the claim that the figures match rests on an unapproved reading.
    - concern: no_effect applies only to the English row as a translation. The row carries 'Required' and a datum that conflicts with the Arabic heading, so a person must confirm it, as the item says. Clause 7.1 is cited from the statements, not printed as a unit.
  - downstream proposal `ESC-ADD03-T5-1-A` escalation (esc:ADD-03:T5-1/a): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
      - concern: The English row text is verbatim and the governing-text clause (AppB/para1) is quoted, so the escalation as insufficient evidence follows. The Arabic heading is not shown. The 'natural ground level' claim is only the proposer's report, so the conflict is unverified and the real gap is the unread go…
      - concern: Controller found S3 not verbatim: S3 is a paraphrase, and its cited cell '25' does not itself show the datum. The datum is in the column heading and note (2).
      - concern: The claim that the lighting requirement depends on the Arabic text is an inference. The Arabic reading is pending.

### ADD-03:T5-1/b (table_row, p5) — UNRESOLVED
- source: “Zone: B | Description: The remainder of the site | Maximum height (m above finished ground level): 40 | Obstacle lighting: Required for any part exceeding 30 m”
- transition: `ADD-03/T5-1/b` disposition no_effect: This row ('Maximum height (m above finished ground level): 40 | Obstacle lighting: Required for any part exceeding 30 m') is part of the English convenience tr…
  - validation: **conflicting** — declared_conflicts: the proposer declares: English column heading 'm above finished ground level' against the Arabic heading 'متر فوق منسوب الأرض الطبيعية' (natural ground level)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
    - concern: The Arabic reading is pending approval.
    - concern: no_effect covers only the translation row. The datum conflict is real and is escalated under note(2). The row's 'Required for any part exceeding 30 m' matches the Arabic reading.
  - downstream proposal `ESC-ADD03-T5-1-B` escalation (esc:ADD-03:T5-1/b): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
      - concern: The English row text is verbatim. The escalation follows from the governing Arabic text being unread. The datum conflict rests only on the proposer's unverified report.
      - concern: S3 is not verbatim-supported per the controller. It cites the '25' cell of row A, not row B or the heading.
      - concern: The 30 m lighting threshold is plausibly tied to the same datum, but the evidence does not state this.

### ADD-03:T5-1/notes (note_intro, p5) — answered
- source: “Notes to Table 5-1:”
- transition: `ADD-03/T5-1/notes` disposition no_effect: 'Notes to Table 5-1:' is only the introductory heading of the notes in the English convenience translation. It prints no change and no obligation. Clause 7.2: …
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The claim that the Arabic prints a matching 'ملاحظات' heading is in the model rationale only. No quotation of it is shown.

### ADD-03:T5-1/note(1) (note, p5) — UNRESOLVED
- source: “(1) These limits apply to all permanent structures, including stacks.”
- transition: `ADD-03/T5-1/note(1)` escalation why: The English note (1), 'These limits apply to all permanent structures, including stacks.', does not match the governing Arabic note 1 (reading pending). The Arabic applies the limits to permanent AND…
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:T5-1/note(1) against ADD-03:p4-image/note1
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The conflict depends on the pending reading of Arabic note 1. If that reading is approved, English note (1) is narrower: it omits temporary structures, cranes and construction equipment.
    - concern: The link to Q21 and cover/para3 is asserted but no evidence for it is shown.
  - downstream proposal `ESC-ADD03-T5-1-NOTE1` escalation (esc:ADD-03:T5-1/note(1)): **conflicting**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-sonnet-5-5
      - concern: The English note (1) text is verbatim, and the Arabic being pending is supported. The wider Arabic scope is only the proposer's claim.
      - concern: The payload ties this to cranes, construction equipment and the lifting plan under ADD-03/Q21 (VOL-I 9.7). No evidence shown contains Q21 or 9.7, so that consequence is unsupported.
      - concern: The 'non-permanent items could include cranes' step is speculation. Without that step the escalation would stand as a plain unread-governing-text issue.

### ADD-03:T5-1/note(2) (note, p5) — UNRESOLVED
- source: “(2) Height is measured from finished ground level after grading and filling.”
- transition: `ADD-03/T5-1/note(2)` escalation why: The English note (2), 'Height is measured from finished ground level after grading and filling.', and the English column heading 'm above finished ground level' give the opposite datum to the governi…
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:T5-1/note(2) against ADD-03:p4-image/note2; ADD-03:T5-1/a and /b column heading against ADD-03:p4-image/table-header
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: Both Arabic readings (note 2 and the heading) are pending approval.
    - concern: The opposite datum is real on the quoted words: finished ground after grading and filling in English, against natural ground before grading and filling in Arabic. The consequence for filled ground follows.
  - downstream proposal `ESC-ADD03-T5-1-NOTE2` escalation (esc:ADD-03:T5-1/note(2)): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
      - concern: The English note (2) text is verbatim. The escalation follows from the Arabic reading being pending.
      - concern: The 'opposite datum' wording states as fact what is only the proposer's unverified report. The Arabic note 2 text is not in the evidence.
      - concern: S3 is not verbatim-supported per the controller. The claim that filled sites give different heights follows logically from the datum wording.

### ADD-03:T5-1/note(3) (note, p5) — UNRESOLVED
- source: “(3) The Office shall be notified at least thirty (30) days before any crane is erected at the site.”
- transition: `ADD-03/T5-1/note(3)` disposition no_effect: 'The Office shall be notified at least thirty (30) days before any crane is erected at the site.' is the English convenience translation of Arabic note 3. Clau…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: whether 'days' are calendar or working days (unqualified in the Arabic)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The Arabic note 3 reading is pending approval.
    - concern: no_effect applies only to the translation. The 30-day notification duty is real and arrives through the Arabic table incorporated by 7.1. The controller flags the 'shall' wording for human confirmation.
    - concern: Neither text says whether the 30 days are calendar or working days. The item states this.
  - downstream proposal `ESC-ADD03-T5-1-NOTE3` escalation (esc:ADD-03:T5-1/note(3)): **escalated**

## Downstream proposals (validated in the candidate)

| Item | Type | Task | Status | First failed check, or what a person confirms |
|---|---|---|---|---|
| DS-ADD03-R01 | row_reading | row:VOL-I-10.3-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R02 | row_reading | row:VOL-I-10.3-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R03 | row_reading | row:VOL-I-6.2-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R04 | row_reading | row:VOL-I-6.2-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R05 | row_reading | row:VOL-I-8.3-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R06 | row_reading | row:VOL-I-9.6-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R07 | row_reading | row:VOL-I-9.7-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R08 | row_reading | row:VOL-II-3.1-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R09 | row_reading | row:VOL-II-6.4-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R10 | row_reading | row:VOL-II-6.4-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R11 | row_reading | row:VOL-IV-F4E-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R12 | row_reading | row:VOL-IV-F4F-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-I01 | issue | row:VOL-IV-F4F-01 | conflicting | declared_conflicts: the proposer declares: ADD-03:Q19; ADD-03:3.1; ADD-03:3.3 |
| DS-ADD03-CQ01 | clarification_item | row:VOL-IV-F4F-01 | insufficient_evidence | held back: linked issues not promotable: ['I-ADD03-AP-PRICE-BASIS'] |
| DS-ADD03-01 | row_reading | row:VOL-IV-F4F-02 | conflicting | declared_conflicts: the proposer declares: I-ADD03-PRICE-BASIS |
| DS-ADD03-02 | issue | row:VOL-IV-F4F-02 | interpretation_pending |  |
| DS-ADD03-03 | clarification_item | row:VOL-IV-F4F-02 | interpretation_pending |  |
| DS-ADD03-04 | escalation | row:VOL-V-29.2-01 | escalated | missing_information: the proposer declares missing: An amendment op for ADD-03:3.3 replacing VOL-V:29.2 |
| DS-ADD03-05 | issue | row:VOL-V-29.2-01 | evidence_verified |  |
| DS-ADD03-06 | row_new | c46:ADD-03/3.2 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-07 | row_new | c46:ADD-03/7.1 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-08 | issue | c46:ADD-03/7.1 | interpretation_pending |  |
| DS-ADD03-09 | activity | act:fin-model-build | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| DS-ADD03-10 | no_change | act:fin-model-freeze | interpretation_pending |  |
| DS-ADD03-11 | no_change | act:model-auditor-appoint | interpretation_pending |  |
| DS-ADD03-12 | no_change | act:model-audit-review | interpretation_pending |  |
| DS-ADD03-13 | no_change | act:model-audit-opinion | interpretation_pending |  |
| DS-ADD03-14 | no_change | act:deliver | interpretation_pending |  |
| DS-ADD03-15 | no_change | act:seal-and-mark | interpretation_pending |  |
| DS-ADD03-16 | no_change | act:copies | interpretation_pending |  |
| DS-ADD03-ACT-ENV-A | activity | act:assemble-envelope-a | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| DS-ADD03-NC-ENV-B | no_change | act:assemble-envelope-b | interpretation_pending |  |
| DS-ADD03-ACT-ISO | activity | act:iso-copy | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| DS-ADD03-ACT-DEVREV | activity | act:deviations-review | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| DS-ADD03-ACT-F4E | activity | act:form-4e | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| DS-ADD03-ACT-TECH | activity | act:technical-proposal | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| DS-ADD03-ACT-F4F | activity | act:form-4f | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| DS-ADD03-ESC-COVER | escalation | esc:ADD-03:cover/para3 | conflicting | declared_conflicts: the proposer declares: ADD-03:2.1; ADD-03:5.1 |
| DS-ADD03-ESC-21 | escalation | esc:ADD-03:2.1 | escalated | missing_information: the proposer declares missing: A valid op set carrying the deletion of VOL-I 6.7 and the replacement Clause 6.6 |
| DS-ADD03-ESC-33 | escalation | esc:ADD-03:3.3 | escalated | missing_information: the proposer declares missing: Limb (b) carried in the same replacement op; Schedule 9 (not checked in this evidence build) |
| DS-ADD03-ESC-33B | escalation | esc:ADD-03:3.3(b) | escalated | missing_information: the proposer declares missing: An op carrying ADD-03:3.3(b) as part of the replacement VOL-V 29.2 |
| DS-ADD03-ESC-51 | escalation | esc:ADD-03:5.1 | conflicting | declared_conflicts: the proposer declares: ADD-03:cover/para3 |
| ESC-ADD03-5.2 | escalation | esc:ADD-03:5.2 | escalated | missing_information: the proposer declares missing: ESIA Figure 7-2 (receptor and concentration) |
| ESC-ADD03-Q18 | escalation | esc:ADD-03:Q18 | escalated | missing_information: the proposer declares missing: ESIA Figure 7-2 (receptor location and concentration) |
| ESC-ADD03-7.2 | escalation | esc:ADD-03:7.2 | escalated | missing_information: the proposer declares missing: approved reading of region ADD-03-p4-r1 |
| ESC-ADD03-7.3 | escalation | esc:ADD-03:7.3 | escalated | missing_information: the proposer declares missing: approved reading of region ADD-03-p4-r1 (zone definitions); a person's decision on a new A1 row and evidence item for the 7.3 notification |
| ESC-ADD03-7.4 | escalation | esc:ADD-03:7.4 | escalated | missing_information: the proposer declares missing: approved reading of region ADD-03-p4-r1 |
| ESC-ADD03-P4-HEADER | escalation | esc:ADD-03:p4-image/table-header | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1 |
| ESC-ADD03-P4-ROWA | escalation | esc:ADD-03:p4-image/row-a | escalated | missing_information: the proposer declares missing: approved reading of region ADD-03-p4-r1 (row A column split) |
| ESC-ADD03-P4-ROWB | escalation | esc:ADD-03:p4-image/row-b | escalated | missing_information: the proposer declares missing: approved reading of region ADD-03-p4-r1 (row B column split) |
| ESC-ADD03-P4-NOTE1 | escalation | esc:ADD-03:p4-image/note1 | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(1) |
| ESC-ADD03-P4-NOTE2 | escalation | esc:ADD-03:p4-image/note2 | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(2) |
| ESC-ADD03-P4-NOTE3 | escalation | esc:ADD-03:p4-image/note3 | escalated | missing_information: the proposer declares missing: approved reading of region ADD-03-p4-r1 |
| ESC-ADD03-P4-STAMP | escalation | esc:ADD-03:p4-image/stamp | escalated | missing_information: the proposer declares missing: the content or significance of the page-4 stamp |
| ESC-ADD03-APPB-PARA1 | escalation | esc:ADD-03:AppB/para1 | escalated | missing_information: the proposer declares missing: approved reading of the Appendix A image (region ADD-03-p4-r1) |
| ESC-ADD03-T5-1-A | escalation | esc:ADD-03:T5-1/a | conflicting | statements: fact downstream-005/S3 is not supported verbatim |
| ESC-ADD03-T5-1-B | escalation | esc:ADD-03:T5-1/b | conflicting | statements: fact downstream-005/S3 is not supported verbatim |
| ESC-ADD03-T5-1-NOTE1 | escalation | esc:ADD-03:T5-1/note(1) | conflicting | declared_conflicts: the proposer declares: English note (1) is limited to permanent structures; the proposer reports that the Arabic note 1 is wider (reading pending) |
| ESC-ADD03-T5-1-NOTE2 | escalation | esc:ADD-03:T5-1/note(2) | conflicting | statements: fact downstream-005/S3 is not supported verbatim |
| ESC-ADD03-T5-1-NOTE3 | escalation | esc:ADD-03:T5-1/note(3) | escalated | missing_information: the proposer declares missing: whether the 30 days are calendar days or Working Days; approved reading of Arabic note 3 (region ADD-03-p4-r1) |

## Promoted into the candidate (PROPOSED; nothing accepted)

- ops: ADD-03/3.1, ADD-03/3.2, ADD-03/3.4, ADD-03/4.1, ADD-03/4.2, ADD-03/Q15, ADD-03/Q16, ADD-03/Q17, ADD-03/Q19, ADD-03/Q20, ADD-03/Q21, ADD-03/7.1
- dispositions: ADD-03:cover/para1: no_effect, ADD-03:cover/para2: no_effect, ADD-03:1.1: no_effect, ADD-03:1.2: no_effect, ADD-03:1.3: no_effect, ADD-03:2.2: no_effect, ADD-03:AppA/para1: no_effect, ADD-03:p4-image/hdr-en: no_effect, ADD-03:p4-image/hdr-ar: no_effect, ADD-03:p4-image/date: no_effect, ADD-03:p4-image/ref: no_effect, ADD-03:p4-image/subject: no_effect, ADD-03:p4-image/tender-ref: no_effect, ADD-03:p4-image/table-title: no_effect, ADD-03:p4-image/table-intro: no_effect, ADD-03:p4-image/notes-head: no_effect, ADD-03:p4-image/signatory: no_effect, ADD-03:AppA/para2: no_effect, ADD-03:T5-1/notes: no_effect
- rows new: ADD-03-3.2-01, ADD-03-7.1-01
- readings: VOL-I-10.3-01, VOL-I-10.3-02, VOL-I-6.2-01, VOL-I-6.2-02, VOL-I-8.3-01, VOL-I-9.6-01, VOL-I-9.7-01, VOL-II-3.1-01, VOL-II-6.4-01, VOL-II-6.4-02, VOL-IV-F4E-01, VOL-IV-F4F-01
- issues: I-ADD03-29.2-NO-OP, I-ADD03-PRICE-BASIS, I-ADD03-T51-DATUM
- activities: fin-model-build, assemble-envelope-a, iso-copy, deviations-review, form-4e, technical-proposal, form-4f
- clarifications: CQ-ADD03-01
- no change: act:fin-model-freeze, act:model-auditor-appoint, act:model-audit-review, act:model-audit-opinion, act:deliver, act:seal-and-mark, act:copies, act:assemble-envelope-b
- unresolved provisions: 23

## check-register on the candidate

- exit 1; 1 finding(s) {'quote': 1}
  - [quote] ADD-03-7.1-01: post_award_evidence basis not found as quoted: VOL-II:5.5+ADD-03 p2 'The Project Company shall comply with the height limits in Table 5-1'

## Coverage

- provisions: 54; accounted for by the combined set: 54; states {'validated': 54}
- resolution (controller): resolved 13, pending 41, invalid 0, unaccounted 0; approved 0
- structural units of ADD-03 that are not provisions (listed so nothing is dropped): ADD-03:H:cover (heading), ADD-03:H:cover-2 (heading), ADD-03:H:S1 (heading), ADD-03:H:S2 (heading), ADD-03:H:S3 (heading), ADD-03:H:S4 (heading), ADD-03:H:S5 (heading), ADD-03:H:S6 (heading), ADD-03:S6/QA (table), ADD-03:H:S7 (heading), ADD-03:H:AppA (heading), ADD-03:region:ADD-03-p4-r1 (region), ADD-03:p4-image (image_text), ADD-03:H:AppB (heading), ADD-03:T5-1 (table)
- batches: reading-ADD-03-p4-r1 done, analysis-001 done, analysis-002 done, analysis-003 done, analysis-004 done, analysis-005 done, analysis-006 done, analysis-007 done, analysis-008 done, analysis-009 done, downstream-001 done, downstream-002 done, downstream-003 done, downstream-004 done, downstream-005 done

## Critic (a second model over the selected items; it changed no status)

**Agreement between the critic and the proposer is not approval**: every item still needs a person's decision, and a disagreement is a concern for that person, not a rejection. The critic reviews only the selected classes (consequential interpretations, uncertain targets, removals, conflicting evidence), in one request per batch.

| Batch | Critic | Selected | Reviewed | Agrees | Does not agree | Note |
|---|---|---|---|---|---|---|
| analysis-001 | done | 7 | 7 | 7 | 0 |  |
| analysis-002 | done | 6 | 6 | 6 | 0 |  |
| analysis-003 | done | 2 | 2 | 1 | 1 |  |
| analysis-004 | done | 7 | 7 | 5 | 2 |  |
| analysis-005 | done | 3 | 3 | 3 | 0 |  |
| analysis-006 | done | 2 | 2 | 2 | 0 |  |
| analysis-007 | done | 8 | 8 | 7 | 1 |  |
| analysis-008 | done | 2 | 2 | 2 | 0 |  |
| analysis-009 | done | 6 | 6 | 6 | 0 |  |
| downstream-001 | done | 3 | 3 | 3 | 0 |  |
| downstream-002 | done | 3 | 3 | 3 | 0 |  |
| downstream-003 | done | 2 | 2 | 1 | 1 |  |
| downstream-004 | done | 3 | 3 | 3 | 0 |  |
| downstream-005 | done | 4 | 4 | 3 | 1 |  |

- **ADD-03/cover/para3** (analysis-001; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Annotation (adds_obligation) of Form 4-A acknowledgement is consistent with the cover text. The target is the provision itself, which is acceptable for a self-annotation, but the cover also lists changes to Vol V 29.2, Vol II 3.1/3.5/5.6 that are not applied here (stated as carried elsewhere).
    - concern: Real conflicts: cover says 'without change of substance' but ADD-03:2.1 shortens the modification window (old 6.7: any time before due date; new: 2 Working Days before). Also the cover cites an 'odour criterion' in Vol II 3.5 while the evidence shows VOL-II:3.5 as a noise criterion (S-I2). Both are…
    - concern: The statement that the Form 4-A acknowledgement is at paragraph 1 as reissued by ADD-01 rests on ADD-01 text only; ADD-01 span says it is added at paragraph 1, which is fine. Whether ADD-02 changed Form 4-A is not shown.
- **ADD-03/1.1** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Reading as a recital with no_effect follows from the words. It does restate precedence, but VOL-I:3.2 and 5.3 texts are not printed in the evidence, so the claim that it merely restates existing precedence cannot be verified here.
- **ADD-03/1.2** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: It is a rule of reading for the Addendum's own references, so no_effect on unit text is reasonable. However, 'unless otherwise stated' could change which version a reference points to; the controller flagged it for a person. No instance of an 'otherwise stated' reference is shown in this evidence.
- **ADD-03/1.3** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Recital reporting that late clarification requests were not answered; consistent with the VOL-I:5.2 quotation. No unit text changed.
- **ADD-03/2.1(a)** (analysis-001; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
    - concern: Replacement text matches ADD-03:2.1 verbatim and the previous value matches VOL-I:6.6. The op replaces 6.6 text only; the deletion of 6.7 is handled separately (2.1(b)), so the two must be applied together or 6.7 will conflict.
    - concern: Real conflict with the cover's 'without change of substance': modification now cut off 2 Working Days before due date (S-I1). The operative text governs only if a person confirms this.
    - concern: The 24 Nov 2026 cut-off depends on assumption S-A1 (due date 26 Nov 2026 from VOL-I:6.1, and 'Working Days' definition/calendar not shown); it needs confirmation, including whether the due date is moved elsewhere. Note that new text also adds that late modifications are rejected unopened, a substan…
- **ADD-03/2.1(b)** (analysis-001; controller status **escalated**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Escalation is appropriate: 2.1 prints that Clauses 6.6 and 6.7 are deleted, and VOL-I:6.7 is a separate unit that must be deleted. The stated reason (engine C22 citation parsing missing 6.7) is a tool limitation reported by the proposer; it is not shown in the evidence printed here, so it cannot be…
- **ADD-03/2.2** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Words say 6.7 is not reused and no renumbering; no_effect on text is consistent. The controller flagged 'renumbered' as amendment language; a person should confirm. It depends on 6.7 actually being recorded as deleted (2.1(b)).
- **ADD-03/3.2** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: The printed number 1.1A is not held in the stored text (S-A1). A person should confirm this convention.
    - concern: The Base Date depends on the Proposal Due Date in force. The item correctly does not compute it.
- **ADD-03/3.3** (analysis-002; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
    - concern: The op leaves VOL-V:29.2 ending in '; and' until limb (b) is appended. The effective text is incomplete in the meantime, as S-I1 says.
    - concern: The old text is located in the target, not quoted by the provision. The old words match VOL-V:29.2 exactly, but a person must confirm that 'deleted and replaced' means the whole clause.
    - concern: The change is substantive. It moves from a fixed 60/40 split to a Bidder-chosen 50-70% in the first ten years, plus a Base Date indexation start. The text is stored without the '29.2' label, in the same way as S-A1.
    - concern: The claim that the engine rejects limb (b) under C21/C22 is not visible in the evidence shown. Only the dry-run result is asserted.
- **ADD-03/3.3(b)** (analysis-002; controller status **escalated**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: ADD-03:3.3(b) does contain limb (b), with 75% from year 11 and the balance fixed, and the closing quote. The text supports the escalation.
    - concern: The engine rejections (C22, C21) are asserted by the proposer. They are not shown in the evidence.
    - concern: A person must append limb (b) to 29.2, or 29.2 stays incomplete.
    - concern: The (a)/(b) split leaves a gap. Limb (a) ends at the tenth year of operations, and limb (b) starts at the eleventh. Nothing in the evidence shows a gap in coverage, but a person should confirm the operations-year counting.
- **ADD-03/3.3-clar** (analysis-002; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: Only one Form 4-F field, 'Indexation basis assumed: Per Volume V Clause 29.2', is shown in the evidence. The claim that none of the 20 members is a field for the Indexed Proportion cannot be checked from what is printed.
    - concern: The gap is real on the evidence shown. Clause 29.2(a) refers to a percentage stated in Form 4-F, and the only indexation field points back to Clause 29.2.
    - concern: ADD-03 provisions outside this batch might reissue Form 4-F. The proposer admits this was not checked.
    - concern: The interim handling is a suggestion for a person to decide.
- **ADD-03/3.4** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The words 'shall reflect this Section 3' do impose an obligation without changing the text of VOL-I:10.3.
    - concern: The note mentions 'Base Date pricing'. That comes from ADD-03/3.1, which is not in the evidence shown.
    - concern: Whether the obligation is 'adds_obligation' or 'no_effect' is an interpretation. A person must confirm it.
- **ADD-03/4.2** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The note's detail about a membrane filtration step with pore size not exceeding 0.1 µm comes from ADD-03 Section 4.1. That is not in the evidence shown, so it cannot be verified here.
    - concern: The target VOL-II:S3 is a group. The evidence is only its heading. The obligation attaches to the design submission, not to any text.
    - concern: Whether the obligation is 'adds_obligation' or 'no_effect' is an interpretation. A person must confirm it.
- **ADD-03/5.1** (analysis-003; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: Real conflict: ADD-03 cover/para3 names Clause 3.5 (the noise clause), but operative 5.1 names Clause 3.4 and quotes words found only in 3.4. The operative text and the quoted words support targeting 3.4, but a person should confirm which clause the cover summary intends.
    - concern: The new limit's numeric value (ESIA Figure 7-2) is not in the evidence, so the replacement cannot be expressed as a number. This is a declared gap.
    - concern: The replacement changes the location from site boundary to nearest sensitive receptor. The trailing words ', assessed as a 98th percentile hourly value' remain, which matches the statement that the basis is unchanged.
    - concern: The old string appears exactly once in 3.4 and matches verbatim, including the m³ superscript.
- **ADD-03/5.2** (analysis-003; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The obligation to demonstrate compliance in the Technical Proposal is clearly stated in ADD-03:5.2, so the adds_obligation annotation is plausible. But the interpretation I1 that it is a new obligation, not confirming an existing one, has no evidence attached. The evidence shown does not include an…
    - concern: Compliance demonstration depends on the ESIA Figure 7-2 value, which is not in the evidence, and on 5.1 and its unresolved cover-page conflict (Clause 3.4 vs 3.5). It therefore stays pending a person's confirmation.
    - concern: Controller status is insufficient_evidence, which is consistent with this.
- **ADD-03/Q15** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- **ADD-03/Q16** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: Payload note says a 'no deviations' statement precludes any qualification elsewhere; this comes from the response's first sentence, which is supported. Clause 9.6 itself only makes such a Proposal non-responsive, so the response adds the 'shall not' wording. Target is 9.6 with Form 4-E as a second …
- **ADD-03/Q17** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Clause 8.3 text is unchanged. The response adds a per-member requirement, so 'adds_obligation' fits. Cited evidence for the clause is only the first sentence.
- **ADD-03/Q18** (analysis-004; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The response points to ESIA Figure 7-2, which is not in the evidence, so the receptor and concentration cannot be checked. The proposer declares this missing.
    - concern: The response refers to Clause 3.4 'as amended by Section 5', and the amendment is not in the evidence. VOL-II:3.4 as printed says 'site boundary', so the response may conflict with it or change it. This cannot be judged from this evidence.
    - concern: The controller status is insufficient_evidence, so this should not be treated as a clean interpretation.
- **ADD-03/Q19** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The proposer flags possible tension with ADD-03:3.1 and 3.3 (Base Date prices and indexation), which are not in the evidence. The response says year 1 prices and indexation from the first anniversary of PCOD. A person should check this.
    - concern: The VOL-V:29.2 text shown is only a fragment. It mentions Schedule 9 and does not show when indexation starts, so the start point cannot be compared with the response.
- **ADD-03/Q20** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: Real conflict. Response 20 requires the Indexed Proportion to be stated in Form 4-F. It also says the Proportion must not appear anywhere in Envelope A. VOL-I:6.2 makes any commercial information in Envelope A non-responsive. The evidence does not show whether Form 4-F is in Envelope A or in anothe…
    - concern: The proposer states that I-Q20 'confirms the Indexed Proportion is commercial information'. The response does not say so. It only says it must not be in Envelope A and that 6.2 applies.
    - concern: 'Indexed Proportion' is defined in ADD-03:3.3, which is not in the evidence.
- **ADD-03/Q21** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Clause 5.6 and Table 5-1 are not in the evidence, so the content of the crane and lifting plan requirement cannot be checked. This is acknowledged in the item and is a dependency on ADD-03:7.1.
- **ADD-03/7.1** (analysis-005; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: VOL-II:5.5 is only the insertion anchor and stays unchanged, which matches the provision text. The new clause incorporates Table 5-1 by reference, so what it requires depends on the Arabic Appendix A reading, which is still pending. The rationale's description of the crop (zone values, letter refer…
- **ADD-03/7.2** (analysis-005; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The Arabic notes are a pending image reading, and the item says so. My own reading of the Arabic matches the proposer's: note 1 covers permanent and temporary structures including stacks, cranes and construction equipment. Note 2 measures from natural ground before grading and filling.
    - concern: The English notes in the evidence are the permanent-structures note and the finished-ground-level note, so the two conflicts are real.
    - concern: I2's claim that the Arabic is the more restrictive reading holds only where the site is filled. If the site is cut, the effect reverses. The statement should be conditional.
    - concern: Whether 7.2 has any effect depends on the target. T5-1 is not yet in force at ADD-02, so no existing op type can record the precedence. Escalation is a reasonable choice, but it rests on the C22 failure, which is not printed in the evidence.
- **ADD-03/7.2/issue** (analysis-005; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The headline 'wider and stricter' overstates the datum point. The Arabic is stricter only if the finished level is above natural ground (fill). The item lists fill depths as missing, which supports this caveat.
    - concern: The references to Q21 and the 7.3 notification of items over 30 m are not backed by evidence shown here.
    - concern: Everything depends on the pending Appendix A Arabic reading, which is a reading and not yet an approved text.
- **ADD-03/p4-image/table-title** (analysis-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Evidence for ADD-03:7.1 supports that the table is incorporated by reference there, so a caption having no independent effect is consistent. The 'inserts Volume II Clause 5.6' part of F2 is not shown in the quoted words of 7.1, but this does not affect the no_effect conclusion. The reading text is …
- **ADD-03/p4-image/table-intro** (analysis-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The lead-in says the maximum permitted height in each zone is determined 'as follows', which is introductory. The limits and their binding force sit in the rows and in 7.1, so no_effect is consistent. It depends on the table rows (not shown) carrying the actual limits. F2's reference to inserting C…
- **ADD-03/p4-image/table-header** (analysis-007; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The Arabic heading says natural ground level. The Appendix B quote (finished ground level) appears only in the statement S3 and the T5-1/a unit is not printed here.
    - concern: The reading's column separators are incomplete (الوصف and الحدّ الأقصى are run together), so a person must correct the structure.
- **ADD-03/p4-image/row-a** (analysis-007; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Row A's words add no amendment to any ADD-02 unit, so no_effect on ADD-02 units is consistent. The row is still a substantive height limit that takes effect through 7.1, so the register must link it there.
    - concern: The claim that Arabic and Appendix B agree (1,500 m, lighting) is interpretation S6. Only the '25' is quoted from Appendix B, so the rest is unverified.
    - concern: The reading is unapproved and ٢٥ and مطلوبة are run together.
- **ADD-03/p4-image/row-b** (analysis-007; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The same limits apply as for row A. The reading is unapproved and باقي مساحة الموقع and ٤٠ are run together.
    - concern: The claim that Arabic and Appendix B agree (40 m, lighting above 30 m) has no Appendix B quotation printed.
    - concern: This row carries the operative 40 m limit and the lighting requirement. A no_effect label must not hide that it takes effect via 7.1.
- **ADD-03/p4-image/notes-head** (analysis-007; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- **ADD-03/p4-image/note1** (analysis-007; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The Arabic reading is verbatim and the unresolved status is justified. The Appendix B text is quoted only in S5.
    - concern: The reading is unapproved.
- **ADD-03/p4-image/note2** (analysis-007; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The Arabic reading is verbatim and the datum opposition with Appendix B is quoted in S4.
    - concern: The Arabic table-header datum and Note 2 are consistent with each other, so the conflict is with Appendix B only. The reading is unapproved.
- **ADD-03/p4-image/note3** (analysis-007; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The words contain an obligation ('يجب' = must; 30 days' notice before any crane). Labelling it no_effect risks losing it.
    - concern: The reason says it binds through 7.1's 'shall comply with the height limits in Table 5-1'. A crane-notice duty is not clearly a 'height limit', so this does not clearly follow from 7.1's words. It depends on the incorporation by reference of the whole table including notes.
    - concern: The claim that Appendix B Note (3) agrees is not supported by any quotation shown.
    - concern: The reading is unapproved.
- **ADD-03/p4-image/signatory** (analysis-007; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- **ADD-03/p4-image/stamp** (analysis-008; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Evidence is only a crop hash and empty text; I could not view the image, so the 'empty oval' description rests on the proposer's account. The no_effect conclusion follows from there being no words, but the controller marked insufficient_evidence and whether an unfilled stamp affects the letter's au…
- **ADD-03/AppB/para1** (analysis-008; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The conflict is real on the quoted words: English note (2) says finished ground level after grading and filling, Arabic note 2 says natural ground level before grading and filling. Note 1 also differs: English says permanent structures including stacks, Arabic says permanent and temporary including…
    - concern: The claims about the Arabic table header, the zone heights (25, 40) and the 30 m lighting threshold are not quoted in the evidence shown, so I could not check them.
    - concern: The target ADD-03:T5-1 is flagged as not among the units the provision cites. Its text before the addendum shows only the table title, and the English notes come from sub-units (T5-1/note(2), note(1)) not printed in the units block. The target unit may be too coarse.
    - concern: S4 cites clause 7.2 ('The Arabic text governs.') but that unit's text is not printed here, so I could not verify it.
    - concern: S6 is an interpretation that a person must confirm. The escalation is reasonable because no amendment op can record precedence between two units both first issued by ADD-03.
- **ADD-03/T5-1/a** (analysis-009; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
    - concern: The Arabic reading (p4 image) is pending approval, so the claim that the figures match rests on an unapproved reading.
    - concern: no_effect applies only to the English row as a translation. The row carries 'Required' and a datum that conflicts with the Arabic heading, so a person must confirm it, as the item says. Clause 7.1 is cited from the statements, not printed as a unit.
- **ADD-03/T5-1/b** (analysis-009; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
    - concern: The Arabic reading is pending approval.
    - concern: no_effect covers only the translation row. The datum conflict is real and is escalated under note(2). The row's 'Required for any part exceeding 30 m' matches the Arabic reading.
- **ADD-03/T5-1/notes** (analysis-009; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The claim that the Arabic prints a matching 'ملاحظات' heading is in the model rationale only. No quotation of it is shown.
- **ADD-03/T5-1/note(1)** (analysis-009; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The conflict depends on the pending reading of Arabic note 1. If that reading is approved, English note (1) is narrower: it omits temporary structures, cranes and construction equipment.
    - concern: The link to Q21 and cover/para3 is asserted but no evidence for it is shown.
- **ADD-03/T5-1/note(2)** (analysis-009; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: Both Arabic readings (note 2 and the heading) are pending approval.
    - concern: The opposite datum is real on the quoted words: finished ground after grading and filling in English, against natural ground before grading and filling in Arabic. The consequence for filled ground follows.
- **ADD-03/T5-1/note(3)** (analysis-009; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The Arabic note 3 reading is pending approval.
    - concern: no_effect applies only to the translation. The 30-day notification duty is real and arrives through the Arabic table incorporated by 7.1. The controller flags the 'shall' wording for human confirmation.
    - concern: Neither text says whether the 30 days are calendar or working days. The item states this.
- **DS-ADD03-R04** (downstream-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is an interpretation. Q20 says only that Clause 6.2 applies, and 'other commercial information' is not defined, so a person must confirm it.
    - concern: Q20 also requires the figure in the Form 4-F row. The evidence shown does not say which envelope Form 4-F belongs to, so the reading depends on Form 4-F being outside Envelope A.
- **DS-ADD03-R06** (downstream-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The evidence shown for VOL-I 9.6 is only the Form 4-E listing sentence. The 'no deviations' non-responsive consequence quote was checked only through the controller's register validation, not through printed text.
    - concern: Whether the concession-term point is a deviation is left open and is not decided by this reading.
- **DS-ADD03-I01** (downstream-001; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
    - concern: The conflict is real on the words. Q19 states year 1 prices with indexation from the first anniversary of PCOD. 3.1 states Base Date prices, and 3.3 indexes annually from the Base Date.
    - concern: The Base Date definition in 3.2 and the content of Schedule 9 are not in the evidence shown. The proposer correctly lists them as missing, so the conflict cannot be resolved from the pack.
- **DS-ADD03-01** (downstream-002; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The conflict is real on the words shown. Q19 says year 1 prices with indexation from the first anniversary of PCOD. ADD-03 3.3 says indexation runs 'from the Base Date', and the 3.1 quote says 'expressed at Base Date prices'.
    - concern: The 3.1 text is not printed in the units. I relied on the controller's verbatim check of that quote.
    - concern: The claim that Q20's field is not a qualification is an interpretation, and a person must confirm it. The target sentence is unchanged and states no consequence.
    - concern: Q20 also says 'Volume I Clause 6.2 applies'. The item does not discuss it, and its text is not in the evidence.
    - concern: The Base Date being 28 days before the PDD is not in the evidence shown.
- **DS-ADD03-02** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The conflict follows from the quoted words: Base Date prices indexed from the Base Date (3.1, 3.3), against year 1 prices indexed from the first anniversary of PCOD (Q19).
    - concern: The Base Date being 28 days before the PDD is not in the evidence shown.
    - concern: The 2026-11-12 clarification cut-off and the 2026-11-15 issue date are not in the evidence shown.
    - concern: The 75% from year 11 rests on a 3.3(b) quote. The printed 3.3 text is truncated after '(a)... and'. That quote is not in this item's own evidence list.
    - concern: The ADD-03 3.4 Financial Model reference is not in the evidence shown.
    - concern: Pending a person's decision on the price basis.
- **DS-ADD03-05** (downstream-002; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The printed VOL-V:29.2 text is still the 60%/40% wording, and the controller validated it as verbatim after the ops. ADD-03 3.3 plainly says the clause is deleted and replaced. This supports the claim that the replacement was not applied.
    - concern: The statement that no promoted op exists for 3.3 comes from the proposer's statement. The op list is not printed here.
    - concern: The statement that Schedule 9 is missing is not in the evidence shown.
    - concern: The 75% from year 11 rests on a 3.3(b) quote that is not printed in the units.
- **DS-ADD03-ESC-COVER** (downstream-003; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-sonnet-5-5
    - concern: The conflict between the cover and ADD-03 5.1 is real. The cover says the odour criterion is in VOL-II 3.5, but VOL-II:3.5 is a noise limit (55/45 dB(A)). The odour limit is in VOL-II 3.4, and that is the clause 5.1 amends.
    - concern: The claim that 2.1 contradicts 'without change of substance' is not shown. ADD-03:2.1 and the original VOL-I 6.6/6.7 text are not printed in the units. Only the 2.1 quote about a two-Working-Day modification deadline is given. Without the earlier 6.6/6.7 wording, we can't tell whether that deadline…
    - concern: The statement that the Form 4-A units in units_after are all superseded is not in the printed evidence. The unclear acknowledgement version therefore can't be checked.
    - concern: The item cites 'VOL-I 3.2 precedence within a document'. The cover itself only says the addendum takes precedence over the RFP Documents. No VOL-I 3.2 text is shown.
    - concern: The 'unsupported downstream changes' list names rows, activities and clarifications that are not in the evidence. This part can't be checked.
- **DS-ADD03-ESC-51** (downstream-003; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The conflict is real. 5.1 amends VOL-II 3.4, whose text before the addendum is the 5 OU/m³ site-boundary limit, while the cover names 3.5. It is probably a cover misreference, but a person should decide that.
    - concern: The new limit is whatever Figure 7-2 of the ESIA shows. Only the VOL-II 9.1 phrase 'available in the data room' is quoted, and the ESIA itself is not in the evidence, so the numeric criterion can't be stated. The item says this correctly.
    - concern: Statements such as 'the 5.1 op is not promotable' and the listed downstream rows go beyond the printed evidence. They are process or controller matters and can't be verified here.
- **ESC-ADD03-P4-HEADER** (downstream-004; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The conflict with ADD-03:T5-1 is declared by the proposer. The English T5-1 text is not printed, so I cannot confirm the conflict independently.
    - concern: The merged-cell claim is plausible. The header reads 'الوصف الحدّ الأقصى للارتفاع ...' with no separator between 'الوصف' and the height column, so the column split is unclear.
    - concern: The approved reading of region ADD-03-p4-r1 is missing, as the proposer says. Escalation to a person is appropriate.
- **ESC-ADD03-P4-NOTE1** (downstream-004; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The English note (1) in ADD-03:T5-1 is not printed in the evidence, so the claimed conflict rests on the proposer's declaration.
    - concern: The Arabic text is quoted accurately: it covers permanent and temporary structures, including stacks, cranes and construction equipment.
    - concern: The link to the crane plan under Q21 is not supported by any evidence shown here.
    - concern: The reading has no approval, so escalation is reasonable.
- **ESC-ADD03-P4-NOTE2** (downstream-004; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The English note (2) is not printed, so the conflict is unverified beyond the proposer's declaration.
    - concern: The Arabic text is quoted accurately: height is measured from natural ground level before grading and fill.
    - concern: The reading has no approval, so the height datum stays unsettled and escalation is reasonable.
- **ESC-ADD03-T5-1-A** (downstream-005; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The English row text is verbatim and the governing-text clause (AppB/para1) is quoted, so the escalation as insufficient evidence follows. The Arabic heading is not shown. The 'natural ground level' claim is only the proposer's report, so the conflict is unverified and the real gap is the unread go…
    - concern: Controller found S3 not verbatim: S3 is a paraphrase, and its cited cell '25' does not itself show the datum. The datum is in the column heading and note (2).
    - concern: The claim that the lighting requirement depends on the Arabic text is an inference. The Arabic reading is pending.
- **ESC-ADD03-T5-1-B** (downstream-005; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The English row text is verbatim. The escalation follows from the governing Arabic text being unread. The datum conflict rests only on the proposer's unverified report.
    - concern: S3 is not verbatim-supported per the controller. It cites the '25' cell of row A, not row B or the heading.
    - concern: The 30 m lighting threshold is plausibly tied to the same datum, but the evidence does not state this.
- **ESC-ADD03-T5-1-NOTE1** (downstream-005; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-sonnet-5-5
    - concern: The English note (1) text is verbatim, and the Arabic being pending is supported. The wider Arabic scope is only the proposer's claim.
    - concern: The payload ties this to cranes, construction equipment and the lifting plan under ADD-03/Q21 (VOL-I 9.7). No evidence shown contains Q21 or 9.7, so that consequence is unsupported.
    - concern: The 'non-permanent items could include cranes' step is speculation. Without that step the escalation would stand as a plain unread-governing-text issue.
- **ESC-ADD03-T5-1-NOTE2** (downstream-005; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The English note (2) text is verbatim. The escalation follows from the Arabic reading being pending.
    - concern: The 'opposite datum' wording states as fact what is only the proposer's unverified report. The Arabic note 2 text is not in the evidence.
    - concern: S3 is not verbatim-supported per the controller. The claim that filled sites give different heights follows logically from the datum wording.

## Requests: failures, deferrals, repairs and route notices

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

## Manual interventions (and automatic host sessions, named as such: not a person)

- 2026-10-05T02:58:19Z: host session (automatic) — batch reading-ADD-03-p4-r1 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session reading an image; not a person
- 2026-10-05T03:04:16Z: host session (automatic) — batch analysis-001 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T03:10:27Z: host session (automatic) — batch analysis-002 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T03:12:38Z: host session (automatic) — batch analysis-003 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T03:17:27Z: host session (automatic) — batch analysis-004 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T03:23:10Z: host session (automatic) — batch analysis-005 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T03:28:12Z: host session (automatic) — batch analysis-006 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T03:34:01Z: host session (automatic) — batch analysis-007 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T03:36:52Z: host session (automatic) — batch analysis-008 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T03:42:53Z: host session (automatic) — batch analysis-009 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T03:50:32Z: host session (automatic) — batch downstream-001 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-05T03:56:34Z: host session (automatic) — batch downstream-002 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-05T04:00:29Z: host session (automatic) — batch downstream-003 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-05T04:02:53Z: host session (automatic) — batch downstream-004 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-05T04:04:11Z: host session (automatic) — batch downstream-005 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person

## The diff (ADD-02 → ADD-03; [diff.md](diff.md))

## What changed from ADD-02 to ADD-03

### ADD-03: PARTIAL (issued 2026-11-15)

- ops: 12 (0 invalid); provisions: 54 (23 unresolved)
- validated state: ADD-02 — this addendum does NOT replace it until every provision is treated and every op is valid
- UNRESOLVED ADD-03:cover/para3: This Addendum consolidates Volume I Clauses 6.6 and 6.7 without change of substance, amends the definition of Availability Payment and the indexation of the Ava
- UNRESOLVED ADD-03:2.1: Volume I Clauses 6.6 and 6.7 are deleted and replaced by the following single Clause 6.6: ‘6.6  A Bidder may withdraw its Proposal at any time before the Propos
- UNRESOLVED ADD-03:3.3: Volume V Clause 29.2 is deleted and replaced by the following: ‘29.2  The Availability Payment shall be indexed annually from the Base Date in accordance with S
- UNRESOLVED ADD-03:3.3(b): (b) from the start of the eleventh (11th) year of operations, seventy-five per cent (75%). The balance of the payment shall remain fixed.’
- UNRESOLVED ADD-03:5.1: In Volume II Clause 3.4, ‘not more than 5 OU/m³ at the site boundary’ is deleted and ‘not more than the odour concentration shown for the nearest sensitive rece
- UNRESOLVED ADD-03:5.2: Bidders shall demonstrate compliance with Volume II Clause 3.4, as amended, in the Technical Proposal.
- UNRESOLVED ADD-03:Q18: No: 18 | Bidder question: Will the Authority provide dispersion modelling inputs for the design of the odour control system? | Authority response: The nearest s
- UNRESOLVED ADD-03:7.2: Table 5-1 is issued in the Arabic language. The Arabic text governs. The English translation at Appendix B is provided for convenience only.
- UNRESOLVED ADD-03:7.3: A Bidder whose Proposal provides for any structure, plant or equipment at the site exceeding thirty (30) metres in height shall notify the Authority through the
- UNRESOLVED ADD-03:7.4: Bidders shall reflect Table 5-1 in the Technical Proposal.
- UNRESOLVED ADD-03:p4-image/table-header: المنطقة | الوصف الحدّ الأقصى للارتفاع (متر فوق منسوب الأرض الطبيعية) | الإنارة التحذيرية
- UNRESOLVED ADD-03:p4-image/row-a: أ | الجزء من الموقع الواقع ضمن مسافة ١٬٥٠٠ متر من الحدّ الشرقي للموقع | ٢٥ مطلوبة
- UNRESOLVED ADD-03:p4-image/row-b: ب | باقي مساحة الموقع ٤٠ | مطلوبة لأي جزء يزيد ارتفاعه على ٣٠ متراً
- UNRESOLVED ADD-03:p4-image/note1: ١. تسري هذه الحدود على جميع المنشآت الدائمة والمؤقتة، بما في ذلك المداخن والرافعات ومعدّات الإنشاء.
- UNRESOLVED ADD-03:p4-image/note2: ٢. يُقاس الارتفاع من منسوب الأرض الطبيعية قبل أعمال التسوية والردم.
- UNRESOLVED ADD-03:p4-image/note3: ٣. يجب إخطار المكتب قبل ثلاثين (٣٠) يوماً على الأقل من تركيب أي رافعة في الموقع.
- UNRESOLVED ADD-03:p4-image/stamp: 
- UNRESOLVED ADD-03:AppB/para1: This translation is provided for convenience only. The Arabic text of Table 5-1 at Appendix A governs.
- UNRESOLVED ADD-03:T5-1/a: Zone: A | Description: The part of the site within 1,500 m of the eastern site boundary | Maximum height (m above finished ground level): 25 | Obstacle lighting
- UNRESOLVED ADD-03:T5-1/b: Zone: B | Description: The remainder of the site | Maximum height (m above finished ground level): 40 | Obstacle lighting: Required for any part exceeding 30 m
- UNRESOLVED ADD-03:T5-1/note(1): (1)  These limits apply to all permanent structures, including stacks.
- UNRESOLVED ADD-03:T5-1/note(2): (2)  Height is measured from finished ground level after grading and filling.
- UNRESOLVED ADD-03:T5-1/note(3): (3)  The Office shall be notified at least thirty (30) days before any crane is erected at the site.
- cover summary vs provisions (C28, report only): 1 finding(s)
  - no summary: ADD-03's cover has no 'This Addendum ...' sentence; nothing to compare

#### Validated vs candidate (partial should not mean useless)

- validated (unchanged, ADD-02): `<outputs>/a3/a3.pdf` (one page), `<outputs>/a5/`
- candidate (CANDIDATE — NOT VALIDATED, ADD-03 as proposed): `<outputs>/a3/a3_candidate.pdf` / `.md`, `<outputs>/a5/candidate/`

**What may be changing.** ADD-03 is PARTIAL: 23 of 54 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 12 op(s) that are valid there stood (each still a proposal: review proposed 12), A3 would gain 0 row(s) (none), lose 0 (none) and change 1 (VOL-IV-F4F-02 (register)); A5, replanned at ADD-03's issue date (2026-11-15), would move the latest dates of 0 activities (none), add 0 (none) and remove 0 (none), and marks 5 REVIEW through relationships. Not settled: 11 activities blocked by an unresolved row (fin-model-build, technical-proposal, fin-model-freeze, form-4a-prep and 7 more), 2 STALE row(s), 0 obligation(s) reaching no output (C46), 0 relationship chain(s) blocked or incomplete, 8 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT and 6 more. Nothing here is validated, accepted or applied to the real state.

### Requirements

- new: 2; out of force: 0; changed: 3

- NEW ADD-03-3.2-01: NEW (introduced by ADD-03/3.2) (by ADD-03/3.2)
- NEW ADD-03-7.1-01: NEW (introduced by ADD-03/7.1) (by ADD-03/7.1)
- CHANGED VOL-II-3.1-01: wording; secondary unit VOL-II:H:S3 annotated by ADD-03/4.2 (by ADD-03/4.1, ADD-03/4.2)
- CHANGED VOL-IV-F4E-01: secondary units VOL-IV:F4-E/T1/1, VOL-IV:F4-E/T1/2, VOL-IV:F4-E/T1/3, VOL-IV:F4-E/T1/4, VOL-IV:F4-E/T1/5, VOL-IV:F4-E/T1/6, VOL-IV:F4-E/total-number-of-deviations-declared, VOL-IV:F4-E/signature-of-authorised-signatory, VOL-IV:F4-E/date annotated by ADD-03/Q16 (by ADD-03/Q16)
- CHANGED VOL-IV-F4F-01: secondary units VOL-IV:F4-F/bidder, VOL-IV:F4-F/availability-payment-sar-per-annum-year-1-of-operations, VOL-IV:F4-F/availability-payment-in-words, VOL-IV:F4-F/estimated-project-cost-sar, VOL-IV:F4-F/assumed-senior-debt-tenor-years-from-financial-close, VOL-IV:F4-F/assumed-senior-debt-margin-bps, VOL-IV:F4-F/assumed-gearing-debt-equity, VOL-IV:F4-F/project-irr-nominal-post-tax, VOL-IV:F4-F/equity-irr-nominal-post-tax, VOL-IV:F4-F/indexation-basis-assumed, VOL-IV:F4-F/model-auditor, VOL-IV:F4-F/date-of-model-audit-opinion, VOL-IV:F4-F/signature, VOL-IV:F4-F/name-and-capacity, VOL-IV:F4-F/date annotated by ADD-03/Q19, ADD-03/Q20 (by ADD-03/Q19, ADD-03/Q20)

### Stale readings and decisions

- STALE VOL-V-29.2-01: new dependency ADD-03:Q19; VOL-V:29.2 changed since ADD-01 (by ADD-03/Q19)
- STALE VOL-IV-F4F-02: new dependency ADD-03:Q19; new dependency ADD-03:Q20; VOL-IV:F4-F/para1 changed since BASE (by ADD-03/Q19, ADD-03/Q20)

### Obligations not reaching the outputs (C46)

- none

### Reached through relationships (indirect: for review, not direct citations)

Curated links (relationships file) followed from what changed. The requirements above cite a changed unit; these are reached through another provision, in three classes that are never merged. A5 marks the activities that serve them REVIEW with their dates unchanged.

#### Confirmed dependency (4)
- VOL-I-10.2-01 (row; ACTIVE) <- VOL-V:29.2 via REL-PAY-MECHANISM > REL-PAY-QUOTED-PRICE [feeds_calculation; link confirmed]
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

- no change

### Programme impact (status date 2026-10-22 -> 2026-11-15)

- REWORK assemble-envelope-a: requirement changed: VOL-I-6.2-01
- REWORK assemble-envelope-b: requirement changed: VOL-I-6.2-01
- REWORK copies: requirement changed: VOL-I-6.2-01
- REWORK deliver: requirement changed: VOL-I-6.2-01
- REWORK deviations-review: requirement changed: VOL-I-9.6-01, VOL-IV-F4E-01
- REWORK fin-model-build: requirement changed: VOL-I-10.3-01, VOL-IV-F4F-02
- REWORK fin-model-freeze: requirement changed: VOL-I-10.3-01, VOL-IV-F4F-02
- REWORK form-4e: requirement changed: VOL-I-9.6-01, VOL-IV-F4E-01
- REWORK form-4f: requirement changed: VOL-IV-F4F-01, VOL-IV-F4F-02
- REWORK iso-copy: requirement changed: VOL-I-8.3-01
- REWORK model-audit-opinion: requirement changed: VOL-I-10.3-02
- REWORK model-audit-review: requirement changed: VOL-I-10.3-02
- REWORK model-auditor-appoint: requirement changed: VOL-I-10.3-02
- REWORK seal-and-mark: requirement changed: VOL-I-6.2-01
- REWORK technical-proposal: requirement changed: VOL-I-9.7-01, VOL-II-3.1-01, VOL-II-6.4-01, VOL-II-6.4-02
- REVIEW (possible impact) fin-assumptions: VOL-I-10.6-01 reached from VOL-V:29.2 via REL-PAY-FINANCING-ASSUMPTIONS, REL-PAY-MECHANISM; dates unchanged
- REVIEW (confirmed dependency) fin-model-build: VOL-IV-F4F-02 reached from VOL-I-10.3-01 via REL-MODEL-FORM-4F; dates unchanged
- REVIEW (proposed relationship) fin-model-build: VOL-I-10.3-01, VOL-IV-F4F-02 reached from VOL-V:29.2 via REL-MODEL-FORM-4F, REL-PAY-FINANCIAL-MODEL, REL-PAY-MECHANISM; dates unchanged
- REVIEW (confirmed dependency) fin-model-freeze: VOL-IV-F4F-02 reached from VOL-I-10.3-01 via REL-MODEL-FORM-4F; dates unchanged
- REVIEW (proposed relationship) fin-model-freeze: VOL-I-10.3-01, VOL-IV-F4F-02 reached from VOL-V:29.2 via REL-MODEL-FORM-4F, REL-PAY-FINANCIAL-MODEL, REL-PAY-MECHANISM; dates unchanged
- REVIEW (confirmed dependency) form-4f: VOL-I-10.2-01, VOL-IV-F4F-01, VOL-IV-F4F-02 reached from VOL-I-10.3-01, VOL-V:29.2 via REL-MODEL-FORM-4F, REL-PAY-FORM-4F, REL-PAY-MECHANISM, REL-PAY-QUOTED-PRICE; dates unchanged
- REVIEW (proposed relationship) form-4f: VOL-IV-F4F-02 reached from VOL-V:29.2 via REL-MODEL-FORM-4F, REL-PAY-FINANCIAL-MODEL, REL-PAY-MECHANISM; dates unchanged
- REVIEW (possible impact) lender-terms: VOL-I-10.6-01 reached from VOL-V:29.2 via REL-PAY-FINANCING-ASSUMPTIONS, REL-PAY-MECHANISM; dates unchanged
- FEASIBILITY lcc-ratio: INFEASIBLE by 12 WD -> INFEASIBLE by 28 WD
- FEASIBILITY lcc-certificate: INFEASIBLE by 12 WD -> INFEASIBLE by 28 WD
- FEASIBILITY fin-model-build: OK -> INFEASIBLE by 14 WD
- FEASIBILITY model-auditor-appoint: OK -> INFEASIBLE by 13 WD
- FEASIBILITY pcg-wording: OK -> INFEASIBLE by 13 WD
- FEASIBILITY technical-proposal: OK -> INFEASIBLE by 13 WD
- FEASIBILITY ground-dd: OK -> INFEASIBLE by 9 WD
- FEASIBILITY lender-terms: OK -> INFEASIBLE by 9 WD
- FEASIBILITY completion-certs: OK -> INFEASIBLE by 8 WD
- FEASIBILITY model-audit-review: OK -> INFEASIBLE by 13 WD
- FEASIBILITY poa-resolutions: OK -> INFEASIBLE by 8 WD
- FEASIBILITY references: OK -> INFEASIBLE by 7 WD
- FEASIBILITY bond-approval: OK -> INFEASIBLE by 6 WD
- FEASIBILITY deviations-review: OK -> INFEASIBLE by 5 WD
- FEASIBILITY om-evidence: OK -> INFEASIBLE by 3 WD
- FEASIBILITY pcg-execution: OK -> INFEASIBLE by 13 WD
- FEASIBILITY poa: OK -> INFEASIBLE by 8 WD
- FEASIBILITY clarifications: OK -> DEADLINE PASSED
- FEASIBILITY fin-statements: OK -> INFEASIBLE by 1 WD
- FEASIBILITY fin-model-freeze: OK -> INFEASIBLE by 14 WD
- FEASIBILITY investment-licence: OK -> INFEASIBLE by 8 WD
- FEASIBILITY model-audit-opinion: OK -> INFEASIBLE by 14 WD
- FEASIBILITY form-4b-prep: OK -> INFEASIBLE by 7 WD
- FEASIBILITY bond-issue: OK -> INFEASIBLE by 6 WD
- FEASIBILITY fin-standing: OK -> INFEASIBLE by 1 WD
- FEASIBILITY form-4c-sign: OK -> INFEASIBLE by 6 WD
- FEASIBILITY fin-assumptions: OK -> INFEASIBLE by 11 WD
- FEASIBILITY form-4e: OK -> INFEASIBLE by 5 WD
- FEASIBILITY form-4f: OK -> INFEASIBLE by 11 WD
- FEASIBILITY form-4a: OK -> INFEASIBLE by 4 WD
- FEASIBILITY form-4b: OK -> INFEASIBLE by 7 WD
- FEASIBILITY form-4g-sign: OK -> INFEASIBLE by 4 WD
- FEASIBILITY assemble-envelope-a: INFEASIBLE by 12 WD -> INFEASIBLE by 28 WD
- FEASIBILITY assemble-envelope-b: OK -> INFEASIBLE by 14 WD
- FEASIBILITY copies: INFEASIBLE by 12 WD -> INFEASIBLE by 28 WD
- FEASIBILITY seal-and-mark: INFEASIBLE by 12 WD -> INFEASIBLE by 28 WD
- FEASIBILITY deliver: INFEASIBLE by 12 WD -> INFEASIBLE by 28 WD

## Next (a person)

- read the unresolved and escalated provisions first, then each item against its evidence (`../ai/ADD-03-run-host-blind05-20261005T025444Z-combined/proposals.yaml`, `../downstream/proposals.yaml`)
- nothing here is applied to the real curation: to take an item over, add the PDF to the pack (OPERATING_GUIDE §3 steps 1-2) and copy the reviewed files listed in `promotion.json`; then `pin`, `check-register`, `outputs` and decide with `accept` / `reject` as usual
