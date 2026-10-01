# tender-pack-reader

Working repository for the Lamar Holding PPP AI Partner Round 2 assessment.

**Status:** Stage 1 (evidence and units) implemented. Image readings are **pending human review**. Stages 2–6 of `docs/PLAN.md` are **proposed**.

```
make setup      # once, needs network: creates .venv from uv.lock
make evidence   # rebuild build/ (the pack) and build/fixture/ (synthetic mixed example); offline
make test       # pytest
make verify     # tests + two clean rebuilds compared by hash
python -m tenderpack show "VOL-I:8.5#fn12"                      # a unit, its page and a highlighted crop
python -m tenderpack approve VOL-IV-p6-r1 --reviewer "<name>"    # a person approves a reading
```

| Path | Contents |
|---|---|
| `sources/candidate_pack/` | The six tender PDFs as received, unaltered (32 pages) |
| `sources/brief/` | The candidate brief as received |
| `sources/correspondence/` | Correspondence received and sent, as provided by the owner |
| `sources/manifest.json` | SHA-256, size and page count for every source file |
| `docs/PLAN.md` | Source findings and the engineering plan (revision 2) |
| `tenderpack/` | The program (Stage 1: extraction, regions, units, readings, review packets, coverage) |
| `config/` | Pack definition and declared furniture rules (header, footer, watermark) |
| `curation/readings/` | Proposed readings of image regions, pending review; approvals go in `curation/approvals.yaml` |
| `build/` | Generated evidence: `units.md`, `coverage.md`, `exclusions.md`, `review/<region>/packet.md`, `fixture/` |
| `tests/` | Tests, golden expectations written from the rendered pages, synthetic fixture builder |
| `worklog/` | Timestamped development log: prompts, actions, errors and corrections |
