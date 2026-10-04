# Review request: ADD-03, run ADD-03-host-20261004T143825Z-cc12

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (the CLI's default model; recorded from the CLI output)`; reported `None`
- status **partial**; created 2026-10-04T14:38:25Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 8b7bf5f1d0dbab0e…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 14 of 35 provisions accounted for
- resolution (kept apart from coverage): 11 resolved, 3 pending a person, 0 invalid, 21 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

## Findings (a person looks at each)

- 2 provisions with amendment language carry no change (0 contradict a change the pattern drafter drafts from their words: invalid; 2 need a person): ADD-03:Q16, ADD-03:Q17

## Provisions not accounted for (a person treats each)

- ADD-03:cover/para1
- ADD-03:cover/para2
- ADD-03:cover/para3
- ADD-03:1.1
- ADD-03:1.2
- ADD-03:2.1
- ADD-03:2.2
- ADD-03:3.1
- ADD-03:3.2
- ADD-03:3.3
- ADD-03:3.4
- ADD-03:4.1
- ADD-03:4.2
- ADD-03:4.3
- ADD-03:4.4
- ADD-03:5.1
- ADD-03:5.2
- ADD-03:6.1
- ADD-03:6.2
- ADD-03:7.1
- ADD-03:7.2

## Items

| id | type | provision | target | status | why (first failed check) |
|---|---|---|---|---|---|
| ADD-03/Q15 | amendment_op | ADD-03:Q15 | ADD-02:Q9 | evidence_verified |  |
| ADD-03/Q19 | disposition | ADD-03:Q19 | VOL-I:9.4 | evidence_verified |  |
| ADD-03/AppA/para1 | amendment_op | ADD-03:AppA/para1 | ADD-02:F4-G | evidence_verified |  |
| ADD-03/Q16 | disposition | ADD-03:Q16 | VOL-II:9.4 | interpretation_pending | semantic: no_effect on amendment language: a person must confirm (its words carry 'shall' (cites VOL-II:9.4)) |
| ADD-03/Q17 | disposition | ADD-03:Q17 | VOL-I:8.1 | interpretation_pending | semantic: no_effect on amendment language: a person must confirm (its words carry 'must' (cites VOL-I:8.1)) |
| ADD-03/Q18 | amendment_op | ADD-03:Q18 | VOL-V:31.4 | interpretation_pending | depends on interpretation S3: a person must confirm it |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S1: ADD-03 Q15 states that the response to clarification request 9 in Addendum No. 2 is amended by adding a sentence at its end; ADD-02:Q9 is active at ADD-02. — evidence verified
- **fact** S2: Proposal Due Date at ADD-02 is Thursday 26 November 2026; four Working Days before it is Sunday 22 November 2026 (calculate add_working_days), matching Q17's date and ADD-03 3.2. — evidence verified
- **fact** S4: The reissued Form 4-G (ADD-03:F4-G, 10 units) differs from ADD-02:F4-G (9 units) by an added item 7 (security screening) and a countersignature line, the item 7 being beyond the stated purpose in 7.1 (countersignature). — evidence verified
- **interpretation** S3: Q18's cross-reference to deletion by Section 6.2 is treated as the same deletion that Section 6.2 makes; the op is proposed here for traceability and must be reconciled with the ADD-03/6.2 op (another batch) so VOL-V:31.4 is deleted once. — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone; NOT clean: 2 provisions with amendment language carry no change (0 contradict a change the pattern drafter drafts from their words: invalid; 2 need a person): ADD-03:Q16, ADD-03:Q17
- units changed: ADD-02:F4-G/T1, ADD-02:F4-G/T1/1, ADD-02:F4-G/T1/2, ADD-02:F4-G/T1/3, ADD-02:F4-G/T1/4, ADD-02:F4-G/T1/5, ADD-02:F4-G/T1/6, ADD-02:F4-G/para1, ADD-02:H:F4-G, ADD-02:Q9, ADD-03:F4-G/T1, ADD-03:F4-G/T1/1, ADD-03:F4-G/T1/2, ADD-03:F4-G/T1/3, ADD-03:F4-G/T1/4, ADD-03:F4-G/T1/5, ADD-03:F4-G/T1/6, ADD-03:F4-G/T1/7, ADD-03:F4-G/para1, ADD-03:H:F4-G
- rows citing them: ADD-02-F4G-01, ADD-02-F4G-02, ADD-02-F4G-03, ADD-02-F4G-04, ADD-02-F4G-05, ADD-02-F4G-06, ADD-02-F4G-07
- rows that would be STALE: VOL-I-9.4-01, VOL-IV-F4C-04, VOL-IV-F4C-N1, VOL-IV-F4C-01, VOL-IV-F4C-02, VOL-IV-F4C-03, VOL-IV-F4C-05
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 1
  - ADD-03/AppA/para1 [A1]: ADD-03/AppA/para1 (replace_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Form 4-G is reissued below in accordance with Section 7 of this Addendum. Bidders shall use …
- clarification entries citing changed units: CQ-F4C-EXCLUSION
- A3: enters none; leaves none
- programme: 2 activity change(s)

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261004T143825Z-cc12/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261004T143825Z-cc12 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
