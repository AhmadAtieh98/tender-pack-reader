> **CANDIDATE: proposed by the AI workflow; not reviewed; nothing accepted**

# A1-A5 outputs (WORKING DRAFT)

Structural checks: **ok**. Release: **WORKING DRAFT (not releasable)**. Validated state: **ADD-02**; working state **ADD-03** (PARTIAL).
Structurally checked does not mean reviewed or approved by a person. Interpretations and ops are PROPOSED; image readings are PENDING the owner's review.

## What blocks a release (`outputs --strict`)

- **coverage**: ADD-03 is PARTIAL; unresolved provisions: ['ADD-03:cover/para3', 'ADD-03:1.2', 'ADD-03:3.1', 'ADD-03:3.2', 'ADD-03:3.3', 'ADD-03:3.4', 'ADD-03:4.1', 'ADD-03:4.2', 'ADD-03:4.3', 'ADD-03:4.4', 'ADD-03:5.1', 'ADD-03:5.2', 'ADD-03:6.2', 'ADD-03:7.1', 'ADD-03:7.2']
- **coverage**: 1 C46 finding(s): ADD-03/AppA/para1
- **stale**: 8 row(s) STALE at ADD-03: VOL-I-9.4-01, VOL-IV-F4C-04, VOL-IV-F4C-N1, VOL-IV-F4C-01, VOL-IV-F4C-02, VOL-IV-F4C-03, VOL-IV-F4C-05, VOL-V-29.3-01
- **approval**: 205 of 205 register rows not accepted by a person (a named decision bound to the current content): proposed 205
- **approval**: 43 of 43 amendment op(s) not accepted by a person (a named decision bound to the current content): proposed 43

| Output | Files |
|---|---|
| A1 compliance register (every row), status at each stage, review decisions | a1/a1.xlsx, a1/a1.csv, a1/a1.json |
| A2 reconciliation: changes, rows that move, answers to review, provision coverage, evidence chains | a2/a2.md, a2/*.csv, a2/*.json |
| A3 one-page disqualification sheet, with linked detail | a3/a3.pdf, a3/a3_detail.html, a3/a3.json |
| A5 programme, marshalling plan, documents, resources, infeasibility drivers, scenarios, replan deltas, Gantt | a5/*.csv, a5/*.json, a5/gantt.*, a5/scenarios/, a5/stages/ |
| A4 supporting record: tender clarification register (DRAFT questions, NOT SENT) | a4/clarification_register.md, .csv, .json |
| Engine results per stage | stages.json |
| Checks | checks.json |

## Checks

| Check | Result | Detail |
|---|---|---|
| E01 | pass | evidence build structurally OK and built from the current inputs |
| C16 | pass | 205 rows x 4 stages; every quote and consequence quote of a current interpretation found in the effective text; quoted text changed under STALE rows (reported as C11): ['VOL-V-29.3-01@ADD-03'] |
| C25 | pass | no unit changed without an op targeting it |
| C12 | pass | every row id in the ledger is present or withdrawn with a reason (0 withdrawn) |
| C47 | pass | every word a unit gains at a stage is printed in that stage's addendum |
| C13 | pass | 17 A3 items, each with an explicit quoted consequence |
| C40 | pass | every A5 activity cites an A1 row in force |
| C44 | pass | every deliverable needed by a row in force has activities or a justified exception |
| C45 | pass | every dependency and lead time is defined |
| C43 | pass | A3 fits one page; smallest text 8.06 pt (scale 0.948) |
| C20 ADD-01 | ok | 36 provisions; unresolved or unaccounted: none |
| C21-C27 ADD-01 | ok | 15 ops; invalid: none |
| C20 ADD-02 | ok | 40 provisions; unresolved or unaccounted: none |
| C21-C27 ADD-02 | ok | 22 ops; invalid: none |
| C20 ADD-03 | REPORTED | 35 provisions; unresolved or unaccounted: ['ADD-03:cover/para3', 'ADD-03:1.2', 'ADD-03:3.1', 'ADD-03:3.2', 'ADD-03:3.3', 'ADD-03:3.4', 'ADD-03:4.1', 'ADD-03:4.2', 'ADD-03:4.3', 'ADD-03:4.4', 'ADD-03:5.1', 'ADD-03:5.2', 'ADD-03:6.2', 'ADD-03:7.1', 'ADD-03:7.2'] |
| C21-C27 ADD-03 | ok | 6 ops; invalid: none |
| C11 | REPORTED | STALE rows: ['VOL-I-9.4-01@ADD-03', 'VOL-IV-F4C-04@ADD-03', 'VOL-IV-F4C-N1@ADD-03', 'VOL-IV-F4C-01@ADD-03', 'VOL-IV-F4C-02@ADD-03', 'VOL-IV-F4C-03@ADD-03', 'VOL-IV-F4C-05@ADD-03', 'VOL-V-29.3-01@ADD-03'] |
| C30 | ok | 46 date/period phrases in force; uncovered: none; explicitly not computed: none |
| C32 | ok | 5 date rule(s) with unstated counting conventions: every reading shown (A1 Dates), planning uses the configured policy |
| C28 ADD-01 | REPORTED | cover summary (5 claims) vs provisions: omitted 2, understated 1; report only, the summary is never applied (A2) |
| C28 ADD-02 | REPORTED | cover summary (7 claims) vs provisions: consequence not mentioned 2, omitted 3, understated 1; report only, the summary is never applied (A2) |
| C28 ADD-03 | REPORTED | cover summary (8 claims) vs provisions: contradicted 1, not found 4, omitted 1, unchecked 14, understated 2; report only, the summary is never applied (A2) |
| C46 | REPORTED | 1 gap(s): ADD-03/AppA/para1 [A1] |
