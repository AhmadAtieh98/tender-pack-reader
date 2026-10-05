> **CANDIDATE: proposed by the AI workflow; not reviewed; nothing accepted**

# A1-A5 outputs (WORKING DRAFT)

Structural checks: **ok**. Release: **WORKING DRAFT (not releasable)**. Validated state: **ADD-02**; working state **ADD-03** (PARTIAL).
Structurally checked does not mean reviewed or approved by a person. Interpretations and ops are PROPOSED; image readings approved by a named reviewer: VOL-II-p3-r1, VOL-IV-p6-r1 (see build/coverage.md); image readings PENDING HUMAN REVIEW: ADD-03-p4-r1.

## What blocks a release (`outputs --strict`)

- **coverage**: ADD-03 is PARTIAL; unresolved provisions: ['ADD-03:cover/para3', 'ADD-03:2.1', 'ADD-03:3.3', 'ADD-03:3.3(b)', 'ADD-03:5.1', 'ADD-03:5.2', 'ADD-03:Q18', 'ADD-03:7.2', 'ADD-03:7.3', 'ADD-03:7.4', 'ADD-03:p4-image/table-header', 'ADD-03:p4-image/row-a', 'ADD-03:p4-image/row-b', 'ADD-03:p4-image/note1', 'ADD-03:p4-image/note2', 'ADD-03:p4-image/note3', 'ADD-03:p4-image/stamp', 'ADD-03:AppB/para1', 'ADD-03:T5-1/a', 'ADD-03:T5-1/b', 'ADD-03:T5-1/note(1)', 'ADD-03:T5-1/note(2)', 'ADD-03:T5-1/note(3)']
- **stale**: 2 row(s) STALE at ADD-03: VOL-V-29.2-01, VOL-IV-F4F-02
- **approval**: image readings pending the owner's review: ADD-03-p4-r1
- **approval**: 207 of 207 register rows not accepted by a person (a named decision bound to the current content): proposed 207
- **approval**: 49 of 49 amendment op(s) not accepted by a person (a named decision bound to the current content): proposed 49

| Output | Files |
|---|---|
| A1 compliance register (every row), status at each stage, review decisions | a1/a1.xlsx, a1/a1.csv, a1/a1.json |
| A2 reconciliation: changes, rows that move, answers to review, provision coverage, evidence chains | a2/a2.md, a2/*.csv, a2/*.json |
| A3 one-page disqualification sheet, with linked detail | a3/a3.pdf, a3/a3_detail.html, a3/a3.json |
| A5 programme, marshalling plan, documents, resources, infeasibility drivers, scenarios, replan deltas, Gantt | a5/*.csv, a5/*.json, a5/gantt.*, a5/scenarios/, a5/stages/ |
| A4 supporting record: tender clarification register (DRAFT questions, NOT SENT) | a4/clarification_register.md, .csv, .json |
| Engine results per stage | stages.json |
| Checks | checks.json |
| A3 and A5 CANDIDATE: ADD-03 as proposed, NOT VALIDATED (the rows and dates it would move, blockers, conditional scenarios; the validated A3 and A5 above are unchanged) | a3/a3_candidate.pdf, .md, .html, .json; a5/candidate/ |

## Checks

| Check | Result | Detail |
|---|---|---|
| E01 | pass | evidence build structurally OK and built from the current inputs |
| C16 | pass | 207 rows x 4 stages; every quote and consequence quote of a current interpretation found in the effective text |
| C25 | pass | no unit changed without an op targeting it |
| C12 | pass | every row id in the ledger is present or withdrawn with a reason (0 withdrawn) |
| C47 | pass | every word a unit gains at a stage is printed in that stage's addendum |
| C13 | pass | 17 A3 items, each with an explicit quoted consequence |
| C40 | pass | every A5 activity cites an A1 row in force |
| C44 | pass | every deliverable needed by a row in force has activities or a justified exception |
| C45 | pass | every dependency and lead time is defined |
| C43 | pass | A3 fits one page; smallest text 8.15 pt (scale 0.959) |
| C20 ADD-01 | ok | 36 provisions; unresolved or unaccounted: none |
| C21-C27 ADD-01 | ok | 15 ops; invalid: none |
| C20 ADD-02 | ok | 40 provisions; unresolved or unaccounted: none |
| C21-C27 ADD-02 | ok | 22 ops; invalid: none |
| C20 ADD-03 | REPORTED | 54 provisions; unresolved or unaccounted: ['ADD-03:cover/para3', 'ADD-03:2.1', 'ADD-03:3.3', 'ADD-03:3.3(b)', 'ADD-03:5.1', 'ADD-03:5.2', 'ADD-03:Q18', 'ADD-03:7.2', 'ADD-03:7.3', 'ADD-03:7.4', 'ADD-03:p4-image/table-header', 'ADD-03:p4-image/row-a', 'ADD-03:p4-image/row-b', 'ADD-03:p4-image/note1', 'ADD-03:p4-image/note2', 'ADD-03:p4-image/note3', 'ADD-03:p4-image/stamp', 'ADD-03:AppB/para1', 'ADD-03:T5-1/a', 'ADD-03:T5-1/b', 'ADD-03:T5-1/note(1)', 'ADD-03:T5-1/note(2)', 'ADD-03:T5-1/note(3)'] |
| C21-C27 ADD-03 | ok | 12 ops; invalid: none |
| C11 | REPORTED | STALE rows: ['VOL-V-29.2-01@ADD-03', 'VOL-IV-F4F-02@ADD-03'] |
| C30 | ok | 46 date/period phrases in force; uncovered: none; explicitly not computed: none |
| C32 | ok | 5 date rule(s) with unstated counting conventions: every reading shown (A1 Dates), planning uses the configured policy |
| C28 ADD-01 | REPORTED | cover summary (5 claims) vs provisions: omitted 2, understated 1; report only, the summary is never applied (A2) |
| C28 ADD-02 | REPORTED | cover summary (7 claims) vs provisions: consequence not mentioned 2, omitted 3, understated 1; report only, the summary is never applied (A2) |
| C28 ADD-03 | REPORTED | cover summary (0 claims) vs provisions: no summary 1; report only, the summary is never applied (A2) |
| C46 | ok | every new or amended obligation reaches A1, A3 where it carries a consequence, and A5 |
