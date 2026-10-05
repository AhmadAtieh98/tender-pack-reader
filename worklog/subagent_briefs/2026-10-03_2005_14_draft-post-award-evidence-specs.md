# Subagent brief 14: Draft post-award evidence specs

Launched 2026-10-03 20:05:32 UTC; model option requested: `(default)`; subagent type: `general-purpose`.
The text below is the prompt exactly as sent by the coordinator (exported from the session transcript on 4 Oct 2026, session 11).

---

You are helping complete a compliance register for a bid on a FICTIONAL tender (an internal assessment pack; confidential: do not publish, upload, search the web, or send anything). You write ONE output file and do not edit the repository.

## Context (repository /home/user/tender-pack-reader; Python at .venv/bin/python)
- Tender text: `build/units.json` -> {"units": [...]} with `unit_id`, `doc`, `pages`, `text` (and `cells` for table rows). VOL-V is the Draft Project Agreement (an EXTRACT: Schedules 7, 9, 11, 12 and the Direct Agreement are referenced but not supplied). VOL-I is the Instructions to Bidders; VOL-II Technical Requirements.
- Register rows: `curation/register/rows.yaml` and `curation/register/rows/*.yaml`. Each row has `id`, `requirement`, `units`, `assessment` (pass_fail | scored | procedural | contractual_post_award), `evidence` (bid deliverable ids such as EV-TECH-PROPOSAL) or `no_deliverable`, and `interpretations` (quote, consequence, note).
- The A1 export currently shows a BLANK "Evidence needed" for these 33 post-award rows: VOL-V-31.3-01, VOL-V-29.2-01, VOL-I-12.1-01, VOL-I-12.2-01, VOL-I-12.2-02, VOL-V-3.1-01, VOL-V-3.2-01, VOL-V-12.1-01, VOL-V-18.3-01, VOL-V-12.2-01, VOL-V-12.3-01, VOL-V-12.4-01, VOL-V-12.4-02, VOL-V-24.1-01, VOL-V-24.2-01, VOL-V-24.3-01, VOL-V-24.4-01, VOL-V-29.3-01, VOL-V-29.4-01, VOL-V-31.1-01, VOL-V-31.1-02, VOL-V-31.1-03, VOL-V-31.3-02, VOL-V-31.3-03, VOL-V-31.4-01, VOL-V-34.3-01, VOL-V-36.2-01, VOL-V-39.1-01, VOL-V-42.1-01, VOL-V-42.1-02, VOL-V-42.2-01, VOL-V-44.2-01, VOL-V-44.3-01.

## The owner's instruction
"Replace blank post-award 'evidence needed' fields with an appropriate proposed evidence requirement, a justified not-applicable entry or an explicit unresolved specification. Don't imply that the bidder has evidence we haven't seen."

## Task
For each of the 33 rows, read the row and the clause text of every unit it cites, then write ONE entry:
- `kind: proposed` — a proposed evidence requirement: what record or document would demonstrate compliance AFTER award (e.g. "monthly availability report with deduction calculation, as the Agreement requires (VOL-V 31.1)"), with `basis` = the clause words that make this evidence natural (verbatim, unit + page), and `when` = the event it relates to (e.g. "monthly after PCOD"). Phrase it as a requirement to produce in future ("to be produced: ..."), never as something held.
- `kind: not_applicable` — when the row is an Authority right, a payment term or a remedy that the Project Company does not evidence (e.g. a deduction the Authority applies); give the `reason`, grounded in the clause words.
- `kind: unresolved` — when the evidence cannot be specified from the pack (e.g. it depends on Schedule 7 or 11, which are not supplied, or on a term the extract does not define); say exactly what is missing (`missing`) and from where it is referenced.
Also give `bid_stage_note` if anything about the row matters for the bid now (e.g. a deviation to list in Form 4-E, a price assumption), otherwise omit.
Never invent figures, dates, holders, certificates or bidder facts; never say the bidder has or holds anything. Quote verbatim and verify each quote with a short Python check against build/units.json (whitespace-normalised) before finishing.

## Output
Write `/tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s08/agents/post_award_evidence.yaml`:
```yaml
rows:
  VOL-V-31.1-01:
    kind: proposed | not_applicable | unresolved
    text: "<one sentence that will appear in the A1 'Evidence needed' column, starting 'Post-award (proposed requirement): ', 'Not applicable: ' or 'Unresolved: '>"
    basis: [{unit: "VOL-V:31.1", page: 3, words: "<verbatim>"}]
    when: "<event/period>"          # proposed only
    reason: "<...>"                 # not_applicable only
    missing: "<...>"                # unresolved only
    bid_stage_note: "<optional>"
```
Then reply with counts per kind and any row you were unsure about. Do not modify repository files, do not commit, and do not mention AI model names in the YAML.
