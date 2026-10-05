# Subagent brief 15: Author sealed unseen Addendum No. 3

Launched 2026-10-03 20:05:50 UTC; model option requested: `(default)`; subagent type: `general-purpose`.
The text below is the prompt exactly as sent by the coordinator (exported from the session transcript on 4 Oct 2026, session 11).

---

You are the independent author of a BLIND rehearsal input for a tender-reading tool. The tender is FICTIONAL (an internal assessment pack; confidential: do not publish, upload, search the web or send anything). Another engineer will run the tool on your addendum without seeing your answer key, then compare. Your independence matters: do NOT read the tool's implementation or its curated data.

## You MAY read (repository /home/user/tender-pack-reader)
- `sources/candidate_pack/*.pdf`: the tender volumes VOL-I, VOL-II, VOL-IV, VOL-V and the real addenda ADD-01 (issued 8 Oct 2026) and ADD-02 (issued 22 Oct 2026). Study ADD-01 and ADD-02 closely: page size, fonts, header/footer furniture (exact text and position), cover lines ("Issued ...", "Tender NUPA/ISTP/2026/014", the cover summary paragraph beginning "This Addendum ..."), section headings, numbered provisions, the clarification Q&A layout, reissued tables/forms and appendices. Use PyMuPDF (`.venv/bin/python -c "import pymupdf"`) to inspect text, fonts and positions.
- `sources/brief/*.pdf` (the assignment brief).
- `rehearsals/blind-01/input/ADD-03_Addendum_No_3.pdf`: a previous blind Addendum No. 3. Read it only so that yours is DIFFERENT (different clauses, different kinds of change). You may read `rehearsals/blind-01/SEALED/build_addendum.py` purely as a technique example for drawing a PDF with PyMuPDF.
## You must NOT read
`tenderpack/`, `tests/`, `curation/`, `config/`, `build/`, `out*/`, `docs/`, `worklog/`, `scripts/`, or anything under `rehearsals/` other than the two files named above.

## Write an "Addendum No. 3" (unseen style)
- Same tender (NUPA/ISTP/2026/014), issued on a date after 22 Oct 2026 and before the clarification cut-off (pick one, e.g. early November 2026, a Sunday-Thursday), in the visual style and furniture of ADD-01/ADD-02, text layer only (no images), 2-4 pages.
- Content: a realistic mix a real Authority might issue, including several of these (choose and vary): a change to a figure or a period in a VOL-I or VOL-II clause; a change to a table cell or a reissued table (with notes that themselves change something); deletion of a requirement; a new obligation with a stated consequence; a change that moves a date the bid programme depends on (e.g. the Proposal Due Date or a submission detail), or that changes copy/packaging quantities; an answer in a clarification table that changes or withdraws an earlier answer from ADD-01/ADD-02; a renumbering or cross-reference correction; something in an appendix or a note rather than a numbered clause. Make the cover summary paragraph ("This Addendum ...") realistic but INCOMPLETE or slightly misleading in one or two places (as real covers are).
- Keep it internally consistent and plausible against the volumes (cite real clause numbers that exist). Do not copy blind-01's changes.

## Outputs
1. The addendum PDF: `rehearsals/blind-02/input/ADD-03_Addendum_No_3.pdf` (create the directories). Nothing else under rehearsals/blind-02/.
2. Sealed material (NOT in the repository): directory `/tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s08/blind02-sealed/` containing:
   - `build_addendum.py` (the script that draws the PDF, deterministic),
   - `expected_findings.yaml`: for EVERY provision, what a correct reader should conclude: the target clause/table/form, the kind of change (amend text / set table value / delete / reinstate / replace table or form / insert / answer with or without effect / renumber), the new words or values, any new obligation and its stated consequence (quoted), any date that moves and the expected new date, effects on copies/packaging/deliverables, and the cover-summary errors (omissions/contradictions) you planted;
   - `author_notes.md` (your reasoning, the traps, anything ambiguous on purpose),
   - `SHA256SUMS` over the three files above and the PDF (sha256sum format, relative names).
3. Reply with ONLY: the PDF path, its sha256, its page count, the issue date printed on it, and the sha256 of the SHA256SUMS file. Do NOT describe the addendum's content, its changes or the traps in your reply (the engineer must stay blind). Do not commit anything and do not mention AI model names in the PDF or files.
