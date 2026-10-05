# Review packet: ADD-03, AI workflow run ADD-03-run-host-blind06-20261005T173226Z

> **CANDIDATE: proposed by the AI workflow; not reviewed; nothing accepted.** Statuses are the controller's; a person decides every item. The real `curation/`, `config/` and `out/` were only read: everything below lives in this run's folder.

- PDF: `/home/user/tender-pack-reader/rehearsals/blind-06/input/ADD-03_Addendum_No_3.pdf` (sha256 9b96c1f627af3c50…, 5 pages); preceding state: pack `/home/user/tender-pack-reader/config/pack.yaml` (NUPA-ISTP-2026-014), previous evidence build `/home/user/tender-pack-reader/build`
- route **host**; model requested `claude-code headless (opus)`, reported `None`; host sessions report: claude-opus-5-5
- status **partial**: 22 provision(s) unresolved in the candidate (listed first in the review packet); 30 downstream task(s) answered only by items that cannot be promoted: row:VOL-II-7.2-01, row:VOL-II-8.1-01, row:VOL-II-8.2-01, row:VOL-II-8.3-01, row:VOL-V-31.3-03, clar:CQ-VOL-III-DRAWINGS, clar:CQ-PERSISTENT-BREACH, clar:CQ-PCOD-RELIABILITY-RUN …; check-register on the candidate: exit 1, 1 finding(s) {'C46': 1}; C46: [C46] ADD-03/cover/para3: [A3] ADD-03/cover/para3 brings in consequence words ['deduction'] that no row's consequence carries at ADD-03: 'This Addendum incorpo…
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed

## Execution, completeness and approval (three separate things)

- **Execution** (what ran): ingest done, readings done, analysis done, validation done, downstream done, downstream_validation done, critic done, promotion done, pin done, check_register done, outputs done, diff done, review running; batches reading: {'done': 1}; analysis: {'done': 10}; downstream: {'done': 4}
- **Completeness** (what the run completed): **partial**: 22 provision(s) unresolved in the candidate (listed first in the review packet); 30 downstream task(s) answered only by items that cannot be promoted: row:VOL-II-7.2-01, row:VOL-II-8.1-01, row:VOL-II-8.2-01, row:VOL-II-8.3-01, row:VOL-V-31.3-03, clar:CQ-VOL-III-DRAWINGS, clar:CQ-PERSISTENT-BREACH, clar:CQ-PCOD-RELIABILITY-RUN …; check-register on the candidate: exit 1, 1 finding(s) {'C46': 1}; C46: [C46] ADD-03/cover/para3: [A3] ADD-03/cover/para3 brings in consequence words ['deduction'] that no row's consequence carries at ADD-03: 'This Addendum incorpo…
  - downstream tasks: 48; answered 18; unanswered 0; answered only by items that cannot be promoted 30; answered 'no change' 0
- **Human approval**: **none** (nothing approved, accepted, rejected or sent); no decision is recorded in the candidate's decisions file

## What is candidate and what is real

- **Candidate** (proposed by this run, nothing accepted): `../candidate/` — a copy of the curation and configuration with ADD-03 added, its evidence build, its op file, rows, issues, templates and outputs.
- **Last validated state**: `../candidate/out-before/` (the pre-addendum outputs built from the copied curation and the previous evidence build; done)
- **Real** (untouched): `curation/`, `config/`, `out/`; the owner's approvals and readings were copied unchanged and used read-only.

- real inputs changed since the run started: none

## Candidate outputs

Exit 0 (WORKING DRAFT (not releasable)); every file carries the banner (`../candidate/out/CANDIDATE.md`); A1 has a candidate status column {'proposed (existing row; not changed by this run; not reviewed)': 185, 'PROPOSED BY THE AI WORKFLOW': 13, 'UNRESOLVED': 9}.

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

- before → after: {"a1": {"rows_before": 205, "rows_after": 207, "new": 2, "gone": 0}, "a3": {"before": 17, "after": 17, "enters": 0, "leaves": 0}, "a5": {"activities_before": 44, "activities_after": 44, "new": 0, "gone": 0}}

- ADD-03 is **PARTIAL** in the candidate (provisions unresolved): A3 and the A5 programme show the validated state (ADD-02); ADD-03 as proposed is in A1's `Status after ADD-03` column, in A2, in the candidate A3 and A5 below, in `a5/working/ADD-03.json` and in the diff below.

### Validated and candidate A3 / A5 (partial should not mean useless)

- **Validated** (unchanged; ADD-02): [a3/a3.pdf](../candidate/out/a3/a3.pdf) (one page), [a5/README.md](../candidate/out/a5/README.md), [a5/gantt.html](../candidate/out/a5/gantt.html)
- **Candidate** (CANDIDATE — NOT VALIDATED; ADD-03 as proposed): [a3/a3_candidate.pdf](../candidate/out/a3/a3_candidate.pdf) (9 page(s)), [a3/a3_candidate.md](../candidate/out/a3/a3_candidate.md), [a5/candidate/README.md](../candidate/out/a5/candidate/README.md), [a5/candidate/gantt.html](../candidate/out/a5/candidate/gantt.html)

**What may be changing.** ADD-03 is PARTIAL: 22 of 70 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 11 op(s) that are valid there stood (each still a proposal: review proposed 11), A3 would gain 0 row(s) (none), lose 0 (none) and change 0 (none); A5, replanned at ADD-03's issue date (2026-11-10), would move the latest dates of 0 activities (none), add 0 (none) and remove 0 (none), and marks 7 REVIEW through relationships. Not settled: 3 activities blocked by an unresolved row (technical-proposal, deviations-review, form-4e), 5 STALE row(s), 1 obligation(s) reaching no output (C46), 0 relationship chain(s) blocked or incomplete, 8 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT and 5 more; conditional or effective-dated: ADD-03:2.5 (conditional obligation). Nothing here is validated, accepted or applied to the real state.


- blockers: 22 unresolved provision(s), 3 blocked activit(y/ies), 5 STALE row(s), 1 C46 gap(s), 0 relationship chain(s) blocked or incomplete, 8 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT, I-VOL-III, I-VOL-II-MISSING, I-VOL-V-MISSING, I-VOL-IV-SCALE, I-OP-ADD-01/Q4
- conditional scenarios: 1; ADD-03:2.5 (conditional obligation)

**Image-read units** (the review packet of each region shows every crop beside its reading; translations are proposals, not evidence):

- ADD-03-p4-r1 (ADD-03 p4; reading pending): [packet](../candidate/build/review/ADD-03-p4-r1/packet.html); 36 unit(s) touched
  - `ADD-03:p4-image`: “Table 1-3 (image, Arabic with English labels): Tie-in Points and Flow Shutdown Conditions, Network Operator letter No. 312/2026”
  - `ADD-03:p4-image/hdr-en`: “Northern Region Water Services Company”
  - `ADD-03:p4-image/hdr-ar`: “شركة خدمات المياه بالمنطقة الشمالية”; translation (apart): ‘Northern Region Water Services Company’
  - `ADD-03:p4-image/ref`: “الرقم: ٣١٢/٢٠٢٦”; translation (apart): ‘Number: 312/2026’
  - `ADD-03:p4-image/date`: “التاريخ: ٥ نوفمبر ٢٠٢٦م”; translation (apart): ‘Date: 5 November 2026 AD’
  - `ADD-03:p4-image/subject`: “الموضوع: نقاط الربط بشبكة التجميع القائمة لمحطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان”; translation (apart): ‘Subject: Tie-in points to the existing collection network for the Wadi Al-Sirhan Independent Sewage Treatment Plant’
  - `ADD-03:p4-image/tender-ref`: “مناقصة رقم: NUPA/ISTP/2026/014”; translation (apart): ‘Tender number: NUPA/ISTP/2026/014’
  - `ADD-03:p4-image/table-title`: “جدول ١-٣: نقاط الربط وشروط إيقاف التدفق”; translation (apart): ‘Table 1-3: Tie-in points and flow shutdown conditions’
  - `ADD-03:p4-image/intro`: “تُحدِّد نقاط الربط بشبكة التجميع القائمة وشروط إيقاف التدفق فيها على النحو الآتي:”; translation (apart): ‘The tie-in points to the existing collection network and the conditions for shutting down flow in them are specified as follows:’
  - `ADD-03:p4-image/th-point`: “نقطة الربط”; translation (apart): ‘Tie-in point’
  - `ADD-03:p4-image/th-location`: “الموقع”; translation (apart): ‘Location’
  - `ADD-03:p4-image/th-diameter`: “قطر الخط القائم (مم)”; translation (apart): ‘Existing line diameter (mm)’
  - … 24 more in `a3/a3_candidate.md`
- VOL-II-p3-r1 (VOL-II p3; reading approved): [packet](../candidate/build/review/VOL-II-p3-r1/packet.html); not touched by this addendum
- VOL-IV-p6-r1 (VOL-IV p6; reading approved): [packet](../candidate/build/review/VOL-IV-p6-r1/packet.html); not touched by this addendum

## Timings (wall clock per step)

| Step | Seconds | Status |
|---|---|---|
| ingest | 29.7 | done |
| readings | 211.4 | done |
| analysis | 2170.6 | done |
| validation | 6.0 | done |
| downstream | 838.9 | done |
| downstream_validation | 0.7 | done |
| critic | 47.2 | done |
| promotion | 17.2 | done |
| pin | 1.2 | done |
| check_register | 4.0 | done |
| outputs | 12.4 | done |
| diff | 3.1 | done |
| review | 0.0 | running |
| **total** | **3342.4** (55.7 min) | target 30 min from the PDF to candidate outputs and this packet, human review excluded |

## Readings of the addendum's image regions (AI-proposed, PENDING HUMAN REVIEW)

Ingest first refused the candidate because these image regions had no reading (C05): ADD-03-p4-r1. Each reading below was proposed by the route of this run, checked by readings.check_reading and written into the candidate's readings; it is an interpretation of an image, never approved, and every unit made from it carries `reading.status: pending`.

