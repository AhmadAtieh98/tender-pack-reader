# The AI quick review (session 13, part 4)

A separate, bounded, lower-priority AI reading of a new addendum, started beside the main AI-plus-code run, that writes
a **PRELIMINARY AI BRIEFING — unverified: not a decision, not a validation; calculations and interpretations
unchecked**, labelled in every rendering (briefing.json/.md, comparison, panel pages, command line) as
**preliminary; model output; not a tool result**. It never edits authoritative data, approves an item or marks pipeline
work complete. Code:
`tenderpack/ai/quick_review.py`; its runtime policy: `tenderpack/ai/policy/70_quick_review.md` (composed after the shared
sections, like every phase; docs/RUNTIME_INSTRUCTIONS.md).

## Commands

    tenderpack ai quick-review ADD-03 --pdf PATH [--route host|anthropic|openrouter|ollama|recorded]
                               [--budget-minutes 10] [--max-tokens 60000] [--model M] [--offline]
    tenderpack ai quick-review compare QR_ID RUN_ID          (or a folder holding a run's checkpoint.json)
    tenderpack ai quick-review answer QR_ID --question Q1 --answer "..." --by "Your Name"
                               [--kind judgment|fact] [--cite "page 3: the words"] [--cite "VOL-I:6.1: the words"]
    tenderpack ai quick-review offer QR_ID RUN_ID            (between phases only)
    tenderpack ai quick-review revalidate RUN_ID             (the staleness guard of the offered notes)

The panel runs the same commands (docs/PANEL.md, "AI quick review").

## What it is given, and what not

- ONE session (no batches, no critic): the recorded and API routes through the workflow's own request path
  (`requests.converse`, `offline.check_route` in `providers.make`); the host route in ONE Claude Code answer session
  (`hostsession.AnswerSession`, `--allowedTools` exactly the tools below; no repair session).
- The addendum's text page by page and, on a route that reports image input, the rendered images of the pages with image
  regions (or no text layer). The host route receives its packet as text, so (session 14) its session is offered ONE
  more read-only tool, `get_addendum_page {page[, region]}`, scoped to the new addendum only: when the quick review
  starts, every page is rendered (at most 1600 px on its longest side) and every image region is cropped (up to 300 dpi,
  at most 2000 px) with its native embedded image (PNG/JPEG up to 3.75 MB) into `addendum-pages/`, each file's sha256
  recorded in `addendum_scope.json`; the session's MCP server is started with `--addendum-scope` and serves those files
  only, re-checking each sha256 (an altered file is an integrity failure), refusing any other page, region or scope
  file, and writing nothing. The packet's `page_images` names the tool and the image pages; the briefing records the
  pages and regions the session requested (`page_images_read_through_tool`) and lists an image page it did not request
  under "Not read" (missing evidence). The tool is gated by `policy.tools("quick_review", "host")`; it is not a model
  tool of the API routes (they receive the images attached) and no other phase is offered it.
- The read-only retrieval tools over the **published** workspace (the validated evidence build and pack: ADD-02 today):
  `search_evidence`, `get_unit`, `get_group`, `get_crop`, `compare_state` (and, on the host route, `get_addendum_page`
  above). No `simulate_amendment`, no `calculate`, no validation and no submission tool, on every route. An evidence build or pack inside the staging folder (a run's
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
- `answer` records the owner's answer (name, time) in `answers.yaml` against the exact question text and its evidence,
  with its KIND (session 14): `judgment` (the default: your proposed judgment) or `fact` (a fact the run may take only
  with evidence: `--cite "page N: words"` on the addendum, `--cite "UNIT_ID: words"` in the pack); `curation/` is never
  changed.
- `offer` offers recorded answers to a run only between phases: while any step or batch of the run is running, every
  answer is held (the reason recorded beside it). Between steps each becomes a PROPOSED note in the run's
  `owner_answers/<qr id>.yaml` (review pending a person) with a staleness fingerprint of the run (combined set,
  downstream set, candidate curation); `revalidate` marks a note STALE when the run changed after it was offered.

## The controlled handoff at safe checkpoints (session 14, `tenderpack/ai/answers.py`)

The run itself takes the offered answers, at its safe checkpoints only (between steps, never under a running batch):
**after readings, before analysis**; **before downstream**; **before promotion** (`workflow._drive` calls
`answers.at_checkpoint` before each of these steps). An answer still HELD for the run is offered there first. Then, per
note:

1. **Staleness**: a note whose fingerprint differs from the run's now is STALE and is not consumed; offer it again (it is
   then re-checked against the current state).
2. **Evidence checks**: a `fact` with no cite, or with a cite not found (the words not verbatim on that page of the run's
   addendum, or not in the named unit's text, or no such unit), is REFUSED with the reason. A `judgment` needs no cite:
   it is recorded as your PROPOSED judgment, owned by you, never an approval.
3. **Approved readings**: an answer citing a unit of an approved reading (`curation/approvals.yaml`) would change that
   reading's interpretation: it is recorded PENDING, never applied and never given to a batch; it changes only through
   the accept/reject workflow.
4. **Consumption and affected-work revalidation**: the answer's scope is the run's provisions whose text holds the quoted
   words of the question or the answer, or whose items target or cite a cited unit (else those on a cited page). The
   done batches in that scope (analysis batches by provision, downstream batches by task) are RE-ASKED: set back to
   pending (their earlier items kept under `superseded`; a kept host submission is set aside), and the steps from that
   phase to the checkpoint run again at once. The checkpoint records what it consumed, re-asked and asked with the
   answer (`checkpoint.json` `owner_answers.checkpoints`).

A consumed answer reaches the next packets of the batches in its scope under `owner_answers`: a **constraint** (a fact
with verified evidence: stay consistent with it, cite the evidence itself) or **context** (a judgment: mention it; never
resolve an ambiguity, close an issue or approve an interpretation on it), each with your name, the times and the evidence
checks, labelled PROPOSED and "never an approval". It is recorded as an intervention by you (`interventions`: "owner
answer consumed", by, ts) and in the candidate's `owner_answers.yaml` (status PROPOSED or PENDING; decision "none ...
accept/reject"). The validated state (`curation/` and the real `out/`) is never touched; approvals still happen only
through the accept/reject workflow. The panel shows each answer's state beside it: recorded, held, offered, consumed at
<checkpoint>, stale, refused (with the reason) or pending (with the reason); no button on the quick-review pages approves
anything.

## Status of the routes (`tenderpack ai routes` prints it per route)

Recorded: tested (hand-written cassettes, tests only). Host, Anthropic, OpenRouter, Ollama: built, untested live.
The host route's `get_addendum_page` (session 14) has run only over the real MCP server on stdio and with a fake host
CLI (tests); no live host session has used it. The checkpoint handoff has run on synthetic run folders and on one
recorded workflow (hand-written cassette); no live run has consumed an answer.
