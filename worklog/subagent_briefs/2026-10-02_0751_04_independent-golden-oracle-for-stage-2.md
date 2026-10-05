# Subagent brief 4: Independent golden oracle for stage 2

Launched 2026-10-02 07:51:22 UTC; model option requested: `(default)`; subagent type: `general-purpose`.
The text below is the prompt exactly as sent by the coordinator (exported from the session transcript on 4 Oct 2026, session 11).

---

You are writing an INDEPENDENT test oracle for a tender-pack reader. Your output will be used to check another program's results, so you must derive every expectation yourself from the source PDFs, not from that program. Repository: /home/user/tender-pack-reader. Sources (read with PyMuPDF via `.venv/bin/python`, e.g. `import pymupdf; pymupdf.open(path)[i].get_text()`): sources/candidate_pack/VOL-I_Instructions_to_Bidders.pdf, VOL-II_Technical_Requirements.pdf, VOL-IV_Form_Sheets.pdf, VOL-V_Draft_Project_Agreement.pdf, ADD-01_Addendum_No_1.pdf, ADD-02_Addendum_No_2.pdf. (Each page also carries a rotated watermark "FICTIONAL — ASSESSMENT PACK"; ignore it.) Two items exist only as images and have proposed transcriptions in curation/readings/VOL-II-p3-r1.yaml (Table 2-4) and curation/readings/VOL-IV-p6-r1.yaml (Form 4-C, Arabic); you may read those two YAML files, and you may view the page images (render with PyMuPDF to PNG under your scratch folder and look at them) to confirm.

STRICT independence rules: do NOT read anything under tenderpack/, tests/ (other than writing your output file), docs/, worklog/, build/, or config/. Do not run the repository's code. Do not edit any file except the single output file below. Do not commit or push. Scratch files go only under /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/oracle/ .

Write `tests/golden/stage2_expectations.yaml` (YAML, UTF-8, comments allowed) containing facts a correct amendment engine must reproduce, each with the PDF page and a short verbatim quote as evidence. Stages are BASE (the volumes as issued), ADD-01 (after Addendum No. 1, issued 8 Oct 2026), ADD-02 (after Addendum No. 2, issued 22 Oct 2026). Cover at least:

1. `pdd`: Proposal Due Date date and time at each stage (from VOL-I Clause 6.1 and its amendment).
2. `lcc`: Volume I Clause 8.6 (Local Content Certificate) at each stage: status (active / deleted / active-reinstated-amended), the percentage, and whether a consequence is stated (quote it); status of Addendum No. 1 Section 4.2 (the "disregard references" rule) at ADD-01 and ADD-02.
3. `repeated_wording`: for each pair, the clause that changes and the one that must NOT change, with values at ADD-02: "seventy-two (72) hours" (VOL-II Clause 4.4 vs VOL-V Clause 31.3); "sixty per cent (60%) ... forty per cent (40%)" (VOL-I Clause 11.2 vs VOL-V Clause 29.2); also VOL-V Clause 36.2 SAR value.
4. `weighting`: VOL-I 11.2 weighting at each stage; Table 1-1 marks for every criterion A–F and total at BASE and at ADD-02; the technical threshold in 11.3 at ADD-02.
5. `tn`: Table 2-4 TN limit, unit and basis at BASE (image) and ADD-02, and note that the base value comes from an image.
6. `form_4g`: whether Form 4-G exists at each stage, where it is inserted in VOL-I Clause 9.1, the stated consequence, and any unspecified detail (e.g. re-lettering).
7. `form_4c`: the English-text requirement (VOL-I 9.4) and its consequence; the Arabic declaration 4 consequence wording and your own English rendering; the Arabic note consequence; ADD-02 Q9.
8. `form_4a`: the printed Proposal Due Date on the original Form 4-A (VOL-IV) and on the reissued Form 4-A (ADD-01 Appendix A); whether that matches the PDD at each stage; list what the reissued form omits compared with the original (fields and numbered confirmations).
9. `dates`: for BASE and ADD-01 PDDs, compute yourself (show your counting in comments) the clarification cut-off (VOL-I 5.2 with VOL-I 2.4's rule), bid bond validity end (6.3), proposal validity end (7.1), reference-plant look-back start (footnote 12 to 8.5), and the ADD-01 Section 3.1 window end; where the counting convention is not stated in the pack, give each plausible reading (e.g. PDD as day 0 vs day 1) as separate values. Working Days are Sunday–Thursday (VOL-I 2.4), no holidays assumed.
10. `answers_quoting_old_values`: clarification answers or minutes items that quote or rely on a value later changed (e.g. ADD-01 Q2's "120-page limit"; the minutes' "seventy / thirty"), with whether they are binding (ADD-01 §3.2 says minutes do not bind) — state facts only; do not decide whether an answer is "revoked".
11. `provisions`: the complete list of provisions (numbered clauses, table notes, Q&A rows, appendix items, form items) in ADD-01 and in ADD-02, each with a one-line description and which volume unit it targets if any (e.g. "VOL-I 6.1"), so a coverage check can be compared against it.

Keep values literal (dates as YYYY-MM-DD strings). Where you are unsure, add `uncertain: <why>` rather than guessing. In your final message summarise the file's top-level keys, counts of provisions per addendum, any discrepancies you noticed in the pack, and anything you could not determine.
