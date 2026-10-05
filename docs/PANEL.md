# The local operating panel (`tenderpack panel`, session 12)

The owner's operating panel: a small page on this machine over the existing engine and workflow. **A1–A5 in `out/`
remain the deliverables**; the panel runs the existing commands and opens their files. It is plain HTML with no
script, no external resource, no branding and no dashboard. Code: `tenderpack/panel/` (`server.py`, `jobs.py`,
`views.py`); tests: `tests/test_session12_panel.py`.

## Start it

```
python -m tenderpack panel --open            # a free port; opens the default browser
python -m tenderpack panel --port 8765       # a fixed port; open the printed address yourself
```

On the Mac: `scripts/mac/launch.command`, item 7 (it runs `.venv/bin/python -m tenderpack panel --open`; the launcher
sets `TENDERPACK_OFFLINE=1`, so AI runs started from the panel are offline: the local ollama route only). The panel
prints its address once: `http://127.0.0.1:<port>/t/<token>/`. Ctrl-C stops the panel; a job it started keeps running,
and the next panel shows it (a job whose process ended while no panel was watching is shown `interrupted`, exit code
unknown; an AI run's own checkpoint says where it stands).

Options for a disposable workspace (the tests use them): `--pack`, `--evidence`, `--out`, `--staging` (the AI staging
folder), `--worklog`, `--panel-dir` (default `staging/panel`).

## Pages

| Page | What it shows | What it runs |
|---|---|---|
| Home | first a **Deliverables** strip (A1 `a1.xlsx`, A2 `a2.md`, A3 `a3.pdf` and its detail page, A4 the clarification register and the work log index, A5 `gantt.html`/`gantt.pdf`/`README.md`, the review batches' `index.html`; each opens in the browser or downloads; a missing key file is named), then the **New addendum** box, then the stages applied (`out/stages.json`); four separate records: **execution** (the last ingest/outputs/strict/check-register jobs and their exit codes), **completeness** (`checks.json` reported checks), **structural validation** (`checks.json` structural checks), **human approval** (release status, the strict check's blockers, items by kind and status from `out/review/items.json`); A1 (xlsx, csv, json), A2, A3 (pdf, html, json), A4 clarification register (md, csv, json), A5 (Gantt pdf/html, programme csv, README), the review packets, each with open and download | Run ingest, Run outputs, Run strict check, Run check-register |
| Stages | BASE, ADD-01, ADD-02 and every candidate run's addendum stage; each stage's source PDF and a units page (unit, pages linked to the PDF page, text as printed); the image region renders under `build/review/` | Compare: `tenderpack diff --from A --to B` (in the candidate's workspace when a candidate stage is involved; two different candidate runs are refused) |
| Addendum | upload form: addendum id (the next ADD-NN by default), PDF, route (host; ollama when the local endpoint lists a usable model; recorded only in tests), model (only what `tenderpack ai routes --json` lists as usable), offline checkbox, `--base-run` (offered when this build's `ai run --help` has it and a run's promotion is done; otherwise disabled, "not in this build") | `tenderpack ai run ADD-NN --pdf staging/panel/uploads/<sha256>.pdf --route R --run-id ID [--offline] [--model M] [--base-run RUN]` |
| Runs | every run under `staging/ai/runs/`: execution (status, reason, exit code explained, steps with seconds, batches with attempts and failure class), failures and deferrals (a rate limit with the reset time; exits 5 and 6 explained), completeness (provisions, downstream tasks, the checkpoint's reasons), structural validation (the candidate outputs build, check-register, the candidate's own `checks.json`), human approval (none unless a person decided: everything PROPOSED), pending questions (the review packet's "unresolved provisions and escalations" section, its HUMAN DECISION PENDING lines, the clarification window note, escalated batches); a run whose checkpoint says running but whose run lock has no live process is shown **interrupted** | Resume: `tenderpack ai resume RUN [--from STEP]`; a finished run's page offers "Open the review packet" (with the diff and a jump to the candidate outputs) right under "What it needs from you" |
| Candidate review | a run's `candidate/out/` files, its review packet and diff, opened in place under the banner "CANDIDATE, not approved; the validated outputs are under out/" (added on top of HTML and text when viewed; the download is the file exactly as written); nothing is copied into `out/` | — |
| Jobs | every job: kind, status, exit code and its meaning, start and end, the exact command line; a job page shows its output (the whole report for a diff or a decision) and a Stop button (SIGINT to its process group, then SIGTERM, then SIGKILL) | — |
| Decisions | the pending rows, ops and readings (`out/review/items.json`), the A4 clarification entries and the curated issues, each with its exact `accept`/`reject` (or `approve` for a reading) command and the latest decision recorded in the decisions file | `accept|reject ITEM --reviewer NAME --note REASON` or `approve REGION --reviewer NAME --notes REASON`, only after a person filled the form |

## Rules the panel keeps

- **Real jobs only.** Every action is `<the same python> -m tenderpack …` in a subprocess with the repository as its
  working directory; `staging/panel/jobs/<job>/job.json` records the argv, the command line to repeat it, start, end,
  exit code and pid; `output.log` holds stdout and stderr. One job at a time per group (ingest, outputs, strict and
  check-register share one; `ai run` and `ai resume` another; diff; decisions).
- **Versioned outputs.** `out/` is written only by the outputs job (the command keeps the previous build on a
  structural failure and on a refused strict release). Candidate outputs stay in their run folders. `rehearsals/` is
  never written; a run whose PDF is a rehearsal input (by path, or an upload whose sha256 equals one) is labelled
  "synthetic (rehearsal input)".
- **Human decisions explicit and recorded.** The panel never pre-selects a decision or pre-fills a name. The form
  needs the decision chosen, a name and a reason; the next page shows the exact command and a confirmation box,
  unticked; only then does the engine run, and the engine records the decision bound to the item's content. The
  result page is the engine's own output. Opening a page starts no job; the Addendum page runs two read-only
  queries each time it opens: `tenderpack ai routes --json` (it checks the LOCAL Ollama endpoint only; never a hosted
  one, never a host process) and, once per panel start, `tenderpack ai run --help` (to see whether `--base-run` exists).
- **Uploads.** At most 50 MB (a larger request is refused from its header, before the body is read); the bytes must
  start with `%PDF-`; stored as `staging/panel/uploads/<sha256>.pdf` (never executed, never opened by the panel); the
  original file name is sanitised and kept only in the job record. The engine's own checks follow (`ai run` refuses an
  unreadable PDF, an addendum id that does not follow the pack's last one, a document the pack already has).
- **Model-produced text** (a run's reasons, errors, review sections, unit text) is HTML-escaped everywhere. Panel pages
  send `Content-Security-Policy: default-src 'none'` (inline style only, no script, no external load); files are
  served with a CSP that runs no script and `X-Content-Type-Options: nosniff`.
- **Files** are served from these areas only: `out/`, the evidence build's `review/` renders, a run's
  `candidate/out/`, `candidate/input/` and `review/`, `staging/panel/jobs/` and `sources/`. A path with `..`, an
  empty or `.` part, a backslash or a NUL is refused; the resolved path must stay inside its area, so a symlink out
  of it is refused.
- **Local only.** 127.0.0.1, a random token per start in the URL path (compared in constant time), the Host header
  must be 127.0.0.1 or localhost on the panel's port (DNS rebinding), forms post only to the panel. The terminal's
  access log replaces the token with `<token>`.
- **Credentials.** The panel reads no key and shows no environment variable. Jobs inherit the environment (a route
  reads its own key, as from a terminal); job records hold the argv only.

## Tested here (tests/test_session12_panel.py, recorded route, disposable folders)

- the server binds 127.0.0.1 only, on a free port; a request without the token, with a wrong token or another Host
  name is refused; path traversal (plain, URL-encoded, NUL, backslash), symlinks out of an area and paths outside the
  areas are refused;
- an upload that is not a PDF, an oversized request, a bad addendum id and a route the panel does not offer are
  refused and start nothing;
- **output parity**: `outputs` run through the panel gives files byte-identical to a direct `outputs` run on the same
  evidence build (every file compared; the guide names no timestamp line, so none is excluded);
- **upload to results**: the synthetic ADD-03 of rehearsal 02 uploaded on the recorded route runs a real
  `tenderpack ai run` job to the end (partial: the cassette leaves batches unrecorded, by design); the job page shows
  the run id and the exact command; the run page shows the four records, the pending questions and Resume;
- **resume**: a second run's process group is killed (SIGKILL) after its first analysis batch; the run page shows it
  interrupted; Resume from the panel finishes it, takes over the dead run lock, and does not ask the done batch again;
- the candidate review page and every file it links never write `out/`; the HTML carries the CANDIDATE banner; a diff
  from ADD-02 to the candidate ADD-03 runs in the candidate workspace; the real `curation/`, `config/`, `out/` and
  `staging/` are unchanged (sha256 of every file) after all of it;
- the decisions form refuses without a decision, a name or a reason, refuses without the confirmation, refuses an
  option passed as an item, and builds exactly `accept ITEM --reviewer NAME --note REASON …` when everything is given
  (the test captures the command instead of running it: no decision was recorded by the tests);
- model text with markup is escaped on the run pages.

## PENDING ON THE MAC

- a browser click-through of every page (Safari and Chrome), including opening the PDFs and the xlsx download;
- `--open` and `scripts/mac/launch.command` item 7;
- an upload and run on the ollama route with a real local model (the recorded route only here), and on the host route
  (it uses the owner's plan; not started here);
- a decision recorded through the form by the owner (no decision was made here);
- `--base-run`: shown "not in this build" here (this build's `ai run --help` has no such flag); check it once the flag
  is merged.
