# Review request: ADD-03, run ADD-03-host-20261004T223447Z-d132

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-04T22:34:47Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build fefc497f4a273092…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 12 of 70 provisions accounted for
- resolution (kept apart from coverage): 11 resolved, 1 pending a person, 0 invalid, 58 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

## Provisions not accounted for (a person treats each)

- ADD-03:cover/para1
- ADD-03:cover/para2
- ADD-03:cover/para3
- ADD-03:1.1
- ADD-03:1.2
- ADD-03:2.1
- ADD-03:2.2
- ADD-03:3.1
- ADD-03:S6/para1
- ADD-03:6.2
- ADD-03:7.1
- ADD-03:7.2
- ADD-03:8.1
- ADD-03:8.2
- ADD-03:8.3
- ADD-03:8.4
- ADD-03:Q15
- ADD-03:Q16
- ADD-03:Q17
- ADD-03:Q18
- ADD-03:Q19
- ADD-03:Q20
- ADD-03:AppA/para1
- ADD-03:F4-H/image/hdr-en
- ADD-03:F4-H/image/hdr-ar
- ADD-03:F4-H/image/ref-en
- ADD-03:F4-H/image/ref-ar
- ADD-03:F4-H/image/form-en
- ADD-03:F4-H/image/form-ar
- ADD-03:F4-H/image/title
- ADD-03:F4-H/image/intro
- ADD-03:F4-H/image/decl1
- ADD-03:F4-H/image/decl2
- ADD-03:F4-H/image/decl3
- ADD-03:F4-H/image/table-header
- ADD-03:F4-H/image/table-row4
- ADD-03:F4-H/image/table-row4-cells
- ADD-03:F4-H/image/field-member-en
- ADD-03:F4-H/image/field-member-ar
- ADD-03:F4-H/image/field-cr-en
- ADD-03:F4-H/image/field-cr-ar
- ADD-03:F4-H/image/field-signatory-en
- ADD-03:F4-H/image/field-signatory-ar
- ADD-03:F4-H/image/field-capacity-en
- ADD-03:F4-H/image/field-capacity-ar
- ADD-03:F4-H/image/field-date-en
- ADD-03:F4-H/image/field-date-ar
- ADD-03:F4-H/image/field-signature-en
- ADD-03:F4-H/image/field-signature-ar
- ADD-03:F4-H/image/note
- ADD-03:F4-H/image/image-footer
- ADD-03:AppB/para1
- ADD-03:F4-H/para1
- ADD-03:F4-H/T1/1
- ADD-03:F4-H/T1/2
- ADD-03:F4-H/T1/3
- ADD-03:F4-H/T1/4
- ADD-03:F4-H/para2

## Items

