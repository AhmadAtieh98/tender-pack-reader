# Review request: ADD-03, run ADD-03-host-20261005T132051Z-592a

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T13:20:51Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build e017ad321f216c3e…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 5 of 63 provisions accounted for
- resolution (kept apart from coverage): 0 resolved, 5 pending a person, 0 invalid, 58 unaccounted; evidence_verified checks quotations, not meaning
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
| ADD-03/7.3 | amendment_op | ADD-03:7.3 | VOL-II:5.5+ADD-03 | interpretation_pending | an annotation that adds obligation is an interpretation of the provision: a person confirms it |
| ADD-03/7.4 | amendment_op | ADD-03:7.4 | VOL-II:5.5+ADD-03 | interpretation_pending | an annotation that adds obligation is an interpretation of the provision: a person confirms it |
| ADD-03/AppA/para1 | amendment_op | ADD-03:AppA/para1 | ADD-03:p4-image | interpretation_pending |  |
| ADD-03/7.1 | amendment_op | ADD-03:7.1 | VOL-II:5.5 | insufficient_evidence | missing_information: the proposer declares missing: The Arabic Table 5-1 readings (region ADD-03-p4-r1) are pending approval; the content of the incorporated table rests on them. |
| ADD-03/7.2-issue | issue | ADD-03:7.2 | ADD-03:T5-1 | insufficient_evidence | missing_information: the proposer declares missing: Approval of the pending Arabic readings of region ADD-03-p4-r1. |
| ADD-03/7.2 | amendment_op | ADD-03:7.2 | ADD-03:p4-image | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(1); ADD-03:T5-1/note(2); ADD-03:T5-1 |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S-F1: ADD-03 Section 7.1 inserts a new Clause 5.6 in Volume II after Clause 5.5, requiring compliance with the height limits in Table 5-1 (Appendix A), incorporated by reference. — evidence verified
- **fact** S-F2: ADD-03 Section 7.2 and Appendix A state that the Arabic text of Table 5-1 governs and the English translation at Appendix B is for convenience only. — evidence verified
- **fact** S-F3: Arabic note 1 (image reading, status pending) says the limits apply to permanent AND temporary structures, including stacks, cranes and construction equipment; English note (1) says permanent structures, including stacks. — evidence verified
- **fact** S-F4: Arabic note 2 and the Arabic height column header measure height from natural ground level before grading and filling; English note (2) and the English column header say finished ground level after grading and filling. — evidence verified
- **fact** S-F5: The zone heights agree between the renderings: Arabic Zone A 25 and Zone B 40 (Arabic-Indic numerals), English Zone A 25 and Zone B 40. — evidence verified
- **fact** S-F6: The image readings of region ADD-03-p4-r1 that hold the Arabic Table 5-1 have reading status 'pending' (not approved). — evidence verified
- **interpretation** S-I1: Because the Arabic text governs, new Clause 5.6 binds the Project Company to height limits that cover temporary structures, cranes and construction equipment and are measured from natural ground level before grading; the English translation (Appendix B) and the cover summary ('limiting the height o… — needs a person
- **interpretation** S-I2: Sections 7.3 and 7.4 are bid-stage obligations on Bidders that do not amend any existing clause; they are recorded as adds_obligation annotations on the new Clause 5.6 (VOL-II:5.5+ADD-03), the unit that carries Table 5-1 into the RFP. Section 7.4 might instead be tied to VOL-I:9.7 (Technical Propos… — needs a person

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-s12-20261005T130341Z-analysis-005-critic`, route **host**; 6 item(s) reviewed

- **ADD-03/7.1** (insufficient_evidence): critic agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
  - concern: The insertion itself is quoted verbatim and the anchor VOL-II:5.5 is correct (new 5.6 after 5.5).
  - concern: The content of the incorporated Table 5-1 depends on Arabic readings that are still pending approval, so the obligation's substance is not settled.
  - concern: The 7.1 text says Table 5-1 is 'reproduced at Appendix A', while the provision text shown only states Arabic/English versions elsewhere; I could not view the crop itself.
  - checked: ADD-03:7.1, VOL-II:5.5, ADD-03:p4-image, ADD-03:7.2
- **ADD-03/7.2** (conflicting): critic agrees — selected because conflicting, consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: 7.2 says the Arabic text of Table 5-1 governs, so the annotation recording precedence of the Arabic image over the English T5-1 follows from the words.
  - concern: The target ADD-03:p4-image is not cited by 7.2; the link is an inference (Arabic image = Arabic text), which a person should confirm.
  - concern: The conflicts between Arabic and English (scope of note 1, datum in note 2) rest on pending, unapproved readings of the image; the evidence shown includes only the readings' words, not the crop.
  - concern: The 'English translation at Appendix B' is called ADD-03:T5-1 on page 5; the mapping of Appendix B to T5-1 is assumed.
  - checked: ADD-03:7.2, ADD-03:p4-image, ADD-03:T5-1, ADD-03:p4-image/note1, ADD-03:T5-1/note(1)
- **ADD-03/7.3** (interpretation_pending): critic agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: 7.3 text is verbatim and imposes a bid-stage notification duty; attaching it to the new Clause 5.6 is an interpretive choice because 7.3 cites no unit.
  - concern: How the 30 m is measured depends on the governing Arabic datum (natural ground), which rests on pending readings.
  - concern: The deadline (3 Working Days before the Proposal Due Date) is not computed; the proposal says so.
  - concern: 7.3 refers to 'Table 5-1 zone', which assumes the zones are those in the pending Arabic reading.
  - checked: ADD-03:7.3, ADD-03:7.1, ADD-03:7.2, VOL-II:5.5
- **ADD-03/7.4** (interpretation_pending): critic agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: 7.4 is verbatim; it does not cite any clause, so tying it to new Clause 5.6 rather than VOL-I:9.7 is an interpretation to confirm.
  - concern: What must be 'reflected' is the governing Arabic table, whose reading is still pending.
  - concern: The Q21 link is relied on in S-I2 but Q21 is not among the units printed here, so I could not check it.
  - checked: ADD-03:7.4, ADD-03:7.1, ADD-03:7.2
- **ADD-03/AppA/para1** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The paragraph says the Arabic text governs in accordance with Section 7, which matches the 'confirms' effect.
  - concern: Target ADD-03:p4-image and the other target T5-1 are inferred rather than named in the paragraph.
  - concern: The cited reading 'rowA-height' (٢٥) does not itself support precedence; it is only context, and it is pending.
  - concern: This duplicates 7.2's precedence; a person should confirm both rather than treat them as independent.
  - checked: ADD-03:AppA/para1, ADD-03:7.2, ADD-03:p4-image, ADD-03:T5-1
- **ADD-03/7.2-issue** (insufficient_evidence): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The quoted Arabic and English notes do differ: notes 1 and 2 differ in scope (temporary, cranes) and datum (natural vs finished ground), and 7.2 says the Arabic governs.
  - concern: The Arabic readings are pending and not approved, so the stated difference is provisional; the controller marks it insufficient_evidence.
  - concern: The issue says 'cranes and construction equipment' follow from Arabic note 1; this is true on the reading quoted, but the English note's 'including stacks' is also in the Arabic, so only the additions differ.
  - concern: The statement that the cover summary understates scope relies on S-I1, an interpretation that needs human confirmation, and on cover/para3, which is not printed in the units shown.
  - checked: ADD-03:7.2, ADD-03:p4-image/note1, ADD-03:T5-1/note(1), ADD-03:p4-image/note2, ADD-03:T5-1/note(2)

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T132051Z-592a/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T132051Z-592a --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
