> **CANDIDATE: proposed by the AI workflow; not reviewed; nothing accepted**

# A5 CANDIDATE — ADD-03 [CANDIDATE — NOT VALIDATED]

> **CANDIDATE — NOT VALIDATED.** The validated A5 is `../README.md` (ADD-02, planning date 2026-10-22); nothing there is changed. This folder replans the programme at the working stage (planning date 2026-11-17, its issue date) with every op that is valid there standing as a proposal. Earliest dates move with the planning date for every activity (EARLY DATES); the latest dates move only where a pack date or a requirement changes.

## What may be changing

ADD-03 is PARTIAL: 8 of 57 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 15 op(s) that are valid there stood (each still a proposal: review proposed 15), A3 would gain 0 row(s) (none), lose 0 (none) and change 0 (none); A5, replanned at ADD-03's issue date (2026-11-17), would move the latest dates of 0 activities (none), add 1 (core-inspection-request) and remove 0 (none), and marks 7 REVIEW through relationships. Not settled: 4 activities blocked by an unresolved row (technical-proposal, core-inspection-request, deviations-review, form-4e), 1 STALE row(s), 2 obligation(s) reaching no output (C46), 0 relationship chain(s) blocked or incomplete, 5 conflict(s); documents not supplied: the Environmental Permit issued for the site, Geotechnical Baseline Report (Revision C), Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions) and 7 more; conditional or effective-dated: ADD-03:T42-1/4 (conditional obligation); ADD-03:T42-1/5 (conditional obligation); ADD-03:T42-1/note(4) (conditional obligation). Clarification route: the clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person. Nothing here is validated, accepted or applied to the real state.

## Computed deadlines and the Working Days left (PROPOSED; nothing typed)

- Working Days left from the issue date (2026-11-17) to the PDD (2026-11-26): 7 (the issue date not counted, the PDD counted; Working Days per VOL-I 2.4 (weekend [4, 5] as date.weekday numbers; holidays none declared))
- `ADD-03:4.3` p2: “three (3) Working Days before the Proposal Due Date” -> **2026-11-23** (computed: calc deadline, anchor PDD = 2026-11-26, rule working-days-before, fingerprint 60b780e98a3a; PROPOSED, not validated)
- `ADD-03:4.3` p2: “within three (3) Working Days of the date of this Addendum” -> **AMBIGUOUS: 2026-11-22 (event_day_excluded); 2026-11-19 (event_day_counted)** (computed: calc deadline, anchor ADD-03-issue = 2026-11-17, rule none, fingerprint 4981e0314953; PROPOSED, not validated); ESCALATED: the counting rules do not settle it; not computed: no rule in the counting registry (config/formulas.yaml `counting`) for Working Days counted after a date (VOL-I 2.4 covers Working Days counted backwards): every reading is listed and a person decides
- `VOL-V:12.4+ADD-03` p2: “within five (5) Working Days of encountering them” -> **not computed: no rule in the counting registry (config/formulas.yaml `counting`) for Working Days counted after a date (VOL-I 2.4 covers Working Days counted backwards); its anchor 'encountering them' is an event, not a date the register holds** (computed: calc deadline, anchor encountering them = None, rule none, fingerprint ; PROPOSED, not validated); CONDITIONAL: “If the Project Company encounters at the site ground conditions that are materially more adverse than those described in the Geotechnical Baseline Report, it s…”

## Proposed from a pending reading (not in force; not planned)

- `ADD-03-T42-1-01` conditional on reading ADD-03-p3-r1 until approval: PENDING READING ADD-03-p3-r1. On the date the Facility is transferred to the Authority, the remaining life of each asset class must not be less than the minimu…

## Clarification route

The clarification window closed on 2026-11-12 (VOL-I 5.2): this question cannot be submitted as a clarification; it is a bid-decision for a person. Activities that relied on it: `lcc-ratio`, `lcc-certificate`, `fin-model-build`, `model-auditor-appoint`, `technical-proposal`, `lender-terms`, `model-audit-review`, `deviations-review`, `clarifications`, `fin-model-freeze`, `model-audit-opinion`, `form-4c-prep`, `fin-assumptions`, `form-4b-prep`, `form-4c-sign`, `form-4a-prep`, `form-4e`, `form-4f`, `form-4a`, `form-4b`, `assemble-envelope-b`, `copies`.

