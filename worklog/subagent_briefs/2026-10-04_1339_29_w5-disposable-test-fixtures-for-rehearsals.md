# Subagent brief 29: W5: disposable test fixtures for rehearsals

Launched 2026-10-04 13:39:43 UTC; model option requested: `opus`; subagent type: `general-purpose`.
The text below is the prompt exactly as sent by the coordinator (exported from the session transcript on 4 Oct 2026, session 11).

---

You are W5, an implementation subagent in the `tender-pack-reader` repository (/home/user/tender-pack-reader; Python; `.venv/bin/python`; tests with `.venv/bin/python -m pytest -q -p no:cacheprovider <files>`). First state which model you are running as (call the claude-code-remote `get_session` tool with no session id if available) and report it in your final message.

TASK (the owner's section 5: "Make the tests generate disposable evidence fixtures instead of relying on ignored rehearsal build folders"). Today several tests read `rehearsals/blind-0N/build/` (gitignored, present only when a rehearsal was run in this checkout) directly, or use it when present and otherwise ingest into tmp (`_rehearsal` helpers in `tests/test_session09_clarify.py`, `tests/test_session09_pdd_flow.py`, `tests/test_session09_blind03_postkey_fixes.py`; direct reads of `B / "build/units.json"` in `tests/test_session09_blind03_live_fixes.py`; search all of `tests/` for `/build` and `rehearsals/` uses, including session 06–08 tests and `tests/test_blind02_live_fixes.py`).
1. Add a shared, session-scoped pytest fixture in `tests/conftest.py` (create it if absent; if present, extend it): `rehearsal_build(name)` that ALWAYS ingests the rehearsal pack (`rehearsals/<name>/work/pack.yaml`) into a disposable folder under `tmp_path_factory` once per session and returns its path (about 13 s per rehearsal); also `rehearsal_run(name)` returning `stage2.run(build, pack, ROOT)` cached per session. Make it available as parametrised fixtures `blind01_build`, `blind02_build`, `blind03_build` (and the `_run` variants). Never read `rehearsals/*/build` in tests again; never write into `rehearsals/*/`.
2. Convert every test that used those folders to the fixtures. Keep each test's assertions unchanged (if an assertion depended on a stale rehearsal build, say so). Keep the real pack's committed `build/` usage as it is (it is committed, not ignored).
3. Run every converted test file and report the results and the added session time. Also run `tests/test_session09_blind03_live_fixes.py` and `tests/test_session09_blind03_postkey_fixes.py` after conversion; they are used by other agents' work, so convert them carefully.
4. Make sure the fixtures work when the test session runs from a fresh checkout without any rehearsal build (simulate by passing a nonexistent `rehearsals/<name>/build` — simply do not read it).

RULES: you own `tests/conftest.py` and the test files you convert (only the fixture usage lines; other agents W1–W4 are writing NEW test files `tests/test_session10_*.py` at the same time — do not touch those, and do not touch `tenderpack/` code at all). Never use the Write tool on an existing file; Edit only, re-read right before editing. Do NOT run git commit/push. Do not run the full suite (38 minutes); run the converted files.

REPORT: your model; the fixture API; the list of converted files; the results; the per-session cost of the fixtures; anything that could not be converted and why.
