# Review request: ADD-03, run ADD-03-host-20261005T031229Z-fd07

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (opus)`; reported `None`
- status **partial**; created 2026-10-05T03:12:29Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build 77784d6d270a9e34…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 2 of 54 provisions accounted for
- resolution (kept apart from coverage): 0 resolved, 2 pending a person, 0 invalid, 52 unaccounted; evidence_verified checks quotations, not meaning
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
| ADD-03/5.2 | amendment_op | ADD-03:5.2 | VOL-II:3.4 | insufficient_evidence | missing_information: the proposer declares missing: Demonstrating compliance needs the ESIA Figure 7-2 concentration, which is not in the evidence build. |
| ADD-03/5.1 | amendment_op | ADD-03:5.1 | VOL-II:3.4 | conflicting | declared_conflicts: the proposer declares: ADD-03:cover/para3 names Volume II Clause 3.5 for the odour criterion; the operative provision 5.1 names Clause 3.4 and quotes words found only in 3.4 (3.5 is the noise clause). |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** F1: ADD-03:5.1 deletes 'not more than 5 OU/m³ at the site boundary' in Volume II Clause 3.4 and substitutes a criterion by reference to Figure 7-2 of the ESIA, and states the 98th percentile hourly basis is unchanged. — evidence verified
- **fact** F2: VOL-II:3.4 at ADD-02 is active and contains the deleted words exactly once, written with the superscript 'm³'. — evidence verified
- **fact** F3: The odour concentration figure itself is not printed in the pack: ADD-03 Q18 says it is shown in Figure 7-2 of the ESIA in the data room; searching the evidence found no Figure 7-2 unit. — evidence verified
- **fact** F4: The ADD-03 cover summary says the odour criterion is replaced in Volume II Clause 3.5, whereas the operative provision 5.1 names Clause 3.4; VOL-II:3.5 is the noise clause. — evidence verified
- **fact** F5: ADD-03:5.2 obliges Bidders to demonstrate compliance with Clause 3.4 as amended in the Technical Proposal. — evidence verified
- **interpretation** I1: ADD-03:5.2 adds a new Technical Proposal submission obligation attached to VOL-II:3.4 (not merely confirming an existing one), so it is represented as an annotate op with effect adds_obligation and no change to the text of 3.4. — needs a person

## Independent critic (a second model; agreement is not approval, and no status was changed)

- critic run `ADD-03-run-host-blind05-20261005T025444Z-analysis-003-critic`, route **host**; 2 item(s) reviewed

- **ADD-03/5.1** (conflicting): critic agrees — selected because conflicting; model claude-sonnet-5-5
  - concern: Real conflict: ADD-03 cover/para3 names Clause 3.5 (the noise clause), but operative 5.1 names Clause 3.4 and quotes words found only in 3.4. The operative text and the quoted words support targeting 3.4, but a person should confirm which clause the cover summary intends.
  - concern: The new limit's numeric value (ESIA Figure 7-2) is not in the evidence, so the replacement cannot be expressed as a number. This is a declared gap.
  - concern: The replacement changes the location from site boundary to nearest sensitive receptor. The trailing words ', assessed as a 98th percentile hourly value' remain, which matches the statement that the basis is unchanged.
  - concern: The old string appears exactly once in 3.4 and matches verbatim, including the m³ superscript.
  - checked: ADD-03:5.1, VOL-II:3.4, VOL-II:3.5, ADD-03:cover/para3, ADD-03:Q18
- **ADD-03/5.2** (insufficient_evidence): critic DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
  - concern: The obligation to demonstrate compliance in the Technical Proposal is clearly stated in ADD-03:5.2, so the adds_obligation annotation is plausible. But the interpretation I1 that it is a new obligation, not confirming an existing one, has no evidence attached. The evidence shown does not include any existing Technical Proposal requirement, so this cannot be checked.
  - concern: Compliance demonstration depends on the ESIA Figure 7-2 value, which is not in the evidence, and on 5.1 and its unresolved cover-page conflict (Clause 3.4 vs 3.5). It therefore stays pending a person's confirmation.
  - concern: Controller status is insufficient_evidence, which is consistent with this.
  - checked: ADD-03:5.2, VOL-II:3.4, ADD-03:Q18, ADD-03:5.1

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261005T031229Z-fd07/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261005T031229Z-fd07 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
