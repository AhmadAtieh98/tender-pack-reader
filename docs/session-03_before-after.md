# Session 03: before / after on the six Stage 1 review gaps

Your review raised six gaps. All six were **reproduced on commit `79ef49c`** and are **confirmed defects of mine**; I found no point to dispute. Regression tests were written first and seen failing (28 failed, 2 errors, 4 passed: two are guards that must keep passing, one is the "nothing approved" guard, and one passed for the wrong reason, see the log). Then the fixes went in. Full record: `worklog/2026-10-02_session-03_review-fixes.md`.

| # | Before (reproduced on 79ef49c) | After |
|---|---|---|
| 1a | VOL-I §3.3 ended "…under Section"; "5. A Bidder that resolves…" became a separate unit `VOL-I:S3/item5`. | A line starting "N. " opens a numbered paragraph only if N is in sequence and the line does not continue an unfinished sentence. "Unfinished" means the previous line had no closing punctuation and wrapped: the next word would not have fitted at its end. §3.3 is whole again. Form 4-A items 1–6 and 4-D items 1–3 still split. **The only unit change in the real pack:** 525 → 524 units. |
| 1b | Two unrelated tables on consecutive pages, with a heading and text between them, were merged into one table because their columns matched. | A table continues the previous one only if nothing came between them, it is first on the next page, its column edges match, and any header repeats the earlier header. Genuine splits still join (Table 2-6, ADD-01 Q&A, synthetic). |
| 2 | Duplicate clause IDs were renamed `~2`. A span listed in two units' anchors was only noted as a "problem". In both cases every check passed and the exit code was 0. The trace test compared four letters of the first word. | New checks: **C07** unique IDs; **C08** each span in exactly one anchor; **C09** no segmentation problems; **C10** each unit's whole printed and matching text equals its spans re-extracted from the PDF (482 units in the real pack). Any failure is a **STRUCTURAL FAILURE: exit 2**, and the previous build is kept. Pending review is separate: exit 0 with "PENDING HUMAN REVIEW", or exit 3 with `--require-approved`. |
| 3 | An approval with no reviewer counted. It stayed valid after the image changed and its hash was updated, after an uncertainty was added, and after the bbox moved. | An approval pins a **review subject**: the whole reading (content, every uncertainty, source claims, preparer, method) plus the evidence (source PDF hash, region page, bbox and kind, native image hash). It counts only with a named reviewer; `<name>`, blank or none is refused. `approve` re-detects the region and refuses readings that fail their checks. **Nothing has been approved; `curation/approvals.yaml` does not exist.** |
| 4 | Deleting TN's unit and basis cells, and duplicating a row key, passed validation. `parse_limit("10")` returned "max 10". | **RD8:** unique keys, exactly one cell per column, and blanks written as `""` and listed in `blank`. `parse_limit` is gone: `numeric_reading` records only the numbers a cell shows (`single` / `range`). The headings, qualifier and notes travel beside them, with `interpretation: null` left for you. |
| 5 | A triangle drawn with straight lines, and a black box with no text, produced no region. The bilingual fixture was never read. | Only axis-aligned rules, light, stroked or thin boxes, and dark bands carrying text count as structure. Diagonals, curves and dark boxes with no text are regions for review (**RD9**: a graphic needs a description). The fixture now holds a **right-to-left Arabic image table**, with Arabic headings, Latin and Arabic-Indic numerals, a time range, a decimal range and a declared blank. It goes through reading, RD3/RD6/RD8 checks, RTL rendering and the packet. Each cell's crop and position were checked against what the fixture actually drew. |
| 6 | `--out` pointing at the repository raised an error *after* deleting it (in a disposable copy). A failed rebuild deleted the previous results. | Output paths are refused if they are the repository or a parent of it, home, `/`, a protected folder, an input, or an existing folder that is not a previous build. Builds go into a temporary sibling and are swapped in only on success. A structural failure goes to `<out>.failed`. Tested only in disposable directories. |

**Tests:** 79 passed: the 39 existing tests (3 adjusted to the new APIs) and 40 regression tests. Of the 40, 34 were written before the fixes; 6 were added while fixing and are marked as such. In 11 deliberate mutations, 10 were caught at once. The full-evidence check (C10) mutation survived until the tests were tightened; it is now caught. `make verify`: the two rebuilds are byte-identical.

**What the checks prove:**
- Every span is accounted for once.
- Units match their source text in full.
- Readings point at the right image.
- Tables have every cell, with blanks declared.
- Every text band is read.
- Arabic is stored in logical order, and declared numerals render in the order the crop shows.

**What they do not prove:** that any word, mark, digit or value is right, that a translation is right, or what a value means. Passing tests are not correct interpretation, and they are not approval.

## Decisions I need from you (packets: `build/review/*/packet.html`)

1. **Form 4-C, declaration 5:** is the second digit ٢ (VOL-I §4.2, blackout) or ٣ (§4.3)? The order is settled; the identity is not.
2. **Form 4-C marks:** confirm the tanween and hamza forms on the native crops.
3. **Form 4-C, declaration 4:** is "exclusion of the proposal" right for استبعاد العرض? Which pack category it falls under (rejection, disqualification or non-responsiveness) is a legal call for you.
4. **Table 2-4 cells:** check each cell against its crop, especially the decimal point in 2.2 and the "-" read as "no unit" for pH.
5. **Table 2-4 meaning:** the chlorine and pH ranges sit under "all values are maxima". What they mean is your call.
6. **Table 2-4 Note 1** touches the image edge (RD7). Accept it, or record possible cropping.
7. **Approve or correct.** Approve each reading yourself with `python -m tenderpack approve <region> --reviewer "Your Name"`, or send me corrections.
8. **Stage 1:** accept it or not. Also D3 (A1 granularity), D4 (counting conventions) and D7 (keep committing `build/`?).

Stopped before Stage 2.
