# Session 04: the assistant's final reply (verbatim)

~~~~markdown
Session 04 is finished, and I stopped before Stage 3. Everything is committed and pushed to `claude/hopeful-curie-7oki9q`. Every interpretation and amendment op is my proposal and nobody has reviewed them yet. Both image readings are still waiting for your review, and nothing is approved (`curation/approvals.yaml` doesn't exist).

**Repairs.** I reproduced all three gaps; I don't dispute any of them. I wrote failing tests first (14 failed, 1 guard passed), then fixed the code. An adversarial review agent then found about 30 ways around those fixes. Its attacks became tests (34, then 14 more, failing) and are now fixed too.
1. **Evidence checks.** Each cell's text is checked in order and in its column, along with normalized values and each anchor's real page and box. On top of that, every unit is compared with an independent re-segmentation of the PDF. Units read from images are rebuilt from their reading and tied to their crop.
2. **`45 dB(A)`.** The raw transcription is unchanged. On display, the English expression keeps its left-to-right order inside the Arabic. It is tested against a correctly drawn source, and digits-only verification is labelled PARTIAL.
3. **`--require-approved`.** The gate now runs before publishing. A rejected build goes to `<out>.rejected`, and the previous build stays untouched.

**Stage 2 (26 rows, not the full register).**
- **One amendment path.** I wrote op files for ADD-01 and ADD-02, starting from the drafter's output. An addendum without an op file is drafted and goes through the same engine. Every provision is accounted for: by an op, as no effect, as outside the slice, or as unresolved.
- **Outputs in `out/`:**
  - A1 in Excel, CSV and JSON, with the status after each stage;
  - A2 with changes, rows that move and why, and evidence chains;
  - A3 on one page;
  - A5 built from the A1 rows, with lead-time assumptions labelled and infeasibility flags.
- **What it found:**
  - **LCC:** deleted, then reinstated at 35% with "non-responsive". ADD-01 4.2 is revoked. With my 30-day lead-time assumption, the certificate is infeasible by 7 Working Days.
  - **PDD:** moving it from 12 to 26 Nov moves the clarification cut-off and the dates that depend on it. VOL-I 8.3 is marked STALE.
  - **72-hour change:** VOL-V 31.3 has the same words but is left untouched.
  - **Form 4-A:** it still prints 12 Nov. This is raised as an issue, not corrected.
- **Proved by tests:**
  - an op aimed at the wrong clause is rejected;
  - a changed dependency marks rows STALE;
  - pending image status carries through to A1, A3 and A5;
  - a partial addendum keeps the last validated state;
  - transcription approval stays separate from interpretation (tested only in a fixture copy).
- **Drill (`out-drill/`).** A synthetic ADD-03 is drafted and applied. It stays PARTIAL: one op is rejected because ADD-02 had already replaced its words, and one provision is unresolved. So the validated state stays at ADD-02.

**The hiring team's reply** is recorded as received in `sources/correspondence/2026-10-02_reply_from_hiring.eml`. As they asked, the Volume III gap is now Issue `I-VOL-III` on A3. Delivery is by 17:00 Monday 5 October.

**Tests:** 237 pass, and repeated builds are byte-identical. Passing tests don't mean the interpretations are correct, and they are not approval.

**Decisions needed from you:**
1. Do you accept the Stage 2 shape (op model, rows, outputs) as the basis for Stage 3?
2. Should working outputs apply proposed ops (as now), or only ops you have accepted?
3. Lead times, especially the LCC certificate's 30 Working Days, which drives the infeasibility.
4. Counting conventions: keep the conservative reading, or fix each rule?
5. Legal calls: the Form 4-C "exclusion" category, the date printed on Form 4-A, and whether ADD-01 Q2 still applies.
6. Please approve or correct both image readings yourself.

The report is `docs/session-04_report.md` and the work log is `worklog/2026-10-02_session-04_repairs-and-stage2.md`.
~~~~
