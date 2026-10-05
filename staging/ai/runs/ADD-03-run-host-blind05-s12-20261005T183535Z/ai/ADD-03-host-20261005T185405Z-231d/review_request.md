# Review request: ADD-03, run ADD-03-host-20261005T185405Z-231d

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T18:54:05Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 42e9285d5bfded97…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 5 of 57 provisions accounted for
- resolution (kept apart from coverage): 1 resolved, 4 pending a person, 0 invalid, 52 unaccounted; evidence_verified checks quotations, not meaning
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
| ADD-03/7.2 | amendment_op | ADD-03:7.2 | ADD-03:T5-1 | interpretation_pending | an annotation that interprets is an interpretation of the provision: a person confirms it |
| ADD-03/7.3 | amendment_op | ADD-03:7.3 | VOL-II:5.5+ADD-03 | interpretation_pending | an annotation that adds obligation is an interpretation of the provision: a person confirms it |
| ADD-03/7.4 | amendment_op | ADD-03:7.4 | VOL-II:5.5+ADD-03 | interpretation_pending | an annotation that adds obligation is an interpretation of the provision: a person confirms it |
| ADD-03/AppA/para1 | amendment_op | ADD-03:AppA/para1 | ADD-03:p4-image | interpretation_pending |  |
| ADD-03/7.2-issue-ar-en | issue | ADD-03:7.2 | ADD-03:T5-1 | insufficient_evidence | missing_information: the proposer declares missing: approved reading of region ADD-03-p4-r1 (status pending); the Arabic words are my reading of the crop only |
| ADD-03/7.2-clar-ar-en | clarification | ADD-03:7.2 | ADD-03:T5-1 | insufficient_evidence | missing_information: the proposer declares missing: approved reading of region ADD-03-p4-r1 (status pending) |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S-F1: ADD-03:7.1 inserts a new Volume II Clause 5.6 after Clause 5.5 and prints its full text. — evidence verified
- **fact** S-F2: ADD-03:7.2 states that Table 5-1 is issued in Arabic, the Arabic text governs and the English translation at Appendix B is for convenience only. — evidence verified
- **fact** S-F3: ADD-03:7.3 obliges a Bidder proposing any structure, plant or equipment over 30 m to notify the Authority through the Portal, not later than three Working Days before the Proposal Due Date, of the Table 5-1 zone and the proposed height. — evidence verified
- **fact** S-F4: The Proposal Due Date in force at ADD-02 is Thursday 26 November 2026 (VOL-I:6.1 as amended by ADD-01/2.1). calculate(relative_date, 3 working days before 2026-11-26, deadline) returns Monday 23 November 2026 (VOL-I §2.4, readings do not differ). — evidence verified
- **fact** S-F5: ADD-03:7.4 obliges Bidders to reflect Table 5-1 in the Technical Proposal. — evidence verified
- **fact** S-F6: ADD-03:AppA/para1 introduces the reproduction of Table 5-1 (image region ADD-03-p4-r1) and restates that the Arabic text governs under Section 7; it changes no text of its own. — evidence verified
- **fact** S-F7: The English translation (Appendix B, page 5) gives Note (1) as 'all permanent structures, including stacks' and Note (2) as 'measured from finished ground level after grading and filling'. — evidence verified
- **assumption** S-A2: UNAPPROVED READING by the host model of the native image of ADD-03-p4-r1 (crop sha256 dadbcea9...; the region reading is still PENDING). The column header reads 'متر فوق منسوب الأرض الطبيعية'. Note ١ reads 'تسري هذه الحدود على جميع المنشآت الدائمة والمؤقتة، بما في ذلك المداخن والرافعات ومعدّات الإن… — needs a person
- **assumption** S-A1: For the 7.3 deadline, the Proposal Due Date is taken as it stands at ADD-02 (26 November 2026). No provision in this batch changes it, but provisions of ADD-03 handled in other batches were not checked for a PDD change. — needs a person
- **interpretation** S-I1: My proposed translation of the Arabic, which governs under ADD-03:7.2: the limits apply to permanent AND temporary structures, including stacks, cranes and construction equipment, and height is measured from NATURAL ground level BEFORE grading and filling. The English Appendix B is narrower (perman… — needs a person
- **interpretation** S-I2: The bidder obligations in ADD-03:7.3 and ADD-03:7.4 are recorded as adds_obligation annotations on the new Clause 5.6 (VOL-II:5.5+ADD-03), which incorporates Table 5-1. They change no existing text, so the choice of annotation target is a judgement. — needs a person

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

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T185405Z-231d/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T185405Z-231d --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
