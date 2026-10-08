# Review request: ADD-03, run ADD-03-host-20261008T054501Z-f368

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (claude-opus-5-5)`; reported `None`
- status **partial**; created 2026-10-08T05:45:01Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build e5d1ff4e390aab4b…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 6 of 52 provisions accounted for
- resolution (kept apart from coverage): 3 resolved, 3 pending a person, 0 invalid, 46 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

## Provisions not accounted for (a person treats each)

- ADD-03:2.1
- ADD-03:2.2
- ADD-03:2.3
- ADD-03:2.4
- ADD-03:2.5
- ADD-03:2.6
- ADD-03:3.1
- ADD-03:3.2
- ADD-03:3.3
- ADD-03:3.4
- ADD-03:4.1
- ADD-03:4.2
- ADD-03:Q15
- ADD-03:Q16
- ADD-03:Q17
- ADD-03:Q18
- ADD-03:Q19
- ADD-03:AppA/para1
- ADD-03:p3-image/r1
- ADD-03:p3-image/r2
- ADD-03:p3-image/r3
- ADD-03:p3-image/hdr-en
- ADD-03:p3-image/hdr-ar
- ADD-03:p3-image/date
- ADD-03:p3-image/ref
- ADD-03:p3-image/to
- ADD-03:p3-image/subject
- ADD-03:p3-image/tender
- ADD-03:p3-image/notes-heading
- ADD-03:p3-image/note1
- ADD-03:p3-image/note2
- ADD-03:p3-image/note3
- ADD-03:p3-image/stamp
- ADD-03:p3-image/signatory
- ADD-03:p3-image/image-footer
- ADD-03:AppA/para2
- ADD-03:AppB/para1
- ADD-03:AppB/para2
- ADD-03:T8-1/1
- ADD-03:T8-1/2
- ADD-03:T8-1/3
- ADD-03:T8-1/notes
- ADD-03:T8-1/note(1)
- ADD-03:T8-1/note(2)
- ADD-03:T8-1/note(3)
- ADD-03:AppB/para3

## Items

| id | type | provision | target | status | why (first failed check) |
|---|---|---|---|---|---|
| ADD-03/disp/cover/para1 | disposition | ADD-03:cover/para1 |  | evidence_verified |  |
| ADD-03/disp/cover/para2 | disposition | ADD-03:cover/para2 |  | evidence_verified |  |
| ADD-03/disp/1.3 | disposition | ADD-03:1.3 |  | evidence_verified |  |
| ADD-03/cover/para3 | amendment_op | ADD-03:cover/para3 | ADD-03:cover/para3 | interpretation_pending | an annotation that adds obligation is an interpretation of the provision: a person confirms it |
| ADD-03/row/ack-4A | row_new | ADD-03:cover/para3 | ADD-03:cover/para3 | interpretation_pending | depends on interpretation S-I2: a person must confirm it |
| ADD-03/issue/cq20 | issue | ADD-03:1.3 | ADD-03:cover/para3 | interpretation_pending |  |
| ADD-03/disp/1.1 | disposition | ADD-03:1.1 |  | interpretation_pending |  |
| ADD-03/disp/1.2 | disposition | ADD-03:1.2 |  | interpretation_pending | depends on interpretation S-I1: a person must confirm it |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S-F1: Volume I Clause 3.2(a) already places the Addenda first, a later Addendum prevailing over an earlier one. — evidence verified
- **fact** S-F2: The cover text says the Addendum responds to clarification requests 15 to 20. — evidence verified
- **fact** S-F3: Clause 1.3 and the Section 5 heading name clarification requests 15 to 19. — evidence verified
- **interpretation** S-I1: Clause 1.2 is a rule for reading the Addendum's own references (to the Clause, Table or Form as amended by Addenda Nos. 1 and 2). It amends no volume unit, and it matches reading targets at previous_stage ADD-02. Whether any provision 'otherwise states' is decided provision by provision in the batc… — needs a person
- **interpretation** S-I2: The cover's 'Bidders shall acknowledge receipt in Form 4-A' is an obligation of the Addendum's own. It is recorded as a register row on the cover unit, as with the same words in the cover texts of Addenda Nos. 1 and 2. — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone
- units changed: none
- rows citing them: none
- rows that would be STALE: none
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 0
- clarification entries citing changed units: none
- A3: enters none; leaves none
- programme: 48 activity change(s)

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-20261008T053735Z-77b2-analysis-001-critic`, route **host**; 4 item(s) reviewed

