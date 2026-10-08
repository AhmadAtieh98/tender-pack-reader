"""Session 14 (coordinator; the full suite on the frozen code, test_session10_routes's Ollama case): the size planner
judges a request to fit counting the planner's output estimate (requests.context_fits), but the request loop reserved
the whole per-call output cap (16,000 tokens) against the usable context and refused the call the planner had admitted.
With session 14's fuller contract (the payload types printed once in `schema_defs`), one provision on Ollama's default
32,768-token context was refused at turn 1 before any call. The loop now reserves what room is left, never less than
the planner's estimate, and still refuses (never truncates) when even that does not fit."""
from __future__ import annotations

import pytest

from tenderpack.ai import requests as Q


def test_the_output_reservation_is_the_room_left_never_less_than_the_estimate():
    assert Q.output_reservation(None, 50_000, 16_000, 2_200) == 16_000      # no known bound: the cap as configured
    assert Q.output_reservation(40_000, 10_000, 16_000, 2_200) == 16_000    # room for the whole cap
    assert Q.output_reservation(29_491, 14_378, 16_000, 2_200) == 15_113    # the Ollama case: the room left
    with pytest.raises(Q.ContextExhausted):
        Q.output_reservation(29_491, 28_000, 16_000, 2_200)                 # not even the estimate fits: refused
