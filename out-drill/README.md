# A1-A5 outputs (WORKING DRAFT)

Structural checks: **ok**. Release: **WORKING DRAFT (not releasable)**. Validated state: **ADD-02**; working state **ADD-03** (PARTIAL).
Structurally checked does not mean reviewed or approved by a person. Interpretations and ops are PROPOSED; image readings PENDING HUMAN REVIEW: VOL-II-p3-r1, VOL-IV-p6-r1.

## What blocks a release (`outputs --strict`)

- **coverage**: ADD-03 is PARTIAL; unresolved provisions: ['ADD-03:6.1', 'ADD-03:7.1', 'ADD-03:Q15', 'ADD-03:Q16']
- **coverage**: 1 C46 finding(s): ADD-03/cover/para3
- **stale**: 13 row(s) STALE at ADD-03: VOL-I-6.1-01, VOL-I-5.2-01, VOL-I-6.3-01, VOL-I-7.1-01, VOL-I-8.3-01, VOL-I-8.5-01, VOL-V-31.3-01, VOL-I-3.4-01, VOL-I-6.7-01, VOL-II-T2-4-TP, VOL-V-29.3-01, VOL-V-31.3-02 ...
- **approval**: image readings pending the owner's review: VOL-II-p3-r1, VOL-IV-p6-r1
- **approval**: 205 of 205 register rows not accepted by a person (a named decision bound to the current content): proposed 205
- **approval**: 44 of 44 amendment op(s) not accepted by a person (a named decision bound to the current content): proposed 44

| Output | Files |
|---|---|
| A1 compliance register (every row), status at each stage, review decisions | a1/a1.xlsx, a1/a1.csv, a1/a1.json |
| A2 reconciliation: changes, rows that move, answers to review, provision coverage, evidence chains | a2/a2.md, a2/*.csv, a2/*.json |
| A3 one-page disqualification sheet, with linked detail | a3/a3.pdf, a3/a3_detail.html, a3/a3.json |
| A5 programme, marshalling plan, documents, resources, infeasibility drivers, scenarios, replan deltas, Gantt | a5/*.csv, a5/*.json, a5/gantt.*, a5/scenarios/, a5/stages/ |
| A4 work log: the session logs (worklog/<date>_session-NN_*.md); the work log index (worklog/README.md); the note of every place the system was wrong (worklog/ERROR_INDEX.md); the prompts and model calls (worklog/model_calls/); the subagent briefs (worklog/subagent_briefs/); and the commit history (`git log`) | worklog/ at the repository root (not under out/); `git log` |
| Supporting record: tender clarification register (DRAFT questions, NOT SENT; not the A4 work log) | a4/clarification_register.md, .csv, .json |
| Engine results per stage | stages.json |
| Checks | checks.json |
| A3 and A5 CANDIDATE: ADD-03 as proposed, NOT VALIDATED (the rows and dates it would move, blockers, conditional scenarios; the validated A3 and A5 above are unchanged) | a3/a3_candidate.pdf, .md, .html, .json; a5/candidate/ |

## Checks

| Check | Result | Detail |
|---|---|---|
| E01 | pass | evidence build structurally OK and built from the current inputs |
| C16 | pass | 205 rows x 4 stages; every quote and consequence quote of a current interpretation found in the effective text; quoted text changed under STALE rows (reported as C11): ['VOL-I-6.1-01@ADD-03', 'VOL-II-T2-4-TP@ADD-03', 'VOL-V-31.3-01@ADD-03'] |
| C25 | pass | no unit changed without an op targeting it |
| C12 | pass | every row id in the ledger is present or withdrawn with a reason (0 withdrawn) |
| C47 | pass | every word a unit gains at a stage is printed in that stage's addendum |
| C13 | pass | 16 (+ VOL-IV-F4C-N1, which restates VOL-I-9.4-01) explicit bid-out triggers + 1 below the score threshold = 18 A3 rows, each row with an explicit quoted consequence |
| C40 | pass | every A5 activity cites an A1 row in force |
| C44 | pass | every deliverable needed by a row in force has activities or a justified exception |
| C45 | pass | every dependency and lead time is defined |
| C43 | pass | A3 fits one page; smallest text 8.35 pt (scale 0.983) |
| C52 | pass | 0 confirmed translation(s) of approved readings; none called 'not reviewed' in the outputs |
| C20 ADD-01 | ok | 36 provisions; unresolved or unaccounted: none |
| C21-C27 ADD-01 | ok | 15 ops; invalid: none |
| C20 ADD-02 | ok | 40 provisions; unresolved or unaccounted: none |
| C21-C27 ADD-02 | ok | 23 ops; invalid: none |
| C20 ADD-03 | REPORTED | 12 provisions; unresolved or unaccounted: ['ADD-03:6.1', 'ADD-03:7.1', 'ADD-03:Q15', 'ADD-03:Q16'] |
| C21-C27 ADD-03 | REPORTED | 6 ops; invalid: ["ADD-03/7.1 (C23: 'seventy-two (72) hours' occurs 0 time(s) in VOL-II:4.4)"] |
| C11 | REPORTED | STALE rows: ['VOL-I-6.1-01@ADD-03', 'VOL-I-5.2-01@ADD-03', 'VOL-I-6.3-01@ADD-03', 'VOL-I-7.1-01@ADD-03', 'VOL-I-8.3-01@ADD-03', 'VOL-I-8.5-01@ADD-03', 'VOL-V-31.3-01@ADD-03', 'VOL-I-3.4-01@ADD-03', 'VOL-I-6.7-01@ADD-03', 'VOL-II-T2-4-TP@ADD-03', 'VOL-V-29.3-01@ADD-03', 'VOL-V-31.3-02@ADD-03', 'VOL-V-31.3-03@ADD-03'] |
| C30 | ok | 46 date/period phrases in force; uncovered: none; explicitly not computed: none |
| C32 | ok | 5 date rule(s) with unstated counting conventions: every reading shown (A1 Dates), planning uses the configured policy |
| C28 ADD-01 | REPORTED | cover summary (5 claims) vs provisions: omitted 2; report only, the summary is never applied (A2) |
| C28 ADD-02 | REPORTED | cover summary (7 claims) vs provisions: consequence not mentioned 2, omitted 3, understated 1; report only, the summary is never applied (A2) |
| C28 ADD-03 | REPORTED | cover summary (3 claims) vs provisions: claimed, not applied 1, unchecked 3; report only, the summary is never applied (A2) |
| C46 | REPORTED | 1 gap(s): ADD-03/cover/para3 [A1] |
| C48 | ok | 200 A1 rows in force at ADD-02: 160 discharged by an activity, 30 reviewed for deviations (the VOL-V volume check), 10 excepted with a reason (listed in a5/requirements_not_carried.csv); not carried: none. Of these, 18 A3 (bid-out) rows: 16 carried, 2 excepted with a reason (the rows the A3 page lists: explicit plus the score row: ADD-02-7.2-01, VOL-I-1.4-01, VOL-I-10.5-01, VOL-I-11.3-01, VOL-I-11.5-01, VOL-I-4.2-01, VOL-I-5.4-01, VOL-I-6.1-01, VOL-I-6.2-02, VOL-I-8.1-01, VOL-I-8.2-01, VOL-I-8.5-01, VOL-I-8.6-01, VOL-I-9.3-01, VOL-I-9.4-01, VOL-I-9.6-01, VOL-IV-F4C-04, VOL-IV-F4C-N1) |
