# Stage 2 outputs (first connected version, DRAFT)

Status: **ok**. Validated state: **ADD-02**; working state **ADD-03** (PARTIAL).
Interpretations and ops are PROPOSED (not reviewed); image readings are PENDING the owner's review.

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
| C16 | pass | 26 rows x 4 stages; every quote and consequence quote of a current interpretation found in the effective text; quoted text changed under STALE rows (reported as C11): ['VOL-I-6.1-01@ADD-03', 'VOL-V-31.3-01@ADD-03'] |
| C25 | pass | no unit changed without an op targeting it |
| C13 | pass | 9 A3 items, each with an explicit quoted consequence |
| C40 | pass | every A5 activity cites an A1 row in force |
| C43 | pass | A3 fits one page at scale 0.937 |
| C20 ADD-01 | ok | 36 provisions; unresolved or unaccounted: none |
| C21-C27 ADD-01 | ok | 11 ops; invalid: none |
| C20 ADD-02 | ok | 40 provisions; unresolved or unaccounted: none |
| C21-C27 ADD-02 | ok | 14 ops; invalid: none |
| C20 ADD-03 | REPORTED | 12 provisions; unresolved or unaccounted: ['ADD-03:6.1', 'ADD-03:7.1', 'ADD-03:Q15', 'ADD-03:Q16'] |
| C21-C27 ADD-03 | REPORTED | 5 ops; invalid: ["ADD-03/7.1 (C23: 'seventy-two (72) hours' occurs 0 time(s) in VOL-II:4.4)"] |
| C11 | REPORTED | STALE rows: ['VOL-I-6.1-01@ADD-03', 'VOL-I-5.2-01@ADD-03', 'VOL-I-6.3-01@ADD-03', 'VOL-I-7.1-01@ADD-03', 'VOL-I-8.3-01@ADD-01', 'VOL-I-8.3-01@ADD-02', 'VOL-I-8.3-01@ADD-03', 'VOL-I-8.5-01@ADD-03', 'VOL-V-31.3-01@ADD-03'] |
