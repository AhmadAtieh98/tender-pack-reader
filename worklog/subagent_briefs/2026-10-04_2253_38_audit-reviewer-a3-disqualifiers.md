# Subagent brief 38: Audit reviewer A3: disqualifiers

Launched 2026-10-04 22:53:27 UTC; model option requested: `opus`; subagent type: `general-purpose`.
The text below is the prompt exactly as sent by the coordinator (exported from the session transcript on 4 Oct 2026, session 11).

---

You are an independent reviewer auditing deliverable A3 (the one-page sheet of what would disqualify a bid) of a tender-reading system. You implemented nothing in this repository. Your id is A3.

Read first, in this order, and follow them exactly:
1. /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/COMMON.md (`<scratch>` means /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11)
2. /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/SCOPE_A3.md
3. /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/MATRIX_SKELETON.md

Current outputs: the fresh rebuild at /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/fresh/out/a3 (byte-identical to the committed /home/user/tender-pack-reader/out/a3). Render the PDF pages with `pdftoppm -r 80 -png` into your scratch folder and read the images; also use pdftotext. Use /home/user/tender-pack-reader/.venv/bin/python.

Hard rules: read-only on the repository (no edits, no git write commands, no `tenderpack approve/accept/reject`, no new files under /home/user/tender-pack-reader); never read rehearsals/, staging/, out-drill*, or anything named ADD-03/ADD-04/blind; derive your expectations (every provision the six PDFs say causes rejection, disqualification or non-responsiveness, and the questions a person must own) BEFORE opening the outputs, and keep those notes in your scratch folder. Write your report to /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/reports/A3.md in COMMON.md's format, then reply with a short summary (findings by severity, matrix results, the model you ran as by your own instructions, time spent). Be economical with turns: the plan's rate limit is shared with a live run.
