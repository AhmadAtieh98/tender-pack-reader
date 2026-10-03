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

Times are from the blind rehearsal (`rehearsals/blind-01/COMPARISON.md`). Total: 12 minutes from receipt to replanned outputs, curated by the assistant. Your own review time comes on top.

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

1. **Image readings.** Approve a reading only after comparing every crop with what is read beside it:
   `python -m tenderpack approve VOL-II-p3-r1 --reviewer "Your Name"`.
   Or correct `curation/readings/<region>.yaml` and run `make evidence`.
2. **Disqualifiers (A3 rows), amendment ops, remaining rows.** Decide each one:
   ```
   python -m tenderpack accept VOL-I-8.6-01 ADD-02/9.1 --reviewer "Your Name" [--note "..."]
   python -m tenderpack reject ADD-02/8.1 --reviewer "Your Name" --note "what is wrong"
   ```
   - A decision binds to the fingerprint of the item, its evidence items and its dependencies.
   - If any of these changes later (e.g. a new addendum), the decision is shown as CHANGED and no longer counts.
   - A rejected op is withdrawn and its addendum becomes PARTIAL.
3. **STALE rows.** The prepared proposals are in `curation/register/proposals/`:
   `python -m tenderpack apply-proposal P-STALE-VOL-I-8.3-01 --by "Your Name"`, then accept or reject the row.

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
| C30 | Every date or period phrase is planned, or explicitly not computed |
| C40 / C44 / C45 | A5 activities and deliverables, both ways; dependencies defined |
| C46 | Every new or amended obligation reaches A1, A3 and A5 |

## 6. Deferred, as directed

The Claude Code app, OpenRouter and Ollama integrations. The system runs without a model.
