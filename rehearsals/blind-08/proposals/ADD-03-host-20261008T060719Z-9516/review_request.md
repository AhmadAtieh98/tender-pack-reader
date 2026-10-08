# Review request: ADD-03, run ADD-03-host-20261008T060719Z-9516

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (claude-opus-5-5)`; reported `None`
- status **partial**; created 2026-10-08T06:07:19Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build e5d1ff4e390aab4b…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 5 of 52 provisions accounted for
- resolution (kept apart from coverage): 4 resolved, 1 pending a person, 0 invalid, 47 unaccounted; evidence_verified checks quotations, not meaning
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
- ADD-03:2.3
- ADD-03:2.4
- ADD-03:2.5
- ADD-03:2.6
- ADD-03:3.4
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
| ADD-03/3.1 | amendment_op | ADD-03:3.1 | VOL-II:4.5 | evidence_verified |  |
| ADD-03/3.2 | disposition | ADD-03:3.2 |  | evidence_verified |  |
| ADD-03/4.1 | amendment_op | ADD-03:4.1 | VOL-V:39.4 | evidence_verified |  |
| ADD-03/4.2 | amendment_op | ADD-03:4.2 | VOL-V:39.4 | evidence_verified |  |
| ADD-03/row-3.4 | row_new | ADD-03:3.4 | ADD-03:3.4 | interpretation_pending | a row reading is an interpretation: a person decides it |
| ADD-03/row-4.6 | row_new | ADD-03:3.1 | VOL-II:4.5+ADD-03 | interpretation_pending | a row reading is an interpretation: a person decides it |
| ADD-03/issue-4.1 | issue | ADD-03:4.1 | VOL-V:39.4 | interpretation_pending |  |
| ADD-03/3.3 | escalation | ADD-03:3.3 | VOL-V:12.1 | escalated |  |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S-F1: ADD-03:4.1 prints a relative reduction of the amount in VOL-V:39.4, which states SAR 20,000,000 at ADD-02. — evidence verified
- **fact** S-F2: The ADD-03 cover summary states a resulting figure of SAR 8,000,000 for Volume V Clause 39.4 and forty-two (42) months for Volume V Clause 12.1. — evidence verified
- **fact** S-F3: ADD-03:3.3 prints an increase of the period in VOL-V:12.1, whose previous value is written in words and figures. — evidence verified

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone
- units changed: VOL-II:4.5+ADD-03, VOL-V:39.4
- rows citing them: none
- rows that would be STALE: none
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 1
  - ADD-03/3.1 [A1]: ADD-03/3.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-II:4.5; a row of the anchor VOL-II:4.5 does not count): 'The following ne…
- clarification entries citing changed units: none
- A3: enters none; leaves none
- programme: 52 activity change(s)

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-20261008T053735Z-77b2-analysis-006-critic`, route **host**; 2 item(s) reviewed

- **ADD-03/3.1** (evidence_verified): critic agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-opus-5-5
  - concern: The anchor is correct. ADD-03:3.1 says 'inserted in Volume II after Clause 4.5', so VOL-II:4.5 is the right anchor and 'number' 4.6 matches the provision. new_text matches the quoted text word for word; only the printed number '4.6' at the start is left out, which is right because it is carried in 'number'.
  - concern: The item's evidence quotes only the instruction ('The following new Clause 4.6 is inserted in Volume II after Clause 4.5'). It does not quote the inserted clause text, which appears only in the payload. Adding a span for the inserted text would make A2 complete.
  - concern: The rationale says no Volume II Clause 4.6 exists at ADD-02. The search result behind that is not shown in this request, so I could not check it.
  - concern: The rationale also mentions ADD-03:Q18, 'Clause 2.1 / Table 2-6' and an A1 row 'ADD-03/row-4.6'. None of these is shown here, so I could not check them. It correctly leaves the 'six (6) hours of the design flow' volume uncomputed.
  - checked: ADD-03:3.1 text_before_addendum, VOL-II:4.5 text_before_addendum, payload.new_text compared with the quoted clause in ADD-03:3.1, evidence span VOL-II:1.2 'the treated effluent storage reservoir' (controller verified; unit text not printed here), controller_validation records
- **ADD-03/row-3.4** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-opus-5-5
  - concern: The requirement and the interpretation quote are word for word from ADD-03:3.4. 'consequence: none_stated' is correct, because ADD-03:3.4 prints no consequence.
  - concern: dependencies lists only ADD-03:3.4. The provision explicitly cites 'Sections 3.1 and 3.3', so the dependencies should also include ADD-03:3.1, ADD-03:3.3 and the new Volume II Clause 4.6 created by ADD-03/3.1. Without them the propagation is incomplete.
  - concern: The text of ADD-03:3.3 is not printed in this request, so I could not check what this row requires for Section 3.3. The row rightly treats that part as pending the escalated ADD-03/3.3.
  - concern: discipline is 'Technical' only, but the provision also requires reflection 'in the Financial Model', which is commercial. The decision owner may need to include Commercial.
  - concern: assessment 'procedural' is a proposed class. The obligation affects what goes into the process design, not only how the bid is submitted. A person should confirm this class.
  - concern: The words 'in the process design and the construction programme submitted in the Technical Proposal and in the Financial Model' could mean both items go in both documents, or each item goes in its own document. The row quotes the words without choosing a reading, which is correct; this may be worth a DRAFT clarification question.
  - checked: ADD-03:3.4 text_before_addendum, row.requirement and interpretations[0].quote compared with ADD-03:3.4, row.introduced.evidence, ADD-03:3.1 (cited by the provision), controller_validation records

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261008T060719Z-9516/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261008T060719Z-9516 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
