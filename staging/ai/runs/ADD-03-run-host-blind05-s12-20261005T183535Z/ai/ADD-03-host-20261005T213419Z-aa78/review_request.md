# Review request: ADD-03, run ADD-03-host-20261005T213419Z-aa78

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T21:34:19Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 42e9285d5bfded97…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 8 of 57 provisions accounted for
- resolution (kept apart from coverage): 0 resolved, 8 pending a person, 0 invalid, 49 unaccounted; evidence_verified checks quotations, not meaning
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
| ADD-03/p4-image/th-left | disposition | ADD-03:p4-image/th-left |  | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/p4-image/th-left/issue | issue | ADD-03:p4-image/th-left | ADD-03:T5-1 | interpretation_pending | depends on interpretation I2: a person must confirm it |
| ADD-03/p4-image/th-right | disposition | ADD-03:p4-image/th-right |  | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/p4-image/row-a-left/disposition | disposition | ADD-03:p4-image/row-a-left |  | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/p4-image/row-a-left | row_new | ADD-03:p4-image/row-a-left | ADD-03:p4-image/row-a-left | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/p4-image/row-a-right/disposition | disposition | ADD-03:p4-image/row-a-right |  | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/p4-image/row-a-right | row_new | ADD-03:p4-image/row-a-right | ADD-03:p4-image/row-a-right | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/p4-image/row-b-left/disposition | disposition | ADD-03:p4-image/row-b-left |  | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/p4-image/row-b-left | row_new | ADD-03:p4-image/row-b-left | ADD-03:p4-image/row-b-left | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/p4-image/row-b-right | disposition | ADD-03:p4-image/row-b-right |  | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/p4-image/notes-head | disposition | ADD-03:p4-image/notes-head |  | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/p4-image/note1/disposition | disposition | ADD-03:p4-image/note1 |  | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/p4-image/note1 | row_new | ADD-03:p4-image/note1 | ADD-03:p4-image/note1 | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/p4-image/note1/issue | issue | ADD-03:p4-image/note1 | ADD-03:T5-1/note(1) | interpretation_pending | depends on interpretation I3: a person must confirm it |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** F1: ADD-03 Section 7.2 states that Table 5-1 is issued in Arabic and that the Arabic text governs; the English translation at Appendix B is for convenience only. — evidence verified
- **fact** F2: ADD-03 Section 7.1 inserts new Volume II Clause 5.6 requiring compliance with the height limits in Table 5-1, reproduced at Appendix A and incorporated by reference. — evidence verified
- **fact** F3: The Arabic column heading of the height column in Appendix A prints the datum as metres above natural ground level. — evidence verified
- **fact** F4: The English translation (Appendix B) prints the height column as metres above finished ground level. — evidence verified
- **fact** F5: Arabic note 1 of Appendix A extends the limits to all permanent and temporary structures including stacks, cranes and construction equipment; English note (1) of Appendix B mentions only permanent structures including stacks. — evidence verified
- **fact** F6: Appendix A row A prints Zone A (the part of the site within 1,500 m of the eastern site boundary) with maximum height 25 and warning lighting required; row B prints Zone B (remainder of the site) with maximum height 40 and warning lighting required for any part exceeding 30 m. — evidence verified
- **interpretation** I1: The Appendix A cells and notes are the governing content of Table 5-1 that new Volume II Clause 5.6 (ADD-03:7.1, another batch) incorporates; they amend no volume unit themselves (no_effect for the amendment engine), so their obligations are recorded as register rows on the addendum's own units (ro… — needs a person
- **interpretation** I2: Because the Arabic text governs (F1), heights in Table 5-1 are measured above natural ground level (F3), not finished ground level as the English convenience translation prints (F4). — needs a person
- **interpretation** I3: Because the Arabic text governs (F1), the Table 5-1 limits apply to temporary structures, cranes and construction equipment as well as permanent structures and stacks (F5), wider than English note (1). — needs a person

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-s12-20261005T183535Z-analysis-007-critic`, route **host**; 14 item(s) reviewed

- **ADD-03/p4-image/th-left** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - checked: ADD-03:p4-image/th-left
- **ADD-03/p4-image/th-left/issue** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The consequence about site filling reducing available height is an inference. It is not printed in the evidence, though it follows from the datum difference.
  - concern: The quote shown for 7.2 is only 'The Arabic text governs.' The 'convenience only' wording for Appendix B is cited in F1 but is not in the quoted span.
  - checked: ADD-03:p4-image/th-left, ADD-03:T5-1, ADD-03:7.2
- **ADD-03/p4-image/th-right** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - checked: ADD-03:p4-image/th-right
- **ADD-03/p4-image/row-a-left/disposition** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - checked: ADD-03:p4-image/row-a-left, ADD-03:7.1
- **ADD-03/p4-image/row-a-left** (interpretation_pending): critic agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The cell text alone does not tie the cell to Zone A. That link rests on row alignment in the image crops, which the printed text does not show.
  - checked: ADD-03:p4-image/row-a-left, ADD-03:p4-image/row-a-right, ADD-03:7.1
- **ADD-03/p4-image/row-a-right/disposition** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - checked: ADD-03:p4-image/row-a-right, ADD-03:7.1
- **ADD-03/p4-image/row-a-right** (interpretation_pending): critic agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The 25 m limit depends on the natural-ground-level datum (I2), which is a pending human decision. The row correctly notes the conflict with the English text.
  - checked: ADD-03:p4-image/row-a-right, ADD-03:p4-image/th-left, ADD-03:7.1
- **ADD-03/p4-image/row-b-left/disposition** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - checked: ADD-03:p4-image/row-b-left, ADD-03:7.1
- **ADD-03/p4-image/row-b-left** (interpretation_pending): critic agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The reading merges the lighting cell and the height cell into one string. Assigning 40 as the height and 30 m as the lighting threshold follows from the crops, not from the text alone.
  - checked: ADD-03:p4-image/row-b-left, ADD-03:p4-image/row-b-right, ADD-03:p4-image/th-left, ADD-03:7.1
- **ADD-03/p4-image/row-b-right** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - checked: ADD-03:p4-image/row-b-right
- **ADD-03/p4-image/notes-head** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - checked: ADD-03:p4-image/notes-head
- **ADD-03/p4-image/note1/disposition** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - checked: ADD-03:p4-image/note1, ADD-03:7.1
- **ADD-03/p4-image/note1** (interpretation_pending): critic agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The row's target is its own provision. The English counterpart is only cited in the confidence reason. This is acceptable, but the Arabic/English difference is carried by the separate issue item.
  - checked: ADD-03:p4-image/note1, ADD-03:T5-1/note(1), ADD-03:7.1
- **ADD-03/p4-image/note1/issue** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The link to the crane and lifting content of the Technical Proposal is an inference and is not shown in the evidence.
  - checked: ADD-03:p4-image/note1, ADD-03:T5-1/note(1), ADD-03:7.2

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T213419Z-aa78/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T213419Z-aa78 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
