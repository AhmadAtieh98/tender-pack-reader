# Review request: ADD-03, run ADD-03-host-20261006T201945Z-dcfc

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (the CLI's default model; recorded from the CLI output)`; reported `None`
- status **partial**; created 2026-10-06T20:19:45Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 8987c98f5ba445d4…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 7 of 49 provisions accounted for
- resolution (kept apart from coverage): 4 resolved, 3 pending a person, 0 invalid, 42 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

## Provisions not accounted for (a person treats each)

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
| ADD-03/cover/para1/disp | disposition | ADD-03:cover/para1 |  | evidence_verified |  |
| ADD-03/cover/para2/disp | disposition | ADD-03:cover/para2 |  | evidence_verified |  |
| ADD-03/1.1/disp | disposition | ADD-03:1.1 |  | evidence_verified |  |
| ADD-03/1.2/disp | disposition | ADD-03:1.2 |  | evidence_verified |  |
| ADD-03/1.3/disp | disposition | ADD-03:1.3 |  | evidence_verified |  |
| ADD-03/2.1/disp | disposition | ADD-03:2.1 | VOL-V:36.2 | evidence_verified |  |
| ADD-03/cover/para3 | amendment_op | ADD-03:cover/para3 | ADD-03:cover/para3 | interpretation_pending | an annotation that adds obligation is an interpretation of the provision: a person confirms it |
| ADD-03/cover/para3/issue | issue | ADD-03:2.1 | VOL-V:36.2 | interpretation_pending |  |
| ADD-03/2.2/row | row_new | ADD-03:2.2 | VOL-IV:F4-F | invalid | payload: not a register.Row: 2 validation errors for Row interpretations.0.consequence.Consequence Input should be a valid dictionary or instance of Consequence [type=model_type, input_value='none stated in this provisi… |

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

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-20261006T201359Z-2503-analysis-001-critic`, route **host**; 1 item(s) reviewed

- **ADD-03/cover/para3** (interpretation_pending): critic DOES NOT agree — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: Target is the provision itself (cover/para3), not a unit of the pack that the provision amends. The op type 'annotate' on the cover paragraph does not amend any pack target; the obligation to acknowledge receipt in Form 4-A should be linked to Form 4-A (or the relevant requirement unit) if it exists. The evidence shown does not identify Form 4-A's unit, so the target is uncertain.
  - concern: The cover text summarises and does not amend (shared policy). Treating a cover sentence as an operative obligation with effect 'adds_obligation' conflicts with that rule. Whether the cover sentence creates an obligation, or whether an operative provision elsewhere does, is for a person to decide. The item should be an uncertain target or an issue, not an op with a stated effect.
  - concern: The note says other cover statements, e.g. 'SAR 4,000,000 in Vol V 36.2', differ from operative clause 2.1, and are reported in a separate issue. The evidence shown does not include clause 2.1 or that issue, so this claim can't be checked. The cover/operative differences are not quoted on both sides here, as the policy requires.
  - concern: The cover also lists other changes: Table 42-1 issued in Arabic, Clause 12.5, borehole core inspection with an exception to Vol I Clause 4.2, and clarifications 15-19. This item does not account for them. The rationale says other batches cover them, but that can't be verified from this request.
  - concern: The cover text ends 'All other terms of the RFP Documents remain unchanged.' Its relationship to the new obligation is not addressed. No consequence for failing to acknowledge is stated in the evidence, and none should be inferred.
  - concern: The controller marks this interpretation_pending, which is appropriate. The quoted words 'Bidders shall acknowledge receipt in Form 4-A.' are verbatim, so the evidence quotation itself is fine.
  - checked: ADD-03:cover/para3: 'Bidders shall acknowledge receipt in Form 4-A.', ADD-03:cover/para3: 'All other terms of the RFP Documents remain unchanged.', controller_validation records (provision, interpretation, evidence, engine)

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261006T201945Z-dcfc/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261006T201945Z-dcfc --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
