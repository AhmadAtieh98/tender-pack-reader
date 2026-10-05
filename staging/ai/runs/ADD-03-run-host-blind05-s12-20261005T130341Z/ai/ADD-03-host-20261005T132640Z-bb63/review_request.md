# Review request: ADD-03, run ADD-03-host-20261005T132640Z-bb63

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T13:26:40Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build e017ad321f216c3e…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 8 of 63 provisions accounted for
- resolution (kept apart from coverage): 0 resolved, 8 pending a person, 0 invalid, 55 unaccounted; evidence_verified checks quotations, not meaning
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
- ADD-03:p4-image/table-qualifier
- ADD-03:p4-image/rowB-zone
- ADD-03:p4-image/rowB-description
- ADD-03:p4-image/rowB-height
- ADD-03:p4-image/rowB-lighting
- ADD-03:p4-image/notes-heading
- ADD-03:p4-image/note1
- ADD-03:p4-image/note2
- ADD-03:p4-image/note3
- ADD-03:p4-image/signatory
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
| ADD-03/p4-image/col-zone | disposition | ADD-03:p4-image/col-zone |  | interpretation_pending | depends on interpretation S6: a person must confirm it |
| ADD-03/p4-image/col-description | disposition | ADD-03:p4-image/col-description |  | interpretation_pending | depends on interpretation S6: a person must confirm it |
| ADD-03/p4-image/col-lighting | disposition | ADD-03:p4-image/col-lighting |  | interpretation_pending | depends on interpretation S6: a person must confirm it |
| ADD-03/p4-image/rowA-zone | disposition | ADD-03:p4-image/rowA-zone |  | interpretation_pending | depends on interpretation S6: a person must confirm it |
| ADD-03/p4-image/rowA-description | disposition | ADD-03:p4-image/rowA-description |  | interpretation_pending | depends on interpretation S6: a person must confirm it |
| ADD-03/p4-image/rowA-lighting | disposition | ADD-03:p4-image/rowA-lighting |  | interpretation_pending | depends on interpretation S6: a person must confirm it |
| ADD-03/p4-image/col-height | escalation | ADD-03:p4-image/col-height | ADD-03:T5-1 | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1 |
| ADD-03/p4-image/rowA-height | disposition | ADD-03:p4-image/rowA-height |  | conflicting | declared_conflicts: the proposer declares: ADD-03:T5-1/a |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S1: Clause 7.1 inserts Volume II Clause 5.6, which incorporates Table 5-1 as reproduced at Appendix A by reference; the Appendix A table cells do not themselves name or amend any unit existing at ADD-02. — evidence verified
- **fact** S2: Clause 7.2 states the Arabic text of Table 5-1 governs and the English translation at Appendix B is for convenience only. — evidence verified
- **fact** S3: The Arabic height column heading as read from the image is 'الحدّ الأقصى للارتفاع (متر فوق منسوب الأرض الطبيعية)'. — evidence verified
- **fact** S4: The English translation at Appendix B heads the height column 'Maximum height (m above finished ground level)'. — evidence verified
- **interpretation** S5: 'منسوب الأرض الطبيعية' means natural (existing, pre-grading) ground level, not finished ground level; the governing Arabic datum therefore differs from the English translation's 'finished ground level'. The translation is proposed, not evidence; a person must confirm it. — needs a person
- **interpretation** S6: The Arabic Zone A row cells (أ; the 1,500 m eastern-boundary description; ٢٥; مطلوبة) and the Zone, Description and warning-lighting column headings agree in substance with the English translation row ADD-03:T5-1/a and its headings. — needs a person

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-s12-20261005T130341Z-analysis-007-critic`, route **host**; 8 item(s) reviewed

- **ADD-03/p4-image/col-zone** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: Relies on S6, an interpretation a person must confirm. The Arabic reading itself is only a pending reading; the crop cannot be checked here.
  - checked: ADD-03:p4-image/col-zone, ADD-03:7.1, ADD-03:T5-1
- **ADD-03/p4-image/col-description** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: Relies on S6, which needs human confirmation. The reading is pending.
  - checked: ADD-03:p4-image/col-description, ADD-03:7.1, ADD-03:T5-1
- **ADD-03/p4-image/col-lighting** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The Arabic 'الإنارة التحذيرية' (warning lighting) is rendered 'Obstacle lighting' in English. S6 treats this as agreement in substance, and that is the person's call.
  - concern: The crop hash is the same as for col-height, which is consistent with both being in the left half of the header.
  - checked: ADD-03:p4-image/col-lighting, ADD-03:7.1, ADD-03:T5-1
- **ADD-03/p4-image/col-height** (conflicting): critic agrees — selected because conflicting, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
  - concern: The conflict follows from the words. The Arabic says 'الأرض الطبيعية' (natural ground level), the English says 'finished ground level', and Clause 7.2 says the Arabic governs.
  - concern: The target ADD-03:T5-1 is the English translation, not a unit existing at ADD-02. An escalation is therefore the right form, and it needs a person's decision.
  - concern: The meaning of 'الطبيعية' as natural is an interpretation (S5). The reading is also still pending and must be approved.
  - concern: The rationale cites note 2 as support, but that note is not in the evidence shown, so it cannot be verified here.
  - checked: ADD-03:p4-image/col-height, ADD-03:T5-1, ADD-03:7.2, ADD-03:7.1
- **ADD-03/p4-image/rowA-zone** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: Relies on S6, which needs human confirmation. The reading is pending.
  - checked: ADD-03:p4-image/rowA-zone, ADD-03:7.1, ADD-03:T5-1/a
- **ADD-03/p4-image/rowA-description** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: Relies on S6. The reading of the Eastern Arabic numerals is pending approval, and the 1,500 m figure matches the English row.
  - checked: ADD-03:p4-image/rowA-description, ADD-03:7.1, ADD-03:T5-1/a
- **ADD-03/p4-image/rowA-height** (conflicting): critic agrees — selected because conflicting; model claude-sonnet-5-5
  - concern: 'unresolved' is appropriate. The figure 25 matches, but the datum is in conflict (natural versus finished ground level).
  - concern: The datum conflict depends on S5, an interpretation that is not yet confirmed.
  - concern: The declared conflict target ADD-03:T5-1/a is an English translation row, and the decision is escalated under col-height.
  - checked: ADD-03:p4-image/rowA-height, ADD-03:p4-image/col-height, ADD-03:T5-1/a, ADD-03:7.2
- **ADD-03/p4-image/rowA-lighting** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The cell states a real requirement ('required'). no_effect is acceptable only because the requirement takes effect through Clause 7.1's incorporation, which is accounted for separately. That separate item should actually exist.
  - concern: Clause 7.1 as quoted refers to 'height limits'. Whether it also brings in the lighting column is not shown in the evidence. A person should confirm that.
  - concern: Relies on S6, which needs human confirmation.
  - checked: ADD-03:p4-image/rowA-lighting, ADD-03:7.1, ADD-03:T5-1/a

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T132640Z-bb63/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T132640Z-bb63 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
