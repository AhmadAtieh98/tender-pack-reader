# Review request: ADD-03, run ADD-03-host-20261004T224836Z-24d7

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-04T22:48:36Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build fefc497f4a273092…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 42 of 70 provisions accounted for
- resolution (kept apart from coverage): 35 resolved, 7 pending a person, 0 invalid, 28 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

## Findings (a person looks at each)

- 1 provision with amendment language carries no change (0 contradict a change the pattern drafter drafts from their words: invalid; 1 need a person): ADD-03:7.1

## Provisions not accounted for (a person treats each)

- ADD-03:cover/para1
- ADD-03:cover/para2
- ADD-03:cover/para3
- ADD-03:1.1
- ADD-03:1.2
- ADD-03:2.1
- ADD-03:2.2
- ADD-03:3.1
- ADD-03:4.1
- ADD-03:5.1
- ADD-03:5.2
- ADD-03:6.1
- ADD-03:T1-1/A
- ADD-03:T1-1/B
- ADD-03:T1-1/C
- ADD-03:T1-1/D
- ADD-03:T1-1/E
- ADD-03:T1-1/F
- ADD-03:T1-1/G
- ADD-03:T1-1/total
- ADD-03:Q15
- ADD-03:Q16
- ADD-03:Q17
- ADD-03:Q18
- ADD-03:Q19
- ADD-03:Q20
- ADD-03:AppA/para1
- ADD-03:AppB/para1

## Items

