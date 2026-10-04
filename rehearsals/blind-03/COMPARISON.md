# Blind rehearsal 03: results against the sealed answer key

## How the rehearsal ran

- **The addendum.** An independent subagent wrote it from the pack's PDFs, the brief and the correspondence only (`FROZEN.md`, `SEALED/author_notes.md`). It did not read the tool's code, tests, curation, outputs or docs. It is the first rehearsal with an Arabic text layer (the substituted Form 4-C declaration), a change inside a definition (Working Day), a notified non-working day, two deadlines for one application in the same addendum, and a cover sentence contradicted only by a derived date.
- **The freeze.** The PDF and the sealed `SHA256SUMS` were frozen by hash in `FROZEN.md` on 4 Oct 2026 at 09:22:15 UTC, before the addendum was opened. The sealed files were kept outside the repository until the unsealing.
- **Unsealing.** The key was opened on 4 Oct 2026 at 11:05:08 UTC, after the last curated build (11:01:55), the diff (11:01:57) and live fix 6 (11:04:47). All four hashes matched: `sha256sum -c SEALED/SHA256SUMS` passed for the three sealed files, the PDF's line passed from the repository root, and the hash of `SEALED/SHA256SUMS` equals the one in `FROZEN.md`.
- **Who did what (the AI layer in the loop).** The pattern drafter proposed 6 ops and left 29 provisions. A **proposer** (a Claude Code subagent, declared model Opus 5.5, the host route through the CLI tools, no application API call) read the evidence through the tools and submitted a proposal set that the deterministic controller validated and staged (`staging/ai/ADD-03-host-20261004T102718Z-97c1/`: 35 of 35 provisions accounted for; 16 evidence_verified, 5 interpretation_pending, 5 conflicting, 1 insufficient_evidence, 13 escalated). A **curator** (another Opus 5.5 subagent, acting as the live-session curator) checked every item against the evidence, used, corrected or rejected it (`ai-proposals-used.md`), wrote the op file, the rows, the issues, the A5 templates and the clarification entries, and ran the normal path. The coordinator (Fable 5.1) opened the key afterwards and scored. Both subagents wrote the tool's code earlier in the session, which is the main limit on how blind this was; neither saw the key.
- **What is scored.** Only what was produced before the key was opened: `out-curated/` (the 11:01:55 build), `diff-ADD-02-to-ADD-03.md`, the `work/` curation and `ai-proposals-used.md`. Changes made after the key (§"After the key") are marked and rebuilt into `out-after-fixes/`; they are not scored.
- **Nothing is decided.** Every op and every row is PROPOSED. Nobody accepted or rejected anything, no clarification question was sent, and the release blockers say so (217 rows, 64 ops).

## Timeline (UTC, from `clock.txt`)

| Step | Start | End | Elapsed |
|---|---|---|---|
| Set up the pack and ingest (7 documents, 573 units; C01–C10 pass) | 10:11:24 | 10:11:39 | 0:15 |
| Draft (6 ops from patterns; 29 provisions left for a person) | 10:11:39 | 10:12:17 | 0:38 |
| Drafted working draft published (ADD-03 PARTIAL; validated state stays ADD-02) | 10:12:17 | 10:13:31 | 1:14 |
| **AI proposals, host route** (task packet with the lock; 35 items; submitted and validated; `review_request.md`) | 10:14:41 | 10:27:20 | 12:39 |
| **Live fixes 1–5** (before the curation; the AI run kept as made): a form an addendum inserted is citable; Arabic matched without diacritics; a notified non-working day as an op; a whole cell value is evidence; an amendment to an approved reading is recorded, not a conflict | 10:31:57 | 10:35:09 | 3:12 |
| Curation: the AI proposals read against the evidence; op file written (27 ops, 4 dispositions; engine: ADD-03 APPLIED) | 10:36:03 | 10:43:26 | 7:23 |
| Register (12 new rows, 32 re-made readings, 7 issues, 4 evidence items), A5 templates (7 new activities, 6 lead times), clarification register (cut-off recomputed, 2 draft questions) | 10:43:26 | 10:55:48 | 12:22 |
| `pin` (44 pins; `pin --rows` crashed: live fix 6 below; the 3 re-pins made from a scratch script) and `check-register --update-ids` (0 findings) | 10:55:53 | 10:56:57 | 1:04 |
| Curated outputs published (STALE none; blocked only by the decisions nobody has made) | 10:56:57 | 10:57:03 | 0:06 |
| `ai-proposals-used.md`; the cover op's issue and the 5.1(b) expectations made checkable; the countersignature as its own evidence item and action; outputs republished (three reruns) and `diff` | 10:57:03 | 11:01:57 | 4:54 |
| **Live fix 6** (after the curation, before the key): `pin --rows` built the register without a calendar | 11:04:47 | | |
| **Unseal** | 11:05:08 | | |
| **Post-key fixes** (not scored; §"After the key") | 11:08 | 11:18 | |

