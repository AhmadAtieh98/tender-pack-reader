# Review request: ADD-03, run ADD-03-host-20261005T184804Z-0589

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T18:48:04Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 42e9285d5bfded97…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 2 of 57 provisions accounted for
- resolution (kept apart from coverage): 1 resolved, 1 pending a person, 0 invalid, 55 unaccounted; evidence_verified checks quotations, not meaning
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
| ADD-03/5.1 | amendment_op | ADD-03:5.1 | VOL-II:3.4 | evidence_verified |  |
| ADD-03/5.2 | amendment_op | ADD-03:5.2 | VOL-II:3.4 | interpretation_pending | an annotation that adds obligation is an interpretation of the provision: a person confirms it |
| ADD-03/5.1-clar | clarification | ADD-03:5.1 | VOL-II:3.4 | insufficient_evidence | missing_information: the proposer declares missing: ESIA Figure 7-2 |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S1: ADD-03 Clause 5.1 deletes 'not more than 5 OU/m³ at the site boundary' in Volume II Clause 3.4 and substitutes a reference to the odour concentration shown for the nearest sensitive receptor in Figure 7-2 of the ESIA, at that receptor; the 98th percentile hourly basis is unchanged. — evidence verified
- **fact** S2: ADD-03 Clause 5.2 requires Bidders to demonstrate compliance with Volume II Clause 3.4, as amended, in the Technical Proposal. — evidence verified
- **fact** S3: Figure 7-2 of the ESIA is not in the evidence build; ADD-03 Q18 says it is available in the data room. The numeric odour concentration now applicable cannot be read from the pack: insufficient evidence. — evidence verified
- **fact** S4: The ADD-03 cover paragraph describes the odour change as being to 'Volume II Clause 3.5', whereas Clause 5.1 names Clause 3.4; VOL-II:3.5 is the noise clause. — evidence verified
- **interpretation** S6: Clause 5.2 adds a submission obligation (demonstrating compliance in the Technical Proposal) attached to VOL-II:3.4 without changing its text; it is recorded as an annotation with effect adds_obligation. — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone
- units changed: VOL-II:3.4
- rows citing them: VOL-II-3.4-01
- rows that would be STALE: VOL-II-3.4-01
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 0
- clarification entries citing changed units: none
- A3: enters none; leaves none
- programme: 49 activity change(s)

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-s12-20261005T183535Z-analysis-003-critic`, route **host**; 1 item(s) reviewed

- **ADD-03/5.2** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The clause says "as amended", which points to some amendment of VOL-II 3.4, probably ADD-03/5.1 (listed as a dependency). The evidence shown does not include 5.1, so I could not check that annotating 3.4 without changing its text is right. If 5.1 amends 3.4, a person should check that this annotation points at the amended version.
  - concern: ADD-03:5.2 has status not_issued in the units. The evidence does not say what that means for whether the obligation takes effect. A person should confirm it.
  - checked: ADD-03:5.2 p2, VOL-II:3.4 p3, controller_validation checks

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T184804Z-0589/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T184804Z-0589 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
