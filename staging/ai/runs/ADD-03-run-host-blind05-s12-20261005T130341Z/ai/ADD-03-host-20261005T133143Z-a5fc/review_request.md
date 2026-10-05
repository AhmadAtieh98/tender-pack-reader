# Review request: ADD-03, run ADD-03-host-20261005T133143Z-a5fc

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T13:31:43Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build e017ad321f216c3e…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 8 of 63 provisions accounted for
- resolution (kept apart from coverage): 0 resolved, 8 pending a person, 0 invalid, 55 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

## Cover discrepancies (retained; the cover is a summary, not a conflict between operative provisions)

- ADD-03/p4-image/note1 (ADD-03:p4-image/note1): ADD-03:cover/para3

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
- ADD-03:p4-image/table-qualifier
- ADD-03:p4-image/col-lighting
- ADD-03:p4-image/col-height
- ADD-03:p4-image/col-description
- ADD-03:p4-image/col-zone
- ADD-03:p4-image/rowA-zone
- ADD-03:p4-image/rowA-description
- ADD-03:p4-image/rowA-height
- ADD-03:p4-image/rowA-lighting
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
| ADD-03/p4-image/rowB-zone | disposition | ADD-03:p4-image/rowB-zone |  | interpretation_pending | depends on assumption S-A1: a person must confirm it |
| ADD-03/p4-image/rowB-description | disposition | ADD-03:p4-image/rowB-description |  | interpretation_pending | depends on assumption S-A1: a person must confirm it |
| ADD-03/p4-image/rowB-lighting | disposition | ADD-03:p4-image/rowB-lighting |  | interpretation_pending | depends on assumption S-A1: a person must confirm it |
| ADD-03/p4-image/notes-heading | disposition | ADD-03:p4-image/notes-heading |  | interpretation_pending | depends on assumption S-A1: a person must confirm it |
| ADD-03/p4-image/note3 | disposition | ADD-03:p4-image/note3 |  | interpretation_pending | depends on assumption S-A1: a person must confirm it |
| ADD-03/p4-image/rowB-height | disposition | ADD-03:p4-image/rowB-height |  | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(2) |
| ADD-03/p4-image/note1 | escalation | ADD-03:p4-image/note1 | ADD-03:T5-1/note(1) | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(1) |
| ADD-03/p4-image/note2 | escalation | ADD-03:p4-image/note2 | ADD-03:T5-1/note(2) | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(2); ADD-03:T5-1 |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S-F1: ADD-03 Section 7.1 inserts Volume II Clause 5.6, which incorporates Table 5-1 (reproduced at Appendix A) by reference. — evidence verified
- **fact** S-F2: ADD-03 Section 7.2 says that the Arabic text of Table 5-1 governs and that the English translation at Appendix B is for convenience only. — evidence verified
- **fact** S-F4: Arabic note 1 applies the limits to all permanent AND temporary structures, including stacks, cranes and construction equipment. English note (1) of the Appendix B translation says 'all permanent structures, including stacks'. — evidence verified
- **fact** S-F5: Arabic note 2 measures height from natural ground level before grading and filling, and the Arabic height column reads metres above natural ground level. English note (2) says 'finished ground level after grading and filling', and the English column reads 'm above finished ground level'. — evidence verified
- **assumption** S-A1: Tool metadata, not document words: the readings of region ADD-03-p4-r1 have status 'pending'. The p4-image units and ADD-03:T5-1/* are issued by ADD-03, and simulate_amendment found no target in force at ADD-02 for an op on ADD-03:T5-1/note(1) (C22 'targets exist: []'). I assume the pending reading… — needs a person
- **interpretation** S-I1: The Appendix A reading blocks are the content of Table 5-1, which enters the RFP through the Section 7.1 insertion (handled in another batch). By themselves they amend no unit in force at ADD-02, so where the Arabic agrees with the English translation they need no op of their own. — needs a person
- **interpretation** S-I2: Under 7.2, governing Arabic notes 1 and 2 differ in substance from the English convenience translation. Note 1 is wider: it adds temporary structures, cranes and construction equipment. Note 2 uses a different datum: natural ground before grading, not finished ground after it. The engine cannot rec… — needs a person

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-s12-20261005T130341Z-analysis-008-critic`, route **host**; 8 item(s) reviewed

- **ADD-03/p4-image/rowB-zone** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: Relies on S-A1 (Arabic reading still pending approval) and on 7.1 being handled in another batch; the 7.1 text itself is quoted but not printed among the units.
  - checked: ADD-03:p4-image/rowB-zone, ADD-03:7.1 quotation in S-F1
- **ADD-03/p4-image/rowB-description** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The T5-1/b English cell is cited only through the item's own quotation ('The remainder of the site'), not printed in units; it matches the Arabic 'باقي مساحة الموقع'.
  - concern: Depends on pending approval of the Arabic reading.
  - checked: ADD-03:p4-image/rowB-description, ADD-03:T5-1/b cell quotation, S-F1
- **ADD-03/p4-image/rowB-height** (conflicting): critic agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
  - concern: The value 40 matches the English cell, so no_effect for the cell is consistent. The datum difference is real (natural ground vs finished ground) and is correctly kept as a conflict via note2. A person must resolve it.
  - concern: The col-height unit is cited but not printed among the units; its reading is quoted in the note2 item.
  - checked: ADD-03:p4-image/rowB-height, ADD-03:T5-1/b cell '40', ADD-03:p4-image/note2, ADD-03:T5-1/note(2)
- **ADD-03/p4-image/rowB-lighting** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: Depends on pending approval of the Arabic reading. The English cell is only quoted in the item.
  - checked: ADD-03:p4-image/rowB-lighting, ADD-03:T5-1/b 'Required for any part exceeding 30 m'
- **ADD-03/p4-image/notes-heading** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - checked: ADD-03:p4-image/notes-heading
- **ADD-03/p4-image/note1** (conflicting): critic agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The divergence is real. Arabic adds temporary structures, cranes and construction equipment; English note (1) has only permanent structures and stacks. Under 7.2 the Arabic governs.
  - concern: The proposer's claim that an op is rejected (C22) is tool metadata and cannot be checked from the evidence printed here.
  - concern: The Arabic reading is still pending approval.
  - checked: ADD-03:p4-image/note1, ADD-03:T5-1/note(1), ADD-03:7.2 quotation, ADD-03:cover/para3 quotation
- **ADD-03/p4-image/note2** (conflicting): critic agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The divergence is real. Arabic measures from natural ground before grading and filling; English measures from finished ground after grading and filling. Under 7.2 the Arabic governs.
  - concern: The C22 rejection is tool metadata and is not verifiable from the evidence printed here. The Arabic reading is still pending approval.
  - checked: ADD-03:p4-image/note2, ADD-03:T5-1/note(2), ADD-03:p4-image/col-height quotation, ADD-03:7.2 quotation
- **ADD-03/p4-image/note3** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The Arabic and English notes agree: notice at least 30 days before any crane is erected. no_effect is on the basis that the obligation enters through 7.1, but the obligation is real and a person should confirm it is carried.
  - concern: The Arabic reading is pending approval.
  - checked: ADD-03:p4-image/note3, ADD-03:T5-1/note(3) quotation, ADD-03:7.1 quotation

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T133143Z-a5fc/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T133143Z-a5fc --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
