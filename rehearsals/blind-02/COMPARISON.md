# Blind rehearsal 02: results against the sealed answer key

## How the rehearsal ran

- **The addendum.** An independent subagent wrote it from the pack's PDFs and the brief only (`FROZEN.md`). It did not read the tool's code, tests, curation, outputs or docs (`SEALED/author_notes.md`). It also read the blind-01 addendum so that this one would avoid overlapping with it.
- **The freeze.** The PDF and the sealed `SHA256SUMS` were frozen by hash in `FROZEN.md` on 3 Oct 2026 at 20:25 UTC, before the addendum was opened. The sealed files were kept outside the repository until the curated outputs and the `diff` had been written.
- **Unsealing.** The key was opened on 4 Oct 2026 at 06:52:58 UTC, after the last curated build (06:52:41) and the diff (06:52:48). All four hashes matched: `sha256sum -c SEALED/SHA256SUMS` passed from the sealed folder for the three files, and from the repository root for the PDF. The hash of `SEALED/SHA256SUMS` equals the one in `FROZEN.md`.
- **Who curated.** The assistant curated, acting as the live-session curator. It also wrote the tool, which is the main limit on how blind this was. It knew in advance that the addendum would be "unseen-style" and would differ from blind-01. It did not know the provisions, the values or the planted errors.
- **What is scored.** Only what was produced blind is scored: `out-drafted/`, `out-curated/` (the 06:52:41 build), `diff-ADD-02-to-ADD-03.md` and the `work/` curation as committed in `ec8085b`. Changes made after unsealing are listed separately at the end and are not counted as hits.
- **Nothing is decided.** Every op and every row is PROPOSED. Nobody accepted or rejected anything, and the release blockers say so.

## Timeline (UTC, from `clock.txt`)

| Step | Start | End | Elapsed |
|---|---|---|---|
| Set up the pack and ingest (7 documents, 579 units; C01–C10 pass) | 06:20:31 | 06:20:45 | 0:14 |
| Draft (9 ops from patterns; 32 provisions left for a person) | 06:20:49 | 06:20:49 | — |
| Drafted working draft published (ADD-03 PARTIAL; validated state stays ADD-02) | 06:20:50 | 06:21:57 | 1:07 |
| Curation: read every ADD-03 unit and the target units, then write the op file (31 ops, 5 dispositions) | 06:22:16 | 06:35:47 | 13:31 |
| **Live fixes 1–3:** "Volume I Appendix 3" citation and a cited group's only unit; form rows named in quotes; re-lettering stated as a range. Three op targets corrected | 06:36:26 | 06:37:24 | 0:58 |
| Register: 8 new rows, 37 re-made readings, 11 summaries made stage-neutral, 6 issues; A5 templates and assumptions; clarification register | 06:37:24 | 06:45:25 | 8:01 |
| Curated outputs, first attempt: **refused** (C47) | 06:45:32 | 06:46:56 | 1:24 |
| **Live fix 4:** C47 read a full stop moved by a deletion as an added word. The first attempt broke two true matches and was corrected | 06:47:13 | 06:49:05 | 1:52 |
| Curated outputs published (structural checks pass; 4 rows STALE) | 06:49:05 | 06:50:29 | 1:24 |
| 4 STALE rows re-made; 3 earlier-stage readings re-pinned after not-yet-issued ADD-03 units were added to their rows | 06:50:29 | 06:51:10 | 0:41 |
| Curated outputs published again (**the scored output**: STALE none; blocked only by the decisions nobody has made) | 06:51:19 | 06:52:41 | 1:22 |
| `diff` ADD-02 → ADD-03 | 06:52:48 | 06:52:48 | — |
| **Unseal** | 06:52:58 | | |

Elapsed from receipt to the scored output: **32 minutes**. That includes about ten minutes, early in the curation (06:22–06:33), when the assistant's working context was being summarised and no curation was done. The curation and its fixes took about 20 minutes of actual work; every build took about 1.5 minutes.

## Results

**Count:** 30 provisions, answers and notes: 24 hits, 6 partial, 0 missed. The scored outputs reproduce every expected date (one, the look-back start, by its alternative reading; see below). Every "must not report" trap was avoided. **But:** the cover-summary check (C28) missed both planted cover errors, and A3 is missing two inferential disqualifiers that the key expects.

### Body provisions

