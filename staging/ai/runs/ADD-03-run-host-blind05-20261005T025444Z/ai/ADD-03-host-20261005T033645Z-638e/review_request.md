# Review request: ADD-03, run ADD-03-host-20261005T033645Z-638e

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T03:36:45Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 77784d6d270a9e34…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 3 of 54 provisions accounted for
- resolution (kept apart from coverage): 1 resolved, 2 pending a person, 0 invalid, 51 unaccounted; evidence_verified checks quotations, not meaning
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
- ADD-03:p4-image/table-intro
- ADD-03:p4-image/table-header
- ADD-03:p4-image/row-a
- ADD-03:p4-image/row-b
- ADD-03:p4-image/notes-head
- ADD-03:p4-image/note1
- ADD-03:p4-image/note2
- ADD-03:p4-image/note3
- ADD-03:p4-image/signatory
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
| ADD-03/p4-image/stamp | disposition | ADD-03:p4-image/stamp |  | insufficient_evidence | missing_information: the proposer declares missing: The stamp prints no text, so no words can be quoted from it; whether the absence of a stamp impression matters for the letter's validity is not established by the evid… |
| ADD-03/AppB/para1 | escalation | ADD-03:AppB/para1 | ADD-03:T5-1 | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(2) vs ADD-03:p4-image/note2 (height datum); ADD-03:T5-1/note(1) vs ADD-03:p4-image/note1 (scope of the limits); ADD-03:T5-1 header 'finished ground level' vs A… |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S1: The stamp reading block of the Appendix A image has empty source text; the band crop b13-right shows only an empty oval outline with no legible text, beside the signatory line. — evidence verified
- **fact** S3: ADD-03:AppA/para2 reads 'End of reproduction.' and closes the reproduction of Table 5-1 at Appendix A. — evidence verified
- **fact** S4: ADD-03:AppB/para1 states that the English translation is for convenience only and that the Arabic text of Table 5-1 at Appendix A governs; Clause 7.2 of the same Addendum says the same. — evidence verified
- **fact** S5: The English Appendix B note (2) measures height from finished ground level after grading and filling; the Arabic Appendix A note 2 measures it from natural ground level before grading and filling (منسوب الأرض الطبيعية قبل أعمال التسوية والردم). The English note (1) covers permanent structures inclu… — evidence verified
- **interpretation** S2: An empty stamp outline prints no words and therefore amends, obliges or excepts nothing in the pack; whether an unfilled stamp affects the authenticity of the Office letter is a separate question for a person. — needs a person
- **interpretation** S6: Under AppB/para1 the Arabic Table 5-1 (Appendix A) prevails where the English translation (ADD-03:T5-1 rows and notes) differs, so the height datum and the scope of the limits must be taken from the Arabic: natural ground level before grading and filling, and temporary structures and cranes include… — needs a person

## Impact of the evidence-verified changes (dry run)

- ADD-03 would be **PARTIAL** with these alone
- units changed: none
- rows citing them: none
- rows that would be STALE: none
- decisions voided: none
- C46 (obligations not reaching A1/A3/A5): 0
- clarification entries citing changed units: none
- A3: enters none; leaves none

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-20261005T025444Z-analysis-008-critic`, route **host**; 2 item(s) reviewed

- **ADD-03/p4-image/stamp** (insufficient_evidence): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: Evidence is only a crop hash and empty text; I could not view the image, so the 'empty oval' description rests on the proposer's account. The no_effect conclusion follows from there being no words, but the controller marked insufficient_evidence and whether an unfilled stamp affects the letter's authenticity is left for a person.
  - checked: ADD-03:p4-image/stamp (empty text, crop sha 92d27467...), controller validation: semantic check consistent with no_effect, S1 evidence: signatory reading 'مدير المكتب'
- **ADD-03/AppB/para1** (conflicting): critic agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The conflict is real on the quoted words: English note (2) says finished ground level after grading and filling, Arabic note 2 says natural ground level before grading and filling. Note 1 also differs: English says permanent structures including stacks, Arabic says permanent and temporary including cranes and construction equipment.
  - concern: The claims about the Arabic table header, the zone heights (25, 40) and the 30 m lighting threshold are not quoted in the evidence shown, so I could not check them.
  - concern: The target ADD-03:T5-1 is flagged as not among the units the provision cites. Its text before the addendum shows only the table title, and the English notes come from sub-units (T5-1/note(2), note(1)) not printed in the units block. The target unit may be too coarse.
  - concern: S4 cites clause 7.2 ('The Arabic text governs.') but that unit's text is not printed here, so I could not verify it.
  - concern: S6 is an interpretation that a person must confirm. The escalation is reasonable because no amendment op can record precedence between two units both first issued by ADD-03.
  - checked: ADD-03:AppB/para1 text, ADD-03:T5-1/note(2) vs ADD-03:p4-image/note2, ADD-03:T5-1/note(1) vs ADD-03:p4-image/note1, ADD-03:T5-1 unit, controller validation (conflicting)

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T033645Z-638e/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T033645Z-638e --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