Elapsed from receipt to the scored output: **50 minutes 31 seconds**, of which the AI proposal run took 12:39 and the live-fix pause between the proposer and the curator 8:43 (10:27:20–10:36:03). The curation itself took 25:52. Blind rehearsal 02 (no AI layer, one curator) took 32 minutes with a 10-minute interruption.

## Results

**Count:** 34 provisions, answers, cover errors, secondary effects and A3 changes: **31 hits, 3 partial, 0 missed.** Every expected date is right (one, the 3.3 notice, by the alternative reading the key accepts when it is stated). Every "must not report" trap was avoided (17 of 17). The deliberate ambiguity (3.2 vs Q17) was escalated with both sources and not resolved.

### Body provisions

| Key | Expected | Result | Evidence in the blind outputs |
|---|---|---|---|
| 1.1, 1.2 | recitals, no effect | **hit** | `no_effect` dispositions with reasons; 1.2's rule applied in every op's target |
| 2.1 | VOL-I 2.4 substitution; second sentence unchanged | **hit** | `replace_text` with the exact old and new words; `ADD-03/2.1(b)` checks the second sentence verbatim (T11) |
| 2.2 | 22 Nov 2026 not a Working Day; PDD unaffected | **hit** | `annotate effect: non_working_day, date: 2026-11-22` (live fix 3): `Register.cal_by_stage` counts it from ADD-03; the PDD stays 26 Nov 14:00 (A3 subtitle, `milestones.csv`); described as a notified closure, not a public holiday (T12) |
| 3.1 | 8.8 appended: member and 10 % lock-in; no stated consequence; mandatory by inference | **hit** | `append_text` verbatim; rows `ADD-03-3.1-01` (pass/fail, "no consequence stated", I-NO-CONSEQUENCE) and `ADD-03-3.1-02` (post-award lock-in). A3 lists 3.1-01 under "no stated consequence" in the VOL-I 11.1(i) gate; the inference is left to a person, as the key's A5 allows |
| 3.2 | consent application Thu 19 Nov 2026 (closure skipped); conflict with Q17 | **hit** | rule CONSENT-APPLICATION 2026-11-19; the Q17 date kept as a second rule (2026-11-22); I-ADD03-CONSENT-DATE and draft CQ-ADD03-CONSENT-DATE; the programme works to the earlier, labelled |
| 3.3 | notice Sun 8 Nov 2026 (or Thu 5 Nov if the convention is stated); not Fri 6 Nov | **hit** | INTENT-NOTICE 2026-11-05 with both readings stated (5 Nov if the issue day counts, 8 Nov if not) and the policy named; no consequence invented (T15) |
| 3.4 | event + 2 Working Days; VOL-I 8.1 applies | **hit** | row `ADD-03-3.4-01`, an event-driven period; activity `om-member-change-notice` (NO DEADLINE REACHED) |
| 4.1–4.4 | fourth declaration replaced; Arabic preserved verbatim; translation discrepancy (3 days vs 3 Working Days) flagged; Arabic applied; 4.4 chain non-responsive; others unchanged | **hit** | the substituted Arabic is the addendum's text-layer words (`insert_unit` from ADD-03:4.2 + `set_status deleted` on the issued declaration); rows `ADD-03-4.2-01/02` quote the Arabic and gloss it with the Authority's translation; the period is "three working days (Arabic, governing)" and the discrepancy is I-ADD03-F4C-UNDERTAKING (T10); `ADD-03-4.4-01` non_responsive via VOL-I 9.4; declarations 1, 2, 3 and 5 untouched (T9). See "What the engine could not express" for why two ops |
| 5.1–5.2 | TP 1 → 0.5 mg/l in the image-only table; unit, basis, other rows unchanged; not an A3 item | **hit** | `set_value` on the TP cell; `5.1(b)` checks TN 3, the unit and the basis (T6); the diff says "image shows 1, ADD-03 makes it 0.5 (reading approved; the image itself is unchanged)"; row `ADD-03-5.2-01`; nothing on A3 |
| 6.1 | 29.3 90 % → 85 %; Ramp-Up unchanged; commercial only; omitted from the cover (E2) | **hit** | `replace_text`; `6.1(b)` checks the twelve months (T7); not on A3; C28 reports the omission |
| 6.2 | 31.4 and 39.3 deleted; no renumbering; cross-references; Schedule 11 gap | **partial** | both deletions, "not renumbered" noted (T8); `VOL-V-31.4-01` DELETED (out of force); Q18 read as moot (T5). Not flagged: that Schedule 11 is not supplied, so whether persistent breach survives there cannot be checked (the key's U5) |
| 7.1–7.2 + App. A | Form 4-G replaced; item 7 unmentioned; countersignature or "treated as not submitted" → non-responsive; items 1–6 unchanged | **hit** | `replace_unit ADD-02:F4-G → ADD-03:F4-G` (live fix 1); row `ADD-03-F4G-01` and I-ADD03-F4G-ITEM7; row `ADD-03-7.2-01` non_responsive through ADD-02 7.2; the six ADD-02 rows follow by key (T14); activity `form-4g-countersign` |

### Clarification answers

| Key | Expected | Result | Evidence |
|---|---|---|---|
| Q15 | ADD-02 response 9 amended; translation required from members incorporated outside the Kingdom; no stated consequence | **hit** | `append_text` on ADD-02:Q9 (A2 shows the response as amended); row `ADD-03-Q15-01`, conditional; I-ADD03-Q15; activity `form-4c-translation` |
| Q16 | decoy: restates VOL-II 9.4 | **hit** | `confirms`; no row (T3) |
| Q17 | the genuine ambiguity: escalate with both sources; no automated choice | **hit** | `adds_obligation` on VOL-I 8.1 with its own date rule; I-ADD03-CONSENT-DATE on A3; the Q17 date applied to the O&M application only (T16) |
| Q18 | consequential; not a second deletion | **hit** | `confirms` VOL-V 31.4 after its deletion |
| Q19 | restates VOL-I 9.4 | **hit** | `confirms`; no change to the signatory rule (T4) |

### The cover's planted errors and the effects it does not itemise

| Key | Expected | Result | Evidence |
|---|---|---|---|
| E1 | "does not affect any deadline" is false: the 5.2 cut-off moves 12 → 11 Nov; 3.2 is 19 Nov | **hit** (by the curator; C28 did not detect it) | cut-off 2026-11-11 in the register, A5 and the diff; op issues on the cover and on 2.2; I-ADD03-CLOSURE on A3; draft CQ-ADD03-CLOSURE. C28 compares claims with ops and had no test for a derived date: post-key fix 1 |
| E2 | 6.1 omitted from the cover | **hit** | C28: "omitted: ADD-03/6.1 amends VOL-V:29.3" (A2, diff) |
| S1 | cut-off 12 → 11 Nov | **hit** | `CLARIFICATION-CUTOFF 2026-11-12 -> 2026-11-11` |
| S2 | 10 % lock-in | **hit** | row `ADD-03-3.1-02`; named in the cover issue |
| S3 | 3.2, 3.3, 3.4 obligations | **hit** | three rows, three activities |
| S4 | 39.3 deleted consequentially | **hit** | `ADD-03/6.2(b)`; C28 reports it omitted from the cover |
| S5 | Form 4-G item 7 | **hit** | row `ADD-03-F4G-01`; I-ADD03-F4G-ITEM7 |
| S6 | no countersignature → non-responsive | **hit** | row `ADD-03-7.2-01` |
| S7 | response 9 amended by Q15 | **hit** | as above |
| S8 | the new Arabic undertaking with exclusion | **hit** | row `ADD-03-4.2-02`, class `exclusion`, quoted |
| S9 | knock-ons of membership: the O&M Operator's own Form 4-C, 8.2, 8.4 weighting, 8.1 consent | **partial** | 8.1 consent and "each member" (4.4) are there; the O&M Operator's own Form 4-C, 8.2 and the 8.4 weighting are not spelled out |
| S10 | TP knock-ons: VOL-II 3.1, 7.2/7.3 reliability run, VOL-V 31.1(b), 29.3 second limb | **partial** | VOL-II 3.1 (via 5.2) and VOL-V 29.3 (its row cites the TP cell) are linked; the reliability run and 31.1(b) are not |

### A3

| Key | Expected | Result |
|---|---|---|
| D1 | substituted declaration or not properly executed → non-responsive | **hit**: `ADD-03-4.4-01` |
| D2 | breach of the undertaking → exclusion; 3 Working Days | **hit**: `ADD-03-4.2-01/02`, exclusion kept as its own category (I-F4C-EXCLUSION), period from the Arabic |
| D3 | no countersignature → non-responsive | **hit**: `ADD-03-7.2-01` |
| D4 | 8.8 membership: inferred, medium | **hit** by the tool's rule: listed under "no stated consequence" in the gate; the inference is for a person (the key's A5 accepts "not stated" with any inference labelled) |
| D5 | admission without consent → rejection; deadline unresolved | **hit**: `ADD-03-3.2-01` rejection (VOL-I 8.1) with I-ADD03-CONSENT-DATE |
| changed | ADD-02 7.2 row refers to the reissue; VOL-I 9.4 row content changes | **hit**: both rows CHANGED in the diff |
| must not add | TP, 29.3, 31.4/39.3, Q16, Q19, 3.3 | none of them on A3 |

