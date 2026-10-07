#!/bin/bash
S=/tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s14/merge
cd /home/user/tender-pack-reader
time .venv/bin/python -m pytest -q -p no:cacheprovider --basetemp=$S/pt14 --durations=8 tests/test_session14_*.py tests/test_session13_audit_fixes.py tests/test_session13_quick_review.py tests/test_session12_closed_window.py
