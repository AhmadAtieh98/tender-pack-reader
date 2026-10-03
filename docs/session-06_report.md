# Session 06: review fixes, decisions workflow, live commands, blind rehearsal, draft archive

Full record: `worklog/2026-10-03_session-06_review-accept-blind-archive.md`.

**Pending your review (nothing has been decided for you):**

| Item | Status |
|---|---|
| Image readings (Table 2-4, Form 4-C) | **pending** |
| Register rows | 202 of 202 **proposed** |
| Amendment ops | 37 of 37 **proposed** |
| STALE rows (VOL-I-8.3-01, VOL-I-3.4-01, VOL-I-6.7-01) | 3; proposals prepared, **not applied** |
| Decisions file (`curation/reviews/decisions.yaml`) | does not exist; only you create it, by deciding |

`outputs --strict` refuses a release in this state (exit 3). Stopped before final submission.

## 1. Your four findings: all confirmed, none disputed

Reproduced on `3c97a8d`. Failing tests were written first (12 failed, 4 controls passed), then the rules were fixed.

| # | Before (reproduced) | After |
|---|---|---|
| 1 | "all tender requirements are waived" appended to the Form 4-G insertion: op valid, ADD-02 APPLIED, build exit 0 | **Op check (C21):** the whole inserted text must be printed in the addendum. **New structural check C47:** every word any unit gains at a stage must be printed in that stage's addendum. Both refuse the waiver |
| 2 | "All other terms remain unchanged except that each bidder shall submit a certificate of good standing" was dropped as harmless; the addendum showed APPLIED | Benign wording must match the **whole** sentence. A qualifier ("except", "provided that", …) or change words left over make the provision **unresolved**. The same rule applies to cover text |
| 3 | Drill B without its good-standing row: no coverage warning; the disqualifier vanished from A3 | **New check C46:** every obligation an op creates or amends must reach an A1 row, A3 when the provision carries consequence words, and A5. A gap is a release blocker and an A3 issue. On your point about `dispositions.py`: it does what it claims (accounts for provisions); the missing step was from op to rows, hence the new `trace.py` |
| 4 | YAML flags with no reviewer counted as accepted. A3 had no confidence and cut the LCC 35%. "slice" labels remained | Only decisions recorded by `accept` and bound to content count (§2). A3 shows every item's confidence and the full requirement; the LCC line shows "not less than thirty-five per cent (35%)". All "slice" labels are gone; outputs say WORKING DRAFT |

**A3, real pack:** one page, smallest text 7.91 pt, no condensation.

## 2. What was built

### `accept` / `reject`

```
tenderpack accept VOL-I-8.6-01 ADD-02/9.1 --reviewer "Your Name" [--note ...]
tenderpack reject ADD-02/8.1 --reviewer "Your Name" --note "..."
```

- **Binding:** each decision binds to a fingerprint of the row or op, its evidence items and its dependency values.
- **If any of these changes** (e.g. a new addendum), the decision shows as **CHANGED** and no longer counts.
- **A rejected op** is withdrawn and its addendum becomes PARTIAL.
- **Refusals:** placeholder names, STALE rows, invalid ops, and rejections without a note.
- **Tested only in disposable copies**, with "Fixture Test Reviewer".

### STALE-row proposals

- **File:** `curation/register/proposals/2026-10-03_stale-rows.yaml`.
- **Contents:** a re-made interpretation for each of the 3 rows, with the quote and the reason.
- **To use one:** `apply-proposal P-STALE-… --by "Your Name"` writes it and pins only that row. You then accept or reject the row.

### Review batches

`out/review/index.html` has 244 items in 9 batches, each item with its crops and the exact command:

| Batch | Items | Content |
|---|---|---|
| 1 | 2 | Image readings (every cell beside its crop) |
| 2 | 19 | Disqualifier rows |
| 3 | 37 | Amendment ops |
| 4 | 3 | STALE-row proposals |
| 5–9 | 183 | Remaining rows |

### Live commands

- **`show VOL-I-8.6-01`:** source pages with crops, the amendment chain, annotations, status at each stage and A5 activities (also as HTML).
- **`diff`:** requirements new, out and changed; STALE rows and voided decisions; image-read values changed; A3 changes; programme impact.

### Coverage gaps closed

| Check | What it does | Real pack |
|---|---|---|
| **C12** | Row ids never disappear (`curation/register/ids.yaml`) | — |
| **C30** | Every date or period phrase is planned or explicitly treated. Unsupported periods use the `unresolved` kind and stay visible, never computed | 46 phrases, none uncovered |
| **C32** | Counting conventions the pack does not state are reported | 5 rules |

