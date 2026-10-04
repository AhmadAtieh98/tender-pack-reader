# Review request: ADD-03, run ADD-03-host-20261004T143515Z-5604

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (the CLI's default model; recorded from the CLI output)`; reported `None`
- status **partial**; created 2026-10-04T14:35:15Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 8b7bf5f1d0dbab0e…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 0 of 35 provisions accounted for
- resolution (kept apart from coverage): 0 resolved, 0 pending a person, 8 invalid, 27 unaccounted; evidence_verified checks quotations, not meaning
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
| ADD-03/3.1 | amendment_op | ADD-03:3.1 | VOL-I:8.8 | invalid | state: the item's state differs from the set's state |
| ADD-03/3.2 | amendment_op | ADD-03:3.2 | VOL-I:8.1 | invalid | state: the item's state differs from the set's state |
| ADD-03/3.3 | amendment_op | ADD-03:3.3 | ADD-03:3.3 | invalid | state: the item's state differs from the set's state |
| ADD-03/3.4 | amendment_op | ADD-03:3.4 | VOL-I:8.1 | invalid | state: the item's state differs from the set's state |
| ADD-03/4.1 | escalation | ADD-03:4.1 | VOL-IV:F4-C/image/decl4 | invalid | state: the item's state differs from the set's state |
| ADD-03/4.2 | escalation | ADD-03:4.2 | VOL-IV:F4-C/image/decl4 | invalid | state: the item's state differs from the set's state |
| ADD-03/4.3 | disposition | ADD-03:4.3 | VOL-I:9.4 | invalid | state: the item's state differs from the set's state |
| ADD-03/4.4 | amendment_op | ADD-03:4.4 | VOL-I:9.4 | invalid | state: the item's state differs from the set's state |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S1: VOL-I:8.8 at ADD-02 is active and ADD-03:3.1 prints an addition at its end. — evidence verified
- **fact** S3: Form 4-C declaration 4 is read from an image (VOL-IV:F4-C/image/decl4, page 6); the crop shows 'رابعاً' followed by the 'correct and complete' sentence and the exclusion sentence over two lines, matching the ADD-03:4.1 quotation. — evidence verified
- **interpretation** S2: Sections 3.2-3.4 and 4.4 create new Bidder obligations; they are recorded as annotations (adds_obligation) on the clauses they refer to, not as text changes. — needs a person

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261004T143515Z-5604/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261004T143515Z-5604 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
