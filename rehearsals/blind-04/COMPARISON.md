# Blind rehearsal 04: the workflow's candidate against the sealed answer key

## How the rehearsal ran

- **The addendum.** An independent subagent wrote it from the pack's PDFs, the brief and the correspondence only (`FROZEN.md`, `SEALED/author_notes.md`); it did not read the tool. Its subjects: a definition changed and used in several volumes (Estimated Project Cost), two values turned into formulas on that definition (the net-worth test, the delay liquidated damages), a velocity ceiling lowered (the cover says "relaxes"), an amendment of an earlier addendum's amending text with a retroactive effective date, a reissued evaluation table whose replaced Notes hide a weighting change and a re-based threshold, a clause split in two with changed content, a conditional amendment that is not in effect, a new Arabic image-only form (Form 4-H) with an English translation that misstates its threshold (25 % for 10 %), a referenced Appendix C that is not supplied, and a genuine ambiguity (how a test that depends on an Envelope B figure is passed at the Envelope A stage).
- **The freeze.** The PDF and the sealed `SHA256SUMS` were frozen by hash in `FROZEN.md` on 4 Oct 2026 at 14:12:18 UTC, before the addendum was opened.
- **The processing agent.** Nobody curated. `tenderpack ai run ADD-03 --pdf … --route host --host-model-alias opus` did everything: the candidate workspace, ingest, the reading of the image region, the analysis in batches, validation, the downstream phase, promotion into the candidate, pin, check-register, outputs, diff and the review packet. Each batch was a headless host session (`claude -p`, built-in tools off, only the MCP tools, the CLI's `opus` alias, reported as Opus 5.5) which could not reach the sealed key. The coordinator (Fable 5.1) opened nothing but the clock and the run's summary line until the freeze.
- **What is scored.** Only the first candidate outputs, frozen at 16:41 UTC (`FROZEN-OUTPUTS.md`, hashes over the run folder) and copied here: `out-candidate/`, `review/`, `proposals/`, `candidate-curation/`, `checkpoint.json`. The post-key resume and fixes (§"After the key") are labelled and not scored.
- **Unsealing.** 16:42 UTC, after the freeze: all four hashes matched (`sha256sum -c SEALED/SHA256SUMS`; the PDF line from the root; the hash of `SEALED/SHA256SUMS` equals `FROZEN.md`'s).
- **Nothing is decided.** Every op, disposition and reading is PROPOSED in the candidate; nothing was accepted, approved or sent; the real `curation/`, `config/` and `out/` were only read.

## Timeline (UTC, from `clock.txt` and `checkpoint.json`)

| Step | Start | End | Elapsed |
|---|---|---|---|
| **Attempt 1**: ingest refused the candidate (C05: the page-4 image region had no reading; the workflow had no step to read a new image region) | 15:05:08 | 15:05:26 | 0:18 |
| **Live fix** (pre-key, W3): a `readings` step for unread image regions, with regressions on a synthetic image | 15:07 | 15:24 | 17 min |
| **Attempt 2**, ingest (candidate workspace, 5 pages, 70 provisions) | 15:25:05 | | 0:19 |
| Reading of the image region `ADD-03-p4-r1` by one host session (checked by `check_reading`, written pending, ingest re-run) | | | 3:51 |
| Analysis: 10 batches of up to 8 provisions; 7 host sessions of 185–458 s; batches 8 and 9 failed at once (the host plan answered HTTP 429, rate limited); batch 10 skipped (already covered) | | | 38:59 |
| Validation; downstream (5 batches: every host session failed in 2 s, the same rate limit); promotion into the candidate; pin; check-register (exit 1: 8 C46 findings, obligations without rows); outputs (exit 0, PARTIAL); diff; review | | 16:10:40 | 2:21 |
| **Total, PDF to candidate outputs and review packet** | 15:25:05 | 16:10:40 | **45:35** |
| Freeze; unseal | 16:41 | 16:42 | |
| Post-key resume (not scored) | 16:50 | | |

**Against the 30-minute target:** missed. The host sessions themselves (39 minutes for 7 batches, 3–8 minutes each, on the Opus alias) are the cost; everything deterministic took under three minutes. The two rate-limit failures cost nothing in time but left 13 provisions unanalysed and the whole downstream phase empty.

## Results (pre-key candidate only)

**Count:** 35 provisions, answers, cover errors, the Arabic image and secondary effects: **19 hits, 10 partial, 6 missed.** Of 9 derived dates: 3 right, 1 partial, 5 not computed. Of the A3 changes the key expects: none applied (the addendum is PARTIAL in the candidate, and the downstream phase produced no rows), 4 flagged as unresolved. All 19 "must not report" traps avoided (one row shows a false CHANGED signal from a confirming answer, noted below).

### Body provisions

| Key | Expected | Result | Evidence in the candidate |
|---|---|---|---|
| 1.1, 1.2 | recitals, no effect | **hit** | `no_effect` dispositions with reasons that quote the provision and VOL-I 3.2(a) |
| 2.1 | VOL-V 1.3 definition replaced | **hit** | `replace_text` with the exact old and new words |
| 2.2 | applies wherever the expression is used; the reader finds the uses | **hit** | `annotate interprets` naming VOL-I 8.4 as amended, VOL-V 18.1/18.4 and Form 4-F |
| 3.1 | 8.4(a) = 25 % of the EPC; limb (b) unchanged; no sanction stated; do not call it relaxed or tightened | **hit** | exact `replace_text`; nothing stated about direction. The rows VOL-I-8.4-01/02 are STALE (changed, not re-read): the downstream phase that re-makes readings failed |
| 4.1 | LD = 0.05 % of the EPC per day | **hit** | exact `replace_text`. The 200-day cap (IE3) was not computed |
| 5.1 | velocity 2.0 → 1.5 m/s, a tightening | **hit** | exact `replace_text`; see E1 for the cover |
| 5.2 | an amendment of ADD-01 5.1 with effect from 8 Oct 2026; the chain VOL-II 5.3 ← ADD-01 5.1 ← ADD-03 5.2 | **partial** | escalated as an unknown change type, with the evidence and the effective date ("the engine reports the same…"): not applied, left for a person, as the owner's rule requires for unknown types |
| 6.1 | Table 1-1 reissued: criterion G, total 120; the replaced Notes hide 70/30 and a 70 %-of-120 threshold; Appendix C | **missed** (the table); the Notes partly hit | the natural `replace_unit ADD-02:T1-1-rev → ADD-03:T1-1` failed C22 in the proposer's simulation — a tool gap: a table issued by an earlier addendum is not resolved as a citation target (the same class as blind-03's Form 4-G, fixed then for forms only). Note (2)'s weighting change **was** caught and applied (`ADD-03/S6/para1(b)`: VOL-I 11.2 65/35 → 70/30, old words located in the target); Note (3) confirmed; Note (1)'s 84-mark threshold not computed; Note (4)'s Appendix C flagged through Q17 |
| 6.2 | 11.3 replaced (70 % of total marks); 11.3A inserted (Envelope B retained until after the PBN); no renumbering | **hit** | `replace_text` on VOL-I 11.3 and `insert_unit` 11.3A after it, both verbatim |
| 7 | conditional; not in effect; VOL-II 1.4 unchanged; a decision milestone on Thu 12 Nov 2026 | **partial** | 7.1 `insufficient_evidence` ("whether the Authority will give the notice"), 7.2 escalated with the deletion quoted and "only where this Section has effect": VOL-II 1.4 correctly not amended; no milestone or dual-scenario note |
| 8.1 | Form 4-H added to Volume IV and after Form 4-G in the 9.1 list | **hit** | `insert_unit` anchored on VOL-I 9.1 after Form 4-G, text from the addendum's own Form 4-H group |
| 8.2 | Arabic governs; the translation's 25 % does not | **partial** | the discrepancy was found (the proposer declared the conflict "Arabic Form 4-H threshold ١٠٪ vs English Appendix B 25 %") but left unresolved instead of applying the stated rule; 25 % was never adopted |
| 8.3 | Envelope A at the PDD; a foreign-incorporated member may use the Portal by Thu 3 Dec 2026 (or 2 Dec if stated) | **partial** | `insufficient_evidence`: the forward-counting convention declared missing ("2 or 3 December"); the per-member split recognised; no date planned |
| 8.4 | failure → non-responsive | **hit** | `annotate adds_obligation` quoting the consequence; no row carries it yet (C46 reports it) |

### Clarification answers

| Key | Expected | Result | Evidence |
|---|---|---|---|
| Q15 | decoy: restates 8.7 and Form 4-D; no change | **hit** | `confirms`; no new row; Form 4-D not amended (the diff still marks VOL-IV-F4D-01 CHANGED because the annotation adds a dependency — a false signal, see traps) |
| Q16 | confirming; grid point outside the EPC unless Section 7 triggers | **hit** | `interprets` on VOL-II 1.4 and Form 4-F |
| Q17 | Appendix C referenced, not supplied; no invented value | **hit** (detection) | `insufficient_evidence`: "Appendix C to ADD-03 … is not in the evidence"; left unresolved rather than entered as a missing-document item |
| Q18 | the 1.5 m/s ceiling applies at the crossings | **hit** | `interprets` on VOL-II 5.2 and 5.4 |
| Q19 | non-answer; ambiguity A1 stays open | **partial** | `effect: none`, "Open issue" in the note; no issue or A3 "could not resolve" entry (the downstream phase failed) |
| Q20 | no legalisation | **hit** | `interprets` on the third declaration and the translation; no activity added |

### The cover's planted errors

| Key | Mechanism | Result | Evidence |
|---|---|---|---|
| E1 | "relaxes the velocity limit" — a direction reversal | **missed** | the op itself is right (1.5 m/s), but nothing flags the cover: C28 does not know the verb "relaxes" (nor "divides", "makes"), so the whole compound sentence came out "not found" and 5.1 was reported "omitted" instead — a second tool gap; a direction judgement would need the model, and the proposer did not raise it |
| E2 | the reissued Notes hide 70/30 and the 84-mark threshold | **partial** | the weighting change was caught and applied as an op; the threshold re-basing and the missing Appendix C were not connected to the cover |
| E3 | "all Bidders may submit through the Portal after the PDD" | **hit** | the proposer declared a conflict between the cover and 8.3 (the relief is per member, foreign-incorporated only) and left the cover paragraph unresolved for a person |

### The Arabic image (Form 4-H)

**hit.** The host session read the native image and the band crops over MCP and proposed a reading that `check_reading` accepted: every Arabic line verbatim (the title, the preamble, the three declarations, the table header, the field labels, the note "عدم تقديمه كاملاً يجعل العرض غير مستجيب"), diacritics present, translations kept apart as non-evidence, the threshold recorded as "عشرة في المائة (١٠٪)" with the numeral checked, the two uncertainties stated (a possibly undotted letter; the table read as blocks because no vertical rules were measured). Status `interpretation_pending`, written pending, never approved. The field labels and the note of the image were then left unresolved only because their analysis batch hit the rate limit.

### Secondary, undisclosed effects

| Key | Expected | Result |
|---|---|---|
| S1 | DN1200 no longer sufficient (→ DN1400), crossings, surge | **missed** (no calculation; no relationship from VOL-II 5.2 to 5.3/5.4/4.5 exists in the curated file) |
| S2 | combined weighting 70/30 | **hit** |
| S3 | threshold 84 of 120 | **missed** |
| S4 | Envelope B retained until after the PBN | **hit** |
| S5 | the second declaration is stricter than 8.2 | **partial** (the declaration read and kept; its implication not drawn) |
| S6 | certified register issued 27 Oct–25 Nov | **partial** (the declaration read; the window not computed) |
| S7 | the 165-day window between the LD cap and termination | **missed** |
| S8 | the Form 4-F EPC row carries the exclusions and drives LD/8.4(a) | **partial** (Q16's annotation reaches Form 4-F; VOL-IV-F4F-01 shows CHANGED) |
| S9 | anything raising the EPC raises LD, cap and 8.4(a) | **missed** |
| S10 | a new deliverable in a missing Appendix C | **partial** (flagged through Q17; no activity) |
| S11 | Envelope A order; the Index of Forms not amended | **hit** |

### Dates

Right: the PDD (unchanged), the clarification cut-off (unchanged), the planning date. Partial: the retroactive effective date (noted in the escalation). Not computed: the Section 7 trigger deadline, the Form 4-H Portal date, the register window, the LD cap in days, the 84-mark threshold.

### A3

Nothing entered or left A3 in the candidate: the addendum is PARTIAL there (24 provisions unresolved) and the downstream phase that writes rows produced nothing, so the Form 4-H row and the threshold row the key expects do not exist (check-register's 8 C46 findings say exactly that: 4.1, 6.2(b), 8.1, 8.4 create obligations no row holds). The 8.4(a) row is STALE. The unresolved items A1 (Q19), Appendix C and Section 7 are visible in the review packet's "unresolved" list, not on A3.

### Traps

None of the 19 reported: no PDD change; VOL-II 1.4 not amended; no PCG change from Q15; no legalisation; 25 % never adopted; the Portal route not generalised; no "relaxed/tightened"; the minutes not cited; no renumbering; ADD-01 5.1 not deleted; no DN1400 text; the index untouched; nothing invented for Appendix C; A1 not resolved; the Arabic not replaced by its translation; no blind-01/02/03 subject. One false signal: the diff marks VOL-IV-F4D-01/02 and VOL-I-8.7-01 CHANGED because a confirming answer (Q15) annotated their units — a confirmation should not read as a change (follow-up).

### Ambiguities

A1 (8.4(a) at the Envelope A stage): noted as an open issue on Q19, not entered as a "could not resolve" item (partial). A2 (forward counting): declared as missing information with both dates (partial). A3–A5: not addressed. A6 (the retroactive date): noted.

## What the workflow did and did not do, honestly

- **Did:** opened a disposable candidate, read an Arabic image with a host session and wrote a checkable pending reading, analysed 57 of 70 provisions, proposed 16 ops and 29 dispositions that the controller verified against the evidence (every quotation verbatim; 0 invalid among the promoted), escalated the unknown change types (an amendment of an amendment with a retroactive date; a conditional amendment) and the conflicts (the cover vs 8.3; the Arabic vs the translation), promoted into the candidate only, published candidate outputs with banners, and wrote the review packet with every provision's chain. No manual intervention: every session is listed as automatic.
- **Did not:** apply the reissued table (a tool gap), compute any derived date or quantity (the 84 marks, the 200 days, the DN1400, the 3 Dec and 12 Nov dates), produce any downstream item (rows, readings, issues, clarification items, activities, dependencies: the five downstream host sessions died on the host plan's rate limit within seconds), flag E1, or meet the 30-minute target.
- **Compared with blind-03** (a curator writing the downstream by hand: 31/3/0 of 34 in 50 minutes), the automatic workflow scored 19/10/6 of 35 in 46 minutes with no human effort before review, and its weak spots are now specific: the downstream phase, derived calculations, and two citation/verb gaps.

**Human review time** for this candidate, estimated and untested: the 40-item review packet against its evidence, the 16 ops and 29 dispositions, the pending reading beside its crops, and the 24 unresolved provisions that a person must now write: about 2–3 hours before any legal or commercial call — the unresolved provisions are the larger part.

## After the key (not scored)

1. **A plain `ai resume`** (16:43–17:14, no code change) re-asked the seven rate-limited batches. Analysis batches 8 and 9 answered (8 and 6 items); the combined set then covered **70 of 70 provisions** (resolution: 7 resolved, 63 pending, 0 invalid, 0 unaccounted). The five downstream batches ran (22 minutes) and proposed **57 items**: 23 row readings, 12 escalations, 8 activities, 6 clarification items, 5 issues, 2 dependencies, 1 new row; the controller rated 34 `interpretation_pending`, 9 `escalated`, 8 `insufficient_evidence`, 5 `conflicting`, 1 `invalid`. They were promoted into the candidate, pinned and checked — and **the candidate outputs build was refused at pre-flight** (C16: the new row `ADD-03-4.1-01` cites only `VOL-V:18.1`, a unit that exists from BASE, with an interpretation at ADD-03 only, so the register treats it as active from BASE and finds no interpretation there). The design held: the run ended `partial` with `out-before/` as the last validated state, and the review packet says why. The lesson is a downstream rule: a `row_new` must cite the addendum's provision as its first unit (the curator's convention in blind-03) so the row starts at that stage — follow-up 8 below. Total with the resume: 76.4 min; resumption never re-asked a done provision (the checkpoint lists every batch and attempt).
2. **Two general fixes**, each with a regression that failed first (`tests/test_session10_blind04_postkey_fixes.py`): a table issued by an addendum is a citation target ("Table 1-1 (revised) … issued by Section 3 of Addendum No. 2" → `ADD-02:T1-1`, resolved to that addendum's issue `ADD-02:T1-1-rev`) and the engine's replacement-title rule reads "Table 1-1" from a suffixed id, so `replace_unit ADD-02:T1-1-rev → ADD-03:T1-1` passes C22 and applies, the old rows `superseded` by key; and C28 knows "relaxes", "tightens", "divides", "splits" and "makes a conditional amendment to", so the cover sentence splits into its eight claims. The real pack and the blind-02/03 after-fixes folders rebuilt after both are byte-identical to the committed ones. The scored candidate was not rebuilt with them.

## Tool follow-ups (for the plan)

1. **Tables issued by an addendum as citation targets** (`citations.resolve`, kind `table`): `replace_unit ADD-02:T1-1-rev → ADD-03:T1-1` must pass C22 when the provision names "Table 1-1 (revised) … issued by Section 3 of Addendum No. 2".
2. **C28's verb list**: "relaxes", "tightens", "divides", "splits", "makes a conditional amendment" and "adds … which" are not claim verbs, so a compound cover sentence falls through as "not found" and every op is reported "omitted". A direction-reversal claim ("relaxes" on a lowered ceiling) also needs the model's judgement: a critic prompt on cover claims about direction.
3. **Derived quantities**: a `calculate` purpose for a value expressed as a percentage or formula of another figure (the net-worth test, the LD rate, the cap in days, the threshold as a percentage of a total), so proposals carry the computed value with its inputs fingerprint.
4. **Rate-limit handling**: a 429 from the host should back off and retry within the run (bounded), not fail the batch; the resume path already re-asks failed batches.
5. **Downstream on the host route**: the downstream sessions read the final message; after the rate limit the message was an error. The step must distinguish a provider failure (retry later) from a malformed answer (ask again with the schema).
6. **A confirming answer is not a change**: `diff` and the STALE logic should not mark a row CHANGED/STALE for a `confirms` annotation that adds a dependency.
7. **Conditional amendments**: a `conditional` op effect with the trigger, the deadline and the two states, so A5 can plan a decision milestone.
8. **A new row starts at its addendum**: `downstream` must require (or set) the addendum's provision as a `row_new`'s first unit, and the register could read a row's first stage from the stage its interpretations begin at; otherwise a row that cites only a volume unit is active from BASE and C16 refuses the build.
