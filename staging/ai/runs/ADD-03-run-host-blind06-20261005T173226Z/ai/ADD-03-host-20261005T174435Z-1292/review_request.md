# Review request: ADD-03, run ADD-03-host-20261005T174435Z-1292

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T17:44:35Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build f826cdeb7fbc262e…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 7 of 70 provisions accounted for
- resolution (kept apart from coverage): 1 resolved, 6 pending a person, 0 invalid, 63 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

## Cover discrepancies (retained; the cover is a summary, not a conflict between operative provisions)

- ADD-03/2.5 (ADD-03:2.5): ADD-03:cover/para3

## Provisions not accounted for (a person treats each)

- ADD-03:cover/para1
- ADD-03:cover/para2
- ADD-03:cover/para3
- ADD-03:1.1
- ADD-03:1.2
- ADD-03:3.1
- ADD-03:3.2
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
- ADD-03:AppA/para1
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
| ADD-03/2.1 | amendment_op | ADD-03:2.1 | VOL-II:1.3 | evidence_verified |  |
| ADD-03/2.4-clarification | clarification | ADD-03:2.4 | ADD-03:T1-3 | interpretation_pending |  |
| ADD-03/2.7-issue | issue | ADD-03:2.7 | ADD-03:T1-3/tp-2 | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/2.3 | amendment_op | ADD-03:2.3 | ADD-03:p4-image | insufficient_evidence | missing_information: the proposer declares missing: An A1 register row for this obligation (C46 need reported by simulate_amendment). |
| ADD-03/2.2 | amendment_op | ADD-03:2.2 | ADD-03:T1-3 | conflicting | declared_conflicts: the proposer declares: ADD-03:T1-3/tp-2; ADD-03:T1-3/note(1) |
| ADD-03/2.7 | amendment_op | ADD-03:2.7 | ADD-03:p4-image | conflicting | declared_conflicts: the proposer declares: ADD-03:T1-3/tp-2 |
| ADD-03/2.4 | escalation | ADD-03:2.4 | ADD-03:T1-3 | escalated | missing_information: the proposer declares missing: The maximum transfer flow for TP-1 and for TP-2 (with units). |
| ADD-03/2.5 | escalation | ADD-03:2.5 |  | escalated | missing_information: the proposer declares missing: Confirmation that the operative 2.5 (Network Operator; 8 WD before PDD) prevails over the cover summary (Authority; within 8 WD of the Addendum date). The ADD-03 issue… |
| ADD-03/2.6 | escalation | ADD-03:2.6 |  | escalated |  |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** F1: ADD-03:2.2 states that Table 1-3 is issued in Arabic, the Arabic text governs and the English translation at Appendix B is for convenience only. — evidence verified
- **fact** F2: For TP-2 the maximum shutdown duration differs between versions: the Arabic Appendix A cell (pending reading) prints ٤ (4); the English Appendix B row prints 6. For TP-1 both print 6 (Arabic ٦). — evidence verified
- **fact** F3: Arabic note 1 of Table 1-3 also excludes shutdowns during the Eid al-Fitr and Eid al-Adha holidays; English note (1) mentions Ramadan only. — evidence verified
- **fact** F4: Table 1-3 (English Appendix B, and the Arabic image which has the same six columns) has columns Tie-in point, Location, Existing sewer diameter, Permitted shutdown window, Maximum shutdown duration and Advance notice; no column or note states a maximum transfer flow. — evidence verified
- **fact** F5: The cover paragraph describes the acceptance as the Authority's and the application period as within eight Working Days of the date of the Addendum; Clause 2.5 says a letter from the Network Operator, applied for not later than eight Working Days before the Proposal Due Date. — evidence verified
- **assumption** A2: Assuming the PDD stays 2026-11-26 (the PDD in force at ADD-02 per simulate_programme), calculate(relative_date, 8 working days before, purpose deadline) gives an application deadline of 2026-11-16 (reading stated_date_excluded; readings_differ false). — needs a person
- **assumption** A1: The Appendix A reading blocks are status 'pending'; I viewed the crop (sha256 f827ab1b...) and it matches them (TP-2 duration cell ٤, windows من ٢٣:٠٠ إلى ٠٥:٠٠ and من ٠١:٠٠ إلى ٠٥:٠٠). This holds only until a person approves the reading. — needs a person
- **interpretation** I1: Under ADD-03:2.2 the governing maximum shutdown duration for TP-2, which ADD-03:2.7 uses as the threshold for rejection, is 4 hours (Arabic), not the 6 hours in the English convenience translation. This is consistent with the TP-2 window 01:00 to 05:00 (4 hours). — needs a person
- **interpretation** I2: ADD-03:2.3 and 2.7 do not change the text of VOL-II:1.3. They add bid-stage obligations or rejection rules that operate on Table 1-3, so they are annotations on Table 1-3 (both versions) and need A1/A3 register rows (C46). — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone
- units changed: VOL-II:1.3
- rows citing them: VOL-II-1.3-01
- rows that would be STALE: VOL-II-1.3-01
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 0
- clarification entries citing changed units: CQ-VOL-III-DRAWINGS
- A3: enters none; leaves none
- programme: 49 activity change(s)

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind06-20261005T173226Z-analysis-002-critic`, route **host**; 7 item(s) reviewed

- **ADD-03/2.2** (conflicting): critic agrees — selected because conflicting, consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The Arabic values (TP-2 duration ٤, Arabic note 1 with the Eid holidays) rest on pending reading blocks and a crop I cannot see. I could only check the text of 2.2, the image caption and AppB/para1.
  - concern: The precedence is stated for Table 1-3 as a whole. The item treats ADD-03:p4-image as the governing unit and ADD-03:T1-3 as the convenience translation. That follows from 2.2 and AppB/para1, but a person should confirm it.
  - concern: The target is T1-3, the English table, while the governing unit is the image. This is a deliberate group target, not a unit that 2.2 names.
  - checked: ADD-03:2.2, ADD-03:p4-image, ADD-03:AppB/para1, ADD-03:T1-3/tp-2
- **ADD-03/2.3** (insufficient_evidence): critic agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: 2.3 cites 'Table 1-3' without naming a unit. Choosing the Arabic image as the target, with the English table as a second target, is an inference that depends on 2.2.
  - concern: The note says both windows agree with English Appendix B. Only the English TP-2 row (01:00 to 05:00) is shown, so the TP-1 window cannot be checked here.
  - concern: The Arabic window readings are pending, and the item itself lists the A1 register row as missing.
  - concern: I2 and the claim that 2.3 does not change VOL-II:1.3 are not supported by any evidence shown.
  - checked: ADD-03:2.3, ADD-03:T1-3/tp-2, reading blocks quoted for tp1-window and tp2-window
- **ADD-03/2.4** (escalated): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The English header row shown has no flow column, which supports the claim. The claim for the Arabic table and for the notes relies on the proposer's own viewing of the image. Only the Arabic duration header is quoted.
  - concern: The English notes are not printed in full in the evidence, so 'no note states a flow' cannot be fully verified here.
  - concern: Escalation is reasonable. An annotate or a derived flow would be unsupported.
  - checked: ADD-03:2.4, ADD-03:T1-3 header row, ADD-03:p4-image/th-duration, ADD-03:Q20
- **ADD-03/2.4-clarification** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The practical_impact says method (a) is the default under 2.6. ADD-03:2.6 is not in the evidence shown, so that statement is unsupported here.
  - concern: The proposed question cites Q20, but this item's own evidence lists only 2.4.
  - checked: ADD-03:2.4, ADD-03:T1-3 header row (F4)
- **ADD-03/2.5** (escalated): critic agrees — selected because conflicting; model claude-sonnet-5-5
  - concern: The 2026-11-16 deadline depends on assumption A2: PDD 2026-11-26 and a Sunday to Thursday working week. The PDD and calendar are not shown. Counting back eight working days on that basis does give 16 November.
  - concern: The Arabic note 3 reading says 'للشركة' (the company's portal). The item equates this with the Network Operator's portal, which is not established by the words quoted.
  - concern: The cover/clause discrepancy is real in the quoted text (Authority versus Network Operator; within 8 WD of the Addendum date versus 8 WD before the PDD). The cover is non-operative and the item says so.
  - checked: ADD-03:2.5, ADD-03:cover/para3, ADD-03:p4-image/note3
- **ADD-03/2.7** (conflicting): critic agrees — selected because conflicting, consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The 4 h versus 6 h conflict for TP-2 depends on a pending Arabic reading of one digit that I cannot verify. Interpretation I1 is pending.
  - concern: 2.7 says 'Table 1-3' without naming a unit. Choosing the Arabic image as target follows from 2.2 but is an inference.
  - concern: The A1/A3 register rows are missing, as the item itself declares.
  - concern: The rejection consequence follows from 2.7's words. A bid relying on 6 h for TP-2 would be rejected only if the Arabic ٤ is confirmed.
  - checked: ADD-03:2.7, ADD-03:2.2, ADD-03:T1-3/tp-2, reading blocks quoted for tp2-duration and tp1-duration
- **ADD-03/2.7-issue** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The statement 'Shutdown programmes must follow the Arabic' is a conclusion that depends on pending interpretation I1 and on the pending Arabic reading.
  - concern: The Eid point rests on the quoted Arabic note 1 reading and on the English note, which is only partly shown. It is not in this item's own evidence list.
  - concern: The target T1-3/tp-2 is the English row, while the governing value is in the Arabic image.
  - checked: ADD-03:2.7, ADD-03:T1-3/tp-2, reading block quoted for tp2-duration, note1 quotations

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T174435Z-1292/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T174435Z-1292 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
