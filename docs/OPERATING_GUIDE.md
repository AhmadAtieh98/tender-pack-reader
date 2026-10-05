# Operating guide (draft handover)

**Purpose.** `tenderpack` reads the tender pack (VOL-I, VOL-II, VOL-IV, VOL-V, ADD-01, ADD-02 and any later addendum) and produces A1–A5:

- A1: the compliance register;
- A2: the addendum reconciliation;
- A3: the one-page disqualification sheet;
- A4: the work log (repository history);
- A5: the programme and marshalling plan.

**How it runs.** Offline and deterministic: the same inputs give byte-identical outputs. The program never approves or accepts anything. Legal and commercial calls stay with people.

## 1. Set up (once)

Two ways to set it up:

- **With network:** `make setup`. This runs `uv sync --extra dev` from `uv.lock`.
- **Offline:** use the wheelhouse (`VERIFY_ON_MAC.md` §3, option B).

Python 3.11 or later.

## 2. Build everything

```
make evidence    # Stage 1: units, checks C01–C10, review packets          -> build/
make outputs     # A1/A2/A3/A5 working draft + review batches               -> out/
make test        # the test suite (about 6 minutes)
make verify      # two clean rebuilds in disposable folders, compared byte for byte
```

**Exit codes:**

| Code | Meaning |
|---|---|
| 0 | Published (a WORKING DRAFT that lists its release blockers) |
| 2 | Structural failure. Nothing is published; the previous output is kept and the candidate is in `<out>.failed` |
| 3 | `--strict` release refused while any blocker remains |

## 3. When a new addendum arrives (the live session)

