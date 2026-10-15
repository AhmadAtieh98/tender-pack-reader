# Live ADD-03 candidate results — after timeout and resume

**PARTIAL · CANDIDATE / NOT VALIDATED · HUMAN REVIEW REQUIRED**

All 13 execution steps finished. This is a publication of the actual 15 October 2026 live interview run, including its limitations. It is not an approved tender submission. Eligible decisions were simulated under the disposable interview-demo profile. No real human approval is implied, and missing evidence or conflicting instructions were not resolved by simulation.

**Start with [WHAT CHANGED IN THE OUTPUTS](OUTPUT_DIFF.md)** for before/after links, material changes, the full activity date/status table and downloadable field-level diffs. Then read the [full review packet](review/index.md).

## Open the outputs

| Deliverable | Primary candidate result | Status / reading instruction |
|---|---|---|
| A1 | [Register XLSX](candidate/out/a1/a1.xlsx) | 210 historical rows. Use `Status after ADD-03`; 203 demo-decided, seven unresolved/stale. |
| A2 | [Change register](candidate/out/a2/a2.md) | Proposed ADD-03 reconciliation and downstream effects. |
| A3 | **[Candidate HTML page](candidate/out/a3/a3_candidate.html)** | Primary A3 presentation. One continuous browser page with full detail; not a verified one-A4-page print layout. |
| A3 supporting evidence | [Full diagnostic PDF](candidate/out/a3/a3_candidate.pdf) · [detail](candidate/out/a3/candidate/a3_detail.html) | Seven-page diagnostic retained. The candidate one-page PDF fit failed; see below. |
| A4 supporting register | [Clarification register](candidate/out/a4/clarification_register.md) | Draft questions/supporting record. Git history remains the implementation record; chat/worklogs are not added here. |
| A5 | [Candidate programme CSV](candidate/out/a5/candidate/programme.csv) · [Gantt HTML](candidate/out/a5/candidate/gantt.html) · [marshalling CSV](candidate/out/a5/candidate/marshalling.csv) | Proposed ADD-03 schedule, 44 activities / 26 items; warnings and decision gates retained. |
| Preliminary AI review | [Briefing](preliminary/briefing.md) | 22 items / three questions; preliminary, not approval or fully validated evidence. |
| Validation | [Output checks](candidate/out/checks.json) · [run summary](run-summary.json) | Execution succeeded, but release blockers remain. |

GitHub displays HTML as source. Clone/download the repository and open the HTML in a browser to render it, or use the existing live Safari panel. Relative supporting assets are included. The primary A3 HTML is used instead of presenting the seven-page PDF as a one-page result.

**Do not confuse retained baseline outputs with ADD-03 proposals.** `candidate/out/a3/a3.pdf` and the main `candidate/out/a5/` programme/Gantt remain at validated ADD-02 because ADD-03 is partial. Use `a3/a3_candidate.html` and `a5/candidate/` for ADD-03. The copied baseline is also available under [out-before](candidate/out-before/README.md).

## Review required

Controller completeness is **14 of 19 provisions answered; five unresolved**, including two partly applied provisions. All 58 downstream tasks received responses, but only 44 have promotable answers; fourteen remain unresolved/non-promotable. Detailed IDs and statuses are in [run-summary.json](run-summary.json).

| Provision | What remains unresolved | Required next action |
|---|---|---|
| ADD-03 §2.2 | Collective PDD-dependent period adjustment rejected by the engine's explicit-citation check. The Form 4-A printed date also conflicts with the amended due date. | Correct/verify target mapping; document control reviews affected date references and the form correction/execution instruction. Do not silently rewrite the form. |
| ADD-03 §3.1 | §7.2 cessation was applied to the candidate, but grouped Form 4-G withdrawal could not be represented. Seven related readings are STALE. | Fix the group/citation targeting limitation; re-read surviving technical undertakings and their evidence route. Review submission-list reconciliation and Form 4-G activities. |
| ADD-03 §4.1 | Volume II §2.1 capacity change was applied, but Table 2-6 rows 2-6.1/2-6.2 failed citation mapping. | Correct the table-target mapping; verify 150,000 m³/day average flow separately from unchanged peak hourly flow. Do not substitute a neighbouring cell. |
| ADD-03 §4.3 | “Amended correspondingly” does not supply the exact replacement for the worded and numeric Volume I §1.3 phrase. | Obtain an explicit technical/document-control interpretation; retain the unresolved disposition until then. |
| ADD-03 Q17 | Pricing row exists, but row-only obligations are not fully accounted for by the amendment-coverage engine. No payment adjustment mechanism is stated. | Fix coverage accounting; commercial/legal review of pricing and payment implications. Do not invent an adjustment mechanism. |

