# Review request: ADD-03, run ADD-03-host-20261004T143400Z-5c8c

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (the CLI's default model; recorded from the CLI output)`; reported `None`
- status **partial**; created 2026-10-04T14:34:00Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 8b7bf5f1d0dbab0e…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 7 of 35 provisions accounted for
- resolution (kept apart from coverage): 5 resolved, 2 pending a person, 0 invalid, 28 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

## Findings (a person looks at each)

- 1 provision with amendment language carries no change (0 contradict a change the pattern drafter drafts from their words: invalid; 1 need a person): ADD-03:1.2

## Provisions not accounted for (a person treats each)

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
- ADD-03:Q15
- ADD-03:Q16
- ADD-03:Q17
- ADD-03:Q18
- ADD-03:Q19
- ADD-03:AppA/para1
- ADD-03:F4-G/T1/1
- ADD-03:F4-G/T1/2
- ADD-03:F4-G/T1/3
- ADD-03:F4-G/T1/4
- ADD-03:F4-G/T1/5
- ADD-03:F4-G/T1/6
- ADD-03:F4-G/T1/7
- ADD-03:F4-G/para1

## Items

| id | type | provision | target | status | why (first failed check) |
|---|---|---|---|---|---|
| ADD-03/cover/para1 | disposition | ADD-03:cover/para1 |  | evidence_verified |  |
| ADD-03/cover/para2 | disposition | ADD-03:cover/para2 |  | evidence_verified |  |
| ADD-03/1.1 | disposition | ADD-03:1.1 |  | evidence_verified |  |
| ADD-03/2.1 | amendment_op | ADD-03:2.1 | VOL-I:2.4 | evidence_verified |  |
| ADD-03/2.2 | amendment_op | ADD-03:2.2 | VOL-I:2.4 | evidence_verified |  |
| ADD-03/cover/para3 | disposition | ADD-03:cover/para3 |  | interpretation_pending | depends on interpretation S2: a person must confirm it |
| ADD-03/1.2 | disposition | ADD-03:1.2 |  | insufficient_evidence | semantic: no_effect on amendment language (its words carry 'unless'), and the reason quotes none of the provision's words: insufficient evidence that it changes nothing |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S1: ADD-03 Section 2.2 notifies Sunday 22 November 2026 as an office-closure day; at ADD-02 the calendar treats that day as a Working Day (no notified days yet). — evidence verified
- **interpretation** S2: The cover sentence that the closure 'does not affect any deadline' appears to conflict with Sections 2.1/2.2, which make 22 November 2026 a non-Working Day and so can move deadlines counted in Working Days. A person must decide which governs. — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone; NOT clean: 1 provision with amendment language carries no change (0 contradict a change the pattern drafter drafts from their words: invalid; 1 need a person): ADD-03:1.2
- units changed: VOL-I:2.4
- rows citing them: none
- rows that would be STALE: none
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 0
- clarification entries citing changed units: none
- A3: enters none; leaves none
- programme: 35 activity change(s)

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261004T143400Z-5c8c/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261004T143400Z-5c8c --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
