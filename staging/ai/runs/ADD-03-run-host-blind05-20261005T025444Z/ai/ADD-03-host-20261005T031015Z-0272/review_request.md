# Review request: ADD-03, run ADD-03-host-20261005T031015Z-0272

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T03:10:15Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 77784d6d270a9e34…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 7 of 54 provisions accounted for
- resolution (kept apart from coverage): 2 resolved, 5 pending a person, 0 invalid, 47 unaccounted; evidence_verified checks quotations, not meaning
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
| ADD-03/3.1 | amendment_op | ADD-03:3.1 | VOL-V:1.1 | evidence_verified |  |
| ADD-03/3.3-clar | clarification | ADD-03:3.3 | VOL-IV:F4-F | evidence_verified |  |
| ADD-03/4.1 | amendment_op | ADD-03:4.1 | VOL-II:3.1 | evidence_verified |  |
| ADD-03/3.2 | amendment_op | ADD-03:3.2 | VOL-V:1.1 | interpretation_pending | depends on assumption S-A1: a person must confirm it |
| ADD-03/3.4 | amendment_op | ADD-03:3.4 | VOL-I:10.3 | interpretation_pending | an annotation that adds obligation is an interpretation of the provision: a person confirms it |
| ADD-03/4.2 | amendment_op | ADD-03:4.2 | VOL-II:S3 | interpretation_pending | an annotation that adds obligation is an interpretation of the provision: a person confirms it |
| ADD-03/3.3 | amendment_op | ADD-03:3.3 | VOL-V:29.2 | insufficient_evidence | missing_information: the proposer declares missing: Limb (b) of the replacement (ADD-03:3.3(b)) is not carried by this op: see the escalation ADD-03/3.3(b). |
| ADD-03/3.3(b) | escalation | ADD-03:3.3(b) | VOL-V:29.2 | escalated | depends on interpretation S-I1: a person must confirm it |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S-F1: At ADD-02, VOL-V:29.2 fixes the indexed proportion at 60% CPI-indexed and 40% fixed. — evidence verified
- **fact** S-F2: The replacement Clause 29.2 quoted in ADD-03:3.3 opens a quotation that is not closed in ADD-03:3.3; it continues in list item ADD-03:3.3(b), which ends with the closing quotation mark. — evidence verified
- **fact** S-F3: At ADD-02, Form 4-F has no field where the Bidder states the Indexed Proportion percentage. Its only indexation field reads 'Indexation basis assumed: Per Volume V Clause 29.2'. — evidence verified
- **assumption** S-A1: The inserted Clause 1.1A is stored without its printed number '1.1A', in the same way that VOL-V:1.1 stores its text without its label. The new unit id is engine-assigned (VOL-V:1.1+ADD-03), so the printed number 1.1A is not held in the unit text. — needs a person
- **interpretation** S-I1: The whole replacement text of VOL-V:29.2 is the text quoted in ADD-03:3.3 (after the label '29.2') followed by limb (b) in ADD-03:3.3(b). The engine checks inserted words per provision, so ADD-03/3.3 carries the ADD-03:3.3 portion only and limb (b) still has to be appended by a person. Until then, … — needs a person
- **interpretation** S-I2: ADD-03:3.4 adds an obligation to reflect Section 3 of ADD-03 in the Financial Model submitted under VOL-I:10.3. It changes no text of VOL-I:10.3. — needs a person
- **interpretation** S-I3: ADD-03:4.2 adds an obligation to reflect Section 4 of ADD-03 (membrane filtration) in the process design submitted under Volume II Section 3. It changes no text of Volume II Section 3. — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone
- units changed: VOL-II:3.1, VOL-V:1.1
- rows citing them: VOL-II-3.1-01
- rows that would be STALE: VOL-II-3.1-01
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 0
- clarification entries citing changed units: none
- A3: enters none; leaves none
- programme: 1 activity change(s)

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-20261005T025444Z-analysis-002-critic`, route **host**; 6 item(s) reviewed

- **ADD-03/3.2** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
  - concern: The printed number 1.1A is not held in the stored text (S-A1). A person should confirm this convention.
  - concern: The Base Date depends on the Proposal Due Date in force. The item correctly does not compute it.
  - checked: ADD-03:3.2, VOL-V:1.1
- **ADD-03/3.3** (insufficient_evidence): critic agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
  - concern: The op leaves VOL-V:29.2 ending in '; and' until limb (b) is appended. The effective text is incomplete in the meantime, as S-I1 says.
  - concern: The old text is located in the target, not quoted by the provision. The old words match VOL-V:29.2 exactly, but a person must confirm that 'deleted and replaced' means the whole clause.
  - concern: The change is substantive. It moves from a fixed 60/40 split to a Bidder-chosen 50-70% in the first ten years, plus a Base Date indexation start. The text is stored without the '29.2' label, in the same way as S-A1.
  - concern: The claim that the engine rejects limb (b) under C21/C22 is not visible in the evidence shown. Only the dry-run result is asserted.
  - checked: ADD-03:3.3, VOL-V:29.2, ADD-03:3.3(b)
- **ADD-03/3.3(b)** (escalated): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: ADD-03:3.3(b) does contain limb (b), with 75% from year 11 and the balance fixed, and the closing quote. The text supports the escalation.
  - concern: The engine rejections (C22, C21) are asserted by the proposer. They are not shown in the evidence.
  - concern: A person must append limb (b) to 29.2, or 29.2 stays incomplete.
  - concern: The (a)/(b) split leaves a gap. Limb (a) ends at the tenth year of operations, and limb (b) starts at the eleventh. Nothing in the evidence shows a gap in coverage, but a person should confirm the operations-year counting.
  - checked: ADD-03:3.3(b), ADD-03:3.3, VOL-V:29.2
- **ADD-03/3.3-clar** (evidence_verified): critic agrees — selected because uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
  - concern: Only one Form 4-F field, 'Indexation basis assumed: Per Volume V Clause 29.2', is shown in the evidence. The claim that none of the 20 members is a field for the Indexed Proportion cannot be checked from what is printed.
  - concern: The gap is real on the evidence shown. Clause 29.2(a) refers to a percentage stated in Form 4-F, and the only indexation field points back to Clause 29.2.
  - concern: ADD-03 provisions outside this batch might reissue Form 4-F. The proposer admits this was not checked.
  - concern: The interim handling is a suggestion for a person to decide.
  - checked: ADD-03:3.3, VOL-IV:F4-F/indexation-basis-assumed
- **ADD-03/3.4** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The words 'shall reflect this Section 3' do impose an obligation without changing the text of VOL-I:10.3.
  - concern: The note mentions 'Base Date pricing'. That comes from ADD-03/3.1, which is not in the evidence shown.
  - concern: Whether the obligation is 'adds_obligation' or 'no_effect' is an interpretation. A person must confirm it.
  - checked: ADD-03:3.4, VOL-I:10.3
- **ADD-03/4.2** (interpretation_pending): critic agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
  - concern: The note's detail about a membrane filtration step with pore size not exceeding 0.1 µm comes from ADD-03 Section 4.1. That is not in the evidence shown, so it cannot be verified here.
  - concern: The target VOL-II:S3 is a group. The evidence is only its heading. The obligation attaches to the design submission, not to any text.
  - concern: Whether the obligation is 'adds_obligation' or 'no_effect' is an interpretation. A person must confirm it.
  - checked: ADD-03:4.2, VOL-II:H:S3

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T031015Z-0272/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T031015Z-0272 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
