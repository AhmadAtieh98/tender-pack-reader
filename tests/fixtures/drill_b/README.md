# Drill B curation (rehearsal of the live-session step)

Synthetic, not tender content. `make_drill_b.py` builds a second "Addendum No. 3". The pattern drafter proposes
ops for what it recognises and leaves the rest unresolved; these files are what the assistant, playing the
person who curates during the session, wrote for the rest. Every op and row stays PROPOSED: nothing here is
an approval. `tests/test_drill_b.py` replays them in a disposable copy and checks the outcome.

- `ADD-03.yaml`         the curated op file (the drafter's ops kept as drafted; the unresolved provisions treated)
- `rows-ADD-03.yaml`    rows for the obligations ADD-03 creates (certificates of good standing; new Clause 4.4)
- `evidence-ADD-03.yaml` the new evidence item, `templates-ADD-03.yaml` its A5 activities,
  `lead-times-ADD-03.yaml` the PROVISIONAL lead time they use
