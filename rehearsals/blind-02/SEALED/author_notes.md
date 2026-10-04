# Blind rehearsal 02: author notes (SEALED)

Input: `rehearsals/blind-02/input/ADD-03_Addendum_No_3.pdf` (4 pages, "Issued 3 November 2026", a Tuesday).
Answer key: `expected_findings.yaml` in this directory. Builder: `build_addendum.py` (deterministic; run
`python build_addendum.py out.pdf` with the repository's virtualenv; two builds give identical bytes).

## What I read

Allowed sources only: the four volumes, ADD-01, ADD-02, the brief, the blind-01 Addendum No. 3 PDF (to
avoid overlap) and the blind-01 builder (as a technique example). I did not open the tool's code, tests,
curation, config, build output, docs, worklog or scripts.

## Style fidelity

- A4, Base-14 Type1 fonts (Helvetica, Helvetica-Bold, Times-Roman, Times-Bold, WinAnsi, not embedded),
  text layer only, no images.
- Furniture copied from the ADD-01/02 content streams: the diagonal grey "FICTIONAL — ASSESSMENT PACK"
  watermark, header "Addendum No. 3" / "NUPA/ISTP/2026/014" with rule, footer disclaimer and "Page N"
  with rule.
- Cover band (#2a2a2a) with "ADDENDUM NO. 3", right-aligned "Issued 3 November 2026" (bold) and
  "Tender NUPA/ISTP/2026/014"; project line; "This Addendum ..." summary; the standard precedence and
  acknowledgement paragraph.
- Numbered headings (Helvetica-Bold 13), provisions with bold numbers and a hanging indent, quoted
  inserted clauses in the ADD-02 9.1 layout (‘6.8 …’, ‘12.5 …’), the Q&A grid (No / Bidder question /
  Authority response) with the header repeated when it splits over a page, and the appendix on a new
  page in the ADD-01 Appendix style.
- Table 2-2 (revised) uses the column positions of the original VOL-II Table 2-2, the inset table
  geometry and caption of ADD-02 Table 1-1 (revised), the short centred rule, and 7.2 pt notes with the
  BOD5 subscript drawn as in Volume II.
- Metadata: anonymous/unspecified as in the originals. The producer field is left empty (the file is not
  claimed to be a ReportLab file). Creation date is fixed at the issue date so the build is reproducible.

## Design: how this differs from blind-01

Blind-01 moved the Proposal Due Date to a new day, changed 5.2, the 6.4 amount and the 6.5 hard copies,
changed footnote 12, 8.6 and 12.2, inserted 10.5 with renumbering, changed Table 2-4 TSS, Table 2-6 and
Form 4-C, and corrected the Form 4-A date. This addendum does none of those. It changes different
things in different ways:

| Kind | Provision |
|---|---|
| Submission time changes on the same date | 2.1 (6.1: 14:00 -> 11:00), with 2.2 cancelling the ADD-01 "time unchanged" sentence |
| Appendix replaced | 2.3 (VOL-I Appendix 3: new box, floor, building, marking time) |
| New obligation with stated consequence + derived date | 2.4 (new 6.8: register delivery persons by Thu 19 Nov 2026; otherwise refused entry and the Proposal is treated as late) |
| Figures/periods changed | 3.1 (7.1: 150 -> 180), 3.2 (6.3: 180 -> 210), 5.1 (VOL-II 3.5 night 45 -> 40), 5.3 (VOL-II 8.4 22% -> 25%) |
| Implicit consequential form change | 3.3 (Form 4-A para 2 "read accordingly") |
| Deletion of a requirement | 4.1 (10.3 model audit opinion removed from the Proposal) |
| Insertion (post-award) | 4.2 (new 12.5) |
| Form rows deleted | 4.3 (Form 4-F) |
| Reinstatement by revoking an earlier addendum | 5.2 (ADD-02 4.1 revoked; VOL-II 4.4 back to 72 h) |
| Sentence replaced (a tightening) | 5.3 second limb |
| Reissued table with a change the narrative does not mention | 6.1 + Appendix A (TP peak 14 -> 16 not listed among the "principal changes") |
| Notes that change things | Note (3) new deliverable with a scoring consequence; Note (4) amends VOL-II 2.3 |
| Re-lettering + cross-reference dependency | 7.1 (9.1 items (f)-(j)); Q16 cites "item (i) ... as re-lettered" |
| Index row inserted | 7.2 (Form 4-G in the VOL-IV Index) |
| Q&A withdrawing an earlier answer | Q15 withdraws ADD-01 Q3 (foreign-bank branch Bid Bonds no longer acceptable) |
| Q&A creating an obligation | Q16 (legalisation/apostille of Powers of Attorney); Q20 (second USB, password window) |
| Q&A decoys with no effect | Q17 (confirms ADD-02 Q10), Q18 (withdrawn), Q19 (intent only), Q21 (no extension) |

## Planted cover errors (two)

1. **E1, misleading:** "The Proposal Due Date is unchanged." VOL-I 2.6 defines the PDD as the date and
   time in 6.1, and the time moves three hours earlier. Q21 ("the date ... is not extended") backs up
   the misreading, so a reader that trusts the cover or Q21 keeps 14:00.
2. **E2, omission:** the Bid Bond validity extension (6.3, 180 -> 210 days) is not on the cover. It sits
   under a heading that says only "PROPOSAL VALIDITY", and the same "180 days" string is the new value
   in 3.1 and the old value in 3.2.

The cover also does not itemise several secondary effects: Note (4) on 2.3, Note (3)'s new report, the
TP change, 12.5 and the Form 4-F rows, and the Q&A effects. That is normal for a cover. They are listed
under `secondary_undisclosed_effects` so they can be scored separately from E1 and E2.

## Traps and intended reasoning

- **Time-dependent knock-ons.** The Q20 password window ends at 12:00. A tool that missed 2.1 would say
  15:00. The envelope marking changes to 11:00.
- **Working-day arithmetic.** 6.8: five Working Days before Thu 26 Nov, not counting the 26th and
  skipping Fri/Sat, gives Thu 19 Nov 2026. The clarification cut-off stays Thu 12 Nov 2026.
- **Validity dates.** These count PDD + N calendar days: 180 days gives 25 May 2027 and 210 days gives
  24 June 2027. A tool that counts the PDD as day 1 gets one day earlier; accept either if the convention
  is stated.
- **Revocation.** 5.2 returns VOL-II 4.4 to the original 72 h. A tool that diffs only against the volume
  sees "no change". A tool that applies addenda without handling revocation keeps 96 h. Both are wrong
  for A2 traceability.
- **Re-lettering.** Q16's "item (i) ... as re-lettered" means the Powers of Attorney. Without 7.1, (i)
  resolves to "certificates and evidence under Section 8".
- **Withdraw versus confirm.** Q15 withdraws an earlier answer. Q17 confirms one, using the same
  "response N in Addendum No. M" wording. Only Q15 changes anything.
- **Scored versus pass/fail.** Note (3)'s consequence is zero marks on criterion A (25 marks), not
  rejection. The technical score is then capped at 75 against a threshold of 70. A well-calibrated A3
  flags this as a serious risk without calling it a stated disqualification.
- **Q15 consequence.** "Will not be accepted" is stated. Rejection of the Proposal is not stated, though
  6.3 makes a Bid Bond mandatory. Medium confidence is the honest answer.
- **Q16 consequence.** "Treated as not submitted" is stated. Non-responsiveness follows only through 9.3
  (Form 4-A signatory POA), so this is also inferential.
- **Q19** must stay unresolved and go to a human. It is the brief's "no correct answer" item, and the
  Authority's statement of intent is not an amendment.
- **Form 4-A PDD entry.** The pre-filled entry in VOL-IV and ADD-01 Appendix A still says "12 November
  2026, 14:00 Riyadh time". 3.3 updates paragraph 2 of Form 4-A but not this entry. A careful reader
  flags it as stale. The correct value by precedence is 26 November 2026, 11:00.
- **Tightening, not deletion.** 5.3 replaces the 500 t/yr landfill threshold with consent for any landfill
  disposal. A tool that labels it "deleted requirement" has misread it.
- **Unmentioned table change.** TP peak 14 -> 16 can only be found by diffing the reissued table against
  VOL-II Table 2-2.

## Deliberate ambiguities (accept a flagged answer)

1. Whether date-based periods counted from the PDD (5.2 cut-off, 6.8 registration) carry the 11:00 time
   of day. The expected answer is the date only. A tool that carries 11:00 should say why.
2. "Within one (1) hour after the Proposal Due Date" is taken as the window 11:00 to 12:00. Uploading
   before 11:00 is arguably non-compliant.
3. The day-counting convention for the validity periods (see above).
4. Whether Note (3) belongs on A3 (see above).

## Internal-consistency checks done

- Every clause, table and form cited exists in the volumes or in ADD-01/02: VOL-I 2.6, 3.2, 5.3, 6.1-6.7,
  6.4, 6.5, 7.1, 8.7, 9.1, 9.2, 9.3, 10.1, 10.3, 12.1, 12.4, App. 3; VOL-II 2.3, 3.5, 4.4, 8.4,
  Section 3, Tables 2-2 and 2-4; VOL-IV Form 4-A para 2, Form 4-F rows, Index of Forms, Form 4-E;
  VOL-V 3.1; ADD-01 2.1 and Q3; ADD-02 4.1, 7.1, Q7, Q10 and Table 1-1 (revised) criterion A.
- Every quoted "old" string matches the source wording exactly.
- 6.8 and 12.5 are appended at the ends of their sections, so nothing is renumbered.
- The issue date (Tue 3 Nov 2026) falls after ADD-02 (22 Oct) and before the clarification cut-off
  (Thu 12 Nov 2026). The registration deadline (19 Nov) falls after the issue date.
- The new Table 2-2 values are self-consistent (NH4-N below TN in both columns).

## Verification

`SHA256SUMS` lists the three sealed files by bare name and the PDF by its repository-relative path:

```
cd <this sealed directory>   && sha256sum -c --ignore-missing SHA256SUMS   # three sealed files
cd <repository root>         && sha256sum -c --ignore-missing <sealed>/SHA256SUMS   # the PDF
```

Nothing was committed. The only file written under `rehearsals/blind-02/` is the input PDF.