- **ADD-03/cover/para3** (interpretation_pending): critic agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
  - concern: The quoted obligation 'Bidders shall acknowledge receipt in Form 4-A.' is verbatim in ADD-03:cover/para3, and recording it as an interpretation pending a person is consistent with 'the cover summarises; it does not amend'. Annotating the cover's own procedural sentence is still a reading of a cover unit, and a person must confirm it (S-I2).
  - concern: S-I2 relies on how 'the same words in the cover texts of Addenda Nos. 1 and 2' were treated, but it carries no evidence and those units are not printed here. I cannot verify the precedent.
  - concern: The rationale says the cover's summaries (8.9, Table 8-1, Vol II 4.6, Vol V 12.1 and 39.4, and 'failing which the Proposal will be rejected') are covered by operative provisions in other batches. None of those provisions is printed here. Each cover summary still has to be compared with its operative provision, and any difference reported as for CQ 20.
  - concern: The dependency VOL-IV:F4-A is not printed, so I cannot check that it is the right unit for Form 4-A as it stands at ADD-02.
  - checked: ADD-03:cover/para3: 'Bidders shall acknowledge receipt in Form 4-A.', ADD-03:cover/para3: 'failing which the Proposal will be rejected', S-I2 (no evidence attached)
- **ADD-03/row/ack-4A** (interpretation_pending): critic DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
  - concern: The row's requirement text 'Bidders shall acknowledge receipt of Addendum No. 3 in Form 4-A.' is not verbatim. The words 'of Addendum No. 3' are not in the cover. A1 needs the obligation quoted verbatim ('Bidders shall acknowledge receipt in Form 4-A.'), with any gloss kept separate and labelled.
  - concern: The scope 'Envelope A' is not supported by any evidence shown. No quoted unit puts Form 4-A in Envelope A, so this may be an unsupported placement.
  - concern: The rationale cites ADD-01:AppA/para1 and VOL-I:9.3, but neither is printed or attached as evidence. The row's own evidence list is empty.
  - concern: The proposer decided that VOL-I:9.3's non-responsiveness ('signing or execution of Form 4-A') does not apply to a failure to acknowledge Addendum No. 3 in Form 4-A. Whether that printed consequence reaches the acknowledgement at paragraph 1 of the reissued Form 4-A is a reading for a person (Legal or Bid management). It should be raised as an issue quoting VOL-I:9.3, not settled as 'none_stated'.
  - concern: Same as the annotate item: it depends on S-I2's unevidenced precedent from Addenda 1 and 2.
  - checked: ADD-03:cover/para3: 'Bidders shall acknowledge receipt in Form 4-A.', row requirement text vs cover quotation, row scope 'Envelope A' (no supporting evidence shown), rationale references ADD-01:AppA/para1, VOL-I:9.3 (not printed)
- **ADD-03/issue/cq20** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
  - concern: The difference is real: the cover says 'and responds to clarification requests 15 to 20', while ADD-03:1.3 and the Section 5 heading say 15 to 19. Raising it as an issue with both quotations, leaving it unresolved, follows the rule on cover/operative differences.
  - concern: Clause 1.3 only says requests 15 to 19 'were received before the time stated in Volume I Clause 5.2'. It does not itself say they are answered; the 'responses' wording comes from the Section 5 heading. The issue text should not imply that 1.3 states the answered set.
  - concern: Reading 3 (a response intended but omitted) is really a missing-evidence possibility, not an ambiguity in the words. A person may want that point raised separately with Document control as possible missing content, so the two classes are not merged under 'ambiguous:'.
  - concern: The 'no response to request 20 found' claim rests on a search that is not printed. The ADD-03:H:S5 and VOL-I:5.2 quotations are confirmed only by the controller's verbatim checks, because those units are not in the units shown.
  - concern: The controller's human-owned flag on 'answered' comes from quoted text and readings ('will not be answered', 'not answered'). The issue does not declare any question answered.
  - checked: ADD-03:cover/para3: 'and responds to clarification requests 15 to 20', ADD-03:1.3: 'Clarification requests 15 to 19 were received before the time stated in Volume I Clause 5.2.', ADD-03:H:S5 (controller-verified quotation), VOL-I:5.2 (controller-verified quotation)
- **ADD-03/disp/1.2** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-opus-5-5
  - concern: The provision contains an exception, 'unless otherwise stated'. The controller's semantic check reports that no exception words remain, which looks wrong for these words. Under the shared rules, a no_effect on a provision with exception wording is a person's decision. The item does leave it for a person to confirm, which is right, but the controller's semantic result should not be relied on.
  - concern: Calling this 'no_effect' understates it. Clause 1.2 decides which version every reference in ADD-03 points to (for example Form 4-A as reissued by ADD-01, and Table 8-1). A person may prefer to record it as a reading rule that the other batches depend on, rather than as having no effect.
  - concern: S-I1 has no evidence attached apart from the provision itself. That is acceptable for a reading of this one clause.
  - checked: ADD-03:1.2: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.', controller semantic check record

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261008T054501Z-f368/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261008T054501Z-f368 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