| Key | Expected | Result | Evidence in the blind outputs |
|---|---|---|---|
| 1.1, 1.2 | recitals, no effect | **hit** | `no_effect` dispositions with reasons |
| 2.1 | 6.1 time 14:00 → 11:00; date unchanged; 6.6 and 6.7 bite at 11:00 | **hit** | `VOL-I:6.1` reads "11:00 hours … Thursday 26 November 2026". The `VOL-I-6.1-01` chain is ADD-01/2.1 (date), then ADD-03/2.1 (time). A3 lists 6.6 rejection citing "ADD-01 2.1 p1, ADD-03 2.1 p1". The 8.3, 3.4 and 6.7 readings were re-made with "26 November 2026, 11:00". The 5.2 cut-off stays 2026-11-12 |
| 2.2 | ADD-01 2.1 second sentence ceases | **hit** | `replace_text` removes the sentence from `ADD-01:2.1` |
| 2.3 | Appendix 3 replaced (box, floor, building, marking 11:00) | **hit** (after live fix 1) | `VOL-I-App3-01` re-made with a new quote and marking. The A5 `deliver` and `seal-and-mark` activities were updated |
| 2.4 | new 6.8; register by Thu 19 Nov 2026; late Proposal under 6.6 | **hit** | Row `ADD-03-6.8-01`: `DELIVERY-REGISTRATION: 2026-11-19`, consequence `rejection`. The diff reports "ENTERS ADD-03-6.8-01" in A3. A5 has `register-reps` with that deadline as a predecessor of `deliver` |
| 3.1 | 7.1 150 → 180; expiry 2027-04-25 → 2027-05-25 | **hit** | the diff gives `PROPOSAL-VALIDITY 2027-04-25 -> 2027-05-25` |
| 3.2 | 6.3 180 → 210; expiry 2027-05-25 → 2027-06-24 (the "180" trap) | **hit** | `BID-BOND-VALIDITY 2027-05-25 -> 2027-06-24`. A2 notes the same words in 7.1 and that they were not targeted. Partial point: the A5 bond activity says "validity per VOL-I 6.3", not "210 days" |
| 3.3 | Form 4-A para 2 read as 180 | **hit** | `VOL-IV-F4A-04` re-made with `validity_days: 180`. Beyond the key: the Form 4-A in use (the ADD-01 App A reissue) has no paragraph 2 (`I-ADD03-F4A-PARA2`) |
| 4.1 | opinion deleted from 10.3; A1 row deleted at ADD-03; removed from the pre-submission A5 | **partial** | The words are deleted and the rest of 10.3 stands. `VOL-I-10.3-02` shows **AMENDED**, not deleted: its note says "NO LONGER A PROPOSAL REQUIREMENT", but the register has no status for an obligation whose words are deleted from a clause that stays in force. In A5 the opinion became a conditional post-award step, but `model-auditor-appoint` and `model-audit-review` stayed in the pre-submission programme |
| 4.2 | new 12.5, post-award, no consequence, not on A3 | **hit** | `ADD-03-12.5-01` is `contractual_post_award`, with the post-award evidence "proposed" and not on A3 |
| 4.3 | Form 4-F rows deleted | **hit** (after live fix 2) | `set_status deleted` on both rows |
| 5.1 | night 45 → 40 dB(A); day unchanged | **hit** | the op plus a `confirms` op with `expect` "55 dB(A) by day" |
| 5.2 | ADD-02 4.1 revoked; 72 h again (not 96, not "no change") | **hit** | `ADD-02:4.1` is revoked, `VOL-II:4.4` reads 72, and `VOL-II-4.4-01` gives 72 at ADD-03 with the chain shown |
| 5.3 | 22% → 25%; landfill threshold replaced (a tightening) | **hit** | two ops; `VOL-II-8.4-02` re-made as "any landfill disposal" needs consent |
| 6.1 | Table 2-2 replaced: TN 60/85, NH4-N new, TP peak 14 → 16, min 12 °C | **hit** | `replace_unit`; the rows follow by key and the NH4-N row was added to `VOL-II-2.1-01`. The op and row notes list all four changes, including TP 14 → 16, which the addendum's narrative does not mention. Reporting gap: `diff` did not list `VOL-II-2.1-01` or `VOL-II-3.1-01` as changed, because their primary units are unchanged |
| 6.2 | reflect Table 2-2 (revised) in the process design | **hit** | row `ADD-03-6.2-01` |
| 7.1 | re-letter 9.1 (f)–(j); dividers follow | **hit** (after live fix 3) | `renumbers`, with the inserted Form 4-G item as (f). `VOL-I-9.1-01` lists (a)–(j). A5 assembly follows the re-lettered list |
| 7.2 | Index of Forms row for Form 4-G | **partial** | Recorded as an annotation and the row `ADD-03-7.2-01`, not as a new row of the index table: the provision gives the entry in prose, and the engine inserts only text that is printed. The curator's first note wrongly said the index was missing; that was corrected before the build (06:43) |

### Clarification answers