### Dates (A5 and the register)

All twelve derived dates match the key: issue Sun 1 Nov; 3.3 notice 5 Nov (the stated alternative; 8 Nov is the other reading, both printed; not Fri 6 Nov); cut-off Wed 11 Nov; 3.2 Thu 19 Nov; closure Sun 22 Nov; PDD Thu 26 Nov 14:00; Proposal validity 25 Apr 2027; Bid Bond validity 25 May 2027; look-back from 26 Nov 2016; the Form 4-C undertaking 3 Working Days to the PBN; the 3.4 notice 2 Working Days; the Ramp-Up Period 12 months at 85 %. The key's VOL-I 4.3 example (a contact change on 19 Nov notified by Tue 24 Nov, the closure skipped) is not printed anywhere: the rule is event-dependent, and the calendar that would compute it is the one the register now keeps per stage.

### Marshalling (A5)

M1 (notice of intention), M2 (clarifications by 11 Nov), M3 (consent application by 19 Nov, labelled conservative), M4 (no delivery on the closure day: the calendar skips it), M5 (Form 4-C per member with the substituted declaration; translations for members incorporated outside the Kingdom), M6 (the reissued Form 4-G with both signatures), M7 (process design at 0.5 mg/l), M9 (Form 4-A acknowledges three addenda), M10 (the two post-submission watch items), M11 (Envelope A order unchanged): **hit**. **M8 partial**: the 85 % Ramp-Up payment reaches A1 (`VOL-V-29.3-01` re-made) but no activity depends on that row, so the Financial Model and Form 4-F activities show no rework.

