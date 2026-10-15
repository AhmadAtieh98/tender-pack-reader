# Review packet: ADD-03, AI workflow run ADD-03-run-host-20261015T140902Z-ab89

> **CANDIDATE: proposed by the AI workflow; not reviewed; nothing accepted.** Statuses are the controller's; a person decides every item. The real `curation/`, `config/` and `out/` were only read: everything below lives in this run's folder.

- PDF: `/Users/ahmad/Desktop/lamar claude code/interview-release/LAMAR-PPP-R2-INTERVIEW_cbe0e94+wt_20261011T1109Z/staging/panel/uploads/6f9f9d7c7d68bc83b947d20fa348271b91695463eae5435a70b09afd1955ad25.pdf` (sha256 6f9f9d7c7d68bc83…, 2 pages); preceding state: pack `/Users/ahmad/Desktop/lamar claude code/interview-release/LAMAR-PPP-R2-INTERVIEW_cbe0e94+wt_20261011T1109Z/config/pack.yaml` (NUPA-ISTP-2026-014), previous evidence build `/Users/ahmad/Desktop/lamar claude code/interview-release/LAMAR-PPP-R2-INTERVIEW_cbe0e94+wt_20261011T1109Z/build`
- route **host**; model requested `claude-code headless (claude-opus-5-5)`, reported `None`; host sessions report: claude-opus-5-5
- status **partial**: 4 provision(s) unresolved in the candidate (listed first in the review packet); 12 downstream task(s) answered only by items that cannot be promoted: row:ADD-02-F4G-01, row:ADD-02-F4G-02, row:ADD-02-F4G-03, row:ADD-02-F4G-04, row:ADD-02-F4G-05, act:form-4g-review, act:form-4g-sign, esc:ADD-03:2.2 …; check-register on the candidate: exit 1, 4 finding(s) {'pending_settled': 4} (0 missing because the downstream phase did not propose them, 4 defect(s))
- usage (application routes): none: the run's route is host, every exchange ran in a host session (below)
- host sessions: 25 (their own records); usage of the 25 that reported it: input 194, cache write 1340787, cache read 3810109 / output 403006 tokens
- code at start: content b6165e419b112854… over 103 files; git not available; recorded 2026-10-15T14:09:03Z

## Execution, completeness and approval (three separate things)

- **Execution** (what ran): ingest done, readings done, analysis done, validation done, downstream done, downstream_validation done, critic done, promotion done, pin done, check_register done, outputs done, diff done, review running; batches analysis: {'done': 4}; downstream: {'done': 10}
- **Completeness** (what the run completed): **partial**: 4 provision(s) unresolved in the candidate (listed first in the review packet); 12 downstream task(s) answered only by items that cannot be promoted: row:ADD-02-F4G-01, row:ADD-02-F4G-02, row:ADD-02-F4G-03, row:ADD-02-F4G-04, row:ADD-02-F4G-05, act:form-4g-review, act:form-4g-sign, esc:ADD-03:2.2 …; check-register on the candidate: exit 1, 4 finding(s) {'pending_settled': 4} (0 missing because the downstream phase did not propose them, 4 defect(s))
  - downstream tasks: 57; answered 45; unanswered 0; answered only by items that cannot be promoted 12; answered 'no change' 11