| Key | Expected | Result | Evidence |
|---|---|---|---|
| Q15 | withdraws ADD-01 Q3; incorporated bank only; A3 yes (inferential, medium confidence) | **partial** | `ADD-01:Q3` revoked; `VOL-I-6.4-02` re-made; `I-ADD03-Q15` notes that the answer narrows 6.4. **A3 miss:** the curator classed "will not be accepted" as a `lesser` consequence, which took `VOL-I-6.4-02` out of the A3 general gate, where it had been at ADD-02 |
| Q16 | legalise or apostille Powers of Attorney executed abroad; "(i) as re-lettered" means Powers of Attorney; A3 yes (inferential); A5 long lead | **partial** | Trap avoided: the op targets the 9.1 list, and its note and `I-ADD03-Q16` map item (i) to the Powers of Attorney issued as (h), not to the certificates. Row `ADD-03-Q16-01`. A5 `poa-legalise` per foreign member (INFEASIBLE by 5 WD). **A3 miss:** the same `lesser` choice took `VOL-I-9.1h-01` out of the gate |
| Q17 | confirms ADD-02 Q10; no O&M guarantee | **hit** | `confirms` on 8.7; no new obligation |
| Q18 | withdrawn; no effect | **hit** | `no_effect` |
| Q19 | no amendment; conflict stays open | **hit** | `confirms` with `expect` on both clauses. `VOL-I-12.1-01` and `VOL-V-3.1-01` re-made, and `CQ-CONCESSION-TERM` updated (Form 4-E route) |
| Q20 | second USB in Envelope B; 6.5 copy Envelope A only; passwords 11:00–12:00; A3 via 6.2 | **hit** | rows `ADD-03-Q20-01` (A3 ENTERS, non-responsive via 6.2) and `ADD-03-Q20-02` ("by 12:00"); `CQ-USB-PACKAGING` and `CQ-ENV-B-CONTENTS` re-read |
| Q21 | date not extended; not read as "PDD unchanged" | **hit** | `confirms` with `expect` on the date; the time still moves |

### Appendix A notes

| Key | Expected | Result | Evidence |
|---|---|---|---|
| Note (1) | definitional | **hit** | content of the 6.1 replacement; no row |
| Note (2) | 12 °C for nitrification | **hit** | `ADD-03-6.2-01` `min_design_temperature_c: 12` |
| Note (3) | simulation report ≤ 25 pages outside the limit; zero marks on criterion A; flag the threshold risk, not as a disqualification | **partial** | Row `ADD-03-T22n3-01`, kept off the A3 disqualifiers, as the key accepts. But it was classed `score_elimination`, which the tool labels "Envelope B returned unopened": wrong for a zero on one criterion. No threshold-risk flag either (25 marks; the score is then capped at 75 against the threshold of 70) |
| Note (4) | 2.3 50% → 25% (an amendment inside a note) | **hit** | op on `VOL-II:2.3`; `I-ADD03-NOTE4` |

### Cover summary (the planted errors)

| Key | Result |
|---|---|
| E1 "The Proposal Due Date is unchanged" (the time moves) | **missed by C28**: the sentence was never extracted as a claim. The curated state is right (26 Nov 2026, 11:00), but no output says the cover statement is wrong. The curator's own op note only repeats it ("the Proposal Due Date is stated to be unchanged") |
| E2 bond validity (3.2) not on the cover | **missed by C28, and inverted**: C28 matched "extends the Proposal validity period" to 3.2 (the Bid Bond) and so reported 3.1 as omitted. The curated state applies both correctly |
| other C28 output | Correct: 2.2, 4.2, 5.2(a), 6.2, 7.2 and note (4) omitted; Q15/Q16/Q20 understated. False positives: 4.1 and 7.1 reported as omitted, because C28 merged "removes the model audit opinion …, re-letters Volume I Clause 9.1" into one claim and matched it only to 4.3. Not reported: TP 14 → 16 (it appears only in the curation notes) |

### Dates, marshalling, A3 and traps

- **Dates: all correct, or one day apart by a stated convention.**
  - clarification cut-off 2026-11-12 (unchanged);
  - registration 2026-11-19;
  - PDD 26 Nov 2026 at 11:00 (text and quotes; the date column shows dates only);
  - password window 11:00–12:00 (row text);
  - validity 2027-05-25; bond 2027-06-24;
  - model audit opinion: PBN + 45 days (not dated);
  - the footnote 12 look-back is unchanged. Its planning value is 2016-11-27 (boundary exclusive); the key's 2016-11-26 is
    the inclusive reading, which A1 records as the second of "two readings" (C32). One day apart, by stated convention.
  - The day-0 / day-1 readings are shown (C32), and the stated convention gives the key's dates.
- **Marshalling plan.**
  - Added and changed items are all present: registration, second USB, password step, simulation report, legalisation, address and marking, bond issuer, dividers, Envelope A-only USB, Form 4-A notes.
  - Removed items are only partly handled: the auditor appointment and review stayed in the pre-submission programme (see 4.1).
