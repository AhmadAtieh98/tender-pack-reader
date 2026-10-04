# Review request: ADD-03, run ADD-03-host-20261004T155951Z-be2f

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-04T15:59:51Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 57d76e1ca885ba7c…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 8 of 70 provisions accounted for
- resolution (kept apart from coverage): 0 resolved, 8 pending a person, 0 invalid, 62 unaccounted; evidence_verified checks quotations, not meaning
- approval: none (approval is a named person's decision; it is never assigned by the controller)

## Provisions not accounted for (a person treats each)

- ADD-03:cover/para1
- ADD-03:cover/para2
- ADD-03:cover/para3
- ADD-03:1.1
- ADD-03:1.2
- ADD-03:2.1
- ADD-03:2.2
- ADD-03:3.1
- ADD-03:4.1
- ADD-03:5.1
- ADD-03:5.2
- ADD-03:6.1
- ADD-03:T1-1/A
- ADD-03:T1-1/B
- ADD-03:T1-1/C
- ADD-03:T1-1/D
- ADD-03:T1-1/E
- ADD-03:T1-1/F
- ADD-03:T1-1/G
- ADD-03:T1-1/total
- ADD-03:S6/para1
- ADD-03:6.2
- ADD-03:7.1
- ADD-03:7.2
- ADD-03:8.1
- ADD-03:8.2
- ADD-03:8.3
- ADD-03:8.4
- ADD-03:Q15
- ADD-03:Q16
- ADD-03:Q17
- ADD-03:Q18
- ADD-03:Q19
- ADD-03:Q20
- ADD-03:AppA/para1
- ADD-03:p4-image/decl1
- ADD-03:p4-image/decl2
- ADD-03:p4-image/decl3
- ADD-03:p4-image/table-header
- ADD-03:p4-image/table-row4
- ADD-03:p4-image/table-row4-blank
- ADD-03:p4-image/field-member-en
- ADD-03:p4-image/field-member-ar
- ADD-03:p4-image/field-cr-en
- ADD-03:p4-image/field-cr-ar
- ADD-03:p4-image/field-signatory-en
- ADD-03:p4-image/field-signatory-ar
- ADD-03:p4-image/field-capacity-en
- ADD-03:p4-image/field-capacity-ar
- ADD-03:p4-image/field-date-en
- ADD-03:p4-image/field-date-ar
- ADD-03:p4-image/field-signature-en
- ADD-03:p4-image/field-signature-ar
- ADD-03:p4-image/note
- ADD-03:p4-image/image-footer
- ADD-03:AppB/para1
- ADD-03:F4-H/para1
- ADD-03:F4-H/T1/1
- ADD-03:F4-H/T1/2
- ADD-03:F4-H/T1/3
- ADD-03:F4-H/T1/4
- ADD-03:F4-H/para2

## Items

| id | type | provision | target | status | why (first failed check) |
|---|---|---|---|---|---|
| ADD-03/p4-image/hdr-en | disposition | ADD-03:p4-image/hdr-en |  | interpretation_pending | depends on assumption S-A1: a person must confirm it |
| ADD-03/p4-image/hdr-ar | disposition | ADD-03:p4-image/hdr-ar |  | interpretation_pending | depends on assumption S-A1: a person must confirm it |
| ADD-03/p4-image/ref-en | disposition | ADD-03:p4-image/ref-en |  | interpretation_pending | depends on assumption S-A1: a person must confirm it |
| ADD-03/p4-image/ref-ar | disposition | ADD-03:p4-image/ref-ar |  | interpretation_pending | depends on assumption S-A1: a person must confirm it |
| ADD-03/p4-image/form-en | disposition | ADD-03:p4-image/form-en |  | interpretation_pending | depends on assumption S-A1: a person must confirm it |
| ADD-03/p4-image/form-ar | disposition | ADD-03:p4-image/form-ar |  | interpretation_pending | depends on assumption S-A1: a person must confirm it |
| ADD-03/p4-image/title | disposition | ADD-03:p4-image/title |  | interpretation_pending | depends on assumption S-A1: a person must confirm it |
| ADD-03/p4-image/intro | disposition | ADD-03:p4-image/intro |  | interpretation_pending | depends on assumption S-A1: a person must confirm it |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S-F1: ADD-03 Clause 8.1 adds a new Form 4-H to Volume IV and states that it is reproduced at Appendix A. — evidence verified
- **fact** S-F2: Appendix A states the form on the following page is reproduced as issued; Appendix B states the Arabic text governs. — evidence verified
- **fact** S-F3: The page-4 image (region ADD-03-p4-r1) shows a bilingual letterhead box (authority name and tender reference in English left, Arabic right), the label FORM 4-H / النموذج ٤-ح, the Arabic title and the Arabic opening declaration, as read in the eight reading blocks; the readings are status pending. — evidence verified
- **assumption** S-A1: The pending readings of the eight blocks are taken as correct; I compared each band crop with its source_text and found them to agree, but the readings are not yet approved by a person. — needs a person
- **interpretation** S-I1: The eight blocks are identification and content of the reproduced Form 4-H (letterhead, tender reference, form label, title, opening words); none of them amends, deletes or replaces any clause, table or form by itself. The form's addition to the documents is effected by ADD-03:8.1 (answered in anot… — needs a person
- **interpretation** S-I2: The words 'نقر ونتعهد بما يلي' in the intro block are the signatory's declaration within the form text that a bidder completes; they are not an amendment of tender text and impose nothing beyond what the insertion of Form 4-H under ADD-03:8.1 brings in. A person must confirm. — needs a person

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261004T155951Z-be2f/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261004T155951Z-be2f --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
