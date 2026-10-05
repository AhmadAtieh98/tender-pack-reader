# Review request: ADD-03, run ADD-03-host-20261005T175300Z-7198

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T17:53:00Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build f826cdeb7fbc262e…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 7 of 70 provisions accounted for
- resolution (kept apart from coverage): 2 resolved, 5 pending a person, 0 invalid, 63 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

## Provisions not accounted for (a person treats each)

- ADD-03:cover/para1
- ADD-03:cover/para2
- ADD-03:cover/para3
- ADD-03:1.1
- ADD-03:1.2
- ADD-03:2.1
- ADD-03:2.2
- ADD-03:2.3
- ADD-03:2.4
- ADD-03:2.5
- ADD-03:2.6
- ADD-03:2.7
- ADD-03:3.1
- ADD-03:3.2
- ADD-03:4.1
- ADD-03:4.2
- ADD-03:5.1
- ADD-03:5.2
- ADD-03:p4-image/hdr-en
- ADD-03:p4-image/hdr-ar
- ADD-03:p4-image/ref
- ADD-03:p4-image/date
- ADD-03:p4-image/subject
- ADD-03:p4-image/tender-ref
- ADD-03:p4-image/table-title
- ADD-03:p4-image/intro
- ADD-03:p4-image/th-point
- ADD-03:p4-image/th-location
- ADD-03:p4-image/th-diameter
- ADD-03:p4-image/th-window
- ADD-03:p4-image/th-duration
- ADD-03:p4-image/th-notice
- ADD-03:p4-image/table-rule
- ADD-03:p4-image/tp1-point
- ADD-03:p4-image/tp1-location
- ADD-03:p4-image/tp1-diameter
- ADD-03:p4-image/tp1-window
- ADD-03:p4-image/tp1-duration
- ADD-03:p4-image/tp1-notice
- ADD-03:p4-image/tp2-point
- ADD-03:p4-image/tp2-location
- ADD-03:p4-image/tp2-diameter
- ADD-03:p4-image/tp2-window
- ADD-03:p4-image/tp2-duration
- ADD-03:p4-image/tp2-notice
- ADD-03:p4-image/notes-heading
- ADD-03:p4-image/note1
- ADD-03:p4-image/note2
- ADD-03:p4-image/note3
- ADD-03:p4-image/note4
- ADD-03:p4-image/signatory
- ADD-03:p4-image/stamp
- ADD-03:p4-image/image-footer
- ADD-03:AppA/para2
- ADD-03:AppB/para1
- ADD-03:T1-3/tp-1
- ADD-03:T1-3/tp-2
- ADD-03:T1-3/notes
- ADD-03:T1-3/note(1)
- ADD-03:T1-3/note(2)
- ADD-03:T1-3/note(3)
- ADD-03:T1-3/note(4)
- ADD-03:AppB/para2

## Items

| id | type | provision | target | status | why (first failed check) |
|---|---|---|---|---|---|
| ADD-03/Q15 | disposition | ADD-03:Q15 |  | evidence_verified |  |
| ADD-03/AppA/para1 | disposition | ADD-03:AppA/para1 |  | evidence_verified |  |
| ADD-03/Q16 | amendment_op | ADD-03:Q16 | VOL-II:3.3 | interpretation_pending | semantic: annotated 'confirms', but the answer adds: a sentence of obligation carries words the annotated units do not print: 'Ozonation shall not be used as the sole means of disinfection.' (adds: used, sole, means) |
| ADD-03/Q18-clar | clarification | ADD-03:Q18 | VOL-V:34.2 | interpretation_pending | depends on interpretation S-Q18-I: a person must confirm it |
| ADD-03/Q20-clar | clarification | ADD-03:Q20 | ADD-03:T1-3 | interpretation_pending | depends on assumption S-AppA-A: a person must confirm it |
| ADD-03/AppA/para1-issue | issue | ADD-03:AppA/para1 | ADD-03:T1-3 | interpretation_pending | depends on assumption S-AppA-A: a person must confirm it |
| ADD-03/Q17 | amendment_op | ADD-03:Q17 | VOL-V:12.3 | insufficient_evidence | missing_information: the proposer declares missing: the wording of Clause 12.3 as amended: the addendum says 'is amended accordingly' and prints no replacement or added text |
| ADD-03/Q18 | amendment_op | ADD-03:Q18 | VOL-II:7.2 | insufficient_evidence | missing_information: the proposer declares missing: whether a shortfall in network inflow during the reliability run is a Relief Event under VOL-V 34.2: the Relief Event list does not name it |
| ADD-03/Q19 | amendment_op | ADD-03:Q19 | VOL-II:7.4 | conflicting | declared_conflicts: the proposer declares: VOL-II:7.4 |
| ADD-03/Q20 | escalation | ADD-03:Q20 | VOL-II:1.3 | escalated | missing_information: the proposer declares missing: the maximum transfer flow for TP-1 and for TP-2: Table 1-3 does not state it in either language |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S-Q15-F: The Authority's response to question 15 states that the Network Operator's ownership has no bearing on any requirement of the RFP Documents. — evidence verified
- **fact** S-Q16-F: The response to question 16 repeats the disinfection options of VOL-II Clause 3.3, says ozonation shall not be the sole means of disinfection and says Clause 3.3 applies. Clause 3.3 already says 'Ozonation alone is not acceptable.' — evidence verified
- **fact** S-Q17-F: The response to question 17 says VOL-V Clause 12.3 'is amended accordingly' but prints no replacement or added wording for the clause. — evidence verified
- **fact** S-Q18-F: The response to question 18 makes no amendment. It says VOL-V Clause 34 applies. Clause 34.2 lists Relief Events and does not name a shortfall in flow delivered by the existing collection network. Clause 34.1 gives an extension of time but no compensation. — evidence verified
- **fact** S-Q19-F: The response to question 19 says the Authority's standard format will be issued only to the Preferred Bidder, and that the asset register shall be kept in the CMMS required by VOL-II 8.2 and submitted before the reliability run under VOL-II 7.2 starts. VOL-II 7.4 requires the asset register not lat… — evidence verified
- **fact** S-Q20-F: Q20 and ADD-03 Clause 2.4 require the temporary works to pass 'the maximum transfer flow stated for each tie-in point in Table 1-3'. The English translation of Table 1-3 (Appendix B) has these columns only: Tie-in point, Location, Existing sewer diameter (mm), Permitted shutdown window, Maximum shu… — evidence verified
- **fact** S-AppA-F: ADD-03 AppA/para1 introduces Appendix A, names its source letter and refers to Section 2.2 for precedence. ADD-03 Clause 2.2 says the Arabic text governs and the English translation is for convenience only. — evidence verified
- **assumption** S-AppA-A: These points come from my own look at the Appendix A image (region ADD-03-p4-r1). The pack's reading of that image is still pending. The Arabic table has six column headers and none of them is a transfer flow. In the TP-2 row the maximum shutdown duration reads ٤ (4) in the Arabic, while the Englis… — needs a person
- **interpretation** S-Q17-I: Read with the response to question 17, Clause 12.3 now means that the Independent Engineer's reasonable costs are shared equally, except costs attributable to any reliability run after the first, which the Project Company bears alone. The exact wording of the amended clause is not printed. — needs a person
- **interpretation** S-Q18-I: The response to question 18 is an Authority interpretation that the relief regime of VOL-V Clause 34 (at most an extension of time) covers an inflow shortfall during the VOL-II 7.2 reliability run. Whether such a shortfall counts as a Relief Event (for example as 'failure of a utility') is not esta… — needs a person
- **interpretation** S-Q19-I: The response to question 19 adds obligations to VOL-II 7.4 for the asset register: it must be kept in the CMMS and submitted before the reliability run starts, which is before PCOD. This brings the 7.4 deadline (sixty days after PCOD) forward for the asset register only. The documentation and manua… — needs a person

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

