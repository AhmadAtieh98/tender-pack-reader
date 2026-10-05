# Review request: ADD-03, run ADD-03-host-20261005T030409Z-1bb2

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T03:04:09Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 77784d6d270a9e34…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 8 of 54 provisions accounted for
- resolution (kept apart from coverage): 2 resolved, 6 pending a person, 0 invalid, 46 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

## Findings (a person looks at each)

- 2 provisions with amendment language carry no change (0 contradict a change the pattern drafter drafts from their words: invalid; 2 need a person): ADD-03:1.2, ADD-03:2.2

## Provisions not accounted for (a person treats each)

- ADD-03:3.1
- ADD-03:3.2
- ADD-03:3.3
- ADD-03:3.3(b)
- ADD-03:3.4
- ADD-03:4.1
- ADD-03:4.2
- ADD-03:5.1
- ADD-03:5.2
- ADD-03:Q15
- ADD-03:Q16
- ADD-03:Q17
- ADD-03:Q18
- ADD-03:Q19
- ADD-03:Q20
- ADD-03:Q21
- ADD-03:7.1
- ADD-03:7.2
- ADD-03:7.3
- ADD-03:7.4
- ADD-03:AppA/para1
- ADD-03:p4-image/hdr-en
- ADD-03:p4-image/hdr-ar
- ADD-03:p4-image/date
- ADD-03:p4-image/ref
- ADD-03:p4-image/subject
- ADD-03:p4-image/tender-ref
- ADD-03:p4-image/table-title
- ADD-03:p4-image/table-intro
- ADD-03:p4-image/table-header
- ADD-03:p4-image/row-a
- ADD-03:p4-image/row-b
- ADD-03:p4-image/notes-head
- ADD-03:p4-image/note1
- ADD-03:p4-image/note2
- ADD-03:p4-image/note3
- ADD-03:p4-image/signatory
- ADD-03:p4-image/stamp
- ADD-03:AppA/para2
- ADD-03:AppB/para1
- ADD-03:T5-1/a
- ADD-03:T5-1/b
- ADD-03:T5-1/notes
- ADD-03:T5-1/note(1)
- ADD-03:T5-1/note(2)
- ADD-03:T5-1/note(3)

## Items

