# Review packet: ADD-03, AI workflow run ADD-03-run-host-20261015T131927Z-745a

> **CANDIDATE: proposed by the AI workflow; not reviewed; nothing accepted.** Statuses are the controller's; a person decides every item. The real `curation/`, `config/` and `out/` were only read: everything below lives in this run's folder.

- PDF: `${INTERVIEW_ROOT}/staging/panel/uploads/6f9f9d7c7d68bc83b947d20fa348271b91695463eae5435a70b09afd1955ad25.pdf` (sha256 6f9f9d7c7d68bc83…, 2 pages); preceding state: pack `${INTERVIEW_ROOT}/config/pack.yaml` (NUPA-ISTP-2026-014), previous evidence build `${INTERVIEW_ROOT}/build`
- route **host**; model requested `codex exec (configured gpt-6-astra; runtime model identity reported separately)`, reported `None`
- status **partial**: 5 provision(s) unresolved in the candidate (listed first in the review packet); 14 downstream task(s) answered only by items that cannot be promoted: row:ADD-02-F4G-06, row:ADD-02-F4G-07, act:form-4g-review, act:form-4g-sign, act:clarifications, act:copies, act:assemble-envelope-a, act:assemble-envelope-b …
- usage (application routes): none: the run's route is host, every exchange ran in a host session (below)
- host sessions: 13 (their own records); usage of the 11 that reported it: input 2525271, cache write 0, cache read 0 / output 60114 tokens; usage **unknown** for 2 session(s): ADD-03-hostsession-20261015T134601Z-a6f3 (batch not recorded), ADD-03-hostsession-20261015T135558Z-c8a1 (batch not recorded)
- code at start: content bbf58cf324573bcd… over 102 files; git not available; recorded 2026-10-15T13:19:27Z

## Execution, completeness and approval (three separate things)

- **Execution** (what ran): ingest done, readings done, analysis done, validation done, downstream done, downstream_validation done, critic done, promotion done, pin done, check_register done, outputs done, diff done, review running; batches analysis: {'done': 4}; downstream: {'done': 10}
- **Completeness** (what the run completed): **partial**: 5 provision(s) unresolved in the candidate (listed first in the review packet); 14 downstream task(s) answered only by items that cannot be promoted: row:ADD-02-F4G-06, row:ADD-02-F4G-07, act:form-4g-review, act:form-4g-sign, act:clarifications, act:copies, act:assemble-envelope-a, act:assemble-envelope-b …
  - downstream tasks: 58; answered 44; unanswered 0; answered only by items that cannot be promoted 14; answered 'no change' 2
