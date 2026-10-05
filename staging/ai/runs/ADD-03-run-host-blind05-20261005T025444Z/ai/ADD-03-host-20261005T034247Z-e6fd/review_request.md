# Review request: ADD-03, run ADD-03-host-20261005T034247Z-e6fd

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T03:42:47Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 77784d6d270a9e34…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 6 of 54 provisions accounted for
- resolution (kept apart from coverage): 0 resolved, 6 pending a person, 0 invalid, 48 unaccounted; evidence_verified checks quotations, not meaning
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

## Items

| id | type | provision | target | status | why (first failed check) |
|---|---|---|---|---|---|
| ADD-03/T5-1/notes | disposition | ADD-03:T5-1/notes |  | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/T5-1/note(3) | disposition | ADD-03:T5-1/note(3) |  | insufficient_evidence | missing_information: the proposer declares missing: whether 'days' are calendar or working days (unqualified in the Arabic) |
| ADD-03/T5-1/a | disposition | ADD-03:T5-1/a |  | conflicting | declared_conflicts: the proposer declares: English column heading 'm above finished ground level' against the Arabic heading 'متر فوق منسوب الأرض الطبيعية' (natural ground level) |
| ADD-03/T5-1/b | disposition | ADD-03:T5-1/b |  | conflicting | declared_conflicts: the proposer declares: English column heading 'm above finished ground level' against the Arabic heading 'متر فوق منسوب الأرض الطبيعية' (natural ground level) |
| ADD-03/T5-1/note(1) | escalation | ADD-03:T5-1/note(1) |  | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(1) against ADD-03:p4-image/note1 |
| ADD-03/T5-1/note(2) | escalation | ADD-03:T5-1/note(2) |  | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(2) against ADD-03:p4-image/note2; ADD-03:T5-1/a and /b column heading against ADD-03:p4-image/table-header |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** F1: Clause 7.2 states that Table 5-1 is issued in Arabic, the Arabic text governs and the English translation at Appendix B is for convenience only. — evidence verified
- **fact** F2: Appendix B opens by saying the translation is for convenience only and the Arabic text at Appendix A governs. — evidence verified
- **fact** F3: Clause 7.1 inserts new Volume II Clause 5.6, which incorporates Table 5-1 as reproduced at Appendix A (the Arabic) by reference. — evidence verified
- **fact** F4: The Arabic rows (readings pending) print zone A: within 1,500 m of the eastern boundary, 25, lighting required; zone B: remainder, 40, lighting required for any part exceeding 30 m. — evidence verified
- **fact** F5: Arabic note 1 (reading pending) applies the limits to permanent and temporary structures including stacks, cranes and construction equipment. — evidence verified
- **fact** F6: Arabic note 2 and the Arabic height column heading (readings pending) use natural ground level (منسوب الأرض الطبيعية), measured before grading and filling works. — evidence verified
- **fact** F7: Arabic note 3 (reading pending) requires notifying the Office at least thirty (30) days before installing any crane on the site; 'days' is not qualified. — evidence verified
- **fact** F8: English note (1) limits to permanent structures including stacks; English note (2) measures from finished ground level after grading and filling; the English height column reads 'm above finished ground level'. — evidence verified
- **interpretation** I1: The Appendix B translation rows and notes do not themselves change any unit of the pack: the change (new Volume II Clause 5.6 incorporating Table 5-1) is made by Clause 7.1, in another batch, and the governing text is the Arabic at Appendix A. — needs a person
- **interpretation** I2: English note (1) is narrower than the governing Arabic note 1: it leaves out temporary structures, cranes and construction equipment. — needs a person
- **interpretation** I3: English note (2) and the English height column heading state the opposite datum to the governing Arabic (finished ground level after grading and filling, against natural ground level before grading and filling works). Where the site is filled, the Arabic allows less height above finished ground. — needs a person

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-20261005T025444Z-analysis-009-critic`, route **host**; 6 item(s) reviewed

- **ADD-03/T5-1/a** (conflicting): critic agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
  - concern: The Arabic reading (p4 image) is pending approval, so the claim that the figures match rests on an unapproved reading.
  - concern: no_effect applies only to the English row as a translation. The row carries 'Required' and a datum that conflicts with the Arabic heading, so a person must confirm it, as the item says. Clause 7.1 is cited from the statements, not printed as a unit.
  - checked: ADD-03:T5-1/a, ADD-03:7.2, ADD-03:p4-image/row-a, ADD-03:p4-image/table-header
- **ADD-03/T5-1/b** (conflicting): critic agrees — selected because conflicting, consequential_interpretation; model claude-sonnet-5-5
  - concern: The Arabic reading is pending approval.
  - concern: no_effect covers only the translation row. The datum conflict is real and is escalated under note(2). The row's 'Required for any part exceeding 30 m' matches the Arabic reading.
  - checked: ADD-03:T5-1/b, ADD-03:7.2, ADD-03:p4-image/row-b, ADD-03:p4-image/table-header
- **ADD-03/T5-1/notes** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The claim that the Arabic prints a matching 'ملاحظات' heading is in the model rationale only. No quotation of it is shown.
  - checked: ADD-03:T5-1/notes, ADD-03:7.2, ADD-03:AppB/para1
- **ADD-03/T5-1/note(1)** (conflicting): critic agrees — selected because conflicting; model claude-sonnet-5-5
  - concern: The conflict depends on the pending reading of Arabic note 1. If that reading is approved, English note (1) is narrower: it omits temporary structures, cranes and construction equipment.
  - concern: The link to Q21 and cover/para3 is asserted but no evidence for it is shown.
  - checked: ADD-03:T5-1/note(1), ADD-03:p4-image/note1, ADD-03:7.2
- **ADD-03/T5-1/note(2)** (conflicting): critic agrees — selected because conflicting; model claude-sonnet-5-5
  - concern: Both Arabic readings (note 2 and the heading) are pending approval.
  - concern: The opposite datum is real on the quoted words: finished ground after grading and filling in English, against natural ground before grading and filling in Arabic. The consequence for filled ground follows.
  - checked: ADD-03:T5-1/note(2), ADD-03:p4-image/note2, ADD-03:p4-image/table-header, ADD-03:7.2
- **ADD-03/T5-1/note(3)** (insufficient_evidence): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The Arabic note 3 reading is pending approval.
  - concern: no_effect applies only to the translation. The 30-day notification duty is real and arrives through the Arabic table incorporated by 7.1. The controller flags the 'shall' wording for human confirmation.
  - concern: Neither text says whether the 30 days are calendar or working days. The item states this.
  - checked: ADD-03:T5-1/note(3), ADD-03:p4-image/note3, ADD-03:7.2, ADD-03:7.1

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T034247Z-e6fd/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T034247Z-e6fd --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
