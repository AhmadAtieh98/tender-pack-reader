# Review request: ADD-03, run ADD-03-host-20261005T185308Z-d215

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T18:53:08Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 42e9285d5bfded97…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 5 of 57 provisions accounted for
- resolution (kept apart from coverage): 0 resolved, 5 pending a person, 0 invalid, 52 unaccounted; evidence_verified checks quotations, not meaning
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
| ADD-03/7.2-clar | clarification | ADD-03:7.2 | ADD-03:T5-1 | interpretation_pending | depends on interpretation S-I1: a person must confirm it |
| ADD-03/AppA/para1 | disposition | ADD-03:AppA/para1 |  | interpretation_pending | depends on interpretation S-I3: a person must confirm it |
| ADD-03/7.1 | amendment_op | ADD-03:7.1 | VOL-II:5.5 | insufficient_evidence | missing_information: the proposer declares missing: c46: no A1 register row yet holds the new Clause 5.6 obligation; a person must add one |
| ADD-03/7.3 | amendment_op | ADD-03:7.3 | VOL-II:5.5+ADD-03 | insufficient_evidence | missing_information: the proposer declares missing: c46: no A1 register row yet holds this notification obligation; whether other ADD-03 provisions (another batch) move the Proposal Due Date |
| ADD-03/7.4 | amendment_op | ADD-03:7.4 | VOL-II:5.5+ADD-03 | insufficient_evidence | missing_information: the proposer declares missing: c46: no A1 register row yet holds this Technical Proposal obligation |
| ADD-03/7.2 | amendment_op | ADD-03:7.2 | ADD-03:T5-1 | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(1) vs ADD-03:p4-image/note1 (scope: permanent only vs permanent and temporary incl. cranes and construction equipment); ADD-03:T5-1/note(2) vs ADD-03:p4-image/… |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S-F1: ADD-03:7.1 inserts a new Clause 5.6 in Volume II after Clause 5.5, requiring compliance with the height limits in Table 5-1 (Appendix A), incorporated by reference. — evidence verified
- **fact** S-F2: ADD-03:7.2 states that Table 5-1 is issued in Arabic, that the Arabic text governs, and that the English translation at Appendix B is for convenience only. Appendix B repeats this. — evidence verified
- **fact** S-F3: Arabic note 1 of Table 5-1 in the Appendix A image applies the limits to all permanent and temporary structures, including stacks, cranes and construction equipment. English note (1) in Appendix B covers permanent structures only, including stacks. — evidence verified
- **fact** S-F4: The Arabic Table 5-1 measures height from natural ground level before grading and filling (note 2 and the column heading). English note (2) measures it from finished ground level after grading and filling. — evidence verified
- **fact** S-F5: ADD-03:7.3 requires notice through the Portal, not later than three (3) Working Days before the Proposal Due Date, for any structure, plant or equipment exceeding 30 m. At ADD-02 the Proposal Due Date is Thursday 26 November 2026 (VOL-I:6.1). calculate(relative_date, 3 working days before, VOL-I 2.… — evidence verified
- **assumption** S-A1: The Proposal Due Date of 26 November 2026 (as at ADD-02) is assumed not to be changed by ADD-03 provisions outside this batch. If it is changed, the 7.3 notice date must be recalculated. — needs a person
- **interpretation** S-I1: Under ADD-03:7.2 the Arabic Table 5-1 governs where the two versions differ. So, for Clause 5.6 and for the 30 m threshold in 7.3, the limits would also cover temporary structures, cranes and construction equipment, and height would be measured from natural ground level before grading and filling, … — needs a person
- **interpretation** S-I2: ADD-03:7.3 and 7.4 add bidder obligations tied to the new Clause 5.6. They change no existing text, so they are recorded as adds_obligation annotations on the inserted unit VOL-II:5.5+ADD-03. — needs a person
- **interpretation** S-I3: ADD-03:AppA/para1 introduces the reproduction and restates the precedence that 7.2 sets. It amends nothing itself. — needs a person

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T185308Z-d215/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T185308Z-d215 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