Additional human questions remain in the full packet, including the §11.6 “within 2%” comparison basis and discretionary criteria, bond counting/coverage, Form 4-A instructions, copies/envelope assembly conflicts, missing documents, and earlier clarification answers requiring re-reading. These are not settled by model agreement or demo approval. The critic reviewed 31 items and disagreed on eleven across nine sessions.

The output builder reports three release-blocker categories: unresolved coverage, seven stale rows, and seven rows without a current human decision. Zero register-check findings is a structural result, not a clean-release certificate. Eight relationship proposals were held back because their endpoints could not be promoted.

## Timing and timeout recovery

| Stage | Observed time / result |
|---|---|
| Whole live run | **71m 09s** wall time; 16:19:27–17:30:36 Riyadh (13:19:27–14:30:36 UTC), 15 October 2026. |
| Preliminary review | 6m 54s, ran alongside the workflow. |
| Analysis | 9m 26s. |
| Downstream | 57m 55s recorded active step time across both attempts, including retry work. |
| Final critic | 2m 39s. Earlier batch critics are separate. |
| Timeout | One host call timed out after about 595 seconds; its retry was interrupted by the 2,700-second overall guard. Initial job exit 130. |
| Resume | 17:04:56 Riyadh; completed batches reused; final job exit 0, result PARTIAL. |

Fast service tier was requested through a run-scoped Codex launcher for the resume. Configured model stayed `gpt-6-astra` with high reasoning. The actual tier/model identity was not independently reported. Application code and policy identity did not change. The original runtime target was missed; this is not a 20–30 minute success claim.

## Known report and presentation limitations

- The generated review packet captures its own `review` step as “running” while it is being written. The final controller summary confirms that all 13 steps, including review, finished.
- Some generated summaries count three wholly unresolved dispositions; the controller counts **five** by also including partly applied §3.1 and §4.1. Use the five-item list above for review scope.
- Cover-summary “not found” diagnostics are matching/representation results, not proof that the addendum lacks Form 4-G withdrawal or the new §11.6; both are printed in the source.
- The candidate one-page PDF fit failed at minimum scale 0.89 with 20 items / 12 unresolved. The complete HTML is the primary presentation; no successful one-page PDF fit is claimed.
- Some preliminary baseline citations were checked against addendum pages and reported NOT FOUND. Treat the preliminary briefing as a starting point and use the full evidence review.
- Generated PDF/XLSX bytes are preserved. Text exports replace the private operating-folder prefix with `${INTERVIEW_ROOT}`. Local-panel/host-session links may require the original live environment; excluded model-session links are intentionally unavailable in this archive.

## Publication scope and integrity

Based on source revision `cbe0e944d0db804b5894d3fb42080e3774c3443d`. Input PDF SHA-256: `6f9f9d7c7d68bc83b947d20fa348271b91695463eae5435a70b09afd1955ad25`; [original live input](candidate/input/6f9f9d7c7d68bc83b947d20fa348271b91695463eae5435a70b09afd1955ad25.pdf).

Included: generated outputs, copied ADD-02 comparison outputs, candidate curation/configuration, source evidence/crops, structured proposals, review/diff records, preliminary briefing, and a selected final run summary. These are a read-only result archive, not a resumable checkpoint or portable installed application.

Excluded: chat transcripts, worklog changes, generated prompts, raw model exchanges, host-session captures, request packets, credentials, runtime logs, caches, virtual environments and the raw checkpoint. Existing repository history is not rewritten. No application code or authoritative source curation was changed by this publication.

Before publication, frozen ADD-02 hashes and live real-input fingerprints matched their starting state; runtime code content matched the recorded identity. [MANIFEST.sha256](MANIFEST.sha256) covers the published run files (excluding itself).
