# Review request: ADD-03, run ADD-03-host-20261005T174557Z-4db2

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T17:45:57Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build f826cdeb7fbc262e…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 6 of 70 provisions accounted for
- resolution (kept apart from coverage): 4 resolved, 2 pending a person, 0 invalid, 64 unaccounted; evidence_verified checks quotations, not meaning
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
| ADD-03/3.1 | amendment_op | ADD-03:3.1 | VOL-II:7.2 | evidence_verified |  |
| ADD-03/3.2(b) | amendment_op | ADD-03:3.2 | VOL-II:7.3 | evidence_verified |  |
| ADD-03/4.2 | amendment_op | ADD-03:4.2 | VOL-II:8.4 | evidence_verified |  |
| ADD-03/5.1 | amendment_op | ADD-03:5.1 | VOL-V:31.1 | evidence_verified |  |
| ADD-03/5.2 | amendment_op | ADD-03:5.2 | VOL-V:31.3 | evidence_verified |  |
| ADD-03/4.1(a) | amendment_op | ADD-03:4.1 | VOL-II:8.1 | interpretation_pending | the old words are located in the target, not quoted by the provision: a person checks them |
| ADD-03/4.1(b) | amendment_op | ADD-03:4.1 | VOL-II:8.2 | interpretation_pending | depends on interpretation S-I2: a person must confirm it |
| ADD-03/4.1(c) | amendment_op | ADD-03:4.1 | VOL-II:8.3 | interpretation_pending | the old words are located in the target, not quoted by the provision: a person checks them |
| ADD-03/3.2(a) | escalation | ADD-03:3.2 | VOL-II:7.2 | escalated | missing_information: the proposer declares missing: whether an out-of-range day suspends or breaks the 'continuous' 30-day run |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S-F1: ADD-03:3.1 deletes 'at not less than 90% of nominal capacity' from Volume II Clause 7.2 and substitutes a daily-average-flow range of 85% to 110% of nominal capacity measured at the inlet works. — evidence verified
- **fact** S-F2: ADD-03:3.2 provides that a day with daily average flow outside 'that range' does not count towards 'the thirty (30) days', and states that Volume II Clause 7.3 is unchanged. It does not cite Clause 7.2 by number. — evidence verified
- **fact** S-F3: ADD-03:4.1 deletes Volume II Clauses 8.1 to 8.3 and prints replacement text for 8.1 and 8.3 only. No replacement text is printed for 8.2. — evidence verified
- **fact** S-F4: ADD-03:4.2 states that the Clauses of Volume II are not renumbered and that Clauses 8.4 and 8.5 are unchanged. — evidence verified
- **fact** S-F5: ADD-03:5.1 replaces the quoted limbs (b)-(c) of Volume V Clause 31.1 with limbs (b)-(d), adding (d), a daily delivered-volume shortfall below 90% of sewage received. ADD-03:5.2 extends the no-cure-period sentence of Clause 31.3 to Clause 31.1(d). — evidence verified
- **fact** S-F6: Volume II Table 2-4 (image region VOL-II-p3-r1) is cited in the retained limb (b) of Clause 31.1. ADD-03 does not change it. The image shows the table title and ten parameter rows (BOD5 to Oil and Grease) with columns Unit / Limit / Basis of assessment. — evidence verified
- **interpretation** S-I1: In ADD-03:3.2, 'that range' means the 85%-110% range that ADD-03:3.1 substitutes into Clause 7.2, and 'the thirty (30) days' means the 30-day reliability run in Clause 7.2. So 3.2 adds a counting rule to Clause 7.2. It is not clear how this fits the word 'continuous' in 7.2: an out-of-range day mig… — needs a person
- **interpretation** S-I2: Clause 8.2 falls inside the deleted range '8.1 to 8.3' and is given no replacement, and 4.2 says the clauses are not renumbered. So Clause 8.2 (the CMMS requirement) is deleted outright, and the 8.2 number stays vacant. This may not have been intended by the Authority. — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone
- units changed: VOL-II:7.2, VOL-V:31.1, VOL-V:31.3
- rows citing them: VOL-II-7.2-01, VOL-V-31.1-01, VOL-V-31.1-02, VOL-V-31.1-03, VOL-V-31.3-01, VOL-V-31.3-02, VOL-V-31.3-03
- rows that would be STALE: VOL-V-31.3-01, VOL-II-7.2-01, VOL-II-8.4-01, VOL-II-8.4-02, VOL-II-8.5-01, VOL-II-8.5-02, VOL-V-31.1-01, VOL-V-31.1-02, VOL-V-31.1-03, VOL-V-31.3-02, VOL-V-31.3-03
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 0
- clarification entries citing changed units: CQ-VOL-III-DRAWINGS, CQ-PERSISTENT-BREACH, CQ-PCOD-RELIABILITY-RUN
- A3: enters none; leaves none
- programme: 60 activity change(s)

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind06-20261005T173226Z-analysis-003-critic`, route **host**; 5 item(s) reviewed

- **ADD-03/3.2(a)** (escalated): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: Escalation is reasonable: 3.2 does not cite 7.2 by number; 'that range' and 'the thirty (30) days' refer back to 3.1, whose text is not shown here, so the link to 7.2 is an inference (S-I1).
  - concern: Interaction of 'shall not count' with 'continuous' in 7.2 is genuinely unresolved on the evidence; 3.2 itself says only 7.3 is unchanged and is silent on 7.2's continuity wording.
  - concern: The mention of Q18/Volume V Clause 34 is not in the printed evidence; I did not rely on it.
  - checked: ADD-03:3.2, VOL-II:7.2
- **ADD-03/4.1(a)** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
  - concern: The new 8.1 text matches the quoted replacement minus the '8.1' label; the old text matches VOL-II:8.1 exactly.
  - concern: The new text adds a reference to Clause 7.4's asset register. Clause 7.4 is not shown in the evidence, so the claim that it is due 60 days after PCOD cannot be verified here.
  - concern: The change goes beyond a quantity change (2 years to 18 months), since it also adds a recording obligation. A person should note that.
  - checked: ADD-03:4.1, VOL-II:8.1
- **ADD-03/4.1(b)** (interpretation_pending): critic agrees — selected because removal; model claude-sonnet-5-5
  - concern: The reading is plausible: 8.2 lies in the range '8.1 to 8.3' that is deleted. Replacement text is printed only for 8.1 and 8.3, and 4.2 says there is no renumbering.
  - concern: It is still an inference that the Authority meant to drop the CMMS obligation. The clause could be an omission, so a clarification question is warranted; the item itself flags this.
  - concern: 4.2 does not list 8.2 as unchanged, which is consistent with deletion.
  - checked: ADD-03:4.1, ADD-03:4.2, VOL-II:8.2
- **ADD-03/4.1(c)** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
  - concern: The old text matches VOL-II:8.3 and the new text matches the quoted replacement for 8.3.
  - concern: The change adds substantive requirements: a degree, ten years' experience, and naming the manager in the Technical Proposal with a CV appendix. The two-operator requirement is retained unchanged.
  - checked: ADD-03:4.1, VOL-II:8.3
- **ADD-03/4.2** (evidence_verified): critic agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
  - concern: The target field names only 8.4, but the payload annotates 8.4 and 8.5. VOL-II:8.5 is not shown in the evidence, so I could not check it directly. 4.2 does state that 8.5 is unchanged.
  - concern: The 'not renumbered' sentence is not annotated on any unit. It is only referenced in the note.
  - checked: ADD-03:4.2, VOL-II:8.4

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T174557Z-4db2/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T174557Z-4db2 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
