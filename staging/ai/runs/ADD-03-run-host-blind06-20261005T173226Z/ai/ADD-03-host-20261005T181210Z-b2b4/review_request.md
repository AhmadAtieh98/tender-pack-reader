# Review request: ADD-03, run ADD-03-host-20261005T181210Z-b2b4

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T18:12:10Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build f826cdeb7fbc262e…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 8 of 70 provisions accounted for
- resolution (kept apart from coverage): 0 resolved, 8 pending a person, 0 invalid, 62 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

## Findings (a person looks at each)

- 1 provision with amendment language carries no change (0 contradict a change the pattern drafter drafts from their words: invalid; 1 need a person): ADD-03:T1-3/note(3)

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

## Items

| id | type | provision | target | status | why (first failed check) |
|---|---|---|---|---|---|
| ADD-03/T1-3/tp-1 | disposition | ADD-03:T1-3/tp-1 |  | interpretation_pending | depends on assumption A1: a person must confirm it |
| ADD-03/T1-3/tp-2/issue | issue | ADD-03:T1-3/tp-2 | ADD-03:T1-3/tp-2 | interpretation_pending | depends on assumption A1: a person must confirm it |
| ADD-03/T1-3/notes | disposition | ADD-03:T1-3/notes |  | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/T1-3/note(1)/issue | issue | ADD-03:T1-3/note(1) | ADD-03:T1-3/note(1) | interpretation_pending | depends on assumption A1: a person must confirm it |
| ADD-03/T1-3/note(2) | disposition | ADD-03:T1-3/note(2) |  | interpretation_pending | depends on assumption A1: a person must confirm it |
| ADD-03/T1-3/note(3) | disposition | ADD-03:T1-3/note(3) |  | interpretation_pending | semantic: no_effect on amendment language: a person must confirm (its words carry 'shall') |
| ADD-03/T1-3/note(4) | disposition | ADD-03:T1-3/note(4) |  | interpretation_pending | depends on assumption A1: a person must confirm it |
| ADD-03/AppB/para2 | disposition | ADD-03:AppB/para2 |  | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/T1-3/tp-2 | escalation | ADD-03:T1-3/tp-2 | ADD-03:p4-image/tp2-duration | conflicting | declared_conflicts: the proposer declares: ADD-03:p4-image/tp2-duration |
| ADD-03/T1-3/note(1) | escalation | ADD-03:T1-3/note(1) | ADD-03:p4-image/note1 | conflicting | declared_conflicts: the proposer declares: ADD-03:p4-image/note1 |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** F1: ADD-03 Section 2.2 states that the Arabic text of Table 1-3 governs and that the English translation at Appendix B is for convenience only. — evidence verified
- **fact** F2: Appendix B opens by restating that it is a convenience translation and that the Arabic Table 1-3 at Appendix A governs. — evidence verified
- **fact** F3: ADD-03 Section 2.1 brings Table 1-3 into Volume II through Appendix A (the Network Operator's issue), not through Appendix B. — evidence verified
- **fact** F4: The English translation gives TP-2's maximum shutdown duration as 6 hours. — evidence verified
- **fact** F5: The pack's reading of the Arabic image (status pending) prints the TP-2 maximum shutdown duration cell as ٤ (4) and the TP-1 cell as ٦ (6). — evidence verified
- **fact** F6: English note (1) bans shutdowns only during Ramadan. The pending reading of the Arabic note 1 also bans them during the Eid al-Fitr and Eid al-Adha holidays. — evidence verified
- **assumption** A1: The pending readings of image region ADD-03-p4-r1 (tp2-duration '٤', tp1-duration '٦', note1) are accurate. I compared them with the crop (sha256 f827ab1b…) and they agree, but no person has approved them yet. — needs a person
- **interpretation** I1: The Appendix B units (table rows, notes and signature) change no unit that stands at ADD-02. Table 1-3's content takes effect through Section 2.1 and the governing Arabic at Appendix A, which other provisions cover. Appendix B text that matches the Arabic therefore has no effect of its own. — needs a person
- **interpretation** I2: For TP-2, the governing Arabic maximum shutdown duration is 4 hours. The English figure of 6 hours is a translation discrepancy and does not govern. — needs a person
- **interpretation** I3: The governing Arabic note 1 also bans shutdowns during the Eid al-Fitr and Eid al-Adha holidays. The English note (1) leaves these out, and the Arabic governs. — needs a person
- **interpretation** I4: The English renders the Arabic '١٠ أيام عمل' ('10 working days') with the capitalised defined term 'Working Days'. Whether the Network Operator's notice period counts days by the tender's VOL-I 2.4 calendar is not established. — needs a person

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind06-20261005T173226Z-analysis-010-critic`, route **host**; 10 item(s) reviewed

- **ADD-03/T1-3/tp-1** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The claim that every cell matches the Arabic row rests on the proposer's reading of the crop. Only the TP-1 duration reading (٦) is printed as evidence, and it is pending.
  - concern: I4 (capitalised 'Working Days') is left open. It does not change the no_effect disposition.
  - checked: ADD-03:T1-3/tp-1, ADD-03:2.2 (F1), ADD-03:2.1 (F3), ADD-03:AppB/para1 (F2), ADD-03:p4-image/tp1-duration
- **ADD-03/T1-3/tp-2** (conflicting): critic agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The conflict is real on the evidence shown: English says 6, the pending Arabic reading says ٤, and ADD-03:2.2 says the Arabic governs.
  - concern: The Arabic value depends on a pending, unapproved reading (A1). The escalation correctly lists this as missing.
  - concern: The claim that ADD-03:2.7 rejects bids on this value is not supported by any printed text. ADD-03:2.7 is not in the evidence.
  - concern: The target is the image reading, which is the right unit for the Arabic side.
  - checked: ADD-03:T1-3/tp-2, ADD-03:p4-image/tp2-duration, ADD-03:2.2, ADD-03:AppB/para1
- **ADD-03/T1-3/tp-2/issue** (interpretation_pending): critic DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The text says the Arabic 'prints ٤ (4 hours)' as settled fact. The reading is pending and unapproved.
  - concern: The consequence that a 6-hour programme 'would be rejected under ADD-03:2.7' cannot be checked. ADD-03:2.7 is not among the evidence printed.
  - concern: The item cites no ADD-03:2.2 evidence for 'the Arabic governs'. The discrepancy itself is plausible and should be wording-qualified (pending reading, 2.7 unverified).
  - checked: ADD-03:T1-3/tp-2, ADD-03:p4-image/tp2-duration
- **ADD-03/T1-3/notes** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: A heading only. It says nothing that amends, obliges or excepts.
  - checked: ADD-03:T1-3/notes, ADD-03:2.2 (F1)
- **ADD-03/T1-3/note(1)** (conflicting): critic agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The Arabic reading includes the Eid holidays and the English omits them, so the conflict is real. It depends on a pending reading (A1).
  - concern: Eid dates are not in the pack, as the item says.
  - concern: The target is the right image unit.
  - checked: ADD-03:T1-3/note(1), ADD-03:p4-image/note1, ADD-03:2.2, ADD-03:AppB/para1
- **ADD-03/T1-3/note(1)/issue** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The wording 'must avoid all three periods' treats the pending Arabic reading as settled. It should be qualified until a person approves the reading.
  - concern: The item cites no ADD-03:2.2 evidence for 'the Arabic governs'. The linked escalation does.
  - checked: ADD-03:T1-3/note(1), ADD-03:p4-image/note1
- **ADD-03/T1-3/note(2)** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The claim that Arabic note 2 matches rests only on the proposer's rationale. No Arabic reading unit for note 2 is printed.
  - concern: The no_effect reasoning (2.2 and 2.1) follows from the cited text, but a person should confirm it.
  - checked: ADD-03:T1-3/note(2), ADD-03:2.2, ADD-03:2.1 (F3)
- **ADD-03/T1-3/note(3)** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The text carries 'shall', and the controller flagged this for a person. no_effect is defensible only because the binding text is Arabic note 3 via 2.1 and 2.2.
  - concern: The match with Arabic note 3 is not shown in the printed evidence, only in the proposer's rationale. The item says a person should confirm this.
  - checked: ADD-03:T1-3/note(3), ADD-03:2.2, ADD-03:2.1 (F3)
- **ADD-03/T1-3/note(4)** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The match with Arabic note 4 is asserted from the crop and not shown in the printed evidence.
  - concern: The item lists only the note itself as evidence. ADD-03:2.2 appears only in the statements.
  - checked: ADD-03:T1-3/note(4), ADD-03:2.2 (F1)
- **ADD-03/AppB/para2** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The text is a signature block and creates no obligation or amendment. No concern with no_effect.
  - checked: ADD-03:AppB/para2

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T181210Z-b2b4/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T181210Z-b2b4 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