- critic run `ADD-03-run-host-blind06-20261005T173226Z-analysis-004-critic`, route **host**; 5 item(s) reviewed

- **ADD-03/Q17** (insufficient_evidence): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The response says 'amended accordingly' but prints no wording, so the annotation records substance only; a person may need to draft the clause text.
  - concern: 'Other costs stay shared equally' is an inference. It is implied by 'attributable to any reliability run after the first' but is not stated.
  - concern: Dependency on VOL-II:7.2 is not backed by any quoted text.
  - checked: ADD-03:Q17, VOL-V:12.3
- **ADD-03/Q18** (insufficient_evidence): critic DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The note says relief is subject to notice within five Working Days under VOL-V 34.3. No text of 34.3 is in the evidence, so that detail is unsupported.
  - concern: The 34.1 text (extension of time, no compensation) appears only in the statement evidence, not in the item's own evidence list.
  - concern: Whether a network inflow shortfall falls under 'failure of a utility not caused by the Project Company' is open. The item correctly flags this, but the 'interprets' effect rests on an unconfirmed interpretation.
  - concern: The response makes no amendment. The annotation is reasonable as a record, but the consequence detail goes beyond the evidence.
  - checked: ADD-03:Q18, VOL-II:7.2, VOL-V:34.2, VOL-V:34.1 (quoted)
- **ADD-03/Q19** (conflicting): critic agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
  - concern: The conflict is real on the words. VOL-II 7.4 requires the register not later than 60 days after PCOD. Q19 requires submission before the start of the 7.2 run, and 7.2 says PCOD is not certified until the run is complete, so the run precedes PCOD.
  - concern: It is unclear whether a Q&A response has the power to amend 7.4. A person must decide which governs.
  - concern: The format is issued only to the Preferred Bidder, which makes pre-run submission harder to price at bid stage. This is context, not a conflict.
  - checked: ADD-03:Q19, VOL-II:7.4, VOL-II:8.2, VOL-II:7.2
- **ADD-03/Q20-clar** (interpretation_pending): critic DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The English translation of Table 1-3 lacks a transfer flow column, and that is verifiable. But the Arabic text governs, and the claim that the Arabic has no such column rests only on the proposer's own reading of the image, which is still pending.
  - concern: The interim handling cites existing 1,000 mm and 800 mm sewers and TP-1/TP-2. These figures are not in the evidence shown.
  - concern: Q20 refers to Table 1-3 'at Appendix A', but the English table checked is the Appendix B translation (T1-3, p5). The target is plausible but its link to the cited provision is indirect.
  - checked: ADD-03:Q20, ADD-03:2.4 (quoted), ADD-03:T1-3 header row, S-AppA-A
- **ADD-03/AppA/para1-issue** (interpretation_pending): critic DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The Arabic observations (TP-2 duration ٤ against 6, and the Eid holidays in note 1) cannot be checked from the evidence shown. Only the image crop hash and the proposer's own description are given.
  - concern: Only the English side is verified: TP-2 reads 6 and note (1) mentions Ramadan only. The mismatch itself is unconfirmed.
  - concern: The target T1-3 is the English translation. The governing Arabic unit is ADD-03:p4-image, so the target may not be the right unit for an issue about the Arabic text.
  - concern: The precedence point is supported by AppA/para1 and 2.2, so the issue is worth raising once the reading is approved.
  - checked: ADD-03:AppA/para1, ADD-03:T1-3/tp-2, ADD-03:T1-3/note(1), ADD-03:p4-image (description only), ADD-03:2.2 (quoted)

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T175300Z-7198/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T175300Z-7198 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
