# Subagent brief 12: Blind Addendum No. 3 author

Launched 2026-10-03 00:43:12 UTC; model option requested: `(default)`; subagent type: `general-purpose`.
The text below is the prompt exactly as sent by the coordinator (exported from the session transcript on 4 Oct 2026, session 11).

---

You are an independent test author. Your job is to write a realistic, fair "Addendum No. 3" to a tender pack, as the Authority's tender clerk would, and to record — sealed — what a correct reader of the pack should conclude from it. A separate system will later process your addendum WITHOUT seeing your expected findings; your findings are the answer key. Your independence is the point of the exercise.

## Strict information boundary (read this first)

You may read ONLY these files:
- `/home/user/tender-pack-reader/sources/candidate_pack/*.pdf` (the tender pack: VOL-I, VOL-II, VOL-IV, VOL-V, ADD-01, ADD-02)
- `/home/user/tender-pack-reader/sources/brief/Lamar_PPP_AI_Partner_Round2_Brief.pdf` (the assignment brief)
- `/home/user/tender-pack-reader/sources/correspondence/2026-10-02_reply_from_hiring.md` (says Addendum 3 will be "a PDF in the same format as Addenda 1 and 2")

You must NOT read, list, grep or open anything else in `/home/user/tender-pack-reader` — in particular not `tenderpack/`, `tests/`, `curation/`, `config/`, `docs/`, `worklog/`, `build/`, `out*/`, `README.md`, `Makefile`, `pyproject.toml`, git history (`git log`, `git show`), or any other directory. Do not read anything else in `/tmp/claude-0/` except your own output directory. Do not import the `tenderpack` package. If you are unsure whether a file is allowed, it is not.

Tools: Python with PyMuPDF (`import pymupdf`) is available as `/home/user/tender-pack-reader/.venv/bin/python`; use it only as a library (to inspect the PDFs and to write your PDF). Write all your files under:
`/tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/blind01/`

## What to produce

1. **`ADD-03_Addendum_No_3.pdf`** — Addendum No. 3, issued after Addendum No. 2 (ADD-02 is dated 22 October 2026) and before the Proposal Due Date then in force. It must be in **the same format as Addenda 1 and 2**: same page size, the same header/footer/watermark furniture (text, fonts, sizes, positions), the same cover block style, numbering style of sections and provisions, fonts and sizes for headings/body/bold, the clarification Q&A table style if you use one, and the issue-date line. Study ADD-01 and ADD-02 precisely with PyMuPDF (`page.get_text("dict")` for spans: font, size, flags, origin/bbox; `page.get_drawings()` for rules/boxes/table lines) and reproduce the layout faithfully; a real Addendum 3 from the same office would look like those two. Use only standard PDF base fonts or the fonts those PDFs use (check what they embed/reference). Keep it to 1–3 pages like ADD-01/02. All text must be a real text layer (no images of text).

   **Content.** 8–14 numbered provisions plus cover text, realistic for this project and consistent with the pack (check the actual clause numbers, wording, values and tables you amend — quote existing words exactly when the addendum says "X is deleted and replaced by Y"). Mix:
   - at least one date change with knock-on effects (e.g., a deadline in VOL-I), and one change to a period expressed in days/Working Days;
   - value changes in clause text, and at least one change to a cell of a text-layer table;
   - a deletion of a requirement, and an insertion of a new requirement that carries an explicit consequence (e.g., rejection / non-responsive / disqualification wording);
   - a change touching wording that appears in more than one place in the pack, where only one occurrence is meant (state precisely which);
   - a change to something that exists only in an image in the pack (e.g., a cell of Table 2-4 in VOL-II, or Form 4-C in VOL-IV) — the addendum text is still a text layer;
   - clarification Q&A: at least one answer that changes substance and one that only restates the pack;
   - at least TWO change types that Addenda 1 and 2 do not use (you decide what they are after reading ADD-01/02 — e.g., a clause renumbered, a change expressed relative to another addendum, a partial table row deletion, a new form, a change applying "mutatis mutandis" to several clauses, a correction of an earlier addendum, a change in a footnote, etc.);
   - one place where the addendum is genuinely ambiguous or incomplete in a way a careful bid team would raise as a clarification (keep it realistic — do not make the whole document a puzzle).
   Everything must be fair: a careful human reading the pack + your addendum could reach the conclusions in your answer key.

2. **`SEALED/expected_findings.yaml`** — the answer key, written BEFORE anyone processes the PDF. For every provision (by the number printed in the addendum, plus cover text): the target(s) in the pack (document, clause/table/form/footnote, PDF page index starting at 1 as printed in the footers), the change type, old → new text or values exactly, the effect on obligations (new / amended / deleted / unchanged requirement), any consequence category and the exact quoted consequence words, dates that move (compute them yourself from the pack's own definitions, e.g. Working Days in VOL-I; show the arithmetic and say which counting convention you assumed where the pack is silent), what should change in a one-page "what puts the bid out" sheet (disqualifiers), what bid-preparation activities are affected (programme impact), the traps and what a correct system should do with each, and what a person must decide (ambiguities, legal/commercial calls). Also list provisions that should have NO effect and why.

3. **`SEALED/author_notes.md`** — how you built it (method, what you measured in ADD-01/02 layout), what change types you chose as "not used in ADD-01/02" and why, start and end time (UTC) and elapsed time; plus the builder script you used as **`SEALED/build_addendum.py`**.

4. **`SEALED/SHA256SUMS`** — sha256 of `ADD-03_Addendum_No_3.pdf` and of every file in `SEALED/` (except SHA256SUMS itself), in `sha256sum` format.

Before finishing, render each page of your PDF to PNG and look at it beside ADD-02's pages to check the format really matches; fix anything that does not. Check with PyMuPDF that the text extracts cleanly in reading order.

## Your final message

Your final message goes to the orchestrator, who must stay blind to the answer key. Report ONLY: the list of files written with their sha256, the PDF page count, the issue date printed on the addendum, and your elapsed time. Do NOT summarise the provisions, changes, traps or expected findings in your final message.
