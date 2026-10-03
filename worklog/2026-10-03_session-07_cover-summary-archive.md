# Session 07: cover-summary check (C28), review packets, archive rebuilt and verified

- **Date:** 3 Oct 2026, from 08:32 UTC (11:32 Riyadh).
- **Who:**
  - **The owner** gave the instructions below. Their reviews and approvals come later.
  - **The assistant** (Claude Code, in the cloud container) did the work.
- **Approvals:** nothing is approved, accepted, refreshed or applied for the owner:
  - both image readings stay pending;
  - all 202 rows and 37 ops stay proposed;
  - the three STALE-row proposals are not applied;
  - `curation/reviews/decisions.yaml` and `curation/approvals.yaml` do not exist.
- **Not touched:** unanswered assumptions and legal or commercial questions stay unresolved, and the A5 scenario values stay labelled PROVISIONAL.
- **Deferred:** the Claude Code app, OpenRouter and Ollama integrations.

## 1. The exchange (verbatim)

**Owner.** Message text as received (08:32 UTC):

~~~~text
keep the original model name and the full git hstory 

Let’s finish the remaining independent work now , my reviews and approvals will come later.
complete the missing cover summary check. compare each addendum’s summary against its actual provisions, including tables, notes and appendices. report omissions or contradictions; the summary must never decide what gets applied. 
test this against the real pack and a misleading synthetic summary

then run the relevant tests and rebuild the draft archive. check it from a fresh extracted folder: checksums, links, repository history and reproducible outputs. retry delivery of the missing mac offline setup files, splitting them if needed. keep the mac instructions short and clearly distinguish what you tested from what i still need to verify

leave unanswered assumptions and legal or commercial questions unresolved. existing scenario values can stay clearly labelled provisional, but don’t invent answers, approve readings, accept rows or apply the stale-row proposals for me.

keep the review packets ready, with source crops beside the readings, including arabic and image tables. keep the claude code app / openrouter / ollama integrations deferred for now.

update the work log with the actual changes, failures and results.
come back with the updated draft package and a short list separating completed work, remaining technical gaps and items waiting for my review. don’t submit anything yet.
~~~~

**The decision this records:** keep the full git history unchanged. Checkpoint `6a5d6cb`, with the owner's session 05 message as first recorded, stays as it is (session 06 decision 8: settled, no rewrite).

## 2. Timeline

All times are UTC, from the session's tool-call timestamps.

| UTC | Step |
|---|---|
| 08:32 | Owner's message. |
| 08:33–08:40 | Read both real cover summaries, every ADD-01/ADD-02 provision, the drafter's cover handling, the citation parser and the stage records. Expected findings written down from the printed text (§3). |
| 08:40–08:42 | **Failing tests first:** `tests/test_session07_summary.py`, 6 tests. Added `front=` to `make_drill.build` for a misleading synthetic summary. |
| 08:42–08:43 | Run: **6 failed** (no `summary_check`; the drafter test fails on a real gap, §4.2). |
| 08:43–08:49 | `tenderpack/summary.py`; wired into `stage2` (run, reported checks, issues, A2) and `diff`; drafter cover rule. |
| 08:46–08:49 | Two fixes found by the tests: the sentence regex stopped at "5.3" (E75); an invalid op's provision was also called "unchecked" (E76). 6 passed. |
| 08:49–08:51 | Regenerated outputs, both drills and the blind rehearsal's `out-after-fixes`. A3 unchanged everywhere; drafted ops unchanged. |
| 08:51–08:55 | Checked C28 against the blind rehearsal's sealed key: three kinds of false result found and fixed (E77–E79, §4.3); a regression test added. 7 passed. |
| 08:55–08:58 | Regenerated; A2 claims table tidied. |
| 08:58 | Full suite started. |
| 08:58–09:00 | Review packets: looked at batch 1 and the Arabic Form 4-C packet. The full packets were not in the review folder or the archive (E80): copied and linked; test added. |
| 09:00–09:02 | Wheel sizes checked (the PyMuPDF wheel alone is about 24 MB); Mac wheels split into 15 MB parts. `VERIFY_ON_MAC.md` rewritten short (tested vs. to verify). Operating guide, README, plan revision 7. |

## 3. What the real summaries leave out (read from the printed addenda before any code)

