# Session 13: the owner's message, verbatim (6 Oct 2026, received 06:01 UTC)

let’s make the final improvements for the interview. we need to prioritize correctness, reliable operation and measured speed.
the scope is this tender through ADD-02, plus the unseen ADD-03. our references remain the brief, emails, volumes, addendums and my recorded decisions. costs stay provisional.

use fable 5.1 at extra-high effort to coordinate, opus 5.5 at high for implementation, and extra-high for independent audits where supported. reserve max for particularly difficult findings, and record the actual settings used.
record what actually runs. start with independent reviewers for A1/A2, A3 and human decisions, and A5/rendering. then assign focused implementation work and independent rechecks. ask me about genuine uncertainties while continuing unaffected work; dont send routine engineering decisions back to me.
1. audit the current outputs, excluding the work log
derive expectations from the original sources before comparing outputs. check source-to-output completeness as well as whether each output is supported.
cover A1’s evidence, classifications, stage statuses and Excel/CSV/JSON agreement; A2’s complete amendment chains and superseded answers; A3’s supported bid-out consequences and understandable unresolved matters; and A5’s requirement coverage, dates, dependencies, resources, marshalling, assumptions, infeasibility and Gantt consistency.
include the clarification register, source links, Arabic, image tables and actual rendered files. keep the maxima/range ambiguity and missing Environmental Permit visible. correct the panel’s “A4 clarification register” label—the work log is A4.
session 12 says the final fixes changed 47 output files without another independent review. recheck the final code and outputs, not an earlier checkpoint. produce one concise findings matrix and independently verify fixes. do not audit or rewrite the historical work log, but record this new work honestly.
2. fix correctness gaps and finish the AI operating rules
first reproduce and fix these findings with failing regressions:
•	a date rule with kind="anchor", PDD and a two-working-day offset is accepted but returns the PDD, ignoring the offset. reject inconsistent rules or calculate the relative date correctly.
•	analysis instructions request row_new for some obligations, but the downstream handoff can drop those items with an empty explanation. every detected obligation needs a supported output path or an explicit unresolved reason.
also challenge the “applied, not decided” mechanism. a clear printed rule can be extracted and applied within its supported scope, but quoting precedence wording must not automatically resolve a contractual ambiguity or remove human ownership.
implement shared runtime instructions for AI operating this system. these should cover the ADD-02 starting state, every ADD-03 provision and attachment, scoped targeting, evidence retrieval, calculations, change propagation, uncertainty, human review and A1–A5 production.
generalize how changes are handled within this pack, not its answers. don’t rely on familiar wording or rehearsal-specific cases. preserve existing rules and decisions where applicable; reconsider them when their evidence or dependencies change. distinguish software limitations from missing evidence and genuine ambiguity.
preserve original evidence separately from effective amended text, including crops, Arabic, translations, table relationships, units and notes. never invent requirements, consequences, bidder facts or approvals. assumptions stay explicit and editable.
ensure every route and phase actually receives the relevant policy: Claude Code, Codex, APIs, Ollama, image reading, analysis, downstream work, critics and repairs. use concise host entry instructions and explicitly supplied runtime prompts. fix contradictory prompt overrides, including HOST_RULES claiming to replace rule 9 and potentially dropping the no_effect safeguard.
enforce critical rules through code and tool permissions too. record code/policy versions at run start and resume; don’t silently continue a benchmark under changed code.
3. improve speed without weakening the checks
the frozen blind-06 run took 55m49s, with only about 78 seconds in deterministic processing. optimize the model workflow first and benchmark the final version; don’t present that earlier timing as its performance.
prioritize preserving completed, validated repsonses through interruptions; reducing repeated context and unnecessary sessions; grouping related provisions; and collecting completed responses promptly so workers don’t sit idle.
collection can happen as responses arrive, but validation and application must retain deterministic dependency order under one controlled writer. revalidate reused results against the current evidence and state.
measure concurrency rather than simply increasing it. preserve coverage, context limits, rate-limit handling, selective criticism and human gates. don’t change inputs underneath running batches or bypass checks to meet 30 minutes.
4. add an optional parallel “AI quick review”
while the main AI-plus-code pipeline runs, let me start a separate, bounded AI reading from the panel.
give it ADD-03 and the relevant original pack/ADD-02 context. it should independently predict changes, cite pages and quotations, identify affected deliverables, explain uncertainties and ask focused questions. read-only retrieval/rendering is fine; don’t prepopulate its conclusions from the main pipeline.
label everything as a preliminary AI briefing. it must not edit authoritative data, approve items or mark pipeline work complete. calculations and interpretations remain unverified until checked.
preserve its initial findings, then compare them with the pipeline results and investigate disagreements. model agreement is not proof. record my answers against the exact questions/evidence and incorporate them at safe checkpoints with revalidation.
keep this pass short and lower priority so it doesn’t starve the main run. measure time to the first useful briefing separately from time to updated A1–A5.
5. prepare a minimal interview folder for my Mac
keep editable code and focused tests for the live fix, original sources, configuration, curated data and approvals, baseline evidence/outputs, runtime instructions, exact dependancies, launcher and the existing panel. include one labelled smoke-test example, recovery instructions and empty folders for new runs/logs.
exclude bulky historical candidate runs and rehearsal outputs/answer keys from this operating copy. preserve the submitted repository separately. build the environment in its final location; don’t assume a copied virtual environment is portable.
fix setup ignoring the dependency lock, ZIP exports losing launcher executable permissions, misleading launcher errors and checks that report PASS without examining actual exit codes/blockers.
support a clear connected/offline choice. Claude Code is the first route to rehearse; keep Codex, the API-key option and Ollama available with honest tested/unverified status. expose usable routes in the panel and explain unavailable ones. keys come later through secure configuration, never chat or logs.
offline mode must prevent hosted calls in every phase. discover installed Ollama models and verify capabilities/context/memory without automatically downloading models.
test on my actual Mac where accesible. otherwise prepare precise checks for me, mark them pending and continue independent work. don’t claim a cloud test proves Mac readiness.
6. finish with verification and a rehearsal
run focused regressions, the full suite on the final code, a fresh rebuild and strict checks. explain every change to the existing ADD-02 outputs with source evidence. pending human approvals must remain pending.
use known rehearsals as labelled regressions, then run one independently authored ADD-03 with its key inaccesible until outputs are frozen. test interruption/resume and the panel’s upload-to-results flow from the interview folder
report missed effects, false positives, usable updates, pending decisions, interventions and timings separately. inspect readability and source navigation on the interview screen.
return a compact report, the runnable folder, launch/recovery instructions and grouped decisions that genuinely need me. preserve 0a63e3a; keep improvements separate and leave the final commit/push for my approval.
