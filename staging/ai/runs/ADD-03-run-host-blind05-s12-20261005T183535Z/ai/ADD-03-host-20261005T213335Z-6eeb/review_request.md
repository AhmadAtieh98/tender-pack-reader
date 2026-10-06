# Review request: ADD-03, run ADD-03-host-20261005T213335Z-6eeb

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T21:33:35Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 42e9285d5bfded97…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 4 of 57 provisions accounted for
- resolution (kept apart from coverage): 3 resolved, 1 pending a person, 0 invalid, 53 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

## Findings (a person looks at each)

- 1 provision with amendment language carries no change (0 contradict a change the pattern drafter drafts from their words: invalid; 1 need a person): ADD-03:AppB/para1

## Provisions not accounted for (a person treats each)

- ADD-03:cover/para1
- ADD-03:cover/para2
- ADD-03:cover/para3
- ADD-03:1.1
- ADD-03:1.2
- ADD-03:1.3
- ADD-03:2.1
- ADD-03:2.2
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
- ADD-03:p4-image/th-left
- ADD-03:p4-image/th-right
- ADD-03:p4-image/row-a-left
- ADD-03:p4-image/row-a-right
- ADD-03:p4-image/row-b-left
- ADD-03:p4-image/row-b-right
- ADD-03:p4-image/notes-head
- ADD-03:p4-image/note1
- ADD-03:p4-image/note2
- ADD-03:p4-image/note3
- ADD-03:T5-1/a
- ADD-03:T5-1/b
- ADD-03:T5-1/notes
- ADD-03:T5-1/note(1)
- ADD-03:T5-1/note(2)
- ADD-03:T5-1/note(3)

## Items

| id | type | provision | target | status | why (first failed check) |
|---|---|---|---|---|---|
| ADD-03/p4-image/signatory | disposition | ADD-03:p4-image/signatory |  | evidence_verified |  |
| ADD-03/p4-image/stamp | disposition | ADD-03:p4-image/stamp |  | evidence_verified |  |
| ADD-03/AppA/para2 | disposition | ADD-03:AppA/para2 |  | evidence_verified |  |
| ADD-03/p4-image/note3 | row_new | ADD-03:p4-image/note3 | ADD-03:p4-image/note3 | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/AppB/para1 | disposition | ADD-03:AppB/para1 |  | interpretation_pending | semantic: no_effect on amendment language: a person must confirm (its words carry 'provided') |
| ADD-03/p4-image/note2 | row_new | ADD-03:p4-image/note2 | ADD-03:p4-image/note2 | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(2) |
| ADD-03/p4-image/note2-issue | issue | ADD-03:p4-image/note2 | ADD-03:T5-1/note(2) | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(2) |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** F1: The Arabic letter reproduced at Appendix A prints note 3 about notifying the Office before installing any crane on site. — evidence verified
- **fact** F2: The Arabic letter reproduced at Appendix A prints note 2 on the datum from which height is measured. — evidence verified
- **fact** F3: The English translation at Appendix B prints note (2) as measuring height from finished ground level after grading and filling. — evidence verified
- **fact** F4: Section 7 incorporates Table 5-1 into Volume II by reference and states that the Arabic text governs and the English translation is for convenience only. — evidence verified
- **fact** F5: The bottom band of the Appendix A image shows the title 'مدير المكتب' over a drawn signature stroke (left), and an empty oval stamp outline with no legible text (right). — evidence verified
- **fact** F6: Appendix A ends with 'End of reproduction.' and Appendix B opens with a convenience/precedence statement that repeats Clause 7.2. — evidence verified
- **interpretation** I1: Arabic note 3 requires notice to the Northern Region Airspace Safeguarding Office at least thirty (30) days before any crane is installed on the site. It binds the Project Company through Volume II Clause 5.6, which incorporates Table 5-1 by reference. The reading's English translation is only prop… — needs a person
- **interpretation** I2: Arabic note 2 sets the height datum as natural ground level before grading and filling works. The English translation instead says 'finished ground level after grading and filling'. Under Clause 7.2 the Arabic governs, so the Table 5-1 limits are measured from natural (pre-grading) ground level. — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone; NOT clean: 1 provision with amendment language carries no change (0 contradict a change the pattern drafter drafts from their words: invalid; 1 need a person): ADD-03:AppB/para1
- units changed: none
- rows citing them: none
- rows that would be STALE: none
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 0
- clarification entries citing changed units: none
- A3: enters none; leaves none
- programme: 48 activity change(s)

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-s12-20261005T183535Z-analysis-008-critic`, route **host**; 3 item(s) reviewed

- **ADD-03/p4-image/note2** (conflicting): critic agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: Row relies on Arabic governing (7.2), which is a person's decision (I2). The row's own text says the English contradicts it; the conflict with ADD-03:T5-1/note(2) is real.
  - concern: Reading of the image is pending approval; I only have the printed Arabic text, not the crop.
  - concern: The row's mention of the 'Arabic column header' and 'English column header' is not in the evidence shown; I could not verify it.
  - concern: Clause 5.6 and 7.1 incorporation: 7.1 text says Table 5-1 is incorporated by reference; reference to 'Clause 5.6' is not in the evidence shown.
  - checked: ADD-03:p4-image/note2, ADD-03:T5-1/note(2), ADD-03:7.2, ADD-03:7.1
- **ADD-03/p4-image/note2-issue** (conflicting): critic agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The conflict is real: Arabic says natural ground before grading and filling; English says finished ground after grading and filling.
  - concern: The claim about the English column header is not in the evidence shown; I could not verify it.
  - concern: The issue's consequence (English-based designs could exceed limits where fill raises ground) follows from the words, assuming Arabic governs. Which clause governs is a human decision.
  - checked: ADD-03:p4-image/note2, ADD-03:T5-1/note(2), ADD-03:7.2, ADD-03:7.1
- **ADD-03/p4-image/note3** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: Arabic text supports a 30-day prior notice to the Office for any crane installed on the site; the row matches that.
  - concern: Calendar vs Working Days is unstated; the row correctly leaves this open.
  - concern: The Office is named in the row as the Northern Region Airspace Safeguarding Office; the Arabic says only 'المكتب' (the Office). The name comes from 7.1, which is plausible but an inference.
  - concern: The rationale says the note is consistent with English note (3); that English note is not in the evidence shown, so I could not check it.
  - concern: Binding via Clause 5.6 is not shown in the evidence; 7.1 incorporates Table 5-1 by reference.
  - checked: ADD-03:p4-image/note3, ADD-03:7.1, ADD-03:7.2

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T213335Z-6eeb/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T213335Z-6eeb --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
