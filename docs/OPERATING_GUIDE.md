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

Times are from the blind rehearsals (`rehearsals/blind-01/COMPARISON.md`, `rehearsals/blind-02/COMPARISON.md`, `rehearsals/blind-03/COMPARISON.md`): 12 and 32 minutes from receipt to replanned outputs, curated by the assistant (rehearsal 02 had 31 ops, 8 new rows and 42 re-made readings; about 10 of its minutes were an interruption), and 50 minutes with the AI layer in the loop (rehearsal 03: 13 of them the model's proposal run, 26 the curation of 27 ops, 12 new rows and 32 re-made readings; §6). Your own review time comes on top (about 2–2½ hours for rehearsal 03's output, estimated).

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
4. **Curate.** Copy the draft to `curation/amendments/ADD-03.yaml`, then treat every unresolved provision:
   - write an op, or a `no_effect` with a reason;
   - add rows for new obligations (C46 lists any that are missing);
   - re-make the interpretations of rows whose quoted words changed;
   - add issues for what a person must decide;
   - read the C28 findings (A2, `diff`): the cover summary is never applied, and a difference may need a clarification;
   - do not trust C28 alone: since session 09 it tests "X is unchanged" sentences against the ops and matches validity claims through the register's date rules (both missed in rehearsal 02), but it is a report, never a gate. Read the cover against the provisions yourself;
   - choosing a consequence class: a stated refusal of a submitted document ("will not be accepted", "treated as not submitted") whose effect on the Proposal is not stated is `document_refusal`, quoting the refusal. A3 lists it under "Document refused" and the row keeps its place in the VOL-I 11.1(i) gate; it is never shown as a disqualification. Zero marks under one scoring criterion is `criterion_zero`: a scored consequence, listed on A3 apart from the threshold; state any threshold risk in the row's note. `score_elimination` means falling below the VOL-I 11.3 threshold (Envelope B returned unopened), not a zero on one criterion. Neither case is `lesser`;
   - after adding a not-yet-issued unit to an existing row, re-pin that row's earlier readings by name (`pin --rows ROW@STAGE`); otherwise they show STALE at stages where the unit did not exist;
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

## 6. The AI layer (session 09)

The system still runs without a model: every reviewed output above is produced offline. When a model is used, it proposes and never decides: `docs/AI_ROUTES.md` gives the commands for each route (Claude Code or Codex over MCP/CLI with their own model; the Anthropic API, OpenRouter or local Ollama with the application's capped calls), what is recorded versus live, and the credential rules (environment only). A run ends in `staging/ai/<run_id>/review_request.md`; `tenderpack ai promote RUN_ID --by "Your Name"` copies the verified items into curation as PROPOSED drafts, and the decisions of §4 still follow. Nothing in `staging/` is applied or published.
