# Review request: ADD-03, run ADD-03-host-20261008T060042Z-c2e0

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (claude-opus-5-5)`; reported `None`
- status **partial**; created 2026-10-08T06:00:42Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build e5d1ff4e390aab4b…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 19 of 52 provisions accounted for
- resolution (kept apart from coverage): 12 resolved, 7 pending a person, 0 invalid, 33 unaccounted; evidence_verified checks quotations, not meaning
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
- ADD-03:3.1
- ADD-03:3.2
- ADD-03:3.3
- ADD-03:3.4
- ADD-03:4.1
- ADD-03:4.2
- ADD-03:Q15
- ADD-03:Q16
- ADD-03:Q17
- ADD-03:Q18
- ADD-03:Q19
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
| D-hdr-en | disposition | ADD-03:p3-image/hdr-en |  | evidence_verified |  |
| D-hdr-ar | disposition | ADD-03:p3-image/hdr-ar |  | evidence_verified |  |
| D-date | disposition | ADD-03:p3-image/date |  | evidence_verified |  |
| D-ref | disposition | ADD-03:p3-image/ref |  | evidence_verified |  |
| D-to | disposition | ADD-03:p3-image/to |  | evidence_verified |  |
| D-subject | disposition | ADD-03:p3-image/subject |  | evidence_verified |  |
| D-tender | disposition | ADD-03:p3-image/tender |  | evidence_verified |  |
| D-notes-heading | disposition | ADD-03:p3-image/notes-heading |  | evidence_verified |  |
| D-stamp | disposition | ADD-03:p3-image/stamp |  | evidence_verified |  |
| D-signatory | disposition | ADD-03:p3-image/signatory |  | evidence_verified |  |
| D-image-footer | disposition | ADD-03:p3-image/image-footer |  | evidence_verified |  |
| D-AppA-para2 | disposition | ADD-03:AppA/para2 |  | evidence_verified |  |
| D-AppA-para1 | disposition | ADD-03:AppA/para1 |  | interpretation_pending | depends on interpretation S-I1: a person must confirm it |
| D-r1 | disposition | ADD-03:p3-image/r1 |  | interpretation_pending | depends on interpretation S-I1: a person must confirm it |
| D-r2 | disposition | ADD-03:p3-image/r2 |  | interpretation_pending | depends on interpretation S-I1: a person must confirm it |
| D-r3 | disposition | ADD-03:p3-image/r3 |  | interpretation_pending | depends on interpretation S-I1: a person must confirm it |
| D-note1 | disposition | ADD-03:p3-image/note1 |  | interpretation_pending | depends on interpretation S-I1: a person must confirm it |
| D-note2 | disposition | ADD-03:p3-image/note2 |  | interpretation_pending | depends on interpretation S-I1: a person must confirm it |
| D-note3 | disposition | ADD-03:p3-image/note3 |  | interpretation_pending | depends on interpretation S-I1: a person must confirm it |
| I-r2-discrepancy | issue | ADD-03:p3-image/r2 | ADD-03:p3-image/r2 | interpretation_pending |  |
| Q-r2-period | clarification | ADD-03:p3-image/r2 | ADD-03:p3-image/r2 | interpretation_pending |  |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S-F1: Clause 2.2 states that Table 8-1 forms part of Volume I and that the Arabic text governs. — evidence verified
- **fact** S-F2: The Arabic Table 8-1 row 2 issue period cell reads ٥ (image reading, pending approval). — evidence verified
- **fact** S-F3: The English translation at Appendix B, row 2, prints an issue period of 3 Working Days. — evidence verified
- **fact** S-F4: Q16 states a two Working Day reduction of the row 2 issue period for an application lodged not later than Sunday 22 November 2026. — evidence verified
- **interpretation** S-I1: The Appendix A units (the Office's letter and the Arabic Table 8-1 rows and notes) are the content of the table that Clause 2.2 makes part of Volume I; that incorporation is the op for ADD-03:2.2 (another batch). The Appendix A units themselves amend no unit of the volumes. — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone
- units changed: none
- rows citing them: none
- rows that would be STALE: none
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 0
- clarification entries citing changed units: none
- A3: enters none; leaves none
- programme: 48 activity change(s)

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261008T060042Z-c2e0/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261008T060042Z-c2e0 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
