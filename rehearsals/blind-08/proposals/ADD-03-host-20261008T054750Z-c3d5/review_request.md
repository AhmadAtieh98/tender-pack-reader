# Review request: ADD-03, run ADD-03-host-20261008T054750Z-c3d5

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (claude-opus-5-5)`; reported `None`
- status **partial**; created 2026-10-08T05:47:50Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build e5d1ff4e390aab4b…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 21 of 52 provisions accounted for
- resolution (kept apart from coverage): 1 resolved, 20 pending a person, 0 invalid, 31 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

## Not ready: waiting on another item of the set (status unchanged; promotion waits)

- ADD-03/2.1-row: depends on ADD-03/2.1 (amendment_op, conflicting)
- ADD-03/2.3-row: depends on ADD-03/2.1 (amendment_op, conflicting)
- ADD-03/2.4: depends on ADD-03/2.1 (amendment_op, conflicting)
- ADD-03/2.4-row: depends on ADD-03/2.4, which is not ready
- ADD-03/2.4-issue: depends on ADD-03/2.4, which is not ready
- ADD-03/2.5-row: depends on ADD-03/2.1 (amendment_op, conflicting)
- ADD-03/2.5-issue: depends on ADD-03/2.5-row, which is not ready

## Provisions not accounted for (a person treats each)

- ADD-03:cover/para1
- ADD-03:cover/para2
- ADD-03:cover/para3
- ADD-03:1.1
- ADD-03:1.2
- ADD-03:1.3
- ADD-03:2.3
- ADD-03:2.5
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
| ADD-03/2.6 | amendment_op | ADD-03:2.6 | VOL-I:12.2 | evidence_verified |  |
| ADD-03/2.1-row | row_reading | ADD-03:2.1 | VOL-I:8.9 | interpretation_pending | readiness: not ready (promotion waits): depends on ADD-03/2.1 (amendment_op, conflicting) |
| ADD-03/2.2 | amendment_op | ADD-03:2.2 | ADD-03:p3-image | interpretation_pending |  |
| ADD-03/2.2-issue | issue | ADD-03:2.2 | ADD-03:p3-image/r2 | interpretation_pending | depends on interpretation S-I1: a person must confirm it |
| ADD-03/2.3-row | row_new | ADD-03:2.3 | ADD-03:2.3 | interpretation_pending | readiness: not ready (promotion waits): depends on ADD-03/2.1 (amendment_op, conflicting) |
| ADD-03/2.4 | amendment_op | ADD-03:2.4 | VOL-I:8.9 | interpretation_pending | readiness: not ready (promotion waits): depends on ADD-03/2.1 (amendment_op, conflicting) |
| ADD-03/2.4-row | row_new | ADD-03:2.4 | ADD-03:2.4 | interpretation_pending | readiness: not ready (promotion waits): depends on ADD-03/2.4, which is not ready |
| ADD-03/2.4-issue | issue | ADD-03:2.4 | VOL-I:8.9 | interpretation_pending | readiness: not ready (promotion waits): depends on ADD-03/2.4, which is not ready |
| ADD-03/2.5-row | row_new | ADD-03:2.5 | ADD-03:2.5 | interpretation_pending | readiness: not ready (promotion waits): depends on ADD-03/2.1 (amendment_op, conflicting) |
| ADD-03/2.5-issue | issue | ADD-03:2.5 | ADD-03:2.5 | interpretation_pending | readiness: not ready (promotion waits): depends on ADD-03/2.5-row, which is not ready |
| ADD-03/2.1 | amendment_op | ADD-03:2.1 | VOL-I:8.9 | conflicting | consistency: VOL-I:8.9: ADD-03/2.1, ADD-03/2.4 change the same unit in different ways across the set |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S-F1: The Arabic Table 8-1 (Appendix A, image reading of ADD-03:p3-image, row 2, class 'company incorporated outside the GCC states') prints an issue period of ٥ (5) Working Days. — evidence verified
- **fact** S-F2: The English translation of Table 8-1 (Appendix B, ADD-03:T8-1/2) prints an issue period of 3 Working Days for row 2. — evidence verified
- **fact** S-F3: Section 2.2 states that the Arabic text of Table 8-1 governs and the English translation is for convenience only. — evidence verified
- **fact** S-F4: The cover text says failure to notify Certificate applications leads to rejection. — evidence verified
- **fact** S-F5: Operative Section 2.5 imposes the notification obligation and states no consequence for failure. — evidence verified
- **fact** S-F6: Q16 reduces the issue period in row 2 of Table 8-1 by two Working Days for applications lodged by 22 November 2026. — evidence verified
- **fact** S-F7: Section 2.4 disapplies Section 2.1 for a class of minority members and requires them to submit the undertaking described in Clause 8.9 as issued. — evidence verified
- **interpretation** S-I1: Because S-F3 says the Arabic governs, the row 2 issue period in force may be read as 5 Working Days (Arabic) rather than 3 (English); which figure governs, and therefore the base to which Q16's reduction applies, is for a person to decide. — needs a person
- **interpretation** S-I2: 'Section 2.1 does not apply' is read as disapplying the new Volume I Clause 8.9 (the text Section 2.1 substitutes) for the stated class; the undertaking 'described in Volume I Clause 8.9 as issued' is read as 'a signed undertaking to obtain such licence prior to Financial Close' (VOL-I:8.9 as issue… — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone
- units changed: none
- rows citing them: none
- rows that would be STALE: VOL-I-12.2-01, VOL-I-12.2-02
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 0
- clarification entries citing changed units: none
- A3: enters none; leaves none
- programme: 48 activity change(s)

## Values the proposer supplied for controller fields (ignored)

- {"item": "ADD-03/2.1", "proposer_status": "conflicting", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:2.1 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "interpretation", "ok": true, "detail": "the old words are located in the target, not quoted by 
- {"item": "ADD-03/2.1-row", "proposer_status": "interpretation_pending", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:2.1 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "payload", "ok": true, "detail": "a well-formed row_reading payload", "aspect": "
- {"item": "ADD-03/2.2", "proposer_status": "interpretation_pending", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:2.2 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "evidence ADD-03:2.2 p1", "ok": true, "detail": "verbatim in ADD-03:2.2 at ADD-02", "
- {"item": "ADD-03/2.2-issue", "proposer_status": "interpretation_pending", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:2.2 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "payload", "ok": true, "detail": "a well-formed issue payload", "aspect": "stru
- {"item": "ADD-03/2.3-row", "proposer_status": "interpretation_pending", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:2.3 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "payload", "ok": true, "detail": "a well-formed row_new payload", "aspect": "stru
- {"item": "ADD-03/2.4", "proposer_status": "interpretation_pending", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:2.4 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "evidence ADD-03:2.4 p1", "ok": true, "detail": "verbatim in ADD-03:2.4 at ADD-02", "
- {"item": "ADD-03/2.4-row", "proposer_status": "interpretation_pending", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:2.4 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "payload", "ok": true, "detail": "a well-formed row_new payload", "aspect": "stru
- {"item": "ADD-03/2.4-issue", "proposer_status": "interpretation_pending", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:2.4 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "payload", "ok": true, "detail": "a well-formed issue payload", "aspect": "stru
- {"item": "ADD-03/2.5-row", "proposer_status": "interpretation_pending", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:2.5 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "payload", "ok": true, "detail": "a well-formed row_new payload", "aspect": "stru
- {"item": "ADD-03/2.5-issue", "proposer_status": "interpretation_pending", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:2.5 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "payload", "ok": true, "detail": "a well-formed issue payload", "aspect": "stru
- {"item": "ADD-03/2.6", "proposer_status": "evidence_verified", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:2.6 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "evidence ADD-03:2.6 p1", "ok": true, "detail": "verbatim in ADD-03:2.6 at ADD-02", "aspec

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-20261008T053735Z-77b2-analysis-002-critic`, route **host**; 8 item(s) reviewed

