# A1-A5 outputs (WORKING DRAFT)

Structural checks: **structural_failure**. Release: **WORKING DRAFT (not releasable)**. Validated state: **ADD-03**.
Structurally checked does not mean reviewed or approved by a person. Interpretations and ops are PROPOSED; image readings are PENDING the owner's review.

## What blocks a release (`outputs --strict`)

- **coverage**: 1 C30 finding(s): ADD-01:AppA/proposal-due-date
- **stale**: 28 row(s) STALE at ADD-03: VOL-I-6.3-01, VOL-I-6.4-02, VOL-I-7.1-01, VOL-I-8.3-01, VOL-IV-F4A-01, VOL-I-9.4-01, ADD-02-7.2-01, VOL-I-3.4-01, VOL-I-5.5-01, VOL-I-6.5-02, VOL-I-6.7-01, VOL-I-8.7-01 ...
- **approval**: image readings pending the owner's review: VOL-II-p3-r1, VOL-IV-p6-r1
- **approval**: 206 of 206 register rows not accepted by a person (a named decision bound to the current content): proposed 206
- **approval**: 65 of 65 amendment op(s) not accepted by a person (a named decision bound to the current content): proposed 65

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
| C16 | pass | 206 rows x 4 stages; every quote and consequence quote of a current interpretation found in the effective text; quoted text changed under STALE rows (reported as C11): ['VOL-IV-F4A-01@ADD-03'] |
| C25 | pass | no unit changed without an op targeting it |
| C12 | pass | every row id in the ledger is present or withdrawn with a reason (0 withdrawn) |
| C47 | pass | every word a unit gains at a stage is printed in that stage's addendum |
| C13 | pass | 20 A3 items, each with an explicit quoted consequence |
| C40 | pass | every A5 activity cites an A1 row in force |
| C44 | pass | every deliverable needed by a row in force has activities or a justified exception |
| C45 | pass | every dependency and lead time is defined |
| C43 | FAIL | A3 does not fit one page at a readable size: A3 content does not fit on one A4 page at scale >= 0.9 (21 items, 12 unresolved); shorten or prioritise it |
| C20 ADD-01 | ok | 36 provisions; unresolved or unaccounted: none |
| C21-C27 ADD-01 | ok | 15 ops; invalid: none |
| C20 ADD-02 | ok | 40 provisions; unresolved or unaccounted: none |
| C21-C27 ADD-02 | ok | 22 ops; invalid: none |
| C20 ADD-03 | ok | 29 provisions; unresolved or unaccounted: none |
| C21-C27 ADD-03 | ok | 28 ops; invalid: none |
| C11 | REPORTED | STALE rows: ['VOL-I-6.3-01@ADD-03', 'VOL-I-6.4-02@ADD-03', 'VOL-I-7.1-01@ADD-03', 'VOL-I-8.3-01@ADD-01', 'VOL-I-8.3-01@ADD-02', 'VOL-I-8.3-01@ADD-03', 'VOL-IV-F4A-01@ADD-03', 'VOL-I-9.4-01@ADD-03', 'ADD-02-7.2-01@ADD-03', 'ADD-01-AppA-01@ADD-01', 'ADD-01-AppA-01@ADD-02', 'VOL-I-3.4-01@ADD-01', 'VOL-I-3.4-01@ADD-02', 'VOL-I-3.4-01@ADD-03', 'VOL-I-5.5-01@ADD-03', 'VOL-I-6.5-02@ADD-03', 'VOL-I-6.7-01@ADD-01', 'VOL-I-6.7-01@ADD-02', 'VOL-I-6.7-01@ADD-03', 'VOL-I-8.7-01@ADD-03', 'VOL-I-9.1-01@ADD-03', 'VOL-I-9.1h-01@ADD-03', 'VOL-I-9.2-01@ADD-03', 'VOL-I-9.5-01@ADD-03', 'VOL-I-9.6-01@ADD-03', 'VOL-I-9.7-01@ADD-03', 'VOL-I-10.5-01@ADD-03', 'VOL-I-10.5-02@ADD-03', 'VOL-I-10.6-01@ADD-03', 'VOL-I-12.2-01@ADD-03', 'VOL-II-5.2-01@ADD-03', 'VOL-II-6.1-01@ADD-03', 'VOL-II-7.2-01@ADD-03', 'VOL-IV-F4A-02@ADD-03', 'VOL-V-29.3-01@ADD-03', 'VOL-V-29.4-01@ADD-03'] |
| C30 | REPORTED | 48 date/period phrases in force; uncovered: ["ADD-01:AppA/proposal-due-date '10 December 2026'"]; explicitly not computed: none |
| C32 | ok | 5 date rule(s) with unstated counting conventions: every reading shown (A1 Dates), planning uses the configured policy |
| C46 | ok | every new or amended obligation reaches A1, A3 where it carries a consequence, and A5 |
