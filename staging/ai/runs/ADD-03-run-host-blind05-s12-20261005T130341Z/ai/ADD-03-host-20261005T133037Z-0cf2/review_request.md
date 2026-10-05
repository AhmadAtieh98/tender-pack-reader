# Review request: ADD-03, run ADD-03-host-20261005T133037Z-0cf2

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T13:30:37Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build e017ad321f216c3e…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 4 of 63 provisions accounted for
- resolution (kept apart from coverage): 1 resolved, 3 pending a person, 0 invalid, 59 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

## Findings (a person looks at each)

- 1 provision with amendment language carries no change (0 contradict a change the pattern drafter drafts from their words: invalid; 1 need a person): ADD-03:AppB/para1

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
- ADD-03:3.3(b)
- ADD-03:3.4
- ADD-03:4.1
- ADD-03:4.2
- ADD-03:5.1
- ADD-03:5.2
- ADD-03:Q15
- ADD-03:Q16
- ADD-03:Q17
- ADD-03:Q18
- ADD-03:Q19
- ADD-03:Q20
- ADD-03:Q21
- ADD-03:7.1
- ADD-03:7.2
- ADD-03:7.3
- ADD-03:7.4
- ADD-03:AppA/para1
- ADD-03:p4-image/hdr-en
- ADD-03:p4-image/hdr-ar
- ADD-03:p4-image/date
- ADD-03:p4-image/ref
- ADD-03:p4-image/subject
- ADD-03:p4-image/tender-ref
- ADD-03:p4-image/table-title
- ADD-03:p4-image/table-qualifier
- ADD-03:p4-image/col-lighting
- ADD-03:p4-image/col-height
- ADD-03:p4-image/col-description
- ADD-03:p4-image/col-zone
- ADD-03:p4-image/rowA-zone
- ADD-03:p4-image/rowA-description
- ADD-03:p4-image/rowA-height
- ADD-03:p4-image/rowA-lighting
- ADD-03:p4-image/rowB-zone
- ADD-03:p4-image/rowB-description
- ADD-03:p4-image/rowB-height
- ADD-03:p4-image/rowB-lighting
- ADD-03:p4-image/notes-heading
- ADD-03:p4-image/note1
- ADD-03:p4-image/note2
- ADD-03:p4-image/note3
- ADD-03:T5-1/a
- ADD-03:T5-1/b
- ADD-03:T5-1/notes
- ADD-03:T5-1/note(1)
- ADD-03:T5-1/note(2)
- ADD-03:T5-1/note(3)

## Items

| id | type | provision | target | status | why (first failed check) |
|---|---|---|---|---|---|
| ADD-03/AppA/para2 | disposition | ADD-03:AppA/para2 |  | evidence_verified |  |
| ADD-03/p4-image/signatory | disposition | ADD-03:p4-image/signatory |  | interpretation_pending | depends on interpretation S7: a person must confirm it |
| ADD-03/p4-image/stamp | disposition | ADD-03:p4-image/stamp |  | interpretation_pending | depends on interpretation S2: a person must confirm it |
| ADD-03/AppB/para1 | disposition | ADD-03:AppB/para1 |  | interpretation_pending | semantic: no_effect on amendment language: a person must confirm (its words carry 'provided') |
| ADD-03/AppB/para1-issue | issue | ADD-03:AppB/para1 | ADD-03:T5-1 | interpretation_pending |  |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S1: The signatory block of the Appendix A image prints only the title 'مدير المكتب' with a signature stroke beneath it. — evidence verified
- **fact** S3: ADD-03:AppA/para2 prints only 'End of reproduction.' — evidence verified
- **fact** S4: ADD-03:AppB/para1 states that the Appendix B translation is for convenience only and that the Arabic Table 5-1 at Appendix A governs; Clause 7.2 of ADD-03 states the same precedence. — evidence verified
- **fact** S6: The Arabic note 2 measures height from natural ground level before grading and filling; the English note (2) measures from finished ground level after grading and filling. The Arabic note 1 covers permanent and temporary structures including cranes and construction equipment; the English note (1) c… — evidence verified
- **interpretation** S2: In my visual reading of crop b13-right (sha256 92d27467...), the stamp block is an empty oval outline with no legible text, and the pack's reading transcribes nothing. No printed words can support this, so a person must confirm it against the crop. — needs a person
- **interpretation** S5: AppB/para1 restates the precedence already printed in ADD-03 Clause 7.2 and changes no unit as it stood at ADD-02 (Table 5-1 is first issued by ADD-03); the precedence itself is to be carried by the ops answering Clause 7.1/7.2 in another batch. — needs a person
- **interpretation** S7: A signatory title and an empty stamp outline attest the issuing Office's letter and print no change, obligation or exception. — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone; NOT clean: 1 provision with amendment language carries no change (0 contradict a change the pattern drafter drafts from their words: invalid; 1 need a person): ADD-03:AppB/para1
- units changed: none
- rows citing them: none
- rows that would be STALE: none
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 0
- clarification entries citing changed units: none
- A3: enters none; leaves none
- programme: 44 activity change(s)

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-s12-20261005T130341Z-analysis-009-critic`, route **host**; 4 item(s) reviewed

- **ADD-03/p4-image/signatory** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: Reading is only the title and a signature stroke; the signature stroke is not in the printed words, so a person should confirm against the crop. Whether the title alone authenticates the letter is not decided by this item.
  - checked: ADD-03:p4-image/signatory reading 'مدير المكتب', controller semantic check
- **ADD-03/p4-image/stamp** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: Evidence is only a crop with empty words; I cannot see the crop, so 'empty oval, no legible text' rests on the model's visual reading (S2) and must be confirmed by a person.
  - concern: Absence of text does not prove the stamp has no significance. Whether a blank stamp authenticates the letter is a separate human question.
  - checked: ADD-03:p4-image/stamp (empty text, crop hash only), controller validation
- **ADD-03/AppB/para1** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The controller flagged the semantic check as not ok ('provided' wording), so a person must confirm no_effect.
  - concern: The provision's words 'The Arabic text of Table 5-1 at Appendix A governs' do carry a precedence statement. no_effect holds only if that precedence is carried by the ops on Clause 7.1/7.2. That is asserted in S5 but is not shown in this evidence.
  - concern: Clause 7.2 is broader (the Arabic text generally governs) while AppB/para1 names Table 5-1 specifically, so it is a restatement rather than an exact duplicate.
  - checked: ADD-03:AppB/para1 text, ADD-03:7.2 quotation, controller semantic check (ok:false)
- **ADD-03/AppB/para1-issue** (interpretation_pending): critic agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The Arabic readings (note1, note2) are pending approval; the divergence rests on them.
  - concern: The issue payload says the column header carries the same difference and that English note 1 'says permanent structures including stacks'. Only note 2 English and the Arabic notes 1 and 2 are quoted. The English note (1) text and the Arabic and English headers are not quoted in the evidence shown, so those parts cannot be checked here.
  - concern: The target T5-1 is not among the cited units' own evidence, but it is the table the provision names. That fits.
  - concern: The conclusion that the Arabic governs rests on 7.2 and AppB/para1. A person decides the consequence.
  - checked: ADD-03:p4-image/note2 reading, ADD-03:T5-1/note(2) span, ADD-03:p4-image/note1 reading, ADD-03:AppB/para1, ADD-03:7.2 quotation

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T133037Z-0cf2/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T133037Z-0cf2 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