## Dates that move (0 activities; latest start / finish, validated -> candidate)

| Activity | Latest start | Latest finish | Shift (WD) | Timing | Rows that move it | Ops |
|---|---|---|---|---|---|---|
| none | | | | | | |

## New and removed activities (1 new, 0 removed)

- NEW `core-inspection-request`: needed by ADD-03-4.3-01; latest start 2026-10-28 (ops ADD-03/Q19)

## Requirement changed: work may need redoing (REWORK, 8)

- `deviations-review`: rows ADD-03-4.1-01, VOL-IV-F4E-01, VOL-V-36.2-01, VOL-V-42.1-01, VOL-V-42.1-02
- `fin-assumptions`: rows ADD-03-Q17-01
- `form-4a`: rows ADD-01-AppA-01, ADD-03-cover-01, ADD-03-cover-para3-01
- `form-4a-prep`: rows ADD-01-AppA-01, ADD-03-cover-01, ADD-03-cover-para3-01
- `form-4e`: rows ADD-03-4.1-01, VOL-IV-F4E-01, VOL-V-36.2-01, VOL-V-42.1-01, VOL-V-42.1-02
- `form-4f`: rows ADD-03-Q17-01
- `lender-terms`: rows ADD-03-Q17-01
- `technical-proposal`: rows ADD-03-3.6-01, ADD-03-4.2-01

## Confirmed, unchanged: work done stands (CONFIRMED, 1)

