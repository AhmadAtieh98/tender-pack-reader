# Session 08: before and after

For the owner. The full record is `worklog/2026-10-03_session-08_review-confirmations-a5-clarifications.md`, and your messages are kept verbatim in `worklog/2026-10-03_session-08_prompt.md`. **Nothing was sent to anyone, nothing was submitted, and no row or op has been accepted.** Your decisions are still needed (§4).

## 1. Before and after

| Area | Before (session 07) | After (session 08) |
|---|---|---|
| Rejected op | reject → rebuild → reject could apply it again | A rejection always withholds the op; decisions bind to the state just before each op; the engine runs once |
| Table replacement | A changed old member row left a decision on the replacement valid | Every member row of both tables is bound; any change voids the decision |
| Inserted obligation | The anchor's existing row satisfied C46 | The inserted item and the inserted group each need their own row |
| 1-WD task, Friday/holiday deadline | Window on the non-working day | Last Working Day before it; the legal deadline is unchanged; explicit flags |
| Op states | Valid and rejected were conflated | Valid / withheld / applied are kept apart; "rejected" is distinct from "unresolved" |
| Your reading confirmations | Pending | Recorded as yours (Ahmad, 3 Oct 2026; your message is the record), pinned to the versions you reviewed, with their limits. **Permit: only the location of the precedence language is confirmed**, not its contents or compliance |
| 8.3 / 3.4 / 6.7 | STALE; earlier proposals conflicted with your direction | New evidence-backed proposals applied through the workflow. The originals are kept, with the exact conflicts. The rows are **PROPOSED**: you decide |
| A1 | Form 4-G merged; first unit only; 33 blank post-award fields | Six Form 4-G rows; every unit and value exported, with each stage's source and status; post-award fields filled (proposed / not applicable / unresolved; none implies evidence is held) |
| A3 | One list | One page: explicit consequences by category; the VOL-I 11.1(i) gate; open matters grouped by theme with clarification ids, each linked to its detail. Form 4-A's consequence applies to execution, not to every blank field; the late-submission line cites ADD-01 2.1 |
| A5 | Late dates only | Forward and backward passes, float, effort vs waiting, three statuses, decision gates, conditional items, overloads (reported, not levelled), a complete marshalling plan, a Gantt, and an editable consortium of three members, one of them foreign |
| Clarifications | None | 21 draft questions with the fields you listed, verified against the pack; settled points kept settled; your interim approaches; **not sent** |
| Unseen addendum | Blind rehearsal 01 | Blind rehearsal 02 through the normal pipeline: 24 of 30 hit, 6 partial, none missed; two cover errors missed by C28 (§3) |

## 2. Verification (actual results)

- **Regressions:** the four findings' tests failed before their fixes and pass now (`tests/test_session08_audit.py`), alongside `test_session08_outputs.py`, `test_session08_a5.py` and `test_blind02_live_fixes.py`.
- **Full suite:** 386 passed on `2708261` (29 min 37 s); **390 passed** with the four live fixes (29 min 59 s).
- **Fresh build:** the real pack's outputs rebuilt with today's code are byte-identical to `out/` (every file, including the review packets).
- **Strict mode:** `outputs --strict` exits 3 and refuses the release. The only blockers are 205 rows and 37 ops without a named decision; there is no reading or STALE blocker. This is the correct answer until you decide them.
- **Archive** (`LAMAR-PPP-R2-DRAFT_eb32b13`), checked in a fresh folder: every checksum matches; A3 is one page with 537 working links; the bundle clones with its full history; offline, with no network, everything committed regenerates byte-identical, and 391 tests pass. Content and rendering are reported separately: here all 181 output files are byte-identical. On your Mac, PDF and XLSX bytes may differ while their content matches.
- **Environment checked:** Linux x86_64 only (Python 3.11.15, PyMuPDF 1.28.2, openpyxl 3.1.5). The Mac and native Excel/PDF viewers were not checked.

## 3. Blind rehearsal 02 in one paragraph

An independent author wrote a 4-page Addendum No. 3, and its key was sealed before the addendum was opened. The assistant ran it through ingest, draft, curation, pin, check-register, outputs and diff in 32 minutes, about 10 of which were an interruption.

**What was right:**

- every expected date, and every trap (the time moved on an unchanged date; a revocation back to 72 h; "(i) as re-lettered"; Q17/Q19/Q21 have no effect).

**What was not:**

- **C28 missed both planted cover errors.** It did not test "The Proposal Due Date is unchanged", and it inverted the Bid Bond validity omission.
- **A3 lost two rows.** The curator classed the Q15/Q16 refusals as `lesser`, which took two rows off the A3 gate.
- **Three smaller gaps:** note (3) was mis-classed; the model-auditor steps stayed in the pre-submission programme; `diff` misses multi-unit rows whose secondary units changed.

**Four live fixes** (general, tested) leave the real outputs unchanged. The post-key fixes are marked and not scored. The tool follow-ups are in PLAN §14.

## 4. What remains for you (grouped)

1. **Decisions:**
   - accept or reject the 205 rows and 37 ops (batches 2–9), including the 8.3, 3.4 and 6.7 rows;
   - decide which clarification questions to send, if any, before the 12 Nov cut-off.
2. **A5 assumptions:**
   - replace the provisional durations, efforts and the consortium make-up with real figures;
   - check the two INFEASIBLE chains (Local Content Certificate, delivery).
3. **Open source points:**
   - Form 4-C diacritics;
   - "exclusion" vs the other categories;
   - the Table 2-4 qualifier with the chlorine/pH ranges;
   - the missing Permit (contents and compliance not confirmed);
   - VOL-I 12.1 vs VOL-V 3.1.
4. **Checks only you can do:**
   - open `a1.xlsx` in Excel and the PDFs in a native viewer, and run the archive on your Mac (`docs/VERIFY_ON_MAC.md`);
   - a visual review of A3 and the Gantt;
   - your own rehearsal of a live addendum.
5. **Before final submission:**
   - this is a stopping point for your review. Nothing has been submitted.