- **ADD-03/2.1** (conflicting): critic agrees — selected because conflicting, uncertain_target, uncertain_target: old words located in the target; model claude-opus-5-5
  - concern: Q15 ('an undertaking is no longer accepted') is used to support the removal of the undertaking option, but Q15's text is not printed in this request, so I could not check it. The substitution does not need it: the words 'is deleted and replaced by the following' are enough.
  - concern: The controller's 'conflicting' flag treats ADD-03/2.4 as changing VOL-I:8.9 'in different ways'. As printed, 2.4 does not rewrite the text of 8.9. It disapplies Section 2.1 for one class of member. That makes it an exception to scope, not a competing text change. A person should decide whether the conflict is real. It should not block the substitution text, which is correct.
  - concern: The rationale says the undertaking is 'now kept only for the Section 2.4 class'. That depends on interpretation S-I2, which is pending. It should be labelled as an interpretation, not stated as the effect of the op.
  - concern: I checked the replace_text old and new values against the quotations, and they are correct. Leaving out the printed number '8.9' in the new text is disclosed.
  - checked: ADD-03:2.1 text, VOL-I:8.9 text_before_addendum (ADD-02), payload old/new vs quotations, controller consistency record
- **ADD-03/2.1-row** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-opus-5-5
  - concern: The rejection consequence is quoted correctly from the new 8.9. It applies to 'each such member', meaning a member incorporated outside the Kingdom. Whether it also covers the 2.4 class's undertaking is still open (see ADD-03/2.4-row). The note should not suggest that the class split is settled.
  - concern: The row's current requirement text was not read. The proposer says so. The row stays incomplete until a person revises it, including any date rule tied to Financial Close.
  - checked: ADD-03:2.1 text, consequence quote 'A Proposal that does not include the evidence required by this Clause for each such member shall be rejected.'
