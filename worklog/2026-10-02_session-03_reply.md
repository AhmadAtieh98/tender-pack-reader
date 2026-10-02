# Session 03: assistant reply (verbatim)

The chat reply delivered at the end of session 03 (2 Oct 2026, about 01:15 UTC / 04:15 Riyadh). It was written to this file before being sent, and sent unchanged.

~~~~markdown
I reproduced all six gaps on `79ef49c` before changing anything. All six are real defects in my session 02 work, and I found nothing to dispute. They're fixed, tested, and pushed as `35ea0dd` on `claude/hopeful-curie-7oki9q`. I stopped before Stage 2, and **nothing is approved**: `curation/approvals.yaml` doesn't exist.

**What was wrong, and what changed** (full table in `docs/session-03_before-after.md`)
1. **Boundaries.**
   - Any line starting "5. " opened a numbered paragraph. Now the number must be in sequence, and the line must not continue an unfinished sentence: one with no closing punctuation, where the previous line ran out of room.
   - Tables were merged across pages on column count alone. Now a table continues only if nothing came between the two parts, the column edges match, and any header repeats the earlier one.
   - §3.3 is whole again. It is the **only unit that changed** in the real pack (525 → 524 units). Form 4-A/4-D numbering and the three genuine split tables still work.
2. **Structural errors.** Duplicate IDs and doubly anchored spans used to pass with exit 0, and my old trace test compared four letters. New checks C07–C10:
   - C07: unique IDs;
   - C08: each span in exactly one anchor;
   - C09: no segmentation problems;
   - C10: each unit's whole text compared with its spans re-extracted from the PDF (482 units).
   Any failure exits 2 and keeps the previous build. Pending review is separate: exit 0 with "PENDING HUMAN REVIEW", or exit 3 with `--require-approved`.
3. **Approvals.** An approval used to survive a replaced image, an added uncertainty and a moved bbox, and needed no reviewer. It now pins the whole reading (including every uncertainty) plus its evidence: source PDF, region position and native image. It counts only with a named reviewer; `approve` refuses placeholders and readings that fail checks.
4. **Table readings.**
   - RD8 now requires every cell, unique keys, and blanks written explicitly (`""` and listed in `blank`). Deleting TN's unit and basis fails it.
   - `parse_limit` is gone. Cells record only the numbers they show (single or range); the headings, qualifier and notes travel beside them with `interpretation: null` for you to fill.
5. **Drawings.**
   - A straight-line triangle and a dark box with no text are now regions for review.
   - The fixture now has a **right-to-left Arabic image table**: Arabic headings, "45 dB(A)", ٢٢:٠٠-٠٦:٠٠, ٦٫٠ - ٩٫٠, ١٢, and a declared blank. It runs through reading, validation, right-to-left rendering and the packet.
   - Cell positions and glyph orders are checked against what the fixture actually drew, not just against my reasoning.
6. **Output safety.**
   - Old behaviour: `--out` pointing at the repository deleted it, in a disposable copy, before failing; a failed rebuild deleted the previous results.
   - Now dangerous paths are refused. Builds go to a temporary sibling and are swapped in only on success; a structural failure goes to `<out>.failed`.
   - All of this was tested only in disposable directories.

**Tests actually run**
- **Failing first** (34 tests, written before any fix): 28 failed, 2 errors, 4 passed. Of the 4 passes:
  - two are guards that must pass;
  - one is the "nothing approved" guard;
  - one passed **for the wrong reason**: argparse rejected the then-unknown `--approvals` option.
- **Now:** 79 passed. That is 39 existing tests (3 adapted to the new APIs) plus 40 regression tests; 6 of those were added while fixing and are marked as such.
- **Mutations:** 11 deliberate breaks of the fixes. 10 were caught. The C10 one survived until I tightened its tests.
- `make verify`: the two rebuilds are byte-identical.

**What the checks prove:**
- each span is used exactly once;
- unit text matches its source spans;
- each reading points at the right image;
- tables have every cell, with blanks declared;
- every text band is read;
- declared numerals render in the order the crop shows.

**What they don't prove:** that any word, mark, digit or value is right, that a translation is right, or what a value means. That's your review.

**Decisions I need from you** (open `build/review/*/packet.html`: every heading, cell and line sits beside its native crop)
1. **Form 4-C, declaration 5:** is the digit ٢ (VOL-I §4.2) or ٣ (§4.3)?
2. **Form 4-C marks:** check the tanween and hamza on the native crops.
3. **Declaration 4:** is "exclusion of the proposal" right for استبعاد العرض? Which pack category it maps to is your call.
4. **Table 2-4 cells:** check each one against its crop, especially the 2.2 decimal point and the "-" read as "no unit" for pH.
5. **Table 2-4 meaning:** the chlorine and pH ranges sit under "all values are maxima". What do they mean?
6. **Note 1** touches the image edge: accept it, or record possible cropping.
7. **Approve or correct.** Approve each reading yourself (`python -m tenderpack approve <region> --reviewer "Your Name"`), or send me corrections.
8. **Stage 1 and open decisions:** accept Stage 1 or not; D3 (A1 granularity), D4 (counting conventions), D7 (keep committing `build/`?).

**Plan:** `docs/PLAN.md` is now one consistent revision 3. It keeps A1 in Excel, configurable bidder assumptions (three members by default) and the later Claude Code / OpenRouter / Ollama routes. Integrations and model selection are deferred.

**My errors this session** (all in `worklog/2026-10-02_session-03_review-fixes.md`):
- I expected "45 dB(A)" to display unchanged in an RTL cell. It displays "(dB(A 45".
- My first RTL test table came out left to right.
- My new drawing rule briefly turned thin border bars into regions. The real pack couldn't catch this; I fixed it and added a test.
- My first reproduction of 2b was vacuous: it injected nothing. I corrected it and re-ran it against `79ef49c`.
- A mutation survived until I tightened the tests.

Your messages, and what happened when the session hit its usage limits, are recorded verbatim in that log.
~~~~
