# A1-A5 outputs (WORKING DRAFT)

Structural checks: **ok**. Release: **WORKING DRAFT (not releasable)**. Validated state: **ADD-02**.
Structurally checked does not mean reviewed or approved by a person. Interpretations and ops are PROPOSED; image readings are PENDING the owner's review.

## What blocks a release (`outputs --strict`)

- **stale**: 3 row(s) STALE at ADD-02: VOL-I-8.3-01, VOL-I-3.4-01, VOL-I-6.7-01
- **approval**: image readings pending the owner's review: VOL-II-p3-r1, VOL-IV-p6-r1
- **approval**: 202 of 202 register rows not accepted by a person (a named decision bound to the current content): proposed 202
- **approval**: 37 of 37 amendment op(s) not accepted by a person (a named decision bound to the current content): proposed 37

| Output | Files |
|---|---|
| A1 compliance register (every row), status at each stage, review decisions | a1/a1.xlsx, a1/a1.csv, a1/a1.json |
| A2 reconciliation: changes, rows that move, answers to review, provision coverage, evidence chains | a2/a2.md, a2/*.csv, a2/*.json |
| A3 one-page disqualification sheet, with linked detail | a3/a3.pdf, a3/a3_detail.html, a3/a3.json |
| A5 programme, marshalling plan, documents, resources, infeasibility drivers, scenarios, replan deltas | a5/*.csv, a5/*.json, a5/scenarios/, a5/stages/ |
| Engine results per stage | stages.json |
| Checks | checks.json |

## Checks

| Check | Result | Detail |
|---|---|---|
| E01 | pass | evidence build structurally OK and built from the current inputs |
| C16 | pass | 202 rows x 3 stages; every quote and consequence quote of a current interpretation found in the effective text |
| C25 | pass | no unit changed without an op targeting it |
| C12 | pass | every row id in the ledger is present or withdrawn with a reason (0 withdrawn) |
| C47 | pass | every word a unit gains at a stage is printed in that stage's addendum |
| C13 | pass | 18 A3 items, each with an explicit quoted consequence |
| C40 | pass | every A5 activity cites an A1 row in force |
| C44 | pass | every deliverable needed by a row in force has activities or a justified exception |
| C45 | pass | every dependency and lead time is defined |
| C43 | pass | A3 fits one page; smallest text 7.91 pt (scale 0.931) |
| C20 ADD-01 | ok | 36 provisions; unresolved or unaccounted: none |
| C21-C27 ADD-01 | ok | 15 ops; invalid: none |
| C20 ADD-02 | ok | 40 provisions; unresolved or unaccounted: none |
| C21-C27 ADD-02 | ok | 22 ops; invalid: none |
| C11 | REPORTED | STALE rows: ['VOL-I-8.3-01@ADD-01', 'VOL-I-8.3-01@ADD-02', 'VOL-I-3.4-01@ADD-01', 'VOL-I-3.4-01@ADD-02', 'VOL-I-6.7-01@ADD-01', 'VOL-I-6.7-01@ADD-02'] |
| C30 | ok | 46 date/period phrases in force; uncovered: none; explicitly not computed: none |
| C32 | ok | 5 date rule(s) with unstated counting conventions: every reading shown (A1 Dates), planning uses the configured policy |
| C46 | ok | every new or amended obligation reaches A1, A3 where it carries a consequence, and A5 |
