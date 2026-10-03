# Blind rehearsal 01: an independently written Addendum No. 3

**Synthetic, not tender content.** An independent subagent wrote the addendum from the sources and the brief, without seeing the implementation. Its answer key was frozen by hash before the rehearsal started (`FROZEN.md`, commit `53ad76f`).

| Path | What it is |
|---|---|
| `input/ADD-03_Addendum_No_3.pdf` | The blind addendum, as received |
| `FROZEN.md` | Hashes of the addendum and of the sealed answer key, committed before the rehearsal |
| `SEALED/` | The answer key, author notes and builder script, added unchanged after the rehearsal (`sha256sum -c SEALED/SHA256SUMS`) |
| `setup_pack.py` | Builds `work/`: the received pack plus ADD-03, with copies of the curation, so the real `curation/` and `config/` stay untouched |
| `work/` | The rehearsal's curation: `amendments/ADD-03.yaml`, the register with the new and re-made rows, `issues/ADD-03.yaml`, replanned assumptions |
| `drafted-ADD-03.yaml`, `drafted-ADD-03.v2.yaml` | What `tenderpack draft` proposed before and after live fix 1 |
| `out-drafted/` | Working draft with ADD-03 drafted (PARTIAL): published blind |
| `out-curated/` | Working draft with ADD-03 curated (APPLIED, replanned): published blind, **the scored output** |
| `diff-ADD-02-to-ADD-03.md` | `tenderpack diff` output, written blind |
| `out-after-fixes/` | The same pack after the post-comparison fixes (renumbering, summary currency, A3 pointers); not scored |
| `clock.txt`, `*.log` | Wall-clock timestamps and command logs |
| `COMPARISON.md` | Results against the answer key, with the timeline |

## Reproduce

These commands rebuild the evidence (`build/` is not committed) and the outputs:

```
python rehearsals/blind-01/setup_pack.py          # only on a fresh checkout without work/ (work/ is committed)
python -m tenderpack ingest --pack rehearsals/blind-01/work/pack.yaml --out rehearsals/blind-01/build
python -m tenderpack outputs --evidence rehearsals/blind-01/build --pack rehearsals/blind-01/work/pack.yaml --out /tmp/blind-out
python -m tenderpack diff --evidence rehearsals/blind-01/build --pack rehearsals/blind-01/work/pack.yaml
```

Nothing here is reviewed or accepted. Every op and row is PROPOSED.