- **Human approval**: **simulated** (INTERVIEW DEMO: eligible reviews assumed approved on the owner's instruction; no actual human review or tender release); decisions a person recorded in the candidate's decisions file: accept row ADD-01-3.1-01 by Interview demo assumption (2026-10-10); accept row ADD-01-AppA-01 by Interview demo assumption (2026-10-10); accept row ADD-01-Q4-01 by Interview demo assumption (2026-10-10); accept op ADD-01/2.1 by Interview demo assumption (2026-10-10); accept op ADD-01/2.2 by Interview demo assumption (2026-10-10); accept op ADD-01/3.1 by Interview demo assumption (2026-10-10); accept op ADD-01/3.2 by Interview demo assumption (2026-10-10); accept op ADD-01/4.1 by Interview demo assumption (2026-10-10); accept op ADD-01/4.2 by Interview demo assumption (2026-10-10); accept op ADD-01/5.1 by Interview demo assumption (2026-10-10)

## What is candidate and what is real

- **Candidate** (proposed by this run, nothing accepted): `../candidate/` — a copy of the curation and configuration with ADD-03 added, its evidence build, its op file, rows, issues, templates and outputs.
- **Last validated state**: `../candidate/out-before/` (the pre-addendum outputs built from the copied curation and the previous evidence build; done)
- **Real** (untouched): `curation/`, `config/`, `out/`; the owner's approvals and readings were copied unchanged and used read-only.

- real inputs changed since the run started: none

## Candidate outputs

Exit 0 (INTERVIEW DEMO (assumed approvals; not a tender release)); every file carries the banner (`../candidate/out/CANDIDATE.md`); A1 has a candidate status column {'DECIDED': 203, 'UNRESOLVED': 7}.

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

- before → after: {"a1": {"rows_before": 205, "rows_after": 210, "new": 5, "gone": 0}, "a3": {"before": 17, "after": 17, "enters": 0, "leaves": 0}, "a5": {"activities_before": 44, "activities_after": 44, "new": 0, "gone": 0}}

- ADD-03 is **PARTIAL** in the candidate (provisions unresolved): A3 and the A5 programme show the validated state (ADD-02); ADD-03 as proposed is in A1's `Status after ADD-03` column, in A2, in the candidate A3 and A5 below, in `a5/working/ADD-03.json` and in the diff below.

### Validated and candidate A3 / A5 (partial should not mean useless)

- **Validated** (unchanged; ADD-02): [a3/a3.pdf](../candidate/out/a3/a3.pdf) (one page), [a5/README.md](../candidate/out/a5/README.md), [a5/gantt.html](../candidate/out/a5/gantt.html)
- **Candidate** (CANDIDATE — NOT VALIDATED; ADD-03 as proposed): [a3/a3_candidate.pdf](../candidate/out/a3/a3_candidate.pdf) (7 page(s)), [a3/a3_candidate.md](../candidate/out/a3/a3_candidate.md), [a5/candidate/README.md](../candidate/out/a5/candidate/README.md), [a5/candidate/gantt.html](../candidate/out/a5/candidate/gantt.html)

**What may be changing.** ADD-03 is PARTIAL: 3 of 19 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 14 op(s) that are valid there stood (each still a proposal: review accepted 14), A3 would gain 0 row(s) (none), lose 1 (ADD-02-7.2-01 (ADD-03/3.1(b))) and change 5 (ADD-02-F4G-04 (register), VOL-I-6.1-01 (ADD-03/2.1(a), ADD-03/2.1(b)), VOL-I-6.3-01 (ADD-03/5.2(a)), VOL-I-6.4-01 (ADD-03/5.1) and 1 more); A5, replanned at ADD-03's issue date (2026-11-08), would move the latest dates of 43 activities (assemble-envelope-a, assemble-envelope-b, bond-approval, bond-issue and 39 more), add 0 (none) and remove 0 (none), and marks 17 REVIEW through relationships. Not settled: 5 activities blocked by an unresolved row (fin-model-build, fin-model-freeze, form-4g-review, form-4f and 1 more), 7 STALE row(s), 0 obligation(s) reaching no output (C46), 8 relationship chain(s) blocked or incomplete, 1 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT and 7 more. Nothing here is validated, accepted or applied to the real state.

- CHANGES ADD-02-F4G-04: now STALE; ops none (status NEW -> ACTIVE (as amended by ADD-02/7.1); NOT SETTLED: STALE at ADD-03: its reading was not re-made (ADD-02:7.2 changed since ADD-02 (by ADD-03/3.1(b))))
- CHANGES VOL-I-6.1-01: text: “Deliver the Proposal to the Authority by the Proposal Due Date and time, at the Appendix 3 address — “Thursday 26 Novem…” -> “Deliver the Proposal to the Authority by the Proposal Due Date and time, at the Appendix 3 address — “Proposals shall b…”; ops ADD-03/2.1(a) (evidence_verified), ADD-03/2.1(b) (interpretation_pending)
- CHANGES VOL-I-6.3-01: text: “Bid Bond valid for two hundred and ten (210) days from the Proposal Due Date and extended on demand where the Authority…” -> “Bid Bond valid for two hundred and ten (210) days from the Proposal Due Date and extended on demand where the Authority…”; ops ADD-03/5.2(a) (evidence_verified)
- CHANGES VOL-I-6.4-01: text: “Bid Bond of SAR 5,600,000, unconditional and payable on first written demand — “in the amount of SAR 4,500,000”” -> “Bid Bond of SAR 5,600,000, unconditional and payable on first written demand”; ops ADD-03/5.1 (evidence_verified)
- CHANGES VOL-I-8.5-01: text: “Evidence at least two (2) reference sewage treatment plants of at least 100,000 m3/day, each having achieved commercial…” -> “Evidence at least two (2) reference sewage treatment plants of at least 100,000 m3/day, each having achieved commercial…”; ops ADD-03/4.2 (evidence_verified)
- LEAVES ADD-02-7.2-01: was explicit (non-responsive); ops ADD-03/3.1(b) (evidence_verified)

- blockers: 3 unresolved provision(s), 5 blocked activit(y/ies), 7 STALE row(s), 0 C46 gap(s), 8 relationship chain(s) blocked or incomplete, 1 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT, I-VOL-III, I-ADD-03-DS009-FLOW-ANSWER, I-VOL-II-MISSING, I-VOL-V-MISSING, I-VOL-II-COMPLIANCE-POINT, I-VOL-IV-SCALE, I-OP-ADD-01/Q4
- conditional scenarios: 0

**Image-read units** (the review packet of each region shows every crop beside its reading; translations are proposals, not evidence):

- VOL-II-p3-r1 (VOL-II p3; reading approved): [packet](../candidate/build/review/VOL-II-p3-r1/packet.html); 5 unit(s) touched
  - `VOL-II:T2-4/BOD5`: “Parameter: Biochemical Oxygen Demand (BOD5) / Unit: mg/l / Limit: 10 / Basis of assessment: 30-day rolling average”; unit mg/l; issues I-PERMIT, I-READING-T24, I-VOL-II-COMPLIANCE-POINT
  - `VOL-II:T2-4/COD`: “Parameter: Chemical Oxygen Demand (COD) / Unit: mg/l / Limit: 50 / Basis of assessment: 30-day rolling average”; unit mg/l; issues I-PERMIT, I-READING-T24, I-VOL-II-COMPLIANCE-POINT
  - `VOL-II:T2-4/TSS`: “Parameter: Total Suspended Solids (TSS) / Unit: mg/l / Limit: 10 / Basis of assessment: 30-day rolling average”; unit mg/l; issues I-PERMIT, I-READING-T24, I-VOL-II-COMPLIANCE-POINT
  - `VOL-II:T2-4/TN`: “Parameter: Total Nitrogen (TN) / Unit: mg/l / Limit: 5 / Basis of assessment: 30-day rolling average”; unit mg/l; issues I-PERMIT, I-READING-T24, I-VOL-II-COMPLIANCE-POINT
  - `VOL-II:T2-4/TP`: “Parameter: Total Phosphorus (TP) / Unit: mg/l / Limit: 1 / Basis of assessment: 30-day rolling average”; unit mg/l; issues I-PERMIT, I-READING-T24, I-VOL-II-COMPLIANCE-POINT
- VOL-IV-p6-r1 (VOL-IV p6; reading approved): [packet](../candidate/build/review/VOL-IV-p6-r1/packet.html); not touched by this addendum

## Timings (wall clock per step)

| Step | Seconds | Status |
|---|---|---|
| ingest | 9.6 | done |
| readings | 0.0 | done |
| analysis | 565.8 | done |
| validation | 3.0 | done |
| downstream | 3475.2 | done |
| downstream_validation | 0.4 | done |
| critic | 159.0 | done |
| promotion | 8.7 | done |
| pin | 0.6 | done |
| check_register | 2.1 | done |
| outputs | 10.7 | done |
| diff | 1.9 | done |
| review | 0.0 | running |
| **total** | **4237.0** (70.6 min) | target 30 min from the PDF to candidate outputs and this packet, human review excluded |

## First: unresolved provisions and escalations

5 of 19 provisions are not applied or settled by a promoted item (each is `unresolved` in the candidate op file with the reason); 5 escalation(s).
- states (session 14: kept distinct): applied 10, no effect 4, partly applied 2, unresolved but accounted for 3, unaccounted 0; approved by a person: none (only a person's recorded decision approves; see Human approval above)

- **ESCALATED ADD-03/2.2** (ADD-03:2.2): software limitation: ADD-03:2.2 states 'Every period calculated by reference to the Proposal Due Date is adjusted accordingly.' The amendment engine rejected annotate targets VOL-I:5.2, VOL-I:6.3, VOL-I:7.1 and VOL-I:8.5#fn12 with C22 'not cited' because this provision identifies the affected perio…
  - unsupported: Applying a collectively scoped period adjustment to evidenced PDD-dependent units without explicit clause citations: simulate_amendment C22 cannot represent this targeting. The listed follow-on work must remain available for human review and the date/register/programme phases.
  - evidence: ADD-03:2.2 p1: “Every period calculated by reference to the Proposal Due Date is adjusted accordingly.”; VOL-I:2.6 p2: “Proposal Due Date means the date and time stated in Clause 6.1, as the same may be amended by Addendum.”; VOL-I:5.2 p3: “Requests for clarification shall be submitted no later than ten (10) Working Days before the Proposal Due Date. Requests received after that time will not be a…”; VOL-I:6.3 p3: “Envelope A shall be accompanied by a Bid Bond which shall remain valid for one hundred and eighty (180) days from the Proposal Due Date and shall be extended o…”; VOL-I:7.1 p4: “Each Proposal shall remain open for acceptance for one hundred and fifty (150) days from the Proposal Due Date.”; VOL-I:8.5#fn12 p4: “For the avoidance of doubt, a Bidder that does not evidence at least two (2) reference sewage treatment plants, each of nominal capacity not less than 80,000 m…”
  - affected scope: units none; rows none; activities none; clarifications none
- **ESCALATED ADD-03/3.1(a)-escalation** (ADD-03:3.1): software limitation: the provision states ‘Form 4-G (Cybersecurity Compliance Undertaking), added by Addendum No. 2 Section 7, is withdrawn.’ The form is supplied as group ADD-02:F4-G; set_status on that group fails C22 target existence, and set_status on its heading fails C22 citation. Document co…
  - unsupported: Group withdrawal with set_status and citation of the group's member units. The form's heading, table headings, undertaking rows (including Item, Undertaking and Confirmed cells) and signature field are all included in the evidence. Do not substitute revocation of the whole Section 7. Follow-on: ins…
  - evidence: ADD-03:3.1 p1: “Form 4-G (Cybersecurity Compliance Undertaking), added by Addendum No. 2 Section 7, is withdrawn. Bidders shall disregard it and shall not submit it. Section 7…”; ADD-02:H:F4-G p3: “FORM 4-G — CYBERSECURITY COMPLIANCE UNDERTAKING”; ADD-02:F4-G/T1 p3: “Item | Undertaking | Confirmed”; ADD-02:F4-G/T1/1 p3: “Item: 1 | Undertaking: The operational technology environment will be segregated from any business network in accordance with Volume II Clause 6.2. | Confirmed…”; ADD-02:F4-G/T1/2 p3: “Item: 2 | Undertaking: An information security management system covering the operational technology environment will be implemented before commissioning. | Co…”; ADD-02:F4-G/T1/3 p3: “Item: 3 | Undertaking: A named accountable security officer will be appointed for the concession period. | Confirmed: Yes / No”; ADD-02:F4-G/T1/4 p3: “Item: 4 | Undertaking: Security incidents affecting the Facility will be notified to the Authority within twenty-four (24) hours of detection. | Confirmed: Yes…”; ADD-02:F4-G/T1/5 p3: “Item: 5 | Undertaking: An independent penetration test of the operational technology environment will be carried out annually and the report provided to the Au…”; ADD-02:F4-G/T1/6 p3: “Item: 6 | Undertaking: Remote access to the control system will require multi-factor authentication and will be logged. | Confirmed: Yes / No”; ADD-02:F4-G/para1 p3: “Signed for and on behalf of the Bidder: _______________________ Name: _______________________ Date: ____________”; ADD-02:7.1 p3: “A new Form 4-G is added to Volume IV and to the list at Volume I Clause 9.1, to be inserted after item (e).”; VOL-I:9.1(e)+ADD-02 p3: “FORM 4-G — CYBERSECURITY COMPLIANCE UNDERTAKING”
  - affected scope: units ADD-02:7.2, ADD-02:F4-G/T1, ADD-02:F4-G/T1/1, ADD-02:F4-G/T1/2, ADD-02:F4-G/T1/3, ADD-02:F4-G/T1/4, ADD-02:F4-G/T1/5, ADD-02:F4-G/T1/6, ADD-02:F4-G/para1, ADD-02:H:F4-G, ADD-02:H:S7; rows ADD-02-7.2-01, ADD-02-F4G-01, ADD-02-F4G-02, ADD-02-F4G-03, ADD-02-F4G-04, ADD-02-F4G-05, ADD-02-F4G-06, ADD-02-F4G-07; activities form-4g-review, form-4g-sign; clarifications none
- **ESCALATED ADD-03/4.1(b)-escalation** (ADD-03:4.1): software limitation: The printed replacement ‘120,000 m³/day’ to ‘150,000 m³/day’ expressly names Table 2-6 row 2-6.1. set_value of its Value cell to the printed numeric component 150,000 fails C22 because the engine recognises only VOL-II:2.1 as cited. Document control owns correction of the citat…
  - unsupported: Recognition of the explicitly printed Table 2-6 row citation. Keep row 2-6.1 Value and row 2-6.2 Value distinct, with their respective Unit cells. No substitute target or neighbouring cell change is proposed.
  - evidence: ADD-03:4.1 p1: “In Volume II Clause 2.1 and in Table 2-6 row 2-6.1, ‘120,000 m³/day’ is deleted and ‘150,000 m³/day’ is substituted. The peak hourly flow in Table 2-6 row 2-6.…”; VOL-II:T2-6/2-6.1 p3: “Ref: 2-6.1 | Criterion: Average daily flow | Value: 120,000 | Unit: m³/day”; VOL-II:T2-6/2-6.1 p3: “Average daily flow”; VOL-II:T2-6/2-6.1 p3: “2-6.1”; VOL-II:T2-6/2-6.1 p3: “m³/day”; VOL-II:T2-6/2-6.1 p3: “120,000”
  - affected scope: units VOL-II:2.1; rows VOL-II-2.1-01; activities technical-proposal; clarifications none
- **ESCALATED ADD-03/4.1(c)-escalation** (ADD-03:4.1): software limitation: The provision expressly states ‘The peak hourly flow in Table 2-6 row 2-6.2 is unchanged.’ An annotate/confirms operation on that row fails C22 because the engine does not recognise its citation. Document control owns correction of the citation mapping; Technical reviews the re…
  - unsupported: Recognition of the explicitly printed Table 2-6 row citation. Keep row 2-6.1 Value and row 2-6.2 Value distinct, with their respective Unit cells. No substitute target or neighbouring cell change is proposed.
  - evidence: ADD-03:4.1 p1: “In Volume II Clause 2.1 and in Table 2-6 row 2-6.1, ‘120,000 m³/day’ is deleted and ‘150,000 m³/day’ is substituted. The peak hourly flow in Table 2-6 row 2-6.…”; VOL-II:T2-6/2-6.2 p3: “Ref: 2-6.2 | Criterion: Peak hourly flow (design) | Value: 7,500 | Unit: m³/h”; VOL-II:T2-6/2-6.2 p3: “Peak hourly flow (design)”; VOL-II:T2-6/2-6.2 p3: “2-6.2”; VOL-II:T2-6/2-6.2 p3: “m³/h”; VOL-II:T2-6/2-6.2 p3: “7,500”
  - affected scope: units VOL-II:2.1; rows VOL-II-2.1-01; activities technical-proposal; clarifications none
- **ESCALATED ADD-03/Q17-coverage** (ADD-03:Q17): software limitation: validate_proposal accepts the well-formed row_new ADD-03/Q17, verifies its quotation and reports it ready with interpretation_pending, but still lists ADD-03:Q17 as UNACCOUNTED in amendment coverage. The source obligation is "Bidders shall price the Project as amended by this A…
  - unsupported: Accounting for a free-standing addendum obligation through row_new alone in the amendment-coverage result. Retain the accompanying row proposal for human review; do not substitute a guessed volume amendment or no_effect disposition.
  - evidence: ADD-03:Q17 p2: “No: 17 | Bidder question: Will the Availability Payment be adjusted for the increased capacity? | Authority response: Bidders shall price the Project as amende…”
  - affected scope: units none; rows none; activities none; clarifications none
- **UNRESOLVED ADD-03:4.3** (clause, p1): unresolved (accounted for by the promoted `unresolved` disposition ADD-03/4.3-unresolved; nothing applied): insufficient evidence: ADD-03:4.3 states ‘Volume I Clause 1.3 is amended correspondingly.’ After reading that provision, ADD-03:4.1 and VOL-I:1.3 at ADD-02, no exact replacement text is supplied for ‘one hundred and twenty thousand cubic metres per day (120,000 m³/day)’. The target is identified, but a literal replacement of the complete worded and numeric phrase cannot be quoted from this provis…

## Earlier answers to re-read against the new text (never revoked; a person decides)

- `ADD-01:Q1` (ADD-01): relies on VOL-II:3.1, which VOL-II:T2-4/TP (changed by ADD-03/7.1) governs through REL-T24-PROCESS-DESIGN; relies on VOL-II:3.1, which VOL-II:T2-4/TP (changed by ADD-03/7.1) governs through REL-AI-007; to be re-read against the new text of VOL-II:T2-4/TP (ADD-03/7.1); a person decides whether the answer still holds (downstream task `reread:ADD-01:Q1`)
- `ADD-01:Q3` (ADD-01): cites VOL-I:6.4, changed by ADD-03/5.1; to be re-read against the new text of VOL-I:6.4 (ADD-03/5.1); a person decides whether the answer still holds (downstream task `reread:ADD-01:Q3`)
- `ADD-01:Q5` (ADD-01): cites VOL-I:8.5#fn12, changed by ADD-03/4.2; to be re-read against the new text of VOL-I:8.5#fn12 (ADD-03/4.2); a person decides whether the answer still holds (downstream task `reread:ADD-01:Q5`)
- `ADD-01:Q6` (ADD-01): relies on VOL-V:29.3, which VOL-II:T2-4/TP (changed by ADD-03/7.1) governs through REL-AI-007; to be re-read against the new text of VOL-II:T2-4/TP (ADD-03/7.1); a person decides whether the answer still holds
- `ADD-02:Q7` (ADD-02): relies on VOL-I:12.1, which VOL-I:11.5+ADD-03 (changed by ADD-03/6.1) governs through REL-AI-010; to be re-read against the new text of VOL-I:11.5+ADD-03 (ADD-03/6.1); a person decides whether the answer still holds
- `ADD-02:Q8` (ADD-02): cites VOL-I:6.4, changed by ADD-03/5.1; to be re-read against the new text of VOL-I:6.4 (ADD-03/5.1); a person decides whether the answer still holds (downstream task `reread:ADD-02:Q8`)
- `ADD-02:Q11` (ADD-02): quotes '120,000 m³/day', a figure ADD-03/4.1(a) replaced; to be re-read against the new text of VOL-II:2.1 (ADD-03/4.1(a)); a person decides whether the answer still holds (downstream task `reread:ADD-02:Q11`)
- `ADD-02:Q13` (ADD-02): relies on VOL-I:12.2, which VOL-I:11.5+ADD-03 (changed by ADD-03/6.1) governs through REL-AI-010; relies on VOL-I:12.2, which VOL-I:11.5+ADD-03 (changed by ADD-03/6.1) governs through REL-AI-010; to be re-read against the new text of VOL-I:11.5+ADD-03 (ADD-03/6.1); a person decides whether the answer still holds

## Derived effects (session 12: pending readings, computed deadlines, conditions, consequences)

## Computed deadlines and the Working Days left (PROPOSED; nothing typed)

- Working Days left from the issue date (2026-11-08) to the PDD (2026-12-10): 24 (the issue date not counted, the PDD counted; Working Days per VOL-I 2.4 (weekend [4, 5] as date.weekday numbers; holidays none declared))
- no 'N days before/after' deadline in the addendum's provisions

## Conditional impact investigations (CONDITIONAL; never accepted facts)

- `impact:ADD-03:4.3` conditional on disposition ADD-03:4.3 (unresolved: insufficient evidence: ADD-03:4.3 states ‘Volume I Clause 1.3 is amended correspondingly.’ After reading that provision, ADD-03:4.1 and VOL-I:1.3 at ADD-02, no exact replacement text is supplied for …): investigate the rows, activities and prices that rest on VOL-I:1.3
- `impact:ADD-03:2.2` conditional on disposition ADD-03:2.2 (unresolved: escalated: software limitation: ADD-03:2.2 states 'Every period calculated by reference to the Proposal Due Date is adjusted accordingly.' The amendment engine rejected annotate targets VOL-I:5.2, VO…): investigate the rows, activities and prices that rest on the provision ADD-03:2.2
- `impact:ADD-03:Q17` conditional on disposition ADD-03:Q17 (unresolved: escalated: software limitation: validate_proposal accepts the well-formed row_new ADD-03/Q17, verifies its quotation and reports it ready with interpretation_pending, but still lists ADD-03:Q17 as UN…): investigate the rows, activities and prices that rest on the provision ADD-03:Q17

## Per provision: source evidence → proposed transition → validation → downstream impact → output difference

### ADD-03:cover/para1 (paragraph, p1) — no effect (PROPOSED; not approved)
- source: “Issued 8 November 2026”
- transition: `ADD-03/cover/para1` disposition no_effect: “Issued 8 November 2026” identifies the issue date; it contains no amendment or bidder obligation. Retain it as stage-date evidence.
  - validation: **evidence_verified**

### ADD-03:cover/para2 (paragraph, p1) — no effect (PROPOSED; not approved)
- source: “Tender NUPA/ISTP/2026/014”
- transition: `ADD-03/cover/para2` disposition no_effect: “Tender NUPA/ISTP/2026/014” identifies the tender; it contains no amendment or bidder obligation.
  - validation: **evidence_verified**

### ADD-03:cover/para3 (paragraph, p1) — applied (PROPOSED; not approved)
- source: “This Addendum amends the Proposal Due Date and Bid Bond, withdraws Form 4-G, increases the nominal capacity with a consequential change to the reference project threshold, amends Table 2-4, adds a new Clause 11.6, and responds to clarification requests 15 to 18. This Addendum forms part of the RFP Documents and takes precedence in accordance with Volume I C…”
- transition: `ADD-03/cover/para3` amendment_op annotate ADD-03:cover/para3 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model codex exec (configured gpt-6-astra; runtime identity recorded separately)
- transition: `ADD-03/cover/para3/acknowledgement-row` row_new {"row": {"id": "ADD-03-cover-acknowledgement-01", "group": "Addendum acknowledgement", "scope": ["bid"], "requirement": "Bidders shall acknowledge receipt in Form 4-A.", "units": ["ADD-03:cover/para3…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model codex exec (configured gpt-6-astra; runtime identity recorded separately)
  - downstream proposal `ADD-03-D004-ACK-ROW` row_new (c46:ADD-03/cover/para3): **interpretation_pending**
  - downstream proposal `ADD-03-D004-ACK-FOLLOW` dependency (c46:ADD-03/cover/para3): **insufficient_evidence** — held back: endpoints not promotable: ['form-4a']
  - downstream proposal `ADD-03-D004-FORM-ISSUE` issue (c46:ADD-03/cover/para3): **insufficient_evidence — HUMAN DECISION PENDING**
  - output difference: NEW ADD-03-cover-01; A5 REWORK form-4a; A5 REWORK form-4a-prep

### ADD-03:1.1 (clause, p1) — applied (PROPOSED; not approved)
- source: “This Addendum takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.”
- transition: `ADD-03/1.1` amendment_op annotate VOL-I:3.2 effect confirms
  - validation: **interpretation_pending — HUMAN DECISION PENDING — applied rule: ADD-03 1.1 provides: 'This Addendum takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.' (applied, not decided); a person confirms the application**

### ADD-03:2.1 (clause, p1) — applied (PROPOSED; not approved)
- source: “Volume I Clause 6.1 is amended by deleting ‘Thursday 26 November 2026’ and substituting ‘Thursday 10 December 2026’, 14:00 Riyadh time.”
- transition: `ADD-03/2.1(a)` amendment_op replace_text VOL-I:6.1 “Thursday 26 November 2026” → “Thursday 10 December 2026”
  - validation: **evidence_verified**
- transition: `ADD-03/2.1(b)` amendment_op annotate VOL-I:6.1 effect confirms
  - validation: **interpretation_pending**
- transition: `ADD-03/2.1/form-date-review` issue {"owner": "Document control", "short": "Revised Form 4-A prints an earlier due date", "theme": "Form and clause discrepancy", "text": "ambiguous: ADD-03:2.1 substitutes 'Thursday 10 December 2026' in…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model codex exec (configured gpt-6-astra; runtime identity recorded separately)
  - downstream: units changed VOL-I:6.1; rows citing them VOL-I-6.1-01
  - downstream proposal `D-ADD-03-OMISSION` row_reading (row:VOL-I-3.4-01): **interpretation_pending**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation
  - downstream proposal `D-ADD-03-CLARIFICATION` row_reading (row:VOL-I-5.2-01): **interpretation_pending**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation
      - concern: insufficient evidence: the relative deadline rule and consequence are supported, but no calculate(deadline) result is printed to substantiate the claimed calculation confirmation. VOL-I:2.4 supports excluding the stated date; provide the calculation record or attribute that reading directly to the …
  - downstream proposal `D-ADD-03-DELIVERY` row_reading (row:VOL-I-6.1-01): **interpretation_pending**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation
      - concern: insufficient evidence: the amended deadline, retained time and address reference, and rejection consequence are supported. However, no activity records or supporting clauses establish the named seal-and-mark, copies, assemble-envelope-a and assemble-envelope-b activities or their dependencies under…
  - downstream proposal `D-ADD-03-LINK-DELIVERY` dependency (row:VOL-I-6.1-01): **insufficient_evidence** — held back: endpoints not promotable: ['copies', 'assemble-envelope-b']
  - downstream proposal `D003-READ-3` row_reading (row:VOL-I-6.7-01): **interpretation_pending**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation
  - downstream proposal `D003-READ-5` row_reading (row:VOL-I-8.3-01): **interpretation_pending**
  - downstream proposal `D003-LINK-3` dependency (row:VOL-I-6.7-01): **interpretation_pending**
  - downstream proposal `D003-LINK-5` dependency (row:VOL-I-8.3-01): **interpretation_pending**
  - downstream proposal `P-ADD03-D006-DELIVER` activity (act:deliver): **interpretation_pending**
  - downstream proposal `DS009-DATE-PROPAGATION` escalation (impact:2. AMENDMENT TO THE PROPOSAL DUE DATE): **escalated**
  - downstream proposal `DS009-FORM-DATE` issue (impact:2. AMENDMENT TO THE PROPOSAL DUE DATE): **interpretation_pending — HUMAN DECISION PENDING**
  - output difference: CHANGED VOL-I-6.1-01; CHANGED VOL-I-5.2-01; CHANGED VOL-I-8.3-01; CHANGED VOL-I-3.4-01; CHANGED VOL-I-6.7-01; A5 REWORK assemble-envelope-a; A5 REWORK assemble-envelope-b; A5 REWORK clarifications; A5 REWORK copies; A5 REWORK deliver; A5 REWORK iso-copy; A5 REWORK seal-and-mark; A5 REVIEW (proposed relationship) assemble-envelope-a; A5 REVIEW (proposed relationship) assemble-envelope-b; A5 REVIEW (proposed relationship) copies; A5 REVIEW (proposed relationship) deliver; A5 REVIEW (proposed relationship) seal-and-mark

### ADD-03:2.2 (clause, p1) — UNRESOLVED (accounted for, not applied)
- source: “Every period calculated by reference to the Proposal Due Date is adjusted accordingly.”
- transition: `ADD-03/2.2` escalation why: software limitation: ADD-03:2.2 states 'Every period calculated by reference to the Proposal Due Date is adjusted accordingly.' The amendment engine rejected annotate targets VOL-I:5.2, VOL-I:6.3, VO…
  - validation: **escalated**
- transition: `ADD-03/2.2/propagation-review` issue {"owner": "Bid management", "short": "Propagate the amended Proposal Due Date", "theme": "Date rules and bid programme", "text": "Review and carry forward the instruction 'Every period calculated by …
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model codex exec (configured gpt-6-astra; runtime identity recorded separately)
    - concern: insufficient evidence: the printed records support the listed PDD-linked requirements, but contain no activities or programme simulation results supporting the specifically named A5 activity chain.
    - concern: insufficient evidence: no printed controller record supports the rationale's claim that the engine cannot annotate this scope. The claimed software limitation cannot be verified.
    - concern: The controller's keyword flags do not reflect the issue's meaning: it expressly leaves questions unanswered and unwithdrawn.
  - downstream proposal `D008-PDD-ESC` escalation (esc:ADD-03:2.2): **escalated**
  - downstream proposal `DS009-DATE-PROPAGATION` escalation (impact:2. AMENDMENT TO THE PROPOSAL DUE DATE): **escalated**
  - downstream proposal `DS009-FORM-DATE` issue (impact:2. AMENDMENT TO THE PROPOSAL DUE DATE): **interpretation_pending — HUMAN DECISION PENDING**

### ADD-03:3.1 (clause, p1) — PARTLY APPLIED (an escalated sibling stays unresolved)
- source: “Form 4-G (Cybersecurity Compliance Undertaking), added by Addendum No. 2 Section 7, is withdrawn. Bidders shall disregard it and shall not submit it. Section 7.2 of Addendum No. 2 ceases to have effect.”
- transition: `ADD-03/3.1(b)` amendment_op set_status ADD-02:7.2
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): agrees — selected because removal; model codex exec (configured gpt-6-astra; runtime identity recorded separately)
- transition: `ADD-03/3.1(a)-escalation` escalation why: software limitation: the provision states ‘Form 4-G (Cybersecurity Compliance Undertaking), added by Addendum No. 2 Section 7, is withdrawn.’ The form is supplied as group ADD-02:F4-G; set_status on …
  - validation: **escalated**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is a group; model codex exec (configured gpt-6-astra; runtime identity recorded separately)
    - concern: The withdrawal and identified form members are supported. However, the asserted C22 failures are not printed in the controller records; those records verify only payload structure and quotations. The claimed software limitation cannot be independently verified without the failed simulation records.
- transition: `ADD-03/3.1-nonsubmission-row` row_new {"row": {"id": "ADD-03-3.1-01", "group": "ADD-03 Section 3", "scope": ["bid"], "requirement": "Bidders shall disregard it and shall not submit it.", "units": ["ADD-03:3.1"], "discipline": "Bid manage…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model codex exec (configured gpt-6-astra; runtime identity recorded separately)
- transition: `ADD-03/3.1-list-review` issue {"owner": "Document control", "short": "Carry form withdrawal into the inserted Envelope A entry", "text": "ADD-03:3.1 states: Form 4-G (Cybersecurity Compliance Undertaking), added by Addendum No. 2…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model codex exec (configured gpt-6-astra; runtime identity recorded separately)
  - downstream: units changed ADD-02:7.2; rows citing them ADD-02-7.2-01
  - downstream proposal `DS-F4G-SUBMISSION-RECONCILIATION` issue (row:ADD-02-7.2-01): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-F4G-01-WITHDRAWAL` issue (row:ADD-02-F4G-01): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-F4G-02-WITHDRAWAL` issue (row:ADD-02-F4G-02): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-F4G-03-WITHDRAWAL` issue (row:ADD-02-F4G-03): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-F4G-04-WITHDRAWAL` issue (row:ADD-02-F4G-04): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-F4G-05-WITHDRAWAL` issue (row:ADD-02-F4G-05): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-ADD-02-F4G-06-WITHDRAWAL` issue (row:ADD-02-F4G-06): **insufficient_evidence — HUMAN DECISION PENDING**
  - downstream proposal `D-ADD-02-F4G-07-WITHDRAWAL` issue (row:ADD-02-F4G-07): **insufficient_evidence — HUMAN DECISION PENDING**
  - downstream proposal `ADD-03-3.1-01-proposal` row_new (ana:ADD-03/3.1-nonsubmission-row): **interpretation_pending**
  - downstream proposal `P-ADD03-D006-ENVELOPE-A-GAP` escalation (act:assemble-envelope-a): **conflicting**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting
      - concern: insufficient evidence: the request does not print the promoted operations or assembly template. The assertions that an operation only revokes ADD-02:7.2 and that assemble-envelope-a still includes Form 4-G cannot be verified. The printed ADD-02 register establishes the previous-stage contents, not …
      - concern: ADD-03:3.1 expressly withdraws Form 4-G and prohibits submission. Any uncertainty should concern implementation of that instruction, without implying that the withdrawal itself lacks evidence.
      - concern: The item declares I-VOL-I-ENV-A-PRICES as a conflict without showing how Form 4-G withdrawal affects that separate issue.
  - downstream proposal `D008-F4G-ESC` escalation (esc:ADD-03:3.1): **escalated**
  - downstream proposal `D008-F4G-HANDLING` escalation (esc:ADD-03:3.1): **escalated**
  - downstream proposal `DS009-F4G-WITHDRAWAL` escalation (impact:3. WITHDRAWAL OF FORM 4-G): **escalated**
  - output difference: NEW ADD-03-3.1-01; OUT ADD-02-7.2-01

### ADD-03:3.2 (clause, p1) — applied (PROPOSED; not approved)
- source: “The substantive requirements of Volume II Section 6 are unchanged and shall be addressed in the Technical Proposal narrative.”
- transition: `ADD-03/3.2(a)` amendment_op annotate VOL-II:S6 effect confirms
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is a group; model codex exec (configured gpt-6-astra; runtime identity recorded separately)
    - concern: The rationale states that VOL-II:S6 contains only its heading. Annotating that group does not establish that the confirmation reaches substantive clauses VOL-II:6.1–6.3. Explicitly target those clauses or provide validation showing that the group annotation covers them; the successful dry run does …
- transition: `ADD-03/3.2-narrative-row` row_new {"row": {"id": "ADD-03-3.2-01", "group": "ADD-03 Section 3", "scope": ["bid"], "requirement": "The substantive requirements of Volume II Section 6 are unchanged and shall be addressed in the Technica…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model codex exec (configured gpt-6-astra; runtime identity recorded separately)
  - downstream proposal `ADD-03-3.2-01-proposal` row_new (ana:ADD-03/3.2-narrative-row): **interpretation_pending**
  - downstream proposal `ADD-03-3.2-programme` dependency (ana:ADD-03/3.2-narrative-row): **interpretation_pending**
  - output difference: NEW ADD-03-3.2-01; A5 REWORK technical-proposal; A5 REVIEW (proposed relationship) technical-proposal

### ADD-03:4.1 (clause, p1) — PARTLY APPLIED (an escalated sibling stays unresolved)
- source: “In Volume II Clause 2.1 and in Table 2-6 row 2-6.1, ‘120,000 m³/day’ is deleted and ‘150,000 m³/day’ is substituted. The peak hourly flow in Table 2-6 row 2-6.2 is unchanged.”
- transition: `ADD-03/4.1(a)` amendment_op replace_text VOL-II:2.1 “120,000 m³/day” → “150,000 m³/day”
  - validation: **evidence_verified**
- transition: `ADD-03/4.1(b)-escalation` escalation why: software limitation: The printed replacement ‘120,000 m³/day’ to ‘150,000 m³/day’ expressly names Table 2-6 row 2-6.1. set_value of its Value cell to the printed numeric component 150,000 fails C22 b…
  - validation: **escalated**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model codex exec (configured gpt-6-astra; runtime identity recorded separately)
    - concern: The provision expressly identifies row 2-6.1 and supports changing only its Value cell to 150,000 while retaining m³/day. However, no failed simulation or citation-mapping record is printed to substantiate the asserted C22 software limitation; payload validation alone does not verify it.
- transition: `ADD-03/4.1(c)-escalation` escalation why: software limitation: The provision expressly states ‘The peak hourly flow in Table 2-6 row 2-6.2 is unchanged.’ An annotate/confirms operation on that row fails C22 because the engine does not recogn…
  - validation: **escalated**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model codex exec (configured gpt-6-astra; runtime identity recorded separately)
    - concern: The provision expressly confirms that row 2-6.2 is unchanged. However, no failed simulation or citation-mapping record is printed to substantiate the asserted C22 software limitation; payload validation alone does not verify it.
- transition: `ADD-03/4.1-flow-review` issue {"owner": "Technical", "short": "Re-read the earlier flow answer against the amended daily flow", "text": "ADD-03:4.1 states: In Volume II Clause 2.1 and in Table 2-6 row 2-6.1, ‘120,000 m³/day’ is d…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model codex exec (configured gpt-6-astra; runtime identity recorded separately)
    - concern: Correct the rationale's attribution: the former daily figure appears in the bidder question, not the Authority response. The changed premise nevertheless supports the proposed human review without establishing a conflict or withdrawing the earlier answer.
  - downstream: units changed VOL-II:2.1; rows citing them VOL-II-2.1-01
  - downstream proposal `ADD-03-D004-CAPACITY` row_reading (row:VOL-II-2.1-01): **interpretation_pending**
  - downstream proposal `ADD-03-D004-CAPACITY-FOLLOW` dependency (row:VOL-II-2.1-01): **interpretation_pending**
  - downstream proposal `D008-FLOWS-ESC` escalation (esc:ADD-03:4.1): **escalated**
  - downstream proposal `DS009-CAPACITY-WORDING` escalation (impact:4. AMENDMENT TO NOMINAL CAPACITY): **escalated**
  - downstream proposal `DS009-FLOW-TARGETS` escalation (impact:4. AMENDMENT TO NOMINAL CAPACITY): **escalated**
  - downstream proposal `DS009-FLOW-ANSWER` issue (impact:4. AMENDMENT TO NOMINAL CAPACITY): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-REREAD-ADD02-Q11` issue (reread:ADD-02:Q11): **interpretation_pending — HUMAN DECISION PENDING**
  - output difference: CHANGED VOL-II-2.1-01; A5 REWORK technical-proposal

### ADD-03:4.2 (clause, p1) — applied (PROPOSED; not approved)
- source: “Consequentially, footnote 12 to Volume I Clause 8.5 is amended by deleting ‘80,000 m³/day’ and substituting ‘100,000 m³/day’. The requirement for two (2) reference plants and the ten (10) year look-back are unchanged.”
- transition: `ADD-03/4.2` amendment_op replace_text VOL-I:8.5#fn12 “80,000 m³/day” → “100,000 m³/day”
  - validation: **evidence_verified**
  - downstream: units changed VOL-I:8.5#fn12; rows citing them VOL-I-8.5-01
  - downstream proposal `D003-READ-6` row_reading (row:VOL-I-8.5-01): **interpretation_pending**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation
  - downstream proposal `D003-LINK-6` dependency (row:VOL-I-8.5-01): **interpretation_pending**
  - downstream proposal `D-ADD03-D007-REFERENCES` activity (act:references): **interpretation_pending**
  - downstream proposal `DS-REREAD-ADD01-Q5` issue (reread:ADD-01:Q5): **interpretation_pending — HUMAN DECISION PENDING**
  - output difference: CHANGED VOL-I-8.5-01; A5 REWORK references

### ADD-03:4.3 (clause, p1) — UNRESOLVED (accounted for, not applied)
- source: “Volume I Clause 1.3 is amended correspondingly.”
- transition: `ADD-03/4.3-unresolved` disposition unresolved: insufficient evidence: ADD-03:4.3 states ‘Volume I Clause 1.3 is amended correspondingly.’ After reading that provision, ADD-03:4.1 and VOL-I:1.3 at ADD-02, no…
  - validation: **evidence_verified**
- transition: `ADD-03/4.3-wording-question` clarification {"gap": "insufficient evidence: ADD-03:4.3 states ‘Volume I Clause 1.3 is amended correspondingly.’ After reading that provision, ADD-03:4.1 and VOL-I:1.3 at ADD-02, no exact replacement text is supp…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D008-CORRESPOND-ESC` escalation (esc:ADD-03:4.3): **escalated**
  - downstream proposal `DS009-CAPACITY-WORDING` escalation (impact:4. AMENDMENT TO NOMINAL CAPACITY): **escalated**
  - downstream proposal `DS009-FLOW-TARGETS` escalation (impact:4. AMENDMENT TO NOMINAL CAPACITY): **escalated**
  - downstream proposal `DS009-FLOW-ANSWER` issue (impact:4. AMENDMENT TO NOMINAL CAPACITY): **interpretation_pending — HUMAN DECISION PENDING**

### ADD-03:5.1 (clause, p1) — applied (PROPOSED; not approved)
- source: “In Volume I Clause 6.4, ‘SAR 4,500,000 (four million five hundred thousand Saudi Riyals)’ is deleted and ‘SAR 5,600,000 (five million six hundred thousand Saudi Riyals)’ is substituted.”
- transition: `ADD-03/5.1` amendment_op replace_text VOL-I:6.4 “SAR 4,500,000 (four million five hundred thousand Saudi Riyals)” → “SAR 5,600,000 (five million six hundred thousand Saudi Riyals)”
  - validation: **evidence_verified**
  - downstream: units changed VOL-I:6.4; rows citing them VOL-I-6.4-01, VOL-I-6.4-02
  - downstream proposal `D003-READ-1` row_reading (row:VOL-I-6.4-01): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D003-READ-2` row_reading (row:VOL-I-6.4-02): **interpretation_pending**
  - downstream proposal `D003-LINK-1` dependency (row:VOL-I-6.4-01): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-ADD03-D007-BOND-APPROVAL` activity (act:bond-approval): **interpretation_pending**
  - downstream proposal `D-ADD03-D007-BOND-LABEL` escalation (act:bond-issue): **escalated**
  - downstream proposal `DS-REREAD-ADD01-Q3` issue (reread:ADD-01:Q3): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-REREAD-ADD02-Q8` issue (reread:ADD-02:Q8): **interpretation_pending — HUMAN DECISION PENDING**
  - output difference: CHANGED VOL-I-6.4-01; CHANGED VOL-I-6.4-02; A5 REWORK bond-approval; A5 REWORK bond-issue

### ADD-03:5.2 (clause, p1) — applied (PROPOSED; not approved)
- source: “In Volume I Clause 6.3, ‘one hundred and eighty (180) days’ is deleted and ‘two hundred and ten (210) days’ is substituted. The Proposal validity period in Clause 7.1 is unchanged.”
- transition: `ADD-03/5.2(a)` amendment_op replace_text VOL-I:6.3 “one hundred and eighty (180) days” → “two hundred and ten (210) days”
  - validation: **evidence_verified**
- transition: `ADD-03/5.2(b)` amendment_op annotate VOL-I:7.1 effect confirms
  - validation: **evidence_verified**
  - downstream: units changed VOL-I:6.3; rows citing them VOL-I-6.3-01
  - downstream proposal `D-ADD-03-BOND` row_reading (row:VOL-I-6.3-01): **interpretation_pending**
  - downstream proposal `D-ADD-03-BOND-COUNTING` issue (row:VOL-I-6.3-01): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-ADD-03-BOND-RULE-GAP` escalation (row:VOL-I-6.3-01): **escalated**
  - downstream proposal `D-ADD-03-LINK-BOND` dependency (row:VOL-I-6.3-01): **interpretation_pending**
  - downstream proposal `D003-READ-4` row_reading (row:VOL-I-7.1-01): **interpretation_pending**
  - downstream proposal `D003-LINK-4` dependency (row:VOL-I-7.1-01): **insufficient_evidence** — held back: endpoints not promotable: ['form-4a']
  - downstream proposal `D-ADD03-D007-BOND-ISSUE` activity (act:bond-issue): **interpretation_pending**
  - output difference: CHANGED VOL-I-6.3-01; CHANGED VOL-I-7.1-01; A5 REWORK bond-approval; A5 REWORK bond-issue; A5 REWORK form-4a; A5 REWORK form-4a-prep

### ADD-03:6.1 (clause, p1,2) — applied (PROPOSED; not approved)
- source: “A new Clause 11.6 is added to Volume I: ‘11.6 Where, on completion of the combined evaluation, two or more Proposals are within two per cent (2%) of one another, the Authority may apply such further criteria as it considers appropriate to determine the Preferred Bidder, and its determination shall be final.’”
- transition: `ADD-03/6.1` amendment_op insert_unit VOL-I:11.5 “Where, on completion of the combined evaluation, two or more Proposals are within two per cent (2%) of one another, the…”
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model codex exec (configured gpt-6-astra; runtime identity recorded separately)
- transition: `ADD-03/6.1/A1` row_new {"row": {"id": "VOL-I-11.6-01", "group": "Evaluation", "scope": ["bid"], "requirement": "Where, on completion of the combined evaluation, two or more Proposals are within two per cent (2%) of one ano…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model codex exec (configured gpt-6-astra; runtime identity recorded separately)
- transition: `ADD-03/6.1/threshold-issue` issue {"text": "ambiguous: “within two per cent (2%) of one another” does not state whether the comparison is a relative percentage difference between combined scores or an absolute difference in percentag…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model codex exec (configured gpt-6-astra; runtime identity recorded separately)
  - downstream: units changed VOL-I:11.5+ADD-03; rows citing them none
  - downstream proposal `ADD-03-D004-EVAL-ROW` row_new (c46:ADD-03/6.1): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `ADD-03-D004-EVAL-ISSUE` issue (c46:ADD-03/6.1): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `ADD-03-D004-EVAL-FOLLOW` dependency (c46:ADD-03/6.1): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS009-EVALUATION-BASIS` issue (impact:6. NEW VOLUME I CLAUSE 11.6): **interpretation_pending — HUMAN DECISION PENDING**
  - output difference: NEW ADD-03-6.1-01

### ADD-03:7.1 (clause, p2) — applied (PROPOSED; not approved)
- source: “In Volume II Table 2-4, the limit for Total Phosphorus (TP) is amended from the value shown to 0.5 mg/l, assessed on the same basis.”
- transition: `ADD-03/7.1` amendment_op set_value VOL-II:T2-4/TP “” → “0.5”
  - validation: **evidence_verified**
  - downstream: units changed VOL-II:T2-4/TP; rows citing them VOL-II-T2-4-TP, VOL-V-29.3-01
  - downstream proposal `ADD-03-D004-TP` row_reading (row:VOL-II-T2-4-TP): **interpretation_pending**
  - downstream proposal `ADD-03-D004-RAMP` row_reading (row:VOL-V-29.3-01): **interpretation_pending**
  - downstream proposal `ADD-03-D004-TP-FOLLOW` dependency (row:VOL-II-T2-4-TP): **interpretation_pending**
  - downstream proposal `ADD-03-D004-RAMP-FOLLOW` dependency (row:VOL-V-29.3-01): **interpretation_pending**
  - downstream proposal `DS009-Q1-REREAD` issue (reread:ADD-01:Q1): **interpretation_pending — HUMAN DECISION PENDING**
  - output difference: CHANGED VOL-II-T2-4-TP; CHANGED VOL-V-29.3-01; A5 REWORK deviations-review; A5 REWORK form-4e; A5 REWORK technical-proposal; A5 REVIEW (confirmed dependency) deviations-review; A5 REVIEW (proposed relationship) deviations-review; A5 REVIEW (confirmed dependency) form-4e; A5 REVIEW (proposed relationship) form-4e

### ADD-03:Q15 (table_row, p2) — applied (PROPOSED; not approved)
- source: “No: 15 | Bidder question: Following the capacity increase, will the Authority extend the construction period in Volume V Clause 12.1? | Authority response: No. The period of thirty-six (36) months is unchanged.”
- transition: `ADD-03/Q15` amendment_op annotate VOL-V:12.1 effect confirms
  - validation: **evidence_verified**
  - downstream proposal `ADD-03-D004-PCOD` row_reading (row:VOL-V-12.1-01): **interpretation_pending**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation
      - concern: insufficient evidence: The proposed review against amended reliability-run requirements has no supporting provision in the supplied evidence. Q15 supports the unchanged construction period and references a capacity increase only.
      - concern: insufficient evidence: No crop or image-inspection record is supplied for table row ADD-03:Q15, so the required image check cannot be verified.
      - concern: The obligation, Notice to Proceed anchor, unchanged month-based date rule and contractual delay-damages consequence are supported. However, the rationale's claim that the reading became stale is not established by the supplied records; the ADD-02 record has no stale entries, and no later staleness …
  - output difference: CHANGED VOL-V-12.1-01; A5 REWORK deviations-review; A5 REWORK form-4e; A5 REVIEW (proposed relationship) deviations-review; A5 REVIEW (proposed relationship) form-4e

### ADD-03:Q16 (table_row, p2) — no effect (PROPOSED; not approved)
- source: “No: 16 | Bidder question: Does the increase in capacity change the design influent characteristics in Table 2-2? | Authority response: No. Table 2-2 is unchanged.”
- transition: `ADD-03/Q16` disposition no_effect: The response states "No. Table 2-2 is unchanged." It prints no replacement, changed value or added obligation. Propose no_effect for human confirmation.
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model codex exec (configured gpt-6-astra; runtime identity recorded separately)

### ADD-03:Q17 (table_row, p2) — UNRESOLVED (accounted for, not applied)
- source: “No: 17 | Bidder question: Will the Availability Payment be adjusted for the increased capacity? | Authority response: Bidders shall price the Project as amended by this Addendum.”
- transition: `ADD-03/Q17` row_new {"row": {"id": "ADD03-Q17-PRICING", "group": "Commercial proposal", "scope": ["bid"], "requirement": "Bidders shall price the Project as amended by this Addendum.", "units": ["ADD-03:Q17"], "discipli…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model codex exec (configured gpt-6-astra; runtime identity recorded separately)
- transition: `ADD-03/Q17-coverage` escalation why: software limitation: validate_proposal accepts the well-formed row_new ADD-03/Q17, verifies its quotation and reports it ready with interpretation_pending, but still lists ADD-03:Q17 as UNACCOUNTED i…
  - validation: **escalated**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model codex exec (configured gpt-6-astra; runtime identity recorded separately)
    - concern: The printed controller records verify the row payload and quotation, but do not show Q17 reported as UNACCOUNTED or the claimed amendment-engine restriction. The asserted software limitation cannot be verified without those validation results; the proposer's rationale alone does not establish it.
  - downstream proposal `ADD-03-Q17-01-proposal` row_new (ana:ADD-03/Q17): **interpretation_pending**
  - downstream proposal `ADD-03-Q17-programme` dependency (ana:ADD-03/Q17): **insufficient_evidence** — held back: endpoints not promotable: ['assemble-envelope-b']
  - downstream proposal `D008-Q17-ESC` escalation (esc:ADD-03:Q17): **escalated**
  - downstream proposal `D008-Q17-QUESTION` issue (esc:ADD-03:Q17): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS009-Q17-COVERAGE` escalation (impact:8. RESPONSES TO CLARIFICATION REQUESTS 15 TO 18): **escalated**
  - output difference: NEW ADD-03-Q17-01; A5 REWORK fin-model-build; A5 REWORK fin-model-freeze; A5 REWORK form-4f

### ADD-03:Q18 (table_row, p2) — no effect (PROPOSED; not approved)
- source: “No: 18 | Bidder question: Please confirm the Proposal validity period following this Addendum. | Authority response: One hundred and fifty (150) days from the Proposal Due Date as amended.”
- transition: `ADD-03/Q18` disposition no_effect: The question requests confirmation and the response states "One hundred and fifty (150) days from the Proposal Due Date as amended." VOL-I:7.1 at ADD-02 alread…
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model codex exec (configured gpt-6-astra; runtime identity recorded separately)

## Downstream proposals (validated in the candidate)

| Item | Type | Task | Status | First failed check, or what a person confirms |
|---|---|---|---|---|
| DS-F4G-SUBMISSION-RECONCILIATION | issue | row:ADD-02-7.2-01 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words withdraws a question ('… |
| DS-F4G-01-WITHDRAWAL | issue | row:ADD-02-F4G-01 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words declares a matter resol… |
| DS-F4G-02-WITHDRAWAL | issue | row:ADD-02-F4G-02 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words declares a matter resol… |
| DS-F4G-03-WITHDRAWAL | issue | row:ADD-02-F4G-03 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words declares a matter resol… |
| DS-F4G-04-WITHDRAWAL | issue | row:ADD-02-F4G-04 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words withdraws a question ('… |
| DS-F4G-05-WITHDRAWAL | issue | row:ADD-02-F4G-05 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words declares a matter resol… |
| D-ADD-02-F4G-06-WITHDRAWAL | issue | row:ADD-02-F4G-06 | insufficient_evidence — HUMAN DECISION PENDING | missing_information: the proposer declares missing: insufficient evidence: no human handling instruction appears in the scoped current_records for reconciling the retained undertaking row with the fo… |
| D-ADD-02-F4G-07-WITHDRAWAL | issue | row:ADD-02-F4G-07 | insufficient_evidence — HUMAN DECISION PENDING | missing_information: the proposer declares missing: insufficient evidence: no human handling instruction appears in the scoped current_records for reconciling the retained undertaking row with the fo… |
| D-ADD-03-OMISSION | row_reading | row:VOL-I-3.4-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-ADD-03-CLARIFICATION | row_reading | row:VOL-I-5.2-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-ADD-03-DELIVERY | row_reading | row:VOL-I-6.1-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-ADD-03-BOND | row_reading | row:VOL-I-6.3-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-ADD-03-BOND-COUNTING | issue | row:VOL-I-6.3-01 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| D-ADD-03-BOND-RULE-GAP | escalation | row:VOL-I-6.3-01 | escalated |  |
| D-ADD-03-LINK-OMISSION | dependency | row:VOL-I-3.4-01 | insufficient_evidence | held back: endpoints not promotable: ['clarifications'] |
| D-ADD-03-LINK-CLARIFICATION | dependency | row:VOL-I-5.2-01 | insufficient_evidence | held back: endpoints not promotable: ['clarifications'] |
| D-ADD-03-LINK-DELIVERY | dependency | row:VOL-I-6.1-01 | insufficient_evidence | held back: endpoints not promotable: ['copies', 'assemble-envelope-b'] |
| D-ADD-03-LINK-BOND | dependency | row:VOL-I-6.3-01 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| D003-READ-1 | row_reading | row:VOL-I-6.4-01 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words declares a matter resolved ('resolution') |
| D003-READ-2 | row_reading | row:VOL-I-6.4-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D003-READ-3 | row_reading | row:VOL-I-6.7-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D003-READ-4 | row_reading | row:VOL-I-7.1-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D003-READ-5 | row_reading | row:VOL-I-8.3-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D003-READ-6 | row_reading | row:VOL-I-8.5-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D003-LINK-1 | dependency | row:VOL-I-6.4-01 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words declares a matter resolved ('resolved') |
| D003-LINK-3 | dependency | row:VOL-I-6.7-01 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| D003-LINK-4 | dependency | row:VOL-I-7.1-01 | insufficient_evidence | held back: endpoints not promotable: ['form-4a'] |
| D003-LINK-5 | dependency | row:VOL-I-8.3-01 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| D003-LINK-6 | dependency | row:VOL-I-8.5-01 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| ADD-03-D004-CAPACITY | row_reading | row:VOL-II-2.1-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| ADD-03-D004-TP | row_reading | row:VOL-II-T2-4-TP | interpretation_pending | a row reading is an interpretation: a person decides it |
| ADD-03-D004-PCOD | row_reading | row:VOL-V-12.1-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| ADD-03-D004-RAMP | row_reading | row:VOL-V-29.3-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| ADD-03-D004-ACK-ROW | row_new | c46:ADD-03/cover/para3 | interpretation_pending | a row reading is an interpretation: a person decides it |
| ADD-03-D004-EVAL-ROW | row_new | c46:ADD-03/6.1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words a waiver ('waiver') |
| ADD-03-D004-CAPACITY-FOLLOW | dependency | row:VOL-II-2.1-01 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| ADD-03-D004-TP-FOLLOW | dependency | row:VOL-II-T2-4-TP | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| ADD-03-D004-PCOD-FOLLOW | dependency | row:VOL-V-12.1-01 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| ADD-03-D004-RAMP-FOLLOW | dependency | row:VOL-V-29.3-01 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| ADD-03-D004-ACK-FOLLOW | dependency | c46:ADD-03/cover/para3 | insufficient_evidence | held back: endpoints not promotable: ['form-4a'] |
| ADD-03-D004-FORM-ISSUE | issue | c46:ADD-03/cover/para3 | insufficient_evidence — HUMAN DECISION PENDING | missing_information: the proposer declares missing: An explicit human instruction for preparing and executing the reissued Form 4-A. |
| ADD-03-D004-EVAL-ISSUE | issue | c46:ADD-03/6.1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| ADD-03-D004-EVAL-FOLLOW | dependency | c46:ADD-03/6.1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words decides which clause governs ('govern') |
| ADD-03-3.1-01-proposal | row_new | ana:ADD-03/3.1-nonsubmission-row | interpretation_pending | a row reading is an interpretation: a person decides it |
| ADD-03-3.2-01-proposal | row_new | ana:ADD-03/3.2-narrative-row | interpretation_pending | a row reading is an interpretation: a person decides it |
| ADD-03-Q17-01-proposal | row_new | ana:ADD-03/Q17 | interpretation_pending | a row reading is an interpretation: a person decides it |
| ADD-03-3.2-programme | dependency | ana:ADD-03/3.2-narrative-row | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| ADD-03-Q17-programme | dependency | ana:ADD-03/Q17 | insufficient_evidence | held back: endpoints not promotable: ['assemble-envelope-b'] |
| ADD-03-bond-clarification | clarification_item | clar:CQ-BOND-FC-COVERAGE | insufficient_evidence — HUMAN DECISION PENDING | missing_information: the proposer declares missing: Engine-derived current bond expiry and counting alternatives.; Express Financial Close coverage instruction and definition of the long-stop date. |
| ADD-03-bond-coverage-issue | issue | clar:CQ-BOND-FC-COVERAGE | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| ADD-03-form-4g-review-followup | issue | act:form-4g-review | insufficient_evidence — HUMAN DECISION PENDING | missing_information: the proposer declares missing: Human instruction on the surviving scope of the separately recorded undertakings and their evidence route. |
| ADD-03-form-4g-sign-followup | issue | act:form-4g-sign | insufficient_evidence — HUMAN DECISION PENDING | missing_information: the proposer declares missing: Human instruction reconciling the active form rows and EV-FORM-4G associations with the withdrawal. |
| P-ADD03-D006-CLARIFICATIONS | activity | act:clarifications | insufficient_evidence | held back: neighbouring activities not promotable: ['consortium-check'] |
| P-ADD03-D006-DELIVER | activity | act:deliver | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| P-ADD03-D006-SEAL | no_change | act:seal-and-mark | interpretation_pending |  |
| P-ADD03-D006-COPIES | activity | act:copies | conflicting | declared_conflicts: the proposer declares: I-VOL-I-COPIES; I-VOL-I-FILE-NAMES |
| P-ADD03-D006-ENVELOPE-A-GAP | escalation | act:assemble-envelope-a | conflicting | declared_conflicts: the proposer declares: I-F4G-LETTERING; I-F4G-NO; I-VOL-I-ENV-A-PRICES |
| P-ADD03-D006-ENVELOPE-B | activity | act:assemble-envelope-b | conflicting | declared_conflicts: the proposer declares: I-VOL-I-ENV-B |
| P-ADD03-D006-ENVELOPE-B-INSTRUCTION | escalation | act:assemble-envelope-b | conflicting | declared_conflicts: the proposer declares: I-VOL-I-ENV-B |
| D-ADD03-D007-BOND-APPROVAL | activity | act:bond-approval | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| D-ADD03-D007-BOND-ISSUE | activity | act:bond-issue | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| D-ADD03-D007-BOND-LABEL | escalation | act:bond-issue | escalated |  |
| D-ADD03-D007-FORM-PREP | no_change | act:form-4a-prep | interpretation_pending |  |
| D-ADD03-D007-FORM-SIGN | activity | act:form-4a | conflicting | declared_conflicts: the proposer declares: I-F4A-FIELDS |
| D-ADD03-D007-FORM-INSTRUCTION | issue | act:form-4a | insufficient_evidence — HUMAN DECISION PENDING | missing_information: the proposer declares missing: A recorded Legal handling instruction distinct from acceptance of the open issue. |
| D-ADD03-D007-ISO | activity | act:iso-copy | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| D-ADD03-D007-REFERENCES | activity | act:references | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| D008-TECH-ACTIVITY | activity | act:technical-proposal | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| D008-PDD-ESC | escalation | esc:ADD-03:2.2 | escalated |  |
| D008-PDD-LINK | dependency | esc:ADD-03:2.2 | insufficient_evidence | held back: endpoints not promotable: ['form-4a'] |
| D008-F4G-ESC | escalation | esc:ADD-03:3.1 | escalated |  |
| D008-F4G-HANDLING | escalation | esc:ADD-03:3.1 | escalated | missing_information: the proposer declares missing: Named human handling instruction for the partly modeled withdrawal |
| D008-FLOWS-ESC | escalation | esc:ADD-03:4.1 | escalated |  |
| D008-CAPACITY-LINK | dependency | esc:ADD-03:4.1 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| D008-CORRESPOND-ESC | escalation | esc:ADD-03:4.3 | escalated | missing_information: the proposer declares missing: Complete source wording for the corresponding worded and numeric capacity replacement |
| D008-Q17-ESC | escalation | esc:ADD-03:Q17 | escalated |  |
| D008-Q17-QUESTION | issue | esc:ADD-03:Q17 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words a waiver ('waiver') |
| DS009-DATE-PROPAGATION | escalation | impact:2. AMENDMENT TO THE PROPOSAL DUE DATE | escalated |  |
| DS009-FORM-DATE | issue | impact:2. AMENDMENT TO THE PROPOSAL DUE DATE | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words a precedence question (… |
| DS009-CAPACITY-WORDING | escalation | impact:4. AMENDMENT TO NOMINAL CAPACITY | escalated |  |
| DS009-FLOW-TARGETS | escalation | impact:4. AMENDMENT TO NOMINAL CAPACITY | escalated |  |
| DS009-FLOW-ANSWER | issue | impact:4. AMENDMENT TO NOMINAL CAPACITY | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words declares a matter resol… |
| DS009-Q17-COVERAGE | escalation | impact:8. RESPONSES TO CLARIFICATION REQUESTS 15 TO 18 | escalated |  |
| DS009-F4G-WITHDRAWAL | escalation | impact:3. WITHDRAWAL OF FORM 4-G | escalated |  |
| DS009-EVALUATION-BASIS | issue | impact:6. NEW VOLUME I CLAUSE 11.6 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS009-Q1-REREAD | issue | reread:ADD-01:Q1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-REREAD-ADD01-Q3 | issue | reread:ADD-01:Q3 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-REREAD-ADD01-Q5 | issue | reread:ADD-01:Q5 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-REREAD-ADD02-Q8 | issue | reread:ADD-02:Q8 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-REREAD-ADD02-Q11 | issue | reread:ADD-02:Q11 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words declares a matter resol… |

## Promoted into the candidate (PROPOSED; nothing accepted)

- ops: ADD-03/cover/para3, ADD-03/1.1, ADD-03/2.1(a), ADD-03/2.1(b), ADD-03/3.1(b), ADD-03/3.2(a), ADD-03/4.1(a), ADD-03/4.2, ADD-03/5.1, ADD-03/5.2(a), ADD-03/5.2(b), ADD-03/6.1, ADD-03/7.1, ADD-03/Q15
- dispositions: ADD-03:cover/para1: no_effect, ADD-03:cover/para2: no_effect, ADD-03:Q16: no_effect, ADD-03:Q18: no_effect
- accounted unresolved: ADD-03:4.3
- rows new: ADD-03-cover-01, ADD-03-6.1-01, ADD-03-3.1-01, ADD-03-3.2-01, ADD-03-Q17-01
- readings: VOL-I-3.4-01, VOL-I-5.2-01, VOL-I-6.1-01, VOL-I-6.3-01, VOL-I-6.4-01, VOL-I-6.4-02, VOL-I-6.7-01, VOL-I-7.1-01, VOL-I-8.3-01, VOL-I-8.5-01, VOL-II-2.1-01, VOL-II-T2-4-TP, VOL-V-12.1-01, VOL-V-29.3-01
- issues: I-ADD-03-BOND-COUNTING, I-ADD-03-BOND-COVERAGE-REVIEW, I-ADD-03-D008-Q17-PRICE, I-ADD-03-DS009-EVALUATION-BASIS, I-ADD-03-DS009-FLOW-ANSWER, I-ADD-03-DS009-FORM-DATE, I-ADD-03-DS009-Q1-REREAD, I-ADD-03-F4G-01-WITHDRAWAL, I-ADD-03-F4G-02-WITHDRAWAL, I-ADD-03-F4G-03-WITHDRAWAL, I-ADD-03-F4G-04-WITHDRAWAL, I-ADD-03-F4G-05-WITHDRAWAL, I-ADD-03-F4G-SUBMISSION-RECONCILIATION, I-ADD03-6-1-THRESHOLD, I-ADD03-REREAD-ADD01-Q3, I-ADD03-REREAD-ADD01-Q5, I-ADD03-REREAD-ADD02-Q11, I-ADD03-REREAD-ADD02-Q8
- activities: deliver, bond-approval, bond-issue, iso-copy, references, technical-proposal
- relationships: REL-AI-001, REL-AI-002, REL-AI-003, REL-AI-004, REL-AI-005, REL-AI-006, REL-AI-007, REL-AI-008, REL-AI-009, REL-AI-010, REL-AI-011, REL-AI-012
- no change: act:seal-and-mark, act:form-4a-prep
- the same question promoted once (analysis issue -> the issue it was merged into): I-ADD-03-2-2-PROPAGATION-REVIEW-ANA -> I-ADD-03-DS009-FORM-DATE; I-ADD-03-2-1-FORM-DATE-REVIEW-ANA -> I-ADD-03-DS009-FORM-DATE; I-ADD-03-4-1-4-1-FLOW-REVIEW-ANA -> I-ADD-03-DS009-FLOW-ANSWER; I-ADD-03-3-1-3-1-LIST-REVIEW-ANA -> I-ADD-03-F4G-SUBMISSION-RECONCILIATION; I-ADD-03-6-1-THRESHOLD-ISSUE-ANA -> I-ADD-03-DS009-EVALUATION-BASIS
- unresolved provisions: 5
- note: ADD-03:3.1: partly answered by ADD-03/3.1(b); escalated: software limitation: the provision states ‘Form 4-G (Cybersecurity Compliance Undertaking), added by Addendum No. 2 Section 7, is withdrawn.’ The form is supplied as group ADD-02:F4-G; set_status on … (the promoted item stands; the escalation is for a person)
- note: ADD-03:4.1: partly answered by ADD-03/4.1(a); escalated: software limitation: The printed replacement ‘120,000 m³/day’ to ‘150,000 m³/day’ expressly names Table 2-6 row 2-6.1. set_value of its Value cell to the printed numeric component 150,000 fails C22 b…; software limitation: The provision expressly states ‘The peak hourly flow in Table 2-6 row 2-6.2 is unchanged.’ An annotate/confirms operation on that row fails C22 because the engine does not recogn… (the promoted item stands; the escalation is for a person)
- note: rows.yaml: 2 comment line(s) inside row VOL-I-6.1-01 were not kept (the row was rewritten; the file's other comments are kept)
- note: rows.yaml: 5 comment line(s) inside row VOL-I-8.5-01 were not kept (the row was rewritten; the file's other comments are kept)
- note: VOL-II.yaml: 1 comment line(s) inside row VOL-II-T2-4-TP were not kept (the row was rewritten; the file's other comments are kept)
- note: VOL-V.yaml: 1 comment line(s) inside row VOL-V-12.1-01 were not kept (the row was rewritten; the file's other comments are kept)
- note: VOL-V.yaml: 1 comment line(s) inside row VOL-V-29.3-01 were not kept (the row was rewritten; the file's other comments are kept)

- left out of the promoted ops: ADD-03/cover/para3/acknowledgement-row: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/cover/para3` as an UN…; ADD-03/2.2/propagation-review: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-2-2-PROPAGATION-REVIEW-ANA; HUMAN DE…; ADD-03/2.1/form-date-review: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-2-1-FORM-DATE-REVIEW-ANA; HUMAN DECI…; ADD-03/3.1-nonsubmission-row: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/3.1-nonsubmission-row…; ADD-03/3.2-narrative-row: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/3.2-narrative-row` as…; ADD-03/4.3-wording-question: an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; th…; ADD-03/4.1-flow-review: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-4-1-4-1-FLOW-REVIEW-ANA; HUMAN DECIS…; ADD-03/3.1-list-review: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-3-1-3-1-LIST-REVIEW-ANA; HUMAN DECIS…; ADD-03/6.1/A1: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/6.1` as an UNVERIFIED…; ADD-03/6.1/threshold-issue: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-6-1-THRESHOLD-ISSUE-ANA; HUMAN DECIS…; ADD-03/Q17: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/Q17` as an UNVERIFIED…

## check-register on the candidate

- exit 0; 0 finding(s) {}
- missing because the downstream phase did not propose them (the run's own new rows): 0
- defects: 0

## Analysis rows carried to downstream tasks (and other analysis items not promoted)

- `ADD-03/cover/para3/acknowledgement-row` row_new (ADD-03:cover/para3, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/cover/para3` as an UNVERIFIED reference — applied as the new row(s) ADD-03-cover-01 (proposed downstream: ADD-03-cover-01 (row_new, interpretation_pending); task(s) c46:ADD-03/cover/para3; PROPOSED, not approved): the provision's obligation is that row; a person confirms it
- `ADD-03/2.2/propagation-review` issue (ADD-03:2.2, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-2-2-PROPAGATION-REVIEW-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ADD-03/2.1/form-date-review` issue (ADD-03:2.1, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-2-1-FORM-DATE-REVIEW-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ADD-03/3.1-nonsubmission-row` row_new (ADD-03:3.1, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/3.1-nonsubmission-row` as an UNVERIFIED reference — applied as the new row(s) ADD-03-3.1-01 (proposed downstream: ADD-03-3.1-01 (row_new, interpretation_pending); task(s) ana:ADD-03/3.1-nonsubmission-row; PROPOSED, not approved): the provision's obligation is that row; a person confirms it
- `ADD-03/3.2-narrative-row` row_new (ADD-03:3.2, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/3.2-narrative-row` as an UNVERIFIED reference — applied as the new row(s) ADD-03-3.2-01 (proposed downstream: ADD-03-3.2-01 (row_new, interpretation_pending), ADD-03-3.2-programme (dependency, interpretation_pending); task(s) ana:ADD-03/3.2-narrative-row; PROPOSED, not approved): the provision's obligation is that row; a person confirms it
- `ADD-03/4.3-wording-question` clarification (ADD-03:4.3, interpretation_pending): an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; the downstream phase proposes issues and clarification entries against the candidate
- `ADD-03/4.1-flow-review` issue (ADD-03:4.1, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-4-1-4-1-FLOW-REVIEW-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ADD-03/3.1-list-review` issue (ADD-03:3.1, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-3-1-3-1-LIST-REVIEW-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ADD-03/6.1/A1` row_new (ADD-03:6.1, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/6.1` as an UNVERIFIED reference — applied as the new row(s) ADD-03-6.1-01 (proposed downstream: ADD-03-6.1-01 (row_new, interpretation_pending), ADD-03-D004-EVAL-ISSUE (issue, interpretation_pending), ADD-03-D004-EVAL-FOLLOW (dependency, interpretation_pending); task(s) c46:ADD-03/6.1; PROPOSED, not approved): the provision's oblig…
- `ADD-03/6.1/threshold-issue` issue (ADD-03:6.1, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-6-1-THRESHOLD-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ADD-03/Q17` row_new (ADD-03:Q17, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ADD-03/Q17` as an UNVERIFIED reference — applied as the new row(s) ADD-03-Q17-01 (proposed downstream: ADD-03-Q17-01 (row_new, interpretation_pending); task(s) ana:ADD-03/Q17; PROPOSED, not approved): the provision's obligation is that row; a person confirms it

## Coverage

- provisions: 19; accounted for by the combined set: 19; states {'validated': 19}
- the analysis ITEMS' resolution by the controller (items, not provisions; session 14): resolved 11, pending 8, invalid 0, unaccounted 0; approved 0
- structural units of ADD-03 that are not provisions (listed so nothing is dropped): ADD-03:H:cover (heading), ADD-03:H:cover-2 (heading), ADD-03:H:S1 (heading), ADD-03:H:S2 (heading), ADD-03:H:S3 (heading), ADD-03:H:S4 (heading), ADD-03:H:S5 (heading), ADD-03:H:S6 (heading), ADD-03:H:S7 (heading), ADD-03:H:S8 (heading), ADD-03:S8/QA (table)
- batches: analysis-001 done, analysis-002 done, analysis-003 done, analysis-004 done, downstream-001 done, downstream-002 done, downstream-003 done, downstream-004 done, downstream-005 done, downstream-006 done, downstream-007 done, downstream-008 done, downstream-009 done, downstream-010 done

## Critic (a second model over the selected items; it changed no status)

**Agreement between the critic and the proposer is not approval**: every item still needs a person's decision, and a disagreement is a concern for that person, not a rejection. The critic reviews only the selected classes (consequential interpretations, uncertain targets, removals, conflicting evidence), in one request per batch.

| Batch | Critic | Selected | Reviewed | Agrees | Does not agree | Note |
|---|---|---|---|---|---|---|
| analysis-001 | done | 4 | 4 | 3 | 1 |  |
| analysis-002 | done | 9 | 9 | 5 | 4 |  |
| analysis-003 | done | 3 | 3 | 3 | 0 |  |
| analysis-004 | done | 4 | 4 | 3 | 1 |  |
| downstream-001 | not_needed | 0 | - | - | - |  |
| downstream-002 | done | 3 | 3 | 1 | 2 |  |
| downstream-003 | done | 2 | 2 | 2 | 0 |  |
| downstream-004 | done | 1 | 1 | 0 | 1 |  |
| downstream-005 | not_needed | 0 | - | - | - |  |
| downstream-006 | done | 4 | 4 | 2 | 2 |  |
| downstream-007 | done | 1 | 1 | 1 | 0 |  |
| downstream-008 | not_needed | 0 | - | - | - |  |
| downstream-009 | not_needed | 0 | - | - | - |  |
| downstream-010 | not_needed | 0 | - | - | - |  |

- **ADD-03/cover/para3** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites
- **ADD-03/cover/para3/acknowledgement-row** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites
- **ADD-03/2.2/propagation-review** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites
    - concern: insufficient evidence: the printed records support the listed PDD-linked requirements, but contain no activities or programme simulation results supporting the specifically named A5 activity chain.
    - concern: insufficient evidence: no printed controller record supports the rationale's claim that the engine cannot annotate this scope. The claimed software limitation cannot be verified.
    - concern: The controller's keyword flags do not reflect the issue's meaning: it expressly leaves questions unanswered and unwithdrawn.
- **ADD-03/2.1/form-date-review** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites
- **ADD-03/3.1(b)** (analysis-002; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because removal
- **ADD-03/3.2(a)** (analysis-002; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is a group
    - concern: The rationale states that VOL-II:S6 contains only its heading. Annotating that group does not establish that the confirmation reaches substantive clauses VOL-II:6.1–6.3. Explicitly target those clauses or provide validation showing that the group annotation covers them; the successful dry run does …
- **ADD-03/3.1(a)-escalation** (analysis-002; controller status **escalated**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is a group
    - concern: The withdrawal and identified form members are supported. However, the asserted C22 failures are not printed in the controller records; those records verify only payload structure and quotations. The claimed software limitation cannot be independently verified without the failed simulation records.
- **ADD-03/4.1(b)-escalation** (analysis-002; controller status **escalated**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites
    - concern: The provision expressly identifies row 2-6.1 and supports changing only its Value cell to 150,000 while retaining m³/day. However, no failed simulation or citation-mapping record is printed to substantiate the asserted C22 software limitation; payload validation alone does not verify it.
- **ADD-03/4.1(c)-escalation** (analysis-002; controller status **escalated**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites
    - concern: The provision expressly confirms that row 2-6.2 is unchanged. However, no failed simulation or citation-mapping record is printed to substantiate the asserted C22 software limitation; payload validation alone does not verify it.
- **ADD-03/3.1-nonsubmission-row** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites
- **ADD-03/3.2-narrative-row** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites
- **ADD-03/4.1-flow-review** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites
    - concern: Correct the rationale's attribution: the former daily figure appears in the bidder question, not the Authority response. The changed premise nevertheless supports the proposed human review without establishing a conflict or withdrawing the earlier answer.
- **ADD-03/3.1-list-review** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites
- **ADD-03/6.1** (analysis-003; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites
- **ADD-03/6.1/A1** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites
- **ADD-03/6.1/threshold-issue** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites
- **ADD-03/Q16** (analysis-004; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites
- **ADD-03/Q17** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites
- **ADD-03/Q18** (analysis-004; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites
- **ADD-03/Q17-coverage** (analysis-004; controller status **escalated**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites
    - concern: The printed controller records verify the row payload and quotation, but do not show Q17 reported as UNACCOUNTED or the claimed amendment-engine restriction. The asserted software limitation cannot be verified without those validation results; the proposer's rationale alone does not establish it.
- **D-ADD-03-OMISSION** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation
- **D-ADD-03-CLARIFICATION** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation
    - concern: insufficient evidence: the relative deadline rule and consequence are supported, but no calculate(deadline) result is printed to substantiate the claimed calculation confirmation. VOL-I:2.4 supports excluding the stated date; provide the calculation record or attribute that reading directly to the …
- **D-ADD-03-DELIVERY** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation
    - concern: insufficient evidence: the amended deadline, retained time and address reference, and rejection consequence are supported. However, no activity records or supporting clauses establish the named seal-and-mark, copies, assemble-envelope-a and assemble-envelope-b activities or their dependencies under…
- **D003-READ-3** (downstream-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation
- **D003-READ-6** (downstream-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation
- **ADD-03-D004-PCOD** (downstream-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation
    - concern: insufficient evidence: The proposed review against amended reliability-run requirements has no supporting provision in the supplied evidence. Q15 supports the unchanged construction period and references a capacity increase only.
    - concern: insufficient evidence: No crop or image-inspection record is supplied for table row ADD-03:Q15, so the required image check cannot be verified.
    - concern: The obligation, Notice to Proceed anchor, unchanged month-based date rule and contractual delay-damages consequence are supported. However, the rationale's claim that the reading became stale is not established by the supplied records; the ADD-02 record has no stale entries, and no later staleness …
- **P-ADD03-D006-COPIES** (downstream-006; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting
    - concern: The proposed preparation and pending instructions follow the quoted requirements and existing issues. However, the claimed preservation of both EV-COPIES and EV-DELIVERY associations is not established: the payload names only EV-DELIVERY and VOL-I-6.1-01, current_records.activities is empty, and th…
- **P-ADD03-D006-ENVELOPE-A-GAP** (downstream-006; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because conflicting
    - concern: insufficient evidence: the request does not print the promoted operations or assembly template. The assertions that an operation only revokes ADD-02:7.2 and that assemble-envelope-a still includes Form 4-G cannot be verified. The printed ADD-02 register establishes the previous-stage contents, not …
    - concern: ADD-03:3.1 expressly withdraws Form 4-G and prohibits submission. Any uncertainty should concern implementation of that instruction, without implying that the withdrawal itself lacks evidence.
    - concern: The item declares I-VOL-I-ENV-A-PRICES as a conflict without showing how Form 4-G withdrawal affects that separate issue.
- **P-ADD03-D006-ENVELOPE-B** (downstream-006; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting
- **P-ADD03-D006-ENVELOPE-B-INSTRUCTION** (downstream-006; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting
- **D-ADD03-D007-FORM-SIGN** (downstream-007; controller status **conflicting**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because conflicting

## Requests: failures, deferrals, repairs and route notices

- every request was answered at the first call, parsed, and fitted its context

Route notices (how the requests were served; they change no status):
- **capabilities_declared** (analysis-001): capabilities declared, not verified: host codex exec (configured gpt-6-astra; runtime identity recorded separately) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: Codex CLI text/tool/image conformance observed locally on 8 Oct 2026; context and output limits are d…
- **capabilities_declared** (downstream-001): capabilities declared, not verified: host codex exec (configured gpt-6-astra; runtime identity recorded separately) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: Codex CLI text/tool/image conformance observed locally on 8 Oct 2026; context and output limits are d…
- **capabilities_declared** (downstream-002): capabilities declared, not verified: host codex exec (configured gpt-6-astra; runtime identity recorded separately) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: Codex CLI text/tool/image conformance observed locally on 8 Oct 2026; context and output limits are d…
- **capabilities_declared** (downstream-003): capabilities declared, not verified: host codex exec (configured gpt-6-astra; runtime identity recorded separately) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: Codex CLI text/tool/image conformance observed locally on 8 Oct 2026; context and output limits are d…
- **capabilities_declared** (downstream-004): capabilities declared, not verified: host codex exec (configured gpt-6-astra; runtime identity recorded separately) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: Codex CLI text/tool/image conformance observed locally on 8 Oct 2026; context and output limits are d…
- **capabilities_declared** (downstream-005): capabilities declared, not verified: host codex exec (configured gpt-6-astra; runtime identity recorded separately) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: Codex CLI text/tool/image conformance observed locally on 8 Oct 2026; context and output limits are d…
- **capabilities_declared** (downstream-006): capabilities declared, not verified: host codex exec (configured gpt-6-astra; runtime identity recorded separately) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: Codex CLI text/tool/image conformance observed locally on 8 Oct 2026; context and output limits are d…
- **capabilities_declared** (downstream-007): capabilities declared, not verified: host codex exec (configured gpt-6-astra; runtime identity recorded separately) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: Codex CLI text/tool/image conformance observed locally on 8 Oct 2026; context and output limits are d…
- **capabilities_declared** (downstream-008): capabilities declared, not verified: host codex exec (configured gpt-6-astra; runtime identity recorded separately) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: Codex CLI text/tool/image conformance observed locally on 8 Oct 2026; context and output limits are d…
- **capabilities_declared** (downstream-009): capabilities declared, not verified: host codex exec (configured gpt-6-astra; runtime identity recorded separately) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: Codex CLI text/tool/image conformance observed locally on 8 Oct 2026; context and output limits are d…
- **capabilities_declared** (downstream-010): capabilities declared, not verified: host codex exec (configured gpt-6-astra; runtime identity recorded separately) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: Codex CLI text/tool/image conformance observed locally on 8 Oct 2026; context and output limits are d…

## Manual interventions (the person's actions)

- 2026-10-15T14:04:27Z: stop (the person's action) by a person (a signal from outside the run: the panel's Stop, Ctrl-C or a kill); SIGTERM during step downstream; 1 host session process(es) stopped
- 2026-10-15T14:04:56Z: resume (the person's action) by a person (tenderpack ai resume, or the panel's Resume); process 14995; status before: stopped

### What the run did with them, and its automatic host sessions (not a person)

- 2026-10-15T13:24:03Z: host session (automatic) — batch analysis-001 by tenderpack.ai.hostsession; host model codex exec (configured gpt-6-astra; runtime identity recorded separately); a headless host session over the MCP tools; not a person
- 2026-10-15T13:27:21Z: submission reused (automatic) — batch analysis-002 by tenderpack.ai.workflow; the host session's staged set ADD-03-host-20261015T132340Z-09b2 (made in this drive) was revalidated and taken instead of asking the batch again
- 2026-10-15T13:28:17Z: submission reused (automatic) — batch analysis-003 by tenderpack.ai.workflow; the host session's staged set ADD-03-host-20261015T132628Z-e556 (made in this drive) was revalidated and taken instead of asking the batch again
- 2026-10-15T13:28:37Z: submission reused (automatic) — batch analysis-004 by tenderpack.ai.workflow; the host session's staged set ADD-03-host-20261015T132659Z-9dd7 (made in this drive) was revalidated and taken instead of asking the batch again
- 2026-10-15T13:33:59Z: host session (automatic) — batch downstream-001 by tenderpack.ai.hostsession; host model codex exec (configured gpt-6-astra; runtime identity recorded separately); a headless host session; not a person
- 2026-10-15T13:42:14Z: host session (automatic) — batch downstream-002 by tenderpack.ai.hostsession; host model codex exec (configured gpt-6-astra; runtime identity recorded separately); a headless host session; not a person
- 2026-10-15T13:46:00Z: host session (automatic) — batch downstream-003 by tenderpack.ai.hostsession; host model codex exec (configured gpt-6-astra; runtime identity recorded separately); a headless host session; not a person
- 2026-10-15T14:04:27Z: host session stopped by the person's stop — batch downstream-004 by tenderpack.ai.workflow (automatic); its exchange was cut before its answer was taken; on resume its staged submission is reused if it made one, else it is asked again
- 2026-10-15T14:13:24Z: host session (automatic) — batch downstream-004 by tenderpack.ai.hostsession; host model codex exec (configured gpt-6-astra; runtime identity recorded separately); a headless host session; not a person
- 2026-10-15T14:13:25Z: host session (automatic) — batch downstream-005 by tenderpack.ai.hostsession; host model codex exec (configured gpt-6-astra; runtime identity recorded separately); a headless host session; not a person
- 2026-10-15T14:16:58Z: host session (automatic) — batch downstream-006 by tenderpack.ai.hostsession; host model codex exec (configured gpt-6-astra; runtime identity recorded separately); a headless host session; not a person
- 2026-10-15T14:17:21Z: host session (automatic) — batch downstream-007 by tenderpack.ai.hostsession; host model codex exec (configured gpt-6-astra; runtime identity recorded separately); a headless host session; not a person
- 2026-10-15T14:24:51Z: host session (automatic) — batch downstream-008 by tenderpack.ai.hostsession; host model codex exec (configured gpt-6-astra; runtime identity recorded separately); a headless host session; not a person
- 2026-10-15T14:24:56Z: host session (automatic) — batch downstream-009 by tenderpack.ai.hostsession; host model codex exec (configured gpt-6-astra; runtime identity recorded separately); a headless host session; not a person
- 2026-10-15T14:27:30Z: host session (automatic) — batch downstream-010 by tenderpack.ai.hostsession; host model codex exec (configured gpt-6-astra; runtime identity recorded separately); a headless host session; not a person

## The diff (ADD-02 → ADD-03; [diff.md](diff.md))

## What changed from ADD-02 to ADD-03

### ADD-03: PARTIAL (issued 2026-11-08)

- ops: 14 (0 invalid); provisions: 19 (3 unresolved)
- validated state: ADD-02 — this addendum does NOT replace it until every provision is treated and every op is valid
- UNRESOLVED ADD-03:2.2: Every period calculated by reference to the Proposal Due Date is adjusted accordingly.
- UNRESOLVED ADD-03:4.3: Volume I Clause 1.3 is amended correspondingly.
- UNRESOLVED ADD-03:Q17: No: 17 | Bidder question: Will the Availability Payment be adjusted for the increased capacity? | Authority response: Bidders shall price the Project as amended
- cover summary vs provisions (C28, report only): 9 finding(s)
  - not found: 'withdraws Form 4-G': no provision of ADD-03 does this
  - not found: 'adds a new Clause 11.6': no provision of ADD-03 does this
  - omitted: ADD-03/1.1 confirms VOL-I:3.2; the summary does not mention it: 'This Addendum takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.'
  - omitted: ADD-03/3.1(b) ends the effect of ADD-02:7.2; the summary does not mention it: 'Form 4-G (Cybersecurity Compliance Undertaking), added by Addendum No. 2 Section 7, is withdrawn. Bidders shall disregard it and shall not submit it. Section 7.2 of Addendum No. 2 ceases to have effect.'
  - omitted: ADD-03/3.2(a) confirms VOL-II:S6; the summary does not mention it: 'The substantive requirements of Volume II Section 6 are unchanged and shall be addressed in the Technical Proposal narrative.'
  - omitted: ADD-03/5.1 amends VOL-I:6.4; the summary does not mention it: 'In Volume I Clause 6.4, ‘SAR 4,500,000 (four million five hundred thousand Saudi Riyals)’ is deleted and ‘SAR 5,600,000 (five million six hundred thousand Saudi Riyals)’ is substituted.'
  - omitted: ADD-03/5.2(a) amends VOL-I:6.3; the summary does not mention it: 'In Volume I Clause 6.3, ‘one hundred and eighty (180) days’ is deleted and ‘two hundred and ten (210) days’ is substituted. The Proposal validity period in Clause 7.1 is unchanged.'
  - omitted: ADD-03/5.2(b) confirms VOL-I:7.1; the summary does not mention it: 'In Volume I Clause 6.3, ‘one hundred and eighty (180) days’ is deleted and ‘two hundred and ten (210) days’ is substituted. The Proposal validity period in Clause 7.1 is unchanged.'
  - omitted: ADD-03/6.1 inserts new text after VOL-I:11.5; the summary does not mention it: 'A new Clause 11.6 is added to Volume I: ‘11.6 Where, on completion of the combined evaluation, two or more Proposals are within two per cent (2%) of one another, the Authority may apply such further criteria as it considers appropriate to …'

#### Validated vs candidate (partial should not mean useless)

- validated (unchanged, ADD-02): `<outputs>/a3/a3.pdf` (one page), `<outputs>/a5/`
- candidate (CANDIDATE — NOT VALIDATED, ADD-03 as proposed): `<outputs>/a3/a3_candidate.pdf` / `.md`, `<outputs>/a5/candidate/`

**What may be changing.** ADD-03 is PARTIAL: 3 of 19 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 14 op(s) that are valid there stood (each still a proposal: review accepted 14), A3 would gain 0 row(s) (none), lose 1 (ADD-02-7.2-01 (ADD-03/3.1(b))) and change 5 (ADD-02-F4G-04 (register), VOL-I-6.1-01 (ADD-03/2.1(a), ADD-03/2.1(b)), VOL-I-6.3-01 (ADD-03/5.2(a)), VOL-I-6.4-01 (ADD-03/5.1) and 1 more); A5, replanned at ADD-03's issue date (2026-11-08), would move the latest dates of 43 activities (assemble-envelope-a, assemble-envelope-b, bond-approval, bond-issue and 39 more), add 0 (none) and remove 0 (none), and marks 17 REVIEW through relationships. Not settled: 5 activities blocked by an unresolved row (fin-model-build, fin-model-freeze, form-4g-review, form-4f and 1 more), 7 STALE row(s), 0 obligation(s) reaching no output (C46), 8 relationship chain(s) blocked or incomplete, 1 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT and 7 more. Nothing here is validated, accepted or applied to the real state.

### Requirements

- new: 5; out of force: 1; changed: 21

- NEW ADD-03-cover-01: NEW (introduced by ADD-03/cover/para3)
- NEW ADD-03-6.1-01: NEW (introduced by ADD-03/6.1) (by ADD-03/6.1)
- NEW ADD-03-3.1-01: NEW (introduced by ADD-03:3.1)
- NEW ADD-03-3.2-01: NEW (introduced by ADD-03:3.2)
- NEW ADD-03-Q17-01: NEW (introduced by ADD-03:Q17)
- OUT ADD-02-7.2-01: REVOKED (ADD-03/3.1(b))
- CHANGED VOL-I-6.1-01: wording; quoted words; PDD 2026-11-26 -> 2026-12-10 (by ADD-03/2.1(a))
- CHANGED VOL-I-5.2-01: CLARIFICATION-CUTOFF 2026-11-12 -> 2026-11-26; reading: parameters
- CHANGED VOL-I-6.3-01: wording; quoted words; BID-BOND-VALIDITY 2027-05-25 -> 2027-07-08; reading: parameters (by ADD-03/5.2(a))
- CHANGED VOL-I-6.4-01: wording; quoted words; reading: parameters (by ADD-03/5.1)
- CHANGED VOL-I-6.4-02: wording (by ADD-03/5.1)
- CHANGED VOL-I-7.1-01: PROPOSAL-VALIDITY 2027-04-25 -> 2027-05-09
- CHANGED VOL-I-8.3-01: ISO-CURRENT-AT 2026-11-26 -> 2026-12-10; reading: parameters
- CHANGED VOL-I-8.5-01: wording; quoted words; REFERENCE-LOOKBACK 2016-11-27 -> 2016-12-11; reading: parameters (by ADD-03/4.2)
- CHANGED VOL-IV-F4A-01: PDD moved 2026-11-26 -> 2026-12-10 (VOL-I 6.1 as amended by ADD-01 2.1, ADD-03 2.1); ADD-01 AppA/proposal-due-date prints 2026-11-12: CONFLICT with the amended PDD, not corrected (a person decides)
- CHANGED VOL-I-3.4-01: OMISSION-CLAIM-CUTOFF 2026-11-26 -> 2026-12-10; reading: parameters
- CHANGED VOL-I-6.7-01: MODIFY-CUTOFF 2026-11-26 -> 2026-12-10; reading: parameters
- CHANGED VOL-II-2.1-01: wording; quoted words; reading: parameters (by ADD-03/4.1(a))
- CHANGED VOL-II-2.4-01: VOL-II T2-4/TP: Limit 1 -> 0.5 mg/l by ADD-03/7.1 (depends on it: REL-T24-COMPLIANCE-MONITORING-STREAMS (limit_applies, confirmed))
- CHANGED VOL-II-T2-4-TP: wording; quoted words; reading: parameters (by ADD-03/7.1)
- CHANGED VOL-II-3.1-01: VOL-II T2-4/TP: Limit 1 -> 0.5 mg/l by ADD-03/7.1 (depends on it: REL-T24-PROCESS-DESIGN (limit_applies, confirmed))
- CHANGED VOL-II-4.3-02: VOL-II T2-4/TP: Limit 1 -> 0.5 mg/l by ADD-03/7.1 (depends on it: REL-T24-COMPLIANCE-MONITORING-STREAMS (limit_applies, confirmed))
- CHANGED VOL-II-7.2-01: VOL-II T2-4/TP: Limit 1 -> 0.5 mg/l by ADD-03/7.1 (depends on it: REL-T24-RELIABILITY-RUN (limit_applies, confirmed))
- CHANGED VOL-IV-F4A-02: PDD moved 2026-11-26 -> 2026-12-10 (VOL-I 6.1 as amended by ADD-01 2.1, ADD-03 2.1); ADD-01 AppA/proposal-due-date prints 2026-11-12: CONFLICT with the amended PDD, not corrected (a person decides)
- CHANGED VOL-V-12.1-01: quoted words; reading: consequence
- CHANGED VOL-V-29.3-01: quoted words; secondary unit VOL-II:T2-4/TP amended by ADD-03/7.1 (Limit: 1 -> 0.5) (by ADD-03/7.1)
- CHANGED VOL-V-31.1-02: VOL-II T2-4/TP: Limit 1 -> 0.5 mg/l by ADD-03/7.1 (depends on it: REL-T24-UNAVAILABILITY (limit_applies, confirmed))

### Stale readings and decisions

- STALE ADD-02-F4G-01: ADD-02:7.2 changed since ADD-02 (by ADD-03/3.1(b))
- STALE ADD-02-F4G-05: ADD-02:7.2 changed since ADD-02 (by ADD-03/3.1(b))
- STALE ADD-02-F4G-06: ADD-02:7.2 changed since ADD-02 (by ADD-03/3.1(b))
- STALE ADD-02-F4G-07: ADD-02:7.2 changed since ADD-02 (by ADD-03/3.1(b))
- STALE ADD-02-F4G-02: ADD-02:7.2 changed since ADD-02 (by ADD-03/3.1(b))
- STALE ADD-02-F4G-03: ADD-02:7.2 changed since ADD-02 (by ADD-03/3.1(b))
- STALE ADD-02-F4G-04: ADD-02:7.2 changed since ADD-02 (by ADD-03/3.1(b))
- DECISION VOID (content changed since review): ADD-02-F4G-01, ADD-02-F4G-05, ADD-02-F4G-06, ADD-02-F4G-07, ADD-02-F4G-02, ADD-02-F4G-03, ADD-02-F4G-04
- IMAGE-READ VALUE CHANGED: VOL-II:T2-4/TP Limit: image shows 1, ADD-03 makes it 0.5 (reading approved; the image itself is unchanged)

### Obligations not reaching the outputs (C46)

- none

### Reached through relationships (indirect: for review, not direct citations)

Curated links (relationships file) followed from what changed. The requirements above cite a changed unit; these are reached through another provision, in three classes that are never merged. A5 marks the activities that serve them REVIEW with their dates unchanged.

Relationship status: confirmed = stated in the documents (the entry quotes the cross-reference), not confirmed by a person; proposed = inferred by a curator or a model, a person decides; possible = a weaker inference.

#### Confirmed dependency (6)
- VOL-II-2.4-01 (row; ACTIVE) <- VOL-II:T2-4 via REL-T24-COMPLIANCE-MONITORING-STREAMS [limit_applies; link confirmed]; BLOCKED: cannot be established: the Environmental Permit issued for the site not supplied (that the reproduced Table 2-4 limits, as amended by the addenda, are the limits that govern (the Permit prevails over the reproduction), and the limit of any parameter not listed (Note 1); Permit compliance is not claimed) [REL-MISSING-ENVIRONMENTAL-PERMIT]
- VOL-II-3.1-01 (row; ACTIVE) <- VOL-II:T2-4 via REL-T24-PROCESS-DESIGN [limit_applies; link confirmed]; BLOCKED: cannot be established: the Environmental Permit issued for the site not supplied (that the reproduced Table 2-4 limits, as amended by the addenda, are the limits that govern (the Permit prevails over the reproduction), and the limit of any parameter not listed (Note 1); Permit compliance is not claimed) [at VOL-II:T2-4, REL-MISSING-ENVIRONMENTAL-PERMIT]
- VOL-II-4.3-02 (row; ACTIVE) <- VOL-II:T2-4 via REL-T24-COMPLIANCE-MONITORING-STREAMS [limit_applies; link confirmed]; BLOCKED: cannot be established: the Environmental Permit issued for the site not supplied (that the reproduced Table 2-4 limits, as amended by the addenda, are the limits that govern (the Permit prevails over the reproduction), and the limit of any parameter not listed (Note 1); Permit compliance is not claimed) [at VOL-II:T2-4, REL-MISSING-ENVIRONMENTAL-PERMIT]
- VOL-II-7.2-01 (row; ACTIVE) <- VOL-II:T2-4 via REL-T24-RELIABILITY-RUN [limit_applies; link confirmed]; BLOCKED: cannot be established: the Environmental Permit issued for the site not supplied (that the reproduced Table 2-4 limits, as amended by the addenda, are the limits that govern (the Permit prevails over the reproduction), and the limit of any parameter not listed (Note 1); Permit compliance is not claimed) [at VOL-II:T2-4, REL-MISSING-ENVIRONMENTAL-PERMIT]
- VOL-V-29.3-01 (row; ACTIVE) <- VOL-II:T2-4 via REL-T24-RAMP-UP-DEDUCTIONS [limit_applies; link confirmed]; also changed directly; BLOCKED: cannot be established: the Environmental Permit issued for the site not supplied (that the reproduced Table 2-4 limits, as amended by the addenda, are the limits that govern (the Permit prevails over the reproduction), and the limit of any parameter not listed (Note 1); Permit compliance is not claimed) [at VOL-II:T2-4, REL-MISSING-ENVIRONMENTAL-PERMIT]
- VOL-V-31.1-02 (row; ACTIVE) <- VOL-II:T2-4 via REL-T24-UNAVAILABILITY [limit_applies; link confirmed]; BLOCKED: cannot be established: Volume V Schedule 7 (deductions) not supplied (the amount of the deduction for each Unavailability Event under 31.1(a), (b) and (c), so the price risk of each) [REL-MISSING-SCHEDULE-7-DEDUCTIONS]; BLOCKED: cannot be established: the Environmental Permit issued for the site not supplied (that the reproduced Table 2-4 limits, as amended by the addenda, are the limits that govern (the Permit prevails over the reproduction), and the limit of any parameter not listed (Note 1); Permit compliance is not claimed) [at VOL-II:T2-4, REL-MISSING-ENVIRONMENTAL-PERMIT]

#### Proposed relationship (47)
- ADD-03-3.2-01 (row; NEW (introduced by ADD-03:3.2)) <- ADD-03:3.2 via REL-AI-011 [depends_on; link proposed]; also changed directly
- BID-BOND-VALIDITY (date rule) <- VOL-I:6.1, VOL-I:6.3 via REL-AI-001 [feeds_calculation; link proposed]
- EV-BID-BOND (evidence item) <- VOL-I:6.4 via REL-AI-002 [depends_on; link proposed]
- EV-COMPLETION-CERT (evidence item) <- VOL-I:6.1, VOL-I:8.5#fn12 via REL-AI-005 [depends_on; link proposed]
- EV-FORM-4B (evidence item) <- VOL-I:6.1, VOL-I:8.5#fn12 via REL-AI-005 [depends_on; link proposed]
- EV-ISO (evidence item) <- VOL-I:6.1 via REL-AI-004 [depends_on; link proposed]
- EV-REFERENCES (evidence item) <- VOL-I:6.1, VOL-I:8.5#fn12 via REL-AI-005 [depends_on; link proposed]
- EV-TECH-PROPOSAL (evidence item) <- ADD-03:3.2 via REL-AI-011 [depends_on; link proposed]
- ISO-CURRENT-AT (date rule) <- VOL-I:6.1 via REL-AI-004 [depends_on; link proposed]
- MODIFY-CUTOFF (date rule) <- VOL-I:6.1 via REL-AI-003 [depends_on; link proposed]
- REFERENCE-LOOKBACK (date rule) <- VOL-I:6.1, VOL-I:8.5#fn12 via REL-AI-005 [depends_on; link proposed]
- VOL-I-11.5-01 (row; ACTIVE) <- VOL-I:11.5+ADD-03 via REL-AI-010 [depends_on; link proposed]
- VOL-I-12.2-01 (row; ACTIVE) <- VOL-I:11.5+ADD-03 via REL-AI-010 [depends_on; link proposed]
- VOL-I-12.2-02 (row; ACTIVE) <- VOL-I:11.5+ADD-03 via REL-AI-010 [depends_on; link proposed]
- VOL-I-4.2-01 (row; ACTIVE) <- VOL-I:11.5+ADD-03 via REL-AI-010 [depends_on; link proposed]
- VOL-I-6.1-01 (row; AMENDED (ADD-03/2.1(a))) <- VOL-I:6.1 via REL-AI-003 [depends_on; link proposed]; also changed directly
- VOL-I:12.1 (unit; ACTIVE) <- VOL-I:11.5+ADD-03 via REL-AI-010 [depends_on; link proposed]
- VOL-I:12.3 (unit; ACTIVE) <- VOL-I:11.5+ADD-03 via REL-AI-010 [depends_on; link proposed]
- VOL-II-2.3-01 (row; ACTIVE) <- VOL-II:2.1 via REL-AI-012 [depends_on; link proposed]
- VOL-II-2.4-01 (row; ACTIVE) <- VOL-II:T2-4/TP via REL-AI-007 [depends_on; link proposed]; BLOCKED: cannot be established: the Environmental Permit issued for the site not supplied (that the reproduced Table 2-4 limits, as amended by the addenda, are the limits that govern (the Permit prevails over the reproduction), and the limit of any parameter not listed (Note 1); Permit compliance is not claimed) [REL-MISSING-ENVIRONMENTAL-PERMIT]
- VOL-II-3.1-01 (row; ACTIVE) <- VOL-II:T2-4/TP via REL-AI-007 [depends_on; link proposed]
- VOL-II-7.2-01 (row; ACTIVE) <- VOL-II:2.1 via REL-AI-006 [depends_on; link proposed]
- VOL-II-7.2-01 (row; ACTIVE) <- VOL-II:T2-4/TP via REL-AI-007 [depends_on; link proposed]
- VOL-II-7.2-01 (row; ACTIVE) <- VOL-II:2.1 via REL-AI-012 [depends_on; link proposed]
- VOL-V-12.1-01 (row; ACTIVE) <- VOL-II:2.1 via REL-AI-006 [depends_on; link proposed]; also changed directly
- VOL-V-12.1-01 (row; ACTIVE) <- ADD-03:Q15 via REL-AI-008 [depends_on; link proposed]; also changed directly
- VOL-V-29.3-01 (row; ACTIVE) <- VOL-II:T2-4/TP via REL-AI-007 [depends_on; link proposed]; also changed directly
- VOL-V-31.1-02 (row; ACTIVE) <- VOL-II:T2-4/TP via REL-AI-007 [depends_on; link proposed]; BLOCKED: cannot be established: Volume V Schedule 7 (deductions) not supplied (the amount of the deduction for each Unavailability Event under 31.1(a), (b) and (c), so the price risk of each) [REL-MISSING-SCHEDULE-7-DEDUCTIONS]
- bond-approval (activity) <- VOL-I:6.1, VOL-I:6.3 via REL-AI-001 [feeds_calculation; link proposed]
- bond-approval (activity) <- VOL-I:6.4 via REL-AI-002 [depends_on; link proposed]
- bond-issue (activity) <- VOL-I:6.1, VOL-I:6.3 via REL-AI-001 [feeds_calculation; link proposed]
- bond-issue (activity) <- VOL-I:6.4 via REL-AI-002 [depends_on; link proposed]
- completion-certs (activity) <- VOL-I:6.1, VOL-I:8.5#fn12 via REL-AI-005 [depends_on; link proposed]
- fin-model-build (activity) <- VOL-II:2.1 via REL-AI-006 [depends_on; link proposed]
- fin-model-build (activity) <- VOL-II:T2-4/TP via REL-AI-007 [depends_on; link proposed]
- fin-model-build (activity) <- ADD-03:Q15 via REL-AI-008 [depends_on; link proposed]
- fin-model-build (activity) <- VOL-II:2.1 via REL-AI-012 [depends_on; link proposed]
- form-4b (activity) <- VOL-I:6.1, VOL-I:8.5#fn12 via REL-AI-005 [depends_on; link proposed]
- form-4b-prep (activity) <- VOL-I:6.1, VOL-I:8.5#fn12 via REL-AI-005 [depends_on; link proposed]
- form-4f (activity) <- VOL-II:2.1 via REL-AI-012 [depends_on; link proposed]
- iso-copy (activity) <- VOL-I:6.1 via REL-AI-004 [depends_on; link proposed]
- references (activity) <- VOL-I:6.1, VOL-I:8.5#fn12 via REL-AI-005 [depends_on; link proposed]
- technical-proposal (activity) <- VOL-II:2.1 via REL-AI-006 [depends_on; link proposed]
- technical-proposal (activity) <- VOL-II:T2-4/TP via REL-AI-007 [depends_on; link proposed]
- technical-proposal (activity) <- ADD-03:Q15 via REL-AI-008 [depends_on; link proposed]
- technical-proposal (activity) <- ADD-03:3.2 via REL-AI-011 [depends_on; link proposed]
- technical-proposal (activity) <- VOL-II:2.1 via REL-AI-012 [depends_on; link proposed]

#### Possible impact (0)
- none

#### Referenced but not supplied: conclusions in play that cannot be established (1)
- VOL-II-T2-4-TP (row; AMENDED (ADD-03/7.1)) <- target changed via REL-MISSING-ENVIRONMENTAL-PERMIT [missing_document; link confirmed]; also changed directly. NOT SUPPLIED: the Environmental Permit issued for the site; cannot be established: that the reproduced Table 2-4 limits, as amended by the addenda, are the limits that govern (the Permit prevails over the reproduction), and the limit of any parameter not listed (Note 1); Permit compliance is not claimed; context (not binding): ADD-01:AppB/item-5-effluent-standards p4 'the permit was under review by the regulator and that any change would be issued by Addendum.' (pre-bid minutes; they do not bind the Authority (ADD-01 3.2, p1))

### Disqualifiers (A3)

- LEAVES ADD-02-7.2-01

### Earlier answers to re-read against the new text (never revoked; a person decides)

- `ADD-01:Q1` (ADD-01): relies on VOL-II:3.1, which VOL-II:T2-4/TP (changed by ADD-03/7.1) governs through REL-T24-PROCESS-DESIGN; relies on VOL-II:3.1, which VOL-II:T2-4/TP (changed by ADD-03/7.1) governs through REL-AI-007; to be re-read against the new text of VOL-II:T2-4/TP (ADD-03/7.1); a person decides whether the answer still holds
- `ADD-01:Q3` (ADD-01): cites VOL-I:6.4, changed by ADD-03/5.1; to be re-read against the new text of VOL-I:6.4 (ADD-03/5.1); a person decides whether the answer still holds
- `ADD-01:Q5` (ADD-01): cites VOL-I:8.5#fn12, changed by ADD-03/4.2; to be re-read against the new text of VOL-I:8.5#fn12 (ADD-03/4.2); a person decides whether the answer still holds
- `ADD-01:Q6` (ADD-01): relies on VOL-V:29.3, which VOL-II:T2-4/TP (changed by ADD-03/7.1) governs through REL-AI-007; to be re-read against the new text of VOL-II:T2-4/TP (ADD-03/7.1); a person decides whether the answer still holds
- `ADD-02:Q7` (ADD-02): relies on VOL-I:12.1, which VOL-I:11.5+ADD-03 (changed by ADD-03/6.1) governs through REL-AI-010; to be re-read against the new text of VOL-I:11.5+ADD-03 (ADD-03/6.1); a person decides whether the answer still holds
- `ADD-02:Q8` (ADD-02): cites VOL-I:6.4, changed by ADD-03/5.1; to be re-read against the new text of VOL-I:6.4 (ADD-03/5.1); a person decides whether the answer still holds
- `ADD-02:Q11` (ADD-02): quotes '120,000 m³/day', a figure ADD-03/4.1(a) replaced; to be re-read against the new text of VOL-II:2.1 (ADD-03/4.1(a)); a person decides whether the answer still holds
- `ADD-02:Q13` (ADD-02): relies on VOL-I:12.2, which VOL-I:11.5+ADD-03 (changed by ADD-03/6.1) governs through REL-AI-010; relies on VOL-I:12.2, which VOL-I:11.5+ADD-03 (changed by ADD-03/6.1) governs through REL-AI-010; to be re-read against the new text of VOL-I:11.5+ADD-03 (ADD-03/6.1); a person decides whether the answer still holds

### Programme impact (status date 2026-10-22 -> 2026-11-08)

- REWORK assemble-envelope-a: requirement changed: VOL-I-6.1-01 (text, dates, status, quote)
- MOVED assemble-envelope-a: latest start 2026-11-24 -> 2026-12-08
- STATUS assemble-envelope-a: timing INFEASIBLE by 12 WD -> INFEASIBLE by 13 WD; total float -12 -> -13 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK assemble-envelope-b: requirement changed: VOL-I-6.1-01 (text, dates, status, quote)
- MOVED assemble-envelope-b: latest start 2026-11-24 -> 2026-12-08
- STATUS assemble-envelope-b: timing OK -> INFEASIBLE by 1 WD; total float 0 -> -1 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- STATUS attendance-notice: timing CONDITIONAL — window elapsed 2026-10-14; whether the condition arose is not known -> CONDITIONAL — window elapsed 2026-10-14; whether the condition arose is not known; total float -7 -> -18 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK bond-approval: requirement changed: VOL-I-6.3-01 (text, dates, status, quote, parameters), VOL-I-6.4-01 (text, status, quote, parameters), VOL-I-6.4-02 (text, status)
- MOVED bond-approval: latest start 2026-11-05 -> 2026-11-19
- STATUS bond-approval: timing OK -> OK; total float +10 -> +9 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK bond-issue: requirement changed: VOL-I-6.3-01 (text, dates, status, quote, parameters), VOL-I-6.4-01 (text, status, quote, parameters), VOL-I-6.4-02 (text, status)
- MOVED bond-issue: latest start 2026-11-19 -> 2026-12-03
- STATUS bond-issue: timing OK -> OK; total float +10 -> +9 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK clarifications: requirement changed: VOL-I-3.4-01 (dates, parameters), VOL-I-5.2-01 (dates, parameters)
- MOVED clarifications: latest start 2026-11-11 -> 2026-11-25
- STATUS clarifications: timing OK -> OK; total float +13 -> +12 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED completion-certs: latest start 2026-11-02 -> 2026-11-16
- STATUS completion-certs: timing OK -> OK; total float +7 -> +6 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED consortium-check: latest start 2026-11-10 -> 2026-11-24
- STATUS consortium-check: timing OK -> OK; total float +13 -> +12 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK copies: requirement changed: VOL-I-6.1-01 (text, dates, status, quote)
- MOVED copies: latest start 2026-11-25 -> 2026-12-09
- STATUS copies: timing INFEASIBLE by 12 WD -> INFEASIBLE by 13 WD; total float -12 -> -13 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK deliver: requirement changed: VOL-I-6.1-01 (text, dates, status, quote)
- MOVED deliver: latest start 2026-11-26 -> 2026-12-10
- STATUS deliver: timing INFEASIBLE by 12 WD -> INFEASIBLE by 13 WD; total float -12 -> -13 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK deviations-review: requirement changed: VOL-V-12.1-01 (consequence, quote), VOL-V-29.3-01 (cited units, quote: cited unit VOL-II T2-4/TP: Limit 1 -> 0.5 mg/l by ADD-03/7.1), VOL-V-31.1-02 (dependency: VOL-II T2-4/TP: Limit 1 -> 0.5 mg/l by ADD-03/7.1 (depends on it: REL-T24-UNAVAILABILITY (limit_applies, confirmed)))
- MOVED deviations-review: latest start 2026-11-08 -> 2026-11-22
- STATUS deviations-review: timing OK -> OK; total float +11 -> +10 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED fin-assumptions: latest start 2026-11-22 -> 2026-12-06
- STATUS fin-assumptions: timing OK -> OK; total float +5 -> +4 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK fin-model-build: requirement changed: ADD-03-Q17-01 (text, status, consequence, quote)
- MOVED fin-model-build: latest start 2026-10-22 -> 2026-11-05
- STATUS fin-model-build: timing OK -> INFEASIBLE by 1 WD; total float 0 -> -1 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK fin-model-freeze: requirement changed: ADD-03-Q17-01 (text, status, consequence, quote)
- MOVED fin-model-freeze: latest start 2026-11-12 -> 2026-11-26
- STATUS fin-model-freeze: timing OK -> INFEASIBLE by 1 WD; total float 0 -> -1 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED fin-standing: latest start 2026-11-19 -> 2026-12-03
- STATUS fin-standing: timing OK -> OK; total float +15 -> +14 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED fin-statements: latest start 2026-11-12 -> 2026-11-26
- STATUS fin-statements: timing OK -> OK; total float +15 -> +14 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK form-4a: requirement changed: ADD-01-AppA-01 (Addenda to acknowledge: ADD-03 issued since ADD-02: 'Bidders shall acknowledge receipt in Form 4-A.'), ADD-03-cover-01 (text, status, consequence, quote, parameters), VOL-I-7.1-01 (dates), VOL-IV-F4A-01 (anchor date: PDD moved 2026-11-26 -> 2026-12-10 (VOL-I 6.1 as amended by ADD-01 2.1, ADD-03 2.1); ADD-01 AppA/proposal-due-date prints 2026-11-12: CONFLICT with the amended PDD, not corrected (a person decides)), VOL-IV-F4A-02 (anchor date: PDD moved 2026-11-26 -> 2026-12-10 (VOL-I 6.1 as amended by ADD-01 2.1, ADD-03 2.1); ADD-01 AppA/proposal-due-date prints 2026-11-12: CONFLICT with the amended PDD, not corrected (a person decides))
- MOVED form-4a: latest start 2026-11-23 -> 2026-12-07
- STATUS form-4a: timing OK -> OK; total float +12 -> +11 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK form-4a-prep: requirement changed: ADD-01-AppA-01 (Addenda to acknowledge: ADD-03 issued since ADD-02: 'Bidders shall acknowledge receipt in Form 4-A.'), ADD-03-cover-01 (text, status, consequence, quote, parameters), VOL-I-7.1-01 (dates), VOL-IV-F4A-01 (anchor date: PDD moved 2026-11-26 -> 2026-12-10 (VOL-I 6.1 as amended by ADD-01 2.1, ADD-03 2.1); ADD-01 AppA/proposal-due-date prints 2026-11-12: CONFLICT with the amended PDD, not corrected (a person decides)), VOL-IV-F4A-02 (anchor date: PDD moved 2026-11-26 -> 2026-12-10 (VOL-I 6.1 as amended by ADD-01 2.1, ADD-03 2.1); ADD-01 AppA/proposal-due-date prints 2026-11-12: CONFLICT with the amended PDD, not corrected (a person decides))
- MOVED form-4a-prep: latest start 2026-11-22 -> 2026-12-06
- STATUS form-4a-prep: timing OK -> OK; total float +20 -> +19 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED form-4b: latest start 2026-11-23 -> 2026-12-07
- STATUS form-4b: timing OK -> OK; total float +7 -> +6 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED form-4b-prep: latest start 2026-11-18 -> 2026-12-02
- STATUS form-4b-prep: timing OK -> OK; total float +9 -> +8 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED form-4c-prep: latest start 2026-11-17 -> 2026-12-01
- STATUS form-4c-prep: timing OK -> OK; total float +18 -> +17 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED form-4c-sign: latest start 2026-11-19 -> 2026-12-03
- STATUS form-4c-sign: timing OK -> OK; total float +10 -> +9 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK form-4e: requirement changed: VOL-V-12.1-01 (consequence, quote), VOL-V-29.3-01 (cited units, quote: cited unit VOL-II T2-4/TP: Limit 1 -> 0.5 mg/l by ADD-03/7.1), VOL-V-31.1-02 (dependency: VOL-II T2-4/TP: Limit 1 -> 0.5 mg/l by ADD-03/7.1 (depends on it: REL-T24-UNAVAILABILITY (limit_applies, confirmed)))
- MOVED form-4e: latest start 2026-11-22 -> 2026-12-06
- STATUS form-4e: timing OK -> OK; total float +1 -> 0 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK form-4f: requirement changed: ADD-03-Q17-01 (text, status, consequence, quote)
- MOVED form-4f: latest start 2026-11-22 -> 2026-12-06
- STATUS form-4f: timing OK -> INFEASIBLE by 1 WD; total float 0 -> -1 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK form-4g-review: requirement changed: ADD-02-F4G-01 (stale), ADD-02-F4G-02 (stale), ADD-02-F4G-03 (stale), ADD-02-F4G-04 (stale), ADD-02-F4G-05 (stale), ADD-02-F4G-06 (stale), ADD-02-F4G-07 (stale)
- MOVED form-4g-review: latest start 2026-11-16 -> 2026-11-30
- STATUS form-4g-review: timing OK -> OK; total float +17 -> +16 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK form-4g-sign: requirement changed: ADD-02-F4G-01 (stale), ADD-02-F4G-02 (stale), ADD-02-F4G-03 (stale), ADD-02-F4G-04 (stale), ADD-02-F4G-05 (stale), ADD-02-F4G-06 (stale), ADD-02-F4G-07 (stale)
- MOVED form-4g-sign: latest start 2026-11-23 -> 2026-12-07
- STATUS form-4g-sign: timing OK -> OK; total float +12 -> +11 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED ground-dd: latest start 2026-10-29 -> 2026-11-12
- STATUS ground-dd: timing OK -> OK; total float +5 -> +4 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED investment-licence: latest start 2026-11-17 -> 2026-12-01
- STATUS investment-licence: timing OK -> OK; total float +8 -> +7 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK iso-copy: requirement changed: VOL-I-8.3-01 (dates, parameters)
- MOVED iso-copy: latest start 2026-11-22 -> 2026-12-06
- STATUS iso-copy: timing OK -> OK; total float +21 -> +20 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED lcc-certificate: latest start 2026-10-13 -> 2026-10-27
- STATUS lcc-certificate: timing INFEASIBLE by 12 WD -> INFEASIBLE by 13 WD; total float -12 -> -13 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED lcc-ratio: latest start 2026-10-06 -> 2026-10-20
- STATUS lcc-ratio: timing INFEASIBLE by 12 WD -> INFEASIBLE by 13 WD; total float -12 -> -13 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED lender-terms: latest start 2026-10-29 -> 2026-11-12
- STATUS lender-terms: timing OK -> OK; total float +5 -> +4 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED model-audit-opinion: latest start 2026-11-15 -> 2026-11-29
- STATUS model-audit-opinion: timing OK -> INFEASIBLE by 1 WD; total float 0 -> -1 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED model-audit-review: latest start 2026-11-01 -> 2026-11-15
- STATUS model-audit-review: timing OK -> OK; total float +1 -> 0 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED model-auditor-appoint: latest start 2026-10-25 -> 2026-11-08
- STATUS model-auditor-appoint: timing OK -> OK; total float +1 -> 0 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED om-evidence: latest start 2026-11-10 -> 2026-11-24
- STATUS om-evidence: timing OK -> OK; total float +13 -> +12 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED pcg-execution: latest start 2026-11-10 -> 2026-11-24
… 49 more lines in [diff.md](diff.md)

## Next (a person)

- read the unresolved and escalated provisions first, then each item against its evidence (`../ai/ADD-03-run-host-20261015T131927Z-745a-combined/proposals.yaml`, `../downstream/proposals.yaml`)
- nothing here is applied to the real curation: to take an item over, add the PDF to the pack (OPERATING_GUIDE §3 steps 1-2) and copy the reviewed files listed in `promotion.json`; then `pin`, `check-register`, `outputs` and decide with `accept` / `reject` as usual
