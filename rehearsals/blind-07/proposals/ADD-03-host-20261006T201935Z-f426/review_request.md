# Review request: ADD-03, run ADD-03-host-20261006T201935Z-f426

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (the CLI's default model; recorded from the CLI output)`; reported `None`
- status **partial**; created 2026-10-06T20:19:35Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 8987c98f5ba445d4…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 5 of 49 provisions accounted for
- resolution (kept apart from coverage): 0 resolved, 4 pending a person, 1 invalid, 44 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

## Findings (a person looks at each)

- 1 provision with amendment language carries no change (0 contradict a change the pattern drafter drafts from their words: invalid; 1 need a person): ADD-03:3.2

## Provisions not accounted for (a person treats each)

- ADD-03:cover/para1
- ADD-03:cover/para2
- ADD-03:cover/para3
- ADD-03:1.1
- ADD-03:1.2
- ADD-03:1.3
- ADD-03:2.1
- ADD-03:2.2
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
| ADD-03/3.5 | disposition | ADD-03:3.5 |  | evidence_verified |  |
| ADD-03/3.2 | disposition | ADD-03:3.2 |  | interpretation_pending | semantic: no_effect on amendment language: a person must confirm (its words carry 'renumbered') |
| ADD-03/3.5-issue | issue | ADD-03:3.5 | ADD-03:T42-1 | insufficient_evidence | evidence ADD-03:T42-1/4 p4: cell evidence needs a column of ADD-03:T42-1/4 (['Asset class', 'Maximum condition grade', 'Minimum residual life (years)', 'No']) |
| ADD-03/3.3 | amendment_op | ADD-03:3.3 | VOL-V:42.1 | conflicting | dependencies: unknown ids ['ADD-03/3.1(a)'] |
| ADD-03/3.4 | amendment_op | ADD-03:3.4 | VOL-V:42.1 | conflicting | statements: fact S1 is not supported verbatim |
| ADD-03/3.1(a) | escalation | ADD-03:3.1 | VOL-V:42.3 | escalated |  |
| ADD-03/3.4-issue | escalation | ADD-03:3.4 | ADD-03:T42-1 | escalated |  |
| ADD-03/3.1(b) | amendment_op | ADD-03:3.1 | VOL-II:8.5 | invalid | previous_value: 'active' does not match VOL-II:8.5 at ADD-02 (it reads: 'A handback condition survey shall be carried out in the final two (2) years of the concession, and any remedial works identified shall be complete… |
| ADD-03/3.6 | row_new | ADD-03:3.6 |  | invalid | payload: not a register.Row: 5 validation errors for Row scope Input should be a valid list [type=list_type, input_value='Technical Proposal', input_type=str] For further information visit https://errors.pydantic.dev/2.… |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S1: Crop ADD-03:T42-1/image (Arabic, page 3) shows row 4 minimum residual life as ٧ (7) and row 5 as ٢٤ شهراً (24 months). The English Appendix B rows ADD-03:T42-1/4 and /5 state 5 and 24 (years). — evidence NOT verified
- **interpretation** S2: ambiguous: ADD-03:3.5 says 'The Arabic text governs', so rows 4 and 5 may read 7 years and 24 months, but whether that prevails over the English is a person's decision; the 3.5 wording is not applied here. — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone; NOT clean: 1 provision with amendment language carries no change (0 contradict a change the pattern drafter drafts from their words: invalid; 1 need a person): ADD-03:3.2
- units changed: none
- rows citing them: none
- rows that would be STALE: none
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 0
- clarification entries citing changed units: none
- A3: enters none; leaves none
- programme: 48 activity change(s)

## Values the proposer supplied for controller fields (ignored)

- {"item": "ADD-03/3.1(a)", "proposer_status": "escalated", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:3.1 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "payload", "ok": true, "detail": "a well-formed escalation payload", "aspect": "structure"}, {"
- {"item": "ADD-03/3.1(b)", "proposer_status": "invalid", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:3.1 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "previous_value", "ok": false, "detail": "'active' does not match VOL-II:8.5 at ADD-02 (it reads:
- {"item": "ADD-03/3.2", "proposer_status": "interpretation_pending", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:3.2 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "evidence ADD-03:3.2 p1", "ok": true, "detail": "verbatim in ADD-03:3.2 at ADD-02", "
- {"item": "ADD-03/3.3", "proposer_status": "conflicting", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:3.3 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "previous_value", "ok": true, "detail": "'The Project Company shall transfer the Facility to the
- {"item": "ADD-03/3.4", "proposer_status": "conflicting", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:3.4 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "previous_value", "ok": true, "detail": "'The Project Company shall transfer the Facility to the
- {"item": "ADD-03/3.4-issue", "proposer_status": "escalated", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:3.4 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "payload", "ok": true, "detail": "a well-formed escalation payload", "aspect": "structure"},
- {"item": "ADD-03/3.5-issue", "proposer_status": "insufficient_evidence", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:3.5 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "payload", "ok": true, "detail": "a well-formed issue payload", "aspect": "struc
- {"item": "ADD-03/3.5", "proposer_status": "evidence_verified", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:3.5 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "evidence ADD-03:3.5 p1", "ok": true, "detail": "verbatim in ADD-03:3.5 at ADD-02", "aspec
- {"item": "ADD-03/3.6", "proposer_status": "invalid", "proposer_validation": [{"check": "provision", "ok": true, "detail": "ADD-03:3.6 is a provision of ADD-03 (p1)", "aspect": "structure"}, {"check": "payload", "ok": false, "detail": "not a register.Row: 5 validation errors for Row scope Input shoul

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-20261006T201359Z-2503-analysis-002-critic`, route **host**; 5 item(s) reviewed

- **ADD-03/3.1(a)** (escalated): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The 'software limitation' class fits: the dry run rejected insert_unit for VOL-V:42.3, which does not exist, and for VOL-V:42.2, which the provision does not cite. That is a tool limitation, not missing evidence.
  - concern: The provision says 'relocated'. Only the insertion of 42.3 is escalated here. The matching removal or relocation of VOL-II:8.5 is not covered by this item, and a person should confirm it is handled. VOL-II:8.5 is not shown as a unit with a stage text, so I cannot confirm that either way.
  - concern: The statement that the text is unchanged rests on ADD-03:3.1. The comparison with VOL-II:8.5 matches word for word on the evidence shown. The placement 'after VOL-V:42.2' is the proposer's inference, because the provision does not name a position. It should be flagged as such.
  - checked: ADD-03:3.1, VOL-II:8.5 span (verbatim, p5), controller validation records (all ok)
- **ADD-03/3.3** (conflicting): critic DOES NOT agree — selected because conflicting; model claude-sonnet-5-5
  - concern: The replace_text op matches the provision wording and the previous_value of VOL-V:42.1 as it stood at ADD-02.
  - concern: The dependency id 'ADD-03/3.1(a)' failed validation as an unknown id. The dependency should be fixed or restated.
  - concern: Ops 3.3 and 3.4 both change VOL-V:42.1 at different spans. The controller flagged this as a consistency conflict. The two spans, 'Volume II Clause 8.5' and 'with a remaining design life...', do not overlap, so they look compatible. Whether the flag is a real conflict is for a person to decide. The item should say that the two ops are applied in sequence on the same unit and do not overlap.
  - concern: The change makes 42.1 point to Clause 42.3, which exists only if the escalated insertion in 3.1(a) is recorded. A person must resolve that first.
  - concern: The rationale says 'Simulated valid', but the dependency check failed. The rationale should not suggest a clean result.
  - checked: ADD-03:3.3, VOL-V:42.1 text at ADD-02, controller validation: dependencies ok=false, consistency ok=false
- **ADD-03/3.4** (conflicting): critic DOES NOT agree — selected because conflicting; model claude-sonnet-5-5
  - concern: The replace_text op matches the provision wording and the target text.
  - concern: The controller says fact S1 is not supported verbatim, and the item itself declares missing information. The item therefore rests on unsupported evidence.
  - concern: The item states the Arabic row 5 value as '24 months' and the English as '24 (years)'. The English cell reads 24 under the column 'Minimum residual life (years)', and the Arabic reads ٢٤ شهراً, which means 24 months. S1 is presented as a fact. The conflict between 7 and 5, and between 24 months and 24 years, is a matter for a person and should not be framed as a settled fact.
  - concern: Evidence span for VOL-V:42.1 on page 4 is 'free of encumbrance and with a remaining design life...' and the proposer gives only part of the sentence. This is acceptable as a span, but the key change appears in the replacement text.
  - concern: The new wording makes 42.1 depend on Table 42-1. Which rendering of rows 4 and 5 applies is unresolved. The item correctly does not apply ADD-03:3.5. Even so, it is submitted as an amendment op that cannot be fully evaluated until the table question is settled.
  - concern: The consistency flag with 3.3 remains. The model rationale mixes an op with an issue; it should be kept apart.
  - concern: The rationale mentions English note (4) about the electrical equipment design life in Volume II Clause 2.2 being increased to 25 years. This is outside the batch but could be a further amendment and is not accounted for in the items shown. It should be listed as follow-on work.
  - checked: ADD-03:3.4, VOL-V:42.1 text at ADD-02, S1 and S2 as printed, controller validation: statements S1 not verbatim, missing_information, consistency
- **ADD-03/3.4-issue** (escalated): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The sentence 'Table 42-1 is reproduced at Appendix A to this Addendum and forms part of Volume V.' does make the table part of Volume V. The software limitation class fits, because no op type inserts a table.
  - concern: The target ADD-03:T42-1 is the addendum's own table, not a VOL-V unit. The controller marked this as an uncertain target. A person should record where the table lands in Volume V.
  - concern: Appendix A is described as the place where the table is reproduced, while the Arabic rendering is on page 3 and the English at Appendix B is on page 4. The item does not say which one is 'Appendix A', so a person should check this. I cannot tell from the evidence shown.
  - checked: ADD-03:3.4 final sentence, ADD-03:T42-1, controller validation (all ok)
- **ADD-03/3.5-issue** (insufficient_evidence): critic DOES NOT agree — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The issue is well founded in substance. 3.5 says the Arabic governs, and the Arabic rows 4 and 5 appear to differ from the English. The issue correctly reserves the reading for Legal.
  - concern: The controller status is insufficient_evidence. The two English cell evidence entries failed because they carry no column, and fact S1 is not supported verbatim. The evidence therefore needs correcting before the item can stand.
  - concern: The issue text opens with 'ambiguous/conflict', which merges two classes. The rules require one class per point. Here the real point is a conflict between the Arabic and English renderings, with 3.5 stating which governs. Whether the Arabic overrides the English is for a person, so it should be put as ambiguous or as a conflict, not both.
  - concern: The English table row 5 gives 24 under a column headed 'years', and the Arabic gives 24 months in a column headed (سنة). I cannot verify from the evidence that the Arabic cell reading is complete. The crop itself is not shown, so the reading is not checked against the image here.
  - concern: The issue brings in the Arabic header date ١٥ نوفمبر ٢٠٢٦م and number ٤١٧/٢٠٢٦ with no evidence entry, and no reason is given for why it matters. Either quote it with evidence or remove it.
  - concern: The issue notes that rows 1 to 3 match. No evidence for rows 1 to 3 is listed in the item, so that claim is unsupported here.
  - checked: ADD-03:3.5, ADD-03:T42-1/image/r4 and /r5 readings, ADD-03:T42-1/4 and /5 cells (failed validation for missing column), controller validation: S1 not verbatim

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261006T201935Z-f426/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261006T201935Z-f426 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
