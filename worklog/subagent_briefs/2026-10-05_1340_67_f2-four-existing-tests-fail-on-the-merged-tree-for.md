# Follow-up message 67: F2: four existing tests fail on the merged tree for the same fit cause

Sent 2026-10-05 13:40:36 UTC to agent `a082fe6c640f6d4f6` (a resume or an added instruction to an agent launched earlier; the agent's brief is the launch file it belongs to).
The text below is the message exactly as sent (exported from the session transcript on 5 Oct 2026, session 12).

---

F2, for the same follow-up: the merged tree's test run (`scratchpad/s12/logs/merge_fixers_all.log`, 286 passed, 4 failed) shows the four tests your fit fix must turn green, all for the one cause: `tests/test_session12_signals_fixes.py::test_a3_2_every_unresolved_line_carries_its_reason` (I-READING-T24's short is '' on the real page), `::test_a3_4_the_window_end_shows_both_readings_and_medium_confidence_points_to_its_reason` (the attendance line's short is ''), `tests/test_session11_audit_a3.py::test_a3_1_every_listed_issue_shows_its_reason_and_owner_on_the_one_page` (I-F4A-FIELDS' short not on the page), and `tests/test_session06_review.py::test_a3_condenses_in_labelled_steps_and_never_drops_a_disqualifier`, which now raises `A3OverflowError: A3 content does not fit on one A4 page at scale >= 0.9 (18 items, 9 unresolved)` on blind-02's synthetic page, so the added legend/labels/banner enlarge the synthetic pages too: the shortening must be general (the legend only for abbreviations used on the page, the marker short, headings trimmed) and the blind-02 page must fit again without weakening that test. Include these four in your report's results.
