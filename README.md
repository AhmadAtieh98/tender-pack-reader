> **Current interview demo:** see [implementation handover](docs/INTERVIEW_DEMO_HANDOVER.md) for the prepared ADD02 → ADD03 workflow, one-page candidate A3, editable simulated decisions, verification boundaries and continuation steps. Coding agents start with [AGENTS.md](AGENTS.md).

# tender-pack-reader

Working repository for the Lamar Holding PPP AI Partner Round 2 assessment.

**Status (session 13, `docs/PLAN.md` revision 13): DRAFT handover, stopped for the owner's review before final submission; the session-13 work (the audit and its fixes, the correctness gaps and the runtime policy, speed, the AI quick review, the interview folder, the sealed blind-07 rehearsal: `docs/session-13_report.md`) is committed as ONE closing commit on top of `0a63e3a`, the head of branch `claude/hopeful-curie-7oki9q` at the end of the session (made after this text was written, so its hash is not in it: `git log -1`), on the owner's instructions of 16:19 UTC ("commit after finishing all") and 20:16–20:18 (the subject's wording). Sessions 09, 10 and 11 are committed (`a41e104`, `a57f118`, `6053493`, each on the owner's authorisation); session 12 is committed as `cfaac79` (progress, 13:38 UTC on the owner's instruction), `eaea64d` (20:08) and `2cff460` (20:46), then the closing commit, the head of branch `claude/hopeful-curie-7oki9q` at the end of the session (made after this text was written, so its hash is not in it: `git log -1`) (on the owner's instructions of 13:37, "commit progress now and continue the work fully and commit once done", and 21:10, "commit when all is done only and we are not waiting for anything").**

**A4, the work log, is not only `out/a4/`:** start at `worklog/README.md` (the index of the commit history, the verbatim prompts, the subagent briefs, the model-call logs, the error index and the session reports). `out/a4/` holds the clarification register, a supporting record.