**ADD-01** says it "amends the Proposal Due Date, deletes one qualification requirement, amends Volume II Clause 5.3, publishes the minutes of the Pre-Bid Conference, and responds to clarification requests 1 to 6". Not in it:

- Appendix A reissues Form 4-A, replacing VOL-IV Form 4-A;
- 3.1 adds a duty: report a wrongly recorded attendance within five Working Days;
- the answer to request 4 adds a duty: "Bidders shall satisfy themselves as to ground conditions".

**ADD-02** says it "amends the page limit, reissues the technical evaluation table, amends Volume II Clauses 4.4 and Table 2-4, adds Form 4-G, amends Volume V Clause 36.2, reinstates Volume I Clause 8.6, and responds to clarification requests 7 to 14". Not in it:

- note (2) to the reissued Table 1-1 amends VOL-I 11.2: the weighting goes from 60/40 to 65/35;
- 9.2 ends ADD-01 Section 4.2;
- 5.2 adds a process-design duty;
- 9.1 reinstates 8.6 "in the following amended form": 35% instead of 30%, and a new non-responsive consequence. The summary says only "reinstates";
- 7.2 makes a missing Form 4-G non-responsive.

## 4. Changes

### 4.1 C28: `tenderpack/summary.py` (new; report only)

**Parsing:**

- The summary is each "This Addendum <verb> …" sentence in an addendum's cover.
- It is parsed into claims: a verb, plus the things the claim names (split at commas and at "and" when a new item starts).
- Plurals are expanded ("Clauses 4.4 and Table 2-4", "Tables 2-4 and 2-6").

**Matching** (deterministic):

- cited targets match ops on that target or inside it, including footnotes and a Form 4-G added by an addendum;
- the register's date anchors resolve "the Proposal Due Date" to VOL-I 6.1. This uses curation data, not a hardcoded rule;
- "clarification requests a to b" match the answers Qa..Qb. An answer is described only by that claim;
- descriptive items match the best-scoring op among those the verb allows, scored on provision text, target text and target heading. Ties go to the provision whose own text names more of the words. Q&A references ("clarification request 13") are not counted as words;
- an inserted clause is keyed by the number it is given ("new Clause 10.5").

**Findings:**

| Finding | When |
|---|---|
| **omitted** | A change or obligation that no claim covers; an interpretation in a section no claim reaches |
| **understated** | An answer that changes or adds something; a clause reinstated in an amended form |
| **consequence not mentioned** | The provision states a consequence; sentences saying a consequence is "unchanged" are not counted |
| **contradicted** | The verb doesn't fit the op, or a range or count differs |
| **not found** | A claim (or one item of it) that no provision supports |
| **claimed, not applied** | The op is invalid or rejected |
| **unchecked** | The provision is still unresolved and has no op |
| **no summary** | The cover has no summary sentence |

**Where it shows:**

- A2: a "Cover summary vs provisions (C28)" section per addendum, plus `a2_cover_summary_check.csv/json`;
- checks.json: a reported C28 entry per addendum;
- A1 Issues: `I-AUTO-SUMMARY-<stage>` (owner Bid manager; not on A3);
- the `diff` command.

It is never structural, never a release blocker, and never on A3 (whose page is unchanged).

### 4.2 The summary never decides what is applied

- **The engine** applies op files only and never reads the cover summary. Tested: a misleading summary over the real ADD-02 leaves every unit's text and status identical at every stage.
- **A real gap in the drafter, found by a failing-first test.** A cover sentence in operative form ("Volume I Clause 10.6 is deleted in its entirety.") was drafted as a `set_status` op from the cover. Now:
  - summary sentences are removed before matching;
  - from the rest of a cover, only stated obligations are drafted ("Bidders shall acknowledge receipt in Form 4-A");
  - a change stated in cover text stays **unresolved** for a person, with the reason "cover text the drafter never applies".
- The real ADD-01/ADD-02 op files are curated and unaffected. After regeneration, drill A's and drill B's drafted op files (`out-drill/drafted/ADD-03.yaml`, `out-drill-b/out-drafted/drafted/ADD-03.yaml`) are byte-identical to the committed ones (git shows no change). The blind rehearsal's `drafted-ADD-03*.yaml` are historical records of the blind run and were not regenerated.

### 4.3 Checked against the blind rehearsal's sealed key, and corrected

