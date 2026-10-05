# Review request: ADD-03, run ADD-03-host-20261005T132405Z-d37a

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T13:24:05Z; controller s10-ai-1
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
| ADD-03/p4-image/hdr-en | disposition | ADD-03:p4-image/hdr-en |  | interpretation_pending | depends on interpretation S3: a person must confirm it |
| ADD-03/p4-image/hdr-ar | disposition | ADD-03:p4-image/hdr-ar |  | interpretation_pending | depends on interpretation S3: a person must confirm it |
| ADD-03/p4-image/date | disposition | ADD-03:p4-image/date |  | interpretation_pending | depends on interpretation S3: a person must confirm it |
| ADD-03/p4-image/ref | disposition | ADD-03:p4-image/ref |  | interpretation_pending | depends on interpretation S3: a person must confirm it |
| ADD-03/p4-image/subject | disposition | ADD-03:p4-image/subject |  | interpretation_pending | depends on interpretation S3: a person must confirm it |
| ADD-03/p4-image/tender-ref | disposition | ADD-03:p4-image/tender-ref |  | interpretation_pending | depends on interpretation S3: a person must confirm it |
| ADD-03/p4-image/table-title | disposition | ADD-03:p4-image/table-title |  | interpretation_pending | depends on interpretation S3: a person must confirm it |
| ADD-03/p4-image/table-qualifier | disposition | ADD-03:p4-image/table-qualifier |  | interpretation_pending | depends on interpretation S3: a person must confirm it |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S1: ADD-03 Clause 7.1 inserts Volume II Clause 5.6, which obliges compliance with the height limits in Table 5-1 reproduced at Appendix A and incorporates it by reference. — evidence verified
- **fact** S2: Appendix A states that Table 5-1 is reproduced as issued by the Office and that the Arabic text governs. — evidence verified
- **assumption** S4: The pending image readings' source texts for these blocks are taken as correct. Their readings are status 'pending' (not approved). The host compared each one by eye with its band crop and found it consistent. — needs a person
- **interpretation** S3: The eight answered blocks (English and Arabic letterhead, date, reference number, subject, tender reference, table title, table lead-in) identify or introduce the reproduced letter and table. None of them prints an amendment (no old/new pair, deletion, substitution or insertion) or an obligation of… — needs a person

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-s12-20261005T130341Z-analysis-006-critic`, route **host**; 8 item(s) reviewed

- **ADD-03/p4-image/hdr-en** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: S3 and S4 are an interpretation and an assumption, and a person must confirm them. The reading is still pending.
  - concern: The reason says the letterhead 'identifies the office that issued the reproduced Table 5-1'. The unit text itself is only the office name. The link to Table 5-1 comes from ADD-03:7.1 and Appendix A, not from this block.
  - checked: ADD-03:p4-image/hdr-en, ADD-03:7.1 quotation, ADD-03:AppA/para1 quotation
- **ADD-03/p4-image/hdr-ar** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The text is only an office name, so no_effect follows. S3 and S4 still need a person to confirm them.
  - concern: The Arabic letterhead matches the English one in meaning. Appendix A says the Arabic text governs, but there is no conflict here.
  - checked: ADD-03:p4-image/hdr-ar, ADD-03:7.1 quotation
- **ADD-03/p4-image/date** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The date '١٠ نوفمبر ٢٠٢٦م' (10 November 2026) is after the session date of 2026-10-05. The evidence does not show ADD-03's own issue date, so the item cannot show that this date is consistent with it. A person should check it. It does not change the no_effect disposition, because a dateline states no change or deadline.
  - concern: S3 and S4 need a person to confirm them.
  - checked: ADD-03:p4-image/date
- **ADD-03/p4-image/ref** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The text is only a reference number, so no_effect follows. S3 and S4 still need confirmation.
  - checked: ADD-03:p4-image/ref
- **ADD-03/p4-image/subject** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The subject line only describes the letter's topic. S3 and S4 need confirmation.
  - checked: ADD-03:p4-image/subject
- **ADD-03/p4-image/tender-ref** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The item says the number matches the pack id, but that match is not shown in the evidence printed here. It does not affect the disposition.
  - concern: S3 and S4 need confirmation.
  - checked: ADD-03:p4-image/tender-ref
- **ADD-03/p4-image/table-title** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The title only names the table. The compliance obligation comes from ADD-03:7.1, which the quotation supports.
  - concern: S3 and S4 need confirmation.
  - checked: ADD-03:p4-image/table-title, ADD-03:7.1 quotation
- **ADD-03/p4-image/table-qualifier** (interpretation_pending): critic agrees — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The sentence says the maximum permitted height is set 'in each zone of the site as follows'. That is introductory wording rather than a limit, but it is close to operative. The limits themselves sit in the rows and notes, which are not shown here, so the no_effect disposition is safe only if those rows are handled elsewhere.
  - concern: The item already says a person should confirm. S3 and S4 also need confirmation.
  - checked: ADD-03:p4-image/table-qualifier, ADD-03:7.1 quotation

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T132405Z-d37a/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T132405Z-d37a --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
