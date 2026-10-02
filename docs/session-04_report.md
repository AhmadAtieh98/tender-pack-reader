# Session 04: repair evidence, Stage 2 outputs, decisions needed

Full record: `worklog/2026-10-02_session-04_repairs-and-stage2.md`. Everything below is a **draft**: interpretations and amendment ops are proposed by the assistant and **not reviewed by a person**; both image readings are **still pending your review**; nothing has been approved.

## 1. The three repairs

All three were reproduced on `574f4b3` before any change; none is disputed.

| # | Before | After |
|---|---|---|
| 1 | C10 passed `120,000` → `210,000` in a cell, text moved between columns, a changed `normalized` value, and anchors pointing at the wrong page or box with unchanged span ids. | C10 checks every cell's text in span order and in its column, rebuilds row/table text and `normalized`, and checks each anchor's real page and box and the span order across anchors. Then, after an adversarial review found about 30 more ways through: every field of every unit is compared with an independent re-segmentation of a fresh extraction, table cells with grids re-detected from the page, and units from image readings are re-derived from the reading and tied to the crop they cite. |
| 2 | The fixture drew `45 dB(A)` scrambled and RD6 passed on the digits alone. | The raw transcription stays unchanged (logical order); for display, a Latin expression in Arabic is laid out as a left-to-right island. The fixture now draws it correctly and the test compares against what was drawn. A declared visual order must hold exactly the token's characters and match a whole rendered run. Digits-only verification is labelled **PARTIAL** (RD6, C05, packets). |
| 3 | `--require-approved` swapped the new build in, then exited 3: the previous build was gone. | The gate runs before publishing: the candidate goes to `<out>.rejected` with `REJECTED.md`; the previous build is untouched; a first build with pending readings publishes nothing. Candidate siblings get the same path-safety checks; symlinks are refused. |