| id | type | provision | target | status | why (first failed check) |
|---|---|---|---|---|---|
| ADD-03/8.1 | amendment_op | ADD-03:8.1 | VOL-I:9.1 | evidence_verified |  |
| ADD-03/S6/para1(a) | amendment_op | ADD-03:S6/para1 | VOL-I:11.3 | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/S6/para1(b) | amendment_op | ADD-03:S6/para1 | VOL-I:11.2 | interpretation_pending | the old words are located in the target, not quoted by the provision: a person checks them |
| ADD-03/S6/para1(c) | amendment_op | ADD-03:S6/para1 | ADD-03:T1-1 | interpretation_pending | an annotation that interprets is an interpretation of the provision: a person confirms it |
| ADD-03/S6/para1/issue | issue | ADD-03:S6/para1 | VOL-I:11.3 | interpretation_pending | depends on interpretation I1: a person must confirm it |
| ADD-03/6.2(a) | amendment_op | ADD-03:6.2 | VOL-I:11.3 | interpretation_pending | the old words are located in the target, not quoted by the provision: a person checks them |
| ADD-03/6.2(b) | amendment_op | ADD-03:6.2 | VOL-I:11.3 | interpretation_pending | depends on interpretation I2: a person must confirm it |
| ADD-03/7.1 | disposition | ADD-03:7.1 | VOL-II:1.4 | interpretation_pending | semantic: no_effect on amendment language: a person must confirm (its words carry 'notifies' (cites VOL-II:1.4)) |
| ADD-03/7.1/issue | issue | ADD-03:7.1 | VOL-II:1.4 | interpretation_pending | depends on assumption A1: a person must confirm it |
| ADD-03/7.2(a) | amendment_op | ADD-03:7.2 | VOL-II:1.4 | interpretation_pending | the old words are located in the target, not quoted by the provision: a person checks them |
| ADD-03/7.2(b) | amendment_op | ADD-03:7.2 | VOL-II:1.4 | interpretation_pending | an annotation that interprets is an interpretation of the provision: a person confirms it |
| ADD-03/8.2 | amendment_op | ADD-03:8.2 | ADD-03:F4-H | interpretation_pending | an annotation that adds obligation is an interpretation of the provision: a person confirms it |
| ADD-03/8.2/issue | issue | ADD-03:8.2 | ADD-03:F4-H | interpretation_pending | depends on interpretation I4: a person must confirm it |
| ADD-03/8.3 | amendment_op | ADD-03:8.3 | ADD-03:F4-H | interpretation_pending | an annotation that adds obligation is an interpretation of the provision: a person confirms it |
| ADD-03/8.4 | amendment_op | ADD-03:8.4 | ADD-03:F4-H | interpretation_pending | an annotation that adds obligation is an interpretation of the provision: a person confirms it |
| ADD-03/S6/para1(d) | amendment_op | ADD-03:S6/para1 | ADD-03:T1-1/G | insufficient_evidence | missing_information: the proposer declares missing: Appendix C (format of the Energy Performance Statement) was not found as a unit in this batch's evidence; C46 reports no A1 row holds this obligation. |
| ADD-03/7.2(c) | escalation | ADD-03:7.2 | VOL-V:1.3 | escalated | depends on interpretation I3: a person must confirm it |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** F1: ADD-03 Note (2) to Table 1-1 (second revision) amends the VOL-I 11.2 weighting to 70% technical / 30% commercial. — evidence verified
- **fact** F2: At ADD-02, VOL-I 11.2 reads 65% technical / 35% commercial (as amended by ADD-02). — evidence verified
- **fact** F3: At ADD-02, VOL-I 11.3 sets the threshold as 70 marks out of 100 and returns Envelope B unopened. — evidence verified
- **fact** F4: Table 1-1 (second revision) in ADD-03 totals 120 marks. — evidence verified
- **fact** F5: calculate threshold_of_total: 70% of 120 marks = 84 marks (not rounded; the pack states no rounding rule). — evidence verified
- **fact** F6: ADD-03:6.2 deletes VOL-I 11.3 and replaces it with a new 11.3 and a new 11.3A. — evidence verified
- **fact** F7: Section 7 takes effect only on an Authority notice through the Portal given not later than 10 Working Days before the Proposal Due Date. If no notice is given, it lapses. — evidence verified
- **fact** F8: VOL-II 1.4 at ADD-02 has the Authority providing a grid connection point at the site boundary. — evidence verified
- **fact** F9: The calculate tool (relative_date, VOL-I 2.4 calendar) gives a Section 7 notice deadline of Thursday 12 November 2026, counting 10 Working Days back from a PDD of 2026-11-26. That PDD is the printed_date of VOL-I:6.1 at ADD-02. — evidence verified
- **fact** F10: ADD-03:8.1 adds Form 4-H to Volume IV and to the VOL-I 9.1 list, after Form 4-G. — evidence verified
- **fact** F11: The Arabic Form 4-H (Appendix A, image p.4, decl1) defines a beneficial owner by a ten per cent (10%) holding. — evidence verified
- **fact** F12: The English Form 4-H text (p.5) defines a beneficial owner by a twenty-five per cent (25%) holding. — evidence verified
- **fact** F13: ADD-03:8.2 makes the Arabic text govern and treats the English translation as for convenience only. — evidence verified
- **fact** F14: ADD-03:8.3 lets members incorporated outside the Kingdom submit Form 4-H through the Portal up to 5 Working Days after the PDD. The calculate tool gives two readings from PDD 2026-11-26: 2026-12-03 if the PDD is not counted, 2026-12-02 if it is (the pack is silent on forward counting). The conserva… — evidence verified
- **fact** F15: ADD-03:8.4 makes a missing or improperly executed Form 4-H for any member a ground of non-responsiveness. — evidence verified
- **assumption** A1: The Proposal Due Date is still 2026-11-26 (VOL-I 6.1 at ADD-02). I have not checked whether another ADD-03 provision outside this batch moves it. — needs a person
- **interpretation** I1: Note (1) says the threshold is 'unchanged at seventy per cent (70%)', but the threshold in marks rises: it was 70 marks out of 100 (VOL-I 11.3 at ADD-02) and becomes 70% of the 120 marks in the second-revision Table 1-1, i.e. 84 marks. A Proposal scoring between 70 and 83 marks out of 120 would hav… — needs a person
- **interpretation** I2: New 11.3A changes what happens to Envelope B. It is no longer simply 'returned unopened': it is retained unopened by the Authority and returned only after the Preferred Bidder Notification. — needs a person
- **interpretation** I3: ADD-03:7.2(c) puts the grid connection works cost into the Estimated Project Cost (defined in VOL-V 1.3). That cost base affects, for example, the VOL-V 18.4 delay-LD cap. The provision does not cite VOL-V 1.3, so the engine refuses an annotation on it (C22 'not cited'). — needs a person
- **interpretation** I4: Because the Arabic text governs (8.2), the 10% beneficial-ownership threshold applies and the English 25% does not. Each member must list every natural person holding 10% or more. The image reading for decl1 is still 'pending' and needs approval. — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone; NOT clean: 1 provision with amendment language carries no change (0 contradict a change the pattern drafter drafts from their words: invalid; 1 need a person): ADD-03:7.1
- units changed: ADD-03:F4-H/T1, ADD-03:F4-H/T1/1, ADD-03:F4-H/T1/2, ADD-03:F4-H/T1/3, ADD-03:F4-H/T1/4, ADD-03:F4-H/image, ADD-03:F4-H/image/decl1, ADD-03:F4-H/image/decl2, ADD-03:F4-H/image/decl3, ADD-03:F4-H/image/field-capacity-ar, ADD-03:F4-H/image/field-capacity-en, ADD-03:F4-H/image/field-cr-ar, ADD-03:F4-H/image/field-cr-en, ADD-03:F4-H/image/field-date-ar, ADD-03:F4-H/image/field-date-en, ADD-03:F4-H/image/field-member-ar, ADD-03:F4-H/image/field-member-en, ADD-03:F4-H/image/field-signatory-ar, ADD-03:F4-H/image/field-signatory-en, ADD-03:F4-H/image/field-signature-ar, ADD-03:F4-H/image/field-signature-en, ADD-03:F4-H/image/form-ar, ADD-03:F4-H/image/form-en, ADD-03:F4-H/image/hdr-ar, ADD-03:F4-H/image/hdr-en, ADD-03:F4-H/image/image-footer, ADD-03:F4-H/image/intro, ADD-03:F4-H/image/note, ADD-03:F4-H/image/ref-ar, ADD-03:F4-H/image/ref-en, ADD-03:F4-H/image/table-header, ADD-03:F4-H/image/table-row4, ADD-03:F4-H/image/table-row4-cells, ADD-03:F4-H/image/title, ADD-03:F4-H/para1, ADD-03:F4-H/para2, ADD-03:H:F4-H, VOL-I:9.1+ADD-03
- rows citing them: none
- rows that would be STALE: none
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 3
  - ADD-03/8.1 [A1]: ADD-03/8.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-I:9.1; a row of the anchor VOL-I:9.1 does not count): 'A new Form 4-H (De…
  - ADD-03/8.1 [A1]: ADD-03/8.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the new ADD-03:F4-H; a row of the anchor VOL-I:9.1 does not count): 'A new Form 4-H (Declaration of B…
  - ADD-03/8.1 [A3]: ADD-03/8.1 brings in consequence words ['non-responsive', 'غير مستجيب'] that no row's consequence carries at ADD-03: 'A new Form 4-H (Declaration of Beneficial Ownership) is added to Volume IV and to…
