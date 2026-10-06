# Review request: ADD-03, run ADD-03-host-20261005T212318Z-d982

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T21:23:18Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 42e9285d5bfded97…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 3 of 57 provisions accounted for
- resolution (kept apart from coverage): 1 resolved, 2 pending a person, 0 invalid, 54 unaccounted; evidence_verified checks quotations, not meaning
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
- ADD-03:7.3
- ADD-03:7.4
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
| ADD-03/7.1/row | row_new | ADD-03:7.1 | VOL-II:5.5+ADD-03 | interpretation_pending | depends on assumption A2: a person must confirm it |
| ADD-03/7.2 | amendment_op | ADD-03:7.2 | ADD-03:p4-image | interpretation_pending | an annotation that interprets is an interpretation of the provision: a person confirms it |
| ADD-03/7.2/issue | issue | ADD-03:7.2 | ADD-03:T5-1 | interpretation_pending | depends on assumption A2: a person must confirm it |
| ADD-03/7.2/clar | clarification | ADD-03:7.2 | ADD-03:T5-1 | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/7.3/row | row_new | ADD-03:7.3 | ADD-03:7.3 | interpretation_pending | depends on assumption A1: a person must confirm it |
| ADD-03/7.4/row | row_new | ADD-03:7.4 | ADD-03:7.4 | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/AppA/para1 | amendment_op | ADD-03:AppA/para1 | ADD-03:p4-image | interpretation_pending |  |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** F1: ADD-03 Section 7.1 inserts a new Clause 5.6 in Volume II after Clause 5.5, requiring compliance with the height limits in Table 5-1, incorporated by reference. — evidence verified
- **fact** F2: ADD-03 Section 7.2 states that the Arabic text of Table 5-1 governs and the English translation at Appendix B is for convenience only; Appendix A para 1 repeats this. — evidence verified
- **fact** F3: The Arabic Table 5-1 (Appendix A image) prints the height column heading as metres above natural ground level; the English translation (Appendix B) prints 'finished ground level'. — evidence verified
- **fact** F4: Arabic note 2 says height is measured from natural ground level before grading and filling works; English note (2) says from finished ground level after grading and filling. — evidence verified
- **fact** F5: Arabic note 1 applies the limits to all permanent and temporary structures, including stacks, cranes and construction equipment; English note (1) says all permanent structures, including stacks. — evidence verified
- **fact** F6: ADD-03 Section 7.3 requires notification through the Portal not later than three (3) Working Days before the Proposal Due Date; calculate(relative_date, anchor 2026-11-26 = PDD in force at ADD-02, 3 working days, before, purpose deadline) returns 2026-11-23 (stated_date_excluded; readings do not di… — evidence verified
- **assumption** A1: The Proposal Due Date of 26 November 2026 (in force at ADD-02) is not moved by another ADD-03 provision; this batch found no change to Volume I Clause 6.1 in ADD-03, but other ADD-03 provisions belong to other batches. — needs a person
- **assumption** A2: The Arabic readings of the Appendix A image (ADD-03:p4-image/*) are pending approval; the Arabic wording relied on here is that pending reading, which I checked against the image in this session. — needs a person
- **interpretation** I1: Because the Arabic text governs (F2), the Table 5-1 limits are to be read as measured from natural ground level before grading/filling and as applying to temporary structures, cranes and construction equipment as well as permanent structures. This is more onerous than the English translation (e.g. … — needs a person
- **interpretation** I2: Sections 7.3 and 7.4 are free-standing bid-stage obligations of the addendum itself that amend no volume unit; they are held as new register rows on the addendum units. — needs a person

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
- programme: 48 activity change(s)

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-s12-20261005T183535Z-analysis-005-critic`, route **host**; 7 item(s) reviewed

- **ADD-03/7.1** (evidence_verified): critic agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
  - concern: Anchor VOL-II:5.5 is correct: the provision inserts new 5.6 after 5.5 and nothing in 5.5 is changed or removed. The new text matches the quoted clause.
  - checked: ADD-03:7.1, VOL-II:5.5
- **ADD-03/7.2** (interpretation_pending): critic agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The evidence never states that ADD-03:T5-1 is Appendix B. It is inferred from the English table text. A person should confirm it.
  - concern: The Arabic reading (th-left) is pending approval (A2). It does read 'الأرض الطبيعية', natural ground, so F3 follows from it.
  - concern: Section 7.2 and AppA/para1 both support Arabic governing over the English. Whether that precedence settles the specific differences is a human decision.
  - checked: ADD-03:7.2, ADD-03:AppA/para1, ADD-03:p4-image/th-left, ADD-03:T5-1
- **ADD-03/7.2/issue** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The two differences are supported by the quoted readings. Arabic note 1 covers permanent and temporary structures, including cranes and construction equipment. English note (1) covers permanent structures only. Arabic note 2 measures from natural ground before grading and filling. English note (2) measures from finished ground after grading and filling.
  - concern: The claim that cranes in Zone A are limited to 25 m is not backed by any quoted evidence. The Zone A row and its 25 m value are not shown. Verify it against the table.
  - concern: The reference to ADD-03 Q21 is not in the evidence shown.
  - concern: Everything relies on the pending Arabic reading (A2) and on interpretation I1. Both need a person to confirm them.
  - checked: ADD-03:7.2, ADD-03:p4-image/note1, ADD-03:p4-image/note2, ADD-03:T5-1/note(1), ADD-03:T5-1/note(2)
- **ADD-03/7.2/clar** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The gap and the question follow from the quoted Arabic heading and the notes in the related statements.
  - concern: The Zone A 25 m figure is not in the evidence shown.
  - concern: The clarification cut-off date (2026-11-12) and the ADD-03 issue date (2026-11-15) are not in the evidence shown. Treat them as unverified.
  - concern: The proposed question depends on interpretation I1 and on the pending Arabic reading.
  - checked: ADD-03:7.2, ADD-03:p4-image/th-left, ADD-03:p4-image/note1, ADD-03:p4-image/note2
- **ADD-03/7.3/row** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The requirement text is verbatim from ADD-03:7.3.
  - concern: The 23 Nov 2026 date assumes a PDD of 26 Nov 2026 (A1) and that 'Working Days' has no holiday exclusions. Neither the PDD nor the definition of Working Days is shown in the evidence. It is a Thursday under a Mon–Fri week.
  - concern: The note that cranes may count as equipment depends on I1. It is not stated in 7.3 itself.
  - checked: ADD-03:7.3
- **ADD-03/7.4/row** (interpretation_pending): critic DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The assessment 'pass_fail' has no support in ADD-03:7.4. The item itself calls it a guess. It should be left unstated or marked unknown, not set to pass_fail.
  - concern: The requirement text is verbatim. The reading 'on the Arabic text' depends on pending interpretation I1.
  - concern: The link to ADD-03/7.1 is reasonable.
  - checked: ADD-03:7.4
- **ADD-03/AppA/para1** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The paragraph says the Arabic text governs in accordance with Section 7. Annotating the p4-image with 'confirms' is consistent with that.
  - concern: It adds no new obligation. Whether this is a precedence question is for a person to confirm.
  - checked: ADD-03:AppA/para1, ADD-03:p4-image, ADD-03:7.2

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T212318Z-d982/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T212318Z-d982 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
