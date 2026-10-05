# Subagent brief 41: Audit reviewer R: rendering

Launched 2026-10-04 22:53:55 UTC; model option requested: `opus`; subagent type: `general-purpose`.
The text below is the prompt exactly as sent by the coordinator (exported from the session transcript on 4 Oct 2026, session 11).

---

You are an independent reviewer auditing the RENDERED deliverables (Excel, PDF, HTML, SVG, Markdown) of a tender-reading system for readability, Arabic rendering, tables, cross-document consistency and stale statements. You implemented nothing in this repository. Your id is R.

Read first, in this order, and follow them exactly:
1. /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/COMMON.md (`<scratch>` means /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11)
2. /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/SCOPE_R.md
3. /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/MATRIX_SKELETON.md

Current outputs: the fresh rebuild at /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/fresh/out (and .../fresh/build for coverage.md and the crops) is the current state; /home/user/tender-pack-reader/out is the committed reference (differs in README.md, a2/a2.md, three a5 files). Render every PDF page with `pdftoppm -r 80 -png` into your scratch folder and read the images; open the xlsx with openpyxl through /home/user/tender-pack-reader/.venv/bin/python; read HTML/SVG/Markdown as text. For the two image readings compare the crops with the Arabic in curation/readings/ and the translations.

Hard rules: read-only on the repository (no edits, no git write commands, no `tenderpack approve/accept/reject`, no new files under /home/user/tender-pack-reader); never read rehearsals/, staging/, out-drill*, or anything named ADD-03/ADD-04/blind; derive from the brief (§3 and §4 especially) what the rendered files must and must not contain BEFORE opening them, and keep those notes in your scratch folder. Write your report to /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/reports/R.md in COMMON.md's format, then reply with a short summary (findings by severity, matrix results, the model you ran as by your own instructions, time spent). Be economical with turns: the plan's rate limit is shared with a live run.
