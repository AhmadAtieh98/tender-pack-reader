# Review request: ADD-03, run ADD-03-host-20261005T131541Z-b560

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T13:15:41Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build e017ad321f216c3e…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 2 of 63 provisions accounted for
- resolution (kept apart from coverage): 0 resolved, 2 pending a person, 0 invalid, 61 unaccounted; evidence_verified checks quotations, not meaning
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
- ADD-03:p4-image/rowB-zone
- ADD-03:p4-image/rowB-description
- ADD-03:p4-image/rowB-height
- ADD-03:p4-image/rowB-lighting
- ADD-03:p4-image/notes-heading
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
| ADD-03/5.1-clar | clarification | ADD-03:5.1 | VOL-II:3.4 | interpretation_pending |  |
| ADD-03/5.2 | amendment_op | ADD-03:5.2 | VOL-II:3.4 | insufficient_evidence | missing_information: the proposer declares missing: The value against which compliance must be demonstrated (ESIA Figure 7-2) is not in the evidence build. |
| ADD-03/5.1 | amendment_op | ADD-03:5.1 | VOL-II:3.4 | conflicting | declared_conflicts: the proposer declares: ADD-03:cover/para3 names 'Volume II Clause 3.5' for the odour change; operative Clause 5.1 and Q18 name Clause 3.4 (3.5 is the noise clause) |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S1: ADD-03 Clause 5.1 prints a deletion and substitution in Volume II Clause 3.4: the words 'not more than 5 OU/m³ at the site boundary' are deleted and replaced by a reference to the odour concentration for the nearest sensitive receptor in Figure 7-2 of the ESIA; the 98th percentile hourly basis is s… — evidence verified
- **fact** S2: VOL-II:3.4 as it stands at ADD-02 is active and contains the deleted words exactly once (simulate_amendment C23). — evidence verified
- **fact** S3: ADD-03 Clause 5.2 obliges Bidders to demonstrate compliance with VOL-II Clause 3.4 as amended in the Technical Proposal; it prints no change of words in any unit. — evidence verified
- **fact** S4: The numeric odour limit now applying is not printed in the pack: ADD-03 Q18 says it is shown in Figure 7-2 of the ESIA in the data room, and search_evidence found no unit of the ESIA or Figure 7-2 in the evidence build (only references to it). — evidence verified
- **fact** S5: The ADD-03 cover summary describes the odour change as made to 'Volume II Clause 3.5', whereas operative Clause 5.1 and Q18 name Clause 3.4; VOL-II:3.5 is the noise clause. — evidence verified
- **interpretation** S6: Clause 5.2 adds a submission obligation tied to VOL-II:3.4 (as amended) and is best recorded as an annotate op with effect adds_obligation on VOL-II:3.4, rather than a text change or no_effect. — needs a person

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-s12-20261005T130341Z-analysis-003-critic`, route **host**; 2 item(s) reviewed

- **ADD-03/5.1** (conflicting): critic agrees — selected because conflicting; model claude-sonnet-5-5
  - concern: Real conflict: the ADD-03 cover paragraph 3 names Volume II Clause 3.5 (the noise clause) for the odour change, while operative Clause 5.1 and Q18 name Clause 3.4. The conflict is only declared by the proposer. The cover text is not printed in the evidence, so I could not check it. The operative clause is unambiguous and the old words match VOL-II:3.4, so targeting 3.4 follows from the text, but a person should resolve the cover discrepancy.
  - concern: The new limit is a cross-reference to ESIA Figure 7-2. Its numeric value is not in the evidence. The substitution also moves the compliance point from the site boundary to the nearest sensitive receptor. The effective limit cannot be determined from the evidence shown.
  - concern: The unchanged 98th percentile hourly basis follows from the second sentence of 5.1 and from the retained tail of 3.4.
  - checked: ADD-03:5.1, VOL-II:3.4, controller_validation previous_value/proposed_value/evidence checks
- **ADD-03/5.2** (insufficient_evidence): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: Clause 5.2 prints no change of words, so an annotate op with effect adds_obligation on VOL-II:3.4 is a reasonable reading. It is an interpretation (S6) that a person must confirm.
  - concern: 5.2 refers to 3.4 'as amended'. It therefore depends on 5.1, and 5.1 is itself in conflict with the cover paragraph that names Clause 3.5. If 5.1 is resolved differently, 5.2's target may change.
  - concern: The value to be demonstrated (ESIA Figure 7-2) is not in the evidence. The obligation can be recorded, but its content cannot be checked. The controller's insufficient_evidence status is appropriate.
  - checked: ADD-03:5.2, VOL-II:3.4, ADD-03:5.1, controller_validation

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T131541Z-b560/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T131541Z-b560 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