- **ADD-03/2.2** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
  - concern: Treating ADD-03:p3-image as Table 8-1 follows from 'reproduced at Appendix A ... and forms part of Volume I'. However, the image reading is pending. The detail described from the crop (three rows ٣/٥/٨, three notes, the Office letter ref and date, an empty stamp circle) is not in the units shown, apart from the title and row 2, so I could not check it.
  - concern: The precedence 'over' ADD-03:T8-1 assumes T8-1 is the Appendix B translation. T8-1 is not printed in the units, so I could not confirm this. Applying 'The Arabic text governs.' still needs a person to confirm it.
  - concern: The stamp circle is described as empty, but nothing is raised about it. A person may want to note whether the table is authenticated as 'issued by the Office'. I make no finding on this.
  - checked: ADD-03:2.2 text, ADD-03:p3-image title text, ADD-03:p3-image/r2 cells
- **ADD-03/2.2-issue** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
  - concern: Row 2 showing ٥ is confirmed by ADD-03:p3-image/r2 cell 'مدة الإصدار (أيام عمل)': '٥'. The English figure 3 is verified only by the controller record. T8-1/2 is not printed in the units.
  - concern: The Q16 quotation in S-F6 (reduction of two Working Days for applications lodged by 22 November 2026) is not among the units printed, and the controller records no check of it. I could not verify it.
  - concern: The issue rightly leaves open which figure applies, even though 2.2 states that the Arabic governs. Applying a printed precedence rule is still a person's call, and the Arabic reading itself is pending.
  - concern: The claim that rows 1 and 3 agree with the translation cannot be checked here.
  - checked: ADD-03:p3-image/r2 cells, ADD-03:2.2 text, controller evidence record for ADD-03:T8-1/2
- **ADD-03/2.3-row** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
  - concern: The date note says the period is 'counted from receipt of a complete application (Table 8-1 Note 1)'. That paraphrases a note that is not printed here, and it differs from the 2.2 rationale ('counting starts the Working Day after receipt of a complete application'). The note should be quoted verbatim from Table 8-1, or left unresolved.
  - concern: The row's dependencies leave out ADD-03/2.2-issue, even though the note relies on the row 2 discrepancy.
  - concern: Recording 'none_stated' for the consequence is right: 2.3 prints none. Treating the Office's undertaking as a lead time rather than a bidder deadline is a fair reading of the words.
  - checked: ADD-03:2.3 text
- **ADD-03/2.4-row** (interpretation_pending): critic DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
  - concern: The rationale says the undertaking's content is quoted from VOL-I:8.9 'as issued' (text_as_issued). The only text printed, and the only one the controller checked, is VOL-I:8.9's effective text at ADD-02 ('verbatim in VOL-I:8.9 at ADD-02'). Section 2.4 refers to Clause 8.9 'as issued'. Nothing shown confirms that ADD-01 and ADD-02 left 8.9 unchanged. The quote has to be checked against the as-issued text.
  - concern: 'assessment': 'pass_fail' is given even though the row records consequence 'none_stated' and leaves open whether the rejection words of the new 8.9 reach this class. 'pass_fail' suggests an assessed outcome that the evidence does not establish.
  - concern: ADD-03/2.4 (the op) and ADD-03/2.4-issue are referred to but not printed in this batch, so I could not check them.
  - concern: The scope paraphrases 'is to hold' as 'holding'. The reading of 'Section 2.1 does not apply' (S-I2) is rightly left pending.
  - checked: ADD-03:2.4 text, VOL-I:8.9 text_before_addendum (ADD-02), controller evidence record for VOL-I:8.9
- **ADD-03/2.5-row** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
  - concern: The rationale says Q16's 22 November lodging date 'falls one Working Day before' the 23 November deadline. That count was not produced by calculate, and the Q16 text is not printed here. The figure should come from calculate, or be removed.
  - concern: The PDD value (2026-11-26) and the calculate result appear only in the note. I cannot check them against the units shown.
  - concern: 'issues': [] is empty, even though the interpretation note points to ADD-03/2.5-issue. The row should link that issue. With the cover and the operative text in disagreement, confidence 'high' may overstate how settled the consequence is.
  - concern: Recording 'none_stated' for the consequence matches the operative words of 2.5.
  - checked: ADD-03:2.5 text, date rule text 'not later than three (3) Working Days before the Proposal Due Date'
- **ADD-03/2.5-issue** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
  - concern: The cover quotation ('failing which the Proposal will be rejected') is verified only by the controller record. ADD-03:cover/para3 is not printed in the units.
  - concern: The item handles the conflict correctly: it reports both quotations, does not resolve which governs, and names Legal as the owner.
  - checked: ADD-03:2.5 text, controller evidence record for ADD-03:cover/para3

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261008T054750Z-c3d5/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261008T054750Z-c3d5 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