- `technical-proposal`: VOL-II-9.3-01: confirmed by ADD-03/Q16 (confirms; ADD-03:Q16) (proposed op, awaiting a person's acceptance); reading re-made at ADD-03 with the same words, values, parameters, dates and consequence (note: 'The text is unchanged. ADD-03 Q16 (op ADD-03/Q16, confirms) restates the clause and says 'Volume II Clause 9.3 applies.' [AI workflow run ADD-03-run-host-20261…'); text, cells, dates, status and consequence unchanged: work done stands

## Marked REVIEW through relationships (7; dates unchanged)

- `deviations-review`: confirmed dependency: VOL-IV-F4E-01 via REL-VOL-V-FORM-4E; proposed relationship: VOL-V-12.1-01, VOL-V-18.3-01 via REL-AI-008
- `fin-model-build`: proposed relationship: fin-model-build via REL-AI-001; possible impact: VOL-I-10.3-01, VOL-IV-F4F-02, fin-model-build via REL-AI-004, REL-AI-009, REL-CHANGE-IN-LAW-FINANCIAL-MODEL, REL-MODEL-FORM-4F
- `fin-model-freeze`: possible impact: VOL-I-10.3-01, VOL-IV-F4F-02 via REL-CHANGE-IN-LAW-FINANCIAL-MODEL, REL-MODEL-FORM-4F
- `form-4a-prep`: proposed relationship: form-4a-prep via REL-AI-006
- `form-4e`: confirmed dependency: VOL-IV-F4E-01 via REL-VOL-V-FORM-4E; proposed relationship: VOL-V-12.1-01, VOL-V-18.3-01 via REL-AI-008
- `form-4f`: possible impact: VOL-IV-F4F-02 via REL-CHANGE-IN-LAW-FINANCIAL-MODEL, REL-MODEL-FORM-4F
- `technical-proposal`: possible impact: technical-proposal via REL-AI-005, REL-AI-009

## Blocked: the row is unresolved, the candidate dates are not reliable (4)

- `technical-proposal` (rows ADD-03-3.6-01, ADD-03-4.2-01, VOL-II-2.2-01, VOL-II-2.2-02): ADD-03:3.6 UNRESOLVED: its obligation is proposed downstream as ADD-03-3.6-01 (row_new, interpretation_pending), DS-ADD03-3.6-issue (issue, interpretation_pending) (task(s) ana:ADD-0…; ADD-03:4.2 UNRESOLVED: its obligation is proposed downstream as ADD-03-4.2-01 (row_new, interpretation_pending) (task(s) ana:ADD-03/4.2/row; PROPOSED): no op or disposition answers t…; ADD-03:T42-1/note(4) UNRESOLVED: not promotable: D-T42-1-note4 conflicting (declared_conflicts: the proposer declares: ADD-03:p3-image); ISS-T42-note4 interpretation_pending (dropped: an analy…
- `core-inspection-request` (rows ADD-03-4.3-01): ADD-03:4.3 UNRESOLVED: its obligation is proposed downstream as ADD-03-4.3-01 (row_new, interpretation_pending), DS-ADD03-4.3-ev (evidence_item, evidence_verified), DS-ADD03-4.3-act …
- `deviations-review` (rows VOL-V-36.2-01): STALE at ADD-03: its reading was not re-made (VOL-V:36.2 changed since ADD-02 (by ADD-03/2.1); quote not found in the effective text at ADD-03: 'SAR 2,500,000' (expected: the interpretation predates the ch…)
- `form-4e` (rows VOL-V-36.2-01): STALE at ADD-03: its reading was not re-made (VOL-V:36.2 changed since ADD-02 (by ADD-03/2.1); quote not found in the effective text at ADD-03: 'SAR 2,500,000' (expected: the interpretation predates the ch…)

## Conditional scenarios and decision milestones (3)

- **DECISION-ADD-03:T42-1/4** (no date: event-dependent): ADD-03:T42-1/4 (conditional obligation; not applied in the candidate). If triggered: the obligation applies (as the candidate shows it). If not: it does not apply to this Bidder; a person records the fact (a bidder fact or an event), nothing is assumed. Activities reached: none. text only: the op file carries no conditional model for it; dates as printed, not computed.
- **DECISION-ADD-03:T42-1/5** (no date: event-dependent): ADD-03:T42-1/5 (conditional obligation; not applied in the candidate). If triggered: the obligation applies (as the candidate shows it). If not: it does not apply to this Bidder; a person records the fact (a bidder fact or an event), nothing is assumed. Activities reached: none. text only: the op file carries no conditional model for it; dates as printed, not computed.
- **DECISION-ADD-03:T42-1/note(4)** (no date: event-dependent): ADD-03:T42-1/note(4) (conditional obligation; not applied in the candidate). If triggered: the obligation applies (as the candidate shows it). If not: it does not apply to this Bidder; a person records the fact (a bidder fact or an event), nothing is assumed. Activities reached: technical-proposal — their dates in both states: technical-proposal LS 2026-10-25 (without) / 2026-10-25 (with). text only: the op file carries no conditional model for it; dates as printed, not computed.

## Files

| File | Content |
|---|---|
| programme.csv/json | every activity at the working stage with its validated dates beside it, candidate status (BLOCKED / MOVED / NEW / REVIEW / REWORK / unchanged; a confirmation is CONFIRMED (unchanged) in its changes), the rows and ops that move it |
| changes.csv/json | every activity that changes (and the removed ones) |
| marshalling.csv/json | the marshalling plan at the working stage, with blocked items |
| milestones.csv/json | the pack milestones and the candidate decision milestones |
| blockers.csv/json | activities whose row is unresolved |
| scenarios.csv/json | conditional scenarios |
| gantt.svg, gantt.html, gantt.pdf | the Gantt drawn from the same data |

CANDIDATE — NOT VALIDATED. The programme replanned at the working stage of a PARTIAL addendum: every op valid there stands as a proposal, none is accepted, and the validated A5 (the a5/ folder above this one) is unchanged. PROPOSAL, not reviewed. Every lead time, staff effort, external party waited on, multiplicity and resource capacity is a PROVISIONAL ASSUMPTION (config/assumptions.yaml: value, basis, owner); none is stated in the tender pack. Earliest dates come from a forward pass from the planning date (the latest addendum's issue date), latest dates from a backward pass in Working Days (VOL-I 2.4) from the pack's dates; negative float is INFEASIBLE, never compressed. Timing, decision readiness and resource feasibility are separate statuses; resource levelling is NOT implemented; overloads are reported, not resolved. No bidder references, certificates, attendance or financial standing are assumed to exist.