- clarification entries citing changed units: none
- A3: enters none; leaves none
- programme: 5 activity change(s)

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind04-s11-20261004T222214Z-analysis-004-critic`, route **host**; 13 item(s) reviewed

- **ADD-03/S6/para1(b)** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
  - concern: The provision does not quote the old words. They come from VOL-I:11.2 at ADD-02, which prints 65/35, and they match the target.
  - checked: ADD-03:S6/para1 note (2), VOL-I:11.2
- **ADD-03/S6/para1(c)** (interpretation_pending): critic agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: Note (3) is a scoring rule, so an interpreting annotation fits. The 'standard five-point scale' is not defined in the evidence shown.
  - concern: Table 1-1 is not named by 7.x, but the notes are headed 'Notes to Table 1-1', so the target is reasonable.
  - checked: ADD-03:S6/para1, ADD-03:T1-1
- **ADD-03/S6/para1(d)** (insufficient_evidence): critic agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The words 'shall shall be included' are not in the evidence. The shown text 'shall be included in the Technical Proposal in the format at Appendix C' does support a new deliverable tied to criterion G.
  - concern: Appendix C is not in the evidence, so the format and any further requirements cannot be checked. This is already declared as missing information.
  - concern: The controller status is insufficient_evidence. A person should obtain Appendix C before relying on the item.
  - checked: ADD-03:S6/para1, ADD-03:T1-1/G
- **ADD-03/6.2(a)** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
  - concern: The old 11.3 text matches the target. The new text matches the quoted new 11.3. The Envelope B sentence moves to 11.3A.
  - concern: The threshold changes from '70 marks out of 100' to '70% of total marks available in Table 1-1'. These are equal only if Table 1-1 totals 100 marks. The evidence shown does not give that total.
  - checked: ADD-03:6.2, VOL-I:11.3
- **ADD-03/6.2(b)** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
  - concern: The new text matches the quoted 11.3A. The timing change (retained, then returned after the Preferred Bidder Notification) follows from the words.
  - concern: The label 11.3A is carried by the renumber map, not by the new_text.
  - checked: ADD-03:6.2, VOL-I:11.3
- **ADD-03/7.2(a)** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
  - concern: The deletion of the words and the preceding comma matches 7.2(a). The triggered result 'free of encumbrance. All other utilities…' is correct.
  - concern: The 12 Nov 2026 deadline depends on a PDD of 26 Nov 2026 and on the Working Day calendar. Neither is shown here, and A1 is an unchecked assumption. A person should confirm both.
  - concern: The text of 7.1 is not among the printed units. It is relied on only through the quoted span, which the controller verified.
  - checked: ADD-03:7.2, ADD-03:7.1 quoted spans, VOL-II:1.4
- **ADD-03/7.2(b)** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: It is a conditional interpretation that depends on 7.1 and on 7.2(a).
  - checked: ADD-03:7.2, VOL-II:1.4
- **ADD-03/7.2(c)** (escalated): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: Escalating is reasonable. 7.2(c) says the grid cost forms part of the Estimated Project Cost, and VOL-V:1.3 defines that term but is not cited by 7.2.
  - concern: The claims that VOL-V 1.3 is also amended by ADD-03 Section 2 and that VOL-V 18.4 caps delay LDs at 10% of EPC are not in the evidence shown. They are unverified context.
  - concern: The consequence is conditional on Section 7 having effect, so it is tied to the 7.1 notice.
  - checked: ADD-03:7.2, VOL-V:1.3
- **ADD-03/8.1** (evidence_verified): critic DOES NOT agree — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
  - concern: The evidence shown for VOL-I:9.1 is only the lead-in line. It does not show the list items, so I cannot confirm that VOL-I:9.1(e)+ADD-02 is Form 4-G, which the 'after' position depends on.
  - concern: The claims that the new group ADD-03:F4-H has 37 units and that this follows the ADD-02/7.1 pattern are not verifiable from the evidence shown.
  - concern: The provision does say Form 4-H is added to the 9.1 list after Form 4-G, so the intent is clear. A person must check the placement.
  - checked: ADD-03:8.1, VOL-I:9.1
- **ADD-03/8.2** (interpretation_pending): critic agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
  - concern: The provision requires Arabic, a signature and stamp from each member, Arabic governing, and an English translation for convenience only. The Arabic note matches.
  - concern: The Arabic image reading is still pending approval.
  - concern: The target is the form group, which 8.2 does not cite by unit id. It names Form 4-H, so this is acceptable.
  - checked: ADD-03:8.2, ADD-03:F4-H/image/note
- **ADD-03/8.2/issue** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
  - concern: The Arabic reading says 'ten per cent (١٠٪)' and the English says 25%, and 8.2 says the Arabic governs. The conflict is real and the conclusion follows.
  - concern: The Arabic reading comes from an image reading that is still pending approval. A person should check it against the image.
  - concern: The advice to prepare to 10% is a recommendation, not something the provision states.
  - checked: ADD-03:F4-H/image/decl1, ADD-03:F4-H/para1, ADD-03:8.2
- **ADD-03/8.3** (interpretation_pending): critic agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
  - concern: The default and the exception for members incorporated outside the Kingdom follow from the words.
  - concern: The 2 or 3 Dec 2026 dates depend on the PDD (A1) and the Working Day calendar, neither of which is shown. The pack's forward-counting convention is unstated, as the item itself says.
  - concern: The Portal route is optional ('may instead'), so the 5-Working-Day window applies only to foreign-incorporated members.
  - checked: ADD-03:8.3
- **ADD-03/8.4** (interpretation_pending): critic agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
  - concern: Non-responsiveness follows from the words. It ties to the time set by 8.3, so it depends on the 8.3 reading.
  - concern: The Arabic note says only that failing to submit it complete makes the Proposal non-responsive. The English adds 'properly executed'. The English text in 8.4 is the stronger statement.
  - checked: ADD-03:8.4, ADD-03:F4-H/image/note

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261004T224836Z-24d7/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261004T224836Z-24d7 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
