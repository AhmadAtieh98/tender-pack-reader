# Review request: ADD-03, run ADD-03-host-20261005T184400Z-be27

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T18:44:00Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 42e9285d5bfded97…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 7 of 57 provisions accounted for
- resolution (kept apart from coverage): 3 resolved, 4 pending a person, 0 invalid, 50 unaccounted; evidence_verified checks quotations, not meaning
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
| ADD-03/3.1 | amendment_op | ADD-03:3.1 | VOL-V:1.1 | evidence_verified |  |
| ADD-03/3.2 | amendment_op | ADD-03:3.2 | VOL-V:1.1 | evidence_verified |  |
| ADD-03/4.1 | amendment_op | ADD-03:4.1 | VOL-II:3.1 | evidence_verified |  |
| ADD-03/3.3 | amendment_op | ADD-03:3.3 | VOL-V:29.2 | interpretation_pending | the old words are located in the target, not quoted by the provision: a person checks them |
| ADD-03/3.3-form | clarification | ADD-03:3.3 | VOL-IV:F4-F | interpretation_pending |  |
| ADD-03/3.4 | amendment_op | ADD-03:3.4 | VOL-I:10.3 | interpretation_pending | an annotation that adds obligation is an interpretation of the provision: a person confirms it |
| ADD-03/4.2 | amendment_op | ADD-03:4.2 | VOL-II:S3 | interpretation_pending | an annotation that adds obligation is an interpretation of the provision: a person confirms it |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S1: ADD-03:3.1 prints a quoted deletion/substitution pair for Volume V Clause 1.1; the deleted words occur once in VOL-V:1.1 at ADD-02. — evidence verified
- **fact** S2: ADD-03:3.2 inserts a new Clause 1.1A (definition of Base Date) in Volume V after Clause 1.1, with its full text quoted. — evidence verified
- **fact** S3: ADD-03:3.3 deletes Volume V Clause 29.2 and replaces it; the quoted replacement opens in ADD-03:3.3 and closes at the end of list item ADD-03:3.3(b). — evidence verified
- **fact** S4: Form 4-F at ADD-02 contains an 'Indexation basis assumed' field pre-filled 'Per Volume V Clause 29.2' and no field in which a Bidder states an Indexed Proportion percentage. — evidence verified
- **fact** S5: ADD-03:4.1 prints a quoted deletion/substitution pair for Volume II Clause 3.1; the substituted text prints the micro sign 'µm'. — evidence verified
- **interpretation** S6: ADD-03:3.4 and ADD-03:4.2 change no text; they add a submission obligation (reflect Section 3 in the Financial Model under VOL-I 10.3; reflect Section 4 in the process design under VOL-II Section 3), recorded as adds_obligation annotations on the cited targets. — needs a person

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
- programme: 53 activity change(s)

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-s12-20261005T183535Z-analysis-002-critic`, route **host**; 5 item(s) reviewed

- **ADD-03/3.2** (evidence_verified): critic agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
  - concern: Minor: the new definition is inserted after VOL-V:1.1, which is the Availability Payment definition. This matches the provision's 'after Clause 1.1'.
  - concern: The Base Date is not computed, which is correct, since the Proposal Due Date is not in the evidence.
  - checked: ADD-03:3.2, VOL-V:1.1
- **ADD-03/3.3** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
  - concern: The printed 3.3 text ends at '(a)...; and'. Part (b) and the closing 'balance remain fixed' come from ADD-03:3.3(b), which is not in the units list. The controller verified it as verbatim, so the full replacement is supported.
  - concern: The 60/40 split is removed and replaced by a Bidder-stated 50–70% for years 1–10 and 75% from year 11. 'Deleted and replaced' supports replacing the whole of 29.2, so the old text matches the whole target.
  - concern: A person should confirm the old words match the target, as the controller flags.
  - checked: ADD-03:3.3, ADD-03:3.3(b) (quoted in evidence), VOL-V:29.2
- **ADD-03/3.3-form** (interpretation_pending): critic DOES NOT agree — selected because uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
  - concern: The claim that Form 4-F has no field for the percentage is not verifiable from the evidence shown. Only one member field is quoted ('Indexation basis assumed: Per Volume V Clause 29.2'). The VOL-IV:F4-F group and its '20 members' are not printed.
  - concern: The claim that ADD-03 Section 3 does not amend Form 4-F is not shown either. Only 3.2, 3.3 and 3.4 are printed, and no unit says Form 4-F is untouched.
  - concern: The quoted evidence does show that the replacement 29.2 refers to a percentage 'stated by the Bidder in Form 4-F'. It also shows an indexation field that merely points to Clause 29.2. The ambiguity is plausible but not proven.
  - concern: The interim handling (state the percentage against the 'Indexation basis assumed' field) is a suggestion, not something the text supports.
  - checked: ADD-03:3.3, VOL-IV:F4-F/indexation-basis-assumed (quoted)
- **ADD-03/3.4** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: 'Shall reflect' is obligation wording with no text change, so an annotate with adds_obligation fits.
  - concern: The obligation applies to 'this Section 3', which includes the Base Date and Indexed Proportion changes. Its scope depends on the S6 interpretation, which a person must confirm.
  - checked: ADD-03:3.4, VOL-I:10.3
- **ADD-03/4.2** (interpretation_pending): critic agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
  - concern: The target is the group VOL-II:S3, evidenced only by its heading 'SECTION 3 — PROCESS REQUIREMENTS'. This matches the cited 'Volume II Section 3'.
  - concern: The content of ADD-03 Section 4 is not shown, so what the obligation covers cannot be checked.
  - concern: The adds_obligation effect depends on the S6 interpretation, which a person must confirm.
  - checked: ADD-03:4.2, VOL-II:H:S3

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T184400Z-be27/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T184400Z-be27 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