- **Human approval**: **simulated** (INTERVIEW DEMO: eligible reviews assumed approved on the owner's instruction; no actual human review or tender release); decisions a person recorded in the candidate's decisions file: accept row ADD-01-3.1-01 by Interview demo assumption (2026-10-11); accept row ADD-01-AppA-01 by Interview demo assumption (2026-10-11); accept row ADD-01-Q4-01 by Interview demo assumption (2026-10-11); accept op ADD-01/2.1 by Interview demo assumption (2026-10-11); accept op ADD-01/2.2 by Interview demo assumption (2026-10-11); accept op ADD-01/3.1 by Interview demo assumption (2026-10-11); accept op ADD-01/3.2 by Interview demo assumption (2026-10-11); accept op ADD-01/4.1 by Interview demo assumption (2026-10-11); accept op ADD-01/4.2 by Interview demo assumption (2026-10-11); accept op ADD-01/5.1 by Interview demo assumption (2026-10-11)

## What is candidate and what is real

- **Candidate** (proposed by this run, nothing accepted): `../candidate/` — a copy of the curation and configuration with ADD-03 added, its evidence build, its op file, rows, issues, templates and outputs.
- **Last validated state**: `../candidate/out-before/` (the pre-addendum outputs built from the copied curation and the previous evidence build; done)
- **Real** (untouched): `curation/`, `config/`, `out/`; the owner's approvals and readings were copied unchanged and used read-only.

- real inputs changed since the run started: none

## Candidate outputs

Exit 0 (INTERVIEW DEMO (assumed approvals; not a tender release)); every file carries the banner (`../candidate/out/CANDIDATE.md`); A1 has a candidate status column {'DECIDED': 205, 'UNRESOLVED': 5}.

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
- **Candidate** (CANDIDATE — NOT VALIDATED; ADD-03 as proposed): [a3/a3_candidate.pdf](../candidate/out/a3/a3_candidate.pdf) (8 page(s)), [a3/a3_candidate.md](../candidate/out/a3/a3_candidate.md), [a5/candidate/README.md](../candidate/out/a5/candidate/README.md), [a5/candidate/gantt.html](../candidate/out/a5/candidate/gantt.html)

**What may be changing.** ADD-03 is PARTIAL: 2 of 19 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 13 op(s) that are valid there stood (each still a proposal: review accepted 13), A3 would gain 1 row(s) (ADD-03-cover-para3-01 (ADD-03/cover/para3)), lose 1 (ADD-02-7.2-01 (ADD-03/3.1(a))) and change 5 (ADD-02-F4G-04 (register), VOL-I-6.1-01 (ADD-03/2.1), VOL-I-6.3-01 (ADD-03/5.2(a)), VOL-I-6.4-01 (ADD-03/5.1) and 1 more); A5, replanned at ADD-03's issue date (2026-11-08), would move the latest dates of 43 activities (assemble-envelope-a, assemble-envelope-b, bond-approval, bond-issue and 39 more), add 0 (none) and remove 0 (none), and marks 8 REVIEW through relationships. Not settled: 8 activities blocked by an unresolved row (references, bond-approval, clarifications, form-4g-review and 4 more), 5 STALE row(s), 0 obligation(s) reaching no output (C46), 9 relationship chain(s) blocked or incomplete, 1 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT and 7 more. Nothing here is validated, accepted or applied to the real state.

- ENTERS ADD-03-cover-para3-01: gate (pass/fail gate); ops ADD-03/cover/para3 (interpretation_pending)
- CHANGES ADD-02-F4G-04: now STALE; ops none (status NEW -> ACTIVE (as amended by ADD-02/7.1); NOT SETTLED: STALE at ADD-03: its reading was not re-made (ADD-02:7.2 changed since ADD-02 (by ADD-03/3.1(a))))
- CHANGES VOL-I-6.1-01: text: “Deliver the Proposal to the Authority by the Proposal Due Date and time, at the Appendix 3 address — “Thursday 26 Novem…” -> “Deliver the Proposal to the Authority by the Proposal Due Date and time, at the Appendix 3 address — “not later than 14…”; ops ADD-03/2.1 (interpretation_pending)
- CHANGES VOL-I-6.3-01: text: “Bid Bond valid for 210 days from the Proposal Due Date (extendable on demand) — “valid for one hundred and eighty (180)…” -> “Bid Bond valid for 210 days from the Proposal Due Date (extendable on demand)”; ops ADD-03/5.2(a) (evidence_verified)
- CHANGES VOL-I-6.4-01: text: “Bid Bond of SAR 5,600,000, unconditional and payable on first written demand — “in the amount of SAR 4,500,000”” -> “Bid Bond of SAR 5,600,000, unconditional and payable on first written demand”; ops ADD-03/5.1 (evidence_verified)
- CHANGES VOL-I-8.5-01: text: “Evidence at least two (2) reference sewage treatment plants of at least 100,000 m3/day, each having achieved commercial…” -> “Evidence at least two (2) reference sewage treatment plants of at least 100,000 m3/day, each having achieved commercial…”; ops ADD-03/4.2(a) (evidence_verified), ADD-03/4.2(b) (evidence_verified)
- LEAVES ADD-02-7.2-01: was explicit (non-responsive); ops ADD-03/3.1(a) (evidence_verified)

- blockers: 2 unresolved provision(s), 8 blocked activit(y/ies), 5 STALE row(s), 0 C46 gap(s), 9 relationship chain(s) blocked or incomplete, 1 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT, I-VOL-III, I-ADD03-ISO-DATE, I-VOL-II-MISSING, I-VOL-V-MISSING, I-VOL-II-COMPLIANCE-POINT, I-VOL-IV-SCALE, I-OP-ADD-01/Q4
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
| ingest | 7.1 | done |
| readings | 0.0 | done |
| analysis | 558.5 | done |
| validation | 2.2 | done |
| downstream | 534.6 | done |
| downstream_validation | 0.4 | done |
| critic | 326.5 | done |
| promotion | 8.6 | done |
| pin | 0.6 | done |
| check_register | 1.9 | done |
| outputs | 9.9 | done |
| diff | 1.8 | done |
| review | 0.0 | running |
| **total** | **1452.1** (24.2 min) | target 30 min from the PDF to candidate outputs and this packet, human review excluded |

## First: unresolved provisions and escalations

4 of 19 provisions are not applied or settled by a promoted item (each is `unresolved` in the candidate op file with the reason); 2 escalation(s).
- states (session 14: kept distinct): applied 9, no effect 6, partly applied 2, unresolved but accounted for 2, unaccounted 0; approved by a person: none (only a person's recorded decision approves; see Human approval above)

- **ESCALATED ESC-ADD-03:3.1-form** (ADD-03:3.1): software limitation: ADD-03:3.1 withdraws the whole of Form 4-G ('Form 4-G (Cybersecurity Compliance Undertaking), added by Addendum No. 2 Section 7, is withdrawn.'), which is the 9-member group ADD-02:F4-G (heading ADD-02:H:F4-G, table ADD-02:F4-G/T1 with rows /1 to /6, paragraph ADD-02:F4-G/para1…
  - unsupported: A status change (withdrawal/revocation) of a whole group (form) named only by its form number: set_status takes a single unit and the engine does not accept the group's members as cited. Also not represented: the listing of Form 4-G at Volume I Clause 9.1 'to be inserted after item (e)' by ADD-02:7…
  - evidence: ADD-03:3.1 p1: “Form 4-G (Cybersecurity Compliance Undertaking), added by Addendum No. 2 Section 7, is withdrawn. Bidders shall disregard it and shall not submit it.”; ADD-02:H:F4-G p3: “FORM 4-G — CYBERSECURITY COMPLIANCE UNDERTAKING”; ADD-02:7.1 p3: “A new Form 4-G is added to Volume IV and to the list at Volume I Clause 9.1, to be inserted after item (e).”
  - affected scope: units ADD-02:7.2, ADD-02:F4-G/T1, ADD-02:F4-G/T1/1, ADD-02:F4-G/T1/2, ADD-02:F4-G/T1/3, ADD-02:F4-G/T1/4, ADD-02:F4-G/T1/5, ADD-02:F4-G/T1/6, ADD-02:F4-G/para1, ADD-02:H:F4-G, ADD-02:H:S7; rows ADD-02-7.2-01, ADD-02-F4G-01, ADD-02-F4G-02, ADD-02-F4G-03, ADD-02-F4G-04, ADD-02-F4G-05, ADD-02-F4G-06, ADD-02-F4G-07; activities form-4g-review, form-4g-sign; clarifications none
- **ESCALATED ESC-ADD-03:4.1-table** (ADD-03:4.1): software limitation: ADD-03:4.1 names 'Table 2-6 row 2-6.1' ('In Volume II Clause 2.1 and in Table 2-6 row 2-6.1, ‘120,000 m³/day’ is deleted and ‘150,000 m³/day’ is substituted.'), but the engine resolves the provision's citations to ['VOL-II:2.1'] only: set_value on VOL-II:T2-6/2-6.1 (column Valu…
  - unsupported: The citation resolver does not link 'Table 2-6 row 2-6.1' / 'row 2-6.2' to VOL-II:T2-6/2-6.1 and VOL-II:T2-6/2-6.2, so no cell op or annotate can be applied; and a quoted old/new string spanning the Value and Unit cells has no direct set_value form. Document control to record the row 2-6.1 Value ch…
  - evidence: ADD-03:4.1 p1: “In Volume II Clause 2.1 and in Table 2-6 row 2-6.1, ‘120,000 m³/day’ is deleted and ‘150,000 m³/day’ is substituted. The peak hourly flow in Table 2-6 row 2-6.…”; VOL-II:T2-6/2-6.1 p3: “120,000”; VOL-II:T2-6/2-6.2 p3: “7,500”
  - affected scope: units VOL-II:2.1; rows VOL-II-2.1-01; activities technical-proposal; clarifications none
- **UNRESOLVED ADD-03:2.2** (clause, p1): unresolved (accounted for by the promoted `unresolved` disposition ADD-03/2.2-disp; nothing applied): ambiguous: 'Every period calculated by reference to the Proposal Due Date is adjusted accordingly.' names no clause, unlike ADD-01:2.2 which listed Volume I Clauses 5.2, 6.3, 7.1 and footnote 12 to Clause 8.5. Reading A: the same periods ADD-01:2.2 listed; Reading B: every PDD-referenced period in the RFP Documents at ADD-03, including any this Addendum amends elsewhere (Bid Bond, Proposal validi…
- **UNRESOLVED ADD-03:4.3** (clause, p1): unresolved (accounted for by the promoted `unresolved` disposition DISP-ADD03-4.3; nothing applied): ambiguous: ADD-03:4.3 prints only 'Volume I Clause 1.3 is amended correspondingly.' and no old/new words. VOL-I:1.3 at ADD-02 reads 'nominal capacity one hundred and twenty thousand cubic metres per day (120,000 m³/day)'. Reading (a): both the spelled-out words and the figure are amended to correspond to the 150,000 m³/day substituted by ADD-03:4.1 (the new spelled-out words are not printed anywh…

## Earlier answers to re-read against the new text (never revoked; a person decides)

- `ADD-01:Q1` (ADD-01): relies on VOL-II:3.1, which VOL-II:T2-4/TP (changed by ADD-03/7.1) governs through REL-T24-PROCESS-DESIGN; to be re-read against the new text of VOL-II:T2-4/TP (ADD-03/7.1); a person decides whether the answer still holds (downstream task `reread:ADD-01:Q1`)
- `ADD-01:Q3` (ADD-01): cites VOL-I:6.4, changed by ADD-03/5.1; to be re-read against the new text of VOL-I:6.4 (ADD-03/5.1); a person decides whether the answer still holds (downstream task `reread:ADD-01:Q3`)
- `ADD-01:Q5` (ADD-01): cites VOL-I:8.5#fn12, changed by ADD-03/4.2(a); to be re-read against the new text of VOL-I:8.5#fn12 (ADD-03/4.2(a)); a person decides whether the answer still holds (downstream task `reread:ADD-01:Q5`)
- `ADD-02:Q7` (ADD-02): relies on VOL-I:12.1, which VOL-I:11.5+ADD-03 (changed by ADD-03/6.1) governs through REL-AI-003; to be re-read against the new text of VOL-I:11.5+ADD-03 (ADD-03/6.1); a person decides whether the answer still holds
- `ADD-02:Q8` (ADD-02): cites VOL-I:6.4, changed by ADD-03/5.1; to be re-read against the new text of VOL-I:6.4 (ADD-03/5.1); a person decides whether the answer still holds (downstream task `reread:ADD-02:Q8`)
- `ADD-02:Q11` (ADD-02): quotes '120,000 m³/day', a figure ADD-03/4.1(a) replaced; to be re-read against the new text of VOL-II:2.1 (ADD-03/4.1(a)); a person decides whether the answer still holds (downstream task `reread:ADD-02:Q11`)

## Derived effects (session 12: pending readings, computed deadlines, conditions, consequences)

## Computed deadlines and the Working Days left (PROPOSED; nothing typed)

- Working Days left from the issue date (2026-11-08) to the PDD (2026-12-10): 24 (the issue date not counted, the PDD counted; Working Days per VOL-I 2.4 (weekend [4, 5] as date.weekday numbers; holidays none declared))
- no 'N days before/after' deadline in the addendum's provisions

## Conditional impact investigations (CONDITIONAL; never accepted facts)

- `impact:ADD-03:2.2` conditional on disposition ADD-03:2.2 (unresolved: ambiguous: 'Every period calculated by reference to the Proposal Due Date is adjusted accordingly.' names no clause, unlike ADD-01:2.2 which listed Volume I Clauses 5.2, 6.3, 7.1 and footnote 12 to C…): investigate the rows, activities and prices that rest on VOL-I:5.2, VOL-I:6.3, VOL-I:7.1, VOL-I:8.5#fn12
- `impact:ADD-03:4.3` conditional on disposition ADD-03:4.3 (unresolved: ambiguous: ADD-03:4.3 prints only 'Volume I Clause 1.3 is amended correspondingly.' and no old/new words. VOL-I:1.3 at ADD-02 reads 'nominal capacity one hundred and twenty thousand cubic metres per …): investigate the rows, activities and prices that rest on VOL-I:1.3

## Per provision: source evidence → proposed transition → validation → downstream impact → output difference

### ADD-03:cover/para1 (paragraph, p1) — no effect (PROPOSED; not approved)
- source: “Issued 8 November 2026”
- transition: `ADD-03/cover/para1-disp` disposition no_effect: Issue-date line 'Issued 8 November 2026': it records the Addendum's date of issue (the stage date) and amends, obliges or excepts nothing.
  - validation: **evidence_verified**

### ADD-03:cover/para2 (paragraph, p1) — no effect (PROPOSED; not approved)
- source: “Tender NUPA/ISTP/2026/014”
- transition: `ADD-03/cover/para2-disp` disposition no_effect: Title line 'Tender NUPA/ISTP/2026/014' under the heading 'ADDENDUM NO. 3': identifies the tender and the Addendum; amends, obliges or excepts nothing.
  - validation: **evidence_verified**

### ADD-03:cover/para3 (paragraph, p1) — applied (PROPOSED; not approved)
- source: “This Addendum amends the Proposal Due Date and Bid Bond, withdraws Form 4-G, increases the nominal capacity with a consequential change to the reference project threshold, amends Table 2-4, adds a new Clause 11.6, and responds to clarification requests 15 to 18. This Addendum forms part of the RFP Documents and takes precedence in accordance with Volume I C…”
- transition: `ADD-03/cover/para3` amendment_op annotate ADD-03:cover/para3 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The core reading holds. 'Bidders shall acknowledge receipt in Form 4-A.' is printed in ADD-03:cover/para3, so annotating the cover with an obligation on its own unit fits the words. The uncertain_target flag comes from this being a self-annotation, not from a wrong unit.
    - concern: The rationale relies on the 'accepted' ADD-02/cover/para3 annotation as a precedent. That acceptance has origin interview_demo ('no observed human review'). It is not a human decision and should not be presented as a precedent supporting this item.
    - concern: The note says the precedence sentence only restates VOL-I:3.2(a). That is consistent with '(a) the Addenda, a later Addendum prevailing over an earlier one;'. However, the cover's summary list (PDD, Bid Bond, Form 4-G withdrawal, capacity/threshold, Table 2-4, Clause 11.6, Q15-18) is only deferred …
    - concern: 'All other terms of the RFP Documents remain unchanged.' is not explicitly accounted for in the note. It should be recorded as a cover statement with no amending effect, so that no provision of the paragraph goes unaccounted.
    - concern: The op lists no dependencies beyond itself. Form 4-A has been reissued (ADD-01 App A; VOL-IV:F4-A/item1 is 'superseded'). The open issue I-F4A-FIELDS and the Form 4-A execution rule in VOL-I:9.3 are directly affected by a new acknowledgement obligation and should be named.
- transition: `ADD-03/row-ack` row_new {"row": {"id": "R-ADD03-ACK", "group": "submission", "scope": ["Bidder"], "requirement": "Bidders shall acknowledge receipt in Form 4-A.", "units": ["ADD-03:cover/para3", "VOL-IV:F4-A/item1"], "disci…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Wrong effective text. The row cites VOL-IV:F4-A/item1 and says receipt 'is acknowledged in Form 4-A paragraph 1 ("including Addenda numbered ______ to ______ ...")'. That unit has status 'superseded'. Row VOL-IV-F4A-03 is evaluated as 'REPLACED (by ADD-01:AppA)', and its note says 'The reissued For…
    - concern: The open issue I-F4A-FIELDS is not linked. It covers the reissued form's 'acknowledgement of Addenda at paragraph 1' purpose with no paragraph 1, its dropped fields and its stale printed PDD. ADD-03 also amends the Proposal Due Date, which makes the stale-PDD point worse. None of this is mentioned.
    - concern: Consequence: not inferring non-responsiveness from VOL-I:9.3 is correct. But whether a missing or wrong addenda acknowledgement counts as an 'improperly executed Form 4-A' ('An unsigned or improperly executed Form 4-A shall render the Proposal non-responsive.') is a genuine ambiguity. It should go …
    - concern: The row's metadata does not match the existing Form 4-A rows (VOL-I-9.3-01, VOL-IV-F4A-03): scope ['Bidder'] and group 'submission' versus envelope_A/forms/addenda_acknowledgement; evidence [] versus EV-FORM-4A; assessment 'procedural' versus pass_fail; and no owner. Possible overlap with ADD-01-Ap…
    - concern: The row should cite the reissued Form 4-A unit (ADD-01 App A field) that carries the acknowledgement at ADD-02, not the superseded VOL-IV paragraph. As proposed, the target and units are not certain and should be escalated as an uncertain target.
    - concern: The interview_demo 'accepted' reviews of VOL-IV-F4A-03, I-F4A-FIELDS and I-NO-CONSEQUENCE are not human decisions. Nothing here should rely on them as settled.
  - downstream proposal `D-ADD03-06` row_new (c46:ADD-03/cover/para3): **interpretation_pending**
  - downstream proposal `D-ADD03-07` dependency (c46:ADD-03/cover/para3): **interpretation_pending**
  - downstream proposal `DS-ADD03-004` no_change (act:form-4a-prep): **interpretation_pending**
  - downstream proposal `DS-ADD03-005` dependency (act:form-4a-prep): **interpretation_pending**
  - output difference: NEW ADD-03-cover-para3-01; A5 REWORK form-4a; A5 REWORK form-4a-prep; A5 REVIEW (proposed relationship) form-4a; A5 REVIEW (proposed relationship) form-4a-prep

### ADD-03:1.1 (clause, p1) — no effect (PROPOSED; not approved)
- source: “This Addendum takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.”
- transition: `ADD-03/1.1-disp` disposition no_effect: Recital: 'This Addendum takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.' It applies the existing order of precedence, VOL-I:…
  - validation: **evidence_verified**

### ADD-03:2.1 (clause, p1) — applied (PROPOSED; not approved)
- source: “Volume I Clause 6.1 is amended by deleting ‘Thursday 26 November 2026’ and substituting ‘Thursday 10 December 2026’, 14:00 Riyadh time.”
- transition: `ADD-03/2.1` amendment_op replace_text VOL-I:6.1 “Thursday 26 November 2026” → “Thursday 10 December 2026”
  - validation: **interpretation_pending**
  - downstream: units changed VOL-I:6.1; rows citing them VOL-I-6.1-01
  - downstream proposal `D-VOL-I-3.4-READING` row_reading (row:VOL-I-3.4-01): **interpretation_pending — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
      - concern: The 3 Oct 2026 direction is carried forward 'unchanged', but its dependency, the PDD, did change. The note does name the direction and says only the PDD moved, and the reading stays pending a person. The reviewer should still confirm that the direction applies to the new date and is not re-decided …
      - concern: VOL-I 3.4 says only 'after the Proposal Due Date'. The time element '14:00 hours' in the cut-off comes from the recorded owner direction, not from the words of 3.4. This is not new, but it is still not stated in 3.4.
      - concern: The clarification date (Thursday 26 November 2026) depends on the quoted calculate output, which cannot be reproduced here. The earlier row called its date 'the planning reading'. This item now says 'single reading' (readings_differ: false). That is consistent with the quoted tool output.
      - concern: The note says the new clarification cut-off falls on the old omission-claim cut-off date. This is accurate and useful for the bid team, and the note correctly keeps the two cut-offs separate. The interview_demo record and the I-VOL-III issue are kept as recorded and are not treated as resolved.
  - downstream proposal `D-VOL-I-5.2-READING` row_reading (row:VOL-I-5.2-01): **interpretation_pending**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
      - concern: The dependencies list only VOL-I-6.1-01. Row VOL-I-3.4-01 states its own cut-off as separate from this deadline and quotes this deadline's date in a parameter, so it could be listed too. So could any clarification-register or A5 items that use this cut-off, though none are shown in the request.
      - concern: The computed date (Thursday 26 November 2026) depends on the quoted calculate output, which cannot be reproduced here. It is correctly kept out of the date rule.
  - downstream proposal `D-VOL-I-6.1-READING` row_reading (row:VOL-I-6.1-01): **interpretation_pending**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
      - concern: The note relies on 'the VOL-I 7.1 Proposal validity, whose length ADD-03 5.2 states is unchanged'. Neither VOL-I:7.1 nor ADD-03:5.2 is printed in the request, so I cannot check this. It should be backed by quoted evidence or removed.
      - concern: The note says VOL-I-6.3-01 is 're-read in this set', but no reading of VOL-I-6.3-01 is among the items reviewed here, so I cannot check that.
      - concern: ADD-03 2.1 ends with '14:00 Riyadh time'; the target reads '14:00 hours Riyadh time'. Treating this as a restatement of the unchanged time is reasonable, and the note quotes both. The quote and the VOL-I 6.6 consequence ('will be rejected unopened and returned to the Bidder') match the evidence.
  - downstream proposal `DS-ADD03-R-6.7-01` row_reading (row:VOL-I-6.7-01): **interpretation_pending**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
      - concern: The reading treats the VOL-I 6.7 cut-off ('before the Proposal Due Date') as following the date in VOL-I 6.1 as amended. The earlier recorded reading relied on VOL-I 2.6 for that link, but VOL-I 2.6 is not printed in this request and the item's note does not cite it. The carry-over to 10 December 2…
      - concern: The note says 'The time is unchanged: 14:00 hours Riyadh time' but quotes only VOL-I 6.1. ADD-03:2.1 itself ends with ', 14:00 Riyadh time', outside the quoted substitution. The op replaces only the date, which fits reading that phrase as a restatement. The item should quote the provision's own tra…
      - concern: The parameter express_late_prohibition ('modifications only ... not extended to withdrawals') carries the owner's session-08 direction. That direction named 26 November 2026, and the review behind it is interview_demo origin ('no observed human review'). The item correctly leaves the carry-over to …
      - concern: The statement relied on, downstream-003/S-F-REVIEW-ORIGIN, cites as evidence VOL-I:6.4 'The Bid Bond shall be in the amount of SAR 5,600,000'. That span does not support a statement about review origin and status. VOL-I:6.4 is printed in this request only at SAR 4,500,000 (before the addendum), and…
      - concern: S-F-REVIEW-ORIGIN names ADD-03 ops 4.2(a), 4.2(b), 5.1 and 5.2(b). Of these, only ADD-03/4.2 (unsplit) appears in current_records.ops; the others cannot be checked here.
  - downstream proposal `DS-ADD03-I-OWNER-DIRECTIONS` issue (row:VOL-I-6.7-01): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-R-8.3-01` row_reading (row:VOL-I-8.3-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-ACT-CLAR` no_change (act:clarifications): **interpretation_pending**
  - downstream proposal `DS-ADD03-ACT-DELIVER` no_change (act:deliver): **interpretation_pending**
  - downstream proposal `DS-ADD03-ACT-SEAL` no_change (act:seal-and-mark): **interpretation_pending**
  - downstream proposal `DS-ADD03-ACT-COPIES` no_change (act:copies): **interpretation_pending**
  - downstream proposal `DS-ADD03-ACT-ENVB` no_change (act:assemble-envelope-b): **interpretation_pending**
  - downstream proposal `DS-ADD03-006` no_change (act:form-4a): **interpretation_pending**
  - downstream proposal `DS-ADD03-007` issue (act:form-4a): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-008` no_change (act:iso-copy): **interpretation_pending**
  - downstream proposal `DS-ADD03-009` issue (act:iso-copy): **interpretation_pending — HUMAN DECISION PENDING**
  - output difference: CHANGED VOL-I-6.1-01; CHANGED VOL-I-5.2-01; CHANGED VOL-I-8.3-01; CHANGED VOL-I-3.4-01; CHANGED VOL-I-6.7-01; A5 REWORK assemble-envelope-a; A5 REWORK assemble-envelope-b; A5 REWORK clarifications; A5 REWORK copies; A5 REWORK deliver; A5 REWORK iso-copy; A5 REWORK seal-and-mark

### ADD-03:2.2 (clause, p1) — UNRESOLVED (accounted for, not applied)
- source: “Every period calculated by reference to the Proposal Due Date is adjusted accordingly.”
- transition: `ADD-03/2.2-disp` disposition unresolved: ambiguous: 'Every period calculated by reference to the Proposal Due Date is adjusted accordingly.' names no clause, unlike ADD-01:2.2 which listed Volume I Cl…
  - validation: **interpretation_pending**
- transition: `ADD-03/2.2-issue` issue {"text": "ambiguous: ADD-03:2.2 reads 'Every period calculated by reference to the Proposal Due Date is adjusted accordingly.' without naming any clause. Open question: which periods does it adjust -…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-ESC-22` escalation (esc:ADD-03:2.2): **escalated**
  - downstream proposal `DS-ADD03-ESC-IMP22` escalation (impact:2. AMENDMENT TO THE PROPOSAL DUE DATE): **escalated**
  - downstream proposal `DS-ADD03-DEP-IMP22` dependency (impact:2. AMENDMENT TO THE PROPOSAL DUE DATE): **interpretation_pending**

### ADD-03:3.1 (clause, p1) — PARTLY APPLIED (an escalated sibling stays unresolved)
- source: “Form 4-G (Cybersecurity Compliance Undertaking), added by Addendum No. 2 Section 7, is withdrawn. Bidders shall disregard it and shall not submit it. Section 7.2 of Addendum No. 2 ceases to have effect.”
- transition: `ADD-03/3.1(a)` amendment_op set_status ADD-02:7.2
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): agrees — selected because removal; model claude-opus-5-5
    - concern: The op follows from the words. ADD-03:3.1 prints 'Section 7.2 of Addendum No. 2 ceases to have effect.' set_status revoked on ADD-02:7.2 is the named unit, and previous_value matches ADD-02:7.2 at ADD-02 word for word.
    - concern: Change propagation is incomplete. The rationale says the A1 row id is 'not visible', but the current records list row ADD-02-7.2-01, which is bound to ADD-02:7.2 and carries the non_responsive consequence 'Failure to submit Form 4-G shall render the Proposal non-responsive.' That row needs a readin…
    - concern: Other dependent records are not named. Row ADD-02-F4G-04 (signature line of Form 4-G) depends on the withdrawn form. Row VOL-I-9.1-01, at its ADD-02 reading, lists 'Form 4-G' in the Envelope A items. Issue I-F4G-LETTERING (lettering of the VOL-I 9.1 list after the Form 4-G insertion) may become moo…
    - concern: The reviews on row ADD-02-7.2-01 ('changed') and on I-F4G-LETTERING ('accepted') have origin interview_demo ('no observed human review'). They are not human approvals, and the follow-on readings must not treat them as settled.
- transition: `ESC-ADD-03:3.1-form` escalation why: software limitation: ADD-03:3.1 withdraws the whole of Form 4-G ('Form 4-G (Cybersecurity Compliance Undertaking), added by Addendum No. 2 Section 7, is withdrawn.'), which is the 9-member group ADD-…
  - validation: **escalated**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is a group; model claude-opus-5-5
    - concern: The core escalation looks right. Withdrawing a whole form group named only by its form number is a fair 'software limitation:' if the engine refuses set_status on the group and on its members. The provision's words support withdrawing the whole form: 'Form 4-G (Cybersecurity Compliance Undertaking)…
    - concern: The claim of a '9-member group' with 'table ADD-02:F4-G/T1 with rows /1 to /6' cannot be checked here. The units printed are ADD-02:H:F4-G, ADD-02:F4-G/T1 (only the header 'Item | Undertaking | Confirmed') and ADD-02:F4-G/para1. No rows /1 to /6 are shown.
    - concern: One statement is wrong as worded. The payload says 'no VOL-I:9.1(f) unit exists at ADD-02', but VOL-I:9.1(f) exists and reads '(f) the Technical Proposal narrative;'. The point seems to be that ADD-02:7.1's insertion has no unit of its own for the Form 4-G list entry; it should say exactly that.
    - concern: The same point is put in two classes. This escalation treats the VOL-I 9.1 Form 4-G listing as something 'which the withdrawal would also touch' (a software limitation). ISS-ADD03-3.1 treats whether that listing survives as 'ambiguous:'. Under one point, one class, the 9.1 listing belongs with the …
    - concern: Follow-on not named: row ADD-02-F4G-04 (bound to ADD-02:F4-G/para1) depends on the form group being withdrawn.
- transition: `ROW-ADD03-3.1` row_new {"row": {"id": "R-ADD03-3.1", "group": "submission", "scope": ["Envelope A"], "requirement": "Bidders shall disregard it and shall not submit it.", "units": ["ADD-03:3.1"], "discipline": "bid managem…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The quote 'Bidders shall disregard it and shall not submit it.' is verbatim from ADD-03:3.1. consequence none_stated is correct: ADD-03:3.1 prints no consequence for submitting the form.
    - concern: Read alone, the requirement text does not say what 'it' is. The note supplies 'Form 4-G'. The requirement description could name Form 4-G while the quote stays verbatim.
    - concern: Scope 'Envelope A' is not printed in ADD-03:3.1. It comes from ADD-02:7.2, which this addendum revokes. The scope tag should either cite that basis or be left out.
    - concern: Labels differ from the existing register: discipline 'bid management' (existing rows use 'Bid management'), and group 'submission' (existing groups are unit-based ids). This is minor.
    - concern: Follow-on not named: the ADD-03 reading of row VOL-I-9.1-01, whose ADD-02 item list includes 'Form 4-G'. That depends on ISS-ADD03-3.1.
- transition: `ISS-ADD03-3.1` issue {"text": "ambiguous: ADD-03:3.1 says Form 4-G 'is withdrawn' and that 'Section 7.2 of Addendum No. 2 ceases to have effect', but says nothing of ADD-02:7.1 ('A new Form 4-G is added to Volume IV and …
  - validation: **interpretation_pending — HUMAN DECISION PENDING** — readiness: not ready (promotion waits): depends on ESC-ADD-03:3.1-form (escalation, escalated)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: This is a real open point. ADD-03:3.1 expressly ends only Section 7.2 ('Section 7.2 of Addendum No. 2 ceases to have effect.'), while ADD-02:7.1 added the form to the VOL-I 9.1 list. Handing it to a person as 'ambiguous:' with two readings is appropriate.
    - concern: The issue leaves out words from ADD-03:3.1 that bear on reading (a): the form was 'added by Addendum No. 2 Section 7', meaning the whole section, not only 7.2, and it 'is withdrawn'. They should be quoted next to the two readings so the decision owner sees the full text.
    - concern: The issue does not link the accepted issue I-F4G-LETTERING (re-lettering of VOL-I 9.1 after item (e)) or row VOL-I-9.1-01. Both depend on the answer here. I-F4G-LETTERING's acceptance has origin interview_demo and is not a human decision.
    - concern: Owner is Document control. Existing Form 4-G list matters (I-F4G-LETTERING, VOL-I-9.1-01) are owned by the Bid manager. Whether Bid management should own this or be named alongside is a matter of consistency.
    - concern: The ESC-ADD-03:3.1-form escalation puts this same 9.1 listing point in the software-limitation class. The two items should be reconciled so the point has one class only.
  - downstream: units changed ADD-02:7.2; rows citing them ADD-02-7.2-01
  - downstream proposal `DS-ADD03-01` issue (row:ADD-02-7.2-01): **interpretation_pending — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
      - concern: Mostly sound: the quotations match the printed units, and the core point is real. ADD-03:3.1 says Form 4-G 'is withdrawn' and that Bidders 'shall not submit it'. Yet the only op, ADD-03/3.1, targets ADD-02:7.2 alone, so the form units (ADD-02:F4-G/T1/1, T1/3, para1) and the Envelope A list entry VO…
      - concern: The item states a status as fact. It says 'Row ADD-02-7.2-01 is therefore REVOKED and needs no new reading', but op ADD-03/3.1 is only at review 'proposed'. Statuses are set by the code and accepted by a person, so this should say 'would be revoked if the op is accepted'.
      - concern: Even after the op, row ADD-02-7.2-01 still cites VOL-I:9.1(e)+ADD-02, which the item itself says stays active. Saying the row 'needs no new reading' is therefore a conclusion that the evidence shown does not support. The point should stay open.
      - concern: It merges two classes of uncertainty. The reason given for the form staying active is a tool limit: the op engine cannot revoke a group, and check C22 rejects the member rows and the list insertion as targets. That is a software limitation and should be an escalation beginning 'software limitation:…
      - concern: The real ambiguity is not stated with its readings. ADD-03:3.1 withdraws the form 'added by Addendum No. 2 Section 7' but says only that 'Section 7.2 ... ceases to have effect'; it says nothing on Section 7.1, which inserted the form into the VOL-I 9.1 list. That should be an 'ambiguous:' point tha…
      - concern: Some claims cannot be checked from the evidence printed. Units ADD-02:F4-G/T1/2, T1/4, T1/5 and T1/6 are not in the request; the item and S-F2 say T1/5 and T1/6 are active. The current records list no activities, so form-4g-review and form-4g-sign cannot be checked. The EV-FORM-4G item record and t…
      - concern: The op is named inconsistently. The item and S-F2 call it 'ADD-03/3.1(a)', but the ops record has id 'ADD-03/3.1'.
      - concern: Losing the non_responsive consequence is not named as follow-on work. That consequence is quoted from ADD-02:7.2 in row ADD-02-7.2-01, and row ADD-02-F4G-04's note also relies on it. If 7.2 ceases, A3 changes, and the item should say so explicitly.
      - concern: The owner is given as Bid management only. The open questions also cover I-F4G-NO (owned by Technical) and how far a withdrawal reaches in the documents (arguably Legal or Document control). Naming the other owners would help the decision.
  - downstream proposal `DS-ADD03-02` escalation (row:ADD-02-7.2-01): **escalated**
  - downstream proposal `DS-ADD03-03` escalation (row:ADD-02-F4G-01): **escalated**
  - downstream proposal `DS-ADD03-04` escalation (row:ADD-02-F4G-02): **escalated**
  - downstream proposal `DS-ADD03-05` escalation (row:ADD-02-F4G-03): **escalated**
  - downstream proposal `DS-ADD03-06` escalation (row:ADD-02-F4G-04): **escalated**
  - downstream proposal `DS-ADD03-07` escalation (row:ADD-02-F4G-05): **escalated**
  - downstream proposal `D-F4G06-READING` row_reading (row:ADD-02-F4G-06): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-F4G06-ISSUE` issue (row:ADD-02-F4G-06): **interpretation_pending — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
      - concern: The main finding is supported. ADD-03:3.1 withdraws the whole of Form 4-G ('is withdrawn. Bidders shall disregard it and shall not submit it.'). The op record shows ADD-03/3.1 as one set_status op with status 'revoked' on ADD-02:7.2 only. The form heading VOL-I:9.1(e)+ADD-02 and the rows ADD-02:F4-…
      - concern: The issue cites op 'ADD-03/3.1(a)'. The ops record only has 'ADD-03/3.1'. The id needs correcting.
      - concern: The list of units still active is incomplete. Op ADD-02/7.1 also covers ADD-02:F4-G/para1, and the issue leaves it out. It lists only the heading and T1/1-6.
      - concern: Open question (1) mentions 'the VOL-I 9.1 list entry', but the dependencies leave out row VOL-I-9.1-01. That row lists 'Form 4-G' among the Envelope A items at ADD-02. The withdrawal directly affects it.
      - concern: The A5 activities 'form-4g-review' and 'form-4g-sign' cannot be checked from this request: current_records.activities is empty. I cannot confirm they exist.
      - concern: Two readings for the open interpretation are stated, (a) and (b), and they are hard to tell apart. The register records undertakings 5 and 6 as not in VOL-II 6. So reading (b), 'survive only so far as VOL-II 6 itself requires them', leads to the same result as reading (a) for those duties. The ambi…
      - concern: The point that the undertakings are 'not in VOL-II 6' rests on a note in the register, not on quoted VOL-II 6 text. No VOL-II 6 unit is in the evidence, so I cannot check it.
      - concern: The rationale says 'no op supports a removal'. A set_status op type does exist, as ADD-03/3.1 uses one. The rationale should say that no op has been proposed for the form units, which is amendment-phase work. As written, it can be read as a software limitation, which would be the wrong class.
  - downstream proposal `D-F4G07-READING` row_reading (row:ADD-02-F4G-07): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-31-ROW` row_new (ana:ROW-ADD03-3.1): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-31-ISSUE` issue (ana:ROW-ADD03-3.1): **interpretation_pending — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
      - concern: The main point is supported by the evidence shown. ADD-03:3.1 says Form 4-G 'is withdrawn. Bidders shall disregard it and shall not submit it.' The only op, ADD-03/3.1, is a set_status to 'revoked' and its only target is ADD-02:7.2. VOL-I:9.1(e)+ADD-02, ADD-02:F4-G/para1 and ADD-02:F4-G/T1/1 are pr…
      - concern: Several claims in the issue text cannot be checked against the evidence shown. Units ADD-02:F4-G/T1/2 to T1/6 are not printed. Of rows ADD-02-F4G-01 to -07, only -01, -02 and -04 are printed. The A5 activities form-4g-review and form-4g-sign do not appear: current_records.activities is empty. The c…
      - concern: The issue calls the op 'the promoted op ADD-03/3.1(a)'. The record shown has id 'ADD-03/3.1' with no '(a)', and its review status is 'proposed', not promoted. The item misstates the status of the op it relies on.
      - concern: The follow-on list is incomplete. Row VOL-I-9.1-01 (owner Bid manager) still lists 'Form 4-G' among its Envelope A items at ADD-02. Row ADD-02-7.2-01 lists unit VOL-I:9.1(e)+ADD-02, which stays active. Issue I-F4G-LETTERING (re-lettering after Form 4-G was inserted into VOL-I 9.1) depends directly …
      - concern: The A3 line (show_in_a3 true) does not state a consequence printed in the pack: S-31-F1 itself says 'no consequence is printed for submitting it'. A3 is limited to consequences the pack states. Whether this belongs in A3 should be confirmed so that a reader does not take it as a stated bid-out cons…
      - concern: The controller's human-owned check reads 'withdrawn' as the issue withdrawing a question. In fact the word quotes the provision ('is withdrawn'), so it should not be read as a resolution. The issue still has to stay open pending a human decision.
      - concern: The reviews of the related rows and issues all have origin 'interview_demo' ('no observed human review'). Nothing in this item should treat them as observed human approvals. The item does not, but those records should keep that origin.
  - downstream proposal `DS-ACT-F4G-REVIEW` escalation (act:form-4g-review): **escalated**
  - downstream proposal `DS-ACT-F4G-SIGN` escalation (act:form-4g-sign): **escalated**
  - downstream proposal `DS-ADD03-ACT-ENVA` activity (act:assemble-envelope-a): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-ISSUE-F4G` issue (act:assemble-envelope-a): **interpretation_pending — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
      - concern: The main point holds on the evidence shown. ADD-03:3.1 withdraws the whole of Form 4-G ('added by Addendum No. 2 Section 7, is withdrawn. Bidders shall disregard it and shall not submit it.'). The only op shown, ADD-03/3.1, sets just ADD-02:7.2 to 'revoked'. ADD-02:7.1 is printed with status 'activ…
      - concern: The dependencies leave out row ADD-02-7.2-01. That row carries the A3 consequence quoted from ADD-02:7.2 ('Failure to submit Form 4-G shall render the Proposal non-responsive.'), and the op revokes that clause. It is the row the withdrawal affects most and should be listed. The issue also does not …
      - concern: show_in_a3 is false, but A3 currently shows a Form 4-G non-responsive consequence (row ADD-02-7.2-01) and I-F4G-NO. The issue does not explain why the withdrawal should stay out of A3. The issue's own 'a3' text also conflicts with show_in_a3 false.
      - concern: The text refers to 'promoted ops' and 'op ADD-03/3.1(a)'. The ops record shown has the id 'ADD-03/3.1' with no '(a)', and current_records give op:ADD-03/3.1 the status 'proposed', not promoted. The statement S-F4G-OPS-PARTIAL makes the same claim.
      - concern: Several claims cannot be checked against the evidence shown. The units ADD-02:F4-G/T1/1-6 are not printed, so their 'active' status at ADD-03 is unverified. current_records.activities is empty, so the activities form-4g-review, form-4g-sign and assemble-envelope-a cannot be confirmed to exist.
      - concern: The sentence "Activity 'assemble-envelope-a' is proposed to drop its Form 4-G instruction" puts an A5 proposal inside the issue text, and nothing shown supports it. That is follow-on work for the phase that owns it. In the same text where the question is asked of Document control, it also partly de…
      - concern: The issue does not state the uncertainty class. ADD-03:3.1 withdraws the form 'added by Addendum No. 2 Section 7' but says only that 'Section 7.2 ... ceases to have effect'. That supports more than one reading: either all of Section 7, including the 7.1 insertion into the VOL-I 9.1 list, falls away…
      - concern: The issue's evidence list does not cite the target ADD-02:7.1, although the text quotes it. The evidence cites only the last sentence of ADD-03:3.1 and ADD-02:F4-G/para1. A quotation of the signature line shows the form's text, not its 'active' status.
      - concern: Rows ADD-02-F4G-01 to -07, VOL-I-9.1-01 and the related issues carry reviews whose origin is 'interview_demo' ('no observed human review'). The issue does not call these approved, which is correct, but it should keep that origin visible when it says the rows 'still stand'.
  - downstream proposal `DS-ADD03-ESC-31` escalation (esc:ADD-03:3.1): **escalated**
  - downstream proposal `DS-ADD03-ISS-31` issue (esc:ADD-03:3.1): **interpretation_pending — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
      - concern: Opening the issue is sound, and its quotations are verbatim. 'Bidders shall disregard it and shall not submit it. Section 7.2 of Addendum No. 2 ceases to have effect.' matches ADD-03:3.1. 'FORM 4-G — CYBERSECURITY COMPLIANCE UNDERTAKING' matches VOL-I:9.1(e)+ADD-02. 'Only ADD-02 7.2 is revoked' mat…
      - concern: Paraphrase: 'takes Form 4-G out of the RFP Documents' is not in the provision. ADD-03:3.1 says the form 'is withdrawn'. The issue should quote that word instead of describing the effect in its own terms.
      - concern: Can't verify from the evidence shown: the issue says 'rows ADD-02-F4G-01 to -07' remain, but only ADD-02-F4G-01 and ADD-02-F4G-04 are in current_records. Rows -02, -03 and -05 to -07 are not shown.
      - concern: Can't verify from the evidence shown: the issue names activities 'form-4g-review' and 'form-4g-sign', but current_records.activities is empty ({}). Nothing in the request shows these activities exist.
      - concern: Missing knock-on effect (bid-out consequence, A3): row ADD-02-7.2-01 rests directly on the revoked ADD-02:7.2. It quotes the consequence 'Failure to submit Form 4-G shall render the Proposal non-responsive.' (class non_responsive), and its review is an interview_demo 'changed' record. The issue nev…
      - concern: Missing knock-on effect: row VOL-I-9.1-01 (accepted through interview_demo) still lists 'Form 4-G' among its Envelope A items at ADD-02. It is not named among the records that rest on Form 4-G. The issue names the unit VOL-I:9.1(e)+ADD-02 but not this row. The confidence_reason of row VOL-II-6.3-01…
      - concern: Wrong class: point (2) is labelled 'ambiguous:', but no words shown support Reading B ('the Authority may still expect them through another document'). ADD-03:3.1 withdraws the whole form and says 'Bidders shall disregard it'. No unit shown carries undertakings 3-6 elsewhere. A genuine ambiguity ne…
      - concern: Can't verify from the evidence shown: undertakings 3-6 ('24-hour incident notice, annual penetration test, multi-factor remote access') and VOL-II 6.2 are not in the units shown. Only undertaking 3 is quoted, in row ADD-02-F4G-01, and only VOL-II:6.3 is printed.
      - concern: Point (1) could be handled differently: ADD-03:3.1 names its target directly ('Form 4-G ... is withdrawn'). Withdrawal ops on the form units and the VOL-I 9.1 entry could arguably be proposed rather than only escalated. If the tool can't represent them, the reason should start with 'software limita…
      - concern: The issue's own wording is right to say 'No decision recorded; pending a human decision' and that the interview_demo acceptances carry no handling instruction.
  - downstream proposal `DS-ADD03-IMP3-01` escalation (impact:3. WITHDRAWAL OF FORM 4-G): **escalated**
  - downstream proposal `DS-ADD03-IMP3-02` issue (impact:3. WITHDRAWAL OF FORM 4-G): **interpretation_pending — HUMAN DECISION PENDING**
  - output difference: NEW ADD-03-3.1-01; OUT ADD-02-7.2-01; CONFIRMED (unchanged) ADD-02-F4G-06; CONFIRMED (unchanged) ADD-02-F4G-07; A5 CONFIRMED (unchanged) form-4g-review; A5 CONFIRMED (unchanged) form-4g-sign

### ADD-03:3.2 (clause, p1) — no effect (PROPOSED; not approved)
- source: “The substantive requirements of Volume II Section 6 are unchanged and shall be addressed in the Technical Proposal narrative.”
- transition: `DISP-ADD03-3.2` disposition no_effect: The provision changes no volume unit: its words 'The substantive requirements of Volume II Section 6 are unchanged' leave VOL-II Section 6 (Clauses 6.1 to 6.3)…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'shall' (cites VOL-II:S6))
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is a group; model claude-opus-5-5
    - concern: The no_effect reading follows from 'The substantive requirements of Volume II Section 6 are unchanged', and the 'shall be addressed' obligation is carried by ROW-ADD03-3.2. The item correctly leaves the no_effect for a person to confirm, since the words carry 'shall'.
    - concern: The target 'VOL-II:S6' is not among the units printed; only the heading VOL-II:H:S6 is shown. The statement that Section 6 consists of 'Clauses 6.1 to 6.3' cannot be checked from the evidence here.
    - concern: Context worth stating for the person who decides: ADD-03:3.2 directly follows the withdrawal of a Cybersecurity form (3.1), and Section 6 is 'SCADA, CONTROL AND CYBER SECURITY'. The disposition could note this link without drawing a conclusion from it.
- transition: `ROW-ADD03-3.2` row_new {"row": {"id": "R-ADD03-3.2", "group": "technical_proposal", "scope": ["Technical Proposal narrative"], "requirement": "The substantive requirements of Volume II Section 6 are unchanged and shall be …
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The quote is verbatim from ADD-03:3.2. consequence none_stated is correct for 3.2 itself.
    - concern: The row has neither evidence nor a no_deliverable statement ('evidence': []). The obligation is met in the Technical Proposal narrative, which comparable rows (VOL-I-9.2-01, VOL-I-9.7-01) tie to EV-TECH-PROPOSAL. The deliverable should be stated.
    - concern: Assessment 'procedural' is not supported. The comparable narrative-content row VOL-I-9.7-01 is pass_fail, and its note says the topics are scored under Table 1-1. ADD-03:3.2 says nothing that makes this procedural, so the class should be justified or brought into line.
    - concern: Dependencies are named only in part. The narrative's page limit (VOL-I:9.2, 150 pages, consequence 'Pages in excess of the limit will be removed before evaluation and will not be scored.') is named. VOL-I-9.7-01 (minimum topics of the Technical Proposal) and VOL-I:9.1(f) (the narrative as an Envelo…
    - concern: The note's 'Clauses 6.1 to 6.3' cannot be checked from the units shown (only VOL-II:H:S6).
  - downstream proposal `DS-32-ROW` row_new (ana:ROW-ADD03-3.2): **interpretation_pending**
  - downstream proposal `DS-32-DEP` dependency (ana:ROW-ADD03-3.2): **interpretation_pending**
  - output difference: NEW ADD-03-3.2-01; A5 REWORK technical-proposal

### ADD-03:4.1 (clause, p1) — PARTLY APPLIED (an escalated sibling stays unresolved)
- source: “In Volume II Clause 2.1 and in Table 2-6 row 2-6.1, ‘120,000 m³/day’ is deleted and ‘150,000 m³/day’ is substituted. The peak hourly flow in Table 2-6 row 2-6.2 is unchanged.”
- transition: `ADD-03/4.1(a)` amendment_op replace_text VOL-II:2.1 “120,000 m³/day” → “150,000 m³/day”
  - validation: **evidence_verified**
- transition: `ESC-ADD-03:4.1-table` escalation why: software limitation: ADD-03:4.1 names 'Table 2-6 row 2-6.1' ('In Volume II Clause 2.1 and in Table 2-6 row 2-6.1, ‘120,000 m³/day’ is deleted and ‘150,000 m³/day’ is substituted.'), but the engine re…
  - validation: **escalated**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The software limitation is correctly classed. ADD-03:4.1 names 'Table 2-6 row 2-6.1' and 'row 2-6.2' explicitly, and the engine reportedly refuses them as 'not cited'. S-I3 (Value '120,000' becomes '150,000', with the Unit cell 'm³/day' unchanged) is correctly labelled as an interpretation pending …
    - concern: Change propagation is not named. Row VOL-II-T2-6-1 ('average daily flow of 120,000 m3/day', value 120000) and row VOL-II-2.1-01 (capacity_m3_day 120000) need ADD-03 readings. The engineering reading in issue I-FLOWS and in the note on row VOL-II-4.2-01 is built on 120,000 m3/day: '120,000 m3/day is…
    - concern: The op on VOL-II:2.1 (apparently ADD-03/4.1(a), referenced by ISS-ADD03-4.1) is not in this review set, so this check cannot confirm that the Clause 2.1 half of the provision is accounted for.
- transition: `ISS-ADD03-4.1` issue {"text": "ADD-03:4.1 raises the average daily flow ('‘120,000 m³/day’ is deleted and ‘150,000 m³/day’ is substituted') but states 'The peak hourly flow in Table 2-6 row 2-6.2 is unchanged.' (row 2-6.…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The core question is supported by the evidence: ADD-03:4.1 raises the average to 150,000 m³/day, states 'The peak hourly flow in Table 2-6 row 2-6.2 is unchanged.', and VOL-II:4.2 requires inconsistencies to be raised. The issue correctly avoids computing a peaking factor.
    - concern: The quotation of row 2-6.3 ('Minimum night flow' 1,800 m³/h) cannot be checked: that row is not among the units or evidence shown. It should be removed or backed by evidence.
    - concern: The issue duplicates the existing issue I-FLOWS without linking or folding into it. I-FLOWS (owner Process engineer) already covers the consistency of the Table 2-6 flows. It records ADD-02 Q11's answer 'Bidders shall design to the figures stated in Volume II. Volume II Clause 4.2 applies.' and an …
    - concern: Owner is 'Technical', while the matching rows and issue are owned by the Process engineer. Rows VOL-II-4.1-01 and VOL-II-5.2-01, which depend on the flows, are not named.
- transition: `CLAR-ADD03-4.1` clarification {"gap": "ADD-03:4.1 increases the average daily flow to 150,000 m³/day while stating 'The peak hourly flow in Table 2-6 row 2-6.2 is unchanged.'; VOL-II:4.2 obliges bidders to raise any inconsistency…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The question is labelled DRAFT and has a decision owner. The practical-impact quote of VOL-II:5.2 ('sized for the peak hourly flow in Table 2-6') can be checked.
    - concern: The question asks the Authority to 'confirm that 7,500 m³/h remains the design peak hourly flow', but ADD-03:4.1 already says so: 'The peak hourly flow in Table 2-6 row 2-6.2 is unchanged.' What VOL-II:4.2 calls for is raising the possible inconsistency between the figures, and the draft does not a…
    - concern: The draft ignores the earlier answer. ADD-02 Q11 replied to a near-identical flow question with 'Bidders shall design to the figures stated in Volume II. Volume II Clause 4.2 applies.' (recorded in I-FLOWS). A new question should acknowledge that answer and say what has changed since. It should als…
    - concern: The reference to 'rows 2-6.3 to 2-6.6 of Table 2-6' cannot be checked: those rows are not among the units shown.
    - concern: The clarification window is not named as a dependency. Row VOL-II-4.2-01 notes that clarification requests close ten Working Days before the Proposal Due Date (VOL-I 5.2), which matters for A5.
    - concern: Part of the interim handling, 'the Technical team flags the point in the bid', is a bidder action not grounded in the pack. It should be labelled as a proposal for the decision owner.
  - downstream: units changed VOL-II:2.1; rows citing them VOL-II-2.1-01
  - downstream proposal `D-ADD03-01` row_reading (row:VOL-II-2.1-01): **interpretation_pending**
  - downstream proposal `D-ADD03-02` dependency (row:VOL-II-2.1-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-ACT-TP` activity (act:technical-proposal): **interpretation_pending**
  - downstream proposal `DS-ADD03-ESC-41` escalation (esc:ADD-03:4.1): **escalated**
  - downstream proposal `DS-ADD03-ISS-41` issue (esc:ADD-03:4.1): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-DEP-72` dependency (esc:ADD-03:4.1): **interpretation_pending**
  - downstream proposal `DS-ADD03-DEP-23` dependency (esc:ADD-03:4.1): **interpretation_pending**
  - downstream proposal `DS-ADD03-IMP4-01` issue (impact:4. AMENDMENT TO NOMINAL CAPACITY): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-IMP4-02` escalation (impact:4. AMENDMENT TO NOMINAL CAPACITY): **escalated**
  - downstream proposal `DS-ADD03-IMP4-03` issue (impact:4. AMENDMENT TO NOMINAL CAPACITY): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-REREAD-Q11` escalation (reread:ADD-02:Q11): **escalated**
  - downstream proposal `DS-ADD03-ISSUE-T26` issue (reread:ADD-02:Q11): **interpretation_pending — HUMAN DECISION PENDING**
  - output difference: CHANGED VOL-II-2.1-01; A5 REWORK technical-proposal

### ADD-03:4.2 (clause, p1) — applied (PROPOSED; not approved)
- source: “Consequentially, footnote 12 to Volume I Clause 8.5 is amended by deleting ‘80,000 m³/day’ and substituting ‘100,000 m³/day’. The requirement for two (2) reference plants and the ten (10) year look-back are unchanged.”
- transition: `ADD-03/4.2(a)` amendment_op replace_text VOL-I:8.5#fn12 “80,000 m³/day” → “100,000 m³/day”
  - validation: **evidence_verified**
- transition: `ADD-03/4.2(b)` amendment_op annotate VOL-I:8.5#fn12 effect confirms
  - validation: **evidence_verified**
  - downstream: units changed VOL-I:8.5#fn12; rows citing them VOL-I-8.5-01
  - downstream proposal `DS-ADD03-R-8.5-01` row_reading (row:VOL-I-8.5-01): **interpretation_pending**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
      - concern: The item rests on ops 'ADD-03/4.2(a)' and 'ADD-03/4.2(b)', which are not in current_records.ops. The only printed op for this provision, ADD-03/4.2, targets 'VOL-I:8.5' (the clause body, which does not contain the threshold) rather than 'VOL-I:8.5#fn12'. It quotes old '80,000 m3/day' rather than th…
      - concern: Substance checks out against ADD-03:4.2: 'deleting ‘80,000 m³/day’ and substituting ‘100,000 m³/day’' in footnote 12; two plants and the ten-year look-back 'are unchanged'; the rejection words in fn12 are untouched. The target (fn12, not the body of 8.5) is correct.
      - concern: The note asserts 'ADD-03 does not change ADD-01 Q5'. Only ADD-03:2.1 and ADD-03:4.2 are printed, so this claim about the whole addendum cannot be checked from the evidence shown.
      - concern: The new parameter lookback_anchor moves the window with the PDD as amended by ADD-03/2.1. That rests on VOL-I 2.6 (not printed) and on reading 'the ten (10) year look-back are unchanged' as fixing the length of the period, not the window as it stood before. That reading is the natural one, but the …
      - concern: The rationale's claims (no other statement of 80,000 m³/day besides footnote 12; the Form 4-B capacity field; VOL-I 9.5) rest on searches and units not printed in this request and cannot be checked here.
      - concern: As for the first item, statement S-F-REVIEW-ORIGIN cites unrelated evidence (VOL-I:6.4 'SAR 5,600,000') for a statement about review origin and status.
  - downstream proposal `DS-ADD03-I-REF-THRESHOLD` issue (row:VOL-I-8.5-01): **interpretation_pending — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
      - concern: The A3 line reads: 'Reference plants: two plants each not less than 100,000 m³/day (ADD-03 4.2), else ‘shall be rejected without further evaluation’'. It leaves out the other condition footnote 12 attaches to the same rejection: 'each having achieved commercial operation within the ten (10) years p…
      - concern: The dependencies EV-FORM-4B, EV-COMPLETION-CERT and the activity 'references' are not in the evidence printed here; current_records.activities is empty. Their link to footnote 12 cannot be checked from this request.
      - concern: The quotation from VOL-I:8.5 leaves off the footnote marker printed in the unit ('Form 4-B.¹²'). The controller accepted it as verbatim, so this is minor.
      - concern: No bidder facts are asserted, the issue is left open with decision owner 'Technical', and the consequence is quoted from fn12 and not inferred. This is consistent with the rules. The issue rests on ops 4.2(a) and 2.1, which are proposed only and not accepted. The record for 4.2(a) is not printed, a…
  - downstream proposal `DS-ADD03-010` no_change (act:references): **interpretation_pending**
  - downstream proposal `DS-ADD03-011` issue (act:references): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-REREAD-Q5` escalation (reread:ADD-01:Q5): **escalated**
  - output difference: CHANGED VOL-I-8.5-01; A5 REWORK references

### ADD-03:4.3 (clause, p1) — UNRESOLVED (accounted for, not applied)
- source: “Volume I Clause 1.3 is amended correspondingly.”
- transition: `DISP-ADD03-4.3` disposition unresolved: ambiguous: ADD-03:4.3 prints only 'Volume I Clause 1.3 is amended correspondingly.' and no old/new words. VOL-I:1.3 at ADD-02 reads 'nominal capacity one hundr…
  - validation: **interpretation_pending**
- transition: `ISS-ADD03-4.3` issue {"text": "ambiguous: 'Volume I Clause 1.3 is amended correspondingly.' (ADD-03:4.3) gives no new words for 'nominal capacity one hundred and twenty thousand cubic metres per day (120,000 m³/day)' (VO…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
- transition: `CLAR-ADD03-4.3` clarification {"gap": "ADD-03:4.3 amends Volume I Clause 1.3 'correspondingly' without printing the new words.", "proposed_question": "DRAFT: Addendum No. 3 Clause 4.3 states that Volume I Clause 1.3 is amended co…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-ESC-43` escalation (esc:ADD-03:4.3): **escalated**
  - downstream proposal `DS-ADD03-CQ-43` clarification_item (esc:ADD-03:4.3): **interpretation_pending**
  - downstream proposal `DS-ADD03-IMP4-01` issue (impact:4. AMENDMENT TO NOMINAL CAPACITY): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-IMP4-02` escalation (impact:4. AMENDMENT TO NOMINAL CAPACITY): **escalated**
  - downstream proposal `DS-ADD03-IMP4-03` issue (impact:4. AMENDMENT TO NOMINAL CAPACITY): **interpretation_pending — HUMAN DECISION PENDING**

### ADD-03:5.1 (clause, p1) — applied (PROPOSED; not approved)
- source: “In Volume I Clause 6.4, ‘SAR 4,500,000 (four million five hundred thousand Saudi Riyals)’ is deleted and ‘SAR 5,600,000 (five million six hundred thousand Saudi Riyals)’ is substituted.”
- transition: `ADD-03/5.1` amendment_op replace_text VOL-I:6.4 “SAR 4,500,000 (four million five hundred thousand Saudi Riyals)” → “SAR 5,600,000 (five million six hundred thousand Saudi Riyals)”
  - validation: **evidence_verified**
  - downstream: units changed VOL-I:6.4; rows citing them VOL-I-6.4-01, VOL-I-6.4-02
  - downstream proposal `DS-ADD03-R-6.4-01` row_reading (row:VOL-I-6.4-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-I-BOND-FOLLOW-ON` issue (row:VOL-I-6.4-01): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-R-6.4-02` row_reading (row:VOL-I-6.4-02): **interpretation_pending**
  - downstream proposal `DS-ADD03-001` no_change (act:bond-approval): **interpretation_pending**
  - downstream proposal `DS-ADD03-002` escalation (act:bond-approval): **escalated**
  - downstream proposal `DS-ADD03-REREAD-Q8` escalation (reread:ADD-02:Q8): **escalated**
  - output difference: CHANGED VOL-I-6.4-01; CHANGED VOL-I-6.4-02; A5 REWORK bond-approval; A5 REWORK bond-issue

### ADD-03:5.2 (clause, p1) — applied (PROPOSED; not approved)
- source: “In Volume I Clause 6.3, ‘one hundred and eighty (180) days’ is deleted and ‘two hundred and ten (210) days’ is substituted. The Proposal validity period in Clause 7.1 is unchanged.”
- transition: `ADD-03/5.2(a)` amendment_op replace_text VOL-I:6.3 “one hundred and eighty (180) days” → “two hundred and ten (210) days”
  - validation: **evidence_verified**
- transition: `ADD-03/5.2(b)` amendment_op annotate VOL-I:7.1 effect confirms
  - validation: **evidence_verified**
  - downstream: units changed VOL-I:6.3; rows citing them VOL-I-6.3-01
  - downstream proposal `D-VOL-I-6.3-READING` row_reading (row:VOL-I-6.3-01): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-VOL-I-6.3-RULE-ESC` escalation (row:VOL-I-6.3-01): **escalated**
  - downstream proposal `DS-ADD03-R-7.1-01` row_reading (row:VOL-I-7.1-01): **interpretation_pending**
  - downstream proposal `DS-CQ-BOND` clarification_item (clar:CQ-BOND-FC-COVERAGE): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-CQ-BOND-ISSUE` issue (clar:CQ-BOND-FC-COVERAGE): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-003` no_change (act:bond-issue): **interpretation_pending**
  - output difference: CHANGED VOL-I-6.3-01; CHANGED VOL-I-7.1-01; A5 REWORK bond-approval; A5 REWORK bond-issue; A5 REWORK form-4a; A5 REWORK form-4a-prep

### ADD-03:6.1 (clause, p1,2) — applied (PROPOSED; not approved)
- source: “A new Clause 11.6 is added to Volume I: ‘11.6 Where, on completion of the combined evaluation, two or more Proposals are within two per cent (2%) of one another, the Authority may apply such further criteria as it considers appropriate to determine the Preferred Bidder, and its determination shall be final.’”
- transition: `ADD-03/6.1` amendment_op insert_unit VOL-I:11.5 “Where, on completion of the combined evaluation, two or more Proposals are within two per cent (2%) of one another, the…”
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The new_text matches the clause printed in ADD-03:6.1 word for word, minus the leading '11.6' and the quotation marks. The number '11.6' is printed in the provision, so insert_unit with number 11.6 follows from the words.
    - concern: The anchor VOL-I:11.5 is inferred: the provision only says 'A new Clause 11.6 is added to Volume I' and names no position. Statement S-6.1-prov is labelled a fact ('the last existing clause of Section 11 at ADD-02 is VOL-I:11.5'), but its evidence is only the first sentence of 11.5, which does not …
    - concern: The change-propagation list names only VOL-I:11.5. The new clause works on the 'combined evaluation', so VOL-I:11.2 (row VOL-I-11.2-01, 65%/35%) is a related unit. The rationale mentions it, but it is not in dependencies.
    - concern: Row VOL-I-11.2-01, which this clause sits beside, shows only an interview_demo acceptance ('no observed human review'). That is not a human approval and should not be relied on as one.
- transition: `ROW-ADD03-11.6` row_new {"row": {"id": "ROW-ADD03-11.6", "group": "evaluation", "scope": ["evaluation"], "requirement": "Where, on completion of the combined evaluation, two or more Proposals are within two per cent (2%) of…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The row's units are ['ADD-03:6.1'] and its target is the addendum provision, not the Volume I clause it inserts (VOL-I:11.6 once ADD-03/6.1 applies). Other rows bind to volume units (for example VOL-I-11.2-01 → VOL-I:11.2). Binding to the addendum text means later amendments to Clause 11.6 would no…
    - concern: Its group is 'evaluation', not a unit id. That does not match the convention used by the other rows (group 'VOL-I:11.2', 'VOL-I:11.5').
    - concern: The interpretation note refers to 'issue ISS-ADD03-6.1', but the row's issues field is empty, so the ambiguity is not linked in a way that can be traced.
    - concern: No owner is given, while the comparable rows name one (VOL-I-11.2-01: 'Bid manager').
    - concern: The quote and consequence 'none_stated' match the words: 'its determination shall be final' is not a stated rejection, disqualification, non-responsiveness or exclusion. The tie_band is kept as the printed words and not computed, which is correct.
- transition: `ISS-ADD03-6.1` issue {"text": "ambiguous: new Volume I Clause 11.6 (ADD-03:6.1) reads 'two or more Proposals are within two per cent (2%) of one another, the Authority may apply such further criteria as it considers appr…
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The 'ambiguous:' label covers three different points, against the one-point-one-class rule. (a) The basis of the 2% is a genuine ambiguity, and it is correctly quoted with two readings. (b) 'The further criteria are not stated anywhere in the pack' is a missing-evidence point. It should start with …
    - concern: The decision owner is only 'Bid management'. The rationale says Legal should review 'its determination shall be final', but Legal is not named as decision owner. That point should be a separate issue owned by Legal.
    - concern: Reading 1 ties 'combined evaluation' in ADD-03:6.1 to the 'combined score' in VOL-I:11.2. That link is itself an interpretation and should be stated as one, not taken as given.
    - concern: The verbatim quotations match ADD-03:6.1 and VOL-I:11.2 at ADD-02, and the issue correctly leaves the reading open for a person.
  - downstream: units changed VOL-I:11.5+ADD-03; rows citing them none
  - downstream proposal `D-ADD03-08` row_new (c46:ADD-03/6.1): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-ADD03-09` issue (c46:ADD-03/6.1): **interpretation_pending — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
      - concern: The ambiguity itself is real. The printed words 'within two per cent (2%) of one another' do not say what the 2% is measured on. But Reading A depends on a quotation from VOL-I 11.2 ('on a combined score calculated on a weighting of sixty per cent (60%) technical and forty per cent (40%) commercial…
      - concern: Page mismatch. The evidence cites doc 'VOL-I', unit 'VOL-I:11.5+ADD-03', page 2, but the issue itself puts VOL-I 11.2 on p5. The inserted wording is printed in ADD-03:6.1 (pp. 1-2). Page 2 looks like an ADD-03 page credited to VOL-I. Document control should check this.
      - concern: Three different points are filed under one 'ambiguous:' label: (1) what the 2% is measured on (a genuine ambiguity); (2) the 'further criteria' not being stated (an open discretion given to the Authority, not two competing readings of the words); (3) what 'its determination shall be final' means (a…
      - concern: The owner is Bid management. The meaning of 'its determination shall be final' is a legal question, so Legal should be named as its decision owner.
      - concern: show_in_a3 is true, and the a3 text describes a discretion. A3 holds only the bid-out consequences the pack states (rejection, disqualification, non-responsiveness, exclusion). New 11.6 states none of these. Putting it in A3 lists as a consequence something the words do not state.
      - concern: 'The clause bears on bid strategy and pricing near the margin' is the proposer's own framing. No unit in the pack says this. It should be marked as framing, not presented as an effect.
      - concern: The draft clarification CQ-ADD03-TIE-BAND is mentioned, but the request carries no clarification records, so it cannot be checked.
  - downstream proposal `D-ADD03-10` clarification_item (c46:ADD-03/6.1): **interpretation_pending**
  - downstream proposal `D-ADD03-11` dependency (c46:ADD-03/6.1): **interpretation_pending**
  - downstream proposal `DS-ADD03-IMP6-01` issue (impact:6. NEW VOLUME I CLAUSE 11.6): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-IMP6-02` dependency (impact:6. NEW VOLUME I CLAUSE 11.6): **interpretation_pending**
  - output difference: NEW ADD-03-6.1-01

### ADD-03:7.1 (clause, p2) — applied (PROPOSED; not approved)
- source: “In Volume II Table 2-4, the limit for Total Phosphorus (TP) is amended from the value shown to 0.5 mg/l, assessed on the same basis.”
- transition: `ADD-03/7.1` amendment_op set_value VOL-II:T2-4/TP “1” → “0.5”
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-opus-5-5
    - concern: The provision does not quote the old value ('amended from the value shown'). The value '1' was found in the target, and the controller has correctly marked it for a person to check.
    - concern: 'assessed on the same basis' supports leaving the Basis of assessment cell ('30-day rolling average') unchanged. The new value '0.5 mg/l' uses the same unit as the row's Unit cell ('mg/l'), so only the Limit cell needs to change.
    - concern: The follow-on list leaves out row VOL-V-29.3-01. That row lists VOL-II:T2-4/TP as a unit and its ADD-02 reading relies on the TP basis. The basis is unchanged, so the rolling-average list probably stands, but the row should be re-read at ADD-03 and not left unchanged without saying so.
    - concern: The reproduction says the Environmental Permit prevails, and the Permit is not supplied (I-PERMIT). After this change the reproduced TP limit may no longer match the Permit. The rationale says this is not decided, which is right; the I-PERMIT text only mentions the TN amendment and may need to cove…
    - concern: Row VOL-II-T2-4-TP is 'changed' with an interview_demo origin (no observed human review). The owner's confirmed transcription (3 Oct 2026, I-READING-T24) covers the image reading only, not this amendment.
  - downstream: units changed VOL-II:T2-4/TP; rows citing them VOL-II-T2-4-TP, VOL-V-29.3-01
  - downstream proposal `D-ADD03-03` row_reading (row:VOL-II-T2-4-TP): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `D-ADD03-05` row_reading (row:VOL-V-29.3-01): **interpretation_pending**
  - output difference: CHANGED VOL-II-T2-4-TP; CHANGED VOL-V-29.3-01; A5 REWORK deviations-review; A5 REWORK form-4e; A5 REWORK technical-proposal; A5 REVIEW (confirmed dependency) deviations-review; A5 REVIEW (confirmed dependency) form-4e

### ADD-03:Q15 (table_row, p2) — applied (PROPOSED; not approved)
- source: “No: 15 | Bidder question: Following the capacity increase, will the Authority extend the construction period in Volume V Clause 12.1? | Authority response: No. The period of thirty-six (36) months is unchanged.”
- transition: `ADD-03/Q15` amendment_op annotate VOL-V:12.1 effect confirms
  - validation: **evidence_verified**
  - downstream proposal `D-ADD03-04` row_reading (row:VOL-V-12.1-01): **interpretation_pending — HUMAN DECISION PENDING**
    - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
      - concern: The note says the programme 'must now reach PCOD within the same 36 months for the 150,000 m³/day capacity of VOL-II 2.1 as amended by ADD-03/4.1(a)'. This rests on op ADD-03/4.1(a), which is still only proposed (S-F1 is checked against the text 'after the proposed ops'). The note should say that t…
      - concern: Q15 is a bidder question and Authority answer printed in ADD-03. The note treats it as an op ('confirms'). Whether answers in the ADD-03 Q&A table bind is not shown in the evidence: the pack's own words on how Q&A answers bind are not printed, and ADD-01 3.2 says the pre-bid minutes do not bind. Th…
      - concern: The note names VOL-V 18.4 (the cap) and VOL-II 7.2 (the 90% reliability run). Neither unit is printed in this request. They can be checked only through the quotes in the curated records VOL-V-12.1-01 and VOL-II-7.2-01.
      - concern: The note says PCOD needs the reliability run 'at 90% of nominal capacity'. The quote in VOL-II-7.2-01 says 'not less than 90%'. The note should keep the 'not less than' wording. It also implies, without saying so, that the run is now tied to the amended 150,000 m³/day nominal capacity. Any figure t…
      - concern: The rationale says 'Text-layer units only'. ADD-03:Q15 is a table row with no crop hash. The request does not show whether that row came from the text layer or from an image, so this cannot be checked.
      - concern: Passing programme-risk and pricing to the Technical and Commercial leads is right. But no issue or escalation is opened with a named decision owner. The handover sits only in the note text.
  - output difference: CONFIRMED (unchanged) VOL-V-12.1-01; A5 CONFIRMED (unchanged) deviations-review; A5 CONFIRMED (unchanged) form-4e

### ADD-03:Q16 (table_row, p2) — no effect (PROPOSED; not approved)
- source: “No: 16 | Bidder question: Does the increase in capacity change the design influent characteristics in Table 2-2? | Authority response: No. Table 2-2 is unchanged.”
- transition: `ADD-03/Q16-disp` disposition no_effect: The provision prints no change: the Authority's response is 'No. Table 2-2 is unchanged.' It contains no amending, obliging or excepting words ('shall', 'must'…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The no_effect follows from the printed words. The response 'No. Table 2-2 is unchanged.' contains no amending, obliging or excepting words. The controller's semantic check agrees.
    - concern: The target is uncertain and depends on interpretation S-Q16-I1. Q16 names 'Table 2-2' without a volume. The claim that VOL-II:T2-2 is the only Table 2-2 rests on a search result that is not printed here, so I cannot check it. A person must confirm the target.
    - concern: The cells of VOL-II:T2-2 are not printed here (cells: null), only its title. I cannot check the rationale's list of six rows (BOD5, COD, TSS, TN, TP, Temperature).
    - concern: Propagation: ADD-03:4.1, in another batch, changes the capacity in VOL-II:2.1. The rationale says VOL-II:2.1 and VOL-II:3.1 still cite Table 2-2, which is correct. Q16 also bears on rows VOL-II-2.1-01 and VOL-II-3.1-01, which list the T2-2 rows as units. Those rows are 'accepted' only by an intervi…

### ADD-03:Q17 (table_row, p2) — applied (PROPOSED; not approved)
- source: “No: 17 | Bidder question: Will the Availability Payment be adjusted for the increased capacity? | Authority response: Bidders shall price the Project as amended by this Addendum.”
- transition: `ADD-03/Q17` amendment_op annotate ADD-03:Q17 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The provision does use obliging words: 'Bidders shall price the Project as amended by this Addendum.' Recording it on its own unit (ADD-03:Q17) is scoped correctly. It does not wrongly widen to VOL-I:10.2.
    - concern: Whether effect 'adds_obligation' is correct is itself an interpretation. The response could be read as restating how the existing pricing obligation in VOL-I:10.2 ('The Bidder shall quote a single Availability Payment...') applies to the amended Project, rather than as a new obligation. The control…
    - concern: This op depends on ADD-03/Q17-row and goes with the ambiguity in ADD-03/Q17-issue. It should not be accepted separately from them.
- transition: `ADD-03/Q17-row` row_new {"row": {"id": "R-ADD03-Q17", "group": "Financial Proposal", "scope": ["Financial Proposal"], "requirement": "Bidders shall price the Project as amended by this Addendum.", "units": ["ADD-03:Q17"], "…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The requirement is quoted verbatim from ADD-03:Q17. 'consequence: none_stated' is correct, because Q17 prints no consequence.
    - concern: The row has no 'owner' field. Every comparable row names one (e.g. VOL-I-10.2-01: 'Commercial lead'), and the Q17 issue names Commercial.
    - concern: 'evidence' is empty. VOL-I-10.2-01, the pricing row this obligation bears on, carries EV-FORM-4F. A5 needs to know which evidence item satisfies this row.
    - concern: No 'issues' are linked. The accepted issue I-NO-CONSEQUENCE (the VOL-I 11.1(i) gate) is attached to other rows that state no consequence. The new Q17 ambiguity issue (ADD-03/Q17-issue) is also not linked, even though confidence_reason says the meaning is pending a Commercial decision.
    - concern: 'group' and 'scope' are both the free text 'Financial Proposal'. Other rows use a unit id as group and scope tags such as 'envelope_B' and 'price'. 'assessment: procedural' differs from VOL-I-10.2-01's 'pass_fail', and no reason is given.
    - concern: Propagation: VOL-I:10.2 is only 'listed, not changed'. Q17 directly concerns the Availability Payment, so row VOL-I-10.2-01 should be flagged for re-review. Its 'accepted' status comes from an interview_demo assumption, not an observed human review.
    - concern: Reading A in S-Q17-I1 adds 'and the Authority makes no other adjustment'. Q17 does not print those words. They are acceptable only as one of the two labelled readings, never as the row's meaning.
- transition: `ADD-03/Q17-issue` issue {"text": "ambiguous: Clarification request 17 asks 'Will the Availability Payment be adjusted for the increased capacity?'; the Authority responds 'Bidders shall price the Project as amended by this …
  - validation: **interpretation_pending — HUMAN DECISION PENDING**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The issue is correctly classed as an ambiguity. The question ('Will the Availability Payment be adjusted for the increased capacity?') and the response ('Bidders shall price the Project as amended by this Addendum.') are quoted verbatim, and the response does not answer yes or no. Both readings are…
    - concern: Reading A's phrase 'with no separate adjustment by the Authority' goes beyond the printed words. It must stay a candidate reading and must not become the issue's conclusion.
    - concern: 'Which reading governs' is put as an open question for a person, which is correct. If Reading B is open, Bid management or Commercial may also want a DRAFT clarification question raised before the cut-off. This is optional and is not decided here.
    - concern: The capacity change in Reading A comes from ADD-03:4.1, which is in another batch and not yet validated. The 150,000 m³/day figure should be treated as depending on that batch.
  - downstream proposal `DS-Q17-ROW` row_new (c46:ADD-03/Q17): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-Q17-ISSUE` issue (c46:ADD-03/Q17): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-Q17-DEP` dependency (c46:ADD-03/Q17): **interpretation_pending**
  - downstream proposal `DS-ADD03-IMP8-01` issue (impact:8. RESPONSES TO CLARIFICATION REQUESTS 15 TO 18): **interpretation_pending — HUMAN DECISION PENDING**
  - downstream proposal `DS-ADD03-IMP8-02` dependency (impact:8. RESPONSES TO CLARIFICATION REQUESTS 15 TO 18): **interpretation_pending — HUMAN DECISION PENDING**
  - output difference: NEW ADD-03-Q17-01; A5 REWORK fin-model-build; A5 REWORK fin-model-freeze; A5 REWORK form-4f; A5 REVIEW (proposed relationship) fin-model-build; A5 REVIEW (proposed relationship) fin-model-freeze; A5 REVIEW (proposed relationship) form-4f

### ADD-03:Q18 (table_row, p2) — no effect (PROPOSED; not approved)
- source: “No: 18 | Bidder question: Please confirm the Proposal validity period following this Addendum. | Authority response: One hundred and fifty (150) days from the Proposal Due Date as amended.”
- transition: `ADD-03/Q18-disp` disposition no_effect: The provision prints no change: the response 'One hundred and fifty (150) days from the Proposal Due Date as amended.' restates the period already in VOL-I:7.1…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The no_effect on VOL-I:7.1 itself is consistent with the evidence. 'One hundred and fifty (150) days from the Proposal Due Date as amended.' matches VOL-I:7.1 at ADD-02, and ADD-03:5.2 states 'The Proposal validity period in Clause 7.1 is unchanged.' The validity end date moves through the existing…
    - concern: Interpretation S-Q18-I1 says the period is 'restated in VOL-IV:F4-A/item2', and the payload lists VOL-IV:F4-A/item2 as a candidate target. At ADD-02 that unit is 'superseded'. Row VOL-IV-F4A-04 is 'REPLACED (by ADD-01:AppA)', and issue I-F4A-FIELDS records that the reissued Form 4-A drops the numbe…
    - concern: The rationale cites 'ADD-03:2.1/2.2'. ADD-03:2.2 is not printed in this request, so I cannot check it.
    - concern: Propagation: row VOL-I-7.1-01 has review status 'changed', from an interview_demo assumption rather than an observed human review. The PDD change in ADD-03:2.1 (to 'Thursday 10 December 2026') moves the PROPOSAL-VALIDITY date rule. That recomputation must be done by calculation in the programme pha…
    - concern: The target is uncertain because Q18 names no clause. A person must confirm that 'the Proposal validity period' means the period in VOL-I:7.1.

## Downstream proposals (validated in the candidate)

| Item | Type | Task | Status | First failed check, or what a person confirms |
|---|---|---|---|---|
| DS-ADD03-01 | issue | row:ADD-02-7.2-01 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words withdraws a question ('… |
| DS-ADD03-02 | escalation | row:ADD-02-7.2-01 | escalated |  |
| DS-ADD03-03 | escalation | row:ADD-02-F4G-01 | escalated |  |
| DS-ADD03-04 | escalation | row:ADD-02-F4G-02 | escalated |  |
| DS-ADD03-05 | escalation | row:ADD-02-F4G-03 | escalated |  |
| DS-ADD03-06 | escalation | row:ADD-02-F4G-04 | escalated |  |
| DS-ADD03-07 | escalation | row:ADD-02-F4G-05 | escalated |  |
| D-F4G06-READING | row_reading | row:ADD-02-F4G-06 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words declares a matter resolved ('resolution'); its own words withdraws a question ('withdraws') |
| D-F4G06-ISSUE | issue | row:ADD-02-F4G-06 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words withdraws a question ('… |
| D-F4G07-READING | row_reading | row:ADD-02-F4G-07 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words declares a matter resolved ('resolution'); its own words withdraws a question ('withdraws') |
| D-VOL-I-3.4-READING | row_reading | row:VOL-I-3.4-01 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words declares a matter resolved ('resolution') |
| D-VOL-I-5.2-READING | row_reading | row:VOL-I-5.2-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-VOL-I-6.1-READING | row_reading | row:VOL-I-6.1-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-VOL-I-6.3-READING | row_reading | row:VOL-I-6.3-01 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words declares a matter resolved ('resolution') |
| D-VOL-I-6.3-RULE-ESC | escalation | row:VOL-I-6.3-01 | escalated |  |
| DS-ADD03-R-6.4-01 | row_reading | row:VOL-I-6.4-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-I-BOND-FOLLOW-ON | issue | row:VOL-I-6.4-01 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-ADD03-R-6.4-02 | row_reading | row:VOL-I-6.4-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R-6.7-01 | row_reading | row:VOL-I-6.7-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-I-OWNER-DIRECTIONS | issue | row:VOL-I-6.7-01 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-ADD03-R-7.1-01 | row_reading | row:VOL-I-7.1-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R-8.3-01 | row_reading | row:VOL-I-8.3-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R-8.5-01 | row_reading | row:VOL-I-8.5-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-I-REF-THRESHOLD | issue | row:VOL-I-8.5-01 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| D-ADD03-01 | row_reading | row:VOL-II-2.1-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-ADD03-02 | dependency | row:VOL-II-2.1-01 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| D-ADD03-03 | row_reading | row:VOL-II-T2-4-TP | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words decides which document prevails (precedence) ('prevails') |
| D-ADD03-04 | row_reading | row:VOL-V-12.1-01 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words interprets a term (legal or commercial interpretation) ('means') |
| D-ADD03-05 | row_reading | row:VOL-V-29.3-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-ADD03-06 | row_new | c46:ADD-03/cover/para3 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-ADD03-07 | dependency | c46:ADD-03/cover/para3 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| D-ADD03-08 | row_new | c46:ADD-03/6.1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words interprets a term (legal or commercial interpretation) ('means') |
| D-ADD03-09 | issue | c46:ADD-03/6.1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words interprets a term (lega… |
| D-ADD03-10 | clarification_item | c46:ADD-03/6.1 | interpretation_pending |  |
| D-ADD03-11 | dependency | c46:ADD-03/6.1 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| DS-Q17-ROW | row_new | c46:ADD-03/Q17 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words interprets a term (legal or commercial interpretation) ('means') |
| DS-Q17-ISSUE | issue | c46:ADD-03/Q17 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-Q17-DEP | dependency | c46:ADD-03/Q17 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| DS-31-ROW | row_new | ana:ROW-ADD03-3.1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words withdraws a question ('withdrawn') |
| DS-31-ISSUE | issue | ana:ROW-ADD03-3.1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words withdraws a question ('… |
| DS-32-ROW | row_new | ana:ROW-ADD03-3.2 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-32-DEP | dependency | ana:ROW-ADD03-3.2 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| DS-CQ-BOND | clarification_item | clar:CQ-BOND-FC-COVERAGE | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): re-reads the existing question CQ-BOND-FC-COVERAGE: a person compares the two; its own words declares a matter settled ('se… |
| DS-CQ-BOND-ISSUE | issue | clar:CQ-BOND-FC-COVERAGE | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-ACT-F4G-REVIEW | escalation | act:form-4g-review | escalated |  |
| DS-ACT-F4G-SIGN | escalation | act:form-4g-sign | escalated |  |
| DS-ADD03-ACT-CLAR | no_change | act:clarifications | interpretation_pending |  |
| DS-ADD03-ACT-DELIVER | no_change | act:deliver | interpretation_pending |  |
| DS-ADD03-ACT-SEAL | no_change | act:seal-and-mark | interpretation_pending |  |
| DS-ADD03-ACT-COPIES | no_change | act:copies | interpretation_pending |  |
| DS-ADD03-ACT-ENVA | activity | act:assemble-envelope-a | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words withdraws a question ('withdrawn') |
| DS-ADD03-ISSUE-F4G | issue | act:assemble-envelope-a | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words withdraws a question ('… |
| DS-ADD03-ACT-ENVB | no_change | act:assemble-envelope-b | interpretation_pending |  |
| DS-ADD03-001 | no_change | act:bond-approval | interpretation_pending |  |
| DS-ADD03-002 | escalation | act:bond-approval | escalated |  |
| DS-ADD03-003 | no_change | act:bond-issue | interpretation_pending |  |
| DS-ADD03-004 | no_change | act:form-4a-prep | interpretation_pending |  |
| DS-ADD03-005 | dependency | act:form-4a-prep | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| DS-ADD03-006 | no_change | act:form-4a | interpretation_pending |  |
| DS-ADD03-007 | issue | act:form-4a | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-ADD03-008 | no_change | act:iso-copy | interpretation_pending |  |
| DS-ADD03-009 | issue | act:iso-copy | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-ADD03-010 | no_change | act:references | interpretation_pending |  |
| DS-ADD03-011 | issue | act:references | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-ADD03-ACT-TP | activity | act:technical-proposal | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| DS-ADD03-ESC-22 | escalation | esc:ADD-03:2.2 | escalated |  |
| DS-ADD03-ESC-31 | escalation | esc:ADD-03:3.1 | escalated |  |
| DS-ADD03-ISS-31 | issue | esc:ADD-03:3.1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-ADD03-ESC-41 | escalation | esc:ADD-03:4.1 | escalated |  |
| DS-ADD03-ISS-41 | issue | esc:ADD-03:4.1 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-ADD03-DEP-72 | dependency | esc:ADD-03:4.1 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| DS-ADD03-DEP-23 | dependency | esc:ADD-03:4.1 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| DS-ADD03-ESC-43 | escalation | esc:ADD-03:4.3 | escalated |  |
| DS-ADD03-CQ-43 | clarification_item | esc:ADD-03:4.3 | interpretation_pending |  |
| DS-ADD03-ESC-IMP22 | escalation | impact:2. AMENDMENT TO THE PROPOSAL DUE DATE | escalated |  |
| DS-ADD03-DEP-IMP22 | dependency | impact:2. AMENDMENT TO THE PROPOSAL DUE DATE | interpretation_pending | an inferred relationship stays `possible`: a person confirms or rejects it |
| DS-ADD03-IMP4-01 | issue | impact:4. AMENDMENT TO NOMINAL CAPACITY | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |
| DS-ADD03-IMP4-02 | escalation | impact:4. AMENDMENT TO NOMINAL CAPACITY | escalated |  |
| DS-ADD03-IMP4-03 | issue | impact:4. AMENDMENT TO NOMINAL CAPACITY | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words declares a matter resol… |
| DS-ADD03-IMP3-01 | escalation | impact:3. WITHDRAWAL OF FORM 4-G | escalated | missing_information: the proposer declares missing: No recorded instruction on how the rows, evidence item and activities of the withdrawn Form 4-G are to be handled; interview_demo acceptance does n… |
| DS-ADD03-IMP3-02 | issue | impact:3. WITHDRAWAL OF FORM 4-G | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words withdraws a question ('… |
| DS-ADD03-IMP6-01 | issue | impact:6. NEW VOLUME I CLAUSE 11.6 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words interprets a term (lega… |
| DS-ADD03-IMP6-02 | dependency | impact:6. NEW VOLUME I CLAUSE 11.6 | interpretation_pending | an inferred relationship stays `possible`: a person confirms or rejects it |
| DS-ADD03-IMP8-01 | issue | impact:8. RESPONSES TO CLARIFICATION REQUESTS 15 TO 18 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's; its own words decides which clause go… |
| DS-ADD03-IMP8-02 | dependency | impact:8. RESPONSES TO CLARIFICATION REQUESTS 15 TO 18 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): its own words decides which clause governs ('governs') |
| DS-ADD03-REREAD-Q1 | escalation | reread:ADD-01:Q1 | invalid | provision: ADD-01:Q1 is not a provision of ADD-03 |
| DS-ADD03-REREAD-Q3 | escalation | reread:ADD-01:Q3 | invalid | provision: ADD-01:Q3 is not a provision of ADD-03 |
| DS-ADD03-REREAD-Q5 | escalation | reread:ADD-01:Q5 | escalated | statements: fact downstream-010/S-OPS-PROPOSED is not supported verbatim |
| DS-ADD03-REREAD-Q8 | escalation | reread:ADD-02:Q8 | escalated | statements: fact downstream-010/S-EV-BID-BOND-NAME is not supported verbatim |
| DS-ADD03-REREAD-Q11 | escalation | reread:ADD-02:Q11 | escalated | statements: fact downstream-010/S-OPS-PROPOSED is not supported verbatim |
| DS-ADD03-ISSUE-T26 | issue | reread:ADD-02:Q11 | interpretation_pending — HUMAN DECISION PENDING | evidence verified; conclusion is a human decision (HUMAN DECISION PENDING): an issue is a matter kept open for people: its framing and conclusion are a person's |

## Promoted into the candidate (PROPOSED; nothing accepted)

- ops: ADD-03/cover/para3, ADD-03/2.1, ADD-03/3.1(a), ADD-03/4.1(a), ADD-03/4.2(a), ADD-03/4.2(b), ADD-03/5.1, ADD-03/5.2(a), ADD-03/5.2(b), ADD-03/6.1, ADD-03/7.1, ADD-03/Q15, ADD-03/Q17
- dispositions: ADD-03:cover/para1: no_effect, ADD-03:cover/para2: no_effect, ADD-03:1.1: no_effect, ADD-03:3.2: no_effect, ADD-03:Q16: no_effect, ADD-03:Q18: no_effect
- accounted unresolved: ADD-03:2.2, ADD-03:4.3
- rows new: ADD-03-cover-para3-01, ADD-03-6.1-01, ADD-03-Q17-01, ADD-03-3.1-01, ADD-03-3.2-01
- readings: ADD-02-F4G-06, ADD-02-F4G-07, VOL-I-3.4-01, VOL-I-5.2-01, VOL-I-6.1-01, VOL-I-6.3-01, VOL-I-6.4-01, VOL-I-6.4-02, VOL-I-6.7-01, VOL-I-7.1-01, VOL-I-8.3-01, VOL-I-8.5-01, VOL-II-2.1-01, VOL-II-T2-4-TP, VOL-V-12.1-01, VOL-V-29.3-01
- issues: I-ADD-03-2-2-2-2-ISSUE-ANA, I-ADD03-11-6-BAND-COND, I-ADD03-BOND-210, I-ADD03-BOND-AMOUNT-FOLLOW-ON, I-ADD03-CAPACITY-VOLI-1-3-COND, I-ADD03-F4A-PDD, I-ADD03-F4G-EFFECTIVE-TEXT, I-ADD03-F4G-LIST-ENTRY-COND, I-ADD03-F4G-SCOPE, I-ADD03-F4G-TAKEN-OUT, I-ADD03-F4G-UNITS, I-ADD03-F4G-UNITS-ACTIVE, I-ADD03-FLOWS-BASIS, I-ADD03-FLOWS-REREAD-COND, I-ADD03-ISO-DATE, I-ADD03-PDD-OWNER-DIRECTIONS, I-ADD03-Q17-AP-CAPACITY, I-ADD03-Q17-PRICING-COND, I-ADD03-REF-THRESHOLD, I-ADD03-REFERENCE-THRESHOLD, I-ADD03-T26-AVG-FLOW, I-ADD03-TIE-BAND
- analysis issues: I-ADD-03-2-2-2-2-ISSUE-ANA
- activities: assemble-envelope-a, technical-proposal
- clarifications: CQ-ADD03-TIE-BAND, CQ-BOND-FC-COVERAGE, CQ-ADD03-VOL-I-1-3
- relationships: REL-AI-001, REL-AI-002, REL-AI-003, REL-AI-004, REL-AI-005, REL-AI-006, REL-AI-007, REL-AI-008, REL-AI-009, REL-AI-010, REL-AI-011
- no change: act:clarifications, act:deliver, act:seal-and-mark, act:copies, act:assemble-envelope-b, act:bond-approval, act:bond-issue, act:form-4a-prep, act:form-4a, act:iso-copy, act:references
- the same question promoted once (analysis issue -> the issue it was merged into): I-ADD-03-3-1-ISSUE-ANA -> I-ADD03-F4G-SCOPE; I-ADD-03-4-1-ISSUE-ANA -> I-ADD03-FLOWS-BASIS; I-ADD-03-4-3-ISSUE-ANA -> I-ADD03-CAPACITY-VOLI-1-3-COND; I-ADD-03-6-1-ISSUE-ANA -> I-ADD03-11-6-BAND-COND; I-ADD-03-Q17-Q17-ISSUE-ANA -> I-ADD03-Q17-AP-CAPACITY
- unresolved provisions: 4
- note: ADD-03:3.1: partly answered by ADD-03/3.1(a); escalated: software limitation: ADD-03:3.1 withdraws the whole of Form 4-G ('Form 4-G (Cybersecurity Compliance Undertaking), added by Addendum No. 2 Section 7, is withdrawn.'), which is the 9-member group ADD-… (the promoted item stands; the escalation is for a person)
- note: ADD-03:4.1: partly answered by ADD-03/4.1(a); escalated: software limitation: ADD-03:4.1 names 'Table 2-6 row 2-6.1' ('In Volume II Clause 2.1 and in Table 2-6 row 2-6.1, ‘120,000 m³/day’ is deleted and ‘150,000 m³/day’ is substituted.'), but the engine re… (the promoted item stands; the escalation is for a person)
- note: rows.yaml: 2 comment line(s) inside row VOL-I-6.1-01 were not kept (the row was rewritten; the file's other comments are kept)
- note: rows.yaml: 5 comment line(s) inside row VOL-I-8.5-01 were not kept (the row was rewritten; the file's other comments are kept)
- note: VOL-II.yaml: 1 comment line(s) inside row VOL-II-T2-4-TP were not kept (the row was rewritten; the file's other comments are kept)
- note: VOL-V.yaml: 1 comment line(s) inside row VOL-V-12.1-01 were not kept (the row was rewritten; the file's other comments are kept)
- note: VOL-V.yaml: 1 comment line(s) inside row VOL-V-29.3-01 were not kept (the row was rewritten; the file's other comments are kept)

- left out of the promoted ops: ISS-ADD03-3.1: not ready: promotion waits while depends on ESC-ADD-03:3.1-form (escalation, escalated); ADD-03/2.2-issue: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-2-2-2-2-ISSUE-ANA; HUMAN DECISION PE…; ADD-03/row-ack: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/cover/para3` as an UN…; ROW-ADD03-3.1: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ROW-ADD03-3.1` as an UNVERIF…; ROW-ADD03-3.2: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ROW-ADD03-3.2` as an UNVERIF…; ISS-ADD03-4.1: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-4-1-ISSUE-ANA; HUMAN DECISION PENDIN…; CLAR-ADD03-4.1: an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; th…; ISS-ADD03-4.3: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-4-3-ISSUE-ANA; HUMAN DECISION PENDIN…; CLAR-ADD03-4.3: an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; th…; ROW-ADD03-11.6: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/6.1` as an UNVERIFIED…; ISS-ADD03-6.1: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-6-1-ISSUE-ANA; HUMAN DECISION PENDIN…; ADD-03/Q17-row: an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/Q17` as an UNVERIFIED…; ADD-03/Q17-issue: an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-Q17-Q17-ISSUE-ANA; HUMAN DECISION PE…

## check-register on the candidate

- exit 1; 4 finding(s) {'pending_settled': 4}
- missing because the downstream phase did not propose them (the run's own new rows): 0
- defects: 4
  - [pending_settled] I-ADD03-F4G-SCOPE: labelled HUMAN DECISION PENDING, yet its own words settle a limb of it ('therefore'): reword it as open (the proposed reading, 'not decided', and who decides) or record a person's decision
  - [pending_settled] I-ADD03-TIE-BAND: labelled HUMAN DECISION PENDING, yet its own words settle a limb of it ('means'): reword it as open (the proposed reading, 'not decided', and who decides) or record a person's decision
  - [pending_settled] I-ADD03-11-6-BAND-COND: labelled HUMAN DECISION PENDING, yet its own words settle a limb of it ('means'): reword it as open (the proposed reading, 'not decided', and who decides) or record a person's decision
  - [pending_settled] I-ADD03-Q17-PRICING-COND: labelled HUMAN DECISION PENDING, yet its own words settle a limb of it ('therefore'): reword it as open (the proposed reading, 'not decided', and who decides) or record a person's decision

## Analysis rows carried to downstream tasks (and other analysis items not promoted)

- `ADD-03/2.2-issue` issue (ADD-03:2.2, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-2-2-2-2-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ADD-03/row-ack` row_new (ADD-03:cover/para3, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/cover/para3` as an UNVERIFIED reference — applied as the new row(s) ADD-03-cover-para3-01 (proposed downstream: ADD-03-cover-para3-01 (row_new, interpretation_pending), D-ADD03-07 (dependency, interpretation_pending); task(s) c46:ADD-03/cover/para3; PROPOSED, not approved): the provision's obligation is that row; a person confirms it
- `ROW-ADD03-3.1` row_new (ADD-03:3.1, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ROW-ADD03-3.1` as an UNVERIFIED reference — applied as the new row(s) ADD-03-3.1-01 (proposed downstream: ADD-03-3.1-01 (row_new, interpretation_pending), DS-31-ISSUE (issue, interpretation_pending); task(s) ana:ROW-ADD03-3.1; PROPOSED, not approved): the provision's obligation is that row; a person confirms it
- `ISS-ADD03-3.1` issue (ADD-03:3.1, interpretation_pending): not ready: promotion waits while depends on ESC-ADD-03:3.1-form (escalation, escalated)
- `ROW-ADD03-3.2` row_new (ADD-03:3.2, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `ana:ROW-ADD03-3.2` as an UNVERIFIED reference — applied as the new row(s) ADD-03-3.2-01 (proposed downstream: ADD-03-3.2-01 (row_new, interpretation_pending), DS-32-DEP (dependency, interpretation_pending); task(s) ana:ROW-ADD03-3.2; PROPOSED, not approved): the provision's obligation is that row; a person confirms it
- `ISS-ADD03-4.1` issue (ADD-03:4.1, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-4-1-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `CLAR-ADD03-4.1` clarification (ADD-03:4.1, interpretation_pending): an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; the downstream phase proposes issues and clarification entries against the candidate
- `ISS-ADD03-4.3` issue (ADD-03:4.3, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-4-3-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `CLAR-ADD03-4.3` clarification (ADD-03:4.3, interpretation_pending): an analysis clarification is not promoted (the analysis set promotes ops and dispositions only): listed for a person in the review packet with its evidence; the downstream phase proposes issues and clarification entries against the candidate
- `ROW-ADD03-11.6` row_new (ADD-03:6.1, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/6.1` as an UNVERIFIED reference — applied as the new row(s) ADD-03-6.1-01 (proposed downstream: ADD-03-6.1-01 (row_new, interpretation_pending), D-ADD03-09 (issue, interpretation_pending), D-ADD03-10 (clarification_item, interpretation_pending), D-ADD03-11 (dependency, interpretation_pending); task(s) c46:ADD-03/6.1; PROPOSED, not …
- `ISS-ADD03-6.1` issue (ADD-03:6.1, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-6-1-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task
- `ADD-03/Q17-row` row_new (ADD-03:Q17, interpretation_pending): an analysis row_new is not promoted from the analysis set (it promotes ops and dispositions only): carried to downstream task `c46:ADD-03/Q17` as an UNVERIFIED reference — applied as the new row(s) ADD-03-Q17-01 (proposed downstream: ADD-03-Q17-01 (row_new, interpretation_pending), DS-Q17-ISSUE (issue, interpretation_pending), DS-Q17-DEP (dependency, interpretation_pending); task(s) c46:ADD-03/Q17; PROPOSED, not approved): the provision's obligation is that row; a pe…
- `ADD-03/Q17-issue` issue (ADD-03:Q17, interpretation_pending): an analysis issue is not an op or a disposition: it is written into the candidate's register as a PROPOSED issue (I-ADD-03-Q17-Q17-ISSUE-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task

## Coverage

- provisions: 19; accounted for by the combined set: 19; states {'validated': 19}
- the analysis ITEMS' resolution by the controller (items, not provisions; session 14): resolved 8, pending 11, invalid 0, unaccounted 0; approved 0
- structural units of ADD-03 that are not provisions (listed so nothing is dropped): ADD-03:H:cover (heading), ADD-03:H:cover-2 (heading), ADD-03:H:S1 (heading), ADD-03:H:S2 (heading), ADD-03:H:S3 (heading), ADD-03:H:S4 (heading), ADD-03:H:S5 (heading), ADD-03:H:S6 (heading), ADD-03:H:S7 (heading), ADD-03:H:S8 (heading), ADD-03:S8/QA (table)
- batches: analysis-001 done, analysis-002 done, analysis-003 done, analysis-004 done, downstream-001 done, downstream-002 done, downstream-003 done, downstream-004 done, downstream-005 done, downstream-006 done, downstream-007 done, downstream-008 done, downstream-009 done, downstream-010 done

## Critic (a second model over the selected items; it changed no status)

**Agreement between the critic and the proposer is not approval**: every item still needs a person's decision, and a disagreement is a concern for that person, not a rejection. The critic reviews only the selected classes (consequential interpretations, uncertain targets, removals, conflicting evidence), in one request per batch.

| Batch | Critic | Selected | Reviewed | Agrees | Does not agree | Note |
|---|---|---|---|---|---|---|
| analysis-001 | done | 2 | 2 | 1 | 1 |  |
| analysis-002 | done | 9 | 9 | 5 | 4 |  |
| analysis-003 | done | 4 | 4 | 2 | 2 |  |
| analysis-004 | done | 5 | 5 | 4 | 1 |  |
| downstream-001 | done | 1 | 1 | 0 | 1 |  |
| downstream-002 | done | 4 | 4 | 3 | 1 |  |
| downstream-003 | done | 3 | 3 | 3 | 0 |  |
| downstream-004 | done | 2 | 2 | 1 | 1 |  |
| downstream-005 | done | 1 | 1 | 0 | 1 |  |
| downstream-006 | done | 1 | 1 | 0 | 1 |  |
| downstream-007 | not_needed | 0 | - | - | - |  |
| downstream-008 | done | 1 | 1 | 0 | 1 |  |
| downstream-009 | not_needed | 0 | - | - | - |  |
| downstream-010 | not_needed | 0 | - | - | - |  |

- **ADD-03/cover/para3** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The core reading holds. 'Bidders shall acknowledge receipt in Form 4-A.' is printed in ADD-03:cover/para3, so annotating the cover with an obligation on its own unit fits the words. The uncertain_target flag comes from this being a self-annotation, not from a wrong unit.
    - concern: The rationale relies on the 'accepted' ADD-02/cover/para3 annotation as a precedent. That acceptance has origin interview_demo ('no observed human review'). It is not a human decision and should not be presented as a precedent supporting this item.
    - concern: The note says the precedence sentence only restates VOL-I:3.2(a). That is consistent with '(a) the Addenda, a later Addendum prevailing over an earlier one;'. However, the cover's summary list (PDD, Bid Bond, Form 4-G withdrawal, capacity/threshold, Table 2-4, Clause 11.6, Q15-18) is only deferred …
    - concern: 'All other terms of the RFP Documents remain unchanged.' is not explicitly accounted for in the note. It should be recorded as a cover statement with no amending effect, so that no provision of the paragraph goes unaccounted.
    - concern: The op lists no dependencies beyond itself. Form 4-A has been reissued (ADD-01 App A; VOL-IV:F4-A/item1 is 'superseded'). The open issue I-F4A-FIELDS and the Form 4-A execution rule in VOL-I:9.3 are directly affected by a new acknowledgement obligation and should be named.
- **ADD-03/row-ack** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: Wrong effective text. The row cites VOL-IV:F4-A/item1 and says receipt 'is acknowledged in Form 4-A paragraph 1 ("including Addenda numbered ______ to ______ ...")'. That unit has status 'superseded'. Row VOL-IV-F4A-03 is evaluated as 'REPLACED (by ADD-01:AppA)', and its note says 'The reissued For…
    - concern: The open issue I-F4A-FIELDS is not linked. It covers the reissued form's 'acknowledgement of Addenda at paragraph 1' purpose with no paragraph 1, its dropped fields and its stale printed PDD. ADD-03 also amends the Proposal Due Date, which makes the stale-PDD point worse. None of this is mentioned.
    - concern: Consequence: not inferring non-responsiveness from VOL-I:9.3 is correct. But whether a missing or wrong addenda acknowledgement counts as an 'improperly executed Form 4-A' ('An unsigned or improperly executed Form 4-A shall render the Proposal non-responsive.') is a genuine ambiguity. It should go …
    - concern: The row's metadata does not match the existing Form 4-A rows (VOL-I-9.3-01, VOL-IV-F4A-03): scope ['Bidder'] and group 'submission' versus envelope_A/forms/addenda_acknowledgement; evidence [] versus EV-FORM-4A; assessment 'procedural' versus pass_fail; and no owner. Possible overlap with ADD-01-Ap…
    - concern: The row should cite the reissued Form 4-A unit (ADD-01 App A field) that carries the acknowledgement at ADD-02, not the superseded VOL-IV paragraph. As proposed, the target and units are not certain and should be escalated as an uncertain target.
    - concern: The interview_demo 'accepted' reviews of VOL-IV-F4A-03, I-F4A-FIELDS and I-NO-CONSEQUENCE are not human decisions. Nothing here should rely on them as settled.
- **ADD-03/3.1(a)** (analysis-002; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because removal; model claude-opus-5-5
    - concern: The op follows from the words. ADD-03:3.1 prints 'Section 7.2 of Addendum No. 2 ceases to have effect.' set_status revoked on ADD-02:7.2 is the named unit, and previous_value matches ADD-02:7.2 at ADD-02 word for word.
    - concern: Change propagation is incomplete. The rationale says the A1 row id is 'not visible', but the current records list row ADD-02-7.2-01, which is bound to ADD-02:7.2 and carries the non_responsive consequence 'Failure to submit Form 4-G shall render the Proposal non-responsive.' That row needs a readin…
    - concern: Other dependent records are not named. Row ADD-02-F4G-04 (signature line of Form 4-G) depends on the withdrawn form. Row VOL-I-9.1-01, at its ADD-02 reading, lists 'Form 4-G' in the Envelope A items. Issue I-F4G-LETTERING (lettering of the VOL-I 9.1 list after the Form 4-G insertion) may become moo…
    - concern: The reviews on row ADD-02-7.2-01 ('changed') and on I-F4G-LETTERING ('accepted') have origin interview_demo ('no observed human review'). They are not human approvals, and the follow-on readings must not treat them as settled.
- **ESC-ADD-03:3.1-form** (analysis-002; controller status **escalated**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is a group; model claude-opus-5-5
    - concern: The core escalation looks right. Withdrawing a whole form group named only by its form number is a fair 'software limitation:' if the engine refuses set_status on the group and on its members. The provision's words support withdrawing the whole form: 'Form 4-G (Cybersecurity Compliance Undertaking)…
    - concern: The claim of a '9-member group' with 'table ADD-02:F4-G/T1 with rows /1 to /6' cannot be checked here. The units printed are ADD-02:H:F4-G, ADD-02:F4-G/T1 (only the header 'Item | Undertaking | Confirmed') and ADD-02:F4-G/para1. No rows /1 to /6 are shown.
    - concern: One statement is wrong as worded. The payload says 'no VOL-I:9.1(f) unit exists at ADD-02', but VOL-I:9.1(f) exists and reads '(f) the Technical Proposal narrative;'. The point seems to be that ADD-02:7.1's insertion has no unit of its own for the Form 4-G list entry; it should say exactly that.
    - concern: The same point is put in two classes. This escalation treats the VOL-I 9.1 Form 4-G listing as something 'which the withdrawal would also touch' (a software limitation). ISS-ADD03-3.1 treats whether that listing survives as 'ambiguous:'. Under one point, one class, the 9.1 listing belongs with the …
    - concern: Follow-on not named: row ADD-02-F4G-04 (bound to ADD-02:F4-G/para1) depends on the form group being withdrawn.
- **ROW-ADD03-3.1** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The quote 'Bidders shall disregard it and shall not submit it.' is verbatim from ADD-03:3.1. consequence none_stated is correct: ADD-03:3.1 prints no consequence for submitting the form.
    - concern: Read alone, the requirement text does not say what 'it' is. The note supplies 'Form 4-G'. The requirement description could name Form 4-G while the quote stays verbatim.
    - concern: Scope 'Envelope A' is not printed in ADD-03:3.1. It comes from ADD-02:7.2, which this addendum revokes. The scope tag should either cite that basis or be left out.
    - concern: Labels differ from the existing register: discipline 'bid management' (existing rows use 'Bid management'), and group 'submission' (existing groups are unit-based ids). This is minor.
    - concern: Follow-on not named: the ADD-03 reading of row VOL-I-9.1-01, whose ADD-02 item list includes 'Form 4-G'. That depends on ISS-ADD03-3.1.
- **ISS-ADD03-3.1** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: This is a real open point. ADD-03:3.1 expressly ends only Section 7.2 ('Section 7.2 of Addendum No. 2 ceases to have effect.'), while ADD-02:7.1 added the form to the VOL-I 9.1 list. Handing it to a person as 'ambiguous:' with two readings is appropriate.
    - concern: The issue leaves out words from ADD-03:3.1 that bear on reading (a): the form was 'added by Addendum No. 2 Section 7', meaning the whole section, not only 7.2, and it 'is withdrawn'. They should be quoted next to the two readings so the decision owner sees the full text.
    - concern: The issue does not link the accepted issue I-F4G-LETTERING (re-lettering of VOL-I 9.1 after item (e)) or row VOL-I-9.1-01. Both depend on the answer here. I-F4G-LETTERING's acceptance has origin interview_demo and is not a human decision.
    - concern: Owner is Document control. Existing Form 4-G list matters (I-F4G-LETTERING, VOL-I-9.1-01) are owned by the Bid manager. Whether Bid management should own this or be named alongside is a matter of consistency.
    - concern: The ESC-ADD-03:3.1-form escalation puts this same 9.1 listing point in the software-limitation class. The two items should be reconciled so the point has one class only.
- **DISP-ADD03-3.2** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is a group; model claude-opus-5-5
    - concern: The no_effect reading follows from 'The substantive requirements of Volume II Section 6 are unchanged', and the 'shall be addressed' obligation is carried by ROW-ADD03-3.2. The item correctly leaves the no_effect for a person to confirm, since the words carry 'shall'.
    - concern: The target 'VOL-II:S6' is not among the units printed; only the heading VOL-II:H:S6 is shown. The statement that Section 6 consists of 'Clauses 6.1 to 6.3' cannot be checked from the evidence here.
    - concern: Context worth stating for the person who decides: ADD-03:3.2 directly follows the withdrawal of a Cybersecurity form (3.1), and Section 6 is 'SCADA, CONTROL AND CYBER SECURITY'. The disposition could note this link without drawing a conclusion from it.
- **ROW-ADD03-3.2** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The quote is verbatim from ADD-03:3.2. consequence none_stated is correct for 3.2 itself.
    - concern: The row has neither evidence nor a no_deliverable statement ('evidence': []). The obligation is met in the Technical Proposal narrative, which comparable rows (VOL-I-9.2-01, VOL-I-9.7-01) tie to EV-TECH-PROPOSAL. The deliverable should be stated.
    - concern: Assessment 'procedural' is not supported. The comparable narrative-content row VOL-I-9.7-01 is pass_fail, and its note says the topics are scored under Table 1-1. ADD-03:3.2 says nothing that makes this procedural, so the class should be justified or brought into line.
    - concern: Dependencies are named only in part. The narrative's page limit (VOL-I:9.2, 150 pages, consequence 'Pages in excess of the limit will be removed before evaluation and will not be scored.') is named. VOL-I-9.7-01 (minimum topics of the Technical Proposal) and VOL-I:9.1(f) (the narrative as an Envelo…
    - concern: The note's 'Clauses 6.1 to 6.3' cannot be checked from the units shown (only VOL-II:H:S6).
- **ESC-ADD-03:4.1-table** (analysis-002; controller status **escalated**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The software limitation is correctly classed. ADD-03:4.1 names 'Table 2-6 row 2-6.1' and 'row 2-6.2' explicitly, and the engine reportedly refuses them as 'not cited'. S-I3 (Value '120,000' becomes '150,000', with the Unit cell 'm³/day' unchanged) is correctly labelled as an interpretation pending …
    - concern: Change propagation is not named. Row VOL-II-T2-6-1 ('average daily flow of 120,000 m3/day', value 120000) and row VOL-II-2.1-01 (capacity_m3_day 120000) need ADD-03 readings. The engineering reading in issue I-FLOWS and in the note on row VOL-II-4.2-01 is built on 120,000 m3/day: '120,000 m3/day is…
    - concern: The op on VOL-II:2.1 (apparently ADD-03/4.1(a), referenced by ISS-ADD03-4.1) is not in this review set, so this check cannot confirm that the Clause 2.1 half of the provision is accounted for.
- **ISS-ADD03-4.1** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The core question is supported by the evidence: ADD-03:4.1 raises the average to 150,000 m³/day, states 'The peak hourly flow in Table 2-6 row 2-6.2 is unchanged.', and VOL-II:4.2 requires inconsistencies to be raised. The issue correctly avoids computing a peaking factor.
    - concern: The quotation of row 2-6.3 ('Minimum night flow' 1,800 m³/h) cannot be checked: that row is not among the units or evidence shown. It should be removed or backed by evidence.
    - concern: The issue duplicates the existing issue I-FLOWS without linking or folding into it. I-FLOWS (owner Process engineer) already covers the consistency of the Table 2-6 flows. It records ADD-02 Q11's answer 'Bidders shall design to the figures stated in Volume II. Volume II Clause 4.2 applies.' and an …
    - concern: Owner is 'Technical', while the matching rows and issue are owned by the Process engineer. Rows VOL-II-4.1-01 and VOL-II-5.2-01, which depend on the flows, are not named.
- **CLAR-ADD03-4.1** (analysis-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The question is labelled DRAFT and has a decision owner. The practical-impact quote of VOL-II:5.2 ('sized for the peak hourly flow in Table 2-6') can be checked.
    - concern: The question asks the Authority to 'confirm that 7,500 m³/h remains the design peak hourly flow', but ADD-03:4.1 already says so: 'The peak hourly flow in Table 2-6 row 2-6.2 is unchanged.' What VOL-II:4.2 calls for is raising the possible inconsistency between the figures, and the draft does not a…
    - concern: The draft ignores the earlier answer. ADD-02 Q11 replied to a near-identical flow question with 'Bidders shall design to the figures stated in Volume II. Volume II Clause 4.2 applies.' (recorded in I-FLOWS). A new question should acknowledge that answer and say what has changed since. It should als…
    - concern: The reference to 'rows 2-6.3 to 2-6.6 of Table 2-6' cannot be checked: those rows are not among the units shown.
    - concern: The clarification window is not named as a dependency. Row VOL-II-4.2-01 notes that clarification requests close ten Working Days before the Proposal Due Date (VOL-I 5.2), which matters for A5.
    - concern: Part of the interim handling, 'the Technical team flags the point in the bid', is a bidder action not grounded in the pack. It should be labelled as a proposal for the decision owner.
- **ADD-03/6.1** (analysis-003; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The new_text matches the clause printed in ADD-03:6.1 word for word, minus the leading '11.6' and the quotation marks. The number '11.6' is printed in the provision, so insert_unit with number 11.6 follows from the words.
    - concern: The anchor VOL-I:11.5 is inferred: the provision only says 'A new Clause 11.6 is added to Volume I' and names no position. Statement S-6.1-prov is labelled a fact ('the last existing clause of Section 11 at ADD-02 is VOL-I:11.5'), but its evidence is only the first sentence of 11.5, which does not …
    - concern: The change-propagation list names only VOL-I:11.5. The new clause works on the 'combined evaluation', so VOL-I:11.2 (row VOL-I-11.2-01, 65%/35%) is a related unit. The rationale mentions it, but it is not in dependencies.
    - concern: Row VOL-I-11.2-01, which this clause sits beside, shows only an interview_demo acceptance ('no observed human review'). That is not a human approval and should not be relied on as one.
- **ADD-03/7.1** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-opus-5-5
    - concern: The provision does not quote the old value ('amended from the value shown'). The value '1' was found in the target, and the controller has correctly marked it for a person to check.
    - concern: 'assessed on the same basis' supports leaving the Basis of assessment cell ('30-day rolling average') unchanged. The new value '0.5 mg/l' uses the same unit as the row's Unit cell ('mg/l'), so only the Limit cell needs to change.
    - concern: The follow-on list leaves out row VOL-V-29.3-01. That row lists VOL-II:T2-4/TP as a unit and its ADD-02 reading relies on the TP basis. The basis is unchanged, so the rolling-average list probably stands, but the row should be re-read at ADD-03 and not left unchanged without saying so.
    - concern: The reproduction says the Environmental Permit prevails, and the Permit is not supplied (I-PERMIT). After this change the reproduced TP limit may no longer match the Permit. The rationale says this is not decided, which is right; the I-PERMIT text only mentions the TN amendment and may need to cove…
    - concern: Row VOL-II-T2-4-TP is 'changed' with an interview_demo origin (no observed human review). The owner's confirmed transcription (3 Oct 2026, I-READING-T24) covers the image reading only, not this amendment.
- **ROW-ADD03-11.6** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The row's units are ['ADD-03:6.1'] and its target is the addendum provision, not the Volume I clause it inserts (VOL-I:11.6 once ADD-03/6.1 applies). Other rows bind to volume units (for example VOL-I-11.2-01 → VOL-I:11.2). Binding to the addendum text means later amendments to Clause 11.6 would no…
    - concern: Its group is 'evaluation', not a unit id. That does not match the convention used by the other rows (group 'VOL-I:11.2', 'VOL-I:11.5').
    - concern: The interpretation note refers to 'issue ISS-ADD03-6.1', but the row's issues field is empty, so the ambiguity is not linked in a way that can be traced.
    - concern: No owner is given, while the comparable rows name one (VOL-I-11.2-01: 'Bid manager').
    - concern: The quote and consequence 'none_stated' match the words: 'its determination shall be final' is not a stated rejection, disqualification, non-responsiveness or exclusion. The tie_band is kept as the printed words and not computed, which is correct.
- **ISS-ADD03-6.1** (analysis-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The 'ambiguous:' label covers three different points, against the one-point-one-class rule. (a) The basis of the 2% is a genuine ambiguity, and it is correctly quoted with two readings. (b) 'The further criteria are not stated anywhere in the pack' is a missing-evidence point. It should start with …
    - concern: The decision owner is only 'Bid management'. The rationale says Legal should review 'its determination shall be final', but Legal is not named as decision owner. That point should be a separate issue owned by Legal.
    - concern: Reading 1 ties 'combined evaluation' in ADD-03:6.1 to the 'combined score' in VOL-I:11.2. That link is itself an interpretation and should be stated as one, not taken as given.
    - concern: The verbatim quotations match ADD-03:6.1 and VOL-I:11.2 at ADD-02, and the issue correctly leaves the reading open for a person.
- **ADD-03/Q16-disp** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The no_effect follows from the printed words. The response 'No. Table 2-2 is unchanged.' contains no amending, obliging or excepting words. The controller's semantic check agrees.
    - concern: The target is uncertain and depends on interpretation S-Q16-I1. Q16 names 'Table 2-2' without a volume. The claim that VOL-II:T2-2 is the only Table 2-2 rests on a search result that is not printed here, so I cannot check it. A person must confirm the target.
    - concern: The cells of VOL-II:T2-2 are not printed here (cells: null), only its title. I cannot check the rationale's list of six rows (BOD5, COD, TSS, TN, TP, Temperature).
    - concern: Propagation: ADD-03:4.1, in another batch, changes the capacity in VOL-II:2.1. The rationale says VOL-II:2.1 and VOL-II:3.1 still cite Table 2-2, which is correct. Q16 also bears on rows VOL-II-2.1-01 and VOL-II-3.1-01, which list the T2-2 rows as units. Those rows are 'accepted' only by an intervi…
- **ADD-03/Q17** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The provision does use obliging words: 'Bidders shall price the Project as amended by this Addendum.' Recording it on its own unit (ADD-03:Q17) is scoped correctly. It does not wrongly widen to VOL-I:10.2.
    - concern: Whether effect 'adds_obligation' is correct is itself an interpretation. The response could be read as restating how the existing pricing obligation in VOL-I:10.2 ('The Bidder shall quote a single Availability Payment...') applies to the amended Project, rather than as a new obligation. The control…
    - concern: This op depends on ADD-03/Q17-row and goes with the ambiguity in ADD-03/Q17-issue. It should not be accepted separately from them.
- **ADD-03/Q17-row** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The requirement is quoted verbatim from ADD-03:Q17. 'consequence: none_stated' is correct, because Q17 prints no consequence.
    - concern: The row has no 'owner' field. Every comparable row names one (e.g. VOL-I-10.2-01: 'Commercial lead'), and the Q17 issue names Commercial.
    - concern: 'evidence' is empty. VOL-I-10.2-01, the pricing row this obligation bears on, carries EV-FORM-4F. A5 needs to know which evidence item satisfies this row.
    - concern: No 'issues' are linked. The accepted issue I-NO-CONSEQUENCE (the VOL-I 11.1(i) gate) is attached to other rows that state no consequence. The new Q17 ambiguity issue (ADD-03/Q17-issue) is also not linked, even though confidence_reason says the meaning is pending a Commercial decision.
    - concern: 'group' and 'scope' are both the free text 'Financial Proposal'. Other rows use a unit id as group and scope tags such as 'envelope_B' and 'price'. 'assessment: procedural' differs from VOL-I-10.2-01's 'pass_fail', and no reason is given.
    - concern: Propagation: VOL-I:10.2 is only 'listed, not changed'. Q17 directly concerns the Availability Payment, so row VOL-I-10.2-01 should be flagged for re-review. Its 'accepted' status comes from an interview_demo assumption, not an observed human review.
    - concern: Reading A in S-Q17-I1 adds 'and the Authority makes no other adjustment'. Q17 does not print those words. They are acceptable only as one of the two labelled readings, never as the row's meaning.
- **ADD-03/Q17-issue** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The issue is correctly classed as an ambiguity. The question ('Will the Availability Payment be adjusted for the increased capacity?') and the response ('Bidders shall price the Project as amended by this Addendum.') are quoted verbatim, and the response does not answer yes or no. Both readings are…
    - concern: Reading A's phrase 'with no separate adjustment by the Authority' goes beyond the printed words. It must stay a candidate reading and must not become the issue's conclusion.
    - concern: 'Which reading governs' is put as an open question for a person, which is correct. If Reading B is open, Bid management or Commercial may also want a DRAFT clarification question raised before the cut-off. This is optional and is not decided here.
    - concern: The capacity change in Reading A comes from ADD-03:4.1, which is in another batch and not yet validated. The 150,000 m³/day figure should be treated as depending on that batch.
- **ADD-03/Q18-disp** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
    - concern: The no_effect on VOL-I:7.1 itself is consistent with the evidence. 'One hundred and fifty (150) days from the Proposal Due Date as amended.' matches VOL-I:7.1 at ADD-02, and ADD-03:5.2 states 'The Proposal validity period in Clause 7.1 is unchanged.' The validity end date moves through the existing…
    - concern: Interpretation S-Q18-I1 says the period is 'restated in VOL-IV:F4-A/item2', and the payload lists VOL-IV:F4-A/item2 as a candidate target. At ADD-02 that unit is 'superseded'. Row VOL-IV-F4A-04 is 'REPLACED (by ADD-01:AppA)', and issue I-F4A-FIELDS records that the reissued Form 4-A drops the numbe…
    - concern: The rationale cites 'ADD-03:2.1/2.2'. ADD-03:2.2 is not printed in this request, so I cannot check it.
    - concern: Propagation: row VOL-I-7.1-01 has review status 'changed', from an interview_demo assumption rather than an observed human review. The PDD change in ADD-03:2.1 (to 'Thursday 10 December 2026') moves the PROPOSAL-VALIDITY date rule. That recomputation must be done by calculation in the programme pha…
    - concern: The target is uncertain because Q18 names no clause. A person must confirm that 'the Proposal validity period' means the period in VOL-I:7.1.
- **DS-ADD03-01** (downstream-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: Mostly sound: the quotations match the printed units, and the core point is real. ADD-03:3.1 says Form 4-G 'is withdrawn' and that Bidders 'shall not submit it'. Yet the only op, ADD-03/3.1, targets ADD-02:7.2 alone, so the form units (ADD-02:F4-G/T1/1, T1/3, para1) and the Envelope A list entry VO…
    - concern: The item states a status as fact. It says 'Row ADD-02-7.2-01 is therefore REVOKED and needs no new reading', but op ADD-03/3.1 is only at review 'proposed'. Statuses are set by the code and accepted by a person, so this should say 'would be revoked if the op is accepted'.
    - concern: Even after the op, row ADD-02-7.2-01 still cites VOL-I:9.1(e)+ADD-02, which the item itself says stays active. Saying the row 'needs no new reading' is therefore a conclusion that the evidence shown does not support. The point should stay open.
    - concern: It merges two classes of uncertainty. The reason given for the form staying active is a tool limit: the op engine cannot revoke a group, and check C22 rejects the member rows and the list insertion as targets. That is a software limitation and should be an escalation beginning 'software limitation:…
    - concern: The real ambiguity is not stated with its readings. ADD-03:3.1 withdraws the form 'added by Addendum No. 2 Section 7' but says only that 'Section 7.2 ... ceases to have effect'; it says nothing on Section 7.1, which inserted the form into the VOL-I 9.1 list. That should be an 'ambiguous:' point tha…
    - concern: Some claims cannot be checked from the evidence printed. Units ADD-02:F4-G/T1/2, T1/4, T1/5 and T1/6 are not in the request; the item and S-F2 say T1/5 and T1/6 are active. The current records list no activities, so form-4g-review and form-4g-sign cannot be checked. The EV-FORM-4G item record and t…
    - concern: The op is named inconsistently. The item and S-F2 call it 'ADD-03/3.1(a)', but the ops record has id 'ADD-03/3.1'.
    - concern: Losing the non_responsive consequence is not named as follow-on work. That consequence is quoted from ADD-02:7.2 in row ADD-02-7.2-01, and row ADD-02-F4G-04's note also relies on it. If 7.2 ceases, A3 changes, and the item should say so explicitly.
    - concern: The owner is given as Bid management only. The open questions also cover I-F4G-NO (owned by Technical) and how far a withdrawal reaches in the documents (arguably Legal or Document control). Naming the other owners would help the decision.
- **D-F4G06-ISSUE** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The main finding is supported. ADD-03:3.1 withdraws the whole of Form 4-G ('is withdrawn. Bidders shall disregard it and shall not submit it.'). The op record shows ADD-03/3.1 as one set_status op with status 'revoked' on ADD-02:7.2 only. The form heading VOL-I:9.1(e)+ADD-02 and the rows ADD-02:F4-…
    - concern: The issue cites op 'ADD-03/3.1(a)'. The ops record only has 'ADD-03/3.1'. The id needs correcting.
    - concern: The list of units still active is incomplete. Op ADD-02/7.1 also covers ADD-02:F4-G/para1, and the issue leaves it out. It lists only the heading and T1/1-6.
    - concern: Open question (1) mentions 'the VOL-I 9.1 list entry', but the dependencies leave out row VOL-I-9.1-01. That row lists 'Form 4-G' among the Envelope A items at ADD-02. The withdrawal directly affects it.
    - concern: The A5 activities 'form-4g-review' and 'form-4g-sign' cannot be checked from this request: current_records.activities is empty. I cannot confirm they exist.
    - concern: Two readings for the open interpretation are stated, (a) and (b), and they are hard to tell apart. The register records undertakings 5 and 6 as not in VOL-II 6. So reading (b), 'survive only so far as VOL-II 6 itself requires them', leads to the same result as reading (a) for those duties. The ambi…
    - concern: The point that the undertakings are 'not in VOL-II 6' rests on a note in the register, not on quoted VOL-II 6 text. No VOL-II 6 unit is in the evidence, so I cannot check it.
    - concern: The rationale says 'no op supports a removal'. A set_status op type does exist, as ADD-03/3.1 uses one. The rationale should say that no op has been proposed for the form units, which is amendment-phase work. As written, it can be read as a software limitation, which would be the wrong class.
- **D-VOL-I-3.4-READING** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The 3 Oct 2026 direction is carried forward 'unchanged', but its dependency, the PDD, did change. The note does name the direction and says only the PDD moved, and the reading stays pending a person. The reviewer should still confirm that the direction applies to the new date and is not re-decided …
    - concern: VOL-I 3.4 says only 'after the Proposal Due Date'. The time element '14:00 hours' in the cut-off comes from the recorded owner direction, not from the words of 3.4. This is not new, but it is still not stated in 3.4.
    - concern: The clarification date (Thursday 26 November 2026) depends on the quoted calculate output, which cannot be reproduced here. The earlier row called its date 'the planning reading'. This item now says 'single reading' (readings_differ: false). That is consistent with the quoted tool output.
    - concern: The note says the new clarification cut-off falls on the old omission-claim cut-off date. This is accurate and useful for the bid team, and the note correctly keeps the two cut-offs separate. The interview_demo record and the I-VOL-III issue are kept as recorded and are not treated as resolved.
- **D-VOL-I-5.2-READING** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The dependencies list only VOL-I-6.1-01. Row VOL-I-3.4-01 states its own cut-off as separate from this deadline and quotes this deadline's date in a parameter, so it could be listed too. So could any clarification-register or A5 items that use this cut-off, though none are shown in the request.
    - concern: The computed date (Thursday 26 November 2026) depends on the quoted calculate output, which cannot be reproduced here. It is correctly kept out of the date rule.
- **D-VOL-I-6.1-READING** (downstream-002; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The note relies on 'the VOL-I 7.1 Proposal validity, whose length ADD-03 5.2 states is unchanged'. Neither VOL-I:7.1 nor ADD-03:5.2 is printed in the request, so I cannot check this. It should be backed by quoted evidence or removed.
    - concern: The note says VOL-I-6.3-01 is 're-read in this set', but no reading of VOL-I-6.3-01 is among the items reviewed here, so I cannot check that.
    - concern: ADD-03 2.1 ends with '14:00 Riyadh time'; the target reads '14:00 hours Riyadh time'. Treating this as a restatement of the unchanged time is reasonable, and the note quotes both. The quote and the VOL-I 6.6 consequence ('will be rejected unopened and returned to the Bidder') match the evidence.
- **DS-ADD03-R-6.7-01** (downstream-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The reading treats the VOL-I 6.7 cut-off ('before the Proposal Due Date') as following the date in VOL-I 6.1 as amended. The earlier recorded reading relied on VOL-I 2.6 for that link, but VOL-I 2.6 is not printed in this request and the item's note does not cite it. The carry-over to 10 December 2…
    - concern: The note says 'The time is unchanged: 14:00 hours Riyadh time' but quotes only VOL-I 6.1. ADD-03:2.1 itself ends with ', 14:00 Riyadh time', outside the quoted substitution. The op replaces only the date, which fits reading that phrase as a restatement. The item should quote the provision's own tra…
    - concern: The parameter express_late_prohibition ('modifications only ... not extended to withdrawals') carries the owner's session-08 direction. That direction named 26 November 2026, and the review behind it is interview_demo origin ('no observed human review'). The item correctly leaves the carry-over to …
    - concern: The statement relied on, downstream-003/S-F-REVIEW-ORIGIN, cites as evidence VOL-I:6.4 'The Bid Bond shall be in the amount of SAR 5,600,000'. That span does not support a statement about review origin and status. VOL-I:6.4 is printed in this request only at SAR 4,500,000 (before the addendum), and…
    - concern: S-F-REVIEW-ORIGIN names ADD-03 ops 4.2(a), 4.2(b), 5.1 and 5.2(b). Of these, only ADD-03/4.2 (unsplit) appears in current_records.ops; the others cannot be checked here.
- **DS-ADD03-R-8.5-01** (downstream-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The item rests on ops 'ADD-03/4.2(a)' and 'ADD-03/4.2(b)', which are not in current_records.ops. The only printed op for this provision, ADD-03/4.2, targets 'VOL-I:8.5' (the clause body, which does not contain the threshold) rather than 'VOL-I:8.5#fn12'. It quotes old '80,000 m3/day' rather than th…
    - concern: Substance checks out against ADD-03:4.2: 'deleting ‘80,000 m³/day’ and substituting ‘100,000 m³/day’' in footnote 12; two plants and the ten-year look-back 'are unchanged'; the rejection words in fn12 are untouched. The target (fn12, not the body of 8.5) is correct.
    - concern: The note asserts 'ADD-03 does not change ADD-01 Q5'. Only ADD-03:2.1 and ADD-03:4.2 are printed, so this claim about the whole addendum cannot be checked from the evidence shown.
    - concern: The new parameter lookback_anchor moves the window with the PDD as amended by ADD-03/2.1. That rests on VOL-I 2.6 (not printed) and on reading 'the ten (10) year look-back are unchanged' as fixing the length of the period, not the window as it stood before. That reading is the natural one, but the …
    - concern: The rationale's claims (no other statement of 80,000 m³/day besides footnote 12; the Form 4-B capacity field; VOL-I 9.5) rest on searches and units not printed in this request and cannot be checked here.
    - concern: As for the first item, statement S-F-REVIEW-ORIGIN cites unrelated evidence (VOL-I:6.4 'SAR 5,600,000') for a statement about review origin and status.
- **DS-ADD03-I-REF-THRESHOLD** (downstream-003; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The A3 line reads: 'Reference plants: two plants each not less than 100,000 m³/day (ADD-03 4.2), else ‘shall be rejected without further evaluation’'. It leaves out the other condition footnote 12 attaches to the same rejection: 'each having achieved commercial operation within the ten (10) years p…
    - concern: The dependencies EV-FORM-4B, EV-COMPLETION-CERT and the activity 'references' are not in the evidence printed here; current_records.activities is empty. Their link to footnote 12 cannot be checked from this request.
    - concern: The quotation from VOL-I:8.5 leaves off the footnote marker printed in the unit ('Form 4-B.¹²'). The controller accepted it as verbatim, so this is minor.
    - concern: No bidder facts are asserted, the issue is left open with decision owner 'Technical', and the consequence is quoted from fn12 and not inferred. This is consistent with the rules. The issue rests on ops 4.2(a) and 2.1, which are proposed only and not accepted. The record for 4.2(a) is not printed, a…
- **D-ADD03-04** (downstream-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The note says the programme 'must now reach PCOD within the same 36 months for the 150,000 m³/day capacity of VOL-II 2.1 as amended by ADD-03/4.1(a)'. This rests on op ADD-03/4.1(a), which is still only proposed (S-F1 is checked against the text 'after the proposed ops'). The note should say that t…
    - concern: Q15 is a bidder question and Authority answer printed in ADD-03. The note treats it as an op ('confirms'). Whether answers in the ADD-03 Q&A table bind is not shown in the evidence: the pack's own words on how Q&A answers bind are not printed, and ADD-01 3.2 says the pre-bid minutes do not bind. Th…
    - concern: The note names VOL-V 18.4 (the cap) and VOL-II 7.2 (the 90% reliability run). Neither unit is printed in this request. They can be checked only through the quotes in the curated records VOL-V-12.1-01 and VOL-II-7.2-01.
    - concern: The note says PCOD needs the reliability run 'at 90% of nominal capacity'. The quote in VOL-II-7.2-01 says 'not less than 90%'. The note should keep the 'not less than' wording. It also implies, without saying so, that the run is now tied to the amended 150,000 m³/day nominal capacity. Any figure t…
    - concern: The rationale says 'Text-layer units only'. ADD-03:Q15 is a table row with no crop hash. The request does not show whether that row came from the text layer or from an image, so this cannot be checked.
    - concern: Passing programme-risk and pricing to the Technical and Commercial leads is right. But no issue or escalation is opened with a named decision owner. The handover sits only in the note text.
- **D-ADD03-09** (downstream-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The ambiguity itself is real. The printed words 'within two per cent (2%) of one another' do not say what the 2% is measured on. But Reading A depends on a quotation from VOL-I 11.2 ('on a combined score calculated on a weighting of sixty per cent (60%) technical and forty per cent (40%) commercial…
    - concern: Page mismatch. The evidence cites doc 'VOL-I', unit 'VOL-I:11.5+ADD-03', page 2, but the issue itself puts VOL-I 11.2 on p5. The inserted wording is printed in ADD-03:6.1 (pp. 1-2). Page 2 looks like an ADD-03 page credited to VOL-I. Document control should check this.
    - concern: Three different points are filed under one 'ambiguous:' label: (1) what the 2% is measured on (a genuine ambiguity); (2) the 'further criteria' not being stated (an open discretion given to the Authority, not two competing readings of the words); (3) what 'its determination shall be final' means (a…
    - concern: The owner is Bid management. The meaning of 'its determination shall be final' is a legal question, so Legal should be named as its decision owner.
    - concern: show_in_a3 is true, and the a3 text describes a discretion. A3 holds only the bid-out consequences the pack states (rejection, disqualification, non-responsiveness, exclusion). New 11.6 states none of these. Putting it in A3 lists as a consequence something the words do not state.
    - concern: 'The clause bears on bid strategy and pricing near the margin' is the proposer's own framing. No unit in the pack says this. It should be marked as framing, not presented as an effect.
    - concern: The draft clarification CQ-ADD03-TIE-BAND is mentioned, but the request carries no clarification records, so it cannot be checked.
- **DS-31-ISSUE** (downstream-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The main point is supported by the evidence shown. ADD-03:3.1 says Form 4-G 'is withdrawn. Bidders shall disregard it and shall not submit it.' The only op, ADD-03/3.1, is a set_status to 'revoked' and its only target is ADD-02:7.2. VOL-I:9.1(e)+ADD-02, ADD-02:F4-G/para1 and ADD-02:F4-G/T1/1 are pr…
    - concern: Several claims in the issue text cannot be checked against the evidence shown. Units ADD-02:F4-G/T1/2 to T1/6 are not printed. Of rows ADD-02-F4G-01 to -07, only -01, -02 and -04 are printed. The A5 activities form-4g-review and form-4g-sign do not appear: current_records.activities is empty. The c…
    - concern: The issue calls the op 'the promoted op ADD-03/3.1(a)'. The record shown has id 'ADD-03/3.1' with no '(a)', and its review status is 'proposed', not promoted. The item misstates the status of the op it relies on.
    - concern: The follow-on list is incomplete. Row VOL-I-9.1-01 (owner Bid manager) still lists 'Form 4-G' among its Envelope A items at ADD-02. Row ADD-02-7.2-01 lists unit VOL-I:9.1(e)+ADD-02, which stays active. Issue I-F4G-LETTERING (re-lettering after Form 4-G was inserted into VOL-I 9.1) depends directly …
    - concern: The A3 line (show_in_a3 true) does not state a consequence printed in the pack: S-31-F1 itself says 'no consequence is printed for submitting it'. A3 is limited to consequences the pack states. Whether this belongs in A3 should be confirmed so that a reader does not take it as a stated bid-out cons…
    - concern: The controller's human-owned check reads 'withdrawn' as the issue withdrawing a question. In fact the word quotes the provision ('is withdrawn'), so it should not be read as a resolution. The issue still has to stay open pending a human decision.
    - concern: The reviews of the related rows and issues all have origin 'interview_demo' ('no observed human review'). Nothing in this item should treat them as observed human approvals. The item does not, but those records should keep that origin.
- **DS-ADD03-ISSUE-F4G** (downstream-006; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: The main point holds on the evidence shown. ADD-03:3.1 withdraws the whole of Form 4-G ('added by Addendum No. 2 Section 7, is withdrawn. Bidders shall disregard it and shall not submit it.'). The only op shown, ADD-03/3.1, sets just ADD-02:7.2 to 'revoked'. ADD-02:7.1 is printed with status 'activ…
    - concern: The dependencies leave out row ADD-02-7.2-01. That row carries the A3 consequence quoted from ADD-02:7.2 ('Failure to submit Form 4-G shall render the Proposal non-responsive.'), and the op revokes that clause. It is the row the withdrawal affects most and should be listed. The issue also does not …
    - concern: show_in_a3 is false, but A3 currently shows a Form 4-G non-responsive consequence (row ADD-02-7.2-01) and I-F4G-NO. The issue does not explain why the withdrawal should stay out of A3. The issue's own 'a3' text also conflicts with show_in_a3 false.
    - concern: The text refers to 'promoted ops' and 'op ADD-03/3.1(a)'. The ops record shown has the id 'ADD-03/3.1' with no '(a)', and current_records give op:ADD-03/3.1 the status 'proposed', not promoted. The statement S-F4G-OPS-PARTIAL makes the same claim.
    - concern: Several claims cannot be checked against the evidence shown. The units ADD-02:F4-G/T1/1-6 are not printed, so their 'active' status at ADD-03 is unverified. current_records.activities is empty, so the activities form-4g-review, form-4g-sign and assemble-envelope-a cannot be confirmed to exist.
    - concern: The sentence "Activity 'assemble-envelope-a' is proposed to drop its Form 4-G instruction" puts an A5 proposal inside the issue text, and nothing shown supports it. That is follow-on work for the phase that owns it. In the same text where the question is asked of Document control, it also partly de…
    - concern: The issue does not state the uncertainty class. ADD-03:3.1 withdraws the form 'added by Addendum No. 2 Section 7' but says only that 'Section 7.2 ... ceases to have effect'. That supports more than one reading: either all of Section 7, including the 7.1 insertion into the VOL-I 9.1 list, falls away…
    - concern: The issue's evidence list does not cite the target ADD-02:7.1, although the text quotes it. The evidence cites only the last sentence of ADD-03:3.1 and ADD-02:F4-G/para1. A quotation of the signature line shows the form's text, not its 'active' status.
    - concern: Rows ADD-02-F4G-01 to -07, VOL-I-9.1-01 and the related issues carry reviews whose origin is 'interview_demo' ('no observed human review'). The issue does not call these approved, which is correct, but it should keep that origin visible when it says the rows 'still stand'.
- **DS-ADD03-ISS-31** (downstream-008; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
    - concern: Opening the issue is sound, and its quotations are verbatim. 'Bidders shall disregard it and shall not submit it. Section 7.2 of Addendum No. 2 ceases to have effect.' matches ADD-03:3.1. 'FORM 4-G — CYBERSECURITY COMPLIANCE UNDERTAKING' matches VOL-I:9.1(e)+ADD-02. 'Only ADD-02 7.2 is revoked' mat…
    - concern: Paraphrase: 'takes Form 4-G out of the RFP Documents' is not in the provision. ADD-03:3.1 says the form 'is withdrawn'. The issue should quote that word instead of describing the effect in its own terms.
    - concern: Can't verify from the evidence shown: the issue says 'rows ADD-02-F4G-01 to -07' remain, but only ADD-02-F4G-01 and ADD-02-F4G-04 are in current_records. Rows -02, -03 and -05 to -07 are not shown.
    - concern: Can't verify from the evidence shown: the issue names activities 'form-4g-review' and 'form-4g-sign', but current_records.activities is empty ({}). Nothing in the request shows these activities exist.
    - concern: Missing knock-on effect (bid-out consequence, A3): row ADD-02-7.2-01 rests directly on the revoked ADD-02:7.2. It quotes the consequence 'Failure to submit Form 4-G shall render the Proposal non-responsive.' (class non_responsive), and its review is an interview_demo 'changed' record. The issue nev…
    - concern: Missing knock-on effect: row VOL-I-9.1-01 (accepted through interview_demo) still lists 'Form 4-G' among its Envelope A items at ADD-02. It is not named among the records that rest on Form 4-G. The issue names the unit VOL-I:9.1(e)+ADD-02 but not this row. The confidence_reason of row VOL-II-6.3-01…
    - concern: Wrong class: point (2) is labelled 'ambiguous:', but no words shown support Reading B ('the Authority may still expect them through another document'). ADD-03:3.1 withdraws the whole form and says 'Bidders shall disregard it'. No unit shown carries undertakings 3-6 elsewhere. A genuine ambiguity ne…
    - concern: Can't verify from the evidence shown: undertakings 3-6 ('24-hour incident notice, annual penetration test, multi-factor remote access') and VOL-II 6.2 are not in the units shown. Only undertaking 3 is quoted, in row ADD-02-F4G-01, and only VOL-II:6.3 is printed.
    - concern: Point (1) could be handled differently: ADD-03:3.1 names its target directly ('Form 4-G ... is withdrawn'). Withdrawal ops on the form units and the VOL-I 9.1 entry could arguably be proposed rather than only escalated. If the tool can't represent them, the reason should start with 'software limita…
    - concern: The issue's own wording is right to say 'No decision recorded; pending a human decision' and that the interview_demo acceptances carry no handling instruction.

## Requests: failures, deferrals, repairs and route notices

- every request was answered at the first call, parsed, and fitted its context

Route notices (how the requests were served; they change no status):
- **capabilities_declared** (analysis-001): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: declared for request sizing, not verified by this tool; Claude Code CLI 2.1.296 text/tool/image conformance observed locally on 11 Oct 2…
- **capabilities_declared** (analysis-002): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: declared for request sizing, not verified by this tool; Claude Code CLI 2.1.296 text/tool/image conformance observed locally on 11 Oct 2…
- **capabilities_declared** (downstream-001): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: declared for request sizing, not verified by this tool; Claude Code CLI 2.1.296 text/tool/image conformance observed locally on 11 Oct 2…
- **capabilities_declared** (downstream-002): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: declared for request sizing, not verified by this tool; Claude Code CLI 2.1.296 text/tool/image conformance observed locally on 11 Oct 2…
- **capabilities_declared** (downstream-003): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: declared for request sizing, not verified by this tool; Claude Code CLI 2.1.296 text/tool/image conformance observed locally on 11 Oct 2…
- **capabilities_declared** (downstream-004): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: declared for request sizing, not verified by this tool; Claude Code CLI 2.1.296 text/tool/image conformance observed locally on 11 Oct 2…
- **capabilities_declared** (downstream-005): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: declared for request sizing, not verified by this tool; Claude Code CLI 2.1.296 text/tool/image conformance observed locally on 11 Oct 2…
- **capabilities_declared** (downstream-006): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: declared for request sizing, not verified by this tool; Claude Code CLI 2.1.296 text/tool/image conformance observed locally on 11 Oct 2…
- **capabilities_declared** (downstream-007): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: declared for request sizing, not verified by this tool; Claude Code CLI 2.1.296 text/tool/image conformance observed locally on 11 Oct 2…
- **capabilities_declared** (downstream-008): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: declared for request sizing, not verified by this tool; Claude Code CLI 2.1.296 text/tool/image conformance observed locally on 11 Oct 2…
- **capabilities_declared** (downstream-009): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: declared for request sizing, not verified by this tool; Claude Code CLI 2.1.296 text/tool/image conformance observed locally on 11 Oct 2…
- **capabilities_declared** (downstream-010): capabilities declared, not verified: host claude-code headless (claude-opus-5-5) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: declared for request sizing, not verified by this tool; Claude Code CLI 2.1.296 text/tool/image conformance observed locally on 11 Oct 2…

## Manual interventions (the person's actions)

- none

### What the run did with them, and its automatic host sessions (not a person)

- 2026-10-15T14:12:22Z: host session (automatic) — batch analysis-001 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session over the MCP tools; not a person
- 2026-10-15T14:14:31Z: host session (automatic) — batch analysis-002 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session over the MCP tools; not a person
- 2026-10-15T14:16:02Z: submission reused (automatic) — batch analysis-003 by tenderpack.ai.workflow; the host session's staged set ADD-03-host-20261015T141228Z-645f (made in this drive) was revalidated and taken instead of asking the batch again
- 2026-10-15T14:16:58Z: submission reused (automatic) — batch analysis-004 by tenderpack.ai.workflow; the host session's staged set ADD-03-host-20261015T141208Z-792e (made in this drive) was revalidated and taken instead of asking the batch again
- 2026-10-15T14:21:45Z: host session (automatic) — batch downstream-001 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session; not a person
- 2026-10-15T14:22:34Z: host session (automatic) — batch downstream-002 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session; not a person
- 2026-10-15T14:22:34Z: host session (automatic) — batch downstream-003 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session; not a person
- 2026-10-15T14:22:35Z: host session (automatic) — batch downstream-004 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session; not a person
- 2026-10-15T14:25:51Z: host session (automatic) — batch downstream-005 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session; not a person
- 2026-10-15T14:25:51Z: host session (automatic) — batch downstream-006 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session; not a person
- 2026-10-15T14:26:15Z: host session (automatic) — batch downstream-007 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session; not a person
- 2026-10-15T14:27:21Z: host session (automatic) — batch downstream-008 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session; not a person
- 2026-10-15T14:27:22Z: host session (automatic) — batch downstream-009 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session; not a person
- 2026-10-15T14:27:25Z: host session (automatic) — batch downstream-010 by tenderpack.ai.hostsession; host model claude-code headless (claude-opus-5-5); a headless host session; not a person

## The diff (ADD-02 → ADD-03; [diff.md](diff.md))

## What changed from ADD-02 to ADD-03

### ADD-03: PARTIAL (issued 2026-11-08)

- ops: 13 (0 invalid); provisions: 19 (2 unresolved)
- validated state: ADD-02 — this addendum does NOT replace it until every provision is treated and every op is valid
- UNRESOLVED ADD-03:2.2: Every period calculated by reference to the Proposal Due Date is adjusted accordingly.
- UNRESOLVED ADD-03:4.3: Volume I Clause 1.3 is amended correspondingly.
- cover summary vs provisions (C28, report only): 8 finding(s)
  - not found: 'withdraws Form 4-G': no provision of ADD-03 does this
  - not found: 'adds a new Clause 11.6': no provision of ADD-03 does this
  - understated: 'responds to clarification requests 15 to 18', but ADD-03/Q17 adds an obligation (ADD-03:Q17): 'Bidders shall price the Project as amended by this Addendum.'
  - omitted: ADD-03/3.1(a) ends the effect of ADD-02:7.2; the summary does not mention it: 'Form 4-G (Cybersecurity Compliance Undertaking), added by Addendum No. 2 Section 7, is withdrawn. Bidders shall disregard it and shall not submit it. Section 7.2 of Addendum No. 2 ceases to have effect.'
  - omitted: ADD-03/5.1 amends VOL-I:6.4; the summary does not mention it: 'In Volume I Clause 6.4, ‘SAR 4,500,000 (four million five hundred thousand Saudi Riyals)’ is deleted and ‘SAR 5,600,000 (five million six hundred thousand Saudi Riyals)’ is substituted.'
  - omitted: ADD-03/5.2(a) amends VOL-I:6.3; the summary does not mention it: 'In Volume I Clause 6.3, ‘one hundred and eighty (180) days’ is deleted and ‘two hundred and ten (210) days’ is substituted. The Proposal validity period in Clause 7.1 is unchanged.'
  - omitted: ADD-03/5.2(b) confirms VOL-I:7.1; the summary does not mention it: 'In Volume I Clause 6.3, ‘one hundred and eighty (180) days’ is deleted and ‘two hundred and ten (210) days’ is substituted. The Proposal validity period in Clause 7.1 is unchanged.'
  - omitted: ADD-03/6.1 inserts new text after VOL-I:11.5; the summary does not mention it: 'A new Clause 11.6 is added to Volume I: ‘11.6 Where, on completion of the combined evaluation, two or more Proposals are within two per cent (2%) of one another, the Authority may apply such further criteria as it considers appropriate to …'

#### Validated vs candidate (partial should not mean useless)

- validated (unchanged, ADD-02): `<outputs>/a3/a3.pdf` (one page), `<outputs>/a5/`
- candidate (CANDIDATE — NOT VALIDATED, ADD-03 as proposed): `<outputs>/a3/a3_candidate.pdf` / `.md`, `<outputs>/a5/candidate/`

**What may be changing.** ADD-03 is PARTIAL: 2 of 19 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 13 op(s) that are valid there stood (each still a proposal: review accepted 13), A3 would gain 1 row(s) (ADD-03-cover-para3-01 (ADD-03/cover/para3)), lose 1 (ADD-02-7.2-01 (ADD-03/3.1(a))) and change 5 (ADD-02-F4G-04 (register), VOL-I-6.1-01 (ADD-03/2.1), VOL-I-6.3-01 (ADD-03/5.2(a)), VOL-I-6.4-01 (ADD-03/5.1) and 1 more); A5, replanned at ADD-03's issue date (2026-11-08), would move the latest dates of 43 activities (assemble-envelope-a, assemble-envelope-b, bond-approval, bond-issue and 39 more), add 0 (none) and remove 0 (none), and marks 8 REVIEW through relationships. Not settled: 8 activities blocked by an unresolved row (references, bond-approval, clarifications, form-4g-review and 4 more), 5 STALE row(s), 0 obligation(s) reaching no output (C46), 9 relationship chain(s) blocked or incomplete, 1 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT and 7 more. Nothing here is validated, accepted or applied to the real state.

### Requirements

- new: 5; out of force: 1; changed: 20

- NEW ADD-03-cover-para3-01: NEW (introduced by ADD-03/cover/para3)
- NEW ADD-03-6.1-01: NEW (introduced by ADD-03/6.1) (by ADD-03/6.1)
- NEW ADD-03-Q17-01: NEW (introduced by ADD-03/Q17)
- NEW ADD-03-3.1-01: NEW (introduced by ADD-03:3.1)
- NEW ADD-03-3.2-01: NEW (introduced by ADD-03:3.2)
- OUT ADD-02-7.2-01: REVOKED (ADD-03/3.1(a))
- CHANGED VOL-I-6.1-01: wording; quoted words; PDD 2026-11-26 -> 2026-12-10 (by ADD-03/2.1)
- CHANGED VOL-I-5.2-01: CLARIFICATION-CUTOFF 2026-11-12 -> 2026-11-26
- CHANGED VOL-I-6.3-01: wording; quoted words; BID-BOND-VALIDITY 2027-05-25 -> 2027-07-08; reading: parameters (by ADD-03/5.2(a))
- CHANGED VOL-I-6.4-01: wording; quoted words; reading: parameters (by ADD-03/5.1)
- CHANGED VOL-I-6.4-02: wording (by ADD-03/5.1)
- CHANGED VOL-I-7.1-01: PROPOSAL-VALIDITY 2027-04-25 -> 2027-05-09
- CHANGED VOL-I-8.3-01: ISO-CURRENT-AT 2026-11-26 -> 2026-12-10; reading: parameters
- CHANGED VOL-I-8.5-01: wording; quoted words; REFERENCE-LOOKBACK 2016-11-27 -> 2016-12-11; reading: parameters (by ADD-03/4.2(a))
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
- CHANGED VOL-V-29.3-01: secondary unit VOL-II:T2-4/TP amended by ADD-03/7.1 (Limit: 1 -> 0.5) (by ADD-03/7.1)
- CHANGED VOL-V-31.1-02: VOL-II T2-4/TP: Limit 1 -> 0.5 mg/l by ADD-03/7.1 (depends on it: REL-T24-UNAVAILABILITY (limit_applies, confirmed))
- CONFIRMED (unchanged) ADD-02-F4G-06: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03 because op ADD-03/3.1(a) revoked ADD-02:7.2. The undertaking unit ADD-02:F4-G/T1/5 is still 'active' in the effective text after the proposed…')
- CONFIRMED (unchanged) ADD-02-F4G-07: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03 because op ADD-03/3.1(a) revoked ADD-02:7.2. The undertaking unit ADD-02:F4-G/T1/6 is still 'active' in the effective text after the proposed…')
- CONFIRMED (unchanged) VOL-V-12.1-01: confirmed by ADD-03/Q15 (confirms; ADD-03:Q15); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-read at ADD-03. ADD-03 Q15 asks 'Following the capacity increase, will the Authority extend the construction period in Volume V Clause 12.1?' The Authority …')

### Stale readings and decisions

- STALE ADD-02-F4G-01: ADD-02:7.2 changed since ADD-02 (by ADD-03/3.1(a))
- STALE ADD-02-F4G-05: ADD-02:7.2 changed since ADD-02 (by ADD-03/3.1(a))
- STALE ADD-02-F4G-02: ADD-02:7.2 changed since ADD-02 (by ADD-03/3.1(a))
- STALE ADD-02-F4G-03: ADD-02:7.2 changed since ADD-02 (by ADD-03/3.1(a))
- STALE ADD-02-F4G-04: ADD-02:7.2 changed since ADD-02 (by ADD-03/3.1(a))
- DECISION VOID (content changed since review): ADD-02-F4G-01, ADD-02-F4G-05, ADD-02-F4G-02, ADD-02-F4G-03, ADD-02-F4G-04
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

#### Proposed relationship (10)
- ADD-01-AppA-01 (row; ACTIVE) <- ADD-03-cover-para3-01 via REL-AI-002 [depends_on; link proposed]
- VOL-I-10.2-01 (row; ACTIVE) <- ADD-03-Q17-01 via REL-AI-004 [depends_on; link proposed]
- VOL-I-12.1-01 (row; ACTIVE) <- VOL-I:11.5+ADD-03 via REL-AI-003 [depends_on; link proposed]
- VOL-II-7.2-01 (row; ACTIVE) <- VOL-II:2.1 via REL-AI-001 [depends_on; link proposed]
- VOL-II-7.2-01 (row; ACTIVE) <- VOL-II:T2-4 via REL-T24-RELIABILITY-RUN > REL-AI-007 > REL-AI-001 [depends_on; link proposed]; cycle: VOL-II-7.2-01 > VOL-II:2.1 > VOL-II-7.2-01 (not followed again); BLOCKED: cannot be established: the Environmental Permit issued for the site not supplied (that the reproduced Table 2-4 limits, as amended by the addenda, are the limits that govern (the Permit prevails over the reproduction), and the limit of any parameter not listed (Note 1); Permit compliance is not claimed) [at VOL-II:T2-4, REL-MISSING-ENVIRONMENTAL-PERMIT]
- VOL-II:2.1 (unit; ACTIVE) <- VOL-II:2.1 via REL-AI-001 > REL-AI-007 [depends_on; link proposed]; also changed directly; cycle: VOL-II:2.1 > VOL-II-7.2-01 > VOL-II:2.1 (not followed again)
- VOL-II:2.1 (unit; ACTIVE) <- VOL-II:T2-4 via REL-T24-RELIABILITY-RUN > REL-AI-007 [depends_on; link proposed]; also changed directly; BLOCKED: cannot be established: the Environmental Permit issued for the site not supplied (that the reproduced Table 2-4 limits, as amended by the addenda, are the limits that govern (the Permit prevails over the reproduction), and the limit of any parameter not listed (Note 1); Permit compliance is not claimed) [at VOL-II:T2-4, REL-MISSING-ENVIRONMENTAL-PERMIT]
- VOL-IV-F4F-01 (row; ACTIVE) <- ADD-03-Q17-01 via REL-AI-004 [depends_on; link proposed]
- VOL-IV-F4F-02 (row; ACTIVE) <- ADD-03-Q17-01 via REL-AI-004 [depends_on; link proposed]
- form-4a-prep (activity) <- ADD-03:cover/para3 via REL-AI-006 [depends_on; link proposed]

#### Possible impact (6)
- BID-BOND-VALIDITY (date rule) <- ADD-03:2.2 via REL-AI-009 [depends_on; link possible]
- CLARIFICATION-CUTOFF (date rule) <- ADD-03:2.2 via REL-AI-009 [depends_on; link possible]
- PROPOSAL-VALIDITY (date rule) <- ADD-03:2.2 via REL-AI-009 [depends_on; link possible]
- REFERENCE-LOOKBACK (date rule) <- ADD-03:2.2 via REL-AI-009 [depends_on; link possible]
- VOL-I-10.2-01 (row; ACTIVE) <- ADD-03:Q17 via REL-AI-011 [depends_on; link possible]
- VOL-I-11.2-01 (row; ACTIVE (as amended by ADD-02/T1-1-rev/note(2))) <- ADD-03:6.1 via REL-AI-010 [depends_on; link possible]

#### Referenced but not supplied: conclusions in play that cannot be established (1)
- VOL-II-T2-4-TP (row; AMENDED (ADD-03/7.1)) <- target changed via REL-MISSING-ENVIRONMENTAL-PERMIT [missing_document; link confirmed]; also changed directly. NOT SUPPLIED: the Environmental Permit issued for the site; cannot be established: that the reproduced Table 2-4 limits, as amended by the addenda, are the limits that govern (the Permit prevails over the reproduction), and the limit of any parameter not listed (Note 1); Permit compliance is not claimed; context (not binding): ADD-01:AppB/item-5-effluent-standards p4 'the permit was under review by the regulator and that any change would be issued by Addendum.' (pre-bid minutes; they do not bind the Authority (ADD-01 3.2, p1))

### Disqualifiers (A3)

- LEAVES ADD-02-7.2-01

### Earlier answers to re-read against the new text (never revoked; a person decides)

- `ADD-01:Q1` (ADD-01): relies on VOL-II:3.1, which VOL-II:T2-4/TP (changed by ADD-03/7.1) governs through REL-T24-PROCESS-DESIGN; to be re-read against the new text of VOL-II:T2-4/TP (ADD-03/7.1); a person decides whether the answer still holds
- `ADD-01:Q3` (ADD-01): cites VOL-I:6.4, changed by ADD-03/5.1; to be re-read against the new text of VOL-I:6.4 (ADD-03/5.1); a person decides whether the answer still holds
- `ADD-01:Q5` (ADD-01): cites VOL-I:8.5#fn12, changed by ADD-03/4.2(a); to be re-read against the new text of VOL-I:8.5#fn12 (ADD-03/4.2(a)); a person decides whether the answer still holds
- `ADD-02:Q7` (ADD-02): relies on VOL-I:12.1, which VOL-I:11.5+ADD-03 (changed by ADD-03/6.1) governs through REL-AI-003; to be re-read against the new text of VOL-I:11.5+ADD-03 (ADD-03/6.1); a person decides whether the answer still holds
- `ADD-02:Q8` (ADD-02): cites VOL-I:6.4, changed by ADD-03/5.1; to be re-read against the new text of VOL-I:6.4 (ADD-03/5.1); a person decides whether the answer still holds
- `ADD-02:Q11` (ADD-02): quotes '120,000 m³/day', a figure ADD-03/4.1(a) replaced; to be re-read against the new text of VOL-II:2.1 (ADD-03/4.1(a)); a person decides whether the answer still holds

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
- REWORK clarifications: requirement changed: VOL-I-3.4-01 (dates, parameters), VOL-I-5.2-01 (dates)
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
- REWORK deviations-review: requirement changed: VOL-V-29.3-01 (cited units: cited unit VOL-II T2-4/TP: Limit 1 -> 0.5 mg/l by ADD-03/7.1), VOL-V-31.1-02 (dependency: VOL-II T2-4/TP: Limit 1 -> 0.5 mg/l by ADD-03/7.1 (depends on it: REL-T24-UNAVAILABILITY (limit_applies, confirmed)))
- CONFIRMED (unchanged) deviations-review: VOL-V-12.1-01: confirmed by ADD-03/Q15 (confirms; ADD-03:Q15); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-read at ADD-03. ADD-03 Q15 asks 'Following the capacity increase, will the Authority extend the construction period in Volume V Clause 12.1?' The Authority …'); text, cells, dates, status and consequence unchanged: work done stands
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
- REWORK form-4a: requirement changed: ADD-01-AppA-01 (Addenda to acknowledge: ADD-03 issued since ADD-02: 'Bidders shall acknowledge receipt in Form 4-A.'), ADD-03-cover-para3-01 (text, status, consequence, quote), VOL-I-7.1-01 (dates), VOL-IV-F4A-01 (anchor date: PDD moved 2026-11-26 -> 2026-12-10 (VOL-I 6.1 as amended by ADD-01 2.1, ADD-03 2.1); ADD-01 AppA/proposal-due-date prints 2026-11-12: CONFLICT with the amended PDD, not corrected (a person decides)), VOL-IV-F4A-02 (anchor date: PDD moved 2026-11-26 -> 2026-12-10 (VOL-I 6.1 as amended by ADD-01 2.1, ADD-03 2.1); ADD-01 AppA/proposal-due-date prints 2026-11-12: CONFLICT with the amended PDD, not corrected (a person decides))
- MOVED form-4a: latest start 2026-11-23 -> 2026-12-07
- STATUS form-4a: timing OK -> OK; total float +12 -> +11 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK form-4a-prep: requirement changed: ADD-01-AppA-01 (Addenda to acknowledge: ADD-03 issued since ADD-02: 'Bidders shall acknowledge receipt in Form 4-A.'), ADD-03-cover-para3-01 (text, status, consequence, quote), VOL-I-7.1-01 (dates), VOL-IV-F4A-01 (anchor date: PDD moved 2026-11-26 -> 2026-12-10 (VOL-I 6.1 as amended by ADD-01 2.1, ADD-03 2.1); ADD-01 AppA/proposal-due-date prints 2026-11-12: CONFLICT with the amended PDD, not corrected (a person decides)), VOL-IV-F4A-02 (anchor date: PDD moved 2026-11-26 -> 2026-12-10 (VOL-I 6.1 as amended by ADD-01 2.1, ADD-03 2.1); ADD-01 AppA/proposal-due-date prints 2026-11-12: CONFLICT with the amended PDD, not corrected (a person decides))
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
- REWORK form-4e: requirement changed: VOL-V-29.3-01 (cited units: cited unit VOL-II T2-4/TP: Limit 1 -> 0.5 mg/l by ADD-03/7.1), VOL-V-31.1-02 (dependency: VOL-II T2-4/TP: Limit 1 -> 0.5 mg/l by ADD-03/7.1 (depends on it: REL-T24-UNAVAILABILITY (limit_applies, confirmed)))
- CONFIRMED (unchanged) form-4e: VOL-V-12.1-01: confirmed by ADD-03/Q15 (confirms; ADD-03:Q15); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-read at ADD-03. ADD-03 Q15 asks 'Following the capacity increase, will the Authority extend the construction period in Volume V Clause 12.1?' The Authority …'); text, cells, dates, status and consequence unchanged: work done stands
- MOVED form-4e: latest start 2026-11-22 -> 2026-12-06
- STATUS form-4e: timing OK -> OK; total float +1 -> 0 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK form-4f: requirement changed: ADD-03-Q17-01 (text, status, consequence, quote)
- MOVED form-4f: latest start 2026-11-22 -> 2026-12-06
- STATUS form-4f: timing OK -> INFEASIBLE by 1 WD; total float 0 -> -1 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK form-4g-review: requirement changed: ADD-02-F4G-01 (stale), ADD-02-F4G-02 (stale), ADD-02-F4G-03 (stale), ADD-02-F4G-04 (stale), ADD-02-F4G-05 (stale)
- CONFIRMED (unchanged) form-4g-review: ADD-02-F4G-06: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03 because op ADD-03/3.1(a) revoked ADD-02:7.2. The undertaking unit ADD-02:F4-G/T1/5 is still 'active' in the effective text after the proposed…'); ADD-02-F4G-07: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03 because op ADD-03/3.1(a) revoked ADD-02:7.2. The undertaking unit ADD-02:F4-G/T1/6 is still 'active' in the effective text after the proposed…'); text, cells, dates, status and consequence unchanged: work done stands
- MOVED form-4g-review: latest start 2026-11-16 -> 2026-11-30
- STATUS form-4g-review: timing OK -> OK; total float +17 -> +16 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK form-4g-sign: requirement changed: ADD-02-F4G-01 (stale), ADD-02-F4G-02 (stale), ADD-02-F4G-03 (stale), ADD-02-F4G-04 (stale), ADD-02-F4G-05 (stale)
- CONFIRMED (unchanged) form-4g-sign: ADD-02-F4G-06: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03 because op ADD-03/3.1(a) revoked ADD-02:7.2. The undertaking unit ADD-02:F4-G/T1/5 is still 'active' in the effective text after the proposed…'); ADD-02-F4G-07: reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'Re-made at ADD-03 because op ADD-03/3.1(a) revoked ADD-02:7.2. The undertaking unit ADD-02:F4-G/T1/6 is still 'active' in the effective text after the proposed…'); text, cells, dates, status and consequence unchanged: work done stands
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
- STATUS pcg-execution: timing OK -> OK; total float +3 -> +2 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED pcg-wording: latest start 2026-10-27 -> 2026-11-10
- STATUS pcg-wording: timing OK -> OK; total float +3 -> +2 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED poa: latest start 2026-11-10 -> 2026-11-24
- STATUS poa: timing OK -> OK; total float +8 -> +7 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED poa-resolutions: latest start 2026-11-03 -> 2026-11-17
- STATUS poa-resolutions: timing OK -> OK; total float +8 -> +7 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK references: requirement changed: VOL-I-8.5-01 (text, dates, status, quote, parameters)
- MOVED references: latest start 2026-11-04 -> 2026-11-18
- STATUS references: timing OK -> OK; total float +9 -> +8 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK seal-and-mark: requirement changed: VOL-I-6.1-01 (text, dates, status, quote)
- MOVED seal-and-mark: latest start 2026-11-25 -> 2026-12-09
- STATUS seal-and-mark: timing INFEASIBLE by 12 WD -> INFEASIBLE by 13 WD; total float -12 -> -13 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- MOVED spoc: latest start 2026-11-22 -> 2026-12-06
- STATUS spoc: timing OK -> OK; total float +21 -> +20 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REWORK technical-proposal: requirement changed: ADD-03-3.2-01 (text, status, consequence, quote), VOL-II-2.1-01 (text, status, quote, parameters), VOL-II-2.4-01 (dependency: VOL-II T2-4/TP: Limit 1 -> 0.5 mg/l by ADD-03/7.1 (depends on it: REL-T24-COMPLIANCE-MONITORING-STREAMS (limit_applies, confirmed))), VOL-II-3.1-01 (dependency: VOL-II T2-4/TP: Limit 1 -> 0.5 mg/l by ADD-03/7.1 (depends on it: REL-T24-PROCESS-DESIGN (limit_applies, confirmed))), VOL-II-4.3-02 (dependency: VOL-II T2-4/TP: Limit 1 -> 0.5 mg/l by ADD-03/7.1 (depends on it: REL-T24-COMPLIANCE-MONITORING-STREAMS (limit_applies, confirmed))), VOL-II-7.2-01 (dependency: VOL-II T2-4/TP: Limit 1 -> 0.5 mg/l by ADD-03/7.1 (depends on it: REL-T24-RELIABILITY-RUN (limit_applies, confirmed))), VOL-II-T2-4-TP (text, cells, status, quote, parameters)
- MOVED technical-proposal: latest start 2026-10-25 -> 2026-11-08
- STATUS technical-proposal: timing OK -> OK; total float +1 -> 0 WD; the planning date moved 2026-10-22 -> 2026-11-08, which by itself shifts every float by the Working Days between them
- REVIEW (confirmed dependency) deviations-review: VOL-V-29.3-01, VOL-V-31.1-02 reached from VOL-II:T2-4 via REL-T24-RAMP-UP-DEDUCTIONS, REL-T24-UNAVAILABILITY; dates unchanged
- REVIEW (proposed relationship) fin-model-build: VOL-IV-F4F-02 reached from ADD-03-Q17-01 via REL-AI-004; dates unchanged
- REVIEW (proposed relationship) fin-model-freeze: VOL-IV-F4F-02 reached from ADD-03-Q17-01 via REL-AI-004; dates unchanged
- REVIEW (proposed relationship) form-4a: ADD-01-AppA-01 reached from ADD-03-cover-para3-01 via REL-AI-002; dates unchanged
- REVIEW (proposed relationship) form-4a-prep: ADD-01-AppA-01, form-4a-prep reached from ADD-03-cover-para3-01, ADD-03:cover/para3 via REL-AI-002, REL-AI-006; dates unchanged
- REVIEW (confirmed dependency) form-4e: VOL-V-29.3-01, VOL-V-31.1-02 reached from VOL-II:T2-4 via REL-T24-RAMP-UP-DEDUCTIONS, REL-T24-UNAVAILABILITY; dates unchanged
- REVIEW (proposed relationship) form-4f: VOL-I-10.2-01, VOL-IV-F4F-01, VOL-IV-F4F-02 reached from ADD-03-Q17-01 via REL-AI-004; dates unchanged
- REVIEW (possible impact) form-4f: VOL-I-10.2-01 reached from ADD-03:Q17 via REL-AI-011; dates unchanged
- REVIEW (confirmed dependency) technical-proposal: VOL-II-2.4-01, VOL-II-3.1-01, VOL-II-4.3-02, VOL-II-7.2-01 reached from VOL-II:T2-4 via REL-T24-COMPLIANCE-MONITORING-STREAMS, REL-T24-PROCESS-DESIGN, REL-T24-RELIABILITY-RUN; dates unchanged
- REVIEW (proposed relationship) technical-proposal: VOL-II-7.2-01 reached from VOL-II:2.1, VOL-II:T2-4 via REL-AI-001, REL-AI-007, REL-T24-RELIABILITY-RUN; dates unchanged
- FEASIBILITY lcc-ratio: INFEASIBLE by 12 WD -> INFEASIBLE by 13 WD
- FEASIBILITY lcc-certificate: INFEASIBLE by 12 WD -> INFEASIBLE by 13 WD
- FEASIBILITY fin-model-build: OK -> INFEASIBLE by 1 WD
- FEASIBILITY fin-model-freeze: OK -> INFEASIBLE by 1 WD
… 7 more lines in [diff.md](diff.md)

## Next (a person)

- read the unresolved and escalated provisions first, then each item against its evidence (`../ai/ADD-03-run-host-20261015T140902Z-ab89-combined/proposals.yaml`, `../downstream/proposals.yaml`)
- nothing here is applied to the real curation: to take an item over, add the PDF to the pack (OPERATING_GUIDE §3 steps 1-2) and copy the reviewed files listed in `promotion.json`; then `pin`, `check-register`, `outputs` and decide with `accept` / `reject` as usual
