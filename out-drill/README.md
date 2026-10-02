# A1-A5 outputs (WORKING DRAFT)

Structural checks: **ok**. Release: **WORKING DRAFT (not releasable)**. Validated state: **ADD-02**; working state **ADD-03** (PARTIAL).
Structurally checked does not mean reviewed or approved by a person. Interpretations and ops are PROPOSED; image readings are PENDING the owner's review.

## What blocks a release (`outputs --strict`)

- **coverage**: ADD-03 is PARTIAL; unresolved provisions: ['ADD-03:6.1', 'ADD-03:7.1', 'ADD-03:Q15', 'ADD-03:Q16']
- **stale**: 13 row(s) STALE at ADD-03: VOL-I-6.1-01, VOL-I-5.2-01, VOL-I-6.3-01, VOL-I-7.1-01, VOL-I-8.3-01, VOL-I-8.5-01, VOL-V-31.3-01, VOL-I-3.4-01, VOL-I-6.7-01, VOL-II-T2-4-TP, VOL-V-29.3-01, VOL-V-31.3-02 ...
- **approval**: image readings pending the owner's review: VOL-II-p3-r1, VOL-IV-p6-r1
- **approval**: 202 of 202 register rows not accepted by a person
- **approval**: 43 amendment op(s) not accepted by a person

| Output | Files |
|---|---|
| A1 register slice, status at each stage | a1/a1.xlsx, a1/a1.csv, a1/a1.json |
| A2 reconciliation: changes, rows that move, answers to review, provision coverage, evidence chains | a2/a2.md, a2/*.csv, a2/*.json |
| A3 one-page draft | a3/a3.pdf, a3/a3.json |
| A5 programme, marshalling plan, replan deltas | a5/programme.*, a5/marshalling.*, a5/replan_deltas.*, a5/stages/*.json |
| Engine results per stage | stages.json |
| Checks | checks.json |

## Checks

| Check | Result | Detail |
|---|---|---|
| E01 | pass | evidence build structurally OK and built from the current inputs |
| C16 | pass | 202 rows x 4 stages; every quote and consequence quote of a current interpretation found in the effective text; quoted text changed under STALE rows (reported as C11): ['VOL-I-6.1-01@ADD-03', 'VOL-II-T2-4-TP@ADD-03', 'VOL-V-31.3-01@ADD-03'] |
| C25 | pass | no unit changed without an op targeting it |
| C13 | pass | 18 A3 items, each with an explicit quoted consequence |
| C40 | pass | every A5 activity cites an A1 row in force |
| C44 | pass | every deliverable needed by a row in force has activities or a justified exception |
| C45 | pass | every dependency and lead time is defined |
| C43 | pass | A3 fits one page; smallest text 7.87 pt (scale 0.925) |
| C20 ADD-01 | ok | 36 provisions; unresolved or unaccounted: none |
| C21-C27 ADD-01 | ok | 15 ops; invalid: none |
| C20 ADD-02 | ok | 40 provisions; unresolved or unaccounted: none |
| C21-C27 ADD-02 | ok | 22 ops; invalid: none |
| C20 ADD-03 | REPORTED | 12 provisions; unresolved or unaccounted: ['ADD-03:6.1', 'ADD-03:7.1', 'ADD-03:Q15', 'ADD-03:Q16'] |
| C21-C27 ADD-03 | REPORTED | 6 ops; invalid: ["ADD-03/7.1 (C23: 'seventy-two (72) hours' occurs 0 time(s) in VOL-II:4.4)"] |
| C11 | REPORTED | STALE rows: ['VOL-I-6.1-01@ADD-03', 'VOL-I-5.2-01@ADD-03', 'VOL-I-6.3-01@ADD-03', 'VOL-I-7.1-01@ADD-03', 'VOL-I-8.3-01@ADD-01', 'VOL-I-8.3-01@ADD-02', 'VOL-I-8.3-01@ADD-03', 'VOL-I-8.5-01@ADD-03', 'VOL-V-31.3-01@ADD-03', 'VOL-I-3.4-01@ADD-01', 'VOL-I-3.4-01@ADD-02', 'VOL-I-3.4-01@ADD-03', 'VOL-I-6.7-01@ADD-01', 'VOL-I-6.7-01@ADD-02', 'VOL-I-6.7-01@ADD-03', 'VOL-II-T2-4-TP@ADD-03', 'VOL-V-29.3-01@ADD-03', 'VOL-V-31.3-02@ADD-03', 'VOL-V-31.3-03@ADD-03'] |
