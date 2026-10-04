# Review request: ADD-03, run ADD-03-host-20261004T143646Z-6929

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (the CLI's default model; recorded from the CLI output)`; reported `None`
- status **partial**; created 2026-10-04T14:36:46Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 8b7bf5f1d0dbab0e…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 4 of 35 provisions accounted for
- resolution (kept apart from coverage): 1 resolved, 3 pending a person, 2 invalid, 29 unaccounted; evidence_verified checks quotations, not meaning
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
- ADD-03:6.2
- ADD-03:7.1
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
| ADD-03/6.1 | amendment_op | ADD-03:6.1 | VOL-V:29.3 | evidence_verified |  |
| ADD-03/7.2 | disposition | ADD-03:7.2 | ADD-02:7.2 | evidence_verified |  |
| ADD-03/5.1 | amendment_op | ADD-03:5.1 | VOL-II:T2-4/TP | insufficient_evidence | evidence VOL-II:T2-4/TP p3: the words are not verbatim in VOL-II:T2-4/TP cell Limit at ADD-02: 'Parameter: Total Phosphorus (TP) / Unit: mg/l / Limit: 1 / Basis of assessment: 30-day rolling average' |
| ADD-03/5.2 | disposition | ADD-03:5.2 | VOL-II:S3 | insufficient_evidence | missing_information: the proposer declares missing: a unit-level target in Volume II Section 3 |
| ADD-03/6.2(a) | amendment_op | ADD-03:6.2 | VOL-V:31.4 | invalid | previous_value: 'active' does not match VOL-V:31.4 at ADD-02 (it reads: 'Persistent breach, being three (3) or more Unavailability Events in any rolling ninety (90) day period, entitles the Authority to require a remedi… |
| ADD-03/6.2(b) | amendment_op | ADD-03:6.2 | VOL-V:39.3 | invalid | previous_value: 'active' does not match VOL-V:39.3 at ADD-02 (it reads: 'The Authority may terminate for persistent breach in the circumstances described in Clause 31.4.') |
| ADD-03/7.1 | amendment_op | ADD-03:7.1 | ADD-02:F4-G | invalid | previous_value: no target to compare the previous value 'FORM 4-G (9 units, six undertakings, Bidder signature only)' with |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S1: Table 2-4 (image reading) prints the TP row with Limit 1, unit mg/l, basis 30-day rolling average; the row unit VOL-II:T2-4/TP carries Limit 1 at ADD-02. — evidence NOT verified
- **interpretation** S2: The 'row for Total Phosphorus (TP)' in ADD-03 5.1 is the row unit VOL-II:T2-4/TP and the changed cell is Limit. — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone
- units changed: VOL-V:29.3
- rows citing them: VOL-V-29.3-01
- rows that would be STALE: VOL-V-29.3-01
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 0
- clarification entries citing changed units: CQ-PERSISTENT-BREACH
- A3: enters none; leaves none
- programme: 6 activity change(s)

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261004T143646Z-6929/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261004T143646Z-6929 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
