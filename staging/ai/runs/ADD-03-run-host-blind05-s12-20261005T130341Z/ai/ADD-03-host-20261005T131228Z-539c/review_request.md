# Review request: ADD-03, run ADD-03-host-20261005T131228Z-539c

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T13:12:28Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build e017ad321f216c3e…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 7 of 63 provisions accounted for
- resolution (kept apart from coverage): 3 resolved, 4 pending a person, 0 invalid, 56 unaccounted; evidence_verified checks quotations, not meaning
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
| ADD-03/3.1 | amendment_op | ADD-03:3.1 | VOL-V:1.1 | evidence_verified |  |
| ADD-03/3.2 | amendment_op | ADD-03:3.2 | VOL-V:1.1 | evidence_verified |  |
| ADD-03/4.1 | amendment_op | ADD-03:4.1 | VOL-II:3.1 | evidence_verified |  |
| ADD-03/3.3 | amendment_op | ADD-03:3.3 | VOL-V:29.2 | interpretation_pending | the old words are located in the target, not quoted by the provision: a person checks them |
| ADD-03/3.4 | amendment_op | ADD-03:3.4 | VOL-I:10.3 | interpretation_pending | an annotation that adds obligation is an interpretation of the provision: a person confirms it |
| ADD-03/4.2 | amendment_op | ADD-03:4.2 | VOL-II:S3 | interpretation_pending | an annotation that adds obligation is an interpretation of the provision: a person confirms it |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S-F1: At ADD-02, VOL-V:29.2 fixes indexation at sixty per cent indexed and forty per cent fixed. — evidence verified
- **fact** S-F2: The replacement Clause 29.2 is printed as one quotation that opens in ADD-03:3.3 and closes in its list item ADD-03:3.3(b). — evidence verified
- **fact** S-F3: At ADD-02, Form 4-F has no field for the Indexed Proportion percentage. Its only indexation row reads 'Indexation basis assumed: Per Volume V Clause 29.2'. ADD-03:Q20, which is in another batch, deals with that row. — evidence verified
- **interpretation** S-I1: ADD-03:3.4 and ADD-03:4.2 do not change any printed text. They add a bidder obligation to reflect the Section in a submission. That is recorded as an annotate op with effect adds_obligation on the cited unit (VOL-I:10.3, VOL-II:S3). — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone
- units changed: VOL-II:3.1, VOL-V:1.1, VOL-V:1.1+ADD-03
- rows citing them: VOL-II-3.1-01
- rows that would be STALE: VOL-II-3.1-01
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 1
  - ADD-03/3.2 [A1]: ADD-03/3.2 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-V:1.1; a row of the anchor VOL-V:1.1 does not count): 'The following new …
- clarification entries citing changed units: none
- A3: enters none; leaves none
- programme: 45 activity change(s)

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-s12-20261005T130341Z-analysis-002-critic`, route **host**; 4 item(s) reviewed

- **ADD-03/3.2** (evidence_verified): critic agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
  - concern: The item's target is VOL-V:1.1, but the payload inserts a new unit 1.1A after it, with 1.1 as the anchor. This is consistent with the provision.
  - concern: The Base Date depends on the Proposal Due Date, which this evidence does not give. Nothing in the item computes it, so this is fine.
  - checked: ADD-03:3.2, VOL-V:1.1
- **ADD-03/3.3** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
  - concern: The new text is the single quotation printed across ADD-03:3.3 and ADD-03:3.3(b), with the '29.2' label dropped. It matches word for word, and the old text matches VOL-V:29.2.
  - concern: The provision deletes and replaces the whole clause, so replacing the 60/40 split is correct. The 75% from year 11 is new and follows from (b).
  - concern: Form 4-F has no field for the bidder-stated percentage (S-F3). I could not check this from the units printed here. The item defers it to Q20, so a person should confirm it is handled.
  - concern: The new text uses 'Base Date', which depends on the 1.1A insertion in ADD-03/3.2.
  - checked: ADD-03:3.3, ADD-03:3.3(b), VOL-V:29.2, S-F1, S-F2, S-F3
- **ADD-03/3.4** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The 'shall' obligation is real, and the annotate op with adds_obligation on VOL-I:10.3 follows from the words.
  - concern: The note refers to 'Base Date pricing', which comes from ADD-03/3.1. The evidence printed here does not include 3.1, so I could not check that wording.
  - concern: The VOL-I:10.3 quotation is only the opening of the clause. That is enough to identify the target.
  - checked: ADD-03:3.4, VOL-I:10.3, S-I1
- **ADD-03/4.2** (interpretation_pending): critic agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
  - concern: The only evidence for the target group VOL-II:S3 is its heading, 'SECTION 3 — PROCESS REQUIREMENTS'. The printed evidence does not show the section's content or that it covers the process design submission. The group is still the unit the provision cites.
  - concern: The note's detail on the membrane filtration step and the 0.1 µm pore size comes from ADD-03/4.1. That is not in the evidence printed here, so I could not check it.
  - concern: A person should confirm S-I1, the reading that this is an added obligation rather than a text change.
  - checked: ADD-03:4.2, VOL-II:H:S3, S-I1

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T131228Z-539c/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T131228Z-539c --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
