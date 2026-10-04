# Blind rehearsal 03: review of the AI proposals (host-route run)

**Synthetic, not tender content.** The review record of the evidence → proposal → validation → review workflow for
ADD-03. Input: the host-route run `ADD-03-host-20261004T102718Z-97c1` (`staging/ai/ADD-03-host-20261004T102718Z-97c1/`:
`review_request.md`, `proposals.yaml`, `log.jsonl`), made before the T5 live fixes. Each item was checked by the
curator against the evidence build (`build/units.json`, the effective text at ADD-02 and ADD-03 through
`tenderpack.amend.Engine`), not against the run's own statuses (which are the controller's, never decisions).

Nothing here is accepted, applied by a person or published as a decision. The run was not promoted
(`tenderpack ai promote`): the curated op file was written by the curator, with each item below used, corrected or
rejected by hand. Every op and row in `work/` stays `review: proposed`; the drafter's ops keep `origin: pattern`, the
curator's `origin: assistant`.

Final curation: `work/amendments/ADD-03.yaml` (27 ops, 4 `no_effect` dispositions, 0 unresolved; ADD-03 APPLIED).

## Items (40)

| AI item | Type | Controller status | What the curator did |
|---|---|---|---|
| ADD-03/cover/para1 | disposition | evidence_verified | USED AS PROPOSED (identical to the drafter's `no_effect`: the issue date line) |
| ADD-03/cover/para2 | disposition | evidence_verified | USED AS PROPOSED (the drafter's `no_effect`, reason "tender reference on the cover") |
| ADD-03/1.1 | disposition | evidence_verified | USED AS PROPOSED (`no_effect`, recital; the drafter's wording kept) |
| ADD-03/1.2 | disposition | evidence_verified | USED AS PROPOSED (`no_effect`: a rule for reading the Addendum's own references, applied in every op's target; the drafter had left it unresolved) |
| ADD-03/2.1 | amendment_op | evidence_verified | USED AS PROPOSED (identical to the drafter's `replace_text` on VOL-I:2.4; kept as `origin: pattern`) |
| ADD-03/2.1(b) | amendment_op | evidence_verified | USED AS PROPOSED; the `expect` quotes the whole unchanged second sentence of VOL-I 2.4 instead of a fragment |
| ADD-03/2.2 | escalation | escalated | ESCALATION RESOLVED: `annotate`, `effect: non_working_day`, `date: "2026-11-22"`, `targets: [ADD-03:2.2]` (T5 fix 3). From ADD-03 the date rules count Sunday 22 November 2026 as non-working: VOL-I 5.2 cut-off Wednesday 11 November (was 12), ADD-03 3.2 Thursday 19 November. REJECTED the proposed remedy ("a person must add 2026-11-22 as a non-Working Day" in the pack's assumptions): the day is notified by the Addendum and is evidence, not an assumption; `assumptions.yaml` calendar left as it was |
| ADD-03/3.1 | amendment_op | evidence_verified | USED AS PROPOSED (identical to the drafter's `append_text` on VOL-I:8.8; `origin: pattern`) |
| ADD-03/3.2 | amendment_op | conflicting | CORRECTED: same op (`annotate adds_obligation` on VOL-I:8.1, condition stated); the note's "calculate gives Sunday 22 November 2026" is replaced by the engine's date with the closure counted (Thursday 19 November 2026). The declared conflict with Q17 is real and KEPT OPEN for a person (op `issue`, I-ADD03-CONSENT-DATE, draft CQ-ADD03-CONSENT-DATE); both dates are planned (row ADD-03-3.2-01: rules CONSENT-APPLICATION and CONSENT-APPLICATION-Q17), the programme works to the earlier |
| ADD-03/3.3 | amendment_op | insufficient_evidence | USED (note corrected): the missing information (whether the issue day counts in a forward Working-Day period) is a counting convention the pack does not state; the date module already computes both readings (Thursday 5 / Sunday 8 November 2026) and plans the earlier, as for ADD-01 3.1. Row ADD-03-3.3-01 (rule INTENT-NOTICE, anchor ADD-03-issue); recorded under `checked_no_question` |
| ADD-03/3.4 | amendment_op | interpretation_pending | USED AS PROPOSED |
| ADD-03/4.1 | escalation | escalated | ESCALATION RESOLVED: two ops under 4.1 (which cites Form 4-C and "the fourth numbered declaration"): ADD-03/4.1(a) `insert_unit`, `anchor: VOL-IV:F4-C/image/decl4`, `new_text` = the substituted Arabic declaration, `new_text_from: ADD-03:4.2`, `covers: [ADD-03:4.2]` (C21: printed in full by ADD-03:4.2), then ADD-03/4.1(b) `set_status: deleted` on decl4. Result: VOL-IV:F4-C/image/decl4+ADD-03 holds the new declaration, the issued one is DELETED. The `replace_text` route suggested for the live fixes does not validate (see "Could not be expressed as proposed") |
| ADD-03/4.2 | escalation | escalated | ESCALATION RESOLVED: content of ADD-03/4.1(a) (`covers`, `new_text_from`) |
| ADD-03/4.3 | amendment_op | conflicting | CORRECTED: op kept (`confirms` VOL-I 9.4). The declared conflict with 4.2 is REJECTED as a conflict: the translation's "within three (3) days" against the Arabic "خلال ثلاثة أيام عمل" is a discrepancy the provision resolves itself ("The Arabic text governs"); kept as an `issue` and I-ADD03-F4C-UNDERTAKING. REJECTED the statement that "exclusion of the Proposal" is "not one of the pack's English consequence categories": `exclusion` is a register consequence class (`register.CONSEQUENCE_CLASSES`), kept as its own category (I-F4C-EXCLUSION) |
| ADD-03/4.4 | amendment_op | interpretation_pending | CORRECTED: the `issue` "depends on the substitution in 4.1/4.2, which is escalated" removed (the substitution is now made); targets and effect as proposed |
| ADD-03/5.1 | amendment_op | conflicting | USED AS PROPOSED (`set_value` VOL-II:T2-4/TP Limit 0.5). The controller's "conflicting" (a change to an owner-approved image reading) is not a conflict (T5 fix 5): the approval covers the transcription as issued; 0.5 mg/l is the Addendum's separate value. The Permit `issue` kept, pointed at I-PERMIT (the missing Permit stays open) |
| ADD-03/5.1(b) | amendment_op | evidence_verified | USED, extended: `expect` checks TN `Limit: 3 |` and TP unit and basis (the provision says both unchanged); all three are `contains` checks, which the engine evaluates for an annotate (a negative control with a wrong value fails C27) |
| ADD-03/5.2 | amendment_op | interpretation_pending | USED AS PROPOSED (target `VOL-II:S3`, as ADD-02 5.2) |
| ADD-03/6.1 | amendment_op | evidence_verified | USED AS PROPOSED (identical to the drafter's; `origin: pattern`) |
| ADD-03/6.1(b) | amendment_op | evidence_verified | USED AS PROPOSED (`expect` widened to "…after PCOD (the Ramp-Up Period)") |
| ADD-03/6.2(a) | amendment_op | evidence_verified | USED AS PROPOSED as the drafter's identical op `ADD-03/6.2` (`set_status deleted` VOL-V:31.4; drafter's id and `origin: pattern` kept) |
| ADD-03/6.2(b) | amendment_op | evidence_verified | USED AS PROPOSED (`set_status deleted` VOL-V:39.3; the cover-omission `issue` kept). Its claim that no other unit cites 31.4 or 39.3 was checked: true |
| ADD-03/7.1 | escalation | escalated | ESCALATION RESOLVED: `replace_unit`, `target: ADD-02:F4-G`, `replacement: ADD-03:F4-G`, `covers:` AppA/para1, F4-G/T1/1-7, F4-G/para1 (T5 fix 1). Items 1-6 follow by key; item 7 and the new signature block are content |
| ADD-03/7.2 | amendment_op | interpretation_pending | CORRECTED: the `issue` "the reissued Form 4-G itself could not be placed by an op" removed; the reading "treated as not submitted, i.e. non-responsive under ADD-02 7.2" agreed (row ADD-03-7.2-01, class `non_responsive`, quoted from ADD-02 7.2) |
| ADD-03/AppA/para1 | escalation | escalated | ESCALATION RESOLVED: covered by ADD-03/7.1 |
| ADD-03/F4-G/T1/1 | escalation | escalated | ESCALATION RESOLVED: covered by ADD-03/7.1 (row ADD-02-F4G-02 follows the reissued item) |
| ADD-03/F4-G/T1/2 | escalation | escalated | ESCALATION RESOLVED: covered by ADD-03/7.1 (row ADD-02-F4G-03 follows) |
| ADD-03/F4-G/T1/3 | escalation | escalated | ESCALATION RESOLVED: covered by ADD-03/7.1 (row ADD-02-F4G-01 follows) |
| ADD-03/F4-G/T1/4 | escalation | escalated | ESCALATION RESOLVED: covered by ADD-03/7.1 (row ADD-02-F4G-05 follows; the reissued unit added to its units for C30) |
| ADD-03/F4-G/T1/5 | escalation | escalated | ESCALATION RESOLVED: covered by ADD-03/7.1 (row ADD-02-F4G-06 follows) |
| ADD-03/F4-G/T1/6 | escalation | escalated | ESCALATION RESOLVED: covered by ADD-03/7.1 (row ADD-02-F4G-07 follows) |
| ADD-03/F4-G/T1/7 | escalation | escalated | ESCALATION RESOLVED: covered by ADD-03/7.1; new row ADD-03-F4G-01 (post-award, with `post_award_evidence`) |
| ADD-03/F4-G/para1 | escalation | escalated | ESCALATION RESOLVED: covered by ADD-03/7.1; new row ADD-03-7.2-01 (countersignature) |
| ADD-03/Q15 | amendment_op | evidence_verified | USED AS PROPOSED (`append_text` on ADD-02:Q9) |
| ADD-03/Q15(b) | amendment_op | interpretation_pending | USED AS PROPOSED |
| ADD-03/Q16 | amendment_op | evidence_verified | USED AS PROPOSED |
| ADD-03/Q17 | escalation | conflicting | ESCALATION RESOLVED as an op (`annotate adds_obligation`, target VOL-I:8.1, with the date as a fixed rule on row ADD-03-3.2-01); the DECISION is KEPT OPEN: which deadline governs (Q17: Sunday 22 November 2026, the closure day; 3.2: Thursday 19 November 2026) is for a person (I-ADD03-CONSENT-DATE, CQ-ADD03-CONSENT-DATE) |
| ADD-03/Q18 | amendment_op | evidence_verified | USED AS PROPOSED (`confirms` VOL-V:31.4, valid after the deletion) |
| ADD-03/Q19 | amendment_op | evidence_verified | USED AS PROPOSED |
| ADD-03/cover/para3 | amendment_op | conflicting | CORRECTED: the drafter's op (acknowledge in Form 4-A) with the AI's cover `issue`, rewritten as the curator's list of the cover's errors (contradicted, omitted, understated). The declared "conflicts" are not conflicts of the op: the cover is never applied. Marked `origin: assistant` |

Statements (kept apart by the run): S-PDD (fact), S-COVER-DEADLINE (fact) and S-F4G-NEW (fact) checked and correct;
S-CLOSURE and S-Q17-DATE (interpretations) checked and adopted (the engine now counts the closure); S-AR-WORKDAYS
(interpretation) checked and adopted (the Arabic says working days and governs); S-FWD-COUNT (assumption) checked:
both readings correct, the earlier is planned.

## Provisions the AI's accounting missed or mis-targeted

- None missed: the run accounted for 35 of 35 provisions, and so does the curation (C20 ADD-03 ok).
- Mis-handled rather than mis-targeted: 4.1/4.2 were escalated as inexpressible, but `insert_unit` (an op type the
  `amend.py` docstring lists) with `new_text_from` a unit of the same addendum, plus `set_status deleted`, expresses
  the substitution; 4.3 was declared a conflict with 4.2 although the provision itself says which text governs; 2.2's
  remedy pointed at the assumptions file instead of an op.
- Not in the run's scope but missing from its impact: the old Form 4-G signature row (ADD-02-F4G-04) goes REPLACED
  with no successor of its own (the reissued signature block replaces the group, not the row): new row ADD-03-7.2-01.

## Could not be expressed as proposed (engine limit; worked around, no code patched)

The substitution in 4.1/4.2 as a single `replace_text` on `VOL-IV:F4-C/image/decl4` (the route the live fixes
anticipated) is refused:

- under ADD-03:4.2 (old `matched_in_target`, new as 4.2 prints): `C22 the provision cites no clause, table, form or
  section that exists in the pack` (4.2 names no target; its heading "4. AMENDMENT TO FORM 4-C" is not read as a
  citation because `citations()` matches "Form 4-C" case-sensitively); `append_text` under 4.2 fails the same way;
- under ADD-03:4.1 (old quoted, new from 4.2): `C21 not in the provision: ['رابعاً: أن جميع المعلومات …']`.

Expressed instead as ADD-03/4.1(a) `insert_unit` + ADD-03/4.1(b) `set_status deleted` (valid; ADD-03 APPLIED). Side
effect: C28 reports three "contradicted" findings on the cover's "replaces the fourth declaration in Form 4-C" that are
artefacts of this representation (the claim is accurate). No provision is left `unresolved`.