### Unresolved items and ambiguities

U1 (3.2 vs Q17), U2 (Q15 consequence), U4 (8.8 consequence): **raised**, as issues with draft questions where a question helps. U3 (3.3 consequence): the "not stated" is recorded; whether a missed notice bars a later application is not asked. **U5 (Schedule 11 not supplied) and U6 (a single-entity Bidder with a separate O&M firm) were not raised**; the key rates U6 low relevance. Ambiguities: A1 escalated; A2 both readings; A4 flagged and the Arabic applied; A5 "not stated" everywhere; A6 as before. A3 (whether the amended 2.4 governs Volume V's own Working-Day periods) was not flagged; the key accepts either reading if flagged and rates the practical impact nil.

### Traps

None of T1–T17 was reported: the PDD unchanged; the cover not trusted; Q16, Q18, Q19 as no change; Table 2-4 beyond TP, the Ramp-Up length, Volume V numbering, the other declarations, the English "three days", the second sentence of 2.4, a public holiday, a Parent Company Guarantee, Form 4-G items 1–6, a consequence for 3.3 or Q15, Q17 generalised, and the blind-01/02 subjects: all untouched.

## The AI layer's contribution, measured against the key

- **The proposer's 35 items** (`ai-proposals-used.md`): 16 `evidence_verified` items were used as proposed (14 of them identical to the curator's final ops, two with widened expectations); 5 `interpretation_pending` used; 5 `conflicting` corrected (two declared conflicts were not conflicts: the translation that the provision itself resolves, and the cover sentence that is never applied; one was the old approval policy; the 3.2 date ignored the closure; the Q17 conflict was real and kept open); 1 `insufficient_evidence` used with its note corrected (the forward-count gap is a stated pair of readings, not missing evidence); 13 `escalated` resolved by the curator, 9 of them because the engine had no way to place a reissued form added by an earlier addendum (live fix 1), 1 because the calendar had no op for a notified day (live fix 3), 2 because the proposer thought the Arabic substitution inexpressible (it was, as two ops), 1 the proposer's own escalation of the Q17 conflict.
- **What the proposer got right that the pattern drafter did not:** 29 of the 35 provisions, including every annotation, the Q15 amendment of an earlier answer, the closure's effect on the dates, the Arabic/English discrepancy and the Q17 conflict, each with verbatim evidence that the controller verified.
- **What a person still had to do:** decide every item (nothing is accepted); correct five statuses; write the 12 rows, 32 readings, 7 issues, the A5 activities and the clarification entries (the proposer's contract carries ops, dispositions and statements, not rows); resolve 13 escalations, 10 of which were tool gaps fixed live.
- **Human review time** for what the rehearsal produced, estimated and untested against a real reviewer: reading the 40-item review request against its evidence, about 30–40 minutes; deciding the 27 ops, about 40 minutes; the 12 new rows and 32 re-made readings, about 45 minutes; the 7 issues and 2 draft questions, about 20 minutes with the advisers' input: **about 2 to 2½ hours** for one reviewer, before any legal or commercial call.

## What the engine could not express (pre-key; worked around, no code patched)

The substitution of the Form 4-C declaration as one `replace_text`: under ADD-03 4.2 it failed C22 (4.2 names no target; its heading "4. AMENDMENT TO FORM 4-C" was not read as a citation because the form pattern was case-sensitive), under 4.1 it failed C21 (the new words are printed by 4.2, not 4.1). The curator wrote `insert_unit` (text from 4.2, `covers: [ADD-03:4.2]`) + `set_status deleted` under 4.1: valid, APPLIED, the same end state, but C28 then reported three "contradicted" findings against the cover's accurate "replaces the fourth declaration in Form 4-C". Both are fixed after the key (below).

## Live fixes (before the key; each general and tested)

1. A form an addendum inserted is citable (`ADD-02:F4-G`): `citations.resolve` (test `test_a_form_that_an_addendum_inserted_resolves_under_the_addendum`).
2. Arabic words matched without diacritics or alef-form differences (`amend._contains`, `_quoted_in`, `_replace_once`, `_arabic_span`).
3. A notified non-working day as an op (`annotate effect: non_working_day`, `date`; C21 requires the provision to print the day); the register keeps a calendar per stage; the date rules and the programme count it.
4. A whole cell value is evidence however short (the AI controller).
5. An amendment to an owner-approved reading is recorded, not a conflict (the AI controller).
6. `pin --rows` built the register without a calendar and crashed after fix 3 (found by the curator at 10:56; fixed at 11:04 before the key; `test_pin_rows_builds_the_register_with_the_packs_calendar`).

All six are in `tests/test_session09_blind03_live_fixes.py`. The real pack's outputs are byte-identical after them, except that `stages.json` now also lists `ADD-02:F4-G` among the units ADD-02/7.1 cites (fix 1); A1–A5 are unchanged.

## After the key (not scored)

Three fixes, each general, each with a regression in `tests/test_session09_blind03_postkey_fixes.py` that failed before it (11:08–11:18 UTC):

1. **C28 "no date affected" claims.** A cover sentence "<X> does not affect any deadline | the Proposal Due Date | ..." is now a claim judged by the register's computed dates: contradicted when a date rule in force at this stage and the one before has a different planning date, naming the rule, its row and both dates (the planted E1: `CLARIFICATION-CUTOFF (row VOL-I-5.2-01, VOL-I 5.2) moves from 2026-11-12 to 2026-11-11`). A scope naming one anchor or rule is judged by that one.
2. **Insert + delete at one anchor is a substitution.** C28 reads an `insert_unit` whose anchor a `set_status deleted` removes at the same stage as "replace": the three artefacts disappear; the obligation 4.4 adds is still reported as omitted; E2 is still found.
3. **A heading names a form whatever its case.** `citations()` reads "FORM 4-C"; a `replace_text` under ADD-03 4.2 (old words located in the target, new words printed by 4.2) now passes C21 and C22. The curation was left as made (two ops under 4.1), so A1's shape is unchanged.

`out-after-fixes/` is the same curation rebuilt with these fixes (11:18–11:19 UTC); `diff-after-fixes-ADD-02-to-ADD-03.md` is its diff. C28 on ADD-03 then reads: 8 claims, **contradicted 1** (E1: "'The closure of the Authority's offices does not affect any deadline under the RFP Documents', but CLARIFICATION-CUTOFF (row VOL-I-5.2-01, VOL-I 5.2) moves from 2026-11-12 to 2026-11-11"), omitted 6, understated 3; before the fixes it read contradicted 3 (the artefacts), omitted 5, understated 3 and nothing on E1. Everything else in the outputs is unchanged. The real pack's outputs and the other two rehearsals' were rebuilt and compared after them (recorded in the session log §6).

## Tool follow-ups (for the plan)

1. **A5 and contract-stage rows.** No activity depends on `VOL-V-29.3-01`, so a payment-mechanism change does not mark the Financial Model and Form 4-F for rework (M8). An activity template for Envelope B should name the VOL-V rows its pricing relies on.
2. **Knock-on rows.** Membership changes (8.2, 8.4 weighting, a Form 4-C from the new member) and effluent-limit changes (the VOL-II 7.2/7.3 reliability run, VOL-V 31.1(b)) are not linked to the rows that carry them; `diff` can only report rows that cite the changed unit. A curated "depends on" list per row would carry them (S9, S10).
3. **Gaps the pack leaves.** A reference to a schedule or document the pack does not supply (Schedule 11) should be an issue on the row whose provision cites it (U5), as the Permit is.
4. **`replace_text` from another provision.** `new_text_from`/`covers` exist for `insert_unit` only; a substitution printed across two provisions (old in 4.1, new in 4.2) still needs two ops or `old_resolved: matched_in_target` under the provision that prints the new words.
5. **The proposer's tool friction** (session log §4.6): the `{"proposal": …}` wrapper, the fixed purpose and unit lists of `calculate`, escalations counted as unaccounted by `simulate_amendment` until submission, `get_unit` on a group, a declared conflict outranking `escalated`.