| id | type | provision | target | status | why (first failed check) |
|---|---|---|---|---|---|
| ADD-03/4.1(a) | amendment_op | ADD-03:4.1 | VOL-V:18.1 | evidence_verified |  |
| ADD-03/4.1(b) | amendment_op | ADD-03:4.1 | VOL-V:18.4 | evidence_verified |  |
| ADD-03/5.1 | amendment_op | ADD-03:5.1 | VOL-II:5.2 | evidence_verified |  |
| ADD-03/6.1 | amendment_op | ADD-03:6.1 | ADD-02:T1-1-rev | evidence_verified |  |
| ADD-03/5.2 | amendment_op | ADD-03:5.2 | ADD-01:5.1 | interpretation_pending | depends on interpretation S5: a person must confirm it |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S1: ADD-03 Section 4.1 deletes 'SAR 180,000 for each day of delay' in VOL-V Clause 18.1 and substitutes a rate of 0.05% of the Estimated Project Cost per day; the quoted old words occur once in VOL-V:18.1 at ADD-02. — evidence verified
- **fact** S2: ADD-03 Section 4.1 states that VOL-V Clause 18.4 (aggregate cap of 10% of the Estimated Project Cost) is unchanged; by the approved cap calculation the cap is reached after 200 days of delay at the new rate. — evidence verified
- **fact** S3: ADD-03 Section 5.1 substitutes '1.5 m/s' for '2.0 m/s' in VOL-II Clause 5.2; the residual head of 15 m stays. — evidence verified
- **fact** S4: ADD-03 Section 5.2 amends ADD-01 Section 5.1 (whose op wrote the GRP sentence into VOL-II:5.3) with effect from 8 October 2026; ADD-03 is dated 'Issued 9 November 2026', so the stated effective date precedes the issue date. — evidence verified
- **fact** S6: ADD-03 Section 6.1 deletes Table 1-1 (revised) and its Notes issued by ADD-02 and replaces them with Table 1-1 (second revision), which adds criterion G (20 marks); rows A to F carry the same marks; the total becomes 120. — evidence verified
- **fact** S7: The new Notes (ADD-03:S6/para1) are parsed as a separate paragraph, not as notes of ADD-03:T1-1, so the replace_unit removes the ADD-02 notes but does not bring in the new ones. The new notes change the threshold wording from 'seventy (70) marks' to 'seventy per cent (70%)' and the weighting from 6… — evidence verified
- **interpretation** S5: The retroactive effective date (8 October 2026, before the 9 November 2026 issue) is taken as printed; whether it affects anything done between those dates is for a person to decide. — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone
- units changed: ADD-02:T1-1-rev, ADD-02:T1-1-rev/A, ADD-02:T1-1-rev/B, ADD-02:T1-1-rev/C, ADD-02:T1-1-rev/D, ADD-02:T1-1-rev/E, ADD-02:T1-1-rev/F, ADD-02:T1-1-rev/note(1), ADD-02:T1-1-rev/note(2), ADD-02:T1-1-rev/note(3), ADD-02:T1-1-rev/notes, ADD-02:T1-1-rev/total, ADD-03:T1-1, ADD-03:T1-1/A, ADD-03:T1-1/B, ADD-03:T1-1/C, ADD-03:T1-1/D, ADD-03:T1-1/E, ADD-03:T1-1/F, ADD-03:T1-1/G, ADD-03:T1-1/total, VOL-II:5.2, VOL-V:18.1
- rows citing them: ADD-02-T1-1-N3-01, VOL-II-5.2-01, VOL-II-5.2-02
- rows that would be STALE: VOL-I-11.3-01, VOL-I-T1-1-B, VOL-I-T1-1-D, VOL-I-T1-1-A, VOL-I-T1-1-C, VOL-I-T1-1-E, VOL-I-T1-1-F, VOL-II-5.2-01, VOL-II-5.2-02, VOL-V-12.1-01
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 2
  - ADD-03/4.1(a) [A1]: ADD-03/4.1(a) (replace_text) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'In Volume V Clause 18.1, ‘SAR 180,000 for each day of delay’ is deleted and ‘one-twentieth of on…
  - ADD-03/6.1 [A1]: ADD-03/6.1 (replace_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Table 1-1 (revised) and the Notes to it, issued by Section 3 of Addendum No. 2, are deleted and rep…
- clarification entries citing changed units: CQ-DWF-STORM-FLOW, CQ-VOL-III-DRAWINGS, CQ-PCOD-RELIABILITY-RUN, CQ-SCORING-METHOD
- A3: enters none; leaves none
- programme: 1 activity change(s)

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind04-s11-20261004T222214Z-analysis-002-critic`, route **host**; 1 item(s) reviewed

- **ADD-03/6.1** (evidence_verified): critic agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
  - concern: The target is right: ADD-03:6.1 names 'Table 1-1 (revised) ... issued by Section 3 of Addendum No. 2', which matches ADD-02:T1-1-rev. The replacement ADD-03:T1-1 is 'Table 1-1 (second revision)'.
  - concern: The provision deletes and replaces the table AND its Notes. The op only maps the table group to ADD-03:T1-1. The new Notes (ADD-03:S6/para1) are not part of the replacement, so the ADD-02 notes would be removed with no replacement in this op. This is a real gap that the item flags correctly and that someone must resolve.
  - concern: The notes change is substantive. The old note says the threshold is 'seventy (70) marks'. The new note says 'seventy per cent (70%)'. With a total of 120 that is 84 marks, not 70. The wording 'unchanged' in the new note does not match the old note.
  - concern: The rationale's claims are not shown in the printed evidence. These are: rows A-F being 25/15/20/20/10/10, the old 65/35 weighting versus the new 70/30, and the 12-unit versus 9-unit counts. Only G=20 and total=120 are quoted, so I could not verify these.
  - concern: The unit status of ADD-03:6.1 is printed as 'not_issued'. The evidence does not explain this, and a person should check it.
  - checked: ADD-03:6.1, ADD-02:T1-1-rev, ADD-03:T1-1, S6 cells G=20 and total=120, S7 quotations of the old and new threshold notes

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261004T223447Z-d132/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261004T223447Z-d132 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
