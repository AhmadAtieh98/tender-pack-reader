# Review request: ADD-03, run ADD-03-host-20261005T180604Z-6291

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T18:06:04Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build f826cdeb7fbc262e…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 8 of 70 provisions accounted for
- resolution (kept apart from coverage): 0 resolved, 8 pending a person, 0 invalid, 62 unaccounted; evidence_verified checks quotations, not meaning
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
| ADD-03/p4-image/tp2-window | disposition | ADD-03:p4-image/tp2-window |  | interpretation_pending | depends on assumption A1: a person must confirm it |
| ADD-03/p4-image/tp2-notice | disposition | ADD-03:p4-image/tp2-notice |  | interpretation_pending | depends on assumption A1: a person must confirm it |
| ADD-03/p4-image/notes-heading | disposition | ADD-03:p4-image/notes-heading |  | interpretation_pending | depends on assumption A1: a person must confirm it |
| ADD-03/p4-image/note2 | disposition | ADD-03:p4-image/note2 |  | interpretation_pending | depends on assumption A1: a person must confirm it |
| ADD-03/p4-image/note3 | disposition | ADD-03:p4-image/note3 |  | interpretation_pending | depends on assumption A1: a person must confirm it |
| ADD-03/p4-image/note4 | disposition | ADD-03:p4-image/note4 |  | interpretation_pending | depends on assumption A1: a person must confirm it |
| ADD-03/p4-image/tp2-duration | escalation | ADD-03:p4-image/tp2-duration | ADD-03:T1-3/tp-2 | conflicting | declared_conflicts: the proposer declares: ADD-03:T1-3/tp-2 |
| ADD-03/p4-image/note1 | escalation | ADD-03:p4-image/note1 | ADD-03:T1-3/note(1) | conflicting | declared_conflicts: the proposer declares: ADD-03:T1-3/note(1) |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** F1: ADD-03 2.2 states that Table 1-3 is issued in Arabic, that the Arabic text governs and that the English translation at Appendix B is for convenience only. — evidence verified
- **fact** F2: ADD-03 2.1 amends Volume II Clause 1.3 so that Table 1-3, reproduced at Appendix A, is incorporated into Volume II by reference. — evidence verified
- **fact** F3: For TP-2 the Arabic Table 1-3 prints a maximum shutdown duration of ٤ (4) hours. The English translation prints 6 hours. — evidence verified
- **fact** F4: Arabic note 1 prohibits shutdowns during Ramadan and also during the Eid al-Fitr and Eid al-Adha holidays. English note (1) mentions only Ramadan. — evidence verified
- **fact** F6: The Arabic cells for the TP-2 window and notice, the notes heading, and notes 2, 3 and 4 have the same content as their English renderings in Appendix B. — evidence verified
- **assumption** F5: At ADD-02 the Arabic reading units and the English T1-3 units all have status not_issued. Because of that, an annotate/precedence op targeting ADD-03:T1-3/tp-2 or ADD-03:T1-3/note(1) cannot be applied: the simulate_amendment dry run reports C22 'targets exist: []'. — needs a person
- **assumption** A1: The pending image readings (status 'pending') correctly transcribe the page-4 image. I compared each one against its crop and the region image, and they agree. — needs a person
- **interpretation** I1: The Appendix A cells and notes are content that ADD-03 itself issues. They amend no unit standing at ADD-02. Their substance enters Volume II through ADD-03 2.1 (another batch), so as provisions they have no separate effect. — needs a person
- **interpretation** I2: Under ADD-03 2.2 the Arabic governs. The binding TP-2 maximum shutdown duration is therefore 4 hours, not 6, and the shutdown prohibition also covers the Eid al-Fitr and Eid al-Adha holidays. The English translation is wrong on both points. — needs a person

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind06-20261005T173226Z-analysis-008-critic`, route **host**; 8 item(s) reviewed

- **ADD-03/p4-image/tp2-window** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The no_effect disposition rests on 2.1 incorporating the table and on I1/A1, which a person must confirm. The Arabic window text matches the English '01:00 to 05:00'.
  - checked: ADD-03:p4-image/tp2-window, ADD-03:T1-3/tp-2, ADD-03:2.1
- **ADD-03/p4-image/tp2-duration** (conflicting): critic agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The conflict is real on the readings shown: Arabic '٤' (4) against English 'Maximum shutdown duration (hours): 6'. 2.2 gives the Arabic precedence and 2.7 makes the Table 1-3 maximum a ground for rejection.
  - concern: The proposer's own rationale says the crop named for this reading (18a85c…) does not show the duration cell. The '٤' reading is therefore not confirmed from its cited crop, and a person should check it against the page image before relying on 4 h.
  - concern: The statements cite the Arabic as governing, but they do not quote the Arabic cell itself beyond the reading. I could not verify the image.
  - checked: ADD-03:p4-image/tp2-duration, ADD-03:T1-3/tp-2, ADD-03:2.2, ADD-03:2.7
- **ADD-03/p4-image/tp2-notice** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: '١٠ أيام عمل' means 10 working days, which matches the English 'Advance notice: 10 Working Days'. The no_effect disposition rests on I1/A1, which a person must confirm.
  - checked: ADD-03:p4-image/tp2-notice, ADD-03:T1-3/tp-2, ADD-03:2.1
- **ADD-03/p4-image/notes-heading** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - checked: ADD-03:p4-image/notes-heading
- **ADD-03/p4-image/note1** (conflicting): critic agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The conflict is real. The Arabic adds 'أو خلال إجازتَي عيد الفطر وعيد الأضحى' (or during the Eid al-Fitr and Eid al-Adha holidays), and English note (1) mentions only Ramadan. 2.2 says the Arabic governs.
  - concern: The Eid holiday dates are not in the evidence, so the prohibited periods cannot be turned into dates here.
  - checked: ADD-03:p4-image/note1, ADD-03:T1-3/note(1), ADD-03:2.2
- **ADD-03/p4-image/note2** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The Arabic matches the English note (2). The note does restrict, so the no_effect wording means only that it amends no ADD-02 unit. Its substance still takes effect through 2.1, and a person should confirm that reading.
  - checked: ADD-03:p4-image/note2, ADD-03:T1-3/note(2), ADD-03:2.1
- **ADD-03/p4-image/note3** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The Arabic matches the English note (3). 'خطة الطوارئ' is rendered 'contingency plan' and 'للشركة' as 'the Network Operator's', which are acceptable. The no_effect disposition means only that no ADD-02 unit is amended. The obligation still enters through 2.1.
  - checked: ADD-03:p4-image/note3, ADD-03:T1-3/note(3), ADD-03:2.1
- **ADD-03/p4-image/note4** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The Arabic matches the English '(4) All times are Riyadh time.'. The no_effect disposition rests on I1/A1, which a person must confirm.
  - checked: ADD-03:p4-image/note4, ADD-03:T1-3/note(4), ADD-03:2.1

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T180604Z-6291/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T180604Z-6291 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
