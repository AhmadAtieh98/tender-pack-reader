# Review request: ADD-03, run ADD-03-host-20261004T164722Z-4d3d

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-04T16:47:22Z; controller s10-ai-1
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
- ADD-03:p4-image/hdr-en
- ADD-03:p4-image/hdr-ar
- ADD-03:p4-image/ref-en
- ADD-03:p4-image/ref-ar
- ADD-03:p4-image/form-en
- ADD-03:p4-image/form-ar
- ADD-03:p4-image/title
- ADD-03:p4-image/intro
- ADD-03:p4-image/decl1
- ADD-03:p4-image/decl2
- ADD-03:p4-image/decl3
- ADD-03:p4-image/table-header
- ADD-03:p4-image/table-row4
- ADD-03:p4-image/table-row4-blank
- ADD-03:p4-image/field-member-en
- ADD-03:p4-image/field-member-ar
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
| ADD-03/p4-image/field-cr-en | disposition | ADD-03:p4-image/field-cr-en |  | interpretation_pending | depends on interpretation S4: a person must confirm it |
| ADD-03/p4-image/field-cr-ar | disposition | ADD-03:p4-image/field-cr-ar |  | interpretation_pending | depends on interpretation S4: a person must confirm it |
| ADD-03/p4-image/field-signatory-en | disposition | ADD-03:p4-image/field-signatory-en |  | interpretation_pending | depends on interpretation S4: a person must confirm it |
| ADD-03/p4-image/field-signatory-ar | disposition | ADD-03:p4-image/field-signatory-ar |  | interpretation_pending | depends on interpretation S4: a person must confirm it |
| ADD-03/p4-image/field-capacity-en | disposition | ADD-03:p4-image/field-capacity-en |  | interpretation_pending | depends on interpretation S4: a person must confirm it |
| ADD-03/p4-image/field-capacity-ar | disposition | ADD-03:p4-image/field-capacity-ar |  | interpretation_pending | depends on interpretation S4: a person must confirm it |
| ADD-03/p4-image/field-date-en | disposition | ADD-03:p4-image/field-date-en |  | interpretation_pending | depends on interpretation S4: a person must confirm it |
| ADD-03/p4-image/field-date-ar | disposition | ADD-03:p4-image/field-date-ar |  | interpretation_pending | depends on interpretation S4: a person must confirm it |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S1: Appendix A of ADD-03 reproduces Form 4-H as an image on page 4, and the text layer says so: 'Form 4-H is reproduced on the following page as issued.' — evidence verified
- **fact** S2: The eight units are bilingual field labels of the blank completion block below the beneficial-owner table on the page-4 image (English at left, Arabic at right, each followed by a blank rule line). The image readings are status 'pending'. — evidence verified
- **fact** S3: None of the eight labels contains change words (no old/new pair, 'deleted', 'substituted', 'amended', 'reissued') and none contains obligation or exception words ('shall', 'must', 'unless'). The obligation about the form ('shall be submitted in the Arabic language') is printed in a separate note un… — evidence verified
- **interpretation** S4: A blank field label of a form is content of the form that the addendum issues; it does not by itself amend, delete or add to any provision. Its effect (issuing Form 4-H) is carried by the Section 8 provisions and the form as a whole, which belong to other batches. So each of these labels is no_effe… — needs a person

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261004T164722Z-4d3d/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261004T164722Z-4d3d --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
