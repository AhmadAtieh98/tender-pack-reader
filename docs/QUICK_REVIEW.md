# The AI quick review (session 13, part 4)

A separate, bounded, lower-priority AI reading of a new addendum, started beside the main AI-plus-code run, that writes
a **PRELIMINARY AI BRIEFING — unverified: not a decision, not a validation; calculations and interpretations
unchecked**. It never edits authoritative data, approves an item or marks pipeline work complete. Code:
`tenderpack/ai/quick_review.py`; its runtime policy: `tenderpack/ai/policy/70_quick_review.md` (composed after the shared
sections, like every phase; docs/RUNTIME_INSTRUCTIONS.md).

## Commands

    tenderpack ai quick-review ADD-03 --pdf PATH [--route host|anthropic|openrouter|ollama|recorded]
                               [--budget-minutes 10] [--max-tokens 60000] [--model M] [--offline]
    tenderpack ai quick-review compare QR_ID RUN_ID          (or a folder holding a run's checkpoint.json)
    tenderpack ai quick-review answer QR_ID --question Q1 --answer "..." --by "Your Name"
    tenderpack ai quick-review offer QR_ID RUN_ID            (between phases only)
    tenderpack ai quick-review revalidate RUN_ID             (the staleness guard of the offered notes)

The panel runs the same commands (docs/PANEL.md, "AI quick review").

## What it is given, and what not

- ONE session (no batches, no critic): the recorded and API routes through the workflow's own request path
  (`requests.converse`, `offline.check_route` in `providers.make`); the host route in ONE Claude Code answer session
  (`hostsession.AnswerSession`, `--allowedTools` exactly the tools below; no repair session).
- The addendum's text page by page and, on a route that reports image input, the rendered images of the pages with image
  regions (or no text layer). The host route receives its packet as text: there the page images are NOT attached and
  the briefing lists them under "Not read" as a software limitation.
- The read-only retrieval tools over the **published** workspace (the validated evidence build and pack: ADD-02 today):
  `search_evidence`, `get_unit`, `get_group`, `get_crop`, `compare_state`. No `simulate_amendment`, no `calculate`, no
  validation and no submission tool, on every route. An evidence build or pack inside the staging folder (a run's
  candidate) is refused; the main run's proposals, candidate and packets are never read (`request.json` records
  `main_run_inputs_read: []`).
- Lower priority: one quick review at a time, a wall-clock budget, a token cap (input; output at most a quarter of it),
  at most 12 calls, a rate limit never waited out (status `deferred`, exit 5: start it again later), no addendum lock
  (the main run holds it), the process niced (the panel starts it under `nice -n 10`).

## What it writes (`staging/ai/quick-review/<qr id>/`)

`request.json`, `briefing.json` and `briefing.md` (predicted changes: provision, page, quotation, target unit guess,
kind, deliverables A1-A5 and rows, confidence, uncertainty class; questions with their evidence; unverified
calculations; what was not read; beside each, the program's CHECKS: is the quotation verbatim on that page of the text
layer, is the target id a unit of the published workspace; checks, never a validation of the reading),
`briefing.sha256` (the initial findings preserved; both files read-only; later steps never edit them), `timing.json`
(start, first useful briefing, end, tokens), `log.jsonl`, and later `comparison.json/.md` and `answers.yaml`.

## Timings, measured separately

`timing.json` measures the time from the quick review's start to its first useful briefing (one with at least one
predicted change or question). The run's time to its updated A1-A5 candidate is read from the run's own checkpoint
(start to the end of its `outputs` step). The comparison and the panel show both side by side; neither is derived from
the other.

## Compare, answers, safe checkpoints

- `compare` matches the briefing's predicted changes one to one with the run's analysis items (its combined set) by
  provision, target unit and quoted words, and lists agreements, disagreements (the differences and the evidence of each
  side) and one-sided items, under "model agreement is not proof: every item is verified only by the validators and a
  person". Disagreements are a list for a person, never an edit.
- `answer` records the owner's answer (name, time) in `answers.yaml` against the exact question text and its evidence;
  `curation/` is never changed.
- `offer` offers recorded answers to a run only between phases: while any step or batch of the run is running, every
  answer is held (the reason recorded beside it). Between steps each becomes a PROPOSED note in the run's
  `owner_answers/<qr id>.yaml` (review pending a person), its evidence checked verbatim against the run's addendum PDF,
  with a staleness fingerprint of the run (combined set, downstream set, candidate curation); `revalidate` marks a note
  STALE when the run changed after it was offered. The workflow does not read these notes by itself: a person carries
  one into the review. A note is never a decision.

## Status of the routes (`tenderpack ai routes` prints it per route)

Recorded: tested (hand-written cassettes, tests only). Host, Anthropic, OpenRouter, Ollama: built, untested live.
