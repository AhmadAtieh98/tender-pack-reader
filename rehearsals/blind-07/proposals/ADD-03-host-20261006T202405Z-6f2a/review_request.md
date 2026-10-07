# Review request: ADD-03, run ADD-03-host-20261006T202405Z-6f2a

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (the CLI's default model; recorded from the CLI output)`; reported `None`
- status **partial**; created 2026-10-06T20:24:05Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 8987c98f5ba445d4…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 2 of 49 provisions accounted for
- resolution (kept apart from coverage): 1 resolved, 1 pending a person, 0 invalid, 47 unaccounted; evidence_verified checks quotations, not meaning
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
- ADD-03:4.2
- ADD-03:4.3
- ADD-03:Q15
- ADD-03:Q16
- ADD-03:Q17
- ADD-03:Q18
- ADD-03:Q19
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
| ADD-03/4.1 | amendment_op | ADD-03:4.1 | VOL-V:12.4 | evidence_verified |  |
| ADD-03/4.4/issue | issue | ADD-03:4.4 | VOL-I:4.2 | insufficient_evidence | evidence: no evidence given |
| ADD-03/4.4/esc | escalation | ADD-03:4.4 | VOL-I:4.2 | escalated | depends on interpretation S-4.4-interp: a person must confirm it |
| ADD-03/4.1/row | row_new | ADD-03:4.1 | VOL-V:12.4 | invalid | payload: not a register.Row: 2 validation errors for Row confidence Field required [type=missing, input_value={'id': 'A1-ADD03-4.1', 'g...llows a late notice.'}]}, input_type=dict] For further information visit https://… |
| ADD-03/4.2/row | row_new | ADD-03:4.2 |  | invalid | payload: not a register.Row: 2 validation errors for Row confidence Field required [type=missing, input_value={'id': 'A1-ADD03-4.2', 'g...a person to confirm."}]}, input_type=dict] For further information visit https://… |
| ADD-03/4.3/row | row_new | ADD-03:4.3 |  | invalid | payload: not a register.Row: 2 validation errors for Row confidence Field required [type=missing, input_value={'id': 'A1-ADD03-4.3', 'g... no date typed here."}]}, input_type=dict] For further information visit https://… |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S-4.1-fact: ADD-03:4.1 inserts a new Clause 12.5 in Volume V after Clause 12.4 (VOL-V:12.4 at ADD-02 is about monthly progress reports and site access). — evidence verified
- **assumption** S-4.3-assumption: PROVISIONAL ASSUMPTION: the date of this Addendum and the Proposal Due Date in force at ADD-03 are taken from the pack's own dates; no date has been computed here. The 3 Working Day dates are for the date-rule engine (calculate) to derive once those anchors are confirmed. — needs a person
- **interpretation** S-4.4-interp: ADD-03:4.4 disapplies Volume I Clause 4.2 (a clause carrying disqualification) for a limited class of communications; whether it is an exception, an interpretation or something else, and its exact scope ('to the extent that they concern the identification and handling of cores and records'), is for… — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone
- units changed: VOL-V:12.4+ADD-03
- rows citing them: none
- rows that would be STALE: none
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 1
  - ADD-03/4.1 [A1]: ADD-03/4.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-V:12.4; a row of the anchor VOL-V:12.4 does not count): 'The following ne…
- clarification entries citing changed units: none
- A3: enters none; leaves none
- programme: 48 activity change(s)

## Values the proposer supplied for controller fields (ignored)

- {"item": "ADD-03/4.1", "proposer_status": "evidence_verified", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:4.1 is a provision of ADD-03 (p2)", "aspect": "structure"}, {"check": "evidence ADD-03:4.1 p2", "ok": true, "detail": "verbatim in ADD-03:4.1 at ADD-02", "aspec
- {"item": "ADD-03/4.1/row", "proposer_status": "invalid", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:4.1 is a provision of ADD-03 (p2)", "aspect": "structure"}, {"check": "payload", "ok": false, "detail": "not a register.Row: 2 validation errors for Row confidence Fi
- {"item": "ADD-03/4.2/row", "proposer_status": "invalid", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:4.2 is a provision of ADD-03 (p2)", "aspect": "structure"}, {"check": "payload", "ok": false, "detail": "not a register.Row: 2 validation errors for Row confidence Fi
- {"item": "ADD-03/4.3/row", "proposer_status": "invalid", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:4.3 is a provision of ADD-03 (p2)", "aspect": "structure"}, {"check": "payload", "ok": false, "detail": "not a register.Row: 2 validation errors for Row confidence Fi
- {"item": "ADD-03/4.4/esc", "proposer_status": "escalated", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:4.4 is a provision of ADD-03 (p2)", "aspect": "structure"}, {"check": "payload", "ok": true, "detail": "a well-formed escalation payload", "aspect": "structure"}, {
- {"item": "ADD-03/4.4/issue", "proposer_status": "insufficient_evidence", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:4.4 is a provision of ADD-03 (p2)", "aspect": "structure"}, {"check": "payload", "ok": true, "detail": "a well-formed issue payload", "aspect": "struc

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-20261006T201359Z-2503-analysis-004-critic`, route **host**; 1 item(s) reviewed

- **ADD-03/4.1** (evidence_verified): critic agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
  - concern: Minor: new_text omits the clause number label '12.5' and the surrounding quotation marks. The number appears only in the provision's lead-in, so the A2 record should keep the lead-in and the new clause number together.
  - concern: Minor: the inserted clause creates an entitlement (extension of Scheduled PCOD and reasonable additional costs) conditional on notice within five (5) Working Days. The evidence shows no stated consequence for late notice beyond the proviso itself, so none should be inferred. The A1 row and the date rule (an event-based period, not a typed date) are listed as follow-on work, which is appropriate.
  - concern: Minor: the clause depends on the defined terms 'Scheduled PCOD' and 'Working Days' and on 'Revision C' of the Geotechnical Baseline Report. The evidence shown does not include the definitions or the report, so the dependency list covers only VOL-V:12.4. Whether the report was supplied in the pack is not shown here and should be checked separately.
  - checked: ADD-03:4.1: 'The following new Clause 12.5 is inserted in Volume V after Clause 12.4', VOL-V:12.4 text at ADD-02: 'The Project Company shall submit monthly progress reports and shall permit the Authority access to the site at all reasonable times.', new_text compared word for word with the quoted clause 12.5 in ADD-03:4.1, controller validation: provision, both evidence spans and the engine dry ru

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261006T202405Z-6f2a/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261006T202405Z-6f2a --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
