# tender-pack-reader

Working repository for the Lamar Holding PPP AI Partner Round 2 assessment.

**Status:** Stage 1 (evidence and units) implemented and revised after the owner's review (session 03); **not yet accepted by the owner**. Both image readings are **pending the owner's review**; nothing has been approved. Stages 2–6 of `docs/PLAN.md` (revision 3) are **proposed**.

```
make setup      # once, needs network: creates .venv from uv.lock
make evidence   # rebuild build/ (the pack) and build/fixture/ (synthetic mixed example); offline
make test       # pytest
make verify     # tests + two clean rebuilds in disposable directories, compared by hash
python -m tenderpack ingest [--require-approved]                   # build; see exit codes below
python -m tenderpack show "VOL-I:8.5#fn12"                         # a unit, its page and a highlighted crop
python -m tenderpack approve VOL-IV-p6-r1 --reviewer "Your Name"   # run by the reviewer only
```

**`ingest` exit codes.** `0`: structure OK; readings may still be pending, which is printed as PENDING HUMAN REVIEW and carried on every unit derived from them. `2`: STRUCTURAL FAILURE (any of checks C01–C10 failed, e.g. duplicate unit IDs, a span in two units, unit text that does not match its spans, an unread region), or an output path that was refused. The previous build is kept and the failed one is written to `<out>.failed`. `3`: structure OK, but readings are pending and `--require-approved` was given.

**Output safety.** `--out` may not be the repository, a parent of it, home, `/`, a protected folder (`sources`, `config`, `curation`, `tenderpack`, `tests`, `docs`, `worklog`, `.git`, `.venv`) or anything that contains or lies inside an input. An existing directory is replaced only if it is empty or a previous build (`.tenderpack-build` or `BUILD_MANIFEST.json`). Each build is written to a temporary sibling and swapped in only after it succeeds.

**Approvals.** Only a person approves, by running `approve` with their own name; placeholders such as `<name>` are refused, as are readings that fail their checks. An approval pins the review subject: the reading (content, uncertainties, source claims), and its evidence (source PDF, region position, native image). Any change to these makes the reading pending again. `--approvals PATH` writes to another file (used in tests); by default it is `curation/approvals.yaml`, which does not exist yet.

| Path | Contents |
|---|---|
| `sources/candidate_pack/` | The six tender PDFs as received, unaltered (32 pages) |
| `sources/brief/` | The candidate brief as received |
| `sources/correspondence/` | Correspondence received and sent, as provided by the owner |
| `sources/manifest.json` | SHA-256, size and page count for every source file |
| `docs/PLAN.md` | Source findings and the engineering plan (revision 3) |
| `docs/session-03_before-after.md` | Short before/after report on the six gaps found in the owner's Stage 1 review |
| `tenderpack/` | The program (Stage 1: extraction, regions, units, readings, review packets, coverage) |
| `config/` | Pack definition and declared furniture rules (header, footer, watermark) |
| `curation/readings/` | Proposed readings of image regions, pending review; approvals go in `curation/approvals.yaml` |
| `build/` | Generated evidence: `units.md`, `coverage.md`, `exclusions.md`, `review/<region>/packet.html` (crops beside readings; also `.md`), `fixture/` |
| `tests/` | Tests, golden expectations written from the rendered pages, synthetic fixture builder |
| `worklog/` | Timestamped development log: prompts, actions, errors and corrections |
