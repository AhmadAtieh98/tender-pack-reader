> **CANDIDATE: proposed by the AI workflow; not reviewed; nothing accepted**

# A1-A5 outputs (WORKING DRAFT)

Structural checks: **ok**. Release: **WORKING DRAFT (not releasable)**. Validated state: **ADD-02**; working state **ADD-03** (PARTIAL).
Structurally checked does not mean reviewed or approved by a person. Interpretations and ops are PROPOSED; image readings approved by a named reviewer: VOL-II-p3-r1, VOL-IV-p6-r1 (see build/coverage.md); image readings PENDING HUMAN REVIEW: ADD-03-p4-r1.

## What blocks a release (`outputs --strict`)

- **coverage**: ADD-03 is PARTIAL; unresolved provisions: ['ADD-03:Q17']
- **coverage**: 11 C46 finding(s): ADD-03/6.1, ADD-03/8.1, ADD-03/8.2, ADD-03/8.3, ADD-03/8.4, ADD-03/cover/para3
- **coverage**: 1 disposition finding(s): VOL-V
- **stale**: 9 row(s) STALE at ADD-03: VOL-I-11.3-01, VOL-I-8.4-01, VOL-II-5.2-01, VOL-II-5.3-01, VOL-IV-F4D-01, VOL-IV-F4D-02, VOL-IV-F4D-03, VOL-IV-F4D-04, VOL-IV-F4D-05
- **approval**: image readings pending the owner's review: ADD-03-p4-r1
- **approval**: 208 of 208 register rows not accepted by a person (a named decision bound to the current content): proposed 208
- **approval**: 62 of 62 amendment op(s) not accepted by a person (a named decision bound to the current content): proposed 62

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
| C16 | pass | 208 rows x 4 stages; every quote and consequence quote of a current interpretation found in the effective text; quoted text changed under STALE rows (reported as C11): ['VOL-I-11.3-01@ADD-03', 'VOL-I-8.4-01@ADD-03', 'VOL-II-5.2-01@ADD-03', 'VOL-II-5.3-01@ADD-03'] |
| C25 | pass | no unit changed without an op targeting it |
| C12 | pass | every row id in the ledger is present or withdrawn with a reason (0 withdrawn) |
| C47 | pass | every word a unit gains at a stage is printed in that stage's addendum |
| C13 | pass | 17 A3 items, each with an explicit quoted consequence |
| C40 | pass | every A5 activity cites an A1 row in force |
| C44 | pass | every deliverable needed by a row in force has activities or a justified exception |
| C45 | pass | every dependency and lead time is defined |
| C43 | pass | A3 fits one page; smallest text 8.05 pt (scale 0.947) |
| C20 ADD-01 | ok | 36 provisions; unresolved or unaccounted: none |
| C21-C27 ADD-01 | ok | 15 ops; invalid: none |
| C20 ADD-02 | ok | 40 provisions; unresolved or unaccounted: none |
| C21-C27 ADD-02 | ok | 22 ops; invalid: none |
| C20 ADD-03 | REPORTED | 70 provisions; unresolved or unaccounted: ['ADD-03:Q17'] |
| C21-C27 ADD-03 | ok | 25 ops; invalid: none |
| C11 | REPORTED | STALE rows: ['VOL-I-11.3-01@ADD-03', 'VOL-I-8.4-01@ADD-03', 'VOL-II-5.2-01@ADD-03', 'VOL-II-5.3-01@ADD-03', 'VOL-IV-F4D-01@ADD-03', 'VOL-IV-F4D-02@ADD-03', 'VOL-IV-F4D-03@ADD-03', 'VOL-IV-F4D-04@ADD-03', 'VOL-IV-F4D-05@ADD-03'] |
| C30 | ok | 46 date/period phrases in force; uncovered: none; explicitly not computed: none |
| C32 | ok | 5 date rule(s) with unstated counting conventions: every reading shown (A1 Dates), planning uses the configured policy |
| C28 ADD-01 | REPORTED | cover summary (5 claims) vs provisions: omitted 2, understated 1; report only, the summary is never applied (A2) |
| C28 ADD-02 | REPORTED | cover summary (7 claims) vs provisions: consequence not mentioned 2, omitted 3, understated 1; report only, the summary is never applied (A2) |
| C28 ADD-03 | REPORTED | cover summary (8 claims) vs provisions: consequence not mentioned 1, contradicted 1, omitted 2, unchecked 1; report only, the summary is never applied (A2) |
| C46 | REPORTED | 11 gap(s): ADD-03/cover/para3 [A3]; ADD-03/6.1 [A1]; ADD-03/8.1 [A1]; ADD-03/8.1 [A1]; ADD-03/8.1 [A3]; ADD-03/8.2 [A1]; ADD-03/8.2 [A3]; ADD-03/8.3 [A1] |
