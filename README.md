# tender-pack-reader

Working repository for the Lamar Holding PPP AI Partner Round 2 assessment.

**Status (session 05, `docs/PLAN.md` revision 5):**

- **Stage 1** (evidence and units): implemented, and revised after the owner's reviews.
- **Stage 2:** the amendment path for ADD-01, ADD-02 and any future addendum. The owner's five code-review findings were fixed in session 05.
- **Stage 3** (full register: dispositions for every unit, 202 A1 rows, English and Arabic consequence sweeps) and **Stage 4** (A5 for both envelopes with counts, issuers, resources, infeasibility drivers and scenarios): built as **working drafts**.
- Every row, op, disposition and lead time is a **proposal, not reviewed by a person**. Both image readings are **pending the owner's review**, and nothing has been approved.
- A strict release (`outputs --strict`) is refused in this state.
- Packaging and final submission (Stage 6) have not started.

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
python -m tenderpack show "VOL-I:8.5#fn12"                         # a unit, its page and a highlighted crop
python -m tenderpack approve VOL-IV-p6-r1 --reviewer "Your Name"   # run by the reviewer only
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
- **approval:** readings pending, rows and ops not accepted by a person.

`outputs --strict` refuses the release while any remains (exit 3; the candidate goes to `out.rejected` with `RELEASE_REJECTED.md`). The program never approves or accepts anything itself.

**Approvals.** Only a person approves, by running `approve` with their own name; placeholders such as `<name>` are refused, as are readings that fail their checks. An approval pins the review subject: the reading (content, uncertainties, source claims), and its evidence (source PDF, region position, native image). Any change to these makes the reading pending again. `--approvals PATH` writes to another file (used in tests); by default it is `curation/approvals.yaml`, which does not exist yet.

| Path | Contents |
|---|---|
| `sources/candidate_pack/` | The six tender PDFs as received, unaltered (32 pages) |
| `sources/brief/` | The candidate brief as received |
| `sources/correspondence/` | Correspondence received and sent, as provided by the owner |
| `sources/manifest.json` | SHA-256, size and page count for every source file |
| `docs/PLAN.md` | Source findings and the engineering plan (revision 5) |
| `docs/session-03_before-after.md` | Short before/after report on the six gaps found in the owner's Stage 1 review |
| `docs/session-04_report.md` | Session 04: repair evidence, Stage 2 outputs, decisions needed |
| `docs/session-05_report.md` | Session 05: review fixes, working outputs, rehearsal results, remaining gaps, prioritised decisions |
| `tenderpack/` | **The program.** Stage 1: extraction, regions, units, readings, review packets, coverage. Stage 2: citations, amend, draft, dates, register, schedule, render, stage2. Stages 3–4: dispositions (and sweeps), evidence (item vocabulary), programme (documents, resources, drivers, scenarios) |
| `config/` | Pack definition, declared furniture rules, planning assumptions (`assumptions.yaml`: calendar, counting policy, bidder, copies, resources, lead times with basis and owner, all PROVISIONAL), A5 scenarios (`scenarios.yaml`) |
| `curation/readings/` | Proposed readings of image regions, pending review; approvals go in `curation/approvals.yaml` |
| `curation/amendments/` | Op files for ADD-01 and ADD-02 (proposed ops and dispositions; every provision accounted for) |
| `curation/register/` | **The A1 register:** `rows.yaml` (core rows; includes `rows/*.yaml` per volume), unit dispositions (`dispositions/*.yaml`), open issues (`issues.yaml`, `issues/*.yaml`), machine-written pins (`pins.yaml`) |
| `curation/evidence_items/` | The evidence-item vocabulary: envelope, issuer, multiplicity, counted |
| `curation/activity_templates.yaml` | Evidence item → A5 activities (owner, issuer, duration key, dependencies, resource role) |
| `build/` | Generated evidence: `units.md`, `coverage.md`, `exclusions.md`, `review/<region>/packet.html` (crops beside readings; also `.md`), `fixture/`, `drill/` and `drill-src/` (ADD-03 drill) |
| `out/` | **Working outputs:** `a1/` (xlsx, csv, json); `a2/` (md, csv, json); `a3/a3.pdf` with `a3_detail.html`; `a5/` (programme, marshalling, documents, resources, drivers, replan deltas, scenario comparison and `scenarios/`); `checks.json` (structural checks and release blockers); `README.md` |
| `out-drill/` | The same outputs for the pack plus the synthetic ADD-03 (PARTIAL; validated state stays ADD-02) |
| `out-drill-b/` | Drill B rehearsal: the drill pack (`src/`), its evidence (`build/`), outputs with ADD-03 drafted (`out-drafted/`, PARTIAL) and curated (`out-curated/`, APPLIED). No review of any kind |
| `tests/` | Tests, golden expectations written from the rendered pages, synthetic fixture builder |
| `worklog/` | Timestamped development log: prompts, actions, errors and corrections |