- **A3.**
  - Correct: 6.6 now cites ADD-03 2.1; 6.8 entered; Q20 via 6.2 entered; Q19 and the stale Form 4-A entry are among the unresolved matters (`I-CONCESSION`, `I-ADD03-F4A-TIME`).
  - Missing: Q15 and Q16, and two existing gate rows dropped out (the `lesser` choice).
- **Must not report: all avoided.**
  - no PDD date change, no O&M guarantee, no amendment to 12.1 / VOL-V 3.1;
  - bond amount, hard copies, page limit, Table 1-1, 65/35, 70, 8.6 and Table 2-4 untouched;
  - 4.4 at 72, not 96; BOD5/COD/TSS unchanged.
- **Ambiguities.**
  - Dates only for the periods counted from the PDD, as the key expects.
  - Password window read as 11:00–12:00.
  - Counting conventions shown.
  - Note (3) kept off A3 (accepted).

## Live fixes made blind (general tool gaps, each with a regression in `tests/test_blind02_live_fixes.py`)

1. **Appendix citations.** "Volume I Appendix 3" is now a citation. A cited group whose only unit is the target accepts that unit (a group with two paragraphs still needs the one named).
2. **Quoted row names.** Form rows named in quotes ("the rows 'Model auditor' and 'Date of model audit opinion'") are now row names.
3. **Letter ranges.** A re-lettering stated as a range ("(f) to (i) become (g) to (j)") now states every letter in the range.
4. **C47 punctuation.** C47 lines words up without the punctuation around them, so a deletion that moves a full stop onto the word before it does not count as an added word. The added words are still checked as printed. The first attempt stripped the punctuation from the checked words too, which broke two true matches ("main, subject", "2, First"); C47 failed on them and the fix was corrected within two minutes.

Curator errors the tool caught before the scored build: two `annotate` targets that the provisions do not cite (Q16 at `VOL-I:9.1(h)` and Q21 at `VOL-I:6.1`, both refused by C22); two issue themes outside the A3 vocabulary; and the wrong "no Index of Forms" note.

Curator errors the tool did not catch, which the key exposed: the `lesser` class on Q15 and Q16, the `score_elimination` class on note (3), and the model-auditor activities left in the pre-submission programme.

## Changes after unsealing (not counted)

Made between 06:57 and 07:03 UTC (`clock.txt`, "POST-KEY") in `work/`, rebuilt into `out-after-fixes/`. Each one is
marked "Post-key fix" in the row or file it changes. Not scored as hits.

1. **Q15 and Q16 back on A3.** `VOL-I-6.4-02` and `VOL-I-9.1h-01` (at ADD-03) and the new `ADD-03-Q16-01` no longer carry
   a `lesser` consequence. They sit in the A3 general gate (VOL-I 11.1(i)), with notes that quote the refusal words and say
   the step to rejection is inferred (medium confidence). For C46, the `VOL-I:6.4` disposition gets a `consequence_note`.
   The gate goes from 35 to 38 items.
2. **Note (3) class.** `ADD-03-T22n3-01` is classed `lesser`, not `score_elimination`. Its note now states the threshold risk:
   criterion A is 25 of 100 marks, so the score is capped at 75 against the threshold of 70.
3. **A5.** The model-auditor appointment and review are now conditional post-award steps (Preferred Bidder, VOL-I 12.5),
   no longer in the pre-submission programme. The Bid Bond activity states 210 days.

`out-after-fixes/`: exit 0, STALE none, C46 clean, C47 pass. `scripts/verify_archive.py` rebuilds it. The scored state is
commit `ec8085b`.

**Tool follow-ups for the plan** (not done here; each needs its own test and a check against the real pack):

- **C28 claims.** Extract "X is unchanged" claims and test them against every op on X: the Proposal Due Date is the date
  and time in VOL-I 6.1 (2.6). Match "the Proposal validity period" to 7.1 rather than to the Bid Bond's validity. Split a
  claim that names two changes.
- **`diff` for multi-unit rows.** Report a row as changed when a unit other than its primary one is replaced or amended
  (here `VOL-II-2.1-01` and `VOL-II-3.1-01`).
- **Deleted words.** Add a register status for an obligation whose words are deleted from a clause that stays in force
  (here `VOL-I-10.3-02`, which shows AMENDED).
- **Index rows in prose.** Insert a row of an index table from an entry described in prose ('an entry for Form 4-G with the
  title …, Envelope 'A' and Status 'Mandatory'') as a `set_value`-style row, with each cell checked against the provision.
- **Curator guidance.** Do not use `lesser` for a refusal of a submitted document ('will not be accepted', 'treated as not
  submitted'): the step to the Proposal's fate is inferred, so the row stays in the gate. Clarify that `score_elimination`
  means the VOL-I 11.3 threshold, not a zero on one criterion.