- **The key's cover trap** says the blind summary omits: 2.3, 3.2, 8.2, 9.2, the change inside the answer to Q16, and the new restriction in Q17.
- **C28's first version** found 2.3, 9.2, Q16 and Q17, but also gave false results:
  - **E77:** "amends the Proposal Due Date, the clarification period, the Bid Bond amount and the number of copies" was matched only by its citation, so 3.1, 4.1 and 5.1 were wrongly "omitted";
  - **E78:** the plural "Tables 2-4 and 2-6" was not expanded;
  - **E79:** the inserted Clause 10.5 was not keyed by its number. That gave a false "contradicted" on the 8.2 renumbering and a false "omitted" on 8.1. In addition, "rejection … is unchanged" was taken as a consequence.
- **After the fixes,** all six key items are reported. Every claim of that summary is "supported" (the summary is true as far as it goes). Three literal extras are also reported:
  - 8.1's rejection consequence is not mentioned;
  - 11.2 and 12.2 add duties.
- **Honest limit:** C28 was written after the key had been opened (session 06). This is a regression test on rehearsal 01, **not blind evidence**.

### 4.4 Review packets

- **What was wrong:** batch 1 already showed each unit's crop beside its reading. The full Stage 1 packets were only named as a `build/review/...` path: they were not linked, and not in the archive (E80). They hold every band, cell and numeral at native resolution, with Arabic right to left.
- **Fix:** `write_batches` now copies both into `out/review/packets/` and links them from batch 1 and the index. They are self-contained (data URIs only, no external links).
- **Native size kept:** crops in the packets stay at native size, so a reviewer scrolls sideways. This is deliberate: diacritics and decimal points disappear when scaled (the packet's own note 1).

### 4.5 Mac setup files and instructions

- **The session 06 wheelhouse** (124 MB, then 67 MB and 51 MB per architecture) failed to upload with HTTP 502. The 22 MB archive went through.
- **The PyMuPDF wheel** alone is about 24 MB, so splitting by wheel cannot get every file small.
- **Now:** `make_draft_archive.py --wheels` writes one zip per architecture, byte-split into 15 MB parts with a `.sha256`. They are joined on the Mac with `cat X.zip.part* > X.zip`.
- **`VERIFY_ON_MAC.md`** is rewritten short: a table of what was tested here and what the owner still checks, then four steps.

### 4.6 Other

- `diff` shows the C28 findings.
- `make_drill.build(front=...)` takes alternative front matter; the default build is unchanged.
- The archive README names the packets and C28, and its session range is no longer hardcoded.
- Operating guide (C28; packets), README, plan revision 7 (§13).

## 5. Errors in this session (continuing from E74)

| # | Error | Found by | Fix |
|---|---|---|---|
| E75 | The summary-sentence pattern ended at the first full stop, so "Volume II Clause 5.3" became "Clause 5" and the claim list was cut | First run of the new tests | A sentence ends at a full stop followed by a capitalised word, or at the end |
| E76 | A provision whose op is invalid was also reported as "unchecked (no op yet)" | Synthetic drill test | Provisions with an op are reported with that op ("claimed, not applied" or "omitted … op INVALID") |
| E77 | A claim naming several things ("the Proposal Due Date, the clarification period, the Bid Bond amount and the number of copies") was matched only by its one citation; the other three were wrongly "omitted" | Checking against the blind key | Each named item is matched on its own |
| E78 | The plural "Volume II Tables 2-4 and 2-6" was not expanded | Same | Expanded like "Clauses" |
| E79 | An inserted clause was not keyed by its new number, giving a false contradiction (renumbering) and a false omission. "the consequence of rejection, is unchanged" was taken as a consequence | Same | Inserted clauses are keyed by "new Clause N"; a claim keeps only the ops its verb describes; "unchanged" sentences are ignored |
| E80 | The full review packets (every band and cell; Arabic Form 4-C) were named only as a `build/review` path and were not in the archive | Looking at batch 1 rendered | Copied into `review/packets/` and linked; test added |
| E81 | Three mistakes in the first version of the new tests: the A1 Issues sheet was read as a list; a convoluted release-blocker assertion; the first "omitted" finding was picked instead of Appendix A's | Running them | Corrected; no expectation about the pack was changed after seeing output, except 3.1's kind (decided before implementing, §4.1) |
| E82 | The first full-suite run (08:58) had collected the code before the packets change | Timing check | Full suite run again on the final code (§6) |