**Months and weeks:** these are now exact units. VOL-V ramp-up and scheduled PCOD were held as years and are now months, as printed.

## 3. Blind rehearsal (`rehearsals/blind-01/COMPARISON.md`)

**Setup:** an independent agent wrote Addendum No. 3 (3 pages) from the sources and the brief only. Its answer key was frozen by hash in `53ad76f` before the start, and opened only after the blind outputs were on disk.

| Measure | Result |
|---|---|
| Author | 22 min; about 302,000 tokens (its own report) |
| Receipt to replanned outputs and `diff` | **12 min 13 s**, including four live fixes, each generic and tested |
| Provisions and answers | **22 hits, 4 partials, 1 miss** |
| A3 | Correct apart from two defects: the footnote-12 line kept a stale "80,000" summary, and a renumbered clause was cited by its old number. Nothing added that should not be |
| Replanning | Envelope A copies 108 → 27, B 16 → 4; clarifications moved to 19 Nov; two new disqualifiers on A3 |
| Left for a person | 28 rows STALE (most anchored on the moved PDD) |

**The miss** was the renumbering of clause 8.2.

**Fixed after scoring** (not counted): renumbering ("VOL-I 10.6 (issued as 10.5)"), out-of-date summaries flagged, clarification pointers on A3 lines.

**Limits:**

- The brief told the author which **kinds** of change to include, so the curator knew the categories but not the content.
- The curator was the assistant, so your review time is extra.
- The A3 page fitted at scale 0.904, against a floor of 0.9. A larger addendum would use the condensation steps, which are built and tested on synthetic data.

## 4. Decisions needed from you (in priority order)

1. **Image readings, batch 1.** Approve or correct Table 2-4 and Form 4-C:
   `tenderpack approve VOL-II-p3-r1 --reviewer "Your Name"` (and `VOL-IV-p6-r1`).
2. **Disqualifiers, batch 2 (19 rows), and amendment ops, batch 3 (37).** Run `accept` or `reject` (with a note) on each. These are the items that put a bid out.
3. **The three STALE-row proposals, batch 4.** Apply them and accept, or reject them with a note.
4. **LCC certificate:** lead time and issuer. It is the main infeasibility:
   - at the provisional 30 WD, the certificate chain is 7 WD short and the ratio chain 12 WD short;
   - feasible at 23 WD or less for the certificate, and 18 WD or less with the ratio calculation;
   - the latest start dates have already passed at the 22 Oct status date.
5. **Legal calls before the 12 Nov clarification cut-off:**
   - the Form 4-C "exclusion" category;
   - what to print and sign on Form 4-A;
   - Envelope B contents;
   - prices in Envelope A;
   - the concession term;
   - the Volume III / Drawing 03-C-114 gap.
6. **A5 assumptions:** consortium size (3), copy counting, the other lead times and capacities.
7. **The remaining 183 rows (batches 5–9):** who reviews which, by owner role.
8. **Repository history.** The archive's `repository.bundle` carries the full history. Checkpoint `6a5d6cb` still holds your session 05 message as first recorded, which named a model; it was redacted in the next commit. Say if you want that rewritten (a force-push) before a final archive. Otherwise it stays as it is.
9. **Generated outputs in git (D7).** Keep committing `out/`, the drills and the rehearsal outputs, or commit only sources and curation and rebuild.

## 5. Draft archive

**Build:** `python scripts/make_draft_archive.py DEST [--wheels WHEELHOUSE]` builds from a clean commit:

- `LAMAR-PPP-R2-DRAFT_<sha>.zip`, organised as `A1_compliance_register/`, `A2_…`, `A3_…`, `A4_work_log/` (work logs, plan, reports, `repository.bundle` with the full history), `A5_programme/`, `REVIEW/`, `REHEARSALS/blind-01/`, the three guides and `SHA256SUMS`;
- optionally, a macOS wheelhouse for an offline Python setup (Apple silicon and Intel; CPython 3.11–3.13).

**Verification:** recorded in the work log, §7. Where it could not be tested (on a Mac), the exact commands are in `docs/VERIFY_ON_MAC.md`.

## 6. Remaining gaps

- **Interpretations are unreviewed.** Nothing establishes that an interpretation, owner, lead time or disposition is right; passing tests are not a review. The register was drafted at scale by subagents, and its quality is that of your review.
- **C28 is not built** (cover-summary cross-check); the blind cover was scored partial for this.
- **A live addendum leaves many rows STALE** (28 in the rehearsal). A person's time on them is the bottleneck of the live session, not the tool's 12 minutes.
- **No Mac run.** The commands are given.
- **Deferred, as directed:** the Claude Code app, OpenRouter and Ollama integrations. The tool runs offline with no model.
