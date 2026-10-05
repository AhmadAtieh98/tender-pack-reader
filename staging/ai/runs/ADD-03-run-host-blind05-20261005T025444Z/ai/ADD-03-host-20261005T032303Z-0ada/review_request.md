# Review request: ADD-03, run ADD-03-host-20261005T032303Z-0ada

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T03:23:03Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 77784d6d270a9e34…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 5 of 54 provisions accounted for
- resolution (kept apart from coverage): 2 resolved, 3 pending a person, 0 invalid, 49 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

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
| ADD-03/7.1 | amendment_op | ADD-03:7.1 | VOL-II:5.5 | evidence_verified |  |
| ADD-03/AppA/para1 | disposition | ADD-03:AppA/para1 |  | evidence_verified |  |
| ADD-03/7.2 | escalation | ADD-03:7.2 | ADD-03:T5-1 | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(1); ADD-03:T5-1/note(2) |
| ADD-03/7.2/issue | issue | ADD-03:7.2 | ADD-03:T5-1 | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(1); ADD-03:T5-1/note(2) |
| ADD-03/7.3 | escalation | ADD-03:7.3 |  | escalated | missing_information: the proposer declares missing: The PDD at ADD-03 (other batches); Whether temporary cranes count as 'equipment' for 7.3 (Arabic note 1) |
| ADD-03/7.4 | escalation | ADD-03:7.4 |  | escalated | missing_information: the proposer declares missing: Approval of the Appendix A Arabic reading |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** F1: ADD-03:7.1 inserts a new Volume II Clause 5.6 after Clause 5.5 requiring compliance with the height limits in Table 5-1, reproduced at Appendix A and incorporated by reference. — evidence verified
- **fact** F2: ADD-03:7.2 states that Table 5-1 is issued in Arabic, the Arabic text governs, and the English translation at Appendix B is for convenience only. AppA/para1 repeats that the Arabic governs. — evidence verified
- **fact** F3: Arabic note 1 of Table 5-1 (Appendix A image, page 4, reading pending) prints the words quoted. The English note (1) at Appendix B prints 'These limits apply to all permanent structures, including stacks.' — evidence verified
- **fact** F4: Arabic note 2 and the Arabic height column heading (Appendix A image, reading pending) print the words quoted. The English note (2) prints 'Height is measured from finished ground level after grading and filling.' and the English column is 'Maximum height (m above finished ground level)'. — evidence verified
- **fact** F5: ADD-03:7.3 requires a Bidder whose Proposal provides for any structure, plant or equipment over 30 m to notify the Authority through the Portal not later than 3 Working Days before the PDD. calculate(relative_date, PDD 2026-11-26 as in force at ADD-02, 3 working days before) gives 2026-11-23 (singl… — evidence verified
- **fact** F6: ADD-03:7.4 requires Bidders to reflect Table 5-1 in the Technical Proposal. — evidence verified
- **assumption** A1: The PDD used for the 7.3 date is 2026-11-26 as in force at ADD-02. Other ADD-03 provisions, outside this batch, may move it. If so, the 7.3 date must be recalculated. — needs a person
- **interpretation** I1: Because the Arabic governs (7.2), Table 5-1 note 1 covers temporary as well as permanent structures, including cranes and construction equipment. This is wider than English note (1), which covers 'permanent structures, including stacks', and wider than the cover note's 'permanent structures'. The l… — needs a person
- **interpretation** I2: Because the Arabic governs, height is measured from natural ground level before grading and filling, not from finished ground level after grading and filling. Where the site is filled, the allowance above finished level shrinks by the fill depth, so the Arabic is the more restrictive reading. — needs a person
- **interpretation** I3: ADD-03:7.3 and 7.4 are free-standing bidder obligations. They do not amend any unit in force at ADD-02, and the inserted Clause 5.6 does not exist until ADD-03 applies, so no annotate target exists. They oblige ('shall'), so they cannot be no_effect. — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone
- units changed: VOL-II:5.5+ADD-03
- rows citing them: none
- rows that would be STALE: none
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 1
  - ADD-03/7.1 [A1]: ADD-03/7.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-II:5.5; a row of the anchor VOL-II:5.5 does not count): 'The following ne…
- clarification entries citing changed units: none
- A3: enters none; leaves none

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-20261005T025444Z-analysis-005-critic`, route **host**; 3 item(s) reviewed

- **ADD-03/7.1** (evidence_verified): critic agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
  - concern: VOL-II:5.5 is only the insertion anchor and stays unchanged, which matches the provision text. The new clause incorporates Table 5-1 by reference, so what it requires depends on the Arabic Appendix A reading, which is still pending. The rationale's description of the crop (zone values, letter reference) is not shown in the printed evidence.
  - checked: ADD-03:7.1, VOL-II:5.5
- **ADD-03/7.2** (conflicting): critic agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The Arabic notes are a pending image reading, and the item says so. My own reading of the Arabic matches the proposer's: note 1 covers permanent and temporary structures including stacks, cranes and construction equipment. Note 2 measures from natural ground before grading and filling.
  - concern: The English notes in the evidence are the permanent-structures note and the finished-ground-level note, so the two conflicts are real.
  - concern: I2's claim that the Arabic is the more restrictive reading holds only where the site is filled. If the site is cut, the effect reverses. The statement should be conditional.
  - concern: Whether 7.2 has any effect depends on the target. T5-1 is not yet in force at ADD-02, so no existing op type can record the precedence. Escalation is a reasonable choice, but it rests on the C22 failure, which is not printed in the evidence.
  - checked: ADD-03:7.2, ADD-03:p4-image/note1, ADD-03:p4-image/note2, ADD-03:T5-1/note(1), ADD-03:T5-1/note(2), ADD-03:T5-1
- **ADD-03/7.2/issue** (conflicting): critic agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The headline 'wider and stricter' overstates the datum point. The Arabic is stricter only if the finished level is above natural ground (fill). The item lists fill depths as missing, which supports this caveat.
  - concern: The references to Q21 and the 7.3 notification of items over 30 m are not backed by evidence shown here.
  - concern: Everything depends on the pending Appendix A Arabic reading, which is a reading and not yet an approved text.
  - checked: ADD-03:7.2, ADD-03:p4-image/note1, ADD-03:p4-image/note2, ADD-03:T5-1/note(1), ADD-03:T5-1/note(2)

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T032303Z-0ada/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T032303Z-0ada --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
