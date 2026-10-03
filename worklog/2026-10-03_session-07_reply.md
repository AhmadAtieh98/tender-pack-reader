# Session 07: reply to the owner (verbatim, as sent)

The updated draft package is attached (`LAMAR-PPP-R2-DRAFT_9fdfd96.zip`, 28 MB). Nothing has been submitted, approved, accepted or applied for you. The git history is kept in full, as you asked.

**Completed**

- **Cover-summary check (C28):** each addendum's summary is compared with its actual provisions, including tables, notes, appendices and answers. It reports omissions, understatements, consequences the summary leaves out, contradictions and claims that nothing supports. Findings appear in A2, the A1 Issues sheet and `diff`. It is report only: the summary is never applied.
  - **ADD-01's summary leaves out** the reissued Form 4-A (Appendix A) and the 5-Working-Day attendance-reporting duty (3.1). It also understates answer 4, which adds a duty.
  - **ADD-02's summary leaves out** the change to Volume I Clause 11.2 hidden in note (2) to the reissued table (60/40 → 65/35 weighting), the end of ADD-01 Section 4.2 (9.2), and a new design duty (5.2). It says only "reinstates 8.6", but 9.1 reinstates it in an amended form (35% instead of 30%, with a new non-responsive consequence). It also doesn't mention that a missing Form 4-G makes the Proposal non-responsive (7.2).
- **Real gap fixed:** the drafter would have drafted a deletion from an operative-looking sentence in an addendum's cover. Cover text can now only produce obligations; any change it states goes to a person.
- **Tests:**
  - 6 tests written first, from the printed addenda, all failed before the code existed and pass now. They cover the real-pack findings and the cases below;
  - a misleading summary over ADD-02 changes nothing that is applied;
  - a misleading synthetic Addendum No. 3, run end to end, has every planted error reported;
  - the blind rehearsal: C28 reports all six omissions in the sealed key. C28 was written after that key was opened, so this is a regression test, not blind evidence.
  - Full suite: 347 passed, here and again offline inside the fresh-folder check.
- **Review packets:** the full packets for both image readings (Table 2-4 cells, the Arabic Form 4-C bands and numerals, native crops beside every reading) are now in `REVIEW/packets/`, linked from batch 1.
- **Archive:** rebuilt and checked in a fresh folder. All 215 files match their checksums, all A3 and review-page links resolve, and the repository bundle clones with its full 19-commit history (as you asked, nothing rewritten). With no network, it reinstalled, regenerated every committed output byte-identically (167 deliverable files identical to the archive) and passed all tests. The full offline run was on `9888b63`. The final `9fdfd96` differs only in the work log and one row of the Mac guide; its deliverables are byte-identical, and its checksums, links and history were checked again.
- **Mac files:** delivered this time as 15 MB parts with checksums: 5 parts for Apple silicon, 4 for Intel. I joined them and checked the checksums here. Every requirement resolves offline for Python 3.11–3.13 on Apple silicon and on Intel with macOS 14 or later. I could not install them on an actual Mac. `VERIFY_ON_MAC.md` is now short and separates what I tested here from what you still need to check.
- **Work log:** `worklog/2026-10-03_session-07_cover-summary-archive.md` records the changes, the failures (E75–E83) and the results.

**Remaining technical gaps**

- **C28 judgement calls:** matching descriptive phrases ("the clarification period") uses word overlap, which can be wrong. Every match is shown in A2 for you to check.
- **Not tested on a Mac,** nor in Preview (A3 links) or Excel.
- **A3 headroom with a third addendum** was small in the rehearsal (scale 0.904 against a 0.9 floor). The condensation steps exist.
- **Not built:** C41's check that A5 inputs hold no literal dates, and a hash manifest for the Stage 2 outputs (C42). Determinism itself is checked.
- **Deferred, as you asked:** the Claude Code app, OpenRouter and Ollama integrations.

**Waiting for your review**

- The two image readings (batch 1 and `REVIEW/packets/`).
- 202 rows and 37 ops, all proposed. Start with the 19 disqualifier rows (batch 2) and the 37 ops (batch 3).
- The three STALE-row proposals (batch 4); not applied.
- The C28 findings: whether any warrants a clarification before the 12 Nov cut-off.
- **Still open:**
  - the LCC lead time and issuer;
  - the legal and commercial calls (the Form 4-C exclusion category, Form 4-A, Envelope B, prices in Envelope A, the concession term, the Volume III gap);
  - the A5 assumptions, which stay labelled PROVISIONAL.
