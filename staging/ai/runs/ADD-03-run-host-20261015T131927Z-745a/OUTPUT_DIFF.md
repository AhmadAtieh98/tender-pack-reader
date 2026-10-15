# Output diff: ADD-02 baseline → ADD-03 candidate

**PARTIAL / NOT VALIDATED.** These are proposed effects, not a tender release. Eligible approvals are simulated. The baseline remains ADD-02. See [human decisions and blockers](README.md#review-required).

## Before / after navigation

| Output | Before: ADD-02 | After: ADD-03 candidate | Change |
|---|---|---|---|
| A1 register | [XLSX](candidate/out-before/a1/a1.xlsx) | [XLSX](candidate/out/a1/a1.xlsx) | 205 → 210 rows; five added, none deleted from the historical register. Use `Status after ADD-03`. |
| A2 changes | [Markdown](candidate/out-before/a2/a2.md) | [Markdown](candidate/out/a2/a2.md) | ADD-03 reconciliation, changed requirements, stale readings, answers to re-read and relationship impacts. |
| A3 bid-out consequences | [ADD-02 one-page PDF](candidate/out-before/a3/a3.pdf) | **[ADD-03 HTML](candidate/out/a3/a3_candidate.html)** | Primary candidate view is one continuous HTML page, with full content; not a verified one-A4-page print layout. |
| Clarification register (A4 supporting output) | [Before](candidate/out-before/a4/clarification_register.md) | [After](candidate/out/a4/clarification_register.md) | See open questions in the review packet and candidate issues; no new clarification items were promoted. A4 implementation history remains Git history. |
| A5 programme | [CSV](candidate/out-before/a5/programme.csv) | [Candidate CSV](candidate/out/a5/candidate/programme.csv) | 44 → 44 activities; 43 latest-start dates move. |
| A5 Gantt | [Before](candidate/out-before/a5/gantt.html) | [Candidate Gantt](candidate/out/a5/candidate/gantt.html) | Proposed schedule; interpretation and feasibility warnings retained. |
| A5 marshalling | [CSV](candidate/out-before/a5/marshalling.csv) | [Candidate CSV](candidate/out/a5/candidate/marshalling.csv) | 26 → 26 items; see field-level diff. |

GitHub shows HTML source; download/clone and open the HTML locally to render it. Its relative detail links and image assets are included. The original live Safari panel also renders these files.

## Material changes proposed by ADD-03

| Topic | Before | Proposed after / qualification |
|---|---|---|
| Proposal due date | 26 November 2026, 14:00 Riyadh | 10 December 2026, 14:00 Riyadh; collective period propagation and Form 4-A discrepancy remain under review. |
| Form 4-G | Required; ADD-02 §7.2 consequence | §7.2 cessation applied in candidate; complete grouped-form withdrawal blocked by software. Seven Form 4-G rows remain STALE. |
| Nominal capacity | 120,000 m³/day | 150,000 m³/day in Volume II §2.1; Table 2-6 target mapping and corresponding Volume I wording remain unresolved. Peak hourly flow is expressly unchanged. |
| Reference plant threshold | 80,000 m³/day | 100,000 m³/day; two plants / ten-year lookback retained. |
| Bid bond | SAR 4,500,000; 180 days | SAR 5,600,000; 210 days. Proposal validity remains 150 days from amended PDD. |
| Evaluation | Existing criteria | New §11.6 within-2% provision; comparison basis and discretionary criteria need human interpretation. |
| Total phosphorus | 1 mg/l | 0.5 mg/l on the same basis; downstream technical and contractual effects flagged. |
| Pricing / Q17 | Earlier project basis | Price the amended project; no inferred payment adjustment mechanism. Coverage limitation remains recorded. |

## A1 changes

Computed stage diff: **5 new, 1 out of force, 21 changed, 7 stale**. “Out” is a status transition, not deletion of a historical row. Categories may overlap. The CSV comparison also includes newly added stage columns; those are schema/history changes, not 210 new legal obligations.

New IDs: `ADD-03-cover-01`, `ADD-03-6.1-01`, `ADD-03-3.1-01`, `ADD-03-3.2-01`, `ADD-03-Q17-01`.

Out of force: `ADD-02-7.2-01`. Changed IDs: `VOL-I-6.1-01`, `VOL-I-5.2-01`, `VOL-I-6.3-01`, `VOL-I-6.4-01`, `VOL-I-6.4-02`, `VOL-I-7.1-01`, `VOL-I-8.3-01`, `VOL-I-8.5-01`, `VOL-IV-F4A-01`, `VOL-I-3.4-01`, `VOL-I-6.7-01`, `VOL-II-2.1-01`, `VOL-II-2.4-01`, `VOL-II-T2-4-TP`, `VOL-II-3.1-01`, `VOL-II-4.3-02`, `VOL-II-7.2-01`, `VOL-IV-F4A-02`, `VOL-V-12.1-01`, `VOL-V-29.3-01`, `VOL-V-31.1-02`.

[Complete field-by-field A1 diff](review/a1-field-diff.csv) · [generated semantic diff](review/diff.md) · [machine-readable semantic diff](review/diff.json).

## A3 changes

The proposed A3 loses `ADD-02-7.2-01` and changes five entries: `ADD-02-F4G-04`, `VOL-I-6.1-01`, `VOL-I-6.3-01`, `VOL-I-6.4-01`, and `VOL-I-8.5-01`. The full HTML retains unresolved risks and linked detail. The validated `candidate/out/a3/a3.pdf` remains the ADD-02 one-page output; it is not an updated ADD-03 release.

The ADD-03 one-page PDF fit failed (20 items, 12 unresolved; minimum scale 0.89). The original seven-page diagnostic PDF is retained as supporting evidence. Using HTML does not change or conceal this fit failure.

## A5 date and status changes

The semantic diff contains **127 change records**, not 127 distinct activities. Replanning moved from 22 October to 8 November 2026 as well as changing the due date. Float changes therefore cannot all be attributed to the deadline extension. Seventeen activities are marked REVIEW through relationships, five are blocked by unresolved rows, eight relationship chains are held back/incomplete, and one conflict remains in the candidate summary.

| Activity | Latest start before | Latest start candidate | Timing before | Timing candidate |
|---|---|---|---|---|
| assemble-envelope-a | 2026-11-24 | 2026-12-08 | INFEASIBLE by 12 WD | INFEASIBLE by 13 WD |
| assemble-envelope-b | 2026-11-24 | 2026-12-08 | OK | INFEASIBLE by 1 WD |
| bond-approval | 2026-11-05 | 2026-11-19 | OK | OK |
| bond-issue | 2026-11-19 | 2026-12-03 | OK | OK |
| clarifications | 2026-11-11 | 2026-11-25 | OK | OK |
| completion-certs | 2026-11-02 | 2026-11-16 | OK | OK |
| consortium-check | 2026-11-10 | 2026-11-24 | OK | OK |
| copies | 2026-11-25 | 2026-12-09 | INFEASIBLE by 12 WD | INFEASIBLE by 13 WD |
| deliver | 2026-11-26 | 2026-12-10 | INFEASIBLE by 12 WD | INFEASIBLE by 13 WD |
| deviations-review | 2026-11-08 | 2026-11-22 | OK | OK |
| fin-assumptions | 2026-11-22 | 2026-12-06 | OK | OK |
| fin-model-build | 2026-10-22 | 2026-11-05 | OK | INFEASIBLE by 1 WD |
| fin-model-freeze | 2026-11-12 | 2026-11-26 | OK | INFEASIBLE by 1 WD |
| fin-standing | 2026-11-19 | 2026-12-03 | OK | OK |
| fin-statements | 2026-11-12 | 2026-11-26 | OK | OK |
| form-4a | 2026-11-23 | 2026-12-07 | OK | OK |
| form-4a-prep | 2026-11-22 | 2026-12-06 | OK | OK |
| form-4b | 2026-11-23 | 2026-12-07 | OK | OK |
| form-4b-prep | 2026-11-18 | 2026-12-02 | OK | OK |
| form-4c-prep | 2026-11-17 | 2026-12-01 | OK | OK |
| form-4c-sign | 2026-11-19 | 2026-12-03 | OK | OK |
| form-4e | 2026-11-22 | 2026-12-06 | OK | OK |
| form-4f | 2026-11-22 | 2026-12-06 | OK | INFEASIBLE by 1 WD |
| form-4g-review | 2026-11-16 | 2026-11-30 | OK | OK |
| form-4g-sign | 2026-11-23 | 2026-12-07 | OK | OK |
| ground-dd | 2026-10-29 | 2026-11-12 | OK | OK |
| investment-licence | 2026-11-17 | 2026-12-01 | OK | OK |
| iso-copy | 2026-11-22 | 2026-12-06 | OK | OK |
| lcc-certificate | 2026-10-13 | 2026-10-27 | INFEASIBLE by 12 WD | INFEASIBLE by 13 WD |
| lcc-ratio | 2026-10-06 | 2026-10-20 | INFEASIBLE by 12 WD | INFEASIBLE by 13 WD |
| lender-terms | 2026-10-29 | 2026-11-12 | OK | OK |
| model-audit-opinion | 2026-11-15 | 2026-11-29 | OK | INFEASIBLE by 1 WD |
| model-audit-review | 2026-11-01 | 2026-11-15 | OK | OK |
| model-auditor-appoint | 2026-10-25 | 2026-11-08 | OK | OK |
| om-evidence | 2026-11-10 | 2026-11-24 | OK | OK |
| pcg-execution | 2026-11-10 | 2026-11-24 | OK | OK |
| pcg-wording | 2026-10-27 | 2026-11-10 | OK | OK |
| poa | 2026-11-10 | 2026-11-24 | OK | OK |
| poa-resolutions | 2026-11-03 | 2026-11-17 | OK | OK |
| references | 2026-11-04 | 2026-11-18 | OK | OK |
| seal-and-mark | 2026-11-25 | 2026-12-09 | INFEASIBLE by 12 WD | INFEASIBLE by 13 WD |
| spoc | 2026-11-22 | 2026-12-06 | OK | OK |
| technical-proposal | 2026-10-25 | 2026-11-08 | OK | OK |

[Full programme field diff](review/a5-programme-field-diff.csv) · [Full marshalling field diff](review/a5-marshalling-field-diff.csv).

## What was held back

Five provisions remain unresolved at controller level; fourteen downstream tasks have responses that cannot be promoted. Seven stale Form 4-G rows were not demo-approved. The run produced reviewable outputs but did not produce a clean tender release. See [review-required actions](README.md#review-required) and [complete review packet](review/index.md).
