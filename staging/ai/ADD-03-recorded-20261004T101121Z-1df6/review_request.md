# Review request: ADD-03, run ADD-03-recorded-20261004T101121Z-1df6

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **recorded** (provider recorded); model requested `recorded-fixture-model`; reported `recorded-fixture-model`
- status **partial**; created 2026-10-04T10:11:21Z; controller s09-ai-1
- state: pack NUPA-ISTP-2026-014-BLIND-02; evidence build 2f9a692b03d6bdc2…; validated ADD-03; working None; decisions none
- usage: 3 call(s), 46500 input / 1780 output tokens; cost not computed (no price configured)
- coverage: 5 of 42 provisions accounted for

## Provisions not accounted for (a person treats each)

- ADD-03:cover/para2
- ADD-03:cover/para3
- ADD-03:1.1
- ADD-03:1.2
- ADD-03:2.2
- ADD-03:2.3
- ADD-03:2.4
- ADD-03:3.2
- ADD-03:3.3
- ADD-03:4.1
- ADD-03:4.2
- ADD-03:4.3
- ADD-03:5.2
- ADD-03:5.3
- ADD-03:6.1
- ADD-03:6.2
- ADD-03:7.1
- ADD-03:Q15
- ADD-03:Q16
- ADD-03:Q17
- ADD-03:Q18
- ADD-03:Q19
- ADD-03:Q20
- ADD-03:Q21
- ADD-03:AppA/para1
- ADD-03:T2-2-rev/bod5
- ADD-03:T2-2-rev/cod
- ADD-03:T2-2-rev/total-suspended-solids
- ADD-03:T2-2-rev/total-nitrogen
- ADD-03:T2-2-rev/ammonia-nitrogen-nh4-n
- ADD-03:T2-2-rev/total-phosphorus
- ADD-03:T2-2-rev/temperature
- ADD-03:T2-2-rev/notes
- ADD-03:T2-2-rev/note(1)
- ADD-03:T2-2-rev/note(2)
- ADD-03:T2-2-rev/note(3)
- ADD-03:T2-2-rev/note(4)

## Items

| id | type | provision | target | status | why (first failed check) |
|---|---|---|---|---|---|
| ADD-03/2.1 | amendment_op | ADD-03:2.1 | VOL-I:6.1 | evidence_verified |  |
| ADD-03/3.1 | amendment_op | ADD-03:3.1 | VOL-I:7.1 | evidence_verified |  |
| ADD-03/cover/para1 | disposition | ADD-03:cover/para1 |  | evidence_verified |  |
| ADD-03/5.1 | amendment_op | ADD-03:5.1 | VOL-II:3.5 | insufficient_evidence | evidence ADD-03:5.1 p2: the words are not verbatim in ADD-03:5.1 at ADD-02: '‘45 dB(A) by night’ is deleted and ‘35 dB(A) by night’ is substituted' |
| ADD-03/7.2 | escalation | ADD-03:7.2 |  | escalated | depends on interpretation S2: a person must confirm it |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S1: ADD-03 2.1 substitutes 11:00 for 14:00 hours in VOL-I 6.1. — evidence verified
- **interpretation** S2: ADD-03 7.2 states a new Index of Forms row in prose; the index table itself is not reissued. — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone
- units changed: VOL-I:6.1, VOL-I:7.1
- rows citing them: VOL-I-6.1-01, VOL-I-7.1-01
- rows that would be STALE: VOL-I-6.1-01, VOL-I-5.2-01, VOL-I-6.3-01, VOL-I-6.4-01, VOL-I-6.4-02, VOL-I-7.1-01, VOL-I-8.3-01, VOL-I-8.5-01, VOL-IV-F4A-01, ADD-02-7.2-01, VOL-II-4.4-01, ADD-03-6.2-01, ADD-01-AppA-01, VOL-I-3.4-01, VOL-I-6.5-01, VOL-I-6.5-02, VOL-I-6.7-01, VOL-I-8.7-01, VOL-I-9.1-01, VOL-I-9.1h-01, VOL-I-9.5-01, VOL-I-9.6-01, VOL-I-9.7-01, VOL-I-10.1-01, VOL-I-10.3-01 (+12 more in proposals.yaml)
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 0
- clarification entries citing changed units: CQ-BOND-FC-COVERAGE
- A3: enters ['ADD-03-Q20-01']; leaves none
- programme: 33 activity change(s)

## Against the reference op file (report only)

- reference: blind rehearsal 02 curation (session 08): pattern drafter + assistant as curator; every op PROPOSED
- {'same': 2, 'partly': 2, 'different': 1, 'missed': 25, 'extra': 0}

## Next

- read every item above against its evidence (`staging/ai/ADD-03-recorded-20261004T101121Z-1df6/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-recorded-20261004T101121Z-1df6 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