Times are from the blind rehearsals (`rehearsals/blind-01/COMPARISON.md`, `rehearsals/blind-02/COMPARISON.md`, `rehearsals/blind-03/COMPARISON.md`): 12 and 32 minutes from receipt to replanned outputs, curated by the assistant (rehearsal 02 had 31 ops, 8 new rows and 42 re-made readings; about 10 of its minutes were an interruption), and 50 minutes with the AI layer in the loop (rehearsal 03: 13 of them the model's proposal run, 26 the curation of 27 ops, 12 new rows and 32 re-made readings; §6). Rehearsal 04 ran the whole path without a curator (`tenderpack ai run`, session 10): 46 minutes to candidate outputs and a review packet, 39 of them host sessions, with the downstream rows still a person's work (`rehearsals/blind-04/COMPARISON.md`). Your own review time comes on top (about 2–2½ hours for rehearsal 03's output, 2–3 hours for rehearsal 04's candidate, estimated).

1. **Add the PDF.** Put it in `sources/candidate_pack/`. Add a `documents:` entry (`doc_id: ADD-03, kind: addendum, number: 3`) to `config/pack.yaml` and its sha256 and page count to `sources/manifest.json`.
2. **Ingest.** Run `make evidence`; it takes 13 s. A structural failure stops here and says why (layout, furniture, an unread image).
3. **Draft and look.** These take seconds:
   ```
   python -m tenderpack draft ADD-03 --to /tmp/ADD-03.draft.yaml
   python -m tenderpack outputs
   python -m tenderpack diff
   ```
   - `draft` proposes ops. Anything it cannot type is listed as **unresolved**.
   - `outputs` publishes a working draft. The addendum is PARTIAL and the validated state stays on the previous addendum.
   - `diff` says what changed: requirements, STALE rows, image-read values, disqualifiers, programme.
   - While the addendum is PARTIAL, `outputs` also writes the **candidate** A3 and A5 beside the validated ones (session 11): `out/a3/a3_candidate.pdf` (with `.md`, `.html` and `.json`) and `out/a5/candidate/`. They show what the addendum would do if every valid op stood: the rows that would enter, leave or change on A3, each with its op and status; the A5 dates that would move and the rows and ops that move them; the activities marked REVIEW through relationships; the activities BLOCKED because a row they serve is unresolved; the blockers (unresolved provisions with their reasons, STALE rows, C46 gaps, documents not supplied such as the Environmental Permit, conflicts); conditional scenarios with a decision milestone at the trigger deadline; and the image-read units the addendum touches, beside their review packets. Every page says CANDIDATE — NOT VALIDATED, and the candidate A3 may run to several pages (the one-page rule applies to the validated A3 only). Nothing validated changes: `a3/a3.pdf` and `a5/` stay on the previous addendum, byte for byte. `diff` and the AI workflow's review packet point to both and say in one paragraph what may be changing.
4. **Curate.** Copy the draft to `curation/amendments/ADD-03.yaml`, then treat every unresolved provision:
   - write an op, or a `no_effect` with a reason;
   - add rows for new obligations (C46 lists any that are missing);
   - re-make the interpretations of rows whose quoted words changed;
   - add issues for what a person must decide;
   - read the C28 findings (A2, `diff`): the cover summary is never applied, and a difference may need a clarification;
   - do not trust C28 alone: since session 09 it tests "X is unchanged" sentences against the ops and matches validity claims through the register's date rules (both missed in rehearsal 02), but it is a report, never a gate. Read the cover against the provisions yourself;
   - choosing a consequence class: a stated refusal of a submitted document ("will not be accepted", "treated as not submitted") whose effect on the Proposal is not stated is `document_refusal`, quoting the refusal. A3 lists it under "Document refused" and the row keeps its place in the VOL-I 11.1(i) gate; it is never shown as a disqualification. Zero marks under one scoring criterion is `criterion_zero`: a scored consequence, listed on A3 apart from the threshold; state any threshold risk in the row's note. `score_elimination` means falling below the VOL-I 11.3 threshold (Envelope B returned unopened), not a zero on one criterion. Neither case is `lesser`;
   - after adding a not-yet-issued unit to an existing row, re-pin that row's earlier readings by name (`pin --rows ROW@STAGE`); otherwise they show STALE at stages where the unit did not exist;
   - a row marked `removed: {by: <op>}` must quote words that op deleted: if the quoted words are still in the unit after the op, check-register reports "the row's words survive the op" and the row stays in force (session 10);
   - a new row for an obligation the addendum creates in a unit that existed before (an answer, or new words in a volume clause) says where it comes into force (session 11): `introduced: {stage: ADD-03, by: <the op id, or the provision unit>, evidence: {unit: <the provision, or a unit its op changed>, page: N, words: "<verbatim, new at that stage>"}}`. Before that stage the row is NOT IN FORCE (no reading needed, never STALE, off A3 and A5); at it, NEW (introduced by …). The claim is checked: the op is applied at that stage (or the provision is that addendum's), the words are printed there and were not there before, and no reading is made earlier; a claim that fails is a C16 finding and the row is then read without it. A row without the field is in force from the stage its first unit is issued in, as before (check-register reports how many rows are explicit and how many derived). Putting the addendum's provision first in `units` remains a convention; it is not the evidence;
   - read the "Reached through relationships" part of `diff` (and A2): rows, activities and calculations reached through another provision (§7);
   - update `config/assumptions.yaml` when a pack fact in it changed (e.g. the number of copies).
5. **Check.** Run each of these; every one must be clean:
   ```
   python -m tenderpack pin                           # pins the NEW interpretations only
   python -m tenderpack check-register --update-ids   # 0 findings; new row ids recorded
   python -m tenderpack outputs                       # ADD-03 APPLIED; C30/C46 clean
   python -m tenderpack diff --md /tmp/diff.md
   ```
6. **Look at any row.** `python -m tenderpack show VOL-I-8.6-01` prints the source pages, crops, amendment chain and A5 activities, and writes `show/VOL-I-8.6-01/index.html`.
7. **Release.** `python -m tenderpack outputs --strict` refuses to release until three things hold:
   - coverage is complete;
   - no row is STALE;
   - every reading, row and op carries your decision.

### 3a. If a run is interrupted, rate-limited or the machine restarts (session 11)

Nothing is lost: every step and batch is checkpointed under `staging/ai/runs/<run>/checkpoint.json`. Run
`python -m tenderpack ai resume <run>`; batches that succeeded are never asked again, a batch the plan's rate limit
deferred (exit 5, "DEFERRED") is asked again, and the steps after the last done batch are recomputed. A run that
stops because it cannot go on by itself exits 6 (session 12): an image region without a usable reading, readings
escalated to a person, or inputs changed before promotion. Do what its reason says, then `resume`. A run killed
mid-batch (a crash, a container restart) leaves its locks behind; `resume` takes over the run lock and the
addendum's staging lock when their process is no longer running on this machine and records the takeover; a lock
held by a live process is still refused, and an old lock without a dead process needs a person
(`--break-lock --by "Your Name"`). After a code change, `ai resume <run> --from <step>` reruns that step and the
later ones without asking any done batch again (proposals made against another state identity are still refused at
promotion). The clock of a rehearsal records every interruption (`rehearsals/blind-04/clock-s11.txt` is an example
with a restart and a rate limit).

### 3b. Two addenda in a row (session 12)

When Addendum No. 4 arrives before Addendum No. 3 is accepted into `curation/`, run No. 3 first and start No. 4 on its
candidate: `python -m tenderpack ai run ADD-04 --pdf PATH --base-run <the ADD-03 run>`. The ADD-04 candidate then starts
from the ADD-03 candidate (its op file, rows, readings, issues, clarifications, relationships, pins, its pack with
ADD-03's PDF and its evidence build), so ADD-03 is ADD-04's previous stage, ADD-04's references to clauses ADD-03
inserted resolve, A2 shows the chain ADD-03 → ADD-04, and the review compares with the ADD-03 candidate state, not
the real `out/`. The ADD-03 run must have reached promotion and must not be running; it is only read (its folder is
unchanged), and `--pack`/`--evidence` are not given with `--base-run`. Remember that the base is itself unreviewed:
everything ADD-04 builds on is still PROPOSED. If the ADD-03 candidate changes afterwards (a person edits it, or it
is rerun), the ADD-04 sets become STALE and promotion refuses: start a new ADD-04 run. `run-status`, the review
packet and the candidate README name the base; `resume <run> --base-run <base>` checks you are resuming on the base
the run was started with. Without `--base-run`, ADD-04 runs on the real curation: the run warns "ADD-03 is not in
this state; run it first or pass --base-run", and every provision that cites ADD-03 and cannot be answered is left
unresolved with that reason.

## 4. Reviewing: the owner's decisions

Open `out/review/index.html` and work through the batches in order:

1. **Image readings.** Batch 1 shows each unit's crop beside its reading. `out/review/packets/` has the full packets: every band, cell and numeral at native resolution, with the Arabic right to left. Approve a reading only after comparing every crop with what is read beside it:
   `python -m tenderpack approve VOL-II-p3-r1 --reviewer "Your Name" --record "where your confirmation is written" [--resolution "..."] [--keeps-open "..."] [--not-covered "..."]`.
   Or correct `curation/readings/<region>.yaml` and run `make evidence`.
   - The approval is dated the day the command runs (never backdated). It pins the review subject (reading + evidence) and records the reading file's sha256, its last commit and a snapshot (`curation/reading-snapshots/`).
   - If a reading changes after an approval, it is pending again. `approve` then prints every meaningful difference from the approved snapshot and writes nothing until it is run again with `--confirm-changes`.
   - **Status (3 Oct 2026):** both readings carry the owner's confirmations (`curation/approvals.yaml`): they cover the transcriptions only, not the register's interpretations, the amendment ops or bidder compliance; the Table 2-4 entry records that the Permit confirmation covers only where the precedence language is, not the Permit's contents or compliance.
2. **Disqualifiers (A3 rows), amendment ops, remaining rows.** Decide each one:
   ```
   python -m tenderpack accept VOL-I-8.6-01 ADD-02/9.1 --reviewer "Your Name" [--note "..."]
   python -m tenderpack reject ADD-02/8.1 --reviewer "Your Name" --note "what is wrong"
   ```
   - A decision on a row binds to the row, its evidence items, where its units are printed and its dependencies. A decision on an op binds to the op and its *subject*: its provision's text, pages and evidence, and every unit it reads or changes (every member row of a replaced table or form, and of the replacement) as they stand immediately before the op, whether or not it then applies.
   - If any of these changes later (e.g. a new addendum), the decision is shown as CHANGED and no longer counts as an acceptance.
   - A rejected op is **withheld** for as long as your latest decision on it is a rejection, even after a rebuild or a change (shown "CHANGED: review again; still withheld"). Its provision shows as `rejected` and the addendum stays PARTIAL. Withheld (your rejection), invalid (a failed structural check) and proposed (pending your review) are three separate states.
   - A name that identifies the assistant or the program is refused for any decision or approval.
3. **STALE rows and proposals.** Prepared proposals are in `curation/register/proposals/`:
   `python -m tenderpack apply-proposal P-... --by "Your Name"`, then accept or reject the row. A proposal marked `superseded` keeps its text and the reason (`superseded_because`) and cannot be applied. On 3 Oct 2026 the three session 06 proposals (VOL-I 8.3, 3.4, 6.7) were superseded by `P-S08-*` proposals written from the owner's direction with their source evidence; those were applied on the owner's written instruction, and the three rows are PROPOSED until you decide them.
4. **Clarification questions.** `curation/clarifications/register.yaml` holds DRAFT questions (never sent by the program) for discrepancies, ambiguities and missing information in the volumes and addenda; `out/a4/clarification_register.md` lists them with sources, impact and interim handling, and the questions closed without one. A3 lists their ids by group. `check-register` verifies every quotation. Raise what you decide through the Portal before the VOL-I 5.2 cut-off.

The `review:` fields in the YAML files are drafting flags. They never count.

## 5. What each check means

| Check | Meaning |
|---|---|
| C01–C10 | Every page, span, image region and unit is accounted for in the evidence |
| C12 | Row ids never disappear (`curation/register/ids.yaml`) |
| C13 / C43 | A3 holds only explicit, quoted consequences, on one page at 7.5 pt or more, condensed in stated steps if needed |
| C15 | Every consequence word, English and Arabic, is linked |
| C16 | Every quote is in the effective text |
| C20–C27 | Every provision is treated; each op is valid (quotes, targets, scope) |
| C25 / C47 | Nothing changes without an op; every added word is printed by the addendum |
| C28 | Each addendum's cover summary is compared with its provisions (tables, notes, appendices, answers): omissions, understatements, unmentioned consequences, contradictions. Report only (A2, A1 Issues, `diff`): the summary is never applied |
| C30 | Every date or period phrase is planned, or explicitly not computed |
| C40 / C44 / C45 | A5 activities and deliverables, both ways; dependencies defined |
| C46 | Every new or amended obligation reaches A1, A3 and A5; an insertion needs a row of its own (the anchor's rows do not count) |
| check-register `relationship` | Every relationship is well formed: its ends exist, a confirmed link quotes the documents verbatim on the stated page, a proposed or possible one states its basis (§7) |

## 6. The AI layer (session 09)

The system still runs without a model: every reviewed output above is produced offline. When a model is used, it proposes and never decides: `docs/AI_ROUTES.md` gives the commands for each route (Claude Code or Codex over MCP/CLI with their own model; the Anthropic API, OpenRouter or local Ollama with the application's capped calls), what is recorded versus live, and the credential rules (environment only). A run ends in `staging/ai/<run_id>/review_request.md`; `tenderpack ai promote RUN_ID --by "Your Name"` copies the verified items into curation as PROPOSED drafts, and the decisions of §4 still follow. Nothing in `staging/` is applied or published.

### 6a. Offline on the Mac (session 12)

On the owner's Mac, `docs/MAC_SETUP.md` covers the one-time setup (`bash scripts/mac/setup.sh`), the double-click
launcher (`scripts/mac/launch.command`) and the offline checks (`bash scripts/mac/checks.sh`, with Wi-Fi off). After
setup, `ingest`, `outputs`, `outputs --strict` and `check-register` need neither internet nor a key.

Local AI runs only in **offline mode**: `--offline`, `offline: true` in `config/ai.yaml`, or `TENDERPACK_OFFLINE=1`.
In that mode every phase uses the local Ollama, and a hosted route is refused before any call (`docs/AI_ROUTES.md` §17).

```
.venv/bin/python -m tenderpack ai routes --offline                      # each route's kind; local models checked; nothing pulled
.venv/bin/python -m tenderpack ai run ADD-03 --pdf PATH --offline       # every phase on the local ollama route
.venv/bin/python -m tenderpack ai resume RUN_ID --offline
.venv/bin/python -m tenderpack ai run-status RUN_ID
```

What to expect from an offline run:

- **Model not installed.** A missing local model stops the run with the `ollama pull` command you may run yourself.
- **Readings.** A reading model without vision escalates the image regions to you.
- **Critic.** The critic runs on `routes.ollama.models.critic`, or the review packet says "independent review did not
  run" with the reason.
- **Checks on the Mac.** These checks are tested here with a fake local server only; on your Mac they are pending
  (`docs/MAC_SETUP.md` lists them).

## 7. Relationships: effects through other provisions (session 10)

A row cites the units its own words are in, so `diff` used to report only rows that cite a changed unit. Effects that run through another provision (who is a member reaching every per-member form and the weighted financial standing; an effluent limit reaching the reliability run and the contract's Unavailability Event; the payment mechanism reaching the quoted price, Form 4-F and the Financial Model; a schedule the pack does not supply) are curated once in `curation/relationships.yaml` (a rehearsal pack keeps its own copy in its `work/` folder). `diff`, A2, A3 (the "Referenced but not supplied" group and `a3_detail.html`), A1 (a Relationships column and sheet) and A5 follow them, in three classes that are never merged with the direct changes: **confirmed dependency**, **proposed relationship**, **possible impact**. Reached A5 activities are flagged `REVIEW (<class>)`; their dates do not move.

To add one, append an entry: `id`, `from` (a row or unit id; a table id also stands for its rows; `calc:<name>`; or `words:<phrase>`), `to` (a row, unit, activity, evidence item, date rule or `calc:<name>`), `kind` (`cites`, `depends_on`, `feeds_calculation`, `member_scope`, `limit_applies`, `missing_document`), `status`, `origin`, `review: proposed`. **Confirmed** means the documents themselves state the link: the entry quotes the cross-reference verbatim in `evidence: [{unit, page, words}]`, and check-register checks it. Anything inferred, by you or a model, is **proposed** (or **possible**) with a `basis` saying why. A `missing_document` entry also names the `document`, a short `document_id` and the conclusion it `blocks`. A model's proposals are landed by `tenderpack.relationships.append_proposed` as proposed; the program never promotes a link to confirmed, and a model's link marked confirmed needs your name in `confirmed_by`. Run `check-register` after any change.

## 8. Handing over: the release archive and the working-tree snapshot (session 12)

Two packages, two purposes:

- `python scripts/make_draft_archive.py DEST [--wheels WHEELHOUSE]` builds the DRAFT handover archive from a clean
  commit and refuses a dirty tree, so that the archive equals a commit (`LAMAR-PPP-R2-DRAFT_<sha>.zip`). It takes
  every blind rehearsal that has a `COMPARISON.md` (session 12: no more hardcoded list) and every session report.
- `python scripts/make_snapshot.py DEST [--label TEXT] [--exclude PREFIX ...]` builds a labelled WORKING-TREE
  SNAPSHOT of the tree as it is, uncommitted changes included: `LAMAR-PPP-R2-SNAPSHOT_<base-sha>+wt_<UTC stamp>/`
  with `SNAPSHOT.md` (the base revision and branch, the `git status` disclosure of every changed and untracked path,
  the diff statistics, the dependency pins of the packaged `pyproject.toml`), `uncommitted.patch`, `MANIFEST.sha256`
  and the files a commit would capture. It is for reviewing work the owner has deliberately left uncommitted; it is
  not a release and says so on its first line. Verify with `shasum -a 256 -c MANIFEST.sha256`.

Both exclude the ignored rebuildable parts of staged runs (`.gitignore`). The snapshot excludes
`staging/ai/runs/_cache/` by default.

## 9. The local operating panel (session 12)

`python -m tenderpack panel --open` (or item 7 of `scripts/mac/launch.command`) starts a plain page on this machine
only: it listens on 127.0.0.1, on a free port unless `--port N` is given, and prints its address once,
`http://127.0.0.1:<port>/t/<token>/`, with a new token at every start (keep it to yourself; without it every request
is refused). It is an operating panel, not a replacement for the deliverables: A1–A5 stay in `out/`. Every button runs
the same command you would type (shown on each job's page, to repeat in a terminal) as a job with its log under
`staging/panel/jobs/`: ingest, outputs, the strict check, check-register, `diff` between stages (BASE, ADD-01, ADD-02
and any candidate run), `ai run` from an uploaded PDF (stored as `staging/panel/uploads/<sha256>.pdf`), `ai resume`.
The run pages keep execution, completeness, structural validation and human approval apart; a candidate's outputs are
opened in place under a CANDIDATE banner and never copied into `out/`. The Decisions page lists every pending item with
its exact `accept`/`reject`/`approve` command; the panel runs one only after you choose the decision, type your name
and a reason, and tick the confirmation. Ctrl-C stops the panel; a job it started keeps running (resume a run later
from the Runs page). Details, the safety rules and what is still to be checked on the Mac: `docs/PANEL.md`.
