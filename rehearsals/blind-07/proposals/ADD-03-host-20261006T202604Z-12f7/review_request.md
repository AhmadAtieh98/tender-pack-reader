# Review request: ADD-03, run ADD-03-host-20261006T202604Z-12f7

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (the CLI's default model; recorded from the CLI output)`; reported `None`
- status **partial**; created 2026-10-06T20:26:04Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 8987c98f5ba445d4…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 2 of 49 provisions accounted for
- resolution (kept apart from coverage): 0 resolved, 2 pending a person, 3 invalid, 44 unaccounted; evidence_verified checks quotations, not meaning
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
- ADD-03:3.1
- ADD-03:3.2
- ADD-03:3.3
- ADD-03:3.4
- ADD-03:3.5
- ADD-03:3.6
- ADD-03:4.1
- ADD-03:4.2
- ADD-03:4.3
- ADD-03:4.4
- ADD-03:Q15
- ADD-03:Q16
- ADD-03:Q17
- ADD-03:AppA/para1
- ADD-03:T42-1/image/r1
- ADD-03:T42-1/image/r2
- ADD-03:T42-1/image/r3
- ADD-03:T42-1/image/r4
- ADD-03:T42-1/image/r5
- ADD-03:T42-1/image/notes-heading
- ADD-03:T42-1/image/note1
- ADD-03:T42-1/image/note2
- ADD-03:T42-1/image/note3
- ADD-03:T42-1/image/signatory
- ADD-03:T42-1/image/english
- ADD-03:AppA/para2
- ADD-03:AppB/para1
- ADD-03:AppB/para2
- ADD-03:T42-1/1
- ADD-03:T42-1/2
- ADD-03:T42-1/3
- ADD-03:T42-1/4
- ADD-03:T42-1/5
- ADD-03:T42-1/notes
- ADD-03:T42-1/note(1)
- ADD-03:T42-1/note(2)
- ADD-03:T42-1/note(3)
- ADD-03:T42-1/note(4)
- ADD-03:AppB/para3

## Items

| id | type | provision | target | status | why (first failed check) |
|---|---|---|---|---|---|
| ADD-03/Q19 | disposition | ADD-03:Q19 |  | evidence_verified |  |
| ADD-03/Q18-issue | issue | ADD-03:Q18 |  | interpretation_pending |  |
| ADD-03/Q18 | disposition | ADD-03:Q18 |  | insufficient_evidence | evidence VOL-V:39.5 p0: page 0 is not a page of VOL-V:39.5 ([4]) |
| ADD-03/Q15 | amendment_op | ADD-03:Q15 | ADD-01:3.2 | invalid | previous_value: no target to compare the previous value "Bidders' attention is drawn to Volume I Clause 5.3. Statements recorded in the minutes at Appendix B are a record of what was said and do not bind the Authority u… |
| ADD-03/Q16 | amendment_op | ADD-03:Q16 | VOL-II:9.3 | invalid | previous_value: no target to compare the previous value 'A grievance mechanism accessible to the affected community shall be established before construction and maintained for the concession period.' with |
| ADD-03/Q17 | amendment_op | ADD-03:Q17 | VOL-I:10.6 | invalid | previous_value: no target to compare the previous value 'The Bidder shall submit with Form 4-F a schedule of the principal financing assumptions underlying the Availability Payment, including the assumed debt tenor, mar… |

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

## Values the proposer supplied for controller fields (ignored)

- {"item": "ADD-03/Q15", "proposer_status": "invalid", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:Q15 is a provision of ADD-03 (p2)", "aspect": "structure"}, {"check": "previous_value", "ok": false, "detail": "no target to compare the previous value \"Bidders' attenti
- {"item": "ADD-03/Q16", "proposer_status": "invalid", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:Q16 is a provision of ADD-03 (p2)", "aspect": "structure"}, {"check": "previous_value", "ok": false, "detail": "no target to compare the previous value 'A grievance mecha
- {"item": "ADD-03/Q17", "proposer_status": "invalid", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:Q17 is a provision of ADD-03 (p2)", "aspect": "structure"}, {"check": "interpretation", "ok": true, "detail": "an annotation that adds obligation is an interpretation of 
- {"item": "ADD-03/Q18", "proposer_status": "insufficient_evidence", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:Q18 is a provision of ADD-03 (p2)", "aspect": "structure"}, {"check": "evidence ADD-03:Q18 p2", "ok": true, "detail": "verbatim in ADD-03:Q18 at ADD-02", "a
- {"item": "ADD-03/Q18-issue", "proposer_status": "interpretation_pending", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:Q18 is a provision of ADD-03 (p2)", "aspect": "structure"}, {"check": "payload", "ok": true, "detail": "a well-formed issue payload", "aspect": "stru
- {"item": "ADD-03/Q19", "proposer_status": "evidence_verified", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:Q19 is a provision of ADD-03 (p2)", "aspect": "structure"}, {"check": "evidence ADD-03:Q19 p2", "ok": true, "detail": "verbatim in ADD-03:Q19 at ADD-02", "aspec

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261006T202604Z-12f7/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261006T202604Z-12f7 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
