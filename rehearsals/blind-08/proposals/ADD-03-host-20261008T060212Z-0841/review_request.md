# Review request: ADD-03, run ADD-03-host-20261008T060212Z-0841

Nothing here is accepted, applied or published. Statuses are the controller's; a person decides each item.

- route **host** (provider host); model requested `claude-code headless (claude-opus-5-5)`; reported `None`
- status **partial**; created 2026-10-08T06:02:12Z; controller s10-ai-1
- state: pack NUPA-ISTP-2026-014+ADD-03-CANDIDATE; evidence build e5d1ff4e390aab4b…; validated ADD-02; working ADD-03; decisions none
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed (host route: no application API call (the host's own usage is not visible to this tool))
- coverage: 2 of 52 provisions accounted for
- resolution (kept apart from coverage): 1 resolved, 1 pending a person, 0 invalid, 50 unaccounted; evidence_verified checks quotations, not meaning
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
- ADD-03:2.3
- ADD-03:2.4
- ADD-03:2.5
- ADD-03:2.6
- ADD-03:3.1
- ADD-03:3.2
- ADD-03:3.3
- ADD-03:3.4
- ADD-03:4.1
- ADD-03:4.2
- ADD-03:Q15
- ADD-03:Q16
- ADD-03:Q17
- ADD-03:Q18
- ADD-03:Q19
- ADD-03:p3-image/r1
- ADD-03:p3-image/r2
- ADD-03:p3-image/r3
- ADD-03:p3-image/hdr-en
- ADD-03:p3-image/hdr-ar
- ADD-03:p3-image/date
- ADD-03:p3-image/ref
- ADD-03:p3-image/to
- ADD-03:p3-image/subject
- ADD-03:p3-image/tender
- ADD-03:p3-image/notes-heading
- ADD-03:p3-image/note1
- ADD-03:p3-image/note2
- ADD-03:p3-image/note3
- ADD-03:p3-image/stamp
- ADD-03:p3-image/signatory
- ADD-03:p3-image/image-footer
- ADD-03:AppB/para1
- ADD-03:AppB/para2
- ADD-03:T8-1/1
- ADD-03:T8-1/2
- ADD-03:T8-1/3
- ADD-03:T8-1/notes
- ADD-03:T8-1/note(1)
- ADD-03:T8-1/note(2)
- ADD-03:T8-1/note(3)
- ADD-03:AppB/para3

## Items

| id | type | provision | target | status | why (first failed check) |
|---|---|---|---|---|---|
| ADD-03/AppA/para2 | disposition | ADD-03:AppA/para2 |  | evidence_verified |  |
| ADD-03/AppA/para1 | disposition | ADD-03:AppA/para1 |  | interpretation_pending | depends on interpretation S-AppA-I1: a person must confirm it |

## Statements (kept apart: facts, assumptions, interpretations)

- **fact** S-AppA-1: ADD-03 Appendix A paragraph 1 states that the letter and table are reproduced as issued by the Office and that the Arabic text governs in accordance with Section 2.2 of the Addendum. — evidence verified
- **fact** S-2.2: ADD-03 Section 2.2 itself makes the precedence of the Arabic text of Table 8-1. — evidence verified
- **fact** S-AppA-2: ADD-03 Appendix A paragraph 2 reads only 'End of reproduction.' — evidence verified
- **interpretation** S-AppA-I1: Appendix A paragraph 1 restates, by reference, the precedence made operative by Section 2.2 and adds no change of its own; the precedence and the incorporation of Table 8-1 into Volume I are dealt with under ADD-03:2.2 and the Table 8-1 provisions in other batches. — needs a person

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

- critic run `ADD-03-run-host-20261008T053735Z-77b2-analysis-004-critic`, route **host**; 1 item(s) reviewed

- **ADD-03/AppA/para1** (interpretation_pending): critic DOES NOT agree — selected because consequential_interpretation; model claude-opus-5-5
  - concern: ambiguous: the paragraph may not simply restate Section 2.2; it may reach further. The only quotation of ADD-03:2.2 shown (S-2.2) limits the Arabic-precedence rule to Table 8-1: "Table 8-1 is issued in the Arabic language. The Arabic text governs." AppA/para1 introduces both items, "The following letter and table are reproduced as issued...", and then says "The Arabic text governs in accordance with Section 2.2 of this Addendum." Reading 1: precedence covers Table 8-1 only, as in 2.2, and the paragraph adds nothing. Reading 2: the paragraph also makes the Arabic text of the Office's letter (ref. No. 228/2026 dated 16 November 2026) govern, which 2.2 as quoted does not do. The item picks Reading 1 without naming Reading 2. This should be raised as an issue for a person (Legal) to decide, not recorded as a no_effect disposition.
  - concern: "The Arabic text governs" is precedence wording, so it says which text prevails. Shared policy makes which text governs or prevails a person's decision, and a no_effect is a person's call where the words print or except something. So the controller's semantic check, which found "no amendment, obligation or exception words", should not be taken as showing that nothing changes here.
  - concern: The paragraph does not say whether the reproduced letter is incorporated into the tender documents or is information only. The item does not identify this as an open point. It only says that Table 8-1's incorporation is dealt with elsewhere. The letter's own status is not dealt with in this item.
  - concern: Only fragments of the full text of ADD-03:2.2 are shown in this request: "The Arabic text governs." and "Table 8-1 is issued in the Arabic language. The Arabic text governs." So I could not check whether 2.2 covers the letter as well. The controller records the 2.2 quotation as "verbatim in ADD-03:2.2 at ADD-02", but AppA/para1 is marked not_issued at ADD-02, which suggests ADD-03 units did not exist at that stage. That evidence check needs confirming.
  - concern: Change propagation: the item names no follow-on work. If the letter's Arabic text governs, then any requirement, date or reference taken from the letter, and any translation of it used in A1 or A5, depends on this paragraph. These are not listed.
  - concern: Interpretation S-AppA-I1 has no evidence of its own. It is the basis for the whole disposition, and it is correctly left pending for a person.
  - checked: ADD-03:AppA/para1: "The following letter and table are reproduced as issued by the Northern Region Investment Services Office under its reference No. 228/2026 dated 16 November 2026. The Arabic text governs in accordance with Section 2.2 of this Addendum.", ADD-03:2.2 (quoted in the item): "The Arabic text governs.", ADD-03:2.2 (quoted in S-2.2): "Table 8-1 is issued in the Arabic language. The Ar

## Next

- read every item above against its evidence (`staging/ai/ADD-03-host-20261008T060212Z-0841/proposals.yaml`)
- promote what you want as PROPOSED drafts: `python -m tenderpack ai promote ADD-03-host-20261008T060212Z-0841 --by "Your Name"`
- then curate, `outputs`, `check-register`, and decide with `accept` / `reject` as usual
