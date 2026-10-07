"""Session 13 (part 2, item 4): the host session's rules no longer drop the no_effect safeguard.

HOST_RULES said "they replace rule 9 above", but rule 9 of controller.SYSTEM is the no_effect safeguard and rule 10 is
the reply format: on the host route the safeguard was dropped (by the words) and the contradictory "reply with ONLY the
JSON" stayed beside "Do not reply with the JSON itself". The composition now lives in one function
(hostsession.compose_host_system): a host session that SUBMITS through a tool replaces the phase's reply-format rule,
found by what it says (never by number), and keeps every other rule; an answer session (readings, downstream: the final
message is the answer) keeps every rule."""
from __future__ import annotations

import re

import pytest

from tenderpack.ai import controller, hostsession as hs
from tenderpack.ai import downstream as DS
from tenderpack.ai import regionread as RR
from tenderpack.ai import workflow as W

RULE9 = "A no_effect disposition says the provision changes nothing"


def _rules(text: str) -> dict[str, str]:
    return {m.group(1): m.group(2) for m in re.finditer(r"^(\d+)\. (.*)$", text, re.M)}


def test_the_analysis_host_prompt_keeps_rule_9_and_does_not_ask_for_a_json_only_reply():
    p = hs.HostSession.system_prompt(None)
    assert RULE9 in p
    assert "reply with ONLY the JSON" not in p and "replace rule 9" not in p, p[-1200:]
    kept = _rules(p)
    base = _rules(controller.SYSTEM)
    assert all(kept.get(k) == v for k, v in base.items() if "reply with ONLY" not in v), sorted(kept)
    assert "submit_proposals" in p and "Do not reply with the JSON itself" in p


@pytest.mark.parametrize("system,rules", [(DS.SYSTEM, W.DOWNSTREAM_HOST_RULES), (RR.SYSTEM, W.READING_HOST_RULES)])
def test_an_answer_session_keeps_every_rule(system, rules):
    p = hs.compose_host_system(system, rules, submits=False)
    assert _rules(p) == _rules(system) and p.endswith(rules)


def test_a_system_without_exactly_one_reply_rule_is_refused_not_guessed():
    with pytest.raises(ValueError, match="reply-format rule"):
        hs.compose_host_system("Rules:\n1. Cite exact words.", hs.HOST_RULES, submits=True)