**Failing first:** round 1, 14 failed / 1 passed (a guard); round 2 (the adversarial reviewer's reproductions), 34 failed / 15 passed (controls), then 14 failed. **Mutations:** round 1, R1a/R1b survived until isolated tests were added; round 2, A2/A4/A6 survived until shared-bug tests were added; all caught now.

## 2. Stage 2 outputs (`out/`; drill in `out-drill/`)

| Output | Files | What to look at |
|---|---|---|
| A1 | `out/a1/a1.xlsx` (also `.csv`, `.json`) | Status after BASE / ADD-01 / ADD-02 per row; separate columns for the image-reading status, the interpretation review and the ops review; Dates sheet with every counting reading |
| A2 | `out/a2/a2.md` (tables also as CSV/JSON) | Per addendum: each op with its provision and page, rows that move and why, answers to review, non-binding minutes, every provision's disposition, evidence chains |
| A3 | `out/a3/a3.pdf` | One page: explicit consequences (quoted, Arabic kept in Arabic), §11.3 score elimination, pass/fail rows with no stated consequence, and what could not be resolved |
| A5 | `out/a5/programme.csv`, `marshalling.csv`, `replan_deltas.csv` | Activities from the A1 rows in force, with dependencies, lead times labelled as assumptions (value, basis, owner) and INFEASIBLE / DEADLINE PASSED flags |

The difficult cases, as the outputs show them:

- **LCC:** active (30%) → deleted (ADD-01 4.1) → reinstated at 35%, non-responsive (ADD-02 9.1); ADD-01 4.2 revoked by ADD-02 9.2. With the 30-WD lead-time assumption the certificate is **INFEASIBLE by 7 WD** at 22 Oct.
- **Deadlines:** PDD 12 → 26 Nov; clarification cut-off, bond and proposal validity and the footnote 12 look-back move with it, each reading shown. VOL-I 8.3 (ISO current at the PDD) is **STALE** after ADD-01.
- **Repeated wording:** ADD-02 4.1 changes VOL-II 4.4 only; VOL-V 31.3 is recorded as "same words, not targeted". VOL-V 29.2 (60/40 indexation) is untouched by the weighting change.
- **Weighting:** 60/40 → 65/35, made only in note (2) to the reissued Table 1-1; Table 1-1 B 20→15, D 15→20.
- **TN:** 5 → 3 mg/l; the old value exists only in the image reading, pending; flagged in A1, A3 and A5.
- **Form 4-G:** inserted after VOL-I 9.1(e); non-responsive if not submitted; re-lettering not stated.
- **Form 4-C:** "exclusion" (استبعاد العرض) in declaration 4 and "non-responsive" in the note, quoted in Arabic with a translation labelled as not reviewed.
- **Form 4-A:** the reissued form still prints 12 November 2026; raised, not corrected.
- **Answers:** ADD-01 Q2 is listed for review after ADD-02 changed the page limit; it stays in force. The minutes are context only.
- **Coverage:** every provision of ADD-01 (36) and ADD-02 (40) is accounted for: op, no effect (with reason), or **OUTSIDE THE SLICE** (3 and 7).

**Proved by tests** (`tests/test_stage2.py`, `tests/test_drill.py`): wrong-target rejection; dependency staleness; pending image status carried through A1, A3, A5; a partial addendum keeps the last validated state; transcription approval separate from interpretation (in a disposable copy, with "Fixture Test Reviewer"); byte-identical rebuilds; the drill. **237 tests pass.**

## 3. The ADD-03 drill (`out-drill/`)

A synthetic Addendum No. 3, laid out like Addenda 1 and 2, went through the same path with no curated op file: drafted, then applied by the same engine.

| Provision | Result |
|---|---|
| 2.1 PDD 26 Nov → 10 Dec | applied; every dependent date recomputed; six rows STALE for a person to re-read |
| 3.1 VOL-V 31.3 72 h → 48 h | applied; VOL-II 4.4 untouched |
| 4.1 delete VOL-I 8.6 | applied: LCC deleted → reinstated → deleted |
| 5.1 TP → 0.5 mg/l | applied; old value from the pending image reading, flagged |
| 6.1 "bid security period extended by thirty days" | **unresolved** (no recognisable target) |
| 7.1 VOL-II 4.4 72 h → 60 h | **rejected** (C23): those words were already replaced by ADD-02; not moved to VOL-V 31.3 |
| Q16 quotes "26 November 2026" | listed for review, not revoked; Q15 (negative control) not listed |

ADD-03 is **PARTIAL**, so A3 and the main A5 stay on ADD-02 (PDD 26 Nov); the ADD-03 column in A1 and `out-drill/a5/working/ADD-03.json` show the working state.

## 4. The hiring team's reply

Recorded as received: `sources/correspondence/2026-10-02_reply_from_hiring.eml` (body in the `.md` beside it). It confirms the approach on all six points, says Addendum 3 will be a PDF in the same format, and asks for Volume III and Drawing 03-C-114 to be flagged as referenced but not supplied, with their impact. That is now Issue `I-VOL-III` on A3: only the drawing shows the effluent main's delivery point (VOL-II 5.1), and no omission claim is accepted after the PDD (VOL-I 3.4). Delivery: by 17:00 Monday 5 October.

## 5. Decisions needed from you

1. **Stage 2 shape:** accept the op model, the row shape (D3) and the four outputs as the basis for Stage 3, or tell me what to change.
2. **Proposed vs accepted ops (plan C29):** no op has been accepted, so the slice applies proposed ops and labels them. Keep that for working outputs, or require your acceptance (per op or per addendum) first?
3. **Lead times** (`config/assumptions.yaml`): especially the LCC certificate (30 WD; the issuer is not named in the pack), which makes the LCC chain infeasible. Confirm or give values.
4. **Counting conventions (D4):** planning uses the conservative reading. Keep that, or fix per rule: day 0 or day 1 for "days from the PDD", the look-back boundary, forward counting for ADD-01 3.1.
5. **Legal calls kept with people:** the Form 4-C "exclusion" category; what to print on Form 4-A (12 vs 26 Nov) and whether to seek clarification; whether ADD-01 Q2 still applies after ADD-02 2.1.
6. **Images:** approve or correct both readings (Table 2-4, Form 4-C) yourself; the TN amendment's old value depends on them.

Stopped before Stage 3.