- **Stages 1–4** (evidence, the amendment path, the full register, A5) are the working basis. The owner's session 08 code-review findings are fixed, each with failing-first tests: a rejected op is never re-applied by a rebuild; decisions bind to the state immediately before each op, including every member row of a replaced table; an inserted obligation needs its own A1 row; a Friday or holiday deadline keeps its legal date and gets a Working-Day window or an explicit conflict.
- **Review:**
  - both image readings carry the **owner's confirmations** (Ahmad, 3 Oct 2026, `curation/approvals.yaml`): transcriptions and displayed translations (Form 4-C's translations as displayed; what they mean stays in the rows), with what stays open and what is not covered (interpretations, amendment ops, bidder compliance, the Environmental Permit's contents and compliance);
  - every row (205) and op (37) is still **proposed**; the owner-directed interpretations of VOL-I 8.3, 3.4 and 6.7 were applied from evidence-backed proposals and await the owner's decision.

  Decisions are recorded only with `tenderpack accept|reject`, bound to the item's current content, under a person's name (the assistant's is refused). A YAML flag is never an approval.
- **A strict release** (`outputs --strict`) is refused in this state.
- **Clarifications:** `curation/clarifications/register.yaml` holds draft questions (never sent); `out/a4/clarification_register.md`.
- **Live-addendum tooling:**
  - `show ROW`, `diff`, review batches (`out/review/`);
  - checks C12 (stable ids), C28 (cover summary vs provisions, report only), C30 (date coverage), C32 (counting conventions), C46 (obligation trace) and C47 (every added word printed).
- **Draft archive:** built by `scripts/make_draft_archive.py`. See `docs/OPERATING_GUIDE.md`, `docs/VERIFY_ON_MAC.md` and `docs/COST_AND_EFFORT.md`.
- **Tested:** two blind rehearsals against independently written Addenda No. 3 (`rehearsals/blind-01/`, `rehearsals/blind-02/`), and a third (`rehearsals/blind-03/`) run with the AI layer in the loop (session 09): 31 hits, 3 partial, 0 missed of 34 scored items before the sealed key was opened; every derived date right; the deliberate ambiguity escalated, not resolved.
- **AI layer (session 09, `tenderpack/ai/`, `docs/AI_ROUTES.md`):** a model proposes through narrow tools; deterministic code validates, assigns every status, simulates the impact and writes to `staging/` only. Four routes: Claude Code and Codex over MCP or the CLI (the host's own model), the Anthropic API, OpenRouter and local Ollama (the application's calls, capped). Offline-tested with recorded responses; **no API-key call has been made** (the Anthropic, OpenRouter and Ollama routes are tested with recorded responses only; the Claude Code host route has run for real on the host's own plan since session 09, see `docs/AI_ROUTES.md` §8 and `worklog/model_calls/`; no key here), and nothing on the Mac has been measured. Codex: the MCP interface it would use is tested, but no Codex session has been run, so automated Codex execution is unverified (`docs/AI_ROUTES.md` §3). Ollama: tested only against a fake local server that replays recorded answers; the real runs on the owner's Mac are pending (`docs/MAC_SETUP.md`, the items marked PENDING ON THE MAC). Model choices and caps are configuration (`config/ai.yaml`); keys live in the environment only.
- **Session 12:** human-owned judgments never settled by the system (`tenderpack/human_owned.py`; HUMAN DECISION PENDING on proposals, issues, clarifications and the rendered A1/A3/A4); the unseen-addendum workflow finished (clause ranges, one replacement across a clause and its items, cover authority split from the body, superseded answers, the closed clarification window, image-table readings, computed deadlines, conditional and indirect effects, the CHANGED / CONFIRMED (unchanged) / NOT SETTLED labels from one function; bounded concurrency on the host route; consecutive addenda by `--base-run`); an explicit offline mode for every phase with the Mac setup (`docs/MAC_SETUP.md`, `scripts/mac/`); the local operating panel (`tenderpack panel`, `docs/PANEL.md`: 127.0.0.1 only, a token per start, real jobs, candidate outputs apart from the validated ones, decisions only through the recorded commands); the audit of the real submission through ADD-02 by six independent reviewers with its fixes and rechecks (`docs/session-12_report.md`); blind rehearsal 06, sealed and timed (55 min 49 s, two host sessions in flight; 20 hit / 14 partial / 1 missed of 35 before the key was opened); the labelled working-tree snapshot beside the clean-commit archive (`scripts/make_snapshot.py`).
- **Session 13:** the final improvements for the interview: an independent audit of the current outputs on the final code (three reviewers, four fixers, three recheck rounds; the maxima/range ambiguity of Table 2-4, the "at all times" reading and the compliance point now visible wherever they bear, every one HUMAN DECISION PENDING); the two named correctness gaps fixed (an anchor date rule with a counted period is refused; an analysis `row_new` is carried with an explicit reason), the applied-rule scope written into code, the run's code and policy identity recorded at start and resume; one runtime policy source delivered to every route and phase (`docs/RUNTIME_INSTRUCTIONS.md`) with the critical rules enforced by tool permissions and code; speed without weaker checks (submitted answers kept through 429 and SIGTERM, structure planning, collection as results arrive under one writer, concurrency measured; `scripts/bench_workflow.py`); the AI quick review (`tenderpack ai quick-review`, `docs/QUICK_REVIEW.md`: a preliminary, read-only, preserved briefing compared with the pipeline); the minimal interview folder for the Mac (`scripts/make_interview_folder.py`, the lock-based setup, the launcher's error paths, the checks that read exit codes, the routes' recorded status, keys outside chat and logs); the panel's A4 = the work log; the sealed blind-07 rehearsal (`docs/session-13_report.md` §8).

```
make setup      # once, needs network: creates .venv from uv.lock
make evidence   # rebuild build/ (the pack) and build/fixture/ (synthetic mixed example); offline
make test       # pytest
make verify     # tests + two clean rebuilds (Stage 1 and Stage 2) in disposable directories, compared
make outputs    # Stage 2: A1/A2/A3/A5 from build/ into out/
make drill      # synthetic Addendum No. 3 through the same path: build/drill-src, build/drill, out-drill/
make rehearsal  # drill B: a second synthetic Addendum No. 3, drafted then curated: out-drill-b/{src,build,out-drafted,out-curated}
python -m tenderpack ingest [--require-approved]                   # build; see exit codes below
python -m tenderpack outputs [--evidence build] [--out out]        # working draft; exit 0 published, 2 structural failure
python -m tenderpack outputs --strict                              # release: exit 3 (refused, previous out/ kept) while any blocker remains
python -m tenderpack check-register [--doc VOL-I]                  # dispositions, rows, evidence items, C15; exit 1 while findings remain
python -m tenderpack draft ADD-03 [--to FILE]                      # propose ops for an addendum (never applied by itself)
python -m tenderpack pin [--rows ROW@STAGE,...]                    # pin unpinned interpretations, or re-pin named ones after review
python -m tenderpack pin --migrate-format                          # format 1 -> 2 pins, only where nothing changed
python -m tenderpack check-register --update-ids                   # record new row ids in curation/register/ids.yaml (C12)
python -m tenderpack show "VOL-I:8.5#fn12"                         # a unit, its page and a highlighted crop
python -m tenderpack show VOL-I-8.6-01                             # an A1 row: pages, crops, amendment chain, A5 (also show/<ROW>/index.html)
python -m tenderpack diff [--from ADD-01] [--to ADD-02] [--md FILE]  # what an addendum changed: requirements, STALE, readings, A3, programme
python -m tenderpack approve VOL-IV-p6-r1 --reviewer "Your Name"   # a reading; run by the reviewer only
python -m tenderpack accept VOL-I-8.6-01 ADD-02/9.1 --reviewer "Your Name" [--note "..."]   # rows and ops; the reviewer only
python -m tenderpack reject ADD-02/8.1 --reviewer "Your Name" --note "what is wrong"         # a rejected op is withdrawn (addendum PARTIAL)
python -m tenderpack apply-proposal P-STALE-VOL-I-8.3-01 --by "Your Name"                   # a prepared STALE-row update; then accept/reject
```

**`ingest` exit codes.** `0`: structure OK; readings may still be pending, which is printed as PENDING HUMAN REVIEW and carried on every unit derived from them. `2`: STRUCTURAL FAILURE (any of checks C01–C10 failed, e.g. duplicate unit IDs, a span in two units, unit text that does not match its spans, an unread region), or an output path that was refused. The previous build is kept and the failed one is written to `<out>.failed`. `3`: structure OK, but readings are pending and `--require-approved` was given.

**Output safety.** `--out` may not be the repository, a parent of it, home, `/`, a protected folder (`sources`, `config`, `curation`, `tenderpack`, `tests`, `docs`, `worklog`, `.git`, `.venv`) or anything that contains or lies inside an input. An existing directory is replaced only if it is empty or a previous build (`.tenderpack-build` or `BUILD_MANIFEST.json`). Each build is written to a temporary sibling and swapped in only after it succeeds.

**Stage 2.** `outputs` reads a structurally OK evidence build, applies the op file of every addendum in number order (`curation/amendments/ADD-0N.yaml`; an addendum without one is drafted by `draft` and goes through the same engine), evaluates the register rows at every stage and writes A1–A5. An addendum with an invalid op or an unaccounted provision is **PARTIAL**: it never replaces the last validated state; A1 shows it as a WORKING column and its A5 goes to `out/a5/working/`. **Structural failures:**

- a quote that is not in the effective text;
- a scope leak;
- an A3 that does not fit one page at 7.5 pt or more;
- an A5 activity with no row in force;
- a needed deliverable with no activities and no justified exception (C44);
- an undefined dependency, lead time or role (C45).

On a structural failure nothing is published, the previous `out/` is kept and the candidate goes to `out.failed`.

**Working draft vs release.** Structurally checked does not mean reviewed. `outputs` publishes a WORKING DRAFT that lists its release blockers:

- **coverage:** PARTIAL addenda, units without a disposition, unlinked consequence words;
- **stale:** STALE interpretations;
- **approval:** readings pending, rows and ops without a person's decision bound to their current content.

`outputs --strict` refuses the release while any remains (exit 3; the candidate goes to `out.rejected` with `RELEASE_REJECTED.md`). The program never approves or accepts anything itself.

**Decisions on rows and ops.** `accept` and `reject` append to `curation/reviews/decisions.yaml` (it does not exist yet). Each decision is bound to a fingerprint of the item, its evidence items and its dependency values; when any of them changes, the decision shows as CHANGED and no longer counts. The `review:` fields in the YAML are drafting flags and never count.

**Approvals of readings.** Only a person approves, by running `approve` with their own name; placeholders such as `<name>` are refused, as are readings that fail their checks. An approval pins the review subject: the reading (content, uncertainties, source claims), and its evidence (source PDF, region position, native image). Any change to these makes the reading pending again. `--approvals PATH` writes to another file (used in tests); by default it is `curation/approvals.yaml`, which holds the owner's two approvals of the image readings (VOL-II-p3-r1 and VOL-IV-p6-r1, reviewer Ahmad, 3 Oct 2026, session 08); `build/coverage.md` shows both as approved.

| Path | Contents |
|---|---|
| `sources/candidate_pack/` | The six tender PDFs as received, unaltered (32 pages) |
| `sources/brief/` | The candidate brief as received |
| `sources/correspondence/` | Correspondence received and sent, as provided by the owner |
| `sources/manifest.json` | SHA-256, size and page count for every source file |
| `docs/PLAN.md` | Source findings and the engineering plan (revision 11) |
| `docs/session-03_before-after.md` | Short before/after report on the six gaps found in the owner's Stage 1 review |
| `docs/session-04_report.md` | Session 04: repair evidence, Stage 2 outputs, decisions needed |
| `docs/session-05_report.md` | Session 05: review fixes, working outputs, rehearsal results, remaining gaps, prioritised decisions |
| `docs/session-06_report.md` | Session 06: the four findings, the accept workflow, live commands, the blind rehearsal, the draft archive, decisions needed |
| `docs/session-08_report.md` | Session 08 before and after: the four findings, your confirmations, A1–A5, the clarification register, blind rehearsal 02, verification results, what remains for you |
| `docs/OPERATING_GUIDE.md`, `docs/VERIFY_ON_MAC.md`, `docs/COST_AND_EFFORT.md` | Operating guide (incl. the live-addendum procedure), offline verification on a Mac, cost and effort |
| `docs/session-09_report.md`, `docs/session-10_report.md`, `docs/session-11_report.md` | Session 09: controls and the AI layer, blind rehearsal 03. Session 10: the runnable workflow, blind rehearsal 04. Session 11: the workflow finished, blind rehearsal 05, the audit of the real package |
| `docs/session-12_report.md` | Session 12: what was asked and done, the models that ran, the rehearsals (blind-06 sealed and timed; blind-05 as a labelled post-key regression with a deliberate interruption), the audit through ADD-02 with its matrix, the decisions that need you in groups A–I, verification, runnable commands |
| `docs/session-13_report.md` | Session 13: what was asked and done, the models and settings that ran, the audit with its matrix and fixes, the correctness gaps and the runtime policy, speed, the AI quick review, the interview folder and the Mac checks, verification and the sealed blind-07 rehearsal, the decisions that need you in groups A–K, runnable commands |
| `docs/RUNTIME_INSTRUCTIONS.md` | The runtime policy the AI receives on every route and phase, generated from `tenderpack/ai/policy/`, with the table of where each critical rule is enforced (code, tool permissions, or prompt only) |
| `docs/QUICK_REVIEW.md` | The optional parallel AI quick review: what it reads, what it may never do, its labels, the comparison with the pipeline, the owner's answers and when they reach a run |
| `docs/PANEL.md`, `docs/MAC_SETUP.md` | The local operating panel (pages, rules, what was tested here, what is pending on the Mac); setting up and checking the Mac offline (`scripts/mac/setup.sh`, `checks.sh`, `launch.command`) |
| `docs/AI_ROUTES.md` | The AI layer: routes, what was run live and what was recorded (§8), the workflow, failure classes, the request layer |
| `worklog/` | **A4:** `README.md` (the index), one log per session with the owner's prompts verbatim, `subagent_briefs/` (every brief given to a subagent, verbatim), `model_calls/` (runtime model-call logs), the error index |
| `tenderpack/` | **The program.** Stage 1: extraction, regions, units, readings, review packets, coverage. Stage 2: citations, amend, draft, dates, register, schedule, render, stage2. Stages 3–4: dispositions (and sweeps), evidence (item vocabulary), programme (documents, resources, drivers, scenarios) |
| `config/` | Pack definition, declared furniture rules, planning assumptions (`assumptions.yaml`: calendar, counting policy, bidder, copies, resources, lead times with basis and owner, all PROVISIONAL), A5 scenarios (`scenarios.yaml`) |
| `curation/readings/` | The two image readings (Table 2-4, Form 4-C), approved by the owner on 3 Oct 2026 in `curation/approvals.yaml` (transcriptions and displayed translations; interpretations stay proposed); any later change makes a reading pending again |
| `curation/amendments/` | Op files for ADD-01 and ADD-02 (proposed ops and dispositions; every provision accounted for) |
| `curation/register/` | **The A1 register:** `rows.yaml` (core rows; includes `rows/*.yaml` per volume), unit dispositions (`dispositions/*.yaml`), open issues (`issues.yaml`, `issues/*.yaml`), machine-written pins (`pins.yaml`), the row-id ledger (`ids.yaml`), prepared proposals not yet applied (`proposals/`) |
| `curation/evidence_items/` | The evidence-item vocabulary: envelope, issuer, multiplicity, counted |
| `curation/activity_templates.yaml` | Evidence item → A5 activities (owner, issuer, duration key, dependencies, resource role) |
| `build/` | Generated evidence: `units.md`, `coverage.md`, `exclusions.md`, `review/<region>/packet.html` (crops beside readings; also `.md`), `fixture/`, `drill/` and `drill-src/` (ADD-03 drill) |
| `out/` | **Working outputs:** `a1/` (xlsx, csv, json); `a2/` (md, csv, json, including the C28 cover-summary check); `a3/a3.pdf` with `a3_detail.html`; `a5/` (programme, marshalling, documents, resources, drivers, replan deltas, scenario comparison and `scenarios/`); `review/` (the owner's review batches: crops beside readings and quotes, the exact decisions; `packets/` holds the full packets of both image readings); `checks.json` (structural checks and release blockers); `README.md` |
| `out-drill/` | The same outputs for the pack plus the synthetic ADD-03 (PARTIAL; validated state stays ADD-02) |
| `out-drill-b/` | Drill B rehearsal: the drill pack (`src/`), its evidence (`build/`), outputs with ADD-03 drafted (`out-drafted/`, PARTIAL) and curated (`out-curated/`, APPLIED). No review of any kind |
| `rehearsals/blind-01/` | Blind rehearsal: an independently written Addendum No. 3, its frozen and sealed answer key, the curation, outputs and `COMPARISON.md` (score and timeline) |
| `rehearsals/blind-03/`, `blind-04/`, `blind-05/` | Blind rehearsals 03–05: independently written Addenda No. 3 with sealed keys, run with the AI layer (03), the workflow (04) and the session-11 workflow (05); each with `FROZEN.md`, `COMPARISON.md` and the scored outputs |
| `rehearsals/blind-06/` | Blind rehearsal 06 (session 12): an independently written Addendum No. 3 (and a short No. 4, not run on the owner's instruction) with a sealed key, run on the frozen session-12 tree with two host sessions in flight; `FROZEN.md`, `FROZEN-OUTPUTS.md`/`.sha256` (the first outputs frozen by hash before the key was opened), `SEALED/`, `COMPARISON.md` (detection, usable updates, missed effects, pending decisions, interventions and time, each counted separately) |
| `rehearsals/blind-02/` | Blind rehearsal 02: a second independently written Addendum No. 3 (time moved on the same date, revocation, re-lettering, notes that amend), curated through the normal pipeline; `COMPARISON.md` scores it against the sealed key |
| `scripts/` | `make_draft_archive.py` (the A1–A5 draft archive from a clean commit; every rehearsal with a `COMPARISON.md` included), `make_snapshot.py` (the labelled working-tree snapshot: base revision, uncommitted changes disclosed, manifest), `compare_outputs.py` (rebuilt outputs vs an archive), `mac/` (the Mac setup, checks and launcher) |
| `tests/` | Tests, golden expectations written from the rendered pages, synthetic fixture builder |
| `worklog/` | Timestamped development log: prompts, actions, errors and corrections |
