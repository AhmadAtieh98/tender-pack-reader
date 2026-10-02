# tender-pack-reader

Working repository for the Lamar Holding PPP AI Partner Round 2 assessment.

**Status:** Stage 1 (evidence and units) implemented and revised after the owner's reviews (sessions 03 and 04). **Stage 2, a thin end-to-end slice** (session 04): the amendment path for ADD-01, ADD-02 and any future addendum, and first connected versions of A1, A2, A3 and A5 for **26 representative rows, not the full register**. Every interpretation and amendment op is a **proposal, not reviewed by a person**; both image readings are **pending the owner's review**; nothing has been approved. Stages 3–6 of `docs/PLAN.md` (revision 4) are **proposed**.

```
make setup      # once, needs network: creates .venv from uv.lock
make evidence   # rebuild build/ (the pack) and build/fixture/ (synthetic mixed example); offline
make test       # pytest
make verify     # tests + two clean rebuilds (Stage 1 and Stage 2) in disposable directories, compared
make outputs    # Stage 2: A1/A2/A3/A5 from build/ into out/
make drill      # synthetic Addendum No. 3 through the same path: build/drill-src, build/drill, out-drill/
python -m tenderpack ingest [--require-approved]                   # build; see exit codes below
python -m tenderpack outputs [--evidence build] [--out out]        # Stage 2 outputs; exit 0 published, 2 structural failure
python -m tenderpack draft ADD-03 [--to FILE]                      # propose ops for an addendum (never applied by itself)
python -m tenderpack pin                                           # pin interpretations to their dependencies
python -m tenderpack show "VOL-I:8.5#fn12"                         # a unit, its page and a highlighted crop
python -m tenderpack approve VOL-IV-p6-r1 --reviewer "Your Name"   # run by the reviewer only
```

**`ingest` exit codes.** `0`: structure OK; readings may still be pending, which is printed as PENDING HUMAN REVIEW and carried on every unit derived from them. `2`: STRUCTURAL FAILURE (any of checks C01–C10 failed, e.g. duplicate unit IDs, a span in two units, unit text that does not match its spans, an unread region), or an output path that was refused. The previous build is kept and the failed one is written to `<out>.failed`. `3`: structure OK, but readings are pending and `--require-approved` was given.

**Output safety.** `--out` may not be the repository, a parent of it, home, `/`, a protected folder (`sources`, `config`, `curation`, `tenderpack`, `tests`, `docs`, `worklog`, `.git`, `.venv`) or anything that contains or lies inside an input. An existing directory is replaced only if it is empty or a previous build (`.tenderpack-build` or `BUILD_MANIFEST.json`). Each build is written to a temporary sibling and swapped in only after it succeeds.

**Stage 2.** `outputs` reads a structurally OK evidence build, applies the op file of every addendum in number order (`curation/amendments/ADD-0N.yaml`; an addendum without one is drafted by `draft` and goes through the same engine), evaluates the register rows at every stage and writes A1–A5. An addendum with an invalid op or an unaccounted provision is **PARTIAL**: it never replaces the last validated state; A1 shows it as a WORKING column and its A5 goes to `out/a5/working/`. A quote that is not in the effective text, a scope leak, an A3 that does not fit one page, or an A5 activity with no row in force is a structural failure: nothing is published, the previous `out/` is kept and the candidate goes to `out.failed`.

**Approvals.** Only a person approves, by running `approve` with their own name; placeholders such as `<name>` are refused, as are readings that fail their checks. An approval pins the review subject: the reading (content, uncertainties, source claims), and its evidence (source PDF, region position, native image). Any change to these makes the reading pending again. `--approvals PATH` writes to another file (used in tests); by default it is `curation/approvals.yaml`, which does not exist yet.

| Path | Contents |
|---|---|
| `sources/candidate_pack/` | The six tender PDFs as received, unaltered (32 pages) |
| `sources/brief/` | The candidate brief as received |
| `sources/correspondence/` | Correspondence received and sent, as provided by the owner |
| `sources/manifest.json` | SHA-256, size and page count for every source file |
| `docs/PLAN.md` | Source findings and the engineering plan (revision 3) |
| `docs/session-03_before-after.md` | Short before/after report on the six gaps found in the owner's Stage 1 review |
| `docs/session-04_report.md` | Session 04: repair evidence, Stage 2 outputs, decisions needed |
| `tenderpack/` | The program. Stage 1: extraction, regions, units, readings, review packets, coverage. Stage 2: citations, amend, draft, dates, register, schedule, render, stage2 |
| `config/` | Pack definition, declared furniture rules, planning assumptions (`assumptions.yaml`: calendar, counting policy, bidder, lead times with basis and owner) |
| `curation/readings/` | Proposed readings of image regions, pending review; approvals go in `curation/approvals.yaml` |
| `curation/amendments/` | Op files for ADD-01 and ADD-02 (proposed ops and dispositions; every provision accounted for) |
| `curation/register/` | The A1 slice (`rows.yaml`), open issues (`issues.yaml`), machine-written pins (`pins.yaml`) |
| `curation/activity_templates.yaml` | Evidence item → A5 activities (owner, issuer, duration key, dependencies) |
| `build/` | Generated evidence: `units.md`, `coverage.md`, `exclusions.md`, `review/<region>/packet.html` (crops beside readings; also `.md`), `fixture/`, `drill/` and `drill-src/` (ADD-03 drill) |
| `out/` | Stage 2 outputs: `a1/` (xlsx, csv, json), `a2/` (md, csv, json), `a3/a3.pdf`, `a5/` (programme, marshalling, replan deltas), `checks.json`, `README.md` |
| `out-drill/` | The same outputs for the pack plus the synthetic ADD-03 (PARTIAL; validated state stays ADD-02) |
| `tests/` | Tests, golden expectations written from the rendered pages, synthetic fixture builder |
| `worklog/` | Timestamped development log: prompts, actions, errors and corrections |