| id | type | provision | target | status | why (first failed check) |
|---|---|---|---|---|---|
| ADD-03/cover/para1 | disposition | ADD-03:cover/para1 |  | evidence_verified |  |
| ADD-03/cover/para2 | disposition | ADD-03:cover/para2 |  | evidence_verified |  |
| ADD-03/1.1 | disposition | ADD-03:1.1 |  | interpretation_pending | depends on interpretation S-I3: a person must confirm it |
| ADD-03/1.2 | disposition | ADD-03:1.2 |  | interpretation_pending | semantic: no_effect on amendment language: a person must confirm (its words carry 'unless') |
| ADD-03/1.3 | disposition | ADD-03:1.3 |  | interpretation_pending | depends on interpretation S-I3: a person must confirm it |
| ADD-03/2.2 | disposition | ADD-03:2.2 |  | interpretation_pending | semantic: no_effect on amendment language: a person must confirm (its words carry 'renumbered') |
| ADD-03/cover/para3 | amendment_op | ADD-03:cover/para3 | ADD-03:cover/para3 | conflicting | declared_conflicts: the proposer declares: The cover says the 6.6/6.7 consolidation is 'without change of substance', but ADD-03:2.1 shortens the modification window to two Working Days before the Proposal Due Date (S-I… |
| ADD-03/2.1(a) | amendment_op | ADD-03:2.1 | VOL-I:6.6 | conflicting | declared_conflicts: the proposer declares: Cover ADD-03:cover/para3 says 'without change of substance'; the new text moves the modification cut-off to two Working Days before the Proposal Due Date (S-I1). |
| ADD-03/2.1(b) | escalation | ADD-03:2.1 | VOL-I:6.7 | escalated |  |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S-F1: ADD-03:2.1 deletes Volume I Clauses 6.6 and 6.7 and prints a single replacement Clause 6.6. — evidence verified
- **fact** S-F2: At ADD-02, VOL-I:6.7 permits modification at any time before the Proposal Due Date; the new Clause 6.6 permits modification only not later than two (2) Working Days before it. — evidence verified
- **fact** S-F3: The cover of ADD-03 describes the consolidation as being without change of substance. — evidence verified
- **fact** S-F6: Form 4-A as reissued by ADD-01 already contains the acknowledgement of Addenda. — evidence verified
- **assumption** S-A1: The Proposal Due Date is the date in VOL-I:6.1 at ADD-02 (Thursday 26 November 2026) and is not moved by another ADD-03 provision outside this batch. On that basis calculate(relative_date, 2026-11-26, 2 working_day before, purpose deadline) gives Tuesday 24 November 2026 as the last day to modify u… — needs a person
- **interpretation** S-I1: The new Clause 6.6 does change substance (the modification cut-off moves from any time before the Proposal Due Date to two Working Days before it, and late modifications are now rejected unopened), which conflicts with the cover's 'without change of substance'. The operative words of 2.1 are taken … — needs a person
- **interpretation** S-I2: The cover says ADD-03 replaces 'the odour criterion in Volume II Clause 3.5', but VOL-II:3.5 at ADD-02 is a noise criterion; this discrepancy belongs to the batch that answers the Volume II provisions and is flagged here only. — needs a person
- **interpretation** S-I3: ADD-03:1.1, 1.2 and 1.3 are recitals: they state the authority for the Addendum, how its references are read, and that late clarification requests were not answered (consistent with VOL-I:5.2); none changes the text of any unit. — needs a person
- **interpretation** S-I4: ADD-03:2.2 confirms that the deletion of 6.7 leaves a gap in numbering and that no Volume I clause is renumbered; it changes no unit beyond the 6.7 deletion carried by 2.1. — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone; NOT clean: 2 provisions with amendment language carry no change (0 contradict a change the pattern drafter drafts from their words: invalid; 2 need a person): ADD-03:1.2, ADD-03:2.2
- units changed: none
- rows citing them: none
- rows that would be STALE: none
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 0
- clarification entries citing changed units: none
- A3: enters none; leaves none

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-20261005T025444Z-analysis-001-critic`, route **host**; 7 item(s) reviewed

- **ADD-03/cover/para3** (conflicting): critic agrees — selected because conflicting, consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: Annotation (adds_obligation) of Form 4-A acknowledgement is consistent with the cover text. The target is the provision itself, which is acceptable for a self-annotation, but the cover also lists changes to Vol V 29.2, Vol II 3.1/3.5/5.6 that are not applied here (stated as carried elsewhere).
  - concern: Real conflicts: cover says 'without change of substance' but ADD-03:2.1 shortens the modification window (old 6.7: any time before due date; new: 2 Working Days before). Also the cover cites an 'odour criterion' in Vol II 3.5 while the evidence shows VOL-II:3.5 as a noise criterion (S-I2). Both are genuine and need a person.
  - concern: The statement that the Form 4-A acknowledgement is at paragraph 1 as reissued by ADD-01 rests on ADD-01 text only; ADD-01 span says it is added at paragraph 1, which is fine. Whether ADD-02 changed Form 4-A is not shown.
  - checked: ADD-03:cover/para3, ADD-01:AppA/para1 span, ADD-03:2.1, VOL-I:6.7, VOL-II:3.5 span in S-I2
- **ADD-03/1.1** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: Reading as a recital with no_effect follows from the words. It does restate precedence, but VOL-I:3.2 and 5.3 texts are not printed in the evidence, so the claim that it merely restates existing precedence cannot be verified here.
  - checked: ADD-03:1.1
- **ADD-03/1.2** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: It is a rule of reading for the Addendum's own references, so no_effect on unit text is reasonable. However, 'unless otherwise stated' could change which version a reference points to; the controller flagged it for a person. No instance of an 'otherwise stated' reference is shown in this evidence.
  - checked: ADD-03:1.2
- **ADD-03/1.3** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: Recital reporting that late clarification requests were not answered; consistent with the VOL-I:5.2 quotation. No unit text changed.
  - checked: ADD-03:1.3, VOL-I:5.2 span
- **ADD-03/2.1(a)** (conflicting): critic agrees — selected because conflicting, uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
  - concern: Replacement text matches ADD-03:2.1 verbatim and the previous value matches VOL-I:6.6. The op replaces 6.6 text only; the deletion of 6.7 is handled separately (2.1(b)), so the two must be applied together or 6.7 will conflict.
  - concern: Real conflict with the cover's 'without change of substance': modification now cut off 2 Working Days before due date (S-I1). The operative text governs only if a person confirms this.
  - concern: The 24 Nov 2026 cut-off depends on assumption S-A1 (due date 26 Nov 2026 from VOL-I:6.1, and 'Working Days' definition/calendar not shown); it needs confirmation, including whether the due date is moved elsewhere. Note that new text also adds that late modifications are rejected unopened, a substantive addition.
  - checked: ADD-03:2.1, VOL-I:6.6, VOL-I:6.7, VOL-I:6.1 span, ADD-03:cover/para3
- **ADD-03/2.1(b)** (escalated): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: Escalation is appropriate: 2.1 prints that Clauses 6.6 and 6.7 are deleted, and VOL-I:6.7 is a separate unit that must be deleted. The stated reason (engine C22 citation parsing missing 6.7) is a tool limitation reported by the proposer; it is not shown in the evidence printed here, so it cannot be verified. If 6.7 stays active it would conflict with the new 6.6, as stated.
  - checked: ADD-03:2.1, VOL-I:6.7
- **ADD-03/2.2** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: Words say 6.7 is not reused and no renumbering; no_effect on text is consistent. The controller flagged 'renumbered' as amendment language; a person should confirm. It depends on 6.7 actually being recorded as deleted (2.1(b)).
  - checked: ADD-03:2.2, ADD-03:2.1

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T030409Z-1bb2/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T030409Z-1bb2 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