- **ADD-03-p4-r1** — done; controller status **interpretation_pending**; unit `ADD-03:p4-image`; file `../candidate/curation/readings/ADD-03-p4-r1.yaml`
  - the reading beside its crops (the build's review packet): [../candidate/build/review/ADD-03-p4-r1/packet.html](../candidate/build/review/ADD-03-p4-r1/packet.html)
  - form reading, languages ['ar', 'en']; prepared by: AI-assisted: headless host session ADD-03-hostsession-20261005T173258Z-efd9 (claude-code headless (opus); the CLI reported claude-opus-5-5), in AI workflow run ADD-03-run-host-blind06-20261005T173226Z (reading-ADD-03-p4-r1), 2026-10-05T17:36:16Z; proposed for a person's review, not approved
  - uncertainty: The pixel grid detector reports a 4 x 3 grid (h_lines 187-898, v_lines 555-1493.5) that does not match the image: the printed table is a heading row and 2 data rows by 6 columns (y ~490-898), read right to left, with the outer and first ve…
  - uncertainty: Order of the table cells within a band half follows the printed columns right to left.
  - uncertainty: Diacritics (damma/shadda/fatha on تُحدِّد, يُسمح, تُقدَّم, مدّة, إجازتَي; tanween on بإيقافٍ واحدٍ, مرفقاً) were checked on enlarged band crops; matching text removes tashkeel.
  - uncertainty: The letter is stated in the page's text layer to be reproduced from the Network Operator; this reading says only what the image shows.

## First: unresolved provisions and escalations

22 of 70 provisions are not answered by a promoted item (each is `unresolved` in the candidate op file with the reason); 9 escalation(s).

- **ESCALATED ADD-03/2.4** (ADD-03:2.4): Insufficient evidence. ADD-03:2.4 (and Q20) require the method (a) temporary works to pass 'the maximum transfer flow stated for that tie-in point in Table 1-3'. Table 1-3 states no maximum transfer flow in either the governing Arabic version (Appendix A image) or the English translation. Its six c…
  - unsupported: An obligation whose governing quantity is cross-referenced to a table that does not contain it. No op can record a value that is not printed, and an annotate would hide the gap. The Authority must state the maximum transfer flow per tie-in point (clarification proposed).
  - evidence: ADD-03:2.4 p1: “The temporary works for method (a) shall be capable of passing, at each tie-in point, the maximum transfer flow stated for that tie-in point in Table 1-3.”; ADD-03:T1-3 p5: “Tie-in point | Location | Existing sewer diameter (mm) | Permitted shutdown window | Maximum shutdown duration (hours) | Advance notice”; ADD-03:p4-image/th-duration p4: “أقصى مدّة للإيقاف (ساعة)”; ADD-03:Q20 p3: “The temporary works shall be capable of passing the maximum transfer flow stated for each tie-in point in Table 1-3 at Appendix A to this Addendum.”
  - affected scope: units none; rows none; activities none; clarifications none
- **ESCALATED ADD-03/2.5** (ADD-03:2.5): ADD-03:2.5 adds a conditional Envelope A submission: a Shutdown Acceptance Letter from the Network Operator where method (b) is elected, applied for not later than eight (8) Working Days before the Proposal Due Date. calculate gives 2026-11-16 against the PDD in force at ADD-02 (2026-11-26). 2.5 ci…
  - unsupported: A new conditional bid-stage obligation and deadline with no cited target unit. This needs register and programme treatment (A1 row, A5 milestone), plus confirmation of the cover-summary discrepancy, not a guessed op.
  - evidence: ADD-03:2.5 p1: “Where the Bidder elects method (b) for a tie-in point, it shall submit with Envelope A a letter from the Network Operator accepting the Bidder's proposed shutd…”; ADD-03:2.5 p1: “Applications for a Shutdown Acceptance Letter shall be made to the Network Operator not later than eight (8) Working Days before the Proposal Due Date. The Net…”; ADD-03:cover/para3 p1: “requires a Bidder that elects to interrupt flows at a tie-in point to obtain the Authority's acceptance of its shutdown programme, applications for which shall…”; ADD-03:p4-image/note3 p4: “٣. تُقدَّم طلبات الإيقاف عبر البوابة الإلكترونية للشركة، مرفقاً بها برنامج الإيقاف المقترح وخطة الطوارئ.”
  - affected scope: units none; rows none; activities none; clarifications none
- **ESCALATED ADD-03/2.6** (ADD-03:2.6): ADD-03:2.6 is a deeming rule: method (b) without a Shutdown Acceptance Letter in Envelope A is deemed an election of method (a). It changes the consequence of the obligations in 2.3 and 2.5, both of which are new in this Addendum, and cites no existing unit. Its practical effect also depends on 2.4…
  - unsupported: A deeming consequence linking two new addendum obligations, with no printed target unit. It needs register treatment (A1/A3 consequence on the 2.3 and 2.5 rows) by a person.
  - evidence: ADD-03:2.6 p1: “A Bidder that elects method (b) for a tie-in point but does not submit a Shutdown Acceptance Letter for that tie-in point with Envelope A shall be deemed to ha…”
  - affected scope: units none; rows none; activities none; clarifications none
- **ESCALATED ADD-03/3.2(a)** (ADD-03:3.2): The first sentence of ADD-03:3.2 adds a counting rule to the 30-day reliability run, but it does not cite Volume II Clause 7.2 by number. It relies on 'that range' (from 3.1) and 'the thirty (30) days'. An annotate op on VOL-II:7.2 fails C22 ('not cited: [VOL-II:7.2]'). No text is printed for inser…
  - unsupported: Linking a rule that changes an uncited clause by cross-reference (3.2 -> 3.1 -> VOL-II:7.2) is not supported. A person needs to record the effect on VOL-II:7.2 (adds_obligation or interprets) and decide how 'shall not count' interacts with 'continuous'.
  - evidence: ADD-03:3.2 p2: “A day on which the daily average flow is outside that range shall not count towards the thirty (30) days.”; VOL-II:7.2 p4: “a continuous reliability run of thirty (30) days”
  - affected scope: units VOL-II:7.3; rows none; activities none; clarifications CQ-PCOD-RELIABILITY-RUN
- **ESCALATED ADD-03/Q20** (ADD-03:Q20): Insufficient evidence. Q20 (and ADD-03 Clause 2.4) set the design flow for the temporary works at the tie-in points by reference to 'the maximum transfer flow stated for each tie-in point in Table 1-3'. Table 1-3 states no transfer flow, neither in the English translation (Appendix B: tie-in point,…
  - unsupported: An obligation whose value comes from a table entry that does not exist. Any op recording a design flow for the VOL-II 1.3 temporary works would invent the value. A clarification to the Authority is needed.
  - evidence: ADD-03:Q20 p3: “The temporary works shall be capable of passing the maximum transfer flow stated for each tie-in point in Table 1-3 at Appendix A to this Addendum. Section 2.4…”; VOL-II:1.3 p2: “The Project Company shall be responsible for all interfaces with the existing collection network at the two designated tie-in points, including any temporary w…”; ADD-03:T1-3 p5: “Tie-in point | Location | Existing sewer diameter (mm) | Permitted shutdown window | Maximum shutdown duration (hours) | Advance notice”; ADD-03:p4-image p4: “Table 1-3 (image, Arabic with English labels): Tie-in Points and Flow Shutdown Conditions, Network Operator letter No. 312/2026”
  - affected scope: units VOL-II:1.3; rows VOL-II-1.3-01; activities technical-proposal; clarifications CQ-VOL-III-DRAWINGS
- **ESCALATED ADD-03/p4-image/tp2-duration** (ADD-03:p4-image/tp2-duration): The two renderings conflict. The governing Arabic Table 1-3 prints '٤' (4 hours) as the TP-2 maximum shutdown duration, while the convenience English translation (ADD-03:T1-3/tp-2) prints 'Maximum shutdown duration (hours): 6'. ADD-03 2.2 says 'The Arabic text governs.' This is consequential: ADD-0…
  - unsupported: Recording the precedence of one rendering over another when both are issued in the same addendum: no op type can target a unit that does not exist at the previous stage. A person must record that the Arabic value (4 h) governs for TP-2 and flag the English 6 h as an erroneous translation. A clarifi…
  - evidence: ADD-03:p4-image/tp2-duration p4: “٤”; ADD-03:T1-3/tp-2 p5: “Maximum shutdown duration (hours): 6”; ADD-03:2.2 p1: “The Arabic text governs.”; ADD-03:2.7 p1: “A Proposal that provides for an interruption of flow at a tie-in point for longer than the maximum shutdown duration stated for that tie-in point in Table 1-3 …”
  - affected scope: units none; rows none; activities none; clarifications none
- **ESCALATED ADD-03/p4-image/note1** (ADD-03:p4-image/note1): The two renderings conflict. Governing Arabic note 1 prohibits any shutdown during Ramadan and also during the Eid al-Fitr and Eid al-Adha holidays ('أو خلال إجازتَي عيد الفطر وعيد الأضحى'). English note (1) reads only '(1) No shutdown is permitted during the holy month of Ramadan.' ADD-03 2.2 says…
  - unsupported: Recording the precedence of one rendering over another when both are issued in the same addendum: no op type can target a unit that does not exist at the previous stage. A person must record that the Arabic note governs and that the Eid holidays are also excluded periods. Turning those holidays int…
  - evidence: ADD-03:p4-image/note1 p4: “١. لا يُسمح بأي إيقاف خلال شهر رمضان المبارك أو خلال إجازتَي عيد الفطر وعيد الأضحى.”; ADD-03:T1-3/note(1) p5: “(1) No shutdown is permitted during the holy month of Ramadan.”; ADD-03:2.2 p1: “The Arabic text governs.”
  - affected scope: units none; rows none; activities none; clarifications none
- **ESCALATED ADD-03/T1-3/tp-2** (ADD-03:T1-3/tp-2): The convenience translation gives TP-2 'Maximum shutdown duration (hours): 6'. The governing Arabic Table 1-3 (Appendix A image, pending reading ADD-03:p4-image/tp2-duration) prints '٤' (4). Under ADD-03:2.2 the Arabic governs, so the English row misstates a value that ADD-03:2.7 relies on to rejec…
  - unsupported: A translation discrepancy between a convenience translation and the governing image text. Before the value can be relied on, a person must approve the image reading and decide how the pack records that 4 hours governs for TP-2.
  - evidence: ADD-03:T1-3/tp-2 p5: “Maximum shutdown duration (hours): 6”; ADD-03:p4-image/tp2-duration p4: “٤”; ADD-03:2.2 p1: “The Arabic text governs.”
  - affected scope: units none; rows none; activities none; clarifications none
- **ESCALATED ADD-03/T1-3/note(1)** (ADD-03:T1-3/note(1)): English note (1) bans shutdowns only during Ramadan. The governing Arabic note 1 (pending reading ADD-03:p4-image/note1) also bans them during the Eid al-Fitr and Eid al-Adha holidays ('أو خلال إجازتَي عيد الفطر وعيد الأضحى'). Under ADD-03:2.2 the Arabic governs. The translation is therefore incomp…
  - unsupported: A translation omission between the convenience translation and the governing image text. A person must approve the image reading and decide how the pack records the governing blackout periods. The Eid holiday dates are not stated in the pack.
  - evidence: ADD-03:T1-3/note(1) p5: “(1) No shutdown is permitted during the holy month of Ramadan.”; ADD-03:p4-image/note1 p4: “١. لا يُسمح بأي إيقاف خلال شهر رمضان المبارك أو خلال إجازتَي عيد الفطر وعيد الأضحى.”; ADD-03:2.2 p1: “The Arabic text governs.”
  - affected scope: units none; rows none; activities none; clarifications none
- **UNRESOLVED ADD-03:2.2** (clause, p1): not promotable: ADD-03/2.2 conflicting (declared_conflicts: the proposer declares: ADD-03:T1-3/tp-2; ADD-03:T1-3/note(1))
- **UNRESOLVED ADD-03:2.3** (clause, p1): not promotable: ADD-03/2.3 insufficient_evidence (missing_information: the proposer declares missing: An A1 register row for this obligation (C46 need reported by simulate_amendment).)
- **UNRESOLVED ADD-03:2.7** (clause, p1): not promotable: ADD-03/2.7 conflicting (declared_conflicts: the proposer declares: ADD-03:T1-3/tp-2); ADD-03/2.7-issue interpretation_pending (dropped: )
- **UNRESOLVED ADD-03:Q17** (table_row, p2): not promotable: ADD-03/Q17 insufficient_evidence (missing_information: the proposer declares missing: the wording of Clause 12.3 as amended: the addendum says 'is amended accordingly' and prints no replacement or added text)
- **UNRESOLVED ADD-03:Q18** (table_row, p2): not promotable: ADD-03/Q18 insufficient_evidence (missing_information: the proposer declares missing: whether a shortfall in network inflow during the reliability run is a Relief Event under VOL-V 34.2: the Relief Event list does …); ADD-03/Q18-clar interpretation_pending (dropped: )
- **UNRESOLVED ADD-03:Q19** (table_row, p3): not promotable: ADD-03/Q19 conflicting (declared_conflicts: the proposer declares: VOL-II:7.4)
- **UNRESOLVED ADD-03:p4-image/tp1-location** (reading_block, p4): not promotable: ADD-03/p4-image/tp1-location insufficient_evidence (missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval; a person should confirm the term خط الطرد ('rising main').)
- **UNRESOLVED ADD-03:p4-image/tp1-diameter** (reading_block, p4): not promotable: ADD-03/p4-image/tp1-diameter insufficient_evidence (missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.)
- **UNRESOLVED ADD-03:p4-image/tp1-window** (reading_block, p4): not promotable: ADD-03/p4-image/tp1-window insufficient_evidence (missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.)
- **UNRESOLVED ADD-03:p4-image/tp1-duration** (reading_block, p4): not promotable: ADD-03/p4-image/tp1-duration insufficient_evidence (missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.)
- **UNRESOLVED ADD-03:p4-image/tp1-notice** (reading_block, p4): not promotable: ADD-03/p4-image/tp1-notice insufficient_evidence (missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.)
- **UNRESOLVED ADD-03:p4-image/tp2-point** (reading_block, p4): not promotable: ADD-03/p4-image/tp2-point insufficient_evidence (missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.)
- **UNRESOLVED ADD-03:p4-image/tp2-location** (reading_block, p4): not promotable: ADD-03/p4-image/tp2-location insufficient_evidence (missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval; a person should confirm the term خط الانحدار ('gravity line/sewer').)
- **UNRESOLVED ADD-03:p4-image/tp2-diameter** (reading_block, p4): not promotable: ADD-03/p4-image/tp2-diameter insufficient_evidence (missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.)

## Earlier answers to re-read against the new text (never revoked; a person decides)

- `ADD-03:Q18` (ADD-03): cites VOL-II:7.2, changed by ADD-03/3.1; to be re-read against the new text of VOL-II:7.2 (ADD-03/3.1); a person decides whether the answer still holds
- `ADD-03:Q19` (ADD-03): cites VOL-II:7.2, changed by ADD-03/3.1; cites VOL-II:8.2, changed by ADD-03/4.1(b); to be re-read against the new text of VOL-II:7.2, VOL-II:8.2 (ADD-03/3.1, ADD-03/4.1(b)); a person decides whether the answer still holds
- `ADD-03:Q20` (ADD-03): cites VOL-II:1.3, changed by ADD-03/2.1; to be re-read against the new text of VOL-II:1.3 (ADD-03/2.1); a person decides whether the answer still holds

## Derived effects (session 12: pending readings, computed deadlines, conditions, consequences)

## Computed deadlines and the Working Days left (PROPOSED; nothing typed)

- Working Days left from the issue date (2026-11-10) to the PDD (2026-11-26): 12 (the issue date not counted, the PDD counted; Working Days per VOL-I 2.4 (weekend [4, 5] as date.weekday numbers; holidays none declared))
- `ADD-03:2.5` p1: “eight (8) Working Days before the Proposal Due Date” -> **2026-11-16** (computed: calc deadline, anchor PDD = 2026-11-26, rule working-days-before, fingerprint 5a8830b5a549; PROPOSED, not validated)

## Bands and the existing bid-out rules (derived consequences are PROPOSED; HUMAN DECISION PENDING)

- `VOL-II:7.2`: “not less than 85% and not more than 110% of nominal capacity” — no bid-out consequence stated
- `ADD-03:3.1`: “not less than 85% and not more than 110% of nominal capacity’ is substituted.” — no bid-out consequence stated

## Per provision: source evidence → proposed transition → validation → downstream impact → output difference

### ADD-03:cover/para1 (paragraph, p1) — answered
- source: “Issued 10 November 2026”
- transition: `ADD-03/cover/para1` disposition no_effect: Issue date line 'Issued 10 November 2026'; it changes no provision (it dates the addendum).
  - validation: **evidence_verified**

### ADD-03:cover/para2 (paragraph, p1) — answered
- source: “Tender NUPA/ISTP/2026/014”
- transition: `ADD-03/cover/para2` disposition no_effect: Title/tender reference 'Tender NUPA/ISTP/2026/014'; it changes no provision.
  - validation: **evidence_verified**

### ADD-03:cover/para3 (paragraph, p1) — answered
- source: “This Addendum incorporates the Network Operator's Table 1-3 describing the two tie-in points referred to in Volume II Clause 1.3, requires a Bidder that elects to interrupt flows at a tie-in point to obtain the Authority's acceptance of its shutdown programme, applications for which shall be made within eight (8) Working Days of the date of this Addendum, i…”
- transition: `ADD-03/cover/para3` amendment_op annotate ADD-03:cover/para3 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The cover paragraph is both the provision and the target, which is why the target is flagged as uncertain. This is acceptable for an annotate op, because the only obligation of its own is the Form 4-A acknowledgement. The other listed changes are not made by this paragraph, and the note says so.
    - concern: The adds_obligation effect is an interpretation. A person should confirm it.
- transition: `ADD-03/cover/para3/issue-shutdown` issue {"text": "The ADD-03 cover summary and operative Clause 2.5 disagree on the tie-in shutdown application. The cover says 'the Authority's acceptance' with applications 'within eight (8) Working Days o…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The conflict is real on the quoted words. The cover says the Authority's acceptance, with applications within 8 Working Days of the date of the Addendum. Clause 2.5 says a Network Operator letter, with applications at least 8 Working Days before the Proposal Due Date.
    - concern: The payload says 'forward from 10 November 2026'. That date is not in the evidence shown, so it is unverified.
    - concern: The item does not say which provision governs. The cover says the Addendum takes precedence under Vol I 3.2, but that does not settle a cover-versus-operative conflict. Leaving it to the person is correct.
- transition: `ADD-03/cover/para3/issue-rampup` issue {"text": "The ADD-03 cover summary says the new Unavailability Event (loss of treated effluent volume) applies 'with no deduction during the Ramp-Up Period'. Operative Clauses 5.1 and 5.2 add event 3…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The cover does say 'no deduction during the Ramp-Up Period'. ADD-03:5.1 as shown adds event (d) with no Ramp-Up wording. This part is supported.
    - concern: The claim that a search of all of ADD-03 found no Ramp-Up exclusion cannot be verified. Only units 5.1 and 5.2 (partial) and the cover are shown.
    - concern: The statement that VOL-V 29.3 covers Table 2-4 parameters only is not supported by any text in the evidence. VOL-V 29.3 is not printed.
    - concern: Without the full ADD-03 text and VOL-V 29.3, the evidence does not show that no Ramp-Up exclusion is in force. The issue may still be worth raising, but its stated basis is not shown.
  - downstream proposal `DS-06` row_new (c46:ADD-03/cover/para3): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-07` issue (c46:ADD-03/cover/para3): **interpretation_pending — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: The three differences are supported by the quoted text. The cover says the Authority accepts the programme, but 2.5 requires a Network Operator letter. The cover sets the deadline at 8 Working Days from the Addendum date, but 2.5 sets it at 8 Working Days before the Proposal Due Date. The cover say…
      - concern: Whether ADD-03 5.1 or 5.2 says anything about Ramp-Up for limb (d) is not shown in full. S-F6 asserts that neither does.
      - concern: The interim advice to plan to 'the earlier of the two deadlines' cannot be checked, because the Addendum date and Proposal Due Date are not in the evidence. The advice to price (d) deductions as applying in Ramp-Up is a conservative planning assumption, not a ruling. The person deciding should trea…
  - downstream proposal `DS-08` clarification_item (c46:ADD-03/cover/para3): **interpretation_pending — HUMAN DECISION PENDING**
  - output difference: NEW ADD-03-cover-para3-01; A5 REWORK form-4a; A5 REWORK form-4a-prep

### ADD-03:1.1 (clause, p1) — answered
- source: “This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.”
- transition: `ADD-03/1.1` disposition no_effect: Recital: 'This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.' It states t…
  - validation: **evidence_verified**

### ADD-03:1.2 (clause, p1) — answered
- source: “A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.”
- transition: `ADD-03/1.2` disposition no_effect: Interpretation rule: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless other…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'unless')
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: no_effect is right in that Clause 1.2 amends no unit. It does fix the stage at which cross-references are read, as amended by Addenda 1 and 2. That is consistent with the ADD-02 stage used here.
    - concern: 'Unless otherwise stated' could be triggered by a later provision. The person should confirm that no ADD-03 clause states a different reading.

### ADD-03:2.1 (clause, p1) — answered
- source: “Volume II Clause 1.3 is amended by adding at the end: ‘The two designated tie-in points are TP-1 and TP-2, described in Table 1-3, which is reproduced at Appendix A to this Addendum as issued by the Northern Region Water Services Company (the Network Operator) and is incorporated into this Volume by reference.’”
- transition: `ADD-03/2.1` amendment_op append_text VOL-II:1.3 “” → “The two designated tie-in points are TP-1 and TP-2, described in Table 1-3, whi…”
  - validation: **evidence_verified**
  - downstream: units changed VOL-II:1.3; rows citing them VOL-II-1.3-01
  - downstream proposal `DS-ADD03-VOL-II-1.3-01` row_reading (row:VOL-II-1.3-01): **insufficient_evidence**
  - downstream proposal `DS-ADD03-DEP-1.3-T13` dependency (row:VOL-II-1.3-01): **interpretation_pending**
  - downstream proposal `DS-09` clarification_item (clar:CQ-VOL-III-DRAWINGS): **insufficient_evidence — HUMAN DECISION PENDING**
  - output difference: CHANGED VOL-II-1.3-01; A5 REWORK technical-proposal

### ADD-03:2.2 (clause, p1) — UNRESOLVED
- source: “Table 1-3 is issued in the Arabic language. The Arabic text governs. The English translation at Appendix B is provided for convenience only.”
- transition: `ADD-03/2.2` amendment_op annotate ADD-03:T1-3 effect interprets
  - validation: **conflicting — HUMAN DECISION PENDING** — declared_conflicts: the proposer declares: ADD-03:T1-3/tp-2; ADD-03:T1-3/note(1)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The Arabic values (TP-2 duration ٤, Arabic note 1 with the Eid holidays) rest on pending reading blocks and a crop I cannot see. I could only check the text of 2.2, the image caption and AppB/para1.
    - concern: The precedence is stated for Table 1-3 as a whole. The item treats ADD-03:p4-image as the governing unit and ADD-03:T1-3 as the convenience translation. That follows from 2.2 and AppB/para1, but a person should confirm it.
    - concern: The target is T1-3, the English table, while the governing unit is the image. This is a deliberate group target, not a unit that 2.2 names.
  - downstream proposal `DS-13` escalation (esc:ADD-03:2.2): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
      - concern: 2.2 says the Arabic text governs, and the Arabic reading (٤, i.e. 4) differs from the English 6. The Arabic note 1 also adds the Eid holidays to the Ramadan exclusion. The conflict is real on the evidence shown.
      - concern: The Arabic reading is still pending approval, so the TP-2 duration and the excluded periods cannot yet be fixed.
      - concern: The item says only that the Arabic value 'differs'. It does not state it. The evidence shows ٤ at ADD-03:p4-image/tp2-duration.
      - concern: The reliance of 2.3(b) and 2.7 on these figures is not shown in the printed evidence.
  - downstream proposal `DS-14` issue (esc:ADD-03:2.2): **interpretation_pending — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: This is the same Arabic/English discrepancy as DS-13, framed as an issue for Legal. It is supported by 2.2 and by the pending Arabic reading.
      - concern: The feed into 2.3 and 2.7 is not shown in the printed evidence.
      - concern: Both the TP-2 duration and the excluded periods rest on an unapproved Arabic reading.
      - concern: The issue leaves the conclusion to a person, which is appropriate.

### ADD-03:2.3 (clause, p1) — UNRESOLVED
- source: “The Bidder shall elect, for each tie-in point, one of the following methods of maintaining flows during the connection works, and shall state its election in the construction methodology section of the Technical Proposal: (a) temporary over-pumping, without interruption of flow in the existing collection network; or (b) interruption of flow within the permi…”
- transition: `ADD-03/2.3` amendment_op annotate ADD-03:p4-image effect adds_obligation
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: An A1 register row for this obligation (C46 need reported by simulate_amendment).
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: 2.3 cites 'Table 1-3' without naming a unit. Choosing the Arabic image as the target, with the English table as a second target, is an inference that depends on 2.2.
    - concern: The note says both windows agree with English Appendix B. Only the English TP-2 row (01:00 to 05:00) is shown, so the TP-1 window cannot be checked here.
    - concern: The Arabic window readings are pending, and the item itself lists the A1 register row as missing.
    - concern: I2 and the claim that 2.3 does not change VOL-II:1.3 are not supported by any evidence shown.
  - downstream proposal `DS-15` row_new (esc:ADD-03:2.3): **interpretation_pending**
  - downstream proposal `DS-16` escalation (esc:ADD-03:2.3): **escalated**
  - output difference: NEW ADD-03-2.3-01; A5 REWORK technical-proposal

### ADD-03:2.4 (clause, p1) — UNRESOLVED
- source: “The temporary works for method (a) shall be capable of passing, at each tie-in point, the maximum transfer flow stated for that tie-in point in Table 1-3.”
- transition: `ADD-03/2.4` escalation why: Insufficient evidence. ADD-03:2.4 (and Q20) require the method (a) temporary works to pass 'the maximum transfer flow stated for that tie-in point in Table 1-3'. Table 1-3 states no maximum transfer …
  - validation: **escalated** — missing_information: the proposer declares missing: The maximum transfer flow for TP-1 and for TP-2 (with units).
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The English header row shown has no flow column, which supports the claim. The claim for the Arabic table and for the notes relies on the proposer's own viewing of the image. Only the Arabic duration header is quoted.
    - concern: The English notes are not printed in full in the evidence, so 'no note states a flow' cannot be fully verified here.
    - concern: Escalation is reasonable. An annotate or a derived flow would be unsupported.
- transition: `ADD-03/2.4-clarification` clarification {"gap": "ADD-03:2.4 and the response to Q20 refer to the maximum transfer flow stated for each tie-in point in Table 1-3, but Table 1-3 (Arabic Appendix A and English Appendix B) states no transfer f…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The practical_impact says method (a) is the default under 2.6. ADD-03:2.6 is not in the evidence shown, so that statement is unsupported here.
    - concern: The proposed question cites Q20, but this item's own evidence lists only 2.4.
  - downstream proposal `ADD-03-DS-ESC-2.4` escalation (esc:ADD-03:2.4): **escalated**
  - downstream proposal `ADD-03-DS-ISSUE-2.4` issue (esc:ADD-03:2.4): **interpretation_pending — HUMAN DECISION PENDING**

### ADD-03:2.5 (clause, p1) — UNRESOLVED
- source: “Where the Bidder elects method (b) for a tie-in point, it shall submit with Envelope A a letter from the Network Operator accepting the Bidder's proposed shutdown programme for that tie-in point (a Shutdown Acceptance Letter). Applications for a Shutdown Acceptance Letter shall be made to the Network Operator not later than eight (8) Working Days before the…”
- transition: `ADD-03/2.5` escalation why: ADD-03:2.5 adds a conditional Envelope A submission: a Shutdown Acceptance Letter from the Network Operator where method (b) is elected, applied for not later than eight (8) Working Days before the P…
  - validation: **escalated** — missing_information: the proposer declares missing: Confirmation that the operative 2.5 (Network Operator; 8 WD before PDD) prevails over the cover summary (Authority; within 8 WD of the Addendum date). The ADD-03 issue date was not found i…
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The 2026-11-16 deadline depends on assumption A2: PDD 2026-11-26 and a Sunday to Thursday working week. The PDD and calendar are not shown. Counting back eight working days on that basis does give 16 November.
    - concern: The Arabic note 3 reading says 'للشركة' (the company's portal). The item equates this with the Network Operator's portal, which is not established by the words quoted.
    - concern: The cover/clause discrepancy is real in the quoted text (Authority versus Network Operator; within 8 WD of the Addendum date versus 8 WD before the PDD). The cover is non-operative and the item says so.
  - downstream proposal `ADD-03-DS-ESC-2.5` escalation (esc:ADD-03:2.5): **escalated**
  - downstream proposal `D-17` row_new (date:ADD-03:2.5): **invalid**
  - downstream proposal `D-18` evidence_item (date:ADD-03:2.5): **insufficient_evidence** — held back: no promotable row or activity uses EV-SHUTDOWN-ACCEPTANCE
  - downstream proposal `D-19` activity (date:ADD-03:2.5): **invalid**

### ADD-03:2.6 (clause, p1) — UNRESOLVED
- source: “A Bidder that elects method (b) for a tie-in point but does not submit a Shutdown Acceptance Letter for that tie-in point with Envelope A shall be deemed to have elected method (a) for that tie-in point.”
- transition: `ADD-03/2.6` escalation why: ADD-03:2.6 is a deeming rule: method (b) without a Shutdown Acceptance Letter in Envelope A is deemed an election of method (a). It changes the consequence of the obligations in 2.3 and 2.5, both of …
  - validation: **escalated**
  - downstream proposal `ADD-03-DS-ESC-2.6` escalation (esc:ADD-03:2.6): **escalated**

### ADD-03:2.7 (clause, p1) — UNRESOLVED
- source: “A Proposal that provides for an interruption of flow at a tie-in point for longer than the maximum shutdown duration stated for that tie-in point in Table 1-3 shall be rejected.”
- transition: `ADD-03/2.7` amendment_op annotate ADD-03:p4-image effect adds_obligation
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:T1-3/tp-2
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The 4 h versus 6 h conflict for TP-2 depends on a pending Arabic reading of one digit that I cannot verify. Interpretation I1 is pending.
    - concern: 2.7 says 'Table 1-3' without naming a unit. Choosing the Arabic image as target follows from 2.2 but is an inference.
    - concern: The A1/A3 register rows are missing, as the item itself declares.
    - concern: The rejection consequence follows from 2.7's words. A bid relying on 6 h for TP-2 would be rejected only if the Arabic ٤ is confirmed.
- transition: `ADD-03/2.7-issue` issue {"text": "The governing Arabic Table 1-3 gives TP-2 a maximum shutdown duration of ٤ (4) hours; the English convenience translation says 6. Under ADD-03:2.7 a Proposal exceeding the governing value i…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The statement 'Shutdown programmes must follow the Arabic' is a conclusion that depends on pending interpretation I1 and on the pending Arabic reading.
    - concern: The Eid point rests on the quoted Arabic note 1 reading and on the English note, which is only partly shown. It is not in this item's own evidence list.
    - concern: The target T1-3/tp-2 is the English row, while the governing value is in the Arabic image.
  - downstream proposal `ADD-03-DS-ESC-2.7` escalation (esc:ADD-03:2.7): **conflicting**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-sonnet-5-5
      - concern: ADD-03:2.7 does say a Proposal is rejected if an interruption exceeds the maximum shutdown duration stated for that tie-in point in Table 1-3.
      - concern: The conflict rests on the TP-2 figures: a 01:00–05:00 window (4 hours) against a 6-hour maximum. The Table 1-3 row (ADD-03:T1-3/tp-2) is not printed in the units or evidence, so I cannot check those figures.
      - concern: The cited span for the statement is only clause 2.7. It does not contain the TP-2 values.
      - concern: Clause 2.7 refers only to the 'maximum shutdown duration'. Whether the permitted window also acts as a limit depends on Table 1-3 text I cannot see.
      - concern: I cannot confirm a real conflict from the evidence shown.

### ADD-03:3.1 (clause, p2) — answered
- source: “In Volume II Clause 7.2, ‘at not less than 90% of nominal capacity’ is deleted and ‘at a daily average flow, measured at the inlet works, of not less than 85% and not more than 110% of nominal capacity’ is substituted.”
- transition: `ADD-03/3.1` amendment_op replace_text VOL-II:7.2 “at not less than 90% of nominal capacity” → “at a daily average flow, measured at the inlet works, of not less than 85% and …”
  - validation: **evidence_verified**
  - downstream: units changed VOL-II:7.2; rows citing them VOL-II-7.2-01
  - downstream proposal `DS-ADD03-VOL-II-7.2-01` row_reading (row:VOL-II-7.2-01): **insufficient_evidence**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: The controller's replace_requirement check failed: the old value is not the row's requirement, or the new value is empty. The payload shows no 'old' field, so the proposed requirement replacement is not validated.
      - concern: The controller status is insufficient_evidence. The row's text before the addendum is not shown, so I cannot confirm the replace_requirement target.
      - concern: The 85%-110% band wording matches ADD-03:3.1, and the 7.3 restart wording is quoted verbatim. Nothing shown says what happens if a day falls outside the band. The item itself leaves that open for a person.
      - concern: The note about the 30-day rolling-average limit, VOL-V 1.5, and VOL-V 18.1/18.3 cites provisions that are not in the evidence shown, so I could not check them.
  - downstream proposal `DS-11` clarification_item (clar:CQ-PCOD-RELIABILITY-RUN): **insufficient_evidence — HUMAN DECISION PENDING**
  - downstream proposal `D-20` escalation (cons:VOL-II:7.2): **escalated**
  - downstream proposal `D-21` escalation (cons:ADD-03:3.1): **escalated**
  - output difference: CHANGED VOL-II-7.2-01; A5 REWORK technical-proposal

### ADD-03:3.2 (clause, p2) — answered
- source: “A day on which the daily average flow is outside that range shall not count towards the thirty (30) days. Volume II Clause 7.3 is unchanged.”
- transition: `ADD-03/3.2(a)` escalation why: The first sentence of ADD-03:3.2 adds a counting rule to the 30-day reliability run, but it does not cite Volume II Clause 7.2 by number. It relies on 'that range' (from 3.1) and 'the thirty (30) day…
  - validation: **escalated** — missing_information: the proposer declares missing: whether an out-of-range day suspends or breaks the 'continuous' 30-day run
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Escalation is reasonable: 3.2 does not cite 7.2 by number; 'that range' and 'the thirty (30) days' refer back to 3.1, whose text is not shown here, so the link to 7.2 is an inference (S-I1).
    - concern: Interaction of 'shall not count' with 'continuous' in 7.2 is genuinely unresolved on the evidence; 3.2 itself says only 7.3 is unchanged and is silent on 7.2's continuity wording.
    - concern: The mention of Q18/Volume V Clause 34 is not in the printed evidence; I did not rely on it.
- transition: `ADD-03/3.2(b)` amendment_op annotate VOL-II:7.3 effect confirms
  - validation: **evidence_verified**

### ADD-03:4.1 (clause, p2) — answered
- source: “Volume II Clauses 8.1 to 8.3 are deleted and replaced by the following: ‘8.1 The Project Company shall hold a spare parts inventory sufficient for eighteen (18) months of normal operation for all items with a lead time exceeding twelve (12) weeks, and shall record that inventory in the asset register required by Clause 7.4.’ ‘8.3 The Project Company shall e…”
- transition: `ADD-03/4.1(a)` amendment_op replace_text VOL-II:8.1 “The Project Company shall hold a spare parts inventory sufficient for two (2) y…” → “The Project Company shall hold a spare parts inventory sufficient for eighteen …”
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
    - concern: The new 8.1 text matches the quoted replacement minus the '8.1' label; the old text matches VOL-II:8.1 exactly.
    - concern: The new text adds a reference to Clause 7.4's asset register. Clause 7.4 is not shown in the evidence, so the claim that it is due 60 days after PCOD cannot be verified here.
    - concern: The change goes beyond a quantity change (2 years to 18 months), since it also adds a recording obligation. A person should note that.
- transition: `ADD-03/4.1(b)` amendment_op set_status VOL-II:8.2
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because removal; model claude-sonnet-5-5
    - concern: The reading is plausible: 8.2 lies in the range '8.1 to 8.3' that is deleted. Replacement text is printed only for 8.1 and 8.3, and 4.2 says there is no renumbering.
    - concern: It is still an inference that the Authority meant to drop the CMMS obligation. The clause could be an omission, so a clarification question is warranted; the item itself flags this.
    - concern: 4.2 does not list 8.2 as unchanged, which is consistent with deletion.
- transition: `ADD-03/4.1(c)` amendment_op replace_text VOL-II:8.3 “The Project Company shall employ a suitably qualified plant manager and shall m…” → “The Project Company shall employ a plant manager holding a degree in chemical, …”
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
    - concern: The old text matches VOL-II:8.3 and the new text matches the quoted replacement for 8.3.
    - concern: The change adds substantive requirements: a degree, ten years' experience, and naming the manager in the Technical Proposal with a CV appendix. The two-operator requirement is retained unchanged.
  - downstream: units changed VOL-II:8.1, VOL-II:8.2, VOL-II:8.3; rows citing them VOL-II-8.1-01, VOL-II-8.2-01, VOL-II-8.3-01, VOL-II-8.3-02
  - downstream proposal `DS-ADD03-VOL-II-8.1-01` row_reading (row:VOL-II-8.1-01): **insufficient_evidence**
  - downstream proposal `DS-ADD03-VOL-II-8.2-01` escalation (row:VOL-II-8.2-01): **escalated**
  - downstream proposal `DS-ADD03-VOL-II-8.3-01` row_reading (row:VOL-II-8.3-01): **insufficient_evidence**
  - downstream proposal `DS-ADD03-VOL-II-8.3-02` row_reading (row:VOL-II-8.3-02): **interpretation_pending**
  - downstream proposal `DS-12` activity (act:technical-proposal): **interpretation_pending**
  - output difference: OUT VOL-II-8.2-01; CHANGED VOL-II-8.1-01; CHANGED VOL-II-8.3-01; CHANGED VOL-II-8.3-02; A5 REWORK technical-proposal

### ADD-03:4.2 (clause, p2) — answered
- source: “The Clauses of Volume II are not renumbered. Volume II Clauses 8.4 and 8.5 are unchanged.”
- transition: `ADD-03/4.2` amendment_op annotate VOL-II:8.4, VOL-II:8.5 effect confirms
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: The target field names only 8.4, but the payload annotates 8.4 and 8.5. VOL-II:8.5 is not shown in the evidence, so I could not check it directly. 4.2 does state that 8.5 is unchanged.
    - concern: The 'not renumbered' sentence is not annotated on any unit. It is only referenced in the note.
  - downstream proposal `DS-ADD03-VOL-II-8.4-01` row_reading (row:VOL-II-8.4-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-VOL-II-8.4-02` row_reading (row:VOL-II-8.4-02): **interpretation_pending**
  - downstream proposal `DS-ADD03-VOL-II-8.5-01` row_reading (row:VOL-II-8.5-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-VOL-II-8.5-02` row_reading (row:VOL-II-8.5-02): **interpretation_pending**
  - output difference: CONFIRMED (unchanged) VOL-II-8.4-01; CONFIRMED (unchanged) VOL-II-8.4-02; CONFIRMED (unchanged) VOL-II-8.5-01; CONFIRMED (unchanged) VOL-II-8.5-02; A5 CONFIRMED (unchanged) technical-proposal

### ADD-03:5.1 (clause, p2) — answered
- source: “In Volume V Clause 31.1, ‘(b) the treated effluent fails any parameter in Volume II Table 2-4, or (c) the Facility fails to deliver treated effluent to the delivery point at the required residual head.’ is deleted and ‘(b) the treated effluent fails any parameter in Volume II Table 2-4, (c) the Facility fails to deliver treated effluent to the delivery poin…”
- transition: `ADD-03/5.1` amendment_op replace_text VOL-V:31.1 “(b) the treated effluent fails any parameter in Volume II Table 2-4, or (c) the…” → “(b) the treated effluent fails any parameter in Volume II Table 2-4, (c) the Fa…”
  - validation: **evidence_verified**
  - downstream: units changed VOL-V:31.1; rows citing them VOL-V-31.1-01, VOL-V-31.1-02, VOL-V-31.1-03
  - downstream proposal `DS-ADD03-VOL-V-31.1-01` row_reading (row:VOL-V-31.1-01): **interpretation_pending**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: The row reads limb (a), which ADD-03 leaves unchanged. The addendum adds limb (d), and the item correctly flags that (d) is not read in this row. A person should decide whether (d) needs its own row.
      - concern: The statement S-311-D says (d) creates an 'Unavailability Event'. The lead-in text of 31.1 is not shown, so that label is not verifiable from the evidence shown.
      - concern: The note that deductions have no cap and that Schedule 7 is not supplied is not supported by the evidence shown. Only the quote from 31.2 is shown.
      - concern: The ADD-03:5.1 evidence span is only 'In Volume V Clause 31.1'. The substance of the change is supported by the (d) wording in the unit text.
  - downstream proposal `DS-01` row_reading (row:VOL-V-31.1-02): **interpretation_pending**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: Limb (b) is re-stated with identical words in the 5.1 substitution, and 31.2 supplies the Schedule 7 deduction and no-cap wording. This follows from the text.
      - concern: The note's statements that 31.3 as amended by ADD-03 5.2 gives no cure period for (b), and that the TN limit is 3 mg/l (ADD-02 5.1), are not backed by the ADD-03 5.1 text printed here. They rest on S-F2 and other units that are not shown. I could not verify the TN figure.
      - concern: Pending a person's decision on the interpretation.
  - downstream proposal `DS-02` row_reading (row:VOL-V-31.1-03): **interpretation_pending**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: Limb (c) is kept verbatim. The substitution only changes the closing punctuation to ', or (d)', as the note says.
      - concern: The 72-hour cure period for (c) comes from 31.3, which is not printed here. It is cited only in S-F2, which this item does not list among its statements.
      - concern: The claim that the delivery point appears only on Drawing 03-C-114, and that this drawing was not supplied, is not in the evidence shown. I could not verify it.
  - downstream proposal `DS-10` clarification_item (clar:CQ-PERSISTENT-BREACH): **insufficient_evidence — HUMAN DECISION PENDING**
  - output difference: CHANGED VOL-V-31.1-01; CHANGED VOL-V-31.1-02; CHANGED VOL-V-31.1-03; A5 REWORK deviations-review; A5 REWORK form-4e

### ADD-03:5.2 (clause, p2) — answered
- source: “In Volume V Clause 31.3, ‘No cure period applies to an event under Clause 31.1(b).’ is deleted and ‘No cure period applies to an event under Clause 31.1(b) or Clause 31.1(d).’ is substituted.”
- transition: `ADD-03/5.2` amendment_op replace_text VOL-V:31.3 “No cure period applies to an event under Clause 31.1(b).” → “No cure period applies to an event under Clause 31.1(b) or Clause 31.1(d).”
  - validation: **evidence_verified**
  - downstream: units changed VOL-V:31.3; rows citing them VOL-V-31.3-01, VOL-V-31.3-02, VOL-V-31.3-03
  - downstream proposal `DS-03` row_reading (row:VOL-V-31.3-01): **interpretation_pending**
  - downstream proposal `DS-04` row_reading (row:VOL-V-31.3-02): **interpretation_pending**
  - downstream proposal `DS-05` row_reading (row:VOL-V-31.3-03): **insufficient_evidence**
  - output difference: CHANGED VOL-V-31.3-01; CHANGED VOL-V-31.3-02; CHANGED VOL-V-31.3-03; A5 REWORK deviations-review; A5 REWORK form-4e

### ADD-03:Q15 (table_row, p2) — answered
- source: “No: 15 | Bidder question: Is the Network Operator owned or controlled by the Authority? | Authority response: No. The Network Operator is a separate company. Its ownership has no bearing on any requirement of the RFP Documents.”
- transition: `ADD-03/Q15` disposition no_effect: This is a factual answer about who owns the Network Operator. It does not amend, oblige or except anything. The response says so itself: 'Its ownership has no …
  - validation: **evidence_verified**

### ADD-03:Q16 (table_row, p2) — answered
- source: “No: 16 | Bidder question: May ozonation be used as the disinfection process? | Authority response: Ozonation shall not be used as the sole means of disinfection. Disinfection shall be by chlorination with provision for dechlorination, or by ultraviolet irradiation with a validated dose, or by a combination. Volume II Clause 3.3 applies.”
- transition: `ADD-03/Q16` amendment_op annotate VOL-II:3.3 effect confirms
  - validation: **interpretation_pending — HUMAN DECISION PENDING** — semantic: annotated 'confirms', but the answer adds: a sentence of obligation carries words the annotated units do not print: 'Ozonation shall not be used as the sole means of disinfection.' (adds: used, sole, means)
  - downstream proposal `DS-ADD03-VOL-II-3.3-01` row_reading (row:VOL-II-3.3-01): **interpretation_pending**
  - output difference: CONFIRMED (unchanged) VOL-II-3.3-01; A5 CONFIRMED (unchanged) technical-proposal

### ADD-03:Q17 (table_row, p2) — UNRESOLVED
- source: “No: 17 | Bidder question: Volume V Clause 12.3 provides that the reasonable costs of the Independent Engineer are borne equally by the parties. Does this apply to the Independent Engineer's attendance at a repeated reliability run? | Authority response: No. The reasonable costs of the Independent Engineer attributable to any reliability run after the first …”
- transition: `ADD-03/Q17` amendment_op annotate VOL-V:12.3 effect adds_obligation
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: the wording of Clause 12.3 as amended: the addendum says 'is amended accordingly' and prints no replacement or added text
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The response says 'amended accordingly' but prints no wording, so the annotation records substance only; a person may need to draft the clause text.
    - concern: 'Other costs stay shared equally' is an inference. It is implied by 'attributable to any reliability run after the first' but is not stated.
    - concern: Dependency on VOL-II:7.2 is not backed by any quoted text.
  - downstream proposal `ADD-03-DS-ESC-Q17` escalation (esc:ADD-03:Q17): **escalated**

### ADD-03:Q18 (table_row, p2) — UNRESOLVED
- source: “No: 18 | Bidder question: If the flow delivered to the Facility by the existing collection network during the reliability run under Volume II Clause 7.2 is lower than the flow required by that Clause, for reasons outside the Project Company's control, will the Project Company be entitled to relief? | Authority response: The Authority notes the question. Vol…”
- transition: `ADD-03/Q18` amendment_op annotate VOL-II:7.2 effect interprets
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: whether a shortfall in network inflow during the reliability run is a Relief Event under VOL-V 34.2: the Relief Event list does not name it
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The note says relief is subject to notice within five Working Days under VOL-V 34.3. No text of 34.3 is in the evidence, so that detail is unsupported.
    - concern: The 34.1 text (extension of time, no compensation) appears only in the statement evidence, not in the item's own evidence list.
    - concern: Whether a network inflow shortfall falls under 'failure of a utility not caused by the Project Company' is open. The item correctly flags this, but the 'interprets' effect rests on an unconfirmed interpretation.
    - concern: The response makes no amendment. The annotation is reasonable as a record, but the consequence detail goes beyond the evidence.
- transition: `ADD-03/Q18-clar` clarification {"gap": "The response to question 18 says 'Volume V Clause 34 applies' to a shortfall in network inflow during the reliability run. The Relief Event list in Clause 34.2 does not name such a shortfall…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `ADD-03-DS-ESC-Q18` escalation (esc:ADD-03:Q18): **escalated**

### ADD-03:Q19 (table_row, p3) — UNRESOLVED
- source: “No: 19 | Bidder question: Volume II Clause 7.4 requires an asset register in the Authority's standard format. Will the format be issued before the Proposal Due Date? | Authority response: No. The format will be issued to the Preferred Bidder. The asset register shall be maintained in the computerised maintenance management system required by Volume II Claus…”
- transition: `ADD-03/Q19` amendment_op annotate VOL-II:7.4 effect adds_obligation
  - validation: **conflicting** — declared_conflicts: the proposer declares: VOL-II:7.4
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
    - concern: The conflict is real on the words. VOL-II 7.4 requires the register not later than 60 days after PCOD. Q19 requires submission before the start of the 7.2 run, and 7.2 says PCOD is not certified until the run is complete, so the run precedes PCOD.
    - concern: It is unclear whether a Q&A response has the power to amend 7.4. A person must decide which governs.
    - concern: The format is issued only to the Preferred Bidder, which makes pre-run submission harder to price at bid stage. This is context, not a conflict.
  - downstream proposal `ADD-03-DS-ESC-Q19` escalation (esc:ADD-03:Q19): **conflicting**
    - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
      - concern: The timing conflict is supported by the text. Q19 requires submission before the start of the reliability run under Vol II 7.2. VOL-II:7.4 says not later than 60 days after PCOD. The evidence does not show how the reliability run is sequenced against PCOD, but the two deadlines differ either way.
      - concern: The claim that ADD-03/4.1(b) deletes Vol II Clause 8.2 is not supported by anything printed. Neither the 4.1(b) text nor Clause 8.2 is shown. The VOL-II:8.2 conflict and the 'is a CMMS still required' question therefore depend on unverified evidence.
      - concern: The response also says the standard format will be issued only to the Preferred Bidder. That does not conflict with 7.4 as shown.

### ADD-03:Q20 (table_row, p3) — UNRESOLVED
- source: “No: 20 | Bidder question: What design flow should be used for the temporary works needed to maintain flows at the tie-in points referred to in Volume II Clause 1.3? | Authority response: The temporary works shall be capable of passing the maximum transfer flow stated for each tie-in point in Table 1-3 at Appendix A to this Addendum. Section 2.4 of this Adde…”
- transition: `ADD-03/Q20` escalation why: Insufficient evidence. Q20 (and ADD-03 Clause 2.4) set the design flow for the temporary works at the tie-in points by reference to 'the maximum transfer flow stated for each tie-in point in Table 1-…
  - validation: **escalated** — missing_information: the proposer declares missing: the maximum transfer flow for TP-1 and for TP-2: Table 1-3 does not state it in either language
- transition: `ADD-03/Q20-clar` clarification {"gap": "Q20 and ADD-03 Clause 2.4 refer to a 'maximum transfer flow stated for each tie-in point in Table 1-3', but Table 1-3 (Arabic or English) states no such flow.", "proposed_question": "Table 1…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The English translation of Table 1-3 lacks a transfer flow column, and that is verifiable. But the Arabic text governs, and the claim that the Arabic has no such column rests only on the proposer's own reading of the image, which is still pending.
    - concern: The interim handling cites existing 1,000 mm and 800 mm sewers and TP-1/TP-2. These figures are not in the evidence shown.
    - concern: Q20 refers to Table 1-3 'at Appendix A', but the English table checked is the Appendix B translation (T1-3, p5). The target is plausible but its link to the cited provision is indirect.
  - downstream proposal `ADD-03-DS-CQ-2.4` clarification_item (esc:ADD-03:Q20): **evidence_verified**
  - downstream proposal `ADD-03-DS-ESC-Q20` escalation (esc:ADD-03:Q20): **escalated**

### ADD-03:AppA/para1 (paragraph, p4) — answered
- source: “The following table is reproduced as issued by the Network Operator under cover of its letter No. 312/2026 dated 5 November 2026. The Arabic text governs in accordance with Section 2.2 of this Addendum.”
- transition: `ADD-03/AppA/para1` disposition no_effect: This is the introductory paragraph of Appendix A. It identifies the table's source ('as issued by the Network Operator under cover of its letter No. 312/2026 d…
  - validation: **evidence_verified**
- transition: `ADD-03/AppA/para1-issue` issue {"text": "The Arabic Table 1-3 governs (ADD-03 2.2), but the English translation in Appendix B appears to differ from the Arabic image on page 4. (1) For TP-2 the Arabic maximum shutdown duration app…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The Arabic observations (TP-2 duration ٤ against 6, and the Eid holidays in note 1) cannot be checked from the evidence shown. Only the image crop hash and the proposer's own description are given.
    - concern: Only the English side is verified: TP-2 reads 6 and note (1) mentions Ramadan only. The mismatch itself is unconfirmed.
    - concern: The target T1-3 is the English translation. The governing Arabic unit is ADD-03:p4-image, so the target may not be the right unit for an issue about the Arabic text.
    - concern: The precedence point is supported by AppA/para1 and 2.2, so the issue is worth raising once the reading is approved.

### ADD-03:p4-image/hdr-en (reading_block, p4) — answered
- source: “Northern Region Water Services Company”
- transition: `ADD-03/p4-image/hdr-en` disposition no_effect: Letterhead name of the issuer printed in English at the top of the Network Operator's letter reproduced as Appendix A: 'Northern Region Water Services Company'…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Crop image not shown to me; I checked only the printed reading text. ADD-03:2.1 words support the incorporation claim.

### ADD-03:p4-image/hdr-ar (reading_block, p4) — answered
- source: “شركة خدمات المياه بالمنطقة الشمالية”
- transition: `ADD-03/p4-image/hdr-ar` disposition no_effect: Arabic letterhead 'شركة خدمات المياه بالمنطقة الشمالية' naming the issuer of the reproduced letter. Identification only; no change, obligation or exception.
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Crop not visible; judged on the reading text only.

### ADD-03:p4-image/ref (reading_block, p4) — answered
- source: “الرقم: ٣١٢/٢٠٢٦”
- transition: `ADD-03/p4-image/ref` disposition no_effect: Letter reference 'الرقم: ٣١٢/٢٠٢٦' of the reproduced Network Operator letter. Identification only; no change, obligation or exception.
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Crop not visible; the digits ٣١٢/٢٠٢٦ rely on the reading as printed. The reference number alone carries no change.

### ADD-03:p4-image/date (reading_block, p4) — answered
- source: “التاريخ: ٥ نوفمبر ٢٠٢٦م”
- transition: `ADD-03/p4-image/date` disposition no_effect: Letter date 'التاريخ: ٥ نوفمبر ٢٠٢٦م' of the reproduced Network Operator letter. It dates the document; it sets no deadline or milestone and prints no change, …
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The text is only a letter date, with no deadline wording, so no_effect follows. Crop not visible.

### ADD-03:p4-image/subject (reading_block, p4) — answered
- source: “الموضوع: نقاط الربط بشبكة التجميع القائمة لمحطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان”
- transition: `ADD-03/p4-image/subject` disposition no_effect: Subject line 'الموضوع: نقاط الربط بشبكة التجميع القائمة لمحطة معالجة مياه الصرف الصحي المستقلة بوادي السرحان' describing the letter. Descriptive only; no chang…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Descriptive subject line only; crop not visible.

### ADD-03:p4-image/tender-ref (reading_block, p4) — answered
- source: “مناقصة رقم: NUPA/ISTP/2026/014”
- transition: `ADD-03/p4-image/tender-ref` disposition no_effect: Tender reference 'مناقصة رقم: NUPA/ISTP/2026/014' identifying the tender the letter relates to. Identification only; no change, obligation or exception.
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Whether this tender number matches the tender's own reference is not in the evidence shown, so I could not check it. It is an identifier and changes nothing.

### ADD-03:p4-image/table-title (reading_block, p4) — answered
- source: “جدول ١-٣: نقاط الربط وشروط إيقاف التدفق”
- transition: `ADD-03/p4-image/table-title` disposition no_effect: Table caption 'جدول ١-٣: نقاط الربط وشروط إيقاف التدفق'. A title only; the table's content is in its rows and notes, incorporated by ADD-03:2.1. No change, obl…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Caption only; the rows and notes are other units and were not shown to me.

### ADD-03:p4-image/intro (reading_block, p4) — answered
- source: “تُحدِّد نقاط الربط بشبكة التجميع القائمة وشروط إيقاف التدفق فيها على النحو الآتي:”
- transition: `ADD-03/p4-image/intro` disposition no_effect: Lead-in sentence 'تُحدِّد نقاط الربط بشبكة التجميع القائمة وشروط إيقاف التدفق فيها على النحو الآتي:' introduces the table that follows ('على النحو الآتي:' = as…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The sentence uses the verb 'تُحدِّد' (specifies) and refers to flow-stopping conditions, but it only introduces the table with 'على النحو الآتي:'. It states no condition itself. That the substance sits in the table rows is not checkable from the units shown.

### ADD-03:p4-image/th-point (reading_block, p4) — answered
- source: “نقطة الربط”
- transition: `ADD-03/p4-th-point` disposition no_effect: Column heading 'نقطة الربط' of the Arabic Table 1-3 at Appendix A. It prints no change, obligation or exception. The table enters Volume II through ADD-03:2.1 …
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is still pending human confirmation. The no_effect conclusion rests on S4, which is an interpretation. The effect of the table is left to 2.1 and other batches.
- transition: `ADD-03/p4-issue-transfer-flow` issue {"text": "The governing Arabic Table 1-3 has six columns (tie-in point, location, existing line diameter, permitted shutdown window, maximum shutdown duration, advance notice) and none gives a maximu…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The unit list shows six heading cells (point, location, diameter, window, duration, notice) and none is a flow column. This supports the claim about the heading row. The readings are still pending.
    - concern: The evidence quotes only two of the six headings directly. The others are in S3 and in the units.
    - concern: The statement that the flow is 'not stated anywhere in the table' goes beyond the heading row. Body rows, notes or other text on page 4 are not shown. A flow could in principle appear outside a column, so a person should check the full page.
    - concern: The target 2.4 is not among the units cited by the provision (the th-point heading). The link is only the inconsistency between the heading row and 2.4.
    - concern: Q20 is named in the payload and dependencies, but no Q20 text is in the evidence. S2 (2.2, Arabic governs) is also quoted but its unit is not printed. I could not check either.

### ADD-03:p4-image/th-location (reading_block, p4) — answered
- source: “الموقع”
- transition: `ADD-03/p4-th-location` disposition no_effect: Column heading 'الموقع' of the Arabic Table 1-3 at Appendix A. It prints no change, obligation or exception. The table enters Volume II through ADD-03:2.1 ('is…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending confirmation. The conclusion depends on S4 and on 2.1 being answered elsewhere.

### ADD-03:p4-image/th-diameter (reading_block, p4) — answered
- source: “قطر الخط القائم (مم)”
- transition: `ADD-03/p4-th-diameter` disposition no_effect: Column heading 'قطر الخط القائم (مم)' of the Arabic Table 1-3 at Appendix A. It prints no change, obligation or exception. The table enters Volume II through A…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending confirmation. The conclusion depends on S4.

### ADD-03:p4-image/th-window (reading_block, p4) — answered
- source: “فترة الإيقاف المسموح بها”
- transition: `ADD-03/p4-th-window` disposition no_effect: Column heading 'فترة الإيقاف المسموح بها' of the Arabic Table 1-3 at Appendix A. It prints no change, obligation or exception. The table enters Volume II throu…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending confirmation. The conclusion depends on S4.

### ADD-03:p4-image/th-duration (reading_block, p4) — answered
- source: “أقصى مدّة للإيقاف (ساعة)”
- transition: `ADD-03/p4-th-duration` disposition no_effect: Column heading 'أقصى مدّة للإيقاف (ساعة)' of the Arabic Table 1-3 at Appendix A. It prints no change, obligation or exception. The table enters Volume II throu…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending confirmation. The reason refers to ADD-03:2.7 as a rejection rule, but 2.7's text is not shown in the evidence, so that remark cannot be checked here. It does not affect no_effect for the heading itself.

### ADD-03:p4-image/th-notice (reading_block, p4) — answered
- source: “مهلة الإشعار المسبق”
- transition: `ADD-03/p4-th-notice` disposition no_effect: Column heading 'مهلة الإشعار المسبق' of the Arabic Table 1-3 at Appendix A. It prints no change, obligation or exception. The table enters Volume II through AD…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending confirmation. The conclusion depends on S4.

### ADD-03:p4-image/table-rule (reading_block, p4) — answered
- source: “”
- transition: `ADD-03/p4-table-rule` disposition no_effect: Band 7 is the horizontal ruled line between the heading row and row TP-1 of the Arabic Table 1-3. It prints no characters (the reading notes 'no printed charac…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The evidence is a crop with an empty reading. A person should glance at the crop to confirm that it shows only a rule and no text.

### ADD-03:p4-image/tp1-point (reading_block, p4) — answered
- source: “TP-1”
- transition: `ADD-03/p4-tp1-point` disposition no_effect: Row identifier 'TP-1' in the 'نقطة الربط' column of the Arabic Table 1-3 at Appendix A. It is a label only and prints no change, obligation or exception. The t…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The quoted 2.1 span 'The two designated tie-in points are TP-1 and TP-2' is reported as verbatim by the controller. The 2.1 text is not printed in the units, so I could not check it myself. The reading is pending confirmation.

### ADD-03:p4-image/tp1-location (reading_block, p4) — UNRESOLVED
- source: “غرفة التفتيش MH-41 على خط الطرد الشمالي”
- transition: `ADD-03/p4-image/tp1-location` disposition no_effect: This is the TP-1 location cell of the Arabic Table 1-3 at Appendix A ('غرفة التفتيش MH-41 على خط الطرد الشمالي'). It is table content, not an amending instruct…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval; a person should confirm the term خط الطرد ('rising main').
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading ADD-03-p4-r1 is still pending approval, and the term خط الطرد ('rising main') needs a person to confirm it.
    - concern: No_effect applies to the cell as an amending instruction only. The cell's content takes effect through the ADD-03:2.1 op, which is outside this batch.
  - downstream proposal `ADD-03-DS-ESC-P4-LOC` escalation (esc:ADD-03:p4-image/tp1-location): **escalated**

### ADD-03:p4-image/tp1-diameter (reading_block, p4) — UNRESOLVED
- source: “١٠٠٠”
- transition: `ADD-03/p4-image/tp1-diameter` disposition no_effect: This is the TP-1 existing-sewer-diameter cell ('١٠٠٠', mm) of the Arabic Table 1-3 at Appendix A. It is table content, not an amending instruction: it prints n…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: No_effect covers only the absence of an old/new pair. The value is operative through the 2.1 incorporation.
  - downstream proposal `ADD-03-DS-ESC-P4-DIA` escalation (esc:ADD-03:p4-image/tp1-diameter): **escalated**

### ADD-03:p4-image/tp1-window (reading_block, p4) — UNRESOLVED
- source: “من ٢٣:٠٠ إلى ٠٥:٠٠”
- transition: `ADD-03/p4-image/tp1-window` disposition no_effect: This is the TP-1 permitted-shutdown-window cell ('من ٢٣:٠٠ إلى ٠٥:٠٠') of the Arabic Table 1-3 at Appendix A. It is table content, not an amending instruction:…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: No_effect covers only the absence of an old/new pair. The value is operative through the 2.1 incorporation.
  - downstream proposal `ADD-03-DS-ESC-P4-WIN` escalation (esc:ADD-03:p4-image/tp1-window): **escalated**

### ADD-03:p4-image/tp1-duration (reading_block, p4) — UNRESOLVED
- source: “٦”
- transition: `ADD-03/p4-image/tp1-duration` disposition no_effect: This is the TP-1 maximum-shutdown-duration cell ('٦', hours) of the Arabic Table 1-3 at Appendix A. It is table content, not an amending instruction: it prints…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The rationale says the cell is not visible in crop b08-right. It says the reading came from b08-left and the full region image.
    - concern: The evidence cites crop_sha256 7058ab6d…, the same hash as tp1-location, tp1-diameter and tp1-window. The tp1-notice item, which the rationale places in b08-left, cites a different hash. So the cited crop may not show the cell, and the evidence shown cannot confirm the '٦' reading against it.
    - concern: The reading is pending approval.
    - concern: The no_effect disposition itself is consistent with the text, but the reading's provenance needs a person to check it.
  - downstream proposal `ADD-03-DS-ESC-P4-DUR` escalation (esc:ADD-03:p4-image/tp1-duration): **escalated**

### ADD-03:p4-image/tp1-notice (reading_block, p4) — UNRESOLVED
- source: “١٠ أيام عمل”
- transition: `ADD-03/p4-image/tp1-notice` disposition no_effect: This is the TP-1 advance-notice cell ('١٠ أيام عمل') of the Arabic Table 1-3 at Appendix A. It is table content, not an amending instruction: it prints no old/…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: No_effect covers only the absence of an old/new pair. The value is operative through the 2.1 incorporation.
  - downstream proposal `D-01` escalation (esc:ADD-03:p4-image/tp1-notice): **escalated**

### ADD-03:p4-image/tp2-point (reading_block, p4) — UNRESOLVED
- source: “TP-2”
- transition: `ADD-03/p4-image/tp2-point` disposition no_effect: This is the tie-in-point identifier cell ('TP-2') of the second row of the Arabic Table 1-3 at Appendix A. It is table content, not an amending instruction: it…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: S-F4 flags an Arabic/English mismatch for the TP-2 duration (٤ in the Arabic, 6 in the English). That conflict belongs to the tp2-duration and T1-3/tp-2 items, not to this identifier cell. It should not be dropped when those items are reviewed.
  - downstream proposal `D-02` escalation (esc:ADD-03:p4-image/tp2-point): **escalated**

### ADD-03:p4-image/tp2-location (reading_block, p4) — UNRESOLVED
- source: “غرفة التفتيش MH-07 على خط الانحدار الجنوبي”
- transition: `ADD-03/p4-image/tp2-location` disposition no_effect: This is the TP-2 location cell ('غرفة التفتيش MH-07 على خط الانحدار الجنوبي') of the Arabic Table 1-3 at Appendix A. It is table content, not an amending instr…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval; a person should confirm the term خط الانحدار ('gravity line/sewer').
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval, and the term خط الانحدار ('gravity line/sewer') needs a person to confirm it.
    - concern: No_effect covers only the absence of an old/new pair. The cell's content takes effect through the 2.1 incorporation.
  - downstream proposal `D-03` escalation (esc:ADD-03:p4-image/tp2-location): **escalated**

### ADD-03:p4-image/tp2-diameter (reading_block, p4) — UNRESOLVED
- source: “٨٠٠”
- transition: `ADD-03/p4-image/tp2-diameter` disposition no_effect: This is the TP-2 existing-sewer-diameter cell ('٨٠٠', mm) of the Arabic Table 1-3 at Appendix A. It is table content, not an amending instruction: it prints no…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: The reading of ADD-03-p4-r1 is still pending approval.
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: No_effect covers only the absence of an old/new pair. The value is operative through the 2.1 incorporation.
  - downstream proposal `D-04` escalation (esc:ADD-03:p4-image/tp2-diameter): **escalated**

### ADD-03:p4-image/tp2-window (reading_block, p4) — answered
- source: “من ٠١:٠٠ إلى ٠٥:٠٠”
- transition: `ADD-03/p4-image/tp2-window` disposition no_effect: This is a cell of the Network Operator's Table 1-3 reproduced at Appendix A, and ADD-03 issues it. It prints no change to any unit standing at ADD-02. The tabl…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The no_effect disposition rests on 2.1 incorporating the table and on I1/A1, which a person must confirm. The Arabic window text matches the English '01:00 to 05:00'.

### ADD-03:p4-image/tp2-duration (reading_block, p4) — UNRESOLVED
- source: “٤”
- transition: `ADD-03/p4-image/tp2-duration` escalation why: The two renderings conflict. The governing Arabic Table 1-3 prints '٤' (4 hours) as the TP-2 maximum shutdown duration, while the convenience English translation (ADD-03:T1-3/tp-2) prints 'Maximum sh…
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:T1-3/tp-2
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The conflict is real on the readings shown: Arabic '٤' (4) against English 'Maximum shutdown duration (hours): 6'. 2.2 gives the Arabic precedence and 2.7 makes the Table 1-3 maximum a ground for rejection.
    - concern: The proposer's own rationale says the crop named for this reading (18a85c…) does not show the duration cell. The '٤' reading is therefore not confirmed from its cited crop, and a person should check it against the page image before relying on 4 h.
    - concern: The statements cite the Arabic as governing, but they do not quote the Arabic cell itself beyond the reading. I could not verify the image.
  - downstream proposal `D-05` escalation (esc:ADD-03:p4-image/tp2-duration): **escalated**

### ADD-03:p4-image/tp2-notice (reading_block, p4) — answered
- source: “١٠ أيام عمل”
- transition: `ADD-03/p4-image/tp2-notice` disposition no_effect: This is a cell of Table 1-3 at Appendix A, and ADD-03 issues it. It prints no change to any unit standing at ADD-02. Its content enters Volume II through ADD-0…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: '١٠ أيام عمل' means 10 working days, which matches the English 'Advance notice: 10 Working Days'. The no_effect disposition rests on I1/A1, which a person must confirm.

### ADD-03:p4-image/notes-heading (reading_block, p4) — answered
- source: “ملاحظات:”
- transition: `ADD-03/p4-image/notes-heading` disposition no_effect: This is only the heading 'ملاحظات:' (Notes:) over the notes to Table 1-3. It carries no requirement and prints no change to any unit standing at ADD-02.
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5

### ADD-03:p4-image/note1 (reading_block, p4) — UNRESOLVED
- source: “١. لا يُسمح بأي إيقاف خلال شهر رمضان المبارك أو خلال إجازتَي عيد الفطر وعيد الأضحى.”
- transition: `ADD-03/p4-image/note1` escalation why: The two renderings conflict. Governing Arabic note 1 prohibits any shutdown during Ramadan and also during the Eid al-Fitr and Eid al-Adha holidays ('أو خلال إجازتَي عيد الفطر وعيد الأضحى'). English …
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:T1-3/note(1)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The conflict is real. The Arabic adds 'أو خلال إجازتَي عيد الفطر وعيد الأضحى' (or during the Eid al-Fitr and Eid al-Adha holidays), and English note (1) mentions only Ramadan. 2.2 says the Arabic governs.
    - concern: The Eid holiday dates are not in the evidence, so the prohibited periods cannot be turned into dates here.
  - downstream proposal `D-06` escalation (esc:ADD-03:p4-image/note1): **escalated**

### ADD-03:p4-image/note2 (reading_block, p4) — answered
- source: “٢. يُسمح بإيقافٍ واحدٍ فقط لكل نقطة ربط طوال مدّة الإنشاء.”
- transition: `ADD-03/p4-image/note2` disposition no_effect: The note does restrict ('يُسمح بإيقافٍ واحدٍ فقط' = only one shutdown is permitted). It is part of Table 1-3, which ADD-03 itself issues, and it prints no chan…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The Arabic matches the English note (2). The note does restrict, so the no_effect wording means only that it amends no ADD-02 unit. Its substance still takes effect through 2.1, and a person should confirm that reading.

### ADD-03:p4-image/note3 (reading_block, p4) — answered
- source: “٣. تُقدَّم طلبات الإيقاف عبر البوابة الإلكترونية للشركة، مرفقاً بها برنامج الإيقاف المقترح وخطة الطوارئ.”
- transition: `ADD-03/p4-image/note3` disposition no_effect: The note does oblige ('تُقدَّم طلبات الإيقاف' = shutdown requests shall be submitted). It is part of Table 1-3, which ADD-03 itself issues, and it prints no ch…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The Arabic matches the English note (3). 'خطة الطوارئ' is rendered 'contingency plan' and 'للشركة' as 'the Network Operator's', which are acceptable. The no_effect disposition means only that no ADD-02 unit is amended. The obligation still enters through 2.1.

### ADD-03:p4-image/note4 (reading_block, p4) — answered
- source: “٤. جميع الأوقات المذكورة بتوقيت الرياض.”
- transition: `ADD-03/p4-image/note4` disposition no_effect: This is a note to Table 1-3 at Appendix A, and ADD-03 issues it. It states the time reference ('جميع الأوقات المذكورة بتوقيت الرياض' = all times are Riyadh tim…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The Arabic matches the English '(4) All times are Riyadh time.'. The no_effect disposition rests on I1/A1, which a person must confirm.

### ADD-03:p4-image/signatory (reading_block, p4) — answered
- source: “مدير إدارة تشغيل الشبكات”
- transition: `ADD-03/p4-image/signatory` disposition no_effect: The unit is the signature block of the reproduced Network Operator letter No. 312/2026: the image prints only the title 'مدير إدارة تشغيل الشبكات' above an ill…
  - validation: **evidence_verified**

### ADD-03:p4-image/stamp (reading_block, p4) — answered
- source: “”
- transition: `ADD-03/p4-image/stamp` disposition no_effect: The image shows an empty oval stamp outline with no legible text (reading source_text is empty). Nothing is printed, so nothing is amended, obliged or excepted.
  - validation: **evidence_verified**

### ADD-03:p4-image/image-footer (reading_block, p4) — answered
- source: “FICTIONAL DOCUMENT - Lamar Holding internal assessment pack - not a real tender.”
- transition: `ADD-03/p4-image/image-footer` disposition no_effect: The image footer prints 'FICTIONAL DOCUMENT - Lamar Holding internal assessment pack - not a real tender.' It is a document-marking line, not a tender provisio…
  - validation: **evidence_verified**

### ADD-03:AppA/para2 (paragraph, p4) — answered
- source: “End of reproduction.”
- transition: `ADD-03/AppA/para2` disposition no_effect: 'End of reproduction.' only marks the end of the reproduced Table 1-3 at Appendix A; it amends, obliges or excepts nothing.
  - validation: **evidence_verified**

### ADD-03:AppB/para1 (paragraph, p5) — answered
- source: “This translation is provided for convenience only. The Arabic text of Table 1-3 at Appendix A governs. Network Operator's letter No. 312/2026 dated 5 November 2026. Subject: tie-in points with the existing collection network for the Wadi Sirhan Independent Sewage Treatment Plant. Tender No. NUPA/ISTP/2026/014.”
- transition: `ADD-03/AppB/para1` disposition no_effect: The words 'This translation is provided for convenience only. The Arabic text of Table 1-3 at Appendix A governs.' restate the precedence already printed in AD…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'provided')
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The no_effect disposition depends on interpretation S7 that ADD-03:2.2 carries the precedence. The 2.2 text is shown verbatim and says the same thing, so this follows from the evidence, but a person must confirm it. The controller's semantic check also flagged it because the paragraph contains 'pro…
    - concern: The paragraph's remaining words (letter No. 312/2026 dated 5 November 2026, subject, tender number) only identify the source. They change no requirement, so no_effect is consistent with the text shown.
    - concern: One difference in wording: 2.2 says 'The Arabic text governs'. AppB/para1 says 'The Arabic text of Table 1-3 at Appendix A governs', which names Appendix A explicitly. This is not a conflict, but the reviewer should note that Appendix A is named only here. The text of 2.2 shown does not name it.

### ADD-03:T1-3/tp-1 (table_row, p5) — answered
- source: “Tie-in point: TP-1 | Location: Manhole MH-41 on the northern rising main | Existing sewer diameter (mm): 1,000 | Permitted shutdown window: 23:00 to 05:00 | Maximum shutdown duration (hours): 6 | Advance notice: 10 Working Days”
- transition: `ADD-03/T1-3/tp-1` disposition no_effect: This row belongs to the convenience English translation at Appendix B. ADD-03:2.2 prints 'The Arabic text governs. The English translation at Appendix B is pro…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The claim that every cell matches the Arabic row rests on the proposer's reading of the crop. Only the TP-1 duration reading (٦) is printed as evidence, and it is pending.
    - concern: I4 (capitalised 'Working Days') is left open. It does not change the no_effect disposition.

### ADD-03:T1-3/tp-2 (table_row, p5) — UNRESOLVED
- source: “Tie-in point: TP-2 | Location: Manhole MH-07 on the southern gravity sewer | Existing sewer diameter (mm): 800 | Permitted shutdown window: 01:00 to 05:00 | Maximum shutdown duration (hours): 6 | Advance notice: 10 Working Days”
- transition: `ADD-03/T1-3/tp-2` escalation why: The convenience translation gives TP-2 'Maximum shutdown duration (hours): 6'. The governing Arabic Table 1-3 (Appendix A image, pending reading ADD-03:p4-image/tp2-duration) prints '٤' (4). Under AD…
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:p4-image/tp2-duration
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The conflict is real on the evidence shown: English says 6, the pending Arabic reading says ٤, and ADD-03:2.2 says the Arabic governs.
    - concern: The Arabic value depends on a pending, unapproved reading (A1). The escalation correctly lists this as missing.
    - concern: The claim that ADD-03:2.7 rejects bids on this value is not supported by any printed text. ADD-03:2.7 is not in the evidence.
    - concern: The target is the image reading, which is the right unit for the Arabic side.
- transition: `ADD-03/T1-3/tp-2/issue` issue {"text": "The Appendix B English translation gives TP-2's maximum shutdown duration as 6 hours. The governing Arabic Table 1-3 at Appendix A prints ٤ (4 hours). Under ADD-03:2.2 the Arabic governs. A…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The text says the Arabic 'prints ٤ (4 hours)' as settled fact. The reading is pending and unapproved.
    - concern: The consequence that a 6-hour programme 'would be rejected under ADD-03:2.7' cannot be checked. ADD-03:2.7 is not among the evidence printed.
    - concern: The item cites no ADD-03:2.2 evidence for 'the Arabic governs'. The discrepancy itself is plausible and should be wording-qualified (pending reading, 2.7 unverified).
  - downstream proposal `D-07` escalation (esc:ADD-03:T1-3/tp-2): **escalated**
  - downstream proposal `D-16` clarification_item (esc:ADD-03:T1-3/tp-2): **invalid**

### ADD-03:T1-3/notes (note_intro, p5) — answered
- source: “Notes to Table 1-3:”
- transition: `ADD-03/T1-3/notes` disposition no_effect: This is the lead-in heading 'Notes to Table 1-3:' of the convenience translation. It amends, obliges or excepts nothing.
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: A heading only. It says nothing that amends, obliges or excepts.

### ADD-03:T1-3/note(1) (note, p5) — UNRESOLVED
- source: “(1) No shutdown is permitted during the holy month of Ramadan.”
- transition: `ADD-03/T1-3/note(1)` escalation why: English note (1) bans shutdowns only during Ramadan. The governing Arabic note 1 (pending reading ADD-03:p4-image/note1) also bans them during the Eid al-Fitr and Eid al-Adha holidays ('أو خلال إجازت…
  - validation: **conflicting** — declared_conflicts: the proposer declares: ADD-03:p4-image/note1
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The Arabic reading includes the Eid holidays and the English omits them, so the conflict is real. It depends on a pending reading (A1).
    - concern: Eid dates are not in the pack, as the item says.
    - concern: The target is the right image unit.
- transition: `ADD-03/T1-3/note(1)/issue` issue {"text": "The English note (1) to Table 1-3 leaves out the Eid al-Fitr and Eid al-Adha holidays. The governing Arabic note bans shutdowns during Ramadan and during both Eid holidays. The shutdown pro…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The wording 'must avoid all three periods' treats the pending Arabic reading as settled. It should be qualified until a person approves the reading.
    - concern: The item cites no ADD-03:2.2 evidence for 'the Arabic governs'. The linked escalation does.
  - downstream proposal `D-08` escalation (esc:ADD-03:T1-3/note(1)): **escalated**

### ADD-03:T1-3/note(2) (note, p5) — answered
- source: “(2) Only one shutdown is permitted at each tie-in point during the construction period.”
- transition: `ADD-03/T1-3/note(2)` disposition no_effect: This note belongs to the convenience translation. ADD-03:2.2 prints 'The English translation at Appendix B is provided for convenience only.' The binding limit…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The claim that Arabic note 2 matches rests only on the proposer's rationale. No Arabic reading unit for note 2 is printed.
    - concern: The no_effect reasoning (2.2 and 2.1) follows from the cited text, but a person should confirm it.

### ADD-03:T1-3/note(3) (note, p5) — answered
- source: “(3) Shutdown requests shall be submitted through the Network Operator's electronic portal, accompanied by the proposed shutdown programme and a contingency plan.”
- transition: `ADD-03/T1-3/note(3)` disposition no_effect: The words 'shall be submitted' are in the convenience translation, and ADD-03:2.2 prints 'The English translation at Appendix B is provided for convenience onl…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'shall')
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The text carries 'shall', and the controller flagged this for a person. no_effect is defensible only because the binding text is Arabic note 3 via 2.1 and 2.2.
    - concern: The match with Arabic note 3 is not shown in the printed evidence, only in the proposer's rationale. The item says a person should confirm this.

### ADD-03:T1-3/note(4) (note, p5) — answered
- source: “(4) All times are Riyadh time.”
- transition: `ADD-03/T1-3/note(4)` disposition no_effect: This note belongs to the convenience translation (ADD-03:2.2: 'The English translation at Appendix B is provided for convenience only.') and matches Arabic not…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The match with Arabic note 4 is asserted from the crop and not shown in the printed evidence.
    - concern: The item lists only the note itself as evidence. ADD-03:2.2 appears only in the statements.

### ADD-03:AppB/para2 (paragraph, p5) — answered
- source: “Signed: Director, Network Operations, Northern Region Water Services Company (signature and company stamp).”
- transition: `ADD-03/AppB/para2` disposition no_effect: This is the translated signature block of the Network Operator's letter. It amends, obliges or excepts nothing.
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The text is a signature block and creates no obligation or amendment. No concern with no_effect.

## Downstream proposals (validated in the candidate)

| Item | Type | Task | Status | First failed check, or what a person confirms |
|---|---|---|---|---|
| DS-ADD03-VOL-II-1.3-01 | row_reading | row:VOL-II-1.3-01 | insufficient_evidence | missing_information: the proposer declares missing: An approved reading of Table 1-3 (ADD-03 Appendix A image) |
| DS-ADD03-DEP-1.3-T13 | dependency | row:VOL-II-1.3-01 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| DS-ADD03-VOL-II-3.3-01 | row_reading | row:VOL-II-3.3-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-VOL-II-7.2-01 | row_reading | row:VOL-II-7.2-01 | insufficient_evidence | replace_requirement: replace_requirement.old is not the row's requirement (or new is empty) |
| DS-ADD03-VOL-II-8.1-01 | row_reading | row:VOL-II-8.1-01 | insufficient_evidence | replace_requirement: replace_requirement.old is not the row's requirement (or new is empty) |
| DS-ADD03-VOL-II-8.2-01 | escalation | row:VOL-II-8.2-01 | escalated |  |
| DS-ADD03-VOL-II-8.3-01 | row_reading | row:VOL-II-8.3-01 | insufficient_evidence | replace_requirement: replace_requirement.old is not the row's requirement (or new is empty) |
| DS-ADD03-VOL-II-8.3-02 | row_reading | row:VOL-II-8.3-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-VOL-II-8.4-01 | row_reading | row:VOL-II-8.4-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-VOL-II-8.4-02 | row_reading | row:VOL-II-8.4-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-VOL-II-8.5-01 | row_reading | row:VOL-II-8.5-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-VOL-II-8.5-02 | row_reading | row:VOL-II-8.5-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-VOL-V-31.1-01 | row_reading | row:VOL-V-31.1-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-01 | row_reading | row:VOL-V-31.1-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-02 | row_reading | row:VOL-V-31.1-03 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-03 | row_reading | row:VOL-V-31.3-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-04 | row_reading | row:VOL-V-31.3-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-05 | row_reading | row:VOL-V-31.3-03 | insufficient_evidence | missing_information: the proposer declares missing: post_award_evidence.basis of VOL-V-31.3-03 quotes 'No cure period applies to an event under Clause 31.1(b).', which is not verbatim at ADD-03 |
| DS-06 | row_new | c46:ADD-03/cover/para3 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words decides which clause governs ('governs') |
| DS-07 | issue | c46:ADD-03/cover/para3 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words declares a matter resol… |
| DS-08 | clarification_item | c46:ADD-03/cover/para3 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words decides which clause governs ('governs') |
| DS-09 | clarification_item | clar:CQ-VOL-III-DRAWINGS | insufficient_evidence — HUMAN DECISION PENDING | clarify.check: CQ-VOL-III-DRAWINGS: not verbatim in VOL-II:1.3: 'The two designated tie-in points are TP-1 and TP-2, described in Table 1-3' |
| DS-10 | clarification_item | clar:CQ-PERSISTENT-BREACH | insufficient_evidence — HUMAN DECISION PENDING | clarify.check: CQ-PERSISTENT-BREACH: not verbatim in VOL-V:31.1: '(d) the volume of treated effluent delivered to the delivery point on any day is' |
| DS-11 | clarification_item | clar:CQ-PCOD-RELIABILITY-RUN | insufficient_evidence — HUMAN DECISION PENDING | clarify.check: CQ-PCOD-RELIABILITY-RUN: not verbatim in VOL-II:7.2: 'PCOD shall not be certified until the Facility has completed a continuous reliab' |
| DS-12 | activity | act:technical-proposal | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| DS-13 | escalation | esc:ADD-03:2.2 | conflicting | declared_conflicts: the proposer declares: ADD-03:T1-3/tp-2; ADD-03:T1-3/note(1) |
| DS-14 | issue | esc:ADD-03:2.2 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words decides which clause go… |
| DS-15 | row_new | esc:ADD-03:2.3 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-16 | escalation | esc:ADD-03:2.3 | escalated | missing_information: the proposer declares missing: approval of the Arabic Table 1-3 reading (ADD-03-p4-r1); a stated consequence for failing to state the election |
| ADD-03-DS-ESC-2.4 | escalation | esc:ADD-03:2.4 | escalated | missing_information: the proposer declares missing: maximum transfer flow per tie-in point (absent from Table 1-3) |
| ADD-03-DS-ISSUE-2.4 | issue | esc:ADD-03:2.4 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| ADD-03-DS-CQ-2.4 | clarification_item | esc:ADD-03:Q20 | evidence_verified |  |
| ADD-03-DS-ESC-Q20 | escalation | esc:ADD-03:Q20 | escalated | missing_information: the proposer declares missing: maximum transfer flow per tie-in point |
| ADD-03-DS-ESC-2.5 | escalation | esc:ADD-03:2.5 | escalated |  |
| ADD-03-DS-ESC-2.6 | escalation | esc:ADD-03:2.6 | escalated |  |
| ADD-03-DS-ESC-2.7 | escalation | esc:ADD-03:2.7 | conflicting | declared_conflicts: the proposer declares: ADD-03:T1-3/tp-2 |
| ADD-03-DS-ESC-Q17 | escalation | esc:ADD-03:Q17 | escalated | missing_information: the proposer declares missing: amended text of VOL-V Clause 12.3 |
| ADD-03-DS-ESC-Q18 | escalation | esc:ADD-03:Q18 | escalated | missing_information: the proposer declares missing: whether network inflow shortfall falls within VOL-V 34.2 |
| ADD-03-DS-ESC-Q19 | escalation | esc:ADD-03:Q19 | conflicting | declared_conflicts: the proposer declares: VOL-II:7.4; VOL-II:8.2 |
| ADD-03-DS-ESC-P4-LOC | escalation | esc:ADD-03:p4-image/tp1-location | escalated | missing_information: the proposer declares missing: approval of reading ADD-03-p4-r1 |
| ADD-03-DS-ESC-P4-DIA | escalation | esc:ADD-03:p4-image/tp1-diameter | escalated | missing_information: the proposer declares missing: approval of reading ADD-03-p4-r1 |
| ADD-03-DS-ESC-P4-WIN | escalation | esc:ADD-03:p4-image/tp1-window | escalated | missing_information: the proposer declares missing: approval of reading ADD-03-p4-r1 |
| ADD-03-DS-ESC-P4-DUR | escalation | esc:ADD-03:p4-image/tp1-duration | escalated | missing_information: the proposer declares missing: approval of reading ADD-03-p4-r1 |
| D-01 | escalation | esc:ADD-03:p4-image/tp1-notice | escalated |  |
| D-02 | escalation | esc:ADD-03:p4-image/tp2-point | escalated |  |
| D-03 | escalation | esc:ADD-03:p4-image/tp2-location | escalated | statements: fact downstream-004/S-TP2-LOC is not supported verbatim |
| D-04 | escalation | esc:ADD-03:p4-image/tp2-diameter | escalated |  |
| D-05 | escalation | esc:ADD-03:p4-image/tp2-duration | escalated | statements: fact downstream-004/S-TP2-EN is not supported verbatim |
| D-06 | escalation | esc:ADD-03:p4-image/note1 | escalated |  |
| D-07 | escalation | esc:ADD-03:T1-3/tp-2 | escalated | statements: fact downstream-004/S-TP2-EN is not supported verbatim |
| D-08 | escalation | esc:ADD-03:T1-3/note(1) | escalated |  |
| D-09 | row_new | reading:ADD-03-p4-r1 | invalid | provision: ADD-03:p4-image is not a provision of ADD-03 |
| D-10 | row_new | reading:ADD-03-p4-r1 | invalid | provision: ADD-03:p4-image is not a provision of ADD-03 |
| D-11 | row_new | reading:ADD-03-p4-r1 | invalid | provision: ADD-03:p4-image is not a provision of ADD-03 |
| D-12 | row_new | reading:ADD-03-p4-r1 | invalid | provision: ADD-03:p4-image is not a provision of ADD-03 |
| D-13 | row_new | reading:ADD-03-p4-r1 | invalid | provision: ADD-03:p4-image is not a provision of ADD-03 |
| D-14 | row_new | reading:ADD-03-p4-r1 | invalid | provision: ADD-03:p4-image is not a provision of ADD-03 |
| D-15 | issue | reading:ADD-03-p4-r1 | invalid — HUMAN DECISION PENDING | provision: ADD-03:p4-image is not a provision of ADD-03 |
| D-16 | clarification_item | esc:ADD-03:T1-3/tp-2 | invalid | statements: fact downstream-004/S-TP2-EN is not supported verbatim |
| D-17 | row_new | date:ADD-03:2.5 | invalid | register: the row does not evaluate: ValueError: rule ADD-03-2.5-sal-application: kind 'deadline' not in ('anchor', 'relative', 'fixed', 'as_at', 'external', 'unresolved') |
| D-18 | evidence_item | date:ADD-03:2.5 | insufficient_evidence | held back: no promotable row or activity uses EV-SHUTDOWN-ACCEPTANCE |
| D-19 | activity | date:ADD-03:2.5 | invalid | computed_from: computed_from matches no deadline the program computed for ADD-03 (its fingerprint; computed: ADD-03:2.5 2026-11-16) |
| D-20 | escalation | cons:VOL-II:7.2 | escalated |  |
| D-21 | escalation | cons:ADD-03:3.1 | escalated |  |

- interactions: A5 with the proposals: C45: the programme cannot be planned with the proposals: ValueError: rule ADD-03-2.5-sal-application: kind 'deadline' not in ('anchor', 'relative', 'fixed', 'as_at', 'external'…
- A5 problems the proposals would add: C45: the programme cannot be planned with the proposals: ValueError: rule ADD-03-2.5-sal-application: kind 'deadline' not in ('anchor', 'relative', 'fixed', 'as_at', 'external', 'unresolved')

## Promoted into the candidate (PROPOSED; nothing accepted)

- ops: ADD-03/cover/para3, ADD-03/2.1, ADD-03/3.1, ADD-03/3.2(b), ADD-03/4.1(a), ADD-03/4.1(b), ADD-03/4.1(c), ADD-03/4.2, ADD-03/5.1, ADD-03/5.2, ADD-03/Q16
- dispositions: ADD-03:cover/para1: no_effect, ADD-03:cover/para2: no_effect, ADD-03:1.1: no_effect, ADD-03:1.2: no_effect, ADD-03:Q15: no_effect, ADD-03:AppA/para1: no_effect, ADD-03:p4-image/hdr-en: no_effect, ADD-03:p4-image/hdr-ar: no_effect, ADD-03:p4-image/ref: no_effect, ADD-03:p4-image/date: no_effect, ADD-03:p4-image/subject: no_effect, ADD-03:p4-image/tender-ref: no_effect, ADD-03:p4-image/table-title: no_effect, ADD-03:p4-image/intro: no_effect, ADD-03:p4-image/th-point: no_effect, ADD-03:p4-image/th-location: no_effect, ADD-03:p4-image/th-diameter: no_effect, ADD-03:p4-image/th-window: no_effect, ADD-03:p4-image/th-duration: no_effect, ADD-03:p4-image/th-notice: no_effect, ADD-03:p4-image/table-rule: no_effect, ADD-03:p4-image/tp1-point: no_effect, ADD-03:p4-image/tp2-window: no_effect, ADD-03:p4-image/tp2-notice: no_effect, ADD-03:p4-image/notes-heading: no_effect, ADD-03:p4-image/note2: no_effect, ADD-03:p4-image/note3: no_effect, ADD-03:p4-image/note4: no_effect, ADD-03:p4-image/signatory: no_effect, ADD-03:p4-image/stamp: no_effect, ADD-03:p4-image/image-footer: no_effect, ADD-03:AppA/para2: no_effect, ADD-03:AppB/para1: no_effect, ADD-03:T1-3/tp-1: no_effect, ADD-03:T1-3/notes: no_effect, ADD-03:T1-3/note(2): no_effect, ADD-03:T1-3/note(3): no_effect, ADD-03:T1-3/note(4): no_effect, ADD-03:AppB/para2: no_effect
- rows new: ADD-03-cover-para3-01, ADD-03-2.3-01
- readings: VOL-II-3.3-01, VOL-II-8.3-02, VOL-II-8.4-01, VOL-II-8.4-02, VOL-II-8.5-01, VOL-II-8.5-02, VOL-V-31.1-01, VOL-V-31.1-02, VOL-V-31.1-03, VOL-V-31.3-01, VOL-V-31.3-02
- issues: I-ADD-03-COVER-01, I-ADD03-SUMMARY-VS-OPERATIVE, I-ADD03-T13-ARABIC-ENGLISH, I-ADD03-TRANSFER-FLOW
- activities: technical-proposal
- clarifications: CQ-ADD03-SUMMARY-DISCREPANCY, CQ-ADD03-TRANSFER-FLOW
- relationships: REL-AI-001
- unresolved provisions: 22

## check-register on the candidate

- exit 1; 1 finding(s) {'C46': 1}
  - [C46] ADD-03/cover/para3: [A3] ADD-03/cover/para3 brings in consequence words ['deduction'] that no row's consequence carries at ADD-03: 'This Addendum incorporates the Network Operator's Table 1-3 describing the two tie-in p…

## Coverage

- provisions: 70; accounted for by the combined set: 70; states {'validated': 70}
- resolution (controller): resolved 14, pending 56, invalid 0, unaccounted 0; approved 0
- structural units of ADD-03 that are not provisions (listed so nothing is dropped): ADD-03:H:cover (heading), ADD-03:H:cover-2 (heading), ADD-03:H:S1 (heading), ADD-03:H:S2 (heading), ADD-03:H:S3 (heading), ADD-03:H:S4 (heading), ADD-03:H:S5 (heading), ADD-03:H:S6 (heading), ADD-03:S6/QA (table), ADD-03:H:AppA (heading), ADD-03:region:ADD-03-p4-r1 (region), ADD-03:p4-image (image_text), ADD-03:H:AppB (heading), ADD-03:T1-3 (table)
- batches: reading-ADD-03-p4-r1 done, analysis-001 done, analysis-002 done, analysis-003 done, analysis-004 done, analysis-005 done, analysis-006 done, analysis-007 done, analysis-008 done, analysis-009 done, analysis-010 done, downstream-001 done, downstream-002 done, downstream-003 done, downstream-004 done

## Critic (a second model over the selected items; it changed no status)

**Agreement between the critic and the proposer is not approval**: every item still needs a person's decision, and a disagreement is a concern for that person, not a rejection. The critic reviews only the selected classes (consequential interpretations, uncertain targets, removals, conflicting evidence), in one request per batch.

| Batch | Critic | Selected | Reviewed | Agrees | Does not agree | Note |
|---|---|---|---|---|---|---|
| analysis-001 | done | 4 | 4 | 3 | 1 |  |
| analysis-002 | done | 7 | 7 | 7 | 0 |  |
| analysis-003 | done | 5 | 5 | 5 | 0 |  |
| analysis-004 | done | 5 | 5 | 2 | 3 |  |
| analysis-005 | done | 8 | 8 | 8 | 0 |  |
| analysis-006 | done | 9 | 9 | 9 | 0 |  |
| analysis-007 | done | 8 | 8 | 7 | 1 |  |
| analysis-008 | done | 8 | 8 | 8 | 0 |  |
| analysis-009 | done | 1 | 1 | 1 | 0 |  |
| analysis-010 | done | 10 | 10 | 9 | 1 |  |
| downstream-001 | done | 2 | 2 | 1 | 1 |  |
| downstream-002 | done | 5 | 5 | 5 | 0 |  |
| downstream-003 | done | 2 | 2 | 1 | 1 |  |
| downstream-004 | not_needed | 0 | - | - | - |  |

- **ADD-03/cover/para3** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The cover paragraph is both the provision and the target, which is why the target is flagged as uncertain. This is acceptable for an annotate op, because the only obligation of its own is the Form 4-A acknowledgement. The other listed changes are not made by this paragraph, and the note says so.
    - concern: The adds_obligation effect is an interpretation. A person should confirm it.
- **ADD-03/cover/para3/issue-shutdown** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The conflict is real on the quoted words. The cover says the Authority's acceptance, with applications within 8 Working Days of the date of the Addendum. Clause 2.5 says a Network Operator letter, with applications at least 8 Working Days before the Proposal Due Date.
    - concern: The payload says 'forward from 10 November 2026'. That date is not in the evidence shown, so it is unverified.
    - concern: The item does not say which provision governs. The cover says the Addendum takes precedence under Vol I 3.2, but that does not settle a cover-versus-operative conflict. Leaving it to the person is correct.
- **ADD-03/cover/para3/issue-rampup** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The cover does say 'no deduction during the Ramp-Up Period'. ADD-03:5.1 as shown adds event (d) with no Ramp-Up wording. This part is supported.
    - concern: The claim that a search of all of ADD-03 found no Ramp-Up exclusion cannot be verified. Only units 5.1 and 5.2 (partial) and the cover are shown.
    - concern: The statement that VOL-V 29.3 covers Table 2-4 parameters only is not supported by any text in the evidence. VOL-V 29.3 is not printed.
    - concern: Without the full ADD-03 text and VOL-V 29.3, the evidence does not show that no Ramp-Up exclusion is in force. The issue may still be worth raising, but its stated basis is not shown.
- **ADD-03/1.2** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: no_effect is right in that Clause 1.2 amends no unit. It does fix the stage at which cross-references are read, as amended by Addenda 1 and 2. That is consistent with the ADD-02 stage used here.
    - concern: 'Unless otherwise stated' could be triggered by a later provision. The person should confirm that no ADD-03 clause states a different reading.
- **ADD-03/2.2** (analysis-002; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The Arabic values (TP-2 duration ٤, Arabic note 1 with the Eid holidays) rest on pending reading blocks and a crop I cannot see. I could only check the text of 2.2, the image caption and AppB/para1.
    - concern: The precedence is stated for Table 1-3 as a whole. The item treats ADD-03:p4-image as the governing unit and ADD-03:T1-3 as the convenience translation. That follows from 2.2 and AppB/para1, but a person should confirm it.
    - concern: The target is T1-3, the English table, while the governing unit is the image. This is a deliberate group target, not a unit that 2.2 names.
- **ADD-03/2.3** (analysis-002; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: 2.3 cites 'Table 1-3' without naming a unit. Choosing the Arabic image as the target, with the English table as a second target, is an inference that depends on 2.2.
    - concern: The note says both windows agree with English Appendix B. Only the English TP-2 row (01:00 to 05:00) is shown, so the TP-1 window cannot be checked here.
    - concern: The Arabic window readings are pending, and the item itself lists the A1 register row as missing.
    - concern: I2 and the claim that 2.3 does not change VOL-II:1.3 are not supported by any evidence shown.
- **ADD-03/2.4** (analysis-002; controller status **escalated**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The English header row shown has no flow column, which supports the claim. The claim for the Arabic table and for the notes relies on the proposer's own viewing of the image. Only the Arabic duration header is quoted.
    - concern: The English notes are not printed in full in the evidence, so 'no note states a flow' cannot be fully verified here.
    - concern: Escalation is reasonable. An annotate or a derived flow would be unsupported.
- **ADD-03/2.4-clarification** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The practical_impact says method (a) is the default under 2.6. ADD-03:2.6 is not in the evidence shown, so that statement is unsupported here.
    - concern: The proposed question cites Q20, but this item's own evidence lists only 2.4.
- **ADD-03/2.5** (analysis-002; controller status **escalated**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The 2026-11-16 deadline depends on assumption A2: PDD 2026-11-26 and a Sunday to Thursday working week. The PDD and calendar are not shown. Counting back eight working days on that basis does give 16 November.
    - concern: The Arabic note 3 reading says 'للشركة' (the company's portal). The item equates this with the Network Operator's portal, which is not established by the words quoted.
    - concern: The cover/clause discrepancy is real in the quoted text (Authority versus Network Operator; within 8 WD of the Addendum date versus 8 WD before the PDD). The cover is non-operative and the item says so.
- **ADD-03/2.7** (analysis-002; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The 4 h versus 6 h conflict for TP-2 depends on a pending Arabic reading of one digit that I cannot verify. Interpretation I1 is pending.
    - concern: 2.7 says 'Table 1-3' without naming a unit. Choosing the Arabic image as target follows from 2.2 but is an inference.
    - concern: The A1/A3 register rows are missing, as the item itself declares.
    - concern: The rejection consequence follows from 2.7's words. A bid relying on 6 h for TP-2 would be rejected only if the Arabic ٤ is confirmed.
- **ADD-03/2.7-issue** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The statement 'Shutdown programmes must follow the Arabic' is a conclusion that depends on pending interpretation I1 and on the pending Arabic reading.
    - concern: The Eid point rests on the quoted Arabic note 1 reading and on the English note, which is only partly shown. It is not in this item's own evidence list.
    - concern: The target T1-3/tp-2 is the English row, while the governing value is in the Arabic image.
- **ADD-03/3.2(a)** (analysis-003; controller status **escalated**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Escalation is reasonable: 3.2 does not cite 7.2 by number; 'that range' and 'the thirty (30) days' refer back to 3.1, whose text is not shown here, so the link to 7.2 is an inference (S-I1).
    - concern: Interaction of 'shall not count' with 'continuous' in 7.2 is genuinely unresolved on the evidence; 3.2 itself says only 7.3 is unchanged and is silent on 7.2's continuity wording.
    - concern: The mention of Q18/Volume V Clause 34 is not in the printed evidence; I did not rely on it.
- **ADD-03/4.1(a)** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
    - concern: The new 8.1 text matches the quoted replacement minus the '8.1' label; the old text matches VOL-II:8.1 exactly.
    - concern: The new text adds a reference to Clause 7.4's asset register. Clause 7.4 is not shown in the evidence, so the claim that it is due 60 days after PCOD cannot be verified here.
    - concern: The change goes beyond a quantity change (2 years to 18 months), since it also adds a recording obligation. A person should note that.
- **ADD-03/4.1(b)** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because removal; model claude-sonnet-5-5
    - concern: The reading is plausible: 8.2 lies in the range '8.1 to 8.3' that is deleted. Replacement text is printed only for 8.1 and 8.3, and 4.2 says there is no renumbering.
    - concern: It is still an inference that the Authority meant to drop the CMMS obligation. The clause could be an omission, so a clarification question is warranted; the item itself flags this.
    - concern: 4.2 does not list 8.2 as unchanged, which is consistent with deletion.
- **ADD-03/4.1(c)** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
    - concern: The old text matches VOL-II:8.3 and the new text matches the quoted replacement for 8.3.
    - concern: The change adds substantive requirements: a degree, ten years' experience, and naming the manager in the Technical Proposal with a CV appendix. The two-operator requirement is retained unchanged.
- **ADD-03/4.2** (analysis-003; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: The target field names only 8.4, but the payload annotates 8.4 and 8.5. VOL-II:8.5 is not shown in the evidence, so I could not check it directly. 4.2 does state that 8.5 is unchanged.
    - concern: The 'not renumbered' sentence is not annotated on any unit. It is only referenced in the note.
- **ADD-03/Q17** (analysis-004; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The response says 'amended accordingly' but prints no wording, so the annotation records substance only; a person may need to draft the clause text.
    - concern: 'Other costs stay shared equally' is an inference. It is implied by 'attributable to any reliability run after the first' but is not stated.
    - concern: Dependency on VOL-II:7.2 is not backed by any quoted text.
- **ADD-03/Q18** (analysis-004; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The note says relief is subject to notice within five Working Days under VOL-V 34.3. No text of 34.3 is in the evidence, so that detail is unsupported.
    - concern: The 34.1 text (extension of time, no compensation) appears only in the statement evidence, not in the item's own evidence list.
    - concern: Whether a network inflow shortfall falls under 'failure of a utility not caused by the Project Company' is open. The item correctly flags this, but the 'interprets' effect rests on an unconfirmed interpretation.
    - concern: The response makes no amendment. The annotation is reasonable as a record, but the consequence detail goes beyond the evidence.
- **ADD-03/Q19** (analysis-004; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
    - concern: The conflict is real on the words. VOL-II 7.4 requires the register not later than 60 days after PCOD. Q19 requires submission before the start of the 7.2 run, and 7.2 says PCOD is not certified until the run is complete, so the run precedes PCOD.
    - concern: It is unclear whether a Q&A response has the power to amend 7.4. A person must decide which governs.
    - concern: The format is issued only to the Preferred Bidder, which makes pre-run submission harder to price at bid stage. This is context, not a conflict.
- **ADD-03/Q20-clar** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The English translation of Table 1-3 lacks a transfer flow column, and that is verifiable. But the Arabic text governs, and the claim that the Arabic has no such column rests only on the proposer's own reading of the image, which is still pending.
    - concern: The interim handling cites existing 1,000 mm and 800 mm sewers and TP-1/TP-2. These figures are not in the evidence shown.
    - concern: Q20 refers to Table 1-3 'at Appendix A', but the English table checked is the Appendix B translation (T1-3, p5). The target is plausible but its link to the cited provision is indirect.
- **ADD-03/AppA/para1-issue** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The Arabic observations (TP-2 duration ٤ against 6, and the Eid holidays in note 1) cannot be checked from the evidence shown. Only the image crop hash and the proposer's own description are given.
    - concern: Only the English side is verified: TP-2 reads 6 and note (1) mentions Ramadan only. The mismatch itself is unconfirmed.
    - concern: The target T1-3 is the English translation. The governing Arabic unit is ADD-03:p4-image, so the target may not be the right unit for an issue about the Arabic text.
    - concern: The precedence point is supported by AppA/para1 and 2.2, so the issue is worth raising once the reading is approved.
- **ADD-03/p4-image/hdr-en** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Crop image not shown to me; I checked only the printed reading text. ADD-03:2.1 words support the incorporation claim.
- **ADD-03/p4-image/hdr-ar** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Crop not visible; judged on the reading text only.
- **ADD-03/p4-image/ref** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Crop not visible; the digits ٣١٢/٢٠٢٦ rely on the reading as printed. The reference number alone carries no change.
- **ADD-03/p4-image/date** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The text is only a letter date, with no deadline wording, so no_effect follows. Crop not visible.
- **ADD-03/p4-image/subject** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Descriptive subject line only; crop not visible.
- **ADD-03/p4-image/tender-ref** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Whether this tender number matches the tender's own reference is not in the evidence shown, so I could not check it. It is an identifier and changes nothing.
- **ADD-03/p4-image/table-title** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Caption only; the rows and notes are other units and were not shown to me.
- **ADD-03/p4-image/intro** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The sentence uses the verb 'تُحدِّد' (specifies) and refers to flow-stopping conditions, but it only introduces the table with 'على النحو الآتي:'. It states no condition itself. That the substance sits in the table rows is not checkable from the units shown.
- **ADD-03/p4-th-point** (analysis-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is still pending human confirmation. The no_effect conclusion rests on S4, which is an interpretation. The effect of the table is left to 2.1 and other batches.
- **ADD-03/p4-th-location** (analysis-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending confirmation. The conclusion depends on S4 and on 2.1 being answered elsewhere.
- **ADD-03/p4-th-diameter** (analysis-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending confirmation. The conclusion depends on S4.
- **ADD-03/p4-th-window** (analysis-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending confirmation. The conclusion depends on S4.
- **ADD-03/p4-th-duration** (analysis-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending confirmation. The reason refers to ADD-03:2.7 as a rejection rule, but 2.7's text is not shown in the evidence, so that remark cannot be checked here. It does not affect no_effect for the heading itself.
- **ADD-03/p4-th-notice** (analysis-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending confirmation. The conclusion depends on S4.
- **ADD-03/p4-table-rule** (analysis-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The evidence is a crop with an empty reading. A person should glance at the crop to confirm that it shows only a rule and no text.
- **ADD-03/p4-tp1-point** (analysis-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The quoted 2.1 span 'The two designated tie-in points are TP-1 and TP-2' is reported as verbatim by the controller. The 2.1 text is not printed in the units, so I could not check it myself. The reading is pending confirmation.
- **ADD-03/p4-issue-transfer-flow** (analysis-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The unit list shows six heading cells (point, location, diameter, window, duration, notice) and none is a flow column. This supports the claim about the heading row. The readings are still pending.
    - concern: The evidence quotes only two of the six headings directly. The others are in S3 and in the units.
    - concern: The statement that the flow is 'not stated anywhere in the table' goes beyond the heading row. Body rows, notes or other text on page 4 are not shown. A flow could in principle appear outside a column, so a person should check the full page.
    - concern: The target 2.4 is not among the units cited by the provision (the th-point heading). The link is only the inconsistency between the heading row and 2.4.
    - concern: Q20 is named in the payload and dependencies, but no Q20 text is in the evidence. S2 (2.2, Arabic governs) is also quoted but its unit is not printed. I could not check either.
- **ADD-03/p4-image/tp1-location** (analysis-007; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading ADD-03-p4-r1 is still pending approval, and the term خط الطرد ('rising main') needs a person to confirm it.
    - concern: No_effect applies to the cell as an amending instruction only. The cell's content takes effect through the ADD-03:2.1 op, which is outside this batch.
- **ADD-03/p4-image/tp1-diameter** (analysis-007; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: No_effect covers only the absence of an old/new pair. The value is operative through the 2.1 incorporation.
- **ADD-03/p4-image/tp1-window** (analysis-007; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: No_effect covers only the absence of an old/new pair. The value is operative through the 2.1 incorporation.
- **ADD-03/p4-image/tp1-duration** (analysis-007; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The rationale says the cell is not visible in crop b08-right. It says the reading came from b08-left and the full region image.
    - concern: The evidence cites crop_sha256 7058ab6d…, the same hash as tp1-location, tp1-diameter and tp1-window. The tp1-notice item, which the rationale places in b08-left, cites a different hash. So the cited crop may not show the cell, and the evidence shown cannot confirm the '٦' reading against it.
    - concern: The reading is pending approval.
    - concern: The no_effect disposition itself is consistent with the text, but the reading's provenance needs a person to check it.
- **ADD-03/p4-image/tp1-notice** (analysis-007; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: No_effect covers only the absence of an old/new pair. The value is operative through the 2.1 incorporation.
- **ADD-03/p4-image/tp2-point** (analysis-007; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: S-F4 flags an Arabic/English mismatch for the TP-2 duration (٤ in the Arabic, 6 in the English). That conflict belongs to the tp2-duration and T1-3/tp-2 items, not to this identifier cell. It should not be dropped when those items are reviewed.
- **ADD-03/p4-image/tp2-location** (analysis-007; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval, and the term خط الانحدار ('gravity line/sewer') needs a person to confirm it.
    - concern: No_effect covers only the absence of an old/new pair. The cell's content takes effect through the 2.1 incorporation.
- **ADD-03/p4-image/tp2-diameter** (analysis-007; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The reading is pending approval.
    - concern: No_effect covers only the absence of an old/new pair. The value is operative through the 2.1 incorporation.
- **ADD-03/p4-image/tp2-window** (analysis-008; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The no_effect disposition rests on 2.1 incorporating the table and on I1/A1, which a person must confirm. The Arabic window text matches the English '01:00 to 05:00'.
- **ADD-03/p4-image/tp2-duration** (analysis-008; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The conflict is real on the readings shown: Arabic '٤' (4) against English 'Maximum shutdown duration (hours): 6'. 2.2 gives the Arabic precedence and 2.7 makes the Table 1-3 maximum a ground for rejection.
    - concern: The proposer's own rationale says the crop named for this reading (18a85c…) does not show the duration cell. The '٤' reading is therefore not confirmed from its cited crop, and a person should check it against the page image before relying on 4 h.
    - concern: The statements cite the Arabic as governing, but they do not quote the Arabic cell itself beyond the reading. I could not verify the image.
- **ADD-03/p4-image/tp2-notice** (analysis-008; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: '١٠ أيام عمل' means 10 working days, which matches the English 'Advance notice: 10 Working Days'. The no_effect disposition rests on I1/A1, which a person must confirm.
- **ADD-03/p4-image/notes-heading** (analysis-008; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
- **ADD-03/p4-image/note1** (analysis-008; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The conflict is real. The Arabic adds 'أو خلال إجازتَي عيد الفطر وعيد الأضحى' (or during the Eid al-Fitr and Eid al-Adha holidays), and English note (1) mentions only Ramadan. 2.2 says the Arabic governs.
    - concern: The Eid holiday dates are not in the evidence, so the prohibited periods cannot be turned into dates here.
- **ADD-03/p4-image/note2** (analysis-008; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The Arabic matches the English note (2). The note does restrict, so the no_effect wording means only that it amends no ADD-02 unit. Its substance still takes effect through 2.1, and a person should confirm that reading.
- **ADD-03/p4-image/note3** (analysis-008; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The Arabic matches the English note (3). 'خطة الطوارئ' is rendered 'contingency plan' and 'للشركة' as 'the Network Operator's', which are acceptable. The no_effect disposition means only that no ADD-02 unit is amended. The obligation still enters through 2.1.
- **ADD-03/p4-image/note4** (analysis-008; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The Arabic matches the English '(4) All times are Riyadh time.'. The no_effect disposition rests on I1/A1, which a person must confirm.
- **ADD-03/AppB/para1** (analysis-009; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The no_effect disposition depends on interpretation S7 that ADD-03:2.2 carries the precedence. The 2.2 text is shown verbatim and says the same thing, so this follows from the evidence, but a person must confirm it. The controller's semantic check also flagged it because the paragraph contains 'pro…
    - concern: The paragraph's remaining words (letter No. 312/2026 dated 5 November 2026, subject, tender number) only identify the source. They change no requirement, so no_effect is consistent with the text shown.
    - concern: One difference in wording: 2.2 says 'The Arabic text governs'. AppB/para1 says 'The Arabic text of Table 1-3 at Appendix A governs', which names Appendix A explicitly. This is not a conflict, but the reviewer should note that Appendix A is named only here. The text of 2.2 shown does not name it.
- **ADD-03/T1-3/tp-1** (analysis-010; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The claim that every cell matches the Arabic row rests on the proposer's reading of the crop. Only the TP-1 duration reading (٦) is printed as evidence, and it is pending.
    - concern: I4 (capitalised 'Working Days') is left open. It does not change the no_effect disposition.
- **ADD-03/T1-3/tp-2** (analysis-010; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The conflict is real on the evidence shown: English says 6, the pending Arabic reading says ٤, and ADD-03:2.2 says the Arabic governs.
    - concern: The Arabic value depends on a pending, unapproved reading (A1). The escalation correctly lists this as missing.
    - concern: The claim that ADD-03:2.7 rejects bids on this value is not supported by any printed text. ADD-03:2.7 is not in the evidence.
    - concern: The target is the image reading, which is the right unit for the Arabic side.
- **ADD-03/T1-3/tp-2/issue** (analysis-010; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The text says the Arabic 'prints ٤ (4 hours)' as settled fact. The reading is pending and unapproved.
    - concern: The consequence that a 6-hour programme 'would be rejected under ADD-03:2.7' cannot be checked. ADD-03:2.7 is not among the evidence printed.
    - concern: The item cites no ADD-03:2.2 evidence for 'the Arabic governs'. The discrepancy itself is plausible and should be wording-qualified (pending reading, 2.7 unverified).
- **ADD-03/T1-3/notes** (analysis-010; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: A heading only. It says nothing that amends, obliges or excepts.
- **ADD-03/T1-3/note(1)** (analysis-010; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The Arabic reading includes the Eid holidays and the English omits them, so the conflict is real. It depends on a pending reading (A1).
    - concern: Eid dates are not in the pack, as the item says.
    - concern: The target is the right image unit.
- **ADD-03/T1-3/note(1)/issue** (analysis-010; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The wording 'must avoid all three periods' treats the pending Arabic reading as settled. It should be qualified until a person approves the reading.
    - concern: The item cites no ADD-03:2.2 evidence for 'the Arabic governs'. The linked escalation does.
- **ADD-03/T1-3/note(2)** (analysis-010; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The claim that Arabic note 2 matches rests only on the proposer's rationale. No Arabic reading unit for note 2 is printed.
    - concern: The no_effect reasoning (2.2 and 2.1) follows from the cited text, but a person should confirm it.
- **ADD-03/T1-3/note(3)** (analysis-010; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The text carries 'shall', and the controller flagged this for a person. no_effect is defensible only because the binding text is Arabic note 3 via 2.1 and 2.2.
    - concern: The match with Arabic note 3 is not shown in the printed evidence, only in the proposer's rationale. The item says a person should confirm this.
- **ADD-03/T1-3/note(4)** (analysis-010; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The match with Arabic note 4 is asserted from the crop and not shown in the printed evidence.
    - concern: The item lists only the note itself as evidence. ADD-03:2.2 appears only in the statements.
- **ADD-03/AppB/para2** (analysis-010; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The text is a signature block and creates no obligation or amendment. No concern with no_effect.
- **DS-ADD03-VOL-II-7.2-01** (downstream-001; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The controller's replace_requirement check failed: the old value is not the row's requirement, or the new value is empty. The payload shows no 'old' field, so the proposed requirement replacement is not validated.
    - concern: The controller status is insufficient_evidence. The row's text before the addendum is not shown, so I cannot confirm the replace_requirement target.
    - concern: The 85%-110% band wording matches ADD-03:3.1, and the 7.3 restart wording is quoted verbatim. Nothing shown says what happens if a day falls outside the band. The item itself leaves that open for a person.
    - concern: The note about the 30-day rolling-average limit, VOL-V 1.5, and VOL-V 18.1/18.3 cites provisions that are not in the evidence shown, so I could not check them.
- **DS-ADD03-VOL-V-31.1-01** (downstream-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The row reads limb (a), which ADD-03 leaves unchanged. The addendum adds limb (d), and the item correctly flags that (d) is not read in this row. A person should decide whether (d) needs its own row.
    - concern: The statement S-311-D says (d) creates an 'Unavailability Event'. The lead-in text of 31.1 is not shown, so that label is not verifiable from the evidence shown.
    - concern: The note that deductions have no cap and that Schedule 7 is not supplied is not supported by the evidence shown. Only the quote from 31.2 is shown.
    - concern: The ADD-03:5.1 evidence span is only 'In Volume V Clause 31.1'. The substance of the change is supported by the (d) wording in the unit text.
- **DS-01** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Limb (b) is re-stated with identical words in the 5.1 substitution, and 31.2 supplies the Schedule 7 deduction and no-cap wording. This follows from the text.
    - concern: The note's statements that 31.3 as amended by ADD-03 5.2 gives no cure period for (b), and that the TN limit is 3 mg/l (ADD-02 5.1), are not backed by the ADD-03 5.1 text printed here. They rest on S-F2 and other units that are not shown. I could not verify the TN figure.
    - concern: Pending a person's decision on the interpretation.
- **DS-02** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: Limb (c) is kept verbatim. The substitution only changes the closing punctuation to ', or (d)', as the note says.
    - concern: The 72-hour cure period for (c) comes from 31.3, which is not printed here. It is cited only in S-F2, which this item does not list among its statements.
    - concern: The claim that the delivery point appears only on Drawing 03-C-114, and that this drawing was not supplied, is not in the evidence shown. I could not verify it.
- **DS-07** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The three differences are supported by the quoted text. The cover says the Authority accepts the programme, but 2.5 requires a Network Operator letter. The cover sets the deadline at 8 Working Days from the Addendum date, but 2.5 sets it at 8 Working Days before the Proposal Due Date. The cover say…
    - concern: Whether ADD-03 5.1 or 5.2 says anything about Ramp-Up for limb (d) is not shown in full. S-F6 asserts that neither does.
    - concern: The interim advice to plan to 'the earlier of the two deadlines' cannot be checked, because the Addendum date and Proposal Due Date are not in the evidence. The advice to price (d) deductions as applying in Ramp-Up is a conservative planning assumption, not a ruling. The person deciding should trea…
- **DS-13** (downstream-002; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: 2.2 says the Arabic text governs, and the Arabic reading (٤, i.e. 4) differs from the English 6. The Arabic note 1 also adds the Eid holidays to the Ramadan exclusion. The conflict is real on the evidence shown.
    - concern: The Arabic reading is still pending approval, so the TP-2 duration and the excluded periods cannot yet be fixed.
    - concern: The item says only that the Arabic value 'differs'. It does not state it. The evidence shows ٤ at ADD-03:p4-image/tp2-duration.
    - concern: The reliance of 2.3(b) and 2.7 on these figures is not shown in the printed evidence.
- **DS-14** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: This is the same Arabic/English discrepancy as DS-13, framed as an issue for Legal. It is supported by 2.2 and by the pending Arabic reading.
    - concern: The feed into 2.3 and 2.7 is not shown in the printed evidence.
    - concern: Both the TP-2 duration and the excluded periods rest on an unapproved Arabic reading.
    - concern: The issue leaves the conclusion to a person, which is appropriate.
- **ADD-03-DS-ESC-2.7** (downstream-003; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting; model claude-sonnet-5-5
    - concern: ADD-03:2.7 does say a Proposal is rejected if an interruption exceeds the maximum shutdown duration stated for that tie-in point in Table 1-3.
    - concern: The conflict rests on the TP-2 figures: a 01:00–05:00 window (4 hours) against a 6-hour maximum. The Table 1-3 row (ADD-03:T1-3/tp-2) is not printed in the units or evidence, so I cannot check those figures.
    - concern: The cited span for the statement is only clause 2.7. It does not contain the TP-2 values.
    - concern: Clause 2.7 refers only to the 'maximum shutdown duration'. Whether the permitted window also acts as a limit depends on Table 1-3 text I cannot see.
    - concern: I cannot confirm a real conflict from the evidence shown.
- **ADD-03-DS-ESC-Q19** (downstream-003; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting; model claude-sonnet-5-5
    - concern: The timing conflict is supported by the text. Q19 requires submission before the start of the reliability run under Vol II 7.2. VOL-II:7.4 says not later than 60 days after PCOD. The evidence does not show how the reliability run is sequenced against PCOD, but the two deadlines differ either way.
    - concern: The claim that ADD-03/4.1(b) deletes Vol II Clause 8.2 is not supported by anything printed. Neither the 4.1(b) text nor Clause 8.2 is shown. The VOL-II:8.2 conflict and the 'is a CMMS still required' question therefore depend on unverified evidence.
    - concern: The response also says the standard format will be issued only to the Preferred Bidder. That does not conflict with 7.4 as shown.

## Requests: failures, deferrals, repairs and route notices

- **downstream-003** (done): repaired once (1 problem(s) before the re-ask)

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
- **capabilities_declared** (analysis-010): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request was checked …
- **capabilities_declared** (downstream-001): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request was checke…
- **capabilities_declared** (downstream-002): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request was checke…
- **capabilities_declared** (downstream-003): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request was checke…
- **capabilities_declared** (downstream-004): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request was checke…

## Manual interventions (and automatic host sessions, named as such: not a person)

- 2026-10-05T17:36:16Z: host session (automatic) — batch reading-ADD-03-p4-r1 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session reading an image; not a person
- 2026-10-05T17:40:00Z: host session (automatic) — batch analysis-001 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T17:44:44Z: host session (automatic) — batch analysis-002 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T17:46:06Z: host session (automatic) — batch analysis-003 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T17:53:08Z: host session (automatic) — batch analysis-004 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T17:53:34Z: host session (automatic) — batch analysis-005 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T17:59:32Z: host session (automatic) — batch analysis-006 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T17:59:50Z: host session (automatic) — batch analysis-007 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T18:06:11Z: host session (automatic) — batch analysis-008 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T18:06:27Z: host session (automatic) — batch analysis-009 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T18:12:16Z: host session (automatic) — batch analysis-010 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-05T18:17:25Z: host session (automatic) — batch downstream-001 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-05T18:19:29Z: host session (automatic) — batch downstream-002 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-05T18:23:34Z: host session (automatic) — batch downstream-003 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-05T18:26:45Z: host session (automatic) — batch downstream-004 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person

## The diff (ADD-02 → ADD-03; [diff.md](diff.md))

## What changed from ADD-02 to ADD-03

### ADD-03: PARTIAL (issued 2026-11-10)

- ops: 11 (0 invalid); provisions: 70 (22 unresolved)
- validated state: ADD-02 — this addendum does NOT replace it until every provision is treated and every op is valid
- UNRESOLVED ADD-03:2.2: Table 1-3 is issued in the Arabic language. The Arabic text governs. The English translation at Appendix B is provided for convenience only.
- UNRESOLVED ADD-03:2.3: The Bidder shall elect, for each tie-in point, one of the following methods of maintaining flows during the connection works, and shall state its election in th
- UNRESOLVED ADD-03:2.4: The temporary works for method (a) shall be capable of passing, at each tie-in point, the maximum transfer flow stated for that tie-in point in Table 1-3.
- UNRESOLVED ADD-03:2.5: Where the Bidder elects method (b) for a tie-in point, it shall submit with Envelope A a letter from the Network Operator accepting the Bidder's proposed shutdo
- UNRESOLVED ADD-03:2.6: A Bidder that elects method (b) for a tie-in point but does not submit a Shutdown Acceptance Letter for that tie-in point with Envelope A shall be deemed to hav
- UNRESOLVED ADD-03:2.7: A Proposal that provides for an interruption of flow at a tie-in point for longer than the maximum shutdown duration stated for that tie-in point in Table 1-3 s
- UNRESOLVED ADD-03:Q17: No: 17 | Bidder question: Volume V Clause 12.3 provides that the reasonable costs of the Independent Engineer are borne equally by the parties. Does this apply 
- UNRESOLVED ADD-03:Q18: No: 18 | Bidder question: If the flow delivered to the Facility by the existing collection network during the reliability run under Volume II Clause 7.2 is lowe
- UNRESOLVED ADD-03:Q19: No: 19 | Bidder question: Volume II Clause 7.4 requires an asset register in the Authority's standard format. Will the format be issued before the Proposal Due 
- UNRESOLVED ADD-03:Q20: No: 20 | Bidder question: What design flow should be used for the temporary works needed to maintain flows at the tie-in points referred to in Volume II Clause 
- UNRESOLVED ADD-03:p4-image/tp1-location: غرفة التفتيش MH-41 على خط الطرد الشمالي
- UNRESOLVED ADD-03:p4-image/tp1-diameter: ١٠٠٠
- UNRESOLVED ADD-03:p4-image/tp1-window: من ٢٣:٠٠ إلى ٠٥:٠٠
- UNRESOLVED ADD-03:p4-image/tp1-duration: ٦
- UNRESOLVED ADD-03:p4-image/tp1-notice: ١٠ أيام عمل
- UNRESOLVED ADD-03:p4-image/tp2-point: TP-2
- UNRESOLVED ADD-03:p4-image/tp2-location: غرفة التفتيش MH-07 على خط الانحدار الجنوبي
- UNRESOLVED ADD-03:p4-image/tp2-diameter: ٨٠٠
- UNRESOLVED ADD-03:p4-image/tp2-duration: ٤
- UNRESOLVED ADD-03:p4-image/note1: ١. لا يُسمح بأي إيقاف خلال شهر رمضان المبارك أو خلال إجازتَي عيد الفطر وعيد الأضحى.
- UNRESOLVED ADD-03:T1-3/tp-2: Tie-in point: TP-2 | Location: Manhole MH-07 on the southern gravity sewer | Existing sewer diameter (mm): 800 | Permitted shutdown window: 01:00 to 05:00 | Max
- UNRESOLVED ADD-03:T1-3/note(1): (1)  No shutdown is permitted during the holy month of Ramadan.
- cover summary vs provisions (C28, report only): 8 finding(s)
  - unknown verb: 'incorporates the Network Operator's Table 1-3 describing the two tie-in points referred to in Volume II Clause 1.3': C28 does not know the verb 'incorporates', so what it claims is compared by its targets only; a person reads it against the provisions
  - not found: 'requires a Bidder that elects to interrupt flows at a tie-in point to obtain the Authority's acceptance of its shutdown programme, applications for which shall be made within eight (8) Working Days of the date of this Addendum': no provision of ADD-03 does this
  - contradicted: 'introduces a flow range for the reliability run in Volume II Clause 7.2', but ADD-03/3.1 amends VOL-II:7.2
  - not found: 'adds to Volume V Clause 31.1 a new Unavailability Event for loss of treated effluent volume, with no cure period and with no deduction during the Ramp-Up Period': no provision of ADD-03 matches 'with no cure period and with no deduction during the Ramp-Up Period'
  - contradicted: 'adds to Volume V Clause 31.1 a new Unavailability Event for loss of treated effluent volume, with no cure period and with no deduction during the Ramp-Up Period', but ADD-03/5.1 amends VOL-V:31.1
  - omitted: ADD-03/4.1(b) deletes VOL-II:8.2; the summary does not mention it: 'Volume II Clauses 8.1 to 8.3 are deleted and replaced by the following: ‘8.1 The Project Company shall hold a spare parts inventory sufficient for eighteen (18) months of normal operation for all items with a lead time exceeding twelve (12…'
  - omitted: ADD-03/4.1(c) amends VOL-II:8.3; the summary does not mention it: 'Volume II Clauses 8.1 to 8.3 are deleted and replaced by the following: ‘8.1 The Project Company shall hold a spare parts inventory sufficient for eighteen (18) months of normal operation for all items with a lead time exceeding twelve (12…'
  - omitted: ADD-03/5.2 amends VOL-V:31.3; the summary does not mention it: 'In Volume V Clause 31.3, ‘No cure period applies to an event under Clause 31.1(b).’ is deleted and ‘No cure period applies to an event under Clause 31.1(b) or Clause 31.1(d).’ is substituted.'

#### Validated vs candidate (partial should not mean useless)

- validated (unchanged, ADD-02): `<outputs>/a3/a3.pdf` (one page), `<outputs>/a5/`
- candidate (CANDIDATE — NOT VALIDATED, ADD-03 as proposed): `<outputs>/a3/a3_candidate.pdf` / `.md`, `<outputs>/a5/candidate/`

**What may be changing.** ADD-03 is PARTIAL: 22 of 70 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 11 op(s) that are valid there stood (each still a proposal: review proposed 11), A3 would gain 0 row(s) (none), lose 0 (none) and change 0 (none); A5, replanned at ADD-03's issue date (2026-11-10), would move the latest dates of 0 activities (none), add 0 (none) and remove 0 (none), and marks 7 REVIEW through relationships. Not settled: 3 activities blocked by an unresolved row (technical-proposal, deviations-review, form-4e), 5 STALE row(s), 1 obligation(s) reaching no output (C46), 0 relationship chain(s) blocked or incomplete, 8 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT and 5 more; conditional or effective-dated: ADD-03:2.5 (conditional obligation). Nothing here is validated, accepted or applied to the real state.

### Requirements

- new: 2; out of force: 1; changed: 15

- NEW ADD-03-cover-para3-01: NEW (introduced by ADD-03/cover/para3)
- NEW ADD-03-2.3-01: NEW (introduced by ADD-03:2.3)
- OUT VOL-II-8.2-01: DELETED (ADD-03/4.1(b))
- CHANGED VOL-V-31.3-01: wording (by ADD-03/5.2)
- CHANGED VOL-I-10.2-01: VOL-V 31.1: 'An Unavailability Event occurs where (a) the Facility is unable to tr…' -> 'An Unavailability Event occurs where (a) the Facility is unable to tr…' by ADD-03/5.1 (depends on it: REL-PAY-QUOTED-PRICE (feeds_calculation, confirmed) < REL-PAY-DEDUCTIONS (depends_on, proposed)); VOL-V 31.3: 'A cure period of twenty-four (24) hours applies to an Unavailability …' -> 'A cure period of twenty-four (24) hours applies to an Unavailability …' by ADD-03/5.2 (depends on it: REL-PAY-QUOTED-PRICE (feeds_calculation, confirmed) < REL-PAY-DEDUCTIONS (depends_on, proposed))
- CHANGED VOL-I-10.3-01: VOL-V 31.1: 'An Unavailability Event occurs where (a) the Facility is unable to tr…' -> 'An Unavailability Event occurs where (a) the Facility is unable to tr…' by ADD-03/5.1 (depends on it: REL-PAY-FINANCIAL-MODEL (depends_on, proposed) < REL-PAY-DEDUCTIONS (depends_on, proposed)); VOL-V 31.3: 'A cure period of twenty-four (24) hours applies to an Unavailability …' -> 'A cure period of twenty-four (24) hours applies to an Unavailability …' by ADD-03/5.2 (depends on it: REL-PAY-FINANCIAL-MODEL (depends_on, proposed) < REL-PAY-DEDUCTIONS (depends_on, proposed))
- CHANGED VOL-II-1.3-01: wording (by ADD-03/2.1)
- CHANGED VOL-II-7.2-01: wording (by ADD-03/3.1)
- CHANGED VOL-II-8.1-01: wording (by ADD-03/4.1(a))
- CHANGED VOL-II-8.3-01: wording (by ADD-03/4.1(c))
- CHANGED VOL-II-8.3-02: wording (by ADD-03/4.1(c))
- CHANGED VOL-IV-F4E-01: VOL-V 31.1: 'An Unavailability Event occurs where (a) the Facility is unable to tr…' -> 'An Unavailability Event occurs where (a) the Facility is unable to tr…' by ADD-03/5.1 (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed)); VOL-V 31.3: 'A cure period of twenty-four (24) hours applies to an Unavailability …' -> 'A cure period of twenty-four (24) hours applies to an Unavailability …' by ADD-03/5.2 (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed))
- CHANGED VOL-IV-F4F-01: VOL-V 31.1: 'An Unavailability Event occurs where (a) the Facility is unable to tr…' -> 'An Unavailability Event occurs where (a) the Facility is unable to tr…' by ADD-03/5.1 (depends on it: REL-PAY-FORM-4F (feeds_calculation, confirmed) < REL-PAY-DEDUCTIONS (depends_on, proposed)); VOL-V 31.3: 'A cure period of twenty-four (24) hours applies to an Unavailability …' -> 'A cure period of twenty-four (24) hours applies to an Unavailability …' by ADD-03/5.2 (depends on it: REL-PAY-FORM-4F (feeds_calculation, confirmed) < REL-PAY-DEDUCTIONS (depends_on, proposed))
- CHANGED VOL-V-31.1-01: wording (by ADD-03/5.1)
- CHANGED VOL-V-31.1-02: wording (by ADD-03/5.1)
- CHANGED VOL-V-31.1-03: wording (by ADD-03/5.1)
- CHANGED VOL-V-31.3-02: wording (by ADD-03/5.2)
- CHANGED VOL-V-31.3-03: wording (by ADD-03/5.2)
- CONFIRMED (unchanged) VOL-II-3.3-01: confirmed by ADD-03/Q16 (confirms; ADD-03:Q16; answer reads 'adds' (summary.classify_answer)); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03 with the same words. ADD-03/Q16 annotates Clause 3.3 as confirmed and leaves its wording unchanged: 'Ozonation alone is not acceptable.' The …')
- CONFIRMED (unchanged) VOL-II-8.4-01: confirmed by ADD-03/4.2 (confirms; ADD-03:4.2); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03 with the same words. ADD-03/4.2 annotates Clause 8.4 as unchanged and not renumbered. [AI workflow run ADD-03-run-host-blind06-20261005T17322…')
- CONFIRMED (unchanged) VOL-II-8.4-02: confirmed by ADD-03/4.2 (confirms; ADD-03:4.2); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03 with the same words; ADD-03/4.2 annotates Clause 8.4 as unchanged. The clause still says: 'Disposal to landfill of sludge exceeding 500 tonne…')
- CONFIRMED (unchanged) VOL-II-8.5-01: confirmed by ADD-03/4.2 (confirms; ADD-03:4.2); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03 with the same words; ADD-03/4.2 annotates Clause 8.5 as unchanged. The handback condition in VOL-V 42.1 refers to this clause. When the conce…')
- CONFIRMED (unchanged) VOL-II-8.5-02: confirmed by ADD-03/4.2 (confirms; ADD-03:4.2); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03 with the same words; ADD-03/4.2 annotates Clause 8.5 as unchanged. The transfer date still depends on the start of the concession term (I-CON…')

### Stale readings and decisions

- STALE VOL-II-1.3-01: VOL-II:1.3 changed since BASE (by ADD-03/2.1)
- STALE VOL-II-7.2-01: new dependency ADD-03:3.2; VOL-II:7.2 changed since BASE (by ADD-03/3.1); VOL-II:7.3 changed since BASE (by ADD-03/3.2(b)); quote not found in the effective text at ADD-03: 'PCOD shall not be certified until the Facility
- STALE VOL-II-8.1-01: VOL-II:8.1 changed since BASE (by ADD-03/4.1(a)); quote not found in the effective text at ADD-03: 'shall hold a spare parts inventory sufficient for two (2) ye' (expected: the interpretation predates the change)
- STALE VOL-II-8.3-01: VOL-II:8.3 changed since BASE (by ADD-03/4.1(c)); quote not found in the effective text at ADD-03: 'shall employ a suitably qualified plant manager' (expected: the interpretation predates the change)
- STALE VOL-V-31.3-03: VOL-V:31.3 changed since BASE (by ADD-03/5.2); quote not found in the effective text at ADD-03: 'No cure period applies to an event under Clause 31.1(b).' (expected: the interpretation predates the change)

### Obligations not reaching the outputs (C46)

- ADD-03/cover/para3 [A3]: ADD-03/cover/para3 brings in consequence words ['deduction'] that no row's consequence carries at ADD-03: 'This Addendum incorporates the Network Operator's Table 1-3 describing the two tie-in points referred to in Volume II Clause 1.3, req

### Reached through relationships (indirect: for review, not direct citations)

Curated links (relationships file) followed from what changed. The requirements above cite a changed unit; these are reached through another provision, in three classes that are never merged. A5 marks the activities that serve them REVIEW with their dates unchanged.

Relationship status: confirmed = stated in the documents (the entry quotes the cross-reference), not confirmed by a person; proposed = inferred by a curator or a model, a person decides; possible = a weaker inference.

#### Confirmed dependency (1)
- VOL-IV-F4E-01 (row; ACTIVE) <- VOL-V:31.1, VOL-V:31.3 via REL-VOL-V-FORM-4E [depends_on; link confirmed]

#### Proposed relationship (6)
- ADD-03:p4-image (unit; ACTIVE) <- VOL-II-1.3-01 via REL-AI-001 [cites; link proposed]; also changed directly
- VOL-I-10.2-01 (row; ACTIVE) <- VOL-V:31.1, VOL-V:31.3 via REL-PAY-DEDUCTIONS > REL-PAY-QUOTED-PRICE [feeds_calculation; link proposed]
- VOL-I-10.3-01 (row; ACTIVE) <- VOL-V:31.1, VOL-V:31.3 via REL-PAY-DEDUCTIONS > REL-PAY-FINANCIAL-MODEL [depends_on; link proposed]
- VOL-IV-F4F-01 (row; ACTIVE) <- VOL-V:31.1, VOL-V:31.3 via REL-PAY-DEDUCTIONS > REL-PAY-FORM-4F [feeds_calculation; link proposed]
- VOL-IV-F4F-02 (row; ACTIVE) <- VOL-V:31.1, VOL-V:31.3 via REL-PAY-DEDUCTIONS > REL-PAY-FINANCIAL-MODEL > REL-MODEL-FORM-4F [feeds_calculation; link proposed]
- calc:availability-payment (calculation) <- VOL-V:31.1, VOL-V:31.3 via REL-PAY-DEDUCTIONS [depends_on; link proposed]

#### Possible impact (1)
- VOL-I-10.6-01 (row; ACTIVE) <- VOL-V:31.1, VOL-V:31.3 via REL-PAY-DEDUCTIONS > REL-PAY-FINANCING-ASSUMPTIONS [depends_on; link possible]

#### Referenced but not supplied: conclusions in play that cannot be established (3)
- VOL-V-31.1-01 (row; AMENDED (ADD-03/5.1)) <- target changed via REL-MISSING-SCHEDULE-7-DEDUCTIONS [missing_document; link confirmed]; also changed directly. NOT SUPPLIED: Volume V Schedule 7 (deductions); cannot be established: the amount of the deduction for each Unavailability Event under 31.1(a), (b) and (c), so the price risk of each
- VOL-V-31.1-02 (row; AMENDED (ADD-03/5.1)) <- target changed via REL-MISSING-SCHEDULE-7-DEDUCTIONS [missing_document; link confirmed]; also changed directly. NOT SUPPLIED: Volume V Schedule 7 (deductions); cannot be established: the amount of the deduction for each Unavailability Event under 31.1(a), (b) and (c), so the price risk of each
- VOL-V-31.1-03 (row; AMENDED (ADD-03/5.1)) <- target changed via REL-MISSING-SCHEDULE-7-DEDUCTIONS [missing_document; link confirmed]; also changed directly. NOT SUPPLIED: Volume V Schedule 7 (deductions); cannot be established: the amount of the deduction for each Unavailability Event under 31.1(a), (b) and (c), so the price risk of each

### Disqualifiers (A3)

- no change

### Earlier answers to re-read against the new text (never revoked; a person decides)

- `ADD-03:Q18` (ADD-03): cites VOL-II:7.2, changed by ADD-03/3.1; to be re-read against the new text of VOL-II:7.2 (ADD-03/3.1); a person decides whether the answer still holds
- `ADD-03:Q19` (ADD-03): cites VOL-II:7.2, changed by ADD-03/3.1; cites VOL-II:8.2, changed by ADD-03/4.1(b); to be re-read against the new text of VOL-II:7.2, VOL-II:8.2 (ADD-03/3.1, ADD-03/4.1(b)); a person decides whether the answer still holds
- `ADD-03:Q20` (ADD-03): cites VOL-II:1.3, changed by ADD-03/2.1; to be re-read against the new text of VOL-II:1.3 (ADD-03/2.1); a person decides whether the answer still holds

### Programme impact (status date 2026-10-22 -> 2026-11-10)

- STATUS assemble-envelope-a: timing INFEASIBLE by 12 WD -> INFEASIBLE by 25 WD; total float -12 -> -25 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS assemble-envelope-b: timing OK -> INFEASIBLE by 13 WD; total float 0 -> -13 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS attendance-notice: timing CONDITIONAL — window elapsed 2026-10-14; whether the condition arose is not known -> CONDITIONAL — window elapsed 2026-10-14; whether the condition arose is not known; total float -7 -> -20 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS bond-approval: timing OK -> INFEASIBLE by 3 WD; total float +10 -> -3 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS bond-issue: timing OK -> INFEASIBLE by 3 WD; total float +10 -> -3 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS clarifications: timing OK -> OK; total float +13 -> 0 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS completion-certs: timing OK -> INFEASIBLE by 6 WD; total float +7 -> -6 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS consortium-check: timing OK -> OK; total float +13 -> 0 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS copies: timing INFEASIBLE by 12 WD -> INFEASIBLE by 25 WD; total float -12 -> -25 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS deliver: timing INFEASIBLE by 12 WD -> INFEASIBLE by 25 WD; total float -12 -> -25 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- REWORK deviations-review: requirement changed: VOL-IV-F4E-01 (dependency: VOL-V 31.1: 'An Unavailability Event occurs where (a) the Facility is unable to tr…' -> 'An Unavailability Event occurs where (a) the Facility is unable to tr…' by ADD-03/5.1 (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed)); VOL-V 31.3: 'A cure period of twenty-four (24) hours applies to an Unavailability …' -> 'A cure period of twenty-four (24) hours applies to an Unavailability …' by ADD-03/5.2 (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed))), VOL-V-31.1-01 (text, status), VOL-V-31.1-02 (text, status), VOL-V-31.1-03 (text, status), VOL-V-31.3-01 (text), VOL-V-31.3-02 (text), VOL-V-31.3-03 (text, status, stale)
- STATUS deviations-review: timing OK -> INFEASIBLE by 2 WD; total float +11 -> -2 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS fin-assumptions: timing OK -> INFEASIBLE by 8 WD; total float +5 -> -8 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- REWORK fin-model-build: requirement changed: VOL-I-10.3-01 (dependency: VOL-V 31.1: 'An Unavailability Event occurs where (a) the Facility is unable to tr…' -> 'An Unavailability Event occurs where (a) the Facility is unable to tr…' by ADD-03/5.1 (depends on it: REL-PAY-FINANCIAL-MODEL (depends_on, proposed) < REL-PAY-DEDUCTIONS (depends_on, proposed)); VOL-V 31.3: 'A cure period of twenty-four (24) hours applies to an Unavailability …' -> 'A cure period of twenty-four (24) hours applies to an Unavailability …' by ADD-03/5.2 (depends on it: REL-PAY-FINANCIAL-MODEL (depends_on, proposed) < REL-PAY-DEDUCTIONS (depends_on, proposed)))
- STATUS fin-model-build: timing OK -> INFEASIBLE by 13 WD; total float 0 -> -13 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- REWORK fin-model-freeze: requirement changed: VOL-I-10.3-01 (dependency: VOL-V 31.1: 'An Unavailability Event occurs where (a) the Facility is unable to tr…' -> 'An Unavailability Event occurs where (a) the Facility is unable to tr…' by ADD-03/5.1 (depends on it: REL-PAY-FINANCIAL-MODEL (depends_on, proposed) < REL-PAY-DEDUCTIONS (depends_on, proposed)); VOL-V 31.3: 'A cure period of twenty-four (24) hours applies to an Unavailability …' -> 'A cure period of twenty-four (24) hours applies to an Unavailability …' by ADD-03/5.2 (depends on it: REL-PAY-FINANCIAL-MODEL (depends_on, proposed) < REL-PAY-DEDUCTIONS (depends_on, proposed)))
- STATUS fin-model-freeze: timing OK -> INFEASIBLE by 13 WD; total float 0 -> -13 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS fin-standing: timing OK -> OK; total float +15 -> +2 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS fin-statements: timing OK -> OK; total float +15 -> +2 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- REWORK form-4a: requirement changed: ADD-01-AppA-01 (Addenda to acknowledge: ADD-03 issued since ADD-02: 'Bidders shall acknowledge receipt in Form 4-A.'), ADD-03-cover-para3-01 (text, status, consequence, quote)
- NOT SETTLED form-4a: VOL-IV-F4A-01: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); VOL-IV-F4A-02: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); unchanged at this stage but not confirmed: a person decides
- STATUS form-4a: timing OK -> INFEASIBLE by 1 WD; total float +12 -> -1 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- REWORK form-4a-prep: requirement changed: ADD-01-AppA-01 (Addenda to acknowledge: ADD-03 issued since ADD-02: 'Bidders shall acknowledge receipt in Form 4-A.'), ADD-03-cover-para3-01 (text, status, consequence, quote)
- NOT SETTLED form-4a-prep: VOL-IV-F4A-01: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); VOL-IV-F4A-02: CONFLICT: ADD-01 AppA/proposal-due-date prints 2026-11-12; the PDD is 2026-11-26 (VOL-I 6.1 as amended by ADD-01 2.1): not corrected (a person decides); unchanged at this stage but not confirmed: a person decides
- STATUS form-4a-prep: timing OK -> OK; total float +20 -> +7 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS form-4b: timing OK -> INFEASIBLE by 6 WD; total float +7 -> -6 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS form-4b-prep: timing OK -> INFEASIBLE by 4 WD; total float +9 -> -4 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS form-4c-prep: timing OK -> OK; total float +18 -> +5 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS form-4c-sign: timing OK -> INFEASIBLE by 3 WD; total float +10 -> -3 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- REWORK form-4e: requirement changed: VOL-IV-F4E-01 (dependency: VOL-V 31.1: 'An Unavailability Event occurs where (a) the Facility is unable to tr…' -> 'An Unavailability Event occurs where (a) the Facility is unable to tr…' by ADD-03/5.1 (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed)); VOL-V 31.3: 'A cure period of twenty-four (24) hours applies to an Unavailability …' -> 'A cure period of twenty-four (24) hours applies to an Unavailability …' by ADD-03/5.2 (depends on it: REL-VOL-V-FORM-4E (depends_on, confirmed))), VOL-V-31.1-01 (text, status), VOL-V-31.1-02 (text, status), VOL-V-31.1-03 (text, status), VOL-V-31.3-01 (text), VOL-V-31.3-02 (text), VOL-V-31.3-03 (text, status, stale)
- STATUS form-4e: timing OK -> INFEASIBLE by 12 WD; total float +1 -> -12 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- REWORK form-4f: requirement changed: VOL-I-10.2-01 (dependency: VOL-V 31.1: 'An Unavailability Event occurs where (a) the Facility is unable to tr…' -> 'An Unavailability Event occurs where (a) the Facility is unable to tr…' by ADD-03/5.1 (depends on it: REL-PAY-QUOTED-PRICE (feeds_calculation, confirmed) < REL-PAY-DEDUCTIONS (depends_on, proposed)); VOL-V 31.3: 'A cure period of twenty-four (24) hours applies to an Unavailability …' -> 'A cure period of twenty-four (24) hours applies to an Unavailability …' by ADD-03/5.2 (depends on it: REL-PAY-QUOTED-PRICE (feeds_calculation, confirmed) < REL-PAY-DEDUCTIONS (depends_on, proposed))), VOL-IV-F4F-01 (dependency: VOL-V 31.1: 'An Unavailability Event occurs where (a) the Facility is unable to tr…' -> 'An Unavailability Event occurs where (a) the Facility is unable to tr…' by ADD-03/5.1 (depends on it: REL-PAY-FORM-4F (feeds_calculation, confirmed) < REL-PAY-DEDUCTIONS (depends_on, proposed)); VOL-V 31.3: 'A cure period of twenty-four (24) hours applies to an Unavailability …' -> 'A cure period of twenty-four (24) hours applies to an Unavailability …' by ADD-03/5.2 (depends on it: REL-PAY-FORM-4F (feeds_calculation, confirmed) < REL-PAY-DEDUCTIONS (depends_on, proposed)))
- STATUS form-4f: timing OK -> INFEASIBLE by 13 WD; total float 0 -> -13 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS form-4g-review: timing OK -> OK; total float +17 -> +4 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS form-4g-sign: timing OK -> INFEASIBLE by 1 WD; total float +12 -> -1 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS ground-dd: timing OK -> INFEASIBLE by 8 WD; total float +5 -> -8 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS investment-licence: timing OK -> INFEASIBLE by 5 WD; total float +8 -> -5 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS iso-copy: timing OK -> OK; total float +21 -> +8 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS lcc-certificate: timing INFEASIBLE by 12 WD -> INFEASIBLE by 25 WD; total float -12 -> -25 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS lcc-ratio: timing INFEASIBLE by 12 WD -> INFEASIBLE by 25 WD; total float -12 -> -25 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS lender-terms: timing OK -> INFEASIBLE by 8 WD; total float +5 -> -8 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS model-audit-opinion: timing OK -> INFEASIBLE by 13 WD; total float 0 -> -13 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS model-audit-review: timing OK -> INFEASIBLE by 12 WD; total float +1 -> -12 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS model-auditor-appoint: timing OK -> INFEASIBLE by 12 WD; total float +1 -> -12 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS om-evidence: timing OK -> OK; total float +13 -> 0 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS pcg-execution: timing OK -> INFEASIBLE by 10 WD; total float +3 -> -10 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS pcg-wording: timing OK -> INFEASIBLE by 10 WD; total float +3 -> -10 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS poa: timing OK -> INFEASIBLE by 5 WD; total float +8 -> -5 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS poa-resolutions: timing OK -> INFEASIBLE by 5 WD; total float +8 -> -5 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS references: timing OK -> INFEASIBLE by 4 WD; total float +9 -> -4 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS seal-and-mark: timing INFEASIBLE by 12 WD -> INFEASIBLE by 25 WD; total float -12 -> -25 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- STATUS spoc: timing OK -> OK; total float +21 -> +8 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- REWORK technical-proposal: requirement changed: ADD-03-2.3-01 (text, status, consequence, quote, parameters), VOL-II-1.3-01 (text, status, stale), VOL-II-7.2-01 (text, status, stale), VOL-II-8.1-01 (text, status, stale), VOL-II-8.3-01 (text, status, stale), VOL-II-8.3-02 (text, status)
- CONFIRMED (unchanged) technical-proposal: VOL-II-3.3-01: confirmed by ADD-03/Q16 (confirms; ADD-03:Q16; answer reads 'adds' (summary.classify_answer)); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03 with the same words. ADD-03/Q16 annotates Clause 3.3 as confirmed and leaves its wording unchanged: 'Ozonation alone is not acceptable.' The …'); VOL-II-8.4-01: confirmed by ADD-03/4.2 (confirms; ADD-03:4.2); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03 with the same words. ADD-03/4.2 annotates Clause 8.4 as unchanged and not renumbered. [AI workflow run ADD-03-run-host-blind06-20261005T17322…'); VOL-II-8.4-02: confirmed by ADD-03/4.2 (confirms; ADD-03:4.2); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03 with the same words; ADD-03/4.2 annotates Clause 8.4 as unchanged. The clause still says: 'Disposal to landfill of sludge exceeding 500 tonne…'); VOL-II-8.5-01: confirmed by ADD-03/4.2 (confirms; ADD-03:4.2); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03 with the same words; ADD-03/4.2 annotates Clause 8.5 as unchanged. The handback condition in VOL-V 42.1 refers to this clause. When the conce…'); VOL-II-8.5-02: confirmed by ADD-03/4.2 (confirms; ADD-03:4.2); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03 with the same words; ADD-03/4.2 annotates Clause 8.5 as unchanged. The transfer date still depends on the start of the concession term (I-CON…'); text, cells, dates, status and consequence unchanged: work done stands
- STATUS technical-proposal: timing OK -> INFEASIBLE by 12 WD; total float +1 -> -12 WD; the planning date moved 2026-10-22 -> 2026-11-10, which by itself shifts every float by the Working Days between them
- REVIEW (confirmed dependency) deviations-review: VOL-IV-F4E-01 reached from VOL-V:31.1, VOL-V:31.3 via REL-VOL-V-FORM-4E; dates unchanged
- REVIEW (possible impact) fin-assumptions: VOL-I-10.6-01 reached from VOL-V:31.1, VOL-V:31.3 via REL-PAY-DEDUCTIONS, REL-PAY-FINANCING-ASSUMPTIONS; dates unchanged
- REVIEW (proposed relationship) fin-model-build: VOL-I-10.3-01, VOL-IV-F4F-02 reached from VOL-V:31.1, VOL-V:31.3 via REL-MODEL-FORM-4F, REL-PAY-DEDUCTIONS, REL-PAY-FINANCIAL-MODEL; dates unchanged
- REVIEW (proposed relationship) fin-model-freeze: VOL-I-10.3-01, VOL-IV-F4F-02 reached from VOL-V:31.1, VOL-V:31.3 via REL-MODEL-FORM-4F, REL-PAY-DEDUCTIONS, REL-PAY-FINANCIAL-MODEL; dates unchanged
- REVIEW (confirmed dependency) form-4e: VOL-IV-F4E-01 reached from VOL-V:31.1, VOL-V:31.3 via REL-VOL-V-FORM-4E; dates unchanged
- REVIEW (proposed relationship) form-4f: VOL-I-10.2-01, VOL-IV-F4F-01, VOL-IV-F4F-02 reached from VOL-V:31.1, VOL-V:31.3 via REL-MODEL-FORM-4F, REL-PAY-DEDUCTIONS, REL-PAY-FINANCIAL-MODEL, REL-PAY-FORM-4F, REL-PAY-QUOTED-PRICE; dates unchanged
- REVIEW (possible impact) lender-terms: VOL-I-10.6-01 reached from VOL-V:31.1, VOL-V:31.3 via REL-PAY-DEDUCTIONS, REL-PAY-FINANCING-ASSUMPTIONS; dates unchanged
- FEASIBILITY lcc-ratio: INFEASIBLE by 12 WD -> INFEASIBLE by 25 WD
- FEASIBILITY lcc-certificate: INFEASIBLE by 12 WD -> INFEASIBLE by 25 WD
- FEASIBILITY fin-model-build: OK -> INFEASIBLE by 13 WD
- FEASIBILITY model-auditor-appoint: OK -> INFEASIBLE by 12 WD
- FEASIBILITY technical-proposal: OK -> INFEASIBLE by 12 WD
- FEASIBILITY pcg-wording: OK -> INFEASIBLE by 10 WD
- FEASIBILITY ground-dd: OK -> INFEASIBLE by 8 WD
- FEASIBILITY lender-terms: OK -> INFEASIBLE by 8 WD
- FEASIBILITY model-audit-review: OK -> INFEASIBLE by 12 WD
- FEASIBILITY completion-certs: OK -> INFEASIBLE by 6 WD
- FEASIBILITY poa-resolutions: OK -> INFEASIBLE by 5 WD
- FEASIBILITY references: OK -> INFEASIBLE by 4 WD
- FEASIBILITY bond-approval: OK -> INFEASIBLE by 3 WD
- FEASIBILITY deviations-review: OK -> INFEASIBLE by 2 WD
- FEASIBILITY pcg-execution: OK -> INFEASIBLE by 10 WD
- FEASIBILITY poa: OK -> INFEASIBLE by 5 WD
- FEASIBILITY fin-model-freeze: OK -> INFEASIBLE by 13 WD
- FEASIBILITY model-audit-opinion: OK -> INFEASIBLE by 13 WD
- FEASIBILITY investment-licence: OK -> INFEASIBLE by 5 WD
- FEASIBILITY form-4b-prep: OK -> INFEASIBLE by 4 WD
- FEASIBILITY bond-issue: OK -> INFEASIBLE by 3 WD
- FEASIBILITY form-4c-sign: OK -> INFEASIBLE by 3 WD
- FEASIBILITY fin-assumptions: OK -> INFEASIBLE by 8 WD
- FEASIBILITY form-4e: OK -> INFEASIBLE by 12 WD
- FEASIBILITY form-4f: OK -> INFEASIBLE by 13 WD
- FEASIBILITY form-4a: OK -> INFEASIBLE by 1 WD
- FEASIBILITY form-4b: OK -> INFEASIBLE by 6 WD
- FEASIBILITY form-4g-sign: OK -> INFEASIBLE by 1 WD
- FEASIBILITY assemble-envelope-a: INFEASIBLE by 12 WD -> INFEASIBLE by 25 WD
- FEASIBILITY assemble-envelope-b: OK -> INFEASIBLE by 13 WD
- FEASIBILITY copies: INFEASIBLE by 12 WD -> INFEASIBLE by 25 WD
- FEASIBILITY seal-and-mark: INFEASIBLE by 12 WD -> INFEASIBLE by 25 WD
- FEASIBILITY deliver: INFEASIBLE by 12 WD -> INFEASIBLE by 25 WD

## Next (a person)

- read the unresolved and escalated provisions first, then each item against its evidence (`../ai/ADD-03-run-host-blind06-20261005T173226Z-combined/proposals.yaml`, `../downstream/proposals.yaml`)
- nothing here is applied to the real curation: to take an item over, add the PDF to the pack (OPERATING_GUIDE §3 steps 1-2) and copy the reviewed files listed in `promotion.json`; then `pin`, `check-register`, `outputs` and decide with `accept` / `reject` as usual
