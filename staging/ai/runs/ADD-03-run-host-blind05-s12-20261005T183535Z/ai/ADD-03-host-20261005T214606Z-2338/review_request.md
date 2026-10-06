# Review request: ADD-03, run ADD-03-host-20261005T214606Z-2338

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T21:46:06Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 42e9285d5bfded97…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 6 of 57 provisions accounted for
- resolution (kept apart from coverage): 0 resolved, 6 pending a person, 0 invalid, 51 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

## Findings (a person looks at each)

- 3 provisions with amendment language carry no change (0 contradict a change the pattern drafter drafts from their words: invalid; 3 need a person): ADD-03:T5-1/a, ADD-03:T5-1/b, ADD-03:T5-1/note(3)

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

## Items

| id | type | provision | target | status | why (first failed check) |
|---|---|---|---|---|---|
| ADD-03/T5-1/a | disposition | ADD-03:T5-1/a |  | interpretation_pending | semantic: no_effect on amendment language: a person must confirm (its words carry 'Required') |
| ADD-03/T5-1/b | disposition | ADD-03:T5-1/b |  | interpretation_pending | semantic: no_effect on amendment language: a person must confirm (its words carry 'Required') |
| ADD-03/T5-1/notes | disposition | ADD-03:T5-1/notes |  | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/T5-1/note(1)/issue | issue | ADD-03:T5-1/note(1) | ADD-03:p4-image/note1 | interpretation_pending | depends on assumption A1: a person must confirm it |
| ADD-03/T5-1/note(1)/clar | clarification | ADD-03:T5-1/note(1) | ADD-03:p4-image/note1 | interpretation_pending | depends on interpretation I2: a person must confirm it |
| ADD-03/T5-1/note(2)/issue | issue | ADD-03:T5-1/note(2) | ADD-03:p4-image/note2 | interpretation_pending | depends on assumption A1: a person must confirm it |
| ADD-03/T5-1/note(2)/clar | clarification | ADD-03:T5-1/note(2) | ADD-03:p4-image/note2 | interpretation_pending | depends on interpretation I2: a person must confirm it |
| ADD-03/T5-1/note(3)/row | row_new | ADD-03:T5-1/note(3) | ADD-03:T5-1/note(3) | interpretation_pending | depends on assumption A1: a person must confirm it |
| ADD-03/T5-1/note(3) | disposition | ADD-03:T5-1/note(3) |  | insufficient_evidence | dependencies: unknown ids ['ADD-03/T5-1/note(3)/row'] |
| ADD-03/T5-1/note(1) | disposition | ADD-03:T5-1/note(1) |  | conflicting | declared_conflicts: the proposer declares: ADD-03:p4-image/note1 |
| ADD-03/T5-1/note(2) | disposition | ADD-03:T5-1/note(2) |  | conflicting | declared_conflicts: the proposer declares: ADD-03:p4-image/note2; ADD-03:p4-image/th-left |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** F1: ADD-03 Clause 7.2 states that Table 5-1 is issued in Arabic, the Arabic text governs and the English translation at Appendix B is provided for convenience only. — evidence verified
- **fact** F2: Appendix B itself states that the translation is for convenience only and the Arabic text at Appendix A governs. — evidence verified
- **fact** F3: ADD-03 Clause 7.1 inserts Volume II Clause 5.6, which incorporates Table 5-1 as reproduced at Appendix A (not Appendix B). — evidence verified
- **fact** F4: The Arabic Table 5-1 (Appendix A image, p4) prints for Zone A (أ): 25, within 1,500 m of the eastern site boundary, lighting required (مطلوبة); for Zone B (ب): remainder of the site, 40, lighting required for any part exceeding 30 m. These values match the English rows a and b. — evidence verified
- **fact** F5: Arabic note 1 applies the limits to all permanent AND temporary structures, including stacks/chimneys (المداخن), cranes (الرافعات) and construction equipment (معدّات الإنشاء); English note (1) says 'all permanent structures, including stacks' and omits temporary structures, cranes and construction … — evidence verified
- **fact** F6: Arabic note 2 measures height from natural ground level (منسوب الأرض الطبيعية) BEFORE grading and filling (قبل أعمال التسوية والردم), and the Arabic height column heading reads metres above natural ground level; English note (2) and the English column heading use finished ground level AFTER grading… — evidence verified
- **fact** F7: Arabic note 3 requires the Office to be notified at least thirty (30) days before any crane is installed at the site, matching English note (3). — evidence verified
- **assumption** A1: The pending Arabic readings of ADD-03:p4-image (note1, note2, note3, th-left, row cells) are accurate; they agree with the image crop I viewed, but no reading of region ADD-03-p4-r1 is yet approved. — needs a person
- **interpretation** I1: Because the Arabic text governs and the English is for convenience only, the Appendix B translation units have no independent effect on the Volumes; the governing content of Table 5-1 is the Arabic table incorporated through new Volume II Clause 5.6 (ADD-03:7.1), which belongs to other batches. — needs a person
- **interpretation** I2: Where the English translation departs from the Arabic (note 1 scope; note 2 and the column heading datum), the Arabic prevails: the height limits apply also to temporary structures, cranes and construction equipment, and height is measured from natural ground level before grading and filling. Bidde… — needs a person
- **interpretation** I3: Note (3) is a free-standing post-award obligation (notice to the Office at least 30 days before crane erection) that amends no volume unit; the party who gives notice is not named (passive voice); it applies through Clause 5.6 to the Project Company. — needs a person

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-s12-20261005T183535Z-analysis-009-critic`, route **host**; 11 item(s) reviewed

- **ADD-03/T5-1/a** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: Controller semantic check flagged 'Required' as amendment-like language; a person must confirm no_effect.
  - concern: Relies on pending Arabic readings (A1) and interpretation I1.
  - concern: The reason text mentions the datum discrepancy in the column heading, which is not part of row A's own text; this is peripheral but accurate per the Arabic heading reading.
  - checked: ADD-03:T5-1/a, ADD-03:7.2, ADD-03:7.1, ADD-03:p4-image/row-a-right, ADD-03:p4-image/row-a-left
- **ADD-03/T5-1/b** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: Controller semantic check flagged 'Required' as amendment-like language; a person must confirm.
  - concern: Relies on pending Arabic readings (A1) and interpretation I1.
  - checked: ADD-03:T5-1/b, ADD-03:7.2, ADD-03:7.1, ADD-03:p4-image/row-b-left, ADD-03:p4-image/row-b-right
- **ADD-03/T5-1/notes** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: Heading only; depends on I1 which a person must confirm.
  - checked: ADD-03:T5-1/notes, ADD-03:7.2
- **ADD-03/T5-1/note(1)** (conflicting): critic agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
  - concern: The English and Arabic note 1 conflict on scope, as the item states; the conflict is real on the quoted text (permanent only vs permanent and temporary including cranes and equipment).
  - concern: Depends on the pending Arabic reading (A1).
  - concern: The no_effect disposition rests on the Arabic governing (7.2). That makes the Arabic scope the operative one, handled elsewhere.
  - checked: ADD-03:T5-1/note(1), ADD-03:7.2, ADD-03:p4-image/note1
- **ADD-03/T5-1/note(1)/issue** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: Target ADD-03:p4-image/note1 is not among the cited units but is the right counterpart.
  - concern: The claim about the 25/40 m limits applying to cranes follows from the Arabic reading only, which is pending (A1).
  - concern: The reference to 'the crane and lifting plan that Q21 requires' is not supported by any evidence shown here.
  - checked: ADD-03:T5-1/note(1), ADD-03:p4-image/note1
- **ADD-03/T5-1/note(1)/clar** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The question follows from the discrepancy. Its evidence list quotes only the English note, not the Arabic. The Arabic is covered through F5.
  - concern: Depends on the pending Arabic reading (A1/I2).
  - checked: ADD-03:T5-1/note(1), ADD-03:p4-image/note1
- **ADD-03/T5-1/note(2)** (conflicting): critic agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
  - concern: The datum conflict is real on the quoted text: English 'finished ground level after grading and filling' vs Arabic 'natural ground level before grading and filling'.
  - concern: The claim about the English column heading is not shown in the evidence here; only the Arabic heading reading is printed.
  - concern: Depends on the pending Arabic readings (A1).
  - checked: ADD-03:T5-1/note(2), ADD-03:7.2, ADD-03:p4-image/note2, ADD-03:p4-image/th-left
- **ADD-03/T5-1/note(2)/issue** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The consequence about fill reducing and cut increasing usable height follows logically from the datum change, but is not printed in the evidence.
  - concern: Depends on the pending Arabic readings (A1).
  - concern: The English column heading text is not shown, only the note; the unit text for the heading is not in the evidence.
  - checked: ADD-03:T5-1/note(2), ADD-03:p4-image/note2, ADD-03:p4-image/th-left
- **ADD-03/T5-1/note(2)/clar** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The question follows from the discrepancy and is reasonable.
  - concern: Its evidence quotes only the English note; the Arabic is covered through F6.
  - concern: Depends on the pending Arabic readings (A1/I2).
  - checked: ADD-03:T5-1/note(2), ADD-03:p4-image/note2, ADD-03:p4-image/th-left
- **ADD-03/T5-1/note(3)** (insufficient_evidence): critic DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: Controller status is insufficient_evidence: the dependency 'ADD-03/T5-1/note(3)/row' is an unknown id for the controller.
  - concern: The semantic check flags the words 'be notified' and 'shall' as obligation language, so no_effect needs human confirmation.
  - concern: The disposition no_effect is paired with a row_new that carries the same obligation. This is a coherent split only if the person accepts it, and the row_new item is itself pending.
  - concern: It relies on the Arabic note 3 (F7), which is pending (A1). The F7 quote is not cited in the item's own evidence, which has only the English span.
  - checked: ADD-03:T5-1/note(3), ADD-03:p4-image/note3, controller_validation dependencies check
- **ADD-03/T5-1/note(3)/row** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The English and Arabic note 3 agree on the 30-day notice for crane erection/installation (Arabic 'تركيب' = install; English 'erected').
  - concern: The row's assertion that the obligation 'falls to the Project Company through Clause 5.6' is an interpretation; the notifying party is not named. Clause 5.6/7.1 text says the Project Company shall comply with the Table 5-1 height limits, which does not itself clearly assign the notice duty.
  - concern: The row is derived from the English convenience translation, which is not governing. It could duplicate a row from the Arabic note 3 batch.
  - concern: Scope 'post_award' and the 'none_stated' consequence are not contradicted by the evidence shown.
  - concern: Depends on pending Arabic reading (A1).
  - checked: ADD-03:T5-1/note(3), ADD-03:p4-image/note3, ADD-03:7.1, controller row quote check

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T214606Z-2338/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T214606Z-2338 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
