# Review request: ADD-03, run ADD-03-host-20261005T173952Z-d69e

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T17:39:52Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build f826cdeb7fbc262e…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 5 of 70 provisions accounted for
- resolution (kept apart from coverage): 3 resolved, 2 pending a person, 0 invalid, 65 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

## Findings (a person looks at each)

- 1 provision with amendment language carries no change (0 contradict a change the pattern drafter drafts from their words: invalid; 1 need a person): ADD-03:1.2

## Provisions not accounted for (a person treats each)

- ADD-03:2.1
- ADD-03:2.2
- ADD-03:2.3
- ADD-03:2.4
- ADD-03:2.5
- ADD-03:2.6
- ADD-03:2.7
- ADD-03:3.1
- ADD-03:3.2
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
- ADD-03:AppA/para1
- ADD-03:p4-image/hdr-en
- ADD-03:p4-image/hdr-ar
- ADD-03:p4-image/ref
- ADD-03:p4-image/date
- ADD-03:p4-image/subject
- ADD-03:p4-image/tender-ref
- ADD-03:p4-image/table-title
- ADD-03:p4-image/intro
- ADD-03:p4-image/th-point
- ADD-03:p4-image/th-location
- ADD-03:p4-image/th-diameter
- ADD-03:p4-image/th-window
- ADD-03:p4-image/th-duration
- ADD-03:p4-image/th-notice
- ADD-03:p4-image/table-rule
- ADD-03:p4-image/tp1-point
- ADD-03:p4-image/tp1-location
- ADD-03:p4-image/tp1-diameter
- ADD-03:p4-image/tp1-window
- ADD-03:p4-image/tp1-duration
- ADD-03:p4-image/tp1-notice
- ADD-03:p4-image/tp2-point
- ADD-03:p4-image/tp2-location
- ADD-03:p4-image/tp2-diameter
- ADD-03:p4-image/tp2-window
- ADD-03:p4-image/tp2-duration
- ADD-03:p4-image/tp2-notice
- ADD-03:p4-image/notes-heading
- ADD-03:p4-image/note1
- ADD-03:p4-image/note2
- ADD-03:p4-image/note3
- ADD-03:p4-image/note4
- ADD-03:p4-image/signatory
- ADD-03:p4-image/stamp
- ADD-03:p4-image/image-footer
- ADD-03:AppA/para2
- ADD-03:AppB/para1
- ADD-03:T1-3/tp-1
- ADD-03:T1-3/tp-2
- ADD-03:T1-3/notes
- ADD-03:T1-3/note(1)
- ADD-03:T1-3/note(2)
- ADD-03:T1-3/note(3)
- ADD-03:T1-3/note(4)
- ADD-03:AppB/para2

## Items

| id | type | provision | target | status | why (first failed check) |
|---|---|---|---|---|---|
| ADD-03/cover/para1 | disposition | ADD-03:cover/para1 |  | evidence_verified |  |
| ADD-03/cover/para2 | disposition | ADD-03:cover/para2 |  | evidence_verified |  |
| ADD-03/1.1 | disposition | ADD-03:1.1 |  | evidence_verified |  |
| ADD-03/cover/para3 | amendment_op | ADD-03:cover/para3 | ADD-03:cover/para3 | interpretation_pending | an annotation that adds obligation is an interpretation of the provision: a person confirms it |
| ADD-03/cover/para3/issue-shutdown | issue | ADD-03:cover/para3 | ADD-03:2.5 | interpretation_pending |  |
| ADD-03/cover/para3/issue-rampup | issue | ADD-03:cover/para3 | ADD-03:5.1 | interpretation_pending |  |
| ADD-03/1.2 | disposition | ADD-03:1.2 |  | interpretation_pending | semantic: no_effect on amendment language: a person must confirm (its words carry 'unless') |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S1: The ADD-03 cover summary requires acknowledgement of receipt in Form 4-A. — evidence verified
- **fact** S2: The cover summary describes the tie-in shutdown application as for the Authority's acceptance, made within eight Working Days of the date of the Addendum; operative clause 2.5 requires a Network Operator letter, applied for not later than eight Working Days before the Proposal Due Date. — evidence verified
- **fact** S3: The cover summary says the new Unavailability Event has no deduction during the Ramp-Up Period; operative clauses 5.1 and 5.2 add event (d) and a no-cure-period rule but no Ramp-Up provision was found in ADD-03 by search. — evidence verified
- **interpretation** S4: The cover summary is descriptive; the changes it lists are made by the operative provisions (Sections 2-5, Appendix A), which are answered in other batches. Its only own effect is the Form 4-A acknowledgement obligation. — needs a person
- **interpretation** S5: Clause 1.2 is an interpretation rule matching how ops are applied (targets read at stage ADD-02); it amends no unit. — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone; NOT clean: 1 provision with amendment language carries no change (0 contradict a change the pattern drafter drafts from their words: invalid; 1 need a person): ADD-03:1.2
- units changed: none
- rows citing them: none
- rows that would be STALE: none
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 0
- clarification entries citing changed units: none
- A3: enters none; leaves none
- programme: 48 activity change(s)

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind06-20261005T173226Z-analysis-001-critic`, route **host**; 4 item(s) reviewed

- **ADD-03/cover/para3** (interpretation_pending): critic agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The cover paragraph is both the provision and the target, which is why the target is flagged as uncertain. This is acceptable for an annotate op, because the only obligation of its own is the Form 4-A acknowledgement. The other listed changes are not made by this paragraph, and the note says so.
  - concern: The adds_obligation effect is an interpretation. A person should confirm it.
  - checked: ADD-03:cover/para3: 'Bidders shall acknowledge receipt in Form 4-A.'
- **ADD-03/cover/para3/issue-shutdown** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The conflict is real on the quoted words. The cover says the Authority's acceptance, with applications within 8 Working Days of the date of the Addendum. Clause 2.5 says a Network Operator letter, with applications at least 8 Working Days before the Proposal Due Date.
  - concern: The payload says 'forward from 10 November 2026'. That date is not in the evidence shown, so it is unverified.
  - concern: The item does not say which provision governs. The cover says the Addendum takes precedence under Vol I 3.2, but that does not settle a cover-versus-operative conflict. Leaving it to the person is correct.
  - checked: ADD-03:cover/para3, ADD-03:2.5
- **ADD-03/cover/para3/issue-rampup** (interpretation_pending): critic DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The cover does say 'no deduction during the Ramp-Up Period'. ADD-03:5.1 as shown adds event (d) with no Ramp-Up wording. This part is supported.
  - concern: The claim that a search of all of ADD-03 found no Ramp-Up exclusion cannot be verified. Only units 5.1 and 5.2 (partial) and the cover are shown.
  - concern: The statement that VOL-V 29.3 covers Table 2-4 parameters only is not supported by any text in the evidence. VOL-V 29.3 is not printed.
  - concern: Without the full ADD-03 text and VOL-V 29.3, the evidence does not show that no Ramp-Up exclusion is in force. The issue may still be worth raising, but its stated basis is not shown.
  - checked: ADD-03:cover/para3, ADD-03:5.1, ADD-03:5.2 quotation
- **ADD-03/1.2** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: no_effect is right in that Clause 1.2 amends no unit. It does fix the stage at which cross-references are read, as amended by Addenda 1 and 2. That is consistent with the ADD-02 stage used here.
  - concern: 'Unless otherwise stated' could be triggered by a later provision. The person should confirm that no ADD-03 clause states a different reading.
  - checked: ADD-03:1.2

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T173952Z-d69e/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T173952Z-d69e --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
