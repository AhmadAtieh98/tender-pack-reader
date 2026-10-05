# Review request: ADD-03, run ADD-03-host-20261005T033353Z-0c84

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T03:33:53Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 77784d6d270a9e34…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 8 of 54 provisions accounted for
- resolution (kept apart from coverage): 0 resolved, 8 pending a person, 0 invalid, 46 unaccounted; evidence_verified checks quotations, not meaning
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
- ADD-03:p4-image/stamp
- ADD-03:AppA/para2
- ADD-03:AppB/para1
- ADD-03:T5-1/a
- ADD-03:T5-1/b
- ADD-03:T5-1/notes
- ADD-03:T5-1/note(1)
- ADD-03:T5-1/note(2)
- ADD-03:T5-1/note(3)

## Items

| id | type | provision | target | status | why (first failed check) |
|---|---|---|---|---|---|
| ADD-03/p4-image/notes-head | disposition | ADD-03:p4-image/notes-head |  | interpretation_pending | depends on interpretation S6: a person must confirm it |
| ADD-03/p4-image/signatory | disposition | ADD-03:p4-image/signatory |  | interpretation_pending | depends on interpretation S6: a person must confirm it |
| ADD-03/p4-image/row-a | disposition | ADD-03:p4-image/row-a |  | insufficient_evidence | missing_information: the proposer declares missing: approved reading of region ADD-03-p4-r1 (row A column split between ٢٥ and مطلوبة) |
| ADD-03/p4-image/row-b | disposition | ADD-03:p4-image/row-b |  | insufficient_evidence | missing_information: the proposer declares missing: approved reading of region ADD-03-p4-r1 (row B column split between باقي مساحة الموقع and ٤٠) |
| ADD-03/p4-image/note3 | disposition | ADD-03:p4-image/note3 |  | insufficient_evidence | missing_information: the proposer declares missing: approved reading of region ADD-03-p4-r1 |
| ADD-03/p4-image/table-header | disposition | ADD-03:p4-image/table-header |  | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1 |
| ADD-03/p4-image/note1 | disposition | ADD-03:p4-image/note1 |  | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(1) |
| ADD-03/p4-image/note2 | disposition | ADD-03:p4-image/note2 |  | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/note(2) |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S1: ADD-03 Clause 7.2 states that Table 5-1 is issued in Arabic and that the Arabic text governs; Appendix B is a convenience translation. — evidence verified
- **fact** S2: ADD-03 Clause 7.1 inserts a new VOL-II Clause 5.6 that incorporates Table 5-1 (Appendix A) by reference. The Appendix A image content is the table being incorporated. It does not itself amend any unit standing at ADD-02. — evidence verified
- **fact** S3: The Arabic column heading states heights in metres above natural ground level (منسوب الأرض الطبيعية). The Appendix B English heading states 'm above finished ground level'. — evidence verified
- **fact** S4: Arabic Note 2 measures height from natural ground level before grading and filling. Appendix B Note (2) measures it from finished ground level after grading and filling. — evidence verified
- **fact** S5: Arabic Note 1 applies the limits to permanent and temporary structures, including stacks, cranes and construction equipment. Appendix B Note (1) mentions only permanent structures, including stacks. — evidence verified
- **interpretation** S6: Rows A and B, the notes heading, Note 3 and the signatory line are the content of the newly issued Table 5-1 and the issuing letter. They change no unit standing at ADD-02. Their effect enters the pack through Clause 7.1 (another batch). For these provisions the Arabic and Appendix B agree in subst… — needs a person
- **interpretation** S7: The image reading of region ADD-03-p4-r1 is pending, and its column separators are incomplete. The header source_text runs الوصف and الحدّ الأقصى together. Row A runs ٢٥ and مطلوبة together. Row B runs باقي مساحة الموقع and ٤٠ together. The image shows four ruled columns (Zone, Description, Maximum… — needs a person

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-20261005T025444Z-analysis-007-critic`, route **host**; 8 item(s) reviewed

- **ADD-03/p4-image/table-header** (conflicting): critic agrees — selected because conflicting; model claude-sonnet-5-5
  - concern: The Arabic heading says natural ground level. The Appendix B quote (finished ground level) appears only in the statement S3 and the T5-1/a unit is not printed here.
  - concern: The reading's column separators are incomplete (الوصف and الحدّ الأقصى are run together), so a person must correct the structure.
  - checked: ADD-03:p4-image/table-header, S1, S2, S3, S7
- **ADD-03/p4-image/row-a** (insufficient_evidence): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: Row A's words add no amendment to any ADD-02 unit, so no_effect on ADD-02 units is consistent. The row is still a substantive height limit that takes effect through 7.1, so the register must link it there.
  - concern: The claim that Arabic and Appendix B agree (1,500 m, lighting) is interpretation S6. Only the '25' is quoted from Appendix B, so the rest is unverified.
  - concern: The reading is unapproved and ٢٥ and مطلوبة are run together.
  - checked: ADD-03:p4-image/row-a, ADD-03:7.1, S2, S6, S7
- **ADD-03/p4-image/row-b** (insufficient_evidence): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The same limits apply as for row A. The reading is unapproved and باقي مساحة الموقع and ٤٠ are run together.
  - concern: The claim that Arabic and Appendix B agree (40 m, lighting above 30 m) has no Appendix B quotation printed.
  - concern: This row carries the operative 40 m limit and the lighting requirement. A no_effect label must not hide that it takes effect via 7.1.
  - checked: ADD-03:p4-image/row-b, ADD-03:7.1, S2, S6, S7
- **ADD-03/p4-image/notes-head** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - checked: ADD-03:p4-image/notes-head
- **ADD-03/p4-image/note1** (conflicting): critic agrees — selected because conflicting; model claude-sonnet-5-5
  - concern: The Arabic reading is verbatim and the unresolved status is justified. The Appendix B text is quoted only in S5.
  - concern: The reading is unapproved.
  - checked: ADD-03:p4-image/note1, S1, S2, S5
- **ADD-03/p4-image/note2** (conflicting): critic agrees — selected because conflicting; model claude-sonnet-5-5
  - concern: The Arabic reading is verbatim and the datum opposition with Appendix B is quoted in S4.
  - concern: The Arabic table-header datum and Note 2 are consistent with each other, so the conflict is with Appendix B only. The reading is unapproved.
  - checked: ADD-03:p4-image/note2, ADD-03:p4-image/table-header, S1, S3, S4
- **ADD-03/p4-image/note3** (insufficient_evidence): critic DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The words contain an obligation ('يجب' = must; 30 days' notice before any crane). Labelling it no_effect risks losing it.
  - concern: The reason says it binds through 7.1's 'shall comply with the height limits in Table 5-1'. A crane-notice duty is not clearly a 'height limit', so this does not clearly follow from 7.1's words. It depends on the incorporation by reference of the whole table including notes.
  - concern: The claim that Appendix B Note (3) agrees is not supported by any quotation shown.
  - concern: The reading is unapproved.
  - checked: ADD-03:p4-image/note3, ADD-03:7.1, S2, S6
- **ADD-03/p4-image/signatory** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - checked: ADD-03:p4-image/signatory

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T033353Z-0c84/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T033353Z-0c84 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
